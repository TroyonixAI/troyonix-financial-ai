"""
Utility functions for API interactions.
"""
import requests
import time
from pathlib import Path

def get_headers(user_agent):
    """Get headers required by various APIs."""
    return {
        "User-Agent": user_agent,
        "Accept-Encoding": "gzip, deflate"
    }

def make_api_request(url, headers, params=None, max_retries=3, retry_delay=1, rate_limit=0.1):
    """
    Make an API request with proper rate limiting and retry logic.
    
    Args:
        url (str): The API endpoint URL
        headers (dict): Request headers
        params (dict, optional): Query parameters
        max_retries (int): Maximum number of retry attempts
        retry_delay (int): Delay between retries in seconds
        rate_limit (float): Minimum time between requests in seconds
    
    Returns:
        dict/None: JSON response if successful, None if failed
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:  # Too Many Requests
                print(f"Rate limit hit. Waiting before retry...")
                time.sleep(retry_delay)
                continue
            else:
                print(f"Request failed. Status: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error making request: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            return None
            
        finally:
            time.sleep(rate_limit)
    
    return None 