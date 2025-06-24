"""
Secure configuration management utilities.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any
import logging
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

def generate_key(password: str, salt: bytes = None) -> tuple:
    """Generate encryption key from password."""
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

def encrypt_config(config: Dict[str, Any], key: bytes) -> bytes:
    """Encrypt configuration data."""
    f = Fernet(key)
    return f.encrypt(json.dumps(config).encode())

def decrypt_config(encrypted_data: bytes, key: bytes) -> Dict[str, Any]:
    """Decrypt configuration data."""
    f = Fernet(key)
    return json.loads(f.decrypt(encrypted_data).decode())

def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load and decrypt configuration securely."""
    try:
        if config_path is None:
            config_path = "config/config.json"
        
        # Check if encrypted config exists
        encrypted_path = f"{config_path}.enc"
        if os.path.exists(encrypted_path):
            # Get encryption key from environment
            password = os.getenv("CONFIG_PASSWORD")
            if not password:
                raise ConfigError("CONFIG_PASSWORD environment variable not set")
            
            # Load salt
            salt_path = f"{config_path}.salt"
            if not os.path.exists(salt_path):
                raise ConfigError("Salt file not found")
            
            with open(salt_path, "rb") as f:
                salt = f.read()
            
            # Generate key and decrypt
            key, _ = generate_key(password, salt)
            with open(encrypted_path, "rb") as f:
                encrypted_data = f.read()
            return decrypt_config(encrypted_data, key)
        
        # Fallback to unencrypted config
        with open(config_path, "r") as f:
            return json.load(f)
            
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise ConfigError(f"Failed to load configuration: {e}")

def save_config(config: Dict[str, Any], config_path: str = None, password: str = None) -> None:
    """Save configuration securely with encryption."""
    try:
        if config_path is None:
            config_path = "config/config.json"
        
        if password:
            # Generate new salt and key
            key, salt = generate_key(password)
            
            # Save salt
            salt_path = f"{config_path}.salt"
            with open(salt_path, "wb") as f:
                f.write(salt)
            
            # Encrypt and save config
            encrypted_data = encrypt_config(config, key)
            encrypted_path = f"{config_path}.enc"
            with open(encrypted_path, "wb") as f:
                f.write(encrypted_data)
            
            # Remove unencrypted config if it exists
            if os.path.exists(config_path):
                os.remove(config_path)
        else:
            # Save unencrypted config
            with open(config_path, "w") as f:
                json.dump(config, f, indent=4)
                
    except Exception as e:
        logger.error(f"Error saving configuration: {e}")
        raise ConfigError(f"Failed to save configuration: {e}")

def get_api_key(config: Dict[str, Any], service: str) -> str:
    """Get API key securely."""
    try:
        if "api_keys" not in config:
            raise ConfigError("API keys not found in configuration")
        
        if service not in config["api_keys"]:
            raise ConfigError(f"API key for {service} not found")
        
        return config["api_keys"][service]
    except Exception as e:
        logger.error(f"Error getting API key: {e}")
        raise ConfigError(f"Failed to get API key: {e}")

def get_user_agent(config: Dict[str, Any], service: str) -> str:
    """Get user agent string securely."""
    try:
        if "user_agents" not in config:
            raise ConfigError("User agents not found in configuration")
        
        if service not in config["user_agents"]:
            raise ConfigError(f"User agent for {service} not found")
        
        return config["user_agents"][service]
    except Exception as e:
        logger.error(f"Error getting user agent: {e}")
        raise ConfigError(f"Failed to get user agent: {e}")

def get_rate_limit(config: Dict[str, Any], service: str) -> float:
    """Get rate limit securely."""
    try:
        if "rate_limits" not in config:
            raise ConfigError("Rate limits not found in configuration")
        
        if service not in config["rate_limits"]:
            raise ConfigError(f"Rate limit for {service} not found")
        
        return float(config["rate_limits"][service])
    except Exception as e:
        logger.error(f"Error getting rate limit: {e}")
        raise ConfigError(f"Failed to get rate limit: {e}") 