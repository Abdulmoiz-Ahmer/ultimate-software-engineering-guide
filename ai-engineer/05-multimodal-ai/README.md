# 05 -- Multimodal AI

This module covers how LLMs work with inputs beyond text -- images and audio. Each project chains a specialized model (vision or speech) with a general-purpose LLM, showing how multimodal pipelines are built in practice.

## Learning path

### 1. [Vision Model Image Analysis](vision-model-image-analysis/)

Sends an image to a local vision model (Llama 3.2 Vision) for analysis. The image is base64-encoded and passed alongside a text prompt in a multimodal message. The model either extracts structured data (receipts) or describes the scene (general images).

**You learn:** How to build multimodal messages with text and image content blocks, base64 data URIs, and how vision models process both inputs together.

**Key concepts:** Multimodal HumanMessage, base64 encoding, vision models, data URI format

---

### 2. [Speech to Summary](speech-to-summary/)

A two-stage pipeline: OpenAI's Whisper transcribes a voice note to text, then Llama 3.1 cleans up filler words and formats the output as bullet points with action items. Demonstrates chaining two different AI models -- a specialized audio model and a general-purpose LLM.

**You learn:** How to chain specialized models together, speech-to-text with Whisper, and LangChain's LCEL pipe operator for composable prompt-to-LLM chains.

**Key concepts:** Whisper speech recognition, two-model pipeline, LCEL pipe operator, structured summarization

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3.2-vision` (project 1) and `llama3.1` (project 2) pulled
- `ffmpeg` installed (project 2 only, required by Whisper)

Each project has its own `README.md` and `requirements.txt` with setup instructions.
