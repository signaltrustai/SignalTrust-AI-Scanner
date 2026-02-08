#!/usr/bin/env python3
"""
Real-time Market Data Module — REAL API Integration
Fetches LIVE data from free public APIs (no keys required):
  • CoinPaprika  → crypto prices, volumes, market caps (250+ coins)
  • CoinCap v2   → backup crypto feed
  • Yahoo Finance chart API → US & Canadian stocks
  • Alternative.me → Fear & Greed Index
Falls back to cached/estimated data if APIs are temporarily unreachable.
"""

import hashlib
import requests
import time
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional


class RealTimeMarketData:
    """Real-time market data provider using FREE public APIs."""

    # ── API endpoints (all free, no key required) ──────────────────────
    COINPAPRIKA_BASE = "https://api.coinpaprika.com/v1"
    COINCAP_BASE = "https://api.coincap.io/v2"
    YAHOO_CHART = "https://query1.finance.yahoo.com/v8/finance/chart"
    FEAR_GREED_URL = "https://api.alternative.me/fng/"

    # ── Symbol lists ───────────────────────────────────────────────────
    CANADIAN_STOCKS = [
        'RY.TO', 'TD.TO', 'BNS.TO', 'BMO.TO', 'CNR.TO', 'ENB.TO',
        'SU.TO', 'CNQ.TO', 'CP.TO', 'TRP.TO', 'MFC.TO',
        'SLF.TO', 'BCE.TO', 'T.TO', 'ABX.TO', 'FNV.TO', 'SHOP.TO',
        'WCN.TO', 'ATD.TO', 'QSR.TO', 'WPM.TO', 'CSU.TO',
    ]
    US_STOCKS = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B',
        'JPM', 'V', 'JNJ', 'WMT', 'PG', 'MA', 'HD', 'CVX', 'LLY', 'PFE',
        'ABBV', 'KO', 'PEP', 'COST', 'AVGO', 'MRK', 'TMO', 'CSCO', 'ACN',
        'NKE', 'ORCL', 'DIS', 'ADBE', 'CRM', 'ABT', 'NFLX', 'INTC', 'VZ',
        'CMCSA', 'AMD', 'TXN', 'PM', 'NEE', 'UNP', 'HON', 'QCOM', 'IBM',
        'BA', 'GE', 'CAT', 'GS', 'AXP',
    ]
    CRYPTOCURRENCIES = [
        'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'DOT', 'MATIC',
        'AVAX', 'LINK', 'UNI', 'ATOM', 'LTC', 'BCH', 'XLM', 'ALGO', 'VET',
        'ICP', 'FIL', 'MANA', 'SAND', 'AXS', 'THETA', 'EGLD', 'XTZ', 'HBAR',
        'NEAR', 'FTM', 'EOS', 'AAVE', 'GRT', 'CAKE', 'MKR', 'NEO', 'KSM',
        'RUNE', 'WAVES', 'ZEC', 'DASH', 'ENJ', 'CHZ', 'BAT', 'ZIL', 'COMP',
        'YFI', 'SUSHI', 'SNX', '1INCH', 'CRV', 'UMA', 'BAL', 'REN', 'LRC',
        'STORJ', 'NMR', 'ANT', 'KNC', 'BNT', 'MLN',
    ]
    DEFI_TOKENS = [
        'AAVE', 'UNI', 'SUSHI', 'COMP', 'MKR', 'SNX', 'YFI', 'CRV',
        '1INCH', 'BAL', 'LRC', 'REN', 'UMA', 'BNT', 'KNC',
    ]
    NFT_TOKENS = [
        'MANA', 'SAND', 'AXS', 'ENJ', 'CHZ', 'FLOW', 'GALA', 'APE',
        'IMX', 'BLUR', 'LRC',
    ]

    # ── Shared HTTP session ────────────────────────────────────────────
    _SESSION = requests.Session()
    _SESSION.headers.update({
        "User-Agent": "SignalTrust-AI-Scanner/2.0",
        "Accept": "application/json",
    })

    def __init__(self):
        self._crypto_cache: Optional[List[Dict]] = None
        self._crypto_cache_ts: float = 0
        self._stock_cache: Dict[str, dict] = {}
        self._cache_ttl = 120  # 2 min

    # ══════════════════════════════════════════════════════════════════
    #  PUBLIC — Crypto
    # ══════════════════════════════════════════════════════════════════

    def get_all_crypto(self, limit: int = None) -> List[Dict]:
        """Get real cryptocurrency data.
        
        Args:
            limit: Max coins to return (None = all available).
        """
        data = self._load_crypto()
        return data[:limit] if limit else data

    def get_defi_tokens(self) -> List[Dict]:
        """Get DeFi tokens from the crypto feed."""
        upper = {s.upper() for s in self.DEFI_TOKENS}
        return [c for c in self._load_crypto() if c["symbol"].upper() in upper]

    def get_nft_tokens(self) -> List[Dict]:
        """Get NFT/Metaverse tokens from the crypto feed."""
        upper = {s.upper() for s in self.NFT_TOKENS}
        return [c for c in self._load_crypto() if c["symbol"].upper() in upper]

    # ══════════════════════════════════════════════════════════════════
    #  PUBLIC — Stocks
    # ══════════════════════════════════════════════════════════════════

    def get_canadian_stocks(self, limit: int = None) -> List[Dict]:
        """Get Canadian stock data (TSX) from Yahoo Finance."""
        syms = self.CANADIAN_STOCKS[:limit] if limit else self.CANADIAN_STOCKS
        return [s for s in (self._load_stock(sym, "TSX", "CAD") for sym in syms) if s]

    def get_us_stocks(self, limit: int = None) -> List[Dict]:
        """Get US stock data from Yahoo Finance."""
        syms = self.US_STOCKS[:limit] if limit else self.US_STOCKS
        return [s for s in (self._load_stock(sym, "NYSE/NASDAQ", "USD") for sym in syms) if s]

    # ══════════════════════════════════════════════════════════════════
    #  PUBLIC — Summary
    # ══════════════════════════════════════════════════════════════════

    def get_market_summary(self) -> Dict:
        """Comprehensive market summary with real data."""
        return {
            'canadian_stocks': {
                'total': len(self.CANADIAN_STOCKS),
                'data': self.get_canadian_stocks(10),
                'market': 'TSX', 'currency': 'CAD',
            },
            'us_stocks': {
                'total': len(self.US_STOCKS),
                'data': self.get_us_stocks(20),
                'markets': ['NYSE', 'NASDAQ'], 'currency': 'USD',
            },
            'cryptocurrencies': {
                'total': len(self.CRYPTOCURRENCIES),
                'data': self.get_all_crypto(30),
                'market': 'Global Crypto',
            },
            'defi': {
                'total': len(self.DEFI_TOKENS),
                'data': self.get_defi_tokens(),
                'category': 'DeFi',
            },
            'nft': {
                'total': len(self.NFT_TOKENS),
                'data': self.get_nft_tokens(),
                'category': 'NFT/Metaverse',
            },
            'fear_greed_index': self._load_fear_greed(),
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'last_update': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
        }

    def search_symbol(self, query: str) -> List[Dict]:
        """Search crypto + stocks by symbol substring."""
        q = query.upper()
        results: List[Dict] = []
        for c in self._load_crypto():
            if q in c["symbol"].upper() or q in c.get("name", "").upper():
                results.append(c)
        for sym in self.CANADIAN_STOCKS + self.US_STOCKS:
            if q in sym.upper():
                s = self._load_stock(sym)
                if s:
                    results.append(s)
        return results[:20]

    # ══════════════════════════════════════════════════════════════════
    #  INTERNAL — Crypto (CoinPaprika → CoinCap → fallback)
    # ══════════════════════════════════════════════════════════════════

    def _load_crypto(self) -> List[Dict]:
        if self._crypto_cache and (time.time() - self._crypto_cache_ts) < self._cache_ttl:
            return self._crypto_cache
        data = self._api_coinpaprika() or self._api_coincap() or self._fallback_crypto()
        self._crypto_cache = data
        self._crypto_cache_ts = time.time()
        return data

    def _api_coinpaprika(self) -> Optional[List[Dict]]:
        try:
            r = self._SESSION.get(f"{self.COINPAPRIKA_BASE}/tickers", params={"limit": 250}, timeout=12)
            if r.status_code != 200:
                return None
            out: List[Dict] = []
            for c in r.json():
                q = c.get("quotes", {}).get("USD", {})
                price = q.get("price", 0)
                pct24 = q.get("percent_change_24h", 0)
                out.append({
                    "symbol": c.get("symbol", ""),
                    "name": c.get("name", ""),
                    "category": "Crypto",
                    "price": price,
                    "change": round(price * pct24 / 100, 6),
                    "change_percent": round(pct24, 2),
                    "change_1h": round(q.get("percent_change_1h", 0), 2),
                    "change_7d": round(q.get("percent_change_7d", 0), 2),
                    "change_30d": round(q.get("percent_change_30d", 0), 2),
                    "volume_24h": f"${round(q.get('volume_24h', 0)/1e6, 1)}M",
                    "volume_24h_raw": q.get("volume_24h", 0),
                    "market_cap": f"${round(q.get('market_cap', 0)/1e9, 2)}B",
                    "market_cap_raw": q.get("market_cap", 0),
                    "rank": c.get("rank", 0),
                    "ath": q.get("ath_price", 0),
                    "percent_from_ath": round(q.get("percent_from_price_ath", 0), 2),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source": "coinpaprika",
                })
            return out
        except Exception as e:
            print(f"⚠️ CoinPaprika: {e}")
            return None

    def _api_coincap(self) -> Optional[List[Dict]]:
        try:
            r = self._SESSION.get(f"{self.COINCAP_BASE}/assets", params={"limit": 250}, timeout=12)
            if r.status_code != 200:
                return None
            out: List[Dict] = []
            for c in r.json().get("data", []):
                price = float(c.get("priceUsd") or 0)
                pct = float(c.get("changePercent24Hr") or 0)
                vol = float(c.get("volumeUsd24Hr") or 0)
                mcap = float(c.get("marketCapUsd") or 0)
                out.append({
                    "symbol": c.get("symbol", ""),
                    "name": c.get("name", ""),
                    "category": "Crypto",
                    "price": round(price, 8 if price < 1 else 2),
                    "change": round(price * pct / 100, 6),
                    "change_percent": round(pct, 2),
                    "volume_24h": f"${round(vol/1e6,1)}M",
                    "volume_24h_raw": vol,
                    "market_cap": f"${round(mcap/1e9,2)}B",
                    "market_cap_raw": mcap,
                    "rank": int(c.get("rank") or 0),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source": "coincap",
                })
            return out
        except Exception as e:
            print(f"⚠️ CoinCap: {e}")
            return None

    def _fallback_crypto(self) -> List[Dict]:
        """Last-resort estimated crypto data using deterministic baselines."""
        baselines = {"BTC": 55000, "ETH": 3000, "BNB": 300, "SOL": 150, "XRP": 0.55,
                     "ADA": 0.35, "DOGE": 0.08, "DOT": 6, "AVAX": 35, "LINK": 15}
        volume_est = {"BTC": 30000, "ETH": 15000, "BNB": 2000, "SOL": 3000, "XRP": 1500,
                      "ADA": 800, "DOGE": 1000, "DOT": 500, "AVAX": 700, "LINK": 600}
        mcap_est = {"BTC": 1100, "ETH": 360, "BNB": 45, "SOL": 65, "XRP": 30,
                    "ADA": 12, "DOGE": 11, "DOT": 8, "AVAX": 13, "LINK": 9}
        out = []
        for i, sym in enumerate(self.CRYPTOCURRENCIES):
            bp = baselines.get(sym, 1.0)
            out.append({
                "symbol": sym, "name": f"{sym}", "category": "Crypto",
                "price": bp,
                "change_percent": 0.0,
                "change": 0.0,
                "volume_24h": f"${volume_est.get(sym, 100)}M",
                "market_cap": f"${mcap_est.get(sym, 1)}B",
                "rank": i + 1,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "fallback",
            })
        return out

    # ══════════════════════════════════════════════════════════════════
    #  INTERNAL — Stocks (Yahoo Finance chart API)
    # ══════════════════════════════════════════════════════════════════

    def _load_stock(self, symbol: str, market: str = "", currency: str = "USD") -> Optional[Dict]:
        ck = f"stk:{symbol}"
        cached = self._stock_cache.get(ck)
        if cached and (time.time() - cached["_t"]) < self._cache_ttl:
            return cached["d"]

        data = self._api_yahoo(symbol, market, currency)
        if data:
            self._stock_cache[ck] = {"d": data, "_t": time.time()}
        return data

    def _api_yahoo(self, symbol: str, market: str = "", currency: str = "USD") -> Optional[Dict]:
        try:
            r = self._SESSION.get(
                f"{self.YAHOO_CHART}/{symbol}",
                params={"range": "5d", "interval": "1d", "includePrePost": "false"},
                timeout=8,
            )
            if r.status_code != 200:
                return self._fallback_stock(symbol, market, currency)
            res = r.json().get("chart", {}).get("result")
            if not res:
                return self._fallback_stock(symbol, market, currency)
            meta = res[0].get("meta", {})
            price = meta.get("regularMarketPrice", 0)
            prev = meta.get("chartPreviousClose") or meta.get("previousClose") or price
            chg = price - prev
            pct = (chg / prev * 100) if prev else 0
            return {
                "symbol": symbol,
                "name": meta.get("shortName") or symbol.replace(".TO", ""),
                "market": market or meta.get("exchangeName", ""),
                "currency": currency or meta.get("currency", "USD"),
                "price": round(price, 2),
                "change": round(chg, 2),
                "change_percent": round(pct, 2),
                "volume": meta.get("regularMarketVolume", 0),
                "52w_high": meta.get("fiftyTwoWeekHigh", 0),
                "52w_low": meta.get("fiftyTwoWeekLow", 0),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "source": "yahoo_finance",
            }
        except Exception as e:
            print(f"⚠️ Yahoo [{symbol}]: {e}")
            return self._fallback_stock(symbol, market, currency)

    def _fallback_stock(self, symbol: str, market: str, currency: str) -> Dict:
        """Fallback stock data with deterministic baseline values."""
        # Deterministic price from symbol hash
        h = int(hashlib.md5(symbol.encode()).hexdigest()[:8], 16)
        bp = 15 + (h % 385)  # 15–400 range
        return {
            "symbol": symbol, "name": symbol.replace(".TO", ""),
            "market": market, "currency": currency,
            "price": round(bp, 2), "change": 0.0,
            "change_percent": 0.0,
            "volume": 0,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source": "fallback",
        }

    # ══════════════════════════════════════════════════════════════════
    #  INTERNAL — Fear & Greed
    # ══════════════════════════════════════════════════════════════════

    def _load_fear_greed(self) -> Dict:
        try:
            r = self._SESSION.get(self.FEAR_GREED_URL, timeout=5)
            if r.status_code == 200:
                d = r.json().get("data", [{}])[0]
                return {
                    "value": int(d.get("value", 50)),
                    "classification": d.get("value_classification", "Neutral"),
                    "source": "alternative.me",
                }
        except Exception:
            pass
        return {"value": 50, "classification": "Neutral", "source": "fallback"}
