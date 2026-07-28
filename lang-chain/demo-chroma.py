import chromadb
# from chromadb.utils import embedding_functions

# 使用 sentence-transformers
# ef = embedding_functions.SentenceTransformerEmbeddingFunction(
#     model_name="BAAI/bge-small-zh-v1.5"
# )

# 创建一个持久化客户端，数据将保存在 "./chroma_db" 目录下
client = chromadb.PersistentClient(path="./chroma_db")

# 如果名为 "my_collection" 的集合不存在，则创建；否则直接获取
collection = client.get_or_create_collection(
    name="my_collection",
    # embedding_function=ef
)

collection.add(
    ids=[
        "doc1",
        "doc2"
    ],
    documents=[
        "Python 是一种高级编程语言",
        "ChromaDB 是一个向量数据库"
    ]
)

result = collection.query(
    query_texts=[
        "什么是 Python?"
    ],
    n_results=2
)

print(result)