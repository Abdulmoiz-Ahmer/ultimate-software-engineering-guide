# RAG — Retrieval-Augmented Generation (ChromaDB + Llama 3)

A CLI chatbot that answers questions about a document by combining **vector search** (ChromaDB) with **local LLM generation** (Llama 3 via Ollama). The model only uses information from the provided document, not its own training data.

## How It Works

1. **Chunk** — The source document is split into overlapping text chunks.
2. **Embed and Store** — Chunks are embedded and stored in a ChromaDB vector database.
3. **Retrieve** — When the user asks a question, the 3 most relevant chunks are retrieved by semantic similarity.
4. **Generate** — The retrieved chunks are injected into a system prompt, and Llama 3 generates an answer grounded in that context.

## Features

- **Document-Grounded Answers:** The model is instructed to only answer from the provided context.
- **Vector Retrieval:** Uses ChromaDB to find the most relevant chunks by meaning, not keywords.
- **Persistent Storage:** Vector database is saved to disk (`./rag_db`).
- **Fully Local:** Runs offline using Ollama + Llama 3. No API keys needed.

## Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com/) installed and running
- Llama 3 model pulled:
    ```bash
    ollama pull llama3
    ```

## Installation

1. **Navigate to the project:**

    ```bash
    cd ai-engineer/02-memory-and-vector-dbs/rag
    ```

2. **Set up the Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

```bash
python main.py
```

The chatbot loads `company_policy.txt`, chunks and embeds it, then lets you ask questions. Type `q` or `e` to exit.

## Customization

Replace `company_policy.txt` with any text file to chat with your own documents. Adjust `chunk_size` and `overlap` in the `get_chunks()` function to tune retrieval granularity.
