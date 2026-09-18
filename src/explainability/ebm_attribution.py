"""EBM native term contributions. Logit / link scale. Not causal effects."""

from __future__ import annotations

import numpy as np
import pandas as pd

from preprocessing.lendingclub_preprocessor import CATEGORICAL_FEATURES, NUMERIC_FEATURES, PRIMARY_PREDICTORS


def eval_terms(model, frame: pd.DataFrame) -> np.ndarray:
    x = frame.loc[:, PRIMARY_PREDICTORS]
    terms = np.asarray(model.eval_terms(x), dtype=float)
    if terms.shape[1] != len(PRIMARY_PREDICTORS):
        raise RuntimeError("EBM term count does not match the frozen predictor set.")
    return terms


def intercept(model) -> float:
    value = np.asarray(model.intercept_, dtype=float).reshape(-1)
    return float(value[0])


def decision_from_terms(terms: np.ndarray, intercept_value: float) -> np.ndarray:
    return terms.sum(axis=1) + intercept_value


def global_abs_stats(contributions: np.ndarray) -> pd.DataFrame:
    abs_c = np.abs(contributions)
    rows = []
    for i, name in enumerate(PRIMARY_PREDICTORS):
        col = abs_c[:, i]
        rows.append(
            {
                "feature": name,
                "mean_abs": float(col.mean()),
                "median_abs": float(np.median(col)),
                "std_abs": float(col.std(ddof=1)),
                "p25_abs": float(np.quantile(col, 0.25)),
                "p75_abs": float(np.quantile(col, 0.75)),
                "mean_signed": float(contributions[:, i].mean()),
            }
        )
    out = pd.DataFrame(rows)
    out["rank"] = out["mean_abs"].rank(ascending=False, method="first").astype(int)
    return out.sort_values("rank").reset_index(drop=True)


def shape_function(model, feature: str) -> dict:
    names = list(model.explain_global().data()["names"])
    idx = names.index(feature)
    payload = model.explain_global().data(idx)
    return {
        "feature": feature,
        "type": "continuous" if feature in NUMERIC_FEATURES else "categorical",
        "names": list(payload["names"]),
        "scores": [float(s) for s in np.asarray(payload["scores"], dtype=float)],
        "scale": "EBM additive term on logit/link scale",
    }


def feature_type(name: str) -> str:
    if name in NUMERIC_FEATURES:
        return "continuous"
    if name in CATEGORICAL_FEATURES:
        return "categorical"
    raise KeyError(name)
