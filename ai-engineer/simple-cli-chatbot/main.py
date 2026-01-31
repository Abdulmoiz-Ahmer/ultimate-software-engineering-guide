import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

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
        response = chat.send_message(user_input)
        
        print("Bot: ", end="")
        print(response.text)
        print("\n")
        
    except Exception as e:
        print(f"Error: {e}")