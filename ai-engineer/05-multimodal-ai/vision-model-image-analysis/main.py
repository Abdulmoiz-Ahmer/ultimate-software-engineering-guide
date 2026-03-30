"""
Vision Model Image Analysis

Sends an image to a local vision-capable LLM (Llama 3.2 Vision via Ollama)
for analysis. The image is base64-encoded and passed as part of a multimodal
HumanMessage alongside a text prompt.

This demonstrates the multimodal input pattern:
  1. Read an image file from disk.
  2. Encode it as a base64 data URI.
  3. Build a HumanMessage with both text and image content blocks.
  4. Send to a vision model and print the analysis.

The prompt is designed to handle two scenarios:
  - Receipts: extract the total amount and store name.
  - General images: provide a detailed description.
"""

import base64
import os

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


# -- Helper: encode image to base64 ----------------------------------------
# Vision models can't read files directly. The image must be converted to
# a base64 string and wrapped in a data URI (data:image/jpeg;base64,...).
# This is the same format used by web browsers for inline images.

def encode_image(path):
    if not os.path.exists(path):
        print(f"Error: Could not find image at '{path}'")
        exit()
    with open(path, "rb") as image:
        return base64.b64encode(image.read()).decode("utf-8")


# -- 1. Set up the vision model --------------------------------------------
# Llama 3.2 Vision is a multimodal model that accepts both text and images.
# temperature=0 for consistent, deterministic analysis.

llm = ChatOllama(model="llama3.2-vision", temperature=0)


# -- 2. Encode the image and build the message -----------------------------
# A multimodal HumanMessage contains a list of content blocks. Each block
# has a "type" field: "text" for the prompt, "image_url" for the image.
# The image is passed as a base64 data URI, not a file path or URL.

image_path = "sample_receipt.jpg"
base64_image = encode_image(image_path)

prompt_text = (
    "Analyze this image. If it is a receipt, extract the total amount "
    "and the store name. If it is a general image, provide a highly "
    "detailed description of what is happening."
)

message = HumanMessage(
    content=[
        {"type": "text", "text": prompt_text},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
        },
    ]
)


# -- 3. Send to the model and print the result -----------------------------
# invoke() accepts a list of messages, just like a text-only chat call.
# The vision model processes both the text prompt and the image together.

try:
    response = llm.invoke([message])

    print("\nAnalysis complete:")
    print("-" * 50)
    print(response.content)
    print("-" * 50)

except Exception as e:
    print(f"Error: {e}")
