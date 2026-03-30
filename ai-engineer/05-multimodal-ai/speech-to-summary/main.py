"""
Speech to Summary

A two-stage multimodal pipeline that converts a voice note into a
clean executive summary:

  Stage 1 (Whisper): Audio file -> raw transcription text
  Stage 2 (Llama 3.1): Raw transcription -> structured summary

OpenAI's Whisper model handles speech-to-text locally (no API key
needed). The transcription is then passed to Llama 3.1 via LangChain,
which cleans up filler words and formats the output as bullet points
with action items.

This demonstrates chaining two different AI models together:
a specialized audio model for transcription and a general-purpose
LLM for text processing.
"""

import os

import whisper
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


# -- 1. Locate the audio file ----------------------------------------------
# Change this to the name of your voice recording. Supported formats
# include mp3, wav, m4a, and most common audio types.

audio_file = "voice_note.mp3"

if not os.path.exists(audio_file):
    print(f"Error: Could not find '{audio_file}'. Place an audio file in this folder.")
    exit()


# -- 2. Transcribe with Whisper --------------------------------------------
# Whisper is OpenAI's open-source speech recognition model. The "base"
# model is fast and accurate for English, and runs easily on standard
# laptops without a GPU. Larger models (small, medium, large) improve
# accuracy at the cost of speed and memory.

print("Loading Whisper model...")
model = whisper.load_model("base")

print(f"Transcribing '{audio_file}'...")
result = model.transcribe(audio_file)
transcription_text = result["text"]

print("\nRaw transcription:")
print("-" * 50)
print(transcription_text)
print("-" * 50)


# -- 3. Summarize with Llama 3.1 -------------------------------------------
# The raw transcription often contains filler words (um, uh), repetition,
# and unstructured rambling. The LLM cleans it up and extracts the key
# points. temperature=0.3 adds slight expressiveness while keeping the
# summary focused.
#
# The pipe operator (prompt | llm) is LangChain's LCEL syntax for chaining
# a prompt template directly into an LLM -- equivalent to calling
# llm.invoke(prompt.format(...)) but composable with other components.

print("\nSummarizing with Llama 3.1...")

llm = ChatOllama(model="llama3.1", temperature=0.3)

prompt = ChatPromptTemplate.from_messages([
    ("system", (
        "You are an expert executive assistant. Read the following "
        "transcribed voice note. Clean up any spoken filler words "
        "(like 'um' or 'uh'). Summarize the core message into 3 crisp "
        "bullet points, and add a 'Next Steps / Action Items' section "
        "if applicable."
    )),
    ("human", "{text}"),
])

chain = prompt | llm

try:
    summary_response = chain.invoke({"text": transcription_text})

    print("\nExecutive Summary:")
    print("=" * 50)
    print(summary_response.content)
    print("=" * 50)

except Exception as e:
    print(f"Error during summarization: {e}")
