# Gemini Chat CLI -- Python

Python implementation using the `google-genai` SDK.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy `example.env` to `.env` and add your API key:

```bash
cp example.env .env
# Edit .env and set GEMINI_API_KEY=your_key_here
```

## Run

```bash
python main.py
```

Type messages and the bot responds. Type `q` to quit.

## Dependencies

- `google-genai` -- Google's Gemini SDK (V2)
- `python-dotenv` -- loads the API key from `.env`
