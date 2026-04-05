# 11 -- UI and Deployment

This module covers the final step of building an AI application -- exposing the model through a web API and connecting it to a user-facing interface. The first project wraps a local LLM in a REST API, and the second project builds a browser-based chat UI that consumes it.

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

### 1. [FastAPI LLM Service](fastapi-llm-service/)

Wraps a local LLM in a REST API using FastAPI. A single POST endpoint accepts a message and returns the model's response. This is the standard deployment pattern for production LLM applications -- the model runs as a service behind an API that any client can call.

**You learn:** How to serve an LLM over HTTP with automatic request validation, JSON serialization, and interactive API docs.

**Key concepts:** LLM as a service, FastAPI, Pydantic request/response models, async endpoints, auto-generated Swagger docs

---

### 2. [Streamlit Chatbot UI](streamlit-chatbot-ui/)

A browser-based chat interface built in pure Python with Streamlit. Connects to the FastAPI backend from project 1. The entire frontend -- chat bubbles, input box, loading spinner, and conversation memory -- is built without any HTML or JavaScript.

**You learn:** How to build a chat UI with Streamlit's execution model (full script rerun on every interaction), session state for conversation persistence, and frontend-backend separation over HTTP.

**Key concepts:** Streamlit execution model, session state, chat components, walrus operator pattern, frontend-backend architecture

## Architecture

```
[Streamlit UI]  --HTTP-->  [FastAPI Server]  ---->  [Ollama / Llama 3.1]
  Port 8501                   Port 8000              Port 11434
```

Both projects run as separate services. The UI sends requests to the API, which sends them to the local LLM. This separation means either side can be swapped independently.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3.1` pulled
- No API keys needed -- everything runs locally

Each project has its own `README.md` with concept explanations, and each language folder has setup instructions.
