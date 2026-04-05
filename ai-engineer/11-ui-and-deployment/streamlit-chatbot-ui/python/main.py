"""
Streamlit Chatbot UI -- Python

A browser-based chat interface built with Streamlit that connects to
the FastAPI LLM service from the previous project. Streamlit handles
the entire frontend: page layout, chat bubbles, input box, loading
states, and session memory -- all in pure Python, no HTML/JS needed.

Architecture:
  Streamlit UI (this file) -> HTTP POST -> FastAPI backend -> Ollama LLM

Key Streamlit behavior: the entire script re-executes from top to bottom
on every user interaction (typing a message, clicking a button). This is
why st.session_state is needed to persist data across reruns.
"""

import streamlit as st
import requests


# -- 1. Page configuration -------------------------------------------------
# set_page_config must be the first Streamlit command. It sets the browser
# tab title and favicon.

st.set_page_config(page_title="Local AI Chat", page_icon="chat")
st.title("Local AI Chat")
st.caption("Powered by Llama 3.1 and FastAPI")

# The URL of the FastAPI backend (must be running before using this UI).
API_URL = "http://127.0.0.1:8000/api/chat"


# -- 2. Session state (conversation memory) --------------------------------
# Streamlit re-runs this entire file on every user interaction, which means
# normal Python variables are reset each time. st.session_state is a dict
# that persists across reruns, acting as the app's in-memory state.
#
# We store the full conversation history as a list of {"role", "content"}
# dicts so the UI can render all previous messages on each rerun.

if "messages" not in st.session_state:
    st.session_state.messages = []

# Render all previous messages from session state. st.chat_message creates
# a styled bubble with an icon based on the role ("user" or "assistant").
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# -- 3. Chat input and response --------------------------------------------
# st.chat_input creates a text box pinned to the bottom of the screen.
# The walrus operator (:=) assigns the input to user_prompt and evaluates
# to True if the user submitted a message, triggering the if block.

if user_prompt := st.chat_input("Ask me anything..."):

    # Display the user's message immediately as a chat bubble.
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Save to session state so it persists across reruns.
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # Create an assistant bubble with a spinner while waiting for the API.
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # POST the user's message to the FastAPI backend.
                response = requests.post(API_URL, json={"user_message": user_prompt})

                # Raise an exception for HTTP error codes (4xx, 5xx).
                response.raise_for_status()

                # Extract the model's reply from the JSON response.
                ai_reply = response.json()["ai_reply"]

                # Render the reply inside the chat bubble (replaces spinner).
                st.markdown(ai_reply)

                # Save the assistant's reply to session state.
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})

            except Exception as e:
                st.error(f"Failed to connect to the backend API: {e}")
