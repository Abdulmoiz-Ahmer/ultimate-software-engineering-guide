"""
CrewAI Hierarchical Multi-Agent

A multi-agent system using CrewAI's hierarchical process mode. Instead of
running tasks sequentially, a hidden Manager agent controls the workflow:
  - It reads the task description.
  - It decides which worker agent to assign work to.
  - It reviews output and can send work back for revision.

The workers (Developer and QA Reviewer) never talk to each other directly.
All coordination flows through the Manager.
"""

from crewai import Agent, Task, Crew, Process, LLM

print("Initializing hierarchical multi-agent pipeline...")


# -- LLM Configuration -------------------------------------------------------
# Worker agents (coder, QA) use Llama 3 -- they only need to follow
# instructions and produce text, no tool-calling required.

worker_llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434",
    temperature=0.1
)

# The Manager agent needs tool-calling capability to delegate tasks to
# workers. Llama 3.1 supports tool use natively; Llama 3 does not.
# If you only have Llama 3, it may still work but delegation will be
# less reliable.

manager_llm = LLM(
    model="ollama/llama3.1",
    base_url="http://localhost:11434",
    temperature=0.1
)


# -- Worker Agents ------------------------------------------------------------
# Workers have allow_delegation=False so they cannot pass work to each
# other. Only the Manager (created implicitly by CrewAI) can delegate.

print("Creating worker agents...")

coder = Agent(
    role="Senior Python Developer",
    goal="Write clean, highly functional, and well-documented Python code based on the prompt.",
    backstory="You are a veteran software engineer. You write the initial drafts of code. You listen to feedback from the QA Reviewer and fix your mistakes.",
    verbose=True,
    allow_delegation=False,
    llm=worker_llm
)

qa_engineer = Agent(
    role="Strict QA Code Reviewer",
    goal="Analyze code written by the Developer, find bugs, and explain exactly what needs to be fixed.",
    backstory="You are a rigorous quality assurance engineer. You do not write code yourself. You read code, find errors, and report them to the Manager to send back for fixing.",
    verbose=True,
    allow_delegation=False,
    llm=worker_llm
)


# -- Task ---------------------------------------------------------------------
# In hierarchical mode, tasks are NOT assigned to a specific agent.
# The Manager reads the task description and decides which agent(s)
# to involve and in what order.

project_task = Task(
    description="Create a fully functional Python script for a CLI-based Tic-Tac-Toe game. It must have input validation so users cannot overwrite existing moves.",
    expected_output="A single, complete, bug-free Python script containing the game.",
)


# -- Crew (Hierarchical Orchestration) ----------------------------------------
# Process.hierarchical activates a hidden Manager agent that:
#   1. Reads the task and assigns it to the coder.
#   2. Sends the coder's output to the QA engineer for review.
#   3. If bugs are found, sends the code back to the coder with feedback.
#   4. Repeats until the QA engineer approves.
# The manager_llm parameter provides the Manager with its own LLM.

print("Manager agent taking control of the project...")

crew = Crew(
    agents=[coder, qa_engineer],
    tasks=[project_task],
    process=Process.hierarchical,
    manager_llm=manager_llm,
    verbose=True
)

print("\nStarting pipeline...\n")
print("-" * 50)

try:
    final_code = crew.kickoff()
    print()
    print("\nFinal output:")
    print("=" * 50)
    print(final_code)
    print("=" * 50)
except Exception as e:
    print(f"Error: {e}")
