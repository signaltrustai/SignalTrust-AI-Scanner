#!/usr/bin/env python3
"""
Market Analyzer Module
Performs technical and sentiment analysis on market data
Uses real price data from realtime_market_data module
"""

import random
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, List
import math

try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)


class MarketAnalyzer:
    """Analyzer for technical analysis and pattern detection.
    
    Uses real price data from free APIs when available,
    falls back to computed simulated data.
    """
    
    def __init__(self):
        """Initialize market analyzer."""
        self.analysis_cache = {}
        self._cache_ttl = 120  # 2-minute cache
        self._session = requests.Session() if requests else None
        if self._session:
            self._session.headers.update({
                "User-Agent": "SignalTrust-MarketAnalyzer/2.0"
            })

    # ── Public API (aliases used by app.py) ──────────────────────────

    def analyze_technical(self, symbol: str, timeframe: str = '1d') -> Dict:
        """Alias for technical_analysis — called by app.py."""
        return self.technical_analysis(symbol, timeframe)

    def analyze_sentiment(self, symbol: str) -> Dict:
        """Alias for sentiment_analysis — called by app.py."""
        return self.sentiment_analysis(symbol, )
        
    def technical_analysis(self, symbol: str, timeframe: str = '1d') -> Dict:
        """Perform technical analysis on a symbol using real price data.
        
        Args:
            symbol: Symbol to analyze
            timeframe: Timeframe for analysis
            
        Returns:
            Technical analysis results
        """
        cache_key = f"ta_{symbol}_{timeframe}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        # Try to get real historical data
        historical_data = self._fetch_real_historical(symbol, timeframe)
        if not historical_data or len(historical_data) < 20:
            historical_data = self._generate_historical_data(symbol, timeframe)
        
        # Calculate technical indicators from real closes
        indicators = self._calculate_indicators(historical_data)
        
        # Generate analysis summary
        summary = self._generate_technical_summary(indicators)
        
        result = {
            'symbol': symbol,
            'timeframe': timeframe,
            'indicators': indicators,
            'summary': summary,
            'recommendation': self._get_recommendation(indicators),
            'data_source': 'live' if len(historical_data) >= 20 else 'simulated',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        self._set_cached(cache_key, result)
        return result
    
    def sentiment_analysis(self, symbol: str) -> Dict:
        """Analyze market sentiment for a symbol using real data sources.
        
        Args:
            symbol: Symbol to analyze
            
        Returns:
            Sentiment analysis results
        """
        cache_key = f"sent_{symbol}"
        cached = self._get_cached(cache_key)
        if cached:
            return cached

        # Try real sentiment from Alternative.me Fear & Greed
        fear_greed = self._fetch_fear_greed()

        # Try to get real price change as momentum proxy
        momentum_score = self._fetch_momentum(symbol)

        # Combine into sentiment
        fg_score = fear_greed.get('value', 50) if fear_greed else 50
        # Map 0-100 fear-greed to -1..+1
        market_sentiment = (fg_score - 50) / 50.0

        sources = {
            'fear_greed_index': round(market_sentiment, 3),
            'price_momentum': round(momentum_score, 3),
            'market_trend': round((market_sentiment + momentum_score) / 2, 3),
        }
        overall = round(sum(sources.values()) / len(sources), 3)
        sentiment_label = self._get_sentiment_label(overall)
        
        result = {
            'symbol': symbol,
            'overall_sentiment': sentiment_label,
            'sentiment_score': overall,
            'fear_greed_index': fg_score,
            'fear_greed_label': fear_greed.get('value_classification', 'Neutral') if fear_greed else 'Unknown',
            'sources': sources,
            'data_source': 'live' if fear_greed else 'estimated',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        self._set_cached(cache_key, result)
        return result
    
    def detect_patterns(self, symbol: str) -> Dict:
        """Detect chart patterns in price data.
        
        Args:
            symbol: Symbol to analyze
            
        Returns:
            Detected patterns
        """
        # Get real price data to detect patterns from
        historical = self._fetch_real_historical(symbol, '1d')
        if not historical or len(historical) < 30:
            historical = self._generate_historical_data(symbol, '1d')

        closes = [d['close'] for d in historical]
        detected = self._detect_from_prices(closes)

        return {
            'symbol': symbol,
            'patterns_detected': len(detected),
            'patterns': detected,
            'data_source': 'live' if len(historical) >= 30 else 'simulated',
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

    # ── Real data fetchers ───────────────────────────────────────────

    def _fetch_real_historical(self, symbol: str, timeframe: str) -> List[Dict]:
        """Fetch real historical price data from Yahoo Finance chart API."""
        if not self._session:
            return []
        try:
            sym = symbol.upper()
            crypto_map = {
                'BTC': 'BTC-USD', 'ETH': 'ETH-USD', 'BNB': 'BNB-USD',
                'SOL': 'SOL-USD', 'XRP': 'XRP-USD', 'ADA': 'ADA-USD',
                'DOGE': 'DOGE-USD', 'DOT': 'DOT-USD', 'AVAX': 'AVAX-USD',
                'MATIC': 'MATIC-USD', 'LINK': 'LINK-USD', 'UNI': 'UNI-USD',
            }
            ticker = crypto_map.get(sym, sym)
            tf_map = {'1h': ('15m', '5d'), '4h': ('1h', '1mo'),
                      '1d': ('1d', '6mo'), '1w': ('1wk', '2y')}
            interval, rng = tf_map.get(timeframe, ('1d', '6mo'))

            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}"
            resp = self._session.get(url, params={
                'interval': interval, 'range': rng
            }, timeout=10)
            if resp.status_code != 200:
                return []
            data = resp.json()
            res = data.get('chart', {}).get('result', [])
            if not res:
                return []
            ts_list = res[0].get('timestamp', [])
            quote = res[0].get('indicators', {}).get('quote', [{}])[0]
            opens = quote.get('open', [])
            highs = quote.get('high', [])
            lows = quote.get('low', [])
            closes = quote.get('close', [])
            volumes = quote.get('volume', [])

            hist = []
            for i, t in enumerate(ts_list):
                if closes[i] is None:
                    continue
                hist.append({
                    'timestamp': datetime.fromtimestamp(t, tz=timezone.utc).isoformat(),
                    'open': round(opens[i] or closes[i], 2),
                    'high': round(highs[i] or closes[i], 2),
                    'low': round(lows[i] or closes[i], 2),
                    'close': round(closes[i], 2),
                    'volume': int(volumes[i] or 0),
                })
            return hist
        except Exception as e:
            logger.debug(f"Historical fetch failed for {symbol}: {e}")
            return []

    def _fetch_fear_greed(self) -> dict:
        """Fetch Fear & Greed Index from Alternative.me."""
        if not self._session:
            return {}
        try:
            resp = self._session.get("https://api.alternative.me/fng/?limit=1", timeout=8)
            if resp.status_code == 200:
                d = resp.json().get('data', [{}])[0]
                return {'value': int(d.get('value', 50)),
                        'value_classification': d.get('value_classification', 'Neutral')}
        except Exception:
            pass
        return {}

    def _fetch_momentum(self, symbol: str) -> float:
        """Get price momentum score (-1 to +1) from CoinPaprika."""
        if not self._session:
            return 0.0
        try:
            sym = symbol.upper()
            paprika_id = f"{sym.lower()}-{self._crypto_name(sym)}"
            resp = self._session.get(
                f"https://api.coinpaprika.com/v1/tickers/{paprika_id}", timeout=8
            )
            if resp.status_code == 200:
                pct = resp.json().get('quotes', {}).get('USD', {}).get('percent_change_24h', 0)
                return max(-1.0, min(1.0, pct / 20.0))
        except Exception:
            pass
        return 0.0

    @staticmethod
    def _crypto_name(sym: str) -> str:
        names = {
            'BTC': 'bitcoin', 'ETH': 'ethereum', 'BNB': 'binance-coin-weth',
            'SOL': 'solana', 'XRP': 'xrp', 'ADA': 'cardano', 'DOGE': 'dogecoin',
            'DOT': 'polkadot', 'AVAX': 'avalanche', 'MATIC': 'polygon',
            'LINK': 'chainlink', 'UNI': 'uniswap',
        }
        return names.get(sym, sym.lower())

    # ── Caching ──────────────────────────────────────────────────────

    def _get_cached(self, key: str):
        entry = self.analysis_cache.get(key)
        if entry and (datetime.now(timezone.utc) - entry['ts']).total_seconds() < self._cache_ttl:
            return entry['data']
        return None

    def _set_cached(self, key: str, data):
        self.analysis_cache[key] = {'data': data, 'ts': datetime.now(timezone.utc)}

    # ── Pattern detection from real prices ───────────────────────────

    def _detect_from_prices(self, closes: List[float]) -> List[Dict]:
        """Detect chart patterns from closing prices."""
        detected = []
        n = len(closes)
        if n < 30:
            return detected

        # Double bottom
        lows_idx = [i for i in range(5, n - 5) if closes[i] == min(closes[i-5:i+5])]
        if len(lows_idx) >= 2:
            a, b = closes[lows_idx[-2]], closes[lows_idx[-1]]
            if abs(a - b) / max(a, b) < 0.03:
                detected.append({
                    'pattern': 'Double Bottom', 'confidence': round(90 - abs(a-b)/max(a,b)*1000, 1),
                    'timeframe': '1d', 'implication': 'Bullish - Potential upward movement',
                    'detected_at': datetime.now(timezone.utc).isoformat(),
                })

        # Double top
        highs_idx = [i for i in range(5, n - 5) if closes[i] == max(closes[i-5:i+5])]
        if len(highs_idx) >= 2:
            a, b = closes[highs_idx[-2]], closes[highs_idx[-1]]
            if abs(a - b) / max(a, b) < 0.03:
                detected.append({
                    'pattern': 'Double Top', 'confidence': round(90 - abs(a-b)/max(a,b)*1000, 1),
                    'timeframe': '1d', 'implication': 'Bearish - Potential downward movement',
                    'detected_at': datetime.now(timezone.utc).isoformat(),
                })

        # Trend channel
        recent = closes[-20:]
        avg_first = sum(recent[:10]) / 10
        avg_last = sum(recent[10:]) / 10
        pct = (avg_last - avg_first) / avg_first
        if pct > 0.05:
            detected.append({
                'pattern': 'Channel (Upward)', 'confidence': round(min(95, 70 + pct*200), 1),
                'timeframe': '1d', 'implication': 'Bullish - Potential upward movement',
                'detected_at': datetime.now(timezone.utc).isoformat(),
            })
        elif pct < -0.05:
            detected.append({
                'pattern': 'Channel (Downward)', 'confidence': round(min(95, 70 + abs(pct)*200), 1),
                'timeframe': '1d', 'implication': 'Bearish - Potential downward movement',
                'detected_at': datetime.now(timezone.utc).isoformat(),
            })
        return detected
    
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
        """Calculate technical indicators from real price data.
        
        Args:
            historical_data: Historical price data
            
        Returns:
            Technical indicators
        """
        closes = [d['close'] for d in historical_data]
        current_price = closes[-1]
        
        # Simple Moving Averages
        sma_20 = sum(closes[-20:]) / min(20, len(closes))
        sma_50 = sum(closes[-50:]) / min(50, len(closes))
        sma_200 = sum(closes[-200:]) / min(200, len(closes))
        
        # RSI (Relative Strength Index) — computed from real closes
        rsi = self._compute_rsi(closes, period=14)
        
        # MACD — computed from real closes
        macd_line, signal_line = self._compute_macd(closes)
        
        # Bollinger Bands — computed from real closes
        bb_sma = sum(closes[-20:]) / min(20, len(closes))
        bb_std = (sum((c - bb_sma) ** 2 for c in closes[-20:]) / min(20, len(closes))) ** 0.5
        bb_upper = bb_sma + 2 * bb_std
        bb_lower = bb_sma - 2 * bb_std
        
        return {
            'current_price': round(current_price, 2),
            'sma_20': round(sma_20, 2),
            'sma_50': round(sma_50, 2),
            'sma_200': round(sma_200, 2),
            'rsi': round(rsi, 2),
            'macd': round(macd_line, 3),
            'macd_signal': round(signal_line, 3),
            'bollinger_upper': round(bb_upper, 2),
            'bollinger_lower': round(bb_lower, 2),
            'volume_avg': sum([d['volume'] for d in historical_data[-20:]]) // max(1, min(20, len(historical_data)))
        }

    @staticmethod
    def _compute_rsi(closes: List[float], period: int = 14) -> float:
        """Compute RSI from closing prices."""
        if len(closes) < period + 1:
            return 50.0
        deltas = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        recent = deltas[-(period):]
        gains = [d for d in recent if d > 0]
        losses = [-d for d in recent if d < 0]
        avg_gain = sum(gains) / period if gains else 0.0001
        avg_loss = sum(losses) / period if losses else 0.0001
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def _compute_macd(closes: List[float]) -> tuple:
        """Compute MACD line and signal line from closing prices."""
        def ema(data, period):
            if len(data) < period:
                return data[-1] if data else 0
            k = 2 / (period + 1)
            val = sum(data[:period]) / period
            for price in data[period:]:
                val = price * k + val * (1 - k)
            return val
        ema12 = ema(closes, 12)
        ema26 = ema(closes, 26)
        macd_line = ema12 - ema26
        # Signal is 9-period EMA of MACD — approximate with simple diff
        signal = macd_line * 0.8  # Simplified
        return macd_line, signal
    
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
            'confidence': round(min(95, 60 + abs(score) * 8), 1)
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
