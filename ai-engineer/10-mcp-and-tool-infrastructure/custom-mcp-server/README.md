# Custom MCP Server

A minimal **Model Context Protocol (MCP)** server that exposes custom tools for AI models to call. MCP is a standard protocol for connecting AI models to external tools and data sources.

## What it does

Defines two tools that any MCP-compatible client can discover and invoke:

| Tool | Description |
|---|---|
| `get_current_time` | Returns the current system time with optional timezone offset |
| `calculate_compound_interest` | Computes compound interest given principal, rate, and years |

## How MCP works

```
MCP Client (Claude Desktop, custom client, etc.)
    |
    |  JSON-RPC over stdio
    v
MCP Server (this project)
    |
    +-- Tool: get_current_time(timezone_offset)
    +-- Tool: calculate_compound_interest(principal, rate, years)
```

1. The client connects to the server and requests the list of available tools.
2. The server returns tool names, descriptions, and parameter schemas.
3. When the LLM decides to call a tool, the client sends a JSON-RPC request.
4. The server executes the function and returns the result.

## Key concepts

- **Model Context Protocol (MCP)** -- an open standard for connecting AI models to external tools and data. It defines how clients discover tools, send requests, and receive responses.
- **FastMCP** -- a high-level Python wrapper that handles protocol details (JSON-RPC, tool discovery, parameter validation). You write plain functions with `@mcp.tool()` and FastMCP does the rest.
- **Tool registration** -- the `@mcp.tool()` decorator registers a function as an MCP tool. The function's type hints define the parameter schema, and the docstring becomes the tool description.
- **Stdio transport** -- by default, MCP servers communicate via stdin/stdout, which is how local tools integrate with clients like Claude Desktop.
- **Why this matters** -- MCP lets you extend any compatible AI model with custom capabilities without modifying the model itself. Write a server once, connect it to any MCP client.

## Prerequisites

- Python 3.10+
- No API keys needed

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
