# LangGraph Stateful Agent

A **graph-based agent loop** where a Writer and a Critic operate as nodes in a state graph. The Writer drafts a story, the Critic reviews it against acceptance criteria, and the graph conditionally loops back for revision or terminates. Built with [LangGraph](https://github.com/langchain-ai/langgraph).

## The problem this solves

CrewAI (used in the previous projects) manages agent coordination at a high level -- you define agents and tasks, and the framework decides the flow. But sometimes you need **explicit control** over the loop: which node runs next, what state is passed, when to stop, and under what conditions to retry.

LangGraph gives you that control by modeling the workflow as a directed graph with shared state, deterministic edges, and conditional branching.

## How it works

```
                   +--------+
                   | Writer |  <-- reads feedback, writes a draft
                   +--------+
                       |
                       v
                   +--------+
                   | Critic |  <-- reviews draft against criteria
                   +--------+
                       |
               (conditional edge)
              /                  \
     draft rejected           draft approved
     or under 3 iters         or 3 iters reached
          |                        |
          v                        v
     loop back                    END
     to Writer
```

### The loop in detail

1. **Writer node** reads feedback from the shared state and drafts a story.
2. **Critic node** checks if the draft meets the criteria (must mention an animal).
3. **Conditional edge** decides: if approved or max iterations reached, go to END. Otherwise, loop back to the Writer with rejection feedback.
4. The Writer incorporates the feedback and tries again.

## Key concepts

- **StateGraph** -- a directed graph where each node is a function that reads from and writes to a shared `TypedDict` state. LangGraph merges each node's return value into the state automatically.
- **Nodes** -- plain functions with the signature `(state) -> partial_state`. Each node receives the full state and returns only the fields it wants to update.
- **Edges** -- define the flow between nodes. Fixed edges (`add_edge`) always go to the same next node. Conditional edges (`add_conditional_edges`) call a routing function that returns the name of the next node or `END`.
- **Conditional routing** -- the `should_continue` function inspects the current state and returns either `"writer"` (loop back) or `END` (terminate). This is how the retry loop is controlled.
- **Shared state** -- all nodes read from and write to the same `AgentState` dict. The state accumulates across iterations -- the Writer sees the Critic's feedback, the Critic sees the Writer's latest draft.
- **Max iterations** -- a safety valve (3 iterations) prevents infinite loops if the LLM never produces an acceptable draft.

## CrewAI vs. LangGraph

| | CrewAI | LangGraph |
|---|---|---|
| Abstraction | High-level (agents, tasks, crews) | Low-level (nodes, edges, state) |
| Flow control | Framework-managed (sequential/hierarchical) | Developer-defined graph |
| State | Implicit (passed between tasks) | Explicit shared TypedDict |
| Looping | Implicit (Manager decides in hierarchical) | Explicit conditional edges |
| Best for | Multi-agent teams with roles | Custom workflows needing precise control |

## Prerequisites

- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
