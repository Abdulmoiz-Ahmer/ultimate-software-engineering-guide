"""
Hybrid Search Pipeline -- Python

Demonstrates hybrid search by combining two retrieval strategies:

  1. Vector search (semantic) -- finds documents by meaning similarity.
     Good for natural language queries but struggles with exact IDs,
     error codes, and random strings.

  2. BM25 search (lexical) -- finds documents by keyword matching.
     Good for exact terms like "ERR-77X-992" but misses paraphrases
     and synonyms.

The EnsembleRetriever merges results from both, weighted 50/50, so
you get the best of both worlds. The test query uses an exact error
code to show where vector search fails and hybrid search succeeds.
"""

import logging

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_core.documents import Document

# Suppress noisy HTTP logs from the embedding model download.
logging.getLogger("httpx").setLevel(logging.WARNING)


# -- 1. Configure the embedding model --------------------------------------
# BGE-small is a compact, high-quality embedding model for the vector
# retriever. It runs locally via HuggingFace (downloaded on first run).

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")


# -- 2. Create sample documents --------------------------------------------
# A mix of natural language descriptions and a technical error code.
# The error code document is the key test case: vector search will
# struggle to match "ERR-77X-992" because it's a random string with
# no semantic meaning, but BM25 will match it exactly.

print("Building document store...")

dummy_documents = [
    Document(page_content="The new Macbook Pro features the M3 Max chip, delivering incredible processing power for video editing."),
    Document(page_content="To reset your password, navigate to the settings panel and click 'Security'."),
    Document(page_content="Error code ERR-77X-992: The motherboard has suffered a critical voltage failure."),
    Document(page_content="Many hardware components can fail if the voltage is too high, leading to complete system shutdown."),
]


# -- 3. Create the two retrieval engines -----------------------------------

# Engine A: Vector retriever (semantic search)
# Embeds documents and queries into vectors, then finds the closest
# matches by cosine similarity. Understands meaning but not exact strings.
print("Initializing vector retriever...")
vector_store = Chroma.from_documents(dummy_documents, embeddings)
vector_retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# Engine B: BM25 retriever (lexical/keyword search)
# Scores documents by term frequency and inverse document frequency.
# Excels at exact keyword matches but misses paraphrases and synonyms.
print("Initializing BM25 keyword retriever...")
bm25_retriever = BM25Retriever.from_documents(dummy_documents)
bm25_retriever.k = 2


# -- 4. Combine into a hybrid ensemble retriever ---------------------------
# EnsembleRetriever merges results from both engines using the specified
# weights. 0.5/0.5 gives equal importance to semantic and keyword matches.
# Adjust weights to favor one strategy (e.g., 0.7/0.3 for more semantic).

print("Fusing into hybrid retriever...")
hybrid_retriever = EnsembleRetriever(
    retrievers=[vector_retriever, bm25_retriever],
    weights=[0.5, 0.5],
)


# -- 5. Run comparison test -------------------------------------------------
# The query contains an exact error code. This is the worst case for vector
# search (random string with no semantic meaning) and the best case for
# BM25 (exact keyword match). Hybrid search should find the right document
# because BM25 compensates for vector search's weakness.

query = "What does ERR-77X-992 mean?"

print("\n" + "=" * 50)
print(f"QUERY: '{query}'")
print("=" * 50)

print("\nVector search only:")
vector_results = vector_retriever.invoke(query)
for idx, doc in enumerate(vector_results):
    print(f"  {idx + 1}. {doc.page_content}")

print("\nHybrid search (vector + BM25):")
hybrid_results = hybrid_retriever.invoke(query)
for idx, doc in enumerate(hybrid_results):
    print(f"  {idx + 1}. {doc.page_content}")
