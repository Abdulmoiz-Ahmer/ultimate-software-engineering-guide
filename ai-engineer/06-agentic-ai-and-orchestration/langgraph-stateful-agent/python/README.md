# LangGraph Stateful Agent -- Python

Python implementation using `langgraph` for graph orchestration and `langchain-ollama` for local LLM access.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure Ollama is running and you have Llama 3 pulled:

```bash
ollama pull llama3
```

## Run

```bash
python main.py
```

Watch the Writer draft a story, the Critic review it, and the graph loop until the story mentions an animal (or 3 iterations are reached).

## Customization

- Change the acceptance criteria in `review_draft()` (e.g., require a specific word or theme).
- Increase the max iterations in `should_continue()`.
- Add more nodes (e.g., an editor that polishes the approved draft before termination).
- Replace `llama3` with a different Ollama model.

## Dependencies

- `langgraph` -- graph-based orchestration framework (StateGraph, conditional edges, END sentinel)
- `langchain-ollama` -- `ChatOllama` for calling Llama 3 locally via Ollama
