"""
CrewAI Research Team

A multi-agent system where two AI agents collaborate sequentially:
  1. Researcher -- searches the web for facts about a given topic.
  2. Writer    -- turns those raw facts into a readable blog post.

The agents are orchestrated by CrewAI, which passes the output of
each task to the next in a sequential pipeline. The agents do not
share tools or overlap responsibilities -- each has a single role.
"""

from crewai import Agent, Task, Crew, Process, LLM
from langchain_community.tools import DuckDuckGoSearchRun
from crewai.tools import tool

print("Initializing multi-agent pipeline...")


# -- LLM Configuration -------------------------------------------------------
# Using Llama 3.1 via Ollama. Low temperature (0.2) for more factual,
# deterministic output from both agents.

llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.2
)


# -- Tools --------------------------------------------------------------------
# CrewAI tools are defined with the @tool decorator. This wraps a plain
# function into a tool object that agents can call during task execution.
# Only the researcher agent will have access to this tool.

@tool("Web Searching Tool")
def search_tool(query: str) -> str:
    """Useful for searching the internet for recent facts and news."""
    return DuckDuckGoSearchRun().run(query)


# -- Agents -------------------------------------------------------------------
# Each agent has a role, goal, backstory (persona), and optional tools.
# allow_delegation=False prevents agents from passing work to each other
# outside the defined task flow.

print("Creating agents...")

researcher = Agent(
    role="Senior Technology Researcher",
    goal="Uncover the latest factual developments about the user's topic.",
    backstory="You are a meticulous researcher. You use your search tool to find raw facts, numbers, and news. You never make things up.",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    llm=llm
)

writer = Agent(
    role="Expert Technical Blogger",
    goal="Craft an engaging, easy-to-read blog post based strictly on the researcher's findings.",
    backstory="You are a renowned tech writer. You take dry, raw data and turn it into engaging, readable Markdown articles. You do not do your own research.",
    verbose=True,
    allow_delegation=False,
    llm=llm
)


# -- Tasks --------------------------------------------------------------------
# Tasks define what each agent should do. In sequential mode, task2 receives
# the output of task1 automatically -- the writer sees the researcher's
# raw facts without any manual wiring.

topic = "The release of the Model Context Protocol (MCP) by Anthropic"

task1 = Task(
    description=f"Search the web and gather the most important facts, benefits, and technical details about: {topic}.",
    expected_output="A raw bulleted list of facts, links, and technical specs.",
    agent=researcher
)

task2 = Task(
    description="Using ONLY the raw facts provided by the researcher, write a 3-paragraph blog post explaining this technology to a beginner. Include a catchy title.",
    expected_output="A formatted 3-paragraph blog post in Markdown.",
    agent=writer
)


# -- Crew (Orchestration) ----------------------------------------------------
# The Crew ties agents and tasks together. Process.sequential runs tasks
# in order: task1 finishes, its output is passed to task2, then task2 runs.

crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

print("Starting pipeline...\n")
print("-" * 50)

try:
    response = crew.kickoff()
    print()
    print("\nFinal output:")
    print("=" * 50)
    print(response)
    print("=" * 50)
except Exception as e:
    print(f"Error: {e}")
