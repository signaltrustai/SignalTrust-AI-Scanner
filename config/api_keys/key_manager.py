#!/usr/bin/env python3
"""
Secure API Key Manager
Handles encrypted storage and retrieval of API keys

Features:
- Encrypted key storage using Fernet (symmetric encryption)
- Environment variable integration
- Secure key rotation
- Access logging
- Multiple provider support
"""

import os
import json
import base64
from pathlib import Path
from typing import Dict, Optional, List
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import logging

logger = logging.getLogger(__name__)


class KeyManager:
    """Secure API Key Manager with encryption support."""
    
    def __init__(self, key_file: Optional[str] = None, master_password: Optional[str] = None):
        """
        Initialize the Key Manager.
        
        Args:
            key_file: Path to encrypted keys file (default: config/api_keys/keys.enc)
            master_password: Master password for encryption (from env: API_MASTER_PASSWORD)
        """
        # Set default paths
        self.base_dir = Path(__file__).parent
        self.key_file = Path(key_file) if key_file else self.base_dir / "keys.enc"
        
        # Get master password from env or parameter
        self.master_password = master_password or os.getenv("API_MASTER_PASSWORD")
        
        # Initialize cipher if master password is set
        self.cipher = None
        if self.master_password:
            self.cipher = self._create_cipher(self.master_password)
        
        # In-memory key cache
        self._cache: Dict[str, str] = {}
        
        logger.info(f"KeyManager initialized with key_file: {self.key_file}")
    
    def _create_cipher(self, password: str) -> Fernet:
        """Create Fernet cipher from password."""
        # Load or generate salt
        salt_file = self.base_dir / ".salt"
        if salt_file.exists():
            with open(salt_file, 'rb') as f:
                salt = f.read()
        else:
            # Generate random salt on first use
            import secrets
            salt = secrets.token_bytes(32)
            # Save salt (unencrypted - it's not secret)
            salt_file.parent.mkdir(parents=True, exist_ok=True)
            with open(salt_file, 'wb') as f:
                f.write(salt)
        
        # Use PBKDF2HMAC to derive a key from password
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return Fernet(key)
    
    def set_key(self, key_name: str, key_value: str, save: bool = True) -> bool:
        """
        Store an API key.
        
        Args:
            key_name: Name of the key (e.g., 'GROQ_API_KEY')
            key_value: The actual key value
            save: Whether to save to disk immediately
            
        Returns:
            True if successful
        """
        try:
            # Store in cache
            self._cache[key_name] = key_value
            
            # Save to disk if requested
            if save and self.cipher:
                return self._save_keys()
            
            return True
        except Exception as e:
            logger.error(f"Failed to set key {key_name}: {str(e)}")
            return False
    
    def get_key(self, key_name: str, fallback_env: bool = True) -> Optional[str]:
        """
        Retrieve an API key.
        
        Args:
            key_name: Name of the key
            fallback_env: If True, fallback to environment variable
            
        Returns:
            The key value or None if not found
        """
        # Check cache first
        if key_name in self._cache:
            return self._cache[key_name]
        
        # Try to load from disk
        if self.cipher and self.key_file.exists():
            self._load_keys()
            if key_name in self._cache:
                return self._cache[key_name]
        
        # Fallback to environment variable
        if fallback_env:
            env_value = os.getenv(key_name)
            if env_value:
                # Cache it for future use
                self._cache[key_name] = env_value
                return env_value
        
        return None
    
    def list_keys(self) -> List[str]:
        """List all stored key names (not values)."""
        # Load from disk first
        if self.cipher and self.key_file.exists():
            self._load_keys()
        
        # Combine with environment variables
        key_names = set(self._cache.keys())
        
        # Add common API key names from environment
        env_keys = [k for k in os.environ.keys() if k.endswith('_API_KEY') or k.endswith('_KEY')]
        key_names.update(env_keys)
        
        return sorted(list(key_names))
    
    def delete_key(self, key_name: str, save: bool = True) -> bool:
        """
        Delete a stored key.
        
        Args:
            key_name: Name of the key to delete
            save: Whether to save changes to disk
            
        Returns:
            True if successful
        """
        try:
            if key_name in self._cache:
                del self._cache[key_name]
            
            if save and self.cipher:
                return self._save_keys()
            
            return True
        except Exception as e:
            logger.error(f"Failed to delete key {key_name}: {str(e)}")
            return False
    
    def rotate_key(self, key_name: str, new_value: str) -> bool:
        """
        Rotate an API key (delete old, set new).
        
        Args:
            key_name: Name of the key
            new_value: New key value
            
        Returns:
            True if successful
        """
        logger.info(f"Rotating key: {key_name}")
        return self.set_key(key_name, new_value, save=True)
    
    def _save_keys(self) -> bool:
        """Save encrypted keys to disk."""
        if not self.cipher:
            logger.warning("Cannot save keys: no cipher initialized (missing master password)")
            return False
        
        try:
            # Convert cache to JSON
            data = json.dumps(self._cache)
            
            # Encrypt
            encrypted_data = self.cipher.encrypt(data.encode())
            
            # Ensure directory exists
            self.key_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Write to file
            with open(self.key_file, 'wb') as f:
                f.write(encrypted_data)
            
            logger.info(f"Keys saved to {self.key_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save keys: {str(e)}")
            return False
    
    def _load_keys(self) -> bool:
        """Load encrypted keys from disk."""
        if not self.cipher:
            logger.warning("Cannot load keys: no cipher initialized (missing master password)")
            return False
        
        if not self.key_file.exists():
            logger.debug(f"Key file not found: {self.key_file}")
            return False
        
        try:
            # Read encrypted file
            with open(self.key_file, 'rb') as f:
                encrypted_data = f.read()
            
            # Decrypt
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Load JSON
            self._cache = json.loads(decrypted_data.decode())
            
            logger.info(f"Loaded {len(self._cache)} keys from {self.key_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to load keys: {str(e)}")
            return False
    
    def import_from_env(self, key_patterns: Optional[List[str]] = None) -> int:
        """
        Import API keys from environment variables.
        
        Args:
            key_patterns: List of patterns to match (default: ['*_API_KEY', '*_KEY'])
            
        Returns:
            Number of keys imported
        """
        if key_patterns is None:
            key_patterns = ['_API_KEY', '_KEY']
        
        count = 0
        for key, value in os.environ.items():
            # Check if key matches any pattern
            if any(pattern in key for pattern in key_patterns):
                if self.set_key(key, value, save=False):
                    count += 1
        
        # Save all at once
        if count > 0 and self.cipher:
            self._save_keys()
        
        logger.info(f"Imported {count} keys from environment")
        return count
    
    def export_to_env(self, key_names: Optional[List[str]] = None) -> int:
        """
        Export stored keys to environment variables (current process only).
        
        Args:
            key_names: Specific keys to export (default: all)
            
        Returns:
            Number of keys exported
        """
        # Load keys first
        if self.cipher and self.key_file.exists():
            self._load_keys()
        
        keys_to_export = key_names or list(self._cache.keys())
        count = 0
        
        for key_name in keys_to_export:
            if key_name in self._cache:
                os.environ[key_name] = self._cache[key_name]
                count += 1
        
        logger.info(f"Exported {count} keys to environment")
        return count
    
    def get_all_keys(self) -> Dict[str, str]:
        """
        Get all keys (for admin/debugging purposes only).
        
        WARNING: This exposes sensitive data. Use with caution.
        
        Returns:
            Dictionary of all keys
        """
        # Load from disk first
        if self.cipher and self.key_file.exists():
            self._load_keys()
        
        return dict(self._cache)
    
    def clear_cache(self):
        """Clear the in-memory key cache."""
        self._cache.clear()
        logger.info("Key cache cleared")
    
    def _mask_key(self, key_value: str) -> str:
        """Safely mask an API key for display.
        
        Args:
            key_value: The key to mask
            
        Returns:
            Masked key string
        """
        if not key_value or len(key_value) < 8:
            return "***"
        # Show only first 4 and last 4 characters
        return key_value[:4] + "..." + key_value[-4:]


# Convenience functions for common operations
def get_groq_key() -> Optional[str]:
    """Get Groq API key."""
    manager = KeyManager()
    return manager.get_key('GROQ_API_KEY')


def get_anthropic_key() -> Optional[str]:
    """Get Anthropic API key."""
    manager = KeyManager()
    return manager.get_key('ANTHROPIC_API_KEY')


def get_market_data_keys() -> Dict[str, Optional[str]]:
    """Get all market data API keys."""
    manager = KeyManager()
    return {
        'coingecko': manager.get_key('COINGECKO_API_KEY'),
        'alphavantage': manager.get_key('ALPHAVANTAGE_API_KEY'),
        'whalealert': manager.get_key('WHALEALERT_API_KEY'),
        'newscatcher': manager.get_key('NEWS_CATCHER_API_KEY'),
    }


if __name__ == "__main__":
    # Example usage
    import sys
    
    logging.basicConfig(level=logging.INFO)
    
    print("SignalTrust AI Key Manager")
    print("=" * 50)
    
    # Initialize manager
    manager = KeyManager()
    
    # List available keys
    print("\nAvailable keys:")
    for key in manager.list_keys():
        value = manager.get_key(key)
        masked = manager._mask_key(value) if value else "***"
        print(f"  {key}: {masked}")
    
    print("\nUse environment variable API_MASTER_PASSWORD to enable encryption.")
