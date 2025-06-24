#!/usr/bin/env python3
"""
Download Economic Policy Uncertainty (EPU) indices from FRED API.
These indices quantify policy uncertainty that affects financial markets.

This script downloads:
- US Economic Policy Uncertainty Index (Daily and Monthly)
- Global Economic Policy Uncertainty Index
- Monetary Policy Uncertainty Index
- Policy uncertainty indices for major economies

Author: Troyonix AI Team
Date: 2025
"""

import requests
import json
import pandas as pd
import os
import time
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PolicyUncertaintyDownloader:
    def __init__(self):
        # Load configuration
        self.config = self.load_config()
        self.api_key = self.config.get('api_keys', {}).get('fred')
        
        if not self.api_key:
            raise ValueError("FRED API key not found in config.json under api_keys.fred")
        
        # Create output directory
        self.output_dir = Path("data/raw/wealth_data/policy_uncertainty")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Define the EPU series to download
        self.epu_series = {
            'USEPUINDXD': {
                'name': 'US_Economic_Policy_Uncertainty_Daily',
                'description': 'Daily US Economic Policy Uncertainty Index based on newspaper coverage'
            },
            'USEPUINDXM': {
                'name': 'US_Economic_Policy_Uncertainty_Monthly', 
                'description': 'Monthly US Economic Policy Uncertainty Index'
            },
            'GEPUCURRENT': {
                'name': 'Global_Economic_Policy_Uncertainty',
                'description': 'Global Economic Policy Uncertainty Index (GDP-weighted average of 20 countries)'
            },
            'EPUMONETARY': {
                'name': 'Monetary_Policy_Uncertainty',
                'description': 'Economic Policy Uncertainty Index: Monetary Policy Category'
            },
            'GEPUWEIGHTS': {
                'name': 'Global_EPU_Weights',
                'description': 'Global Economic Policy Uncertainty Index: Weights'
            }
        }

    def load_config(self):
        """Load configuration from config.json"""
        config_path = Path("config/config.json")
        if config_path.exists():
            with open(config_path, 'r') as f:
                return json.load(f)
        else:
            raise FileNotFoundError("config.json not found")

    def fetch_series_data(self, series_id):
        """Fetch data for a specific FRED series"""
        url = f"https://api.stlouisfed.org/fred/series/observations"
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json',
            'sort_order': 'desc'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'observations' in data:
                return data['observations']
            else:
                logger.error(f"No observations found for series {series_id}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data for series {series_id}: {str(e)}")
            return []

    def fetch_series_info(self, series_id):
        """Fetch metadata for a specific FRED series"""
        url = f"https://api.stlouisfed.org/fred/series"
        params = {
            'series_id': series_id,
            'api_key': self.api_key,
            'file_type': 'json'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if 'seriess' in data and data['seriess']:
                return data['seriess'][0]
            else:
                logger.error(f"No series info found for {series_id}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching series info for {series_id}: {str(e)}")
            return None

    def process_series_data(self, series_id, series_name, observations):
        """Process and save series data"""
        if not observations:
            logger.warning(f"No data to process for {series_id}")
            return None
        
        # Convert to DataFrame
        df = pd.DataFrame(observations)
        
        # Convert date and value columns
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        
        # Remove rows with missing values
        df = df.dropna(subset=['value'])
        
        # Sort by date
        df = df.sort_values('date')
        
        # Add metadata
        df['series_id'] = series_id
        df['series_name'] = series_name
        
        return df

    def generate_policy_context(self, df, series_info):
        """Generate human-readable policy context from the data"""
        if df.empty:
            return []
        
        context_descriptions = []
        
        # Get the most recent value
        latest = df.iloc[-1]
        latest_value = latest['value']
        latest_date = latest['date'].strftime('%Y-%m-%d')
        
        # Get the previous value for comparison
        if len(df) > 1:
            previous = df.iloc[-2]
            previous_value = previous['value']
            change = latest_value - previous_value
            change_percent = (change / previous_value) * 100 if previous_value != 0 else 0
            
            # Determine trend
            if change > 0:
                trend = "increased"
                direction = "higher"
            elif change < 0:
                trend = "decreased"
                direction = "lower"
            else:
                trend = "remained unchanged"
                direction = "stable"
            
            # Generate description
            description = (
                f"As of {latest_date}, the {series_info.get('title', 'Policy Uncertainty Index')} "
                f"stands at {latest_value:.2f}, which has {trend} by {abs(change):.2f} points "
                f"({abs(change_percent):.1f}%) from the previous reading. "
                f"This indicates {direction} policy uncertainty in the market."
            )
        else:
            description = (
                f"As of {latest_date}, the {series_info.get('title', 'Policy Uncertainty Index')} "
                f"stands at {latest_value:.2f}. This represents the current level of policy uncertainty."
            )
        
        context_descriptions.append(description)
        
        # Add historical context if available
        if len(df) >= 12:  # At least a year of data
            year_ago = df.iloc[-12]
            year_ago_value = year_ago['value']
            year_change = latest_value - year_ago_value
            year_change_percent = (year_change / year_ago_value) * 100 if year_ago_value != 0 else 0
            
            if abs(year_change_percent) > 10:  # Significant change
                year_description = (
                    f"Compared to one year ago, policy uncertainty has "
                    f"{'increased' if year_change > 0 else 'decreased'} by {abs(year_change_percent):.1f}%, "
                    f"indicating a {'more' if year_change > 0 else 'less'} uncertain policy environment."
                )
                context_descriptions.append(year_description)
        
        return context_descriptions

    def download_all_series(self):
        """Download all EPU series"""
        logger.info("--- Starting Policy Uncertainty Data Download ---")
        
        all_data = []
        all_context = []
        
        for series_id, series_config in self.epu_series.items():
            logger.info(f"Processing {series_config['name']} ({series_id})...")
            
            # Fetch series info
            series_info = self.fetch_series_info(series_id)
            if not series_info:
                logger.warning(f"Could not fetch info for {series_id}, skipping...")
                continue
            
            # Fetch series data
            observations = self.fetch_series_data(series_id)
            if not observations:
                logger.warning(f"Could not fetch data for {series_id}, skipping...")
                continue
            
            # Process data
            df = self.process_series_data(series_id, series_config['name'], observations)
            if df is not None and not df.empty:
                all_data.append(df)
                
                # Generate context
                context = self.generate_policy_context(df, series_info)
                all_context.extend(context)
                
                logger.info(f"  Generated {len(context)} context descriptions")
            
            # Rate limiting
            time.sleep(1)
        
        # Combine all data
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Save raw data
            csv_path = self.output_dir / "policy_uncertainty_data.csv"
            combined_df.to_csv(csv_path, index=False)
            logger.info(f"Raw data saved to: {csv_path}")
            
            # Save context descriptions
            context_path = self.output_dir / "policy_uncertainty_context.json"
            with open(context_path, 'w') as f:
                json.dump(all_context, f, indent=2)
            logger.info(f"Context descriptions saved to: {context_path}")
            
            # Create summary
            summary = {
                'download_date': datetime.now().isoformat(),
                'total_series': len(all_data),
                'total_observations': len(combined_df),
                'date_range': {
                    'start': combined_df['date'].min().strftime('%Y-%m-%d'),
                    'end': combined_df['date'].max().strftime('%Y-%m-%d')
                },
                'series_included': list(self.epu_series.keys()),
                'context_descriptions_count': len(all_context)
            }
            
            summary_path = self.output_dir / "download_summary.json"
            with open(summary_path, 'w') as f:
                json.dump(summary, f, indent=2)
            logger.info(f"Download summary saved to: {summary_path}")
            
            logger.info(f"--- Policy Uncertainty Data Download Complete ---")
            logger.info(f"Total context descriptions generated: {len(all_context)}")
            logger.info(f"Data saved to: {self.output_dir}")
            
            return True
        else:
            logger.error("No data was successfully downloaded")
            return False

def main():
    """Main function"""
    try:
        downloader = PolicyUncertaintyDownloader()
        success = downloader.download_all_series()
        
        if success:
            logger.info("Policy uncertainty data download completed successfully!")
        else:
            logger.error("Policy uncertainty data download failed!")
            
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        raise

if __name__ == "__main__":
    main() 