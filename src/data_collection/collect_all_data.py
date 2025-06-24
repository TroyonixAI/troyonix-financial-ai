#!/usr/bin/env python3
"""
Comprehensive data collection script for Troyonix wealth management AI.
Orchestrates collection from all legal, public domain sources.

Phase 1: SEC EDGAR Filings (Company financial data)
Phase 2: FRED Economic Data (Government economic indicators)
Phase 3: Policy Uncertainty Indices (Market sentiment indicators)

Author: Troyonix AI Team
Date: 2025
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.utils.config_utils import load_config
from src.utils.file_utils import ensure_directory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('data_collection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DataCollectionOrchestrator:
    def __init__(self):
        self.config = load_config()
        self.start_time = datetime.now()
        
        # Ensure all output directories exist
        self.directories = {
            'sec_filings': 'data/raw/wealth_data/sec_filings',
            'fred_data': 'data/raw/wealth_data/fred_data',
            'policy_uncertainty': 'data/raw/wealth_data/policy_uncertainty',
            'processed': 'data/processed/wealth_data'
        }
        
        for dir_path in self.directories.values():
            ensure_directory(dir_path)
    
    def run_sec_collection(self):
        """Phase 1: Collect SEC EDGAR filings"""
        logger.info("=== PHASE 1: SEC EDGAR Filings Collection ===")
        
        try:
            from src.data_collection.download_sec_filings import download_sec_filings
            download_sec_filings()
            logger.info("SEC filings collection completed successfully")
            return True
        except Exception as e:
            logger.error(f"SEC filings collection failed: {e}")
            return False
    
    def run_fred_collection(self):
        """Phase 2: Collect FRED economic data"""
        logger.info("=== PHASE 2: FRED Economic Data Collection ===")
        
        # Check if FRED API key is configured
        fred_api_key = self.config.get('api_keys', {}).get('fred')
        if not fred_api_key or fred_api_key == "YOUR_FRED_API_KEY_HERE":
            logger.warning("FRED API key not configured. Skipping FRED data collection.")
            logger.info("To enable FRED data collection:")
            logger.info("1. Get a free API key from: https://fred.stlouisfed.org/docs/api/api_key.html")
            logger.info("2. Update config/config.json with your FRED API key")
            return False
        
        try:
            from src.data_collection.download_fred_data import download_fred_data
            download_fred_data()
            logger.info("FRED data collection completed successfully")
            return True
        except Exception as e:
            logger.error(f"FRED data collection failed: {e}")
            return False
    
    def run_policy_uncertainty_collection(self):
        """Phase 3: Collect policy uncertainty indices"""
        logger.info("=== PHASE 3: Policy Uncertainty Data Collection ===")
        
        # Check if FRED API key is configured (same as FRED data)
        fred_api_key = self.config.get('api_keys', {}).get('fred')
        if not fred_api_key or fred_api_key == "YOUR_FRED_API_KEY_HERE":
            logger.warning("FRED API key not configured. Skipping policy uncertainty collection.")
            return False
        
        try:
            from src.data_collection.download_policy_uncertainty import main as download_policy_uncertainty
            download_policy_uncertainty()
            logger.info("Policy uncertainty data collection completed successfully")
            return True
        except Exception as e:
            logger.error(f"Policy uncertainty collection failed: {e}")
            return False
    
    def generate_collection_summary(self):
        """Generate a summary of collected data"""
        logger.info("=== DATA COLLECTION SUMMARY ===")
        
        summary = {
            'sec_filings': 0,
            'fred_data': 0,
            'policy_uncertainty': 0
        }
        
        # Count SEC filings
        sec_dir = Path(self.directories['sec_filings'])
        if sec_dir.exists():
            summary['sec_filings'] = len(list(sec_dir.glob('*.txt')))
        
        # Count FRED data files
        fred_dir = Path(self.directories['fred_data'])
        if fred_dir.exists():
            summary['fred_data'] = len(list(fred_dir.glob('*.json'))) + len(list(fred_dir.glob('*.txt')))
        
        # Count policy uncertainty files
        policy_dir = Path(self.directories['policy_uncertainty'])
        if policy_dir.exists():
            summary['policy_uncertainty'] = len(list(policy_dir.glob('*.json'))) + len(list(policy_dir.glob('*.csv')))
        
        logger.info(f"SEC Filings: {summary['sec_filings']} files")
        logger.info(f"FRED Data: {summary['fred_data']} files")
        logger.info(f"Policy Uncertainty: {summary['policy_uncertainty']} files")
        
        total_files = sum(summary.values())
        logger.info(f"Total files collected: {total_files}")
        
        return summary
    
    def run_complete_collection(self):
        """Run the complete data collection pipeline"""
        logger.info("🚀 Starting Troyonix Data Collection Pipeline")
        logger.info(f"Start time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Track success of each phase
        results = {
            'sec_filings': False,
            'fred_data': False,
            'policy_uncertainty': False
        }
        
        # Phase 1: SEC Filings (Always run - no API key required)
        results['sec_filings'] = self.run_sec_collection()
        
        # Phase 2: FRED Economic Data (Requires API key)
        results['fred_data'] = self.run_fred_collection()
        
        # Phase 3: Policy Uncertainty (Requires FRED API key)
        results['policy_uncertainty'] = self.run_policy_uncertainty_collection()
        
        # Generate summary
        summary = self.generate_collection_summary()
        
        # Final report
        end_time = datetime.now()
        duration = end_time - self.start_time
        
        logger.info("=== COLLECTION COMPLETE ===")
        logger.info(f"Duration: {duration}")
        logger.info(f"Successful phases: {sum(results.values())}/{len(results)}")
        
        for phase, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED/SKIPPED"
            logger.info(f"{phase.replace('_', ' ').title()}: {status}")
        
        return results, summary

def main():
    """Main entry point"""
    orchestrator = DataCollectionOrchestrator()
    results, summary = orchestrator.run_complete_collection()
    
    # Print final summary to console
    print("\n" + "="*60)
    print("TROYONIX DATA COLLECTION COMPLETE")
    print("="*60)
    print(f"SEC Filings: {summary['sec_filings']} files")
    print(f"FRED Data: {summary['fred_data']} files") 
    print(f"Policy Uncertainty: {summary['policy_uncertainty']} files")
    print(f"Total: {sum(summary.values())} files")
    print("="*60)
    
    if summary['sec_filings'] > 0:
        print("✅ Phase 1 (SEC Filings): SUCCESS")
    else:
        print("❌ Phase 1 (SEC Filings): FAILED")
    
    if summary['fred_data'] > 0:
        print("✅ Phase 2 (FRED Data): SUCCESS")
    else:
        print("⚠️  Phase 2 (FRED Data): SKIPPED (API key required)")
    
    if summary['policy_uncertainty'] > 0:
        print("✅ Phase 3 (Policy Uncertainty): SUCCESS")
    else:
        print("⚠️  Phase 3 (Policy Uncertainty): SKIPPED (API key required)")

if __name__ == "__main__":
    main() 