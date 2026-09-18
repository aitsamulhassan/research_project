# AMENDMENT-SHARIAH-001

Permanent Constitution Rule #14 methodology record.

This file is the controlling methodology decision for the upcoming Stage 7/8 Shariah-governance remediation. Recording this amendment does **not** implement that remediation.

| Item | Value |
| --- | --- |
| **Amendment ID** | `AMENDMENT-SHARIAH-001` |
| **Constitution basis** | Rule #14: Document every methodology change |
| **Approval date** | `[APPROVAL DATE — RESEARCH OWNER]` |
| **Status** | `APPROVED` |
| **Affected stages** | Stage 7, Stage 8 |
| **Stage 9** | **Blocked** until this amendment is implemented and verified |
| **Does not affect** | Frozen EBM, frozen feature set, frozen temporal split, frozen Platt calibrator, frozen validation-selected thresholds, Stage 6 explainability artifacts |
| **Approver** | Research owner (identity **not** fabricated in this record) |
| **Expert sign-off** | None. This amendment is methodological. It is **not** expert Shariah validation |
| **Implementation of L1/L2 / Stage 7–8 remediation** | Stage 7 v2 L1/L2 **implemented**. Stage 8 v2 per-row fusion **implemented**. Stage 9 **blocked**. |

---

## 1. Purpose

This amendment records a **methodology clarification and freeze** after Pre-Stage 9 diagnostic `CATEGORY D` and the approved Stage 7–8 remediation design.

It exists so that later implementation cannot silently:

- treat a **broadcast dataset profile** as 208,886 independent Shariah inspections;
- treat LendingClub `purpose` / `title` / `desc` as Islamic-contract evidence;
- reconstruct unsupported identifier `SHR-001`;
- implement AAOIFI SS(8)/SS(9) **operative clauses** without verified primary text.

It does **not** change credit modelling, calibration, or threshold **selection** rules.

---

## 2. Previous implementation state

*(Engineering / representation state. Not a religious finding.)*

**Stage 7** implemented a Shariah-oriented **governance engine** with:

- research-architecture rules `SH-ARCH-001` (contract identification) and `SH-ARCH-003` (credit-field firewall);
- source-mapped SBP SGF / IBD Circular 01 of 2012 and SECP SGR 2023 operational rules, labeled `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW`;
- AAOIFI SS(8)/SS(9) **identity** sources and **unavailability gates**, not clause engines;
- synthetic, evidence-sensitive test cases (not LendingClub rows).

**Stage 8** fused frozen Platt-calibrated EBM probabilities with a **single** LendingClub **dataset profile** (`contract_type=unknown`, `institution_class=lendingclub_application`, no credit fields) and **broadcast** that one `INSUFFICIENT_INFORMATION` status onto every test row. Cost-sensitive `t_low` / `t_high` were selected on **validation** from a **credit-only** objective.

Identifier `SHR-001` did **not** appear as an implemented rule in the repository (constitution, catalogs, sources, code, tests, or reports) prior to this amendment. This record marks it `UNSUPPORTED_RETIRED` without reconstructing historical wording.

Stage 7 v1 and Stage 8 v1 reports and audits remain **historical evidence**. They are not rewritten to imply that L1/L2 or per-row governance existed at the time of those runs.

---

## 3. Methodological problem discovered

The diagnostic established **multiple issues**, not a single Shariah conclusion:

1. **Broadcast representation.** Stage 8 called the engine **once** and copied the result. That is an **integration design**, not evidence that 208,886 applications were independently evaluated. Uniform `INSUFFICIENT_INFORMATION` was **over-determined**: the payload never contained contractual fields, and `purpose` was never passed.

2. **Risk of false scientific claim.** Reporting “all test rows are `INSUFFICIENT_INFORMATION`” without stating **broadcast vs per-row** can be read as applicant-level Shariah screening. That reading is **not** licensed by the implementation.

3. **Unsupported purpose→contract inference.** Using `purpose` (e.g. `car`, `home_improvement`) as Murabahah/Ijarah evidence would be an **unverified religious/legal inference**. AAOIFI operative clauses were **not** retrieved. `purpose` is a frozen **credit** predictor.

4. **`SHR-001`.** An owner-side identifier was **not** found in-repo as an implemented rule. Reconstructing it would violate “do not invent rules / do not invent clauses.” Constitution #14 requires documenting this gap rather than silently substituting `SH-ARCH-*` under the old name.

5. **Broadcast is not itself a Shariah finding.** The Shariah-relevant finding is: **this conventional dataset’s schema lacks the contractual evidence the engine is specified to use.** How that finding was **attached** to rows is an audit/architecture defect to correct.

---

## 4. Corrected methodology (frozen; approved)

### 4.1 Shariah layer — formal scope

The project implements:

> A **Shariah-oriented governance and evidence-traceability layer** that evaluates **verified contractual and institutional evidence** where such evidence exists.

It is **not**:

- a Shariah-compliance classifier;
- a halal/haram classifier;
- a Shariah score or weighted fusion with credit probability;
- a religious ruling engine;
- a certification mechanism;
- a substitute for a qualified Shariah scholar or Shariah supervisory board.

`PASS` means only that **configured, in-scope, executable rules did not raise a concern on the evidence object supplied**. It does **not** mean the financing is religiously approved.

### 4.2 Design A adopted; Design B rejected

**Design A (frozen):** contract-level / institutional-product governance.

**Design B (rejected):** application-purpose screening as Islamic-contract classification.

No mapping of the form `car → Ijarah`, `home_improvement → Murabahah`, `renewable_energy → …`, `small_business → …`, or any equivalent, is part of the executable methodology.

### 4.3 LendingClub role

LendingClub is a **conventional historical lending/application dataset**.

It does **not** provide the contractual/product-governance evidence required by this methodology (verified contract type, SB product/process approval, Murabaha invoice/payment path, SECP security-certificate evidence, AAOIFI clause-level possession/sequence evidence, etc.).

Therefore:

> LendingClub can demonstrate an **evidence-gap / governance-readiness limitation**, but **cannot** establish applicant-level Shariah compliance.

The study **must not** claim that LendingClub applicants were Shariah-screened, or that applications are Islamic or non-Islamic **merely** from dataset fields.

### 4.4 Purpose / text ban (frozen)

`purpose` is a **credit / application-purpose** field. It **must not** be interpreted as:

- contract type;
- Murabahah evidence;
- Ijarah evidence;
- asset-ownership evidence;
- possession evidence;
- Shariah-compliance evidence.

`title` and `desc` are **not currently** Shariah evidence. They may be reconsidered **only** through a **future** Constitution #14 amendment with **authoritative source support** and **appropriate expert review**. Until then, they must not enter the Shariah evidence object.

Creating a purpose classifier would be an **unsupported religious/legal inference**, not a source-grounded rule.

### 4.5 Two-level governance architecture (frozen)

**L1 — Dataset / integration readiness** (once per dataset/integration context)

> Does this dataset/schema contain the evidence necessary for **applicant-level** Shariah governance evaluation?

LendingClub L1 identifier (frozen for this amendment):

```text
INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION
```

This is **dataset-level**. It is not a per-applicant religious ruling.

**L2 — Application evidence evaluation**

> Given the **governance evidence object derived from that specific application**, what can the engine determine?

Input must be built **from that row**. For LendingClub, L2 may remain `INSUFFICIENT_INFORMATION` because contractual fields are absent.

**Identical L2 statuses are acceptable. Identical unevaluated payloads presented as independent inspections are not.**

Broadcast of a single profile **as if** each application had been evaluated is **not** permitted after implementation of this amendment.

Deterministic **caching by evidence-object hash** is allowed only if each row still stores its own `record_reference_hash`, evidence hash, missing-evidence list, and `evaluation_mode = PER_APPLICATION`.

Stage 7 v2 implements L1/L2 in `src/shariah/l1.py` and `src/shariah/l2.py`. Stage 8 v2 implements per-row fusion in `src/decision/stage8_v2.py` and `experiments/stage8_decision/run_stage8_v2.py`. Stage 8 v1 broadcast remains historical.

### 4.6 Credit / Shariah firewall (frozen)

The following **must not** enter the Shariah evidence object (except a **deliberate** `extra` injection in a **boundary test**):

`fico_n`, `loan_amnt`, `dti_n`, `revenue`, `emp_length`, `home_ownership_n`, `addr_state`, `zip_code`, `purpose`, `title`, `desc`, `id`, `issue_d`, `experience_c`, `Default`.

If injected for a test, existing architecture rule **`SH-ARCH-003`** treats this as a **governance-boundary violation** (`REVIEW` on that check), not as religious evidence.

Credit evidence remains for: prediction, probability, calibration, and **decision policy**.
Shariah governance evidence remains: contract type, institution scope, SB approvals, invoice/payment/advisor-exception fields, security claim and certificate — **conditionally**, only when the applicable contract/institution/regulatory scope requires them. This amendment does **not** make every listed field universally required.

### 4.7 `SHR-001` retirement (frozen)

`SHR-001` is **UNSUPPORTED / RETIRED** in this repository and **will not be reconstructed**.

This amendment does **not** recreate its wording, infer its historical contents, or relabel `SH-ARCH-001` or `SH-ARCH-003` as `SHR-001`.

Any earlier owner-side intention of the form **purpose → asset-backed Murabahah/Ijarah classification** is **not** part of the executable methodology unless independently restored by a **later**, source-grounded, expert-reviewed #14 amendment.

The project adopts:

- `SH-ARCH-*` for **research-architecture** controls;
- source-specific IDs (`SH-SBP-*`, `SH-SECP-*`, `SH-AAOIFI-*-GATE`) for implemented mappings/gates;
- **no** unsupported `SHR-001`.

### 4.8 AAOIFI methodology (frozen)

**Allowed now**

- SS(8) / SS(9) **identity** verification;
- explicit **unavailability / identity gates** stating that **operative clauses** were not verified from authoritative primary text.

**Not allowed now**

- implementing SS(8)/SS(9) operative clauses from memory;
- treating secondary reproductions as authoritative primary text;
- inventing clause mappings;
- purpose → contract classification from identity pages;
- claiming full AAOIFI implementation.

> Clause-level AAOIFI implementation remains **blocked** until authoritative operative text is available and appropriately reviewed.

This amendment does **not** claim that official text will become available.

### 4.9 Validation-state vocabulary (frozen)

| Status | Use |
| --- | --- |
| `RESEARCH_ARCHITECTURE_NOT_A_RULING` | Evidence separation, missing-evidence handling, contract-identification architecture, firewall, refusal to invent unavailable clauses |
| `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW` | Machine interpretation of **retrieved** SBP/SECP operational text |
| `EXPERT_VALIDATED` | **Only** with reviewer identity, qualification/scope, date, reviewed source, reviewed machine mapping, recorded opinion/sign-off. **Do not fabricate.** |
| `IDENTITY_VERIFIED_CLAUSES_NOT_VERIFIED` | AAOIFI identity-only sources |

No rule in the current repository is `EXPERT_VALIDATED`. This amendment does not change that.

### 4.10 Certification boundary (frozen)

The system **must not** output **“Shariah compliant”** (or equivalent) as an automated determination.

Human review **does not** automatically equal certification.

Formal Shariah certification remains **outside** current research scope unless separately established through appropriate authority.

---

## 5. Consequences for Stage 7

**Status: `REQUIRES REVISION`** (approved methodology; **not executed** in this documentation-only recording).

Stage 7 v1 (`docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT.md`, `audit/stage7_*`, `results/shariah/*`) remains **historical evidence**. Remediation, when authorized, will produce **versioned Stage 7 v2** artifacts. Do not silently overwrite v1.

Revised Stage 7 must:

1. document L1/L2;
2. document the evidence firewall;
3. document the purpose / `title` / `desc` ban;
4. document `SHR-001` retirement;
5. preserve AAOIFI identity/unavailability gates;
6. preserve source provenance;
7. distinguish architecture from religious rulings;
8. preserve expert-validation states;
9. retain synthetic **evidence-sensitive** testing;
10. add tests for **row-specific** governance extraction when implementation begins (two rows that differ only in `purpose` must yield **identical** Shariah evidence objects).

Stage 7’s existing engine, catalog families, and synthetic cases remain the **starting point**. This amendment does not authorize new religious rules.

---

## 6. Consequences for Stage 8

**Status: `REQUIRES REVISION`** of **governance integration, fusion representation, and audit claims**.

Stage 8 v1 (`docs/STAGE_8_DECISION_POLICY_REPORT.md`, `audit/stage8_*`, `results/decision/*`) remains **historical evidence**. Remediation, when authorized, will produce **versioned Stage 8 v2** artifacts. Do not silently overwrite v1.

**Not invalidated** by this amendment:

- frozen EBM and feature policy;
- frozen temporal split;
- calibrated probabilities (Stage 5);
- validation-selected thresholds and credit-only cost **assumptions**;
- monolithic **credit-policy** baseline definition;
- Stage 6 explainability results.

After L2 implementation is frozen, Stage 8 **governance/fusion/audit** artifacts require **one** regeneration on TEST. Existing thresholds **remain frozen** provided the selection objective remains **credit-only** and **validation-only**. No new threshold search on TEST.

---

## 7. Future implementation requirements (not done in this recording)

1. Owner **approved** this amendment (this record). Approval calendar date is `[APPROVAL DATE — RESEARCH OWNER]`.
2. Record it in the constitution / `docs/shariah_methodology.md` (this documentation-only task).
3. Implement L1 dataset readiness + L2 extractor that **does not** copy firewall fields. **Stage 7 v2 done.**
4. Stage 8: per-row `evaluate` (or hash-cached equivalent with per-row audit fields); stop broadcast-as-inspection. **Stage 8 v2 done.**
5. Tests: firewall, purpose-invariance, synthetic cases unchanged in religious content. **Stage 8 v2 tests added.**
6. Versioned Stage 7/8 reports and audits (`v2`); do not silently overwrite `v1` history. **Stage 7 v2 and Stage 8 v2 done.**
7. **One** fused TEST evaluation after freeze. **Executed once in Stage 8 v2 after unit/synthetic prerequisites.** See `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`.
8. Stage 9 stays **blocked**. Stage 8 v2 does not authorize Stage 9.

Development of extractor/schema/tests uses **synthetic/unit fixtures**. TEST is not used for methodology or threshold **selection**.

### Audit fields (Stage 8 v2)

Where appropriate: record reference/hash; dataset/integration readiness ID; evidence hash; `evaluation_mode`; governance status; completeness; missing evidence; triggered rule IDs; source IDs; expert-validation status; credit model version; calibrator version; threshold/policy version; final decision. No unnecessary raw identifiers (`id`, address, zip, free text) in published artifacts.

---

## 8. Paper claims frozen by this amendment

**SAFE**

- “The study implements a Shariah-oriented governance and evidence-traceability layer.”
- “The conventional LendingClub dataset lacks sufficient contractual evidence for applicant-level Shariah determination under the implemented governance schema.”
- “The architecture separates credit-risk evidence from Shariah-governance evidence.”

**NOT SAFE**

- “The system is Shariah-compliant.”
- “LendingClub applications were Shariah-screened.”
- “Loan purpose identifies the Islamic contract.”
- “AAOIFI requirements are fully implemented.”
- “The rules were validated by Shariah experts” — unless actual `EXPERT_VALIDATED` records exist (they do not).

**NOT SAFE without L2 + precise wording**

- Treating 208,886 identical statuses as 208,886 independent contractual inspections.

---

## 9. Novelty position (frozen)

Do **not** claim novelty from XGBoost, EBM, SHAP, calibration, or Islamic-finance terminology alone.

Defensible contribution language:

1. evidence-separated decision architecture;
2. separation of credit prediction from Shariah-oriented governance;
3. explicit governance evidence traceability;
4. calibrated and cost-sensitive decision policy under **stated research cost assumptions**;
5. refusal to manufacture religious evidence from ordinary credit fields;
6. empirical demonstration of an evidence gap in conventional lending data;
7. auditable handling of insufficient/uncertain governance evidence.

> This is **methodology / governance-informatics** research, **not** a new credit-learning algorithm and **not** Islamic legal scholarship.

---

## 10. Amendment impact matrix

| Artifact | Change required later? | Reason |
| --- | --- | --- |
| `RESEARCH_CONSTITUTION.md` | Yes (pointer in this recording) | Record Rule #14 amendment pointer/ID (constitution text itself need not grow into a full Shariah spec) |
| `docs/shariah_methodology.md` | Yes (this recording) | Replace Stage 0 stub with approved amendment scope; distinguish current vs future |
| Rule catalog | Yes (retirement record in this recording) | Document `SHR-001` unsupported/retired; do not add purpose rules; do not rename `SH-ARCH-*` |
| Source registry | Yes (pointer in this recording) | Provenance pointer to `AMENDMENT-SHARIAH-001` |
| Shariah engine (`src/shariah/*`) | Minimal — **not in this recording** | Core evaluate/completeness/gates remain; no clause invention |
| LC governance extractor | Yes — **not in this recording** | New L2 (and explicit L1); currently a constant profile in `decision_engine.py` |
| Stage 7 tests | Yes — **not in this recording** | Per-row extraction, purpose-invariance, firewall |
| Stage 7 report / `audit/stage7_*` / `results/shariah/*` | Yes later as **v2**; v1 preserved | Reflect frozen methodology; version rather than silent replace |
| Stage 8 integration (`run_stage8.py`, `apply_policy` usage) | Yes — **not in this recording** | Remove broadcast-as-inspection |
| Stage 8 audit / fused tables/figures/report | Yes later as **v2**; v1 preserved | Per-row evidence + L1 ID; one TEST fused pass after freeze |
| Credit model | No | Independent |
| Calibration | No | Independent |
| Thresholds | No | Validation-only, credit-only; remain frozen |
| Stage 6 explainability | No | Independent |
| Stage 9 | **BLOCKED** | Until Stage 7/8 remediation is implemented and verified |
| `docs/text_feature_policy.md` | Maybe later | Clarify reservation of `title`/`desc` ≠ current Shariah evidence (align with this ban). Not edited in this recording because that file is a Stage 3 generated artifact / feature-policy surface |
| Synthetic governance cases | No change of religious content | Keep evidence-sensitive cases; do not add purpose→contract cases |

---

## AMENDMENT APPROVAL CHECKLIST

Checked items record the research owner's approval of this methodology. The approval calendar date is **not** invented; it remains `[APPROVAL DATE — RESEARCH OWNER]`.

* [x] Design A approved
* [x] Design B / purpose classifier rejected
* [x] L1/L2 architecture approved
* [x] Credit/Shariah firewall approved
* [x] `SHR-001` retirement approved
* [x] AAOIFI clause-level implementation remains blocked
* [x] Expert-validation boundary approved
* [x] “Shariah compliant” output prohibited
* [x] Stage 7 revision required
* [x] Stage 8 revision required
* [x] Frozen credit model remains unchanged
* [x] Frozen calibration remains unchanged
* [x] Frozen thresholds remain unchanged
* [x] TEST remains protected
* [x] Stage 9 remains blocked

---

## FINAL STATUS

```text
AMENDMENT-SHARIAH-001 = APPROVED
```

```text
Approval date field = [APPROVAL DATE — RESEARCH OWNER]
Stage 7/8 remediation was not implemented in this recording.
Stage 7 was not rerun.
Stage 8 was not rerun.
No models were trained.
No thresholds were changed.
Stage 9 was not started.
```
