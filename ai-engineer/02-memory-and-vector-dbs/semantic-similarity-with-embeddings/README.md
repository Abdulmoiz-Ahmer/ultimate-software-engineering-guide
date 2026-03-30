# Semantic Similarity with Embeddings

Demonstrates how **text embeddings** and **cosine similarity** work -- the foundational concepts behind vector databases and RAG. Sentences are converted into numerical vectors and compared to measure how close they are in meaning.

## What it does

1. Loads a pre-trained sentence embedding model (`all-MiniLM-L6-v2`).
2. Encodes a list of sentences into 384-dimensional vectors.
3. Compares a target sentence against all others using cosine similarity.
4. Prints a similarity score for each pair (0% = unrelated, 100% = identical meaning).

## Example output

```
Target: 'Batman is a fictional character.'

  vs 'Batman is a witty character.'
  Similarity: 82.35%

  vs 'Pineapple pizza is a controversial topic.'
  Similarity: 12.47%

  vs 'Have you ever tried ice tea?'
  Similarity: 5.21%
```

## Key concepts

- **Text embeddings** -- a pre-trained model converts sentences into fixed-size numerical vectors. Sentences with similar meaning get vectors that point in similar directions.
- **Cosine similarity** -- measures the angle between two vectors. 1.0 = same direction (identical meaning), 0.0 = perpendicular (unrelated). Two sentences can score high even with no shared words.
- **`SentenceTransformer`** -- the `sentence-transformers` library provides pre-trained models optimized for embedding sentences. `all-MiniLM-L6-v2` is lightweight and general-purpose.
- **Why this matters** -- vector search (used in RAG and vector databases) relies on this exact process: encode a query, then find the stored embeddings closest to it.

## Prerequisites

- Python 3.10+
- No API keys needed -- the model runs locally (downloaded on first run)

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```
