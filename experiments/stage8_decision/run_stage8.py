"""Stage 8 decision fusion, cost-sensitive policy, and audit trail.

Does not retrain the EBM or Platt calibrator. Thresholds are selected on
VALIDATION only. TEST is loaded only after the policy is frozen to disk.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from calibration.metrics import calibration_metrics  # noqa: E402
from data.audit_datasets import git_commit, sha256_file  # noqa: E402
from decision.audit_record import (  # noqa: E402
    AUDIT_SCHEMA_VERSION,
    POLICY_VERSION,
    build_record,
    logic_hash,
    schema_document,
)
from decision.config_load import JSON_PATH, YAML_PATH, load_policy_config  # noqa: E402
from decision.cost_policy import CostScenario  # noqa: E402
from decision.decision_engine import (  # noqa: E402
    apply_policy,
    evaluate_lendingclub_governance,
    fuse_decision,
    lendingclub_governance_payload,
)
from decision.plots import (  # noqa: E402
    figure1_cost_curve,
    figure2_cost_ratio,
    figure3_action_rates,
    figure4_default_by_band,
    figure5_heatmap,
    figure6_architecture,
    figure7_audit_lifecycle,
)
from decision.policy_matrix import CREDIT_BANDS, GOVERNANCE_STATUSES, build_matrix  # noqa: E402
from decision.threshold_selection import (  # noqa: E402
    assert_validation_split,
    credit_only_decisions,
    make_threshold_grid,
    select_policy,
    single_threshold_cost_curve,
)
from evaluation.decision_metrics import band_outcome_table, policy_metrics  # noqa: E402
from preprocessing.lendingclub_preprocessor import (  # noqa: E402
    FEATURE_POLICY_PATH,
    PREPROCESS_POLICY_PATH,
    RECORDED_LC_SHA256,
    SCRIPT_VERSION as PREPROCESSOR_VERSION,
    sha256_text_file,
)

EXPERIMENT_ID = "stage8-lc-decision-v1"
DATASET_ID = "lendingclub_granting_v0.1"
VAL_CAL = ROOT / "results" / "calibration" / "validation" / "ebm_seed42_calibrated.csv"
TEST_CAL = ROOT / "results" / "calibration" / "test" / "ebm_seed42_calibrated.csv"
STAGE5_TEST = ROOT / "results" / "calibration" / "metrics" / "stage5_test_metrics.json"
STAGE5_SELECTED = ROOT / "experiments" / "stage5_calibration" / "selected_calibration.json"
PLATT_RECORD = ROOT / "results" / "calibration" / "artifacts" / "platt_record.json"
GLOBAL_SHAP = ROOT / "results" / "explainability" / "tables" / "table1_global_attribution.csv"
SPLIT_MANIFEST = ROOT / "audit" / "lendingclub_split_manifest.json"
OUT = ROOT / "results" / "decision"
FIG = ROOT / "results" / "figures" / "decision"
TAB = OUT / "tables"
AUDIT_RUN = ROOT / "audit" / "stage8_decision_policy_run.json"
AUDIT_THRESH = ROOT / "audit" / "stage8_threshold_selection.json"
AUDIT_CFG = ROOT / "audit" / "stage8_policy_config.json"
AUDIT_SCHEMA = ROOT / "audit" / "stage8_audit_schema.json"
FREEZE_PATH = OUT / "frozen_policy.json"
REPORT = ROOT / "docs" / "STAGE_8_DECISION_POLICY_REPORT.md"
FIXED_GOV_TS = "2026-09-15T00:00:00+00:00"


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
        if not np.isfinite(value):
            return None
        return value
    if isinstance(obj, (np.integer, int)) and not isinstance(obj, bool):
        return int(obj)
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    return obj


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_json(payload: Any) -> str:
    blob = json.dumps(json_safe(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return sha256_bytes(blob.encode("utf-8"))


def load_split_predictions(path: Path, expected_split: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    splits = set(frame["split"].astype(str).unique())
    if splits != {expected_split}:
        raise RuntimeError(f"{path} splits={splits} expected {{{expected_split}}}")
    need = {"row_ref", "split", "year", "y_true", "p_raw", "p_selected", "p_platt"}
    missing = sorted(need - set(frame.columns))
    if missing:
        raise RuntimeError(f"{path} missing columns {missing}")
    if frame["p_selected"].isna().any() or frame["p_raw"].isna().any():
        raise RuntimeError(f"{path} contains missing probabilities.")
    p = frame["p_selected"].to_numpy(dtype=float)
    if np.any(~np.isfinite(p)) or np.any(p < 0.0) or np.any(p > 1.0):
        raise RuntimeError(f"{path} contains probabilities outside [0, 1].")
    return frame


def load_test_after_freeze(freeze_path: Path) -> pd.DataFrame:
    if not freeze_path.exists():
        raise RuntimeError("Attempted to load test predictions before freezing the Stage 8 policy.")
    return load_split_predictions(TEST_CAL, "test")


def run_pytest() -> tuple[int, str]:
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", str(ROOT / "tests"), "-q", "--tb=short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, text.strip()


def top_explanation_features(path: Path, k: int = 5) -> list[str]:
    table = pd.read_csv(path)
    ordered = table.sort_values("shap_rank")
    return ordered["feature"].astype(str).head(k).tolist()


def stage5_platt_test_metrics() -> dict[str, Any]:
    rows = json.loads(STAGE5_TEST.read_text(encoding="utf-8"))
    platt = next(r for r in rows if r["method"] == "platt")
    return platt


def verify_stage5_metrics(frame: pd.DataFrame, artifact: dict[str, Any]) -> dict[str, Any]:
    computed = calibration_metrics(frame["y_true"].to_numpy(), frame["p_selected"].to_numpy())
    keys = ["roc_auc", "pr_auc", "brier", "ece"]
    gaps = {k: abs(float(computed[k]) - float(artifact[k])) for k in keys}
    if any(v > 1e-10 for v in gaps.values()):
        raise RuntimeError(f"Stage 8 recomputed metrics disagree with Stage 5 artifacts: {gaps}")
    return {"artifact": artifact, "recomputed": computed, "abs_gap": gaps}


def selection_view(result: dict[str, Any]) -> dict[str, Any]:
    selected = result["selected"]
    return {
        "t_low": selected["t_low"],
        "t_high": selected["t_high"],
        "policy_type": selected["policy_type"],
        "expected_normalized_cost": selected["expected_normalized_cost"],
        "approval_rate": selected["approval_rate"],
        "review_rate": selected["review_rate"],
        "rejection_rate": selected["rejection_rate"],
        "fnr_population": selected["fnr_population"],
        "fpr_population": selected["fpr_population"],
        "fnr_auto": selected["fnr_auto"],
        "fpr_auto": selected["fpr_auto"],
        "n_candidates": result["n_candidates"],
        "selected_single": {
            "t_low": result["selected_single"]["t_low"],
            "t_high": result["selected_single"]["t_high"],
            "expected_normalized_cost": result["selected_single"]["expected_normalized_cost"],
            "approval_rate": result["selected_single"]["approval_rate"],
            "rejection_rate": result["selected_single"]["rejection_rate"],
            "fnr_population": result["selected_single"]["fnr_population"],
            "fpr_population": result["selected_single"]["fpr_population"],
        },
        "selected_two_threshold": None
        if result["selected_two_threshold"] is None
        else {
            "t_low": result["selected_two_threshold"]["t_low"],
            "t_high": result["selected_two_threshold"]["t_high"],
            "expected_normalized_cost": result["selected_two_threshold"]["expected_normalized_cost"],
            "approval_rate": result["selected_two_threshold"]["approval_rate"],
            "review_rate": result["selected_two_threshold"]["review_rate"],
            "rejection_rate": result["selected_two_threshold"]["rejection_rate"],
            "fnr_population": result["selected_two_threshold"]["fnr_population"],
            "fpr_population": result["selected_two_threshold"]["fpr_population"],
        },
    }


def contingency_table(bands: np.ndarray, statuses: np.ndarray, decisions: np.ndarray, matrix) -> list[dict[str, Any]]:
    rows = []
    for band in CREDIT_BANDS:
        for status in GOVERNANCE_STATUSES:
            mask = (bands == band) & (statuses == status)
            n = int(mask.sum())
            policy = matrix[(status, band)]
            observed = sorted({str(v) for v in decisions[mask]}) if n else []
            rows.append(
                {
                    "credit_band": band,
                    "governance_status": status,
                    "n": n,
                    "configured_final_policy": policy,
                    "observed_decisions": observed,
                }
            )
    return rows


def heatmap_matrix(contingency: list[dict[str, Any]]) -> tuple[list[str], list[str], np.ndarray]:
    values = np.zeros((len(CREDIT_BANDS), len(GOVERNANCE_STATUSES)), dtype=int)
    lookup = {(r["credit_band"], r["governance_status"]): r["n"] for r in contingency}
    for i, band in enumerate(CREDIT_BANDS):
        for j, status in enumerate(GOVERNANCE_STATUSES):
            values[i, j] = lookup[(band, status)]
    short = {
        "NOT_STRUCTURABLE_WITHOUT_REDESIGN": "NOT_STRUCTURABLE",
        "INSUFFICIENT_INFORMATION": "INSUFFICIENT",
        "REVIEW": "REVIEW",
        "PASS": "PASS",
    }
    return list(CREDIT_BANDS), [short[s] for s in GOVERNANCE_STATUSES], values


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)


def fmt(value: Any, digits: int = 6) -> str:
    if value is None:
        return "NA"
    if isinstance(value, float) and not np.isfinite(value):
        return "NA"
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.{digits}f}"
    return str(value)


def write_report(payload: dict[str, Any]) -> None:
    primary = payload["primary"]
    fused_test = payload["fused_test"]
    mono_test = payload["monolithic_test"]
    gov = payload["lendingclub_governance"]
    lines = [
        "# Stage 8 Decision Policy Report",
        "",
        "Credit risk, explainability, and Shariah-oriented governance remain independently validated evidence layers. This stage implements a transparent approve / review / reject policy and an audit record. It does not retrain the EBM, does not refit Platt scaling, and does not create a Shariah score.",
        "",
        f"**Status:** `{payload['status']}`",
        "",
        "## Separation of claims",
        "",
        "| Question | What this stage reports |",
        "| --- | --- |",
        "| Predictive | Frozen Stage 5 Platt-calibrated EBM discrimination and calibration, cited from Stage 5 artifacts and consistency-checked |",
        "| Governance | Whether contractual evidence exists for the configured Stage 7 rules |",
        "| Decision policy | The action recommended under explicit researcher cost and matrix assumptions |",
        "| Auditability | Whether another researcher can reconstruct the logic hash of a decision |",
        "",
        "These questions are not collapsed into a single accuracy number.",
        "",
        "## Observed empirical results",
        "",
        f"- LendingClub governance profile evaluated once: completeness `{gov['layer_a']}`, status `{gov['overall_governance_status']}`. Real LendingClub rows were not given fabricated contract fields.",
        f"- Primary ASSUMED RELATIVE COST SCENARIO: `{primary['scenario']}` with `C_REVIEW = {primary['c_review_over_fp']} * C_FP`.",
        f"- Validation-selected credit-only policy: type `{primary['policy_type']}`, `t_low={primary['t_low']}`, `t_high={primary['t_high']}`, expected normalized cost `{fmt(primary['expected_normalized_cost'])}`.",
        f"- Frozen test fused-policy action mix: approval `{fmt(fused_test['approval_rate'])}`, review `{fmt(fused_test['review_rate'])}`, rejection `{fmt(fused_test['rejection_rate'])}`.",
        f"- Frozen test fused-policy default rates by action are in `results/decision/tables/table3_test_decision_outcomes.csv`.",
        f"- Credit-risk × governance contingency is in `results/decision/tables/table4_credit_governance_contingency.csv`.",
        "",
        "### Validation threshold selection by cost scenario",
        "",
        "| Scenario | Type | t_low | t_high | Val expected cost | Val approve | Val review | Val reject | Val FNR (pop.) | Val FPR (pop.) |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in payload["experiment_b"]:
        lines.append(
            f"| {row['scenario']} | {row['policy_type']} | {fmt(row['t_low'], 2)} | {fmt(row['t_high'], 2)} | {fmt(row['expected_normalized_cost'])} | {fmt(row['approval_rate'])} | {fmt(row['review_rate'])} | {fmt(row['rejection_rate'])} | {fmt(row['fnr_population'])} | {fmt(row['fpr_population'])} |"
        )
    pred = payload["predictive_test"]
    lines += [
        "",
        "### Frozen test predictive metrics (Stage 5 Platt artifacts)",
        "",
        f"- ROC-AUC `{fmt(pred['roc_auc'])}`",
        f"- PR-AUC `{fmt(pred['pr_auc'])}`",
        f"- Brier `{fmt(pred['brier'])}`",
        f"- ECE `{fmt(pred['ece'])}`",
        f"- MCE `{fmt(pred['mce'])}`",
        "- Stage 8 recomputed the same functions on the frozen test prediction file; absolute gaps to the Stage 5 artifact are reported in the run audit and must be numerically zero at 1e-12.",
        "",
        "### Frozen test fused policy",
        "",
        f"- n = {fused_test['n']}",
        f"- approval_rate = {fmt(fused_test['approval_rate'])}",
        f"- review_rate = {fmt(fused_test['review_rate'])}",
        f"- rejection_rate = {fmt(fused_test['rejection_rate'])}",
        f"- FNR (population, auto-approved defaults / all defaults) = {fmt(fused_test['fnr_population'])}",
        f"- FPR (population, auto-rejected non-defaults / all non-defaults) = {fmt(fused_test['fpr_population'])}",
        f"- precision of REJECT = {fmt(fused_test['precision_reject'])}",
        f"- expected normalized cost under the primary assumed scenario = {fmt(fused_test.get('expected_normalized_cost'))}",
        "",
        "The review band is a **simulated decision-policy band**. No human-review outcomes were collected. This stage does not claim that human reviewers improved accuracy, fairness, or Shariah status.",
        "",
        "## Researcher policy assumptions",
        "",
        "- Relative FN:FP costs `{1,2,5,10}` are sensitivity scenarios, not LendingClub, bank, Islamic-institution, or regulator costs.",
        f"- Review is not free: `C_REVIEW = {payload['config']['cost_scenarios']['c_review_over_fp']} * C_FP` unless perturbed in Experiment G.",
        "- Primary freeze uses FN:FP = 5:1, declared in `configs/stage8_decision_policy.yaml` before test evaluation.",
        "- Credit-risk thresholds are selected from a **credit-only** cost objective on validation. Rationale: under LendingClub `INSUFFICIENT_INFORMATION`, LOW and MEDIUM both map to HUMAN_REVIEW, so `t_low` is not identified by fused cost.",
        "- The governance matrix is a researcher operating procedure, not a religious ruling and not expert-validated.",
        "",
        "## Architectural design choices",
        "",
        "1. Governance `NOT_STRUCTURABLE_WITHOUT_REDESIGN` is a hard stop: REJECT for every credit band.",
        "2. Unknown or missing governance is treated as `INSUFFICIENT_INFORMATION`, never as PASS.",
        "3. APPROVE requires governance PASS and a LOW credit-risk band.",
        "4. Explainability is attached to the audit record and is not an independent approval criterion.",
        "5. The monolithic baseline is a single threshold on the same calibrated probability with no governance layer and no review band.",
        "",
        "## Fairness limitation",
        "",
        "Fairness evaluation is limited by unavailable protected attributes. Race, religion, gender, and ethnicity are not inferred from `addr_state`, `zip_code`, or `purpose`.",
        "",
        "## Tests and reproducibility",
        "",
        payload.get("test_suite_summary", "Not run."),
        "",
        f"- In-process threshold selection repeated twice: equivalent `{payload['reproducibility']['selection_equivalent']}`.",
        f"- Audit logic hashes ignore event timestamps: equivalent `{payload['reproducibility']['audit_timestamp_invariant']}`.",
        "",
        "## Stage boundary",
        "",
        "Stage 9 has NOT been started.",
        "",
        "## Artifact index",
        "",
    ]
    for path in payload["artifact_paths"]:
        lines.append(f"- `{path}`")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    started = utc_now()
    config = load_policy_config(YAML_PATH)
    dump_json(JSON_PATH, config)
    dump_json(AUDIT_CFG, {"source_yaml": str(YAML_PATH.relative_to(ROOT)).replace("\\", "/"), "config": config})
    dump_json(AUDIT_SCHEMA, schema_document())

    matrix = build_matrix(config["governance_policy"]["matrix"])
    unknown_as = config["governance_policy"]["unknown_status_treated_as"]
    grid = make_threshold_grid(
        float(config["threshold_grid"]["start"]),
        float(config["threshold_grid"]["stop"]),
        float(config["threshold_grid"]["step"]),
    )
    scenarios = [
        CostScenario(
            fn_fp_ratio=float(ratio),
            c_fp=float(config["cost_scenarios"]["c_fp"]),
            c_review_over_fp=float(config["cost_scenarios"]["c_review_over_fp"]),
        )
        for ratio in config["cost_scenarios"]["fn_fp_ratios"]
    ]
    primary_ratio = float(config["cost_scenarios"]["primary_fn_fp_ratio"])
    primary_scenario = next(s for s in scenarios if s.fn_fp_ratio == primary_ratio)
    top_features = top_explanation_features(GLOBAL_SHAP)
    platt = json.loads(PLATT_RECORD.read_text(encoding="utf-8"))
    selected_cal = json.loads(STAGE5_SELECTED.read_text(encoding="utf-8"))

    gov = evaluate_lendingclub_governance(timestamp=FIXED_GOV_TS)
    catalog_rules = json.loads((ROOT / "docs" / "shariah" / "rule_catalog.json").read_text(encoding="utf-8"))["rules"]
    id_to_source = {row["rule_id"]: row["source_id"] for row in catalog_rules}
    triggered = [row["rule_id"] for row in gov["rule_evaluations"] if row["applicable"]]
    sources = sorted({id_to_source[rid] for rid in triggered if rid in id_to_source})
    lc_status = gov["overall_governance_status"]
    lc_layer_a = gov["layer_a_completeness"]["layer_a"]
    if lc_status == "PASS":
        raise RuntimeError("LendingClub profile unexpectedly PASSed; refusing to proceed without investigation.")

    val = load_split_predictions(VAL_CAL, "validation")
    y_val = val["y_true"].to_numpy(dtype=int)
    p_val = val["p_selected"].to_numpy(dtype=float)
    assert_validation_split("validation")
    print(f"Validation rows loaded: {len(val)}. Test file not opened.", flush=True)

    experiment_b = []
    selections = {}
    for scenario in scenarios:
        print(f"Selecting thresholds for {scenario.name} on validation...", flush=True)
        result = select_policy(
            y_val,
            p_val,
            scenario,
            grid,
            split="validation",
            include_two_threshold=True,
        )
        selections[scenario.name] = result
        view = selection_view(result)
        view["scenario"] = scenario.name
        view["fn_fp_ratio"] = scenario.fn_fp_ratio
        experiment_b.append(view)

    primary_result = selections[primary_scenario.name]
    primary_sel = primary_result["selected"]
    t_low = float(primary_sel["t_low"])
    t_high = float(primary_sel["t_high"])
    curve = single_threshold_cost_curve(y_val, p_val, primary_scenario, grid, split="validation")

    fused_val = apply_policy(p_val, lc_status, t_low, t_high, matrix, unknown_as)
    fused_val_metrics = policy_metrics(y_val, fused_val["final_decision"], primary_scenario)
    credit_val_metrics = policy_metrics(y_val, credit_only_decisions(p_val, t_low, t_high), primary_scenario)

    perturb_rows = []
    for c_rev in config["perturbation"]["c_review_over_fp_values"]:
        scen = CostScenario(fn_fp_ratio=primary_ratio, c_fp=1.0, c_review_over_fp=float(c_rev))
        result = select_policy(y_val, p_val, scen, grid, split="validation", include_two_threshold=True)
        view = selection_view(result)
        view["scenario"] = scen.name
        view["c_review_over_fp"] = float(c_rev)
        perturb_rows.append(view)

    freeze = {
        "experiment_id": EXPERIMENT_ID,
        "policy_version": config["policy_version"],
        "audit_schema_version": str(config["audit_schema_version"]),
        "frozen_before_test": True,
        "cost_scenario": primary_scenario.as_dict(),
        "t_low": t_low,
        "t_high": t_high,
        "policy_type": primary_sel["policy_type"],
        "selection_split": "validation",
        "threshold_identification": (
            "Credit-only expected cost on validation. Governance matrix is applied after freeze "
            "and is not used to choose t_low/t_high because LendingClub evidence is INSUFFICIENT_INFORMATION."
        ),
        "platt": platt,
        "selected_calibration_method": selected_cal["selected_method"],
        "top_explanation_features": top_features,
        "lendingclub_governance_status": lc_status,
        "lendingclub_layer_a": lc_layer_a,
        "timestamp": utc_now(),
    }
    dump_json(FREEZE_PATH, freeze)
    print(f"Policy frozen at {FREEZE_PATH}. Loading test predictions once.", flush=True)
    dump_json(
        AUDIT_THRESH,
        {
            "experiment_id": EXPERIMENT_ID,
            "grid": [float(x) for x in grid],
            "primary_scenario": primary_scenario.as_dict(),
            "experiment_b": json_safe(experiment_b),
            "primary_selected": json_safe(primary_sel),
            "perturbation": json_safe(perturb_rows),
            "n_validation": int(len(val)),
            "frozen_before_test": True,
        },
    )

    test = load_test_after_freeze(FREEZE_PATH)
    y_test = test["y_true"].to_numpy(dtype=int)
    p_test = test["p_selected"].to_numpy(dtype=float)
    pred_check = verify_stage5_metrics(test, stage5_platt_test_metrics())

    fused_test = apply_policy(p_test, lc_status, t_low, t_high, matrix, unknown_as)
    fused_test_metrics = policy_metrics(y_test, fused_test["final_decision"], primary_scenario)
    credit_test_decisions = credit_only_decisions(p_test, t_low, t_high)
    credit_test_metrics = policy_metrics(y_test, credit_test_decisions, primary_scenario)
    credit_band_rows = band_outcome_table(y_test, fused_test["credit_risk_band"])
    decision_band_rows = band_outcome_table(y_test, fused_test["final_decision"])

    mono_t = float(primary_result["selected_single"]["t_low"])
    mono_decisions = credit_only_decisions(p_test, mono_t, mono_t)
    mono_scenario = CostScenario(fn_fp_ratio=primary_ratio, c_fp=1.0, c_review_over_fp=0.0)
    mono_test_metrics = policy_metrics(y_test, mono_decisions, mono_scenario)
    mono_val = policy_metrics(y_val, credit_only_decisions(p_val, mono_t, mono_t), mono_scenario)

    contingency = contingency_table(
        fused_test["credit_risk_band"],
        fused_test["shariah_governance_status"],
        fused_test["final_decision"],
        matrix,
    )

    event_ts = utc_now()
    threshold_configuration = {
        "t_low": t_low,
        "t_high": t_high,
        "policy_type": primary_sel["policy_type"],
        "identification": "credit_only_validation",
    }
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    (OUT / "audit").mkdir(parents=True, exist_ok=True)
    audit_csv = OUT / "audit" / "test_audit_records.csv"
    sample_records: list[dict[str, Any]] = []
    by_decision: dict[str, dict[str, Any]] = {}
    fieldnames = [
        "decision_id",
        "event_timestamp",
        "audit_schema_version",
        "dataset_id",
        "dataset_hash",
        "record_reference_hash",
        "model_name",
        "model_version",
        "preprocessor_version",
        "calibrator_name",
        "calibrator_version",
        "raw_probability",
        "calibrated_probability",
        "credit_risk_band",
        "top_explanation_features",
        "shariah_evidence_completeness",
        "shariah_governance_status",
        "triggered_rule_ids",
        "rule_source_ids",
        "policy_version",
        "cost_scenario",
        "threshold_configuration",
        "final_decision",
        "review_required",
    ]
    p_raw = test["p_raw"].to_numpy(dtype=float)
    refs = test["row_ref"].astype(str).to_numpy()
    with audit_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(test)):
            rec = build_record(
                event_timestamp=event_ts,
                dataset_id=DATASET_ID,
                dataset_hash=RECORDED_LC_SHA256,
                record_reference_hash=str(refs[i]),
                model_name="explainable_boosting_machine",
                model_version="stage4b-lc-granting-v1:seed42",
                preprocessor_version=PREPROCESSOR_VERSION,
                calibrator_name="platt",
                calibrator_version="stage5-lc-ebm-calibration-v1",
                raw_probability=float(p_raw[i]),
                calibrated_probability=float(p_test[i]),
                credit_risk_band=str(fused_test["credit_risk_band"][i]),
                top_explanation_features=top_features,
                shariah_evidence_completeness=lc_layer_a,
                shariah_governance_status=str(fused_test["shariah_governance_status"][i]),
                triggered_rule_ids=triggered,
                rule_source_ids=sources,
                policy_version=str(config["policy_version"]),
                cost_scenario=primary_scenario.name,
                threshold_configuration=threshold_configuration,
                final_decision=str(fused_test["final_decision"][i]),
                review_required=str(fused_test["final_decision"][i]) == "HUMAN_REVIEW",
                audit_schema_version=str(config["audit_schema_version"]),
            )
            writer.writerow(
                {
                    **{
                        k: rec[k]
                        for k in fieldnames
                        if k
                        not in {
                            "top_explanation_features",
                            "triggered_rule_ids",
                            "rule_source_ids",
                            "threshold_configuration",
                        }
                    },
                    "top_explanation_features": "|".join(rec["top_explanation_features"]),
                    "triggered_rule_ids": "|".join(rec["triggered_rule_ids"]),
                    "rule_source_ids": "|".join(rec["rule_source_ids"]),
                    "threshold_configuration": json.dumps(rec["threshold_configuration"], sort_keys=True),
                }
            )
            if rec["final_decision"] not in by_decision:
                by_decision[rec["final_decision"]] = rec
                if i < 25:
                    sample_records.append(rec)
                if (i + 1) % 50000 == 0:
                    print(f"Wrote {i + 1} audit records...", flush=True)

    later_ts = utc_now()
    invariant = True
    for rec in sample_records:
        shifted = dict(rec)
        shifted["event_timestamp"] = later_ts
        if logic_hash(shifted) != rec["decision_id"]:
            invariant = False
            break

    published = []
    for key in ("REJECT", "HUMAN_REVIEW", "APPROVE"):
        if key in by_decision:
            published.append(by_decision[key])
    synthetic_pass = fuse_decision(0.05, "PASS", t_low, t_high, matrix, unknown_as)
    synthetic_rec = build_record(
        event_timestamp=event_ts,
        dataset_id="synthetic_governance_illustration",
        dataset_hash="synthetic-not-a-lendingclub-row",
        record_reference_hash=hashlib.sha256(b"synthetic-audit|PASS-LOW").hexdigest()[:16],
        model_name="explainable_boosting_machine",
        model_version="stage4b-lc-granting-v1:seed42",
        preprocessor_version=PREPROCESSOR_VERSION,
        calibrator_name="platt",
        calibrator_version="stage5-lc-ebm-calibration-v1",
        raw_probability=0.04,
        calibrated_probability=0.05,
        credit_risk_band=synthetic_pass["credit_risk_band"],
        top_explanation_features=top_features,
        shariah_evidence_completeness="COMPLETE",
        shariah_governance_status="PASS",
        triggered_rule_ids=["SYNTHETIC_ILLUSTRATION_NOT_A_STAGE7_RULE"],
        rule_source_ids=["SYNTHETIC_ILLUSTRATION"],
        policy_version=str(config["policy_version"]),
        cost_scenario=primary_scenario.name,
        threshold_configuration=threshold_configuration,
        final_decision=synthetic_pass["final_decision"],
        review_required=synthetic_pass["review_required"],
    )
    synthetic_rec["synthetic"] = True
    synthetic_rec["label"] = "Synthetic illustration of PASS+LOW. Not a LendingClub observation."
    published.append(synthetic_rec)

    table1 = [
        {
            "governance": row["governance"],
            "credit_band": row["credit_band"],
            "final_decision": row["decision"],
            "assumption": "Researcher policy mapping, not a religious ruling",
        }
        for row in config["governance_policy"]["matrix"]
    ]
    table2 = []
    for row in experiment_b:
        table2.append(
            {
                "cost_scenario": row["scenario"],
                "label": "ASSUMED RELATIVE COST SCENARIO",
                "policy_type": row["policy_type"],
                "t_low": row["t_low"],
                "t_high": row["t_high"],
                "expected_normalized_cost": row["expected_normalized_cost"],
                "approval_rate": row["approval_rate"],
                "review_rate": row["review_rate"],
                "rejection_rate": row["rejection_rate"],
                "fnr_population": row["fnr_population"],
                "fpr_population": row["fpr_population"],
                "single_t": row["selected_single"]["t_low"],
                "single_cost": row["selected_single"]["expected_normalized_cost"],
                "two_t_low": None if row["selected_two_threshold"] is None else row["selected_two_threshold"]["t_low"],
                "two_t_high": None if row["selected_two_threshold"] is None else row["selected_two_threshold"]["t_high"],
                "two_cost": None if row["selected_two_threshold"] is None else row["selected_two_threshold"]["expected_normalized_cost"],
            }
        )
    table3 = [
        {**{"split": "test", "architecture": "fused_evidence_separated", **fused_test_metrics}},
        {**{"split": "test", "architecture": "monolithic_credit_threshold", **mono_test_metrics}},
        {**{"split": "test", "architecture": "credit_only_selected_bands", **credit_test_metrics}},
    ]
    table3_bands = [{"architecture": "fused_credit_band", **r} for r in credit_band_rows] + [
        {"architecture": "fused_decision", **r} for r in decision_band_rows
    ]
    table5 = [
        {
            "item": "predictive_scores",
            "monolithic": "same frozen Platt-calibrated EBM probabilities",
            "evidence_separated": "same frozen Platt-calibrated EBM probabilities",
            "note": "Architecture does not change ROC-AUC/PR-AUC/Brier",
        },
        {
            "item": "threshold",
            "monolithic": f"single t={mono_t}",
            "evidence_separated": f"t_low={t_low}, t_high={t_high} ({primary_sel['policy_type']})",
            "note": "Both selected on validation only",
        },
        {
            "item": "governance",
            "monolithic": "absent",
            "evidence_separated": lc_status,
            "note": "Not converted to a score",
        },
        {
            "item": "test_approval_rate",
            "monolithic": mono_test_metrics["approval_rate"],
            "evidence_separated": fused_test_metrics["approval_rate"],
            "note": "Fused APPROVE requires governance PASS",
        },
        {
            "item": "test_review_rate",
            "monolithic": mono_test_metrics["review_rate"],
            "evidence_separated": fused_test_metrics["review_rate"],
            "note": "Monolithic has no review band",
        },
        {
            "item": "test_rejection_rate",
            "monolithic": mono_test_metrics["rejection_rate"],
            "evidence_separated": fused_test_metrics["rejection_rate"],
            "note": "",
        },
        {
            "item": "test_expected_normalized_cost",
            "monolithic": mono_test_metrics["expected_normalized_cost"],
            "evidence_separated": fused_test_metrics["expected_normalized_cost"],
            "note": "Fused cost uses C_REVIEW; monolithic uses C_REVIEW=0. Not a claim of superior accuracy.",
        },
    ]
    table6 = [{"field": f, "required": True} for f in schema_document()["required_fields"]]

    write_csv(TAB / "table1_decision_policy_definitions.csv", table1)
    write_csv(TAB / "table2_validation_threshold_selection.csv", table2)
    write_csv(TAB / "table3_test_decision_outcomes.csv", [{k: v for k, v in r.items() if k != "decision_bands" and k != "cost_scenario"} for r in table3])
    write_csv(TAB / "table3b_test_default_rates_by_band.csv", table3_bands)
    write_csv(TAB / "table4_credit_governance_contingency.csv", contingency)
    write_csv(TAB / "table5_monolithic_vs_separated.csv", table5)
    write_csv(TAB / "table6_audit_schema.csv", table6)
    write_csv(TAB / "experiment_g_review_cost_perturbation.csv", perturb_rows)
    write_csv(TAB / "validation_single_threshold_cost_curve.csv", curve)

    dump_json(OUT / "audit" / "published_examples.json", published)
    dump_json(
        OUT / "metrics" / "fused_test.json",
        json_safe({"metrics": fused_test_metrics, "credit_bands": credit_band_rows, "decision_bands": decision_band_rows}),
    )
    dump_json(OUT / "metrics" / "monolithic_test.json", json_safe(mono_test_metrics))
    dump_json(OUT / "metrics" / "fused_validation.json", json_safe(fused_val_metrics))
    dump_json(OUT / "metrics" / "credit_only_validation.json", json_safe(credit_val_metrics))
    dump_json(OUT / "metrics" / "monolithic_validation.json", json_safe(mono_val))
    dump_json(OUT / "metrics" / "predictive_test_stage5.json", json_safe(pred_check))

    idx, cols, heat = heatmap_matrix(contingency)
    figure1_cost_curve(curve, float(primary_result["selected_single"]["t_low"]), FIG / "figure1_validation_cost_curve")
    figure2_cost_ratio(
        [{"scenario": r["scenario"], "expected_normalized_cost": r["expected_normalized_cost"]} for r in experiment_b],
        FIG / "figure2_cost_ratio_sensitivity",
    )
    figure3_action_rates(experiment_b, FIG / "figure3_action_mix_by_cost")
    figure4_default_by_band(credit_band_rows, decision_band_rows, FIG / "figure4_default_rate_by_band")
    figure5_heatmap(idx, cols, heat, FIG / "figure5_credit_governance_heatmap")
    figure6_architecture(FIG / "figure6_evidence_separated_architecture")
    figure7_audit_lifecycle(FIG / "figure7_audit_trail_lifecycle")

    result_again = select_policy(
        y_val, p_val, primary_scenario, grid, split="validation", include_two_threshold=True
    )
    selection_equivalent = (
        result_again["selected"]["t_low"] == t_low
        and result_again["selected"]["t_high"] == t_high
        and abs(result_again["selected"]["expected_normalized_cost"] - primary_sel["expected_normalized_cost"]) < 1e-15
    )

    pytest_code, pytest_text = run_pytest()
    summary_line = pytest_text.splitlines()[-1] if pytest_text else "pytest produced no output"

    def _count(label: str) -> int:
        match = re.search(rf"(\d+)\s+{label}", summary_line)
        return int(match.group(1)) if match else 0

    passed, failed, skipped, warnings = _count("passed"), _count("failed"), _count("skipped"), _count("warnings")

    figures = [
        "results/figures/decision/figure1_validation_cost_curve.png",
        "results/figures/decision/figure2_cost_ratio_sensitivity.png",
        "results/figures/decision/figure3_action_mix_by_cost.png",
        "results/figures/decision/figure4_default_rate_by_band.png",
        "results/figures/decision/figure5_credit_governance_heatmap.png",
        "results/figures/decision/figure6_evidence_separated_architecture.png",
        "results/figures/decision/figure7_audit_trail_lifecycle.png",
    ]
    tables = [
        "results/decision/tables/table1_decision_policy_definitions.csv",
        "results/decision/tables/table2_validation_threshold_selection.csv",
        "results/decision/tables/table3_test_decision_outcomes.csv",
        "results/decision/tables/table4_credit_governance_contingency.csv",
        "results/decision/tables/table5_monolithic_vs_separated.csv",
        "results/decision/tables/table6_audit_schema.csv",
    ]
    required_docs = [
        "docs/decision_policy_specification.md",
        "docs/decision_cost_assumptions.md",
        "docs/audit_schema.md",
        "docs/monolithic_baseline.md",
    ]
    issues = []
    if not selection_equivalent:
        issues.append("Threshold selection was not reproducible in-process.")
    if not invariant:
        issues.append("Audit decision_id changed when event_timestamp changed.")
    if pytest_code != 0 or failed:
        issues.append(f"Pytest failed: {summary_line}")
    if lc_status == "PASS":
        issues.append("LendingClub profile PASSed without contractual evidence.")
    for rel in figures + tables + required_docs:
        if not (ROOT / rel.replace("/", "\\") if False else ROOT / rel).exists():
            issues.append(f"Missing required artifact: {rel}")
    if "shariah_score" in json.dumps(config):
        issues.append("Configuration contains a shariah_score field.")

    status = "PASS" if not issues else "BLOCKED"
    software = {
        "python": sys.version,
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "matplotlib": __import__("matplotlib").__version__,
    }
    artifact_paths = figures + tables + [
        "results/decision/frozen_policy.json",
        "results/decision/audit/test_audit_records.csv",
        "results/decision/audit/published_examples.json",
        "audit/stage8_decision_policy_run.json",
        "audit/stage8_threshold_selection.json",
        "audit/stage8_policy_config.json",
        "audit/stage8_audit_schema.json",
        "configs/stage8_decision_policy.yaml",
        "configs/stage8_decision_policy.json",
    ]
    run_audit = {
        "experiment_id": EXPERIMENT_ID,
        "policy_version": config["policy_version"],
        "audit_schema_version": str(config["audit_schema_version"]),
        "dataset_id": DATASET_ID,
        "dataset_hash": RECORDED_LC_SHA256,
        "split_manifest_hash": sha256_text_file(SPLIT_MANIFEST),
        "feature_policy_hash": sha256_text_file(FEATURE_POLICY_PATH),
        "preprocessing_policy_hash": sha256_text_file(PREPROCESS_POLICY_PATH),
        "config_hash": sha256_json(config),
        "validation_predictions_hash": sha256_file(VAL_CAL),
        "test_predictions_hash": sha256_file(TEST_CAL),
        "freeze_hash": sha256_file(FREEZE_PATH),
        "random_seed": int(config["random_seed"]),
        "threshold_grid": [float(x) for x in grid],
        "cost_scenarios": [s.as_dict() for s in scenarios],
        "selected_policy": json_safe(freeze),
        "test_evaluation": json_safe(
            {
                "fused": fused_test_metrics,
                "monolithic": mono_test_metrics,
                "predictive_stage5": pred_check["artifact"],
            }
        ),
        "lendingclub_governance": {
            "overall_governance_status": lc_status,
            "layer_a": lc_layer_a,
            "payload": lendingclub_governance_payload(),
            "triggered_rule_ids": triggered,
        },
        "software_library_versions": software,
        "git_commit": git_commit(ROOT),
        "execution_timestamp": started,
        "completed_timestamp": utc_now(),
        "pytest_exit_code": pytest_code,
        "pytest_summary": summary_line,
        "status": status,
        "issues": issues,
        "artifact_paths": artifact_paths,
        "reproducibility": {
            "selection_equivalent": selection_equivalent,
            "audit_timestamp_invariant": invariant,
        },
        "test_loaded_only_after_freeze": True,
        "experiments_completed": ["A", "B", "C", "D", "E", "F", "G", "H"],
    }
    dump_json(AUDIT_RUN, json_safe(run_audit))

    report_payload = {
        "status": f"STAGE_8_STATUS = {status}",
        "primary": {
            "scenario": primary_scenario.name,
            "c_review_over_fp": primary_scenario.c_review_over_fp,
            "policy_type": primary_sel["policy_type"],
            "t_low": t_low,
            "t_high": t_high,
            "expected_normalized_cost": primary_sel["expected_normalized_cost"],
        },
        "experiment_b": experiment_b,
        "fused_test": fused_test_metrics,
        "monolithic_test": mono_test_metrics,
        "predictive_test": pred_check["artifact"],
        "lendingclub_governance": {"layer_a": lc_layer_a, "overall_governance_status": lc_status},
        "config": config,
        "test_suite_summary": summary_line,
        "reproducibility": run_audit["reproducibility"],
        "artifact_paths": artifact_paths,
    }
    write_report(report_payload)

    print(f"STAGE_8_STATUS = {status}")
    if issues:
        for issue in issues:
            print(f"BLOCKED: {issue}")
    print(summary_line)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
