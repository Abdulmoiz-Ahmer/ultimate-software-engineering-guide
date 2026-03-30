# Vision Model Image Analysis

Sends an image to a local vision-capable LLM (**Llama 3.2 Vision** via Ollama) for analysis. Demonstrates how to build multimodal messages that combine text and image inputs using LangChain.

## What it does

1. Reads an image file from disk and encodes it as base64.
2. Builds a multimodal `HumanMessage` with a text prompt and the image.
3. Sends it to Llama 3.2 Vision for analysis.
4. Prints the model's description or extracted data.

The prompt handles two scenarios:
- **Receipts** -- extracts the total amount and store name.
- **General images** -- provides a detailed description of the scene.

## Key concepts

- **Multimodal messages** -- a `HumanMessage` can contain multiple content blocks with different types (`"text"` and `"image_url"`). This is how you pass both a prompt and an image to a vision model.
- **Base64 data URI** -- vision models can't read files directly. The image is encoded as a base64 string and wrapped in a data URI (`data:image/jpeg;base64,...`), the same format used by web browsers for inline images.
- **Vision models** -- Llama 3.2 Vision is a multimodal model that processes both text and images in a single call. The `ChatOllama` interface is the same as for text-only models.

## Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com/) running locally with the `llama3.2-vision` model pulled

## Setup

```bash
pip install -r requirements.txt
ollama pull llama3.2-vision
```

## Usage

Place an image file in the project folder (default: `sample_receipt.jpg`), then run:

```bash
python main.py
```

## Customization

- Change `image_path` in `main.py` to analyze a different image.
- Edit `prompt_text` to ask different questions about the image.
- For PNG images, change the data URI prefix from `image/jpeg` to `image/png`.
