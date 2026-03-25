from sentence_transformers import SentenceTransformer, util

# Load the pre-trained embedding model (downloads on first run)
print("Loading model (all-MiniLM-L6-v2)... (Downloading if first time)")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Sample sentences to compare — the first one is our target
sentences = [
    "Batman is a fictional character.",
    "Batman is a witty character.",
    "Pineapple pizza is a controversial topic.",
    "Green arrow movie is coming out soon.",
    "The cat is on the roof.",
    "Have you ever tried ice tea?"
]

# Convert all sentences into numerical vectors (embeddings)
# Sentences with similar meaning will have vectors pointing in similar directions
print("\nConverting sentences to vectors (embeddings)...")
embeddings = model.encode(sentences)

print("-" * 50)
print("Semantic Similarity Results")
print("-" * 50)

# Use the first sentence as the target to compare against all others
target_index = 0
target_sentence = sentences[target_index]
target_embedding = embeddings[target_index]

print(f"Target: '{target_sentence}'\n")

# Compare the target embedding against each other sentence's embedding
# using cosine similarity (1.0 = identical meaning, 0.0 = unrelated)
for i in range(1, len(sentences)):
    compare_sentence = sentences[i]
    compare_embedding = embeddings[i]
    similarity_score = util.cos_sim(target_embedding, compare_embedding).item()
    print(f"Comparing to: '{compare_sentence}'")
    print(f"Similarity Score': {similarity_score * 100:.2f}%\n")
