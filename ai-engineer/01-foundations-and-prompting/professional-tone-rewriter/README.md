# Professional Tone Rewriter

Rewrites angry or rude text into polished, professional language using Google's **Gemini 2.5 Flash** model. This project demonstrates **prompt engineering** -- using a system instruction to give the model a specific persona and strict behavioral rules.

## What it does

1. You paste raw text (angry email, rude message, etc.).
2. The model rewrites it to be professional, constructive, and concise.
3. The core message and intent are preserved -- only the tone changes.

## Key concepts

- **System instruction** -- a persistent directive injected into the chat session that defines the model's persona ("Senior Corporate Communications Specialist") and rules (no swearing, no blame, output only the rewrite).
- **Temperature** -- controls randomness. Lower values produce more deterministic output; higher values introduce more creativity.
- **Chat session** -- preserves conversation history so the model can reference earlier rewrites.

## Prerequisites

- A Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/))

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
