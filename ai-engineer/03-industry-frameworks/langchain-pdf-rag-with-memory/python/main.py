"""
LangChain PDF RAG with Conversation Memory

Extends the text-based RAG pipeline with PDF support. The only
structural change is swapping TextLoader for PyPDFLoader, which
extracts text page by page from a PDF file. Everything else --
chunking, embedding, history-aware retrieval, rolling memory --
is identical to the text-based version.

This demonstrates that LangChain's loader abstraction makes it
trivial to switch document formats: swap one loader, keep the
entire pipeline unchanged.

Pipeline:
  Load PDF (PyPDFLoader)
    -> Split pages into chunks
    -> Embed & store in ChromaDB
    -> User question + chat history
    -> Rephrase into standalone query
    -> Vector search -> context injection -> LLM answer
    -> Append turn to chat history
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever


# -- Step 1: Load the PDF --------------------------------------------------
# PyPDFLoader extracts text page by page. Each page becomes a separate
# LangChain Document object with page metadata. Unlike TextLoader, PDFs
# can fail if the file is missing, corrupt, or password-protected.

print("Building PDF RAG pipeline...")

pdf_path = "typesofpl.pdf"
try:
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"Loaded {len(docs)} pages from PDF.")
except Exception as error:
    print(f"Error loading PDF: {error}")
    print("Make sure the PDF file exists in the project folder.")
    exit()


# -- Step 2: Split into chunks ---------------------------------------------
# RecursiveCharacterTextSplitter tries paragraph breaks first, then
# sentences, then words -- keeping related text together.

text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=50)
splits = text_splitter.split_documents(docs)
print(f"Split into {len(splits)} chunks.")


# -- Step 3: Embed and store in ChromaDB -----------------------------------

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./langchain_db",
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


# -- Step 4: Define the two prompts ----------------------------------------

llm = ChatOllama(model="llama3")

# Prompt A: Rephraser
# Rewrites follow-up questions into self-contained queries before they
# reach the vector database. Without this, a query like "Tell me more
# about that" would retrieve irrelevant chunks.
rephrase_system_prompt = (
    "Given a chat history and the latest user question which might "
    "reference context in the chat history, formulate a standalone "
    "question which can be understood without the chat history. "
    "Do NOT answer the question, just reformulate it if needed and "
    "otherwise return it as is."
)

rephrase_prompt = ChatPromptTemplate.from_messages([
    ("system", rephrase_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

# Prompt B: QA (final answer)
# Answers the rephrased question using only the retrieved context.
qa_system_prompt = (
    "You are a strict corporate assistant. Answer the user's question "
    "using ONLY the context provided below.\n"
    "If the answer is not in the context, say \"I don't know.\"\n\n"
    "Context:\n{context}"
)

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", qa_system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])


# -- Step 5: Build the chain -----------------------------------------------
# create_history_aware_retriever wraps the base retriever with the
# rephraser: rewrite the query first, then search the vector database.

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, rephrase_prompt
)

document_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(history_aware_retriever, document_chain)

print("Pipeline ready!\n")
print("-" * 50)
print("PDF RAG Chat with Memory. Type 'q' to quit.")
print("-" * 50)


# -- Step 6: Interactive loop with rolling memory --------------------------
# chat_history stores the full conversation as HumanMessage/AIMessage
# objects, passed into each invoke() call.

chat_history = []

while True:
    user_query = input("\nYou: ")
    if user_query.lower() in ("q", "quit", "exit"):
        break

    print("   [Rephrasing, retrieving, generating...]")

    try:
        response = rag_chain.invoke({
            "input": user_query,
            "chat_history": chat_history,
        })

        bot_reply = response["answer"]
        print(f"\nBot: {bot_reply}")

        chat_history.extend([
            HumanMessage(content=user_query),
            AIMessage(content=bot_reply),
        ])

    except Exception as e:
        print(f"Error: {e}")
