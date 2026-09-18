# Cross-Dataset Comparability

The datasets were not merged.
No applicant-level linkage key exists between US LendingClub loans and Taiwan credit-card clients.

| Concept | LendingClub variable(s) | UCI variable(s) | Comparable? | Reason |
| --- | --- | --- | --- | --- |
| target | Default | default payment next month | No | Both are binary default labels, but they are not equivalent outcomes: LC is terminal resolution of an originated US P2P installment loan (fully paid vs defaulted/charged-off per depositor); UCI is whether a Taiwan credit-card client defaulted in the next month after a 2005 window. |
| credit history | fico_n; experience_c (timing unverified) | PAY_0, PAY_2, PAY_3, PAY_4, PAY_5, PAY_6 | No | FICO/repeat-borrower flag vs six months of repayment-status codes. Not the same construct. |
| income | revenue | ABSENT | No | UCI has no income field. |
| debt/obligations | dti_n; loan_amnt | LIMIT_BAL; BILL_AMT1-BILL_AMT6 | No | Requested installment amount and DTI vs revolving limit and monthly bill amounts. |
| age/demographics | ABSENT in this release (geography only) | AGE; SEX; EDUCATION; MARRIAGE | No | This LC granting release has no age/sex/education/marriage fields. |
| credit utilization | ABSENT | BILL_AMT* with LIMIT_BAL (constructable; not a native field) | No | No LC utilization field in this release; UCI utilization would be derived and was not created here. |
| payment history | ABSENT as monthly payments | PAY_AMT1-PAY_AMT6 and PAY_0, PAY_2-PAY_6 | No | UCI is a 6-month revolving payment history; this LC release excludes servicing fields by design. |
| financing purpose | purpose; title; desc | ABSENT | No | UCI has no loan-purpose or borrower-description fields. |
| time | issue_d | No per-row timestamp; April-September 2005 encoded as column groups | No | LC has a loan-level approval month. UCI is a single study window, not a panel of origination dates. |
| geographic information | addr_state; zip_code | ABSENT | No | UCI has no geography fields. Populations are US vs Taiwan. |
| application-time availability | Depositor-selected granting/application subset (with issue_d and experience_c caveats) | Snapshot of existing revolving-account behaviour plus demographics | No | LC features are (claimed) origination-application attributes for issued P2P loans. UCI features are performance of already-issued credit cards. Not the same decision point. |

## Semantically similar but not equivalent

- Default vs default payment next month look like generic 'default' labels but differ in product, horizon, and population.
- loan_amnt vs LIMIT_BAL are both size-of-credit numbers but request vs revolving limit.
- fico_n vs PAY_* are both 'credit history' only at a slogan level.
- revenue vs AGE/SEX are both applicant descriptors but not substitutes.

## Conclusion

UCI supports `GENERALIZATION_OF_METHOD` (can the same evidence-separated audit/decision pipeline be applied to a second tabular credit-default dataset?).

UCI does **not** support `DIRECT_DOMAIN_TRANSFER`. Nothing in the schemas, populations, products, timestamps, or purpose fields justifies treating UCI as a LendingClub domain replica.
