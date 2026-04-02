# Query Transform with HyDE -- Python

Python implementation using `langchain-ollama` for generation, `langchain-community` for BGE embeddings, and `langchain-chroma` for in-memory vector search.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure Ollama is running and you have Llama 3 pulled:

```bash
ollama pull llama3
```

## Run

```bash
python main.py
```

The script generates a hypothetical document from the vague query "code collision", then uses that document's embedding to retrieve the real git merge conflict document from the vector database.

## Customization

- Change `user_query` to test with different vague or short queries.
- Add more documents to the `documents` list to make retrieval harder.
- Replace `BAAI/bge-small-en-v1.5` with a different embedding model.
- Compare results by searching with the raw query vs. the hypothetical document.

## Dependencies

- `langchain-ollama` -- `ChatOllama` for generating the hypothetical document via Llama 3
- `langchain-community` -- `HuggingFaceBgeEmbeddings` for local BGE-small embeddings
- `langchain-chroma` -- ChromaDB vector store integration for LangChain
- `langchain-core` -- `Document` objects for storing text with metadata
- `chromadb` -- in-memory vector database backend
- `sentence-transformers` -- underlying engine for the BGE embedding model
