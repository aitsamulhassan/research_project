"""Leakage tests for Stage 4A LendingClub preprocessing. No model training."""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data.audit_datasets import (  # noqa: E402
    EXPECTED_LC_FILENAME,
    RAW_DIR,
    sha256_file,
)
from preprocessing.lendingclub_preprocessor import (  # noqa: E402
    CATEGORICAL_FEATURES,
    FORBIDDEN_COLUMNS,
    NUMERIC_FEATURES,
    PREPROCESSOR_PATH,
    PRIMARY_PREDICTORS,
    RECORDED_LC_SHA256,
    LendingClubPreprocessor,
    load_split_predictor_frames,
)

SUMMARY = ROOT / "results" / "metrics" / "preprocessing_summary.json"
POLICY = ROOT / "docs" / "lendingclub_preprocessing_policy.csv"
RUN = ROOT / "audit" / "preprocessing_run.json"


@pytest.fixture(scope="module")
def splits() -> dict[str, pd.DataFrame]:
    return load_split_predictor_frames()


@pytest.fixture(scope="module")
def fitted(splits: dict[str, pd.DataFrame]) -> LendingClubPreprocessor:
    preprocessor = LendingClubPreprocessor()
    preprocessor.fit(splits["train"])
    return preprocessor


def test_preprocessing_is_fitted_only_on_training_data(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    train = splits["train"]
    state = fitted.fitted_state()
    for feature, categories in zip(CATEGORICAL_FEATURES, state["categories"]):
        observed = {str(v) for v in train[feature].dropna().unique()}
        assert set(categories) == observed
        assert "__MISSING__" not in set(categories)
    medians = dict(zip(NUMERIC_FEATURES, state["numeric_statistics"]))
    for feature in NUMERIC_FEATURES:
        train_median = float(pd.to_numeric(train[feature], errors="coerce").median())
        assert medians[feature] == pytest.approx(train_median)
    assert state["fitted_on_n_rows"] == len(train)


def test_validation_does_not_alter_fitted_parameters(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    before = copy.deepcopy(fitted.fitted_state())
    fitted.transform(splits["validation"].iloc[:2000])
    assert fitted.fitted_state() == before


def test_test_data_does_not_alter_fitted_parameters(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    before = copy.deepcopy(fitted.fitted_state())
    fitted.transform(splits["test"].iloc[:2000])
    assert fitted.fitted_state() == before


def test_transforming_additional_rows_does_not_change_fitted_state(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    before = copy.deepcopy(fitted.fitted_state())
    fitted.transform(splits["validation"].iloc[:100])
    fitted.transform(splits["validation"].iloc[:3000])
    fitted.transform(splits["test"].iloc[:100])
    fitted.transform(
        pd.concat(
            [splits["validation"].iloc[:50], splits["test"].iloc[:50]],
            ignore_index=True,
        )
    )
    assert fitted.fitted_state() == before


def test_raw_data_remains_unchanged() -> None:
    assert sha256_file(RAW_DIR / EXPECTED_LC_FILENAME) == RECORDED_LC_SHA256
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert summary["raw_modified"] is False


def test_feature_count_is_deterministic(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    train_head = splits["train"].iloc[:500]
    first = fitted.transform(train_head)
    second = fitted.transform(train_head)
    assert first.shape[1] == second.shape[1] == fitted.n_features_out_
    again = LendingClubPreprocessor()
    again.fit(splits["train"])
    assert again.n_features_out_ == fitted.n_features_out_
    assert list(again.get_feature_names_out()) == list(fitted.get_feature_names_out())


def test_transformed_schemas_are_identical(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    names = list(fitted.get_feature_names_out())
    x_train = fitted.transform(splits["train"].iloc[:25])
    x_val = fitted.transform(splits["validation"].iloc[:25])
    x_test = fitted.transform(splits["test"].iloc[:25])
    assert x_train.shape[1] == x_val.shape[1] == x_test.shape[1] == len(names)
    assert names == list(fitted.get_feature_names_out())


def test_target_is_never_passed_into_preprocessing(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    train = splits["train"].iloc[:20].copy()
    train["Default"] = 1
    with pytest.raises(ValueError, match="Forbidden columns"):
        fitted.fit(train)
    with pytest.raises(ValueError, match="Forbidden columns"):
        fitted.transform(train)
    with pytest.raises(ValueError, match="Target must not"):
        fitted.fit(splits["train"].iloc[:20], y=[0] * 20)


def test_issue_d_is_not_passed_into_preprocessing(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    frame = splits["train"].iloc[:10].copy()
    frame["issue_d"] = "Dec-2015"
    with pytest.raises(ValueError, match="issue_d"):
        fitted.transform(frame)


def test_experience_c_is_not_passed_into_preprocessing(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    frame = splits["train"].iloc[:10].copy()
    frame["experience_c"] = 1
    with pytest.raises(ValueError, match="experience_c"):
        fitted.transform(frame)


def test_id_is_not_passed_into_preprocessing(
    splits: dict[str, pd.DataFrame], fitted: LendingClubPreprocessor
) -> None:
    frame = splits["train"].iloc[:10].copy()
    frame["id"] = 1
    with pytest.raises(ValueError, match=r"\bid\b"):
        fitted.transform(frame)


def test_forbidden_set_matches_frozen_exclusions() -> None:
    assert FORBIDDEN_COLUMNS == {"Default", "issue_d", "experience_c", "id", "title", "desc"}
    assert "issue_d" not in PRIMARY_PREDICTORS
    assert "experience_c" not in PRIMARY_PREDICTORS
    assert "Default" not in PRIMARY_PREDICTORS
    assert "id" not in PRIMARY_PREDICTORS


def test_unseen_category_does_not_refit(
    fitted: LendingClubPreprocessor, splits: dict[str, pd.DataFrame]
) -> None:
    before = copy.deepcopy(fitted.fitted_state())
    frame = splits["train"].iloc[:5].copy()
    frame["purpose"] = "UNSEEN_PURPOSE_FOR_TEST_ONLY"
    transformed = fitted.transform(frame)
    assert transformed.shape[1] == fitted.n_features_out_
    assert fitted.fitted_state() == before


def test_saved_artifacts_exist_and_agree_with_fit(fitted: LendingClubPreprocessor) -> None:
    assert POLICY.is_file()
    assert SUMMARY.is_file()
    assert RUN.is_file()
    assert PREPROCESSOR_PATH.is_file()
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    assert summary["fitted_on"] == "LendingClub TRAIN only"
    assert summary["n_features_out"] == fitted.n_features_out_
    assert summary["modeling_started"] is False
    assert summary["uci_merged"] is False
    policy = pd.read_csv(POLICY)
    assert list(policy["column"]) == PRIMARY_PREDICTORS
    assert set(policy["fit_on"]) <= {"TRAIN_ONLY", "NONE"}
    run = json.loads(RUN.read_text(encoding="utf-8"))
    assert run["dataset_hash"] == RECORDED_LC_SHA256
    assert "git_commit" in run
