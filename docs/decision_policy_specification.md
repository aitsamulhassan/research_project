# Decision-policy specification (Stage 8)

> Stage 8 v2 reuses this matrix and these credit-band definitions without re-selecting thresholds. Per-row fusion/audit is documented in `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`. This specification is not rewritten.

This document is the formal operating procedure for Stage 8. It is **not** a religious ruling, **not** a Shariah Board decision, and **not** a claim of certification.

Policy version: `stage8-v1`  
Audit schema version: `1.0`  
Configuration: `configs/stage8_decision_policy.yaml`

## Evidence layers

The policy consumes three independently produced evidence objects:

1. **Credit-risk evidence:** frozen Platt-calibrated default probability `p_selected` from Stage 5. The EBM and calibrator are not refit.
2. **Shariah-oriented governance evidence:** Stage 7 engine outputs. Completeness is `COMPLETE | PARTIAL | INSUFFICIENT`. Overall status is `PASS | REVIEW | NOT_STRUCTURABLE_WITHOUT_REDESIGN | INSUFFICIENT_INFORMATION`. These labels are **not** converted to a score, a 0/1 code, or a probability.
3. **Explainability evidence:** frozen Stage 6 global feature ranking, attached to the audit record. Attribution is **not** an independent approval criterion in this policy.

## Decision vocabulary

| Action | Meaning in this research system |
| --- | --- |
| `APPROVE` | Automatic approval under the stated policy. Not a statement of Shariah compliance. |
| `HUMAN_REVIEW` | Simulated review band. No human-review outcomes exist in this study. |
| `REJECT` | Automatic rejection / withhold approval under the stated policy. For `NOT_STRUCTURABLE_WITHOUT_REDESIGN`, the operational reading is reject-or-redesign, not a fatwa. |

## Credit-risk bands

Let `t_low <= t_high` be thresholds selected on **validation only**.

| Band | Definition |
| --- | --- |
| `LOW` | `p < t_low` |
| `MEDIUM` | `t_low <= p < t_high` |
| `HIGH` | `p >= t_high` |

A value exactly equal to `t_low` is `MEDIUM` (not approved). A value exactly equal to `t_high` is `HIGH`. If `t_low = t_high = t`, the medium band is empty: `p < t` is `LOW` and `p >= t` is `HIGH`.

Missing, non-finite, or out-of-range probabilities raise an error. They are not clipped.

## Governance normalization

| Input | Treatment |
| --- | --- |
| `None`, `unknown`, empty | `INSUFFICIENT_INFORMATION` |
| `PARTIAL` (Layer A label if mis-supplied as overall status) | `REVIEW` |
| Any other non-catalog status | error (no silent PASS) |

Unknown evidence cannot produce `PASS`.

## Evaluation order and rationale

The configured order is:

1. **Governance hard-stop.** `NOT_STRUCTURABLE_WITHOUT_REDESIGN` maps to `REJECT` for every credit band. A low default probability does not override a redesign condition, because the condition is contractual/structural, not a risk score.
2. **Evidence insufficiency and governance REVIEW.** Incomplete or REVIEW governance cannot produce `APPROVE`. High credit risk still produces `REJECT`; otherwise the action is `HUMAN_REVIEW`.
3. **Credit-risk band given governance PASS.** `LOW` → `APPROVE`, `MEDIUM` → `HUMAN_REVIEW`, `HIGH` → `REJECT`.

This order is an **architectural design choice**. It is not derived from a Shariah standard.

## Decision matrix

The matrix is exhaustive over the four governance statuses and three credit bands. The candidate mapping is:

| Governance status | LOW | MEDIUM | HIGH |
| --- | --- | --- | --- |
| `NOT_STRUCTURABLE_WITHOUT_REDESIGN` | REJECT | REJECT | REJECT |
| `INSUFFICIENT_INFORMATION` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |
| `REVIEW` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |
| `PASS` | APPROVE | HUMAN_REVIEW | REJECT |

Conflicts: if several conditions apply, the matrix cell is the only outcome. There is no numeric weighting across layers.

## Threshold identification

Thresholds are **not** selected on the fused LendingClub policy. Under real LendingClub evidence the Stage 7 profile is `INSUFFICIENT_INFORMATION`, so LOW and MEDIUM both become `HUMAN_REVIEW` and `t_low` is not identified by fused cost.

Therefore `t_low` and `t_high` are selected by minimizing expected normalized cost of the **credit-only** three-way rule on validation:

- LOW → APPROVE
- MEDIUM → HUMAN_REVIEW
- HIGH → REJECT

The frozen governance matrix is then applied without retuning. Test labels are not loaded until the freeze file is written.

## What this policy does not claim

- It does not call any application Shariah-compliant or Shariah-certified.
- It does not claim that human review improves accuracy, fairness, or religious validity.
- It does not claim that one cost ratio is the true institutional cost.
- It does not use SHAP values or Shariah labels as model features.
