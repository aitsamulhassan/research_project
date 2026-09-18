"""Stage 9.3 governance sensitivity. Hypothetical G1/G3; G0 remains the observed primary. No retraining."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from decision.policy_matrix import CREDIT_BANDS, DECISIONS, GOVERNANCE_STATUSES, build_matrix, lookup
from decision.stage9_1 import (
    EXPECTED_A1,
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_V1_FREEZE_SHA256,
    V1_FREEZE,
    V2_AUDIT,
    verify_frozen_artifacts,
)

ROOT = Path(__file__).resolve().parents[2]

EXPERIMENT_ID = "stage9_3_governance_sensitivity_lc_v1"
PROTOCOL_ID = "STAGE-9-PROTOCOL-2026-09-15"
PROTOCOL_SECTION = "5.2"
STAGE7_L1L2_VERSION = "stage7-l1l2-v2"
OBSERVED_L2 = "INSUFFICIENT_INFORMATION"
EXPERT_VALIDATION = "NONE_EXPERT_VALIDATED"
CERTIFICATION_CLAIM = False

# Frozen Stage 8 G0 matrix (configs/stage8_decision_policy.yaml). Not modified.
G0_MATRIX_ROWS = [
    {"governance": "NOT_STRUCTURABLE_WITHOUT_REDESIGN", "credit_band": "LOW", "decision": "REJECT"},
    {"governance": "NOT_STRUCTURABLE_WITHOUT_REDESIGN", "credit_band": "MEDIUM", "decision": "REJECT"},
    {"governance": "NOT_STRUCTURABLE_WITHOUT_REDESIGN", "credit_band": "HIGH", "decision": "REJECT"},
    {"governance": "INSUFFICIENT_INFORMATION", "credit_band": "LOW", "decision": "HUMAN_REVIEW"},
    {"governance": "INSUFFICIENT_INFORMATION", "credit_band": "MEDIUM", "decision": "HUMAN_REVIEW"},
    {"governance": "INSUFFICIENT_INFORMATION", "credit_band": "HIGH", "decision": "REJECT"},
    {"governance": "REVIEW", "credit_band": "LOW", "decision": "HUMAN_REVIEW"},
    {"governance": "REVIEW", "credit_band": "MEDIUM", "decision": "HUMAN_REVIEW"},
    {"governance": "REVIEW", "credit_band": "HIGH", "decision": "REJECT"},
    {"governance": "PASS", "credit_band": "LOW", "decision": "APPROVE"},
    {"governance": "PASS", "credit_band": "MEDIUM", "decision": "HUMAN_REVIEW"},
    {"governance": "PASS", "credit_band": "HIGH", "decision": "REJECT"},
]

G1_INSUFFICIENT_TREATMENT = {"LOW": "REJECT", "MEDIUM": "REJECT", "HIGH": "REJECT"}
G3_INSUFFICIENT_TREATMENT = {"LOW": "HUMAN_REVIEW", "MEDIUM": "HUMAN_REVIEW", "HIGH": "HUMAN_REVIEW"}
G0_INSUFFICIENT_TREATMENT = {"LOW": "HUMAN_REVIEW", "MEDIUM": "HUMAN_REVIEW", "HIGH": "REJECT"}

G1_DEFINITION = (
    "Conservative REJECT: treatment of INSUFFICIENT_INFORMATION maps all credit bands "
    "(LOW, MEDIUM, HIGH) to REJECT. Hypothetical engineering scenario. Protocol §5.2."
)
G3_DEFINITION = (
    "Governance-gated REVIEW: treatment of INSUFFICIENT_INFORMATION maps all credit bands "
    "(LOW, MEDIUM, HIGH) to HUMAN_REVIEW, including HIGH. Hypothetical engineering scenario. Protocol §5.2."
)
G0_DEFINITION = (
    "Frozen Stage 8 matrix treatment of INSUFFICIENT_INFORMATION: LOW/MEDIUM → HUMAN_REVIEW; "
    "HIGH → REJECT. Primary observed LendingClub evidence state."
)

G_UNSAFE_STATUS = "NOT_EXECUTED — NOT_AUTHORIZED"
STAGE7_AUDIT = ROOT / "audit" / "stage7_v2_governance_run.json"
STAGE8_V2_CONFIG = ROOT / "configs" / "stage8_v2_decision_policy.yaml"
STAGE8_MATRIX_CONFIG = ROOT / "configs" / "stage8_decision_policy.yaml"


def g0_matrix() -> dict[tuple[str, str], str]:
    return build_matrix(G0_MATRIX_ROWS)


def _replace_insufficient_row(treatment: dict[str, str]) -> dict[tuple[str, str], str]:
    rows = []
    for row in G0_MATRIX_ROWS:
        if row["governance"] == "INSUFFICIENT_INFORMATION":
            rows.append(
                {
                    "governance": "INSUFFICIENT_INFORMATION",
                    "credit_band": row["credit_band"],
                    "decision": treatment[row["credit_band"]],
                }
            )
        else:
            rows.append(dict(row))
    return build_matrix(rows)


def g1_matrix() -> dict[tuple[str, str], str]:
    return _replace_insufficient_row(G1_INSUFFICIENT_TREATMENT)


def g3_matrix() -> dict[tuple[str, str], str]:
    return _replace_insufficient_row(G3_INSUFFICIENT_TREATMENT)


def fuse_status_band(scenario: str, governance_status: str, credit_band: str) -> str:
    """Decision-layer lookup only. Does not evaluate Shariah rules or load a credit model."""
    matrices = {"G0": g0_matrix(), "G1": g1_matrix(), "G3": g3_matrix()}
    if scenario not in matrices:
        raise ValueError(f"Unauthorized scenario: {scenario}")
    return lookup(matrices[scenario], governance_status, credit_band)


def _rate(count: int, n: int) -> float:
    return float(count / n) if n else float("nan")


def allocate_from_band_counts(
    band_counts: dict[str, int],
    governance_status: str,
    scenario: str,
) -> dict[str, Any]:
    n = int(sum(band_counts.values()))
    counts = {d: 0 for d in DECISIONS}
    by_band: dict[str, dict[str, Any]] = {}
    for band in CREDIT_BANDS:
        n_band = int(band_counts[band])
        decision = fuse_status_band(scenario, governance_status, band)
        counts[decision] += n_band
        by_band[band] = {"n": n_band, "decision": decision}
    if sum(counts.values()) != n:
        raise RuntimeError("Allocated counts do not sum to n.")
    return {
        "scenario": scenario,
        "governance_status_input": governance_status,
        "n": n,
        "APPROVE": counts["APPROVE"],
        "HUMAN_REVIEW": counts["HUMAN_REVIEW"],
        "REJECT": counts["REJECT"],
        "approval_rate": _rate(counts["APPROVE"], n),
        "review_rate": _rate(counts["HUMAN_REVIEW"], n),
        "rejection_rate": _rate(counts["REJECT"], n),
        "by_band": by_band,
    }


def load_published_stage8_v2_counts() -> dict[str, Any]:
    audit = json.loads(V2_AUDIT.read_text(encoding="utf-8"))
    band_counts = {k: int(v) for k, v in audit["band_counts"].items()}
    gov_counts = {k: int(v) for k, v in audit["gov_counts"].items()}
    fused = {k: int(v) for k, v in audit["fused_counts"].items()}
    n = int(audit["n_test"])
    if gov_counts != {OBSERVED_L2: n}:
        raise RuntimeError(f"Published L2 distribution is not all {OBSERVED_L2}: {gov_counts}")
    if sum(band_counts.values()) != n:
        raise RuntimeError("Published credit-band counts do not sum to n_test.")
    if fused != EXPECTED_A1:
        raise RuntimeError(f"Published G0 fused counts {fused} != Stage 8 v2 {EXPECTED_A1}.")
    return {
        "n": n,
        "band_counts": band_counts,
        "gov_counts": gov_counts,
        "g0_fused_stored": fused,
        "l1_status": audit["l1_status"],
        "l2_evaluation_mode": audit["l2_evaluation_mode"],
        "any_expert_validated": bool(audit["any_expert_validated"]),
        "certification_claim_policy": bool(audit["certification_claim_policy"]),
        "stage7_v2": audit.get("stage7_v2"),
        "t_low": float(audit["t_low"]),
        "t_high": float(audit["t_high"]),
    }


def assemble_governance_sensitivity() -> dict[str, Any]:
    integrity = verify_frozen_artifacts()
    if integrity["t_low"] != EXPECTED_T_LOW or integrity["t_high"] != EXPECTED_T_HIGH:
        raise RuntimeError("Stage 8 thresholds are not 0.06/0.69.")
    if integrity["v1_freeze_sha256"] != EXPECTED_V1_FREEZE_SHA256:
        raise RuntimeError("Stage 8 freeze hash mismatch.")
    published = load_published_stage8_v2_counts()
    g0 = allocate_from_band_counts(published["band_counts"], OBSERVED_L2, "G0")
    if {k: g0[k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")} != published["g0_fused_stored"]:
        raise RuntimeError("G0 algebra from published bands does not match stored Stage 8 v2 fused counts.")
    g1 = allocate_from_band_counts(published["band_counts"], OBSERVED_L2, "G1")
    g3 = allocate_from_band_counts(published["band_counts"], OBSERVED_L2, "G3")
    g0["label"] = "Frozen Stage 8 matrix (primary / observed)"
    g1["label"] = "Conservative REJECT"
    g3["label"] = "Governance-gated REVIEW"
    g0["role"] = "observed_data_supported"
    g1["role"] = "hypothetical_engineering_scenario"
    g3["role"] = "hypothetical_engineering_scenario"
    g0["definition"] = G0_DEFINITION
    g1["definition"] = G1_DEFINITION
    g3["definition"] = G3_DEFINITION
    g0["source"] = "stored Stage 8 v2 fused counts; algebra from published band counts confirms"
    g1["source"] = "derived commentary from published Stage 8 v2 band counts; not a new TEST evaluation"
    g3["source"] = "derived commentary from published Stage 8 v2 band counts; not a new TEST evaluation"
    if g1["REJECT"] != published["n"] or g1["HUMAN_REVIEW"] != 0 or g1["APPROVE"] != 0:
        raise RuntimeError("G1 on all-INSUFFICIENT_INFORMATION must be 100% REJECT.")
    if g3["HUMAN_REVIEW"] != published["n"] or g3["REJECT"] != 0 or g3["APPROVE"] != 0:
        raise RuntimeError("G3 on all-INSUFFICIENT_INFORMATION must be 100% HUMAN_REVIEW.")
    other_statuses_unchanged = True
    for status in GOVERNANCE_STATUSES:
        if status == OBSERVED_L2:
            continue
        for band in CREDIT_BANDS:
            g0_d = fuse_status_band("G0", status, band)
            if fuse_status_band("G1", status, band) != g0_d or fuse_status_band("G3", status, band) != g0_d:
                other_statuses_unchanged = False
    return {
        "experiment_id": EXPERIMENT_ID,
        "integrity": integrity,
        "published": published,
        "scenarios": {"G0": g0, "G1": g1, "G3": g3},
        "observed_l2": OBSERVED_L2,
        "g_unsafe_status": G_UNSAFE_STATUS,
        "g_unsafe_executed": False,
        "other_governance_statuses_unchanged": other_statuses_unchanged,
        "credit_bands_unchanged": True,
        "thresholds_unchanged": True,
        "used_for_selection": False,
        "models_loaded": False,
        "models_trained": False,
        "calibration_refit": False,
        "new_shariah_rules_added": False,
        "expert_validation": EXPERT_VALIDATION,
        "certification_claim": CERTIFICATION_CLAIM,
        "any_expert_validated": published["any_expert_validated"],
        "analysis_label": "derived_commentary_from_published_stage8_v2_band_counts",
    }


def stage8_guard_paths() -> list[Path]:
    return [
        V1_FREEZE,
        ROOT / "results" / "decision" / "v2" / "frozen_policy.json",
        ROOT / "results" / "decision" / "v2" / "tables" / "table3_test_decision_outcomes.csv",
        ROOT / "results" / "decision" / "v2" / "metrics" / "fused_test.json",
        ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md",
        V2_AUDIT,
        STAGE8_MATRIX_CONFIG,
        STAGE8_V2_CONFIG,
        STAGE7_AUDIT,
        ROOT / "docs" / "STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md",
    ]


def stage91_guard_paths() -> list[Path]:
    return [
        ROOT / "results" / "ablation" / "v1" / "metrics" / "ablation_summary.json",
        ROOT / "docs" / "STAGE_9_1_ABLATION_REPORT.md",
        ROOT / "audit" / "stage9_1_ablation_run.json",
    ]


def stage92_guard_paths() -> list[Path]:
    return [
        ROOT / "results" / "cost_sensitivity" / "v1" / "metrics" / "cost_sensitivity_summary.json",
        ROOT / "docs" / "STAGE_9_2_COST_SENSITIVITY_REPORT.md",
        ROOT / "audit" / "stage9_2_cost_sensitivity_run.json",
    ]
