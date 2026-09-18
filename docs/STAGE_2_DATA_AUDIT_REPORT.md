# Stage 2 Data Acquisition & Forensic Audit

## 1. Executive Summary

Stage 2 acquired the specified Zenodo LendingClub granting-model release and the official UCI Default of Credit Card Clients package, stored them as immutable raw files, and produced schema, target, temporal, leakage, purpose, privacy, missingness, integrity, distribution, and comparability audits. No model was trained. No split was created. No Shariah rule engine was built. No synthetic applicants were created.

- LendingClub rows x columns: 1347681 x 15
- UCI rows x columns: 30000 x 25
- Stage status: COMPLETE

## 2. Data Sources and Licensing

- LendingClub: DOI 10.5281/zenodo.11295916, https://zenodo.org/records/11295916. License: cc-by-4.0. Version: 0.1. File: `LC_loans_granting_model_dataset.csv` (167468415 bytes). SHA-256: `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc`.
- UCI: https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients, DOI 10.24432/C55S3H. License: CC BY 4.0. File: `default+of+credit+card+clients.zip` (5539494 bytes). SHA-256: `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602`.
- Manifests: `docs/raw_data_manifest.csv`, `docs/raw_data_manifest.json`.

## 3. Dataset Dimensions

LendingClub: 1347681 rows, 15 columns. Duplicate rows: 0. Duplicate IDs: 0. Schema match to Zenodo variable list: True.

UCI: 30000 rows, 25 columns (UCI page: 30000 instances, 23 features). Spreadsheet has two header rows (X-codes and names).

## 4. Target Definitions

LendingClub target column: `Default`. Prevalence Default=1: 19.978689%. Status: TARGET_DEFINITION_DOCUMENTATION_CONFLICT.

Zenodo documentation states that Default=1 corresponds to charged off and Default=0 to fully paid, and that transitory loan_status values were removed. A later sentence says the release keeps loans that are either "Fully Paid" or "Default" (original loan_status names) and does not mention "Charged Off" in that filter sentence. Original loan_status also contains a rare 'Default' category distinct from 'Charged Off'. This internal documentation conflict is not silently reconciled.

UCI target column: `default payment next month`. Prevalence =1: 22.12%. Status: VERIFIED_FROM_UCI_SPREADSHEET_AND_DOCUMENTATION.

## 5. Temporal Audit

LendingClub `issue_d` dtype: str. Unique parsed months: 139. Range: 2007-06-01 to 2018-12-01. Missing: 0.0%. Malformed: 0. Availability: AT_APPROVAL_NOT_SHOWN_TO_BE_BEFORE_DECISION. Split cutoffs were not defined.

UCI: NO_CALENDAR_TIMESTAMPS. Payment/bill columns encode a fixed April-September 2005 window from the UCI documentation, not per-row origination timestamps.

## 6. Leakage Audit

Non-SAFE classifications:

| column | classification | confidence |
| --- | --- | --- |
| issue_d | POTENTIAL_LEAKAGE | high |
| experience_c | UNKNOWN | low |
| Default | TARGET | high |

Full audit: `docs/lendingclub_leakage_audit.csv` and `docs/lendingclub_leakage_audit.md`. No feature was dropped.

## 7. Purpose/Application-Field Audit

`purpose`, `title`, and `desc` are present. `purpose` is documented as the loan-request purpose category. `title`/`desc` are borrower free text (raw values not published). No Shariah rules were written. Details: `docs/lendingclub_purpose_audit.md`.

UCI financing purpose: ABSENT.

## 8. Privacy/Identifier Audit

LendingClub: `id` DIRECT_IDENTIFIER; `addr_state`/`zip_code`/`revenue` QUASI_IDENTIFIER; `title`/`desc` FREE_TEXT. Employer name, email, phone, and street address columns were not present in this release. Raw PII/free text is not printed in reports. Table: `docs/lendingclub_privacy_audit.csv`.

UCI: `ID` identifier; demographic attributes present.

## 9. Missingness

Missingness classes are diagnostic only (0 = none; <5.0% = low; <20.0% = moderate; else high). No imputation was performed.

LendingClub high-missingness columns: desc (91.162671%).

UCI observed any missing: False.

## 10. Integrity and Duplicate Findings

See `docs/lendingclub_integrity_audit.md`. Outliers were not deleted.

## 11. Distribution Findings

Numeric and categorical diagnostic profiles (no winsorizing, clipping, or scaling): `results/tables/lendingclub_numeric_profile.csv`, `results/tables/lendingclub_categorical_profile.csv`. Free-text top categories are redacted.

## 12. UCI Audit

See `docs/uci_schema_report.md` and `results/metrics/uci_dataset_audit.json`. Loader: Excel COM conversion of the official `.xls` member from the official zip, without modifying the zip.

UCI Additional Variable Information does not fully match observed codes (EDUCATION 0/5/6, MARRIAGE 0, PAY_* values 0 and -2). Negative BILL_AMT* values are present. None of these were recoded or deleted.

## 13. Cross-Dataset Comparability

See `docs/dataset_comparability.md`. Conclusion: `GENERALIZATION_OF_METHOD`, not `DIRECT_DOMAIN_TRANSFER`. Datasets were not merged.

## 14. Dataset Limitations

- LendingClub observations are originated loans that reached a terminal status in the depositor's filter, not the full application funnel.
- Depositor already cleaned/filtered the parent Kaggle extract; this is not the raw LendingClub tape.
- US P2P 2007–2018; not an Islamic-finance sample.
- UCI is a 2005 Taiwan credit-card snapshot without purpose or origination dates.

## 15. Unsupported Claims

- Neither dataset is Islamic, Shariah-compliant, or a Shariah certification corpus.
- UCI is not a LendingClub proxy.
- Presence of `purpose` does not authorize a Shariah engine or certified rulings.
- `issue_d` is not shown to be a pre-decision application timestamp.
- No experimental performance numbers exist yet.

## 16. Stage-2 Decisions

- Raw files in `data/raw/` are immutable.
- Do not combine the datasets at applicant level.
- Do not drop columns from raw data.
- Do not impute, encode, or split yet.
- Do not train models.
- Primary/secondary roles remain as specified, with the caveats in this report.

## 17. Items Requiring Research-Owner Review

- issue_d: approval month vs feature vs time-index only; do not set split cutoffs until reviewed.
- experience_c: TIMING_UNVERIFIED construction using current-obligation credit date.
- dti_n: depositor application-time claim vs 'Monthly information' wording.
- Target Default: documentation conflict between charged-off mapping and 'Fully Paid or Default' filter sentence.
- Selection bias: dataset contains originated and resolved loans only.
- UCI role remains GENERALIZATION_OF_METHOD, not DIRECT_DOMAIN_TRANSFER; do not merge.
- UCI EDUCATION/MARRIAGE/PAY_* codes include values not defined in UCI Additional Variable Information; do not recode without a protocol.
- purpose/title/desc may later feed decision-support; no Shariah certification is implied.

Open issues:

- LendingClub target original loan_status mapping is not uniquely specified in Zenodo text.
- UCI documentation vs contents conflict (not recoded) in: EDUCATION, MARRIAGE, PAY_0, PAY_2, PAY_3, PAY_4, PAY_5, PAY_6.

## 18. Reproducibility Information

- run_id: 894198d9-f636-4874-a300-e43aeee44a64
- timestamp: 2026-09-14T11:24:13+00:00
- git_commit: None
- python_version: 3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]
- operating_system: Windows 11 (10.0.26200)
- script_version: stage2-0.1.0
- dataset hashes: {
  "LC_loans_granting_model_dataset.csv": "207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc",
  "default+of+credit+card+clients.zip": "56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602"
}
- Reproduce: `python src/data/audit_datasets.py`
