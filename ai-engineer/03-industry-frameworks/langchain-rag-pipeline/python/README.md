# LangChain RAG Pipeline -- Python

Python implementation using LangChain with `ChatOllama`, `HuggingFaceEmbeddings`, and `Chroma`.

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

Ask questions about `company_policy.txt`. Type `q` to quit.

## Customization

Replace `company_policy.txt` with any text file. Adjust `chunk_size`, `chunk_overlap`, and `k` to tune retrieval quality.

## Dependencies

- `langchain`, `langchain-core`, `langchain-classic` -- chain orchestration and prompt templates
- `langchain-community` -- `TextLoader` for document loading
- `langchain-text-splitters` -- `RecursiveCharacterTextSplitter`
- `langchain-huggingface` -- `HuggingFaceEmbeddings` (all-MiniLM-L6-v2)
- `langchain-chroma` -- ChromaDB vector store integration
- `langchain-ollama` -- `ChatOllama` for local Llama 3
- `sentence-transformers`, `chromadb` -- underlying embedding and storage engines
