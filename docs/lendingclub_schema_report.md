# LendingClub Schema Report

Source: Zenodo 10.5281/zenodo.11295916, file `LC_loans_granting_model_dataset.csv`.
Loaded without dtype coercion beyond pandas CSV inference. No transformations were applied.

- Rows: 1347681
- Columns: 15
- Duplicate column names: none
- Duplicate rows: 0
- Duplicate loan identifiers (`id`): 0
- Unique `id` values: 1347681
- Schema matches Zenodo documented variable list: True

## Exact column names

| position | column | dtype |
| --- | --- | --- |
| 0 | id | int64 |
| 1 | issue_d | str |
| 2 | revenue | float64 |
| 3 | dti_n | float64 |
| 4 | loan_amnt | int64 |
| 5 | fico_n | float64 |
| 6 | experience_c | int64 |
| 7 | emp_length | str |
| 8 | purpose | str |
| 9 | home_ownership_n | str |
| 10 | addr_state | str |
| 11 | zip_code | str |
| 12 | Default | int64 |
| 13 | title | str |
| 14 | desc | str |

## Documented vs observed schema

- Documented columns missing from file: none
- File columns missing from documentation: none

Full per-column null/unique/sample profile: `results/tables/lendingclub_column_profile.csv`.
Free-text and identifier sample values are redacted in that profile.
