"""Minimal Stage 2 audit tests. No ML behaviour is tested."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from data.audit_datasets import (  # noqa: E402
    DOCUMENTED_LC_COLUMNS,
    EXPECTED_LC_FILENAME,
    EXPECTED_LC_MD5,
    EXPECTED_LC_SIZE,
    EXPECTED_UCI_ZIP_FILENAME,
    RAW_DIR,
    md5_file,
    sha256_file,
)

LC_PATH = RAW_DIR / EXPECTED_LC_FILENAME
UCI_PATH = RAW_DIR / EXPECTED_UCI_ZIP_FILENAME
MANIFEST = ROOT / "docs" / "raw_data_manifest.json"
STAGE_SUMMARY = ROOT / "results" / "metrics" / "stage2_summary.json"

REQUIRED_OUTPUTS = [
    ROOT / "docs" / "raw_data_manifest.csv",
    ROOT / "docs" / "raw_data_manifest.json",
    ROOT / "results" / "metrics" / "lendingclub_dimensions.json",
    ROOT / "docs" / "lendingclub_schema_report.md",
    ROOT / "results" / "tables" / "lendingclub_column_profile.csv",
    ROOT / "results" / "metrics" / "lendingclub_target_audit.json",
    ROOT / "results" / "metrics" / "lendingclub_temporal_audit.json",
    ROOT / "results" / "tables" / "lendingclub_date_distribution.csv",
    ROOT / "docs" / "lendingclub_leakage_audit.csv",
    ROOT / "docs" / "lendingclub_leakage_audit.md",
    ROOT / "results" / "tables" / "lendingclub_purpose_audit.csv",
    ROOT / "docs" / "lendingclub_purpose_audit.md",
    ROOT / "docs" / "lendingclub_privacy_audit.csv",
    ROOT / "results" / "tables" / "lendingclub_missingness.csv",
    ROOT / "docs" / "lendingclub_integrity_audit.md",
    ROOT / "results" / "tables" / "lendingclub_integrity_findings.csv",
    ROOT / "results" / "tables" / "lendingclub_numeric_profile.csv",
    ROOT / "results" / "tables" / "lendingclub_categorical_profile.csv",
    ROOT / "docs" / "uci_schema_report.md",
    ROOT / "results" / "tables" / "uci_column_profile.csv",
    ROOT / "results" / "metrics" / "uci_dataset_audit.json",
    ROOT / "docs" / "dataset_comparability.md",
    ROOT / "docs" / "dataset_card.md",
    ROOT / "docs" / "dataset_decision.md",
    ROOT / "docs" / "STAGE_2_DATA_AUDIT_REPORT.md",
    ROOT / "audit" / "data_audit_run.json",
    ROOT / "results" / "metrics" / "stage2_summary.json",
]


def test_raw_files_exist() -> None:
    assert LC_PATH.is_file(), f"Missing raw LendingClub file: {LC_PATH}"
    assert UCI_PATH.is_file(), f"Missing raw UCI zip: {UCI_PATH}"
    assert LC_PATH.stat().st_size > 0
    assert UCI_PATH.stat().st_size > 0


def test_hashes_can_be_reproduced() -> None:
    lc_sha = sha256_file(LC_PATH)
    uci_sha = sha256_file(UCI_PATH)
    lc_md5 = md5_file(LC_PATH)
    assert len(lc_sha) == 64
    assert len(uci_sha) == 64
    assert lc_md5 == EXPECTED_LC_MD5
    assert LC_PATH.stat().st_size == EXPECTED_LC_SIZE
    if MANIFEST.is_file():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        by_name = {row["filename"]: row for row in manifest}
        assert by_name[EXPECTED_LC_FILENAME]["sha256"] == lc_sha
        assert by_name[EXPECTED_UCI_ZIP_FILENAME]["sha256"] == uci_sha


def test_target_column_found_from_verified_schema() -> None:
    header = pd.read_csv(LC_PATH, nrows=0)
    columns = list(header.columns)
    assert "Default" in columns
    assert columns == DOCUMENTED_LC_COLUMNS


def test_audit_outputs_are_generated() -> None:
    missing = [str(path.relative_to(ROOT)) for path in REQUIRED_OUTPUTS if not path.is_file()]
    assert missing == [], f"Missing audit outputs: {missing}"
    summary = json.loads(STAGE_SUMMARY.read_text(encoding="utf-8"))
    assert summary["stage"] == "2"
    assert summary["modeling_started"] is False
    assert summary["test_set_created"] is False


def test_no_raw_file_is_modified() -> None:
    before_lc = sha256_file(LC_PATH)
    before_uci = sha256_file(UCI_PATH)
    if MANIFEST.is_file():
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        by_name = {row["filename"]: row for row in manifest}
        assert by_name[EXPECTED_LC_FILENAME]["sha256"] == before_lc
        assert by_name[EXPECTED_UCI_ZIP_FILENAME]["sha256"] == before_uci
    after_lc = sha256_file(LC_PATH)
    after_uci = sha256_file(UCI_PATH)
    assert after_lc == before_lc
    assert after_uci == before_uci
    run_path = ROOT / "audit" / "data_audit_run.json"
    if run_path.is_file():
        run = json.loads(run_path.read_text(encoding="utf-8"))
        assert run.get("raw_files_unmodified") is True
        assert run["dataset_hashes"][EXPECTED_LC_FILENAME] == before_lc
        assert run["dataset_hashes"][EXPECTED_UCI_ZIP_FILENAME] == before_uci
