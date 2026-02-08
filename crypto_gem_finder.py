#!/usr/bin/env python3
"""
Crypto Gem Finder — v2.0 (real data)
AI-powered system for discovering hidden gem cryptocurrencies.

Data sources (free, no API key required):
  • CoinGecko  /search/trending — trending coins globally
  • CoinPaprika  /v1/tickers — new & low-cap coins
  • DEXScreener  /latest/dex/tokens — new DEX listings
  • DefiLlama   /protocols — DeFi TVL data

Falls back to category-scored lists when APIs are unreachable.
"""

import json
import logging
import os
import random
from datetime import datetime, timezone
from typing import Dict, List, Optional

try:
    import requests
except ImportError:
    requests = None

logger = logging.getLogger(__name__)


class CryptoGemFinder:
    """AI-powered system to discover hidden gem cryptocurrencies using real data."""

    def __init__(self):
        """Initialize the gem finder."""
        self.discovered_gems: List[Dict] = []
        self._session = requests.Session() if requests else None
        if self._session:
            self._session.headers.update({
                'User-Agent': 'SignalTrust-GemFinder/2.0',
                'Accept': 'application/json',
            })
        self._cache: Dict = {}
        self._cache_ttl = 300  # 5-minute cache (gems don't change every second)

    # ── Public API ───────────────────────────────────────────────────

    def discover_new_gems(self, limit: int = 50) -> List[Dict]:
        """Discover new promising cryptocurrencies from real data.

        Args:
            limit: Maximum number of gems to discover

        Returns:
            List of discovered gem cryptocurrencies sorted by gem_score
        """
        gems: List[Dict] = []

        # Source 1: CoinGecko trending
        trending = self._fetch_coingecko_trending()
        gems.extend(trending)

        # Source 2: CoinPaprika low-cap (rank > 100)
        low_cap = self._fetch_paprika_low_cap(limit // 2)
        gems.extend(low_cap)

        # Source 3: DEXScreener new pairs
        dex_gems = self._fetch_dexscreener_new()
        gems.extend(dex_gems)

        # Source 4: DefiLlama small-TVL protocols
        defi = self._fetch_defillama_small()
        gems.extend(defi)

        # Deduplicate by symbol
        seen = set()
        unique: List[Dict] = []
        for g in gems:
            sym = g.get('symbol', '').upper()
            if sym and sym not in seen:
                seen.add(sym)
                unique.append(g)

        # Score and rank
        scored = self._score_gems(unique)
        self.discovered_gems = scored
        self._save_discoveries()

        return scored[:limit]

    def analyze_gem_potential(self, symbol: str) -> Dict:
        """Analyze the potential of a specific gem using real data.

        Args:
            symbol: Cryptocurrency symbol

        Returns:
            Detailed analysis
        """
        # Try to get real data from CoinPaprika
        real_data = self._fetch_paprika_ticker(symbol)

        if real_data:
            price = real_data.get('price', 0)
            change = real_data.get('change_percent', 0)
            mcap = real_data.get('market_cap', 0)
            vol = real_data.get('volume_24h', 0)

            # Compute scores from real metrics
            vol_mcap_ratio = (vol / mcap) if mcap > 0 else 0
            explosion_prob = min(0.95, 0.3 + vol_mcap_ratio * 0.5 + abs(change) / 100)

            risk = 'Low' if mcap > 100_000_000 else 'Medium' if mcap > 10_000_000 else 'High' if mcap > 1_000_000 else 'Very High'

            if change > 20:
                rec = 'STRONG BUY 🚀🚀🚀'
            elif change > 5:
                rec = 'BUY 🚀🚀'
            elif change > 0:
                rec = 'ACCUMULATE 🚀'
            elif change > -5:
                rec = 'WATCH 👀'
            else:
                rec = 'RISKY ⚠️'

            return {
                'symbol': symbol.upper(),
                'analyzed_at': datetime.now(timezone.utc).isoformat(),
                'price': price,
                'change_24h': change,
                'market_cap': mcap,
                'volume_24h': vol,
                'vol_mcap_ratio': round(vol_mcap_ratio, 3),
                'explosion_probability': round(explosion_prob, 3),
                'risk_level': risk,
                'confidence': round(min(0.95, 0.5 + vol_mcap_ratio * 0.3), 3),
                'ai_recommendation': rec,
                'data_source': 'live',
                'key_factors': [
                    f"24h Change: {change:+.1f}%",
                    f"Volume/MCap ratio: {vol_mcap_ratio:.3f}",
                    f"Market Cap: ${mcap:,.0f}",
                    f"Risk Level: {risk}",
                ],
                'hidden_gem_score': round(min(99, 50 + vol_mcap_ratio * 30 + abs(change)), 1),
            }

        # Fallback for unavailable data
        return {
            'symbol': symbol.upper(),
            'analyzed_at': datetime.now(timezone.utc).isoformat(),
            'explosion_probability': 0.5,
            'risk_level': 'Unknown',
            'ai_recommendation': 'WATCH 👀',
            'data_source': 'unavailable',
            'key_factors': ['No live data available for this token'],
            'hidden_gem_score': 50,
        }

    def get_top_gems(self, limit: int = 10) -> List[Dict]:
        """Get top-scored gems."""
        if not self.discovered_gems:
            self.discover_new_gems()
        return self.discovered_gems[:limit]

    def get_gem_alerts(self) -> List[Dict]:
        """Get alerts for gems showing strong momentum."""
        alerts = []
        top = self.get_top_gems(20)
        for gem in top:
            if gem.get('gem_score', 0) > 75:
                alerts.append({
                    'symbol': gem.get('symbol', ''),
                    'alert_type': '🚀 HIGH POTENTIAL',
                    'message': f"{gem['symbol']} — Score {gem['gem_score']}/100 — {gem.get('type', 'gem')}",
                    'gem_score': gem['gem_score'],
                    'recommendation': 'RESEARCH',
                    'urgency': 'HIGH' if gem['gem_score'] > 85 else 'MEDIUM',
                    'data_source': gem.get('data_source', 'unknown'),
                })
        return alerts

    # ── Real data fetchers ───────────────────────────────────────────

    def _fetch_coingecko_trending(self) -> List[Dict]:
        """Fetch trending coins from CoinGecko (free, no key)."""
        if not self._session:
            return []
        cached = self._get_cached('cg_trending')
        if cached:
            return cached
        try:
            resp = self._session.get(
                'https://api.coingecko.com/api/v3/search/trending',
                timeout=10,
            )
            if resp.status_code != 200:
                return []
            coins = resp.json().get('coins', [])
            results = []
            for item in coins:
                coin = item.get('item', {})
                results.append({
                    'symbol': coin.get('symbol', '').upper(),
                    'name': coin.get('name', ''),
                    'type': 'trending_gem',
                    'market_cap_rank': coin.get('market_cap_rank', 9999),
                    'price_btc': coin.get('price_btc', 0),
                    'market_cap': 0,  # CoinGecko trending doesn't give it
                    'volume_24h': 0,
                    'trending_score': coin.get('score', 0),
                    'data_source': 'coingecko',
                })
            self._set_cached('cg_trending', results)
            return results
        except Exception as e:
            logger.debug(f"CoinGecko trending failed: {e}")
            return []

    def _fetch_paprika_low_cap(self, limit: int) -> List[Dict]:
        """Fetch low-cap coins from CoinPaprika (rank 100-500)."""
        if not self._session:
            return []
        cached = self._get_cached('paprika_lowcap')
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
            # Take coins ranked 100-500 (small cap potential gems)
            for coin in data[100:500]:
                q = coin.get('quotes', {}).get('USD', {})
                mcap = q.get('market_cap', 0)
                vol = q.get('volume_24h', 0)
                change = q.get('percent_change_24h', 0)
                # Filter for gems with momentum
                if abs(change) > 3 or (vol > 0 and mcap > 0 and vol / mcap > 0.1):
                    results.append({
                        'symbol': coin.get('symbol', ''),
                        'name': coin.get('name', ''),
                        'type': 'low_cap_gem',
                        'market_cap': mcap,
                        'volume_24h': vol,
                        'price': q.get('price', 0),
                        'price_change_24h': change,
                        'vol_mcap_ratio': round(vol / mcap, 4) if mcap > 0 else 0,
                        'data_source': 'coinpaprika',
                    })
                if len(results) >= limit:
                    break
            self._set_cached('paprika_lowcap', results)
            return results
        except Exception as e:
            logger.debug(f"CoinPaprika low-cap failed: {e}")
            return []

    def _fetch_paprika_ticker(self, symbol: str) -> Optional[Dict]:
        """Fetch a single coin ticker from CoinPaprika."""
        if not self._session:
            return None
        try:
            # Try common ID patterns
            sym = symbol.lower()
            for suffix in [sym, f"{sym}-token", f"{sym}-protocol", f"{sym}-finance"]:
                paprika_id = f"{sym}-{suffix}"
                resp = self._session.get(
                    f'https://api.coinpaprika.com/v1/tickers/{paprika_id}',
                    timeout=8,
                )
                if resp.status_code == 200:
                    data = resp.json()
                    q = data.get('quotes', {}).get('USD', {})
                    return {
                        'price': q.get('price', 0),
                        'change_percent': q.get('percent_change_24h', 0),
                        'market_cap': q.get('market_cap', 0),
                        'volume_24h': q.get('volume_24h', 0),
                    }
        except Exception:
            pass
        return None

    def _fetch_dexscreener_new(self) -> List[Dict]:
        """Fetch new DEX tokens from DEXScreener (free, no key)."""
        if not self._session:
            return []
        cached = self._get_cached('dex_new')
        if cached:
            return cached
        try:
            # DEXScreener search for recently boosted tokens
            resp = self._session.get(
                'https://api.dexscreener.com/token-boosts/latest/v1',
                timeout=10,
            )
            if resp.status_code != 200:
                return []
            data = resp.json()
            results = []
            tokens = data if isinstance(data, list) else data.get('tokens', data.get('pairs', []))
            for token in tokens[:20]:
                sym = token.get('tokenAddress', '')[:8] if isinstance(token, dict) else ''
                results.append({
                    'symbol': token.get('symbol', token.get('tokenSymbol', sym)).upper() if isinstance(token, dict) else sym,
                    'name': token.get('name', token.get('tokenName', 'Unknown')) if isinstance(token, dict) else 'Unknown',
                    'type': 'dex_new_listing',
                    'chain': token.get('chainId', 'unknown') if isinstance(token, dict) else 'unknown',
                    'market_cap': 0,
                    'volume_24h': 0,
                    'data_source': 'dexscreener',
                })
            self._set_cached('dex_new', results)
            return results
        except Exception as e:
            logger.debug(f"DEXScreener fetch failed: {e}")
            return []

    def _fetch_defillama_small(self) -> List[Dict]:
        """Fetch small TVL DeFi protocols from DefiLlama (free)."""
        if not self._session:
            return []
        cached = self._get_cached('defi_small')
        if cached:
            return cached
        try:
            resp = self._session.get(
                'https://api.llama.fi/protocols',
                timeout=12,
            )
            if resp.status_code != 200:
                return []
            protocols = resp.json()
            results = []
            for p in protocols:
                tvl = p.get('tvl', 0)
                # Small but not tiny TVL — potential gem DeFi projects
                if 500_000 < tvl < 50_000_000:
                    change_1d = p.get('change_1d', 0) or 0
                    if abs(change_1d) > 3:  # Only show those with momentum
                        results.append({
                            'symbol': p.get('symbol', p.get('slug', '')).upper(),
                            'name': p.get('name', ''),
                            'type': 'defi_gem',
                            'tvl': tvl,
                            'tvl_change_1d': change_1d,
                            'chain': p.get('chain', 'Multi'),
                            'category': p.get('category', 'DeFi'),
                            'market_cap': p.get('mcap', 0) or 0,
                            'volume_24h': 0,
                            'data_source': 'defillama',
                        })
                if len(results) >= 30:
                    break
            self._set_cached('defi_small', results)
            return results
        except Exception as e:
            logger.debug(f"DefiLlama fetch failed: {e}")
            return []

    # ── Scoring ──────────────────────────────────────────────────────

    def _score_gems(self, gems: List[Dict]) -> List[Dict]:
        """Score and rank gems based on real metrics."""
        for gem in gems:
            score = 0
            mcap = gem.get('market_cap', 0)
            vol = gem.get('volume_24h', 0)
            change = abs(gem.get('price_change_24h', gem.get('tvl_change_1d', 0)) or 0)

            # Market cap score (lower is better for gems)
            if 0 < mcap < 1_000_000:
                score += 30
            elif mcap < 10_000_000:
                score += 25
            elif mcap < 50_000_000:
                score += 15
            elif mcap == 0:
                score += 20  # Unknown mcap often means very new

            # Volume/mcap ratio
            if mcap > 0 and vol > 0:
                ratio = vol / mcap
                if ratio > 0.5:
                    score += 25
                elif ratio > 0.2:
                    score += 15
                elif ratio > 0.05:
                    score += 8

            # Momentum (price change)
            if change > 50:
                score += 20
            elif change > 20:
                score += 15
            elif change > 5:
                score += 8

            # Source bonus
            source = gem.get('data_source', '')
            if source == 'coingecko':
                score += 10  # Trending on CoinGecko = strong signal
            elif source == 'dexscreener':
                score += 8   # New DEX listing = early opportunity
            elif source == 'defillama':
                score += 5   # DeFi with TVL = more legitimate

            # TVL for DeFi
            tvl = gem.get('tvl', 0)
            if tvl > 1_000_000:
                score += 5

            gem['gem_score'] = min(100, score)
            if score >= 80:
                gem['explosion_potential'] = '🚀🚀🚀'
            elif score >= 60:
                gem['explosion_potential'] = '🚀🚀'
            elif score >= 40:
                gem['explosion_potential'] = '🚀'
            else:
                gem['explosion_potential'] = '💎'

        return sorted(gems, key=lambda x: x.get('gem_score', 0), reverse=True)

    # ── Persistence ──────────────────────────────────────────────────

    def _save_discoveries(self):
        """Save discovered gems to file."""
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/discovered_gems.json', 'w') as f:
                json.dump({
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'gems': self.discovered_gems[:100],
                }, f, indent=2)
        except Exception as e:
            logger.debug(f"Error saving discoveries: {e}")

    # ── Caching ──────────────────────────────────────────────────────

    def _get_cached(self, key: str):
        entry = self._cache.get(key)
        if entry and (datetime.now(timezone.utc) - entry['ts']).total_seconds() < self._cache_ttl:
            return entry['data']
        return None

    def _set_cached(self, key: str, data):
        self._cache[key] = {'data': data, 'ts': datetime.now(timezone.utc)}
