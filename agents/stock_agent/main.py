"""
SignalTrust Stock Market Analyst Agent EU
Based on Stock-GPT architecture for stock market analysis
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
from typing import Optional, Dict, Any
import pandas as pd
import requests
from datetime import datetime, timedelta

app = FastAPI(title="SignalTrust Stock Analyst EU", version="1.0.0")


class StockLLM:
    """Wrapper for OpenAI LLM for stock analysis"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        
    def run(self, prompt: str, output_format: str = "json") -> Dict[str, Any]:
        """Run LLM inference"""
        if not self.api_key:
            return self._mock_response(prompt)
            
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a stock market analyst. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            if output_format == "json":
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    if "```json" in content:
                        content = content.split("```json")[1].split("```")[0].strip()
                        return json.loads(content)
                    elif "```" in content:
                        content = content.split("```")[1].split("```")[0].strip()
                        return json.loads(content)
                    return {"response": content}
            return {"response": content}
            
        except Exception as e:
            print(f"LLM error: {e}")
            return self._mock_response(prompt)
    
    def _mock_response(self, prompt: str) -> Dict[str, Any]:
        """Mock response when API key is not available"""
        return {
            "current_price": "175.50",
            "volatility_30d": "18.5%",
            "sentiment": "positive",
            "technical_points": ["Support at $170", "Resistance at $185", "RSI showing bullish divergence"],
            "recommendation": "Buy",
            "confidence": 0.78,
            "price_targets": {
                "7d": {"price": "182.00", "probability": 0.72},
                "30d": {"price": "195.00", "probability": 0.65}
            },
            "note": "Mock response - configure OPENAI_API_KEY for real analysis"
        }


class PriceFetcher:
    """Fetch stock market data"""
    
    def __init__(self, key: Optional[str] = None):
        self.api_key = key
        
    def get_daily(self, ticker: str, outputsize: str = "compact") -> pd.DataFrame:
        """Fetch daily stock data"""
        try:
            # Mock data for demonstration
            dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
            data = {
                'date': dates,
                'open': [175.0 + i * 0.5 for i in range(100)],
                'high': [177.0 + i * 0.5 for i in range(100)],
                'low': [173.0 + i * 0.5 for i in range(100)],
                'close': [175.5 + i * 0.5 for i in range(100)],
                'volume': [50000000 + i * 10000 for i in range(100)]
            }
            
            df = pd.DataFrame(data)
            return df
            
        except Exception as e:
            print(f"Data fetch error: {e}")
            return pd.DataFrame({
                'date': [datetime.now()],
                'open': [175.0],
                'high': [177.0],
                'low': [173.0],
                'close': [175.5],
                'volume': [50000000]
            })


class PredictRequest(BaseModel):
    ticker: str


# Initialize components
llm = StockLLM(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
price_fetcher = PriceFetcher(key=os.getenv("ALPHAVANTAGE_API_KEY"))


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "SignalTrust Stock Analyst EU",
        "status": "online",
        "version": "1.0.0"
    }


@app.post("/predict")
async def predict(request: PredictRequest):
    """
    Analyze a stock ticker and provide predictions
    
    Args:
        ticker: Stock ticker symbol (e.g., "AAPL", "GOOGL")
    
    Returns:
        JSON with analysis, sentiment, recommendation, and price targets
    """
    try:
        ticker = request.ticker
        
        # Fetch daily data
        df = price_fetcher.get_daily(ticker, outputsize="compact")
        
        # Create analysis prompt
        prompt = f"""Donne une analyse détaillée du ticker {ticker}:
• Prix actuel, volatilité 30 j
• SAO (Sentiment Analystique Ø) via news & earnings
• Points de retournement technique
• Recommandation (Buy/Hold/Sell) avec cible prix (7 j, 30 j)
Donne un score de confiance (0-1). Données courtes :
{df.tail(10).to_json(orient='records')}

Réponds en JSON avec les champs: current_price, volatility_30d, sentiment, technical_points (array), recommendation, confidence, price_targets (avec 7d et 30d, chacun ayant price et probability).
"""
        
        # Get LLM response
        response = llm.run(prompt, output_format="json")
        
        # Add metadata
        response["ticker"] = ticker
        response["timestamp"] = datetime.now().isoformat()
        response["data_points"] = len(df)
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "stock_agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
