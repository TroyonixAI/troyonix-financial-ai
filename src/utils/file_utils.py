"""
Utility functions for file operations.
"""
import os
import json
from pathlib import Path

def ensure_directory(directory):
    """
    Ensure a directory exists, create if it doesn't.
    
    Args:
        directory (str/Path): Directory path to ensure exists
    """
    Path(directory).mkdir(parents=True, exist_ok=True)

def save_json(data, filepath):
    """
    Save data to a JSON file.
    
    Args:
        data (dict): Data to save
        filepath (str/Path): Path to save the JSON file
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def load_json(filepath):
    """
    Load data from a JSON file.
    
    Args:
        filepath (str/Path): Path to the JSON file
    
    Returns:
        dict: Loaded data or None if file doesn't exist
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_text(text, filepath):
    """
    Save text to a file.
    
    Args:
        text (str): Text to save
        filepath (str/Path): Path to save the text file
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)

def load_text(filepath):
    """
    Load text from a file.
    
    Args:
        filepath (str/Path): Path to the text file
    
    Returns:
        str: Loaded text or None if file doesn't exist
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None 