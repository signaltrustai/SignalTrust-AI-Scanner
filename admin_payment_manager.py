#!/usr/bin/env python3
"""
Admin Payment Manager
Secure management of payment information for admin use only
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional
from cryptography.fernet import Fernet
import base64
import hashlib


class AdminPaymentManager:
    """Manages admin payment information securely"""
    
    def __init__(self, data_file: str = 'data/admin_payment_info.json'):
        """Initialize the admin payment manager.
        
        Args:
            data_file: Path to encrypted payment info file
        """
        self.data_file = data_file
        self._ensure_data_dir()
        self._init_encryption()
        self._load_payment_info()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists."""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _init_encryption(self):
        """Initialize encryption key from environment or generate one."""
        # Use SECRET_KEY from environment or generate one
        secret_key = os.getenv('SECRET_KEY', 'default-key-change-in-production')
        
        # Generate Fernet key from secret
        key_material = hashlib.sha256(secret_key.encode()).digest()
        self.cipher_key = base64.urlsafe_b64encode(key_material)
        self.cipher = Fernet(self.cipher_key)
    
    def _load_payment_info(self):
        """Load payment information from file."""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    encrypted_data = f.read()
                    if encrypted_data:
                        decrypted = self.cipher.decrypt(encrypted_data.encode())
                        self.payment_info = json.loads(decrypted.decode())
                    else:
                        self._init_default_payment_info()
            except Exception as e:
                print(f"Error loading payment info: {e}")
                self._init_default_payment_info()
        else:
            self._init_default_payment_info()
    
    def _init_default_payment_info(self):
        """Initialize with default/empty payment information."""
        self.payment_info = {
            "crypto_wallets": {
                "ethereum": os.getenv("ETHEREUM_WALLET_ADDRESS", "0xFDAf80b517993A3420E96Fb11D01e959EE35A419"),
                "polygon": os.getenv("POLYGON_WALLET_ADDRESS", "0xFDAf80b517993A3420E96Fb11D01e959EE35A419"),
                "binance": os.getenv("BINANCE_WALLET_ADDRESS", "0xFDAf80b517993A3420E96Fb11D01e959EE35A419"),
                "arbitrum": os.getenv("ARBITRUM_WALLET_ADDRESS", "0xFDAf80b517993A3420E96Fb11D01e959EE35A419"),
                "bitcoin": os.getenv("BITCOIN_WALLET_ADDRESS", "bc1qz4kq6hu05j6rdnzv2xe325wf0404smhsaxas86"),
                "solana": os.getenv("SOLANA_WALLET_ADDRESS", "BATM5MQZxeNaJGPGdUsRGD5mputbCkHheckcm1y8Vt6r")
            },
            "bank_accounts": {
                "usd": {
                    "bank_name": os.getenv("BANK_NAME_USD", ""),
                    "account_number": os.getenv("BANK_ACCOUNT_NUMBER_USD", ""),
                    "routing_number": os.getenv("BANK_ROUTING_NUMBER_USD", ""),
                    "swift_code": os.getenv("BANK_SWIFT_CODE_USD", ""),
                    "account_holder": os.getenv("BANK_ACCOUNT_HOLDER", "SignalTrust AI")
                },
                "eur": {
                    "bank_name": os.getenv("BANK_NAME_EUR", ""),
                    "iban": os.getenv("BANK_IBAN_EUR", ""),
                    "swift_code": os.getenv("BANK_SWIFT_CODE_EUR", ""),
                    "account_holder": os.getenv("BANK_ACCOUNT_HOLDER", "SignalTrust AI")
                }
            },
            "paypal": {
                "email": os.getenv("PAYPAL_EMAIL", "payments@signaltrust.ai"),
                "paypal_me": os.getenv("PAYPAL_ME_LINK", "https://paypal.me/signaltrust")
            },
            "stripe": {
                "starter_monthly": os.getenv("STRIPE_STARTER_MONTHLY_LINK", ""),
                "pro_monthly": os.getenv("STRIPE_PRO_MONTHLY_LINK", ""),
                "enterprise_monthly": os.getenv("STRIPE_ENTERPRISE_MONTHLY_LINK", "")
            },
            "other_methods": {
                "buymeacoffee": os.getenv("BUYMEACOFFEE_LINK", ""),
                "kofi": os.getenv("KOFI_LINK", "")
            },
            "notes": "",
            "last_updated": datetime.now().isoformat()
        }
        self._save_payment_info()
    
    def _save_payment_info(self):
        """Save payment information to encrypted file."""
        try:
            # Update timestamp
            self.payment_info['last_updated'] = datetime.now().isoformat()
            
            # Encrypt and save
            json_data = json.dumps(self.payment_info, indent=2)
            encrypted = self.cipher.encrypt(json_data.encode())
            
            with open(self.data_file, 'w') as f:
                f.write(encrypted.decode())
            
            return True
        except Exception as e:
            print(f"Error saving payment info: {e}")
            return False
    
    def get_payment_info(self) -> Dict:
        """Get all payment information (decrypted).
        
        Returns:
            Dictionary with payment information
        """
        return self.payment_info.copy()
    
    def update_crypto_wallet(self, network: str, address: str) -> bool:
        """Update a cryptocurrency wallet address.
        
        Args:
            network: Network name (ethereum, bitcoin, etc.)
            address: Wallet address
            
        Returns:
            True if updated successfully
        """
        if "crypto_wallets" not in self.payment_info:
            self.payment_info["crypto_wallets"] = {}
        
        self.payment_info["crypto_wallets"][network] = address
        return self._save_payment_info()
    
    def update_bank_account(self, currency: str, bank_data: Dict) -> bool:
        """Update bank account information.
        
        Args:
            currency: Currency code (usd, eur, etc.)
            bank_data: Dictionary with bank details
            
        Returns:
            True if updated successfully
        """
        if "bank_accounts" not in self.payment_info:
            self.payment_info["bank_accounts"] = {}
        
        self.payment_info["bank_accounts"][currency] = bank_data
        return self._save_payment_info()
    
    def update_paypal(self, email: str, paypal_me: str = "") -> bool:
        """Update PayPal information.
        
        Args:
            email: PayPal email
            paypal_me: PayPal.me link
            
        Returns:
            True if updated successfully
        """
        self.payment_info["paypal"] = {
            "email": email,
            "paypal_me": paypal_me
        }
        return self._save_payment_info()
    
    def update_stripe_links(self, links: Dict) -> bool:
        """Update Stripe payment links.
        
        Args:
            links: Dictionary with Stripe links
            
        Returns:
            True if updated successfully
        """
        if "stripe" not in self.payment_info:
            self.payment_info["stripe"] = {}
        
        self.payment_info["stripe"].update(links)
        return self._save_payment_info()
    
    def update_notes(self, notes: str) -> bool:
        """Update payment notes.
        
        Args:
            notes: Payment notes or instructions
            
        Returns:
            True if updated successfully
        """
        self.payment_info["notes"] = notes
        return self._save_payment_info()
    
    def get_public_payment_methods(self) -> Dict:
        """Get payment methods safe for client display.
        
        Returns:
            Dictionary with public payment information (no bank details)
        """
        return {
            "crypto_wallets": self.payment_info.get("crypto_wallets", {}),
            "paypal": self.payment_info.get("paypal", {}).get("email", ""),
            "paypal_me": self.payment_info.get("paypal", {}).get("paypal_me", ""),
            "available_methods": ["crypto", "paypal", "stripe", "bank_transfer"]
        }


# Global instance
_payment_manager = None


def get_payment_manager() -> AdminPaymentManager:
    """Get global payment manager instance.
    
    Returns:
        AdminPaymentManager instance
    """
    global _payment_manager
    if _payment_manager is None:
        _payment_manager = AdminPaymentManager()
    return _payment_manager
