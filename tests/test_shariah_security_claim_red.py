"""RED-phase checks for the security-claim flag.

Synthetic inputs only. A certificate predicate PASS is not SECP applicability,
document authentication, or Shariah compliance. Failures are expected where
omitted, missing, explicit False, and non-Boolean values are collapsed.
Do not mark these tests xfail or skip.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision.decision_engine import fuse_decision  # noqa: E402
from decision.policy_matrix import build_matrix  # noqa: E402
from decision.stage8_v2 import (  # noqa: E402
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    load_frozen_thresholds,
)
from decision.config_load import load_policy_config  # noqa: E402
from shariah.engine import evaluate, from_mapping  # noqa: E402
from shariah.l2 import evaluate_lendingclub_application  # noqa: E402
from shariah.schema import FinancingEvidence  # noqa: E402

TS = "2026-09-15T00:00:00+00:00"
CLAIM = "claims_shariah_compliant_security"
CERTIFICATE = "secp_shariah_compliance_certificate"
SECP_RULE = "SH-SECP-SGR-SEC-001"
OMITTED = object()
REJECTION_NEEDLES = (
    "boolean",
    "bool",
    "invalid",
    "unsupported",
    "claim",
    "schema",
    "evidence",
    "missing",
    "omitted",
)
INVALID_CLAIMS = [
    pytest.param("true", id="string-true"),
    pytest.param("false", id="string-false"),
    pytest.param(0, id="integer-zero"),
    pytest.param(1, id="integer-one"),
    pytest.param("", id="empty-string"),
    pytest.param("not-a-boolean", id="arbitrary-text"),
    pytest.param([], id="empty-list"),
    pytest.param(["token"], id="nonempty-list"),
    pytest.param({}, id="empty-dict"),
    pytest.param({"claim": True}, id="nonempty-dict"),
]
TRUTHY_MALFORMED = [
    pytest.param("true", id="string-true"),
    pytest.param("false", id="string-false"),
    pytest.param(1, id="integer-one"),
    pytest.param("not-a-boolean", id="arbitrary-text"),
    pytest.param(["token"], id="nonempty-list"),
    pytest.param({"claim": True}, id="nonempty-dict"),
]
MATRIX = build_matrix(load_policy_config()["governance_policy"]["matrix"])


def _fuse(status: str) -> str:
    return fuse_decision(0.05, status, EXPECTED_T_LOW, EXPECTED_T_HIGH, MATRIX)["final_decision"]


def _payload(case_id: str, claim: object = OMITTED, certificate: object = None) -> dict:
    payload = {
        "case_id": case_id,
        "synthetic": True,
        "contract_type": "conventional_credit",
        "institution_class": "other",
        "jurisdiction": "PK",
        CERTIFICATE: certificate,
    }
    if claim is not OMITTED:
        payload[CLAIM] = claim
    return payload


def _rule(result: dict, rule_id: str) -> dict:
    return next(row for row in result["rule_evaluations"] if row["rule_id"] == rule_id)


def _assert_documented_rejection(exc: Exception) -> None:
    assert isinstance(exc, ValueError)
    text = str(exc).lower()
    assert text.strip()
    assert any(needle in text for needle in REJECTION_NEEDLES), text


def _observe(case_id: str, claim: object = OMITTED, certificate: object = None) -> dict | None:
    raw = _payload(case_id, claim, certificate)
    try:
        evidence = from_mapping(raw)
        result = evaluate(evidence, timestamp=TS)
    except ValueError as exc:
        _assert_documented_rejection(exc)
        return None
    layer = result["layer_a_completeness"]
    rule = _rule(result, SECP_RULE)
    status = result["overall_governance_status"]
    return {
        "omitted_from_mapping": CLAIM not in raw,
        "stored": evidence.claims_shariah_compliant_security,
        "stored_type": type(evidence.claims_shariah_compliant_security),
        "serialized": rule["input_evidence"][CLAIM],
        "required_fields": list(layer["required_fields"]),
        "certificate_required": CERTIFICATE in layer["required_fields"],
        "layer_a": layer["layer_a"],
        "applicable": rule["applicable"],
        "rule_result": rule["rule_result"],
        "reason": rule["reason"],
        "diagnostic_predicate_result": rule.get("diagnostic_predicate_result"),
        "diagnostic_predicate_applicable": rule.get("diagnostic_predicate_applicable"),
        "diagnostic_predicate_reason": rule.get("diagnostic_predicate_reason"),
        "applicability_status": (rule.get("applicability_decision") or {}).get("status"),
        "source_digest_verified": rule.get("source_digest_verified"),
        "overall": status,
        "fusion": _fuse(status),
        "certification_claim": result["certification_claim"],
        "validation_status": rule["validation_status"],
    }


def _token(value: object) -> str:
    if value == "":
        return "empty"
    if value == []:
        return "empty-list"
    if value == {}:
        return "empty-dict"
    return str(value).replace(" ", "-")


def _treated_as_explicit_no_claim(obs: dict) -> bool:
    return (
        obs["applicable"] is False
        and obs["rule_result"] == "NOT_APPLICABLE"
        and "no claim" in obs["reason"].lower()
    )


def test_dataclass_default_does_not_invent_an_explicit_false_claim() -> None:
    """Omitted construction must not become a statement that no claim was made."""
    evidence = FinancingEvidence(
        case_id="claim-default",
        synthetic=True,
        contract_type="conventional_credit",
        institution_class="other",
    )
    assert evidence.claims_shariah_compliant_security is not False


def test_omitted_mapping_is_not_recorded_as_explicit_false() -> None:
    obs = _observe("claim-omitted")
    assert obs is not None
    assert obs["omitted_from_mapping"] is True
    assert obs["stored"] is not False, (
        f"omitted claim stored={obs['stored']!r} type={obs['stored_type'].__name__} "
        f"serialized={obs['serialized']!r} rule={obs['rule_result']} reason={obs['reason']!r}"
    )
    assert obs["serialized"] is not False


def test_explicit_false_is_distinct_from_missing_at_the_rule() -> None:
    missing = _observe("claim-none", None)
    explicit = _observe("claim-false", False)
    assert missing is not None and explicit is not None
    assert missing["stored"] is None
    assert explicit["stored"] is False
    assert type(explicit["stored"]) is bool
    missing_rule = (missing["applicable"], missing["rule_result"], missing["reason"])
    explicit_rule = (explicit["applicable"], explicit["rule_result"], explicit["reason"])
    assert missing_rule != explicit_rule, (
        f"missing rule={missing_rule} explicit_false rule={explicit_rule} "
        f"missing_layer={missing['layer_a']} explicit_layer={explicit['layer_a']}"
    )


def test_exact_true_runs_certificate_check_without_certification() -> None:
    """Control. Exact True may open the certificate predicate. It does not certify anything."""
    obs = _observe("claim-true", True, certificate=True)
    assert obs is not None
    assert obs["stored"] is True
    assert obs["stored_type"] is bool
    assert obs["certificate_required"] is True
    assert obs["applicable"] is True
    assert obs["diagnostic_predicate_applicable"] is True
    assert obs["diagnostic_predicate_result"] == "PASS"
    assert obs["rule_result"] == "REVIEW"
    assert obs["diagnostic_predicate_result"] != obs["rule_result"]
    assert obs["diagnostic_predicate_reason"]
    assert obs["reason"] != obs["diagnostic_predicate_reason"]
    assert "SCOPE_UNKNOWN" in obs["reason"]
    assert obs["applicability_status"] == "SCOPE_UNKNOWN"
    assert obs["source_digest_verified"] is False
    assert obs["validation_status"] != "EXPERT_VALIDATED"
    assert obs["certification_claim"] is False
    assert obs["overall"] == "REVIEW"
    assert obs["overall"] != "PASS"
    assert obs["fusion"] == "HUMAN_REVIEW"
    assert obs["fusion"] != "APPROVE"


def test_exact_true_with_missing_certificate_is_insufficient() -> None:
    """Control. A real claim without certificate evidence stays nonaffirmative."""
    obs = _observe("claim-true-missing-cert", True, certificate=None)
    assert obs is not None
    assert obs["applicable"] is True
    assert obs["rule_result"] == "INSUFFICIENT_INFORMATION"
    assert obs["certificate_required"] is True
    assert obs["layer_a"] == "INSUFFICIENT"
    assert obs["overall"] == "INSUFFICIENT_INFORMATION"
    assert obs["fusion"] != "APPROVE"
    assert obs["certification_claim"] is False


def test_explicit_false_does_not_require_a_certificate() -> None:
    """Control. An explicit Boolean False is stored as False and does not open the certificate check."""
    obs = _observe("claim-explicit-false", False)
    assert obs is not None
    assert obs["omitted_from_mapping"] is False
    assert obs["stored"] is False
    assert obs["stored_type"] is bool
    assert obs["certificate_required"] is False
    assert obs["applicable"] is False
    assert obs["rule_result"] != "PASS"
    assert obs["overall"] != "PASS"
    assert obs["certification_claim"] is False


def test_omitted_claim_does_not_produce_a_positive_secp_result() -> None:
    """Control. Absence of a claim must not become a certificate PASS."""
    obs = _observe("claim-omitted-not-pass")
    assert obs is not None
    assert obs["rule_result"] != "PASS"
    assert obs["overall"] != "PASS"
    assert obs["fusion"] != "APPROVE"
    assert obs["certification_claim"] is False


@pytest.mark.parametrize("value", INVALID_CLAIMS)
def test_invalid_claim_is_not_a_silent_negative_claim(value: object) -> None:
    obs = _observe(f"claim-invalid-{_token(value)}", value)
    if obs is None:
        return
    assert obs["stored"] == value
    assert obs["stored_type"] is type(value)
    assert obs["overall"] != "PASS"
    assert obs["fusion"] != "APPROVE"
    assert obs["certification_claim"] is False
    assert not _treated_as_explicit_no_claim(obs), (
        f"value={value!r} type={type(value).__name__} applicable={obs['applicable']} "
        f"rule_result={obs['rule_result']} certificate_required={obs['certificate_required']} "
        f"layer_a={obs['layer_a']} overall={obs['overall']} reason={obs['reason']!r}"
    )


@pytest.mark.parametrize("value", TRUTHY_MALFORMED)
def test_truthy_malformed_claim_does_not_split_layer_a_from_the_rule(value: object) -> None:
    obs = _observe(f"claim-split-{_token(value)}", value)
    if obs is None:
        return
    assert obs["certificate_required"] is obs["applicable"], (
        f"value={value!r} type={type(value).__name__} certificate_required={obs['certificate_required']} "
        f"applicable={obs['applicable']} rule_result={obs['rule_result']} "
        f"required_fields={obs['required_fields']} reason={obs['reason']!r}"
    )


def test_ibi_exclusion_does_not_add_a_certificate_requirement() -> None:
    """An IBI record is outside this SECP rule. The claim must not impose a certificate through Layer A."""
    result = evaluate(
        from_mapping(
            {
                "case_id": "claim-ibi-true",
                "synthetic": True,
                "contract_type": "Murabahah",
                "institution_class": "IBI",
                "jurisdiction": "PK",
                "sb_prior_product_approval": True,
                "sb_approved_agreements_and_process_flows": True,
                "invoice_name_status": "bank_account_client",
                "payment_channel": "supplier",
                CLAIM: True,
            }
        ),
        timestamp=TS,
    )
    rule = _rule(result, SECP_RULE)
    required = result["layer_a_completeness"]["required_fields"]
    assert rule["applicable"] is False
    assert result["certification_claim"] is False
    assert CERTIFICATE not in required, (
        f"required={required} rule={rule['rule_result']} reason={rule['reason']!r} "
        f"layer={result['layer_a_completeness']['layer_a']} overall={result['overall_governance_status']}"
    )


def test_lendingclub_l2_missing_claim_is_not_an_secp_security() -> None:
    """Control. An ordinary LendingClub row is not classified by this claim field."""
    result = evaluate_lendingclub_application(
        {"_fixture_key": "claim-lc", "purpose": "car", "id": "synthetic-claim"},
        timestamp=TS,
        synthetic=True,
    )
    evidence = result["rule_evaluations"][0]["input_evidence"]
    rule = _rule(result, SECP_RULE)
    assert result["contract_type"] == "unknown"
    assert "purpose" not in evidence
    assert evidence[CLAIM] is None
    assert rule["applicable"] is False
    assert rule["rule_result"] != "PASS"
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert result["certification_claim"] is False
    assert _fuse(result["overall_governance_status"]) != "APPROVE"


def test_documentary_string_false_remains_nonaffirmative() -> None:
    """Control. The earlier invoice-approval Boolean correction still rejects a false token."""
    result = evaluate(
        from_mapping(
            {
                "case_id": "claim-doc-control",
                "synthetic": True,
                "contract_type": "Murabahah",
                "institution_class": "IBI",
                "jurisdiction": "PK",
                "sb_prior_product_approval": True,
                "sb_approved_agreements_and_process_flows": True,
                "invoice_name_status": "client_only",
                "shariah_advisor_invoice_exception_approval": "false",
                "payment_channel": "supplier",
            }
        ),
        timestamp=TS,
    )
    invoice = _rule(result, "SH-SBP-MUR-INV-001")
    assert invoice["applicable"] is True
    assert invoice["rule_result"] != "PASS"
    assert result["certification_claim"] is False


def test_aaoifi_identity_gates_remain_dispatched_by_rule_id() -> None:
    """Control. SS8 stays on Murabahah and SS9 stays on Ijarah. Neither gate passes."""
    murabahah = evaluate(
        from_mapping(
            {
                "case_id": "claim-ss8",
                "synthetic": True,
                "contract_type": "Murabahah",
                "institution_class": "other",
                "jurisdiction": "PK",
            }
        ),
        timestamp=TS,
    )
    ijarah = evaluate(
        from_mapping(
            {
                "case_id": "claim-ss9",
                "synthetic": True,
                "contract_type": "Ijarah",
                "institution_class": "other",
                "jurisdiction": "PK",
            }
        ),
        timestamp=TS,
    )
    ss8_m = _rule(murabahah, "SH-AAOIFI-SS8-GATE")
    ss9_m = _rule(murabahah, "SH-AAOIFI-SS9-GATE")
    ss8_i = _rule(ijarah, "SH-AAOIFI-SS8-GATE")
    ss9_i = _rule(ijarah, "SH-AAOIFI-SS9-GATE")
    assert ss8_m["applicable"] is True
    assert ss8_m["rule_result"] == "INSUFFICIENT_INFORMATION"
    assert ss9_m["applicable"] is False
    assert ss9_m["rule_result"] == "NOT_APPLICABLE"
    assert ss8_i["applicable"] is False
    assert ss8_i["rule_result"] == "NOT_APPLICABLE"
    assert ss9_i["applicable"] is True
    assert ss9_i["rule_result"] == "INSUFFICIENT_INFORMATION"
    assert murabahah["certification_claim"] is False
    assert ijarah["certification_claim"] is False


def test_frozen_decision_thresholds_remain_unchanged() -> None:
    """Control. This file only reads the frozen policy."""
    freeze = load_frozen_thresholds()
    assert freeze["t_low"] == EXPECTED_T_LOW
    assert freeze["t_high"] == EXPECTED_T_HIGH
    assert freeze["selection_split"] == "validation"
