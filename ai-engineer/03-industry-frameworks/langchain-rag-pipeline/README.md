# LangChain RAG Pipeline

Rebuilds the manual RAG pipeline from module 02 using **LangChain** abstractions. LangChain replaces hand-written load/chunk/embed/retrieve/generate steps with composable components that wire together into a single callable chain.

## How it works

```
TextLoader -> RecursiveCharacterTextSplitter -> HuggingFace + Chroma -> Retriever -> ChatOllama
     |                  |                            |                      |              |
   Load doc        Smart chunking           Embed & store           Vector search     LLM answer
```

1. **Load** -- `TextLoader` reads the source document into Document objects.
2. **Split** -- `RecursiveCharacterTextSplitter` chunks the document intelligently, splitting on paragraphs first, then sentences, then words.
3. **Embed and store** -- Embeddings convert chunks to vectors; a vector store persists them on disk.
4. **Retrieve** -- a retriever wraps the vector store and fetches the top 2 most relevant chunks per query.
5. **Generate** -- a local LLM generates an answer grounded in the retrieved context.
6. **Chain** -- a retrieval chain wires all steps together; a single `invoke()` runs the full pipeline.

## Key concepts

- **Smart chunking** -- `RecursiveCharacterTextSplitter` tries paragraph breaks first, then sentences, then words, keeping semantically related text together.
- **Stuff documents chain** -- "stuffs" retrieved chunks into the `{context}` placeholder of the prompt template.
- **Retrieval chain** -- connects the retriever and document chain so one `invoke()` call triggers the full pipeline.
- **Retriever abstraction** -- wraps any vector store with a consistent search interface, decoupling retrieval from storage.

## Comparison with manual RAG (module 02)

| | Manual RAG | LangChain RAG |
|---|---|---|
| Document loading | `open().read()` | `TextLoader` |
| Chunking | Custom `get_chunks()` | `RecursiveCharacterTextSplitter` |
| Embedding | Auto (ChromaDB built-in) | Explicit model choice |
| Retrieval | `collection.query()` | `retriever` via `as_retriever` |
| Generation | Manual prompt string | `ChatPromptTemplate` + chain |
| Orchestration | Hand-written loop | Single `rag_chain.invoke()` |

## Prerequisites

- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
