# Evidence schema

Governance evidence is **not** the LendingClub predictor set (`revenue`, `dti_n`, `loan_amnt`, `fico_n`, `emp_length`, `purpose`, `home_ownership_n`, `addr_state`, `zip_code`). Those fields are permanently excluded from Shariah evaluation.

Machine-readable items live in `docs/shariah/evidence_schema.json`.

## Layer A

Does the record contain the information needed to evaluate **applicable verified** rules?

- COMPLETE
- PARTIAL (including when a named AAOIFI standard is in scope but clauses were not verified)
- INSUFFICIENT

## Layer B

Evaluate a rule only when it is in scope and executable.

Unknown/null required fields produce INSUFFICIENT_INFORMATION. Unknown is never treated as PASS.

## LendingClub

For a LendingClub-style application profile, contract-level items are NOT_AVAILABLE. The expected L2 governance outcome is INSUFFICIENT_INFORMATION.

Stage 7 v2 L1 for this dataset is `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` (dataset/integration readiness, not a ruling). L2 extraction drops firewall fields including `purpose` and does not infer contract type.
