# RAG with LangChain + Conversation History + PDF

Extends `rag-with-langchain-history` with **PDF support**. Swaps `TextLoader` for `PyPDFLoader` so the chatbot can ingest any PDF document, while keeping full conversation memory and history-aware retrieval.

## What Changed from rag-with-langchain-history

The only difference is the document loader. `PyPDFLoader` extracts text page by page from a PDF, with error handling for missing or corrupt files. Everything else — chunking, embedding, history-aware retrieval, rolling memory — is identical.

## How It Works

1. **Load** — `PyPDFLoader` reads the PDF from disk, extracting text page by page into LangChain Document objects.
2. **Split** — `RecursiveCharacterTextSplitter` chunks the pages, preserving sentence boundaries.
3. **Embed and Store** — `HuggingFaceEmbeddings` converts chunks to vectors; `Chroma` persists them to disk.
4. **Two Prompts:**
   - **Rephraser prompt** — rewrites follow-up questions into standalone queries using the chat history.
   - **QA prompt** — answers the rephrased question using only the retrieved context.
5. **History-Aware Retriever** — `create_history_aware_retriever` rephrases before searching, so the vector database always receives a clear, context-free query.
6. **Chain** — `create_retrieval_chain` wires everything together; a single `invoke()` runs the full pipeline.
7. **Rolling Memory** — each turn's messages are appended to `chat_history` as `HumanMessage` / `AIMessage` objects and passed into the next `invoke()`.

## Features

- **PDF Ingestion:** Loads any PDF using `PyPDFLoader`, with error handling for missing or unreadable files.
- **Conversation Memory:** Resolves pronouns and references across multiple turns.
- **History-Aware Retrieval:** Rephrases follow-up questions before vector search, not after.
- **Document-Grounded Answers:** The model only answers from the provided document context.
- **Persistent Vector Store:** Embeddings are saved to `./langchain_db` and reusable between runs.
- **Fully Local:** Runs offline using Ollama + Llama 3 and a local HuggingFace embedding model.

## Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com/) installed and running
- Llama 3 model pulled:
    ```bash
    ollama pull llama3
    ```

## Installation

1. **Navigate to the project:**

    ```bash
    cd ai-engineer/03-industry-frameworks/rag-with-langchain-history-pdf
    ```

2. **Set up the Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Place your PDF in the project folder and name it `typesofpl.pdf`, then run:

```bash
python main.py
```

Ask questions about the PDF. The chatbot remembers previous turns, so follow-up questions work naturally. Type `q` or `quit` to exit.

## Customization

Replace `typesofpl.pdf` with any PDF file and update the `pdf_path` variable in `main.py`. Adjust `chunk_size`, `chunk_overlap`, and `k` (number of retrieved chunks) to tune retrieval quality.
