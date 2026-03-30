# 01 -- Foundations and Prompting

This module covers the fundamentals of working with LLMs: making API calls, prompt engineering, system instructions, safety guardrails, and running models locally. Each project builds on the previous one.

## Learning path

### 1. [Gemini Chat CLI](gemini-chat-cli/)

Your first LLM app -- a minimal terminal chatbot powered by Gemini 2.5 Flash. Covers API key setup, the `google-genai` SDK, and how chat sessions preserve context across messages.

**You learn:** How to connect to an LLM API, send messages, and maintain conversation history.

**Key concepts:** API clients, chat sessions, conversation memory

---

### 2. [Professional Tone Rewriter](professional-tone-rewriter/)

Takes angry or rude text and rewrites it professionally. Introduces prompt engineering by giving the model a persona ("Senior Corporate Communications Specialist") and tuning creativity with the temperature parameter.

**You learn:** How to control model behavior using system instructions and temperature.

**Key concepts:** System instructions, prompt engineering, temperature control

---

### 3. [Content Safety Guardrail](content-safety-guardrail/)

Adds a content safety layer in front of a chatbot. A dedicated moderation model analyzes each message for harmful content (returning structured JSON), and only safe messages reach the chatbot.

**You learn:** How to build a two-model pipeline where one model screens input before another responds.

**Key concepts:** Multi-model pipelines, structured JSON output, content moderation, guardrail pattern

---

### 4. [Local Tone Rewriter (Ollama)](local-tone-rewriter-ollama/)

Rebuilds the tone rewriter using Llama 3 running locally via Ollama. Same prompt engineering concepts, but fully offline -- no API keys, no cloud services, no data leaves your machine.

**You learn:** How to run models locally with no cloud dependency using Ollama.

**Key concepts:** Local inference, Ollama, open-source models

## Prerequisites

- Python 3.10+
- A Gemini API key (projects 1-3) -- get one from [Google AI Studio](https://aistudio.google.com/)
- [Ollama](https://ollama.com/) with `llama3` pulled (project 4 only)

Each project has its own `README.md` and `requirements.txt` with setup instructions.
