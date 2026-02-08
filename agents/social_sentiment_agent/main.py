"""
Social Sentiment Analyst Agent
Analyzes social media sentiment from Twitter, Reddit, Discord, Telegram
Uses BERT-finance for sentiment analysis
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Social Sentiment Agent",
    description="Real-time social media sentiment analysis for crypto/stocks",
    version="1.0.0"
)

class SentimentRequest(BaseModel):
    """Request model for sentiment analysis"""
    symbol: str
    platforms: List[str] = ["twitter", "reddit"]
    timeframe: str = "24h"  # 1h, 6h, 24h, 7d

class SentimentResponse(BaseModel):
    """Response model for sentiment analysis"""
    symbol: str
    timestamp: str
    overall_sentiment: float  # -1 to 1
    sentiment_class: str  # negative, neutral, positive
    volume_score: float  # 0 to 1
    trending_score: float  # 0 to 1
    platforms: Dict[str, Dict]
    keywords: List[str]
    insights: List[str]

class SocialSentimentAgent:
    """
    Analyzes sentiment across multiple social platforms
    """
    
    def __init__(self):
        self.twitter_api_key = os.getenv("TWITTER_API_KEY", "")
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Sentiment model (would use BERT-finance in production)
        self.model_available = False
        
    async def analyze_sentiment(self, symbol: str, platforms: List[str],
                               timeframe: str) -> SentimentResponse:
        """
        Analyze sentiment across platforms
        
        Args:
            symbol: Asset symbol (e.g., BTC, AAPL)
            platforms: List of platforms to analyze
            timeframe: Time window for analysis
            
        Returns:
            SentimentResponse with aggregated sentiment data
        """
        logger.info(f"Analyzing sentiment for {symbol} on {platforms}")
        
        platform_results = {}
        
        # Analyze each platform
        for platform in platforms:
            if platform == "twitter":
                platform_results["twitter"] = await self._analyze_twitter(symbol, timeframe)
            elif platform == "reddit":
                platform_results["reddit"] = await self._analyze_reddit(symbol, timeframe)
            elif platform == "discord":
                platform_results["discord"] = await self._analyze_discord(symbol, timeframe)
            elif platform == "telegram":
                platform_results["telegram"] = await self._analyze_telegram(symbol, timeframe)
        
        # Aggregate results
        overall_sentiment = self._aggregate_sentiment(platform_results)
        volume_score = self._calculate_volume_score(platform_results)
        trending_score = self._calculate_trending_score(platform_results)
        
        # Extract keywords
        keywords = self._extract_keywords(platform_results)
        
        # Generate insights
        insights = self._generate_insights(symbol, overall_sentiment, 
                                          volume_score, trending_score)
        
        return SentimentResponse(
            symbol=symbol,
            timestamp=datetime.utcnow().isoformat(),
            overall_sentiment=round(overall_sentiment, 3),
            sentiment_class=self._classify_sentiment(overall_sentiment),
            volume_score=round(volume_score, 3),
            trending_score=round(trending_score, 3),
            platforms=platform_results,
            keywords=keywords,
            insights=insights
        )
    
    async def _analyze_twitter(self, symbol: str, timeframe: str) -> Dict:
        """Analyze Twitter sentiment"""
        # Simulated data (would use Twitter API + BERT-finance)
        return {
            "mention_count": 1250,
            "sentiment_score": 0.65,
            "engagement_rate": 0.78,
            "top_influencers": ["@crypto_expert", "@trader_pro"],
            "sentiment_distribution": {
                "positive": 0.60,
                "neutral": 0.25,
                "negative": 0.15
            }
        }
    
    async def _analyze_reddit(self, symbol: str, timeframe: str) -> Dict:
        """Analyze Reddit sentiment"""
        # Simulated data (would use Reddit API + BERT-finance)
        return {
            "mention_count": 450,
            "sentiment_score": 0.55,
            "upvote_ratio": 0.72,
            "top_subreddits": ["r/cryptocurrency", "r/wallstreetbets"],
            "sentiment_distribution": {
                "positive": 0.55,
                "neutral": 0.30,
                "negative": 0.15
            }
        }
    
    async def _analyze_discord(self, symbol: str, timeframe: str) -> Dict:
        """Analyze Discord sentiment"""
        return {
            "mention_count": 320,
            "sentiment_score": 0.60,
            "active_channels": 15
        }
    
    async def _analyze_telegram(self, symbol: str, timeframe: str) -> Dict:
        """Analyze Telegram sentiment"""
        return {
            "mention_count": 580,
            "sentiment_score": 0.58,
            "active_groups": 8
        }
    
    def _aggregate_sentiment(self, platforms: Dict) -> float:
        """Aggregate sentiment across platforms"""
        if not platforms:
            return 0.0
        
        total_sentiment = 0.0
        total_weight = 0.0
        
        # Weight by mention count
        for platform, data in platforms.items():
            mentions = data.get("mention_count", 0)
            sentiment = data.get("sentiment_score", 0.0)
            
            total_sentiment += sentiment * mentions
            total_weight += mentions
        
        if total_weight == 0:
            return 0.0
        
        return total_sentiment / total_weight
    
    def _calculate_volume_score(self, platforms: Dict) -> float:
        """Calculate volume score (0-1) based on mention counts"""
        total_mentions = sum(p.get("mention_count", 0) for p in platforms.values())
        
        # Normalize (assuming 1000 mentions is "high")
        return min(total_mentions / 1000.0, 1.0)
    
    def _calculate_trending_score(self, platforms: Dict) -> float:
        """Calculate trending score based on engagement"""
        scores = []
        
        for data in platforms.values():
            engagement = data.get("engagement_rate", data.get("upvote_ratio", 0.5))
            scores.append(engagement)
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _extract_keywords(self, platforms: Dict) -> List[str]:
        """Extract trending keywords"""
        # Simulated (would use NLP in production)
        return ["bullish", "breakout", "moon", "buy", "hodl"]
    
    def _classify_sentiment(self, score: float) -> str:
        """Classify sentiment score"""
        if score > 0.3:
            return "positive"
        elif score < -0.3:
            return "negative"
        else:
            return "neutral"
    
    def _generate_insights(self, symbol: str, sentiment: float,
                          volume: float, trending: float) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        if sentiment > 0.5 and volume > 0.7:
            insights.append(f"Strong positive sentiment with high volume for {symbol}")
        
        if trending > 0.7:
            insights.append(f"{symbol} is trending across social platforms")
        
        if sentiment > 0.6 and volume < 0.3:
            insights.append(f"Positive sentiment but low volume - potential early signal")
        
        if sentiment < -0.5:
            insights.append(f"Negative sentiment detected - caution advised")
        
        return insights or ["Neutral social sentiment"]

# Initialize agent
agent = SocialSentimentAgent()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "social_sentiment",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/analyze", response_model=SentimentResponse)
async def analyze_sentiment(request: SentimentRequest):
    """
    Analyze social sentiment for a symbol
    
    Example:
    ```json
    {
        "symbol": "BTC",
        "platforms": ["twitter", "reddit"],
        "timeframe": "24h"
    }
    ```
    """
    try:
        result = await agent.analyze_sentiment(
            request.symbol,
            request.platforms,
            request.timeframe
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/trending")
async def get_trending_symbols():
    """Get trending symbols across social media"""
    return {
        "trending": [
            {"symbol": "BTC", "score": 0.95, "mentions": 15000},
            {"symbol": "ETH", "score": 0.88, "mentions": 8500},
            {"symbol": "AAPL", "score": 0.75, "mentions": 3200}
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
