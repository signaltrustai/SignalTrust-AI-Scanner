"""
Macro-Economics Analyst Agent
Monitors and analyzes macroeconomic indicators and events
Tracks Fed decisions, CPI, GDP, unemployment, and their market impact
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from datetime import datetime, timedelta, timezone
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Macro-Economics Agent",
    description="Macroeconomic indicators and calendar analysis",
    version="1.0.0"
)

class MacroRequest(BaseModel):
    """Request model for macro analysis"""
    region: str = "US"  # US, EU, GLOBAL
    timeframe: str = "7d"  # 1d, 7d, 30d
    indicators: List[str] = ["all"]  # fed_rate, cpi, gdp, etc.

class MacroResponse(BaseModel):
    """Response model for macro data"""
    region: str
    timestamp: str
    current_indicators: Dict
    upcoming_events: List[Dict]
    economic_calendar: List[Dict]
    impact_score: float  # -1 to 1
    market_sentiment: str
    insights: List[str]

class MacroEconomicsAgent:
    """
    Analyzes macroeconomic indicators and their market impact
    """
    
    def __init__(self):
        self.fred_api_key = os.getenv("FRED_API_KEY", "")
        self.world_bank_key = os.getenv("WORLD_BANK_API_KEY", "")
        self.eia_key = os.getenv("EIA_API_KEY", "")
        
    async def analyze_macro(self, region: str, timeframe: str,
                           indicators: List[str]) -> MacroResponse:
        """
        Analyze macroeconomic conditions
        
        Args:
            region: Geographic region (US, EU, GLOBAL)
            timeframe: Time window for analysis
            indicators: List of indicators to analyze
            
        Returns:
            MacroResponse with economic data and analysis
        """
        logger.info(f"Analyzing macro for {region}, timeframe: {timeframe}")
        
        # Get current indicators
        current = await self._get_current_indicators(region)
        
        # Get upcoming events
        events = await self._get_upcoming_events(region, timeframe)
        
        # Get economic calendar
        calendar = await self._get_economic_calendar(region, timeframe)
        
        # Calculate market impact
        impact_score = self._calculate_impact_score(current, events)
        
        # Determine sentiment
        sentiment = self._determine_sentiment(impact_score, current)
        
        # Generate insights
        insights = self._generate_insights(region, current, events, impact_score)
        
        return MacroResponse(
            region=region,
            timestamp=datetime.now(timezone.utc).isoformat(),
            current_indicators=current,
            upcoming_events=events,
            economic_calendar=calendar,
            impact_score=round(impact_score, 3),
            market_sentiment=sentiment,
            insights=insights
        )
    
    async def _get_current_indicators(self, region: str) -> Dict:
        """Get current macroeconomic indicators"""
        # Simulated data (would use FRED, World Bank, etc.)
        return {
            "fed_funds_rate": 5.25,  # Current Fed rate
            "fed_rate_change": 0.0,  # Last change
            "cpi_annual": 3.2,  # CPI year-over-year
            "cpi_monthly": 0.2,  # CPI month-over-month
            "unemployment": 3.7,  # Unemployment rate
            "gdp_growth": 2.8,  # GDP growth (annual)
            "pce_inflation": 2.9,  # PCE inflation (Fed's preferred)
            "10y_treasury": 4.35,  # 10-year Treasury yield
            "vix": 14.5,  # VIX (volatility index)
            "dxy": 103.2,  # Dollar index
            "oil_price": 78.50,  # WTI crude
            "gold_price": 2025.00,  # Gold per oz
        }
    
    async def _get_upcoming_events(self, region: str, timeframe: str) -> List[Dict]:
        """Get upcoming macro events"""
        now = datetime.now(timezone.utc)
        return [
            {
                "date": (now + timedelta(days=2)).isoformat(),
                "event": "FOMC Meeting",
                "impact": "high",
                "expected": "Rate hold at 5.25%",
                "consensus": "No change expected"
            },
            {
                "date": (now + timedelta(days=5)).isoformat(),
                "event": "CPI Release",
                "impact": "high",
                "expected": "3.1% YoY",
                "consensus": "Slight decline from previous"
            },
            {
                "date": (now + timedelta(days=7)).isoformat(),
                "event": "Unemployment Report",
                "impact": "medium",
                "expected": "3.8%",
                "consensus": "Stable labor market"
            },
            {
                "date": (now + timedelta(days=10)).isoformat(),
                "event": "GDP Report",
                "impact": "medium",
                "expected": "2.5% growth",
                "consensus": "Moderate growth"
            }
        ]
    
    async def _get_economic_calendar(self, region: str, timeframe: str) -> List[Dict]:
        """Get full economic calendar"""
        # Simulated calendar with dynamic dates
        now = datetime.now()
        return [
            {"date": (now + timedelta(days=3)).strftime("%Y-%m-%d"), "event": "FOMC Minutes", "impact": "medium"},
            {"date": (now + timedelta(days=5)).strftime("%Y-%m-%d"), "event": "Retail Sales", "impact": "low"},
            {"date": (now + timedelta(days=6)).strftime("%Y-%m-%d"), "event": "CPI Data", "impact": "high"},
            {"date": (now + timedelta(days=8)).strftime("%Y-%m-%d"), "event": "Industrial Production", "impact": "low"},
        ]
    
    def _calculate_impact_score(self, indicators: Dict, events: List[Dict]) -> float:
        """
        Calculate market impact score (-1 to 1)
        Positive = bullish for risk assets
        Negative = bearish for risk assets
        """
        score = 0.0
        
        # Interest rates (higher = more negative for risk assets)
        fed_rate = indicators.get("fed_funds_rate", 5.0)
        if fed_rate > 5.0:
            score -= 0.2
        elif fed_rate < 4.0:
            score += 0.2
        
        # Inflation (moderate inflation is good, too high/low is bad)
        cpi = indicators.get("cpi_annual", 3.0)
        if 2.0 <= cpi <= 3.0:
            score += 0.1
        elif cpi > 4.0:
            score -= 0.3
        
        # Unemployment (low is good for economy)
        unemployment = indicators.get("unemployment", 4.0)
        if unemployment < 4.0:
            score += 0.2
        elif unemployment > 5.0:
            score -= 0.2
        
        # GDP growth (higher is better)
        gdp = indicators.get("gdp_growth", 2.0)
        if gdp > 2.5:
            score += 0.2
        elif gdp < 1.5:
            score -= 0.2
        
        # VIX (fear gauge - lower is better)
        vix = indicators.get("vix", 15.0)
        if vix < 15:
            score += 0.1
        elif vix > 20:
            score -= 0.2
        
        # Upcoming high-impact events
        high_impact_count = sum(1 for e in events if e.get("impact") == "high")
        if high_impact_count >= 2:
            score -= 0.1  # Uncertainty
        
        return max(-1.0, min(1.0, score))
    
    def _determine_sentiment(self, impact_score: float, indicators: Dict) -> str:
        """Determine overall market sentiment"""
        if impact_score > 0.3:
            return "bullish"
        elif impact_score < -0.3:
            return "bearish"
        else:
            return "neutral"
    
    def _generate_insights(self, region: str, indicators: Dict,
                          events: List[Dict], impact: float) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        # Fed rate analysis
        fed_rate = indicators.get("fed_funds_rate", 5.0)
        if fed_rate >= 5.0:
            insights.append(f"Fed funds rate at {fed_rate}% - restrictive monetary policy")
        
        # Inflation
        cpi = indicators.get("cpi_annual", 3.0)
        if cpi > 3.5:
            insights.append(f"Elevated inflation at {cpi}% - potential for further tightening")
        elif cpi < 2.5:
            insights.append(f"Inflation cooling at {cpi}% - Fed may pause or cut rates")
        
        # GDP
        gdp = indicators.get("gdp_growth", 2.0)
        if gdp > 2.5:
            insights.append(f"Strong GDP growth at {gdp}% - economy resilient")
        elif gdp < 1.5:
            insights.append(f"Weak GDP growth at {gdp}% - recession risk")
        
        # Upcoming events
        high_impact = [e for e in events if e.get("impact") == "high"]
        if high_impact:
            next_event = high_impact[0]
            insights.append(f"⚠️ Major event: {next_event['event']} on {next_event['date'][:10]}")
        
        # Overall sentiment
        if impact > 0.3:
            insights.append("✅ Favorable macro conditions for risk assets")
        elif impact < -0.3:
            insights.append("⚠️ Challenging macro environment - defensive positioning advised")
        
        return insights or ["Neutral macro environment"]

# Initialize agent
agent = MacroEconomicsAgent()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "macro_economics",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/analyze", response_model=MacroResponse)
async def analyze_macro(request: MacroRequest):
    """
    Analyze macroeconomic conditions
    
    Example:
    ```json
    {
        "region": "US",
        "timeframe": "7d",
        "indicators": ["all"]
    }
    ```
    """
    try:
        result = await agent.analyze_macro(
            request.region,
            request.timeframe,
            request.indicators
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing macro: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/indicators")
async def get_current_indicators():
    """Get current macro indicators snapshot"""
    indicators = await agent._get_current_indicators("US")
    return {
        "indicators": indicators,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/calendar")
async def get_economic_calendar():
    """Get upcoming economic events"""
    events = await agent._get_upcoming_events("US", "30d")
    return {
        "events": events,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
