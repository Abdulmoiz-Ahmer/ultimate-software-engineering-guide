# LangChain RAG with Conversation Memory -- Python

Python implementation using LangChain's `create_history_aware_retriever` and `MessagesPlaceholder` for conversation memory.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure Ollama is running and you have Llama 3 pulled:

```bash
ollama pull llama3
```

## Run

```bash
python main.py
```

Try a multi-turn conversation:
- `Who is the IT lead?`
- `What is her extension?` (resolved using chat history)
- `When is the cafeteria open?`

Type `q` to quit.

## Customization

Replace `company_policy.txt` with any text file. Adjust `chunk_size`, `chunk_overlap`, and `k` to tune retrieval quality.

## Dependencies

Same as the base LangChain RAG pipeline, plus:
- `langchain-core` -- `MessagesPlaceholder`, `HumanMessage`, `AIMessage` for history injection
- `langchain-classic` -- `create_history_aware_retriever` for the rephrase-then-retrieve pattern
