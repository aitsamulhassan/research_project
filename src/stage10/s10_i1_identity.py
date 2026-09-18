"""S10-I1-IDENTITY: integrity/provenance check on frozen LC TEST p_selected.

Not a scientific confirmatory experiment. Does not retrain, refit, or search thresholds.
Does not load EBM or Platt joblib objects for scoring.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from decision.stage9_1 import (
    EXPECTED_A1,
    EXPECTED_PLATT_A,
    EXPECTED_PLATT_B,
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_T_STAR,
    EXPECTED_TEST_CAL_SHA256,
    EXPECTED_V1_FREEZE_SHA256,
    PLATT_RECORD,
    TEST_CAL,
    V1_FREEZE,
    V2_FREEZE,
    V2_TABLE3,
    apply_frozen_binary,
    apply_frozen_credit_only,
    credit_bands,
    load_stored_ablation,
    sha256_file,
    verify_frozen_artifacts,
)

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_ID = "s10_i1_identity_v1"
EXPECTED_N = 208886
EXPECTED_V2_FREEZE_SHA256 = "b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b"
EXPECTED_TABLE3_SHA256 = "90759eb72f1173b40b5b9363c21b0ef3d6f1cde5042748eb57871d49fb73d5ee"
V2_AUDIT_RECORDS = ROOT / "results" / "decision" / "v2" / "audit" / "test_audit_records.csv"
STAGE9_4_AUDIT = ROOT / "audit" / "stage9_4_uci_run.json"
STATUS_PASS = "PASS — identity/provenance verified"
STATUS_PASS_DOC = "PASS WITH DOCUMENTATION LIMITATION"
STATUS_FAIL = "FAIL — mismatch detected"

G0_INSUFFICIENT = {"LOW": "HUMAN_REVIEW", "MEDIUM": "HUMAN_REVIEW", "HIGH": "REJECT"}


def _counts(decisions: np.ndarray) -> dict[str, int]:
    return {k: int((decisions == k).sum()) for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")}


def _band_counts(bands: np.ndarray) -> dict[str, int]:
    return {k: int((bands == k).sum()) for k in ("LOW", "MEDIUM", "HIGH")}


def g0_from_bands(bands: np.ndarray) -> np.ndarray:
    out = np.empty(bands.shape, dtype=object)
    for band, decision in G0_INSUFFICIENT.items():
        out[bands == band] = decision
    return out


def live_protected_hashes() -> dict[str, str]:
    return {
        "results/decision/frozen_policy.json": sha256_file(V1_FREEZE),
        "results/decision/v2/frozen_policy.json": sha256_file(V2_FREEZE),
        "results/decision/v2/tables/table3_test_decision_outcomes.csv": sha256_file(V2_TABLE3),
        "results/calibration/test/ebm_seed42_calibrated.csv": sha256_file(TEST_CAL),
    }


def _posix(path: str) -> str:
    return path.replace("\\", "/")


def compare_to_stage9_4_protection(live: dict[str, str]) -> dict[str, Any]:
    """Match live relative paths to Stage 9.4 absolute keys by suffix, not basename.

    v1 and v2 both use frozen_policy.json; basename matching would collide.
    """
    payload = json.loads(STAGE9_4_AUDIT.read_text(encoding="utf-8"))
    after = payload["protected_hashes_after"]
    checks = {}
    for rel, digest in live.items():
        rel_posix = _posix(rel)
        expected = None
        matched_key = None
        for key, value in after.items():
            key_posix = _posix(key)
            if key_posix.endswith("/" + rel_posix) or key_posix.endswith(rel_posix):
                expected = value
                matched_key = key
                break
        checks[rel] = {
            "live": digest,
            "stage9_4_protected_after": expected,
            "matched_key": matched_key,
            "match": expected == digest,
        }
    return {
        "all_match": all(row["match"] for row in checks.values()),
        "checks": checks,
    }


def classify_status(issues: list[str], documentation_limitations: list[str]) -> str:
    if issues:
        return STATUS_FAIL
    if documentation_limitations:
        return STATUS_PASS_DOC
    return STATUS_PASS


def run_identity_check() -> dict[str, Any]:
    issues: list[str] = []
    documentation_limitations: list[str] = []
    try:
        integrity = verify_frozen_artifacts()
    except (FileNotFoundError, RuntimeError) as exc:
        integrity = {"error": str(exc)}
        issues.append(str(exc))
    stored = load_stored_ablation()
    live_hashes = live_protected_hashes()
    if live_hashes["results/decision/frozen_policy.json"] != EXPECTED_V1_FREEZE_SHA256:
        issues.append("Stage 8 v1 freeze SHA-256 mismatch.")
    if live_hashes["results/decision/v2/frozen_policy.json"] != EXPECTED_V2_FREEZE_SHA256:
        issues.append("Stage 8 v2 freeze SHA-256 mismatch.")
    if live_hashes["results/decision/v2/tables/table3_test_decision_outcomes.csv"] != EXPECTED_TABLE3_SHA256:
        issues.append("table3 SHA-256 mismatch.")
    if live_hashes["results/calibration/test/ebm_seed42_calibrated.csv"] != EXPECTED_TEST_CAL_SHA256:
        issues.append("TEST calibrated CSV SHA-256 mismatch.")

    cal = pd.read_csv(
        TEST_CAL,
        usecols=["row_ref", "split", "p_raw", "p_platt", "p_selected", "selected_method"],
    )
    n = int(len(cal))
    split_ok = set(cal["split"].astype(str).unique()) == {"test"}
    selected_ok = set(cal["selected_method"].astype(str).unique()) == {"platt"}
    p_selected = cal["p_selected"].to_numpy(dtype=float)
    p_platt = cal["p_platt"].to_numpy(dtype=float)
    p_raw = cal["p_raw"].to_numpy(dtype=float)
    p_selected_equals_platt = bool(np.allclose(p_selected, p_platt, rtol=0.0, atol=0.0))
    p_selected_not_raw = bool(not np.allclose(p_selected, p_raw, rtol=0.0, atol=0.0))
    unique_rows = int(cal["row_ref"].nunique()) if "row_ref" in cal.columns else None
    duplicate_row_ref = bool(unique_rows is not None and unique_rows != n)

    if stored["n"] != EXPECTED_N:
        issues.append(f"Stored table3 n={stored['n']} != {EXPECTED_N}.")
    if n != EXPECTED_N:
        issues.append(f"TEST calibrated CSV n={n} != {EXPECTED_N}.")
    if not split_ok:
        issues.append("Calibrated CSV is not exclusively split=test.")
    if not selected_ok:
        issues.append("selected_method is not exclusively platt.")
    if not p_selected_equals_platt:
        issues.append("p_selected is not identical to stored p_platt.")
    if duplicate_row_ref:
        issues.append("row_ref is not unique on TEST calibrated CSV.")

    a0 = apply_frozen_credit_only(p_selected)
    a3 = apply_frozen_binary(p_selected)
    bands = credit_bands(p_selected, EXPECTED_T_LOW, EXPECTED_T_HIGH)
    a1_from_g0 = g0_from_bands(bands)
    a0_counts = _counts(a0)
    a3_counts = _counts(a3)
    a1_counts = _counts(a1_from_g0)
    band_n = _band_counts(bands)
    stored_a0 = {k: stored["systems"]["A0"][k] for k in a0_counts}
    stored_a1 = {k: stored["systems"]["A1"][k] for k in a1_counts}
    stored_a3 = {k: stored["systems"]["A3_A4"][k] for k in a3_counts}
    stored_bands = {str(k): int(v) for k, v in stored["a1_band_counts"].items()}

    a0_match = a0_counts == stored_a0
    a1_match = a1_counts == stored_a1
    a3_match = a3_counts == stored_a3
    bands_match = band_n == stored_bands
    a3_no_review = a3_counts["HUMAN_REVIEW"] == 0
    a0_a1_same_p = True  # single p_selected vector used for A0 bands and A1 G0 map
    if not a0_match:
        issues.append(f"A0 remap {a0_counts} != stored {stored_a0}.")
    if not a1_match:
        issues.append(f"A1 G0-from-same-bands {a1_counts} != stored {stored_a1}.")
    if not a3_match:
        issues.append(f"A3 remap {a3_counts} != stored {stored_a3}.")
    if not bands_match:
        issues.append(f"Credit bands {band_n} != stored A1 bands {stored_bands}.")
    if not a3_no_review:
        issues.append("A3/A4 remap produced HUMAN_REVIEW.")

    audit_n = None
    audit_p_match = None
    audit_band_match = None
    if V2_AUDIT_RECORDS.exists():
        audit = pd.read_csv(
            V2_AUDIT_RECORDS,
            usecols=["calibrated_probability", "credit_risk_band", "raw_probability"],
        )
        audit_n = int(len(audit))
        if audit_n != n:
            issues.append(f"Stage 8 v2 audit records n={audit_n} != calibrated n={n}.")
        else:
            audit_p = audit["calibrated_probability"].to_numpy(dtype=float)
            audit_raw = audit["raw_probability"].to_numpy(dtype=float)
            # Positional identity: Stage 8 v2 iterated the calibrated TEST file in order.
            audit_p_match = bool(np.allclose(audit_p, p_selected, rtol=0.0, atol=1e-12))
            audit_raw_match = bool(np.allclose(audit_raw, p_raw, rtol=0.0, atol=1e-12))
            audit_band_match = bool(np.array_equal(audit["credit_risk_band"].astype(str).to_numpy(), bands.astype(str)))
            if not audit_raw_match:
                issues.append("Stage 8 v2 audit raw_probability is not aligned with TEST p_raw.")
            if not audit_p_match:
                issues.append("Stage 8 v2 audit calibrated_probability is not aligned with p_selected.")
            if not audit_band_match:
                issues.append("Stage 8 v2 audit credit_risk_band is not aligned with frozen 0.06/0.69 bands.")
        documentation_limitations.append(
            "Stage 8 v2 test_audit_records.csv has no row_ref column; "
            "calibrated_probability vs p_selected identity is positional (calibrated CSV file order), "
            "not a keyed join. This is a provenance documentation limitation, not a count/hash mismatch."
        )
    else:
        issues.append("Missing Stage 8 v2 per-row audit records.")

    hash_vs_94 = compare_to_stage9_4_protection(live_hashes)
    if not hash_vs_94["all_match"]:
        issues.append("Live freeze/TEST hashes do not match Stage 9.4 protected_hashes_after.")

    platt = json.loads(PLATT_RECORD.read_text(encoding="utf-8"))
    v1 = json.loads(V1_FREEZE.read_text(encoding="utf-8"))
    v2 = json.loads(V2_FREEZE.read_text(encoding="utf-8"))
    platt_ok = (
        float(platt["a"]) == EXPECTED_PLATT_A
        and float(platt["b"]) == EXPECTED_PLATT_B
        and float(v1["platt"]["a"]) == EXPECTED_PLATT_A
        and float(v1["platt"]["b"]) == EXPECTED_PLATT_B
        and float(v2["platt"]["a"]) == EXPECTED_PLATT_A
        and float(v2["platt"]["b"]) == EXPECTED_PLATT_B
    )
    if not platt_ok:
        issues.append("Platt a,b mismatch across freeze/record artifacts.")

    status = classify_status(issues, documentation_limitations)
    return {
        "experiment_id": EXPERIMENT_ID,
        "classification": "INTEGRITY / PROVENANCE CHECK — NOT A SCIENTIFIC CONFIRMATORY EXPERIMENT",
        "status": status,
        "issues": issues,
        "documentation_limitations": documentation_limitations,
        "n": n,
        "same_test_rows": n == EXPECTED_N and stored["n"] == EXPECTED_N and (audit_n in (None, EXPECTED_N)),
        "probability_file": TEST_CAL.as_posix(),
        "p_selected_identity": {
            "a0_a1_a3_share_single_p_selected_vector": a0_a1_same_p,
            "p_selected_equals_stored_p_platt": p_selected_equals_platt,
            "p_selected_differs_from_p_raw": p_selected_not_raw,
            "selected_method_platt_only": selected_ok,
            "no_ebm_or_platt_joblib_loaded_for_scoring": True,
            "no_p_selected_recomputed_from_p_raw": True,
        },
        "a0": {
            "t_low": EXPECTED_T_LOW,
            "t_high": EXPECTED_T_HIGH,
            "remap_counts": a0_counts,
            "stored_counts": stored_a0,
            "match": a0_match,
        },
        "a1": {
            "credit_bands_from_same_p_selected": band_n,
            "stored_credit_bands": stored_bands,
            "bands_match": bands_match,
            "g0_insufficient_map": G0_INSUFFICIENT,
            "remap_counts": a1_counts,
            "stored_counts": stored_a1,
            "match": a1_match,
            "expected_a1": EXPECTED_A1,
        },
        "a3_a4": {
            "t_star": EXPECTED_T_STAR,
            "remap_counts": a3_counts,
            "stored_counts": stored_a3,
            "match": a3_match,
            "human_review_branch": False,
            "human_review_count": a3_counts["HUMAN_REVIEW"],
        },
        "row_provenance": {
            "test_cal_n": n,
            "unique_row_ref": unique_rows,
            "split_test_only": split_ok,
            "stage8_v2_audit_n": audit_n,
            "audit_calibrated_matches_p_selected": audit_p_match,
            "audit_bands_match_frozen_map": audit_band_match,
        },
        "hashes": {
            "v1_freeze_sha256": live_hashes["results/decision/frozen_policy.json"],
            "v2_freeze_sha256": live_hashes["results/decision/v2/frozen_policy.json"],
            "table3_sha256": live_hashes["results/decision/v2/tables/table3_test_decision_outcomes.csv"],
            "test_cal_sha256": live_hashes["results/calibration/test/ebm_seed42_calibrated.csv"],
            "expected_v1": EXPECTED_V1_FREEZE_SHA256,
            "expected_v2": EXPECTED_V2_FREEZE_SHA256,
            "expected_table3": EXPECTED_TABLE3_SHA256,
            "expected_test_cal": EXPECTED_TEST_CAL_SHA256,
            "vs_stage9_4_protected_after": hash_vs_94,
        },
        "thresholds": {
            "t_low": EXPECTED_T_LOW,
            "t_high": EXPECTED_T_HIGH,
            "t_star": EXPECTED_T_STAR,
            "v1_t_low": float(v1["t_low"]),
            "v1_t_high": float(v1["t_high"]),
            "v2_t_low": float(v2["t_low"]),
            "v2_t_high": float(v2["t_high"]),
            "v2_monolithic_t": float(v2["monolithic_t"]),
            "thresholds_reselected": v2.get("thresholds_reselected"),
        },
        "platt": {
            "a": EXPECTED_PLATT_A,
            "b": EXPECTED_PLATT_B,
            "record_a": float(platt["a"]),
            "record_b": float(platt["b"]),
            "match": platt_ok,
            "fit_split": platt.get("fit_split"),
        },
        "integrity_from_stage9_1": integrity,
        "models_trained": False,
        "models_loaded_for_scoring": False,
        "calibration_refit": False,
        "thresholds_searched": False,
        "uci_opened": False,
        "stage8_9_results_modified": False,
        "s10_r1_executed": False,
        "s10_a1_gap_executed": False,
        "s10_a4_executed": False,
        "confirmatory_experiment": False,
    }
