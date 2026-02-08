"""
Agent Client - Interface for SignalTrust Multi-Agent System
============================================================
Provides a Python client to interact with all SignalTrust AI agents
running in Docker containers.
"""

import os
import logging
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class AgentClient:
    """Client for interacting with SignalTrust multi-agent system."""
    
    def __init__(self, base_url: str = "http://localhost"):
        """
        Initialize the agent client.
        
        Args:
            base_url: Base URL for agent services (default: http://localhost)
        """
        self.base_url = base_url
        self.timeout = 30  # seconds
        
        # Agent ports configuration
        self.agent_ports = {
            "coordinator": 8000,
            "crypto": 8001,
            "stock": 8002,
            "whale": 8003,
            "news": 8004,
            "social_sentiment": 8005,
            "onchain": 8006,
            "macro_economics": 8007,
            "portfolio_optimizer": 8008,
        }
        
    def _build_url(self, agent: str, endpoint: str = "") -> str:
        """Build full URL for agent endpoint."""
        port = self.agent_ports.get(agent)
        if not port:
            raise ValueError(f"Unknown agent: {agent}")
        return f"{self.base_url}:{port}{endpoint}"
    
    def _make_request(self, method: str, url: str, **kwargs) -> Dict[str, Any]:
        """
        Make HTTP request with error handling.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Target URL
            **kwargs: Additional request parameters
            
        Returns:
            Response data as dictionary
        """
        try:
            kwargs.setdefault('timeout', self.timeout)
            response = requests.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            logger.error(f"Timeout calling {url}")
            return {"success": False, "error": f"Agent timeout after {self.timeout}s"}
        except requests.ConnectionError:
            logger.error(f"Connection error to {url}")
            return {"success": False, "error": "Agent service unavailable"}
        except requests.RequestException as e:
            logger.error(f"Request error to {url}: {str(e)}")
            return {"success": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error calling {url}: {str(e)}")
            return {"success": False, "error": f"Unexpected error: {str(e)}"}
    
    def check_health(self, agent: str) -> Dict[str, Any]:
        """
        Check if an agent is healthy and responding.
        
        Args:
            agent: Agent name (coordinator, crypto, stock, etc.)
            
        Returns:
            Health check response
        """
        url = self._build_url(agent, "/health")
        return self._make_request("GET", url)
    
    def check_all_agents(self) -> Dict[str, Dict[str, Any]]:
        """
        Check health of all agents.
        
        Returns:
            Dictionary mapping agent name to health status
        """
        results = {}
        for agent in self.agent_ports.keys():
            results[agent] = self.check_health(agent)
        return results
    
    # -------------------------------------------------------------------------
    # Coordinator Agent
    # -------------------------------------------------------------------------
    
    def get_agents(self) -> Dict[str, Any]:
        """List all available agents from coordinator."""
        url = self._build_url("coordinator", "/agents")
        return self._make_request("GET", url)
    
    def run_workflow(
        self,
        symbol: str = "BTC/USDT",
        ticker: str = "AAPL",
        network: str = "btc",
        topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Run complete market analysis workflow through coordinator.
        
        Args:
            symbol: Crypto symbol (e.g., "BTC/USDT")
            ticker: Stock ticker (e.g., "AAPL")
            network: Blockchain network (btc, eth, bnb)
            topics: List of news topics
            
        Returns:
            Complete workflow analysis results
        """
        if topics is None:
            topics = ["crypto", "stocks", "market"]
            
        url = self._build_url("coordinator", "/run-workflow")
        data = {
            "symbol": symbol,
            "ticker": ticker,
            "network": network,
            "topics": topics
        }
        return self._make_request("POST", url, json=data)
    
    # -------------------------------------------------------------------------
    # Crypto Agent
    # -------------------------------------------------------------------------
    
    def analyze_crypto(self, symbol: str, timeframe: str = "1d") -> Dict[str, Any]:
        """
        Analyze cryptocurrency market.
        
        Args:
            symbol: Crypto symbol (e.g., "BTC/USDT", "ETH/USDT")
            timeframe: Analysis timeframe (1h, 4h, 1d, 1w)
            
        Returns:
            Crypto analysis with predictions and indicators
        """
        url = self._build_url("crypto", "/predict")
        data = {"symbol": symbol, "timeframe": timeframe}
        return self._make_request("POST", url, json=data)
    
    # -------------------------------------------------------------------------
    # Stock Agent
    # -------------------------------------------------------------------------
    
    def analyze_stock(self, ticker: str) -> Dict[str, Any]:
        """
        Analyze stock market.
        
        Args:
            ticker: Stock ticker symbol (e.g., "AAPL", "GOOGL", "TSLA")
            
        Returns:
            Stock analysis with recommendations
        """
        url = self._build_url("stock", "/predict")
        data = {"ticker": ticker}
        return self._make_request("POST", url, json=data)
    
    # -------------------------------------------------------------------------
    # Whale Agent
    # -------------------------------------------------------------------------
    
    def watch_whales(
        self,
        network: str = "btc",
        min_usd: int = 5_000_000
    ) -> Dict[str, Any]:
        """
        Monitor whale (large) blockchain transactions.
        
        Args:
            network: Blockchain network (btc, eth, bnb)
            min_usd: Minimum transaction value in USD
            
        Returns:
            Whale transaction analysis
        """
        url = self._build_url("whale", f"/whales?network={network}&min_usd={min_usd}")
        return self._make_request("GET", url)
    
    # -------------------------------------------------------------------------
    # News Agent
    # -------------------------------------------------------------------------
    
    def get_news(
        self,
        topics: List[str],
        max_items: int = 10
    ) -> Dict[str, Any]:
        """
        Get and analyze market news.
        
        Args:
            topics: List of topics (e.g., ["crypto", "stocks", "technology"])
            max_items: Maximum number of news items
            
        Returns:
            News articles with AI-generated insights
        """
        url = self._build_url("news", "/news")
        data = {"topics": topics, "max_items": max_items}
        return self._make_request("POST", url, json=data)
    
    # -------------------------------------------------------------------------
    # Social Sentiment Agent
    # -------------------------------------------------------------------------
    
    def analyze_sentiment(
        self,
        symbol: str,
        platforms: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze social media sentiment for a symbol.
        
        Args:
            symbol: Symbol to analyze (e.g., "BTC", "AAPL")
            platforms: Social platforms (twitter, reddit, discord, telegram)
            
        Returns:
            Sentiment analysis from social media
        """
        if platforms is None:
            platforms = ["twitter", "reddit"]
            
        url = self._build_url("social_sentiment", "/analyze")
        data = {"symbol": symbol, "platforms": platforms}
        return self._make_request("POST", url, json=data)
    
    def get_trending(self) -> Dict[str, Any]:
        """
        Get trending symbols from social media.
        
        Returns:
            List of trending symbols with sentiment scores
        """
        url = self._build_url("social_sentiment", "/trending")
        return self._make_request("GET", url)
    
    # -------------------------------------------------------------------------
    # On-Chain Agent
    # -------------------------------------------------------------------------
    
    def analyze_onchain(
        self,
        symbol: str,
        network: str = "mainnet"
    ) -> Dict[str, Any]:
        """
        Analyze on-chain blockchain metrics.
        
        Args:
            symbol: Crypto symbol (e.g., "BTC", "ETH")
            network: Network (mainnet, testnet)
            
        Returns:
            On-chain metrics and analysis
        """
        url = self._build_url("onchain", "/analyze")
        data = {"symbol": symbol, "network": network}
        return self._make_request("POST", url, json=data)
    
    def get_whale_alerts(self) -> Dict[str, Any]:
        """
        Get recent whale transaction alerts from on-chain data.
        
        Returns:
            Recent large transactions
        """
        url = self._build_url("onchain", "/whale-alerts")
        return self._make_request("GET", url)
    
    # -------------------------------------------------------------------------
    # Macro Economics Agent
    # -------------------------------------------------------------------------
    
    def get_macro_data(
        self,
        indicators: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Get macroeconomic indicators.
        
        Args:
            indicators: Economic indicators (gdp, inflation, interest_rate, etc.)
            
        Returns:
            Macroeconomic data and analysis
        """
        if indicators is None:
            indicators = ["gdp", "inflation", "interest_rate"]
            
        url = self._build_url("macro_economics", "/indicators")
        data = {"indicators": indicators}
        return self._make_request("POST", url, json=data)
    
    def analyze_fed_events(self) -> Dict[str, Any]:
        """
        Analyze Federal Reserve events and their market impact.
        
        Returns:
            Fed events analysis
        """
        url = self._build_url("macro_economics", "/fed-events")
        return self._make_request("GET", url)
    
    # -------------------------------------------------------------------------
    # Portfolio Optimizer Agent
    # -------------------------------------------------------------------------
    
    def optimize_portfolio(
        self,
        holdings: Dict[str, float],
        risk_tolerance: str = "moderate"
    ) -> Dict[str, Any]:
        """
        Optimize portfolio allocation.
        
        Args:
            holdings: Current holdings {symbol: amount}
            risk_tolerance: Risk level (conservative, moderate, aggressive)
            
        Returns:
            Optimized portfolio allocation recommendations
        """
        url = self._build_url("portfolio_optimizer", "/optimize")
        data = {
            "holdings": holdings,
            "risk_tolerance": risk_tolerance
        }
        return self._make_request("POST", url, json=data)
    
    def calculate_risk(self, holdings: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculate portfolio risk metrics.
        
        Args:
            holdings: Current holdings {symbol: amount}
            
        Returns:
            Risk metrics (VaR, Sharpe ratio, volatility, etc.)
        """
        url = self._build_url("portfolio_optimizer", "/risk")
        data = {"holdings": holdings}
        return self._make_request("POST", url, json=data)
    
    # -------------------------------------------------------------------------
    # Convenience Methods
    # -------------------------------------------------------------------------
    
    def complete_analysis(
        self,
        symbol: str,
        asset_type: str = "crypto"
    ) -> Dict[str, Any]:
        """
        Run complete analysis using multiple agents.
        
        Args:
            symbol: Symbol to analyze
            asset_type: Asset type (crypto, stock)
            
        Returns:
            Aggregated analysis from multiple agents
        """
        results = {
            "symbol": symbol,
            "asset_type": asset_type,
            "timestamp": datetime.utcnow().isoformat(),
            "analysis": {}
        }
        
        # Get market analysis
        if asset_type == "crypto":
            results["analysis"]["market"] = self.analyze_crypto(symbol)
            results["analysis"]["onchain"] = self.analyze_onchain(symbol.split("/")[0])
        elif asset_type == "stock":
            results["analysis"]["market"] = self.analyze_stock(symbol)
        
        # Get sentiment analysis
        results["analysis"]["sentiment"] = self.analyze_sentiment(symbol.split("/")[0])
        
        # Get news
        results["analysis"]["news"] = self.get_news([asset_type, symbol.split("/")[0]], max_items=5)
        
        return results


# Global instance
_agent_client = None


def get_agent_client() -> AgentClient:
    """Get or create global agent client instance."""
    global _agent_client
    if _agent_client is None:
        base_url = os.getenv("AGENT_BASE_URL", "http://localhost")
        _agent_client = AgentClient(base_url)
    return _agent_client
