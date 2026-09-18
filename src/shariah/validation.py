"""Catalog validation. Fails closed: unverified clauses cannot execute as authority."""

from __future__ import annotations

from typing import Any

EXECUTABLE_STATUSES = {"SOURCE_VERIFIED_PENDING_EXPERT_REVIEW", "EXPERT_VALIDATED"}
ARCHITECTURE_STATUSES = {"RESEARCH_ARCHITECTURE_NOT_A_RULING"}


def assert_source_fields(source: dict[str, Any]) -> None:
    for key in ("source_id", "authority", "organization", "document_title", "url", "access_date", "verification_status"):
        if not source.get(key):
            raise ValueError(f"Source missing required field {key}")
    if source.get("verification_status") == "CLAUSE_VERIFIED" and (
        source.get("section") in {None, "", "NOT_VERIFIED"} and source.get("clause") in {None, "", "NOT_VERIFIED"}
    ):
        raise ValueError("Clause marked verified without section/clause evidence.")


def assert_rule_executable(rule: dict[str, Any]) -> None:
    status = rule.get("validation_status")
    if status == "EXPERT_VALIDATED" and not rule.get("expert_validation_record"):
        raise ValueError(f"{rule.get('rule_id')} claims EXPERT_VALIDATED without an expert record.")
    if status == "NOT_VERIFIED" and rule.get("executable") is True:
        raise ValueError(f"{rule.get('rule_id')} is NOT_VERIFIED and cannot execute as authoritative.")
    if rule.get("executable") and status not in EXECUTABLE_STATUSES | ARCHITECTURE_STATUSES:
        raise ValueError(f"{rule.get('rule_id')} executable flag inconsistent with validation_status={status}")
    if rule.get("executable"):
        for key in ("authority", "document", "source_url", "source_id"):
            if not rule.get(key):
                raise ValueError(f"{rule.get('rule_id')} missing provenance field {key}")
        if rule.get("standard_applicable") and not rule.get("standard"):
            raise ValueError(f"{rule.get('rule_id')} standard marked applicable but standard number missing.")
        if rule.get("clause_verified") and rule.get("clause") in {None, "", "NOT_VERIFIED"}:
            raise ValueError(f"{rule.get('rule_id')} clause marked verified without clause evidence.")
