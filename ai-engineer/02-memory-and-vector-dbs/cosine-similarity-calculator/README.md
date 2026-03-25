# Cosine Similarity Calculator

A CLI tool that demonstrates **semantic similarity** by converting sentences into vector embeddings and comparing them using cosine similarity. Built with the `sentence-transformers` library and the **all-MiniLM-L6-v2** model.

## Features

- **Sentence Embeddings:** Converts natural language into numerical vectors using a pre-trained transformer model.
- **Cosine Similarity:** Measures how semantically similar two sentences are (0% = unrelated, 100% = identical meaning).
- **No API Key Needed:** Runs fully offline using a local model (downloaded on first run).

## Prerequisites

- Python 3.10 or higher

## Installation

1. **Navigate to the project:**

    ```bash
    cd ai-engineer/02-memory-and-vector-dbs/cosine-similarity-calculator
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

The script compares a target sentence against a list of other sentences and prints the similarity score for each pair.
