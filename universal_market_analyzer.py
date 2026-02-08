#!/usr/bin/env python3
"""
Universal Market Analyzer — SignalTrust AI Scanner
════════════════════════════════════════════════════════════════
Analyzes ALL markets using REAL data only — zero random scores.

Data sources:
  • RealTimeMarketData (CoinPaprika / CoinCap / Yahoo Finance)
  • CryptoGemFinder (DEXScreener / CoinPaprika)
  • Yahoo Finance chart API (stocks)
  • DefiLlama (DeFi TVL)
"""

import json
import logging
import time
import requests
from datetime import datetime, timezone
from typing import Dict, List

from realtime_market_data import RealTimeMarketData
from crypto_gem_finder import CryptoGemFinder

logger = logging.getLogger(__name__)

# ── tiny cache ──────────────────────────────────────────────────────
_uma_cache: Dict[str, dict] = {}
_CACHE_TTL = 300


def _cached(key: str):
    e = _uma_cache.get(key)
    if e and time.time() - e["ts"] < _CACHE_TTL:
        return e["v"]
    return None


def _store(key: str, val):
    _uma_cache[key] = {"v": val, "ts": time.time()}


# ═══════════════════════════════════════════════════════════════════
#  Scoring helpers — deterministic from price data
# ═══════════════════════════════════════════════════════════════════

def _score_asset(change_pct: float, volume: float = 0) -> float:
    """Compute a deterministic 0-100 opportunity score from real metrics.

    Components:
      • Momentum (0-40): abs(change_pct) capped at 20% maps linearly to 40
      • Direction (0-30): positive change → 30, negative → 30*(1 - abs(chg)/20)
      • Volume premium (0-30): log-scaled from volume when available
    """
    import math
    abs_chg = min(abs(change_pct), 20)
    momentum = (abs_chg / 20) * 40

    if change_pct > 0:
        direction = 30
    else:
        direction = max(0, 30 * (1 - abs_chg / 20))

    vol_score = 0
    if volume and volume > 0:
        vol_score = min(30, math.log10(max(volume, 1)) * 3)

    return round(min(100, momentum + direction + vol_score), 1)


def _recommendation(score: float, change_pct: float) -> str:
    if score >= 80 and change_pct > 0:
        return "STRONG BUY"
    elif score >= 65 and change_pct > 0:
        return "BUY"
    elif score >= 50:
        return "HOLD"
    else:
        return "WATCH"


# ═══════════════════════════════════════════════════════════════════
#  Main class
# ═══════════════════════════════════════════════════════════════════

class UniversalMarketAnalyzer:
    """Comprehensive analyzer using REAL data only."""

    def __init__(self):
        self.market_data = RealTimeMarketData()
        self.gem_finder = CryptoGemFinder()

    # ── public API (same interface) ────────────────────────────────

    def analyze_everything(self) -> Dict:
        """Analyze ALL markets using real data."""
        cached = _cached("full_analysis")
        if cached:
            return cached

        logger.info("Universal market analysis starting (live data)...")

        analysis: Dict = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_assets_analyzed": 0,
            "data_source": "live",
            "markets": {},
        }

        us = self._analyze_us_stocks()
        analysis["markets"]["us_stocks"] = us
        analysis["total_assets_analyzed"] += us["count"]

        ca = self._analyze_canadian_stocks()
        analysis["markets"]["canadian_stocks"] = ca
        analysis["total_assets_analyzed"] += ca["count"]

        crypto = self._analyze_crypto()
        analysis["markets"]["cryptocurrencies"] = crypto
        analysis["total_assets_analyzed"] += crypto["count"]

        gems = self._discover_gems()
        analysis["markets"]["hidden_gems"] = gems
        analysis["total_assets_analyzed"] += gems["count"]

        defi = self._analyze_defi()
        analysis["markets"]["defi"] = defi
        analysis["total_assets_analyzed"] += defi["count"]

        analysis["top_opportunities"] = self._find_top_opportunities(analysis)

        self._save_analysis(analysis)
        _store("full_analysis", analysis)
        return analysis

    def get_analysis_summary(self) -> Dict:
        """Load cached analysis or run fresh."""
        try:
            with open("data/universal_market_analysis.json", "r") as f:
                return json.load(f)
        except Exception:
            return self.analyze_everything()

    def get_total_coverage(self) -> Dict:
        return {
            "us_stocks": len(self._us_tickers()),
            "canadian_stocks": len(self._ca_tickers()),
            "data_source": "live",
        }

    # ══════════════════════════════════════════════════════════════
    #  US Stocks — Yahoo Finance chart API
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def _us_tickers() -> List[str]:
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "AMD", "INTC", "QCOM",
            "JPM", "BAC", "WFC", "GS", "MS", "C", "BLK", "SCHW", "AXP", "V", "MA", "PYPL",
            "JNJ", "UNH", "PFE", "ABBV", "TMO", "MRK", "ABT", "DHR", "BMY", "AMGN", "LLY",
            "WMT", "HD", "COST", "TGT", "LOW", "TJX", "DG", "ROST", "BBY",
            "XOM", "CVX", "COP", "SLB", "EOG", "MPC", "PSX", "VLO", "OXY", "HAL",
            "BA", "LMT", "RTX", "GD", "NOC", "LHX",
            "PG", "KO", "PEP", "PM", "MDLZ", "CL", "GIS", "HSY",
            "GM", "F", "RIVN", "NIO",
            "DIS", "NFLX", "CMCSA", "T", "VZ", "TMUS",
            "CAT", "DE", "MMM", "HON", "UPS", "FDX", "GE",
            "CRM", "ADBE", "ORCL", "NOW", "INTU",
        ]

    def _analyze_us_stocks(self) -> Dict:
        cached = _cached("us_analysis")
        if cached:
            return cached

        tickers = self._us_tickers()
        assets = self._fetch_yahoo_batch(tickers)

        opps = []
        for a in assets:
            s = _score_asset(a["change_pct"], a.get("volume", 0))
            if s >= 60:
                opps.append({
                    "symbol": a["symbol"], "price": a["price"],
                    "change_pct": a["change_pct"], "score": s,
                    "recommendation": _recommendation(s, a["change_pct"]),
                })

        opps.sort(key=lambda x: x["score"], reverse=True)
        result = {
            "count": len(assets), "analyzed": len(assets),
            "opportunities": opps[:20], "data_source": "yahoo_finance",
        }
        _store("us_analysis", result)
        return result

    # ══════════════════════════════════════════════════════════════
    #  Canadian Stocks — Yahoo Finance (*.TO)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def _ca_tickers() -> List[str]:
        return [
            "SHOP.TO", "RY.TO", "TD.TO", "ENB.TO", "CNQ.TO", "BNS.TO", "BMO.TO",
            "TRP.TO", "CP.TO", "CNR.TO", "SU.TO", "WCN.TO", "BCE.TO", "T.TO",
            "MFC.TO", "ABX.TO", "FM.TO", "BAM.TO", "NTR.TO",
        ]

    def _analyze_canadian_stocks(self) -> Dict:
        cached = _cached("ca_analysis")
        if cached:
            return cached

        tickers = self._ca_tickers()
        assets = self._fetch_yahoo_batch(tickers)

        opps = []
        for a in assets:
            s = _score_asset(a["change_pct"], a.get("volume", 0))
            if s >= 55:
                opps.append({
                    "symbol": a["symbol"], "price": a["price"],
                    "change_pct": a["change_pct"], "score": s,
                    "recommendation": _recommendation(s, a["change_pct"]),
                })

        opps.sort(key=lambda x: x["score"], reverse=True)
        result = {
            "count": len(assets), "analyzed": len(assets),
            "opportunities": opps[:10], "data_source": "yahoo_finance",
        }
        _store("ca_analysis", result)
        return result

    # ── shared Yahoo helper ────────────────────────────────────────

    @staticmethod
    def _fetch_yahoo_batch(tickers: List[str]) -> List[Dict]:
        results: List[Dict] = []
        for t in tickers:
            try:
                r = requests.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{t}",
                    params={"range": "2d", "interval": "1d"},
                    headers={"User-Agent": "Mozilla/5.0"}, timeout=6,
                )
                if r.status_code == 200:
                    meta = r.json()["chart"]["result"][0]["meta"]
                    prev = meta.get("chartPreviousClose", meta.get("previousClose", 0))
                    price = meta.get("regularMarketPrice", prev)
                    chg = ((price - prev) / prev * 100) if prev else 0
                    results.append({
                        "symbol": t, "price": round(price, 2),
                        "change_pct": round(chg, 2),
                        "volume": meta.get("regularMarketVolume", 0),
                    })
            except Exception:
                continue
        return results

    # ══════════════════════════════════════════════════════════════
    #  Crypto — CoinPaprika tickers (free, no key)
    # ══════════════════════════════════════════════════════════════

    def _analyze_crypto(self) -> Dict:
        cached = _cached("crypto_analysis")
        if cached:
            return cached

        cryptos = self.market_data.get_all_crypto(limit=100)

        opps = []
        for c in cryptos:
            chg = c.get("change_percent", c.get("change_24h", 0)) or 0
            vol = c.get("volume_24h", c.get("volume", 0)) or 0
            s = _score_asset(chg, vol)
            if s >= 60:
                opps.append({
                    "symbol": c.get("symbol", ""), "price": c.get("price", 0),
                    "change_pct": round(chg, 2), "score": s,
                    "recommendation": _recommendation(s, chg),
                })

        opps.sort(key=lambda x: x["score"], reverse=True)
        result = {
            "count": len(cryptos), "analyzed": len(cryptos),
            "opportunities": opps[:30], "data_source": "coinpaprika",
        }
        _store("crypto_analysis", result)
        return result

    # ══════════════════════════════════════════════════════════════
    #  Hidden Gems — CryptoGemFinder (already real data)
    # ══════════════════════════════════════════════════════════════

    def _discover_gems(self) -> Dict:
        try:
            gems = self.gem_finder.discover_new_gems(limit=50)
            top = [g for g in gems if g.get("gem_score", 0) > 70]
            alerts = self.gem_finder.get_gem_alerts()
        except Exception:
            gems, top, alerts = [], [], []

        return {
            "count": len(gems),
            "top_gems": top[:20],
            "alerts": alerts,
            "data_source": "dexscreener",
        }

    # ══════════════════════════════════════════════════════════════
    #  DeFi — DefiLlama (free, no key)
    # ══════════════════════════════════════════════════════════════

    def _analyze_defi(self) -> Dict:
        cached = _cached("defi_analysis")
        if cached:
            return cached

        protocols: List[Dict] = []
        try:
            r = requests.get("https://api.llama.fi/protocols", timeout=10)
            if r.status_code == 200:
                for p in r.json()[:50]:
                    tvl = p.get("tvl", 0) or 0
                    chg_1d = p.get("change_1d", 0) or 0
                    protocols.append({
                        "symbol": p.get("symbol", ""),
                        "name": p.get("name", ""),
                        "tvl": tvl,
                        "tvl_display": f"${tvl / 1e6:.1f}M" if tvl < 1e9 else f"${tvl / 1e9:.2f}B",
                        "change_1d": round(chg_1d, 2),
                    })
        except Exception as e:
            logger.error(f"DefiLlama: {e}")

        opps = []
        for p in protocols:
            chg = p.get("change_1d", 0)
            tvl_val = p.get("tvl", 0)
            s = _score_asset(chg, tvl_val)
            if s >= 50:
                opps.append({
                    "symbol": p["symbol"], "name": p.get("name", ""),
                    "tvl": p["tvl_display"], "change_1d": p["change_1d"],
                    "score": s, "recommendation": _recommendation(s, chg),
                })

        opps.sort(key=lambda x: x["score"], reverse=True)
        result = {
            "count": len(protocols), "analyzed": len(protocols),
            "opportunities": opps[:10], "data_source": "defillama",
        }
        _store("defi_analysis", result)
        return result

    # ══════════════════════════════════════════════════════════════
    #  Cross-market opportunity ranking
    # ══════════════════════════════════════════════════════════════

    def _find_top_opportunities(self, analysis: Dict) -> List[Dict]:
        all_opps: List[Dict] = []
        for market, data in analysis["markets"].items():
            if "opportunities" in data:
                for opp in data["opportunities"]:
                    opp["market"] = market
                    all_opps.append(opp)
            elif "top_gems" in data:
                for gem in data["top_gems"][:10]:
                    all_opps.append({
                        "symbol": gem.get("symbol", ""),
                        "score": gem.get("gem_score", 0),
                        "market": "hidden_gems",
                        "recommendation": "GEM",
                        "explosion_potential": gem.get("explosion_potential", ""),
                    })
        return sorted(all_opps, key=lambda x: x.get("score", 0), reverse=True)[:50]

    # ── persistence ────────────────────────────────────────────────

    @staticmethod
    def _save_analysis(analysis: Dict):
        try:
            import os
            os.makedirs("data", exist_ok=True)
            with open("data/universal_market_analysis.json", "w") as f:
                json.dump(analysis, f, indent=2)
        except Exception as e:
            logger.error(f"Save analysis: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    analyzer = UniversalMarketAnalyzer()

    print("=" * 70)
    print("UNIVERSAL MARKET ANALYZER — LIVE DATA")
    print("=" * 70)

    analysis = analyzer.analyze_everything()

    print(f"\nTotal assets analyzed: {analysis['total_assets_analyzed']}")
    print(f"Markets covered: {len(analysis['markets'])}")
    print(f"Top opportunities: {len(analysis['top_opportunities'])}")

    for i, opp in enumerate(analysis["top_opportunities"][:10], 1):
        sym = opp.get("symbol", opp.get("name", "N/A"))
        print(f"  {i}. {sym} ({opp['market']}) — score {opp.get('score', 0):.1f} — {opp.get('recommendation', '')}")
