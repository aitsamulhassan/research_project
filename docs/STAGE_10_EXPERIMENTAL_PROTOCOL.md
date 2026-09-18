# Stage 10 Experimental Protocol — Robustness and Controlled Ablation

**Status:** `STAGE 10 DESIGN COMPLETE — EXECUTION GATED`  
**Protocol ID:** `STAGE-10-PROTOCOL-2026-09-15`  
**Design date:** 2026-09-15  
**Stage 9:** **CLOSED FOR EXPERIMENTATION** (`docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md` is authoritative)  
**Controlling authorization:** `docs/amendments/AMENDMENT-STAGE10-AUTHORIZATION.md` (`APPROVED`, 2026-09-15)  
**This documentation edit does not execute Stage 10.**

```text
STAGE_10_DESIGN_STATUS = COMPLETE
STAGE_10_EXECUTION = AUTHORIZED FOR S10-I1-IDENTITY, S10-R1-YEAR, S10-A1-GAP, AND S10-A4-SIDEBYSIDE ONLY
  (controlling authorization: AMENDMENT-STAGE10-AUTHORIZATION, APPROVED 2026-09-15).
Stage 9 remains CLOSED. Stage 10 does not reopen Stage 9.
No new confirmatory TEST-set experiment is authorized.
```

**Not done by this document:** Stage 10 runners, configs, result files, figures, tests, amendments, constitution edits, Stage 9 result edits, Stage 10 execution, Stage 11, paper drafting.

---

## Design authority and inherited freeze

| Object | Binding source | Frozen value |
| --- | --- | --- |
| Constitution | `RESEARCH_CONSTITUTION.md` | Rules #1–#15; `AMENDMENT-STAGE9-4-AUTHORIZATION` `APPROVED` 2026-09-15; Stage 9 closed (constitution text not modified by this gate edit) |
| Stage 10 amendment | `docs/amendments/AMENDMENT-STAGE10-AUTHORIZATION.md` | `APPROVED` 2026-09-15; **controlling authorization** for the four activities below |
| Stage 9 closure | `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md` | Classification **B**; Stage 9 closed; 9.2/9.3 class **C** exploratory; 9.4 XGBoost class **C** exploratory |
| Stage 9.0 science freeze | `audit/stage9_0_experimental_freeze.json` | Historical `stage9_execution: NOT AUTHORIZED` — **not rewritten** |
| LC model | Stage 4B | EBM, seed 42 TRAIN-only for calibration map |
| LC calibrator | Stage 5 | Platt `a=1.1988263209549705`, `b=0.6697765046966161` |
| LC thresholds | Stage 8 | `t_low=0.06`, `t_high=0.69`, `t*=0.16` |
| Stage 8 v1 freeze SHA-256 | `results/decision/frozen_policy.json` | `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4` |
| Stage 8 v2 freeze SHA-256 | `results/decision/v2/frozen_policy.json` | `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b` |
| LC TEST `p_selected` SHA-256 | `results/calibration/test/ebm_seed42_calibrated.csv` | `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb` |
| Primary cost scenario | `docs/decision_cost_assumptions.md` | `FN:FP=5:1`, `C_FP=1`, `C_REVIEW=0.25*C_FP` (assumed, not institutional) |
| A0 / A1 / A3 / A4 | Stage 9.0 / 9.1 | **Not redefined** (Section 4) |
| UCI written model scope | `AMENDMENT-STAGE9-4-AUTHORIZATION` | Logistic Regression + EBM only |
| UCI XGBoost | `DEVIATION-001` | Permanently exploratory; no ratification sought |

Stage 10 **does not** repair Stage 9 documentation. It asks whether **principal empirical findings remain stable** under pre-specified robustness checks and controlled ablations.

**Stage 10 character (binding):**

* Stage 10 currently proposes **NO NEW CONFIRMATORY TEST-SET EXPERIMENT**.
* Stage 10 is primarily a **controlled documentation / robustness-analysis** phase using **already-frozen** evidence.
* Existing freeze-backed results from Stages **4B, 5, 8, 9.1**, and the **approved-scope** portion of **9.4** (Logistic Regression + EBM) retain their **original provenance**. They are not re-labeled by Stage 10.
* Stage 9.4 **XGBoost remains exploratory** and must **not** be elevated.
* **No post-hoc LendingClub TEST analysis may be called confirmatory**, including year-wise decision-mix cuts of already-unblinded TEST outputs.
* This protocol does **not** add replacement experiments merely to create a confirmatory Stage 10 section.

---

## Evidence classes (do not relabel after seeing numbers)

| Class | Meaning | May support a paper confirmatory claim? |
| --- | --- | --- |
| **1. CONFIRMATORY / FREEZE-BACKED** | Already produced under a frozen protocol (Stages 4B–8, 9.1 ablation maps, 9.4 LR+EBM methodology). Cited, not regenerated. | **Yes**, with the original stage’s caveats (9.1 = authorization class B: disclose the documentation gap). Stage 10 does **not** create this evidence. |
| **2. STAGE 10 INTEGRITY / ANALYSIS-ONLY / DESCRIPTIVE** | Documentation, hash/identity checks, algebraic decompositions, or citation tables over frozen artifacts. Includes post-hoc descriptive cuts of already-unblinded LC TEST. | **No** as *new* confirmatory experiments. They do not generate independent confirmatory TEST evidence. |
| **3. EXPLORATORY** | Stage 9.2, 9.3 G1/G3, 9.4 XGBoost, Experiment G citation, S10-R1-YEAR, any unplanned extra cut. | **No.** Favorable numbers do **not** convert these to confirmatory. |

There is **no** Stage 10 class “new confirmatory TEST-set experiment.” An analysis is not confirmatory merely because it produces a favorable result.

LendingClub TEST is **already unblinded** (Stages 4B–8). Any Stage 10 LC TEST work is **reanalysis of previously exposed outputs**, never model/threshold/calibration **selection**, and **must not** be called confirmatory.

---

## 1. Research questions

Do **not** assume positive answers.

**RQ10.1 — Architecture ablation.**  
Does the evidence-separated decision architecture produce a materially different approve/review/reject allocation than the credit-only and monolithic comparators **because of explicit governance/evidence handling**, rather than because of a hidden credit-model change?

**RQ10.2 — Decision-policy robustness.**  
How sensitive are approve/review/reject outcomes and error/cost characteristics to the pre-specified assumed relative cost scenarios already used in Stage 8 (`r ∈ {1,2,5,10}`, `C_REVIEW=0.25*C_FP` unless Experiment G)?

**RQ10.3 — Calibration robustness.**  
Are the main probability-quality conclusions stable across the frozen calibration alternatives already evaluated (raw / Platt / isotonic), **without using TEST performance for selection**?

**RQ10.4 — Generalization robustness.**  
Which findings are specific to LendingClub (temporal split, `Default` = Charged Off vs Fully Paid, evidence-separated governance) and which **methodology-level** observations are also visible on independent UCI (`default payment next month`, no Shariah layer)?

**RQ10.5 — Evidence-gap robustness.**  
Does the very high review allocation under A1/G0 persist **because the current LendingClub dataset lacks contract-level evidence** (L2 `INSUFFICIENT_INFORMATION`), rather than because credit scores were altered?

---

## 2. Hypotheses

Where a statistical test would be inappropriate, the statement is **descriptive**, not inferential. No p-value is attached to policy allocations.

### H10.1 Architecture (RQ10.1) — descriptive plus identity check

**Descriptive directional statement (not a p-test):** Under the **same** frozen `p_selected`, A0, A1/G0, and A3/A4 produce different TEST decision allocations. By construction A3/A4 has zero `HUMAN_REVIEW`. Existing freeze-backed counts (n = 208,886) are:

| System | APPROVE | HUMAN_REVIEW | REJECT |
| ---: | ---: | ---: | ---: |
| A0 | 5232 | 203627 | 27 |
| A1/G0 | 0 | 208859 | 27 |
| A3/A4 | 61855 | 0 | 147031 |

**Practical significance (pre-specified, not a p-value):** a **material architecture effect on allocation** is a review-rate difference |A1 − A0| ≥ 0.01 **or** an APPROVE-count difference driven only by the G0 matrix (A0 LOW band mapped to review). Existing |A1 − A0| review rate = 5232/208886 ≈ 0.0250.

**Identity check (integrity / provenance, abort if false; not a confirmatory experiment):** A0, A1, and A3/A4 consume identical stored `p_selected` row-wise. If scores differ, the architecture comparison is invalid. Passing this check does **not** generate independent scientific evidence.

**Causal claim that is NOT allowed:** A1 “improves prediction,” ROC-AUC, PR-AUC, or Brier relative to A0/A3. Those metrics are properties of the frozen credit model.

### H10.2 Cost / policy (RQ10.2) — mixed

**Freeze-backed (Stage 8 validation, already executed):** as assumed FN:FP ratio `r` increases, validation-selected `t_low` does not increase (observed table: 0.25, 0.12, 0.06, 0.04). This is cited, not rerun.

**Exploratory (Stage 9.2, class C):** for **frozen** TEST maps, A0 and A3/A4 normalized cost increase with `r`; A1 cost is invariant because stored FN = 0. Stage 10 **cites** this and **does not** promote it to confirmatory.

**No new inferential hypothesis** that a particular `r` is the “true” institutional cost. Ratios remain researcher assumptions.

### H10.3 Calibration (RQ10.3) — already evaluated; cite-only

**Directional (Stage 5, validation-selected Platt):** on LC TEST, Platt Brier and ECE are lower than raw (paired bootstrap CIs for Brier/ECE differences exclude 0 in the Stage 5 report). Discrimination (ROC-AUC/PR-AUC) is unchanged for Platt because the map is strictly increasing.

**Limitation already on record (not a reason to refit):** 2018 year-slice ECE is worse for Platt/isotonic than raw. Stage 10 **must not** recode the frozen calibrator from that slice.

**No new calibration-selection hypothesis.** TEST is not used to choose raw vs Platt vs isotonic.

### H10.4 Generalization (RQ10.4) — descriptive, not an equality test

UCI can show that **independent** train → validation selection → TEST reporting for credit scoring and calibration is implementable. It **cannot** validate Shariah governance, L2 fusion, or LC thresholds.

**Not hypothesized:** equality of LC and UCI AUC/Brier. Targets differ (`Default` vs `default payment next month`). No test of AUC equality is authorized.

**Freeze-backed UCI statements** (original Stage 9.4 provenance) may use Logistic Regression and EBM only. **XGBoost is exploratory** (`DEVIATION-001`); no retroactive or prospective ratification is sought. **S10-A4-SIDEBYSIDE** is an analysis-only comparison of those citations; it is **not** a new confirmatory experiment or statistical test.

### H10.5 Evidence gap (RQ10.5) — descriptive, not a Shariah ruling

**Statement:** A1 APPROVE = 0 and review ≈ 0.999871 because every stored L2 status is `INSUFFICIENT_INFORMATION` and G0 maps LOW/MEDIUM + that status to `HUMAN_REVIEW`. The 5,232 applications that A0 would APPROVE and A1 sends to review **are exactly the credit LOW band**. This is an **evidence-gap / schema** finding (L1 `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`), **not** a religious classification, **not** expert validation, **not** a halal/haram label.

### H10.6 Predictive “non-collapse” — citation, not a new test

Stage 4B already reports TEST PR-AUC below validation PR-AUC for every family, and a large 2018 vs 2017 PR-AUC drop. Stage 10 **does not** define a new inferential collapse test on already-seen LC TEST metrics (that would be post-hoc). **S10-R1-YEAR** does not retrain and is **exploratory / descriptive post-hoc reanalysis**, not a confirmatory TEST experiment. If **S10-I1** fails, Stage 10 aborts rather than interpreting a score mismatch as a robustness finding.

---

## 3. Experiment inventory

Keep the set **small**. Cite-only rows are **not** rerun. Analysis/integrity rows do **not** retrain models, refit calibrators, or search thresholds. **None** of the Stage 10-native IDs is a new confirmatory TEST-set experiment.

| Experiment ID | RQ | Dataset / split | Execution | Classification | Rationale |
| --- | --- | --- | --- | --- | --- |
| **S10-CITE-ARCH** | 10.1 | LC TEST n=208886 | **CITE_ONLY** | Freeze-backed (9.1 class B: disclose gap) | A0/A1/A3 counts already exist |
| **S10-I1-IDENTITY** | 10.1 | LC TEST stored `p_selected` | Integrity check | `INTEGRITY / PROVENANCE CHECK — NOT A SCIENTIFIC CONFIRMATORY EXPERIMENT` | Verifies A0/A1/A3 use the same frozen `p_selected`; does not generate independent scientific evidence |
| **S10-R1-YEAR** | 10.1, 10.2, 10.5 | LC TEST + stored `year` | Descriptive reanalysis | `EXPLORATORY / DESCRIPTIVE POST-HOC REANALYSIS` | LC TEST already unblinded; year-wise TEST decision-mix cannot be confirmatory. May be reported as descriptive temporal analysis of already-observed TEST outputs |
| **S10-CITE-COST-VAL** | 10.2 | LC **validation** | **CITE_ONLY** | Freeze-backed (Stage 8 v1 table2) | Thresholds already selected per `r` on validation |
| **S10-CITE-COST-92** | 10.2 | LC TEST frozen maps | **CITE_ONLY** | **Exploratory** (9.2 class C) | Answers frozen-map cost vs `r`; do not rerun; do not promote |
| **S10-CITE-G** | 10.2 | LC validation Experiment G | **CITE_ONLY** | Exploratory / cite-only (Stage 9.0) | `c_review_over_fp ∈ {0.10,0.25,0.50}`; do not rerun; do not promote G’s `t_low/t_high` |
| **S10-CITE-CAL** | 10.3 | LC val + TEST | **CITE_ONLY** | Freeze-backed (Stage 5) | Raw/Platt/isotonic already selected on val Brier |
| **S10-CITE-SEED** | 10.3 / model | LC val seeds | **CITE_ONLY** | Freeze-backed (4B + 5) | Five-seed family and Platt-selection stability already exist |
| **S10-CITE-UCI** | 10.4 | UCI TEST n=4502 | **CITE_ONLY** | Freeze-backed **LR+EBM**; XGBoost **exploratory** | Do not rerun UCI; do not transfer LC objects; do not elevate XGBoost |
| **S10-A4-SIDEBYSIDE** | 10.4 | LC cited + UCI cited | Analysis-only | `ANALYSIS-ONLY / DESCRIPTIVE COMPARISON` | Cites existing UCI and LC results. Not a new statistical test or new confirmatory experiment. LR/EBM columns inherit 9.4 freeze-backed provenance; XGBoost column remains exploratory |
| **S10-A1-GAP** | 10.5 | Published 8v2/9.1 counts | Analysis-only | `ANALYSIS-ONLY / DESCRIPTIVE` | Decomposes already-observed A1 review using Stage 8/9 artifacts. Not a new empirical experiment; does not independently validate the Shariah governance layer |
| **S10-CITE-GOV** | 10.5 | LC TEST | **CITE_ONLY** | G0 freeze-backed; G1/G3 **exploratory** hypothetical | Do not execute G-unsafe |

### 3.1 Full specification — S10-I1-IDENTITY

| Field | Specification |
| --- | --- |
| Experiment ID | `S10-I1-IDENTITY` |
| Research question | RQ10.1 |
| Dataset | LendingClub granting extract |
| Population/split | TEST (`issue_month >= 2017-02`), n = 208,886 |
| Inputs | `results/calibration/test/ebm_seed42_calibrated.csv`; Stage 8 v2 `table3`; frozen `t_low/t_high/t*` |
| Model(s) | **None loaded.** Frozen EBM is not retrained or scored. |
| Calibration | Frozen Platt `p_selected` column only; **no refit** |
| Policy | Re-apply A0 and A3 maps; A1 cited from stored fusion counts |
| Primary metric | Boolean: A0 re-map counts match table3 `credit_only_selected_bands`; A3 matches `monolithic_credit_threshold`; `p_selected` unique-row identity for all maps |
| Secondary metrics | SHA-256 of freeze files vs Stage 9.4 `protected_hashes_after` |
| Selection rule | **None** |
| TEST usage | Reanalysis only; **not** selection; **not** a confirmatory TEST experiment |
| Expected artifact | `results/stage10/v1/metrics/s10_i1_identity.json`; `audit/stage10_i1_identity.json` (**not created now**) |
| Classification | `INTEGRITY / PROVENANCE CHECK — NOT A SCIENTIFIC CONFIRMATORY EXPERIMENT` |
| Rationale | Verifies A0/A1/A3 use the same frozen `p_selected`. Passing does **not** generate independent scientific evidence. |
| Stop/abort | Hash mismatch; count mismatch; any `.fit` / threshold grid / model load for scoring |

### 3.2 Full specification — S10-R1-YEAR

| Field | Specification |
| --- | --- |
| Experiment ID | `S10-R1-YEAR` |
| Research question | RQ10.1, RQ10.2 (allocation stability), RQ10.5 |
| Dataset | LendingClub granting extract |
| Population/split | TEST rows with stored `year ∈ {2017, 2018}` in `ebm_seed42_calibrated.csv` (column already present; **do not invent calendar fields**) |
| Inputs | Same CSV (`year`, `p_selected`, `y_true`); frozen thresholds; G0 row for `INSUFFICIENT_INFORMATION` |
| Model(s) | None trained |
| Calibration | Frozen `p_selected` |
| Policy | Frozen A0 / A1 / A3 maps. A1 uses **constant** L2 = `INSUFFICIENT_INFORMATION` (Stage 8 v2: 208886/208886). **No new fusion engine run** unless identity with published counts fails. |
| Primary metric | Approve / review / reject **counts and rates by year and architecture** |
| Secondary metrics | Wilson 95% CI on rates; default rate by year × band (evaluation only). **No** year-specific threshold. **No** p-test of 2017 vs 2018 equality (same rule as Stage 4B/5 year slices). |
| Selection rule | **None.** Year is not used to choose policy. |
| TEST usage | Previously exposed TEST, grouped by an already-stored `year` field. Not selection. **Must not** be called confirmatory. |
| Expected artifact | `results/stage10/v1/tables/s10_r1_year_decision_mix.csv`; report section; audit JSON (**not created now**) |
| Classification | `EXPLORATORY / DESCRIPTIVE POST-HOC REANALYSIS` |
| Rationale | LC TEST was already unblinded in Stages 4B–8. A year-wise TEST decision-mix cannot be confirmatory evidence, even if specified before this particular calculation. It may be reported transparently as a descriptive temporal analysis of already-observed TEST outputs. Stage 4B/5 year slices exist for **metrics**, not for **decision mix**; Stage 9 O-YEAR was optional and unused. |
| Stop/abort | `year` missing/not in {2017,2018}; n_2017+n_2018 ≠ 208886; any threshold search; any claim that year slices are Shariah findings |

### 3.3 Full specification — S10-A1-GAP

| Field | Specification |
| --- | --- |
| Experiment ID | `S10-A1-GAP` |
| Research question | RQ10.5 |
| Dataset | LendingClub (published aggregates only) |
| Population/split | TEST n = 208,886 |
| Inputs | Stage 8 v2 credit-band counts LOW 5232 / MEDIUM 203627 / HIGH 27; fusion matrix G0; L1/L2 statuses |
| Model(s) | None |
| Calibration | None |
| Policy | Algebra: A1 − A0 on APPROVE equals −LOW under G0 + all-insufficient L2 |
| Primary metric | Decomposition table (see Section 9) |
| Secondary metrics | Review-cause citation from Stage 8 v2 (`governance_insufficiency` 5232; `governance_insufficiency_and_credit_uncertainty` 203627) |
| Selection rule | None |
| TEST usage | None beyond published tables |
| Expected artifact | Section in `docs/STAGE_10_ROBUSTNESS_REPORT.md` (**not written now**) |
| Classification | `ANALYSIS-ONLY / DESCRIPTIVE` |
| Rationale | Decomposes the already-observed A1 review allocation using existing Stage 8/9 artifacts. Not a new empirical experiment and does **not** independently validate the Shariah governance layer. |
| Stop/abort | Any fabrication of contract evidence; any Shariah score; G-unsafe; treating G1/G3 as empirical Shariah |

### 3.4 Full specification — S10-A4-SIDEBYSIDE

| Field | Specification |
| --- | --- |
| Experiment ID | `S10-A4-SIDEBYSIDE` |
| Research question | RQ10.4 |
| Dataset | LC TEST (cited Stage 5 Platt) **and** UCI TEST (cited Stage 9.4 family table) |
| Population/split | Not merged |
| Inputs | `results/calibration/metrics/stage5_test_metrics.json`; Stage 9.4 report raw TEST family table (LR, EBM; XGBoost optional exploratory column) |
| Model(s) | None trained |
| Calibration | None refit |
| Policy | None on UCI |
| Primary metric | Side-by-side ROC-AUC, PR-AUC, Brier, log loss, ECE **without** a statistical equality test |
| Secondary metrics | Target-definition footnote |
| Selection rule | None |
| TEST usage | Citation of already-reported TEST metrics |
| Expected artifact | One comparison table in the Stage 10 report (**not created now**) |
| Classification | `ANALYSIS-ONLY / DESCRIPTIVE COMPARISON` |
| Rationale | Cites existing UCI and LendingClub results. Must **not** be presented as a new statistical test or new confirmatory experiment. UCI **LR and EBM** cells inherit Stage 9.4 freeze-backed provenance; any XGBoost column remains exploratory (`DEVIATION-001`). |
| Stop/abort | Merging rows; transferring thresholds; labeling UCI as Shariah validation |

### 3.5 Cite-only rows (do not execute)

**S10-CITE-ARCH.** Inputs: Stage 9.1 report §8; `audit/stage9_1_ablation_run.json`. Primary: A0/A1/A3 counts. TEST: previously exposed, not selection. Artifact: citation. Abort if anyone regenerates table3.

**S10-CITE-COST-VAL.** Inputs: `results/decision/tables/table2_validation_threshold_selection.csv` (SHA-256 `797b96255c65663641fab75b98456fd6a7c673d3954b4940bca631b94f030c45` as recorded in Stage 9.2). Primary: `t_low/t_high` and VAL expected cost by `r`. Abort if a new validation grid is searched.

**S10-CITE-COST-92.** Inputs: `docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md` §7.2. Primary: A0 0.244706 / 0.245645 / 0.248460 / 0.253151; A1 0.250030 invariant; A3/A4 0.549347 / 0.577976 / 0.663860 / 0.807000. **Exploratory.** Abort if rerun or if cited as pre-registered confirmatory.

**S10-CITE-G.** Inputs: `results/decision/tables/experiment_g_review_cost_perturbation.csv` SHA-256 `98c673e98732f21d0863eb4737bbab5744a5859937f624dc229e6853fd535bb3`. **Not executed in Stage 10.** Abort if G thresholds are written into Stage 8 freeze.

**S10-CITE-CAL.** Inputs: Stage 5 report §§B–H. Selection: validation Brier, 0.001 tie, simplicity raw > platt > isotonic → Platt. TEST: reporting only. Abort if TEST Brier is used to recode the calibrator (including 2018 ECE).

**S10-CITE-SEED.** Inputs: Stage 4B per-seed table; Stage 5 seed-stability Platt selection (all five seeds selected Platt). Abort if R-SEED-POLICY threshold re-search is started (Stage 9 freeze: **SKIP**).

**S10-CITE-UCI.** Inputs: Stage 9.4 report; `results/uci_generalization/v1/metrics/uci_test_selected.json` (XGBoost+isotonic numbers are **exploratory** and must not be elevated). Freeze-backed family TEST raw metrics already stored: LR ROC-AUC 0.757278 PR-AUC 0.525511 Brier 0.187096; EBM 0.768856 / 0.537376 / 0.137432. Abort if UCI is rerun, if LC Platt `(a,b)` is applied, if LC thresholds are applied, or if XGBoost is labeled pre-registered.

**S10-CITE-GOV.** G0 observed 0 / 208859 / 27. G1/G3 hypothetical 0/0/208886 and 0/208886/0. G-unsafe **not executed**.

---

## 4. Architecture ablation

Definitions are **copied from Stage 9.0 / 9.1**. They are **not** silently redefined.

| ID | Definition | HUMAN_REVIEW | Governance | Role |
| --- | --- | --- | --- | --- |
| **A0** | `p_selected < 0.06` APPROVE; `0.06 ≤ p < 0.69` HUMAN_REVIEW; `p ≥ 0.69` REJECT | Yes (credit MEDIUM) | None | Credit-only ablation |
| **A1** | Same credit bands, fused with Stage 7 v2 L2 under **G0** | Yes | G0 primary | Proposed architecture |
| **A3** | `p_selected < 0.16` APPROVE; `p_selected ≥ 0.16` REJECT | No | None | Binary comparator |
| **A4** | Same object as A3 under the Stage 9.0 freeze | No | None | Collapses to A3; report once |

**G0 matrix (unchanged):**

| Governance | LOW | MEDIUM | HIGH |
| --- | --- | --- | --- |
| `NOT_STRUCTURABLE_WITHOUT_REDESIGN` | REJECT | REJECT | REJECT |
| `INSUFFICIENT_INFORMATION` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |
| `REVIEW` | HUMAN_REVIEW | HUMAN_REVIEW | REJECT |
| `PASS` | APPROVE | HUMAN_REVIEW | REJECT |

### Held constant vs changed

| Component | A0 | A1 | A3/A4 |
| --- | --- | --- | --- |
| Credit model (EBM) | Frozen, not scored anew | Same | Same |
| `p_selected` (Platt) | Same stored column | Same | Same |
| `t_low`, `t_high` | 0.06, 0.69 | 0.06, 0.69 | N/A (`t*=0.16`) |
| Review band | Present (MEDIUM) | Present (MEDIUM and/or governance) | **Removed** |
| L2 G0 | **Off** | **On** | **Off** |
| Explainability | Not an approval criterion | Not an approval criterion | Not an approval criterion |

**What is removed/changed:** only the **decision map** (credit-only three-way vs G0 fusion vs binary `t*`).

**Causal interpretation that is NOT allowed:**

- A1 is a more accurate default classifier than A0 or A3.
- Governance “improves AUC.”
- High review is a Shariah ruling or expert-validated non-compliance.
- A3 is an end-to-end Shariah model.

**A3-F** (fused policy with zero `HUMAN_REVIEW`) remains **unspecified and unauthorized**.

---

## 5. Cost / policy sensitivity

### Already observed — reuse, do not rerun

| Evidence | What it answers | Class |
| --- | --- | --- |
| Stage 8 validation table2 | How **selected thresholds** move with `r ∈ {1,2,5,10}` on **validation** | Freeze-backed confirmatory citation |
| Stage 8 primary freeze | `r=5` → `t_low=0.06`, `t_high=0.69`; monolithic `t*=0.16` | Freeze-backed |
| Stage 9.2 | How **frozen TEST maps** score under the same `r` (decisions unchanged) | **Exploratory** |
| Experiment G | Validation `c_review_over_fp ∈ {0.10,0.25,0.50}` under FN:FP=5:1 | Cite-only; do not promote G thresholds |

Stage 9.2 **adequately** answers “frozen A0/A1/A3 TEST maps under alternative `r`.” Stage 10 **recommends reuse**, not a rerun.

### Deliberately NOT proposed

**TEST remaps using validation-selected alternative `(t_low, t_high)` for `r ∈ {1,2,10}`.**  
Stage 8 validation already shows the threshold movement. Additional LC TEST remaps would consume already-unblinded TEST for a pattern visible on validation, and would repeat the class of analysis Stage 9 froze as O-TEST Option A. Stage 10 does **not** require that remap.

### Stage 10 year-stratified allocation (not a confirmatory TEST experiment)

**S10-R1-YEAR** may report allocation (not cost) by year under the **frozen primary** maps. It is `EXPLORATORY / DESCRIPTIVE POST-HOC REANALYSIS`. Cost numbers by year are optional secondary arithmetic using the Stage 8 formula on year-stratified confusion counts; they are **not** used to pick `r` and are **not** confirmatory.

---

## 6. Calibration robustness

**Use Stage 5. Do not rerun calibration to reproduce existing results.**

| Split | Role | Methods | Result (already stored) |
| --- | --- | --- | --- |
| LC TRAIN | EBM fit only | — | TRAIN-only EBM seed 42 |
| LC VALIDATION | **Selection** | Raw / Platt / isotonic | Brier 0.179908 / 0.174845 / 0.174694; 0.001 tie → **Platt** |
| LC TEST | **Reporting only** | Same three, frozen | Platt Brier 0.156169, ECE 0.020267, ROC-AUC 0.677669, PR-AUC 0.350963 |

**Prohibited:** selecting a calibrator on TEST; recoding Platt from 2018 ECE; fitting on TRAIN+VALIDATION; applying LC `(a,b)` to UCI.

If a later amendment ever added a **new** calibration experiment (not proposed here), it would have to specify: train = TRAIN-only model; calibrate = VALIDATION; select = validation Brier + 0.001 simplicity rule; TEST = once after freeze; CI = 1000 percentile bootstrap seed 42; primary metric = Brier.

UCI calibration is already done in Stage 9.4 (isotonic on UCI validation Brier for the executed family). **Do not rerun.** Freeze-backed interpretation of the **rule** (val-only Brier) as applied to **EBM/LR** retains Stage 9.4 provenance. The executed XGBoost+isotonic TEST row is exploratory and must not be elevated.

---

## 7. Model / seed robustness

**Already available — do not retrain because Stage 10 exists.**

| Source | What it resolves |
| --- | --- |
| Stage 4B five seeds `{42,123,2024,3407,9999}` | Family ranking stability on LC validation; RF is the only family with material seed SD; LR seed-degenerate; EBM/XGB tiny SD |
| Stage 4B TEST once after freeze | Honest family metrics + 1000-bootstrap CIs seed 42 |
| Stage 4B 2017/2018 slices | Descriptive temporal discrimination/Brier shift |
| Stage 5 five-seed calibrator selection | Platt selected on every seed |
| Stage 6 five-seed SHAP ranks | Attribution rank stability (not a decision-policy robustness item) |
| Stage 9 freeze **R-SEED-POLICY = SKIP** | No five-seed **threshold** re-search |
| Stage 9.4 UCI seeds | LR deterministic; EBM small SD; XGBoost seed table **degenerate** (exploratory) |

**Additional model/seed experiments proposed:** **none.**

**Not proposed:** adding random forest to UCI; expanding the LC model zoo; retraining EBM; using TEST to change the Stage 4B family.

Negative result retained by citation: LC random forest weaker than L2 logistic on every validation metric.

---

## 8. UCI generalization

Treat Stage 9.4 as **existing** evidence. **Do not rerun UCI automatically.**

**Do not transfer:** LC thresholds `0.06/0.69/0.16`; LC Platt `a,b`; LC Shariah rules; LC decision policy; LC/UCI row merges; invented UCI calendar time.

**Additional UCI training/calibration/TEST evaluation:** **not necessary** for Stage 10. **S10-A4-SIDEBYSIDE** is citation-only.

| | LendingClub | UCI |
| --- | --- | --- |
| Split | Real temporal (`issue_month`) | Stratified 70/15/15, seed 42; `NO_CALENDAR_TIMESTAMPS` |
| Target | `Default` (Charged Off vs Fully Paid) | `default payment next month` |
| Governance architecture | L1/L2 + G0 fusion | **None.** U3 metadata-only. **Does not validate Shariah architecture** |
| Freeze-backed credit models (original provenance) | Frozen EBM + Platt | **LR and EBM** only |
| Exploratory | — | **XGBoost** (execution-time expansion; must not be elevated) |

Datasets are **not** directly equivalent. A better UCI number does not imply the LC pipeline is inferior.

---

## 9. Evidence-gap analysis

**Finding to analyze (already observed, not regenerated):**

- L1: `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` (dataset context, not an applicant ruling)
- L2: `INSUFFICIENT_INFORMATION` on **208,886 / 208,886** TEST rows
- A1/G0: APPROVE 0, HUMAN_REVIEW 208859 (≈ 99.9871%), REJECT 27

**This is not a Shariah ruling.** Do not invent contractual fields, fake contract evidence, halal/haram labels, a Shariah probability/score, or unsupported AAOIFI clauses. Do not run G-unsafe (treat insufficiency as PASS).

**S10-A1-GAP decomposition (`ANALYSIS-ONLY / DESCRIPTIVE`, existing counts; does not independently validate Shariah governance):**

| Piece | n | Interpretation |
| ---: | ---: | --- |
| Credit LOW (would be A0 APPROVE) | 5232 | G0 + insufficient L2 → A1 REVIEW (`governance_insufficiency`) |
| Credit MEDIUM | 203627 | Already review on credit; still review under G0 (`governance_insufficiency_and_credit_uncertainty`) |
| Credit HIGH | 27 | G0 REJECT (same as A0 REJECT) |
| A1 APPROVE | 0 | APPROVE requires L2 `PASS` **and** LOW; PASS never occurs in this extract |

**Hypothetical G1/G3** remain **exploratory engineering** (Stage 9.3 class C), not empirical Shariah findings.

If L2 were hypothetically `PASS` for every row (counterfactual, **not executed**, **not G-unsafe on real rows**): A1 would equal A0 by the G0 matrix. That sentence is **algebra**, not an experiment, and **must not** be stored as a TEST policy.

---

## 10. Statistical analysis

Applies to Stage 10 **integrity / descriptive / citation** work. Citations keep their original Stage 4B/5/8/9 methods and provenance. **No** new confirmatory TEST-set experiment is specified.

| Experiment | Point estimate | Interval | Bootstrap | Seeds | Multiplicity | Effect size | Practical threshold |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S10-I1 | Match booleans; counts | None | None | None new | None | — | Abort on any mismatch |
| S10-R1 | Year × architecture rates | Wilson 95% CI on binomial rates (same method as Stage 9.1 band default-rate CIs) | **Not required** (descriptive rates). Do **not** bootstrap to select policy | Stored seed 42 predictions only | No p-values → no Bonferroni | Δ review rate A1−A0 within year (= LOW rate under constant L2) | Material if \|Δ\| ≥ 0.01 (same as H10.1) |
| S10-A1 | Integer counts | None | None | None | None | LOW n as APPROVE blocked | — |
| S10-A4 | Cited metrics | Cite existing CIs; **no** new CI; **no** AUC test | Do not rerun 1000-bootstrap | — | None | — | Do not declare “better dataset” |
| All cite-only | As originally stored | As originally stored | Do not recompute | Do not retrain | Do not convert exploratory CIs into confirmatory tests | — | — |

**Do not** apply p-values to descriptive policy allocations (A0 vs A1 vs A3; G0 vs G1 vs G3; 2017 vs 2018 mix).

If year-stratified cost is reported, use `Cost_total = C_FN*FN + C_FP*FP + C_REVIEW*n_review` with frozen `r=5` only as a **descriptive** secondary number, not a selection criterion.

---

## 11. TEST protection

**Hard rules for any later Stage 10 execution:**

1. TEST sets are **never** used for model selection.
2. TEST sets are **never** used for threshold selection.
3. TEST sets are **never** used for calibration selection.
4. TEST results are **not** inspected to choose methodology.
5. A TEST result may support a confirmatory **claim** only if it is a **citation of freeze-backed prior-stage evidence** (Stages 4B, 5, 8, 9.1, approved-scope 9.4). **No post-hoc LendingClub TEST analysis** (including **S10-R1-YEAR**) may be called confirmatory. Stage 10 currently proposes **no new confirmatory TEST-set experiment**.

**LendingClub TEST** (n = 208,886, already unblinded): reusable **without rerunning** for citation of Stages 4B, 5, 6 (explanations), 8 v1/v2, 9.1. Grouping **S10-R1** is allowed only under frozen A0/A1/A3 maps and stored `year`, and is **exploratory / descriptive post-hoc reanalysis**. **No new policy remap grid.**

**UCI TEST** (n = 4,502): reusable **without rerunning** for citation of Stage 9.4. **Not** used to select UCI family or calibrator (already true in the 9.4 audit). Stage 10 must not open UCI TEST for a new selection.

**Reusable TEST artifacts (do not regenerate):**

| Artifact | Use |
| --- | --- |
| `results/metrics/stage4b_test_metrics.json` | LC family TEST (cite) |
| `results/calibration/metrics/stage5_test_metrics.json` | LC Platt TEST (cite) |
| `results/calibration/test/ebm_seed42_calibrated.csv` | `p_selected`, `year` for S10-I1 / S10-R1 |
| `results/decision/v2/tables/table3_test_decision_outcomes.csv` | A0/A1/A3 counts |
| `results/uci_generalization/v1/metrics/uci_test_selected.json` | Exploratory XGBoost+isotonic row only |
| Stage 9.4 report family TEST table | Cite UCI LR/EBM (freeze-backed provenance); XGBoost remains exploratory |

---

## 12. Artifacts (created only during later execution of the gated activities; not by this documentation edit)

The protocol and the approved amendment already exist. Execution artifacts below are **not** created by this gate edit.

| Path | When | Role |
| --- | --- | --- |
| `docs/STAGE_10_EXPERIMENTAL_PROTOCOL.md` | Exists | This protocol |
| `docs/amendments/AMENDMENT-STAGE10-AUTHORIZATION.md` | Exists (`APPROVED` 2026-09-15) | Controlling authorization |
| `configs/stage10/*.yaml` | After gated execution starts | Execution config |
| `experiments/stage10/**` | After gated execution starts | Runners |
| `src/` Stage 10 modules | After gated execution starts | Integrity + year tables only |
| `results/stage10/v1/**` | After execution | Tables/metrics |
| `results/figures/stage10/**` | After execution | Optional allocation charts |
| `audit/stage10_*.json` | After execution | Manifests, hashes, `git_commit` if available |
| `docs/STAGE_10_ROBUSTNESS_REPORT.md` | After execution | Results |
| `tests/test_stage10_*.py` | After gated execution starts | Identity hashes, freeze thresholds, no `.fit` on TEST |

Runners **must not** edit this protocol, the constitution, amendment status, or Stage 7–9 result files.

---

## 13. Authorization gate

```text
STAGE_10_DESIGN_STATUS = COMPLETE
STAGE_10_EXECUTION = AUTHORIZED FOR S10-I1-IDENTITY, S10-R1-YEAR, S10-A1-GAP, AND S10-A4-SIDEBYSIDE ONLY
  (controlling authorization: AMENDMENT-STAGE10-AUTHORIZATION, APPROVED 2026-09-15).
```

**Permitted only** (classifications unchanged; this gate does not execute them):

1. `S10-I1-IDENTITY` — integrity/provenance check only. **NOT** a scientific confirmatory experiment.
2. `S10-R1-YEAR` — exploratory/descriptive post-hoc LendingClub TEST reanalysis. **Non-confirmatory.** No model selection. No threshold selection. No calibration selection.
3. `S10-A1-GAP` — analysis-only decomposition of the existing Stage 8/9 A1 review allocation. Existing artifacts only. No new Shariah rules. No fabricated contractual evidence. No Shariah score/probability.
4. `S10-A4-SIDEBYSIDE` — descriptive comparison using existing LR/EBM evidence. No new TEST AUC experiment. Do not reopen UCI TEST for model/calibration selection.

**This gate also states:**

* Stage 9 remains **CLOSED**.
* Stage 10 does **not** reopen Stage 9.
* No new confirmatory TEST-set experiment is authorized.
* No new model family is authorized.
* No threshold search is authorized.
* No calibration selection on TEST is authorized.
* No new Shariah rules or expert-validation claims are authorized.
* No fabricated contract evidence is authorized.
* XGBoost remains exploratory and is **NOT** ratified.
* Stage 11 is **not** authorized.
* Paper drafting is **not** authorized.
* The approved amendment `AMENDMENT-STAGE10-AUTHORIZATION` remains the **controlling authorization**.

This protocol does **not** edit `RESEARCH_CONSTITUTION.md` and does **not** modify the approved amendment file.

Chat instructions to “run Stage 10,” Cursor commands, or a runner writing files do **not** expand this scope. Favorable numbers do **not** convert S10-I1 / S10-R1 / S10-A1 / S10-A4 into confirmatory TEST experiments.

The amendment **must not** be read as: rewriting `audit/stage9_0_experimental_freeze.json`; converting 9.2/9.3/XGBoost to confirmatory; authorizing G-unsafe; authorizing LC→UCI threshold/calibrator/governance transfer; starting Stage 11 or the paper.

---

## 14. Stop conditions

Do **not** proceed with Stage 10 execution (or abort an authorized run) if any of the following hold:

| Condition | Action |
| --- | --- |
| Required freeze artifact missing or SHA-256 ≠ Section “Design authority” | Abort |
| Frozen split membership mismatch (LC or UCI) | Abort |
| TEST leakage: any model/threshold/calibrator selection on TEST | Abort; do not invent confirmatory claims from leaked selection |
| Methodology ambiguity (e.g. attempting A3-F, G-unsafe, Shariah score) | Abort |
| Duplicate experiment: rerunning Stage 5/8/9.1/9.2/9.4 to “get the same table” | Do not start |
| Labeling S10-I1 / S10-R1 / S10-A1 / S10-A4 as confirmatory TEST experiments | Forbidden; abort the claim |
| `S10-I1` count or hash mismatch | Abort **S10-R1** |
| `year` missing or not {2017,2018}; year counts do not sum to n | Abort **S10-R1** |
| Insufficient data for intended inference (e.g. HIGH band n=27: no year-wise HIGH inference beyond descriptive counts) | Report limitation; do not overclaim |
| Cannot reproduce a required frozen artifact | Abort |
| Authorization mismatch: runner exists while amendment is not `APPROVED`; runner edits gates | Abort |
| Attempt to ratify 9.2/9.3/XGBoost via Stage 10 | Forbidden |
| Git unavailable | Record `git_commit: null`; do **not** fabricate; not by itself a scientific abort |

---

## 15. Documentation-only design review (no experiments)

Inspected for consistency (read-only): `RESEARCH_CONSTITUTION.md`; `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md`; `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md`; Stage 8 v1/v2 reports; Stage 4B, 5, 6 reports; Stage 9.1–9.4 reports; `docs/decision_cost_assumptions.md`; Stage 8/9 configs; Stage 8 v2 / Stage 5 / UCI result manifests.

| Check | Outcome |
| --- | --- |
| A0/A1/A3/A4 match Stage 9.1 §3 | Yes |
| Thresholds 0.06 / 0.69 / 0.16 | Yes |
| Stage 9.2 not proposed for rerun | Yes |
| Stage 9.4 UCI not proposed for rerun | Yes |
| XGBoost remains exploratory | Yes |
| No Shariah score / fake contracts | Yes |
| LC TEST unblinded → reanalysis only; no post-hoc LC TEST analysis called confirmatory | Yes |
| `ebm_seed42_calibrated.csv` already contains `year` | Yes — S10-R1 does not invent time; S10-R1 is exploratory/descriptive post-hoc |
| Stage 5 2018 ECE deterioration retained as limitation | Yes |
| O-YEAR was optional and unused in Stage 9 | Yes — S10-R1 remains a descriptive option, **not** confirmatory |
| Stage 10 proposes no new confirmatory TEST-set experiment | Yes |
| R-SEED-POLICY SKIP | Honored |
| A2-D not proposed (would re-search thresholds) | Yes |
| Constitution / Stage 9 freeze JSON / results **not modified** by this design | Yes |

### Unresolved methodology questions (do not invent answers)

1. **A3-F** (fused zero-review policy) remains unspecified.
2. How a **contract-complete** dataset would change L2 (cannot be answered on LendingClub without fabricating fields).
3. Whether a future paper cites Stage 9.2 costs as exploratory footnotes only (this protocol requires that).
4. `docs/statistical_analysis_plan.md` remains an unfilled Stage 0 stub; **this document is the Stage 10 SAP**.
5. No `.git` directory: execution manifests will have `git_commit: null` unless a repository is created later.

---

## Experiments deliberately NOT proposed

| Tempting extra | Why not |
| --- | --- |
| Retrain LC EBM / LR / XGB / RF | Stage 4B already did five-seed + TEST |
| Refit Platt/isotonic | Stage 5 already did val selection + TEST reporting + seed table |
| Rerun Stage 9.1 ablation | Counts frozen; S10-I1 only checks identity |
| Rerun Stage 9.2 | Adequately answers frozen-map cost vs `r` (exploratory citation) |
| TEST remap of table2 thresholds for other `r` | Incremental TEST use; VAL already shows threshold movement |
| Rerun Experiment G | Cite-only; would re-select thresholds |
| Rerun UCI 9.4 | Independent pipeline already exists |
| Add RF to UCI / four-family bake-off | U1 freeze; unjustified zoo expansion |
| SHAP rerun | Stage 6 complete; not a decision-robustness gap |
| G-unsafe | Not a candidate policy |
| Year-tuned policy or year-specific calibrator | Forbidden by Stage 5 limitations and this protocol |
| p-test of LC vs UCI AUC | Targets not equivalent |
| Promote XGBoost / 9.2 / 9.3 to confirmatory | `DEVIATION-001` |

---

```text
STAGE_10_DESIGN_STATUS = COMPLETE
STAGE_10_EXECUTION = AUTHORIZED FOR S10-I1-IDENTITY, S10-R1-YEAR, S10-A1-GAP, AND S10-A4-SIDEBYSIDE ONLY
  (controlling authorization: AMENDMENT-STAGE10-AUTHORIZATION, APPROVED 2026-09-15).
Stage 9 remains CLOSED. Stage 10 does not reopen Stage 9.
No new confirmatory TEST-set experiment is authorized.
Stage 11 is not authorized. Paper drafting is not authorized.
```
