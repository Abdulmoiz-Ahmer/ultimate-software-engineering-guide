"""
Query Transform with HyDE (Hypothetical Document Embeddings)

Standard vector search fails on vague or short queries like "code collision"
because the query's embedding lands far from the relevant document's embedding.

HyDE fixes this in two steps:
  1. Ask the LLM to generate a hypothetical answer to the query -- a fake but
     detailed document full of relevant vocabulary.
  2. Embed that hypothetical document (not the original query) and search the
     vector database with it.

The hypothetical document's embedding is much closer to the real document's
embedding than the short query's embedding ever would be, because they share
similar technical language and structure.
"""

import logging
from langchain_ollama import ChatOllama
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# Suppress noisy HTTP logs from the Ollama client
logging.getLogger("httpx").setLevel(logging.WARNING)

print("Initializing HyDE pipeline...")


# -- LLM and Embeddings ------------------------------------------------------
# The LLM generates the hypothetical document. Temperature 0.7 gives enough
# creativity to produce rich, varied vocabulary in the fake answer.
# BGE-small is the embedding model -- it converts both the hypothetical
# document and the stored documents into comparable vectors.

llm = ChatOllama(model="llama3", temperature=0.7)
embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5")


# -- Vector Database ----------------------------------------------------------
# A small in-memory ChromaDB with 3 technical documents. In production this
# would be a large persistent knowledge base.

print("Building in-memory vector database...")

documents = [
    Document(page_content="To resolve a git merge conflict, open the file, look for the <<<<<<< HEAD markers, manually edit the code to keep the desired changes, remove the markers, and then run git add and git commit."),
    Document(page_content="If your Python script throws a KeyError, it means you tried to access a dictionary key that does not exist in the current mapping."),
    Document(page_content="Docker containers share the host machine's OS kernel and therefore do not require an OS per application, making them very lightweight."),
]

db = Chroma.from_documents(documents, embeddings)


# -- The Problem --------------------------------------------------------------
# A vague query like "code collision" is semantically far from the actual
# document about git merge conflicts. A standard similarity search would
# likely miss it or rank it poorly.

user_query = "code collision"

print()
print("=" * 50)
print(f"User query: '{user_query}'")
print("=" * 50)


# -- HyDE Step 1: Generate a hypothetical document ---------------------------
# Ask the LLM to write a detailed technical answer to the query. The LLM
# will "hallucinate" content -- and that's the point. We don't need the
# content to be factually correct. We need it to contain the right vocabulary
# (e.g., "merge", "conflict", "git") so its embedding lands near the real
# document's embedding.

print("\nStep 1: Generating hypothetical document...")

hyde_prompt = f"""
Please write a short, detailed, and highly technical paragraph answering this search query.
Do not apologize or say you don't have enough info. Just write a hypothetical technical answer.
Query: {user_query}
"""

hypothetical_document = llm.invoke(hyde_prompt).content

print("\nHypothetical document generated:")
print("-" * 50)
print(hypothetical_document)
print("-" * 50)


# -- HyDE Step 2: Search using the hypothetical document ---------------------
# Instead of embedding the vague 2-word query, we embed the rich hypothetical
# document and use that embedding to search the vector database. The
# hypothetical document's embedding is much closer to the real git merge
# conflict document than "code collision" would ever be.

print("\nStep 2: Searching vector database with hypothetical document...")

results = db.similarity_search(hypothetical_document, k=1)

print("\nRetrieved document:")
print("=" * 50)
print(results[0].page_content)
print("=" * 50)
