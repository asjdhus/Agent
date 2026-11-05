from .config_handler import prompts_config
from .path_tool import get_abs_path
from .logger_handler import logger

def load_system_prompt():
    try:
        system_prompt_path=get_abs_path(prompts_config["main_prompt_path"])
    except KeyError as e:
        logger.error(f"获取系统提示失败,没有main_prompt_path配置")
        raise e
    
    try:
        return open(system_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"获取系统提示失败system_prompt_path不存在")
        raise e

def load_rag_prompt():
    try:
        rag_prompt_path=get_abs_path(prompts_config["rag_summarizer_prompt_path"])
    except KeyError as e:
        logger.error(f"获取RAG提示失败,没有rag_summarizer_prompt_path配置")
        raise e
    
    try:
        return open(rag_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"获取RAG提示失败rag_summarizer_prompt_path不存在")
        raise e
    
    
def load_report_prompt():
    try:
        report_prompt_path=get_abs_path(prompts_config["report_prompt_path"])
    except KeyError as e:
        logger.error(f"获取报告提示失败,没有report_prompt_path配置")
        raise e
    
    try:
        return open(report_prompt_path,"r",encoding="utf-8").read()
    except Exception as e:
        logger.error(f"获取报告提示失败report_prompt_path不存在")
        raise e