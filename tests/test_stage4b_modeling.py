"""Integrity tests for Stage 4B. No test-set tuning is permitted."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from scipy import sparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data.audit_datasets import EXPECTED_LC_FILENAME, RAW_DIR, sha256_file  # noqa: E402
from evaluation.bootstrap import bootstrap_ci  # noqa: E402
from evaluation.metrics import classification_metrics, roc_auc  # noqa: E402
from models.common import SEEDS, row_ref  # noqa: E402
from models.logistic import logistic_pipeline  # noqa: E402
from preprocessing.lendingclub_preprocessor import (  # noqa: E402
    FORBIDDEN_COLUMNS,
    PRIMARY_PREDICTORS,
    RECORDED_LC_SHA256,
    LendingClubPreprocessor,
)

ASSIGN = ROOT / "results" / "tables" / "lendingclub_split_assignments.csv"
SELECTION = ROOT / "experiments" / "stage4b_credit_risk" / "selected_configurations.json"
SELECTION_RULE = ROOT / "experiments" / "stage4b_credit_risk" / "selection_rule.json"
VAL_PRED = ROOT / "results" / "predictions" / "validation"
TEST_PRED = ROOT / "results" / "predictions" / "test"
TEMPORAL = ROOT / "results" / "metrics" / "stage4b_temporal_metrics.json"
FAMILIES = [
    "logistic_regression",
    "random_forest",
    "xgboost",
    "explainable_boosting_machine",
]


def artifacts_complete() -> bool:
    return all((VAL_PRED / f"{family}_seed42.csv").exists() for family in FAMILIES) and all(
        (TEST_PRED / f"{family}_seed42.csv").exists() for family in FAMILIES
    )


def test_target_is_never_included_as_predictor() -> None:
    assert "Default" not in PRIMARY_PREDICTORS
    assert "Default" in FORBIDDEN_COLUMNS


def test_excluded_columns_are_never_passed_to_models() -> None:
    for col in ("id", "issue_d", "experience_c", "title", "desc"):
        assert col not in PRIMARY_PREDICTORS
        assert col in FORBIDDEN_COLUMNS


def test_preprocessing_fit_only_on_allowed_data() -> None:
    prep = LendingClubPreprocessor()
    frame = pd.DataFrame({c: [0] for c in PRIMARY_PREDICTORS})
    frame["Default"] = 1
    with pytest.raises(ValueError, match="Forbidden"):
        prep.fit(frame)
    with pytest.raises(ValueError, match="Target must not"):
        prep.fit(pd.DataFrame({c: [0] for c in PRIMARY_PREDICTORS}), y=np.array([1]))


def test_bootstrap_procedure_is_reproducible() -> None:
    rng = np.random.RandomState(0)
    y = rng.randint(0, 2, size=200)
    y[0] = 0
    y[1] = 1
    p = rng.uniform(0.1, 0.9, size=200)
    a = bootstrap_ci(y, p, roc_auc, n_bootstrap=200, seed=42)
    b = bootstrap_ci(y, p, roc_auc, n_bootstrap=200, seed=42)
    assert a == b
    c = bootstrap_ci(y, p, roc_auc, n_bootstrap=200, seed=99)
    assert a["ci_lower"] != c["ci_lower"] or a["ci_upper"] != c["ci_upper"]
    assert a["method"] == "percentile_bootstrap_rows_with_replacement"
    assert a["n_bootstrap"] == 200
    assert a["seed"] == 42
    assert a["confidence_level"] == 0.95


def test_seeds_are_the_frozen_list() -> None:
    assert SEEDS == [42, 123, 2024, 3407, 9999]


def test_seeds_reproduce_logistic_within_tolerance() -> None:
    rng = np.random.RandomState(0)
    x = sparse.csr_matrix(rng.randn(400, 24))
    y = rng.randint(0, 2, size=400)
    y[0] = 0
    y[1] = 1
    p1 = logistic_pipeline(42).fit(x, y).predict_proba(x)[:, 1]
    p2 = logistic_pipeline(42).fit(x, y).predict_proba(x)[:, 1]
    assert np.allclose(p1, p2, atol=1e-10)


def test_seeds_reproduce_random_forest_within_tolerance() -> None:
    from models.random_forest import random_forest_model

    rng = np.random.RandomState(0)
    x = rng.randn(300, 8)
    y = rng.randint(0, 2, size=300)
    y[0] = 0
    y[1] = 1
    p1 = random_forest_model(42).fit(x, y).predict_proba(x)[:, 1]
    p2 = random_forest_model(42).fit(x, y).predict_proba(x)[:, 1]
    p3 = random_forest_model(123).fit(x, y).predict_proba(x)[:, 1]
    assert np.allclose(p1, p2, atol=1e-10)
    assert not np.allclose(p1, p3, atol=1e-8)


def test_metric_definitions_match_sklearn() -> None:
    y = np.array([0, 0, 1, 1])
    p = np.array([0.1, 0.4, 0.35, 0.8])
    got = classification_metrics(y, p)
    from sklearn.metrics import average_precision_score, brier_score_loss, log_loss, roc_auc_score

    assert got["roc_auc"] == pytest.approx(roc_auc_score(y, p))
    assert got["pr_auc"] == pytest.approx(average_precision_score(y, p))
    assert got["brier"] == pytest.approx(brier_score_loss(y, p))
    assert got["log_loss"] == pytest.approx(log_loss(y, np.clip(p, 1e-15, 1 - 1e-15), labels=[0, 1]))


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 4B artifacts not generated yet")
def test_test_data_never_used_during_model_fitting() -> None:
    rule = json.loads(SELECTION_RULE.read_text(encoding="utf-8"))
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    assert rule["test_metrics_not_consulted"] is True
    assert selection["declared_before_test"] is True
    blob = json.dumps(selection)
    assert "roc_auc_ci" not in blob
    assert "test_rows" not in blob


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 4B artifacts not generated yet")
def test_test_labels_not_used_for_model_selection() -> None:
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    assert "selected_family" in selection
    dumped = json.dumps(selection)
    assert "p_hat" not in dumped
    test_files = list(TEST_PRED.glob("*.csv"))
    assert test_files
    sel_mtime = SELECTION.stat().st_mtime
    for path in test_files:
        assert path.stat().st_mtime >= sel_mtime - 2.0


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 4B artifacts not generated yet")
def test_prediction_rows_match_splits_and_are_unique() -> None:
    assign = pd.read_csv(ASSIGN, usecols=["id", "split"])
    val_ids = assign.loc[assign["split"] == "validation", "id"]
    expected_val = {row_ref(i) for i in val_ids}
    test_ids = assign.loc[assign["split"] == "test", "id"]
    expected_test = {row_ref(i) for i in test_ids}
    for family in FAMILIES:
        val = pd.read_csv(VAL_PRED / f"{family}_seed42.csv")
        assert val["row_ref"].is_unique
        assert set(val["row_ref"]) == expected_val
        assert (val["split"] == "validation").all()
        test = pd.read_csv(TEST_PRED / f"{family}_seed42.csv")
        assert test["row_ref"].is_unique
        assert set(test["row_ref"]) == expected_test
        assert (test["split"] == "test").all()
        assert "id" not in val.columns and "id" not in test.columns


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 4B artifacts not generated yet")
def test_no_duplicate_prediction_rows() -> None:
    for path in list(VAL_PRED.glob("*.csv")) + list(TEST_PRED.glob("*.csv")):
        frame = pd.read_csv(path, usecols=["row_ref"])
        assert not frame["row_ref"].duplicated().any()


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 4B artifacts not generated yet")
def test_probabilities_within_unit_interval() -> None:
    for path in list(VAL_PRED.glob("*.csv")) + list(TEST_PRED.glob("*.csv")):
        p = pd.read_csv(path, usecols=["p_hat"])["p_hat"]
        assert p.between(0, 1).all()


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 4B artifacts not generated yet")
def test_test_evaluation_happens_only_after_freeze() -> None:
    rule_time = SELECTION_RULE.stat().st_mtime
    sel_time = SELECTION.stat().st_mtime
    assert sel_time >= rule_time - 2.0
    for path in TEST_PRED.glob("*.csv"):
        assert path.stat().st_mtime >= sel_time - 2.0


@pytest.mark.skipif(not artifacts_complete() or not TEMPORAL.exists(), reason="Stage 4B artifacts not generated yet")
def test_temporal_evaluation_uses_correct_calendar_periods() -> None:
    rows = json.loads(TEMPORAL.read_text(encoding="utf-8"))
    years = {r["year"] for r in rows}
    assert years == {2017, 2018}
    test = pd.read_csv(TEST_PRED / "xgboost_seed42.csv")
    assert set(test["year"]) <= {2017, 2018}


def test_raw_hash_unchanged() -> None:
    assert sha256_file(RAW_DIR / EXPECTED_LC_FILENAME) == RECORDED_LC_SHA256
