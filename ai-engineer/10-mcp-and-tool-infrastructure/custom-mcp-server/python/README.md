# Custom MCP Server -- Python

Python implementation using the `mcp` library's `FastMCP` high-level wrapper.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The server starts and listens for MCP connections via stdio (stdin/stdout). Connect an MCP client to interact with the tools.

## Testing with Claude Desktop

Add this to your Claude Desktop MCP configuration:

```json
{
  "mcpServers": {
    "test-tools": {
      "command": "python",
      "args": ["path/to/main.py"]
    }
  }
}
```

## Dependencies

- `mcp` -- Model Context Protocol SDK with `FastMCP` high-level server wrapper
