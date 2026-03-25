import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file (GEMINI_API_KEY)
load_dotenv()

# Initialize the Gemini client with the API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# --- PROMPT ENGINEERING ---
# This is where we define the "Brain" of the application.
# We give it a specific persona and strict rules.
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

# Create a chat session with a system instruction (persona) and temperature setting
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=SYS_INSTRUCT, # Injecting the persona
        temperature=0.7 # Creativity control (0.0 = deterministic, 1.0 = creative)
    )
)

print("Booting...")
print("Welcome to Professional Tone Converter")
print("Paste your angry email below. Type 'q' or 'e' to exit.")
print("-" * 100)

# Main loop — keeps accepting input until the user quits
while True:
    user_input = input("\nAngry Input: ")

    # Exit condition
    if user_input.lower() in ['q', 'e', 'quit', 'exit']:
        break

    try:
        # Send the angry text to the model for rewriting
        response = chat.send_message(user_input)

        print(f"\n✨ Professional: {response.text}")
        print("-" * 100)

    except Exception as e:
        print(f"Error: {e}")
