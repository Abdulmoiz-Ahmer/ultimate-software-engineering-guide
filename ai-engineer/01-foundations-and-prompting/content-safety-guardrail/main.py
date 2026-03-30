"""
Content Safety Guardrail

A chatbot with a two-stage pipeline: every user message passes through
a moderation layer before reaching the main chat model. This demonstrates
the guardrail pattern:

  User input -> Moderation model (pass/block) -> Chat model -> Response

The moderation model is a separate, stateless call that returns structured
JSON ({"is_safe": bool, "reason": str}). If the input is blocked, the
chat model never sees it. If it passes, the chat model responds normally
with full conversation history.

Key techniques:
  - Structured JSON output via response_mime_type
  - Temperature 0.0 for deterministic safety checks
  - Separate model instances for moderation vs. chat
"""

import os
import json

from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load the GEMINI_API_KEY from the .env file.
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Both the moderation layer and chat use the same model but as separate
# instances -- the moderation call is stateless (one-shot), while the
# chat session maintains conversation history.
MODERATION_MODEL = "gemini-2.5-flash"
CHAT_MODEL = "gemini-2.5-flash"


# -- Moderation system instruction -----------------------------------------
# Defines what the moderation model should flag and the output format.
# response_mime_type="application/json" forces the model to return valid
# JSON, which we parse to get the safety verdict.

MODERATION_INSTRUCTION = """
You are a content safety shield. Analyze the user's input.
Return a valid JSON object: {"is_safe": boolean, "reason": "string"}.
Rules:
- Block hate speech, violence, illegal acts, and personal insults.
- Allow casual conversation and technical questions.
- If unsafe, provide a short, polite reason.
"""

# The main chat session -- preserves conversation history across turns.
chat = client.chats.create(model=CHAT_MODEL)

print("Secure Chatbot ready. Type 'q' or 'e' to exit.")
print("-" * 50)


# -- Main loop -------------------------------------------------------------
# Each message goes through two stages:
#   1. Moderation gate -- a one-shot call screens the input.
#   2. Chat response   -- only reached if moderation passes.

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ("q", "e", "quit", "exit"):
        print("Goodbye!")
        break

    # -- Step 1: Moderation gate -------------------------------------------
    # A stateless generate_content call (not a chat) checks the input.
    # temperature=0.0 ensures deterministic, consistent safety decisions.
    try:
        moderation_response = client.models.generate_content(
            model=MODERATION_MODEL,
            contents=f"Analyze this text: {user_input}",
            config=types.GenerateContentConfig(
                system_instruction=MODERATION_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.0,
            ),
        )

        safety_response = json.loads(moderation_response.text)
        is_safe = safety_response.get("is_safe", False)
        reason = safety_response.get("reason", "Unknown safety error")

        if not is_safe:
            print(f"[Blocked] {reason}")
            continue

    except Exception as e:
        print(f"[Moderation error] {e}")
        continue

    # -- Step 2: Chat response ---------------------------------------------
    # Only reached if moderation passed. The chat session preserves history
    # so the model has context from earlier turns.
    try:
        response = chat.send_message(user_input)
        print(f"\nBot: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
