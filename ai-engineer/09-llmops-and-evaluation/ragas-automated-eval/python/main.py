"""
RAGAS Automated Evaluation -- Python

Uses the RAGAS (Retrieval Augmented Generation Assessment) framework to
automatically evaluate RAG pipeline outputs. Instead of manually checking
whether the AI's answers are correct, RAGAS uses a "judge" LLM to score
responses on standardized metrics.

This demo evaluates a deliberately wrong answer to show how the metrics
detect hallucination:

  Question:     "Are lists mutable in Python?"
  Context:      "Python lists are dynamic arrays. They are mutable..."
  AI's answer:  "No, lists in Python are immutable."  <-- wrong
  Ground truth: "Yes, lists are mutable."

Two metrics are used:
  - Faithfulness: Does the answer agree with the provided context?
  - Answer Correctness: Does the answer match the ground truth?

Both should score low because the answer contradicts both the context
and the ground truth.
"""

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import Faithfulness, AnswerCorrectness
from openai import OpenAI
from ragas.llms import llm_factory


# -- 1. Set up the judge LLM -----------------------------------------------
# RAGAS needs an LLM to act as the "judge" that evaluates the answers.
# Here we use a local Llama 3 via Ollama's OpenAI-compatible API endpoint.
# The OpenAI client is pointed at localhost:11434 (Ollama's default port).

print("Setting up judge LLM...")

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama-local",
)

judge_llm = llm_factory("llama3", client=client)


# -- 2. Create the evaluation dataset --------------------------------------
# RAGAS expects a HuggingFace Dataset with these columns:
#   question     -- what was asked
#   contexts     -- the retrieved context chunks (list of lists)
#   answer       -- the AI's actual response (what we're evaluating)
#   ground_truth -- the correct answer (for correctness comparison)
#
# The answer here is deliberately wrong: it says lists are immutable,
# which contradicts both the context and the ground truth. This lets
# us verify that the metrics correctly detect the hallucination.

print("Preparing evaluation data...")

homework_data = {
    "question": ["Are lists mutable in Python?"],
    "contexts": [["Python lists are dynamic arrays. They are mutable, meaning elements can be added or removed."]],
    "answer": ["No, lists in Python are immutable data structures."],
    "ground_truth": ["Yes, lists are mutable."],
}

dataset = Dataset.from_dict(homework_data)


# -- 3. Run evaluation ------------------------------------------------------
# evaluate() sends each row to the judge LLM, which scores the answer
# against the context (Faithfulness) and ground truth (AnswerCorrectness).
# This may take a minute as the judge processes each metric.

print("Evaluating (this may take a minute)...\n")

results = evaluate(
    dataset=dataset,
    metrics=[Faithfulness(), AnswerCorrectness()],
    llm=judge_llm,
)

print("=" * 50)
print("Evaluation results:")
print("=" * 50)
print(results)
