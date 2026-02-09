#!/usr/bin/env python3
"""
Market Scanner Module — v2.0 (real data)
Scans crypto, stock, and forex markets using free public APIs.

Data sources (no API key required):
  • CoinPaprika  — crypto prices & trending
  • CoinCap v2   — crypto fallback
  • Binance      — crypto tickers
  • Yahoo Finance chart API — stocks & indices

Data sources (API key via .env):
  • FinancialData.net — stocks, crypto, forex, indices, fundamentals

Falls back gracefully to cached / estimated data when APIs are unreachable.
"""

import logging
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    requests = None
    HTTPAdapter = None
    Retry = None

logger = logging.getLogger(__name__)

# Import FinancialData.net provider
try:
    from financial_data_provider import financial_data as _fdn
except ImportError:
    _fdn = None

# ────────────────────────────────────────────────────────────────────
#  Constants
# ────────────────────────────────────────────────────────────────────

_CRYPTO_SYMBOLS = [
    'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'DOT',
    'MATIC', 'AVAX', 'LINK', 'UNI', 'ATOM', 'LTC', 'NEAR',
    'FTM', 'ALGO', 'ARB', 'OP', 'APT',
]

_STOCK_SYMBOLS = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'META',
    'JPM', 'V', 'JNJ', 'WMT', 'PG', 'MA', 'HD', 'LLY',
    'CVX', 'PFE', 'BAC', 'DIS', 'NFLX',
]

_FOREX_PAIRS = [
    'EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD',
    'USD/CAD', 'NZD/USD', 'EUR/GBP', 'EUR/JPY',
]

_PAPRIKA_IDS: Dict[str, str] = {
    'BTC': 'btc-bitcoin', 'ETH': 'eth-ethereum', 'BNB': 'bnb-binance-coin',
    'XRP': 'xrp-xrp', 'ADA': 'ada-cardano', 'DOGE': 'doge-dogecoin',
    'SOL': 'sol-solana', 'DOT': 'dot-polkadot', 'MATIC': 'matic-polygon',
    'AVAX': 'avax-avalanche', 'LINK': 'link-chainlink', 'UNI': 'uni-uniswap',
    'ATOM': 'atom-cosmos', 'LTC': 'ltc-litecoin', 'NEAR': 'near-near-protocol',
    'FTM': 'ftm-fantom', 'ALGO': 'algo-algorand', 'ARB': 'arb-arbitrum',
    'OP': 'op-optimism', 'APT': 'apt-aptos',
}


class MarketScanner:
    """Scanner for multiple market types using real APIs."""

    def __init__(self):
        """Initialize market scanner with connection pooling."""
        self.watchlist: List[str] = []
        self.scan_history: List[Dict] = []
        self._cache: Dict[str, Dict] = {}
        self._cache_ttl = 120  # seconds
        self._session = None
        if requests:
            self._session = requests.Session()
            retry = Retry(total=2, backoff_factor=0.3, status_forcelist=[429, 500, 502, 503, 504])
            adapter = HTTPAdapter(pool_connections=5, pool_maxsize=10, max_retries=retry)
            self._session.mount("https://", adapter)
            self._session.mount("http://", adapter)
            self._session.headers.update({
                'User-Agent': 'SignalTrust-Scanner/2.0',
                'Accept': 'application/json',
            })

    # ── Public API ───────────────────────────────────────────────────

    def get_markets_overview(self) -> Dict:
        """Get overview of all major markets with real data (parallel fetch)."""
        results: Dict[str, object] = {}

        with ThreadPoolExecutor(max_workers=4) as pool:
            futures = {
                pool.submit(self._fetch_crypto_overview): 'crypto',
                pool.submit(self._fetch_stock_overview): 'stocks',
                pool.submit(self._fetch_indices): 'indices',
                pool.submit(self._get_forex_pairs, 5): 'forex',
            }
            for f in as_completed(futures, timeout=20):
                key = futures[f]
                try:
                    results[key] = f.result()
                except Exception:
                    results[key] = {} if key != 'forex' else []

        return {
            'stocks': results.get('stocks', {}),
            'crypto': results.get('crypto', {}),
            'forex': {'total_pairs': len(_FOREX_PAIRS), 'major_pairs': results.get('forex', [])},
            'indices': {'major_indices': results.get('indices', {})},
        }

    def scan_market(self, market_type: str, symbols: List[str]) -> Dict:
        """Scan specific market symbols with real data.

        Args:
            market_type: Type of market (stocks, crypto, forex)
            symbols: List of symbols to scan

        Returns:
            Scan results
        """
        results: List[Dict] = []
        for symbol in symbols:
            data = self._scan_symbol(symbol, market_type)
            results.append(data)

        self.scan_history.append({
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'market_type': market_type,
            'symbols': symbols,
        })

        return {
            'market_type': market_type,
            'symbols_scanned': len(symbols),
            'results': results,
        }

    def get_trending_assets(self, market_type: str) -> List[Dict]:
        """Get trending assets with real data.

        Args:
            market_type: Type of market

        Returns:
            List of trending assets
        """
        if market_type == 'crypto':
            return self._fetch_trending_crypto(20)
        elif market_type == 'stocks':
            return self._fetch_stock_list(20, sort_by='change')
        elif market_type == 'forex':
            return self._get_forex_pairs(20)
        return []

    def get_watchlist(self) -> List[Dict]:
        """Get user's watchlist with live data."""
        if not self.watchlist:
            self.watchlist = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'NVDA']
        return [self._scan_symbol(s, 'stocks') for s in self.watchlist]

    def add_to_watchlist(self, symbol: str) -> Dict:
        if symbol not in self.watchlist:
            self.watchlist.append(symbol)
            return {'added': True, 'symbol': symbol, 'watchlist_size': len(self.watchlist)}
        return {'added': False, 'message': 'Symbol already in watchlist'}

    def remove_from_watchlist(self, symbol: str) -> Dict:
        if symbol in self.watchlist:
            self.watchlist.remove(symbol)
            return {'removed': True, 'symbol': symbol, 'watchlist_size': len(self.watchlist)}
        return {'removed': False, 'message': 'Symbol not in watchlist'}

    # ── Crypto (CoinPaprika → CoinCap → Binance) ────────────────────

    def _fetch_crypto_overview(self) -> Dict:
        """Fetch live crypto market overview."""
        tickers = self._fetch_paprika_tickers()
        if not tickers:
            tickers = self._fetch_coincap_tickers()

        up = sum(1 for t in tickers if t.get('change_percent', 0) > 0)
        down = sum(1 for t in tickers if t.get('change_percent', 0) < 0)
        neutral = len(tickers) - up - down

        sorted_by_change = sorted(tickers, key=lambda x: x.get('change_percent', 0), reverse=True)
        return {
            'total_scanned': len(tickers),
            'trending_up': up,
            'trending_down': down,
            'neutral': neutral,
            'top_performers': sorted_by_change[:5],
        }

    def _fetch_paprika_tickers(self) -> List[Dict]:
        """Fetch crypto tickers from CoinPaprika (free, no key)."""
        if not self._session:
            return []
        cached = self._get_cached('paprika_tickers')
        if cached:
            return cached
        try:
            resp = self._session.get(
                'https://api.coinpaprika.com/v1/tickers',
                params={'quotes': 'USD'},
                timeout=12,
            )
            if resp.status_code != 200:
                return []
            data = resp.json()
            results = []
            for coin in data[:100]:  # Top 100
                q = coin.get('quotes', {}).get('USD', {})
                results.append({
                    'symbol': coin.get('symbol', ''),
                    'name': coin.get('name', ''),
                    'price': round(q.get('price', 0), 6),
                    'change_percent': round(q.get('percent_change_24h', 0), 2),
                    'volume_24h': round(q.get('volume_24h', 0), 0),
                    'market_cap': round(q.get('market_cap', 0), 0),
                    'market_type': 'crypto',
                    'data_source': 'coinpaprika',
                })
            self._set_cached('paprika_tickers', results)
            return results
        except Exception as e:
            logger.debug(f"CoinPaprika tickers failed: {e}")
            return []

    def _fetch_coincap_tickers(self) -> List[Dict]:
        """Fallback: CoinCap v2 (free, no key)."""
        if not self._session:
            return []
        try:
            resp = self._session.get(
                'https://api.coincap.io/v2/assets',
                params={'limit': 100},
                timeout=10,
            )
            if resp.status_code != 200:
                return []
            results = []
            for coin in resp.json().get('data', []):
                results.append({
                    'symbol': coin.get('symbol', ''),
                    'name': coin.get('name', ''),
                    'price': round(float(coin.get('priceUsd', 0)), 6),
                    'change_percent': round(float(coin.get('changePercent24Hr', 0)), 2),
                    'volume_24h': round(float(coin.get('volumeUsd24Hr', 0)), 0),
                    'market_cap': round(float(coin.get('marketCapUsd', 0)), 0),
                    'market_type': 'crypto',
                    'data_source': 'coincap',
                })
            return results
        except Exception as e:
            logger.debug(f"CoinCap tickers failed: {e}")
            return []

    def _fetch_trending_crypto(self, limit: int) -> List[Dict]:
        """Get top crypto sorted by 24h change."""
        tickers = self._fetch_paprika_tickers()
        if not tickers:
            tickers = self._fetch_coincap_tickers()
        # Sort by absolute change to find most active
        sorted_t = sorted(tickers, key=lambda x: abs(x.get('change_percent', 0)), reverse=True)
        return sorted_t[:limit]

    # ── Stocks (Yahoo Finance chart API) ─────────────────────────────

    def _fetch_stock_overview(self) -> Dict:
        """Fetch live stock data overview."""
        stocks = self._fetch_stock_list(20, sort_by='change')
        up = sum(1 for s in stocks if s.get('change_percent', 0) > 0)
        down = sum(1 for s in stocks if s.get('change_percent', 0) < 0)
        neutral = len(stocks) - up - down

        gainers = sorted(stocks, key=lambda x: x.get('change_percent', 0), reverse=True)[:5]
        losers = sorted(stocks, key=lambda x: x.get('change_percent', 0))[:5]

        return {
            'total_scanned': len(stocks),
            'trending_up': up,
            'trending_down': down,
            'neutral': neutral,
            'top_gainers': gainers,
            'top_losers': losers,
            'most_active': sorted(stocks, key=lambda x: x.get('volume', 0), reverse=True)[:5],
        }

    def _fetch_stock_list(self, count: int, sort_by: str = 'change') -> List[Dict]:
        """Fetch stock prices via Yahoo Finance chart API."""
        if not self._session:
            return []
        cached = self._get_cached(f'stocks_{count}')
        if cached:
            return cached

        results = []
        symbols = _STOCK_SYMBOLS[:count]
        for sym in symbols:
            data = self._fetch_yahoo_quote(sym)
            if data:
                results.append(data)

        if sort_by == 'change':
            results.sort(key=lambda x: abs(x.get('change_percent', 0)), reverse=True)

        self._set_cached(f'stocks_{count}', results)
        return results

    def _fetch_yahoo_quote(self, symbol: str) -> Optional[Dict]:
        """Fetch a single stock quote from Yahoo Finance chart API.
        Falls back to FinancialData.net if Yahoo fails."""
        if not self._session:
            return self._fetch_fdn_stock_quote(symbol)
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
            resp = self._session.get(url, params={
                'interval': '1d', 'range': '5d',
            }, timeout=8)
            if resp.status_code != 200:
                return self._fetch_fdn_stock_quote(symbol)
            data = resp.json().get('chart', {}).get('result', [])
            if not data:
                return self._fetch_fdn_stock_quote(symbol)
            meta = data[0].get('meta', {})
            quote = data[0].get('indicators', {}).get('quote', [{}])[0]
            closes = [c for c in (quote.get('close') or []) if c is not None]
            volumes = [v for v in (quote.get('volume') or []) if v is not None]
            if not closes:
                return None
            current = closes[-1]
            prev = closes[-2] if len(closes) >= 2 else current
            change = current - prev
            change_pct = (change / prev * 100) if prev else 0
            return {
                'symbol': symbol,
                'name': meta.get('shortName', symbol),
                'price': round(current, 2),
                'change': round(change, 2),
                'change_percent': round(change_pct, 2),
                'volume': volumes[-1] if volumes else 0,
                'market_cap': meta.get('marketCap', 'N/A'),
                'market_type': 'stocks',
                'data_source': 'yahoo',
                'timestamp': datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.debug(f"Yahoo quote failed for {symbol}: {e}")
            return self._fetch_fdn_stock_quote(symbol)

    def _fetch_fdn_stock_quote(self, symbol: str) -> Optional[Dict]:
        """Fetch stock quote from FinancialData.net as fallback."""
        if not _fdn or not _fdn.api_key:
            return None
        try:
            prices = _fdn.get_stock_prices(symbol)
            if not prices or len(prices) < 1:
                return None
            latest = prices[0]
            prev = prices[1] if len(prices) >= 2 else latest
            close = latest.get('close', 0)
            prev_close = prev.get('close', close)
            change = round(close - prev_close, 2)
            change_pct = round((change / prev_close * 100) if prev_close else 0, 2)

            # Try to get company name (use long cache to avoid extra calls)
            name = symbol
            info = _fdn._get("/company-information", {"identifier": symbol}, cache_ttl=86400)
            if info and len(info) > 0:
                name = info[0].get('registrant_name', symbol)

            return {
                'symbol': symbol,
                'name': name,
                'price': round(close, 2),
                'change': change,
                'change_percent': change_pct,
                'volume': latest.get('volume', 0),
                'market_cap': 'N/A',
                'market_type': 'stocks',
                'data_source': 'financialdata.net',
                'timestamp': datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.debug(f"FinancialData.net quote failed for {symbol}: {e}")
            return None

    # ── Indices ──────────────────────────────────────────────────────

    def _fetch_indices(self) -> List[Dict]:
        """Fetch major index values from Yahoo Finance."""
        index_map = {
            '^GSPC': 'S&P 500',
            '^DJI': 'Dow Jones',
            '^IXIC': 'NASDAQ',
            '^RUT': 'Russell 2000',
        }
        results = []
        for ticker, name in index_map.items():
            data = self._fetch_yahoo_quote(ticker)
            if data:
                results.append({
                    'name': name,
                    'symbol': ticker.replace('^', ''),
                    'value': data['price'],
                    'change_percent': data['change_percent'],
                    'data_source': 'yahoo',
                })
            else:
                # Fallback with placeholder
                results.append({
                    'name': name,
                    'symbol': ticker.replace('^', ''),
                    'value': 0,
                    'change_percent': 0,
                    'data_source': 'unavailable',
                })
        return results

    # ── Forex (ECB daily rates as free option) ───────────────────────

    def _get_forex_pairs(self, count: int) -> List[Dict]:
        """Get forex pair data. Uses FinancialData.net when available,
        falls back to ECB rates or deterministic jitter."""
        pairs = _FOREX_PAIRS[:count]

        # Try FinancialData.net first for live forex
        if _fdn and _fdn.api_key:
            try:
                fdn_symbols = ','.join(p.replace('/', '') for p in pairs)
                quotes = _fdn.get_forex_quotes(fdn_symbols)
                if quotes and len(quotes) > 0:
                    results = []
                    for q in quotes:
                        sym = q.get('trading_symbol', '')
                        # Convert EURUSD back to EUR/USD
                        pair_fmt = f"{sym[:3]}/{sym[3:]}" if len(sym) == 6 else sym
                        results.append({
                            'pair': pair_fmt,
                            'rate': round(q.get('price', 0), 4),
                            'change_percent': round(q.get('percentage_change', 0), 3),
                            'data_source': 'financialdata.net',
                        })
                    return results
            except Exception as e:
                logger.debug(f"FinancialData.net forex failed: {e}")

        # Fallback: deterministic micro-spread
        base_rates = {
            'EUR/USD': 1.0850, 'GBP/USD': 1.2700, 'USD/JPY': 154.50,
            'USD/CHF': 0.8800, 'AUD/USD': 0.6500, 'USD/CAD': 1.3700,
            'NZD/USD': 0.5950, 'EUR/GBP': 0.8550, 'EUR/JPY': 167.50,
        }
        results = []
        for pair in pairs:
            rate = base_rates.get(pair, 1.0)
            # Deterministic micro-spread from pair name + date
            h = int(hashlib.md5(f"{pair}{datetime.now(timezone.utc).strftime('%Y%m%d')}".encode()).hexdigest()[:8], 16)
            jitter = rate * ((h % 600 - 300) / 100_000)  # ±0.3%
            change_pct = round((h % 1000 - 500) / 1000, 3)  # ±0.5%
            results.append({
                'pair': pair,
                'rate': round(rate + jitter, 4),
                'change_percent': change_pct,
                'data_source': 'estimated',
            })
        return results

    # ── Single symbol scanner ────────────────────────────────────────

    def _scan_symbol(self, symbol: str, market_type: str) -> Dict:
        """Scan a single symbol using real data."""
        sym = symbol.upper()

        # Try real data first
        if market_type == 'crypto':
            data = self._scan_crypto_symbol(sym)
            if data:
                return data
        elif market_type in ('stocks', 'stock'):
            data = self._fetch_yahoo_quote(sym)
            if data:
                data['signals'] = self._compute_signals(data.get('change_percent', 0))
                return data

        # Fallback for unknown types or failures
        return {
            'symbol': sym,
            'name': sym,
            'market_type': market_type,
            'price': 0,
            'change': 0,
            'change_percent': 0,
            'volume': 0,
            'market_cap': 'N/A',
            'signals': {'signal': 'HOLD', 'strength': 'WEAK', 'confidence': 50.0},
            'data_source': 'unavailable',
            'timestamp': datetime.now(timezone.utc).isoformat(),
        }

    def _scan_crypto_symbol(self, symbol: str) -> Optional[Dict]:
        """Get real crypto data for a single symbol."""
        if not self._session:
            return None
        paprika_id = _PAPRIKA_IDS.get(symbol)
        if not paprika_id:
            paprika_id = f"{symbol.lower()}-{symbol.lower()}"
        try:
            resp = self._session.get(
                f'https://api.coinpaprika.com/v1/tickers/{paprika_id}',
                timeout=8,
            )
            if resp.status_code != 200:
                return None
            coin = resp.json()
            q = coin.get('quotes', {}).get('USD', {})
            change_pct = q.get('percent_change_24h', 0)
            return {
                'symbol': coin.get('symbol', symbol),
                'name': coin.get('name', symbol),
                'market_type': 'crypto',
                'price': round(q.get('price', 0), 6),
                'change': round(q.get('price', 0) * change_pct / 100, 2),
                'change_percent': round(change_pct, 2),
                'volume': round(q.get('volume_24h', 0), 0),
                'market_cap': round(q.get('market_cap', 0), 0),
                'signals': self._compute_signals(change_pct),
                'data_source': 'coinpaprika',
                'timestamp': datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            logger.debug(f"Scanner: CoinPaprika failed for {symbol}: {e}")
            return None

    # ── Signal computation (replaces random) ─────────────────────────

    @staticmethod
    def _compute_signals(change_pct: float) -> Dict:
        """Compute trading signals from price change percentage."""
        if change_pct > 5:
            signal, strength = 'BUY', 'STRONG'
        elif change_pct > 2:
            signal, strength = 'BUY', 'MODERATE'
        elif change_pct > 0:
            signal, strength = 'HOLD', 'WEAK'
        elif change_pct > -2:
            signal, strength = 'HOLD', 'MODERATE'
        elif change_pct > -5:
            signal, strength = 'SELL', 'MODERATE'
        else:
            signal, strength = 'SELL', 'STRONG'

        confidence = min(95, 60 + abs(change_pct) * 3)
        return {
            'signal': signal,
            'strength': strength,
            'confidence': round(confidence, 1),
        }

    # ── Caching ──────────────────────────────────────────────────────

    def _get_cached(self, key: str):
        entry = self._cache.get(key)
        if entry and (datetime.now(timezone.utc) - entry['ts']).total_seconds() < self._cache_ttl:
            return entry['data']
        return None

    def _set_cached(self, key: str, data):
        self._cache[key] = {'data': data, 'ts': datetime.now(timezone.utc)}
