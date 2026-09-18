"""Regularized logistic regression baseline."""

from __future__ import annotations

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from models.common import NumericBlockScaler


def logistic_pipeline(seed: int) -> Pipeline:
    return Pipeline(
        steps=[
            ("numeric_scale", NumericBlockScaler()),
            (
                "clf",
                LogisticRegression(
                    penalty="l2",
                    C=1.0,
                    solver="liblinear",
                    class_weight="balanced",
                    max_iter=300,
                    random_state=seed,
                    tol=1.0e-4,
                ),
            ),
        ]
    )


def logistic_config(seed: int) -> dict:
    return {
        "family": "logistic_regression",
        "solver": "liblinear",
        "penalty": "l2",
        "C": 1.0,
        "class_weight": "balanced",
        "max_iter": 300,
        "tol": 1.0e-4,
        "numeric_scaling": "StandardScaler on Stage 4A numeric block only, fit on current training matrix",
        "random_state": seed,
        "imbalance_strategy": "sklearn class_weight='balanced' (n_samples / (n_classes * n_class))",
    }
