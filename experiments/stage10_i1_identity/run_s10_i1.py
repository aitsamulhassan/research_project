"""S10-I1-IDENTITY runner. Integrity/provenance only. Does not edit authorization files."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from stage10.s10_i1_identity import (  # noqa: E402
    EXPERIMENT_ID,
    STATUS_PASS,
    classify_status,
    run_identity_check,
    sha256_file,
)

METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json"
AUDIT = ROOT / "audit" / "stage10_i1_identity.json"
REPORT = ROOT / "docs" / "STAGE_10_S10_I1_IDENTITY_REPORT.md"
CONFIG = ROOT / "configs" / "stage10" / "s10_i1_identity.yaml"
TEST_FILE = ROOT / "tests" / "test_stage10_i1_identity.py"
FORBIDDEN_WRITE = (
    ROOT / "docs" / "amendments" / "AMENDMENT-STAGE10-AUTHORIZATION.md",
    ROOT / "docs" / "STAGE_10_EXPERIMENTAL_PROTOCOL.md",
    ROOT / "RESEARCH_CONSTITUTION.md",
    ROOT / "results" / "decision" / "frozen_policy.json",
    ROOT / "results" / "decision" / "v2" / "frozen_policy.json",
    ROOT / "results" / "calibration" / "test" / "ebm_seed42_calibrated.csv",
    ROOT / "results" / "decision" / "v2" / "tables" / "table3_test_decision_outcomes.csv",
    ROOT / "results" / "calibration" / "artifacts" / "platt_record.json",
    ROOT / "docs" / "audits" / "STAGE_9_FINAL_CLOSURE_AUDIT.md",
    ROOT / "results" / "ablation" / "v1" / "metrics" / "ablation_summary.json",
    ROOT / "docs" / "STAGE_9_1_ABLATION_REPORT.md",
    ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md",
    ROOT / "audit" / "stage9_4_uci_run.json",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def git_commit(root: Path) -> str | None:
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
        if proc.returncode == 0:
            text = proc.stdout.strip()
            return text or None
    except OSError:
        return None
    return None


def apply_git_limitation(check: dict[str, Any], commit: str | None) -> dict[str, Any]:
    check = dict(check)
    limitations = list(check.get("documentation_limitations") or [])
    if commit is None:
        limitations.append(
            "git_commit is null (no usable .git / git). Recorded, not fabricated. "
            "Stage 10 protocol §14: not by itself a scientific abort."
        )
    check["documentation_limitations"] = limitations
    check["git_commit"] = commit
    check["status"] = classify_status(list(check.get("issues") or []), limitations)
    return check


def write_report(check: dict[str, Any]) -> None:
    a0 = check["a0"]
    a1 = check["a1"]
    a3 = check["a3_a4"]
    hashes = check["hashes"]
    limitations = check.get("documentation_limitations") or []
    issues = check.get("issues") or []
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    limitation_lines = [f"- {item}" for item in limitations] if limitations else ["- None beyond the statements above."]
    issue_lines = [f"- {item}" for item in issues] if issues else ["- None."]
    REPORT.write_text(
        "\n".join(
            [
                "# Stage 10 S10-I1-IDENTITY report",
                "",
                "This is an **integrity/provenance check**. It is **not** a new scientific confirmatory experiment.",
                "",
                "Passing does **not** generate independent scientific evidence. LendingClub TEST was already unblinded in Stages 4B–8.",
                "",
                f"**Experiment ID:** `{EXPERIMENT_ID}` (`S10-I1-IDENTITY`)  ",
                f"**Status:** `{check['status']}`  ",
                "**Classification:** `INTEGRITY / PROVENANCE CHECK — NOT A SCIENTIFIC CONFIRMATORY EXPERIMENT`  ",
                "**Authorization:** `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED` 2026-09-15  ",
                "**Execution gate:** `STAGE_10_EXECUTION = AUTHORIZED FOR S10-I1-IDENTITY, S10-R1-YEAR, S10-A1-GAP, AND S10-A4-SIDEBYSIDE ONLY`  ",
                "**This run executed:** `S10-I1-IDENTITY` only.",
                "",
                "## Bound statements",
                "",
                "- No model was retrained.",
                "- No EBM was refit.",
                "- No calibration was refit (Platt/isotonic were not fitted).",
                "- No threshold was selected or changed.",
                "- No historical Stage 7/8/9 result was overwritten.",
                "- UCI TEST was not opened.",
                "- Shariah rules and governance evidence were not modified.",
                "- A0, A1, and A3/A4 policies were not altered.",
                "- The paper was not drafted.",
                "- S10-R1-YEAR, S10-A1-GAP, and S10-A4-SIDEBYSIDE were **not** executed.",
                "- Stage 9 remains **CLOSED**.",
                "",
                "## A. A0 and A1",
                "",
                "A0 and A1 consume the **same** frozen stored column `p_selected` from",
                "`results/calibration/test/ebm_seed42_calibrated.csv`. A0 is the frozen two-threshold credit map.",
                "A1 uses the same credit-band mapping (`t_low=0.06`, `t_high=0.69`) and then the frozen G0",
                "`INSUFFICIENT_INFORMATION` fusion (LOW/MEDIUM → HUMAN_REVIEW, HIGH → REJECT). No new fusion engine was run;",
                "G0 is the algebraic identity of the stored Stage 8 v2 fused counts.",
                "",
                f"- A0 remap match: `{a0['match']}` counts `{a0['remap_counts']}` (t_low={a0['t_low']}, t_high={a0['t_high']})",
                f"- A1 credit-band match: `{a1['bands_match']}` `{a1['credit_bands_from_same_p_selected']}`",
                f"- A1 G0-from-same-bands match: `{a1['match']}` counts `{a1['remap_counts']}`",
                "",
                "## B. A3/A4",
                "",
                "A3/A4 consume the **same** frozen `p_selected` vector. The frozen monolithic threshold is `t*=0.16`",
                "applied as a binary map (`t_low=t_high=t*`), which has **no HUMAN_REVIEW branch**.",
                "",
                f"- A3/A4 remap match: `{a3['match']}` counts `{a3['remap_counts']}`",
                f"- t* = {a3['t_star']}",
                f"- HUMAN_REVIEW count = {a3['human_review_count']}",
                f"- human_review_branch = `{a3['human_review_branch']}`",
                "",
                "## C. Provenance",
                "",
                "Probability / decision inputs:",
                "",
                f"- `{check['probability_file']}` (`p_selected`, `p_platt`, `p_raw`, `row_ref`, `selected_method`)",
                "- `results/decision/v2/tables/table3_test_decision_outcomes.csv` (stored A0/A1/A3 counts)",
                "- `results/decision/v2/audit/test_audit_records.csv` (Stage 8 v2 per-row calibrated_probability / bands)",
                "- `results/decision/frozen_policy.json` (Stage 8 v1 freeze)",
                "- `results/decision/v2/frozen_policy.json` (Stage 8 v2 freeze)",
                "- `results/calibration/artifacts/platt_record.json`",
                "- `audit/stage9_4_uci_run.json` (`protected_hashes_after`)",
                "",
                f"- Calibrated TEST n = {check['n']}",
                f"- Unique `row_ref` = {check['row_provenance']['unique_row_ref']}",
                f"- Same 208,886 LendingClub TEST rows: `{check['same_test_rows']}`",
                f"- `p_selected` identical to stored `p_platt`: `{check['p_selected_identity']['p_selected_equals_stored_p_platt']}`",
                f"- `selected_method` is Platt only: `{check['p_selected_identity']['selected_method_platt_only']}`",
                f"- Stage 8 v2 audit n = {check['row_provenance']['stage8_v2_audit_n']}",
                f"- Audit calibrated_probability matches `p_selected` (positional, atol 1e-12): `{check['row_provenance']['audit_calibrated_matches_p_selected']}`",
                "- `p_selected` was **not** recomputed from `p_raw` in this check.",
                "- EBM/Platt joblib files were **not** loaded for scoring.",
                "",
                "## D. Policy integrity",
                "",
                f"- Stage 8 v1 freeze SHA-256: `{hashes['v1_freeze_sha256']}` (expected `{hashes['expected_v1']}`)",
                f"- Stage 8 v2 freeze SHA-256: `{hashes['v2_freeze_sha256']}` (expected `{hashes['expected_v2']}`)",
                f"- table3 SHA-256: `{hashes['table3_sha256']}` (expected `{hashes['expected_table3']}`)",
                f"- TEST calibrated CSV SHA-256: `{hashes['test_cal_sha256']}` (expected `{hashes['expected_test_cal']}`)",
                f"- Match Stage 9.4 `protected_hashes_after`: `{hashes['vs_stage9_4_protected_after']['all_match']}`",
                f"- t_low={check['thresholds']['t_low']}, t_high={check['thresholds']['t_high']}, t*={check['thresholds']['t_star']}",
                f"- v2 freeze t_low={check['thresholds']['v2_t_low']}, t_high={check['thresholds']['v2_t_high']}, monolithic_t={check['thresholds']['v2_monolithic_t']}",
                f"- thresholds_reselected=`{check['thresholds']['thresholds_reselected']}`",
                f"- Platt a={check['platt']['a']}, b={check['platt']['b']}; record match=`{check['platt']['match']}`",
                "",
                "## E. Outcome",
                "",
                f"**{check['status']}**",
                "",
                "This classification is an integrity/provenance result. It is not a scientific confirmatory TEST experiment.",
                "",
                "## Issues",
                "",
                *issue_lines,
                "",
                "## Documentation limitations",
                "",
                *limitation_lines,
                "",
                "## Activities not executed",
                "",
                "- S10-R1-YEAR: not executed",
                "- S10-A1-GAP: not executed",
                "- S10-A4-SIDEBYSIDE: not executed",
                "",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> int:
    started = utc_now()
    before = {str(p): sha256_file(p) for p in FORBIDDEN_WRITE if p.exists()}
    commit = git_commit(ROOT)
    check = apply_git_limitation(run_identity_check(), commit)
    dump_json(METRICS, check)
    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    if not CONFIG.exists():
        CONFIG.write_text(
            "experiment_id: s10_i1_identity_v1\n"
            "classification: INTEGRITY / PROVENANCE CHECK — NOT A SCIENTIFIC CONFIRMATORY EXPERIMENT\n"
            "models_trained: false\n"
            "calibration_refit: false\n"
            "thresholds_searched: false\n",
            encoding="utf-8",
        )
    write_report(check)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(TEST_FILE), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    exit_code = int(proc.returncode)
    lines = [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]
    test_summary = lines[-1] if lines else (proc.stderr or "")[-200:]
    after = {str(p): sha256_file(p) for p in FORBIDDEN_WRITE if p.exists()}
    if after != before:
        raise RuntimeError(f"S10-I1 runner mutated protected files: {before} vs {after}")
    audit = {
        "experiment_id": EXPERIMENT_ID,
        "amendment_id": "AMENDMENT-STAGE10-AUTHORIZATION",
        "amendment_status": "APPROVED",
        "started": started,
        "execution_timestamp": utc_now(),
        "git_commit": commit,
        "status": check["status"],
        "classification": check["classification"],
        "confirmatory_experiment": False,
        "models_trained": False,
        "models_loaded_for_scoring": False,
        "calibration_refit": False,
        "thresholds_searched": False,
        "uci_opened": False,
        "stage8_9_results_modified": False,
        "s10_r1_executed": False,
        "s10_a1_gap_executed": False,
        "s10_a4_executed": False,
        "issues": check["issues"],
        "documentation_limitations": check["documentation_limitations"],
        "n": check["n"],
        "a0_match": check["a0"]["match"],
        "a1_match": check["a1"]["match"],
        "a3_match": check["a3_a4"]["match"],
        "hashes": check["hashes"],
        "thresholds": check["thresholds"],
        "platt": check["platt"],
        "protected_files_unchanged": after == before,
        "config_sha256": sha256_file(CONFIG),
        "metrics_sha256": sha256_file(METRICS),
        "report_sha256": sha256_file(REPORT),
        "pytest_exit_code": exit_code,
        "test_command": f"python -m pytest {TEST_FILE.relative_to(ROOT).as_posix()} -q --tb=short",
        "test_summary": test_summary,
        "software": {
            "python": sys.version,
        },
    }
    dump_json(AUDIT, audit)
    if check["issues"]:
        return 1
    if check["status"] == STATUS_PASS or check["status"].startswith("PASS"):
        return 0 if exit_code == 0 else exit_code
    return 1 if exit_code == 0 else exit_code


if __name__ == "__main__":
    raise SystemExit(main())
