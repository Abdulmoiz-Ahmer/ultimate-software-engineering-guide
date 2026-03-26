# RAG with LangChain

A RAG (Retrieval-Augmented Generation) chatbot built using the **LangChain** framework. This project rebuilds the manual RAG pipeline from module 02 using LangChain abstractions — showing how the framework simplifies document loading, chunking, embedding, retrieval, and chaining into a clean, declarative pipeline.

## How It Works

1. **Load** — `TextLoader` reads the source document from disk.
2. **Split** — `RecursiveCharacterTextSplitter` chunks the document intelligently, preserving sentence boundaries.
3. **Embed and Store** — `HuggingFaceEmbeddings` converts chunks to vectors; `Chroma` stores them on disk.
4. **Retrieve** — A LangChain `Retriever` fetches the top 2 most relevant chunks for each query.
5. **Generate** — `ChatOllama` (Llama 3) generates an answer grounded in the retrieved context.
6. **Chain** — `create_retrieval_chain` wires all steps together; a single `invoke()` runs the full pipeline.

## Features

- **LangChain Pipeline:** Replaces manual RAG boilerplate with composable LangChain components.
- **Smart Chunking:** `RecursiveCharacterTextSplitter` splits on paragraphs, then sentences, then words.
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
    cd ai-engineer/03-industry-frameworks/rag-with-langchain
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

```bash
python main.py
```

Ask any question about `company_policy.txt`. The pipeline retrieves the most relevant chunks and generates a grounded answer. Type `q` or `quit` to exit.

## Customization

Replace `company_policy.txt` with any text file to chat with your own documents. Adjust `chunk_size`, `chunk_overlap`, and `k` (number of retrieved chunks) to tune retrieval quality.
