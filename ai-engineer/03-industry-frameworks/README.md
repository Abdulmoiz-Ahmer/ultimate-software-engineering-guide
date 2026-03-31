# 03 -- Industry Frameworks

This module rebuilds the RAG pipeline from module 02 using industry-standard frameworks -- **LangChain** and **LlamaIndex**. The LangChain projects add capabilities progressively, and the final project shows the same pipeline in LlamaIndex for comparison.

## Learning path

### 1. [LangChain RAG Pipeline](langchain-rag-pipeline/)

Rebuilds the manual RAG pipeline from module 02 using LangChain components. Document loading, chunking, embedding, retrieval, and generation are wired together into a single callable chain.

**You learn:** How LangChain abstractions (TextLoader, RecursiveCharacterTextSplitter, Chroma, create_retrieval_chain) replace hand-written RAG boilerplate.

**Key concepts:** LangChain chains, smart chunking, retriever abstraction, stuff documents chain

---

### 2. [LangChain RAG with Memory](langchain-rag-with-memory/)

Adds conversation history to the RAG pipeline. Follow-up questions like "What is her extension?" are rephrased into standalone queries before hitting the vector database, so the retriever always gets a clear, context-free search.

**You learn:** How to make RAG conversational with a two-prompt architecture (rephraser + QA) and rolling message history.

**Key concepts:** History-aware retriever, question rephrasing, MessagesPlaceholder, HumanMessage/AIMessage

---

### 3. [LangChain PDF RAG with Memory](langchain-pdf-rag-with-memory/)

Swaps `TextLoader` for `PyPDFLoader` so the chatbot can ingest PDF documents. Everything else -- chunking, embedding, memory, history-aware retrieval -- stays identical, demonstrating how LangChain's loader abstraction makes format switching trivial.

**You learn:** How to work with PDF documents in a RAG pipeline and how LangChain's loader abstraction decouples document format from pipeline logic.

**Key concepts:** PyPDFLoader, page-by-page extraction, loader abstraction

---

### 4. [LlamaIndex PDF RAG](llamaindex-pdf-rag/python/)

The same PDF RAG concept rebuilt with **LlamaIndex** -- a different framework with a more declarative, batteries-included philosophy. The entire pipeline (load, chunk, embed, store, query) is set up in under 10 lines of code, compared to the explicit step-by-step approach in LangChain.

**You learn:** How LlamaIndex compares to LangChain, global configuration via Settings, and how VectorStoreIndex bundles chunking + embedding + storage into a single call.

**Key concepts:** LlamaIndex Settings, SimpleDirectoryReader, VectorStoreIndex, query engine, BGE embeddings

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3` pulled
- No API keys needed -- all projects run locally

Each project has its own `README.md` and `requirements.txt` with setup instructions.
