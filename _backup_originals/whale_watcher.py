#!/usr/bin/env python3
"""
Whale Watcher Module
Tracks large crypto/NFT transactions with restricted access
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class WhaleWatcher:
    """Whale transaction tracking with access control"""
    
    # Owner ID - full access
    OWNER_ID = 'owner_admin_001'
    
    # Subscription tiers with whale watcher access
    ALLOWED_TIERS = ['pro', 'enterprise']  # Top 2 tiers
    
    def __init__(self):
        """Initialize whale watcher."""
        self.tracked_wallets = []
        self.transaction_history = []
        
    def check_access(self, user_id: str, user_plan: str) -> bool:
        """Check if user has access to whale watcher.
        
        Args:
            user_id: User ID
            user_plan: User's subscription plan
            
        Returns:
            True if user has access
        """
        # Owner always has access
        if user_id == self.OWNER_ID:
            return True
        
        # Check if user's plan is in allowed tiers
        return user_plan in self.ALLOWED_TIERS
    
    def get_whale_transactions(
        self,
        user_id: str,
        user_plan: str,
        limit: int = 20,
        min_value: float = 100000
    ) -> Dict:
        """Get recent whale transactions.
        
        Args:
            user_id: User ID
            user_plan: User's subscription plan
            limit: Number of transactions to return
            min_value: Minimum transaction value in USD
            
        Returns:
            Whale transactions or access denied
        """
        if not self.check_access(user_id, user_plan):
            return {
                'success': False,
                'error': 'Access denied. Whale Watcher is available only for Pro and Enterprise plans.',
                'required_plans': self.ALLOWED_TIERS,
                'current_plan': user_plan
            }
        
        transactions = self._generate_whale_transactions(limit, min_value)
        
        return {
            'success': True,
            'transactions': transactions,
            'total': len(transactions),
            'min_value_usd': min_value,
            'timestamp': datetime.now().isoformat()
        }
    
    def track_wallet(
        self,
        user_id: str,
        user_plan: str,
        wallet_address: str,
        label: str = ""
    ) -> Dict:
        """Add a wallet to tracking list.
        
        Args:
            user_id: User ID
            user_plan: User's subscription plan
            wallet_address: Wallet address to track
            label: Optional label for the wallet
            
        Returns:
            Result of operation
        """
        if not self.check_access(user_id, user_plan):
            return {
                'success': False,
                'error': 'Access denied. Whale Watcher is available only for Pro and Enterprise plans.'
            }
        
        if wallet_address in [w['address'] for w in self.tracked_wallets]:
            return {
                'success': False,
                'error': 'Wallet is already being tracked'
            }
        
        wallet = {
            'address': wallet_address,
            'label': label or f'Wallet {len(self.tracked_wallets) + 1}',
            'added_by': user_id,
            'added_at': datetime.now().isoformat(),
            'transaction_count': 0
        }
        
        self.tracked_wallets.append(wallet)
        
        return {
            'success': True,
            'wallet': wallet,
            'message': 'Wallet added to tracking list'
        }
    
    def get_nft_whale_movements(
        self,
        user_id: str,
        user_plan: str,
        limit: int = 15
    ) -> Dict:
        """Get NFT whale movements.
        
        Args:
            user_id: User ID
            user_plan: User's subscription plan
            limit: Number of movements to return
            
        Returns:
            NFT whale movements
        """
        if not self.check_access(user_id, user_plan):
            return {
                'success': False,
                'error': 'Access denied. Whale Watcher is available only for Pro and Enterprise plans.'
            }
        
        movements = self._generate_nft_movements(limit)
        
        return {
            'success': True,
            'movements': movements,
            'total': len(movements),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_whale_statistics(
        self,
        user_id: str,
        user_plan: str
    ) -> Dict:
        """Get whale activity statistics.
        
        Args:
            user_id: User ID
            user_plan: User's subscription plan
            
        Returns:
            Whale statistics
        """
        if not self.check_access(user_id, user_plan):
            return {
                'success': False,
                'error': 'Access denied'
            }
        
        return {
            'success': True,
            'stats': {
                'total_transactions_24h': random.randint(50, 200),
                'total_value_24h_usd': f'${random.randint(100, 500)}M',
                'avg_transaction_size': f'${random.randint(500, 2000)}K',
                'most_active_chain': random.choice(['Ethereum', 'Binance Smart Chain', 'Polygon']),
                'top_token': random.choice(['BTC', 'ETH', 'BNB', 'USDT']),
                'whale_count_active': random.randint(500, 1500)
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_whale_transactions(self, limit: int, min_value: float) -> List[Dict]:
        """Generate whale transaction data.
        
        Args:
            limit: Number of transactions
            min_value: Minimum value
            
        Returns:
            List of transactions
        """
        transactions = []
        tokens = ['BTC', 'ETH', 'USDT', 'USDC', 'BNB', 'WBTC', 'WETH']
        chains = ['Ethereum', 'Binance Smart Chain', 'Polygon', 'Avalanche']
        
        for i in range(limit):
            token = random.choice(tokens)
            value_usd = random.uniform(min_value, min_value * 100)
            
            transactions.append({
                'id': f'tx_{random.randint(100000, 999999)}',
                'token': token,
                'amount': round(value_usd / random.uniform(1, 50000), 4),
                'value_usd': round(value_usd, 2),
                'from_address': f'0x{random.randbytes(20).hex()}',
                'to_address': f'0x{random.randbytes(20).hex()}',
                'chain': random.choice(chains),
                'type': random.choice(['transfer', 'swap', 'stake', 'unstake']),
                'timestamp': (datetime.now() - timedelta(minutes=random.randint(1, 1440))).isoformat(),
                'tx_hash': f'0x{random.randbytes(32).hex()}'
            })
        
        # Sort by timestamp descending
        transactions.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return transactions
    
    def _generate_nft_movements(self, limit: int) -> List[Dict]:
        """Generate NFT whale movement data.
        
        Args:
            limit: Number of movements
            
        Returns:
            List of NFT movements
        """
        movements = []
        collections = [
            'Bored Ape Yacht Club',
            'CryptoPunks',
            'Azuki',
            'Mutant Ape Yacht Club',
            'Doodles',
            'CloneX',
            'Moonbirds',
            'Otherside',
            'Pudgy Penguins',
            'DeGods'
        ]
        
        for i in range(limit):
            collection = random.choice(collections)
            floor_price = random.uniform(1, 100)
            sale_price = floor_price * random.uniform(0.5, 3)
            
            movements.append({
                'id': f'nft_{random.randint(100000, 999999)}',
                'collection': collection,
                'token_id': f'#{random.randint(1, 10000)}',
                'sale_price_eth': round(sale_price, 2),
                'sale_price_usd': round(sale_price * random.uniform(1500, 2500), 2),
                'floor_price_eth': round(floor_price, 2),
                'premium': round(((sale_price - floor_price) / floor_price) * 100, 2),
                'from_address': f'0x{random.randbytes(20).hex()[:10]}...',
                'to_address': f'0x{random.randbytes(20).hex()[:10]}...',
                'marketplace': random.choice(['OpenSea', 'Blur', 'LooksRare', 'X2Y2']),
                'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 24))).isoformat(),
                'tx_hash': f'0x{random.randbytes(32).hex()[:16]}...'
            })
        
        # Sort by timestamp descending
        movements.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return movements
