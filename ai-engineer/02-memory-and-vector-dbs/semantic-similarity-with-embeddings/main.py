"""
Semantic Similarity with Embeddings

Demonstrates how text embeddings and cosine similarity work. Sentences
are converted into numerical vectors (embeddings) using a pre-trained
transformer model, then compared using cosine similarity to measure
how close they are in meaning.

This is the foundational concept behind vector databases and RAG:
  1. Encode text into a fixed-size vector.
  2. Compare vectors to find semantically related content.

Cosine similarity ranges from 0.0 (completely unrelated) to 1.0
(identical meaning). Two sentences can score high even if they share
no words, as long as their meanings are close.
"""

from sentence_transformers import SentenceTransformer, util


# -- 1. Load the embedding model -------------------------------------------
# all-MiniLM-L6-v2 is a lightweight, general-purpose sentence embedding
# model. It maps any sentence to a 384-dimensional vector. The model is
# downloaded automatically on first run and cached locally.

print("Loading model (all-MiniLM-L6-v2)...")
model = SentenceTransformer("all-MiniLM-L6-v2")


# -- 2. Define sample sentences -------------------------------------------
# The first sentence is the target. The rest are compared against it.
# Notice the mix: some are semantically close to the target, others are
# completely unrelated -- this makes the similarity scores more interesting.

sentences = [
    "Batman is a fictional character.",
    "Batman is a witty character.",
    "Pineapple pizza is a controversial topic.",
    "Green arrow movie is coming out soon.",
    "The cat is on the roof.",
    "Have you ever tried ice tea?",
]


# -- 3. Encode sentences into embeddings ----------------------------------
# model.encode converts each sentence into a numerical vector. Sentences
# with similar meaning will have vectors pointing in similar directions
# in the 384-dimensional space.

print("Converting sentences to vectors (embeddings)...\n")
embeddings = model.encode(sentences)


# -- 4. Compare using cosine similarity -----------------------------------
# Cosine similarity measures the angle between two vectors. A score of
# 1.0 means the vectors point in the same direction (identical meaning),
# 0.0 means they are perpendicular (unrelated).

target_sentence = sentences[0]
target_embedding = embeddings[0]

print("-" * 50)
print(f"Target: '{target_sentence}'\n")

for i in range(1, len(sentences)):
    score = util.cos_sim(target_embedding, embeddings[i]).item()
    print(f"  vs '{sentences[i]}'")
    print(f"  Similarity: {score * 100:.2f}%\n")
