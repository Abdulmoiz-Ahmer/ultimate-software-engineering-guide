# LangChain PDF RAG with Conversation Memory

Extends the [LangChain RAG with Memory](../langchain-rag-with-memory/) pipeline with **PDF support**. Swaps `TextLoader` for `PyPDFLoader` so the chatbot can ingest any PDF document, while keeping full conversation memory and history-aware retrieval.

## What changed from the text-based version

The only difference is the document loader. `PyPDFLoader` extracts text page by page from a PDF, with error handling for missing or corrupt files. Everything else -- chunking, embedding, history-aware retrieval, rolling memory -- is identical. This shows how the loader abstraction makes format switching trivial.

## How it works

```
Load PDF (page by page extraction)
    |
    v
Split into chunks (smart recursive splitting)
    |
    v
Embed & store (local embeddings + vector DB)
    |
    v
User question + chat history
    |
    v
Rephrase follow-ups into standalone queries
    |
    v
Retrieve relevant chunks -> Generate grounded answer
    |
    v
Append turn to chat history
```

## Key concepts

- **PDF loader** -- reads a PDF file and creates one Document per page, with page number metadata. Handles extraction from multi-page documents automatically.
- **Loader abstraction** -- the rest of the pipeline (splitter, embeddings, retriever, chain) doesn't care whether the source was a text file or PDF. Swapping the loader is the only change needed.
- **History-aware retrieval** -- inherited from the previous project. Follow-up questions are rephrased into standalone queries before vector search.
- **Rolling memory** -- user and assistant messages are accumulated and passed into each call.

## Prerequisites

- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
