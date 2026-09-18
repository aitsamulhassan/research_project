"""Stage 3: frozen feature policy and train/validation/test split membership.

Loads immutable raw files. Does not train models, impute, scale, encode,
calibrate, or select features. Does not modify data/raw/.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from data.audit_datasets import (
    EXPECTED_LC_FILENAME,
    EXPECTED_UCI_ZIP_FILENAME,
    RAW_DIR,
    REPO_ROOT,
    git_commit,
    load_lendingclub,
    load_uci_dataframe,
    parse_issue_d,
    sha256_file,
)

SCRIPT_VERSION = "stage3-0.1.0"
ZENODO_EVIDENCE = (
    "Zenodo record 10.5281/zenodo.11295916 version 0.1 dataset description; "
    "Stage 2 leakage audit; research-owner Stage 3 freeze."
)
UCI_EVIDENCE = (
    "UCI Machine Learning Repository dataset 350 Additional Variable Information "
    "and observed spreadsheet columns; Stage 2 UCI audit; research-owner Stage 3 freeze."
)
LC_TRAIN_CUM_MAX = 0.70
LC_TRAIN_PLUS_VAL_CUM_MAX = 0.85
UCI_SEED = 42
UCI_TRAIN_FRAC = 0.70
UCI_VAL_FRAC = 0.15
UCI_TARGET = "default payment next month"
RECORDED_LC_SHA256 = "207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc"
RECORDED_UCI_SHA256 = "56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602"

DOCS_DIR = REPO_ROOT / "docs"
RESULTS_TABLES = REPO_ROOT / "results" / "tables"
RESULTS_METRICS = REPO_ROOT / "results" / "metrics"
AUDIT_DIR = REPO_ROOT / "audit"

LC_POLICY_FIELDS = [
    "column",
    "role",
    "status",
    "reason",
    "source_evidence",
    "timing_status",
    "model_use",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return str(value)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_safe(payload), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: "" if row.get(k) is None else row.get(k) for k in fieldnames})


def membership_hash(ids: list[Any], order_keys: list[Any]) -> str:
    if len(ids) != len(order_keys):
        raise ValueError("ids and order_keys must be the same length.")
    paired = sorted(zip((str(k) for k in order_keys), (str(i) for i in ids)))
    payload = "\n".join(f"{key}\t{item}" for key, item in paired) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def lendingclub_feature_policy_rows() -> list[dict[str, str]]:
    return [
        {
            "column": "id",
            "role": "IDENTIFIER",
            "status": "EXCLUDE",
            "reason": "Unique loan identifier. Research-owner freeze: IDENTIFIER + EXCLUDE from the model.",
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "NOT_APPLICABLE",
            "model_use": "EXCLUDE_FROM_MODEL",
        },
        {
            "column": "issue_d",
            "role": "TIME_INDEX",
            "status": "EXCLUDE",
            "reason": (
                "Month/year the loan was approved. Research-owner freeze: temporal ordering "
                "variable only; MUST NOT be used as a predictive model feature "
                "(TIME_INDEX + EXCLUDE_FROM_MODEL)."
            ),
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "AT_APPROVAL_NOT_PRE_DECISION",
            "model_use": "EXCLUDE_FROM_MODEL",
        },
        {
            "column": "revenue",
            "role": "PREDICTOR",
            "status": "RETAIN",
            "reason": "Borrower self-declared annual income during registration. Stage 2: SAFE_APPLICATION_TIME.",
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "PRIMARY_MODEL_PREDICTOR",
        },
        {
            "column": "dti_n",
            "role": "PREDICTOR",
            "status": "RETAIN",
            "reason": (
                "Application-time indebtedness ratio. Research-owner freeze: retain as an "
                "application-time feature; preserve original values; do not alter or recalculate."
            ),
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "PRIMARY_MODEL_PREDICTOR",
        },
        {
            "column": "loan_amnt",
            "role": "PREDICTOR",
            "status": "RETAIN",
            "reason": "Amount of credit requested by the borrower. Stage 2: SAFE_APPLICATION_TIME.",
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "PRIMARY_MODEL_PREDICTOR",
        },
        {
            "column": "fico_n",
            "role": "PREDICTOR",
            "status": "RETAIN",
            "reason": "FICO reported at application (average of fico_range_low/high). Stage 2: SAFE_APPLICATION_TIME.",
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "PRIMARY_MODEL_PREDICTOR",
        },
        {
            "column": "experience_c",
            "role": "EXCLUDED",
            "status": "EXCLUDE",
            "reason": (
                "Research-owner freeze: excluded from model features. Construction uses credit "
                "dates from previous/current obligations; timing cannot be established as safely "
                "available at the precise granting decision point."
            ),
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "TIMING_UNVERIFIED",
            "model_use": "EXCLUDE_FROM_MODEL",
        },
        {
            "column": "emp_length",
            "role": "PREDICTOR",
            "status": "RETAIN",
            "reason": "Employment length, including a no-information category. Stage 2: SAFE_APPLICATION_TIME.",
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "PRIMARY_MODEL_PREDICTOR",
        },
        {
            "column": "purpose",
            "role": "PREDICTOR",
            "status": "RETAIN",
            "reason": (
                "Coarse financing-purpose category for the loan request. Stage 2: "
                "SAFE_APPLICATION_TIME. Structured predictor for the primary credit model; "
                "also the documented purpose field for later decision-support work."
            ),
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "PRIMARY_MODEL_PREDICTOR",
        },
        {
            "column": "home_ownership_n",
            "role": "PREDICTOR",
            "status": "RETAIN",
            "reason": "Homeownership status provided during registration. Stage 2: SAFE_APPLICATION_TIME.",
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "PRIMARY_MODEL_PREDICTOR",
        },
        {
            "column": "addr_state",
            "role": "PREDICTOR",
            "status": "RETAIN",
            "reason": "US residence state provided at registration. Application-time; also a quasi-identifier.",
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "PRIMARY_MODEL_PREDICTOR",
        },
        {
            "column": "zip_code",
            "role": "PREDICTOR",
            "status": "RETAIN",
            "reason": "Residence zip code (masked prefix in this release). Application-time; also a quasi-identifier.",
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "PRIMARY_MODEL_PREDICTOR",
        },
        {
            "column": "Default",
            "role": "TARGET",
            "status": "RETAIN",
            "reason": (
                "Research-owner freeze: binary target. Default=1 is Charged Off; Default=0 is Fully Paid."
            ),
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "POST_OUTCOME",
            "model_use": "TARGET_ONLY",
        },
        {
            "column": "title",
            "role": "TEXT",
            "status": "EXCLUDE",
            "reason": (
                "Borrower-provided free-text title. Excluded from the primary credit model. "
                "Retained as a future experimental branch for explainability/Shariah investigation. "
                "Not silently discarded."
            ),
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "FUTURE_EXPERIMENTAL_BRANCH",
        },
        {
            "column": "desc",
            "role": "TEXT",
            "status": "EXCLUDE",
            "reason": (
                "Borrower-provided free-text description. Excluded from the primary credit model. "
                "Retained as a future experimental branch despite high missingness. Not silently discarded."
            ),
            "source_evidence": ZENODO_EVIDENCE,
            "timing_status": "APPLICATION_TIME",
            "model_use": "FUTURE_EXPERIMENTAL_BRANCH",
        },
    ]


def uci_feature_policy_rows() -> list[dict[str, str]]:
    predictors = [
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
    rows = [
        {
            "column": "ID",
            "role": "IDENTIFIER",
            "status": "EXCLUDE",
            "reason": "Row identifier. Excluded from the UCI model feature list.",
            "source_evidence": UCI_EVIDENCE,
            "timing_status": "NOT_APPLICABLE",
            "model_use": "EXCLUDE_FROM_MODEL",
        },
        {
            "column": UCI_TARGET,
            "role": "TARGET",
            "status": "RETAIN",
            "reason": "Binary default payment next month (Yes=1, No=0). UCI-specific target; not equivalent to LendingClub Default.",
            "source_evidence": UCI_EVIDENCE,
            "timing_status": "POST_WINDOW_OUTCOME",
            "model_use": "TARGET_ONLY",
        },
    ]
    for column in predictors:
        rows.append(
            {
                "column": column,
                "role": "PREDICTOR",
                "status": "RETAIN",
                "reason": (
                    "UCI-specific candidate predictor. Not claimed to be semantically equivalent "
                    "to any LendingClub feature. Undocumented codes are preserved, not recoded."
                ),
                "source_evidence": UCI_EVIDENCE,
                "timing_status": "UCI_STUDY_WINDOW_NOT_LC_APPLICATION_TIME",
                "model_use": "UCI_CANDIDATE_PREDICTOR",
            }
        )
    return rows


def policy_model_columns(rows: list[dict[str, str]]) -> list[str]:
    return [r["column"] for r in rows if r["model_use"] == "PRIMARY_MODEL_PREDICTOR"]


def policy_uci_model_columns(rows: list[dict[str, str]]) -> list[str]:
    return [r["column"] for r in rows if r["model_use"] == "UCI_CANDIDATE_PREDICTOR"]


def write_text_feature_policy() -> None:
    text = """# Text Feature Policy

This policy covers LendingClub `title` and `desc` only. No text model is built in Stage 3.

## title

- Role: TEXT
- Primary credit model: excluded
- Retention: kept in the immutable raw file and in the frozen feature policy as a future experimental branch
- Timing: application-time borrower-provided request title (Zenodo; Stage 2 leakage audit)

## desc

- Role: TEXT
- Primary credit model: excluded
- Retention: kept as a future experimental branch even though Stage 2 found high missingness (91.162671%)
- Timing: application-time borrower-provided request description (Zenodo; Stage 2 leakage audit)

## Why text is not silently discarded

`purpose` is a coarse category. `title` and `desc` are the only finer borrower-provided purpose language in this release. They are application-time fields and are therefore in scope for later explainability work and for a later Shariah-oriented decision-support investigation. Silently dropping them would destroy that option and would violate the research constitution rule against silently removing inconvenient material. They are excluded from the Stage 3/4 primary credit-risk predictor set because this stage does not encode text and the owner did not approve a text model.

`purpose` remains a structured primary-model predictor. That is not a text model.

## Prohibited in this stage

- No embeddings, bag-of-words, TF-IDF, or LLM features
- No Shariah rule engine
- No publication of raw free-text values in reports
"""
    write_text(DOCS_DIR / "text_feature_policy.md", text)


def monthly_target_distribution(df: pd.DataFrame, parsed: pd.Series) -> pd.DataFrame:
    if parsed.isna().any():
        raise RuntimeError("HARD STOP: issue_d could not be parsed reliably for every row.")
    month = parsed.dt.to_period("M").astype(str)
    grouped = (
        pd.DataFrame({"issue_month": month, "Default": df["Default"].to_numpy()})
        .groupby("issue_month", sort=True)
        .agg(n_rows=("Default", "size"), n_default=("Default", "sum"))
        .reset_index()
    )
    grouped["n_default"] = grouped["n_default"].astype(int)
    grouped["n_rows"] = grouped["n_rows"].astype(int)
    grouped["default_rate"] = grouped["n_default"] / grouped["n_rows"]
    grouped["cumulative_rows"] = grouped["n_rows"].cumsum()
    grouped["cumulative_fraction"] = grouped["cumulative_rows"] / int(grouped["n_rows"].sum())
    return grouped


def choose_temporal_cutoffs(monthly: pd.DataFrame) -> dict[str, Any]:
    """Derive month boundaries from chronological observation mass.

    Train = earliest months whose cumulative share is at most LC_TRAIN_CUM_MAX.
    Validation = following months until cumulative share is at most LC_TRAIN_PLUS_VAL_CUM_MAX.
    Test = remaining latest months. No month is split across sets.
    Proportions are sample-size rules, not model-performance rules.
    """
    if monthly.empty or monthly["issue_month"].isna().any():
        raise RuntimeError("HARD STOP: temporal ordering is impossible; monthly index is empty or null.")
    total = int(monthly["n_rows"].sum())
    train_mask = monthly["cumulative_fraction"] <= LC_TRAIN_CUM_MAX
    if not train_mask.any():
        raise RuntimeError("HARD STOP: no month has cumulative fraction <= train mass cap.")
    train_end = str(monthly.loc[train_mask, "issue_month"].iloc[-1])
    val_mask = (monthly["issue_month"] > train_end) & (
        monthly["cumulative_fraction"] <= LC_TRAIN_PLUS_VAL_CUM_MAX
    )
    if not val_mask.any():
        raise RuntimeError("HARD STOP: validation window would be empty.")
    validation_end = str(monthly.loc[val_mask, "issue_month"].iloc[-1])
    test_mask = monthly["issue_month"] > validation_end
    if not test_mask.any():
        raise RuntimeError("HARD STOP: test window would be empty.")
    train_start = str(monthly["issue_month"].iloc[0])
    validation_start = str(monthly.loc[monthly["issue_month"] > train_end, "issue_month"].iloc[0])
    test_start = str(monthly.loc[test_mask, "issue_month"].iloc[0])
    test_end = str(monthly["issue_month"].iloc[-1])
    train_rows = int(monthly.loc[monthly["issue_month"] <= train_end, "n_rows"].sum())
    val_rows = int(
        monthly.loc[
            (monthly["issue_month"] >= validation_start) & (monthly["issue_month"] <= validation_end),
            "n_rows",
        ].sum()
    )
    test_rows = int(monthly.loc[monthly["issue_month"] >= test_start, "n_rows"].sum())
    for name, n in (("train", train_rows), ("validation", val_rows), ("test", test_rows)):
        if n < 1000:
            raise RuntimeError(f"HARD STOP: {name} split is unusably small ({n} rows).")
    if train_rows + val_rows + test_rows != total:
        raise RuntimeError("HARD STOP: split row counts do not cover every source row.")
    return {
        "rule": (
            "Chronological issue_d month order. Train = earliest months with cumulative "
            f"observation share <= {LC_TRAIN_CUM_MAX:.2f}. Validation = subsequent months "
            f"until cumulative share <= {LC_TRAIN_PLUS_VAL_CUM_MAX:.2f}. Test = remaining "
            "latest months. Cutoffs snap to observed months; a month is never split. "
            "Cutoffs were not chosen by inspecting model performance."
        ),
        "train_start": train_start,
        "train_end": train_end,
        "validation_start": validation_start,
        "validation_end": validation_end,
        "test_start": test_start,
        "test_end": test_end,
        "train_rows": train_rows,
        "validation_rows": val_rows,
        "test_rows": test_rows,
    }


def assign_temporal_split(month: str, cutoffs: dict[str, Any]) -> str:
    if month <= cutoffs["train_end"]:
        return "train"
    if month <= cutoffs["validation_end"]:
        return "validation"
    return "test"


def stratified_uci_assignments(ids: pd.Series, y: pd.Series, seed: int = UCI_SEED) -> pd.DataFrame:
    if ids.duplicated().any():
        raise RuntimeError("HARD STOP: UCI IDs are not unique.")
    rng = np.random.RandomState(seed)
    assigned = np.empty(len(ids), dtype=object)
    assigned[:] = ""
    labels = sorted(pd.unique(y.dropna()))
    for label in labels:
        class_pos = np.flatnonzero(y.to_numpy() == label)
        class_pos_sorted = class_pos[np.argsort(ids.iloc[class_pos].astype(str).to_numpy())]
        shuffled = rng.permutation(class_pos_sorted)
        n = len(shuffled)
        n_train = int(n * UCI_TRAIN_FRAC)
        n_val = int(n * UCI_VAL_FRAC)
        assigned[shuffled[:n_train]] = "train"
        assigned[shuffled[n_train : n_train + n_val]] = "validation"
        assigned[shuffled[n_train + n_val :]] = "test"
    if (assigned == "").any():
        raise RuntimeError("HARD STOP: some UCI rows were not assigned to a split.")
    return pd.DataFrame({"ID": ids.to_numpy(), "split": assigned})


def undocumented_uci_codes(df: pd.DataFrame) -> dict[str, Any]:
    documented_edu = {1, 2, 3, 4}
    documented_mar = {1, 2, 3}
    documented_pay = set([-1]) | set(range(1, 10))
    payload: dict[str, Any] = {"recode_applied": False, "fields": []}
    edu = pd.to_numeric(df["EDUCATION"], errors="coerce")
    extra_edu = sorted(set(edu.dropna().astype(int)) - documented_edu)
    payload["fields"].append(
        {
            "column": "EDUCATION",
            "documented_values": sorted(documented_edu),
            "undocumented_values_observed": extra_edu,
            "counts": {str(v): int((edu == v).sum()) for v in extra_edu},
        }
    )
    mar = pd.to_numeric(df["MARRIAGE"], errors="coerce")
    extra_mar = sorted(set(mar.dropna().astype(int)) - documented_mar)
    payload["fields"].append(
        {
            "column": "MARRIAGE",
            "documented_values": sorted(documented_mar),
            "undocumented_values_observed": extra_mar,
            "counts": {str(v): int((mar == v).sum()) for v in extra_mar},
        }
    )
    for column in ["PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6"]:
        pay = pd.to_numeric(df[column], errors="coerce")
        extra = sorted(set(pay.dropna().astype(int)) - documented_pay)
        payload["fields"].append(
            {
                "column": column,
                "documented_values": sorted(documented_pay),
                "undocumented_values_observed": extra,
                "counts": {str(v): int((pay == v).sum()) for v in extra},
            }
        )
    return payload


def split_stats(labels: pd.Series, target: pd.Series) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for split in ("train", "validation", "test"):
        mask = labels == split
        n = int(mask.sum())
        n_pos = int(target[mask].eq(1).sum())
        out[split] = {
            "n_rows": n,
            "n_default": n_pos,
            "prevalence": (n_pos / n) if n else None,
        }
    return out


def verify_lc_integrity(
    df: pd.DataFrame,
    assignments: pd.DataFrame,
    cutoffs: dict[str, Any],
    policy_rows: list[dict[str, str]],
    raw_hash: str,
) -> list[str]:
    errors: list[str] = []
    model_cols = policy_model_columns(policy_rows)
    if "issue_d" in model_cols:
        errors.append("issue_d is present in the model feature list.")
    if "experience_c" in model_cols:
        errors.append("experience_c is present in the model feature list.")
    target_rows = [r for r in policy_rows if r["role"] == "TARGET"]
    if len(target_rows) != 1 or target_rows[0]["column"] != "Default":
        errors.append("Default is not the unique TARGET in the feature policy.")
    if not df["Default"].isin([0, 1]).all() or int(df["Default"].isna().sum()) != 0:
        errors.append("Target values changed or are missing.")
    if assignments["id"].duplicated().any():
        errors.append("Duplicate IDs in split assignments.")
    if set(assignments["id"]) != set(df["id"]):
        errors.append("Split assignments do not cover exactly the source IDs.")
    counts = assignments["split"].value_counts()
    if int(counts.get("train", 0)) + int(counts.get("validation", 0)) + int(counts.get("test", 0)) != len(df):
        errors.append("Not every source row belongs to exactly one split.")
    train_m = assignments.loc[assignments["split"] == "train", "issue_month"]
    val_m = assignments.loc[assignments["split"] == "validation", "issue_month"]
    test_m = assignments.loc[assignments["split"] == "test", "issue_month"]
    if not (train_m.max() < val_m.min() and val_m.max() < test_m.min()):
        errors.append("Chronological ordering is not preserved across splits.")
    if raw_hash != RECORDED_LC_SHA256:
        errors.append("LendingClub raw hash does not match the recorded artifact.")
    joined = assignments.merge(df[["id", "Default"]], on="id", how="left", suffixes=("", "_raw"))
    if int(joined["Default"].isna().sum()) != 0:
        errors.append("Target missing after split join.")
    return errors


def write_stage3_report(payload: dict[str, Any]) -> None:
    lc = payload["lendingclub"]
    uci = payload["uci"]
    policy = payload["lc_policy"]
    predictors = [r["column"] for r in policy if r["model_use"] == "PRIMARY_MODEL_PREDICTOR"]
    excluded = [r for r in policy if r["status"] == "EXCLUDE"]
    md = f"""# Stage 3 Split and Feature Policy Report

## 1. Executive Summary

Stage 3 froze the LendingClub target, predictor set, exclusions, and temporal train/validation/test membership, and created a separate UCI stratified split for method generalization. No model was trained. No preprocessing was fit. Raw files were not modified. LendingClub and UCI were not merged.

- LendingClub primary predictors: {len(predictors)}
- LendingClub split: train {lc["summary"]["train_rows"]}, validation {lc["summary"]["validation_rows"]}, test {lc["summary"]["test_rows"]}
- UCI split seed: {UCI_SEED}

## 2. Frozen Target Definition

LendingClub target is `Default`.

- Positive class `1` = Charged Off
- Negative class `0` = Fully Paid

This is the research-owner freeze. No additional target interpretation was invented. Integrity re-check: Default is in {{0,1}} with zero missing values. Artifact: `results/metrics/final_target_definition.json`.

## 3. LendingClub Feature Policy

Primary-model predictors ({len(predictors)}): {", ".join(f"`{c}`" for c in predictors)}.

Full table: `docs/lendingclub_feature_policy.csv`.

## 4. Excluded Variables

{chr(10).join(f"- `{r['column']}` ({r['role']}): {r['reason']}" for r in excluded)}

`dti_n` is retained with original values.

## 5. Text Feature Policy

`title` and `desc` are excluded from the primary credit model and retained as a future experimental branch. They are not silently discarded. Details: `docs/text_feature_policy.md`. No text model was built.

## 6. Temporal Index Definition

`issue_d` is the approval month/year. It is used only to order observations. It is not a predictor.

## 7. LendingClub Split Method

{lc["cutoffs"]["rule"]}

Train rule: `issue_month <= {lc["cutoffs"]["train_end"]}`.
Validation rule: `{lc["cutoffs"]["validation_start"]} <= issue_month <= {lc["cutoffs"]["validation_end"]}`.
Test rule: `issue_month >= {lc["cutoffs"]["test_start"]}`.

No row appears in more than one split. No resampling, class balancing, or synthetic rows.

## 8. LendingClub Split Boundaries

- Train: {lc["summary"]["train_start"]} to {lc["summary"]["train_end"]}
- Validation: {lc["summary"]["validation_start"]} to {lc["summary"]["validation_end"]}
- Test: {lc["summary"]["test_start"]} to {lc["summary"]["test_end"]}

`train_date < validation_date < test_date` holds at the month grain.

## 9. Split Class Distribution

- Train: {lc["summary"]["train_rows"]} rows, prevalence {lc["summary"]["train_prevalence"]}
- Validation: {lc["summary"]["validation_rows"]} rows, prevalence {lc["summary"]["validation_prevalence"]}
- Test: {lc["summary"]["test_rows"]} rows, prevalence {lc["summary"]["test_prevalence"]}

Monthly table: `results/tables/lendingclub_monthly_target_distribution.csv`.
Split table: `results/tables/lendingclub_split_distribution.csv`.

## 10. UCI Split Method

No reliable UCI timestamp exists. Split is stratified on `{UCI_TARGET}` with proportions {UCI_TRAIN_FRAC:.2f}/{UCI_VAL_FRAC:.2f}/{1.0 - UCI_TRAIN_FRAC - UCI_VAL_FRAC:.2f}, seed {UCI_SEED}. Within each class, IDs are sorted then shuffled with `numpy.random.RandomState({UCI_SEED})` consumed in increasing class-label order. Remainder after floor(0.70n) and floor(0.15n) goes to test. This split is not used for LendingClub.

- Train: {uci["summary"]["train_rows"]}
- Validation: {uci["summary"]["validation_rows"]}
- Test: {uci["summary"]["test_rows"]}

## 11. UCI Feature Policy

`ID` is an excluded identifier. `{UCI_TARGET}` is the UCI target. The remaining 23 columns are UCI-specific candidate predictors. They are not claimed to be semantically equivalent to LendingClub features. Table: `docs/uci_feature_policy.csv`.

## 12. Undocumented UCI Codes

Observed undocumented codes were preserved and not recoded: EDUCATION 0/5/6, MARRIAGE 0, PAY_0 and PAY_2–PAY_6 values 0 and -2. Counts are in `results/metrics/uci_split_summary.json`.

## 13. Leakage Controls

- `issue_d` excluded from predictors
- `experience_c` excluded from predictors
- `id` excluded from predictors
- `Default` used only as target
- `title`/`desc` excluded from the primary model
- Temporal split prevents later-originated loans from training
- UCI not merged into LendingClub
- No preprocessing that could leak test information

Newly discovered leakage in this stage: {payload.get("new_leakage") or "none"}.

## 14. Reproducibility Artifacts

- `docs/lendingclub_feature_policy.csv`
- `docs/uci_feature_policy.csv`
- `docs/text_feature_policy.md`
- `results/metrics/final_target_definition.json`
- `results/metrics/lendingclub_split_summary.json`
- `results/metrics/uci_split_summary.json`
- `audit/lendingclub_split_manifest.json`
- `audit/uci_split_manifest.json`
- `results/tables/lendingclub_split_assignments.csv`
- `results/tables/uci_split_assignments.csv`
- Script: `src/data/create_splits.py` version {SCRIPT_VERSION}

Raw LendingClub SHA-256: `{payload["lc_raw_hash"]}`.
Raw UCI SHA-256: `{payload["uci_raw_hash"]}`.

## 15. Integrity Test Results

Script-level integrity errors: {payload.get("integrity_errors") or "none"}.
Pytest module: `tests/test_splits.py`.

## 16. Open Issues

{chr(10).join(f"- {item}" for item in payload.get("open_issues", [])) or "- None."}

## 17. Stage-4 Preconditions

Stage 4 (preprocessing) may begin only if:

- these splits and policies remain frozen;
- preprocessing is fit on train only;
- `issue_d` and `experience_c` stay out of the predictor matrix;
- undocumented UCI codes are not given invented meanings;
- no test-driven feature selection or thresholding.

Stage 4 is not started by this script.
"""
    write_text(DOCS_DIR / "STAGE_3_SPLIT_AND_FEATURE_REPORT.md", md)


def main() -> int:
    lc_path = RAW_DIR / EXPECTED_LC_FILENAME
    uci_path = RAW_DIR / EXPECTED_UCI_ZIP_FILENAME
    if not lc_path.is_file() or not uci_path.is_file():
        print("HARD STOP: raw files are missing.", file=sys.stderr)
        return 2

    lc_hash = sha256_file(lc_path)
    uci_hash = sha256_file(uci_path)
    if lc_hash != RECORDED_LC_SHA256:
        print("HARD STOP: LendingClub raw hash changed.", file=sys.stderr)
        return 2
    if uci_hash != RECORDED_UCI_SHA256:
        print("HARD STOP: UCI raw hash changed.", file=sys.stderr)
        return 2

    lc_policy = lendingclub_feature_policy_rows()
    uci_policy = uci_feature_policy_rows()
    write_csv_rows(DOCS_DIR / "lendingclub_feature_policy.csv", lc_policy, LC_POLICY_FIELDS)
    write_csv_rows(DOCS_DIR / "uci_feature_policy.csv", uci_policy, LC_POLICY_FIELDS)
    write_text_feature_policy()

    lc = load_lendingclub(lc_path)
    expected_cols = [r["column"] for r in lc_policy]
    if list(lc.columns) != expected_cols:
        print(
            "HARD STOP: feature-policy columns conflict with the raw LendingClub schema: "
            f"raw={list(lc.columns)} policy={expected_cols}",
            file=sys.stderr,
        )
        return 2

    if not lc["Default"].isin([0, 1]).all() or int(lc["Default"].isna().sum()) != 0:
        print("HARD STOP: Default is not a complete binary {{0,1}} column.", file=sys.stderr)
        return 2

    write_json(
        RESULTS_METRICS / "final_target_definition.json",
        {
            "dataset": "LendingClub",
            "target": "Default",
            "positive_class": 1,
            "negative_class": 0,
            "positive_semantics": "Charged Off",
            "negative_semantics": "Fully Paid",
            "n_rows": int(len(lc)),
            "missing_count": int(lc["Default"].isna().sum()),
            "value_counts": {
                "0": int((lc["Default"] == 0).sum()),
                "1": int((lc["Default"] == 1).sum()),
            },
        },
    )

    parsed = parse_issue_d(lc["issue_d"])
    monthly = monthly_target_distribution(lc, parsed)
    write_csv_rows(
        RESULTS_TABLES / "lendingclub_monthly_target_distribution.csv",
        monthly[["issue_month", "n_rows", "n_default", "default_rate"]].to_dict("records"),
        ["issue_month", "n_rows", "n_default", "default_rate"],
    )
    cutoffs = choose_temporal_cutoffs(monthly)
    issue_month = parsed.dt.to_period("M").astype(str)
    split = np.where(
        issue_month <= cutoffs["train_end"],
        "train",
        np.where(issue_month <= cutoffs["validation_end"], "validation", "test"),
    )
    lc_assign = pd.DataFrame(
        {
            "id": lc["id"].to_numpy(),
            "issue_month": issue_month.to_numpy(),
            "split": split,
        }
    )
    if lc_assign.groupby("id")["split"].nunique().gt(1).any():
        print("HARD STOP: duplicate IDs cross splits.", file=sys.stderr)
        return 2

    lc_stats = split_stats(lc_assign["split"], lc["Default"])
    lc_summary = {
        "train_rows": lc_stats["train"]["n_rows"],
        "validation_rows": lc_stats["validation"]["n_rows"],
        "test_rows": lc_stats["test"]["n_rows"],
        "train_start": cutoffs["train_start"],
        "train_end": cutoffs["train_end"],
        "validation_start": cutoffs["validation_start"],
        "validation_end": cutoffs["validation_end"],
        "test_start": cutoffs["test_start"],
        "test_end": cutoffs["test_end"],
        "train_prevalence": lc_stats["train"]["prevalence"],
        "validation_prevalence": lc_stats["validation"]["prevalence"],
        "test_prevalence": lc_stats["test"]["prevalence"],
        "cutoff_rule": cutoffs["rule"],
        "train_plus_validation_cumulative_cap": LC_TRAIN_PLUS_VAL_CUM_MAX,
        "train_cumulative_cap": LC_TRAIN_CUM_MAX,
    }
    write_json(RESULTS_METRICS / "lendingclub_split_summary.json", lc_summary)
    write_csv_rows(
        RESULTS_TABLES / "lendingclub_split_distribution.csv",
        [
            {
                "split": name,
                "n_rows": lc_stats[name]["n_rows"],
                "n_default": lc_stats[name]["n_default"],
                "default_rate": lc_stats[name]["prevalence"],
                "start_month": lc_summary[f"{'train' if name=='train' else 'validation' if name=='validation' else 'test'}_start"],
                "end_month": lc_summary[f"{'train' if name=='train' else 'validation' if name=='validation' else 'test'}_end"],
            }
            for name in ("train", "validation", "test")
        ],
        ["split", "n_rows", "n_default", "default_rate", "start_month", "end_month"],
    )
    RESULTS_TABLES.mkdir(parents=True, exist_ok=True)
    lc_assign.to_csv(RESULTS_TABLES / "lendingclub_split_assignments.csv", index=False)

    lc_hashes = {}
    for split in ("train", "validation", "test"):
        part = lc_assign.loc[lc_assign["split"] == split]
        lc_hashes[split] = membership_hash(part["id"].tolist(), part["issue_month"].tolist())

    excluded_cols = [r["column"] for r in lc_policy if r["status"] == "EXCLUDE"]
    retained_predictors = policy_model_columns(lc_policy)
    lc_manifest = {
        "dataset_hash": lc_hash,
        "target_column": "Default",
        "time_index": "issue_d",
        "excluded_columns": excluded_cols,
        "retained_columns": retained_predictors,
        "train_rule": f"issue_month <= {cutoffs['train_end']}",
        "validation_rule": f"{cutoffs['validation_start']} <= issue_month <= {cutoffs['validation_end']}",
        "test_rule": f"issue_month >= {cutoffs['test_start']}",
        "train_row_count": lc_summary["train_rows"],
        "validation_row_count": lc_summary["validation_rows"],
        "test_row_count": lc_summary["test_rows"],
        "train_hash": lc_hashes["train"],
        "validation_hash": lc_hashes["validation"],
        "test_hash": lc_hashes["test"],
        "creation_timestamp": utc_now_iso(),
        "git_commit": git_commit(REPO_ROOT),
        "script_version": SCRIPT_VERSION,
        "hash_method": "sha256 of sorted issue_month\\tid lines within each split",
    }
    write_json(AUDIT_DIR / "lendingclub_split_manifest.json", lc_manifest)

    integrity_errors = verify_lc_integrity(lc, lc_assign, cutoffs, lc_policy, lc_hash)

    uci_df, _uci_meta = load_uci_dataframe(uci_path)
    if UCI_TARGET not in uci_df.columns:
        print("HARD STOP: UCI target column not found.", file=sys.stderr)
        return 2
    uci_assign = stratified_uci_assignments(uci_df["ID"], uci_df[UCI_TARGET], seed=UCI_SEED)
    uci_stats = split_stats(uci_assign["split"], pd.to_numeric(uci_df[UCI_TARGET], errors="coerce"))
    undocumented = undocumented_uci_codes(uci_df)
    uci_summary = {
        "train_rows": uci_stats["train"]["n_rows"],
        "validation_rows": uci_stats["validation"]["n_rows"],
        "test_rows": uci_stats["test"]["n_rows"],
        "train_prevalence": uci_stats["train"]["prevalence"],
        "validation_prevalence": uci_stats["validation"]["prevalence"],
        "test_prevalence": uci_stats["test"]["prevalence"],
        "seed": UCI_SEED,
        "train_fraction": UCI_TRAIN_FRAC,
        "validation_fraction": UCI_VAL_FRAC,
        "method": "stratified_by_target_no_temporal_index",
        "merged_with_lendingclub": False,
        "undocumented_codes": undocumented,
        "recode_applied": False,
    }
    write_json(RESULTS_METRICS / "uci_split_summary.json", uci_summary)
    write_csv_rows(
        RESULTS_TABLES / "uci_split_distribution.csv",
        [
            {
                "split": name,
                "n_rows": uci_stats[name]["n_rows"],
                "n_default": uci_stats[name]["n_default"],
                "default_rate": uci_stats[name]["prevalence"],
            }
            for name in ("train", "validation", "test")
        ],
        ["split", "n_rows", "n_default", "default_rate"],
    )
    uci_assign.to_csv(RESULTS_TABLES / "uci_split_assignments.csv", index=False)

    uci_hashes = {}
    for split in ("train", "validation", "test"):
        part = uci_assign.loc[uci_assign["split"] == split]
        uci_hashes[split] = membership_hash(part["ID"].tolist(), part["ID"].tolist())

    uci_manifest = {
        "dataset_hash": uci_hash,
        "target_column": UCI_TARGET,
        "time_index": None,
        "excluded_columns": [r["column"] for r in uci_policy if r["status"] == "EXCLUDE"],
        "retained_columns": policy_uci_model_columns(uci_policy),
        "train_rule": f"stratified {UCI_TRAIN_FRAC:.2f} within each target class; seed {UCI_SEED}",
        "validation_rule": f"stratified {UCI_VAL_FRAC:.2f} within each target class; seed {UCI_SEED}",
        "test_rule": "stratified remainder within each target class; seed 42",
        "train_row_count": uci_summary["train_rows"],
        "validation_row_count": uci_summary["validation_rows"],
        "test_row_count": uci_summary["test_rows"],
        "train_hash": uci_hashes["train"],
        "validation_hash": uci_hashes["validation"],
        "test_hash": uci_hashes["test"],
        "creation_timestamp": utc_now_iso(),
        "git_commit": git_commit(REPO_ROOT),
        "script_version": SCRIPT_VERSION,
        "merged_with_lendingclub": False,
        "hash_method": "sha256 of sorted ID\\tID lines within each split",
        "recode_applied": False,
    }
    write_json(AUDIT_DIR / "uci_split_manifest.json", uci_manifest)

    if len(set(uci_assign.columns) & {"id", "issue_d", "Default", "issue_month"}) != 0:
        integrity_errors.append("UCI assignment table contains LendingClub fields.")
    if Path(RESULTS_TABLES / "lendingclub_uci_merged.csv").exists():
        integrity_errors.append("A merged LendingClub-UCI file was written; this is forbidden.")

    open_issues = [
        "Primary credit model still excludes title/desc; a later text/Shariah branch is not specified in Stage 3.",
        "UCI undocumented codes remain unlabeled; no recode protocol is approved.",
        "addr_state and zip_code are retained predictors and quasi-identifiers; privacy handling is not a Stage 3 encoding task.",
    ]
    report_payload = {
        "lendingclub": {"summary": lc_summary, "cutoffs": cutoffs},
        "uci": {"summary": uci_summary},
        "lc_policy": lc_policy,
        "lc_raw_hash": lc_hash,
        "uci_raw_hash": uci_hash,
        "integrity_errors": integrity_errors,
        "open_issues": open_issues,
        "new_leakage": "none identified beyond the frozen Stage 2/owner exclusions",
    }
    write_stage3_report(report_payload)
    write_json(
        RESULTS_METRICS / "stage3_summary.json",
        {
            "stage": "3",
            "status": "COMPLETE" if not integrity_errors else "BLOCKED",
            "modeling_started": False,
            "preprocessing_fit": False,
            "lendingclub_primary_predictor_count": len(retained_predictors),
            "lendingclub_primary_predictors": retained_predictors,
            "integrity_errors": integrity_errors,
        },
    )
    if integrity_errors:
        print("HARD STOP: integrity errors:", file=sys.stderr)
        for item in integrity_errors:
            print(f"- {item}", file=sys.stderr)
        return 2
    print(json.dumps(json_safe({
        "status": "COMPLETE",
        "lc_predictors": retained_predictors,
        "lc_summary": lc_summary,
        "uci_rows": {
            "train": uci_summary["train_rows"],
            "validation": uci_summary["validation_rows"],
            "test": uci_summary["test_rows"],
        },
    }), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
