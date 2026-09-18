# Shariah-oriented governance methodology

**Amendment:** `AMENDMENT-SHARIAH-001`  
**Status:** `APPROVED`  
**Approval date field:** `[APPROVAL DATE — RESEARCH OWNER]`  
**Full controlling text:** `docs/amendments/AMENDMENT-SHARIAH-001.md`

This document is the operational methodology boundary. It does **not** replace the full amendment. It **does** distinguish what is already in the repository from what is approved but not yet implemented.

| Gate | Status |
| --- | --- |
| Amendment approved | **Yes** |
| Stage 7 remediation (L1/L2) | **Implemented** — see `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md` |
| Stage 8 remediation (per-row governance / fusion) | **Implemented** — see `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md` |
| Stage 9 | **Blocked** |

This layer is a Shariah-oriented **governance and evidence-traceability** prototype. It is **not** a Shariah authority, **not** a certification mechanism, and **not** `EXPERT_VALIDATED`.

---

## Current implemented state

The following describes the repository after Stage 8 v2. Stage 9 remains blocked.

### Stage 8 v2 (current decision fusion)

- Frozen Stage 8 v1 thresholds (`t_low=0.06`, `t_high=0.69`) and the frozen governance matrix are reused. Thresholds are not re-selected.
- Each application is extracted and evaluated through Stage 7 v2 L2 with `evaluation_mode=PER_APPLICATION`.
- L1 remains dataset context (`INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`), not an applicant-level ruling.
- Stage 8 v1 broadcast fusion remains historical evidence.

### Stage 7 v2 (current Shariah integration)

- L1 dataset/integration readiness is implemented. LendingClub L1 = `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`. This is **not** an applicant-level ruling.
- L2 per-application extraction/evaluation is implemented in `src/shariah/l1.py` and `src/shariah/l2.py`.
- LendingClub L2 evidence does not include firewall fields. `purpose` is not used as contract type.
- `evaluation_mode = PER_APPLICATION`. Each result has a privacy-safe `record_reference_hash` and an `evidence_hash`.
- Stage 7 v2 report/audit live at `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md` and `audit/stage7_v2_governance_run.json`.
- Stage 8 v2 per-row fusion: `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`.

### Stage 7 v1 (historical, implemented)

- A deterministic governance engine exists under `src/shariah/*`.
- Executable research-architecture controls: `SH-ARCH-001` (contract identification), `SH-ARCH-003` (credit-field firewall).
- Executable source-mapped controls: `SH-SBP-*`, `SH-SECP-*`.
- Executable AAOIFI **identity / unavailability gates**: `SH-AAOIFI-SS8-GATE`, `SH-AAOIFI-SS9-GATE`.
- Documented non-executable gap: `SH-AAOIFI-SS8-POSSESSION` (`NOT_VERIFIED`; cannot execute).
- Synthetic evidence-sensitive cases exist. They are not LendingClub rows.
- Stage 7 v1 report, audit, and `results/shariah/*` remain **historical evidence**. Gate `STAGE_7_STATUS = PASS` in that report is the **historical run status**, not a claim that the approved L1/L2 architecture was already implemented.

### Stage 8 v1 (historical, implemented)

- Frozen Platt-calibrated EBM probabilities were fused with a **single LendingClub dataset profile** (`contract_type=unknown`, `institution_class=lendingclub_application`, no credit fields).
- That one `INSUFFICIENT_INFORMATION` result was **broadcast** onto test rows. This is **not** per-application L2 evaluation.
- `purpose` was **not** passed into the governance engine.
- Validation-selected thresholds remain frozen (`t_low` / `t_high` from a **credit-only**, **validation-only** objective).
- Stage 8 v1 report, audit, and `results/decision/*` remain **historical evidence**.

### What is **not** currently implemented

- Stage 9 robustness/ablation experiments.
- Any purpose classifier.
- Any mapping of `purpose` / `title` / `desc` to Murabahah, Ijarah, or other Islamic contract types.
- Any AAOIFI SS(8)/SS(9) **operative clause** engine.
- Any `EXPERT_VALIDATED` rule.

### `SHR-001`

`SHR-001 = UNSUPPORTED / RETIRED`.

The identifier is recorded as retired in the rule catalog metadata and source registry. It is **not** an executable rule. Its historical wording is **not** reconstructed. `SH-ARCH-001` and `SH-ARCH-003` are **not** `SHR-001`.

---

## Approved future implementation requirements

These requirements are **approved** by `AMENDMENT-SHARIAH-001`. L1/L2 and Stage 8 v2 per-row fusion are now implemented. Remaining items (Stage 9, purpose classifiers, AAOIFI operative clauses, `EXPERT_VALIDATED` rules) are **not** claimed as already built.

### Design A; Design B rejected

- **Adopt Design A:** contract-level / institutional-product governance.
- **Reject Design B:** application-purpose screening as Islamic-contract classification.
- No mapping of the form `car → Ijarah`, `home_improvement → Murabahah`, or any equivalent.

### LendingClub evidence-gap scope

LendingClub is a conventional historical application dataset. It can demonstrate an **evidence-gap / governance-readiness limitation**. It **cannot** establish applicant-level Shariah compliance.

### Purpose / title / desc ban

`purpose`, `title`, and `desc` are **not** Shariah evidence. They must not enter the Shariah evidence object. `purpose` remains a frozen **credit** predictor. `title` and `desc` remain reserved text fields under the Stage 3 text-feature policy; reservation is **not** current Shariah evidence.

### L1 / L2 architecture (Stage 7 v2 implemented; Stage 8 v2 consumes L2 per row)

- **L1** (once per dataset/integration): dataset/schema readiness. LendingClub L1 identifier: `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`.
- **L2** (per application): evaluate the governance evidence object **derived from that row**.
- Identical L2 statuses are acceptable. Identical unevaluated payloads presented as independent inspections are **not**.
- Broadcast-as-inspection is **not** permitted after Stage 8 remediation.
- Hash caching is allowed only with per-row audit fields and `evaluation_mode = PER_APPLICATION`.

### Credit / Shariah firewall

These fields must not enter the Shariah evidence object except as a deliberate boundary-test `extra` injection: `fico_n`, `loan_amnt`, `dti_n`, `revenue`, `emp_length`, `home_ownership_n`, `addr_state`, `zip_code`, `purpose`, `title`, `desc`, `id`, `issue_d`, `experience_c`, `Default`.

If injected, `SH-ARCH-003` is a **boundary violation** check, not religious evidence.

### Rule-family distinction (frozen)

| Family | Meaning |
| --- | --- |
| `SH-ARCH-*` | Research architecture controls (not religious rulings) |
| `SH-SBP-*` / `SH-SECP-*` | Source-specific operational mappings (`SOURCE_VERIFIED_PENDING_EXPERT_REVIEW`) |
| `SH-AAOIFI-*-GATE` | Identity / unavailability gates; **not** clause engines |
| `SHR-001` | `UNSUPPORTED / RETIRED` — do not reconstruct |

No unsupported religious rule may be introduced.

### AAOIFI

Identity verification and unavailability gates may remain. **Clause-level implementation remains blocked** until authoritative operative text is available and appropriately reviewed. Do not invent clauses, do not treat secondary reproductions as primary text, and do not classify contracts from identity pages.

### Expert-validation states

| Status | Use |
| --- | --- |
| `RESEARCH_ARCHITECTURE_NOT_A_RULING` | Architecture / firewall / refusal to invent unavailable clauses |
| `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW` | Retrieved SBP/SECP operational text |
| `EXPERT_VALIDATED` | Only with a documented expert record. **Do not fabricate.** None exists. |
| `IDENTITY_VERIFIED_CLAUSES_NOT_VERIFIED` | AAOIFI identity-only sources |

### Certification boundary

The system must not output “Shariah compliant” (or equivalent) as an automated determination. Human review is not certification.

### Stage 7 consequences

Stage 7 v2 L1/L2 is implemented. Existing engine/catalog/synthetic cases remain the starting point. No new religious rules were added. Stage 7 v1 artifacts are preserved.

### Stage 8 consequences (implemented as v2)

Stage 8 v2 remediates governance integration, fusion representation, and audit claims. Credit model, calibration, validation-selected thresholds, split, and Stage 6 explainability remain frozen. Stage 8 v1 is preserved. Thresholds were not re-selected on TEST.

### TEST protection

TEST is not used for methodology decisions or threshold selection. No TEST rows were selected for this amendment.

### Stage 9 block

Stage 9 remains **blocked**. Stage 8 v2 does not authorize Stage 9.

### Paper-claim and novelty boundaries

Safe / not-safe claims and the novelty position are those frozen in `AMENDMENT-SHARIAH-001` sections 8–9. This is methodology / governance-informatics research, not a new credit-learning algorithm and not Islamic legal scholarship.
