"""Seed-level attribution stability. All seeds are reported; none is selected."""

from __future__ import annotations

import numpy as np
import pandas as pd

from explainability.ranking import overlap_at_k, ranks_from_importance, spearman_ranks
from preprocessing.lendingclub_preprocessor import PRIMARY_PREDICTORS


def rank_matrix(importances: dict[int, np.ndarray]) -> pd.DataFrame:
    rows = []
    for seed, imp in sorted(importances.items()):
        ranks = ranks_from_importance(imp)
        for i, name in enumerate(PRIMARY_PREDICTORS):
            rows.append({"seed": seed, "feature": name, "mean_abs": float(imp[i]), "rank": int(ranks[i])})
    return pd.DataFrame(rows)


def feature_stability(rank_frame: pd.DataFrame, n_seeds: int) -> pd.DataFrame:
    rows = []
    for name in PRIMARY_PREDICTORS:
        sub = rank_frame.loc[rank_frame["feature"] == name]
        ranks = sub["rank"].to_numpy()
        imps = sub["mean_abs"].to_numpy()
        rows.append(
            {
                "feature": name,
                "mean_importance": float(imps.mean()),
                "sd_importance": float(imps.std(ddof=1) if len(imps) > 1 else 0.0),
                "mean_rank": float(ranks.mean()),
                "rank_sd": float(ranks.std(ddof=1) if len(ranks) > 1 else 0.0),
                "top3_frequency": float((ranks <= 3).sum() / n_seeds),
                "top5_frequency": float((ranks <= 5).sum() / n_seeds),
            }
        )
    return pd.DataFrame(rows).sort_values("mean_rank").reset_index(drop=True)


def pairwise_spearman(importances: dict[int, np.ndarray]) -> pd.DataFrame:
    seeds = sorted(importances)
    rows = []
    for i, s1 in enumerate(seeds):
        for s2 in seeds[i + 1 :]:
            rows.append(
                {
                    "seed_a": s1,
                    "seed_b": s2,
                    "spearman": spearman_ranks(importances[s1], importances[s2]),
                    "top3_overlap": overlap_at_k(importances[s1], importances[s2], 3),
                    "top5_overlap": overlap_at_k(importances[s1], importances[s2], 5),
                }
            )
    return pd.DataFrame(rows)
