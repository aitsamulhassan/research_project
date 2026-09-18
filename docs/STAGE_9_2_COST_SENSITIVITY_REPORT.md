# Stage 9.2 Cost Sensitivity Report

LendingClub TEST was already exposed during Stages 4B–8. Stage 9.2 did not use TEST data for model or policy selection. The analysis scores already-frozen Stage 8 v2 decision/outcome counts under alternative relative FN:FP assumptions. Decisions are not changed.

**Status:** `STAGE_9_2_STATUS = PASS`

```text
STAGE_9_3+ = NOT EXECUTED
EXPERIMENT_G = NOT_EXECUTED — CITE_ONLY_PER_STAGE_9_0_FREEZE
```

## 1. Objective

Determine how the already-frozen A0 / A1 / A3–A4 decision outputs behave under different explicit relative error-cost assumptions. This is a policy-analysis experiment, not model training, and not a new threshold search.

## 2. Relationship to Stage 9.0 freeze

The Stage 9.0 design freeze is controlling (`audit/stage9_0_experimental_freeze.json`). There is no file named `docs/STAGE_9_0_DESIGN_FREEZE_REPORT.md`; the freeze artifact used is that JSON plus `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` §0 and §5.1.

- Frozen thresholds remain `t_low=0.06`, `t_high=0.69`, `t*=0.16`.
- G0 remains the A1 governance treatment.
- Cost set remains `r ∈ {1, 2, 5, 10}` labeled `FN:FP=r:1` with `C_FP=1`.
- O-TEST Option A: no additional LC TEST policy remaps. Stage 9.2 does not remap decisions.
- Protocol §5.1 already-executed validation threshold table is cited, not rerun.
- Experiment G is cited from its existing validation CSV and is not rerun.

The Stage 9.2 authorization listed FN:FP as `1:1, 1:2, 1:5, 1:10`. The freeze and Stage 8 `table2` use `FN:FP = r:1` with `r ∈ {1,2,5,10}` (`C_FN = r`, `C_FP = 1`). **The freeze notation is used.** The inverted reading `C_FN:C_FP = 1:2` was not implemented.

## 3. Data / artifacts used

- Dataset: LendingClub granting extract, split = TEST (`issue_month >= 2017-02`), n = 208,886.
- Source confusion: `results/decision/v2/tables/table3_test_decision_outcomes.csv`.
- Stage 8 v1 freeze sha256 `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4`.
- Stage 9.1 identity of A3/A4: identical binary comparator; reported once.
- Predictive metrics are the frozen Stage 5 Platt TEST metrics; they are not recomputed here.

## 4. Cost definition

The cost ratios are analytical assumptions rather than observed monetary costs.

```text
C_FP = 1
C_FN = r * C_FP
C_REVIEW = 0.25 * C_FP   for A0 and A1 (three-way / fused)
C_REVIEW = 0             for A3/A4 (binary; n_review = 0)
Cost_total = C_FN * FN + C_FP * FP + C_REVIEW * n_review
Cost_normalized = Cost_total / n
```

This is the Stage 8 formula (`docs/decision_cost_assumptions.md`; `src/decision/cost_policy.py`). `FN` is auto-approved defaults. `FP` is auto-rejected non-defaults. Reviewed applications are excluded from TP/TN/FP/FN and incur `C_REVIEW`. No currency unit is assigned.

The FN+FP-only component `C_FN*FN + C_FP*FP` is also stored so the two-term form is visible. It is not used as a replacement for the frozen three-term formula.

## 5. Cost ratios

| Label | C_FN | C_FP | Role |
| --- | ---: | ---: | --- |
| FN:FP=1:1 | 1 | 1 | sensitivity |
| FN:FP=2:1 | 2 | 1 | sensitivity |
| FN:FP=5:1 | 5 | 1 | primary frozen scenario |
| FN:FP=10:1 | 10 | 1 | sensitivity |

No ratio is selected as universally correct. TEST is not used to pick a ratio.

## 6. Policies evaluated

| System | Frozen policy | HUMAN_REVIEW | Governance | Role |
| --- | --- | --- | --- | --- |
| A0 | `t_low=0.06`, `t_high=0.69` credit-only | Yes (MEDIUM) | none | credit-only ablation |
| A1 | same bands + G0 fusion | Yes | G0 / L2 `INSUFFICIENT_INFORMATION` | proposed architecture |
| A3/A4 | `t*=0.16` binary | No | none | monolithic comparator; identical under the freeze |

A1 retains HUMAN_REVIEW. HUMAN_REVIEW represents an evidence-handling state under the frozen governance policy, not a Shariah ruling. L2 `INSUFFICIENT_INFORMATION` means insufficient contractual evidence for an application-level Shariah-oriented determination.

same predictions → same decisions → different assumed cost functions → different reported cost values.

## 7. Results

### 7.1 Frozen decision allocation (unchanged across cost ratios)

| System | n | APPROVE | HUMAN_REVIEW | REJECT | TP | TN | FP | FN | FPR (pop.) | FNR (pop.) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A0 | 208886 | 5232 | 203627 | 27 | 14 | 5036 | 13 | 196 | 0.000079 | 0.004430 |
| A1 | 208886 | 0 | 208859 | 27 | 14 | 0 | 13 | 0 | 0.000079 | 0.000000 |
| A3/A4 | 208886 | 61855 | 0 | 147031 | 38260 | 55875 | 108771 | 5980 | 0.660636 | 0.135172 |

FPR/FNR are decision-policy error rates of the frozen maps. They do not change when the cost function changes.

### 7.2 Relative cost of the same frozen TEST decisions

| System | FN:FP | C_FN | C_FP | C_REVIEW | cost_total | cost_normalized | FN+FP component | review component |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A0 | FN:FP=1:1 | 1.0 | 1.0 | 0.250000 | 51115.75 | 0.244706 | 209.00 | 50906.75 |
| A0 | FN:FP=2:1 | 2.0 | 1.0 | 0.250000 | 51311.75 | 0.245645 | 405.00 | 50906.75 |
| A0 | FN:FP=5:1 | 5.0 | 1.0 | 0.250000 | 51899.75 | 0.248460 | 993.00 | 50906.75 |
| A0 | FN:FP=10:1 | 10.0 | 1.0 | 0.250000 | 52879.75 | 0.253151 | 1973.00 | 50906.75 |
| A1 | FN:FP=1:1 | 1.0 | 1.0 | 0.250000 | 52227.75 | 0.250030 | 13.00 | 52214.75 |
| A1 | FN:FP=2:1 | 2.0 | 1.0 | 0.250000 | 52227.75 | 0.250030 | 13.00 | 52214.75 |
| A1 | FN:FP=5:1 | 5.0 | 1.0 | 0.250000 | 52227.75 | 0.250030 | 13.00 | 52214.75 |
| A1 | FN:FP=10:1 | 10.0 | 1.0 | 0.250000 | 52227.75 | 0.250030 | 13.00 | 52214.75 |
| A3/A4 | FN:FP=1:1 | 1.0 | 1.0 | 0.000000 | 114751.00 | 0.549347 | 114751.00 | 0.00 |
| A3/A4 | FN:FP=2:1 | 2.0 | 1.0 | 0.000000 | 120731.00 | 0.577976 | 120731.00 | 0.00 |
| A3/A4 | FN:FP=5:1 | 5.0 | 1.0 | 0.000000 | 138671.00 | 0.663860 | 138671.00 | 0.00 |
| A3/A4 | FN:FP=10:1 | 10.0 | 1.0 | 0.000000 | 168571.00 | 0.807000 | 168571.00 | 0.00 |

FN:FP=5:1 normalized costs reproduce the stored Stage 8 v2 `expected_normalized_cost` values (A0 0.248460; A1 0.250030; A3/A4 0.663860).

### 7.3 Predictive metrics (unchanged; not a cost result)

A0, A1, and A3/A4 share the frozen Stage 5 Platt TEST scores. Stage 9.2 does not alter ROC-AUC, PR-AUC, Brier, log loss, or ECE. Those remain the Stage 9.1 / Stage 5 citation.

## 8. Interpretation

Cost sensitivity evaluates the consequences of alternative relative error-cost assumptions; it does not establish real-world profitability or economic optimality.

- A1 has `FN=0` because APPROVE=0. Its total relative cost is therefore invariant to the FN:FP ratio and is almost entirely `C_REVIEW * n_review`.
- A0 has 196 auto-approved defaults, so its cost rises slowly as `r` increases; review still dominates.
- A3/A4 has no review band. Its cost is `C_FN*FN + C_FP*FP` and is much more sensitive to `r` because both FN (5,980) and FP (108,771) are large.
- Lower A1 cost than A3/A4 under these assumptions is not evidence that A1 is economically superior. It reflects sending almost every application to simulated review at `C_REVIEW=0.25`.

HUMAN_REVIEW represents an evidence-handling state under the frozen governance policy, not a Shariah ruling.

## 9. Sensitivity analysis

### 9.1 Fixed-policy FN:FP sensitivity (this Stage 9.2 primary result)

The table in §7.2 is the authorized analysis: frozen TEST decisions, four assumed ratios, Stage 8 cost formula.

### 9.2 Already-executed validation threshold identification (cited, not rerun)

Stage 8 already selected different `t_low/t_high` and `t*` on **validation** for each ratio. That is a different scientific object (new policies), not the Stage 9.2 primary analysis. It is cited only:

| FN:FP | val t_low | val t_high | val single t* | val two-threshold cost |
| --- | ---: | ---: | ---: | ---: |
| FN:FP=1:1 | 0.25 | 0.69 | 0.53 | 0.205605 |
| FN:FP=2:1 | 0.12 | 0.69 | 0.33 | 0.240082 |
| FN:FP=5:1 | 0.06 | 0.69 | 0.16 | 0.249025 |
| FN:FP=10:1 | 0.04 | 0.69 | 0.10 | 0.249727 |

Source: `C:/Users/User/research-project/results/decision/tables/table2_validation_threshold_selection.csv` sha256 `797b96255c65663641fab75b98456fd6a7c673d3954b4940bca631b94f030c45`. These thresholds were **not** applied to TEST in Stage 9.2.

### 9.3 Experiment G (cited, not executed)

Status: `NOT_EXECUTED — CITE_ONLY_PER_STAGE_9_0_FREEZE`.

Definition reproduced from the protocol: validation-only, c_review_over_fp in {0.10, 0.25, 0.50} under FN:FP=5:1 (results/decision/tables/experiment_g_review_cost_perturbation.csv). Stage 9 cites this. Do not promote G's t_low/t_high into Stage 8.

Stage 9.0 freeze instructs Stage 9 to cite the existing validation Experiment G table and not rerun it, and not to promote G's t_low/t_high into Stage 8. Re-running G would re-select thresholds (new APPROVE/REVIEW/REJECT maps). Stage 9.2 primary analysis keeps frozen decisions fixed. LC TEST was not used for G.

| c_review_over_fp | val t_low | val t_high | val normalized cost | val review rate |
| ---: | ---: | ---: | ---: | ---: |
| 0.10 | 0.04 | 0.77 | 0.099939 | 0.997114 |
| 0.25 | 0.06 | 0.69 | 0.249025 | 0.985086 |
| 0.50 | 0.10 | 0.53 | 0.487192 | 0.915364 |

Source: `C:/Users/User/research-project/results/decision/tables/experiment_g_review_cost_perturbation.csv` sha256 `98c673e98732f21d0863eb4737bbab5744a5859937f624dc229e6853fd535bb3`. G's `t_low/t_high` are not promoted into Stage 8.

## 10. Limitations

- Costs are researcher assumptions, not bank, regulator, or Shariah-board costs.
- No dollar amounts, LGD, recovery, or profit model is used or claimed.
- HUMAN_REVIEW has no observed reviewer outcome; `C_REVIEW` is not a staffing model.
- TEST was previously unblinded; this is not a new holdout confirmation.
- A1's near-universal review is an evidence-availability result (`INSUFFICIENT_INFORMATION`), not a religious classification.

## 11. Test / selection leakage statement

LendingClub TEST was already exposed during Stages 4B–8. Stage 9.2 did not use TEST data for model or policy selection. No threshold was searched. No cost ratio was chosen using TEST. FN:FP=5:1 remains the pre-declared primary scenario from Stage 8. The analysis is a controlled re-scoring of frozen confusion counts.

## 12. Reproducibility

- experiment_id: `stage9_2_cost_sensitivity_lc_v1`
- config: `configs/stage9_2_cost_sensitivity.yaml`
- script: `experiments/stage9_2_cost_sensitivity/run_stage9_2.py`
- execution_timestamp: `2026-09-15T18:08:42+00:00`
- git_commit: `None`
- test command: `python -m pytest tests/test_stage9_2_cost_sensitivity.py -q --tb=short`
- test summary: `10 passed in 0.78s`
- Stage 8 freeze sha256: `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4`

## 13. Conclusion

The cost ratios are analytical assumptions rather than observed monetary costs. Cost sensitivity evaluates the consequences of alternative relative error-cost assumptions; it does not establish real-world profitability or economic optimality. Under the frozen Stage 8 maps, changing FN:FP reweights the same FP/FN/review counts. A1 does not become a binary policy, does not lose HUMAN_REVIEW, and does not acquire a Shariah score. Stage 9.3+ were not executed.

## Artifact index

- `docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md`
- `audit/stage9_2_cost_sensitivity_run.json`
- `results/cost_sensitivity/v1/stage9_2_cost_sensitivity.yaml`
- `results/cost_sensitivity/v1/tables/table1_frozen_confusion.csv`
- `results/cost_sensitivity/v1/tables/table2_cost_by_policy_and_ratio.csv`
- `results/cost_sensitivity/v1/tables/table3_cited_validation_threshold_selection.csv`
- `results/cost_sensitivity/v1/tables/table4_cited_experiment_g.csv`
- `results/cost_sensitivity/v1/metrics/cost_sensitivity_summary.json`
- `results/figures/cost_sensitivity/v1/figure1_normalized_cost_vs_fnfp.png`
- `results/figures/cost_sensitivity/v1/figure2_cost_decomposition_fnfp5.png`
