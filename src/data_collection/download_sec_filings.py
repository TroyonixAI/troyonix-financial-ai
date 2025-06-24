"""
Download SEC filings with proper rate limiting and error handling.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

import os
import time
import requests
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
    "Apple": "320193",
    "Amazon": "1018724",
    "Google": "1652044",
    "Microsoft": "789019",
    "Tesla": "1326801",
    "JPMorgan Chase": "19617",
    "Bank of America": "70858",
    "Goldman Sachs": "886982",
    "BlackRock": "1364742",
    "Berkshire Hathaway": "1067983"
}

# Form types to download
FORM_TYPES = ["10-K", "10-Q", "8-K"]

# Number of recent filings to download for each form type
FILINGS_PER_TYPE = 10

# --- Main Logic ---

def get_filing_content(cik, accession_number_with_dashes, primary_document):
    """
    Fetches the content of a specific filing.
    """
    url = f"https://www.sec.gov/Archives/edgar/data/{cik}/{accession_number_with_dashes.replace('-', '')}/{primary_document}"
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def download_sec_filings():
    """
    Downloads recent SEC filings for a predefined list of companies.
    It fetches all recent filings and saves them locally.
    """
    # Ensure the output directory exists
    output_dir = "data/raw/wealth_data/sec_filings"
    os.makedirs(output_dir, exist_ok=True)

    print("--- Starting SEC Filing Download ---")

    for company_name, cik in COMPANIES.items():
        print(f"\nProcessing {company_name} (CIK: {cik})...")
        
        try:
            print(f"  Fetching recent filings...")
            
            # Construct the URL for the submissions API
            submissions_url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
            headers = {'User-Agent': USER_AGENT}
            
            # Get the most recent filings of any type
            response = requests.get(submissions_url, headers=headers)
            response.raise_for_status()
            submissions = response.json()
            
            if submissions and 'filings' in submissions and 'recent' in submissions['filings']:
                recent_filings = submissions['filings']['recent']
                accession_numbers = recent_filings.get('accessionNumber', [])
                filing_dates = recent_filings.get('filingDate', [])
                form_types = recent_filings.get('form', [])
                primary_documents = recent_filings.get('primaryDocument', [])

                filing_counts = {form_type: 0 for form_type in FORM_TYPES}

                for i, accession_number_raw in enumerate(accession_numbers):
                    form_type = form_types[i]

                    if form_type in FORM_TYPES and filing_counts[form_type] < FILINGS_PER_TYPE:
                        accession_number = accession_number_raw.replace("-", "")
                        filing_date = filing_dates[i]
                        primary_document = primary_documents[i]
                        
                        try:
                            # Get the full filing content
                            filing_content = get_filing_content(cik, accession_number_raw, primary_document)
                            
                            # Define the output path
                            filename = f"{accession_number}_{form_type.replace('/', '_')}_{filing_date}.txt"
                            output_path = os.path.join(output_dir, filename)
                            
                            # Save the filing content
                            with open(output_path, "w", encoding="utf-8") as f:
                                f.write(filing_content)
                            
                            print(f"    ({filing_counts[form_type] + 1}/{FILINGS_PER_TYPE}) Downloaded {form_type}: {filename}")
                            filing_counts[form_type] += 1
                            
                            # Adhere to SEC rate limits
                            time.sleep(0.1) 
                            
                        except requests.exceptions.HTTPError as e:
                            print(f"    HTTP Error downloading filing {accession_number_raw}: {e}")
                        except Exception as e:
                            print(f"    Error processing filing {accession_number_raw}: {e}")
            else:
                print(f"  No recent filings found for {company_name}.")
                
        except requests.exceptions.HTTPError as e:
            print(f"  HTTP Error fetching submissions for {company_name}: {e}")
        except Exception as e:
            print(f"  Error processing {company_name}: {e}")

    print("\n--- SEC Filing Download Complete ---")

if __name__ == "__main__":
    download_sec_filings() 