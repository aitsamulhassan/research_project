"""Calibration metrics. ECE/MCE binning is declared here and is not a test-tuned choice."""

from __future__ import annotations

import numpy as np

from evaluation.metrics import brier, logloss, pr_auc, roc_auc

N_BINS = 10
BINNING = "equal_width"
BIN_EDGES = np.linspace(0.0, 1.0, N_BINS + 1)
EMPTY_BIN_POLICY = "exclude_from_ece_and_mce"
RISK_RANGES = [
    (0.00, 0.10),
    (0.10, 0.20),
    (0.20, 0.30),
    (0.30, 0.50),
    (0.50, 1.00),
]
MIN_N_STABLE = 50


def _bin_index(p: np.ndarray, n_bins: int = N_BINS) -> np.ndarray:
    p = np.clip(np.asarray(p, dtype=float), 0.0, 1.0)
    idx = np.floor(p * n_bins).astype(int)
    idx = np.clip(idx, 0, n_bins - 1)
    return idx


def reliability_table(y_true: np.ndarray, p_hat: np.ndarray, n_bins: int = N_BINS) -> list[dict]:
    y = np.asarray(y_true)
    p = np.asarray(p_hat, dtype=float)
    idx = _bin_index(p, n_bins)
    rows = []
    for b in range(n_bins):
        mask = idx == b
        n = int(mask.sum())
        left = b / n_bins
        right = (b + 1) / n_bins
        if n == 0:
            rows.append(
                {
                    "bin": b,
                    "bin_left": left,
                    "bin_right": right,
                    "n": 0,
                    "mean_predicted": None,
                    "observed_rate": None,
                    "gap": None,
                    "empty": True,
                }
            )
            continue
        mean_p = float(p[mask].mean())
        obs = float(y[mask].mean())
        rows.append(
            {
                "bin": b,
                "bin_left": left,
                "bin_right": right,
                "n": n,
                "mean_predicted": mean_p,
                "observed_rate": obs,
                "gap": float(obs - mean_p),
                "empty": False,
            }
        )
    return rows


def ece(y_true: np.ndarray, p_hat: np.ndarray, n_bins: int = N_BINS) -> float:
    """Expected Calibration Error with declared equal-width bins.

    ECE = sum_{non-empty b} (n_b / n) * |observed_rate_b - mean_predicted_b|.
    Empty bins contribute nothing. This is a common but not unique definition.
    """
    y = np.asarray(y_true)
    p = np.asarray(p_hat, dtype=float)
    n = y.shape[0]
    if n == 0:
        raise ValueError("Empty arrays.")
    total = 0.0
    for row in reliability_table(y, p, n_bins):
        if row["empty"]:
            continue
        total += (row["n"] / n) * abs(row["gap"])
    return float(total)


def mce(y_true: np.ndarray, p_hat: np.ndarray, n_bins: int = N_BINS) -> float:
    """Maximum Calibration Error: max |gap| over non-empty equal-width bins."""
    gaps = [abs(row["gap"]) for row in reliability_table(y_true, p_hat, n_bins) if not row["empty"]]
    if not gaps:
        raise ValueError("All bins empty.")
    return float(max(gaps))


def risk_range_table(y_true: np.ndarray, p_hat: np.ndarray) -> list[dict]:
    y = np.asarray(y_true)
    p = np.asarray(p_hat, dtype=float)
    rows = []
    n_ranges = len(RISK_RANGES)
    for i, (left, right) in enumerate(RISK_RANGES):
        if i == n_ranges - 1:
            mask = (p >= left) & (p <= right)
        else:
            mask = (p >= left) & (p < right)
        n = int(mask.sum())
        if n == 0:
            rows.append(
                {
                    "range_left": left,
                    "range_right": right,
                    "range_label": f"{left:.2f}–{right:.2f}",
                    "n": 0,
                    "mean_predicted": None,
                    "observed_rate": None,
                    "gap": None,
                    "stable": False,
                }
            )
            continue
        mean_p = float(p[mask].mean())
        obs = float(y[mask].mean())
        rows.append(
            {
                "range_left": left,
                "range_right": right,
                "range_label": f"{left:.2f}–{right:.2f}",
                "n": n,
                "mean_predicted": mean_p,
                "observed_rate": obs,
                "gap": float(obs - mean_p),
                "stable": n >= MIN_N_STABLE,
            }
        )
    return rows


def calibration_metrics(y_true: np.ndarray, p_hat: np.ndarray) -> dict[str, float]:
    y = np.asarray(y_true)
    p = np.asarray(p_hat, dtype=float)
    if y.shape[0] != p.shape[0]:
        raise ValueError("y_true and p_hat length mismatch.")
    if np.isnan(p).any() or np.isinf(p).any():
        raise ValueError("Probabilities contain NaN or inf.")
    if y.min() == y.max():
        raise ValueError("Cannot compute discrimination metrics: only one class present.")
    return {
        "brier": brier(y, p),
        "log_loss": logloss(y, p),
        "ece": ece(y, p),
        "mce": mce(y, p),
        "roc_auc": roc_auc(y, p),
        "pr_auc": pr_auc(y, p),
        "n": float(y.shape[0]),
        "n_positive": float((y == 1).sum()),
        "prevalence": float((y == 1).mean()),
    }


CALIB_METRIC_FUNCS = {
    "brier": brier,
    "log_loss": logloss,
    "ece": ece,
    "mce": mce,
    "roc_auc": roc_auc,
    "pr_auc": pr_auc,
}

ECE_RECORD = {
    "n_bins": N_BINS,
    "binning": BINNING,
    "bin_edges": BIN_EDGES.tolist(),
    "empty_bins": EMPTY_BIN_POLICY,
    "formula": "sum_b (n_b / n) * |acc_b - conf_b| over non-empty bins",
}
