from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from util.config import config


# -------------------------------
# 1. 自定义 Middleware
# -------------------------------

class LoggingMiddleware(AgentMiddleware):

    def before_model(
        self,
        state,
        runtime
    ):
        """
        调用模型之前执行
        """

        print("\n====== before_model ======")

        messages = state["messages"]

        print(
            "当前消息数量:",
            len(messages)
        )

        return state


    def after_model(
        self,
        state,
        runtime
    ):
        """
        模型返回之后执行
        """

        print("\n====== after_model ======")

        last_message = (
            state["messages"][-1]
        )

        print(
            "AI回复:",
            last_message.content
        )
        print("\n----------------------------------")

        return state



# -------------------------------
# 2. Prompt增强 Middleware
# -------------------------------

class SystemPromptMiddleware(
    AgentMiddleware
):

    def before_model(
        self,
        state,
        runtime
    ):

        messages = state["messages"]


        # 如果没有System消息
        # 自动添加

        if not any(
            isinstance(
                m,
                SystemMessage
            )
            for m in messages
        ):

            print("\n====== insert systemMessage======")
            messages.insert(
                0,
                SystemMessage(
                    content=
                    "你是一个专业Python助手，请使用中文回答"
                )
            )


        return state



# -------------------------------
# 3. 创建模型
# -------------------------------

model = ChatOpenAI(
    base_url="https://api.deepseek.com",  # DeepSeek API 地址
    api_key=config.OPENAI_API_KEY,        # 替换成你的真实密钥
    model="deepseek-v4-pro",                    # DeepSeek 模型名称
    temperature=0.7,                          # 控制随机性，0-1之间
)



# -------------------------------
# 4. 创建 Agent
# -------------------------------

agent = create_agent(
    model=model,

    tools=[],

    middleware=[
        LoggingMiddleware(),
        SystemPromptMiddleware()
    ]
)



# -------------------------------
# 5. 调用 Agent
# -------------------------------

result = agent.invoke(
    {
        "messages":[
            (
                "human",
                "解释一下 LangChain Middleware"
            )
        ]
    }
)
print("\n========== 最终结果 ==========")
print(
    result["messages"][-1].content
)

# stream = agent.stream(
#     {
#         "messages":[
#             (
#                 "human",
#                 "解释一下 LangChain Middleware"
#             )
#         ]
#     }
# )
# for chunk in stream:    
#     if "model" in chunk:
#         message = (
#             chunk["model"]["messages"][-1]
#         )
#         print(
#             message.content,
#             end="",
#             flush=True
#         )