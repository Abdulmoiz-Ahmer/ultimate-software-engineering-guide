# LangChain RAG with Conversation Memory

Extends the [LangChain RAG Pipeline](../langchain-rag-pipeline/) with **conversation history**. Follow-up questions like "What is her extension?" are correctly resolved against the document instead of failing or hallucinating.

## The problem this solves

A basic RAG pipeline treats every question in isolation. If the user asks "Who is the IT lead?" and follows up with "What is her extension?", the retriever sees the second question with no idea who "her" refers to -- and retrieves the wrong chunks.

This project fixes that with a **rephrasing step** that rewrites follow-up questions into standalone queries before they hit the vector database.

## How it works

```
User question + chat history
    |
    v
Rephrase: "What is her extension?" -> "What is Sarah Connor's extension?"
    |
    v
Retrieve: vector search with the standalone query
    |
    v
Generate: LLM answers from retrieved context
    |
    v
Append turn to chat history
```

## Key concepts

- **Two-prompt architecture** -- the pipeline uses two separate prompts:
  - **Rephraser prompt** -- rewrites follow-up questions into self-contained queries using chat history. The retriever always gets a clear, context-free query.
  - **QA prompt** -- answers the rephrased question using only the retrieved document chunks.
- **`create_history_aware_retriever`** -- wraps the base retriever with the rephraser prompt. The LLM rewrites the query first, then the standalone query is used for vector search.
- **`MessagesPlaceholder`** -- injects the chat history list into the prompt template at runtime.
- **Rolling memory** -- after each turn, `HumanMessage` and `AIMessage` are appended to `chat_history` and passed into the next `invoke()` call.

## Comparison with basic RAG pipeline

| | Basic RAG | RAG with Memory |
|---|---|---|
| Follow-up questions | Fail (no context) | Resolved via rephrasing |
| Prompts | 1 (QA only) | 2 (rephraser + QA) |
| Retriever | Base retriever | History-aware retriever |
| Chat history | None | Rolling `HumanMessage`/`AIMessage` list |

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3
```

## Usage

```bash
python main.py
```

Try a multi-turn conversation:
- `Who is the IT lead?`
- `What is her extension?` (resolved using chat history)
- `When is the cafeteria open?`

Type `q` to quit.

## Customization

Replace `company_policy.txt` with any text file. Adjust `chunk_size`, `chunk_overlap`, and `k` to tune retrieval quality.
