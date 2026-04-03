# Cohere Reranking Pipeline

Demonstrates how **reranking** improves retrieval quality. The base vector retriever returns K candidates by embedding similarity, then Cohere's cross-encoder model rescores them against the original query and returns only the top N most relevant.

## The problem

Vector search ranks documents by how close their embeddings are to the query embedding. This is fast but approximate -- it compares representations independently, so it often gets the order wrong when documents are semantically similar.

For the query "How do I reset my router?", vector search might rank a password reset document above the actual router reset document, because both contain "reset" and have similar embeddings.

## How reranking fixes this

```
User query
    |
    v
Vector search: return top 4 candidates (fast, approximate)
    |
    v
Cohere reranker: rescore all 4 against the query (slow, accurate)
    |
    v
Return top 2 in correct relevance order (with scores)
```

The reranker is a **cross-encoder** -- it reads the query and each document together as a pair, producing a single relevance score. This is much more accurate than comparing embeddings independently, but too slow to run over the entire document set. That's why it's used as a second stage after vector search narrows the candidates.

## Key concepts

- **Two-stage retrieval** -- vector search is fast but approximate (narrows to K candidates), reranking is slow but accurate (orders the final N results). This is the standard production pattern.
- **Cross-encoder vs. bi-encoder** -- vector search uses a bi-encoder (embeds query and documents separately). The reranker uses a cross-encoder (reads query + document together). Cross-encoders are more accurate but can't be precomputed.
- **ContextualCompressionRetriever** -- LangChain wrapper that chains a base retriever with a "compressor" (the reranker). First retrieves, then filters and reorders.
- **Relevance score** -- the reranker returns a score per document, making it easy to set confidence thresholds.
- **Why this matters** -- in production RAG, the quality of retrieved context directly affects the LLM's answer. Reranking is the highest-leverage improvement you can make to retrieval quality.

## Prerequisites

- A [Cohere](https://cohere.com/) API key (free tier available)

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
