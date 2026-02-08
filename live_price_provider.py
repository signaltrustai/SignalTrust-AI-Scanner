#!/usr/bin/env python3
"""
Real-time Market Data Provider
Fetches live prices from multiple sources for crypto and stocks
"""

import requests
import time
from typing import Dict, Optional
from datetime import datetime, timedelta


class LivePriceProvider:
    """Fetches real-time prices from multiple market data sources"""
    
    def __init__(self):
        """Initialize live price provider"""
        import os
        self.cache = {}
        self.cache_duration = 30  # Cache prices for 30 seconds
        
        # CoinGecko API key (if available, use demo endpoint for better rate limits)
        self.coingecko_api_key = os.environ.get('COINGECKO_API_KEY', '')
        
        # API endpoints
        if self.coingecko_api_key:
            self.coingecko_base = "https://api.coingecko.com/api/v3"
            self.coingecko_headers = {'x-cg-demo-key': self.coingecko_api_key}
        else:
            self.coingecko_base = "https://api.coingecko.com/api/v3"
            self.coingecko_headers = {}
        self.binance_base = "https://api.binance.com/api/v3"
        self.yahoo_base = "https://query1.finance.yahoo.com/v8/finance"
        
        # Symbol mappings
        self.crypto_id_map = {
            "BTC": "bitcoin", "ETH": "ethereum", "BNB": "binancecoin",
            "XRP": "ripple", "SOL": "solana", "ADA": "cardano",
            "DOGE": "dogecoin", "TRX": "tron", "AVAX": "avalanche-2",
            "LINK": "chainlink", "MATIC": "matic-network", "DOT": "polkadot",
            "UNI": "uniswap", "AAVE": "aave", "MKR": "maker",
            "COMP": "compound-governance-token", "CRV": "curve-dao-token",
            "SUSHI": "sushi", "ATOM": "cosmos", "NEAR": "near",
            "APT": "aptos", "OP": "optimism", "ARB": "arbitrum",
            "SUI": "sui", "INJ": "injective-protocol", "ALGO": "algorand",
            "ICP": "internet-computer", "SHIB": "shiba-inu", "PEPE": "pepe",
            "FLOKI": "floki", "SAND": "the-sandbox", "MANA": "decentraland",
            "AXS": "axie-infinity", "GALA": "gala", "FET": "fetch-ai",
            "RENDER": "render-token", "GRT": "the-graph", "LTC": "litecoin",
            "BCH": "bitcoin-cash", "ETC": "ethereum-classic", "XLM": "stellar",
            "FIL": "filecoin", "THETA": "theta-token", "FTM": "fantom",
            "HBAR": "hedera-hashgraph", "QNT": "quant-network"
        }
    
    def get_live_price(self, symbol: str) -> Optional[float]:
        """Get live price for any symbol (crypto or stock)
        
        Args:
            symbol: Trading symbol (e.g., "BINANCE:BTCUSDT" or "NASDAQ:AAPL")
            
        Returns:
            Live price in USD or None if unavailable
        """
        # Check cache first
        cache_key = symbol
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_duration:
                return cached_data['price']
        
        # Parse symbol
        if ":" in symbol:
            exchange, ticker = symbol.split(":")
        else:
            exchange = ""
            ticker = symbol
        
        # Determine if crypto or stock
        price = None
        if "BINANCE" in exchange.upper() or self._is_crypto(ticker):
            price = self._get_crypto_price(ticker)
        else:
            price = self._get_stock_price(ticker)
        
        # Cache the result
        if price:
            self.cache[cache_key] = {
                'price': price,
                'timestamp': time.time()
            }
        
        return price
    
    def _is_crypto(self, ticker: str) -> bool:
        """Check if ticker is a cryptocurrency"""
        # Remove USDT, BUSD, etc. from ticker
        base_ticker = ticker.replace("USDT", "").replace("BUSD", "").replace("USDC", "")
        return base_ticker.upper() in self.crypto_id_map
    
    def _get_crypto_price(self, ticker: str) -> Optional[float]:
        """Get live crypto price from Binance or CoinGecko
        
        Args:
            ticker: Crypto ticker (e.g., "BTCUSDT" or "BTC")
            
        Returns:
            Live price in USD
        """
        # Try Binance first (fastest and most reliable)
        try:
            if not ticker.endswith("USDT"):
                ticker = ticker + "USDT"
            
            url = f"{self.binance_base}/ticker/price"
            params = {"symbol": ticker.upper()}
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return float(data['price'])
        except Exception as e:
            print(f"Binance API error for {ticker}: {e}")
        
        # Fallback to CoinGecko
        try:
            # Extract base currency
            base = ticker.replace("USDT", "").replace("BUSD", "").replace("USDC", "")
            coin_id = self.crypto_id_map.get(base.upper())
            
            if not coin_id:
                return None
            
            url = f"{self.coingecko_base}/simple/price"
            params = {
                "ids": coin_id,
                "vs_currencies": "usd"
            }
            response = requests.get(url, params=params, headers=self.coingecko_headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if coin_id in data:
                    return float(data[coin_id]['usd'])
        except Exception as e:
            print(f"CoinGecko API error for {ticker}: {e}")
        
        return None
    
    def _get_stock_price(self, ticker: str) -> Optional[float]:
        """Get live stock price from Yahoo Finance
        
        Args:
            ticker: Stock ticker (e.g., "AAPL")
            
        Returns:
            Live price in USD
        """
        try:
            # Yahoo Finance API
            url = f"{self.yahoo_base}/quote"
            params = {"symbols": ticker.upper()}
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, params=params, headers=headers, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if 'quoteResponse' in data and 'result' in data['quoteResponse']:
                    results = data['quoteResponse']['result']
                    if results and len(results) > 0:
                        quote = results[0]
                        # Try different price fields
                        price = quote.get('regularMarketPrice') or quote.get('currentPrice') or quote.get('price')
                        if price:
                            return float(price)
        except Exception as e:
            print(f"Yahoo Finance API error for {ticker}: {e}")
        
        # Fallback: Try alternative stock API
        try:
            # Using Financial Modeling Prep (free tier available)
            url = f"https://financialmodelingprep.com/api/v3/quote-short/{ticker.upper()}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    return float(data[0]['price'])
        except Exception as e:
            print(f"Alternative stock API error for {ticker}: {e}")
        
        return None
    
    def get_multiple_prices(self, symbols: list) -> Dict[str, Optional[float]]:
        """Get live prices for multiple symbols
        
        Args:
            symbols: List of symbols
            
        Returns:
            Dictionary mapping symbols to their prices
        """
        prices = {}
        for symbol in symbols:
            prices[symbol] = self.get_live_price(symbol)
        return prices
    
    def get_market_data(self, symbol: str) -> Dict:
        """Get comprehensive market data for a symbol
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Dictionary with price, volume, change, etc.
        """
        price = self.get_live_price(symbol)
        
        return {
            'symbol': symbol,
            'price': price,
            'timestamp': datetime.now().isoformat(),
            'source': 'live_api',
            'cached': False
        }
    
    def clear_cache(self):
        """Clear price cache to force fresh data"""
        self.cache.clear()


# Global instance
live_price_provider = LivePriceProvider()
