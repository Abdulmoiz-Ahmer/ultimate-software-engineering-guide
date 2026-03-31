# LangChain PDF RAG with Conversation Memory -- Python

Python implementation using LangChain's `PyPDFLoader` for PDF ingestion with full conversation memory.

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

Place your PDF in this folder (default: `typesofpl.pdf`), then run:

```bash
python main.py
```

Ask questions about the PDF content. Follow-up questions work naturally. Type `q` to quit.

## Customization

Replace `typesofpl.pdf` with any PDF and update the `pdf_path` variable in `main.py`. Adjust `chunk_size`, `chunk_overlap`, and `k` to tune retrieval quality.

## Dependencies

Same as the LangChain RAG with Memory pipeline, plus:
- `pypdf` -- backend used by `PyPDFLoader` to parse PDF files
