# Stage 8 v2 Decision Fusion Report

This stage fuses frozen credit-risk probabilities with Stage 7 v2 per-application L2 governance evidence. It does not retrain the EBM, does not refit Platt scaling, does not search thresholds, and does not create a Shariah score.

Stage 8 v1 remains historical evidence: `docs/STAGE_8_DECISION_POLICY_REPORT.md` and `audit/stage8_decision_policy_run.json`.

**Status:** `STAGE_8_STATUS = PASS`

```text
STAGE_9 = BLOCKED
```

## A. Methodology authority

Controlling amendment: `AMENDMENT-SHARIAH-001`. Stage 7 v2: `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md`. Fusion matrix: Stage 8 v1 specification `docs/decision_policy_specification.md` (not rewritten).

## B. Fusion policy (frozen; not re-derived on TEST)

Credit bands use frozen validation-selected thresholds:

- `t_low = 0.06`
- `t_high = 0.69`

Governance × band matrix (unchanged from Stage 8 v1):

| Governance | LOW | MEDIUM | HIGH |
| --- | --- | --- | --- |
| `NOT_STRUCTURABLE_WITHOUT_REDESIGN` | REJECT | REJECT | REJECT |
| `INSUFFICIENT_INFORMATION` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |
| `REVIEW` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |
| `PASS` | APPROVE | HUMAN_REVIEW | REJECT |

L1 `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` is dataset context. It is **not** the matrix governance input. L2 `overall_governance_status` is the matrix input. `INSUFFICIENT_INFORMATION` is not converted to PASS or to religious non-compliance.

## C. Validation-derived (frozen from Stage 8 v1; not recomputed)

- Primary cost scenario: `FN:FP=5:1` with `C_REVIEW = 0.25 * C_FP`.
- Credit-only two-threshold policy: `t_low=0.06`, `t_high=0.69`.
- Monolithic single threshold (FN:FP=5:1): `t*=0.16`.
- Thresholds were selected on validation only in Stage 8 v1. Stage 8 v2 did not search a new grid.

## D. L1 / L2 integration

- L1 (once): `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` (`is_applicant_level_ruling=false`).
- L2 evaluation_mode: `PER_APPLICATION`.
- Unique TEST evidence hashes: `1`.
- Unique TEST record hashes: `208886`.
- Identical evidence hashes with distinct record hashes are expected for LendingClub: contractual fields are absent, so L2 statuses may repeat. That is not broadcast-as-inspection.

## E. TEST-derived results

- n = 208886
- credit-band counts: {'HIGH': 27, 'LOW': 5232, 'MEDIUM': 203627}
- governance-status counts: {'INSUFFICIENT_INFORMATION': 208886}
- fused decisions: APPROVE=0, HUMAN_REVIEW=208859, REJECT=27
- fused approval_rate = 0.000000
- fused review_rate = 0.999871
- fused rejection_rate = 0.000129
- rows with missing governance evidence (L2 INSUFFICIENT_INFORMATION) = 208886
- rows with NOT_STRUCTURABLE_WITHOUT_REDESIGN = 0
- audit completeness (required v2 fields present) = 1.0

### Review burden

- review_count = 208859
- review_rate = 0.999871
- review causes: {'governance_insufficiency': 5232, 'governance_insufficiency_and_credit_uncertainty': 203627}
- reviewed credit-band distribution: {'LOW': 5232, 'MEDIUM': 203627}

The review band is a simulated research-policy band. No human-review outcomes were collected.

### Credit-only vs evidence-separated (same frozen probabilities)

- credit-only (bands, no governance): approval=0.025047, review=0.974824, reject=0.000129
- monolithic single threshold: approval=0.296118, review=0.000000, reject=0.703882
- evidence-separated fused: approval=0.000000, review=0.999871, reject=0.000129

Predictive ROC-AUC/Brier are properties of the frozen credit model and are not claimed as architectural improvement.

### Default rates by fused credit band (TEST labels, evaluation only)

| Band | n | default_rate |
| --- | ---: | ---: |
| HIGH | 27 | 0.518519 |
| LOW | 5232 | 0.037462 |
| MEDIUM | 203627 | 0.216229 |

## F. What this does not claim

- No applicant is Shariah compliant or non-compliant.
- LendingClub L2 `INSUFFICIENT_INFORMATION` means insufficient contractual evidence, not a religious finding.
- L1 is not 208,886 applicant-level Shariah evaluations.
- `purpose` is not Shariah evidence.

## G. Reproducibility

- experiment_id: `stage8-lc-decision-v2`
- amendment_id: `AMENDMENT-SHARIAH-001`
- policy_version: `stage8-v2`
- l1l2_version: `stage7-l1l2-v2`
- t_low/t_high: `0.06` / `0.69`
- test_cal_sha256: `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb`
- v1_freeze_sha256: `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4`
- git_commit: `None`
- execution_timestamp: `2026-09-15T14:20:40+00:00`
- software: `3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]`
- prerequisite tests: `84 passed, 2 skipped in 2.11s`
- final test command: `python -m pytest tests -q --tb=short`
- final test summary: `164 passed, 2 warnings in 50.91s`

## H. Stage gate

`STAGE_8_STATUS = PASS`

Stage 8 v2 per-row L2 fusion implemented under AMENDMENT-SHARIAH-001; frozen thresholds reused; no broadcast; pytest passed; Stage 9 blocked.

```text
STAGE_9 = BLOCKED
```

## Artifact index

- `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`
- `audit/stage8_v2_decision_fusion_run.json`
- `results/decision/v2/frozen_policy.json`
- `results/decision/v2/tables/table3_test_decision_outcomes.csv`
- `results/decision/v2/audit/test_audit_records.csv`
- `results/figures/decision/v2/figure4_default_rate_by_band.png`
- `results/figures/decision/v2/figure5_credit_governance_heatmap.png`
- `results/figures/decision/v2/figure6_evidence_separated_architecture.png`
