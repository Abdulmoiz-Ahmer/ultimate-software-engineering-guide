# Content Safety Guardrail -- Python

Python implementation using the `google-genai` SDK with structured JSON output for moderation.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `example.env` to `.env` and add your API key:

```bash
cp example.env .env
# Edit .env and set GEMINI_API_KEY=your_key_here
```

## Run

```bash
python main.py
```

Type messages and the safety shield screens them before the chatbot responds. Type `q` to quit.

## Dependencies

- `google-genai` -- Google's Gemini SDK (V2), with `response_mime_type="application/json"` to force structured output
- `python-dotenv` -- loads the API key from `.env`
