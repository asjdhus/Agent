"""
RAG服务类,用户提问,搜索参考资料,将提问和参考资料交给模型,让模型总结回复
"""
from rag.vector_store import VectorService
from utils.prompt_loader import load_rag_prompt
from langchain_core.prompts import PromptTemplate
from model.factory import chat_model
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document


class RagSummraizeService(object):
    def __init__(self):
        self.vector_store=VectorService()
        self.retriever=self.vector_store.get_retriever()
        self.prompt_text=load_rag_prompt()
        self.prompt_template=PromptTemplate.from_template(self.prompt_text)
        self.model=chat_model
        self.chain=self.__init_chain()
        
        
    def __init_chain(self):                        #构造链
        chain=self.prompt_template|self.model|StrOutputParser()
        return chain
    
    def retriever_docs(self,query:str)->list[Document]:
        """
        搜索参考资料
        """
        return self.retriever.invoke(query)
    
    def rag_summarize(self,query:str)->str:
        """
        搜索参考资料,将提问和参考资料交给模型,让模型总结回复
        """
        context_docs=self.retriever_docs(query)
        context=""
        for doc in context_docs:
            context+=doc.page_content+"\n"
        return self.chain.invoke({"input":query,"context":context})
    
    
# if __name__=="__main__":
#     rag_service=RagSummraizeService()
#     query="你好"
#     print(rag_service.rag_summarize(query))
"""
遇到导包问题,直接在终端中输入类似于python -m rag.rag_service的命令,具体根据执行文件修改命令，就可以直接执行
"""
    