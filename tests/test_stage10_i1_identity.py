"""S10-I1-IDENTITY tests. No model training. No S10-R1/A1/A4."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision.stage9_1 import apply_frozen_binary, apply_frozen_credit_only  # noqa: E402
from stage10.s10_i1_identity import (  # noqa: E402
    EXPECTED_N,
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_T_STAR,
    STATUS_FAIL,
    STATUS_PASS,
    STATUS_PASS_DOC,
    g0_from_bands,
    run_identity_check,
)

HELPER = ROOT / "src" / "stage10" / "s10_i1_identity.py"
RUNNER = ROOT / "experiments" / "stage10_i1_identity" / "run_s10_i1.py"
SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json"


def test_no_fit_or_joblib_load_in_s10_i1_source() -> None:
    text = HELPER.read_text(encoding="utf-8") + "\n" + RUNNER.read_text(encoding="utf-8")
    assert ".fit(" not in text
    assert "joblib.load" not in text
    assert "IsotonicRegression" not in text
    assert "minimize(" not in text


def test_a3_has_no_human_review_branch() -> None:
    decisions = apply_frozen_binary(np.array([0.0, 0.159, 0.16, 1.0]))
    assert "HUMAN_REVIEW" not in set(decisions)
    assert EXPECTED_T_STAR == 0.16


def test_a0_uses_frozen_two_threshold_map() -> None:
    assert EXPECTED_T_LOW == 0.06
    assert EXPECTED_T_HIGH == 0.69
    decisions = apply_frozen_credit_only(np.array([0.05, 0.06, 0.68, 0.69]))
    assert list(decisions) == ["APPROVE", "HUMAN_REVIEW", "HUMAN_REVIEW", "REJECT"]


def test_identity_check_pass_and_same_p_selected() -> None:
    check = run_identity_check()
    assert check["issues"] == []
    assert check["status"] in {STATUS_PASS, STATUS_PASS_DOC}
    assert check["status"] != STATUS_FAIL
    assert check["n"] == EXPECTED_N
    assert check["p_selected_identity"]["a0_a1_a3_share_single_p_selected_vector"] is True
    assert check["p_selected_identity"]["p_selected_equals_stored_p_platt"] is True
    assert check["a0"]["match"] is True
    assert check["a1"]["match"] is True
    assert check["a3_a4"]["match"] is True
    assert check["a3_a4"]["human_review_count"] == 0
    assert check["models_trained"] is False
    assert check["calibration_refit"] is False
    assert check["thresholds_searched"] is False
    assert check["uci_opened"] is False
    assert check["s10_r1_executed"] is False
    assert check["confirmatory_experiment"] is False


def test_g0_maps_low_medium_to_review() -> None:
    from decision.stage9_1 import credit_bands

    bands = credit_bands(np.array([0.01, 0.20, 0.80]), 0.06, 0.69)
    fused = g0_from_bands(bands)
    assert list(fused) == ["HUMAN_REVIEW", "HUMAN_REVIEW", "REJECT"]


def test_written_metrics_if_present() -> None:
    if not SUMMARY.exists():
        return
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["experiment_id"] == "s10_i1_identity_v1"
    assert payload["confirmatory_experiment"] is False
    assert payload["n"] == EXPECTED_N
