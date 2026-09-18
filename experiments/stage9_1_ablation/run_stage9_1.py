"""Stage 9.1 ablation report from frozen Stage 8 artifacts. No retraining. No Stage 9.2+."""

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

from decision.stage9_1 import (  # noqa: E402
    EXPERIMENT_ID,
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    EXPECTED_T_STAR,
    V1_FREEZE,
    V2_TABLE3,
    consistency_check_stored_probabilities,
    load_stored_ablation,
    sha256_file,
    verify_frozen_artifacts,
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

OUT = ROOT / "results" / "ablation" / "v1"
FIG = ROOT / "results" / "figures" / "ablation" / "v1"
TAB = OUT / "tables"
AUDIT = ROOT / "audit" / "stage9_1_ablation_run.json"
REPORT = ROOT / "docs" / "STAGE_9_1_ABLATION_REPORT.md"
CONFIG = ROOT / "configs" / "stage9_1_ablation.yaml"
V8_REPORT = ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md"
V8_FREEZE = ROOT / "results" / "decision" / "frozen_policy.json"


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


def figure_decision_distribution(systems: dict[str, Any], path_stem: Path) -> None:
    labels = ["A0 credit-only", "A1 proposed", "A3/A4 binary"]
    keys = ["A0", "A1", "A3_A4"]
    approve = [systems[k]["APPROVE"] for k in keys]
    review = [systems[k]["HUMAN_REVIEW"] for k in keys]
    reject = [systems[k]["REJECT"] for k in keys]
    x = np.arange(len(labels))
    w = 0.25
    fig, ax = plt.subplots(figsize=(8.4, 4.6))
    ax.bar(x - w, approve, w, label="APPROVE", color="#c6efce")
    ax.bar(x, review, w, label="HUMAN_REVIEW", color="#fff2cc")
    ax.bar(x + w, reject, w, label="REJECT", color="#f4cccc")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Applications (TEST, previously exposed)")
    ax.set_title("Stage 9.1. Decision counts under frozen policies")
    ax.legend(frameon=False)
    fig.tight_layout()
    _save(fig, path_stem)


def figure_a1_default_by_band(rows: list[dict[str, Any]], path_stem: Path) -> None:
    order = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    rows = sorted(rows, key=lambda r: order.get(str(r["band"]), 9))
    names = [r["band"] for r in rows]
    rates = [r["default_rate"] for r in rows]
    lo = [r["default_rate"] - r["default_rate_ci_lower"] for r in rows]
    hi = [r["default_rate_ci_upper"] - r["default_rate"] for r in rows]
    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ax.bar(names, rates, color="#1f77b4", yerr=np.vstack([lo, hi]), capsize=4)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Observed default rate")
    ax.set_xlabel("A1 credit-risk band (frozen t_low=0.06, t_high=0.69)")
    ax.set_title("Stage 9.1. A1 credit bands vs default rate (Wilson 95% CI)")
    fig.tight_layout()
    _save(fig, path_stem)


def figure_a1_vs_a3_rates(systems: dict[str, Any], path_stem: Path) -> None:
    metrics = ["approval_rate", "review_rate", "rejection_rate"]
    pretty = ["Approval", "Human review", "Rejection"]
    a1 = [systems["A1"][m] for m in metrics]
    a3 = [systems["A3_A4"][m] for m in metrics]
    x = np.arange(len(metrics))
    w = 0.35
    fig, ax = plt.subplots(figsize=(7.2, 4.4))
    ax.bar(x - w / 2, a1, w, label="A1 proposed (G0)", color="#e2d5f1")
    ax.bar(x + w / 2, a3, w, label="A3/A4 binary t*=0.16", color="#cce5ff")
    ax.set_xticks(x)
    ax.set_xticklabels(pretty)
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Share of previously exposed TEST")
    ax.set_title("Stage 9.1. A1 vs A3/A4 policy rates")
    ax.legend(frameon=False)
    fig.tight_layout()
    _save(fig, path_stem)


def write_report(payload: dict[str, Any]) -> None:
    s = payload["systems"]
    pred = payload["predictive"]
    lines = [
        "# Stage 9.1 Ablation / Comparator Report",
        "",
        "LendingClub TEST was already exposed during Stages 4B–8. Stage 9.1 did not use TEST data for model or policy selection. The analysis is a controlled ablation/re-analysis of frozen artifacts and previously exposed TEST outputs.",
        "",
        f"**Status:** `STAGE_9_1_STATUS = {payload['status']}`",
        "",
        "```text",
        "STAGE_9_2+ = NOT EXECUTED",
        "STAGE_9_EXECUTION = AUTHORIZED FOR STAGE 9.1 ONLY",
        "```",
        "",
        "## 1. Objective",
        "",
        "Compare the frozen evidence-separated decision architecture (A1) with the frozen credit-only three-way policy (A0) and the frozen binary monolithic comparator (A3/A4), without retraining, without threshold search, and without changing Stage 8.",
        "",
        "## 2. Research question linkage",
        "",
        "> Does separating credit-risk scoring, explainability, and Shariah-oriented governance into independently validated and auditable evidence layers, fused only at the final decision stage, provide a more transparent and defensible digital-financing pipeline than a monolithic end-to-end classifier without materially sacrificing predictive performance?",
        "",
        "The monolithic comparator is the Stage 8 single-threshold credit policy (`t*=0.16`) on the same frozen Platt-calibrated EBM. It is not a neural Shariah classifier. Predictive scores are identical across A0/A1/A3; only the decision map changes.",
        "",
        "## 3. Exact definitions",
        "",
        "| ID | Definition | HUMAN_REVIEW | Governance | Role |",
        "| --- | --- | --- | --- | --- |",
        "| A0 | `p_selected < 0.06` APPROVE; `0.06 <= p < 0.69` HUMAN_REVIEW; `p >= 0.69` REJECT | Yes (credit MEDIUM) | None | Credit-only ablation |",
        "| A1 | Same credit bands, fused with Stage 7 v2 L2 under G0 | Yes (credit and/or governance) | G0 primary | **Proposed architecture** |",
        "| A3 | `p_selected < 0.16` APPROVE; `p_selected >= 0.16` REJECT | No | None | Binary comparator/ablation |",
        "| A4 | Same as A3 under the Stage 9.0 freeze | No | None | Collapses to A3 |",
        "",
        "A3 and A4 collapse to the same frozen binary monolithic credit-policy comparator under the Stage 9.0 freeze. They are reported once.",
        "",
        "## 4. Frozen artifacts used",
        "",
        f"- Stage 8 v1 freeze: `{V1_FREEZE.relative_to(ROOT).as_posix()}` sha256 `{payload['integrity']['v1_freeze_sha256']}`",
        f"- Stage 8 v2 table: `{V2_TABLE3.relative_to(ROOT).as_posix()}`",
        f"- t_low={EXPECTED_T_LOW}, t_high={EXPECTED_T_HIGH}, t*={EXPECTED_T_STAR}",
        f"- Platt a={payload['integrity']['platt_a']}, b={payload['integrity']['platt_b']}",
        f"- EBM joblib sha256 `{payload['integrity']['ebm_joblib_sha256']}` (not loaded for scoring)",
        "",
        "## 5. Data/split provenance",
        "",
        "- Dataset: LendingClub granting extract, split = TEST (`issue_month >= 2017-02`), n = 208,886.",
        "- Probabilities: stored `p_selected` from Stage 5 Platt, seed 42.",
        "- Labels: stored `y_true` already used in Stage 8 policy tables; not used here for selection.",
        "",
        "## 6. TEST protection statement",
        "",
        "LendingClub TEST was already exposed during Stages 4B–8. Stage 9.1 did not use TEST data for model or policy selection. The analysis is a controlled ablation/re-analysis of frozen artifacts and previously exposed TEST outputs.",
        "",
        f"Consistency check (A0/A3 maps re-applied to stored `p_selected`): `{payload['consistency']['label']}`; used_for_selection=`{payload['consistency']['used_for_selection']}`; a0_match=`{payload['consistency']['a0_match']}`; a3_match=`{payload['consistency']['a3_match']}`.",
        "",
        "## 7. Decision-policy definitions",
        "",
        "A1 retains HUMAN_REVIEW. G0 maps L2 `INSUFFICIENT_INFORMATION` + LOW/MEDIUM → HUMAN_REVIEW and HIGH → REJECT. No Shariah score is created. Governance outputs are not fed into the credit model.",
        "",
        "## 8. Results",
        "",
        "A1 counts are the Stage 8 v2 fused TEST result, confirmed against the stored table. They are not a newly discovered TEST result.",
        "",
        "| System | Credit policy | Governance | APPROVE | HUMAN_REVIEW | REJECT | Review burden | Notes |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | --- |",
        f"| A0 | frozen three-way 0.06/0.69 | none | {s['A0']['APPROVE']} ({pct(s['A0']['approval_rate'])}) | {s['A0']['HUMAN_REVIEW']} ({pct(s['A0']['review_rate'])}) | {s['A0']['REJECT']} ({pct(s['A0']['rejection_rate'])}) | {pct(s['A0']['review_burden'])} | credit-only |",
        f"| A1 | frozen three-way 0.06/0.69 | G0 | {s['A1']['APPROVE']} ({pct(s['A1']['approval_rate'])}) | {s['A1']['HUMAN_REVIEW']} ({pct(s['A1']['review_rate'])}) | {s['A1']['REJECT']} ({pct(s['A1']['rejection_rate'])}) | {pct(s['A1']['review_burden'])} | proposed architecture |",
        f"| A3/A4 | `t*=0.16` binary | none | {s['A3_A4']['APPROVE']} ({pct(s['A3_A4']['approval_rate'])}) | {s['A3_A4']['HUMAN_REVIEW']} ({pct(s['A3_A4']['review_rate'])}) | {s['A3_A4']['REJECT']} ({pct(s['A3_A4']['rejection_rate'])}) | {pct(s['A3_A4']['review_burden'])} | monolithic comparator |",
        "",
        f"n = {payload['n']}.",
        "",
        "### A1 credit-risk bands (same frozen thresholds as A0)",
        "",
        "| Band | n | default_rate | Wilson 95% CI |",
        "| --- | ---: | ---: | --- |",
    ]
    for row in sorted(payload["a1_credit_bands"], key=lambda r: {"LOW": 0, "MEDIUM": 1, "HIGH": 2}.get(r["band"], 9)):
        lines.append(f"| {row['band']} | {row['n']} | {fmt(row['default_rate'])} | [{fmt(row['default_rate_ci_lower'])}, {fmt(row['default_rate_ci_upper'])}] |")
    lines += [
        "",
        "### Default rate by decision (stored TEST labels, evaluation only)",
        "",
        "| System | Decision | n | n_default | default_rate |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for sys_id, rows in (("A0", payload["a0_outcomes"]), ("A1", payload["a1_outcomes"]), ("A3/A4", payload["a3_outcomes"])):
        for row in rows:
            lines.append(f"| {sys_id} | {row['band']} | {row['n']} | {row['n_default']} | {fmt(row['default_rate'])} |")
    lines += [
        "",
        f"A1 L2 governance-status counts: `{payload['a1_governance']}`.",
        "",
        "These default rates describe the already-exposed TEST split under frozen policies. They are not causal effects and are not used to choose a policy.",
        "",
        "A1 APPROVE is listed with n=0 because the stored Stage 8 v2 fused output has `n_approve=0`; it is not a new TEST finding.",
        "",
        "## 9. Predictive vs policy metrics",
        "",
        "A0, A1, and A3/A4 consume the same frozen `p_selected`. They therefore share the Stage 5 Platt TEST predictive metrics:",
        "",
        f"- ROC-AUC `{fmt(pred['roc_auc'])}` 95% CI `[{fmt(pred['roc_auc_ci_lower'])}, {fmt(pred['roc_auc_ci_upper'])}]`",
        f"- PR-AUC `{fmt(pred['pr_auc'])}`",
        f"- Brier `{fmt(pred['brier'])}`",
        f"- log loss `{fmt(pred['log_loss'])}`",
        f"- ECE `{fmt(pred['ece'])}`",
        "",
        "A1 does not change EBM discrimination or calibration. Differences below are **policy allocation** differences.",
        "",
        "## 10. Governance interpretation",
        "",
        "LendingClub L2 status is `INSUFFICIENT_INFORMATION` for every stored TEST row. That means **insufficient contractual evidence for an application-level Shariah-oriented determination**. It does not mean applicants are Shariah compliant, non-compliant, halal, or haram. The engine did not classify Shariah compliance. L1 remains dataset context (`INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`), not 208,886 rulings.",
        "",
        "## 11. Limitations",
        "",
        "- TEST was previously unblinded; Stage 9.1 is not a new holdout confirmation.",
        "- No human-review outcomes exist; review burden is a simulated policy band.",
        "- Cost comparisons are not authorized in Stage 9.1.",
        "- A3/A4 is not an end-to-end Shariah model.",
        "",
        "## 12. Reproducibility",
        "",
        f"- experiment_id: `{EXPERIMENT_ID}`",
        f"- config: `{CONFIG.relative_to(ROOT).as_posix()}`",
        f"- script: `experiments/stage9_1_ablation/run_stage9_1.py`",
        f"- execution_timestamp: `{payload['execution_timestamp']}`",
        f"- git_commit: `{payload['git_commit']}`",
        f"- consistency test_cal_sha256: `{payload['consistency']['test_cal_sha256']}`",
        f"- test command: `{payload['test_command']}`",
        f"- test summary: `{payload['test_summary']}`",
        "",
        "## 13. Negative / unexpected results",
        "",
        "- A1 assigns 208,859 / 208,886 applications to HUMAN_REVIEW because L2 evidence is insufficient and LOW/MEDIUM map to review under G0. That is preserved, not softened.",
        "- A1 APPROVE count is 0. Automatic approval requires L2 `PASS`, which LendingClub rows do not receive.",
        "- A3/A4 approves 61,855 applications and has no review band, so the decision mix is not comparable as “better accuracy.”",
        "- Default rate among A3 APPROVE (0.096678) is higher than among A0 APPROVE (LOW band, 0.037462), as expected from a looser single threshold. This is not used to rank policies in Stage 9.1.",
        "",
        "## 14. Paper-safe interpretation",
        "",
        "The evidence-separated architecture produces a substantially different decision allocation because it introduces an explicit human-review state and incorporates the governance evidence state at the final decision layer. It does not improve ROC-AUC/Brier relative to A3/A4, because the credit scores are the same frozen scores. Stage 9.1 does not claim that A1 is economically superior, religiously correct, or more accurate as a default classifier.",
        "",
        "## 15. Later stages",
        "",
        "Stage 9.2 cost sensitivity, Stage 9.3 governance sensitivity, Stage 9.4 temporal analysis, Stage 9.5 UCI, Stage 9.6 clean-room reproduction, and paper writing were **not** executed.",
        "",
        "## Artifact index",
        "",
    ]
    for path in payload["artifact_paths"]:
        lines.append(f"- `{path}`")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if not V8_REPORT.exists() or not V8_FREEZE.exists():
        raise RuntimeError("Stage 8 artifacts missing; refusing to continue.")
    started = utc_now()
    stage8_guard = [
        ROOT / "results" / "decision" / "frozen_policy.json",
        ROOT / "results" / "decision" / "v2" / "frozen_policy.json",
        ROOT / "results" / "decision" / "v2" / "tables" / "table3_test_decision_outcomes.csv",
        ROOT / "results" / "decision" / "v2" / "metrics" / "fused_test.json",
        ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md",
        ROOT / "audit" / "stage8_v2_decision_fusion_run.json",
    ]
    stage8_hashes_before = {p.as_posix(): sha256_file(p) for p in stage8_guard}
    integrity = verify_frozen_artifacts()
    stored = load_stored_ablation()
    consistency = consistency_check_stored_probabilities(stored["systems"])
    OUT.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CONFIG, OUT / "stage9_1_ablation.yaml")
    systems = stored["systems"]
    comparison_rows = []
    for key in ("A0", "A1", "A3_A4"):
        row = systems[key]
        comparison_rows.append(
            {
                "system": key,
                "credit_policy": row["credit_policy"],
                "governance": row["governance"],
                "n": row["n"],
                "n_approve": row["APPROVE"],
                "n_human_review": row["HUMAN_REVIEW"],
                "n_reject": row["REJECT"],
                "approval_rate": row["approval_rate"],
                "review_rate": row["review_rate"],
                "rejection_rate": row["rejection_rate"],
                "review_burden": row["review_burden"],
                "notes": row["notes"],
            }
        )
    pd.DataFrame(comparison_rows).to_csv(TAB / "table1_ablation_comparison.csv", index=False)
    outcome_rows = []
    for sys_id, rows in (("A0", stored["a0_outcomes"]), ("A1", stored["a1_outcomes"]), ("A3_A4", stored["a3_outcomes"])):
        for row in rows:
            outcome_rows.append({"system": sys_id, **row})
    pd.DataFrame(outcome_rows).to_csv(TAB / "table2_default_rate_by_decision.csv", index=False)
    pd.DataFrame(stored["a1_credit_bands"]).to_csv(TAB / "table2b_a1_default_rate_by_credit_band.csv", index=False)
    pred = stored["predictive"]
    pd.DataFrame(
        [
            {
                "metric": k,
                "value": pred[k],
                "ci_lower": pred.get(f"{k}_ci_lower"),
                "ci_upper": pred.get(f"{k}_ci_upper"),
                "shared_by": "A0,A1,A3/A4",
                "source": "results/decision/v2/metrics/predictive_test_stage5.json",
            }
            for k in ("roc_auc", "pr_auc", "brier", "log_loss", "ece")
        ]
    ).to_csv(TAB / "table3_predictive_metrics_shared.csv", index=False)
    figure_decision_distribution(systems, FIG / "figure1_decision_counts")
    figure_a1_default_by_band(stored["a1_credit_bands"], FIG / "figure2_a1_default_by_credit_band")
    figure_a1_vs_a3_rates(systems, FIG / "figure3_a1_vs_a3_policy_rates")
    dump_json(
        OUT / "metrics" / "ablation_summary.json",
        json_safe(
            {
                "experiment_id": EXPERIMENT_ID,
                "systems": systems,
                "a3_identical_to_a4": True,
                "consistency": consistency,
                "predictive": pred,
                "a1_governance": stored["a1_governance"],
                "a1_band_counts": stored["a1_band_counts"],
                "integrity": integrity,
            }
        ),
    )
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests" / "test_stage9_1_ablation.py"), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    pytest_text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    summary_line = next((line.strip() for line in reversed(pytest_text.splitlines()) if "passed" in line), pytest_text[-400:])
    issues = []
    if proc.returncode != 0:
        issues.append(f"pytest failed: {summary_line}")
    if systems["A1"]["HUMAN_REVIEW"] != 208859:
        issues.append("A1 HUMAN_REVIEW count drifted from Stage 8 v2.")
    if systems["A3_A4"]["HUMAN_REVIEW"] != 0:
        issues.append("A3 produced HUMAN_REVIEW.")
    if not V8_REPORT.exists():
        issues.append("Stage 8 v2 report missing.")
    stage8_hashes_after = {p.as_posix(): sha256_file(p) for p in stage8_guard}
    if stage8_hashes_after != stage8_hashes_before:
        issues.append("Stage 8 artifact mutated during Stage 9.1.")
    status = "PASS" if not issues else "BLOCKED"
    execution_timestamp = utc_now()
    artifact_paths = [
        "docs/STAGE_9_1_ABLATION_REPORT.md",
        "audit/stage9_1_ablation_run.json",
        "results/ablation/v1/stage9_1_ablation.yaml",
        "results/ablation/v1/tables/table1_ablation_comparison.csv",
        "results/ablation/v1/tables/table2_default_rate_by_decision.csv",
        "results/ablation/v1/tables/table2b_a1_default_rate_by_credit_band.csv",
        "results/ablation/v1/tables/table3_predictive_metrics_shared.csv",
        "results/ablation/v1/metrics/ablation_summary.json",
        "results/figures/ablation/v1/figure1_decision_counts.png",
        "results/figures/ablation/v1/figure2_a1_default_by_credit_band.png",
        "results/figures/ablation/v1/figure3_a1_vs_a3_policy_rates.png",
    ]
    audit = {
        "experiment_id": EXPERIMENT_ID,
        "amendment_id": "AMENDMENT-SHARIAH-001",
        "started": started,
        "execution_timestamp": execution_timestamp,
        "git_commit": git_commit(ROOT),
        "status": status,
        "issues": issues,
        "a3_identical_to_a4": True,
        "a1_counts": {k: systems["A1"][k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")},
        "a0_counts": {k: systems["A0"][k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")},
        "a3_counts": {k: systems["A3_A4"][k] for k in ("APPROVE", "HUMAN_REVIEW", "REJECT")},
        "integrity": integrity,
        "consistency": consistency,
        "stage8_not_overwritten": stage8_hashes_after == stage8_hashes_before,
        "stage8_hashes": stage8_hashes_after,
        "models_trained": False,
        "thresholds_searched": False,
        "test_used_for_selection": False,
        "stage9_2_plus_executed": False,
        "config_sha256": sha256_file(CONFIG),
        "source_table3_sha256": sha256_file(V2_TABLE3),
        "pytest_exit_code": proc.returncode,
        "test_command": "python -m pytest tests/test_stage9_1_ablation.py -q --tb=short",
        "test_summary": summary_line,
        "software": {"python": sys.version.replace("\n", " "), "pandas": pd.__version__, "numpy": np.__version__},
    }
    dump_json(AUDIT, json_safe(audit))
    write_report(
        {
            "status": status,
            "n": stored["n"],
            "systems": systems,
            "predictive": pred,
            "a1_credit_bands": stored["a1_credit_bands"],
            "a0_outcomes": stored["a0_outcomes"],
            "a1_outcomes": stored["a1_outcomes"],
            "a3_outcomes": stored["a3_outcomes"],
            "a1_governance": stored["a1_governance"],
            "integrity": integrity,
            "consistency": consistency,
            "execution_timestamp": execution_timestamp,
            "git_commit": git_commit(ROOT),
            "test_command": "python -m pytest tests/test_stage9_1_ablation.py -q --tb=short",
            "test_summary": summary_line,
            "artifact_paths": artifact_paths,
        }
    )
    print(json.dumps({"status": status, "a1": audit["a1_counts"], "a3": audit["a3_counts"]}, indent=2), flush=True)
    if proc.returncode != 0:
        print(pytest_text[-2000:], flush=True)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
