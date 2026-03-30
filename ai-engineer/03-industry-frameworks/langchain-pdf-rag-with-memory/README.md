# LangChain PDF RAG with Conversation Memory

Extends the [LangChain RAG with Memory](../langchain-rag-with-memory/) pipeline with **PDF support**. Swaps `TextLoader` for `PyPDFLoader` so the chatbot can ingest any PDF document, while keeping full conversation memory and history-aware retrieval.

## What changed from the text-based version

The only difference is the document loader. `PyPDFLoader` extracts text page by page from a PDF, with error handling for missing or corrupt files. Everything else -- chunking, embedding, history-aware retrieval, rolling memory -- is identical. This shows how LangChain's loader abstraction makes it trivial to switch document formats.

## How it works

```
Load PDF (PyPDFLoader, page by page)
    |
    v
Split into chunks (RecursiveCharacterTextSplitter)
    |
    v
Embed & store (HuggingFace + ChromaDB)
    |
    v
User question + chat history
    |
    v
Rephrase follow-ups into standalone queries
    |
    v
Retrieve relevant chunks -> Generate grounded answer
    |
    v
Append turn to chat history
```

## Key concepts

- **`PyPDFLoader`** -- reads a PDF file and creates one LangChain Document per page, with page number metadata. Handles extraction from multi-page documents automatically.
- **Loader abstraction** -- the rest of the pipeline (splitter, embeddings, retriever, chain) doesn't care whether the source was a text file or PDF. Swapping the loader is the only change needed.
- **History-aware retrieval** -- inherited from the previous project. Follow-up questions are rephrased into standalone queries before vector search.
- **Rolling memory** -- `HumanMessage`/`AIMessage` pairs are accumulated and passed into each `invoke()` call.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3
```

## Usage

Place your PDF in the project folder (default: `typesofpl.pdf`), then run:

```bash
python main.py
```

Ask questions about the PDF content. Follow-up questions work naturally. Type `q` to quit.

## Customization

Replace `typesofpl.pdf` with any PDF and update the `pdf_path` variable in `main.py`. Adjust `chunk_size`, `chunk_overlap`, and `k` to tune retrieval quality.
