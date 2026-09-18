"""XGBoost primary nonlinear model."""

from __future__ import annotations

from xgboost import XGBClassifier

from models.common import scale_pos_weight


def xgboost_model(seed: int, y_fit, n_estimators: int = 300, early_stopping_rounds: int | None = 30) -> XGBClassifier:
    kwargs = dict(
        objective="binary:logistic",
        eval_metric="logloss",
        n_estimators=n_estimators,
        learning_rate=0.05,
        max_depth=4,
        min_child_weight=20,
        subsample=0.8,
        colsample_bytree=0.8,
        reg_lambda=1.0,
        reg_alpha=0.0,
        scale_pos_weight=scale_pos_weight(y_fit),
        random_state=seed,
        n_jobs=-1,
        tree_method="hist",
    )
    if early_stopping_rounds is not None:
        kwargs["early_stopping_rounds"] = early_stopping_rounds
    return XGBClassifier(**kwargs)


def xgboost_config(seed: int, scale_pos_weight_value: float, n_estimators: int = 300) -> dict:
    return {
        "family": "xgboost",
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "n_estimators": n_estimators,
        "learning_rate": 0.05,
        "max_depth": 4,
        "min_child_weight": 20,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "reg_lambda": 1.0,
        "reg_alpha": 0.0,
        "scale_pos_weight": scale_pos_weight_value,
        "tree_method": "hist",
        "random_state": seed,
        "imbalance_strategy": "scale_pos_weight = n_neg/n_pos computed on the current fitting labels only",
        "early_stopping": "validation split only during the train/val phase; not used on test",
    }
