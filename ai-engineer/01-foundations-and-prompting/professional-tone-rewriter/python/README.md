# Professional Tone Rewriter -- Python

Python implementation using the `google-genai` SDK with system instructions and temperature control.

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

Paste your text and get a professional rewrite. Type `q` to quit.

## Dependencies

- `google-genai` -- Google's Gemini SDK (V2), with `types.GenerateContentConfig` for system instructions and temperature
- `python-dotenv` -- loads the API key from `.env`
