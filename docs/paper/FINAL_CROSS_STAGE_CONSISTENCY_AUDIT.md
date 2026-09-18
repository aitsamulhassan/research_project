# Final Cross-Stage Consistency Audit

| Item | Value |
| --- | --- |
| **Document ID** | `FINAL-CROSS-STAGE-CONSISTENCY-AUDIT` |
| **Audit date** | 2026-09-17 |
| **Type** | Repository-only forensic consistency inspection |
| **Web search** | **None** |
| **Experiments / recomputes** | **None** |
| **Manuscript / IEEE source / PDF modified** | **No** |
| **Stage 2–10 artifacts modified** | **No** |
| **TEST reopened** | **No** |
| **Stage 9 / Stage 10 reopened** | **No** |

This audit inspects existing files only. It does not recalculate metrics, rerun experiments, rewrite the paper, repair formatting, or treat later closure records as silently overwriting earlier Stage-boundary text.

Requested path `docs/paper/PAPER_EVIDENCE_INVENTORY.md` was **not found**. The inventory used here is `docs/PAPER_EVIDENCE_INVENTORY.md`. Controlling inventory-audit used: `docs/audits/PAPER_EVIDENCE_INVENTORY_AUDIT.md`.

---

## 1. Executive Status

CONSISTENT_WITH_HISTORICAL_STATUS_NOTES

The inspected scientific claims (model contexts, executed datasets, TEST identity/n, Platt identity, explainability method, Shariah non-certification, decision-policy assumptions, reference UNVERIFIED fields, and IEEE source vs review PDF scientific keys) agree across the current manuscript family and the Stage 2–10 evidence those files cite.

Apparent contradictions in **stage-status strings** are contemporaneous Stage-boundary or later-file-lag statements. They are not a second set of TEST metrics and do not reverse Stage 9 / Stage 10 closure in the current manuscript.

---

## 2. Stage Status Matrix

| Stage | Current status | Evidence file | Historical-status issue? | Paper impact |
| --- | --- | --- | --- | --- |
| Stage 2 | COMPLETE (no `STAGE_2_STATUS` gate line) | `docs/STAGE_2_DATA_AUDIT_REPORT.md` §1 (“Stage status: COMPLETE”); `docs/audits/PAPER_PHASE_READINESS_AUDIT.md` §2 | No | None. Manuscript cites LC/UCI acquisition as executed. |
| Stage 3 | Frozen / complete (no `STAGE_3_STATUS` gate line) | `docs/STAGE_3_SPLIT_AND_FEATURE_REPORT.md` §1 (split frozen; TEST n=208886); readiness audit §2 | No | None. Manuscript uses the same TRAIN/VAL/TEST counts. |
| Stage 4A | Complete; Stage 4B proceeded (no `STAGE_4A_STATUS` gate line) | `docs/STAGE_4A_PREPROCESSING_REPORT.md`; readiness audit §2 | No | None. Preprocessing is cited as TRAIN-only fit. |
| Stage 4B | `STAGE_4B_STATUS = PASS` | `docs/STAGE_4B_MODELING_REPORT.md` (status line); readiness inventory | No | Paper context **M-4B** (TRAIN+VAL refit TEST families). |
| Stage 5 | `STAGE_5_STATUS = PASS` | `docs/STAGE_5_CALIBRATION_REPORT.md`; readiness inventory | No | Paper context **M-5** (TRAIN-only EBM + VAL Platt). |
| Stage 6 | `STAGE_6_STATUS = PASS` | `docs/STAGE_6_EXPLAINABILITY_REPORT.md`; readiness inventory | Opening-sentence provenance vs metadata: **documented**, Stage 6 file not rewritten | Paper follows metadata (M-5 TRAIN-only EBM); discloses the Stage 6 opening-sentence wording. |
| Stage 7 | `STAGE_7_STATUS = PASS` (v2 controlling) | `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md`; v1 `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT.md` labeled historical | v2 header: “Stage 8 fusion was not started in that run”; “Stage 9 remains blocked” — **Stage-7-time / v2-run boundary** | Manuscript uses v2 L1/L2; does not claim Stage 8/9 never later ran. |
| Stage 8 | `STAGE_8_STATUS = PASS` (v2 controlling) | `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`; v1 `docs/STAGE_8_DECISION_POLICY_REPORT.md` labeled **Stage 8 v1 historical evidence** | v1 § Stage boundary: “Stage 9 has NOT been started.” v2 §H: `STAGE_9 = BLOCKED` — **Stage-8-time boundary**, not the current Stage 9 closure record | Manuscript cites Stage 8 v1 thresholds and Stage 8 v2 fusion; states Stage 9 **CLOSED**. |
| Stage 9 | CLOSED (experimentation closed; 9.1–9.4 reports exist) | `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md`; `docs/PAPER_EVIDENCE_INVENTORY.md` header; `docs/paper/MANUSCRIPT_DRAFT.md` experimental-protocol text | Freeze JSON still stores `stage9_execution` = `NOT AUTHORIZED` (explicitly not rewritten). Stage 9 protocol footer still says “Stage 10 is not started.” | Paper treats 9.1–9.4 as executed with recorded classes; XGBoost remains exploratory. |
| Stage 10 | CLOSED (`STAGE_10_EXECUTION = CLOSED`) | `docs/audits/STAGE_10_FINAL_CLOSURE_AUDIT.md`; inventory header | Constitution leftover “Stage 10 is not started.” Stage 9 closure audit (2026-09-15): “Stage 10 started = No.” | Manuscript limitation discloses constitution leftover; claims Stage 10 **CLOSED**. |
| Stage 11 | NOT STARTED / not authorized | Stage 10 closure; readiness audit §1; Stage 10 amendment | No | Paper does not claim Stage 11 execution. |

Paper-phase documentation lag (not a Stage-science conflict): `docs/audits/PAPER_PHASE_READINESS_AUDIT.md` (2026-09-16) records “Paper drafted: No” / “no paper/manuscript path found.” `docs/PAPER_EVIDENCE_INVENTORY.md` header still says **Paper drafting: NOT STARTED**. Paper files now exist under `docs/paper/`. Those inventory/readiness statements are file-lag / contemporaneous-audit text, not manuscript scientific claims that drafting never occurred.

---

## 3. Historical vs Current Status Discrepancies

### 3.1 Focal sentence: “Stage 9 has NOT been started.”

| Field | Record |
| --- | --- |
| Exact wording | `Stage 9 has NOT been started.` |
| Source file | `docs/STAGE_8_DECISION_POLICY_REPORT.md` |
| Source section | `## Stage boundary` (line 89) |
| Same-file context | Line 3: “**Historical preservation.** This document is **Stage 8 v1 historical evidence**.” Line 3 also: “Stage 9 remains **blocked**.” Line 7: `STAGE_8_STATUS = PASS`. |
| Explicitly historical? | **Yes**, as a Stage 8 v1 document. The file header labels the whole report Stage 8 v1 historical evidence. The sentence sits under a Stage-8 **boundary** heading, not under a later Stage 9 closure heading. |
| Conflicts with current Stage 9 closure? | **No as a current-status record.** It is a Stage-8-time boundary. It is **not** the Stage 9 closure audit. |
| Affects manuscript claims? | **No.** The manuscript states Stage 9 remains CLOSED and cites 9.1–9.4 / S10 artifacts. It does not claim Stage 9 was never started. |

Current Stage 9 closure (not inferred from Stage 8):

| Field | Record |
| --- | --- |
| Exact wording | “**Closure:** Stage 9 is closed for experimentation.” |
| Source file | `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md` |
| Source section | Opening closure paragraph (after the audit table) |
| Explicitly historical? | This is the Stage 9 **final closure** record (audit date 2026-09-15). The same file’s table still records “Stage 10 started = No” because that audit was written **before** Stage 10 execution. |
| Paper impact | Manuscript follows CLOSED for Stage 9. |

Controlling Stage 8 science (not v1 as current fusion):

| Field | Record |
| --- | --- |
| Exact wording | `STAGE_9 = BLOCKED` and “Stage 9 blocked.” |
| Source file | `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md` |
| Source section | Lines 9–11 (code block after status); §H Stage gate (lines 111–118) |
| Explicitly historical? | The file does **not** use the word “historical” on the `STAGE_9 = BLOCKED` line. It **does** identify itself as the Stage 8 v2 fusion report, `STAGE_8_STATUS = PASS`, and points v1 to `docs/STAGE_8_DECISION_POLICY_REPORT.md` as remaining historical evidence. `STAGE_9 = BLOCKED` is a Stage-8 gate line in that Stage 8 report. |
| Do not resolve by inference beyond file text | This audit does not rewrite v2 to say CLOSED. Current **program** closure for Stage 9 is the Stage 9 closure audit, not the Stage 8 v2 gate line. |
| Paper impact | None on metrics. Manuscript does not reprint `STAGE_9 = BLOCKED` as current program status. |

### 3.2 Other status-string discrepancies (same class)

| Exact wording | Source file | Section / location | Explicitly historical? | Affects manuscript claims? |
| --- | --- | --- | --- | --- |
| “Stage 8 fusion was not started in that run.” / “Stage 9 remains blocked.” / “Stage 8 fusion and Stage 9 were not started in this run.” | `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md` | Header blockquote (line 3); §B (line 21) | Header also says Stage 8 v2 fusion is documented separately. The “not started in this run / remains blocked” lines are Stage-7-v2-run boundary text. | No. Paper cites Stage 8 v2 as executed fusion. |
| “Stage 9 is closed for experimentation. … Stage 10 is not started.” | `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` | Footer / next-action table (grep hit ~line 756) | Protocol is a Stage 9 document; footer records Stage 10 as not started **in that protocol’s next-action cell**. Stage 10 later has its own closure audit. | Manuscript limitation 29 / experimental-protocol paragraph already disclose constitution leftover vs Stage 10 CLOSED. Protocol footer is not used as current Stage 10 status in the paper body. |
| “Stage 10 started \| **No**” | `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md` | Opening audit table, line 15 | **Yes, as of that audit date (2026-09-15).** The file states it does not start Stage 10. | No. Later Stage 10 closure is a different dated record. |
| “Stage 10 is not started.” | `RESEARCH_CONSTITUTION.md` | Line 37 (same paragraph that also says Stage 9 is closed for experimentation) | The sentence is present without a “historical” label. Later paper audits (`FINAL_MANUSCRIPT_INTEGRITY_AUDIT.md`, `MANUSCRIPT_DRAFT.md` limitation 29) **explicitly** call it a leftover vs Stage 10 CLOSED. | Paper discloses the leftover. Paper does **not** claim Stage 10 is open. |
| “Stage 11 and paper drafting remain unauthorized.” / “Paper drafted \| **No**” | `docs/audits/STAGE_10_FINAL_CLOSURE_AUDIT.md`; `docs/audits/PAPER_PHASE_READINESS_AUDIT.md` | Closure paragraph; readiness table | Dated 2026-09-16 readiness/closure snapshots. Readiness: “No paper/manuscript path found.” | Paper-phase files now exist. This is **documentation lag in readiness/inventory**, not a TEST-metric conflict. Manuscript science is not rewritten by those headers. |
| “Paper drafting \| **NOT STARTED**” | `docs/PAPER_EVIDENCE_INVENTORY.md` | Header table (line 13) | Inventory date 2026-09-16; file states it does not write the paper. Later integrity audits already flag this header lag. | No scientific metric change. |
| `C_INFINITY_RENDERING = REVIEW_REQUIRED` | `docs/paper/IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md` | Header (line 15) | Checklist written **before** the C=∞ LaTeX fix. Later `docs/paper/FINAL_LATEX_BUILD_QA.md` records the typesetting fix. | Not a scientific identity change. Checklist line is stale relative to later QA; C=∞ rendering is a format record, not a new metric. |
| `TEMPLATE_NOT_FOUND` | `docs/paper/IEEE_TEMPLATE_PLACEMENT_AUDIT.md` | Historical placement record | `docs/paper/PRE_SUBMISSION_INTEGRITY_AUDIT.md` already labels this file historical vs later Access placement COMPLETED. | No science impact. |

### 3.3 Stage 9 freeze JSON vs later Stage 9 execution

| Field | Record |
| --- | --- |
| Exact wording (closure audit) | Freeze JSON `stage9_execution` remains `"NOT AUTHORIZED"`; “Freeze JSON rewritten to look like later stages were authorized \| **No**.” |
| Source | `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md` §1 |
| Explicitly historical? | The freeze JSON is a **design-freeze** record (`record_type`: `stage9_0_design_freeze`). The closure audit states it was not rewritten to backdate authorization. Later 9.1–9.4 reports exist with recorded authorization classes. |
| Paper impact | Manuscript discloses 9.1 class B and 9.2/9.3/9.4-X class C. It does not treat the freeze JSON `NOT AUTHORIZED` string as meaning 9.1–9.4 never ran. |

---

## 4. Model Context Audit

| Context ID | Repository-supported classification | Silent merge found? |
| --- | --- | --- |
| **M-4B** | Stage 4B LendingClub family TEST after TRAIN+VALIDATION refit. Controlling report: `docs/STAGE_4B_MODELING_REPORT.md`. TEST EBM ROC-AUC **0.6799408767429772**. LC XGBoost in this context is a Stage 4B family, not UCI 9.4 XGBoost. | **No.** IEEE source Table (M-4B vs M-5) and abstract keep TRAIN+VAL refit vs TRAIN-only separate. |
| **M-5** | Stage 5 TRAIN-only EBM + validation-only Platt (`p_selected`). Controlling: `docs/STAGE_5_CALIBRATION_REPORT.md`. TEST ROC-AUC **0.6776693941139847** (raw and Platt; rank-based). Downstream Stages 6–8 / 9.1 / S10 use this probability stream. | **No.** Paper states downstream probabilities come from M-5, not the M-4B joblib. |
| **M-9.4-AE** | Independent UCI methodology: Logistic Regression + EBM; approved written scope `AMENDMENT-STAGE9-4-AUTHORIZATION`. Human-review file `docs/paper/M9_4_AE_HUMAN_REVIEW.md`: **SUPPORTED_AS_INDEPENDENT_UCI_METHODOLOGY**; frozen artifacts do **not** classify AE as `EXECUTION-TIME EXPANSION, EXPLORATORY`. | **No** merge with M-9.4-X or with LC models. A prior IEEE **task instruction** once said “UCI exploratory analysis context”; that instruction is recorded as task-vs-repository wording, not as a manuscript reclassification. |
| **M-9.4-X** | Exploratory UCI XGBoost; `DEVIATION-001` class C execution-time expansion. Selected-family raw TEST ECE **0.20065704943022225**. Paper labels the ECE cell exploratory / not primary. | **No.** Side-by-side citation records `xgboost_ratified=false`. |

LC XGBoost (M-4B family) and UCI XGBoost (M-9.4-X) remain distinct in inventory (`docs/PAPER_EVIDENCE_INVENTORY.md` §1) and in the IEEE manuscript.

---

## 5. Dataset Audit

| Dataset | Role in evidence inventory | Role in manuscript / IEEE source | Accidentally described as executed? |
| --- | --- | --- | --- |
| LendingClub (Zenodo granting-model extract) | Primary executed LC pipeline (Stages 2–8, 9.1, S10 on LC TEST) | Primary executed dataset; n=1,347,681; TEST n=208,886 | No |
| UCI Default of Credit Card Clients | Independent methodology context (Stage 9.4); not full architecture / not Shariah layer | Independent credit/calibration methodology context | No |
| German Credit | Literature-only (`docs/PAPER_EVIDENCE_INVENTORY.md`; map [22]) | “were **not** executed”; bibitem “not executed in this project” | No |
| Australian Credit Approval | Literature-only (map [23]) | Same | No |

Stage 2 report acquired **only** the Zenodo LC file and the UCI Default of Credit Card Clients package. No German/Australian execution artifacts were cited as run in the inspected paper family.

UCI is not used to validate Shariah compliance in the manuscript (no Shariah layer on UCI; 9.4 is credit/calibration methodology).

---

## 6. TEST and Calibration Audit

### TEST identity

| Item | Recorded consistently as |
| --- | --- |
| LC TEST n | **208,886** (Stage 3 report; Stage 8 v1 n=208886; Stage 9 closure; IEEE tex TRAIN/VAL/TEST table; abstract) |
| TEST hash (manuscript) | `4dfedb1ad7785fa3833047135b1883676f3e1b49aca9c87fcdb346e64fd489c6` |
| Split | Chronological LC split frozen in Stage 3; paper does not introduce a new TEST draw |

No paper section inspected here presents a newly calculated TEST metric. IEEE tables transcribe stored Stage 4B / Stage 5 / Stage 9.4 / Stage 8 v2 / Stage 9.1 counts.

Stage 8 v1 predictive block reports **rounded** TEST ROC-AUC `0.677669` (`docs/STAGE_8_DECISION_POLICY_REPORT.md`, frozen test predictive metrics). The manuscript/IEEE source use the stored full-precision Stage 5 value `0.6776693941139847`. That is display precision in the v1 Stage 8 report, not a second TEST calculation in the paper.

### Platt / calibration

| Item | Consistency |
| --- | --- |
| Fit | Validation-only Platt; unregularized logistic `C=∞`, solver `lbfgs`, on `logit(p_raw)` |
| Form | \(\sigma(a \cdot \operatorname{logit}(p_{\text{raw}}) + b)\) with frozen \(a=1.1988263209549705\), \(b=0.6697765046966161\) (paper/evidence map lineage; not recomputed here) |
| M-4B vs M-5 | IEEE comparison table keeps M-4B EBM TEST ROC-AUC **0.6799408767429772** separate from M-5 **0.6776693941139847**. Stage 10 closure already classifies that difference **EXPLAINED** (different fit), not as a new experiment. |
| Mixing | Not found: Stage 5 calibrated TEST metrics are not labeled as Stage 4B TRAIN+VAL EBM metrics in the IEEE source/abstract. |

---

## 7. Explainability Audit

| Check | Finding |
| --- | --- |
| Additive EBM explanation language | IEEE source: `interactions=0`; exact additive logit-scale SHAP-style decomposition \(\phi_i = g_i - \operatorname{mean}_{TRAIN} g_i\). Matches Stage 6 report method (closed-form additive interventional SHAP on logit). |
| TreeSHAP | Stage 6: “TreeSHAP was not used.” IEEE source repeats “TreeSHAP was **not** used” in related work, contributions, protocol, and methods. Literature [13] is cited as TreeSHAP **identity**, not as a method used on the EBM. |
| Stage 6 opening-sentence provenance | **Still present in the Stage 6 report and still disclosed in the paper.** Stage 6 line 5: “The frozen Stage 4B model is an Explainable Boosting Machine…”. IEEE source documented provenance limitation: metadata `model_id=ebm_train_only_seed42` / `stage5_model_path=results/calibration/artifacts/ebm_train_only_seed42.joblib` identify the TRAIN-only **M-5** EBM, not `results/artifacts/final_explainable_boosting_machine_seed42.joblib`. “This paper follows the metadata.” Historical Stage 6 opening sentence was **not** rewritten. This is a **documented provenance discrepancy**, not an unresolved silent merge in the manuscript. |

---

## 8. Shariah / Regulatory Claim Audit

Inspected IEEE source / IEEE manuscript / draft language:

| Prohibited claim | Found? |
| --- | --- |
| Certification / fatwa / automated compliance verdict / `EXPERT_VALIDATED` as achieved | **No.** Abstract and methods deny these. |
| LendingClub contains contract-level Shariah data | **No.** L1 `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`; “lacks contract-level Shariah fields.” |
| UCI validates Shariah compliance | **No.** UCI is independent credit/calibration methodology; no Shariah layer. |
| Researcher assumption presented as a religious ruling | **No.** Governance matrix / costs labeled researcher operating procedure / assumptions. `INSUFFICIENT_INFORMATION` is an evidence/schema limitation, not applicant non-compliance. |
| Regulatory/standard sources overstated | AAOIFI SS 8/9: named standards; operative clauses not retrieved; years **UNVERIFIED**. SECP used as **prohibition** on calling a security Shariah compliant without a Commission certificate, not as a certificate of this prototype. IFSB-10: FAQ verified rather than full-body re-parse. |

Stage 7 v2: “research prototype for Shariah-oriented governance and evidence traceability, not a Shariah certification mechanism.”

---

## 9. Decision-Policy Audit

| Check | Finding |
| --- | --- |
| Cost assumptions labeled assumptions | Stage 8 v1 § Researcher policy assumptions: FN:FP ratios are sensitivity scenarios, not LendingClub/bank/Islamic-institution/regulator costs. IEEE source: thresholds `0.06/0.69/0.16` are researcher-scenario identifications, not official operational costs. |
| HUMAN_REVIEW simulated / research policy | Stage 8 v1: “The review band is a **simulated decision-policy band**. No human-review outcomes were collected.” IEEE conclusion: counts are not production origination outcomes. |
| APPROVE/REJECT as real origination | **Not claimed.** A0 5232 / 203627 / 27; A1 0 / 208859 / 27; A3/A4 61855 / 0 / 147031 are research-map assignments on frozen `p_selected`. |
| Threshold identity | `t_low=0.06`, `t_high=0.69`, `t*=0.16` identified as validation-derived in Stage 8 v1 and reused frozen in Stage 8 v2 (“Thresholds were selected on validation only in Stage 8 v1. Stage 8 v2 did not search a new grid.”). IEEE methods: two-threshold bands and monolithic \(t^{*}=0.16\). |

---

## 10. Reference Integrity Audit

Evidence map (`docs/paper/MANUSCRIPT_EVIDENCE_MAP.md`) copies bibliographic fields from `docs/literature/LITERATURE_SOURCE_REGISTER.csv` and states unverified fields are not filled.

| Check | Finding |
| --- | --- |
| Fabricated references | **Not found** in this inspection. IEEE `\bibitem{b1}`–`{b34}` correspond to draft [1]–[34]. |
| Unverified metadata still explicit | Platt [14] / `b14`: DOI none recorded; official publisher URL **UNVERIFIED**. Zenodo [20]: creator names **UNVERIFIED**. AAOIFI years **UNVERIFIED**. Guo et al. DOI field NONE in register. |
| Unsupported DOI/author/year silently inserted | **Not found** relative to the frozen literature map and prior integrity audits (`FINAL_MANUSCRIPT_INTEGRITY_AUDIT.md`, IEEE placement audits). |

This audit did not search the web and did not re-verify DOIs.

---

## 11. PDF / LaTeX Scientific-Content Consistency

| Artifact | Role |
| --- | --- |
| `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` | Current IEEE Access source (layout helpers + prior C=∞ typesetting). Compile copy also under the official template directory. |
| `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf` | Current review-view PDF (layout-repaired build; 13 pages per `IEEE_ACCESS_LAYOUT_REPAIR_AUDIT.md`). |
| `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.pdf` | **Prior** 12-page build left in place after layout repair (per layout-repair audit). Not treated as the current review PDF. |

Scientific-key comparison in this pass is against the LaTeX source and against existing QA/layout audits (no new metric calculation, no TEST reopen):

| Check | Finding |
| --- | --- |
| Same scientific content (source vs REVIEW_READY) | `docs/paper/IEEE_ACCESS_LAYOUT_REPAIR_AUDIT.md` records format-only repair (hash wrapping, table width, TABLE 9 float class) and preservation of frozen numerical keys. |
| Metric differs source vs PDF | **Not found** in those QA records or in the source keys listed in §4 and §6. |
| Figure/table scientific content | Fig. 1 remains a text schematic; Fig. 2 omitted. Table IV (a)/(b); Table II before III; Table VII before VIII — structure preserved; TABLE 9 changed from `table*` to single-column `table` for **layout**, not content rewrite. |
| `C=\infty` | Source: `\texttt{C=}\(\infty\)` (post `FINAL_LATEX_BUILD_QA.md`). Checklist `REVIEW_REQUIRED` is **stale** relative to that QA. |
| Hidden scientific alteration during layout repair | Layout audit: scientific classification unchanged; no Stage 9/10 reopen. This forensic pass found no substituted TEST n, swapped M-4B/M-5 AUCs, or upgraded M-9.4-X. |

Minor two-column formatting issues remaining on REVIEW_READY are **presentation** (`IEEE_ACCESS_LAYOUT_REPAIR_AUDIT.md`: `MINOR_FORMATTING_ISSUES`) and are out of scope to repair here.

Markdown masters (`MANUSCRIPT_DRAFT.md`, `IEEE_MANUSCRIPT.md`, `IEEE_TEMPLATE_READY_MANUSCRIPT.md`) carry the same scientific classification and frozen keys; they are not bit-identical to the LaTeX (Access markup, `\sha`, table float class).

---

## 12. Required Human Decisions

Only items that still require owner input (not resolvable from repository text alone):

1. **Author submission metadata** (emails, ORCID, biographies, corresponding-author designation, funding/acknowledgments if any). Status remains `USER_INPUT_REQUIRED` in `docs/paper/IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md` and `PRE_SUBMISSION_INTEGRITY_STATUS = USER_INPUT_REQUIRED`. Do not invent these.
2. **Whether to edit historical status strings** in Stage 8 v1/v2, Stage 7 v2, `RESEARCH_CONSTITUTION.md`, Stage 9 protocol footer, and paper-inventory/readiness headers so they no longer say Stage 9/10 “not started” / `BLOCKED` / paper drafting `NOT STARTED`. That is a **documentation-maintenance** choice. This audit does not perform it. The manuscript already discloses the constitution leftover. Silent rewrite of historical Stage-boundary reports is a separate owner decision.
3. **Optional IEEE Access minor-formatting polish** (remaining NICE_TO_FIX layout items). Not a scientific gate. Not performed here.

No human decision is required to choose between “Stage 9 never started” and “Stage 9 CLOSED” for **manuscript science**: the Stage 8 sentence is a Stage-8-time boundary in a file labeled Stage 8 v1 historical evidence; current Stage 9/10 closures and the paper body use CLOSED.

---

## 13. Final Gate

FINAL_CROSS_STAGE_STATUS = CONSISTENT_WITH_HISTORICAL_STATUS_NOTES

---

## Scientific integrity block

```text
experiments_run = NONE
metrics_recalculated = NONE
models_changed = NONE
results_changed = NONE
datasets_changed = NONE
calibration_changed = NONE
thresholds_changed = NONE
TEST_reopened = NO
Stage_9_reopened = NO
Stage_10_reopened = NO
manuscript_modified = NO
IEEE_source_modified = NO
PDF_modified = NO
scientific_classification_changed = NO
```

STOP. No other file was modified. No formatting polish. No paper rewrite.
