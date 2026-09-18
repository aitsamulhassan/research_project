"""Stage 8 decision-policy tests. No EBM/Platt refitting."""

from __future__ import annotations

import hashlib
import inspect
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments" / "stage8_decision"))

from decision.audit_record import (  # noqa: E402
    FORBIDDEN_PUBLISHED_KEYS,
    REQUIRED_FIELDS,
    assert_no_raw_identifiers,
    build_record,
    logic_hash,
)
from decision.cost_policy import CostScenario, expected_normalized_cost  # noqa: E402
from decision.decision_engine import (  # noqa: E402
    apply_policy,
    assert_no_credit_fields_in_governance_payload,
    credit_band,
    evaluate_lendingclub_governance,
    fuse_decision,
    lendingclub_governance_payload,
)
from decision.policy_matrix import build_matrix  # noqa: E402
from decision.threshold_selection import (  # noqa: E402
    assert_validation_split,
    evaluate_thresholds,
    make_threshold_grid,
    select_policy,
)
from evaluation.decision_metrics import wilson_ci  # noqa: E402
from models.ebm_model import ebm_config  # noqa: E402
from preprocessing.lendingclub_preprocessor import FORBIDDEN_COLUMNS, PRIMARY_PREDICTORS  # noqa: E402
from shariah.schema import LENDINGCLUB_PREDICTORS  # noqa: E402

from run_stage8 import load_test_after_freeze  # noqa: E402

MATRIX_ROWS = [
    {"governance": "NOT_STRUCTURABLE_WITHOUT_REDESIGN", "credit_band": "LOW", "decision": "REJECT"},
    {"governance": "NOT_STRUCTURABLE_WITHOUT_REDESIGN", "credit_band": "MEDIUM", "decision": "REJECT"},
    {"governance": "NOT_STRUCTURABLE_WITHOUT_REDESIGN", "credit_band": "HIGH", "decision": "REJECT"},
    {"governance": "INSUFFICIENT_INFORMATION", "credit_band": "LOW", "decision": "HUMAN_REVIEW"},
    {"governance": "INSUFFICIENT_INFORMATION", "credit_band": "MEDIUM", "decision": "HUMAN_REVIEW"},
    {"governance": "INSUFFICIENT_INFORMATION", "credit_band": "HIGH", "decision": "REJECT"},
    {"governance": "REVIEW", "credit_band": "LOW", "decision": "HUMAN_REVIEW"},
    {"governance": "REVIEW", "credit_band": "MEDIUM", "decision": "HUMAN_REVIEW"},
    {"governance": "REVIEW", "credit_band": "HIGH", "decision": "REJECT"},
    {"governance": "PASS", "credit_band": "LOW", "decision": "APPROVE"},
    {"governance": "PASS", "credit_band": "MEDIUM", "decision": "HUMAN_REVIEW"},
    {"governance": "PASS", "credit_band": "HIGH", "decision": "REJECT"},
]
MATRIX = build_matrix(MATRIX_ROWS)
TS = "2026-09-15T00:00:00+00:00"
FREEZE = ROOT / "results" / "decision" / "frozen_policy.json"
PUBLISHED = ROOT / "results" / "decision" / "audit" / "published_examples.json"


def _record(**overrides):
    payload = dict(
        event_timestamp=TS,
        dataset_id="lendingclub_granting_v0.1",
        dataset_hash="abc",
        record_reference_hash="deadbeefcafebabe",
        model_name="explainable_boosting_machine",
        model_version="stage4b-lc-granting-v1:seed42",
        preprocessor_version="stage4a-0.1.0",
        calibrator_name="platt",
        calibrator_version="stage5-lc-ebm-calibration-v1",
        raw_probability=0.2,
        calibrated_probability=0.25,
        credit_risk_band="LOW",
        top_explanation_features=["fico_n", "loan_amnt"],
        shariah_evidence_completeness="INSUFFICIENT",
        shariah_governance_status="INSUFFICIENT_INFORMATION",
        triggered_rule_ids=["SH-ARCH-001"],
        rule_source_ids=["SRC-STAGE7-ARCHITECTURE"],
        policy_version="stage8-v1",
        cost_scenario="FN:FP=5:1",
        threshold_configuration={"t_low": 0.2, "t_high": 0.4},
        final_decision="HUMAN_REVIEW",
        review_required=True,
    )
    payload.update(overrides)
    return build_record(**payload)


def test_threshold_selection_rejects_non_validation_split() -> None:
    y = np.array([0, 1, 0, 1])
    p = np.array([0.1, 0.2, 0.8, 0.9])
    scen = CostScenario(5)
    with pytest.raises(ValueError, match="validation"):
        evaluate_thresholds(y, p, 0.3, 0.3, scen, split="test")
    with pytest.raises(ValueError, match="validation"):
        select_policy(y, p, scen, np.array([0.2, 0.4]), split="train")
    with pytest.raises(ValueError, match="validation"):
        assert_validation_split("test")


def test_threshold_selection_is_deterministic() -> None:
    rng = np.random.RandomState(42)
    p = np.clip(rng.beta(2, 5, 400), 0.02, 0.98)
    y = (p + rng.normal(0, 0.15, 400) > 0.3).astype(int)
    y[0], y[1] = 0, 1
    grid = make_threshold_grid(0.05, 0.6, 0.05)
    scen = CostScenario(5, c_review_over_fp=0.25)
    a = select_policy(y, p, scen, grid, split="validation")
    b = select_policy(y, p, scen, grid, split="validation")
    assert a["selected"]["t_low"] == b["selected"]["t_low"]
    assert a["selected"]["t_high"] == b["selected"]["t_high"]
    assert a["selected"]["expected_normalized_cost"] == b["selected"]["expected_normalized_cost"]


def test_expected_cost_and_ratio() -> None:
    scen = CostScenario(fn_fp_ratio=5, c_fp=1.0, c_review_over_fp=0.25)
    assert scen.c_fn == 5.0
    assert scen.c_review == 0.25
    assert expected_normalized_cost(fn=2, fp=4, n_review=8, n=10, scenario=scen) == pytest.approx(
        (5 * 2 + 1 * 4 + 0.25 * 8) / 10
    )


def test_cost_tie_prefers_single_threshold() -> None:
    y = np.array([0, 1])
    p = np.array([0.10, 0.90])
    scen = CostScenario(fn_fp_ratio=1, c_fp=1.0, c_review_over_fp=0.0)
    grid = np.array([0.2, 0.5, 0.8])
    result = select_policy(y, p, scen, grid, split="validation", include_two_threshold=True)
    assert result["selected"]["policy_type"] == "single_threshold"


def test_credit_band_thresholds() -> None:
    assert credit_band(0.199, 0.20, 0.40) == "LOW"
    assert credit_band(0.20, 0.20, 0.40) == "MEDIUM"
    assert credit_band(0.399, 0.20, 0.40) == "MEDIUM"
    assert credit_band(0.40, 0.20, 0.40) == "HIGH"
    assert credit_band(0.19, 0.20, 0.20) == "LOW"
    assert credit_band(0.20, 0.20, 0.20) == "HIGH"


def test_invalid_and_missing_probability() -> None:
    with pytest.raises(ValueError):
        credit_band(-0.01, 0.2, 0.4)
    with pytest.raises(ValueError):
        credit_band(1.01, 0.2, 0.4)
    with pytest.raises(ValueError):
        credit_band(float("nan"), 0.2, 0.4)
    with pytest.raises(ValueError):
        credit_band(None, 0.2, 0.4)  # type: ignore[arg-type]


def test_governance_hard_stops_and_review() -> None:
    low, high = 0.2, 0.5
    assert fuse_decision(0.05, "NOT_STRUCTURABLE_WITHOUT_REDESIGN", low, high, MATRIX)["final_decision"] == "REJECT"
    assert fuse_decision(0.99, "NOT_STRUCTURABLE_WITHOUT_REDESIGN", low, high, MATRIX)["final_decision"] == "REJECT"
    assert fuse_decision(0.05, "REVIEW", low, high, MATRIX)["final_decision"] == "HUMAN_REVIEW"
    assert fuse_decision(0.99, "REVIEW", low, high, MATRIX)["final_decision"] == "REJECT"
    assert fuse_decision(0.05, "INSUFFICIENT_INFORMATION", low, high, MATRIX)["final_decision"] == "HUMAN_REVIEW"
    assert fuse_decision(0.30, "INSUFFICIENT_INFORMATION", low, high, MATRIX)["final_decision"] == "HUMAN_REVIEW"
    assert fuse_decision(0.99, "INSUFFICIENT_INFORMATION", low, high, MATRIX)["final_decision"] == "REJECT"
    assert fuse_decision(0.05, "PASS", low, high, MATRIX)["final_decision"] == "APPROVE"
    assert fuse_decision(0.30, "PASS", low, high, MATRIX)["final_decision"] == "HUMAN_REVIEW"
    assert fuse_decision(0.99, "PASS", low, high, MATRIX)["final_decision"] == "REJECT"


def test_unknown_evidence_is_never_pass() -> None:
    out = fuse_decision(0.01, None, 0.2, 0.5, MATRIX)
    assert out["final_decision"] != "APPROVE"
    assert out["shariah_governance_status"] == "INSUFFICIENT_INFORMATION"
    out2 = fuse_decision(0.01, "unknown", 0.2, 0.5, MATRIX)
    assert out2["final_decision"] == "HUMAN_REVIEW"


def test_missing_governance_low_and_high_risk() -> None:
    assert fuse_decision(0.05, None, 0.2, 0.5, MATRIX)["final_decision"] == "HUMAN_REVIEW"
    assert fuse_decision(0.9, None, 0.2, 0.5, MATRIX)["final_decision"] == "REJECT"


def test_apply_policy_is_deterministic() -> None:
    p = np.array([0.05, 0.3, 0.9])
    gov = np.array(["PASS", "REVIEW", "INSUFFICIENT_INFORMATION"], dtype=object)
    a = apply_policy(p, gov, 0.2, 0.5, MATRIX)
    b = apply_policy(p, gov, 0.2, 0.5, MATRIX)
    assert list(a["final_decision"]) == list(b["final_decision"])
    assert list(a["final_decision"]) == ["APPROVE", "HUMAN_REVIEW", "REJECT"]


def test_shariah_firewall_credit_fields_cannot_enter_payload() -> None:
    payload = lendingclub_governance_payload()
    assert_no_credit_fields_in_governance_payload(payload)
    for col in PRIMARY_PREDICTORS:
        assert col not in payload
    with pytest.raises(ValueError, match="Credit"):
        assert_no_credit_fields_in_governance_payload({**payload, "fico_n": 700})
    with pytest.raises(ValueError, match="Credit"):
        assert_no_credit_fields_in_governance_payload({**payload, "loan_amnt": 1000})


def test_lendingclub_profile_does_not_pass() -> None:
    result = evaluate_lendingclub_governance(timestamp=TS)
    assert result["overall_governance_status"] != "PASS"
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert result["synthetic"] is False
    assert result["certification_claim"] is False


def test_model_firewall_shariah_fields_never_enter_ebm() -> None:
    names = ebm_config(42)["feature_names"]
    assert names == list(PRIMARY_PREDICTORS)
    assert "contract_type" not in names
    text = (ROOT / "src" / "models" / "ebm_model.py").read_text(encoding="utf-8")
    assert "shariah" not in text.lower()
    assert "governance" not in text.lower()
    runner = (ROOT / "experiments" / "stage8_decision" / "run_stage8.py").read_text(encoding="utf-8")
    assert "ebm_model" not in runner
    assert "PlattCalibrator" not in runner
    assert "fit(" not in inspect.getsource(select_policy)


def test_frozen_predictors_unchanged() -> None:
    assert list(PRIMARY_PREDICTORS) == list(LENDINGCLUB_PREDICTORS)
    for col in ("id", "issue_d", "experience_c", "title", "desc"):
        assert col not in PRIMARY_PREDICTORS
        assert col in FORBIDDEN_COLUMNS


def test_audit_required_fields_and_timestamp_invariance() -> None:
    a = _record(event_timestamp="2026-01-01T00:00:00+00:00")
    b = _record(event_timestamp="2026-12-31T23:59:59+00:00")
    assert a["decision_id"] == b["decision_id"]
    assert logic_hash(a) == a["decision_id"]
    for field in REQUIRED_FIELDS:
        assert field in a
    with pytest.raises(ValueError, match="forbidden"):
        assert_no_raw_identifiers({"id": "123", "final_decision": "REJECT"})


def test_audit_reference_is_hash_not_raw_id() -> None:
    rec = _record(record_reference_hash=hashlib.sha256(b"lc-row|999").hexdigest()[:16])
    assert rec["record_reference_hash"] != "999"
    assert "id" not in rec
    for key in FORBIDDEN_PUBLISHED_KEYS:
        assert key not in rec


def test_test_predictions_cannot_load_before_freeze(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="before freezing"):
        load_test_after_freeze(tmp_path / "missing_freeze.json")


def test_runner_loads_test_only_after_freeze() -> None:
    text = (ROOT / "experiments" / "stage8_decision" / "run_stage8.py").read_text(encoding="utf-8")
    assert text.index("dump_json(FREEZE_PATH") < text.index("test = load_test_after_freeze")


def test_no_shariah_score_in_policy_modules() -> None:
    yaml_text = (ROOT / "configs" / "stage8_decision_policy.yaml").read_text(encoding="utf-8")
    assert "shariah_score" not in yaml_text
    assert "final_score" not in yaml_text
    for path in (ROOT / "src" / "decision").glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "shariah_score =" not in text
        assert "final_score =" not in text


def test_all_zero_all_one_labels_do_not_crash() -> None:
    p = np.linspace(0.05, 0.95, 20)
    scen = CostScenario(2)
    grid = make_threshold_grid(0.1, 0.8, 0.1)
    zeros = np.zeros(20, dtype=int)
    ones = np.ones(20, dtype=int)
    z = select_policy(zeros, p, scen, grid, split="validation", include_two_threshold=False)
    o = select_policy(ones, p, scen, grid, split="validation", include_two_threshold=False)
    assert z["selected"]["n_positive"] == 0
    assert o["selected"]["n_negative"] == 0


def test_wilson_ci_bounds() -> None:
    lo, hi = wilson_ci(0, 10)
    assert 0 <= lo <= hi <= 1
    lo2, hi2 = wilson_ci(10, 10)
    assert 0 <= lo2 <= hi2 <= 1
    with pytest.raises(ValueError):
        wilson_ci(11, 10)


@pytest.mark.skipif(not FREEZE.exists(), reason="Stage 8 artifacts not generated yet")
def test_frozen_policy_declares_validation_only() -> None:
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert freeze["selection_split"] == "validation"
    assert freeze["frozen_before_test"] is True


@pytest.mark.skipif(not PUBLISHED.exists(), reason="Stage 8 artifacts not generated yet")
def test_published_examples_have_no_raw_identifiers() -> None:
    rows = json.loads(PUBLISHED.read_text(encoding="utf-8"))
    assert rows
    for row in rows:
        assert_no_raw_identifiers(row)
        for field in REQUIRED_FIELDS:
            assert field in row
        assert "zip_code" not in row
        assert "addr_state" not in row
        assert row["record_reference_hash"]
        assert row["record_reference_hash"] != row.get("id")
