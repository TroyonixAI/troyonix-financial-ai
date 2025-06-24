import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import hashlib
import hmac
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecureDataError(Exception):
    """Custom exception for secure data handling errors."""
    pass

def generate_data_key() -> bytes:
    """Generate a secure key for data encryption."""
    return Fernet.generate_key()

def derive_key(password: str, salt: bytes = None) -> tuple:
    """Derive a secure key from a password."""
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key, salt

def encrypt_data(data: Dict[str, Any], key: bytes) -> bytes:
    """Encrypt sensitive data."""
    try:
        f = Fernet(key)
        return f.encrypt(json.dumps(data).encode())
    except Exception as e:
        logger.error(f"Error encrypting data: {e}")
        raise SecureDataError(f"Failed to encrypt data: {e}")

def decrypt_data(encrypted_data: bytes, key: bytes) -> Dict[str, Any]:
    """Decrypt sensitive data."""
    try:
        f = Fernet(key)
        return json.loads(f.decrypt(encrypted_data).decode())
    except Exception as e:
        logger.error(f"Error decrypting data: {e}")
        raise SecureDataError(f"Failed to decrypt data: {e}")

def secure_save(data: Dict[str, Any], filepath: str, password: str) -> None:
    """Securely save data with encryption."""
    try:
        # Generate key and salt
        key, salt = derive_key(password)
        
        # Encrypt data
        encrypted_data = encrypt_data(data, key)
        
        # Save salt
        salt_path = f"{filepath}.salt"
        with open(salt_path, "wb") as f:
            f.write(salt)
        
        # Save encrypted data
        with open(filepath, "wb") as f:
            f.write(encrypted_data)
            
    except Exception as e:
        logger.error(f"Error saving data securely: {e}")
        raise SecureDataError(f"Failed to save data securely: {e}")

def secure_load(filepath: str, password: str) -> Dict[str, Any]:
    """Securely load encrypted data."""
    try:
        # Load salt
        salt_path = f"{filepath}.salt"
        if not os.path.exists(salt_path):
            raise SecureDataError("Salt file not found")
        
        with open(salt_path, "rb") as f:
            salt = f.read()
        
        # Derive key
        key, _ = derive_key(password, salt)
        
        # Load and decrypt data
        with open(filepath, "rb") as f:
            encrypted_data = f.read()
        
        return decrypt_data(encrypted_data, key)
        
    except Exception as e:
        logger.error(f"Error loading data securely: {e}")
        raise SecureDataError(f"Failed to load data securely: {e}")

def verify_data_integrity(data: Dict[str, Any], signature: str) -> bool:
    """Verify data integrity using HMAC."""
    try:
        # Get secret key from environment
        secret_key = os.getenv("DATA_INTEGRITY_KEY")
        if not secret_key:
            raise SecureDataError("DATA_INTEGRITY_KEY environment variable not set")
        
        # Calculate HMAC
        h = hmac.new(
            secret_key.encode(),
            json.dumps(data, sort_keys=True).encode(),
            hashlib.sha256
        )
        calculated_signature = h.hexdigest()
        
        return hmac.compare_digest(calculated_signature, signature)
        
    except Exception as e:
        logger.error(f"Error verifying data integrity: {e}")
        raise SecureDataError(f"Failed to verify data integrity: {e}")

def sanitize_sensitive_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Remove or mask sensitive data."""
    sensitive_fields = {
        "api_key", "password", "token", "secret", "key",
        "credit_card", "ssn", "social_security", "account_number"
    }
    
    def mask_value(value: str) -> str:
        if len(value) <= 4:
            return "*" * len(value)
        return value[:2] + "*" * (len(value) - 4) + value[-2:]
    
    def sanitize_dict(d: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for key, value in d.items():
            if isinstance(value, dict):
                result[key] = sanitize_dict(value)
            elif isinstance(value, str) and any(field in key.lower() for field in sensitive_fields):
                result[key] = mask_value(value)
            else:
                result[key] = value
        return result
    
    return sanitize_dict(data)

def secure_log(data: Dict[str, Any], log_file: str) -> None:
    """Securely log data with sensitive information removed."""
    try:
        # Sanitize data
        sanitized_data = sanitize_sensitive_data(data)
        
        # Add timestamp
        sanitized_data["timestamp"] = datetime.now().isoformat()
        
        # Log to file
        with open(log_file, "a") as f:
            json.dump(sanitized_data, f)
            f.write("\n")
            
    except Exception as e:
        logger.error(f"Error logging data securely: {e}")
        raise SecureDataError(f"Failed to log data securely: {e}") 