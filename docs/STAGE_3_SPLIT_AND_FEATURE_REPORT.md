# Stage 3 Split and Feature Policy Report

## 1. Executive Summary

Stage 3 froze the LendingClub target, predictor set, exclusions, and temporal train/validation/test membership, and created a separate UCI stratified split for method generalization. No model was trained. No preprocessing was fit. Raw files were not modified. LendingClub and UCI were not merged.

- LendingClub primary predictors: 9
- LendingClub split: train 941267, validation 197528, test 208886
- UCI split seed: 42

## 2. Frozen Target Definition

LendingClub target is `Default`.

- Positive class `1` = Charged Off
- Negative class `0` = Fully Paid

This is the research-owner freeze. No additional target interpretation was invented. Integrity re-check: Default is in {0,1} with zero missing values. Artifact: `results/metrics/final_target_definition.json`.

## 3. LendingClub Feature Policy

Primary-model predictors (9): `revenue`, `dti_n`, `loan_amnt`, `fico_n`, `emp_length`, `purpose`, `home_ownership_n`, `addr_state`, `zip_code`.

Full table: `docs/lendingclub_feature_policy.csv`.

## 4. Excluded Variables

- `id` (IDENTIFIER): Unique loan identifier. Research-owner freeze: IDENTIFIER + EXCLUDE from the model.
- `issue_d` (TIME_INDEX): Month/year the loan was approved. Research-owner freeze: temporal ordering variable only; MUST NOT be used as a predictive model feature (TIME_INDEX + EXCLUDE_FROM_MODEL).
- `experience_c` (EXCLUDED): Research-owner freeze: excluded from model features. Construction uses credit dates from previous/current obligations; timing cannot be established as safely available at the precise granting decision point.
- `title` (TEXT): Borrower-provided free-text title. Excluded from the primary credit model. Retained as a future experimental branch for explainability/Shariah investigation. Not silently discarded.
- `desc` (TEXT): Borrower-provided free-text description. Excluded from the primary credit model. Retained as a future experimental branch despite high missingness. Not silently discarded.

`dti_n` is retained with original values.

## 5. Text Feature Policy

`title` and `desc` are excluded from the primary credit model and retained as a future experimental branch. They are not silently discarded. Details: `docs/text_feature_policy.md`. No text model was built.

## 6. Temporal Index Definition

`issue_d` is the approval month/year. It is used only to order observations. It is not a predictor.

## 7. LendingClub Split Method

Chronological issue_d month order. Train = earliest months with cumulative observation share <= 0.70. Validation = subsequent months until cumulative share <= 0.85. Test = remaining latest months. Cutoffs snap to observed months; a month is never split. Cutoffs were not chosen by inspecting model performance.

Train rule: `issue_month <= 2016-03`.
Validation rule: `2016-04 <= issue_month <= 2017-01`.
Test rule: `issue_month >= 2017-02`.

No row appears in more than one split. No resampling, class balancing, or synthetic rows.

## 8. LendingClub Split Boundaries

- Train: 2007-06 to 2016-03
- Validation: 2016-04 to 2017-01
- Test: 2017-02 to 2018-12

`train_date < validation_date < test_date` holds at the month grain.

## 9. Split Class Distribution

- Train: 941267 rows, prevalence 0.18681840540463016
- Validation: 197528 rows, prevalence 0.24889129642379815
- Test: 208886 rows, prevalence 0.2117901630554465

Monthly table: `results/tables/lendingclub_monthly_target_distribution.csv`.
Split table: `results/tables/lendingclub_split_distribution.csv`.

## 10. UCI Split Method

No reliable UCI timestamp exists. Split is stratified on `default payment next month` with proportions 0.70/0.15/0.15, seed 42. Within each class, IDs are sorted then shuffled with `numpy.random.RandomState(42)` consumed in increasing class-label order. Remainder after floor(0.70n) and floor(0.15n) goes to test. This split is not used for LendingClub.

- Train: 20999
- Validation: 4499
- Test: 4502

## 11. UCI Feature Policy

`ID` is an excluded identifier. `default payment next month` is the UCI target. The remaining 23 columns are UCI-specific candidate predictors. They are not claimed to be semantically equivalent to LendingClub features. Table: `docs/uci_feature_policy.csv`.

## 12. Undocumented UCI Codes

Observed undocumented codes were preserved and not recoded: EDUCATION 0/5/6, MARRIAGE 0, PAY_0 and PAY_2–PAY_6 values 0 and -2. Counts are in `results/metrics/uci_split_summary.json`.

## 13. Leakage Controls

- `issue_d` excluded from predictors
- `experience_c` excluded from predictors
- `id` excluded from predictors
- `Default` used only as target
- `title`/`desc` excluded from the primary model
- Temporal split prevents later-originated loans from training
- UCI not merged into LendingClub
- No preprocessing that could leak test information

Newly discovered leakage in this stage: none identified beyond the frozen Stage 2/owner exclusions.

## 14. Reproducibility Artifacts

- `docs/lendingclub_feature_policy.csv`
- `docs/uci_feature_policy.csv`
- `docs/text_feature_policy.md`
- `results/metrics/final_target_definition.json`
- `results/metrics/lendingclub_split_summary.json`
- `results/metrics/uci_split_summary.json`
- `audit/lendingclub_split_manifest.json`
- `audit/uci_split_manifest.json`
- `results/tables/lendingclub_split_assignments.csv`
- `results/tables/uci_split_assignments.csv`
- Script: `src/data/create_splits.py` version stage3-0.1.0

Raw LendingClub SHA-256: `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc`.
Raw UCI SHA-256: `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602`.

## 15. Integrity Test Results

Script-level integrity errors: none.
Pytest module: `tests/test_splits.py`.

## 16. Open Issues

- Primary credit model still excludes title/desc; a later text/Shariah branch is not specified in Stage 3.
- UCI undocumented codes remain unlabeled; no recode protocol is approved.
- addr_state and zip_code are retained predictors and quasi-identifiers; privacy handling is not a Stage 3 encoding task.

## 17. Stage-4 Preconditions

Stage 4 (preprocessing) may begin only if:

- these splits and policies remain frozen;
- preprocessing is fit on train only;
- `issue_d` and `experience_c` stay out of the predictor matrix;
- undocumented UCI codes are not given invented meanings;
- no test-driven feature selection or thresholding.

Stage 4 is not started by this script.
