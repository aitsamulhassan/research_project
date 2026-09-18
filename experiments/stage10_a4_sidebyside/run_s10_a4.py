"""S10-A4-SIDEBYSIDE runner. Citation only. Does not edit authorization files."""

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
from stage10.s10_a4_sidebyside import CLASSIFICATION, EXPERIMENT_ID, json_safe, run_sidebyside  # noqa: E402

METRICS = ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_a4_sidebyside.json"
TABLE = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_a4_sidebyside.csv"
TABLE_CTX = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_a4_dataset_context.csv"
TABLE_XGB = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_a4_xgboost_exploratory_not_primary.csv"
TABLE_MODEL = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_a4_model_evidence.csv"
TABLE_CAL = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_a4_calibration.csv"
TABLE_POLICY = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_a4_policy.csv"
TABLE_TEST = ROOT / "results" / "stage10" / "v1" / "tables" / "s10_a4_test_provenance.csv"
AUDIT = ROOT / "audit" / "stage10_s10_a4_sidebyside.json"
REPORT = ROOT / "docs" / "STAGE_10_S10_A4_SIDEBYSIDE_REPORT.md"
CONFIG = ROOT / "configs" / "stage10" / "s10_a4_sidebyside.yaml"
TEST_FILE = ROOT / "tests" / "test_stage10_a4_sidebyside.py"
FORBIDDEN_WRITE = (
    ROOT / "docs" / "amendments" / "AMENDMENT-STAGE10-AUTHORIZATION.md",
    ROOT / "docs" / "STAGE_10_EXPERIMENTAL_PROTOCOL.md",
    ROOT / "RESEARCH_CONSTITUTION.md",
    ROOT / "results" / "calibration" / "metrics" / "stage5_test_metrics.json",
    ROOT / "results" / "metrics" / "stage4b_test_metrics.json",
    ROOT / "results" / "uci_generalization" / "v1" / "tables" / "uci_test_family_raw.csv",
    ROOT / "results" / "uci_generalization" / "v1" / "metrics" / "uci_test_selected.json",
    ROOT / "docs" / "STAGE_9_4_UCI_GENERALIZATION_REPORT.md",
    ROOT / "audit" / "stage9_4_uci_run.json",
    ROOT / "audit" / "stage4b_modeling_run.json",
    ROOT / "audit" / "stage5_calibration_run.json",
    ROOT / "audit" / "lendingclub_split_manifest.json",
    ROOT / "audit" / "stage9_1_ablation_run.json",
    ROOT / "results" / "decision" / "frozen_policy.json",
    ROOT / "results" / "decision" / "v2" / "frozen_policy.json",
    ROOT / "results" / "decision" / "v2" / "tables" / "table3_test_decision_outcomes.csv",
    ROOT / "results" / "calibration" / "test" / "ebm_seed42_calibrated.csv",
    ROOT / "results" / "calibration" / "raw" / "ebm_train_only_seed42_test.csv",
    ROOT / "results" / "predictions" / "test" / "explainable_boosting_machine_seed42.csv",
    ROOT / "results" / "calibration" / "artifacts" / "platt_record.json",
    ROOT / "docs" / "audits" / "STAGE_9_FINAL_CLOSURE_AUDIT.md",
    ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_i1_identity.json",
    ROOT / "docs" / "STAGE_10_S10_I1_IDENTITY_REPORT.md",
    ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_r1_year.json",
    ROOT / "docs" / "STAGE_10_S10_R1_YEAR_REPORT.md",
    ROOT / "results" / "stage10" / "v1" / "metrics" / "s10_a1_gap.json",
    ROOT / "docs" / "STAGE_10_S10_A1_GAP_REPORT.md",
    ROOT / "src" / "stage10" / "s10_i1_identity.py",
    ROOT / "src" / "stage10" / "s10_r1_year.py",
    ROOT / "src" / "stage10" / "s10_a1_gap.py",
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


def _fmt(value: Any) -> str:
    if value is None:
        return "not reported"
    if isinstance(value, float):
        return f"{value:.6f}"
    return str(value)


def _hash_fmt(value: Any) -> str:
    if value is None:
        return "not recorded in existing artifacts"
    return str(value)


def _model_table_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        item = dict(row)
        hp = item.get("hyperparameters") or {}
        item["hyperparameters"] = json.dumps(hp, sort_keys=True)
        out.append(item)
    return out


def write_report(payload: dict[str, Any], commit: str | None) -> None:
    issues = payload.get("issues") or []
    limitations = list(payload.get("documentation_limitations") or [])
    if commit is None and not any("git_commit is null" in str(item) for item in limitations):
        limitations.append(
            "git_commit is null (no usable .git / git). Recorded, not fabricated. "
            "Stage 10 protocol §14: not by itself a scientific abort."
        )
    hashes = payload.get("hashes") or {}
    disc = payload.get("ebm_test_roc_discrepancy") or {}
    cal = payload.get("calibration_evidence") or {}
    prov = payload.get("test_provenance") or {}
    platt = (cal.get("platt_parameters") or {})
    iso = (cal.get("isotonic_parameters") or {})
    roc_store = cal.get("stored_test_roc_auc") or {}
    roc_note = (cal.get("calibration_changes_roc_auc_according_to_stored_metrics") or {})
    body = [
        "# Stage 10 S10-A4-SIDEBYSIDE report",
        "",
        f"**Classification:** `{CLASSIFICATION}`",
        "",
        f"**Audit classification:** `{payload.get('audit_classification')}`",
        "",
        "This is **not** a new confirmatory experiment. Metrics and counts below are **cited** from existing Stage 3, 4B, 5, 8, 9.1, 9.4, and prior Stage 10 artifacts. They were **not** recomputed.",
        "",
        f"**Experiment ID:** `{EXPERIMENT_ID}` (`S10-A4-SIDEBYSIDE`)  ",
        f"**Status:** `{payload.get('status')}`  ",
        "**Authorization:** `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED` 2026-09-15  ",
        "**This run executed:** `S10-A4-SIDEBYSIDE` only.",
        "",
        "## 1. Purpose",
        "",
        "Describe differences among already-existing LendingClub TEST model, calibration, and policy evidence. Protocol RQ10.4 also cites already-stored UCI LR/EBM TEST metrics. This activity does not train models, rescore TEST, select thresholds, or produce a ranking.",
        "",
        "## 2. Authorization",
        "",
        "- Controlling amendment: `docs/amendments/AMENDMENT-STAGE10-AUTHORIZATION.md` status `APPROVED` 2026-09-15.",
        "- Controlling protocol: `docs/STAGE_10_EXPERIMENTAL_PROTOCOL.md` activity `S10-A4-SIDEBYSIDE`.",
        "- Authorized Stage 10 activities: S10-I1-IDENTITY, S10-R1-YEAR, S10-A1-GAP, S10-A4-SIDEBYSIDE.",
        f"- Prior gates: S10-I1 `{payload.get('prior_gates', {}).get('i1_status')}`; S10-R1 `{payload.get('prior_gates', {}).get('r1_status')}`; S10-A1 `{payload.get('prior_gates', {}).get('a1_status')}`.",
        "- Stage 9 remains CLOSED. Stage 11 and paper drafting remain unauthorized.",
        "",
        "## Bound statements",
        "",
        "- No model was retrained. No EBM was refit. No model was loaded for scoring.",
        "- No calibrator was refit. No threshold was selected or changed.",
        "- No new TEST AUC, PR-AUC, Brier, log-loss, or ECE was calculated from predictions.",
        "- Policy assignments were not recomputed. A0/A1/A3/A4 counts are cited from stored Stage 8 v2 table3 / Stage 9.1.",
        "- LendingClub TEST membership was not recomputed.",
        "- UCI TEST was not reopened for model or calibration selection.",
        "- LendingClub thresholds and calibration were not transferred to UCI.",
        "- XGBoost is **not** in the primary comparison and is **not** ratified.",
        "- No overall model ranking was produced.",
        "- The Stage 4B vs Stage 5 EBM TEST ROC-AUC discrepancy investigation was **not** reopened.",
        "- Stage 4B/5/8/9/9.4, S10-I1, S10-R1, and S10-A1-GAP artifacts were not overwritten.",
        "- Stage 9 remains **CLOSED**. The paper was not drafted.",
        "",
        "## 3. Data/provenance basis",
        "",
        "LendingClub TEST is the frozen Stage 3 split (`issue_month >= 2017-02`). UCI TEST is cited only from already-stored Stage 9.4 family metrics. The two datasets are not merged.",
        "",
        "| Dataset | Target definition | Split methodology | Role in the research architecture | Shariah governance applied |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in payload.get("dataset_context") or []:
        body.append(
            f"| {row['dataset']} | {row['target_definition']} | {row['split_methodology']} | "
            f"{row['role_in_research_architecture']} | {row['shariah_governance_applied']} |"
        )
    body.extend(
        [
            "",
            "## 4. Model side-by-side comparison",
            "",
            "Stage 4B EBM: TRAIN+VALIDATION refit",
            "",
            "Stage 5 EBM: TRAIN-only fit",
            "",
            "Their stored TEST ROC-AUC values are not treated as a contradiction. Classification: "
            f"`{disc.get('classification')}`.",
            "",
            "| Evidence | Family | Model artifact | Model hash | Training split | Training rows | Seed | Probability | Stored TEST ROC-AUC | Used by Stage 8 onward | Provenance |",
            "| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | --- | --- |",
        ]
    )
    for row in payload.get("model_evidence") or []:
        body.append(
            f"| {row['label']} | `{row['model_family']}` | `{row['model_artifact_path']}` | "
            f"`{_hash_fmt(row.get('model_hash'))}` | {row['training_split']} | "
            f"{_fmt(row.get('training_row_count'))} | {row['seed']} | {row['probability_type']} | "
            f"{_fmt(row.get('stored_roc_auc'))} | {row['used_by_stage8_onward']} | {row['provenance_status']} |"
        )
    body.extend(
        [
            "",
            "Recorded hyperparameters (same `ebm_config` keys in Stage 4B TEST metrics and Stage 5 TRAIN-only meta): "
            "interactions=0, max_bins=256, learning_rate=0.02, max_rounds=200, outer_bags=4, inner_bags=0, "
            "validation_size=0.15 (EBM-internal), early_stopping_rounds=20, random_state=42.",
            "",
            "Prediction artifacts:",
            "",
            "- Stage 4B: `results/predictions/test/explainable_boosting_machine_seed42.csv` (`p_hat`)",
            "- Stage 5 raw: `results/calibration/raw/ebm_train_only_seed42_test.csv` (`p_raw`)",
            "- Stage 5 calibrated: `results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected`)",
            "",
            "Preprocessing artifacts:",
            "",
            "- Stage 4B TEST: `results/artifacts/preprocessor_train_plus_validation.joblib`",
            "- Stage 5: `results/artifacts/lendingclub_preprocessor.joblib` (train-only)",
            "",
            "Stage 8 onward uses `results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected`) from the Stage 5 TRAIN-only EBM "
            f"`results/calibration/artifacts/ebm_train_only_seed42.joblib` (recorded SHA-256 `{payload.get('stage8_onward_model_hash')}`).",
            "",
            "### Protocol citation inventory (RQ10.4; existing stored metrics only)",
            "",
            "UCI TEST was **not** reopened. LR and EBM only in this table. UCI LR/EBM inherit Stage 9.4 freeze-backed provenance for the approved written scope.",
            "",
            "| Dataset | Model | Calibration | Existing TEST ROC-AUC | Existing TEST PR-AUC | Existing TEST Brier | Existing TEST Log Loss | Existing ECE | Evidence status |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in payload.get("primary_rows") or []:
        body.append(
            f"| {row['dataset']} | {row['model']} | {row['calibration']} | "
            f"{_fmt(row['existing_test_roc_auc'])} | {_fmt(row['existing_test_pr_auc'])} | "
            f"{_fmt(row['existing_test_brier'])} | {_fmt(row['existing_test_log_loss'])} | "
            f"{_fmt(row['existing_test_ece'])} | {row['evidence_status']} |"
        )
    body.extend(
        [
            "",
            "`not reported` means the metric is not stored in the cited artifact. Values were not estimated.",
            "",
            "### Exploratory UCI XGBoost (not primary; not ratified)",
            "",
            "Approved Stage 9.4 written scope: Logistic Regression + EBM. XGBoost was an execution-time scope expansion (`DEVIATION-001`). It is **not** ratified and is **not** pre-registered confirmatory evidence.",
            "",
            "| Dataset | Model | Calibration | Existing TEST ROC-AUC | Existing TEST PR-AUC | Existing TEST Brier | Existing TEST Log Loss | Existing ECE | Evidence status |",
            "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in payload.get("exploratory_xgboost_rows") or []:
        body.append(
            f"| {row['dataset']} | {row['model']} | {row['calibration']} | "
            f"{_fmt(row['existing_test_roc_auc'])} | {_fmt(row['existing_test_pr_auc'])} | "
            f"{_fmt(row['existing_test_brier'])} | {_fmt(row['existing_test_log_loss'])} | "
            f"{_fmt(row['existing_test_ece'])} | {row['evidence_status']} |"
        )
    body.extend(
        [
            "",
            "The Stage 9.4 file `uci_vs_lendingclub_test_alongside.csv` is **not** reused as the S10-A4 primary table.",
            "",
            "## 5. Calibration side-by-side comparison",
            "",
            f"- Raw EBM probability artifact: `{cal.get('raw_probability_artifact')}`",
            f"- Calibrated probability artifact: `{cal.get('calibrated_probability_artifact')}`",
            f"- Methods already stored: {', '.join(f'`{m}`' for m in (cal.get('methods_stored') or []))}",
            f"- Frozen selected method: `{cal.get('selected_method')}`",
            f"- Frozen selected probability column: `{cal.get('frozen_selected_probability_column')}` (equals stored `{cal.get('selected_column_equals_stored')}`)",
            f"- Calibrator fit split: `{cal.get('fit_split')}`",
            f"- Protocol: `{cal.get('protocol')}`",
            f"- Platt parameters: a=`{platt.get('a')}`, b=`{platt.get('b')}`, form=`{platt.get('form')}`",
            f"- Isotonic parameters stored: y_min=`{iso.get('y_min')}`, y_max=`{iso.get('y_max')}`, out_of_bounds=`{iso.get('out_of_bounds')}`, increasing=`{iso.get('increasing')}`",
            f"- Stored TEST ROC-AUC raw=`{_fmt(roc_store.get('raw'))}`; Platt=`{_fmt(roc_store.get('platt'))}`; isotonic=`{_fmt(roc_store.get('isotonic'))}`",
            f"- Does stored Platt change ROC-AUC vs raw? `{roc_note.get('platt_vs_raw')}`. Does stored isotonic differ from raw ROC-AUC? `{roc_note.get('isotonic_vs_raw')}`.",
            f"- {roc_note.get('note')}",
            "",
            "## 6. Policy side-by-side comparison",
            "",
            "Counts are copied from stored Stage 8 v2 `table3_test_decision_outcomes.csv` and Stage 9.1 audit. Assignments were not recomputed.",
            "",
            "| Policy | Definition | APPROVE | HUMAN_REVIEW | REJECT | Governance | Evidence-gap fields (already stored) |",
            "| --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    for row in payload.get("policy_evidence") or []:
        body.append(
            f"| {row['policy']} | {row['definition']} | {row['APPROVE']} | {row['HUMAN_REVIEW']} | "
            f"{row['REJECT']} | {row['governance']} | {row['evidence_gap_fields']} |"
        )
    body.extend(
        [
            "",
            "A4 is reported because the Stage 9.0 freeze defines it as the same object as A3. It is not a second TEST assignment.",
            "",
            "## 7. TEST provenance",
            "",
            f"- TEST n (Stage 3 manifest): `{prov.get('test_n_stage3_manifest')}`",
            f"- TEST n (Stage 4B EBM metrics): `{prov.get('test_n_stage4b_ebm_metrics')}`",
            f"- TEST n (Stage 5 raw / Platt metrics): `{prov.get('test_n_stage5_raw_metrics')}` / `{prov.get('test_n_stage5_platt_metrics')}`",
            f"- Frozen Stage 3 TEST hash: `{prov.get('stage3_test_hash')}`",
            f"- TEST rule: `{prov.get('stage3_test_rule')}`",
            f"- Dataset hash (manifest / Stage 4B audit / Stage 5 audit): `{prov.get('dataset_hash_manifest')}` / `{prov.get('dataset_hash_stage4b_audit')}` / `{prov.get('dataset_hash_stage5_audit')}`",
            f"- Split manifest hash (Stage 4B audit / Stage 5 audit): `{prov.get('split_manifest_hash_stage4b_audit')}` / `{prov.get('split_manifest_hash_stage5_audit')}`",
            f"- Same frozen TEST split according to recorded hashes and n: `{prov.get('same_frozen_test_split_according_to_recorded_hashes')}`",
            f"- Membership recomputed in S10-A4: `{prov.get('membership_recomputed')}`",
            "",
            "## 8. Neutral interpretation",
            "",
            "**Supported by stored evidence.** Stage 4B TEST EBM and Stage 5 TEST EBM are different fitted models: TRAIN+VALIDATION refit versus TRAIN-only fit, with different recorded preprocessors and different stored probability files. They share recorded hyperparameters, seed 42, and the same frozen Stage 3 TEST split (n=208886). Stored Stage 4B EBM TEST ROC-AUC is 0.6799408767429772; stored Stage 5 raw TEST ROC-AUC is 0.6776693941139847. That gap is classified `EXPLAINED` and is not a measurement contradiction. Stored Stage 5 Platt TEST ROC-AUC equals stored raw TEST ROC-AUC. Stage 8/9 consume stored `p_selected` from the Stage 5 TRAIN-only pipeline, not Stage 4B TEST `p_hat`.",
            "",
            "**Supported by stored evidence.** A0, A1, and A3/A4 are different decision maps on the same stored `p_selected`. A0 is credit-only two-threshold (5232 / 203627 / 27). A1 applies frozen G0 to the same credit bands; stored L2 is INSUFFICIENT_INFORMATION on all 208886 TEST rows, which routes LOW and MEDIUM to HUMAN_REVIEW and HIGH to REJECT (0 / 208859 / 27). A3/A4 remove the review branch with t*=0.16 (61855 / 0 / 147031).",
            "",
            "**Interpretation (not a new empirical finding).** Policy-count differences are routing/governance-map differences, not a change of the credit model. The A1 review allocation is the stored evidence-gap effect (schema/governance insufficiency under G0), not a claim that governance improved or reduced discrimination. UCI LR/EBM numbers are an independent methodology-context citation; they are not a test of LC Shariah governance or LC thresholds.",
            "",
            "## 9. Limitations",
            "",
        ]
    )
    for item in limitations:
        body.append(f"- {item}")
    body.extend(
        [
            "",
            "## Missing metrics / provenance",
            "",
            *[f"- {item}" for item in payload.get("missing_metrics") or []],
            "",
            "## 10. Audit classification",
            "",
            f"`{payload.get('audit_classification')}`",
            "",
            "The activity remained analysis-only / descriptive and non-confirmatory. Authorization is `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED`. Documentation limitations are the unrecorded Stage 4B final-EBM hash, the unstored concatenated TRAIN+VALIDATION row total, missing ECE in some cited tables, and git_commit null. These do not convert the activity into an unauthorized or invalid run.",
            "",
            "## 11. No new confirmatory experiment",
            "",
            "No new confirmatory experiment was performed. S10-A4-SIDEBYSIDE cites existing artifacts. Favorable or unfavorable stored numbers do not create a confirmatory TEST result.",
            "",
            "## Issues",
            "",
            *([f"- {item}" for item in issues] if issues else ["- None."]),
            "",
            "## Provenance hashes",
            "",
            f"- Stage 5 TEST metrics SHA-256: `{hashes.get('stage5_test_metrics_sha256')}`",
            f"- Stage 4B TEST metrics SHA-256: `{hashes.get('stage4b_test_metrics_sha256')}`",
            f"- table3 SHA-256: `{hashes.get('table3_sha256')}`",
            f"- UCI family-raw TEST SHA-256: `{hashes.get('uci_test_family_raw_sha256')}`",
            f"- UCI selected TEST SHA-256: `{hashes.get('uci_test_selected_sha256')}` (exploratory XGBoost+isotonic row)",
            f"- Recorded Stage 5 EBM joblib SHA-256: `{hashes.get('recorded_ebm_train_only_joblib_sha256')}`",
            f"- Recorded TEST calibrated CSV SHA-256: `{hashes.get('recorded_test_cal_sha256')}`",
            f"- git_commit: `{commit}`",
            "- Source artifacts:",
            *[f"  - `{path}`" for path in payload.get("source_artifacts") or []],
            "",
        ]
    )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(body) + "\n", encoding="utf-8")


def main() -> int:
    started = utc_now()
    before = {str(p): sha256_file(p) for p in FORBIDDEN_WRITE if p.exists()}
    commit = git_commit(ROOT)
    payload = run_sidebyside()
    if commit is None:
        payload["documentation_limitations"] = list(payload.get("documentation_limitations") or []) + [
            "git_commit is null (no usable .git / git). Recorded, not fabricated. "
            "Stage 10 protocol §14: not by itself a scientific abort."
        ]
    payload["git_commit"] = commit
    dump_json(METRICS, payload)
    if not payload.get("issues"):
        TABLE.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(payload.get("primary_rows") or []).to_csv(TABLE, index=False)
        pd.DataFrame(payload.get("dataset_context") or []).to_csv(TABLE_CTX, index=False)
        pd.DataFrame(payload.get("exploratory_xgboost_rows") or []).to_csv(TABLE_XGB, index=False)
        pd.DataFrame(_model_table_rows(payload.get("model_evidence") or [])).to_csv(TABLE_MODEL, index=False)
        cal = payload.get("calibration_evidence") or {}
        roc_note = cal.get("calibration_changes_roc_auc_according_to_stored_metrics") or {}
        pd.DataFrame(
            [
                {
                    "raw_probability_artifact": cal.get("raw_probability_artifact"),
                    "calibrated_probability_artifact": cal.get("calibrated_probability_artifact"),
                    "selected_method": cal.get("selected_method"),
                    "frozen_selected_probability_column": cal.get("frozen_selected_probability_column"),
                    "platt_a": (cal.get("platt_parameters") or {}).get("a"),
                    "platt_b": (cal.get("platt_parameters") or {}).get("b"),
                    "stored_raw_roc_auc": (cal.get("stored_test_roc_auc") or {}).get("raw"),
                    "stored_platt_roc_auc": (cal.get("stored_test_roc_auc") or {}).get("platt"),
                    "stored_isotonic_roc_auc": (cal.get("stored_test_roc_auc") or {}).get("isotonic"),
                    "platt_changes_roc_auc": roc_note.get("platt_vs_raw"),
                    "isotonic_differs_from_raw_roc_auc": roc_note.get("isotonic_vs_raw"),
                }
            ]
        ).to_csv(TABLE_CAL, index=False)
        pd.DataFrame(payload.get("policy_evidence") or []).to_csv(TABLE_POLICY, index=False)
        pd.DataFrame([payload.get("test_provenance") or {}]).to_csv(TABLE_TEST, index=False)
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
        raise RuntimeError(f"S10-A4 runner mutated protected files: {before} vs {after}")
    dump_json(
        AUDIT,
        {
            "experiment_id": EXPERIMENT_ID,
            "amendment_id": "AMENDMENT-STAGE10-AUTHORIZATION",
            "amendment_status": "APPROVED",
            "started": started,
            "execution_timestamp": utc_now(),
            "git_commit": commit,
            "status": payload.get("status"),
            "audit_classification": payload.get("audit_classification"),
            "classification": CLASSIFICATION,
            "confirmatory_experiment": False,
            "new_confirmatory_experiment_performed": False,
            "metrics_recomputed": False,
            "models_trained": False,
            "models_loaded_for_scoring": False,
            "calibration_refit": False,
            "thresholds_searched": False,
            "policy_assignments_recomputed": False,
            "uci_reopened": False,
            "xgboost_in_primary_table": False,
            "xgboost_ratified": False,
            "overall_model_ranking_produced": False,
            "stage9_reopened": False,
            "discrepancy_reopened": False,
            "issues": payload.get("issues"),
            "documentation_limitations": payload.get("documentation_limitations"),
            "hashes": payload.get("hashes"),
            "protected_files_unchanged": after == before,
            "config_sha256": sha256_file(CONFIG) if CONFIG.exists() else None,
            "metrics_sha256": sha256_file(METRICS),
            "report_sha256": sha256_file(REPORT),
            "table_sha256": sha256_file(TABLE) if TABLE.exists() else None,
            "model_table_sha256": sha256_file(TABLE_MODEL) if TABLE_MODEL.exists() else None,
            "policy_table_sha256": sha256_file(TABLE_POLICY) if TABLE_POLICY.exists() else None,
            "pytest_exit_code": exit_code,
            "test_command": f"python -m pytest {TEST_FILE.relative_to(ROOT).as_posix()} -q --tb=short",
            "test_summary": test_summary,
            "software": {"python": sys.version},
            "random_seed_used": None,
            "authorized_stage10_activities_complete_after_this_run": payload.get(
                "authorized_stage10_activities_complete_after_this_run"
            ),
        },
    )
    if payload.get("issues"):
        return 1
    return 0 if exit_code == 0 else exit_code


if __name__ == "__main__":
    raise SystemExit(main())
