# Simple CLI Chatbot (Gemini 2.5)

A lightweight, terminal-based chatbot powered by Google's **Gemini 2.5 Flash** model. This project demonstrates how to build a Python application that maintains conversation history and interacts with the modern `google-genai` SDK.

## Features

- **Persistent Memory:** The bot remembers previous context in the conversation loop (e.g., it remembers your name).
- **Gemini 2.5 Integration:** Uses the latest `google-genai` SDK (V2) with the `gemini-2.5-flash` model.
- **Secure:** Uses `.env` to protect API keys.
- **Clean CLI:** Simple, distraction-free terminal interface with streaming capabilities.

## Prerequisites

- Python 3.10 or higher
- A Google Cloud Project with the Gemini API enabled
- A Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1.  **Clone the repository** (if you haven't already):

    ```bash
    git clone <your-repo-url>
    cd ai-engineer/simple-cli-chatbot
    ```

2.  **Set up the Virtual Environment:**

    ```bash
    # Create the environment
    python3 -m venv venv

    # Activate it (Mac/Linux)
    source venv/bin/activate

    # Activate it (Windows)
    .\venv\Scripts\Activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install google-genai python-dotenv
    ```

## Configuration

1.  Create a `.env` file in the project root:

    ```bash
    touch .env  # or create it manually in your editor
    ```

2.  Add your API key to the file:
    ```env
    GEMINI_API_KEY=AIzaSy...[Your-Key-Here]
    ```

## Usage

Run the chatbot script:

```bash
python chatbot.py
```
