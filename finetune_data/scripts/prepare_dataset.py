import os
import argparse
from llama_index.core import Document
from llama_index.core.node_parser import SimpleNodeParser
from llama_index.core.text_splitter import TokenTextSplitter
from llama_index.readers.file import PDFReader
import json
import re
from typing import Dict, Any

def count_tokens(text: str) -> int:
    """Estimate token count for metrics purposes."""
    # Using llama-index's TokenTextSplitter since we already have it
    splitter = TokenTextSplitter()
    return len(splitter.split_text(text))

def analyze_text_quality(text: str) -> Dict[str, float]:
    """Analyze text quality metrics."""
    total_chars = len(text)
    if total_chars == 0:
        return {
            "alphanumeric_ratio": 0.0,
            "sentence_count": 0,
            "avg_sentence_length": 0.0
        }
    
    alphanumeric_chars = len(re.findall(r'[a-zA-Z0-9]', text))
    sentences = re.split(r'[.!?]+', text)
    valid_sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
    
    return {
        "alphanumeric_ratio": alphanumeric_chars / total_chars,
        "sentence_count": len(valid_sentences),
        "avg_sentence_length": len(text.split()) / len(valid_sentences) if valid_sentences else 0
    }

def clean_chunk(text: str) -> str:
    """Clean up a chunk of text by removing artifacts and normalizing format."""
    # Remove leading page numbers (e.g., "6 ", "12 ", etc.)
    text = text.strip()
    if text and text.split()[0].isdigit():
        text = ' '.join(text.split()[1:])
    
    # Normalize whitespace
    text = ' '.join(text.split())
    
    # Ensure sentences are properly spaced after periods
    text = re.sub(r'\.(?=[A-Z])', '. ', text)
    
    return text

def validate_training_example(example: dict, max_tokens: int = 4096) -> tuple[bool, Dict[str, Any]]:
    """Validate that a training example meets requirements and return quality metrics."""
    try:
        messages = example["messages"]
        if not isinstance(messages, list):
            return False, {}
            
        # Check message sequence
        if len(messages) < 2:  # Must have at least user + assistant
            return False, {}
            
        # If system message exists, must be first
        if messages[0]["role"] == "system":
            messages = messages[1:]  # Skip system for subsequent checks
            
        # Check alternating user/assistant pattern
        for i, msg in enumerate(messages):
            expected_role = "user" if i % 2 == 0 else "assistant"
            if msg["role"] != expected_role:
                return False, {}
        
        # Count total tokens
        total_tokens = sum(count_tokens(msg["content"]) for msg in example["messages"])
        if total_tokens > max_tokens:
            return False, {}
        
        # Analyze text quality of user and assistant messages
        user_text = messages[0]["content"]
        assistant_text = messages[1]["content"]
        
        user_metrics = analyze_text_quality(user_text)
        assistant_metrics = analyze_text_quality(assistant_text)
        
        # Quality thresholds
        if (user_metrics["alphanumeric_ratio"] < 0.7 or 
            assistant_metrics["alphanumeric_ratio"] < 0.7 or
            user_metrics["avg_sentence_length"] < 5 or
            assistant_metrics["avg_sentence_length"] < 5):
            return False, {}
        
        metrics = {
            "total_tokens": total_tokens,
            "user_metrics": user_metrics,
            "assistant_metrics": assistant_metrics
        }
        
        return True, metrics
                
    except (KeyError, IndexError):
        return False, {}

def process_investor_letter(input_file: str, output_dir: str, chunk_size: int = 1024, chunk_overlap: int = 100):
    """
    Process a single investor letter PDF into a format suitable for Fireworks fine-tuning.
    
    Args:
        input_file: Path to the PDF file
        output_dir: Directory for the output JSON file
        chunk_size: Size of text chunks
        chunk_overlap: Overlap between chunks
    """
    # Load document
    print(f"Loading document: {input_file}")
    reader = PDFReader()
    documents = reader.load_data(file=input_file)
    print(f"Loaded document with {len(documents)} pages")
    
    # Filter out unwanted content
    filtered_docs = []
    for i, doc in enumerate(documents, 1):
        text = doc.text.strip()
        # Log what's being filtered
        if not text:
            print(f"Page {i}: Filtered - Empty page")
            continue
        if text.isdigit():
            print(f"Page {i}: Filtered - Only numbers: {text}")
            continue
        if len(text.split()) < 20:
            print(f"Page {i}: Filtered - Too short ({len(text.split())} words): {text[:100]}...")
            continue
        filtered_docs.append(doc)
    
    print(f"Filtered down to {len(filtered_docs)} content pages")
    
    # Parse into nodes (chunks)
    print("Chunking document...")
    text_splitter = TokenTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    parser = SimpleNodeParser()
    nodes = []
    
    for doc in filtered_docs:
        doc_text = clean_chunk(doc.text)  # Clean the text before chunking
        chunks = text_splitter.split_text(doc_text)
        for chunk in chunks:
            # Skip chunks that are too short or too long
            if len(chunk.split()) < 50:
                continue
            chunk = clean_chunk(chunk)  # Clean again after splitting to catch any artifacts
            node = parser.get_nodes_from_documents([Document(text=chunk)])[0]
            nodes.append(node)
    
    print(f"Created {len(nodes)} chunks")
    
    # Prepare training data
    print("Preparing training data...")
    training_data = []
    dataset_metrics = {
        "total_examples": 0,
        "rejected_examples": 0,
        "token_stats": {
            "min": float('inf'),
            "max": 0,
            "total": 0
        },
        "quality_metrics": {
            "avg_alphanumeric_ratio": 0,
            "avg_sentence_length": 0
        }
    }
    
    system_message = (
        "You are an experienced investment manager writing detailed letters to your partners. "
        "Write in a clear, analytical style that combines investment insights with real-world examples. "
        "Focus on long-term value investing principles, careful analysis of businesses, and clear explanations "
        "of your investment decisions. Maintain a thoughtful, personal tone while discussing complex investment concepts."
    )
    
    for i in range(0, len(nodes)-1):
        current_chunk = nodes[i].text
        next_chunk = nodes[i+1].text
        
        # Extract date if present at the start of the chunk
        date_match = re.search(r'^(?:\d{1,2}(?:st|nd|rd|th)?\s+)?(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}', current_chunk)
        date = date_match.group(0) if date_match else None
        
        entry = {
            "messages": [
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": f"Continue writing the investment letter from this point:\n\n{current_chunk}"
                },
                {
                    "role": "assistant",
                    "content": next_chunk
                }
            ],
            "metadata": {
                "date": date,
                "source_file": os.path.basename(input_file),
                "chunk_index": i
            }
        }
        
        # Validate and get metrics
        is_valid, metrics = validate_training_example(entry)
        if is_valid:
            training_data.append(entry)
            dataset_metrics["total_examples"] += 1
            dataset_metrics["token_stats"]["min"] = min(dataset_metrics["token_stats"]["min"], metrics["total_tokens"])
            dataset_metrics["token_stats"]["max"] = max(dataset_metrics["token_stats"]["max"], metrics["total_tokens"])
            dataset_metrics["token_stats"]["total"] += metrics["total_tokens"]
            dataset_metrics["quality_metrics"]["avg_alphanumeric_ratio"] += (metrics["user_metrics"]["alphanumeric_ratio"] + metrics["assistant_metrics"]["alphanumeric_ratio"]) / 2
            dataset_metrics["quality_metrics"]["avg_sentence_length"] += (metrics["user_metrics"]["avg_sentence_length"] + metrics["assistant_metrics"]["avg_sentence_length"]) / 2
        else:
            dataset_metrics["rejected_examples"] += 1
            print(f"Warning: Skipping invalid training example at chunk {i}")
    
    if len(training_data) < 3:
        raise ValueError("Not enough valid training examples. Minimum required is 3.")
    
    # Finalize averages
    total_examples = dataset_metrics["total_examples"]
    dataset_metrics["quality_metrics"]["avg_alphanumeric_ratio"] /= total_examples
    dataset_metrics["quality_metrics"]["avg_sentence_length"] /= total_examples
    dataset_metrics["token_stats"]["avg"] = dataset_metrics["token_stats"]["total"] / total_examples
    
    # Save dataset and metrics
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = os.path.join(output_dir, f"{base_name}_dataset.jsonl")
    metrics_file = os.path.join(output_dir, f"{base_name}_metrics.json")
    
    print(f"Saving {len(training_data)} training examples...")
    with open(output_file, 'w') as f:
        for entry in training_data:
            f.write(json.dumps(entry) + '\n')
            
    with open(metrics_file, 'w') as f:
        json.dump(dataset_metrics, f, indent=2)
    
    print(f"\nDataset Statistics:")
    print(f"- Total examples: {dataset_metrics['total_examples']}")
    print(f"- Rejected examples: {dataset_metrics['rejected_examples']}")
    print(f"- Token stats:")
    print(f"  - Min: {dataset_metrics['token_stats']['min']}")
    print(f"  - Max: {dataset_metrics['token_stats']['max']}")
    print(f"  - Avg: {dataset_metrics['token_stats']['avg']:.1f}")
    print(f"- Quality metrics:")
    print(f"  - Avg alphanumeric ratio: {dataset_metrics['quality_metrics']['avg_alphanumeric_ratio']:.2f}")
    print(f"  - Avg sentence length: {dataset_metrics['quality_metrics']['avg_sentence_length']:.1f}")
    
    print(f"\nProcessing complete. Files saved:")
    print(f"- Dataset: {output_file}")
    print(f"- Metrics: {metrics_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process an investor letter PDF for fine-tuning')
    parser.add_argument('input_file', help='Path to the PDF file to process')
    parser.add_argument('--chunk-size', type=int, default=1024, help='Size of text chunks')
    parser.add_argument('--chunk-overlap', type=int, default=100, help='Overlap between chunks')
    
    args = parser.parse_args()
    
    # Set paths relative to data_prep directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_dir = os.path.join(base_dir, "processed")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process the document
    process_investor_letter(
        input_file=args.input_file,
        output_dir=output_dir,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap
    ) 