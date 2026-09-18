"""Stage 4B leakage-safe credit-risk modeling.

Validation may inform family selection. The test set is used once after freeze.
"""

from __future__ import annotations

import gc
import json
import subprocess
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from scipy import sparse

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from data.audit_datasets import (  # noqa: E402
    EXPECTED_LC_FILENAME,
    RAW_DIR,
    git_commit,
    sha256_file,
)
from evaluation.bootstrap import bootstrap_ci  # noqa: E402
from evaluation.metrics import METRIC_FUNCS, classification_metrics  # noqa: E402
from evaluation.plots import plot_pr, plot_roc, plot_temporal  # noqa: E402
from models.common import EXPERIMENT_ID, FINAL_SEED, SEEDS, assert_predictor_frame, row_ref  # noqa: E402
from models.ebm_model import ebm_config, ebm_model  # noqa: E402
from models.logistic import logistic_config, logistic_pipeline  # noqa: E402
from models.random_forest import random_forest_config, random_forest_model  # noqa: E402
from models.xgboost_model import xgboost_config, xgboost_model  # noqa: E402
from preprocessing.lendingclub_preprocessor import (  # noqa: E402
    ASSIGNMENTS_PATH,
    FEATURE_POLICY_PATH,
    FORBIDDEN_COLUMNS,
    PREPROCESS_POLICY_PATH,
    PRIMARY_PREDICTORS,
    RECORDED_LC_SHA256,
    LendingClubPreprocessor,
    sha256_text_file,
)

FAMILIES = [
    "logistic_regression",
    "random_forest",
    "xgboost",
    "explainable_boosting_machine",
]
SIMPLICITY = [
    "logistic_regression",
    "explainable_boosting_machine",
    "random_forest",
    "xgboost",
]
N_BOOT = 1000
BOOT_SEED = 42
EXP_DIR = ROOT / "experiments" / "stage4b_credit_risk"
CKPT_DIR = EXP_DIR / "checkpoints"
PRED_DIR = ROOT / "results" / "predictions"
FIG_DIR = ROOT / "results" / "figures"
TABLE_DIR = ROOT / "results" / "tables"
METRICS_DIR = ROOT / "results" / "metrics"
ART_DIR = ROOT / "results" / "artifacts"
AUDIT_DIR = ROOT / "audit"
SPLIT_MANIFEST = ROOT / "audit" / "lendingclub_split_manifest.json"
SELECTION_PATH = EXP_DIR / "selected_configurations.json"
SELECTION_RULE_PATH = EXP_DIR / "selection_rule.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def dump_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def load_table() -> pd.DataFrame:
    usecols = ["id", "Default", *PRIMARY_PREDICTORS]
    raw = pd.read_csv(RAW_DIR / EXPECTED_LC_FILENAME, usecols=usecols, low_memory=False)
    forbidden = FORBIDDEN_COLUMNS.intersection(PRIMARY_PREDICTORS)
    if forbidden:
        raise RuntimeError(f"Frozen predictors include excluded columns: {forbidden}")
    assign = pd.read_csv(ASSIGNMENTS_PATH, usecols=["id", "split", "issue_month"])
    merged = raw.merge(assign, on="id", how="inner")
    if len(merged) != len(raw):
        raise RuntimeError("Assignments do not match raw rows 1:1.")
    merged["year"] = merged["issue_month"].astype(str).str.slice(0, 4).astype(int)
    return merged


def split_xy(table: pd.DataFrame, split: str) -> tuple[pd.DataFrame, np.ndarray, np.ndarray, np.ndarray]:
    part = table.loc[table["split"] == split].reset_index(drop=True)
    x = part.loc[:, PRIMARY_PREDICTORS].copy()
    assert_predictor_frame(x)
    y = part["Default"].to_numpy()
    ids = part["id"].to_numpy()
    years = part["year"].to_numpy()
    return x, y, ids, years


def to_rf_matrix(matrix):
    """Keep Random Forest on the Stage 4A matrix without densifying 1023 columns."""
    if sparse.issparse(matrix):
        return matrix.astype(np.float32).tocsc()
    return np.asarray(matrix, dtype=np.float32)


def xgb_n_trees(model) -> int:
    best = getattr(model, "best_iteration", None)
    if best is None:
        return int(model.get_booster().num_boosted_rounds())
    return int(best) + 1


def write_predictions(path: Path, ids, years, y, p, model: str, seed: int, split: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(
        {
            "row_ref": [row_ref(i) for i in ids],
            "split": split,
            "year": years,
            "y_true": y.astype(int),
            "p_hat": np.asarray(p, dtype=float),
            "model": model,
            "seed": seed,
            "experiment_id": EXPERIMENT_ID,
        }
    )
    frame.to_csv(path, index=False)


def fit_family_val(family, seed, x_tr, y_tr, x_va, y_va, frame_tr, frame_va):
    extra = {}
    if family == "logistic_regression":
        model = logistic_pipeline(seed)
        model.fit(x_tr, y_tr)
        clf = model.named_steps["clf"]
        n_iter = int(np.max(np.atleast_1d(clf.n_iter_)))
        extra = {"n_iter": n_iter, "converged": n_iter < clf.max_iter, "config": logistic_config(seed)}
        p_va = model.predict_proba(x_va)[:, 1]
    elif family == "random_forest":
        model = random_forest_model(seed)
        x_tr_s = to_rf_matrix(x_tr)
        x_va_s = to_rf_matrix(x_va)
        model.fit(x_tr_s, y_tr)
        extra = {"config": random_forest_config(seed)}
        p_va = model.predict_proba(x_va_s)[:, 1]
        del x_tr_s, x_va_s
    elif family == "xgboost":
        from models.common import scale_pos_weight

        model = xgboost_model(seed, y_tr, n_estimators=300, early_stopping_rounds=30)
        model.fit(x_tr, y_tr, eval_set=[(x_va, y_va)], verbose=False)
        best_iter = xgb_n_trees(model)
        extra = {
            "config": xgboost_config(seed, scale_pos_weight(y_tr), n_estimators=300),
            "best_iteration": best_iter,
        }
        p_va = model.predict_proba(x_va)[:, 1]
    elif family == "explainable_boosting_machine":
        model = ebm_model(seed)
        model.fit(frame_tr, y_tr)
        extra = {"config": ebm_config(seed)}
        p_va = model.predict_proba(frame_va)[:, 1]
    else:
        raise ValueError(family)
    return model, p_va, extra


def fit_family_final(family, seed, x_tv, y_tv, frame_tv, xgb_n_estimators: int):
    extra = {}
    if family == "logistic_regression":
        model = logistic_pipeline(seed)
        model.fit(x_tv, y_tv)
        clf = model.named_steps["clf"]
        n_iter = int(np.max(np.atleast_1d(clf.n_iter_)))
        extra = {"n_iter": n_iter, "converged": n_iter < clf.max_iter, "config": logistic_config(seed)}
    elif family == "random_forest":
        model = random_forest_model(seed)
        model.fit(to_rf_matrix(x_tv), y_tv)
        extra = {"config": random_forest_config(seed)}
    elif family == "xgboost":
        from models.common import scale_pos_weight

        model = xgboost_model(seed, y_tv, n_estimators=xgb_n_estimators, early_stopping_rounds=None)
        model.fit(x_tv, y_tv, verbose=False)
        extra = {
            "config": xgboost_config(seed, scale_pos_weight(y_tv), n_estimators=xgb_n_estimators),
            "early_stopping": False,
        }
    elif family == "explainable_boosting_machine":
        model = ebm_model(seed)
        model.fit(frame_tv, y_tv)
        extra = {"config": ebm_config(seed)}
    else:
        raise ValueError(family)
    return model, extra


def predict_family(family, model, x, frame):
    if family == "explainable_boosting_machine":
        return model.predict_proba(frame)[:, 1]
    if family == "random_forest":
        return model.predict_proba(to_rf_matrix(x))[:, 1]
    return model.predict_proba(x)[:, 1]


def aggregate(rows: list[dict], family: str) -> dict:
    sub = [r for r in rows if r["family"] == family]
    out = {"family": family, "n_seeds": len(sub)}
    for key in ("roc_auc", "pr_auc", "brier", "log_loss"):
        vals = np.array([r[key] for r in sub], dtype=float)
        out[f"{key}_mean"] = float(vals.mean())
        out[f"{key}_std"] = float(vals.std(ddof=1) if len(vals) > 1 else 0.0)
        out[f"{key}_min"] = float(vals.min())
        out[f"{key}_max"] = float(vals.max())
    return out


def select_family(aggregates: list[dict]) -> dict:
    """Pre-declared rule: mean PR-AUC, then Brier within 0.005, then simplicity."""
    best_pr = max(a["pr_auc_mean"] for a in aggregates)
    candidates = [a for a in aggregates if best_pr - a["pr_auc_mean"] <= 0.005]
    candidates.sort(key=lambda a: (a["brier_mean"], SIMPLICITY.index(a["family"])))
    chosen = candidates[0]["family"]
    ranked = sorted(
        (a["family"] for a in aggregates),
        key=lambda f: (
            -next(a["pr_auc_mean"] for a in aggregates if a["family"] == f),
            SIMPLICITY.index(f),
        ),
    )
    chosen_row = next(a for a in aggregates if a["family"] == chosen)
    reason = (
        f"Primary criterion is mean validation PR-AUC. Best PR-AUC is {best_pr:.6f}. "
        f"Candidates within 0.005: {[c['family'] for c in candidates]}. "
        f"Among those, lowest mean Brier then simplicity selected `{chosen}` "
        f"(PR-AUC={chosen_row['pr_auc_mean']:.6f}, Brier={chosen_row['brier_mean']:.6f})."
    )
    return {"selected_family": chosen, "reason": reason, "ranking": ranked}


def mean_sd(mean: float, sd: float) -> str:
    return f"{mean:.4f}±{sd:.4f}"


def validation_complete(val_rows: list[dict]) -> bool:
    expected = {(family, seed) for family in FAMILIES for seed in SEEDS}
    got = {(r["family"], r["seed"]) for r in val_rows}
    return expected <= got


def run_pytest() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests"), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, text.strip()


def write_report(payload: dict) -> None:
    val_rows = payload.get("validation_rows") or []
    agg = payload.get("validation_aggregates") or []
    test_rows = payload.get("test_rows") or []
    temporal = payload.get("temporal_rows") or []
    lines = [
        "# Stage 4B Modeling Report",
        "",
        "## A. Dataset actually used",
        "",
        f"- Dataset: LendingClub granting-model extract, SHA-256 `{payload.get('dataset_hash', '')}`",
        f"- Predictors: {', '.join(f'`{c}`' for c in PRIMARY_PREDICTORS)} (9 frozen fields; Stage 4A matrix width {payload.get('n_features_out', 'NA')})",
        f"- Train rows: {payload.get('n_train', 'NA')}",
        f"- Validation rows: {payload.get('n_val', 'NA')}",
        f"- Test rows: {payload.get('n_test', 'NA')}",
        "- UCI was not used or merged.",
        "",
        "## B. Models executed",
        "",
        json.dumps(payload.get("configs") or {}, indent=2),
        "",
        "## C. Validation results",
        "",
    ]
    if val_rows:
        lines += [
            "### Per seed",
            "",
            "| Model | Seed | ROC-AUC | PR-AUC | Brier | Log Loss |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for r in val_rows:
            lines.append(
                f"| {r['family']} | {r['seed']} | {r['roc_auc']:.6f} | {r['pr_auc']:.6f} | {r['brier']:.6f} | {r['log_loss']:.6f} |"
            )
        lines += [
            "",
            "### Aggregate across seeds",
            "",
            "| Model | ROC-AUC Mean±SD | PR-AUC Mean±SD | Brier Mean±SD | Log Loss Mean±SD |",
            "| --- | --- | --- | --- | --- |",
        ]
        for a in agg:
            lines.append(
                "| {family} | {roc} | {pr} | {brier} | {ll} |".format(
                    family=a["family"],
                    roc=mean_sd(a["roc_auc_mean"], a["roc_auc_std"]),
                    pr=mean_sd(a["pr_auc_mean"], a["pr_auc_std"]),
                    brier=mean_sd(a["brier_mean"], a["brier_std"]),
                    ll=mean_sd(a["log_loss_mean"], a["log_loss_std"]),
                )
            )
    else:
        lines.append("Validation did not complete.")
    lines += [
        "",
        "## D. Selected configurations",
        "",
    ]
    selection = payload.get("selection")
    if selection:
        lines += [
            f"Primary validation criterion: mean PR-AUC across seeds {SEEDS}.",
            f"Selected family: `{selection['selected_family']}`.",
            selection.get("reason", ""),
            "",
            "All completed families were still retrained on TRAIN+VALIDATION and evaluated once on TEST after freeze, unless the run was blocked first. Test numbers were not used to choose the family.",
            "",
        ]
    else:
        lines += ["Selection was not declared because validation was incomplete.", ""]
    lines += [
        "## E. Final test results",
        "",
    ]
    if test_rows:
        lines += [
            "| Model | ROC-AUC | 95% CI | PR-AUC | 95% CI | Brier | 95% CI | Log Loss | 95% CI |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
        for r in test_rows:
            lines.append(
                "| {m} | {roc:.6f} | [{roc_l:.6f}, {roc_u:.6f}] | {pr:.6f} | [{pr_l:.6f}, {pr_u:.6f}] | {brier:.6f} | [{b_l:.6f}, {b_u:.6f}] | {ll:.6f} | [{ll_l:.6f}, {ll_u:.6f}] |".format(
                    m=r["family"],
                    roc=r["roc_auc"],
                    roc_l=r["roc_auc_ci_lower"],
                    roc_u=r["roc_auc_ci_upper"],
                    pr=r["pr_auc"],
                    pr_l=r["pr_auc_ci_lower"],
                    pr_u=r["pr_auc_ci_upper"],
                    brier=r["brier"],
                    b_l=r["brier_ci_lower"],
                    b_u=r["brier_ci_upper"],
                    ll=r["log_loss"],
                    ll_l=r["log_loss_ci_lower"],
                    ll_u=r["log_loss_ci_upper"],
                )
            )
        lines += ["", "Bootstrap: 1000 row resamples, percentile 95% CI, seed 42. Not used for tuning.", ""]
    else:
        lines += ["Test evaluation was not performed.", ""]
    lines += [
        "## F. Temporal robustness",
        "",
    ]
    if temporal:
        lines += [
            "| Model | Year | ROC-AUC | PR-AUC | Brier |",
            "| --- | --- | --- | --- | --- |",
        ]
        for r in temporal:
            lines.append(f"| {r['model']} | {r['year']} | {r['roc_auc']:.6f} | {r['pr_auc']:.6f} | {r['brier']:.6f} |")
        lines += ["", "These year slices are descriptive and were not used to modify models.", ""]
    else:
        lines += ["Temporal test slices were not computed.", ""]
    lines += [
        "## G. Reproducibility",
        "",
        f"- experiment_id: `{EXPERIMENT_ID}`",
        f"- seeds: {SEEDS}; final test seed: {FINAL_SEED}",
        f"- dataset_hash: `{payload.get('dataset_hash', '')}`",
        f"- split_manifest_hash: `{payload.get('split_manifest_hash', '')}`",
        f"- preprocessing_policy_hash: `{payload.get('preprocessing_policy_hash', '')}`",
        f"- git_commit: `{payload.get('git_commit', '')}`",
        f"- libraries: {json.dumps(payload.get('library_versions') or {})}",
        "",
        "## H. Tests",
        "",
        payload.get("test_suite_summary", "Tests were not executed."),
        "",
        "## I. Unexpected issues",
        "",
    ]
    issues = payload.get("issues") or ["None recorded during execution."]
    lines.extend(f"- {item}" for item in issues)
    lines += [
        "",
        "## J. Stage gate",
        "",
        f"`STAGE_4B_STATUS = {payload['status']}`",
        "",
        payload.get("status_reason", ""),
        "",
        "Stage 5 was not started.",
        "",
    ]
    (ROOT / "docs" / "STAGE_4B_MODELING_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def library_versions() -> dict[str, str]:
    import interpret
    import matplotlib
    import sklearn
    import xgboost

    return {
        "python": sys.version.replace("\n", " "),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "sklearn": sklearn.__version__,
        "xgboost": xgboost.__version__,
        "interpret": interpret.__version__,
        "matplotlib": matplotlib.__version__,
        "joblib": joblib.__version__,
    }


def main() -> int:
    issues: list[str] = []
    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    PRED_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    ART_DIR.mkdir(parents=True, exist_ok=True)

    dataset_hash = sha256_file(RAW_DIR / EXPECTED_LC_FILENAME)
    if dataset_hash != RECORDED_LC_SHA256:
        print("HARD STOP: raw hash changed.", file=sys.stderr)
        return 2

    if not SELECTION_RULE_PATH.exists():
        dump_json(
            SELECTION_RULE_PATH,
            {
                "declared_before_test": True,
                "primary_criterion": "mean validation PR-AUC across frozen seeds",
                "secondary": "among families within 0.005 mean PR-AUC of the best, prefer lower mean Brier",
                "tie_break": SIMPLICITY,
                "test_metrics_not_consulted": True,
                "timestamp": utc_now(),
            },
        )

    table = load_table()
    x_train, y_train, id_train, year_train = split_xy(table, "train")
    x_val, y_val, id_val, year_val = split_xy(table, "validation")
    x_test, y_test, id_test, year_test = split_xy(table, "test")
    n_train, n_val, n_test = int(len(x_train)), int(len(x_val)), int(len(x_test))
    del table
    gc.collect()

    prep_train = LendingClubPreprocessor()
    prep_train.fit(x_train)
    xtr_mat = prep_train.transform(x_train)
    xva_mat = prep_train.transform(x_val)
    ebm_tr = prep_train.transform_imputed_frame(x_train)
    ebm_va = prep_train.transform_imputed_frame(x_val)
    n_features = int(xtr_mat.shape[1])

    val_rows: list[dict] = []
    xgb_best_iters: list[int] = []
    val_series_seed42: dict[str, tuple[np.ndarray, np.ndarray]] = {}

    for family in FAMILIES:
        for seed in SEEDS:
            ckpt = CKPT_DIR / f"val_{family}_{seed}.json"
            pred_path = PRED_DIR / "validation" / f"{family}_seed{seed}.csv"
            if ckpt.exists() and pred_path.exists():
                rec = json.loads(ckpt.read_text(encoding="utf-8"))
                val_rows.append(rec)
                if family == "xgboost" and "best_iteration" in rec:
                    xgb_best_iters.append(int(rec["best_iteration"]))
                if seed == FINAL_SEED:
                    saved = pd.read_csv(pred_path)
                    val_series_seed42[family] = (saved["y_true"].to_numpy(), saved["p_hat"].to_numpy())
                print(f"skip existing {family} seed {seed}", flush=True)
                continue
            print(f"VAL fit {family} seed {seed}", flush=True)
            try:
                model, p_va, extra = fit_family_val(
                    family, seed, xtr_mat, y_train, xva_mat, y_val, ebm_tr, ebm_va
                )
            except Exception as exc:
                issues.append(f"{family} seed {seed} failed: {exc}")
                dump_json(
                    CKPT_DIR / f"val_{family}_{seed}_ERROR.json",
                    {"error": str(exc), "trace": traceback.format_exc()},
                )
                print(traceback.format_exc(), flush=True)
                gc.collect()
                continue
            metrics = classification_metrics(y_val, p_va)
            rec = {
                "family": family,
                "seed": seed,
                "split": "validation",
                "experiment_id": EXPERIMENT_ID,
                **metrics,
                **{k: extra[k] for k in extra if k != "config"},
                "config": extra.get("config"),
            }
            dump_json(ckpt, rec)
            write_predictions(pred_path, id_val, year_val, y_val, p_va, family, seed, "validation")
            val_rows.append(rec)
            if family == "xgboost":
                xgb_best_iters.append(int(extra.get("best_iteration", 300)))
            if seed == FINAL_SEED:
                val_series_seed42[family] = (y_val, p_va)
            print(
                f"  PR-AUC={metrics['pr_auc']:.4f} ROC-AUC={metrics['roc_auc']:.4f} Brier={metrics['brier']:.4f}",
                flush=True,
            )
            del model, p_va
            gc.collect()

    versions = library_versions()
    hashes = {
        "dataset_hash": dataset_hash,
        "split_manifest_hash": sha256_text_file(SPLIT_MANIFEST),
        "feature_policy_hash": sha256_text_file(FEATURE_POLICY_PATH),
        "preprocessing_policy_hash": sha256_text_file(PREPROCESS_POLICY_PATH),
        "git_commit": git_commit(ROOT),
        "library_versions": versions,
        "n_train": n_train,
        "n_val": n_val,
        "n_test": n_test,
        "n_features_out": n_features,
        "issues": issues,
        "validation_rows": val_rows,
        "configs": {
            family: next((r.get("config") for r in val_rows if r["family"] == family), None)
            for family in FAMILIES
        },
    }

    if not validation_complete(val_rows):
        reason = "Not all model families completed all five validation seeds. Test was not touched."
        dump_json(
            AUDIT_DIR / "stage4b_modeling_run.json",
            {
                "experiment_id": EXPERIMENT_ID,
                "status": "BLOCKED",
                "reason": reason,
                **hashes,
                "execution_timestamp": utc_now(),
            },
        )
        write_report({**hashes, "status": "BLOCKED", "status_reason": reason, "test_suite_summary": "Not run; modeling blocked."})
        print("BLOCKED: incomplete validation families", issues, file=sys.stderr)
        return 2

    aggregates = [aggregate(val_rows, family) for family in FAMILIES]
    if SELECTION_PATH.exists():
        selection = json.loads(SELECTION_PATH.read_text(encoding="utf-8"))
        print("Keeping previously frozen selected_configurations.json", flush=True)
        xgb_n = int(selection.get("xgboost_frozen_n_estimators") or 300)
    else:
        selection = select_family(aggregates)
        xgb_n = int(np.median(xgb_best_iters)) if xgb_best_iters else 300
        xgb_n = max(50, min(300, xgb_n))
        selection["xgboost_frozen_n_estimators"] = xgb_n
        selection["declared_before_test"] = True
        selection["timestamp"] = utc_now()
        dump_json(SELECTION_PATH, selection)

    print("FROZEN selection written; beginning TRAIN+VAL refit and TEST eval", flush=True)
    x_tv = pd.concat([x_train, x_val], ignore_index=True)
    y_tv = np.concatenate([y_train, y_val])
    prep_tv = LendingClubPreprocessor()
    prep_tv.fit(x_tv)
    joblib.dump(prep_tv, ART_DIR / "preprocessor_train_plus_validation.joblib")
    xtv_mat = prep_tv.transform(x_tv)
    xte_mat = prep_tv.transform(x_test)
    ebm_tv = prep_tv.transform_imputed_frame(x_tv)
    ebm_te = prep_tv.transform_imputed_frame(x_test)
    del x_train, x_val, ebm_tr, ebm_va, xtr_mat, xva_mat, x_tv
    gc.collect()

    test_rows = []
    temporal_rows = []
    test_series = {}
    for family in FAMILIES:
        test_ckpt = CKPT_DIR / f"test_{family}_{FINAL_SEED}.json"
        pred_path = PRED_DIR / "test" / f"{family}_seed{FINAL_SEED}.csv"
        if test_ckpt.exists() and pred_path.exists():
            rec = json.loads(test_ckpt.read_text(encoding="utf-8"))
            test_rows.append(rec)
            saved = pd.read_csv(pred_path)
            p_te = saved["p_hat"].to_numpy()
            test_series[family] = (y_test, p_te)
            for year in (2017, 2018):
                mask = year_test == year
                tm = classification_metrics(y_test[mask], p_te[mask])
                temporal_rows.append(
                    {
                        "model": family,
                        "year": year,
                        "n": tm["n"],
                        "roc_auc": tm["roc_auc"],
                        "pr_auc": tm["pr_auc"],
                        "brier": tm["brier"],
                        "log_loss": tm["log_loss"],
                    }
                )
            print(f"skip existing TEST {family}", flush=True)
            continue
        print(f"TEST refit {family}", flush=True)
        try:
            model, extra = fit_family_final(family, FINAL_SEED, xtv_mat, y_tv, ebm_tv, xgb_n)
            p_te = predict_family(family, model, xte_mat, ebm_te)
        except Exception as exc:
            issues.append(f"TEST {family} failed: {exc}")
            dump_json(
                CKPT_DIR / f"test_{family}_{FINAL_SEED}_ERROR.json",
                {"error": str(exc), "trace": traceback.format_exc()},
            )
            print(traceback.format_exc(), flush=True)
            gc.collect()
            continue
        metrics = classification_metrics(y_test, p_te)
        boot = {
            name: bootstrap_ci(y_test, p_te, fn, n_bootstrap=N_BOOT, confidence_level=0.95, seed=BOOT_SEED)
            for name, fn in METRIC_FUNCS.items()
        }
        rec = {
            "family": family,
            "seed": FINAL_SEED,
            "split": "test",
            "experiment_id": EXPERIMENT_ID,
            "roc_auc": metrics["roc_auc"],
            "pr_auc": metrics["pr_auc"],
            "brier": metrics["brier"],
            "log_loss": metrics["log_loss"],
            "n": metrics["n"],
            "roc_auc_ci_lower": boot["roc_auc"]["ci_lower"],
            "roc_auc_ci_upper": boot["roc_auc"]["ci_upper"],
            "pr_auc_ci_lower": boot["pr_auc"]["ci_lower"],
            "pr_auc_ci_upper": boot["pr_auc"]["ci_upper"],
            "brier_ci_lower": boot["brier"]["ci_lower"],
            "brier_ci_upper": boot["brier"]["ci_upper"],
            "log_loss_ci_lower": boot["log_loss"]["ci_lower"],
            "log_loss_ci_upper": boot["log_loss"]["ci_upper"],
            "bootstrap": boot,
            "config": extra.get("config"),
        }
        dump_json(test_ckpt, rec)
        test_rows.append(rec)
        write_predictions(pred_path, id_test, year_test, y_test, p_te, family, FINAL_SEED, "test")
        joblib.dump(model, ART_DIR / f"final_{family}_seed{FINAL_SEED}.joblib")
        test_series[family] = (y_test, p_te)
        for year in (2017, 2018):
            mask = year_test == year
            if int(mask.sum()) < 100:
                issues.append(f"Year {year} has fewer than 100 test rows; metric still computed.")
            tm = classification_metrics(y_test[mask], p_te[mask])
            temporal_rows.append(
                {
                    "model": family,
                    "year": year,
                    "n": tm["n"],
                    "roc_auc": tm["roc_auc"],
                    "pr_auc": tm["pr_auc"],
                    "brier": tm["brier"],
                    "log_loss": tm["log_loss"],
                }
            )
        print(f"  TEST PR-AUC={metrics['pr_auc']:.4f} ROC-AUC={metrics['roc_auc']:.4f}", flush=True)
        del model, p_te
        gc.collect()

    if {r["family"] for r in test_rows} != set(FAMILIES):
        reason = "Not all families completed the frozen test evaluation."
        dump_json(
            AUDIT_DIR / "stage4b_modeling_run.json",
            {
                "experiment_id": EXPERIMENT_ID,
                "status": "BLOCKED",
                "reason": reason,
                "issues": issues,
                "execution_timestamp": utc_now(),
                **hashes,
                "selection": selection,
            },
        )
        write_report(
            {
                **hashes,
                "status": "BLOCKED",
                "status_reason": reason,
                "validation_aggregates": aggregates,
                "selection": selection,
                "test_rows": test_rows,
                "temporal_rows": temporal_rows,
                "test_suite_summary": "Not run; test evaluation incomplete.",
            }
        )
        print("BLOCKED: incomplete test families", issues, file=sys.stderr)
        return 2

    pd.DataFrame(val_rows)[["family", "seed", "roc_auc", "pr_auc", "brier", "log_loss"]].to_csv(
        TABLE_DIR / "stage4b_validation_per_seed.csv", index=False
    )
    pd.DataFrame(aggregates).to_csv(TABLE_DIR / "stage4b_validation_aggregate.csv", index=False)
    pd.DataFrame(test_rows).drop(columns=["bootstrap", "config"], errors="ignore").to_csv(
        TABLE_DIR / "stage4b_test_performance.csv", index=False
    )
    pd.DataFrame(temporal_rows).to_csv(TABLE_DIR / "stage4b_test_temporal.csv", index=False)
    dump_json(METRICS_DIR / "stage4b_validation_metrics.json", {"per_seed": val_rows, "aggregate": aggregates})
    dump_json(METRICS_DIR / "stage4b_test_metrics.json", test_rows)
    dump_json(METRICS_DIR / "stage4b_temporal_metrics.json", temporal_rows)

    plot_roc(val_series_seed42, "Validation ROC (seed 42; not used as the sole selection statistic)", FIG_DIR / "figure1_validation_roc")
    plot_pr(val_series_seed42, "Validation precision-recall (seed 42)", FIG_DIR / "figure2_validation_pr")
    plot_roc(test_series, "Test ROC (frozen models; one evaluation)", FIG_DIR / "figure3_test_roc")
    plot_pr(test_series, "Test precision-recall (frozen models; one evaluation)", FIG_DIR / "figure4_test_pr")
    plot_temporal(temporal_rows, FIG_DIR / "figure5_test_by_year")

    print("Running pytest", flush=True)
    pytest_code, pytest_text = run_pytest()
    test_summary = pytest_text if pytest_text else f"pytest exit {pytest_code}"
    status = "PASS" if pytest_code == 0 and not issues else "BLOCKED"
    status_reason = (
        "All four families completed validation (5 seeds) and one frozen test evaluation; integrity tests passed."
        if status == "PASS"
        else f"Blocked after modeling. pytest_exit={pytest_code}. issues={issues}"
    )

    run_record = {
        "experiment_id": EXPERIMENT_ID,
        "dataset_hash": dataset_hash,
        "split_manifest_hash": hashes["split_manifest_hash"],
        "feature_policy_hash": hashes["feature_policy_hash"],
        "preprocessing_policy_hash": hashes["preprocessing_policy_hash"],
        "selection_path": str(SELECTION_PATH.relative_to(ROOT)),
        "model_configuration": hashes["configs"],
        "random_seeds": SEEDS,
        "final_seed": FINAL_SEED,
        "software_library_versions": versions,
        "execution_timestamp": utc_now(),
        "git_commit": hashes["git_commit"],
        "xgboost_frozen_n_estimators": xgb_n,
        "bootstrap": {
            "n_bootstrap": N_BOOT,
            "seed": BOOT_SEED,
            "confidence_level": 0.95,
            "method": "percentile_bootstrap_rows_with_replacement",
        },
        "status": status,
        "status_reason": status_reason,
        "issues": issues,
        "pytest_exit_code": pytest_code,
        "pytest_summary": test_summary[-4000:],
    }
    dump_json(AUDIT_DIR / "stage4b_modeling_run.json", run_record)
    write_report(
        {
            "status": status,
            "status_reason": status_reason,
            "dataset_hash": dataset_hash,
            "split_manifest_hash": hashes["split_manifest_hash"],
            "preprocessing_policy_hash": hashes["preprocessing_policy_hash"],
            "git_commit": hashes["git_commit"],
            "library_versions": versions,
            "n_train": n_train,
            "n_val": n_val,
            "n_test": n_test,
            "n_features_out": n_features,
            "configs": hashes["configs"],
            "validation_rows": val_rows,
            "validation_aggregates": aggregates,
            "selection": selection,
            "test_rows": test_rows,
            "temporal_rows": temporal_rows,
            "test_suite_summary": test_summary,
            "issues": issues,
        }
    )
    print(json.dumps({"status": status, "selected": selection["selected_family"], "issues": issues}, indent=2), flush=True)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
