"""Stage 9.1 ablation tests. No model training. No Stage 9.2+."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision.stage9_1 import (  # noqa: E402
    EXPECTED_A1,
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_T_STAR,
    EXPECTED_V1_FREEZE_SHA256,
    V1_FREEZE,
    apply_frozen_binary,
    apply_frozen_credit_only,
    load_stored_ablation,
    sha256_file,
    verify_frozen_artifacts,
)

RUNNER = ROOT / "experiments" / "stage9_1_ablation" / "run_stage9_1.py"
HELPER = ROOT / "src" / "decision" / "stage9_1.py"
SUMMARY = ROOT / "results" / "ablation" / "v1" / "metrics" / "ablation_summary.json"
V8_FREEZE = ROOT / "results" / "decision" / "frozen_policy.json"
V8_REPORT = ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md"


def test_a3_threshold_is_016() -> None:
    assert EXPECTED_T_STAR == 0.16
    freeze = json.loads(V1_FREEZE.read_text(encoding="utf-8"))
    v2 = json.loads((ROOT / "results" / "decision" / "v2" / "frozen_policy.json").read_text(encoding="utf-8"))
    assert float(v2["monolithic_t"]) == 0.16
    assert float(freeze["t_low"]) == EXPECTED_T_LOW
    assert float(freeze["t_high"]) == EXPECTED_T_HIGH


def test_a3_produces_no_human_review() -> None:
    p = np.array([0.0, 0.159, 0.16, 0.50, 1.0])
    decisions = apply_frozen_binary(p)
    assert "HUMAN_REVIEW" not in set(decisions)
    assert list(decisions) == ["APPROVE", "APPROVE", "REJECT", "REJECT", "REJECT"]


def test_a1_architecture_retains_human_review() -> None:
    stored = load_stored_ablation()
    assert stored["systems"]["A1"]["HUMAN_REVIEW"] == EXPECTED_A1["HUMAN_REVIEW"]
    assert stored["systems"]["A1"]["APPROVE"] == 0
    assert stored["systems"]["A1"]["REJECT"] == 27
    mid = apply_frozen_credit_only(np.array([0.20]))
    assert mid[0] == "HUMAN_REVIEW"


def test_stage8_thresholds_unchanged() -> None:
    integrity = verify_frozen_artifacts()
    assert integrity["t_low"] == 0.06
    assert integrity["t_high"] == 0.69
    assert sha256_file(V1_FREEZE) == EXPECTED_V1_FREEZE_SHA256
    assert V8_REPORT.exists()
    assert V8_FREEZE.exists()


def test_no_governance_score() -> None:
    text = HELPER.read_text(encoding="utf-8")
    assert "shariah_score" not in text
    assert "credit_probability_adjusted" not in text
    stored = load_stored_ablation()
    assert stored["a1_governance"] == {"INSUFFICIENT_INFORMATION": 208886}


def test_no_model_retraining_in_runner() -> None:
    text = RUNNER.read_text(encoding="utf-8") + "\n" + HELPER.read_text(encoding="utf-8")
    assert "select_policy(" not in text
    assert "PlattCalibrator" not in text
    assert "ebm_model" not in text
    assert ".fit(" not in text
    assert "joblib.load" not in text


def test_a3_a4_identity() -> None:
    stored = load_stored_ablation()
    assert stored["a3_identical_to_a4"] is True
    assert stored["systems"]["A3_A4"]["HUMAN_REVIEW"] == 0
    assert stored["systems"]["A3_A4"]["APPROVE"] == 61855
    assert stored["systems"]["A3_A4"]["REJECT"] == 147031


def test_deterministic_stored_assembly() -> None:
    a = load_stored_ablation()
    b = load_stored_ablation()
    assert a["systems"]["A0"]["APPROVE"] == b["systems"]["A0"]["APPROVE"]
    assert a["systems"]["A1"]["HUMAN_REVIEW"] == b["systems"]["A1"]["HUMAN_REVIEW"]
    assert a["systems"]["A3_A4"]["REJECT"] == b["systems"]["A3_A4"]["REJECT"]


@pytest.mark.skipif(not SUMMARY.exists(), reason="Stage 9.1 outputs not written yet")
def test_written_summary_records_hashes_and_no_selection() -> None:
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["experiment_id"] == "stage9_1_ablation_lc_v1"
    assert payload["a3_identical_to_a4"] is True
    assert payload["integrity"]["v1_freeze_sha256"] == EXPECTED_V1_FREEZE_SHA256
    assert payload["integrity"]["t_low"] == 0.06
    assert payload["integrity"]["t_high"] == 0.69
    assert payload["integrity"]["t_star"] == 0.16
    assert payload["consistency"]["used_for_selection"] is False
    assert payload["systems"]["A1"]["HUMAN_REVIEW"] == 208859
    assert payload["systems"]["A3_A4"]["HUMAN_REVIEW"] == 0
