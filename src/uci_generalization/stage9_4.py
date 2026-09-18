"""Stage 9.4 UCI independent generalization helpers. No LendingClub training."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from calibration.isotonic import IsotonicCalibrator
from calibration.metrics import calibration_metrics
from calibration.platt import PlattCalibrator
from data.audit_datasets import EXPECTED_UCI_ZIP_FILENAME, RAW_DIR, load_uci_dataframe, sha256_file
from data.create_splits import membership_hash, policy_uci_model_columns
from preprocessing.uci_preprocessor import UCI_ID, UCI_PREDICTORS, UCI_TARGET, ebm_frame

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT_ID = "stage9_4_uci_generalization_v1"
AMENDMENT_ID = "AMENDMENT-STAGE9-4-AUTHORIZATION"
AMENDMENT_PATH = ROOT / "docs" / "amendments" / "AMENDMENT-STAGE9-4-AUTHORIZATION.md"
ASSIGN_PATH = ROOT / "results" / "tables" / "uci_split_assignments.csv"
SUMMARY_PATH = ROOT / "results" / "metrics" / "uci_split_summary.json"
MANIFEST_PATH = ROOT / "audit" / "uci_split_manifest.json"
POLICY_PATH = ROOT / "docs" / "uci_feature_policy.csv"
LC_STAGE5_TEST = ROOT / "results" / "calibration" / "metrics" / "stage5_test_metrics.json"
RECORDED_UCI_SHA256 = "56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602"
SEEDS = [42, 123, 2024, 3407, 9999]
FINAL_SEED = 42
FAMILIES = ["logistic_regression", "explainable_boosting_machine", "xgboost"]
SIMPLICITY = ["logistic_regression", "explainable_boosting_machine", "xgboost"]
PR_AUC_TIE = 0.005
BRIER_TIE = 0.001
CALIB_SIMPLICITY = ["raw", "platt", "isotonic"]
N_BOOT = 1000
BOOT_SEED = 42

L1_METADATA_ONLY = (
    "UCI Default of Credit Card Clients lacks contract-type, counterparty, and Islamic-finance fields "
    "required for applicant-level Shariah determination. Stage 9.4 L1 is dataset-metadata only; "
    "no L2 fusion and no per-row Shariah rulings were performed."
)

PROTECTED_LC_PATHS = [
    ROOT / "results" / "decision" / "frozen_policy.json",
    ROOT / "results" / "decision" / "v2" / "frozen_policy.json",
    ROOT / "results" / "decision" / "v2" / "tables" / "table3_test_decision_outcomes.csv",
    ROOT / "results" / "calibration" / "test" / "ebm_seed42_calibrated.csv",
    ROOT / "results" / "calibration" / "metrics" / "stage5_test_metrics.json",
    ROOT / "results" / "metrics" / "stage4b_test_metrics.json",
    ROOT / "experiments" / "stage5_calibration" / "selected_calibration.json",
    ROOT / "docs" / "STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md",
    ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md",
    ROOT / "docs" / "STAGE_9_1_ABLATION_REPORT.md",
    ROOT / "docs" / "STAGE_9_2_COST_SENSITIVITY_REPORT.md",
    ROOT / "docs" / "STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md",
    ROOT / "audit" / "stage9_0_experimental_freeze.json",
    ROOT / "audit" / "stage9_1_ablation_run.json",
    ROOT / "audit" / "stage9_2_cost_sensitivity_run.json",
    ROOT / "audit" / "stage9_3_governance_sensitivity_run.json",
    ROOT / "configs" / "stage8_decision_policy.yaml",
]

FORBIDDEN_SELF_EDIT = [
    ROOT / "docs" / "STAGE_9_EXPERIMENTAL_PROTOCOL.md",
    ROOT / "RESEARCH_CONSTITUTION.md",
    ROOT / "docs" / "amendments" / "AMENDMENT-STAGE9-4-AUTHORIZATION.md",
    ROOT / "docs" / "amendments" / "AMENDMENT-SHARIAH-001.md",
    ROOT / "docs" / "deviations" / "DEVIATION-001-stage9-authorization-gap.md",
]


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require_amendment_approved() -> dict[str, str]:
    text = AMENDMENT_PATH.read_text(encoding="utf-8")
    status_match = re.search(r"^\*\*STATUS:\s*(.+?)\*\*\s*$", text, flags=re.MULTILINE)
    table_status = re.search(r"\|\s*\*\*Status\*\*\s*\|\s*`?([^|`]+)`?\s*\|", text)
    status = (status_match.group(1).strip() if status_match else "")
    if status != "APPROVED":
        table = table_status.group(1).strip() if table_status else ""
        raise RuntimeError(
            f"AMENDMENT-STAGE9-4-AUTHORIZATION is not APPROVED (STATUS={status!r}, table={table!r}). STOP."
        )
    date_match = re.search(r"\|\s*\*\*Approval date\*\*\s*\|\s*([^|]+)\|", text)
    return {
        "status": status,
        "approval_date": date_match.group(1).strip() if date_match else "",
        "path": str(AMENDMENT_PATH),
    }


def verify_frozen_uci_split() -> dict[str, Any]:
    if not ASSIGN_PATH.exists() or not MANIFEST_PATH.exists() or not SUMMARY_PATH.exists():
        raise RuntimeError("HARD STOP: frozen UCI split artifacts are missing. Do not recreate a new split.")
    assign = pd.read_csv(ASSIGN_PATH)
    summary = read_json(SUMMARY_PATH)
    manifest = read_json(MANIFEST_PATH)
    zip_path = RAW_DIR / EXPECTED_UCI_ZIP_FILENAME
    if not zip_path.exists():
        raise RuntimeError("HARD STOP: UCI raw zip is missing.")
    zip_hash = sha256_file(zip_path)
    if zip_hash != RECORDED_UCI_SHA256 or zip_hash != manifest["dataset_hash"]:
        raise RuntimeError(
            f"HARD STOP: UCI raw hash mismatch. observed={zip_hash} recorded={RECORDED_UCI_SHA256}."
        )
    policy_rows = pd.read_csv(POLICY_PATH).to_dict(orient="records")
    retained = policy_uci_model_columns(policy_rows)
    if retained != UCI_PREDICTORS:
        raise RuntimeError("HARD STOP: UCI predictor list does not match the frozen feature policy.")
    hashes = {}
    counts = {}
    for split, key in (("train", "train_hash"), ("validation", "validation_hash"), ("test", "test_hash")):
        part = assign.loc[assign["split"] == split]
        observed = membership_hash(part[UCI_ID].tolist(), part[UCI_ID].tolist())
        recorded = manifest[key]
        if observed != recorded:
            raise RuntimeError(f"HARD STOP: UCI {split} membership hash mismatch.")
        hashes[split] = observed
        counts[split] = int(len(part))
    expected_counts = {
        "train": int(manifest["train_row_count"]),
        "validation": int(manifest["validation_row_count"]),
        "test": int(manifest["test_row_count"]),
    }
    if counts != expected_counts:
        raise RuntimeError(f"HARD STOP: UCI split counts {counts} != manifest {expected_counts}.")
    if bool(manifest.get("merged_with_lendingclub")) or bool(summary.get("merged_with_lendingclub")):
        raise RuntimeError("HARD STOP: UCI split is marked merged with LendingClub.")
    return {
        "zip_sha256": zip_hash,
        "assignment_sha256": sha256_file(ASSIGN_PATH),
        "manifest_sha256": sha256_file(MANIFEST_PATH),
        "split_hashes": hashes,
        "split_counts": counts,
        "summary_prevalence": {
            "train": float(summary["train_prevalence"]),
            "validation": float(summary["validation_prevalence"]),
            "test": float(summary["test_prevalence"]),
        },
        "target_column": manifest["target_column"],
        "time_index": manifest["time_index"],
        "merged_with_lendingclub": False,
        "recode_applied": bool(manifest.get("recode_applied")),
    }


def load_uci_with_splits() -> pd.DataFrame:
    verify = verify_frozen_uci_split()
    df, _meta = load_uci_dataframe(RAW_DIR / EXPECTED_UCI_ZIP_FILENAME)
    assign = pd.read_csv(ASSIGN_PATH)
    df[UCI_ID] = pd.to_numeric(df[UCI_ID], errors="coerce").astype("int64")
    assign[UCI_ID] = pd.to_numeric(assign[UCI_ID], errors="coerce").astype("int64")
    merged = df.merge(assign, on=UCI_ID, how="inner")
    if len(merged) != len(df) or len(merged) != len(assign):
        raise RuntimeError("HARD STOP: UCI assignments do not match raw rows 1:1.")
    merged[UCI_TARGET] = pd.to_numeric(merged[UCI_TARGET], errors="coerce").astype(int)
    if not merged[UCI_TARGET].isin([0, 1]).all():
        raise RuntimeError("HARD STOP: UCI target is not binary {0,1}.")
    prevalence = {}
    for split in ("train", "validation", "test"):
        part = merged.loc[merged["split"] == split, UCI_TARGET]
        prevalence[split] = {
            "n": int(len(part)),
            "n_positive": int((part == 1).sum()),
            "prevalence": float(part.mean()),
        }
    merged.attrs["split_prevalence"] = prevalence
    merged.attrs["split_verify"] = verify
    return merged


def snapshot_protected_hashes() -> dict[str, str]:
    out = {}
    for path in PROTECTED_LC_PATHS:
        if not path.exists():
            raise RuntimeError(f"Protected artifact missing: {path}")
        out[str(path)] = sha256_file(path)
    return out


def assert_protected_unchanged(before: dict[str, str]) -> dict[str, str]:
    after = snapshot_protected_hashes()
    changed = [p for p, digest in before.items() if after.get(p) != digest]
    if changed:
        raise RuntimeError(f"HARD STOP: protected LendingClub/Stage 7-9.3 artifacts changed: {changed}")
    return after


def select_family(aggregates: list[dict]) -> dict:
    best_pr = max(a["pr_auc_mean"] for a in aggregates)
    candidates = [a for a in aggregates if best_pr - a["pr_auc_mean"] <= PR_AUC_TIE]
    candidates.sort(key=lambda a: (a["brier_mean"], SIMPLICITY.index(a["family"])))
    chosen = candidates[0]["family"]
    chosen_row = next(a for a in aggregates if a["family"] == chosen)
    reason = (
        f"Primary criterion is mean UCI validation PR-AUC. Best PR-AUC is {best_pr:.6f}. "
        f"Candidates within {PR_AUC_TIE}: {[c['family'] for c in candidates]}. "
        f"Among those, lowest mean Brier then simplicity selected `{chosen}` "
        f"(PR-AUC={chosen_row['pr_auc_mean']:.6f}, Brier={chosen_row['brier_mean']:.6f})."
    )
    return {
        "selected_family": chosen,
        "reason": reason,
        "candidates": [c["family"] for c in candidates],
        "declared_before_test": True,
        "test_metrics_not_consulted": True,
        "primary_criterion": "mean validation PR-AUC across frozen UCI seeds",
        "pr_auc_tie": PR_AUC_TIE,
        "simplicity_order": SIMPLICITY,
    }


def select_calibrator(val_rows: list[dict]) -> dict:
    by = {r["method"]: r for r in val_rows}
    best = min(by[m]["brier"] for m in CALIB_SIMPLICITY)
    candidates = [m for m in CALIB_SIMPLICITY if by[m]["brier"] - best <= BRIER_TIE]
    chosen = sorted(candidates, key=CALIB_SIMPLICITY.index)[0]
    reason = (
        f"Primary criterion is UCI validation Brier. Best Brier={best:.6f}. "
        f"Methods within {BRIER_TIE} (practically indistinguishable): {candidates}. "
        f"Among those, simplicity order {CALIB_SIMPLICITY} selected `{chosen}` "
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
        "simplicity_order": CALIB_SIMPLICITY,
        "test_metrics_not_consulted": True,
    }


def fit_calibrators(p_val: np.ndarray, y_val: np.ndarray) -> dict[str, Any]:
    platt = PlattCalibrator().fit(p_val, y_val, split="validation")
    iso = IsotonicCalibrator().fit(p_val, y_val, split="validation")
    rows = []
    mapped = {
        "raw": p_val,
        "platt": platt.transform(p_val),
        "isotonic": iso.transform(p_val),
    }
    for method, p_hat in mapped.items():
        metrics = calibration_metrics(y_val, p_hat)
        rows.append({"method": method, "split": "validation", **metrics})
    return {
        "platt": platt,
        "isotonic": iso,
        "validation_rows": rows,
        "selection": select_calibrator(rows),
        "mapped": mapped,
    }


def cite_lendingclub_stage5_test() -> dict[str, Any]:
    rows = read_json(LC_STAGE5_TEST)
    platt = next(r for r in rows if r["method"] == "platt")
    return {
        "dataset": "LendingClub granting extract",
        "target": "Default (1 = Charged Off, 0 = Fully Paid)",
        "source": "results/calibration/metrics/stage5_test_metrics.json",
        "source_sha256": sha256_file(LC_STAGE5_TEST),
        "split": "LC TEST",
        "n": int(platt["n"]),
        "method": "platt",
        "family": "explainable_boosting_machine",
        "roc_auc": float(platt["roc_auc"]),
        "pr_auc": float(platt["pr_auc"]),
        "brier": float(platt["brier"]),
        "log_loss": float(platt["log_loss"]),
        "ece": float(platt["ece"]),
        "note": "Cited from frozen Stage 5 artifacts. Not recomputed. Not merged with UCI rows.",
    }


def split_xy(table: pd.DataFrame, split: str) -> tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    part = table.loc[table["split"] == split].reset_index(drop=True)
    y = part[UCI_TARGET].to_numpy(dtype=int)
    ids = part[UCI_ID].to_numpy()
    return part, y, ids


def aggregate_seed_metrics(val_rows: list[dict], family: str) -> dict[str, float | str]:
    subset = [r for r in val_rows if r["family"] == family]
    roc = np.array([r["roc_auc"] for r in subset], dtype=float)
    pr = np.array([r["pr_auc"] for r in subset], dtype=float)
    brier = np.array([r["brier"] for r in subset], dtype=float)
    logloss = np.array([r["log_loss"] for r in subset], dtype=float)
    return {
        "family": family,
        "n_seeds": int(len(subset)),
        "roc_auc_mean": float(roc.mean()),
        "roc_auc_sd": float(roc.std(ddof=1) if len(roc) > 1 else 0.0),
        "pr_auc_mean": float(pr.mean()),
        "pr_auc_sd": float(pr.std(ddof=1) if len(pr) > 1 else 0.0),
        "brier_mean": float(brier.mean()),
        "brier_sd": float(brier.std(ddof=1) if len(brier) > 1 else 0.0),
        "log_loss_mean": float(logloss.mean()),
        "log_loss_sd": float(logloss.std(ddof=1) if len(logloss) > 1 else 0.0),
    }


def row_ref(uci_id: Any) -> str:
    return hashlib.sha256(f"uci-row|{uci_id}".encode("utf-8")).hexdigest()[:16]


def ebm_global_stats(model, frame: pd.DataFrame) -> pd.DataFrame:
    x = ebm_frame(frame)
    terms = np.asarray(model.eval_terms(x), dtype=float)
    if terms.shape[1] != len(UCI_PREDICTORS):
        raise RuntimeError("UCI EBM term count does not match the frozen predictor set.")
    abs_c = np.abs(terms)
    rows = []
    for i, name in enumerate(UCI_PREDICTORS):
        col = abs_c[:, i]
        rows.append(
            {
                "feature": name,
                "mean_abs": float(col.mean()),
                "median_abs": float(np.median(col)),
                "std_abs": float(col.std(ddof=1)),
                "mean_signed": float(terms[:, i].mean()),
            }
        )
    out = pd.DataFrame(rows)
    out["rank"] = out["mean_abs"].rank(ascending=False, method="first").astype(int)
    intercept = float(np.asarray(model.intercept_, dtype=float).reshape(-1)[0])
    out.attrs["intercept"] = intercept
    return out.sort_values("rank").reset_index(drop=True)


def ebm_shape(model, feature: str) -> dict[str, Any]:
    names = list(model.explain_global().data()["names"])
    idx = names.index(feature)
    payload = model.explain_global().data(idx)
    return {
        "feature": feature,
        "scores": [float(s) for s in np.asarray(payload["scores"], dtype=float)],
        "names": [str(n) for n in payload["names"]],
        "scale": "EBM additive term on logit/link scale",
        "causal": False,
    }
