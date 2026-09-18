"""Integrity tests for Stage 6 explainability."""

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

from explainability.local_cases import select_local_cases  # noqa: E402
from explainability.ranking import overlap_at_k, ranks_from_importance, spearman_ranks  # noqa: E402
from explainability.sampling import SAMPLE_N, SAMPLE_SEED, deterministic_indices  # noqa: E402
from explainability.shap_additive import additive_shap, shap_base_value  # noqa: E402
from explainability.stability import feature_stability, rank_matrix  # noqa: E402
from preprocessing.lendingclub_preprocessor import FORBIDDEN_COLUMNS, PRIMARY_PREDICTORS  # noqa: E402

SAMPLE = ROOT / "results" / "explainability" / "sample" / "explanation_sample_row_refs.csv"
TABLE1 = ROOT / "results" / "explainability" / "tables" / "table1_global_attribution.csv"
TABLE4 = ROOT / "results" / "explainability" / "tables" / "table4_local_cases.csv"
NPZ = ROOT / "results" / "explainability" / "artifacts" / "seed42_attributions.npz"
NPZ_META = ROOT / "results" / "explainability" / "artifacts" / "seed42_attributions.meta.json"
AUDIT = ROOT / "audit" / "stage6_explainability_run.json"
CASES = ROOT / "results" / "explainability" / "metrics" / "local_cases.json"
CONSISTENCY = ROOT / "results" / "explainability" / "metrics" / "consistency_checks.json"
CAL_ATTR = ROOT / "results" / "explainability" / "metrics" / "calibration_attribution.json"
FIG_DIR = ROOT / "results" / "figures" / "explainability"
ASSIGN = ROOT / "results" / "tables" / "lendingclub_split_assignments.csv"
TABLE_DIR = ROOT / "results" / "explainability" / "tables"

FIGURE_STEMS = [
    "figure1_global_shap_importance",
    "figure2_shap_beeswarm",
    "figure3_local_high_risk",
    "figure4_local_low_risk",
    "figure5_local_median_risk",
    "figure6_shap_vs_ebm_disagreement",
    "figure7_effect_fico_n",
    "figure8_effect_loan_amnt",
    "figure9_effect_dti_n",
    "figure10_effect_revenue",
    "figure11_effect_home_ownership_n",
    "figure12_seed_rank_stability",
]


def artifacts_complete() -> bool:
    return SAMPLE.exists() and TABLE1.exists() and NPZ.exists() and AUDIT.exists()


def test_deterministic_explanation_sampling() -> None:
    a = deterministic_indices(1000, 50, 42)
    b = deterministic_indices(1000, 50, 42)
    c = deterministic_indices(1000, 50, 123)
    assert np.array_equal(a, b)
    assert not np.array_equal(a, c)
    assert len(np.unique(a)) == 50


def test_no_excluded_features_and_nine_predictors() -> None:
    assert len(PRIMARY_PREDICTORS) == 9
    assert "Default" not in PRIMARY_PREDICTORS
    for col in ("id", "issue_d", "experience_c", "title", "desc"):
        assert col not in PRIMARY_PREDICTORS
        assert col in FORBIDDEN_COLUMNS


def test_topk_spearman_overlap_unit() -> None:
    a = np.array([5.0, 4.0, 3.0, 2.0, 1.0, 0.5, 0.4, 0.3, 0.2])
    b = np.array([5.0, 4.0, 3.0, 2.0, 1.0, 0.5, 0.4, 0.3, 0.2])
    assert overlap_at_k(a, b, 3) == 1.0
    assert spearman_ranks(a, b) == pytest.approx(1.0)
    c = np.array([0.2, 0.3, 0.4, 0.5, 1.0, 2.0, 3.0, 4.0, 5.0])
    assert overlap_at_k(a, c, 3) == 0.0
    assert overlap_at_k(a, c, 9) == 1.0
    assert ranks_from_importance(a)[0] == 1
    mixed = np.array([5.0, 4.0, 0.1, 2.0, 1.0, 0.5, 0.4, 0.3, 0.2])
    assert overlap_at_k(a, mixed, 3) == pytest.approx(2 / 3)


def test_seed_aggregation_unit() -> None:
    imps = {
        42: np.arange(9)[::-1].astype(float),
        123: np.arange(9)[::-1].astype(float),
    }
    ranks = rank_matrix(imps)
    stab = feature_stability(ranks, 2)
    assert stab.loc[stab["feature"] == PRIMARY_PREDICTORS[0], "top5_frequency"].iloc[0] == pytest.approx(1.0)
    assert stab.loc[stab["feature"] == PRIMARY_PREDICTORS[0], "top3_frequency"].iloc[0] == pytest.approx(1.0)
    assert stab.loc[stab["feature"] == PRIMARY_PREDICTORS[-1], "top5_frequency"].iloc[0] == pytest.approx(0.0)


def test_additive_shap_identity() -> None:
    terms = np.array([[1.0, 2.0], [3.0, 4.0]])
    means = np.array([1.0, 3.0])
    phi = additive_shap(terms, means)
    assert np.allclose(phi, np.array([[0.0, -1.0], [2.0, 1.0]]))
    base = shap_base_value(0.5, means)
    assert np.allclose(phi.sum(1) + base, terms.sum(1) + 0.5)


def test_local_case_selection_ignores_labels() -> None:
    assert "y" not in inspect.signature(select_local_cases).parameters
    assert "label" not in inspect.signature(select_local_cases).parameters
    p = np.array([0.1, 0.9, 0.5, 0.51])
    shap_v = np.eye(4, 9)
    ebm = np.eye(4, 9) * 2
    ebm[3] = np.arange(9)[::-1]
    shap_v[3] = np.arange(9)
    refs = np.array(["d", "c", "b", "a"])
    y = np.array([1, 0, 1, 0])
    _ = y
    chosen = select_local_cases(p, shap_v, ebm, refs)
    assert chosen["high_risk"] == 1
    assert chosen["low_risk"] == 0
    assert chosen["median_risk"] in (2, 3)
    assert chosen["disagreement"] not in {chosen["high_risk"], chosen["low_risk"], chosen["median_risk"]}


def test_repeatability_of_additive_shap() -> None:
    terms = np.random.RandomState(0).randn(20, 9)
    means = terms.mean(0)
    a = additive_shap(terms, means)
    b = additive_shap(terms, means)
    assert np.allclose(a, b)


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 6 artifacts not generated yet")
def test_sample_is_test_only_and_has_metadata() -> None:
    sample = pd.read_csv(SAMPLE)
    assert sample["row_ref"].is_unique
    assert len(sample) == 5000
    assert (sample["split"] == "test").all()
    assert "experiment_id" in sample.columns
    assert "id" not in sample.columns
    assert "Default" not in sample.columns
    n_test = int((pd.read_csv(ASSIGN, usecols=["split"])["split"] == "test").sum())
    expected = deterministic_indices(n_test, SAMPLE_N, SAMPLE_SEED)
    assert np.array_equal(sample["source_iloc"].to_numpy(), expected)


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 6 artifacts not generated yet")
def test_table_features_are_exactly_nine_predictors() -> None:
    table = pd.read_csv(TABLE1)
    assert set(table["feature"]) == set(PRIMARY_PREDICTORS)
    for col in ("id", "issue_d", "experience_c", "title", "desc", "Default"):
        assert col not in set(table["feature"])
    assert "experiment_id" in table.columns


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 6 artifacts not generated yet")
def test_no_nan_inf_attributions() -> None:
    data = np.load(NPZ, allow_pickle=True)
    for key in ("shap_values", "ebm_terms"):
        arr = data[key]
        assert np.isfinite(arr).all()
        assert arr.shape[1] == 9
        assert arr.shape[0] == 5000


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 6 artifacts not generated yet")
def test_local_cases_follow_probability_rule() -> None:
    data = np.load(NPZ, allow_pickle=True)
    p = data["p_raw"]
    blob = json.loads(CASES.read_text(encoding="utf-8"))
    idx = blob["indices"]
    refs = np.asarray(data["row_ref"])
    assert idx["high_risk"] == int(np.flatnonzero(p == p.max())[np.argsort(refs[p == p.max()])[0]])
    assert idx["low_risk"] == int(np.flatnonzero(p == p.min())[np.argsort(refs[p == p.min()])[0]])
    median = float(np.median(p))
    assert abs(p[idx["median_risk"]] - median) == pytest.approx(np.min(np.abs(p - median)))
    table = pd.read_csv(TABLE4)
    assert "y_true_descriptive_only" in table.columns
    assert "local_rank_spearman" in table.columns


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 6 artifacts not generated yet")
def test_calibration_did_not_modify_ebm_and_sample_not_train() -> None:
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["ebm_parameters_unchanged_by_calibration"] is True
    assert audit["shap"]["tree_shap"] is False
    assert audit["sampling_used_labels"] is False
    sample = pd.read_csv(SAMPLE)
    assert (sample["split"] == "test").all()
    cal = json.loads(CAL_ATTR.read_text(encoding="utf-8"))
    assert cal["rank_spearman_raw_vs_scaled"] == pytest.approx(1.0)
    assert cal["ebm_parameters_unchanged_by_calibration"] is True


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 6 artifacts not generated yet")
def test_additivity_on_saved_shap() -> None:
    data = np.load(NPZ, allow_pickle=True)
    recon = data["shap_values"].sum(1) + float(data["base_value"][0])
    assert np.allclose(recon, data["decision"], atol=1e-8)


@pytest.mark.skipif(not artifacts_complete(), reason="Stage 6 artifacts not generated yet")
def test_output_files_contain_experiment_metadata() -> None:
    for path in TABLE_DIR.glob("*.csv"):
        frame = pd.read_csv(path)
        assert "experiment_id" in frame.columns, path.name
    meta = json.loads(NPZ_META.read_text(encoding="utf-8"))
    assert meta["experiment_id"] == "stage6-lc-ebm-explain-v1"
    cons = json.loads(CONSISTENCY.read_text(encoding="utf-8"))
    assert cons["passed"] is True
    assert cons["experiment_id"] == "stage6-lc-ebm-explain-v1"
    for stem in FIGURE_STEMS:
        assert (FIG_DIR / f"{stem}.png").exists(), stem
        assert (FIG_DIR / f"{stem}.pdf").exists(), stem
    manifest = json.loads((FIG_DIR / "figure_manifest.json").read_text(encoding="utf-8"))
    assert manifest["experiment_id"] == "stage6-lc-ebm-explain-v1"
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert set(audit["model_seeds"]) == {42, 123, 2024, 3407, 9999}
