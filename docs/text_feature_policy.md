# Text Feature Policy

This policy covers LendingClub `title` and `desc` only. No text model is built in Stage 3.

## title

- Role: TEXT
- Primary credit model: excluded
- Retention: kept in the immutable raw file and in the frozen feature policy as a future experimental branch
- Timing: application-time borrower-provided request title (Zenodo; Stage 2 leakage audit)

## desc

- Role: TEXT
- Primary credit model: excluded
- Retention: kept as a future experimental branch even though Stage 2 found high missingness (91.162671%)
- Timing: application-time borrower-provided request description (Zenodo; Stage 2 leakage audit)

## Why text is not silently discarded

`purpose` is a coarse category. `title` and `desc` are the only finer borrower-provided purpose language in this release. They are application-time fields and are therefore in scope for later explainability work and for a later Shariah-oriented decision-support investigation. Silently dropping them would destroy that option and would violate the research constitution rule against silently removing inconvenient material. They are excluded from the Stage 3/4 primary credit-risk predictor set because this stage does not encode text and the owner did not approve a text model.

`purpose` remains a structured primary-model predictor. That is not a text model.

## Prohibited in this stage

- No embeddings, bag-of-words, TF-IDF, or LLM features
- No Shariah rule engine
- No publication of raw free-text values in reports
