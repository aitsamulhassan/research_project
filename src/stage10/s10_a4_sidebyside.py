"""S10-A4-SIDEBYSIDE: cite stored LC and UCI TEST evidence. No recomputation.

Analysis-only / descriptive comparison. Not confirmatory.
Does not train, calibrate, select thresholds, rescore TEST, or reopen UCI TEST.
XGBoost is not in the primary table.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

from decision.stage9_1 import sha256_file

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_ID = "s10_a4_sidebyside_v1"
CLASSIFICATION = "ANALYSIS-ONLY / DESCRIPTIVE COMPARISON"
ACTIVITY_ID = "S10-A4-SIDEBYSIDE"

STAGE5_TEST = ROOT / "results" / "calibration" / "metrics" / "stage5_test_metrics.json"
STAGE4B_TEST = ROOT / "results" / "metrics" / "stage4b_test_metrics.json"
STAGE4B_AUDIT = ROOT / "audit" / "stage4b_modeling_run.json"
STAGE5_AUDIT = ROOT / "audit" / "stage5_calibration_run.json"
SPLIT_MANIFEST = ROOT / "audit" / "lendingclub_split_manifest.json"
TRAIN_ONLY_META = ROOT / "experiments" / "stage5_calibration" / "checkpoints" / "train_only_ebm_meta.json"
PLATT_RECORD = ROOT / "results" / "calibration" / "artifacts" / "platt_record.json"
ISOTONIC_RECORD = ROOT / "results" / "calibration" / "artifacts" / "isotonic_record.json"
SELECTION = ROOT / "experiments" / "stage5_calibration" / "selected_calibration.json"
TABLE3 = ROOT / "results" / "decision" / "v2" / "tables" / "table3_test_decision_outcomes.csv"
STAGE9_1_AUDIT = ROOT / "audit" / "stage9_1_ablation_run.json"
A1_METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_a1_gap.json"
UCI_FAMILY_RAW = ROOT / "results" / "uci_generalization" / "v1" / "tables" / "uci_test_family_raw.csv"
UCI_SELECTED = ROOT / "results" / "uci_generalization" / "v1" / "metrics" / "uci_test_selected.json"
STAGE9_4_AUDIT = ROOT / "audit" / "stage9_4_uci_run.json"
STAGE9_4_REPORT = ROOT / "docs" / "STAGE_9_4_UCI_GENERALIZATION_REPORT.md"
I1_METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json"
R1_METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_r1_year.json"

EXPECTED_STAGE5_SHA256 = "a6c8ab44676d62109c1a346dbcf14a12a745b761f13b9fda6a9002853fc326e3"
EXPECTED_STAGE4B_SHA256 = "960c01643a671805daa1c692e9034454a94d6088651c6336076433b3e8bdc612"
EXPECTED_TABLE3_SHA256 = "90759eb72f1173b40b5b9363c21b0ef3d6f1cde5042748eb57871d49fb73d5ee"
EXPECTED_N = 208886
EXPECTED_DATASET_HASH = "207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc"
EXPECTED_SPLIT_MANIFEST_HASH = "d4db2099199258ae5ca4f5a85a7ce8e7dde2943a0bf7b9239212cce1e44d0e70"
EXPECTED_TEST_HASH = "4dfedb1ad7785fa3833047135b1883676f3e1b49aca9c87fcdb346e64fd489c6"
EXPECTED_EBM_JOBLIB_SHA256 = "8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4"
EXPECTED_TEST_CAL_SHA256 = "e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb"
EXPECTED_STAGE4B_EBM_ROC = 0.6799408767429772
EXPECTED_STAGE5_RAW_ROC = 0.6776693941139847
EXPECTED_POLICY = {
    "A0": {"APPROVE": 5232, "HUMAN_REVIEW": 203627, "REJECT": 27},
    "A1": {"APPROVE": 0, "HUMAN_REVIEW": 208859, "REJECT": 27},
    "A3": {"APPROVE": 61855, "HUMAN_REVIEW": 0, "REJECT": 147031},
}
TABLE3_ARCH = {
    "credit_only_selected_bands": "A0",
    "fused_evidence_separated_v2": "A1",
    "monolithic_credit_threshold": "A3",
}
METRIC_KEYS = ("roc_auc", "pr_auc", "brier", "log_loss", "ece")
COMPACT_HP_KEYS = (
    "interactions",
    "max_bins",
    "learning_rate",
    "max_rounds",
    "outer_bags",
    "inner_bags",
    "validation_size",
    "early_stopping_rounds",
    "random_state",
)


def json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    return obj


def _metrics(src: dict[str, Any], *, ece_present: bool) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in ("roc_auc", "pr_auc", "brier", "log_loss"):
        out[key] = float(src[key]) if key in src and src[key] is not None else None
    out["ece"] = float(src["ece"]) if ece_present and src.get("ece") is not None else None
    out["n"] = int(src["n"]) if src.get("n") is not None else None
    return out


def _row(
    *,
    dataset: str,
    model: str,
    calibration: str,
    evidence_status: str,
    source: str,
    metrics: dict[str, Any],
    primary: bool,
) -> dict[str, Any]:
    return {
        "dataset": dataset,
        "model": model,
        "calibration": calibration,
        "existing_test_roc_auc": metrics.get("roc_auc"),
        "existing_test_pr_auc": metrics.get("pr_auc"),
        "existing_test_brier": metrics.get("brier"),
        "existing_test_log_loss": metrics.get("log_loss"),
        "existing_test_ece": metrics.get("ece"),
        "n": metrics.get("n"),
        "evidence_status": evidence_status,
        "source_artifact": source,
        "primary_comparison": primary,
        "metrics_recomputed": False,
    }


def _compact_hp(config: dict[str, Any] | None) -> dict[str, Any]:
    if not config:
        return {}
    return {key: config.get(key) for key in COMPACT_HP_KEYS if key in config}


def require_prior_stage10() -> dict[str, Any]:
    missing = [str(p) for p in (I1_METRICS, R1_METRICS, A1_METRICS) if not p.exists()]
    if missing:
        raise RuntimeError(f"S10-A4 aborted: prior Stage 10 metrics missing: {missing}")
    i1 = json.loads(I1_METRICS.read_text(encoding="utf-8"))
    r1 = json.loads(R1_METRICS.read_text(encoding="utf-8"))
    a1 = json.loads(A1_METRICS.read_text(encoding="utf-8"))
    if not str(i1.get("status") or "").startswith("PASS"):
        raise RuntimeError(f"S10-A4 aborted: S10-I1 status={i1.get('status')!r}.")
    if not str(r1.get("status") or "").startswith("COMPLETED"):
        raise RuntimeError(f"S10-A4 aborted: S10-R1 status={r1.get('status')!r}.")
    if not str(a1.get("status") or "").startswith("COMPLETED"):
        raise RuntimeError(f"S10-A4 aborted: S10-A1 status={a1.get('status')!r}.")
    return {
        "i1_status": i1.get("status"),
        "r1_status": r1.get("status"),
        "a1_status": a1.get("status"),
    }


def _stage5_by_method() -> dict[str, dict[str, Any]]:
    rows = json.loads(STAGE5_TEST.read_text(encoding="utf-8"))
    return {str(row["method"]): row for row in rows}


def _stage4b_by_family() -> dict[str, dict[str, Any]]:
    rows = json.loads(STAGE4B_TEST.read_text(encoding="utf-8"))
    return {str(row["family"]): row for row in rows}


def _uci_family_raw() -> dict[str, dict[str, Any]]:
    frame = pd.read_csv(UCI_FAMILY_RAW)
    out: dict[str, dict[str, Any]] = {}
    for _, row in frame.iterrows():
        out[str(row["family"])] = row.to_dict()
    return out


def _abort(issues: list[str], documentation_limitations: list[str], gates: dict[str, Any] | None = None) -> dict[str, Any]:
    return json_safe(
        {
            "experiment_id": EXPERIMENT_ID,
            "activity_id": ACTIVITY_ID,
            "classification": CLASSIFICATION,
            "audit_classification": "INVALID",
            "status": "INVALID — source metric artifact mismatch",
            "confirmatory_experiment": False,
            "issues": issues,
            "documentation_limitations": documentation_limitations,
            "prior_gates": gates or {},
            "models_trained": False,
            "models_loaded_for_scoring": False,
            "metrics_recomputed": False,
            "uci_reopened": False,
            "stage9_reopened": False,
            "discrepancy_reopened": False,
        }
    )


def dataset_context_rows() -> list[dict[str, Any]]:
    return [
        {
            "dataset": "LendingClub granting extract",
            "target_definition": "Default; 1=Charged Off, 0=Fully Paid",
            "split_methodology": "Temporal by issue_month; TEST issue_month >= 2017-02; n=208886",
            "role_in_research_architecture": "Primary dataset for the evidence-separated decision architecture (credit bands + L1/L2 + G0)",
            "shariah_governance_applied": "Yes (Stage 7 v2 L1/L2 + Stage 8 v2 G0 on LC TEST)",
            "targets_equivalent_to_the_other_dataset": False,
        },
        {
            "dataset": "UCI Default of Credit Card Clients",
            "target_definition": "default payment next month; 1=default next month, 0=no default next month",
            "split_methodology": "Stratified 70/15/15, seed 42; NO_CALENDAR_TIMESTAMPS; TEST n=4502",
            "role_in_research_architecture": "Independent credit-risk / calibration methodology context only. Not a test of the evidence-separated architecture as a whole",
            "shariah_governance_applied": "No. UCI lacks contract-level fields (Stage 2 / U3 metadata-only). UCI does not validate Shariah governance",
            "targets_equivalent_to_the_other_dataset": False,
        },
    ]


def _policy_rows(table3: pd.DataFrame, stage9_1: dict[str, Any], a1_gap: dict[str, Any]) -> tuple[list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    by_arch = {str(row["architecture"]): row for _, row in table3.iterrows()}
    mapped: dict[str, dict[str, Any]] = {}
    for arch, policy_id in TABLE3_ARCH.items():
        if arch not in by_arch:
            issues.append(f"table3 missing architecture={arch}.")
            continue
        row = by_arch[arch]
        counts = {
            "APPROVE": int(row["n_approve"]),
            "HUMAN_REVIEW": int(row["n_review"]),
            "REJECT": int(row["n_reject"]),
        }
        if int(row["n"]) != EXPECTED_N:
            issues.append(f"table3 {arch} n={row['n']} != {EXPECTED_N}.")
        expected = EXPECTED_POLICY[policy_id]
        if counts != expected:
            issues.append(f"table3 {policy_id} counts {counts} != frozen {expected}.")
        mapped[policy_id] = counts

    for policy_id, key in (("A0", "a0_counts"), ("A1", "a1_counts"), ("A3", "a3_counts")):
        stored = stage9_1.get(key) or {}
        expected = EXPECTED_POLICY[policy_id]
        if {k: int(stored[k]) for k in expected} != expected:
            issues.append(f"Stage 9.1 {key} {stored} != frozen {expected}.")

    if stage9_1.get("a3_identical_to_a4") is not True:
        issues.append("Stage 9.1 a3_identical_to_a4 is not True.")

    l1 = a1_gap.get("l1") or {}
    l2_rows = a1_gap.get("l2_governance_states") or []
    l2_ii = next((r for r in l2_rows if r.get("l2_governance_status") == "INSUFFICIENT_INFORMATION"), None)
    evidence = {
        "A0": (
            "Governance off. Credit-only two-threshold map on stored p_selected "
            "(t_low=0.06, t_high=0.69). L1/L2 are not decision inputs."
        ),
        "A1": (
            f"G0 on. Stored L1={l1.get('status')} (n={l1.get('count')}; not an applicant-level ruling). "
            f"Stored L2 INSUFFICIENT_INFORMATION n={None if l2_ii is None else l2_ii.get('count')}. "
            "G0 maps INSUFFICIENT_INFORMATION × LOW/MEDIUM → HUMAN_REVIEW and × HIGH → REJECT."
        ),
        "A3": (
            "Governance off. Binary map on stored p_selected (t*=0.16). "
            "HUMAN_REVIEW branch absent by construction."
        ),
        "A4": (
            "Same object as A3 under the Stage 9.0 freeze (Stage 9.1 a3_identical_to_a4=true). "
            "Counts are not a second independent assignment."
        ),
    }
    source = TABLE3.as_posix()
    rows = [
        {
            "policy": "A0",
            "definition": "credit-only two-threshold",
            "probability_column": "p_selected",
            "thresholds": "t_low=0.06, t_high=0.69",
            "APPROVE": mapped.get("A0", {}).get("APPROVE"),
            "HUMAN_REVIEW": mapped.get("A0", {}).get("HUMAN_REVIEW"),
            "REJECT": mapped.get("A0", {}).get("REJECT"),
            "governance": "off",
            "evidence_gap_fields": evidence["A0"],
            "source_artifact": source,
            "assignments_recomputed": False,
        },
        {
            "policy": "A1",
            "definition": "evidence-separated G0 fusion",
            "probability_column": "p_selected",
            "thresholds": "t_low=0.06, t_high=0.69 plus frozen G0",
            "APPROVE": mapped.get("A1", {}).get("APPROVE"),
            "HUMAN_REVIEW": mapped.get("A1", {}).get("HUMAN_REVIEW"),
            "REJECT": mapped.get("A1", {}).get("REJECT"),
            "governance": "G0 on (Stage 7 v2 L2)",
            "evidence_gap_fields": evidence["A1"],
            "source_artifact": source,
            "assignments_recomputed": False,
        },
        {
            "policy": "A3",
            "definition": "binary no-review comparator",
            "probability_column": "p_selected",
            "thresholds": "t*=0.16",
            "APPROVE": mapped.get("A3", {}).get("APPROVE"),
            "HUMAN_REVIEW": mapped.get("A3", {}).get("HUMAN_REVIEW"),
            "REJECT": mapped.get("A3", {}).get("REJECT"),
            "governance": "off",
            "evidence_gap_fields": evidence["A3"],
            "source_artifact": source,
            "assignments_recomputed": False,
        },
        {
            "policy": "A4",
            "definition": "collapses to A3 (Stage 9.0 freeze)",
            "probability_column": "p_selected",
            "thresholds": "t*=0.16",
            "APPROVE": mapped.get("A3", {}).get("APPROVE"),
            "HUMAN_REVIEW": mapped.get("A3", {}).get("HUMAN_REVIEW"),
            "REJECT": mapped.get("A3", {}).get("REJECT"),
            "governance": "off",
            "evidence_gap_fields": evidence["A4"],
            "source_artifact": STAGE9_1_AUDIT.as_posix(),
            "assignments_recomputed": False,
        },
    ]
    return rows, issues


def run_sidebyside() -> dict[str, Any]:
    issues: list[str] = []
    documentation_limitations: list[str] = [
        "LendingClub and UCI targets are not equivalent; rows are not merged; no AUC equality test is performed.",
        "UCI does not apply Shariah governance and cannot validate the LC evidence-separated architecture.",
        "Stage 4B LC TEST tables do not store ECE; UCI family-raw TEST tables do not store ECE for LR or EBM.",
        "Stage 5 calibrated LC TEST (raw/Platt/isotonic) is EBM-only. LC logistic regression has no stored Platt TEST row.",
        "Stage 4B final EBM joblib SHA-256 is not recorded in existing artifacts. The dump path is documented; the hash is unavailable without computing it, which this activity does not do.",
        "Stage 4B TRAIN+VALIDATION concatenated training-row total is not stored as a single field; TRAIN=941267 and VALIDATION=197528 are stored separately.",
        "S10-A4 cites stored metrics and counts only. It is not a confirmatory TEST experiment and produces no model ranking.",
    ]
    try:
        gates = require_prior_stage10()
    except RuntimeError as exc:
        return json_safe(
            {
                "experiment_id": EXPERIMENT_ID,
                "activity_id": ACTIVITY_ID,
                "classification": CLASSIFICATION,
                "audit_classification": "INVALID",
                "status": "INVALID — prior Stage 10 gate failed",
                "confirmatory_experiment": False,
                "issues": [str(exc)],
                "models_trained": False,
                "uci_reopened": False,
                "discrepancy_reopened": False,
            }
        )

    h5 = sha256_file(STAGE5_TEST)
    h4 = sha256_file(STAGE4B_TEST)
    h_uci = sha256_file(UCI_FAMILY_RAW)
    h_sel = sha256_file(UCI_SELECTED)
    h_table3 = sha256_file(TABLE3)
    if h5 != EXPECTED_STAGE5_SHA256:
        issues.append("stage5_test_metrics.json SHA-256 does not match Stage 9.4 protected hash.")
    if h4 != EXPECTED_STAGE4B_SHA256:
        issues.append("stage4b_test_metrics.json SHA-256 does not match Stage 9.4 protected hash.")
    if h_table3 != EXPECTED_TABLE3_SHA256:
        issues.append("table3_test_decision_outcomes.csv SHA-256 does not match Stage 9.1 recorded hash.")

    stage5 = _stage5_by_method()
    stage4b = _stage4b_by_family()
    uci_raw = _uci_family_raw()
    uci_selected = json.loads(UCI_SELECTED.read_text(encoding="utf-8"))
    stage4b_audit = json.loads(STAGE4B_AUDIT.read_text(encoding="utf-8"))
    stage5_audit = json.loads(STAGE5_AUDIT.read_text(encoding="utf-8"))
    manifest = json.loads(SPLIT_MANIFEST.read_text(encoding="utf-8"))
    meta = json.loads(TRAIN_ONLY_META.read_text(encoding="utf-8"))
    platt = json.loads(PLATT_RECORD.read_text(encoding="utf-8"))
    isotonic = json.loads(ISOTONIC_RECORD.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    stage9_1 = json.loads(STAGE9_1_AUDIT.read_text(encoding="utf-8"))
    a1_gap = json.loads(A1_METRICS.read_text(encoding="utf-8"))
    table3 = pd.read_csv(TABLE3)

    for required in ("raw", "platt", "isotonic"):
        if required not in stage5:
            issues.append(f"Stage 5 TEST metrics missing method={required}.")
    if "logistic_regression" not in stage4b:
        issues.append("Stage 4B TEST metrics missing logistic_regression.")
    if "explainable_boosting_machine" not in stage4b:
        issues.append("Stage 4B TEST metrics missing explainable_boosting_machine.")
    if "logistic_regression" not in uci_raw or "explainable_boosting_machine" not in uci_raw:
        issues.append("UCI family-raw TEST table missing LR or EBM.")
    if str(meta.get("trained_on")) != "TRAIN_ONLY":
        issues.append("train_only_ebm_meta.json trained_on is not TRAIN_ONLY.")
    if stage4b_audit.get("split_manifest_hash") != EXPECTED_SPLIT_MANIFEST_HASH:
        issues.append("Stage 4B split_manifest_hash does not match the frozen Stage 3 manifest hash.")
    if stage5_audit.get("split_manifest_hash") != EXPECTED_SPLIT_MANIFEST_HASH:
        issues.append("Stage 5 split_manifest_hash does not match the frozen Stage 3 manifest hash.")
    if manifest.get("test_hash") != EXPECTED_TEST_HASH:
        issues.append("Stage 3 split manifest test_hash does not match the recorded frozen value.")
    if int(manifest.get("test_row_count") or 0) != EXPECTED_N:
        issues.append("Stage 3 split manifest test_row_count is not 208886.")

    policy_rows, policy_issues = _policy_rows(table3, stage9_1, a1_gap)
    issues.extend(policy_issues)

    if issues:
        return _abort(issues, documentation_limitations, gates)

    lc_lr = _metrics(stage4b["logistic_regression"], ece_present=False)
    lc_ebm_4b = _metrics(stage4b["explainable_boosting_machine"], ece_present=False)
    lc_ebm_raw = _metrics(stage5["raw"], ece_present=True)
    lc_ebm_platt = _metrics(stage5["platt"], ece_present=True)
    lc_ebm_iso = _metrics(stage5["isotonic"], ece_present=True)
    uci_lr = _metrics(uci_raw["logistic_regression"], ece_present=False)
    uci_ebm = _metrics(uci_raw["explainable_boosting_machine"], ece_present=False)
    xgb_raw = _metrics(uci_raw["xgboost"], ece_present=False) if "xgboost" in uci_raw else None
    xgb_iso = _metrics(uci_selected, ece_present=True)

    if lc_ebm_4b["roc_auc"] != EXPECTED_STAGE4B_EBM_ROC:
        return _abort(
            [f"Stage 4B EBM TEST ROC-AUC {lc_ebm_4b['roc_auc']} != recorded 0.6799408767429772."],
            documentation_limitations,
            gates,
        )
    if lc_ebm_raw["roc_auc"] != EXPECTED_STAGE5_RAW_ROC:
        return _abort(
            [f"Stage 5 raw EBM TEST ROC-AUC {lc_ebm_raw['roc_auc']} != recorded 0.6776693941139847."],
            documentation_limitations,
            gates,
        )
    if lc_ebm_platt["roc_auc"] != lc_ebm_raw["roc_auc"]:
        return _abort(
            ["Stored Stage 5 Platt TEST ROC-AUC is not identical to stored raw TEST ROC-AUC."],
            documentation_limitations,
            gates,
        )
    for label, metrics in (("Stage 4B EBM", lc_ebm_4b), ("Stage 5 raw", lc_ebm_raw), ("Stage 5 Platt", lc_ebm_platt)):
        if metrics.get("n") != EXPECTED_N:
            return _abort([f"{label} stored n={metrics.get('n')} != 208886."], documentation_limitations, gates)

    hp_4b = _compact_hp(stage4b["explainable_boosting_machine"].get("config") or {})
    hp_5 = _compact_hp(meta.get("config") or {})
    model_evidence = [
        {
            "evidence_id": "stage4b_ebm_test",
            "label": "Stage 4B EBM TEST",
            "model_family": "explainable_boosting_machine",
            "model_artifact_path": "results/artifacts/final_explainable_boosting_machine_seed42.joblib",
            "model_hash": None,
            "model_hash_status": "not recorded in existing artifacts",
            "training_split": "TRAIN+VALIDATION refit",
            "training_row_count": None,
            "training_row_count_note": "TRAIN=941267 + VALIDATION=197528; concatenated total not stored as a single field",
            "seed": 42,
            "hyperparameters": hp_4b,
            "preprocessing_artifact": "results/artifacts/preprocessor_train_plus_validation.joblib",
            "prediction_artifact": "results/predictions/test/explainable_boosting_machine_seed42.csv",
            "probability_type": "raw (p_hat)",
            "stored_roc_auc": lc_ebm_4b["roc_auc"],
            "stored_pr_auc": lc_ebm_4b["pr_auc"],
            "stored_brier": lc_ebm_4b["brier"],
            "stored_log_loss": lc_ebm_4b["log_loss"],
            "stored_ece": None,
            "n": lc_ebm_4b["n"],
            "used_by_stage8_onward": False,
            "provenance_status": "freeze-backed Stage 4B TEST; TRAIN+VALIDATION refit",
            "source_artifact": STAGE4B_TEST.as_posix(),
        },
        {
            "evidence_id": "stage5_ebm_raw_test",
            "label": "Stage 5 TRAIN-only EBM raw TEST",
            "model_family": "explainable_boosting_machine",
            "model_artifact_path": "results/calibration/artifacts/ebm_train_only_seed42.joblib",
            "model_hash": EXPECTED_EBM_JOBLIB_SHA256,
            "model_hash_status": "recorded (Stage 9.1 verify_frozen_artifacts)",
            "training_split": "TRAIN-only fit",
            "training_row_count": int(meta["n_train"]),
            "training_row_count_note": "n_train recorded in train_only_ebm_meta.json",
            "seed": 42,
            "hyperparameters": hp_5,
            "preprocessing_artifact": str(meta.get("preprocessor")),
            "prediction_artifact": "results/calibration/raw/ebm_train_only_seed42_test.csv",
            "probability_type": "raw (p_raw)",
            "stored_roc_auc": lc_ebm_raw["roc_auc"],
            "stored_pr_auc": lc_ebm_raw["pr_auc"],
            "stored_brier": lc_ebm_raw["brier"],
            "stored_log_loss": lc_ebm_raw["log_loss"],
            "stored_ece": lc_ebm_raw["ece"],
            "n": lc_ebm_raw["n"],
            "used_by_stage8_onward": False,
            "provenance_status": "freeze-backed Stage 5 TEST raw; TRAIN-only fit",
            "source_artifact": STAGE5_TEST.as_posix(),
        },
        {
            "evidence_id": "stage5_ebm_platt_test",
            "label": "Stage 5 calibrated TEST (selected Platt)",
            "model_family": "explainable_boosting_machine",
            "model_artifact_path": "results/calibration/artifacts/ebm_train_only_seed42.joblib",
            "model_hash": EXPECTED_EBM_JOBLIB_SHA256,
            "model_hash_status": "recorded (Stage 9.1 verify_frozen_artifacts)",
            "training_split": "TRAIN-only fit",
            "training_row_count": int(meta["n_train"]),
            "training_row_count_note": "same TRAIN-only EBM as Stage 5 raw; Platt fit on VALIDATION only",
            "seed": 42,
            "hyperparameters": hp_5,
            "preprocessing_artifact": str(meta.get("preprocessor")),
            "prediction_artifact": "results/calibration/test/ebm_seed42_calibrated.csv",
            "probability_type": "calibrated (p_selected = p_platt)",
            "stored_roc_auc": lc_ebm_platt["roc_auc"],
            "stored_pr_auc": lc_ebm_platt["pr_auc"],
            "stored_brier": lc_ebm_platt["brier"],
            "stored_log_loss": lc_ebm_platt["log_loss"],
            "stored_ece": lc_ebm_platt["ece"],
            "n": lc_ebm_platt["n"],
            "used_by_stage8_onward": True,
            "provenance_status": "freeze-backed Stage 5 selected calibrator; frozen Stage 8/9 probability",
            "source_artifact": STAGE5_TEST.as_posix(),
        },
    ]

    calibration_evidence = {
        "raw_probability_artifact": "results/calibration/raw/ebm_train_only_seed42_test.csv",
        "calibrated_probability_artifact": "results/calibration/test/ebm_seed42_calibrated.csv",
        "methods_stored": ["raw", "platt", "isotonic"],
        "selected_method": selection.get("selected_method"),
        "frozen_selected_probability_column": "p_selected",
        "selected_column_equals_stored": "p_platt",
        "fit_split": "validation",
        "protocol": stage5_audit.get("protocol"),
        "platt_parameters": {
            "a": platt.get("a"),
            "b": platt.get("b"),
            "form": platt.get("form"),
            "fit_split": platt.get("fit_split"),
        },
        "isotonic_parameters": {
            "y_min": isotonic.get("y_min"),
            "y_max": isotonic.get("y_max"),
            "out_of_bounds": isotonic.get("out_of_bounds"),
            "increasing": isotonic.get("increasing"),
            "fit_split": isotonic.get("fit_split"),
        },
        "stored_test_roc_auc": {
            "raw": lc_ebm_raw["roc_auc"],
            "platt": lc_ebm_platt["roc_auc"],
            "isotonic": lc_ebm_iso["roc_auc"],
        },
        "calibration_changes_roc_auc_according_to_stored_metrics": {
            "platt_vs_raw": lc_ebm_platt["roc_auc"] != lc_ebm_raw["roc_auc"],
            "isotonic_vs_raw": lc_ebm_iso["roc_auc"] != lc_ebm_raw["roc_auc"],
            "note": (
                "Stored Platt TEST ROC-AUC equals stored raw TEST ROC-AUC. "
                "Stored isotonic TEST ROC-AUC differs slightly. "
                "No calibrator was fit or compared in S10-A4."
            ),
        },
        "source_artifacts": [
            STAGE5_TEST.as_posix(),
            PLATT_RECORD.as_posix(),
            ISOTONIC_RECORD.as_posix(),
            SELECTION.as_posix(),
        ],
    }

    test_provenance = {
        "test_n_stage3_manifest": int(manifest["test_row_count"]),
        "test_n_stage4b_ebm_metrics": lc_ebm_4b["n"],
        "test_n_stage5_raw_metrics": lc_ebm_raw["n"],
        "test_n_stage5_platt_metrics": lc_ebm_platt["n"],
        "test_n_table3": EXPECTED_N,
        "stage3_test_hash": manifest.get("test_hash"),
        "stage3_test_rule": manifest.get("test_rule"),
        "dataset_hash_manifest": manifest.get("dataset_hash"),
        "dataset_hash_stage4b_audit": stage4b_audit.get("dataset_hash"),
        "dataset_hash_stage5_audit": stage5_audit.get("dataset_hash"),
        "split_manifest_hash_stage4b_audit": stage4b_audit.get("split_manifest_hash"),
        "split_manifest_hash_stage5_audit": stage5_audit.get("split_manifest_hash"),
        "expected_dataset_hash": EXPECTED_DATASET_HASH,
        "expected_split_manifest_hash": EXPECTED_SPLIT_MANIFEST_HASH,
        "expected_test_hash": EXPECTED_TEST_HASH,
        "same_frozen_test_split_according_to_recorded_hashes": (
            manifest.get("test_hash") == EXPECTED_TEST_HASH
            and stage4b_audit.get("split_manifest_hash") == EXPECTED_SPLIT_MANIFEST_HASH
            and stage5_audit.get("split_manifest_hash") == EXPECTED_SPLIT_MANIFEST_HASH
            and stage4b_audit.get("dataset_hash") == EXPECTED_DATASET_HASH
            and stage5_audit.get("dataset_hash") == EXPECTED_DATASET_HASH
            and lc_ebm_4b["n"] == EXPECTED_N
            and lc_ebm_raw["n"] == EXPECTED_N
        ),
        "membership_recomputed": False,
        "split_manifest_path": SPLIT_MANIFEST.as_posix(),
    }

    discrepancy = {
        "classification": "EXPLAINED",
        "stage4b_ebm_test_roc_auc": lc_ebm_4b["roc_auc"],
        "stage5_ebm_raw_test_roc_auc": lc_ebm_raw["roc_auc"],
        "same_frozen_test_split": True,
        "same_roc_auc_implementation_recorded": "evaluation.metrics.roc_auc wrapper used by Stage 4B and Stage 5",
        "reason": (
            "Stage 4B TEST ROC-AUC comes from an EBM refit on TRAIN+VALIDATION. "
            "Stage 5 raw TEST ROC-AUC comes from a separately fitted TRAIN-only EBM. "
            "Both use the same frozen TEST split (n=208886) and the same recorded ROC-AUC implementation. "
            "Stage 8 onward uses the Stage 5 TRAIN-only EBM / stored calibrated p_selected. "
            "The difference is not treated as a contradiction. S10-A4 does not reopen that investigation."
        ),
        "investigation_reopened": False,
        "correction_required": False,
    }

    primary = [
        _row(
            dataset="LendingClub",
            model="logistic_regression",
            calibration="none (Stage 4B TEST; no stored Platt row)",
            evidence_status="freeze-backed Stage 4B TEST citation",
            source=STAGE4B_TEST.as_posix(),
            metrics=lc_lr,
            primary=True,
        ),
        _row(
            dataset="LendingClub",
            model="explainable_boosting_machine",
            calibration="raw (Stage 5 TEST; TRAIN-only EBM)",
            evidence_status="freeze-backed Stage 5 TEST citation",
            source=STAGE5_TEST.as_posix(),
            metrics=lc_ebm_raw,
            primary=True,
        ),
        _row(
            dataset="LendingClub",
            model="explainable_boosting_machine",
            calibration="platt (Stage 5 selected calibrator; frozen decision pipeline)",
            evidence_status="freeze-backed Stage 5 TEST citation",
            source=STAGE5_TEST.as_posix(),
            metrics=lc_ebm_platt,
            primary=True,
        ),
        _row(
            dataset="UCI",
            model="logistic_regression",
            calibration="raw (Stage 9.4 family TEST; not UCI-selected family)",
            evidence_status="freeze-backed Stage 9.4 approved scope (LR+EBM)",
            source=UCI_FAMILY_RAW.as_posix(),
            metrics=uci_lr,
            primary=True,
        ),
        _row(
            dataset="UCI",
            model="explainable_boosting_machine",
            calibration="raw (Stage 9.4 family TEST; not UCI-selected family)",
            evidence_status="freeze-backed Stage 9.4 approved scope (LR+EBM)",
            source=UCI_FAMILY_RAW.as_posix(),
            metrics=uci_ebm,
            primary=True,
        ),
    ]
    exploratory = []
    if xgb_raw is not None:
        exploratory.append(
            _row(
                dataset="UCI",
                model="xgboost",
                calibration="raw (Stage 9.4 family TEST)",
                evidence_status="EXPLORATORY — execution-time scope expansion; NOT ratified; NOT pre-registered",
                source=UCI_FAMILY_RAW.as_posix(),
                metrics=xgb_raw,
                primary=False,
            )
        )
    exploratory.append(
        _row(
            dataset="UCI",
            model="xgboost",
            calibration="isotonic (Stage 9.4 selected UCI TEST row)",
            evidence_status="EXPLORATORY — execution-time scope expansion; NOT ratified; NOT pre-registered",
            source=UCI_SELECTED.as_posix(),
            metrics=xgb_iso,
            primary=False,
        )
    )

    missing = [
        "LendingClub logistic_regression ECE: not stored in Stage 4B TEST artifacts.",
        "UCI logistic_regression ECE: not stored in uci_test_family_raw.csv.",
        "UCI explainable_boosting_machine ECE: not stored in uci_test_family_raw.csv.",
        "LendingClub logistic_regression Platt/isotonic TEST: not stored (Stage 5 calibrated EBM only).",
        "UCI LR/EBM calibrated TEST (Platt/isotonic): not stored as family TEST rows; Stage 9.4 calibrated TEST is the exploratory selected XGBoost row.",
        "Stage 4B final_explainable_boosting_machine_seed42.joblib SHA-256: not recorded.",
        "git_commit may be null; not fabricated.",
    ]

    return json_safe(
        {
            "experiment_id": EXPERIMENT_ID,
            "activity_id": ACTIVITY_ID,
            "classification": CLASSIFICATION,
            "audit_classification": "PASS WITH DOCUMENTATION LIMITATION",
            "status": "PASS WITH DOCUMENTATION LIMITATION",
            "confirmatory_experiment": False,
            "new_confirmatory_experiment_performed": False,
            "issues": [],
            "documentation_limitations": documentation_limitations,
            "missing_metrics": missing,
            "prior_gates": gates,
            "model_evidence": model_evidence,
            "calibration_evidence": calibration_evidence,
            "policy_evidence": policy_rows,
            "test_provenance": test_provenance,
            "ebm_test_roc_discrepancy": discrepancy,
            "primary_rows": primary,
            "exploratory_xgboost_rows": exploratory,
            "dataset_context": dataset_context_rows(),
            "xgboost_in_primary_table": False,
            "xgboost_ratified": False,
            "overall_model_ranking_produced": False,
            "metrics_recomputed": False,
            "statistical_equality_test": False,
            "rows_merged_across_datasets": False,
            "lc_thresholds_transferred_to_uci": False,
            "lc_calibration_transferred_to_uci": False,
            "models_trained": False,
            "models_loaded_for_scoring": False,
            "calibration_refit": False,
            "thresholds_searched": False,
            "policy_assignments_recomputed": False,
            "uci_reopened": False,
            "uci_test_used_for_selection": False,
            "stage9_reopened": False,
            "discrepancy_reopened": False,
            "stage8_onward_probability_artifact": "results/calibration/test/ebm_seed42_calibrated.csv",
            "stage8_onward_model_artifact": "results/calibration/artifacts/ebm_train_only_seed42.joblib",
            "stage8_onward_model_hash": EXPECTED_EBM_JOBLIB_SHA256,
            "stage8_onward_test_cal_hash": EXPECTED_TEST_CAL_SHA256,
            "hashes": {
                "stage5_test_metrics_sha256": h5,
                "stage4b_test_metrics_sha256": h4,
                "uci_test_family_raw_sha256": h_uci,
                "uci_test_selected_sha256": h_sel,
                "table3_sha256": h_table3,
                "expected_stage5": EXPECTED_STAGE5_SHA256,
                "expected_stage4b": EXPECTED_STAGE4B_SHA256,
                "expected_table3": EXPECTED_TABLE3_SHA256,
                "recorded_ebm_train_only_joblib_sha256": EXPECTED_EBM_JOBLIB_SHA256,
                "recorded_test_cal_sha256": EXPECTED_TEST_CAL_SHA256,
            },
            "source_artifacts": [
                STAGE5_TEST.as_posix(),
                STAGE4B_TEST.as_posix(),
                STAGE4B_AUDIT.as_posix(),
                STAGE5_AUDIT.as_posix(),
                SPLIT_MANIFEST.as_posix(),
                TRAIN_ONLY_META.as_posix(),
                PLATT_RECORD.as_posix(),
                ISOTONIC_RECORD.as_posix(),
                SELECTION.as_posix(),
                TABLE3.as_posix(),
                STAGE9_1_AUDIT.as_posix(),
                A1_METRICS.as_posix(),
                UCI_FAMILY_RAW.as_posix(),
                UCI_SELECTED.as_posix(),
                STAGE9_4_REPORT.as_posix(),
                STAGE9_4_AUDIT.as_posix(),
            ],
            "random_seed_used": None,
            "authorized_stage10_activities_complete_after_this_run": True,
        }
    )
