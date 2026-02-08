"""
SignalTrust Coordinator Agent EU
Based on CrewAI for multi-agent orchestration
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import json
import requests
from typing import Dict, Any, List, Optional
from datetime import datetime

app = FastAPI(title="SignalTrust Coordinator EU", version="1.0.0")


class Agent:
    """Represents an agent in the system"""
    
    def __init__(self, name: str, role: str, url: str, task: str):
        self.name = name
        self.role = role
        self.url = url
        self.task = task
    
    def execute(self, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Execute the agent's task"""
        try:
            if "GET" in self.task:
                # Parse GET request
                endpoint = self.task.split("GET ")[1]
                if params:
                    endpoint = endpoint.format(**params)
                response = requests.get(f"{self.url}{endpoint}", timeout=30)
            else:
                # Parse POST request
                endpoint = self.task.split("POST ")[1]
                response = requests.post(f"{self.url}{endpoint}", json=params, timeout=30)
            
            if response.status_code == 200:
                return {
                    "status": "success",
                    "agent": self.name,
                    "data": response.json()
                }
            else:
                return {
                    "status": "error",
                    "agent": self.name,
                    "error": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            return {
                "status": "error",
                "agent": self.name,
                "error": str(e)
            }


class Workflow:
    """Orchestrates multiple agents"""
    
    def __init__(self, name: str, description: str, agents: List[Agent]):
        self.name = name
        self.description = description
        self.agents = agents
        
    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the workflow"""
        results = {}
        
        for agent in self.agents:
            print(f"Executing agent: {agent.name}")
            result = agent.execute(params.get(agent.name, {}))
            results[agent.name] = result
        
        # Aggregate results
        all_data = {}
        for agent_name, result in results.items():
            if result["status"] == "success":
                all_data[agent_name] = result["data"]
        
        # Calculate confidence score
        success_count = sum(1 for r in results.values() if r["status"] == "success")
        confidence = success_count / len(self.agents) if self.agents else 0
        
        return {
            "workflow": self.name,
            "status": "completed",
            "confidence": confidence,
            "results": results,
            "aggregated_data": all_data,
            "timestamp": datetime.now().isoformat()
        }


# Define agents
crypto_analyst = Agent(
    name="crypto_analyst",
    role="Analyse le marché crypto",
    url="http://crypto_agent:8000",
    task="POST /predict"
)

stock_analyst = Agent(
    name="stock_analyst",
    role="Analyse le marché actions",
    url="http://stock_agent:8000",
    task="POST /predict"
)

whale_watcher = Agent(
    name="whale_watcher",
    role="Surveille les gros mouvements blockchain",
    url="http://whale_agent:8000",
    task="GET /whales"
)

news_agent = Agent(
    name="news_agent",
    role="Récupère et résume les dernières news",
    url="http://news_agent:8000",
    task="POST /news"
)

# Define workflow
market_pipeline = Workflow(
    name="signaltrust_market_pipeline_eu",
    description="Orchestration complète d'une analyse de marché quotidien",
    agents=[crypto_analyst, stock_analyst, whale_watcher, news_agent]
)


class WorkflowRequest(BaseModel):
    symbol: Optional[str] = "BTC/USDT"
    ticker: Optional[str] = "AAPL"
    network: Optional[str] = "btc"
    topics: Optional[List[str]] = ["crypto", "stocks"]


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "service": "SignalTrust Coordinator EU",
        "status": "online",
        "version": "1.0.0",
        "workflow": market_pipeline.name
    }


@app.post("/run-workflow")
async def run_workflow(request: WorkflowRequest):
    """
    Run the complete market analysis workflow
    
    Coordinates all agents to perform:
    - Crypto market analysis
    - Stock market analysis
    - Whale transaction monitoring
    - Market news aggregation
    
    Returns:
        Aggregated results from all agents with confidence score
    """
    try:
        # Prepare parameters for each agent
        params = {
            "crypto_analyst": {"symbol": request.symbol},
            "stock_analyst": {"ticker": request.ticker},
            "whale_watcher": {"network": request.network},
            "news_agent": {"topics": request.topics, "max_items": 10}
        }
        
        # Run workflow
        result = market_pipeline.run(params)
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Workflow failed: {str(e)}")


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "service": "coordinator"}


@app.get("/agents")
async def list_agents():
    """List all available agents"""
    return {
        "agents": [
            {
                "name": agent.name,
                "role": agent.role,
                "url": agent.url,
                "task": agent.task
            }
            for agent in market_pipeline.agents
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
