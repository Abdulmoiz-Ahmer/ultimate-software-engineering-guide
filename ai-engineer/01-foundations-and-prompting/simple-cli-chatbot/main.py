import os
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file (GEMINI_API_KEY)
load_dotenv()

# Initialize the Gemini client with the API key
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Create a chat session — this maintains conversation history automatically
chat = client.chats.create(model="gemini-2.5-flash")

print("Booting...")
print("Type 'q' or 'e' to exit.")
print("-" * 100)

# Main conversation loop
while True:
    user_input = input("You: ")

    # Exit condition
    if user_input.lower() in ['q', 'e', 'exit', "quit"]:
        print("Shutting down...")
        break

    try:
        # Send the user's message and get a response (chat history is preserved)
        response = chat.send_message(user_input)

        print("Bot: ", end="")
        print(response.text)
        print("\n")

    except Exception as e:
        print(f"Error: {e}")
