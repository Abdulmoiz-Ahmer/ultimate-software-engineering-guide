# HuggingFace Dataset Prep

Prepares training data for LLM fine-tuning by converting raw instruction/context/response examples into the **Alpaca prompt format** and saving them as a HuggingFace Dataset.

## What it does

1. Defines raw training examples with `instruction`, `context`, and `response` fields.
2. Formats each example into the Alpaca template (a single "text" string).
3. Saves the formatted dataset as optimized Arrow files for fine-tuning.

## The Alpaca format

The [Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca) format is the most widely used template for instruction-tuning. The model learns to follow instructions by training on examples structured like this:

**With context:**
```
Below is an instruction that describes a task, paired with an input
that provides further context. Write a response that appropriately
completes the request.

### Instruction:
Extract the error code from the following log.

### Input:
System crashed at midnight. Traceback: 0x88A FATAL_MEMORY_LEAK.

### Response:
0x88A
```

**Without context:**
```
Below is an instruction that describes a task. Write a response
that appropriately completes the request.

### Instruction:
Write a professional email declining a meeting.

### Response:
Hi team, I am currently at capacity and will have to decline...
```

## Key concepts

- **Instruction tuning** -- fine-tuning a base model on instruction/response pairs so it learns to follow instructions rather than just predict next tokens.
- **Alpaca format** -- a prompt template that structures training data into `### Instruction`, `### Input` (optional), and `### Response` sections. The model learns this structure during training.
- **HuggingFace Dataset** -- a high-performance data container backed by Apache Arrow. Supports efficient `.map()` transformations and saves to disk in a format compatible with fine-tuning frameworks.
- **Why formatting matters** -- the model learns whatever structure it sees during training. Consistent formatting (same template, same delimiters) ensures the model reliably follows the pattern at inference time.

## Prerequisites

- Python 3.10+
- No API keys or GPU needed -- this is data preparation only

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
