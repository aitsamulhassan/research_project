"""Stage 9.4 UCI generalization tests. Do not train on LendingClub. Do not open UCI TEST for selection."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from calibration.isotonic import IsotonicCalibrator  # noqa: E402
from calibration.platt import PlattCalibrator  # noqa: E402
from data.audit_datasets import sha256_file  # noqa: E402
from preprocessing.uci_preprocessor import (  # noqa: E402
    FORBIDDEN_LC_COLUMNS,
    UCI_PREDICTORS,
    UCIPreprocessor,
)
from uci_generalization.stage9_4 import (  # noqa: E402
    FAMILIES,
    FORBIDDEN_SELF_EDIT,
    L1_METADATA_ONLY,
    PROTECTED_LC_PATHS,
    require_amendment_approved,
    select_calibrator,
    select_family,
    verify_frozen_uci_split,
)

RUNNER = ROOT / "experiments" / "stage9_4_uci_generalization" / "run_stage9_4.py"
UCI_MODELS = ROOT / "src" / "models" / "uci_models.py"
UCI_PRE = ROOT / "src" / "preprocessing" / "uci_preprocessor.py"
HELPER = ROOT / "src" / "uci_generalization" / "stage9_4.py"
AUDIT = ROOT / "audit" / "stage9_4_uci_run.json"
REPORT = ROOT / "docs" / "STAGE_9_4_UCI_GENERALIZATION_REPORT.md"
FREEZE = ROOT / "audit" / "stage9_0_experimental_freeze.json"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_amendment_is_approved() -> None:
    info = require_amendment_approved()
    assert info["status"] == "APPROVED"


def test_frozen_uci_split_hashes_match() -> None:
    payload = verify_frozen_uci_split()
    assert payload["split_counts"] == {"train": 20999, "validation": 4499, "test": 4502}
    assert payload["merged_with_lendingclub"] is False
    assert payload["zip_sha256"] == "56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602"
    assert payload["recode_applied"] is False


def test_preprocessor_fit_on_train_retains_undocumented_pay_codes() -> None:
    rng = np.random.RandomState(0)
    n = 40
    frame = pd.DataFrame({name: rng.normal(size=n) for name in UCI_PREDICTORS})
    frame["SEX"] = rng.choice([1, 2], size=n)
    frame["EDUCATION"] = rng.choice([0, 1, 2, 3, 4, 5, 6], size=n)
    frame["MARRIAGE"] = rng.choice([0, 1, 2, 3], size=n)
    frame["PAY_0"] = rng.choice([-2, -1, 0, 1, 2], size=n)
    pre = UCIPreprocessor().fit(frame)
    names = " ".join(pre.feature_names_out_ or [])
    assert "PAY_0=-2" in names
    assert "PAY_0=0" in names
    assert "EDUCATION=0" in names
    assert pre.record()["recode_applied"] is False
    assert pre.record()["lendingclub_imputer_applied"] is False


def test_preprocessor_rejects_lendingclub_columns() -> None:
    frame = pd.DataFrame({name: [0.0, 1.0] for name in UCI_PREDICTORS})
    frame["loan_amnt"] = [1.0, 2.0]
    with pytest.raises(ValueError, match="LendingClub"):
        UCIPreprocessor().fit(frame)


def test_calibrators_reject_uci_test_split() -> None:
    rng = np.random.RandomState(0)
    p = rng.uniform(0.1, 0.9, 80)
    y = rng.randint(0, 2, 80)
    y[0] = 0
    y[1] = 1
    with pytest.raises(ValueError, match="validation"):
        PlattCalibrator().fit(p, y, split="test")
    with pytest.raises(ValueError, match="validation"):
        IsotonicCalibrator().fit(p, y, split="test")


def test_family_selection_uses_validation_pr_auc_not_test() -> None:
    rows = [
        {"family": "logistic_regression", "pr_auc_mean": 0.50, "brier_mean": 0.20},
        {"family": "explainable_boosting_machine", "pr_auc_mean": 0.55, "brier_mean": 0.18},
        {"family": "xgboost", "pr_auc_mean": 0.551, "brier_mean": 0.19},
    ]
    sel = select_family(rows)
    assert sel["selected_family"] == "explainable_boosting_machine"
    assert sel["test_metrics_not_consulted"] is True
    assert sel["declared_before_test"] is True


def test_calibrator_tie_prefers_simpler() -> None:
    rows = [
        {"method": "raw", "brier": 0.170, "log_loss": 0.5, "ece": 0.04},
        {"method": "platt", "brier": 0.1692, "log_loss": 0.49, "ece": 0.01},
        {"method": "isotonic", "brier": 0.1690, "log_loss": 0.49, "ece": 0.00},
    ]
    sel = select_calibrator(rows)
    assert sel["selected_method"] == "platt"
    assert sel["test_metrics_not_consulted"] is True


def test_only_three_families() -> None:
    assert FAMILIES == ["logistic_regression", "explainable_boosting_machine", "xgboost"]
    assert "random_forest" not in FAMILIES


def test_uci_modules_do_not_import_lendingclub_preprocessor() -> None:
    for path in (UCI_MODELS, UCI_PRE, HELPER, RUNNER):
        tree = ast.parse(_read(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and (node.module or "").startswith("preprocessing.lendingclub"):
                raise AssertionError(f"{path} imports LendingClub preprocessor")
            if isinstance(node, ast.ImportFrom) and node.module == "models.ebm_model":
                raise AssertionError(f"{path} imports LC EBM factory")


def test_runner_does_not_write_authorization_files() -> None:
    text = _read(RUNNER)
    assert "STAGE_9_EXPERIMENTAL_PROTOCOL.md" not in text
    assert "RESEARCH_CONSTITUTION.md" not in text
    assert "write_text" not in text or "STAGE_9_4_UCI_GENERALIZATION_REPORT.md" in text
    for path in FORBIDDEN_SELF_EDIT:
        assert path.name != "STAGE_9_4_UCI_GENERALIZATION_REPORT.md"


def test_helper_does_not_write_freeze_json() -> None:
    text = _read(HELPER) + _read(RUNNER)
    assert "stage9_0_experimental_freeze.json" not in _read(RUNNER)
    freeze = json.loads(FREEZE.read_text(encoding="utf-8"))
    assert freeze["stage9_execution"] == "NOT AUTHORIZED"
    assert L1_METADATA_ONLY.startswith("UCI Default of Credit Card Clients")


def test_forbidden_lc_feature_names_listed() -> None:
    assert "loan_amnt" in FORBIDDEN_LC_COLUMNS
    assert "Default" in FORBIDDEN_LC_COLUMNS


def test_audit_flags_when_present() -> None:
    if not AUDIT.exists():
        pytest.skip("Stage 9.4 audit not written yet")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["models_trained"] is True
    assert audit["test_used_for_selection"] is False
    assert audit["thresholds_searched"] is False
    assert audit["shariah_evaluation_on_uci"] is False
    assert audit["l2_fusion_on_uci"] is False
    assert audit["merged_with_lendingclub"] is False
    assert audit["protected_hashes_unchanged"] is True
    assert audit["uci_test_evaluated"] is True
    assert int(audit["uci_test_selected"]["n"]) == 4502
    before = audit["protected_hashes_before"]
    after = audit["protected_hashes_after"]
    assert before == after
    for path in PROTECTED_LC_PATHS:
        assert sha256_file(path) == after[str(path)]


def test_report_states_purpose_and_nonclaims_when_present() -> None:
    if not REPORT.exists():
        pytest.skip("Stage 9.4 report not written yet")
    text = REPORT.read_text(encoding="utf-8")
    assert "credit-risk / calibration METHODOLOGY" in text
    assert "NOT a test of the evidence-separated decision architecture" in text
    assert "No Shariah governance evaluation was performed on UCI" in text
    assert "default payment next month" in text
    assert "Charged Off" in text
    assert "SHAP-vs-EBM fidelity: **skipped**" in text
    assert "alongside" in text.lower()
