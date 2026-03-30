# AgentExecutor with Web Search and Calculator

Demonstrates LangChain's **AgentExecutor** -- the built-in agent loop that automatically handles tool selection, execution, and result routing. This is the higher-level counterpart to a manual tool-calling loop.

## What it does

The agent has two tools:

| Tool | Description |
|------|-------------|
| **TavilySearch** | Live web search via the Tavily API (returns up to 2 results) |
| **calculator** | Evaluates math expressions using Python's `eval()` |

When you ask a question, AgentExecutor runs a loop:

1. The LLM reads the query and decides which tool (if any) to call.
2. The tool executes and its output is stored in the agent scratchpad.
3. The LLM reads the scratchpad and either calls another tool or returns a final answer.

All of this happens automatically -- you don't need to write the loop yourself.

## Key concepts

- **`create_tool_calling_agent`** -- wires together the LLM, tools, and prompt into an agent.
- **`AgentExecutor`** -- wraps the agent with the decide -> call -> observe run-loop.
- **`agent_scratchpad`** -- a prompt placeholder where intermediate tool results are stored between steps.
- **`verbose=True`** -- prints each agent step so you can follow its reasoning.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with the `llama3.1` model pulled
- A [Tavily](https://tavily.com/) API key

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3.1
```

Copy `example.env` to `.env` and add your Tavily API key:

```bash
cp example.env .env
# Edit .env and set TAVILY_API_KEY=your_key_here
```

## Usage

```bash
python main.py
```

Example queries:

- `What is the latest news about AI?` (triggers web search)
- `What is 1500 * 3.14 / 7?` (triggers calculator)
- `What is the population of Japan and multiply it by 2?` (may chain both tools)
- Type `q` to quit.
