"""L1 dataset / integration readiness. Not an applicant-level religious ruling."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from shariah.engine import AMENDMENT_ID, L1L2_VERSION
from shariah.schema import EVIDENCE_FIELDS, FIREWALL_FIELDS

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_SCHEMA_PATH = ROOT / "docs" / "shariah" / "evidence_schema.json"

L1_LC_STATUS = "INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION"
EVALUATION_MODE_DATASET = "DATASET_INTEGRATION"
DATASET_ID_LENDINGCLUB = "lendingclub"
LENDINGCLUB_DATASET_IDS = frozenset({"lendingclub", "lendingclub_granting_v0.1"})

# Documented Stage 2 LendingClub columns. Not derived from the protected TEST split.
LENDINGCLUB_DOCUMENTED_COLUMNS = (
    "id",
    "issue_d",
    "revenue",
    "dti_n",
    "loan_amnt",
    "fico_n",
    "experience_c",
    "emp_length",
    "purpose",
    "home_ownership_n",
    "addr_state",
    "zip_code",
    "Default",
    "title",
    "desc",
)

L1_REASON = (
    "LendingClub is a conventional historical consumer-credit application dataset. "
    "Its documented schema does not contain contractual or institutional Shariah-governance "
    "evidence required for applicant-level determination under AMENDMENT-SHARIAH-001. "
    "This L1 status is dataset/integration readiness, not an applicant-level religious ruling."
)


def contractual_schema_field_names(schema_path: Path | None = None) -> tuple[str, ...]:
    payload = json.loads((schema_path or EVIDENCE_SCHEMA_PATH).read_text(encoding="utf-8"))
    return tuple(item["evidence_item"] for item in payload["items"])


def _as_field_set(available_fields: Iterable[str] | None) -> set[str]:
    if available_fields is None:
        return set(LENDINGCLUB_DOCUMENTED_COLUMNS)
    return {str(name) for name in available_fields}


def assess_dataset_readiness(
    dataset_id: str = DATASET_ID_LENDINGCLUB,
    available_fields: Sequence[str] | Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return L1 readiness for a dataset/integration context.

    LendingClub L1 is frozen by AMENDMENT-SHARIAH-001 as
    INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION. This function does not read
    TRAIN/VALIDATION/TEST rows.
    """
    if dataset_id not in LENDINGCLUB_DATASET_IDS:
        raise ValueError(f"No L1 readiness mapping for dataset_id={dataset_id!r}.")
    if isinstance(available_fields, Mapping):
        fields = _as_field_set(available_fields.keys())
    else:
        fields = _as_field_set(available_fields)
    required = contractual_schema_field_names()
    present = [name for name in required if name in fields]
    missing = [name for name in required if name not in fields]
    firewall_in_schema = sorted(name for name in FIREWALL_FIELDS if name in fields)
    identity_fields = [name for name in EVIDENCE_FIELDS if name not in {"case_id", "synthetic"}]
    return {
        "layer": "L1",
        "dataset_id": dataset_id,
        "readiness_status": L1_LC_STATUS,
        "is_applicant_level_ruling": False,
        "evaluation_mode": EVALUATION_MODE_DATASET,
        "amendment_id": AMENDMENT_ID,
        "l1l2_version": L1L2_VERSION,
        "status_basis": "AMENDMENT-SHARIAH-001 frozen LendingClub L1",
        "documented_columns_used": available_fields is None,
        "available_field_count": len(fields),
        "contractual_schema_fields_present": present,
        "contractual_schema_fields_missing": missing,
        "firewall_fields_present_in_schema": firewall_in_schema,
        "governance_evidence_fields_expected": list(identity_fields),
        "reason": L1_REASON,
        "certification_claim": False,
        "disclaimer": (
            "L1 is dataset/integration readiness only. It is not a Shariah ruling "
            "and is not an applicant-level determination."
        ),
    }
