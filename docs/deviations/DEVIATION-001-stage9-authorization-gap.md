# DEVIATION-001 — Stage 9 authorization-process gap

| Item | Value |
| --- | --- |
| **Deviation ID** | `DEVIATION-001` |
| **Title** | Stage 9 authorization-process gap |
| **Record date** | 2026-09-15 |
| **Record type** | Historical / process deviation |
| **Constitution basis** | Rule #14 (document methodology and process changes). This file is **not** a Rule #14 scientific-method amendment and is **not** retroactive authorization. |
| **Status** | `RECORDED — PENDING RESEARCH-OWNER REVIEW` |
| **Approval** | **Not claimed.** No owner-approval date is recorded. None is invented. |
| **Does not authorize** | Stage 9.2, Stage 9.3, Stage 9.4, Stages 9.5–9.7, paper confirmatory use of 9.2/9.3 |

This was a process deviation, not a scientific error.

---

## A. Summary

### Historical facts

1. `audit/stage9_0_experimental_freeze.json` (`execution_timestamp` `2026-09-15T16:34:17+00:00`) records `stage9_execution`: `"NOT AUTHORIZED"` and `experiments_executed`: `false`. That freeze file is **not** edited by this deviation and remains historically accurate.

2. `RESEARCH_CONSTITUTION.md`, as of the Stage 9.0 freeze and through Stage 9.3 execution, stated that Stage 9 remained blocked and that Stage 8 v2 does not authorize Stage 9. The historical meaning of that sentence is **not** rewritten by this record.

3. The only Rule #14 amendment listed at that time was `AMENDMENT-SHARIAH-001` (`docs/amendments/AMENDMENT-SHARIAH-001.md`), which controls Stage 7/8 and states that Stage 9 is blocked until that amendment is implemented and verified. It does **not** authorize Stage 9.1, 9.2, or 9.3.

4. Stage 9.1 (`stage9_1_ablation_lc_v1`) was executed after a chat instruction from the research owner authorizing Stage 9.1 only. The repository freeze JSON and constitution did not contain a corresponding formal prospective authorization record. The Stage 9 protocol execution-gate text was later edited by the Stage 9.1 executor during that stage. Chat instruction is not a dated amendment file. A command having been run is not owner approval.

5. Stage 9.2 (`stage9_2_cost_sensitivity_lc_v1`; audit `started` `2026-09-15T18:08:19+00:00`) and Stage 9.3 (`stage9_3_governance_sensitivity_lc_v1`; audit `started` `2026-09-15T18:22:31+00:00`) were executed while the frozen protocol execution gate still stated that Stages 9.2–9.7 remain unauthorized, and while `audit/stage9_0_experimental_freeze.json` still recorded `stage9_execution`: `"NOT AUTHORIZED"`. No Stage 9 execution amendment existed. The protocol was not prospectively updated before those runs.

### Classification (authorization, not PASS/FAIL of science)

| Stage | Authorization classification |
| --- | --- |
| Stage 9.1 | **B. AUTHORIZED WITH DOCUMENTATION GAP** |
| Stage 9.2 | **C. UNAUTHORIZED BUT SCIENTIFICALLY VALID POST-FREEZE ANALYSIS** |
| Stage 9.3 | **C. UNAUTHORIZED BUT SCIENTIFICALLY VALID POST-FREEZE ANALYSIS** |

Stage 9.1 was executed following a chat instruction from the research owner, but the repository's frozen Stage 9 protocol/constitution did not contain a corresponding formal prospective authorization record.

Stage 9.2 and Stage 9.3 were executed without frozen-protocol execution-gate authorization.

### Technical audit findings (not new scientific claims)

The technical audit independently found that Stage 9.1–9.3 were technically supported by frozen inputs and did not:

- retrain models,
- refit calibration,
- select thresholds using the LC TEST set,
- modify Stage 8 policy/results,
- introduce new Shariah rules,
- fabricate expert validation,
- fabricate results.

This was a process deviation, not a scientific error.

---

## B. No retroactive authorization

**No retroactive authorization is being claimed.**

Specifically:

- `audit/stage9_0_experimental_freeze.json` is **NOT** being edited to make it appear that Stage 9.2 or Stage 9.3 were authorized in advance.
- `RESEARCH_CONSTITUTION.md` is **NOT** being rewritten to make it appear that Stage 9.2 or Stage 9.3 were authorized in advance.
- Both historical records remain historically accurate as-is.

Nothing in this file backdates owner approval, expert validation, or execution-gate authorization. `DEVIATION-001` does not convert classification C into classification A.

---

## C. Treatment of Stage 9.2 and Stage 9.3

Stage 9.2 and Stage 9.3 are permanently retained as:

**EXPLORATORY / SENSITIVITY ANALYSIS**

Any future paper draft must label them exactly in this category.

Example publication-safe wording:

> post-freeze sensitivity analysis, not part of the pre-registered Stage 9 confirmatory protocol

**No retrospective ratification is being sought.**

Do not convert 9.2 or 9.3 into confirmatory/pre-registered evidence.

Artifacts already written under `results/cost_sensitivity/`, `results/governance_sensitivity/`, `docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md`, `docs/STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md`, and the corresponding `audit/stage9_2_*` / `audit/stage9_3_*` files are **preserved**. This deviation does not regenerate, overwrite, or scientifically reinterpret those numbers.

---

## D. Evidentiary basis

No standalone `docs/` markdown titled “Stage 9 authorization audit” exists in the research repository. This deviation therefore cites **existing repository artifacts** plus the workspace evidence canvas produced in the prior audit-only task:

| Kind | Path | Role |
| --- | --- | --- |
| Historical freeze | `audit/stage9_0_experimental_freeze.json` | Gate at freeze: execution not authorized |
| Historical protocol | `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` | Scientific freeze; prior execution-gate wording |
| Historical constitution | `RESEARCH_CONSTITUTION.md` | Stage 9 blocked by Stage 8 v2; Rule #14 table |
| Stage 9.1 machine manifest | `audit/stage9_1_ablation_run.json` | What 9.1 wrote after execution |
| Stage 9.1 report | `docs/STAGE_9_1_ABLATION_REPORT.md` | Report-only (not a raw terminal log) |
| Stage 9.2 machine manifest | `audit/stage9_2_cost_sensitivity_run.json` | What 9.2 wrote after execution |
| Stage 9.2 report | `docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md` | Report-only |
| Stage 9.3 machine manifest | `audit/stage9_3_governance_sensitivity_run.json` | What 9.3 wrote after execution |
| Stage 9.3 report | `docs/STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md` | Report-only |
| Prior audit presentation (workspace, not a Stage 9 experiment result) | Cursor canvas `stage9-execution-evidence-audit.canvas.tsx` | Evidence-recovery presentation from the audit-only task |

Authorization classifications B and C above are the **treatment decision** recorded here. They are not new experimental results.

Distinction:

- **Historical facts:** freeze JSON, constitution wording at the time, protocol execution gate, experiment IDs and timestamps in Stage 9.1–9.3 audits.
- **Technical audit findings:** frozen-input consistency, no retraining/refit/TEST selection/Stage 8 mutation/new Shariah rules/fabricated expert validation, as already recorded in those audits and the prior audit-only review.
- **Treatment decision:** 9.1 = B; 9.2/9.3 = C and exploratory/sensitivity only; no retroactive authorization.

Original raw terminal logs for Stage 9.1–9.3 were not found in the repository (`NO ORIGINAL RAW TERMINAL LOG FOUND`).

---

## E. Status

This is a historical/process deviation record.

This document does **not** claim that the deviation has been retroactively approved.

Owner-review status: `RECORDED — PENDING RESEARCH-OWNER REVIEW`.

Related document (not this deviation): `docs/amendments/AMENDMENT-STAGE9-4-AUTHORIZATION.md` (status `APPROVED`, approval date 2026-09-15). That amendment does not ratify Stage 9.2 or Stage 9.3.

---

## Stage 9.4 — Model-scope expansion

AMENDMENT-STAGE9-4-AUTHORIZATION approved scope: Logistic Regression, EBM.
Actual Stage 9.4 execution added XGBoost without a dated successor amendment.

Classification: C. UNAUTHORIZED BUT SCIENTIFICALLY VALID POST-FREEZE ANALYSIS
(same category and same reasoning as Stage 9.2/9.3 — technically supported,
no TEST leakage, no retraining outside protocol, but executed outside the
approved written scope).

Decision (final, not to be revisited without explicit research-owner
instruction): the XGBoost result on UCI is RETAINED PERMANENTLY as an
EXPLORATORY EXTENSION, not elevated to confirmatory/pre-registered status.
No retroactive or prospective ratification is being sought for this specific
expansion, consistent with the treatment already applied to Stage 9.2/9.3.

Report the UCI model-selection finding exactly as observed, labeled by
provenance:

* Logistic Regression, EBM: PRE-REGISTERED SCOPE (per
  AMENDMENT-STAGE9-4-AUTHORIZATION)
* XGBoost: EXECUTION-TIME EXPANSION, EXPLORATORY, retained per this
  deviation entry

The actual finding was: EBM had the better raw Brier score; XGBoost had the
better PR-AUC; the declared selection rule (PR-AUC first) selected XGBoost.
This selection rule was therefore applied to a model that was itself outside
pre-registered scope, so the "selected model" label must be read as
exploratory, not as the protocol's pre-registered confirmatory outcome.

The original `docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md` numbers are not
modified by this deviation entry.
