# LangChain RAG Pipeline

Rebuilds the manual RAG pipeline from module 02 using **LangChain** abstractions. LangChain replaces hand-written load/chunk/embed/retrieve/generate steps with composable components that wire together into a single callable chain.

## How it works

```
TextLoader -> RecursiveCharacterTextSplitter -> HuggingFace + Chroma -> Retriever -> ChatOllama
     |                  |                            |                      |              |
   Load doc        Smart chunking           Embed & store           Vector search     LLM answer
```

1. **Load** -- `TextLoader` reads the source document into LangChain Document objects.
2. **Split** -- `RecursiveCharacterTextSplitter` chunks the document intelligently, splitting on paragraphs first, then sentences, then words.
3. **Embed and store** -- `HuggingFaceEmbeddings` converts chunks to vectors; `Chroma` stores them on disk.
4. **Retrieve** -- `as_retriever` wraps the vector store and fetches the top 2 most relevant chunks per query.
5. **Generate** -- `ChatOllama` (Llama 3) generates an answer grounded in the retrieved context.
6. **Chain** -- `create_retrieval_chain` wires all steps together; a single `invoke()` runs the full pipeline.

## Key concepts

- **`RecursiveCharacterTextSplitter`** -- smarter than fixed-size chunking. Tries paragraph breaks first, then sentences, then words, keeping semantically related text together.
- **`create_stuff_documents_chain`** -- "stuffs" retrieved chunks into the `{context}` placeholder of the prompt template.
- **`create_retrieval_chain`** -- connects the retriever and document chain so one `invoke()` call triggers the full pipeline.
- **Retriever abstraction** -- `as_retriever` wraps any vector store with a consistent search interface, decoupling retrieval from storage.

## Comparison with manual RAG (module 02)

| | Manual RAG | LangChain RAG |
|---|---|---|
| Document loading | `open().read()` | `TextLoader` |
| Chunking | Custom `get_chunks()` | `RecursiveCharacterTextSplitter` |
| Embedding | ChromaDB built-in | `HuggingFaceEmbeddings` (explicit model choice) |
| Retrieval | `collection.query()` | `retriever` via `as_retriever` |
| Generation | Manual prompt string | `ChatPromptTemplate` + chain |
| Orchestration | Hand-written loop | Single `rag_chain.invoke()` |

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3
```

## Usage

```bash
python main.py
```

Ask questions about `company_policy.txt`. Type `q` to quit.

## Customization

Replace `company_policy.txt` with any text file. Adjust `chunk_size`, `chunk_overlap`, and `k` to tune retrieval quality.
