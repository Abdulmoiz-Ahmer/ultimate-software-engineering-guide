"""
Cohere Reranking Pipeline -- Python

Demonstrates how reranking improves retrieval quality. The base vector
retriever returns K documents by embedding similarity, then Cohere's
reranking model rescores them with a more powerful cross-encoder and
returns only the top N most relevant.

The pipeline:
  1. Vector search returns 4 candidates (fast but approximate ranking).
  2. Cohere reranker rescores all 4 against the original query.
  3. Only the top 2 are returned, in the correct relevance order.

The test query ("How do I reset my router?") is deliberately ambiguous --
the document set contains results about password resets, router resets,
and networking. Vector search ranks them by embedding distance, which
often gets the order wrong. The reranker fixes this by doing a deeper,
query-aware relevance comparison.
"""

import logging

from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_cohere import CohereRerank

# Load COHERE_API_KEY from .env file. LangChain's CohereRerank picks
# it up automatically from the environment.
load_dotenv()

# Suppress noisy HTTP logs from the embedding model download.
logging.getLogger("httpx").setLevel(logging.WARNING)


# -- 1. Set up embeddings and sample documents ------------------------------
# BGE-small is used for the initial vector retrieval step. The documents
# are deliberately similar (password reset vs. router reset) to show
# where vector search gets confused and reranking helps.

embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

dummy_documents = [
    Document(page_content="To reset your account password, click the forgot password link on the login screen."),
    Document(page_content="A router is a networking device that forwards data packets between computer networks."),
    Document(page_content="To perform a hard factory reset on your Wi-Fi router, hold the small red button on the back for 30 seconds."),
    Document(page_content="If your password is not working, ensure your caps lock is disabled and try typing it again."),
]

vector_store = Chroma.from_documents(dummy_documents, embeddings)
base_retriever = vector_store.as_retriever(search_kwargs={"k": 4})


# -- 2. Set up the Cohere reranker -----------------------------------------
# CohereRerank uses Cohere's cross-encoder model to rescore documents
# against the query. Unlike vector search (which compares embeddings
# independently), the reranker reads the query and each document together,
# producing a more accurate relevance score.
#
# top_n=2 means only the 2 highest-scoring documents are returned.

cohere_rerank = CohereRerank(model="rerank-english-v3.0", top_n=2)

# ContextualCompressionRetriever wraps the base retriever with a
# "compressor" (the reranker). It first retrieves K documents, then
# passes them through the compressor to filter and reorder.
compression_retriever = ContextualCompressionRetriever(
    base_compressor=cohere_rerank,
    base_retriever=base_retriever,
)


# -- 3. Run comparison test ------------------------------------------------
# Shows base vector results (often wrong order) vs. reranked results
# (correct order with relevance scores).

query = "How do I reset my router?"

print(f"\nQUERY: '{query}'")
print("=" * 50)

print("\nBase vector search results (4 candidates):")
base_results = base_retriever.invoke(query)
for idx, doc in enumerate(base_results):
    print(f"  {idx + 1}. {doc.page_content}")

print("\nCohere reranked results (top 2):")
reranked_results = compression_retriever.invoke(query)
for idx, doc in enumerate(reranked_results):
    score = doc.metadata.get("relevance_score", "N/A")
    print(f"  {idx + 1}. (score: {score}) {doc.page_content}")
