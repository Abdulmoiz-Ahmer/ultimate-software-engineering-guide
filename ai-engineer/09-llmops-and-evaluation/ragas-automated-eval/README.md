# RAGAS Automated Evaluation

Uses the **RAGAS** (Retrieval Augmented Generation Assessment) framework to automatically evaluate RAG pipeline outputs. Instead of manually reviewing answers, a "judge" LLM scores responses on standardized metrics.

## The problem

A RAG pipeline can produce answers that look plausible but are actually wrong -- hallucinated, contradicting the retrieved context, or factually incorrect. Manually checking every answer doesn't scale.

## How RAGAS solves it

```
Evaluation dataset:
  - question
  - contexts (retrieved chunks)
  - answer (AI's response)
  - ground_truth (correct answer)
        |
        v
RAGAS evaluate() with judge LLM
        |
        v
Scores per metric:
  - Faithfulness: 0.0 - 1.0
  - Answer Correctness: 0.0 - 1.0
```

RAGAS sends each evaluation row to a judge LLM that scores the answer against the context and ground truth. The scores are standardized (0.0 to 1.0), making it easy to track quality over time or compare pipeline changes.

## Metrics used

| Metric | What it measures | Inputs |
|---|---|---|
| **Faithfulness** | Does the answer agree with the retrieved context? Catches hallucinations where the model ignores or contradicts the context. | answer + contexts |
| **Answer Correctness** | Does the answer match the ground truth? Catches factual errors regardless of context. | answer + ground_truth |

## The test case

The demo uses a deliberately wrong answer to verify the metrics work:

- **Question:** "Are lists mutable in Python?"
- **Context:** "Python lists are dynamic arrays. They are mutable..."
- **AI's answer:** "No, lists in Python are immutable." (wrong)
- **Ground truth:** "Yes, lists are mutable."

Both metrics should score low because the answer contradicts both the context and the ground truth.

## Key concepts

- **LLM-as-judge** -- using an LLM to evaluate another LLM's output. The judge reads the question, context, answer, and ground truth, then assigns a score based on well-defined criteria.
- **Faithfulness** -- measures whether the answer is supported by the retrieved context. A low score means the model hallucinated or contradicted its sources.
- **Answer Correctness** -- measures factual accuracy against a known correct answer. Useful when you have labeled test data.
- **Why this matters** -- automated evaluation lets you run regression tests on RAG pipelines, catch quality degradation after changes, and compare different retrieval strategies quantitatively.

## Prerequisites

- [Ollama](https://ollama.com/) running locally with `llama3` pulled
- No API keys needed -- the judge LLM runs locally

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
