"""Deterministic audit records. Timestamps never affect decisions."""

from __future__ import annotations

import hashlib
import json
from typing import Any

AUDIT_SCHEMA_VERSION = "1.0"
POLICY_VERSION = "stage8-v1"

REQUIRED_FIELDS = (
    "audit_schema_version",
    "decision_id",
    "event_timestamp",
    "dataset_id",
    "dataset_hash",
    "record_reference_hash",
    "model_name",
    "model_version",
    "preprocessor_version",
    "calibrator_name",
    "calibrator_version",
    "raw_probability",
    "calibrated_probability",
    "credit_risk_band",
    "top_explanation_features",
    "shariah_evidence_completeness",
    "shariah_governance_status",
    "triggered_rule_ids",
    "rule_source_ids",
    "policy_version",
    "cost_scenario",
    "threshold_configuration",
    "final_decision",
    "review_required",
)

LOGIC_FIELDS = tuple(f for f in REQUIRED_FIELDS if f not in {"decision_id", "event_timestamp"})

FORBIDDEN_PUBLISHED_KEYS = {
    "id",
    "loan_id",
    "addr_state",
    "zip_code",
    "title",
    "desc",
    "issue_d",
    "address",
    "raw_id",
    "applicant_id",
}


def canonical_dumps(payload: dict[str, Any]) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def logic_payload(record: dict[str, Any]) -> dict[str, Any]:
    missing = [f for f in LOGIC_FIELDS if f not in record]
    if missing:
        raise ValueError(f"Audit record missing logic fields: {missing}")
    return {k: record[k] for k in LOGIC_FIELDS}


def logic_hash(record: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_dumps(logic_payload(record)).encode("utf-8")).hexdigest()


def assert_no_raw_identifiers(record: dict[str, Any]) -> None:
    leaked = sorted(k for k in record if k in FORBIDDEN_PUBLISHED_KEYS)
    if leaked:
        raise ValueError(f"Audit record contains forbidden identifier fields: {leaked}")


def build_record(
    *,
    event_timestamp: str,
    dataset_id: str,
    dataset_hash: str,
    record_reference_hash: str,
    model_name: str,
    model_version: str,
    preprocessor_version: str,
    calibrator_name: str,
    calibrator_version: str,
    raw_probability: float,
    calibrated_probability: float,
    credit_risk_band: str,
    top_explanation_features: list[str],
    shariah_evidence_completeness: str,
    shariah_governance_status: str,
    triggered_rule_ids: list[str],
    rule_source_ids: list[str],
    policy_version: str,
    cost_scenario: str,
    threshold_configuration: dict[str, Any],
    final_decision: str,
    review_required: bool,
    audit_schema_version: str = AUDIT_SCHEMA_VERSION,
) -> dict[str, Any]:
    record = {
        "audit_schema_version": audit_schema_version,
        "event_timestamp": event_timestamp,
        "dataset_id": dataset_id,
        "dataset_hash": dataset_hash,
        "record_reference_hash": record_reference_hash,
        "model_name": model_name,
        "model_version": model_version,
        "preprocessor_version": preprocessor_version,
        "calibrator_name": calibrator_name,
        "calibrator_version": calibrator_version,
        "raw_probability": float(raw_probability),
        "calibrated_probability": float(calibrated_probability),
        "credit_risk_band": credit_risk_band,
        "top_explanation_features": list(top_explanation_features),
        "shariah_evidence_completeness": shariah_evidence_completeness,
        "shariah_governance_status": shariah_governance_status,
        "triggered_rule_ids": list(triggered_rule_ids),
        "rule_source_ids": list(rule_source_ids),
        "policy_version": policy_version,
        "cost_scenario": cost_scenario,
        "threshold_configuration": dict(threshold_configuration),
        "final_decision": final_decision,
        "review_required": bool(review_required),
    }
    record["decision_id"] = logic_hash(record)
    assert_no_raw_identifiers(record)
    missing = [f for f in REQUIRED_FIELDS if f not in record]
    if missing:
        raise ValueError(f"Audit record missing required fields: {missing}")
    return record


def schema_document() -> dict[str, Any]:
    return {
        "audit_schema_version": AUDIT_SCHEMA_VERSION,
        "policy_version": POLICY_VERSION,
        "required_fields": list(REQUIRED_FIELDS),
        "logic_fields": list(LOGIC_FIELDS),
        "timestamp_policy": (
            "event_timestamp records when the audit object was written. It is excluded from "
            "decision_id / logic_hash and never enters the decision engine."
        ),
        "identifier_policy": (
            "Published records store record_reference_hash = sha256('lc-row|{id}')[:16]. "
            "Raw id, address, zip, and free text are forbidden."
        ),
        "explainability_policy": (
            "top_explanation_features are the frozen Stage 6 global |SHAP| ranking attached as "
            "evidence. They are not an independent approval criterion."
        ),
        "forbidden_published_keys": sorted(FORBIDDEN_PUBLISHED_KEYS),
    }


POLICY_VERSION_V2 = "stage8-v2"
AUDIT_SCHEMA_VERSION_V2 = "2.0"

REQUIRED_FIELDS_V2 = REQUIRED_FIELDS + (
    "evidence_hash",
    "evaluation_mode",
    "l1_status",
    "l1_is_applicant_level_ruling",
    "missing_evidence",
    "expert_validation_state",
    "amendment_id",
    "l1l2_version",
    "certification_claim",
)

LOGIC_FIELDS_V2 = tuple(f for f in REQUIRED_FIELDS_V2 if f not in {"decision_id", "event_timestamp"})


def logic_payload_v2(record: dict[str, Any]) -> dict[str, Any]:
    missing = [f for f in LOGIC_FIELDS_V2 if f not in record]
    if missing:
        raise ValueError(f"Audit v2 record missing logic fields: {missing}")
    return {k: record[k] for k in LOGIC_FIELDS_V2}


def logic_hash_v2(record: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_dumps(logic_payload_v2(record)).encode("utf-8")).hexdigest()


def build_record_v2(
    *,
    event_timestamp: str,
    dataset_id: str,
    dataset_hash: str,
    record_reference_hash: str,
    evidence_hash: str,
    evaluation_mode: str,
    l1_status: str,
    l1_is_applicant_level_ruling: bool,
    missing_evidence: list[str],
    expert_validation_state: str,
    amendment_id: str,
    l1l2_version: str,
    certification_claim: bool,
    model_name: str,
    model_version: str,
    preprocessor_version: str,
    calibrator_name: str,
    calibrator_version: str,
    raw_probability: float,
    calibrated_probability: float,
    credit_risk_band: str,
    top_explanation_features: list[str],
    shariah_evidence_completeness: str,
    shariah_governance_status: str,
    triggered_rule_ids: list[str],
    rule_source_ids: list[str],
    policy_version: str,
    cost_scenario: str,
    threshold_configuration: dict[str, Any],
    final_decision: str,
    review_required: bool,
    audit_schema_version: str = AUDIT_SCHEMA_VERSION_V2,
) -> dict[str, Any]:
    if evaluation_mode != "PER_APPLICATION":
        raise ValueError("Stage 8 v2 audit records must use evaluation_mode=PER_APPLICATION.")
    if l1_is_applicant_level_ruling:
        raise ValueError("L1 status must not be recorded as an applicant-level ruling.")
    if certification_claim:
        raise ValueError("Audit records must not claim Shariah certification.")
    record = {
        "audit_schema_version": audit_schema_version,
        "event_timestamp": event_timestamp,
        "dataset_id": dataset_id,
        "dataset_hash": dataset_hash,
        "record_reference_hash": record_reference_hash,
        "evidence_hash": evidence_hash,
        "evaluation_mode": evaluation_mode,
        "l1_status": l1_status,
        "l1_is_applicant_level_ruling": False,
        "missing_evidence": list(missing_evidence),
        "expert_validation_state": expert_validation_state,
        "amendment_id": amendment_id,
        "l1l2_version": l1l2_version,
        "certification_claim": False,
        "model_name": model_name,
        "model_version": model_version,
        "preprocessor_version": preprocessor_version,
        "calibrator_name": calibrator_name,
        "calibrator_version": calibrator_version,
        "raw_probability": float(raw_probability),
        "calibrated_probability": float(calibrated_probability),
        "credit_risk_band": credit_risk_band,
        "top_explanation_features": list(top_explanation_features),
        "shariah_evidence_completeness": shariah_evidence_completeness,
        "shariah_governance_status": shariah_governance_status,
        "triggered_rule_ids": list(triggered_rule_ids),
        "rule_source_ids": list(rule_source_ids),
        "policy_version": policy_version,
        "cost_scenario": cost_scenario,
        "threshold_configuration": dict(threshold_configuration),
        "final_decision": final_decision,
        "review_required": bool(review_required),
    }
    record["decision_id"] = logic_hash_v2(record)
    assert_no_raw_identifiers(record)
    missing = [f for f in REQUIRED_FIELDS_V2 if f not in record]
    if missing:
        raise ValueError(f"Audit v2 record missing required fields: {missing}")
    return record


def schema_document_v2() -> dict[str, Any]:
    return {
        "audit_schema_version": AUDIT_SCHEMA_VERSION_V2,
        "policy_version": POLICY_VERSION_V2,
        "required_fields": list(REQUIRED_FIELDS_V2),
        "logic_fields": list(LOGIC_FIELDS_V2),
        "l1_policy": (
            "l1_status is dataset/integration context. It is not an applicant-level Shariah ruling "
            "and is not the fusion-matrix governance input."
        ),
        "l2_policy": (
            "evaluation_mode must be PER_APPLICATION. evidence_hash may repeat when evidence is identical; "
            "record_reference_hash must identify the row."
        ),
        "timestamp_policy": (
            "event_timestamp records when the audit object was written. It is excluded from "
            "decision_id / logic_hash_v2 and never enters the decision engine."
        ),
        "identifier_policy": (
            "Published records store Stage 7 v2 record_reference_hash. Raw id, address, zip, and free text are forbidden."
        ),
        "forbidden_published_keys": sorted(FORBIDDEN_PUBLISHED_KEYS),
    }
