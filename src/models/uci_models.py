"""UCI-specific model factories. Hyperparameters are not copied from LendingClub configs."""

from __future__ import annotations

import numpy as np
from interpret.glassbox import ExplainableBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

from preprocessing.uci_preprocessor import EBM_FEATURE_TYPES, UCI_PREDICTORS


def scale_pos_weight(y: np.ndarray) -> float:
    y = np.asarray(y)
    n_pos = float((y == 1).sum())
    n_neg = float((y == 0).sum())
    if n_pos == 0:
        raise ValueError("No positive labels in the UCI fitting set.")
    return n_neg / n_pos


def logistic_model(seed: int) -> LogisticRegression:
    return LogisticRegression(
        penalty="l2",
        C=1.0,
        solver="lbfgs",
        class_weight="balanced",
        max_iter=1000,
        random_state=seed,
        tol=1.0e-4,
    )


def logistic_config(seed: int) -> dict:
    return {
        "family": "logistic_regression",
        "dataset": "uci",
        "solver": "lbfgs",
        "penalty": "l2",
        "C": 1.0,
        "class_weight": "balanced",
        "max_iter": 1000,
        "tol": 1.0e-4,
        "random_state": seed,
        "justification": (
            "UCI n≈21k, 23 mixed features after train-only one-hot. lbfgs L2 with sklearn default C=1.0. "
            "class_weight='balanced' is justified by UCI prevalence ≈0.221, not by copying LendingClub liblinear settings."
        ),
        "lendingclub_hyperparameters_transferred": False,
    }


def ebm_model(seed: int) -> ExplainableBoostingClassifier:
    return ExplainableBoostingClassifier(
        feature_names=list(UCI_PREDICTORS),
        feature_types=list(EBM_FEATURE_TYPES),
        interactions=0,
        max_bins=256,
        learning_rate=0.01,
        max_rounds=500,
        outer_bags=8,
        inner_bags=0,
        validation_size=0.15,
        early_stopping_rounds=50,
        n_jobs=2,
        random_state=seed,
    )


def ebm_config(seed: int) -> dict:
    return {
        "family": "explainable_boosting_machine",
        "dataset": "uci",
        "feature_names": list(UCI_PREDICTORS),
        "feature_types": list(EBM_FEATURE_TYPES),
        "interactions": 0,
        "interaction_justification": "Frozen U1 / Stage 9 protocol: additive per-feature EBM; interactions not added to chase TEST scores.",
        "max_bins": 256,
        "learning_rate": 0.01,
        "max_rounds": 500,
        "outer_bags": 8,
        "inner_bags": 0,
        "validation_size": 0.15,
        "early_stopping_rounds": 50,
        "random_state": seed,
        "justification": (
            "UCI-sized additive EBM: interpret-default learning_rate 0.01 and outer_bags 8, max_rounds capped at 500 "
            "because n=20999. These are not LendingClub Stage 4B values (those were lr=0.02, max_rounds=200, outer_bags=4)."
        ),
        "lendingclub_hyperparameters_transferred": False,
        "imbalance_strategy": "none (interpret 0.7.8 has no class_weight; labels used as observed)",
    }


def xgboost_model(seed: int, y_fit, n_estimators: int = 400, early_stopping_rounds: int | None = 30) -> XGBClassifier:
    kwargs = dict(
        objective="binary:logistic",
        eval_metric="logloss",
        n_estimators=n_estimators,
        learning_rate=0.1,
        max_depth=3,
        min_child_weight=10,
        subsample=1.0,
        colsample_bytree=1.0,
        reg_lambda=1.0,
        reg_alpha=0.0,
        scale_pos_weight=scale_pos_weight(y_fit),
        random_state=seed,
        n_jobs=2,
        tree_method="hist",
    )
    if early_stopping_rounds is not None:
        kwargs["early_stopping_rounds"] = early_stopping_rounds
    return XGBClassifier(**kwargs)


def xgboost_config(seed: int, scale_pos_weight_value: float, n_estimators: int = 400) -> dict:
    return {
        "family": "xgboost",
        "dataset": "uci",
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "n_estimators": n_estimators,
        "learning_rate": 0.1,
        "max_depth": 3,
        "min_child_weight": 10,
        "subsample": 1.0,
        "colsample_bytree": 1.0,
        "reg_lambda": 1.0,
        "reg_alpha": 0.0,
        "scale_pos_weight": scale_pos_weight_value,
        "tree_method": "hist",
        "random_state": seed,
        "justification": (
            "UCI n≈21k with one-hot mixed features. Depth 3, lr=0.1, min_child_weight=10, no column/row subsampling. "
            "Not LendingClub XGBoost (those were depth 4, lr=0.05, min_child_weight=20, subsample=0.8, colsample=0.8, 300 trees)."
        ),
        "lendingclub_hyperparameters_transferred": False,
        "early_stopping": "UCI validation only during train/val; not used on UCI TEST",
        "imbalance_strategy": "scale_pos_weight = n_neg/n_pos on the current UCI fitting labels only",
    }


def predict_positive(model, x) -> np.ndarray:
    proba = model.predict_proba(x)
    return np.asarray(proba[:, 1], dtype=float)
