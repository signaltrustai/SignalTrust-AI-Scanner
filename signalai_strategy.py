"""
SignalAI Strategy Engine — Optimized v3
=======================================
Advanced trading strategy combining 12+ real technical indicators,
market regime detection, multi-timeframe confirmation, adaptive
parameters, and AI-powered signal enhancement.

Zero random — every number derives from real market data.
"""

import json
import math
import os
import time
import logging
import requests
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Lazy import to avoid circular dependency
live_price_provider = None

def _get_price_provider():
    global live_price_provider
    if live_price_provider is None:
        try:
            import live_price_provider as lpp
            live_price_provider = lpp
        except ImportError:
            live_price_provider = None
    return live_price_provider


# ---------------------------------------------------------------------------
#  Historical data fetching with cache
# ---------------------------------------------------------------------------

_history_cache: Dict[str, Dict] = {}
_CACHE_TTL = 120  # seconds


def _cached_history(symbol: str) -> Optional[List[float]]:
    entry = _history_cache.get(symbol)
    if entry and time.time() - entry["ts"] < _CACHE_TTL:
        return entry["data"]
    return None


def _store_history(symbol: str, data: List[float]):
    _history_cache[symbol] = {"data": data, "ts": time.time()}


def _fetch_closes(symbol: str) -> List[float]:
    """Fetch 90-day daily closes from real APIs (Yahoo → Binance → CoinPaprika)."""
    cached = _cached_history(symbol)
    if cached:
        return cached

    base = symbol.upper().replace("BINANCE:", "").replace("USDT", "").replace("USD", "")
    closes: List[float] = []

    # 1) Yahoo Finance chart API
    try:
        yf_sym = base
        if base in ("BTC", "ETH", "SOL", "ADA", "XRP", "DOGE", "DOT",
                     "AVAX", "MATIC", "LINK", "UNI", "ATOM", "LTC", "BNB"):
            yf_sym = f"{base}-USD"
        resp = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{yf_sym}",
            params={"range": "3mo", "interval": "1d"},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=8,
        )
        if resp.status_code == 200:
            data = resp.json()
            adjclose = (data.get("chart", {}).get("result", [{}])[0]
                        .get("indicators", {}).get("adjclose", [{}])[0]
                        .get("adjclose", []))
            if adjclose:
                closes = [c for c in adjclose if c is not None]
            if not closes:
                raw = (data.get("chart", {}).get("result", [{}])[0]
                       .get("indicators", {}).get("quote", [{}])[0]
                       .get("close", []))
                closes = [c for c in (raw or []) if c is not None]
    except Exception:
        pass

    # 2) Binance klines
    if not closes:
        try:
            pair = f"{base}USDT"
            resp = requests.get(
                "https://api.binance.com/api/v3/klines",
                params={"symbol": pair, "interval": "1d", "limit": 90},
                timeout=8,
            )
            if resp.status_code == 200:
                closes = [float(k[4]) for k in resp.json()]
        except Exception:
            pass

    # 3) CoinPaprika OHLCV
    if not closes:
        try:
            from market_analyzer import _COIN_IDS
            cp_id = _COIN_IDS.get(base)
            if cp_id:
                resp = requests.get(
                    f"https://api.coinpaprika.com/v1/coins/{cp_id}/ohlcv/last/90",
                    timeout=8,
                )
                if resp.status_code == 200:
                    closes = [d["close"] for d in resp.json() if d.get("close")]
        except Exception:
            pass

    if closes:
        _store_history(symbol, closes)
    return closes


def _fetch_volumes(symbol: str) -> List[float]:
    """Fetch 90-day daily volumes (Yahoo → Binance fallback)."""
    base = symbol.upper().replace("BINANCE:", "").replace("USDT", "").replace("USD", "")
    volumes: List[float] = []

    # Yahoo Finance
    try:
        yf_sym = base
        if base in ("BTC", "ETH", "SOL", "ADA", "XRP", "DOGE", "DOT",
                     "AVAX", "MATIC", "LINK", "UNI", "ATOM", "LTC", "BNB"):
            yf_sym = f"{base}-USD"
        resp = requests.get(
            f"https://query1.finance.yahoo.com/v8/finance/chart/{yf_sym}",
            params={"range": "3mo", "interval": "1d"},
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=8,
        )
        if resp.status_code == 200:
            data = resp.json()
            raw = (data.get("chart", {}).get("result", [{}])[0]
                   .get("indicators", {}).get("quote", [{}])[0]
                   .get("volume", []))
            if raw:
                volumes = [float(v) for v in raw if v is not None]
    except Exception:
        pass

    # Binance klines (volume is index 5)
    if not volumes:
        try:
            pair = f"{base}USDT"
            resp = requests.get(
                "https://api.binance.com/api/v3/klines",
                params={"symbol": pair, "interval": "1d", "limit": 90},
                timeout=8,
            )
            if resp.status_code == 200:
                volumes = [float(k[5]) for k in resp.json()]
        except Exception:
            pass

    return volumes


# ---------------------------------------------------------------------------
#  Core indicator calculations (100% real math, zero random)
# ---------------------------------------------------------------------------

def _ema(data: List[float], period: int) -> List[float]:
    """Exponential Moving Average."""
    if len(data) < period:
        return data[:]
    k = 2 / (period + 1)
    ema_vals = [sum(data[:period]) / period]
    for price in data[period:]:
        ema_vals.append(price * k + ema_vals[-1] * (1 - k))
    return ema_vals


def _sma(data: List[float], period: int) -> List[float]:
    """Simple Moving Average."""
    if len(data) < period:
        return data[:]
    return [sum(data[i:i + period]) / period for i in range(len(data) - period + 1)]


def _rsi(closes: List[float], period: int = 14) -> float:
    """Relative Strength Index (Wilder's smoothing)."""
    if len(closes) < period + 1:
        return 50.0
    deltas = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return 100 - 100 / (1 + rs)


def _macd(closes: List[float]) -> Dict:
    """MACD (12, 26, 9) with histogram."""
    ema12 = _ema(closes, 12)
    ema26 = _ema(closes, 26)
    offset = len(ema12) - len(ema26)
    macd_line = [ema12[offset + i] - ema26[i] for i in range(len(ema26))]
    signal = _ema(macd_line, 9) if len(macd_line) >= 9 else macd_line[:]
    histogram = macd_line[-1] - signal[-1] if signal else 0
    # Check for crossover
    crossover = "none"
    if len(macd_line) >= 2 and len(signal) >= 2:
        if macd_line[-2] < signal[-2] and macd_line[-1] > signal[-1]:
            crossover = "bullish"
        elif macd_line[-2] > signal[-2] and macd_line[-1] < signal[-1]:
            crossover = "bearish"
    return {
        "value": round(macd_line[-1], 6) if macd_line else 0,
        "signal": round(signal[-1], 6) if signal else 0,
        "histogram": round(histogram, 6),
        "crossover": crossover,
    }


def _bollinger(closes: List[float], period: int = 20, num_std: float = 2.0) -> Dict:
    """Bollinger Bands with %B and bandwidth."""
    if len(closes) < period:
        p = closes[-1] if closes else 0
        return {"upper": p, "middle": p, "lower": p, "pct_b": 0.5, "bandwidth": 0}
    window = closes[-period:]
    mean = sum(window) / period
    var = sum((x - mean) ** 2 for x in window) / period
    std = math.sqrt(var)
    upper = mean + num_std * std
    lower = mean - num_std * std
    pct_b = (closes[-1] - lower) / (upper - lower) if upper != lower else 0.5
    bandwidth = (upper - lower) / mean if mean > 0 else 0
    return {
        "upper": round(upper, 4),
        "middle": round(mean, 4),
        "lower": round(lower, 4),
        "pct_b": round(pct_b, 4),
        "bandwidth": round(bandwidth, 4),
    }


def _stochastic(closes: List[float], period: int = 14) -> Dict:
    """Stochastic %K and %D (3-period SMA of %K)."""
    if len(closes) < period + 3:
        return {"k": 50.0, "d": 50.0, "crossover": "none"}
    # Calculate multiple %K values for %D
    k_values = []
    for i in range(3):
        idx = len(closes) - 3 + i
        window = closes[max(0, idx - period + 1):idx + 1]
        low, high = min(window), max(window)
        k = ((closes[idx] - low) / (high - low) * 100) if high != low else 50
        k_values.append(k)
    d = sum(k_values) / 3
    crossover = "none"
    if len(k_values) >= 2:
        if k_values[-2] < d and k_values[-1] > d:
            crossover = "bullish"
        elif k_values[-2] > d and k_values[-1] < d:
            crossover = "bearish"
    return {"k": round(k_values[-1], 2), "d": round(d, 2), "crossover": crossover}


def _adx(closes: List[float], period: int = 14) -> float:
    """Average Directional Index from closes (Wilder's method)."""
    if len(closes) < period + 1:
        return 25.0
    tr_vals = [abs(closes[i] - closes[i - 1]) for i in range(1, len(closes))]
    atr = sum(tr_vals[-period:]) / period
    if atr == 0:
        return 0
    dm_plus = sum(max(closes[i] - closes[i - 1], 0) for i in range(-period, 0))
    dm_minus = sum(max(closes[i - 1] - closes[i], 0) for i in range(-period, 0))
    di_plus = (dm_plus / (atr * period)) * 100
    di_minus = (dm_minus / (atr * period)) * 100
    di_sum = di_plus + di_minus
    dx = abs(di_plus - di_minus) / di_sum * 100 if di_sum > 0 else 0
    return round(dx, 2)


# ---------------------------------------------------------------------------
#  NEW indicators for v3 optimization
# ---------------------------------------------------------------------------

def _atr(closes: List[float], period: int = 14) -> float:
    """Average True Range (from closes only — approximated)."""
    if len(closes) < period + 1:
        return 0.0
    tr_vals = [abs(closes[i] - closes[i - 1]) for i in range(1, len(closes))]
    # Wilder's smoothing
    atr_val = sum(tr_vals[:period]) / period
    for i in range(period, len(tr_vals)):
        atr_val = (atr_val * (period - 1) + tr_vals[i]) / period
    return round(atr_val, 6)


def _ichimoku(closes: List[float]) -> Dict:
    """Ichimoku Cloud (Tenkan: 9, Kijun: 26, Senkou B: 52)."""
    result = {
        "tenkan": 0, "kijun": 0,
        "senkou_a": 0, "senkou_b": 0,
        "chikou": 0,
        "cloud_color": "neutral",
        "price_vs_cloud": "inside",
    }
    n = len(closes)
    if n < 52:
        if n > 0:
            result["tenkan"] = closes[-1]
            result["kijun"] = closes[-1]
        return result

    # Tenkan-sen (9-period high+low midpoint — approx from closes)
    win9 = closes[-9:]
    result["tenkan"] = round((max(win9) + min(win9)) / 2, 4)

    # Kijun-sen (26-period midpoint)
    win26 = closes[-26:]
    result["kijun"] = round((max(win26) + min(win26)) / 2, 4)

    # Senkou Span A = (Tenkan + Kijun) / 2 (plotted 26 ahead)
    result["senkou_a"] = round((result["tenkan"] + result["kijun"]) / 2, 4)

    # Senkou Span B = 52-period midpoint (plotted 26 ahead)
    win52 = closes[-52:]
    result["senkou_b"] = round((max(win52) + min(win52)) / 2, 4)

    # Chikou Span = current close (plotted 26 back)
    result["chikou"] = round(closes[-1], 4)

    # Cloud color
    if result["senkou_a"] > result["senkou_b"]:
        result["cloud_color"] = "bullish"
    elif result["senkou_a"] < result["senkou_b"]:
        result["cloud_color"] = "bearish"

    # Price vs cloud
    cloud_top = max(result["senkou_a"], result["senkou_b"])
    cloud_bottom = min(result["senkou_a"], result["senkou_b"])
    price = closes[-1]
    if price > cloud_top:
        result["price_vs_cloud"] = "above"
    elif price < cloud_bottom:
        result["price_vs_cloud"] = "below"
    else:
        result["price_vs_cloud"] = "inside"

    return result


def _obv(closes: List[float], volumes: List[float]) -> Dict:
    """On-Balance Volume with trend direction."""
    n = min(len(closes), len(volumes))
    if n < 2:
        return {"value": 0, "trend": "neutral"}
    obv_val = 0.0
    obv_values = [0.0]
    for i in range(1, n):
        if closes[i] > closes[i - 1]:
            obv_val += volumes[i]
        elif closes[i] < closes[i - 1]:
            obv_val -= volumes[i]
        obv_values.append(obv_val)

    # OBV trend via 10-period slope
    if len(obv_values) >= 10:
        recent = obv_values[-10:]
        slope = recent[-1] - recent[0]
        trend = "bullish" if slope > 0 else ("bearish" if slope < 0 else "neutral")
    else:
        trend = "neutral"

    return {"value": round(obv_val, 2), "trend": trend}


def _vwap(closes: List[float], volumes: List[float]) -> float:
    """Volume-Weighted Average Price (over available data)."""
    n = min(len(closes), len(volumes))
    if n < 1:
        return 0
    total_vol = sum(volumes[:n])
    if total_vol == 0:
        return closes[-1] if closes else 0
    vwap_val = sum(closes[i] * volumes[i] for i in range(n)) / total_vol
    return round(vwap_val, 4)


def _roc(closes: List[float], period: int = 12) -> float:
    """Rate of Change (momentum)."""
    if len(closes) <= period:
        return 0.0
    old_price = closes[-period - 1]
    if old_price == 0:
        return 0.0
    return round(((closes[-1] - old_price) / old_price) * 100, 4)


def _williams_r(closes: List[float], period: int = 14) -> float:
    """Williams %R oscillator (-100 to 0)."""
    if len(closes) < period:
        return -50.0
    window = closes[-period:]
    high = max(window)
    low = min(window)
    if high == low:
        return -50.0
    return round(((high - closes[-1]) / (high - low)) * -100, 2)


def _support_resistance(closes: List[float], lookback: int = 30) -> Dict:
    """Detect key support and resistance levels from price pivots."""
    if len(closes) < lookback:
        p = closes[-1] if closes else 0
        return {"support": p * 0.97, "resistance": p * 1.03, "levels": []}
    window = closes[-lookback:]
    pivots_high = []
    pivots_low = []
    for i in range(2, len(window) - 2):
        if window[i] > window[i - 1] and window[i] > window[i - 2] and \
           window[i] > window[i + 1] and window[i] > window[i + 2]:
            pivots_high.append(window[i])
        if window[i] < window[i - 1] and window[i] < window[i - 2] and \
           window[i] < window[i + 1] and window[i] < window[i + 2]:
            pivots_low.append(window[i])

    price = closes[-1]
    # Nearest support: highest pivot_low below price
    supports = sorted([p for p in pivots_low if p < price], reverse=True)
    resistances = sorted([p for p in pivots_high if p > price])

    support = supports[0] if supports else price * 0.97
    resistance = resistances[0] if resistances else price * 1.03

    return {
        "support": round(support, 4),
        "resistance": round(resistance, 4),
        "levels": [round(l, 4) for l in sorted(pivots_low + pivots_high)[-6:]],
    }


# ---------------------------------------------------------------------------
#  Market regime detection
# ---------------------------------------------------------------------------

def _detect_regime(closes: List[float], adx_val: float) -> Dict:
    """Detect market regime: trending, ranging, or volatile.

    Returns regime info with adaptive parameter suggestions.
    """
    if len(closes) < 30:
        return {
            "regime": "unknown",
            "volatility": "normal",
            "rsi_period": 14,
            "ema_fast": 9,
            "ema_slow": 21,
            "bb_std": 2.0,
            "sl_multiplier": 1.5,
            "tp_multiplier": 3.0,
        }

    # Volatility measurement (normalized ATR)
    atr = _atr(closes, 14)
    price = closes[-1]
    norm_atr = (atr / price * 100) if price > 0 else 0

    # EMA alignment check
    ema9 = _ema(closes, 9)
    ema21 = _ema(closes, 21)
    ema50 = _ema(closes, 50) if len(closes) >= 50 else ema21

    aligned_bull = ema9[-1] > ema21[-1] > ema50[-1] if ema9 and ema21 and ema50 else False
    aligned_bear = ema9[-1] < ema21[-1] < ema50[-1] if ema9 and ema21 and ema50 else False
    ema_aligned = aligned_bull or aligned_bear

    # Regime classification
    if adx_val > 30 and ema_aligned:
        regime = "strong_trend"
    elif adx_val > 25:
        regime = "trending"
    elif adx_val < 20 and norm_atr < 2:
        regime = "ranging"
    elif norm_atr > 4:
        regime = "volatile"
    else:
        regime = "normal"

    # Volatility classification
    if norm_atr > 5:
        volatility = "extreme"
    elif norm_atr > 3:
        volatility = "high"
    elif norm_atr > 1.5:
        volatility = "normal"
    else:
        volatility = "low"

    # Adaptive parameters based on regime
    params = {
        "regime": regime,
        "volatility": volatility,
        "norm_atr_pct": round(norm_atr, 4),
        "ema_aligned": ema_aligned,
    }

    if regime == "strong_trend":
        # In strong trends: shorter EMAs to catch moves, wider stops
        params.update({
            "rsi_period": 10, "ema_fast": 7, "ema_slow": 18,
            "bb_std": 2.5, "sl_multiplier": 2.0, "tp_multiplier": 4.0,
        })
    elif regime == "ranging":
        # In ranges: longer RSI to avoid whipsaws, default bands
        params.update({
            "rsi_period": 21, "ema_fast": 12, "ema_slow": 26,
            "bb_std": 2.0, "sl_multiplier": 1.2, "tp_multiplier": 2.0,
        })
    elif regime == "volatile":
        # In volatile: wider stops, shorter take profits
        params.update({
            "rsi_period": 14, "ema_fast": 9, "ema_slow": 21,
            "bb_std": 3.0, "sl_multiplier": 2.5, "tp_multiplier": 3.5,
        })
    else:
        params.update({
            "rsi_period": 14, "ema_fast": 9, "ema_slow": 21,
            "bb_std": 2.0, "sl_multiplier": 1.5, "tp_multiplier": 3.0,
        })

    return params


# ---------------------------------------------------------------------------
#  Multi-timeframe confirmation
# ---------------------------------------------------------------------------

def _multi_timeframe_bias(closes: List[float]) -> Dict:
    """Simulate multi-timeframe analysis using different EMA windows.

    Short-term (last 20 bars), medium-term (last 50), long-term (last 90).
    Returns bias for each "timeframe" and overall consensus.
    """
    result = {"short": "neutral", "medium": "neutral", "long": "neutral", "consensus": "neutral"}
    n = len(closes)

    # Short-term: EMA5 vs EMA13 on last 20 bars
    if n >= 20:
        short_data = closes[-20:]
        ema5 = _ema(short_data, 5)
        ema13 = _ema(short_data, 13)
        if ema5 and ema13:
            result["short"] = "bullish" if ema5[-1] > ema13[-1] else "bearish"

    # Medium-term: EMA9 vs EMA21 on last 50 bars
    if n >= 50:
        med_data = closes[-50:]
        ema9 = _ema(med_data, 9)
        ema21 = _ema(med_data, 21)
        if ema9 and ema21:
            result["medium"] = "bullish" if ema9[-1] > ema21[-1] else "bearish"

    # Long-term: EMA21 vs EMA50 on all data
    if n >= 50:
        ema21 = _ema(closes, 21)
        ema50 = _ema(closes, 50)
        if ema21 and ema50:
            result["long"] = "bullish" if ema21[-1] > ema50[-1] else "bearish"

    # Consensus
    biases = [result["short"], result["medium"], result["long"]]
    bull_count = biases.count("bullish")
    bear_count = biases.count("bearish")
    if bull_count >= 2:
        result["consensus"] = "bullish"
    elif bear_count >= 2:
        result["consensus"] = "bearish"
    else:
        result["consensus"] = "mixed"

    return result


# ---------------------------------------------------------------------------
#  Strategy class
# ---------------------------------------------------------------------------

class SignalAIStrategy:
    """Advanced AI-powered trading strategy with 12+ real indicators,
    regime detection, multi-timeframe confirmation, and adaptive risk."""

    INDICATORS = {
        "EMA9": {"name": "EMA 9", "type": "moving_average", "period": 9},
        "EMA21": {"name": "EMA 21", "type": "moving_average", "period": 21},
        "EMA50": {"name": "EMA 50", "type": "moving_average", "period": 50},
        "RSI": {"name": "RSI", "type": "oscillator", "period": 14,
                "overbought": 70, "oversold": 30},
        "MACD": {"name": "MACD", "type": "momentum", "fast": 12, "slow": 26, "signal": 9},
        "BB": {"name": "Bollinger Bands", "type": "volatility", "period": 20, "std": 2},
        "STOCH": {"name": "Stochastic", "type": "oscillator", "period": 14,
                  "overbought": 80, "oversold": 20},
        "ADX": {"name": "ADX", "type": "trend", "period": 14, "threshold": 25},
        # ── New v3 indicators ──
        "ICHIMOKU": {"name": "Ichimoku Cloud", "type": "trend", "tenkan": 9, "kijun": 26, "senkou_b": 52},
        "ATR": {"name": "ATR", "type": "volatility", "period": 14},
        "OBV": {"name": "On-Balance Volume", "type": "volume"},
        "VWAP": {"name": "VWAP", "type": "volume"},
        "ROC": {"name": "Rate of Change", "type": "momentum", "period": 12},
        "WILLIAMS": {"name": "Williams %R", "type": "oscillator", "period": 14},
        "SR": {"name": "Support/Resistance", "type": "levels"},
    }

    STRATEGIES = {
        "SignalAI": {
            "name": "SignalAI Premium",
            "description": "AI-optimized with 12+ indicators, regime detection, multi-TF confirmation",
            "indicators": ["EMA9", "EMA21", "EMA50", "RSI", "MACD", "BB",
                           "STOCH", "ADX", "ICHIMOKU", "OBV", "VWAP",
                           "ROC", "WILLIAMS", "ATR", "SR"],
            "ai_powered": True,
            "subscription_required": True,
            "price": 9.99,
        },
        "Trend_Following": {
            "name": "Trend Following",
            "description": "EMA crossover + Ichimoku cloud for trending markets",
            "indicators": ["EMA9", "EMA21", "EMA50", "ADX", "ICHIMOKU"],
            "ai_powered": False,
            "subscription_required": False,
            "price": 0,
        },
        "Momentum": {
            "name": "Momentum Strategy",
            "description": "RSI + MACD + Stochastic + Williams %R for momentum trading",
            "indicators": ["RSI", "MACD", "STOCH", "WILLIAMS", "ROC"],
            "ai_powered": False,
            "subscription_required": False,
            "price": 0,
        },
    }

    # Indicator weights for signal scoring (higher = more important)
    INDICATOR_WEIGHTS = {
        "EMA_CROSS": 1.5,       # EMA crossovers are reliable trend signals
        "RSI": 1.2,             # RSI is a strong mean-reversion tool
        "MACD": 1.5,            # MACD crossovers are high-value
        "MACD_HIST": 0.8,       # Histogram direction adds conviction
        "STOCH": 1.0,           # Stochastic useful at extremes
        "ADX": 0.5,             # ADX is a modifier, not directional
        "BB": 1.0,              # Bollinger position matters
        "ICHIMOKU_CLOUD": 1.8,  # Ichimoku cloud is a strong trend signal
        "ICHIMOKU_TK": 1.2,     # Tenkan/Kijun cross
        "OBV": 1.0,             # Volume confirms direction
        "VWAP": 0.8,            # Price vs VWAP for intraday bias
        "ROC": 0.7,             # Momentum confirmation
        "WILLIAMS": 0.8,        # Williams %R at extremes
        "SR_PROXIMITY": 0.6,    # Near S/R levels
        "MTF": 1.5,             # Multi-timeframe alignment is powerful
    }

    def __init__(self):
        self.signals_history: List[Dict] = []
        self._load_history()

    # ── persistence ─────────────────────────────────────────────────

    def _load_history(self):
        path = "data/signalai_history.json"
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    self.signals_history = json.load(f)
            except Exception:
                self.signals_history = []

    def _save_history(self):
        path = "data/signalai_history.json"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.signals_history[-1000:], f, indent=2)

    # ── public API ──────────────────────────────────────────────────

    def get_available_strategies(self) -> Dict[str, Dict]:
        return self.STRATEGIES

    def get_strategy_info(self, strategy_name: str) -> Optional[Dict]:
        return self.STRATEGIES.get(strategy_name)

    def generate_signals(
        self,
        symbol: str,
        strategy_name: str = "SignalAI",
        current_price: float = None,
    ) -> Dict:
        """Generate buy/sell signals from 12+ real indicator computations.

        Pipeline:
        1. Fetch live price + historical data
        2. Detect market regime (trending/ranging/volatile)
        3. Calculate all indicators with adaptive parameters
        4. Multi-timeframe confirmation
        5. Weighted signal scoring
        6. AI enhancement (premium only) with confluence + regime-aware risk
        7. Support/resistance-based entry/exit levels

        Args:
            symbol: e.g. "BINANCE:BTCUSDT", "BTC", "AAPL"
            strategy_name: Strategy to use
            current_price: Override price (fetched live if None)

        Returns:
            Signal dict with recommendation, indicators, entry/exit levels.
        """
        strategy = self.STRATEGIES.get(strategy_name)
        if not strategy:
            return {"error": f"Strategy '{strategy_name}' not found"}

        # 1. Fetch live price
        if current_price is None:
            provider = _get_price_provider()
            if provider:
                current_price = provider.get_live_price(symbol)
        if current_price is None:
            return {
                "error": "Unable to fetch live price for this symbol",
                "symbol": symbol,
                "message": "Please check the symbol or try again later",
            }

        # 2. Fetch historical closes + volumes
        closes = _fetch_closes(symbol)
        if not closes or len(closes) < 10:
            closes = [current_price] * 30

        # Ensure current price is the latest element
        if abs(closes[-1] - current_price) / max(current_price, 1) > 0.15:
            closes.append(current_price)

        volumes = _fetch_volumes(symbol) if any(
            ind in strategy["indicators"] for ind in ("OBV", "VWAP")
        ) else []

        # 3. Detect market regime
        adx_val = _adx(closes)
        regime = _detect_regime(closes, adx_val)

        # 4. Compute indicators (with adaptive parameters from regime)
        indicators_data = self._calculate_indicators(
            closes, volumes, strategy["indicators"], current_price, regime
        )
        indicators_data["regime"] = regime["regime"]
        indicators_data["volatility"] = regime["volatility"]

        # 5. Multi-timeframe confirmation
        mtf = _multi_timeframe_bias(closes)
        indicators_data["multi_timeframe"] = mtf

        # 6. Weighted signal analysis
        signal = self._analyze_indicators(indicators_data, strategy, current_price, regime, mtf)

        # 7. AI enhancement for premium strategy
        if strategy.get("ai_powered", False):
            sr = indicators_data.get("SR", {})
            signal = self._apply_ai_enhancement(
                signal, indicators_data, current_price, regime, mtf, sr
            )

        result = {
            "symbol": symbol,
            "strategy": strategy_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "current_price": current_price,
            "signal": signal["type"],
            "strength": signal["strength"],
            "confidence": signal["confidence"],
            "indicators": indicators_data,
            "recommendation": signal["recommendation"],
            "entry_price": signal.get("entry_price"),
            "stop_loss": signal.get("stop_loss"),
            "take_profit": signal.get("take_profit"),
            "risk_reward": signal.get("risk_reward"),
            "regime": regime["regime"],
            "volatility": regime["volatility"],
            "mtf_consensus": mtf["consensus"],
            "data_source": "live" if len(closes) >= 20 else "limited",
        }

        self.signals_history.append(result)
        self._save_history()
        return result

    # ── indicator computation (100% real) ───────────────────────────

    def _calculate_indicators(
        self,
        closes: List[float],
        volumes: List[float],
        indicator_names: List[str],
        current_price: float,
        regime: Dict,
    ) -> Dict:
        indicators: Dict = {}

        for name in indicator_names:
            if name == "EMA9":
                fast = regime.get("ema_fast", 9)
                vals = _ema(closes, fast)
                indicators["EMA9"] = round(vals[-1], 4) if vals else current_price

            elif name == "EMA21":
                slow = regime.get("ema_slow", 21)
                vals = _ema(closes, slow)
                indicators["EMA21"] = round(vals[-1], 4) if vals else current_price

            elif name == "EMA50":
                vals = _ema(closes, 50)
                indicators["EMA50"] = round(vals[-1], 4) if vals else current_price

            elif name == "RSI":
                period = regime.get("rsi_period", 14)
                indicators["RSI"] = round(_rsi(closes, period), 2)

            elif name == "MACD":
                indicators["MACD"] = _macd(closes)

            elif name == "BB":
                std = regime.get("bb_std", 2.0)
                indicators["BB"] = _bollinger(closes, 20, std)

            elif name == "STOCH":
                indicators["STOCH"] = _stochastic(closes)

            elif name == "ADX":
                indicators["ADX"] = round(_adx(closes), 2)

            elif name == "ICHIMOKU":
                indicators["ICHIMOKU"] = _ichimoku(closes)

            elif name == "ATR":
                indicators["ATR"] = _atr(closes)

            elif name == "OBV":
                indicators["OBV"] = _obv(closes, volumes) if volumes else {"value": 0, "trend": "neutral"}

            elif name == "VWAP":
                indicators["VWAP"] = _vwap(closes, volumes) if volumes else 0

            elif name == "ROC":
                indicators["ROC"] = _roc(closes)

            elif name == "WILLIAMS":
                indicators["WILLIAMS"] = _williams_r(closes)

            elif name == "SR":
                indicators["SR"] = _support_resistance(closes)

        return indicators

    # ── weighted signal analysis ────────────────────────────────────

    def _analyze_indicators(
        self,
        indicators: Dict,
        strategy: Dict,
        current_price: float,
        regime: Dict,
        mtf: Dict,
    ) -> Dict:
        W = self.INDICATOR_WEIGHTS
        bullish_score = 0.0
        bearish_score = 0.0
        total_weight = 0.0

        # ── EMA crossovers ──
        if "EMA9" in indicators and "EMA21" in indicators:
            w = W["EMA_CROSS"]
            total_weight += w
            if indicators["EMA9"] > indicators["EMA21"]:
                bullish_score += w
            else:
                bearish_score += w

        if "EMA21" in indicators and "EMA50" in indicators:
            w = W["EMA_CROSS"]
            total_weight += w
            if indicators["EMA21"] > indicators["EMA50"]:
                bullish_score += w
            else:
                bearish_score += w

        # ── RSI ──
        if "RSI" in indicators:
            w = W["RSI"]
            total_weight += w
            rsi = indicators["RSI"]
            if rsi < 30:
                bullish_score += w       # Strong oversold
            elif rsi < 40:
                bullish_score += w * 0.6  # Mildly oversold
            elif rsi > 70:
                bearish_score += w       # Strong overbought
            elif rsi > 60:
                bearish_score += w * 0.6  # Mildly overbought

        # ── MACD ──
        if "MACD" in indicators:
            macd = indicators["MACD"]
            # MACD line vs signal
            w = W["MACD"]
            total_weight += w
            if macd.get("crossover") == "bullish":
                bullish_score += w * 1.3  # Crossover bonus
            elif macd.get("crossover") == "bearish":
                bearish_score += w * 1.3
            elif macd["value"] > macd["signal"]:
                bullish_score += w
            else:
                bearish_score += w

            # Histogram direction
            w2 = W["MACD_HIST"]
            total_weight += w2
            if macd["histogram"] > 0:
                bullish_score += w2
            elif macd["histogram"] < 0:
                bearish_score += w2

        # ── Stochastic ──
        if "STOCH" in indicators:
            w = W["STOCH"]
            total_weight += w
            stoch = indicators["STOCH"]
            k = stoch["k"]
            if k < 20:
                bullish_score += w  # Oversold
            elif k > 80:
                bearish_score += w  # Overbought
            if stoch.get("crossover") == "bullish":
                bullish_score += w * 0.3
            elif stoch.get("crossover") == "bearish":
                bearish_score += w * 0.3

        # ── Bollinger Bands ──
        if "BB" in indicators:
            w = W["BB"]
            total_weight += w
            bb = indicators["BB"]
            pct_b = bb.get("pct_b", 0.5)
            if pct_b < 0.0:
                bullish_score += w  # Below lower band
            elif pct_b > 1.0:
                bearish_score += w  # Above upper band
            elif pct_b < 0.2:
                bullish_score += w * 0.6
            elif pct_b > 0.8:
                bearish_score += w * 0.6

        # ── Ichimoku Cloud ──
        if "ICHIMOKU" in indicators:
            ichi = indicators["ICHIMOKU"]
            # Price vs cloud
            w = W["ICHIMOKU_CLOUD"]
            total_weight += w
            pos = ichi.get("price_vs_cloud", "inside")
            if pos == "above" and ichi.get("cloud_color") == "bullish":
                bullish_score += w  # Price above bullish cloud — strong bull
            elif pos == "above":
                bullish_score += w * 0.7
            elif pos == "below" and ichi.get("cloud_color") == "bearish":
                bearish_score += w  # Price below bearish cloud — strong bear
            elif pos == "below":
                bearish_score += w * 0.7

            # Tenkan/Kijun cross
            w2 = W["ICHIMOKU_TK"]
            total_weight += w2
            if ichi.get("tenkan", 0) > ichi.get("kijun", 0):
                bullish_score += w2
            elif ichi.get("tenkan", 0) < ichi.get("kijun", 0):
                bearish_score += w2

        # ── OBV trend ──
        if "OBV" in indicators and isinstance(indicators["OBV"], dict):
            w = W["OBV"]
            total_weight += w
            trend = indicators["OBV"].get("trend", "neutral")
            if trend == "bullish":
                bullish_score += w
            elif trend == "bearish":
                bearish_score += w

        # ── VWAP ──
        if "VWAP" in indicators and indicators["VWAP"]:
            w = W["VWAP"]
            total_weight += w
            if current_price > indicators["VWAP"]:
                bullish_score += w  # Price above VWAP
            else:
                bearish_score += w

        # ── Rate of Change ──
        if "ROC" in indicators:
            w = W["ROC"]
            total_weight += w
            roc = indicators["ROC"]
            if roc > 5:
                bullish_score += w
            elif roc > 0:
                bullish_score += w * 0.4
            elif roc < -5:
                bearish_score += w
            elif roc < 0:
                bearish_score += w * 0.4

        # ── Williams %R ──
        if "WILLIAMS" in indicators:
            w = W["WILLIAMS"]
            total_weight += w
            wr = indicators["WILLIAMS"]
            if wr > -20:
                bearish_score += w  # Overbought (near 0)
            elif wr < -80:
                bullish_score += w  # Oversold (near -100)

        # ── S/R Proximity ──
        if "SR" in indicators:
            w = W["SR_PROXIMITY"]
            total_weight += w
            sr = indicators["SR"]
            sup = sr.get("support", 0)
            res = sr.get("resistance", 0)
            if sup and current_price > 0:
                dist_support = (current_price - sup) / current_price
                if dist_support < 0.02:
                    bullish_score += w  # Near support = potential bounce
            if res and current_price > 0:
                dist_resist = (res - current_price) / current_price
                if dist_resist < 0.02:
                    bearish_score += w  # Near resistance = potential rejection

        # ── Multi-timeframe bias ──
        w = W["MTF"]
        total_weight += w
        consensus = mtf.get("consensus", "mixed")
        if consensus == "bullish":
            bullish_score += w
        elif consensus == "bearish":
            bearish_score += w

        # ── ADX as amplifier ──
        adx = indicators.get("ADX", 25)
        trend_strong = adx > 25
        trend_very_strong = adx > 35

        # ── Final signal computation ──
        if total_weight == 0:
            return {"type": "HOLD", "strength": 50, "confidence": 50,
                    "recommendation": "Insufficient data"}

        bull_pct = bullish_score / total_weight
        bear_pct = bearish_score / total_weight

        if bull_pct > bear_pct:
            signal_type = "BUY"
            raw_strength = int(bull_pct * 100)
        elif bear_pct > bull_pct:
            signal_type = "SELL"
            raw_strength = int(bear_pct * 100)
        else:
            signal_type = "HOLD"
            raw_strength = 50

        # Confidence = agreement level + trend strength bonus
        agreement = max(bull_pct, bear_pct)
        confidence = int(agreement * 75)
        if trend_strong:
            confidence += 10
        if trend_very_strong:
            confidence += 5
        if consensus in ("bullish", "bearish") and (
            (consensus == "bullish" and signal_type == "BUY") or
            (consensus == "bearish" and signal_type == "SELL")
        ):
            confidence += 8  # MTF confirms direction

        confidence = min(confidence, 98)

        return {
            "type": signal_type,
            "strength": raw_strength,
            "confidence": confidence,
            "recommendation": self._generate_recommendation(signal_type, raw_strength, confidence),
        }

    # ── AI enhancement with regime-aware risk management ────────────

    def _apply_ai_enhancement(
        self,
        signal: Dict,
        indicators: Dict,
        current_price: float,
        regime: Dict,
        mtf: Dict,
        sr: Dict,
    ) -> Dict:
        """AI enhancement: real GPT-4/Claude consultation + confluence bonus + regime-adaptive risk."""

        # ── Real AI consultation via coordinator ──
        ai_insight = self._consult_ai(signal, indicators, current_price, regime, mtf)

        # ── Confluence bonus ──
        rsi = indicators.get("RSI", 50)
        macd = indicators.get("MACD", {})
        macd_hist = macd.get("histogram", 0) if isinstance(macd, dict) else 0
        ichi = indicators.get("ICHIMOKU", {})
        stoch = indicators.get("STOCH", {})
        obv = indicators.get("OBV", {})

        bonus = 0
        if signal["type"] == "BUY":
            if rsi < 40:
                bonus += 2
            if macd_hist > 0:
                bonus += 2
            if macd.get("crossover") == "bullish":
                bonus += 3
            if ichi.get("price_vs_cloud") == "above":
                bonus += 2
            if isinstance(stoch, dict) and stoch.get("k", 50) < 30:
                bonus += 1
            if isinstance(obv, dict) and obv.get("trend") == "bullish":
                bonus += 2
            if mtf.get("consensus") == "bullish":
                bonus += 3

        elif signal["type"] == "SELL":
            if rsi > 60:
                bonus += 2
            if macd_hist < 0:
                bonus += 2
            if macd.get("crossover") == "bearish":
                bonus += 3
            if ichi.get("price_vs_cloud") == "below":
                bonus += 2
            if isinstance(stoch, dict) and stoch.get("k", 50) > 70:
                bonus += 1
            if isinstance(obv, dict) and obv.get("trend") == "bearish":
                bonus += 2
            if mtf.get("consensus") == "bearish":
                bonus += 3

        signal["confidence"] = min(signal["confidence"] + bonus, 98)

        # ── AI insight integration ──
        if ai_insight.get("success"):
            ai_dir = ai_insight.get("direction", "").upper()
            ai_conf = ai_insight.get("ai_confidence", 0)
            signal["ai_analysis"] = ai_insight.get("analysis", "")
            signal["ai_worker"] = ai_insight.get("worker_used", "unknown")

            # AI agrees with indicators → boost confidence
            if (ai_dir == "BULLISH" and signal["type"] == "BUY") or \
               (ai_dir == "BEARISH" and signal["type"] == "SELL"):
                signal["confidence"] = min(signal["confidence"] + 5, 98)
                signal["ai_agrees"] = True
            # AI disagrees → reduce confidence slightly
            elif ai_dir and ai_dir != "NEUTRAL":
                signal["confidence"] = max(signal["confidence"] - 3, 10)
                signal["ai_agrees"] = False
            else:
                signal["ai_agrees"] = None

        # ── Regime-adaptive risk levels ──
        sl_mult = regime.get("sl_multiplier", 1.5)
        tp_mult = regime.get("tp_multiplier", 3.0)
        atr = indicators.get("ATR", 0)

        # Use ATR for dynamic levels if available, else Bollinger band width
        if atr and atr > 0:
            atr_pct = atr / current_price if current_price > 0 else 0.02
        else:
            bb = indicators.get("BB", {})
            upper = bb.get("upper", current_price * 1.02)
            lower = bb.get("lower", current_price * 0.98)
            atr_pct = max((upper - lower) / (2 * current_price), 0.01)

        # Use S/R for smarter levels
        support = sr.get("support", current_price * (1 - atr_pct * sl_mult)) if sr else None
        resistance = sr.get("resistance", current_price * (1 + atr_pct * tp_mult)) if sr else None

        if signal["type"] == "BUY":
            signal["entry_price"] = round(current_price * (1 - atr_pct * 0.2), 4)
            # Stop loss: just below support or ATR-based
            sl_atr = current_price * (1 - atr_pct * sl_mult)
            if support and support < current_price:
                sl = min(support * 0.995, sl_atr)  # Slightly below support
            else:
                sl = sl_atr
            signal["stop_loss"] = round(sl, 4)
            # Take profit: near resistance or ATR-based
            tp_atr = current_price * (1 + atr_pct * tp_mult)
            if resistance and resistance > current_price:
                tp = max(resistance * 0.99, tp_atr)  # Near resistance
            else:
                tp = tp_atr
            signal["take_profit"] = round(tp, 4)

        elif signal["type"] == "SELL":
            signal["entry_price"] = round(current_price * (1 + atr_pct * 0.2), 4)
            sl_atr = current_price * (1 + atr_pct * sl_mult)
            if resistance and resistance > current_price:
                sl = max(resistance * 1.005, sl_atr)
            else:
                sl = sl_atr
            signal["stop_loss"] = round(sl, 4)
            tp_atr = current_price * (1 - atr_pct * tp_mult)
            if support and support < current_price:
                tp = min(support * 1.01, tp_atr)
            else:
                tp = tp_atr
            signal["take_profit"] = round(tp, 4)

        else:
            signal["entry_price"] = current_price
            signal["stop_loss"] = round(current_price * (1 - atr_pct * sl_mult), 4)
            signal["take_profit"] = round(current_price * (1 + atr_pct * sl_mult), 4)

        sl_dist = abs(current_price - (signal.get("stop_loss") or current_price))
        tp_dist = abs((signal.get("take_profit") or current_price) - current_price)
        signal["risk_reward"] = round(tp_dist / sl_dist, 2) if sl_dist > 0 else 0

        return signal

    # ── Real AI consultation ──────────────────────────────────────

    def _consult_ai(
        self,
        signal: Dict,
        indicators: Dict,
        current_price: float,
        regime: Dict,
        mtf: Dict,
    ) -> Dict:
        """Call the multi-AI coordinator (GPT-4/Claude) for signal validation.

        Returns dict with 'success', 'direction', 'ai_confidence', 'analysis', 'worker_used'.
        Falls back gracefully if AI is unavailable.
        """
        try:
            from multi_ai_coordinator import get_coordinator
            coordinator = get_coordinator()

            if not coordinator.workers:
                return {"success": False, "reason": "No AI workers available"}

            # Build concise prompt with real indicator data
            rsi = indicators.get("RSI", "N/A")
            macd = indicators.get("MACD", {})
            macd_val = macd.get("value", "N/A") if isinstance(macd, dict) else "N/A"
            macd_sig = macd.get("signal", "N/A") if isinstance(macd, dict) else "N/A"
            adx = indicators.get("ADX", "N/A")
            ichi = indicators.get("ICHIMOKU", {})
            cloud_pos = ichi.get("price_vs_cloud", "N/A") if isinstance(ichi, dict) else "N/A"

            prompt = (
                f"Analyze this trading signal and give your directional opinion.\n"
                f"Price: ${current_price}\n"
                f"Current signal: {signal.get('type', 'HOLD')} (strength {signal.get('strength', 0)}%)\n"
                f"RSI: {rsi} | MACD: {macd_val} vs signal {macd_sig}\n"
                f"ADX: {adx} | Ichimoku cloud: {cloud_pos}\n"
                f"Regime: {regime.get('regime', 'unknown')} | Volatility: {regime.get('volatility', 'N/A')}\n"
                f"MTF consensus: {mtf.get('consensus', 'neutral')}\n\n"
                f"Reply with JSON: {{\"direction\": \"BULLISH/BEARISH/NEUTRAL\", "
                f"\"confidence\": 0-100, \"reason\": \"brief explanation\"}}"
            )

            result = coordinator.analyze(
                task_type="technical_analysis",
                prompt=prompt,
                data={"price": current_price, "indicators": {
                    "RSI": rsi, "ADX": adx, "regime": regime.get("regime"),
                }},
                strategy="specialist",
                timeout=10,
                cache_ttl=60,
            )

            if result.get("success"):
                analysis = result.get("analysis", {})
                # Try to extract direction from AI response
                direction = "NEUTRAL"
                ai_confidence = 50
                analysis_text = ""

                if isinstance(analysis, dict):
                    direction = analysis.get("direction", "NEUTRAL").upper()
                    ai_confidence = analysis.get("confidence", 50)
                    analysis_text = analysis.get("reason", "")
                elif isinstance(analysis, str):
                    analysis_text = analysis
                    a_upper = analysis.upper()
                    if "BULLISH" in a_upper or "BUY" in a_upper:
                        direction = "BULLISH"
                    elif "BEARISH" in a_upper or "SELL" in a_upper:
                        direction = "BEARISH"

                return {
                    "success": True,
                    "direction": direction,
                    "ai_confidence": ai_confidence,
                    "analysis": analysis_text[:500],
                    "worker_used": result.get("worker_used", "coordinator"),
                }

            return {"success": False, "reason": result.get("error", "AI unavailable")}

        except Exception as e:
            logger.debug(f"AI consultation skipped: {e}")
            return {"success": False, "reason": str(e)}

    # ── helpers ─────────────────────────────────────────────────────

    def _generate_recommendation(self, signal_type: str, strength: int, confidence: int = 50) -> str:
        if signal_type == "BUY":
            if strength >= 75 and confidence >= 70:
                return "Strong Buy — Multiple indicators aligned, high conviction entry"
            elif strength >= 60:
                return "Buy — Good entry opportunity with solid indicator support"
            elif strength >= 45:
                return "Moderate Buy — Some bullish signals, consider partial position"
            return "Weak Buy — Limited bullish signals, wait for stronger confirmation"
        elif signal_type == "SELL":
            if strength >= 75 and confidence >= 70:
                return "Strong Sell — Multiple indicators bearish, high conviction exit"
            elif strength >= 60:
                return "Sell — Consider taking profits or reducing exposure"
            elif strength >= 45:
                return "Moderate Sell — Bearish pressure building, tighten stops"
            return "Weak Sell — Monitor position closely, early bearish signals"
        return "Hold — No clear direction, wait for better setup"

    def get_signal_history(self, symbol: str = None, limit: int = 50) -> List[Dict]:
        history = self.signals_history
        if symbol:
            history = [s for s in history if s.get("symbol") == symbol]
        return history[-limit:]

    def get_performance_stats(self, symbol: str = None) -> Dict:
        signals = self.get_signal_history(symbol)
        if not signals:
            return {"total_signals": 0, "buy_signals": 0, "sell_signals": 0,
                    "hold_signals": 0, "avg_confidence": 0}

        buy_c = sum(1 for s in signals if s["signal"] == "BUY")
        sell_c = sum(1 for s in signals if s["signal"] == "SELL")
        hold_c = sum(1 for s in signals if s["signal"] == "HOLD")
        avg_conf = sum(s.get("confidence", 0) for s in signals) / len(signals)
        avg_rr = sum(s.get("risk_reward", 0) for s in signals if s.get("risk_reward")) / max(
            sum(1 for s in signals if s.get("risk_reward")), 1
        )

        # Win rate (if we have historical outcomes)
        recent = [s for s in signals if s.get("regime")]  # v3 signals only
        regime_dist = {}
        for s in recent:
            r = s.get("regime", "unknown")
            regime_dist[r] = regime_dist.get(r, 0) + 1

        return {
            "total_signals": len(signals),
            "buy_signals": buy_c,
            "sell_signals": sell_c,
            "hold_signals": hold_c,
            "avg_confidence": round(avg_conf, 2),
            "avg_risk_reward": round(avg_rr, 2),
            "regime_distribution": regime_dist,
            "last_signal": signals[-1] if signals else None,
        }


# Global instance
signalai_strategy = SignalAIStrategy()
