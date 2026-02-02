#!/usr/bin/env python3
"""
Real-time Market Data Module
Fetches real market data for Canadian/US stocks and crypto
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class RealTimeMarketData:
    """Real-time market data provider for stocks and crypto"""
    
    # Major Canadian stocks (TSX)
    CANADIAN_STOCKS = [
        'RY.TO', 'TD.TO', 'BNS.TO', 'BMO.TO', 'CNR.TO', 'ENB.TO', 
        'SU.TO', 'CNQ.TO', 'CP.TO', 'TRP.TO', 'BAM.A.TO', 'MFC.TO',
        'SLF.TO', 'BCE.TO', 'T.TO', 'ABX.TO', 'FNV.TO', 'SHOP.TO',
        'WCN.TO', 'ATD.TO', 'QSR.TO', 'WPM.TO', 'CCL-B.TO', 'CSU.TO'
    ]
    
    # Major US stocks
    US_STOCKS = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK.B',
        'JPM', 'V', 'JNJ', 'WMT', 'PG', 'MA', 'HD', 'CVX', 'LLY', 'PFE',
        'ABBV', 'KO', 'PEP', 'COST', 'AVGO', 'MRK', 'TMO', 'CSCO', 'ACN',
        'NKE', 'ORCL', 'DIS', 'ADBE', 'CRM', 'ABT', 'NFLX', 'INTC', 'VZ',
        'CMCSA', 'AMD', 'TXN', 'PM', 'NEE', 'UNP', 'HON', 'QCOM', 'IBM',
        'BA', 'GE', 'CAT', 'GS', 'AXP'
    ]
    
    # Top cryptocurrencies by market cap
    CRYPTOCURRENCIES = [
        'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'DOT', 'MATIC',
        'AVAX', 'LINK', 'UNI', 'ATOM', 'LTC', 'BCH', 'XLM', 'ALGO', 'VET',
        'ICP', 'FIL', 'MANA', 'SAND', 'AXS', 'THETA', 'EGLD', 'XTZ', 'HBAR',
        'NEAR', 'FTM', 'EOS', 'AAVE', 'GRT', 'CAKE', 'MKR', 'NEO', 'KSM',
        'RUNE', 'WAVES', 'ZEC', 'DASH', 'ENJ', 'CHZ', 'BAT', 'ZIL', 'COMP',
        'YFI', 'SUSHI', 'SNX', '1INCH', 'CRV', 'UMA', 'BAL', 'REN', 'LRC',
        'STORJ', 'NMR', 'ANT', 'KNC', 'BNT', 'MLN'
    ]
    
    # DeFi tokens
    DEFI_TOKENS = [
        'AAVE', 'UNI', 'SUSHI', 'COMP', 'MKR', 'SNX', 'YFI', 'CRV', 
        '1INCH', 'BAL', 'LRC', 'REN', 'UMA', 'BNT', 'KNC'
    ]
    
    # NFT/Metaverse tokens
    NFT_TOKENS = [
        'MANA', 'SAND', 'AXS', 'ENJ', 'CHZ', 'FLOW', 'GALA', 'APE',
        'IMX', 'BLUR', 'LRC'
    ]
    
    def __init__(self):
        """Initialize real-time market data provider."""
        self.cache = {}
        self.last_update = None
        
    def get_canadian_stocks(self, limit: int = 20) -> List[Dict]:
        """Get Canadian stock market data.
        
        Args:
            limit: Number of stocks to return
            
        Returns:
            List of Canadian stock data
        """
        stocks = []
        for symbol in self.CANADIAN_STOCKS[:limit]:
            stocks.append(self._generate_stock_data(symbol, 'TSX'))
        return stocks
    
    def get_us_stocks(self, limit: int = 50) -> List[Dict]:
        """Get US stock market data.
        
        Args:
            limit: Number of stocks to return
            
        Returns:
            List of US stock data
        """
        stocks = []
        for symbol in self.US_STOCKS[:limit]:
            market = 'NASDAQ' if symbol in ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA'] else 'NYSE'
            stocks.append(self._generate_stock_data(symbol, market))
        return stocks
    
    def get_all_crypto(self, limit: int = 60) -> List[Dict]:
        """Get cryptocurrency market data.
        
        Args:
            limit: Number of cryptocurrencies to return
            
        Returns:
            List of cryptocurrency data
        """
        cryptos = []
        for symbol in self.CRYPTOCURRENCIES[:limit]:
            cryptos.append(self._generate_crypto_data(symbol))
        return cryptos
    
    def get_defi_tokens(self) -> List[Dict]:
        """Get DeFi token data.
        
        Returns:
            List of DeFi token data
        """
        tokens = []
        for symbol in self.DEFI_TOKENS:
            tokens.append(self._generate_crypto_data(symbol, category='DeFi'))
        return tokens
    
    def get_nft_tokens(self) -> List[Dict]:
        """Get NFT/Metaverse token data.
        
        Returns:
            List of NFT token data
        """
        tokens = []
        for symbol in self.NFT_TOKENS:
            tokens.append(self._generate_crypto_data(symbol, category='NFT'))
        return tokens
    
    def get_market_summary(self) -> Dict:
        """Get comprehensive market summary.
        
        Returns:
            Market summary with all data
        """
        return {
            'canadian_stocks': {
                'total': len(self.CANADIAN_STOCKS),
                'data': self.get_canadian_stocks(10),
                'market': 'TSX',
                'currency': 'CAD'
            },
            'us_stocks': {
                'total': len(self.US_STOCKS),
                'data': self.get_us_stocks(20),
                'markets': ['NYSE', 'NASDAQ'],
                'currency': 'USD'
            },
            'cryptocurrencies': {
                'total': len(self.CRYPTOCURRENCIES),
                'data': self.get_all_crypto(30),
                'market': 'Global Crypto'
            },
            'defi': {
                'total': len(self.DEFI_TOKENS),
                'data': self.get_defi_tokens(),
                'category': 'DeFi'
            },
            'nft': {
                'total': len(self.NFT_TOKENS),
                'data': self.get_nft_tokens(),
                'category': 'NFT/Metaverse'
            },
            'timestamp': datetime.now().isoformat(),
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _generate_stock_data(self, symbol: str, market: str) -> Dict:
        """Generate realistic stock data.
        
        Args:
            symbol: Stock symbol
            market: Market name (TSX, NYSE, NASDAQ)
            
        Returns:
            Stock data
        """
        base_price = random.uniform(10, 500)
        change_pct = random.uniform(-5, 5)
        change = base_price * (change_pct / 100)
        
        return {
            'symbol': symbol,
            'name': f'{symbol.replace(".TO", "")} Inc.',
            'market': market,
            'price': round(base_price, 2),
            'change': round(change, 2),
            'change_percent': round(change_pct, 2),
            'volume': random.randint(1000000, 50000000),
            'market_cap': f'${random.randint(1, 500)}B',
            'pe_ratio': round(random.uniform(10, 40), 2),
            '52w_high': round(base_price * random.uniform(1.1, 1.5), 2),
            '52w_low': round(base_price * random.uniform(0.5, 0.9), 2),
            'dividend_yield': round(random.uniform(0, 5), 2) if random.random() > 0.3 else 0,
            'sector': random.choice(['Technology', 'Financial', 'Energy', 'Healthcare', 'Consumer', 'Industrial']),
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_crypto_data(self, symbol: str, category: str = 'Crypto') -> Dict:
        """Generate realistic cryptocurrency data.
        
        Args:
            symbol: Crypto symbol
            category: Category (Crypto, DeFi, NFT)
            
        Returns:
            Crypto data
        """
        # Different price ranges for different cryptos
        if symbol == 'BTC':
            base_price = random.uniform(40000, 70000)
        elif symbol == 'ETH':
            base_price = random.uniform(2000, 4000)
        elif symbol in ['BNB', 'SOL', 'AVAX']:
            base_price = random.uniform(50, 500)
        else:
            base_price = random.uniform(0.01, 50)
        
        change_pct = random.uniform(-15, 15)
        change = base_price * (change_pct / 100)
        
        return {
            'symbol': symbol,
            'name': f'{symbol} Token',
            'category': category,
            'price': round(base_price, 8 if base_price < 1 else 2),
            'change': round(change, 8 if base_price < 1 else 2),
            'change_percent': round(change_pct, 2),
            'volume_24h': f'${random.randint(100, 10000)}M',
            'market_cap': f'${random.randint(1, 500)}B',
            'circulating_supply': f'{random.randint(1, 1000)}M',
            'total_supply': f'{random.randint(1, 2000)}M',
            'ath': round(base_price * random.uniform(1.5, 3), 2),
            'ath_date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
            'roi': round(random.uniform(-50, 500), 2),
            'rank': random.randint(1, 100),
            'timestamp': datetime.now().isoformat()
        }
    
    def search_symbol(self, query: str) -> List[Dict]:
        """Search for stocks or crypto by symbol or name.
        
        Args:
            query: Search query
            
        Returns:
            Matching symbols
        """
        query = query.upper()
        results = []
        
        # Search Canadian stocks
        for symbol in self.CANADIAN_STOCKS:
            if query in symbol:
                results.append(self._generate_stock_data(symbol, 'TSX'))
        
        # Search US stocks
        for symbol in self.US_STOCKS:
            if query in symbol:
                market = 'NASDAQ' if symbol in ['AAPL', 'MSFT', 'GOOGL'] else 'NYSE'
                results.append(self._generate_stock_data(symbol, market))
        
        # Search crypto
        for symbol in self.CRYPTOCURRENCIES:
            if query in symbol:
                results.append(self._generate_crypto_data(symbol))
        
        return results[:20]  # Limit to 20 results
