"""Stage 7 rule-engine tests. Synthetic cases only; no credit-model calls."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shariah.engine import ENGINE_VERSION, evaluate, from_mapping  # noqa: E402
from shariah.rules import Rule, load_catalog  # noqa: E402
from shariah.schema import LENDINGCLUB_PREDICTORS  # noqa: E402

CASES = json.loads((ROOT / "data" / "synthetic" / "shariah_governance_cases.json").read_text(encoding="utf-8"))
CATALOG = json.loads((ROOT / "docs" / "shariah" / "rule_catalog.json").read_text(encoding="utf-8"))
TS = "2026-09-15T00:00:00+00:00"


def _case(case_id: str) -> dict:
    row = next(c for c in CASES["cases"] if c["case_id"] == case_id)
    skip = {"expected_layer_a", "expected_status", "note"}
    return {k: v for k, v in row.items() if k not in skip}


def test_missing_evidence_is_insufficient() -> None:
    result = evaluate(from_mapping(_case("SYN-MUR-MISSING-PAY-001")), timestamp=TS)
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert result["layer_a_completeness"]["layer_a"] == "INSUFFICIENT"


def test_ambiguous_contract_is_review() -> None:
    result = evaluate(from_mapping(_case("SYN-AMBIGUOUS-001")), timestamp=TS)
    assert result["overall_governance_status"] == "REVIEW"


def test_unverified_rule_cannot_execute() -> None:
    row = next(r for r in CATALOG["rules"] if r["rule_id"] == "SH-AAOIFI-SS8-POSSESSION")
    assert row["executable"] is False
    with pytest.raises(RuntimeError, match="not executable"):
        Rule(row).evaluate(from_mapping(_case("SYN-LC-001")))


def test_verified_rule_is_deterministic() -> None:
    ev = from_mapping(_case("SYN-MUR-PAY-CUSTOMER-001"))
    a = evaluate(ev, timestamp=TS)
    b = evaluate(ev, timestamp=TS)
    assert a == b
    assert a["overall_governance_status"] == "NOT_STRUCTURABLE_WITHOUT_REDESIGN"


def test_every_applicable_outcome_has_rule_id_and_provenance() -> None:
    result = evaluate(from_mapping(_case("SYN-MUR-OPS-COMPLETE-001")), timestamp=TS)
    for row in result["rule_evaluations"]:
        assert row["rule_id"]
        assert row["authority"]
        assert row["source_document"]
        assert row["source_version"]
        assert row["source_url"]
        assert row["timestamp"] == TS


def test_unknown_evidence_is_not_pass() -> None:
    result = evaluate(from_mapping(_case("SYN-UNKNOWN-NOT-PASS-001")), timestamp=TS)
    assert result["overall_governance_status"] != "PASS"
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"


def test_synthetic_cases_are_marked_synthetic() -> None:
    assert CASES["version"].startswith("stage7-synthetic")
    for row in CASES["cases"]:
        assert row["synthetic"] is True
        result = evaluate(from_mapping(_case(row["case_id"])), timestamp=TS)
        assert result["synthetic"] is True
        assert result["label"] == "Synthetic governance test case"


def test_engine_source_has_no_ml_imports() -> None:
    forbidden = {"sklearn", "interpret", "shap", "xgboost", "joblib"}
    for path in (ROOT / "src" / "shariah").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module.split(".")[0]]
            for name in names:
                assert name not in forbidden, f"{path.name} imports {name}"


def test_lendingclub_predictors_are_not_shariah_variables() -> None:
    payload = _case("SYN-LC-001")
    payload["fico_n"] = 720
    result = evaluate(from_mapping(payload), timestamp=TS)
    leak = next(r for r in result["rule_evaluations"] if r["rule_id"] == "SH-ARCH-003")
    assert leak["rule_result"] == "REVIEW"
    for name in LENDINGCLUB_PREDICTORS:
        assert name not in ("contract_type", "payment_channel", "invoice_name_status")


def test_conflicting_unresolved_murabaha_coverage_is_review() -> None:
    result = evaluate(from_mapping(_case("SYN-MUR-OPS-COMPLETE-001")), timestamp=TS)
    assert "CONF-AAOIFI-SS8-VS-SBP-MUR-OPS" in result["unresolved_conflicts"]
    assert result["overall_governance_status"] == "REVIEW"


def test_rule_versioning_and_engine_id() -> None:
    catalog = load_catalog()
    ids = [r.rule_id for r in catalog]
    assert ids == sorted(ids, key=lambda _: ids.index(_))
    assert ENGINE_VERSION == "stage7-shariah-engine-v1"
    versions = {r.payload["rule_version"] for r in catalog}
    assert versions


def test_engine_can_return_insufficient_information() -> None:
    result = evaluate(from_mapping(_case("SYN-LC-001")), timestamp=TS)
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert result["certification_claim"] is False


def test_expected_synthetic_statuses() -> None:
    for row in CASES["cases"]:
        result = evaluate(from_mapping(_case(row["case_id"])), timestamp=TS)
        assert result["overall_governance_status"] == row["expected_status"], row["case_id"]
        assert result["layer_a_completeness"]["layer_a"] == row["expected_layer_a"], row["case_id"]
