"""S10-R1-YEAR: exploratory/descriptive post-hoc year mix on frozen LC TEST p_selected.

Non-confirmatory. Does not retrain, refit, search thresholds, or invent calendar fields.
Does not load EBM or Platt joblib objects for scoring.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from decision.stage9_1 import (
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_T_STAR,
    EXPECTED_TEST_CAL_SHA256,
    TEST_CAL,
    apply_frozen_binary,
    apply_frozen_credit_only,
    credit_bands,
    sha256_file,
    wilson_ci,
)
from stage10.s10_i1_identity import (
    EXPECTED_N,
    EXPECTED_TABLE3_SHA256,
    EXPECTED_V2_FREEZE_SHA256,
    g0_from_bands,
    live_protected_hashes,
)

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_ID = "s10_r1_year_v1"
CLASSIFICATION = "EXPLORATORY / DESCRIPTIVE POST-HOC REANALYSIS — NON-CONFIRMATORY"
ALLOWED_YEARS = (2017, 2018)
I1_METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json"
STAGE5_TEMPORAL = ROOT / "results" / "calibration" / "metrics" / "stage5_temporal.json"
DECISIONS = ("APPROVE", "HUMAN_REVIEW", "REJECT")
BANDS = ("LOW", "MEDIUM", "HIGH")
ARCHITECTURES = ("A0", "A1", "A3_A4")


def json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return json_safe(obj.tolist())
    if isinstance(obj, (np.floating, float)):
        value = float(obj)
        if math.isnan(value) or math.isinf(value):
            return None
        return value
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    return obj


def _rate_block(count: int, n: int) -> dict[str, Any]:
    lo, hi = wilson_ci(count, n) if n else (float("nan"), float("nan"))
    rate = (count / n) if n else float("nan")
    return {
        "count": int(count),
        "rate": rate,
        "percentage": (100.0 * rate) if n else float("nan"),
        "wilson_ci_lower": lo,
        "wilson_ci_upper": hi,
        "ci_method": "wilson_95",
    }


def _decision_block(decisions: np.ndarray) -> dict[str, Any]:
    n = int(decisions.size)
    out: dict[str, Any] = {"n": n}
    for label in DECISIONS:
        out[label] = _rate_block(int((decisions == label).sum()), n)
    return out


def _band_block(bands: np.ndarray, y: np.ndarray) -> dict[str, Any]:
    n = int(bands.size)
    out: dict[str, Any] = {"n": n}
    for band in BANDS:
        mask = bands == band
        k = int(mask.sum())
        n_default = int(y[mask].sum()) if k else 0
        block = _rate_block(k, n)
        default_block = _rate_block(n_default, k) if k else _rate_block(0, 0)
        out[band] = {
            "count": k,
            "rate": block["rate"],
            "percentage": block["percentage"],
            "wilson_ci_lower": block["wilson_ci_lower"],
            "wilson_ci_upper": block["wilson_ci_upper"],
            "n_default": n_default,
            "default_rate": default_block["rate"],
            "default_rate_wilson_ci_lower": default_block["wilson_ci_lower"],
            "default_rate_wilson_ci_upper": default_block["wilson_ci_upper"],
            "ci_method": "wilson_95",
        }
    return out


def _composition(y: np.ndarray) -> dict[str, Any]:
    n = int(y.size)
    n_default = int(y.sum())
    return {"n": n, "n_default": n_default, **_rate_block(n_default, n)}


def stage5_year_n() -> dict[int, int]:
    rows = json.loads(STAGE5_TEMPORAL.read_text(encoding="utf-8"))
    by_year: dict[int, int] = {}
    for row in rows:
        if str(row.get("method")) != "platt":
            continue
        by_year[int(row["year"])] = int(row["n"])
    return by_year


def require_i1_gate() -> dict[str, Any]:
    if not I1_METRICS.exists():
        raise RuntimeError("S10-R1 aborted: S10-I1 metrics missing.")
    payload = json.loads(I1_METRICS.read_text(encoding="utf-8"))
    status = str(payload.get("status") or "")
    if payload.get("issues"):
        raise RuntimeError(f"S10-R1 aborted: S10-I1 reported issues {payload['issues']}.")
    if not status.startswith("PASS"):
        raise RuntimeError(f"S10-R1 aborted: S10-I1 status={status!r} is not PASS.")
    live_cal = sha256_file(TEST_CAL)
    recorded = payload.get("hashes", {}).get("test_cal_sha256")
    if live_cal != EXPECTED_TEST_CAL_SHA256:
        raise RuntimeError("S10-R1 aborted: live TEST calibrated CSV hash mismatch.")
    if recorded not in (None, EXPECTED_TEST_CAL_SHA256):
        raise RuntimeError("S10-R1 aborted: S10-I1 recorded TEST cal hash mismatch.")
    return payload


def year_slice_payload(
    year: int,
    p: np.ndarray,
    y: np.ndarray,
) -> dict[str, Any]:
    bands = credit_bands(p, EXPECTED_T_LOW, EXPECTED_T_HIGH)
    a0 = apply_frozen_credit_only(p)
    a1 = g0_from_bands(bands)
    a3 = apply_frozen_binary(p)
    composition = _composition(y)
    a0_block = _decision_block(a0)
    a1_block = _decision_block(a1)
    a3_block = _decision_block(a3)
    delta_review = a1_block["HUMAN_REVIEW"]["rate"] - a0_block["HUMAN_REVIEW"]["rate"]
    return {
        "year": int(year),
        "composition": composition,
        "A0": a0_block,
        "A1": a1_block,
        "A3_A4": a3_block,
        "credit_bands": _band_block(bands, y),
        "delta_review_rate_A1_minus_A0": delta_review,
        "delta_review_equals_LOW_rate": bool(
            math.isclose(delta_review, float(a0_block["APPROVE"]["rate"]), rel_tol=0.0, abs_tol=1e-15)
        ),
        "a3_human_review_count": a3_block["HUMAN_REVIEW"]["count"],
        "a1_approve_count": a1_block["APPROVE"]["count"],
    }


def descriptive_notes(by_year: dict[int, dict[str, Any]]) -> list[str]:
    y17 = by_year[2017]
    y18 = by_year[2018]
    notes = [
        (
            f"TEST composition: 2017 n={y17['composition']['n']}, "
            f"2018 n={y18['composition']['n']}. This is the stored year split, not a sampling design."
        ),
        (
            "Observed difference in default prevalence: "
            f"2017 {y17['composition']['rate']:.6f} "
            f"({y17['composition']['n_default']}/{y17['composition']['n']}) vs "
            f"2018 {y18['composition']['rate']:.6f} "
            f"({y18['composition']['n_default']}/{y18['composition']['n']}). "
            "This is a descriptive temporal difference, not a causal effect, "
            "not concept drift inference, and not a generalization-failure test."
        ),
    ]
    for arch in ARCHITECTURES:
        a17 = y17[arch]
        a18 = y18[arch]
        notes.append(
            f"{arch} year-specific decision allocation: "
            f"2017 APPROVE/REVIEW/REJECT = "
            f"{a17['APPROVE']['count']}/{a17['HUMAN_REVIEW']['count']}/{a17['REJECT']['count']} "
            f"vs 2018 "
            f"{a18['APPROVE']['count']}/{a18['HUMAN_REVIEW']['count']}/{a18['REJECT']['count']}. "
            "Reported as a post-hoc temporal pattern under frozen maps, not as policy failure."
        )
    high_total = y17["credit_bands"]["HIGH"]["count"] + y18["credit_bands"]["HIGH"]["count"]
    notes.append(
        f"HIGH credit band remains n={high_total} overall. Year-wise HIGH rates are descriptive "
        "counts only and do not support inference beyond those counts."
    )
    notes.append("No p-test of 2017 vs 2018 equality was computed.")
    notes.append("Year was not used to select a threshold, calibrator, or policy.")
    return notes


def decision_mix_rows(by_year: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for year, payload in by_year.items():
        for architecture in ARCHITECTURES:
            block = payload[architecture]
            rows.append(
                {
                    "year": year,
                    "architecture": architecture,
                    "n": payload["composition"]["n"],
                    "n_default": payload["composition"]["n_default"],
                    "default_rate": payload["composition"]["rate"],
                    "n_approve": block["APPROVE"]["count"],
                    "n_review": block["HUMAN_REVIEW"]["count"],
                    "n_reject": block["REJECT"]["count"],
                    "approval_rate": block["APPROVE"]["rate"],
                    "review_rate": block["HUMAN_REVIEW"]["rate"],
                    "rejection_rate": block["REJECT"]["rate"],
                    "approval_rate_ci_lower": block["APPROVE"]["wilson_ci_lower"],
                    "approval_rate_ci_upper": block["APPROVE"]["wilson_ci_upper"],
                    "review_rate_ci_lower": block["HUMAN_REVIEW"]["wilson_ci_lower"],
                    "review_rate_ci_upper": block["HUMAN_REVIEW"]["wilson_ci_upper"],
                    "rejection_rate_ci_lower": block["REJECT"]["wilson_ci_lower"],
                    "rejection_rate_ci_upper": block["REJECT"]["wilson_ci_upper"],
                    "ci_method": "wilson_95",
                }
            )
    return rows


def credit_band_rows(by_year: dict[int, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for year, payload in by_year.items():
        for band in BANDS:
            block = payload["credit_bands"][band]
            rows.append(
                {
                    "year": year,
                    "band": band,
                    "n_year": payload["composition"]["n"],
                    "n_band": block["count"],
                    "band_rate": block["rate"],
                    "n_default": block["n_default"],
                    "default_rate": block["default_rate"],
                    "default_rate_ci_lower": block["default_rate_wilson_ci_lower"],
                    "default_rate_ci_upper": block["default_rate_wilson_ci_upper"],
                    "t_low": EXPECTED_T_LOW,
                    "t_high": EXPECTED_T_HIGH,
                    "ci_method": "wilson_95",
                }
            )
    return rows


def run_year_reanalysis() -> dict[str, Any]:
    issues: list[str] = []
    documentation_limitations: list[str] = [
        "HIGH credit-band n is 27 on pooled TEST; year-wise HIGH default rates are descriptive counts only.",
        "S10-R1 is post-hoc grouping of already-unblinded LendingClub TEST outputs. It is not confirmatory.",
    ]
    try:
        i1 = require_i1_gate()
    except RuntimeError as exc:
        return json_safe(
            {
                "experiment_id": EXPERIMENT_ID,
                "classification": CLASSIFICATION,
                "status": "ABORTED — year/identity integrity failed",
                "confirmatory_experiment": False,
                "issues": [str(exc)],
                "documentation_limitations": documentation_limitations,
                "models_trained": False,
                "calibration_refit": False,
                "thresholds_searched": False,
                "year_specific_threshold": False,
                "uci_opened": False,
                "s10_a1_gap_executed": False,
                "s10_a4_executed": False,
            }
        )
    hashes = live_protected_hashes()
    if hashes["results/calibration/test/ebm_seed42_calibrated.csv"] != EXPECTED_TEST_CAL_SHA256:
        issues.append("TEST calibrated CSV SHA-256 mismatch.")
    if hashes["results/decision/v2/frozen_policy.json"] != EXPECTED_V2_FREEZE_SHA256:
        issues.append("Stage 8 v2 freeze SHA-256 mismatch.")
    if hashes["results/decision/v2/tables/table3_test_decision_outcomes.csv"] != EXPECTED_TABLE3_SHA256:
        issues.append("table3 SHA-256 mismatch.")

    frame = pd.read_csv(
        TEST_CAL,
        usecols=["row_ref", "split", "year", "y_true", "p_selected", "selected_method"],
    )
    n = int(len(frame))
    years = frame["year"].astype(int)
    unique_years = set(int(v) for v in years.unique())
    n_by_year = {int(year): int((years == year).sum()) for year in ALLOWED_YEARS}
    n_year_sum = int(sum(n_by_year.values()))
    unique_rows = int(frame["row_ref"].nunique())
    split_ok = set(frame["split"].astype(str).unique()) == {"test"}
    selected_ok = set(frame["selected_method"].astype(str).unique()) == {"platt"}

    if n != EXPECTED_N:
        issues.append(f"TEST calibrated CSV n={n} != {EXPECTED_N}.")
    if unique_years != set(ALLOWED_YEARS):
        issues.append(f"stored year values {sorted(unique_years)} are not exactly {list(ALLOWED_YEARS)}.")
    if n_year_sum != EXPECTED_N:
        issues.append(f"n_2017+n_2018={n_year_sum} != {EXPECTED_N}.")
    if unique_rows != n:
        issues.append("row_ref is not unique on TEST calibrated CSV.")
    if not split_ok:
        issues.append("Calibrated CSV is not exclusively split=test.")
    if not selected_ok:
        issues.append("selected_method is not exclusively platt.")

    cited_n = stage5_year_n()
    for year in ALLOWED_YEARS:
        if cited_n.get(year) != n_by_year[year]:
            issues.append(
                f"Year {year} n={n_by_year[year]} does not match Stage 5 temporal n={cited_n.get(year)}."
            )

    if issues:
        return json_safe(
            {
                "experiment_id": EXPERIMENT_ID,
                "classification": CLASSIFICATION,
                "status": "ABORTED — year/identity integrity failed",
                "confirmatory_experiment": False,
                "issues": issues,
                "documentation_limitations": documentation_limitations,
                "n": n,
                "n_by_year": n_by_year,
                "s10_i1_status": i1.get("status"),
                "models_trained": False,
                "calibration_refit": False,
                "thresholds_searched": False,
                "year_specific_threshold": False,
                "uci_opened": False,
                "s10_a1_gap_executed": False,
                "s10_a4_executed": False,
            }
        )

    p = frame["p_selected"].to_numpy(dtype=float)
    y = frame["y_true"].to_numpy(dtype=int)
    by_year: dict[int, dict[str, Any]] = {}
    for year in ALLOWED_YEARS:
        mask = years.to_numpy() == year
        by_year[year] = year_slice_payload(year, p[mask], y[mask])
        if by_year[year]["a3_human_review_count"] != 0:
            issues.append(f"A3/A4 produced HUMAN_REVIEW in {year}.")
        if by_year[year]["a1_approve_count"] != 0:
            issues.append(f"A1 produced APPROVE in {year} under constant G0 INSUFFICIENT_INFORMATION.")

    pooled_a0 = sum(by_year[year]["A0"]["APPROVE"]["count"] for year in ALLOWED_YEARS)
    pooled_a0_review = sum(by_year[year]["A0"]["HUMAN_REVIEW"]["count"] for year in ALLOWED_YEARS)
    pooled_a0_reject = sum(by_year[year]["A0"]["REJECT"]["count"] for year in ALLOWED_YEARS)
    pooled_a1_review = sum(by_year[year]["A1"]["HUMAN_REVIEW"]["count"] for year in ALLOWED_YEARS)
    pooled_a3_approve = sum(by_year[year]["A3_A4"]["APPROVE"]["count"] for year in ALLOWED_YEARS)
    if (pooled_a0, pooled_a0_review, pooled_a0_reject) != (5232, 203627, 27):
        issues.append("Year-pooled A0 counts do not match Stage 8 v2 table3.")
    if pooled_a1_review != 208859:
        issues.append("Year-pooled A1 HUMAN_REVIEW does not match Stage 8 v2 table3.")
    if pooled_a3_approve != 61855:
        issues.append("Year-pooled A3 APPROVE does not match Stage 8 v2 table3.")

    if issues:
        status = "ABORTED — year/identity integrity failed"
    else:
        status = "COMPLETED — exploratory/descriptive post-hoc reanalysis"

    return json_safe(
        {
            "experiment_id": EXPERIMENT_ID,
            "classification": CLASSIFICATION,
            "status": status,
            "confirmatory_experiment": False,
            "issues": issues,
            "documentation_limitations": documentation_limitations,
            "s10_i1_status": i1.get("status"),
            "n": n,
            "n_by_year": n_by_year,
            "unique_row_ref": unique_rows,
            "probability_file": TEST_CAL.as_posix(),
            "year_derivation": {
                "used_in_this_run": "stored column `year` in results/calibration/test/ebm_seed42_calibrated.csv",
                "not_recomputed": True,
                "not_parsed_here": ["issue_d", "issue_month"],
                "historical_stage5_source": (
                    "Stage 5 stored year as int(issue_month[0:4]); S10-R1 reads the stored column only."
                ),
                "allowed_years": list(ALLOWED_YEARS),
                "stage5_temporal_n_citation": cited_n,
            },
            "thresholds": {
                "t_low": EXPECTED_T_LOW,
                "t_high": EXPECTED_T_HIGH,
                "t_star": EXPECTED_T_STAR,
                "year_specific_threshold": False,
                "thresholds_searched": False,
            },
            "hashes": hashes,
            "expected_test_cal_sha256": EXPECTED_TEST_CAL_SHA256,
            "by_year": {str(year): by_year[year] for year in ALLOWED_YEARS},
            "decision_mix_rows": decision_mix_rows(by_year),
            "credit_band_rows": credit_band_rows(by_year),
            "descriptive_notes": descriptive_notes(by_year),
            "models_trained": False,
            "models_loaded_for_scoring": False,
            "calibration_refit": False,
            "thresholds_searched": False,
            "year_specific_calibrator": False,
            "uci_opened": False,
            "stage8_9_results_modified": False,
            "s10_i1_modified": False,
            "s10_a1_gap_executed": False,
            "s10_a4_executed": False,
            "random_seed_used": None,
            "stored_prediction_seed": 42,
        }
    )
