"""Shariah-oriented governance evidence types. Not a certification layer."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

OUTCOMES = (
    "PASS",
    "REVIEW",
    "NOT_STRUCTURABLE_WITHOUT_REDESIGN",
    "INSUFFICIENT_INFORMATION",
)

LAYER_A = ("COMPLETE", "PARTIAL", "INSUFFICIENT")

CONTRACT_TYPES = (
    "Murabahah",
    "Ijarah",
    "Ijarah_Muntahia_Bittamleek",
    "Musharakah",
    "Mudarabah",
    "Qard",
    "Salam",
    "Istisna",
    "conventional_credit",
    "unknown",
    "ambiguous",
)

INSTITUTION_CLASSES = (
    "IBI",
    "secp_ifi",
    "lendingclub_application",
    "other",
    "unknown",
)

LENDINGCLUB_PREDICTORS = (
    "revenue",
    "dti_n",
    "loan_amnt",
    "fico_n",
    "emp_length",
    "purpose",
    "home_ownership_n",
    "addr_state",
    "zip_code",
)

LENDINGCLUB_EXCLUDED = ("id", "issue_d", "experience_c", "title", "desc", "Default")

# AMENDMENT-SHARIAH-001 firewall. These must not enter the Shariah evidence object
# except as a deliberate extra injection in a boundary test (SH-ARCH-003).
FIREWALL_FIELDS = LENDINGCLUB_PREDICTORS + LENDINGCLUB_EXCLUDED

TRI = bool | None

EVIDENCE_FIELDS = (
    "case_id",
    "synthetic",
    "contract_type",
    "institution_class",
    "jurisdiction",
    "instrument_type",
    "sb_prior_product_approval",
    "sb_approved_agreements_and_process_flows",
    "invoice_name_status",
    "shariah_advisor_invoice_exception_approval",
    "alternative_purchase_documents_present",
    "payment_channel",
    "shariah_advisor_agent_payment_approval",
    "agent_payment_reasons_recorded",
    "claims_shariah_compliant_security",
    "secp_shariah_compliance_certificate",
    "underlying_asset_identified",
    "ownership_or_possession_evidence",
    "late_payment_treatment_documented",
    "contractual_sequence_documented",
)


@dataclass(frozen=True)
class FinancingEvidence:
    case_id: str
    synthetic: bool
    contract_type: str
    institution_class: str = "unknown"
    jurisdiction: str = "unknown"
    instrument_type: str = "unknown"
    sb_prior_product_approval: TRI = None
    sb_approved_agreements_and_process_flows: TRI = None
    invoice_name_status: str | None = None
    shariah_advisor_invoice_exception_approval: TRI = None
    alternative_purchase_documents_present: TRI = None
    payment_channel: str | None = None
    shariah_advisor_agent_payment_approval: TRI = None
    agent_payment_reasons_recorded: TRI = None
    claims_shariah_compliant_security: TRI = False
    secp_shariah_compliance_certificate: TRI = None
    underlying_asset_identified: TRI = None
    ownership_or_possession_evidence: TRI = None
    late_payment_treatment_documented: TRI = None
    contractual_sequence_documented: TRI = None
    extra: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "case_id": self.case_id,
            "synthetic": self.synthetic,
            "contract_type": self.contract_type,
            "institution_class": self.institution_class,
            "jurisdiction": self.jurisdiction,
            "instrument_type": self.instrument_type,
            "sb_prior_product_approval": self.sb_prior_product_approval,
            "sb_approved_agreements_and_process_flows": self.sb_approved_agreements_and_process_flows,
            "invoice_name_status": self.invoice_name_status,
            "shariah_advisor_invoice_exception_approval": self.shariah_advisor_invoice_exception_approval,
            "alternative_purchase_documents_present": self.alternative_purchase_documents_present,
            "payment_channel": self.payment_channel,
            "shariah_advisor_agent_payment_approval": self.shariah_advisor_agent_payment_approval,
            "agent_payment_reasons_recorded": self.agent_payment_reasons_recorded,
            "claims_shariah_compliant_security": self.claims_shariah_compliant_security,
            "secp_shariah_compliance_certificate": self.secp_shariah_compliance_certificate,
            "underlying_asset_identified": self.underlying_asset_identified,
            "ownership_or_possession_evidence": self.ownership_or_possession_evidence,
            "late_payment_treatment_documented": self.late_payment_treatment_documented,
            "contractual_sequence_documented": self.contractual_sequence_documented,
        }
        payload.update(self.extra)
        return payload


def tri(value: Any) -> TRI:
    if value is None or value == "unknown":
        return None
    if value is True or value == "true" or value is False or value == "false":
        return bool(value) if value != "false" else False
    if isinstance(value, str) and value.lower() in {"true", "yes"}:
        return True
    if isinstance(value, str) and value.lower() in {"false", "no"}:
        return False
    raise ValueError(f"Unsupported tri-state value: {value!r}")
