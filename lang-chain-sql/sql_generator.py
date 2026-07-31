# sql_generator.py
# 基于 LangChain 的 SQL 生成模块
# 依赖: pip install langchain langchain-openai
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from config import config

# ============================================================
# Prompt 模板
# ============================================================

SQL_GENERATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """\
你是一个专业的 MySQL 数据库查询助手。你的任务是根据数据库表结构和用户的自然语言需求，生成准确的 SELECT 查询语句。

## 数据库表结构

以下是数据库中所有表的完整结构（DDL）：

{table_schemas}

## 重要规则

1. **只生成 SELECT 查询**：绝对不要生成 INSERT、UPDATE、DELETE、DROP、CREATE、ALTER、TRUNCATE 等任何修改数据或结构的语句。
2. **只返回 SQL**：你的回复中只能包含 SQL 语句本身，不要包含任何解释、注释、分析或 markdown 格式（不要用 ```sql 代码块包裹）。
3. **表名和列名用反引号**：例如 `users`、`orders`，避免与 MySQL 保留字冲突。
4. **使用表结构中的列名**：严格根据上面提供的表结构来引用列，不要凭空编造列名。
5. **考虑 NULL 值**：如果用户要求"查找没有 XX 的记录"，使用 IS NULL 而不是 = NULL。
6. **限制结果数量**：如果用户没有明确指定数量，默认添加 LIMIT 100 避免返回过多数据。
7. **处理模糊需求**：如果用户的描述不明确，选择最合理的解释给出 SQL，不要反问。
8. **字符串匹配**：使用 LIKE 或 = 进行字符串比较，模糊搜索使用 LIKE '%关键词%'。
9. **日期处理**：使用 MySQL 标准的日期函数（DATE()、NOW()、CURDATE()、DATE_SUB()、DATEDIFF() 等）。
10. **JOIN 关联**：如果查询涉及多个表，根据表结构中的外键关系进行 JOIN。
11. **聚合查询**：如果用户要求"统计"、"汇总"、"分组"等，使用 GROUP BY 和适当的聚合函数（COUNT、SUM、AVG、MAX、MIN）。
12. **排序**：如果用户要求"排名"、"前N"、"最多"、"最少"等，使用 ORDER BY 配合 LIMIT。

## 用户需求

{user_requirement}""",
        ),
    ]
)


# ============================================================
# Chain 构建
# ============================================================


def create_sql_chain():
    """
    创建 LangChain SQL 生成链。

    链结构: Prompt → ChatOpenAI → StrOutputParser
    """
    model = ChatOpenAI(
        base_url="https://api.deepseek.com",
        api_key=config.OPENAI_API_KEY,
        model="deepseek-v4-pro",
        temperature=0.1,  # 低温度，确保 SQL 生成的确定性
    )

    chain = SQL_GENERATION_PROMPT | model | StrOutputParser()
    return chain


# ============================================================
# SQL 生成与清洗
# ============================================================


def generate_sql(chain, table_schemas: str, user_requirement: str) -> str:
    """
    调用 LLM 生成 SQL 语句。

    参数:
        chain: LangChain 链对象
        table_schemas: 所有表的 DDL 字符串
        user_requirement: 用户的自然语言需求

    返回:
        生成的原始 SQL 字符串（可能包含 markdown 包裹）
    """
    response = chain.invoke(
        {
            "table_schemas": table_schemas,
            "user_requirement": user_requirement,
        }
    )
    return response


def clean_sql_output(raw: str) -> str:
    """
    清洗 LLM 输出的 SQL 语句。

    处理:
    - 去掉 ```sql ... ``` 或 ``` ... ``` markdown 代码块
    - 去掉首尾空白
    - 去掉尾部分号
    """
    cleaned = raw.strip()

    # 去掉 markdown 代码块包裹 ```sql ... ``` 或 ``` ... ```
    # 匹配开头的 ```sql 或 ``` 以及结尾的 ```
    cleaned = re.sub(r"^```(?:sql)?\s*\n?", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\n?```\s*$", "", cleaned)

    # 去掉首尾空白
    cleaned = cleaned.strip()

    # 去掉尾部分号
    if cleaned.endswith(";"):
        cleaned = cleaned[:-1].strip()

    return cleaned