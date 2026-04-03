# Hybrid Search Pipeline -- Python

Python implementation using LangChain's `EnsembleRetriever` with `Chroma` (vector) and `BM25Retriever` (lexical).

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

The script runs a comparison test showing vector-only vs. hybrid results for an exact error code query.

## Dependencies

- `langchain-huggingface` -- local BGE-small embeddings for vector search
- `langchain-chroma` + `chromadb` -- in-memory vector store
- `langchain-community` -- `BM25Retriever` for keyword search
- `langchain-classic` -- `EnsembleRetriever` to merge both engines
- `rank-bm25` -- BM25 scoring backend
- `sentence-transformers` -- embedding model runtime
