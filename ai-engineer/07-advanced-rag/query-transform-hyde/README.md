# Query Transform with HyDE

**HyDE (Hypothetical Document Embeddings)** is a retrieval technique that fixes a fundamental weakness in standard vector search: short or vague queries produce poor embeddings that miss relevant documents.

## The problem

Standard RAG embeds the user's query and searches for the nearest documents. This works well when the query uses the same vocabulary as the stored documents. But when the query is vague or uses different terminology, the embedding lands far from the target:

```
Query: "code collision"           --> embedding lands in a vague region
Document: "git merge conflict..." --> embedding is specific and technical

Result: low similarity, poor retrieval
```

The query means the same thing as the document, but the embeddings don't overlap because the words are too different.

## How HyDE solves it

Instead of embedding the raw query, HyDE adds a generation step before retrieval:

```
User query: "code collision"
      |
      v
Step 1: LLM generates a hypothetical answer
        "When two developers modify the same file and attempt to merge,
         a conflict arises at the git level. The <<<<<<< HEAD markers..."
      |
      v
Step 2: Embed the hypothetical document (not the query)
        and search the vector database with that embedding
      |
      v
Result: retrieves the real git merge conflict document
```

The hypothetical document doesn't need to be factually correct. It just needs to contain the right vocabulary ("merge", "conflict", "git", "markers") so its embedding lands near the real document's embedding.

## Key concepts

- **Hypothetical Document Embeddings** -- use the LLM to expand a vague query into a detailed fake document, then embed that instead of the raw query. The fake document's embedding is much closer to the real document's embedding.
- **Query transformation** -- a family of techniques that modify the query before retrieval. HyDE is one approach; others include query expansion, multi-query, and step-back prompting.
- **Controlled hallucination** -- the LLM is deliberately asked to make things up. The factual accuracy doesn't matter -- only the vocabulary and structure of the generated text matters for embedding quality.
- **When to use HyDE** -- most effective when users write short, vague, or jargon-free queries against a knowledge base full of detailed, technical documents. Less useful when queries already match the document vocabulary closely.

## Trade-offs

| | Standard RAG | HyDE |
|---|---|---|
| Query embedding | Embed raw query directly | Embed LLM-generated hypothetical document |
| Latency | Fast (embedding only) | Slower (LLM generation + embedding) |
| Short/vague queries | Poor retrieval | Much better retrieval |
| Precise queries | Good retrieval | Similar retrieval (no harm) |
| Cost | Embedding only | LLM call + embedding |

## Prerequisites

- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
