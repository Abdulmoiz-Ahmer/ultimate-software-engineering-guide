# Streamlit Chatbot UI

A browser-based chat interface built with **Streamlit** that connects to the [FastAPI LLM Service](../fastapi-llm-service/). The entire frontend -- page layout, chat bubbles, input box, loading spinner, and conversation memory -- is built in pure Python with no HTML or JavaScript.

## How it works

```
Browser (Streamlit UI)
    |
    |  User types a message
    v
Streamlit re-runs the entire script
    |
    |  POST /api/chat {"user_message": "..."}
    v
FastAPI backend
    |
    |  Sends to Ollama LLM, returns response
    v
Streamlit renders AI reply in chat bubble
    |
    |  Saves to session state for conversation history
    v
Full chat history persists across reruns
```

## Key concepts

- **Streamlit execution model** -- the entire Python script re-executes from top to bottom on every user interaction. This is fundamentally different from traditional web apps. Understanding this is essential for working with Streamlit.
- **Session state** -- `st.session_state` is a dict that persists across script reruns. Without it, the conversation history would be lost every time the user sends a message.
- **Chat components** -- `st.chat_message` creates styled bubbles with role-based icons. `st.chat_input` creates a pinned input box at the bottom of the page. These are purpose-built for chatbot UIs.
- **Walrus operator** -- `if user_prompt := st.chat_input(...)` assigns the input and checks if it's non-empty in a single expression, a common Streamlit pattern.
- **Frontend-backend separation** -- the UI (Streamlit) and the LLM (FastAPI + Ollama) are separate services communicating over HTTP. This is the standard production architecture -- you can swap either side independently.

## Architecture

```
[Streamlit UI]  --HTTP-->  [FastAPI Server]  ---->  [Ollama / Llama 3.1]
  Port 8501                   Port 8000              Port 11434
```

Both services must be running simultaneously.

## Prerequisites

- The [FastAPI LLM Service](../fastapi-llm-service/) running on port 8000
- [Ollama](https://ollama.com/) running with `llama3.1` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
