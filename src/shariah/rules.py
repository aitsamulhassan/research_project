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
    if ev.sb_prior_product_approval is None:
        return _result("INSUFFICIENT_INFORMATION", "Prior Shariah Board product approval status is unknown.")
    if ev.sb_prior_product_approval is False:
        return _result(
            "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
            "SGF Section 3.B.ii requires prior Shariah Board approval before an IBI offers or launches a product or service.",
        )
    return _result("PASS", "Evidence states prior Shariah Board product approval exists. This is not a certification.")


def eval_sb_docs_approval(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.institution_class != "IBI":
        return _skip("SGF document-approval rule applies to Islamic Banking Institutions only.")
    if ev.contract_type in {"unknown", "ambiguous", "conventional_credit"}:
        return _skip("No IBI Islamic product offering is in scope.")
    if ev.sb_approved_agreements_and_process_flows is None:
        return _result("INSUFFICIENT_INFORMATION", "Shariah Board approval of agreements/process flows is unknown.")
    if ev.sb_approved_agreements_and_process_flows is False:
        return _result(
            "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
            "SGF Section 3.B.iii requires Shariah Board review and approval of product programs/structures, process flows, and related agreements.",
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
        if ev.shariah_advisor_invoice_exception_approval is None:
            return _result("INSUFFICIENT_INFORMATION", "Client-name invoice requires documented Shariah Advisor approval; approval status unknown.")
        if ev.shariah_advisor_invoice_exception_approval is False:
            return _result(
                "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
                "Client-name Murabaha invoice without Shariah Advisor approval does not meet IBD Circular 01 of 2012 paragraph 1.",
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
    if ev.alternative_purchase_documents_present is None or ev.shariah_advisor_invoice_exception_approval is None:
        return _result(
            "INSUFFICIENT_INFORMATION",
            "IBD Circular 01 of 2012 paragraph 2 requires alternative purchase documents and Shariah Advisor approval when no formal invoice exists.",
        )
    if ev.alternative_purchase_documents_present is False or ev.shariah_advisor_invoice_exception_approval is False:
        return _result(
            "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
            "No formal invoice and missing alternative documents and/or Shariah Advisor approval; IBD Circular 01 of 2012 paragraph 2 is not met.",
        )
    return _result("PASS", "Alternative purchase documents with Shariah Advisor approval are present.")


def eval_murabaha_payment(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.contract_type != "Murabahah" or ev.institution_class != "IBI":
        return _skip("Payment-channel rule applies to IBI Murabaha only.")
    channel = ev.payment_channel
    if channel in {None, "unknown"}:
        return _result("INSUFFICIENT_INFORMATION", "Murabaha payment channel is unknown.")
    if channel in {"supplier", "escrow"}:
        return _result("PASS", "Payment is to the supplier or an escrow account as required by IBD Circular 01 of 2012 paragraph 4.")
    if channel == "agent":
        if ev.shariah_advisor_agent_payment_approval is None or ev.agent_payment_reasons_recorded is None:
            return _result(
                "INSUFFICIENT_INFORMATION",
                "Agent payment requires recorded reasons and Shariah Advisor approval; one or both are unknown.",
            )
        if ev.shariah_advisor_agent_payment_approval is False or ev.agent_payment_reasons_recorded is False:
            return _result(
                "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
                "Agent payment without recorded reasons and Shariah Advisor approval does not meet IBD Circular 01 of 2012 paragraph 4.",
            )
        return _result("PASS", "Agent payment has recorded reasons and Shariah Advisor approval.")
    if channel == "customer":
        return _result(
            "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
            "Payment to the customer rather than the supplier/escrow/approved-agent path does not meet IBD Circular 01 of 2012 paragraph 4.",
        )
    return _result("REVIEW", f"Payment channel {channel!r} is not in the configured vocabulary.")


def eval_secp_security_claim(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.institution_class == "IBI":
        return _skip("SECP Shariah Governance Regulations 2023 exclude SBP-regulated banking companies.")
    if ev.claims_shariah_compliant_security is not True:
        return _skip("No claim that a security is Shariah compliant.")
    if ev.secp_shariah_compliance_certificate is None:
        return _result("INSUFFICIENT_INFORMATION", "A Shariah-compliant-security claim is present but SECP certificate evidence is unknown.")
    if ev.secp_shariah_compliance_certificate is False:
        return _result(
            "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
            "SGR 2023 Regulation 7(2) states that no security shall be called a Shariah compliant security unless a Shariah compliance certificate has been granted by the Commission.",
        )
    return _result("PASS", "Evidence states a SECP Shariah compliance certificate exists for the claimed security. This is not a ruling by this engine.")


def eval_aaoifi_clause_gate(ev: FinancingEvidence) -> dict[str, Any]:
    if ev.contract_type == "Murabahah":
        return _result(
            "INSUFFICIENT_INFORMATION",
            "AAOIFI SS (8) is the named Murabahah standard on aaoifi.com, but official clause text is access-controlled/password-protected; this engine does not evaluate invented SS (8) conditions.",
        )
    if ev.contract_type in {"Ijarah", "Ijarah_Muntahia_Bittamleek"}:
        return _result(
            "INSUFFICIENT_INFORMATION",
            "AAOIFI SS (9) is the named Ijarah standard on aaoifi.com, but official clause text is access-controlled; this engine does not evaluate invented SS (9) conditions.",
        )
    return _skip("AAOIFI SS (8)/SS (9) clause gate applies only to Murabahah and Ijarah identifications.")


EVALUATORS: dict[str, EvalFn] = {
    "SH-ARCH-001": eval_contract_identification,
    "SH-ARCH-003": eval_lc_predictors_not_shariah,
    "SH-SBP-SGF-002": eval_sb_prior_approval,
    "SH-SBP-SGF-003": eval_sb_docs_approval,
    "SH-SBP-MUR-INV-001": eval_murabaha_invoice,
    "SH-SBP-MUR-INV-002": eval_murabaha_alt_docs,
    "SH-SBP-MUR-PAY-001": eval_murabaha_payment,
    "SH-SECP-SGR-SEC-001": eval_secp_security_claim,
    "SH-AAOIFI-SS8-GATE": eval_aaoifi_clause_gate,
    "SH-AAOIFI-SS9-GATE": eval_aaoifi_clause_gate,
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
