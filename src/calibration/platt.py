"""Platt / logistic calibration. Fit on validation scores only."""

from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression

EPS = 1e-15


def logit(p: np.ndarray) -> np.ndarray:
    x = np.clip(np.asarray(p, dtype=float), EPS, 1.0 - EPS)
    return np.log(x / (1.0 - x))


def sigmoid(z: np.ndarray) -> np.ndarray:
    z = np.asarray(z, dtype=float)
    return 1.0 / (1.0 + np.exp(-z))


class PlattCalibrator:
    """Unregularized logistic calibration: sigmoid(a * logit(p_raw) + b).

    The Stage 4B artifacts store probabilities, not decision scores. The raw
    score used here is therefore logit(p_raw). Parameters are learned only from
    the arrays passed to fit; the caller must pass validation data and the
    split='validation' guard.
    """

    def __init__(self, max_iter: int = 1000) -> None:
        self.max_iter = max_iter
        self.coef_: float | None = None
        self.intercept_: float | None = None
        self.n_iter_: int | None = None
        self.converged_: bool | None = None
        self.solver_ = "lbfgs"
        self.penalty_ = "none (C=np.inf)"

    def fit(self, p_raw: np.ndarray, y: np.ndarray, *, split: str) -> "PlattCalibrator":
        if split != "validation":
            raise ValueError("Platt calibration may only be fit on validation.")
        y = np.asarray(y)
        if y.min() == y.max():
            raise ValueError("Validation labels must contain both classes.")
        z = logit(p_raw).reshape(-1, 1)
        clf = LogisticRegression(
            solver="lbfgs",
            C=np.inf,
            max_iter=self.max_iter,
            tol=1e-6,
        )
        clf.fit(z, y)
        self.coef_ = float(clf.coef_[0, 0])
        self.intercept_ = float(clf.intercept_[0])
        self.n_iter_ = int(np.max(np.atleast_1d(clf.n_iter_)))
        self.converged_ = self.n_iter_ < clf.max_iter
        self._clf = clf
        return self

    def transform(self, p_raw: np.ndarray) -> np.ndarray:
        if self.coef_ is None:
            raise RuntimeError("PlattCalibrator has not been fitted.")
        z = logit(p_raw)
        return sigmoid(self.coef_ * z + self.intercept_)

    def record(self) -> dict:
        return {
            "method": "platt",
            "form": "sigmoid(a * logit(p_raw) + b)",
            "a": self.coef_,
            "b": self.intercept_,
            "solver": self.solver_,
            "penalty": self.penalty_,
            "max_iter": self.max_iter,
            "n_iter": self.n_iter_,
            "converged": self.converged_,
            "fit_split": "validation",
        }
