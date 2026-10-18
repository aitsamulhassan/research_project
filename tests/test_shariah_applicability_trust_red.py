"""RED-phase checks for regulatory applicability and catalog trust.

Synthetic inputs only. A predicate PASS is not regulatory applicability, expert
validation, or an overall governance approval. A caller-supplied catalog is not
a qualified reviewer. Failures are expected where the current engine presents
an unscoped source result as authoritative. Do not mark these tests xfail or skip.

These fixtures contain no qualified scope review. A self-declared
VERIFIED_IN_SCOPE label does not satisfy them. GB and PK are not treated as
legal conclusions in either direction.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from decision.config_load import load_policy_config  # noqa: E402
from decision.decision_engine import fuse_decision  # noqa: E402
from decision.policy_matrix import build_matrix  # noqa: E402
from decision.stage8_v2 import (  # noqa: E402
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    load_frozen_thresholds,
)
from shariah.engine import evaluate, from_mapping  # noqa: E402
from shariah.l2 import evaluate_lendingclub_application  # noqa: E402
from shariah.provenance import load_source_register, source_by_id  # noqa: E402
from shariah.rules import Rule, load_catalog  # noqa: E402
from shariah.schema import EVIDENCE_FIELDS  # noqa: E402

TS = "2026-09-15T00:00:00+00:00"
PRE_FRAMEWORK_TS = "2020-01-01T00:00:00+00:00"
LOW_PROBABILITY = 0.05
SGF_PRIOR = "SH-SBP-SGF-002"
SGF_DOCS = "SH-SBP-SGF-003"
PAY_RULE = "SH-SBP-MUR-PAY-001"
INVOICE_RULE = "SH-SBP-MUR-INV-001"
SECP_RULE = "SH-SECP-SGR-SEC-001"
ARCHITECTURE = "RESEARCH_ARCHITECTURE_NOT_A_RULING"
AUTHORITATIVE_RESULTS = {"PASS", "NOT_STRUCTURABLE_WITHOUT_REDESIGN"}
ALTERED_CLAUSE = "SYNTHETIC ALTERED CLAUSE TEXT — NOT A REGULATORY INSTRUMENT"
PROBE_RECORD = {
    "probe_marker": "SYNTHETIC_NON_AUTHORITATIVE",
    "not_an_expert": True,
}
BOUNDARY_NEEDLES = (
    "scope",
    "applicab",
    "trust",
    "provenance",
    "catalog",
    "source",
    "unverified",
    "expert",
    "jurisdiction",
)
SBP_JURISDICTIONS = [
    pytest.param("GB", id="gb"),
    pytest.param("PK", id="pk"),
    pytest.param("unknown", id="unknown"),
]
SECP_JURISDICTIONS = [
    pytest.param("US", id="us"),
    pytest.param("PK", id="pk"),
    pytest.param("unknown", id="unknown"),
]
ABSENT_TEMPORAL_FIELDS = (
    "contract_execution_date",
    "transaction_date",
    "regulatory_effective_date",
    "effective_date",
)
MATRIX = build_matrix(load_policy_config()["governance_policy"]["matrix"])


def _fuse(status: str) -> str:
    return fuse_decision(LOW_PROBABILITY, status, EXPECTED_T_LOW, EXPECTED_T_HIGH, MATRIX)["final_decision"]


def _payload(case_id: str, **fields: object) -> dict:
    payload = {"case_id": case_id, "synthetic": True, "jurisdiction": "PK"}
    payload.update(fields)
    return payload


def _musharakah_ibi(case_id: str, jurisdiction: str, approval: bool) -> dict:
    return _payload(
        case_id,
        contract_type="Musharakah",
        institution_class="IBI",
        jurisdiction=jurisdiction,
        sb_prior_product_approval=approval,
        sb_approved_agreements_and_process_flows=approval,
    )


def _security_claim(case_id: str, jurisdiction: str, certificate: bool, **fields: object) -> dict:
    payload = _payload(
        case_id,
        contract_type="conventional_credit",
        institution_class="secp_ifi",
        jurisdiction=jurisdiction,
        claims_shariah_compliant_security=True,
        secp_shariah_compliance_certificate=certificate,
    )
    payload.update(fields)
    return payload


def _rule(result: dict, rule_id: str) -> dict:
    return next(row for row in result["rule_evaluations"] if row["rule_id"] == rule_id)


def _unsafe_source_conclusion(row: dict) -> bool:
    """True when a source rule emits PASS or a hard stop without a qualified review.

    Architecture checks are not source-regulatory conclusions. These fixtures have
    no qualified applicability review in the repository, so a self-declared
    verified-scope label does not make the conclusion safe.
    """
    if row.get("validation_status") == ARCHITECTURE:
        return False
    return row.get("rule_result") in AUTHORITATIVE_RESULTS


def _evaluate(payload: dict, *, catalog: list[Rule] | None = None, timestamp: str = TS):
    try:
        result = evaluate(from_mapping(payload), timestamp=timestamp, catalog=catalog)
    except ValueError as exc:
        text = str(exc).lower()
        assert text.strip()
        assert any(needle in text for needle in BOUNDARY_NEEDLES), text
        return None
    return result


def _catalog(transform) -> list[Rule]:
    forged = []
    for rule in load_catalog():
        payload = copy.deepcopy(rule.payload)
        transform(payload)
        forged.append(Rule(payload))
    return forged


def _arm_sgf(payload: dict, *, jurisdiction: str, relabel: bool, clause: str | None = None) -> None:
    if payload.get("rule_id") not in {SGF_PRIOR, SGF_DOCS}:
        return
    if relabel:
        payload["contract_type"] = "Musharakah"
    payload["validation_status"] = "EXPERT_VALIDATED"
    payload["expert_validation_record"] = dict(PROBE_RECORD)
    payload["applicability_scope"] = {
        "verified": True,
        "authority": "synthetic-probe-not-a-regulator",
        "jurisdiction": jurisdiction,
    }
    if clause is not None:
        payload["clause"] = clause
        payload["source_statement"] = clause


def _assert_forged_cannot_approve(result: dict) -> None:
    status = result["overall_governance_status"]
    decision = _fuse(status)
    assert result["certification_claim"] is False
    assert result["synthetic"] is True
    assert status != "PASS" and decision != "APPROVE", (
        f"overall={status} fusion={decision} certification={result['certification_claim']} "
        f"guard={result['aggregation_guard']}"
    )


@pytest.mark.parametrize("jurisdiction", SBP_JURISDICTIONS)
def test_sgf_true_flags_are_not_authoritative_without_scope(jurisdiction: str) -> None:
    """PK is not accepted from a catalog sentence. GB is not marked legally out of scope."""
    payload = _musharakah_ibi(f"scope-sgf-{jurisdiction}", jurisdiction, True)
    result = _evaluate(payload)
    if result is None:
        return
    for rule_id in (SGF_PRIOR, SGF_DOCS):
        row = _rule(result, rule_id)
        status = result["overall_governance_status"]
        assert not _unsafe_source_conclusion(row), (
            f"jurisdiction={jurisdiction} rule={rule_id} result={row['rule_result']} "
            f"reason={row['reason']!r} validation={row['validation_status']} "
            f"applicability={row.get('applicability_decision')!r} overall={status} "
            f"fusion={_fuse(status)} certification={result['certification_claim']}"
        )


@pytest.mark.parametrize("jurisdiction", SBP_JURISDICTIONS)
def test_sgf_true_flags_do_not_create_an_overall_pass(jurisdiction: str) -> None:
    """Control. The current aggregation guard already withholds overall PASS."""
    result = _evaluate(_musharakah_ibi(f"scope-sgf-overall-{jurisdiction}", jurisdiction, True))
    assert result is not None
    status = result["overall_governance_status"]
    assert status != "PASS"
    assert _fuse(status) != "APPROVE"
    assert result["certification_claim"] is False


def test_unknown_institution_does_not_receive_an_sgf_pass() -> None:
    """Control. An unknown institution label does not establish IBI coverage."""
    payload = _payload(
        "scope-institution-unknown",
        contract_type="Musharakah",
        institution_class="unknown",
        jurisdiction="GB",
        sb_prior_product_approval=True,
        sb_approved_agreements_and_process_flows=True,
    )
    result = _evaluate(payload)
    assert result is not None
    for rule_id in (SGF_PRIOR, SGF_DOCS):
        assert not _unsafe_source_conclusion(_rule(result, rule_id))
    assert result["overall_governance_status"] != "PASS"
    assert result["certification_claim"] is False


@pytest.mark.parametrize("jurisdiction", SECP_JURISDICTIONS)
def test_secp_certificate_flag_is_not_authoritative_without_scope(jurisdiction: str) -> None:
    """A certificate Boolean and an institution label do not establish Regulation 7(2)."""
    payload = _security_claim(f"scope-secp-{jurisdiction}", jurisdiction, True)
    result = _evaluate(payload)
    if result is None:
        return
    row = _rule(result, SECP_RULE)
    status = result["overall_governance_status"]
    assert not _unsafe_source_conclusion(row), (
        f"jurisdiction={jurisdiction} result={row['rule_result']} reason={row['reason']!r} "
        f"validation={row['validation_status']} applicability={row.get('applicability_decision')!r} "
        f"overall={status} fusion={_fuse(status)} certification={result['certification_claim']}"
    )


@pytest.mark.parametrize("jurisdiction", SECP_JURISDICTIONS)
def test_secp_certificate_flag_does_not_create_an_overall_pass(jurisdiction: str) -> None:
    """Control. Certificate-flag screens stay nonaffirmative at the overall layer."""
    result = _evaluate(_security_claim(f"scope-secp-overall-{jurisdiction}", jurisdiction, True))
    assert result is not None
    status = result["overall_governance_status"]
    assert status != "PASS"
    assert _fuse(status) != "APPROVE"
    assert result["certification_claim"] is False


def test_ibi_exclusion_is_not_verified_out_of_scope() -> None:
    """Control. The IBI skip is not a verified legal exclusion and it is not a source PASS."""
    payload = _security_claim(
        "scope-ibi-exclusion",
        "GB",
        True,
        contract_type="Musharakah",
        institution_class="IBI",
    )
    result = _evaluate(payload)
    assert result is not None
    row = _rule(result, SECP_RULE)
    decision = row.get("applicability_decision")
    verified_out = (
        isinstance(decision, dict)
        and str(decision.get("status", "")).upper() == "VERIFIED_OUT_OF_SCOPE"
    )
    assert row["rule_result"] != "PASS"
    assert not verified_out
    assert result["overall_governance_status"] != "PASS"
    assert result["certification_claim"] is False


def test_ibi_regulatory_exclusion_has_an_auditable_scope_decision() -> None:
    """The exclusion reason cites SGR. That citation needs an explicit scope decision."""
    payload = _security_claim(
        "scope-ibi-decision",
        "GB",
        True,
        contract_type="Musharakah",
        institution_class="IBI",
    )
    result = _evaluate(payload)
    if result is None:
        return
    row = _rule(result, SECP_RULE)
    decision = row.get("applicability_decision")
    assert isinstance(decision, dict) and str(decision.get("status", "")).strip(), (
        f"result={row['rule_result']} reason={row['reason']!r} "
        f"applicability={decision!r} overall={result['overall_governance_status']}"
    )
    assert str(decision.get("status", "")).upper() != "VERIFIED_OUT_OF_SCOPE"


def test_forged_scope_mismatch_cannot_authorize_overall_pass() -> None:
    """In-memory catalog only. Declared jurisdiction ZZ does not match evidence GB."""
    evidence = _musharakah_ibi("forge-mismatch", "GB", True)

    def transform(payload: dict) -> None:
        _arm_sgf(payload, jurisdiction="ZZ", relabel=True)

    result = _evaluate(evidence, catalog=_catalog(transform))
    if result is None:
        return
    _assert_forged_cannot_approve(result)


def test_forged_matching_jurisdiction_without_trust_cannot_authorize_overall_pass() -> None:
    """A scope jurisdiction string equal to the evidence is still untrusted metadata."""
    evidence = _musharakah_ibi("forge-matching-label", "GB", True)

    def transform(payload: dict) -> None:
        _arm_sgf(payload, jurisdiction="GB", relabel=True)

    result = _evaluate(evidence, catalog=_catalog(transform))
    if result is None:
        return
    _assert_forged_cannot_approve(result)


def test_forged_clause_and_expert_metadata_cannot_authorize_overall_pass() -> None:
    evidence = _musharakah_ibi("forge-clause", "GB", True)

    def transform(payload: dict) -> None:
        _arm_sgf(payload, jurisdiction="ZZ", relabel=True, clause=ALTERED_CLAUSE)

    result = _evaluate(evidence, catalog=_catalog(transform))
    if result is None:
        return
    _assert_forged_cannot_approve(result)
    row = _rule(result, SGF_PRIOR)
    assert row["source_clause"] != ALTERED_CLAUSE or result["overall_governance_status"] != "PASS"


def test_expert_metadata_without_contract_relabel_does_not_overall_pass() -> None:
    """Control. Expert labels alone do not currently create overall PASS."""
    evidence = _musharakah_ibi("forge-no-relabel", "GB", True)

    def transform(payload: dict) -> None:
        _arm_sgf(payload, jurisdiction="GB", relabel=False)

    result = _evaluate(evidence, catalog=_catalog(transform))
    assert result is not None
    _assert_forged_cannot_approve(result)


def test_altered_clause_is_not_an_authoritative_pass() -> None:
    """A valid source_id does not authenticate replacement clause text."""
    original = next(rule.payload["clause"] for rule in load_catalog() if rule.rule_id == SGF_PRIOR)

    def transform(payload: dict) -> None:
        if payload.get("rule_id") == SGF_PRIOR:
            payload["clause"] = ALTERED_CLAUSE
            payload["source_statement"] = ALTERED_CLAUSE

    result = _evaluate(_musharakah_ibi("provenance-clause", "GB", True), catalog=_catalog(transform))
    if result is None:
        return
    row = _rule(result, SGF_PRIOR)
    assert not (_unsafe_source_conclusion(row) and row.get("source_clause") == ALTERED_CLAUSE), (
        f"original_clause={original!r} emitted_clause={row.get('source_clause')!r} "
        f"result={row['rule_result']} validation={row['validation_status']} "
        f"overall={result['overall_governance_status']}"
    )


def test_source_pass_does_not_treat_a_stored_hash_string_as_verified_bytes() -> None:
    """The register hash is not a digest check of source bytes available to this test."""
    source = source_by_id("SRC-SBP-SGF-2025-TEXT", load_source_register())
    result = _evaluate(_musharakah_ibi("provenance-hash", "GB", True))
    if result is None:
        return
    row = _rule(result, SGF_PRIOR)
    assert not _unsafe_source_conclusion(row) or row.get("source_digest_verified") is True, (
        f"register_sha256_present={bool(source.sha256)} result={row['rule_result']} "
        f"row_has_verified_digest={row.get('source_digest_verified')!r} "
        f"overall={result['overall_governance_status']}"
    )


def test_evidence_schema_has_no_contract_or_effective_date() -> None:
    """Control. The schema cannot yet represent the dates a temporal rule would need."""
    assert set(ABSENT_TEMPORAL_FIELDS).isdisjoint(EVIDENCE_FIELDS)


def test_audit_timestamp_is_not_a_contract_date_for_source_pass() -> None:
    """evaluate(timestamp=...) is the audit clock. It does not authorize a dated instrument."""
    result = _evaluate(_musharakah_ibi("provenance-timestamp", "GB", True), timestamp=PRE_FRAMEWORK_TS)
    if result is None:
        return
    row = _rule(result, SGF_PRIOR)
    evidence = row["input_evidence"]
    assert row["timestamp"] == PRE_FRAMEWORK_TS
    assert set(ABSENT_TEMPORAL_FIELDS).isdisjoint(evidence)
    assert not _unsafe_source_conclusion(row), (
        f"audit_timestamp={row['timestamp']} source_version={row.get('source_version')!r} "
        f"result={row['rule_result']} overall={result['overall_governance_status']} "
        f"fusion={_fuse(result['overall_governance_status'])}"
    )


@pytest.mark.parametrize("jurisdiction", SBP_JURISDICTIONS)
def test_customer_payment_hard_stop_is_not_an_authoritative_rejection(jurisdiction: str) -> None:
    payload = _payload(
        f"hard-customer-{jurisdiction}",
        contract_type="Murabahah",
        institution_class="IBI",
        jurisdiction=jurisdiction,
        sb_prior_product_approval=True,
        sb_approved_agreements_and_process_flows=True,
        invoice_name_status="bank_account_client",
        payment_channel="customer",
    )
    result = _evaluate(payload)
    if result is None:
        return
    row = _rule(result, PAY_RULE)
    status = result["overall_governance_status"]
    decision = _fuse(status)
    assert not _unsafe_source_conclusion(row) and decision != "REJECT", (
        f"jurisdiction={jurisdiction} rule={PAY_RULE} result={row['rule_result']} "
        f"reason={row['reason']!r} overall={status} fusion={decision} "
        f"certification={result['certification_claim']}"
    )


@pytest.mark.parametrize("jurisdiction", SBP_JURISDICTIONS)
def test_false_board_approval_hard_stop_is_not_an_authoritative_rejection(jurisdiction: str) -> None:
    payload = _musharakah_ibi(f"hard-board-{jurisdiction}", jurisdiction, False)
    result = _evaluate(payload)
    if result is None:
        return
    row = _rule(result, SGF_PRIOR)
    status = result["overall_governance_status"]
    decision = _fuse(status)
    assert not _unsafe_source_conclusion(row) and decision != "REJECT", (
        f"jurisdiction={jurisdiction} rule={SGF_PRIOR} result={row['rule_result']} "
        f"reason={row['reason']!r} overall={status} fusion={decision}"
    )


@pytest.mark.parametrize("jurisdiction", SECP_JURISDICTIONS)
def test_false_secp_certificate_hard_stop_is_not_an_authoritative_rejection(jurisdiction: str) -> None:
    payload = _security_claim(f"hard-secp-{jurisdiction}", jurisdiction, False)
    result = _evaluate(payload)
    if result is None:
        return
    row = _rule(result, SECP_RULE)
    status = result["overall_governance_status"]
    decision = _fuse(status)
    assert not _unsafe_source_conclusion(row) and decision != "REJECT", (
        f"jurisdiction={jurisdiction} rule={SECP_RULE} result={row['rule_result']} "
        f"reason={row['reason']!r} overall={status} fusion={decision}"
    )


def test_unknown_contract_certificate_flag_is_not_positive_applicability() -> None:
    payload = _payload(
        "unknown-contract-claim",
        contract_type="unknown",
        institution_class="other",
        jurisdiction="US",
        claims_shariah_compliant_security=True,
        secp_shariah_compliance_certificate=True,
    )
    result = _evaluate(payload)
    if result is None:
        return
    row = _rule(result, SECP_RULE)
    assert not _unsafe_source_conclusion(row), (
        f"result={row['rule_result']} reason={row['reason']!r} "
        f"layer={result['layer_a_completeness']['layer_a']} "
        f"identification={_rule(result, 'SH-ARCH-001')['rule_result']} "
        f"overall={result['overall_governance_status']}"
    )


def test_unknown_contract_does_not_approve() -> None:
    """Control. Incomplete identification stays nonaffirmative at the screen level."""
    payload = _payload(
        "unknown-contract-overall",
        contract_type="unknown",
        institution_class="other",
        jurisdiction="US",
        claims_shariah_compliant_security=True,
        secp_shariah_compliance_certificate=True,
    )
    result = _evaluate(payload)
    assert result is not None
    status = result["overall_governance_status"]
    assert result["layer_a_completeness"]["layer_a"] == "INSUFFICIENT"
    assert status != "PASS"
    assert _fuse(status) != "APPROVE"
    assert result["certification_claim"] is False


def test_checked_in_catalog_has_no_expert_validation_or_verified_scope() -> None:
    """Control. This test only reads the on-disk catalog."""
    catalog = json.loads((ROOT / "docs" / "shariah" / "rule_catalog.json").read_text(encoding="utf-8"))
    for rule in catalog["rules"]:
        assert rule.get("validation_status") != "EXPERT_VALIDATED"
        scope = rule.get("applicability_scope")
        assert not (isinstance(scope, dict) and scope.get("verified") is True)


def test_architecture_only_screen_stays_nonaffirmative() -> None:
    """Control. Identification architecture is not a source-regulatory approval."""
    result = _evaluate(
        _payload(
            "control-architecture",
            contract_type="Musharakah",
            institution_class="other",
            jurisdiction="GB",
        )
    )
    assert result is not None
    status = result["overall_governance_status"]
    assert status != "PASS"
    assert _fuse(status) != "APPROVE"
    assert result["certification_claim"] is False
    assert not _unsafe_source_conclusion(_rule(result, SGF_PRIOR))


def test_invalid_documentary_token_does_not_satisfy_invoice_predicate() -> None:
    """Control. The documentary Boolean correction still rejects a false token."""
    result = _evaluate(
        _payload(
            "control-doc-token",
            contract_type="Murabahah",
            institution_class="IBI",
            jurisdiction="PK",
            sb_prior_product_approval=True,
            sb_approved_agreements_and_process_flows=True,
            invoice_name_status="client_only",
            shariah_advisor_invoice_exception_approval="false",
            payment_channel="supplier",
        )
    )
    assert result is not None
    invoice = _rule(result, INVOICE_RULE)
    assert invoice["applicable"] is True
    assert invoice["rule_result"] != "PASS"
    assert result["certification_claim"] is False


def test_malformed_security_claim_is_rejected() -> None:
    """Control. A string claim is not Boolean evidence."""
    with pytest.raises(ValueError, match="claims_shariah_compliant_security"):
        evaluate(
            from_mapping(
                _payload(
                    "control-malformed-claim",
                    contract_type="conventional_credit",
                    institution_class="other",
                    jurisdiction="US",
                    claims_shariah_compliant_security="true",
                )
            ),
            timestamp=TS,
        )


def test_aaoifi_identity_gates_remain_dispatched() -> None:
    """Control. SS8 stays on Murabahah and SS9 stays on Ijarah. Neither gate passes."""
    murabahah = _evaluate(
        _payload("control-ss8", contract_type="Murabahah", institution_class="other", jurisdiction="PK")
    )
    ijarah = _evaluate(
        _payload("control-ss9", contract_type="Ijarah", institution_class="other", jurisdiction="PK")
    )
    assert murabahah is not None and ijarah is not None
    ss8_m = _rule(murabahah, "SH-AAOIFI-SS8-GATE")
    ss9_m = _rule(murabahah, "SH-AAOIFI-SS9-GATE")
    ss8_i = _rule(ijarah, "SH-AAOIFI-SS8-GATE")
    ss9_i = _rule(ijarah, "SH-AAOIFI-SS9-GATE")
    assert ss8_m["applicable"] is True and ss8_m["rule_result"] == "INSUFFICIENT_INFORMATION"
    assert ss9_m["applicable"] is False and ss9_m["rule_result"] == "NOT_APPLICABLE"
    assert ss8_i["applicable"] is False and ss8_i["rule_result"] == "NOT_APPLICABLE"
    assert ss9_i["applicable"] is True and ss9_i["rule_result"] == "INSUFFICIENT_INFORMATION"
    assert murabahah["certification_claim"] is False
    assert ijarah["certification_claim"] is False


def test_lendingclub_l2_stays_unknown_and_insufficient() -> None:
    """Control. An ordinary LendingClub row is not an Islamic contract or an SECP security."""
    result = evaluate_lendingclub_application(
        {"_fixture_key": "applicability-lc", "purpose": "car", "id": "synthetic-applicability"},
        timestamp=TS,
        synthetic=True,
    )
    evidence = result["rule_evaluations"][0]["input_evidence"]
    secp = _rule(result, SECP_RULE)
    assert result["contract_type"] == "unknown"
    assert "purpose" not in evidence
    assert evidence["claims_shariah_compliant_security"] is None
    assert secp["rule_result"] != "PASS"
    assert result["overall_governance_status"] == "INSUFFICIENT_INFORMATION"
    assert result["certification_claim"] is False
    assert _fuse(result["overall_governance_status"]) != "APPROVE"


def test_frozen_decision_thresholds_remain_unchanged() -> None:
    """Control. This file only reads the frozen policy."""
    freeze = load_frozen_thresholds()
    assert freeze["t_low"] == EXPECTED_T_LOW
    assert freeze["t_high"] == EXPECTED_T_HIGH
    assert freeze["selection_split"] == "validation"
