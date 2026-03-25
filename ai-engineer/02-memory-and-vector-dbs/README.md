# 02 — Memory and Vector Databases

This module covers how LLMs can work with long-term memory using embeddings and vector databases. You will learn how text is converted into numerical representations, how similarity search works under the hood, and how to build a full RAG pipeline.

## Learning Path

Work through these projects in order:

### 1. [Cosine Similarity Calculator](cosine-similarity-calculator/)
> **You will learn:** How sentence embeddings work and how to measure semantic similarity between texts.

Your entry point into the world of vectors. Converts sentences into numerical embeddings using a pre-trained transformer model and compares them using cosine similarity. This is the math behind every vector database — understanding this first makes everything else click.

**Key concepts:** Sentence embeddings, cosine similarity, transformer models, semantic search fundamentals

---

### 2. [Semantic Search](semantic-search/)
> **You will learn:** How to store documents in a vector database and retrieve them by meaning using ChromaDB.

Takes the cosine similarity concept from project 1 and puts it into practice with a real search engine. Documents are stored in ChromaDB (a persistent vector database), and user queries return the most semantically similar results — no keyword matching needed.

**Key concepts:** Vector databases, ChromaDB, persistent storage, semantic retrieval, distance-based ranking

---

### 3. [RAG — Retrieval-Augmented Generation](rag/)
> **You will learn:** How to combine vector search with an LLM to build a chatbot that answers questions grounded in a specific document.

The culmination of this module. A document is chunked, embedded, and stored in ChromaDB. When the user asks a question, the most relevant chunks are retrieved and injected into a prompt for Llama 3 — so the model answers from your data, not its training data.

**Key concepts:** RAG pipeline, text chunking, context injection, document-grounded generation
