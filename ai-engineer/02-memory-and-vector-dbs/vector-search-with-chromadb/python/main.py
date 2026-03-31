"""
Vector Search with ChromaDB

A semantic search engine that stores documents in a ChromaDB vector
database and retrieves the most relevant results by meaning, not
keywords. This builds on the embeddings concept from the previous
project by introducing persistent storage and nearest-neighbor search.

Flow:
  1. Store documents in ChromaDB (auto-embedded on insert).
  2. User types a search query.
  3. ChromaDB embeds the query and finds the nearest stored documents.
  4. Results are ranked by distance (lower = more similar).

ChromaDB handles embedding automatically using its built-in model,
so there is no manual encode step like with sentence-transformers.
"""

import chromadb


# -- 1. Initialize the vector database ------------------------------------
# PersistentClient saves data to disk at ./chroma_db so it survives
# between runs. Use chromadb.Client() for a temporary in-memory store.

print("Initializing vector database...")
client = chromadb.PersistentClient(path="./chroma_db")

# A collection is ChromaDB's equivalent of a database table. Each
# collection stores documents, their embeddings, and optional metadata.
collection = client.get_or_create_collection(name="my_collection")


# -- 2. Add documents to the collection -----------------------------------
# ChromaDB embeds documents automatically on insert using its built-in
# embedding model. Each document needs a unique ID for retrieval.

documents = [
    "Batman is a fictional character.",
    "Batman is a witty character.",
    "Pineapple pizza is a controversial topic.",
    "Green arrow movie is coming out soon.",
    "The cat is on the roof.",
    "Have you ever tried ice tea?",
]

ids = ["doc1", "doc2", "doc3", "doc4", "doc5", "doc6"]

print("Storing documents in ChromaDB...")
collection.add(documents=documents, ids=ids)

print("-" * 50)
print("Vector search ready.")
print("-" * 50)


# -- 3. Interactive search loop --------------------------------------------
# The user types a concept or phrase. ChromaDB embeds the query using the
# same model used for the documents, then returns the n closest matches
# ranked by distance (lower distance = higher semantic similarity).

while True:
    user_input = input("\nSearch (or 'q' to quit): ")

    if user_input.lower() in ("q", "e", "quit", "exit"):
        break

    results = collection.query(query_texts=[user_input], n_results=3)

    print("\nTop results:")
    for idx, document in enumerate(results["documents"][0]):
        distance = results["distances"][0][idx]
        print(f"  {idx + 1}. {document} (distance: {distance:.4f})")
