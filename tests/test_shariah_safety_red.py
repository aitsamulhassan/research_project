"""RED-phase safety regressions for the Shariah governance screen.

Synthetic inputs only. These tests do not certify religious compliance.
Failures are expected where the current engine violates a safety invariant.
Do not mark them xfail or skip to force a green report.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision.config_load import load_policy_config  # noqa: E402
from decision.decision_engine import fuse_decision  # noqa: E402
from decision.policy_matrix import build_matrix  # noqa: E402
from decision.stage8_v2 import EXPECTED_T_HIGH, EXPECTED_T_LOW  # noqa: E402
from shariah.engine import evaluate, from_mapping  # noqa: E402
from shariah.l2 import evaluate_lendingclub_application  # noqa: E402
from shariah.schema import CONTRACT_TYPES  # noqa: E402

TS = "2026-09-15T00:00:00+00:00"
LOW_PROBABILITY = 0.05
MATRIX = build_matrix(load_policy_config()["governance_policy"]["matrix"])
ARCHITECTURE_RULES = {"SH-ARCH-001", "SH-ARCH-003"}
BOARD_RULES = ("SH-SBP-SGF-002", "SH-SBP-SGF-003")
SOURCE_VERIFIED = "SOURCE_VERIFIED_PENDING_EXPERT_REVIEW"

UNCOVERED_CONTRACTS = (
    "Musharakah",
    "Qard",
    "Mudarabah",
    "Salam",
    "Istisna",
    "conventional_credit",
)
OUTSIDE_VOCABULARY = ("Tawarruq", "Unknown", "", "not-a-contract")


def _fuse_low(status: str) -> str:
    return fuse_decision(
        LOW_PROBABILITY,
        status,
        EXPECTED_T_LOW,
        EXPECTED_T_HIGH,
        MATRIX,
    )["final_decision"]


def _rule(result: dict, rule_id: str) -> dict:
    return next(row for row in result["rule_evaluations"] if row["rule_id"] == rule_id)


def _base_payload(case_id: str, **fields: object) -> dict:
    payload = {
        "case_id": case_id,
        "synthetic": True,
        "institution_class": "other",
        "jurisdiction": "PK",
    }
    payload.update(fields)
    return payload


def _evaluate(payload: dict) -> dict:
    return evaluate(from_mapping(payload), timestamp=TS)


def _ibi_musharakah(case_id: str, approval: object, *, jurisdiction: str = "PK") -> dict:
    return _base_payload(
        case_id,
        contract_type="Musharakah",
        institution_class="IBI",
        jurisdiction=jurisdiction,
        sb_prior_product_approval=approval,
        sb_approved_agreements_and_process_flows=approval,
    )


def _verified_applicability_scope(row: dict) -> bool:
    """True only when the engine itself records a verified scope decision.

    This does not decide whether a regulator may apply outside one country.
    """
    scope = row.get("applicability_scope")
    if not isinstance(scope, dict):
        return False
    return (
        scope.get("verified") is True
        and bool(scope.get("authority"))
        and bool(scope.get("jurisdiction"))
    )


def _unscoped_source_passes(result: dict) -> list[str]:
    found = []
    for row in result["rule_evaluations"]:
        if row["validation_status"] != SOURCE_VERIFIED:
            continue
        if row["rule_result"] != "PASS":
            continue
        if not _verified_applicability_scope(row):
            found.append(row["rule_id"])
    return found


def _assert_input_rejection(exc: Exception, *needles: str) -> None:
    assert isinstance(exc, ValueError)
    text = str(exc).lower()
    assert text.strip()
    assert any(needle.lower() in text for needle in needles), text


def _screen_or_reject(payload: dict, *rejection_needles: str) -> dict | None:
    try:
        return _evaluate(payload)
    except ValueError as exc:
        _assert_input_rejection(exc, *rejection_needles)
        return None


def _assert_gate_reports_unavailable_text(row: dict) -> None:
    reason = str(row["reason"]).lower()
    assert row["applicable"] is True
    assert row["rule_result"] != "PASS"
    assert row["validation_status"] != "EXPERT_VALIDATED"
    assert row["source_clause"] == "NOT_VERIFIED"
    assert row["rule_result"] == "INSUFFICIENT_INFORMATION" or any(
        token in reason for token in ("not retrieved", "access-controlled", "unavailable")
    )


def _murabahah_operational() -> dict:
    return _base_payload(
        "red-murabahah-operational",
        contract_type="Murabahah",
        institution_class="IBI",
        jurisdiction="PK",
        sb_prior_product_approval=True,
        sb_approved_agreements_and_process_flows=True,
        invoice_name_status="bank_account_client",
        payment_channel="supplier",
    )


def _ijarah_family(case_id: str, contract_type: str) -> dict:
    return _base_payload(
        case_id,
        contract_type=contract_type,
        institution_class="IBI",
        jurisdiction="PK",
        sb_prior_product_approval=True,
        sb_approved_agreements_and_process_flows=True,
    )


@pytest.mark.parametrize("contract_type", UNCOVERED_CONTRACTS)
def test_architecture_only_screen_is_not_substantive_pass(contract_type: str) -> None:
    """D1 and D2. Identification plus a clean firewall is not substantive screening."""
    assert contract_type in CONTRACT_TYPES
    result = _evaluate(
        _base_payload(
            f"red-uncovered-{contract_type}",
            contract_type=contract_type,
        )
    )
    applicable = {row["rule_id"] for row in result["rule_evaluations"] if row["applicable"]}
    assert applicable <= ARCHITECTURE_RULES
    assert not any(
        row["applicable"] and row["validation_status"] == "EXPERT_VALIDATED"
        for row in result["rule_evaluations"]
    )
    assert result["certification_claim"] is False
    status = result["overall_governance_status"]
    decision = _fuse_low(status)
    assert status != "PASS" and decision != "APPROVE", (
        f"architecture-only {contract_type} screen returned status={status} "
        f"low_band_decision={decision}"
    )


@pytest.mark.parametrize(
    "approval",
    [False, None],
    ids=["boolean-false", "missing"],
)
def test_false_or_missing_board_flag_is_not_affirmative(approval: object) -> None:
    """Control for D3. Boolean false and missing approval already abstain or hard-stop."""
    result = _evaluate(_ibi_musharakah(f"red-board-{approval!r}", approval))
    assert result["certification_claim"] is False
    for rule_id in BOARD_RULES:
        assert _rule(result, rule_id)["rule_result"] != "PASS"
    status = result["overall_governance_status"]
    assert status != "PASS"
    assert _fuse_low(status) != "APPROVE"


@pytest.mark.parametrize("approval", ["false", 0], ids=["string-false", "integer-zero"])
def test_non_boolean_false_board_flag_is_not_affirmative(approval: object) -> None:
    """D3. String and integer false-tokens must not satisfy the board-approval predicate."""
    payload = _ibi_musharakah(f"red-board-token-{approval!r}", approval)
    result = _screen_or_reject(payload, "tri-state", "unsupported", "approval", "invalid", "schema")
    if result is None:
        return
    assert result["certification_claim"] is False
    status = result["overall_governance_status"]
    decision = _fuse_low(status)
    rule_results = {rule_id: _rule(result, rule_id)["rule_result"] for rule_id in BOARD_RULES}
    assert (
        rule_results["SH-SBP-SGF-002"] != "PASS"
        and rule_results["SH-SBP-SGF-003"] != "PASS"
        and status != "PASS"
        and decision != "APPROVE"
    ), f"rules={rule_results} overall={status} low_band_decision={decision}"


def test_boolean_approval_tokens_keep_their_python_types() -> None:
    """Fixture control. The engine receives a bool, a string, and an int as distinct objects."""
    boolean_true = from_mapping(_ibi_musharakah("red-type-true", True))
    string_false = from_mapping(_ibi_musharakah("red-type-string", "false"))
    integer_zero = from_mapping(_ibi_musharakah("red-type-zero", 0))
    assert boolean_true.sb_prior_product_approval is True
    assert type(boolean_true.sb_approved_agreements_and_process_flows) is bool
    assert string_false.sb_prior_product_approval == "false"
    assert type(string_false.sb_prior_product_approval) is str
    assert integer_zero.sb_prior_product_approval == 0
    assert type(integer_zero.sb_prior_product_approval) is int


def test_boolean_true_board_outcome_differs_from_false_tokens() -> None:
    """D3. Exact True stays a diagnostic pass. Malformed tokens stay diagnostic review.

    Engine v2 can guard both public rule results as REVIEW while applicability
    is SCOPE_UNKNOWN. The diagnostic predicates must still differ.
    """

    def screen(approval: object, case_id: str) -> tuple[dict, list[dict]]:
        result = _evaluate(_ibi_musharakah(case_id, approval))
        rows = [_rule(result, rule_id) for rule_id in BOARD_RULES]
        return result, rows

    true_result, true_rows = screen(True, "red-distinguish-true")
    string_result, string_rows = screen("false", "red-distinguish-string")
    zero_result, zero_rows = screen(0, "red-distinguish-zero")

    def diagnostics(rows: list[dict]) -> tuple[str, ...]:
        return tuple(row["diagnostic_predicate_result"] for row in rows)

    assert diagnostics(true_rows) == ("PASS", "PASS")
    assert diagnostics(string_rows) == ("REVIEW", "REVIEW")
    assert diagnostics(zero_rows) == ("REVIEW", "REVIEW")
    assert diagnostics(true_rows) != diagnostics(string_rows)
    assert diagnostics(true_rows) != diagnostics(zero_rows)

    for row in true_rows:
        assert row["diagnostic_predicate_applicable"] is True
        assert row["diagnostic_predicate_result"] == "PASS"
        assert row["rule_result"] == "REVIEW"
        assert row["diagnostic_predicate_reason"] != row["reason"]
        assert "SCOPE_UNKNOWN" in row["reason"]
        assert row["diagnostic_predicate_reason"]
    for row in string_rows + zero_rows:
        assert row["diagnostic_predicate_applicable"] is True
        assert row["diagnostic_predicate_result"] == "REVIEW"
        assert row["diagnostic_predicate_result"] != "PASS"
        assert row["diagnostic_predicate_result"] != "NOT_STRUCTURABLE_WITHOUT_REDESIGN"
        assert row["rule_result"] == "REVIEW"
        assert "non-Boolean" in row["diagnostic_predicate_reason"]
        assert row["reason"] == row["diagnostic_predicate_reason"]

    for result, rows in (
        (true_result, true_rows),
        (string_result, string_rows),
        (zero_result, zero_rows),
    ):
        assert result["certification_claim"] is False
        assert result["overall_governance_status"] == "REVIEW"
        assert result["overall_governance_status"] != "PASS"
        decision = _fuse_low(result["overall_governance_status"])
        assert decision == "HUMAN_REVIEW"
        assert decision != "APPROVE"
        for row in rows:
            assert row["applicability_decision"]["status"] == "SCOPE_UNKNOWN"
            assert row["source_digest_verified"] is False
            assert row["validation_status"] != "EXPERT_VALIDATED"


@pytest.mark.parametrize("contract_type", OUTSIDE_VOCABULARY)
def test_contract_outside_vocabulary_is_not_positively_screened(contract_type: str) -> None:
    """D5. Values outside CONTRACT_TYPES must be rejected or abstained, not passed."""
    assert contract_type not in CONTRACT_TYPES
    payload = _base_payload(f"red-vocab-{contract_type or 'empty'}", contract_type=contract_type)
    result = _screen_or_reject(
        payload,
        "contract",
        "vocabulary",
        "unsupported",
        "invalid",
        "unknown",
        contract_type or "empty",
    )
    if result is None:
        return
    assert result["certification_claim"] is False
    status = result["overall_governance_status"]
    decision = _fuse_low(status)
    assert status != "PASS" and decision != "APPROVE", (
        f"contract_type={contract_type!r} status={status} low_band_decision={decision}"
    )


def test_gb_ibi_source_pass_requires_verified_scope() -> None:
    """D4. Institution class IBI alone does not establish SBP applicability for jurisdiction GB."""
    result = _screen_or_reject(
        _ibi_musharakah("red-jurisdiction-gb", True, jurisdiction="GB"),
        "scope",
        "jurisdiction",
        "applicab",
    )
    if result is None:
        return
    evidence = result["rule_evaluations"][0]["input_evidence"]
    assert evidence["jurisdiction"] == "GB"
    assert evidence["institution_class"] == "IBI"
    assert result["certification_claim"] is False
    unscoped = _unscoped_source_passes(result)
    assert unscoped == [], (
        f"source rules passed without a verified applicability scope: {unscoped}; "
        f"overall={result['overall_governance_status']}"
    )


def test_us_security_claim_source_pass_requires_verified_scope() -> None:
    """D4. A US institution class match must not by itself produce an SECP source PASS."""
    payload = _base_payload(
        "red-jurisdiction-us-secp",
        contract_type="conventional_credit",
        institution_class="secp_ifi",
        jurisdiction="US",
        claims_shariah_compliant_security=True,
        secp_shariah_compliance_certificate=True,
    )
    result = _screen_or_reject(payload, "scope", "jurisdiction", "applicab")
    if result is None:
        return
    evidence = result["rule_evaluations"][0]["input_evidence"]
    assert evidence["jurisdiction"] == "US"
    assert evidence["institution_class"] == "secp_ifi"
    assert result["certification_claim"] is False
    unscoped = _unscoped_source_passes(result)
    assert unscoped == [], (
        f"source rules passed without a verified applicability scope: {unscoped}; "
        f"overall={result['overall_governance_status']}"
    )


def test_ss8_gate_on_murabahah_reports_unavailable_text_and_is_not_compliance() -> None:
    """Control for D6. The Murabahah identity gate abstains and does not certify."""
    result = _evaluate(_murabahah_operational())
    gate = _rule(result, "SH-AAOIFI-SS8-GATE")
    _assert_gate_reports_unavailable_text(gate)
    assert result["overall_governance_status"] != "PASS"
    assert result["certification_claim"] is False


def test_ss9_gate_does_not_apply_to_murabahah() -> None:
    """D6. The SS9 identity gate is not a Murabahah rule."""
    result = _evaluate(_murabahah_operational())
    gate = _rule(result, "SH-AAOIFI-SS9-GATE")
    assert gate["applicable"] is False
    assert gate["rule_result"] == "NOT_APPLICABLE"


def test_ss9_gate_on_ijarah_reports_unavailable_text_and_is_not_compliance() -> None:
    """Control for D6. The Ijarah identity gate abstains and does not certify."""
    result = _evaluate(_ijarah_family("red-ijarah", "Ijarah"))
    gate = _rule(result, "SH-AAOIFI-SS9-GATE")
    _assert_gate_reports_unavailable_text(gate)
    assert result["overall_governance_status"] != "PASS"
    assert result["certification_claim"] is False


def test_ss8_gate_does_not_apply_to_ijarah() -> None:
    """D6. The SS8 identity gate is not an Ijarah rule."""
    result = _evaluate(_ijarah_family("red-ijarah-ss8", "Ijarah"))
    gate = _rule(result, "SH-AAOIFI-SS8-GATE")
    assert gate["applicable"] is False
    assert gate["rule_result"] == "NOT_APPLICABLE"


def test_ss9_gate_on_ijarah_muntahia_reports_unavailable_text() -> None:
    """Control for D6. Ijarah Muntahia Bittamleek remains in the SS9 identity family."""
    result = _evaluate(_ijarah_family("red-imbt", "Ijarah_Muntahia_Bittamleek"))
    gate = _rule(result, "SH-AAOIFI-SS9-GATE")
    _assert_gate_reports_unavailable_text(gate)
    assert result["certification_claim"] is False
    assert result["overall_governance_status"] != "PASS"


def test_ss8_gate_does_not_apply_to_ijarah_muntahia() -> None:
    """D6. The SS8 identity gate does not cover Ijarah Muntahia Bittamleek."""
    result = _evaluate(_ijarah_family("red-imbt-ss8", "Ijarah_Muntahia_Bittamleek"))
    gate = _rule(result, "SH-AAOIFI-SS8-GATE")
    assert gate["applicable"] is False
    assert gate["rule_result"] == "NOT_APPLICABLE"


def test_lendingclub_l2_stays_unknown_and_purpose_car_is_not_ijarah() -> None:
    """Passing control. The LendingClub extractor does not invent an Islamic contract."""
    result = evaluate_lendingclub_application(
        {"_fixture_key": "red-lc-car", "purpose": "car", "id": "synthetic-red", "fico_n": 700},
        timestamp=TS,
        synthetic=True,
    )
    evidence = result["rule_evaluations"][0]["input_evidence"]
    assert result["synthetic"] is True
    assert result["contract_type"] == "unknown"
    assert result["contract_type"] != "Ijarah"
    assert "purpose" not in evidence
    assert "purpose" not in evidence.get("_extra", {})
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert result["layer_a_completeness"]["layer_a"] == "INSUFFICIENT"
    assert result["certification_claim"] is False
    assert result["any_expert_validated"] is False
    assert _fuse_low(result["overall_governance_status"]) == "HUMAN_REVIEW"


def test_unknown_contract_does_not_approve_at_low_probability() -> None:
    """Passing control. Missing contract identity stays non-approving under the frozen matrix."""
    result = _evaluate(_base_payload("red-unknown-contract", contract_type="unknown"))
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert result["certification_claim"] is False
    assert _fuse_low(result["overall_governance_status"]) != "APPROVE"
    assert _fuse_low(result["overall_governance_status"]) == "HUMAN_REVIEW"


def test_certification_claim_stays_false_on_architecture_only_screen() -> None:
    """Passing control. Even an unsafe status token must not claim certification."""
    result = _evaluate(_base_payload("red-claim-flag", contract_type="Qard"))
    assert result["synthetic"] is True
    assert result["certification_claim"] is False
    assert "shariah compliant" not in str(result["overall_governance_status"]).lower()
    assert "shariah compliant" not in str(result["disclaimer"]).lower()
