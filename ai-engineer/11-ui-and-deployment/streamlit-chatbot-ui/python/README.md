# Streamlit Chatbot UI -- Python

Python implementation using Streamlit for the frontend and `requests` to call the FastAPI backend.

## Prerequisites

The [FastAPI LLM Service](../../fastapi-llm-service/) must be running on `http://127.0.0.1:8000`.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

In a separate terminal from the FastAPI server:

```bash
streamlit run main.py
```

Opens at `http://localhost:8501` in your browser.

## Dependencies

- `streamlit` -- Python web framework for building data/AI apps with built-in chat components
- `requests` -- HTTP client for calling the FastAPI backend
