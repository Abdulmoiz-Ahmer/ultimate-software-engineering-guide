# Gemini Chat CLI -- JavaScript

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

Type messages and the bot responds. Type `q` to quit.

## Differences from the Python version

- Uses `readline` with a recursive callback for the input loop (Node.js has no synchronous `input()` like Python).
- `dotenv/config` import auto-loads `.env` on startup (equivalent to `load_dotenv()`).
- The `@google/genai` SDK mirrors the Python `google-genai` SDK with the same chat session API.

## Dependencies

- `@google/genai` -- Google's Gemini SDK for JavaScript
- `dotenv` -- loads environment variables from `.env`
