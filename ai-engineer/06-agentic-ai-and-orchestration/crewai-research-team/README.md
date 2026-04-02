# CrewAI Research Team

A **multi-agent system** where two specialized AI agents collaborate in sequence: a **Researcher** searches the web for facts, then a **Writer** turns those facts into a polished blog post. Orchestrated by [CrewAI](https://www.crewai.com/).

## The problem this solves

A single LLM prompt that tries to "research and write an article" often hallucinates facts or produces shallow content. By splitting the work across two agents with distinct roles and constraints, each agent focuses on what it does best -- and the writer is explicitly forbidden from making up facts.

## How it works

```
Topic
  |
  v
Researcher agent (has web search tool)
  -> searches DuckDuckGo for facts, numbers, links
  -> outputs a raw bulleted list
  |
  v
Writer agent (no tools, text only)
  -> receives the researcher's raw findings
  -> writes a 3-paragraph Markdown blog post
  |
  v
Final blog post
```

## Key concepts

- **Multi-agent orchestration** -- instead of one prompt doing everything, the work is split across agents with distinct roles, tools, and constraints. CrewAI manages the handoff between them.
- **Sequential process** -- `Process.sequential` runs tasks in order. Each task's output is automatically passed to the next task as context.
- **Agent specialization** -- the researcher has a web search tool but doesn't write; the writer has no tools but excels at turning raw data into readable text. Neither agent can delegate to the other.
- **Tool binding** -- tools are defined with the `@tool` decorator and assigned to specific agents. Only agents with the tool can use it.
- **Backstory as persona** -- each agent's `backstory` field shapes its behavior and reasoning style, acting like a system instruction.

## Prerequisites

- [Ollama](https://ollama.com/) running locally with `llama3.1` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
