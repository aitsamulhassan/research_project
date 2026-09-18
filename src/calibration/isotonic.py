"""Isotonic calibration. Fit on validation probabilities only."""

from __future__ import annotations

import numpy as np
from sklearn.isotonic import IsotonicRegression


class IsotonicCalibrator:
    """Non-decreasing map from raw probabilities to calibrated probabilities.

    y_min=0, y_max=1, out_of_bounds='clip'. No test-set fitting.
    """

    def __init__(self) -> None:
        self.n_thresholds_: int | None = None
        self.y_min_ = 0.0
        self.y_max_ = 1.0
        self.out_of_bounds_ = "clip"
        self._iso: IsotonicRegression | None = None

    def fit(self, p_raw: np.ndarray, y: np.ndarray, *, split: str) -> "IsotonicCalibrator":
        if split != "validation":
            raise ValueError("Isotonic calibration may only be fit on validation.")
        y = np.asarray(y, dtype=float)
        if y.min() == y.max():
            raise ValueError("Validation labels must contain both classes.")
        iso = IsotonicRegression(
            y_min=self.y_min_,
            y_max=self.y_max_,
            increasing=True,
            out_of_bounds=self.out_of_bounds_,
        )
        iso.fit(np.asarray(p_raw, dtype=float), y)
        self._iso = iso
        x_thr = getattr(iso, "X_thresholds_", None)
        self.n_thresholds_ = int(len(x_thr)) if x_thr is not None else None
        return self

    def transform(self, p_raw: np.ndarray) -> np.ndarray:
        if self._iso is None:
            raise RuntimeError("IsotonicCalibrator has not been fitted.")
        return np.asarray(self._iso.transform(np.asarray(p_raw, dtype=float)), dtype=float)

    def record(self) -> dict:
        return {
            "method": "isotonic",
            "y_min": self.y_min_,
            "y_max": self.y_max_,
            "out_of_bounds": self.out_of_bounds_,
            "increasing": True,
            "n_thresholds": self.n_thresholds_,
            "clipping": "predictions outside the fitted raw-probability range are clipped to the boundary calibrated value",
            "random_seed": None,
            "fit_split": "validation",
        }
