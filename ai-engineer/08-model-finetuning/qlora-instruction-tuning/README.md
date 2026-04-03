# QLoRA Instruction Tuning

Fine-tunes a language model on custom instruction data using **LoRA (Low-Rank Adaptation)**. Instead of updating all model parameters (billions), LoRA freezes the base model and trains a small adapter (millions of parameters) that modifies the model's behavior.

## The problem

Full fine-tuning requires updating every parameter in the model, which needs enormous GPU memory and produces a full-size model copy. For a 7B parameter model, that means ~28 GB of GPU RAM just for the weights.

## How LoRA solves it

```
Base model (frozen, unchanged)
    |
    +-- Attention layer: q_proj
    |       |
    |       +-- LoRA adapter (small trainable matrix, rank 8)
    |
    +-- Attention layer: v_proj
            |
            +-- LoRA adapter (small trainable matrix, rank 8)

Only the adapter matrices are trained. Everything else stays frozen.
```

LoRA injects small, low-rank matrices into specific layers (typically the attention projections). During training, only these adapter weights are updated. The result is:

- ~99% fewer trainable parameters
- Dramatically lower GPU memory usage
- The adapter is only a few MB (not a full model copy)
- The base model is unchanged, so you can swap adapters for different tasks

## Key concepts

- **LoRA (Low-Rank Adaptation)** -- freezes the base model and trains small adapter matrices injected into attention layers. The rank (`r`) controls adapter capacity.
- **QLoRA** -- LoRA combined with 4-bit quantization of the base model, reducing memory further (not used in this demo for hardware compatibility, but the concept is the same).
- **SFTTrainer** -- Supervised Fine-Tuning Trainer from the `trl` library. Handles tokenization, training loop, and gradient accumulation.
- **Target modules** -- `q_proj` and `v_proj` are the query and value projections in the attention mechanism, where LoRA adapters have the most impact on model behavior.
- **Gradient accumulation** -- simulates larger batch sizes by accumulating gradients over multiple forward passes before updating weights. Keeps memory low.

## Pipeline

1. Load the Alpaca-formatted dataset (from [huggingface-dataset-prep](../huggingface-dataset-prep/)).
2. Download the base model (TinyLlama 1.1B) and tokenizer.
3. Attach LoRA adapters to the attention layers.
4. Train only the adapter parameters (20 steps for demo).
5. Save the trained adapter (a few MB).

## Prerequisites

- A GPU is recommended (NVIDIA with CUDA)
- The dataset from [huggingface-dataset-prep](../huggingface-dataset-prep/) must be built first

## Implementations

| Language | Folder |
|---|---|
| Python | [python/](python/) |
