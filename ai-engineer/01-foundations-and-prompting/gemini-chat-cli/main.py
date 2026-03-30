"""
Gemini Chat CLI

A minimal terminal chatbot using Google's Gemini 2.5 Flash model.
The google-genai SDK's chat session handles conversation history
automatically, so follow-up questions retain context from earlier
in the conversation.

This is the simplest possible example of an LLM-powered chatbot:
  1. Create a chat session.
  2. Send user input.
  3. Print the response.
  4. Repeat.
"""

import os

from google import genai
from dotenv import load_dotenv

# Load the GEMINI_API_KEY from the .env file.
load_dotenv()

# Initialize the Gemini client. The API key authenticates all
# requests to Google's generative AI service.
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Create a chat session. This object tracks the full conversation
# history, so the model remembers prior messages automatically.
chat = client.chats.create(model="gemini-2.5-flash")

print("Chat ready. Type 'q' or 'e' to exit.")
print("-" * 50)

# -- Main conversation loop ------------------------------------------------
# Each iteration reads user input, sends it to Gemini, and prints the reply.
# The chat session appends every exchange to its internal history.

while True:
    user_input = input("You: ")

    if user_input.lower() in ("q", "e", "exit", "quit"):
        print("Shutting down...")
        break

    try:
        response = chat.send_message(user_input)
        print(f"Bot: {response.text}\n")
    except Exception as e:
        print(f"Error: {e}")
