"""
AgentExecutor with Web Search and Calculator

Demonstrates LangChain's AgentExecutor — the built-in agent loop that
automatically handles tool selection, execution, and result routing.
Two tools are provided:

  - TavilySearch: live web search via the Tavily API
  - calculator:   evaluates math expressions

Unlike a manual tool-calling loop, AgentExecutor manages the entire
decide -> call -> observe -> respond cycle internally.
"""

import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langchain_core.tools import tool
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

if not os.getenv("TAVILY_API_KEY"):
    print("Error: TAVILY_API_KEY not found in .env file!")
    exit()


# -- 1. Define tools ------------------------------------------------------

# Tool A: Web search powered by Tavily. Returns up to 2 results per query.
search_tool = TavilySearch(max_results=2)


# Tool B: Simple math evaluator.
@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression.
    Input MUST be a valid math string (e.g., '100 * 4.5 / 2')."""
    print(f"   [SYSTEM: Running calculator -> {expression}]")
    try:
        # Note: eval() is unsafe for public-facing production code,
        # but acceptable here for local experimentation.
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Math Error: {e}"


tools = [search_tool, calculator]


# -- 2. Configure the LLM and prompt --------------------------------------
# The prompt includes a placeholder for the agent scratchpad, which is where
# AgentExecutor stores intermediate tool calls and their results.

llm = ChatOllama(model="llama3.1", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a strict, robotic data assistant. You have access to a "
        "search tool and a calculator.\n\n"
        "CRITICAL RULES:\n"
        "1. NEVER explain your plan to the user.\n"
        "2. NEVER output raw JSON code blocks or markdown text.\n"
        "3. You must trigger the tools directly via the native tool API.\n"
        "4. Stop talking and execute the tool immediately."
    )),
    ("human", "{input}"),
    # The scratchpad is where the agent stores intermediate tool results
    # between steps -- managed automatically by AgentExecutor.
    ("placeholder", "{agent_scratchpad}"),
])


# -- 3. Build the agent ---------------------------------------------------
# create_tool_calling_agent wires the LLM, tools, and prompt together.
# AgentExecutor wraps it with the run-loop (decide -> call -> observe).
# verbose=True prints each step so you can follow the agent's reasoning.

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

print("Agent ready!\n")
print("-" * 50)


# -- 4. Interactive loop ---------------------------------------------------

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ("q", "e", "quit", "exit"):
        break

    try:
        response = agent_executor.invoke({"input": user_input})
        print(f"\nAgent: {response['output']}")
    except Exception as e:
        print(f"Error: {e}")
