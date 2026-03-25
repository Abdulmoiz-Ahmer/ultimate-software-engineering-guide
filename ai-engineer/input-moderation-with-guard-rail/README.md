# Input Moderation with Guardrail (Gemini 2.5)

A secure chatbot that uses a two-model pipeline: a **content safety shield** that screens user input before it reaches the main chatbot. Built with Google's **Gemini 2.5 Flash**.

## Features

- **Safety Guardrail:** A dedicated moderation model analyzes input for hate speech, violence, illegal acts, and personal insults before the chatbot responds.
- **Structured JSON Moderation:** The safety model returns structured `{"is_safe": boolean, "reason": "string"}` responses.
- **Conversation Memory:** The chat model maintains context across messages.
- **Secure:** Uses `.env` to protect API keys.

## Prerequisites

- Python 3.10 or higher
- A Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1. **Navigate to the project:**

    ```bash
    cd ai-engineer/input-moderation-with-guard-rail
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

Type your messages and the safety shield will screen them before the chatbot responds. Type `q` or `e` to exit.
