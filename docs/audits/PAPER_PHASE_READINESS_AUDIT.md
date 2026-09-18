# Paper-phase readiness audit

| Item | Value |
| --- | --- |
| **Audit ID** | `PAPER-PHASE-READINESS-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Audit type** | Documentation / metadata inspection only |
| **Paper drafted** | **No** |
| **Experiments run** | **No** |
| **Models trained or loaded** | **No** |
| **Metrics recomputed** | **No** |
| **Historical experiment artifacts modified** | **No** |
| **Stage 9 reopened** | **No** |
| **Stage 11 started** | **No** |
| **XGBoost ratified** | **No** |
| **New scientific claims created** | **No** |
| **New Shariah rules or expert validation added** | **No** |

This audit asks whether the repository already contains sufficient **audited** evidence to begin writing a research paper. It does **not** write that paper. It does **not** authorize Stage 11. It does **not** expand experimental scope.

**Final classification: B. READY FOR PAPER DRAFTING WITH DOCUMENTATION LIMITATIONS**

---

## 1. PAPER PHASE STATUS

| Gate | Finding | Source |
| --- | --- | --- |
| Stage 10 CLOSED | **Yes.** `STAGE_10_EXECUTION = CLOSED`; `STAGE_10_FINAL_CLOSURE = B. PASS WITH DOCUMENTATION/REPRODUCIBILITY LIMITATION` | `docs/audits/STAGE_10_FINAL_CLOSURE_AUDIT.md` |
| Stage 9 CLOSED | **Yes.** Stage 9 closed for experimentation; Stage 10 amendment forbids reopening it | `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md`; `docs/amendments/AMENDMENT-STAGE10-AUTHORIZATION.md` §2 |
| Stage 11 NOT started | **Yes.** No `stage11` path found. Protocol and Stage 10 authorization leave Stage 11 unauthorized | glob; Stage 10 protocol; Stage 10 closure audit |
| Paper drafting NOT started | **Yes.** No paper/manuscript path found. Protocol: paper drafting not authorized as a Stage 10 activity | glob; Stage 10 protocol |

Stage 10 authorized activities (S10-I1, S10-R1, S10-A1, S10-A4) are recorded as complete. Cite-only inventory rows were not additional experiments.

---

## 2. EXPERIMENTAL EVIDENCE INVENTORY

Cite-safety means: may appear in a paper **if** the recorded class and limitations are preserved. It does **not** mean the item is confirmatory.

| Stage / activity | Status | Key evidence / report | Evidence class | Safe to cite? | Important limitations |
| --- | --- | --- | --- | --- | --- |
| Stage 2 data audit | COMPLETE | `docs/STAGE_2_DATA_AUDIT_REPORT.md`; `docs/raw_data_manifest.json` | Audit / data provenance | **Yes**, as data audit | Zenodo target-documentation conflict (later frozen in Stage 3); selection bias (originated and resolved loans only); UCI undocumented codes; `git_commit` null |
| Stage 3 feature policy and chronological split | Frozen / complete (no `STAGE_3_STATUS` gate line) | `docs/STAGE_3_SPLIT_AND_FEATURE_REPORT.md`; `audit/lendingclub_split_manifest.json` | Methodology freeze | **Yes**, as split/feature freeze | `title`/`desc` excluded from primary model; UCI undocumented codes unlabeled; `addr_state`/`zip_code` are quasi-identifiers |
| Stage 4A preprocessing | Complete; Stage 4B proceeded | `docs/STAGE_4A_PREPROCESSING_REPORT.md` | Methodology (train-only fit) | **Yes**, as preprocessing protocol | High-cardinality `zip_code` one-hot; `dti_n==999` unlabeled; transformed matrices not stored as public tables |
| Stage 4B baseline models | `STAGE_4B_STATUS = PASS` | `docs/STAGE_4B_MODELING_REPORT.md`; `results/metrics/stage4b_test_metrics.json` | Confirmatory **for LC family TEST after freeze** (TRAIN+VAL refit) | **Yes**, with provenance | TEST PR-AUC below validation for every family; 2018 vs 2017 PR-AUC drop; final EBM joblib hash not recorded; LC XGBoost here is a Stage 4B family, distinct from Stage 9.4 UCI XGBoost authorization |
| Stage 5 calibration | `STAGE_5_STATUS = PASS` | `docs/STAGE_5_CALIBRATION_REPORT.md`; `results/calibration/metrics/stage5_test_metrics.json` | Confirmatory **for LC TRAIN-only EBM + VAL-fit Platt**, TEST reporting only | **Yes**, as frozen pipeline | TRAIN-only TEST numbers will not match Stage 4B TRAIN+VAL TEST; 2018 Platt ECE deterioration; no nested TRAIN calibrator |
| Stage 6 explainability | `STAGE_6_STATUS = PASS` | `docs/STAGE_6_EXPLAINABILITY_REPORT.md` | Descriptive attribution on frozen TRAIN-only EBM | **Yes**, as model attribution | 5,000 TEST rows not full TEST; additive SHAP equals centered EBM terms (not a second model class); not causal; not an approval criterion |
| Stage 7 Shariah governance | `STAGE_7_STATUS = PASS` (v2 controlling) | `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md`; `docs/amendments/AMENDMENT-SHARIAH-001.md` | Governance / evidence-traceability prototype | **Yes**, as prototype governance | Not certification; no `EXPERT_VALIDATED` rule; AAOIFI operative clauses unimplemented; LC L1 `INSUFFICIENT_SCHEMA`; v1 report is historical |
| Stage 8 policy / threshold analysis | `STAGE_8_STATUS = PASS` (v2 controlling) | `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`; `results/decision/v2/frozen_policy.json`; v1 report historical | Policy analysis on frozen `p_selected` | **Yes**, as policy/fusion on stored scores | Thresholds from validation cost scenario, not real operational cost; not real-world approval performance; Stage 8 v2 audit lacks `row_ref` |
| Stage 9.0 freeze | Design freeze PASS; `stage9_execution` remains `NOT AUTHORIZED` in freeze JSON | `audit/stage9_0_experimental_freeze.json` | Freeze / protocol | **Yes**, as freeze record | Freeze JSON was not rewritten to backdate later execution |
| Stage 9.1 ablation | `STAGE_9_1_STATUS = PASS`; authorization **class B** | `docs/STAGE_9_1_ABLATION_REPORT.md`; `audit/stage9_1_ablation_run.json` | Descriptive re-analysis of previously exposed LC TEST | **Yes, with class-B qualification** | Documentation-gap authorization; not a new confirmatory TEST experiment |
| Stage 9.2 cost sensitivity | `STAGE_9_2_STATUS = PASS`; authorization **class C** | `docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md` | Exploratory / sensitivity | **Yes, as exploratory only** | Permanently exploratory; assumed FN:FP costs; no retrospective ratification |
| Stage 9.3 governance sensitivity | `STAGE_9_3_STATUS = PASS`; authorization **class C** | `docs/STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md` | Exploratory / hypothetical engineering | **Yes, as exploratory only** | G1/G3 hypothetical, not empirical Shariah findings; G-unsafe not executed |
| Stage 9.4 UCI | `PASS`; LR+EBM approved scope; XGBoost class C | `docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md`; `DEVIATION-001` | Methodology generalization (LR+EBM freeze-backed); XGBoost exploratory | **LR+EBM: yes, as independent credit/calibration context. XGBoost: exploratory only** | Not a test of the full architecture; no Shariah layer; XGBoost execution-time expansion; degenerate five-seed XGBoost table |
| S10-I1 | `PASS WITH DOCUMENTATION LIMITATION` | `docs/STAGE_10_S10_I1_IDENTITY_REPORT.md` | Integrity / provenance — **not** confirmatory science | **Yes**, as integrity check | Positional audit join; passing does not generate independent scientific evidence |
| S10-R1 | `COMPLETED` exploratory/descriptive post-hoc | `docs/STAGE_10_S10_R1_YEAR_REPORT.md` | Exploratory / descriptive post-hoc | **Yes, as post-hoc descriptive** | Must not be called confirmatory; HIGH n=27 |
| S10-A1 | `COMPLETED` analysis-only | `docs/STAGE_10_S10_A1_GAP_REPORT.md` | Analysis-only / descriptive | **Yes**, as evidence-gap decomposition | Does not independently validate Shariah; no fabricated contracts |
| S10-A4 | `PASS WITH DOCUMENTATION LIMITATION` | `docs/STAGE_10_S10_A4_SIDEBYSIDE_REPORT.md` | Analysis-only / descriptive comparison | **Yes**, as citation comparison | No ranking; no AUC equality test; UCI ≠ LC targets |

Stage 4A is included because later modeling depends on it; the user inventory named Stage 4B as the modeling stage.

---

## 3. CORE MODEL EVIDENCE

The repository contains **two fitted LC EBMs** and **one frozen decision probability**. They must not be collapsed.

### A. Stage 4B final TRAIN+VALIDATION EBM

- Fit: TRAIN+VALIDATION refit after family freeze (`docs/STAGE_4B_MODELING_REPORT.md`).
- TEST ROC-AUC **0.6799408767429772** (`results/metrics/stage4b_test_metrics.json`).
- Prediction artifact: `results/predictions/test/explainable_boosting_machine_seed42.csv` (`p_hat`).
- Model dump path documented: `results/artifacts/final_explainable_boosting_machine_seed42.joblib`. SHA-256 **not recorded**.
- Preprocessor: train+val (`preprocessor_train_plus_validation.joblib`).

### B. Stage 5 TRAIN-only EBM raw TEST

- Fit: TRAIN only (`experiments/stage5_calibration/checkpoints/train_only_ebm_meta.json`: `trained_on=TRAIN_ONLY`, `n_train=941267`).
- Raw TEST ROC-AUC **0.6776693941139847** (`results/calibration/metrics/stage5_test_metrics.json` method `raw`).
- Model: `results/calibration/artifacts/ebm_train_only_seed42.joblib`, recorded SHA-256 `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4`.
- Prediction artifact: `results/calibration/raw/ebm_train_only_seed42_test.csv` (`p_raw`).

### C. Stage 5 Platt-calibrated `p_selected`

- Same TRAIN-only EBM as B. Platt fit on VALIDATION only; selected on validation Brier (0.001 tie, simplicity).
- TEST ROC-AUC **0.6776693941139847** (identical to stored raw; Platt is a strictly increasing map of `p_raw`).
- Artifact: `results/calibration/test/ebm_seed42_calibrated.csv` column `p_selected`.

**Difference A vs B/C:** different fitted training datasets (TRAIN+VALIDATION vs TRAIN only), same frozen Stage 3 TEST split (n=208,886), same recorded ROC-AUC wrapper. Classified **EXPLAINED**. Not a contradiction. Not a calibration effect on ROC-AUC for Platt vs raw.

**Stage 8 onward** uses C: stored `p_selected` from the Stage 5 TRAIN-only EBM + frozen Platt. It does **not** use the Stage 4B TEST EBM. Stage 6 also uses the TRAIN-only EBM (`docs/STAGE_6_EXPLAINABILITY_REPORT.md` limitation).

---

## 4. CALIBRATION EVIDENCE

From Stage 5 report / audit / `platt_record.json` / S10-A4 (cited, not refit):

| Item | Recorded fact |
| --- | --- |
| Base model | TRAIN-only EBM, seed 42, frozen Stage 4B hyperparameters |
| Calibrator fitting | VALIDATION raw probabilities and labels only |
| Methods stored | raw, Platt, isotonic |
| Selection | validation Brier; 0.001 practical-tie; simplicity `raw > platt > isotonic` → **Platt** |
| Protocol | `validation_only_calibration_no_train_val_calibrator_refit` |
| Platt form | `sigmoid(a * logit(p_raw) + b)` |
| Frozen parameters | `a=1.1988263209549705`, `b=0.6697765046966161` |
| Frozen TEST vector | `results/calibration/test/ebm_seed42_calibrated.csv` |
| Probability artifact SHA-256 | `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb` |
| TEST n | 208,886 |

Calibrators were **not** refit on TRAIN+VALIDATION. Stage 4B TRAIN+VAL TEST probabilities were **not** used for calibration.

---

## 5. EXPLAINABILITY EVIDENCE

From `docs/STAGE_6_EXPLAINABILITY_REPORT.md`:

- Frozen EBM **`interactions=0`** (additive per original feature; nine native columns).
- EBM is a **transparent-model reference**, not ground truth, not causal, not an approval criterion.
- SHAP values are **model attributions**, not causes of default.
- **TreeSHAP was not used** (EBM is a first-order GAM of bin terms, not a TreeSHAP-compatible forest).
- Exact additive interventional SHAP on the **logit / EBM `decision_function` scale**:
  `phi_i(x) = g_i(x_i) - mean_TRAIN g_i`
  using centered native EBM terms from `eval_terms`.
- `shap.AdditiveExplainer` was not used (Independent masker / mixed categoricals).
- Platt is a later monotone map and is **not inside** the EBM explanation.
- Explanation sample: 5,000 TEST rows, `RandomState(42)`, without replacement; labels not used to draw the sample.
- Perfect SHAP vs centered-EBM rank agreement is **expected** for this identity, not independent confirmation from a second model class.
- Stage 6 uses the **TRAIN-only** Stage 5 EBM, not the Stage 4B TRAIN+VAL TEST EBM.

---

## 6. SHARIAH GOVERNANCE EVIDENCE

Controlling language (Stage 7 v2 report; `AMENDMENT-SHARIAH-001`; `docs/shariah_methodology.md`; `docs/shariah/SHARIAH_GOVERNANCE_SCOPE.md`):

- This is a **research prototype for Shariah-oriented governance and evidence traceability**.
- It is **NOT** certification.
- **No applicant is described as Shariah compliant** on the basis of this system.
- **No rule is `EXPERT_VALIDATED`.**
- **AAOIFI SS 8 / SS 9 identity verified**; operative clauses **unavailable** (Stage 7 v1: official text copyrighted; AAOIFI viewer password-protected / access control). Gates `SH-AAOIFI-SS8-GATE` and `SH-AAOIFI-SS9-GATE` are identity/unavailability gates, not clause engines. `SH-AAOIFI-SS8-POSSESSION` is `NOT_VERIFIED` / not executable.
- **SBP SGF 2025** (product/process-flow prior Shariah Board approval for IBIs).
- **SBP IBD Circular 01 of 2012** (Murabaha invoice/payment instructions).
- **SECP SGR 2023 Regulation 7** (when a security is claimed Shariah compliant; not SBP banks).
- **Only verified mappings implemented.** Source-mapped SBP/SECP rules are `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW`.
- **AAOIFI clauses remain unimplemented.** Clause-level AAOIFI implementation remains blocked.
- Design A (contract-level / institutional-product governance) adopted; Design B (purpose classification) rejected; `SHR-001` remains `UNSUPPORTED_RETIRED`.
- LC L1: `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION` (dataset context, not an applicant-level ruling).
- LC L2 on TEST: `INSUFFICIENT_INFORMATION` on all 208,886 rows (evidence-gap, not halal/haram).
- Credit features are firewalled from the Shariah evidence object. `purpose` is not contract type.

Stage 7 v1 report remains historical. Stage 7 v2 + Stage 8 v2 are the implemented L1/L2 + fusion record.

---

## 7. STAGE 9 / UCI EVIDENCE

UCI is **not** the LendingClub evidence-separated architecture.

| Item | Recorded fact |
| --- | --- |
| Stage 9.4 approved written scope | Logistic Regression + EBM (`AMENDMENT-STAGE9-4-AUTHORIZATION`) |
| XGBoost | Added during execution **without** a dated successor amendment |
| `DEVIATION-001` | **UNAUTHORIZED BUT SCIENTIFICALLY VALID POST-FREEZE ANALYSIS** |
| XGBoost presentation | Permanently **exploratory**. **Must NOT** be presented as pre-registered/confirmatory. No retroactive or prospective ratification |
| UCI purpose | Independent generalization test for **credit-risk / calibration methodology** |
| UCI does **not** validate | The complete evidence-separated architecture |
| UCI does **not** validate | Shariah governance (no contract-level fields; U3 metadata-only) |
| UCI selected executed pipeline | XGBoost + isotonic (**exploratory** because the family was outside approved written scope) |
| UCI TEST (stored selected row) | ROC-AUC **0.770878**; PR-AUC **0.522421**; Brier **0.136853**; log loss **0.449533**; ECE **0.017443**; n=4502 |
| Freeze-backed family-raw UCI TEST (approved scope) | LR ROC-AUC 0.757278 / PR-AUC 0.525511 / Brier 0.187096; EBM 0.768856 / 0.537376 / 0.137432 (S10-A4 citation) |
| XGBoost five-seed validation table | Degenerate (identical metrics across five recorded seeds) |

LC and UCI targets are **not** equivalent (`Default` Charged Off/Fully Paid vs `default payment next month`). Rows were not merged. LC thresholds and Platt `(a,b)` were not transferred.

Stage 9.1 remains **class B**. Stage 9.2 and 9.3 remain **class C**.

---

## 8. THRESHOLD / POLICY EVIDENCE

Frozen maps on Stage 5 `p_selected` (Stage 8 v1 selection on **validation** cost; Stage 8 v2 / 9.1 TEST counts). n = 208,886.

| Policy | Thresholds | APPROVE | HUMAN_REVIEW | REJECT |
| --- | --- | ---: | ---: | ---: |
| A0 (credit-only two-threshold) | `t_low=0.06`, `t_high=0.69` | 5232 | 203627 | 27 |
| A1 (G0 fusion) | same bands + frozen G0 | 0 | 208859 | 27 |
| A3/A4 (binary) | `t*=0.16` | 61855 | 0 | 147031 |

Cost scenario used to **identify** thresholds (validation): assumed FN:FP=5:1, `C_REVIEW=0.25*C_FP`. This is a researcher sensitivity scenario, **not** a real operational cost (`frozen_policy.json`).

These are **policy analyses over the frozen Stage 5 `p_selected` vector**. They are **not** evidence of real-world approval performance, fairness, or regulatory compliance. A1’s near-universal HUMAN_REVIEW is the G0 image of all-TEST `INSUFFICIENT_INFORMATION`, not a credit-AUC result.

---

## 9. STAGE 10 EVIDENCE

| Activity | Classification | Recorded status | What it is | What it is not |
| --- | --- | --- | --- | --- |
| S10-I1 | Integrity / provenance — not a scientific confirmatory experiment | `PASS WITH DOCUMENTATION LIMITATION` | A0/A1/A3 share stored `p_selected`; freeze hashes match | Independent scientific evidence |
| S10-R1 | Exploratory / descriptive post-hoc reanalysis — non-confirmatory | `COMPLETED` | 2017 n=152726 vs 2018 n=56160 decision mix under frozen maps | Confirmatory TEST; year-tuned policy |
| S10-A1 | Analysis-only / descriptive | `COMPLETED` | A1 review = LOW+MEDIUM under all-INSUFFICIENT L2 × G0 | Independent Shariah validation |
| S10-A4 | Analysis-only / descriptive comparison | `PASS WITH DOCUMENTATION LIMITATION` | Side-by-side citation of stored LC/UCI metrics; 4B vs 5 EBM **EXPLAINED** | New AUC test; model ranking; UCI as architecture validation |

Limitations remain those recorded on each activity (positional `row_ref`, `git_commit` null, post-hoc year cut, no contract evidence, unrecorded Stage 4B joblib hash). Stage 10 closure: **B. PASS WITH DOCUMENTATION/REPRODUCIBILITY LIMITATION**.

---

## 10. DOCUMENTATION / REPRODUCIBILITY LIMITATIONS

Consolidated from existing Stage 2–10 reports and closure audits. **None invented here.**

1. Stage 4B final EBM SHA-256 not recorded.
2. `git_commit` null / no usable `.git` (Stages 2–10 manifests).
3. Stage 8 v2 audit rows lack `row_ref`; S10-I1 used positional matching.
4. Stage 9.4 XGBoost execution-time expansion was outside the approved written scope (`DEVIATION-001`).
5. AAOIFI operative clauses could not be verified due to access control / copyrighted viewer; clauses remain unimplemented.
6. UCI and LendingClub targets are not equivalent.
7. UCI does not validate Shariah governance.
8. Stage 2 Zenodo target-documentation conflict (Stage 3 owner freeze: 1=Charged Off, 0=Fully Paid).
9. LC sample is originated-and-resolved loans only (selection bias; Stage 2).
10. Stage 4B TEST PR-AUC below validation for every family; 2018 PR-AUC drop (descriptive temporal).
11. Stage 5: 2018 Platt ECE deterioration; no nested TRAIN calibrator.
12. Stage 6: 5,000-row explanation sample; SHAP ≡ centered EBM terms.
13. No `EXPERT_VALIDATED` rule; certification outside scope.
14. Stage 9.1 authorization class B (documentation gap).
15. Stage 9.2 / 9.3 class C exploratory; G1/G3 hypothetical.
16. XGBoost five-seed UCI validation table degenerate.
17. Stored pytest summaries do not independently lock every historical TEST point estimate.
18. Stage 4B TRAIN+VALIDATION concatenated training-row total not stored as one field.
19. HIGH credit band n=27; year-wise HIGH rates are small-count descriptive.
20. S10-R1 is post-hoc and non-confirmatory.
21. S10-A1 does not independently validate Shariah compliance; LC lacks contract-level Shariah fields; no contract evidence was fabricated.
22. Some ECE values absent from Stage 4B LR and UCI family-raw LR/EBM tables.
23. Stage 4A: high-cardinality zip one-hot; `dti_n==999` unlabeled; transformed matrices not stored as public tables.

These remain **documentation/reproducibility limitations**, not new experimental failures.

---

## 11. PAPER-SAFE CLAIM BOUNDARIES

Conservative. A claim may appear only if a stored artifact already supports it **and** its class is preserved.

### A. CLAIMS DIRECTLY SUPPORTED

- LC granting extract and UCI Default of Credit Card Clients were audited, hashed, and not merged.
- LC primary model uses nine frozen predictors and a chronological Stage 3 split (TEST `issue_month >= 2017-02`, n=208,886).
- After validation family selection, Stage 4B reported TEST metrics for LR/RF/XGBoost/EBM from TRAIN+VAL refits; EBM TEST ROC-AUC 0.6799408767429772.
- The frozen decision pipeline is a TRAIN-only EBM + validation-fit Platt; stored TEST raw and Platt ROC-AUC 0.6776693941139847.
- Stage 4B vs Stage 5 EBM TEST ROC-AUC difference is explained by TRAIN+VAL vs TRAIN-only fitting on the same TEST split.
- Stage 8–10 consume stored `p_selected` (hash `e15ddd2f…`).
- Platt was selected on validation Brier with the declared tie/simplicity rule; TEST was reporting-only.
- EBM `interactions=0`; additive SHAP on logit scale is centered EBM terms; TreeSHAP was not used.
- The governance layer is an evidence-traceability prototype with L1/L2, G0 fusion, and no `EXPERT_VALIDATED` rules.
- LC TEST L2 is `INSUFFICIENT_INFORMATION` for all rows; A1 counts are 0 / 208859 / 27.
- A0 / A3 counts and thresholds are as stored above.
- A0, A1, and A3 consume the same stored `p_selected` (S10-I1).
- UCI LR and EBM TEST metrics exist as independent credit/calibration methodology context.
- XGBoost on UCI is documented as an execution-time exploratory expansion.

### B. CLAIMS THAT REQUIRE QUALIFICATION

- Any statement that Stage 9.1 “shows” architecture effects: previously exposed TEST; class B documentation gap; decision-map differences only (scores unchanged).
- S10-R1 2017 vs 2018 mix: post-hoc descriptive, not confirmatory, not causal drift inference.
- Stage 9.2 costs: exploratory; assumed relative costs.
- Stage 9.3 G1/G3: hypothetical engineering, not Shariah findings.
- UCI TEST numbers, including 0.770878: different target/split; not LC architecture validation; selected XGBoost+isotonic row is exploratory.
- Stage 4B “selected EBM” vs Stage 5 pipeline: two different fits; paper must say which number is which.
- “More transparent / defensible pipeline” as a research question: may be discussed as design intent; Stage 9.1 does not prove operational superiority.
- Attribution ranks (`fico_n`, `loan_amnt`, …): this EBM’s attributions, not causes.
- Threshold values 0.06 / 0.69 / 0.16: validation cost-scenario identification, not an official fair-lending or Shariah threshold.

### C. CLAIMS THAT MUST NOT BE MADE

- “Shariah-compliant loan approval system”
- “Shariah-certified AI”
- “Applicants are Shariah compliant / non-compliant / halal / haram”
- “Rules were expert-validated” / any `EXPERT_VALIDATED` claim
- “AAOIFI is fully implemented”
- “Real-world deployment performance”
- “The model is production-ready”
- “The threshold guarantees fair lending”
- “The system guarantees regulatory compliance”
- “XGBoost was pre-registered”
- “XGBoost was part of the approved Stage 9.4 protocol”
- “UCI validates the entire system”
- “UCI validates Shariah governance”
- “Governance improves ROC-AUC / predictive accuracy”
- “A1 is the best / optimal / winning policy”
- “S10-R1 is a confirmatory temporal TEST”
- “Calibration improved discrimination” (Platt TEST ROC-AUC equals raw)
- “SHAP independently confirms the EBM” (identity of centered terms)
- Treating Stage 4B 0.679941 and Stage 5 0.677669 as the same model, or as an unresolved error
- Inventing missing contractual evidence or reconstructing `SHR-001`

---

## 12. PAPER STRUCTURE READINESS

Do **not** write these sections here. Evidence sufficiency for a **bounded** paper:

| Section | Evidence already in repo | Still needed (documentation/writing, not new experiments) |
| --- | --- | --- |
| Abstract | Metrics, counts, claim boundaries exist | Must encode classes (confirmatory vs exploratory) and Shariah non-certification in one paragraph |
| Introduction | Research question in Stage 9.1 report; architecture freeze | Framing only; no new claims |
| Related Work | **No dedicated related-work manuscript** | Literature synthesis from external sources. Not an experimental gap |
| Methodology | Stages 3–8 protocols, amendments, feature/split/preprocessing policies | Align older `docs/shariah/SHARIAH_GOVERNANCE_SCOPE.md` (still says Stage 8 fusion is not implemented) with the later Stage 8 v2 report when writing; do not silently rewrite that file in this audit |
| Experimental Setup | Frozen hashes, n, seeds, libraries in stage reports | Cite stored hashes; do not recompute |
| Results | Stage 4B/5/8/9.1/9.4/S10 tables | Separate LC EBM A/B/C; keep XGBoost exploratory; no ranking language |
| Explainability | Stage 6 report and tables | Keep “transparent reference / not ground truth” |
| Shariah-oriented Governance | Stage 7 v2, Stage 8 v2, S10-A1 | Keep prototype / non-certification / unimplemented AAOIFI clauses |
| Limitations | This audit §10 plus stage reports | Must appear in the paper; do not omit class B/C and git/hash gaps |
| Conclusion | Supported claims in §11.A only | Must not convert exploratory/post-hoc work into confirmatory success |

No additional experiment is required **to begin drafting**, provided §11.C is respected. A related-work section still has to be written from literature; that is ordinary paper work, not a missing Stage 2–10 result.

---

## 13. FINAL CLASSIFICATION

**B. READY FOR PAPER DRAFTING WITH DOCUMENTATION LIMITATIONS**

Not A: git/hash/`row_ref` gaps; Stage 9 class B/C; XGBoost exploratory; AAOIFI clauses unavailable; no related-work file; Stage 2 target-documentation conflict frozen rather than resolved in source text.

Not C: Stages 2–10 experimental/audit chain is complete and closed; core LC pipeline, calibration, policy counts, governance prototype language, and UCI methodology context are on record. Missing items are documentation/claim-discipline, not absent primary results.

Drafting remains a **separate authorization**. This audit does **not** start Stage 11 and does **not** draft the paper.

```text
PAPER_PHASE_READINESS = B. READY FOR PAPER DRAFTING WITH DOCUMENTATION LIMITATIONS
STAGE_10_STATUS = CLOSED
STAGE_9_STATUS = CLOSED
STAGE_11_STATUS = NOT STARTED
PAPER_DRAFTING_STATUS = NOT STARTED
```

| Item | Status |
| --- | --- |
| Exact file created | `docs/audits/PAPER_PHASE_READINESS_AUDIT.md` |
| Files modified | **NONE** (this file created only) |
| Experiments run | **NONE** |
| Models trained | **NONE** |
| Historical results changed | **NONE** |
| Thresholds changed | **NONE** |
| Calibration changed | **NONE** |
