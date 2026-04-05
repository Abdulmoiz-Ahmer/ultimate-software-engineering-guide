"""
Custom MCP Server -- Python

A minimal Model Context Protocol (MCP) server that exposes two tools:
  - get_current_time: returns the current system time with optional timezone offset
  - calculate_compound_interest: computes compound interest over a period

MCP is a standard protocol for connecting AI models to external tools
and data sources. The server defines tools with typed parameters and
docstrings, and any MCP-compatible client (Claude Desktop, a custom
client, etc.) can discover and call them.

FastMCP is a high-level wrapper that handles the MCP protocol details
(JSON-RPC, tool discovery, parameter validation) so you only need to
write plain Python functions with the @mcp.tool() decorator.

To test this server, run it and connect an MCP client to it, or use
the companion mcp-client-connection project.
"""

import datetime
import math

from mcp.server.fastmcp import FastMCP

# Create an MCP server instance. The name ("Test_Tools") identifies this
# server to clients during the connection handshake.
mcp = FastMCP("Test_Tools")


# -- Tool 1: Current time --------------------------------------------------
# The @mcp.tool() decorator registers this function as an MCP tool.
# The function signature defines the tool's parameters (with types),
# and the docstring becomes the tool's description that clients and
# LLMs read to decide when to call it.

@mcp.tool()
def get_current_time(timezone_offset: int = 0) -> str:
    """Get the current exact system time.
    Provide an optional timezone offset in hours."""
    time = datetime.datetime.utcnow() + datetime.timedelta(hours=timezone_offset)
    return f"The system time is {time.strftime('%Y-%m-%d %H:%M:%S')}"


# -- Tool 2: Compound interest calculator -----------------------------------

@mcp.tool()
def calculate_compound_interest(principal: float, rate: float, years: int) -> str:
    """Calculate compound interest.
    - principal: The starting amount of money
    - rate: The annual interest rate as a decimal (e.g., 0.05 for 5%)
    - years: The number of years the money is invested"""
    amount = principal * math.pow((1 + rate), years)
    return f"After {years} years, the total amount is ${amount:.2f}"


# -- Start the server -------------------------------------------------------
# mcp.run() starts the server and listens for incoming MCP connections.
# By default it uses stdio transport (stdin/stdout), which is the standard
# way MCP clients like Claude Desktop communicate with local servers.

if __name__ == "__main__":
    mcp.run()
