# Stage 10 S10-A1-GAP report

**Classification:** `ANALYSIS-ONLY / DESCRIPTIVE`

This is **not** a new scientific confirmatory experiment. It decomposes already-observed
Stage 8 v2 / Stage 9.1 A1 counts. It does **not** independently validate the Shariah governance layer.

**Experiment ID:** `s10_a1_gap_v1` (`S10-A1-GAP`)  
**Status:** `COMPLETED — analysis-only descriptive decomposition`  
**Authorization:** `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED` 2026-09-15  
**This run executed:** `S10-A1-GAP` only. **S10-A4-SIDEBYSIDE was not executed.**

## Bound statements

- No model was retrained. No EBM/Platt/isotonic was refit.
- No threshold was searched or changed (`t_low=0.06`, `t_high=0.69` unchanged).
- A1/G0 policy was not altered. No new governance state was introduced.
- No Shariah score/probability, new Shariah rule, or halal/haram inference.
- No contractual evidence was fabricated.
- G1/G3 hypotheticals were **not** treated as observed results.
- Stage 8, Stage 9, S10-I1, and S10-R1 artifacts were not overwritten.
- UCI TEST was not opened. Stage 9 remains **CLOSED**. The paper was not drafted.

## A. Credit-band decomposition

Frozen bands: LOW `p_selected < 0.06`; MEDIUM `0.06 <= p_selected < 0.69`; HIGH `p_selected >= 0.69`.

- LOW: n=5232 (2.5047% of TEST); rule `p_selected < 0.06`
- MEDIUM: n=203627 (97.4824% of TEST); rule `0.06 <= p_selected < 0.69`
- HIGH: n=27 (0.0129% of TEST); rule `p_selected >= 0.69`

These match the existing Stage 8 v2 values LOW=5232, MEDIUM=203627, HIGH=27.

## B. Governance-state decomposition

Observed L2 `overall_governance_status` on stored Stage 8 v2 TEST audit records and published `gov_counts`:

- `PASS`: n=0 (0.0000% of TEST); not observed on LC TEST
- `REVIEW`: n=0 (0.0000% of TEST); not observed on LC TEST
- `NOT_STRUCTURABLE_WITHOUT_REDESIGN`: n=0 (0.0000% of TEST); not observed on LC TEST
- `INSUFFICIENT_INFORMATION`: n=208886 (100.0000% of TEST); observed

L1 (not the G0 input): `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` on all 208886 rows; `l1_is_applicant_level_ruling=false`. L1 is dataset/schema readiness, not an applicant-level ruling.

## C. Cross-tab `credit_band × L2_governance_status`

| credit_band | L2 status | n | % of TEST | G0 decision | populated |
| --- | --- | ---: | ---: | --- | --- |
| LOW | `PASS` | 0 | 0.0000 | APPROVE | False |
| LOW | `REVIEW` | 0 | 0.0000 | HUMAN_REVIEW | False |
| LOW | `NOT_STRUCTURABLE_WITHOUT_REDESIGN` | 0 | 0.0000 | REJECT | False |
| LOW | `INSUFFICIENT_INFORMATION` | 5232 | 2.5047 | HUMAN_REVIEW | True |
| MEDIUM | `PASS` | 0 | 0.0000 | HUMAN_REVIEW | False |
| MEDIUM | `REVIEW` | 0 | 0.0000 | HUMAN_REVIEW | False |
| MEDIUM | `NOT_STRUCTURABLE_WITHOUT_REDESIGN` | 0 | 0.0000 | REJECT | False |
| MEDIUM | `INSUFFICIENT_INFORMATION` | 203627 | 97.4824 | HUMAN_REVIEW | True |
| HIGH | `PASS` | 0 | 0.0000 | REJECT | False |
| HIGH | `REVIEW` | 0 | 0.0000 | REJECT | False |
| HIGH | `NOT_STRUCTURABLE_WITHOUT_REDESIGN` | 0 | 0.0000 | REJECT | False |
| HIGH | `INSUFFICIENT_INFORMATION` | 27 | 0.0129 | REJECT | True |

Populated cells only: LOW×INSUFFICIENT_INFORMATION=5232 → HUMAN_REVIEW; MEDIUM×INSUFFICIENT_INFORMATION=203627 → HUMAN_REVIEW; HIGH×INSUFFICIENT_INFORMATION=27 → REJECT.

## D. Deterministic policy trace

Not a new experiment. Frozen map: `p_selected` → credit band → stored L2 → G0 → A1.

- `p_selected < 0.06` → `LOW` → `INSUFFICIENT_INFORMATION` → G0[INSUFFICIENT_INFORMATION, LOW] = HUMAN_REVIEW → A1 `HUMAN_REVIEW` (n=5232)
- `0.06 <= p_selected < 0.69` → `MEDIUM` → `INSUFFICIENT_INFORMATION` → G0[INSUFFICIENT_INFORMATION, MEDIUM] = HUMAN_REVIEW → A1 `HUMAN_REVIEW` (n=203627)
- `p_selected >= 0.69` → `HIGH` → `INSUFFICIENT_INFORMATION` → G0[INSUFFICIENT_INFORMATION, HIGH] = REJECT → A1 `REJECT` (n=27)

## E. Review-rate decomposition

- A1 HUMAN_REVIEW = 208859 / 208886 = 0.9998707428932527
- LOW contribution to REVIEW: 5232 (2.5047% of TEST; 2.5050% of A1 reviews); Stage 8 cause `governance_insufficiency`.
- MEDIUM contribution to REVIEW: 203627 (97.4824% of TEST; 97.4950% of A1 reviews); Stage 8 cause `governance_insufficiency_and_credit_uncertainty`.
- HIGH contribution to REVIEW: 0 (0).
- HIGH contribution to REJECT: 27 (0.0129% of TEST; 100% of A1 REJECT).
- A1 HUMAN_REVIEW = LOW + MEDIUM = 5232 + 203627 = 208859.
- A1 REJECT = HIGH = 27.
- A1 APPROVE requires G0(PASS, LOW). Observed PASS n=0, so A1 APPROVE=0. Algebra: A1 APPROVE - A0 APPROVE = -LOW = -5232.

This high review rate is the G0 image of an all-insufficient L2 extract. It is **not** claimed to be a credit-model error merely because it is high.

## F. Evidence-gap interpretation

From existing Stage 7 v2 / Stage 8 v2 documentation only:

- `INSUFFICIENT_INFORMATION` is an L2 **evidence-completeness / schema-gap** status. It means the prototype did not have the contractual fields required for applicant-level determination.
- It is **not** a Shariah ruling, **not** expert validation, and **not** a finding that an applicant is non-compliant.
- It is **not** a finding that a contract is actually non-compliant; LendingClub rows do not contain those contracts.
- HUMAN_REVIEW under G0 is a **governance-hold** when evidence is insufficient or credit is MEDIUM. It is not a religious classification of applicants.
- L1 `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` is dataset context (`is_applicant_level_ruling=false`), and is distinct from the L2 status that enters the G0 matrix.

## G. What this analysis does NOT establish

S10-A1-GAP does **not** establish:

- that the governance layer is universally correct;
- that the review band is operationally optimal;
- that the applicants are Shariah non-compliant;
- that contracts are actually non-compliant;
- that the policy is suitable for production;
- that a human reviewer would reach a specific Shariah conclusion.

G1/G3 remain Stage 9.3 exploratory hypotheticals and are **not** observed LC TEST results.

## Provenance

- `p_selected` source (cited, not rescored): `C:/Users/User/research-project/results/calibration/test/ebm_seed42_calibrated.csv`
- Stage 8 v1 freeze SHA-256: `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4`
- Stage 8 v2 freeze SHA-256: `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b`
- table3 SHA-256: `90759eb72f1173b40b5b9363c21b0ef3d6f1cde5042748eb57871d49fb73d5ee`
- TEST cal SHA-256: `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb`
- Stage 8 policy YAML SHA-256: `d1f20fd8a0fd2ffde1ba93db36b4029af0f11a0c38215c9aba0a09a58087dfaf`
- Prior gates: S10-I1 `PASS WITH DOCUMENTATION LIMITATION`; S10-R1 `COMPLETED — exploratory/descriptive post-hoc reanalysis`
- git_commit: `None`
- Source artifacts:
  - `C:/Users/User/research-project/audit/stage8_v2_decision_fusion_run.json`
  - `C:/Users/User/research-project/results/decision/v2/tables/table3_test_decision_outcomes.csv`
  - `C:/Users/User/research-project/results/decision/v2/audit/test_audit_records.csv`
  - `C:/Users/User/research-project/configs/stage8_decision_policy.yaml`
  - `C:/Users/User/research-project/results/decision/frozen_policy.json`
  - `C:/Users/User/research-project/results/decision/v2/frozen_policy.json`
  - `C:/Users/User/research-project/results/calibration/test/ebm_seed42_calibrated.csv`
  - `C:/Users/User/research-project/docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md`
  - `C:/Users/User/research-project/docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`
  - `C:/Users/User/research-project/results/stage10/v1/metrics/s10_i1_identity.json`
  - `C:/Users/User/research-project/results/stage10/v1/metrics/s10_r1_year.json`

## Issues

- None.

## Limitations

- Stage 8 v2 per-row audit records have no row_ref; band × L2 identity uses stored Stage 8 columns, not a keyed join to p_selected.
- LendingClub schema does not contain contractual Shariah evidence; this analysis does not invent it.
- S10-A1-GAP is analysis-only / descriptive. It does not independently validate the governance layer.
- Stage 8 v2 recorded n_unique_evidence_hashes=1 and n_unique_record_hashes=208886: per-row record hashes are unique, but the governance evidence object is identical across TEST rows.
- git_commit is null (no usable .git / git). Recorded, not fabricated. Stage 10 protocol §14: not by itself a scientific abort.

## Activities not executed

- S10-A4-SIDEBYSIDE: not executed

