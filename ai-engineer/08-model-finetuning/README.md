# 08 -- Model Finetuning

This module covers how to customize a language model's behavior by fine-tuning it on your own data. The first project prepares the training data, and the second project trains a LoRA adapter on that data -- so the model learns to follow your specific instructions.

## Project structure

Each project folder contains a language-agnostic README explaining the concept, with implementation-specific code and instructions inside language subfolders:

```
project-name/
  README.md          # What it does, key concepts, prerequisites
  python/            # Python implementation + setup instructions
    main.py
    requirements.txt
    README.md
  # js/              # (coming soon)
```

## Learning path

### 1. [HuggingFace Dataset Prep](huggingface-dataset-prep/)

Prepares training data for fine-tuning by converting raw instruction/context/response examples into the Alpaca prompt format and saving them as a HuggingFace Dataset. This is the data pipeline that feeds into the training step.

**You learn:** How training data is structured for instruction tuning, what the Alpaca format is, and how HuggingFace Datasets work.

**Key concepts:** Instruction tuning, Alpaca format, HuggingFace Dataset, prompt templates, Apache Arrow storage

---

### 2. [QLoRA Instruction Tuning](qlora-instruction-tuning/)

Fine-tunes TinyLlama 1.1B on the dataset from project 1 using LoRA adapters. Instead of updating all model parameters (billions), LoRA freezes the base model and trains a small adapter (millions of parameters) injected into the attention layers. The result is a customized model with ~99% fewer trainable parameters.

**You learn:** How LoRA works, why it's dramatically more memory-efficient than full fine-tuning, and how to run a training loop with SFTTrainer.

**Key concepts:** LoRA (Low-Rank Adaptation), adapter matrices, target modules (q_proj/v_proj), SFTTrainer, gradient accumulation

## Prerequisites

- Python 3.10+
- A GPU is recommended for project 2 (NVIDIA with CUDA)
- No API keys needed
- Project 2 depends on the dataset output from project 1

Each project has its own `README.md` with concept explanations, and each language folder has setup instructions.
