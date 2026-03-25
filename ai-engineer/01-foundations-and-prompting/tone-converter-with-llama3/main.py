import ollama

# System prompt — gives the model a "Corporate Communications Specialist" persona
# that rewrites angry text into professional language
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

print("Booting...")
print("Welcome to Secure Local Chatbot")
print("Type 'q' or 'e' to exit.")
print("-" * 100)

# Main loop — keeps accepting input until the user quits
while True:
    user_input = input("\nAngry Input: ")

    # Exit condition
    if user_input.lower() in ['q', 'e', 'quit', 'exit']:
        break

    try:
        print("Rewriting input...")
        # Send to local Llama 3 model via Ollama with system prompt and user input
        response = ollama.chat(
            model='llama3',
            messages=[
                {"role": "system", "content": SYS_INSTRUCT},
                {"role": "user", "content": user_input}
            ]
        )
        # Extract the message content from Ollama's response dict
        print(f"Bot:{response['message']['content']}")
    except Exception as e:
        print(f"Bot:{e}")
