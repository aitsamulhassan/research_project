# Stage 10 S10-I1-IDENTITY report

This is an **integrity/provenance check**. It is **not** a new scientific confirmatory experiment.

Passing does **not** generate independent scientific evidence. LendingClub TEST was already unblinded in Stages 4B–8.

**Experiment ID:** `s10_i1_identity_v1` (`S10-I1-IDENTITY`)  
**Status:** `PASS WITH DOCUMENTATION LIMITATION`  
**Classification:** `INTEGRITY / PROVENANCE CHECK — NOT A SCIENTIFIC CONFIRMATORY EXPERIMENT`  
**Authorization:** `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED` 2026-09-15  
**Execution gate:** `STAGE_10_EXECUTION = AUTHORIZED FOR S10-I1-IDENTITY, S10-R1-YEAR, S10-A1-GAP, AND S10-A4-SIDEBYSIDE ONLY`  
**This run executed:** `S10-I1-IDENTITY` only.

## Bound statements

- No model was retrained.
- No EBM was refit.
- No calibration was refit (Platt/isotonic were not fitted).
- No threshold was selected or changed.
- No historical Stage 7/8/9 result was overwritten.
- UCI TEST was not opened.
- Shariah rules and governance evidence were not modified.
- A0, A1, and A3/A4 policies were not altered.
- The paper was not drafted.
- S10-R1-YEAR, S10-A1-GAP, and S10-A4-SIDEBYSIDE were **not** executed.
- Stage 9 remains **CLOSED**.

## A. A0 and A1

A0 and A1 consume the **same** frozen stored column `p_selected` from
`results/calibration/test/ebm_seed42_calibrated.csv`. A0 is the frozen two-threshold credit map.
A1 uses the same credit-band mapping (`t_low=0.06`, `t_high=0.69`) and then the frozen G0
`INSUFFICIENT_INFORMATION` fusion (LOW/MEDIUM → HUMAN_REVIEW, HIGH → REJECT). No new fusion engine was run;
G0 is the algebraic identity of the stored Stage 8 v2 fused counts.

- A0 remap match: `True` counts `{'APPROVE': 5232, 'HUMAN_REVIEW': 203627, 'REJECT': 27}` (t_low=0.06, t_high=0.69)
- A1 credit-band match: `True` `{'LOW': 5232, 'MEDIUM': 203627, 'HIGH': 27}`
- A1 G0-from-same-bands match: `True` counts `{'APPROVE': 0, 'HUMAN_REVIEW': 208859, 'REJECT': 27}`

## B. A3/A4

A3/A4 consume the **same** frozen `p_selected` vector. The frozen monolithic threshold is `t*=0.16`
applied as a binary map (`t_low=t_high=t*`), which has **no HUMAN_REVIEW branch**.

- A3/A4 remap match: `True` counts `{'APPROVE': 61855, 'HUMAN_REVIEW': 0, 'REJECT': 147031}`
- t* = 0.16
- HUMAN_REVIEW count = 0
- human_review_branch = `False`

## C. Provenance

Probability / decision inputs:

- `C:/Users/User/research-project/results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected`, `p_platt`, `p_raw`, `row_ref`, `selected_method`)
- `results/decision/v2/tables/table3_test_decision_outcomes.csv` (stored A0/A1/A3 counts)
- `results/decision/v2/audit/test_audit_records.csv` (Stage 8 v2 per-row calibrated_probability / bands)
- `results/decision/frozen_policy.json` (Stage 8 v1 freeze)
- `results/decision/v2/frozen_policy.json` (Stage 8 v2 freeze)
- `results/calibration/artifacts/platt_record.json`
- `audit/stage9_4_uci_run.json` (`protected_hashes_after`)

- Calibrated TEST n = 208886
- Unique `row_ref` = 208886
- Same 208,886 LendingClub TEST rows: `True`
- `p_selected` identical to stored `p_platt`: `True`
- `selected_method` is Platt only: `True`
- Stage 8 v2 audit n = 208886
- Audit calibrated_probability matches `p_selected` (positional, atol 1e-12): `True`
- `p_selected` was **not** recomputed from `p_raw` in this check.
- EBM/Platt joblib files were **not** loaded for scoring.

## D. Policy integrity

- Stage 8 v1 freeze SHA-256: `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4` (expected `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4`)
- Stage 8 v2 freeze SHA-256: `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b` (expected `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b`)
- table3 SHA-256: `90759eb72f1173b40b5b9363c21b0ef3d6f1cde5042748eb57871d49fb73d5ee` (expected `90759eb72f1173b40b5b9363c21b0ef3d6f1cde5042748eb57871d49fb73d5ee`)
- TEST calibrated CSV SHA-256: `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb` (expected `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb`)
- Match Stage 9.4 `protected_hashes_after`: `True`
- t_low=0.06, t_high=0.69, t*=0.16
- v2 freeze t_low=0.06, t_high=0.69, monolithic_t=0.16
- thresholds_reselected=`False`
- Platt a=1.1988263209549705, b=0.6697765046966161; record match=`True`

## E. Outcome

**PASS WITH DOCUMENTATION LIMITATION**

This classification is an integrity/provenance result. It is not a scientific confirmatory TEST experiment.

## Issues

- None.

## Documentation limitations

- Stage 8 v2 test_audit_records.csv has no row_ref column; calibrated_probability vs p_selected identity is positional (calibrated CSV file order), not a keyed join. This is a provenance documentation limitation, not a count/hash mismatch.
- git_commit is null (no usable .git / git). Recorded, not fabricated. Stage 10 protocol §14: not by itself a scientific abort.

## Activities not executed

- S10-R1-YEAR: not executed
- S10-A1-GAP: not executed
- S10-A4-SIDEBYSIDE: not executed

