from mcp.server import MCPServer
from db import get_connection, get_table_names, get_table_schema, get_all_schemas
from sql_generator import create_sql_chain, generate_sql, clean_sql_output

server = MCPServer(
    "mcp-server-test"
)

# 初始化 LLM 链（服务启动时创建一次，复用）
sql_chain = create_sql_chain()


@server.tool()
def queryAllTable() -> str:
    """
    列出数据库中所有表名
    """
    conn = get_connection()
    try:
        tables = get_table_names(conn)
        if not tables:
            return "数据库中没有任何表。"
        return f"数据库中共有 {len(tables)} 张表:\n" + "\n".join(f"  - {t}" for t in tables)
    finally:
        conn.close()


@server.tool()
def queryTableSchema(table_name: str) -> str:
    """
    查看指定表的 CREATE TABLE 语句（DDL）

    Args:
        table_name: 表名
    """
    conn = get_connection()
    try:
        schema = get_table_schema(conn, table_name)
        return schema
    except ValueError as e:
        return f"❌ {e}"
    finally:
        conn.close()


@server.tool()
def queryGenerateSql(requirement: str) -> str:
    """
    根据自然语言需求生成 SQL 查询语句

    Args:
        requirement: 自然语言描述的查询需求，例如 "查询所有用户" 或 "查找2024年之后注册的用户"
    """
    conn = get_connection()
    try:
        table_schemas = get_all_schemas(conn)
        raw_sql = generate_sql(sql_chain, table_schemas, requirement)
        sql = clean_sql_output(raw_sql)
        return f"[生成的 SQL]\n{sql}"
    finally:
        conn.close()


if __name__ == "__main__":
    print("mcp server starting on http://127.0.0.1:8000/sse")
    server.run(transport="sse", host="127.0.0.1", port=8000)