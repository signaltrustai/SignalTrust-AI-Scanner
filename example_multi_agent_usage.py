"""
Example: Using the SignalTrust EU Multi-Agent System
This script demonstrates how to interact with the multi-agent system
"""

import requests
import json
from typing import Dict, Any


class SignalTrustEUClient:
    """Client for interacting with SignalTrust EU Multi-Agent System"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        
    def get_agents(self) -> Dict[str, Any]:
        """List all available agents"""
        response = requests.get(f"{self.base_url}/agents")
        return response.json()
    
    def run_workflow(
        self, 
        symbol: str = "BTC/USDT",
        ticker: str = "AAPL",
        network: str = "btc",
        topics: list = None
    ) -> Dict[str, Any]:
        """Run the complete market analysis workflow"""
        if topics is None:
            topics = ["crypto", "stocks", "market"]
            
        data = {
            "symbol": symbol,
            "ticker": ticker,
            "network": network,
            "topics": topics
        }
        
        response = requests.post(
            f"{self.base_url}/run-workflow",
            json=data,
            timeout=60
        )
        return response.json()
    
    def analyze_crypto(self, symbol: str) -> Dict[str, Any]:
        """Analyze a cryptocurrency"""
        response = requests.post(
            "http://localhost:8001/predict",
            json={"symbol": symbol}
        )
        return response.json()
    
    def analyze_stock(self, ticker: str) -> Dict[str, Any]:
        """Analyze a stock"""
        response = requests.post(
            "http://localhost:8002/predict",
            json={"ticker": ticker}
        )
        return response.json()
    
    def watch_whales(self, network: str = "btc", min_usd: int = 5_000_000) -> Dict[str, Any]:
        """Monitor whale transactions"""
        response = requests.get(
            f"http://localhost:8003/whales",
            params={"network": network, "min_usd": min_usd}
        )
        return response.json()
    
    def get_news(self, topics: list, max_items: int = 10) -> Dict[str, Any]:
        """Get and analyze market news"""
        response = requests.post(
            "http://localhost:8004/news",
            json={"topics": topics, "max_items": max_items}
        )
        return response.json()


def print_section(title: str):
    """Print a section header"""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def main():
    """Main example function"""
    
    # Initialize client
    client = SignalTrustEUClient()
    
    print_section("SignalTrust EU Multi-Agent System - Example")
    
    # 1. List available agents
    print_section("1. Available Agents")
    try:
        agents = client.get_agents()
        print(f"Found {len(agents.get('agents', []))} agents:")
        for agent in agents.get('agents', []):
            print(f"  • {agent['name']}: {agent['role']}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 2. Analyze cryptocurrency
    print_section("2. Crypto Analysis (BTC/USDT)")
    try:
        crypto_result = client.analyze_crypto("BTC/USDT")
        print(json.dumps(crypto_result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # 3. Analyze stock
    print_section("3. Stock Analysis (AAPL)")
    try:
        stock_result = client.analyze_stock("AAPL")
        print(json.dumps(stock_result, indent=2))
    except Exception as e:
        print(f"Error: {e}")
    
    # 4. Watch whale transactions
    print_section("4. Whale Watching (BTC)")
    try:
        whale_result = client.watch_whales("btc", 5_000_000)
        print(f"Monitoring {whale_result.get('summary', {}).get('transaction_count', 0)} transactions")
        print(f"Pattern: {whale_result.get('summary', {}).get('pattern', 'N/A')}")
        print(f"Risk Score: {whale_result.get('summary', {}).get('risk_score', 'N/A')}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 5. Get market news
    print_section("5. Market News")
    try:
        news_result = client.get_news(["crypto", "technology", "market"], 5)
        print(f"Found {len(news_result.get('articles', []))} articles")
        print("\nKey Insights:")
        for insight in news_result.get('insights', [])[:3]:
            print(f"  • {insight}")
    except Exception as e:
        print(f"Error: {e}")
    
    # 6. Run complete workflow
    print_section("6. Complete Market Analysis Workflow")
    try:
        workflow_result = client.run_workflow(
            symbol="ETH/USDT",
            ticker="GOOGL",
            network="eth",
            topics=["cryptocurrency", "technology", "AI"]
        )
        
        print(f"Workflow: {workflow_result.get('workflow', 'N/A')}")
        print(f"Status: {workflow_result.get('status', 'N/A')}")
        print(f"Confidence: {workflow_result.get('confidence', 0) * 100:.1f}%")
        
        print("\nAgent Results:")
        for agent_name, result in workflow_result.get('results', {}).items():
            status = result.get('status', 'unknown')
            symbol = "✅" if status == "success" else "❌"
            print(f"  {symbol} {agent_name}: {status}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    print_section("Example Complete")
    print("For more information, see: MULTI_AGENT_SYSTEM.md\n")


if __name__ == "__main__":
    main()
