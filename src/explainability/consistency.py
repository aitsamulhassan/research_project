"""Automated explanation-consistency checks. Attribution, not causality."""

from __future__ import annotations

import numpy as np
import pandas as pd

from explainability.shap_additive import additive_shap
from preprocessing.lendingclub_preprocessor import FORBIDDEN_COLUMNS, PRIMARY_PREDICTORS

EXCLUDED = ("id", "issue_d", "experience_c", "title", "desc")


def _item(name: str, passed: bool, detail: str) -> dict:
    return {"check": name, "passed": bool(passed), "detail": detail}


def check_predictor_identities(names: list[str] | tuple[str, ...]) -> dict:
    names_t = tuple(names)
    passed = names_t == tuple(PRIMARY_PREDICTORS)
    return _item(
        "exactly_nine_predictors",
        passed,
        f"names={list(names_t)}",
    )


def check_excluded_and_target_absent(names: list[str] | tuple[str, ...]) -> dict:
    present = [c for c in (*EXCLUDED, "Default") if c in names]
    forbidden_overlap = FORBIDDEN_COLUMNS.intersection(names)
    passed = not present and not forbidden_overlap
    return _item("no_excluded_fields_or_target", passed, f"violations={present or sorted(forbidden_overlap)}")


def check_finite_attributions(shap_values: np.ndarray, ebm_terms: np.ndarray) -> list[dict]:
    out = []
    for label, arr in (("shap", shap_values), ("ebm", ebm_terms)):
        finite = bool(np.isfinite(arr).all())
        out.append(_item(f"no_nan_inf_{label}", finite, f"shape={tuple(arr.shape)}"))
    return out


def check_additivity(shap_values: np.ndarray, base_value: float, decision: np.ndarray) -> dict:
    recon = np.asarray(shap_values).sum(axis=1) + float(base_value)
    err = float(np.max(np.abs(recon - np.asarray(decision))))
    return _item("shap_additivity_logit_link", err < 1e-8, f"max_abs_error={err}")


def check_repeatability(terms: np.ndarray, background_means: np.ndarray) -> dict:
    a = additive_shap(terms, background_means)
    b = additive_shap(terms, background_means)
    ok = bool(np.allclose(a, b, atol=0.0, rtol=0.0) or np.array_equal(a, b))
    if not ok:
        ok = bool(np.allclose(a, b, atol=1e-15))
    return _item("repeatable_additive_shap", ok, "identical closed-form evaluation")


def check_sample_deterministic(n: int, size: int, seed: int, saved_iloc: np.ndarray) -> dict:
    from explainability.sampling import deterministic_indices

    expected = deterministic_indices(n, size, seed)
    ok = bool(np.array_equal(expected, np.asarray(saved_iloc)))
    return _item("deterministic_explanation_sample", ok, f"n={n} size={size} seed={seed}")


def run_consistency_checks(
    *,
    feature_names: list[str] | tuple[str, ...],
    shap_values: np.ndarray,
    ebm_terms: np.ndarray,
    base_value: float,
    decision: np.ndarray,
    background_means: np.ndarray,
    test_n: int,
    sample_n: int,
    sample_seed: int,
    source_iloc: np.ndarray,
    seed_feature_names: list[str] | tuple[str, ...],
) -> dict:
    checks = [
        check_predictor_identities(feature_names),
        check_excluded_and_target_absent(feature_names),
        check_predictor_identities(seed_feature_names),
        check_additivity(shap_values, base_value, decision),
        check_repeatability(ebm_terms, background_means),
        check_sample_deterministic(test_n, sample_n, sample_seed, source_iloc),
        _item("shap_columns_match_predictors", shap_values.shape[1] == len(PRIMARY_PREDICTORS), f"p={shap_values.shape[1]}"),
        _item("ebm_columns_match_predictors", ebm_terms.shape[1] == len(PRIMARY_PREDICTORS), f"p={ebm_terms.shape[1]}"),
        _item(
            "identical_seed_feature_order",
            tuple(seed_feature_names) == tuple(PRIMARY_PREDICTORS),
            "seed experiments use the frozen predictor order",
        ),
    ]
    checks.extend(check_finite_attributions(shap_values, ebm_terms))
    passed = all(c["passed"] for c in checks)
    return {"passed": passed, "checks": checks}
