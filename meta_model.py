"""
Meta-Model Integration for SignalTrust AI
Combines LLM insights with ML ensemble for superior predictions

This module implements the hybrid approach:
1. LLM for reasoning and feature extraction
2. XGBoost/LightGBM for probability estimation
3. SHAP for explainability
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import json
import logging

# ML Libraries
try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    logging.warning("XGBoost not available. Install with: pip install xgboost")

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False
    logging.warning("LightGBM not available. Install with: pip install lightgbm")

try:
    import shap
    SHAP_AVAILABLE = True
except ImportError:
    SHAP_AVAILABLE = False
    logging.warning("SHAP not available. Install with: pip install shap")


class FeatureEngineer:
    """
    Feature engineering pipeline for trading signals
    Combines technical, fundamental, sentiment, and macro features
    """
    
    def __init__(self):
        self.feature_names = []
        self.scaler = None
        
    def extract_features(self, data: Dict) -> Dict[str, float]:
        """
        Extract and normalize features from raw data
        
        Args:
            data: Dictionary containing market data, sentiment, etc.
            
        Returns:
            Dictionary of engineered features
        """
        features = {}
        
        # Technical Features
        features["price_change_1h"] = data.get("price_change_1h", 0.0)
        features["price_change_24h"] = data.get("price_change_24h", 0.0)
        features["volume_change_24h"] = data.get("volume_change_24h", 0.0)
        features["rsi_14"] = data.get("rsi", 50.0) / 100.0  # Normalize to 0-1
        features["adx"] = data.get("adx", 0.0) / 100.0
        features["ema_cross"] = 1.0 if data.get("ema_cross", False) else 0.0
        features["macd_signal"] = data.get("macd_signal", 0.0)
        features["bollinger_position"] = data.get("bollinger_position", 0.5)
        
        # On-Chain Features (for crypto)
        features["whale_flow_24h"] = min(data.get("whale_flow", 0.0) / 1e7, 1.0)
        features["active_addresses"] = data.get("active_addresses_change", 0.0)
        features["token_age_consumed"] = data.get("token_age_consumed", 0.0)
        features["exchange_inflow"] = data.get("exchange_inflow", 0.0)
        features["exchange_outflow"] = data.get("exchange_outflow", 0.0)
        
        # Sentiment Features
        features["sentiment_score"] = (data.get("sentiment", 0.0) + 1) / 2  # [-1,1] -> [0,1]
        features["twitter_volume"] = min(data.get("twitter_volume", 0.0) / 1000, 1.0)
        features["reddit_mentions"] = min(data.get("reddit_mentions", 0.0) / 100, 1.0)
        features["news_impact"] = data.get("news_impact_score", 0.0)
        features["social_trend"] = data.get("social_trend", 0.0)
        
        # Macro Features
        features["fed_rate"] = data.get("fed_rate", 5.0) / 10.0  # Normalize
        features["cpi_trend"] = data.get("cpi_trend", 0.0)
        features["unemployment"] = data.get("unemployment", 4.0) / 10.0
        features["macro_event"] = 1.0 if data.get("macro_event", False) else 0.0
        
        # LLM-Extracted Features
        features["fundamentals_score"] = data.get("fundamentals_score", 0.5)
        features["llm_confidence"] = data.get("llm_confidence", 0.5)
        features["pattern_strength"] = data.get("pattern_strength", 0.0)
        
        # Volatility Features
        features["volatility_1w"] = data.get("volatility_1w", 0.0)
        features["volatility_1m"] = data.get("volatility_1m", 0.0)
        features["atr"] = data.get("atr", 0.0)
        
        return features
    
    def get_feature_vector(self, features: Dict[str, float]) -> np.ndarray:
        """Convert feature dict to numpy array in consistent order"""
        if not self.feature_names:
            self.feature_names = sorted(features.keys())
        return np.array([features.get(name, 0.0) for name in self.feature_names])


class MetaModel:
    """
    Meta-model that combines LLM insights with ML predictions
    Uses ensemble of XGBoost and LightGBM
    """
    
    def __init__(self, model_type: str = "xgboost"):
        """
        Initialize meta-model
        
        Args:
            model_type: "xgboost", "lightgbm", or "ensemble"
        """
        self.model_type = model_type
        self.model = None
        self.feature_engineer = FeatureEngineer()
        self.explainer = None
        self.is_trained = False
        
        # Model hyperparameters
        self.xgb_params = {
            'n_estimators': 1000,
            'learning_rate': 0.01,
            'max_depth': 7,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'eval_metric': 'auc',
            'early_stopping_rounds': 50,
            'random_state': 42
        }
        
        self.lgb_params = {
            'n_estimators': 1000,
            'learning_rate': 0.01,
            'max_depth': 7,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'metric': 'auc',
            'early_stopping_rounds': 50,
            'random_state': 42
        }
    
    def train(self, X_train: pd.DataFrame, y_train: pd.Series,
              X_val: Optional[pd.DataFrame] = None,
              y_val: Optional[pd.Series] = None):
        """
        Train the meta-model
        
        Args:
            X_train: Training features
            y_train: Training labels (0/1 for breakout)
            X_val: Validation features (optional)
            y_val: Validation labels (optional)
        """
        if self.model_type == "xgboost" and XGBOOST_AVAILABLE:
            self.model = xgb.XGBClassifier(**self.xgb_params)
            
            if X_val is not None and y_val is not None:
                eval_set = [(X_val, y_val)]
                self.model.fit(X_train, y_train, eval_set=eval_set, verbose=False)
            else:
                self.model.fit(X_train, y_train)
                
        elif self.model_type == "lightgbm" and LIGHTGBM_AVAILABLE:
            self.model = lgb.LGBMClassifier(**self.lgb_params)
            
            if X_val is not None and y_val is not None:
                eval_set = [(X_val, y_val)]
                self.model.fit(X_train, y_train, eval_set=eval_set, verbose=False)
            else:
                self.model.fit(X_train, y_train)
        else:
            logging.error(f"Model type {self.model_type} not available")
            return
        
        self.is_trained = True
        
        # Initialize SHAP explainer
        if SHAP_AVAILABLE:
            self.explainer = shap.TreeExplainer(self.model)
    
    def predict_proba(self, features: Dict) -> float:
        """
        Predict probability of breakout
        
        Args:
            features: Feature dictionary
            
        Returns:
            Probability (0-1)
        """
        if not self.is_trained:
            logging.warning("Model not trained, returning default probability")
            return 0.5
        
        # Engineer features
        engineered = self.feature_engineer.extract_features(features)
        feature_vector = self.feature_engineer.get_feature_vector(engineered)
        
        # Reshape for prediction
        X = feature_vector.reshape(1, -1)
        
        # Get probability
        prob = self.model.predict_proba(X)[0, 1]
        
        return float(prob)
    
    def explain_prediction(self, features: Dict) -> Dict[str, float]:
        """
        Get SHAP values explaining the prediction
        
        Args:
            features: Feature dictionary
            
        Returns:
            Dictionary mapping feature names to contributions
        """
        if not SHAP_AVAILABLE or self.explainer is None:
            return {"note": "SHAP not available"}
        
        # Engineer features
        engineered = self.feature_engineer.extract_features(features)
        feature_vector = self.feature_engineer.get_feature_vector(engineered)
        
        # Calculate SHAP values
        X = feature_vector.reshape(1, -1)
        shap_values = self.explainer.shap_values(X)
        
        # Convert to dictionary
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # For binary classification
        
        explanation = {}
        for name, value in zip(self.feature_engineer.feature_names, shap_values[0]):
            explanation[name] = float(value)
        
        return explanation


class BreakoutScorer:
    """
    Calculate breakout score using multi-signal convergence
    """
    
    def __init__(self):
        self.weights = {
            "momentum": 0.25,
            "onchain_flow": 0.25,
            "sentiment": 0.20,
            "macro": 0.15,
            "news_impact": 0.15,
        }
    
    def calculate_score(self, features: Dict) -> float:
        """
        Calculate breakout score from features
        
        Args:
            features: Feature dictionary
            
        Returns:
            Score 0-1 (threshold: 0.73 for "Strong Breakout")
        """
        # Momentum component
        rsi = features.get("rsi", 50.0) / 100.0
        adx = features.get("adx", 0.0) / 100.0
        ema_cross = 1.0 if features.get("ema_cross", False) else 0.0
        momentum = rsi * adx * ema_cross
        
        # On-chain flow component
        whale_flow = min(features.get("whale_flow", 0.0) / 1e7, 1.0)
        
        # Sentiment component
        sentiment_raw = features.get("sentiment", 0.0)
        sentiment = (sentiment_raw + 1) / 2  # [-1,1] -> [0,1]
        
        # Macro component
        macro_event = 1.0 if features.get("macro_event", False) else 0.0
        
        # News impact component
        news_impact = features.get("news_impact_score", 0.0)
        
        # Weighted combination
        score = (
            self.weights["momentum"] * momentum +
            self.weights["onchain_flow"] * whale_flow +
            self.weights["sentiment"] * sentiment +
            self.weights["macro"] * macro_event +
            self.weights["news_impact"] * news_impact
        )
        
        return float(score)
    
    def classify_breakout(self, score: float) -> str:
        """Classify breakout strength"""
        if score >= 0.73:
            return "Strong Breakout"
        elif score >= 0.60:
            return "Moderate Breakout"
        elif score >= 0.50:
            return "Weak Signal"
        else:
            return "No Signal"


class HybridSignalGenerator:
    """
    Combines LLM reasoning with ML meta-model for final signal
    """
    
    def __init__(self, meta_model: Optional[MetaModel] = None):
        """
        Initialize hybrid signal generator
        
        Args:
            meta_model: Pre-trained meta-model (optional)
        """
        self.meta_model = meta_model or MetaModel()
        self.breakout_scorer = BreakoutScorer()
        
        # Ensemble weights
        self.llm_weight = 0.4
        self.ml_weight = 0.6
    
    async def generate_signal(self, ticker: str, llm_result: Dict,
                            market_data: Dict) -> Dict:
        """
        Generate comprehensive trading signal
        
        Args:
            ticker: Asset ticker/symbol
            llm_result: Results from LLM analysis
            market_data: Additional market data
            
        Returns:
            Comprehensive signal with score, explanation, etc.
        """
        # Combine all features
        all_features = {**llm_result, **market_data}
        
        # Calculate ML probability
        ml_prob = self.meta_model.predict_proba(all_features)
        
        # Calculate breakout score
        breakout_score = self.breakout_scorer.calculate_score(all_features)
        
        # Get LLM confidence
        llm_confidence = llm_result.get("confidence", 0.5)
        
        # Ensemble (weighted combination)
        final_score = self.ml_weight * ml_prob + self.llm_weight * llm_confidence
        
        # Get explanation
        explanation = self.meta_model.explain_prediction(all_features)
        
        # Classify signal
        signal_class = self.breakout_scorer.classify_breakout(breakout_score)
        
        return {
            "ticker": ticker,
            "timestamp": datetime.utcnow().isoformat(),
            "final_score": round(final_score, 3),
            "ml_probability": round(ml_prob, 3),
            "llm_confidence": round(llm_confidence, 3),
            "breakout_score": round(breakout_score, 3),
            "signal_class": signal_class,
            "recommendation": self._get_recommendation(final_score),
            "explanation": explanation,
            "components": {
                "momentum": all_features.get("rsi", 0),
                "sentiment": all_features.get("sentiment", 0),
                "volume": all_features.get("volume_change_24h", 0),
                "whale_activity": all_features.get("whale_flow", 0)
            }
        }
    
    def _get_recommendation(self, score: float) -> str:
        """Get trading recommendation based on score"""
        if score >= 0.75:
            return "Strong Buy"
        elif score >= 0.65:
            return "Buy"
        elif score >= 0.55:
            return "Hold/Watch"
        elif score >= 0.45:
            return "Neutral"
        elif score >= 0.35:
            return "Caution"
        else:
            return "Avoid"


# Example usage
if __name__ == "__main__":
    # Example: Generate a signal
    scorer = BreakoutScorer()
    
    example_features = {
        "rsi": 65,
        "adx": 35,
        "ema_cross": True,
        "whale_flow": 7e6,
        "sentiment": 0.6,
        "macro_event": True,
        "news_impact_score": 0.8
    }
    
    score = scorer.calculate_score(example_features)
    classification = scorer.classify_breakout(score)
    
    print(f"Breakout Score: {score:.3f}")
    print(f"Classification: {classification}")
    
    # Example: Feature engineering
    engineer = FeatureEngineer()
    features = engineer.extract_features(example_features)
    print(f"\nEngineered {len(features)} features")
    
    print("\n" + "="*50)
    print("Meta-Model Module Ready!")
    print("="*50)
    print("\nInstall optional dependencies:")
    print("  pip install xgboost lightgbm shap")
    print("\nFor full functionality, ensure ML libraries are installed.")
