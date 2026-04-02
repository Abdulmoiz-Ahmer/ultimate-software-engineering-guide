# CrewAI Hierarchical Multi-Agent -- Python

Python implementation using the `crewai` framework in hierarchical process mode with Llama 3 / 3.1 via Ollama.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure Ollama is running and you have both models pulled:

```bash
ollama pull llama3
ollama pull llama3.1
```

Llama 3.1 is required for the Manager agent (tool-calling support). The worker agents use Llama 3.

## Run

```bash
python main.py
```

Watch the Manager delegate coding to the Developer, send the output to the QA Reviewer, and iterate until the code is approved. Verbose mode is on by default.

## Customization

- Change the `project_task` description to generate different code (e.g., a calculator, a todo app).
- Add more worker agents (e.g., a documentation writer) to expand the team.
- Replace `ollama/llama3.1` with a more capable model for better Manager delegation.

## Dependencies

- `crewai` -- multi-agent orchestration framework (Agent, Task, Crew, Process, LLM). Includes hierarchical process mode with the implicit Manager agent.
