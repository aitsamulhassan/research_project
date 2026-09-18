# Dataset Decision Memo

Stage 2 audit memo. Roles were not changed. No applicant-level merge was performed.

## A. Why is LendingClub the primary dataset?

The verified Zenodo release is a granting-model extract of issued LendingClub loans with a public credit-performance outcome, application-oriented features selected by the depositor, `issue_d`, and `purpose`. Observed size is 1347681 rows and 15 columns. That combination matches the assigned role `PRIMARY_CREDIT_RISK_DATASET` for an evidence-separated decision architecture study that needs a financing-purpose field and a temporal stamp. This does not make the data Islamic or Shariah-certified.

## B. Why is UCI used only as a methodological replication/generalization dataset?

UCI Default of Credit Card Clients is a 30,000-row Taiwan credit-card default table with demographics and six-month bill/payment history, no financing purpose, and no origination timestamp. It can test whether the same audit/evaluation *method* runs on a second credit-default table. It cannot stand in for US P2P origination or for Shariah-purpose governance.

## C. What research questions can each dataset legitimately answer?

- LendingClub (this release): questions about credit-risk prediction on *originated and resolved* US P2P loans using the depositor's application-time subset; questions about temporal ordering via `issue_d`; questions about whether a purpose field exists for a later decision-support layer.
- UCI: questions about whether the same pipeline/metrics/calibration/explainability *procedure* can be repeated on a different tabular default dataset.

## D. What questions can they NOT answer?

- Neither dataset answers questions about Islamic financing markets, Shariah compliance, or certified religious permissibility.
- LendingClub cannot answer reject-inference / full-application-funnel questions: rejected applicants are absent.
- LendingClub cannot answer questions requiring servicing fields the depositor removed (interest rate, grade, post-origination performance series).
- UCI cannot answer purpose-conditioned or origination-time P2P underwriting questions.
- Neither dataset provides entity-level linkage to the other.

## E. Can the two datasets be combined?

**Do not combine them into one applicant-level dataset.**

No legitimate applicant-level linkage key was found. Populations, products, geographies, time bases, and labels differ. If a later methodological proposal argues for a non-entity combination (for example, separate-task evaluation of the same code path), that is a methodology-review item. It was not implemented.

Observed row counts: LendingClub 1347681; UCI 30000.
