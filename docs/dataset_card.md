# Preliminary Dataset Card

This card does not describe either dataset as Islamic, Shariah-compliant, or representative of Islamic financing markets.

## LendingClub granting-model dataset

- Dataset name: Lending Club loan dataset for granting models
- Source: Zenodo
- DOI/URL: 10.5281/zenodo.11295916 / https://doi.org/10.5281/zenodo.11295916
- License: cc-by-4.0
- Dataset role: PRIMARY_CREDIT_RISK_DATASET
- Target: `Default` (documented 0=fully paid, 1=defaulted; original loan_status mapping has a documentation conflict)
- Row count: 1347681
- Feature count (columns including target and identifiers): 15
- Temporal availability: `issue_d` present; documented as approval month/year; range 2007-06-01 to 2018-12-01
- Missingness summary: high-missingness columns = ['desc']; full table in `results/tables/lendingclub_missingness.csv`
- Known limitations: issued-and-resolved loans only (no rejected applications); transitory statuses excluded; depositor already filtered and cleaned; US P2P market 2007-2018 origin, not Islamic finance
- Privacy considerations: loan `id` is a direct identifier; `zip_code`/`addr_state`/`revenue` are quasi-identifiers; `title`/`desc` are free text (raw text not published here)
- Leakage concerns: `issue_d` as a feature; `experience_c` timing unverified; target is post-decision by definition
- Intended use: primary credit-risk architecture/evaluation dataset for this research project
- Prohibited/unsupported claims: not a Shariah-compliance dataset; not a full applicant funnel; not certified; not to be described as real-time underwriting data from an Islamic bank

## UCI Default of Credit Card Clients

- Dataset name: Default of Credit Card Clients
- Source: UCI Machine Learning Repository dataset 350
- DOI/URL: 10.24432/C55S3H / https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients
- License: CC BY 4.0
- Dataset role: SECONDARY_GENERALIZATION_DATASET
- Target: `default payment next month` (Yes=1 / No=0 default payment next month)
- Row count: 30000
- Feature count: UCI states 23 features; observed columns including ID and target = 25
- Temporal availability: no per-row timestamps; fixed 2005 payment window in column groups
- Missingness summary: UCI page states no missing values; observed any missing = False
- Known limitations: Taiwan credit-card clients; no financing purpose; not P2P origination; single-period study
- Privacy considerations: `ID` identifier; demographics present (SEX, EDUCATION, MARRIAGE, AGE)
- Leakage concerns: bill/payment history is contemporaneous account performance, not origination-application data for a new loan grant
- Intended use: methodological replication / pipeline generalization, not domain transfer
- Prohibited/unsupported claims: not Islamic finance; not equivalent to LendingClub; not a basis for combining applicant records
