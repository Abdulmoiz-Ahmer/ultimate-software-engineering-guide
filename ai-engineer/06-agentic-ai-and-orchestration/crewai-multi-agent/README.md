# CrewAI Hierarchical Multi-Agent

A **hierarchical multi-agent system** where a hidden Manager agent autonomously coordinates a Developer and a QA Reviewer to produce bug-free code. Built with [CrewAI](https://www.crewai.com/).

## The problem this solves

The [crewai-research-team](../crewai-research-team/) project used a **sequential** pipeline -- task 1 runs, then task 2 runs, in a fixed order. That works for linear workflows, but real projects need iteration: if the QA reviewer finds bugs, the code should go back to the developer for fixing, not just proceed to the next step.

**Hierarchical mode** solves this by introducing a Manager agent that decides the workflow at runtime -- assigning tasks, reviewing output, and sending work back for revision as needed.

## How it works

```
Project task (unassigned)
  |
  v
Manager agent (implicit, created by CrewAI)
  |
  |-- assigns coding task --> Developer agent
  |                              |
  |                              v
  |                          Produces code
  |                              |
  |-- sends code for review --> QA Reviewer agent
  |                              |
  |                              v
  |                          Finds bugs / approves
  |                              |
  |-- if bugs: sends back --> Developer agent (with feedback)
  |-- if approved: returns final output
```

## Sequential vs. Hierarchical

| | Sequential (research-team) | Hierarchical (this project) |
|---|---|---|
| Task flow | Fixed order: task 1 then task 2 | Manager decides dynamically |
| Iteration | None -- each task runs once | Manager can send work back for revision |
| Task assignment | Each task assigned to a specific agent | Tasks are unassigned; Manager delegates |
| Manager agent | None | Implicit, created by CrewAI |
| LLM requirement | Any model | Manager needs tool-calling support (e.g., Llama 3.1) |

## Key concepts

- **Hierarchical process** -- `Process.hierarchical` activates an implicit Manager agent that reads task descriptions, decides which worker to assign, reviews output, and iterates until satisfied.
- **Manager LLM** -- the Manager needs a model with tool-calling support (Llama 3.1+) because it uses internal tools to delegate work to agents. Worker agents don't need this capability.
- **Unassigned tasks** -- unlike sequential mode, tasks in hierarchical mode have no `agent=` parameter. The Manager decides who works on what.
- **No cross-delegation** -- `allow_delegation=False` on workers ensures they can't pass work to each other. All coordination flows through the Manager.
- **Iterative refinement** -- the Manager can send output back to the developer with QA feedback, creating a review loop that runs until quality standards are met.

## Prerequisites

- [Ollama](https://ollama.com/) running locally with `llama3` and `llama3.1` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
