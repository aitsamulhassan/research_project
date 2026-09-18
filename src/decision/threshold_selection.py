"""Validation-only threshold selection. Test labels never enter this module's fit path."""

from __future__ import annotations

from typing import Any, Iterable

import numpy as np

from decision.cost_policy import CostScenario, expected_normalized_cost
from decision.decision_engine import credit_bands

ALLOWED_SELECTION_SPLIT = "validation"


def assert_validation_split(split: str) -> None:
    if split != ALLOWED_SELECTION_SPLIT:
        raise ValueError("Threshold selection is permitted on the validation split only.")


def make_threshold_grid(start: float, stop: float, step: float) -> np.ndarray:
    if step <= 0 or stop < start:
        raise ValueError("Invalid threshold grid.")
    n = int(round((stop - start) / step)) + 1
    grid = np.round(start + step * np.arange(n), 10)
    grid = grid[(grid >= start - 1e-12) & (grid <= stop + 1e-12)]
    if grid.size == 0:
        raise ValueError("Empty threshold grid.")
    return grid


def credit_only_decisions(p: np.ndarray, t_low: float, t_high: float) -> np.ndarray:
    bands = credit_bands(p, t_low, t_high)
    out = np.empty(bands.shape, dtype=object)
    out[bands == "LOW"] = "APPROVE"
    out[bands == "MEDIUM"] = "HUMAN_REVIEW"
    out[bands == "HIGH"] = "REJECT"
    return out


def auto_confusion(y: np.ndarray, decisions: np.ndarray) -> dict[str, float]:
    y = np.asarray(y).astype(int)
    decisions = np.asarray(decisions, dtype=object)
    if y.shape != decisions.shape:
        raise ValueError("y and decisions length mismatch.")
    n = int(y.size)
    approve = decisions == "APPROVE"
    reject = decisions == "REJECT"
    review = decisions == "HUMAN_REVIEW"
    if int(approve.sum() + reject.sum() + review.sum()) != n:
        unknown = sorted({str(v) for v in np.unique(decisions) if v not in {"APPROVE", "REJECT", "HUMAN_REVIEW"}})
        raise ValueError(f"Unknown decisions: {unknown}")
    fn = int(np.sum(approve & (y == 1)))
    tn = int(np.sum(approve & (y == 0)))
    fp = int(np.sum(reject & (y == 0)))
    tp = int(np.sum(reject & (y == 1)))
    n_review = int(np.sum(review))
    n_approve = int(np.sum(approve))
    n_reject = int(np.sum(reject))
    n_pos = int(np.sum(y == 1))
    n_neg = int(np.sum(y == 0))
    n_auto_pos = fn + tp
    n_auto_neg = fp + tn
    return {
        "n": n,
        "n_positive": n_pos,
        "n_negative": n_neg,
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
        "n_approve": n_approve,
        "n_review": n_review,
        "n_reject": n_reject,
        "approval_rate": n_approve / n,
        "review_rate": n_review / n,
        "rejection_rate": n_reject / n,
        "fpr_auto": (fp / n_auto_neg) if n_auto_neg else float("nan"),
        "fnr_auto": (fn / n_auto_pos) if n_auto_pos else float("nan"),
        "fpr_population": (fp / n_neg) if n_neg else float("nan"),
        "fnr_population": (fn / n_pos) if n_pos else float("nan"),
        "precision_reject": (tp / (tp + fp)) if (tp + fp) else float("nan"),
        "recall_reject_auto": (tp / n_auto_pos) if n_auto_pos else float("nan"),
        "recall_reject_population": (tp / n_pos) if n_pos else float("nan"),
    }


def evaluate_thresholds(
    y: np.ndarray,
    p: np.ndarray,
    t_low: float,
    t_high: float,
    scenario: CostScenario,
    *,
    split: str,
    decisions: np.ndarray | None = None,
) -> dict[str, Any]:
    assert_validation_split(split)
    if decisions is None:
        y = np.asarray(y).astype(int)
        p = np.asarray(p, dtype=float)
        approve = p < t_low
        reject = p >= t_high
        review = ~(approve | reject)
        decisions = np.empty(p.shape, dtype=object)
        decisions[approve] = "APPROVE"
        decisions[review] = "HUMAN_REVIEW"
        decisions[reject] = "REJECT"
    counts = auto_confusion(y, decisions)
    cost = expected_normalized_cost(counts["fn"], counts["fp"], counts["n_review"], counts["n"], scenario)
    row = {
        "t_low": float(t_low),
        "t_high": float(t_high),
        "policy_type": "single_threshold" if t_low == t_high else "two_threshold",
        "expected_normalized_cost": float(cost),
        "expected_cost_total": float(cost * counts["n"]),
        **counts,
        "cost_scenario": scenario.as_dict(),
        "split": split,
    }
    return row


def _tie_key(row: dict[str, Any]) -> tuple:
    fnr = row["fnr_population"]
    fnr_key = 1.0 if fnr != fnr else float(fnr)  # NaN sorts last
    return (
        float(row["expected_normalized_cost"]),
        0 if row["policy_type"] == "single_threshold" else 1,
        float(row["review_rate"]),
        fnr_key,
        float(row["t_high"] - row["t_low"]),
        float(row["t_low"]),
        float(row["t_high"]),
    )


def select_policy(
    y: np.ndarray,
    p: np.ndarray,
    scenario: CostScenario,
    grid: np.ndarray,
    *,
    split: str,
    include_two_threshold: bool = True,
) -> dict[str, Any]:
    """Minimize expected normalized cost on VALIDATION. Test data must not be passed."""
    assert_validation_split(split)
    p = np.asarray(p, dtype=float)
    y = np.asarray(y).astype(int)
    if p.shape != y.shape:
        raise ValueError("p and y length mismatch.")
    pos = y == 1
    neg = y == 0
    n = int(y.size)
    n_pos = int(pos.sum())
    n_neg = int(neg.sum())

    def row_from_thresholds(t_low: float, t_high: float) -> dict[str, Any]:
        approve = p < t_low
        reject = p >= t_high
        n_approve = int(approve.sum())
        n_reject = int(reject.sum())
        n_review = n - n_approve - n_reject
        fn = int(np.sum(approve & pos))
        tn = n_approve - fn
        fp = int(np.sum(reject & neg))
        tp = n_reject - fp
        n_auto_pos = fn + tp
        n_auto_neg = fp + tn
        cost = expected_normalized_cost(fn, fp, n_review, n, scenario)
        return {
            "t_low": float(t_low),
            "t_high": float(t_high),
            "policy_type": "single_threshold" if t_low == t_high else "two_threshold",
            "expected_normalized_cost": float(cost),
            "expected_cost_total": float(cost * n),
            "n": n,
            "n_positive": n_pos,
            "n_negative": n_neg,
            "tp": tp,
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "n_approve": n_approve,
            "n_review": n_review,
            "n_reject": n_reject,
            "approval_rate": n_approve / n,
            "review_rate": n_review / n,
            "rejection_rate": n_reject / n,
            "fpr_auto": (fp / n_auto_neg) if n_auto_neg else float("nan"),
            "fnr_auto": (fn / n_auto_pos) if n_auto_pos else float("nan"),
            "fpr_population": (fp / n_neg) if n_neg else float("nan"),
            "fnr_population": (fn / n_pos) if n_pos else float("nan"),
            "precision_reject": (tp / (tp + fp)) if (tp + fp) else float("nan"),
            "recall_reject_auto": (tp / n_auto_pos) if n_auto_pos else float("nan"),
            "recall_reject_population": (tp / n_pos) if n_pos else float("nan"),
            "cost_scenario": scenario.as_dict(),
            "split": split,
        }

    candidates = [row_from_thresholds(float(t), float(t)) for t in grid]
    if include_two_threshold:
        for i, t_low in enumerate(grid):
            for t_high in grid[i + 1 :]:
                candidates.append(row_from_thresholds(float(t_low), float(t_high)))
    single_best = min(
        (c for c in candidates if c["policy_type"] == "single_threshold"),
        key=_tie_key,
    )
    two_best = None
    if include_two_threshold:
        two_best = min(
            (c for c in candidates if c["policy_type"] == "two_threshold"),
            key=_tie_key,
        )
    overall = min(candidates, key=_tie_key)
    return {
        "selected": overall,
        "selected_single": single_best,
        "selected_two_threshold": two_best,
        "n_candidates": len(candidates),
        "grid": [float(x) for x in grid],
        "split": split,
        "selection_rule": {
            "objective": "minimize expected_normalized_cost",
            "tie_break": [
                "prefer_single_threshold",
                "lower_review_rate",
                "lower_fnr_population",
                "smaller_band_width",
                "lower_t_low",
                "lower_t_high",
            ],
        },
    }


def single_threshold_cost_curve(
    y: np.ndarray,
    p: np.ndarray,
    scenario: CostScenario,
    grid: Iterable[float],
    *,
    split: str,
) -> list[dict[str, Any]]:
    return [evaluate_thresholds(y, p, float(t), float(t), scenario, split=split) for t in grid]
