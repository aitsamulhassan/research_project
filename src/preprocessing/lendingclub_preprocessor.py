"""Stage 4A leakage-safe LendingClub preprocessor.

Fits exclusively on TRAIN. Does not train models, does not modify data/raw/,
and refuses target/time-index/identifier/excluded columns.
"""

from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from data.audit_datasets import (  # noqa: E402
    EXPECTED_LC_FILENAME,
    RAW_DIR,
    REPO_ROOT,
    git_commit,
    load_lendingclub,
    sha256_file,
)

SCRIPT_VERSION = "stage4a-0.1.0"
RECORDED_LC_SHA256 = "207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc"

PRIMARY_PREDICTORS = [
    "revenue",
    "dti_n",
    "loan_amnt",
    "fico_n",
    "emp_length",
    "purpose",
    "home_ownership_n",
    "addr_state",
    "zip_code",
]
NUMERIC_FEATURES = ["revenue", "dti_n", "loan_amnt", "fico_n"]
CATEGORICAL_FEATURES = [
    "emp_length",
    "purpose",
    "home_ownership_n",
    "addr_state",
    "zip_code",
]
FORBIDDEN_COLUMNS = {
    "Default",
    "issue_d",
    "experience_c",
    "id",
    "title",
    "desc",
}
MISSING_TOKEN = "__MISSING__"
DTI_SENTINEL = 999.0

DOCS_DIR = REPO_ROOT / "docs"
RESULTS_TABLES = REPO_ROOT / "results" / "tables"
RESULTS_METRICS = REPO_ROOT / "results" / "metrics"
ARTIFACTS_DIR = REPO_ROOT / "results" / "artifacts"
AUDIT_DIR = REPO_ROOT / "audit"
ASSIGNMENTS_PATH = REPO_ROOT / "results" / "tables" / "lendingclub_split_assignments.csv"
SPLIT_MANIFEST_PATH = REPO_ROOT / "audit" / "lendingclub_split_manifest.json"
FEATURE_POLICY_PATH = REPO_ROOT / "docs" / "lendingclub_feature_policy.csv"
PREPROCESS_POLICY_PATH = DOCS_DIR / "lendingclub_preprocessing_policy.csv"
PREPROCESSOR_PATH = ARTIFACTS_DIR / "lendingclub_preprocessor.joblib"

POLICY_FIELDS = ["column", "dtype", "preprocessing_operation", "fit_on", "reason"]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def sha256_text_file(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest().lower()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def preprocessing_policy_rows() -> list[dict[str, str]]:
    return [
        {
            "column": "revenue",
            "dtype": "float64",
            "preprocessing_operation": "median_impute_then_passthrough",
            "fit_on": "TRAIN_ONLY",
            "reason": (
                "Train-only schema: continuous numeric. No missing values in TRAIN. "
                "Median imputer is fitted on TRAIN as a transform-time safety policy. "
                "No scaling, clipping, winsorizing, or log transform: those would be "
                "performance-motivated, not required by the schema."
            ),
        },
        {
            "column": "dti_n",
            "dtype": "float64",
            "preprocessing_operation": "median_impute_then_passthrough_preserve_999",
            "fit_on": "TRAIN_ONLY",
            "reason": (
                "Train-only schema: continuous numeric. Research-owner freeze: preserve "
                "original values. dti_n==999 is left unchanged because its interpretation "
                "as missing/invalid is unconfirmed. No clipping of extreme DTI."
            ),
        },
        {
            "column": "loan_amnt",
            "dtype": "int64",
            "preprocessing_operation": "median_impute_then_passthrough",
            "fit_on": "TRAIN_ONLY",
            "reason": (
                "Train-only schema: continuous numeric requested amount. No missing values "
                "in TRAIN. Median imputer fitted on TRAIN only. No scaling or clipping."
            ),
        },
        {
            "column": "fico_n",
            "dtype": "float64",
            "preprocessing_operation": "median_impute_then_passthrough",
            "fit_on": "TRAIN_ONLY",
            "reason": (
                "Train-only schema: continuous FICO average. Train min/max lie inside the "
                "documented 300-850 range. No missing values in TRAIN. No rescaling."
            ),
        },
        {
            "column": "emp_length",
            "dtype": "string",
            "preprocessing_operation": "constant_impute_then_one_hot",
            "fit_on": "TRAIN_ONLY",
            "reason": (
                "Train-only schema: 12 string categories, including documented NI "
                "(no-information). Not numeric. NI is a real category, not converted to NA. "
                "One-hot encoder fitted on TRAIN; unseen labels at transform become all-zero."
            ),
        },
        {
            "column": "purpose",
            "dtype": "string",
            "preprocessing_operation": "constant_impute_then_one_hot",
            "fit_on": "TRAIN_ONLY",
            "reason": (
                "Train-only schema: 14 string purpose categories. One-hot encoder fitted on "
                "TRAIN only. Unseen validation/test labels are not inspected to build mappings; "
                "they are handled by handle_unknown='ignore'."
            ),
        },
        {
            "column": "home_ownership_n",
            "dtype": "string",
            "preprocessing_operation": "constant_impute_then_one_hot",
            "fit_on": "TRAIN_ONLY",
            "reason": (
                "Train-only schema: 4 string categories (MORTGAGE, RENT, OWN, OTHER). "
                "Categorical, not numeric. One-hot fitted on TRAIN only."
            ),
        },
        {
            "column": "addr_state",
            "dtype": "string",
            "preprocessing_operation": "constant_impute_then_one_hot",
            "fit_on": "TRAIN_ONLY",
            "reason": (
                "Train-only schema: 51 US state codes. One-hot fitted on TRAIN only. "
                "Unseen codes at transform are all-zero (handle_unknown='ignore')."
            ),
        },
        {
            "column": "zip_code",
            "dtype": "string",
            "preprocessing_operation": "constant_impute_then_one_hot",
            "fit_on": "TRAIN_ONLY",
            "reason": (
                "Train-only schema: 938 masked 5-character zip prefixes (e.g. 190xx). "
                "Categorical, not numeric. High-cardinality one-hot is the encoding of the "
                "retained predictor; no frequency threshold was invented. Unseen zips at "
                "transform are all-zero. Zero missing values in TRAIN; transform-time NA is "
                "filled with a token that, because it is absent from TRAIN, follows the same "
                "unseen-category rule."
            ),
        },
    ]


def write_preprocessing_policy() -> Path:
    import csv

    rows = preprocessing_policy_rows()
    PREPROCESS_POLICY_PATH.parent.mkdir(parents=True, exist_ok=True)
    with PREPROCESS_POLICY_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=POLICY_FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return PREPROCESS_POLICY_PATH


def _assert_allowed_columns(frame: pd.DataFrame) -> None:
    forbidden = FORBIDDEN_COLUMNS.intersection(frame.columns)
    if forbidden:
        raise ValueError(
            "Forbidden columns were passed into preprocessing: "
            + ", ".join(sorted(forbidden))
        )
    missing = [c for c in PRIMARY_PREDICTORS if c not in frame.columns]
    if missing:
        raise ValueError("Missing required predictors: " + ", ".join(missing))


def _prepare_frame(frame: pd.DataFrame) -> pd.DataFrame:
    _assert_allowed_columns(frame)
    out = frame.loc[:, PRIMARY_PREDICTORS].copy()
    for column in NUMERIC_FEATURES:
        out[column] = pd.to_numeric(out[column], errors="coerce")
    for column in CATEGORICAL_FEATURES:
        out[column] = out[column].astype("object")
    return out


class LendingClubPreprocessor:
    """Sklearn-compatible preprocessor with an explicit train-only fit."""

    def __init__(self) -> None:
        self.pipeline_: Pipeline | None = None
        self.n_features_out_: int | None = None
        self.feature_names_out_: list[str] | None = None
        self.fitted_on_n_rows_: int | None = None

    def _build_pipeline(self) -> Pipeline:
        numeric = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
            ]
        )
        categorical = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(strategy="constant", fill_value=MISSING_TOKEN),
                ),
                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        sparse_output=True,
                        dtype=np.float64,
                    ),
                ),
            ]
        )
        transformer = ColumnTransformer(
            transformers=[
                ("numeric", numeric, NUMERIC_FEATURES),
                ("categorical", categorical, CATEGORICAL_FEATURES),
            ],
            remainder="drop",
            sparse_threshold=0.3,
            verbose_feature_names_out=True,
        )
        return Pipeline(steps=[("columns", transformer)])

    def fit(self, train: pd.DataFrame, y: None = None) -> "LendingClubPreprocessor":
        if y is not None:
            raise ValueError("Target must not be passed into preprocessing.fit.")
        prepared = _prepare_frame(train)
        self.pipeline_ = self._build_pipeline()
        self.pipeline_.fit(prepared)
        names = self.pipeline_.named_steps["columns"].get_feature_names_out()
        self.feature_names_out_ = [str(n) for n in names]
        self.n_features_out_ = len(self.feature_names_out_)
        self.fitted_on_n_rows_ = int(len(prepared))
        return self

    def transform(self, frame: pd.DataFrame):
        if self.pipeline_ is None:
            raise RuntimeError("Preprocessor has not been fitted.")
        prepared = _prepare_frame(frame)
        return self.pipeline_.transform(prepared)

    def transform_imputed_frame(self, frame: pd.DataFrame) -> pd.DataFrame:
        """Apply TRAIN-fitted imputers only; keep the original 9 columns.

        Used by EBM so additive functions attach to native fields rather than
        one-hot expansions. Imputer parameters still come from the Stage 4A
        pipeline fit on the allowed training data.
        """
        if self.pipeline_ is None:
            raise RuntimeError("Preprocessor has not been fitted.")
        prepared = _prepare_frame(frame)
        columns = self.pipeline_.named_steps["columns"]
        numeric_imputer: SimpleImputer = columns.named_transformers_["numeric"].named_steps["imputer"]
        categorical_imputer: SimpleImputer = columns.named_transformers_["categorical"].named_steps["imputer"]
        numeric = numeric_imputer.transform(prepared[NUMERIC_FEATURES])
        categorical = categorical_imputer.transform(prepared[CATEGORICAL_FEATURES])
        out = pd.DataFrame(numeric, columns=NUMERIC_FEATURES)
        for idx, name in enumerate(CATEGORICAL_FEATURES):
            out[name] = categorical[:, idx]
        return out.loc[:, PRIMARY_PREDICTORS]

    def fit_transform(self, train: pd.DataFrame, y: None = None):
        return self.fit(train, y=y).transform(train)

    def get_feature_names_out(self) -> np.ndarray:
        if self.feature_names_out_ is None:
            raise RuntimeError("Preprocessor has not been fitted.")
        return np.asarray(self.feature_names_out_)

    def fitted_state(self) -> dict[str, Any]:
        if self.pipeline_ is None:
            raise RuntimeError("Preprocessor has not been fitted.")
        columns = self.pipeline_.named_steps["columns"]
        numeric_imputer: SimpleImputer = columns.named_transformers_["numeric"].named_steps["imputer"]
        categorical_imputer: SimpleImputer = columns.named_transformers_["categorical"].named_steps["imputer"]
        encoder: OneHotEncoder = columns.named_transformers_["categorical"].named_steps["encoder"]
        return {
            "numeric_statistics": [None if pd.isna(v) else float(v) for v in numeric_imputer.statistics_],
            "numeric_features": list(NUMERIC_FEATURES),
            "categorical_fill_value": categorical_imputer.fill_value,
            "categorical_features": list(CATEGORICAL_FEATURES),
            "categories": [[str(v) for v in cat] for cat in encoder.categories_],
            "n_features_out": self.n_features_out_,
            "feature_names_out": list(self.feature_names_out_ or []),
            "fitted_on_n_rows": self.fitted_on_n_rows_,
        }


def load_split_predictor_frames() -> dict[str, pd.DataFrame]:
    raw = load_lendingclub(RAW_DIR / EXPECTED_LC_FILENAME)
    assignments = pd.read_csv(ASSIGNMENTS_PATH, usecols=["id", "split"])
    merged = raw.merge(assignments, on="id", how="inner")
    if len(merged) != len(raw):
        raise RuntimeError("Split assignments do not align 1:1 with raw LendingClub rows.")
    frames = {}
    for split in ("train", "validation", "test"):
        part = merged.loc[merged["split"] == split, PRIMARY_PREDICTORS].copy()
        frames[split] = part.reset_index(drop=True)
    return frames


def _library_versions() -> dict[str, str]:
    import sklearn

    return {
        "python": sys.version.replace("\n", " "),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "sklearn": sklearn.__version__,
        "joblib": joblib.__version__,
    }


def _special_value_policy(train: pd.DataFrame) -> dict[str, Any]:
    dti = pd.to_numeric(train["dti_n"], errors="coerce")
    n_999 = int((dti == DTI_SENTINEL).sum())
    return {
        "original_value": DTI_SENTINEL,
        "interpretation": "UNCERTAIN",
        "evidence": (
            "Stage 2 noted dti_n==999 as a possible sentinel in some LendingClub extracts. "
            "Zenodo documentation for this granting-model release does not define 999 as missing. "
            "Research-owner freeze: preserve original dti_n values; do not alter or recalculate."
        ),
        "transformation": "NONE",
        "justification": (
            "Interpretation remains uncertain, so the value is preserved. It is not deleted, "
            "not recoded to NA, and not clipped. TRAIN count of exact 999 is recorded only as "
            "an audit statistic."
        ),
        "train_count_exact_999": n_999,
    }


def _feature_summary_rows(state: dict[str, Any], train: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    for column in NUMERIC_FEATURES:
        rows.append(
            {
                "feature": column,
                "original_dtype": str(train[column].dtype),
                "processed_representation": "numeric_passthrough_after_median_impute",
                "missing_policy": "SimpleImputer median fitted on TRAIN; no missing values in TRAIN",
                "encoding_policy": "NONE",
                "fit_source": "TRAIN_ONLY",
            }
        )
    cat_counts = {
        name: len(cats)
        for name, cats in zip(CATEGORICAL_FEATURES, state["categories"])
    }
    for column in CATEGORICAL_FEATURES:
        rows.append(
            {
                "feature": column,
                "original_dtype": str(train[column].dtype),
                "processed_representation": f"one_hot_{cat_counts[column]}_train_categories",
                "missing_policy": (
                    f"SimpleImputer constant token {MISSING_TOKEN!r}; token is not a TRAIN "
                    "category, so transform-time NA follows unseen-category handling"
                ),
                "encoding_policy": "OneHotEncoder(handle_unknown='ignore') fitted on TRAIN",
                "fit_source": "TRAIN_ONLY",
            }
        )
    return rows


def write_stage4a_report(payload: dict[str, Any]) -> None:
    policy = preprocessing_policy_rows()
    ops = "\n".join(
        f"- `{r['column']}` ({r['dtype']}): `{r['preprocessing_operation']}` fit_on={r['fit_on']}"
        for r in policy
    )
    md = f"""# Stage 4A Preprocessing Report

## 1. Objective

Fit a leakage-safe preprocessor for the frozen LendingClub primary predictor set. Parameters are learned from TRAIN only. Validation and test are transformed with those frozen parameters. No model was trained. Raw files were not modified. UCI was not merged.

## 2. Frozen Feature Set

Primary predictors: {", ".join(f"`{c}`" for c in PRIMARY_PREDICTORS)}.

Explicitly excluded and rejected by the preprocessor if present: {", ".join(f"`{c}`" for c in sorted(FORBIDDEN_COLUMNS))}.

Frozen split used to select TRAIN rows: 2007-06 through 2016-03. Boundaries were not changed.

## 3. Preprocessing Policy

Policy file: `docs/lendingclub_preprocessing_policy.csv`.

{ops}

Operations were chosen from the TRAIN schema, not from common-practice defaults. No variable was standardized, winsorized, or clipped.

## 4. Missing-Value Handling

TRAIN missing counts for the nine predictors: {payload["train_missing"]}.

Because TRAIN has no missing values on these predictors, no missingness indicator was added. A TRAIN-only median imputer is still fitted for numeric columns, and a constant token imputer is applied to categoricals, so a later missing cell can be transformed without refitting. Categorical missing at transform uses token `{MISSING_TOKEN}`. That token is not a TRAIN category, so it is treated as unseen (all-zero one-hot). Validation/test missingness was not inspected to set this policy.

## 5. Numeric Feature Handling

Numeric predictors from the actual TRAIN schema: `revenue`, `dti_n`, `loan_amnt`, `fico_n`.

`emp_length`, `home_ownership_n`, and `zip_code` are strings in TRAIN and are treated as categorical, not numeric.

Numeric values are passed through after median imputation. No scaler, log, clip, or winsorize step is included.

Fitted TRAIN medians: {payload["numeric_medians"]}.

## 6. Categorical Feature Handling

Categorical predictors: `emp_length` ({payload["category_counts"]["emp_length"]} TRAIN categories, including `NI`), `purpose` ({payload["category_counts"]["purpose"]}), `home_ownership_n` ({payload["category_counts"]["home_ownership_n"]}), `addr_state` ({payload["category_counts"]["addr_state"]}), `zip_code` ({payload["category_counts"]["zip_code"]} masked prefixes).

Encoding: `sklearn.preprocessing.OneHotEncoder(handle_unknown='ignore')` fitted on TRAIN only. Categories not observed in TRAIN are not enumerated from validation/test. At transform they yield an all-zero dummy row for that feature group.

## 7. Special-Value Handling

`dti_n == 999`: {payload["special_values"]}.

## 8. Train-Only Fitting

The preprocessor was fitted on {payload["fitted_on_n_rows"]} TRAIN rows. Validation and test were transformed afterward and were not concatenated into `fit`. Fitted state was re-read after those transforms and matched the post-fit snapshot.

## 9. Leakage Tests

Module: `tests/test_preprocessing_leakage.py`.

Script-level state comparison after transforming validation and test: {payload["state_unchanged_after_val_test"]}.

Pytest results are recorded when that suite is executed. This report does not claim leakage safety beyond the checks that were actually run.

## 10. Reproducibility

See `audit/preprocessing_run.json`. `git_commit` is recorded as null when no git repository exists.

## 11. Artifacts

- `docs/lendingclub_preprocessing_policy.csv`
- `src/preprocessing/lendingclub_preprocessor.py`
- `results/artifacts/lendingclub_preprocessor.joblib`
- `results/metrics/preprocessing_summary.json`
- `results/tables/preprocessing_feature_summary.csv`
- `audit/preprocessing_run.json`
- `docs/STAGE_4A_PREPROCESSING_REPORT.md`
- `tests/test_preprocessing_leakage.py`

Applicant-level transformed matrices were not written to `results/`.

## 12. Open Issues

- `zip_code` one-hot uses {payload["category_counts"]["zip_code"]} TRAIN levels (high cardinality). No frequency grouping was invented in this stage.
- `dti_n == 999` remains unlabeled.
- No scaling is applied; Stage 4B models that require scaled inputs must either tolerate raw numeric scales or obtain a new, separately justified, TRAIN-only scaler through methodology review.
- Transformed matrices are produced in memory / by re-running `transform`; they are not stored as public result tables.

## 13. Stage-4B Preconditions

Stage 4B may begin only if these fitted parameters remain frozen, preprocessing stays TRAIN-only, excluded columns stay excluded, and no test metric is used to revise encoding. Stage 4B is not started by this script.
"""
    write_text(DOCS_DIR / "STAGE_4A_PREPROCESSING_REPORT.md", md)


def main() -> int:
    write_preprocessing_policy()
    lc_hash = sha256_file(RAW_DIR / EXPECTED_LC_FILENAME)
    if lc_hash != RECORDED_LC_SHA256:
        print("HARD STOP: LendingClub raw hash changed.", file=sys.stderr)
        return 2

    frames = load_split_predictor_frames()
    train = frames["train"]
    validation = frames["validation"]
    test = frames["test"]
    train_missing = {c: int(train[c].isna().sum()) for c in PRIMARY_PREDICTORS}

    preprocessor = LendingClubPreprocessor()
    preprocessor.fit(train)
    state_after_fit = preprocessor.fitted_state()
    x_train = preprocessor.transform(train)
    state_after_train_transform = preprocessor.fitted_state()
    x_val = preprocessor.transform(validation)
    state_after_val = preprocessor.fitted_state()
    x_test = preprocessor.transform(test)
    state_after_test = preprocessor.fitted_state()

    if state_after_fit != state_after_train_transform:
        print("HARD STOP: transforming TRAIN changed fitted state.", file=sys.stderr)
        return 2
    if state_after_fit != state_after_val or state_after_fit != state_after_test:
        print("HARD STOP: transforming validation/test changed fitted state.", file=sys.stderr)
        return 2

    names = preprocessor.get_feature_names_out()
    if x_train.shape[1] != x_val.shape[1] or x_train.shape[1] != x_test.shape[1]:
        print("HARD STOP: transformed splits have different feature counts.", file=sys.stderr)
        return 2
    if x_train.shape[0] != len(train) or x_val.shape[0] != len(validation) or x_test.shape[0] != len(test):
        print("HARD STOP: transformed row counts do not match split sizes.", file=sys.stderr)
        return 2

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)

    category_counts = {
        name: len(cats)
        for name, cats in zip(CATEGORICAL_FEATURES, state_after_fit["categories"])
    }
    numeric_medians = {
        name: value
        for name, value in zip(NUMERIC_FEATURES, state_after_fit["numeric_statistics"])
    }
    special = _special_value_policy(train)
    summary_rows = _feature_summary_rows(state_after_fit, train)
    RESULTS_TABLES.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(summary_rows).to_csv(
        RESULTS_TABLES / "preprocessing_feature_summary.csv",
        index=False,
        encoding="utf-8",
    )

    summary = {
        "fitted_on": "LendingClub TRAIN only",
        "fitted_on_n_rows": preprocessor.fitted_on_n_rows_,
        "n_features_out": preprocessor.n_features_out_,
        "train_rows_transformed": int(x_train.shape[0]),
        "validation_rows_transformed": int(x_val.shape[0]),
        "test_rows_transformed": int(x_test.shape[0]),
        "numeric_features": NUMERIC_FEATURES,
        "categorical_features": CATEGORICAL_FEATURES,
        "category_counts_from_train": category_counts,
        "numeric_medians_from_train": numeric_medians,
        "train_missing_counts": train_missing,
        "unseen_category_handling": "OneHotEncoder handle_unknown='ignore' (all-zero dummy group)",
        "scaling": "NONE",
        "clipping": "NONE",
        "winsorizing": "NONE",
        "special_values": special,
        "forbidden_columns_rejected": sorted(FORBIDDEN_COLUMNS),
        "modeling_started": False,
        "uci_merged": False,
        "raw_modified": False,
        "transformed_matrices_saved_to_results": False,
        "preprocessor_path": str(PREPROCESSOR_PATH.relative_to(REPO_ROOT)),
        "leakage_tests": "pending_pytest",
    }
    write_json(RESULTS_METRICS / "preprocessing_summary.json", summary)

    run_record = {
        "dataset_hash": lc_hash,
        "split_manifest_hash": sha256_text_file(SPLIT_MANIFEST_PATH),
        "feature_policy_hash": sha256_text_file(FEATURE_POLICY_PATH),
        "preprocessing_policy_hash": sha256_text_file(PREPROCESS_POLICY_PATH),
        "python_version": sys.version.replace("\n", " "),
        "library_versions": _library_versions(),
        "git_commit": git_commit(REPO_ROOT),
        "run_timestamp": utc_now_iso(),
        "script_version": SCRIPT_VERSION,
        "n_features_out": preprocessor.n_features_out_,
    }
    write_json(AUDIT_DIR / "preprocessing_run.json", run_record)

    write_stage4a_report(
        {
            "train_missing": train_missing,
            "numeric_medians": numeric_medians,
            "category_counts": category_counts,
            "special_values": special,
            "fitted_on_n_rows": preprocessor.fitted_on_n_rows_,
            "state_unchanged_after_val_test": True,
        }
    )
    print(
        json.dumps(
            {
                "status": "COMPLETE",
                "n_features_out": preprocessor.n_features_out_,
                "fitted_on_n_rows": preprocessor.fitted_on_n_rows_,
                "category_counts_from_train": category_counts,
                "numeric_medians_from_train": numeric_medians,
            },
            indent=2,
        )
    )
    _ = names
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
