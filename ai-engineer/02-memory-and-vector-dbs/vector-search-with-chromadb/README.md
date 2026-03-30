# Vector Search with ChromaDB

A semantic search engine that stores documents in a **ChromaDB** vector database and retrieves the most relevant results by meaning, not keywords. Searching "superhero" will match "Batman" even though the word never appears in the document.

## What it does

1. Stores a set of documents in ChromaDB (embedded automatically on insert).
2. You type a search query in natural language.
3. ChromaDB embeds the query, finds the 3 nearest documents, and returns them ranked by distance.

## Example output

```
Search: comic book hero

Top results:
  1. Batman is a fictional character. (distance: 0.8234)
  2. Batman is a witty character. (distance: 0.9012)
  3. Green arrow movie is coming out soon. (distance: 1.2145)
```

## Key concepts

- **Vector database** -- stores documents as numerical vectors (embeddings) and supports nearest-neighbor search. ChromaDB handles embedding automatically using its built-in model.
- **Collection** -- ChromaDB's equivalent of a database table. Stores documents, embeddings, and optional metadata.
- **PersistentClient** -- saves data to disk (`./chroma_db`) so it survives between runs, unlike an in-memory client.
- **Distance score** -- measures how far apart two embeddings are. Lower distance = higher semantic similarity. This is the inverse of the cosine similarity from the previous project.
- **Why this matters** -- vector search is the retrieval step in RAG (Retrieval-Augmented Generation). You store your knowledge base as embeddings, then find the most relevant chunks for a given query.

## Prerequisites

- Python 3.10+
- No API keys needed -- runs fully offline

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Type any concept or phrase to search. Results show the top 3 matches with distance scores. Type `q` to quit.
