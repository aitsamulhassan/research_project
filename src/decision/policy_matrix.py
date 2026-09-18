"""Configurable governance × credit-band matrix. Not a religious ruling."""

from __future__ import annotations


DECISIONS = ("APPROVE", "HUMAN_REVIEW", "REJECT")
CREDIT_BANDS = ("LOW", "MEDIUM", "HIGH")
GOVERNANCE_STATUSES = (
    "PASS",
    "REVIEW",
    "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
    "INSUFFICIENT_INFORMATION",
)


def build_matrix(rows: list[dict[str, str]]) -> dict[tuple[str, str], str]:
    matrix: dict[tuple[str, str], str] = {}
    for row in rows:
        g = row["governance"]
        b = row["credit_band"]
        d = row["decision"]
        if g not in GOVERNANCE_STATUSES or b not in CREDIT_BANDS or d not in DECISIONS:
            raise ValueError(f"Invalid matrix row: {row}")
        matrix[(g, b)] = d
    for g in GOVERNANCE_STATUSES:
        for b in CREDIT_BANDS:
            if (g, b) not in matrix:
                raise ValueError(f"Incomplete matrix: missing {(g, b)}")
    return matrix


def normalize_governance_status(status: str | None, unknown_as: str) -> str:
    if status is None or status in {"", "unknown", "UNKNOWN"}:
        return unknown_as
    if status == "PARTIAL":
        return "REVIEW"
    if status not in GOVERNANCE_STATUSES:
        raise ValueError(f"Invalid governance status: {status}")
    return status


def lookup(matrix: dict[tuple[str, str], str], governance_status: str, credit_band: str) -> str:
    if credit_band not in CREDIT_BANDS:
        raise ValueError(f"Invalid credit band: {credit_band}")
    return matrix[(governance_status, credit_band)]
