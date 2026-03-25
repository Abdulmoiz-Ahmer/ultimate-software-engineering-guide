import chromadb

print("Initializing Local Vector Database...")

# Create a persistent ChromaDB client — data is saved to disk at ./chroma_db
# so it survives between runs (unlike an in-memory client)
client = chromadb.PersistentClient(path="./chroma_db")

# Get or create a collection — a collection is like a "table" for vectors
# ChromaDB automatically handles embedding the documents using its default model
collection = client.get_or_create_collection(name="my_collection")

# Sample documents to store in the vector database
documents = [
    "Batman is a fictional character.",
    "Batman is a witty character.",
    "Pineapple pizza is a controversial topic.",
    "Green arrow movie is coming out soon.",
    "The cat is on the roof.",
    "Have you ever tried ice tea?"
]

# Each document needs a unique ID for storage and retrieval
ids = ["doc1", "doc2", "doc3", "doc4", "doc5", "doc6"]

# Add documents to the collection — ChromaDB embeds them automatically
print("Saving documents to ChromaDB...")
collection.add(documents=documents, ids=ids)

print("-" * 100)
print("Semantic Search Engine Online")
print("-" * 100)

# Main search loop — user types a concept and gets the closest matching documents
while True:
    user_input = input("\nSearch for a concept (or type 'q'or 'e' to quit): ")

    # Exit condition
    if user_input.lower() in ['q', 'e', 'quit', 'exit']:
        break

    # Query the collection — ChromaDB embeds the query and finds the 3 nearest documents
    # Results are ranked by distance (lower = more similar)
    results = collection.query(query_texts=[user_input], n_results=3)

    print("\nTop Results Found:")

    # Display each result with its distance score
    for ids, document in enumerate(results['documents'][0]):
        distance = results['distances'][0][ids]
        print(f"{ids+1}. {document} (Distance: {distance:.4f})")
