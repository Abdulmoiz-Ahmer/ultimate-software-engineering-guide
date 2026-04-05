# FastAPI LLM Service

Wraps a local LLM in a **REST API** using FastAPI. This turns the model into a web service that any frontend, mobile app, or backend can call over HTTP -- the standard way to deploy LLMs for production use.

## What it does

A single endpoint that accepts a message and returns the LLM's response:

```
POST /api/chat
  Request:  {"user_message": "What is Python?"}
  Response: {"ai_reply": "Python is a high-level programming language..."}
```

## How it works

```
Client (browser, curl, frontend app)
    |
    |  POST /api/chat  {"user_message": "..."}
    v
FastAPI server
    |
    |  Validates request with Pydantic
    |  Sends message to LLM
    v
Ollama (local Llama 3.1)
    |
    |  Returns model response
    v
FastAPI server
    |
    |  Serializes response with Pydantic
    v
Client receives  {"ai_reply": "..."}
```

## Key concepts

- **LLM as a service** -- wrapping a model in an HTTP API decouples the AI from the consumer. Any client that can make HTTP requests can use the model, regardless of language or platform.
- **Pydantic models** -- define the request/response JSON schemas. FastAPI uses them for automatic validation (rejects malformed input with 422), serialization, and documentation generation.
- **Auto-generated docs** -- FastAPI creates interactive Swagger UI at `/docs` and OpenAPI spec at `/openapi.json` from the Pydantic models and endpoint definitions.
- **Async endpoint** -- the endpoint is `async def`, allowing FastAPI to handle multiple concurrent requests without blocking.
- **Why this matters** -- this is the deployment pattern for every production LLM application. The model runs as a service behind an API; frontends, chatbots, and other services call it over HTTP.

## Prerequisites

- [Ollama](https://ollama.com/) running locally with `llama3.1` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
