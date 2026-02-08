"""
On-Chain Data Analyst Agent
Analyzes blockchain metrics: active addresses, token age, contract calls
Uses Dune Analytics and Glassnode APIs
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="On-Chain Data Agent",
    description="Blockchain metrics and on-chain analysis",
    version="1.0.0"
)

class OnChainRequest(BaseModel):
    """Request model for on-chain analysis"""
    symbol: str  # e.g., BTC, ETH
    network: str = "mainnet"  # mainnet, testnet
    metrics: List[str] = ["all"]  # active_addresses, whale_flow, etc.

class OnChainResponse(BaseModel):
    """Response model for on-chain data"""
    symbol: str
    network: str
    timestamp: str
    active_addresses: Dict
    whale_activity: Dict
    token_metrics: Dict
    exchange_flow: Dict
    insights: List[str]
    risk_score: float  # 0-1

class OnChainAgent:
    """
    Analyzes on-chain metrics for cryptocurrencies
    """
    
    def __init__(self):
        self.glassnode_api_key = os.getenv("GLASSNODE_API_KEY", "")
        self.dune_api_key = os.getenv("DUNE_API_KEY", "")
        
    async def analyze_onchain(self, symbol: str, network: str,
                             metrics: List[str]) -> OnChainResponse:
        """
        Analyze on-chain metrics
        
        Args:
            symbol: Cryptocurrency symbol
            network: Blockchain network
            metrics: List of metrics to analyze
            
        Returns:
            OnChainResponse with comprehensive metrics
        """
        logger.info(f"Analyzing on-chain data for {symbol} on {network}")
        
        # Get various metrics
        active_addresses = await self._get_active_addresses(symbol, network)
        whale_activity = await self._get_whale_activity(symbol, network)
        token_metrics = await self._get_token_metrics(symbol, network)
        exchange_flow = await self._get_exchange_flow(symbol, network)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(
            active_addresses, whale_activity, exchange_flow
        )
        
        # Generate insights
        insights = self._generate_insights(
            symbol, active_addresses, whale_activity, 
            exchange_flow, risk_score
        )
        
        return OnChainResponse(
            symbol=symbol,
            network=network,
            timestamp=datetime.utcnow().isoformat(),
            active_addresses=active_addresses,
            whale_activity=whale_activity,
            token_metrics=token_metrics,
            exchange_flow=exchange_flow,
            insights=insights,
            risk_score=round(risk_score, 3)
        )
    
    async def _get_active_addresses(self, symbol: str, network: str) -> Dict:
        """Get active address metrics"""
        # Simulated data (would use Glassnode/Dune API)
        return {
            "count_24h": 145000,
            "change_24h": 0.32,  # +32%
            "count_7d": 980000,
            "change_7d": 0.15,
            "new_addresses_24h": 12500,
            "trend": "increasing"
        }
    
    async def _get_whale_activity(self, symbol: str, network: str) -> Dict:
        """Get whale transaction data"""
        return {
            "large_transactions_24h": 45,
            "total_volume_usd": 125000000,
            "inflow_to_exchanges": 35000000,
            "outflow_from_exchanges": 58000000,
            "net_flow": 23000000,  # Positive = accumulation
            "whale_addresses_active": 234,
            "pattern": "accumulation"
        }
    
    async def _get_token_metrics(self, symbol: str, network: str) -> Dict:
        """Get token-specific metrics"""
        return {
            "token_age_consumed": 0.45,  # 0-1 scale
            "hodl_waves": {
                "1d_to_1w": 0.15,
                "1w_to_1m": 0.25,
                "1m_to_3m": 0.30,
                "3m_to_1y": 0.20,
                "1y_plus": 0.10
            },
            "supply_on_exchanges": 0.12,  # 12% on exchanges
            "supply_last_active": {
                "1d": 0.08,
                "7d": 0.22,
                "30d": 0.45
            }
        }
    
    async def _get_exchange_flow(self, symbol: str, network: str) -> Dict:
        """Get exchange inflow/outflow data"""
        return {
            "inflow_24h_usd": 35000000,
            "outflow_24h_usd": 58000000,
            "net_flow_24h_usd": 23000000,
            "inflow_change_24h": 0.15,
            "outflow_change_24h": 0.28,
            "top_exchanges": [
                {"name": "Binance", "net_flow": 12000000},
                {"name": "Coinbase", "net_flow": 8500000},
                {"name": "Kraken", "net_flow": 2500000}
            ]
        }
    
    def _calculate_risk_score(self, active_addr: Dict, whale: Dict,
                             exchange: Dict) -> float:
        """
        Calculate risk score (0-1, lower is better)
        
        Factors:
        - Exchange inflow (selling pressure)
        - Whale accumulation/distribution
        - Active address trend
        """
        risk = 0.0
        
        # Exchange inflow risk
        net_flow = exchange.get("net_flow_24h_usd", 0)
        if net_flow < 0:  # Net inflow to exchanges
            risk += 0.3
        
        # Whale distribution risk
        whale_pattern = whale.get("pattern", "neutral")
        if whale_pattern == "distribution":
            risk += 0.4
        elif whale_pattern == "accumulation":
            risk -= 0.2
        
        # Active addresses declining
        addr_change = active_addr.get("change_24h", 0)
        if addr_change < -0.1:  # Declining 10%+
            risk += 0.3
        
        return max(0.0, min(1.0, risk))
    
    def _generate_insights(self, symbol: str, active_addr: Dict,
                          whale: Dict, exchange: Dict, risk: float) -> List[str]:
        """Generate actionable insights"""
        insights = []
        
        # Active addresses
        addr_change = active_addr.get("change_24h", 0)
        if addr_change > 0.2:
            insights.append(f"Active addresses up {addr_change*100:.1f}% - strong network growth")
        elif addr_change < -0.2:
            insights.append(f"Active addresses down {abs(addr_change)*100:.1f}% - declining activity")
        
        # Whale activity
        whale_pattern = whale.get("pattern", "neutral")
        if whale_pattern == "accumulation":
            insights.append("Whales accumulating - bullish signal")
        elif whale_pattern == "distribution":
            insights.append("Whale distribution detected - caution advised")
        
        # Exchange flow
        net_flow = exchange.get("net_flow_24h_usd", 0)
        if net_flow > 10000000:
            insights.append(f"Large outflow from exchanges (${net_flow/1e6:.1f}M) - bullish")
        elif net_flow < -10000000:
            insights.append(f"Large inflow to exchanges (${abs(net_flow)/1e6:.1f}M) - potential selling pressure")
        
        # Risk assessment
        if risk > 0.7:
            insights.append("⚠️ High on-chain risk - proceed with caution")
        elif risk < 0.3:
            insights.append("✅ Low on-chain risk - favorable conditions")
        
        return insights or ["Neutral on-chain metrics"]

# Initialize agent
agent = OnChainAgent()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "onchain_data",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/analyze", response_model=OnChainResponse)
async def analyze_onchain(request: OnChainRequest):
    """
    Analyze on-chain metrics for a cryptocurrency
    
    Example:
    ```json
    {
        "symbol": "BTC",
        "network": "mainnet",
        "metrics": ["all"]
    }
    ```
    """
    try:
        result = await agent.analyze_onchain(
            request.symbol,
            request.network,
            request.metrics
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing on-chain data: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/whale-alerts")
async def get_whale_alerts():
    """Get recent whale transaction alerts"""
    return {
        "alerts": [
            {
                "timestamp": datetime.utcnow().isoformat(),
                "amount_usd": 25000000,
                "from": "unknown",
                "to": "Binance",
                "type": "exchange_inflow"
            },
            {
                "timestamp": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
                "amount_usd": 18000000,
                "from": "Coinbase",
                "to": "unknown",
                "type": "exchange_outflow"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
