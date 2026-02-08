"""
Crypto Payment Processor - MetaMask Integration
Handles cryptocurrency payments via MetaMask wallet
"""

import os
import json
from typing import Dict, Optional, Any
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CryptoPaymentProcessor:
    """Process cryptocurrency payments via MetaMask"""
    
    # Supported networks and their chain IDs
    NETWORKS = {
        'ethereum': {
            'chain_id': '0x1',  # Mainnet
            'name': 'Ethereum Mainnet',
            'currency': 'ETH',
            'rpc_url': 'https://mainnet.infura.io/v3/',
            'explorer': 'https://etherscan.io'
        },
        'polygon': {
            'chain_id': '0x89',  # Polygon Mainnet
            'name': 'Polygon Mainnet',
            'currency': 'MATIC',
            'rpc_url': 'https://polygon-rpc.com',
            'explorer': 'https://polygonscan.com'
        },
        'binance': {
            'chain_id': '0x38',  # BSC Mainnet
            'name': 'Binance Smart Chain',
            'currency': 'BNB',
            'rpc_url': 'https://bsc-dataseed.binance.org',
            'explorer': 'https://bscscan.com'
        },
        'arbitrum': {
            'chain_id': '0xa4b1',  # Arbitrum One
            'name': 'Arbitrum One',
            'currency': 'ETH',
            'rpc_url': 'https://arb1.arbitrum.io/rpc',
            'explorer': 'https://arbiscan.io'
        }
    }
    
    # Price tiers in USD (will be converted to crypto)
    PLANS_USD = {
        'basic': 29.99,
        'pro': 79.99,
        'enterprise': 299.99
    }
    
    def __init__(self):
        """Initialize crypto payment processor"""
        # Wallet addresses for receiving payments (multi-chain support)
        self.wallet_addresses = {
            'ethereum': os.getenv('ETHEREUM_WALLET_ADDRESS', '0xFDAf80b517993A3420E96Fb11D01e959EE35A419'),
            'polygon': os.getenv('POLYGON_WALLET_ADDRESS', '0xFDAf80b517993A3420E96Fb11D01e959EE35A419'),
            'binance': os.getenv('BINANCE_WALLET_ADDRESS', '0xFDAf80b517993A3420E96Fb11D01e959EE35A419'),
            'arbitrum': os.getenv('ARBITRUM_WALLET_ADDRESS', '0xFDAf80b517993A3420E96Fb11D01e959EE35A419'),
            'bitcoin': os.getenv('BITCOIN_WALLET_ADDRESS', 'bc1qz4kq6hu05j6rdnzv2xe325wf0404smhsaxas86'),
            'solana': os.getenv('SOLANA_WALLET_ADDRESS', 'BATM5MQZxeNaJGPGdUsRGD5mputbCkHheckcm1y8Vt6r')
        }
        
        # Default wallet address for EVM chains (Ethereum, Polygon, BSC, Arbitrum)
        self.wallet_address = self.wallet_addresses['polygon']  # Default to Polygon
        
        # Preferred network for payments
        self.preferred_network = os.getenv('CRYPTO_NETWORK', 'polygon')
        
        # Minimum confirmations before payment is considered valid
        self.min_confirmations = int(os.getenv('CRYPTO_MIN_CONFIRMATIONS', '3'))
        
        logger.info(f"Crypto payment processor initialized")
        logger.info(f"EVM Wallet (ETH/Polygon/BSC/Arbitrum): {self.wallet_addresses['ethereum'][:10]}...")
        logger.info(f"Bitcoin Wallet: {self.wallet_addresses['bitcoin'][:10]}...")
        logger.info(f"Solana Wallet: {self.wallet_addresses['solana'][:10]}...")
    
    def get_payment_address(self, network: str = 'polygon') -> str:
        """Get the wallet address for receiving payments on specific network"""
        if network in ['ethereum', 'polygon', 'binance', 'arbitrum']:
            # EVM chains use same address
            return self.wallet_addresses.get(network, self.wallet_address)
        elif network == 'bitcoin':
            return self.wallet_addresses['bitcoin']
        elif network == 'solana':
            return self.wallet_addresses['solana']
        else:
            return self.wallet_address
    
    def get_supported_networks(self) -> Dict[str, Any]:
        """Get list of supported blockchain networks"""
        return self.NETWORKS
    
    def get_plan_price_crypto(self, plan: str, network: str = 'polygon', 
                              crypto_price_usd: float = None) -> Dict[str, Any]:
        """
        Calculate plan price in cryptocurrency
        
        Args:
            plan: Plan name (basic, pro, enterprise)
            network: Blockchain network
            crypto_price_usd: Current crypto price in USD (fetch from API if None)
        
        Returns:
            Dictionary with price details
        """
        if plan not in self.PLANS_USD:
            return {'success': False, 'error': 'Invalid plan'}
        
        if network not in self.NETWORKS:
            return {'success': False, 'error': 'Unsupported network'}
        
        plan_price_usd = self.PLANS_USD[plan]
        network_info = self.NETWORKS[network]
        
        # If crypto price not provided, use approximate values
        # In production, fetch from CoinGecko or similar API
        if crypto_price_usd is None:
            crypto_prices = {
                'ETH': 2500.00,
                'MATIC': 0.80,
                'BNB': 300.00
            }
            crypto_price_usd = crypto_prices.get(network_info['currency'], 1.0)
        
        # Calculate amount in crypto
        crypto_amount = plan_price_usd / crypto_price_usd
        
        # Add 1% buffer for price fluctuation
        crypto_amount = crypto_amount * 1.01
        
        return {
            'success': True,
            'plan': plan,
            'usd_price': plan_price_usd,
            'crypto_price': crypto_price_usd,
            'crypto_amount': round(crypto_amount, 6),
            'currency': network_info['currency'],
            'network': network_info['name'],
            'chain_id': network_info['chain_id'],
            'recipient_address': self.get_payment_address(network),
            'min_confirmations': self.min_confirmations
        }
    
    def create_payment_request(self, user_id: str, plan: str, 
                               network: str = None) -> Dict[str, Any]:
        """
        Create a new crypto payment request
        
        Args:
            user_id: User identifier
            plan: Subscription plan
            network: Blockchain network (uses default if None)
        
        Returns:
            Payment request details
        """
        network = network or self.preferred_network
        
        # Get price information
        price_info = self.get_plan_price_crypto(plan, network)
        if not price_info.get('success'):
            return price_info
        
        # Generate unique payment ID
        payment_id = f"crypto_{datetime.now().timestamp()}_{user_id}"
        
        payment_request = {
            'success': True,
            'payment_id': payment_id,
            'user_id': user_id,
            'plan': plan,
            'amount': price_info['crypto_amount'],
            'currency': price_info['currency'],
            'network': network,
            'chain_id': price_info['chain_id'],
            'recipient_address': self.get_payment_address(network),
            'created_at': datetime.now().isoformat(),
            'status': 'pending',
            'explorer_url': f"{self.NETWORKS[network]['explorer']}/address/{self.get_payment_address(network)}"
        }
        
        # Store payment request (implement your storage logic)
        self._store_payment_request(payment_request)
        
        logger.info(f"Created crypto payment request: {payment_id}")
        
        return payment_request
    
    def verify_payment(self, payment_id: str, tx_hash: str) -> Dict[str, Any]:
        """
        Verify a cryptocurrency payment
        
        Args:
            payment_id: Payment request ID
            tx_hash: Transaction hash from blockchain
        
        Returns:
            Verification result
        """
        # In production, verify transaction on blockchain
        # This is a placeholder implementation
        
        logger.info(f"Verifying payment {payment_id} with tx_hash: {tx_hash}")
        
        # Retrieve payment request
        payment_request = self._get_payment_request(payment_id)
        if not payment_request:
            return {'success': False, 'error': 'Payment request not found'}
        
        # Verify transaction on blockchain
        # In production: use Web3.py or similar library to verify
        verification_result = {
            'success': True,
            'payment_id': payment_id,
            'tx_hash': tx_hash,
            'status': 'confirmed',
            'confirmations': 12,  # Placeholder
            'verified_at': datetime.now().isoformat()
        }
        
        # Update payment status
        self._update_payment_status(payment_id, 'confirmed', tx_hash)
        
        return verification_result
    
    def _store_payment_request(self, payment_request: Dict[str, Any]):
        """Store payment request (implement your storage logic)"""
        # Store in database or file
        filename = f"data/crypto_payments/{payment_request['payment_id']}.json"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(payment_request, f, indent=2)
    
    def _get_payment_request(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve payment request"""
        filename = f"data/crypto_payments/{payment_id}.json"
        
        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    def _update_payment_status(self, payment_id: str, status: str, tx_hash: str = None):
        """Update payment status"""
        payment_request = self._get_payment_request(payment_id)
        if payment_request:
            payment_request['status'] = status
            if tx_hash:
                payment_request['tx_hash'] = tx_hash
            payment_request['updated_at'] = datetime.now().isoformat()
            self._store_payment_request(payment_request)
    
    def get_payment_instructions(self, payment_id: str) -> Dict[str, Any]:
        """Get detailed payment instructions"""
        payment_request = self._get_payment_request(payment_id)
        
        if not payment_request:
            return {'success': False, 'error': 'Payment not found'}
        
        network_info = self.NETWORKS[payment_request['network']]
        
        return {
            'success': True,
            'instructions': {
                'step1': f"Connect your MetaMask wallet",
                'step2': f"Switch to {network_info['name']} network",
                'step3': f"Send exactly {payment_request['amount']} {payment_request['currency']}",
                'step4': f"To address: {self.get_payment_address(payment_request['network'])}",
                'step5': "Copy the transaction hash after sending",
                'step6': "Submit the transaction hash for verification"
            },
            'payment_details': payment_request,
            'explorer_url': f"{network_info['explorer']}/address/{self.get_payment_address(payment_request['network'])}",
            'qr_code_data': f"{self.get_payment_address(payment_request['network'])}?amount={payment_request['amount']}"
        }


# Global instance
crypto_processor = CryptoPaymentProcessor()


def get_crypto_processor() -> CryptoPaymentProcessor:
    """Get the global crypto payment processor instance"""
    return crypto_processor
