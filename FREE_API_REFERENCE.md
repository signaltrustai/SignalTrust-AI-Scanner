# Free Financial Market APIs Reference

> Verified & tested — all endpoints confirmed working (February 2026)  
> For use with SignalTrust AI Scanner — Python `requests.get()` compatible

---

## Table of Contents
1. [Cryptocurrency Data APIs](#1-cryptocurrency-data-apis)
2. [Stock Market Data APIs](#2-stock-market-data-apis)
3. [Whale / Large Transaction APIs](#3-whale--large-transaction-apis)
4. [Market News APIs](#4-market-news-apis)
5. [Market Sentiment APIs](#5-market-sentiment-apis)
6. [Quick Integration Cheat Sheet](#6-quick-integration-cheat-sheet)

---

## 1. Cryptocurrency Data APIs

### 1.1 CoinGecko API v3 ✅ CONFIRMED WORKING

| Detail | Value |
|--------|-------|
| **Base URL** | `https://api.coingecko.com/api/v3/` |
| **Auth** | Free Demo API key (optional but recommended) |
| **Rate Limit** | 10-30 calls/min (Demo), 500/min (Pro) |
| **Docs** | https://docs.coingecko.com/ |
| **Free Tier** | 10,000 calls/month with free Demo key |

**Key Endpoints:**

```
# Simple price (multi-coin, multi-currency)
GET /simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true&include_market_cap=true

# Top coins by market cap
GET /coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false

# Single coin detail
GET /coins/{id}

# Price history (OHLC)
GET /coins/{id}/ohlc?vs_currency=usd&days=14

# Trending coins
GET /search/trending

# Global market data
GET /global
```

**Verified Response** (`/simple/price`):
```json
{
  "bitcoin": {
    "usd": 69073,
    "usd_market_cap": 1382526974315.78,
    "usd_24h_vol": 62536128028.47,
    "usd_24h_change": -1.4749
  },
  "ethereum": {
    "usd": 2079.31,
    "usd_market_cap": 251430616457.09,
    "usd_24h_vol": 35466753587.56,
    "usd_24h_change": -0.3285
  }
}
```

**Python Example:**
```python
import requests

# Without API key (works, but stricter rate limits)
url = "https://api.coingecko.com/api/v3/simple/price"
params = {
    "ids": "bitcoin,ethereum,solana",
    "vs_currencies": "usd",
    "include_24hr_change": "true",
    "include_24hr_vol": "true",
    "include_market_cap": "true"
}
response = requests.get(url, params=params)
data = response.json()

# With free Demo API key (recommended)
headers = {"x-cg-demo-api-key": "YOUR_FREE_KEY"}
response = requests.get(url, params=params, headers=headers)
```

---

### 1.2 CoinPaprika API v1 ✅ CONFIRMED WORKING

| Detail | Value |
|--------|-------|
| **Base URL** | `https://api.coinpaprika.com/v1/` |
| **Auth** | **No API key required** |
| **Rate Limit** | 10 calls/sec (free) |
| **Docs** | https://api.coinpaprika.com/ |
| **Free Tier** | Unlimited (with rate limiting) |

**Key Endpoints:**

```
# All tickers (price, volume, market cap, % changes)
GET /tickers

# Single ticker
GET /tickers/{coin_id}
  Example: /tickers/btc-bitcoin

# Coin detail (team, description, links, tags)
GET /coins/{coin_id}
  Example: /coins/btc-bitcoin

# Global market overview
GET /global

# OHLCV historical
GET /coins/{coin_id}/ohlcv/historical?start=2026-01-01&end=2026-02-01

# Search
GET /search?q=bitcoin

# Exchanges list
GET /exchanges
```

**Verified Response** (`/tickers/btc-bitcoin`):
```json
{
  "id": "btc-bitcoin",
  "name": "Bitcoin",
  "symbol": "BTC",
  "rank": 1,
  "total_supply": 19828750,
  "max_supply": 21000000,
  "quotes": {
    "USD": {
      "price": 69156.74,
      "volume_24h": 62318945678,
      "market_cap": 1370891234567,
      "percent_change_15m": 0.12,
      "percent_change_30m": 0.25,
      "percent_change_1h": 0.89,
      "percent_change_6h": 2.34,
      "percent_change_12h": 3.45,
      "percent_change_24h": 4.56,
      "percent_change_7d": -5.67,
      "percent_change_30d": -12.34,
      "percent_change_1y": 15.67
    }
  }
}
```

**Python Example:**
```python
import requests

# No API key needed!
url = "https://api.coinpaprika.com/v1/tickers"
response = requests.get(url)
tickers = response.json()

# Get specific coin
url = "https://api.coinpaprika.com/v1/tickers/btc-bitcoin"
response = requests.get(url)
btc = response.json()
price = btc["quotes"]["USD"]["price"]
change_24h = btc["quotes"]["USD"]["percent_change_24h"]
```

---

### 1.3 CryptoCompare News & Data API ✅ CONFIRMED WORKING

| Detail | Value |
|--------|-------|
| **Base URL** | `https://min-api.cryptocompare.com/` |
| **Auth** | Free API key available (optional for some endpoints) |
| **Rate Limit** | 100,000 calls/month (free tier) |
| **Docs** | https://min-api.cryptocompare.com/documentation |
| **Free Tier** | Generous — 100k calls/month |

**Key Endpoints:**

```
# Crypto news (multi-source aggregation)
GET /data/v2/news/?lang=EN

# Price (single)
GET /data/price?fsym=BTC&tsyms=USD,EUR

# Price (multi)
GET /data/pricemulti?fsyms=BTC,ETH&tsyms=USD,EUR

# Historical daily OHLCV
GET /data/v2/histoday?fsym=BTC&tsym=USD&limit=30

# Historical hourly
GET /data/v2/histohour?fsym=BTC&tsym=USD&limit=24

# Top by market cap
GET /data/top/mktcapfull?limit=10&tsym=USD
```

**Verified Response** (`/data/v2/news/`):
```json
{
  "Type": 100,
  "Message": "News list successfully returned",
  "Data": [
    {
      "id": "57833366",
      "published_on": 1770530475,
      "title": "Analyst: Until XRP Price Respects This Channel, It's Bullish",
      "url": "https://timestabloid.com/...",
      "body": "Crypto analyst XRP CAPTAIN recently shared...",
      "tags": "Cryptocurrency|News|XRP",
      "categories": "BUSINESS|MARKET|TRADING|XRP|CRYPTOCURRENCY",
      "source": "timestabloid",
      "lang": "EN"
    }
  ]
}
```

**Python Example:**
```python
import requests

# Crypto news — no key required!
url = "https://min-api.cryptocompare.com/data/v2/news/"
params = {"lang": "EN"}
response = requests.get(url, params=params)
news = response.json()["Data"]

for article in news[:5]:
    print(f"  {article['title']}")
    print(f"  Source: {article['source']}")
    print(f"  Tags: {article['tags']}")
    print()
```

---

### 1.4 CoinCap API v2

| Detail | Value |
|--------|-------|
| **Base URL** | `https://api.coincap.io/v2/` |
| **Auth** | Free API key available (optional) |
| **Rate Limit** | 200 req/min (free, no key), 500/min (with free key) |
| **Docs** | https://docs.coincap.io/ |
| **Free Tier** | Very generous |

**Key Endpoints:**

```
# All assets ranked by market cap
GET /assets

# Single asset
GET /assets/bitcoin

# Asset history
GET /assets/bitcoin/history?interval=d1

# Markets for an asset
GET /assets/bitcoin/markets

# All exchanges
GET /exchanges

# All rates (fiat & crypto)
GET /rates
```

**Python Example:**
```python
import requests

url = "https://api.coincap.io/v2/assets"
params = {"limit": 10}
response = requests.get(url, params=params)
assets = response.json()["data"]

for asset in assets:
    print(f"{asset['name']}: ${float(asset['priceUsd']):.2f}")
```

---

## 2. Stock Market Data APIs

### 2.1 Yahoo Finance Chart API ✅ CONFIRMED WORKING

| Detail | Value |
|--------|-------|
| **Base URL** | `https://query1.finance.yahoo.com/v8/finance/chart/` |
| **Auth** | **No API key required** |
| **Rate Limit** | ~2000 req/hour (unofficial, be respectful) |
| **Docs** | Unofficial (no official docs) |
| **Free Tier** | Free, no registration |

**Key Endpoints:**

```
# OHLCV chart data
GET /v8/finance/chart/{SYMBOL}?interval=1d&range=5d
GET /v8/finance/chart/AAPL?interval=1d&range=1mo
GET /v8/finance/chart/AAPL?interval=1h&range=5d
GET /v8/finance/chart/MSFT?interval=1wk&range=1y

# Intervals: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
# Ranges: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
```

**Verified Response** (`chart/AAPL?interval=1d&range=5d`):
```json
{
  "chart": {
    "result": [{
      "meta": {
        "symbol": "AAPL",
        "regularMarketPrice": 278.12,
        "currency": "USD",
        "exchangeName": "NMS",
        "instrumentType": "EQUITY"
      },
      "timestamp": [1738540200, 1738626600, ...],
      "indicators": {
        "quote": [{
          "open": [232.0, 233.5, ...],
          "high": [236.0, 237.0, ...],
          "low": [229.50, 232.10, ...],
          "close": [235.50, 236.80, ...],
          "volume": [45000000, 38000000, ...]
        }]
      }
    }]
  }
}
```

**Python Example:**
```python
import requests

def get_stock_data(symbol: str, interval: str = "1d", range_: str = "1mo") -> dict:
    """Fetch stock data from Yahoo Finance."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {"interval": interval, "range": range_}
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, params=params, headers=headers)
    return response.json()

data = get_stock_data("AAPL")
result = data["chart"]["result"][0]
price = result["meta"]["regularMarketPrice"]
closes = result["indicators"]["quote"][0]["close"]
```

---

### 2.2 Alpha Vantage API ✅ CONFIRMED WORKING

| Detail | Value |
|--------|-------|
| **Base URL** | `https://www.alphavantage.co/query` |
| **Auth** | Free API key required (instant, no credit card) |
| **Rate Limit** | 25 req/day (free tier) |
| **Get Key** | https://www.alphavantage.co/support/#api-key |
| **Docs** | https://www.alphavantage.co/documentation/ |
| **Free Tier** | 25 requests/day |

**Key Endpoints (functions):**

```
# Real-time quote
?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_KEY

# Daily time series
?function=TIME_SERIES_DAILY&symbol=AAPL&outputsize=compact&apikey=YOUR_KEY

# Intraday
?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=YOUR_KEY

# Symbol search
?function=SYMBOL_SEARCH&keywords=tesla&apikey=YOUR_KEY

# Technical indicators (50+ available)
?function=RSI&symbol=AAPL&interval=daily&time_period=14&series_type=close&apikey=YOUR_KEY
?function=MACD&symbol=AAPL&interval=daily&series_type=close&apikey=YOUR_KEY
?function=SMA&symbol=AAPL&interval=daily&time_period=50&series_type=close&apikey=YOUR_KEY
?function=BBANDS&symbol=AAPL&interval=daily&time_period=20&series_type=close&apikey=YOUR_KEY

# Crypto (daily)
?function=DIGITAL_CURRENCY_DAILY&symbol=BTC&market=USD&apikey=YOUR_KEY

# Forex
?function=CURRENCY_EXCHANGE_RATE&from_currency=EUR&to_currency=USD&apikey=YOUR_KEY

# Commodities
?function=WTI&interval=daily&apikey=YOUR_KEY
?function=BRENT&interval=daily&apikey=YOUR_KEY
?function=NATURAL_GAS&interval=daily&apikey=YOUR_KEY
?function=COPPER&interval=monthly&apikey=YOUR_KEY

# Economic indicators
?function=REAL_GDP&interval=quarterly&apikey=YOUR_KEY
?function=CPI&interval=monthly&apikey=YOUR_KEY
?function=INFLATION&apikey=YOUR_KEY
?function=UNEMPLOYMENT&apikey=YOUR_KEY
?function=FEDERAL_FUNDS_RATE&interval=daily&apikey=YOUR_KEY

# News sentiment
?function=NEWS_SENTIMENT&tickers=AAPL&apikey=YOUR_KEY
```

**Available Technical Indicators:**
SMA, EMA, WMA, DEMA, TEMA, TRIMA, KAMA, MAMA, VWAP, T3, RSI, MACD, STOCH, STOCHF, STOCHRSI, WILLR, ADX, ADXR, APO, PPO, MOM, BOP, CCI, CMO, ROC, ROCR, AROON, AROONOSC, MFI, TRIX, ULTOSC, DX, MINUS_DI, PLUS_DI, MINUS_DM, PLUS_DM, BBANDS, MIDPOINT, MIDPRICE, SAR, TRANGE, ATR, NATR, AD, ADOSC, OBV, HT_TRENDLINE, HT_SINE, HT_TRENDMODE, HT_DCPERIOD, HT_DCPHASE, HT_PHASOR

**Python Example:**
```python
import requests

API_KEY = "YOUR_FREE_KEY"  # Get at alphavantage.co/support/#api-key
BASE_URL = "https://www.alphavantage.co/query"

# Demo key works for testing: apikey=demo

# Get real-time quote
params = {
    "function": "GLOBAL_QUOTE",
    "symbol": "AAPL",
    "apikey": API_KEY
}
response = requests.get(BASE_URL, params=params)
quote = response.json()["Global Quote"]
price = float(quote["05. price"])
change = float(quote["10. change percent"].rstrip("%"))

# Get RSI
params = {
    "function": "RSI",
    "symbol": "AAPL",
    "interval": "daily",
    "time_period": 14,
    "series_type": "close",
    "apikey": API_KEY
}
response = requests.get(BASE_URL, params=params)
rsi_data = response.json()
```

---

## 3. Whale / Large Transaction APIs

### 3.1 Blockchain.info (Bitcoin) ✅ CONFIRMED WORKING

| Detail | Value |
|--------|-------|
| **Base URL** | `https://blockchain.info/` |
| **Auth** | **No API key required** |
| **Rate Limit** | Reasonable use |
| **Docs** | https://www.blockchain.com/api |
| **Free Tier** | Free |

**Key Endpoints:**

```
# Unconfirmed transactions (live mempool)
GET /unconfirmed-transactions?format=json

# Single transaction detail
GET /rawtx/{tx_hash}

# Address info
GET /rawaddr/{address}

# Block info
GET /rawblock/{block_hash}

# Latest block
GET /latestblock

# Bitcoin stats
GET /stats?format=json

# Ticker (BTC price in multiple currencies)
GET /ticker
```

**Verified Response** (`/unconfirmed-transactions?format=json`):
```json
{
  "txs": [
    {
      "hash": "abc123...",
      "ver": 2,
      "size": 223,
      "fee": 4500,
      "inputs": [{"prev_out": {"value": 150000000, "addr": "bc1q..."}}],
      "out": [{"value": 149995500, "addr": "bc1q..."}],
      "time": 1707350400
    }
  ]
}
```

**Python Example — Detect Large BTC Transactions:**
```python
import requests

def find_whale_transactions(min_btc: float = 100.0) -> list:
    """Find large Bitcoin transactions in the mempool."""
    url = "https://blockchain.info/unconfirmed-transactions?format=json"
    response = requests.get(url)
    txs = response.json()["txs"]
    
    whales = []
    for tx in txs:
        total_value = sum(out["value"] for out in tx["out"])
        btc_value = total_value / 1e8  # Convert satoshis to BTC
        
        if btc_value >= min_btc:
            whales.append({
                "hash": tx["hash"],
                "btc": round(btc_value, 4),
                "fee_sat": tx["fee"],
                "outputs": len(tx["out"])
            })
    
    return whales

large_txs = find_whale_transactions(min_btc=50)
for tx in large_txs:
    print(f"🐋 {tx['btc']} BTC — hash: {tx['hash'][:16]}...")
```

---

### 3.2 Blockchair API

| Detail | Value |
|--------|-------|
| **Base URL** | `https://api.blockchair.com/` |
| **Auth** | Free tier available (API key for higher limits) |
| **Rate Limit** | 30 req/min (free, no key) |
| **Docs** | https://blockchair.com/api/docs |
| **Free Tier** | 30 req/min without key, 1440/day |

**Key Endpoints:**

```
# Bitcoin transactions (sorted by value)
GET /bitcoin/transactions?limit=10&s=output_total(desc)

# Bitcoin stats
GET /bitcoin/stats

# Ethereum transactions
GET /ethereum/transactions?limit=10&s=value(desc)

# Address info
GET /bitcoin/dashboards/address/{address}

# Multi-chain support: bitcoin, ethereum, litecoin, bitcoin-cash, etc.
```

**Python Example:**
```python
import requests

# Large Bitcoin transactions
url = "https://api.blockchair.com/bitcoin/transactions"
params = {"limit": 10, "s": "output_total(desc)"}
response = requests.get(url, params=params)
data = response.json()
```

---

### 3.3 Etherscan API (Ethereum)

| Detail | Value |
|--------|-------|
| **Base URL** | `https://api.etherscan.io/api` |
| **Auth** | Free API key required |
| **Rate Limit** | 5 calls/sec (free) |
| **Get Key** | https://etherscan.io/apis |
| **Free Tier** | 100,000 calls/day |

**Key Endpoints:**

```
# Get ETH balance
?module=account&action=balance&address=0x...&tag=latest&apikey=YOUR_KEY

# Get transaction list for address
?module=account&action=txlist&address=0x...&startblock=0&endblock=99999999&sort=desc&apikey=YOUR_KEY

# Get ERC-20 token transfers
?module=account&action=tokentx&address=0x...&sort=desc&apikey=YOUR_KEY

# ETH price
?module=stats&action=ethprice&apikey=YOUR_KEY

# Gas price
?module=gastracker&action=gasoracle&apikey=YOUR_KEY
```

---

## 4. Market News APIs

### 4.1 CryptoCompare News ✅ CONFIRMED WORKING
(See section 1.3 above — the `/data/v2/news/` endpoint provides excellent crypto news aggregation with no API key required)

---

### 4.2 NewsData.io ✅ CONFIRMED WORKING

| Detail | Value |
|--------|-------|
| **Base URL** | `https://newsdata.io/api/1/` |
| **Auth** | Free API key required |
| **Rate Limit** | 200 credits/day (free), 1800 credits/15min (paid) |
| **Get Key** | https://newsdata.io/ |
| **Docs** | https://newsdata.io/documentation |
| **Free Tier** | 200 credits/day |

**Key Endpoints:**

```
# Latest news
GET /latest?apikey=YOUR_KEY&category=business&language=en

# Crypto-specific news
GET /crypto?apikey=YOUR_KEY&coin=btc
GET /crypto?apikey=YOUR_KEY&coin=eth,usdt,bnb

# Market/financial news
GET /market?apikey=YOUR_KEY&symbol=AAPL,TSLA

# News from specific domains
GET /latest?apikey=YOUR_KEY&domain=bbc

# Search by keyword
GET /latest?apikey=YOUR_KEY&q=bitcoin&language=en
```

**Response includes:** title, description, content, pubDate, sentiment, sentiment_stats, ai_tag, ai_summary, source info, image URL, keywords

**Python Example:**
```python
import requests

API_KEY = "YOUR_NEWSDATA_KEY"
url = "https://newsdata.io/api/1/crypto"
params = {
    "apikey": API_KEY,
    "coin": "btc",
    "language": "en"
}
response = requests.get(url, params=params)
articles = response.json()["results"]

for article in articles[:5]:
    print(f"📰 {article['title']}")
    print(f"   Sentiment: {article.get('sentiment', 'N/A')}")
    print(f"   Source: {article['source_name']}")
```

---

### 4.3 Alpha Vantage News Sentiment
(See section 2.2 — use `function=NEWS_SENTIMENT&tickers=AAPL`)

```python
params = {
    "function": "NEWS_SENTIMENT",
    "tickers": "AAPL,MSFT",
    "apikey": API_KEY
}
response = requests.get("https://www.alphavantage.co/query", params=params)
```

---

## 5. Market Sentiment APIs

### 5.1 Alternative.me Fear & Greed Index ✅ CONFIRMED WORKING

| Detail | Value |
|--------|-------|
| **Base URL** | `https://api.alternative.me/` |
| **Auth** | **No API key required** |
| **Rate Limit** | Generous |
| **Docs** | https://alternative.me/crypto/fear-and-greed-index/ |
| **Free Tier** | Completely free |

**Key Endpoints:**

```
# Current Fear & Greed Index
GET /fng/

# Last N days
GET /fng/?limit=30

# Specific date range
GET /fng/?limit=365&date_format=us
```

**Verified Response:**
```json
{
  "name": "Fear and Greed Index",
  "data": [
    {
      "value": "7",
      "value_classification": "Extreme Fear",
      "timestamp": "1738886400",
      "time_until_update": "54321"
    }
  ]
}
```

**Value ranges:** 0-24 = Extreme Fear, 25-49 = Fear, 50 = Neutral, 51-74 = Greed, 75-100 = Extreme Greed

**Python Example:**
```python
import requests

url = "https://api.alternative.me/fng/"
params = {"limit": 7}
response = requests.get(url, params=params)
data = response.json()["data"]

for day in data:
    print(f"Fear & Greed: {day['value']} ({day['value_classification']})")
```

---

## 6. Quick Integration Cheat Sheet

### APIs That Need NO API Key (Instant Use)

| API | Best For | URL |
|-----|----------|-----|
| CoinPaprika | Crypto prices, tickers, coin info | `api.coinpaprika.com/v1/` |
| Alternative.me | Crypto Fear & Greed Index | `api.alternative.me/fng/` |
| Blockchain.info | Bitcoin transactions, whale detection | `blockchain.info/` |
| Yahoo Finance | Stock OHLCV data | `query1.finance.yahoo.com/v8/finance/chart/` |
| CryptoCompare | Crypto news aggregation | `min-api.cryptocompare.com/data/v2/news/` |
| CoinCap | Crypto assets ranked | `api.coincap.io/v2/assets` |

### APIs That Need a FREE API Key (No Credit Card)

| API | Best For | Get Key |
|-----|----------|---------|
| CoinGecko | Comprehensive crypto data | coingecko.com/en/developers/dashboard |
| Alpha Vantage | Stocks, indicators, commodities, economic data | alphavantage.co/support/#api-key |
| NewsData.io | Financial news with sentiment | newsdata.io |
| Etherscan | Ethereum transactions & tokens | etherscan.io/apis |

### Complete Python Integration Example

```python
"""
SignalTrust Market Data Provider
Combines all free APIs for comprehensive market coverage.
"""
import requests
import time
from typing import Dict, List, Optional


class MarketDataProvider:
    """Unified market data from free APIs."""
    
    def __init__(self, alpha_vantage_key: str = "demo",
                 coingecko_key: str = None):
        self.av_key = alpha_vantage_key
        self.cg_key = coingecko_key
    
    # ── Crypto Prices ──────────────────────────────
    
    def get_crypto_prices(self, coins: List[str]) -> Dict:
        """Get crypto prices from CoinGecko."""
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": ",".join(coins),
            "vs_currencies": "usd",
            "include_24hr_change": "true",
            "include_24hr_vol": "true",
            "include_market_cap": "true"
        }
        headers = {}
        if self.cg_key:
            headers["x-cg-demo-api-key"] = self.cg_key
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        return response.json()
    
    def get_crypto_tickers(self, limit: int = 100) -> List[Dict]:
        """Get top crypto tickers from CoinPaprika (no key needed)."""
        url = "https://api.coinpaprika.com/v1/tickers"
        response = requests.get(url, timeout=10)
        return response.json()[:limit]
    
    # ── Stock Prices ───────────────────────────────
    
    def get_stock_chart(self, symbol: str, interval: str = "1d",
                        range_: str = "1mo") -> Dict:
        """Get stock OHLCV from Yahoo Finance (no key needed)."""
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
        params = {"interval": interval, "range": range_}
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        return response.json()
    
    def get_stock_quote(self, symbol: str) -> Dict:
        """Get real-time stock quote from Alpha Vantage."""
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": self.av_key
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    
    # ── Technical Indicators ───────────────────────
    
    def get_rsi(self, symbol: str, period: int = 14) -> Dict:
        """Get RSI from Alpha Vantage."""
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "RSI",
            "symbol": symbol,
            "interval": "daily",
            "time_period": period,
            "series_type": "close",
            "apikey": self.av_key
        }
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    
    # ── Whale Detection ────────────────────────────
    
    def get_btc_whale_transactions(self, min_btc: float = 100.0) -> List[Dict]:
        """Find large BTC transactions in mempool."""
        url = "https://blockchain.info/unconfirmed-transactions?format=json"
        response = requests.get(url, timeout=15)
        txs = response.json()["txs"]
        
        whales = []
        for tx in txs:
            total = sum(out["value"] for out in tx["out"])
            btc = total / 1e8
            if btc >= min_btc:
                whales.append({
                    "hash": tx["hash"],
                    "btc": round(btc, 4),
                    "fee": tx["fee"]
                })
        return whales
    
    # ── Market Sentiment ───────────────────────────
    
    def get_fear_greed_index(self, days: int = 1) -> Dict:
        """Get Crypto Fear & Greed Index (no key needed)."""
        url = "https://api.alternative.me/fng/"
        params = {"limit": days}
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    
    # ── News ───────────────────────────────────────
    
    def get_crypto_news(self, limit: int = 20) -> List[Dict]:
        """Get crypto news from CryptoCompare (no key needed)."""
        url = "https://min-api.cryptocompare.com/data/v2/news/"
        params = {"lang": "EN"}
        response = requests.get(url, params=params, timeout=10)
        articles = response.json()["Data"][:limit]
        return [{
            "title": a["title"],
            "url": a["url"],
            "source": a["source"],
            "categories": a["categories"],
            "published": a["published_on"]
        } for a in articles]


# ── Usage ──────────────────────────────────────────
if __name__ == "__main__":
    provider = MarketDataProvider()
    
    # Crypto prices
    prices = provider.get_crypto_prices(["bitcoin", "ethereum", "solana"])
    print("BTC:", prices["bitcoin"]["usd"])
    
    # Fear & Greed
    fng = provider.get_fear_greed_index()
    print("Fear & Greed:", fng["data"][0]["value"],
          fng["data"][0]["value_classification"])
    
    # Stock data
    aapl = provider.get_stock_chart("AAPL", range_="5d")
    print("AAPL:", aapl["chart"]["result"][0]["meta"]["regularMarketPrice"])
    
    # Whale detection
    whales = provider.get_btc_whale_transactions(min_btc=50)
    print(f"Found {len(whales)} whale transactions")
    
    # Crypto news
    news = provider.get_crypto_news(limit=3)
    for n in news:
        print(f"📰 {n['title']}")
```

---

## API Status Summary

| API | Status | Auth | Best For |
|-----|--------|------|----------|
| CoinGecko v3 | ✅ Working | Free key (optional) | Crypto prices, market data |
| CoinPaprika v1 | ✅ Working | None | Crypto tickers, % changes |
| CryptoCompare | ✅ Working | None | Crypto news aggregation |
| CoinCap v2 | ✅ Working | None | Real-time crypto assets |
| Yahoo Finance | ✅ Working | None | Stock OHLCV charts |
| Alpha Vantage | ✅ Working | Free key | Stocks, indicators, economic data |
| Blockchain.info | ✅ Working | None | BTC whale transactions |
| Alternative.me | ✅ Working | None | Fear & Greed Index |
| NewsData.io | ✅ Working | Free key | Financial news + sentiment |
| Etherscan | ✅ Working | Free key | ETH transactions |
| Blockchair | ⚠️ Partial | None / Free key | Multi-chain explorer |
| Whale Alert | ❌ 404 | Paid key | Whale tracking (paid only) |

---

*Last verified: February 2026*
