from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain

print("Building LangChain RAG Pipeline...")

# --- STEP 1: LOAD ---
# TextLoader reads the source document from disk into LangChain Document objects
# Replaces the manual open().read() approach
loader = TextLoader("company_policy.txt")
docs = loader.load()

# --- STEP 2: SPLIT ---
# RecursiveCharacterTextSplitter chunks the document intelligently:
# it tries to split on paragraphs first, then sentences, then words
# to keep semantically related text together as much as possible.
# chunk_overlap ensures context isn't lost at chunk boundaries.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=50)
splits = text_splitter.split_documents(docs)
print(f"Sliced into {len(splits)} chunks.")

# --- STEP 3: EMBED AND STORE ---
# Use the same HuggingFace model (all-MiniLM-L6-v2) as the manual RAG project
# Chroma.from_documents handles embedding + persisting to disk in a single call
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./langchain_db"  # persists the vector DB between runs
)

# Wrap the vector store as a Retriever — fetches the top 2 most relevant chunks per query
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# --- STEP 4: LLM AND PROMPT ---
# Connect to the local Llama 3 model via Ollama
llm = ChatOllama(model="llama3")

# Define a prompt template with two placeholders:
# {context} — filled with the retrieved document chunks
# {input}   — filled with the user's question
prompt = ChatPromptTemplate.from_template("""
You are a strict corporate assistant. Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say "I don't know."

Context:
{context}

Question: {input}
""")

# --- STEP 5: BUILD THE CHAIN ---
# create_stuff_documents_chain "stuffs" the retrieved chunks into the {context} placeholder
document_chain = create_stuff_documents_chain(llm, prompt)

# create_retrieval_chain wires everything together:
# user question -> retriever (vector search) -> document_chain (prompt + LLM) -> answer
rag_chain = create_retrieval_chain(retriever, document_chain)

print("Pipeline ready!\n")
print("-" * 50)
print("LangChain Chat (Type 'q' to quit)")
print("-" * 50)

while True:
    user_query = input("\nYou: ")
    if user_query.lower() in ['q', 'quit', 'exit']:
        break

    print("   [LangChain is thinking...]")

    # --- STEP 6: INVOKE ---
    # A single invoke() call triggers the full pipeline:
    # retrieve -> inject context -> generate answer
    try:
        response = rag_chain.invoke({"input": user_query})

        # The response dict contains "answer" (LLM output) and "context" (retrieved chunks)
        print(f"\nLlama 3: {response['answer']}")

    except Exception as e:
        print(f"Error: {e}")
