from typing import TypedDict, Annotated
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from util.config import config



# =========================
# 1. 定义 State
# =========================

class ChatState(TypedDict):

    # 保存聊天消息
    messages: Annotated[
        list,
        add_messages
    ]

    # 自定义字段
    user_name: str



# =========================
# 2. 创建模型
# =========================

llm = ChatOpenAI(
    base_url="https://api.deepseek.com",  # DeepSeek API 地址
    api_key=config.OPENAI_API_KEY,        # 替换成你的真实密钥
    model="deepseek-v4-pro",                    # DeepSeek 模型名称
    temperature=0.7,                          # 控制随机性，0-1之间
)



# =========================
# 3. 定义节点
# =========================

def chat_node(
    state: ChatState
):

    messages = state["messages"]

    response = llm.invoke(
        messages
    )


    return {

        "messages":[
            AIMessage(
                content=response.content
            )
        ]

    }



# =========================
# 4. 创建 Graph
# =========================

builder = StateGraph(
    ChatState
)


builder.add_node(
    "chat",
    chat_node
)


builder.add_edge(
    START,
    "chat"
)


builder.add_edge(
    "chat",
    END
)



# =========================
# 5. Checkpointer
# =========================

memory = MemorySaver()



graph = builder.compile(
    checkpointer=memory
)



# =========================
# 6. 第一次对话
# =========================

config = {

    "configurable": {

        # 会话ID
        "thread_id":
            "user_001"
    }
}



result1 = graph.invoke(

    {
        "messages":[
            HumanMessage(
                content="我叫张三"
            )
        ],

        "user_name":
            "张三"
    },

    config=config
)


print(
    "第一次:"
)

print(
    result1["messages"][-1].content
)



# =========================
# 7. 第二次对话
# =========================


result2 = graph.invoke(

    {
        "messages":[
            HumanMessage(
                content="我叫什么?"
            )
        ]
    },

    config=config

)


print(
    "\n第二次:"
)

print(
    result2["messages"][-1].content
)