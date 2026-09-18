# FINAL MANUSCRIPT DOCUMENTATION CLEANUP AUDIT

| Item | Value |
| --- | --- |
| **Audit ID** | `FINAL-MANUSCRIPT-DOCUMENTATION-CLEANUP-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Type** | Documentation-only evidence-marker cleanup and static consistency check |
| **Prior forensic audit** | `docs/paper/FINAL_MANUSCRIPT_EVIDENCE_AUDIT.md` (`READY_WITH_DOCUMENTATION_LIMITATIONS`) |
| **Experiments / recomputes** | **None** |
| **TEST reopened** | **No** |
| **Models trained / retrained** | **None** |
| **New data** | **None** |
| **Stage 2–10 artifacts modified** | **No** |
| **Stage 9 / 10 reopened** | **No** |
| **Stage 11 started** | **No** |
| **Web search / invented citations** | **None** |
| **Final status** | **PASS_WITH_DOCUMENTATION_LIMITATIONS** |

This audit records a documentation-only conversion of remaining `[EVIDENCE REQUIRED]` markers using stored repository artifacts. No metric was calculated. No figure was generated. No historical Stage 2–10 report was rewritten.

---

## 1. Files inspected

### Controlling paper documents

- `docs/paper/MANUSCRIPT_DRAFT.md` (before and after this cleanup)
- `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md` (synchronized)
- `docs/paper/FINAL_MANUSCRIPT_EVIDENCE_AUDIT.md`
- `docs/paper/MANUSCRIPT_EVIDENCE_AUDIT.md` (prior diagnostic; not modified)
- `docs/PAPER_EVIDENCE_INVENTORY.md`
- `docs/PAPER_DRAFTING_PROTOCOL.md`

### Stage reports (read / searched; not modified)

- `docs/STAGE_5_CALIBRATION_REPORT.md`
- `docs/STAGE_4B_MODELING_REPORT.md` (`docs/STAGE_4B_BASELINE_REPORT.md` is **not present**)
- `docs/STAGE_6_EXPLAINABILITY_REPORT.md` (C2 provenance wording already disclosed in the draft; historical file not rewritten)
- `docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md`
- `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` (status CLOSED; leftover `DRAFT` treated as historical)
- `docs/STAGE_9_1_ABLATION_REPORT.md` (class B design-question context)
- `docs/STAGE_10_S10_A4_SIDEBYSIDE_REPORT.md` / `results/stage10/v1/tables/s10_a4_sidebyside.csv`

### Stored metric / calibration artifacts (read; not modified)

- `results/metrics/stage4b_test_metrics.json`
- `results/uci_generalization/v1/tables/uci_test_family_raw.csv`
- `results/uci_generalization/v1/tables/uci_test_calibration.csv`
- `results/uci_generalization/v1/metrics/family_selection.json`
- `results/figures/explainability/figure_manifest.json`
- `results/figures/shariah/figure_manifest.json`
- Search for `results/figures/calibration/` image files
- Search of `results/` for `*.png` / `*.pdf` / `*.svg`
- Search for `results/calibration/uci_test_calibration.csv` (**NOT FOUND**)

### Files modified

- `docs/paper/MANUSCRIPT_DRAFT.md`
- `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md`

### Files created

- `docs/paper/FINAL_MANUSCRIPT_DOCUMENTATION_CLEANUP_AUDIT.md` (this file)

### Explicitly not modified

Historical Stage 2–10 reports, frozen `results/` metrics, models, datasets, literature register, inventory, protocol, constitution, and `MANUSCRIPT_EVIDENCE_AUDIT.md` / `FINAL_MANUSCRIPT_EVIDENCE_AUDIT.md`.

---

## 2. `[EVIDENCE REQUIRED]` markers found initially

Five live markers in `docs/paper/MANUSCRIPT_DRAFT.md` before this cleanup (plus one header sentence describing the marker convention):

| ID | Location (pre-cleanup) | Marker text (summary) |
| --- | --- | --- |
| M0 | Header paragraph | Convention: missing stored values marked `[EVIDENCE REQUIRED]` |
| M1 | Table/figure plan (reliability diagrams) | `[EVIDENCE REQUIRED]` if later recovery of stored images is authorized |
| M2 | §9.1 after Table III | Stage 4B logistic-regression ECE: `[EVIDENCE REQUIRED]` if an ECE column is desired |
| M3 | §9.2 after Table IV | Reliability diagrams omitted (`[EVIDENCE REQUIRED]` for those figure files) |
| M4 | Table VII, logistic_regression ECE | `[EVIDENCE REQUIRED]` (not in `uci_test_family_raw.csv`) |
| M5 | Table VII, EBM ECE | `[EVIDENCE REQUIRED]` (not in that CSV) |
| M6 | Table VII, xgboost ECE | `[EVIDENCE REQUIRED]` (not in that CSV) |

No `TODO`, `FIXME`, or `TBD` markers were present in the manuscript or evidence map.

The string `[CITATION MAPPING REQUIRED]` appears only in a **closed** sentence stating that no such marker was needed for references `[1]`–`[34]`. It is not an open evidence gap.

---

## 3. Disposition of every marker

Classification used here: **A** = existing repository evidence supports a positive statement; **B** = convert to a documented limitation (quantity or file not stored); **C** = remove the marker/claim.

| ID | Disposition | Action taken | Reason |
| --- | --- | --- | --- |
| M0 | **B** | Header rewritten: absent quantities are stated as **not stored** and are not calculated | Marker convention is no longer needed after conversion |
| M1 | **B** | Converted to omission / not-retained-image limitation; marker removed | See Item 1 |
| M2 | **B** | Numerical ECE claim removed; “not stored” wording for **all** Stage 4B families | See Item 2 |
| M3 | **B** | Same limitation as M1, restated in §9.2 without a recovery marker | See Item 1 |
| M4 | **B** | Table cell = `not stored`; prose states not calculated | See Item 3 |
| M5 | **B** | Table cell = `not stored`; prose states not calculated | See Item 3 |
| M6 | **A** (transcribe from a *different* stored file, with exploratory label) | Table cell = `0.20065704943022225` with selected-family-raw / M-9.4-X / `DEVIATION-001` note | See Item 4 |

No marker was resolved by inventing a value, regenerating a figure, or computing ECE from predictions.

---

## 4. Item-by-item evidence reconciliation

### Item 1 — Stage 5 reliability-diagram images

| Check | Result |
| --- | --- |
| Named in `docs/STAGE_5_CALIBRATION_REPORT.md` §E | Yes: `results/figures/calibration/figure1_validation_reliability`; `figure2_test_reliability` (TEST: RAW, Platt, isotonic, reporting only) |
| PNG / PDF / SVG under `results/figures/calibration/` | **NOT FOUND** (image directory absent) |
| Reliability-diagram image anywhere under `results/` | **NOT FOUND** (0 `png`/`pdf`/`svg` under `results/`) |
| Calibration figure manifest | **NOT FOUND** |
| Other figure manifests | Explainability and Shariah manifests exist; they do **not** list calibration reliability diagrams; those PNG/PDF files are also absent |
| Runner code | `src/calibration/reliability.py` exists (code, not a stored figure) |

**Exact decision:** Do not regenerate. Do not infer plot contents. The manuscript now states that the diagrams were **named / referenced** in the historical Stage 5 report and that the image files are **not retained** in the current repository, so the visual artifacts are omitted from the reproducible manuscript package.

The report names paths; this audit does **not** independently assert that image binaries were generated and later deleted—only that the named files are not present now.

**Limitation 30** records this omission. It may remain in the paper.

### Item 2 — Stage 4B logistic-regression ECE

| Check | Result |
| --- | --- |
| `results/metrics/stage4b_test_metrics.json` `ece` key | **NOT FOUND** for `logistic_regression` |
| Same JSON, other families (RF / XGBoost / EBM) | **NOT FOUND** (`ece` absent for all four) |
| `docs/STAGE_4B_MODELING_REPORT.md` ECE | **NOT FOUND** (TEST table: ROC-AUC, PR-AUC, Brier, log loss) |
| S10-A4 `existing_test_ece` for LC logistic_regression | **empty** |

**Exact decision:** No numerical Stage 4B ECE is reported. Wording is “not stored in the Stage 4B metric artifact,” extended for accuracy to all four families in that JSON. **Not calculated.**

### Item 3 — UCI family-raw logistic regression / EBM ECE

| Check | Result |
| --- | --- |
| `uci_test_family_raw.csv` ECE column | **NOT FOUND** (columns: family, seed, split, roc_auc, pr_auc, brier, log_loss, n, n_positive, prevalence) |
| S10-A4 `existing_test_ece` UCI LR | **empty** |
| S10-A4 `existing_test_ece` UCI EBM | **empty** |
| `uci_test_calibration.csv` as LR/EBM ECE | **Not used.** That file is the **selected-family** calibration table (`selected_family=xgboost`) |

**Exact decision:** Table VII cells for LR and EBM ECE = `not stored`. Values are not estimated, not derived from the XGBoost calibration file, and not calculated.

### Item 4 — UCI XGBoost family-raw ECE

Guessed path `results/calibration/uci_test_calibration.csv`: **NOT FOUND**.

Authoritative stored file found:

- Path: `results/uci_generalization/v1/tables/uci_test_calibration.csv`
- Row: `method=raw`, `split=test`, `seed=42`
- **Exact stored ECE:** `0.20065704943022225`
- Same row ROC-AUC `0.7733509623204742`, Brier `0.18173602230220492`, log loss `0.5518604686417851` (match the family-raw XGBoost row)
- `family_selection.json`: `selected_family=xgboost`

The guessed rounded value `0.200657049220` was **not** used. The Stage 9.4 report prints a rounded `0.200657`; the manuscript transcribes the **CSV** digits.

**Exact decision:** Transcribe `0.20065704943022225` **only** as exploratory UCI XGBoost selected-family **raw** ECE (context **M-9.4-X**, `DEVIATION-001`). Explicitly not:

- family-raw CSV ECE (that column does not exist)
- LR or EBM ECE
- a primary validated result
- a superiority / ranking claim
- a reason to change LendingClub conclusions

Selected-pipeline isotonic ECE `0.01744321566180452` remains from `uci_test_selected.json` and remains exploratory.

---

## 5. Previously approved documentation corrections (C1–C6)

Checked against the current draft after this cleanup. All remain in force; none was silently undone.

| ID | Requirement | Current draft |
| --- | --- | --- |
| C1 | Downstream model = `results/calibration/artifacts/ebm_train_only_seed42.joblib` | §7.7; Table II; Abstract M-5 |
| C2 | Stage 6 opening vs TRAIN-only metadata disclosed; historical Stage 6 files not rewritten | §7.8; Limitation 21 |
| C3 | Stage 4B LC XGBoost ≠ Stage 9.4 UCI XGBoost | Abstract; §5.4; §7.6; §9.1; §9.5 |
| C4 | Historical Stage 9 `DRAFT` is historical; current Stage 9/10 **CLOSED** | §8; Limitation 22 / 29 |
| C5 | UCI XGBoost not primary validated / superior | Abstract; §9.5; Conclusion; Table VII note |
| C6 | LC has no contract-level Shariah fields; S10-A1 does not validate compliance | Abstract; §7.9; §9.6; Limitation 24; Conclusion |

---

## 6. Model-context separation (post-cleanup)

| Context | Draft identity | Verdict |
| --- | --- | --- |
| **M-4B** | TRAIN+VALIDATION refit; TEST EBM ROC-AUC **0.6799408767429772**; not used from Stage 8 | Preserved |
| **M-5** | TRAIN-only EBM `ebm_train_only_seed42.joblib` hash `8d373df1…a0c4`; raw/Platt TEST ROC-AUC **0.6776693941139847**; Stage 8 onward uses stored `p_selected` | Preserved |
| **M-9.4-AE** | UCI LR + EBM family-raw; ECE not stored | Preserved |
| **M-9.4-X** | Exploratory UCI XGBoost / `DEVIATION-001`; raw ECE transcribed from selected-family calibration CSV only | Preserved; not merged with M-4B LC XGBoost |

No wording was found that sends the Stage 4B TRAIN+VALIDATION EBM into Stage 8, that treats Platt as changing EBM rank, or that upgrades M-9.4-X to a primary validated model.

---

## 7. Shariah / scientific-claim scan (post-cleanup)

| Prohibited or watch-list phrasing | Found as an affirmative claim? |
| --- | --- |
| Shariah certification / fatwa / applicant-level compliance verdict | **No** (explicitly denied) |
| `INSUFFICIENT_INFORMATION` = religious non-compliance | **No** (explicitly denied) |
| `EXPERT_VALIDATED` rules | **No** (`none`) |
| Contract-level validation from LendingClub | **No** (fields absent) |
| “Best model” / overall superior / winner ranking | **No** (only negated, or validation **selection-criterion** “best mean PR-AUC / Brier”) |
| German / Australian executed | **No** (literature-only) |
| Stage 9.1–9.3 or Stage 10 as new confirmatory TEST | **No** |
| TreeSHAP used for EBM | **No** |
| Calibration changes EBM ranking / SHAP proves correctness | **No** |

Remaining interpretive Discussion verbs (“modest,” “conservative,” “approximately 0.76–0.77,” “can be demonstrated”) are **not** new metrics and are **not** class-D scientific claims. They may be softened in a later prose pass; they are not FAIL conditions.

---

## 8. Confirmations required by this task

| Confirmation | Result |
| --- | --- |
| No new metric was calculated | **Confirmed.** Stage 4B ECE and UCI LR/EBM ECE were left unstored. XGBoost raw ECE was **transcribed** from `uci_test_calibration.csv`. |
| No model was trained or retrained | **Confirmed.** |
| TEST was not reopened | **Confirmed.** |
| No new data was introduced | **Confirmed.** |
| No Shariah certification/compliance claim was introduced | **Confirmed.** |
| Stage 4B / Stage 5 / Stage 9.4 model contexts remain separate | **Confirmed.** |
| No figure was generated | **Confirmed.** |
| Historical Stage 2–10 records not rewritten | **Confirmed.** |

---

## 9. Remaining documentation limitations (may stay in the paper)

These are not fake scientific failures. They do not require experiments.

1. Stage 5 reliability-diagram **image files** named in the Stage 5 report are not retained; omitted (Limitation 30).
2. Stage 4B family ECE not stored in `stage4b_test_metrics.json` (Limitation 18).
3. UCI family-raw ECE not stored for logistic regression or EBM (Limitation 18).
4. UCI XGBoost family-raw CSV has no ECE column; only selected-family raw ECE is stored elsewhere and is exploratory.
5. Unverified literature metadata: Platt `[14]` DOI/URL; Zenodo `[20]` creator names; AAOIFI `[28]`/`[29]` years/URL; IFSB-10 full body not re-parsed.
6. Stage 6 report opening vs TRAIN-only metadata (disclosed; historical files unchanged).
7. M-4B final EBM SHA-256 not recorded; `git_commit` null.
8. Fig. 1–2 remain text schematic / table copy (no PNG).
9. HIGH band \(n=27\); Stage 6 sample \(n=5000\); 2018 Platt ECE deterioration (descriptive).
10. M-9.4-X remains `DEVIATION-001` exploratory; Stage 9.1 class B; 9.2/9.3 class C; Stage 10 non-confirmatory.
11. No `EXPERT_VALIDATED` rule; LC contract-level Shariah fields absent.
12. Optional later prose polish (Discussion verbs; IFSB vs SBP grouping) is writing, not missing science.

---

## 10. Final status

**PASS_WITH_DOCUMENTATION_LIMITATIONS**

Not **PASS**: genuine stored-artifact gaps remain (reliability images; Stage 4B ECE; UCI LR/EBM ECE) and are now stated as limitations rather than draft markers.

Not **FAIL**: no unsupported scientific result, fabricated metadata, model-context mixing, unauthorized experiment, or unsupported Shariah/legal claim was found or introduced.

A later **writing** pass may still polish prose. That pass is not Stage 11 and is not authorized by this cleanup audit beyond the documentation edits already applied.

```text
DOCUMENTATION_CLEANUP_STATUS = COMPLETE
UNSUPPORTED_CLAIMS_REMAINING = NO
EVIDENCE_MARKERS_REMAINING = NONE
NEW_METRICS_CALCULATED = NO
NEW_MODELS_TRAINED = NO
TEST_REOPENED = NO
NEW_DATA_INTRODUCED = NO
SHARIAH_CERTIFICATION_CLAIM_PRESENT = NO
MODEL_CONTEXT_MIXING = NO
FINAL_STATUS = PASS_WITH_DOCUMENTATION_LIMITATIONS
```

```text
FILES_CREATED = docs/paper/FINAL_MANUSCRIPT_DOCUMENTATION_CLEANUP_AUDIT.md
FILES_MODIFIED = docs/paper/MANUSCRIPT_DRAFT.md; docs/paper/MANUSCRIPT_EVIDENCE_MAP.md
STAGE_2_10_ARTIFACTS_MODIFIED = NO
EXPERIMENTS_RUN = NONE
STAGE_9_STATUS = CLOSED
STAGE_10_STATUS = CLOSED
STAGE_11_STATUS = NOT_STARTED
```
