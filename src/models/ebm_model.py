"""Explainable Boosting Machine transparent nonlinear reference."""

from __future__ import annotations

from interpret.glassbox import ExplainableBoostingClassifier

from preprocessing.lendingclub_preprocessor import CATEGORICAL_FEATURES, NUMERIC_FEATURES, PRIMARY_PREDICTORS

EBM_FEATURE_TYPES = ["continuous"] * len(NUMERIC_FEATURES) + ["nominal"] * len(CATEGORICAL_FEATURES)


def ebm_model(seed: int) -> ExplainableBoostingClassifier:
    return ExplainableBoostingClassifier(
        feature_names=list(PRIMARY_PREDICTORS),
        feature_types=EBM_FEATURE_TYPES,
        interactions=0,
        max_bins=256,
        learning_rate=0.02,
        max_rounds=200,
        outer_bags=4,
        inner_bags=0,
        validation_size=0.15,
        early_stopping_rounds=20,
        n_jobs=-2,
        random_state=seed,
    )


def ebm_config(seed: int) -> dict:
    return {
        "family": "explainable_boosting_machine",
        "feature_names": list(PRIMARY_PREDICTORS),
        "feature_types": EBM_FEATURE_TYPES,
        "interactions": 0,
        "interaction_justification": (
            "Interactions are set to 0 before any test evaluation so EBM remains an "
            "additive per-original-feature reference. They are not added to improve test scores."
        ),
        "max_bins": 256,
        "learning_rate": 0.02,
        "max_rounds": 200,
        "outer_bags": 4,
        "inner_bags": 0,
        "validation_size": 0.15,
        "early_stopping_rounds": 20,
        "random_state": seed,
        "imbalance_strategy": "none (EBM 0.7.8 has no class_weight argument; labels are used as observed)",
        "input_representation": (
            "Stage 4A train-only (or train+val) imputers applied to the original 9 columns; "
            "one-hot expansion is not used because it would destroy EBM additive structure "
            "and exceed practical memory on 1023 dense dummy columns."
        ),
    }
