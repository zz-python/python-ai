# pip langchain_community install langchain_chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

# 1. 加载 Markdown 文件
loader = DirectoryLoader(
    "./docs",
    glob="**/*.md",
    loader_cls=TextLoader,
    loader_kwargs={
        "encoding": "utf-8"
    }
)

documents = loader.load()

print(
    "Markdown数量:",
    len(documents)
)

# 2. 文本切分
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    # 中文优化
    separators=[
        "\n## ",
        "\n### ",
        "\n\n",
        "\n",
        "。",
        "！",
        "？",
        ""
    ]
)


docs = splitter.split_documents(
    documents
)

print(
    "切分数量:",
    len(docs)
)

# 3. Embedding
# embedding = HuggingFaceBgeEmbeddings(
#     model_name="BAAI/bge-small-zh-v1.5"
# )


# 4. 创建 Chroma
vectorstore = Chroma.from_documents(
    documents=docs,
    # embedding=embedding,
    persist_directory="./chroma_db",
    collection_name="markdown_knowledge"
)

print("Markdown知识库创建完成")

# import chromadb
# client = chromadb.PersistentClient(path="./chroma_db")
# collection = client.get_or_create_collection(
#     name="markdown_knowledge",
#     # embedding_function=ef
# )
# result = collection.query(
#     query_texts=[
#         "什么是 Python?"
#     ],
#     n_results=3
# )

# print(result)