"""L2 per-application governance evidence extraction and evaluation.

Does not infer Islamic contract type from LendingClub purpose/title/desc.
Does not implement AAOIFI operative clauses.
"""

from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import replace
from typing import Any, Mapping

from shariah.engine import AMENDMENT_ID, L1L2_VERSION, evaluate
from shariah.evidence import completeness
from shariah.l1 import DATASET_ID_LENDINGCLUB, LENDINGCLUB_DATASET_IDS, assess_dataset_readiness
from shariah.rules import load_catalog
from shariah.schema import EVIDENCE_FIELDS, FIREWALL_FIELDS, FinancingEvidence, OUTCOMES

EVALUATION_MODE_PER_APPLICATION = "PER_APPLICATION"
RECORD_HASH_PREFIX = "stage7-v2-record-ref-v1"
EVIDENCE_HASH_PREFIX = "stage7-v2-evidence-v1"

# Semantic governance fields hashed for cache identity. case_id is row identity, not evidence.
SEMANTIC_EVIDENCE_FIELDS = tuple(name for name in EVIDENCE_FIELDS if name != "case_id")

LENDINGCLUB_MISSING_EVIDENCE = (
    "verified_contract_type",
    "shariah_board_approval",
    "invoice_or_payment_path",
    "security_claim",
    "security_certificate",
    "ownership_or_possession_evidence",
    "contractual_sequence_documented",
)

CERTIFICATION_PHRASES = (
    "shariah compliant",
    "shariah-compliant",
    "halal loan",
    "haram loan",
    "certified shariah",
)


def firewall_fields_in(payload: Mapping[str, Any]) -> tuple[str, ...]:
    return tuple(sorted(name for name in FIREWALL_FIELDS if name in payload))


def semantic_evidence_payload(evidence: FinancingEvidence) -> dict[str, Any]:
    data = evidence.as_dict()
    payload = {name: data.get(name) for name in SEMANTIC_EVIDENCE_FIELDS}
    payload["_extra"] = dict(evidence.extra)
    return payload


def evidence_object_hash(evidence: FinancingEvidence) -> str:
    blob = json.dumps(semantic_evidence_payload(evidence), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(f"{EVIDENCE_HASH_PREFIX}|{blob}".encode("utf-8")).hexdigest()


def compute_record_reference_hash(dataset_id: str, row: Mapping[str, Any]) -> str:
    """Privacy-safe row identity. Raw id/address/zip/free text are not stored."""
    if row.get("_fixture_key") not in {None, ""}:
        token = "fixture|" + str(row["_fixture_key"])
    elif row.get("id") not in {None, ""}:
        inner = hashlib.sha256(str(row["id"]).encode("utf-8")).hexdigest()
        token = "id|" + inner
    elif row.get("_row_index") not in {None, ""}:
        token = "row_index|" + str(row["_row_index"])
    else:
        raise ValueError("L2 record reference requires _fixture_key, id, or _row_index.")
    return hashlib.sha256(f"{RECORD_HASH_PREFIX}|{dataset_id}|{token}".encode("utf-8")).hexdigest()


def inject_firewall_field_for_boundary_test(
    evidence: FinancingEvidence,
    field: str,
    value: Any,
) -> FinancingEvidence:
    """Deliberate SH-ARCH-003 boundary injection. Not a production extractor path."""
    if field not in FIREWALL_FIELDS:
        raise ValueError(f"{field!r} is not a firewall field.")
    extra = dict(evidence.extra)
    extra[field] = value
    return replace(evidence, extra=extra)


def extract_application_governance_evidence(
    row: Mapping[str, Any],
    *,
    dataset_id: str = DATASET_ID_LENDINGCLUB,
    synthetic: bool = True,
) -> tuple[FinancingEvidence, dict[str, Any]]:
    """Build a per-row Shariah evidence object. Firewall fields are dropped, not interpreted."""
    if dataset_id not in LENDINGCLUB_DATASET_IDS:
        raise ValueError(f"No L2 extractor for dataset_id={dataset_id!r}.")
    dropped = firewall_fields_in(row)
    record_hash = compute_record_reference_hash(dataset_id, row)
    case_id = f"l2:{dataset_id}:{record_hash[:16]}"
    evidence = FinancingEvidence(
        case_id=case_id,
        synthetic=synthetic,
        contract_type="unknown",
        institution_class="lendingclub_application",
        jurisdiction="US",
        instrument_type="consumer_credit_application",
        sb_prior_product_approval=None,
        sb_approved_agreements_and_process_flows=None,
        invoice_name_status=None,
        shariah_advisor_invoice_exception_approval=None,
        alternative_purchase_documents_present=None,
        payment_channel=None,
        shariah_advisor_agent_payment_approval=None,
        agent_payment_reasons_recorded=None,
        claims_shariah_compliant_security=None,
        secp_shariah_compliance_certificate=None,
        underlying_asset_identified=None,
        ownership_or_possession_evidence=None,
        late_payment_treatment_documented=None,
        contractual_sequence_documented=None,
        extra={},
    )
    meta = {
        "dataset_id": dataset_id,
        "record_reference_hash": record_hash,
        "evidence_hash": evidence_object_hash(evidence),
        "evaluation_mode": EVALUATION_MODE_PER_APPLICATION,
        "firewall_fields_dropped": list(dropped),
        "source_fields_copied_into_evidence": [],
        "missing_evidence": list(LENDINGCLUB_MISSING_EVIDENCE),
        "purpose_used_as_contract_type": False,
        "amendment_id": AMENDMENT_ID,
        "l1l2_version": L1L2_VERSION,
    }
    return evidence, meta


def _triggered_rules(engine_result: Mapping[str, Any]) -> list[str]:
    ids = []
    for row in engine_result.get("rule_evaluations", []):
        if row.get("applicable") and row.get("rule_result") not in {None, "NOT_APPLICABLE", "PASS"}:
            ids.append(row["rule_id"])
    return ids


def _source_ids(triggered: list[str]) -> list[str]:
    by_id = {rule.rule_id: rule.payload.get("source_id") for rule in load_catalog()}
    out: list[str] = []
    seen: set[str] = set()
    for rule_id in triggered:
        source_id = by_id.get(rule_id)
        if source_id and source_id not in seen:
            seen.add(source_id)
            out.append(source_id)
    return out


def _expert_states(engine_result: Mapping[str, Any]) -> list[str]:
    states = []
    seen: set[str] = set()
    for row in engine_result.get("rule_evaluations", []):
        status = row.get("validation_status")
        if status and status not in seen:
            seen.add(status)
            states.append(status)
    return states


def _bind_row_identity(
    engine_result: dict[str, Any],
    evidence: FinancingEvidence,
    meta: Mapping[str, Any],
) -> dict[str, Any]:
    bound = copy.deepcopy(engine_result)
    bound["case_id"] = evidence.case_id
    bound["synthetic"] = evidence.synthetic
    bound["label"] = "Synthetic governance test case" if evidence.synthetic else "Non-synthetic evidence record"
    bound["contract_type"] = evidence.contract_type
    layer_a = bound.get("layer_a_completeness") or completeness(evidence)
    if isinstance(layer_a, dict):
        layer_a = dict(layer_a)
        layer_a["case_id"] = evidence.case_id
        layer_a["synthetic"] = evidence.synthetic
        bound["layer_a_completeness"] = layer_a
    for row in bound.get("rule_evaluations", []):
        row["case_id"] = evidence.case_id
        row["synthetic"] = evidence.synthetic
        row["contract_type"] = evidence.contract_type
        if isinstance(row.get("input_evidence"), dict):
            inp = dict(row["input_evidence"])
            inp["case_id"] = evidence.case_id
            inp["synthetic"] = evidence.synthetic
            row["input_evidence"] = inp
    bound["evaluation_mode"] = EVALUATION_MODE_PER_APPLICATION
    bound["dataset_id"] = meta["dataset_id"]
    bound["record_reference_hash"] = meta["record_reference_hash"]
    bound["evidence_hash"] = meta["evidence_hash"]
    bound["missing_evidence"] = list(meta["missing_evidence"])
    bound["l1l2_version"] = L1L2_VERSION
    bound["amendment_id"] = AMENDMENT_ID
    bound["certification_claim"] = False
    return bound


def evaluate_application_governance(
    application_evidence: FinancingEvidence,
    *,
    l2_meta: Mapping[str, Any],
    l1_result: Mapping[str, Any] | None = None,
    timestamp: str | None = None,
    cache: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Evaluate one application's evidence object. Cache is by evidence hash only."""
    l1 = dict(l1_result) if l1_result is not None else assess_dataset_readiness(l2_meta["dataset_id"])
    evidence_hash = l2_meta["evidence_hash"]
    cache_hit = False
    if cache is not None and evidence_hash in cache:
        engine_out = copy.deepcopy(cache[evidence_hash])
        cache_hit = True
    else:
        engine_out = evaluate(application_evidence, timestamp=timestamp)
        if cache is not None:
            cache[evidence_hash] = copy.deepcopy(engine_out)
    bound = _bind_row_identity(engine_out, application_evidence, l2_meta)
    triggered = _triggered_rules(bound)
    bound["triggered_rule_ids"] = triggered
    bound["source_ids"] = _source_ids(triggered)
    expert_states = _expert_states(bound)
    bound["expert_validation_states"] = expert_states
    bound["any_expert_validated"] = "EXPERT_VALIDATED" in expert_states
    bound["l1"] = {
        "readiness_status": l1["readiness_status"],
        "is_applicant_level_ruling": False,
        "evaluation_mode": l1.get("evaluation_mode"),
        "dataset_id": l1.get("dataset_id"),
    }
    bound["l2"] = {
        "evaluation_mode": EVALUATION_MODE_PER_APPLICATION,
        "dataset_id": l2_meta["dataset_id"],
        "record_reference_hash": l2_meta["record_reference_hash"],
        "evidence_hash": evidence_hash,
        "missing_evidence": list(l2_meta["missing_evidence"]),
        "cache_hit": cache_hit,
        "firewall_fields_dropped": list(l2_meta.get("firewall_fields_dropped", [])),
    }
    bound["cache_hit"] = cache_hit
    return bound


def result_contains_certification_claim(result: Mapping[str, Any]) -> bool:
    """True only if the automated determination claims compliance. Quoted source text is ignored."""
    if result.get("certification_claim") is True:
        return True
    status = str(result.get("overall_governance_status", "")).lower()
    label = str(result.get("label", "")).lower()
    if result.get("overall_governance_status") not in OUTCOMES:
        return True
    scanned = f"{status} {label}"
    return any(phrase in scanned for phrase in CERTIFICATION_PHRASES)


def evaluate_lendingclub_application(
    row: Mapping[str, Any],
    *,
    dataset_id: str = DATASET_ID_LENDINGCLUB,
    synthetic: bool = True,
    timestamp: str | None = None,
    cache: dict[str, dict[str, Any]] | None = None,
    l1_result: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    evidence, meta = extract_application_governance_evidence(row, dataset_id=dataset_id, synthetic=synthetic)
    return evaluate_application_governance(
        evidence,
        l2_meta=meta,
        l1_result=l1_result,
        timestamp=timestamp,
        cache=cache,
    )
