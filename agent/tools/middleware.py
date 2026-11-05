from langchain.agents.middleware import wrap_tool_call, before_model, dynamic_prompt, ModelRequest
from langchain.tools.tool_node import ToolCallRequest
from typing import Callable
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from utils.logger_handler import logger
from langchain.agents import AgentState
from langgraph.runtime import Runtime
from utils.prompt_loader import load_system_prompt,load_report_prompt


@wrap_tool_call                   #每次工具调用前自动调用此函数监控
def monitor_tool(                 #工具执行的监控,ToolCallRequest对象见下面的注释
    request:ToolCallRequest,       #请求的数据封装，request和handler都是LangGraph 框架内部自动传入的
    handler:Callable[[ToolCallRequest], ToolMessage|Command],        #执行的函数本身，handler 是一个函数：接收 1 个 ToolCallRequest 类型的参数，返回 ToolMessage 或 Command 类型的结果。
    )->ToolMessage|Command:             
    logger.info(f"执行工具: {request.tool_call['name']}")
    logger.info(f"工具调用参数: {request.tool_call['args']}")
    try:
        result= handler(request)                         #执行工具
        logger.info(f"工具调用成功: {request.tool_call['name']}")
        if request.tool_call['name']=="fill_context_for_report":
            request.runtime.context["report"]=True
        return result                                     #返回工具执行结果,是ToolMessage或Command类型,ToolMessage对象构造见下面注释
    except Exception as e:
        logger.error(f"工具{request.tool_call['name']}调用失败: {e}")
        raise e
    
@before_model
def log_before_model(          #在模型执行前输出日志记录
    state:AgentState,           #智能体的状态信息,state 是 Agent 当前的全部对话历史，由 LangGraph 框架自动传入，不需要手动传
    runtime:Runtime,             #记录整个执行过程中上下文信息
    ):          
    logger.info(f"即将调用模型，有{len(state['messages'])}条消息。")
    logger.debug(f"{type(state['messages'][-1]).__name__}|{state['messages'][-1].content.strip()}")
    return None

@dynamic_prompt                    #每一次在生成提示词之前调用此函数
def report_prompt_switch(request:ModelRequest):         #动态切换提示词
    is_report=request.runtime.context.get("report",False)
    if is_report:                       #是报告生成场景，返回报告生成提示词内容
        return load_report_prompt()
    return load_system_prompt()



"""
构造ToolCallRequest 对象：
       ToolCallRequest(
           tool_call={"name": "get_user_id", "args": {}, "id": "call_xxx"},  #因为有dataclass,所以tool_call,runtime,state都是属性 ,self.tool_call=tool_call
           runtime=Runtime(context={"report": False}),
           state=AgentState(messages=[...]),     
           ...
       )
       
构造ToolMessage 对象：              #是pydantic,类似于dataclass,会自动生成__init__方法
ToolMessage(
    content="工具执行结果字符串",
    tool_call_id="call_abc123",   # 与 request.tool_call['id'] 对应
    name="get_user_id",           # 工具名
)
"""
