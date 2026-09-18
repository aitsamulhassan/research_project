"""Stage 9.2 cost sensitivity on frozen Stage 8/9.1 decisions. No retraining. No threshold search."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd

from decision.cost_policy import CostScenario, expected_cost, expected_normalized_cost
from decision.stage9_1 import (
    EXPECTED_A1,
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_T_STAR,
    V1_FREEZE,
    V2_TABLE3,
    sha256_file,
    verify_frozen_artifacts,
)

ROOT = Path(__file__).resolve().parents[2]

EXPERIMENT_ID = "stage9_2_cost_sensitivity_lc_v1"
FN_FP_RATIOS = (1, 2, 5, 10)
RATIO_LABELS = tuple(f"FN:FP={r}:1" for r in FN_FP_RATIOS)
C_FP = 1.0
C_REVIEW_OVER_FP_THREE_WAY = 0.25
C_REVIEW_OVER_FP_BINARY = 0.0
PRIMARY_RATIO = 5

ARCHITECTURE_ROWS = {
    "A0": "credit_only_selected_bands",
    "A1": "fused_evidence_separated_v2",
    "A3_A4": "monolithic_credit_threshold",
}
REVIEW_COST_BY_SYSTEM = {
    "A0": C_REVIEW_OVER_FP_THREE_WAY,
    "A1": C_REVIEW_OVER_FP_THREE_WAY,
    "A3_A4": C_REVIEW_OVER_FP_BINARY,
}

TABLE2_VAL = ROOT / "results" / "decision" / "tables" / "table2_validation_threshold_selection.csv"
EXPERIMENT_G_CSV = ROOT / "results" / "decision" / "tables" / "experiment_g_review_cost_perturbation.csv"
STAGE91_SUMMARY = ROOT / "results" / "ablation" / "v1" / "metrics" / "ablation_summary.json"
STAGE91_REPORT = ROOT / "docs" / "STAGE_9_1_ABLATION_REPORT.md"
STAGE91_AUDIT = ROOT / "audit" / "stage9_1_ablation_run.json"
STAGE91_TABLE1 = ROOT / "results" / "ablation" / "v1" / "tables" / "table1_ablation_comparison.csv"

EXPERIMENT_G_STATUS = "NOT_EXECUTED — CITE_ONLY_PER_STAGE_9_0_FREEZE"
EXPERIMENT_G_DEFINITION = (
    "validation-only, c_review_over_fp in {0.10, 0.25, 0.50} under FN:FP=5:1 "
    "(results/decision/tables/experiment_g_review_cost_perturbation.csv). "
    "Stage 9 cites this. Do not promote G's t_low/t_high into Stage 8."
)


def _row(frame: pd.DataFrame, architecture: str) -> dict[str, Any]:
    hits = frame.loc[frame["architecture"].astype(str) == architecture]
    if len(hits) != 1:
        raise RuntimeError(f"Expected one row for architecture={architecture!r}, got {len(hits)}.")
    return hits.iloc[0].to_dict()


def load_frozen_confusion() -> dict[str, dict[str, Any]]:
    """Load stored Stage 8 v2 TEST confusion counts. Does not re-apply a policy."""
    table3 = pd.read_csv(V2_TABLE3)
    out: dict[str, dict[str, Any]] = {}
    for system, architecture in ARCHITECTURE_ROWS.items():
        row = _row(table3, architecture)
        n = int(row["n"])
        n_pos = int(row["n_positive"])
        n_neg = int(row["n_negative"])
        tp = int(row["tp"])
        tn = int(row["tn"])
        fp = int(row["fp"])
        fn = int(row["fn"])
        n_approve = int(row["n_approve"])
        n_review = int(row["n_review"])
        n_reject = int(row["n_reject"])
        if n_approve + n_review + n_reject != n:
            raise RuntimeError(f"{system} decision counts do not sum to n.")
        if tp + tn + fp + fn + n_review != n:
            raise RuntimeError(f"{system} confusion + review does not sum to n.")
        out[system] = {
            "system": system,
            "architecture": architecture,
            "n": n,
            "n_positive": n_pos,
            "n_negative": n_neg,
            "tp": tp,
            "tn": tn,
            "fp": fp,
            "fn": fn,
            "n_approve": n_approve,
            "n_review": n_review,
            "n_reject": n_reject,
            "approval_rate": float(row["approval_rate"]),
            "review_rate": float(row["review_rate"]),
            "rejection_rate": float(row["rejection_rate"]),
            "fpr_auto": float(row["fpr_auto"]),
            "fnr_auto": float(row["fnr_auto"]),
            "fpr_population": float(row["fpr_population"]),
            "fnr_population": float(row["fnr_population"]),
            "stored_expected_normalized_cost_fnfp5": float(row["expected_normalized_cost"]),
            "c_review_over_fp": REVIEW_COST_BY_SYSTEM[system],
        }
    if out["A1"]["n_approve"] != EXPECTED_A1["APPROVE"]:
        raise RuntimeError("A1 APPROVE drifted from Stage 8 v2.")
    if out["A1"]["n_review"] != EXPECTED_A1["HUMAN_REVIEW"]:
        raise RuntimeError("A1 HUMAN_REVIEW drifted from Stage 8 v2.")
    if out["A1"]["n_reject"] != EXPECTED_A1["REJECT"]:
        raise RuntimeError("A1 REJECT drifted from Stage 8 v2.")
    if out["A3_A4"]["n_review"] != 0:
        raise RuntimeError("A3/A4 stored HUMAN_REVIEW is not zero.")
    return out


def score_confusion(counts: dict[str, Any], fn_fp_ratio: int) -> dict[str, Any]:
    """Score a frozen confusion matrix under one assumed FN:FP ratio. Decisions are not changed."""
    scenario = CostScenario(
        fn_fp_ratio=float(fn_fp_ratio),
        c_fp=C_FP,
        c_review_over_fp=float(counts["c_review_over_fp"]),
    )
    total = expected_cost(int(counts["fn"]), int(counts["fp"]), int(counts["n_review"]), scenario)
    normalized = expected_normalized_cost(
        int(counts["fn"]), int(counts["fp"]), int(counts["n_review"]), int(counts["n"]), scenario
    )
    fn_fp_only = float(scenario.c_fn * int(counts["fn"]) + scenario.c_fp * int(counts["fp"]))
    review_only = float(scenario.c_review * int(counts["n_review"]))
    return {
        "ratio_label": scenario.name,
        "fn_fp_ratio": int(fn_fp_ratio),
        "c_fp": float(scenario.c_fp),
        "c_fn": float(scenario.c_fn),
        "c_review": float(scenario.c_review),
        "c_review_over_fp": float(scenario.c_review_over_fp),
        "tp": int(counts["tp"]),
        "tn": int(counts["tn"]),
        "fp": int(counts["fp"]),
        "fn": int(counts["fn"]),
        "n": int(counts["n"]),
        "n_approve": int(counts["n_approve"]),
        "n_review": int(counts["n_review"]),
        "n_reject": int(counts["n_reject"]),
        "fpr_population": float(counts["fpr_population"]),
        "fnr_population": float(counts["fnr_population"]),
        "fpr_auto": float(counts["fpr_auto"]),
        "fnr_auto": float(counts["fnr_auto"]),
        "cost_fn_fp_only": fn_fp_only,
        "cost_review_only": review_only,
        "cost_total": total,
        "cost_normalized": normalized,
        "formula": "Cost_total = C_FN*FN + C_FP*FP + C_REVIEW*n_review; Cost_normalized = Cost_total / n",
        "assumption": "Researcher sensitivity scenario, not a real operational cost.",
    }


def assemble_cost_sensitivity() -> dict[str, Any]:
    integrity = verify_frozen_artifacts()
    if integrity["t_low"] != EXPECTED_T_LOW or integrity["t_high"] != EXPECTED_T_HIGH:
        raise RuntimeError("Stage 8 thresholds are not 0.06/0.69.")
    if integrity["t_star"] != EXPECTED_T_STAR:
        raise RuntimeError("Frozen monolithic t* is not 0.16.")
    if FN_FP_RATIOS != (1, 2, 5, 10):
        raise RuntimeError("FN:FP ratio set is not the frozen {1,2,5,10}.")
    confusion = load_frozen_confusion()
    rows: list[dict[str, Any]] = []
    by_system: dict[str, list[dict[str, Any]]] = {}
    for system, counts in confusion.items():
        fingerprints = []
        scored = []
        for ratio in FN_FP_RATIOS:
            item = score_confusion(counts, ratio)
            scored.append(item)
            fingerprints.append(
                (item["tp"], item["tn"], item["fp"], item["fn"], item["n_approve"], item["n_review"], item["n_reject"])
            )
            rows.append({"system": system, **item})
        if len(set(fingerprints)) != 1:
            raise RuntimeError(f"{system} decisions changed across cost ratios.")
        primary = next(item for item in scored if item["fn_fp_ratio"] == PRIMARY_RATIO)
        stored = float(counts["stored_expected_normalized_cost_fnfp5"])
        if abs(primary["cost_normalized"] - stored) > 1e-12:
            raise RuntimeError(
                f"{system} recomputed FN:FP=5:1 cost {primary['cost_normalized']} != stored {stored}."
            )
        by_system[system] = scored
    a1_costs = [item["cost_normalized"] for item in by_system["A1"]]
    a1_cost_invariant = max(a1_costs) - min(a1_costs) < 1e-15
    return {
        "experiment_id": EXPERIMENT_ID,
        "integrity": integrity,
        "confusion": confusion,
        "rows": rows,
        "by_system": by_system,
        "fn_fp_ratios": list(FN_FP_RATIOS),
        "ratio_labels": list(RATIO_LABELS),
        "a3_identical_to_a4": True,
        "a1_human_review_retained": confusion["A1"]["n_review"] > 0,
        "a1_cost_invariant_to_fn_fp_ratio": a1_cost_invariant,
        "decisions_unchanged_across_ratios": True,
        "used_for_selection": False,
        "models_loaded": False,
        "models_trained": False,
        "calibration_refit": False,
        "formula": "Cost_total = C_FN * FN + C_FP * FP + C_REVIEW * n_review; Cost_normalized = Cost_total / n; C_FP = 1",
    }


def cite_experiment_g() -> dict[str, Any]:
    """Cite the frozen Stage 8 Experiment G table. Do not re-select thresholds."""
    if not EXPERIMENT_G_CSV.exists():
        raise FileNotFoundError(f"Missing Experiment G artifact: {EXPERIMENT_G_CSV}")
    frame = pd.read_csv(EXPERIMENT_G_CSV)
    required_c = {0.10, 0.25, 0.50}
    observed = {round(float(v), 2) for v in frame["c_review_over_fp"].tolist()}
    if observed != required_c:
        raise RuntimeError(f"Experiment G c_review_over_fp set {observed} != {required_c}.")
    rows = []
    for rec in frame.to_dict(orient="records"):
        rows.append(
            {
                "c_review_over_fp": float(rec["c_review_over_fp"]),
                "t_low": float(rec["t_low"]),
                "t_high": float(rec["t_high"]),
                "policy_type": str(rec["policy_type"]),
                "expected_normalized_cost": float(rec["expected_normalized_cost"]),
                "approval_rate": float(rec["approval_rate"]),
                "review_rate": float(rec["review_rate"]),
                "rejection_rate": float(rec["rejection_rate"]),
                "scenario": str(rec["scenario"]),
                "split": "validation",
            }
        )
    return {
        "status": EXPERIMENT_G_STATUS,
        "executed_in_stage9_2": False,
        "cited_existing_artifact": True,
        "constraint_conflict_lc_test_selection": False,
        "definition": EXPERIMENT_G_DEFINITION,
        "reason": (
            "Stage 9.0 freeze instructs Stage 9 to cite the existing validation Experiment G table "
            "and not rerun it, and not to promote G's t_low/t_high into Stage 8. Re-running G would "
            "re-select thresholds (new APPROVE/REVIEW/REJECT maps). Stage 9.2 primary analysis keeps "
            "frozen decisions fixed. LC TEST was not used for G."
        ),
        "artifact": EXPERIMENT_G_CSV.as_posix(),
        "sha256": sha256_file(EXPERIMENT_G_CSV),
        "rows": rows,
    }


def cite_validation_table2() -> dict[str, Any]:
    if not TABLE2_VAL.exists():
        raise FileNotFoundError(f"Missing validation cost-selection table: {TABLE2_VAL}")
    frame = pd.read_csv(TABLE2_VAL)
    labels = [str(v) for v in frame["cost_scenario"].tolist()]
    if labels != list(RATIO_LABELS):
        raise RuntimeError(f"Validation table2 scenarios {labels} != {list(RATIO_LABELS)}.")
    rows = []
    for rec in frame.to_dict(orient="records"):
        rows.append(
            {
                "cost_scenario": str(rec["cost_scenario"]),
                "t_low": float(rec["t_low"]),
                "t_high": float(rec["t_high"]),
                "single_t": float(rec["single_t"]),
                "expected_normalized_cost": float(rec["expected_normalized_cost"]),
                "single_cost": float(rec["single_cost"]),
                "approval_rate": float(rec["approval_rate"]),
                "review_rate": float(rec["review_rate"]),
                "rejection_rate": float(rec["rejection_rate"]),
                "split": "validation",
                "note": "Already-executed Stage 8 validation threshold identification. Not repeated. Not TEST selection.",
            }
        )
    return {
        "status": "CITED_EXISTING_VALIDATION_ARTIFACT",
        "executed_in_stage9_2": False,
        "artifact": TABLE2_VAL.as_posix(),
        "sha256": sha256_file(TABLE2_VAL),
        "rows": rows,
    }


def stage91_guard_paths() -> list[Path]:
    return [STAGE91_SUMMARY, STAGE91_REPORT, STAGE91_AUDIT, STAGE91_TABLE1]


def stage8_guard_paths() -> list[Path]:
    return [
        V1_FREEZE,
        ROOT / "results" / "decision" / "v2" / "frozen_policy.json",
        V2_TABLE3,
        ROOT / "results" / "decision" / "v2" / "metrics" / "fused_test.json",
        ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md",
        ROOT / "audit" / "stage8_v2_decision_fusion_run.json",
        TABLE2_VAL,
        EXPERIMENT_G_CSV,
    ]
