"""Versioned applicability boundary for source-specific research rules.

This module separates a diagnostic predicate from a regulatory applicability
decision. It does not decide that a source applies, that a source is outside
scope, or that an expert has validated a rule.

The six executable source rules remain ``SCOPE_UNKNOWN`` for every
jurisdiction, including PK, GB, US, and unknown. There is no Pakistan
allow-list and no ``VERIFIED_OUT_OF_SCOPE`` label. A verified in-scope status
is reserved for a future controlled review and is never emitted here.

The following inputs are not accepted as that review:

- catalog ``applicability_scope``
- catalog ``EXPERT_VALIDATED``
- a nonempty expert record
- catalog authority text
- a source identifier
- a stored hash string
- a user-supplied jurisdiction label
- the audit timestamp

The evidence schema has no contract execution date. The timestamp passed to
``evaluate()`` is an audit clock, not a contract date.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

APPLICABILITY_VERSION = "stage7-applicability-scope-unknown-v1"
SCOPE_UNKNOWN = "SCOPE_UNKNOWN"
# Reserved name only. This module never returns it.
VERIFIED_IN_SCOPE = "VERIFIED_IN_SCOPE"

SOURCE_SPECIFIC_RULE_IDS = frozenset(
    {
        "SH-SBP-SGF-002",
        "SH-SBP-SGF-003",
        "SH-SBP-MUR-INV-001",
        "SH-SBP-MUR-INV-002",
        "SH-SBP-MUR-PAY-001",
        "SH-SECP-SGR-SEC-001",
    }
)

# Public results that would be read as an authoritative source finding.
WITHHELD_AUTHORITATIVE_RESULTS = frozenset(
    {
        "PASS",
        "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
    }
)

UNAVAILABLE_PREREQUISITES = (
    "authenticated_primary_source_bytes",
    "reviewed_applicability_decision",
    "contract_execution_date",
    "qualified_expert_validation",
    "reviewed_effective_date_and_supersession_record",
)

SCOPE_UNRESOLVED_REASON = (
    "Applicability is SCOPE_UNKNOWN. The diagnostic predicate is retained "
    "separately and is not an authoritative regulatory finding. No reviewed "
    "scope decision, authenticated source bytes, contract execution date, or "
    "qualified expert validation is available. The audit timestamp is not a "
    "contract date. Catalog applicability, expert metadata, source identifiers, "
    "and stored hash strings were not accepted as verification."
)


@dataclass(frozen=True)
class ApplicabilityDecision:
    """Deterministic applicability record. Status is not a legal conclusion."""

    rule_id: str
    status: str
    applicability_version: str
    reason: str
    unavailable_prerequisites: tuple[str, ...]
    contract_date_status: str
    source_text_authenticated: bool
    expert_metadata_authenticated: bool
    source_digest_verified: bool
    catalog_metadata_accepted: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "status": self.status,
            "applicability_version": self.applicability_version,
            "reason": self.reason,
            "unavailable_prerequisites": list(self.unavailable_prerequisites),
            "contract_date_status": self.contract_date_status,
            "source_text_authenticated": self.source_text_authenticated,
            "expert_metadata_authenticated": self.expert_metadata_authenticated,
            "source_digest_verified": self.source_digest_verified,
            "catalog_metadata_accepted": self.catalog_metadata_accepted,
        }


def decide_applicability(rule_id: str) -> ApplicabilityDecision | None:
    """Return ``SCOPE_UNKNOWN`` for a source rule, or None for any other rule.

    The decision does not read catalog metadata, evidence jurisdiction, source
    hashes, or the audit timestamp.
    """
    if rule_id not in SOURCE_SPECIFIC_RULE_IDS:
        return None
    return ApplicabilityDecision(
        rule_id=rule_id,
        status=SCOPE_UNKNOWN,
        applicability_version=APPLICABILITY_VERSION,
        reason=SCOPE_UNRESOLVED_REASON,
        unavailable_prerequisites=UNAVAILABLE_PREREQUISITES,
        contract_date_status="CONTRACT_DATE_NOT_IN_SCHEMA",
        source_text_authenticated=False,
        expert_metadata_authenticated=False,
        source_digest_verified=False,
        catalog_metadata_accepted=False,
    )


def trusted_scope_established(rule_id: str) -> bool:
    """True only for a controlled in-scope decision. None exists in this repository."""
    decision = decide_applicability(rule_id)
    if decision is None:
        return False
    return decision.status == VERIFIED_IN_SCOPE


def trusted_expert_authorization_available() -> bool:
    """This repository has no independently authenticated expert-review pathway."""
    return False


def gate_source_rule(rule_id: str, raw: dict[str, Any]) -> dict[str, Any]:
    """Keep the diagnostic predicate and withhold unscoped authoritative results.

    Applicable diagnostic PASS and NOT_STRUCTURABLE_WITHOUT_REDESIGN become
    research-screen REVIEW while applicability is SCOPE_UNKNOWN. Diagnostic
    INSUFFICIENT_INFORMATION and REVIEW stay as they are: missing evidence and
    invalid evidence are not rewritten into a new compliance finding.

    A skipped predicate keeps its diagnostic reason so distinct skip reasons
    remain auditable. The attached decision states that the skip is not a
    verified legal exclusion.
    """
    diagnostic_result = raw.get("rule_result")
    diagnostic_reason = raw.get("reason")
    diagnostic_applicable = bool(raw.get("applicable"))
    screened = {
        "diagnostic_predicate_result": diagnostic_result,
        "diagnostic_predicate_reason": diagnostic_reason,
        "diagnostic_predicate_applicable": diagnostic_applicable,
        "applicable": diagnostic_applicable,
        "rule_result": diagnostic_result,
        "reason": diagnostic_reason,
    }
    decision = decide_applicability(rule_id)
    if decision is None:
        return screened
    screened["applicability_decision"] = decision.as_dict()
    screened["source_digest_verified"] = False
    if not diagnostic_applicable:
        # Keep the diagnostic sentence so distinct skips stay distinguishable,
        # and state that the sentence is not a verified scope determination.
        screened["reason"] = (
            f"{diagnostic_reason} This recorded skip is not a verified legal exclusion."
        )
        return screened
    if diagnostic_result in WITHHELD_AUTHORITATIVE_RESULTS:
        screened["rule_result"] = "REVIEW"
        screened["reason"] = decision.reason
    return screened
