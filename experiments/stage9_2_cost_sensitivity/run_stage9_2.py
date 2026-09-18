"""Stage 9.2 cost sensitivity from frozen Stage 8/9.1 decisions. No retraining. No Stage 9.3+."""

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
from decision.stage9_2 import (  # noqa: E402
    EXPERIMENT_ID,
    FN_FP_RATIOS,
    assemble_cost_sensitivity,
    cite_experiment_g,
    cite_validation_table2,
    stage8_guard_paths,
    stage91_guard_paths,
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


OUT = ROOT / "results" / "cost_sensitivity" / "v1"
FIG = ROOT / "results" / "figures" / "cost_sensitivity" / "v1"
TAB = OUT / "tables"
AUDIT = ROOT / "audit" / "stage9_2_cost_sensitivity_run.json"
REPORT = ROOT / "docs" / "STAGE_9_2_COST_SENSITIVITY_REPORT.md"
CONFIG = ROOT / "configs" / "stage9_2_cost_sensitivity.yaml"


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


def figure_normalized_cost(by_system: dict[str, list[dict[str, Any]]], path_stem: Path) -> None:
    fig, ax = plt.subplots(figsize=(7.4, 4.6))
    styles = {
        "A0": ("A0 credit-only", "#4c78a8"),
        "A1": ("A1 proposed (G0)", "#f58518"),
        "A3_A4": ("A3/A4 binary t*=0.16", "#54a24b"),
    }
    for key, (label, color) in styles.items():
        xs = [row["fn_fp_ratio"] for row in by_system[key]]
        ys = [row["cost_normalized"] for row in by_system[key]]
        ax.plot(xs, ys, marker="o", label=label, color=color)
    ax.set_xticks(list(FN_FP_RATIOS))
    ax.set_xticklabels([f"{r}:1" for r in FN_FP_RATIOS])
    ax.set_xlabel("Assumed FN:FP ratio (C_FN / C_FP)")
    ax.set_ylabel("Normalized relative cost (C_FP = 1)")
    ax.set_title("Stage 9.2. Frozen decisions under alternative FN:FP assumptions")
    ax.legend(frameon=False)
    fig.tight_layout()
    _save(fig, path_stem)


def figure_cost_decomposition(by_system: dict[str, list[dict[str, Any]]], path_stem: Path) -> None:
    systems = ["A0", "A1", "A3_A4"]
    labels = ["A0", "A1", "A3/A4"]
    primary = [next(r for r in by_system[s] if r["fn_fp_ratio"] == 5) for s in systems]
    fn_part = [r["c_fn"] * r["fn"] / r["n"] for r in primary]
    fp_part = [r["c_fp"] * r["fp"] / r["n"] for r in primary]
    rev_part = [r["cost_review_only"] / r["n"] for r in primary]
    x = np.arange(len(systems))
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.bar(x, fn_part, label="C_FN * FN / n", color="#d62728")
    ax.bar(x, fp_part, bottom=fn_part, label="C_FP * FP / n", color="#ff7f0e")
    ax.bar(x, rev_part, bottom=np.array(fn_part) + np.array(fp_part), label="C_REVIEW * n_review / n", color="#9467bd")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Normalized relative cost at FN:FP=5:1")
    ax.set_title("Stage 9.2. Cost decomposition of frozen TEST decisions")
    ax.legend(frameon=False)
    fig.tight_layout()
    _save(fig, path_stem)


def write_report(payload: dict[str, Any]) -> None:
    c = payload["confusion"]
    g = payload["experiment_g"]
    t2 = payload["validation_table2"]
    lines = [
        "# Stage 9.2 Cost Sensitivity Report",
        "",
        "LendingClub TEST was already exposed during Stages 4B–8. Stage 9.2 did not use TEST data for model or policy selection. The analysis scores already-frozen Stage 8 v2 decision/outcome counts under alternative relative FN:FP assumptions. Decisions are not changed.",
        "",
        f"**Status:** `STAGE_9_2_STATUS = {payload['status']}`",
        "",
        "```text",
        "STAGE_9_3+ = NOT EXECUTED",
        "EXPERIMENT_G = NOT_EXECUTED — CITE_ONLY_PER_STAGE_9_0_FREEZE",
        "```",
        "",
        "## 1. Objective",
        "",
        "Determine how the already-frozen A0 / A1 / A3–A4 decision outputs behave under different explicit relative error-cost assumptions. This is a policy-analysis experiment, not model training, and not a new threshold search.",
        "",
        "## 2. Relationship to Stage 9.0 freeze",
        "",
        "The Stage 9.0 design freeze is controlling (`audit/stage9_0_experimental_freeze.json`). There is no file named `docs/STAGE_9_0_DESIGN_FREEZE_REPORT.md`; the freeze artifact used is that JSON plus `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` §0 and §5.1.",
        "",
        "- Frozen thresholds remain `t_low=0.06`, `t_high=0.69`, `t*=0.16`.",
        "- G0 remains the A1 governance treatment.",
        "- Cost set remains `r ∈ {1, 2, 5, 10}` labeled `FN:FP=r:1` with `C_FP=1`.",
        "- O-TEST Option A: no additional LC TEST policy remaps. Stage 9.2 does not remap decisions.",
        "- Protocol §5.1 already-executed validation threshold table is cited, not rerun.",
        "- Experiment G is cited from its existing validation CSV and is not rerun.",
        "",
        "The Stage 9.2 authorization listed FN:FP as `1:1, 1:2, 1:5, 1:10`. The freeze and Stage 8 `table2` use `FN:FP = r:1` with `r ∈ {1,2,5,10}` (`C_FN = r`, `C_FP = 1`). **The freeze notation is used.** The inverted reading `C_FN:C_FP = 1:2` was not implemented.",
        "",
        "## 3. Data / artifacts used",
        "",
        "- Dataset: LendingClub granting extract, split = TEST (`issue_month >= 2017-02`), n = 208,886.",
        "- Source confusion: `results/decision/v2/tables/table3_test_decision_outcomes.csv`.",
        f"- Stage 8 v1 freeze sha256 `{payload['integrity']['v1_freeze_sha256']}`.",
        "- Stage 9.1 identity of A3/A4: identical binary comparator; reported once.",
        "- Predictive metrics are the frozen Stage 5 Platt TEST metrics; they are not recomputed here.",
        "",
        "## 4. Cost definition",
        "",
        "The cost ratios are analytical assumptions rather than observed monetary costs.",
        "",
        "```text",
        "C_FP = 1",
        "C_FN = r * C_FP",
        "C_REVIEW = 0.25 * C_FP   for A0 and A1 (three-way / fused)",
        "C_REVIEW = 0             for A3/A4 (binary; n_review = 0)",
        "Cost_total = C_FN * FN + C_FP * FP + C_REVIEW * n_review",
        "Cost_normalized = Cost_total / n",
        "```",
        "",
        "This is the Stage 8 formula (`docs/decision_cost_assumptions.md`; `src/decision/cost_policy.py`). `FN` is auto-approved defaults. `FP` is auto-rejected non-defaults. Reviewed applications are excluded from TP/TN/FP/FN and incur `C_REVIEW`. No currency unit is assigned.",
        "",
        "The FN+FP-only component `C_FN*FN + C_FP*FP` is also stored so the two-term form is visible. It is not used as a replacement for the frozen three-term formula.",
        "",
        "## 5. Cost ratios",
        "",
        "| Label | C_FN | C_FP | Role |",
        "| --- | ---: | ---: | --- |",
        "| FN:FP=1:1 | 1 | 1 | sensitivity |",
        "| FN:FP=2:1 | 2 | 1 | sensitivity |",
        "| FN:FP=5:1 | 5 | 1 | primary frozen scenario |",
        "| FN:FP=10:1 | 10 | 1 | sensitivity |",
        "",
        "No ratio is selected as universally correct. TEST is not used to pick a ratio.",
        "",
        "## 6. Policies evaluated",
        "",
        "| System | Frozen policy | HUMAN_REVIEW | Governance | Role |",
        "| --- | --- | --- | --- | --- |",
        "| A0 | `t_low=0.06`, `t_high=0.69` credit-only | Yes (MEDIUM) | none | credit-only ablation |",
        "| A1 | same bands + G0 fusion | Yes | G0 / L2 `INSUFFICIENT_INFORMATION` | proposed architecture |",
        "| A3/A4 | `t*=0.16` binary | No | none | monolithic comparator; identical under the freeze |",
        "",
        "A1 retains HUMAN_REVIEW. HUMAN_REVIEW represents an evidence-handling state under the frozen governance policy, not a Shariah ruling. L2 `INSUFFICIENT_INFORMATION` means insufficient contractual evidence for an application-level Shariah-oriented determination.",
        "",
        "same predictions → same decisions → different assumed cost functions → different reported cost values.",
        "",
        "## 7. Results",
        "",
        "### 7.1 Frozen decision allocation (unchanged across cost ratios)",
        "",
        "| System | n | APPROVE | HUMAN_REVIEW | REJECT | TP | TN | FP | FN | FPR (pop.) | FNR (pop.) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
        f"| A0 | {c['A0']['n']} | {c['A0']['n_approve']} | {c['A0']['n_review']} | {c['A0']['n_reject']} | {c['A0']['tp']} | {c['A0']['tn']} | {c['A0']['fp']} | {c['A0']['fn']} | {fmt(c['A0']['fpr_population'])} | {fmt(c['A0']['fnr_population'])} |",
        f"| A1 | {c['A1']['n']} | {c['A1']['n_approve']} | {c['A1']['n_review']} | {c['A1']['n_reject']} | {c['A1']['tp']} | {c['A1']['tn']} | {c['A1']['fp']} | {c['A1']['fn']} | {fmt(c['A1']['fpr_population'])} | {fmt(c['A1']['fnr_population'])} |",
        f"| A3/A4 | {c['A3_A4']['n']} | {c['A3_A4']['n_approve']} | {c['A3_A4']['n_review']} | {c['A3_A4']['n_reject']} | {c['A3_A4']['tp']} | {c['A3_A4']['tn']} | {c['A3_A4']['fp']} | {c['A3_A4']['fn']} | {fmt(c['A3_A4']['fpr_population'])} | {fmt(c['A3_A4']['fnr_population'])} |",
        "",
        "FPR/FNR are decision-policy error rates of the frozen maps. They do not change when the cost function changes.",
        "",
        "### 7.2 Relative cost of the same frozen TEST decisions",
        "",
        "| System | FN:FP | C_FN | C_FP | C_REVIEW | cost_total | cost_normalized | FN+FP component | review component |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for system in ("A0", "A1", "A3_A4"):
        for row in payload["by_system"][system]:
            label = "A3/A4" if system == "A3_A4" else system
            lines.append(
                f"| {label} | {row['ratio_label']} | {fmt(row['c_fn'], 1)} | {fmt(row['c_fp'], 1)} | {fmt(row['c_review'])} | {fmt(row['cost_total'], 2)} | {fmt(row['cost_normalized'])} | {fmt(row['cost_fn_fp_only'], 2)} | {fmt(row['cost_review_only'], 2)} |"
            )
    lines += [
        "",
        "FN:FP=5:1 normalized costs reproduce the stored Stage 8 v2 `expected_normalized_cost` values (A0 0.248460; A1 0.250030; A3/A4 0.663860).",
        "",
        "### 7.3 Predictive metrics (unchanged; not a cost result)",
        "",
        "A0, A1, and A3/A4 share the frozen Stage 5 Platt TEST scores. Stage 9.2 does not alter ROC-AUC, PR-AUC, Brier, log loss, or ECE. Those remain the Stage 9.1 / Stage 5 citation.",
        "",
        "## 8. Interpretation",
        "",
        "Cost sensitivity evaluates the consequences of alternative relative error-cost assumptions; it does not establish real-world profitability or economic optimality.",
        "",
        "- A1 has `FN=0` because APPROVE=0. Its total relative cost is therefore invariant to the FN:FP ratio and is almost entirely `C_REVIEW * n_review`.",
        "- A0 has 196 auto-approved defaults, so its cost rises slowly as `r` increases; review still dominates.",
        "- A3/A4 has no review band. Its cost is `C_FN*FN + C_FP*FP` and is much more sensitive to `r` because both FN (5,980) and FP (108,771) are large.",
        "- Lower A1 cost than A3/A4 under these assumptions is not evidence that A1 is economically superior. It reflects sending almost every application to simulated review at `C_REVIEW=0.25`.",
        "",
        "HUMAN_REVIEW represents an evidence-handling state under the frozen governance policy, not a Shariah ruling.",
        "",
        "## 9. Sensitivity analysis",
        "",
        "### 9.1 Fixed-policy FN:FP sensitivity (this Stage 9.2 primary result)",
        "",
        "The table in §7.2 is the authorized analysis: frozen TEST decisions, four assumed ratios, Stage 8 cost formula.",
        "",
        "### 9.2 Already-executed validation threshold identification (cited, not rerun)",
        "",
        "Stage 8 already selected different `t_low/t_high` and `t*` on **validation** for each ratio. That is a different scientific object (new policies), not the Stage 9.2 primary analysis. It is cited only:",
        "",
        "| FN:FP | val t_low | val t_high | val single t* | val two-threshold cost |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in t2["rows"]:
        lines.append(
            f"| {row['cost_scenario']} | {fmt(row['t_low'], 2)} | {fmt(row['t_high'], 2)} | {fmt(row['single_t'], 2)} | {fmt(row['expected_normalized_cost'])} |"
        )
    lines += [
        "",
        f"Source: `{t2['artifact']}` sha256 `{t2['sha256']}`. These thresholds were **not** applied to TEST in Stage 9.2.",
        "",
        "### 9.3 Experiment G (cited, not executed)",
        "",
        f"Status: `{g['status']}`.",
        "",
        f"Definition reproduced from the protocol: {g['definition']}",
        "",
        f"{g['reason']}",
        "",
        "| c_review_over_fp | val t_low | val t_high | val normalized cost | val review rate |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in g["rows"]:
        lines.append(
            f"| {fmt(row['c_review_over_fp'], 2)} | {fmt(row['t_low'], 2)} | {fmt(row['t_high'], 2)} | {fmt(row['expected_normalized_cost'])} | {fmt(row['review_rate'])} |"
        )
    lines += [
        "",
        f"Source: `{g['artifact']}` sha256 `{g['sha256']}`. G's `t_low/t_high` are not promoted into Stage 8.",
        "",
        "## 10. Limitations",
        "",
        "- Costs are researcher assumptions, not bank, regulator, or Shariah-board costs.",
        "- No dollar amounts, LGD, recovery, or profit model is used or claimed.",
        "- HUMAN_REVIEW has no observed reviewer outcome; `C_REVIEW` is not a staffing model.",
        "- TEST was previously unblinded; this is not a new holdout confirmation.",
        "- A1's near-universal review is an evidence-availability result (`INSUFFICIENT_INFORMATION`), not a religious classification.",
        "",
        "## 11. Test / selection leakage statement",
        "",
        "LendingClub TEST was already exposed during Stages 4B–8. Stage 9.2 did not use TEST data for model or policy selection. No threshold was searched. No cost ratio was chosen using TEST. FN:FP=5:1 remains the pre-declared primary scenario from Stage 8. The analysis is a controlled re-scoring of frozen confusion counts.",
        "",
        "## 12. Reproducibility",
        "",
        f"- experiment_id: `{EXPERIMENT_ID}`",
        f"- config: `{CONFIG.relative_to(ROOT).as_posix()}`",
        f"- script: `experiments/stage9_2_cost_sensitivity/run_stage9_2.py`",
        f"- execution_timestamp: `{payload['execution_timestamp']}`",
        f"- git_commit: `{payload['git_commit']}`",
        f"- test command: `{payload['test_command']}`",
        f"- test summary: `{payload['test_summary']}`",
        f"- Stage 8 freeze sha256: `{payload['integrity']['v1_freeze_sha256']}`",
        "",
        "## 13. Conclusion",
        "",
        "The cost ratios are analytical assumptions rather than observed monetary costs. Cost sensitivity evaluates the consequences of alternative relative error-cost assumptions; it does not establish real-world profitability or economic optimality. Under the frozen Stage 8 maps, changing FN:FP reweights the same FP/FN/review counts. A1 does not become a binary policy, does not lose HUMAN_REVIEW, and does not acquire a Shariah score. Stage 9.3+ were not executed.",
        "",
        "## Artifact index",
        "",
    ]
    for path in payload["artifact_paths"]:
        lines.append(f"- `{path}`")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    started = utc_now()
    guard_paths = stage8_guard_paths() + stage91_guard_paths()
    hashes_before = {p.as_posix(): sha256_file(p) for p in guard_paths}
    assembled = assemble_cost_sensitivity()
    experiment_g = cite_experiment_g()
    table2 = cite_validation_table2()
    OUT.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    shutil.copy2(CONFIG, OUT / "stage9_2_cost_sensitivity.yaml")
    confusion_rows = []
    for system, counts in assembled["confusion"].items():
        confusion_rows.append(
            {
                "system": system,
                "n": counts["n"],
                "n_approve": counts["n_approve"],
                "n_review": counts["n_review"],
                "n_reject": counts["n_reject"],
                "tp": counts["tp"],
                "tn": counts["tn"],
                "fp": counts["fp"],
                "fn": counts["fn"],
                "fpr_population": counts["fpr_population"],
                "fnr_population": counts["fnr_population"],
                "fpr_auto": counts["fpr_auto"],
                "fnr_auto": counts["fnr_auto"],
                "c_review_over_fp": counts["c_review_over_fp"],
            }
        )
    pd.DataFrame(confusion_rows).to_csv(TAB / "table1_frozen_confusion.csv", index=False)
    pd.DataFrame(assembled["rows"]).to_csv(TAB / "table2_cost_by_policy_and_ratio.csv", index=False)
    pd.DataFrame(table2["rows"]).to_csv(TAB / "table3_cited_validation_threshold_selection.csv", index=False)
    pd.DataFrame(experiment_g["rows"]).to_csv(TAB / "table4_cited_experiment_g.csv", index=False)
    figure_normalized_cost(assembled["by_system"], FIG / "figure1_normalized_cost_vs_fnfp")
    figure_cost_decomposition(assembled["by_system"], FIG / "figure2_cost_decomposition_fnfp5")
    dump_json(
        OUT / "metrics" / "cost_sensitivity_summary.json",
        json_safe(
            {
                "experiment_id": EXPERIMENT_ID,
                "used_for_selection": False,
                "models_trained": False,
                "models_loaded": False,
                "calibration_refit": False,
                "a3_identical_to_a4": True,
                "a1_human_review_retained": assembled["a1_human_review_retained"],
                "a1_cost_invariant_to_fn_fp_ratio": assembled["a1_cost_invariant_to_fn_fp_ratio"],
                "decisions_unchanged_across_ratios": True,
                "fn_fp_ratios": assembled["fn_fp_ratios"],
                "ratio_labels": assembled["ratio_labels"],
                "formula": assembled["formula"],
                "integrity": assembled["integrity"],
                "confusion": assembled["confusion"],
                "by_system": assembled["by_system"],
                "experiment_g": experiment_g,
                "validation_table2": {"status": table2["status"], "sha256": table2["sha256"], "artifact": table2["artifact"]},
            }
        ),
    )
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests" / "test_stage9_2_cost_sensitivity.py"), "-q", "--tb=short"],
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
        issues.append("Stage 8 or Stage 9.1 artifact mutated during Stage 9.2.")
    if assembled["confusion"]["A1"]["n_review"] != 208859:
        issues.append("A1 HUMAN_REVIEW drifted.")
    if assembled["confusion"]["A3_A4"]["n_review"] != 0:
        issues.append("A3 produced HUMAN_REVIEW.")
    status = "PASS" if not issues else "BLOCKED"
    execution_timestamp = utc_now()
    artifact_paths = [
        "docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md",
        "audit/stage9_2_cost_sensitivity_run.json",
        "results/cost_sensitivity/v1/stage9_2_cost_sensitivity.yaml",
        "results/cost_sensitivity/v1/tables/table1_frozen_confusion.csv",
        "results/cost_sensitivity/v1/tables/table2_cost_by_policy_and_ratio.csv",
        "results/cost_sensitivity/v1/tables/table3_cited_validation_threshold_selection.csv",
        "results/cost_sensitivity/v1/tables/table4_cited_experiment_g.csv",
        "results/cost_sensitivity/v1/metrics/cost_sensitivity_summary.json",
        "results/figures/cost_sensitivity/v1/figure1_normalized_cost_vs_fnfp.png",
        "results/figures/cost_sensitivity/v1/figure2_cost_decomposition_fnfp5.png",
    ]
    audit = {
        "experiment_id": EXPERIMENT_ID,
        "amendment_id": "AMENDMENT-SHARIAH-001",
        "started": started,
        "execution_timestamp": execution_timestamp,
        "git_commit": git_commit(ROOT),
        "status": status,
        "issues": issues,
        "dataset": "LendingClub granting extract",
        "split": "test",
        "n": 208886,
        "cost_ratios": list(FN_FP_RATIOS),
        "cost_ratio_labels": [f"FN:FP={r}:1" for r in FN_FP_RATIOS],
        "cost_formula": assembled["formula"],
        "policy_identifiers": ["A0", "A1", "A3_A4"],
        "frozen_thresholds": {"t_low": 0.06, "t_high": 0.69, "t_star": 0.16},
        "stage8_policy_hash": assembled["integrity"]["v1_freeze_sha256"],
        "a3_identical_to_a4": True,
        "random_seed": 42,
        "models_loaded": False,
        "models_trained": False,
        "calibration_refit": False,
        "lendingclub_test_used": True,
        "test_used_for_policy_selection": False,
        "stage8_modified": False,
        "stage9_1_modified": False,
        "stage8_not_overwritten": hashes_after == hashes_before,
        "stage9_3_plus_executed": False,
        "experiment_g": {
            "status": experiment_g["status"],
            "executed_in_stage9_2": False,
            "cited_existing_artifact": True,
            "constraint_conflict_lc_test_selection": False,
            "sha256": experiment_g["sha256"],
        },
        "integrity": assembled["integrity"],
        "config_sha256": sha256_file(CONFIG),
        "source_table3_sha256": sha256_file(ROOT / "results" / "decision" / "v2" / "tables" / "table3_test_decision_outcomes.csv"),
        "guard_hashes": hashes_after,
        "pytest_exit_code": proc.returncode,
        "test_command": "python -m pytest tests/test_stage9_2_cost_sensitivity.py -q --tb=short",
        "test_summary": summary_line,
        "software": {"python": sys.version.replace("\n", " "), "pandas": pd.__version__, "numpy": np.__version__},
    }
    dump_json(AUDIT, json_safe(audit))
    write_report(
        {
            "status": status,
            "confusion": assembled["confusion"],
            "by_system": assembled["by_system"],
            "integrity": assembled["integrity"],
            "experiment_g": experiment_g,
            "validation_table2": table2,
            "execution_timestamp": execution_timestamp,
            "git_commit": git_commit(ROOT),
            "test_command": "python -m pytest tests/test_stage9_2_cost_sensitivity.py -q --tb=short",
            "test_summary": summary_line,
            "artifact_paths": artifact_paths,
        }
    )
    print(
        json.dumps(
            {
                "status": status,
                "experiment_g": experiment_g["status"],
                "a1_fnfp5_cost_normalized": next(r["cost_normalized"] for r in assembled["by_system"]["A1"] if r["fn_fp_ratio"] == 5),
                "a3_fnfp5_cost_normalized": next(r["cost_normalized"] for r in assembled["by_system"]["A3_A4"] if r["fn_fp_ratio"] == 5),
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
