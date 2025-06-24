"""
Evaluate the fine-tuned model's performance on a labeled dataset of financial texts.
"""
import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from pathlib import Path
import sys
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config_utils import load_config

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

def predict(texts, model, tokenizer):
    """Predict sentiment for a list of texts."""
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    return predictions.argmax(dim=-1)

def evaluate_model_performance():
    """
    Test model performance on a labeled dataset of financial texts.
    
    NOTE: This is a small, example dataset. For a robust evaluation, you should
    use a larger, more diverse, and standardized test set like the Financial PhraseBank
    or create your own high-quality labeled dataset.
    """
    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer()
    
    # Example labeled test set (text, label_index)
    # 0: positive, 1: negative, 2: neutral
    test_data = [
        ("The company reported a significant increase in quarterly profits.", 0),
        ("Our revenue grew by 25% year-over-year, exceeding all expectations.", 0),
        ("The new product launch was a resounding success with customers.", 0),
        
        ("The firm is facing litigation that could result in substantial fines.", 1),
        ("A decline in consumer spending has negatively impacted our sales.", 1),
        ("We have decided to close down our underperforming international division.", 1),
        
        ("The board of directors will hold their annual meeting next Tuesday.", 2),
        ("This report was prepared in accordance with generally accepted accounting principles.", 2),
        ("The company's stock price remained unchanged at the close of trading.", 2),
    ]
    
    texts = [item[0] for item in test_data]
    true_labels = [item[1] for item in test_data]
    
    # Get model predictions
    predicted_labels = predict(texts, model, tokenizer)
    
    # Calculate metrics
    precision, recall, f1, _ = precision_recall_fscore_support(true_labels, predicted_labels, average='weighted')
    accuracy = accuracy_score(true_labels, predicted_labels)
    
    # Print results
    print("="*50)
    print("Model Performance Evaluation")
    print("="*50)
    print(f"Accuracy: {accuracy:.2%}")
    print(f"Precision: {precision:.2%}")
    print(f"Recall: {recall:.2%}")
    print(f"F1-Score: {f1:.2%}")
    print("\nNote: These results are based on a small example dataset.")
    print("For a true measure of performance, a larger labeled test set is required.")
    print("="*50)

if __name__ == "__main__":
    evaluate_model_performance() 