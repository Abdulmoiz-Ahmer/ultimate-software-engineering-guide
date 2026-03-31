# LlamaIndex PDF RAG

A RAG pipeline built with **LlamaIndex** instead of LangChain. Loads a PDF, builds an in-memory vector index, and answers questions grounded in the document content. The entire pipeline is set up in under 10 lines of code.

## How it works

```
PDF file
    |
    v
SimpleDirectoryReader (load & extract text)
    |
    v
VectorStoreIndex.from_documents (chunk, embed, store -- all in one call)
    |
    v
query_engine.query("your question") (retrieve + generate -- all in one call)
    |
    v
Grounded answer
```

## LlamaIndex vs. LangChain

| | LangChain | LlamaIndex |
|---|---|---|
| Configuration | Explicit per-component | Global `Settings` object |
| Document loading | `TextLoader` / `PyPDFLoader` | `SimpleDirectoryReader` with extractors |
| Chunking | Separate `RecursiveCharacterTextSplitter` | Built into `VectorStoreIndex.from_documents` |
| Embedding + storage | Separate `Chroma.from_documents` | Built into `VectorStoreIndex.from_documents` |
| Query | `rag_chain.invoke()` | `query_engine.query()` |
| Philosophy | Explicit, composable components | Declarative, batteries-included |

LlamaIndex does more with fewer lines by bundling chunking, embedding, and storage into single high-level calls. LangChain gives you more control over each step.

## Key concepts

- **Global Settings** -- set the LLM and embedding model once, and every LlamaIndex component uses them automatically.
- **SimpleDirectoryReader** -- loads files from disk with format-specific extractors. Handles PDFs, text, and other formats.
- **VectorStoreIndex** -- chunks documents, embeds them, and stores the vectors in a single call.
- **Query engine** -- wraps the index with a retrieval + generation pipeline. A single `query()` call handles everything.

## Prerequisites

- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
