# 07 -- Advanced RAG

This module covers techniques that improve retrieval quality beyond basic vector search. Each project addresses a specific weakness in standard RAG -- vague queries, keyword-dependent content, and imprecise ranking -- and shows how production pipelines solve it.

## Project structure

Each project folder contains a language-agnostic README explaining the concept, with implementation-specific code and instructions inside language subfolders:

```
project-name/
  README.md          # What it does, key concepts, prerequisites
  python/            # Python implementation + setup instructions
    main.py
    requirements.txt
    README.md
  # js/              # (coming soon)
```

## Learning path

### 1. [Query Transform with HyDE](query-transform-hyde/)

Fixes the problem of vague or short queries producing poor embeddings. Instead of embedding the raw query, the LLM generates a hypothetical answer first, and that document's embedding is used for retrieval. "code collision" becomes a rich paragraph about git merge conflicts -- landing much closer to the real document.

**You learn:** How query transformation improves retrieval when users write vague queries, and why controlled hallucination produces better embeddings than the raw query.

**Key concepts:** HyDE (Hypothetical Document Embeddings), query transformation, controlled hallucination, embedding quality

---

### 2. [Hybrid Search Pipeline](hybrid-search-pipeline/)

Combines vector search (semantic) and BM25 search (keyword) into a single retriever. Vector search understands meaning but misses exact IDs and error codes. BM25 matches keywords exactly but misses paraphrases. Hybrid search merges both so you get the best of both worlds.

**You learn:** Why neither semantic nor keyword search is complete on its own, and how EnsembleRetriever fuses both with configurable weights.

**Key concepts:** Hybrid search, BM25, EnsembleRetriever, vector + keyword fusion, configurable weights

---

### 3. [Cohere Reranking Pipeline](cohere-reranking/)

Adds a second-stage reranker after vector search. The base retriever returns K candidates quickly, then Cohere's cross-encoder model rescores them against the original query and returns only the top N in correct relevance order. This is the highest-leverage improvement you can make to retrieval quality.

**You learn:** How two-stage retrieval works (fast approximate search + slow accurate reranking) and why cross-encoders outperform bi-encoders at scoring relevance.

**Key concepts:** Two-stage retrieval, cross-encoder vs. bi-encoder, Cohere reranker, ContextualCompressionRetriever, relevance scoring

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3` pulled (projects 1-2)
- A [Cohere](https://cohere.com/) API key (project 3, free tier available)

Each project has its own `README.md` with concept explanations, and each language folder has setup instructions.
