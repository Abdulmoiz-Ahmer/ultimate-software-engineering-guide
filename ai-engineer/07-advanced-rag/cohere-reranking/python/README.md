# Cohere Reranking Pipeline -- Python

Python implementation using LangChain's `ContextualCompressionRetriever` with `Chroma` (vector) and `CohereRerank` (cross-encoder reranker).

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `example.env` to `.env` and add your Cohere API key:

```bash
cp example.env .env
# Edit .env and set COHERE_API_KEY=your_key_here
```

Get a free API key from [Cohere Dashboard](https://dashboard.cohere.com/api-keys).

## Run

```bash
python main.py
```

The script runs a comparison showing base vector results vs. reranked results for an ambiguous query.

## Dependencies

- `langchain-huggingface` -- local BGE-small embeddings for vector search
- `langchain-chroma` + `chromadb` -- in-memory vector store
- `langchain-cohere` -- `CohereRerank` cross-encoder reranker
- `langchain-classic` -- `ContextualCompressionRetriever` wrapper
- `python-dotenv` -- loads `COHERE_API_KEY` from `.env`
