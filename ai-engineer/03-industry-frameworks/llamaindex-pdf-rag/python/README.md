# LlamaIndex PDF RAG

A RAG pipeline built with **LlamaIndex** instead of LangChain. Loads a PDF, builds an in-memory vector index, and answers questions grounded in the document content. The entire pipeline is set up in under 10 lines of code.

## How it works

```
PDF file
    |
    v
SimpleDirectoryReader + PyMuPDFReader (load & extract text)
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

- **`Settings`** -- global configuration object. Set `Settings.llm` and `Settings.embed_model` once, and every LlamaIndex component uses them automatically.
- **`SimpleDirectoryReader`** -- loads files from disk with format-specific extractors. `PyMuPDFReader` handles PDFs with better layout extraction than basic text parsing.
- **`VectorStoreIndex.from_documents`** -- chunks documents, embeds them, and stores the vectors in memory in a single call.
- **`as_query_engine()`** -- wraps the index with a retrieval + generation pipeline. A single `query()` call handles retrieval, context injection, and LLM generation.
- **BGE-small** (`BAAI/bge-small-en-v1.5`) -- a compact embedding model optimized for retrieval tasks, running locally via HuggingFace.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3
```

## Usage

Place a PDF in the project folder (default: `typesofpl.pdf`), then run:

```bash
python main.py
```

Ask questions about the PDF content. Type `q` to quit.

## Customization

- Change `input_files` in `SimpleDirectoryReader` to load different PDFs.
- Replace `BAAI/bge-small-en-v1.5` with a larger embedding model for better retrieval accuracy.
- Increase the Ollama `request_timeout` if generation is slow on your hardware.
