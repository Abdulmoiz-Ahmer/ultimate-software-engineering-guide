import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file (GEMINI_API_KEY)
load_dotenv()

# Initialize the Gemini client with the API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Both the moderation layer and chat use the same model (but separate instances)
MODERATION_MODEL = "gemini-2.5-flash"
CHAT_MODEL = "gemini-2.5-flash"

# System prompt for the moderation model — acts as a content safety shield
# Returns structured JSON with is_safe (boolean) and reason (string)
MODERATION_INSTRUCTION = """
You are a content safety shield. Analyze the user's input.
Return a valid JSON object: {"is_safe": boolean, "reason": "string"}.
Rules:
- Block hate speech, violence, illegal acts, and personal insults.
- Allow casual conversation and technical questions.
- If unsafe, provide a short, polite reason.
"""

# Create a chat session for the main chatbot (maintains conversation history)
chat = client.chats.create(model=CHAT_MODEL)

print("Booting...")
print("Welcome to Secure Chatbot")
print("Type 'q' or 'e' to exit.")
print("-" * 100)

# Main loop — each message goes through moderation before reaching the chatbot
while True:
    user_input = input()

    # Exit condition
    if user_input.lower() in ["q", "e"]:
        print("Goodbye!")
        break

    # --- STEP 1: Moderation Gate ---
    # A separate one-shot call (not chat) screens the input for safety
    try:
        moderation_response = client.models.generate_content(
            model=MODERATION_MODEL,
            contents=f"Analyze this text:{user_input}",
            config=types.GenerateContentConfig(
                system_instruction=MODERATION_INSTRUCTION,
                response_mime_type="application/json", # Forces JSON output
                temperature=0.0 # Deterministic — no creativity for safety checks
            )
        )

        # Parse the JSON safety verdict
        safety_response = json.loads(moderation_response.text)
        is_safe = safety_response.get("is_safe", False)
        reason = safety_response.get("reason", "Unknown safety error")

        # Block unsafe input and skip to next iteration
        if not is_safe:
            print(f"Safety Reason: {reason}")
            continue

    except Exception as e:
        print(f"Safety Reason: {e}")

    # --- STEP 2: Chat Response ---
    # Only reached if moderation passed — send the input to the chatbot
    try:
        print("Sending response...")
        response = chat.send_message(user_input)
        print(f"Bot:{response}")
    except Exception as e:
        print(f"Bot:{e}")
