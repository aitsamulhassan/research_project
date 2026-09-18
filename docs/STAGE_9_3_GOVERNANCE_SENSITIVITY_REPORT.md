# Stage 9.3 Governance Sensitivity Report

LendingClub TEST was already exposed during Stages 4B–8. Stage 9.3 did not use TEST data to select a governance scenario, threshold, or policy. G0 cites stored Stage 8 v2 fused counts. G1 and G3 are algebraic illustrations from already published credit-band counts. They are labeled derived commentary, not a new TEST evaluation.

**Status:** `STAGE_9_3_STATUS = PASS`

```text
STAGE_9_4+ = NOT EXECUTED
G-unsafe = NOT_EXECUTED — NOT_AUTHORIZED
```

## 1. Objective

Describe how the **decision layer** allocation would change if the governance-state input supplied to the frozen fusion policy were treated differently. This is an engineering sensitivity analysis. It is not a religious ruling, not a compliance test, and not a ranking of which state is more appropriate as a religious judgment.

## 2. Relationship to Stage 9.0 freeze

Controlling freeze: `audit/stage9_0_experimental_freeze.json`; protocol `STAGE-9-PROTOCOL-2026-09-15` §5.2.

- O-G: G0 remains primary; G1 and G3 are hypothetical engineering sensitivities.
- O-TEST Option A: no additional LC TEST policy remaps. Stage 9.3 does not rewrite Stage 8 outputs and does not apply G1/G3 as a new stored TEST policy.
- Arithmetic from already published Stage 8 v2 band counts is the authorized illustration method.
- G-unsafe (treat insufficiency as PASS) is not a candidate policy and was not executed.
- Stage 8 thresholds remain `t_low=0.06`, `t_high=0.69`. The G0 matrix is not altered in Stage 8.

## 3. Governance-state definitions

G1 and G3 change **only** the `INSUFFICIENT_INFORMATION` row of the frozen Stage 8 matrix. PASS / REVIEW / `NOT_STRUCTURABLE_WITHOUT_REDESIGN` cells remain the G0 cells.

| ID | Role | Treatment of `INSUFFICIENT_INFORMATION` |
| --- | --- | --- |
| G0 | Primary / observed | LOW → HUMAN_REVIEW; MEDIUM → HUMAN_REVIEW; HIGH → REJECT |
| G1 | Hypothetical engineering | LOW → REJECT; MEDIUM → REJECT; HIGH → REJECT |
| G3 | Hypothetical engineering | LOW → HUMAN_REVIEW; MEDIUM → HUMAN_REVIEW; HIGH → HUMAN_REVIEW |

The remainder of the frozen G0 matrix (unchanged in G1/G3) is:

| Governance status | LOW | MEDIUM | HIGH |
| --- | --- | --- | --- |
| `NOT_STRUCTURABLE_WITHOUT_REDESIGN` | REJECT | REJECT | REJECT |
| `REVIEW` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |
| `PASS` | APPROVE | HUMAN_REVIEW | REJECT |

## 4. G0 observed evidence state

LendingClub L2 on the stored Stage 8 v2 TEST fusion is `INSUFFICIENT_INFORMATION` for every application (208,886 / 208,886). That is an **observed governance evidence state**: insufficient contractual evidence for an application-level Shariah-oriented determination. It is not a religious classification of applicants.

L1 remains `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` (dataset context, not an applicant-level ruling). L2 evaluation_mode remains `PER_APPLICATION`. Stage 7 version: `stage7-l1l2-v2`.

G0 decision counts are the stored Stage 8 v2 fused result, confirmed by applying the frozen G0 `INSUFFICIENT_INFORMATION` row to the published credit-band counts.

## 5. Hypothetical G1/G3 scenarios

G1 and G3 are **hypothetical engineering scenarios**. They are not observed evidence states, not expert-validated statuses, and not evidence that a real financing application should receive those treatments. They ask only: if the frozen fusion policy treated `INSUFFICIENT_INFORMATION` as all-REJECT (G1) or all-HUMAN_REVIEW including HIGH (G3), how would the published band counts allocate?

They are not ranked. Neither is selected as a replacement for G0.

## 6. Experimental controls

- Same published sample n = 208,886.
- Same frozen credit bands: LOW 5,232; MEDIUM 203,627; HIGH 27.
- Same frozen thresholds `0.06 / 0.69`.
- Same observed L2 input `INSUFFICIENT_INFORMATION` for all rows.
- Only the authorized `INSUFFICIENT_INFORMATION` treatment differs.
- Credit model, calibration, and Stage 7 rule inventory are not called.
- Predictive metrics are not recomputed: governance sensitivity is a decision-layer analysis.
- Stage 9.2 cost analysis is not repeated and is not used to choose a scenario.

## 7. Decision-allocation results

| Scenario | Role | APPROVE | HUMAN_REVIEW | REJECT | Approval rate | Review rate | Rejection rate |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| G0 | observed / primary | 0 | 208859 | 27 | 0.0000% | 99.9871% | 0.0129% |
| G1 | hypothetical | 0 | 0 | 208886 | 0.0000% | 0.0000% | 100.0000% |
| G3 | hypothetical | 0 | 208886 | 0 | 0.0000% | 100.0000% | 0.0000% |

Band-level mapping under the observed L2 input:

| Band | n | G0 | G1 | G3 |
| --- | ---: | --- | --- | --- |
| LOW | 5232 | HUMAN_REVIEW | REJECT | HUMAN_REVIEW |
| MEDIUM | 203627 | HUMAN_REVIEW | REJECT | HUMAN_REVIEW |
| HIGH | 27 | REJECT | REJECT | HUMAN_REVIEW |

G0’s large HUMAN_REVIEW rate is preserved. It is not “fixed.”

## 8. Interpretation

This is **decision-layer sensitivity** to the treatment of evidence insufficiency, holding credit bands fixed.

- Under G0, HIGH credit risk still REJECT (27 applications); LOW and MEDIUM go to HUMAN_REVIEW because contractual evidence is insufficient.
- Under hypothetical G1, the same insufficiency treatment sends every published band to REJECT, so review rate is 0 and rejection rate is 1.
- Under hypothetical G3, even HIGH is held in HUMAN_REVIEW, so rejection rate is 0 and review rate is 1.
- None of these allocations is a statement about economic optimality. Stage 9.2 is not reused to pick a winner.

A governance layer that refuses to infer contractual status from generic credit/application data can substantially constrain automated decisions when contractual evidence is absent. That is an evidence-gap property of the observed schema, not a demonstration that the architecture is economically superior.

## 9. Shariah-interpretation boundary

This experiment does **not** produce a religious score, religious probability, religious ranking, or religious accuracy. It does not classify purpose, FICO, or demographics as contractual evidence. It does not claim that G0, G1, or G3 is the religiously correct treatment. Expert validation remains `NONE_EXPERT_VALIDATED`. `certification_claim=false`.

G1 must not be read as “these applications are non-compliant.” G3 must not be read as “these applications should be approved after review as compliant.” Both are engineering counterfactuals about how a frozen matrix cell could be filled.

## 10. Limitations

- G1/G3 are not observed L2 statuses on LendingClub.
- No reviewer outcomes exist; HUMAN_REVIEW is a simulated policy band.
- Algebra from published band counts does not create new per-row TEST audit records (O-TEST Option A).
- The analysis cannot say which scenario a bank or board should adopt.

## 11. Leakage / selection statement

LendingClub TEST was already exposed during Stages 4B–8. Stage 9.3 did not use TEST outcomes to choose G0, G1, or G3. No threshold was searched. No scenario was selected as best. G0 remains the pre-declared primary from Stage 8 / Stage 9.0.

## 12. Reproducibility

- experiment_id: `stage9_3_governance_sensitivity_lc_v1`
- protocol: `STAGE-9-PROTOCOL-2026-09-15` §5.2
- Stage 7 governance version: `stage7-l1l2-v2`
- Stage 8 v1 freeze sha256: `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4`
- config: `configs/stage9_3_governance_sensitivity.yaml`
- script: `experiments/stage9_3_governance_sensitivity/run_stage9_3.py`
- execution_timestamp: `2026-09-15T18:22:35+00:00`
- git_commit: `None`
- expert_validation: `NONE_EXPERT_VALIDATED`
- certification_claim: `False`
- test command: `python -m pytest tests/test_stage9_3_governance_sensitivity.py -q --tb=short`
- test summary: `13 passed in 1.16s`

## 13. Conclusion

G0 remains the only observed, data-supported governance evidence state on this LendingClub extract: `INSUFFICIENT_INFORMATION`, producing a near-universal HUMAN_REVIEW allocation under the frozen matrix. Hypothetical G1 collapses that allocation to all REJECT; hypothetical G3 collapses it to all HUMAN_REVIEW. Those are engineering sensitivities to one matrix row. They are not religious findings. Stage 9.4+ were not executed.

## Artifact index

- `docs/STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md`
- `audit/stage9_3_governance_sensitivity_run.json`
- `results/governance_sensitivity/v1/stage9_3_governance_sensitivity.yaml`
- `results/governance_sensitivity/v1/tables/table1_governance_scenario_allocation.csv`
- `results/governance_sensitivity/v1/tables/table2_band_mapping_by_scenario.csv`
- `results/governance_sensitivity/v1/metrics/governance_sensitivity_summary.json`
- `results/figures/governance_sensitivity/v1/figure1_decision_counts.png`
- `results/figures/governance_sensitivity/v1/figure2_decision_rates.png`
