"""
Professional Tone Rewriter

Rewrites angry or rude text into polished, professional language using
Google's Gemini 2.5 Flash model. This project demonstrates two core
prompt engineering techniques:

  1. System instructions -- giving the model a specific persona and
     strict behavioral rules so it consistently produces the desired output.
  2. Temperature control -- tuning the creativity/randomness of the
     model's responses (0.0 = deterministic, 1.0 = highly creative).

The chat session preserves history, so the model can reference earlier
rewrites if needed.
"""

import os

from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load the GEMINI_API_KEY from the .env file.
load_dotenv()

# Initialize the Gemini client with the API key.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


# -- System instruction (prompt engineering) -------------------------------
# This is the core of the application. The system instruction defines the
# model's persona and rules. It acts as a persistent directive that applies
# to every message in the chat session.

SYS_INSTRUCT = """
You are a Senior Corporate Communications Specialist.
Your task is to rewrite the user's input to be:
1. Professional and polite.
2. Constructive (focus on solutions, not blame).
3. Concise.

Rules:
- Remove all swearing, insults, and aggressive punctuation (!!!).
- Do not change the core message or intent.
- Output ONLY the rewritten text. Do not add "Here is the rewritten version:".
"""

# Create a chat session with the persona injected via system_instruction.
# temperature=0.7 gives a balance between consistency and natural variation.
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYS_INSTRUCT,
        temperature=0.7,
    ),
)

print("Professional Tone Rewriter")
print("Paste your text below. Type 'q' or 'e' to exit.")
print("-" * 50)


# -- Main loop -------------------------------------------------------------
# Each iteration takes the user's raw text, sends it to Gemini (which
# applies the system instruction), and prints the rewritten version.

while True:
    user_input = input("\nOriginal: ")

    if user_input.lower() in ("q", "e", "quit", "exit"):
        break

    try:
        response = chat.send_message(user_input)
        print(f"\nRewritten: {response.text}")
        print("-" * 50)
    except Exception as e:
        print(f"Error: {e}")
