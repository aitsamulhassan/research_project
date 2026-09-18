"""Shared modeling utilities. No test-set fitting."""

from __future__ import annotations

import hashlib
from typing import Any

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler

from preprocessing.lendingclub_preprocessor import NUMERIC_FEATURES, PRIMARY_PREDICTORS

N_NUMERIC = len(NUMERIC_FEATURES)
SEEDS = [42, 123, 2024, 3407, 9999]
FINAL_SEED = 42
EXPERIMENT_ID = "stage4b-lc-granting-v1"


def row_ref(loan_id: Any) -> str:
    return hashlib.sha256(f"lc-row|{loan_id}".encode("utf-8")).hexdigest()[:16]


def scale_pos_weight(y: np.ndarray) -> float:
    y = np.asarray(y)
    n_pos = float((y == 1).sum())
    n_neg = float((y == 0).sum())
    if n_pos == 0:
        raise ValueError("No positive labels in the fitting set.")
    return n_neg / n_pos


class NumericBlockScaler(BaseEstimator, TransformerMixin):
    """Standard-scale the leading numeric block of a Stage 4A matrix.

    Fitted only on the matrix passed to fit (train, or train+validation).
    One-hot columns are left unchanged. Used by logistic regression only.
    """

    def __init__(self, n_numeric: int = N_NUMERIC) -> None:
        self.n_numeric = n_numeric
        self.scaler_ = StandardScaler()

    def fit(self, X, y=None):
        block = _numeric_block(X, self.n_numeric)
        self.scaler_.fit(block)
        return self

    def transform(self, X):
        scaled = self.scaler_.transform(_numeric_block(X, self.n_numeric))
        rest = X[:, self.n_numeric :]
        scaled_sparse = sparse.csr_matrix(scaled)
        if sparse.issparse(rest):
            return sparse.hstack([scaled_sparse, rest], format="csr")
        return np.hstack([scaled, np.asarray(rest)])


def _numeric_block(X, n_numeric: int) -> np.ndarray:
    block = X[:, :n_numeric]
    if sparse.issparse(block):
        return block.toarray()
    return np.asarray(block)


def assert_predictor_frame(frame: pd.DataFrame) -> None:
    extra = [c for c in frame.columns if c not in PRIMARY_PREDICTORS]
    if extra:
        raise ValueError(f"Non-predictor columns passed to a model: {extra}")
    missing = [c for c in PRIMARY_PREDICTORS if c not in frame.columns]
    if missing:
        raise ValueError(f"Missing predictors: {missing}")
