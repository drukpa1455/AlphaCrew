# Fine-tuning Dataset Preparation

This directory contains tools for preparing training datasets for Fireworks AI fine-tuning. Currently focused on processing investment letters into the required JSONL format.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Directory Structure

```
finetune_data/
├── README.md              # This file
├── requirements.txt       # Project dependencies
├── raw/                  # Raw input files (e.g., investor letter PDFs)
├── processed/            # Output JSONL datasets and metrics
└── scripts/              
    └── prepare_dataset.py # Dataset preparation script
```

## Features

### Dataset Preparation
- Process investment letters into training data
- Convert PDFs to structured text
- Generate training examples in JSONL format
- Validate token counts and data quality

## Usage

1. Place your input PDFs in the `raw/` directory

2. Run the processing script:
```bash
python scripts/prepare_dataset.py raw/your_file.pdf
```

3. Find the processed outputs in `processed/`:
   - `*_dataset.jsonl`: The training dataset
   - `*_metrics.json`: Dataset quality metrics

## Output Format

The script creates a JSONL dataset following the Fireworks chat fine-tuning format. Each line contains a JSON object with:

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are an experienced investment manager..."
    },
    {
      "role": "user",
      "content": "Continue writing the investment letter from this point:\n\n..."
    },
    {
      "role": "assistant",
      "content": "..."
    }
  ],
  "metadata": {
    "date": "January 2002",
    "source_file": "example.pdf",
    "chunk_index": 0
  }
}
```

## Quality Controls
- Token count validation for model compatibility
- Text quality metrics (alphanumeric ratio, sentence length)
- Content validation
- Proper chunking with context overlap

## Customization

You can modify the processing by passing arguments:
```bash
python scripts/prepare_dataset.py raw/your_file.pdf --chunk-size 1024 --chunk-overlap 100
```

Key parameters:
- `chunk-size`: Size of text chunks (default: 1024)
- `chunk-overlap`: Overlap between chunks (default: 100)

Additional customization can be done in `scripts/prepare_dataset.py`:
- System message content
- Quality thresholds
- Validation rules
- Output format 