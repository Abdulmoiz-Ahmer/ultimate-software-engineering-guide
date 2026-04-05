"""
FastAPI LLM Service -- Python

Wraps a local LLM (Llama 3.1 via Ollama) in a REST API using FastAPI.
This turns the model into a web service that any frontend, mobile app,
or backend can call over HTTP.

The API has a single endpoint:
  POST /api/chat
    Request:  {"user_message": "your question"}
    Response: {"ai_reply": "the model's answer"}

Pydantic models define the request/response schemas, which FastAPI uses
to generate automatic validation, documentation (Swagger UI at /docs),
and OpenAPI spec.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_ollama import ChatOllama


# -- FastAPI app setup ------------------------------------------------------
# FastAPI generates interactive API docs at /docs (Swagger UI) and /redoc
# automatically from the app metadata and Pydantic models.

app = FastAPI(
    title="LLM Chat API",
    description="REST API for a local LLM powered by Ollama",
    version="1.0",
)

# Initialize the LLM once at startup so it's reused across requests.
# temperature=0 for consistent, deterministic responses.
llm = ChatOllama(model="llama3.1", temperature=0)


# -- Request/response schemas ----------------------------------------------
# Pydantic models define the JSON structure for the API. FastAPI uses these
# for automatic request validation (rejects malformed JSON with a 422 error)
# and response serialization.

class ChatRequest(BaseModel):
    user_message: str


class ChatResponse(BaseModel):
    ai_reply: str


# -- Chat endpoint ----------------------------------------------------------
# POST /api/chat accepts a user message, sends it to the LLM, and returns
# the model's response. The response_model parameter tells FastAPI to
# validate and serialize the output using ChatResponse.

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        print(f"Received: '{request.user_message}'")

        response = llm.invoke(request.user_message)

        print("Reply generated.")
        return ChatResponse(ai_reply=response.content)

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
