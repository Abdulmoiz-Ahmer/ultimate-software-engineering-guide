"""
LangChain RAG Pipeline

Rebuilds the manual RAG pipeline from module 02 using LangChain
abstractions. LangChain replaces the hand-written load/chunk/embed/
retrieve/generate steps with composable components that wire together
into a single callable chain.

Pipeline:
  Load (TextLoader)
    -> Split (RecursiveCharacterTextSplitter)
    -> Embed & Store (HuggingFace + Chroma)
    -> Retrieve (as_retriever)
    -> Generate (ChatOllama + prompt template)

A single rag_chain.invoke() call triggers the full pipeline:
  user question -> vector search -> context injection -> LLM answer
"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain


# -- Step 1: Load the document ---------------------------------------------
# TextLoader reads a file from disk and returns LangChain Document objects.
# This replaces the manual open().read() approach and integrates with the
# rest of the LangChain pipeline.

print("Building RAG pipeline...")
loader = TextLoader("company_policy.txt")
docs = loader.load()


# -- Step 2: Split into chunks ---------------------------------------------
# RecursiveCharacterTextSplitter tries to split on paragraph breaks first,
# then sentence boundaries, then words -- keeping semantically related text
# together. chunk_overlap ensures context isn't lost at boundaries.

text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=50)
splits = text_splitter.split_documents(docs)
print(f"Document split into {len(splits)} chunks.")


# -- Step 3: Embed and store in ChromaDB -----------------------------------
# HuggingFaceEmbeddings uses the same all-MiniLM-L6-v2 model from module 02.
# Chroma.from_documents handles embedding and persisting in a single call.

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./langchain_db",
)

# as_retriever wraps the vector store with a search interface.
# k=2 means each query returns the top 2 most relevant chunks.
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


# -- Step 4: Configure the LLM and prompt template -------------------------
# The prompt has two placeholders:
#   {context} -- filled automatically with retrieved chunks
#   {input}   -- filled with the user's question

llm = ChatOllama(model="llama3")

prompt = ChatPromptTemplate.from_template(
    "You are a strict corporate assistant. Answer the user's question "
    "using ONLY the context provided below.\n"
    "If the answer is not in the context, say \"I don't know.\"\n\n"
    "Context:\n{context}\n\n"
    "Question: {input}"
)


# -- Step 5: Build the chain -----------------------------------------------
# create_stuff_documents_chain "stuffs" retrieved chunks into the {context}
# placeholder and passes the result to the LLM.
# create_retrieval_chain wires the retriever and document chain together
# so a single invoke() runs the full pipeline.

document_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, document_chain)

print("Pipeline ready!\n")
print("-" * 50)
print("LangChain RAG Chat. Type 'q' to quit.")
print("-" * 50)


# -- Step 6: Interactive loop -----------------------------------------------
# Each invoke() call triggers: retrieve -> inject context -> generate answer.
# The response dict contains "answer" (LLM output) and "context" (retrieved chunks).

while True:
    user_query = input("\nYou: ")
    if user_query.lower() in ("q", "quit", "exit"):
        break

    print("   [Retrieving and generating...]")

    try:
        response = rag_chain.invoke({"input": user_query})
        print(f"\nBot: {response['answer']}")
    except Exception as e:
        print(f"Error: {e}")
