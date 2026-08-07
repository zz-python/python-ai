# from chromadb.utils import embedding_functions
# from langchain_community.embeddings import HuggingFaceBgeEmbeddings
import os
# 在所有导入和加载模型之前，设置镜像站
# https://huggingface.co/BAAI/bge-small-zh-v1.5/resolve/main/./modules.json
# https://hf-mirror.com/BAAI/bge-small-zh-v1.5/resolve/main/./modules.json
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from langchain_huggingface import HuggingFaceEmbeddings

# 使用 sentence-transformers
# ef = embedding_functions.SentenceTransformerEmbeddingFunction(
#     model_name="BAAI/bge-small-zh-v1.5"
# )
# 1. 加载中文Embedding
ef = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5"
)

