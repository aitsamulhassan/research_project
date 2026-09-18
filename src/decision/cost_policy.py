"""Relative-cost scenarios. Research assumptions, not institutional costs."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CostScenario:
    fn_fp_ratio: float
    c_fp: float = 1.0
    c_review_over_fp: float = 0.25
    label: str = "ASSUMED RELATIVE COST SCENARIO"

    def __post_init__(self) -> None:
        if self.fn_fp_ratio <= 0 or self.c_fp <= 0 or self.c_review_over_fp < 0:
            raise ValueError("Cost parameters must be positive (review cost may be zero).")

    @property
    def c_fn(self) -> float:
        return self.c_fp * float(self.fn_fp_ratio)

    @property
    def c_review(self) -> float:
        return self.c_fp * float(self.c_review_over_fp)

    @property
    def name(self) -> str:
        ratio = int(self.fn_fp_ratio) if float(self.fn_fp_ratio).is_integer() else self.fn_fp_ratio
        return f"FN:FP={ratio}:1"

    def as_dict(self) -> dict:
        return {
            "label": self.label,
            "name": self.name,
            "fn_fp_ratio": float(self.fn_fp_ratio),
            "c_fp": float(self.c_fp),
            "c_fn": float(self.c_fn),
            "c_review_over_fp": float(self.c_review_over_fp),
            "c_review": float(self.c_review),
            "assumption": "Researcher sensitivity scenario, not a real operational cost.",
        }


def expected_cost(fn: int, fp: int, n_review: int, scenario: CostScenario) -> float:
    return float(scenario.c_fn * fn + scenario.c_fp * fp + scenario.c_review * n_review)


def expected_normalized_cost(fn: int, fp: int, n_review: int, n: int, scenario: CostScenario) -> float:
    if n <= 0:
        raise ValueError("n must be positive.")
    return expected_cost(fn, fp, n_review, scenario) / float(n)


def confusion_from_masks(y: np.ndarray, approve: np.ndarray, reject: np.ndarray) -> dict[str, int]:
    y = np.asarray(y).astype(int)
    approve = np.asarray(approve, dtype=bool)
    reject = np.asarray(reject, dtype=bool)
    if approve.shape != y.shape or reject.shape != y.shape:
        raise ValueError("Mask length mismatch.")
    if np.any(approve & reject):
        raise ValueError("Approve and reject masks overlap.")
    fn = int(np.sum(approve & (y == 1)))
    tn = int(np.sum(approve & (y == 0)))
    fp = int(np.sum(reject & (y == 0)))
    tp = int(np.sum(reject & (y == 1)))
    n_review = int(np.sum(~approve & ~reject))
    return {"tp": tp, "tn": tn, "fp": fp, "fn": fn, "n_review": n_review, "n": int(y.size)}
