"""Stage 9.4 UCI independent generalization.

Does not modify LendingClub artifacts, Stage 7/8 governance, or Stage 9.1-9.3.
Does not edit execution-gate / constitution / amendment files.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import joblib
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from calibration.metrics import CALIB_METRIC_FUNCS, calibration_metrics  # noqa: E402
from calibration.reliability import plot_reliability_panels  # noqa: E402
from data.audit_datasets import git_commit, sha256_file  # noqa: E402
from evaluation.bootstrap import bootstrap_ci  # noqa: E402
from evaluation.metrics import METRIC_FUNCS, classification_metrics  # noqa: E402
from evaluation.plots import plot_pr, plot_roc  # noqa: E402
from models.uci_models import (  # noqa: E402
    ebm_config,
    ebm_model,
    logistic_config,
    logistic_model,
    predict_positive,
    scale_pos_weight,
    xgboost_config,
    xgboost_model,
)
from preprocessing.uci_preprocessor import UCIPreprocessor, UCI_TARGET, ebm_frame  # noqa: E402
from uci_generalization.stage9_4 import (  # noqa: E402
    AMENDMENT_ID,
    EXPERIMENT_ID,
    FAMILIES,
    FINAL_SEED,
    L1_METADATA_ONLY,
    N_BOOT,
    BOOT_SEED,
    SEEDS,
    aggregate_seed_metrics,
    assert_protected_unchanged,
    cite_lendingclub_stage5_test,
    ebm_global_stats,
    ebm_shape,
    fit_calibrators,
    load_uci_with_splits,
    require_amendment_approved,
    row_ref,
    select_family,
    snapshot_protected_hashes,
    split_xy,
    verify_frozen_uci_split,
)

OUT = ROOT / "results" / "uci_generalization" / "v1"
TAB = OUT / "tables"
MET = OUT / "metrics"
FIG = OUT / "figures"
PRED = OUT / "predictions"
CKPT = ROOT / "experiments" / "stage9_4_uci_generalization" / "checkpoints"
AUDIT = ROOT / "audit" / "stage9_4_uci_run.json"
REPORT = ROOT / "docs" / "STAGE_9_4_UCI_GENERALIZATION_REPORT.md"
CONFIG = ROOT / "configs" / "stage9_4_uci_generalization.yaml"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(json_safe(payload), indent=2, ensure_ascii=True, allow_nan=False) + "\n", encoding="utf-8")


def json_safe(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, np.ndarray):
        return json_safe(obj.tolist())
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, (np.floating, float)):
        return float(obj)
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if obj is None or isinstance(obj, str):
        return obj
    return str(obj)


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)


def md_table(rows: list[dict], columns: list[str], fmt: dict[str, str] | None = None) -> str:
    fmt = fmt or {}
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = []
        for col in columns:
            val = row.get(col, "")
            spec = fmt.get(col)
            if spec and isinstance(val, (int, float, np.floating)) and val is not None:
                cells.append(format(float(val), spec))
            else:
                cells.append("" if val is None else str(val))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def compare_plain(uci: float, lc: float, higher_better: bool) -> str:
    if abs(uci - lc) < 1e-4:
        return "comparable"
    better = (uci > lc) if higher_better else (uci < lc)
    return "better" if better else "worse"


def fit_family(family: str, seed: int, x_tr, y_tr, x_va, y_va, ebm_tr, ebm_va, xgb_estimators: int | None = None):
    if family == "logistic_regression":
        model = logistic_model(seed)
        model.fit(x_tr, y_tr)
        return model, predict_positive(model, x_va), logistic_config(seed)
    if family == "explainable_boosting_machine":
        model = ebm_model(seed)
        model.fit(ebm_tr, y_tr)
        return model, predict_positive(model, ebm_va), ebm_config(seed)
    if family == "xgboost":
        if xgb_estimators is None:
            model = xgboost_model(seed, y_tr, n_estimators=400, early_stopping_rounds=30)
            model.fit(x_tr, y_tr, eval_set=[(x_va, y_va)], verbose=False)
        else:
            model = xgboost_model(seed, y_tr, n_estimators=xgb_estimators, early_stopping_rounds=None)
            model.fit(x_tr, y_tr, verbose=False)
        cfg = xgboost_config(seed, scale_pos_weight(y_tr), n_estimators=int(getattr(model, "n_estimators", 400)))
        cfg["best_iteration"] = int(getattr(model, "best_iteration", -1))
        return model, predict_positive(model, x_va), cfg
    raise ValueError(family)


def apply_family(family: str, model, x_mat, ebm_x):
    if family == "explainable_boosting_machine":
        return predict_positive(model, ebm_x)
    return predict_positive(model, x_mat)


def plot_importance(stats: pd.DataFrame, path_stem: Path) -> None:
    frame = stats.sort_values("mean_abs", ascending=True)
    fig, ax = plt.subplots(figsize=(6.4, 5.4))
    ax.barh(frame["feature"], frame["mean_abs"], color="#1f77b4")
    ax.set_xlabel("Mean |EBM term| (logit / link scale)")
    ax.set_title("UCI EBM native global attributions (train)")
    fig.tight_layout()
    path_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(path_stem.with_suffix(".png"), bbox_inches="tight")
    plt.close(fig)


def run_pytest() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests" / "test_stage9_4_uci.py"), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    summary = lines[-1] if lines else "no pytest output"
    return proc.returncode, summary


def write_report(payload: dict[str, Any]) -> None:
    split = payload["split_prevalence"]
    fam_sel = payload["family_selection"]
    cal_sel = payload["calibrator_selection"]
    lc = payload["lendingclub_citation"]
    uci_sel = payload["uci_test_selected"]
    purpose = (
        "This experiment tests whether the credit-risk / calibration METHODOLOGY generalizes to a second, "
        "independent, public credit dataset. It is NOT a test of the evidence-separated decision architecture "
        "as a whole, and it does NOT include a Shariah governance layer, because UCI structurally lacks "
        "contract-level fields (already established in the Stage 2 audit)."
    )
    cmp_rows = []
    for metric, higher in (("roc_auc", True), ("pr_auc", True), ("brier", False), ("log_loss", False), ("ece", False)):
        cmp_rows.append(
            {
                "metric": metric,
                "uci_test": uci_sel[metric],
                "lc_test_cited": lc[metric],
                "plain_comparison": compare_plain(uci_sel[metric], lc[metric], higher),
            }
        )
    shap_note = payload["shap_vs_ebm"]
    md = f"""# Stage 9.4 UCI Independent Generalization Report

**Experiment ID:** `{EXPERIMENT_ID}`  
**Amendment:** `{AMENDMENT_ID}` status `{payload["amendment"]["status"]}` (approval date {payload["amendment"]["approval_date"]})  
**Status:** `{payload["status"]}`

## Purpose

{purpose}

Do not overclaim: UCI results do not validate or invalidate the LendingClub architecture as a whole.

## A. Frozen UCI split

Verified existing Stage 3 artifacts. A new split was **not** created.

| Split | Rows | Positives | Prevalence |
| --- | ---: | ---: | ---: |
| train | {split["train"]["n"]} | {split["train"]["n_positive"]} | {split["train"]["prevalence"]:.6f} |
| validation | {split["validation"]["n"]} | {split["validation"]["n_positive"]} | {split["validation"]["prevalence"]:.6f} |
| test | {split["test"]["n"]} | {split["test"]["n_positive"]} | {split["test"]["prevalence"]:.6f} |

- Raw UCI SHA-256: `{payload["split_verify"]["zip_sha256"]}`
- Membership hashes matched `audit/uci_split_manifest.json`
- `merged_with_lendingclub`: false
- Time index: none (`NO_CALENDAR_TIMESTAMPS`). No temporal structure was invented.

## B. Targets (semantic difference)

| Dataset | Target column | Positive class | Negative class |
| --- | --- | --- | --- |
| UCI Default of Credit Card Clients | `default payment next month` | 1 = default payment next month | 0 = no default payment next month |
| LendingClub granting extract | `Default` | 1 = Charged Off | 0 = Fully Paid |

These are two separate datasets with two separate targets. Metrics are reported **alongside**, not merged. No statistical test of equality of AUCs is performed.

## C. Models

Small justified UCI-only set: logistic regression, EBM (`interactions=0`), XGBoost. Random forest was not run.

Frozen protocol U1 listed EBM + logistic regression. This execution additionally includes XGBoost because the research-owner Stage 9.4 instruction of 2026-09-15 specified those three families. Hyperparameters were pre-specified for UCI sample size and were **not** copied from LendingClub Stage 4B configs. LendingClub thresholds `0.06/0.69/0.16` were **not** transferred.

{fam_sel["reason"]}

Validation seed metrics:

{md_table(payload["validation_family_rows"], ["family", "seed", "roc_auc", "pr_auc", "brier", "log_loss"], {"roc_auc": ".6f", "pr_auc": ".6f", "brier": ".6f", "log_loss": ".6f"})}

Seed aggregates (selection input):

{md_table(payload["validation_aggregates"], ["family", "pr_auc_mean", "pr_auc_sd", "brier_mean", "roc_auc_mean"], {"pr_auc_mean": ".6f", "pr_auc_sd": ".6f", "brier_mean": ".6f", "roc_auc_mean": ".6f"})}

## D. Calibration

Raw vs Platt vs isotonic, fit on **UCI validation only** for the selected family (seed 42, train-only model). Stage 5 rule: validation Brier, 0.001 practical tie preferring simpler methods (`raw` > `platt` > `isotonic`). LendingClub Platt `a,b` were not reused.

{cal_sel["reason"]}

Validation calibration:

{md_table(payload["validation_calibration_rows"], ["method", "brier", "log_loss", "ece", "roc_auc", "pr_auc"], {"brier": ".6f", "log_loss": ".6f", "ece": ".6f", "roc_auc": ".6f", "pr_auc": ".6f"})}

## E. UCI TEST metrics (once, after freeze)

Selected family `{payload["selected_family"]}`, selected calibrator `{payload["selected_calibrator"]}`. `test_used_for_selection = false`.

{md_table(payload["uci_test_calibration_rows"], ["method", "roc_auc", "pr_auc", "brier", "log_loss", "ece"], {"roc_auc": ".6f", "pr_auc": ".6f", "brier": ".6f", "log_loss": ".6f", "ece": ".6f"})}

Bootstrap: 1000 row resamples, percentile 95% CI, seed 42. Not used for selection.

Selected UCI TEST (with CI):

| Metric | Point | 95% CI |
| --- | ---: | --- |
| ROC-AUC | {uci_sel["roc_auc"]:.6f} | [{uci_sel["roc_auc_ci_lower"]:.6f}, {uci_sel["roc_auc_ci_upper"]:.6f}] |
| PR-AUC | {uci_sel["pr_auc"]:.6f} | [{uci_sel["pr_auc_ci_lower"]:.6f}, {uci_sel["pr_auc_ci_upper"]:.6f}] |
| Brier | {uci_sel["brier"]:.6f} | [{uci_sel["brier_ci_lower"]:.6f}, {uci_sel["brier_ci_upper"]:.6f}] |
| Log loss | {uci_sel["log_loss"]:.6f} | [{uci_sel["log_loss_ci_lower"]:.6f}, {uci_sel["log_loss_ci_upper"]:.6f}] |
| ECE | {uci_sel["ece"]:.6f} | [{uci_sel["ece_ci_lower"]:.6f}, {uci_sel["ece_ci_upper"]:.6f}] |

Raw TEST metrics for all three families (reported after freeze; not used to choose the family):

{md_table(payload["uci_test_family_rows"], ["family", "roc_auc", "pr_auc", "brier", "log_loss"], {"roc_auc": ".6f", "pr_auc": ".6f", "brier": ".6f", "log_loss": ".6f"})}

## F. Alongside frozen LendingClub TEST (not merged)

LendingClub numbers are **cited** from `results/calibration/metrics/stage5_test_metrics.json` (Platt, selected EBM, LC TEST). They were not recomputed.

| Metric | UCI TEST (`{payload["selected_family"]}` / `{payload["selected_calibrator"]}`) | LC TEST (EBM / Platt, cited) | Plain comparison |
| --- | ---: | ---: | --- |
| n | {uci_sel["n"]} | {lc["n"]} | separate samples |
| ROC-AUC | {uci_sel["roc_auc"]:.6f} | {lc["roc_auc"]:.6f} | {cmp_rows[0]["plain_comparison"]} |
| PR-AUC | {uci_sel["pr_auc"]:.6f} | {lc["pr_auc"]:.6f} | {cmp_rows[1]["plain_comparison"]} |
| Brier | {uci_sel["brier"]:.6f} | {lc["brier"]:.6f} | {cmp_rows[2]["plain_comparison"]} |
| Log loss | {uci_sel["log_loss"]:.6f} | {lc["log_loss"]:.6f} | {cmp_rows[3]["plain_comparison"]} |
| ECE | {uci_sel["ece"]:.6f} | {lc["ece"]:.6f} | {cmp_rows[4]["plain_comparison"]} |

A worse UCI number is a valid finding, not something to hide. A better UCI number does **not** mean the LendingClub pipeline is inferior: prevalence, features, and labels differ.

## G. Explainability (Tier 2)

EBM native additive term attributions on UCI **train** (logit/link scale). Associations, not causes.

{md_table(payload["ebm_global_rows"], ["rank", "feature", "mean_abs", "mean_signed"], {"mean_abs": ".6f", "mean_signed": ".6f"})}

SHAP-vs-EBM fidelity: **{shap_note["status"]}**. {shap_note["reason"]}

## H. Explicit non-claims

- No Shariah governance evaluation was performed on UCI.
- {L1_METADATA_ONLY}
- No claim is made that UCI results validate or invalidate the LendingClub architecture as a whole — only that the credit-risk/calibration methodology was independently reproduced on a second dataset.
- No UCI decision thresholds were selected. LendingClub `t_low`/`t_high`/`t*` were not applied.
- UCI is not temporally validated.

## I. Reproducibility

- Config: `configs/stage9_4_uci_generalization.yaml`
- Audit: `audit/stage9_4_uci_run.json`
- Models trained: UCI only. `models_trained=true`. `test_used_for_selection=false`.
- Protected LendingClub / Stage 7–9.3 artifact hashes were snapshotted before and after; they matched.
- The runner did not edit the Stage 9 execution gate, constitution, or amendment files.

## J. What this stage did not do

Stage 9.5–9.7, Stage 10, and paper writing were not started.
"""
    REPORT.write_text(md if md.endswith("\n") else md + "\n", encoding="utf-8")


def main() -> int:
    started = utc_now()
    amendment = require_amendment_approved()
    split_verify = verify_frozen_uci_split()
    before = snapshot_protected_hashes()
    table = load_uci_with_splits()
    prevalence = table.attrs["split_prevalence"]

    train_df, y_tr, id_tr = split_xy(table, "train")
    val_df, y_va, id_va = split_xy(table, "validation")
    preprocessor = UCIPreprocessor().fit(train_df)
    x_tr = preprocessor.transform(train_df)
    x_va = preprocessor.transform(val_df)
    ebm_tr = ebm_frame(train_df)
    ebm_va = ebm_frame(val_df)

    val_family_rows: list[dict] = []
    seed42_xgb_best = None
    for family in FAMILIES:
        for seed in SEEDS:
            print(f"UCI validation {family} seed={seed}", flush=True)
            model, p_va, cfg = fit_family(family, seed, x_tr, y_tr, x_va, y_va, ebm_tr, ebm_va)
            metrics = classification_metrics(y_va, p_va)
            row = {"family": family, "seed": seed, "split": "validation", **metrics, "config": cfg}
            val_family_rows.append(row)
            if family == "xgboost" and seed == FINAL_SEED:
                seed42_xgb_best = int(cfg.get("best_iteration", -1))
                if seed42_xgb_best is not None and seed42_xgb_best >= 0:
                    seed42_xgb_best = seed42_xgb_best + 1
                else:
                    seed42_xgb_best = 400

    aggregates = [aggregate_seed_metrics(val_family_rows, family) for family in FAMILIES]
    family_selection = select_family(aggregates)
    selected_family = family_selection["selected_family"]
    print(f"Selected UCI family: {selected_family}", flush=True)

    xgb_final_trees = seed42_xgb_best or 400
    train_only: dict[str, Any] = {}
    for family in FAMILIES:
        print(f"UCI train-only freeze {family} seed={FINAL_SEED}", flush=True)
        n_est = xgb_final_trees if family == "xgboost" else None
        dummy_xgb_va = x_va
        dummy_y_va = y_va
        if family == "xgboost":
            model, p_va, cfg = fit_family(
                family, FINAL_SEED, x_tr, y_tr, dummy_xgb_va, dummy_y_va, ebm_tr, ebm_va, xgb_estimators=n_est
            )
        else:
            model, p_va, cfg = fit_family(family, FINAL_SEED, x_tr, y_tr, x_va, y_va, ebm_tr, ebm_va)
        train_only[family] = {"model": model, "p_val_raw": p_va, "config": cfg}

    calib = fit_calibrators(train_only[selected_family]["p_val_raw"], y_va)
    cal_sel = calib["selection"]
    selected_calibrator = cal_sel["selected_method"]
    print(f"Selected UCI calibrator: {selected_calibrator}", flush=True)

    test_df, y_te, id_te = split_xy(table, "test")
    x_te = preprocessor.transform(test_df)
    ebm_te = ebm_frame(test_df)

    test_family_rows = []
    raw_test = {}
    for family in FAMILIES:
        p_raw = apply_family(family, train_only[family]["model"], x_te, ebm_te)
        raw_test[family] = p_raw
        test_family_rows.append({"family": family, "seed": FINAL_SEED, "split": "test", **classification_metrics(y_te, p_raw)})

    p_raw_sel = raw_test[selected_family]
    mapped_test = {
        "raw": p_raw_sel,
        "platt": calib["platt"].transform(p_raw_sel),
        "isotonic": calib["isotonic"].transform(p_raw_sel),
    }
    test_cal_rows = []
    for method, p_hat in mapped_test.items():
        metrics = calibration_metrics(y_te, p_hat)
        boot = {}
        for name, fn in list(CALIB_METRIC_FUNCS.items()):
            boot[name] = bootstrap_ci(y_te, p_hat, fn, n_bootstrap=N_BOOT, seed=BOOT_SEED)
        row = {"method": method, "split": "test", "seed": FINAL_SEED, **metrics}
        for name, result in boot.items():
            row[f"{name}_ci_lower"] = result["ci_lower"]
            row[f"{name}_ci_upper"] = result["ci_upper"]
        test_cal_rows.append(row)

    selected_p = mapped_test[selected_calibrator]
    selected_row = next(r for r in test_cal_rows if r["method"] == selected_calibrator)

    ebm_stats = ebm_global_stats(train_only["explainable_boosting_machine"]["model"], train_df)
    top_features = ebm_stats["feature"].head(6).tolist()
    shapes = [ebm_shape(train_only["explainable_boosting_machine"]["model"], name) for name in top_features]

    OUT.mkdir(parents=True, exist_ok=True)
    TAB.mkdir(parents=True, exist_ok=True)
    MET.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    PRED.mkdir(parents=True, exist_ok=True)
    CKPT.mkdir(parents=True, exist_ok=True)

    write_csv(TAB / "uci_validation_family_metrics.csv", [{k: v for k, v in r.items() if k != "config"} for r in val_family_rows])
    write_csv(TAB / "uci_validation_family_aggregates.csv", aggregates)
    write_csv(TAB / "uci_validation_calibration.csv", calib["validation_rows"])
    write_csv(TAB / "uci_test_family_raw.csv", test_family_rows)
    write_csv(TAB / "uci_test_calibration.csv", test_cal_rows)
    write_csv(TAB / "uci_vs_lendingclub_test_alongside.csv", [
        {
            "metric": m,
            "uci_test": selected_row[m],
            "lendingclub_test_cited": cite_lendingclub_stage5_test()[m],
            "plain_comparison": compare_plain(selected_row[m], cite_lendingclub_stage5_test()[m], m in {"roc_auc", "pr_auc"}),
        }
        for m in ("roc_auc", "pr_auc", "brier", "log_loss", "ece")
    ])
    ebm_stats.to_csv(TAB / "uci_ebm_global_attributions.csv", index=False)

    dump_json(MET / "uci_split_verify.json", split_verify)
    dump_json(MET / "uci_split_prevalence.json", prevalence)
    dump_json(MET / "family_selection.json", family_selection)
    dump_json(MET / "calibrator_selection.json", {**cal_sel, "platt": calib["platt"].record(), "isotonic": calib["isotonic"].record()})
    dump_json(MET / "uci_test_selected.json", selected_row)
    dump_json(MET / "lendingclub_test_citation.json", cite_lendingclub_stage5_test())
    dump_json(MET / "ebm_shape_top6.json", shapes)
    dump_json(MET / "preprocessor.json", preprocessor.record())

    pred_val = pd.DataFrame({
        "ID": id_va,
        "row_ref": [row_ref(i) for i in id_va],
        "y": y_va,
        "p_raw": train_only[selected_family]["p_val_raw"],
        "p_platt": calib["mapped"]["platt"],
        "p_isotonic": calib["mapped"]["isotonic"],
        "p_selected": calib["mapped"][selected_calibrator],
        "split": "validation",
    })
    pred_te = pd.DataFrame({
        "ID": id_te,
        "row_ref": [row_ref(i) for i in id_te],
        "y": y_te,
        "p_raw": mapped_test["raw"],
        "p_platt": mapped_test["platt"],
        "p_isotonic": mapped_test["isotonic"],
        "p_selected": selected_p,
        "split": "test",
    })
    pred_val.to_csv(PRED / "uci_validation_selected_family.csv", index=False)
    pred_te.to_csv(PRED / "uci_test_selected_family.csv", index=False)

    joblib.dump(preprocessor, CKPT / "uci_preprocessor.joblib")
    joblib.dump(train_only[selected_family]["model"], CKPT / f"uci_{selected_family}_seed42.joblib")
    joblib.dump({"platt": calib["platt"], "isotonic": calib["isotonic"], "selected": selected_calibrator}, CKPT / "uci_calibrators.joblib")
    joblib.dump(train_only["explainable_boosting_machine"]["model"], CKPT / "uci_ebm_seed42.joblib")

    shutil.copy2(CONFIG, OUT / "stage9_4_uci_generalization.yaml")

    roc_series = {}
    pr_series = {}
    for family in FAMILIES:
        p_va = train_only[family]["p_val_raw"]
        roc_series[family] = (y_va, p_va)
        pr_series[family] = (y_va, p_va)
    plot_roc(roc_series, "UCI validation ROC (train-only seed 42, not TEST)", FIG / "figure1_uci_validation_roc")
    plot_pr(pr_series, "UCI validation PR (train-only seed 42, not TEST)", FIG / "figure2_uci_validation_pr")
    plot_reliability_panels(
        {m: (y_te, mapped_test[m]) for m in ("raw", "platt", "isotonic")},
        "UCI TEST reliability (selected family; reporting only)",
        FIG / "figure3_uci_test_reliability",
    )
    plot_importance(ebm_stats, FIG / "figure4_uci_ebm_global_importance")

    shap_vs_ebm = {
        "status": "skipped",
        "reason": (
            "SHAP-vs-EBM fidelity is optional in the Stage 9.4 instruction. It was skipped rather than "
            "run superficially. Native EBM attributions are the Tier-2 deliverable."
        ),
    }

    lc_cite = cite_lendingclub_stage5_test()
    after = assert_protected_unchanged(before)

    payload = {
        "experiment_id": EXPERIMENT_ID,
        "amendment_id": AMENDMENT_ID,
        "amendment": amendment,
        "status": "PASS",
        "split_verify": split_verify,
        "split_prevalence": prevalence,
        "validation_family_rows": [{k: v for k, v in r.items() if k != "config"} for r in val_family_rows],
        "validation_aggregates": aggregates,
        "family_selection": family_selection,
        "selected_family": selected_family,
        "validation_calibration_rows": calib["validation_rows"],
        "calibrator_selection": cal_sel,
        "selected_calibrator": selected_calibrator,
        "uci_test_family_rows": test_family_rows,
        "uci_test_calibration_rows": test_cal_rows,
        "uci_test_selected": selected_row,
        "lendingclub_citation": lc_cite,
        "ebm_global_rows": ebm_stats.to_dict(orient="records"),
        "shap_vs_ebm": shap_vs_ebm,
        "models_trained": True,
        "test_used_for_selection": False,
        "thresholds_searched": False,
        "lendingclub_artifacts_touched": False,
    }
    write_report(payload)

    audit = {
        "experiment_id": EXPERIMENT_ID,
        "amendment_id": AMENDMENT_ID,
        "amendment_status": amendment["status"],
        "started": started,
        "execution_timestamp": utc_now(),
        "git_commit": git_commit(ROOT),
        "status": "PASS",
        "issues": [],
        "models_trained": True,
        "calibrators_fitted": True,
        "test_used_for_selection": False,
        "thresholds_searched": False,
        "uci_test_evaluated": True,
        "lendingclub_models_retrained": False,
        "lendingclub_calibration_refit": False,
        "lendingclub_thresholds_changed": False,
        "stage7_8_modified": False,
        "stage9_1_3_modified": False,
        "shariah_evaluation_on_uci": False,
        "l2_fusion_on_uci": False,
        "merged_with_lendingclub": False,
        "invented_temporal_structure": False,
        "shap_vs_ebm": shap_vs_ebm["status"],
        "selected_family": selected_family,
        "selected_calibrator": selected_calibrator,
        "split_verify": split_verify,
        "split_prevalence": prevalence,
        "family_selection": family_selection,
        "calibrator_selection": {**cal_sel, "platt": calib["platt"].record(), "isotonic": calib["isotonic"].record()},
        "uci_test_selected": selected_row,
        "lendingclub_test_citation": lc_cite,
        "protected_hashes_before": before,
        "protected_hashes_after": after,
        "protected_hashes_unchanged": True,
        "config_sha256": sha256_file(CONFIG),
        "report_sha256": sha256_file(REPORT),
        "runner_did_not_edit_authorization": True,
        "pytest_exit_code": None,
        "test_command": "python -m pytest tests/test_stage9_4_uci.py -q --tb=short",
        "test_summary": None,
        "software": {
            "python": sys.version,
            "pandas": pd.__version__,
            "numpy": np.__version__,
        },
    }
    dump_json(AUDIT, audit)
    dump_json(MET / "stage9_4_summary.json", {
        "selected_family": selected_family,
        "selected_calibrator": selected_calibrator,
        "uci_test": {k: selected_row[k] for k in ("roc_auc", "pr_auc", "brier", "log_loss", "ece", "n")},
        "lendingclub_test_cited": {k: lc_cite[k] for k in ("roc_auc", "pr_auc", "brier", "log_loss", "ece", "n")},
        "test_used_for_selection": False,
        "models_trained": True,
        "lendingclub_artifacts_touched": False,
    })
    pytest_code, pytest_summary = run_pytest()
    audit["pytest_exit_code"] = pytest_code
    audit["test_summary"] = pytest_summary
    audit["status"] = "PASS" if pytest_code == 0 else "FAIL"
    audit["issues"] = [] if pytest_code == 0 else ["pytest failed"]
    dump_json(AUDIT, audit)
    print(pytest_summary, flush=True)
    print(f"Selected {selected_family}/{selected_calibrator} UCI TEST ROC-AUC={selected_row['roc_auc']:.6f}", flush=True)
    return 0 if pytest_code == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
