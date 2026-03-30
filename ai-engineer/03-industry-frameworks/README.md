# 03 -- Industry Frameworks

This module rebuilds the RAG pipeline from module 02 using **LangChain** -- the most widely used framework for building LLM applications. Each project adds one new capability on top of the previous one, showing how LangChain's composable abstractions simplify real-world AI pipelines.

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

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3` pulled
- No API keys needed -- all projects run locally

Each project has its own `README.md` and `requirements.txt` with setup instructions.
