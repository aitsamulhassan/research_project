"""S10-A1-GAP: analysis-only descriptive decomposition of frozen A1/G0 allocation.

Not a confirmatory experiment. Does not retrain, refit, search thresholds, or alter G0.
Does not treat G1/G3 as observed. Does not fabricate contractual evidence.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from decision.config_load import YAML_PATH, load_policy_config
from decision.policy_matrix import CREDIT_BANDS, GOVERNANCE_STATUSES, build_matrix, lookup
from decision.stage9_1 import (
    EXPECTED_A1,
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_TEST_CAL_SHA256,
    EXPECTED_V1_FREEZE_SHA256,
    TEST_CAL,
    V1_FREEZE,
    V2_AUDIT,
    V2_FREEZE,
    V2_TABLE3,
    sha256_file,
)
from stage10.s10_i1_identity import (
    EXPECTED_N,
    EXPECTED_TABLE3_SHA256,
    EXPECTED_V2_FREEZE_SHA256,
    V2_AUDIT_RECORDS,
)

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_ID = "s10_a1_gap_v1"
CLASSIFICATION = "ANALYSIS-ONLY / DESCRIPTIVE"
EXPECTED_BANDS = {"LOW": 5232, "MEDIUM": 203627, "HIGH": 27}
EXPECTED_REVIEW_CAUSES = {
    "governance_insufficiency": 5232,
    "governance_insufficiency_and_credit_uncertainty": 203627,
}
L1_STATUS = "INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION"
L2_OBSERVED = "INSUFFICIENT_INFORMATION"
I1_METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json"
R1_METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_r1_year.json"
STAGE7_REPORT = ROOT / "docs" / "STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md"
STAGE8_REPORT = ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md"


def json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    return obj


def pct(count: int, n: int) -> float:
    return (100.0 * count / n) if n else float("nan")


def g0_matrix() -> dict[tuple[str, str], str]:
    config = load_policy_config(YAML_PATH)
    rows = config["governance_policy"]["matrix"]
    return build_matrix(rows)


def require_prior_gates() -> dict[str, Any]:
    if not I1_METRICS.exists():
        raise RuntimeError("S10-A1-GAP aborted: S10-I1 metrics missing.")
    if not R1_METRICS.exists():
        raise RuntimeError("S10-A1-GAP aborted: S10-R1 metrics missing.")
    i1 = json.loads(I1_METRICS.read_text(encoding="utf-8"))
    r1 = json.loads(R1_METRICS.read_text(encoding="utf-8"))
    if i1.get("issues"):
        raise RuntimeError(f"S10-A1-GAP aborted: S10-I1 issues {i1['issues']}.")
    if not str(i1.get("status") or "").startswith("PASS"):
        raise RuntimeError(f"S10-A1-GAP aborted: S10-I1 status={i1.get('status')!r}.")
    if r1.get("issues"):
        raise RuntimeError(f"S10-A1-GAP aborted: S10-R1 issues {r1['issues']}.")
    if not str(r1.get("status") or "").startswith("COMPLETED"):
        raise RuntimeError(f"S10-A1-GAP aborted: S10-R1 status={r1.get('status')!r}.")
    return {"i1_status": i1.get("status"), "r1_status": r1.get("status")}


def published_stage8() -> dict[str, Any]:
    audit = json.loads(V2_AUDIT.read_text(encoding="utf-8"))
    table3 = pd.read_csv(V2_TABLE3)
    a1_row = table3.loc[table3["architecture"].astype(str) == "fused_evidence_separated_v2"].iloc[0]
    return {
        "n": int(audit["n_test"]),
        "band_counts": {str(k): int(v) for k, v in audit["band_counts"].items()},
        "gov_counts": {str(k): int(v) for k, v in audit["gov_counts"].items()},
        "fused_counts": {str(k): int(v) for k, v in audit["fused_counts"].items()},
        "review_causes": {str(k): int(v) for k, v in audit["review_causes"].items()},
        "l1_status": audit["l1_status"],
        "l1_is_applicant_level_ruling": bool(audit["l1_is_applicant_level_ruling"]),
        "l2_evaluation_mode": audit["l2_evaluation_mode"],
        "any_expert_validated": bool(audit["any_expert_validated"]),
        "certification_claim_policy": bool(audit["certification_claim_policy"]),
        "n_unique_evidence_hashes": int(audit["n_unique_evidence_hashes"]),
        "n_unique_record_hashes": int(audit["n_unique_record_hashes"]),
        "t_low": float(audit["t_low"]),
        "t_high": float(audit["t_high"]),
        "table3_a1": {
            "APPROVE": int(a1_row["n_approve"]),
            "HUMAN_REVIEW": int(a1_row["n_review"]),
            "REJECT": int(a1_row["n_reject"]),
            "n": int(a1_row["n"]),
        },
        "v1_freeze_sha256_recorded": audit.get("v1_freeze_sha256"),
        "test_cal_sha256_recorded": audit.get("test_cal_sha256"),
    }


def verify_audit_records(matrix: dict[tuple[str, str], str]) -> dict[str, Any]:
    if not V2_AUDIT_RECORDS.exists():
        raise RuntimeError("Missing Stage 8 v2 per-row audit records.")
    frame = pd.read_csv(
        V2_AUDIT_RECORDS,
        usecols=["credit_risk_band", "shariah_governance_status", "final_decision", "l1_status"],
    )
    n = int(len(frame))
    band_counts = {str(k): int(v) for k, v in frame["credit_risk_band"].astype(str).value_counts().items()}
    gov_counts = {
        str(k): int(v) for k, v in frame["shariah_governance_status"].astype(str).value_counts().items()
    }
    l1_counts = {str(k): int(v) for k, v in frame["l1_status"].astype(str).value_counts().items()}
    decision_counts = {str(k): int(v) for k, v in frame["final_decision"].astype(str).value_counts().items()}
    crosstab_counter: Counter[tuple[str, str]] = Counter(
        zip(
            frame["credit_risk_band"].astype(str).tolist(),
            frame["shariah_governance_status"].astype(str).tolist(),
            strict=True,
        )
    )
    combo_counter: Counter[tuple[str, str, str]] = Counter(
        zip(
            frame["credit_risk_band"].astype(str).tolist(),
            frame["shariah_governance_status"].astype(str).tolist(),
            frame["final_decision"].astype(str).tolist(),
            strict=True,
        )
    )
    g0_mismatches = []
    for (band, status, decision), count in combo_counter.items():
        expected = lookup(matrix, status, band)
        if expected != decision:
            g0_mismatches.append(
                {
                    "credit_band": band,
                    "l2_status": status,
                    "stored_decision": decision,
                    "g0_lookup": expected,
                    "n": int(count),
                }
            )
    return {
        "n": n,
        "band_counts": band_counts,
        "gov_counts": gov_counts,
        "l1_counts": l1_counts,
        "decision_counts": decision_counts,
        "crosstab_counter": {f"{b}|{g}": int(c) for (b, g), c in crosstab_counter.items()},
        "combo_counter": combo_counter,
        "g0_mismatches": g0_mismatches,
        "missing_row_ref": True,
    }


def full_crosstab(counter: Counter[tuple[str, str]]) -> list[dict[str, Any]]:
    matrix = g0_matrix()
    rows: list[dict[str, Any]] = []
    for band in CREDIT_BANDS:
        for status in GOVERNANCE_STATUSES:
            n_cell = int(counter.get((band, status), 0))
            decision = lookup(matrix, status, band)
            rows.append(
                {
                    "credit_band": band,
                    "l2_governance_status": status,
                    "n": n_cell,
                    "percentage_of_test": pct(n_cell, EXPECTED_N),
                    "g0_decision": decision,
                    "populated": n_cell > 0,
                }
            )
    return rows


def policy_trace(crosstab_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    band_rule = {
        "LOW": "p_selected < 0.06",
        "MEDIUM": "0.06 <= p_selected < 0.69",
        "HIGH": "p_selected >= 0.69",
    }
    traces = []
    for row in crosstab_rows:
        if not row["populated"]:
            continue
        traces.append(
            {
                "p_selected_rule": band_rule[row["credit_band"]],
                "credit_band": row["credit_band"],
                "l2_governance_status": row["l2_governance_status"],
                "g0_mapping": f"G0[{row['l2_governance_status']}, {row['credit_band']}] = {row['g0_decision']}",
                "final_a1_decision": row["g0_decision"],
                "n": row["n"],
            }
        )
    return traces


def decomposition(crosstab_rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_band = {row["credit_band"]: row for row in crosstab_rows if row["l2_governance_status"] == L2_OBSERVED}
    low = int(by_band["LOW"]["n"])
    medium = int(by_band["MEDIUM"]["n"])
    high = int(by_band["HIGH"]["n"])
    review = low + medium
    reject = high
    approve = 0
    return {
        "n": EXPECTED_N,
        "a1_approve": approve,
        "a1_review": review,
        "a1_reject": reject,
        "review_rate": review / EXPECTED_N,
        "low_to_review": {
            "n": low,
            "share_of_test": low / EXPECTED_N,
            "share_of_a1_review": low / review,
            "stage8_review_cause": "governance_insufficiency",
            "meaning": "LOW would be A0 APPROVE; G0 + INSUFFICIENT_INFORMATION maps LOW to HUMAN_REVIEW.",
        },
        "medium_to_review": {
            "n": medium,
            "share_of_test": medium / EXPECTED_N,
            "share_of_a1_review": medium / review,
            "stage8_review_cause": "governance_insufficiency_and_credit_uncertainty",
            "meaning": "MEDIUM is already HUMAN_REVIEW on credit; G0 keeps HUMAN_REVIEW.",
        },
        "high_to_review": {
            "n": 0,
            "share_of_test": 0.0,
            "share_of_a1_review": 0.0,
            "meaning": "HIGH does not contribute to A1 HUMAN_REVIEW.",
        },
        "high_to_reject": {
            "n": reject,
            "share_of_test": reject / EXPECTED_N,
            "share_of_a1_reject": 1.0,
            "meaning": "HIGH + INSUFFICIENT_INFORMATION maps to REJECT under G0 (same REJECT count as A0).",
        },
        "approve_identity": (
            "A1 APPROVE requires G0(PASS, LOW). Observed PASS n=0, so A1 APPROVE=0. "
            "Algebra: A1 APPROVE - A0 APPROVE = -LOW = -5232."
        ),
        "review_identity": "A1 HUMAN_REVIEW = LOW + MEDIUM = 5232 + 203627 = 208859.",
        "reject_identity": "A1 REJECT = HIGH = 27.",
    }


def run_gap_analysis() -> dict[str, Any]:
    issues: list[str] = []
    documentation_limitations: list[str] = [
        "Stage 8 v2 per-row audit records have no row_ref; band × L2 identity uses stored Stage 8 columns, not a keyed join to p_selected.",
        "LendingClub schema does not contain contractual Shariah evidence; this analysis does not invent it.",
        "S10-A1-GAP is analysis-only / descriptive. It does not independently validate the governance layer.",
    ]
    try:
        gates = require_prior_gates()
    except RuntimeError as exc:
        return json_safe(
            {
                "experiment_id": EXPERIMENT_ID,
                "classification": CLASSIFICATION,
                "status": "ABORTED — prior Stage 10 gate failed",
                "confirmatory_experiment": False,
                "issues": [str(exc)],
                "documentation_limitations": documentation_limitations,
                "models_trained": False,
                "s10_a4_executed": False,
            }
        )

    matrix = g0_matrix()
    published = published_stage8()
    live_v1 = sha256_file(V1_FREEZE)
    live_v2 = sha256_file(V2_FREEZE)
    live_table3 = sha256_file(V2_TABLE3)
    live_cal = sha256_file(TEST_CAL)
    live_yaml = sha256_file(YAML_PATH)

    if published["n"] != EXPECTED_N:
        issues.append(f"Published n={published['n']} != {EXPECTED_N}.")
    if published["band_counts"] != EXPECTED_BANDS:
        issues.append(f"Published bands {published['band_counts']} != {EXPECTED_BANDS}.")
    if published["gov_counts"] != {L2_OBSERVED: EXPECTED_N}:
        issues.append(f"Published L2 distribution {published['gov_counts']} is not all {L2_OBSERVED}.")
    if published["fused_counts"] != EXPECTED_A1:
        issues.append(f"Published A1 fused counts {published['fused_counts']} != {EXPECTED_A1}.")
    if published["table3_a1"] != {**EXPECTED_A1, "n": EXPECTED_N}:
        issues.append(f"table3 A1 {published['table3_a1']} != expected.")
    if published["review_causes"] != EXPECTED_REVIEW_CAUSES:
        issues.append(f"Published review_causes {published['review_causes']} != {EXPECTED_REVIEW_CAUSES}.")
    if published["l1_status"] != L1_STATUS:
        issues.append("Published L1 status is not INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION.")
    if published["t_low"] != EXPECTED_T_LOW or published["t_high"] != EXPECTED_T_HIGH:
        issues.append("Published thresholds are not 0.06/0.69.")
    documentation_limitations.append(
        f"Stage 8 v2 recorded n_unique_evidence_hashes={published['n_unique_evidence_hashes']} "
        f"and n_unique_record_hashes={published['n_unique_record_hashes']}: "
        "per-row record hashes are unique, but the governance evidence object is identical across TEST rows."
    )
    if live_v1 != EXPECTED_V1_FREEZE_SHA256:
        issues.append("Stage 8 v1 freeze SHA-256 mismatch.")
    if live_v2 != EXPECTED_V2_FREEZE_SHA256:
        issues.append("Stage 8 v2 freeze SHA-256 mismatch.")
    if live_table3 != EXPECTED_TABLE3_SHA256:
        issues.append("table3 SHA-256 mismatch.")
    if live_cal != EXPECTED_TEST_CAL_SHA256:
        issues.append("TEST calibrated CSV SHA-256 mismatch.")

    verified = verify_audit_records(matrix)
    if verified["n"] != EXPECTED_N:
        issues.append(f"Audit records n={verified['n']} != {EXPECTED_N}.")
    if verified["band_counts"] != EXPECTED_BANDS:
        issues.append(f"Stored audit band counts {verified['band_counts']} != {EXPECTED_BANDS}.")
    if verified["gov_counts"] != {L2_OBSERVED: EXPECTED_N}:
        issues.append(f"Stored audit L2 counts {verified['gov_counts']} are not all {L2_OBSERVED}.")
    if verified["l1_counts"] != {L1_STATUS: EXPECTED_N}:
        issues.append(f"Stored audit L1 counts {verified['l1_counts']} != all {L1_STATUS}.")
    stored_decisions = {k: int(verified["decision_counts"].get(k, 0)) for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")}
    if stored_decisions != EXPECTED_A1:
        issues.append(f"Stored audit A1 decisions {stored_decisions} != {EXPECTED_A1}.")
    if verified["g0_mismatches"]:
        issues.append(f"Stored final_decision disagrees with frozen G0 lookup: {verified['g0_mismatches']}")

    combo = verified["combo_counter"]
    band_status_counter: Counter[tuple[str, str]] = Counter()
    for (band, status, _dec), count in combo.items():
        band_status_counter[(band, status)] += int(count)
    crosstab_rows = full_crosstab(band_status_counter)
    traces = policy_trace(crosstab_rows)
    decomp = decomposition(crosstab_rows)

    if decomp["a1_review"] != 208859 or decomp["a1_reject"] != 27 or decomp["a1_approve"] != 0:
        issues.append("Algebraic A1 decomposition does not equal 0 / 208859 / 27.")

    status = (
        "ABORTED — published/stored A1 decomposition mismatch"
        if issues
        else "COMPLETED — analysis-only descriptive decomposition"
    )
    l2_rows = [
        {
            "l2_governance_status": status_name,
            "count": int(verified["gov_counts"].get(status_name, 0)),
            "percentage_of_test": pct(int(verified["gov_counts"].get(status_name, 0)), EXPECTED_N),
            "observed_on_lc_test": status_name == L2_OBSERVED,
        }
        for status_name in GOVERNANCE_STATUSES
    ]
    band_rows = [
        {
            "credit_band": band,
            "count": int(EXPECTED_BANDS[band]),
            "percentage_of_test": pct(EXPECTED_BANDS[band], EXPECTED_N),
            "rule": {
                "LOW": "p_selected < 0.06",
                "MEDIUM": "0.06 <= p_selected < 0.69",
                "HIGH": "p_selected >= 0.69",
            }[band],
        }
        for band in CREDIT_BANDS
    ]
    return json_safe(
        {
            "experiment_id": EXPERIMENT_ID,
            "classification": CLASSIFICATION,
            "status": status,
            "confirmatory_experiment": False,
            "issues": issues,
            "documentation_limitations": documentation_limitations,
            "prior_gates": gates,
            "n": EXPECTED_N,
            "thresholds": {"t_low": EXPECTED_T_LOW, "t_high": EXPECTED_T_HIGH, "unchanged": True},
            "credit_bands": band_rows,
            "l2_governance_states": l2_rows,
            "l1": {
                "status": L1_STATUS,
                "is_applicant_level_ruling": False,
                "count": EXPECTED_N,
                "note": "L1 is dataset/schema readiness, not an applicant-level Shariah ruling, and is not the G0 matrix input.",
            },
            "crosstab": crosstab_rows,
            "policy_trace": traces,
            "decomposition": decomp,
            "g1_g3_treated_as_observed": False,
            "shariah_score_created": False,
            "contracts_fabricated": False,
            "halal_haram_inferred": False,
            "p_selected_source": TEST_CAL.as_posix(),
            "p_selected_rescored": False,
            "year_derivation": None,
            "hashes": {
                "v1_freeze_sha256": live_v1,
                "v2_freeze_sha256": live_v2,
                "table3_sha256": live_table3,
                "test_cal_sha256": live_cal,
                "stage8_policy_yaml_sha256": live_yaml,
                "expected_v1": EXPECTED_V1_FREEZE_SHA256,
                "expected_v2": EXPECTED_V2_FREEZE_SHA256,
                "expected_table3": EXPECTED_TABLE3_SHA256,
                "expected_test_cal": EXPECTED_TEST_CAL_SHA256,
            },
            "source_artifacts": [
                V2_AUDIT.as_posix(),
                V2_TABLE3.as_posix(),
                V2_AUDIT_RECORDS.as_posix(),
                YAML_PATH.as_posix(),
                V1_FREEZE.as_posix(),
                V2_FREEZE.as_posix(),
                TEST_CAL.as_posix(),
                STAGE7_REPORT.as_posix(),
                STAGE8_REPORT.as_posix(),
                I1_METRICS.as_posix(),
                R1_METRICS.as_posix(),
            ],
            "published": published,
            "models_trained": False,
            "models_loaded_for_scoring": False,
            "calibration_refit": False,
            "thresholds_searched": False,
            "uci_opened": False,
            "stage8_9_results_modified": False,
            "s10_i1_modified": False,
            "s10_r1_modified": False,
            "s10_a4_executed": False,
            "random_seed_used": None,
        }
    )
