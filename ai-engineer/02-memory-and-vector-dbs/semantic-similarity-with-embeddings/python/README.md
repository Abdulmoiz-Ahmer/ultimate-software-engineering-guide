# Semantic Similarity with Embeddings -- Python

Python implementation using the `sentence-transformers` library.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The model (`all-MiniLM-L6-v2`) is downloaded automatically on first run.

## Dependencies

- `sentence-transformers` -- provides `SentenceTransformer` for encoding sentences into embeddings and `util.cos_sim` for computing cosine similarity
