# FastAPI LLM Service -- Python

Python implementation using FastAPI, Pydantic, and LangChain with Ollama.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
ollama pull llama3.1
```

## Run

```bash
uvicorn main:app --reload
```

The server starts at `http://localhost:8000`.

## Test

Open `http://localhost:8000/docs` for the interactive Swagger UI, or use curl:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message": "What is Python?"}'
```

Response:

```json
{"ai_reply": "Python is a high-level programming language..."}
```

## Dependencies

- `fastapi` -- web framework with automatic validation, docs, and OpenAPI spec
- `uvicorn` -- ASGI server to run the FastAPI app
- `langchain-ollama` -- local Llama 3.1 via Ollama
