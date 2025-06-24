"""
Download and process Federal Reserve Economic Data (FRED) for model enrichment.
Transforms numerical economic data into meaningful text descriptions.
"""
import os
import json
import requests
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import sys
from typing import Dict, List, Any, Optional

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.config_utils import load_config
from src.utils.file_utils import save_text, ensure_directory

# Load configuration
config = load_config()
FRED_API_KEY = config["api_keys"]["fred"]

# FRED API base URL
FRED_BASE_URL = "https://api.stlouisfed.org/fred"

# Key economic indicators to track
ECONOMIC_INDICATORS = {
    "GDP": {
        "series_id": "GDP",
        "name": "Gross Domestic Product",
        "frequency": "quarterly",
        "description": "The total value of goods and services produced in the US"
    },
    "CPI": {
        "series_id": "CPIAUCSL",
        "name": "Consumer Price Index",
        "frequency": "monthly", 
        "description": "Measures inflation by tracking changes in consumer prices"
    },
    "UNEMPLOYMENT": {
        "series_id": "UNRATE",
        "name": "Unemployment Rate",
        "frequency": "monthly",
        "description": "Percentage of the labor force that is unemployed"
    },
    "FEDERAL_FUNDS_RATE": {
        "series_id": "FEDFUNDS",
        "name": "Federal Funds Rate",
        "frequency": "monthly",
        "description": "The interest rate at which banks lend to each other overnight"
    },
    "CONSUMER_SENTIMENT": {
        "series_id": "UMCSENT",
        "name": "University of Michigan Consumer Sentiment",
        "frequency": "monthly",
        "description": "Measures consumer confidence and economic outlook"
    },
    "MANUFACTURING_PMI": {
        "series_id": "NAPM",
        "name": "ISM Manufacturing PMI",
        "frequency": "monthly",
        "description": "Purchasing Managers Index indicating manufacturing sector health"
    }
}

def get_fred_data(series_id: str, limit: int = 24) -> Optional[Dict[str, Any]]:
    """
    Fetch data for a specific FRED series.
    
    Args:
        series_id: The FRED series ID
        limit: Number of most recent observations to fetch
        
    Returns:
        Dictionary containing series metadata and observations
    """
    url = f"{FRED_BASE_URL}/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "limit": limit,
        "sort_order": "desc"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {series_id}: {e}")
        return None

def get_series_info(series_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch metadata for a FRED series.
    
    Args:
        series_id: The FRED series ID
        
    Returns:
        Dictionary containing series metadata
    """
    url = f"{FRED_BASE_URL}/series"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("seriess", [{}])[0] if data.get("seriess") else None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching series info for {series_id}: {e}")
        return None

def transform_to_text(series_data: Dict[str, Any], series_info: Dict[str, Any], indicator_config: Dict[str, str]) -> List[str]:
    """
    Transform numerical economic data into meaningful text descriptions.
    
    Args:
        series_data: Raw FRED data
        series_info: Series metadata
        indicator_config: Configuration for this indicator
        
    Returns:
        List of text descriptions for model training
    """
    texts = []
    
    if not series_data or "observations" not in series_data:
        return texts
    
    observations = series_data["observations"]
    if not observations:
        return texts
    
    # Get the most recent observations for analysis
    recent_obs = observations[:12]  # Last 12 observations
    
    # Calculate basic statistics
    values = []
    dates = []
    for obs in recent_obs:
        try:
            value = float(obs["value"])
            values.append(value)
            dates.append(obs["date"])
        except (ValueError, KeyError):
            continue
    
    if len(values) < 2:
        return texts
    
    # Calculate trends
    current_value = values[0]
    previous_value = values[1] if len(values) > 1 else current_value
    change = current_value - previous_value
    change_percent = (change / previous_value * 100) if previous_value != 0 else 0
    
    # Determine trend direction
    if change > 0:
        trend = "increased"
        sentiment = "positive"
    elif change < 0:
        trend = "decreased"
        sentiment = "negative"
    else:
        trend = "remained stable"
        sentiment = "neutral"
    
    # Create contextual text descriptions
    indicator_name = indicator_config["name"]
    description = indicator_config["description"]
    
    # Current status text
    current_text = f"The {indicator_name} is currently {current_value:.2f}. {description}. "
    current_text += f"This represents a {trend} from the previous period."
    
    # Trend analysis text
    trend_text = f"Economic indicator analysis: {indicator_name} has {trend} by {abs(change):.2f} "
    trend_text += f"({abs(change_percent):.1f}%) from the previous measurement period. "
    trend_text += f"This {sentiment} movement suggests {'improving' if sentiment == 'positive' else 'declining' if sentiment == 'negative' else 'stable'} economic conditions."
    
    # Historical context text
    if len(values) >= 4:
        avg_value = sum(values[:4]) / 4  # Average of last 4 periods
        if current_value > avg_value * 1.05:
            context = "above recent historical levels"
        elif current_value < avg_value * 0.95:
            context = "below recent historical levels"
        else:
            context = "in line with recent historical levels"
        
        context_text = f"The current {indicator_name} reading of {current_value:.2f} is {context}, "
        context_text += f"compared to the recent average of {avg_value:.2f}."
    else:
        context_text = f"The {indicator_name} shows a current reading of {current_value:.2f}."
    
    texts.extend([current_text, trend_text, context_text])
    
    return texts

def download_fred_data():
    """
    Download and process FRED economic data for model enrichment.
    """
    print("--- Starting FRED Economic Data Download ---")
    
    # Ensure output directory exists
    output_dir = "data/raw/wealth_data/fred_data"
    ensure_directory(output_dir)
    
    all_texts = []
    
    for indicator_key, config in ECONOMIC_INDICATORS.items():
        print(f"\nProcessing {config['name']} ({config['series_id']})...")
        
        # Get series metadata
        series_info = get_series_info(config['series_id'])
        if not series_info:
            print(f"  Could not fetch metadata for {config['series_id']}")
            continue
        
        # Get series data
        series_data = get_fred_data(config['series_id'])
        if not series_data:
            print(f"  Could not fetch data for {config['series_id']}")
            continue
        
        # Transform to text
        texts = transform_to_text(series_data, series_info, config)
        
        if texts:
            # Save individual indicator data
            indicator_file = os.path.join(output_dir, f"{indicator_key.lower()}_data.json")
            with open(indicator_file, 'w') as f:
                json.dump({
                    "indicator": config,
                    "series_info": series_info,
                    "series_data": series_data,
                    "text_descriptions": texts
                }, f, indent=2)
            
            all_texts.extend(texts)
            print(f"  Generated {len(texts)} text descriptions")
        else:
            print(f"  No text descriptions generated for {config['series_id']}")
        
        # Respect rate limits
        import time
        time.sleep(0.1)
    
    # Save all texts in a format compatible with our training pipeline
    if all_texts:
        combined_file = os.path.join(output_dir, "combined_economic_context.txt")
        with open(combined_file, 'w') as f:
            for text in all_texts:
                f.write(text + "\n\n")
        
        print(f"\n--- FRED Data Download Complete ---")
        print(f"Total text descriptions generated: {len(all_texts)}")
        print(f"Data saved to: {output_dir}")
        print(f"Combined text file: {combined_file}")
    else:
        print("\n--- No FRED data was successfully processed ---")

if __name__ == "__main__":
    download_fred_data() 