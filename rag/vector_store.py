from langchain_chroma import Chroma
from utils.config_handler import chroma_config 
from model.factory import embedding_model
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from utils.path_tool import get_abs_path
from utils.file_handler import txt_loader,pdf_loader,listdir_with_allowed_type,get_file_md5_hex
from utils.logger_handler import logger
from langchain_core.documents import Document

class VectorService:
    def __init__(self):
        self.vector_store = Chroma(                                   #创建chroma对象方便后续存储以及检索向量
            collection_name=chroma_config["collection_name"],
            embedding_function=embedding_model,
            persist_directory=get_abs_path(chroma_config["persist_directory"]),
        )
        self.splitter = RecursiveCharacterTextSplitter(                   #创建文本分割器，用于将文本分割成多个向量
            chunk_size=chroma_config["chunk_size"],
            chunk_overlap=chroma_config["chunk_overlap"],
            length_function=len,
            separators=chroma_config["separators"],
        )
    
    def get_retriever(self):                                        #创建向量检索器对象，用于根据查询向量检索相关向量
        return self.vector_store.as_retriever(search_kwargs={"k": chroma_config["k"]})
    
    def load_documents(self):                             #从数据文件夹读取数据文件，转为向量存入向量库中
        """
        先通过文件的md5值做去重
        """
        def check_md5(file_md5: str):
            if not os.path.exists(get_abs_path(chroma_config["md5_hex_store"])):       #先看存md5值的文件是否存在,如果不存在则创建
                open(get_abs_path(chroma_config["md5_hex_store"]), "w",encoding="utf-8").close()
                return False                                                           #False表示该文件没被处理过
            with open(get_abs_path(chroma_config["md5_hex_store"]), "r",encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() == file_md5:                                             #strip()方法去掉字符串首尾的空格符
                        return True
                return False
            
        def save_md5(file_md5: str):
             with open(get_abs_path(chroma_config["md5_hex_store"]), "a",encoding="utf-8") as f:
                 f.write(file_md5 + "\n")
                 
        def get_file_documents(read_path: str):
            if read_path.endswith(".txt"):
                return txt_loader(read_path)
            if read_path.endswith(".pdf"):
                return pdf_loader(read_path)
            return []
        
        
        allowed_file_path = listdir_with_allowed_type(get_abs_path(chroma_config["data_path"]),
                                                       tuple(chroma_config["allow_knowledge_types"]))
        
        for file_path in allowed_file_path:
             #获取文件的md5值
             file_md5 = get_file_md5_hex(file_path)
             if check_md5(file_md5):
                 logger.info(f"文件{file_path}已存在知识库内，跳过")
                 continue
             try:
                 documents: list[Document] = get_file_documents(file_path)
                 if not documents:
                     logger.warning(f"文件{file_path}读取为空，跳过")
                     continue
                 split_documents: list[Document] = self.splitter.split_documents(documents)
                 if not split_documents:
                     logger.warning(f"文件{file_path}分割为空，跳过")
                     continue
                 self.vector_store.add_documents(split_documents)          #将分割后的向量添加到向量库中
                 save_md5(file_md5)
                 logger.info(f"文件{file_path}已添加到知识库")
             except Exception as e:
                 logger.error(f"文件{file_path}读取失败,错误信息:{e}",exc_info=True)       #exc_info=True表示打印详细的错误信息，如果为False则只打印错误信息，不打印详细的错误信息，
                 continue
             
             
if __name__ == "__main__":
    vector_service = VectorService()
    vector_service.load_documents()
#     retriever = vector_service.get_retriever()
#     results = retriever.invoke("机器人怎么扫地")
#     for result in results:
#         print(result.page_content)
