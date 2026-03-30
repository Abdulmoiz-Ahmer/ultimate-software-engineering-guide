# Gemini Chat CLI

A minimal terminal chatbot powered by Google's **Gemini 2.5 Flash** model. This is the simplest possible LLM chatbot -- create a session, send messages, and get responses with full conversation memory.

## What it does

1. Creates a chat session with the Gemini API.
2. You type a message; the model responds.
3. The session tracks conversation history automatically, so the model remembers context (e.g., your name, earlier questions).

## Key concepts

- **`genai.Client`** -- authenticates with the Gemini API using your key.
- **`client.chats.create`** -- creates a stateful chat session that accumulates message history.
- **`chat.send_message`** -- sends user input and returns the model's response. History is appended internally.

## Prerequisites

- Python 3.10+
- A Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/))

## Setup

```bash
pip install -r requirements.txt
```

Copy `example.env` to `.env` and add your API key:

```bash
cp example.env .env
# Edit .env and set GEMINI_API_KEY=your_key_here
```

## Usage

```bash
python main.py
```

Type messages and the bot responds. Type `q` to quit.
