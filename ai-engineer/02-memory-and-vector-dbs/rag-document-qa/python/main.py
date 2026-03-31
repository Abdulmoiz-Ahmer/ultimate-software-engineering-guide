"""
RAG Document Q&A

Retrieval-Augmented Generation (RAG) chatbot that answers questions
about a text document. Combines vector search (ChromaDB) with local
LLM generation (Llama 3 via Ollama).

The RAG pipeline has three stages:
  1. Retrieve -- find the most relevant chunks from the vector database.
  2. Augment  -- inject the retrieved chunks into the system prompt.
  3. Generate -- the LLM answers using only the provided context.

This ensures the model's answers are grounded in the actual document
rather than its training data, reducing hallucination.
"""

import os

import chromadb
import ollama


# -- Chunking utility ------------------------------------------------------
# Splits text into fixed-size chunks with overlap. Overlap ensures that
# sentences spanning a chunk boundary are captured in at least one chunk,
# so retrieval doesn't miss partial context.

def get_chunks(text, chunk_size=20, overlap=5):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


# -- 1. Load and chunk the source document ---------------------------------

file_path = os.path.join(os.path.dirname(__file__), "company_policy.txt")
if not os.path.exists(file_path):
    print(f"Error: {file_path} not found.")
    exit(1)

with open(file_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

text_chunks = get_chunks(raw_text)
print(f"Document split into {len(text_chunks)} chunks.")


# -- 2. Store chunks in ChromaDB -------------------------------------------
# The collection is recreated on each run to avoid duplicate entries.
# ChromaDB auto-embeds documents using its built-in model on insert.

print("Initializing vector database...")
client = chromadb.PersistentClient(path="./rag_db")

try:
    client.delete_collection("policy_collection")
except Exception:
    pass

collection = client.get_or_create_collection(name="policy_collection")
ids = [f"chunk_{i}" for i in range(len(text_chunks))]
collection.add(documents=text_chunks, ids=ids)

print("Chunks embedded and stored.")
print("-" * 50)
print("Document Q&A ready. Type 'q' to quit.")
print("-" * 50)


# -- 3. RAG loop -----------------------------------------------------------
# Each turn:
#   a) Retrieve the 3 most relevant chunks for the user's question.
#   b) Build a system prompt that includes the retrieved context and
#      instructs the model to answer only from that context.
#   c) Send the augmented prompt + question to Llama 3 for generation.

while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ("q", "e", "quit", "exit"):
        break

    # Step A: Retrieve -- semantic search over the stored chunks.
    print("   [Searching for relevant context...]")
    results = collection.query(query_texts=[user_input], n_results=3)
    retrieved_context = "\n".join(results["documents"][0])

    # Step B: Augment -- inject retrieved chunks into the system prompt.
    # The instruction constrains the model to only use the provided context.
    system_prompt = f"""You are a helpful assistant. Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say "I don't know based on the provided document."

CONTEXT:
{retrieved_context}
"""

    # Step C: Generate -- send to Llama 3 via Ollama.
    print("   [Generating answer...]")
    try:
        response = ollama.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
        )
        print(f"\nBot: {response['message']['content']}")
    except Exception as e:
        print(f"Error: {e}")
