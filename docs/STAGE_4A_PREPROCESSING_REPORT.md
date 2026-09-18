# Stage 4A Preprocessing Report

## 1. Objective

Fit a leakage-safe preprocessor for the frozen LendingClub primary predictor set. Parameters are learned from TRAIN only. Validation and test are transformed with those frozen parameters. No model was trained. Raw files were not modified. UCI was not merged.

## 2. Frozen Feature Set

Primary predictors: `revenue`, `dti_n`, `loan_amnt`, `fico_n`, `emp_length`, `purpose`, `home_ownership_n`, `addr_state`, `zip_code`.

Explicitly excluded and rejected by the preprocessor if present: `Default`, `desc`, `experience_c`, `id`, `issue_d`, `title`.

Frozen split used to select TRAIN rows: 2007-06 through 2016-03. Boundaries were not changed.

## 3. Preprocessing Policy

Policy file: `docs/lendingclub_preprocessing_policy.csv`.

- `revenue` (float64): `median_impute_then_passthrough` fit_on=TRAIN_ONLY
- `dti_n` (float64): `median_impute_then_passthrough_preserve_999` fit_on=TRAIN_ONLY
- `loan_amnt` (int64): `median_impute_then_passthrough` fit_on=TRAIN_ONLY
- `fico_n` (float64): `median_impute_then_passthrough` fit_on=TRAIN_ONLY
- `emp_length` (string): `constant_impute_then_one_hot` fit_on=TRAIN_ONLY
- `purpose` (string): `constant_impute_then_one_hot` fit_on=TRAIN_ONLY
- `home_ownership_n` (string): `constant_impute_then_one_hot` fit_on=TRAIN_ONLY
- `addr_state` (string): `constant_impute_then_one_hot` fit_on=TRAIN_ONLY
- `zip_code` (string): `constant_impute_then_one_hot` fit_on=TRAIN_ONLY

Operations were chosen from the TRAIN schema, not from common-practice defaults. No variable was standardized, winsorized, or clipped.

## 4. Missing-Value Handling

TRAIN missing counts for the nine predictors: {'revenue': 0, 'dti_n': 0, 'loan_amnt': 0, 'fico_n': 0, 'emp_length': 0, 'purpose': 0, 'home_ownership_n': 0, 'addr_state': 0, 'zip_code': 0}.

Because TRAIN has no missing values on these predictors, no missingness indicator was added. A TRAIN-only median imputer is still fitted for numeric columns, and a constant token imputer is applied to categoricals, so a later missing cell can be transformed without refitting. Categorical missing at transform uses token `__MISSING__`. That token is not a TRAIN category, so it is treated as unseen (all-zero one-hot). Validation/test missingness was not inspected to set this policy.

## 5. Numeric Feature Handling

Numeric predictors from the actual TRAIN schema: `revenue`, `dti_n`, `loan_amnt`, `fico_n`.

`emp_length`, `home_ownership_n`, and `zip_code` are strings in TRAIN and are treated as categorical, not numeric.

Numeric values are passed through after median imputation. No scaler, log, clip, or winsorize step is included.

Fitted TRAIN medians: {'revenue': 65000.0, 'dti_n': 17.6, 'loan_amnt': 12000.0, 'fico_n': 692.0}.

## 6. Categorical Feature Handling

Categorical predictors: `emp_length` (12 TRAIN categories, including `NI`), `purpose` (14), `home_ownership_n` (4), `addr_state` (51), `zip_code` (938 masked prefixes).

Encoding: `sklearn.preprocessing.OneHotEncoder(handle_unknown='ignore')` fitted on TRAIN only. Categories not observed in TRAIN are not enumerated from validation/test. At transform they yield an all-zero dummy row for that feature group.

## 7. Special-Value Handling

`dti_n == 999`: {'original_value': 999.0, 'interpretation': 'UNCERTAIN', 'evidence': 'Stage 2 noted dti_n==999 as a possible sentinel in some LendingClub extracts. Zenodo documentation for this granting-model release does not define 999 as missing. Research-owner freeze: preserve original dti_n values; do not alter or recalculate.', 'transformation': 'NONE', 'justification': 'Interpretation remains uncertain, so the value is preserved. It is not deleted, not recoded to NA, and not clipped. TRAIN count of exact 999 is recorded only as an audit statistic.', 'train_count_exact_999': 1}.

## 8. Train-Only Fitting

The preprocessor was fitted on 941267 TRAIN rows. Validation and test were transformed afterward and were not concatenated into `fit`. Fitted state was re-read after those transforms and matched the post-fit snapshot.

## 9. Leakage Tests

Module: `tests/test_preprocessing_leakage.py`.

Script-level state comparison after transforming validation and test: True.

Pytest: 14 passed (`python -m pytest tests/test_preprocessing_leakage.py`). Checks covered train-only category/median identity, unchanged fitted state after validation/test/extra-row transforms, unchanged raw hash, deterministic feature count, identical transformed schemas, and rejection of `Default`, `issue_d`, `experience_c`, `id`, and an unseen purpose label without refitting.

On the basis of those executed tests, the Stage 4A preprocessor is leakage-safe with respect to train-only fitting and the frozen excluded columns.

## 10. Reproducibility

See `audit/preprocessing_run.json`. `git_commit` is recorded as null when no git repository exists.

## 11. Artifacts

- `docs/lendingclub_preprocessing_policy.csv`
- `src/preprocessing/lendingclub_preprocessor.py`
- `results/artifacts/lendingclub_preprocessor.joblib`
- `results/metrics/preprocessing_summary.json`
- `results/tables/preprocessing_feature_summary.csv`
- `audit/preprocessing_run.json`
- `docs/STAGE_4A_PREPROCESSING_REPORT.md`
- `tests/test_preprocessing_leakage.py`

Applicant-level transformed matrices were not written to `results/`.

## 12. Open Issues

- `zip_code` one-hot uses 938 TRAIN levels (high cardinality). No frequency grouping was invented in this stage.
- `dti_n == 999` remains unlabeled.
- No scaling is applied; Stage 4B models that require scaled inputs must either tolerate raw numeric scales or obtain a new, separately justified, TRAIN-only scaler through methodology review.
- Transformed matrices are produced in memory / by re-running `transform`; they are not stored as public result tables.

## 13. Stage-4B Preconditions

Stage 4B may begin only if these fitted parameters remain frozen, preprocessing stays TRAIN-only, excluded columns stay excluded, and no test metric is used to revise encoding. Stage 4B is not started by this script.
