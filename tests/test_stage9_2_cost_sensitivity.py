"""Stage 9.2 cost-sensitivity tests. No model training. No Stage 9.3+."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision.stage9_1 import (  # noqa: E402
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_T_STAR,
    EXPECTED_V1_FREEZE_SHA256,
    V1_FREEZE,
    sha256_file,
    verify_frozen_artifacts,
)
from decision.stage9_2 import (  # noqa: E402
    C_FP,
    C_REVIEW_OVER_FP_BINARY,
    C_REVIEW_OVER_FP_THREE_WAY,
    EXPERIMENT_G_STATUS,
    FN_FP_RATIOS,
    PRIMARY_RATIO,
    RATIO_LABELS,
    assemble_cost_sensitivity,
    cite_experiment_g,
    score_confusion,
)

RUNNER = ROOT / "experiments" / "stage9_2_cost_sensitivity" / "run_stage9_2.py"
HELPER = ROOT / "src" / "decision" / "stage9_2.py"
SUMMARY = ROOT / "results" / "cost_sensitivity" / "v1" / "metrics" / "cost_sensitivity_summary.json"
STAGE91_SUMMARY = ROOT / "results" / "ablation" / "v1" / "metrics" / "ablation_summary.json"
STAGE91_REPORT = ROOT / "docs" / "STAGE_9_1_ABLATION_REPORT.md"
V8_FREEZE = ROOT / "results" / "decision" / "frozen_policy.json"
V8_REPORT = ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md"


def test_stage8_thresholds_remain_006_069() -> None:
    integrity = verify_frozen_artifacts()
    assert integrity["t_low"] == 0.06
    assert integrity["t_high"] == 0.69
    assert EXPECTED_T_LOW == 0.06
    assert EXPECTED_T_HIGH == 0.69
    freeze = json.loads(V1_FREEZE.read_text(encoding="utf-8"))
    assert float(freeze["t_low"]) == 0.06
    assert float(freeze["t_high"]) == 0.69
    assert sha256_file(V8_FREEZE) == EXPECTED_V1_FREEZE_SHA256


def test_a3_threshold_remains_016() -> None:
    integrity = verify_frozen_artifacts()
    assert integrity["t_star"] == 0.16
    assert EXPECTED_T_STAR == 0.16
    v2 = json.loads((ROOT / "results" / "decision" / "v2" / "frozen_policy.json").read_text(encoding="utf-8"))
    assert float(v2["monolithic_t"]) == 0.16


def test_no_model_retraining() -> None:
    text = RUNNER.read_text(encoding="utf-8") + "\n" + HELPER.read_text(encoding="utf-8")
    assert "select_policy(" not in text
    assert "PlattCalibrator" not in text
    assert "ebm_model" not in text
    assert ".fit(" not in text
    assert "joblib.load" not in text
    assert "train_ebm" not in text
    payload = assemble_cost_sensitivity()
    assert payload["models_trained"] is False
    assert payload["models_loaded"] is False


def test_no_calibration_refit() -> None:
    text = RUNNER.read_text(encoding="utf-8") + "\n" + HELPER.read_text(encoding="utf-8")
    assert "IsotonicRegression" not in text
    assert "platt_calibrator" not in text
    assert "fit_isotonic" not in text
    payload = assemble_cost_sensitivity()
    assert payload["calibration_refit"] is False


def test_cost_ratios_are_frozen_set() -> None:
    assert FN_FP_RATIOS == (1, 2, 5, 10)
    assert RATIO_LABELS == ("FN:FP=1:1", "FN:FP=2:1", "FN:FP=5:1", "FN:FP=10:1")
    payload = assemble_cost_sensitivity()
    assert payload["fn_fp_ratios"] == [1, 2, 5, 10]
    labels = {row["ratio_label"] for row in payload["rows"]}
    assert labels == set(RATIO_LABELS)
    assert all(row["c_fp"] == C_FP == 1.0 for row in payload["rows"])
    inverted = [row for row in payload["rows"] if row["c_fn"] == 1.0 and row["c_fp"] == 2.0]
    assert inverted == []


def test_fixed_decisions_unchanged_across_cost_ratios() -> None:
    payload = assemble_cost_sensitivity()
    assert payload["decisions_unchanged_across_ratios"] is True
    for system, items in payload["by_system"].items():
        keys = {(d["tp"], d["tn"], d["fp"], d["fn"], d["n_approve"], d["n_review"], d["n_reject"]) for d in items}
        assert len(keys) == 1, system
        rates = {(d["fpr_population"], d["fnr_population"]) for d in items}
        assert len(rates) == 1, system
    assert payload["confusion"]["A1"]["n_review"] == 208859
    assert payload["confusion"]["A3_A4"]["n_review"] == 0
    assert payload["a1_human_review_retained"] is True
    assert payload["a3_identical_to_a4"] is True


def test_cost_formula_matches_stage8_and_arithmetic() -> None:
    payload = assemble_cost_sensitivity()
    a0 = payload["confusion"]["A0"]
    a1 = payload["confusion"]["A1"]
    a3 = payload["confusion"]["A3_A4"]
    n = 208886
    for ratio in FN_FP_RATIOS:
        a0_s = score_confusion(a0, ratio)
        a1_s = score_confusion(a1, ratio)
        a3_s = score_confusion(a3, ratio)
        assert a0_s["cost_total"] == pytest.approx(ratio * 196 + 13 + C_REVIEW_OVER_FP_THREE_WAY * 203627)
        assert a1_s["cost_total"] == pytest.approx(ratio * 0 + 13 + C_REVIEW_OVER_FP_THREE_WAY * 208859)
        assert a3_s["cost_total"] == pytest.approx(ratio * 5980 + 108771 + C_REVIEW_OVER_FP_BINARY * 0)
        assert a0_s["cost_normalized"] == pytest.approx(a0_s["cost_total"] / n)
        assert a1_s["cost_normalized"] == pytest.approx(a1_s["cost_total"] / n)
        assert a3_s["cost_normalized"] == pytest.approx(a3_s["cost_total"] / n)
    primary_a0 = next(r for r in payload["by_system"]["A0"] if r["fn_fp_ratio"] == PRIMARY_RATIO)
    primary_a1 = next(r for r in payload["by_system"]["A1"] if r["fn_fp_ratio"] == PRIMARY_RATIO)
    primary_a3 = next(r for r in payload["by_system"]["A3_A4"] if r["fn_fp_ratio"] == PRIMARY_RATIO)
    assert primary_a0["cost_normalized"] == pytest.approx(a0["stored_expected_normalized_cost_fnfp5"])
    assert primary_a1["cost_normalized"] == pytest.approx(a1["stored_expected_normalized_cost_fnfp5"])
    assert primary_a3["cost_normalized"] == pytest.approx(a3["stored_expected_normalized_cost_fnfp5"])
    assert payload["a1_cost_invariant_to_fn_fp_ratio"] is True


def test_no_lc_test_policy_selection() -> None:
    text = RUNNER.read_text(encoding="utf-8") + "\n" + HELPER.read_text(encoding="utf-8")
    assert "select_policy(" not in text
    assert "threshold_grid" not in text
    payload = assemble_cost_sensitivity()
    assert payload["used_for_selection"] is False
    g = cite_experiment_g()
    assert g["executed_in_stage9_2"] is False
    assert g["constraint_conflict_lc_test_selection"] is False
    assert g["status"] == EXPERIMENT_G_STATUS


def test_stage8_and_stage91_artifacts_exist() -> None:
    assert V8_REPORT.exists()
    assert V8_FREEZE.exists()
    assert STAGE91_SUMMARY.exists()
    assert STAGE91_REPORT.exists()
    s91 = json.loads(STAGE91_SUMMARY.read_text(encoding="utf-8"))
    assert s91["experiment_id"] == "stage9_1_ablation_lc_v1"
    assert s91["systems"]["A1"]["HUMAN_REVIEW"] == 208859


@pytest.mark.skipif(not SUMMARY.exists(), reason="Stage 9.2 outputs not written yet")
def test_written_summary_records_no_selection_and_hashes() -> None:
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["experiment_id"] == "stage9_2_cost_sensitivity_lc_v1"
    assert payload["used_for_selection"] is False
    assert payload["models_trained"] is False
    assert payload["integrity"]["v1_freeze_sha256"] == EXPECTED_V1_FREEZE_SHA256
    assert payload["integrity"]["t_low"] == 0.06
    assert payload["integrity"]["t_high"] == 0.69
    assert payload["integrity"]["t_star"] == 0.16
    assert payload["experiment_g"]["executed_in_stage9_2"] is False
    assert payload["a1_human_review_retained"] is True
