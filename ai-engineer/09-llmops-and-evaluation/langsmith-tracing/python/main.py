"""
LangSmith Tracing -- Python

Demonstrates how to add observability to a LangChain pipeline using
LangSmith. Every LLM call, prompt, and output is automatically traced
and sent to the LangSmith dashboard for inspection.

LangSmith tracing is enabled entirely through environment variables --
no code changes are needed. When LANGCHAIN_TRACING_V2=true is set,
LangChain automatically sends traces to the LangSmith API endpoint.

The pipeline itself is a simple LCEL chain:
  prompt -> LLM -> output parser

The value is in the observability: you can see the exact prompt sent
to the model, the raw response, latency, token counts, and cost --
all in the LangSmith web dashboard.
"""

import os

from dotenv import load_dotenv

# override=True ensures .env values take precedence over any existing
# environment variables, which is useful during development.
load_dotenv(override=True)


# -- Verify LangSmith configuration ----------------------------------------
# LangSmith requires these environment variables:
#   LANGCHAIN_TRACING_V2=true     -- enables tracing
#   LANGCHAIN_API_KEY=lsv2_pt_... -- authenticates with LangSmith
#   LANGCHAIN_ENDPOINT             -- API endpoint (default: api.smith.langchain.com)
#   LANGCHAIN_PROJECT              -- groups traces under a project name

api_key = os.environ.get("LANGCHAIN_API_KEY", "NOT_FOUND")
print("=" * 50)
print(f"API key prefix: {api_key[:10]}...")
print(f"API key length: {len(api_key)} characters")
print("=" * 50)

if os.environ.get("LANGCHAIN_TRACING_V2") != "true":
    raise ValueError("LangSmith tracing is not enabled. Set LANGCHAIN_TRACING_V2=true in .env")


from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser


# -- Build a simple LCEL chain ---------------------------------------------
# This is a minimal prompt -> LLM -> parser chain. The point is not the
# chain itself, but that every step is automatically traced in LangSmith.
#
# StrOutputParser extracts the text content from the LLM's response
# object, so you get a plain string instead of a Message object.

print("\nBuilding traced pipeline...")

prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a highly sarcastic, brilliant software engineer. "
        "Answer the user's question, but make fun of them for asking it."
    )),
    ("user", "{question}"),
])

llm = ChatOllama(model="llama3")
parser = StrOutputParser()

chain = prompt | llm | parser


# -- Run the chain (trace is sent automatically) ---------------------------
# When this invoke() call runs, LangChain sends the full trace to
# LangSmith in the background: the formatted prompt, the raw LLM
# response, latency, token counts, and any errors.

query = "What is the difference between a list and a tuple in Python?"

print(f"\nQuery: '{query}'")
print("Running (trace will appear in LangSmith dashboard)...\n")

response = chain.invoke({"question": query})

print("Response:")
print(response)
