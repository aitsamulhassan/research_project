# Paper drafting protocol

| Item | Value |
| --- | --- |
| **Document ID** | `PAPER-DRAFTING-PROTOCOL` |
| **Date** | 2026-09-16 |
| **Type** | Design / protocol only — **no manuscript** |
| **Experiments run** | **None** |
| **Results modified** | **None** |
| **Models modified** | **None** |
| **Stage 9** | **CLOSED** |
| **Stage 10** | **CLOSED** |
| **Stage 11** | **NOT STARTED** (this protocol does **not** start Stage 11) |
| **Paper drafting** | **NOT STARTED** |

This protocol defines **how** the eventual paper must be written from existing evidence. It does **not** write the paper. It does **not** authorize new experiments. It does **not** modify the Research Constitution, the evidence inventory, or any Stage 2–10 artifact.

**Authoritative evidence source:** `docs/PAPER_EVIDENCE_INVENTORY.md` (C1–C6 applied).  
**Authoritative inventory audit:** `docs/PAPER_EVIDENCE_INVENTORY_AUDIT.md` (`INVENTORY_ACCURACY = PASS_WITH_CORRECTIONS`; corrections C1–C6 subsequently applied to the inventory).  
**Readiness:** `docs/audits/PAPER_PHASE_READINESS_AUDIT.md` — `B. READY FOR PAPER DRAFTING WITH DOCUMENTATION LIMITATIONS`.  
**Closures:** `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md`; `docs/audits/STAGE_10_FINAL_CLOSURE_AUDIT.md`.  
**Constitution (unchanged):** `RESEARCH_CONSTITUTION.md`, especially Rules 1–15. Rule 12: every numerical claim must map to a generated experiment artifact.

Documentation lag (disclose, do not silently rewrite): the constitution still contains a leftover sentence that Stage 10 is not started. Controlling status is Stage 10 **CLOSED**. Older `docs/shariah/SHARIAH_GOVERNANCE_SCOPE.md` still says Stage 8 fusion is not implemented; Stage 8 v2 is the later controlling implementation record.

---

## 0. Binding constraints for this protocol and all later drafts

1. No experiments, scoring, metric recompute, prediction regeneration, calibration refit, threshold search, or policy rewrite.
2. No Stage 9 or Stage 10 reopen.
3. No Stage 11 scientific experiment.
4. No invented citations, results, dataset fields, or Shariah evidence.
5. No Shariah certification, Shariah-compliant system, or applicant-level compliance claim.
6. Stage 9.4 UCI XGBoost remains `EXECUTION-TIME EXPANSION, EXPLORATORY` (`DEVIATION-001`). Not pre-registered, confirmatory, primary validated, confirmed best, or overall superior.
7. Stage 4B LendingClub XGBoost and Stage 9.4 UCI XGBoost must never be merged.
8. Downstream LC pipeline = Stage 5 TRAIN-only EBM + stored Platt `p_selected`, **not** the Stage 4B TRAIN+VALIDATION TEST EBM.
9. Numbers in the paper must be transcribed from existing artifacts (or from the inventory’s already-recorded transcription of those artifacts). Prefer the source JSON/CSV when a rounding question arises.
10. Historical discrepancies are disclosed, not rewritten.

This protocol is **not** a Rule #14 scientific-method amendment. Later drafting still requires a separate owner instruction to write manuscript text.

---

## 1. PAPER PURPOSE AND SCOPE

### 1.1 Legitimate purpose

The paper may describe a **research prototype** that:

- trains and evaluates credit-risk models on a Zenodo LendingClub granting-model extract under a chronological split;
- calibrates a **TRAIN-only** Explainable Boosting Machine (EBM) on validation scores and reports frozen TEST metrics;
- attributes that TRAIN-only EBM with exact additive SHAP on the logit scale (`interactions=0`; TreeSHAP not used);
- implements Shariah-**oriented** governance and evidence-traceability predicates (L1/L2) fused with credit bands only at the decision stage (G0);
- reports policy analyses on frozen `p_selected` (A0 / A1 / A3=A4);
- reports UCI Default of Credit Card Clients as an **independent credit-risk / calibration methodology** context, not as validation of the LendingClub architecture or of Shariah governance.

Executed research-question wording (Stage 9.1 report §2; **not** stub `docs/research_question.md`):

> Does separating credit-risk scoring, explainability, and Shariah-oriented governance into independently validated and auditable evidence layers, fused only at the final decision stage, provide a more transparent and defensible digital-financing pipeline than a monolithic end-to-end classifier without materially sacrificing predictive performance?

The paper may **state** this as the design question. Stage 9.1 does **not** prove operational superiority. Predictive scores are identical across A0/A1/A3; only the decision map changes.

### 1.2 What the paper can legitimately claim

Only inventory §1 freeze-backed / confirmatory items, plus documentation/integrity items labeled as such, plus exploratory items **with their class labels**. Strongest freeze-backed empirical core:

- Two datasets used, hashed, not merged (LC primary; UCI secondary methodology).
- LC nine-predictor policy; chronological TEST n=208,886.
- Stage 4B four-family LC TEST after freeze, including TRAIN+VAL EBM TEST ROC-AUC **0.6799408767429772** (that fit only).
- Frozen decision pipeline: TRAIN-only EBM + validation-fit Platt; TEST raw/Platt ROC-AUC **0.6776693941139847**.
- Downstream artifacts: `results/calibration/artifacts/ebm_train_only_seed42.joblib`; `results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected`).
- Stage 4B vs Stage 5 EBM gap **EXPLAINED** (different fits, same TEST split).
- Thresholds `t_low=0.06`, `t_high=0.69`, `t*=0.16` identified on validation cost scenario.
- TEST policy counts: A0 5232 / 203627 / 27; A1 0 / 208859 / 27; A3/A4 61855 / 0 / 147031.
- LC TEST L2 `INSUFFICIENT_INFORMATION` on all 208,886 rows; not a Shariah ruling.
- Stage 9.4 UCI **LR + EBM** as independent methodology (approved written scope).
- Governance wording: research prototype for Shariah-oriented governance and evidence traceability; not certification.

### 1.3 What the paper cannot claim

All of inventory §11, including: Shariah certification/compliance; applicant-level rulings; `EXPERT_VALIDATED` rules; AAOIFI fully implemented; production/fair-lending/regulatory guarantees; fraud-detection performance; pre-registered 9.4 XGBoost; UCI as architecture or Shariah validation; governance improves AUC; A0/A1/A3 as best/optimal/winner; causal SHAP; Stage 10 confirmatory TEST; treating the two LC EBM ROC-AUC values as one model; reconstructing `SHR-001`; inventing contract evidence; treating `INSUFFICIENT_INFORMATION` as non-compliance.

### 1.4 Contribution boundaries

Allowed contribution framing (design + executed prototype, not a certified product):

1. **Evidence-separated architecture** on LC: credit score, explanation, and governance evidence are separate objects; fusion is a decision map on frozen `p_selected`.
2. **Leakage-controlled LC pipeline** with documented hashes, chronological split, train-only preprocessing, validation-only calibration selection, TEST reporting after freeze.
3. **Transparent EBM reference** (`interactions=0`) with exact additive logit SHAP of **that** model, not ground truth.
4. **Governance/evidence-gap prototype** (L1/L2, G0) demonstrating schema insufficiency on LC, not applicant Shariah determination.
5. **Independent UCI methodology context** for LR/EBM credit/calibration; XGBoost only as exploratory execution-time expansion.

Not a contribution: a new confirmatory TEST after Stage 8; a fraud detector; a certified Islamic-finance engine; proof that governance improves discrimination; proof that XGBoost is superior overall.

---

## 2. AUTHORITATIVE EVIDENCE HIERARCHY

When sources conflict, use this order. Do not average or “reconcile” numbers.

| Rank | Source | Use |
| --- | --- | --- |
| 1 | Frozen result JSON/CSV under `results/` and `audit/` hashes cited by stage reports | Numerical claims |
| 2 | Controlling stage **v2** reports (Stage 7 v2, Stage 8 v2) and Stage 5/6/4B reports | Method and interpretation |
| 3 | `docs/PAPER_EVIDENCE_INVENTORY.md` | Claim class, permitted wording, section map |
| 4 | Stage 9 / Stage 10 **closure** audits | Authorization class, closed-experiment status, documentation limitations |
| 5 | Paper-phase readiness audit | Drafting-safe claim list |
| 6 | Protocols, freeze JSON, amendments, `DEVIATION-001` | Provenance; not a substitute for executed metrics |
| 7 | Historical v1 Stage 7/8 reports | Predecessors only |
| 8 | Stage 0 stubs (`research_question.md`, `contribution_statement.md`, `docs/explainability_protocol.md`) | **Do not cite as finalized** |

**Constitution leftover vs closures:** closures and the inventory control Stage 10 status (**CLOSED**).

### 2.1 Authority by domain

| Domain | Authoritative artifacts |
| --- | --- |
| Datasets | `docs/STAGE_2_DATA_AUDIT_REPORT.md`; `docs/raw_data_manifest.json`; `docs/dataset_decision.md`; `docs/dataset_comparability.md` |
| Splits / features | `docs/STAGE_3_SPLIT_AND_FEATURE_REPORT.md`; `audit/lendingclub_split_manifest.json`; `audit/uci_split_manifest.json`; `docs/lendingclub_feature_policy.csv`; `docs/uci_feature_policy.csv` |
| Preprocessing | `docs/STAGE_4A_PREPROCESSING_REPORT.md`; `docs/lendingclub_preprocessing_policy.csv` |
| LC models (Stage 4B) | `docs/STAGE_4B_MODELING_REPORT.md`; `results/metrics/stage4b_test_metrics.json`; `experiments/stage4b_credit_risk/selected_configurations.json` |
| Downstream LC model | `results/calibration/artifacts/ebm_train_only_seed42.joblib` (SHA-256 `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4`); **not** `results/artifacts/final_explainable_boosting_machine_seed42.joblib` |
| Calibration | `docs/STAGE_5_CALIBRATION_REPORT.md`; `experiments/stage5_calibration/selected_calibration.json`; `results/calibration/artifacts/platt_record.json`; `results/calibration/metrics/stage5_test_metrics.json`; TEST vector `results/calibration/test/ebm_seed42_calibrated.csv` (SHA-256 `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb`) |
| Explainability | `docs/STAGE_6_EXPLAINABILITY_REPORT.md` **limitation + metadata**, not the opening “frozen Stage 4B model” sentence; `results/explainability/artifacts/seed42_attributions.meta.json`; tables `table1`–`table5` |
| Shariah governance | `docs/amendments/AMENDMENT-SHARIAH-001.md`; `docs/shariah_methodology.md`; `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md`; rule catalog / source register; Stage 8 v2 for fusion |
| Decision policies | Stage 8 v1 report + `results/decision/tables/table2_validation_threshold_selection.csv` for threshold **identification**; Stage 8 v2 `results/decision/v2/tables/table3_test_decision_outcomes.csv` for TEST counts (prefer v2 table3 over v1 `monolithic_test.json`); freeze JSON v1/v2 |
| Stage 9 | 9.0 freeze JSON; 9.1–9.4 reports; `DEVIATION-001`; `AMENDMENT-STAGE9-4-AUTHORIZATION`; Stage 9 closure audit |
| Stage 10 | S10-I1 / R1 / A1 / A4 reports and `audit/stage10_*.json`; Stage 10 closure audit |
| Metric definitions | `docs/METRIC_DEFINITIONS.md` |

---

## 3. PAPER DATASETS

Only these two executed datasets. Do not import planning-only or unused downloads (no PaySim, IEEE-CIS, fraud datasets, or extra credit files).

| Dataset | Role | Size / split (inventory) | Target | Split | Must not be described as |
| --- | --- | --- | --- | --- | --- |
| LendingClub granting-model extract (`LC_loans_granting_model_dataset.csv`); Zenodo 10.5281/zenodo.11295916; SHA-256 `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc` | **PRIMARY** credit-risk and decision-architecture setting | 1,347,681 × 15; TRAIN 941,267; VALIDATION 197,528; TEST 208,886; TEST hash `4dfedb1a…` | `Default`; Stage 3 freeze: 1=Charged Off, 0=Fully Paid | Temporal by `issue_month`: TRAIN `<= 2016-03`; VAL `2016-04`–`2017-01`; TEST `>= 2017-02` | Islamic-finance dataset; full application funnel; source of contract-level Shariah fields |
| UCI Default of Credit Card Clients; DOI 10.24432/C55S3H; zip SHA-256 `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602` | **Independent methodology** (credit/calibration only) | 30,000 × 25; TRAIN 20,999; VAL 4,499; TEST 4,502; TEST hash `0783db42…` | `default payment next month` | Stratified 70/15/15 by target, seed 42; `NO_CALENDAR_TIMESTAMPS` | Validation of LC architecture; validation of Shariah governance; equivalent target to LC |

Not merged (`dataset_decision.md` §E; UCI `merged_with_lendingclub: false`). Zenodo is a depositor-filtered Kaggle parent extract (Stage 2); do not treat Kaggle as a third executed dataset. Disclose Stage 2 Zenodo target-documentation conflict; Stage 3 freeze controls the coding.

---

## 4. MODEL AND EXPERIMENT DESCRIPTION

The paper must keep **four contexts** separate. Use these labels in Methods and Results.

| Context ID | Name | Split / fit | Role in paper | Downstream LC decisions? |
| --- | --- | --- | --- | --- |
| **M-4B** | Stage 4B LendingClub families (logistic regression, EBM, random forest, **LC XGBoost**) | After freeze, TEST metrics from TRAIN+VALIDATION refits | Confirmatory **family TEST after freeze** for LC | **No** |
| **M-5** | Stage 5 TRAIN-only EBM + Platt `p_selected` | TRAIN-only EBM (`n_train=941267`); Platt fit on VALIDATION | Frozen LC decision pipeline | **Yes** (Stage 8 onward) |
| **M-9.4-AE** | Stage 9.4 UCI logistic regression and EBM | UCI-local train/val/TEST; approved written scope | Independent methodology; **not** LC architecture validation | **No** |
| **M-9.4-X** | Stage 9.4 UCI XGBoost | Execution-time expansion; `DEVIATION-001`; `EXECUTION-TIME EXPANSION, EXPLORATORY` | Exploratory UCI footnote/subsection only | **No** |

### 4.1 Two LC EBMs (never collapse)

| | Stage 4B TEST EBM (M-4B selected family refit) | Stage 5 raw / Platt TEST (M-5) |
| --- | --- | --- |
| Training split | TRAIN+VALIDATION refit | TRAIN only |
| Preprocessor | `preprocessor_train_plus_validation.joblib` | `lendingclub_preprocessor.joblib` |
| Model dump | `results/artifacts/final_explainable_boosting_machine_seed42.joblib` (SHA-256 **not recorded**) | `results/calibration/artifacts/ebm_train_only_seed42.joblib` |
| TEST n | 208,886 | 208,886 (same Stage 3 TEST) |
| ROC-AUC | 0.6799408767429772 | 0.6776693941139847 |
| Gap | **EXPLAINED** (different fitted models) | Same |
| Stage 8 onward | **No** | **Yes** (`p_selected`) |

Do not describe the gap as calibration changing rank (Platt TEST ROC-AUC equals stored raw). Do not describe it as an unresolved error.

### 4.2 Two XGBoost contexts (never merge)

1. **Stage 4B LC XGBoost** — LC four-family evidence (`stage4b_test_metrics.json`). Not the Stage 8 model.
2. **Stage 9.4 UCI XGBoost** — exploratory execution-time expansion. Not a primary validated LendingClub model.

### 4.3 LC predictors (both LC EBMs)

`revenue`, `dti_n`, `loan_amnt`, `fico_n`, `emp_length`, `purpose`, `home_ownership_n`, `addr_state`, `zip_code` (`docs/lendingclub_feature_policy.csv`).

---

## 5. RESULTS POLICY

Constitution Rule 12 is binding.

1. Every reported number traces to an existing artifact path in the inventory or the stage report it cites.
2. **No new TEST metrics.** No loading of joblibs for scoring during drafting.
3. Transcribe stored values. Inventory rounding of UCI selected ROC-AUC `0.7708780071798891` → `0.770878` is already recorded; if the paper uses more decimals, take them from `uci_test_selected.json`, not from a recompute.
4. Quote LC EBM ROC-AUC with the full inventory precision when space allows: **0.6799408767429772** (4B) and **0.6776693941139847** (5).
5. Stage 9.4 UCI XGBoost selected row (exploratory): ROC-AUC 0.770878; PR-AUC 0.522421; Brier 0.136853; log loss 0.449533; ECE 0.017443. The declared PR-AUC-first rule selected XGBoost **within that exploratory UCI analysis**. That fact does **not** upgrade the class.
6. Do not rank A0/A1/A3 as winner. Do not claim governance improves AUC (scores identical; maps differ).
7. Preserve negative / inconvenient results (Rule 13/15): Stage 4B TEST PR-AUC below validation; 2018 PR-AUC/ECE deterioration; HIGH band n=27; all-TEST insufficiency; degenerate UCI XGBoost five-seed table.
8. Prefer v2 table3 for A3 counts. Cite v1 `monolithic_test.json` only as historical if needed.

### 5.1 Inventory numbers that must not be altered in prose

| Quantity | Value |
| --- | --- |
| Platt `a`, `b` | `1.1988263209549705`, `0.6697765046966161` |
| `t_low`, `t_high`, `t*` | 0.06, 0.69, 0.16 |
| A0 APPROVE / REVIEW / REJECT | 5232 / 203627 / 27 |
| A1 | 0 / 208859 / 27 |
| A3/A4 | 61855 / 0 / 147031 |
| Cost scenario used to **identify** thresholds | FN:FP=5:1, `C_REVIEW=0.25*C_FP` (researcher scenario, not operational cost) |
| S10-R1 year n | 152726 (2017) / 56160 (2018) |

---

## 6. CALIBRATION POLICY

- Base model for calibration: **TRAIN-only** EBM seed 42 (`ebm_train_only_seed42.joblib`), frozen Stage 4B hyperparameters, **not** the Stage 4B TRAIN+VAL TEST EBM.
- Candidates stored: raw, Platt, isotonic. Isotonic stored, **not** selected.
- Fit split: VALIDATION only. Protocol: `validation_only_calibration_no_train_val_calibrator_refit`.
- Selection: validation Brier; 0.001 practical tie; simplicity `raw > platt > isotonic`; `declared_before_test=true` → **Platt**.
- Form: `sigmoid(a * logit(p_raw) + b)`.
- TEST is reporting-only. Do not say calibration improved discrimination.
- All five validation seeds selected Platt (`stage5_seed_stability.json`).
- 2018 ECE deterioration under frozen Platt is **descriptive** (`stage5_temporal.json`), not a new confirmatory TEST.
- Stage 8–10 consume stored `p_selected` = `p_platt` in `ebm_seed42_calibrated.csv`.

---

## 7. EXPLAINABILITY POLICY

From Stage 6 report (method + limitation) and `seed42_attributions.meta.json`:

- EBM `interactions=0`; transparent-model **reference**, not ground truth, not causal, not an approval criterion.
- **TreeSHAP was not used** and is not valid for this first-order GAM.
- Exact additive interventional SHAP on logit / `decision_function` scale: `phi_i(x) = g_i(x_i) - mean_TRAIN g_i`.
- `shap.AdditiveExplainer` was not used (masker / mixed categoricals).
- Platt is a later monotone map and is **not inside** the EBM explanation.
- Sample: 5,000 TEST rows, seed 42; not full TEST.
- Perfect SHAP vs centered-EBM rank agreement is the identity of centered terms, **not** independent confirmation from a second model class.

**C2 provenance limitation (disclose; do not rewrite Stage 6 files):** the Stage 6 report opening sentence says “the frozen Stage 4B model.” Metadata (`model_id=ebm_train_only_seed42`; `stage5_model_path=results/calibration/artifacts/ebm_train_only_seed42.joblib`) and the report limitation identify the TRAIN-only Stage 5 EBM. Paper text must follow metadata/limitation.

---

## 8. SHARIAH GOVERNANCE POLICY

**Required system description:** research prototype for **Shariah-oriented governance and evidence traceability**. Decision-support / evidence-gap handling. **Not** Shariah certification. **Not** a Shariah-compliant or Shariah-approved system.

### 8.1 Four-way separation (must appear)

| Layer | Paper treatment |
| --- | --- |
| A. Verified source/provenance | SBP SGF 2025; SBP IBD Circular 01 of 2012; SECP SGR 2023 Regulation 7; AAOIFI SS 8/9 **identity** URLs |
| B. Implemented predicates | L1 vs L2; source-mapped SBP/SECP rules (`SOURCE_VERIFIED_PENDING_EXPERT_REVIEW`); AAOIFI identity/unavailability gates only; credit-feature firewall; purpose-invariance (`purpose` ≠ contract type) |
| C. Evidence/schema gaps | L1 `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`; L2 `INSUFFICIENT_INFORMATION` all LC TEST; `SH-AAOIFI-SS8-POSSESSION` `NOT_VERIFIED`; `SHR-001` `UNSUPPORTED_RETIRED` |
| D. Unvalidated / unavailable | AAOIFI operative clauses not retrieved/implemented; **no** `EXPERT_VALIDATED` rule |

### 8.2 LendingClub evidence limitation (C6)

- LC does **not** contain contract-level Shariah evidence fields sufficient for applicant-level Shariah compliance determination.
- Do **not** invent Islamic-finance contract information.
- S10-A1-GAP is analysis-only/descriptive decomposition of **existing** governance evidence. It does **not** validate Shariah compliance.
- `INSUFFICIENT_INFORMATION` = insufficient contractual/schema evidence, **not** a Shariah ruling, applicant non-compliance, or proof a contract is non-compliant.
- A1 HUMAN_REVIEW = 208,859 from G0 × insufficiency, **not** from a Shariah score.
- Insufficiency does **not** mean the applicant is religiously non-compliant.

Controlling implementation: Stage 7 **v2** + Stage 8 **v2**. v1 reports are historical predecessors.

---

## 9. STAGE 9 POLICY

Stage 9 remains **CLOSED**. Do not reopen. Do not backdate the 9.0 freeze JSON (`stage9_execution` remains `NOT AUTHORIZED` at freeze time).

| Activity | Authorization class | Paper role | Permitted | Prohibited |
| --- | --- | --- | --- | --- |
| 9.0 | Design freeze | Record A0–A4, thresholds, U1=LR+EBM | “Design freeze recorded” | Treat freeze JSON as having pre-authorized 9.1–9.4 |
| 9.1 | **B** (documentation gap); report PASS | Ablation of frozen maps on previously exposed TEST | Decision counts differ; scores identical | New confirmatory TEST; “governance improves AUC” |
| 9.2 | **C** exploratory | Assumed-`r` cost sensitivity | Exploratory sensitivity under assumed costs | Pre-registered confirmatory ranking; optimal policy |
| 9.3 | **C** exploratory | G0 vs hypothetical G1/G3 | Hypothetical engineering allocation | Religiously correct treatment; G-unsafe as executed |
| 9.4 LR+EBM | Amendment **APPROVED** 2026-09-15 | Independent methodology | UCI credit/calibration context | Validates LC architecture or Shariah |
| 9.4 XGBoost | **C** `DEVIATION-001`; `EXECUTION-TIME EXPANSION, EXPLORATORY` | Exploratory subsection/footnote | Execution-time extension; PR-AUC-first selected XGBoost **within that exploratory analysis** | Primary validated / confirmed best / overall superior / pre-registered / confirmatory; merge with Stage 4B LC XGBoost |

**C4 documentation limitations (disclose):** leftover `DRAFT` wording in the Stage 9 protocol vs approved 9.4 amendment; Stage 9.4 report hash changed after provenance caveat; UCI TEST metric JSON **not** rewritten. Not TEST leakage or fabrication.

Experiment G: cite existing validation CSV only; not a Stage 10 experiment.

---

## 10. STAGE 10 POLICY

Stage 10 remains **CLOSED**. Native Stage 10 activities are **not** confirmatory TEST experiments. Do not present them as a new experimental campaign.

| Activity | Exact class | Paper use | Must not be described as |
| --- | --- | --- | --- |
| S10-I1 | Integrity/provenance check — **not** a scientific confirmatory experiment | A0/A1/A3 share stored `p_selected`; freeze hashes; positional `row_ref` caveat | Independent scientific result |
| S10-R1 | Exploratory/descriptive **post-hoc** reanalysis — non-confirmatory | 2017/2018 mix under frozen maps (n=152726 / 56160) | Confirmatory temporal TEST; year-tuned policy |
| S10-A1-GAP | Analysis-only / descriptive | Algebra of A1 review = LOW+MEDIUM × all-TEST insufficiency | Independent Shariah validation; applicant ruling |
| S10-A4-SIDEBYSIDE | Analysis-only / descriptive comparison | Citation table LC vs UCI; 4B vs 5 **EXPLAINED** | New AUC test; model ranking; UCI architecture validation |

S10-A4 `xgboost_ratified=false`; keep XGBoost off the primary comparison table.

---

## 11. REQUIRED PAPER STRUCTURE

Do not force a section the evidence cannot support. **Related Work has no repository literature file**; it is allowed only as a later external literature-review phase (this protocol does not add citations).

**Working title (not final; no certification language):**  
*Evidence-Separated Credit Scoring, Additive Explainability, and Shariah-Oriented Governance: A Research Prototype on a LendingClub Extract, with Independent UCI Methodology Context*

| Section | Include? | Evidence / rule |
| --- | --- | --- |
| Title | Yes | Working title above; no “Shariah-compliant AI” |
| Abstract | Yes | Inventory §12; encode classes and non-certification; name which EBM |
| Keywords | Yes | From executed study terms only (see §11.1) |
| Introduction | Yes | Stage 9.1 §2 RQ; `dataset_decision.md`; not stub RQ file |
| Related Work | Yes as **later writing**, not from this repo | External literature only; no invented citations in this protocol |
| Research Questions / Contributions | Yes | Design question + contribution boundaries §1.4; protocol hypotheses are **not** proven results; not stub `contribution_statement.md` |
| Materials and Methods (overview) | Yes | Evidence separation; amendment; metric definitions |
| Dataset and Data Governance | Yes | Stage 2–3; two datasets only |
| Temporal Split and Leakage Control | Yes | Stage 3 LC chronological; UCI stratified; train-only preprocess |
| Models | Yes | M-4B / M-5 / M-9.4-AE / M-9.4-X labels |
| Calibration | Yes | Stage 5 Platt policy |
| Explainability | Yes | Stage 6; C2 disclosure |
| Shariah-Oriented Governance | Yes | Prototype + C6; v2 controlling |
| Decision Policy | Yes | G0; A0/A1/A3; thresholds as scenario-identified |
| Experimental Results (LC) | Yes | 4B/5 metrics; table3 counts; explicit A/B/C EBM rows |
| Cross-Dataset / Generalization Analysis | Yes, **labeled independent methodology** | 9.4 LR+EBM freeze-backed; XGBoost exploratory |
| Robustness / Post-hoc Analysis | Yes, **labeled** | S10-I1 integrity; S10-R1 post-hoc; Stage 5 temporal descriptive; 9.2/9.3 only if labeled exploratory |
| Discussion | Yes | Interpretation without new numbers |
| Limitations | Yes | Inventory §10 items 1–24 in full spirit |
| Conclusion | Yes | Supported claims only; restated non-certification |
| References | Yes later | Literature-review phase; none invented here |

Do **not** add a Fraud Detection, Deployment Evaluation, or Expert Validation section. Evidence does not support them.

### 11.1 Keyword candidates (from existing study language)

`credit risk`; `explainable boosting machine`; `probability calibration`; `additive SHAP`; `decision policy`; `Shariah-oriented governance`; `evidence traceability`; `LendingClub`; `temporal split`.  
Do not use `Shariah-compliant`, `certified`, or `fraud detection` as keywords.

---

## 12. FIGURE AND TABLE PLAN

**This protocol does not create figures or tables.** Later manuscript figures/tables may be produced **only** as transcription or layout of existing artifacts.

**Computation permission under closed-experiment state:**

| Class | Permitted now / at drafting? |
| --- | --- |
| Transcribe stored CSV/JSON into a paper table | Yes (documentation) |
| Schematic diagrams with no new numbers (architecture, G0 matrix copied from Stage 8 v2) | Yes (writing) |
| Plot already-stored columns (e.g. bar chart of table3 counts) without model load or metric functions | Yes, as **presentation of stored values**; caption must cite source artifact |
| Load joblib, score rows, recompute ROC/PR/Brier/ECE, refit calibrators, search thresholds | **No** |
| Hash Stage 4B final EBM to “fill” the missing SHA-256 | **No** unless a later owner authorization says otherwise; disclose absence |

| ID | Purpose | Source artifact | Computation? | Permitted? |
| --- | --- | --- | --- | --- |
| Fig-Arch | Evidence-separated layers (credit / explanation / governance / fusion) | Stage 6/7/8 v2 reports; decision policy specification | None | Yes (schematic) |
| Fig-G0 | G0 matrix | Stage 8 v2 G0 table | None | Yes (copy) |
| Tab-Data | Dataset roles, n, hashes, targets, splits | Inventory §2; Stage 2 report; split manifests | None | Yes |
| Tab-4B | LC family TEST metrics | `results/metrics/stage4b_test_metrics.json` | None | Yes |
| Tab-EBM | Stage 4B vs Stage 5 EBM identity | Inventory §3; S10-A4 `ebm_test_roc_discrepancy` / side-by-side tables | None | Yes; required wherever LC ROC-AUC appears |
| Tab-Cal-VAL | Calibration selection | `stage5_validation_comparison.csv`; `selected_calibration.json` | None | Yes |
| Tab-Cal-TEST | Raw/Platt/isotonic TEST | `stage5_test_metrics.json`; `stage5_test_comparison.csv` | None | Yes; state Platt ROC-AUC = raw |
| Tab-Pol | A0/A1/A3 counts | v2 `table3_test_decision_outcomes.csv` | None | Yes |
| Tab-Band | Band default rates | v2 `table3b_test_default_rates_by_band.csv` | None | Yes; HIGH n=27 caveat |
| Tab-Contingency | Credit × governance | v2 `table4_credit_governance_contingency.csv` | None | Yes |
| Tab-SHAP1 | Global attribution | `table1_global_attribution.csv` | None | Yes; not causal |
| Tab-SHAP2 | SHAP–EBM agreement | `table2_shap_ebm_agreement.csv` | None | Yes; identity caveat |
| Tab-UCI-AE | UCI LR/EBM family-raw TEST | `uci_test_family_raw.csv`; S10-A4 citation tables | None | Yes; not architecture validation |
| Tab-UCI-X | UCI XGBoost selected + family-raw | `uci_test_selected.json`; `s10_a4_xgboost_exploratory_not_primary.csv` | None | Yes **only** with class `EXECUTION-TIME EXPANSION, EXPLORATORY` |
| Tab-S10I1 | Integrity statement | S10-I1 report / audit JSON | None | Yes; not a result table of new AUC |
| Tab-S10R1 | Year mix | `s10_r1_year_decision_mix.csv` | None | Yes; post-hoc label |
| Tab-S10A1 | Gap crosstab | `s10_a1_gap_crosstab.csv` | None | Yes; not Shariah validation |
| Tab-Lim | Documentation limitations | Inventory §10 | None | Yes |
| Fig-Cal-reliability | Reliability diagram | Only if an **existing** Stage 5 figure file is reused | Do not recompute bins | Reuse existing artifact only; if none stored as an image, **omit** rather than regenerate from scores |
| 9.2 cost curves | Sensitivity vs `r` | `results/cost_sensitivity/v1/` | None beyond copy | Optional; **exploratory** caption required |
| 9.3 G1/G3 | Hypothetical allocations | Stage 9.3 report | None | Optional; **exploratory / not Shariah findings** |

If a desired figure would require reading `p_selected` and calling `sklearn.metrics`, **omit it**.

---

## 13. CLAIM-TO-EVIDENCE TRACEABILITY

Assign every sentence that asserts a finding to exactly one class.

### Directly supported

Freeze-backed inventory §1 items and readiness audit §11.A: dataset hashes/splits; two LC EBM identities; Platt selection; A0/A1/A3 counts; L1/L2 statuses; G0 definition; UCI LR/EBM as independent methodology; TreeSHAP not used; no `EXPERT_VALIDATED` rule.

### Supported with limitation

Stage 9.1 architecture comparison (class B; previously exposed TEST; maps not scores). Stage 6 attributions (this EBM only; n=5,000; C2 wording). Thresholds as validation cost-scenario identification, not official/operational. S10-I1 / S10-A4 as integrity/citation (positional `row_ref`; missing 4B hash). Missing `git_commit`. AAOIFI identity without clauses.

### Exploratory

9.2 costs; 9.3 G1/G3; 9.4 UCI XGBoost (+ selected isotonic row); S10-R1 year mix; S10-A1 algebra (not Shariah validation); Stage 4B/5 2017–2018 metric slices; Experiment G.

### Must not be claimed

Inventory §11 in full. Especially: certification; applicant compliance; fraud performance; pre-registered/primary/best/superior UCI XGBoost; merged XGBoost contexts; UCI validates LC architecture; governance improves AUC; causal SHAP; Stage 10 confirmatory TEST; 4B and 5 EBM as one model; `INSUFFICIENT_INFORMATION` as a ruling.

---

## 14. WRITING RULES

1. Formal academic English. No marketing (“industry-leading”, “guarantees”, “production-ready”).
2. No unsupported novelty (“first certified Shariah AI”, “state-of-the-art fraud detector”).
3. No exaggerated performance; quote stored metrics with context (selection bias; TEST vs VAL drop).
4. No causal claims from SHAP, EBM terms, or year slices.
5. No hidden limitations: inventory §10 items 1–24 must be representable in Limitations (not necessarily as 24 bullets, but none silently dropped).
6. Historical discrepancies disclosed (Stage 6 opening vs metadata; protocol leftover DRAFT; constitution leftover Stage 10 sentence; `SHARIAH_GOVERNANCE_SCOPE.md` lag). Do not silently rewrite those historical files during drafting unless a later documentation-only task authorizes it.
7. Class labels travel with results (B/C, post-hoc, analysis-only, exploratory).
8. Prefer “research prototype”, “evidence gap”, “decision map”, “stored `p_selected`” over “approval engine” / “compliant loan”.
9. Do not personify the system as a Shariah Board.
10. When in doubt, omit the claim.

---

## 15. CITATION POLICY

**This protocol does not search the web and does not add bibliographic citations.**

| Needs external literature (later review phase) | Must **not** be invented from the repo |
| --- | --- |
| Related work on credit scoring, calibration, GAMs/EBMs, SHAP, Islamic-finance governance standards as **published** texts | Fake papers, fake DOIs, or “as shown in prior work” without a real source |
| Standard citations for sklearn/EBM/XGBoost software, UCI dataset, Zenodo deposit | Citing unused datasets as if used |
| Discussion of SBP/SECP/AAOIFI **as named in the source register** | Quoting AAOIFI operative clauses that were never retrieved |

Repository artifacts are cited as **data/software provenance** (paths, hashes, reports), not as peer-reviewed literature.

A separate literature-review task must verify current citations before Related Work is considered complete. Until then, Related Work remains a placeholder section in the outline, not a drafted bibliography.

---

## 16. DRAFTING WORKFLOW

**Current gate:** protocol created; paper text **not** started. Drafting begins only after an explicit later owner instruction. That instruction would be a **writing** authorization. It is **not** Stage 11 and **not** a new experiment.

Proposed sequence after approval of this protocol:

| Step | Activity | Check against | Forbidden |
| --- | --- | --- | --- |
| 0 | Keep this protocol and inventory frozen unless a documentation correction is separately authorized | Inventory C1–C6 already applied | Editing results |
| 1 | Literature-review phase (external sources only) | Citation policy §15 | Invented citations; new experiments |
| 2 | Draft Title + Abstract + Keywords | Inventory §1, §11, §12 Abstract row | Certification; unnamed EBM; ranking |
| 3 | Draft Introduction + RQ/Contributions | Stage 9.1 §2; this protocol §1.4 | Stub RQ/contribution files as finalized |
| 4 | Draft Data + Split + Leakage | Stage 2–3; two datasets only | Extra datasets |
| 5 | Draft Models + Calibration | M-4B vs M-5 vs M-9.4; Platt | Mixing joblibs |
| 6 | Draft Explainability | Stage 6 metadata; C2 | TreeSHAP; causality |
| 7 | Draft Governance + Decision Policy | v2 reports; C6; table3 | Applicant rulings |
| 8 | Draft LC Results | 4B/5 JSON; table3; no new metrics | Winner language |
| 9 | Draft UCI subsection | LR+EBM vs exploratory XGBoost | Architecture validation |
| 10 | Draft Robustness (S10 + temporal + optional 9.2/9.3) | Exact S10 class strings | Confirmatory Stage 10 |
| 11 | Draft Discussion + Limitations + Conclusion | Inventory §10 and §11 | New numbers; omitted limitations |
| 12 | Insert Related Work from step 1 | External sources | Repo-invented papers |
| 13 | Claim audit: tag every result sentence Direct / Limited / Exploratory / Forbidden | This protocol §13 | Upgrading exploratory → confirmatory |
| 14 | Number audit: every numeral → artifact path | Rule 12; inventory | Recompute |
| 15 | Manuscript freeze; still no Stage 11 | Closures remain CLOSED | Experiments |

Each step 2–12 produces manuscript text only. Continuous check: if a sentence is not supported by `docs/PAPER_EVIDENCE_INVENTORY.md`, delete or relabel it. Do not fill holes with new runs.

---

## Protocol close

```text
PAPER_DRAFTING_PROTOCOL_STATUS = COMPLETE
PAPER_DRAFTING = NOT_STARTED
STAGE_9_STATUS = CLOSED
STAGE_10_STATUS = CLOSED
STAGE_11_STATUS = NOT_STARTED
EXPERIMENTS_RUN = NONE
RESULTS_MODIFIED = NONE
MODELS_MODIFIED = NONE
```

This protocol is the drafting **design**. It is not the paper. It does not start Stage 11. It does not modify the evidence inventory or any Stage 2–10 science artifact.
