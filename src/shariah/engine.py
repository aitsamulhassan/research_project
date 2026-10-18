"""Deterministic Shariah-oriented governance engine. No ML. Not a Shariah authority."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from shariah.applicability import (
    APPLICABILITY_VERSION,
    gate_source_rule,
    trusted_expert_authorization_available,
    trusted_scope_established,
)
from shariah.evidence import completeness
from shariah.provenance import load_source_register, source_by_id
from shariah.rules import Rule, load_catalog
from shariah.schema import FinancingEvidence, LENDINGCLUB_EXCLUDED, LENDINGCLUB_PREDICTORS

# Historical Stage 7/8 artifacts remain stage7-shariah-engine-v1.
# This identifier is the scope-gated screen: unscoped source PASS and
# unscoped source hard stops are withheld while applicability is SCOPE_UNKNOWN.
ENGINE_VERSION = "stage7-shariah-engine-v2-scope-gated"
L1L2_VERSION = "stage7-l1l2-v2"
CATALOG_VERSION = "stage7-shariah-catalog-v1"
AMENDMENT_ID = "AMENDMENT-SHARIAH-001"
CONFLICTS_PATH = Path(__file__).resolve().parents[2] / "docs" / "shariah" / "conflicts.json"

def matching_unresolved_conflicts(evidence: FinancingEvidence) -> list[dict[str, Any]]:
    blob = json.loads(CONFLICTS_PATH.read_text(encoding="utf-8"))
    hits = []
    for row in blob["conflicts"]:
        if row.get("resolution_status") != "unresolved":
            continue
        match = row.get("match") or {}
        ok = True
        for key, value in match.items():
            if evidence.as_dict().get(key) != value:
                ok = False
                break
        if ok and match:
            hits.append(row)
    return hits


PRIORITY = (
    "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
    "REVIEW",
    "INSUFFICIENT_INFORMATION",
    "PASS",
)

COVERAGE_GAP_RULES = {"SH-AAOIFI-SS8-GATE", "SH-AAOIFI-SS9-GATE"}
ARCHITECTURE_RULE_IDS = frozenset({"SH-ARCH-001", "SH-ARCH-003"})
EXPERT_VALIDATED = "EXPERT_VALIDATED"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def from_mapping(payload: dict[str, Any]) -> FinancingEvidence:
    blocked = [k for k in payload if k in LENDINGCLUB_PREDICTORS or k in LENDINGCLUB_EXCLUDED]
    extra = {k: payload[k] for k in blocked}
    known = {f.name for f in FinancingEvidence.__dataclass_fields__.values() if f.name != "extra"}
    kwargs = {k: payload.get(k) for k in known if k in payload}
    if "synthetic" not in kwargs:
        raise ValueError("Every Shariah evidence record must declare synthetic true/false.")
    return FinancingEvidence(extra=extra, **kwargs)


def _expert_record_present(record: Any) -> bool:
    """A qualified-expert record must be present. Null and empty records are absent."""
    if record is None:
        return False
    if isinstance(record, str):
        return bool(record.strip())
    if isinstance(record, dict | list | tuple | set):
        return bool(record)
    return True


def _scope_verified(payload: dict[str, Any]) -> bool:
    """Catalog applicability_scope is not a verification record.

    A named authority, a stored hash, or SOURCE_VERIFIED_PENDING_EXPERT_REVIEW
    does not establish scope. Only the applicability component can, and it
    currently has no authenticated in-scope decision.
    """
    return trusted_scope_established(str(payload.get("rule_id") or ""))


def _is_architecture(payload: dict[str, Any]) -> bool:
    return (
        payload.get("rule_id") in ARCHITECTURE_RULE_IDS
        or payload.get("rule_family") == "architecture"
        or payload.get("validation_status") == "RESEARCH_ARCHITECTURE_NOT_A_RULING"
    )


def _is_contract_specific(payload: dict[str, Any], contract_type: str | None) -> bool:
    """True when the catalog row is for this contract, not an architecture or gate row."""
    if _is_architecture(payload) or payload.get("rule_id") in COVERAGE_GAP_RULES:
        return False
    declared = payload.get("contract_type")
    if not isinstance(declared, str) or declared.strip() in {"", "any"}:
        return False
    return declared == contract_type


def _is_substantive(payload: dict[str, Any]) -> bool:
    """Regulatory substance excludes architecture checks and unavailable-standard gates."""
    if _is_architecture(payload) or payload.get("rule_id") in COVERAGE_GAP_RULES:
        return False
    return True


def _rule_meets_affirmative_bar(payload: dict[str, Any], raw: dict[str, Any]) -> bool:
    """Catalog expert status, records, scope, and clause text cannot open this gate.

    ``raw`` is the guarded research-screen result, not the diagnostic predicate.
    A controlled expert pathway does not exist in this repository, so the bar
    stays closed. A catalog ``EXPERT_VALIDATED`` status is rejected rather than
    accepted. ``_expert_record_present`` still describes a nonempty record; a
    nonempty record is not authorization.
    """
    catalog_declares_expert = payload.get("validation_status") == EXPERT_VALIDATED
    return (
        raw.get("rule_result") == "PASS"
        and trusted_expert_authorization_available()
        and not catalog_declares_expert
        and _expert_record_present(payload.get("expert_validation_record"))
        and _scope_verified(payload)
    )


def _affirmative_coverage(
    evidence: FinancingEvidence,
    considered: list[tuple[Rule, dict[str, Any]]],
    *,
    layer_a: str,
    coverage_gap: bool,
    unresolved_conflict: bool,
) -> tuple[bool, dict[str, Any]]:
    """Return whether an overall PASS is demonstrated, plus a deterministic audit record.

    Architecture checks cannot satisfy this gate. Source verification pending expert
    review cannot satisfy it. NOT_APPLICABLE rows are not treated as passes.
    """
    unmet: list[str] = []
    if layer_a != "COMPLETE":
        unmet.append("layer_a_not_complete")
    if coverage_gap:
        unmet.append("unresolved_coverage_gap")
    if unresolved_conflict:
        unmet.append("unresolved_conflict")

    contract_specific: list[tuple[Rule, dict[str, Any]]] = []
    other_substantive: list[tuple[Rule, dict[str, Any]]] = []
    for rule, raw in considered:
        if not raw.get("applicable") or raw.get("rule_result") in {None, "NOT_APPLICABLE"}:
            continue
        if _is_contract_specific(rule.payload, evidence.contract_type):
            contract_specific.append((rule, raw))
        elif _is_substantive(rule.payload):
            other_substantive.append((rule, raw))

    if not contract_specific:
        unmet.append("no_applicable_contract_specific_coverage")

    expert_pass_ids: list[str] = []
    for rule, raw in contract_specific + other_substantive:
        if not trusted_scope_established(rule.rule_id):
            unmet.append("no_trusted_applicability_pathway")
        if not trusted_expert_authorization_available():
            unmet.append("no_trusted_expert_authorization_pathway")
        if raw.get("rule_result") != "PASS":
            unmet.append("applicable_substantive_result_not_pass")
            continue
        if not _expert_record_present(rule.payload.get("expert_validation_record")):
            unmet.append("expert_validation_record_missing")
        if not _scope_verified(rule.payload):
            unmet.append("applicability_scope_not_verified")
        if _rule_meets_affirmative_bar(rule.payload, raw):
            expert_pass_ids.append(rule.rule_id)

    deduped: list[str] = []
    seen: set[str] = set()
    for item in unmet:
        if item not in seen:
            seen.add(item)
            deduped.append(item)

    required = len(contract_specific) + len(other_substantive)
    permitted = (
        not deduped
        and len(contract_specific) > 0
        and required > 0
        and len(expert_pass_ids) == required
    )
    guard = {
        "architecture_rules_excluded_from_affirmative_pass": sorted(ARCHITECTURE_RULE_IDS),
        "affirmative_pass_permitted": permitted,
        "unmet_affirmative_conditions": deduped,
        "contract_specific_applicable_rule_ids": [rule.rule_id for rule, _raw in contract_specific],
        "substantive_applicable_rule_ids": [rule.rule_id for rule, _raw in contract_specific + other_substantive],
        "expert_validated_scoped_pass_rule_ids": expert_pass_ids,
        "catalog_self_assertion_accepted": False,
        "trusted_applicability_pathway_available": False,
    }
    return permitted, guard


def _aggregate(
    layer_a: str,
    operational_results: list[str],
    *,
    identification_review: bool,
    coverage_gap: bool,
    affirmative_coverage: bool,
) -> str:
    """Combine rule results. Negative evidence keeps its previous precedence.

    Previous PASS rule: Layer A COMPLETE, operational results non-empty, and every
    operational result PASS. Architecture PASSes were operational results, so they
    could produce overall PASS with no contract-specific rule.

    Unchanged earlier branches:
    1. NOT_STRUCTURABLE_WITHOUT_REDESIGN if any operational rule returned it.
    2. INSUFFICIENT_INFORMATION if Layer A is INSUFFICIENT or any operational rule
       returned INSUFFICIENT_INFORMATION.
    3. REVIEW if identification requires review, any operational rule returned
       REVIEW, Layer A is PARTIAL, or a named coverage-gap rule fired.

    PASS now also requires affirmative_coverage. When every check that ran returned
    PASS but that coverage is not demonstrated, the status is REVIEW: an unresolved
    coverage or expert-validation gap, not a prohibition and not missing Layer A data.
    """
    if "NOT_STRUCTURABLE_WITHOUT_REDESIGN" in operational_results:
        return "NOT_STRUCTURABLE_WITHOUT_REDESIGN"
    if layer_a == "INSUFFICIENT" or "INSUFFICIENT_INFORMATION" in operational_results:
        return "INSUFFICIENT_INFORMATION"
    if identification_review or "REVIEW" in operational_results or layer_a == "PARTIAL" or coverage_gap:
        return "REVIEW"
    if (
        layer_a == "COMPLETE"
        and operational_results
        and all(result == "PASS" for result in operational_results)
        and affirmative_coverage
    ):
        return "PASS"
    if layer_a == "COMPLETE" and operational_results and all(result == "PASS" for result in operational_results):
        return "REVIEW"
    return "INSUFFICIENT_INFORMATION"


def evaluate(
    evidence: FinancingEvidence,
    *,
    timestamp: str | None = None,
    catalog: list[Rule] | None = None,
) -> dict[str, Any]:
    ts = timestamp or utc_now()
    layer_a = completeness(evidence)
    register = load_source_register()
    rules = catalog if catalog is not None else load_catalog()
    evaluations = []
    operational_results: list[str] = []
    considered: list[tuple[Rule, dict[str, Any]]] = []
    coverage_gap = False
    identification_review = evidence.contract_type == "ambiguous"
    conflicts = matching_unresolved_conflicts(evidence)
    for rule in rules:
        raw = rule.evaluate(evidence)
        screen = gate_source_rule(rule.rule_id, raw)
        public_result = screen["rule_result"] if screen["applicable"] else "NOT_APPLICABLE"
        considered.append((rule, {"applicable": screen["applicable"], "rule_result": public_result}))
        source = source_by_id(rule.payload["source_id"], register)
        row = {
            "rule_id": rule.rule_id,
            "rule_version": rule.payload["rule_version"],
            "contract_type": evidence.contract_type,
            "input_evidence": evidence.as_dict(),
            "required_evidence": rule.payload.get("required_information", []),
            "evidence_status": "present" if screen["applicable"] else "not_applicable",
            "rule_result": public_result,
            "applicable": screen["applicable"],
            "reason": screen["reason"],
            "diagnostic_predicate_result": screen["diagnostic_predicate_result"],
            "diagnostic_predicate_reason": screen["diagnostic_predicate_reason"],
            "diagnostic_predicate_applicable": screen["diagnostic_predicate_applicable"],
            "authority": rule.payload["authority"],
            "source_document": rule.payload["document"],
            "source_section": rule.payload.get("section", "NOT_VERIFIED"),
            "source_clause": rule.payload.get("clause", "NOT_VERIFIED"),
            "source_version": rule.payload.get("source_version", source.version),
            "source_url": rule.payload["source_url"],
            "interpretation_note": rule.payload["interpretation_note"],
            "implementation_note": rule.payload["implementation_note"],
            "source_statement": rule.payload["source_statement"],
            "validation_status": rule.payload["validation_status"],
            "timestamp": ts,
            "synthetic": evidence.synthetic,
            "label": "Synthetic governance test case" if evidence.synthetic else "Non-synthetic evidence record",
        }
        if "applicability_decision" in screen:
            row["applicability_decision"] = screen["applicability_decision"]
            row["source_digest_verified"] = False
        evaluations.append(row)
        if screen["applicable"] and public_result in PRIORITY:
            if rule.rule_id in COVERAGE_GAP_RULES:
                coverage_gap = True
            else:
                operational_results.append(public_result)
    if conflicts and evidence.contract_type not in {"unknown"}:
        identification_review = identification_review or layer_a["layer_a"] != "INSUFFICIENT"
    affirmative_coverage, aggregation_guard = _affirmative_coverage(
        evidence,
        considered,
        layer_a=layer_a["layer_a"],
        coverage_gap=coverage_gap,
        unresolved_conflict=bool(conflicts) and evidence.contract_type not in {"unknown"},
    )
    overall = _aggregate(
        layer_a["layer_a"],
        operational_results,
        identification_review=identification_review,
        coverage_gap=coverage_gap,
        affirmative_coverage=affirmative_coverage,
    )
    return {
        "engine_version": ENGINE_VERSION,
        "applicability_version": APPLICABILITY_VERSION,
        "catalog_version": CATALOG_VERSION,
        "case_id": evidence.case_id,
        "synthetic": evidence.synthetic,
        "label": "Synthetic governance test case" if evidence.synthetic else "Non-synthetic evidence record",
        "contract_type": evidence.contract_type,
        "layer_a_completeness": layer_a,
        "rule_evaluations": evaluations,
        "overall_governance_status": overall,
        "aggregation_guard": aggregation_guard,
        "unresolved_conflicts": [c["conflict_id"] for c in conflicts],
        "certification_claim": False,
        "disclaimer": (
            "Research prototype for Shariah-oriented governance and evidence traceability, "
            "not a Shariah certification mechanism."
        ),
        "timestamp": ts,
    }
