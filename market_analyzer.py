#!/usr/bin/env python3
"""
Market Analyzer Module
Performs technical and sentiment analysis on market data
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List
import math


class MarketAnalyzer:
    """Analyzer for technical analysis and pattern detection"""
    
    def __init__(self):
        """Initialize market analyzer."""
        self.analysis_cache = {}
        
    def technical_analysis(self, symbol: str, timeframe: str = '1d') -> Dict:
        """Perform technical analysis on a symbol.
        
        Args:
            symbol: Symbol to analyze
            timeframe: Timeframe for analysis
            
        Returns:
            Technical analysis results
        """
        # Generate historical price data
        historical_data = self._generate_historical_data(symbol, timeframe)
        
        # Calculate technical indicators
        indicators = self._calculate_indicators(historical_data)
        
        # Generate analysis summary
        summary = self._generate_technical_summary(indicators)
        
        return {
            'symbol': symbol,
            'timeframe': timeframe,
            'indicators': indicators,
            'summary': summary,
            'recommendation': self._get_recommendation(indicators),
            'timestamp': datetime.now().isoformat()
        }
    
    def sentiment_analysis(self, symbol: str) -> Dict:
        """Analyze market sentiment for a symbol.
        
        Args:
            symbol: Symbol to analyze
            
        Returns:
            Sentiment analysis results
        """
        # Simulate sentiment data from various sources
        sentiment_score = random.uniform(-1, 1)  # -1 (bearish) to 1 (bullish)
        
        sources = {
            'social_media': random.uniform(-1, 1),
            'news': random.uniform(-1, 1),
            'analyst_ratings': random.uniform(-1, 1),
            'market_momentum': random.uniform(-1, 1)
        }
        
        sentiment_label = self._get_sentiment_label(sentiment_score)
        
        return {
            'symbol': symbol,
            'overall_sentiment': sentiment_label,
            'sentiment_score': round(sentiment_score, 3),
            'sources': {k: round(v, 3) for k, v in sources.items()},
            'social_mentions': random.randint(1000, 50000),
            'news_articles': random.randint(10, 200),
            'analyst_count': random.randint(5, 50),
            'timestamp': datetime.now().isoformat()
        }
    
    def detect_patterns(self, symbol: str) -> Dict:
        """Detect chart patterns in price data.
        
        Args:
            symbol: Symbol to analyze
            
        Returns:
            Detected patterns
        """
        # Common chart patterns
        all_patterns = [
            'Head and Shoulders',
            'Inverse Head and Shoulders',
            'Double Top',
            'Double Bottom',
            'Triangle (Ascending)',
            'Triangle (Descending)',
            'Triangle (Symmetrical)',
            'Flag Pattern',
            'Pennant Pattern',
            'Cup and Handle',
            'Wedge (Rising)',
            'Wedge (Falling)',
            'Channel (Upward)',
            'Channel (Downward)'
        ]
        
        # Randomly detect 2-4 patterns
        num_patterns = random.randint(2, 4)
        detected = []
        
        for pattern in random.sample(all_patterns, num_patterns):
            confidence = random.uniform(60, 95)
            timeframe = random.choice(['1h', '4h', '1d', '1w'])
            
            detected.append({
                'pattern': pattern,
                'confidence': round(confidence, 1),
                'timeframe': timeframe,
                'implication': self._get_pattern_implication(pattern),
                'detected_at': datetime.now().isoformat()
            })
        
        return {
            'symbol': symbol,
            'patterns_detected': len(detected),
            'patterns': detected,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_historical_data(self, symbol: str, timeframe: str) -> List[Dict]:
        """Generate simulated historical price data.
        
        Args:
            symbol: Symbol
            timeframe: Timeframe
            
        Returns:
            Historical data points
        """
        num_points = 100
        base_price = random.uniform(50, 500)
        data = []
        
        for i in range(num_points):
            # Random walk with drift
            change = random.gauss(0, 2)
            base_price = max(1, base_price + change)
            
            data.append({
                'timestamp': (datetime.now() - timedelta(days=num_points-i)).isoformat(),
                'open': round(base_price, 2),
                'high': round(base_price * random.uniform(1.0, 1.05), 2),
                'low': round(base_price * random.uniform(0.95, 1.0), 2),
                'close': round(base_price, 2),
                'volume': random.randint(1000000, 50000000)
            })
        
        return data
    
    def _calculate_indicators(self, historical_data: List[Dict]) -> Dict:
        """Calculate technical indicators.
        
        Args:
            historical_data: Historical price data
            
        Returns:
            Technical indicators
        """
        closes = [d['close'] for d in historical_data]
        current_price = closes[-1]
        
        # Simple Moving Averages
        sma_20 = sum(closes[-20:]) / 20
        sma_50 = sum(closes[-50:]) / 50
        sma_200 = sum(closes[-200:]) / len(closes[-200:]) if len(closes) >= 200 else sum(closes) / len(closes)
        
        # RSI (Relative Strength Index) - simplified
        rsi = random.uniform(20, 80)
        
        # MACD - simplified
        macd = random.uniform(-5, 5)
        macd_signal = random.uniform(-5, 5)
        
        # Bollinger Bands - simplified
        bb_upper = current_price * random.uniform(1.02, 1.08)
        bb_lower = current_price * random.uniform(0.92, 0.98)
        
        return {
            'current_price': round(current_price, 2),
            'sma_20': round(sma_20, 2),
            'sma_50': round(sma_50, 2),
            'sma_200': round(sma_200, 2),
            'rsi': round(rsi, 2),
            'macd': round(macd, 3),
            'macd_signal': round(macd_signal, 3),
            'bollinger_upper': round(bb_upper, 2),
            'bollinger_lower': round(bb_lower, 2),
            'volume_avg': sum([d['volume'] for d in historical_data[-20:]]) // 20
        }
    
    def _generate_technical_summary(self, indicators: Dict) -> Dict:
        """Generate technical analysis summary.
        
        Args:
            indicators: Technical indicators
            
        Returns:
            Summary
        """
        price = indicators['current_price']
        sma_20 = indicators['sma_20']
        sma_50 = indicators['sma_50']
        rsi = indicators['rsi']
        
        # Trend analysis
        if price > sma_20 > sma_50:
            trend = 'Strong Uptrend'
        elif price > sma_20:
            trend = 'Uptrend'
        elif price < sma_20 < sma_50:
            trend = 'Strong Downtrend'
        elif price < sma_20:
            trend = 'Downtrend'
        else:
            trend = 'Sideways'
        
        # RSI interpretation
        if rsi > 70:
            rsi_status = 'Overbought'
        elif rsi < 30:
            rsi_status = 'Oversold'
        else:
            rsi_status = 'Neutral'
        
        # Momentum
        momentum = 'Bullish' if indicators['macd'] > indicators['macd_signal'] else 'Bearish'
        
        return {
            'trend': trend,
            'rsi_status': rsi_status,
            'momentum': momentum,
            'support_level': indicators['bollinger_lower'],
            'resistance_level': indicators['bollinger_upper']
        }
    
    def _get_recommendation(self, indicators: Dict) -> Dict:
        """Get trading recommendation based on indicators.
        
        Args:
            indicators: Technical indicators
            
        Returns:
            Recommendation
        """
        score = 0
        
        # Price vs SMA
        if indicators['current_price'] > indicators['sma_20']:
            score += 1
        if indicators['current_price'] > indicators['sma_50']:
            score += 1
        
        # RSI
        if indicators['rsi'] < 30:
            score += 2  # Oversold - buy signal
        elif indicators['rsi'] > 70:
            score -= 2  # Overbought - sell signal
        
        # MACD
        if indicators['macd'] > indicators['macd_signal']:
            score += 1
        
        # Determine recommendation
        if score >= 3:
            action = 'STRONG BUY'
        elif score >= 1:
            action = 'BUY'
        elif score <= -3:
            action = 'STRONG SELL'
        elif score <= -1:
            action = 'SELL'
        else:
            action = 'HOLD'
        
        return {
            'action': action,
            'score': score,
            'confidence': round(random.uniform(65, 90), 1)
        }
    
    def _get_sentiment_label(self, score: float) -> str:
        """Get sentiment label from score.
        
        Args:
            score: Sentiment score
            
        Returns:
            Sentiment label
        """
        if score > 0.5:
            return 'Very Bullish'
        elif score > 0.2:
            return 'Bullish'
        elif score > -0.2:
            return 'Neutral'
        elif score > -0.5:
            return 'Bearish'
        else:
            return 'Very Bearish'
    
    def _get_pattern_implication(self, pattern: str) -> str:
        """Get implication of a chart pattern.
        
        Args:
            pattern: Pattern name
            
        Returns:
            Implication
        """
        bullish_patterns = [
            'Inverse Head and Shoulders',
            'Double Bottom',
            'Triangle (Ascending)',
            'Cup and Handle',
            'Wedge (Falling)',
            'Channel (Upward)'
        ]
        
        bearish_patterns = [
            'Head and Shoulders',
            'Double Top',
            'Triangle (Descending)',
            'Wedge (Rising)',
            'Channel (Downward)'
        ]
        
        if any(p in pattern for p in bullish_patterns):
            return 'Bullish - Potential upward movement'
        elif any(p in pattern for p in bearish_patterns):
            return 'Bearish - Potential downward movement'
        else:
            return 'Neutral - Continuation or breakout possible'
