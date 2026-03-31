# Local Tone Rewriter (Ollama)

Rewrites angry or rude text into professional language using **Llama 3** running locally via [Ollama](https://ollama.com/). No API keys or cloud services needed.

This is the local/offline counterpart to the Gemini-based [professional-tone-rewriter](../professional-tone-rewriter/). Same prompt engineering approach, but runs entirely on your machine.

## What it does

1. You paste raw text (angry email, rude message, etc.).
2. The local Llama 3 model rewrites it to be professional, constructive, and concise.
3. Each rewrite is a standalone call -- there is no conversation history between turns.

## Key concepts

- **System role message** -- the Ollama chat API accepts a system message that acts like a system instruction, defining the model's persona and rules.
- **Fully local** -- no API keys, no network calls, no data leaves your machine.

## Comparison with Gemini version

| | Gemini version | This version |
|---|---|---|
| Model | Gemini 2.5 Flash (cloud) | Llama 3 (local) |
| API key required | Yes | No |
| Conversation history | Yes (chat session) | No (standalone calls) |
| Temperature control | Yes (configurable) | Default |

## Prerequisites

- [Ollama](https://ollama.com/) installed and running
- Llama 3 model pulled:
  ```bash
  ollama pull llama3
  ```

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
