# MCP Demo Server

基于 **MCP 2.0 (Python SDK)** 实现的自定义 MCP 服务，通过 stdio、sse 传输协议与 Claude Code 通信。

## 环境要求

- Python 3.12+
- 已安装 `mcp` 包（`pip install mcp`）

## server-sse启动

```bash
python server-sse.py
```

### Claude对接.mcp.json配置

```json
{
  "mcpServers": {
    "mcp-server-test": {
      "type": "sse",
      "url": "http://127.0.0.1:8000/sse"
    },
    "mcp-tool-test": {
      "command": "python",
      "args": ["e:/projects/python-ai/mcp-server/server-stdio.py"]
    }
  }
}
```
