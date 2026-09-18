# Stage 9 Experimental Protocol

**Status:** `STAGE 9.0 DESIGN FREEZE` — scientific protocol frozen in Stage 9.0.  
**Authorization in this document:** see execution gate below. Historical Stage 9.1–9.3 process record: `docs/deviations/DEVIATION-001-stage9-authorization-gap.md`. Stage 9.4: `docs/amendments/AMENDMENT-STAGE9-4-AUTHORIZATION.md` (status `APPROVED`, approval date 2026-09-15).  
**Not authorized:** Stages 9.5–9.7; confirmatory/pre-registered use of Stage 9.4 XGBoost (execution-time expansion outside approved written Logistic Regression + EBM scope; see `DEVIATION-001`); threshold changes; new Shariah rules; AAOIFI clause retrieval/invention; paper drafting.

| Gate | Status |
| --- | --- |
| Stage 7 v2 | `PASS` (`docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md`) |
| Stage 8 v2 | `PASS` (`docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`) |
| Stage 8 v1 | Historical evidence (`docs/STAGE_8_DECISION_POLICY_REPORT.md`) |
| Controlling methodology | `AMENDMENT-SHARIAH-001` |
| Constitution | `RESEARCH_CONSTITUTION.md` |
| This protocol | `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` |
| Stage 9.0 freeze audit | `audit/stage9_0_experimental_freeze.json` |
| Stage 9 execution | See gate text below (`DEVIATION-001`; `AMENDMENT-STAGE9-4-AUTHORIZATION`) |

```text
STAGE_9_DESIGN_FREEZE = PASS
STAGE_9_EXECUTION = AUTHORIZED FOR STAGE 9.1-9.3 (historical, see DEVIATION-001) AND STAGE 9.4 (per AMENDMENT-STAGE9-4-AUTHORIZATION).
Stages 9.5-9.7 remain unauthorized.
```

Gate attribution: historical 9.1–9.3 wording is recorded in `docs/deviations/DEVIATION-001-stage9-authorization-gap.md` and is **not** retroactive freeze-JSON authorization. Stage 9.4 wording is recorded in `docs/amendments/AMENDMENT-STAGE9-4-AUTHORIZATION.md` (status `APPROVED`, approval date 2026-09-15). Approved written Stage 9.4 model scope remains Logistic Regression + EBM. XGBoost remains an exploratory execution-time expansion per `DEVIATION-001`; no retroactive or prospective ratification is being sought for that expansion.

```text
Stage 8 t_low  = 0.06 → FROZEN
Stage 8 t_high = 0.69 → FROZEN
Stage 8 policy → FROZEN
Stage 8 results → PRESERVED
LC TEST → NO NEW POLICY TUNING
UCI TEST → PROTECTED UNTIL UCI FREEZE
```

No repository experiment is started by this freeze.

---

## 0. Stage 9.0 design freeze (this task)

This section records research-owner freeze decisions. It does not execute Stage 9.

### 0.1 Proposed architecture (not an ablation)

The proposed evidence-separated system remains the Stage 8 three-way credit policy fused with independent L2 governance (A1 / G0):

```text
p_selected < 0.06            → LOW     → (credit-only would APPROVE; fused: matrix cell)
0.06 <= p_selected < 0.69    → MEDIUM  → HUMAN_REVIEW  (credit band)
p_selected >= 0.69           → HIGH    → REJECT
```

Human Review is **part of the proposed architecture**. It is not removed. Frozen calibrated thresholds:

```text
t_low  = 0.06
t_high = 0.69
```

These values are not re-selected in Stage 9.

### 0.2 Cite-only vs newly executed

| ID | Role | Stage 9 action |
| --- | --- | --- |
| A0 | Credit-only two-threshold | **Cite-only** — Stage 8 v2 artifacts. Do not rerun. |
| A1 | Evidence-separated fused architecture | **Cite-only** — Stage 8 v2 artifacts. Do not rerun. |
| A4 / A3 | Monolithic / binary no-review comparator | **Cite-only** — Stage 8 monolithic `t*=0.16` artifacts. Do not rerun. |
| A2-P | Raw vs Platt scoring | **Cite-only** — Stage 5 TEST/validation artifacts. Do not rerun. |
| A2-D | Raw-probability policy thresholds | **Optional later**; validation-only; not executed in 9.0 |
| Cost `{1,2,5,10}` and Experiment G | Assumption sensitivity | **Cite-only** existing validation tables; no Stage 8 rewrite |
| G0 | Primary governance treatment | **Cite-only** Stage 8 matrix |
| G1 / G3 | Hypothetical engineering sensitivity | Not executed in 9.0; not religious rankings |
| UCI pipeline | Secondary credit generalization | Not executed in 9.0; UCI TEST protected |
| 9.6 clean-room | Hash/pytest reproduction | Not executed in 9.0 |

Citation/reuse of existing results is not a new experiment and must not overwrite Stages 4–8.

### 0.3 A3 definition (binary ablation only)

A3 answers: *what happens if the explicit `HUMAN_REVIEW` state is removed?*  
A3 does **not** replace A1.

The Stage 8 specification already defines a binary policy (`configs/stage8_decision_policy.yaml` `monolithic_baseline`, `docs/decision_policy_specification.md`). Stage 9 **reuses that frozen rule**. No new A3 threshold-search rule is invented.

| Item | Frozen specification |
| --- | --- |
| 1. How review is removed | Set `t_low = t_high = t*` so MEDIUM is empty (`empty_medium_when_t_low_equals_t_high`). Decisions are only APPROVE or REJECT. Governance is **not** applied (credit-policy comparator). |
| 2. Probability | Frozen Platt `p_selected` (not `p_raw`; not a Shariah score). |
| 3. Binary threshold | `t* = 0.16` = Stage 8 FN:FP=5:1 `selected_single` (`results/decision/v2/frozen_policy.json` `monolithic_t`; `audit/stage8_threshold_selection.json`). |
| 4. Selection split | Validation only (already performed in Stage 8). |
| 5. Selection objective | Already fixed in Stage 8: minimize expected normalized cost of the **single-threshold** credit rule with `cost_uses_review: false` (`C_REVIEW=0` in that selection), grid `0.02–0.80` step `0.01`, same tie-break as `selection_rule`. |
| 6. LC TEST | Must not be used to select `t*`. Stage 8 already evaluated this policy once; Stage 9 cites that artifact and does not re-select. |
| 7. Stage 8 two-threshold policy | Unchanged: `0.06/0.69` remain the proposed-system thresholds. |
| 8. Reporting | Ablation/comparator only. Same scientific object as A4 under the primary cost scenario. |

**A3-F retired for this freeze.** Applying the frozen G0 matrix with `t_low=t_high` still yields `HUMAN_REVIEW` for `INSUFFICIENT_INFORMATION` + LOW. A fused policy that *eliminates* `HUMAN_REVIEW` while keeping L2 would require a new mapping of former review cells to APPROVE or REJECT. That mapping is **not** in the Stage 8 specification. It is **not invented** here. It is **not authorized**.

### 0.4 Final freeze table

| ID | Final decision |
| --- | --- |
| O-TEST | **Option A** — no additional LC TEST policy remaps |
| O-A2D | **Optional**; execute later only if the paper explicitly evaluates calibration-vs-policy thresholding; validation-only; never apply `0.06/0.69` to `p_raw` |
| O-A3F | **Binary policy pre-specified:** Stage 8 monolithic `t*=0.16` on `p_selected`; validation-selected already; no LC TEST re-selection; A3-F fused-no-review mapping **not specified / not authorized** |
| O-G | G0 remains primary; G1 = all REJECT and G3 = all REVIEW are hypothetical **engineering** sensitivities; not religious rulings; not ranked as more/less Shariah-compliant |
| O-YEAR | **Optional** descriptive reuse of stored Stage 8 v2 outputs (2017 vs 2018); not new training; not year-tuned policy |
| U1 | **EBM + logistic regression only**; not a four-family competition |
| U2 | No LendingClub threshold transfer; UCI Stage 9 work is scoring, calibration, robustness/generalization |
| U3 | UCI L1 is dataset metadata only; no L2 governance fusion |
| R-SEED-POLICY | **SKIP** five-seed LC threshold re-search |

Seeds for existing LC credit robustness remain `42, 123, 2024, 3407, 9999`. No new seeds for threshold re-search.

---

## 0.5 Design constraints inherited from the repository

Stage 9 must use the repository’s actual frozen objects. It must not invent replacements.

| Object | Frozen value / artifact |
| --- | --- |
| Primary dataset | LendingClub granting extract, SHA-256 `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc` |
| Secondary dataset | UCI Default of Credit Card Clients, SHA-256 `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602` |
| LC target | `Default` (`1` = Charged Off, `0` = Fully Paid) |
| LC predictors | `revenue`, `dti_n`, `loan_amnt`, `fico_n`, `emp_length`, `purpose`, `home_ownership_n`, `addr_state`, `zip_code` |
| LC split | Temporal: train `issue_month <= 2016-03` (941,267); validation `2016-04`–`2017-01` (197,528); test `issue_month >= 2017-02` (208,886) |
| UCI split | Stratified 0.70/0.15/0.15, seed 42; train 20,999; validation 4,499; test 4,502. `NO_CALENDAR_TIMESTAMPS` |
| Selected credit family | `explainable_boosting_machine` (`stage4b-lc-granting-v1`) |
| Seeds | `42`, `123`, `2024`, `3407`, `9999`; LC TEST evaluation seed `42` |
| Calibrator | Platt, `a=1.1988263209549705`, `b=0.6697765046966161`, fit on validation only |
| LC TEST `p_selected` file | `results/calibration/test/ebm_seed42_calibrated.csv`, SHA-256 `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb` |
| Primary cost scenario | `FN:FP=5:1`, `C_FP=1`, `C_REVIEW=0.25*C_FP` (assumed, not institutional) |
| Frozen thresholds | `t_low=0.06`, `t_high=0.69` (credit-only, validation-selected, two-threshold) |
| Monolithic single threshold | `t*=0.16` (FN:FP=5:1 `selected_single`) |
| Fusion matrix | `docs/decision_policy_specification.md` / `configs/stage8_decision_policy.yaml` |
| L1 (LendingClub) | `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` (dataset context, not a ruling) |
| L2 (LendingClub TEST) | `evaluation_mode=PER_APPLICATION`; status `INSUFFICIENT_INFORMATION` on all 208,886 rows |
| Design A / Design B | Contract-level governance adopted; purpose-as-contract rejected |
| `SHR-001` | `UNSUPPORTED_RETIRED` |
| AAOIFI operative clauses | Blocked |
| Expert validation | None; do not fabricate `EXPERT_VALIDATED` |

`docs/statistical_analysis_plan.md` is an unfilled Stage 0 stub. Stage 9 uses this protocol plus `docs/METRIC_DEFINITIONS.md` as the statistical plan. `configs/research_config.yaml` is an empty stub. Stage 9.0 freeze metadata is `audit/stage9_0_experimental_freeze.json`. A later execution config may be written only after `STAGE_9_EXECUTION` is authorized.

### TEST already unblinded (critical)

LendingClub TEST labels have already been used for:

- Stage 4B one-shot family evaluation
- Stage 5 calibration reporting
- Stage 6 explanation-sample metrics (labels not used for case selection)
- Stage 8 v1 and Stage 8 v2 decision-policy reporting

Therefore **LendingClub TEST is not a naive holdout for new methodological choices**. Stage 9 may cite existing TEST artifacts. **O-TEST = Option A:** no new LendingClub TEST policy remaps. UCI TEST remains unused for modeling and stays protected until a complete UCI methodology freeze and a later execution authorization.

---

## 1. Objective

Evaluate whether an **evidence-separated** pipeline — independently produced credit-risk scores, explainability attributions, and Shariah-oriented governance evidence, fused only at an explicit decision-policy stage — is more **transparent and defensible** than a **monolithic credit-policy comparator**, without claiming that governance improves ranking metrics and without treating governance rates as religious compliance rates.

Stage 9 is an **evaluation and robustness stage**, not a model-search stage and not a Shariah-rule stage.

---

## 2. Research questions

The controlling question is **not rewritten**:

> Does separating credit-risk scoring, explainability, and Shariah-oriented governance into independently validated and auditable evidence layers, fused only at the final decision stage, provide a more transparent and defensible digital-financing pipeline than a monolithic end-to-end classifier without materially sacrificing predictive performance?

No methodological contradiction with the frozen amendment was found. The phrase “monolithic end-to-end classifier” in the question is interpreted **exactly** as the repository already defines it: a **monolithic credit-policy comparator** (single threshold on the same frozen calibrated EBM probability; no governance; no review band). It is **not** a neural Shariah model and **not** a separately trained end-to-end architecture. Claiming otherwise would be a novelty and baseline error.

Decomposed questions (all subordinate to the controlling question):

| ID | Question | Primary evidence class |
| --- | --- | --- |
| RQ-P | Do credit ranking/calibration metrics of the frozen EBM remain the predictive basis of both architectures? | Predictive / calibration |
| RQ-A | Which architectural switches change **decision** rates rather than ROC-AUC? | Ablation |
| RQ-C | How do assumed FN:FP and `C_REVIEW` values move validation-selected thresholds and rates? | Sensitivity |
| RQ-G | How do explicit hypothetical treatments of `INSUFFICIENT_INFORMATION` move decisions? | Sensitivity |
| RQ-R | Are seed-level credit findings already sufficient, or is further LC retraining required? | Robustness |
| RQ-T | Do year slices of the frozen LC TEST show descriptive drift? | Temporal (descriptive) |
| RQ-U | Does an independently trained UCI credit pipeline show qualitatively similar ranking/calibration behavior? | Generalization (credit only) |
| RQ-Q | Do audit records remain complete, per-row, firewalled, and non-certifying? | Auditability |

---

## 3. Hypotheses

Hypotheses are **pre-declared**. They are not to be selected from TEST.

| ID | Hypothesis | Falsification |
| --- | --- | --- |
| H-P1 | Evidence-separated fusion does **not** change ROC-AUC, PR-AUC, Brier, or log loss relative to credit-only scoring on the same rows, because it consumes the same `p_selected`. | A fused pipeline that modifies probabilities or retrains on governance outputs. |
| H-P2 | Platt calibration can change Brier/ECE without changing ROC-AUC relative to raw EBM `p_raw` (strictly increasing map). | Already supported by Stage 5; Stage 9 cites, does not retune. |
| H-A1 | On LendingClub, A1 (fused) approval rate is lower than A0 (credit-only bands) because `APPROVE` requires L2 `PASS` and LC L2 is `INSUFFICIENT_INFORMATION`. | Fused APPROVE > 0 on LC TEST under the frozen matrix. |
| H-A2 | Review under A1 is produced by **governance insufficiency** and/or **credit MEDIUM**, not by a Shariah score. | Review rows whose audit `review_cause` is unexplained, or a numeric Shariah score in the pipeline. |
| H-A3 | Removing the explicit `HUMAN_REVIEW` state (binary A3/A4, `t*=0.16` on `p_selected`, no governance) yields only APPROVE or REJECT and does not change `p_selected` or ROC-AUC. | A3 producing `HUMAN_REVIEW`, using `p_raw` with `0.06/0.69`, or replacing A1 as the proposed system. |
| H-C1 | Higher FN:FP on validation selects a lower `t_low` and a higher review rate under the credit-only two-threshold rule. | Already tabulated in Stage 8 v1 validation; Stage 9 cites. |
| H-G1 | Treating LC `INSUFFICIENT_INFORMATION` as REJECT (G1) drives review rate to 0 and rejection rate to 1 on LC, given current L2. | A different L2 distribution (not expected on LC). |
| H-G2 | No treatment of insufficiency is a religiously correct policy. Differences are **policy sensitivities**. | Language claiming a treatment is Shariah-compliant. |
| H-U1 | UCI supports a reproducible credit-risk pipeline with its own stratified split, not temporal validation and not Islamic-contract evaluation. | Merging UCI with LC, applying LC thresholds, or running L2 contract rules on UCI as if it were Islamic-finance data. |
| H-Q1 | Purpose changes do not change L2 `evidence_hash` or governance status. | Purpose firewall regression failure. |
| H-N1 | Governance does not improve predictive accuracy. Any paper sentence implying otherwise is false. | A table presenting fused ROC-AUC as an architectural win. |

Negative findings that must remain visible if supported: LC contractual evidence gap; near-universal review under A1; no applicant-level Shariah determination; no `EXPERT_VALIDATED` rules; 2018 PR-AUC drop already reported in Stage 4B; 2018 Platt ECE deterioration already reported in Stage 5.

---

## 4. Ablation matrix

All ablations consume **frozen** Stage 4B/5 probabilities unless a row explicitly says otherwise. None may search thresholds on TEST. None may create a Shariah score.

### 4.1 Inventory

| ID | Name | Decision map | Probability | Governance | Review band | New LC TEST? |
| --- | --- | --- | --- | --- | --- | --- |
| A0 | Credit-only two-threshold | LOW→APPROVE, MEDIUM→HUMAN_REVIEW, HIGH→REJECT | `p_selected` (Platt) | Ignored | Yes (credit MEDIUM) | **No** — Stage 8 v2 already reported |
| A1 | Evidence-separated full | Frozen Stage 8 matrix | `p_selected` | Stage 7 v2 L2 | Yes (credit and/or governance) | **No** — Stage 8 v2 already reported |
| A2-P | Without calibration (predictive) | None (scores only) | `p_raw` vs `p_selected` | None | n/a | **No** — Stage 5 TEST already reported |
| A2-D | Without calibration (policy, validation) | Same credit-only rule as A0, thresholds **re-selected on validation `p_raw`** | `p_raw` | Ignored | Yes if two-threshold selected | **No TEST**; optional later validation-only |
| A2-X | Invalid transfer (rejected as primary) | Apply `t_low=0.06`, `t_high=0.69` to `p_raw` | `p_raw` | — | — | **Forbidden as a fair ablation** |
| A3 / A4 | Binary no-review comparator (ablation) | `p < 0.16` APPROVE else REJECT | `p_selected` | Absent | **No** | **No** — Stage 8 already reported; cite-only |
| A5 | Explainability detached (audit-only) | Identical to A1 decisions | `p_selected` | L2 | Same as A1 | **No** — decisions unchanged; optional audit-field contrast |

A5 does not change actions. It tests whether explainability is a **decision criterion** (it is not) versus an **audit attachment** (Stage 6 global top features). If executed, it is an audit completeness check, not a performance ablation.

### 4.2 Safety sheet (required eight answers)

#### A0 — Credit-only

1. **Changes:** Drops L2 from the matrix; uses credit bands only.  
2. **Frozen:** EBM, Platt, `t_low=0.06`, `t_high=0.69`, split, labels.  
3. **Split for selection:** Validation (already done, Stage 8 v1).  
4. **TEST touched?** Already, once, Stage 8. Do not repeat.  
5. **Tunable on validation?** Thresholds already frozen; do not re-search.  
6. **Metrics:** Approval/review/rejection rates; default rate by band; expected normalized cost under the stated scenario; **not** ROC-AUC as an A0-vs-A1 contrast.  
7. **Supports:** “Credit policy alone auto-approves LOW-band applications.”  
8. **Does not support:** Shariah compliance; superiority of ROC-AUC; operational staffing claims.

#### A1 — Evidence-separated full architecture

1. **Changes:** Adds independent L2 status to the frozen matrix.  
2. **Frozen:** Same as A0 plus Stage 7 v2 engine/L1/L2; fusion matrix; no new rules.  
3. **Split for selection:** Fusion matrix frozen in Stage 8 specification, not selected on TEST.  
4. **TEST touched?** Already, once, Stage 8 v2. Do not repeat.  
5. **Tunable on validation?** No. Matrix is a declared architectural mapping.  
6. **Metrics:** Decision rates; review causes; governance-status distribution; audit completeness; per-row hash uniqueness.  
7. **Supports:** Traceable fusion; evidence-gap handling; L1≠L2.  
8. **Does not support:** Applicant-level Shariah rulings; improved AUC; “208,886 inspections” as contractual review.

#### A2 — Without calibration

**Methodological constraint:** `t_low=0.06` and `t_high=0.69` were identified on **calibrated** validation probabilities. They are calibration-specific. Applying them to `p_raw` is not a valid “turn calibration off” ablation (A2-X). Stage 5 already shows `p_raw` and Platt `p_selected` are not on the same numerical scale for ECE/Brier (validation RAW Brier 0.179908 vs Platt 0.174845; TEST RAW ECE 0.037535 vs Platt 0.020267).

**A2-P (authorized without new TEST):** Cite Stage 5 paired TEST metrics and reliability diagrams. Claim: calibration is a scoring-layer property, independent of governance.

**A2-D (optional later; not executed in 9.0):** Include only if the paper explicitly evaluates the effect of calibration on downstream credit-policy thresholding. Re-run the Stage 8 credit-only selection rule (`configs/stage8_decision_policy.yaml` grid 0.02–0.80 step 0.01, minimize expected normalized cost, same tie-break) on validation **`p_raw`**. Compare selected `(t_low, t_high)` and validation rates to the frozen calibrated selection. Do **not** replace Stage 8 thresholds. Do **not** apply `0.06/0.69` to `p_raw`. Do **not** choose the raw-policy using TEST.

6. **Metrics:** Validation selected thresholds; validation policy rates; optional overlay of reliability diagrams (existing).  
7. **Supports:** “Policy thresholds are not portable across uncalibrated vs calibrated scores.”  
8. **Does not support:** A claim that Stage 8’s 0.06/0.69 are the correct raw-score thresholds; any TEST-tuned raw policy.

#### A3 / A4 — Binary no-review comparator (ablation)

This is **not** the proposed architecture. Human Review remains in A1.

**How the review band is removed**

```text
t_low = t_high = t* = 0.16
LOW  := p_selected < 0.16   → APPROVE
HIGH := p_selected >= 0.16  → REJECT
MEDIUM is empty
HUMAN_REVIEW is not an output
governance is not applied
```

This is Stage 8 `monolithic_baseline` / `empty_medium_when_t_low_equals_t_high`. A3 and A4 name the same frozen object under FN:FP=5:1.

**Probability:** frozen Platt `p_selected`.

**Threshold selection (already executed in Stage 8; not repeated):** validation only; minimize expected normalized cost of the single-threshold rule with `cost_uses_review: false`; grid 0.02–0.80 step 0.01. LC TEST was not used to select `t*`. Stage 9 must not re-search `t*` on TEST or validation.

**Does not modify** Stage 8 `t_low=0.06`, `t_high=0.69`.

1. **Changes:** Removes `HUMAN_REVIEW` and governance from the decision map.  
2. **Frozen:** `p_selected`; `t*=0.16`; Stage 8 `monolithic_baseline`.  
3. **Split for selection:** Validation (already done).  
4. **TEST touched?** Already, once, Stage 8. Cite-only. Do not repeat.  
5. **Tunable on validation?** Forbidden to re-search.  
6. **Metrics:** Approval/rejection rates; expected cost with `C_REVIEW=0` as in Stage 8; default rates by action. Not ROC-AUC vs A1.  
7. **Supports:** A decision-policy ablation of “no review band.”  
8. **Does not support:** Replacing A1; a neural Shariah classifier; religious validity; AUC gains.

**Not authorized:** A3-F (frozen G0 matrix without credit MEDIUM). That still emits `HUMAN_REVIEW`. A fused binary mapping of review cells is unspecified and is not invented.

#### A4

A4 is the Stage 8 name for the same binary comparator as A3. Report once; do not duplicate as two TEST evaluations.

### 4.3 What Stage 9 should **not** re-execute

Do not retrain EBM, refit Platt, rebuild Stage 4A matrices, re-extract all 208,886 L2 rows, or rewrite Stage 8 v2 audits in order to reproduce A0/A1/A3/A4/A2-P. Point to existing versioned artifacts.

---

## 5. Sensitivity matrix

Stage 9 sensitivity **must not retroactively alter Stage 8**. The Stage 8 v2 policy remains:

```text
t_low = 0.06
t_high = 0.69
matrix = Stage 8 specification
primary scenario = FN:FP=5:1, C_REVIEW = 0.25 * C_FP
```

### 5.1 Cost-ratio sensitivity (credit-only threshold identification)

**Already executed on validation (cite, do not rerun unless a code bug is proven):**

| Scenario | Selected type | `t_low` | `t_high` | Val expected cost | Artifact |
| --- | --- | ---: | ---: | ---: | --- |
| FN:FP=1:1 | two_threshold | 0.25 | 0.69 | 0.205605 | `results/decision/tables/table2_validation_threshold_selection.csv` |
| FN:FP=2:1 | two_threshold | 0.12 | 0.69 | 0.240082 | same |
| FN:FP=5:1 (primary) | two_threshold | 0.06 | 0.69 | 0.249025 | same; Stage 8 freeze |
| FN:FP=10:1 | two_threshold | 0.04 | 0.69 | 0.249727 | same |

Monolithic `selected_single` on the same rows: 0.53 / 0.33 / **0.16** / 0.10 respectively.

**Candidate ratios for Stage 9:** keep the frozen set `{1, 2, 5, 10}`. Do **not** add new ratios without a Rule #14 amendment. Do **not** pick a “winner” from TEST.

**Selection procedure (already frozen):** minimize validation expected normalized cost on the credit-only three-way rule; grid `0.02–0.80` step `0.01`; tie-break as in `configs/stage8_decision_policy.yaml`.

**Validation protocol:** all four scenarios already have validation selections. Stage 9 reports them as **assumption dependence**, not as a new search.

**Threshold derivation:** none new for the primary paper policy.

**TEST:** **not** re-evaluated for non-primary ratios (O-TEST = Option A). Sensitivity remains validation-only citation of existing tables.

**Outputs:** table of `(ratio → t_low, t_high, val approve/review/reject, val cost)`; optional plot already in Stage 8 figures 1–3. Confidence intervals: Wilson 95% on **rates** if recomputed on validation counts; do not bootstrap-select thresholds.

**Experiment G (review-cost perturbation):** validation-only, `c_review_over_fp ∈ {0.10, 0.25, 0.50}` under FN:FP=5:1 (`results/decision/tables/experiment_g_review_cost_perturbation.csv`). Stage 9 cites this. Do not promote G’s `t_low/t_high` into Stage 8.

### 5.2 Governance-insufficiency sensitivity (hypothetical policies)

LendingClub L2 is `INSUFFICIENT_INFORMATION` for every TEST row. Sensitivity is therefore a **matrix treatment of one status**, not a search over religious content.

| ID | Label | Treatment of `INSUFFICIENT_INFORMATION` | Status |
| --- | --- | --- | --- |
| G0 | Frozen Stage 8 matrix | LOW/MEDIUM → `HUMAN_REVIEW`; HIGH → `REJECT` | **Primary**; already TEST-reported |
| G1 | Conservative REJECT | All bands → `REJECT` | Hypothetical sensitivity |
| G3 | Governance-gated REVIEW | All bands → `HUMAN_REVIEW` (including HIGH) | Hypothetical sensitivity |
| G-unsafe | Treat as PASS | LOW → `APPROVE` (i.e. behave like A0 for this status) | **Unsafe counterfactual only**; not a candidate policy |

**Forbidden:** adopting G1, G3, or G-unsafe as “the Shariah-correct” treatment; converting insufficiency to religious non-compliance; using TEST to pick among G0/G1/G3; ranking G1/G3 as more or less Shariah-compliant.

**Not executed in 9.0.** Under O-TEST Option A, no new LC TEST policy remaps. Conceptual/synthetic description of G1/G3 is allowed after execution authorization. Arithmetic illustrations that use **already published** Stage 8 v2 band counts must be labeled as derived commentary, not a new TEST evaluation.

**Synthetic (after execution authorization, no LC TEST, no fabricated LC contracts):** reuse Stage 7 synthetic evidence-sensitive cases through the G0 matrix (already in `tests/test_stage8_v2.py::test_h_synthetic_fusion_cases`). Extend unit tests for G1/G3 only after execution is authorized.

Do not call any G-row a compliance rate.

### 5.3 Sensitivity safety sheet (pattern)

For every sensitivity cell: (1) only the named cost or matrix cell changes; (2) EBM/Platt/split/L2 extractor frozen; (3) thresholds from validation or frozen Stage 8; (4) TEST not used to choose; (5) no validation re-search except A2-D if approved; (6) metrics = decision rates and stated expected cost; (7) supports assumption-dependence; (8) does not support a true institutional cost or a fatwa.

---

## 6. Robustness plan

### 6.1 Seeds `42, 123, 2024, 3407, 9999`

**Already exists — do not blindly repeat:**

| Stage | What exists | Additional LC execution needed? |
| --- | --- | --- |
| 4B | Five-seed validation metrics for LR, RF, XGB, EBM; TEST once at seed 42 | **No** retraining |
| 5 | Five-seed Platt vs isotonic vs raw Brier; Platt selected every seed | **No** recalibration |
| 6 | Five-seed SHAP rank stability on the explanation protocol | **No** new SHAP |
| 8 | Policy freeze is seed-42 `p_selected` | Do not re-select thresholds per seed on TEST |

EBM validation ROC-AUC range across seeds is `0.665655–0.665831`. Platt is selected at every seed. That is sufficient for **credit-model seed robustness** in the paper, with the existing mean±SD tables.

**Not authorized:** five-seed TRAIN-only EBM refits solely to re-derive `t_low/t_high`. `R-SEED-POLICY = SKIP`.

### 6.2 Temporal robustness (LendingClub)

Do **not** change the frozen temporal split. Year slices are **descriptive**, not new validation sets.

**Already exists:** Stage 4B TEST-by-year ROC-AUC/PR-AUC/Brier; Stage 5 TEST-by-year Brier/log-loss/ECE (including 2018 Platt ECE increase). Preserve these negative/mixed findings.

**Stage 9 addition (optional descriptive, after execution authorization):** using **already written** Stage 8 v2 decisions joined to `year` on the frozen TEST prediction file, report approval/review/rejection rates and default rates for 2017 vs 2018. Grouping rule: calendar year of `issue_d` as already stored in `ebm_seed42_calibrated.csv`. Do not retune thresholds by year. Do not refit calibration by year. Do not call 2018 a second TEST or a temporal training experiment.

### 6.3 Governance-engineering robustness (not religious validation)

No new religious rules. Tests are engineering properties, largely already in `tests/test_stage7_l1l2.py`, `tests/test_stage8_v2.py`, `tests/test_shariah_rules.py`, `tests/test_shariah_provenance.py`.

| Property | Existing test / artifact | Stage 9 action |
| --- | --- | --- |
| Missing contractual evidence → `INSUFFICIENT_INFORMATION` | Stage 7/8 v2 tests + LC TEST distribution | Cite; do not weaken |
| Firewall (`FIREWALL_FIELDS`) | `test_d_purpose_firewall` and Stage 7 firewall tests | Re-run pytest in 9.6 |
| Purpose invariance | Stage 7 hashes equal; Stage 8 `test_e` | Re-run pytest |
| Deterministic `evidence_hash` | Stage 7 v2 | Hash audit in 9.6 |
| Per-row `record_reference_hash` uniqueness | Stage 8 v2: 208,886 unique hashes | Cite; do not re-broadcast |
| Cache-by-evidence-hash with distinct record hashes | Stage 8 v2 compact cache | Cite |
| Rule provenance | `test_shariah_provenance.py` | Re-run pytest |
| Expert-validation boundary | No `EXPERT_VALIDATED` | Assert in 9.6 |
| Certification boundary | `certification_claim=false`; no “Shariah compliant” label | Assert in 9.6 |

Synthetic governance vectors remain synthetic and labeled. Do not fabricate LendingClub contractual evidence. Do not convert LC rows into “Islamic applications.”

---

## 7. UCI role

UCI Default of Credit Card Clients is the **secondary credit-risk robustness/generalization dataset**.

It is **not**:

- Islamic-finance contractual data
- a temporal replica of LendingClub
- a row-wise match or synthetic applicant link to LendingClub
- an input to Stage 7 L2 / Stage 8 fusion

Stage 2/3 already froze: 30,000 rows; target `default payment next month`; 23 candidate predictors; `ID` excluded; undocumented codes **not recoded**; stratified split seed 42; `merged_with_lendingclub: false`.

### 7.1 Independent pipeline (must remain separately reproducible)

| Step | Specification |
| --- | --- |
| Preprocessing | **New UCI-only** train-fit transformers. Do not apply LendingClub imputers or the 1023-column LC matrix. Preserve undocumented codes as discrete levels. Fit on UCI train only. |
| Candidate credit model | **Frozen U1:** EBM (additive, `interactions=0`) plus L2 logistic regression only. Not a four-family bake-off. Hyperparameters are UCI-specific and train-only; LC weights are not transferred. |
| Metrics | ROC-AUC, PR-AUC, Brier, log loss (`docs/METRIC_DEFINITIONS.md`); ECE with the Stage 5 10 equal-width bin rule if calibrated. |
| Calibration | Platt (and optional isotonic) **fit on UCI validation only**, select with the Stage 5 rule (validation Brier, 0.001 tie → simpler). Do not reuse LC `a,b`. |
| Seeds | Validation: `42, 123, 2024, 3407, 9999`. UCI TEST: **once**, seed 42, after freeze. |
| Confidence intervals | 1000-row percentile bootstrap, `RandomState(42)`, 95%, TEST only, not for selection. |
| Thresholds | **Do not transfer** `0.06/0.69/0.16`. UCI Stage 9 work is initially scoring, calibration, and robustness/generalization. Any later UCI decision threshold must have its **own** pre-specified validation-only procedure; it is not Stage 8 and is not authorized in 9.0. |
| Governance | **Do not run** L2 fusion. U3: at most a dataset-metadata L1 sentence (schema insufficient for applicant-level Shariah determination), not 4,502 rulings. |
| Comparison with LC | Qualitative: ranking discrimination above chance; whether calibration reduces ECE; seed stability. **No** pooled AUC; **no** feature-name alignment (`LIMIT_BAL` is not `loan_amnt`). |

UCI TEST must not be used to choose the UCI family, calibrator, or any LC methodology.

---

## 8. Statistical evaluation plan

This section replaces the empty `docs/statistical_analysis_plan.md` for Stage 9 purposes. It does not execute analyses.

### 8.1 Uncertainty tools already in the repository

- Predictive TEST metrics: percentile bootstrap, `n_bootstrap=1000`, seed 42 (`docs/METRIC_DEFINITIONS.md`).
- Stage 5 paired differences: bootstrap of (calibrated − raw) on the same resampled rows; interval exclusion of zero is **not** treated as a p-value.
- Decision default rates: Wilson 95% CI (`src/evaluation/decision_metrics.py`).
- Seed robustness: mean ± SD and min–max across five seeds on **validation**.

### 8.2 What to use for which claim

| Claim type | Interval / test | Unit | Notes |
| --- | --- | --- | --- |
| ROC-AUC / PR-AUC / Brier / log loss on a frozen TEST | Percentile bootstrap 95% | Row | Cite Stage 4B/5; do not retune |
| ECE | Same bootstrap; declare 10 equal-width bins | Row | MCE intervals are wide; do not over-interpret |
| Platt vs raw on same rows | Paired bootstrap of difference | Row | Already Stage 5 |
| A0 vs A1 ROC-AUC | **None** | — | Scores identical; difference is exactly 0 |
| Approval/review/rejection rates | Wilson 95% on binomial counts | Application | Descriptive |
| Default rate by band/action | Wilson 95% | Application in band | Existing Stage 8 tables |
| Seed mean metric | Mean±SD over 5 seeds | Fitted model | Validation only |
| G0 vs G1 rates | Algebraic function of frozen band counts | Policy | Not a random experiment |
| UCI vs LC AUC | **No statistical test of equality** | Dataset | Different tasks; qualitative only |

### 8.3 Hypothesis tests (only if used)

Do not add p-values for architecture-vs-AUC. If a paired predictive comparison is restated (e.g. Platt vs raw Brier):

| Item | Specification |
| --- | --- |
| Null | Mean paired difference = 0 (descriptive bootstrap, not NHST by default) |
| Alternative | Two-sided difference |
| Unit | TEST (or UCI TEST) row |
| Resampling | 1000 with-replacement row draws, seed 42 |
| Confidence | 95% percentile interval |
| Multiplicity | Primary LC predictive metrics already reported; Stage 9 does not open a new family of TEST tests. Sensitivity tables are not multiplicity-adjusted “winners.” |

No McNemar/DeLong theatre for A0 vs A1 decisions-as-if-they-were-classifiers: the research object is **policy**, and labels in the review band are not operational outcomes.

### 8.4 Metric categories (do not mix)

**Predictive:** ROC-AUC, PR-AUC, Brier, log loss.  
**Calibration:** ECE, MCE, reliability diagrams, paired Brier/log-loss/ECE.  
**Decision policy:** approval/review/rejection rates; counts by band; default rate by band/action; expected normalized cost under **named** assumptions.  
**Governance/audit:** L1 status; L2 status distribution; missing-evidence rate; `NOT_STRUCTURABLE` rate; audit-field completeness; unique `record_reference_hash` count; unique `evidence_hash` count; `evaluation_mode`; `certification_claim`; expert-validation state.

Governance rates are **not** Shariah-compliance rates.

---

## 9. Reproducibility plan

### 9.1 Clean-room checklist

Another researcher, with this repository and the raw files named in Stage 2, should be able to verify:

1. Dataset hashes (LC `207d65b2…`; UCI `56c885f8…`)
2. Split membership (`audit/lendingclub_split_manifest.json`, `audit/uci_split_manifest.json`)
3. Preprocessing schema (Stage 4A report + policy hashes)
4. Selected model (`results/calibration/artifacts/ebm_train_only_seed42.joblib`, SHA-256 `8d373df1…`)
5. Calibration artifact (`platt_calibrator.joblib` `7f05d116…`; `platt_record.json` parameters)
6. Thresholds (`results/decision/frozen_policy.json` SHA-256 `4d3da6a9…`; v2 freeze copies the same `t_low/t_high`)
7. Stage 7 L1/L2 (`src/shariah/l1.py`, `l2.py`; `audit/stage7_v2_governance_run.json`)
8. Stage 8 fusion (`src/decision/stage8_v2.py`; `audit/stage8_v2_decision_fusion_run.json`)
9. Audit records (`results/decision/v2/audit/test_audit_records.csv`)
10. Reported metrics (Stage 4B/5/6/7 v2/8 v2 reports)

### 9.2 Procedure (no execution in this task)

1. Verify raw SHA-256 against `docs/raw_data_manifest.json`.  
2. Verify split assignment hashes.  
3. `python -m pytest tests -q --tb=short`.  
4. Confirm frozen joblibs and `p_selected` hashes against Stage 8 v2 audit.  
5. Confirm `t_low==0.06` and `t_high==0.69` in both v1 and v2 freeze files.  
6. Confirm L1 string and L2 `PER_APPLICATION`.  
7. Confirm Stage 8 v1 artifacts still exist and were not overwritten.  
8. Record Python/library versions as in Stage 4B (`python 3.12.10`, `sklearn 1.9.0`, `interpret 0.7.8`, etc.).  
9. Do not retrain to “confirm” hashes.

`git_commit` is recorded as `null` in prior audits because the workspace was not a git repository. Do not fabricate a commit. If git is later initialized, record the real hash going forward.

### 9.3 Stage 9.0 freeze set

Recorded in `audit/stage9_0_experimental_freeze.json`. Includes: amendment ID; protocol path; O-TEST Option A; U1 EBM+LR; A2-D optional; O-YEAR optional descriptive; R-SEED-POLICY SKIP; Stage 8 `t_low/t_high` frozen; `thresholds_reselected: false`; no experiments executed.

---

## 10. Likely reviewer attacks

| # | Attack | Defensible response | Evidence required |
| --- | --- | --- | --- |
| 1 | “This is just an integration of existing models.” | Agree that EBM, Platt, and SHAP are not the novelty. Novelty is **evidence-separated decision architecture** with an independent governance layer, firewall, L1/L2, and explicit insufficiency handling (`AMENDMENT-SHARIAH-001` §9). | Architecture figure; audit schema; firewall tests; claim matrix. |
| 2 | “There is no real Shariah validation.” | Correct. Rules are `RESEARCH_ARCHITECTURE_NOT_A_RULING` or `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW`. None are `EXPERT_VALIDATED`. The paper must say so. | Stage 7 v2 expert-validation section; catalog. |
| 3 | “LendingClub is not Islamic finance data.” | By design. LC demonstrates an **evidence gap** in conventional lending data, not a Sukuk/Murabahah corpus. | L1 status; missing-evidence list; amendment §4.3. |
| 4 | “Why call it Shariah-aware?” | Use **Shariah-oriented governance and evidence-traceability**, not “Shariah-aware scoring.” The layer evaluates configured contractual/institutional evidence when present. | Safe-wording table; methodology doc. |
| 5 | “Why does nearly everyone go to human review?” | Under G0, LC L2 is insufficient and LOW/MEDIUM map to review; MEDIUM is huge at `t_low=0.06`. That is an honest operational implication of the **stated** policy and evidence gap, not a hidden failure. | Stage 8 v2 review causes (5,232 governance-only; 203,627 both). |
| 6 | “The architecture cannot prove Shariah compliance.” | Agreed; proving compliance is out of scope and forbidden. | Certification-boundary tests; `certification_claim=false`. |
| 7 | “The monolithic baseline is not truly end-to-end.” | Agreed. It is a **monolithic credit-policy comparator** on the same scores. Do not claim a deep Shariah network was beaten. | Stage 8 spec `monolithic_baseline`; table5. |
| 8 | “Cost-sensitive thresholds are assumption-dependent.” | Yes. `{1,2,5,10}` and Experiment G are the answer, not a denial. Primary remains 5:1 by prior freeze. | table2; experiment_g CSV; cost-assumptions doc. |
| 9 | “Why not use text to infer contracts?” | Design B is rejected. `purpose`/`title`/`desc` are not contract evidence. Inferring Murabahah/Ijarah would be an unverified religious/legal leap and is constitutionally banned. | Amendment §4.2–4.4; purpose-invariance tests. |
| 10 | “Why use UCI?” | Secondary **credit-risk** generalization where no timestamp exists. Not a Shariah dataset. Not merged. | Stage 3 UCI split; this protocol §7. |
| 11 | “Does governance improve predictive accuracy?” | **No.** H-N1. Report identical `p_selected` metrics; contrast **decision** rates. | Stage 8 table5 first row: “Architecture does not change ROC-AUC/PR-AUC/Brier.” |
| 12 | “How is this different from rule-based compliance checking?” | Conventional checkers often assume fields exist and output pass/fail. This system **refuses** to treat missing contract fields as fail-or-pass religion, separates L1 dataset readiness from L2 row evidence, firewalled credit features, and fuses only at the decision layer with an audit hash. | L1 vs L2; `INSUFFICIENT_INFORMATION` ≠ `PASS`/`NOT_STRUCTURABLE`; audit records. |

---

## 11. Paper claim matrix

No paper sentence may be used without an artifact. Existing numbers below are **already executed**; they are not Stage 9 results.

| Claim | Evidence required | Existing evidence | Missing evidence | Safe wording |
| --- | --- | --- | --- | --- |
| Evidence-separated architecture is implemented | Code + figure + spec | Stage 8 v2; figure6; specification | Stage 9 execution report (optional citation polish) | “Credit, explainability, and governance evidence are produced separately and fused only at the decision policy.” |
| Same predictive scores under A0 and A1 | Identical `p_selected` | Stage 8 table5; Stage 5 TEST Platt metrics | None for LC seed 42 | “Fusion does not alter calibrated default probabilities or ROC-AUC.” |
| LC lacks contractual evidence for applicant-level determination | L1 + L2 missing list | Stage 7 v2 L1/L2; Stage 8 v2 208,886 `INSUFFICIENT_INFORMATION` | Expert Shariah opinion (not claimed) | “Under the implemented schema, LC does not supply the contractual evidence the governance layer requires.” |
| Per-row L2, not broadcast | Unique record hashes | Stage 8 v2: 208,886 record hashes, 1 evidence hash | None | “Each application has its own audit identity; identical evidence hashes reflect identical missing fields, not a broadcast profile presented as independent inspections.” |
| Purpose is not Shariah evidence | Firewall tests | Stage 7/8 v2 tests | None | “`purpose` is a frozen credit predictor and is not used as contract type.” |
| Cost thresholds are assumption-dependent | Validation table across ratios | table2; Experiment G | None required for citation | “Reported `t_low/t_high` minimize expected cost under stated research cost assumptions, not measured bank costs.” |
| Monolithic comparator has no review band | A4 TEST rates | Stage 8: approve 0.296, review 0, reject 0.704 | None | “The monolithic baseline is a single-threshold credit policy on the same scores, not an end-to-end Shariah model.” |
| Fused LC policy has near-universal review | A1 TEST rates | Stage 8 v2: review 0.999871 | None | “Under the frozen matrix and LC evidence gap, almost all TEST cases are assigned to simulated human review.” |
| Calibration improves ECE on LC TEST overall | Stage 5 bootstrap | Platt ECE 0.020 vs raw 0.038 | None | “Platt reduced TEST ECE relative to raw EBM scores; this is a scoring result, not a governance result.” |
| Calibration transfer can fail by year | Stage 5 year table | 2018 Platt ECE 0.0615 > raw 0.0103 | Decision-by-year (optional) | “Year slices are descriptive; 2018 calibration transfer deteriorated and was not used to refit.” |
| Seed-stable EBM ranking | Stage 4B seed table | ROC-AUC SD ~0.0001 | Five-seed policy thresholds (not required) | “EBM validation metrics were stable across five seeds.” |
| UCI credit generalization | Independent UCI train/calibrate/TEST | Split/audit only | **All UCI modeling** | Only after Stage 9.5: “On a second credit-default dataset with a stratified split, an independently trained credit model …” |
| System is Shariah-compliant | Expert ruling | **None** | Would require real `EXPERT_VALIDATED` records | **Do not claim.** |
| Applicants were Shariah-screened | Contractual evaluation | Contradicted by L1/L2 | — | **Do not claim.** |
| AAOIFI fully implemented | Clause engine | Gates only; SS8 possession `NOT_VERIFIED` | Primary operative text + review | “AAOIFI identity/unavailability gates are implemented; operative clauses are not.” |
| Governance improves AUC | Fused vs credit ROC | Difference is 0 by construction | — | **Do not claim.** |
| Review improves accuracy | Human outcomes | No human-review labels | Would need a review study | “Review is a simulated policy band; no reviewer outcomes were collected.” |
| UCI is temporally validated | Timestamps | `NO_CALENDAR_TIMESTAMPS` | Impossible without new data | **Do not claim.** |

---

## 12. Execution order

Preferred order (**only after** a later, separate `STAGE_9_EXECUTION` authorization; 9.0 is this freeze and is not execution):

```text
Stage 9.0  Experimental freeze          ← this document / audit (DONE as design freeze)
Stage 9.1  Ablations (cite A0/A1/A3=A4/A2-P; optional A2-D on validation)
Stage 9.2  Cost sensitivity (cite validation table2 + Experiment G)
Stage 9.3  Governance-insufficiency sensitivity (synthetic/unit; G0 primary)
Stage 9.4  Credit robustness (cite Stage 4B/5/6 seeds; optional year descriptions)
Stage 9.5  UCI generalization (new modeling only after UCI freeze; UCI TEST once)
Stage 9.6  Reproducibility audit (hashes + pytest; no retraining)
Stage 9.7  Final results freeze (versioned Stage 9 report; do not overwrite Stages 4–8)
```

**Why this order:** freeze first; exhaust artifacts that must not touch TEST; keep the only still-naive TEST (UCI) last among modeling steps; lock hashes before writing the Stage 9 report.

A different order is not scientifically better unless UCI is dropped entirely (then 9.5 is skipped). Do not run UCI before 9.0.

---

## 13. TEST protection

### Before any later TEST (UCI only, after execution authorization)

- Stage 9.0 freeze in force  
- Stage 8 policy **unchanged**  
- No purpose→contract experiments  
- UCI methodology frozen before UCI TEST  

### LendingClub TEST

- **Already evaluated** for A0, A1, A3/A4, and Stage 5 scores  
- **Do not** use LC TEST to choose fusion rules, cost ratio, G-treatment, A3 policy, models, or thresholds  
- **Do not** repeat the Stage 8 v2 fused evaluation  
- **O-TEST = Option A:** no new LC TEST policy remaps  
- Any later additional LC TEST analysis requires explicit owner authorization and must be descriptive only  

### UCI TEST

- **Protected** until a complete UCI methodology freeze and execution authorization  
- Then one evaluation per frozen UCI experiment  
- No tuning; no LC threshold transfer; no L2 fusion  

### After TEST

- Descriptive analysis only  
- No methodology changes based on results  
- Negative findings retained  

---

## 14. Stopping criteria

Stop Stage 9 design/execution and return to the owner if any of the following occurs:

1. A proposed experiment would select thresholds, fusion cells, or G-treatments on TEST.  
2. A proposed experiment infers Islamic contract type from `purpose`, `title`, or `desc`.  
3. A proposed experiment invents AAOIFI operative clauses or reconstructs `SHR-001`.  
4. A proposed experiment fabricates `EXPERT_VALIDATED` or certification claims.  
5. A proposed experiment merges UCI and LendingClub or transfers LC thresholds to UCI as if comparable.  
6. A proposed experiment retrains EBM/Platt “to improve Stage 8.”  
7. An implementer decides an optional item (A2-D, O-YEAR, UCI thresholds) informally during coding rather than from this freeze.  
8. Results would overwrite Stage 8 v1/v2 historical artifacts.  
9. Paper text would claim governance-improved AUC or applicant-level Shariah compliance.

---

## 15. Experiments that are **not** authorized

Even after a later execution approval of this protocol, the following remain **prohibited** unless a new Rule #14 amendment says otherwise:

- Any purpose / title / desc classifier for Murabahah, Ijarah, or “Islamic vs conventional”  
- Asset-backing or possession inference from LC credit fields  
- Numeric Shariah score or `p_adjusted = p_cal + f(governance)`  
- Training EBM/XGB/LR on governance outputs  
- Refitting Platt or re-searching `t_low/t_high` on TEST  
- Replacing Stage 8 primary policy with a TEST-preferred cost ratio  
- Adopting G1/G3/G-unsafe as the religiously correct policy  
- AAOIFI SS(8)/SS(9) clause engines; scraping/inventing clauses  
- Reconstructing `SHR-001`  
- Expert-validation fabrication  
- Human-review outcome simulation presented as real reviewer data  
- Neural/LLM “end-to-end Shariah” model as a silent new baseline  
- Additional LC TEST policy remaps (O-TEST Option A)  
- A3-F fused mapping that silently eliminates `HUMAN_REVIEW`  
- Recoding UCI undocumented values after seeing UCI TEST  
- Changing the LC temporal split or UCI stratified split  
- Stage 10+ paper drafting under this authorization  
- New datasets beyond LC and UCI  

---

## 16. Novelty check (for owner review, not a paper draft)

**Not novel (do not claim):** XGBoost, EBM, SHAP, Platt/isotonic calibration, generic “Islamic finance” vocabulary, cost-sensitive thresholding as a generic OR idea.

**Defensible (amendment §9):** evidence-separated architecture; credit vs governance separation; evidence firewall; L1/L2; explicit insufficient-evidence handling; final-stage fusion; calibrated credit risk plus governance traceability; empirical evidence gap on conventional lending data.

**Reviewer risk:** integration-only papers. Mitigation: keep negative results (review burden, no compliance claim, no AUC lift, 2018 calibration transfer) in the foreground.

---

## 17. Artifact plan

**Created in Stage 9.0 (design freeze only):**

- `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` (this file)
- `audit/stage9_0_experimental_freeze.json`

When **execution** is later authorized, produce versioned outputs under `docs/STAGE_9_*`, `audit/stage9_*`, `results/.../stage9/` without overwriting Stages 4–8.

---

## 18. Freeze status of former open choices

The §0.4 table is authoritative. Summary:

| ID | Status after 9.0 |
| --- | --- |
| O-TEST | **Frozen:** Option A |
| O-A2D | **Frozen as optional** (paper-scope switch; not a missing threshold rule) |
| O-A3F | **Frozen:** binary A3 = Stage 8 `t*=0.16` monolithic policy; A3-F **not specified / not authorized** |
| O-G | **Frozen:** G0 primary; G1/G3 hypothetical engineering cases |
| O-YEAR | **Frozen as optional descriptive** |
| U1 | **Frozen:** EBM + logistic regression |
| U2 | **Frozen:** no LC threshold transfer; scoring/calibration focus |
| U3 | **Frozen:** L1 metadata only; no L2 fusion |
| R-SEED-POLICY | **Frozen:** SKIP |

**Still not specified (do not invent during execution):** a fused (L2-on) policy that has **zero** `HUMAN_REVIEW` outputs. That would be a new matrix, not A3.

**Still optional later (not missing methodology for A1):** A2-D; O-YEAR descriptive tables; a separate UCI decision-threshold procedure if the owner later wants UCI policy rates.

**Fusion matrix and Stage 8 `0.06/0.69`:** frozen. Not open.

---

## 19. Stage 9 execution gate

```text
STAGE_9_EXECUTION = AUTHORIZED FOR STAGE 9.1-9.3 (historical, see DEVIATION-001) AND STAGE 9.4 (per AMENDMENT-STAGE9-4-AUTHORIZATION).
Stages 9.5-9.7 remain unauthorized.
```

`STAGE_9_DESIGN_FREEZE` remains `PASS`. This gate text is attributable to `docs/deviations/DEVIATION-001-stage9-authorization-gap.md` (historical 9.1–9.3 process record; **not** retroactive authorization in `audit/stage9_0_experimental_freeze.json`) and `docs/amendments/AMENDMENT-STAGE9-4-AUTHORIZATION.md` (Stage 9.4; status `APPROVED`, approval date 2026-09-15).

Stage 9.4 UCI methodology (Logistic Regression + EBM) was authorized by that amendment after it became `APPROVED`. XGBoost was outside the approved written scope and remains exploratory per `DEVIATION-001`. Stages 9.5–9.7 remain unauthorized.

### 19.1 Standing rule — runners must not edit authorization

No stage runner may edit its own execution-gate or authorization text going forward.

Execution-gate changes may occur only through a dedicated, dated amendment file created and reviewed BEFORE the corresponding stage's runner is executed.

The Stage 9.4 runner, when eventually created, MUST NOT be permitted to modify: execution authorization, protocol authorization text, amendment status, or Constitution authorization records. Authorization must always be external to the runner.

---

## Document control

| Field | Value |
| --- | --- |
| Protocol ID | `STAGE-9-PROTOCOL-2026-09-15` |
| Protocol freeze version | `stage9.0-design-freeze` |
| Freeze audit | `audit/stage9_0_experimental_freeze.json` (historical; **not** rewritten) |
| Deviation record | `docs/deviations/DEVIATION-001-stage9-authorization-gap.md` |
| Stage 9.4 amendment | `docs/amendments/AMENDMENT-STAGE9-4-AUTHORIZATION.md` (status `APPROVED`, approval date 2026-09-15) |
| Stage 9.1 experiment | `stage9_1_ablation_lc_v1` (`docs/STAGE_9_1_ABLATION_REPORT.md`) |
| Stage 9.2 / 9.3 | Executed; retained as exploratory/sensitivity per `DEVIATION-001` (not confirmatory) |
| TEST used for model/policy selection in Stage 9.1 | **No** |
| Model training in Stage 9.1 | **Not performed** |
| Stage 8 artifacts | **Not modified** |
| Next action | Stage 9 is closed for experimentation. No further Stage 9 experiments should be started without a new prospective amendment. Stages 9.5–9.7 remain unauthorized. Stage 10 is not started. |
