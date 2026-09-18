# Stage 9.4 UCI Independent Generalization Report

> **Provenance caveat:** The Stage 9.4 XGBoost result was an execution-time
> model-scope expansion beyond the approved Logistic Regression + EBM scope.
> It is retained as an exploratory extension and is not treated as a
> pre-registered/confirmatory outcome. See `DEVIATION-001-stage9-authorization-gap.md`,
> subsection **Stage 9.4 — Model-scope expansion**.

**Experiment ID:** `stage9_4_uci_generalization_v1`  
**Amendment:** `AMENDMENT-STAGE9-4-AUTHORIZATION` status `APPROVED` (approval date 2026-09-15)  
**Status:** `PASS`

## Purpose

This experiment tests whether the credit-risk / calibration METHODOLOGY generalizes to a second, independent, public credit dataset. It is NOT a test of the evidence-separated decision architecture as a whole, and it does NOT include a Shariah governance layer, because UCI structurally lacks contract-level fields (already established in the Stage 2 audit).

Do not overclaim: UCI results do not validate or invalidate the LendingClub architecture as a whole.

## A. Frozen UCI split

Verified existing Stage 3 artifacts. A new split was **not** created.

| Split | Rows | Positives | Prevalence |
| --- | ---: | ---: | ---: |
| train | 20999 | 4645 | 0.221201 |
| validation | 4499 | 995 | 0.221160 |
| test | 4502 | 996 | 0.221235 |

- Raw UCI SHA-256: `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602`
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

Primary criterion is mean UCI validation PR-AUC. Best PR-AUC is 0.534172. Candidates within 0.005: ['xgboost']. Among those, lowest mean Brier then simplicity selected `xgboost` (PR-AUC=0.534172, Brier=0.178710).

Validation seed metrics:

| family | seed | roc_auc | pr_auc | brier | log_loss |
| --- | --- | --- | --- | --- | --- |
| logistic_regression | 42 | 0.763567 | 0.520869 | 0.183702 | 0.562443 |
| logistic_regression | 123 | 0.763567 | 0.520869 | 0.183702 | 0.562443 |
| logistic_regression | 2024 | 0.763567 | 0.520869 | 0.183702 | 0.562443 |
| logistic_regression | 3407 | 0.763567 | 0.520869 | 0.183702 | 0.562443 |
| logistic_regression | 9999 | 0.763567 | 0.520869 | 0.183702 | 0.562443 |
| explainable_boosting_machine | 42 | 0.774234 | 0.527971 | 0.138019 | 0.437807 |
| explainable_boosting_machine | 123 | 0.774468 | 0.528029 | 0.138078 | 0.437838 |
| explainable_boosting_machine | 2024 | 0.774147 | 0.527150 | 0.138151 | 0.438019 |
| explainable_boosting_machine | 3407 | 0.774636 | 0.528353 | 0.138016 | 0.437609 |
| explainable_boosting_machine | 9999 | 0.774267 | 0.526924 | 0.138106 | 0.437934 |
| xgboost | 42 | 0.776028 | 0.534172 | 0.178710 | 0.543870 |
| xgboost | 123 | 0.776028 | 0.534172 | 0.178710 | 0.543870 |
| xgboost | 2024 | 0.776028 | 0.534172 | 0.178710 | 0.543870 |
| xgboost | 3407 | 0.776028 | 0.534172 | 0.178710 | 0.543870 |
| xgboost | 9999 | 0.776028 | 0.534172 | 0.178710 | 0.543870 |

Seed aggregates (selection input):

| family | pr_auc_mean | pr_auc_sd | brier_mean | roc_auc_mean |
| --- | --- | --- | --- | --- |
| logistic_regression | 0.520869 | 0.000000 | 0.183702 | 0.763567 |
| explainable_boosting_machine | 0.527686 | 0.000615 | 0.138074 | 0.774351 |
| xgboost | 0.534172 | 0.000000 | 0.178710 | 0.776028 |

## D. Calibration

Raw vs Platt vs isotonic, fit on **UCI validation only** for the selected family (seed 42, train-only model). Stage 5 rule: validation Brier, 0.001 practical tie preferring simpler methods (`raw` > `platt` > `isotonic`). LendingClub Platt `a,b` were not reused.

Primary criterion is UCI validation Brier. Best Brier=0.134862. Methods within 0.001 (practically indistinguishable): ['isotonic']. Among those, simplicity order ['raw', 'platt', 'isotonic'] selected `isotonic` (Brier=0.134862, log_loss=0.428378, ECE=0.000000).

Validation calibration:

| method | brier | log_loss | ece | roc_auc | pr_auc |
| --- | --- | --- | --- | --- | --- |
| raw | 0.178710 | 0.543870 | 0.195387 | 0.776028 | 0.534172 |
| platt | 0.136998 | 0.434463 | 0.018891 | 0.776028 | 0.534172 |
| isotonic | 0.134862 | 0.428378 | 0.000000 | 0.780610 | 0.524953 |

## E. UCI TEST metrics (once, after freeze)

Selected family `xgboost`, selected calibrator `isotonic`. `test_used_for_selection = false`.

| method | roc_auc | pr_auc | brier | log_loss | ece |
| --- | --- | --- | --- | --- | --- |
| raw | 0.773351 | 0.545664 | 0.181736 | 0.551860 | 0.200657 |
| platt | 0.773351 | 0.545664 | 0.136406 | 0.435551 | 0.019547 |
| isotonic | 0.770878 | 0.522421 | 0.136853 | 0.449533 | 0.017443 |

Bootstrap: 1000 row resamples, percentile 95% CI, seed 42. Not used for selection.

Selected UCI TEST (with CI):

| Metric | Point | 95% CI |
| --- | ---: | --- |
| ROC-AUC | 0.770878 | [0.753054, 0.787670] |
| PR-AUC | 0.522421 | [0.489710, 0.553604] |
| Brier | 0.136853 | [0.131053, 0.143440] |
| Log loss | 0.449533 | [0.426559, 0.475760] |
| ECE | 0.017443 | [0.011304, 0.029490] |

Raw TEST metrics for all three families (reported after freeze; not used to choose the family):

| family | roc_auc | pr_auc | brier | log_loss |
| --- | --- | --- | --- | --- |
| logistic_regression | 0.757278 | 0.525511 | 0.187096 | 0.570735 |
| explainable_boosting_machine | 0.768856 | 0.537376 | 0.137432 | 0.438423 |
| xgboost | 0.773351 | 0.545664 | 0.181736 | 0.551860 |

## F. Alongside frozen LendingClub TEST (not merged)

LendingClub numbers are **cited** from `results/calibration/metrics/stage5_test_metrics.json` (Platt, selected EBM, LC TEST). They were not recomputed.

| Metric | UCI TEST (`xgboost` / `isotonic`) | LC TEST (EBM / Platt, cited) | Plain comparison |
| --- | ---: | ---: | --- |
| n | 4502.0 | 208886 | separate samples |
| ROC-AUC | 0.770878 | 0.677669 | better |
| PR-AUC | 0.522421 | 0.350963 | better |
| Brier | 0.136853 | 0.156169 | better |
| Log loss | 0.449533 | 0.483570 | better |
| ECE | 0.017443 | 0.020267 | better |

A worse UCI number is a valid finding, not something to hide. A better UCI number does **not** mean the LendingClub pipeline is inferior: prevalence, features, and labels differ.

## G. Explainability (Tier 2)

EBM native additive term attributions on UCI **train** (logit/link scale). Associations, not causes.

| rank | feature | mean_abs | mean_signed |
| --- | --- | --- | --- |
| 1 | PAY_0 | 0.477839 | -0.000000 |
| 2 | LIMIT_BAL | 0.167350 | 0.000000 |
| 3 | PAY_AMT2 | 0.122763 | -0.000000 |
| 4 | BILL_AMT1 | 0.117968 | 0.000000 |
| 5 | PAY_AMT1 | 0.112329 | 0.000000 |
| 6 | PAY_3 | 0.103556 | 0.000000 |
| 7 | MARRIAGE | 0.095106 | 0.000000 |
| 8 | PAY_6 | 0.081458 | -0.000000 |
| 9 | PAY_2 | 0.077539 | -0.000000 |
| 10 | PAY_AMT4 | 0.075613 | 0.000000 |
| 11 | PAY_AMT3 | 0.073822 | -0.000000 |
| 12 | PAY_AMT6 | 0.062260 | -0.000000 |
| 13 | BILL_AMT3 | 0.056917 | -0.000000 |
| 14 | BILL_AMT4 | 0.055049 | -0.000000 |
| 15 | PAY_4 | 0.052958 | 0.000000 |
| 16 | PAY_AMT5 | 0.047364 | -0.000000 |
| 17 | BILL_AMT2 | 0.047034 | 0.000000 |
| 18 | PAY_5 | 0.043471 | -0.000000 |
| 19 | SEX | 0.035288 | -0.000000 |
| 20 | EDUCATION | 0.027808 | 0.000000 |
| 21 | BILL_AMT6 | 0.026960 | -0.000000 |
| 22 | BILL_AMT5 | 0.021458 | -0.000000 |
| 23 | AGE | 0.015297 | -0.000000 |

SHAP-vs-EBM fidelity: **skipped**. SHAP-vs-EBM fidelity is optional in the Stage 9.4 instruction. It was skipped rather than run superficially. Native EBM attributions are the Tier-2 deliverable.

## H. Explicit non-claims

- No Shariah governance evaluation was performed on UCI.
- UCI Default of Credit Card Clients lacks contract-type, counterparty, and Islamic-finance fields required for applicant-level Shariah determination. Stage 9.4 L1 is dataset-metadata only; no L2 fusion and no per-row Shariah rulings were performed.
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
