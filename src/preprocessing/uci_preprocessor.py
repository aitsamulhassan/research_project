"""UCI-only train-fit preprocessor. Does not load or transform LendingClub."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

UCI_TARGET = "default payment next month"
UCI_ID = "ID"

CONTINUOUS_FEATURES = [
    "LIMIT_BAL",
    "AGE",
    "BILL_AMT1",
    "BILL_AMT2",
    "BILL_AMT3",
    "BILL_AMT4",
    "BILL_AMT5",
    "BILL_AMT6",
    "PAY_AMT1",
    "PAY_AMT2",
    "PAY_AMT3",
    "PAY_AMT4",
    "PAY_AMT5",
    "PAY_AMT6",
]
NOMINAL_FEATURES = [
    "SEX",
    "EDUCATION",
    "MARRIAGE",
    "PAY_0",
    "PAY_2",
    "PAY_3",
    "PAY_4",
    "PAY_5",
    "PAY_6",
]
UCI_PREDICTORS = [
    "LIMIT_BAL",
    "SEX",
    "EDUCATION",
    "MARRIAGE",
    "AGE",
    "PAY_0",
    "PAY_2",
    "PAY_3",
    "PAY_4",
    "PAY_5",
    "PAY_6",
    "BILL_AMT1",
    "BILL_AMT2",
    "BILL_AMT3",
    "BILL_AMT4",
    "BILL_AMT5",
    "BILL_AMT6",
    "PAY_AMT1",
    "PAY_AMT2",
    "PAY_AMT3",
    "PAY_AMT4",
    "PAY_AMT5",
    "PAY_AMT6",
]
EBM_FEATURE_TYPES = [
    "continuous" if name in CONTINUOUS_FEATURES else "nominal" for name in UCI_PREDICTORS
]
FORBIDDEN_LC_COLUMNS = {
    "loan_amnt",
    "fico_n",
    "dti_n",
    "revenue",
    "purpose",
    "home_ownership_n",
    "addr_state",
    "zip_code",
    "Default",
    "issue_d",
    "experience_c",
}


class UCIPreprocessor:
    """Train-only StandardScaler + OneHotEncoder. Undocumented codes stay as levels."""

    def __init__(self) -> None:
        self.transformer_: ColumnTransformer | None = None
        self.feature_names_out_: list[str] | None = None
        self.n_features_in_ = len(UCI_PREDICTORS)

    def fit(self, frame: pd.DataFrame) -> "UCIPreprocessor":
        prepared = prepare_frame(frame)
        transformer = ColumnTransformer(
            transformers=[
                ("num", StandardScaler(), CONTINUOUS_FEATURES),
                (
                    "cat",
                    OneHotEncoder(handle_unknown="ignore", sparse_output=False, dtype=np.float64),
                    NOMINAL_FEATURES,
                ),
            ],
            remainder="drop",
        )
        transformer.fit(prepared)
        self.transformer_ = transformer
        self.feature_names_out_ = _names(transformer)
        return self

    def transform(self, frame: pd.DataFrame) -> np.ndarray:
        if self.transformer_ is None:
            raise RuntimeError("UCIPreprocessor has not been fitted.")
        prepared = prepare_frame(frame)
        return np.asarray(self.transformer_.transform(prepared), dtype=np.float64)

    def record(self) -> dict:
        return {
            "dataset": "uci_default_of_credit_card_clients",
            "fit_split": "train",
            "numeric_scaling": "StandardScaler on UCI continuous columns, train-fit only",
            "categorical_encoding": "OneHotEncoder handle_unknown=ignore, undocumented codes retained as observed levels",
            "recode_applied": False,
            "lendingclub_imputer_applied": False,
            "n_features_out": None if self.feature_names_out_ is None else len(self.feature_names_out_),
        }


def prepare_frame(frame: pd.DataFrame) -> pd.DataFrame:
    _assert_uci_frame(frame)
    out = pd.DataFrame(index=frame.index)
    for name in CONTINUOUS_FEATURES:
        out[name] = pd.to_numeric(frame[name], errors="coerce").astype(float)
    for name in NOMINAL_FEATURES:
        out[name] = frame[name].map(_nominal_token)
    return out


def ebm_frame(frame: pd.DataFrame) -> pd.DataFrame:
    """Original 23 columns; nominal codes as strings so undocumented values stay distinct."""
    prepared = prepare_frame(frame)
    ordered = pd.DataFrame(index=prepared.index)
    for name in UCI_PREDICTORS:
        ordered[name] = prepared[name]
    return ordered


def _nominal_token(value) -> str:
    if pd.isna(value):
        return "__missing__"
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    text = str(value).strip()
    try:
        return str(int(float(text)))
    except ValueError:
        return text


def _names(transformer: ColumnTransformer) -> list[str]:
    names = list(CONTINUOUS_FEATURES)
    encoder: OneHotEncoder = transformer.named_transformers_["cat"]
    for col, levels in zip(NOMINAL_FEATURES, encoder.categories_):
        for level in levels:
            names.append(f"{col}={level}")
    return names


def _assert_uci_frame(frame: pd.DataFrame) -> None:
    missing = [c for c in UCI_PREDICTORS if c not in frame.columns]
    if missing:
        raise ValueError(f"Missing UCI predictors: {missing}")
    extra_lc = [c for c in frame.columns if c in FORBIDDEN_LC_COLUMNS]
    if extra_lc:
        raise ValueError(f"LendingClub columns passed to UCI preprocessor: {extra_lc}")
