# Stage 10 S10-R1-YEAR report

**Classification:** `EXPLORATORY / DESCRIPTIVE POST-HOC REANALYSIS — NON-CONFIRMATORY`

This analysis is **not** a new confirmatory TEST-set experiment. LendingClub TEST was already unblinded in Stages 4B–8.
Year slices describe frozen A0 / A1 / A3/A4 maps on stored `p_selected`. They are not used to choose a policy.

**Experiment ID:** `s10_r1_year_v1` (`S10-R1-YEAR`)  
**Status:** `COMPLETED — exploratory/descriptive post-hoc reanalysis`  
**Authorization:** `AMENDMENT-STAGE10-AUTHORIZATION` `APPROVED` 2026-09-15  
**This run executed:** `S10-R1-YEAR` only.

## Bound statements

- No model was retrained.
- No EBM was refit.
- No calibration was refit.
- No threshold was selected or changed, including year-specific thresholds.
- A0, A1, and A3/A4 policies were not altered.
- Shariah rules and governance evidence were not modified.
- Year slices are **not** Shariah findings.
- UCI TEST was not opened.
- Stage 8, Stage 9, and S10-I1 artifacts were not overwritten.
- S10-A1-GAP and S10-A4-SIDEBYSIDE were **not** executed.
- Stage 9 remains **CLOSED**.
- The paper was not drafted.

## Interpretation rule

Differences between 2017 and 2018 are reported as **descriptive temporal differences**,
**year-specific decision allocation**, **observed difference in default prevalence**,
or a **post-hoc temporal pattern**.

This report does **not** call those differences model degradation, concept drift,
calibration failure, policy failure, a causal effect, or evidence of generalization failure.
No p-test of 2017 vs 2018 equality was computed.

## Year derivation

- Used the stored `year` column in `results/calibration/test/ebm_seed42_calibrated.csv`.
- Did **not** parse `issue_d` or `issue_month` in this run.
- Historically, Stage 5 stored `year` as `int(issue_month[0:4])`. That derivation was not repeated here.

## Frozen inputs

- TEST n = 208886
- n_2017 = 152726; n_2018 = 56160
- `p_selected` = stored Platt-calibrated probability (not recomputed)
- `t_low=0.06`, `t_high=0.69`, `t*=0.16`
- S10-I1 status (gate): `PASS WITH DOCUMENTATION LIMITATION`

## Dataset composition

- 2017: n=152726, defaults=35394, default rate=0.231748 (Wilson 95% CI 0.229639–0.233871)
- 2018: n=56160, defaults=8846, default rate=0.157514 (Wilson 95% CI 0.154525–0.160551)

## A0 (frozen 0.06 / 0.69)

- 2017: APPROVE 3339 (2.1863%); HUMAN_REVIEW 149366 (97.8000%); REJECT 21 (0.0138%)
- 2018: APPROVE 1893 (3.3707%); HUMAN_REVIEW 54261 (96.6186%); REJECT 6 (0.0107%)

## A1 (same credit bands, frozen G0 INSUFFICIENT_INFORMATION)

- 2017: APPROVE 0 (0.0000%); HUMAN_REVIEW 152705 (99.9862%); REJECT 21 (0.0138%)
- 2018: APPROVE 0 (0.0000%); HUMAN_REVIEW 56154 (99.9893%); REJECT 6 (0.0107%)

## A3/A4 (frozen t*=0.16, no HUMAN_REVIEW branch)

- 2017: APPROVE 42443 (27.7903%); HUMAN_REVIEW 0 (0.0000%); REJECT 110283 (72.2097%)
- 2018: APPROVE 19412 (34.5655%); HUMAN_REVIEW 0 (0.0000%); REJECT 36748 (65.4345%)

## Credit-band distribution (frozen 0.06 / 0.69)

- 2017: LOW 3339 (2.1863%); MEDIUM 149366 (97.8000%); HIGH 21 (0.0138%)
- 2018: LOW 1893 (3.3707%); MEDIUM 54261 (96.6186%); HIGH 6 (0.0107%)

## Descriptive default rate by A0 credit band

Evaluation only. Not used to tune a threshold or policy.

- 2017 LOW: n=3339, defaults=145, default rate=0.043426 (Wilson 95% CI 0.037022–0.050880)
- 2017 MEDIUM: n=149366, defaults=35238, default rate=0.235917 (Wilson 95% CI 0.233771–0.238077)
- 2017 HIGH: n=21, defaults=11, default rate=0.523810 (Wilson 95% CI 0.323692–0.716563)
- 2018 LOW: n=1893, defaults=51, default rate=0.026941 (Wilson 95% CI 0.020550–0.035249)
- 2018 MEDIUM: n=54261, defaults=8792, default rate=0.162032 (Wilson 95% CI 0.158955–0.165156)
- 2018 HIGH: n=6, defaults=3, default rate=0.500000 (Wilson 95% CI 0.187613–0.812387)

## Descriptive notes

- TEST composition: 2017 n=152726, 2018 n=56160. This is the stored year split, not a sampling design.
- Observed difference in default prevalence: 2017 0.231748 (35394/152726) vs 2018 0.157514 (8846/56160). This is a descriptive temporal difference, not a causal effect, not concept drift inference, and not a generalization-failure test.
- A0 year-specific decision allocation: 2017 APPROVE/REVIEW/REJECT = 3339/149366/21 vs 2018 1893/54261/6. Reported as a post-hoc temporal pattern under frozen maps, not as policy failure.
- A1 year-specific decision allocation: 2017 APPROVE/REVIEW/REJECT = 0/152705/21 vs 2018 0/56154/6. Reported as a post-hoc temporal pattern under frozen maps, not as policy failure.
- A3_A4 year-specific decision allocation: 2017 APPROVE/REVIEW/REJECT = 42443/0/110283 vs 2018 19412/0/36748. Reported as a post-hoc temporal pattern under frozen maps, not as policy failure.
- HIGH credit band remains n=27 overall. Year-wise HIGH rates are descriptive counts only and do not support inference beyond those counts.
- No p-test of 2017 vs 2018 equality was computed.
- Year was not used to select a threshold, calibrator, or policy.

## Provenance

- Probability file: `C:/Users/User/research-project/results/calibration/test/ebm_seed42_calibrated.csv`
- TEST cal SHA-256: `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb`
- Stage 8 v2 freeze SHA-256: `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b`
- table3 SHA-256: `90759eb72f1173b40b5b9363c21b0ef3d6f1cde5042748eb57871d49fb73d5ee`
- EBM/Platt joblib files were **not** loaded.
- `p_selected` was **not** recomputed from `p_raw`.
- random_seed_used: `None` (none). Stored prediction seed in the CSV: 42.
- git_commit: `None`

## Issues

- None.

## Limitations

- HIGH credit-band n is 27 on pooled TEST; year-wise HIGH default rates are descriptive counts only.
- S10-R1 is post-hoc grouping of already-unblinded LendingClub TEST outputs. It is not confirmatory.
- git_commit is null (no usable .git / git). Recorded, not fabricated. Stage 10 protocol §14: not by itself a scientific abort.

## Activities not executed

- S10-A1-GAP: not executed
- S10-A4-SIDEBYSIDE: not executed

