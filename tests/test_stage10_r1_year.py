"""S10-R1-YEAR tests. No model training. No S10-A1-GAP / S10-A4."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stage10.s10_r1_year import (  # noqa: E402
    ALLOWED_YEARS,
    CLASSIFICATION,
    EXPECTED_N,
    EXPERIMENT_ID,
    run_year_reanalysis,
)

HELPER = ROOT / "src" / "stage10" / "s10_r1_year.py"
RUNNER = ROOT / "experiments" / "stage10_r1_year" / "run_s10_r1.py"
SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_r1_year.json"
I1_SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json"
I1_REPORT = ROOT / "docs" / "STAGE_10_S10_I1_IDENTITY_REPORT.md"


def test_no_fit_or_joblib_load_in_s10_r1_source() -> None:
    text = HELPER.read_text(encoding="utf-8") + "\n" + RUNNER.read_text(encoding="utf-8")
    assert ".fit(" not in text
    assert "joblib.load" not in text
    assert "IsotonicRegression" not in text
    assert "minimize(" not in text
    assert "select_policy(" not in text


def test_does_not_parse_issue_calendar_fields() -> None:
    text = HELPER.read_text(encoding="utf-8")
    assert "pd.to_datetime" not in text
    assert '["issue_d"]' not in text
    assert 'frame["issue_d"]' not in text
    assert 'frame["issue_month"]' not in text


def test_year_reanalysis_is_non_confirmatory_and_uses_stored_year() -> None:
    payload = run_year_reanalysis()
    assert payload["issues"] == []
    assert payload["classification"] == CLASSIFICATION
    assert payload["confirmatory_experiment"] is False
    assert payload["n"] == EXPECTED_N
    assert payload["n_by_year"]["2017"] + payload["n_by_year"]["2018"] == EXPECTED_N
    assert set(int(y) for y in payload["n_by_year"]) == set(ALLOWED_YEARS)
    assert payload["thresholds"]["t_low"] == 0.06
    assert payload["thresholds"]["t_high"] == 0.69
    assert payload["thresholds"]["t_star"] == 0.16
    assert payload["thresholds"]["year_specific_threshold"] is False
    assert payload["models_trained"] is False
    assert payload["calibration_refit"] is False
    assert payload["s10_a1_gap_executed"] is False
    assert payload["s10_a4_executed"] is False
    for year in ("2017", "2018"):
        slice_ = payload["by_year"][year]
        assert slice_["A3_A4"]["HUMAN_REVIEW"]["count"] == 0
        assert slice_["A1"]["APPROVE"]["count"] == 0


def test_s10_i1_artifacts_remain() -> None:
    assert I1_SUMMARY.exists()
    payload = json.loads(I1_SUMMARY.read_text(encoding="utf-8"))
    assert payload["experiment_id"] == "s10_i1_identity_v1"
    assert I1_REPORT.exists()


def test_written_metrics_if_present() -> None:
    if not SUMMARY.exists():
        return
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["experiment_id"] == EXPERIMENT_ID
    assert payload["confirmatory_experiment"] is False
    assert payload["classification"] == CLASSIFICATION
    assert payload["n"] == EXPECTED_N
