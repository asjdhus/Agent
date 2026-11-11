from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt,load_report_prompt
from agent.tools.agent_tools import rag_summarize,get_weather,get_user_location,get_user_id,get_current_month,fetch_external_data,fill_context_for_report
from agent.tools.middleware import monitor_tool,log_before_model,report_prompt_switch
from dotenv import load_dotenv

load_dotenv()
class ReactAgent:
    def __init__(self):
        self.agent=create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize,get_weather,get_user_location,get_user_id,get_current_month,fetch_external_data,fill_context_for_report],
            middleware=[monitor_tool,log_before_model,report_prompt_switch],
        )
        
    def execute_stream(self,query:str,history:list=None):
        messages=[]
        if history:
            for msg in history:
                messages.append({"role":msg["role"],"content":msg["content"]})
        messages.append({"role":"user","content":query})
        input_dict={"messages":messages}
        for chunk in self.agent.stream(input_dict,stream_mode="values",context={"report":False}):  #第三个参数context就是上下文runtime中的信息,就是做提示词切换的标记
            latest_message=chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip()+"\n"          #返回的还是一个迭代器
            

# if __name__ == "__main__":
#     agent=ReactAgent()
#     for chunk in agent.execute_stream("生成使用报告"):
#         print(chunk, end="",flush=True)