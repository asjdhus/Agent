"""
yaml
k: v
"""
import yaml
import os
from .path_tool import get_abs_path

#读对应的配置文件，转为字典
def load_rag_config(config_path:str=get_abs_path("config/rag.yml"),encoding:str="utf-8"):
    with open(config_path,"r",encoding=encoding) as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
        return config

def load_chroma_config(config_path:str=get_abs_path("config/chroma.yml"),encoding:str="utf-8"):
    with open(config_path,"r",encoding=encoding) as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
        return config
    
def load_prompts_config(config_path:str=get_abs_path("config/prompts.yml"),encoding:str="utf-8"):
    with open(config_path,"r",encoding=encoding) as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
        return config

def load_agent_config(config_path:str=get_abs_path("config/agent.yml"),encoding:str="utf-8"):
    with open(config_path,"r",encoding=encoding) as f:
        config = yaml.load(f,Loader=yaml.FullLoader)
        return config
    

rag_config = load_rag_config()
chroma_config = load_chroma_config()
prompts_config = load_prompts_config()
agent_config = load_agent_config()
