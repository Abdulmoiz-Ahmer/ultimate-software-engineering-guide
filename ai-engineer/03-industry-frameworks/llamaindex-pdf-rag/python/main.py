"""
LlamaIndex PDF RAG

A RAG pipeline built with LlamaIndex instead of LangChain. Loads a PDF,
builds an in-memory vector index, and answers questions grounded in the
document content.

LlamaIndex takes a more declarative approach than LangChain:
  - Settings.llm and Settings.embed_model configure the models globally.
  - SimpleDirectoryReader handles document loading with format-specific
    extractors (PyMuPDFReader for PDFs).
  - VectorStoreIndex.from_documents builds the index in a single call
    (chunking, embedding, and storage all happen internally).
  - as_query_engine() returns a ready-to-use query interface that
    handles retrieval and generation behind the scenes.

The entire RAG pipeline (load -> chunk -> embed -> retrieve -> generate)
is set up in under 10 lines of code.
"""

from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.readers.file import PyMuPDFReader


# -- 1. Configure models globally ------------------------------------------
# LlamaIndex uses a global Settings object. Any component that needs an
# LLM or embedding model will use these defaults automatically.
#
# Ollama: local Llama 3 with a long timeout for slower hardware.
# HuggingFaceEmbedding: BGE-small is a compact, high-quality embedding
# model optimized for retrieval tasks.

print("Configuring models...")

Settings.llm = Ollama(model="llama3", request_timeout=1200.0)
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")


# -- 2. Load the PDF -------------------------------------------------------
# SimpleDirectoryReader accepts a list of files and a dict mapping file
# extensions to specific reader classes. PyMuPDFReader extracts text from
# PDFs using the PyMuPDF library, which handles complex layouts better
# than basic text extraction.

print("Loading PDF...")

extractor = {".pdf": PyMuPDFReader()}
documents = SimpleDirectoryReader(
    input_files=["typesofpl.pdf"],
    file_extractor=extractor,
).load_data()

print(f"Loaded {len(documents)} document chunks.")


# -- 3. Build the vector index ---------------------------------------------
# VectorStoreIndex.from_documents handles chunking, embedding, and
# in-memory storage in a single call. This is the key difference from
# LangChain, where each step is an explicit, separate operation.

print("Building vector index...")
index = VectorStoreIndex.from_documents(documents)


# -- 4. Query engine -------------------------------------------------------
# as_query_engine() wraps the index with a retrieval + generation pipeline.
# When you call query(), it retrieves the most relevant chunks, injects
# them into a prompt, and generates an answer -- all in one call.

query_engine = index.as_query_engine()

print("RAG pipeline ready!\n")
print("-" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() in ("q", "e", "quit", "exit"):
        break

    print("   [Searching and generating...]")
    try:
        response = query_engine.query(user_input)
        print(f"\nBot: {response}")
    except Exception as error:
        print(f"Error: {error}")
