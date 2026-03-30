# Manual Tool-Calling Agent

A minimal example showing how to implement the **tool-calling loop manually** using LangChain and a local Ollama model (Llama 3.1). Instead of using `AgentExecutor`, this project walks through each step of the loop so you can see exactly what happens under the hood.

## What it does

1. The user types a query in an interactive prompt.
2. The LLM decides whether the query requires a tool (the `get_weather` function) or can be answered directly.
3. If a tool is needed, the code executes the Python function, sends the result back to the LLM, and the LLM composes a final answer.
4. If no tool is needed, the LLM responds directly from its own knowledge.

## How it works

```
User query
    |
    v
LLM (with tool schema bound)
    |
    +-- tool_calls present? --YES--> Execute get_weather()
    |                                    |
    |                                    v
    |                              ToolMessage returned to LLM
    |                                    |
    |                                    v
    |                              LLM writes final answer
    |
    +-- No tool calls -----------> LLM answers directly
```

## Key concepts

- **`@tool` decorator** converts a Python function into a JSON schema the LLM can understand. The docstring tells the LLM when to use it.
- **`bind_tools`** attaches tool schemas to the LLM so it knows what is available.
- **`ToolMessage`** wraps function output and links it back to the original tool call via `tool_call_id`.
- **Manual loop** gives full control over how tool calls are dispatched, letting you add logging, validation, or routing logic.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with the `llama3.1` model pulled

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3.1
```

## Usage

```bash
python main.py
```

Then try queries like:

- `What is the weather in Tokyo?` (triggers the tool)
- `What is the capital of France?` (answered directly, no tool)
- Type `q` to quit.
