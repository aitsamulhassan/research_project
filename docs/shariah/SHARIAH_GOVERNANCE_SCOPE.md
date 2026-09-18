# Shariah-oriented governance scope

Methodology control: `AMENDMENT-SHARIAH-001` (`APPROVED`). Full text: `docs/amendments/AMENDMENT-SHARIAH-001.md`. Operational boundary: `docs/shariah_methodology.md`.

This file describes the **implemented** Stage 7 engine scope. L1/L2 extraction is implemented in Stage 7 v2. Stage 8 per-row fusion is **not** implemented.

## Purpose

This layer is a **Shariah-oriented governance / evidence-traceability prototype**. It screens whether a proposed financing representation contains conditions that, under **verified** public rules, require:

- PASS
- REVIEW
- NOT_STRUCTURABLE_WITHOUT_REDESIGN
- INSUFFICIENT_INFORMATION

It is **not** a Shariah authority, **not** a generic Islamic classifier, and **not** a certification mechanism.

## Terminology

Use: Shariah-oriented governance layer; Shariah-aware governance layer; Shariah-oriented rule-based screening.

Do not use “Shariah-certified”, “Shariah-compliant”, “halal loan”, or “haram loan” as outputs of this engine.

PASS means only that **available evidence did not trigger a configured, verified governance concern**. It does not mean the financing is religiously approved.

## Evidence separation

Credit-risk evidence, calibration evidence, explainability/SHAP evidence, and this governance layer remain independent. Shariah rules are not credit features. SHAP does not determine rulings. The credit model does not modify rules.

## Scope

Implemented operational mappings are limited to:

1. Pakistani **Islamic Banking Institution** product-governance requirements in SBP SGF 2025 (prior Shariah Board approval of products and of process flows/agreements).
2. Pakistani IBI **Murabaha** invoice and payment instructions in SBP IBD Circular 01 of 2012.
3. SECP SGR 2023 Regulation 7(2) when a **security** is claimed to be Shariah compliant (not SBP banks).
4. Methodological gates: unknown/ambiguous contract type; refusal to invent AAOIFI SS (8)/SS (9) clauses; LendingClub credit fields are not Shariah variables.

Murabahah rules do **not** automatically apply to Ijarah, Musharakah, Mudarabah, Qard, Salam, or Istisna.

## Non-certification status

No applicant, including any LendingClub borrower, is described as Shariah compliant on the basis of this system. Qualified Shariah experts have **not** validated the machine interpretation.

## Limitations

LendingClub application attributes do not reconstruct Islamic contract mechanics. Missing information yields INSUFFICIENT_INFORMATION, never PASS.
