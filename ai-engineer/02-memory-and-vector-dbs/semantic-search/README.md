# Semantic Search Engine (ChromaDB)

A CLI semantic search engine that stores documents in a **ChromaDB** vector database and retrieves the most relevant results by meaning, not keywords. ChromaDB handles embedding automatically.

## Features

- **Vector Database:** Uses ChromaDB to store and query document embeddings locally.
- **Persistent Storage:** Data is saved to disk (`./chroma_db`) and survives between runs.
- **Semantic Retrieval:** Finds documents by meaning — searching "superhero" will match "Batman" even though the word never appears.
- **No API Key Needed:** Runs fully offline using ChromaDB's built-in embedding model.

## Prerequisites

- Python 3.10 or higher

## Installation

1. **Navigate to the project:**

    ```bash
    cd ai-engineer/02-memory-and-vector-dbs/semantic-search
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

Type any concept or phrase to search. The engine returns the top 3 most semantically similar documents with their distance scores (lower = more similar). Type `q` or `e` to exit.
