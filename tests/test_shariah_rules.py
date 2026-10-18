"""Stage 7 rule-engine tests. Synthetic cases only; no credit-model calls."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision.config_load import load_policy_config  # noqa: E402
from decision.decision_engine import fuse_decision  # noqa: E402
from decision.policy_matrix import build_matrix  # noqa: E402
from decision.stage8_v2 import EXPECTED_T_HIGH, EXPECTED_T_LOW  # noqa: E402
from shariah.applicability import APPLICABILITY_VERSION  # noqa: E402
from shariah.engine import ENGINE_VERSION, evaluate, from_mapping  # noqa: E402
from shariah.rules import Rule, load_catalog  # noqa: E402
from shariah.schema import LENDINGCLUB_PREDICTORS  # noqa: E402

CASES = json.loads((ROOT / "data" / "synthetic" / "shariah_governance_cases.json").read_text(encoding="utf-8"))
CATALOG = json.loads((ROOT / "docs" / "shariah" / "rule_catalog.json").read_text(encoding="utf-8"))
HISTORICAL_AUDIT = json.loads((ROOT / "results" / "shariah" / "rule_evaluations.json").read_text(encoding="utf-8"))
TS = "2026-09-15T00:00:00+00:00"
LIVE_ENGINE = "stage7-shariah-engine-v2-scope-gated"
HISTORICAL_ENGINE = "stage7-shariah-engine-v1"
MATRIX = build_matrix(load_policy_config()["governance_policy"]["matrix"])
SCOPE_GATED_HARD_STOPS = {
    "SYN-MUR-PAY-CUSTOMER-001": {
        "rule_id": "SH-SBP-MUR-PAY-001",
        "diagnostic_reason": (
            "Payment to the customer rather than the supplier/escrow/approved-agent path "
            "does not meet IBD Circular 01 of 2012 paragraph 4."
        ),
    },
    "SYN-MUR-NO-SB-001": {
        "rule_id": "SH-SBP-SGF-002",
        "diagnostic_reason": (
            "SGF Section 3.B.ii requires prior Shariah Board approval before an IBI "
            "offers or launches a product or service."
        ),
    },
    "SYN-SECP-CLAIM-NO-CERT-001": {
        "rule_id": "SH-SECP-SGR-SEC-001",
        "diagnostic_reason": (
            "SGR 2023 Regulation 7(2) states that no security shall be called a Shariah "
            "compliant security unless a Shariah compliance certificate has been granted "
            "by the Commission."
        ),
    },
}


def _case(case_id: str) -> dict:
    row = next(c for c in CASES["cases"] if c["case_id"] == case_id)
    skip = {"expected_layer_a", "expected_status", "note"}
    return {k: v for k, v in row.items() if k not in skip}


def _fuse_low(status: str) -> str:
    return fuse_decision(0.05, status, EXPECTED_T_LOW, EXPECTED_T_HIGH, MATRIX)["final_decision"]


def _assert_live_scope_gated_hard_stop(case_row: dict, result: dict) -> None:
    """Historical fixture status stays on the JSON. The live screen withholds it."""
    spec = SCOPE_GATED_HARD_STOPS[case_row["case_id"]]
    assert case_row["expected_status"] == "NOT_STRUCTURABLE_WITHOUT_REDESIGN"
    assert result["engine_version"] == LIVE_ENGINE
    assert result["applicability_version"] == APPLICABILITY_VERSION
    assert result["overall_governance_status"] == "REVIEW"
    assert result["overall_governance_status"] != case_row["expected_status"]
    assert result["certification_claim"] is False
    assert result["layer_a_completeness"]["layer_a"] == case_row["expected_layer_a"]
    assert _fuse_low(result["overall_governance_status"]) == "HUMAN_REVIEW"
    rule = next(row for row in result["rule_evaluations"] if row["rule_id"] == spec["rule_id"])
    assert rule["diagnostic_predicate_applicable"] is True
    assert rule["diagnostic_predicate_result"] == "NOT_STRUCTURABLE_WITHOUT_REDESIGN"
    assert rule["diagnostic_predicate_reason"] == spec["diagnostic_reason"]
    assert rule["rule_result"] == "REVIEW"
    assert rule["reason"] != rule["diagnostic_predicate_reason"]
    assert "SCOPE_UNKNOWN" in rule["reason"]
    assert rule["applicability_decision"]["status"] == "SCOPE_UNKNOWN"
    assert rule["source_digest_verified"] is False
    assert rule["validation_status"] != "EXPERT_VALIDATED"


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
    case_row = next(row for row in CASES["cases"] if row["case_id"] == "SYN-MUR-PAY-CUSTOMER-001")
    _assert_live_scope_gated_hard_stop(case_row, a)


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
    assert ENGINE_VERSION == LIVE_ENGINE
    assert APPLICABILITY_VERSION == "stage7-applicability-scope-unknown-v1"
    assert HISTORICAL_AUDIT["experiment_id"] == "stage7-shariah-gov-v1"
    historical_versions = {row["engine_version"] for row in HISTORICAL_AUDIT["evaluations"]}
    assert historical_versions == {HISTORICAL_ENGINE}
    assert LIVE_ENGINE not in historical_versions
    versions = {r.payload["rule_version"] for r in catalog}
    assert versions


def test_engine_can_return_insufficient_information() -> None:
    result = evaluate(from_mapping(_case("SYN-LC-001")), timestamp=TS)
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert result["certification_claim"] is False


def test_expected_synthetic_statuses() -> None:
    for row in CASES["cases"]:
        result = evaluate(from_mapping(_case(row["case_id"])), timestamp=TS)
        assert result["layer_a_completeness"]["layer_a"] == row["expected_layer_a"], row["case_id"]
        assert result["synthetic"] is True
        if row["case_id"] in SCOPE_GATED_HARD_STOPS:
            _assert_live_scope_gated_hard_stop(row, result)
            continue
        assert result["overall_governance_status"] == row["expected_status"], row["case_id"]
