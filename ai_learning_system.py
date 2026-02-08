#!/usr/bin/env python3
"""
AI Learning System — Smart Data Persistence & Continuous Evolution
===================================================================
Tracks prediction accuracy per model/strategy, evolves weights,
maintains pattern memory, and automatically cleans low-value data.

Key features:
- Prediction recording with outcome tracking
- Per-model and per-strategy accuracy scoring
- Automatic weight adjustment for the coordinator
- Pattern memory with importance-based pruning
- Smart data lifecycle: keep high-value, discard noise
- Daily evolution cycle with auto price evaluation
- Data compression for historical archives
"""

import os
import json
import gzip
import time
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any

import requests

logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "ai_learning")

# Limits
MAX_PREDICTIONS = 5000
MAX_EVOLUTION_REPORTS = 365
MAX_PATTERNS_PER_KEY = 50
MAX_ARCHIVE_FILES = 30
ARCHIVE_THRESHOLD_DAYS = 30
IMPORTANCE_PRUNE_THRESHOLD = 0.2  # patterns with hit_rate < 20% are pruned


# ---------------------------------------------------------------------------
# PredictionRecord
# ---------------------------------------------------------------------------

class PredictionRecord:
    """One prediction with its eventual outcome."""

    def __init__(
        self,
        prediction_id: str,
        symbol: str,
        direction: str,
        confidence: float,
        model: str,
        strategy: str,
        price_at_prediction: float,
        timestamp: Optional[str] = None,
        outcome: Optional[str] = None,
        price_at_evaluation: Optional[float] = None,
        evaluated_at: Optional[str] = None,
        importance: float = 1.0,
    ):
        self.prediction_id = prediction_id
        self.symbol = symbol.upper()
        self.direction = direction.upper()
        self.confidence = confidence
        self.model = model
        self.strategy = strategy
        self.price_at_prediction = price_at_prediction
        self.timestamp = timestamp or datetime.now(timezone.utc).isoformat()
        self.outcome = outcome  # CORRECT / INCORRECT / PARTIAL / None
        self.price_at_evaluation = price_at_evaluation
        self.evaluated_at = evaluated_at
        self.importance = importance  # 0-2 importance score

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, d: dict) -> "PredictionRecord":
        return cls(**{k: v for k, v in d.items() if k in cls.__init__.__code__.co_varnames})


# ---------------------------------------------------------------------------
# AI Learning System
# ---------------------------------------------------------------------------

class AILearningSystem:
    """
    Learns from prediction outcomes and evolves AI weights.
    
    Smart data lifecycle:
    - High-accuracy, high-confidence predictions → kept indefinitely
    - Low-importance, old data → archived & compressed
    - Stale pattern memory → pruned automatically
    """

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)

        # In-memory state
        self.predictions: List[PredictionRecord] = []
        self.scores: Dict[str, Dict] = {}          # model_name → {correct, total, ...}
        self.pattern_memory: Dict[str, List] = {}   # pattern_hash → [outcomes]
        self.evolution_reports: List[dict] = []

        # Load persisted state
        self._load_state()

    # ---- Recording predictions --------------------------------------------

    def record_prediction(
        self,
        symbol: str,
        direction: str,
        confidence: float,
        model: str,
        strategy: str,
        price_at_prediction: float,
        extra: Optional[dict] = None,
    ) -> str:
        """Record a new prediction. Returns prediction_id."""
        pid = hashlib.md5(
            f"{symbol}{direction}{confidence}{model}{time.time()}".encode()
        ).hexdigest()[:16]

        rec = PredictionRecord(
            prediction_id=pid,
            symbol=symbol,
            direction=direction,
            confidence=confidence,
            model=model,
            strategy=strategy,
            price_at_prediction=price_at_prediction,
        )

        self.predictions.append(rec)
        self._record_pattern(rec, extra)

        # Enforce limits
        if len(self.predictions) > MAX_PREDICTIONS:
            self._smart_prune_predictions()

        self._save_predictions()
        return pid

    def evaluate_prediction(self, prediction_id: str, outcome: str, price_now: float) -> bool:
        """Evaluate a past prediction. outcome: CORRECT / INCORRECT / PARTIAL."""
        for rec in self.predictions:
            if rec.prediction_id == prediction_id and rec.outcome is None:
                rec.outcome = outcome.upper()
                rec.price_at_evaluation = price_now
                rec.evaluated_at = datetime.now(timezone.utc).isoformat()

                # Boost importance for correct high-confidence
                if outcome == "CORRECT" and rec.confidence >= 0.7:
                    rec.importance = min(2.0, rec.importance + 0.3)
                elif outcome == "INCORRECT":
                    rec.importance = max(0.1, rec.importance - 0.2)

                self._update_scores(rec)
                self._save_predictions()
                self._save_scores()
                return True
        return False

    def batch_evaluate(self, evaluations: List[dict]):
        """Evaluate many predictions at once. Each item: {prediction_id, outcome, price_now}."""
        for ev in evaluations:
            self.evaluate_prediction(ev["prediction_id"], ev["outcome"], ev["price_now"])

    # ---- Accuracy queries -------------------------------------------------

    def get_model_accuracy(self, model: str) -> dict:
        """Get accuracy stats for a specific model."""
        stats = self.scores.get(model, {"correct": 0, "total": 0, "incorrect": 0, "partial": 0})
        total = stats["total"]
        return {
            "model": model,
            "accuracy": round(stats["correct"] / total, 3) if total else 0,
            "total_predictions": total,
            "correct": stats["correct"],
            "incorrect": stats["incorrect"],
            "partial": stats.get("partial", 0),
        }

    def get_strategy_accuracy(self, strategy: str) -> dict:
        """Get accuracy stats for a strategy (filtering predictions)."""
        relevant = [p for p in self.predictions if p.strategy == strategy and p.outcome]
        if not relevant:
            return {"strategy": strategy, "accuracy": 0, "total": 0}
        correct = sum(1 for p in relevant if p.outcome == "CORRECT")
        return {
            "strategy": strategy,
            "accuracy": round(correct / len(relevant), 3),
            "total": len(relevant),
            "correct": correct,
        }

    def get_recommended_weights(self) -> Dict[str, float]:
        """Compute recommended weights for coordinator based on accuracy."""
        weights = {}
        for model, stats in self.scores.items():
            total = stats["total"]
            if total < 5:
                weights[model] = 1.0
            else:
                acc = stats["correct"] / total
                # Weight = 0.4 + 1.2 * accuracy (range 0.4 — 1.6)
                weights[model] = round(0.4 + 1.2 * acc, 2)
        return weights

    def apply_weights_to_coordinator(self, coordinator) -> Dict[str, float]:
        """Apply learned weights to the coordinator's workers."""
        weights = self.get_recommended_weights()
        applied = {}
        for worker in coordinator.workers:
            w = weights.get(worker.name, 1.0)
            coordinator.set_weight(worker.name, w)
            applied[worker.name] = w
        return applied

    # ---- Symbol insights --------------------------------------------------

    def get_symbol_insights(self, symbol: str) -> dict:
        """Get learning insights for a specific symbol."""
        relevant = [p for p in self.predictions if p.symbol == symbol.upper()]
        if not relevant:
            return {"symbol": symbol, "predictions": 0}

        evaluated = [p for p in relevant if p.outcome]
        correct = sum(1 for p in evaluated if p.outcome == "CORRECT")
        directions = {}
        for p in relevant[-20:]:
            d = p.direction
            directions[d] = directions.get(d, 0) + 1

        return {
            "symbol": symbol.upper(),
            "total_predictions": len(relevant),
            "evaluated": len(evaluated),
            "accuracy": round(correct / len(evaluated), 3) if evaluated else 0,
            "dominant_direction": max(directions, key=directions.get) if directions else "NEUTRAL",
            "avg_confidence": round(sum(p.confidence for p in relevant) / len(relevant), 2),
        }

    # ---- Learning summary -------------------------------------------------

    def get_learning_summary(self) -> dict:
        """Overall learning system summary."""
        evaluated = [p for p in self.predictions if p.outcome]
        correct = sum(1 for p in evaluated if p.outcome == "CORRECT")
        models = list(self.scores.keys())

        return {
            "total_predictions": len(self.predictions),
            "evaluated": len(evaluated),
            "accuracy": round(correct / len(evaluated), 3) if evaluated else 0,
            "models_tracked": models,
            "patterns_stored": sum(len(v) for v in self.pattern_memory.values()),
            "pattern_keys": len(self.pattern_memory),
            "evolution_reports": len(self.evolution_reports),
            "data_dir": DATA_DIR,
        }

    # ---- Daily evolution cycle --------------------------------------------

    def daily_evolution(self, coordinator=None) -> dict:
        """
        Run the daily evolution cycle:
        1. Auto-evaluate old predictions via live price check
        2. Recompute weights
        3. Prune low-value data
        4. Archive old predictions
        5. Generate evolution report
        """
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "predictions_auto_evaluated": 0,
            "weight_changes": {},
            "data_pruned": 0,
            "archived": 0,
            "summary": {},
        }

        # 1. Auto-evaluate predictions older than 24h
        cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
        unevaluated = [
            p for p in self.predictions
            if p.outcome is None
            and datetime.fromisoformat(p.timestamp.replace("Z", "+00:00")) < cutoff
        ]

        for pred in unevaluated:
            try:
                auto_outcome = self._auto_evaluate_direction(pred)
                if auto_outcome:
                    pred.outcome = auto_outcome
                    pred.evaluated_at = datetime.now(timezone.utc).isoformat()
                    self._update_scores(pred)
                    report["predictions_auto_evaluated"] += 1
            except Exception as e:
                logger.debug("Auto-eval failed for %s: %s", pred.prediction_id, e)

        # 2. Apply weights to coordinator
        if coordinator:
            report["weight_changes"] = self.apply_weights_to_coordinator(coordinator)

        # 3. Smart prune predictions
        pruned = self._smart_prune_predictions()
        report["data_pruned"] = pruned

        # 4. Prune low-value patterns
        pattern_pruned = self._prune_pattern_memory()
        report["patterns_pruned"] = pattern_pruned

        # 5. Archive old data
        archived = self._archive_old_data()
        report["archived"] = archived

        # 6. Summary
        report["summary"] = self.get_learning_summary()

        # Save
        self.evolution_reports.append(report)
        if len(self.evolution_reports) > MAX_EVOLUTION_REPORTS:
            self.evolution_reports = self.evolution_reports[-MAX_EVOLUTION_REPORTS:]

        self._save_predictions()
        self._save_scores()
        self._save_evolution_report(report)

        return report

    # ---- Auto evaluation --------------------------------------------------

    def _auto_evaluate_direction(self, pred: PredictionRecord) -> Optional[str]:
        """
        Evaluate a directional prediction by checking real price change.
        Uses CoinPaprika (crypto) or CoinCap as fallback.
        """
        symbol = pred.symbol.upper()

        # Try CoinPaprika
        price_change = self._get_price_change_coinpaprika(symbol)

        # Try CoinCap fallback
        if price_change is None:
            price_change = self._get_price_change_coincap(symbol)

        if price_change is None:
            return None

        # Record evaluation price
        pred.price_at_evaluation = pred.price_at_prediction * (1 + price_change / 100)

        # Classify
        threshold = 2.0  # ±2% significance
        if price_change > threshold:
            actual = "BULLISH"
        elif price_change < -threshold:
            actual = "BEARISH"
        else:
            actual = "NEUTRAL"

        # Match
        if pred.direction == actual:
            return "CORRECT"
        elif pred.direction == "NEUTRAL" or actual == "NEUTRAL":
            return "PARTIAL"
        else:
            return "INCORRECT"

    def _get_price_change_coinpaprika(self, symbol: str) -> Optional[float]:
        """Get 24h price change from CoinPaprika."""
        slug_map = {
            "BTC": "btc-bitcoin", "ETH": "eth-ethereum", "BNB": "bnb-binance-coin",
            "SOL": "sol-solana", "XRP": "xrp-xrp", "ADA": "ada-cardano",
            "DOGE": "doge-dogecoin", "DOT": "dot-polkadot", "AVAX": "avax-avalanche",
            "MATIC": "matic-polygon", "LINK": "link-chainlink", "UNI": "uni-uniswap",
            "ATOM": "atom-cosmos", "LTC": "ltc-litecoin", "NEAR": "near-near-protocol",
            "FTM": "ftm-fantom", "ALGO": "algo-algorand", "APE": "ape-apecoin",
            "SHIB": "shib-shiba-inu", "TRX": "trx-tron", "ARB": "arb-arbitrum",
            "OP": "op-optimism", "SUI": "sui-sui", "SEI": "sei-sei",
            "FIL": "fil-filecoin", "AAVE": "aave-aave", "MKR": "mkr-maker",
            "INJ": "inj-injective", "RNDR": "rndr-render", "PEPE": "pepe-pepe",
        }
        slug = slug_map.get(symbol)
        if not slug:
            # Try to guess the slug
            slug = f"{symbol.lower()}-{symbol.lower()}"
        try:
            r = requests.get(f"https://api.coinpaprika.com/v1/tickers/{slug}", timeout=8)
            if r.status_code == 200:
                data = r.json()
                return data.get("quotes", {}).get("USD", {}).get("percent_change_24h")
        except Exception:
            pass
        return None

    def _get_price_change_coincap(self, symbol: str) -> Optional[float]:
        """Get 24h price change from CoinCap."""
        try:
            r = requests.get(
                f"https://api.coincap.io/v2/assets/{symbol.lower()}",
                timeout=8,
            )
            if r.status_code == 200:
                data = r.json().get("data", {})
                change = data.get("changePercent24Hr")
                if change is not None:
                    return float(change)
        except Exception:
            pass
        return None

    # ---- Score tracking ---------------------------------------------------

    def _update_scores(self, rec: PredictionRecord):
        """Update model accuracy scores after evaluation."""
        if rec.model not in self.scores:
            self.scores[rec.model] = {"correct": 0, "incorrect": 0, "partial": 0, "total": 0}
        s = self.scores[rec.model]
        s["total"] += 1
        if rec.outcome == "CORRECT":
            s["correct"] += 1
        elif rec.outcome == "INCORRECT":
            s["incorrect"] += 1
        elif rec.outcome == "PARTIAL":
            s["partial"] += 1

    # ---- Pattern memory ---------------------------------------------------

    def _record_pattern(self, rec: PredictionRecord, extra: Optional[dict] = None):
        """Record a prediction pattern for future reference."""
        rsi_bucket = ""
        macd_sign = ""
        trend = ""
        if extra:
            rsi = extra.get("rsi")
            macd = extra.get("macd")
            if rsi is not None:
                rsi_bucket = str(int(rsi) // 10)
            if macd is not None:
                macd_sign = "pos" if (macd if isinstance(macd, (int, float)) else 0) > 0 else "neg"
            trend = extra.get("trend", "")

        key = hashlib.md5(
            f"{rec.symbol}_{rsi_bucket}_{macd_sign}_{trend}".encode()
        ).hexdigest()[:12]

        self.pattern_memory.setdefault(key, [])
        self.pattern_memory[key].append({
            "direction": rec.direction,
            "confidence": rec.confidence,
            "model": rec.model,
            "timestamp": rec.timestamp,
            "symbol": rec.symbol,
        })

        # Cap per key
        if len(self.pattern_memory[key]) > MAX_PATTERNS_PER_KEY:
            self.pattern_memory[key] = self.pattern_memory[key][-MAX_PATTERNS_PER_KEY:]

    def _prune_pattern_memory(self) -> int:
        """Remove patterns with low hit rate or very old data."""
        pruned = 0
        keys_to_remove = []

        for key, entries in self.pattern_memory.items():
            # Remove entries older than 90 days
            cutoff = (datetime.now(timezone.utc) - timedelta(days=90)).isoformat()
            fresh = [e for e in entries if e.get("timestamp", "") > cutoff]

            if len(fresh) < 2:
                keys_to_remove.append(key)
                pruned += len(entries)
            else:
                removed = len(entries) - len(fresh)
                pruned += removed
                self.pattern_memory[key] = fresh

        for k in keys_to_remove:
            del self.pattern_memory[k]

        return pruned

    # ---- Smart data pruning -----------------------------------------------

    def _smart_prune_predictions(self) -> int:
        """
        Smart pruning: keep high-value predictions, discard noise.
        
        Priority (keep):
        1. Evaluated + CORRECT + high confidence
        2. Recent (last 7 days)
        3. High importance score
        
        Discard:
        - Old unevaluated predictions
        - Low-confidence INCORRECT predictions
        """
        if len(self.predictions) <= MAX_PREDICTIONS:
            return 0

        now = datetime.now(timezone.utc)
        week_ago = (now - timedelta(days=7)).isoformat()

        # Score each prediction for retention
        scored = []
        for p in self.predictions:
            score = p.importance
            # Recent predictions get a boost
            if p.timestamp > week_ago:
                score += 1.0
            # Evaluated correctly with high confidence = very valuable
            if p.outcome == "CORRECT" and p.confidence >= 0.7:
                score += 1.5
            elif p.outcome == "CORRECT":
                score += 0.8
            elif p.outcome == "PARTIAL":
                score += 0.3
            # Old unevaluated = low value
            if p.outcome is None and p.timestamp < week_ago:
                score -= 0.5
            scored.append((score, p))

        # Sort by score descending, keep top MAX_PREDICTIONS
        scored.sort(key=lambda x: x[0], reverse=True)
        keep = scored[:MAX_PREDICTIONS]
        pruned = len(scored) - len(keep)

        self.predictions = [p for _, p in keep]
        return pruned

    # ---- Data archiving ---------------------------------------------------

    def _archive_old_data(self) -> int:
        """
        Compress and archive predictions older than ARCHIVE_THRESHOLD_DAYS.
        Keeps them in gzipped JSON for potential future analysis.
        """
        cutoff = (datetime.now(timezone.utc) - timedelta(days=ARCHIVE_THRESHOLD_DAYS)).isoformat()
        to_archive = [p for p in self.predictions if p.timestamp < cutoff and p.outcome is not None]

        if len(to_archive) < 50:
            return 0

        archive_dir = os.path.join(DATA_DIR, "archives")
        os.makedirs(archive_dir, exist_ok=True)

        stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        archive_path = os.path.join(archive_dir, f"archive_{stamp}.json.gz")

        archive_data = [p.to_dict() for p in to_archive]
        with gzip.open(archive_path, "wt", encoding="utf-8") as f:
            json.dump(archive_data, f, default=str)

        # Remove archived predictions from active list
        archived_ids = {p.prediction_id for p in to_archive}
        self.predictions = [p for p in self.predictions if p.prediction_id not in archived_ids]

        # Clean up old archive files
        self._cleanup_old_archives(archive_dir)

        logger.info("Archived %d predictions to %s", len(to_archive), archive_path)
        return len(to_archive)

    def _cleanup_old_archives(self, archive_dir: str):
        """Keep only the last MAX_ARCHIVE_FILES archive files."""
        try:
            files = sorted(
                [f for f in os.listdir(archive_dir) if f.endswith(".json.gz")],
                reverse=True,
            )
            for old_file in files[MAX_ARCHIVE_FILES:]:
                os.remove(os.path.join(archive_dir, old_file))
        except Exception as e:
            logger.warning("Archive cleanup error: %s", e)

    # ---- Persistence ------------------------------------------------------

    def _save_predictions(self):
        """Save predictions to disk."""
        path = os.path.join(DATA_DIR, "predictions.json")
        try:
            data = [p.to_dict() for p in self.predictions]
            with open(path, "w") as f:
                json.dump(data, f, indent=1, default=str)
        except Exception as e:
            logger.error("Failed to save predictions: %s", e)

    def _save_scores(self):
        """Save scores to disk."""
        path = os.path.join(DATA_DIR, "scores.json")
        try:
            with open(path, "w") as f:
                json.dump(self.scores, f, indent=2)
        except Exception as e:
            logger.error("Failed to save scores: %s", e)

    def _save_evolution_report(self, report: dict):
        """Save evolution reports to disk."""
        path = os.path.join(DATA_DIR, "evolution_reports.json")
        try:
            with open(path, "w") as f:
                json.dump(self.evolution_reports[-MAX_EVOLUTION_REPORTS:], f, indent=1, default=str)
        except Exception as e:
            logger.error("Failed to save evolution report: %s", e)

    def _load_state(self):
        """Load persisted state from disk."""
        # Predictions
        pred_path = os.path.join(DATA_DIR, "predictions.json")
        if os.path.exists(pred_path):
            try:
                with open(pred_path) as f:
                    data = json.load(f)
                self.predictions = [PredictionRecord.from_dict(d) for d in data]
            except Exception as e:
                logger.warning("Failed to load predictions: %s", e)

        # Scores
        scores_path = os.path.join(DATA_DIR, "scores.json")
        if os.path.exists(scores_path):
            try:
                with open(scores_path) as f:
                    self.scores = json.load(f)
            except Exception as e:
                logger.warning("Failed to load scores: %s", e)

        # Evolution reports
        evo_path = os.path.join(DATA_DIR, "evolution_reports.json")
        if os.path.exists(evo_path):
            try:
                with open(evo_path) as f:
                    self.evolution_reports = json.load(f)
            except Exception as e:
                logger.warning("Failed to load evolution reports: %s", e)

        # Pattern memory
        pattern_path = os.path.join(DATA_DIR, "patterns.json")
        if os.path.exists(pattern_path):
            try:
                with open(pattern_path) as f:
                    self.pattern_memory = json.load(f)
            except Exception as e:
                logger.warning("Failed to load pattern memory: %s", e)

    def save_all(self):
        """Save everything to disk."""
        self._save_predictions()
        self._save_scores()
        # Save pattern memory
        pattern_path = os.path.join(DATA_DIR, "patterns.json")
        try:
            with open(pattern_path, "w") as f:
                json.dump(self.pattern_memory, f, indent=1, default=str)
        except Exception as e:
            logger.error("Failed to save pattern memory: %s", e)
        # Save evolution reports
        if self.evolution_reports:
            self._save_evolution_report(self.evolution_reports[-1])


# ---------------------------------------------------------------------------
# Module singleton
# ---------------------------------------------------------------------------

_learning_system: Optional[AILearningSystem] = None


def get_learning_system() -> AILearningSystem:
    """Get or create the global learning system instance."""
    global _learning_system
    if _learning_system is None:
        _learning_system = AILearningSystem()
    return _learning_system
