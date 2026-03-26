# RAG with LangChain + Conversation History

Extends the `rag-with-langchain` project with **conversation memory**. The chatbot remembers what was said in previous turns, so follow-up questions like "what about his salary?" are correctly resolved against the document instead of failing or hallucinating.

## The Problem This Solves

A basic RAG pipeline treats every question in isolation. If a user asks "Who is the IT lead?" and then follows up with "What is her extension?", the retriever sees "What is her extension?" with no idea who "her" refers to — and retrieves the wrong chunks.

This project fixes that by adding a **rephrasing step** that rewrites follow-up questions into standalone queries before they hit the vector database.

## How It Works

1. **Load** — `TextLoader` reads the source document from disk.
2. **Split** — `RecursiveCharacterTextSplitter` chunks the document, preserving sentence boundaries.
3. **Embed and Store** — `HuggingFaceEmbeddings` converts chunks to vectors; `Chroma` persists them.
4. **Two Prompts:**
   - **Rephraser prompt** — given the chat history and the latest question, rewrites it as a self-contained standalone query.
   - **QA prompt** — answers the rephrased question using only the retrieved context.
5. **History-Aware Retriever** — `create_history_aware_retriever` wraps the base retriever with the rephraser, so the vector search always receives a clear, context-free query.
6. **Chain** — `create_retrieval_chain` wires everything together; a single `invoke()` runs the full pipeline.
7. **Rolling Memory** — after each turn, the user message and bot reply are appended to `chat_history` as `HumanMessage` / `AIMessage` objects and passed into the next `invoke()` call.

## Features

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
    cd ai-engineer/03-industry-frameworks/rag-with-langchain-history
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

Ask questions about `company_policy.txt`. The chatbot remembers previous turns, so follow-up questions work naturally. Type `q` or `quit` to exit.

## Customization

Replace `company_policy.txt` with any text file to chat with your own documents. Adjust `chunk_size`, `chunk_overlap`, and `k` (number of retrieved chunks) to tune retrieval quality.
