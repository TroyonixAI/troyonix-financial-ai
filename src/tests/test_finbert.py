import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_finbert_model_loading():
    """Test that the fine-tuned FinBERT model can be loaded."""
    logger.info("Testing if fine-tuned FinBERT model loads correctly...")
    
    # Path to the fine-tuned model
    model_path = "data/finetuned_models/financial_llm"
    
    # Check if the model directory exists
    if not Path(model_path).exists():
        logger.warning(f"Model directory not found at {model_path}. Skipping test.")
        return

    try:
        # Load fine-tuned model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSequenceClassification.from_pretrained(model_path)
        logger.info("Model and tokenizer loaded successfully!")
        
        # Check if MPS (Apple Silicon) is available and move model to device
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        logger.info(f"Using device: {device}")
        model.to(device)
        logger.info(f"Model moved to {device} successfully.")

    except Exception as e:
        logger.error(f"Failed to load the model or move it to the device: {e}")
        assert False, f"Model loading failed: {e}"

if __name__ == "__main__":
    test_finbert_model_loading() 