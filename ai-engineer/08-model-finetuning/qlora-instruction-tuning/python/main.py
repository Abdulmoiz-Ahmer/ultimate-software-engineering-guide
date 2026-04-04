"""
QLoRA Instruction Tuning -- Python

Fine-tunes a small language model (TinyLlama 1.1B) on custom instruction
data using LoRA (Low-Rank Adaptation). Instead of updating all model
parameters (billions), LoRA freezes the base model and trains a small
adapter (millions) that modifies the model's behavior.

The pipeline:
  1. Load the Alpaca-formatted dataset from the previous project.
  2. Download the base model and tokenizer from HuggingFace.
  3. Attach a LoRA adapter to the model's attention layers.
  4. Train only the adapter parameters using SFTTrainer.
  5. Save the trained adapter (a few MB, not the full model).

The adapter can later be loaded on top of the base model to get the
fine-tuned behavior without duplicating the entire model.

Requirements:
  - The dataset from huggingface-dataset-prep must be built first.
  - A GPU is recommended but not strictly required (CPU will be very slow).
"""

import os
import logging

import torch
from datasets import load_from_disk
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer, SFTConfig 

# Suppress verbose transformer warnings during training.
logging.getLogger("transformers").setLevel(logging.ERROR)


# -- 1. Load the Alpaca-formatted dataset -----------------------------------
# This is the dataset created by huggingface-dataset-prep. Each row has a
# "text" field containing the full Alpaca prompt (instruction + context +
# response formatted as a single string).

dataset_path = "./my-custom-alpaca-dataset"
if not os.path.exists(dataset_path):
    raise FileNotFoundError(
        f"Could not find dataset at {dataset_path}. "
        "Run huggingface-dataset-prep first."
    )

print("Loading dataset...")
dataset = load_from_disk(dataset_path)


# -- 2. Load the base model and tokenizer ----------------------------------
# TinyLlama 1.1B is small enough to fine-tune on consumer hardware while
# still being a real causal language model. device_map="auto" places
# layers on GPU if available, otherwise CPU. float16 halves memory usage.

model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
print(f"Downloading {model_id}...")

tokenizer = AutoTokenizer.from_pretrained(model_id)
# Many models don't define a padding token. Setting it to the end-of-
# sequence token prevents errors during batched training.
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    torch_dtype=torch.float16,
)


# -- 3. Attach the LoRA adapter --------------------------------------------
# LoRA freezes all base model weights and injects small trainable matrices
# into specific layers. Only these matrices are updated during training.
#
# Key parameters:
#   r=8          -- rank of the adapter matrices (higher = more capacity
#                   but more parameters). 8 is a common starting point.
#   lora_alpha   -- scaling factor for the adapter output. Usually 2x r.
#   target_modules -- which layers to attach adapters to. q_proj and v_proj
#                     are the query and value projections in the attention
#                     mechanism, where LoRA has the most impact.
#   lora_dropout -- dropout on adapter weights to prevent overfitting.

print("Attaching LoRA adapter...")

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)
# Shows exactly how many parameters are trainable vs. frozen.
model.print_trainable_parameters()


# -- 4. Configure the trainer -----------------------------------------------
# SFTTrainer (Supervised Fine-Tuning Trainer) from the trl library handles
# the training loop, including tokenization of the "text" field.
#
# Key settings:
#   per_device_train_batch_size=1 -- keeps memory usage low.
#   gradient_accumulation_steps=4 -- simulates a batch size of 4 by
#                                    accumulating gradients over 4 steps.
#   max_steps=20 -- very short run for demonstration. Real fine-tuning
#                    would use hundreds or thousands of steps.
#   fp16=True -- 16-bit floating point for faster training and lower memory.
#   optim="paged_adamw_8bit" -- memory-efficient optimizer variant.

print("Configuring trainer...")

training_args = SFTConfig(
    output_dir="./results",
    per_device_train_batch_size=1, 
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    logging_steps=1,
    max_steps=20, 
    fp16=True, 
    optim="paged_adamw_8bit",
    dataset_text_field="text", 
    max_length=512      
)

trainer = SFTTrainer(
  model=model,
    train_dataset=dataset,
    args=training_args,
)


# -- 5. Run training --------------------------------------------------------
# Watch the loss decrease over 20 steps. In a real scenario, you'd train
# for much longer and monitor validation loss to avoid overfitting.

print("\nStarting training (20 steps)...")
print("-" * 50)
trainer.train()
print("-" * 50)


# -- 6. Save the trained adapter --------------------------------------------
# Only the LoRA adapter weights are saved (a few MB). The base model is
# unchanged. To use the fine-tuned model later, load the base model and
# apply the adapter on top.

save_path = "./my-trained-lora-adapter"
print(f"\nSaving LoRA adapter to {save_path}...")
trainer.save_model(save_path)
print(f"Done. Adapter saved to {save_path}")
