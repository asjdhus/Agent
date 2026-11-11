import sqlite3
from langchain.agents import create_agent
from model.factory import chat_model
from utils.prompt_loader import load_system_prompt,load_report_prompt
from agent.tools.agent_tools import rag_summarize,get_weather,get_user_location,get_user_id,get_current_month,fetch_external_data,fill_context_for_report
from agent.tools.middleware import monitor_tool,log_before_model,report_prompt_switch
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv

load_dotenv()
class ReactAgent:
    def __init__(self):
        conn=sqlite3.connect("checkpoints.db",check_same_thread=False)
        checkpointer=SqliteSaver(conn)
        self.agent=create_agent(
            model=chat_model,
            system_prompt=load_system_prompt(),
            tools=[rag_summarize,get_weather,get_user_location,get_user_id,get_current_month,fetch_external_data,fill_context_for_report],
            middleware=[monitor_tool,log_before_model,report_prompt_switch],
            checkpointer=checkpointer,
        )
        self.config={"configurable":{"thread_id":"default"}}
        
    def execute_stream(self,query:str,thread_id:str="default"):
        self.config["configurable"]["thread_id"]=thread_id
        input_dict={"messages":[{"role":"user","content":query}]}
        for chunk in self.agent.stream(input_dict,config=self.config,stream_mode="values",context={"report":False}):  #config传thread_id，checkpointer按会话持久化状态
            latest_message=chunk["messages"][-1]
            if latest_message.content:
                yield latest_message.content.strip()+"\n"          #返回的还是一个迭代器

    def get_history(self,thread_id:str="default")->list:
        self.config["configurable"]["thread_id"]=thread_id
        snapshot=self.agent.get_state(self.config)
        result=[]
        if snapshot and snapshot.values:
            for msg in snapshot.values.get("messages",[]):
                if msg.type=="human":
                    role="user"
                elif msg.type=="ai":
                    role="assistant"
                else:
                    continue
                if msg.content:
                    result.append({"role":role,"content":msg.content})
        return result
            

# if __name__ == "__main__":
#     agent=ReactAgent()
#     for chunk in agent.execute_stream("生成使用报告"):
#         print(chunk, end="",flush=True)