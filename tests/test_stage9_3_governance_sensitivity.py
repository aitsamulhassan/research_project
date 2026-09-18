"""Stage 9.3 governance-sensitivity tests. No model training. No Stage 9.4+."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision.policy_matrix import CREDIT_BANDS, GOVERNANCE_STATUSES  # noqa: E402
from decision.stage9_1 import (  # noqa: E402
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_V1_FREEZE_SHA256,
    V1_FREEZE,
    sha256_file,
    verify_frozen_artifacts,
)
from decision.stage9_3 import (  # noqa: E402
    CERTIFICATION_CLAIM,
    EXPERT_VALIDATION,
    G0_INSUFFICIENT_TREATMENT,
    G1_INSUFFICIENT_TREATMENT,
    G3_INSUFFICIENT_TREATMENT,
    G_UNSAFE_STATUS,
    OBSERVED_L2,
    assemble_governance_sensitivity,
    fuse_status_band,
)

RUNNER = ROOT / "experiments" / "stage9_3_governance_sensitivity" / "run_stage9_3.py"
HELPER = ROOT / "src" / "decision" / "stage9_3.py"
SUMMARY = ROOT / "results" / "governance_sensitivity" / "v1" / "metrics" / "governance_sensitivity_summary.json"
V8_FREEZE = ROOT / "results" / "decision" / "frozen_policy.json"


def _source_text() -> str:
    return RUNNER.read_text(encoding="utf-8") + "\n" + HELPER.read_text(encoding="utf-8")


def test_g0_uses_observed_insufficient_information() -> None:
    payload = assemble_governance_sensitivity()
    assert payload["observed_l2"] == OBSERVED_L2 == "INSUFFICIENT_INFORMATION"
    assert payload["published"]["gov_counts"] == {"INSUFFICIENT_INFORMATION": 208886}
    g0 = payload["scenarios"]["G0"]
    assert g0["governance_status_input"] == "INSUFFICIENT_INFORMATION"
    assert g0["APPROVE"] == 0
    assert g0["HUMAN_REVIEW"] == 208859
    assert g0["REJECT"] == 27
    assert G0_INSUFFICIENT_TREATMENT == {"LOW": "HUMAN_REVIEW", "MEDIUM": "HUMAN_REVIEW", "HIGH": "REJECT"}
    assert fuse_status_band("G0", "INSUFFICIENT_INFORMATION", "LOW") == "HUMAN_REVIEW"
    assert fuse_status_band("G0", "INSUFFICIENT_INFORMATION", "HIGH") == "REJECT"


def test_g1_matches_protocol_definition() -> None:
    assert G1_INSUFFICIENT_TREATMENT == {"LOW": "REJECT", "MEDIUM": "REJECT", "HIGH": "REJECT"}
    for band in CREDIT_BANDS:
        assert fuse_status_band("G1", "INSUFFICIENT_INFORMATION", band) == "REJECT"
    payload = assemble_governance_sensitivity()
    g1 = payload["scenarios"]["G1"]
    assert g1["APPROVE"] == 0
    assert g1["HUMAN_REVIEW"] == 0
    assert g1["REJECT"] == 208886
    assert g1["role"] == "hypothetical_engineering_scenario"
    assert fuse_status_band("G1", "PASS", "LOW") == "APPROVE"


def test_g3_matches_protocol_definition() -> None:
    assert G3_INSUFFICIENT_TREATMENT == {
        "LOW": "HUMAN_REVIEW",
        "MEDIUM": "HUMAN_REVIEW",
        "HIGH": "HUMAN_REVIEW",
    }
    for band in CREDIT_BANDS:
        assert fuse_status_band("G3", "INSUFFICIENT_INFORMATION", band) == "HUMAN_REVIEW"
    payload = assemble_governance_sensitivity()
    g3 = payload["scenarios"]["G3"]
    assert g3["APPROVE"] == 0
    assert g3["HUMAN_REVIEW"] == 208886
    assert g3["REJECT"] == 0
    assert g3["role"] == "hypothetical_engineering_scenario"
    assert fuse_status_band("G3", "PASS", "LOW") == "APPROVE"
    assert fuse_status_band("G3", "INSUFFICIENT_INFORMATION", "HIGH") == "HUMAN_REVIEW"


def test_no_new_shariah_rules() -> None:
    text = _source_text()
    assert "SHR-001" not in text
    assert "AAOIFI" not in text
    assert "Murabahah" not in text
    assert "Ijarah" not in text
    payload = assemble_governance_sensitivity()
    assert payload["new_shariah_rules_added"] is False


def test_no_credit_model_retraining() -> None:
    text = _source_text()
    assert "select_policy(" not in text
    assert "PlattCalibrator" not in text
    assert "ebm_model" not in text
    assert ".fit(" not in text
    assert "joblib.load" not in text
    payload = assemble_governance_sensitivity()
    assert payload["models_trained"] is False
    assert payload["models_loaded"] is False


def test_no_calibration_refit() -> None:
    text = _source_text()
    assert "IsotonicRegression" not in text
    assert "fit_isotonic" not in text
    payload = assemble_governance_sensitivity()
    assert payload["calibration_refit"] is False


def test_frozen_credit_bands_and_thresholds_unchanged() -> None:
    integrity = verify_frozen_artifacts()
    assert integrity["t_low"] == EXPECTED_T_LOW == 0.06
    assert integrity["t_high"] == EXPECTED_T_HIGH == 0.69
    payload = assemble_governance_sensitivity()
    assert payload["published"]["band_counts"] == {"HIGH": 27, "LOW": 5232, "MEDIUM": 203627}
    assert payload["credit_bands_unchanged"] is True
    assert payload["thresholds_unchanged"] is True
    assert payload["published"]["t_low"] == 0.06
    assert payload["published"]["t_high"] == 0.69


def test_stage8_policy_artifact_unchanged() -> None:
    assert sha256_file(V8_FREEZE) == EXPECTED_V1_FREEZE_SHA256
    freeze = json.loads(V1_FREEZE.read_text(encoding="utf-8"))
    assert float(freeze["t_low"]) == 0.06
    assert float(freeze["t_high"]) == 0.69


def test_g0_g1_g3_differ_only_in_insufficient_information_row() -> None:
    payload = assemble_governance_sensitivity()
    assert payload["other_governance_statuses_unchanged"] is True
    for status in GOVERNANCE_STATUSES:
        if status == "INSUFFICIENT_INFORMATION":
            continue
        for band in CREDIT_BANDS:
            g0 = fuse_status_band("G0", status, band)
            assert fuse_status_band("G1", status, band) == g0
            assert fuse_status_band("G3", status, band) == g0
    g0_i = {b: fuse_status_band("G0", "INSUFFICIENT_INFORMATION", b) for b in CREDIT_BANDS}
    g1_i = {b: fuse_status_band("G1", "INSUFFICIENT_INFORMATION", b) for b in CREDIT_BANDS}
    g3_i = {b: fuse_status_band("G3", "INSUFFICIENT_INFORMATION", b) for b in CREDIT_BANDS}
    assert g0_i != g1_i
    assert g0_i != g3_i
    assert g1_i != g3_i


def test_no_test_based_scenario_selection() -> None:
    text = _source_text()
    assert "select_policy(" not in text
    payload = assemble_governance_sensitivity()
    assert payload["used_for_selection"] is False
    assert payload["g_unsafe_executed"] is False
    assert payload["g_unsafe_status"] == G_UNSAFE_STATUS


def test_no_shariah_probability_or_score() -> None:
    text = _source_text().lower()
    assert "shariah_score" not in text
    assert "shariah_probability" not in text
    assert "halal_probability" not in text
    assert "haram_probability" not in text
    assert "credit_probability_adjusted" not in text


def test_expert_validation_and_certification_flags() -> None:
    payload = assemble_governance_sensitivity()
    assert payload["expert_validation"] == EXPERT_VALIDATION == "NONE_EXPERT_VALIDATED"
    assert payload["certification_claim"] is CERTIFICATION_CLAIM is False
    assert payload["any_expert_validated"] is False
    assert payload["published"]["certification_claim_policy"] is False


@pytest.mark.skipif(not SUMMARY.exists(), reason="Stage 9.3 outputs not written yet")
def test_written_summary_records_flags() -> None:
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["experiment_id"] == "stage9_3_governance_sensitivity_lc_v1"
    assert payload["used_for_selection"] is False
    assert payload["models_trained"] is False
    assert payload["integrity"]["v1_freeze_sha256"] == EXPECTED_V1_FREEZE_SHA256
    assert payload["scenarios"]["G0"]["HUMAN_REVIEW"] == 208859
    assert payload["scenarios"]["G1"]["REJECT"] == 208886
    assert payload["scenarios"]["G3"]["HUMAN_REVIEW"] == 208886
    assert payload["certification_claim"] is False
    assert payload["expert_validation"] == "NONE_EXPERT_VALIDATED"

