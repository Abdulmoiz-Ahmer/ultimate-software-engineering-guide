# RAG Document Q&A -- Python

Python implementation using `chromadb` for vector storage and `ollama` for local LLM generation.

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

Example queries:
- `What is the Wi-Fi password?`
- `How many PTO days do employees get?`
- `Who should I contact if the server crashes?`

## Customization

- Replace `company_policy.txt` with any text file.
- Adjust `chunk_size` and `overlap` in `get_chunks()` to tune retrieval granularity.

## Dependencies

- `chromadb` -- vector database for storing and querying document embeddings
- `ollama` -- Python client for calling Llama 3 locally via Ollama
