"""Random Forest nonlinear baseline."""

from __future__ import annotations

from sklearn.ensemble import RandomForestClassifier


def random_forest_model(seed: int) -> RandomForestClassifier:
    return RandomForestClassifier(
        n_estimators=80,
        max_depth=12,
        min_samples_leaf=100,
        max_features="sqrt",
        class_weight="balanced",
        random_state=seed,
        n_jobs=4,
        # Sparse Stage-4A matrices are used as CSC; sklearn 1.9 accepts sparse CSC.
        bootstrap=True,
    )


def random_forest_config(seed: int) -> dict:
    return {
        "family": "random_forest",
        "n_estimators": 80,
        "max_depth": 12,
        "min_samples_leaf": 100,
        "max_features": "sqrt",
        "class_weight": "balanced",
        "bootstrap": True,
        "n_jobs": 4,
        "random_state": seed,
        "imbalance_strategy": "sklearn class_weight='balanced'",
        "input_representation": (
            "Stage 4A sparse matrix converted to CSC float32. Not densified; "
            "sklearn 1.9 RandomForestClassifier accepts sparse CSC."
        ),
        "size_justification": (
            "80 trees, depth 12, leaf 100: small enough for reproducible training on "
            "~941k rows x 1023 features without an uncontrolled search."
        ),
    }
