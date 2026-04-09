# Content Safety Guardrail -- JavaScript

Node.js implementation using the `@google/genai` SDK with ES modules.

## Setup

```bash
npm install
```

Copy `example.env` to `.env` and add your API key:

```bash
cp example.env .env
# Edit .env and set GEMINI_API_KEY=your_key_here
```

Get a key from [Google AI Studio](https://aistudio.google.com/).

## Run

```bash
npm run gcli
# or
node index.js
```

Type messages and the safety shield screens them before the chatbot responds. Blocked messages show the reason. Type `q` to quit.

## Differences from the Python version

- Uses `readline` with a recursive callback for the input loop.
- `ai.models.generateContent` is the one-shot moderation call (equivalent to Python's `client.models.generate_content`).
- `responseMimeType: 'application/json'` forces structured JSON output (equivalent to Python's `response_mime_type`).
- Nullish coalescing (`??`) replaces Python's `.get()` with defaults for safe JSON parsing.

## Dependencies

- `@google/genai` -- Google's Gemini SDK for JavaScript
- `dotenv` -- loads environment variables from `.env`
