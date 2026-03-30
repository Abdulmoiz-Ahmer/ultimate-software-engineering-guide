"""
Manual Tool-Calling Agent

Demonstrates how to manually implement the tool-calling loop with LangChain
instead of relying on AgentExecutor. The LLM decides whether to invoke a tool
based on the user's query, and our code handles executing the tool function
and feeding the result back to the LLM for a final response.

Flow:
  User query -> LLM decides (tool or direct answer)
    -> If tool: execute function -> return result to LLM -> final answer
    -> If no tool: LLM answers directly
"""

from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage, SystemMessage


# -- 1. Define the tool ---------------------------------------------------
# The @tool decorator converts a Python function into a JSON schema the LLM
# can understand. The docstring is essential -- the LLM reads it to decide
# when to call this tool.

@tool
def get_weather(target_location_for_weather_forecast_only: str) -> str:
    """Fetches the current meteorological weather, temperature, or forecast.
    CRITICAL INSTRUCTION: NEVER use this tool for geography, location, or
    history questions. ONLY use this if the user specifically types the
    words 'weather', 'temperature', or 'forecast'."""

    print(f"\n   [SYSTEM: Executing get_weather('{target_location_for_weather_forecast_only}')]")

    # Stub data -- replace with a real weather API call in production.
    city_lower = target_location_for_weather_forecast_only.lower()
    if "tokyo" in city_lower:
        return "Raining, 15C"
    elif "rawalpindi" in city_lower:
        return "Clear, 28C"
    else:
        return "Sunny, 22C"


# -- 2. Set up the LLM with tools -----------------------------------------
# bind_tools attaches the tool schema to the model so it knows what tools
# are available and how to call them.

llm = ChatOllama(model="llama3.1", temperature=0)
llm_with_tools = llm.bind_tools([get_weather])

print("Agent ready!\n")
print("-" * 50)


# -- 3. Interactive loop ---------------------------------------------------
# Each iteration builds a fresh message list (system + user), sends it to
# the LLM, and then manually processes any tool calls the LLM makes.

while True:
    user_query = input("\nYou: ")
    if user_query.lower() in ("q", "quit", "exit"):
        break

    # Start each turn with a system prompt that constrains tool usage,
    # followed by the user's message.
    messages = [
        SystemMessage(
            content=(
                "You are a strict, helpful AI. ONLY use tools if the user "
                "explicitly asks for weather. If the user asks about geography, "
                "location, or general knowledge, DO NOT use any tools. "
                "Answer from your own memory."
            )
        ),
        HumanMessage(content=user_query),
    ]

    print("   [AI is thinking...]")

    try:
        # Step A: Send messages to the LLM and let it decide whether to
        # call a tool or respond directly.
        ai_response = llm_with_tools.invoke(messages)
        messages.append(ai_response)

        # Step B: If the LLM chose to call one or more tools, execute them.
        if ai_response.tool_calls:
            for tool_call in ai_response.tool_calls:
                print(f"   [AI decided to use tool: {tool_call['name']}]")

                # Step C: Match the tool name and run the corresponding
                # Python function with the arguments the LLM provided.
                if tool_call["name"] == "get_weather":
                    city_arg = tool_call["args"]["target_location_for_weather_forecast_only"]
                    function_result = get_weather.invoke(city_arg)

                    # Step D: Wrap the function output in a ToolMessage so
                    # the LLM can associate it with the correct tool call.
                    tool_msg = ToolMessage(
                        content=function_result,
                        tool_call_id=tool_call["id"],
                    )
                    messages.append(tool_msg)

            # Step E: Send the updated messages (now including tool results)
            # back to the LLM so it can compose a human-friendly answer.
            print("   [AI is reading the tool output...]")
            final_response = llm_with_tools.invoke(messages)
            print(f"\nAgent: {final_response.content}")

        else:
            # No tool was needed -- the LLM answered directly.
            print(f"\nAgent: {ai_response.content}")

    except Exception as e:
        print(f"Error: {e}")
