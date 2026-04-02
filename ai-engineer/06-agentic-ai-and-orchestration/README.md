# 06 -- Agentic AI and Orchestration

This module covers multi-agent systems -- how to make LLMs collaborate, delegate, and iterate autonomously. The projects progress from a simple two-agent pipeline to a hierarchical manager-worker system to a fully custom graph-based agent loop.

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

### 1. [CrewAI Research Team](crewai-research-team/)

Two agents -- a Researcher with web search and a Writer with no tools -- collaborate in a fixed sequential pipeline. The Researcher gathers facts, then the Writer turns them into a blog post. Each agent has a single role and cannot delegate.

**You learn:** How multi-agent orchestration works with CrewAI's sequential process, tool binding, and agent specialization.

**Key concepts:** CrewAI agents, sequential process, @tool decorator, backstory as persona, DuckDuckGo search

---

### 2. [CrewAI Hierarchical Multi-Agent](crewai-multi-agent/)

Introduces a hidden Manager agent that coordinates a Developer and a QA Reviewer. Unlike the sequential pipeline, the Manager decides who works on what, reviews output, and sends work back for revision -- creating an iterative feedback loop at runtime.

**You learn:** How hierarchical orchestration enables dynamic task assignment and iterative refinement without hardcoded task order.

**Key concepts:** Hierarchical process, implicit Manager agent, unassigned tasks, manager LLM (tool-calling), iterative review loop

---

### 3. [LangGraph Stateful Agent](langgraph-stateful-agent/)

Drops down from CrewAI's high-level abstractions to LangGraph's explicit graph-based control. A Writer node and a Critic node operate in a state graph with conditional looping -- the graph retries until acceptance criteria are met or a max iteration count is reached.

**You learn:** How to model agent workflows as directed graphs with shared state, conditional edges, and explicit loop control.

**Key concepts:** StateGraph, nodes as functions, shared TypedDict state, conditional routing, fixed vs. conditional edges, termination conditions

## Progression

| Project | Framework | Flow control | Iteration |
|---|---|---|---|
| Research Team | CrewAI | Sequential (fixed order) | None |
| Hierarchical Multi-Agent | CrewAI | Hierarchical (Manager decides) | Manager-driven review loop |
| Stateful Agent | LangGraph | Graph (developer-defined) | Explicit conditional edges |

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) with `llama3` and `llama3.1` pulled
- No API keys needed -- all projects run locally

Each project has its own `README.md` with concept explanations, and each language folder has setup instructions.
