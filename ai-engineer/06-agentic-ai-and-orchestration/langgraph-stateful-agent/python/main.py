"""
LangGraph Stateful Agent

A graph-based agent loop where a Writer node drafts a story and a
Critic node reviews it. If the draft doesn't meet the criteria (must
mention an animal), the Critic sends feedback and the graph loops back
to the Writer for another attempt -- up to a maximum of 3 iterations.

This demonstrates LangGraph's core pattern:
  1. Define a shared state (TypedDict).
  2. Create nodes (functions) that read and update that state.
  3. Wire nodes together with edges and conditional routing.
  4. The graph manages the loop, state passing, and termination.
"""

from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama

print("Initializing LangGraph agent...")


# -- Shared State -------------------------------------------------------------
# Every node in the graph reads from and writes to this shared state dict.
# LangGraph merges each node's return value into the state automatically.

class AgentState(TypedDict):
    draft: str        # the current story draft
    feedback: str     # critic's feedback or "approved"
    iterations: int   # how many write attempts have been made


# -- LLM ---------------------------------------------------------------------

llm = ChatOllama(model="llama3", temperature=0.5)


# -- Node: Writer -------------------------------------------------------------
# Reads any existing feedback from the state and writes a new draft.
# On the first pass, feedback is the initial instruction. On subsequent
# passes, it contains the critic's rejection reason.

def write_draft(state: AgentState):
    iteration = state.get("iterations", 0) + 1
    print(f"\n[Writer] Drafting (iteration {iteration})...")

    feedback = state.get("feedback", "None")
    prompt = f"Write a short, creative 2-sentence story. Feedback to incorporate: {feedback}"

    response = llm.invoke(prompt)

    return {
        "draft": response.content,
        "iterations": iteration
    }


# -- Node: Critic -------------------------------------------------------------
# Checks whether the draft meets the acceptance criteria (must mention
# an animal). Returns "approved" or a rejection with specific feedback.

def review_draft(state: AgentState):
    print("[Critic] Reviewing the draft...")

    draft = state["draft"]
    prompt = f"Does this story explicitly mention an animal? Story: {draft}\nAnswer ONLY with the word 'yes' or 'no'."
    response = llm.invoke(prompt).content.lower()

    if "yes" in response:
        print("   -> Approved. Story mentions an animal.")
        return {"feedback": "approved"}
    else:
        print("   -> Rejected. Missing an animal.")
        return {"feedback": "You must include an animal in the story!"}


# -- Conditional Edge: should_continue ----------------------------------------
# After the critic reviews, this function decides where the graph goes next:
#   - If approved or max iterations reached -> END (terminate the graph)
#   - Otherwise -> loop back to the "writer" node for another attempt

def should_continue(state: AgentState):
    if "approved" in state["feedback"] or state["iterations"] >= 3:
        return END
    return "writer"


# -- Build the Graph ----------------------------------------------------------
# StateGraph manages the flow: writer -> reviewer -> (conditional) -> writer or END
# The entry point is always the writer node.

print("Building graph...")

builder = StateGraph(AgentState)

# Register the two nodes
builder.add_node("writer", write_draft)
builder.add_node("reviewer", review_draft)

# Writer is always the first node to execute
builder.set_entry_point("writer")

# Writer output always goes to the reviewer
builder.add_edge("writer", "reviewer")

# After the reviewer, the conditional edge decides: loop back or end
builder.add_conditional_edges("reviewer", should_continue)

# Compile the graph into a runnable object
graph = builder.compile()


# -- Execute ------------------------------------------------------------------
# invoke() runs the graph from the entry point with the given initial state.
# The graph loops until should_continue returns END.

print("\nStarting graph execution...\n")
print("-" * 50)

final_state = graph.invoke({
    "draft": "",
    "iterations": 0,
    "feedback": "Make sure it is exactly two sentences.",
})

print("-" * 50)
print(f"\nFinal state:")
print(f"  Iterations: {final_state['iterations']}")
print(f"  Draft:\n{final_state['draft']}")
