import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODERATION_MODEL = "gemini-2.5-flash"
CHAT_MODEL = "gemini-2.5-flash"

MODERATION_INSTRUCTION = """
You are a content safety shield. Analyze the user's input.
Return a valid JSON object: {"is_safe": boolean, "reason": "string"}.
Rules:
- Block hate speech, violence, illegal acts, and personal insults.
- Allow casual conversation and technical questions.
- If unsafe, provide a short, polite reason.
"""
chat = client.chats.create(model=CHAT_MODEL)
print("Booting...")
print("Welcome to Secure Chatbot")
print("Type 'q' or 'e' to exit.")
print("-" * 100)

while True:
    user_input = input()
    if user_input.lower() in ["q", "e"]:
        print("Goodbye!")
        break

    try:
        moderation_reponse = client.models.generate_content(
            model=MODERATION_MODEL,
            contents=f"Analyze this text:{user_input}",
            config=types.GenerateContentConfig(
                system_instruction=MODERATION_INSTRUCTION,
                response_mime_type="application/json",
                temperature=0.0
            )
        )

        safety_repsonse = json.loads(moderation_reponse.text)
        is_safe = safety_repsonse.get("is_safe", False)
        reason = safety_repsonse.get("reason", "Unknown safety error")

        if not is_safe:
            print(f"Safety Reason: {reason}")
            continue

    except Exception as e:
        print(f"Safety Reason: {e}")


    try:
        print("Sending response...")
        response = chat.send_message(user_input)
        print(f"Bot:{response}")
    except Exception as e:
        print(f"Bot:{e}")