from mcp.server import MCPServer


server = MCPServer(
    "mcp-server-test"
)


@server.tool()
def hello(name: str) -> str:
    """
    返回问候
    """

    return f"Hello {name}"



@server.tool()
def add(a: int, b: int) -> int:
    """
    两数相加
    """

    return a + b



if __name__ == "__main__":
    print("mcp server starting on http://127.0.0.1:8000/sse")
    server.run(transport="sse", host="127.0.0.1", port=8000)