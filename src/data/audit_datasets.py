"""Stage 2 forensic dataset audit.

Reads immutable raw files, writes diagnostic reports, and never trains models
or modifies files under data/raw/.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import subprocess
import sys
import tempfile
import uuid
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

SCRIPT_VERSION = "stage2-0.1.0"
MISSINGNESS_LOW_MAX_PCT = 5.0
MISSINGNESS_MODERATE_MAX_PCT = 20.0
QUANTILES = [0.01, 0.05, 0.25, 0.50, 0.75, 0.95, 0.99]
FREE_TEXT_COLUMNS = {"title", "desc"}
IDENTIFIER_COLUMNS = {"id"}
ZENODO_DOI = "10.5281/zenodo.11295916"
ZENODO_URL = "https://doi.org/10.5281/zenodo.11295916"
ZENODO_RECORD_URL = "https://zenodo.org/records/11295916"
ZENODO_API_URL = "https://zenodo.org/api/records/11295916"
ZENODO_EVIDENCE = (
    "Zenodo record 10.5281/zenodo.11295916 version 0.1 dataset description "
    "(publication_date 2024-05-25; retrieved from official Zenodo API JSON)."
)
UCI_URL = "https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients"
UCI_DOI = "10.24432/C55S3H"
UCI_EVIDENCE = (
    "UCI Machine Learning Repository dataset 350 page (official URL) plus "
    "Additional Variable Information on that page; DOI 10.24432/C55S3H."
)
EXPECTED_LC_FILENAME = "LC_loans_granting_model_dataset.csv"
EXPECTED_LC_SIZE = 167468415
EXPECTED_LC_MD5 = "b019384d6bc65bf2a3e839362e4ff502"
EXPECTED_UCI_ZIP_FILENAME = "default+of+credit+card+clients.zip"
DOCUMENTED_LC_COLUMNS = [
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
]
DOCUMENTED_HOME_OWNERSHIP = {"mortgage", "rent", "own", "other"}
LC_TARGET_DOC_CONFLICT = (
    "Zenodo documentation states that Default=1 corresponds to charged off and "
    "Default=0 to fully paid, and that transitory loan_status values were removed. "
    "A later sentence says the release keeps loans that are either \"Fully Paid\" or "
    "\"Default\" (original loan_status names) and does not mention \"Charged Off\" in "
    "that filter sentence. Original loan_status also contains a rare 'Default' category "
    "distinct from 'Charged Off'. This internal documentation conflict is not silently "
    "reconciled."
)

REPO_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = REPO_ROOT / "data" / "raw"
DOCS_DIR = REPO_ROOT / "docs"
RESULTS_TABLES = REPO_ROOT / "results" / "tables"
RESULTS_METRICS = REPO_ROOT / "results" / "metrics"
AUDIT_DIR = REPO_ROOT / "audit"
SOURCE_META_DIR = AUDIT_DIR / "source_metadata"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
            return None
        return value
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        if np.isnan(value) or np.isinf(value):
            return None
        return float(value)
    if isinstance(value, (np.bool_,)):
        return bool(value)
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return str(value)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(json_safe(payload), indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if text.endswith("\n") else text + "\n", encoding="utf-8")


def write_csv_rows(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    names = fieldnames or list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=names, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: json_safe(row.get(k)) for k in names})


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def md5_file(path: Path) -> str:
    digest = hashlib.md5(usedforsecurity=False)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().lower()


def git_commit(root: Path) -> str | None:
    if not (root / ".git").exists():
        return None
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip() or None
    except (OSError, subprocess.CalledProcessError):
        return None


def missingness_class(pct: float) -> str:
    if pct == 0:
        return "NO_MISSINGNESS"
    if pct < MISSINGNESS_LOW_MAX_PCT:
        return "LOW_MISSINGNESS"
    if pct < MISSINGNESS_MODERATE_MAX_PCT:
        return "MODERATE_MISSINGNESS"
    return "HIGH_MISSINGNESS"


def redact_sample(column: str, value: Any) -> str:
    if pd.isna(value):
        return "<NA>"
    name = str(column)
    if name in IDENTIFIER_COLUMNS or name.lower() == "id":
        return "<REDACTED_IDENTIFIER>"
    if name in FREE_TEXT_COLUMNS:
        text = str(value)
        return f"<REDACTED_FREE_TEXT n_chars={len(text)}>"
    text = str(value)
    if len(text) > 80:
        return text[:77] + "..."
    return text


def unique_sample_values(series: pd.Series, column: str, n: int = 5) -> list[str]:
    non_null = series.dropna()
    if non_null.empty:
        return []
    unique_vals = non_null.drop_duplicates().head(n)
    return [redact_sample(column, v) for v in unique_vals.tolist()]


def parse_issue_d(series: pd.Series) -> pd.Series:
    raw = series.astype("string")
    parsed = pd.to_datetime(raw, format="%b-%Y", errors="coerce")
    still_null = parsed.isna() & raw.notna()
    if still_null.any():
        inferred = pd.to_datetime(raw[still_null], errors="coerce")
        parsed.loc[still_null] = inferred
    return parsed


def extract_license_from_uci_html(html_path: Path) -> dict[str, Any]:
    if not html_path.exists():
        return {
            "license": "LICENSE_UNVERIFIED",
            "evidence": "UCI dataset HTML was not captured locally.",
            "verified": False,
        }
    html = html_path.read_text(encoding="utf-8", errors="replace")
    has_cc_by = (
        "Creative Commons Attribution 4.0 International" in html
        and "CC BY 4.0" in html
    )
    if has_cc_by:
        return {
            "license": "CC BY 4.0",
            "license_url": "https://creativecommons.org/licenses/by/4.0/legalcode",
            "evidence": str(html_path.relative_to(REPO_ROOT)),
            "verified": True,
        }
    return {
        "license": "LICENSE_UNVERIFIED",
        "evidence": str(html_path.relative_to(REPO_ROOT)),
        "verified": False,
    }


def load_zenodo_record() -> dict[str, Any] | None:
    path = SOURCE_META_DIR / "zenodo_11295916_record.json"
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def convert_xls_to_csv_via_excel(xls_path: Path, csv_path: Path) -> None:
    xls = str(xls_path).replace("'", "''")
    csv_out = str(csv_path).replace("'", "''")
    script = f"""
$ErrorActionPreference = 'Stop'
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
try {{
  $wb = $excel.Workbooks.Open('{xls}')
  $wb.SaveAs('{csv_out}', 6)
  $wb.Close($false)
}} finally {{
  $excel.Quit()
  [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
  [GC]::Collect()
  [GC]::WaitForPendingFinalizers()
}}
"""
    completed = subprocess.run(
        ["powershell", "-NoProfile", "-Command", script],
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0 or not csv_path.exists():
        raise RuntimeError(
            "Excel COM conversion of UCI .xls failed. "
            f"stdout={completed.stdout!r} stderr={completed.stderr!r}"
        )


def load_uci_dataframe(zip_path: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    import zipfile

    with zipfile.ZipFile(zip_path) as archive:
        members = archive.namelist()
        xls_members = [name for name in members if name.lower().endswith(".xls")]
        if len(xls_members) != 1:
            raise RuntimeError(
                f"Expected exactly one .xls member in UCI zip, found {xls_members!r}."
            )
        xls_name = xls_members[0]
        xls_bytes = archive.read(xls_name)
        xls_info = archive.getinfo(xls_name)

    with tempfile.TemporaryDirectory(prefix="uci_audit_") as tmp:
        tmp_path = Path(tmp)
        xls_path = tmp_path / Path(xls_name).name
        csv_path = tmp_path / "uci_converted.csv"
        xls_path.write_bytes(xls_bytes)
        convert_xls_to_csv_via_excel(xls_path, csv_path)
        raw = pd.read_csv(csv_path, header=None, dtype=str, keep_default_na=False)
        raw = raw.replace({"": np.nan})

    if raw.shape[0] < 3:
        raise RuntimeError("UCI spreadsheet has fewer rows than expected (headers + data).")

    x_codes = ["" if pd.isna(v) else str(v).strip() for v in raw.iloc[0].tolist()]
    names = ["" if pd.isna(v) else str(v).strip() for v in raw.iloc[1].tolist()]
    if names[0] == "":
        names[0] = "ID"
    if x_codes[0] == "":
        x_codes[0] = "ID"
    data = raw.iloc[2:].copy()
    data.columns = names
    data = data.reset_index(drop=True)

    alias_map = {}
    for x_code, name in zip(x_codes, names):
        alias_map[name] = x_code

    numeric_like = [c for c in data.columns if c not in {"ID"}]
    for column in numeric_like:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    meta = {
        "zip_members": members,
        "xls_member": xls_name,
        "xls_member_size_bytes": xls_info.file_size,
        "header_row_x_codes": x_codes,
        "header_row_names": names,
        "alias_map": alias_map,
        "loader": "zipfile + Microsoft Excel COM SaveAs CSV (xlCSV=6) to a temporary file; raw zip was not modified",
    }
    return data, meta


def load_lendingclub(csv_path: Path) -> pd.DataFrame:
    return pd.read_csv(csv_path, low_memory=False)


def profile_columns(df: pd.DataFrame, redact: bool = True) -> list[dict[str, Any]]:
    rows = []
    n = len(df)
    for column in df.columns:
        series = df[column]
        null_count = int(series.isna().sum())
        non_null = n - null_count
        unique_count = int(series.nunique(dropna=True))
        sample = unique_sample_values(series, column if redact else "", n=5)
        rows.append(
            {
                "column": column,
                "dtype": str(series.dtype),
                "non_null_count": non_null,
                "null_count": null_count,
                "null_percentage": round(100.0 * null_count / n, 6) if n else None,
                "unique_count": unique_count,
                "sample_values": " | ".join(sample),
            }
        )
    return rows


def missingness_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    rows = []
    n = len(df)
    for column in df.columns:
        series = df[column]
        null_count = int(series.isna().sum())
        pct = 100.0 * null_count / n if n else 0.0
        non_null = series.dropna()
        min_non_null = None
        max_non_null = None
        if not non_null.empty and pd.api.types.is_numeric_dtype(non_null):
            min_non_null = json_safe(non_null.min())
            max_non_null = json_safe(non_null.max())
        rows.append(
            {
                "column": column,
                "missing_count": null_count,
                "missing_percentage": round(pct, 6),
                "minimum_non_null": min_non_null,
                "maximum_non_null": max_non_null,
                "missingness_class": missingness_class(pct),
            }
        )
    return rows


def numeric_profile(df: pd.DataFrame, exclude: set[str] | None = None) -> list[dict[str, Any]]:
    exclude = exclude or set()
    rows = []
    for column in df.columns:
        if column in exclude:
            continue
        series = df[column]
        if not pd.api.types.is_numeric_dtype(series):
            continue
        non_null = pd.to_numeric(series, errors="coerce").dropna()
        if non_null.empty:
            continue
        quant = {f"q{int(q * 100):02d}": json_safe(non_null.quantile(q)) for q in QUANTILES}
        row = {
            "column": column,
            "count": int(non_null.shape[0]),
            "min": json_safe(non_null.min()),
            "max": json_safe(non_null.max()),
            "mean": json_safe(non_null.mean()),
            "median": json_safe(non_null.median()),
            "std": json_safe(non_null.std(ddof=1) if len(non_null) > 1 else 0.0),
            "zero_count": int((non_null == 0).sum()),
            "negative_count": int((non_null < 0).sum()),
        }
        row.update(quant)
        rows.append(row)
    return rows


def categorical_profile(df: pd.DataFrame, columns: list[str], top_n: int = 20) -> list[dict[str, Any]]:
    rows = []
    n = len(df)
    for column in columns:
        if column not in df.columns:
            continue
        series = df[column]
        value_counts = series.value_counts(dropna=True)
        unique_count = int(series.nunique(dropna=True))
        if column in FREE_TEXT_COLUMNS:
            top_repr = "TOP_VALUES_REDACTED_FREE_TEXT"
            freqs = "REDACTED"
        else:
            top = value_counts.head(top_n)
            top_repr = " | ".join(f"{idx}={int(val)}" for idx, val in top.items())
            freqs = json.dumps(
                {str(idx): {"count": int(val), "pct": round(100.0 * val / n, 6)} for idx, val in top.items()},
                ensure_ascii=True,
            )
        rows.append(
            {
                "column": column,
                "unique_count": unique_count,
                "null_count": int(series.isna().sum()),
                "top_categories": top_repr,
                "top_category_frequencies_json": freqs,
            }
        )
    return rows


def lendingclub_leakage_rows(columns: list[str]) -> list[dict[str, Any]]:
    catalog = {
        "id": {
            "classification": "IDENTIFIER",
            "reason": (
                "Documented as a unique loan identifier. It does not encode credit "
                "risk attributes and must not be used as a model feature."
            ),
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": "Retain for audit/join only; exclude from features.",
        },
        "issue_d": {
            "classification": "POTENTIAL_LEAKAGE",
            "reason": (
                "Zenodo defines issue_d as the month and year in which the loan was "
                "approved. That is an origination/approval stamp, not an application "
                "date and not a post-servicing performance field. It is contemporaneous "
                "with the lending decision, not shown to be available before the "
                "decision. Using it as a predictive feature can encode time, policy, "
                "and origination-mix effects. Using it solely as a temporal index for "
                "later splits is a separate methodological choice and is not defined here."
            ),
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": (
                "Do not use as a predictive feature until methodology review. "
                "Candidate time index only. Split cutoffs are not defined in Stage 2."
            ),
        },
        "revenue": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": "Documented as borrower's self-declared annual income during registration.",
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": "Eligible application-time candidate feature.",
        },
        "dti_n": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": (
                "Listed among explanatory variables that the depositor states were "
                "known at the loan request. The same paragraph also says \"Monthly "
                "information\" and describes a co-borrower combined calculation. "
                "Application-time status is accepted from the depositor documentation "
                "with that wording ambiguity recorded; independent LC dictionary timing "
                "was not retrieved."
            ),
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "medium",
            "action_recommendation": (
                "Eligible candidate feature; TIMING wording ambiguity flagged for review."
            ),
        },
        "loan_amnt": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": "Documented as the amount of credit requested by the borrower.",
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": "Eligible application-time candidate feature.",
        },
        "fico_n": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": (
                "Documented as FICO based on historical credit information reported at "
                "the time of application (average of fico_range_low and fico_range_high)."
            ),
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": "Eligible application-time candidate feature.",
        },
        "experience_c": {
            "classification": "UNKNOWN",
            "reason": (
                "Documented as a binary indicator of whether the borrower is new to "
                "Lending Club, constructed from the credit date of a previous LC "
                "obligation and the credit date of the current obligation. The current "
                "obligation credit date is not independently shown to be an "
                "application-time field (it may coincide with issue/approval). "
                "TIMING_UNVERIFIED for the construction inputs."
            ),
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "low",
            "action_recommendation": (
                "Do not treat as confirmed application-time until methodology review. "
                "Do not drop silently."
            ),
        },
        "emp_length": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": "Documented as borrower employment length, including a no-information category.",
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": "Eligible application-time candidate feature.",
        },
        "purpose": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": "Documented as the credit purpose category for the loan request.",
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": (
                "Eligible application-time candidate feature and the documented "
                "financing-purpose field for later Shariah-oriented decision-support "
                "work. No Shariah rules are created in Stage 2."
            ),
        },
        "home_ownership_n": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": (
                "Documented as homeownership status provided during registration; "
                "depositor merged other/any/none into other."
            ),
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": "Eligible application-time candidate feature.",
        },
        "addr_state": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": "Documented as borrower's US residence state.",
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": "Eligible candidate feature; also a quasi-identifier.",
        },
        "zip_code": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": "Documented as zip code of the borrower's residence.",
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": "Eligible candidate feature; treat as quasi-identifier.",
        },
        "Default": {
            "classification": "TARGET",
            "reason": (
                "Documented binary final-resolution outcome (0 fully paid, 1 defaulted). "
                "Observed after origination by definition. See target-audit documentation conflict."
            ),
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": "Use only as the credit-risk target; never as a feature.",
        },
        "title": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": (
                "Documented as the borrower-provided title of the credit request. "
                "The depositor cleaned default web-form text, a dated borrower-added "
                "prefix, and HTML entities. Cleaning does not by itself move the field "
                "after the decision."
            ),
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": (
                "Free-text application-time field. Not a structured model feature unless "
                "a later protocol says so. Do not publish raw text."
            ),
        },
        "desc": {
            "classification": "SAFE_APPLICATION_TIME",
            "reason": (
                "Documented as the borrower-provided credit-request description, with "
                "the same depositor cleaning as title."
            ),
            "evidence_source": ZENODO_EVIDENCE,
            "confidence": "high",
            "action_recommendation": (
                "Free-text application-time field. Likely sparse. Do not publish raw text. "
                "No Shariah rules in Stage 2."
            ),
        },
    }
    rows = []
    for column in columns:
        if column in catalog:
            item = dict(catalog[column])
            item["column"] = column
            rows.append(item)
        else:
            rows.append(
                {
                    "column": column,
                    "classification": "UNKNOWN",
                    "reason": (
                        "Column is present in the raw file but is not in the Zenodo "
                        "documented variable list for this release. Timing was not guessed."
                    ),
                    "evidence_source": "Observed schema vs Zenodo documented variable list",
                    "confidence": "low",
                    "action_recommendation": "TIMING_UNVERIFIED. Do not drop silently. Flag for review.",
                }
            )
    return rows


def privacy_rows(columns: list[str]) -> list[dict[str, Any]]:
    catalog = {
        "id": ("DIRECT_IDENTIFIER", "Unique loan identifier documented by the depositor."),
        "issue_d": ("NON_IDENTIFYING", "Approval month/year; not a personal name or contact field."),
        "revenue": ("QUASI_IDENTIFIER", "Income can contribute to re-identification in combination with geography."),
        "dti_n": ("NON_IDENTIFYING", "Debt ratio; not a direct identifier."),
        "loan_amnt": ("NON_IDENTIFYING", "Requested loan amount."),
        "fico_n": ("NON_IDENTIFYING", "Credit score aggregate; not a direct identifier."),
        "experience_c": ("NON_IDENTIFYING", "Binary repeat-borrower flag."),
        "emp_length": ("NON_IDENTIFYING", "Binned employment length, not employer name. Employer name is not in this release."),
        "purpose": ("NON_IDENTIFYING", "Coarse financing-purpose category."),
        "home_ownership_n": ("NON_IDENTIFYING", "Coarse housing status."),
        "addr_state": ("QUASI_IDENTIFIER", "US state of residence."),
        "zip_code": ("QUASI_IDENTIFIER", "Residence zip code; samples in this release are 3-digit prefixes with xx."),
        "Default": ("NON_IDENTIFYING", "Outcome label."),
        "title": ("FREE_TEXT", "Borrower-provided free text; may incidentally contain identifying phrases. Raw values are not published in reports."),
        "desc": ("FREE_TEXT", "Borrower-provided free text; may incidentally contain identifying phrases. Raw values are not published in reports."),
    }
    rows = []
    for column in columns:
        if column in catalog:
            classification, reason = catalog[column]
        else:
            classification, reason = (
                "UNKNOWN",
                "Not classified from the Zenodo variable list; privacy class not guessed.",
            )
        rows.append(
            {
                "column": column,
                "classification": classification,
                "reason": reason,
                "evidence_source": ZENODO_EVIDENCE,
            }
        )
    return rows


def integrity_findings(df: pd.DataFrame, parsed_issue_d: pd.Series) -> list[dict[str, Any]]:
    findings = []
    n = len(df)

    def add(check: str, n_affected: int, note: str, severity: str) -> None:
        findings.append(
            {
                "check": check,
                "n_affected": int(n_affected),
                "n_total": n,
                "pct_affected": round(100.0 * n_affected / n, 6) if n else None,
                "severity": severity,
                "note": note,
            }
        )

    dup_rows = int(df.duplicated().sum())
    add("duplicate_rows", dup_rows, "Exact full-row duplicates.", "info" if dup_rows == 0 else "warning")

    if "id" in df.columns:
        dup_ids = int(df["id"].duplicated().sum())
        add("duplicate_id_values", dup_ids, "Repeated loan identifiers.", "info" if dup_ids == 0 else "warning")
        id_null = int(df["id"].isna().sum())
        add("null_id", id_null, "Missing loan identifiers.", "info" if id_null == 0 else "warning")
        if dup_ids:
            contradiction = (
                df.groupby("id")["Default"].nunique(dropna=False) > 1
            ).sum() if "Default" in df.columns else 0
            add(
                "duplicate_id_contradictory_target",
                int(contradiction),
                "Repeated IDs with more than one Default value.",
                "warning" if contradiction else "info",
            )

    if "Default" in df.columns:
        invalid_target = int((~df["Default"].isin([0, 1]) & df["Default"].notna()).sum())
        add("target_not_in_0_1", invalid_target, "Default values other than 0 or 1.", "warning" if invalid_target else "info")
        add("target_missing", int(df["Default"].isna().sum()), "Missing Default.", "warning" if df["Default"].isna().any() else "info")

    if "fico_n" in df.columns:
        fico = pd.to_numeric(df["fico_n"], errors="coerce")
        add("fico_below_300", int((fico < 300).sum()), "Below documented 300-850 range.", "warning")
        add("fico_above_850", int((fico > 850).sum()), "Above documented 300-850 range.", "warning")

    if "loan_amnt" in df.columns:
        amt = pd.to_numeric(df["loan_amnt"], errors="coerce")
        add("loan_amnt_non_positive", int((amt <= 0).sum()), "Requested amount <= 0.", "warning")

    if "revenue" in df.columns:
        rev = pd.to_numeric(df["revenue"], errors="coerce")
        add("revenue_negative", int((rev < 0).sum()), "Negative self-declared income.", "warning")
        add("revenue_zero", int((rev == 0).sum()), "Zero income; may be legitimate or a sentinel. Not deleted.", "info")

    if "dti_n" in df.columns:
        dti = pd.to_numeric(df["dti_n"], errors="coerce")
        add("dti_negative", int((dti < 0).sum()), "Negative DTI.", "warning")
        add("dti_ge_100", int((dti >= 100).sum()), "Extreme DTI >= 100; not deleted.", "info")
        add("dti_eq_999", int((dti == 999).sum()), "DTI equal to 999 (possible sentinel in some LC extracts).", "info")

    if "experience_c" in df.columns:
        exp = df["experience_c"]
        add(
            "experience_c_not_binary",
            int((~exp.isin([0, 1]) & exp.notna()).sum()),
            "Values other than 0/1.",
            "warning",
        )

    raw_issue = df["issue_d"] if "issue_d" in df.columns else None
    if raw_issue is not None:
        malformed = int(parsed_issue_d.isna().sum() - raw_issue.isna().sum())
        add("issue_d_malformed_unparseable", max(malformed, 0), "Non-null issue_d values that did not parse.", "warning")
        add("issue_d_missing", int(raw_issue.isna().sum()), "Missing issue_d.", "info")

    if "home_ownership_n" in df.columns:
        observed = {str(v).strip().lower() for v in df["home_ownership_n"].dropna().unique()}
        unexpected = sorted(observed - DOCUMENTED_HOME_OWNERSHIP)
        add(
            "home_ownership_unexpected_categories",
            int(df["home_ownership_n"].dropna().astype(str).str.strip().str.lower().isin(unexpected).sum()) if unexpected else 0,
            "Observed values not in documented {mortgage, rent, own, other} after case-normalisation: "
            + (", ".join(unexpected) if unexpected else "none"),
            "info" if not unexpected else "warning",
        )

    if "purpose" in df.columns:
        add("purpose_missing", int(df["purpose"].isna().sum()), "Missing purpose.", "info")

    return findings


def purpose_audit_rows(df: pd.DataFrame) -> list[dict[str, Any]]:
    specs = [
        (
            "purpose",
            "Credit purpose category for the loan request (Zenodo).",
            "SAFE_APPLICATION_TIME",
        ),
        (
            "title",
            "Title of the credit request description provided by the borrower (Zenodo).",
            "SAFE_APPLICATION_TIME",
        ),
        (
            "desc",
            "Description of the credit request provided by the borrower (Zenodo).",
            "SAFE_APPLICATION_TIME",
        ),
    ]
    rows = []
    n = len(df)
    present = set(df.columns)
    similar = [
        c
        for c in df.columns
        if c not in {"purpose", "title", "desc"}
        and any(token in c.lower() for token in ("purpose", "title", "desc", "reason"))
    ]
    for column, role, timing in specs:
        available = column in present
        if not available:
            rows.append(
                {
                    "column": column,
                    "availability": "ABSENT",
                    "missingness": None,
                    "unique_count": None,
                    "top_values": None,
                    "example_values": None,
                    "apparent_semantic_role": role,
                    "application_time_status": "NOT_APPLICABLE_FIELD_ABSENT",
                }
            )
            continue
        series = df[column]
        missing_pct = round(100.0 * float(series.isna().mean()), 6)
        unique_count = int(series.nunique(dropna=True))
        if column in FREE_TEXT_COLUMNS:
            top_values = "REDACTED_FREE_TEXT"
            example_values = "REDACTED_FREE_TEXT"
        else:
            top = series.value_counts(dropna=True).head(15)
            top_values = " | ".join(f"{idx}={int(val)}" for idx, val in top.items())
            example_values = " | ".join(redact_sample(column, v) for v in series.dropna().drop_duplicates().head(8).tolist())
        rows.append(
            {
                "column": column,
                "availability": "PRESENT",
                "missingness": missing_pct,
                "unique_count": unique_count,
                "top_values": top_values,
                "example_values": example_values,
                "apparent_semantic_role": role,
                "application_time_status": timing,
            }
        )
    for column in similar:
        rows.append(
            {
                "column": column,
                "availability": "PRESENT",
                "missingness": round(100.0 * float(df[column].isna().mean()), 6),
                "unique_count": int(df[column].nunique(dropna=True)),
                "top_values": "INSPECT_MANUALLY",
                "example_values": "NOT_EXPANDED",
                "apparent_semantic_role": "Name resembles a purpose/description field; semantic role not guessed beyond the name.",
                "application_time_status": "UNKNOWN",
            }
        )
    rows.append(
        {
            "column": "_similar_purpose_like_fields_other_than_purpose_title_desc",
            "availability": "NONE" if not similar else "PRESENT",
            "missingness": None,
            "unique_count": len(similar),
            "top_values": ",".join(similar) if similar else "",
            "example_values": "",
            "apparent_semantic_role": "Scan for additional purpose-like columns.",
            "application_time_status": "NOT_APPLICABLE",
        }
    )
    return rows


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    def cell(value: Any) -> str:
        text = "" if value is None else str(value)
        return text.replace("|", "\\|").replace("\n", " ")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(v) for v in row) + " |")
    return "\n".join(lines)


def audit_lendingclub(df: pd.DataFrame) -> dict[str, Any]:
    n_rows, n_cols = df.shape
    columns = list(df.columns)
    duplicate_column_names = [c for c, count in Counter(columns).items() if count > 1]
    duplicate_rows = int(df.duplicated().sum())
    duplicate_ids = int(df["id"].duplicated().sum()) if "id" in df.columns else None
    unique_ids = int(df["id"].nunique(dropna=True)) if "id" in df.columns else None

    dimensions = {
        "n_rows": int(n_rows),
        "n_columns": int(n_cols),
        "column_names": columns,
        "duplicate_column_names": duplicate_column_names,
        "duplicate_rows": duplicate_rows,
        "duplicate_applicant_or_loan_identifiers": duplicate_ids,
        "unique_id_count": unique_ids,
        "documented_column_names": DOCUMENTED_LC_COLUMNS,
        "columns_missing_from_documentation": [c for c in columns if c not in DOCUMENTED_LC_COLUMNS],
        "documented_columns_missing_from_file": [c for c in DOCUMENTED_LC_COLUMNS if c not in columns],
        "schema_matches_zenodo_variable_list": columns == DOCUMENTED_LC_COLUMNS,
    }

    column_profile = profile_columns(df)
    write_csv_rows(RESULTS_TABLES / "lendingclub_column_profile.csv", column_profile)

    target_name = "Default" if "Default" in df.columns else None
    target_audit: dict[str, Any]
    if target_name is None:
        target_audit = {
            "target_column": None,
            "target_definition_status": "TARGET_DEFINITION_UNVERIFIED",
            "reason": "No column named Default was found; target was not guessed.",
        }
        target_verified = False
    else:
        series = df[target_name]
        counts = series.value_counts(dropna=False).sort_index()
        value_records = []
        for value, count in counts.items():
            key = "NA" if pd.isna(value) else json_safe(value)
            value_records.append(
                {
                    "value": key,
                    "count": int(count),
                    "percentage": round(100.0 * count / n_rows, 6),
                }
            )
        missing = int(series.isna().sum())
        non_binary = int((~series.isin([0, 1]) & series.notna()).sum())
        prevalence_default = float((series == 1).mean()) if n_rows else None
        target_audit = {
            "target_column": target_name,
            "target_definition_from_documentation": (
                "Binary variable Default: 0 = fully paid, 1 = defaulted. The depositor "
                "states the default category corresponds to charged off and that "
                "transitory loan_status values were excluded."
            ),
            "target_definition_status": "TARGET_DEFINITION_DOCUMENTATION_CONFLICT",
            "documentation_conflict": LC_TARGET_DOC_CONFLICT,
            "unique_values": [json_safe(v) for v in series.dropna().unique().tolist()],
            "value_counts": value_records,
            "missing_target_rows": missing,
            "impossible_or_undocumented_target_values": non_binary,
            "prevalence_Default_eq_1": prevalence_default,
            "prevalence_Default_eq_1_percentage": round(100.0 * prevalence_default, 6) if prevalence_default is not None else None,
        }
        target_verified = True
        # Column identity and 0/1 coding are verified; original loan_status mapping is not.
        target_audit["column_and_binary_coding_verified"] = True
        target_audit["original_loan_status_mapping_verified"] = False

    write_json(RESULTS_METRICS / "lendingclub_target_audit.json", target_audit)

    parsed_issue = parse_issue_d(df["issue_d"]) if "issue_d" in df.columns else pd.Series(dtype="datetime64[ns]")
    temporal: dict[str, Any]
    if "issue_d" not in df.columns:
        temporal = {
            "issue_d_present": False,
            "temporal_field_verified": False,
            "note": "issue_d was not found. TIMING_UNVERIFIED.",
        }
        date_distribution: list[dict[str, Any]] = []
        temporal_verified = False
    else:
        non_null_raw = int(df["issue_d"].notna().sum())
        parsed_ok = parsed_issue.dropna()
        malformed = int(parsed_issue.isna().sum() - df["issue_d"].isna().sum())
        month_counts = (
            parsed_ok.dt.to_period("M").astype(str).value_counts().sort_index()
            if not parsed_ok.empty
            else pd.Series(dtype=int)
        )
        date_distribution = [
            {"year_month": str(idx), "count": int(val)} for idx, val in month_counts.items()
        ]
        other_date_like = [
            c
            for c in df.columns
            if c != "issue_d"
            and any(tok in c.lower() for tok in ("date", "_d", "time", "issue", "last_", "earliest", "pymnt"))
        ]
        temporal = {
            "issue_d_present": True,
            "documented_meaning": "Month and year in which the loan was approved (Zenodo).",
            "available_at_or_before_lending_decision": (
                "AT_APPROVAL_NOT_SHOWN_TO_BE_BEFORE_DECISION"
            ),
            "available_at_or_before_lending_decision_detail": (
                "Documentation defines issue_d as the approval month/year. That is the "
                "decision/origination stamp, not a pre-decision application timestamp, "
                "and not a post-decision servicing date. Flagged for methodology review "
                "if used as a model feature."
            ),
            "dtype_in_raw_file": str(df["issue_d"].dtype),
            "parsed_as": "pandas datetime using format %b-%Y, with a secondary infer parse for leftovers",
            "unique_raw_values": int(df["issue_d"].nunique(dropna=True)),
            "unique_parsed_months": int(parsed_ok.dt.to_period("M").nunique()) if not parsed_ok.empty else 0,
            "minimum_date": parsed_ok.min().strftime("%Y-%m-%d") if not parsed_ok.empty else None,
            "maximum_date": parsed_ok.max().strftime("%Y-%m-%d") if not parsed_ok.empty else None,
            "missing_count": int(df["issue_d"].isna().sum()),
            "missing_percentage": round(100.0 * float(df["issue_d"].isna().mean()), 6),
            "malformed_unparseable_count": malformed,
            "non_null_raw_count": non_null_raw,
            "other_date_like_column_names": other_date_like,
            "split_cutoffs_defined": False,
            "note": "Train/validation/test cutoffs are not defined in Stage 2.",
        }
        temporal_verified = malformed == 0 and non_null_raw == n_rows and not parsed_ok.empty
        write_csv_rows(RESULTS_TABLES / "lendingclub_date_distribution.csv", date_distribution)

    write_json(RESULTS_METRICS / "lendingclub_temporal_audit.json", temporal)

    leakage_rows = lendingclub_leakage_rows(columns)
    write_csv_rows(
        DOCS_DIR / "lendingclub_leakage_audit.csv",
        leakage_rows,
        ["column", "classification", "reason", "evidence_source", "confidence", "action_recommendation"],
    )

    purpose_rows = purpose_audit_rows(df)
    write_csv_rows(RESULTS_TABLES / "lendingclub_purpose_audit.csv", purpose_rows)

    privacy = privacy_rows(columns)
    write_csv_rows(DOCS_DIR / "lendingclub_privacy_audit.csv", privacy)

    missing_rows = missingness_rows(df)
    write_csv_rows(RESULTS_TABLES / "lendingclub_missingness.csv", missing_rows)

    findings = integrity_findings(df, parsed_issue)
    write_csv_rows(RESULTS_TABLES / "lendingclub_integrity_findings.csv", findings)

    numeric_rows = numeric_profile(df, exclude=set())
    write_csv_rows(RESULTS_TABLES / "lendingclub_numeric_profile.csv", numeric_rows)

    categorical_columns = [
        c
        for c in columns
        if c in {"emp_length", "purpose", "home_ownership_n", "addr_state", "zip_code", "issue_d", "experience_c", "title", "desc"}
        or (not pd.api.types.is_numeric_dtype(df[c]) and c not in {"id", "Default"})
    ]
    categorical_rows = categorical_profile(df, categorical_columns)
    write_csv_rows(RESULTS_TABLES / "lendingclub_categorical_profile.csv", categorical_rows)

    write_json(RESULTS_METRICS / "lendingclub_dimensions.json", dimensions)

    schema_md = [
        "# LendingClub Schema Report",
        "",
        "Source: Zenodo 10.5281/zenodo.11295916, file `LC_loans_granting_model_dataset.csv`.",
        "Loaded without dtype coercion beyond pandas CSV inference. No transformations were applied.",
        "",
        f"- Rows: {n_rows}",
        f"- Columns: {n_cols}",
        f"- Duplicate column names: {duplicate_column_names or 'none'}",
        f"- Duplicate rows: {duplicate_rows}",
        f"- Duplicate loan identifiers (`id`): {duplicate_ids}",
        f"- Unique `id` values: {unique_ids}",
        f"- Schema matches Zenodo documented variable list: {dimensions['schema_matches_zenodo_variable_list']}",
        "",
        "## Exact column names",
        "",
        md_table(["position", "column", "dtype"], [[i, c, str(df[c].dtype)] for i, c in enumerate(columns)]),
        "",
        "## Documented vs observed schema",
        "",
        f"- Documented columns missing from file: {dimensions['documented_columns_missing_from_file'] or 'none'}",
        f"- File columns missing from documentation: {dimensions['columns_missing_from_documentation'] or 'none'}",
        "",
        "Full per-column null/unique/sample profile: `results/tables/lendingclub_column_profile.csv`.",
        "Free-text and identifier sample values are redacted in that profile.",
        "",
    ]
    write_text(DOCS_DIR / "lendingclub_schema_report.md", "\n".join(schema_md))

    leakage_md = [
        "# LendingClub Leakage Audit",
        "",
        "Classifications use the Zenodo granting-model documentation for this release.",
        "Features were not dropped. Timing was not guessed when it could not be established.",
        "",
        md_table(
            ["column", "classification", "confidence", "action_recommendation"],
            [[r["column"], r["classification"], r["confidence"], r["action_recommendation"]] for r in leakage_rows],
        ),
        "",
        "## Notes requiring review",
        "",
        "- `issue_d` is an approval/origination month, not a demonstrated pre-decision application date.",
        "- `experience_c` construction uses a current-obligation credit date whose application-time status is TIMING_UNVERIFIED.",
        "- `dti_n` is documented as application-time but the phrase \"Monthly information\" is recorded as a wording ambiguity.",
        "- No official separate LendingClub parent data dictionary was retrieved in this stage; evidence is the Zenodo release description.",
        "",
        "Full reasons: `docs/lendingclub_leakage_audit.csv`.",
        "",
    ]
    write_text(DOCS_DIR / "lendingclub_leakage_audit.md", "\n".join(leakage_md))

    purpose_md = [
        "# LendingClub Purpose / Application-Field Audit",
        "",
        "No Shariah rules were created. This audit only records whether purpose-related fields exist and whether documentation places them at application time.",
        "",
        md_table(
            ["column", "availability", "missingness_pct", "unique_count", "application_time_status"],
            [
                [r["column"], r["availability"], r["missingness"], r["unique_count"], r["application_time_status"]]
                for r in purpose_rows
                if not str(r["column"]).startswith("_")
            ],
        ),
        "",
        "`purpose` is a coarse category. `title` and `desc` are free text; raw examples are not published.",
        "Details: `results/tables/lendingclub_purpose_audit.csv`.",
        "",
    ]
    write_text(DOCS_DIR / "lendingclub_purpose_audit.md", "\n".join(purpose_md))

    integrity_md = [
        "# LendingClub Integrity Audit",
        "",
        "Outliers were not deleted. No rows were dropped.",
        "",
        md_table(
            ["check", "n_affected", "pct_affected", "severity", "note"],
            [[f["check"], f["n_affected"], f["pct_affected"], f["severity"], f["note"]] for f in findings],
        ),
        "",
        "Machine-readable copy: `results/tables/lendingclub_integrity_findings.csv`.",
        "",
    ]
    write_text(DOCS_DIR / "lendingclub_integrity_audit.md", "\n".join(integrity_md))

    return {
        "dimensions": dimensions,
        "target_audit": target_audit,
        "target_verified": target_verified,
        "temporal": temporal,
        "temporal_verified": temporal_verified,
        "leakage_rows": leakage_rows,
        "purpose_rows": purpose_rows,
        "privacy_rows": privacy,
        "missing_rows": missing_rows,
        "findings": findings,
        "numeric_rows": numeric_rows,
        "categorical_rows": categorical_rows,
        "date_distribution": date_distribution if "issue_d" in df.columns else [],
        "purpose_verified": "purpose" in df.columns,
    }


def audit_uci(df: pd.DataFrame, load_meta: dict[str, Any]) -> dict[str, Any]:
    n_rows, n_cols = df.shape
    columns = list(df.columns)
    target_candidates = [c for c in columns if "default" in c.lower() or c == "Y"]
    if "default payment next month" in columns:
        target_name = "default payment next month"
        target_status = "VERIFIED_FROM_UCI_SPREADSHEET_AND_DOCUMENTATION"
        target_verified = True
    elif len(target_candidates) == 1:
        target_name = target_candidates[0]
        target_status = "TARGET_NAME_INFERRED_FROM_SINGLE_MATCH"
        target_verified = False
    else:
        target_name = None
        target_status = "TARGET_DEFINITION_UNVERIFIED"
        target_verified = False

    target_block: dict[str, Any] = {
        "target_column": target_name,
        "target_definition_status": target_status,
        "target_definition_from_documentation": (
            "UCI Additional Variable Information: binary default payment (Yes = 1, No = 0) "
            "as the response variable. Spreadsheet header names this column "
            "'default payment next month'."
        ),
    }
    if target_name is not None:
        series = pd.to_numeric(df[target_name], errors="coerce")
        counts = series.value_counts(dropna=False).sort_index()
        target_block["unique_values"] = [json_safe(v) for v in series.dropna().unique().tolist()]
        target_block["value_counts"] = [
            {
                "value": "NA" if pd.isna(v) else json_safe(v),
                "count": int(c),
                "percentage": round(100.0 * c / n_rows, 6),
            }
            for v, c in counts.items()
        ]
        target_block["missing_target_rows"] = int(series.isna().sum())
        target_block["prevalence_eq_1"] = float((series == 1).mean()) if n_rows else None
        target_block["prevalence_eq_1_percentage"] = (
            round(100.0 * float((series == 1).mean()), 6) if n_rows else None
        )

    documented_conflicts: list[dict[str, Any]] = []
    if "EDUCATION" in df.columns:
        edu = pd.to_numeric(df["EDUCATION"], errors="coerce")
        documented_edu = {1, 2, 3, 4}
        extra_edu = sorted(set(edu.dropna().astype(int)) - documented_edu)
        documented_conflicts.append(
            {
                "field": "EDUCATION",
                "documentation": "UCI Additional Variable Information: 1=graduate school; 2=university; 3=high school; 4=others.",
                "undocumented_values_observed": extra_edu,
                "counts": {str(k): int((edu == k).sum()) for k in extra_edu},
                "status": "SOURCE_CONTENTS_CONFLICT" if extra_edu else "ALIGNED",
            }
        )
    if "MARRIAGE" in df.columns:
        mar = pd.to_numeric(df["MARRIAGE"], errors="coerce")
        documented_mar = {1, 2, 3}
        extra_mar = sorted(set(mar.dropna().astype(int)) - documented_mar)
        documented_conflicts.append(
            {
                "field": "MARRIAGE",
                "documentation": "UCI Additional Variable Information: 1=married; 2=single; 3=others.",
                "undocumented_values_observed": extra_mar,
                "counts": {str(k): int((mar == k).sum()) for k in extra_mar},
                "status": "SOURCE_CONTENTS_CONFLICT" if extra_mar else "ALIGNED",
            }
        )
    pay_documented = set([-1]) | set(range(1, 10))
    pay_cols = [
        c
        for c in columns
        if c.startswith("PAY_") and not c.startswith("PAY_AMT")
    ]
    for column in pay_cols:
        pay = pd.to_numeric(df[column], errors="coerce")
        extra_pay = sorted(set(pay.dropna().astype(int)) - pay_documented)
        documented_conflicts.append(
            {
                "field": column,
                "documentation": (
                    "UCI Additional Variable Information: -1=pay duly; 1=delay one month; "
                    "...; 8=delay eight months; 9=delay nine months and above. Values 0 and -2 are not defined there."
                ),
                "undocumented_values_observed": extra_pay,
                "counts": {str(k): int((pay == k).sum()) for k in extra_pay},
                "status": "SOURCE_CONTENTS_CONFLICT" if extra_pay else "ALIGNED",
            }
        )
    negative_bills = {}
    for column in [c for c in columns if str(c).startswith("BILL_AMT")]:
        bill = pd.to_numeric(df[column], errors="coerce")
        negative_bills[column] = int((bill < 0).sum())

    date_like = [
        c
        for c in columns
        if any(
            tok in c.lower().replace(" ", "_")
            for tok in ("_date", "date_", "timestamp", "issue_d", "origination")
        )
        or c.lower() in {"date", "time", "issue_d"}
    ]
    purpose_like = [
        c
        for c in columns
        if c.lower() in {"purpose", "title", "desc"}
        or any(tok in c.lower() for tok in ("purpose", "loan_title", "loan_desc"))
    ]

    column_profile = profile_columns(df, redact=True)
    write_csv_rows(RESULTS_TABLES / "uci_column_profile.csv", column_profile)
    missing_rows = missingness_rows(df)
    numeric_rows = numeric_profile(df, exclude={"ID"} if "ID" in df.columns else set())

    uci_audit = {
        "n_rows": int(n_rows),
        "n_columns": int(n_cols),
        "column_names": columns,
        "x_code_aliases": load_meta.get("alias_map"),
        "uci_stated_instances": 30000,
        "uci_stated_features": 23,
        "observed_minus_id_and_target_feature_count": int(n_cols - (1 if "ID" in columns else 0) - (1 if target_name else 0)),
        "duplicate_rows": int(df.duplicated().sum()),
        "duplicate_ids": int(df["ID"].duplicated().sum()) if "ID" in df.columns else None,
        "target": target_block,
        "missingness": missing_rows,
        "has_calendar_timestamp_fields": bool(date_like),
        "date_like_column_names": date_like,
        "temporal_field_availability": (
            "NO_CALENDAR_TIMESTAMPS. Payment/bill columns encode a fixed April-September 2005 "
            "window from the UCI documentation, not per-row origination timestamps."
        ),
        "financing_purpose_fields": purpose_like or [],
        "financing_purpose_availability": "ABSENT" if not purpose_like else "PRESENT",
        "identifier_fields": ["ID"] if "ID" in columns else [],
        "documented_no_missing_values_on_uci_page": True,
        "observed_any_missing": bool(df.isna().any().any()),
        "documentation_vs_contents_conflicts": documented_conflicts,
        "negative_bill_amount_counts": negative_bills,
        "negative_bill_amounts_note": (
            "Negative bill statement amounts are present. UCI documentation does not define "
            "their meaning. They were not deleted."
        ),
        "load_meta": {k: v for k, v in load_meta.items() if k != "header_row_x_codes"},
        "semantic_differences_from_lendingclub": [
            "UCI is revolving credit-card default in Taiwan, not US P2P personal-loan origination.",
            "UCI has no financing-purpose field.",
            "UCI has no issue/application timestamp.",
            "UCI includes demographics (SEX, EDUCATION, MARRIAGE, AGE) absent from this LendingClub release.",
            "UCI includes 6-month bill and payment history; this LendingClub granting release does not.",
            "UCI target is default payment next month after the 2005 observation window, not terminal Fully Paid vs charged-off on a closed installment loan.",
        ],
    }
    write_json(RESULTS_METRICS / "uci_dataset_audit.json", uci_audit)

    schema_md = [
        "# UCI Default of Credit Card Clients Schema Report",
        "",
        f"Official URL: {UCI_URL}",
        f"DOI: {UCI_DOI}",
        "Raw artifact: `data/raw/default+of+credit+card+clients.zip` (not modified).",
        "The `.xls` member was converted via Excel COM to a temporary CSV for reading only.",
        "",
        f"- Rows: {n_rows}",
        f"- Columns: {n_cols}",
        f"- UCI page stated instances: 30000",
        f"- UCI page stated features: 23",
        f"- Target column: {target_name}",
        f"- Target definition status: {target_status}",
        "",
        "## Columns",
        "",
        md_table(
            ["column", "x_code", "dtype"],
            [[c, load_meta.get("alias_map", {}).get(c, ""), str(df[c].dtype)] for c in columns],
        ),
        "",
        "## Target",
        "",
        json.dumps(json_safe(target_block), indent=2),
        "",
        "## Temporal fields",
        "",
        uci_audit["temporal_field_availability"],
        "",
        "## Financing purpose",
        "",
        uci_audit["financing_purpose_availability"],
        "",
        "## Documentation vs contents conflicts",
        "",
        "These discrepancies were not silently recoded.",
        "",
        json.dumps(json_safe(documented_conflicts), indent=2),
        "",
        f"Negative BILL_AMT* counts: {negative_bills}",
        "",
        "Column profile: `results/tables/uci_column_profile.csv`.",
        "",
    ]
    write_text(DOCS_DIR / "uci_schema_report.md", "\n".join(schema_md))

    return {
        "uci_audit": uci_audit,
        "target_verified": target_verified,
        "n_rows": n_rows,
        "n_cols": n_cols,
        "target_name": target_name,
        "missing_rows": missing_rows,
        "numeric_rows": numeric_rows,
        "column_profile": column_profile,
        "df_columns": columns,
    }


def write_comparability(lc: dict[str, Any], uci: dict[str, Any]) -> None:
    lc_cols = set(lc["dimensions"]["column_names"])
    uci_cols = set(uci["df_columns"])
    rows = [
        {
            "Concept": "target",
            "LendingClub variable(s)": "Default",
            "UCI variable(s)": uci["target_name"],
            "Comparable?": "No",
            "Reason": (
                "Both are binary default labels, but they are not equivalent outcomes: "
                "LC is terminal resolution of an originated US P2P installment loan "
                "(fully paid vs defaulted/charged-off per depositor); UCI is whether a "
                "Taiwan credit-card client defaulted in the next month after a 2005 window."
            ),
        },
        {
            "Concept": "credit history",
            "LendingClub variable(s)": "fico_n; experience_c (timing unverified)",
            "UCI variable(s)": "PAY_0, PAY_2, PAY_3, PAY_4, PAY_5, PAY_6",
            "Comparable?": "No",
            "Reason": "FICO/repeat-borrower flag vs six months of repayment-status codes. Not the same construct.",
        },
        {
            "Concept": "income",
            "LendingClub variable(s)": "revenue" if "revenue" in lc_cols else "ABSENT",
            "UCI variable(s)": "ABSENT",
            "Comparable?": "No",
            "Reason": "UCI has no income field.",
        },
        {
            "Concept": "debt/obligations",
            "LendingClub variable(s)": "dti_n; loan_amnt",
            "UCI variable(s)": "LIMIT_BAL; BILL_AMT1-BILL_AMT6",
            "Comparable?": "No",
            "Reason": "Requested installment amount and DTI vs revolving limit and monthly bill amounts.",
        },
        {
            "Concept": "age/demographics",
            "LendingClub variable(s)": "ABSENT in this release (geography only)",
            "UCI variable(s)": "AGE; SEX; EDUCATION; MARRIAGE",
            "Comparable?": "No",
            "Reason": "This LC granting release has no age/sex/education/marriage fields.",
        },
        {
            "Concept": "credit utilization",
            "LendingClub variable(s)": "ABSENT",
            "UCI variable(s)": "BILL_AMT* with LIMIT_BAL (constructable; not a native field)",
            "Comparable?": "No",
            "Reason": "No LC utilization field in this release; UCI utilization would be derived and was not created here.",
        },
        {
            "Concept": "payment history",
            "LendingClub variable(s)": "ABSENT as monthly payments",
            "UCI variable(s)": "PAY_AMT1-PAY_AMT6 and PAY_0, PAY_2-PAY_6",
            "Comparable?": "No",
            "Reason": "UCI is a 6-month revolving payment history; this LC release excludes servicing fields by design.",
        },
        {
            "Concept": "financing purpose",
            "LendingClub variable(s)": "purpose; title; desc",
            "UCI variable(s)": "ABSENT",
            "Comparable?": "No",
            "Reason": "UCI has no loan-purpose or borrower-description fields.",
        },
        {
            "Concept": "time",
            "LendingClub variable(s)": "issue_d",
            "UCI variable(s)": "No per-row timestamp; April-September 2005 encoded as column groups",
            "Comparable?": "No",
            "Reason": "LC has a loan-level approval month. UCI is a single study window, not a panel of origination dates.",
        },
        {
            "Concept": "geographic information",
            "LendingClub variable(s)": "addr_state; zip_code",
            "UCI variable(s)": "ABSENT",
            "Comparable?": "No",
            "Reason": "UCI has no geography fields. Populations are US vs Taiwan.",
        },
        {
            "Concept": "application-time availability",
            "LendingClub variable(s)": "Depositor-selected granting/application subset (with issue_d and experience_c caveats)",
            "UCI variable(s)": "Snapshot of existing revolving-account behaviour plus demographics",
            "Comparable?": "No",
            "Reason": (
                "LC features are (claimed) origination-application attributes for issued P2P loans. "
                "UCI features are performance of already-issued credit cards. Not the same decision point."
            ),
        },
    ]
    lookalikes = [
        "Default vs default payment next month look like generic 'default' labels but differ in product, horizon, and population.",
        "loan_amnt vs LIMIT_BAL are both size-of-credit numbers but request vs revolving limit.",
        "fico_n vs PAY_* are both 'credit history' only at a slogan level.",
        "revenue vs AGE/SEX are both applicant descriptors but not substitutes.",
    ]
    md = [
        "# Cross-Dataset Comparability",
        "",
        "The datasets were not merged.",
        "No applicant-level linkage key exists between US LendingClub loans and Taiwan credit-card clients.",
        "",
        md_table(
            ["Concept", "LendingClub variable(s)", "UCI variable(s)", "Comparable?", "Reason"],
            [
                [r["Concept"], r["LendingClub variable(s)"], r["UCI variable(s)"], r["Comparable?"], r["Reason"]]
                for r in rows
            ],
        ),
        "",
        "## Semantically similar but not equivalent",
        "",
    ]
    md.extend(f"- {item}" for item in lookalikes)
    md.extend(
        [
            "",
            "## Conclusion",
            "",
            "UCI supports `GENERALIZATION_OF_METHOD` (can the same evidence-separated audit/decision pipeline be applied to a second tabular credit-default dataset?).",
            "",
            "UCI does **not** support `DIRECT_DOMAIN_TRANSFER`. Nothing in the schemas, populations, products, timestamps, or purpose fields justifies treating UCI as a LendingClub domain replica.",
            "",
        ]
    )
    write_text(DOCS_DIR / "dataset_comparability.md", "\n".join(md))
    _ = uci_cols  # recorded via uci report; unused here on purpose


def write_dataset_card(lc_meta: dict[str, Any], uci_meta: dict[str, Any], lc: dict[str, Any], uci: dict[str, Any]) -> None:
    lc_target = lc["target_audit"]
    uci_target = uci["uci_audit"]["target"]
    lc_missing = lc["missing_rows"]
    high_lc = [r["column"] for r in lc_missing if r["missingness_class"] == "HIGH_MISSINGNESS"]
    md = f"""# Preliminary Dataset Card

This card does not describe either dataset as Islamic, Shariah-compliant, or representative of Islamic financing markets.

## LendingClub granting-model dataset

- Dataset name: Lending Club loan dataset for granting models
- Source: Zenodo
- DOI/URL: {ZENODO_DOI} / {ZENODO_URL}
- License: {lc_meta.get("license")}
- Dataset role: PRIMARY_CREDIT_RISK_DATASET
- Target: `{lc_target.get("target_column")}` (documented 0=fully paid, 1=defaulted; original loan_status mapping has a documentation conflict)
- Row count: {lc["dimensions"]["n_rows"]}
- Feature count (columns including target and identifiers): {lc["dimensions"]["n_columns"]}
- Temporal availability: `issue_d` present; documented as approval month/year; range {lc["temporal"].get("minimum_date")} to {lc["temporal"].get("maximum_date")}
- Missingness summary: high-missingness columns = {high_lc or "none"}; full table in `results/tables/lendingclub_missingness.csv`
- Known limitations: issued-and-resolved loans only (no rejected applications); transitory statuses excluded; depositor already filtered and cleaned; US P2P market 2007-2018 origin, not Islamic finance
- Privacy considerations: loan `id` is a direct identifier; `zip_code`/`addr_state`/`revenue` are quasi-identifiers; `title`/`desc` are free text (raw text not published here)
- Leakage concerns: `issue_d` as a feature; `experience_c` timing unverified; target is post-decision by definition
- Intended use: primary credit-risk architecture/evaluation dataset for this research project
- Prohibited/unsupported claims: not a Shariah-compliance dataset; not a full applicant funnel; not certified; not to be described as real-time underwriting data from an Islamic bank

## UCI Default of Credit Card Clients

- Dataset name: Default of Credit Card Clients
- Source: UCI Machine Learning Repository dataset 350
- DOI/URL: {UCI_DOI} / {UCI_URL}
- License: {uci_meta.get("license")}
- Dataset role: SECONDARY_GENERALIZATION_DATASET
- Target: `{uci_target.get("target_column")}` (Yes=1 / No=0 default payment next month)
- Row count: {uci["n_rows"]}
- Feature count: UCI states 23 features; observed columns including ID and target = {uci["n_cols"]}
- Temporal availability: no per-row timestamps; fixed 2005 payment window in column groups
- Missingness summary: UCI page states no missing values; observed any missing = {uci["uci_audit"]["observed_any_missing"]}
- Known limitations: Taiwan credit-card clients; no financing purpose; not P2P origination; single-period study
- Privacy considerations: `ID` identifier; demographics present (SEX, EDUCATION, MARRIAGE, AGE)
- Leakage concerns: bill/payment history is contemporaneous account performance, not origination-application data for a new loan grant
- Intended use: methodological replication / pipeline generalization, not domain transfer
- Prohibited/unsupported claims: not Islamic finance; not equivalent to LendingClub; not a basis for combining applicant records
"""
    write_text(DOCS_DIR / "dataset_card.md", md)


def write_dataset_decision(lc: dict[str, Any], uci: dict[str, Any]) -> None:
    md = f"""# Dataset Decision Memo

Stage 2 audit memo. Roles were not changed. No applicant-level merge was performed.

## A. Why is LendingClub the primary dataset?

The verified Zenodo release is a granting-model extract of issued LendingClub loans with a public credit-performance outcome, application-oriented features selected by the depositor, `issue_d`, and `purpose`. Observed size is {lc["dimensions"]["n_rows"]} rows and {lc["dimensions"]["n_columns"]} columns. That combination matches the assigned role `PRIMARY_CREDIT_RISK_DATASET` for an evidence-separated decision architecture study that needs a financing-purpose field and a temporal stamp. This does not make the data Islamic or Shariah-certified.

## B. Why is UCI used only as a methodological replication/generalization dataset?

UCI Default of Credit Card Clients is a 30,000-row Taiwan credit-card default table with demographics and six-month bill/payment history, no financing purpose, and no origination timestamp. It can test whether the same audit/evaluation *method* runs on a second credit-default table. It cannot stand in for US P2P origination or for Shariah-purpose governance.

## C. What research questions can each dataset legitimately answer?

- LendingClub (this release): questions about credit-risk prediction on *originated and resolved* US P2P loans using the depositor's application-time subset; questions about temporal ordering via `issue_d`; questions about whether a purpose field exists for a later decision-support layer.
- UCI: questions about whether the same pipeline/metrics/calibration/explainability *procedure* can be repeated on a different tabular default dataset.

## D. What questions can they NOT answer?

- Neither dataset answers questions about Islamic financing markets, Shariah compliance, or certified religious permissibility.
- LendingClub cannot answer reject-inference / full-application-funnel questions: rejected applicants are absent.
- LendingClub cannot answer questions requiring servicing fields the depositor removed (interest rate, grade, post-origination performance series).
- UCI cannot answer purpose-conditioned or origination-time P2P underwriting questions.
- Neither dataset provides entity-level linkage to the other.

## E. Can the two datasets be combined?

**Do not combine them into one applicant-level dataset.**

No legitimate applicant-level linkage key was found. Populations, products, geographies, time bases, and labels differ. If a later methodological proposal argues for a non-entity combination (for example, separate-task evaluation of the same code path), that is a methodology-review item. It was not implemented.

Observed row counts: LendingClub {lc["dimensions"]["n_rows"]}; UCI {uci["n_rows"]}.
"""
    write_text(DOCS_DIR / "dataset_decision.md", md)


def write_stage2_report(
    lc_file: dict[str, Any],
    uci_file: dict[str, Any],
    lc: dict[str, Any],
    uci: dict[str, Any],
    run_meta: dict[str, Any],
    open_issues: list[str],
    review_items: list[str],
    summary: dict[str, Any],
) -> None:
    lc_target = lc["target_audit"]
    high_miss = [r for r in lc["missing_rows"] if r["missingness_class"] == "HIGH_MISSINGNESS"]
    leakage_special = [
        r
        for r in lc["leakage_rows"]
        if r["classification"] in {"POTENTIAL_LEAKAGE", "POST_DECISION", "UNKNOWN", "TARGET"}
    ]
    md = f"""# Stage 2 Data Acquisition & Forensic Audit

## 1. Executive Summary

Stage 2 acquired the specified Zenodo LendingClub granting-model release and the official UCI Default of Credit Card Clients package, stored them as immutable raw files, and produced schema, target, temporal, leakage, purpose, privacy, missingness, integrity, distribution, and comparability audits. No model was trained. No split was created. No Shariah rule engine was built. No synthetic applicants were created.

- LendingClub rows x columns: {lc["dimensions"]["n_rows"]} x {lc["dimensions"]["n_columns"]}
- UCI rows x columns: {uci["n_rows"]} x {uci["n_cols"]}
- Stage status: {summary["status"]}

## 2. Data Sources and Licensing

- LendingClub: DOI {ZENODO_DOI}, {ZENODO_RECORD_URL}. License: {lc_file.get("license")}. Version: {lc_file.get("version_if_available")}. File: `{lc_file.get("filename")}` ({lc_file.get("file_size_bytes")} bytes). SHA-256: `{lc_file.get("sha256")}`.
- UCI: {UCI_URL}, DOI {UCI_DOI}. License: {uci_file.get("license")}. File: `{uci_file.get("filename")}` ({uci_file.get("file_size_bytes")} bytes). SHA-256: `{uci_file.get("sha256")}`.
- Manifests: `docs/raw_data_manifest.csv`, `docs/raw_data_manifest.json`.

## 3. Dataset Dimensions

LendingClub: {lc["dimensions"]["n_rows"]} rows, {lc["dimensions"]["n_columns"]} columns. Duplicate rows: {lc["dimensions"]["duplicate_rows"]}. Duplicate IDs: {lc["dimensions"]["duplicate_applicant_or_loan_identifiers"]}. Schema match to Zenodo variable list: {lc["dimensions"]["schema_matches_zenodo_variable_list"]}.

UCI: {uci["n_rows"]} rows, {uci["n_cols"]} columns (UCI page: 30000 instances, 23 features). Spreadsheet has two header rows (X-codes and names).

## 4. Target Definitions

LendingClub target column: `{lc_target.get("target_column")}`. Prevalence Default=1: {lc_target.get("prevalence_Default_eq_1_percentage")}%. Status: {lc_target.get("target_definition_status")}.

{LC_TARGET_DOC_CONFLICT}

UCI target column: `{uci["target_name"]}`. Prevalence =1: {uci["uci_audit"]["target"].get("prevalence_eq_1_percentage")}%. Status: {uci["uci_audit"]["target"].get("target_definition_status")}.

## 5. Temporal Audit

LendingClub `issue_d` dtype: {lc["temporal"].get("dtype_in_raw_file")}. Unique parsed months: {lc["temporal"].get("unique_parsed_months")}. Range: {lc["temporal"].get("minimum_date")} to {lc["temporal"].get("maximum_date")}. Missing: {lc["temporal"].get("missing_percentage")}%. Malformed: {lc["temporal"].get("malformed_unparseable_count")}. Availability: {lc["temporal"].get("available_at_or_before_lending_decision")}. Split cutoffs were not defined.

UCI: {uci["uci_audit"]["temporal_field_availability"]}

## 6. Leakage Audit

Non-SAFE classifications:

{md_table(
        ["column", "classification", "confidence"],
        [[r["column"], r["classification"], r["confidence"]] for r in leakage_special],
    )}

Full audit: `docs/lendingclub_leakage_audit.csv` and `docs/lendingclub_leakage_audit.md`. No feature was dropped.

## 7. Purpose/Application-Field Audit

`purpose`, `title`, and `desc` are present. `purpose` is documented as the loan-request purpose category. `title`/`desc` are borrower free text (raw values not published). No Shariah rules were written. Details: `docs/lendingclub_purpose_audit.md`.

UCI financing purpose: {uci["uci_audit"]["financing_purpose_availability"]}.

## 8. Privacy/Identifier Audit

LendingClub: `id` DIRECT_IDENTIFIER; `addr_state`/`zip_code`/`revenue` QUASI_IDENTIFIER; `title`/`desc` FREE_TEXT. Employer name, email, phone, and street address columns were not present in this release. Raw PII/free text is not printed in reports. Table: `docs/lendingclub_privacy_audit.csv`.

UCI: `ID` identifier; demographic attributes present.

## 9. Missingness

Missingness classes are diagnostic only (0 = none; <{MISSINGNESS_LOW_MAX_PCT}% = low; <{MISSINGNESS_MODERATE_MAX_PCT}% = moderate; else high). No imputation was performed.

LendingClub high-missingness columns: {", ".join(r["column"] + f" ({r['missing_percentage']}%)" for r in high_miss) or "none"}.

UCI observed any missing: {uci["uci_audit"]["observed_any_missing"]}.

## 10. Integrity and Duplicate Findings

See `docs/lendingclub_integrity_audit.md`. Outliers were not deleted.

## 11. Distribution Findings

Numeric and categorical diagnostic profiles (no winsorizing, clipping, or scaling): `results/tables/lendingclub_numeric_profile.csv`, `results/tables/lendingclub_categorical_profile.csv`. Free-text top categories are redacted.

## 12. UCI Audit

See `docs/uci_schema_report.md` and `results/metrics/uci_dataset_audit.json`. Loader: Excel COM conversion of the official `.xls` member from the official zip, without modifying the zip.

UCI Additional Variable Information does not fully match observed codes (EDUCATION 0/5/6, MARRIAGE 0, PAY_* values 0 and -2). Negative BILL_AMT* values are present. None of these were recoded or deleted.

## 13. Cross-Dataset Comparability

See `docs/dataset_comparability.md`. Conclusion: `GENERALIZATION_OF_METHOD`, not `DIRECT_DOMAIN_TRANSFER`. Datasets were not merged.

## 14. Dataset Limitations

- LendingClub observations are originated loans that reached a terminal status in the depositor's filter, not the full application funnel.
- Depositor already cleaned/filtered the parent Kaggle extract; this is not the raw LendingClub tape.
- US P2P 2007–2018; not an Islamic-finance sample.
- UCI is a 2005 Taiwan credit-card snapshot without purpose or origination dates.

## 15. Unsupported Claims

- Neither dataset is Islamic, Shariah-compliant, or a Shariah certification corpus.
- UCI is not a LendingClub proxy.
- Presence of `purpose` does not authorize a Shariah engine or certified rulings.
- `issue_d` is not shown to be a pre-decision application timestamp.
- No experimental performance numbers exist yet.

## 16. Stage-2 Decisions

- Raw files in `data/raw/` are immutable.
- Do not combine the datasets at applicant level.
- Do not drop columns from raw data.
- Do not impute, encode, or split yet.
- Do not train models.
- Primary/secondary roles remain as specified, with the caveats in this report.

## 17. Items Requiring Research-Owner Review

{os.linesep.join(f"- {item}" for item in review_items) if review_items else "- None."}

Open issues:

{os.linesep.join(f"- {item}" for item in open_issues) if open_issues else "- None."}

## 18. Reproducibility Information

- run_id: {run_meta.get("run_id")}
- timestamp: {run_meta.get("timestamp")}
- git_commit: {run_meta.get("git_commit")}
- python_version: {run_meta.get("python_version")}
- operating_system: {run_meta.get("operating_system")}
- script_version: {run_meta.get("script_version")}
- dataset hashes: {json.dumps(run_meta.get("dataset_hashes"), indent=2)}
- Reproduce: `python src/data/audit_datasets.py`
"""
    write_text(DOCS_DIR / "STAGE_2_DATA_AUDIT_REPORT.md", md)


def build_manifest(entries: list[dict[str, Any]]) -> None:
    fieldnames = [
        "dataset_name",
        "source",
        "doi_or_official_url",
        "download_date",
        "filename",
        "file_size_bytes",
        "sha256",
        "license",
        "version_if_available",
    ]
    write_csv_rows(DOCS_DIR / "raw_data_manifest.csv", entries, fieldnames)
    write_json(DOCS_DIR / "raw_data_manifest.json", entries)


def file_download_date(path: Path) -> str:
    ts = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc).replace(microsecond=0)
    return ts.isoformat()


def main() -> int:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_TABLES.mkdir(parents=True, exist_ok=True)
    RESULTS_METRICS.mkdir(parents=True, exist_ok=True)
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    lc_path = RAW_DIR / EXPECTED_LC_FILENAME
    uci_path = RAW_DIR / EXPECTED_UCI_ZIP_FILENAME
    open_issues: list[str] = []
    review_items: list[str] = []
    datasets_audited: list[str] = []

    if not lc_path.exists():
        write_json(
            RESULTS_METRICS / "stage2_summary.json",
            {
                "stage": "2",
                "status": "BLOCKED",
                "datasets_audited": [],
                "raw_hashes_verified": False,
                "target_verified": False,
                "temporal_field_verified": False,
                "leakage_audit_complete": False,
                "purpose_field_verified": False,
                "license_verified": False,
                "modeling_started": False,
                "test_set_created": False,
                "open_issues": ["LendingClub raw file missing; download failed or was not performed. No silent Kaggle substitute."],
                "requires_research_owner_review": ["Acquire Zenodo 10.5281/zenodo.11295916 before Stage 3."],
            },
        )
        print("BLOCKED: LendingClub raw file is missing.", file=sys.stderr)
        return 2
    if not uci_path.exists():
        write_json(
            RESULTS_METRICS / "stage2_summary.json",
            {
                "stage": "2",
                "status": "BLOCKED",
                "datasets_audited": [],
                "raw_hashes_verified": False,
                "target_verified": False,
                "temporal_field_verified": False,
                "leakage_audit_complete": False,
                "purpose_field_verified": False,
                "license_verified": False,
                "modeling_started": False,
                "test_set_created": False,
                "open_issues": ["UCI raw zip missing; no silent mirror substitute."],
                "requires_research_owner_review": ["Acquire official UCI dataset 350 zip before Stage 3."],
            },
        )
        print("BLOCKED: UCI raw zip is missing.", file=sys.stderr)
        return 2

    lc_hash_before = sha256_file(lc_path)
    uci_hash_before = sha256_file(uci_path)
    lc_md5 = md5_file(lc_path)
    lc_size = lc_path.stat().st_size
    uci_size = uci_path.stat().st_size

    zenodo = load_zenodo_record()
    lc_license = "LICENSE_UNVERIFIED"
    lc_version = None
    if zenodo and zenodo.get("metadata", {}).get("license", {}).get("id"):
        lc_license = str(zenodo["metadata"]["license"]["id"])
        lc_version = zenodo.get("metadata", {}).get("version")
    else:
        open_issues.append("LendingClub license could not be read from saved Zenodo API JSON.")

    if lc_size != EXPECTED_LC_SIZE:
        open_issues.append(
            f"LendingClub file size {lc_size} != Zenodo-listed size {EXPECTED_LC_SIZE}."
        )
    if lc_md5 != EXPECTED_LC_MD5:
        open_issues.append(
            f"LendingClub MD5 {lc_md5} != Zenodo-listed MD5 {EXPECTED_LC_MD5}."
        )

    uci_license_info = extract_license_from_uci_html(SOURCE_META_DIR / "uci_350_dataset_page.html")
    uci_license = uci_license_info["license"]
    if not uci_license_info["verified"]:
        open_issues.append("UCI license LICENSE_UNVERIFIED from captured HTML.")

    lc_entry = {
        "dataset_name": "Lending Club loan dataset for granting models",
        "source": ZENODO_RECORD_URL,
        "doi_or_official_url": f"https://doi.org/{ZENODO_DOI}",
        "download_date": file_download_date(lc_path),
        "filename": lc_path.name,
        "file_size_bytes": lc_size,
        "sha256": lc_hash_before,
        "license": lc_license,
        "version_if_available": lc_version,
        "md5": lc_md5,
        "role": "PRIMARY_CREDIT_RISK_DATASET",
    }
    uci_entry = {
        "dataset_name": "Default of Credit Card Clients",
        "source": UCI_URL,
        "doi_or_official_url": f"https://doi.org/{UCI_DOI}",
        "download_date": file_download_date(uci_path),
        "filename": uci_path.name,
        "file_size_bytes": uci_size,
        "sha256": uci_hash_before,
        "license": uci_license,
        "version_if_available": None,
        "role": "SECONDARY_GENERALIZATION_DATASET",
    }
    build_manifest([lc_entry, uci_entry])

    lc_df = load_lendingclub(lc_path)
    lc_result = audit_lendingclub(lc_df)
    datasets_audited.append("lendingclub_zenodo_11295916")

    uci_df, uci_load_meta = load_uci_dataframe(uci_path)
    uci_result = audit_uci(uci_df, uci_load_meta)
    datasets_audited.append("uci_default_of_credit_card_clients_350")

    write_comparability(lc_result, uci_result)
    write_dataset_card(lc_entry, uci_entry, lc_result, uci_result)
    write_dataset_decision(lc_result, uci_result)

    review_items.extend(
        [
            "issue_d: approval month vs feature vs time-index only; do not set split cutoffs until reviewed.",
            "experience_c: TIMING_UNVERIFIED construction using current-obligation credit date.",
            "dti_n: depositor application-time claim vs 'Monthly information' wording.",
            "Target Default: documentation conflict between charged-off mapping and 'Fully Paid or Default' filter sentence.",
            "Selection bias: dataset contains originated and resolved loans only.",
            "UCI role remains GENERALIZATION_OF_METHOD, not DIRECT_DOMAIN_TRANSFER; do not merge.",
            "UCI EDUCATION/MARRIAGE/PAY_* codes include values not defined in UCI Additional Variable Information; do not recode without a protocol.",
            "purpose/title/desc may later feed decision-support; no Shariah certification is implied.",
        ]
    )
    if lc_result["target_audit"].get("target_definition_status") == "TARGET_DEFINITION_DOCUMENTATION_CONFLICT":
        open_issues.append("LendingClub target original loan_status mapping is not uniquely specified in Zenodo text.")
    if not lc_result["temporal_verified"]:
        open_issues.append("LendingClub issue_d temporal parse was incomplete or field was missing.")
    if lc_result["dimensions"]["n_rows"] != 1347681:
        open_issues.append(
            f"Observed LendingClub rows {lc_result['dimensions']['n_rows']} != Zenodo stated 1,347,681."
        )
    if uci_result["n_rows"] != 30000:
        open_issues.append(f"Observed UCI rows {uci_result['n_rows']} != UCI stated 30000.")
    uci_conflicts = [
        item["field"]
        for item in uci_result["uci_audit"].get("documentation_vs_contents_conflicts", [])
        if item.get("status") == "SOURCE_CONTENTS_CONFLICT"
    ]
    if uci_conflicts:
        open_issues.append(
            "UCI documentation vs contents conflict (not recoded) in: "
            + ", ".join(uci_conflicts)
            + "."
        )

    lc_hash_after = sha256_file(lc_path)
    uci_hash_after = sha256_file(uci_path)
    raw_unmodified = lc_hash_before == lc_hash_after and uci_hash_before == uci_hash_after
    if not raw_unmodified:
        open_issues.append("Raw file hash changed during audit; this must not happen.")

    hashes_verified = (
        raw_unmodified
        and lc_md5 == EXPECTED_LC_MD5
        and lc_size == EXPECTED_LC_SIZE
    )

    run_meta = {
        "run_id": str(uuid.uuid4()),
        "timestamp": utc_now_iso(),
        "git_commit": git_commit(REPO_ROOT),
        "python_version": sys.version.replace("\n", " "),
        "operating_system": f"{platform.system()} {platform.release()} ({platform.version()})",
        "dataset_files": [str(lc_path.relative_to(REPO_ROOT)), str(uci_path.relative_to(REPO_ROOT))],
        "dataset_hashes": {
            lc_path.name: lc_hash_after,
            uci_path.name: uci_hash_after,
        },
        "script_version": SCRIPT_VERSION,
        "raw_files_unmodified": raw_unmodified,
    }
    write_json(AUDIT_DIR / "data_audit_run.json", run_meta)

    license_verified = lc_license != "LICENSE_UNVERIFIED" and uci_license != "LICENSE_UNVERIFIED"
    leakage_complete = bool(lc_result["leakage_rows"]) and len(lc_result["leakage_rows"]) == lc_result["dimensions"]["n_columns"]
    status = "COMPLETE" if raw_unmodified else "BLOCKED"

    summary = {
        "stage": "2",
        "status": status,
        "datasets_audited": datasets_audited,
        "raw_hashes_verified": bool(hashes_verified),
        "target_verified": bool(lc_result["target_verified"] and uci_result["target_verified"]),
        "temporal_field_verified": bool(lc_result["temporal_verified"]),
        "leakage_audit_complete": bool(leakage_complete),
        "purpose_field_verified": bool(lc_result["purpose_verified"]),
        "license_verified": bool(license_verified),
        "modeling_started": False,
        "test_set_created": False,
        "open_issues": open_issues,
        "requires_research_owner_review": review_items,
    }
    write_json(RESULTS_METRICS / "stage2_summary.json", summary)
    write_stage2_report(lc_entry, uci_entry, lc_result, uci_result, run_meta, open_issues, review_items, summary)
    print(json.dumps(summary, indent=2))
    return 0 if status != "BLOCKED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
