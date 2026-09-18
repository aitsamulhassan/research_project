"""Integrity tests for Stage 5 calibration. No test-set fitting or selection."""

from __future__ import annotations

import inspect
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from calibration.isotonic import IsotonicCalibrator  # noqa: E402
from calibration.metrics import brier, ece, logloss, mce  # noqa: E402
from calibration.platt import PlattCalibrator, logit  # noqa: E402
from evaluation.metrics import brier as eval_brier  # noqa: E402
from evaluation.metrics import logloss as eval_logloss  # noqa: E402
from models.common import row_ref  # noqa: E402
from preprocessing.lendingclub_preprocessor import FORBIDDEN_COLUMNS, PRIMARY_PREDICTORS  # noqa: E402

ASSIGN = ROOT / "results" / "tables" / "lendingclub_split_assignments.csv"
SELECTION = ROOT / "experiments" / "stage5_calibration" / "selected_calibration.json"
SELECTION_RULE = ROOT / "experiments" / "stage5_calibration" / "selection_rule.json"
VAL_CAL = ROOT / "results" / "calibration" / "validation" / "ebm_seed42_calibrated.csv"
TEST_CAL = ROOT / "results" / "calibration" / "test" / "ebm_seed42_calibrated.csv"
RAW_VAL = ROOT / "results" / "calibration" / "raw" / "ebm_train_only_seed42_validation.csv"
RAW_TEST = ROOT / "results" / "calibration" / "raw" / "ebm_train_only_seed42_test.csv"
TEMPORAL = ROOT / "results" / "calibration" / "metrics" / "stage5_temporal.json"


def artifacts_complete() -> bool:
    return VAL_CAL.exists() and TEST_CAL.exists() and SELECTION.exists() and SELECTION_RULE.exists()


def test_calibrators_reject_non_validation_split() -> None:
    rng = np.random.RandomState(0)
    p = rng.uniform(0.1, 0.9, 80)
    y = rng.randint(0, 2, 80)
    y[0] = 0
    y[1] = 1
    with pytest.raises(ValueError, match="validation"):
        PlattCalibrator().fit(p, y, split="test")
    with pytest.raises(ValueError, match="validation"):
        IsotonicCalibrator().fit(p, y, split="test")
    with pytest.raises(ValueError, match="validation"):
        PlattCalibrator().fit(p, y, split="train")


def test_transform_does_not_accept_labels() -> None:
    assert "y" not in inspect.signature(PlattCalibrator.transform).parameters
    assert "y" not in inspect.signature(IsotonicCalibrator.transform).parameters


def test_calibration_cannot_alter_frozen_feature_set() -> None:
    assert "Default" not in PRIMARY_PREDICTORS
    for col in ("id", "issue_d", "experience_c", "title", "desc"):
        assert col not in PRIMARY_PREDICTORS
        assert col in FORBIDDEN_COLUMNS
    text = "".join(path.read_text(encoding="utf-8") for path in (ROOT / "src" / "calibration").glob("*.py"))
    for token in ('"experience_c"', "'experience_c'", '"title"', "'title'", '"desc"', "'desc'"):
        assert token not in text


def test_ece_known_example() -> None:
    y = np.array([0, 0, 1, 1])
    p = np.array([0.1, 0.1, 0.9, 0.9])
    assert ece(y, p, n_bins=2) == pytest.approx(0.1)
    assert mce(y, p, n_bins=2) == pytest.approx(0.1)


def test_ece_is_reproducible() -> None:
    rng = np.random.RandomState(1)
    y = rng.randint(0, 2, 500)
    y[0] = 0
    y[1] = 1
    p = rng.uniform(0, 1, 500)
    assert ece(y, p) == ece(y, p)


def test_brier_matches_declared_definition() -> None:
    y = np.array([0, 1, 1, 0], dtype=float)
    p = np.array([0.2, 0.7, 0.9, 0.1])
    assert brier(y, p) == pytest.approx(eval_brier(y, p))
    assert brier(y, p) == pytest.approx(float(np.mean((p - y) ** 2)))


def test_log_loss_matches_declared_definition() -> None:
    y = np.array([0, 1, 1, 0], dtype=float)
    p = np.array([0.2, 0.7, 0.9, 0.1])
    assert logloss(y, p) == pytest.approx(eval_logloss(y, p))


def test_platt_and_isotonic_are_deterministic() -> None:
    rng = np.random.RandomState(0)
    p = rng.uniform(0.05, 0.95, 200)
    y = rng.randint(0, 2, 200)
    y[0] = 0
    y[1] = 1
    a = PlattCalibrator().fit(p, y, split="validation").transform(p)
    b = PlattCalibrator().fit(p, y, split="validation").transform(p)
    assert np.allclose(a, b)
    c = IsotonicCalibrator().fit(p, y, split="validation").transform(p)
    d = IsotonicCalibrator().fit(p, y, split="validation").transform(p)
    assert np.allclose(c, d)


def test_calibrated_probabilities_in_unit_interval_synthetic() -> None:
    rng = np.random.RandomState(0)
    p = rng.uniform(0.01, 0.99, 150)
    y = rng.randint(0, 2, 150)
    y[0] = 0
    y[1] = 1
    out = PlattCalibrator().fit(p, y, split="validation").transform(np.array([0.0, 0.5, 1.0]))
    assert np.all((out >= 0) & (out <= 1))
    assert np.all(np.isfinite(out))
    out_i = IsotonicCalibrator().fit(p, y, split="validation").transform(np.array([0.0, 0.5, 1.0]))
    assert np.all((out_i >= 0) & (out_i <= 1))
    assert np.all(np.isfinite(out_i))


def test_logit_bounds() -> None:
    z = logit(np.array([0.0, 1.0, 0.5]))
    assert np.all(np.isfinite(z))
    assert z[2] == pytest.approx(0.0)


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 5 artifacts not generated yet")
def test_validation_predictions_match_validation_rows() -> None:
    assign = pd.read_csv(ASSIGN, usecols=["id", "split"])
    expected = {row_ref(i) for i in assign.loc[assign["split"] == "validation", "id"]}
    val = pd.read_csv(VAL_CAL)
    assert val["row_ref"].is_unique
    assert set(val["row_ref"]) == expected
    assert (val["split"] == "validation").all()
    assert "id" not in val.columns


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 5 artifacts not generated yet")
def test_test_predictions_match_test_rows() -> None:
    assign = pd.read_csv(ASSIGN, usecols=["id", "split"])
    expected = {row_ref(i) for i in assign.loc[assign["split"] == "test", "id"]}
    test = pd.read_csv(TEST_CAL)
    assert test["row_ref"].is_unique
    assert set(test["row_ref"]) == expected
    assert (test["split"] == "test").all()
    assert "id" not in test.columns


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 5 artifacts not generated yet")
def test_raw_probabilities_remain_unchanged() -> None:
    val = pd.read_csv(VAL_CAL)
    raw = pd.read_csv(RAW_VAL)
    merged = val.merge(raw, on="row_ref", suffixes=("_cal", "_rawfile"))
    assert np.allclose(merged["p_raw_cal"], merged["p_raw_rawfile"])
    test = pd.read_csv(TEST_CAL)
    raw_te = pd.read_csv(RAW_TEST)
    merged_te = test.merge(raw_te, on="row_ref", suffixes=("_cal", "_rawfile"))
    assert np.allclose(merged_te["p_raw_cal"], merged_te["p_raw_rawfile"])


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 5 artifacts not generated yet")
def test_calibrated_probabilities_finite_unit_interval() -> None:
    for path in (VAL_CAL, TEST_CAL):
        frame = pd.read_csv(path)
        for col in ("p_raw", "p_platt", "p_isotonic"):
            p = frame[col]
            assert p.between(0, 1).all()
            assert np.isfinite(p.to_numpy()).all()


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 5 artifacts not generated yet")
def test_test_metrics_only_after_freeze() -> None:
    rule = json.loads(SELECTION_RULE.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    assert rule["test_metrics_not_consulted"] is True
    assert selection["declared_before_test"] is True
    blob = json.dumps(selection)
    assert "roc_auc_ci" not in blob
    assert TEST_CAL.stat().st_mtime >= SELECTION.stat().st_mtime - 2.0
    assert SELECTION.stat().st_mtime >= SELECTION_RULE.stat().st_mtime - 2.0


@pytest.mark.skipif(not artifacts_complete() or not TEMPORAL.exists(), reason="Stage 5 artifacts not generated yet")
def test_temporal_calibration_uses_correct_years() -> None:
    rows = json.loads(TEMPORAL.read_text(encoding="utf-8"))
    assert {r["year"] for r in rows} == {2017, 2018}
    test = pd.read_csv(TEST_CAL)
    assert set(test["year"]) <= {2017, 2018}


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 5 artifacts not generated yet")
def test_no_test_information_in_calibrator_fit_records() -> None:
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    assert selection["platt"]["fit_split"] == "validation"
    assert selection["isotonic"]["fit_split"] == "validation"
