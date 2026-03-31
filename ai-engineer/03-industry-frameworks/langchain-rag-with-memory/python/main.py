"""
LangChain RAG with Conversation Memory

Extends the basic LangChain RAG pipeline with conversation history.
The key problem: a plain RAG pipeline treats every question in isolation.
If the user asks "Who is the IT lead?" then follows up with "What is
her extension?", the retriever has no idea who "her" refers to.

The fix is a two-prompt architecture:
  1. Rephraser prompt -- rewrites follow-up questions into standalone
     queries using the chat history (e.g., "What is her extension?"
     becomes "What is Sarah Connor's extension?").
  2. QA prompt -- answers the rephrased question using only the
     retrieved document context.

Pipeline:
  User question + chat history
    -> Rephrase into standalone query
    -> Vector search (retriever)
    -> Inject retrieved chunks into QA prompt
    -> LLM generates grounded answer
    -> Append turn to chat history
"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains import create_retrieval_chain, create_history_aware_retriever


# -- Step 1: Load the document ---------------------------------------------

print("Building RAG pipeline with memory...")
loader = TextLoader("company_policy.txt")
docs = loader.load()


# -- Step 2: Split into chunks ---------------------------------------------
# RecursiveCharacterTextSplitter tries paragraph breaks first, then
# sentences, then words -- keeping related text together.

text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=50)
splits = text_splitter.split_documents(docs)
print(f"Document split into {len(splits)} chunks.")


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
# reach the vector database. Without this, a query like "What is her
# extension?" would retrieve irrelevant chunks because the retriever
# doesn't know who "her" refers to.
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
# After the rephrased question retrieves the right chunks, this prompt
# instructs the LLM to answer strictly from the retrieved context.
# MessagesPlaceholder gives the LLM awareness of the conversation tone
# and flow, even though retrieval was already handled.
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
# rephraser: it uses the LLM to rewrite the query first, then runs
# the standalone query against the vector database.

history_aware_retriever = create_history_aware_retriever(
    llm, retriever, rephrase_prompt
)

document_chain = create_stuff_documents_chain(llm, qa_prompt)

# The full chain: rephrase -> retrieve -> stuff context -> generate answer.
rag_chain = create_retrieval_chain(history_aware_retriever, document_chain)

print("Pipeline ready!\n")
print("-" * 50)
print("RAG Chat with Memory. Type 'q' to quit.")
print("-" * 50)


# -- Step 6: Interactive loop with rolling memory --------------------------
# chat_history stores the full conversation as HumanMessage/AIMessage
# objects. It is passed into each invoke() call so both the rephraser
# and QA prompt have access to prior turns.

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

        # Append this turn so the next invoke() has the full context.
        chat_history.extend([
            HumanMessage(content=user_query),
            AIMessage(content=bot_reply),
        ])

    except Exception as e:
        print(f"Error: {e}")
