import os
import hashlib
from .logger_handler import logger
from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_core.documents import Document



def get_file_md5_hex(file_path:str):      #获取文件的md5值，和RAG项目一样去重
    if not os.path.exists(file_path):
        logger.error(f"文件不存在：{file_path}")
        return
    if not os.path.isfile(file_path):
        logger.error(f"文件不是文件：{file_path}")
        return
    md5 = hashlib.md5()
    chunk_size = 4096       #4KB分片，避免文件过大爆内存
    try:
        with open(file_path,"rb") as f:    #二进制读取
            while chunk := f.read(chunk_size):
                md5.update(chunk)
        """
        chunk=f.read(chunk_size)
        while chunk:
            md5.update(chunk)
            chunk=f.read(chunk_size)
        """
        return md5.hexdigest()
    except Exception as e:
        logger.error(f"获取文件md5值失败：{file_path}，错误信息：{e}")
        return None
            


def listdir_with_allowed_type(path:str,allowed_types:tuple[str]):    #扫描文件夹，筛选出指定后缀的文件，返回它们的完整路径
    files=[]
    
    if not os.path.isdir(path):
        logger.error(f"路径不是文件夹：{path}")
        return tuple(allowed_types)
    
    for f in os.listdir(path):                   #遍历文件夹内的所有文件
        if f.endswith(allowed_types):            #如果文件后缀在允许的列表中
            files.append(os.path.join(path,f))    #添加到结果列表
    return tuple(files)                            #返回不可变的元组,元素为文件路径

def pdf_loader(file_path:str,password:list[str]=None)->list[Document]:
    return PyPDFLoader(file_path,password=password).load()

def txt_loader(file_path:str)->list[Document]:
    return TextLoader(file_path,encoding="utf-8").load()
