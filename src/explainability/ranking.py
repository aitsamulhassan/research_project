"""Ranking and agreement utilities. No causal interpretation."""

from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, spearmanr

from preprocessing.lendingclub_preprocessor import PRIMARY_PREDICTORS


def ranks_from_importance(importance: np.ndarray) -> np.ndarray:
    """Rank 1 = largest importance. Ties broken by lower index (frozen feature order)."""
    order = np.lexsort((np.arange(len(importance)), -np.asarray(importance, dtype=float)))
    ranks = np.empty(len(importance), dtype=int)
    ranks[order] = np.arange(1, len(importance) + 1)
    return ranks


def top_k_set(importance: np.ndarray, k: int) -> set[str]:
    ranks = ranks_from_importance(importance)
    return {PRIMARY_PREDICTORS[i] for i in range(len(PRIMARY_PREDICTORS)) if ranks[i] <= k}


def overlap_at_k(imp_a: np.ndarray, imp_b: np.ndarray, k: int) -> float:
    return len(top_k_set(imp_a, k) & top_k_set(imp_b, k)) / float(k)


def spearman_ranks(imp_a: np.ndarray, imp_b: np.ndarray) -> float:
    ra = ranks_from_importance(imp_a)
    rb = ranks_from_importance(imp_b)
    corr, _ = spearmanr(ra, rb)
    return float(corr)


def kendall_ranks(imp_a: np.ndarray, imp_b: np.ndarray) -> float:
    ra = ranks_from_importance(imp_a)
    rb = ranks_from_importance(imp_b)
    corr, _ = kendalltau(ra, rb)
    return float(corr)


def spearman_footrule(imp_a: np.ndarray, imp_b: np.ndarray) -> dict[str, float]:
    ra = ranks_from_importance(imp_a)
    rb = ranks_from_importance(imp_b)
    distance = float(np.abs(ra - rb).sum())
    n = len(ra)
    max_dist = float((n * n) // 2)
    return {"footrule": distance, "footrule_normalized": distance / max_dist if max_dist else 0.0}


def sign_agreement(a: np.ndarray, b: np.ndarray) -> float:
    sa = np.sign(a)
    sb = np.sign(b)
    mask = (sa != 0) | (sb != 0)
    if mask.sum() == 0:
        return 1.0
    return float((sa[mask] == sb[mask]).mean())


def comparison_table(shap_mean_abs: np.ndarray, ebm_mean_abs: np.ndarray) -> pd.DataFrame:
    shap_rank = ranks_from_importance(shap_mean_abs)
    ebm_rank = ranks_from_importance(ebm_mean_abs)
    return pd.DataFrame(
        {
            "feature": PRIMARY_PREDICTORS,
            "shap_mean_abs": shap_mean_abs,
            "shap_rank": shap_rank,
            "ebm_mean_abs": ebm_mean_abs,
            "ebm_rank": ebm_rank,
        }
    ).sort_values("shap_rank").reset_index(drop=True)
