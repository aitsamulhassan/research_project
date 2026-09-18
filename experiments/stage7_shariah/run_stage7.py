"""Stage 7 Shariah-oriented governance layer. No credit-model calls. Not certification."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data.audit_datasets import git_commit  # noqa: E402
from shariah.engine import CATALOG_VERSION, ENGINE_VERSION, evaluate, from_mapping  # noqa: E402
from shariah.plots import figure_evidence_separation, figure_governance_flow  # noqa: E402
from shariah.provenance import load_source_register  # noqa: E402
from shariah.rules import load_catalog  # noqa: E402
from shariah.schema import LENDINGCLUB_PREDICTORS  # noqa: E402
from shariah.validation import assert_rule_executable, assert_source_fields  # noqa: E402

EXPERIMENT_ID = "stage7-shariah-gov-v1"
FIXED_TS = "2026-09-15T00:00:00+00:00"
CASES_PATH = ROOT / "data" / "synthetic" / "shariah_governance_cases.json"
EVIDENCE_SCHEMA = ROOT / "docs" / "shariah" / "evidence_schema.json"
OUT = ROOT / "results" / "shariah"
FIG = ROOT / "results" / "figures" / "shariah"
AUDIT = ROOT / "audit" / "stage7_shariah_run.json"
REPORT = ROOT / "docs" / "STAGE_7_SHARIAH_GOVERNANCE_REPORT.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def run_pytest() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests"), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, text.strip()


def case_to_evidence(row: dict) -> dict:
    skip = {"expected_layer_a", "expected_status", "note"}
    return {k: v for k, v in row.items() if k not in skip}


def write_report(payload: dict) -> None:
    lines = [
        "# Stage 7 Shariah-Oriented Governance Report",
        "",
        "This implemented system is a **research prototype for Shariah-oriented governance and evidence traceability**, not a Shariah certification mechanism. No applicant is described as Shariah compliant on the basis of this system.",
        "",
        "## A. Sources verified",
        "",
    ]
    for src in payload["sources"]:
        lines.append(
            f"- `{src['source_id']}` — {src['authority']}: {src['document_title']} ({src['verification_status']}). URL: {src['url']}"
        )
    lines += [
        "",
        "## B. Rules implemented",
        "",
        "| Rule ID | Contract/scope | Condition | Outcome vocabulary | Source | Validation status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for rule in payload["implemented_rules"]:
        lines.append(
            f"| {rule['rule_id']} | {rule['contract_type']} | {rule['condition']} | {rule['outcome']} | {rule['document']} | {rule['validation_status']} |"
        )
    lines += [
        "",
        "## C. Rules not implemented",
        "",
        "AAOIFI SS (8) and SS (9) **operative clauses** were not implemented: official text is copyrighted and the AAOIFI viewer is password-protected. IBD Circular 02 of 2008 Appendix-A Essentials were not implemented beyond paragraphs restated in retrieved IBD Circular 01 of 2012. No rule was written from memory.",
        "",
        "## D. Evidence schema",
        "",
        "Governance requires contract type, institution class, and, where a verified rule applies, Shariah Board product approval, Murabaha invoice/payment channels, or SECP security-certificate evidence. See `docs/shariah/EVIDENCE_SCHEMA.md`.",
        "",
        "## E. LendingClub evidence availability",
        "",
        "None of the nine frozen credit predictors is Shariah evidence. Contract-level fields are **NOT_AVAILABLE** in LendingClub.",
        "",
        "| Evidence item | Available in LendingClub | Verification status |",
        "| --- | --- | --- |",
    ]
    for row in payload["lc_evidence"]:
        lines.append(f"| {row['evidence_item']} | {row['available_in_lendingclub']} | {row['verification_status']} |")
    lines += [
        "",
        "## F. Rule-engine behavior",
        "",
        "Layer A: COMPLETE / PARTIAL / INSUFFICIENT. Layer B: PASS / REVIEW / NOT_STRUCTURABLE_WITHOUT_REDESIGN / INSUFFICIENT_INFORMATION.",
        "Overall PASS is possible only when Layer A is COMPLETE and every applicable verified rule PASSes. Murabahah/Ijarah identifications remain PARTIAL because AAOIFI clauses were not verified, so they cannot overall PASS.",
        "",
        "## G. Synthetic test cases",
        "",
        "All cases below are **Synthetic governance test cases**, not LendingClub observations.",
        "",
        "| Case ID | Synthetic | Layer A | Expected | Actual |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in payload["case_table"]:
        lines.append(
            f"| {row['case_id']} | {row['synthetic']} | {row['layer_a']} | {row['expected_status']} | {row['actual_status']} |"
        )
    lines += [
        "",
        "## H. Provenance",
        "",
        "Each evaluation stores rule_id, source document, section/clause, version, URL, source statement, research interpretation, and machine implementation. Expert validation is not claimed.",
        "",
        "## I. Conflicts",
        "",
        "Unresolved: AAOIFI SS (8) clauses vs SBP Murabaha operational circulars cannot be compared because SS (8) body text was not retrieved. SECP vs SBP scopes are complementary, not contradictory.",
        "",
        "## J. Expert-validation status",
        "",
        "No rule is marked EXPERT_VALIDATED. Implemented Shariah-mapped rules are SOURCE_VERIFIED_PENDING_EXPERT_REVIEW. Architecture gates are RESEARCH_ARCHITECTURE_NOT_A_RULING.",
        "",
        "## K. Tests",
        "",
        payload.get("test_suite_summary", "Not run."),
        "",
        "## L. Limitations",
        "",
        "- LendingClub application data cannot establish contractual Shariah status.",
        "- AAOIFI SS (8)/SS (9) clauses were not verified from official text.",
        "- SBP SGF annex text was mapped from a public republication matching IFPD Circular 08 of 2024 because sbp.org.pk PDFs returned HTTP 403 here.",
        "- SECP SGR clause text was mapped from a MUFAP-hosted SRO PDF because secp.gov.pk PDF download returned HTTP 403 here.",
        "- This layer does not issue religious rulings and does not fuse with credit, calibration, or SHAP evidence.",
        "",
        "## M. Reproducibility",
        "",
        f"- experiment_id: `{EXPERIMENT_ID}`",
        f"- engine_version: `{ENGINE_VERSION}`",
        f"- catalog_version: `{CATALOG_VERSION}`",
        f"- git_commit: `{payload['git_commit']}`",
        f"- timestamp: `{payload['execution_timestamp']}`",
        "",
        "## N. Stage gate",
        "",
        f"`STAGE_7_STATUS = {payload['status']}`",
        "",
        payload.get("status_reason", ""),
        "",
        "Stage 8 was not started.",
        "",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    for path in (OUT / "tables", FIG, ROOT / "docs" / "shariah"):
        path.mkdir(parents=True, exist_ok=True)

    sources = [s.as_dict() for s in load_source_register()]
    for src in sources:
        assert_source_fields(src)
    catalog = json.loads((ROOT / "docs" / "shariah" / "rule_catalog.json").read_text(encoding="utf-8"))
    for rule in catalog["rules"]:
        assert_rule_executable(rule)
    load_catalog()

    pd.DataFrame(sources).to_csv(ROOT / "docs" / "shariah" / "source_register.csv", index=False)
    pd.DataFrame(sources).assign(experiment_id=EXPERIMENT_ID).to_csv(OUT / "tables" / "table1_source_register.csv", index=False)

    implemented = [r for r in catalog["rules"] if r.get("executable")]
    pd.DataFrame(implemented).assign(experiment_id=EXPERIMENT_ID).to_csv(
        OUT / "tables" / "table2_rule_catalog.csv", index=False
    )

    schema = json.loads(EVIDENCE_SCHEMA.read_text(encoding="utf-8"))
    lc_rows = []
    for item in schema["items"]:
        lc_rows.append(
            {
                "contract_scope": ",".join(item["applies_to"]),
                "evidence_item": item["evidence_item"],
                "required_or_conditional": item["required_or_conditional"],
                "available_in_lendingclub": item["available_in_lendingclub"],
                "source_requirement": item["source_requirement"],
                "verification_status": item["verification_status"],
                "experiment_id": EXPERIMENT_ID,
                "lendingclub_predictors_are_not_this_field": True,
                "frozen_predictors": ";".join(LENDINGCLUB_PREDICTORS),
            }
        )
    pd.DataFrame(lc_rows).to_csv(OUT / "tables" / "table3_evidence_requirements.csv", index=False)
    pd.DataFrame(lc_rows).to_csv(OUT / "evidence_completeness.csv", index=False)

    cases_blob = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    evaluations = []
    case_table = []
    mismatches = []
    for row in cases_blob["cases"]:
        ev = from_mapping(case_to_evidence(row))
        result = evaluate(ev, timestamp=FIXED_TS)
        evaluations.append(result)
        actual = result["overall_governance_status"]
        layer_a = result["layer_a_completeness"]["layer_a"]
        case_table.append(
            {
                "case_id": row["case_id"],
                "synthetic": True,
                "label": "Synthetic governance test case",
                "layer_a": layer_a,
                "expected_status": row["expected_status"],
                "actual_status": actual,
                "experiment_id": EXPERIMENT_ID,
            }
        )
        if actual != row["expected_status"] or layer_a != row["expected_layer_a"]:
            mismatches.append({"case_id": row["case_id"], "expected": row, "actual": {"status": actual, "layer_a": layer_a}})

    dump_json(OUT / "rule_evaluations.json", {"experiment_id": EXPERIMENT_ID, "evaluations": evaluations})
    pd.DataFrame(case_table).to_csv(OUT / "tables" / "table4_governance_test_cases.csv", index=False)

    prov_rows = []
    for rule in implemented:
        prov_rows.append(
            {
                "rule_id": rule["rule_id"],
                "authority": rule["authority"],
                "document": rule["document"],
                "clause": rule.get("clause"),
                "version": rule.get("source_version"),
                "url": rule["source_url"],
                "expert_validation": rule["validation_status"],
                "expert_validation_record": rule.get("expert_validation_record"),
                "experiment_id": EXPERIMENT_ID,
            }
        )
    pd.DataFrame(prov_rows).to_csv(OUT / "tables" / "table5_provenance_completeness.csv", index=False)

    figure_governance_flow(FIG / "figure1_governance_architecture")
    figure_evidence_separation(FIG / "figure2_evidence_separation")
    dump_json(FIG / "figure_manifest.json", {"experiment_id": EXPERIMENT_ID, "stems": ["figure1_governance_architecture", "figure2_evidence_separation"]})

    audit_body = {
        "explainability_not_used_for_rulings": True,
        "credit_model_not_called": True,
        "experiment_id": EXPERIMENT_ID,
        "engine_version": ENGINE_VERSION,
        "catalog_version": CATALOG_VERSION,
        "synthetic_case_version": cases_blob["version"],
        "fixed_timestamp": FIXED_TS,
        "git_commit": git_commit(ROOT),
        "execution_timestamp": utc_now(),
        "status": "PENDING_TESTS",
        "mismatches": mismatches,
        "software_library_versions": {"python": sys.version.replace("\n", " ")},
    }
    dump_json(AUDIT, audit_body)

    print("Running pytest", flush=True)
    pytest_code, pytest_text = run_pytest()
    status = "PASS" if pytest_code == 0 and not mismatches else "BLOCKED"
    reason = (
        "Authoritative source verification completed for implemented rules; no invented AAOIFI clauses; tests passed."
        if status == "PASS"
        else f"pytest_exit={pytest_code} mismatches={mismatches}"
    )
    audit_body["status"] = status
    audit_body["status_reason"] = reason
    audit_body["pytest_exit_code"] = pytest_code
    dump_json(AUDIT, audit_body)

    write_report(
        {
            "sources": sources,
            "implemented_rules": implemented,
            "lc_evidence": lc_rows,
            "case_table": case_table,
            "git_commit": git_commit(ROOT),
            "execution_timestamp": audit_body["execution_timestamp"],
            "test_suite_summary": pytest_text[-4000:] if pytest_text else f"pytest exit {pytest_code}",
            "status": status,
            "status_reason": reason,
        }
    )
    print(json.dumps({"status": status, "mismatches": mismatches}, indent=2), flush=True)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
