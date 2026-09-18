# Paper evidence inventory

| Item | Value |
| --- | --- |
| **Document ID** | `PAPER-EVIDENCE-INVENTORY` |
| **Date** | 2026-09-16 |
| **Type** | Inventory only — no paper text |
| **Experiments run** | **None** |
| **Results modified** | **None** |
| **Models modified** | **None** |
| **Stage 9** | **CLOSED** |
| **Stage 10** | **CLOSED** |
| **Paper drafting** | **NOT STARTED** |

This file maps planned paper sections to **existing** repository artifacts. It does not write the paper. It does not add datasets, numbers, or claims.

Controlling readiness record: `docs/audits/PAPER_PHASE_READINESS_AUDIT.md`.  
Controlling closures: `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md`; `docs/audits/STAGE_10_FINAL_CLOSURE_AUDIT.md`.  
Documentation corrections C1–C6 from `docs/PAPER_EVIDENCE_INVENTORY_AUDIT.md` applied 2026-09-16. No metrics, sample sizes, thresholds, hashes, model results, or evidence classifications were changed.

---

## 1. PAPER CLAIM BOUNDARIES

### Freeze-backed / confirmatory (cite as executed, frozen science)

Use only with the original stage provenance. Stage 10 did **not** convert these into “Stage 10 confirmatory experiments.”

- Stage 2–3 LC/UCI acquisition, hashes, feature policy, chronological LC split, stratified UCI split.
- Stage 4A train-only LC preprocessor.
- Stage 4B LC family validation selection and one TEST evaluation after freeze (TRAIN+VALIDATION refit TEST metrics). Stage 4B **LendingClub XGBoost** is one of those LC families; it is **not** Stage 9.4 UCI XGBoost.
- Stage 5 TRAIN-only EBM; validation-only calibrator fit/selection; TEST reporting of raw/Platt/isotonic. Downstream artifact: `results/calibration/artifacts/ebm_train_only_seed42.joblib`.
- Stage 6 attributions on the frozen TRAIN-only EBM (descriptive of that model, not a second confirmatory predictor). Stage 6 report opening language vs metadata: see §5 (documentation/provenance limitation; historical Stage 6 records not rewritten).
- Stage 7 v2 L1/L2 prototype implementation and synthetic tests (governance evidence, not religious certification).
- Stage 8 v1 validation threshold identification (`t_low`, `t_high`, `t*`); Stage 8 v2 TEST fusion counts on stored `p_selected`.
- Stage 9.4 **Logistic Regression + EBM** UCI family TEST (approved written scope), as methodology generalization only.

### Documentation-only / integrity (cite as provenance, not new science)

- `AMENDMENT-SHARIAH-001`, Stage 9/10 protocols, `DEVIATION-001`.
- S10-I1 identity/hash check.
- S10-A4 citation tables (no new AUC).
- Freeze JSON files and recorded SHA-256 values.
- `docs/METRIC_DEFINITIONS.md`.

### Exploratory / descriptive / class-qualified (cite only with that label)

- Stage 9.1: previously exposed LC TEST ablation; authorization **class B**.
- Stage 9.2 cost sensitivity: **class C** exploratory.
- Stage 9.3 G1/G3: **class C** hypothetical engineering.
- Stage 9.4 **XGBoost**: `EXECUTION-TIME EXPANSION, EXPLORATORY`; **class C**; `DEVIATION-001`. Not a primary validated model; not the confirmed best / overall superior model; not pre-registered or confirmatory. Distinct from Stage 4B LC XGBoost.
- S10-R1 year mix: **exploratory / descriptive post-hoc**, non-confirmatory.
- S10-A1-GAP: **analysis-only / descriptive** evidence-gap algebra.
- Experiment G: cite-only from existing validation CSV; not a Stage 10 experiment.
- Stage 4B/5 temporal 2017 vs 2018 metric slices (descriptive, not a new inferential TEST).

### Unsupported / prohibited

See §11. Includes Shariah certification, applicant-level compliance, treating `INSUFFICIENT_INFORMATION` as a Shariah ruling, production performance, fraud-detection claims, pre-registered UCI XGBoost, UCI XGBoost as primary/best/superior, merging Stage 4B LC XGBoost with Stage 9.4 UCI XGBoost, UCI-as-architecture-validation, causal SHAP, treating Stage 4B and Stage 5 EBM TEST ROC-AUC as the same model.

`docs/research_question.md` and `docs/contribution_statement.md` are Stage 0 stubs (“To be finalized…”). Do **not** treat them as finalized paper text. The executed research-question wording is in `docs/STAGE_9_1_ABLATION_REPORT.md` §2.

---

## 2. DATASETS

Only two datasets were acquired and used in the executed study. Do not import unused planning datasets.

### LendingClub granting-model extract (primary)

| Field | Recorded value |
| --- | --- |
| Name | LendingClub granting-model extract (`LC_loans_granting_model_dataset.csv`) |
| Role | **PRIMARY** credit-risk / decision-architecture dataset |
| Target | `Default`; Stage 3 freeze: `1` = Charged Off, `0` = Fully Paid |
| Full-file rows | 1,347,681 × 15 (Stage 2) |
| Split rows | TRAIN 941,267; VALIDATION 197,528; TEST 208,886 |
| Split methodology | Temporal by `issue_month`: TRAIN `<= 2016-03`; VALIDATION `2016-04`–`2017-01`; TEST `>= 2017-02` |
| Source / provenance | Zenodo DOI 10.5281/zenodo.11295916; license CC-BY-4.0; SHA-256 `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc` |
| TEST hash | `4dfedb1ad7785fa3833047135b1883676f3e1b49aca9c87fcdb346e64fd489c6` |
| Belongs in final paper | **Yes** — primary empirical setting |
| Artifacts | `docs/STAGE_2_DATA_AUDIT_REPORT.md`; `docs/STAGE_3_SPLIT_AND_FEATURE_REPORT.md`; `docs/raw_data_manifest.json`; `audit/lendingclub_split_manifest.json`; `docs/dataset_decision.md` |

Not Islamic data. Not a full application funnel (rejected applicants absent). Depositor already filtered the parent Kaggle extract (Stage 2). The LendingClub extract does **not** contain contract-level Shariah evidence fields sufficient for applicant-level Shariah compliance determination (see §6 and §10).

### UCI Default of Credit Card Clients (secondary methodology)

| Field | Recorded value |
| --- | --- |
| Name | UCI Default of Credit Card Clients |
| Role | **Independent credit-risk / calibration methodology** generalization only |
| Target | `default payment next month` (`1` = default next month) |
| Full-file rows | 30,000 × 25 (Stage 2) |
| Split rows | TRAIN 20,999; VALIDATION 4,499; TEST 4,502 |
| Split methodology | Stratified 70/15/15 by target, seed 42; `NO_CALENDAR_TIMESTAMPS` |
| Source / provenance | UCI dataset 350; DOI 10.24432/C55S3H; zip SHA-256 `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602` |
| TEST hash | `0783db42ac57a277f79379e0a62ef00f2a2b189f868ed993cebdf16def404126` |
| Belongs in final paper | **Yes**, as a **separate** methodology-context study — **not** as validation of LC architecture or Shariah governance |
| Artifacts | Stage 2 report; `audit/uci_split_manifest.json`; `docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md`; `docs/uci_feature_policy.csv` |

### Datasets that must **not** be presented as used

No fraud, PaySim, IEEE-CIS, or other credit datasets appear in Stage 2 acquisition or later executed stages. Do not add them from older planning notes. The two datasets were **not** merged (`dataset_decision.md` §E; UCI split `merged_with_lendingclub: false`).

---

## 3. CREDIT-RISK EVIDENCE

Downstream (Stage 8 onward) uses the **Stage 5 TRAIN-only EBM** and stored Platt **`p_selected`**, **not** the Stage 4B TRAIN+VALIDATION TEST EBM.

**Downstream identity (do not substitute):**

| Role | Artifact |
| --- | --- |
| Downstream model | `results/calibration/artifacts/ebm_train_only_seed42.joblib` (Stage 5 TRAIN-only EBM; recorded SHA-256 `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4`) |
| Downstream probability | `results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected`) |
| Not used downstream | `results/artifacts/final_explainable_boosting_machine_seed42.joblib` (Stage 4B TRAIN+VALIDATION TEST EBM; SHA-256 **not recorded**) |

| Stage | What it contributes | Downstream? | Exact artifacts |
| --- | --- | --- | --- |
| 4B | Four-family LC modeling (logistic regression, EBM, random forest, **LC XGBoost** — see two-XGBoost note below); validation selection; TRAIN+VAL TEST EBM ROC-AUC **0.6799408767429772** | **No** for later decisions | `docs/STAGE_4B_MODELING_REPORT.md`; `results/metrics/stage4b_test_metrics.json`; `results/predictions/test/explainable_boosting_machine_seed42.csv`; dump path `results/artifacts/final_explainable_boosting_machine_seed42.joblib` (**hash not recorded**) |
| 5 | TRAIN-only EBM raw TEST ROC-AUC **0.6776693941139847**; Platt same ROC-AUC; frozen `p_selected` | **Yes** | `results/calibration/artifacts/ebm_train_only_seed42.joblib`; `results/calibration/test/ebm_seed42_calibrated.csv`; remainder in §4 |
| 6 | Attributions on TRAIN-only EBM | Explainability section only | See §5 |
| 8 | Policy on stored `p_selected`; predictive TEST row cites Stage 5 | Decision fusion | `results/decision/v2/metrics/predictive_test_stage5.json`; freeze JSONs |
| 9.1 | A0/A1/A3 maps on same `p_selected`; scores unchanged | Ablation (class B) | `docs/STAGE_9_1_ABLATION_REPORT.md`; `audit/stage9_1_ablation_run.json` |
| 9.4 | UCI-local models; LC cited not rescored | UCI section only | Stage 9.4 report; `results/uci_generalization/v1/metrics/lendingclub_test_citation.json` |
| 10 | Identity, year mix, A1 gap, citation comparison | Integrity / descriptive | S10 reports |

### Stage 4B vs Stage 5 EBM (must appear wherever LC ROC-AUC is quoted)

| | Stage 4B TEST EBM | Stage 5 raw / Platt TEST |
| --- | --- | --- |
| Training split | TRAIN+VALIDATION refit | TRAIN only (`n_train=941267`) |
| Preprocessor | `preprocessor_train_plus_validation.joblib` | `lendingclub_preprocessor.joblib` |
| TEST n | 208,886 | 208,886 (same Stage 3 TEST) |
| ROC-AUC | 0.6799408767429772 | 0.6776693941139847 |
| Classification of the gap | **EXPLAINED** (different fitted models) | Same |
| Used by Stage 8 onward | **No** | **Yes** (`p_selected`) |

Do not treat the two ROC-AUC values as a contradiction or as calibration changing rank for Platt vs raw.

### Two distinct XGBoost contexts (do not merge)

These are **not** one “XGBoost result.”

1. **Stage 4B LendingClub XGBoost** — one family in the original LC four-family modeling evidence (`docs/STAGE_4B_MODELING_REPORT.md`; `results/metrics/stage4b_test_metrics.json`). It belongs to LC Stage 4B family TEST after freeze. It is **not** the Stage 9.4 UCI XGBoost run and is **not** the downstream Stage 8 model (downstream is the Stage 5 TRAIN-only EBM).
2. **Stage 9.4 UCI XGBoost** — execution-time model-scope expansion under `DEVIATION-001`; class **`EXECUTION-TIME EXPANSION, EXPLORATORY`**. UCI-local only. It is **not** a primary validated LendingClub model.

Primary predictors (both LC EBMs): `revenue`, `dti_n`, `loan_amnt`, `fico_n`, `emp_length`, `purpose`, `home_ownership_n`, `addr_state`, `zip_code` (`docs/lendingclub_feature_policy.csv`).

---

## 4. CALIBRATION EVIDENCE

Do not recompute. Cite stored files.

| Item | Artifact / recorded fact |
| --- | --- |
| Raw TRAIN-only scores (VAL) | `results/calibration/raw/ebm_train_only_seed42_validation.csv` |
| Raw TRAIN-only scores (TEST) | `results/calibration/raw/ebm_train_only_seed42_test.csv` |
| Platt | `results/calibration/artifacts/platt_record.json`; `a=1.1988263209549705`, `b=0.6697765046966161`; form `sigmoid(a * logit(p_raw) + b)`; fit_split=`validation` |
| Isotonic | `results/calibration/artifacts/isotonic_record.json` (stored; not selected) |
| Validation metrics | `results/calibration/metrics/stage5_validation_metrics.json`; `results/calibration/tables/stage5_validation_comparison.csv` |
| Selection rule | `experiments/stage5_calibration/selected_calibration.json`: validation Brier; 0.001 tie; simplicity `raw > platt > isotonic`; `declared_before_test=true` |
| Final selected calibration | **Platt** |
| Calibrated VAL/TEST frames | `results/calibration/validation/ebm_seed42_calibrated.csv`; `results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected` = `p_platt`) |
| TEST metrics | `results/calibration/metrics/stage5_test_metrics.json`; report `docs/STAGE_5_CALIBRATION_REPORT.md` |
| TEST vector SHA-256 | `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb` |
| Seed-stability (VAL selection) | `results/calibration/metrics/stage5_seed_stability.json` (all five seeds selected Platt) |
| Temporal TEST slices | `results/calibration/metrics/stage5_temporal.json` (descriptive; 2018 ECE deterioration under frozen Platt) |
| Protocol | `validation_only_calibration_no_train_val_calibrator_refit` |

Metric definitions: `docs/METRIC_DEFINITIONS.md` (ROC-AUC = `sklearn.metrics.roc_auc_score`). ECE: Stage 5, 10 equal-width bins.

---

## 5. EXPLAINABILITY EVIDENCE

Report: `docs/STAGE_6_EXPLAINABILITY_REPORT.md` (`STAGE_6_STATUS = PASS`).

| Artifact | Use |
| --- | --- |
| `results/explainability/tables/table1_global_attribution.csv` | Global mean \|SHAP\| / EBM ranks |
| `results/explainability/tables/table2_shap_ebm_agreement.csv` | Rank agreement |
| `results/explainability/tables/table3_seed_stability.csv` | Seed ranks |
| `results/explainability/tables/table4_local_cases.csv` | Local cases |
| `results/explainability/tables/table5_top_feature_effects.csv` | Category/numeric effects |
| `results/explainability/metrics/shap_vs_ebm_agreement.json` | Agreement metrics |
| `results/explainability/artifacts/seed42_attributions.meta.json` | Model path = Stage 5 TRAIN-only EBM (`model_id=ebm_train_only_seed42`; `stage5_model_path=results/calibration/artifacts/ebm_train_only_seed42.joblib`) |
| `results/explainability/sample/explanation_sample_row_refs.csv` | 5,000 TEST row_refs |

**Can claim:** EBM `interactions=0`; additive structure; exact additive SHAP on logit scale `phi_i = g_i(x_i) - mean_TRAIN g_i`; TreeSHAP was not used; attributions of **this** EBM; sample n=5000, seed 42; Stage 6 uses TRAIN-only EBM, not Stage 4B TEST EBM.

**Cannot claim:** SHAP as causality; SHAP as independent confirmation of a second model class (identity of centered terms); probability-space KernelSHAP; explanations as approval criteria; ground-truth feature importance.

**Stage 6 provenance wording discrepancy (documentation/provenance limitation; historical Stage 6 records not rewritten):** the Stage 6 report opening sentence refers to “the frozen Stage 4B model.” The Stage 6 metadata (`seed42_attributions.meta.json`) and the Stage 6 report limitation identify the **TRAIN-only** EBM used by Stage 5 (`results/calibration/artifacts/ebm_train_only_seed42.joblib`), not `results/artifacts/final_explainable_boosting_machine_seed42.joblib`. Paper writers must follow the metadata/limitation, not the opening family phrasing.

---

## 6. SHARIAH GOVERNANCE EVIDENCE

Controlling implementation: Stage 7 **v2** + Stage 8 **v2**. Stage 7/8 **v1** reports are historical.

### Verified source / provenance

- `docs/amendments/AMENDMENT-SHARIAH-001.md` (`APPROVED`)
- `docs/shariah_methodology.md`
- `docs/shariah/SHARIAH_RULE_CATALOG.md`; `docs/shariah/rule_catalog.json`
- `docs/shariah_source_register.md`; `docs/shariah/source_register.json`
- `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md`
- SBP SGF 2025; SBP IBD Circular 01 of 2012; SECP SGR 2023 Regulation 7 (scope: `docs/shariah/SHARIAH_GOVERNANCE_SCOPE.md`)
- AAOIFI SS 8 / SS 9 **identity** URLs; operative clauses **not** retrieved (access control / copyrighted viewer; Stage 7 v1 report)

### Implemented governance predicates

- L1 dataset readiness vs L2 per-application evaluation
- Executable architecture gates and source-mapped SBP/SECP rules (`SOURCE_VERIFIED_PENDING_EXPERT_REVIEW`)
- AAOIFI **identity/unavailability gates** only (`SH-AAOIFI-SS8-GATE`, `SH-AAOIFI-SS9-GATE`)
- Evidence firewall: credit fields excluded from Shariah evidence object
- `purpose` is not contract type (purpose-invariance tests)

### Evidence-gap findings

- LC L1: `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`
- LC TEST L2: `INSUFFICIENT_INFORMATION` on all 208,886 rows (S10-A1; Stage 8 v2)
- A1 HUMAN_REVIEW = 208,859 from G0 × insufficiency, not from a Shariah score
- `SH-AAOIFI-SS8-POSSESSION`: `NOT_VERIFIED`, not executable
- `SHR-001`: `UNSUPPORTED_RETIRED`
- LendingClub does **not** contain contract-level Shariah evidence fields sufficient for applicant-level Shariah compliance determination.
- S10-A1-GAP is an **analysis-only / descriptive** decomposition of **existing** governance evidence. S10-A1 does **not** validate Shariah compliance.
- `INSUFFICIENT_INFORMATION` is an evidence-gap status. It must **not** be described as a Shariah ruling, an applicant non-compliance finding, or proof that a contract is non-compliant.

### What is NOT validated

- Certification; applicant-level Shariah compliance; expert validation (`EXPERT_VALIDATED` = none); AAOIFI operative clauses; Islamic-market data; G1/G3 as religious findings.

Wording: **research prototype for Shariah-oriented governance and evidence traceability**. The governance layer is **decision-support / evidence-gap handling**, not Shariah certification. Not a Shariah-compliant or certified system.

---

## 7. DECISION-FUSION EVIDENCE

| Item | Freeze-backed vs exploratory | Artifacts |
| --- | --- | --- |
| Threshold identification (VAL) | Freeze-backed Stage 8 v1 | `docs/STAGE_8_DECISION_POLICY_REPORT.md`; `results/decision/tables/table2_validation_threshold_selection.csv`; `results/decision/frozen_policy.json` |
| G0 matrix | Freeze-backed | `docs/decision_policy_specification.md`; Stage 8 v2 report |
| A0 TEST counts 5232 / 203627 / 27 | Freeze-backed Stage 8 v2 / 9.1 | `results/decision/v2/tables/table3_test_decision_outcomes.csv` (`credit_only_selected_bands`) |
| A1 TEST counts 0 / 208859 / 27 | Freeze-backed Stage 8 v2 / 9.1 | table3 `fused_evidence_separated_v2`; `results/decision/v2/metrics/fused_test.json` |
| A3/A4 TEST counts 61855 / 0 / 147031 | Freeze-backed Stage 8 v2 / 9.1 (`a3_identical_to_a4`) | table3 `monolithic_credit_threshold`; `results/decision/metrics/monolithic_test.json` |
| Band default rates | Freeze-backed descriptive | `results/decision/v2/tables/table3b_test_default_rates_by_band.csv` |
| Credit × governance contingency | Freeze-backed | `results/decision/v2/tables/table4_credit_governance_contingency.csv` |
| Predictive TEST (Stage 5 cite) | Freeze-backed citation | `results/decision/v2/metrics/predictive_test_stage5.json` |
| Stage 9.2 costs by `r` | **Exploratory** class C | `docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md` |
| Stage 9.3 G1/G3 | **Exploratory** hypothetical | `docs/STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md` |
| Experiment G | Cite-only, not rerun | `results/decision/tables/experiment_g_review_cost_perturbation.csv` |

`t_low=0.06`, `t_high=0.69`, `t*=0.16`. Assumed cost FN:FP=5:1, `C_REVIEW=0.25*C_FP` — researcher scenario, not operational cost.

These are **policy analyses on frozen `p_selected`**, not real-world approval performance.

v2 freeze SHA-256 (recorded): `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b`.  
v1 freeze SHA-256 (recorded): `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4`.  
table3 SHA-256 (recorded): `90759eb72f1173b40b5b9363c21b0ef3d6f1cde5042748eb57871d49fb73d5ee`.

---

## 8. STAGE 9 EVIDENCE

Stage 9 is **CLOSED**. Do not reopen.

| Activity | Classification | Purpose | Artifacts | Confirmatory vs exploratory | Permitted wording | Prohibited wording |
| --- | --- | --- | --- | --- | --- | --- |
| 9.0 | Design freeze | Freeze A0–A4, thresholds, U1=LR+EBM | `audit/stage9_0_experimental_freeze.json`; `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` | Freeze record | “Design freeze recorded …” | Rewriting freeze as if later stages were pre-authorized in that JSON |
| 9.1 | Auth **class B**; report `STAGE_9_1_STATUS=PASS` | Ablation A0/A1/A3 on stored `p_selected` | `docs/STAGE_9_1_ABLATION_REPORT.md`; `audit/stage9_1_ablation_run.json` | Descriptive re-analysis of **previously exposed** TEST | “On frozen maps, decision counts differ; scores identical” | “New confirmatory TEST experiment”; “governance improves AUC” |
| 9.2 | Auth **class C**; report PASS | Frozen counts under alternative `r` | `docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md`; `results/cost_sensitivity/v1/` | **Exploratory / sensitivity** | “Exploratory cost sensitivity under assumed r” | “Pre-registered confirmatory cost ranking”; “optimal policy” |
| 9.3 | Auth **class C**; report PASS | G0 observed vs G1/G3 hypothetical | `docs/STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md`; `audit/stage9_3_governance_sensitivity_run.json` | **Exploratory**; G1/G3 not empirical Shariah | “Hypothetical engineering allocation” | “Religiously correct treatment”; G-unsafe as executed |
| 9.4 LR+EBM | Prospective amendment APPROVED; methodology generalization | UCI-local train/val/TEST | `docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md`; `results/uci_generalization/v1/tables/uci_test_family_raw.csv` | Freeze-backed **for approved families**, not LC architecture validation | “Independent credit/calibration methodology context” | “Validates the LC evidence-separated system”; “validates Shariah” |
| 9.4 XGBoost | **`DEVIATION-001`: UNAUTHORIZED BUT SCIENTIFICALLY VALID POST-FREEZE ANALYSIS**; class **`EXECUTION-TIME EXPANSION, EXPLORATORY`** | Execution-time UCI family expansion; **not** Stage 4B LC XGBoost | Same report provenance caveat; `uci_test_selected.json` (XGB+isotonic) | **Exploratory**; not pre-registered | “Exploratory execution-time extension”; “declared PR-AUC-first rule selected XGBoost within that exploratory UCI analysis” | “Primary validated model”; “confirmed best model”; “overall superior model”; “pre-registered/confirmatory”; “Approved Stage 9.4 protocol included XGBoost”; merging with Stage 4B LC XGBoost |

UCI selected executed pipeline (exploratory because of family scope): XGBoost + isotonic; TEST ROC-AUC 0.770878; PR-AUC 0.522421; Brier 0.136853; log loss 0.449533; ECE 0.017443 (`results/uci_generalization/v1/metrics/uci_test_selected.json`). The declared PR-AUC-first rule selected XGBoost **within that exploratory UCI analysis**. That selection does **not** make XGBoost the primary validated model, the confirmed best model, an overall superior model, or a pre-registered/confirmatory outcome. Permitted class only: **`EXECUTION-TIME EXPANSION, EXPLORATORY`**. Five-seed XGBoost validation table is degenerate. Do not merge this result with Stage 4B LendingClub XGBoost.

---

## 9. STAGE 10 EVIDENCE

Stage 10 is **CLOSED**. Native Stage 10 activities are **not** confirmatory TEST experiments.

| Activity | Exact classification | Status | Paper contribution | Must not be treated as |
| --- | --- | --- | --- | --- |
| S10-I1 | `INTEGRITY / PROVENANCE CHECK — NOT A SCIENTIFIC CONFIRMATORY EXPERIMENT` | `PASS WITH DOCUMENTATION LIMITATION` | A0/A1/A3 share `p_selected`; freeze hashes; positional audit caveat | Independent scientific result |
| S10-R1 | `EXPLORATORY / DESCRIPTIVE POST-HOC REANALYSIS — NON-CONFIRMATORY` | `COMPLETED` | 2017/2018 mix under frozen maps (n=152726 / 56160) | Confirmatory temporal TEST |
| S10-A1-GAP | `ANALYSIS-ONLY / DESCRIPTIVE` | `COMPLETED` | Why A1 review = 208,859 (LOW+MEDIUM × INSUFFICIENT_INFORMATION). Decomposition of **existing** governance evidence. Does **not** validate Shariah compliance. LC has no contract-level Shariah fields sufficient for applicant-level determination. `INSUFFICIENT_INFORMATION` is not a Shariah ruling. | Independent Shariah validation; applicant non-compliance finding |
| S10-A4 | `ANALYSIS-ONLY / DESCRIPTIVE COMPARISON` | `PASS WITH DOCUMENTATION LIMITATION` | Citation table LC vs UCI; 4B vs 5 EBM **EXPLAINED** | New AUC test; model ranking |

Reports: `docs/STAGE_10_S10_I1_IDENTITY_REPORT.md`; `docs/STAGE_10_S10_R1_YEAR_REPORT.md`; `docs/STAGE_10_S10_A1_GAP_REPORT.md`; `docs/STAGE_10_S10_A4_SIDEBYSIDE_REPORT.md`.  
Audits: `audit/stage10_i1_identity.json`; `audit/stage10_s10_r1_year.json`; `audit/stage10_s10_a1_gap.json`; `audit/stage10_s10_a4_sidebyside.json`.  
Closure: `docs/audits/STAGE_10_FINAL_CLOSURE_AUDIT.md`.

---

## 10. DOCUMENTATION / REPRODUCIBILITY LIMITATIONS

From final audits and stage reports (not invented):

1. No `.git` / `git_commit` null throughout.
2. Stage 4B final EBM SHA-256 not recorded.
3. Stage 8 v2 `test_audit_records.csv` has no `row_ref`; S10-I1 identity is positional.
4. Stored pytest summaries do not independently lock every historical TEST point estimate.
5. Stage 9.4 XGBoost five-seed validation table is degenerate.
6. Stage 9.4 XGBoost authorization/deviation provenance (`DEVIATION-001`; no successor amendment).
7. Stage 9.1 documentation-gap authorization (class B).
8. Stage 9.2 / 9.3 class C exploratory.
9. AAOIFI operative clauses unavailable (access control); unimplemented.
10. No `EXPERT_VALIDATED` rule.
11. Stage 4B TRAIN+VAL concatenated n not stored as one field.
12. Stage 2 Zenodo target-documentation conflict (frozen in Stage 3).
13. LC originated-and-resolved selection bias; no reject inference.
14. UCI ≠ LC targets; UCI undocumented codes unlabeled.
15. Stage 5 2018 Platt ECE deterioration; no nested TRAIN calibrator.
16. Stage 6 explanation sample n=5,000, not full TEST.
17. HIGH band n=27.
18. Some ECE missing in Stage 4B LR and UCI family-raw LR/EBM tables.
19. Stage 4A high-cardinality zip one-hot; `dti_n==999` unlabeled.
20. Older `docs/shariah/SHARIAH_GOVERNANCE_SCOPE.md` still says Stage 8 fusion is not implemented; Stage 8 v2 report is the later controlling record (documentation lag when writing).
21. Stage 6 report opening language refers to a “frozen Stage 4B model,” while Stage 6 metadata/evidence identify the TRAIN-only EBM used by Stage 5. Historical Stage 6 records were **not** rewritten; this is a documentation/provenance limitation.
22. Stage 9 protocol has leftover historical `DRAFT` wording despite `AMENDMENT-STAGE9-4-AUTHORIZATION` being **APPROVED** on 2026-09-15. Documentation/provenance lag, not TEST leakage or result fabrication.
23. The Stage 9.4 report hash changed when its provenance caveat was added; the underlying UCI TEST metric JSON was **not** rewritten. Documentation/provenance limitation, not TEST leakage or result fabrication.
24. LendingClub does not contain contract-level Shariah evidence fields sufficient for applicant-level Shariah compliance determination. S10-A1-GAP is analysis-only/descriptive and does **not** validate Shariah compliance. `INSUFFICIENT_INFORMATION` is not a Shariah ruling, applicant non-compliance finding, or proof that a contract is non-compliant. The governance layer is decision-support / evidence-gap handling, not Shariah certification.

---

## 11. CLAIMS THAT MUST NOT APPEAR

The final paper must **not** state:

- Shariah certification, “Shariah-certified AI,” or “Shariah-compliant loan approval system.”
- Applicant-level Shariah compliance / non-compliance / halal / haram determinations.
- Rules were expert-validated (`EXPERT_VALIDATED`).
- AAOIFI fully implemented.
- Real-world deployment, production-ready, or live approval performance.
- Fair-lending or regulatory-compliance **guarantees**.
- Real-world **fraud-detection** performance (no fraud experiment was executed).
- XGBoost was pre-registered or part of the approved Stage 9.4 written model scope.
- Stage 9.4 UCI XGBoost is the primary validated model, the confirmed best model, an overall superior model, or a confirmatory outcome. Permitted class only: `EXECUTION-TIME EXPANSION, EXPLORATORY`.
- Stage 4B LendingClub XGBoost and Stage 9.4 UCI XGBoost are the same result.
- Stage 10 post-hoc TEST findings (especially S10-R1) as confirmatory evidence.
- UCI validates the LendingClub evidence-separated architecture.
- UCI validates Shariah governance.
- Governance improves ROC-AUC / predictive accuracy.
- A0/A1/A3 ranking as “best / optimal / winner.”
- Causal claims from SHAP or EBM terms.
- Calibration improved discrimination (Platt TEST ROC-AUC equals raw).
- Stage 4B 0.679941 and Stage 5 0.677669 are the same fitted EBM, or an unresolved error.
- Datasets other than the Zenodo LC extract and UCI Default of Credit Card Clients were used.
- LC and UCI were merged.
- `SHR-001` was reconstructed; contract evidence was fabricated.
- Human review equals certification.
- G1/G3 are empirical Shariah findings.
- Thresholds 0.06/0.69/0.16 are official or operationally costed.
- `INSUFFICIENT_INFORMATION` is a Shariah ruling, an applicant non-compliance finding, or proof that a contract is non-compliant.
- S10-A1 validates Shariah compliance.
- The governance layer is Shariah certification.

---

## 12. FINAL PAPER SECTION MAP

Recommended structure. Source artifacts only; **do not write the sections in this task.**

| Section | Use these artifacts |
| --- | --- |
| Abstract | Stage 5 TEST metrics JSON; table3 counts; Stage 7 v2 non-certification sentence; claim boundaries §1 and §11 of this inventory; S10-A4 for 4B vs 5 distinction |
| Introduction | `docs/STAGE_9_1_ABLATION_REPORT.md` §2 (executed RQ); `docs/dataset_decision.md`; **not** the Stage 0 stub `docs/research_question.md` as if finalized |
| Related Work | **No repository literature review.** External literature only; no invented citations from this inventory |
| Research Gap / Contributions | `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` hypotheses table (as protocol, not as proven results); Stage 9.1 definitions; this inventory §11.C as negative space; **not** stub `docs/contribution_statement.md` |
| Data | Stage 2 report; `docs/raw_data_manifest.json`; Stage 3 report; `audit/lendingclub_split_manifest.json`; `audit/uci_split_manifest.json`; `docs/lendingclub_feature_policy.csv`; `docs/uci_feature_policy.csv`; `docs/dataset_comparability.md` |
| Methodology | `AMENDMENT-SHARIAH-001`; `docs/shariah_methodology.md`; `docs/decision_policy_specification.md`; Stage 4A report + `docs/lendingclub_preprocessing_policy.csv`; `docs/METRIC_DEFINITIONS.md`; `docs/explainability_protocol.md`; evidence-separation language in Stage 6/7/8 reports |
| Experimental Protocol | Stage 3–5 reports; `experiments/stage4b_credit_risk/selected_configurations.json`; `experiments/stage5_calibration/selected_calibration.json`; Stage 8 v1 table2; Stage 9.0 freeze JSON; Stage 9/10 protocols for class labels |
| Results | `results/metrics/stage4b_test_metrics.json`; `results/calibration/metrics/stage5_test_metrics.json`; S10-A4 tables; **explicit A/B/C EBM rows**; do not mix 4B TEST EBM with Stage 8 `p_selected`; downstream model `results/calibration/artifacts/ebm_train_only_seed42.joblib` |
| Explainability | Stage 6 report; `results/explainability/tables/table1_*.csv` through `table5_*.csv`; flag Stage 6 opening “frozen Stage 4B model” vs TRAIN-only metadata |
| Shariah Governance | Stage 7 v2 report; rule catalog; source register; S10-A1 report; amendment; **prototype / evidence-gap wording only**; LC has no contract-level Shariah fields |
| Decision Fusion | Stage 8 v2 report; v2 table3 / table3b / table4; frozen_policy v1+v2; Stage 9.1 counts; **9.2/9.3 only if labeled exploratory** |
| Independent methodology (UCI) | Stage 9.4 report; `uci_test_family_raw.csv` for LR+EBM; XGBoost only as `EXECUTION-TIME EXPANSION, EXPLORATORY` with `DEVIATION-001`; do not merge with Stage 4B LC XGBoost |
| Robustness / integrity | S10-I1; S10-R1 (post-hoc label); S10-A4; Stage 5 temporal table |
| Limitations | This inventory §10; Stage 2 open issues; Stage 9/10 closure audits |
| Discussion | Only §1 freeze-backed facts plus qualified exploratory notes; no new numbers |
| Conclusion | Repeat supported claims only; restated non-certification and non-production |

v1 Stage 7/8 reports may be cited as **historical predecessors**, not as the implemented L1/L2 fusion.

---

## Inventory close

```text
PAPER_EVIDENCE_INVENTORY_STATUS = COMPLETE
EXPERIMENTS_RUN = NONE
RESULTS_MODIFIED = NONE
MODELS_MODIFIED = NONE
STAGE_9_STATUS = CLOSED
STAGE_10_STATUS = CLOSED
PAPER_DRAFTING = NOT STARTED
```
