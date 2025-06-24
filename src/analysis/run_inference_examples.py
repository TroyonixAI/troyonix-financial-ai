"""
Run inference on a few example financial texts to demonstrate the model's capabilities.
"""
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path
import sys

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

def load_model_and_tokenizer():
    """Load the fine-tuned model and tokenizer."""
    model_path = "data/finetuned_models/financial_llm"
    if not os.path.exists(model_path):
        print(f"Error: Model not found at {model_path}")
        print("Please run the training script first: python src/training/train_finbert.py")
        sys.exit(1)
        
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return model, tokenizer

def predict_sentiment(text, model, tokenizer):
    """Predict sentiment for a given text."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    sentiment_idx = predictions.argmax().item()
    confidence = predictions[0][sentiment_idx].item()
    
    # Map index to sentiment label from the model's config
    sentiment_map = model.config.id2label
    return sentiment_map[sentiment_idx], confidence

def run_inference_examples():
    """Run inference on a few examples from different SEC filing sections."""
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer()
    
    # Test cases from SEC filings
    test_cases = {
        "Positive Examples": [
            "Net sales for the third quarter increased by 15% compared to the same period last year, primarily due to strong demand for our new product line.",
            "On June 1, 2025, we completed the acquisition of a leading competitor, which is expected to be accretive to earnings.",
            "We entered into a new credit facility that provides us with increased financial flexibility."
        ],
        "Negative Examples": [
            "Our operations are subject to intense competition, and we may not be able to compete effectively.",
            "We face significant risks associated with cybersecurity incidents, which could harm our business.",
            "Our operating margin decreased from 25% to 22% due to increased raw material costs and supply chain disruptions."
        ],
        "Neutral Examples": [
            "The company announced the departure of its Chief Financial Officer, effective immediately.",
            "We anticipate that capital expenditures for the remainder of the year will be approximately $50 million.",
            "The company will hold its annual general meeting on October 25th."
        ]
    }
    
    # Test each category
    print("="*50)
    print("Running Inference Examples")
    print("="*50)
    for category, texts in test_cases.items():
        print(f"\n--- {category} ---")
        for text in texts:
            sentiment, confidence = predict_sentiment(text, model, tokenizer)
            print(f"\nText: {text}")
            print(f"Predicted: {sentiment.upper()} (Confidence: {confidence:.2%})")
    print("\n" + "="*50)


if __name__ == "__main__":
    run_inference_examples() 