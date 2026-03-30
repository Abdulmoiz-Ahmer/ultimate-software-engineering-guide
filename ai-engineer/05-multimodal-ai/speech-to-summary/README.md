# Speech to Summary

A two-stage multimodal pipeline that converts a **voice note** into a clean **executive summary**. Chains OpenAI's Whisper (speech-to-text) with Llama 3.1 (text summarization), both running locally.

## How it works

```
Audio file (mp3/wav/m4a)
    |
    v
Stage 1: Whisper transcribes speech to raw text
    |
    v
Stage 2: Llama 3.1 cleans up filler words and
         formats as bullet points + action items
    |
    v
Executive summary output
```

## Key concepts

- **Two-model pipeline** -- a specialized audio model (Whisper) handles transcription, then a general-purpose LLM (Llama 3.1) handles text processing. Each model does what it's best at.
- **Whisper** -- OpenAI's open-source speech recognition model. The `base` model is fast and accurate for English. Larger models (`small`, `medium`, `large`) improve accuracy at the cost of speed.
- **LCEL pipe operator** -- `prompt | llm` is LangChain's expression syntax for chaining a prompt template directly into an LLM. This is composable with other components (retrievers, output parsers, etc.).
- **Structured summarization** -- the system prompt instructs the LLM to remove filler words, extract 3 bullet points, and add action items -- turning unstructured speech into clean, actionable output.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with `llama3.1` pulled
- `ffmpeg` installed (required by Whisper for audio decoding)

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3.1
```

Install ffmpeg if not already present:

```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

## Usage

Place an audio file in the project folder (default: `voice_note.mp3`), then run:

```bash
python main.py
```

The script prints the raw transcription followed by the executive summary.

## Customization

- Change `audio_file` in `main.py` to use a different recording.
- Edit the system prompt to change the summary format (e.g., paragraph instead of bullet points).
- Use a larger Whisper model (`whisper.load_model("medium")`) for better accuracy on noisy audio.
