# LlamaIndex PDF RAG -- Python

Python implementation using the `llama-index` ecosystem with `Ollama` LLM and `HuggingFace` embeddings.

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

Place a PDF in this folder (default: `typesofpl.pdf`), then run:

```bash
python main.py
```

Ask questions about the PDF content. Type `q` to quit.

## Customization

- Change `input_files` in `SimpleDirectoryReader` to load different PDFs.
- Replace `BAAI/bge-small-en-v1.5` with a larger embedding model for better retrieval accuracy.
- Increase the Ollama `request_timeout` if generation is slow on your hardware.

## Dependencies

- `llama-index-core` -- core LlamaIndex framework (Settings, VectorStoreIndex, query engine)
- `llama-index-llms-ollama` -- Ollama integration for local Llama 3
- `llama-index-embeddings-huggingface` -- local BGE-small embeddings
- `llama-index-readers-file` -- `SimpleDirectoryReader` with format-specific extractors
- `pymupdf` -- PDF text extraction backend used by `PyMuPDFReader`
