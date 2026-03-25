# Professional Tone Converter (Gemini 2.5)

A CLI tool that rewrites angry or rude text into professional, polite language using Google's **Gemini 2.5 Flash** model with prompt engineering.

## Features

- **Prompt Engineering:** Uses a system instruction to give the model a "Senior Corporate Communications Specialist" persona.
- **Temperature Control:** Configurable creativity level (default 0.7).
- **Conversation Memory:** Maintains chat context across rewrites.
- **Secure:** Uses `.env` to protect API keys.

## Prerequisites

- Python 3.10 or higher
- A Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1. **Navigate to the project:**

    ```bash
    cd ai-engineer/tone-converter
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

## Configuration

1. Copy the example env file and add your API key:

    ```bash
    cp example.env .env
    ```

2. Edit `.env` and add your key:
    ```env
    GEMINI_API_KEY=your-key-here
    ```

## Usage

```bash
python main.py
```

Paste your angry text and get a professional rewrite. Type `q` or `e` to exit.
