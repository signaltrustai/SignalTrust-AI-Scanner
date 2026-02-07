#!/usr/bin/env python3
"""
TradingView Integration Manager
Handles TradingView charts, symbols, and real-time data integration
"""

import json
import os
from typing import Dict, List, Optional
from datetime import datetime


class TradingViewManager:
    """Manager for TradingView integration and chart handling"""
    
    # Popular symbols for quick access
    POPULAR_CRYPTO = [
        "BINANCE:BTCUSDT", "BINANCE:ETHUSDT", "BINANCE:BNBUSDT",
        "BINANCE:ADAUSDT", "BINANCE:SOLUSDT", "BINANCE:DOGEUSDT",
        "BINANCE:XRPUSDT", "BINANCE:DOTUSDT", "BINANCE:MATICUSDT",
        "BINANCE:AVAXUSDT", "BINANCE:LINKUSDT", "BINANCE:UNIUSDT"
    ]
    
    POPULAR_STOCKS = [
        "NASDAQ:AAPL", "NASDAQ:MSFT", "NASDAQ:GOOGL", "NASDAQ:AMZN",
        "NASDAQ:TSLA", "NASDAQ:NVDA", "NASDAQ:META", "NYSE:JPM",
        "NYSE:V", "NASDAQ:NFLX", "NYSE:DIS", "NYSE:BA"
    ]
    
    # Available timeframes
    TIMEFRAMES = ["1", "5", "15", "30", "60", "240", "D", "W", "M"]
    
    def __init__(self):
        """Initialize TradingView Manager"""
        self.widget_config = self._get_default_widget_config()
    
    def _get_default_widget_config(self) -> Dict:
        """Get default TradingView widget configuration"""
        return {
            "width": "100%",
            "height": 600,
            "autosize": True,
            "symbol": "BINANCE:BTCUSDT",
            "interval": "D",
            "timezone": "Etc/UTC",
            "theme": "dark",
            "style": "1",
            "locale": "en",
            "toolbar_bg": "#f1f3f6",
            "enable_publishing": False,
            "allow_symbol_change": True,
            "studies": [],
            "container_id": "tradingview_chart"
        }
    
    def get_widget_config(self, symbol: str = None, interval: str = None, 
                         studies: List[str] = None) -> Dict:
        """Get TradingView widget configuration
        
        Args:
            symbol: Trading symbol (e.g., "BINANCE:BTCUSDT")
            interval: Chart interval (e.g., "D" for daily)
            studies: List of technical indicators to display
            
        Returns:
            Widget configuration dictionary
        """
        config = self.widget_config.copy()
        
        if symbol:
            config["symbol"] = symbol
        if interval:
            config["interval"] = interval
        if studies:
            config["studies"] = studies
            
        return config
    
    def get_popular_symbols(self, category: str = "all") -> Dict[str, List[str]]:
        """Get popular symbols by category
        
        Args:
            category: "crypto", "stocks", or "all"
            
        Returns:
            Dictionary of symbols by category
        """
        if category == "crypto":
            return {"crypto": self.POPULAR_CRYPTO}
        elif category == "stocks":
            return {"stocks": self.POPULAR_STOCKS}
        else:
            return {
                "crypto": self.POPULAR_CRYPTO,
                "stocks": self.POPULAR_STOCKS
            }
    
    def format_symbol(self, symbol: str, exchange: str = None) -> str:
        """Format symbol for TradingView
        
        Args:
            symbol: Symbol name (e.g., "BTCUSDT")
            exchange: Exchange name (e.g., "BINANCE")
            
        Returns:
            Formatted symbol (e.g., "BINANCE:BTCUSDT")
        """
        if ":" in symbol:
            return symbol
        
        if exchange:
            return f"{exchange.upper()}:{symbol.upper()}"
        
        # Try to detect if crypto or stock
        if "USDT" in symbol.upper() or "BTC" in symbol.upper():
            return f"BINANCE:{symbol.upper()}"
        else:
            return f"NASDAQ:{symbol.upper()}"
    
    def get_available_timeframes(self) -> List[str]:
        """Get available chart timeframes"""
        return self.TIMEFRAMES
    
    def generate_advanced_chart_script(self, symbol: str, interval: str = "D",
                                      studies: List[str] = None) -> str:
        """Generate TradingView advanced chart script
        
        Args:
            symbol: Trading symbol
            interval: Chart interval
            studies: List of technical indicators
            
        Returns:
            JavaScript code for TradingView widget
        """
        config = self.get_widget_config(symbol, interval, studies)
        
        script = f"""
        new TradingView.widget({{
            "autosize": true,
            "symbol": "{config['symbol']}",
            "interval": "{config['interval']}",
            "timezone": "{config['timezone']}",
            "theme": "{config['theme']}",
            "style": "{config['style']}",
            "locale": "{config['locale']}",
            "toolbar_bg": "{config['toolbar_bg']}",
            "enable_publishing": {str(config['enable_publishing']).lower()},
            "allow_symbol_change": {str(config['allow_symbol_change']).lower()},
            "container_id": "{config['container_id']}",
            "height": {config['height']}
        }});
        """
        
        return script
    
    def search_symbols(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for symbols matching query
        
        Args:
            query: Search query
            limit: Maximum results to return
            
        Returns:
            List of matching symbols with metadata
        """
        query_lower = query.lower()
        results = []
        
        # Search in crypto symbols
        for symbol in self.POPULAR_CRYPTO:
            if query_lower in symbol.lower():
                exchange, ticker = symbol.split(":")
                results.append({
                    "symbol": symbol,
                    "ticker": ticker,
                    "exchange": exchange,
                    "type": "crypto",
                    "name": ticker.replace("USDT", " / USDT")
                })
        
        # Search in stock symbols
        for symbol in self.POPULAR_STOCKS:
            if query_lower in symbol.lower():
                exchange, ticker = symbol.split(":")
                results.append({
                    "symbol": symbol,
                    "ticker": ticker,
                    "exchange": exchange,
                    "type": "stock",
                    "name": ticker
                })
        
        return results[:limit]


# Initialize global instance
tradingview_manager = TradingViewManager()
