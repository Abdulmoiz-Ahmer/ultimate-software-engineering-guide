# AI Engineer -- Learning Path

A hands-on, project-based curriculum for learning AI engineering from the ground up. 11 modules, 30+ projects, progressing from basic LLM API calls to deploying a full-stack AI application.

## Modules

### [01 -- Foundations and Prompting](01-foundations-and-prompting/)

Making API calls, prompt engineering, system instructions, safety guardrails, and running models locally.

4 projects: Gemini chatbot, tone rewriter, content safety guardrail, local Ollama rewriter

---

### [02 -- Memory and Vector Databases](02-memory-and-vector-dbs/)

Text embeddings, cosine similarity, vector databases, and building a full RAG pipeline from scratch.

3 projects: Semantic similarity, ChromaDB vector search, RAG document Q&A

---

### [03 -- Industry Frameworks](03-industry-frameworks/)

Rebuilding the RAG pipeline with LangChain and LlamaIndex -- adding conversation memory, PDF support, and comparing framework philosophies.

4 projects: LangChain RAG, RAG with memory, PDF RAG, LlamaIndex PDF RAG

---

### [04 -- Agents and Tools](04-agents-and-tools/)

LLMs calling external tools and acting autonomously -- from manual tool-calling loops to LangChain agent executors and data analysis agents.

3 projects: Manual tool-calling agent, web search agent, CSV data analyst agent

---

### [05 -- Multimodal AI](05-multimodal-ai/)

Working with inputs beyond text -- images and audio -- by chaining specialized models with general-purpose LLMs.

2 projects: Vision model image analysis, speech-to-summary

---

### [06 -- Agentic AI and Orchestration](06-agentic-ai-and-orchestration/)

Multi-agent systems with CrewAI (sequential and hierarchical) and custom graph-based agent loops with LangGraph.

3 projects: CrewAI research team, hierarchical multi-agent, LangGraph stateful agent

---

### [07 -- Advanced RAG](07-advanced-rag/)

Techniques that improve retrieval quality beyond basic vector search -- query transformation, hybrid search, and reranking.

3 projects: HyDE query transform, hybrid search pipeline, Cohere reranking

---

### [08 -- Model Finetuning](08-model-finetuning/)

Customizing a language model's behavior by preparing training data and fine-tuning with LoRA adapters.

2 projects: HuggingFace dataset prep, QLoRA instruction tuning

---

### [09 -- LLMOps and Evaluation](09-llmops-and-evaluation/)

Observability with LangSmith tracing and automated RAG evaluation with RAGAS.

2 projects: LangSmith tracing, RAGAS automated evaluation

---

### [10 -- MCP and Tool Infrastructure](10-mcp-and-tool-infrastructure/)

Building custom MCP servers that expose tools, and connecting them to LLM agents via the Model Context Protocol.

2 projects: Custom MCP server, MCP client connection

---

### [11 -- UI and Deployment](11-ui-and-deployment/)

Serving an LLM through a REST API with FastAPI and building a browser-based chat UI with Streamlit.

2 projects: FastAPI LLM service, Streamlit chatbot UI

## Project structure

Each project folder contains a language-agnostic README explaining the concept, with implementation-specific code and instructions inside language subfolders:

```
module-name/
  README.md              # Module overview and learning path
  project-name/
    README.md            # What it does, key concepts (language-agnostic)
    python/
      main.py
      requirements.txt
      README.md          # Python-specific setup and usage
    # js/                # (coming soon)
```

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3` pulled (most projects)
- A Gemini API key for module 01 projects 1-3 (get one from [Google AI Studio](https://aistudio.google.com/))
- A [Tavily](https://tavily.com/) API key (module 04, projects 2-3)
- A [Cohere](https://cohere.com/) API key (module 07, project 3)
- A GPU is recommended for module 08 (LoRA fine-tuning)
- A [LangSmith](https://smith.langchain.com/) API key (module 09, project 1, free tier available)
