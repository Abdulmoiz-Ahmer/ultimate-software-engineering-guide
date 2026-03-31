# Local Tone Rewriter (Ollama) -- Python

Python implementation using the `ollama` package.

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

Paste your text and get a professional rewrite. Type `q` to quit.

## Dependencies

- `ollama` -- Python client for the Ollama API, used to call `ollama.chat()` with system messages
