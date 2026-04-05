"""
MCP Client Connection -- Python

Connects to the custom MCP server from the previous project and uses
its tools through a LangGraph ReAct agent. This demonstrates the full
MCP client-server workflow:

  1. Launch the MCP server as a subprocess (stdio transport).
  2. Establish a client session and perform the protocol handshake.
  3. Discover available tools from the server.
  4. Convert them into LangChain-compatible tool objects.
  5. Wire them into a ReAct agent powered by a local LLM.
  6. The agent reasons about a query and calls the MCP tools as needed.

The key integration layer is langchain-mcp-adapters, which bridges
MCP tools into LangChain's tool interface so they work seamlessly
with LangChain agents and LangGraph.
"""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent


async def run_agent():
    # -- 1. Connect to the MCP server --------------------------------------
    # StdioServerParameters tells the client how to launch the server
    # process. The client communicates with it over stdin/stdout.
    print("Connecting to MCP server...")

    server_params = StdioServerParameters(
        command="python",
        args=["../../custom-mcp-server/python/main.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # -- 2. Initialize the session ----------------------------------
            # The handshake exchanges protocol version and capabilities
            # between client and server.
            await session.initialize()
            print("Session initialized.")

            # -- 3. Discover and load tools ---------------------------------
            # load_mcp_tools queries the server for its tool list and
            # converts each one into a LangChain Tool object. The tool
            # names, descriptions, and parameter schemas all come from
            # the server's @mcp.tool() definitions.
            tools = await load_mcp_tools(session)
            print(f"Loaded {len(tools)} tools from server:")
            for tool in tools:
                print(f"  - {tool.name}")

            # -- 4. Build a ReAct agent with the MCP tools ------------------
            # create_react_agent from LangGraph creates an agent that
            # reasons in Thought/Action/Observation steps, using the
            # MCP tools as its available actions.
            print("\nBuilding agent...")
            llm = ChatOllama(model="llama3.1", temperature=0)
            agent = create_react_agent(llm, tools)

            # -- 5. Run a query that requires both tools --------------------
            # This query is designed to trigger both tools: the time tool
            # and the compound interest calculator.
            query = (
                "What is the system time right now? Also, if I invest "
                "$5,000 at a 7% interest rate, what will I have after 5 years?"
            )
            print(f"\nQuery: {query}")
            print("Agent is reasoning and calling tools...\n")

            result = await agent.ainvoke(
                {"messages": {"role": "user", "content": query}}
            )

            print("\nResponse:")
            print(result["messages"][-1].content)


# MCP client sessions are async because the stdio transport uses
# non-blocking I/O for subprocess communication.
if __name__ == "__main__":
    asyncio.run(run_agent())
