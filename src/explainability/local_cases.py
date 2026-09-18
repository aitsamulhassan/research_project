"""Deterministic local-case selection. Uses predictions/attributions, not labels."""

from __future__ import annotations

import numpy as np
import pandas as pd

from explainability.ranking import ranks_from_importance, spearman_ranks
from preprocessing.lendingclub_preprocessor import PRIMARY_PREDICTORS


def _tie_break(mask: np.ndarray, row_refs: np.ndarray) -> int:
    idx = np.flatnonzero(mask)
    if len(idx) == 0:
        raise RuntimeError("No rows matched a local-case rule.")
    order = np.argsort(row_refs[idx])
    return int(idx[order[0]])


def select_local_cases(
    p_raw: np.ndarray,
    shap_values: np.ndarray,
    ebm_terms: np.ndarray,
    row_refs: np.ndarray,
) -> dict[str, int]:
    """Return sample-position indices. Labels are not consulted."""
    p = np.asarray(p_raw, dtype=float)
    refs = np.asarray(row_refs)
    high = _tie_break(p == p.max(), refs)
    low = _tie_break(p == p.min(), refs)
    median = float(np.median(p))
    dist = np.abs(p - median)
    mid = _tie_break(dist == dist.min(), refs)

    disagreements = []
    for i in range(len(p)):
        corr = spearman_ranks(np.abs(shap_values[i]), np.abs(ebm_terms[i]))
        disagreements.append(corr)
    disagreements = np.asarray(disagreements, dtype=float)
    worst = disagreements.min()
    disagree = _tie_break(disagreements == worst, refs)

    used = {high, low, mid}
    if disagree in used:
        remaining = np.array([i for i in range(len(p)) if i not in used])
        worst_rem = disagreements[remaining].min()
        mask = np.zeros(len(p), dtype=bool)
        mask[remaining] = disagreements[remaining] == worst_rem
        disagree = _tie_break(mask, refs)

    return {
        "high_risk": high,
        "low_risk": low,
        "median_risk": mid,
        "disagreement": disagree,
        "disagreement_spearman": float(disagreements[disagree]),
    }


def local_payload(
    position: int,
    frame: pd.DataFrame,
    p_raw: np.ndarray,
    p_cal: np.ndarray,
    shap_values: np.ndarray,
    ebm_terms: np.ndarray,
    y_true: np.ndarray | None,
) -> dict:
    shap_row = shap_values[position]
    ebm_row = ebm_terms[position]
    shap_rank = ranks_from_importance(np.abs(shap_row))
    ebm_rank = ranks_from_importance(np.abs(ebm_row))
    features = []
    for i, name in enumerate(PRIMARY_PREDICTORS):
        features.append(
            {
                "feature": name,
                "value": frame.iloc[position][name],
                "shap": float(shap_row[i]),
                "ebm_term": float(ebm_row[i]),
                "shap_abs_rank": int(shap_rank[i]),
                "ebm_abs_rank": int(ebm_rank[i]),
            }
        )
    by_shap = sorted(features, key=lambda r: -abs(r["shap"]))
    pos = [r["feature"] for r in by_shap if r["shap"] > 0][:3]
    neg = [r["feature"] for r in by_shap if r["shap"] < 0][:3]
    out = {
        "sample_position": position,
        "row_ref": frame.iloc[position]["row_ref"],
        "p_raw": float(p_raw[position]),
        "p_calibrated": float(p_cal[position]),
        "top_positive_shap": pos,
        "top_negative_shap": neg,
        "local_rank_spearman": spearman_ranks(np.abs(shap_row), np.abs(ebm_row)),
        "features": features,
    }
    if y_true is not None:
        out["y_true_descriptive_only"] = int(y_true[position])
    return out
