"""Evaluation metrics for Stage 4B. No calibration or thresholding."""

from __future__ import annotations

from typing import Callable

import numpy as np
from sklearn.metrics import (
    average_precision_score,
    brier_score_loss,
    log_loss,
    roc_auc_score,
    roc_curve,
    precision_recall_curve,
)


def roc_auc(y_true: np.ndarray, p_hat: np.ndarray) -> float:
    return float(roc_auc_score(y_true, p_hat))


def pr_auc(y_true: np.ndarray, p_hat: np.ndarray) -> float:
    return float(average_precision_score(y_true, p_hat))


def brier(y_true: np.ndarray, p_hat: np.ndarray) -> float:
    return float(brier_score_loss(y_true, p_hat))


def logloss(y_true: np.ndarray, p_hat: np.ndarray) -> float:
    p = np.clip(np.asarray(p_hat, dtype=float), 1e-15, 1 - 1e-15)
    return float(log_loss(y_true, p, labels=[0, 1]))


METRIC_FUNCS: dict[str, Callable[[np.ndarray, np.ndarray], float]] = {
    "roc_auc": roc_auc,
    "pr_auc": pr_auc,
    "brier": brier,
    "log_loss": logloss,
}


def classification_metrics(y_true: np.ndarray, p_hat: np.ndarray) -> dict[str, float]:
    y = np.asarray(y_true)
    p = np.asarray(p_hat, dtype=float)
    if y.shape[0] != p.shape[0]:
        raise ValueError("y_true and p_hat length mismatch.")
    if y.min() == y.max():
        raise ValueError("Cannot compute discrimination metrics: only one class present.")
    return {
        "roc_auc": roc_auc(y, p),
        "pr_auc": pr_auc(y, p),
        "brier": brier(y, p),
        "log_loss": logloss(y, p),
        "n": int(y.shape[0]),
        "n_positive": int((y == 1).sum()),
        "prevalence": float((y == 1).mean()),
    }


def roc_curve_points(y_true: np.ndarray, p_hat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    fpr, tpr, _ = roc_curve(y_true, p_hat)
    return fpr, tpr


def pr_curve_points(y_true: np.ndarray, p_hat: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    precision, recall, _ = precision_recall_curve(y_true, p_hat)
    return recall, precision
