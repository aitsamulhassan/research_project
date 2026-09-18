"""Stage 5 probability calibration.

Calibrators are fit on validation scores from the Stage 4B selected family
(EBM) trained on TRAIN only. TEST labels are not used until after the
calibration method is frozen.
"""

from __future__ import annotations

import gc
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from calibration.isotonic import IsotonicCalibrator  # noqa: E402
from calibration.metrics import (  # noqa: E402
    CALIB_METRIC_FUNCS,
    ECE_RECORD,
    calibration_metrics,
    ece,
    risk_range_table,
)
from calibration.platt import PlattCalibrator  # noqa: E402
from calibration.reliability import (  # noqa: E402
    plot_brier_comparison,
    plot_reliability_overlay,
    plot_reliability_panels,
    plot_risk_range_gaps,
    plot_temporal,
)
from data.audit_datasets import EXPECTED_LC_FILENAME, RAW_DIR, git_commit, sha256_file  # noqa: E402
from evaluation.bootstrap import bootstrap_ci, bootstrap_paired_diff  # noqa: E402
from models.common import FINAL_SEED, SEEDS, assert_predictor_frame, row_ref  # noqa: E402
from models.ebm_model import ebm_config, ebm_model  # noqa: E402
from preprocessing.lendingclub_preprocessor import (  # noqa: E402
    ASSIGNMENTS_PATH,
    FEATURE_POLICY_PATH,
    FORBIDDEN_COLUMNS,
    PREPROCESS_POLICY_PATH,
    PRIMARY_PREDICTORS,
    PREPROCESSOR_PATH,
    RECORDED_LC_SHA256,
    LendingClubPreprocessor,
    sha256_text_file,
)

CALIB_EXPERIMENT_ID = "stage5-lc-ebm-calibration-v1"
STAGE4B_ID = "stage4b-lc-granting-v1"
FAMILY = "explainable_boosting_machine"
BRIER_TIE = 0.001
SIMPLICITY = ["raw", "platt", "isotonic"]
N_BOOT = 1000
BOOT_SEED = 42
METHODS = ["raw", "platt", "isotonic"]

EXP_DIR = ROOT / "experiments" / "stage5_calibration"
CKPT_DIR = EXP_DIR / "checkpoints"
OUT_DIR = ROOT / "results" / "calibration"
FIG_DIR = ROOT / "results" / "figures" / "calibration"
AUDIT_DIR = ROOT / "audit"
SPLIT_MANIFEST = ROOT / "audit" / "lendingclub_split_manifest.json"
STAGE4B_SELECTION = ROOT / "experiments" / "stage4b_credit_risk" / "selected_configurations.json"
STAGE4B_VAL = ROOT / "results" / "predictions" / "validation"
SELECTION_RULE_PATH = EXP_DIR / "selection_rule.json"
SELECTION_PATH = EXP_DIR / "selected_calibration.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def load_table() -> pd.DataFrame:
    usecols = ["id", "Default", *PRIMARY_PREDICTORS]
    raw = pd.read_csv(RAW_DIR / EXPECTED_LC_FILENAME, usecols=usecols, low_memory=False)
    if FORBIDDEN_COLUMNS.intersection(PRIMARY_PREDICTORS):
        raise RuntimeError("Frozen predictors include excluded columns.")
    assign = pd.read_csv(ASSIGNMENTS_PATH, usecols=["id", "split", "issue_month"])
    merged = raw.merge(assign, on="id", how="inner")
    if len(merged) != len(raw):
        raise RuntimeError("Assignments do not match raw rows 1:1.")
    merged["year"] = merged["issue_month"].astype(str).str.slice(0, 4).astype(int)
    return merged


def split_xy(table: pd.DataFrame, split: str):
    part = table.loc[table["split"] == split].reset_index(drop=True)
    x = part.loc[:, PRIMARY_PREDICTORS].copy()
    assert_predictor_frame(x)
    return x, part["Default"].to_numpy(), part["id"].to_numpy(), part["year"].to_numpy()


def select_method(val_rows: list[dict]) -> dict:
    by = {r["method"]: r for r in val_rows}
    best = min(by[m]["brier"] for m in METHODS)
    candidates = [m for m in METHODS if by[m]["brier"] - best <= BRIER_TIE]
    chosen = sorted(candidates, key=SIMPLICITY.index)[0]
    reason = (
        f"Primary criterion is validation Brier. Best Brier={best:.6f}. "
        f"Methods within {BRIER_TIE} (practically indistinguishable): {candidates}. "
        f"Among those, simplicity order {SIMPLICITY} selected `{chosen}` "
        f"(Brier={by[chosen]['brier']:.6f}, log_loss={by[chosen]['log_loss']:.6f}, "
        f"ECE={by[chosen]['ece']:.6f})."
    )
    return {
        "selected_method": chosen,
        "reason": reason,
        "candidates": candidates,
        "best_brier": best,
        "declared_before_test": True,
        "indistinguishable_brier": BRIER_TIE,
        "simplicity_order": SIMPLICITY,
        "timestamp": utc_now(),
    }


def train_only_raw_predictions() -> dict:
    raw_val_path = OUT_DIR / "raw" / "ebm_train_only_seed42_validation.csv"
    raw_te_path = OUT_DIR / "raw" / "ebm_train_only_seed42_test.csv"
    meta_path = CKPT_DIR / "train_only_ebm_meta.json"
    if raw_val_path.exists() and raw_te_path.exists() and meta_path.exists():
        val = pd.read_csv(raw_val_path)
        te = pd.read_csv(raw_te_path)
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return {"val": val, "test": te, "meta": meta, "reused": True}

    table = load_table()
    x_tr, y_tr, id_tr, year_tr = split_xy(table, "train")
    x_va, y_va, id_va, year_va = split_xy(table, "validation")
    x_te, y_te, id_te, year_te = split_xy(table, "test")
    del table
    gc.collect()

    if PREPROCESSOR_PATH.exists():
        prep = joblib.load(PREPROCESSOR_PATH)
    else:
        prep = LendingClubPreprocessor()
        prep.fit(x_tr)
    ebm_tr = prep.transform_imputed_frame(x_tr)
    ebm_va = prep.transform_imputed_frame(x_va)
    ebm_te = prep.transform_imputed_frame(x_te)
    del x_tr, x_va, x_te
    gc.collect()

    model = ebm_model(FINAL_SEED)
    print("Fitting TRAIN-only EBM seed 42 for Stage 5 raw scores", flush=True)
    model.fit(ebm_tr, y_tr)
    p_va = model.predict_proba(ebm_va)[:, 1]
    p_te = model.predict_proba(ebm_te)[:, 1]
    stored = pd.read_csv(STAGE4B_VAL / f"{FAMILY}_seed{FINAL_SEED}.csv")
    refs = [row_ref(i) for i in id_va]
    stored_aligned = stored.set_index("row_ref").loc[refs, "p_hat"].to_numpy()
    max_abs = float(np.max(np.abs(p_va - stored_aligned)))
    meta = {
        "family": FAMILY,
        "seed": FINAL_SEED,
        "trained_on": "TRAIN_ONLY",
        "preprocessor": "results/artifacts/lendingclub_preprocessor.joblib",
        "stage4b_val_max_abs_diff": max_abs,
        "config": ebm_config(FINAL_SEED),
        "n_train": int(len(y_tr)),
        "n_val": int(len(y_va)),
        "n_test": int(len(y_te)),
    }
    val = pd.DataFrame(
        {
            "row_ref": [row_ref(i) for i in id_va],
            "split": "validation",
            "year": year_va,
            "y_true": y_va.astype(int),
            "p_raw": p_va,
            "model": FAMILY,
            "seed": FINAL_SEED,
            "experiment_id": CALIB_EXPERIMENT_ID,
        }
    )
    te = pd.DataFrame(
        {
            "row_ref": [row_ref(i) for i in id_te],
            "split": "test",
            "year": year_te,
            "y_true": y_te.astype(int),
            "p_raw": p_te,
            "model": FAMILY,
            "seed": FINAL_SEED,
            "experiment_id": CALIB_EXPERIMENT_ID,
        }
    )
    raw_val_path.parent.mkdir(parents=True, exist_ok=True)
    val.to_csv(raw_val_path, index=False)
    te.to_csv(raw_te_path, index=False)
    dump_json(meta_path, meta)
    joblib.dump(model, OUT_DIR / "artifacts" / "ebm_train_only_seed42.joblib")
    return {"val": val, "test": te, "meta": meta, "reused": False}


def apply_and_save(base: pd.DataFrame, p_platt, p_iso, selected: str, path: Path) -> pd.DataFrame:
    out = base.copy()
    out["p_platt"] = p_platt
    out["p_isotonic"] = p_iso
    out["p_selected"] = out[{"raw": "p_raw", "platt": "p_platt", "isotonic": "p_isotonic"}[selected]]
    out["selected_method"] = selected
    path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(path, index=False)
    return out


def method_probs(frame: pd.DataFrame) -> dict[str, np.ndarray]:
    return {
        "raw": frame["p_raw"].to_numpy(),
        "platt": frame["p_platt"].to_numpy(),
        "isotonic": frame["p_isotonic"].to_numpy(),
    }


def seed_stability() -> list[dict]:
    rows = []
    for seed in SEEDS:
        stored = pd.read_csv(STAGE4B_VAL / f"{FAMILY}_seed{seed}.csv")
        y = stored["y_true"].to_numpy()
        p_raw = stored["p_hat"].to_numpy()
        platt = PlattCalibrator().fit(p_raw, y, split="validation")
        iso = IsotonicCalibrator().fit(p_raw, y, split="validation")
        probs = {"raw": p_raw, "platt": platt.transform(p_raw), "isotonic": iso.transform(p_raw)}
        method_rows = []
        for method, p in probs.items():
            metrics = calibration_metrics(y, p)
            rec = {"seed": seed, "method": method, "source": "stage4b_stored_validation", **metrics}
            method_rows.append(rec)
            rows.append(rec)
        choice = select_method(method_rows)
        for rec in rows[-3:]:
            rec["selected_on_this_seed"] = choice["selected_method"]
    return rows


def run_pytest() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests"), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, text.strip()


def fmt_ci(row: dict, key: str) -> str:
    return f"[{row[f'{key}_ci_lower']:.6f}, {row[f'{key}_ci_upper']:.6f}]"


def write_report(payload: dict) -> None:
    val_rows = payload["val_rows"]
    test_rows = payload["test_rows"]
    paired = payload["paired"]
    temporal = payload["temporal"]
    risk = payload["risk"]
    stability = payload["stability"]
    selection = payload["selection"]
    lines = [
        "# Stage 5 Calibration Report",
        "",
        "## A. Calibration protocol",
        "",
        "Selected Stage 4B family: Explainable Boosting Machine. Stage 4B model-selection decisions were not changed.",
        "",
        "Protocol: TRAIN-only EBM (seed 42, frozen Stage 4B hyperparameters) produces raw probabilities. Platt and isotonic calibrators are fit on VALIDATION raw probabilities and labels only. The calibration method is frozen using validation Brier (with a 0.001 practical-tie rule preferring simpler methods). Frozen calibrators are then applied to TEST raw probabilities. Calibrators were **not** refit on TRAIN+VALIDATION.",
        "",
        "Platt form: `sigmoid(a * logit(p_raw) + b)`, unregularized logistic regression (`C=np.inf`, solver `lbfgs`) on `logit(p_raw)`. Stage 4B stored probabilities rather than decision scores, so logit of the probability is the raw score.",
        "",
        "Isotonic: `sklearn.isotonic.IsotonicRegression(y_min=0, y_max=1, increasing=True, out_of_bounds='clip')`.",
        "",
        f"ECE: {ECE_RECORD['n_bins']} equal-width bins on [0,1]; empty bins excluded from ECE and MCE.",
        "",
        f"TRAIN-only EBM vs Stage 4B stored validation probabilities: max abs diff = {payload['raw_meta'].get('stage4b_val_max_abs_diff')}.",
        "",
        "## B. Validation results",
        "",
        "| Method | Brier | Log Loss | ECE | MCE | ROC-AUC | PR-AUC |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in val_rows:
        lines.append(
            f"| {r['method'].upper()} | {r['brier']:.6f} | {r['log_loss']:.6f} | {r['ece']:.6f} | {r['mce']:.6f} | {r['roc_auc']:.6f} | {r['pr_auc']:.6f} |"
        )
    lines += [
        "",
        "## C. Selected calibration method",
        "",
        f"Selected method: `{selection['selected_method']}`.",
        selection["reason"],
        "",
        "Selection used validation metrics only. Test metrics were not consulted.",
        "",
        "## D. Final test results",
        "",
        "| Method | Brier | 95% CI | Log Loss | 95% CI | ECE | 95% CI | MCE | 95% CI | ROC-AUC | PR-AUC |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in test_rows:
        lines.append(
            "| {m} | {b:.6f} | {bci} | {ll:.6f} | {llci} | {e:.6f} | {eci} | {mc:.6f} | {mci} | {roc:.6f} | {pr:.6f} |".format(
                m=r["method"].upper(),
                b=r["brier"],
                bci=fmt_ci(r, "brier"),
                ll=r["log_loss"],
                llci=fmt_ci(r, "log_loss"),
                e=r["ece"],
                eci=fmt_ci(r, "ece"),
                mc=r["mce"],
                mci=fmt_ci(r, "mce"),
                roc=r["roc_auc"],
                pr=r["pr_auc"],
            )
        )
    lines += [
        "",
        "Bootstrap: 1000 row resamples, percentile 95% CI, seed 42. Not used for tuning. Negative Brier/log-loss/ECE/MCE differences mean improvement.",
        "",
        "ROC-AUC and PR-AUC are reported to check ranking. Calibration is not claimed to improve discrimination.",
        "",
        "## E. Calibration curves",
        "",
        "Validation reliability diagrams: `results/figures/calibration/figure1_validation_reliability`.",
        "Test reliability diagrams for RAW, Platt, and isotonic (reporting only): `results/figures/calibration/figure2_test_reliability`.",
        "",
        "## F. Paired differences",
        "",
        "| Comparison | Metric | Difference | 95% CI |",
        "| --- | --- | --- | --- |",
    ]
    for r in paired:
        lines.append(
            f"| {r['comparison']} | {r['metric']} | {r['difference']:.6f} | [{r['ci_lower']:.6f}, {r['ci_upper']:.6f}] |"
        )
    lines += [
        "",
        "Difference = calibrated − raw. Intervals are percentile bootstrap intervals for that difference. This report does not interpret interval exclusion of zero as a hypothesis test p-value.",
        "",
        "## G. Temporal robustness",
        "",
        "| Method | Year | Brier | Log Loss | ECE |",
        "| --- | --- | --- | --- | --- |",
    ]
    for r in temporal:
        lines.append(
            f"| {r['method'].upper()} | {r['year']} | {r['brier']:.6f} | {r['log_loss']:.6f} | {r['ece']:.6f} |"
        )
    lines += [
        "",
        "Year slices are descriptive. Models and calibrators were not refit by year.",
        "",
        "## H. Seed stability",
        "",
        "For each Stage 4B seed, Platt and isotonic were fit on that seed's stored TRAIN-only validation predictions (never test). The same selection rule was applied.",
        "",
        "| Seed | RAW Brier | Platt Brier | Isotonic Brier | Selected |",
        "| --- | --- | --- | --- | --- |",
    ]
    for seed in SEEDS:
        sub = [r for r in stability if r["seed"] == seed]
        b = {r["method"]: r["brier"] for r in sub}
        chosen = sub[0]["selected_on_this_seed"]
        lines.append(f"| {seed} | {b['raw']:.6f} | {b['platt']:.6f} | {b['isotonic']:.6f} | {chosen} |")
    lines += [
        "",
        "## I. Leakage audit",
        "",
        "- Calibrator `.fit` methods raise if `split != 'validation'`.",
        "- Selection file is written before test metrics are computed.",
        "- Test labels are used only after freeze, and only to compute reporting metrics.",
        "- No test-set Brier/ECE was used to choose Platt vs isotonic vs raw.",
        "- Feature policy is unchanged; calibration maps a scalar probability and cannot add predictors.",
        "- Stage 4B TRAIN+VALIDATION refit test probabilities were not used, because a calibrator fit on TRAIN-only validation scores is not a valid map for a different (train+val) model.",
        "",
        "## J. Tests",
        "",
        payload.get("test_suite_summary", "Not run."),
        "",
        "## K. Limitations",
        "",
        "- Validation selection for isotonic is optimistic because the isotonic map is fit and evaluated on the same validation predictions. The 0.001 Brier-tie rule reduces tiny overfits but does not remove this bias. TEST evaluation is the honest comparison.",
        "- No nested cross-fitting of the calibrator inside TRAIN was used. A TRAIN+VALIDATION model with a nested calibrator was not implemented; the simpler valid protocol was preserved.",
        "- Stage 5 RAW test metrics are from a TRAIN-only EBM and will not match Stage 4B's TRAIN+VALIDATION test numbers.",
        "- ECE/MCE depend on the declared 10 equal-width bins; they are not a universal standard.",
        "- Platt uses logit(p_raw) rather than an EBM decision_function object because Stage 4B artifacts store probabilities.",
        "- Decision thresholds and Shariah rules were not applied.",
        "",
        "## L. Stage gate",
        "",
        f"`STAGE_5_STATUS = {payload['status']}`",
        "",
        payload.get("status_reason", ""),
        "",
        "Stage 6 was not started.",
        "",
    ]
    (ROOT / "docs" / "STAGE_5_CALIBRATION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    issues: list[str] = []
    for path in (CKPT_DIR, OUT_DIR, FIG_DIR, OUT_DIR / "metrics", OUT_DIR / "tables", OUT_DIR / "artifacts"):
        path.mkdir(parents=True, exist_ok=True)

    dataset_hash = sha256_file(RAW_DIR / EXPECTED_LC_FILENAME)
    if dataset_hash != RECORDED_LC_SHA256:
        print("HARD STOP: raw hash changed.", file=sys.stderr)
        return 2

    stage4b_sel = json.loads(STAGE4B_SELECTION.read_text(encoding="utf-8"))
    if stage4b_sel["selected_family"] != FAMILY:
        print("HARD STOP: Stage 4B selected family is not EBM.", file=sys.stderr)
        return 2

    if not SELECTION_RULE_PATH.exists():
        dump_json(
            SELECTION_RULE_PATH,
            {
                "declared_before_test": True,
                "primary_criterion": "validation Brier score",
                "indistinguishable_brier": BRIER_TIE,
                "simplicity_order": SIMPLICITY,
                "secondary_inspected": ["log_loss", "ece", "mce"],
                "test_metrics_not_consulted": True,
                "ece_definition": ECE_RECORD,
                "timestamp": utc_now(),
            },
        )

    print("Seed-stability calibration on stored Stage 4B validation predictions", flush=True)
    stability = seed_stability()
    dump_json(OUT_DIR / "metrics" / "stage5_seed_stability.json", stability)

    print("TRAIN-only EBM raw probabilities", flush=True)
    raw = train_only_raw_predictions()
    val = raw["val"]
    y_va = val["y_true"].to_numpy()
    p_raw_va = val["p_raw"].to_numpy()

    platt = PlattCalibrator().fit(p_raw_va, y_va, split="validation")
    iso = IsotonicCalibrator().fit(p_raw_va, y_va, split="validation")
    dump_json(OUT_DIR / "artifacts" / "platt_record.json", platt.record())
    dump_json(OUT_DIR / "artifacts" / "isotonic_record.json", iso.record())
    joblib.dump(platt, OUT_DIR / "artifacts" / "platt_calibrator.joblib")
    joblib.dump(iso, OUT_DIR / "artifacts" / "isotonic_calibrator.joblib")

    p_platt_va = platt.transform(p_raw_va)
    p_iso_va = iso.transform(p_raw_va)
    val_probs = {"raw": p_raw_va, "platt": p_platt_va, "isotonic": p_iso_va}
    val_rows = [{"method": m, "split": "validation", **calibration_metrics(y_va, p)} for m, p in val_probs.items()]
    dump_json(OUT_DIR / "metrics" / "stage5_validation_metrics.json", val_rows)
    pd.DataFrame(val_rows).to_csv(OUT_DIR / "tables" / "stage5_validation_comparison.csv", index=False)

    if SELECTION_PATH.exists():
        selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
        print("Keeping previously frozen selected_calibration.json", flush=True)
    else:
        selection = select_method(val_rows)
        selection["platt"] = platt.record()
        selection["isotonic"] = iso.record()
        dump_json(SELECTION_PATH, selection)

    selected = selection["selected_method"]
    apply_and_save(val, p_platt_va, p_iso_va, selected, OUT_DIR / "validation" / "ebm_seed42_calibrated.csv")

    print("FROZEN calibration method; applying to TEST", flush=True)
    te = raw["test"]
    y_te = te["y_true"].to_numpy()
    p_raw_te = te["p_raw"].to_numpy()
    p_platt_te = platt.transform(p_raw_te)
    p_iso_te = iso.transform(p_raw_te)
    te_frame = apply_and_save(te, p_platt_te, p_iso_te, selected, OUT_DIR / "test" / "ebm_seed42_calibrated.csv")
    te_probs = method_probs(te_frame)

    test_rows = []
    for method, p in te_probs.items():
        metrics = calibration_metrics(y_te, p)
        rec = {"method": method, "split": "test", "seed": FINAL_SEED, **metrics}
        for name, fn in CALIB_METRIC_FUNCS.items():
            boot = bootstrap_ci(y_te, p, fn, n_bootstrap=N_BOOT, confidence_level=0.95, seed=BOOT_SEED)
            rec[f"{name}_ci_lower"] = boot["ci_lower"]
            rec[f"{name}_ci_upper"] = boot["ci_upper"]
        test_rows.append(rec)
        print(f"  TEST {method} Brier={metrics['brier']:.4f} ECE={metrics['ece']:.4f}", flush=True)

    paired = []
    for method in ("platt", "isotonic"):
        for name, fn in CALIB_METRIC_FUNCS.items():
            if name in ("roc_auc", "pr_auc"):
                continue
            diff = bootstrap_paired_diff(
                y_te, te_probs[method], te_probs["raw"], fn, n_bootstrap=N_BOOT, seed=BOOT_SEED
            )
            paired.append(
                {
                    "comparison": f"RAW vs {method.upper()}",
                    "metric": name,
                    "difference": diff["point"],
                    "ci_lower": diff["ci_lower"],
                    "ci_upper": diff["ci_upper"],
                    "direction": "calibrated_minus_raw",
                }
            )

    temporal = []
    years = te_frame["year"].to_numpy()
    for method, p in te_probs.items():
        for year in (2017, 2018):
            mask = years == year
            tm = calibration_metrics(y_te[mask], p[mask])
            temporal.append({"method": method, "year": year, "n": int(mask.sum()), **{k: tm[k] for k in ("brier", "log_loss", "ece", "mce", "roc_auc", "pr_auc")}})

    risk = []
    for method, p in te_probs.items():
        for row in risk_range_table(y_te, p):
            risk.append({"method": method, **row})

    pd.DataFrame(test_rows).to_csv(OUT_DIR / "tables" / "stage5_test_comparison.csv", index=False)
    pd.DataFrame(paired).to_csv(OUT_DIR / "tables" / "stage5_paired_differences.csv", index=False)
    pd.DataFrame(temporal).to_csv(OUT_DIR / "tables" / "stage5_temporal.csv", index=False)
    pd.DataFrame(risk).to_csv(OUT_DIR / "tables" / "stage5_risk_ranges.csv", index=False)
    dump_json(OUT_DIR / "metrics" / "stage5_test_metrics.json", test_rows)
    dump_json(OUT_DIR / "metrics" / "stage5_paired_differences.json", paired)
    dump_json(OUT_DIR / "metrics" / "stage5_temporal.json", temporal)
    dump_json(OUT_DIR / "metrics" / "stage5_risk_ranges.json", risk)

    val_series = {m: (y_va, val_probs[m]) for m in METHODS}
    test_series = {m: (y_te, te_probs[m]) for m in METHODS}
    plot_reliability_panels(val_series, "Validation reliability (used for method selection)", FIG_DIR / "figure1_validation_reliability")
    plot_reliability_panels(
        test_series,
        "Test reliability (reporting only; calibration method already frozen)",
        FIG_DIR / "figure2_test_reliability",
    )
    plot_brier_comparison(val_rows, test_rows, FIG_DIR / "figure3_brier_comparison")
    plot_risk_range_gaps(risk, FIG_DIR / "figure4_risk_range_gaps")
    plot_temporal(temporal, FIG_DIR / "figure5_temporal")

    import interpret
    import matplotlib
    import sklearn

    versions = {
        "python": sys.version.replace("\n", " "),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "sklearn": sklearn.__version__,
        "interpret": interpret.__version__,
        "matplotlib": matplotlib.__version__,
        "joblib": joblib.__version__,
    }

    print("Running pytest", flush=True)
    pytest_code, pytest_text = run_pytest()
    status = "PASS" if pytest_code == 0 and not issues else "BLOCKED"
    status_reason = (
        "Calibration experiments completed; method frozen on validation; test evaluated once; leakage tests passed."
        if status == "PASS"
        else f"pytest_exit={pytest_code}; issues={issues}"
    )
    report_payload = {
        "status": status,
        "status_reason": status_reason,
        "val_rows": val_rows,
        "test_rows": test_rows,
        "paired": paired,
        "temporal": temporal,
        "risk": risk,
        "stability": stability,
        "selection": selection,
        "raw_meta": raw["meta"],
        "test_suite_summary": pytest_text[-4000:] if pytest_text else f"pytest exit {pytest_code}",
        "issues": issues,
    }
    write_report(report_payload)
    dump_json(
        AUDIT_DIR / "stage5_calibration_run.json",
        {
            "calibration_experiment_id": CALIB_EXPERIMENT_ID,
            "base_model_experiment_id": STAGE4B_ID,
            "selected_family": FAMILY,
            "selected_calibration_method": selected,
            "dataset_hash": dataset_hash,
            "split_manifest_hash": sha256_text_file(SPLIT_MANIFEST),
            "feature_policy_hash": sha256_text_file(FEATURE_POLICY_PATH),
            "preprocessing_policy_hash": sha256_text_file(PREPROCESS_POLICY_PATH),
            "random_seed": FINAL_SEED,
            "software_library_versions": versions,
            "execution_timestamp": utc_now(),
            "git_commit": git_commit(ROOT),
            "ece": ECE_RECORD,
            "bootstrap": {
                "n_bootstrap": N_BOOT,
                "seed": BOOT_SEED,
                "confidence_level": 0.95,
                "method": "percentile_bootstrap_rows_with_replacement",
            },
            "protocol": "validation_only_calibration_no_train_val_calibrator_refit",
            "status": status,
            "status_reason": status_reason,
            "issues": issues,
            "pytest_exit_code": pytest_code,
            "platt": platt.record(),
            "isotonic": iso.record(),
            "train_only_vs_stage4b_val_max_abs_diff": raw["meta"].get("stage4b_val_max_abs_diff"),
        },
    )
    print(json.dumps({"status": status, "selected": selected, "issues": issues}, indent=2), flush=True)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
