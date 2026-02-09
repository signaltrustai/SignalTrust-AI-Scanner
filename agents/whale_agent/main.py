"""
SignalTrust Whale Watcher Agent EU
Monitors large blockchain transactions
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
import random
from typing import Optional, Dict, Any, List
from datetime import datetime

app = FastAPI(title="SignalTrust Whale Watcher EU", version="1.0.0")


class Summarizer:
    """LLM-based transaction summarizer"""
    
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
                    {"role": "system", "content": "You are a blockchain analyst specializing in whale transactions. Respond in valid JSON format."},
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
            "pattern": "accumulation",
            "top_addresses": ["0x1234...5678", "0xabcd...ef90"],
            "total_volume": "$150,000,000",
            "risk_score": 0.45,
            "insights": [
                "Large institutional accumulation detected",
                "Multiple whale wallets showing similar patterns",
                "Potential bullish signal"
            ],
            "note": "Mock response - configure OPENAI_API_KEY and WHALEALERT_API_KEY for real analysis"
        }


class WhaleAlertClient:
    """Client for WhaleAlert API"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        
    def get_transactions(self, network: str = "btc", min_usd: int = 5_000_000, limit: int = 30) -> List[Dict]:
        """Fetch large transactions"""
        try:
            # Mock transaction data
            transactions = []
            for i in range(limit):
                transactions.append({
                    "hash": f"0x{random.randbytes(32).hex()}",
                    "from": f"0x{'1' * 40}",
                    "to": f"0x{'2' * 40}",
                    "amount": min_usd + i * 1000000,
                    "timestamp": int(datetime.now().timestamp()) - i * 3600,
                    "network": network.upper()
                })
            return transactions
            
        except Exception as e:
            print(f"API error: {e}")
            return []


# Initialize components
client = WhaleAlertClient(api_key=os.getenv("WHALEALERT_API_KEY"))
summarizer = Summarizer(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "SignalTrust Whale Watcher EU",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/whales")
async def recent_whales(network: str = "btc", min_usd: int = 5_000_000):
    """
    Get recent whale transactions and AI-powered analysis
    
    Args:
        network: Blockchain network (btc, eth, bnb, etc.)
        min_usd: Minimum transaction value in USD
    
    Returns:
        JSON with raw transactions and AI summary
    """
    try:
        # Fetch transactions
        raw = client.get_transactions(network=network, min_usd=min_usd, limit=30)
        
        # Create summary prompt
        prompt = f"""Voici les {len(raw)} plus grosses transactions {network.upper()} (>{min_usd:,}$). Résume
les adresses remettantes, les patterns (ex. : accumulation, distribution) et un score de risque.

Transactions:
{json.dumps(raw[:5], indent=2)}

Réponds en JSON avec les champs: pattern, top_addresses (array), total_volume, risk_score (0-1), insights (array de strings).
"""
        
        # Get LLM summary
        summary = summarizer.run(prompt, output_format="json")
        
        # Add metadata
        summary["network"] = network
        summary["timestamp"] = datetime.now().isoformat()
        summary["transaction_count"] = len(raw)
        
        return {
            "raw": raw,
            "summary": summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "whale_agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
