from abc import ABC, abstractmethod
from typing import Optional
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.embeddings import Embeddings
from langchain_community.chat_models.tongyi import BaseChatModel
from utils.config_handler import rag_config
from dotenv import load_dotenv
load_dotenv()


class BaseModelFactory(ABC):
    @abstractmethod
    def generation(self)->Optional[Embeddings|BaseChatModel]:
        pass
    
    
class ChatModelFactory(BaseModelFactory):
    def generation(self)->Optional[BaseChatModel]:
        return ChatTongyi(model=rag_config["chat_model_name"])
    
class EmbeddingModelFactory(BaseModelFactory):
    def generation(self)->Optional[Embeddings]:
        return DashScopeEmbeddings(model=rag_config["embedding_model_name"])
    
chat_model=ChatModelFactory().generation()
embedding_model=EmbeddingModelFactory().generation()
