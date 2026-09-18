# Stage 8 Decision Policy Report

> **Historical preservation.** This document is **Stage 8 v1 historical evidence**. The v1 fusion used a **broadcast** LendingClub dataset profile. Stage 8 v2 per-row fusion is in `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`. Frozen thresholds and the credit model are **not** invalidated. Stage 9 remains **blocked**.

Credit risk, explainability, and Shariah-oriented governance remain independently validated evidence layers. This stage implements a transparent approve / review / reject policy and an audit record. It does not retrain the EBM, does not refit Platt scaling, and does not create a Shariah score.

**Status:** `STAGE_8_STATUS = PASS`

## Separation of claims

| Question | What this stage reports |
| --- | --- |
| Predictive | Frozen Stage 5 Platt-calibrated EBM discrimination and calibration, cited from Stage 5 artifacts and consistency-checked |
| Governance | Whether contractual evidence exists for the configured Stage 7 rules |
| Decision policy | The action recommended under explicit researcher cost and matrix assumptions |
| Auditability | Whether another researcher can reconstruct the logic hash of a decision |

These questions are not collapsed into a single accuracy number.

## Observed empirical results

- LendingClub governance profile evaluated once: completeness `INSUFFICIENT`, status `INSUFFICIENT_INFORMATION`. Real LendingClub rows were not given fabricated contract fields.
- Primary ASSUMED RELATIVE COST SCENARIO: `FN:FP=5:1` with `C_REVIEW = 0.25 * C_FP`.
- Validation-selected credit-only policy: type `two_threshold`, `t_low=0.06`, `t_high=0.69`, expected normalized cost `0.249025`.
- Frozen test fused-policy action mix: approval `0.000000`, review `0.999871`, rejection `0.000129`.
- Frozen test fused-policy default rates by action are in `results/decision/tables/table3_test_decision_outcomes.csv`.
- Credit-risk × governance contingency is in `results/decision/tables/table4_credit_governance_contingency.csv`.

### Validation threshold selection by cost scenario

| Scenario | Type | t_low | t_high | Val expected cost | Val approve | Val review | Val reject | Val FNR (pop.) | Val FPR (pop.) |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| FN:FP=1:1 | two_threshold | 0.25 | 0.69 | 0.205605 | 0.542703 | 0.457186 | 0.000111 | 0.366780 | 0.000027 |
| FN:FP=2:1 | two_threshold | 0.12 | 0.69 | 0.240082 | 0.116915 | 0.882974 | 0.000111 | 0.038810 | 0.000027 |
| FN:FP=5:1 | two_threshold | 0.06 | 0.69 | 0.249025 | 0.014803 | 0.985086 | 0.000111 | 0.002197 | 0.000027 |
| FN:FP=10:1 | two_threshold | 0.04 | 0.69 | 0.249727 | 0.002886 | 0.997003 | 0.000111 | 0.000183 | 0.000027 |

### Frozen test predictive metrics (Stage 5 Platt artifacts)

- ROC-AUC `0.677669`
- PR-AUC `0.350963`
- Brier `0.156169`
- ECE `0.020267`
- MCE `0.186947`
- Stage 8 recomputed the same functions on the frozen test prediction file; absolute gaps to the Stage 5 artifact are reported in the run audit.

### Frozen test fused policy

- n = 208886
- approval_rate = 0.000000
- review_rate = 0.999871
- rejection_rate = 0.000129
- FNR (population, auto-approved defaults / all defaults) = 0.000000
- FPR (population, auto-rejected non-defaults / all non-defaults) = 0.000079
- precision of REJECT = 0.518519
- expected normalized cost under the primary assumed scenario = 0.250030

The review band is a **simulated decision-policy band**. No human-review outcomes were collected. This stage does not claim that human reviewers improved accuracy, fairness, or Shariah status.

## Researcher policy assumptions

- Relative FN:FP costs `{1,2,5,10}` are sensitivity scenarios, not LendingClub, bank, Islamic-institution, or regulator costs.
- Review is not free: `C_REVIEW = 0.25 * C_FP` unless perturbed in Experiment G.
- Primary freeze uses FN:FP = 5:1, declared in `configs/stage8_decision_policy.yaml` before test evaluation.
- Credit-risk thresholds are selected from a **credit-only** cost objective on validation. Rationale: under LendingClub `INSUFFICIENT_INFORMATION`, LOW and MEDIUM both map to HUMAN_REVIEW, so `t_low` is not identified by fused cost.
- The governance matrix is a researcher operating procedure, not a religious ruling and not expert-validated.

## Architectural design choices

1. Governance `NOT_STRUCTURABLE_WITHOUT_REDESIGN` is a hard stop: REJECT for every credit band.
2. Unknown or missing governance is treated as `INSUFFICIENT_INFORMATION`, never as PASS.
3. APPROVE requires governance PASS and a LOW credit-risk band.
4. Explainability is attached to the audit record and is not an independent approval criterion.
5. The monolithic baseline is a single threshold on the same calibrated probability with no governance layer and no review band.

## Fairness limitation

Fairness evaluation is limited by unavailable protected attributes. Race, religion, gender, and ethnicity are not inferred from `addr_state`, `zip_code`, or `purpose`.

## Tests and reproducibility

120 passed, 2 warnings in 38.99s

- In-process threshold selection repeated twice: equivalent `True`.
- Audit logic hashes ignore event timestamps: equivalent `True`.

## Stage boundary

Stage 9 has NOT been started.

## Artifact index

- `results/figures/decision/figure1_validation_cost_curve.png`
- `results/figures/decision/figure2_cost_ratio_sensitivity.png`
- `results/figures/decision/figure3_action_mix_by_cost.png`
- `results/figures/decision/figure4_default_rate_by_band.png`
- `results/figures/decision/figure5_credit_governance_heatmap.png`
- `results/figures/decision/figure6_evidence_separated_architecture.png`
- `results/figures/decision/figure7_audit_trail_lifecycle.png`
- `results/decision/tables/table1_decision_policy_definitions.csv`
- `results/decision/tables/table2_validation_threshold_selection.csv`
- `results/decision/tables/table3_test_decision_outcomes.csv`
- `results/decision/tables/table4_credit_governance_contingency.csv`
- `results/decision/tables/table5_monolithic_vs_separated.csv`
- `results/decision/tables/table6_audit_schema.csv`
- `results/decision/frozen_policy.json`
- `results/decision/audit/test_audit_records.csv`
- `results/decision/audit/published_examples.json`
- `audit/stage8_decision_policy_run.json`
- `audit/stage8_threshold_selection.json`
- `audit/stage8_policy_config.json`
- `audit/stage8_audit_schema.json`
- `configs/stage8_decision_policy.yaml`
- `configs/stage8_decision_policy.json`
