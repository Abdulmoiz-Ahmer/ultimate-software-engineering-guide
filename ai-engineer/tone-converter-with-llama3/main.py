import ollama
import json

MODERATION_INSTRUCTION = """
You are a content safety shield. Analyze the user's input.
Return a valid JSON object: {"is_safe": boolean, "reason": "string"}.
Rules:
- Block hate speech, violence, illegal acts, and personal insults.
- Allow casual conversation and technical questions.
- If unsafe, provide a short, polite reason.
"""

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

while True:
    user_input = input("\nAngry Input: ")
    
    if user_input.lower() in ['q', 'e', 'quit', 'exit']:
        break

    print("   [1/2] Checking safety...")
    
    try:
        moderation_response = ollama.chat(
            model='llama3',
            format='json',
            messages=[
                {"role": "system", "content": MODERATION_INSTRUCTION},
                {"role": "user", "content": f"Analyze this text:{user_input}"}
            ]
        )
        
        safety_response = json.loads(moderation_response.text)
        is_safe = safety_response.get("is_safe", False)
        reason = safety_response.get("reason", "Unknown safety error")   
        
        if not is_safe:
            print(f"Safety Reason: {reason}")
            continue

    except Exception as e:
        print(f"Safety Reason: {e}")
        
        
    try:
        print("   [2/2] Rewriting input...")
        response = ollama.chat(
            model='llama3',
            messages=[
                {"role": "system", "content": SYS_INSTRUCT},
                {"role": "user", "content": user_input}
            ]
        )
        print(f"Bot:{response}")
    except Exception as e:
        print(f"Bot:{e}")           