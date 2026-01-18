import os
from google import genai
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Initialize the Client (The new way)
# It automatically looks for "GEMINI_API_KEY" or "GOOGLE_API_KEY" in your .env
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# 3. Create a Chat Session
# Note: The model name 'gemini-2.0-flash' is the current standard for this SDK. but on free plan we can use 1.5 or 2.5 flash
chat = client.chats.create(model="gemini-2.5-flash")

print("Booting...")
print("Type 'q' or 'e' to exit.")
print("-" * 100)

while True:
    user_input = input("You: ")
    
    if user_input.lower() in ['q', 'e', 'exit', "quit"]:
        print("Shutting down...")
        break

    try:
        # 4. Send Message (Streamed)
        response = chat.send_message(user_input)
        
        print("Bot: ", end="")
        # The new SDK handles text access slightly differently
        print(response.text)
        print("\n")
        
    except Exception as e:
        print(f"Error: {e}")