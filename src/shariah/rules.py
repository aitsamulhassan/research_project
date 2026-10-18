"""Deterministic rule catalog loaders and evaluators. No ML."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from shariah.schema import FinancingEvidence
from shariah.validation import assert_rule_executable

ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "docs" / "shariah" / "rule_catalog.json"

EvalFn = Callable[[FinancingEvidence], dict[str, Any]]


def _skip(reason: str) -> dict[str, Any]:
    return {"applicable": False, "rule_result": None, "reason": reason}


def _result(outcome: str, reason: str, applicable: bool = True) -> dict[str, Any]:
    return {"applicable": applicable, "rule_result": outcome, "reason": reason}


def _board_approval_state(value: Any) -> str:
    """Classify one SBP board-approval flag without coercing other types.

    None is missing evidence. Only an exact Python bool is approval evidence:
    True may satisfy the predicate, and False is a documented refusal.
    Every other supplied value is invalid, including "true", "false", "",
    "unknown", 0, and 1. bool is a subclass of int, so this uses an exact
    type test rather than an int test. Invalid values are not converted into
    True, False, or a regulatory finding.
    """
    if value is None:
        return "missing"
    if type(value) is bool:
        return "approved" if value else "refused"
    return "invalid"


def _paired_documentary_result(
    left: Any,
    right: Any,
    *,
    left_name: str,
    right_name: str,
    missing_reason: str,
    refused_reason: str,
    pass_reason: str,
) -> dict[str, Any]:
    """Apply the exact-bool contract to two required documentary flags.

    Missing evidence wins, then a documented Boolean refusal, then a
    malformed value. PASS requires both flags to be exact True.
    """
    states = {
        left_name: _board_approval_state(left),
        right_name: _board_approval_state(right),
    }
    if "missing" in states.values():
        return _result("INSUFFICIENT_INFORMATION", missing_reason)
    if "refused" in states.values():
        return _result("NOT_STRUCTURABLE_WITHOUT_REDESIGN", refused_reason)
    invalid = [name for name, state in states.items() if state == "invalid"]
    if invalid:
        if len(invalid) == 1:
            detail = f"{invalid[0]} was supplied as a non-Boolean value. This screen does not treat that value as affirmative evidence or as a documented refusal."
        else:
            detail = (
                f"{invalid[0]} and {invalid[1]} were supplied as non-Boolean values. "
                "This screen does not treat those values as affirmative evidence or as a documented refusal."
            )
        return _result("REVIEW", detail)
    return _result("PASS", pass_reason)


def eval_contract_identification(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.contract_type == "ambiguous":
        return _result("REVIEW", "Contract type is ambiguous; qualified review is required before rule application.")
    if ev.contract_type == "unknown":
        return _result(
            "INSUFFICIENT_INFORMATION",
            "Contract type is not identified, so structure-specific screening cannot run.",
        )
    return _result("PASS", "Contract type is identified for scoping. This is not a religious ruling.")


def eval_lc_predictors_not_shariah(ev: FinancingEvidence) -> dict[str, Any]:
    leaked = [k for k in ev.extra if k in {
        "revenue", "dti_n", "loan_amnt", "fico_n", "emp_length", "purpose",
        "home_ownership_n", "addr_state", "zip_code", "id", "issue_d",
        "experience_c", "title", "desc", "Default",
    }]
    if leaked:
        return _result(
            "REVIEW",
            "LendingClub credit fields were supplied to the Shariah layer and are not interpreted as Shariah variables; review required because the input boundary was violated.",
        )
    return _result("PASS", "No LendingClub credit predictor was treated as a Shariah variable.")


def eval_sb_prior_approval(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.institution_class != "IBI":
        return _skip("SGF product-approval rule applies to Islamic Banking Institutions only.")
    if ev.contract_type in {"unknown", "ambiguous", "conventional_credit"}:
        return _skip("No IBI Islamic product offering is in scope for this identification.")
    state = _board_approval_state(ev.sb_prior_product_approval)
    if state == "missing":
        return _result("INSUFFICIENT_INFORMATION", "Prior Shariah Board product approval status is unknown.")
    if state == "refused":
        return _result(
            "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
            "SGF Section 3.B.ii requires prior Shariah Board approval before an IBI offers or launches a product or service.",
        )
    if state == "invalid":
        return _result(
            "REVIEW",
            "Prior Shariah Board product approval was supplied as a non-Boolean value. "
            "This screen does not treat that value as approval or as a documented refusal.",
        )
    return _result("PASS", "Evidence states prior Shariah Board product approval exists. This is not a certification.")


def eval_sb_docs_approval(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.institution_class != "IBI":
        return _skip("SGF document-approval rule applies to Islamic Banking Institutions only.")
    if ev.contract_type in {"unknown", "ambiguous", "conventional_credit"}:
        return _skip("No IBI Islamic product offering is in scope.")
    state = _board_approval_state(ev.sb_approved_agreements_and_process_flows)
    if state == "missing":
        return _result("INSUFFICIENT_INFORMATION", "Shariah Board approval of agreements/process flows is unknown.")
    if state == "refused":
        return _result(
            "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
            "SGF Section 3.B.iii requires Shariah Board review and approval of product programs/structures, process flows, and related agreements.",
        )
    if state == "invalid":
        return _result(
            "REVIEW",
            "Shariah Board approval of agreements and process flows was supplied as a non-Boolean value. "
            "This screen does not treat that value as approval or as a documented refusal.",
        )
    return _result("PASS", "Evidence states Shariah Board approved the agreements and process flows.")


def eval_murabaha_invoice(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.contract_type != "Murabahah" or ev.institution_class != "IBI":
        return _skip("IBD Circular 01 of 2012 invoice instructions apply to IBI Murabaha only.")
    status = ev.invoice_name_status
    if status in {None, "unknown"}:
        return _result("INSUFFICIENT_INFORMATION", "Murabaha invoice naming status is unknown.")
    if status == "bank_account_client":
        return _result("PASS", "Invoice is in the Bank-Account Client form described in IBD Circular 01 of 2012 paragraph 1.")
    if status == "client_only":
        state = _board_approval_state(ev.shariah_advisor_invoice_exception_approval)
        if state == "missing":
            return _result("INSUFFICIENT_INFORMATION", "Client-name invoice requires documented Shariah Advisor approval; approval status unknown.")
        if state == "refused":
            return _result(
                "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
                "Client-name Murabaha invoice without Shariah Advisor approval does not meet IBD Circular 01 of 2012 paragraph 1.",
            )
        if state == "invalid":
            return _result(
                "REVIEW",
                "Client-name invoice Shariah Advisor approval was supplied as a non-Boolean value. "
                "This screen does not treat that value as approval or as a documented refusal.",
            )
        return _result("PASS", "Client-name invoice is accompanied by Shariah Advisor approval as permitted by IBD Circular 01 of 2012 paragraph 1.")
    if status == "no_formal_invoice":
        return _skip("No formal invoice; alternative-document rule applies instead.")
    return _result("REVIEW", f"Invoice naming status {status!r} is not in the configured vocabulary.")


def eval_murabaha_alt_docs(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.contract_type != "Murabahah" or ev.institution_class != "IBI":
        return _skip("Alternative-document rule applies to IBI Murabaha only.")
    if ev.invoice_name_status != "no_formal_invoice":
        return _skip("Formal invoice path is in use; paragraph 2 is not engaged.")
    return _paired_documentary_result(
        ev.alternative_purchase_documents_present,
        ev.shariah_advisor_invoice_exception_approval,
        left_name="alternative_purchase_documents_present",
        right_name="shariah_advisor_invoice_exception_approval",
        missing_reason=(
            "IBD Circular 01 of 2012 paragraph 2 requires alternative purchase documents "
            "and Shariah Advisor approval when no formal invoice exists."
        ),
        refused_reason=(
            "No formal invoice and missing alternative documents and/or Shariah Advisor approval; "
            "IBD Circular 01 of 2012 paragraph 2 is not met."
        ),
        pass_reason="Alternative purchase documents with Shariah Advisor approval are present.",
    )


def eval_murabaha_payment(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.contract_type != "Murabahah" or ev.institution_class != "IBI":
        return _skip("Payment-channel rule applies to IBI Murabaha only.")
    channel = ev.payment_channel
    if channel in {None, "unknown"}:
        return _result("INSUFFICIENT_INFORMATION", "Murabaha payment channel is unknown.")
    if channel in {"supplier", "escrow"}:
        return _result("PASS", "Payment is to the supplier or an escrow account as required by IBD Circular 01 of 2012 paragraph 4.")
    if channel == "agent":
        return _paired_documentary_result(
            ev.shariah_advisor_agent_payment_approval,
            ev.agent_payment_reasons_recorded,
            left_name="shariah_advisor_agent_payment_approval",
            right_name="agent_payment_reasons_recorded",
            missing_reason="Agent payment requires recorded reasons and Shariah Advisor approval; one or both are unknown.",
            refused_reason=(
                "Agent payment without recorded reasons and Shariah Advisor approval "
                "does not meet IBD Circular 01 of 2012 paragraph 4."
            ),
            pass_reason="Agent payment has recorded reasons and Shariah Advisor approval.",
        )
    if channel == "customer":
        return _result(
            "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
            "Payment to the customer rather than the supplier/escrow/approved-agent path does not meet IBD Circular 01 of 2012 paragraph 4.",
        )
    return _result("REVIEW", f"Payment channel {channel!r} is not in the configured vocabulary.")


def eval_secp_security_claim(ev: FinancingEvidence) -> dict[str, Any]:
    claim = ev.claims_shariah_compliant_security
    if claim is not None and type(claim) is not bool:
        raise ValueError(
            "claims_shariah_compliant_security has invalid evidence type "
            f"{type(claim).__name__}. Only exact Boolean True, exact Boolean False, or None are accepted."
        )
    if ev.institution_class == "IBI":
        return _skip("SECP Shariah Governance Regulations 2023 exclude SBP-regulated banking companies.")
    if claim is None:
        return _skip("Claim information was not provided or remains unknown.")
    if claim is False:
        return _skip("The input declares that no security-compliance claim is being made.")
    state = _board_approval_state(ev.secp_shariah_compliance_certificate)
    if state == "missing":
        return _result("INSUFFICIENT_INFORMATION", "A Shariah-compliant-security claim is present but SECP certificate evidence is unknown.")
    if state == "refused":
        return _result(
            "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
            "SGR 2023 Regulation 7(2) states that no security shall be called a Shariah compliant security unless a Shariah compliance certificate has been granted by the Commission.",
        )
    if state == "invalid":
        return _result(
            "REVIEW",
            "SECP certificate evidence was supplied as a non-Boolean value. "
            "This screen does not treat that value as a certificate or as a documented refusal.",
        )
    return _result("PASS", "Evidence states a SECP Shariah compliance certificate exists for the claimed security. This is not a ruling by this engine.")


def eval_aaoifi_ss8_gate(ev: FinancingEvidence) -> dict[str, Any]:
    """Identity gate for SS (8). Applicable only to Murabahah. Not a clause ruling."""
    if ev.contract_type != "Murabahah":
        return _skip("SH-AAOIFI-SS8-GATE applies only to a Murabahah identification. It does not evaluate SS (8) clauses.")
    return _result(
        "INSUFFICIENT_INFORMATION",
        "AAOIFI SS (8) is the named Murabahah standard on aaoifi.com, but official clause text is access-controlled/password-protected; this engine does not evaluate invented SS (8) conditions.",
    )


def eval_aaoifi_ss9_gate(ev: FinancingEvidence) -> dict[str, Any]:
    """Identity gate for SS (9). Applicable to the existing Ijarah family. Not a clause ruling."""
    if ev.contract_type not in {"Ijarah", "Ijarah_Muntahia_Bittamleek"}:
        return _skip(
            "SH-AAOIFI-SS9-GATE applies only to Ijarah or Ijarah Muntahia Bittamleek identifications. "
            "It does not evaluate SS (9) clauses."
        )
    return _result(
        "INSUFFICIENT_INFORMATION",
        "AAOIFI SS (9) is the named Ijarah standard on aaoifi.com, but official clause text is access-controlled; this engine does not evaluate invented SS (9) conditions.",
    )


EVALUATORS: dict[str, EvalFn] = {
    "SH-ARCH-001": eval_contract_identification,
    "SH-ARCH-003": eval_lc_predictors_not_shariah,
    "SH-SBP-SGF-002": eval_sb_prior_approval,
    "SH-SBP-SGF-003": eval_sb_docs_approval,
    "SH-SBP-MUR-INV-001": eval_murabaha_invoice,
    "SH-SBP-MUR-INV-002": eval_murabaha_alt_docs,
    "SH-SBP-MUR-PAY-001": eval_murabaha_payment,
    "SH-SECP-SGR-SEC-001": eval_secp_security_claim,
    "SH-AAOIFI-SS8-GATE": eval_aaoifi_ss8_gate,
    "SH-AAOIFI-SS9-GATE": eval_aaoifi_ss9_gate,
}


@dataclass(frozen=True)
class Rule:
    payload: dict[str, Any]

    @property
    def rule_id(self) -> str:
        return str(self.payload["rule_id"])

    def evaluate(self, evidence: FinancingEvidence) -> dict[str, Any]:
        if not self.payload.get("executable"):
            raise RuntimeError(f"{self.rule_id} is not executable as an authoritative rule.")
        fn = EVALUATORS[self.rule_id]
        return fn(evidence)


def load_catalog(path: Path | None = None) -> list[Rule]:
    blob = json.loads((path or CATALOG_PATH).read_text(encoding="utf-8"))
    rules = []
    for row in blob["rules"]:
        assert_rule_executable(row)
        if row.get("executable"):
            if row["rule_id"] not in EVALUATORS:
                raise KeyError(f"No evaluator for {row['rule_id']}")
            rules.append(Rule(row))
    return rules
