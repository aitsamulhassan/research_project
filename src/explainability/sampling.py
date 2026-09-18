"""Deterministic explanation sampling. Labels are not used for selection."""

from __future__ import annotations

import numpy as np
import pandas as pd

from models.common import row_ref
from preprocessing.lendingclub_preprocessor import PRIMARY_PREDICTORS

SAMPLE_SEED = 42
SAMPLE_N = 5000


def deterministic_indices(n: int, size: int, seed: int) -> np.ndarray:
    if size > n:
        raise ValueError("Requested sample is larger than the split.")
    rng = np.random.RandomState(seed)
    chosen = rng.choice(n, size=size, replace=False)
    return np.sort(chosen)


def sample_split_frame(frame: pd.DataFrame, size: int = SAMPLE_N, seed: int = SAMPLE_SEED) -> pd.DataFrame:
    """Sample rows from an already-filtered split frame. Does not read labels."""
    idx = deterministic_indices(len(frame), size, seed)
    part = frame.iloc[idx].copy().reset_index(drop=True)
    part["source_iloc"] = idx
    part["sample_position"] = np.arange(len(part))
    part["row_ref"] = [row_ref(i) for i in part["id"].to_numpy()]
    return part


def assert_predictor_only(columns: list[str]) -> None:
    extra = [c for c in columns if c not in PRIMARY_PREDICTORS]
    if extra:
        raise ValueError(f"Non-predictor columns in explanation matrix: {extra}")
    missing = [c for c in PRIMARY_PREDICTORS if c not in columns]
    if missing:
        raise ValueError(f"Missing predictors: {missing}")
