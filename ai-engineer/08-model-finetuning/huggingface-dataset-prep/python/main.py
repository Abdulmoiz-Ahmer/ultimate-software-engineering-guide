"""
HuggingFace Dataset Prep -- Python

Prepares training data for LLM fine-tuning by converting raw
instruction/context/response examples into the Alpaca prompt format
and saving them as a HuggingFace Dataset.

The Alpaca format is a widely used template for instruction-tuning:

  With context:
    ### Instruction:
    {instruction}
    ### Input:
    {context}
    ### Response:
    {response}

  Without context:
    ### Instruction:
    {instruction}
    ### Response:
    {response}

Each example is formatted into a single "text" string. The saved
dataset (Arrow format) can be loaded directly into fine-tuning
frameworks like Hugging Face Transformers, Axolotl, or Unsloth.
"""

from datasets import Dataset


# -- 1. Define raw training data -------------------------------------------
# Each example has three fields:
#   instruction -- what the user asks the model to do
#   context     -- optional background information (empty string if none)
#   response    -- the exact answer the model should learn to produce
#
# In practice, this would be loaded from a CSV or JSONL file with
# hundreds or thousands of examples.

print("Loading raw training data...")

raw_data = [
    {
        "instruction": "Extract the error code from the following log.",
        "context": "System crashed at midnight. Traceback: 0x88A FATAL_MEMORY_LEAK.",
        "response": "0x88A",
    },
    {
        "instruction": "Write a professional email declining a meeting.",
        "context": "",
        "response": "Hi team, I am currently at capacity and will have to decline this meeting. Best, AI.",
    },
    {
        "instruction": "Classify the sentiment of this review.",
        "context": "The battery life on this laptop is absolute garbage.",
        "response": "Negative",
    },
]


# -- 2. Convert to HuggingFace Dataset ------------------------------------
# Dataset.from_list converts a Python list of dicts into a high-performance
# HuggingFace Dataset backed by Apache Arrow (columnar, memory-mapped).

hf_dataset = Dataset.from_list(raw_data)


# -- 3. Format into Alpaca prompt template ---------------------------------
# The formatting function takes a single row and returns a dict with a
# "text" field containing the complete prompt string. The Alpaca format
# includes the context block only when context is present, so the model
# learns to handle both cases.

def format_instruction_prompt(example):
    if example.get("context"):
        prompt = (
            "Below is an instruction that describes a task, paired with an "
            "input that provides further context. "
            "Write a response that appropriately completes the request.\n\n"
            f"### Instruction:\n{example['instruction']}\n\n"
            f"### Input:\n{example['context']}\n\n"
            f"### Response:\n{example['response']}"
        )
    else:
        prompt = (
            "Below is an instruction that describes a task. "
            "Write a response that appropriately completes the request.\n\n"
            f"### Instruction:\n{example['instruction']}\n\n"
            f"### Response:\n{example['response']}"
        )
    return {"text": prompt}


# -- 4. Apply the template to every row -----------------------------------
# .map() runs the formatting function across all rows efficiently.
# The result has a new "text" column with the formatted prompts.

print("Formatting data into Alpaca template...")
formatted_dataset = hf_dataset.map(format_instruction_prompt)


# -- 5. Preview and save ---------------------------------------------------
# save_to_disk writes the dataset as optimized Arrow files that can be
# loaded back with datasets.load_from_disk() for fine-tuning.

print("\n" + "=" * 50)
print("Preview (row 1):")
print("=" * 50)
print(formatted_dataset[0]["text"])
print("=" * 50)

save_path = "./my-custom-alpaca-dataset"
print(f"\nSaving dataset to {save_path}...")
formatted_dataset.save_to_disk(save_path)

print(f"Done. Dataset saved to {save_path}")
