# MCP Client Connection

Connects to the [Custom MCP Server](../custom-mcp-server/) and uses its tools through a **LangGraph ReAct agent**. This is the client side of the MCP architecture -- it discovers tools from the server, converts them into LangChain-compatible objects, and lets an LLM agent call them autonomously.

## How it works

```
MCP Client (this project)
    |
    |  1. Launch server as subprocess
    v
MCP Server (custom-mcp-server)
    |
    |  2. Handshake (protocol version, capabilities)
    v
Client discovers tools:
    - get_current_time
    - calculate_compound_interest
    |
    |  3. Convert to LangChain tools via langchain-mcp-adapters
    v
ReAct Agent (LangGraph + Llama 3.1)
    |
    |  4. Agent reasons about query, calls tools as needed
    v
Final answer using tool results
```

1. The client launches the MCP server as a child process (stdio transport).
2. A session handshake exchanges protocol version and capabilities.
3. `load_mcp_tools` queries the server for available tools and wraps each one as a LangChain Tool.
4. A ReAct agent uses the tools to answer a query that requires both time and math.

## Key concepts

- **MCP client session** -- establishes the connection, performs the handshake, and provides methods to discover and call tools on the server.
- **Stdio transport** -- the client and server communicate over stdin/stdout of the server subprocess. This is the standard local transport for MCP.
- **langchain-mcp-adapters** -- the bridge between MCP and LangChain. `load_mcp_tools` converts MCP tool definitions (name, description, parameter schema) into LangChain Tool objects that agents can call.
- **LangGraph ReAct agent** -- `create_react_agent` builds an agent that reasons in Thought/Action/Observation steps. The MCP tools become its available actions.
- **Async architecture** -- MCP client sessions use async I/O because the stdio transport requires non-blocking subprocess communication.
- **Why this matters** -- MCP decouples tool implementation from tool consumption. The server defines tools once; any MCP client can discover and use them, whether it's Claude Desktop, a custom agent, or this script.

## Prerequisites

- The [custom-mcp-server](../custom-mcp-server/) project must be set up
- [Ollama](https://ollama.com/) running locally with `llama3.1` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
