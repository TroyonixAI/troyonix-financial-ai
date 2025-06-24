import os
from pathlib import Path
import json
import shutil
import sys

# Add src to Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.utils.secure_data_utils import secure_save

def setup_kaggle_credentials():
    """Set up Kaggle credentials securely."""
    # Create .kaggle directory in user's home directory
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_dir.mkdir(exist_ok=True)
    
    # Check if kaggle.json exists in current directory
    current_dir = Path.cwd()
    kaggle_json = current_dir / "kaggle.json"
    
    if not kaggle_json.exists():
        print("\nPlease follow these steps to set up Kaggle credentials:")
        print("1. Go to https://www.kaggle.com/account")
        print("2. Click 'Create New API Token'")
        print("3. Save the downloaded kaggle.json file in your project root directory")
        print("4. Run this script again")
        return False
    
    # Read the Kaggle credentials
    with open(kaggle_json, 'r') as f:
        credentials = json.load(f)
    
    # Save credentials securely
    secure_save(
        credentials,
        str(kaggle_dir / "kaggle.json"),
        os.getenv("CONFIG_PASSWORD", "default_password")  # Use environment variable or default
    )
    
    # Set correct permissions
    os.chmod(kaggle_dir / "kaggle.json", 0o600)
    
    print("Kaggle credentials set up successfully!")
    return True

if __name__ == "__main__":
    setup_kaggle_credentials() 