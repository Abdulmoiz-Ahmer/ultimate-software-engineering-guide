# LangSmith Tracing

Adds **observability** to a LangChain pipeline using [LangSmith](https://smith.langchain.com/). Every LLM call, prompt, and output is automatically traced and sent to a web dashboard for inspection -- with zero code changes to the pipeline itself.

## The problem

When an LLM pipeline gives a bad answer, you need to know:
- What exact prompt was sent to the model?
- What did the model actually return?
- How long did it take? How many tokens were used?
- Where in a multi-step chain did things go wrong?

Without observability, you're debugging blind.

## How LangSmith solves it

```
Your LangChain code (unchanged)
    |
    v
LANGCHAIN_TRACING_V2=true (environment variable)
    |
    v
LangChain auto-sends traces to LangSmith API
    |
    v
LangSmith dashboard shows:
  - Full prompt text
  - Raw LLM response
  - Latency per step
  - Token counts and cost
  - Error traces
```

Tracing is enabled entirely through environment variables -- no code instrumentation needed. When `LANGCHAIN_TRACING_V2=true` is set, LangChain automatically captures and sends trace data.

## Key concepts

- **Tracing** -- recording the inputs, outputs, and timing of every step in an LLM pipeline. LangSmith collects these traces automatically when the environment variables are configured.
- **Zero-code instrumentation** -- LangChain's integration with LangSmith requires no decorators, wrappers, or code changes. Set the env vars and traces appear.
- **Projects** -- traces are grouped under a project name (`LANGCHAIN_PROJECT`), making it easy to separate development, staging, and production traces.
- **LCEL chain** -- the demo uses a simple prompt -> LLM -> parser chain. In production, the same tracing works for complex multi-step agents and RAG pipelines.
- **Why this matters** -- observability is essential for debugging, evaluating, and monitoring LLM applications in production. LangSmith is the standard tool in the LangChain ecosystem.

## Environment variables

| Variable | Purpose |
|---|---|
| `LANGCHAIN_TRACING_V2` | Set to `true` to enable tracing |
| `LANGCHAIN_API_KEY` | Your LangSmith API key (starts with `lsv2_pt_`) |
| `LANGCHAIN_ENDPOINT` | API endpoint (default: `https://api.smith.langchain.com`) |
| `LANGCHAIN_PROJECT` | Project name to group traces under |

## Prerequisites

- A [LangSmith](https://smith.langchain.com/) account and API key (free tier available)
- [Ollama](https://ollama.com/) running locally with `llama3` pulled

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
