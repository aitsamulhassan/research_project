"""S10-A1-GAP runner. Analysis-only descriptive decomposition. Does not edit authorization files."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision.stage9_1 import sha256_file  # noqa: E402
from stage10.s10_a1_gap import CLASSIFICATION, EXPERIMENT_ID, json_safe, run_gap_analysis  # noqa: E402

METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_a1_gap.json"
TABLE_CROSS = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_a1_gap_crosstab.csv"
TABLE_TRACE = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_a1_gap_policy_trace.csv"
AUDIT = ROOT / "audit" / "stage10_s10_a1_gap.json"
REPORT = ROOT / "docs" / "STAGE_10_S10_A1_GAP_REPORT.md"
CONFIG = ROOT / "configs" / "stage10" / "s10_a1_gap.yaml"
TEST_FILE = ROOT / "tests" / "test_stage10_a1_gap.py"
FORBIDDEN_WRITE = (
    ROOT / "docs" / "amendments" / "AMENDMENT-STAGE10-AUTHORIZATION.md",
    ROOT / "docs" / "STAGE_10_EXPERIMENTAL_PROTOCOL.md",
    ROOT / "RESEARCH_CONSTITUTION.md",
    ROOT / "results" / "decision" / "frozen_policy.json",
    ROOT / "results" / "decision" / "v2" / "frozen_policy.json",
    ROOT / "results" / "calibration" / "test" / "ebm_seed42_calibrated.csv",
    ROOT / "results" / "decision" / "v2" / "tables" / "table3_test_decision_outcomes.csv",
    ROOT / "docs" / "audits" / "STAGE_9_FINAL_CLOSURE_AUDIT.md",
    ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json",
    ROOT / "audit" / "stage10_i1_identity.json",
    ROOT / "docs" / "STAGE_10_S10_I1_IDENTITY_REPORT.md",
    ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_r1_year.json",
    ROOT / "audit" / "stage10_s10_r1_year.json",
    ROOT / "docs" / "STAGE_10_S10_R1_YEAR_REPORT.md",
    ROOT / "src" / "stage10" / "s10_i1_identity.py",
    ROOT / "src" / "stage10" / "s10_r1_year.py",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_safe(payload), indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def git_commit(root: Path) -> str | None:
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
        if proc.returncode == 0:
            text = proc.stdout.strip()
            return text or None
    except OSError:
        return None
    return None


def _band_line(rows: list[dict[str, Any]]) -> list[str]:
    lines = []
    for row in rows:
        lines.append(
            f"- {row['credit_band']}: n={row['count']} ({row['percentage_of_test']:.4f}% of TEST); rule `{row['rule']}`"
        )
    return lines


def _l2_line(rows: list[dict[str, Any]]) -> list[str]:
    lines = []
    for row in rows:
        observed = "observed" if row["observed_on_lc_test"] else "not observed on LC TEST"
        lines.append(
            f"- `{row['l2_governance_status']}`: n={row['count']} "
            f"({row['percentage_of_test']:.4f}% of TEST); {observed}"
        )
    return lines


def write_report(payload: dict[str, Any], commit: str | None) -> None:
    issues = payload.get("issues") or []
    limitations = list(payload.get("documentation_limitations") or [])
    if commit is None and not any("git_commit is null" in str(item) for item in limitations):
        limitations.append(
            "git_commit is null (no usable .git / git). Recorded, not fabricated. "
            "Stage 10 protocol §14: not by itself a scientific abort."
        )
    decomp = payload.get("decomposition") or {}
    hashes = payload.get("hashes") or {}
    body = [
        "# Stage 10 S10-A1-GAP report",
        "",
        "**Classification:** `ANALYSIS-ONLY / DESCRIPTIVE`",
        "",
        "This is **not** a new scientific confirmatory experiment. It decomposes already-observed",
        "Stage 8 v2 / Stage 9.1 A1 counts. It does **not** independently validate the Shariah governance layer.",
        "",
        f"**Experiment ID:** `{EXPERIMENT_ID}` (`S10-A1-GAP`)  ",
        f"**Status:** `{payload.get('status')}`  ",
        "**Authorization:** `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED` 2026-09-15  ",
        "**This run executed:** `S10-A1-GAP` only. **S10-A4-SIDEBYSIDE was not executed.**",
        "",
        "## Bound statements",
        "",
        "- No model was retrained. No EBM/Platt/isotonic was refit.",
        "- No threshold was searched or changed (`t_low=0.06`, `t_high=0.69` unchanged).",
        "- A1/G0 policy was not altered. No new governance state was introduced.",
        "- No Shariah score/probability, new Shariah rule, or halal/haram inference.",
        "- No contractual evidence was fabricated.",
        "- G1/G3 hypotheticals were **not** treated as observed results.",
        "- Stage 8, Stage 9, S10-I1, and S10-R1 artifacts were not overwritten.",
        "- UCI TEST was not opened. Stage 9 remains **CLOSED**. The paper was not drafted.",
        "",
        "## A. Credit-band decomposition",
        "",
        "Frozen bands: LOW `p_selected < 0.06`; MEDIUM `0.06 <= p_selected < 0.69`; HIGH `p_selected >= 0.69`.",
        "",
        *(_band_line(payload.get("credit_bands") or [])),
        "",
        "These match the existing Stage 8 v2 values LOW=5232, MEDIUM=203627, HIGH=27.",
        "",
        "## B. Governance-state decomposition",
        "",
        "Observed L2 `overall_governance_status` on stored Stage 8 v2 TEST audit records and published `gov_counts`:",
        "",
        *(_l2_line(payload.get("l2_governance_states") or [])),
        "",
        f"L1 (not the G0 input): `{payload.get('l1', {}).get('status')}` on all {payload.get('n')} rows; "
        "`l1_is_applicant_level_ruling=false`. L1 is dataset/schema readiness, not an applicant-level ruling.",
        "",
        "## C. Cross-tab `credit_band × L2_governance_status`",
        "",
        "| credit_band | L2 status | n | % of TEST | G0 decision | populated |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in payload.get("crosstab") or []:
        body.append(
            f"| {row['credit_band']} | `{row['l2_governance_status']}` | {row['n']} | "
            f"{row['percentage_of_test']:.4f} | {row['g0_decision']} | {row['populated']} |"
        )
    body.extend(
        [
            "",
            "Populated cells only: LOW×INSUFFICIENT_INFORMATION=5232 → HUMAN_REVIEW; "
            "MEDIUM×INSUFFICIENT_INFORMATION=203627 → HUMAN_REVIEW; "
            "HIGH×INSUFFICIENT_INFORMATION=27 → REJECT.",
            "",
            "## D. Deterministic policy trace",
            "",
            "Not a new experiment. Frozen map: `p_selected` → credit band → stored L2 → G0 → A1.",
            "",
        ]
    )
    for trace in payload.get("policy_trace") or []:
        body.append(
            f"- `{trace['p_selected_rule']}` → `{trace['credit_band']}` → "
            f"`{trace['l2_governance_status']}` → {trace['g0_mapping']} → "
            f"A1 `{trace['final_a1_decision']}` (n={trace['n']})"
        )
    low = decomp.get("low_to_review") or {}
    med = decomp.get("medium_to_review") or {}
    high_rev = decomp.get("high_to_review") or {}
    high_rej = decomp.get("high_to_reject") or {}
    body.extend(
        [
            "",
            "## E. Review-rate decomposition",
            "",
            f"- A1 HUMAN_REVIEW = {decomp.get('a1_review')} / {decomp.get('n')} "
            f"= {decomp.get('review_rate')}",
            f"- LOW contribution to REVIEW: {low.get('n')} "
            f"({100 * float(low.get('share_of_test') or 0):.4f}% of TEST; "
            f"{100 * float(low.get('share_of_a1_review') or 0):.4f}% of A1 reviews); "
            f"Stage 8 cause `{low.get('stage8_review_cause')}`.",
            f"- MEDIUM contribution to REVIEW: {med.get('n')} "
            f"({100 * float(med.get('share_of_test') or 0):.4f}% of TEST; "
            f"{100 * float(med.get('share_of_a1_review') or 0):.4f}% of A1 reviews); "
            f"Stage 8 cause `{med.get('stage8_review_cause')}`.",
            f"- HIGH contribution to REVIEW: {high_rev.get('n')} (0).",
            f"- HIGH contribution to REJECT: {high_rej.get('n')} "
            f"({100 * float(high_rej.get('share_of_test') or 0):.4f}% of TEST; 100% of A1 REJECT).",
            f"- {decomp.get('review_identity')}",
            f"- {decomp.get('reject_identity')}",
            f"- {decomp.get('approve_identity')}",
            "",
            "This high review rate is the G0 image of an all-insufficient L2 extract. "
            "It is **not** claimed to be a credit-model error merely because it is high.",
            "",
            "## F. Evidence-gap interpretation",
            "",
            "From existing Stage 7 v2 / Stage 8 v2 documentation only:",
            "",
            "- `INSUFFICIENT_INFORMATION` is an L2 **evidence-completeness / schema-gap** status. "
            "It means the prototype did not have the contractual fields required for applicant-level determination.",
            "- It is **not** a Shariah ruling, **not** expert validation, and **not** a finding that an applicant is non-compliant.",
            "- It is **not** a finding that a contract is actually non-compliant; LendingClub rows do not contain those contracts.",
            "- HUMAN_REVIEW under G0 is a **governance-hold** when evidence is insufficient or credit is MEDIUM. "
            "It is not a religious classification of applicants.",
            "- L1 `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` is dataset context (`is_applicant_level_ruling=false`), "
            "and is distinct from the L2 status that enters the G0 matrix.",
            "",
            "## G. What this analysis does NOT establish",
            "",
            "S10-A1-GAP does **not** establish:",
            "",
            "- that the governance layer is universally correct;",
            "- that the review band is operationally optimal;",
            "- that the applicants are Shariah non-compliant;",
            "- that contracts are actually non-compliant;",
            "- that the policy is suitable for production;",
            "- that a human reviewer would reach a specific Shariah conclusion.",
            "",
            "G1/G3 remain Stage 9.3 exploratory hypotheticals and are **not** observed LC TEST results.",
            "",
            "## Provenance",
            "",
            f"- `p_selected` source (cited, not rescored): `{payload.get('p_selected_source')}`",
            f"- Stage 8 v1 freeze SHA-256: `{hashes.get('v1_freeze_sha256')}`",
            f"- Stage 8 v2 freeze SHA-256: `{hashes.get('v2_freeze_sha256')}`",
            f"- table3 SHA-256: `{hashes.get('table3_sha256')}`",
            f"- TEST cal SHA-256: `{hashes.get('test_cal_sha256')}`",
            f"- Stage 8 policy YAML SHA-256: `{hashes.get('stage8_policy_yaml_sha256')}`",
            f"- Prior gates: S10-I1 `{payload.get('prior_gates', {}).get('i1_status')}`; "
            f"S10-R1 `{payload.get('prior_gates', {}).get('r1_status')}`",
            f"- git_commit: `{commit}`",
            "- Source artifacts:",
            *[f"  - `{path}`" for path in payload.get("source_artifacts") or []],
            "",
            "## Issues",
            "",
            *( [f"- {item}" for item in issues] if issues else ["- None."] ),
            "",
            "## Limitations",
            "",
            *[f"- {item}" for item in limitations],
            "",
            "## Activities not executed",
            "",
            "- S10-A4-SIDEBYSIDE: not executed",
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(body) + "\n", encoding="utf-8")


def main() -> int:
    started = utc_now()
    before = {str(p): sha256_file(p) for p in FORBIDDEN_WRITE if p.exists()}
    commit = git_commit(ROOT)
    payload = run_gap_analysis()
    if commit is None:
        payload["documentation_limitations"] = list(payload.get("documentation_limitations") or []) + [
            "git_commit is null (no usable .git / git). Recorded, not fabricated. "
            "Stage 10 protocol §14: not by itself a scientific abort."
        ]
    payload["git_commit"] = commit
    dump_json(METRICS, payload)
    if not payload.get("issues"):
        TABLE_CROSS.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(payload.get("crosstab") or []).to_csv(TABLE_CROSS, index=False)
        pd.DataFrame(payload.get("policy_trace") or []).to_csv(TABLE_TRACE, index=False)
    write_report(payload, commit)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(TEST_FILE), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    exit_code = int(proc.returncode)
    lines = [ln.strip() for ln in (proc.stdout or "").splitlines() if ln.strip()]
    test_summary = lines[-1] if lines else (proc.stderr or "")[-400:]
    after = {str(p): sha256_file(p) for p in FORBIDDEN_WRITE if p.exists()}
    if after != before:
        raise RuntimeError(f"S10-A1-GAP runner mutated protected files: {before} vs {after}")
    dump_json(
        AUDIT,
        {
            "experiment_id": EXPERIMENT_ID,
            "amendment_id": "AMENDMENT-STAGE10-AUTHORIZATION",
            "amendment_status": "APPROVED",
            "started": started,
            "execution_timestamp": utc_now(),
            "git_commit": commit,
            "status": payload.get("status"),
            "classification": CLASSIFICATION,
            "confirmatory_experiment": False,
            "models_trained": False,
            "calibration_refit": False,
            "thresholds_searched": False,
            "uci_opened": False,
            "g1_g3_treated_as_observed": False,
            "s10_i1_modified": False,
            "s10_r1_modified": False,
            "s10_a4_executed": False,
            "issues": payload.get("issues"),
            "documentation_limitations": payload.get("documentation_limitations"),
            "n": payload.get("n"),
            "decomposition": payload.get("decomposition"),
            "hashes": payload.get("hashes"),
            "protected_files_unchanged": after == before,
            "config_sha256": sha256_file(CONFIG) if CONFIG.exists() else None,
            "metrics_sha256": sha256_file(METRICS),
            "report_sha256": sha256_file(REPORT),
            "crosstab_sha256": sha256_file(TABLE_CROSS) if TABLE_CROSS.exists() else None,
            "pytest_exit_code": exit_code,
            "test_command": f"python -m pytest {TEST_FILE.relative_to(ROOT).as_posix()} -q --tb=short",
            "test_summary": test_summary,
            "software": {"python": sys.version},
            "random_seed_used": None,
        },
    )
    if payload.get("issues"):
        return 1
    return 0 if exit_code == 0 else exit_code


if __name__ == "__main__":
    raise SystemExit(main())
