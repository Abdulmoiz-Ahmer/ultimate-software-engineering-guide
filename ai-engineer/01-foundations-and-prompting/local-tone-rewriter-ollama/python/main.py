"""
Local Tone Rewriter (Ollama)

Rewrites angry or rude text into professional language using Llama 3
running locally via Ollama. No API keys or cloud services needed.

This is the local/offline counterpart to the Gemini-based professional
tone rewriter. It uses the same prompt engineering approach (system
instruction with a persona and strict rules) but runs entirely on
your machine through Ollama's Python SDK.

Unlike the Gemini version, this does not use a persistent chat session.
Each turn is a standalone call with the system prompt and user message,
so there is no conversation history between rewrites.
"""

import ollama


# -- System instruction (prompt engineering) -------------------------------
# Defines the model's persona and rewriting rules. This is passed as the
# "system" role message on every call, giving the model consistent behavior.

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

print("Local Tone Rewriter (Ollama + Llama 3)")
print("Paste your text below. Type 'q' or 'e' to exit.")
print("-" * 50)


# -- Main loop -------------------------------------------------------------
# Each iteration sends a standalone chat request with the system prompt and
# the user's raw text. ollama.chat returns a dict; the rewritten text is
# in response["message"]["content"].

while True:
    user_input = input("\nOriginal: ")

    if user_input.lower() in ("q", "e", "quit", "exit"):
        break

    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": SYS_INSTRUCT},
                {"role": "user", "content": user_input},
            ],
        )
        print(f"\nRewritten: {response['message']['content']}")
    except Exception as e:
        print(f"Error: {e}")
