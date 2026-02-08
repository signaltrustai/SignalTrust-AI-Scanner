#!/usr/bin/env python3
"""
AI Predictor Module — SignalTrust AI Scanner
═══════════════════════════════════════════════
Price prediction, signal generation, and risk assessment using
REAL market data from live APIs.

Data sources:
  • live_price_provider (Binance, CoinGecko, Yahoo Finance)
  • Yahoo Finance chart API for historical candles
  • signalai_strategy indicator engine for RSI/MACD/Bollinger
  • EnhancedAIEngine (OpenAI/Anthropic) when available
"""

import math
import time
import logging
import requests
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

try:
    from ai_provider import EnhancedAIEngine, AIProviderFactory
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

logger = logging.getLogger(__name__)

# ── tiny cache ─────────────────────────────────────────────────────
_price_cache: Dict[str, dict] = {}
_CACHE_TTL = 90  # seconds


def _get_cached(key: str):
    e = _price_cache.get(key)
    if e and time.time() - e["ts"] < _CACHE_TTL:
        return e["val"]
    return None


def _set_cache(key: str, val):
    _price_cache[key] = {"val": val, "ts": time.time()}


# ── fetch helpers ──────────────────────────────────────────────────

def _fetch_live_price(symbol: str) -> Optional[float]:
    """Fetch a single live price via multiple fallbacks."""
    try:
        from live_price_provider import live_price_provider
        return live_price_provider.get_live_price(symbol)
    except Exception:
        pass

    # Direct Binance fallback for crypto
    base = symbol.upper().replace("USDT", "").replace("BUSD", "")
    try:
        r = requests.get(
            "https://api.binance.com/api/v3/ticker/price",
            params={"symbol": f"{base}USDT"}, timeout=6)
        if r.status_code == 200:
            return float(r.json()["price"])
    except Exception:
        pass

    # Yahoo Finance fallback for stocks
    for t in [base, f"{base}-USD"]:
        try:
            r = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{t}",
                params={"range": "1d", "interval": "1d"},
                headers={"User-Agent": "Mozilla/5.0"}, timeout=6)
            if r.status_code == 200:
                meta = r.json()["chart"]["result"][0]["meta"]
                return float(meta.get("regularMarketPrice", meta.get("previousClose", 0)))
        except Exception:
            pass
    return None


def _fetch_closes(symbol: str, days: int = 90) -> List[float]:
    """Fetch daily closing prices (most-recent last)."""
    ck = f"closes_{symbol}_{days}"
    cached = _get_cached(ck)
    if cached:
        return cached

    base = symbol.upper().replace("USDT", "").replace("BUSD", "")
    closes: List[float] = []

    # Yahoo Finance chart
    for t in [base, f"{base}-USD"]:
        try:
            r = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{t}",
                params={"range": "3mo", "interval": "1d"},
                headers={"User-Agent": "Mozilla/5.0"}, timeout=8)
            if r.status_code == 200:
                q = r.json()["chart"]["result"][0]["indicators"]["quote"][0]
                closes = [c for c in q.get("close", []) if c is not None]
                if len(closes) >= 20:
                    break
        except Exception:
            pass

    # Binance klines fallback
    if not closes:
        try:
            r = requests.get(
                "https://api.binance.com/api/v3/klines",
                params={"symbol": f"{base}USDT", "interval": "1d", "limit": days},
                timeout=8)
            if r.status_code == 200:
                closes = [float(k[4]) for k in r.json()]
        except Exception:
            pass

    if closes:
        _set_cache(ck, closes)
    return closes


def _compute_volatility(closes: List[float]) -> float:
    """Annualized volatility from daily returns (%)."""
    if len(closes) < 5:
        return 25.0  # default
    returns = [(closes[i] / closes[i - 1] - 1) for i in range(1, len(closes)) if closes[i - 1]]
    if not returns:
        return 25.0
    mean_r = sum(returns) / len(returns)
    var = sum((r - mean_r) ** 2 for r in returns) / len(returns)
    daily_vol = math.sqrt(var)
    return round(daily_vol * math.sqrt(365) * 100, 2)


def _compute_beta(closes: List[float], bench_closes: List[float]) -> float:
    """Approximate beta vs benchmark."""
    n = min(len(closes), len(bench_closes))
    if n < 10:
        return 1.0
    r_asset = [(closes[-(n - i)] / closes[-(n - i) - 1] - 1) for i in range(1, n)]
    r_bench = [(bench_closes[-(n - i)] / bench_closes[-(n - i) - 1] - 1) for i in range(1, n)]
    mean_a = sum(r_asset) / len(r_asset)
    mean_b = sum(r_bench) / len(r_bench)
    cov = sum((r_asset[i] - mean_a) * (r_bench[i] - mean_b) for i in range(len(r_asset))) / len(r_asset)
    var_b = sum((r_bench[i] - mean_b) ** 2 for i in range(len(r_bench))) / len(r_bench)
    return round(cov / var_b, 2) if var_b > 0 else 1.0


# ── main class ─────────────────────────────────────────────────────

class AIPredictor:
    """AI-powered market predictor with REAL data."""

    def __init__(self, use_real_ai: bool = True):
        self.model_version = "4.0.0"
        self.use_real_ai = use_real_ai and AI_AVAILABLE
        self.ai_engine = None
        if self.use_real_ai:
            try:
                self.ai_engine = EnhancedAIEngine()
                print("✅ AI Predictor initialized with enhanced AI engine")
            except Exception:
                self.use_real_ai = False

    # ── predict_price ──────────────────────────────────────────────

    def predict_price(self, symbol: str, days_ahead: int = 7) -> Dict:
        """Predict future price using historical trend + volatility.

        Uses real closing prices to extrapolate a trend-based forecast.
        """
        current_price = _fetch_live_price(symbol)
        closes = _fetch_closes(symbol)

        if current_price is None and closes:
            current_price = closes[-1]
        if current_price is None:
            current_price = 0

        # Try AI engine first
        if self.use_real_ai and self.ai_engine and current_price > 0:
            try:
                ai_pred = self.ai_engine.generate_prediction(
                    symbol=symbol,
                    data={"current_price": current_price, "days_ahead": days_ahead, "symbol": symbol},
                )
                if ai_pred.get("success"):
                    return {
                        "symbol": symbol,
                        "current_price": round(current_price, 2),
                        "ai_prediction": ai_pred.get("prediction", ""),
                        "model_used": "Enhanced AI Engine",
                        "model_version": self.model_version,
                        "ai_powered": True,
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
            except Exception:
                pass

        # Trend + volatility forecast from real closes
        if len(closes) >= 10:
            # Compute daily trend from recent 20 days
            window = closes[-20:]
            daily_returns = [(window[i] / window[i - 1] - 1) for i in range(1, len(window)) if window[i - 1]]
            avg_return = sum(daily_returns) / len(daily_returns) if daily_returns else 0
            vol = _compute_volatility(closes) / 100 / math.sqrt(365)  # daily vol

            predictions = []
            price = current_price
            for day in range(1, days_ahead + 1):
                # Simple drift + decay
                drift = avg_return * (1 - day * 0.02)  # trend decays over time
                price = price * (1 + drift)
                band = price * vol * math.sqrt(day) * 1.96  # 95% CI
                conf = max(50, 92 - day * 3)
                predictions.append({
                    "day": day,
                    "date": (datetime.now(timezone.utc) + timedelta(days=day)).strftime("%Y-%m-%d"),
                    "predicted_price": round(price, 2),
                    "low_estimate": round(price - band, 2),
                    "high_estimate": round(price + band, 2),
                    "confidence": round(conf, 1),
                })

            first, last = predictions[0]["predicted_price"], predictions[-1]["predicted_price"]
            change = ((last - first) / first * 100) if first else 0

            return {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "predictions": predictions,
                "overall_trend": "Bullish" if change > 1 else ("Bearish" if change < -1 else "Neutral"),
                "expected_change_percent": round(change, 2),
                "model_used": "Trend + Volatility Forecast (live data)",
                "model_version": self.model_version,
                "ai_powered": False,
                "data_source": "live",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }

        # Minimal data — return honest message
        return {
            "symbol": symbol,
            "current_price": round(current_price, 2) if current_price else None,
            "predictions": [],
            "overall_trend": "Unknown",
            "expected_change_percent": 0,
            "model_used": "Insufficient historical data",
            "model_version": self.model_version,
            "ai_powered": False,
            "data_source": "limited",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ── generate_signals ──────────────────────────────────────────

    def generate_signals(self, symbol: str) -> Dict:
        """Generate trading signals from real technical indicators."""
        current_price = _fetch_live_price(symbol)
        closes = _fetch_closes(symbol)

        if not current_price and closes:
            current_price = closes[-1]
        if not current_price:
            return {"symbol": symbol, "error": "Cannot fetch price",
                    "timestamp": datetime.now(timezone.utc).isoformat()}

        # Compute real indicators
        from signalai_strategy import _rsi, _macd, _bollinger, _ema

        rsi = _rsi(closes) if len(closes) > 14 else 50
        macd = _macd(closes) if len(closes) > 26 else {"value": 0, "signal": 0, "histogram": 0}
        bb = _bollinger(closes) if len(closes) > 20 else {"upper": current_price * 1.02, "middle": current_price, "lower": current_price * 0.98}

        ema9 = _ema(closes, 9)[-1] if len(closes) >= 9 else current_price
        ema21 = _ema(closes, 21)[-1] if len(closes) >= 21 else current_price

        # Score each indicator
        bullish, bearish, total = 0, 0, 0

        total += 1
        if ema9 > ema21:
            bullish += 1
        else:
            bearish += 1

        total += 1
        if rsi < 35:
            bullish += 1
        elif rsi > 65:
            bearish += 1

        total += 1
        if macd["histogram"] > 0:
            bullish += 1
        else:
            bearish += 1

        total += 1
        if current_price < bb["lower"]:
            bullish += 1
        elif current_price > bb["upper"]:
            bearish += 1

        if bullish > bearish:
            sig_type, strength_label = "BUY", "STRONG" if bullish >= 3 else "MODERATE"
        elif bearish > bullish:
            sig_type, strength_label = "SELL", "STRONG" if bearish >= 3 else "MODERATE"
        else:
            sig_type, strength_label = "HOLD", "MODERATE"

        agreement = max(bullish, bearish) / total * 100
        confidence = round(min(95, agreement + 10), 1)

        # Entry / SL / TP from Bollinger width
        bw = (bb["upper"] - bb["lower"]) / current_price if current_price else 0.04
        atr_pct = max(bw / 2, 0.01)

        entry = round(current_price * (0.997 if sig_type == "BUY" else 1.003), 2)
        sl = round(current_price * (1 - atr_pct * 1.5), 2) if sig_type == "BUY" else round(current_price * (1 + atr_pct * 1.5), 2)
        tp = round(current_price * (1 + atr_pct * 3), 2) if sig_type == "BUY" else round(current_price * (1 - atr_pct * 3), 2)

        return {
            "symbol": symbol,
            "signals": {
                "primary_signal": {
                    "signal": sig_type,
                    "strength": strength_label,
                    "confidence": confidence,
                    "generated_at": datetime.now(timezone.utc).isoformat(),
                },
                "secondary_signals": [
                    {"type": "RSI", "signal": "Oversold" if rsi < 35 else ("Overbought" if rsi > 65 else "Neutral"), "strength": round(abs(rsi - 50) / 5)},
                    {"type": "MACD", "signal": "Bullish" if macd["histogram"] > 0 else "Bearish", "strength": min(10, int(abs(macd["histogram"])))},
                    {"type": "EMA Crossover", "signal": "Bullish" if ema9 > ema21 else "Bearish", "strength": min(10, int(abs(ema9 - ema21) / current_price * 1000))},
                ],
                "entry_points": [{"level": entry, "type": "Computed", "probability": confidence}],
                "exit_points": [{"level": tp, "type": "Take Profit", "target": "Bollinger-based"}],
                "stop_loss": {"suggested_level": sl, "percentage": round((sl / current_price - 1) * 100, 1), "type": "Volatility-based"},
                "take_profit": {"target_1": tp, "reasoning": "Based on Bollinger width and trend"},
            },
            "signal_strength": int(agreement),
            "recommended_action": self._get_recommended_action(int(agreement)),
            "ai_confidence": confidence,
            "data_source": "live",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ── assess_risk ────────────────────────────────────────────────

    def assess_risk(self, symbol: str) -> Dict:
        """Assess risk using real volatility, beta, and drawdown metrics."""
        closes = _fetch_closes(symbol)
        current_price = _fetch_live_price(symbol) or (closes[-1] if closes else 0)

        volatility = _compute_volatility(closes) if len(closes) > 5 else 25.0

        # Beta vs BTC (for crypto) or SPY (for stocks)
        bench_sym = "BTC" if symbol.upper() in ("ETH", "SOL", "BNB", "XRP", "ADA", "DOGE", "AVAX", "LINK") else "SPY"
        bench_closes = _fetch_closes(bench_sym)
        beta = _compute_beta(closes, bench_closes) if len(closes) > 10 and len(bench_closes) > 10 else 1.0

        # Real max drawdown
        max_dd = 0
        if closes:
            peak = closes[0]
            for c in closes:
                if c > peak:
                    peak = c
                dd = (c - peak) / peak * 100
                if dd < max_dd:
                    max_dd = dd
        max_dd = round(max_dd, 2)

        # VaR 95% — historical
        if len(closes) > 5:
            returns = sorted([(closes[i] / closes[i - 1] - 1) for i in range(1, len(closes)) if closes[i - 1]])
            idx = max(0, int(len(returns) * 0.05))
            var_95 = round(returns[idx] * 100, 2)
        else:
            var_95 = -5.0

        # Sharpe (annualized, risk-free = 4%)
        if len(closes) > 10:
            rets = [(closes[i] / closes[i - 1] - 1) for i in range(1, len(closes)) if closes[i - 1]]
            mean_r = sum(rets) / len(rets)
            std_r = math.sqrt(sum((r - mean_r) ** 2 for r in rets) / len(rets))
            sharpe = round(((mean_r * 365) - 0.04) / (std_r * math.sqrt(365)), 2) if std_r > 0 else 0
        else:
            sharpe = 0

        # Overall risk score 0-100
        vol_score = min(100, volatility * 1.5)
        dd_score = min(100, abs(max_dd) * 2)
        overall = round((vol_score * 0.4 + dd_score * 0.3 + max(0, 50 - sharpe * 10) * 0.3), 1)
        overall = min(100, max(0, overall))

        risk_factors = [
            {"factor": "Market Volatility", "level": self._get_risk_level(volatility, 20, 40), "score": round(volatility, 2), "impact": "High" if volatility > 40 else "Medium" if volatility > 20 else "Low"},
            {"factor": "Max Drawdown", "level": self._get_risk_level(abs(max_dd), 15, 30), "score": abs(max_dd), "impact": "High" if abs(max_dd) > 30 else "Medium"},
            {"factor": "Beta Sensitivity", "level": "High" if beta > 1.5 else ("Medium" if beta > 1.0 else "Low"), "score": beta, "impact": "High" if beta > 1.5 else "Low"},
            {"factor": "VaR Exposure", "level": "High" if var_95 < -5 else ("Medium" if var_95 < -2 else "Low"), "score": var_95, "impact": "High" if var_95 < -5 else "Low"},
        ]

        return {
            "symbol": symbol,
            "current_price": round(current_price, 2) if current_price else None,
            "overall_risk_score": overall,
            "risk_rating": self._get_risk_rating(overall),
            "metrics": {
                "volatility": round(volatility, 2),
                "beta": beta,
                "sharpe_ratio": sharpe,
                "var_95": var_95,
                "max_drawdown": max_dd,
            },
            "risk_factors": risk_factors,
            "recommendation": self._get_risk_recommendation(overall),
            "data_source": "live" if len(closes) >= 20 else "limited",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    # ── helpers ────────────────────────────────────────────────────

    def _get_recommended_action(self, strength: int) -> str:
        if strength >= 80:
            return "Strong Buy — High conviction trade"
        elif strength >= 65:
            return "Buy — Favorable risk/reward"
        elif strength >= 50:
            return "Hold — Wait for better setup"
        elif strength >= 35:
            return "Cautious — Consider reducing position"
        return "Sell — Unfavorable conditions"

    def _get_risk_level(self, value: float, med: float, high: float) -> str:
        if value > high:
            return "High"
        elif value > med:
            return "Medium"
        return "Low"

    def _get_risk_rating(self, score: float) -> str:
        if score >= 70:
            return "High Risk"
        elif score >= 50:
            return "Moderate-High Risk"
        elif score >= 35:
            return "Moderate Risk"
        elif score >= 20:
            return "Low-Moderate Risk"
        return "Low Risk"

    def _get_risk_recommendation(self, score: float) -> str:
        if score >= 70:
            return "High risk — Only for experienced traders with strong risk management"
        elif score >= 50:
            return "Moderate risk — Implement strict stop losses and position sizing"
        elif score >= 35:
            return "Acceptable risk — Good for diversified portfolios"
        return "Low risk — Suitable for conservative investors"
