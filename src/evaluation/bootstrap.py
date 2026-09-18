"""Reproducible bootstrap confidence intervals. Used after model freeze only."""

from __future__ import annotations

from typing import Callable

import numpy as np


def bootstrap_ci(
    y_true: np.ndarray,
    p_hat: np.ndarray,
    metric_fn: Callable[[np.ndarray, np.ndarray], float],
    n_bootstrap: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> dict[str, float | int | str]:
    """Percentile bootstrap by resampling rows with replacement.

    Degenerate resamples (single class) are skipped. This procedure is for
    uncertainty on a frozen model, not for model selection.
    """
    y = np.asarray(y_true)
    p = np.asarray(p_hat, dtype=float)
    if y.shape[0] != p.shape[0]:
        raise ValueError("y_true and p_hat length mismatch.")
    rng = np.random.RandomState(seed)
    n = y.shape[0]
    stats: list[float] = []
    skipped = 0
    for _ in range(n_bootstrap):
        idx = rng.randint(0, n, size=n)
        y_b = y[idx]
        if y_b.min() == y_b.max():
            skipped += 1
            continue
        stats.append(float(metric_fn(y_b, p[idx])))
    if len(stats) < 50:
        raise RuntimeError("Too few valid bootstrap replicates.")
    alpha = (1.0 - confidence_level) / 2.0
    lower = float(np.percentile(stats, 100 * alpha))
    upper = float(np.percentile(stats, 100 * (1.0 - alpha)))
    point = float(metric_fn(y, p))
    return {
        "point": point,
        "ci_lower": lower,
        "ci_upper": upper,
        "n_bootstrap": int(n_bootstrap),
        "n_valid": int(len(stats)),
        "n_skipped_degenerate": int(skipped),
        "confidence_level": float(confidence_level),
        "seed": int(seed),
        "method": "percentile_bootstrap_rows_with_replacement",
    }


def bootstrap_paired_diff(
    y_true: np.ndarray,
    p_calibrated: np.ndarray,
    p_raw: np.ndarray,
    metric_fn: Callable[[np.ndarray, np.ndarray], float],
    n_bootstrap: int = 1000,
    confidence_level: float = 0.95,
    seed: int = 42,
) -> dict[str, float | int | str]:
    """Percentile bootstrap of metric(calibrated) - metric(raw). Not for tuning."""
    y = np.asarray(y_true)
    p_c = np.asarray(p_calibrated, dtype=float)
    p_r = np.asarray(p_raw, dtype=float)
    if y.shape[0] != p_c.shape[0] or y.shape[0] != p_r.shape[0]:
        raise ValueError("Array length mismatch.")
    rng = np.random.RandomState(seed)
    n = y.shape[0]
    stats: list[float] = []
    skipped = 0
    for _ in range(n_bootstrap):
        idx = rng.randint(0, n, size=n)
        y_b = y[idx]
        if y_b.min() == y_b.max():
            skipped += 1
            continue
        stats.append(float(metric_fn(y_b, p_c[idx]) - metric_fn(y_b, p_r[idx])))
    if len(stats) < 50:
        raise RuntimeError("Too few valid bootstrap replicates.")
    alpha = (1.0 - confidence_level) / 2.0
    lower = float(np.percentile(stats, 100 * alpha))
    upper = float(np.percentile(stats, 100 * (1.0 - alpha)))
    point = float(metric_fn(y, p_c) - metric_fn(y, p_r))
    return {
        "point": point,
        "ci_lower": lower,
        "ci_upper": upper,
        "n_bootstrap": int(n_bootstrap),
        "n_valid": int(len(stats)),
        "n_skipped_degenerate": int(skipped),
        "confidence_level": float(confidence_level),
        "seed": int(seed),
        "method": "percentile_bootstrap_paired_rows_with_replacement",
        "direction": "calibrated_minus_raw",
        "negative_means_improvement": True,
    }
