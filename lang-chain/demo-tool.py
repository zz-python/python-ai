# 安装依赖: pip install langchain langchain-openai

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.tools import tool
from util.config import config

@tool
def get_jiaguwen_lang(
    text:str
):
    """
    将传入的文本翻译成甲骨文
    """
    return "甲骨文xxxxxxxxxxxxxxxxx"

tools=[
    get_jiaguwen_lang
]

# 1. 定义提示词模板 (Prompt)
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的翻译官，请将用户输入的文本从 {source_lang} 翻译成 {target_lang}。"),
    ("human", "{text}")
])

# 2. 初始化模型 (Model)
# 注意: 需要设置环境变量 OPENAI_API_KEY，或在这里传入 openai_api_key="your-key"
llm = ChatOpenAI(
    base_url="https://api.deepseek.com",  # DeepSeek API 地址
    api_key=config.OPENAI_API_KEY,        # 替换成你的真实密钥
    model="deepseek-v4-pro",                    # DeepSeek 模型名称
    temperature=0.7,                          # 控制随机性，0-1之间
)

agent=create_agent(
    model=llm,
    tools=tools
)

# 3. 构建链 (Chain)
# LCEL 用管道符 | 将组件串联起来，形成清晰的流转 pipeline
chain = prompt | agent

# 4. 运行并获取结果
response = chain.invoke({
    "source_lang": "中文",
    "target_lang": "甲骨文",
    "text": "你好，今天天气不错。"
})

print(response)
