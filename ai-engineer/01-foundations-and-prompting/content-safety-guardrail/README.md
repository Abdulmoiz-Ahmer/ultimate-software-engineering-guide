# Content Safety Guardrail

A chatbot with a **two-stage pipeline**: every user message passes through a moderation model before reaching the main chat model. Built with Google's **Gemini 2.5 Flash**.

## What it does

```
User input -> Moderation model (pass/block) -> Chat model -> Response
```

1. The moderation model analyzes the input and returns a JSON verdict: `{"is_safe": true/false, "reason": "..."}`.
2. If the input is blocked, the chat model never sees it and the user gets a short explanation.
3. If the input passes, the chat model responds normally with full conversation history.

## Key concepts

- **Guardrail pattern** -- a separate, stateless model call screens input before it reaches the main model. This keeps safety logic decoupled from chat logic.
- **Structured JSON output** -- `response_mime_type="application/json"` forces the model to return valid JSON, making the verdict easy to parse programmatically.
- **Temperature 0.0** -- deterministic output for the moderation call ensures consistent safety decisions.
- **Separate model instances** -- the moderation call is stateless (one-shot), while the chat session preserves conversation history.

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

Type messages and the safety shield screens them before the chatbot responds. Blocked messages show the reason. Type `q` to quit.
