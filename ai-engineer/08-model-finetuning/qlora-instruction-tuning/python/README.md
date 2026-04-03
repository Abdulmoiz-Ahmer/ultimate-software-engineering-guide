# QLoRA Instruction Tuning -- Python

Python implementation using HuggingFace Transformers, PEFT, and TRL.

## Prerequisites

- The dataset from [huggingface-dataset-prep](../../huggingface-dataset-prep/python/) must be built first. Copy or symlink the `my-custom-alpaca-dataset/` folder into this directory.
- A GPU is recommended (NVIDIA with CUDA). CPU works but will be very slow.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

The script downloads TinyLlama 1.1B, attaches a LoRA adapter, trains for 20 steps, and saves the adapter to `./my-trained-lora-adapter/`.

## Output

- `./results/` -- training checkpoints and logs
- `./my-trained-lora-adapter/` -- the trained LoRA adapter weights (a few MB)

To use the adapter later:

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

base_model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
model = PeftModel.from_pretrained(base_model, "./my-trained-lora-adapter")
```

## Dependencies

- `torch` -- PyTorch backend
- `transformers` -- model loading, tokenizer, training arguments
- `peft` -- LoRA adapter creation and management
- `trl` -- SFTTrainer for supervised fine-tuning
- `accelerate` -- device placement and distributed training
- `bitsandbytes` -- 8-bit optimizer support
- `datasets` -- loading the Alpaca-formatted dataset
