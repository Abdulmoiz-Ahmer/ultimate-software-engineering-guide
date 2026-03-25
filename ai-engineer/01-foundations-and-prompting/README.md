# 01 — Foundations and Prompting

This module covers the fundamentals of working with LLMs: making API calls, prompt engineering, system instructions, safety guardrails, and running models locally. Each project builds on the previous one.

## Learning Path

Work through these projects in order:

### 1. [Simple CLI Chatbot](simple-cli-chatbot/)
> **You will learn:** How to connect to an LLM API, send messages, and maintain conversation history.

Your first LLM app — a terminal chatbot powered by Gemini 2.5 Flash. Covers API key setup, the `google-genai` SDK, and how chat sessions preserve context across messages.

**Key concepts:** API clients, chat sessions, conversation memory

---

### 2. [Tone Converter](tone-converter/)
> **You will learn:** How to control model behavior using system instructions and temperature.

Takes angry or rude text and rewrites it professionally. Introduces prompt engineering by giving the model a persona ("Senior Corporate Communications Specialist") and tuning creativity with the temperature parameter.

**Key concepts:** System instructions, prompt engineering, temperature control

---

### 3. [Input Moderation with Guardrail](input-moderation-with-guard-rail/)
> **You will learn:** How to build a two-model pipeline where one model screens input before another responds.

Adds a content safety layer in front of a chatbot. A dedicated moderation model analyzes each message for harmful content (returning structured JSON), and only safe messages reach the chatbot.

**Key concepts:** Multi-model pipelines, structured JSON output, content moderation

---

### 4. [Tone Converter with Llama 3](tone-converter-with-llama3/)
> **You will learn:** How to run models locally with no cloud dependency using Ollama.

Rebuilds the tone converter using Llama 3 running locally via Ollama. Same prompt engineering concepts, but fully offline — no API keys, no cloud services.

**Key concepts:** Local inference, Ollama, open-source models
