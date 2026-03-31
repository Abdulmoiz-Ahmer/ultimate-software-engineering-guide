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
- **Structured JSON output** -- forcing the model to return valid JSON makes the verdict easy to parse programmatically.
- **Temperature 0.0** -- deterministic output for the moderation call ensures consistent safety decisions.
- **Separate model instances** -- the moderation call is stateless (one-shot), while the chat session preserves conversation history.

## Prerequisites

- A Gemini API key (get one from [Google AI Studio](https://aistudio.google.com/))

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
