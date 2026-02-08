"""
FinancialData.net API Provider for SignalTrust AI Scanner.

Comprehensive financial data integration covering:
- Stock prices (US & international), quotes, historical OHLCV
- Crypto prices, quotes, symbols, info
- Commodity prices & symbols
- Market indexes (S&P 500, Dow Jones, NASDAQ, etc.)
- Company fundamentals (income statements, balance sheets, ratios)
- Earnings releases, dividends, stock splits
- Short interest, insider trading
- ETF data, OTC data
- Forex data

API Docs: https://financialdata.net/documentation
Auth: ?key=API_KEY appended to all requests
"""

import os
import time
import logging
import requests
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

# ─── Base URL ────────────────────────────────────────────────────────
BASE_URL = "https://financialdata.net/api/v1"


class FinancialDataProvider:
    """Client for FinancialData.net REST API."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the FinancialData.net provider.

        Args:
            api_key: API key (falls back to FINANCIAL_DATA_API_KEY env var)
        """
        self.api_key = api_key or os.environ.get("FINANCIAL_DATA_API_KEY", "")
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/json",
            "User-Agent": "SignalTrust-AI-Scanner/2.0"
        })
        # Simple in-memory cache: key → (timestamp, data)
        self._cache: Dict[str, tuple] = {}
        self._cache_ttl = 120  # seconds

    # ── helpers ──────────────────────────────────────────────────────

    def _get(self, endpoint: str, params: Optional[Dict] = None,
             cache_ttl: Optional[int] = None) -> Optional[Any]:
        """Make authenticated GET request with caching.

        Args:
            endpoint: API path (e.g. "/stock-prices")
            params:   Extra query params
            cache_ttl: Override cache TTL for this call
        Returns:
            Parsed JSON or None on error
        """
        if not self.api_key:
            logger.warning("FinancialDataProvider: no API key configured")
            return None

        ttl = cache_ttl if cache_ttl is not None else self._cache_ttl
        cache_key = f"{endpoint}|{params}"
        cached = self._cache.get(cache_key)
        if cached and (time.time() - cached[0]) < ttl:
            return cached[1]

        url = f"{BASE_URL}{endpoint}"
        query = dict(params or {})
        query["key"] = self.api_key

        try:
            resp = self._session.get(url, params=query, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                self._cache[cache_key] = (time.time(), data)
                return data
            else:
                logger.warning(
                    "FinancialData API %s returned %s: %s",
                    endpoint, resp.status_code, resp.text[:200]
                )
                return None
        except requests.RequestException as e:
            logger.error("FinancialData API error on %s: %s", endpoint, e)
            return None

    # ═══════════════════════════════════════════════════════════════════
    #  STOCK DATA
    # ═══════════════════════════════════════════════════════════════════

    def get_stock_symbols(self, offset: int = 0) -> Optional[List[Dict]]:
        """Get list of US stock symbols (FREE). Limit 500/call."""
        return self._get("/stock-symbols", {"offset": offset})

    def get_international_stock_symbols(self, offset: int = 0) -> Optional[List[Dict]]:
        """Get international stock symbols (FREE). Limit 500/call."""
        return self._get("/international-stock-symbols", {"offset": offset})

    def get_stock_prices(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get 10+ years daily historical prices (FREE). Limit 300/call.

        Returns list of {trading_symbol, date, open, high, low, close, volume}.
        """
        return self._get("/stock-prices", {"identifier": symbol, "offset": offset})

    def get_stock_quotes(self, symbols: str) -> Optional[List[Dict]]:
        """Get real-time stock quotes (PREMIUM). Comma-separated symbols.

        Returns {trading_symbol, registrant_name, time, price, change, percentage_change}.
        """
        return self._get("/stock-quotes", {"identifiers": symbols}, cache_ttl=30)

    def get_commodity_symbols(self) -> Optional[List[Dict]]:
        """Get commodity trading symbols (FREE)."""
        return self._get("/commodity-symbols")

    def get_commodity_prices(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get 10+ years daily commodity prices (FREE). Limit 300/call."""
        return self._get("/commodity-prices", {"identifier": symbol, "offset": offset})

    def get_otc_prices(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get 10+ years daily OTC prices (FREE). Limit 300/call."""
        return self._get("/otc-prices", {"identifier": symbol, "offset": offset})

    # ═══════════════════════════════════════════════════════════════════
    #  MARKET INDEXES
    # ═══════════════════════════════════════════════════════════════════

    def get_index_symbols(self) -> Optional[List[Dict]]:
        """Get list of major market index symbols (STANDARD)."""
        return self._get("/index-symbols")

    def get_index_quotes(self, symbols: str) -> Optional[List[Dict]]:
        """Get real-time index quotes (PREMIUM). e.g. "^GSPC,^DJI"."""
        return self._get("/index-quotes", {"identifiers": symbols}, cache_ttl=30)

    def get_index_prices(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get 10+ years daily index prices (STANDARD). Limit 300/call."""
        return self._get("/index-prices", {"identifier": symbol, "offset": offset})

    def get_index_constituents(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get constituents of an index (STANDARD). e.g. ^GSPC for S&P 500."""
        return self._get("/index-constituents", {"identifier": symbol, "offset": offset})

    # ═══════════════════════════════════════════════════════════════════
    #  CRYPTO DATA
    # ═══════════════════════════════════════════════════════════════════

    def get_crypto_symbols(self, offset: int = 0) -> Optional[List[Dict]]:
        """Get crypto pair symbols (STANDARD). Limit 500/call."""
        return self._get("/crypto-symbols", {"offset": offset})

    def get_crypto_info(self, symbol: str) -> Optional[List[Dict]]:
        """Get crypto info: market cap, supply, description (STANDARD)."""
        return self._get("/crypto-information", {"identifier": symbol})

    def get_crypto_quotes(self, symbols: str) -> Optional[List[Dict]]:
        """Get real-time crypto quotes (PREMIUM). e.g. "BTCUSD,ETHUSD"."""
        return self._get("/crypto-quotes", {"identifiers": symbols}, cache_ttl=30)

    def get_crypto_prices(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get daily historical crypto prices (STANDARD). Limit 300/call."""
        return self._get("/crypto-prices", {"identifier": symbol, "offset": offset})

    def get_crypto_minute_prices(self, symbol: str, date: str,
                                  offset: int = 0) -> Optional[List[Dict]]:
        """Get 1-min crypto prices for a date (STANDARD). Limit 300/call."""
        return self._get("/crypto-minute-prices", {
            "identifier": symbol, "date": date, "offset": offset
        })

    # ═══════════════════════════════════════════════════════════════════
    #  FOREX DATA
    # ═══════════════════════════════════════════════════════════════════

    def get_forex_symbols(self) -> Optional[List[Dict]]:
        """Get forex currency pair symbols (PREMIUM)."""
        return self._get("/forex-symbols")

    def get_forex_quotes(self, symbols: str) -> Optional[List[Dict]]:
        """Get real-time forex quotes (PREMIUM). e.g. "EURUSD,GBPUSD"."""
        return self._get("/forex-quotes", {"identifiers": symbols}, cache_ttl=30)

    def get_forex_prices(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get daily historical forex prices (PREMIUM). Limit 300/call."""
        return self._get("/forex-prices", {"identifier": symbol, "offset": offset})

    # ═══════════════════════════════════════════════════════════════════
    #  COMPANY FUNDAMENTALS
    # ═══════════════════════════════════════════════════════════════════

    def get_company_info(self, symbol: str) -> Optional[List[Dict]]:
        """Get company information: industry, CEO, employees, etc (STANDARD)."""
        return self._get("/company-information", {"identifier": symbol}, cache_ttl=3600)

    def get_key_metrics(self, symbol: str) -> Optional[List[Dict]]:
        """Get P/E ratio, EPS, free cash flow, beta, etc (STANDARD)."""
        return self._get("/key-metrics", {"identifier": symbol}, cache_ttl=3600)

    def get_market_cap(self, symbol: str) -> Optional[List[Dict]]:
        """Get historical market cap data (STANDARD)."""
        return self._get("/market-cap", {"identifier": symbol}, cache_ttl=3600)

    def get_income_statements(self, symbol: str,
                               period: str = "year") -> Optional[List[Dict]]:
        """Get income statements (STANDARD). period: 'year' or 'quarter'."""
        return self._get("/income-statements", {
            "identifier": symbol, "period": period
        }, cache_ttl=3600)

    def get_balance_sheet(self, symbol: str,
                          period: str = "year") -> Optional[List[Dict]]:
        """Get balance sheet statements (STANDARD)."""
        return self._get("/balance-sheet-statements", {
            "identifier": symbol, "period": period
        }, cache_ttl=3600)

    def get_cash_flow(self, symbol: str,
                      period: str = "year") -> Optional[List[Dict]]:
        """Get cash flow statements (STANDARD)."""
        return self._get("/cash-flow-statements", {
            "identifier": symbol, "period": period
        }, cache_ttl=3600)

    # ═══════════════════════════════════════════════════════════════════
    #  FINANCIAL RATIOS
    # ═══════════════════════════════════════════════════════════════════

    def get_liquidity_ratios(self, symbol: str,
                              period: str = "year") -> Optional[List[Dict]]:
        """Get liquidity ratios (STANDARD)."""
        return self._get("/liquidity-ratios", {
            "identifier": symbol, "period": period
        }, cache_ttl=3600)

    def get_profitability_ratios(self, symbol: str,
                                  period: str = "year") -> Optional[List[Dict]]:
        """Get profitability ratios: profit margin, ROE, ROA (STANDARD)."""
        return self._get("/profitability-ratios", {
            "identifier": symbol, "period": period
        }, cache_ttl=3600)

    def get_solvency_ratios(self, symbol: str,
                             period: str = "year") -> Optional[List[Dict]]:
        """Get solvency ratios (STANDARD)."""
        return self._get("/solvency-ratios", {
            "identifier": symbol, "period": period
        }, cache_ttl=3600)

    def get_efficiency_ratios(self, symbol: str,
                               period: str = "year") -> Optional[List[Dict]]:
        """Get efficiency ratios (STANDARD)."""
        return self._get("/efficiency-ratios", {
            "identifier": symbol, "period": period
        }, cache_ttl=3600)

    def get_valuation_ratios(self, symbol: str,
                              period: str = "year") -> Optional[List[Dict]]:
        """Get valuation ratios: dividends/share, book value (STANDARD)."""
        return self._get("/valuation-ratios", {
            "identifier": symbol, "period": period
        }, cache_ttl=3600)

    # ═══════════════════════════════════════════════════════════════════
    #  EVENTS & CALENDARS
    # ═══════════════════════════════════════════════════════════════════

    def get_earnings_releases(self, symbol: str) -> Optional[List[Dict]]:
        """Get historical earnings releases for a company (STANDARD)."""
        return self._get("/earnings-releases", {"identifier": symbol}, cache_ttl=3600)

    def get_dividends(self, symbol: str) -> Optional[List[Dict]]:
        """Get dividend history for a company (STANDARD)."""
        return self._get("/dividends", {"identifier": symbol}, cache_ttl=3600)

    def get_stock_splits(self, symbol: str) -> Optional[List[Dict]]:
        """Get stock split history (STANDARD)."""
        return self._get("/stock-splits", {"identifier": symbol}, cache_ttl=3600)

    def get_short_interest(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get short interest data (STANDARD). Limit 100/call."""
        return self._get("/short-interest", {"identifier": symbol, "offset": offset})

    def get_initial_public_offerings(self, symbol: str) -> Optional[List[Dict]]:
        """Get IPO data for a company (STANDARD)."""
        return self._get("/initial-public-offerings", {"identifier": symbol}, cache_ttl=3600)

    # ═══════════════════════════════════════════════════════════════════
    #  OPTIONS & DERIVATIVES
    # ═══════════════════════════════════════════════════════════════════

    def get_option_chain(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get option chain: puts & calls with strikes/expirations (STANDARD)."""
        return self._get("/option-chain", {"identifier": symbol, "offset": offset})

    def get_futures_symbols(self, offset: int = 0) -> Optional[List[Dict]]:
        """Get futures trading symbols (STANDARD). Limit 500/call."""
        return self._get("/futures-symbols", {"offset": offset})

    def get_futures_prices(self, symbol: str, offset: int = 0) -> Optional[List[Dict]]:
        """Get 10+ years daily futures prices (STANDARD). Limit 300/call."""
        return self._get("/futures-prices", {"identifier": symbol, "offset": offset})

    # ═══════════════════════════════════════════════════════════════════
    #  ETF DATA
    # ═══════════════════════════════════════════════════════════════════

    def get_etf_symbols(self, offset: int = 0) -> Optional[List[Dict]]:
        """Get ETF trading symbols (FREE). Limit 500/call."""
        return self._get("/etf-symbols", {"offset": offset})

    # ═══════════════════════════════════════════════════════════════════
    #  HIGH-LEVEL CONVENIENCE METHODS
    # ═══════════════════════════════════════════════════════════════════

    def get_stock_overview(self, symbol: str) -> Dict:
        """Get a comprehensive stock overview combining price + fundamentals.

        Returns:
            Combined dict with price data, company info, and key metrics.
        """
        result: Dict[str, Any] = {
            "success": False,
            "symbol": symbol,
            "source": "financialdata.net"
        }

        # 1. Latest prices (last 5 days)
        prices = self.get_stock_prices(symbol)
        if prices and len(prices) > 0:
            latest = prices[0]
            result["price"] = latest.get("close", 0)
            result["open"] = latest.get("open", 0)
            result["high"] = latest.get("high", 0)
            result["low"] = latest.get("low", 0)
            result["volume"] = latest.get("volume", 0)
            result["date"] = latest.get("date", "")

            if len(prices) >= 2:
                prev_close = prices[1].get("close", 0)
                if prev_close > 0:
                    change = result["price"] - prev_close
                    change_pct = (change / prev_close) * 100
                    result["change"] = round(change, 2)
                    result["change_percent"] = round(change_pct, 2)

            result["success"] = True

        # 2. Company info
        info = self.get_company_info(symbol)
        if info and len(info) > 0:
            company = info[0]
            result["company_name"] = company.get("registrant_name", "")
            result["industry"] = company.get("industry", "")
            result["sector"] = company.get("sic_description", "")
            result["exchange"] = company.get("exchange", "")
            result["ceo"] = company.get("chief_executive_officer", "")
            result["employees"] = company.get("number_of_employees", 0)
            result["market_cap"] = company.get("market_cap", 0)
            result["website"] = company.get("website", "")
            result["description"] = company.get("description", "")

        # 3. Key metrics
        metrics = self.get_key_metrics(symbol)
        if metrics and len(metrics) > 0:
            m = metrics[0]
            result["metrics"] = {
                "pe_ratio": m.get("price_to_earnings_ratio"),
                "forward_pe": m.get("forward_price_to_earnings_ratio"),
                "eps": m.get("earnings_per_share"),
                "eps_forecast": m.get("earnings_per_share_forecast"),
                "earnings_growth": m.get("earnings_growth_rate"),
                "peg_ratio": m.get("price_earnings_to_growth_ratio"),
                "pb_ratio": m.get("price_to_book_ratio"),
                "book_value": m.get("book_value_per_share"),
                "dividend_yield": m.get("dividend_yield"),
                "dividend_payout": m.get("dividend_payout_ratio"),
                "debt_to_equity": m.get("debt_to_equity_ratio"),
                "free_cash_flow": m.get("free_cash_flow"),
                "ebitda": m.get("ebitda"),
                "enterprise_value": m.get("enterprise_value"),
                "beta_1y": m.get("one_year_beta"),
                "beta_5y": m.get("five_year_beta"),
                "capex": m.get("capital_expenditures"),
                "roe": m.get("return_on_equity"),
            }

        return result

    def get_crypto_overview(self, symbol: str) -> Dict:
        """Get comprehensive crypto overview.

        Args:
            symbol: Base crypto symbol like "BTC" or pair like "BTCUSD"

        Returns:
            Combined dict with price data and crypto info.
        """
        result: Dict[str, Any] = {
            "success": False,
            "symbol": symbol,
            "source": "financialdata.net"
        }

        # Normalize: if just "BTC", make it "BTCUSD" for price endpoint
        pair = symbol.upper() if "USD" in symbol.upper() else f"{symbol.upper()}USD"
        base = symbol.upper().replace("USD", "").replace("USDT", "")

        # 1. Prices
        prices = self.get_crypto_prices(pair)
        if prices and len(prices) > 0:
            latest = prices[0]
            result["price"] = latest.get("close", 0)
            result["open"] = latest.get("open", 0)
            result["high"] = latest.get("high", 0)
            result["low"] = latest.get("low", 0)
            result["volume"] = latest.get("volume", 0)
            result["date"] = latest.get("date", "")

            if len(prices) >= 2:
                prev = prices[1].get("close", 0)
                if prev > 0:
                    change = result["price"] - prev
                    result["change"] = round(change, 2)
                    result["change_percent"] = round((change / prev) * 100, 2)

            result["success"] = True

        # 2. Crypto info
        info = self.get_crypto_info(base)
        if info and len(info) > 0:
            c = info[0]
            result["crypto_name"] = c.get("crypto_name", "")
            result["market_cap"] = c.get("market_cap", 0)
            result["total_supply"] = c.get("total_supply", 0)
            result["max_supply"] = c.get("max_supply", 0)
            result["circulating_supply"] = c.get("circulating_supply", 0)
            result["ath"] = c.get("highest_price", 0)
            result["ath_date"] = c.get("highest_price_date", "")
            result["atl"] = c.get("lowest_price", 0)
            result["hash_function"] = c.get("hash_function", "")
            result["block_time"] = c.get("block_time", "")
            result["website"] = c.get("website", "")
            result["description"] = c.get("description", "")

        return result

    def get_historical_ohlcv(self, symbol: str, market_type: str = "stock",
                              limit: int = 300) -> List[Dict]:
        """Get historical OHLCV data for technical analysis.

        Args:
            symbol:      Trading symbol
            market_type: "stock", "crypto", "commodity", "index", "etf", "futures"
            limit:       Max records (up to 300 per call)

        Returns:
            List of {date, open, high, low, close, volume} dicts,
            newest first.
        """
        endpoint_map = {
            "stock": "/stock-prices",
            "crypto": "/crypto-prices",
            "commodity": "/commodity-prices",
            "index": "/index-prices",
            "etf": "/etf-prices",
            "futures": "/futures-prices",
            "otc": "/otc-prices",
        }
        endpoint = endpoint_map.get(market_type, "/stock-prices")

        # For crypto, ensure pair format
        if market_type == "crypto" and "USD" not in symbol.upper():
            symbol = f"{symbol}USD"

        data = self._get(endpoint, {"identifier": symbol, "offset": 0})
        if data and isinstance(data, list):
            return data[:limit]
        return []

    def get_fundamental_analysis(self, symbol: str) -> Dict:
        """Get comprehensive fundamental analysis for AI-powered insights.

        Returns:
            Dict with income_statement, balance_sheet, cash_flow,
            ratios (profitability, liquidity, solvency, efficiency, valuation),
            key_metrics, earnings, dividends, short_interest.
        """
        result: Dict[str, Any] = {
            "success": False,
            "symbol": symbol,
            "source": "financialdata.net"
        }

        # Income statement
        income = self.get_income_statements(symbol, "year")
        if income:
            result["income_statement"] = income[0] if income else None
            result["success"] = True

        # Balance sheet
        balance = self.get_balance_sheet(symbol, "year")
        if balance:
            result["balance_sheet"] = balance[0] if balance else None

        # Cash flow
        cashflow = self.get_cash_flow(symbol, "year")
        if cashflow:
            result["cash_flow"] = cashflow[0] if cashflow else None

        # Profitability
        prof = self.get_profitability_ratios(symbol)
        if prof:
            result["profitability"] = prof[0] if prof else None

        # Liquidity
        liq = self.get_liquidity_ratios(symbol)
        if liq:
            result["liquidity"] = liq[0] if liq else None

        # Earnings
        earnings = self.get_earnings_releases(symbol)
        if earnings:
            result["earnings_history"] = earnings[:4]  # Last 4 quarters

        # Dividends
        divs = self.get_dividends(symbol)
        if divs:
            result["dividends"] = divs[:4]  # Last 4

        # Short interest
        short = self.get_short_interest(symbol)
        if short:
            result["short_interest"] = short[0] if short else None

        return result

    def search_symbols(self, query: str) -> List[Dict]:
        """Search across stocks, ETFs, crypto for a symbol.

        Args:
            query: Symbol or partial name to search

        Returns:
            List of matching symbols with type info.
        """
        results = []
        query_upper = query.upper()

        # Search stocks
        stocks = self.get_stock_symbols()
        if stocks:
            for s in stocks:
                sym = s.get("trading_symbol", "")
                name = s.get("registrant_name", "")
                if query_upper in sym.upper() or query_upper in name.upper():
                    results.append({
                        "symbol": sym,
                        "name": name,
                        "type": "stock",
                        "source": "financialdata.net"
                    })
                if len(results) >= 20:
                    break

        # Search ETFs
        if len(results) < 20:
            etfs = self.get_etf_symbols()
            if etfs:
                for e in etfs:
                    sym = e.get("trading_symbol", "")
                    desc = e.get("description", "")
                    if query_upper in sym.upper() or query_upper in desc.upper():
                        results.append({
                            "symbol": sym,
                            "name": desc,
                            "type": "etf",
                            "source": "financialdata.net"
                        })
                    if len(results) >= 20:
                        break

        return results[:20]

    def is_available(self) -> bool:
        """Check if the API key is configured and working."""
        if not self.api_key:
            return False
        test = self._get("/stock-symbols", {"offset": 0})
        return test is not None and len(test) > 0

    def get_status(self) -> Dict:
        """Get provider status info."""
        return {
            "provider": "financialdata.net",
            "api_key_set": bool(self.api_key),
            "api_key_preview": f"{self.api_key[:8]}..." if self.api_key else "",
            "base_url": BASE_URL,
            "cache_size": len(self._cache),
            "features": [
                "stock_prices", "stock_quotes", "crypto_prices", "crypto_info",
                "forex_quotes", "commodity_prices", "index_prices",
                "company_info", "key_metrics", "financial_statements",
                "ratios", "earnings", "dividends", "short_interest",
                "option_chain", "futures", "etf_data"
            ]
        }


# ── Module-level singleton ───────────────────────────────────────────
financial_data = FinancialDataProvider()
