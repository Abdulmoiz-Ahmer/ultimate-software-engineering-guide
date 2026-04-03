# HuggingFace Dataset Prep -- Python

Python implementation using the `datasets` library to format and save training data.

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

The script formats 3 sample examples into Alpaca prompt format, previews the first one, and saves the dataset to `./my-custom-alpaca-dataset/`.

## Output

The saved dataset contains Apache Arrow files that can be loaded back with:

```python
from datasets import load_from_disk
dataset = load_from_disk("./my-custom-alpaca-dataset")
```

## Dependencies

- `datasets` -- HuggingFace Datasets library for creating, transforming, and saving datasets backed by Apache Arrow
