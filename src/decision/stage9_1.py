"""Stage 9.1 ablation assembly from frozen Stage 8 artifacts. No retraining. No threshold search."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

EXPERIMENT_ID = "stage9_1_ablation_lc_v1"
EXPECTED_T_LOW = 0.06
EXPECTED_T_HIGH = 0.69
EXPECTED_T_STAR = 0.16
EXPECTED_PLATT_A = 1.1988263209549705
EXPECTED_PLATT_B = 0.6697765046966161
EXPECTED_V1_FREEZE_SHA256 = "4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4"
EXPECTED_TEST_CAL_SHA256 = "e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb"
EXPECTED_A1 = {"APPROVE": 0, "HUMAN_REVIEW": 208859, "REJECT": 27}

V1_FREEZE = ROOT / "results" / "decision" / "frozen_policy.json"
V2_FREEZE = ROOT / "results" / "decision" / "v2" / "frozen_policy.json"
V2_TABLE3 = ROOT / "results" / "decision" / "v2" / "tables" / "table3_test_decision_outcomes.csv"
V2_TABLE3B = ROOT / "results" / "decision" / "v2" / "tables" / "table3b_test_default_rates_by_band.csv"
V2_FUSED = ROOT / "results" / "decision" / "v2" / "metrics" / "fused_test.json"
V2_PRED = ROOT / "results" / "decision" / "v2" / "metrics" / "predictive_test_stage5.json"
V2_AUDIT = ROOT / "audit" / "stage8_v2_decision_fusion_run.json"
MONO_TEST = ROOT / "results" / "decision" / "metrics" / "monolithic_test.json"
PLATT_RECORD = ROOT / "results" / "calibration" / "artifacts" / "platt_record.json"
TEST_CAL = ROOT / "results" / "calibration" / "test" / "ebm_seed42_calibrated.csv"
EBM_JOBLIB = ROOT / "results" / "calibration" / "artifacts" / "ebm_train_only_seed42.joblib"
PLATT_JOBLIB = ROOT / "results" / "calibration" / "artifacts" / "platt_calibrator.joblib"


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return (float("nan"), float("nan"))
    if k < 0 or k > n:
        raise ValueError("Wilson CI requires 0 <= k <= n.")
    p = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    half = z * ((p * (1.0 - p) + z2 / (4.0 * n)) / n) ** 0.5 / denom
    return (max(0.0, center - half), min(1.0, center + half))


def credit_bands(p: np.ndarray, t_low: float, t_high: float) -> np.ndarray:
    p = np.asarray(p, dtype=float)
    out = np.empty(p.shape, dtype=object)
    out[p < t_low] = "LOW"
    out[(p >= t_low) & (p < t_high)] = "MEDIUM"
    out[p >= t_high] = "HIGH"
    return out


def credit_only_decisions(p: np.ndarray, t_low: float, t_high: float) -> np.ndarray:
    bands = credit_bands(p, t_low, t_high)
    out = np.empty(bands.shape, dtype=object)
    out[bands == "LOW"] = "APPROVE"
    out[bands == "MEDIUM"] = "HUMAN_REVIEW"
    out[bands == "HIGH"] = "REJECT"
    return out


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_frozen_artifacts() -> dict[str, Any]:
    required = (
        V1_FREEZE,
        V2_FREEZE,
        V2_TABLE3,
        V2_FUSED,
        V2_PRED,
        V2_AUDIT,
        MONO_TEST,
        PLATT_RECORD,
        EBM_JOBLIB,
        PLATT_JOBLIB,
        TEST_CAL,
    )
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError(f"Frozen artifacts missing: {missing}")
    v1_hash = sha256_file(V1_FREEZE)
    if v1_hash != EXPECTED_V1_FREEZE_SHA256:
        raise RuntimeError(f"Stage 8 v1 freeze hash mismatch: {v1_hash}")
    test_cal_hash = sha256_file(TEST_CAL)
    if test_cal_hash != EXPECTED_TEST_CAL_SHA256:
        raise RuntimeError(f"TEST calibrated-probability hash mismatch: {test_cal_hash}")
    freeze = json.loads(V1_FREEZE.read_text(encoding="utf-8"))
    v2 = json.loads(V2_FREEZE.read_text(encoding="utf-8"))
    platt = json.loads(PLATT_RECORD.read_text(encoding="utf-8"))
    if float(freeze["t_low"]) != EXPECTED_T_LOW or float(freeze["t_high"]) != EXPECTED_T_HIGH:
        raise RuntimeError("Stage 8 v1 thresholds are not 0.06/0.69.")
    if float(v2["t_low"]) != EXPECTED_T_LOW or float(v2["t_high"]) != EXPECTED_T_HIGH:
        raise RuntimeError("Stage 8 v2 thresholds are not 0.06/0.69.")
    if float(v2["monolithic_t"]) != EXPECTED_T_STAR:
        raise RuntimeError("Frozen monolithic t* is not 0.16.")
    if float(platt["a"]) != EXPECTED_PLATT_A or float(platt["b"]) != EXPECTED_PLATT_B:
        raise RuntimeError("Platt parameters do not match the frozen Stage 8 values.")
    if v2.get("thresholds_reselected") is True:
        raise RuntimeError("Stage 8 v2 freeze marked thresholds as reselected.")
    return {
        "v1_freeze_sha256": v1_hash,
        "v2_freeze_sha256": sha256_file(V2_FREEZE),
        "platt_record_sha256": sha256_file(PLATT_RECORD),
        "ebm_joblib_sha256": sha256_file(EBM_JOBLIB),
        "platt_joblib_sha256": sha256_file(PLATT_JOBLIB),
        "t_low": EXPECTED_T_LOW,
        "t_high": EXPECTED_T_HIGH,
        "t_star": EXPECTED_T_STAR,
        "platt_a": EXPECTED_PLATT_A,
        "platt_b": EXPECTED_PLATT_B,
        "test_cal_sha256": test_cal_hash,
    }


def _row(frame: pd.DataFrame, architecture: str) -> dict[str, Any]:
    hits = frame.loc[frame["architecture"].astype(str) == architecture]
    if len(hits) != 1:
        raise RuntimeError(f"Expected one row for architecture={architecture!r}, got {len(hits)}.")
    return hits.iloc[0].to_dict()


def _counts_from_policy_row(row: dict[str, Any]) -> dict[str, int]:
    return {
        "n": int(row["n"]),
        "APPROVE": int(row["n_approve"]),
        "HUMAN_REVIEW": int(row["n_review"]),
        "REJECT": int(row["n_reject"]),
        "n_default_total": int(row["n_positive"]),
    }


def _rate(count: int, n: int) -> float:
    return float(count / n) if n else float("nan")


def _outcome(band: str, n: int, n_default: int) -> dict[str, Any]:
    lo, hi = wilson_ci(n_default, n) if n else (float("nan"), float("nan"))
    return {
        "band": band,
        "n": n,
        "n_default": n_default,
        "default_rate": (n_default / n) if n else float("nan"),
        "default_rate_ci_lower": lo,
        "default_rate_ci_upper": hi,
        "ci_method": "wilson_95",
    }


def load_stored_ablation() -> dict[str, Any]:
    """Assemble A0/A1/A3=A4 from Stage 8 stored TEST-policy tables. No model is called."""
    table3 = pd.read_csv(V2_TABLE3)
    a0 = _counts_from_policy_row(_row(table3, "credit_only_selected_bands"))
    a1 = _counts_from_policy_row(_row(table3, "fused_evidence_separated_v2"))
    a3 = _counts_from_policy_row(_row(table3, "monolithic_credit_threshold"))
    if a1["APPROVE"] != EXPECTED_A1["APPROVE"] or a1["HUMAN_REVIEW"] != EXPECTED_A1["HUMAN_REVIEW"] or a1["REJECT"] != EXPECTED_A1["REJECT"]:
        raise RuntimeError(f"Stored A1 counts {a1} do not match Stage 8 v2 fused result {EXPECTED_A1}.")
    if a3["HUMAN_REVIEW"] != 0:
        raise RuntimeError("Stored monolithic comparator produced HUMAN_REVIEW.")
    if a1["HUMAN_REVIEW"] <= 0:
        raise RuntimeError("Stored A1 lost HUMAN_REVIEW.")
    fused = json.loads(V2_FUSED.read_text(encoding="utf-8"))
    pred = json.loads(V2_PRED.read_text(encoding="utf-8"))
    audit = json.loads(V2_AUDIT.read_text(encoding="utf-8"))
    mono = json.loads(MONO_TEST.read_text(encoding="utf-8"))
    a0_row = _row(table3, "credit_only_selected_bands")
    n = a1["n"]
    systems = {
        "A0": {
            "label": "credit-only three-way",
            "credit_policy": "t_low=0.06, t_high=0.69",
            "governance": "none",
            "notes": "credit-only; HUMAN_REVIEW is the MEDIUM credit band",
            **a0,
            "approval_rate": _rate(a0["APPROVE"], n),
            "review_rate": _rate(a0["HUMAN_REVIEW"], n),
            "rejection_rate": _rate(a0["REJECT"], n),
            "review_burden": _rate(a0["HUMAN_REVIEW"], n),
        },
        "A1": {
            "label": "evidence-separated (proposed)",
            "credit_policy": "t_low=0.06, t_high=0.69",
            "governance": "G0 / L2 INSUFFICIENT_INFORMATION",
            "notes": "proposed architecture; HUMAN_REVIEW retained",
            **a1,
            "approval_rate": _rate(a1["APPROVE"], n),
            "review_rate": _rate(a1["HUMAN_REVIEW"], n),
            "rejection_rate": _rate(a1["REJECT"], n),
            "review_burden": _rate(a1["HUMAN_REVIEW"], n),
        },
        "A3_A4": {
            "label": "binary monolithic comparator",
            "credit_policy": "t*=0.16",
            "governance": "none",
            "notes": "A3 and A4 collapse to the same frozen binary comparator",
            **a3,
            "approval_rate": _rate(a3["APPROVE"], n),
            "review_rate": 0.0,
            "rejection_rate": _rate(a3["REJECT"], n),
            "review_burden": 0.0,
        },
    }
    a0_outcomes = [
        _outcome("APPROVE", int(a0_row["n_approve"]), int(a0_row["fn"])),
        _outcome("HUMAN_REVIEW", int(a0_row["n_review"]), int(a0_row["n_positive"]) - int(a0_row["fn"]) - int(a0_row["tp"])),
        _outcome("REJECT", int(a0_row["n_reject"]), int(a0_row["tp"])),
    ]
    a1_outcomes = list(fused["metrics"]["decision_bands"])
    if int(fused["metrics"]["n_approve"]) == 0 and not any(str(row.get("band")) == "APPROVE" for row in a1_outcomes):
        a1_outcomes = [_outcome("APPROVE", 0, 0)] + a1_outcomes
    a3_outcomes = list(mono["decision_bands"])
    credit_bands = list(fused["credit_bands"])
    return {
        "n": n,
        "systems": systems,
        "a0_outcomes": a0_outcomes,
        "a1_outcomes": a1_outcomes,
        "a3_outcomes": a3_outcomes,
        "a1_credit_bands": credit_bands,
        "a1_governance": dict(audit["gov_counts"]),
        "a1_band_counts": dict(audit["band_counts"]),
        "predictive": pred["artifact"],
        "a3_identical_to_a4": True,
        "source_table3": V2_TABLE3.as_posix(),
    }


def apply_frozen_binary(p: np.ndarray) -> np.ndarray:
    return credit_only_decisions(p, EXPECTED_T_STAR, EXPECTED_T_STAR)


def apply_frozen_credit_only(p: np.ndarray) -> np.ndarray:
    return credit_only_decisions(p, EXPECTED_T_LOW, EXPECTED_T_HIGH)


def consistency_check_stored_probabilities(systems: dict[str, Any]) -> dict[str, Any]:
    """Re-apply frozen A0/A3 maps to stored p_selected. Descriptive re-analysis, not selection."""
    if not TEST_CAL.exists():
        raise FileNotFoundError(f"Missing stored TEST probabilities: {TEST_CAL}")
    cal_hash = sha256_file(TEST_CAL)
    if cal_hash != EXPECTED_TEST_CAL_SHA256:
        raise RuntimeError(f"TEST calibrated-probability hash mismatch: {cal_hash}")
    frame = pd.read_csv(TEST_CAL, usecols=["split", "p_selected"])
    if set(frame["split"].astype(str).unique()) != {"test"}:
        raise RuntimeError("Calibrated file is not the TEST split.")
    p = frame["p_selected"].to_numpy(dtype=float)
    a0 = apply_frozen_credit_only(p)
    a3 = apply_frozen_binary(p)
    a0_counts = {k: int((a0 == k).sum()) for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")}
    a3_counts = {k: int((a3 == k).sum()) for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")}
    stored_a0 = {k: systems["A0"][k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")}
    stored_a3 = {k: systems["A3_A4"][k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")}
    if a0_counts != stored_a0:
        raise RuntimeError(f"A0 re-analysis {a0_counts} != stored {stored_a0}")
    if a3_counts != stored_a3:
        raise RuntimeError(f"A3 re-analysis {a3_counts} != stored {stored_a3}")
    if a3_counts["HUMAN_REVIEW"] != 0:
        raise RuntimeError("A3 re-analysis produced HUMAN_REVIEW.")
    return {
        "label": "descriptive_reanalysis_of_previously_exposed_test_outputs",
        "used_for_selection": False,
        "test_cal_sha256": cal_hash,
        "a0_match": True,
        "a3_match": True,
        "n": int(p.size),
    }
