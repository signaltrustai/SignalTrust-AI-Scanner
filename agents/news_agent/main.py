"""
SignalTrust Market News Agent EU
Aggregates and analyzes market news
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
from typing import Optional, Dict, Any, List
from datetime import datetime

app = FastAPI(title="SignalTrust Market News EU", version="1.0.0")


class LLM:
    """Wrapper for OpenAI LLM for news analysis"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")
        
    def run(self, prompt: str, output_format: str = "list") -> Dict[str, Any]:
        """Run LLM inference"""
        if not self.api_key:
            return self._mock_response(prompt)
            
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a financial news analyst. Respond in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            if output_format in ["json", "list"]:
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
            "insights": [
                "Market sentiment is bullish with increased institutional interest",
                "Federal Reserve policy remains accommodative, supporting risk assets",
                "Crypto regulation discussions heating up in major economies",
                "Technology sector showing strong earnings growth",
                "Energy sector volatile due to geopolitical tensions"
            ]
        }


class NewsCatcher:
    """News aggregation client"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        
    def search(self, topics: List[str], page_size: int = 10) -> List[Dict]:
        """Search for news articles"""
        try:
            # Mock news data
            articles = []
            for i, topic in enumerate(topics):
                for j in range(min(page_size // len(topics), 5)):
                    articles.append({
                        "title": f"Breaking: {topic.capitalize()} Market Update {j+1}",
                        "summary": f"Latest developments in {topic} market showing significant movement. Analysts predict continued volatility as investors digest recent economic data.",
                        "url": f"https://example.com/news/{topic}-{j+1}",
                        "published": datetime.now().isoformat(),
                        "source": "Financial Times",
                        "impact_score": 0.7 + i * 0.05
                    })
            return articles
            
        except Exception as e:
            print(f"API error: {e}")
            return []


class NewsRequest(BaseModel):
    topics: List[str]
    max_items: int = 10


# Initialize components
nc = NewsCatcher(api_key=os.getenv("NEWS_CATCHER_API_KEY"))
llm = LLM(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "SignalTrust Market News EU",
        "status": "online",
        "version": "1.0.0"
    }


@app.post("/news")
async def get_news(request: NewsRequest):
    """
    Get and analyze market news
    
    Args:
        topics: List of topics to search for (e.g., ["crypto", "stocks", "forex"])
        max_items: Maximum number of articles to return
    
    Returns:
        JSON with articles and AI-powered insights
    """
    try:
        topics = request.topics
        max_items = request.max_items
        
        # Fetch articles
        articles = nc.search(topics=topics, page_size=max_items)
        
        # Concatenate article summaries
        corpus = "\n\n".join([a["summary"] for a in articles])
        
        # Create analysis prompt
        prompt = f"""Analyse les {len(articles)} articles ci-dessus et donne :
• Tendance générale du marché (bull/bear/neutral)
• Mots-clés récurrents (inflation, Fed, crypto-regulation…)
• Impact potentiel sur les actifs de SignalTrust EU (crypto, actions).
Résume en 5 bullet-points.

Articles:
{corpus}

Réponds avec un array JSON de 5 strings (insights).
"""
        
        # Get LLM insights
        insights = llm.run(prompt, output_format="list")
        
        # Ensure insights is a list
        if isinstance(insights, dict):
            insights = insights.get("insights", [insights.get("response", "")])
        elif not isinstance(insights, list):
            insights = [str(insights)]
        
        return {
            "insights": insights,
            "articles": articles,
            "topics": topics,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "news_agent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
