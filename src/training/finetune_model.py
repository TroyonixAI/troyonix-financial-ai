"""
Fine-tune FinBERT on financial data for Troyonix wealth management AI.
Optimized for macOS training with processed training data.

Author: Troyonix AI Team
Date: 2025
"""
import os
import json
import torch
from pathlib import Path
import sys
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional
import platform
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, DataCollatorWithPadding
from datasets import Dataset
import logging
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
import random

# Add src to Python path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config_utils import load_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
try:
    config = load_config()
    MODEL_NAME = config["model"]["base_model"]
    OUTPUT_DIR = config["model"]["output_dir"]
    TRAINING_ARGS = config["model"]["training_args"]
except Exception as e:
    logger.error(f"Error loading configuration: {e}")
    sys.exit(1)

# Constants
TRAINING_DATA_PATH = "data/processed/wealth_data/training_data.csv"
MAX_LENGTH = 512  # FinBERT can handle longer sequences
LABEL_MAPPING = {"negative": 0, "neutral": 1, "positive": 2}

def get_device():
    """Get the appropriate device for training based on system capabilities."""
    if torch.backends.mps.is_available():
        return torch.device("mps")  # Use Metal Performance Shaders on macOS
    elif torch.cuda.is_available():
        return torch.device("cuda")
    else:
        return torch.device("cpu")

def load_training_data() -> pd.DataFrame:
    """Load the processed training data."""
    logger.info(f"Loading training data from {TRAINING_DATA_PATH}")
    
    if not os.path.exists(TRAINING_DATA_PATH):
        raise FileNotFoundError(f"Training data not found at {TRAINING_DATA_PATH}")
    
    df = pd.read_csv(TRAINING_DATA_PATH)
    logger.info(f"Loaded {len(df)} training examples")
    
    # Display data distribution
    logger.info("Data distribution:")
    logger.info(f"  Total examples: {len(df)}")
    logger.info(f"  Label distribution: {df['label'].value_counts().to_dict()}")
    logger.info(f"  Source distribution: {df['source'].value_counts().to_dict()}")
    
    return df

def prepare_dataset(df: pd.DataFrame) -> Tuple[Dataset, Dataset]:
    """Prepare the dataset for training and validation."""
    logger.info("Preparing dataset for training...")
    
    # Convert labels to numeric format
    df['label_id'] = df['label'].map(LABEL_MAPPING)
    
    # Split into train and validation sets
    train_df, val_df = train_test_split(
        df, 
        test_size=0.2, 
        random_state=42, 
        stratify=df['label_id']
    )
    
    logger.info(f"Training set: {len(train_df)} examples")
    logger.info(f"Validation set: {len(val_df)} examples")
    
    # Convert to HuggingFace datasets
    train_dataset = Dataset.from_pandas(train_df)
    val_dataset = Dataset.from_pandas(val_df)
    
    return train_dataset, val_dataset

def preprocess_function(examples: Dict[str, Any], tokenizer: AutoTokenizer) -> Dict[str, Any]:
    """Tokenize and prepare examples for the model."""
    # Tokenize the texts
    tokenized = tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
        return_tensors="pt"
    )
    
    # Remove the batch dimension added by return_tensors="pt"
    for key in tokenized:
        if isinstance(tokenized[key], torch.Tensor):
            tokenized[key] = tokenized[key].squeeze(0)
    
    return tokenized

def compute_metrics(pred):
    """Compute evaluation metrics."""
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    # Calculate metrics
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def finetune_model():
    """Main function to fine-tune the FinBERT model."""
    logger.info("🚀 Starting FinBERT Fine-tuning for Troyonix")
    
    # Log system information
    device = get_device()
    logger.info(f"Using device: {device}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"Python version: {platform.python_version()}")
    
    # Load training data
    df = load_training_data()
    
    # Prepare datasets
    train_dataset, val_dataset = prepare_dataset(df)
    
    # Load tokenizer and model
    logger.info(f"Loading model: {MODEL_NAME}")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, 
        num_labels=len(LABEL_MAPPING)
    )
    
    # Move model to device
    model = model.to(device)
    
    # Tokenize datasets
    logger.info("Tokenizing datasets...")
    
    def tokenize_function(examples):
        return preprocess_function(examples, tokenizer)
    
    train_dataset = train_dataset.map(tokenize_function, batched=True)
    val_dataset = val_dataset.map(tokenize_function, batched=True)
    
    # Set up training arguments
    training_args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        num_train_epochs=TRAINING_ARGS.get("num_train_epochs", 3),
        per_device_train_batch_size=TRAINING_ARGS.get("per_device_train_batch_size", 8),
        per_device_eval_batch_size=TRAINING_ARGS.get("per_device_eval_batch_size", 8),
        gradient_accumulation_steps=TRAINING_ARGS.get("gradient_accumulation_steps", 4),
        learning_rate=TRAINING_ARGS.get("learning_rate", 2e-5),
        weight_decay=TRAINING_ARGS.get("weight_decay", 0.01),
        warmup_steps=TRAINING_ARGS.get("warmup_steps", 100),
        logging_steps=TRAINING_ARGS.get("logging_steps", 50),
        save_steps=TRAINING_ARGS.get("save_steps", 500),
        eval_steps=TRAINING_ARGS.get("eval_steps", 500),
        save_total_limit=TRAINING_ARGS.get("save_total_limit", 2),
        evaluation_strategy="steps",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        greater_is_better=True,
        fp16=TRAINING_ARGS.get("fp16", False),
        use_mps_device=TRAINING_ARGS.get("use_mps_device", True),
        dataloader_num_workers=TRAINING_ARGS.get("dataloader_num_workers", 0),
        dataloader_pin_memory=TRAINING_ARGS.get("dataloader_pin_memory", False),
        report_to=None,  # Disable wandb/tensorboard logging
    )
    
    # Initialize trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )
    
    # Start training
    logger.info("Starting training...")
    trainer.train()
    
    # Evaluate the model
    logger.info("Evaluating model...")
    eval_results = trainer.evaluate()
    
    # Save the final model
    logger.info("Saving model...")
    trainer.save_model()
    tokenizer.save_pretrained(OUTPUT_DIR)
    
    # Save training results
    results = {
        "model_name": MODEL_NAME,
        "training_args": training_args.to_dict(),
        "eval_results": eval_results,
        "label_mapping": LABEL_MAPPING,
        "max_length": MAX_LENGTH,
        "training_data_info": {
            "total_examples": len(df),
            "label_distribution": df['label'].value_counts().to_dict(),
            "source_distribution": df['source'].value_counts().to_dict()
        },
        "training_date": datetime.now().isoformat()
    }
    
    results_path = os.path.join(OUTPUT_DIR, "training_results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info("=== TRAINING COMPLETE ===")
    logger.info(f"Model saved to: {OUTPUT_DIR}")
    logger.info(f"Results saved to: {results_path}")
    logger.info(f"Final evaluation results: {eval_results}")
    
    return results

def main():
    """Main entry point."""
    try:
        results = finetune_model()
        
        # Print summary
        print("\n" + "="*60)
        print("FINBERT FINE-TUNING COMPLETE")
        print("="*60)
        print(f"Model: {results['model_name']}")
        print(f"Output directory: {OUTPUT_DIR}")
        print(f"Training examples: {results['training_data_info']['total_examples']}")
        print(f"Final F1 Score: {results['eval_results']['eval_f1']:.4f}")
        print(f"Final Accuracy: {results['eval_results']['eval_accuracy']:.4f}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise

if __name__ == "__main__":
    main() 