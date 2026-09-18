"""Stage 8 v2 per-row fusion tests. Synthetic/unit fixtures first; no TEST tuning."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision.audit_record import (  # noqa: E402
    FORBIDDEN_PUBLISHED_KEYS,
    REQUIRED_FIELDS_V2,
    assert_no_raw_identifiers,
    build_record_v2,
    logic_hash_v2,
)
from decision.config_load import YAML_PATH, load_policy_config  # noqa: E402
from decision.decision_engine import apply_policy  # noqa: E402
from decision.policy_matrix import build_matrix  # noqa: E402
from decision.stage8_v2 import (  # noqa: E402
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    FROZEN_DATASET_ID,
    assert_l1_not_confused_with_l2,
    assert_platt_integrity,
    evaluate_row_for_fusion,
    fuse_with_frozen_policy,
    load_frozen_thresholds,
    review_cause,
)
from shariah.l1 import L1_LC_STATUS  # noqa: E402
from shariah.l2 import EVALUATION_MODE_PER_APPLICATION  # noqa: E402

FIXTURES = json.loads((ROOT / "data" / "synthetic" / "lendingclub_l2_schema_fixtures.json").read_text(encoding="utf-8"))
V1_FREEZE = ROOT / "results" / "decision" / "frozen_policy.json"
V1_REPORT = ROOT / "docs" / "STAGE_8_DECISION_POLICY_REPORT.md"
V1_RUNNER = ROOT / "experiments" / "stage8_decision" / "run_stage8.py"
V2_RUNNER = ROOT / "experiments" / "stage8_decision" / "run_stage8_v2.py"
TS = "2026-09-15T00:00:00+00:00"


def _fixture(key: str) -> dict:
    return dict(next(row for row in FIXTURES["fixtures"] if row["_fixture_key"] == key))


def _matrix():
    return build_matrix(load_policy_config(YAML_PATH)["governance_policy"]["matrix"])


def _audit(**overrides):
    payload = dict(
        event_timestamp=TS,
        dataset_id=FROZEN_DATASET_ID,
        dataset_hash="abc",
        record_reference_hash="a" * 64,
        evidence_hash="b" * 64,
        evaluation_mode=EVALUATION_MODE_PER_APPLICATION,
        l1_status=L1_LC_STATUS,
        l1_is_applicant_level_ruling=False,
        missing_evidence=["verified_contract_type"],
        expert_validation_state="NONE_EXPERT_VALIDATED",
        amendment_id="AMENDMENT-SHARIAH-001",
        l1l2_version="stage7-l1l2-v2",
        certification_claim=False,
        model_name="explainable_boosting_machine",
        model_version="stage4b-lc-granting-v1:seed42",
        preprocessor_version="stage4a-0.1.0",
        calibrator_name="platt",
        calibrator_version="stage5-lc-ebm-calibration-v1",
        raw_probability=0.04,
        calibrated_probability=0.05,
        credit_risk_band="LOW",
        top_explanation_features=["fico_n"],
        shariah_evidence_completeness="INSUFFICIENT",
        shariah_governance_status="INSUFFICIENT_INFORMATION",
        triggered_rule_ids=["SH-ARCH-001"],
        rule_source_ids=["SRC-STAGE7-ARCHITECTURE"],
        policy_version="stage8-v2",
        cost_scenario="FN:FP=5:1",
        threshold_configuration={"t_low": EXPECTED_T_LOW, "t_high": EXPECTED_T_HIGH},
        final_decision="HUMAN_REVIEW",
        review_required=True,
    )
    payload.update(overrides)
    return build_record_v2(**payload)


def test_a_per_row_audit_identity() -> None:
    cache: dict[str, dict] = {}
    a = evaluate_row_for_fusion(_fixture("lc-unit-001"), compact_cache=cache, synthetic=True)
    b = evaluate_row_for_fusion(_fixture("lc-unit-003"), compact_cache=cache, synthetic=True)
    assert a["record_reference_hash"] != b["record_reference_hash"]
    assert a["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION
    assert b["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION


def test_b_no_broadcast() -> None:
    cache: dict[str, dict] = {}
    rows = [_fixture("lc-unit-001"), _fixture("lc-unit-002"), _fixture("lc-unit-003")]
    recs = [evaluate_row_for_fusion(row, compact_cache=cache, synthetic=True) for row in rows]
    hashes = [r["record_reference_hash"] for r in recs]
    assert len(set(hashes)) == 3
    assert recs[0]["evidence_hash"] == recs[1]["evidence_hash"]
    assert all(r["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION for r in recs)
    assert "lendingclub-application-profile" not in hashes
    assert recs[0]["record_reference_hash"] != recs[0]["evidence_hash"]


def test_c_l1_l2_distinction() -> None:
    rec = evaluate_row_for_fusion(_fixture("lc-unit-001"), synthetic=True)
    assert rec["l1_status"] == L1_LC_STATUS
    assert rec["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert rec["l1_status"] != rec["overall_governance_status"]
    assert rec["l1_is_applicant_level_ruling"] is False
    assert_l1_not_confused_with_l2(rec)


def test_d_purpose_firewall() -> None:
    row = _fixture("lc-unit-001")
    rec = evaluate_row_for_fusion(row, synthetic=True)
    assert rec["purpose_used_as_contract_type"] is False
    assert "purpose" in rec["firewall_fields_dropped"]
    assert rec["overall_governance_status"] != "Ijarah"
    from shariah.l2 import extract_application_governance_evidence

    ev, meta = extract_application_governance_evidence(row, dataset_id=FROZEN_DATASET_ID, synthetic=True)
    assert "purpose" not in ev.as_dict()
    assert ev.contract_type == "unknown"


def test_e_credit_purpose_distinction() -> None:
    matrix = _matrix()
    freeze = load_frozen_thresholds()
    t_low, t_high = float(freeze["t_low"]), float(freeze["t_high"])
    car = _fixture("lc-unit-001")
    home = _fixture("lc-unit-001")
    home["_fixture_key"] = "purpose-home-only"
    home["id"] = 777
    home["purpose"] = "home_improvement"
    cache: dict[str, dict] = {}
    g_car = evaluate_row_for_fusion(car, compact_cache=cache, synthetic=True)
    g_home = evaluate_row_for_fusion(home, compact_cache=cache, synthetic=True)
    assert g_car["evidence_hash"] == g_home["evidence_hash"]
    assert g_car["overall_governance_status"] == g_home["overall_governance_status"]
    same_p = 0.05
    d_car = fuse_with_frozen_policy(same_p, g_car, t_low=t_low, t_high=t_high, matrix=matrix)
    d_home = fuse_with_frozen_policy(same_p, g_home, t_low=t_low, t_high=t_high, matrix=matrix)
    assert d_car["final_decision"] == d_home["final_decision"]
    different_credit_p = fuse_with_frozen_policy(0.80, g_home, t_low=t_low, t_high=t_high, matrix=matrix)
    assert different_credit_p["final_decision"] != d_home["final_decision"]


def test_f_evidence_insufficiency() -> None:
    rec = evaluate_row_for_fusion(_fixture("lc-unit-001"), synthetic=True)
    assert rec["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert rec["overall_governance_status"] != "PASS"
    assert rec["layer_a"] == "INSUFFICIENT"
    assert "verified_contract_type" in rec["missing_evidence"]


def test_g_certification_boundary() -> None:
    rec = evaluate_row_for_fusion(_fixture("lc-unit-001"), synthetic=True)
    fused = fuse_with_frozen_policy(0.05, rec, t_low=EXPECTED_T_LOW, t_high=EXPECTED_T_HIGH, matrix=_matrix())
    assert rec["certification_claim"] is False
    assert fused["certification_claim"] is False
    assert fused["final_decision"] != "Shariah compliant"
    audit = _audit(final_decision=fused["final_decision"])
    dumped = json.dumps(audit, ensure_ascii=True).lower()
    assert "shariah compliant" not in dumped
    with pytest.raises(ValueError, match="certification"):
        _audit(certification_claim=True)


def test_h_synthetic_fusion_cases() -> None:
    matrix = _matrix()
    rec = evaluate_row_for_fusion(_fixture("lc-unit-001"), synthetic=True)
    low = fuse_with_frozen_policy(0.05, rec, t_low=EXPECTED_T_LOW, t_high=EXPECTED_T_HIGH, matrix=matrix)
    high = fuse_with_frozen_policy(0.70, rec, t_low=EXPECTED_T_LOW, t_high=EXPECTED_T_HIGH, matrix=matrix)
    assert rec["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert low["final_decision"] == "HUMAN_REVIEW"
    assert high["final_decision"] == "REJECT"
    pass_low = fuse_decision_status("PASS", 0.05, matrix)
    assert pass_low == "APPROVE"
    nsr_low = fuse_decision_status("NOT_STRUCTURABLE_WITHOUT_REDESIGN", 0.05, matrix)
    assert nsr_low == "REJECT"
    review_med = fuse_decision_status("REVIEW", 0.20, matrix)
    assert review_med == "HUMAN_REVIEW"
    missing = fuse_decision_status(None, 0.05, matrix)
    assert missing == "HUMAN_REVIEW"


def fuse_decision_status(status, p, matrix) -> str:
    from decision.decision_engine import fuse_decision

    return fuse_decision(p, status, EXPECTED_T_LOW, EXPECTED_T_HIGH, matrix)["final_decision"]


def test_i_audit_completeness() -> None:
    rec = _audit()
    for field in REQUIRED_FIELDS_V2:
        assert field in rec
    assert rec["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION
    later = _audit(event_timestamp="2026-12-31T00:00:00+00:00")
    assert logic_hash_v2(rec) == logic_hash_v2(later)
    assert rec["decision_id"] == later["decision_id"]
    with pytest.raises(ValueError, match="applicant-level"):
        _audit(l1_is_applicant_level_ruling=True)
    with pytest.raises(ValueError, match="PER_APPLICATION"):
        _audit(evaluation_mode="BROADCAST")
    assert_no_raw_identifiers(rec)
    for key in FORBIDDEN_PUBLISHED_KEYS:
        assert key not in rec


def test_j_historical_preservation() -> None:
    assert V1_REPORT.exists()
    freeze = json.loads(V1_FREEZE.read_text(encoding="utf-8"))
    assert freeze["policy_version"] == "stage8-v1"
    assert freeze["t_low"] == EXPECTED_T_LOW
    assert freeze["t_high"] == EXPECTED_T_HIGH
    v1_text = V1_RUNNER.read_text(encoding="utf-8")
    assert "evaluate_lendingclub_governance" in v1_text
    assert "stage8-lc-decision-v1" in v1_text


def test_k_frozen_threshold_integrity() -> None:
    freeze = load_frozen_thresholds()
    assert freeze["t_low"] == EXPECTED_T_LOW
    assert freeze["t_high"] == EXPECTED_T_HIGH
    assert freeze["policy_type"] == "two_threshold"
    bands = apply_policy(np.array([0.059, 0.06, 0.68, 0.69]), "PASS", EXPECTED_T_LOW, EXPECTED_T_HIGH, _matrix())
    assert list(bands["credit_risk_band"]) == ["LOW", "MEDIUM", "MEDIUM", "HIGH"]


def test_l_frozen_credit_probability_integrity() -> None:
    platt = assert_platt_integrity()
    freeze = load_frozen_thresholds()
    assert platt["a"] == freeze["platt"]["a"]
    assert platt["b"] == freeze["platt"]["b"]
    cal = ROOT / "results" / "calibration" / "test" / "ebm_seed42_calibrated.csv"
    assert cal.exists()
    header = cal.read_text(encoding="utf-8").splitlines()[0]
    assert "p_selected" in header


def test_v2_runner_does_not_reselect_or_retrain() -> None:
    text = V2_RUNNER.read_text(encoding="utf-8")
    assert "select_policy(" not in text
    assert "PlattCalibrator" not in text
    assert "ebm_model" not in text
    assert "dump_json(FREEZE_PATH" in text
    assert "load_test_after_freeze" in text or "load_split_predictions(TEST_CAL" in text


V2_FREEZE = ROOT / "results" / "decision" / "v2" / "frozen_policy.json"
V2_AUDIT = ROOT / "audit" / "stage8_v2_decision_fusion_run.json"


@pytest.mark.skipif(not V2_FREEZE.exists(), reason="Stage 8 v2 freeze not written yet")
def test_v2_freeze_reuses_v1_thresholds() -> None:
    v1 = json.loads(V1_FREEZE.read_text(encoding="utf-8"))
    v2 = json.loads(V2_FREEZE.read_text(encoding="utf-8"))
    assert v2["t_low"] == v1["t_low"] == EXPECTED_T_LOW
    assert v2["t_high"] == v1["t_high"] == EXPECTED_T_HIGH
    assert v2["thresholds_reselected"] is False
    assert v2["selection_split"] == "validation"
    assert v2["policy_version"] == "stage8-v2"
    assert v1["policy_version"] == "stage8-v1"


@pytest.mark.skipif(not V2_AUDIT.exists(), reason="Stage 8 v2 audit not written yet")
def test_v2_audit_no_broadcast_and_no_certification() -> None:
    audit = json.loads(V2_AUDIT.read_text(encoding="utf-8"))
    assert audit["l1_is_applicant_level_ruling"] is False
    assert audit["l2_evaluation_mode"] == "PER_APPLICATION"
    assert audit["n_unique_record_hashes"] == audit["n_test"]
    assert audit["any_expert_validated"] is False
    assert audit["certification_claim_policy"] is False
    assert audit["thresholds_reselected"] is False
    assert audit["stage9"] == "BLOCKED"


def test_review_cause_labels() -> None:
    assert review_cause("LOW", "INSUFFICIENT_INFORMATION", "HUMAN_REVIEW") == "governance_insufficiency"
    assert (
        review_cause("MEDIUM", "INSUFFICIENT_INFORMATION", "HUMAN_REVIEW")
        == "governance_insufficiency_and_credit_uncertainty"
    )
    assert review_cause("HIGH", "INSUFFICIENT_INFORMATION", "REJECT") is None
    assert review_cause("LOW", "PASS", "APPROVE") is None
