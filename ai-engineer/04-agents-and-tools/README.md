# 04 -- Agents and Tools

This module covers how LLMs go beyond generating text by calling external tools and acting autonomously. The projects progress from writing the tool-calling loop by hand, to letting LangChain manage it for you, to giving an agent a full data-analysis toolkit.

## Learning path

### 1. [Manual Tool-Calling Agent](manual-tool-calling-agent/)

Start here. This project implements the tool-calling loop from scratch so you can see every step that normally happens behind the scenes:

- Define a tool with the `@tool` decorator and a descriptive docstring.
- Bind the tool schema to the LLM with `bind_tools`.
- Send a user query and inspect the LLM's response for `tool_calls`.
- Execute the matching Python function and wrap the result in a `ToolMessage`.
- Feed the result back to the LLM for a final, human-friendly answer.

**You learn:** What tool calling actually is -- the LLM doesn't run code; it outputs a structured request, and your code does the execution.

### 2. [AgentExecutor with Web Search](agent-executor-with-web-search/)

Now that you understand the manual loop, this project hands that work off to LangChain's `AgentExecutor`. It manages the decide -> call -> observe -> respond cycle automatically, so you only need to define the tools and the prompt.

Two tools are introduced:

- **TavilySearch** -- live web search via the Tavily API.
- **calculator** -- evaluates math expressions.

**You learn:** How `create_tool_calling_agent` and `AgentExecutor` abstract away the loop, how multiple tools coexist, and how the agent scratchpad stores intermediate results between steps.

### 3. [CSV Data Analyst Agent](csv-data-analyst-agent/)

The final project moves from simple tools to a specialized agent toolkit. `create_csv_agent` loads a CSV into a Pandas DataFrame and gives the LLM a Python REPL so it can write and execute Pandas code to answer your questions.

The agent uses the **ReAct** (Reason + Act) pattern: it thinks about the question, writes code, runs it, observes the output, and iterates until it has an answer.

**You learn:** How pre-built agent toolkits work, the ReAct reasoning loop, and how an LLM can autonomously write and execute code against real data.

## Key takeaways

| Concept | Where it appears |
|---------|-----------------|
| `@tool` decorator and tool schemas | Project 1, 2 |
| `bind_tools` / manual tool dispatch | Project 1 |
| `AgentExecutor` and automatic looping | Project 2, 3 |
| Multiple tools in one agent | Project 2 |
| ReAct (Reason + Act) pattern | Project 3 |
| Code execution (Python REPL) as a tool | Project 3 |

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with the `llama3.1` model pulled
- A [Tavily](https://tavily.com/) API key (for project 2 only)

Each project has its own `requirements.txt` and `README.md` with setup instructions.
