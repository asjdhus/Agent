from langchain_core.tools import tool
from rag.rag_service import RagSummraizeService
import random
from utils.config_handler import agent_config 
from utils.path_tool import get_abs_path
import os
from utils.logger_handler import logger

rag=RagSummraizeService()
user_ids=["1001","1002","1003","1004","1005","1006","1007","1008","1009","1010"]
month_arr=["2025-01","2025-02","2025-03","2025-04","2025-05","2025-06","2025-07","2025-08","2025-09","2025-10","2025-11","2025-12"]
external_data={}


@tool(description="从向量存储中检索参考资料")
def rag_summarize(query:str)->str:
    return rag.rag_summarize(query)

@tool(description="获取城市的天气,以消息字符串形式返回")
def get_weather(city:str)->str:
    return f"{city}的天气晴朗,温度22摄氏度,湿度60%,风速10km/h"


@tool(description="获取用户所在城市的名称,以字符串形式返回")
def get_user_location()->str:
    return random.choice(["北京","上海","广州","深圳"])


@tool(description="获取用户id,以字符串形式返回")
def get_user_id()->str:
    return random.choice(user_ids)

@tool(description="获取当前月份，以字符串形式返回")
def get_current_month()->str:
    return random.choice(month_arr)


def generate_external_data():         #user_id1,user_id2,user_id3,...是user_ids里面的元素
                                      #month1,month2,month3,...是month_arr里面的元素
    """
    这个函数的目标是填充external_data,使最终external_data=                             
    {
        "user_id1":{
                    "month1":{"特征":xxx,"效率":xxx}
                    "month2":{"特征":xxx,"效率":xxx}
                    "month3":{"特征":xxx,"效率":xxx}
            ...
        }
        "user_id2":{
                    "month1":{"特征":xxx,"效率":xxx}
                    "month2":{"特征":xxx,"效率":xxx}
                    "month3":{"特征":xxx,"效率":xxx}
                    ...
                }
        "user_id3":{
                    "month1":{"特征":xxx,"效率":xxx}
                    "month2":{"特征":xxx,"效率":xxx}
                    "month3":{"特征":xxx,"效率":xxx}
                    ...
                }
        ...
    }
    """
    if not external_data:
        external_data_path=get_abs_path(agent_config["external_data_path"])
        if not os.path.exists(external_data_path):
            raise FileNotFoundError(f"外部数据文件不存在:{external_data_path}")
        with open(external_data_path,"r",encoding="utf-8") as f:
            for line in f.readlines()[1:]:   #跳过第一行,因为是表头,从第二行开始
                arr:list[str]=line.strip().split(",")
                user_id:str=arr[0].replace('"',"")    #去掉双引号
                feature:str=arr[1].replace('"',"")    
                efficiency:str=arr[2].replace('"',"")    
                consumables:str=arr[3].replace('"',"")   
                comparison:str=arr[4].replace('"',"")   
                time:str=arr[5].replace('"',"")   
                
                if user_id not in external_data:
                    external_data[user_id]={}         #先看external_data是否有这一行的这个user_id的这个key，没有则创建一个key为这个user_id的空字典,这个user_id每一行可能不同,可能是user_id1,user_id2,user_id3等,每个user_id对应一个字典
                
                external_data[user_id][time]={          #这里的time是月份,比如2025-01,就是month_arr里面的元素
                    "特征":feature,
                    "效率":efficiency,
                    "耗材":consumables,
                    "对比":comparison
                }
                
                
@tool(description="从外部系统中获取指定用户指定月份的使用记录，以字符串形式返回,如果未检索到返回空字符串")
def fetch_external_data(user_id:str,month:str)->str:
    generate_external_data()
    
    try:
        return external_data[user_id][month]
    except KeyError:
        logger.warning(f"用户{user_id}在{month}没有使用记录")
        return ""
    
    
@tool(description="无入参，无返回值，调用后触发中间件，自动为报告生成的场景动态注入上下文信息，为后续提示词切换提供上下文信息")
def fill_context_for_report():
    return "fill_context_for_report已调用"
        

# if __name__=="__main__":
#     generate_external_data()
#     print(external_data)
#     print(fetch_external_data("1001","2025-01"))
        
    



