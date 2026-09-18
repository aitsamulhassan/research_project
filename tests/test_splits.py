"""Stage 3 split and feature-policy integrity tests. No ML behaviour is tested."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data.audit_datasets import (  # noqa: E402
    EXPECTED_LC_FILENAME,
    EXPECTED_UCI_ZIP_FILENAME,
    RAW_DIR,
    sha256_file,
)
from data.create_splits import (  # noqa: E402
    RECORDED_LC_SHA256,
    RECORDED_UCI_SHA256,
    membership_hash,
    policy_model_columns,
    policy_uci_model_columns,
)

LC_RAW = RAW_DIR / EXPECTED_LC_FILENAME
UCI_RAW = RAW_DIR / EXPECTED_UCI_ZIP_FILENAME
LC_POLICY = ROOT / "docs" / "lendingclub_feature_policy.csv"
UCI_POLICY = ROOT / "docs" / "uci_feature_policy.csv"
LC_ASSIGN = ROOT / "results" / "tables" / "lendingclub_split_assignments.csv"
UCI_ASSIGN = ROOT / "results" / "tables" / "uci_split_assignments.csv"
LC_SUMMARY = ROOT / "results" / "metrics" / "lendingclub_split_summary.json"
UCI_SUMMARY = ROOT / "results" / "metrics" / "uci_split_summary.json"
LC_MANIFEST = ROOT / "audit" / "lendingclub_split_manifest.json"
UCI_MANIFEST = ROOT / "audit" / "uci_split_manifest.json"
TARGET_DEF = ROOT / "results" / "metrics" / "final_target_definition.json"
RAW_MANIFEST = ROOT / "docs" / "raw_data_manifest.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_splits_are_disjoint() -> None:
    lc = pd.read_csv(LC_ASSIGN)
    uci = pd.read_csv(UCI_ASSIGN)
    for frame, key in ((lc, "id"), (uci, "ID")):
        by_split = {name: set(part[key]) for name, part in frame.groupby("split")}
        assert by_split["train"].isdisjoint(by_split["validation"])
        assert by_split["train"].isdisjoint(by_split["test"])
        assert by_split["validation"].isdisjoint(by_split["test"])


def test_every_source_row_belongs_to_exactly_one_split() -> None:
    lc_assign = pd.read_csv(LC_ASSIGN)
    header = pd.read_csv(LC_RAW, usecols=["id"])
    assert not lc_assign["id"].duplicated().any()
    assert not lc_assign.groupby("id")["split"].nunique().gt(1).any()
    assert set(lc_assign["id"]) == set(header["id"])
    assert set(lc_assign["split"]) == {"train", "validation", "test"}
    assert len(lc_assign) == len(header)

    uci_assign = pd.read_csv(UCI_ASSIGN)
    uci_summary = _load_json(UCI_SUMMARY)
    assert not uci_assign["ID"].duplicated().any()
    assert len(uci_assign) == (
        uci_summary["train_rows"] + uci_summary["validation_rows"] + uci_summary["test_rows"]
    )
    assert set(uci_assign["split"]) == {"train", "validation", "test"}


def test_chronological_ordering_is_preserved() -> None:
    lc = pd.read_csv(LC_ASSIGN)
    train_max = lc.loc[lc["split"] == "train", "issue_month"].max()
    val_min = lc.loc[lc["split"] == "validation", "issue_month"].min()
    val_max = lc.loc[lc["split"] == "validation", "issue_month"].max()
    test_min = lc.loc[lc["split"] == "test", "issue_month"].min()
    assert train_max < val_min < val_max < test_min
    summary = _load_json(LC_SUMMARY)
    assert summary["train_end"] < summary["validation_start"]
    assert summary["validation_end"] < summary["test_start"]
    assert summary["train_start"] < summary["train_end"] or summary["train_start"] == summary["train_end"]


def test_target_values_remain_unchanged() -> None:
    target_def = _load_json(TARGET_DEF)
    assert target_def["target"] == "Default"
    assert target_def["positive_class"] == 1
    assert target_def["negative_class"] == 0
    assert target_def["positive_semantics"] == "Charged Off"
    assert target_def["negative_semantics"] == "Fully Paid"
    raw = pd.read_csv(LC_RAW, usecols=["id", "Default"])
    assert raw["Default"].isin([0, 1]).all()
    assert int(raw["Default"].isna().sum()) == 0
    assign = pd.read_csv(LC_ASSIGN)
    merged = assign.merge(raw, on="id", how="left")
    assert int(merged["Default"].isna().sum()) == 0
    assert merged["Default"].isin([0, 1]).all()
    assert len(merged) == len(raw)


def test_split_row_counts_match_saved_metadata() -> None:
    lc = pd.read_csv(LC_ASSIGN)
    summary = _load_json(LC_SUMMARY)
    manifest = _load_json(LC_MANIFEST)
    counts = lc["split"].value_counts().to_dict()
    assert counts["train"] == summary["train_rows"] == manifest["train_row_count"]
    assert counts["validation"] == summary["validation_rows"] == manifest["validation_row_count"]
    assert counts["test"] == summary["test_rows"] == manifest["test_row_count"]

    uci = pd.read_csv(UCI_ASSIGN)
    uci_summary = _load_json(UCI_SUMMARY)
    uci_manifest = _load_json(UCI_MANIFEST)
    uci_counts = uci["split"].value_counts().to_dict()
    assert uci_counts["train"] == uci_summary["train_rows"] == uci_manifest["train_row_count"]
    assert uci_counts["validation"] == uci_summary["validation_rows"] == uci_manifest["validation_row_count"]
    assert uci_counts["test"] == uci_summary["test_rows"] == uci_manifest["test_row_count"]


def test_dataset_hash_matches_recorded_raw_artifact() -> None:
    lc_hash = sha256_file(LC_RAW)
    uci_hash = sha256_file(UCI_RAW)
    assert lc_hash == RECORDED_LC_SHA256
    assert uci_hash == RECORDED_UCI_SHA256
    assert _load_json(LC_MANIFEST)["dataset_hash"] == lc_hash
    assert _load_json(UCI_MANIFEST)["dataset_hash"] == uci_hash
    raw_manifest = _load_json(RAW_MANIFEST)
    by_name = {row["filename"]: row for row in raw_manifest}
    assert by_name[EXPECTED_LC_FILENAME]["sha256"] == lc_hash
    assert by_name[EXPECTED_UCI_ZIP_FILENAME]["sha256"] == uci_hash


def test_issue_d_absent_from_model_feature_list() -> None:
    policy = pd.read_csv(LC_POLICY)
    rows = policy.to_dict("records")
    model_cols = policy_model_columns(rows)
    assert "issue_d" not in model_cols
    issue = policy.loc[policy["column"] == "issue_d"].iloc[0]
    assert issue["role"] == "TIME_INDEX"
    assert issue["status"] == "EXCLUDE"
    assert issue["model_use"] == "EXCLUDE_FROM_MODEL"


def test_experience_c_absent_from_model_feature_list() -> None:
    policy = pd.read_csv(LC_POLICY)
    rows = policy.to_dict("records")
    model_cols = policy_model_columns(rows)
    assert "experience_c" not in model_cols
    exp = policy.loc[policy["column"] == "experience_c"].iloc[0]
    assert exp["role"] == "EXCLUDED"
    assert exp["status"] == "EXCLUDE"


def test_default_is_the_target() -> None:
    policy = pd.read_csv(LC_POLICY)
    targets = policy.loc[policy["role"] == "TARGET", "column"].tolist()
    assert targets == ["Default"]
    assert _load_json(TARGET_DEF)["target"] == "Default"
    assert _load_json(LC_MANIFEST)["target_column"] == "Default"


def test_no_uci_rows_merged_into_lendingclub() -> None:
    lc_assign = pd.read_csv(LC_ASSIGN)
    uci_assign = pd.read_csv(UCI_ASSIGN)
    assert "ID" not in lc_assign.columns
    assert "id" not in uci_assign.columns
    assert "issue_month" not in uci_assign.columns
    assert not (ROOT / "results" / "tables" / "lendingclub_uci_merged.csv").exists()
    assert _load_json(UCI_MANIFEST)["merged_with_lendingclub"] is False
    assert _load_json(UCI_SUMMARY)["merged_with_lendingclub"] is False
    uci_policy = pd.read_csv(UCI_POLICY)
    assert "Default" not in set(uci_policy["column"])
    assert "issue_d" not in set(uci_policy["column"])


def test_membership_hashes_match_manifest() -> None:
    lc = pd.read_csv(LC_ASSIGN)
    manifest = _load_json(LC_MANIFEST)
    for split, key in (("train", "train_hash"), ("validation", "validation_hash"), ("test", "test_hash")):
        part = lc.loc[lc["split"] == split]
        assert membership_hash(part["id"].tolist(), part["issue_month"].tolist()) == manifest[key]
    uci = pd.read_csv(UCI_ASSIGN)
    uci_manifest = _load_json(UCI_MANIFEST)
    for split, key in (("train", "train_hash"), ("validation", "validation_hash"), ("test", "test_hash")):
        part = uci.loc[uci["split"] == split]
        assert membership_hash(part["ID"].tolist(), part["ID"].tolist()) == uci_manifest[key]


def test_uci_codes_were_not_recoded() -> None:
    summary = _load_json(UCI_SUMMARY)
    assert summary["recode_applied"] is False
    fields = {item["column"]: item for item in summary["undocumented_codes"]["fields"]}
    assert 0 in fields["EDUCATION"]["undocumented_values_observed"]
    assert 0 in fields["MARRIAGE"]["undocumented_values_observed"]
    assert 0 in fields["PAY_0"]["undocumented_values_observed"]
    assert -2 in fields["PAY_0"]["undocumented_values_observed"]
    uci_predictors = policy_uci_model_columns(pd.read_csv(UCI_POLICY).to_dict("records"))
    assert "ID" not in uci_predictors
    assert "default payment next month" not in uci_predictors
    assert len(uci_predictors) == 23
