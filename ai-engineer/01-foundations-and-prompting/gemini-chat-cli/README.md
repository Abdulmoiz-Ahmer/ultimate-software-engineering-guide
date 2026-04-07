# Gemini Chat CLI

A minimal terminal chatbot powered by Google's **Gemini 2.5 Flash** model. This is the simplest possible LLM chatbot -- create a session, send messages, and get responses with full conversation memory.

## What it does

1. Creates a chat session with the Gemini API.
2. You type a message; the model responds.
3. The session tracks conversation history automatically, so the model remembers context (e.g., your name, earlier questions).

## Key concepts

- **API client** -- authenticates with the Gemini API using your key.
- **Chat session** -- a stateful session that accumulates message history across turns.
- **Conversation memory** -- the model remembers what was said earlier because the session appends every exchange internally.

## Prerequisites

- A Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/))

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
| JavaScript | [js/](js/) |
