#!/usr/bin/env python3
"""
Example script demonstrating OpenAI integration with SignalTrust AI Scanner

This example shows how to:
1. Initialize the OpenAI client
2. Analyze market data
3. Get price predictions
4. Analyze whale transactions
5. Generate market summaries
"""

import os
from dotenv import load_dotenv
from asi1_integration import ASI1AIIntegration
import json

# Load environment variables from .env file
load_dotenv()

def main():
    """Main example function"""
    
    print("=" * 60)
    print("SignalTrust AI Scanner - OpenAI Integration Example")
    print("=" * 60)
    print()
    
    # Check if API key is configured
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print()
        print("Please create a .env file with your OpenAI API key:")
        print("  OPENAI_API_KEY=sk-proj-your-api-key-here")
        print()
        print("Get your API key from: https://platform.openai.com/api-keys")
        return
    
    print("✓ OpenAI API key found")
    print(f"✓ Using model: {os.getenv('OPENAI_MODEL', 'gpt-4')}")
    print()
    
    # Initialize AI integration
    ai = ASI1AIIntegration()
    
    # Example 1: Market Analysis
    print("=" * 60)
    print("Example 1: Market Analysis")
    print("=" * 60)
    
    market_data = {
        "symbol": "BTC",
        "price": 45000,
        "volume": 1000000000,
        "change_24h": 5.2,
        "market_cap": 880000000000,
        "trend": "bullish"
    }
    
    print(f"Analyzing market data for {market_data['symbol']}...")
    print(json.dumps(market_data, indent=2))
    print()
    
    result = ai.analyze_market_with_ai(market_data, context="Bitcoin 24h performance")
    
    if result['success']:
        print("✓ Analysis successful")
        print(f"Provider: {result.get('provider', 'N/A')}")
        print(f"Model: {result.get('model', 'N/A')}")
        print()
        print("AI Analysis:")
        print("-" * 60)
        print(result['analysis'])
    else:
        print(f"❌ Analysis failed: {result.get('error', 'Unknown error')}")
    
    print()
    
    # Example 2: Price Prediction
    print("=" * 60)
    print("Example 2: Price Prediction")
    print("=" * 60)
    
    historical_data = [
        {"timestamp": "2024-01-01T00:00:00", "price": 42000, "volume": 900000000},
        {"timestamp": "2024-01-02T00:00:00", "price": 43000, "volume": 950000000},
        {"timestamp": "2024-01-03T00:00:00", "price": 43500, "volume": 980000000},
        {"timestamp": "2024-01-04T00:00:00", "price": 44000, "volume": 1000000000},
        {"timestamp": "2024-01-05T00:00:00", "price": 45000, "volume": 1050000000},
    ]
    
    print(f"Predicting price movement for BTC...")
    print(f"Using {len(historical_data)} historical data points")
    print()
    
    prediction = ai.predict_price_movement("BTC", historical_data)
    
    if prediction['success']:
        print("✓ Prediction successful")
        print(f"Symbol: {prediction['symbol']}")
        print()
        print("Price Prediction:")
        print("-" * 60)
        print(prediction['prediction'])
    else:
        print(f"❌ Prediction failed: {prediction.get('error', 'Unknown error')}")
    
    print()
    
    # Example 3: Whale Transaction Analysis
    print("=" * 60)
    print("Example 3: Whale Transaction Analysis")
    print("=" * 60)
    
    whale_data = {
        "transaction_hash": "0x123abc...def456",
        "amount": 1000,
        "value_usd": 45000000,
        "from_address": "0xabc...def (Unknown Whale)",
        "to_address": "0xdef...ghi (Binance)",
        "timestamp": "2024-01-05T12:00:00",
        "asset": "BTC"
    }
    
    print("Analyzing whale transaction...")
    print(json.dumps(whale_data, indent=2))
    print()
    
    whale_analysis = ai.whale_watch_analysis(whale_data)
    
    if whale_analysis['success']:
        print("✓ Analysis successful")
        print(f"Alert Level: {whale_analysis['alert_level'].upper()}")
        print()
        print("Whale Analysis:")
        print("-" * 60)
        print(whale_analysis['whale_analysis'])
    else:
        print(f"❌ Analysis failed: {whale_analysis.get('error', 'Unknown error')}")
    
    print()
    
    # Example 4: Market Summary
    print("=" * 60)
    print("Example 4: Comprehensive Market Summary")
    print("=" * 60)
    
    all_markets = {
        "crypto": {
            "BTC": {"price": 45000, "change_24h": 5.2},
            "ETH": {"price": 2500, "change_24h": 3.8},
            "SOL": {"price": 100, "change_24h": 8.5}
        },
        "stocks": {
            "AAPL": {"price": 180, "change_24h": 1.2},
            "TSLA": {"price": 250, "change_24h": -2.5},
            "NVDA": {"price": 500, "change_24h": 4.8}
        }
    }
    
    print("Generating comprehensive market summary...")
    print()
    
    summary = ai.get_ai_market_summary(all_markets)
    
    if summary['success']:
        print("✓ Summary generated")
        print()
        print("Market Summary:")
        print("-" * 60)
        print(summary['summary'])
    else:
        print(f"❌ Summary failed: {summary.get('error', 'Unknown error')}")
    
    print()
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
