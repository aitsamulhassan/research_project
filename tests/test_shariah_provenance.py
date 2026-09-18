"""Provenance integrity tests for Stage 7."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shariah.provenance import load_source_register  # noqa: E402
from shariah.validation import assert_rule_executable, assert_source_fields  # noqa: E402

CATALOG = json.loads((ROOT / "docs" / "shariah" / "rule_catalog.json").read_text(encoding="utf-8"))
AUDIT = ROOT / "audit" / "stage7_shariah_run.json"
TABLE4 = ROOT / "results" / "shariah" / "tables" / "table4_governance_test_cases.csv"
TABLE5 = ROOT / "results" / "shariah" / "tables" / "table5_provenance_completeness.csv"


def test_every_source_has_url_and_authority() -> None:
    for src in load_source_register():
        payload = src.as_dict()
        assert_source_fields(payload)
        assert payload["authority"]
        assert payload["url"]
        assert payload["organization"]
        assert payload["document_title"]


def test_standard_present_where_applicable() -> None:
    for rule in CATALOG["rules"]:
        if rule.get("standard_applicable"):
            assert rule.get("standard")


def test_clause_not_marked_verified_without_evidence() -> None:
    for rule in CATALOG["rules"]:
        if rule.get("clause_verified"):
            assert rule.get("clause") not in {None, "", "NOT_VERIFIED"}
            assert rule.get("section") not in {None, "", "NOT_VERIFIED"}


def test_expert_validation_cannot_be_falsely_asserted() -> None:
    for rule in CATALOG["rules"]:
        assert rule.get("validation_status") != "EXPERT_VALIDATED"
        assert not rule.get("expert_validation_record")
    fake = dict(next(r for r in CATALOG["rules"] if r["executable"]))
    fake["validation_status"] = "EXPERT_VALIDATED"
    fake["expert_validation_record"] = None
    with pytest.raises(ValueError, match="EXPERT_VALIDATED"):
        assert_rule_executable(fake)


def test_unverified_rule_not_executable() -> None:
    row = next(r for r in CATALOG["rules"] if r["validation_status"] == "NOT_VERIFIED")
    assert row["executable"] is False
    with pytest.raises(ValueError, match="NOT_VERIFIED"):
        bad = dict(row)
        bad["executable"] = True
        assert_rule_executable(bad)


@pytest.mark.skipif(not (AUDIT.exists() and TABLE4.exists() and TABLE5.exists()), reason="Stage 7 artifacts not generated yet")
def test_artifact_metadata_and_no_expert_claim() -> None:
    import pandas as pd

    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    assert audit["credit_model_not_called"] is True
    assert audit["experiment_id"]
    table4 = pd.read_csv(TABLE4)
    assert (table4["synthetic"] == True).all()  # noqa: E712
    assert "experiment_id" in table4.columns
    table5 = pd.read_csv(TABLE5)
    assert "experiment_id" in table5.columns
    assert (table5["expert_validation"] != "EXPERT_VALIDATED").all()
