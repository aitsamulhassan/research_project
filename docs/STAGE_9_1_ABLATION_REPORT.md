# Stage 9.1 Ablation / Comparator Report

LendingClub TEST was already exposed during Stages 4B–8. Stage 9.1 did not use TEST data for model or policy selection. The analysis is a controlled ablation/re-analysis of frozen artifacts and previously exposed TEST outputs.

**Status:** `STAGE_9_1_STATUS = PASS`

```text
STAGE_9_2+ = NOT EXECUTED
STAGE_9_EXECUTION = AUTHORIZED FOR STAGE 9.1 ONLY
```

## 1. Objective

Compare the frozen evidence-separated decision architecture (A1) with the frozen credit-only three-way policy (A0) and the frozen binary monolithic comparator (A3/A4), without retraining, without threshold search, and without changing Stage 8.

## 2. Research question linkage

> Does separating credit-risk scoring, explainability, and Shariah-oriented governance into independently validated and auditable evidence layers, fused only at the final decision stage, provide a more transparent and defensible digital-financing pipeline than a monolithic end-to-end classifier without materially sacrificing predictive performance?

The monolithic comparator is the Stage 8 single-threshold credit policy (`t*=0.16`) on the same frozen Platt-calibrated EBM. It is not a neural Shariah classifier. Predictive scores are identical across A0/A1/A3; only the decision map changes.

## 3. Exact definitions

| ID | Definition | HUMAN_REVIEW | Governance | Role |
| --- | --- | --- | --- | --- |
| A0 | `p_selected < 0.06` APPROVE; `0.06 <= p < 0.69` HUMAN_REVIEW; `p >= 0.69` REJECT | Yes (credit MEDIUM) | None | Credit-only ablation |
| A1 | Same credit bands, fused with Stage 7 v2 L2 under G0 | Yes (credit and/or governance) | G0 primary | **Proposed architecture** |
| A3 | `p_selected < 0.16` APPROVE; `p_selected >= 0.16` REJECT | No | None | Binary comparator/ablation |
| A4 | Same as A3 under the Stage 9.0 freeze | No | None | Collapses to A3 |

A3 and A4 collapse to the same frozen binary monolithic credit-policy comparator under the Stage 9.0 freeze. They are reported once.

## 4. Frozen artifacts used

- Stage 8 v1 freeze: `results/decision/frozen_policy.json` sha256 `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4`
- Stage 8 v2 table: `results/decision/v2/tables/table3_test_decision_outcomes.csv`
- t_low=0.06, t_high=0.69, t*=0.16
- Platt a=1.1988263209549705, b=0.6697765046966161
- EBM joblib sha256 `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4` (not loaded for scoring)

## 5. Data/split provenance

- Dataset: LendingClub granting extract, split = TEST (`issue_month >= 2017-02`), n = 208,886.
- Probabilities: stored `p_selected` from Stage 5 Platt, seed 42.
- Labels: stored `y_true` already used in Stage 8 policy tables; not used here for selection.

## 6. TEST protection statement

LendingClub TEST was already exposed during Stages 4B–8. Stage 9.1 did not use TEST data for model or policy selection. The analysis is a controlled ablation/re-analysis of frozen artifacts and previously exposed TEST outputs.

Consistency check (A0/A3 maps re-applied to stored `p_selected`): `descriptive_reanalysis_of_previously_exposed_test_outputs`; used_for_selection=`False`; a0_match=`True`; a3_match=`True`.

## 7. Decision-policy definitions

A1 retains HUMAN_REVIEW. G0 maps L2 `INSUFFICIENT_INFORMATION` + LOW/MEDIUM → HUMAN_REVIEW and HIGH → REJECT. No Shariah score is created. Governance outputs are not fed into the credit model.

## 8. Results

A1 counts are the Stage 8 v2 fused TEST result, confirmed against the stored table. They are not a newly discovered TEST result.

| System | Credit policy | Governance | APPROVE | HUMAN_REVIEW | REJECT | Review burden | Notes |
| --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| A0 | frozen three-way 0.06/0.69 | none | 5232 (2.5047%) | 203627 (97.4824%) | 27 (0.0129%) | 97.4824% | credit-only |
| A1 | frozen three-way 0.06/0.69 | G0 | 0 (0.0000%) | 208859 (99.9871%) | 27 (0.0129%) | 99.9871% | proposed architecture |
| A3/A4 | `t*=0.16` binary | none | 61855 (29.6118%) | 0 (0.0000%) | 147031 (70.3882%) | 0.0000% | monolithic comparator |

n = 208886.

### A1 credit-risk bands (same frozen thresholds as A0)

| Band | n | default_rate | Wilson 95% CI |
| --- | ---: | ---: | --- |
| LOW | 5232 | 0.037462 | [0.032646, 0.042956] |
| MEDIUM | 203627 | 0.216229 | [0.214446, 0.218022] |
| HIGH | 27 | 0.518519 | [0.339853, 0.692570] |

### Default rate by decision (stored TEST labels, evaluation only)

| System | Decision | n | n_default | default_rate |
| --- | --- | ---: | ---: | ---: |
| A0 | APPROVE | 5232 | 196 | 0.037462 |
| A0 | HUMAN_REVIEW | 203627 | 44030 | 0.216229 |
| A0 | REJECT | 27 | 14 | 0.518519 |
| A1 | APPROVE | 0 | 0 | NA |
| A1 | HUMAN_REVIEW | 208859 | 44226 | 0.211751 |
| A1 | REJECT | 27 | 14 | 0.518519 |
| A3/A4 | APPROVE | 61855 | 5980 | 0.096678 |
| A3/A4 | REJECT | 147031 | 38260 | 0.260217 |

A1 L2 governance-status counts: `{'INSUFFICIENT_INFORMATION': 208886}`.

These default rates describe the already-exposed TEST split under frozen policies. They are not causal effects and are not used to choose a policy.

A1 APPROVE is listed with n=0 because the stored Stage 8 v2 fused output has `n_approve=0`; it is not a new TEST finding.

## 9. Predictive vs policy metrics

A0, A1, and A3/A4 consume the same frozen `p_selected`. They therefore share the Stage 5 Platt TEST predictive metrics:

- ROC-AUC `0.677669` 95% CI `[0.674956, 0.680502]`
- PR-AUC `0.350963`
- Brier `0.156169`
- log loss `0.483570`
- ECE `0.020267`

A1 does not change EBM discrimination or calibration. Differences below are **policy allocation** differences.

## 10. Governance interpretation

LendingClub L2 status is `INSUFFICIENT_INFORMATION` for every stored TEST row. That means **insufficient contractual evidence for an application-level Shariah-oriented determination**. It does not mean applicants are Shariah compliant, non-compliant, halal, or haram. The engine did not classify Shariah compliance. L1 remains dataset context (`INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`), not 208,886 rulings.

## 11. Limitations

- TEST was previously unblinded; Stage 9.1 is not a new holdout confirmation.
- No human-review outcomes exist; review burden is a simulated policy band.
- Cost comparisons are not authorized in Stage 9.1.
- A3/A4 is not an end-to-end Shariah model.

## 12. Reproducibility

- experiment_id: `stage9_1_ablation_lc_v1`
- config: `configs/stage9_1_ablation.yaml`
- script: `experiments/stage9_1_ablation/run_stage9_1.py`
- execution_timestamp: `2026-09-15T16:50:11+00:00`
- git_commit: `None`
- consistency test_cal_sha256: `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb`
- test command: `python -m pytest tests/test_stage9_1_ablation.py -q --tb=short`
- test summary: `9 passed in 0.54s`

## 13. Negative / unexpected results

- A1 assigns 208,859 / 208,886 applications to HUMAN_REVIEW because L2 evidence is insufficient and LOW/MEDIUM map to review under G0. That is preserved, not softened.
- A1 APPROVE count is 0. Automatic approval requires L2 `PASS`, which LendingClub rows do not receive.
- A3/A4 approves 61,855 applications and has no review band, so the decision mix is not comparable as “better accuracy.”
- Default rate among A3 APPROVE (0.096678) is higher than among A0 APPROVE (LOW band, 0.037462), as expected from a looser single threshold. This is not used to rank policies in Stage 9.1.

## 14. Paper-safe interpretation

The evidence-separated architecture produces a substantially different decision allocation because it introduces an explicit human-review state and incorporates the governance evidence state at the final decision layer. It does not improve ROC-AUC/Brier relative to A3/A4, because the credit scores are the same frozen scores. Stage 9.1 does not claim that A1 is economically superior, religiously correct, or more accurate as a default classifier.

## 15. Later stages

Stage 9.2 cost sensitivity, Stage 9.3 governance sensitivity, Stage 9.4 temporal analysis, Stage 9.5 UCI, Stage 9.6 clean-room reproduction, and paper writing were **not** executed.

## Artifact index

- `docs/STAGE_9_1_ABLATION_REPORT.md`
- `audit/stage9_1_ablation_run.json`
- `results/ablation/v1/stage9_1_ablation.yaml`
- `results/ablation/v1/tables/table1_ablation_comparison.csv`
- `results/ablation/v1/tables/table2_default_rate_by_decision.csv`
- `results/ablation/v1/tables/table2b_a1_default_rate_by_credit_band.csv`
- `results/ablation/v1/tables/table3_predictive_metrics_shared.csv`
- `results/ablation/v1/metrics/ablation_summary.json`
- `results/figures/ablation/v1/figure1_decision_counts.png`
- `results/figures/ablation/v1/figure2_a1_default_by_credit_band.png`
- `results/figures/ablation/v1/figure3_a1_vs_a3_policy_rates.png`
