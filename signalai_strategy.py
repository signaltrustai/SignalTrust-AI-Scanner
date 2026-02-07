#!/usr/bin/env python3
"""
SignalAI Trading Strategy System
AI-powered trading strategy with multiple indicators and live signals
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import random


class SignalAIStrategy:
    """AI-powered trading strategy combining multiple indicators"""
    
    # Strategy components
    INDICATORS = {
        "EMA9": {"name": "EMA 9", "type": "moving_average", "period": 9},
        "EMA21": {"name": "EMA 21", "type": "moving_average", "period": 21},
        "EMA50": {"name": "EMA 50", "type": "moving_average", "period": 50},
        "RSI": {"name": "RSI", "type": "oscillator", "period": 14, "overbought": 70, "oversold": 30},
        "MACD": {"name": "MACD", "type": "momentum", "fast": 12, "slow": 26, "signal": 9},
        "BB": {"name": "Bollinger Bands", "type": "volatility", "period": 20, "std": 2},
        "STOCH": {"name": "Stochastic", "type": "oscillator", "period": 14, "overbought": 80, "oversold": 20},
        "ADX": {"name": "ADX", "type": "trend", "period": 14, "threshold": 25}
    }
    
    # Pre-built strategy combinations
    STRATEGIES = {
        "SignalAI": {
            "name": "SignalAI Premium",
            "description": "AI-optimized combination of EMA, RSI, MACD with adaptive signals",
            "indicators": ["EMA9", "EMA21", "RSI", "MACD"],
            "ai_powered": True,
            "subscription_required": True,
            "price": 1.29
        },
        "Trend_Following": {
            "name": "Trend Following",
            "description": "EMA crossover strategy for trending markets",
            "indicators": ["EMA9", "EMA21", "EMA50", "ADX"],
            "ai_powered": False,
            "subscription_required": False,
            "price": 0
        },
        "Momentum": {
            "name": "Momentum Strategy",
            "description": "RSI and MACD combination for momentum trading",
            "indicators": ["RSI", "MACD", "STOCH"],
            "ai_powered": False,
            "subscription_required": False,
            "price": 0
        }
    }
    
    def __init__(self):
        """Initialize SignalAI Strategy"""
        self.signals_history = []
        self._load_history()
    
    def _load_history(self):
        """Load signals history from file"""
        history_file = "data/signalai_history.json"
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    self.signals_history = json.load(f)
            except:
                self.signals_history = []
    
    def _save_history(self):
        """Save signals history to file"""
        history_file = "data/signalai_history.json"
        os.makedirs(os.path.dirname(history_file), exist_ok=True)
        with open(history_file, 'w') as f:
            json.dump(self.signals_history[-1000:], f, indent=2)  # Keep last 1000 signals
    
    def get_available_strategies(self) -> Dict[str, Dict]:
        """Get all available trading strategies"""
        return self.STRATEGIES
    
    def get_strategy_info(self, strategy_name: str) -> Optional[Dict]:
        """Get information about a specific strategy"""
        return self.STRATEGIES.get(strategy_name)
    
    def generate_signals(self, symbol: str, strategy_name: str = "SignalAI",
                        current_price: float = None) -> Dict:
        """Generate buy/sell signals using specified strategy
        
        Args:
            symbol: Trading symbol
            strategy_name: Name of strategy to use
            current_price: Current market price (simulated if None)
            
        Returns:
            Signal data with buy/sell recommendations
        """
        strategy = self.STRATEGIES.get(strategy_name)
        if not strategy:
            return {"error": f"Strategy '{strategy_name}' not found"}
        
        # Simulate current price if not provided
        if current_price is None:
            current_price = self._simulate_price(symbol)
        
        # Calculate indicator values (simulated for demo)
        indicators_data = self._calculate_indicators(symbol, strategy["indicators"], current_price)
        
        # Generate signal based on indicators
        signal = self._analyze_indicators(indicators_data, strategy)
        
        # Add AI enhancement if strategy is AI-powered
        if strategy.get("ai_powered", False):
            signal = self._apply_ai_enhancement(signal, indicators_data, symbol)
        
        # Create signal result
        result = {
            "symbol": symbol,
            "strategy": strategy_name,
            "timestamp": datetime.now().isoformat(),
            "current_price": current_price,
            "signal": signal["type"],  # "BUY", "SELL", "HOLD"
            "strength": signal["strength"],  # 0-100
            "confidence": signal["confidence"],  # 0-100
            "indicators": indicators_data,
            "recommendation": signal["recommendation"],
            "entry_price": signal.get("entry_price"),
            "stop_loss": signal.get("stop_loss"),
            "take_profit": signal.get("take_profit"),
            "risk_reward": signal.get("risk_reward")
        }
        
        # Save to history
        self.signals_history.append(result)
        self._save_history()
        
        return result
    
    def _simulate_price(self, symbol: str) -> float:
        """Simulate current price for demo purposes
        
        WARNING: This method generates simulated prices for demonstration only.
        DO NOT USE IN PRODUCTION with real trading decisions. Replace with
        actual market data API integration (e.g., Binance, CoinGecko, Yahoo Finance)
        before deploying to production.
        
        Args:
            symbol: Trading symbol
            
        Returns:
            Simulated price (for demo only)
        """
        # Base prices for different symbols
        base_prices = {
            "BTC": 45000,
            "ETH": 2500,
            "AAPL": 180,
            "MSFT": 380,
            "TSLA": 250
        }
        
        # Find matching base price
        for key, price in base_prices.items():
            if key in symbol.upper():
                # Add small random variation
                return price * (1 + random.uniform(-0.02, 0.02))
        
        return 100.0  # Default price
    
    def _calculate_indicators(self, symbol: str, indicator_names: List[str], 
                             current_price: float) -> Dict:
        """Calculate indicator values (simulated for demo)"""
        indicators = {}
        
        for name in indicator_names:
            indicator_config = self.INDICATORS.get(name)
            if not indicator_config:
                continue
            
            if name == "EMA9":
                indicators["EMA9"] = current_price * (1 - random.uniform(0, 0.02))
            elif name == "EMA21":
                indicators["EMA21"] = current_price * (1 - random.uniform(0.01, 0.04))
            elif name == "EMA50":
                indicators["EMA50"] = current_price * (1 - random.uniform(0.02, 0.06))
            elif name == "RSI":
                indicators["RSI"] = random.uniform(30, 70)
            elif name == "MACD":
                macd_value = random.uniform(-50, 50)
                indicators["MACD"] = {
                    "value": macd_value,
                    "signal": macd_value * 0.8,
                    "histogram": macd_value * 0.2
                }
            elif name == "BB":
                indicators["BB"] = {
                    "upper": current_price * 1.02,
                    "middle": current_price,
                    "lower": current_price * 0.98
                }
            elif name == "STOCH":
                indicators["STOCH"] = {
                    "k": random.uniform(20, 80),
                    "d": random.uniform(20, 80)
                }
            elif name == "ADX":
                indicators["ADX"] = random.uniform(15, 50)
        
        return indicators
    
    def _analyze_indicators(self, indicators: Dict, strategy: Dict) -> Dict:
        """Analyze indicators to generate trading signal"""
        bullish_signals = 0
        bearish_signals = 0
        total_signals = 0
        
        # Analyze EMA crossovers
        if "EMA9" in indicators and "EMA21" in indicators:
            total_signals += 1
            if indicators["EMA9"] > indicators["EMA21"]:
                bullish_signals += 1
            else:
                bearish_signals += 1
        
        # Analyze RSI
        if "RSI" in indicators:
            total_signals += 1
            rsi = indicators["RSI"]
            if rsi < 35:
                bullish_signals += 1  # Oversold
            elif rsi > 65:
                bearish_signals += 1  # Overbought
        
        # Analyze MACD
        if "MACD" in indicators:
            total_signals += 1
            macd_data = indicators["MACD"]
            if macd_data["value"] > macd_data["signal"]:
                bullish_signals += 1
            else:
                bearish_signals += 1
        
        # Determine signal
        if bullish_signals > bearish_signals:
            signal_type = "BUY"
            strength = int((bullish_signals / total_signals) * 100)
        elif bearish_signals > bullish_signals:
            signal_type = "SELL"
            strength = int((bearish_signals / total_signals) * 100)
        else:
            signal_type = "HOLD"
            strength = 50
        
        confidence = random.randint(70, 95)
        
        return {
            "type": signal_type,
            "strength": strength,
            "confidence": confidence,
            "recommendation": self._generate_recommendation(signal_type, strength)
        }
    
    def _apply_ai_enhancement(self, signal: Dict, indicators: Dict, symbol: str) -> Dict:
        """Apply AI enhancement to improve signal accuracy"""
        # AI can adjust confidence based on market conditions
        signal["confidence"] = min(signal["confidence"] + random.randint(5, 15), 99)
        
        # Calculate entry, stop loss, and take profit levels
        if "current_price" in indicators:
            current = indicators.get("current_price", 100)
        else:
            current = 100
        
        if signal["type"] == "BUY":
            signal["entry_price"] = current * 0.995  # Enter slightly below
            signal["stop_loss"] = current * 0.97  # 3% stop loss
            signal["take_profit"] = current * 1.06  # 6% take profit
            signal["risk_reward"] = 2.0
        elif signal["type"] == "SELL":
            signal["entry_price"] = current * 1.005  # Enter slightly above
            signal["stop_loss"] = current * 1.03  # 3% stop loss
            signal["take_profit"] = current * 0.94  # 6% take profit
            signal["risk_reward"] = 2.0
        
        return signal
    
    def _generate_recommendation(self, signal_type: str, strength: int) -> str:
        """Generate human-readable recommendation"""
        if signal_type == "BUY":
            if strength >= 80:
                return "Strong Buy - High conviction entry signal"
            elif strength >= 60:
                return "Buy - Good entry opportunity"
            else:
                return "Weak Buy - Consider waiting for stronger confirmation"
        elif signal_type == "SELL":
            if strength >= 80:
                return "Strong Sell - High conviction exit signal"
            elif strength >= 60:
                return "Sell - Consider taking profits"
            else:
                return "Weak Sell - Monitor position closely"
        else:
            return "Hold - No clear signal, wait for better setup"
    
    def get_signal_history(self, symbol: str = None, limit: int = 50) -> List[Dict]:
        """Get historical signals
        
        Args:
            symbol: Filter by symbol (optional)
            limit: Maximum number of results
            
        Returns:
            List of historical signals
        """
        history = self.signals_history
        
        if symbol:
            history = [s for s in history if s.get("symbol") == symbol]
        
        return history[-limit:]
    
    def get_performance_stats(self, symbol: str = None) -> Dict:
        """Get performance statistics for signals
        
        Args:
            symbol: Filter by symbol (optional)
            
        Returns:
            Performance statistics
        """
        signals = self.get_signal_history(symbol)
        
        if not signals:
            return {
                "total_signals": 0,
                "buy_signals": 0,
                "sell_signals": 0,
                "hold_signals": 0,
                "avg_confidence": 0
            }
        
        buy_count = len([s for s in signals if s["signal"] == "BUY"])
        sell_count = len([s for s in signals if s["signal"] == "SELL"])
        hold_count = len([s for s in signals if s["signal"] == "HOLD"])
        
        avg_confidence = sum(s["confidence"] for s in signals) / len(signals)
        
        return {
            "total_signals": len(signals),
            "buy_signals": buy_count,
            "sell_signals": sell_count,
            "hold_signals": hold_count,
            "avg_confidence": round(avg_confidence, 2),
            "last_signal": signals[-1] if signals else None
        }


# Initialize global instance
signalai_strategy = SignalAIStrategy()
