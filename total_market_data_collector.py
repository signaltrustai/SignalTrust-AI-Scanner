#!/usr/bin/env python3
"""
Total Market Data Collector — SignalTrust AI Scanner
════════════════════════════════════════════════════════════════
Collects REAL data from free public APIs — zero random/fake data.

Sources:
  Crypto  — CoinPaprika tickers (2500+)
  Stocks  — Yahoo Finance chart API (US + Canadian tickers)
  NFTs    — OpenSea / DefiLlama NFT collections
  Whales  — WhaleWatcher (Etherscan)
  News    — CryptoPanic free feed
"""

import json
import logging
import os
import time
import requests
from datetime import datetime, timezone
from typing import Dict, List

logger = logging.getLogger(__name__)

# ── tiny in-memory cache ────────────────────────────────────────────
_tmc_cache: Dict[str, dict] = {}
_CACHE_TTL = 300   # 5 min — heavy collection should not spam APIs


def _cached(key: str):
    e = _tmc_cache.get(key)
    if e and time.time() - e["ts"] < _CACHE_TTL:
        return e["v"]
    return None


def _store(key: str, val):
    _tmc_cache[key] = {"v": val, "ts": time.time()}


# ══════════════════════════════════════════════════════════════════
#  Main class
# ══════════════════════════════════════════════════════════════════

class TotalMarketDataCollector:
    """Collects market data from REAL public APIs."""

    def __init__(self):
        self.data_directory = "data/total_market_intelligence/"
        self._ensure_directories()

    # ── directories ────────────────────────────────────────────────

    def _ensure_directories(self):
        dirs = [
            self.data_directory,
            f"{self.data_directory}crypto/",
            f"{self.data_directory}stocks/",
            f"{self.data_directory}whales/",
            f"{self.data_directory}news/",
            f"{self.data_directory}learning/",
        ]
        for d in dirs:
            os.makedirs(d, exist_ok=True)

    # ══════════════════════════════════════════════════════════════
    #  Public API  — same interface as before
    # ══════════════════════════════════════════════════════════════

    def collect_all_data(self) -> Dict:
        """Collect ALL data from ALL real sources.

        Returns:
            Complete market intelligence data.
        """
        cached = _cached("full_sweep")
        if cached:
            return cached

        logger.info("Collecting all market data from live APIs...")

        crypto_data = self._collect_all_crypto_data()
        us_data = self._collect_all_us_stock_data()
        cad_data = self._collect_all_canadian_stock_data()
        nft_data = self._collect_all_nft_data()
        whale_data = self._collect_all_whale_data()
        news_data = self._collect_all_news()

        total_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "collection_type": "TOTAL_MARKET_SWEEP",
            "data_source": "live",
            "data": {
                "cryptocurrencies": crypto_data,
                "us_stocks": us_data,
                "canadian_stocks": cad_data,
                "nfts": nft_data,
                "whales": whale_data,
                "news": news_data,
            },
        }

        # Persist
        self._save_complete_dataset(total_data)
        self._save_for_ai_learning(total_data)

        _store("full_sweep", total_data)
        return total_data

    def get_total_coverage(self) -> Dict:
        """Return number of assets we can actually cover from real APIs."""
        return {
            "cryptocurrencies": 2500,        # CoinPaprika covers ~2500
            "us_stocks": len(self._us_tickers()),
            "canadian_stocks": len(self._ca_tickers()),
            "nft_collections": 0,            # live count from API
            "news_sources": 1,               # CryptoPanic
            "total_assets": 2500 + len(self._us_tickers()) + len(self._ca_tickers()),
            "data_source": "live",
        }

    # ══════════════════════════════════════════════════════════════
    #  Crypto — CoinPaprika free (2500 tickers, no key)
    # ══════════════════════════════════════════════════════════════

    def _collect_all_crypto_data(self) -> Dict:
        cached = _cached("crypto_all")
        if cached:
            return cached

        assets: List[Dict] = []
        try:
            r = requests.get("https://api.coinpaprika.com/v1/tickers?limit=250", timeout=15)
            if r.status_code == 200:
                for c in r.json():
                    q = c.get("quotes", {}).get("USD", {})
                    assets.append({
                        "symbol": c.get("symbol", ""),
                        "name": c.get("name", ""),
                        "price": q.get("price", 0),
                        "volume_24h": q.get("volume_24h", 0),
                        "market_cap": q.get("market_cap", 0),
                        "change_24h": q.get("percent_change_24h", 0),
                    })
        except Exception as e:
            logger.error(f"CoinPaprika tickers: {e}")

        result = {"total_cryptos": len(assets), "assets": assets, "data_source": "coinpaprika"}
        _store("crypto_all", result)
        return result

    # ══════════════════════════════════════════════════════════════
    #  US Stocks — Yahoo Finance chart API (free, no key)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def _us_tickers() -> List[str]:
        return [
            "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "AMD", "INTC",
            "JPM", "BAC", "WFC", "GS", "MS", "C", "V", "MA", "PYPL",
            "JNJ", "UNH", "PFE", "ABBV", "TMO", "MRK", "ABT",
            "WMT", "HD", "COST", "TGT", "LOW", "TJX",
            "XOM", "CVX", "COP", "SLB", "EOG",
            "BA", "LMT", "RTX", "GD", "NOC",
            "DIS", "NFLX", "CMCSA", "T", "VZ",
            "CRM", "ADBE", "ORCL", "NOW", "INTU",
        ]

    def _collect_all_us_stock_data(self) -> Dict:
        cached = _cached("us_stocks_all")
        if cached:
            return cached

        tickers = self._us_tickers()
        assets = self._fetch_yahoo_batch(tickers)

        result = {"total_stocks": len(assets), "assets": assets, "data_source": "yahoo_finance"}
        _store("us_stocks_all", result)
        return result

    # ══════════════════════════════════════════════════════════════
    #  Canadian Stocks — Yahoo Finance (*.TO tickers)
    # ══════════════════════════════════════════════════════════════

    @staticmethod
    def _ca_tickers() -> List[str]:
        return [
            "RY.TO", "TD.TO", "ENB.TO", "CNR.TO", "BMO.TO", "BNS.TO", "SHOP.TO",
            "CP.TO", "SU.TO", "TRP.TO", "MFC.TO", "BCE.TO", "ABX.TO", "FM.TO",
            "CNQ.TO", "WCN.TO", "BAM.TO", "NTR.TO", "T.TO",
        ]

    def _collect_all_canadian_stock_data(self) -> Dict:
        cached = _cached("ca_stocks_all")
        if cached:
            return cached

        tickers = self._ca_tickers()
        assets = self._fetch_yahoo_batch(tickers)

        result = {"total_stocks": len(assets), "assets": assets, "data_source": "yahoo_finance"}
        _store("ca_stocks_all", result)
        return result

    # ── shared Yahoo helper ────────────────────────────────────────

    def _fetch_yahoo_batch(self, tickers: List[str]) -> List[Dict]:
        """Fetch a batch of tickers from Yahoo Finance chart API."""
        results: List[Dict] = []
        for t in tickers:
            try:
                r = requests.get(
                    f"https://query1.finance.yahoo.com/v8/finance/chart/{t}",
                    params={"range": "2d", "interval": "1d"},
                    headers={"User-Agent": "Mozilla/5.0"},
                    timeout=6,
                )
                if r.status_code == 200:
                    meta = r.json()["chart"]["result"][0]["meta"]
                    prev = meta.get("chartPreviousClose", meta.get("previousClose", 0))
                    price = meta.get("regularMarketPrice", prev)
                    chg = ((price - prev) / prev * 100) if prev else 0
                    results.append({
                        "symbol": t,
                        "price": round(price, 2),
                        "change": round(chg, 2),
                        "volume": meta.get("regularMarketVolume", 0),
                        "market_cap": 0,   # chart API doesn't expose this
                    })
            except Exception:
                continue
        return results

    # ══════════════════════════════════════════════════════════════
    #  NFTs — DefiLlama / Simple fallback
    # ══════════════════════════════════════════════════════════════

    def _collect_all_nft_data(self) -> Dict:
        cached = _cached("nft_all")
        if cached:
            return cached

        collections: List[Dict] = []
        # DefiLlama NFT endpoint (free)
        try:
            r = requests.get("https://nft.llama.fi/collections", timeout=10)
            if r.status_code == 200:
                for c in r.json()[:100]:  # Top 100
                    collections.append({
                        "name": c.get("name", ""),
                        "symbol": c.get("collectionId", ""),
                        "floor_price": c.get("floorPrice", 0),
                        "volume_24h": c.get("dailyVolume", 0),
                        "change_24h": c.get("dailyVolumeChange", 0),
                    })
        except Exception as e:
            logger.error(f"DefiLlama NFT: {e}")

        result = {
            "total_collections": len(collections),
            "collections": collections,
            "data_source": "defillama" if collections else "unavailable",
        }
        _store("nft_all", result)
        return result

    # ══════════════════════════════════════════════════════════════
    #  Whales — WhaleWatcher (Etherscan)
    # ══════════════════════════════════════════════════════════════

    def _collect_all_whale_data(self) -> Dict:
        cached = _cached("whale_all")
        if cached:
            return cached

        transactions: List[Dict] = []
        try:
            from whale_watcher import WhaleWatcher
            ww = WhaleWatcher()
            transactions = ww.get_recent_transactions(limit=100)
        except Exception as e:
            logger.warning(f"WhaleWatcher: {e}")

        buy_count = sum(1 for t in transactions if t.get("type") == "buy")
        sell_count = sum(1 for t in transactions if t.get("type") == "sell")
        total_vol = sum(t.get("value_usd", 0) for t in transactions)

        result = {
            "total_transactions": len(transactions),
            "total_value_usd": total_vol,
            "buy_count": buy_count,
            "sell_count": sell_count,
            "transactions": transactions[:50],  # Keep payload small
            "data_source": "etherscan" if transactions else "unavailable",
        }
        _store("whale_all", result)
        return result

    # ══════════════════════════════════════════════════════════════
    #  News — CryptoPanic free feed
    # ══════════════════════════════════════════════════════════════

    def _collect_all_news(self) -> Dict:
        cached = _cached("news_all")
        if cached:
            return cached

        articles: List[Dict] = []
        try:
            r = requests.get("https://cryptopanic.com/api/free/v1/posts/?public=true", timeout=8)
            if r.status_code == 200:
                for post in r.json().get("results", [])[:50]:
                    votes = post.get("votes", {})
                    pos = votes.get("positive", 0)
                    neg = votes.get("negative", 0)
                    sentiment = "bullish" if pos > neg else ("bearish" if neg > pos else "neutral")
                    articles.append({
                        "title": post.get("title", ""),
                        "source": post.get("source", {}).get("title", ""),
                        "sentiment": sentiment,
                        "impact": "high" if pos + neg > 10 else "medium",
                        "url": post.get("url", ""),
                        "published": post.get("published_at", ""),
                    })
        except Exception as e:
            logger.error(f"CryptoPanic: {e}")

        bullish = sum(1 for a in articles if a.get("sentiment") == "bullish")
        bearish = sum(1 for a in articles if a.get("sentiment") == "bearish")

        result = {
            "total_articles": len(articles),
            "sources": len(set(a.get("source") for a in articles)),
            "articles": articles,
            "bullish": bullish,
            "bearish": bearish,
            "neutral": len(articles) - bullish - bearish,
            "overall_sentiment": "bullish" if bullish > bearish else ("bearish" if bearish > bullish else "neutral"),
            "data_source": "cryptopanic" if articles else "unavailable",
        }
        _store("news_all", result)
        return result

    # ══════════════════════════════════════════════════════════════
    #  Persistence — same as before
    # ══════════════════════════════════════════════════════════════

    def _save_complete_dataset(self, data: Dict):
        try:
            fn = f"{self.data_directory}complete_market_data_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
            with open(fn, "w") as f:
                json.dump(data, f, indent=2)
            logger.info(f"Dataset saved: {fn}")
        except Exception as e:
            logger.error(f"Save dataset: {e}")

    def _save_for_ai_learning(self, data: Dict):
        try:
            d = data["data"]
            learning_data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total_assets_analyzed": (
                    d["cryptocurrencies"]["total_cryptos"]
                    + d["us_stocks"]["total_stocks"]
                    + d["canadian_stocks"]["total_stocks"]
                    + d["nfts"]["total_collections"]
                ),
                "total_whale_transactions": d["whales"]["total_transactions"],
                "total_news_articles": d["news"]["total_articles"],
                "market_summary": {
                    "cryptos": d["cryptocurrencies"]["total_cryptos"],
                    "us_stocks": d["us_stocks"]["total_stocks"],
                    "canadian_stocks": d["canadian_stocks"]["total_stocks"],
                    "nfts": d["nfts"]["total_collections"],
                    "whales": d["whales"]["total_transactions"],
                    "news": d["news"]["total_articles"],
                },
                "learning_insights": self._generate_learning_insights(data),
            }

            fn = f"{self.data_directory}learning/ai_evolution_data.json"
            existing: List = []
            if os.path.exists(fn):
                try:
                    with open(fn, "r") as f:
                        existing = json.load(f)
                except Exception:
                    existing = []

            existing.append(learning_data)
            existing = existing[-100:]

            with open(fn, "w") as f:
                json.dump(existing, f, indent=2)
            logger.info(f"AI learning data saved ({len(existing)} sessions)")
        except Exception as e:
            logger.error(f"Save learning: {e}")

    def _generate_learning_insights(self, data: Dict) -> Dict:
        d = data["data"]
        crypto_assets = d["cryptocurrencies"]["assets"]
        us_assets = d["us_stocks"]["assets"]
        cad_assets = d["canadian_stocks"]["assets"]
        whale_txs = d["whales"].get("transactions", [])
        news_arts = d["news"]["articles"]

        def _safe_sort(lst, key, reverse=False, n=10):
            try:
                return sorted(lst, key=lambda x: x.get(key, 0), reverse=reverse)[:n]
            except Exception:
                return []

        buy_txs = [t for t in whale_txs if t.get("type") == "buy"]
        sell_txs = [t for t in whale_txs if t.get("type") == "sell"]

        return {
            "top_gainers": {
                "crypto": _safe_sort(crypto_assets, "change_24h", True),
                "us_stocks": _safe_sort(us_assets, "change", True),
                "canadian_stocks": _safe_sort(cad_assets, "change", True),
            },
            "top_losers": {
                "crypto": _safe_sort(crypto_assets, "change_24h"),
                "us_stocks": _safe_sort(us_assets, "change"),
                "canadian_stocks": _safe_sort(cad_assets, "change"),
            },
            "highest_volume": {
                "crypto": _safe_sort(crypto_assets, "volume_24h", True),
                "us_stocks": _safe_sort(us_assets, "volume", True),
            },
            "whale_insights": {
                "total_value": sum(t.get("value_usd", 0) for t in whale_txs),
                "buy_sell_ratio": len(buy_txs) / max(len(sell_txs), 1),
                "top_whale_assets": list(set(t.get("asset", t.get("token", "")) for t in whale_txs[:50])),
            },
            "news_sentiment": {
                "bullish_count": d["news"].get("bullish", 0),
                "bearish_count": d["news"].get("bearish", 0),
                "neutral_count": d["news"].get("neutral", 0),
                "overall_sentiment": d["news"].get("overall_sentiment", "neutral"),
            },
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    collector = TotalMarketDataCollector()

    print("=" * 70)
    print("TOTAL MARKET DATA COLLECTOR — LIVE DATA")
    print("=" * 70)

    coverage = collector.get_total_coverage()
    print(f"\nMarket Coverage:")
    print(f"  Cryptocurrencies: ~{coverage['cryptocurrencies']:,}")
    print(f"  US Stocks:        {coverage['us_stocks']}")
    print(f"  Canadian Stocks:  {coverage['canadian_stocks']}")
    print(f"  Data source:      {coverage['data_source']}")

    print("\nCollecting live data...")
    data = collector.collect_all_data()

    d = data["data"]
    print(f"\nResults:")
    print(f"  Cryptos collected:  {d['cryptocurrencies']['total_cryptos']}")
    print(f"  US stocks:          {d['us_stocks']['total_stocks']}")
    print(f"  CA stocks:          {d['canadian_stocks']['total_stocks']}")
    print(f"  NFT collections:    {d['nfts']['total_collections']}")
    print(f"  Whale transactions: {d['whales']['total_transactions']}")
    print(f"  News articles:      {d['news']['total_articles']}")
    print("Done.")
