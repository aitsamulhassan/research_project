# M-9.4-AE Correction Log

| Item | Value |
| --- | --- |
| **Document ID** | `M9-4-AE-CORRECTION-LOG` |
| **Date** | 2026-09-16 |
| **Type** | Controlled documentation correction only |
| **Classification source** | `docs/paper/M9_4_AE_HUMAN_REVIEW.md` |
| **Scientific experiment** | **NONE** |

This log does **not** reopen Stage 9 or Stage 10 and does **not** change scientific numbers, models, datasets, calibration, thresholds, or frozen results.

---

## 1. Previous unsupported label

Placement-task STEP 9 phrasing (not a frozen Stage 9 artifact):

> M-9.4-AE = “UCI exploratory analysis context”

That phrase is **not** supported by `AMENDMENT-STAGE9-4-AUTHORIZATION`, `DEVIATION-001` (Stage 9.4 model-scope subsection), the drafting protocol, the evidence master, the evidence map, or the IEEE manuscript body.

---

## 2. Authoritative repository classification

From `docs/paper/M9_4_AE_HUMAN_REVIEW.md` and the frozen Stage 9 / drafting records it cites:

- **M-9.4-AE** = independent UCI logistic-regression + EBM methodology (approved written U1 scope).
- **M-9.4-X** = UCI XGBoost exploratory / `DEVIATION-001` (execution-time expansion).

---

## 3. Exact file(s) where the unsupported label was found

| Location | How the label appeared | Manuscript scientific claim? |
| --- | --- | --- |
| IEEE **placement-task instruction** (chat; not a repo science file) | “M-9.4-AE: UCI exploratory analysis context” | No |
| `docs/paper/IEEE_TEMPLATE_PLACEMENT_AUDIT.md` | Quoted the task phrase and left remaining-limitation item 9 as **left for human review** | No (workflow/placement audit) |
| `docs/paper/M9_4_AE_HUMAN_REVIEW.md` | Quoted the task phrase as the **issue under review** | No (review record; not a paper claim) |

**Not found** as an M-9.4-AE = exploratory classification in:

- `docs/paper/MANUSCRIPT_DRAFT.md`
- `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md`
- `docs/paper/IEEE_MANUSCRIPT.md`
- `docs/paper/IEEE_TEMPLATE_READY_MANUSCRIPT.md` (paper body)
- Stage 9 authorization/report artifacts

Those files already separate **M-9.4-AE** (independent methodology / approved written scope) from **M-9.4-X** (exploratory). Sentences of the form “Context **M-9.4-AE** (approved written scope) and **M-9.4-X** (exploratory)” attach “exploratory” to **X**, not to AE, and were **not** rewritten.

---

## 4. Exact file(s) changed

| File | Changed? |
| --- | --- |
| `docs/paper/IEEE_TEMPLATE_PLACEMENT_AUDIT.md` | **Yes** (workflow/placement audit only) |
| `docs/paper/M9_4_AE_CORRECTION_LOG.md` | **Created** (this file) |
| `docs/paper/MANUSCRIPT_DRAFT.md` | **No** |
| `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md` | **No** |
| `docs/paper/IEEE_MANUSCRIPT.md` | **No** |
| `docs/paper/IEEE_TEMPLATE_READY_MANUSCRIPT.md` | **No** |
| `docs/paper/M9_4_AE_HUMAN_REVIEW.md` | **No** (historical review retained) |
| `docs/amendments/AMENDMENT-STAGE9-4-AUTHORIZATION.md` | **No** |
| `docs/deviations/DEVIATION-001-stage9-authorization-gap.md` | **No** |
| Stage 9/10 reports, models, results, datasets, calibration, thresholds | **No** |

---

## 5. Exact nature of correction

**DOCUMENTATION CORRECTION ONLY** in `docs/paper/IEEE_TEMPLATE_PLACEMENT_AUDIT.md`:

- Recorded Human review performed = YES and Classification source = `docs/paper/M9_4_AE_HUMAN_REVIEW.md`.
- Stated current classification as:
  - M-9.4-AE = independent UCI logistic-regression + EBM methodology
  - M-9.4-X = UCI XGBoost exploratory / DEVIATION-001
- Withdrew the placement-task phrase “UCI exploratory analysis context” as the **current** label for M-9.4-AE (kept only as a named withdrawn workflow label).
- Closed remaining-limitation item 9 (“left for human review”).
- Added the required none/NO integrity fields (experiments, metrics, models, results, data, calibration, thresholds, Stage 9/10, TEST, citations, figures, tables, Shariah claims, scientific content).

No scientific methodology, number, table cell, figure, or citation was changed.

---

## 6. Confirmation: no scientific artifact changed

Scientific artifacts unchanged: evidence master, evidence map, IEEE manuscript, ready-manuscript paper body, Stage 9 amendment/deviation/reports, Stage 10 records, models, datasets, predictions, calibration, thresholds, frozen result files.

---

## 7. Confirmation: M-9.4-X remains the only exploratory UCI XGBoost extension

M-9.4-X remains the paper context for UCI XGBoost as `EXECUTION-TIME EXPANSION, EXPLORATORY`. No second UCI XGBoost exploratory context was added or merged with M-4B LendingClub XGBoost.

---

## 8. Confirmation: DEVIATION-001 remains associated with M-9.4-X

`DEVIATION-001` Stage 9.4 model-scope expansion remains attached to **UCI XGBoost (M-9.4-X)**. It is **not** reassigned to M-9.4-AE. (The same deviation file also historically records Stage 9.2/9.3 class C exploratory cost/governance analyses; those are not M-9.4-AE and were not edited.)

---

## Integrity after correction

- M-9.4-AE consistently described as independent UCI logistic-regression + EBM methodology in manuscripts and in the updated placement audit.
- M-9.4-X consistently described as exploratory UCI XGBoost / `DEVIATION-001`.
- No other scientific wording changed.
- Numerical values unchanged (not opened).
- Stage 9 = CLOSED; Stage 10 = CLOSED; TEST remains closed.
- experiments run = NONE.

Actual IEEE template placement was **not** started.
