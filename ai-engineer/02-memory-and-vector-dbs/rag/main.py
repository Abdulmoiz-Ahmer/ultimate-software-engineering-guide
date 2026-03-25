import chromadb
import ollama
import os

print("Building Document Knowledge Base...")

# Split text into overlapping chunks so that context isn't lost at chunk boundaries
# overlap ensures sentences that span two chunks are still captured
def get_chunks(text, chunk_size=20, overlap=5):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

# Load the source document that the chatbot will answer questions about
file_path = os.path.join(os.path.dirname(__file__), "company_policy.txt")
if not os.path.exists(file_path):
    print(f"Error: {file_path} not found. Please make sure the file exists.")
    exit(1)

with open(file_path, "r", encoding="utf-8") as file:
    raw_text = file.read()

# Break the document into smaller chunks for more precise retrieval
text_chunks = get_chunks(raw_text)

print(f"Document sliced into {len(text_chunks)} chunks.")
print("Initializing Local Vector Database...")

# Create a persistent ChromaDB client — data is saved to disk at ./rag_db
client = chromadb.PersistentClient(path="./rag_db")

# Delete existing collection to avoid duplicate entries on re-runs
try:
    client.delete_collection("policy_collection")
except:
    pass

# Create a fresh collection — ChromaDB auto-embeds documents using its default model
collection = client.get_or_create_collection(name="policy_collection")

# Generate unique IDs for each chunk
ids = [f"chunk_{i}" for i in range(len(text_chunks))]

# Store chunks in the vector database (embedding happens automatically)
print("Chunks embedded and saved to vector database!\n...")
collection.add(documents=text_chunks, ids=ids)

print("-" * 100)
print("Chat with your Document (Type 'q' or 'e' to quit)")
print("-" * 100)

# Main RAG loop: retrieve relevant chunks, then generate an answer with Llama 3
while True:
    user_input = input("\nYou: ")

    # Exit condition
    if user_input.lower() in ['q', 'e', 'quit', 'exit']:
        break

    # STEP 1: Retrieval — find the 3 most relevant chunks from the vector database
    print("   [Searching database for context...]")
    results = collection.query(query_texts=[user_input], n_results=3)

    # Combine retrieved chunks into a single context string
    retrieved_context = "\n".join(results['documents'][0])

    # STEP 2: Augmented Generation — inject the retrieved context into the system prompt
    # The model is instructed to only use the provided context, not its own training data
    system_prompt = f"""
    You are a helpful assistant. Answer the user's question using ONLY the context provided below.
    If the answer is not in the context, say "I don't know based on the provided document."

    CONTEXT:
    {retrieved_context}
    """

    # STEP 3: Generate — send the augmented prompt + user question to Llama 3
    print("   [Reading chunks and generating answer...]")
    try:
        response = ollama.chat(
            model='llama3',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_input}
            ]
        )
        print(f"\nLlama 3: {response['message']['content']}")

    except Exception as e:
        print(f"Error talking to model: {e}")
