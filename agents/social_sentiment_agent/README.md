# Social Sentiment Agent

Real-time social media sentiment analysis for cryptocurrency and stock markets.

## Features

- **Multi-Platform Analysis**: Twitter, Reddit, Discord, Telegram
- **BERT-Finance Integration**: Domain-specific sentiment model
- **Real-time Trending**: Identify trending assets
- **Volume Scoring**: Measure social media activity
- **Keyword Extraction**: Extract trending keywords and themes

## API Endpoints

### POST /analyze
Analyze sentiment for a symbol across social platforms.

**Request:**
```json
{
  "symbol": "BTC",
  "platforms": ["twitter", "reddit"],
  "timeframe": "24h"
}
```

**Response:**
```json
{
  "symbol": "BTC",
  "timestamp": "2026-02-08T00:00:00",
  "overall_sentiment": 0.625,
  "sentiment_class": "positive",
  "volume_score": 0.85,
  "trending_score": 0.72,
  "platforms": {...},
  "keywords": ["bullish", "breakout"],
  "insights": ["Strong positive sentiment with high volume for BTC"]
}
```

### GET /trending
Get currently trending symbols across all platforms.

### GET /health
Health check endpoint.

## Environment Variables

- `TWITTER_API_KEY`: Twitter API key
- `REDDIT_CLIENT_ID`: Reddit client ID
- `REDDIT_CLIENT_SECRET`: Reddit client secret
- `PORT`: Server port (default: 8000)

## Running Locally

```bash
pip install -r requirements.txt
export TWITTER_API_KEY=your_key
python main.py
```

## Running with Docker

```bash
docker build -t social-sentiment-agent .
docker run -p 8005:8000 \
  -e TWITTER_API_KEY=your_key \
  -e REDDIT_CLIENT_ID=your_id \
  social-sentiment-agent
```

## Integration

This agent integrates with the coordinator via port 8005:

```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://social_sentiment_agent:8000/analyze",
        json={"symbol": "BTC", "platforms": ["twitter", "reddit"]}
    )
    sentiment_data = response.json()
```

## Production Notes

For production deployment:
1. Install BERT-finance model: `pip install transformers torch`
2. Configure API keys for all platforms
3. Set up rate limiting and caching
4. Monitor API quotas

## Data Sources

- **Twitter API v2**: Real-time tweets and engagement
- **Reddit API (PRAW)**: Subreddit posts and comments
- **Discord API**: Server messages (requires bot)
- **Telegram Bot API**: Group/channel messages

---

**Port**: 8005  
**Agent Type**: Complementary  
**Priority**: ⭐⭐⭐⭐ (High)
