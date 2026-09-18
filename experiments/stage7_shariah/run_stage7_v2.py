"""Stage 7 v2 L1/L2 Shariah-oriented governance. Does not rerun Stage 8 or TEST fusion."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data.audit_datasets import git_commit, sha256_file  # noqa: E402
from shariah.engine import AMENDMENT_ID, CATALOG_VERSION, ENGINE_VERSION, L1L2_VERSION, evaluate, from_mapping  # noqa: E402
from shariah.l1 import assess_dataset_readiness  # noqa: E402
from shariah.l2 import (  # noqa: E402
    EVALUATION_MODE_PER_APPLICATION,
    evaluate_lendingclub_application,
)
from shariah.plots import figure_l1_l2  # noqa: E402
from shariah.provenance import load_source_register  # noqa: E402
from shariah.validation import assert_rule_executable, assert_source_fields  # noqa: E402

EXPERIMENT_ID = "stage7-shariah-gov-v2"
FIXED_TS = "2026-09-15T00:00:00+00:00"
CASES_PATH = ROOT / "data" / "synthetic" / "shariah_governance_cases.json"
FIXTURES_PATH = ROOT / "data" / "synthetic" / "lendingclub_l2_schema_fixtures.json"
OUT = ROOT / "results" / "shariah" / "v2"
FIG = ROOT / "results" / "figures" / "shariah" / "v2"
AUDIT = ROOT / "audit" / "stage7_v2_governance_run.json"
REPORT = ROOT / "docs" / "STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md"
V1_REPORT = ROOT / "docs" / "STAGE_7_SHARIAH_GOVERNANCE_REPORT.md"
V1_AUDIT = ROOT / "audit" / "stage7_shariah_run.json"
CATALOG_PATH = ROOT / "docs" / "shariah" / "rule_catalog.json"
SOURCE_PATH = ROOT / "docs" / "shariah" / "source_register.json"
AMENDMENT_PATH = ROOT / "docs" / "amendments" / "AMENDMENT-SHARIAH-001.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def run_pytest() -> tuple[int, str, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests"), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    summary = ""
    for line in reversed(text.splitlines()):
        if "passed" in line:
            summary = line.strip()
            break
    return proc.returncode, text.strip(), summary


def case_to_evidence(row: dict) -> dict:
    skip = {"expected_layer_a", "expected_status", "note"}
    return {k: v for k, v in row.items() if k not in skip}


def compact_l2_result(result: dict) -> dict:
    return {
        "case_id": result["case_id"],
        "synthetic": result["synthetic"],
        "evaluation_mode": result["evaluation_mode"],
        "dataset_id": result["dataset_id"],
        "record_reference_hash": result["record_reference_hash"],
        "evidence_hash": result["evidence_hash"],
        "overall_governance_status": result["overall_governance_status"],
        "layer_a": result["layer_a_completeness"]["layer_a"],
        "missing_evidence": result["missing_evidence"],
        "triggered_rule_ids": result["triggered_rule_ids"],
        "source_ids": result["source_ids"],
        "expert_validation_states": result["expert_validation_states"],
        "any_expert_validated": result["any_expert_validated"],
        "certification_claim": result["certification_claim"],
        "cache_hit": result["cache_hit"],
        "l1": result["l1"],
        "l2": result["l2"],
        "amendment_id": result["amendment_id"],
        "engine_version": result["engine_version"],
        "l1l2_version": result["l1l2_version"],
        "timestamp": result["timestamp"],
    }


def write_report(payload: dict) -> None:
    lines = [
        "# Stage 7 v2 Shariah-Oriented Governance Report",
        "",
        "This implemented system is a **research prototype for Shariah-oriented governance and evidence traceability**, not a Shariah certification mechanism. No applicant is described as Shariah compliant on the basis of this system.",
        "",
        f"Stage 7 v1 remains historical evidence: `{V1_REPORT.relative_to(ROOT).as_posix()}` and `{V1_AUDIT.relative_to(ROOT).as_posix()}`. This document does not overwrite those artifacts.",
        "",
        "## A. Methodology authority",
        "",
        f"Controlling amendment: `{AMENDMENT_ID}` (`APPROVED`). Full text: `docs/amendments/AMENDMENT-SHARIAH-001.md`.",
        "",
        "Design A (contract-level / institutional-product governance) is adopted. Design B (purpose classification) is rejected. `SHR-001` remains `UNSUPPORTED_RETIRED` and is not reconstructed.",
        "",
        "## B. Stage 7 objective",
        "",
        "**L1 — Dataset / integration readiness** asks whether a dataset/schema contains the evidence required for applicant-level Shariah governance evaluation. It is not an applicant-level religious ruling.",
        "",
        "**L2 — Per-application evaluation** extracts a governance evidence object from that row, then evaluates it. Identical L2 statuses are allowed. Broadcast of one unevaluated profile as N independent inspections is not.",
        "",
        "Stage 8 fusion and Stage 9 were not started in this run.",
        "",
        "## C. L1 result",
        "",
        f"LendingClub L1 status: `{payload['l1']['readiness_status']}`.",
        "",
        f"This is dataset/integration readiness (`is_applicant_level_ruling={payload['l1']['is_applicant_level_ruling']}`). Reason: {payload['l1']['reason']}",
        "",
        "Contractual schema fields present in the documented LendingClub columns: none.",
        "",
        "## D. L2 design",
        "",
        "`extract_application_governance_evidence(row)` builds a row-specific evidence object. Firewall fields are dropped. Contract type is set to `unknown`; it is never inferred from `purpose`. `evaluate_application_governance` calls the existing Stage 7 engine and attaches per-row `record_reference_hash`, `evidence_hash`, missing-evidence, and `evaluation_mode=PER_APPLICATION`. Deterministic cache-by-evidence-hash is allowed; each row still keeps its own record hash.",
        "",
        "Development used synthetic/unit fixtures only. The protected TEST split was not used to select rules, schema, or methodology.",
        "",
        "## E. Evidence firewall",
        "",
        "Prohibited in the Shariah evidence object except as a deliberate SH-ARCH-003 boundary-test `extra` injection:",
        "",
        "`fico_n`, `loan_amnt`, `dti_n`, `revenue`, `emp_length`, `home_ownership_n`, `addr_state`, `zip_code`, `purpose`, `title`, `desc`, `id`, `issue_d`, `experience_c`, `Default`.",
        "",
        "## F. Purpose invariance",
        "",
        "`purpose` is a frozen credit / application-purpose field. It is not contract type, not Murabahah evidence, not Ijarah evidence, and not Shariah-compliance evidence. Two unit fixtures that differ only in `purpose` produce identical semantic evidence objects and identical L2 governance status.",
        "",
        f"Purpose-invariance evidence hashes in this run: `{payload['purpose_invariance']['hash_a']}` and `{payload['purpose_invariance']['hash_b']}` (equal={payload['purpose_invariance']['hashes_equal']}). Record hashes differ.",
        "",
        "## G. Rule inventory",
        "",
        "| Rule ID | Family | Validation status | Executable |",
        "| --- | --- | --- | --- |",
    ]
    for rule in payload["implemented_rules"]:
        family = rule.get("rule_family", "")
        lines.append(
            f"| {rule['rule_id']} | {family} | {rule['validation_status']} | {rule['executable']} |"
        )
    lines += [
        "",
        "| Identifier | Status |",
        "| --- | --- |",
        "| `SHR-001` | `UNSUPPORTED_RETIRED` (not reconstructed; not in `rules[]`) |",
        "| `SH-AAOIFI-SS8-POSSESSION` | `NOT_VERIFIED`; not executable |",
        "",
        "No executable religious rule was added in Stage 7 v2. The core engine version remains `stage7-shariah-engine-v1`.",
        "",
        "## H. AAOIFI boundary",
        "",
        "`SH-AAOIFI-SS8-GATE` and `SH-AAOIFI-SS9-GATE` remain identity/unavailability gates. Operative SS(8)/SS(9) clauses were not implemented. Clause-level AAOIFI implementation remains blocked.",
        "",
        "## I. Expert validation",
        "",
        "No current rule is `EXPERT_VALIDATED`. No expert-validation record was created. Architecture gates remain `RESEARCH_ARCHITECTURE_NOT_A_RULING`. Source-mapped SBP/SECP rules remain `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW`.",
        "",
        "## J. Synthetic testing",
        "",
        "Existing synthetic evidence-sensitive cases were preserved and rerun. L1/L2 tests A–H used unit fixtures, not the protected TEST split.",
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
        "L2 unit fixtures (compact):",
        "",
        "| Fixture | evaluation_mode | L2 status | evidence_hash (12) | record_hash (12) | cache_hit |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in payload["l2_table"]:
        lines.append(
            f"| {row['fixture_key']} | {row['evaluation_mode']} | {row['overall_governance_status']} | `{row['evidence_hash'][:12]}` | `{row['record_reference_hash'][:12]}` | {row['cache_hit']} |"
        )
    lines += [
        "",
        "## K. Reproducibility",
        "",
        f"- experiment_id: `{EXPERIMENT_ID}`",
        f"- amendment_id: `{AMENDMENT_ID}`",
        f"- engine_version: `{ENGINE_VERSION}`",
        f"- l1l2_version: `{L1L2_VERSION}`",
        f"- catalog_version: `{CATALOG_VERSION}`",
        f"- catalog_sha256: `{payload['hashes']['catalog']}`",
        f"- source_register_sha256: `{payload['hashes']['source_register']}`",
        f"- amendment_sha256: `{payload['hashes']['amendment']}`",
        f"- synthetic_cases_sha256: `{payload['hashes']['synthetic_cases']}`",
        f"- l2_fixtures_sha256: `{payload['hashes']['l2_fixtures']}`",
        f"- git_commit: `{payload['git_commit']}`",
        f"- execution_timestamp: `{payload['execution_timestamp']}`",
        f"- software: `{payload['python']}`",
        f"- test command: `python -m pytest tests -q --tb=short`",
        f"- test summary: `{payload['test_summary']}`",
        "",
        "## L. Limitations",
        "",
        "- LendingClub cannot establish applicant-level Shariah compliance. L1 records a schema/evidence-gap. L2 for LendingClub-schema rows remains `INSUFFICIENT_INFORMATION`.",
        "- This is not applicant-level Shariah screening of the protected TEST set.",
        "- AAOIFI SS(8)/SS(9) operative clauses were not verified and are not implemented.",
        "- No rule is expert-validated.",
        "- Stage 8 broadcast fusion is unchanged and remains historically v1.",
        "- Stage 9 remains blocked.",
        "",
        "## Stage gate",
        "",
        f"`STAGE_7_STATUS = {payload['status']}`",
        "",
        payload.get("status_reason", ""),
        "",
        "```text",
        "STAGE_8 = NOT IMPLEMENTED",
        "STAGE_9 = BLOCKED",
        "```",
        "",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if REPORT.resolve() == V1_REPORT.resolve():
        raise RuntimeError("Refusing to overwrite Stage 7 v1 report.")
    if AUDIT.resolve() == V1_AUDIT.resolve():
        raise RuntimeError("Refusing to overwrite Stage 7 v1 audit.")

    for path in (OUT / "tables", FIG):
        path.mkdir(parents=True, exist_ok=True)

    sources = [s.as_dict() for s in load_source_register()]
    for src in sources:
        assert_source_fields(src)
    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    for rule in catalog["rules"]:
        assert_rule_executable(rule)

    implemented = [r for r in catalog["rules"] if r.get("executable")]
    l1 = assess_dataset_readiness("lendingclub")

    cases_blob = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    case_table = []
    mismatches = []
    for row in cases_blob["cases"]:
        result = evaluate(from_mapping(case_to_evidence(row)), timestamp=FIXED_TS)
        actual = result["overall_governance_status"]
        layer_a = result["layer_a_completeness"]["layer_a"]
        case_table.append(
            {
                "case_id": row["case_id"],
                "synthetic": True,
                "layer_a": layer_a,
                "expected_status": row["expected_status"],
                "actual_status": actual,
                "experiment_id": EXPERIMENT_ID,
            }
        )
        if actual != row["expected_status"] or layer_a != row["expected_layer_a"]:
            mismatches.append(row["case_id"])

    fixtures_blob = json.loads(FIXTURES_PATH.read_text(encoding="utf-8"))
    cache: dict[str, dict] = {}
    l2_compact = []
    l2_table = []
    for row in fixtures_blob["fixtures"]:
        result = evaluate_lendingclub_application(row, timestamp=FIXED_TS, cache=cache, l1_result=l1)
        compact = compact_l2_result(result)
        compact["fixture_key"] = row["_fixture_key"]
        l2_compact.append(compact)
        l2_table.append(
            {
                "fixture_key": row["_fixture_key"],
                "evaluation_mode": result["evaluation_mode"],
                "overall_governance_status": result["overall_governance_status"],
                "evidence_hash": result["evidence_hash"],
                "record_reference_hash": result["record_reference_hash"],
                "cache_hit": result["cache_hit"],
            }
        )

    purpose_a = dict(fixtures_blob["fixtures"][0])
    purpose_b = dict(fixtures_blob["fixtures"][0])
    purpose_b["_fixture_key"] = "report-purpose-b"
    purpose_b["id"] = 999001
    purpose_b["purpose"] = "home_improvement"
    out_a = evaluate_lendingclub_application(purpose_a, timestamp=FIXED_TS, l1_result=l1)
    out_b = evaluate_lendingclub_application(purpose_b, timestamp=FIXED_TS, l1_result=l1)
    purpose_invariance = {
        "hash_a": out_a["evidence_hash"],
        "hash_b": out_b["evidence_hash"],
        "hashes_equal": out_a["evidence_hash"] == out_b["evidence_hash"],
        "status_equal": out_a["overall_governance_status"] == out_b["overall_governance_status"],
        "record_hashes_differ": out_a["record_reference_hash"] != out_b["record_reference_hash"],
    }

    pd.DataFrame(case_table).to_csv(OUT / "tables" / "table_synthetic_cases.csv", index=False)
    pd.DataFrame(l2_table).to_csv(OUT / "tables" / "table_l2_fixtures.csv", index=False)
    dump_json(OUT / "l1_lendingclub.json", l1)
    dump_json(OUT / "l2_fixture_evaluations.json", {"experiment_id": EXPERIMENT_ID, "evaluations": l2_compact})
    figure_l1_l2(FIG / "figure_l1_l2")

    hashes = {
        "catalog": sha256_file(CATALOG_PATH),
        "source_register": sha256_file(SOURCE_PATH),
        "amendment": sha256_file(AMENDMENT_PATH),
        "synthetic_cases": sha256_file(CASES_PATH),
        "l2_fixtures": sha256_file(FIXTURES_PATH),
    }
    execution_timestamp = utc_now()
    audit_body = {
        "amendment_id": AMENDMENT_ID,
        "methodology_version": L1L2_VERSION,
        "experiment_id": EXPERIMENT_ID,
        "engine_version": ENGINE_VERSION,
        "l1l2_version": L1L2_VERSION,
        "catalog_version": CATALOG_VERSION,
        "source_register_version": json.loads(SOURCE_PATH.read_text(encoding="utf-8"))["register_version"],
        "l1_status": l1["readiness_status"],
        "l1_is_applicant_level_ruling": False,
        "l2_evaluation_mode": EVALUATION_MODE_PER_APPLICATION,
        "any_expert_validated": False,
        "certification_claim_policy": False,
        "shr_001_status": "UNSUPPORTED_RETIRED",
        "aaoifi_clause_level_implementation": "BLOCKED",
        "credit_model_not_called": True,
        "explainability_not_used_for_rulings": True,
        "protected_test_split_not_used": True,
        "stage8_implemented": False,
        "stage9": "BLOCKED",
        "hashes": hashes,
        "git_commit": git_commit(ROOT),
        "execution_timestamp": execution_timestamp,
        "fixed_evaluation_timestamp": FIXED_TS,
        "software_library_versions": {"python": sys.version.replace("\n", " ")},
        "synthetic_case_mismatches": mismatches,
        "purpose_invariance": purpose_invariance,
        "status": "PENDING_TESTS",
        "tests_executed": "python -m pytest tests -q --tb=short",
        "pass_count": None,
        "fail_count": None,
        "pytest_exit_code": None,
    }
    dump_json(AUDIT, audit_body)

    print("Running pytest", flush=True)
    pytest_code, pytest_text, pytest_summary = run_pytest()

    passed = re.search(r"(\d+) passed", pytest_summary or pytest_text)
    failed = re.search(r"(\d+) failed", pytest_summary or pytest_text)
    audit_body["pass_count"] = int(passed.group(1)) if passed else None
    audit_body["fail_count"] = int(failed.group(1)) if failed else 0
    status = "PASS" if pytest_code == 0 and not mismatches and purpose_invariance["hashes_equal"] else "REQUIRES REVISION"
    reason = (
        "Stage 7 v2 L1/L2 implemented under AMENDMENT-SHARIAH-001; synthetic cases matched; pytest passed; no EXPERT_VALIDATED claim; Stage 8 not modified."
        if status == "PASS"
        else f"pytest_exit={pytest_code} mismatches={mismatches} purpose_invariance={purpose_invariance}"
    )
    audit_body["status"] = status
    audit_body["status_reason"] = reason
    audit_body["pytest_exit_code"] = pytest_code
    audit_body["test_summary"] = pytest_summary or pytest_text[-500:]
    audit_body["pytest_tail"] = pytest_text[-2000:]
    dump_json(AUDIT, audit_body)

    write_report(
        {
            "l1": l1,
            "implemented_rules": implemented,
            "case_table": case_table,
            "l2_table": l2_table,
            "purpose_invariance": purpose_invariance,
            "hashes": hashes,
            "git_commit": audit_body["git_commit"],
            "execution_timestamp": execution_timestamp,
            "python": audit_body["software_library_versions"]["python"],
            "test_summary": pytest_summary or f"pytest exit {pytest_code}",
            "status": status,
            "status_reason": reason,
        }
    )
    print(json.dumps({"status": status, "report": str(REPORT), "audit": str(AUDIT)}, indent=2), flush=True)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
