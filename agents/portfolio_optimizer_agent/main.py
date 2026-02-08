"""
Portfolio Optimizer Agent
Dynamic position sizing using Kelly Criterion, risk parity, and mean-variance optimization
Converts trading signals into optimal portfolio allocations
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from datetime import datetime, timezone
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Portfolio Optimizer Agent",
    description="Optimal portfolio allocation and position sizing",
    version="1.0.0"
)

class PortfolioRequest(BaseModel):
    """Request model for portfolio optimization"""
    signals: List[Dict]  # List of trading signals with scores
    total_capital: float  # Total capital to allocate
    method: str = "kelly"  # kelly, risk_parity, mean_variance
    risk_tolerance: float = 0.5  # 0-1 scale
    max_position_size: float = 0.25  # Max 25% per position

class PortfolioResponse(BaseModel):
    """Response model for optimized portfolio"""
    timestamp: str
    method: str
    total_capital: float
    allocations: List[Dict]
    risk_metrics: Dict
    expected_return: float
    expected_volatility: float
    sharpe_ratio: float
    recommendations: List[str]

class PortfolioOptimizer:
    """
    Optimizes portfolio allocation based on trading signals
    """
    
    def __init__(self):
        self.default_risk_free_rate = 0.05  # 5% risk-free rate
        
    async def optimize(self, signals: List[Dict], capital: float,
                      method: str, risk_tolerance: float,
                      max_position: float) -> PortfolioResponse:
        """
        Optimize portfolio allocation
        
        Args:
            signals: List of trading signals
            capital: Total capital
            method: Optimization method
            risk_tolerance: Risk tolerance (0-1)
            max_position: Maximum position size (0-1)
            
        Returns:
            PortfolioResponse with optimal allocations
        """
        logger.info(f"Optimizing portfolio: {len(signals)} signals, ${capital:,.0f}")
        
        # Calculate allocations based on method
        if method == "kelly":
            allocations = self._kelly_criterion(signals, capital, max_position)
        elif method == "risk_parity":
            allocations = self._risk_parity(signals, capital, max_position)
        elif method == "mean_variance":
            allocations = self._mean_variance(signals, capital, risk_tolerance, max_position)
        else:
            allocations = self._equal_weight(signals, capital, max_position)
        
        # Calculate risk metrics
        risk_metrics = self._calculate_risk_metrics(allocations)
        
        # Calculate expected return and volatility
        exp_return = self._expected_return(allocations)
        exp_vol = self._expected_volatility(allocations)
        
        # Calculate Sharpe ratio
        sharpe = (exp_return - self.default_risk_free_rate) / exp_vol if exp_vol > 0 else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            allocations, risk_metrics, sharpe
        )
        
        return PortfolioResponse(
            timestamp=datetime.now(timezone.utc).isoformat(),
            method=method,
            total_capital=capital,
            allocations=allocations,
            risk_metrics=risk_metrics,
            expected_return=round(exp_return, 4),
            expected_volatility=round(exp_vol, 4),
            sharpe_ratio=round(sharpe, 3),
            recommendations=recommendations
        )
    
    def _kelly_criterion(self, signals: List[Dict], capital: float,
                        max_position: float) -> List[Dict]:
        """
        Kelly Criterion position sizing
        
        Kelly% = (p * odds - (1 - p)) / odds
        where p = probability of win, odds = win/loss ratio
        """
        allocations = []
        
        for signal in signals:
            symbol = signal.get("symbol", "UNKNOWN")
            score = signal.get("score", 0.5)  # 0-1 probability
            win_loss_ratio = signal.get("win_loss_ratio", 2.0)  # Expected win/loss
            
            # Kelly percentage
            p_win = score
            odds = win_loss_ratio
            kelly_pct = (p_win * odds - (1 - p_win)) / odds
            
            # Apply safety factor (half Kelly)
            kelly_pct = kelly_pct * 0.5
            
            # Cap at max position
            kelly_pct = max(0, min(kelly_pct, max_position))
            
            allocation = capital * kelly_pct
            
            if allocation > 0:
                allocations.append({
                    "symbol": symbol,
                    "weight": round(kelly_pct, 4),
                    "allocation": round(allocation, 2),
                    "signal_score": score,
                    "method": "kelly"
                })
        
        return allocations
    
    def _risk_parity(self, signals: List[Dict], capital: float,
                    max_position: float) -> List[Dict]:
        """
        Risk Parity allocation
        Equal risk contribution from each asset
        """
        allocations = []
        
        # Calculate risk for each signal
        risks = []
        for signal in signals:
            volatility = signal.get("volatility", 0.2)  # Default 20% vol
            risks.append(volatility)
        
        # Inverse volatility weighting
        inv_risks = [1/r if r > 0 else 0 for r in risks]
        total_inv_risk = sum(inv_risks)
        
        for i, signal in enumerate(signals):
            if total_inv_risk > 0:
                weight = (inv_risks[i] / total_inv_risk)
                weight = min(weight, max_position)
                
                allocation = capital * weight
                
                if allocation > 0:
                    allocations.append({
                        "symbol": signal.get("symbol", "UNKNOWN"),
                        "weight": round(weight, 4),
                        "allocation": round(allocation, 2),
                        "signal_score": signal.get("score", 0.5),
                        "volatility": signal.get("volatility", 0.2),
                        "method": "risk_parity"
                    })
        
        return allocations
    
    def _mean_variance(self, signals: List[Dict], capital: float,
                      risk_tolerance: float, max_position: float) -> List[Dict]:
        """
        Mean-Variance Optimization (simplified)
        Maximize Sharpe ratio given risk tolerance
        """
        allocations = []
        
        for signal in signals:
            symbol = signal.get("symbol", "UNKNOWN")
            expected_return = signal.get("expected_return", 0.1)
            volatility = signal.get("volatility", 0.2)
            score = signal.get("score", 0.5)
            
            # Weight by Sharpe ratio and signal score
            sharpe = (expected_return - self.default_risk_free_rate) / volatility if volatility > 0 else 0
            
            # Adjust by risk tolerance
            weight = sharpe * risk_tolerance * score
            weight = max(0, min(weight / 10, max_position))  # Normalize
            
            allocation = capital * weight
            
            if allocation > 0:
                allocations.append({
                    "symbol": symbol,
                    "weight": round(weight, 4),
                    "allocation": round(allocation, 2),
                    "signal_score": score,
                    "expected_return": expected_return,
                    "volatility": volatility,
                    "sharpe": round(sharpe, 3),
                    "method": "mean_variance"
                })
        
        return allocations
    
    def _equal_weight(self, signals: List[Dict], capital: float,
                     max_position: float) -> List[Dict]:
        """Equal weight allocation (baseline)"""
        n = len(signals)
        if n == 0:
            return []
        
        weight = min(1.0 / n, max_position)
        
        allocations = []
        for signal in signals:
            allocation = capital * weight
            allocations.append({
                "symbol": signal.get("symbol", "UNKNOWN"),
                "weight": round(weight, 4),
                "allocation": round(allocation, 2),
                "signal_score": signal.get("score", 0.5),
                "method": "equal_weight"
            })
        
        return allocations
    
    def _calculate_risk_metrics(self, allocations: List[Dict]) -> Dict:
        """Calculate portfolio risk metrics"""
        if not allocations:
            return {"var_95": 0, "cvar_95": 0, "max_drawdown": 0}
        
        # Simplified risk calculation
        total_weight = sum(a["weight"] for a in allocations)
        avg_vol = np.mean([a.get("volatility", 0.2) for a in allocations])
        
        # VaR (Value at Risk) - 95% confidence
        var_95 = 1.65 * avg_vol * np.sqrt(total_weight)
        
        # CVaR (Conditional VaR)
        cvar_95 = var_95 * 1.3
        
        # Estimated max drawdown
        max_drawdown = avg_vol * 2.5
        
        return {
            "var_95": round(var_95, 4),
            "cvar_95": round(cvar_95, 4),
            "max_drawdown_est": round(max_drawdown, 4),
            "portfolio_volatility": round(avg_vol, 4)
        }
    
    def _expected_return(self, allocations: List[Dict]) -> float:
        """Calculate expected portfolio return"""
        if not allocations:
            return 0.0
        
        total_return = 0.0
        for alloc in allocations:
            weight = alloc["weight"]
            exp_return = alloc.get("expected_return", 0.1)
            total_return += weight * exp_return
        
        return total_return
    
    def _expected_volatility(self, allocations: List[Dict]) -> float:
        """Calculate expected portfolio volatility (simplified)"""
        if not allocations:
            return 0.0
        
        # Simplified: weighted average volatility
        total_vol = 0.0
        for alloc in allocations:
            weight = alloc["weight"]
            vol = alloc.get("volatility", 0.2)
            total_vol += weight * vol
        
        return total_vol
    
    def _generate_recommendations(self, allocations: List[Dict],
                                 risk_metrics: Dict, sharpe: float) -> List[str]:
        """Generate portfolio recommendations"""
        recommendations = []
        
        # Check concentration
        max_weight = max([a["weight"] for a in allocations]) if allocations else 0
        if max_weight > 0.4:
            recommendations.append("⚠️ High concentration risk - largest position exceeds 40%")
        
        # Check Sharpe ratio
        if sharpe > 2.0:
            recommendations.append("✅ Excellent risk-adjusted returns (Sharpe > 2)")
        elif sharpe < 1.0:
            recommendations.append("⚠️ Low risk-adjusted returns (Sharpe < 1) - reconsider allocations")
        
        # Check diversification
        if len(allocations) < 3:
            recommendations.append("Consider adding more positions for diversification")
        
        # VaR warning (var_95 is a proportion 0-1 representing percentage loss)
        var_95 = risk_metrics.get("var_95", 0)
        if var_95 > 0.3:  # 30% VaR is very high
            recommendations.append(f"High VaR at {var_95:.1%} - potential for large losses")
        
        return recommendations or ["Portfolio allocation looks reasonable"]

# Initialize optimizer
optimizer = PortfolioOptimizer()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "portfolio_optimizer",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/optimize", response_model=PortfolioResponse)
async def optimize_portfolio(request: PortfolioRequest):
    """
    Optimize portfolio allocation
    
    Example:
    ```json
    {
        "signals": [
            {"symbol": "BTC", "score": 0.85, "expected_return": 0.3, "volatility": 0.4},
            {"symbol": "ETH", "score": 0.75, "expected_return": 0.25, "volatility": 0.35}
        ],
        "total_capital": 100000,
        "method": "kelly",
        "risk_tolerance": 0.5,
        "max_position_size": 0.25
    }
    ```
    """
    try:
        result = await optimizer.optimize(
            request.signals,
            request.total_capital,
            request.method,
            request.risk_tolerance,
            request.max_position_size
        )
        return result
    except Exception as e:
        logger.error(f"Error optimizing portfolio: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/methods")
async def get_methods():
    """Get available optimization methods"""
    return {
        "methods": [
            {
                "name": "kelly",
                "description": "Kelly Criterion - maximize long-term growth",
                "best_for": "High confidence signals with known win/loss ratios"
            },
            {
                "name": "risk_parity",
                "description": "Equal risk contribution from each asset",
                "best_for": "Diversified portfolios with different volatilities"
            },
            {
                "name": "mean_variance",
                "description": "Markowitz mean-variance optimization",
                "best_for": "Balancing return and risk based on tolerance"
            },
            {
                "name": "equal_weight",
                "description": "Simple equal weighting",
                "best_for": "Baseline comparison"
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
