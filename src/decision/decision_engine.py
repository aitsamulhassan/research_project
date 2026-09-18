"""Deterministic credit-band and fused decision. No Shariah score."""

from __future__ import annotations

from typing import Any

import numpy as np

from decision.policy_matrix import lookup, normalize_governance_status
from preprocessing.lendingclub_preprocessor import FORBIDDEN_COLUMNS, PRIMARY_PREDICTORS
from shariah.engine import evaluate as evaluate_shariah
from shariah.engine import from_mapping as shariah_from_mapping

CREDIT_PREDICTORS = tuple(PRIMARY_PREDICTORS)


def assert_probability(p: float) -> float:
    if p is None or (isinstance(p, float) and np.isnan(p)):
        raise ValueError("Missing probability.")
    value = float(p)
    if value < 0.0 or value > 1.0 or not np.isfinite(value):
        raise ValueError(f"Probability outside [0, 1]: {p!r}")
    return value


def credit_band(p: float, t_low: float, t_high: float) -> str:
    prob = assert_probability(p)
    if t_low > t_high:
        raise ValueError("t_low must be <= t_high.")
    if prob < t_low:
        return "LOW"
    if prob >= t_high:
        return "HIGH"
    return "MEDIUM"


def credit_bands(p: np.ndarray, t_low: float, t_high: float) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    if np.any(~np.isfinite(p)) or np.any(p < 0.0) or np.any(p > 1.0):
        raise ValueError("Probability array contains values outside [0, 1] or non-finite values.")
    if t_low > t_high:
        raise ValueError("t_low must be <= t_high.")
    out = np.empty(p.shape, dtype=object)
    out[p < t_low] = "LOW"
    out[(p >= t_low) & (p < t_high)] = "MEDIUM"
    out[p >= t_high] = "HIGH"
    return out


def lendingclub_governance_payload(case_id: str = "lendingclub-application-profile") -> dict[str, Any]:
    """Contract-level evidence for real LendingClub rows. Credit fields are excluded."""
    return {
        "case_id": case_id,
        "synthetic": False,
        "contract_type": "unknown",
        "institution_class": "lendingclub_application",
        "jurisdiction": "US",
        "instrument_type": "consumer_credit_application",
    }


def assert_no_credit_fields_in_governance_payload(payload: dict[str, Any]) -> None:
    blocked = set(PRIMARY_PREDICTORS) | set(FORBIDDEN_COLUMNS)
    leaked = sorted(k for k in payload if k in blocked)
    if leaked:
        raise ValueError(f"Credit/excluded fields cannot enter Shariah evaluation: {leaked}")


def evaluate_lendingclub_governance(*, timestamp: str) -> dict[str, Any]:
    payload = lendingclub_governance_payload()
    assert_no_credit_fields_in_governance_payload(payload)
    return evaluate_shariah(shariah_from_mapping(payload), timestamp=timestamp)


def fuse_decision(
    p_calibrated: float,
    governance_status: str | None,
    t_low: float,
    t_high: float,
    matrix: dict[tuple[str, str], str],
    unknown_as: str = "INSUFFICIENT_INFORMATION",
) -> dict[str, Any]:
    band = credit_band(p_calibrated, t_low, t_high)
    status = normalize_governance_status(governance_status, unknown_as)
    decision = lookup(matrix, status, band)
    return {
        "credit_risk_band": band,
        "shariah_governance_status": status,
        "final_decision": decision,
        "review_required": decision == "HUMAN_REVIEW",
    }


def apply_policy(
    p: np.ndarray,
    governance_status: str | np.ndarray | list[str],
    t_low: float,
    t_high: float,
    matrix: dict[tuple[str, str], str],
    unknown_as: str = "INSUFFICIENT_INFORMATION",
) -> dict[str, np.ndarray]:
    p = np.asarray(p, dtype=float)
    bands = credit_bands(p, t_low, t_high)
    if isinstance(governance_status, str) or governance_status is None:
        statuses_in = np.array([governance_status] * p.size, dtype=object)
    else:
        statuses_in = np.asarray(governance_status, dtype=object)
        if statuses_in.shape != p.shape:
            raise ValueError("governance_status length mismatch.")
    statuses = np.empty(p.shape, dtype=object)
    decisions = np.empty(p.shape, dtype=object)
    for i, (status, band) in enumerate(zip(statuses_in, bands)):
        statuses[i] = normalize_governance_status(None if status is None else str(status), unknown_as)
        decisions[i] = lookup(matrix, statuses[i], str(band))
    return {"credit_risk_band": bands, "shariah_governance_status": statuses, "final_decision": decisions}
