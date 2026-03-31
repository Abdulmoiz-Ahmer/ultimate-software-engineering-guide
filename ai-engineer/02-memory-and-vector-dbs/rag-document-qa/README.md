# RAG Document Q&A

A chatbot that answers questions about a text document using **Retrieval-Augmented Generation (RAG)**. Combines vector search (ChromaDB) with local LLM generation (Llama 3 via Ollama). The model only uses information from the provided document, not its training data.

## How it works

```
User question
    |
    v
Retrieve: find top 3 relevant chunks from ChromaDB
    |
    v
Augment: inject chunks into the system prompt
    |
    v
Generate: Llama 3 answers using only the provided context
```

1. **Chunk** -- the source document is split into overlapping text chunks.
2. **Embed and store** -- chunks are embedded and stored in ChromaDB (auto-embedded on insert).
3. **Retrieve** -- when you ask a question, the 3 most relevant chunks are found by semantic similarity.
4. **Generate** -- the retrieved chunks are injected into a system prompt, and Llama 3 generates a grounded answer.

## Key concepts

- **RAG (Retrieval-Augmented Generation)** -- instead of relying on the model's training data, RAG retrieves relevant context at query time and feeds it to the model. This reduces hallucination and lets the model answer from up-to-date or private documents.
- **Chunking with overlap** -- the document is split into fixed-size chunks with overlap so that sentences spanning a boundary are captured in at least one chunk.
- **Grounding prompt** -- the system instruction tells the model to answer only from the provided context. If the answer isn't there, it says so rather than guessing.
- **Persistent vector storage** -- embeddings are saved to disk so they survive between runs.

## Sample data

The included `company_policy.txt` contains a short company policy document. Replace it with any text file to chat with your own documents.

## Prerequisites

- [Ollama](https://ollama.com/) running locally with the `llama3` model pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
