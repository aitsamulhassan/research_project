"""Stage 8 v2 per-row L2 fusion. Does not reselect thresholds or refit models."""

from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
from collections import Counter
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
    AUDIT_SCHEMA_VERSION_V2,
    POLICY_VERSION_V2,
    REQUIRED_FIELDS_V2,
    build_record_v2,
    logic_hash_v2,
    schema_document_v2,
)
from decision.config_load import YAML_PATH, load_policy_config  # noqa: E402
from decision.cost_policy import CostScenario  # noqa: E402
from decision.decision_engine import apply_policy  # noqa: E402
from decision.plots import figure4_default_by_band, figure5_heatmap, figure6_architecture  # noqa: E402
from decision.policy_matrix import CREDIT_BANDS, GOVERNANCE_STATUSES  # noqa: E402
from decision.stage8_v2 import (  # noqa: E402
    EXPECTED_T_HIGH,
    EXPECTED_T_LOW,
    FROZEN_DATASET_ID,
    assert_platt_integrity,
    evaluate_row_for_fusion,
    load_frozen_thresholds,
    matrix_from_config,
    review_cause,
)
from decision.threshold_selection import credit_only_decisions  # noqa: E402
from evaluation.decision_metrics import band_outcome_table, policy_metrics  # noqa: E402
from preprocessing.lendingclub_preprocessor import (  # noqa: E402
    RECORDED_LC_SHA256,
    SCRIPT_VERSION as PREPROCESSOR_VERSION,
)

EXPERIMENT_ID = "stage8-lc-decision-v2"
DATASET_ID = FROZEN_DATASET_ID
VAL_CAL = ROOT / "results" / "calibration" / "validation" / "ebm_seed42_calibrated.csv"
TEST_CAL = ROOT / "results" / "calibration" / "test" / "ebm_seed42_calibrated.csv"
STAGE5_TEST = ROOT / "results" / "calibration" / "metrics" / "stage5_test_metrics.json"
GLOBAL_SHAP = ROOT / "results" / "explainability" / "tables" / "table1_global_attribution.csv"
V1_FREEZE = ROOT / "results" / "decision" / "frozen_policy.json"
V1_THRESH = ROOT / "audit" / "stage8_threshold_selection.json"
V1_REPORT = ROOT / "docs" / "STAGE_8_DECISION_POLICY_REPORT.md"
V1_AUDIT = ROOT / "audit" / "stage8_decision_policy_run.json"
OUT = ROOT / "results" / "decision" / "v2"
FIG = ROOT / "results" / "figures" / "decision" / "v2"
TAB = OUT / "tables"
FREEZE_PATH = OUT / "frozen_policy.json"
AUDIT_RUN = ROOT / "audit" / "stage8_v2_decision_fusion_run.json"
REPORT = ROOT / "docs" / "STAGE_8_DECISION_FUSION_REPORT_V2.md"
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
        return None if not np.isfinite(value) else value
    if isinstance(obj, (np.integer, int)) and not isinstance(obj, bool):
        return int(obj)
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    return obj


def load_split_predictions(path: Path, expected_split: str) -> pd.DataFrame:
    frame = pd.read_csv(path)
    splits = set(frame["split"].astype(str).unique())
    if splits != {expected_split}:
        raise RuntimeError(f"{path} splits={splits} expected {{{expected_split}}}")
    need = {"row_ref", "split", "year", "y_true", "p_raw", "p_selected"}
    missing = sorted(need - set(frame.columns))
    if missing:
        raise RuntimeError(f"{path} missing columns {missing}")
    p = frame["p_selected"].to_numpy(dtype=float)
    if frame["p_selected"].isna().any() or np.any(~np.isfinite(p)) or np.any(p < 0.0) or np.any(p > 1.0):
        raise RuntimeError(f"{path} contains invalid probabilities.")
    return frame


def load_test_after_freeze(freeze_path: Path) -> pd.DataFrame:
    if not freeze_path.exists():
        raise RuntimeError("Attempted to load test predictions before freezing the Stage 8 v2 policy.")
    return load_split_predictions(TEST_CAL, "test")


def run_pytest(targets: list[Path] | None = None) -> tuple[int, str]:
    args = [sys.executable, "-m", "pytest"]
    args.extend(str(p) for p in (targets or [ROOT / "tests"]))
    args.extend(["-q", "--tb=short"])
    proc = subprocess.run(args, cwd=ROOT, capture_output=True, text=True)
    text = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
    return proc.returncode, text.strip()


def stage5_platt_test_metrics() -> dict[str, Any]:
    rows = json.loads(STAGE5_TEST.read_text(encoding="utf-8"))
    return next(r for r in rows if r["method"] == "platt")


def verify_stage5_metrics(frame: pd.DataFrame, artifact: dict[str, Any]) -> dict[str, Any]:
    computed = calibration_metrics(frame["y_true"].to_numpy(), frame["p_selected"].to_numpy())
    keys = ["roc_auc", "pr_auc", "brier", "ece"]
    gaps = {k: abs(float(computed[k]) - float(artifact[k])) for k in keys}
    if any(v > 1e-10 for v in gaps.values()):
        raise RuntimeError(f"Stage 8 v2 recomputed metrics disagree with Stage 5 artifacts: {gaps}")
    return {"artifact": artifact, "recomputed": computed, "abs_gap": gaps}


def contingency_table(bands: np.ndarray, statuses: np.ndarray, decisions: np.ndarray, matrix) -> list[dict[str, Any]]:
    rows = []
    for band in CREDIT_BANDS:
        for status in GOVERNANCE_STATUSES:
            mask = (bands == band) & (statuses == status)
            n = int(mask.sum())
            rows.append(
                {
                    "credit_band": band,
                    "governance_status": status,
                    "n": n,
                    "configured_final_policy": matrix[(status, band)],
                    "observed_decisions": sorted({str(v) for v in decisions[mask]}) if n else [],
                }
            )
    return rows


def heatmap_matrix(contingency: list[dict[str, Any]]) -> tuple[list[str], list[str], np.ndarray]:
    values = np.zeros((len(CREDIT_BANDS), len(GOVERNANCE_STATUSES)), dtype=int)
    lookup = {(r["credit_band"], r["governance_status"]): r["n"] for r in contingency}
    short = {
        "NOT_STRUCTURABLE_WITHOUT_REDESIGN": "NOT_STRUCTURABLE",
        "INSUFFICIENT_INFORMATION": "INSUFFICIENT",
        "REVIEW": "REVIEW",
        "PASS": "PASS",
    }
    for i, band in enumerate(CREDIT_BANDS):
        for j, status in enumerate(GOVERNANCE_STATUSES):
            values[i, j] = lookup[(band, status)]
    return list(CREDIT_BANDS), [short[s] for s in GOVERNANCE_STATUSES], values


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(path, index=False)


def fmt(value: Any, digits: int = 6) -> str:
    if value is None or (isinstance(value, float) and not np.isfinite(value)):
        return "NA"
    if isinstance(value, (float, np.floating)):
        return f"{float(value):.{digits}f}"
    return str(value)


def write_report(payload: dict[str, Any]) -> None:
    fused = payload["fused_test"]
    mono = payload["monolithic_test"]
    credit = payload["credit_only_test"]
    lines = [
        "# Stage 8 v2 Decision Fusion Report",
        "",
        "This stage fuses frozen credit-risk probabilities with Stage 7 v2 per-application L2 governance evidence. It does not retrain the EBM, does not refit Platt scaling, does not search thresholds, and does not create a Shariah score.",
        "",
        f"Stage 8 v1 remains historical evidence: `{V1_REPORT.relative_to(ROOT).as_posix()}` and `{V1_AUDIT.relative_to(ROOT).as_posix()}`.",
        "",
        f"**Status:** `STAGE_8_STATUS = {payload['status']}`",
        "",
        "```text",
        "STAGE_9 = BLOCKED",
        "```",
        "",
        "## A. Methodology authority",
        "",
        "Controlling amendment: `AMENDMENT-SHARIAH-001`. Stage 7 v2: `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md`. Fusion matrix: Stage 8 v1 specification `docs/decision_policy_specification.md` (not rewritten).",
        "",
        "## B. Fusion policy (frozen; not re-derived on TEST)",
        "",
        "Credit bands use frozen validation-selected thresholds:",
        "",
        f"- `t_low = {payload['t_low']}`",
        f"- `t_high = {payload['t_high']}`",
        "",
        "Governance × band matrix (unchanged from Stage 8 v1):",
        "",
        "| Governance | LOW | MEDIUM | HIGH |",
        "| --- | --- | --- | --- |",
        "| `NOT_STRUCTURABLE_WITHOUT_REDESIGN` | REJECT | REJECT | REJECT |",
        "| `INSUFFICIENT_INFORMATION` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |",
        "| `REVIEW` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |",
        "| `PASS` | APPROVE | HUMAN_REVIEW | REJECT |",
        "",
        "L1 `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` is dataset context. It is **not** the matrix governance input. L2 `overall_governance_status` is the matrix input. `INSUFFICIENT_INFORMATION` is not converted to PASS or to religious non-compliance.",
        "",
        "## C. Validation-derived (frozen from Stage 8 v1; not recomputed)",
        "",
        f"- Primary cost scenario: `{payload['cost_scenario']}` with `C_REVIEW = 0.25 * C_FP`.",
        f"- Credit-only two-threshold policy: `t_low={payload['t_low']}`, `t_high={payload['t_high']}`.",
        f"- Monolithic single threshold (FN:FP=5:1): `t*={payload['mono_t']}`.",
        "- Thresholds were selected on validation only in Stage 8 v1. Stage 8 v2 did not search a new grid.",
        "",
        "## D. L1 / L2 integration",
        "",
        f"- L1 (once): `{payload['l1_status']}` (`is_applicant_level_ruling=false`).",
        f"- L2 evaluation_mode: `PER_APPLICATION`.",
        f"- Unique TEST evidence hashes: `{payload['n_unique_evidence_hashes']}`.",
        f"- Unique TEST record hashes: `{payload['n_unique_record_hashes']}`.",
        "- Identical evidence hashes with distinct record hashes are expected for LendingClub: contractual fields are absent, so L2 statuses may repeat. That is not broadcast-as-inspection.",
        "",
        "## E. TEST-derived results",
        "",
        f"- n = {payload['n_test']}",
        f"- credit-band counts: {payload['band_counts']}",
        f"- governance-status counts: {payload['gov_counts']}",
        f"- fused decisions: APPROVE={payload['fused_counts']['APPROVE']}, HUMAN_REVIEW={payload['fused_counts']['HUMAN_REVIEW']}, REJECT={payload['fused_counts']['REJECT']}",
        f"- fused approval_rate = {fmt(fused['approval_rate'])}",
        f"- fused review_rate = {fmt(fused['review_rate'])}",
        f"- fused rejection_rate = {fmt(fused['rejection_rate'])}",
        f"- rows with missing governance evidence (L2 INSUFFICIENT_INFORMATION) = {payload['n_insufficient']}",
        f"- rows with NOT_STRUCTURABLE_WITHOUT_REDESIGN = {payload['n_not_structurable']}",
        f"- audit completeness (required v2 fields present) = {payload['audit_complete_rate']}",
        "",
        "### Review burden",
        "",
        f"- review_count = {payload['review_count']}",
        f"- review_rate = {fmt(payload['fused_test']['review_rate'])}",
        f"- review causes: {payload['review_causes']}",
        f"- reviewed credit-band distribution: {payload['review_bands']}",
        "",
        "The review band is a simulated research-policy band. No human-review outcomes were collected.",
        "",
        "### Credit-only vs evidence-separated (same frozen probabilities)",
        "",
        f"- credit-only (bands, no governance): approval={fmt(credit['approval_rate'])}, review={fmt(credit['review_rate'])}, reject={fmt(credit['rejection_rate'])}",
        f"- monolithic single threshold: approval={fmt(mono['approval_rate'])}, review={fmt(mono['review_rate'])}, reject={fmt(mono['rejection_rate'])}",
        f"- evidence-separated fused: approval={fmt(fused['approval_rate'])}, review={fmt(fused['review_rate'])}, reject={fmt(fused['rejection_rate'])}",
        "",
        "Predictive ROC-AUC/Brier are properties of the frozen credit model and are not claimed as architectural improvement.",
        "",
        "### Default rates by fused credit band (TEST labels, evaluation only)",
        "",
        "| Band | n | default_rate |",
        "| --- | ---: | ---: |",
    ]
    for row in payload["credit_band_rows"]:
        lines.append(f"| {row['band']} | {row['n']} | {fmt(row['default_rate'])} |")
    lines += [
        "",
        "## F. What this does not claim",
        "",
        "- No applicant is Shariah compliant or non-compliant.",
        "- LendingClub L2 `INSUFFICIENT_INFORMATION` means insufficient contractual evidence, not a religious finding.",
        "- L1 is not 208,886 applicant-level Shariah evaluations.",
        "- `purpose` is not Shariah evidence.",
        "",
        "## G. Reproducibility",
        "",
        f"- experiment_id: `{EXPERIMENT_ID}`",
        f"- amendment_id: `AMENDMENT-SHARIAH-001`",
        f"- policy_version: `{POLICY_VERSION_V2}`",
        f"- l1l2_version: `{payload['l1l2_version']}`",
        f"- t_low/t_high: `{payload['t_low']}` / `{payload['t_high']}`",
        f"- test_cal_sha256: `{payload['test_cal_sha256']}`",
        f"- v1_freeze_sha256: `{payload['v1_freeze_sha256']}`",
        f"- git_commit: `{payload['git_commit']}`",
        f"- execution_timestamp: `{payload['execution_timestamp']}`",
        f"- software: `{payload['python']}`",
        f"- prerequisite tests: `{payload['prereq_summary']}`",
        f"- final test command: `python -m pytest tests -q --tb=short`",
        f"- final test summary: `{payload['test_summary']}`",
        "",
        "## H. Stage gate",
        "",
        f"`STAGE_8_STATUS = {payload['status']}`",
        "",
        payload.get("status_reason", ""),
        "",
        "```text",
        "STAGE_9 = BLOCKED",
        "```",
        "",
        "## Artifact index",
        "",
    ]
    for path in payload["artifact_paths"]:
        lines.append(f"- `{path}`")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if REPORT.resolve() == V1_REPORT.resolve() or AUDIT_RUN.resolve() == V1_AUDIT.resolve():
        raise RuntimeError("Refusing to overwrite Stage 8 v1 artifacts.")
    started = utc_now()
    freeze_v1 = load_frozen_thresholds()
    platt = assert_platt_integrity()
    v1_config = load_policy_config(YAML_PATH)
    matrix = matrix_from_config(v1_config)
    unknown_as = v1_config["governance_policy"]["unknown_status_treated_as"]
    t_low = float(freeze_v1["t_low"])
    t_high = float(freeze_v1["t_high"])
    if t_low != EXPECTED_T_LOW or t_high != EXPECTED_T_HIGH:
        raise RuntimeError("Threshold integrity check failed.")
    thresh_v1 = json.loads(V1_THRESH.read_text(encoding="utf-8"))
    five = next(row for row in thresh_v1["experiment_b"] if float(row["fn_fp_ratio"]) == 5.0)
    mono_t = float(five["selected_single"]["t_low"])
    primary_scenario = CostScenario(fn_fp_ratio=5.0, c_fp=1.0, c_review_over_fp=0.25)
    mono_scenario = CostScenario(fn_fp_ratio=5.0, c_fp=1.0, c_review_over_fp=0.0)
    top_features = (
        pd.read_csv(GLOBAL_SHAP).sort_values("shap_rank")["feature"].astype(str).head(5).tolist()
    )
    from shariah.l1 import assess_dataset_readiness
    from shariah.engine import L1L2_VERSION

    l1 = assess_dataset_readiness(DATASET_ID)
    if l1["readiness_status"] != "INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION":
        raise RuntimeError("Unexpected L1 status.")

    print("Running prerequisite unit/synthetic tests before TEST...", flush=True)
    prereq_code, prereq_text = run_pytest(
        [
            ROOT / "tests" / "test_stage8_v2.py",
            ROOT / "tests" / "test_stage7_l1l2.py",
            ROOT / "tests" / "test_shariah_rules.py",
            ROOT / "tests" / "test_shariah_provenance.py",
            ROOT / "tests" / "test_stage8_decision.py",
        ]
    )
    prereq_summary = next((line.strip() for line in reversed(prereq_text.splitlines()) if "passed" in line), prereq_text[-400:])
    if prereq_code != 0:
        dump_json(
            AUDIT_RUN,
            {
                "status": "REQUIRES REVISION",
                "status_reason": f"Prerequisite tests failed before TEST: {prereq_summary}",
                "stage9": "BLOCKED",
                "execution_timestamp": utc_now(),
                "pytest_tail": prereq_text[-2000:],
            },
        )
        print(prereq_text[-2000:], flush=True)
        return 2

    freeze = {
        "experiment_id": EXPERIMENT_ID,
        "policy_version": POLICY_VERSION_V2,
        "audit_schema_version": AUDIT_SCHEMA_VERSION_V2,
        "frozen_before_test": True,
        "thresholds_reselected": False,
        "thresholds_source": "results/decision/frozen_policy.json",
        "t_low": t_low,
        "t_high": t_high,
        "policy_type": freeze_v1["policy_type"],
        "selection_split": "validation",
        "cost_scenario": primary_scenario.as_dict(),
        "platt": platt,
        "l1_status": l1["readiness_status"],
        "l1_is_applicant_level_ruling": False,
        "l2_evaluation_mode": "PER_APPLICATION",
        "amendment_id": "AMENDMENT-SHARIAH-001",
        "l1l2_version": L1L2_VERSION,
        "monolithic_t": mono_t,
        "timestamp": utc_now(),
    }
    dump_json(FREEZE_PATH, freeze)
    dump_json(OUT / "audit_schema.json", schema_document_v2())
    print(f"Policy frozen at {FREEZE_PATH}. Loading test predictions once.", flush=True)
    test = load_test_after_freeze(FREEZE_PATH)
    y_test = test["y_true"].to_numpy(dtype=int)
    p_test = test["p_selected"].to_numpy(dtype=float)
    p_raw = test["p_raw"].to_numpy(dtype=float)
    refs = test["row_ref"].astype(str).to_numpy()
    pred_check = verify_stage5_metrics(test, stage5_platt_test_metrics())
    test_cal_sha = sha256_file(TEST_CAL)

    compact_cache: dict[str, dict[str, Any]] = {}
    gov_rows: list[dict[str, Any]] = []
    print(f"Evaluating Stage 7 v2 L2 per TEST row (n={len(test)})...", flush=True)
    for i, ref in enumerate(refs):
        gov_rows.append(
            evaluate_row_for_fusion(
                {"_fixture_key": str(ref)},
                dataset_id=DATASET_ID,
                l1_result=l1,
                timestamp=FIXED_GOV_TS,
                compact_cache=compact_cache,
                synthetic=False,
            )
        )
        if (i + 1) % 50000 == 0:
            print(f"L2 extract {i + 1}/{len(test)} unique_evidence={len(compact_cache)}", flush=True)

    statuses = np.array([g["overall_governance_status"] for g in gov_rows], dtype=object)
    fused = apply_policy(p_test, statuses, t_low, t_high, matrix, unknown_as)
    credit_decisions = credit_only_decisions(p_test, t_low, t_high)
    mono_decisions = credit_only_decisions(p_test, mono_t, mono_t)
    fused_metrics = policy_metrics(y_test, fused["final_decision"], primary_scenario)
    credit_metrics = policy_metrics(y_test, credit_decisions, primary_scenario)
    mono_metrics = policy_metrics(y_test, mono_decisions, mono_scenario)
    credit_band_rows = band_outcome_table(y_test, fused["credit_risk_band"])
    decision_band_rows = band_outcome_table(y_test, fused["final_decision"])
    contingency = contingency_table(fused["credit_risk_band"], fused["shariah_governance_status"], fused["final_decision"], matrix)

    causes: Counter[str] = Counter()
    review_bands: Counter[str] = Counter()
    for band, status, decision in zip(fused["credit_risk_band"], fused["shariah_governance_status"], fused["final_decision"]):
        cause = review_cause(str(band), str(status), str(decision))
        if cause:
            causes[cause] += 1
            review_bands[str(band)] += 1

    n_unique_evi = len({g["evidence_hash"] for g in gov_rows})
    n_unique_rec = len({g["record_reference_hash"] for g in gov_rows})
    if n_unique_rec != len(test):
        raise RuntimeError("Record hashes are not unique per TEST row.")
    if n_unique_evi < 1:
        raise RuntimeError("No evidence hashes produced.")

    event_ts = utc_now()
    threshold_configuration = {
        "t_low": t_low,
        "t_high": t_high,
        "policy_type": freeze_v1["policy_type"],
        "identification": "credit_only_validation_frozen_from_stage8_v1",
        "reselected": False,
    }
    TAB.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    (OUT / "audit").mkdir(parents=True, exist_ok=True)
    audit_csv = OUT / "audit" / "test_audit_records.csv"
    fieldnames = list(REQUIRED_FIELDS_V2)
    sample_records: list[dict[str, Any]] = []
    complete = 0
    with audit_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for i, gov in enumerate(gov_rows):
            rec = build_record_v2(
                event_timestamp=event_ts,
                dataset_id=DATASET_ID,
                dataset_hash=RECORDED_LC_SHA256,
                record_reference_hash=gov["record_reference_hash"],
                evidence_hash=gov["evidence_hash"],
                evaluation_mode=gov["evaluation_mode"],
                l1_status=gov["l1_status"],
                l1_is_applicant_level_ruling=False,
                missing_evidence=list(gov["missing_evidence"]),
                expert_validation_state=gov["expert_validation_state"],
                amendment_id="AMENDMENT-SHARIAH-001",
                l1l2_version=gov["l1l2_version"],
                certification_claim=False,
                model_name="explainable_boosting_machine",
                model_version="stage4b-lc-granting-v1:seed42",
                preprocessor_version=PREPROCESSOR_VERSION,
                calibrator_name="platt",
                calibrator_version="stage5-lc-ebm-calibration-v1",
                raw_probability=float(p_raw[i]),
                calibrated_probability=float(p_test[i]),
                credit_risk_band=str(fused["credit_risk_band"][i]),
                top_explanation_features=top_features,
                shariah_evidence_completeness=gov["layer_a"],
                shariah_governance_status=str(fused["shariah_governance_status"][i]),
                triggered_rule_ids=list(gov["triggered_rule_ids"]),
                rule_source_ids=list(gov["source_ids"]),
                policy_version=POLICY_VERSION_V2,
                cost_scenario=primary_scenario.name,
                threshold_configuration=threshold_configuration,
                final_decision=str(fused["final_decision"][i]),
                review_required=str(fused["final_decision"][i]) == "HUMAN_REVIEW",
            )
            if all(k in rec for k in REQUIRED_FIELDS_V2):
                complete += 1
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
                            "missing_evidence",
                            "threshold_configuration",
                        }
                    },
                    "top_explanation_features": "|".join(rec["top_explanation_features"]),
                    "triggered_rule_ids": "|".join(rec["triggered_rule_ids"]),
                    "rule_source_ids": "|".join(rec["rule_source_ids"]),
                    "missing_evidence": "|".join(rec["missing_evidence"]),
                    "threshold_configuration": json.dumps(rec["threshold_configuration"], sort_keys=True),
                }
            )
            if i < 8:
                sample_records.append(rec)
            if (i + 1) % 50000 == 0:
                print(f"Wrote {i + 1} audit records...", flush=True)

    later_ts = utc_now()
    invariant = all(logic_hash_v2({**rec, "event_timestamp": later_ts}) == rec["decision_id"] for rec in sample_records)
    idx, cols, heat = heatmap_matrix(contingency)
    figure4_default_by_band(credit_band_rows, decision_band_rows, FIG / "figure4_default_rate_by_band")
    figure5_heatmap(idx, cols, heat, FIG / "figure5_credit_governance_heatmap")
    figure6_architecture(FIG / "figure6_evidence_separated_architecture")

    fused_counts = {
        "APPROVE": int((fused["final_decision"] == "APPROVE").sum()),
        "HUMAN_REVIEW": int((fused["final_decision"] == "HUMAN_REVIEW").sum()),
        "REJECT": int((fused["final_decision"] == "REJECT").sum()),
    }
    gov_counts = {str(k): int(v) for k, v in zip(*np.unique(fused["shariah_governance_status"], return_counts=True))}
    band_counts = {str(k): int(v) for k, v in zip(*np.unique(fused["credit_risk_band"], return_counts=True))}
    n_insufficient = int((fused["shariah_governance_status"] == "INSUFFICIENT_INFORMATION").sum())
    n_nsr = int((fused["shariah_governance_status"] == "NOT_STRUCTURABLE_WITHOUT_REDESIGN").sum())

    write_csv(
        TAB / "table1_decision_policy_definitions.csv",
        [
            {"governance": r["governance"], "credit_band": r["credit_band"], "final_decision": r["decision"]}
            for r in v1_config["governance_policy"]["matrix"]
        ],
    )
    write_csv(
        TAB / "table3_test_decision_outcomes.csv",
        [
            {k: v for k, v in {"split": "test", "architecture": "fused_evidence_separated_v2", **fused_metrics}.items() if k not in {"decision_bands", "cost_scenario"}},
            {k: v for k, v in {"split": "test", "architecture": "credit_only_selected_bands", **credit_metrics}.items() if k not in {"decision_bands", "cost_scenario"}},
            {k: v for k, v in {"split": "test", "architecture": "monolithic_credit_threshold", **mono_metrics}.items() if k not in {"decision_bands", "cost_scenario"}},
        ],
    )
    write_csv(TAB / "table3b_test_default_rates_by_band.csv", [{"architecture": "fused_credit_band", **r} for r in credit_band_rows] + [{"architecture": "fused_decision", **r} for r in decision_band_rows])
    write_csv(TAB / "table4_credit_governance_contingency.csv", contingency)
    write_csv(
        TAB / "table_review_burden.csv",
        [{"cause": k, "n": int(v), "share_of_test": v / len(test)} for k, v in causes.items()]
        or [{"cause": "none", "n": 0, "share_of_test": 0.0}],
    )
    dump_json(OUT / "metrics" / "fused_test.json", json_safe({"metrics": fused_metrics, "credit_bands": credit_band_rows, "decision_bands": decision_band_rows}))
    dump_json(OUT / "metrics" / "predictive_test_stage5.json", json_safe(pred_check))
    dump_json(OUT / "audit" / "published_examples.json", sample_records[:5])

    issues = []
    if not invariant:
        issues.append("Audit decision_id changed when event_timestamp changed.")
    if n_unique_rec != len(test):
        issues.append("Broadcast-like record hashes.")
    if n_insufficient != len(test):
        issues.append("Unexpected TEST L2 statuses; LendingClub should be INSUFFICIENT_INFORMATION.")
    if fused_counts["APPROVE"] != 0:
        issues.append("TEST fused policy produced APPROVE without governance PASS.")
    if complete != len(test):
        issues.append("Incomplete audit records.")
    if not V1_REPORT.exists() or not V1_FREEZE.exists():
        issues.append("Stage 8 v1 artifacts missing.")
    artifact_paths = [
        "docs/STAGE_8_DECISION_FUSION_REPORT_V2.md",
        "audit/stage8_v2_decision_fusion_run.json",
        "results/decision/v2/frozen_policy.json",
        "results/decision/v2/tables/table3_test_decision_outcomes.csv",
        "results/decision/v2/audit/test_audit_records.csv",
    ]
    execution_timestamp = utc_now()
    audit_body = {
        "amendment_id": "AMENDMENT-SHARIAH-001",
        "experiment_id": EXPERIMENT_ID,
        "policy_version": POLICY_VERSION_V2,
        "stage7_v2": L1L2_VERSION,
        "t_low": t_low,
        "t_high": t_high,
        "thresholds_reselected": False,
        "platt_a": platt["a"],
        "platt_b": platt["b"],
        "l1_status": l1["readiness_status"],
        "l1_is_applicant_level_ruling": False,
        "l2_evaluation_mode": "PER_APPLICATION",
        "n_test": int(len(test)),
        "n_unique_evidence_hashes": n_unique_evi,
        "n_unique_record_hashes": n_unique_rec,
        "fused_counts": fused_counts,
        "gov_counts": gov_counts,
        "band_counts": band_counts,
        "review_rate": fused_metrics["review_rate"],
        "review_causes": dict(causes),
        "n_insufficient": n_insufficient,
        "audit_complete_rate": complete / len(test),
        "any_expert_validated": False,
        "certification_claim_policy": False,
        "credit_model_not_called": True,
        "protected_test_used_for_evaluation_only": True,
        "stage9": "BLOCKED",
        "test_cal_sha256": test_cal_sha,
        "v1_freeze_sha256": sha256_file(V1_FREEZE),
        "git_commit": git_commit(ROOT),
        "execution_timestamp": execution_timestamp,
        "started": started,
        "prereq_summary": prereq_summary,
        "test_summary": "pending_final_pytest",
        "pytest_exit_code": None,
        "software_library_versions": {"python": sys.version.replace("\n", " "), "pandas": pd.__version__, "numpy": np.__version__},
        "status": "EVALUATION_COMPLETE_PYTEST_PENDING" if not issues else "REQUIRES REVISION",
        "status_reason": "; ".join(issues) if issues else "TEST evaluation complete; final pytest pending.",
        "predictive_check": json_safe(pred_check),
    }
    dump_json(AUDIT_RUN, json_safe(audit_body))
    print("Running full pytest after TEST evaluation and audit write...", flush=True)
    pytest_code, pytest_text = run_pytest()
    summary_line = next((line.strip() for line in reversed(pytest_text.splitlines()) if "passed" in line), "pytest produced no output")

    def _count(label: str) -> int:
        match = re.search(rf"(\d+)\s+{label}", summary_line)
        return int(match.group(1)) if match else 0

    if pytest_code != 0 or _count("failed"):
        issues.append(f"Pytest failed: {summary_line}")
    status = "PASS" if not issues else "REQUIRES REVISION"
    reason = (
        "Stage 8 v2 per-row L2 fusion implemented under AMENDMENT-SHARIAH-001; frozen thresholds reused; no broadcast; pytest passed; Stage 9 blocked."
        if status == "PASS"
        else "; ".join(issues)
    )
    audit_body["test_summary"] = summary_line
    audit_body["pytest_exit_code"] = pytest_code
    audit_body["status"] = status
    audit_body["status_reason"] = reason
    audit_body["execution_timestamp"] = utc_now()
    dump_json(AUDIT_RUN, json_safe(audit_body))
    write_report(
        {
            "status": status,
            "status_reason": reason,
            "t_low": t_low,
            "t_high": t_high,
            "mono_t": mono_t,
            "cost_scenario": primary_scenario.name,
            "l1_status": l1["readiness_status"],
            "l1l2_version": L1L2_VERSION,
            "n_test": int(len(test)),
            "n_unique_evidence_hashes": n_unique_evi,
            "n_unique_record_hashes": n_unique_rec,
            "band_counts": band_counts,
            "gov_counts": gov_counts,
            "fused_counts": fused_counts,
            "n_insufficient": n_insufficient,
            "n_not_structurable": n_nsr,
            "audit_complete_rate": complete / len(test),
            "review_count": fused_counts["HUMAN_REVIEW"],
            "review_causes": dict(causes),
            "review_bands": dict(review_bands),
            "fused_test": fused_metrics,
            "credit_only_test": credit_metrics,
            "monolithic_test": mono_metrics,
            "credit_band_rows": credit_band_rows,
            "test_cal_sha256": test_cal_sha,
            "v1_freeze_sha256": sha256_file(V1_FREEZE),
            "git_commit": git_commit(ROOT),
            "execution_timestamp": audit_body["execution_timestamp"],
            "python": sys.version.replace("\n", " "),
            "prereq_summary": prereq_summary,
            "test_summary": summary_line,
            "artifact_paths": artifact_paths,
        }
    )
    print(json.dumps({"status": status, "n_test": int(len(test)), "unique_record_hashes": n_unique_rec}, indent=2), flush=True)
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
