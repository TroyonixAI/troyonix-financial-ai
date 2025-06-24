"""
Analyze sentiment distribution in the financial dataset.
"""
import os
import json
from collections import Counter
from pathlib import Path
import sys

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))
from src.utils.config_utils import load_config

def load_json_files(directory):
    """Load all JSON files from a directory."""
    data = []
    for file in os.listdir(directory):
        if file.endswith('.json'):
            with open(os.path.join(directory, file), 'r', encoding='utf-8') as f:
                try:
                    data.append(json.load(f))
                except json.JSONDecodeError:
                    print(f"Error reading {file}")
    return data

def analyze_sentiment_distribution():
    """Analyze sentiment distribution across different data sources."""
    # Load configuration
    config = load_config()
    
    # Define data directories
    base_dir = "data/raw/wealth_data"
    sources = {
        "sec_filings": os.path.join(base_dir, "sec_filings"),
    }
    
    # Sentiment mapping
    sentiment_map = {0: "negative", 1: "neutral", 2: "positive"}
    
    # Analyze each source
    for source_name, directory in sources.items():
        print(f"\nAnalyzing {source_name} data...")
        
        # Load data from JSON file
        with open(os.path.join(directory, "sentiment_analysis.json"), "r") as f:
            data = json.load(f)
        
        for item in data:
            if isinstance(item, dict):
                # Extract text based on source
                if source_name == "sec_filings":
                    text = item.get('text', '')
                
                # Extract sentiment if available
                sentiment = item.get('sentiment', 'unknown')
                if isinstance(sentiment, int) and sentiment in sentiment_map:
                    sentiment = sentiment_map[sentiment]
                
                if text:
                    texts.append(text)
                    sentiments.append(sentiment)
        
        # Print statistics
        print(f"Total documents: {len(texts)}")
        sentiment_counts = Counter(sentiments)
        print("Sentiment distribution:")
        for sentiment, count in sentiment_counts.most_common():
            print(f"  {sentiment}: {count} ({count/len(sentiments)*100:.1f}%)")
        
        # Print sample texts for each sentiment
        print("\nSample texts for each sentiment:")
        for sentiment in sentiment_counts.keys():
            sample_texts = [text for text, sent in zip(texts, sentiments) if sent == sentiment][:2]
            print(f"\n{sentiment.upper()} samples:")
            for text in sample_texts:
                print(f"  - {text[:200]}...")

if __name__ == "__main__":
    analyze_sentiment_distribution() 