# Tone Converter with Llama 3 (Local/Offline)

A fully local tone converter that rewrites angry or rude text into professional, polite language using **Llama 3** via [Ollama](https://ollama.com/). No API keys or cloud services required.

## Features

- **Fully Local:** Runs entirely on your machine using Ollama + Llama 3.
- **Tone Conversion:** Rewrites aggressive text into professional, constructive language using prompt engineering.
- **No API Key Needed:** Zero cloud dependencies.

## Prerequisites

- Python 3.10 or higher
- [Ollama](https://ollama.com/) installed and running
- Llama 3 model pulled:
    ```bash
    ollama pull llama3
    ```

## Installation

1. **Navigate to the project:**

    ```bash
    cd ai-engineer/tone-converter-with-llama3
    ```

2. **Set up the Virtual Environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

```bash
python main.py
```

Paste your angry text and get a professional rewrite. Type `q` or `e` to exit.
