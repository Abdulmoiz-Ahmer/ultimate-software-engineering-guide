# RAGAS Automated Evaluation -- Python

Python implementation using the `ragas` library with a local Llama 3 judge via Ollama's OpenAI-compatible API.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure Ollama is running with `llama3` pulled:

```bash
ollama pull llama3
```

## Run

```bash
python main.py
```

The script evaluates a deliberately wrong answer and prints Faithfulness and Answer Correctness scores. Both should be low, confirming the metrics detect the hallucination.

## Dependencies

- `ragas` -- RAGAS evaluation framework with built-in metrics and judge LLM support
- `datasets` -- HuggingFace Datasets for creating the evaluation dataset
- `openai` -- OpenAI client pointed at Ollama's local API endpoint
