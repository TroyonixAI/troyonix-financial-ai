import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import os
import time
from sec_edgar_api import EdgarClient
from src.utils.file_utils import save_text, ensure_directory

# --- Configuration ---

# Directory to save the downloaded filings
SAVE_DIR = "data/raw/wealth_data/sec_filings"
ensure_directory(SAVE_DIR)

# SEC Edgar User-Agent
# IMPORTANT: Replace with your actual name and email address
USER_AGENT = "Your Name (your.email@example.com)"

# List of companies to process by their Central Index Key (CIK)
COMPANIES = {
    "Apple": "0000320193",
    "Amazon": "0001018724",
    "Google": "0001652044",
    "Microsoft": "0000789019",
    "Tesla": "0001326801",
    "JPMorgan Chase": "0000019617",
    "Bank of America": "0000070858",
    "Goldman Sachs": "0000886982",
    "BlackRock": "0001364742",
    "Berkshire Hathaway": "0001067983"
}

# Form types to download
FORM_TYPES = ["10-K", "10-Q", "8-K"]

# Number of recent filings to download for each form type
FILINGS_PER_TYPE = 5

# --- Main Logic ---

def download_sec_filings():
    """
    Downloads recent SEC filings for a list of companies using the sec-edgar-api library.
    """
    print("Starting SEC filings download...")
    print(f"User-Agent: {USER_AGENT}")
    
    # Initialize the EdgarClient
    edgar_client = EdgarClient(user_agent=USER_AGENT)
    
    # Loop through each company
    for company_name, cik in COMPANIES.items():
        print(f"\nProcessing {company_name} (CIK: {cik})...")
        
        # Loop through each form type
        for form_type in FORM_TYPES:
            try:
                print(f"  Fetching recent {form_type} filings...")
                
                # Get the N most recent filings of the specified type
                filings = edgar_client.get_filings(cik=cik, form_type=form_type, limit=FILINGS_PER_TYPE)
                
                if not filings or 'filings' not in filings or not filings['filings']:
                    print(f"  No recent {form_type} filings found.")
                    continue
                    
                # Download each filing
                for filing in filings['filings']:
                    accession_number = filing['accessionNumber']
                    filing_date = filing['filingDate']
                    
                    try:
                        # Get the full text of the filing
                        filing_text = edgar_client.get_filing_text(accession_number=accession_number)
                        
                        # Save the filing
                        filename = f"{company_name.replace(' ', '_')}_{cik}_{form_type}_{filing_date}.txt"
                        filepath = os.path.join(SAVE_DIR, filename)
                        save_text(filing_text, filepath)
                        
                        print(f"    Successfully downloaded {form_type} from {filing_date} to {filename}")
                        
                    except Exception as e:
                        print(f"    Error downloading filing {accession_number}: {e}")
                    
                    # Respect SEC rate limits by sleeping briefly
                    time.sleep(0.1) 
                    
            except Exception as e:
                print(f"  Error fetching {form_type} filings for {company_name}: {e}")

    print("\nSEC filings download complete.")

if __name__ == "__main__":
    download_sec_filings() 