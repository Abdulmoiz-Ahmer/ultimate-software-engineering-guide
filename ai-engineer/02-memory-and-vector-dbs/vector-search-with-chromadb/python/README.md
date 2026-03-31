# Vector Search with ChromaDB -- Python

Python implementation using the `chromadb` package.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

Type any concept or phrase to search. Results show the top 3 matches with distance scores. Type `q` to quit.

## Dependencies

- `chromadb` -- vector database with built-in embedding. `PersistentClient` saves to disk; `collection.add()` auto-embeds; `collection.query()` finds nearest neighbors
