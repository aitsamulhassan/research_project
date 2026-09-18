# Paper evidence inventory audit

| Item | Value |
| --- | --- |
| **Audit ID** | `PAPER-EVIDENCE-INVENTORY-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Audited file** | `docs/PAPER_EVIDENCE_INVENTORY.md` |
| **Inventory modified** | **No** |
| **Paper text written** | **No** |
| **Experiments run** | **No** |
| **Stage 9 / 10 reopened** | **No** |
| **Stage 11 started** | **No** |

This audit cross-checks the inventory against existing Stage 2–10 reports and artifacts. It does **not** recompute metrics, rescore models, or edit the inventory.

**INVENTORY_ACCURACY = PASS_WITH_CORRECTIONS**

The inventory is publication-directionally correct: two executed datasets, Stage 4B vs Stage 5 EBM distinction, Platt selection, Stage 6 additive SHAP, Shariah non-certification, A0/A1/A3 counts, Stage 9.4 XGBoost exploratory, Stage 10 non-confirmatory. Corrections below are omissions and phrasing traps for the **next inventory revision**, not a requirement to rewrite frozen science. The original inventory file was **not** modified.

---

## 1. DATASET ACCURACY

Cross-check: `docs/STAGE_2_DATA_AUDIT_REPORT.md`, `docs/raw_data_manifest.json`, `docs/STAGE_3_SPLIT_AND_FEATURE_REPORT.md`, `audit/lendingclub_split_manifest.json`, `audit/uci_split_manifest.json`, `docs/dataset_decision.md`.

| Inventory statement | Source | Verdict |
| --- | --- | --- |
| Only LC Zenodo extract and UCI Default of Credit Card Clients were used | Stage 2 acquisition; dataset decision memo; no other raw files in the executed pipeline | **Accurate** |
| No fraud / PaySim / IEEE-CIS executed | Stage 2 report; no later stage uses those sources | **Accurate** |
| LC full file 1,347,681 × 15 | Stage 2 | **Accurate** |
| LC splits 941,267 / 197,528 / 208,886 | Stage 3 / split manifest | **Accurate** (sum = full file) |
| LC target Stage 3 freeze 1=Charged Off, 0=Fully Paid | Stage 3; Stage 2 documents a Zenodo text conflict | **Accurate**; inventory correctly keeps the conflict as a limitation |
| LC temporal rules by `issue_month` | Split manifest `train_rule` / `validation_rule` / `test_rule` | **Accurate** |
| LC SHA-256 `207d65b2…` / TEST hash `4dfedb1a…` | Manifests | **Accurate** (cited, not recomputed) |
| UCI 30,000 × 25; splits 20,999 / 4,499 / 4,502 | Stage 2; UCI split manifest | **Accurate** (sum = 30,000) |
| UCI target `default payment next month` | UCI split manifest | **Accurate** |
| UCI stratified 70/15/15 seed 42; no calendar timestamps | Stage 2/3; UCI manifest | **Accurate** |
| UCI zip SHA-256 `56c885f8…`; TEST hash `0783db42…` | Stage 2; UCI manifest | **Accurate** |
| Datasets not merged | `merged_with_lendingclub: false`; dataset decision §E | **Accurate** |

**Flags:** none of the listed datasets are planning-only or downloaded-unused. Zenodo is a depositor-filtered Kaggle parent extract (Stage 2); the inventory states that and does not treat Kaggle as a third executed dataset.

---

## 2. MODEL / EVIDENCE TRACEABILITY

Cross-check: Stage 4B/5 reports; `train_only_ebm_meta.json`; S10-A4 metrics `ebm_test_roc_discrepancy`; Stage 8 v2 policy YAML; Stage 6 `seed42_attributions.meta.json`.

| Required distinction | Inventory | Verdict |
| --- | --- | --- |
| Stage 4B TEST EBM = TRAIN+VALIDATION refit; ROC-AUC 0.6799408767429772 | §3 table | **Accurate** |
| Stage 5 = TRAIN-only EBM; raw/Platt TEST ROC-AUC 0.6776693941139847 | §3–§4 | **Accurate** |
| Gap **EXPLAINED**; same TEST n; not Platt changing ROC-AUC vs raw | §3 | **Accurate** |
| Downstream probability = `results/calibration/test/ebm_seed42_calibrated.csv` | Named in **§4 only** | **Correct file, incomplete placement** |
| Downstream model = `results/calibration/artifacts/ebm_train_only_seed42.joblib` | **String absent from the inventory** | **Omission** |

The inventory **does not replace** downstream use with the Stage 4B final EBM. It states Stage 8 onward uses Stage 5 `p_selected`. That is correct.

**Correction C1 (do not apply in this audit):** In inventory §3, name explicitly:

- Probability: `results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected`)
- Model: `results/calibration/artifacts/ebm_train_only_seed42.joblib` (recorded SHA-256 `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4`)
- Not: `results/artifacts/final_explainable_boosting_machine_seed42.joblib`

Stage 6 meta records `stage5_model_path` as that TRAIN-only joblib (copy also under `results/explainability/artifacts/`).

---

## 3. CALIBRATION

Cross-check: `docs/STAGE_5_CALIBRATION_REPORT.md`; `experiments/stage5_calibration/selected_calibration.json`; `platt_record.json`; `isotonic_record.json`; `stage5_test_metrics.json`.

| Topic | Inventory | Verdict |
| --- | --- | --- |
| Raw VAL/TEST CSVs | Paths match Stage 5 outputs | **Accurate** |
| Platt form, a/b, validation fit | Matches `platt_record.json` / Stage 5 report | **Accurate** |
| Isotonic stored, not selected | Matches selection file | **Accurate** |
| Selection: VAL Brier, 0.001 tie, simplicity raw > platt > isotonic | Matches `selected_calibration.json` | **Accurate** |
| Final selected = Platt | Matches | **Accurate** |
| TEST metrics JSON + report | Paths exist | **Accurate** |
| TEST vector hash `e15ddd2f…` | Matches Stage 9.1 / S10 recorded hash | **Accurate** (cited) |
| No TRAIN+VAL calibrator refit | Matches protocol string | **Accurate** |
| All five seeds selected Platt | Matches seed-stability artifact citation | **Accurate** as a citation of that file |

No metric was recomputed in this audit.

---

## 4. EXPLAINABILITY

Cross-check: `docs/STAGE_6_EXPLAINABILITY_REPORT.md`; listed `results/explainability/tables/*`.

| Requirement | Inventory | Verdict |
| --- | --- | --- |
| `interactions=0` | §5 can-claim | **Accurate** |
| Transparent reference, not ground truth | §5 cannot-claim | **Accurate** |
| TreeSHAP not used / not valid for this EBM | §5 | **Accurate** |
| Exact additive SHAP on logit: `phi_i = g_i - mean_TRAIN g_i` | §5 | **Accurate** |
| No causal interpretation | §5 / §11 | **Accurate** |
| n=5000, seed 42; TRAIN-only EBM | §5 | **Accurate** |
| Listed table paths | Files exist under `results/explainability/tables/` | **Accurate** |

**Correction C2:** Stage 6 report **opening sentence** calls the model “the frozen Stage 4B model” (family), while the limitation and `seed42_attributions.meta.json` identify the **TRAIN-only** Stage 5 joblib. The inventory already uses TRAIN-only. The paper must not treat that Stage 6 heading as evidence that Stage 6 scored `final_explainable_boosting_machine_seed42.joblib`. Flag this source-phrasing trap in the inventory before drafting.

---

## 5. SHARIAH GOVERNANCE

Cross-check: Stage 7 v2 report; `AMENDMENT-SHARIAH-001`; `docs/shariah/SHARIAH_GOVERNANCE_SCOPE.md`; S10-A1; Stage 8 v2 §F.

| Required element | Present in inventory? | Verdict |
| --- | --- | --- |
| A. Verified source/provenance | Amendment, catalogs, registers, SBP/SECP/AAOIFI identity | **Yes** |
| B. Implemented predicates | L1/L2, SBP/SECP mappings, AAOIFI gates, firewall, purpose invariance | **Yes** |
| C. Evidence/schema gaps | L1 INSUFFICIENT_SCHEMA; L2 INSUFFICIENT_INFORMATION all TEST; SS8 possession NOT_VERIFIED; SHR-001 retired | **Yes** |
| D. Unvalidated/unavailable clauses | AAOIFI operative clauses unimplemented; no EXPERT_VALIDATED | **Yes** |
| SBP SGF 2025; IBD Circular 01 of 2012; SECP SGR 2023 Regulation 7 | Named | **Yes** |
| No certification / no applicant-level compliance | Named | **Yes** |
| Insufficiency ≠ non-compliance | §6 and §7 (“not from a Shariah score”); §11 | **Yes** |

Controlling implementation Stage 7 v2 + Stage 8 v2, with v1 historical: **Accurate**.

---

## 6. DECISION FUSION

Cross-check: Stage 8 v2 report; v2 `table3`; Stage 9.1 audit; Stage 9.2/9.3 reports.

| Item | Inventory class | Source match | Verdict |
| --- | --- | --- | --- |
| VAL threshold ID `t_low=0.06`, `t_high=0.69`, `t*=0.16` | Freeze-backed Stage 8 v1 | Freeze JSON; table2 | **Accurate** |
| A0 5232 / 203627 / 27 | Freeze-backed 8 v2 / 9.1 | table3 `credit_only_selected_bands` | **Accurate** |
| A1 0 / 208859 / 27 | Freeze-backed | table3 fused | **Accurate** |
| A3/A4 61855 / 0 / 147031 | Freeze-backed; A3=A4 | table3 monolithic; 9.1 `a3_identical_to_a4` | **Accurate** |
| 9.2 costs | Exploratory class C | Stage 9 closure / 9.2 report | **Accurate** |
| 9.3 G1/G3 | Exploratory hypothetical | 9.3 report | **Accurate** |
| Experiment G | Cite-only | 9.2 header; existing CSV | **Accurate** |
| Not real-world approval performance | Stated | Stage 8 v2 §F | **Accurate** |
| Insufficiency ≠ applicant non-compliance | Stated | Stage 8 v2 §F | **Accurate** |

S10-I1 / S10-A4 are correctly **not** used as new fusion experiments.

Minor note (not a count error): A3 extra path `results/decision/metrics/monolithic_test.json` is the Stage 8 **v1** metrics file; the v2 count source of truth in the same row is v2 table3. Prefer v2 table3 when drafting.

---

## 7. STAGE 9

Stage 9 remains **CLOSED**. Inventory states that.

| Activity | Classification | Purpose | Artifacts exist? | Confirmatory vs exploratory | XGBoost / UCI wording |
| --- | --- | --- | --- | --- | --- |
| 9.0 | Design freeze | Freeze A0–A4, thresholds, U1=LR+EBM | Freeze JSON; Stage 9 protocol | Freeze record | OK |
| 9.1 | Class B; report PASS | Ablation on stored `p_selected` | Report + `audit/stage9_1_ablation_run.json` | Previously exposed TEST; not a new confirmatory TEST | OK |
| 9.2 | Class C | Assumed `r` costs on frozen counts | Report + `results/cost_sensitivity/v1/` | Exploratory | OK |
| 9.3 | Class C | G0 vs hypothetical G1/G3 | Report + audit | Exploratory; not Shariah findings | OK |
| 9.4 LR+EBM | Approved written scope | UCI methodology generalization | Report; `uci_test_family_raw.csv` | Freeze-backed **families**, not LC architecture validation | OK — UCI not described as architecture validation |
| 9.4 XGBoost | `DEVIATION-001` C: UNAUTHORIZED BUT SCIENTIFICALLY VALID POST-FREEZE ANALYSIS | Execution-time expansion | Report caveat; `uci_test_selected.json` | **Exploratory**; not pre-registered | Inventory **does not** itself call XGBoost planned, confirmatory, or LC-architecture validation. Prohibited-cell completeness: **C5** |

UCI selected-row metrics in the inventory match `uci_test_selected.json` after ordinary rounding (e.g. ROC-AUC stored `0.7708780071798891` cited as `0.770878`). Degenerate five-seed XGBoost table is recorded. The selected UCI family is XGBoost + isotonic; the inventory labels that row exploratory because of family scope.

**Correction C3:** Explicitly warn that **Stage 4B LC XGBoost** (a declared Stage 4B family; paper-phase readiness already records the distinction) is **not** the Stage 9.4 UCI XGBoost deviation. Mixing those two would falsely look like XGBoost was in the approved 9.4 protocol.

**Correction C5:** The 9.4 XGBoost prohibited-wording cell lists “Approved Stage 9.4 protocol included XGBoost” and “pre-registered selected model.” It does **not** also list the task-required phrases “primary validated model” or “XGBoost is superior overall.” Those prohibitions are implied by §11 ranking language (which is about A0/A1/A3, not UCI families) but should be explicit for 9.4.

---

## 8. STAGE 10

Stage 10 remains **CLOSED**. Inventory states that.

| Activity | Required class | Inventory | New confirmatory TEST? |
| --- | --- | --- | --- |
| S10-I1 | Integrity/provenance, not confirmatory science | Exact string match | **No** |
| S10-R1 | Exploratory/descriptive post-hoc | Exact string match; n=152726/56160 | **No** |
| S10-A1-GAP | Analysis-only / descriptive | Match | **No** |
| S10-A4 | Analysis-only / descriptive comparison | Match; 4B vs 5 EXPLAINED | **No** |

---

## 9. DOCUMENTATION / REPRODUCIBILITY LIMITATIONS

Inventory §10 covers the items this task listed (git null; missing Stage 4B EBM hash; positional `row_ref`; pytest not locking point estimates; XGBoost seed degeneracy; 9.4 deviation provenance) plus additional already-recorded Stage 2–8 limitations.

**Correction C4 — present in Stage 9/10 closure audits but not in inventory §10:**

- Stage 9 protocol / `DEVIATION-001` leftover “DRAFT” wording versus the **APPROVED** Stage 9.4 amendment (documentation lag, not a result rewrite).
- Stage 9.4 report SHA-256 changed after a later provenance caveat; metrics in the report were not changed (`STAGE_9_FINAL_CLOSURE_AUDIT.md` §10).

**Correction C6:** Stage 10 closure also records “LendingClub lacks contract-level Shariah fields” and that S10-A1 “does not independently validate Shariah compliance.” The inventory states this in §2/§6/§9/§11 but does not restate it in §10. Add it to the limitations list so paper Limitations cannot omit it.

These are documentation limitations, not new scientific failures.

---

## 10. CLAIM BOUNDARY AUDIT

Assignment of major planned claims. One category each.

### A. CONFIRMATORY / FREEZE-BACKED CLAIMS

- LC and UCI were acquired, hashed, split as recorded, and not merged.
- LC nine-predictor policy and chronological TEST n=208,886.
- Stage 4B family TEST metrics after freeze, including EBM TRAIN+VAL TEST ROC-AUC 0.6799408767429772 (that fit only).
- Stage 5 TRAIN-only EBM + validation-fit Platt; TEST raw/Platt ROC-AUC 0.6776693941139847; selected method Platt.
- Stage 8 v1 validation thresholds 0.06 / 0.69 / 0.16.
- Stage 8 v2 / 9.1 TEST decision counts A0 / A1 / A3=A4 as stored.
- LC TEST L1/L2 statuses as stored; G0 fusion definition.
- Stage 9.4 UCI **LR and EBM** family TEST as independent credit/calibration methodology (not architecture validation).

### B. DOCUMENTATION / INTEGRITY CLAIMS

- S10-I1: A0/A1/A3 share stored `p_selected`; freeze hashes.
- S10-A4: citation comparison; 4B vs 5 **EXPLAINED**.
- Amendment/protocol/deviation provenance; recorded SHA-256 values.
- Metric definitions (`sklearn.metrics.roc_auc_score` wrapper).
- `git_commit` null; missing Stage 4B joblib hash.

### C. EXPLORATORY CLAIMS

- Stage 9.1 as previously exposed TEST ablation (class B disclosure required).
- Stage 9.2 assumed-cost sensitivity (class C).
- Stage 9.3 G1/G3 hypothetical allocations (class C).
- Stage 9.4 UCI XGBoost + isotonic selected row (class C / execution-time expansion).
- S10-R1 2017 vs 2018 mix (post-hoc, non-confirmatory).
- S10-A1 algebraic A1-review decomposition (analysis-only; not Shariah validation).
- Stage 6 attributions (freeze-backed **method/results for this EBM**, not confirmatory credit performance and not a second model class).
- Stage 4B/5 year slices (descriptive temporal).

### D. UNSUPPORTED / PROHIBITED CLAIMS

All of inventory §11, including: Shariah certification/compliance; applicant-level rulings; expert-validated rules; AAOIFI fully implemented; production/fair-lending/regulatory guarantees; fraud-detection performance; pre-registered 9.4 XGBoost; UCI validates LC architecture or Shariah; governance improves AUC; causal SHAP; Stage 10 confirmatory TEST; 4B and 5 EBM as one model.

---

## 11. PAPER SECTION TRACEABILITY

| Section | Supporting artifact(s) in inventory | Strongest allowable claim | Caveat |
| --- | --- | --- | --- |
| Abstract | Stage 5 TEST JSON; table3; Stage 7 v2 non-certification; S10-A4 4B vs 5 | Frozen LC pipeline is TRAIN-only EBM + Platt `p_selected`; counts as stored; prototype governance | Must name which EBM; no certification; no ranking |
| Introduction | Stage 9.1 §2 RQ; `dataset_decision.md` | Evidence-separated credit / explanation / governance design on LC | Do not use Stage 0 stub `research_question.md` as finalized |
| Related Work | **None in repo** | None from this repository | Literature must be added from **external** sources without inventing repo citations |
| Research Gap / Contributions | Stage 9 protocol (as protocol); Stage 9.1 definitions; §11 prohibitions | State design gap and executed scope | Do not treat protocol hypotheses as proven; stub `contribution_statement.md` unused |
| Data | Stage 2–3; manifests; feature policies | Two datasets, roles, splits, hashes as recorded | Target-doc conflict; selection bias; UCI ≠ LC |
| Methodology | Amendment; shariah_methodology; 4A policy; metric defs; explainability protocol | Evidence separation; L1/L2; G0; additive EBM | Older `SHARIAH_GOVERNANCE_SCOPE.md` lags Stage 8 v2 |
| Experimental Protocol | 3–5 reports; selected_configurations; selected_calibration; freeze JSON; 9/10 protocols | Leakage-safe split; VAL selection; TEST once after freeze | Preserve class labels for 9.1–9.4 and S10 |
| Results | 4B/5 metric JSON; S10-A4 tables | Quote stored metrics with A/B/C EBM rows | Do not mix 4B TEST EBM with Stage 8 `p_selected` |
| Explainability | Stage 6 report + tables | Additive logit SHAP of this EBM | Not causal; not Stage 4B TRAIN+VAL joblib |
| Shariah Governance | Stage 7 v2; catalogs; S10-A1; amendment | Prototype + evidence gap on LC | No compliance/certification |
| Decision Fusion | Stage 8 v2; v2 table3; freeze JSON; 9.1 | Policy counts on frozen `p_selected` | 9.2/9.3 exploratory only |
| Limitations | Inventory §10; Stage 2; 9/10 closures | All listed limitations | Add C4 items when revising inventory |
| Discussion | Freeze-backed facts + labeled exploratory notes | Interpretation without new numbers | No superiority/causal/production language |
| Conclusion | §10.A claims only | Restate non-certification and closed experimental scope | No new results |

UCI belongs in Results or a labeled independent-methodology subsection, not as architecture validation.

---

## 12. MISSING-EVIDENCE CHECK

The outline can be drafted from existing artifacts **except** where listed. Do **not** fill these by new experiments.

| Wanted for a paper | Repository support | Action |
| --- | --- | --- |
| Related Work citations | No literature review artifact | External writing only; do not fabricate |
| Finalized RQ / contribution memo | Stubs only | Use Stage 9.1 §2 and protocols, or leave as writing, not as Stage 0 evidence |
| Stage 4B final EBM SHA-256 | Not recorded | Disclose absence; do not compute in paper-prep unless separately authorized |
| `git_commit` | Null | Disclose |
| AAOIFI operative clauses / EXPERT_VALIDATED | Unavailable / none | Disclose; do not invent |
| Fraud-detection performance | No executed fraud study | Do not claim |
| Operational/regulatory cost of thresholds | Assumed FN:FP scenario only | Do not claim real costs |
| UCI as full-system validation | Explicitly out of scope | Do not claim |
| Explicit downstream joblib path in the inventory | Omitted (C1) | Add to inventory before drafting |
| Stage 9 leftover DRAFT vs APPROVED 9.4 amendment; 9.4 report hash caveat | In Stage 9 closure, not inventory §10 (C4) | Add to limitations list |
| Distinguish LC Stage 4B XGBoost family vs UCI 9.4 XGBoost (C3) | Implied but not explicit | Add warning |
| 9.4 prohibited phrases “primary validated model” / “XGBoost is superior overall” | Not in the 9.4 prohibited cell (C5) | Add wording |
| Contract-level Shariah-field absence as a §10 limitation | In Stage 10 closure and inventory §2/§6, not §10 (C6) | Restate in limitations |

None of these missing items is solved by this audit.

---

## Corrections required (inventory file NOT modified)

1. **C1.** In §3 (not only §4), name the downstream probability `results/calibration/test/ebm_seed42_calibrated.csv` and the downstream model `results/calibration/artifacts/ebm_train_only_seed42.joblib` (recorded SHA-256 `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4`). Do not substitute `results/artifacts/final_explainable_boosting_machine_seed42.joblib`.
2. **C2.** Flag Stage 6 report’s opening “frozen Stage 4B model” sentence versus TRAIN-only `stage5_model_path` in `seed42_attributions.meta.json`.
3. **C3.** Separate Stage 4B LC XGBoost family from Stage 9.4 UCI XGBoost deviation.
4. **C4.** Add Stage 9 closure documentation-lag items (leftover DRAFT wording; 9.4 report hash after provenance caveat).
5. **C5.** Add 9.4 prohibited wording: not a “primary validated model”; not evidence that “XGBoost is superior overall.”
6. **C6.** Restate in §10: LendingClub has no contract-level Shariah fields; S10-A1 does not independently validate Shariah compliance.

No false dataset, count, threshold, hash, or evidence-class upgrade was found. Omissions above are why this is **PASS_WITH_CORRECTIONS** rather than **PASS**. It is not **FAIL**: the inventory does not treat the Stage 4B TRAIN+VAL EBM as the downstream model, does not upgrade 9.4 XGBoost to confirmatory, and does not claim certification or unused datasets.

**Sources inspected (read-only):** `docs/PAPER_EVIDENCE_INVENTORY.md`; Stage 2 report and `docs/raw_data_manifest.json`; Stage 3 split manifests; Stage 5 `selected_calibration.json`; Stage 6 report and `seed42_attributions.meta.json`; Stage 8 v2 `table3_test_decision_outcomes.csv`; Stage 9.4 report and `uci_test_selected.json`; `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md`; `docs/audits/STAGE_10_FINAL_CLOSURE_AUDIT.md`; `docs/audits/PAPER_PHASE_READINESS_AUDIT.md`. Metrics were **cited, not recomputed**.

---

```text
PAPER_EVIDENCE_INVENTORY_AUDIT_STATUS = COMPLETE
```

| Item | Value |
| --- | --- |
| INVENTORY_ACCURACY | **PASS_WITH_CORRECTIONS** |
| EXPERIMENTS_RUN | **NONE** |
| RESULTS_MODIFIED | **NONE** |
| MODELS_MODIFIED | **NONE** |
| STAGE_9_STATUS | **CLOSED** |
| STAGE_10_STATUS | **CLOSED** |
| PAPER_DRAFTING | **NOT_STARTED** |

File created: `docs/PAPER_EVIDENCE_INVENTORY_AUDIT.md`  
Files modified: **NONE** (inventory unchanged)
