"""S10-A4-SIDEBYSIDE tests. Citation only. No new AUC. No XGBoost in primary table."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stage10.s10_a4_sidebyside import CLASSIFICATION, EXPERIMENT_ID, run_sidebyside  # noqa: E402

HELPER = ROOT / "src" / "stage10" / "s10_a4_sidebyside.py"
RUNNER = ROOT / "experiments" / "stage10_a4_sidebyside" / "run_s10_a4.py"
SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_a4_sidebyside.json"
REPORT = ROOT / "docs" / "STAGE_10_S10_A4_SIDEBYSIDE_REPORT.md"
I1_SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json"
R1_SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_r1_year.json"
A1_SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_a1_gap.json"


def test_no_recompute_or_training_in_source() -> None:
    text = HELPER.read_text(encoding="utf-8") + "\n" + RUNNER.read_text(encoding="utf-8")
    assert ".fit(" not in text
    assert "joblib.load" not in text
    assert "roc_auc_score" not in text
    assert "sklearn.metrics" not in text
    assert "select_policy(" not in text
    assert "predict_proba" not in text
    helper = HELPER.read_text(encoding="utf-8")
    assert "pd.read_csv(TEST_CAL" not in helper
    assert "frozen_selected_probability_column" in helper


def test_primary_table_is_lr_ebm_only() -> None:
    payload = run_sidebyside()
    assert payload["issues"] == []
    assert payload["classification"] == CLASSIFICATION
    assert payload["confirmatory_experiment"] is False
    assert payload["metrics_recomputed"] is False
    assert payload["xgboost_in_primary_table"] is False
    assert payload["xgboost_ratified"] is False
    assert payload["overall_model_ranking_produced"] is False
    assert payload["uci_reopened"] is False
    assert payload["discrepancy_reopened"] is False
    assert payload["policy_assignments_recomputed"] is False
    models = {row["model"] for row in payload["primary_rows"]}
    assert models == {"logistic_regression", "explainable_boosting_machine"}
    assert all(row["primary_comparison"] is True for row in payload["primary_rows"])
    for row in payload["exploratory_xgboost_rows"]:
        assert row["model"] == "xgboost"
        assert "EXPLORATORY" in row["evidence_status"]
        assert row["primary_comparison"] is False


def test_cited_values_match_source_files() -> None:
    payload = run_sidebyside()
    lc_platt = [
        row
        for row in payload["primary_rows"]
        if row["dataset"] == "LendingClub" and "platt" in row["calibration"]
    ][0]
    uci_lr = [
        row
        for row in payload["primary_rows"]
        if row["dataset"] == "UCI" and row["model"] == "logistic_regression"
    ][0]
    uci_ebm = [
        row
        for row in payload["primary_rows"]
        if row["dataset"] == "UCI" and row["model"] == "explainable_boosting_machine"
    ][0]
    assert lc_platt["existing_test_roc_auc"] == 0.6776693941139847
    assert lc_platt["existing_test_brier"] == 0.15616920271522994
    assert abs(uci_lr["existing_test_roc_auc"] - 0.7572778277972128) < 1e-15
    assert abs(uci_ebm["existing_test_roc_auc"] - 0.7688563724378406) < 1e-15
    assert uci_lr["existing_test_ece"] is None
    assert uci_ebm["existing_test_ece"] is None


def test_model_evidence_distinguishes_train_splits() -> None:
    payload = run_sidebyside()
    by_id = {row["evidence_id"]: row for row in payload["model_evidence"]}
    assert by_id["stage4b_ebm_test"]["training_split"] == "TRAIN+VALIDATION refit"
    assert by_id["stage5_ebm_raw_test"]["training_split"] == "TRAIN-only fit"
    assert by_id["stage5_ebm_platt_test"]["training_split"] == "TRAIN-only fit"
    assert by_id["stage4b_ebm_test"]["stored_roc_auc"] == 0.6799408767429772
    assert by_id["stage5_ebm_raw_test"]["stored_roc_auc"] == 0.6776693941139847
    assert by_id["stage5_ebm_platt_test"]["stored_roc_auc"] == 0.6776693941139847
    assert by_id["stage4b_ebm_test"]["used_by_stage8_onward"] is False
    assert by_id["stage5_ebm_platt_test"]["used_by_stage8_onward"] is True
    assert by_id["stage4b_ebm_test"]["model_hash"] is None
    assert payload["ebm_test_roc_discrepancy"]["classification"] == "EXPLAINED"
    assert payload["ebm_test_roc_discrepancy"]["investigation_reopened"] is False
    cal = payload["calibration_evidence"]
    assert cal["selected_method"] == "platt"
    assert cal["calibration_changes_roc_auc_according_to_stored_metrics"]["platt_vs_raw"] is False
    assert payload["test_provenance"]["test_n_stage3_manifest"] == 208886
    assert payload["test_provenance"]["same_frozen_test_split_according_to_recorded_hashes"] is True
    assert payload["test_provenance"]["membership_recomputed"] is False


def test_policy_counts_are_cited_not_recomputed() -> None:
    payload = run_sidebyside()
    by_id = {row["policy"]: row for row in payload["policy_evidence"]}
    assert by_id["A0"]["APPROVE"] == 5232
    assert by_id["A0"]["HUMAN_REVIEW"] == 203627
    assert by_id["A0"]["REJECT"] == 27
    assert by_id["A1"]["APPROVE"] == 0
    assert by_id["A1"]["HUMAN_REVIEW"] == 208859
    assert by_id["A1"]["REJECT"] == 27
    assert by_id["A3"]["APPROVE"] == 61855
    assert by_id["A3"]["HUMAN_REVIEW"] == 0
    assert by_id["A3"]["REJECT"] == 147031
    assert by_id["A4"]["APPROVE"] == by_id["A3"]["APPROVE"]
    assert by_id["A4"]["HUMAN_REVIEW"] == 0
    assert all(row["assignments_recomputed"] is False for row in payload["policy_evidence"])
    assert payload["audit_classification"] == "PASS WITH DOCUMENTATION LIMITATION"


def test_report_has_required_sections_and_no_ranking_language_if_present() -> None:
    if not REPORT.exists():
        return
    text = REPORT.read_text(encoding="utf-8")
    lowered = text.lower()
    for heading in (
        "## 1. Purpose",
        "## 2. Authorization",
        "## 3. Data/provenance basis",
        "## 4. Model side-by-side comparison",
        "## 5. Calibration side-by-side comparison",
        "## 6. Policy side-by-side comparison",
        "## 7. TEST provenance",
        "## 8. Neutral interpretation",
        "## 9. Limitations",
        "## 10. Audit classification",
        "## 11. No new confirmatory experiment",
        "Stage 4B EBM: TRAIN+VALIDATION refit",
        "Stage 5 EBM: TRAIN-only fit",
        "No new confirmatory experiment was performed",
    ):
        assert heading in text
    assert "best model" not in lowered
    assert "winner" not in lowered
    assert "loser" not in lowered
    assert "validates shariah" not in lowered
    assert "superior" not in lowered
    assert "optimal" not in lowered


def test_prior_artifacts_remain() -> None:
    assert json.loads(I1_SUMMARY.read_text(encoding="utf-8"))["experiment_id"] == "s10_i1_identity_v1"
    assert json.loads(R1_SUMMARY.read_text(encoding="utf-8"))["experiment_id"] == "s10_r1_year_v1"
    assert json.loads(A1_SUMMARY.read_text(encoding="utf-8"))["experiment_id"] == "s10_a1_gap_v1"


def test_written_metrics_if_present() -> None:
    if not SUMMARY.exists():
        return
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["experiment_id"] == EXPERIMENT_ID
    assert payload["xgboost_in_primary_table"] is False
    assert payload["metrics_recomputed"] is False
    assert payload["new_confirmatory_experiment_performed"] is False
