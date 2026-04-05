# 10 -- MCP and Tool Infrastructure

This module covers the **Model Context Protocol (MCP)** -- an open standard for connecting AI models to external tools and data sources. The first project builds a server that exposes custom tools, and the second project builds a client that discovers those tools and lets an LLM agent call them autonomously.

## Project structure

Each project folder contains a language-agnostic README explaining the concept, with implementation-specific code and instructions inside language subfolders:

```
project-name/
  README.md          # What it does, key concepts, prerequisites
  python/            # Python implementation + setup instructions
    main.py
    requirements.txt
    README.md
  # js/              # (coming soon)
```

## Learning path

### 1. [Custom MCP Server](custom-mcp-server/)

Build a minimal MCP server that exposes two custom tools (time lookup and compound interest calculator). Any MCP-compatible client can discover and call these tools through the standard protocol. Uses FastMCP to handle JSON-RPC, tool discovery, and parameter validation automatically.

**You learn:** How to define MCP tools with `@mcp.tool()`, how the server advertises tools to clients, and how stdio transport works.

**Key concepts:** Model Context Protocol, FastMCP, tool registration, parameter schemas from type hints, stdio transport

---

### 2. [MCP Client Connection](mcp-client-connection/)

Build a client that connects to the MCP server, discovers its tools, converts them into LangChain-compatible objects, and hands them to a LangGraph ReAct agent. The agent reasons about a user query and calls the MCP tools autonomously to produce an answer.

**You learn:** How the client side of MCP works -- launching the server subprocess, performing the handshake, discovering tools, and bridging MCP to LangChain with adapters.

**Key concepts:** MCP client session, stdio subprocess transport, langchain-mcp-adapters, tool discovery, LangGraph ReAct agent, async I/O

## How the two projects connect

```
Project 1: Custom MCP Server          Project 2: MCP Client Connection
  @mcp.tool() definitions    <---->    load_mcp_tools() discovery
  FastMCP + stdio transport  <---->    ClientSession + StdioServerParameters
  Executes tool functions    <---->    ReAct agent calls tools via MCP
```

The server runs as a subprocess of the client. The client launches it, performs a handshake, discovers available tools, and then the agent uses them as needed.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3.1` pulled (project 2)
- No API keys needed

Each project has its own `README.md` with concept explanations, and each language folder has setup instructions.
