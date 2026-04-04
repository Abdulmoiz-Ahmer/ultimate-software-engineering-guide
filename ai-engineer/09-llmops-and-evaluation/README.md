# 09 -- LLMOps and Evaluation

This module covers the operational side of LLM applications -- how to observe what your pipeline is doing and how to measure whether it's doing it well. The first project adds tracing so you can inspect every step, and the second project adds automated evaluation so you can score output quality without manual review.

## Project structure

Each project folder contains a language-agnostic README explaining the concept, with implementation-specific code and instructions inside language subfolders:

```
project-name/
  README.md          # What it does, key concepts, prerequisites
  python/            # Python implementation + setup instructions
    main.py
    requirements.txt
    README.md
  # js/              # (coming soon)
```

## Learning path

### 1. [LangSmith Tracing](langsmith-tracing/)

Adds observability to a LangChain pipeline using LangSmith. Every LLM call, prompt, and output is automatically traced and sent to a web dashboard for inspection -- with zero code changes. Tracing is enabled entirely through environment variables.

**You learn:** How to add observability to LLM pipelines, what traces capture (prompts, responses, latency, tokens), and why debugging without tracing is guessing.

**Key concepts:** LangSmith tracing, zero-code instrumentation, environment variable configuration, trace projects, LCEL chains

---

### 2. [RAGAS Automated Evaluation](ragas-automated-eval/)

Uses the RAGAS framework to automatically score RAG pipeline outputs. A judge LLM evaluates answers against retrieved context and ground truth, producing standardized metrics (faithfulness, answer correctness) on a 0-1 scale.

**You learn:** How to evaluate RAG quality automatically using LLM-as-judge, what faithfulness and correctness measure, and how to build regression tests for LLM pipelines.

**Key concepts:** RAGAS framework, LLM-as-judge, faithfulness, answer correctness, automated evaluation, regression testing

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3` pulled
- A [LangSmith](https://smith.langchain.com/) account and API key (project 1, free tier available)

Each project has its own `README.md` with concept explanations, and each language folder has setup instructions.
