"""Deterministic Shariah-oriented governance engine. No ML. Not a Shariah authority."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import json

from shariah.evidence import completeness
from shariah.provenance import load_source_register, source_by_id
from shariah.rules import Rule, load_catalog
from shariah.schema import FinancingEvidence, LENDINGCLUB_EXCLUDED, LENDINGCLUB_PREDICTORS

ENGINE_VERSION = "stage7-shariah-engine-v1"
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


def _aggregate(
    layer_a: str,
    operational_results: list[str],
    *,
    identification_review: bool,
    coverage_gap: bool,
) -> str:
    if "NOT_STRUCTURABLE_WITHOUT_REDESIGN" in operational_results:
        return "NOT_STRUCTURABLE_WITHOUT_REDESIGN"
    if layer_a == "INSUFFICIENT" or "INSUFFICIENT_INFORMATION" in operational_results:
        return "INSUFFICIENT_INFORMATION"
    if identification_review or "REVIEW" in operational_results or layer_a == "PARTIAL" or coverage_gap:
        return "REVIEW"
    if layer_a == "COMPLETE" and operational_results and all(r == "PASS" for r in operational_results):
        return "PASS"
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
    coverage_gap = False
    identification_review = evidence.contract_type == "ambiguous"
    conflicts = matching_unresolved_conflicts(evidence)
    for rule in rules:
        raw = rule.evaluate(evidence)
        source = source_by_id(rule.payload["source_id"], register)
        row = {
            "rule_id": rule.rule_id,
            "rule_version": rule.payload["rule_version"],
            "contract_type": evidence.contract_type,
            "input_evidence": evidence.as_dict(),
            "required_evidence": rule.payload.get("required_information", []),
            "evidence_status": "present" if raw["applicable"] else "not_applicable",
            "rule_result": raw["rule_result"] if raw["applicable"] else "NOT_APPLICABLE",
            "applicable": raw["applicable"],
            "reason": raw["reason"],
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
        evaluations.append(row)
        if raw["applicable"] and raw["rule_result"] in PRIORITY:
            if rule.rule_id in COVERAGE_GAP_RULES:
                coverage_gap = True
            else:
                operational_results.append(raw["rule_result"])
    if conflicts and evidence.contract_type not in {"unknown"}:
        identification_review = identification_review or layer_a["layer_a"] != "INSUFFICIENT"
    overall = _aggregate(
        layer_a["layer_a"],
        operational_results,
        identification_review=identification_review,
        coverage_gap=coverage_gap,
    )
    return {
        "engine_version": ENGINE_VERSION,
        "catalog_version": CATALOG_VERSION,
        "case_id": evidence.case_id,
        "synthetic": evidence.synthetic,
        "label": "Synthetic governance test case" if evidence.synthetic else "Non-synthetic evidence record",
        "contract_type": evidence.contract_type,
        "layer_a_completeness": layer_a,
        "rule_evaluations": evaluations,
        "overall_governance_status": overall,
        "unresolved_conflicts": [c["conflict_id"] for c in conflicts],
        "certification_claim": False,
        "disclaimer": (
            "Research prototype for Shariah-oriented governance and evidence traceability, "
            "not a Shariah certification mechanism."
        ),
        "timestamp": ts,
    }
