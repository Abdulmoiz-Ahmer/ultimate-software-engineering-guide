# MCP Client Connection -- Python

Python implementation using the `mcp` client SDK, `langchain-mcp-adapters`, and `langgraph`.

## Prerequisites

- The [custom-mcp-server](../../custom-mcp-server/python/) must be accessible at `../../custom-mcp-server/python/main.py` (relative to this folder).
- [Ollama](https://ollama.com/) running locally with `llama3.1` pulled.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.1
```

## Run

```bash
python main.py
```

The client launches the MCP server as a subprocess, discovers its tools, builds a ReAct agent, and runs a query that triggers both tools.

## Dependencies

- `mcp` -- MCP client SDK for connecting to servers via stdio transport
- `langchain-mcp-adapters` -- bridges MCP tools into LangChain's tool interface
- `langchain-ollama` -- local Llama 3.1 via Ollama
- `langgraph` -- `create_react_agent` for building a ReAct agent with the MCP tools
