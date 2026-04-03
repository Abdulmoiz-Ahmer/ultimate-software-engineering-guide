# Hybrid Search Pipeline

Combines **vector search** (semantic) and **BM25 search** (lexical/keyword) into a single retriever. This solves a fundamental limitation of pure vector search: it struggles with exact identifiers, error codes, and random strings that have no semantic meaning.

## The problem

| Query | Vector search | BM25 search |
|---|---|---|
| "What does ERR-77X-992 mean?" | Misses it (random string has no semantic meaning) | Finds it (exact keyword match) |
| "hardware failure issues" | Finds it (understands meaning) | Misses it (no exact keyword overlap) |

Neither strategy is complete on its own. Hybrid search merges both, so you get semantic understanding *and* exact keyword matching.

## How it works

```
User query
    |
    +---> Vector retriever (semantic similarity via embeddings)
    |         |
    |         v
    |     Top K results (by meaning)
    |
    +---> BM25 retriever (keyword matching via term frequency)
              |
              v
          Top K results (by exact terms)
              |
              v
    EnsembleRetriever merges + reranks with configurable weights
              |
              v
    Final results (best of both worlds)
```

## Key concepts

- **Vector search** -- embeds queries and documents into vectors, finds closest matches by cosine similarity. Understands paraphrases and synonyms but fails on exact IDs and codes.
- **BM25 search** -- scores documents by term frequency and inverse document frequency (TF-IDF variant). Excels at exact keyword matches but misses meaning.
- **EnsembleRetriever** -- merges results from multiple retrievers using configurable weights (e.g., 50/50). Adjusting weights lets you favor one strategy over the other.
- **Why this matters** -- real-world documents contain both natural language and structured identifiers (error codes, product IDs, version numbers). Hybrid search handles both.

## Prerequisites

- Python 3.10+
- No API keys needed -- runs fully offline

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
