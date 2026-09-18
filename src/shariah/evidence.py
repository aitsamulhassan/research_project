"""Layer A: evidence completeness. Missing data is never treated as PASS."""

from __future__ import annotations

from typing import Any

from shariah.schema import FinancingEvidence, LAYER_A


NAMED_UNVERIFIED_STANDARDS = {
    "Murabahah": "AAOIFI SS (8) Murabahah identity verified; operative clauses not retrieved from official text.",
    "Ijarah": "AAOIFI SS (9) Ijarah identity verified; operative clauses not retrieved from official text.",
    "Ijarah_Muntahia_Bittamleek": "AAOIFI SS (9) Ijarah and Ijarah Muntahia Bittamleek identity verified; operative clauses not retrieved from official text.",
}


def _present(value: Any) -> bool:
    return value is not None and value != "" and value != "unknown"


def required_fields_for(evidence: FinancingEvidence) -> list[str]:
    fields = ["contract_type", "institution_class"]
    if evidence.contract_type in {"unknown", "ambiguous"}:
        return ["contract_type"]
    if evidence.institution_class == "IBI":
        fields.extend(["sb_prior_product_approval", "sb_approved_agreements_and_process_flows"])
    if evidence.contract_type == "Murabahah" and evidence.institution_class == "IBI":
        fields.extend(["invoice_name_status", "payment_channel"])
        if evidence.invoice_name_status == "client_only":
            fields.append("shariah_advisor_invoice_exception_approval")
        if evidence.invoice_name_status == "no_formal_invoice":
            fields.extend(["alternative_purchase_documents_present", "shariah_advisor_invoice_exception_approval"])
        if evidence.payment_channel == "agent":
            fields.extend(["shariah_advisor_agent_payment_approval", "agent_payment_reasons_recorded"])
    if evidence.claims_shariah_compliant_security:
        fields.append("secp_shariah_compliance_certificate")
    return fields


def field_value(evidence: FinancingEvidence, name: str) -> Any:
    return evidence.as_dict().get(name)


def completeness(evidence: FinancingEvidence) -> dict[str, Any]:
    required = required_fields_for(evidence)
    missing = [name for name in required if not _present(field_value(evidence, name))]
    named_gap = NAMED_UNVERIFIED_STANDARDS.get(evidence.contract_type)
    if evidence.contract_type in {"unknown"} or evidence.institution_class == "lendingclub_application":
        status = "INSUFFICIENT"
        reason = "Contract-level Shariah evidence is not available for this profile."
    elif evidence.contract_type == "ambiguous":
        status = "PARTIAL"
        reason = "Contract type is ambiguous; identification is incomplete."
    elif missing:
        status = "INSUFFICIENT"
        reason = "Required fields for applicable verified operational rules are missing: " + ", ".join(missing)
    elif named_gap:
        status = "PARTIAL"
        reason = named_gap
    else:
        status = "COMPLETE"
        reason = "Required evidence for applicable verified operational rules is present; no named unverified standard applies."
    assert status in LAYER_A
    return {
        "layer_a": status,
        "required_fields": required,
        "missing_fields": missing,
        "named_unverified_standard_gap": named_gap,
        "reason": reason,
        "synthetic": evidence.synthetic,
        "case_id": evidence.case_id,
    }
