# Rule provenance

Methodology control: `AMENDMENT-SHARIAH-001` (`APPROVED`). `SHR-001` is `UNSUPPORTED_RETIRED` and is not reconstructed. No rule is `EXPERT_VALIDATED`.

## Source hierarchy

1. **Tier 1** official AAOIFI identity pages; SBP circulars/frameworks; SECP SRO text.
2. **Tier 2** peer-reviewed scholarship — not used as executable authority in Stage 7.
3. **Tier 3** discovery only. Unofficial copies of AAOIFI standards were **not** used to implement clauses.

## Provenance fields

Every executable rule stores: authority, document, standard (where applicable), section, clause, page or NOT_VERIFIED, URL, version, access date, source statement, research interpretation, machine implementation, validation status.

## Interpretation versus implementation

These three layers are stored separately and must not be merged:

1. **Source statement** — quoted or tightly paraphrased from the retrieved document.
2. **Research interpretation** — how this study scopes that statement for a governance engine.
3. **Machine implementation** — the evaluator function name and boolean/tri-state logic.

## Expert-validation policy

Implemented Shariah-mapped rules are `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW`.

`EXPERT_VALIDATED` is allowed only when a documented qualified-expert review record exists. No such record exists in this repository. Tests fail if expert validation is asserted without that record.

Architecture gates are `RESEARCH_ARCHITECTURE_NOT_A_RULING` and are not religious rulings.
