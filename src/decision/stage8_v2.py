"""Stage 8 v2 per-row governance fusion. No Shariah score. Thresholds are frozen."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from decision.decision_engine import fuse_decision
from decision.policy_matrix import build_matrix
from shariah.engine import AMENDMENT_ID, L1L2_VERSION
from shariah.l1 import L1_LC_STATUS, assess_dataset_readiness
from shariah.l2 import (
    EVALUATION_MODE_PER_APPLICATION,
    evaluate_application_governance,
    extract_application_governance_evidence,
)
from shariah.schema import FIREWALL_FIELDS

ROOT = Path(__file__).resolve().parents[2]
V1_FREEZE_PATH = ROOT / "results" / "decision" / "frozen_policy.json"
PLATT_RECORD = ROOT / "results" / "calibration" / "artifacts" / "platt_record.json"
EXPECTED_T_LOW = 0.06
EXPECTED_T_HIGH = 0.69
EXPECTED_PLATT_A = 1.1988263209549705
EXPECTED_PLATT_B = 0.6697765046966161
FROZEN_DATASET_ID = "lendingclub_granting_v0.1"
FIXED_GOV_TS = "2026-09-15T00:00:00+00:00"


def load_frozen_thresholds(path: Path | None = None) -> dict[str, Any]:
    freeze = json.loads((path or V1_FREEZE_PATH).read_text(encoding="utf-8"))
    t_low = float(freeze["t_low"])
    t_high = float(freeze["t_high"])
    if t_low != EXPECTED_T_LOW or t_high != EXPECTED_T_HIGH:
        raise RuntimeError(f"Frozen thresholds changed: t_low={t_low} t_high={t_high}")
    if freeze.get("selection_split") != "validation":
        raise RuntimeError("Frozen policy is not validation-selected.")
    return freeze


def assert_platt_integrity() -> dict[str, Any]:
    freeze = load_frozen_thresholds()
    platt = json.loads(PLATT_RECORD.read_text(encoding="utf-8"))
    if float(platt["a"]) != EXPECTED_PLATT_A or float(platt["b"]) != EXPECTED_PLATT_B:
        raise RuntimeError("Platt artifact parameters do not match the frozen Stage 8 values.")
    frozen_platt = freeze["platt"]
    if float(frozen_platt["a"]) != float(platt["a"]) or float(frozen_platt["b"]) != float(platt["b"]):
        raise RuntimeError("frozen_policy.json Platt parameters disagree with platt_record.json.")
    return platt


def matrix_from_config(config: Mapping[str, Any]) -> dict[tuple[str, str], str]:
    return build_matrix(list(config["governance_policy"]["matrix"]))


def compact_governance(full: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "overall_governance_status": full["overall_governance_status"],
        "layer_a": full["layer_a_completeness"]["layer_a"],
        "missing_evidence": list(full["missing_evidence"]),
        "triggered_rule_ids": list(full["triggered_rule_ids"]),
        "source_ids": list(full["source_ids"]),
        "expert_validation_states": list(full["expert_validation_states"]),
        "any_expert_validated": bool(full["any_expert_validated"]),
        "certification_claim": bool(full["certification_claim"]),
    }


def evaluate_row_for_fusion(
    row: Mapping[str, Any],
    *,
    dataset_id: str = FROZEN_DATASET_ID,
    l1_result: Mapping[str, Any] | None = None,
    timestamp: str = FIXED_GOV_TS,
    compact_cache: dict[str, dict[str, Any]] | None = None,
    synthetic: bool = False,
) -> dict[str, Any]:
    """Stage 7 v2 L2 extract/evaluate for one application. Cache stores compact fields only."""
    l1 = dict(l1_result) if l1_result is not None else assess_dataset_readiness(dataset_id)
    evidence, meta = extract_application_governance_evidence(row, dataset_id=dataset_id, synthetic=synthetic)
    leaked = [name for name in FIREWALL_FIELDS if name in evidence.as_dict()]
    if leaked:
        raise RuntimeError(f"Firewall leak into Shariah evidence: {leaked}")
    if evidence.contract_type != "unknown":
        raise RuntimeError("LendingClub L2 inferred a contract type.")
    key = meta["evidence_hash"]
    cache = compact_cache if compact_cache is not None else {}
    if key not in cache:
        full = evaluate_application_governance(
            evidence,
            l2_meta=meta,
            l1_result=l1,
            timestamp=timestamp,
        )
        cache[key] = compact_governance(full)
    compact = cache[key]
    if compact["certification_claim"] or compact["any_expert_validated"]:
        raise RuntimeError("Governance result claimed certification or expert validation.")
    return {
        **compact,
        "dataset_id": dataset_id,
        "record_reference_hash": meta["record_reference_hash"],
        "evidence_hash": meta["evidence_hash"],
        "evaluation_mode": EVALUATION_MODE_PER_APPLICATION,
        "l1_status": l1["readiness_status"],
        "l1_is_applicant_level_ruling": False,
        "expert_validation_state": (
            "NONE_EXPERT_VALIDATED"
            if not compact["any_expert_validated"]
            else "|".join(compact["expert_validation_states"])
        ),
        "amendment_id": AMENDMENT_ID,
        "l1l2_version": L1L2_VERSION,
        "firewall_fields_dropped": list(meta.get("firewall_fields_dropped", [])),
        "purpose_used_as_contract_type": bool(meta.get("purpose_used_as_contract_type")),
    }


def fuse_with_frozen_policy(
    p_calibrated: float,
    governance: Mapping[str, Any],
    *,
    t_low: float,
    t_high: float,
    matrix: dict[tuple[str, str], str],
    unknown_as: str = "INSUFFICIENT_INFORMATION",
) -> dict[str, Any]:
    fused = fuse_decision(
        p_calibrated,
        governance["overall_governance_status"],
        t_low,
        t_high,
        matrix,
        unknown_as,
    )
    return {
        **fused,
        "evaluation_mode": governance["evaluation_mode"],
        "record_reference_hash": governance["record_reference_hash"],
        "evidence_hash": governance["evidence_hash"],
        "l1_status": governance["l1_status"],
        "l1_is_applicant_level_ruling": False,
        "missing_evidence": list(governance["missing_evidence"]),
        "shariah_evidence_completeness": governance["layer_a"],
        "certification_claim": False,
    }


def review_cause(credit_band: str, governance_status: str, final_decision: str) -> str | None:
    if final_decision != "HUMAN_REVIEW":
        return None
    gov_insuf = governance_status == "INSUFFICIENT_INFORMATION"
    gov_review = governance_status == "REVIEW"
    credit_unc = credit_band == "MEDIUM"
    if gov_insuf and credit_unc:
        return "governance_insufficiency_and_credit_uncertainty"
    if gov_insuf:
        return "governance_insufficiency"
    if gov_review and credit_unc:
        return "governance_review_and_credit_uncertainty"
    if gov_review:
        return "governance_review"
    if credit_unc:
        return "credit_uncertainty"
    return "other_review"


def assert_l1_not_confused_with_l2(governance: Mapping[str, Any]) -> None:
    if governance["l1_status"] != L1_LC_STATUS:
        raise RuntimeError("Unexpected LendingClub L1 status.")
    if governance["l1_status"] == governance["overall_governance_status"]:
        raise RuntimeError("L1 dataset status was stored as the L2 governance status.")
    if governance["evaluation_mode"] != EVALUATION_MODE_PER_APPLICATION:
        raise RuntimeError("L2 evaluation_mode is not PER_APPLICATION.")
    if governance["l1_is_applicant_level_ruling"]:
        raise RuntimeError("L1 was marked as an applicant-level ruling.")
