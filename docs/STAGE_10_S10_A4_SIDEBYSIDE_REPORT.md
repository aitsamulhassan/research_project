# Stage 10 S10-A4-SIDEBYSIDE report

**Classification:** `ANALYSIS-ONLY / DESCRIPTIVE COMPARISON`

**Audit classification:** `PASS WITH DOCUMENTATION LIMITATION`

This is **not** a new confirmatory experiment. Metrics and counts below are **cited** from existing Stage 3, 4B, 5, 8, 9.1, 9.4, and prior Stage 10 artifacts. They were **not** recomputed.

**Experiment ID:** `s10_a4_sidebyside_v1` (`S10-A4-SIDEBYSIDE`)  
**Status:** `PASS WITH DOCUMENTATION LIMITATION`  
**Authorization:** `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED` 2026-09-15  
**This run executed:** `S10-A4-SIDEBYSIDE` only.

## 1. Purpose

Describe differences among already-existing LendingClub TEST model, calibration, and policy evidence. Protocol RQ10.4 also cites already-stored UCI LR/EBM TEST metrics. This activity does not train models, rescore TEST, select thresholds, or produce a ranking.

## 2. Authorization

- Controlling amendment: `docs/amendments/AMENDMENT-STAGE10-AUTHORIZATION.md` status `APPROVED` 2026-09-15.
- Controlling protocol: `docs/STAGE_10_EXPERIMENTAL_PROTOCOL.md` activity `S10-A4-SIDEBYSIDE`.
- Authorized Stage 10 activities: S10-I1-IDENTITY, S10-R1-YEAR, S10-A1-GAP, S10-A4-SIDEBYSIDE.
- Prior gates: S10-I1 `PASS WITH DOCUMENTATION LIMITATION`; S10-R1 `COMPLETED — exploratory/descriptive post-hoc reanalysis`; S10-A1 `COMPLETED — analysis-only descriptive decomposition`.
- Stage 9 remains CLOSED. Stage 11 and paper drafting remain unauthorized.

## Bound statements

- No model was retrained. No EBM was refit. No model was loaded for scoring.
- No calibrator was refit. No threshold was selected or changed.
- No new TEST AUC, PR-AUC, Brier, log-loss, or ECE was calculated from predictions.
- Policy assignments were not recomputed. A0/A1/A3/A4 counts are cited from stored Stage 8 v2 table3 / Stage 9.1.
- LendingClub TEST membership was not recomputed.
- UCI TEST was not reopened for model or calibration selection.
- LendingClub thresholds and calibration were not transferred to UCI.
- XGBoost is **not** in the primary comparison and is **not** ratified.
- No overall model ranking was produced.
- The Stage 4B vs Stage 5 EBM TEST ROC-AUC discrepancy investigation was **not** reopened.
- Stage 4B/5/8/9/9.4, S10-I1, S10-R1, and S10-A1-GAP artifacts were not overwritten.
- Stage 9 remains **CLOSED**. The paper was not drafted.

## 3. Data/provenance basis

LendingClub TEST is the frozen Stage 3 split (`issue_month >= 2017-02`). UCI TEST is cited only from already-stored Stage 9.4 family metrics. The two datasets are not merged.

| Dataset | Target definition | Split methodology | Role in the research architecture | Shariah governance applied |
| --- | --- | --- | --- | --- |
| LendingClub granting extract | Default; 1=Charged Off, 0=Fully Paid | Temporal by issue_month; TEST issue_month >= 2017-02; n=208886 | Primary dataset for the evidence-separated decision architecture (credit bands + L1/L2 + G0) | Yes (Stage 7 v2 L1/L2 + Stage 8 v2 G0 on LC TEST) |
| UCI Default of Credit Card Clients | default payment next month; 1=default next month, 0=no default next month | Stratified 70/15/15, seed 42; NO_CALENDAR_TIMESTAMPS; TEST n=4502 | Independent credit-risk / calibration methodology context only. Not a test of the evidence-separated architecture as a whole | No. UCI lacks contract-level fields (Stage 2 / U3 metadata-only). UCI does not validate Shariah governance |

## 4. Model side-by-side comparison

Stage 4B EBM: TRAIN+VALIDATION refit

Stage 5 EBM: TRAIN-only fit

Their stored TEST ROC-AUC values are not treated as a contradiction. Classification: `EXPLAINED`.

| Evidence | Family | Model artifact | Model hash | Training split | Training rows | Seed | Probability | Stored TEST ROC-AUC | Used by Stage 8 onward | Provenance |
| --- | --- | --- | --- | --- | --- | ---: | --- | ---: | --- | --- |
| Stage 4B EBM TEST | `explainable_boosting_machine` | `results/artifacts/final_explainable_boosting_machine_seed42.joblib` | `not recorded in existing artifacts` | TRAIN+VALIDATION refit | TRAIN=941267 + VALIDATION=197528; concatenated total not stored as a single field | 42 | raw (p_hat) | 0.679941 | False | freeze-backed Stage 4B TEST; TRAIN+VALIDATION refit |
| Stage 5 TRAIN-only EBM raw TEST | `explainable_boosting_machine` | `results/calibration/artifacts/ebm_train_only_seed42.joblib` | `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4` | TRAIN-only fit | 941267 | 42 | raw (p_raw) | 0.677669 | False | freeze-backed Stage 5 TEST raw; TRAIN-only fit |
| Stage 5 calibrated TEST (selected Platt) | `explainable_boosting_machine` | `results/calibration/artifacts/ebm_train_only_seed42.joblib` | `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4` | TRAIN-only fit | 941267 | 42 | calibrated (p_selected = p_platt) | 0.677669 | True | freeze-backed Stage 5 selected calibrator; frozen Stage 8/9 probability |

Recorded hyperparameters (same `ebm_config` keys in Stage 4B TEST metrics and Stage 5 TRAIN-only meta): interactions=0, max_bins=256, learning_rate=0.02, max_rounds=200, outer_bags=4, inner_bags=0, validation_size=0.15 (EBM-internal), early_stopping_rounds=20, random_state=42.

Prediction artifacts:

- Stage 4B: `results/predictions/test/explainable_boosting_machine_seed42.csv` (`p_hat`)
- Stage 5 raw: `results/calibration/raw/ebm_train_only_seed42_test.csv` (`p_raw`)
- Stage 5 calibrated: `results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected`)

Preprocessing artifacts:

- Stage 4B TEST: `results/artifacts/preprocessor_train_plus_validation.joblib`
- Stage 5: `results/artifacts/lendingclub_preprocessor.joblib` (train-only)

Stage 8 onward uses `results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected`) from the Stage 5 TRAIN-only EBM `results/calibration/artifacts/ebm_train_only_seed42.joblib` (recorded SHA-256 `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4`).

### Protocol citation inventory (RQ10.4; existing stored metrics only)

UCI TEST was **not** reopened. LR and EBM only in this table. UCI LR/EBM inherit Stage 9.4 freeze-backed provenance for the approved written scope.

| Dataset | Model | Calibration | Existing TEST ROC-AUC | Existing TEST PR-AUC | Existing TEST Brier | Existing TEST Log Loss | Existing ECE | Evidence status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| LendingClub | logistic_regression | none (Stage 4B TEST; no stored Platt row) | 0.676356 | 0.340648 | 0.219984 | 0.635413 | not reported | freeze-backed Stage 4B TEST citation |
| LendingClub | explainable_boosting_machine | raw (Stage 5 TEST; TRAIN-only EBM) | 0.677669 | 0.350963 | 0.157936 | 0.488086 | 0.037535 | freeze-backed Stage 5 TEST citation |
| LendingClub | explainable_boosting_machine | platt (Stage 5 selected calibrator; frozen decision pipeline) | 0.677669 | 0.350963 | 0.156169 | 0.483570 | 0.020267 | freeze-backed Stage 5 TEST citation |
| UCI | logistic_regression | raw (Stage 9.4 family TEST; not UCI-selected family) | 0.757278 | 0.525511 | 0.187096 | 0.570735 | not reported | freeze-backed Stage 9.4 approved scope (LR+EBM) |
| UCI | explainable_boosting_machine | raw (Stage 9.4 family TEST; not UCI-selected family) | 0.768856 | 0.537376 | 0.137432 | 0.438423 | not reported | freeze-backed Stage 9.4 approved scope (LR+EBM) |

`not reported` means the metric is not stored in the cited artifact. Values were not estimated.

### Exploratory UCI XGBoost (not primary; not ratified)

Approved Stage 9.4 written scope: Logistic Regression + EBM. XGBoost was an execution-time scope expansion (`DEVIATION-001`). It is **not** ratified and is **not** pre-registered confirmatory evidence.

| Dataset | Model | Calibration | Existing TEST ROC-AUC | Existing TEST PR-AUC | Existing TEST Brier | Existing TEST Log Loss | Existing ECE | Evidence status |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| UCI | xgboost | raw (Stage 9.4 family TEST) | 0.773351 | 0.545664 | 0.181736 | 0.551860 | not reported | EXPLORATORY — execution-time scope expansion; NOT ratified; NOT pre-registered |
| UCI | xgboost | isotonic (Stage 9.4 selected UCI TEST row) | 0.770878 | 0.522421 | 0.136853 | 0.449533 | 0.017443 | EXPLORATORY — execution-time scope expansion; NOT ratified; NOT pre-registered |

The Stage 9.4 file `uci_vs_lendingclub_test_alongside.csv` is **not** reused as the S10-A4 primary table.

## 5. Calibration side-by-side comparison

- Raw EBM probability artifact: `results/calibration/raw/ebm_train_only_seed42_test.csv`
- Calibrated probability artifact: `results/calibration/test/ebm_seed42_calibrated.csv`
- Methods already stored: `raw`, `platt`, `isotonic`
- Frozen selected method: `platt`
- Frozen selected probability column: `p_selected` (equals stored `p_platt`)
- Calibrator fit split: `validation`
- Protocol: `validation_only_calibration_no_train_val_calibrator_refit`
- Platt parameters: a=`1.1988263209549705`, b=`0.6697765046966161`, form=`sigmoid(a * logit(p_raw) + b)`
- Isotonic parameters stored: y_min=`0.0`, y_max=`1.0`, out_of_bounds=`clip`, increasing=`True`
- Stored TEST ROC-AUC raw=`0.677669`; Platt=`0.677669`; isotonic=`0.677514`
- Does stored Platt change ROC-AUC vs raw? `False`. Does stored isotonic differ from raw ROC-AUC? `True`.
- Stored Platt TEST ROC-AUC equals stored raw TEST ROC-AUC. Stored isotonic TEST ROC-AUC differs slightly. No calibrator was fit or compared in S10-A4.

## 6. Policy side-by-side comparison

Counts are copied from stored Stage 8 v2 `table3_test_decision_outcomes.csv` and Stage 9.1 audit. Assignments were not recomputed.

| Policy | Definition | APPROVE | HUMAN_REVIEW | REJECT | Governance | Evidence-gap fields (already stored) |
| --- | --- | ---: | ---: | ---: | --- | --- |
| A0 | credit-only two-threshold | 5232 | 203627 | 27 | off | Governance off. Credit-only two-threshold map on stored p_selected (t_low=0.06, t_high=0.69). L1/L2 are not decision inputs. |
| A1 | evidence-separated G0 fusion | 0 | 208859 | 27 | G0 on (Stage 7 v2 L2) | G0 on. Stored L1=INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION (n=208886; not an applicant-level ruling). Stored L2 INSUFFICIENT_INFORMATION n=208886. G0 maps INSUFFICIENT_INFORMATION × LOW/MEDIUM → HUMAN_REVIEW and × HIGH → REJECT. |
| A3 | binary no-review comparator | 61855 | 0 | 147031 | off | Governance off. Binary map on stored p_selected (t*=0.16). HUMAN_REVIEW branch absent by construction. |
| A4 | collapses to A3 (Stage 9.0 freeze) | 61855 | 0 | 147031 | off | Same object as A3 under the Stage 9.0 freeze (Stage 9.1 a3_identical_to_a4=true). Counts are not a second independent assignment. |

A4 is reported because the Stage 9.0 freeze defines it as the same object as A3. It is not a second TEST assignment.

## 7. TEST provenance

- TEST n (Stage 3 manifest): `208886`
- TEST n (Stage 4B EBM metrics): `208886`
- TEST n (Stage 5 raw / Platt metrics): `208886` / `208886`
- Frozen Stage 3 TEST hash: `4dfedb1ad7785fa3833047135b1883676f3e1b49aca9c87fcdb346e64fd489c6`
- TEST rule: `issue_month >= 2017-02`
- Dataset hash (manifest / Stage 4B audit / Stage 5 audit): `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc` / `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc` / `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc`
- Split manifest hash (Stage 4B audit / Stage 5 audit): `d4db2099199258ae5ca4f5a85a7ce8e7dde2943a0bf7b9239212cce1e44d0e70` / `d4db2099199258ae5ca4f5a85a7ce8e7dde2943a0bf7b9239212cce1e44d0e70`
- Same frozen TEST split according to recorded hashes and n: `True`
- Membership recomputed in S10-A4: `False`

## 8. Neutral interpretation

**Supported by stored evidence.** Stage 4B TEST EBM and Stage 5 TEST EBM are different fitted models: TRAIN+VALIDATION refit versus TRAIN-only fit, with different recorded preprocessors and different stored probability files. They share recorded hyperparameters, seed 42, and the same frozen Stage 3 TEST split (n=208886). Stored Stage 4B EBM TEST ROC-AUC is 0.6799408767429772; stored Stage 5 raw TEST ROC-AUC is 0.6776693941139847. That gap is classified `EXPLAINED` and is not a measurement contradiction. Stored Stage 5 Platt TEST ROC-AUC equals stored raw TEST ROC-AUC. Stage 8/9 consume stored `p_selected` from the Stage 5 TRAIN-only pipeline, not Stage 4B TEST `p_hat`.

**Supported by stored evidence.** A0, A1, and A3/A4 are different decision maps on the same stored `p_selected`. A0 is credit-only two-threshold (5232 / 203627 / 27). A1 applies frozen G0 to the same credit bands; stored L2 is INSUFFICIENT_INFORMATION on all 208886 TEST rows, which routes LOW and MEDIUM to HUMAN_REVIEW and HIGH to REJECT (0 / 208859 / 27). A3/A4 remove the review branch with t*=0.16 (61855 / 0 / 147031).

**Interpretation (not a new empirical finding).** Policy-count differences are routing/governance-map differences, not a change of the credit model. The A1 review allocation is the stored evidence-gap effect (schema/governance insufficiency under G0), not a claim that governance improved or reduced discrimination. UCI LR/EBM numbers are an independent methodology-context citation; they are not a test of LC Shariah governance or LC thresholds.

## 9. Limitations

- LendingClub and UCI targets are not equivalent; rows are not merged; no AUC equality test is performed.
- UCI does not apply Shariah governance and cannot validate the LC evidence-separated architecture.
- Stage 4B LC TEST tables do not store ECE; UCI family-raw TEST tables do not store ECE for LR or EBM.
- Stage 5 calibrated LC TEST (raw/Platt/isotonic) is EBM-only. LC logistic regression has no stored Platt TEST row.
- Stage 4B final EBM joblib SHA-256 is not recorded in existing artifacts. The dump path is documented; the hash is unavailable without computing it, which this activity does not do.
- Stage 4B TRAIN+VALIDATION concatenated training-row total is not stored as a single field; TRAIN=941267 and VALIDATION=197528 are stored separately.
- S10-A4 cites stored metrics and counts only. It is not a confirmatory TEST experiment and produces no model ranking.
- git_commit is null (no usable .git / git). Recorded, not fabricated. Stage 10 protocol §14: not by itself a scientific abort.

## Missing metrics / provenance

- LendingClub logistic_regression ECE: not stored in Stage 4B TEST artifacts.
- UCI logistic_regression ECE: not stored in uci_test_family_raw.csv.
- UCI explainable_boosting_machine ECE: not stored in uci_test_family_raw.csv.
- LendingClub logistic_regression Platt/isotonic TEST: not stored (Stage 5 calibrated EBM only).
- UCI LR/EBM calibrated TEST (Platt/isotonic): not stored as family TEST rows; Stage 9.4 calibrated TEST is the exploratory selected XGBoost row.
- Stage 4B final_explainable_boosting_machine_seed42.joblib SHA-256: not recorded.
- git_commit may be null; not fabricated.

## 10. Audit classification

`PASS WITH DOCUMENTATION LIMITATION`

The activity remained analysis-only / descriptive and non-confirmatory. Authorization is `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED`. Documentation limitations are the unrecorded Stage 4B final-EBM hash, the unstored concatenated TRAIN+VALIDATION row total, missing ECE in some cited tables, and git_commit null. These do not convert the activity into an unauthorized or invalid run.

## 11. No new confirmatory experiment

No new confirmatory experiment was performed. S10-A4-SIDEBYSIDE cites existing artifacts. Favorable or unfavorable stored numbers do not create a confirmatory TEST result.

## Issues

- None.

## Provenance hashes

- Stage 5 TEST metrics SHA-256: `a6c8ab44676d62109c1a346dbcf14a12a745b761f13b9fda6a9002853fc326e3`
- Stage 4B TEST metrics SHA-256: `960c01643a671805daa1c692e9034454a94d6088651c6336076433b3e8bdc612`
- table3 SHA-256: `90759eb72f1173b40b5b9363c21b0ef3d6f1cde5042748eb57871d49fb73d5ee`
- UCI family-raw TEST SHA-256: `fdf7eeb420a763e3be45c86ac5a1140e7ad00b1426810879e8400dd600695d56`
- UCI selected TEST SHA-256: `9d2635919c7dfe0a8cc03040cffcb1cbc750db8235507e94ee2e215762000a02` (exploratory XGBoost+isotonic row)
- Recorded Stage 5 EBM joblib SHA-256: `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4`
- Recorded TEST calibrated CSV SHA-256: `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb`
- git_commit: `None`
- Source artifacts:
  - `C:/Users/User/research-project/results/calibration/metrics/stage5_test_metrics.json`
  - `C:/Users/User/research-project/results/metrics/stage4b_test_metrics.json`
  - `C:/Users/User/research-project/audit/stage4b_modeling_run.json`
  - `C:/Users/User/research-project/audit/stage5_calibration_run.json`
  - `C:/Users/User/research-project/audit/lendingclub_split_manifest.json`
  - `C:/Users/User/research-project/experiments/stage5_calibration/checkpoints/train_only_ebm_meta.json`
  - `C:/Users/User/research-project/results/calibration/artifacts/platt_record.json`
  - `C:/Users/User/research-project/results/calibration/artifacts/isotonic_record.json`
  - `C:/Users/User/research-project/experiments/stage5_calibration/selected_calibration.json`
  - `C:/Users/User/research-project/results/decision/v2/tables/table3_test_decision_outcomes.csv`
  - `C:/Users/User/research-project/audit/stage9_1_ablation_run.json`
  - `C:/Users/User/research-project/results/stage10/v1/metrics/s10_a1_gap.json`
  - `C:/Users/User/research-project/results/uci_generalization/v1/tables/uci_test_family_raw.csv`
  - `C:/Users/User/research-project/results/uci_generalization/v1/metrics/uci_test_selected.json`
  - `C:/Users/User/research-project/docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md`
  - `C:/Users/User/research-project/audit/stage9_4_uci_run.json`

