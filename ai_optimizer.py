"""
AI Optimizer Module — v1.0
==========================
Self-improving AI system that continuously optimizes:
  • Worker performance weights
  • Strategy indicator weights
  • Signal confidence calibration
  • Risk parameters per regime
  • AI provider selection per task type

Uses real performance data from ai_learning_system to make decisions.
Zero random — all optimization is data-driven.
"""

import json
import math
import os
import time
import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from threading import Lock

logger = logging.getLogger(__name__)


class AIOptimizer:
    """
    Continuously learns from prediction outcomes and optimizes:
    1. Worker weights in MultiAICoordinator
    2. Indicator weights in SignalAI strategy
    3. Risk parameters per market regime
    4. Confidence calibration curves
    """

    DATA_FILE = "data/ai_optimizer_state.json"
    MIN_SAMPLES = 5  # Minimum samples before adjusting weights

    def __init__(self):
        self._lock = Lock()
        self.state: Dict = {
            "version": 1,
            "last_optimization": None,
            "optimization_count": 0,
            # Worker performance tracking
            "worker_scores": {},
            # Indicator performance per regime
            "indicator_scores": {
                "trending": {},
                "ranging": {},
                "volatile": {},
            },
            # Confidence calibration: predicted vs actual
            "calibration": {
                "buckets": {},  # "70-80" -> {correct: N, total: N}
            },
            # Regime-specific risk multipliers
            "regime_risk": {
                "trending": {"sl_mult": 1.0, "tp_mult": 1.0, "size_mult": 1.0},
                "ranging": {"sl_mult": 0.8, "tp_mult": 0.8, "size_mult": 0.7},
                "volatile": {"sl_mult": 1.5, "tp_mult": 1.3, "size_mult": 0.5},
            },
            # Best strategy per task
            "task_strategy_map": {},
        }
        self._load_state()

    # ── Persistence ─────────────────────────────────────────────────

    def _load_state(self):
        """Load optimizer state from disk."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as f:
                    saved = json.load(f)
                self.state.update(saved)
                logger.info("AIOptimizer: Loaded state (%d optimizations)",
                            self.state["optimization_count"])
            except Exception as e:
                logger.warning(f"AIOptimizer: Could not load state: {e}")

    def save_state(self):
        """Persist optimizer state to disk."""
        with self._lock:
            os.makedirs(os.path.dirname(self.DATA_FILE), exist_ok=True)
            try:
                with open(self.DATA_FILE, "w") as f:
                    json.dump(self.state, f, indent=2)
            except Exception as e:
                logger.error(f"AIOptimizer: Save failed: {e}")

    # ── Record outcomes ─────────────────────────────────────────────

    def record_prediction_outcome(
        self,
        worker_name: str,
        predicted_direction: str,
        actual_direction: str,
        confidence: float,
        regime: str = "unknown",
        indicators_used: Optional[List[str]] = None,
    ):
        """Record whether a prediction was correct for learning.

        Args:
            worker_name: Which AI worker made the prediction
            predicted_direction: 'BULLISH', 'BEARISH', 'NEUTRAL'
            actual_direction: What actually happened
            confidence: Predicted confidence (0-100)
            regime: Market regime at time of prediction
            indicators_used: Which indicators contributed
        """
        with self._lock:
            correct = predicted_direction == actual_direction

            # 1. Update worker scores
            ws = self.state["worker_scores"]
            if worker_name not in ws:
                ws[worker_name] = {"correct": 0, "total": 0, "weight": 1.0}
            ws[worker_name]["total"] += 1
            if correct:
                ws[worker_name]["correct"] += 1

            # 2. Update indicator scores per regime
            if indicators_used and regime in self.state["indicator_scores"]:
                reg_scores = self.state["indicator_scores"][regime]
                for ind in indicators_used:
                    if ind not in reg_scores:
                        reg_scores[ind] = {"correct": 0, "total": 0, "weight": 1.0}
                    reg_scores[ind]["total"] += 1
                    if correct:
                        reg_scores[ind]["correct"] += 1

            # 3. Calibration bucket
            bucket = f"{int(confidence // 10) * 10}-{int(confidence // 10) * 10 + 10}"
            cal = self.state["calibration"]["buckets"]
            if bucket not in cal:
                cal[bucket] = {"correct": 0, "total": 0}
            cal[bucket]["total"] += 1
            if correct:
                cal[bucket]["correct"] += 1

    def record_strategy_result(
        self,
        task_type: str,
        strategy: str,
        success: bool,
        latency_ms: float,
    ):
        """Track which coordinator strategy works best per task type.

        Args:
            task_type: e.g. 'technical_analysis', 'sentiment'
            strategy: e.g. 'consensus', 'fastest', 'specialist'
            success: Whether the result was useful
            latency_ms: How long it took
        """
        with self._lock:
            tsm = self.state["task_strategy_map"]
            key = f"{task_type}:{strategy}"
            if key not in tsm:
                tsm[key] = {"success": 0, "total": 0, "avg_latency": 0}
            entry = tsm[key]
            entry["total"] += 1
            if success:
                entry["success"] += 1
            # Running average latency
            n = entry["total"]
            entry["avg_latency"] = round(
                (entry["avg_latency"] * (n - 1) + latency_ms) / n, 1
            )

    # ── Optimization runs ───────────────────────────────────────────

    def optimize_worker_weights(self) -> Dict[str, float]:
        """Recalculate optimal weights for each AI worker based on accuracy.

        Returns:
            Dict of worker_name -> optimized_weight (0.1 - 2.0)
        """
        with self._lock:
            weights = {}
            for name, stats in self.state["worker_scores"].items():
                if stats["total"] < self.MIN_SAMPLES:
                    weights[name] = 1.0  # Not enough data yet
                    continue

                accuracy = stats["correct"] / stats["total"]
                # Map accuracy to weight: 50% -> 0.5, 70% -> 1.0, 90% -> 1.8
                weight = max(0.1, min(2.0, accuracy * 2.0))
                weights[name] = round(weight, 3)
                stats["weight"] = weights[name]

            return weights

    def optimize_indicator_weights(self, regime: str = "trending") -> Dict[str, float]:
        """Recalculate optimal indicator weights for a specific regime.

        Args:
            regime: 'trending', 'ranging', or 'volatile'

        Returns:
            Dict of indicator_name -> optimized_weight
        """
        with self._lock:
            if regime not in self.state["indicator_scores"]:
                return {}

            weights = {}
            reg_scores = self.state["indicator_scores"][regime]
            for ind, stats in reg_scores.items():
                if stats["total"] < self.MIN_SAMPLES:
                    weights[ind] = 1.0
                    continue

                accuracy = stats["correct"] / stats["total"]
                # Scale: 40% accuracy -> 0.3, 60% -> 1.0, 80% -> 1.6
                weight = max(0.1, min(2.0, (accuracy - 0.3) * 3.33))
                weights[ind] = round(weight, 3)
                stats["weight"] = weights[ind]

            return weights

    def get_calibrated_confidence(self, raw_confidence: float) -> float:
        """Adjust predicted confidence based on historical calibration.

        If we predicted 80% confidence but only 60% of those were correct,
        we calibrate down to ~60%.

        Args:
            raw_confidence: The model's raw confidence (0-100)

        Returns:
            Calibrated confidence (0-100)
        """
        bucket = f"{int(raw_confidence // 10) * 10}-{int(raw_confidence // 10) * 10 + 10}"
        cal = self.state["calibration"]["buckets"].get(bucket)

        if not cal or cal["total"] < self.MIN_SAMPLES:
            return raw_confidence  # Not enough data to calibrate

        actual_accuracy = cal["correct"] / cal["total"] * 100
        # Blend: 70% calibrated + 30% raw (smooth transition)
        calibrated = actual_accuracy * 0.7 + raw_confidence * 0.3
        return round(max(5, min(95, calibrated)), 1)

    def get_optimal_strategy(self, task_type: str) -> str:
        """Return the best coordinator strategy for a given task type.

        Args:
            task_type: e.g. 'technical_analysis', 'sentiment'

        Returns:
            Best strategy name (e.g. 'consensus', 'specialist')
        """
        best_strategy = "consensus"  # Default
        best_score = -1

        tsm = self.state["task_strategy_map"]
        for key, stats in tsm.items():
            t, strat = key.split(":", 1)
            if t != task_type or stats["total"] < self.MIN_SAMPLES:
                continue
            # Score = success_rate * (1 / normalized_latency)
            success_rate = stats["success"] / stats["total"]
            latency_penalty = min(1.0, 5000 / max(stats["avg_latency"], 1))
            score = success_rate * latency_penalty
            if score > best_score:
                best_score = score
                best_strategy = strat

        return best_strategy

    def get_regime_risk_params(self, regime: str) -> Dict[str, float]:
        """Get optimized risk parameters for current market regime.

        Args:
            regime: 'trending', 'ranging', 'volatile'

        Returns:
            Dict with sl_mult, tp_mult, size_mult
        """
        return self.state["regime_risk"].get(regime, {
            "sl_mult": 1.0, "tp_mult": 1.0, "size_mult": 1.0
        })

    def update_regime_risk(self, regime: str, param: str, value: float):
        """Update a regime risk parameter.

        Args:
            regime: 'trending', 'ranging', 'volatile'
            param: 'sl_mult', 'tp_mult', 'size_mult'
            value: New value (0.1 - 3.0)
        """
        with self._lock:
            if regime in self.state["regime_risk"]:
                self.state["regime_risk"][regime][param] = round(
                    max(0.1, min(3.0, value)), 2
                )

    def run_full_optimization(self) -> Dict:
        """Run a complete optimization cycle.

        Returns:
            Report with all optimization results.
        """
        report = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "worker_weights": self.optimize_worker_weights(),
            "indicator_weights": {},
            "best_strategies": {},
            "calibration_status": {},
        }

        # Optimize indicators for each regime
        for regime in ("trending", "ranging", "volatile"):
            weights = self.optimize_indicator_weights(regime)
            if weights:
                report["indicator_weights"][regime] = weights

        # Find best strategy per task
        task_types = set()
        for key in self.state["task_strategy_map"]:
            t, _ = key.split(":", 1)
            task_types.add(t)
        for task in task_types:
            report["best_strategies"][task] = self.get_optimal_strategy(task)

        # Calibration summary
        for bucket, stats in self.state["calibration"]["buckets"].items():
            if stats["total"] > 0:
                report["calibration_status"][bucket] = {
                    "accuracy": round(stats["correct"] / stats["total"] * 100, 1),
                    "samples": stats["total"],
                }

        # Update metadata
        with self._lock:
            self.state["optimization_count"] += 1
            self.state["last_optimization"] = report["timestamp"]

        self.save_state()

        logger.info(
            "AIOptimizer: Full optimization #%d complete — %d workers, %d tasks",
            self.state["optimization_count"],
            len(report["worker_weights"]),
            len(report["best_strategies"]),
        )

        return report

    def get_status(self) -> Dict:
        """Get optimizer status for dashboard."""
        return {
            "optimization_count": self.state["optimization_count"],
            "last_optimization": self.state["last_optimization"],
            "workers_tracked": len(self.state["worker_scores"]),
            "total_predictions": sum(
                s["total"] for s in self.state["worker_scores"].values()
            ),
            "overall_accuracy": self._overall_accuracy(),
            "regime_risk": self.state["regime_risk"],
            "calibration_buckets": len(self.state["calibration"]["buckets"]),
        }

    def _overall_accuracy(self) -> float:
        """Calculate overall prediction accuracy across all workers."""
        total_correct = sum(s["correct"] for s in self.state["worker_scores"].values())
        total_all = sum(s["total"] for s in self.state["worker_scores"].values())
        if total_all == 0:
            return 0.0
        return round(total_correct / total_all * 100, 1)


# ── Singleton ───────────────────────────────────────────────────

_optimizer_instance = None


def get_optimizer() -> AIOptimizer:
    """Get or create the singleton AIOptimizer."""
    global _optimizer_instance
    if _optimizer_instance is None:
        _optimizer_instance = AIOptimizer()
    return _optimizer_instance
