from mcp.server import MCPServer


server = MCPServer(
    "mcp-stdio-test"
)

@server.tool()
def get_weather(city: str) -> str:
    """
    查询城市天气

    Args:
        city:
            城市名称
    """

    weather = {
        "北京": "晴天 25℃",
        "上海": "多云 28℃",
        "深圳": "小雨 30℃"
    }

    return weather.get(
        city,
        "暂无天气信息"
    )



if __name__ == "__main__":
    server.run(transport="stdio")