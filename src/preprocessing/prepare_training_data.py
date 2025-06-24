#!/usr/bin/env python3
"""
Prepare training data for FinBERT fine-tuning from collected sources.
Transforms raw data into training-ready format with proper labeling.

Author: Troyonix AI Team
Date: 2025
"""

import os
import sys
import json
import logging
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Tuple
import re
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.config_utils import load_config
from src.utils.file_utils import ensure_directory

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TrainingDataPreparer:
    def __init__(self):
        self.config = load_config()
        
        # Input directories
        self.input_dirs = {
            'sec_filings': 'data/raw/wealth_data/sec_filings',
            'fred_data': 'data/raw/wealth_data/fred_data',
            'policy_uncertainty': 'data/raw/wealth_data/policy_uncertainty'
        }
        
        # Output directory
        self.output_dir = 'data/processed/wealth_data'
        ensure_directory(self.output_dir)
        
        # Training data containers
        self.training_data = []
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text for training"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that might interfere with tokenization
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}]', ' ', text)
        
        # Normalize quotes and dashes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace('–', '-').replace('—', '-')
        
        # Remove HTML-like tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Limit text length (FinBERT has token limits)
        if len(text) > 5000:
            text = text[:5000] + "..."
        
        return text.strip()
    
    def extract_sentiment_from_sec_filing(self, content: str, form_type: str) -> Tuple[str, str]:
        """
        Extract sentiment from SEC filing content.
        Returns (cleaned_text, sentiment_label)
        """
        # Clean the content
        cleaned_content = self.clean_text(content)
        
        # Simple sentiment analysis based on form type and content keywords
        # This is a basic heuristic - in production, you might use a more sophisticated approach
        
        positive_keywords = [
            'increase', 'growth', 'improve', 'positive', 'strong', 'profit', 'revenue',
            'success', 'gain', 'up', 'higher', 'better', 'excellent', 'outperform'
        ]
        
        negative_keywords = [
            'decrease', 'decline', 'loss', 'negative', 'weak', 'risk', 'challenge',
            'down', 'lower', 'worse', 'poor', 'underperform', 'volatility'
        ]
        
        # Count keyword occurrences
        content_lower = cleaned_content.lower()
        positive_count = sum(1 for word in positive_keywords if word in content_lower)
        negative_count = sum(1 for word in negative_keywords if word in content_lower)
        
        # Determine sentiment based on form type and keyword analysis
        if form_type == "10-K":
            # Annual reports are generally neutral/informational
            sentiment = "neutral"
        elif form_type == "10-Q":
            # Quarterly reports can be more dynamic
            if positive_count > negative_count + 2:
                sentiment = "positive"
            elif negative_count > positive_count + 2:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        elif form_type == "8-K":
            # Current reports often contain significant events
            if positive_count > negative_count:
                sentiment = "positive"
            elif negative_count > positive_count:
                sentiment = "negative"
            else:
                sentiment = "neutral"
        else:
            sentiment = "neutral"
        
        return cleaned_content, sentiment
    
    def process_sec_filings(self) -> int:
        """Process SEC filings and extract training examples"""
        logger.info("Processing SEC filings...")
        
        sec_dir = Path(self.input_dirs['sec_filings'])
        if not sec_dir.exists():
            logger.warning("SEC filings directory not found")
            return 0
        
        processed_count = 0
        
        for filing_file in sec_dir.glob('*.txt'):
            try:
                # Parse filename to extract metadata
                filename = filing_file.stem
                parts = filename.split('_')
                
                if len(parts) >= 3:
                    accession_number = parts[0]
                    form_type = parts[1]
                    filing_date = parts[2]
                    
                    # Read filing content
                    with open(filing_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract sentiment and clean text
                    cleaned_text, sentiment = self.extract_sentiment_from_sec_filing(content, form_type)
                    
                    if cleaned_text and len(cleaned_text) > 100:  # Minimum length threshold
                        training_example = {
                            'text': cleaned_text,
                            'label': sentiment,
                            'source': 'sec_filing',
                            'metadata': {
                                'accession_number': accession_number,
                                'form_type': form_type,
                                'filing_date': filing_date,
                                'filename': filename
                            }
                        }
                        
                        self.training_data.append(training_example)
                        processed_count += 1
                        
                        if processed_count % 10 == 0:
                            logger.info(f"Processed {processed_count} SEC filings...")
                
            except Exception as e:
                logger.error(f"Error processing {filing_file}: {e}")
                continue
        
        logger.info(f"Completed SEC filings processing: {processed_count} examples")
        return processed_count
    
    def process_fred_data(self) -> int:
        """Process FRED economic data and extract training examples"""
        logger.info("Processing FRED economic data...")
        
        fred_dir = Path(self.input_dirs['fred_data'])
        if not fred_dir.exists():
            logger.warning("FRED data directory not found")
            return 0
        
        processed_count = 0
        
        # Process combined economic context file
        combined_file = fred_dir / "combined_economic_context.txt"
        if combined_file.exists():
            try:
                with open(combined_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Split into individual descriptions
                descriptions = [desc.strip() for desc in content.split('\n\n') if desc.strip()]
                
                for desc in descriptions:
                    cleaned_text = self.clean_text(desc)
                    
                    if cleaned_text and len(cleaned_text) > 50:
                        # Economic data is generally neutral/informational
                        training_example = {
                            'text': cleaned_text,
                            'label': 'neutral',
                            'source': 'fred_data',
                            'metadata': {
                                'data_type': 'economic_indicator',
                                'description_length': len(cleaned_text)
                            }
                        }
                        
                        self.training_data.append(training_example)
                        processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing FRED combined file: {e}")
        
        logger.info(f"Completed FRED data processing: {processed_count} examples")
        return processed_count
    
    def process_policy_uncertainty(self) -> int:
        """Process policy uncertainty data and extract training examples"""
        logger.info("Processing policy uncertainty data...")
        
        policy_dir = Path(self.input_dirs['policy_uncertainty'])
        if not policy_dir.exists():
            logger.warning("Policy uncertainty directory not found")
            return 0
        
        processed_count = 0
        
        # Process JSON files containing policy context
        for json_file in policy_dir.glob('*.json'):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract text descriptions if available
                if 'text_descriptions' in data:
                    for desc in data['text_descriptions']:
                        cleaned_text = self.clean_text(desc)
                        
                        if cleaned_text and len(cleaned_text) > 50:
                            # Policy uncertainty data is generally neutral
                            training_example = {
                                'text': cleaned_text,
                                'label': 'neutral',
                                'source': 'policy_uncertainty',
                                'metadata': {
                                    'data_type': 'policy_uncertainty',
                                    'filename': json_file.name
                                }
                            }
                            
                            self.training_data.append(training_example)
                            processed_count += 1
                
            except Exception as e:
                logger.error(f"Error processing {json_file}: {e}")
                continue
        
        logger.info(f"Completed policy uncertainty processing: {processed_count} examples")
        return processed_count
    
    def create_training_dataset(self) -> pd.DataFrame:
        """Create final training dataset"""
        logger.info("Creating final training dataset...")
        
        # Convert to DataFrame
        df = pd.DataFrame(self.training_data)
        
        if df.empty:
            logger.warning("No training data was created")
            return df
        
        # Add dataset metadata
        df['created_at'] = datetime.now().isoformat()
        df['dataset_version'] = '1.0'
        
        # Ensure we have the required columns for FinBERT
        required_columns = ['text', 'label']
        for col in required_columns:
            if col not in df.columns:
                logger.error(f"Missing required column: {col}")
                return pd.DataFrame()
        
        # Remove duplicates
        initial_count = len(df)
        df = df.drop_duplicates(subset=['text'])
        final_count = len(df)
        
        if initial_count != final_count:
            logger.info(f"Removed {initial_count - final_count} duplicate entries")
        
        # Label distribution
        label_counts = df['label'].value_counts()
        logger.info("Label distribution:")
        for label, count in label_counts.items():
            logger.info(f"  {label}: {count} ({count/len(df)*100:.1f}%)")
        
        return df
    
    def save_training_data(self, df: pd.DataFrame) -> str:
        """Save training data in multiple formats"""
        if df.empty:
            logger.warning("No data to save")
            return ""
        
        # Save as CSV
        csv_path = os.path.join(self.output_dir, 'training_data.csv')
        df.to_csv(csv_path, index=False)
        
        # Save as JSON (for HuggingFace datasets)
        json_path = os.path.join(self.output_dir, 'training_data.json')
        df.to_json(json_path, orient='records', indent=2)
        
        # Save metadata
        metadata = {
            'total_examples': len(df),
            'label_distribution': df['label'].value_counts().to_dict(),
            'source_distribution': df['source'].value_counts().to_dict(),
            'created_at': datetime.now().isoformat(),
            'dataset_version': '1.0'
        }
        
        metadata_path = os.path.join(self.output_dir, 'dataset_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Training data saved:")
        logger.info(f"  CSV: {csv_path}")
        logger.info(f"  JSON: {json_path}")
        logger.info(f"  Metadata: {metadata_path}")
        
        return csv_path
    
    def run_preprocessing(self) -> Dict[str, Any]:
        """Run the complete preprocessing pipeline"""
        logger.info("🚀 Starting Training Data Preparation")
        
        # Process each data source
        counts = {
            'sec_filings': self.process_sec_filings(),
            'fred_data': self.process_fred_data(),
            'policy_uncertainty': self.process_policy_uncertainty()
        }
        
        # Create final dataset
        df = self.create_training_dataset()
        
        # Save data
        output_path = self.save_training_data(df)
        
        # Summary
        total_examples = len(df)
        logger.info("=== PREPROCESSING COMPLETE ===")
        logger.info(f"Total training examples: {total_examples}")
        logger.info(f"SEC filings processed: {counts['sec_filings']}")
        logger.info(f"FRED data processed: {counts['fred_data']}")
        logger.info(f"Policy uncertainty processed: {counts['policy_uncertainty']}")
        
        return {
            'total_examples': total_examples,
            'counts': counts,
            'output_path': output_path,
            'label_distribution': df['label'].value_counts().to_dict() if not df.empty else {}
        }

def main():
    """Main entry point"""
    preparer = TrainingDataPreparer()
    results = preparer.run_preprocessing()
    
    # Print summary
    print("\n" + "="*60)
    print("TRAINING DATA PREPARATION COMPLETE")
    print("="*60)
    print(f"Total training examples: {results['total_examples']}")
    print(f"SEC filings: {results['counts']['sec_filings']}")
    print(f"FRED data: {results['counts']['fred_data']}")
    print(f"Policy uncertainty: {results['counts']['policy_uncertainty']}")
    
    if results['label_distribution']:
        print("\nLabel distribution:")
        for label, count in results['label_distribution'].items():
            percentage = (count / results['total_examples']) * 100
            print(f"  {label}: {count} ({percentage:.1f}%)")
    
    print(f"\nOutput saved to: {results['output_path']}")
    print("="*60)

if __name__ == "__main__":
    main() 