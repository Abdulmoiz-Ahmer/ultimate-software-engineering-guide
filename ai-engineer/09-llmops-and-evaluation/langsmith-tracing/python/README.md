# LangSmith Tracing -- Python

Python implementation using LangChain with LangSmith tracing enabled via environment variables.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `example.env` to `.env` and add your LangSmith API key:

```bash
cp example.env .env
# Edit .env and set LANGCHAIN_API_KEY=your_key_here
```

Get a free API key from [LangSmith](https://smith.langchain.com/).

Make sure Ollama is running with `llama3` pulled:

```bash
ollama pull llama3
```

## Run

```bash
python main.py
```

After running, open the [LangSmith dashboard](https://smith.langchain.com/) and look for the trace under your project name.

## Dependencies

- `langchain-core` -- prompt templates, output parsers, LCEL chain
- `langchain-ollama` -- local Llama 3 via Ollama
- `langsmith` -- tracing client (sends traces to the LangSmith API)
- `python-dotenv` -- loads LangSmith credentials from `.env`
