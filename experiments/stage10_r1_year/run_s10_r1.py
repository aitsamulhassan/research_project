"""S10-R1-YEAR runner. Exploratory/descriptive post-hoc only. Does not edit authorization files."""

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
from stage10.s10_r1_year import CLASSIFICATION, EXPERIMENT_ID, json_safe, run_year_reanalysis  # noqa: E402

METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_r1_year.json"
TABLE_MIX = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_r1_year_decision_mix.csv"
TABLE_BANDS = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_r1_year_credit_bands.csv"
AUDIT = ROOT / "audit" / "stage10_s10_r1_year.json"
REPORT = ROOT / "docs" / "STAGE_10_S10_R1_YEAR_REPORT.md"
CONFIG = ROOT / "configs" / "stage10" / "s10_r1_year.yaml"
TEST_FILE = ROOT / "tests" / "test_stage10_r1_year.py"
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
    ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json",
    ROOT / "audit" / "stage10_i1_identity.json",
    ROOT / "docs" / "STAGE_10_S10_I1_IDENTITY_REPORT.md",
    ROOT / "src" / "stage10" / "s10_i1_identity.py",
    ROOT / "tests" / "test_stage10_i1_identity.py",
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


def _pct(block: dict[str, Any]) -> str:
    if block.get("percentage") is None:
        return "NA"
    return f"{block['percentage']:.4f}%"


def _fmt_slice_decisions(block: dict[str, Any]) -> str:
    return (
        f"APPROVE {block['APPROVE']['count']} ({_pct(block['APPROVE'])}); "
        f"HUMAN_REVIEW {block['HUMAN_REVIEW']['count']} ({_pct(block['HUMAN_REVIEW'])}); "
        f"REJECT {block['REJECT']['count']} ({_pct(block['REJECT'])})"
    )


def _fmt_bands(block: dict[str, Any]) -> str:
    parts = []
    for band in ("LOW", "MEDIUM", "HIGH"):
        row = block[band]
        parts.append(f"{band} {row['count']} ({_pct(row)})")
    return "; ".join(parts)


def write_report(payload: dict[str, Any], commit: str | None) -> None:
    issues = payload.get("issues") or []
    limitations = list(payload.get("documentation_limitations") or [])
    if commit is None and not any("git_commit is null" in str(item) for item in limitations):
        limitations.append(
            "git_commit is null (no usable .git / git). Recorded, not fabricated. "
            "Stage 10 protocol §14: not by itself a scientific abort."
        )
    issue_lines = [f"- {item}" for item in issues] if issues else ["- None."]
    limitation_lines = [f"- {item}" for item in limitations]
    by_year = payload.get("by_year") or {}
    y17 = by_year.get("2017")
    y18 = by_year.get("2018")
    body: list[str] = [
        "# Stage 10 S10-R1-YEAR report",
        "",
        "**Classification:** `EXPLORATORY / DESCRIPTIVE POST-HOC REANALYSIS — NON-CONFIRMATORY`",
        "",
        "This analysis is **not** a new confirmatory TEST-set experiment. LendingClub TEST was already unblinded in Stages 4B–8.",
        "Year slices describe frozen A0 / A1 / A3/A4 maps on stored `p_selected`. They are not used to choose a policy.",
        "",
        f"**Experiment ID:** `{EXPERIMENT_ID}` (`S10-R1-YEAR`)  ",
        f"**Status:** `{payload.get('status')}`  ",
        "**Authorization:** `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED` 2026-09-15  ",
        "**This run executed:** `S10-R1-YEAR` only.",
        "",
        "## Bound statements",
        "",
        "- No model was retrained.",
        "- No EBM was refit.",
        "- No calibration was refit.",
        "- No threshold was selected or changed, including year-specific thresholds.",
        "- A0, A1, and A3/A4 policies were not altered.",
        "- Shariah rules and governance evidence were not modified.",
        "- Year slices are **not** Shariah findings.",
        "- UCI TEST was not opened.",
        "- Stage 8, Stage 9, and S10-I1 artifacts were not overwritten.",
        "- S10-A1-GAP and S10-A4-SIDEBYSIDE were **not** executed.",
        "- Stage 9 remains **CLOSED**.",
        "- The paper was not drafted.",
        "",
        "## Interpretation rule",
        "",
        "Differences between 2017 and 2018 are reported as **descriptive temporal differences**,",
        "**year-specific decision allocation**, **observed difference in default prevalence**,",
        "or a **post-hoc temporal pattern**.",
        "",
        "This report does **not** call those differences model degradation, concept drift,",
        "calibration failure, policy failure, a causal effect, or evidence of generalization failure.",
        "No p-test of 2017 vs 2018 equality was computed.",
        "",
        "## Year derivation",
        "",
        "- Used the stored `year` column in `results/calibration/test/ebm_seed42_calibrated.csv`.",
        "- Did **not** parse `issue_d` or `issue_month` in this run.",
        "- Historically, Stage 5 stored `year` as `int(issue_month[0:4])`. That derivation was not repeated here.",
        "",
        "## Frozen inputs",
        "",
        f"- TEST n = {payload.get('n')}",
        f"- n_2017 = {payload.get('n_by_year', {}).get('2017')}; n_2018 = {payload.get('n_by_year', {}).get('2018')}",
        "- `p_selected` = stored Platt-calibrated probability (not recomputed)",
        "- `t_low=0.06`, `t_high=0.69`, `t*=0.16`",
        f"- S10-I1 status (gate): `{payload.get('s10_i1_status')}`",
        "",
    ]
    if y17 and y18:
        body.extend(
            [
                "## Dataset composition",
                "",
                f"- 2017: n={y17['composition']['n']}, defaults={y17['composition']['n_default']}, "
                f"default rate={y17['composition']['rate']:.6f} "
                f"(Wilson 95% CI {y17['composition']['wilson_ci_lower']:.6f}–{y17['composition']['wilson_ci_upper']:.6f})",
                f"- 2018: n={y18['composition']['n']}, defaults={y18['composition']['n_default']}, "
                f"default rate={y18['composition']['rate']:.6f} "
                f"(Wilson 95% CI {y18['composition']['wilson_ci_lower']:.6f}–{y18['composition']['wilson_ci_upper']:.6f})",
                "",
                "## A0 (frozen 0.06 / 0.69)",
                "",
                f"- 2017: {_fmt_slice_decisions(y17['A0'])}",
                f"- 2018: {_fmt_slice_decisions(y18['A0'])}",
                "",
                "## A1 (same credit bands, frozen G0 INSUFFICIENT_INFORMATION)",
                "",
                f"- 2017: {_fmt_slice_decisions(y17['A1'])}",
                f"- 2018: {_fmt_slice_decisions(y18['A1'])}",
                "",
                "## A3/A4 (frozen t*=0.16, no HUMAN_REVIEW branch)",
                "",
                f"- 2017: {_fmt_slice_decisions(y17['A3_A4'])}",
                f"- 2018: {_fmt_slice_decisions(y18['A3_A4'])}",
                "",
                "## Credit-band distribution (frozen 0.06 / 0.69)",
                "",
                f"- 2017: {_fmt_bands(y17['credit_bands'])}",
                f"- 2018: {_fmt_bands(y18['credit_bands'])}",
                "",
                "## Descriptive default rate by A0 credit band",
                "",
                "Evaluation only. Not used to tune a threshold or policy.",
                "",
            ]
        )
        for year_label, slice_ in (("2017", y17), ("2018", y18)):
            for band in ("LOW", "MEDIUM", "HIGH"):
                row = slice_["credit_bands"][band]
                if row["count"] == 0:
                    body.append(f"- {year_label} {band}: n=0 (no default rate).")
                else:
                    body.append(
                        f"- {year_label} {band}: n={row['count']}, defaults={row['n_default']}, "
                        f"default rate={row['default_rate']:.6f} "
                        f"(Wilson 95% CI {row['default_rate_wilson_ci_lower']:.6f}–{row['default_rate_wilson_ci_upper']:.6f})"
                    )
        body.extend(["", "## Descriptive notes", ""])
        body.extend([f"- {note}" for note in payload.get("descriptive_notes") or []])
    body.extend(
        [
            "",
            "## Provenance",
            "",
            f"- Probability file: `{payload.get('probability_file')}`",
            f"- TEST cal SHA-256: `{payload.get('hashes', {}).get('results/calibration/test/ebm_seed42_calibrated.csv')}`",
            f"- Stage 8 v2 freeze SHA-256: `{payload.get('hashes', {}).get('results/decision/v2/frozen_policy.json')}`",
            f"- table3 SHA-256: `{payload.get('hashes', {}).get('results/decision/v2/tables/table3_test_decision_outcomes.csv')}`",
            "- EBM/Platt joblib files were **not** loaded.",
            "- `p_selected` was **not** recomputed from `p_raw`.",
            f"- random_seed_used: `{payload.get('random_seed_used')}` (none). Stored prediction seed in the CSV: 42.",
            f"- git_commit: `{commit}`",
            "",
            "## Issues",
            "",
            *issue_lines,
            "",
            "## Limitations",
            "",
            *limitation_lines,
            "",
            "## Activities not executed",
            "",
            "- S10-A1-GAP: not executed",
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
    payload = run_year_reanalysis()
    if commit is None:
        payload["documentation_limitations"] = list(payload.get("documentation_limitations") or []) + [
            "git_commit is null (no usable .git / git). Recorded, not fabricated. "
            "Stage 10 protocol §14: not by itself a scientific abort."
        ]
    payload["git_commit"] = commit
    dump_json(METRICS, payload)
    if not payload.get("issues") and payload.get("decision_mix_rows"):
        TABLE_MIX.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(payload["decision_mix_rows"]).to_csv(TABLE_MIX, index=False)
        pd.DataFrame(payload["credit_band_rows"]).to_csv(TABLE_BANDS, index=False)
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
        raise RuntimeError(f"S10-R1 runner mutated protected files: {before} vs {after}")
    audit = {
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
        "models_loaded_for_scoring": False,
        "calibration_refit": False,
        "thresholds_searched": False,
        "year_specific_threshold": False,
        "uci_opened": False,
        "stage8_9_results_modified": False,
        "s10_i1_modified": False,
        "s10_a1_gap_executed": False,
        "s10_a4_executed": False,
        "issues": payload.get("issues"),
        "documentation_limitations": payload.get("documentation_limitations"),
        "n": payload.get("n"),
        "n_by_year": payload.get("n_by_year"),
        "hashes": payload.get("hashes"),
        "year_derivation": payload.get("year_derivation"),
        "thresholds": payload.get("thresholds"),
        "protected_files_unchanged": after == before,
        "config_sha256": sha256_file(CONFIG) if CONFIG.exists() else None,
        "metrics_sha256": sha256_file(METRICS),
        "report_sha256": sha256_file(REPORT),
        "table_mix_sha256": sha256_file(TABLE_MIX) if TABLE_MIX.exists() else None,
        "table_bands_sha256": sha256_file(TABLE_BANDS) if TABLE_BANDS.exists() else None,
        "pytest_exit_code": exit_code,
        "test_command": f"python -m pytest {TEST_FILE.relative_to(ROOT).as_posix()} -q --tb=short",
        "test_summary": test_summary,
        "software": {"python": sys.version},
        "random_seed_used": None,
        "stored_prediction_seed": 42,
    }
    dump_json(AUDIT, audit)
    if payload.get("issues"):
        return 1
    return 0 if exit_code == 0 else exit_code


if __name__ == "__main__":
    raise SystemExit(main())
