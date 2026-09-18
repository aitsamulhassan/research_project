# LendingClub Leakage Audit

Classifications use the Zenodo granting-model documentation for this release.
Features were not dropped. Timing was not guessed when it could not be established.

| column | classification | confidence | action_recommendation |
| --- | --- | --- | --- |
| id | IDENTIFIER | high | Retain for audit/join only; exclude from features. |
| issue_d | POTENTIAL_LEAKAGE | high | Do not use as a predictive feature until methodology review. Candidate time index only. Split cutoffs are not defined in Stage 2. |
| revenue | SAFE_APPLICATION_TIME | high | Eligible application-time candidate feature. |
| dti_n | SAFE_APPLICATION_TIME | medium | Eligible candidate feature; TIMING wording ambiguity flagged for review. |
| loan_amnt | SAFE_APPLICATION_TIME | high | Eligible application-time candidate feature. |
| fico_n | SAFE_APPLICATION_TIME | high | Eligible application-time candidate feature. |
| experience_c | UNKNOWN | low | Do not treat as confirmed application-time until methodology review. Do not drop silently. |
| emp_length | SAFE_APPLICATION_TIME | high | Eligible application-time candidate feature. |
| purpose | SAFE_APPLICATION_TIME | high | Eligible application-time candidate feature and the documented financing-purpose field for later Shariah-oriented decision-support work. No Shariah rules are created in Stage 2. |
| home_ownership_n | SAFE_APPLICATION_TIME | high | Eligible application-time candidate feature. |
| addr_state | SAFE_APPLICATION_TIME | high | Eligible candidate feature; also a quasi-identifier. |
| zip_code | SAFE_APPLICATION_TIME | high | Eligible candidate feature; treat as quasi-identifier. |
| Default | TARGET | high | Use only as the credit-risk target; never as a feature. |
| title | SAFE_APPLICATION_TIME | high | Free-text application-time field. Not a structured model feature unless a later protocol says so. Do not publish raw text. |
| desc | SAFE_APPLICATION_TIME | high | Free-text application-time field. Likely sparse. Do not publish raw text. No Shariah rules in Stage 2. |

## Notes requiring review

- `issue_d` is an approval/origination month, not a demonstrated pre-decision application date.
- `experience_c` construction uses a current-obligation credit date whose application-time status is TIMING_UNVERIFIED.
- `dti_n` is documented as application-time but the phrase "Monthly information" is recorded as a wording ambiguity.
- No official separate LendingClub parent data dictionary was retrieved in this stage; evidence is the Zenodo release description.

Full reasons: `docs/lendingclub_leakage_audit.csv`.
