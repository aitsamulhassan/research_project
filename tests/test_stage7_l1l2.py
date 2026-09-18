"""Stage 7 v2 L1/L2 tests. Synthetic/unit fixtures only; no protected TEST split."""

from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shariah.engine import AMENDMENT_ID, ENGINE_VERSION, evaluate, from_mapping  # noqa: E402
from shariah.l1 import L1_LC_STATUS, assess_dataset_readiness  # noqa: E402
from shariah.l2 import (  # noqa: E402
    EVALUATION_MODE_PER_APPLICATION,
    evaluate_application_governance,
    evaluate_lendingclub_application,
    extract_application_governance_evidence,
    inject_firewall_field_for_boundary_test,
    result_contains_certification_claim,
    semantic_evidence_payload,
)
from shariah.schema import FIREWALL_FIELDS, OUTCOMES  # noqa: E402

CASES = json.loads((ROOT / "data" / "synthetic" / "shariah_governance_cases.json").read_text(encoding="utf-8"))
FIXTURES = json.loads((ROOT / "data" / "synthetic" / "lendingclub_l2_schema_fixtures.json").read_text(encoding="utf-8"))
CATALOG = json.loads((ROOT / "docs" / "shariah" / "rule_catalog.json").read_text(encoding="utf-8"))
TS = "2026-09-15T00:00:00+00:00"
ISLAMIC_CONTRACTS = {
    "Murabahah",
    "Ijarah",
    "Ijarah_Muntahia_Bittamleek",
    "Musharakah",
    "Mudarabah",
    "Qard",
    "Salam",
    "Istisna",
}


def _fixture(key: str) -> dict:
    return dict(next(row for row in FIXTURES["fixtures"] if row["_fixture_key"] == key))


def _case(case_id: str) -> dict:
    row = next(c for c in CASES["cases"] if c["case_id"] == case_id)
    skip = {"expected_layer_a", "expected_status", "note"}
    return {k: v for k, v in row.items() if k not in skip}


def test_a_lendingclub_l1_insufficient_schema() -> None:
    result = assess_dataset_readiness("lendingclub")
    assert result["readiness_status"] == L1_LC_STATUS
    assert result["readiness_status"] == "INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION"
    assert result["is_applicant_level_ruling"] is False
    assert result["layer"] == "L1"
    assert result["evaluation_mode"] == "DATASET_INTEGRATION"
    assert result["certification_claim"] is False
    assert not result["contractual_schema_fields_present"]
    alias = assess_dataset_readiness("lendingclub_granting_v0.1")
    assert alias["readiness_status"] == L1_LC_STATUS


def test_b_two_rows_have_separate_record_references() -> None:
    ev_a, meta_a = extract_application_governance_evidence(_fixture("lc-unit-001"))
    ev_b, meta_b = extract_application_governance_evidence(_fixture("lc-unit-003"))
    assert meta_a["record_reference_hash"] != meta_b["record_reference_hash"]
    assert ev_a.case_id != ev_b.case_id
    assert meta_a["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION
    assert meta_b["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION
    out_a = evaluate_application_governance(ev_a, l2_meta=meta_a, timestamp=TS)
    out_b = evaluate_application_governance(ev_b, l2_meta=meta_b, timestamp=TS)
    assert out_a["record_reference_hash"] != out_b["record_reference_hash"]
    assert out_a["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION
    assert out_b["l2"]["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION


def test_c_purpose_invariance() -> None:
    row_car = _fixture("lc-unit-001")
    row_home = _fixture("lc-unit-001")
    row_home["_fixture_key"] = "lc-unit-001-purpose-home"
    row_home["id"] = 10101
    row_home["purpose"] = "home_improvement"
    assert row_car["purpose"] != row_home["purpose"]
    for key in FIREWALL_FIELDS:
        if key in {"purpose", "id"}:
            continue
        assert row_car.get(key) == row_home.get(key)
    ev_car, meta_car = extract_application_governance_evidence(row_car)
    ev_home, meta_home = extract_application_governance_evidence(row_home)
    assert "purpose" not in ev_car.as_dict()
    assert "purpose" not in ev_home.as_dict()
    assert "purpose" not in ev_car.extra
    assert semantic_evidence_payload(ev_car) == semantic_evidence_payload(ev_home)
    assert meta_car["evidence_hash"] == meta_home["evidence_hash"]
    assert meta_car["record_reference_hash"] != meta_home["record_reference_hash"]
    out_car = evaluate_application_governance(ev_car, l2_meta=meta_car, timestamp=TS)
    out_home = evaluate_application_governance(ev_home, l2_meta=meta_home, timestamp=TS)
    assert out_car["overall_governance_status"] == out_home["overall_governance_status"]
    assert out_car["layer_a_completeness"]["layer_a"] == out_home["layer_a_completeness"]["layer_a"]


@pytest.mark.parametrize("field", FIREWALL_FIELDS)
def test_d_firewall_boundary_injection(field: str) -> None:
    ev, meta = extract_application_governance_evidence(_fixture("lc-unit-001"))
    assert field not in ev.as_dict()
    assert field not in ev.extra
    injected = inject_firewall_field_for_boundary_test(ev, field, "INJECTED_BOUNDARY_VALUE")
    assert injected.extra[field] == "INJECTED_BOUNDARY_VALUE"
    assert injected.contract_type == "unknown"
    assert injected.contract_type not in ISLAMIC_CONTRACTS
    result = evaluate(injected, timestamp=TS)
    arch003 = next(row for row in result["rule_evaluations"] if row["rule_id"] == "SH-ARCH-003")
    assert arch003["rule_result"] == "REVIEW"
    assert result["contract_type"] == "unknown"


def test_e_purpose_car_is_not_ijarah() -> None:
    row = _fixture("lc-unit-001")
    assert row["purpose"] == "car"
    ev, meta = extract_application_governance_evidence(row)
    assert ev.contract_type == "unknown"
    assert ev.contract_type != "Ijarah"
    for purpose in ("car", "home_improvement", "small_business", "renewable_energy", "wedding", "credit_card"):
        variant = dict(row)
        variant["_fixture_key"] = f"purpose-{purpose}"
        variant["purpose"] = purpose
        extracted, _ = extract_application_governance_evidence(variant)
        assert extracted.contract_type == "unknown"
        assert extracted.contract_type not in ISLAMIC_CONTRACTS
        assert "purpose" not in extracted.as_dict()


def test_f_missing_evidence_is_insufficient_never_pass() -> None:
    result = evaluate_lendingclub_application(_fixture("lc-unit-001"), timestamp=TS)
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert result["overall_governance_status"] != "PASS"
    assert result["layer_a_completeness"]["layer_a"] == "INSUFFICIENT"
    assert result["missing_evidence"]
    assert "verified_contract_type" in result["missing_evidence"]


def test_g_certification_boundary() -> None:
    result = evaluate_lendingclub_application(_fixture("lc-unit-001"), timestamp=TS)
    assert result["certification_claim"] is False
    assert result["overall_governance_status"] in OUTCOMES
    assert result_contains_certification_claim(result) is False
    blob_status = json.dumps(
        {"status": result["overall_governance_status"], "claim": result["certification_claim"]},
        ensure_ascii=True,
    ).lower()
    assert "shariah compliant" not in blob_status
    assert "halal loan" not in blob_status


def test_h_synthetic_evidence_sensitive_cases_preserved() -> None:
    assert CASES["version"].startswith("stage7-synthetic")
    for row in CASES["cases"]:
        result = evaluate(from_mapping(_case(row["case_id"])), timestamp=TS)
        assert result["overall_governance_status"] == row["expected_status"], row["case_id"]
        assert result["layer_a_completeness"]["layer_a"] == row["expected_layer_a"], row["case_id"]
        assert result["synthetic"] is True


def test_cache_keeps_per_row_identity() -> None:
    cache: dict[str, dict] = {}
    first = evaluate_lendingclub_application(_fixture("lc-unit-001"), timestamp=TS, cache=cache)
    second = evaluate_lendingclub_application(_fixture("lc-unit-002"), timestamp=TS, cache=cache)
    assert first["cache_hit"] is False
    assert second["cache_hit"] is True
    assert first["evidence_hash"] == second["evidence_hash"]
    assert first["record_reference_hash"] != second["record_reference_hash"]
    assert first["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION
    assert second["evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION
    assert first["l1"]["readiness_status"] == L1_LC_STATUS
    assert second["l1"]["is_applicant_level_ruling"] is False


def test_shr001_not_reconstructed() -> None:
    assert all(rule["rule_id"] != "SHR-001" for rule in CATALOG["rules"])
    retired = CATALOG["unsupported_retired_identifiers"]
    assert retired[0]["rule_id"] == "SHR-001"
    assert retired[0]["status"] == "UNSUPPORTED_RETIRED"
    assert retired[0]["reconstructed"] is False
    for path in (ROOT / "src" / "shariah").glob("*.py"):
        assert "SHR-001" not in path.read_text(encoding="utf-8")


def test_no_expert_validated_and_no_new_aaoifi_clause_engine() -> None:
    for rule in CATALOG["rules"]:
        assert rule.get("validation_status") != "EXPERT_VALIDATED"
        assert not rule.get("expert_validation_record")
    possession = next(rule for rule in CATALOG["rules"] if rule["rule_id"] == "SH-AAOIFI-SS8-POSSESSION")
    assert possession["executable"] is False
    result = evaluate_lendingclub_application(_fixture("lc-unit-001"), timestamp=TS)
    assert result["any_expert_validated"] is False
    assert ENGINE_VERSION == "stage7-shariah-engine-v1"
    assert result["amendment_id"] == AMENDMENT_ID


def test_l2_does_not_copy_firewall_or_infer_from_purpose() -> None:
    source = (ROOT / "src" / "shariah" / "l2.py").read_text(encoding="utf-8")
    assert "car" not in source
    ev, meta = extract_application_governance_evidence(_fixture("lc-unit-001"))
    assert meta["purpose_used_as_contract_type"] is False
    assert meta["source_fields_copied_into_evidence"] == []
    for field in FIREWALL_FIELDS:
        assert field not in ev.as_dict()
    tree = ast.parse(source)
    assert tree is not None


def test_raw_id_is_not_published_in_l2_result() -> None:
    result = evaluate_lendingclub_application(_fixture("lc-unit-001"), timestamp=TS)
    assert result.get("id") is None
    assert "101" not in result["record_reference_hash"]
    assert result["case_id"].startswith("l2:lendingclub:")
    dumped = json.dumps(result, ensure_ascii=True)
    assert '"id": 101' not in dumped
    assert "unit fixture title a" not in dumped
    assert "900xx" not in dumped


V2_AUDIT = ROOT / "audit" / "stage7_v2_governance_run.json"


@pytest.mark.skipif(not V2_AUDIT.exists(), reason="Stage 7 v2 audit not generated yet")
def test_v2_audit_records_methodology_gates() -> None:
    audit = json.loads(V2_AUDIT.read_text(encoding="utf-8"))
    assert audit["amendment_id"] == "AMENDMENT-SHARIAH-001"
    assert audit["l1_status"] == L1_LC_STATUS
    assert audit["l2_evaluation_mode"] == EVALUATION_MODE_PER_APPLICATION
    assert audit["any_expert_validated"] is False
    assert audit["certification_claim_policy"] is False
    assert audit["stage8_implemented"] is False
    assert audit["stage9"] == "BLOCKED"
