"""
CSV Data Analyst Agent

Uses LangChain's create_csv_agent to build an agent that can answer
natural-language questions about a CSV file. Under the hood the agent
loads the CSV into a Pandas DataFrame and writes/executes Python code
to answer each query.

The agent type is "zero-shot-react-description", which means it uses
the ReAct (Reason + Act) pattern: think about the question, decide
which tool to use, observe the result, and repeat until it has an answer.
"""

from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_ollama import ChatOllama


# -- 1. Set up the LLM and CSV agent --------------------------------------
# create_csv_agent loads the CSV into a Pandas DataFrame and gives the
# LLM a Python REPL tool so it can write and run Pandas code on the fly.
#
# Key options:
#   verbose=True             -- prints each reasoning step
#   allow_dangerous_code     -- required because the agent runs eval/exec
#   handle_parsing_errors    -- retries if the LLM output can't be parsed

llm = ChatOllama(model="llama3.1", temperature=0)
csv_file_path = "sales.csv"

try:
    agent_executor = create_csv_agent(
        llm,
        csv_file_path,
        verbose=True,
        allow_dangerous_code=True,
        agent_type="zero-shot-react-description",
        handle_parsing_errors=True,
    )
except Exception as error:
    print(f"Failed to load agent: {error}")
    exit()

print("Agent ready! CSV loaded into a Pandas DataFrame.\n")
print("-" * 50)


# -- 2. Interactive loop ---------------------------------------------------
# Each query is sent to the agent, which writes Pandas code, executes it,
# and returns the result in plain language.

while True:
    user_query = input("\nYou: ")
    if user_query.lower() in ("q", "e", "exit", "quit"):
        break

    print("[AI is writing and running Pandas code...]")

    try:
        response = agent_executor.invoke({"input": user_query})
        print(f"\nAgent: {response['output']}")
    except Exception as error:
        print(f"\nError: {error}")
