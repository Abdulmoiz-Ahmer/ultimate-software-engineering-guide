from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever

print("Building LangChain RAG Pipeline...")

# --- STEP 1: LOAD ---
# PyPDFLoader reads a PDF from disk, extracting text page by page.
# Each page becomes a separate LangChain Document object.
# Unlike TextLoader, PDFs can fail if the file is missing, corrupt, or password-protected,
# so we wrap the load in a try/except and exit early with a helpful message.
pdf_path = "typesofpl.pdf"
try:
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"Successfully loaded {len(docs)} pages from the PDF.")
except Exception as error:
    print(f"Error loading PDF: {error}")
    print("Did you put a real PDF file in the folder and name it correctly?")
    exit()
    
# --- STEP 2: SPLIT ---
# RecursiveCharacterTextSplitter chunks the document intelligently:
# it tries to split on paragraphs first, then sentences, then words
# to keep semantically related text together as much as possible.
# chunk_overlap ensures context isn't lost at chunk boundaries.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=50)
splits = text_splitter.split_documents(docs)
print(f"Sliced into {len(splits)} chunks.")

# --- STEP 3: EMBED AND STORE ---
# Use the HuggingFace model (all-MiniLM-L6-v2) for local, offline embeddings
# Chroma.from_documents handles embedding + persisting to disk in a single call
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./langchain_db"  # persists the vector DB between runs
)

# Wrap the vector store as a Retriever — fetches the top 2 most relevant chunks per query
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# --- STEP 4: LLM AND PROMPTS ---
# Connect to the local Llama 3 model via Ollama
llm = ChatOllama(model="llama3")

# Prompt A: The Rephraser
# When a user asks a follow-up like "what about his salary?", the retriever
# won't know who "his" refers to without the history. This prompt instructs
# the LLM to rewrite the question as a self-contained, standalone query
# before it hits the vector database.
rephrase_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

rephrase_prompt = ChatPromptTemplate.from_messages([
    ("system", rephrase_system_prompt),
    MessagesPlaceholder("chat_history"),  # injects the full conversation history
    ("human", "{input}")
])

# Prompt B: The Final Answer
# After the rephrased question retrieves the right chunks, this prompt
# instructs the LLM to answer strictly from the retrieved context.
qa_system_prompt = """You are a strict corporate assistant. Answer the user's question using ONLY the context provided below.
If the answer is not in the context, say "I don't know."

Context:
{context}"""

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),  # gives the LLM awareness of what was said before
    ("human", "{input}"),
])

# --- STEP 5: BUILD THE CHAIN ---
# history_aware_retriever wraps the base retriever with the rephraser prompt:
# it uses the LLM to turn the follow-up question into a standalone query first,
# then runs that query against the vector database
history_aware_retriever = create_history_aware_retriever(
    llm,
    retriever,
    rephrase_prompt
)

# create_stuff_documents_chain "stuffs" the retrieved chunks into the {context} placeholder
document_chain = create_stuff_documents_chain(llm, qa_prompt)

# create_retrieval_chain wires the full pipeline together:
# user question -> history_aware_retriever (rephrase + vector search) -> document_chain (prompt + LLM) -> answer
rag_chain = create_retrieval_chain(history_aware_retriever, document_chain)

print("Pipeline ready!\n")
print("-" * 50)
print("LangChain Chat (Type 'q' to quit)")
print("-" * 50)

# Rolling memory — stores the full conversation as LangChain message objects.
# Passed into invoke() each turn so the chain has access to prior context.
chat_history = []

while True:
    user_query = input("\nYou: ")
    if user_query.lower() in ['q', 'quit', 'exit']:
        break

    print("   [LangChain is thinking...]")

    # --- STEP 6: INVOKE ---
    # invoke() runs the full pipeline: rephrase -> retrieve -> inject context -> generate
    # chat_history is passed so the rephraser and QA prompt are both history-aware
    try:
        response = rag_chain.invoke({
            "input": user_query,
            "chat_history": chat_history
        })

        bot_reply = response["answer"]
        print(f"\nLlama 3: {bot_reply}")

        # Append this turn to history so the next invoke() has the full context
        chat_history.extend([
            HumanMessage(content=user_query),
            AIMessage(content=bot_reply)
        ])

    except Exception as e:
        print(f"Error: {e}")
