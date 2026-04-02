# CrewAI Research Team -- Python

Python implementation using the `crewai` framework with `DuckDuckGoSearchRun` for web search and Llama 3.1 via Ollama.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Make sure Ollama is running and you have Llama 3.1 pulled:

```bash
ollama pull llama3.1
```

## Run

```bash
python main.py
```

The researcher agent searches the web, then the writer agent produces a blog post from those findings. Verbose mode is on by default so you can watch the agents reason and act in real time.

## Customization

- Change the `topic` variable in `main.py` to research any subject.
- Replace `ollama/llama3.1` with a different model (e.g., `ollama/mistral`).
- Set `verbose=False` on the agents or crew to suppress step-by-step logs.

## Dependencies

- `crewai` -- multi-agent orchestration framework (Agent, Task, Crew, Process)
- `crewai-tools` -- the `@tool` decorator for defining agent-callable tools
- `langchain-community` -- `DuckDuckGoSearchRun` for web search
- `duckduckgo-search` -- backend used by DuckDuckGoSearchRun
