"""Operational decision metrics. Labels are used only for evaluation, not for policy fitting here."""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from decision.cost_policy import CostScenario, expected_normalized_cost
from decision.threshold_selection import auto_confusion


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return (float("nan"), float("nan"))
    if k < 0 or k > n:
        raise ValueError("Wilson CI requires 0 <= k <= n.")
    p = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    half = z * math.sqrt((p * (1.0 - p) + z2 / (4.0 * n)) / n) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def band_outcome_table(y: np.ndarray, labels: np.ndarray) -> list[dict[str, Any]]:
    y = np.asarray(y).astype(int)
    labels = np.asarray(labels, dtype=object)
    rows = []
    for name in sorted({str(v) for v in np.unique(labels)}):
        mask = labels == name
        n = int(mask.sum())
        k = int(np.sum(y[mask] == 1)) if n else 0
        lo, hi = wilson_ci(k, n) if n else (float("nan"), float("nan"))
        rows.append(
            {
                "band": name,
                "n": n,
                "n_default": k,
                "default_rate": (k / n) if n else float("nan"),
                "default_rate_ci_lower": lo,
                "default_rate_ci_upper": hi,
                "ci_method": "wilson_95",
            }
        )
    return rows


def policy_metrics(y: np.ndarray, decisions: np.ndarray, scenario: CostScenario | None = None) -> dict[str, Any]:
    counts = auto_confusion(y, decisions)
    payload: dict[str, Any] = dict(counts)
    if scenario is not None:
        payload["expected_normalized_cost"] = expected_normalized_cost(
            counts["fn"], counts["fp"], counts["n_review"], counts["n"], scenario
        )
        payload["cost_scenario"] = scenario.as_dict()
    payload["decision_bands"] = band_outcome_table(y, decisions)
    return payload
