"""Stage 9.3 governance sensitivity from published Stage 8 v2 band counts. No Stage 9.4+."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from decision.stage9_1 import sha256_file  # noqa: E402
from decision.stage9_3 import (  # noqa: E402
    CERTIFICATION_CLAIM,
    EXPERIMENT_ID,
    EXPERT_VALIDATION,
    PROTOCOL_ID,
    PROTOCOL_SECTION,
    STAGE7_L1L2_VERSION,
    assemble_governance_sensitivity,
    stage8_guard_paths,
    stage91_guard_paths,
    stage92_guard_paths,
)


def _save(fig, path_stem: Path) -> None:
    path_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path_stem.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def git_commit(root: Path) -> str | None:
    try:
        proc = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, capture_output=True, text=True)
        if proc.returncode == 0:
            text = proc.stdout.strip()
            return text or None
    except OSError:
        return None
    return None


OUT = ROOT / "results" / "governance_sensitivity" / "v1"
FIG = ROOT / "results" / "figures" / "governance_sensitivity" / "v1"
TAB = OUT / "tables"
AUDIT = ROOT / "audit" / "stage9_3_governance_sensitivity_run.json"
REPORT = ROOT / "docs" / "STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md"
CONFIG = ROOT / "configs" / "stage9_3_governance_sensitivity.yaml"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8")


def json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return json_safe(obj.tolist())
    if isinstance(obj, (np.floating, float)):
        value = float(obj)
        return None if not np.isfinite(value) else value
    if isinstance(obj, (np.integer, int)) and not isinstance(obj, bool):
        return int(obj)
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    return obj


def fmt(value: Any, digits: int = 6) -> str:
    if value is None or (isinstance(value, float) and not np.isfinite(value)):
        return "NA"
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.{digits}f}"
    return str(value)


def pct(rate: float) -> str:
    return f"{100.0 * float(rate):.4f}%"


def figure_decision_allocation(scenarios: dict[str, Any], path_stem: Path) -> None:
    labels = ["G0 observed", "G1 hypothetical", "G3 hypothetical"]
    keys = ["G0", "G1", "G3"]
    approve = [scenarios[k]["APPROVE"] for k in keys]
    review = [scenarios[k]["HUMAN_REVIEW"] for k in keys]
    reject = [scenarios[k]["REJECT"] for k in keys]
    x = np.arange(len(labels))
    w = 0.25
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(x - w, approve, w, label="APPROVE", color="#c6efce")
    ax.bar(x, review, w, label="HUMAN_REVIEW", color="#fff2cc")
    ax.bar(x + w, reject, w, label="REJECT", color="#f4cccc")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Applications (published Stage 8 v2 band counts)")
    ax.set_title("Stage 9.3. Decision-layer allocation under G0/G1/G3")
    ax.legend(frameon=False)
    fig.tight_layout()
    _save(fig, path_stem)


def figure_rates(scenarios: dict[str, Any], path_stem: Path) -> None:
    metrics = ["approval_rate", "review_rate", "rejection_rate"]
    pretty = ["Approval", "Human review", "Rejection"]
    x = np.arange(len(metrics))
    w = 0.25
    fig, ax = plt.subplots(figsize=(7.6, 4.4))
    ax.bar(x - w, [scenarios["G0"][m] for m in metrics], w, label="G0 observed", color="#4c78a8")
    ax.bar(x, [scenarios["G1"][m] for m in metrics], w, label="G1 hypothetical", color="#e45756")
    ax.bar(x + w, [scenarios["G3"][m] for m in metrics], w, label="G3 hypothetical", color="#72b7b2")
    ax.set_xticks(x)
    ax.set_xticklabels(pretty)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Share of n = 208,886")
    ax.set_title("Stage 9.3. Decision rates (engineering sensitivity)")
    ax.legend(frameon=False)
    fig.tight_layout()
    _save(fig, path_stem)


def write_report(payload: dict[str, Any]) -> None:
    s = payload["scenarios"]
    p = payload["published"]
    lines = [
        "# Stage 9.3 Governance Sensitivity Report",
        "",
        "LendingClub TEST was already exposed during Stages 4B–8. Stage 9.3 did not use TEST data to select a governance scenario, threshold, or policy. G0 cites stored Stage 8 v2 fused counts. G1 and G3 are algebraic illustrations from already published credit-band counts. They are labeled derived commentary, not a new TEST evaluation.",
        "",
        f"**Status:** `STAGE_9_3_STATUS = {payload['status']}`",
        "",
        "```text",
        "STAGE_9_4+ = NOT EXECUTED",
        "G-unsafe = NOT_EXECUTED — NOT_AUTHORIZED",
        "```",
        "",
        "## 1. Objective",
        "",
        "Describe how the **decision layer** allocation would change if the governance-state input supplied to the frozen fusion policy were treated differently. This is an engineering sensitivity analysis. It is not a religious ruling, not a compliance test, and not a ranking of which state is more appropriate as a religious judgment.",
        "",
        "## 2. Relationship to Stage 9.0 freeze",
        "",
        f"Controlling freeze: `audit/stage9_0_experimental_freeze.json`; protocol `{PROTOCOL_ID}` §{PROTOCOL_SECTION}.",
        "",
        "- O-G: G0 remains primary; G1 and G3 are hypothetical engineering sensitivities.",
        "- O-TEST Option A: no additional LC TEST policy remaps. Stage 9.3 does not rewrite Stage 8 outputs and does not apply G1/G3 as a new stored TEST policy.",
        "- Arithmetic from already published Stage 8 v2 band counts is the authorized illustration method.",
        "- G-unsafe (treat insufficiency as PASS) is not a candidate policy and was not executed.",
        "- Stage 8 thresholds remain `t_low=0.06`, `t_high=0.69`. The G0 matrix is not altered in Stage 8.",
        "",
        "## 3. Governance-state definitions",
        "",
        "G1 and G3 change **only** the `INSUFFICIENT_INFORMATION` row of the frozen Stage 8 matrix. PASS / REVIEW / `NOT_STRUCTURABLE_WITHOUT_REDESIGN` cells remain the G0 cells.",
        "",
        "| ID | Role | Treatment of `INSUFFICIENT_INFORMATION` |",
        "| --- | --- | --- |",
        "| G0 | Primary / observed | LOW → HUMAN_REVIEW; MEDIUM → HUMAN_REVIEW; HIGH → REJECT |",
        "| G1 | Hypothetical engineering | LOW → REJECT; MEDIUM → REJECT; HIGH → REJECT |",
        "| G3 | Hypothetical engineering | LOW → HUMAN_REVIEW; MEDIUM → HUMAN_REVIEW; HIGH → HUMAN_REVIEW |",
        "",
        "The remainder of the frozen G0 matrix (unchanged in G1/G3) is:",
        "",
        "| Governance status | LOW | MEDIUM | HIGH |",
        "| --- | --- | --- | --- |",
        "| `NOT_STRUCTURABLE_WITHOUT_REDESIGN` | REJECT | REJECT | REJECT |",
        "| `REVIEW` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |",
        "| `PASS` | APPROVE | HUMAN_REVIEW | REJECT |",
        "",
        "## 4. G0 observed evidence state",
        "",
        "LendingClub L2 on the stored Stage 8 v2 TEST fusion is `INSUFFICIENT_INFORMATION` for every application (208,886 / 208,886). That is an **observed governance evidence state**: insufficient contractual evidence for an application-level Shariah-oriented determination. It is not a religious classification of applicants.",
        "",
        f"L1 remains `{p['l1_status']}` (dataset context, not an applicant-level ruling). L2 evaluation_mode remains `{p['l2_evaluation_mode']}`. Stage 7 version: `{p['stage7_v2']}`.",
        "",
        "G0 decision counts are the stored Stage 8 v2 fused result, confirmed by applying the frozen G0 `INSUFFICIENT_INFORMATION` row to the published credit-band counts.",
        "",
        "## 5. Hypothetical G1/G3 scenarios",
        "",
        "G1 and G3 are **hypothetical engineering scenarios**. They are not observed evidence states, not expert-validated statuses, and not evidence that a real financing application should receive those treatments. They ask only: if the frozen fusion policy treated `INSUFFICIENT_INFORMATION` as all-REJECT (G1) or all-HUMAN_REVIEW including HIGH (G3), how would the published band counts allocate?",
        "",
        "They are not ranked. Neither is selected as a replacement for G0.",
        "",
        "## 6. Experimental controls",
        "",
        "- Same published sample n = 208,886.",
        "- Same frozen credit bands: LOW 5,232; MEDIUM 203,627; HIGH 27.",
        "- Same frozen thresholds `0.06 / 0.69`.",
        "- Same observed L2 input `INSUFFICIENT_INFORMATION` for all rows.",
        "- Only the authorized `INSUFFICIENT_INFORMATION` treatment differs.",
        "- Credit model, calibration, and Stage 7 rule inventory are not called.",
        "- Predictive metrics are not recomputed: governance sensitivity is a decision-layer analysis.",
        "- Stage 9.2 cost analysis is not repeated and is not used to choose a scenario.",
        "",
        "## 7. Decision-allocation results",
        "",
        "| Scenario | Role | APPROVE | HUMAN_REVIEW | REJECT | Approval rate | Review rate | Rejection rate |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
        f"| G0 | observed / primary | {s['G0']['APPROVE']} | {s['G0']['HUMAN_REVIEW']} | {s['G0']['REJECT']} | {pct(s['G0']['approval_rate'])} | {pct(s['G0']['review_rate'])} | {pct(s['G0']['rejection_rate'])} |",
        f"| G1 | hypothetical | {s['G1']['APPROVE']} | {s['G1']['HUMAN_REVIEW']} | {s['G1']['REJECT']} | {pct(s['G1']['approval_rate'])} | {pct(s['G1']['review_rate'])} | {pct(s['G1']['rejection_rate'])} |",
        f"| G3 | hypothetical | {s['G3']['APPROVE']} | {s['G3']['HUMAN_REVIEW']} | {s['G3']['REJECT']} | {pct(s['G3']['approval_rate'])} | {pct(s['G3']['review_rate'])} | {pct(s['G3']['rejection_rate'])} |",
        "",
        "Band-level mapping under the observed L2 input:",
        "",
        "| Band | n | G0 | G1 | G3 |",
        "| --- | ---: | --- | --- | --- |",
        f"| LOW | {p['band_counts']['LOW']} | HUMAN_REVIEW | REJECT | HUMAN_REVIEW |",
        f"| MEDIUM | {p['band_counts']['MEDIUM']} | HUMAN_REVIEW | REJECT | HUMAN_REVIEW |",
        f"| HIGH | {p['band_counts']['HIGH']} | REJECT | REJECT | HUMAN_REVIEW |",
        "",
        "G0’s large HUMAN_REVIEW rate is preserved. It is not “fixed.”",
        "",
        "## 8. Interpretation",
        "",
        "This is **decision-layer sensitivity** to the treatment of evidence insufficiency, holding credit bands fixed.",
        "",
        "- Under G0, HIGH credit risk still REJECT (27 applications); LOW and MEDIUM go to HUMAN_REVIEW because contractual evidence is insufficient.",
        "- Under hypothetical G1, the same insufficiency treatment sends every published band to REJECT, so review rate is 0 and rejection rate is 1.",
        "- Under hypothetical G3, even HIGH is held in HUMAN_REVIEW, so rejection rate is 0 and review rate is 1.",
        "- None of these allocations is a statement about economic optimality. Stage 9.2 is not reused to pick a winner.",
        "",
        "A governance layer that refuses to infer contractual status from generic credit/application data can substantially constrain automated decisions when contractual evidence is absent. That is an evidence-gap property of the observed schema, not a demonstration that the architecture is economically superior.",
        "",
        "## 9. Shariah-interpretation boundary",
        "",
        "This experiment does **not** produce a religious score, religious probability, religious ranking, or religious accuracy. It does not classify purpose, FICO, or demographics as contractual evidence. It does not claim that G0, G1, or G3 is the religiously correct treatment. Expert validation remains `NONE_EXPERT_VALIDATED`. `certification_claim=false`.",
        "",
        "G1 must not be read as “these applications are non-compliant.” G3 must not be read as “these applications should be approved after review as compliant.” Both are engineering counterfactuals about how a frozen matrix cell could be filled.",
        "",
        "## 10. Limitations",
        "",
        "- G1/G3 are not observed L2 statuses on LendingClub.",
        "- No reviewer outcomes exist; HUMAN_REVIEW is a simulated policy band.",
        "- Algebra from published band counts does not create new per-row TEST audit records (O-TEST Option A).",
        "- The analysis cannot say which scenario a bank or board should adopt.",
        "",
        "## 11. Leakage / selection statement",
        "",
        "LendingClub TEST was already exposed during Stages 4B–8. Stage 9.3 did not use TEST outcomes to choose G0, G1, or G3. No threshold was searched. No scenario was selected as best. G0 remains the pre-declared primary from Stage 8 / Stage 9.0.",
        "",
        "## 12. Reproducibility",
        "",
        f"- experiment_id: `{EXPERIMENT_ID}`",
        f"- protocol: `{PROTOCOL_ID}` §{PROTOCOL_SECTION}",
        f"- Stage 7 governance version: `{STAGE7_L1L2_VERSION}`",
        f"- Stage 8 v1 freeze sha256: `{payload['integrity']['v1_freeze_sha256']}`",
        f"- config: `{CONFIG.relative_to(ROOT).as_posix()}`",
        f"- script: `experiments/stage9_3_governance_sensitivity/run_stage9_3.py`",
        f"- execution_timestamp: `{payload['execution_timestamp']}`",
        f"- git_commit: `{payload['git_commit']}`",
        f"- expert_validation: `{EXPERT_VALIDATION}`",
        f"- certification_claim: `{CERTIFICATION_CLAIM}`",
        f"- test command: `{payload['test_command']}`",
        f"- test summary: `{payload['test_summary']}`",
        "",
        "## 13. Conclusion",
        "",
        "G0 remains the only observed, data-supported governance evidence state on this LendingClub extract: `INSUFFICIENT_INFORMATION`, producing a near-universal HUMAN_REVIEW allocation under the frozen matrix. Hypothetical G1 collapses that allocation to all REJECT; hypothetical G3 collapses it to all HUMAN_REVIEW. Those are engineering sensitivities to one matrix row. They are not religious findings. Stage 9.4+ were not executed.",
        "",
        "## Artifact index",
        "",
    ]
    for path in payload["artifact_paths"]:
        lines.append(f"- `{path}`")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    started = utc_now()
    guard_paths = stage8_guard_paths() + stage91_guard_paths() + stage92_guard_paths()
    hashes_before = {p.as_posix(): sha256_file(p) for p in guard_paths}
    assembled = assemble_governance_sensitivity()
    OUT.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CONFIG, OUT / "stage9_3_governance_sensitivity.yaml")
    scenarios = assembled["scenarios"]
    rows = []
    for key in ("G0", "G1", "G3"):
        row = scenarios[key]
        rows.append(
            {
                "scenario": key,
                "role": row["role"],
                "governance_status_input": row["governance_status_input"],
                "n": row["n"],
                "n_approve": row["APPROVE"],
                "n_human_review": row["HUMAN_REVIEW"],
                "n_reject": row["REJECT"],
                "approval_rate": row["approval_rate"],
                "review_rate": row["review_rate"],
                "rejection_rate": row["rejection_rate"],
                "source": row["source"],
            }
        )
    pd.DataFrame(rows).to_csv(TAB / "table1_governance_scenario_allocation.csv", index=False)
    band_rows = []
    for band, n_band in assembled["published"]["band_counts"].items():
        band_rows.append(
            {
                "credit_band": band,
                "n": n_band,
                "G0": scenarios["G0"]["by_band"][band]["decision"],
                "G1": scenarios["G1"]["by_band"][band]["decision"],
                "G3": scenarios["G3"]["by_band"][band]["decision"],
            }
        )
    pd.DataFrame(band_rows).to_csv(TAB / "table2_band_mapping_by_scenario.csv", index=False)
    figure_decision_allocation(scenarios, FIG / "figure1_decision_counts")
    figure_rates(scenarios, FIG / "figure2_decision_rates")
    dump_json(
        OUT / "metrics" / "governance_sensitivity_summary.json",
        json_safe(
            {
                "experiment_id": EXPERIMENT_ID,
                "used_for_selection": False,
                "models_trained": False,
                "models_loaded": False,
                "calibration_refit": False,
                "new_shariah_rules_added": False,
                "expert_validation": EXPERT_VALIDATION,
                "certification_claim": CERTIFICATION_CLAIM,
                "observed_l2": assembled["observed_l2"],
                "g_unsafe_status": assembled["g_unsafe_status"],
                "integrity": assembled["integrity"],
                "published": assembled["published"],
                "scenarios": scenarios,
                "other_governance_statuses_unchanged": assembled["other_governance_statuses_unchanged"],
            }
        ),
    )
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests" / "test_stage9_3_governance_sensitivity.py"), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    pytest_text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    summary_line = next((line.strip() for line in reversed(pytest_text.splitlines()) if "passed" in line), pytest_text[-400:])
    hashes_after = {p.as_posix(): sha256_file(p) for p in guard_paths}
    issues: list[str] = []
    if proc.returncode != 0:
        issues.append(f"pytest failed: {summary_line}")
    if hashes_after != hashes_before:
        issues.append("Stage 7/8/9.1/9.2 artifact mutated during Stage 9.3.")
    if scenarios["G0"]["HUMAN_REVIEW"] != 208859:
        issues.append("G0 HUMAN_REVIEW drifted from Stage 8 v2.")
    if scenarios["G1"]["REJECT"] != 208886:
        issues.append("G1 is not all REJECT on the observed L2 state.")
    if scenarios["G3"]["HUMAN_REVIEW"] != 208886:
        issues.append("G3 is not all HUMAN_REVIEW on the observed L2 state.")
    status = "PASS" if not issues else "BLOCKED"
    execution_timestamp = utc_now()
    artifact_paths = [
        "docs/STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md",
        "audit/stage9_3_governance_sensitivity_run.json",
        "results/governance_sensitivity/v1/stage9_3_governance_sensitivity.yaml",
        "results/governance_sensitivity/v1/tables/table1_governance_scenario_allocation.csv",
        "results/governance_sensitivity/v1/tables/table2_band_mapping_by_scenario.csv",
        "results/governance_sensitivity/v1/metrics/governance_sensitivity_summary.json",
        "results/figures/governance_sensitivity/v1/figure1_decision_counts.png",
        "results/figures/governance_sensitivity/v1/figure2_decision_rates.png",
    ]
    audit = {
        "experiment_id": EXPERIMENT_ID,
        "amendment_id": "AMENDMENT-SHARIAH-001",
        "protocol_id": PROTOCOL_ID,
        "protocol_section": PROTOCOL_SECTION,
        "started": started,
        "execution_timestamp": execution_timestamp,
        "git_commit": git_commit(ROOT),
        "status": status,
        "issues": issues,
        "stage7_governance_version": STAGE7_L1L2_VERSION,
        "g0_definition": scenarios["G0"]["definition"],
        "g1_definition": scenarios["G1"]["definition"],
        "g3_definition": scenarios["G3"]["definition"],
        "g_unsafe_status": assembled["g_unsafe_status"],
        "n": assembled["published"]["n"],
        "frozen_thresholds": {"t_low": 0.06, "t_high": 0.69},
        "credit_band_counts": assembled["published"]["band_counts"],
        "governance_state_counts": assembled["published"]["gov_counts"],
        "final_decision_counts": {
            key: {k: scenarios[key][k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")} for key in ("G0", "G1", "G3")
        },
        "stage8_policy_hash": assembled["integrity"]["v1_freeze_sha256"],
        "models_loaded": False,
        "models_trained": False,
        "calibration_refit": False,
        "test_used_for_selection": False,
        "stage8_modified": False,
        "new_shariah_rules_added": False,
        "expert_validation": EXPERT_VALIDATION,
        "certification_claim": CERTIFICATION_CLAIM,
        "stage9_4_plus_executed": False,
        "integrity": assembled["integrity"],
        "config_sha256": sha256_file(CONFIG),
        "guard_hashes": hashes_after,
        "pytest_exit_code": proc.returncode,
        "test_command": "python -m pytest tests/test_stage9_3_governance_sensitivity.py -q --tb=short",
        "test_summary": summary_line,
        "software": {"python": sys.version.replace("\n", " "), "pandas": pd.__version__, "numpy": np.__version__},
    }
    dump_json(AUDIT, json_safe(audit))
    write_report(
        {
            "status": status,
            "scenarios": scenarios,
            "published": assembled["published"],
            "integrity": assembled["integrity"],
            "execution_timestamp": execution_timestamp,
            "git_commit": git_commit(ROOT),
            "test_command": "python -m pytest tests/test_stage9_3_governance_sensitivity.py -q --tb=short",
            "test_summary": summary_line,
            "artifact_paths": artifact_paths,
        }
    )
    print(
        json.dumps(
            {
                "status": status,
                "G0": {k: scenarios["G0"][k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")},
                "G1": {k: scenarios["G1"][k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")},
                "G3": {k: scenarios["G3"][k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")},
                "g_unsafe": assembled["g_unsafe_status"],
            },
            indent=2,
        ),
        flush=True,
    )
    if proc.returncode != 0:
        print(pytest_text[-2000:], flush=True)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
