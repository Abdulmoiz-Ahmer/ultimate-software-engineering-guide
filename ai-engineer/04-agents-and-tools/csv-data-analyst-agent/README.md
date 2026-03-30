# CSV Data Analyst Agent

A natural-language data analyst powered by LangChain's `create_csv_agent`. Ask questions about a CSV file in plain English and the agent writes and executes Pandas code to get the answer.

## What it does

1. Loads a CSV file (`sales.csv`) into a Pandas DataFrame.
2. You ask a question in natural language.
3. The agent uses the ReAct pattern (Reason + Act) to write Python/Pandas code, execute it, observe the result, and return a human-readable answer.

## Sample data

The included `sales.csv` contains a small sales dataset:

| Date | Region | Product | Units_Sold | Price_Per_Unit | Total_Sales |
|------|--------|---------|------------|----------------|-------------|
| 2026-01-01 | North | Widget A | 100 | 10.50 | 1050.00 |
| 2026-01-02 | South | Widget B | 50 | 20.00 | 1000.00 |
| ... | ... | ... | ... | ... | ... |

## Key concepts

- **`create_csv_agent`** -- loads a CSV into a DataFrame and gives the LLM a Python REPL tool to query it.
- **ReAct agent** (`zero-shot-react-description`) -- the LLM reasons about the question, decides what code to run, observes the output, and iterates until it has an answer.
- **`allow_dangerous_code=True`** -- required because the agent executes Python code at runtime. Only use with trusted input in local environments.
- **`handle_parsing_errors=True`** -- automatically retries when the LLM output can't be parsed into a valid action.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with the `llama3.1` model pulled

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3.1
```

## Usage

```bash
python main.py
```

Example queries:

- `What is the total sales across all regions?`
- `Which product sold the most units?`
- `Show me the average price per unit by region.`
- Type `q` to quit.
