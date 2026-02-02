#!/usr/bin/env python3
"""
Market Scanner Module
Scans various markets for opportunities and trends
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List


class MarketScanner:
    """Scanner for multiple market types (stocks, crypto, forex, etc.)"""
    
    def __init__(self):
        """Initialize market scanner."""
        self.watchlist = []
        self.scan_history = []
        
    def get_markets_overview(self) -> Dict:
        """Get overview of all major markets.
        
        Returns:
            Dictionary with market overview data
        """
        return {
            'stocks': {
                'total_scanned': 500,
                'trending_up': 245,
                'trending_down': 180,
                'neutral': 75,
                'top_gainers': self._get_sample_stocks(5, trend='up'),
                'top_losers': self._get_sample_stocks(5, trend='down'),
                'most_active': self._get_sample_stocks(5, trend='active')
            },
            'crypto': {
                'total_scanned': 100,
                'trending_up': 55,
                'trending_down': 35,
                'neutral': 10,
                'top_performers': self._get_sample_crypto(5)
            },
            'forex': {
                'total_pairs': 50,
                'major_pairs': self._get_sample_forex(5)
            },
            'indices': {
                'major_indices': self._get_sample_indices()
            }
        }
    
    def scan_market(self, market_type: str, symbols: List[str]) -> Dict:
        """Scan specific market symbols.
        
        Args:
            market_type: Type of market (stocks, crypto, forex)
            symbols: List of symbols to scan
            
        Returns:
            Scan results
        """
        results = {
            'market_type': market_type,
            'symbols_scanned': len(symbols),
            'results': []
        }
        
        for symbol in symbols:
            scan_result = self._scan_symbol(symbol, market_type)
            results['results'].append(scan_result)
            
        self.scan_history.append({
            'timestamp': datetime.now().isoformat(),
            'market_type': market_type,
            'symbols': symbols
        })
        
        return results
    
    def get_trending_assets(self, market_type: str) -> List[Dict]:
        """Get trending assets in a market.
        
        Args:
            market_type: Type of market
            
        Returns:
            List of trending assets
        """
        if market_type == 'stocks':
            return self._get_sample_stocks(20, trend='trending')
        elif market_type == 'crypto':
            return self._get_sample_crypto(20)
        elif market_type == 'forex':
            return self._get_sample_forex(20)
        else:
            return []
    
    def get_watchlist(self) -> List[Dict]:
        """Get user's watchlist.
        
        Returns:
            List of watched symbols with current data
        """
        if not self.watchlist:
            # Default watchlist
            self.watchlist = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
        
        return [self._scan_symbol(symbol, 'stocks') for symbol in self.watchlist]
    
    def add_to_watchlist(self, symbol: str) -> Dict:
        """Add symbol to watchlist.
        
        Args:
            symbol: Symbol to add
            
        Returns:
            Result of operation
        """
        if symbol not in self.watchlist:
            self.watchlist.append(symbol)
            return {'added': True, 'symbol': symbol, 'watchlist_size': len(self.watchlist)}
        return {'added': False, 'message': 'Symbol already in watchlist'}
    
    def remove_from_watchlist(self, symbol: str) -> Dict:
        """Remove symbol from watchlist.
        
        Args:
            symbol: Symbol to remove
            
        Returns:
            Result of operation
        """
        if symbol in self.watchlist:
            self.watchlist.remove(symbol)
            return {'removed': True, 'symbol': symbol, 'watchlist_size': len(self.watchlist)}
        return {'removed': False, 'message': 'Symbol not in watchlist'}
    
    def _scan_symbol(self, symbol: str, market_type: str) -> Dict:
        """Scan a single symbol.
        
        Args:
            symbol: Symbol to scan
            market_type: Type of market
            
        Returns:
            Scan result
        """
        # Simulate real market data
        base_price = random.uniform(10, 500)
        change_pct = random.uniform(-10, 10)
        
        return {
            'symbol': symbol,
            'name': f'{symbol} {"Corp" if market_type == "stocks" else ""}',
            'market_type': market_type,
            'price': round(base_price, 2),
            'change': round(base_price * change_pct / 100, 2),
            'change_percent': round(change_pct, 2),
            'volume': random.randint(1000000, 100000000),
            'market_cap': f'${random.randint(1, 500)}B',
            'signals': self._generate_signals(),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_signals(self) -> Dict:
        """Generate trading signals.
        
        Returns:
            Signal data
        """
        signals = ['BUY', 'SELL', 'HOLD']
        strengths = ['STRONG', 'MODERATE', 'WEAK']
        
        return {
            'signal': random.choice(signals),
            'strength': random.choice(strengths),
            'confidence': round(random.uniform(60, 95), 1)
        }
    
    def _get_sample_stocks(self, count: int, trend: str = 'up') -> List[Dict]:
        """Get sample stock data.
        
        Args:
            count: Number of stocks to return
            trend: Trend type (up, down, active, trending)
            
        Returns:
            List of stock data
        """
        symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META', 'BRK.B', 
                   'JPM', 'V', 'JNJ', 'WMT', 'PG', 'MA', 'HD', 'CVX', 'LLY', 'PFE']
        
        results = []
        for symbol in random.sample(symbols, min(count, len(symbols))):
            price = random.uniform(50, 500)
            if trend == 'up':
                change = random.uniform(3, 15)
            elif trend == 'down':
                change = random.uniform(-15, -3)
            else:
                change = random.uniform(-5, 5)
            
            results.append({
                'symbol': symbol,
                'price': round(price, 2),
                'change_percent': round(change, 2),
                'volume': random.randint(10000000, 200000000)
            })
        
        return results
    
    def _get_sample_crypto(self, count: int) -> List[Dict]:
        """Get sample cryptocurrency data.
        
        Args:
            count: Number of cryptos to return
            
        Returns:
            List of crypto data
        """
        symbols = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'DOT', 
                   'MATIC', 'AVAX', 'LINK', 'UNI', 'ATOM', 'LTC']
        
        results = []
        for symbol in random.sample(symbols, min(count, len(symbols))):
            price = random.uniform(0.1, 50000)
            change = random.uniform(-20, 20)
            
            results.append({
                'symbol': symbol,
                'price': round(price, 2),
                'change_percent': round(change, 2),
                'volume_24h': f'${random.randint(100, 10000)}M'
            })
        
        return results
    
    def _get_sample_forex(self, count: int) -> List[Dict]:
        """Get sample forex pair data.
        
        Args:
            count: Number of pairs to return
            
        Returns:
            List of forex data
        """
        pairs = ['EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD', 
                 'USD/CAD', 'NZD/USD', 'EUR/GBP', 'EUR/JPY']
        
        results = []
        for pair in random.sample(pairs, min(count, len(pairs))):
            rate = random.uniform(0.5, 2.0)
            change = random.uniform(-2, 2)
            
            results.append({
                'pair': pair,
                'rate': round(rate, 4),
                'change_percent': round(change, 3)
            })
        
        return results
    
    def _get_sample_indices(self) -> List[Dict]:
        """Get major market indices.
        
        Returns:
            List of index data
        """
        indices = [
            {'name': 'S&P 500', 'symbol': 'SPX', 'value': 4500 + random.uniform(-100, 100)},
            {'name': 'Dow Jones', 'symbol': 'DJI', 'value': 35000 + random.uniform(-500, 500)},
            {'name': 'NASDAQ', 'symbol': 'IXIC', 'value': 14000 + random.uniform(-300, 300)},
            {'name': 'Russell 2000', 'symbol': 'RUT', 'value': 2000 + random.uniform(-50, 50)}
        ]
        
        for index in indices:
            index['value'] = round(index['value'], 2)
            index['change_percent'] = round(random.uniform(-2, 2), 2)
        
        return indices
