"""RED-phase checks for documentary Boolean flags.

Synthetic inputs only. A rule-level PASS here is a data-integrity result, not
Shariah compliance and not authentication of the underlying document.
Failures are expected where a non-Boolean token is treated as affirmative.
Do not mark these tests xfail or skip to force a green report.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shariah.engine import evaluate, from_mapping  # noqa: E402

TS = "2026-09-15T00:00:00+00:00"
INVOICE_RULE = "SH-SBP-MUR-INV-001"
ALT_DOCS_RULE = "SH-SBP-MUR-INV-002"
PAYMENT_RULE = "SH-SBP-MUR-PAY-001"
SECP_RULE = "SH-SECP-SGR-SEC-001"
REJECTION_NEEDLES = (
    "boolean",
    "bool",
    "invalid",
    "unsupported",
    "schema",
    "tri-state",
    "evidence",
)
INVALID_TOKENS = [
    pytest.param("false", id="string-false"),
    pytest.param("true", id="string-true"),
    pytest.param(0, id="integer-zero"),
    pytest.param(1, id="integer-one"),
    pytest.param("", id="empty-string"),
    pytest.param("not-a-boolean", id="arbitrary-text"),
]


def _case_token(value: object) -> str:
    if value == "":
        return "empty"
    return str(value).replace(" ", "-")


def _murabahah(**fields: object) -> dict:
    payload = {
        "synthetic": True,
        "contract_type": "Murabahah",
        "institution_class": "IBI",
        "jurisdiction": "PK",
        "sb_prior_product_approval": True,
        "sb_approved_agreements_and_process_flows": True,
        "payment_channel": "supplier",
    }
    payload.update(fields)
    return payload


def _evaluate(payload: dict) -> dict:
    return evaluate(from_mapping(payload), timestamp=TS)


def _rule(result: dict, rule_id: str) -> dict:
    return next(row for row in result["rule_evaluations"] if row["rule_id"] == rule_id)


def _assert_documented_rejection(exc: Exception) -> None:
    assert isinstance(exc, ValueError)
    text = str(exc).lower()
    assert text.strip()
    assert any(needle in text for needle in REJECTION_NEEDLES), text


def _evaluated_rule(payload: dict, rule_id: str) -> dict | None:
    """Return the applicable rule row, or None when malformed evidence is rejected."""
    try:
        result = _evaluate(payload)
    except ValueError as exc:
        _assert_documented_rejection(exc)
        return None
    row = _rule(result, rule_id)
    assert row["applicable"] is True
    assert result["certification_claim"] is False
    row["_overall_governance_status"] = result["overall_governance_status"]
    row["_certification_claim"] = result["certification_claim"]
    return row


def _assert_not_rule_pass(payload: dict, rule_id: str, field: str, value: object) -> None:
    row = _evaluated_rule(payload, rule_id)
    if row is None:
        return
    evidence = row["input_evidence"]
    assert evidence[field] == value
    assert type(evidence[field]) is type(value)
    assert row["diagnostic_predicate_result"] != "PASS", (
        f"{rule_id} diagnostic={row['diagnostic_predicate_result']} field={field} value={value!r} "
        f"type={type(value).__name__} overall={row['_overall_governance_status']}"
    )
    assert row["rule_result"] != "PASS"
    assert row["applicability_decision"]["status"] == "SCOPE_UNKNOWN"
    assert row["source_digest_verified"] is False
    assert row["validation_status"] != "EXPERT_VALIDATED"
    if type(value) is bool:
        assert value is False
        assert row["diagnostic_predicate_result"] == "NOT_STRUCTURABLE_WITHOUT_REDESIGN"
        assert row["diagnostic_predicate_applicable"] is True
        assert row["rule_result"] == "REVIEW"
        assert row["diagnostic_predicate_reason"] != row["reason"]
        return
    assert row["diagnostic_predicate_result"] == "REVIEW"
    assert row["diagnostic_predicate_result"] != "NOT_STRUCTURABLE_WITHOUT_REDESIGN"
    assert row["rule_result"] == "REVIEW"
    assert row["reason"] == row["diagnostic_predicate_reason"]


def _assert_scope_gated_diagnostic_pass(row: dict) -> None:
    """Exact True may pass the documentary predicate. Public scope remains unresolved."""
    assert row["diagnostic_predicate_applicable"] is True
    assert row["diagnostic_predicate_result"] == "PASS"
    assert row["rule_result"] == "REVIEW"
    assert row["diagnostic_predicate_result"] != row["rule_result"]
    assert row["diagnostic_predicate_reason"]
    assert row["reason"] != row["diagnostic_predicate_reason"]
    assert "SCOPE_UNKNOWN" in row["reason"]
    decision = row["applicability_decision"]
    assert decision["status"] == "SCOPE_UNKNOWN"
    assert decision["applicability_version"] == "stage7-applicability-scope-unknown-v1"
    assert decision["expert_metadata_authenticated"] is False
    assert decision["source_digest_verified"] is False
    assert row["source_digest_verified"] is False
    assert row["validation_status"] != "EXPERT_VALIDATED"
    assert row["_certification_claim"] is False
    assert row["_overall_governance_status"] != "PASS"


def _assert_rule_pass(payload: dict, rule_id: str, field: str) -> None:
    row = _evaluated_rule(payload, rule_id)
    assert row is not None
    assert row["input_evidence"][field] is True
    assert type(row["input_evidence"][field]) is bool
    _assert_scope_gated_diagnostic_pass(row)


def test_boolean_tokens_keep_distinct_python_types() -> None:
    """Fixture control. Strings and integers must not be coerced before evaluation."""
    true_evidence = from_mapping(
        _murabahah(
            case_id="doc-type-true",
            invoice_name_status="client_only",
            shariah_advisor_invoice_exception_approval=True,
        )
    )
    string_evidence = from_mapping(
        _murabahah(
            case_id="doc-type-string",
            invoice_name_status="client_only",
            shariah_advisor_invoice_exception_approval="false",
        )
    )
    integer_evidence = from_mapping(
        _murabahah(
            case_id="doc-type-zero",
            invoice_name_status="client_only",
            shariah_advisor_invoice_exception_approval=0,
        )
    )
    assert true_evidence.shariah_advisor_invoice_exception_approval is True
    assert type(true_evidence.shariah_advisor_invoice_exception_approval) is bool
    assert string_evidence.shariah_advisor_invoice_exception_approval == "false"
    assert type(string_evidence.shariah_advisor_invoice_exception_approval) is str
    assert integer_evidence.shariah_advisor_invoice_exception_approval == 0
    assert type(integer_evidence.shariah_advisor_invoice_exception_approval) is int


def test_client_only_boolean_true_may_satisfy_invoice_predicate() -> None:
    """Control. Exact True may satisfy SH-SBP-MUR-INV-001. This is not a certification."""
    payload = _murabahah(
        case_id="doc-invoice-true",
        invoice_name_status="client_only",
        shariah_advisor_invoice_exception_approval=True,
    )
    _assert_rule_pass(payload, INVOICE_RULE, "shariah_advisor_invoice_exception_approval")


def test_client_only_boolean_false_is_not_invoice_pass() -> None:
    payload = _murabahah(
        case_id="doc-invoice-false",
        invoice_name_status="client_only",
        shariah_advisor_invoice_exception_approval=False,
    )
    _assert_not_rule_pass(payload, INVOICE_RULE, "shariah_advisor_invoice_exception_approval", False)


def test_client_only_missing_approval_is_not_invoice_pass() -> None:
    payload = _murabahah(
        case_id="doc-invoice-missing",
        invoice_name_status="client_only",
        shariah_advisor_invoice_exception_approval=None,
    )
    row = _evaluated_rule(payload, INVOICE_RULE)
    assert row is not None
    assert row["input_evidence"]["shariah_advisor_invoice_exception_approval"] is None
    assert row["diagnostic_predicate_result"] == "INSUFFICIENT_INFORMATION"
    assert row["rule_result"] == "INSUFFICIENT_INFORMATION"


@pytest.mark.parametrize("value", INVALID_TOKENS)
def test_client_only_invalid_approval_is_not_invoice_pass(value: object) -> None:
    payload = _murabahah(
        case_id=f"doc-invoice-{_case_token(value)}",
        invoice_name_status="client_only",
        shariah_advisor_invoice_exception_approval=value,
    )
    _assert_not_rule_pass(payload, INVOICE_RULE, "shariah_advisor_invoice_exception_approval", value)


def test_alt_docs_boolean_true_may_satisfy_predicate() -> None:
    """Control. Both exact True flags may satisfy SH-SBP-MUR-INV-002."""
    payload = _murabahah(
        case_id="doc-alt-true",
        invoice_name_status="no_formal_invoice",
        alternative_purchase_documents_present=True,
        shariah_advisor_invoice_exception_approval=True,
    )
    row = _evaluated_rule(payload, ALT_DOCS_RULE)
    assert row is not None
    assert row["input_evidence"]["alternative_purchase_documents_present"] is True
    assert row["input_evidence"]["shariah_advisor_invoice_exception_approval"] is True
    _assert_scope_gated_diagnostic_pass(row)


@pytest.mark.parametrize(
    "field",
    [
        "alternative_purchase_documents_present",
        "shariah_advisor_invoice_exception_approval",
    ],
)
def test_alt_docs_boolean_false_is_not_pass(field: str) -> None:
    fields = {
        "alternative_purchase_documents_present": True,
        "shariah_advisor_invoice_exception_approval": True,
    }
    fields[field] = False
    payload = _murabahah(case_id=f"doc-alt-false-{field}", invoice_name_status="no_formal_invoice", **fields)
    _assert_not_rule_pass(payload, ALT_DOCS_RULE, field, False)


@pytest.mark.parametrize(
    "field",
    [
        "alternative_purchase_documents_present",
        "shariah_advisor_invoice_exception_approval",
    ],
)
def test_alt_docs_missing_flag_is_not_pass(field: str) -> None:
    fields = {
        "alternative_purchase_documents_present": True,
        "shariah_advisor_invoice_exception_approval": True,
    }
    fields[field] = None
    payload = _murabahah(case_id=f"doc-alt-missing-{field}", invoice_name_status="no_formal_invoice", **fields)
    row = _evaluated_rule(payload, ALT_DOCS_RULE)
    assert row is not None
    assert row["input_evidence"][field] is None
    assert row["diagnostic_predicate_result"] == "INSUFFICIENT_INFORMATION"
    assert row["rule_result"] == "INSUFFICIENT_INFORMATION"


@pytest.mark.parametrize(
    "field",
    [
        "alternative_purchase_documents_present",
        "shariah_advisor_invoice_exception_approval",
    ],
)
@pytest.mark.parametrize("value", INVALID_TOKENS)
def test_alt_docs_invalid_flag_is_not_pass(field: str, value: object) -> None:
    fields = {
        "alternative_purchase_documents_present": True,
        "shariah_advisor_invoice_exception_approval": True,
    }
    fields[field] = value
    payload = _murabahah(
        case_id=f"doc-alt-{field}-{_case_token(value)}",
        invoice_name_status="no_formal_invoice",
        **fields,
    )
    _assert_not_rule_pass(payload, ALT_DOCS_RULE, field, value)


def test_agent_payment_boolean_true_may_satisfy_predicate() -> None:
    """Control. Both exact True flags may satisfy SH-SBP-MUR-PAY-001."""
    payload = _murabahah(
        case_id="doc-agent-true",
        invoice_name_status="bank_account_client",
        payment_channel="agent",
        shariah_advisor_agent_payment_approval=True,
        agent_payment_reasons_recorded=True,
    )
    row = _evaluated_rule(payload, PAYMENT_RULE)
    assert row is not None
    assert row["input_evidence"]["shariah_advisor_agent_payment_approval"] is True
    assert row["input_evidence"]["agent_payment_reasons_recorded"] is True
    _assert_scope_gated_diagnostic_pass(row)


@pytest.mark.parametrize(
    "field",
    [
        "shariah_advisor_agent_payment_approval",
        "agent_payment_reasons_recorded",
    ],
)
def test_agent_payment_boolean_false_is_not_pass(field: str) -> None:
    fields = {
        "shariah_advisor_agent_payment_approval": True,
        "agent_payment_reasons_recorded": True,
    }
    fields[field] = False
    payload = _murabahah(
        case_id=f"doc-agent-false-{field}",
        invoice_name_status="bank_account_client",
        payment_channel="agent",
        **fields,
    )
    _assert_not_rule_pass(payload, PAYMENT_RULE, field, False)


@pytest.mark.parametrize(
    "field",
    [
        "shariah_advisor_agent_payment_approval",
        "agent_payment_reasons_recorded",
    ],
)
def test_agent_payment_missing_flag_is_not_pass(field: str) -> None:
    fields = {
        "shariah_advisor_agent_payment_approval": True,
        "agent_payment_reasons_recorded": True,
    }
    fields[field] = None
    payload = _murabahah(
        case_id=f"doc-agent-missing-{field}",
        invoice_name_status="bank_account_client",
        payment_channel="agent",
        **fields,
    )
    row = _evaluated_rule(payload, PAYMENT_RULE)
    assert row is not None
    assert row["input_evidence"][field] is None
    assert row["diagnostic_predicate_result"] == "INSUFFICIENT_INFORMATION"
    assert row["rule_result"] == "INSUFFICIENT_INFORMATION"


@pytest.mark.parametrize(
    "field",
    [
        "shariah_advisor_agent_payment_approval",
        "agent_payment_reasons_recorded",
    ],
)
@pytest.mark.parametrize("value", INVALID_TOKENS)
def test_agent_payment_invalid_flag_is_not_pass(field: str, value: object) -> None:
    fields = {
        "shariah_advisor_agent_payment_approval": True,
        "agent_payment_reasons_recorded": True,
    }
    fields[field] = value
    payload = _murabahah(
        case_id=f"doc-agent-{field}-{_case_token(value)}",
        invoice_name_status="bank_account_client",
        payment_channel="agent",
        **fields,
    )
    _assert_not_rule_pass(payload, PAYMENT_RULE, field, value)


def _security_claim(**fields: object) -> dict:
    payload = {
        "synthetic": True,
        "contract_type": "conventional_credit",
        "institution_class": "secp_ifi",
        "jurisdiction": "PK",
        "claims_shariah_compliant_security": True,
    }
    payload.update(fields)
    return payload


def test_secp_boolean_true_may_satisfy_certificate_predicate() -> None:
    """Control. Exact True may satisfy the certificate flag. This does not decide SECP scope."""
    payload = _security_claim(case_id="doc-secp-true", secp_shariah_compliance_certificate=True)
    _assert_rule_pass(payload, SECP_RULE, "secp_shariah_compliance_certificate")


def test_secp_boolean_false_is_not_certificate_pass() -> None:
    payload = _security_claim(case_id="doc-secp-false", secp_shariah_compliance_certificate=False)
    _assert_not_rule_pass(payload, SECP_RULE, "secp_shariah_compliance_certificate", False)


def test_secp_missing_certificate_is_not_pass() -> None:
    payload = _security_claim(case_id="doc-secp-missing", secp_shariah_compliance_certificate=None)
    row = _evaluated_rule(payload, SECP_RULE)
    assert row is not None
    assert row["input_evidence"]["secp_shariah_compliance_certificate"] is None
    assert row["diagnostic_predicate_result"] == "INSUFFICIENT_INFORMATION"
    assert row["rule_result"] == "INSUFFICIENT_INFORMATION"


@pytest.mark.parametrize("value", INVALID_TOKENS)
def test_secp_invalid_certificate_is_not_pass(value: object) -> None:
    payload = _security_claim(
        case_id=f"doc-secp-{_case_token(value)}",
        secp_shariah_compliance_certificate=value,
    )
    _assert_not_rule_pass(payload, SECP_RULE, "secp_shariah_compliance_certificate", value)
