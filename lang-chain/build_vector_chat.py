import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from util.config import config

load_dotenv()

# 1. 加载Embedding
embedding = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-zh-v1.5"
)

# 2. 加载Chroma
vectorstore = Chroma(
    persist_directory="./chroma_db",
    collection_name="markdown_knowledge_zh",
    embedding_function=embedding
)

# 3. Retriever
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k":4
    }
)

# 4. DeepSeek
llm = ChatOpenAI(
    base_url="https://api.deepseek.com",  # DeepSeek API 地址
    api_key=config.OPENAI_API_KEY,        # 替换成你的真实密钥
    model="deepseek-v4-pro",                    # DeepSeek 模型名称
    temperature=0.7,                          # 控制随机性，0-1之间
)

# 5. Prompt
prompt = ChatPromptTemplate.from_template(
"""
你是一个知识库助手。

请根据下面资料回答问题。

资料:
{context}


问题:
{question}


要求:
1. 只根据资料回答
2. 如果资料没有答案，明确说明不知道
3. 不要编造


"""
)

# 6. 问答
while True:
    question = input(
        "\n问题:"
    )
    if question == "exit":
        break
    docs = retriever.invoke(
        question
    )
    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )
    messages = prompt.invoke(
        {
            "context":context,
            "question":question
        }
    )
    answer = llm.invoke(
        messages
    )
    print(
        "\n答案:"
    )
    print(
        answer.content
    )