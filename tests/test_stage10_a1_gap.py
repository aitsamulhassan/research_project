"""S10-A1-GAP tests. Analysis-only. No S10-A4. No model training."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from stage10.s10_a1_gap import CLASSIFICATION, EXPECTED_N, EXPERIMENT_ID, run_gap_analysis  # noqa: E402

HELPER = ROOT / "src" / "stage10" / "s10_a1_gap.py"
RUNNER = ROOT / "experiments" / "stage10_a1_gap" / "run_s10_a1.py"
SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_a1_gap.json"
I1_SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json"
R1_SUMMARY = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_r1_year.json"


def test_no_fit_or_new_shariah_constructs() -> None:
    text = HELPER.read_text(encoding="utf-8") + "\n" + RUNNER.read_text(encoding="utf-8")
    assert ".fit(" not in text
    assert "joblib.load" not in text
    assert "def shariah_score" not in text
    assert "shariah_probability" not in text
    assert "G-unsafe" not in text
    assert "select_policy(" not in text


def test_gap_decomposition_matches_frozen_a1() -> None:
    payload = run_gap_analysis()
    assert payload["issues"] == []
    assert payload["classification"] == CLASSIFICATION
    assert payload["confirmatory_experiment"] is False
    assert payload["n"] == EXPECTED_N
    bands = {row["credit_band"]: row["count"] for row in payload["credit_bands"]}
    assert bands == {"LOW": 5232, "MEDIUM": 203627, "HIGH": 27}
    l2 = {row["l2_governance_status"]: row["count"] for row in payload["l2_governance_states"]}
    assert l2["INSUFFICIENT_INFORMATION"] == EXPECTED_N
    assert l2["PASS"] == 0
    assert payload["decomposition"]["a1_approve"] == 0
    assert payload["decomposition"]["a1_review"] == 208859
    assert payload["decomposition"]["a1_reject"] == 27
    assert payload["g1_g3_treated_as_observed"] is False
    assert payload["s10_a4_executed"] is False
    assert payload["models_trained"] is False
    assert payload["thresholds_searched"] is False


def test_crosstab_explains_review_and_reject() -> None:
    payload = run_gap_analysis()
    cells = {
        (row["credit_band"], row["l2_governance_status"]): row
        for row in payload["crosstab"]
    }
    low = cells[("LOW", "INSUFFICIENT_INFORMATION")]
    med = cells[("MEDIUM", "INSUFFICIENT_INFORMATION")]
    high = cells[("HIGH", "INSUFFICIENT_INFORMATION")]
    assert low["n"] == 5232 and low["g0_decision"] == "HUMAN_REVIEW"
    assert med["n"] == 203627 and med["g0_decision"] == "HUMAN_REVIEW"
    assert high["n"] == 27 and high["g0_decision"] == "REJECT"
    assert cells[("LOW", "PASS")]["n"] == 0


def test_prior_artifacts_remain() -> None:
    assert json.loads(I1_SUMMARY.read_text(encoding="utf-8"))["experiment_id"] == "s10_i1_identity_v1"
    assert json.loads(R1_SUMMARY.read_text(encoding="utf-8"))["experiment_id"] == "s10_r1_year_v1"


def test_written_metrics_if_present() -> None:
    if not SUMMARY.exists():
        return
    payload = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert payload["experiment_id"] == EXPERIMENT_ID
    assert payload["classification"] == CLASSIFICATION
    assert payload["s10_a4_executed"] is False
