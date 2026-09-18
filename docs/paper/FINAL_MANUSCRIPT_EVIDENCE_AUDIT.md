# FINAL MANUSCRIPT EVIDENCE AUDIT

| Item | Value |
| --- | --- |
| **Audit ID** | `FINAL-MANUSCRIPT-EVIDENCE-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Audited manuscript** | `docs/paper/MANUSCRIPT_DRAFT.md` (post documentation-correction pass) |
| **Prior audit** | `docs/paper/MANUSCRIPT_EVIDENCE_AUDIT.md` (`PASS_WITH_DOCUMENTATION_LIMITATIONS`) |
| **Type** | Forensic documentation / publication-safety audit only |
| **Manuscript modified** | **No** |
| **Experiments / recomputes** | **None** |
| **Web search** | **None** |
| **Stage 9 / 10 reopened** | **No** |
| **Stage 11 started** | **No** |

This audit inspects the **current** draft after the five documentation corrections. It does not rewrite the manuscript and does not start the final writing pass.

**Prior required corrections (verified still applied):**

1. ECE 10-bin rule cites `docs/STAGE_5_CALIBRATION_REPORT.md`, not `METRIC_DEFINITIONS.md`.
2. Stage 9 leftover `DRAFT` is historical; current protocol has no `DRAFT` status string; Stage 9/10 stated **CLOSED**.
3. Table I and Fig. 1–2 are instantiated from frozen text/tables (no invented PNG).
4. KDD/ICML `[10]`, `[15]`, `[16]`, `[18]` use register venue strings.
5. “US consumer” removed; “US P2P 2007–2018” is attributed to Stage 2 §14.

---

## 1. Overall classification

**B. READY WITH DOCUMENTATION LIMITATIONS**

No substantive unsupported scientific claim (class **D**) remains. Frozen TEST numerals, four model contexts, validation-only Platt, additive SHAP, Shariah prototype bounds, and Stage 9/10 class labels are consistent with the repository.

Remaining items are documentation limitations, draft markers (`[EVIDENCE REQUIRED]`), and writing-pass wording (interpretive Discussion verbs). They do **not** require new experiments, TEST reopen, or model retraining.

---

## 2. Manuscript claim audit (STEP 1)

Classification: **A** = directly supported by an existing artifact; **B** = supported but needs clearer provenance wording in a later writing pass; **C** = documentation limitation / evidence gap; **D** = unsupported (must be removed or rewritten).

No **D** rows were found in the current draft.

| Location | Claim | Class | Evidence | Issue for final writing |
| --- | --- | --- | --- | --- |
| Title | Research prototype; no certification | A | Protocol working title; inventory §11 | None |
| Abstract | LC n/splits; M-4B TRAIN+VAL TEST; M-5 TRAIN-only + VAL Platt; TEST ROC-AUC/Brier/ECE; TreeSHAP unused; L1/L2; A0/A1/A3 counts; UCI independent; M-9.4-X not primary | A | Split manifests; Stage 4B/5 JSON; table3; Stage 7/8 v2 | Keep M-4B vs M-5 distinct (already done) |
| Abstract | Stage 2 “US P2P 2007–2018” | A | `docs/STAGE_2_DATA_AUDIT_REPORT.md` §14 | Do not reintroduce “US consumer” |
| Abstract | “digital credit decisioning” | B | Prototype scope | Application-flavored; not a production claim |
| Keywords | Omits certified / fraud | A | Protocol §11.1 | None |
| §4 RQ quote | “independently validated … layers” | B | Stage 9.1 §2 exact quote | Keep **design-question** qualifier (already present). Do not let the quote become a result |
| §4 | Two executed datasets; German/Australian not executed | A | Inventory §2; DS-003/004 | None |
| §5 | Literature does not validate this TEST | A | Literature package §4; CLM-36 | None |
| §6 | Gap vs literature package, not absolute novelty | A | Protocol writing rules | None |
| §6.2 | “Leakage-controlled chronological evaluation” | B | Stage 3: no newly discovered leakage beyond frozen exclusions | Design wording |
| §6.4 | Predicates “demonstrate” schema insufficiency | B | L1/L2 stored statuses | Soften verb in writing pass |
| §7 table | M-4B / M-5 / M-9.4-AE / M-9.4-X | A | Protocol §4 | None |
| Fig. 1 | Four-layer text schematic | A | Stage 7 v2 / Stage 8 v2 objects | Caption already says not a PNG |
| Table I | Dataset n, hashes, splits, Stage 2 characterizations | A | Inventory §2; Stage 2; split manifests | None |
| §7.6 | Family selection 0.388473 / EBM 0.385841, Brier 0.179907 | A | Stage 4B report §D | “Best mean” is selection-criterion language only |
| §7.7 | Platt a/b; VAL fit; TEST hash; Stage 8 uses `p_selected` | A | `platt_record.json`; `selected_calibration.json`; inventory | None |
| §7.7 | ECE 10 equal-width bins, empty bins excluded | A | Stage 5 report §A | Correct source |
| §7.8 | Additive logit SHAP; TreeSHAP unused; C2 disclosure | A | Stage 6 report + metadata | None |
| §7.9–7.10 | Prototype; G0; thresholds; freeze hashes | A | Stage 8 v2; spec; inventory §7 | Fig. 2 = Table IX copy |
| §8 | Stage 9/10 CLOSED; class B/C; 9.0 freeze JSON | A | Closures; `stage9_0_experimental_freeze.json` | None |
| §8 | Historical leftover `DRAFT` vs current protocol | A | Closure audit vs current protocol file | Present-tense leftover **not** claimed |
| Table III | M-4B TEST metrics | A | `stage4b_test_metrics.json` | Digit match |
| Table II | Two EBM ROC-AUCs; EXPLAINED | A | JSON + S10-A4 | None |
| Table IV | M-5 VAL/TEST calibration | A | Stage 5 JSON | None |
| Table V | SHAP ranks | A | `table1_global_attribution.csv` | Not causal |
| Table VI–VIII, X–XI | Counts, bands, year mix, gap | A | v2 table3/3b; S10 CSVs | Post-hoc labels present |
| Table VII ECE column | `[EVIDENCE REQUIRED]` | C | See STEP 2 | Convert marker to limitation prose in writing pass |
| Reliability figures | `[EVIDENCE REQUIRED]` | C | STEP 2: images **NOT FOUND** | Convert to “not stored as image files” |
| Stage 4B LR ECE | `[EVIDENCE REQUIRED]` | C | STEP 2: **NOT FOUND** | Convert to “not stored” |
| §10 | “modest”; “Calibration improved” Brier/ECE; “conservative”; “can be demonstrated”; UCI “approximately 0.76–0.77” | B | Stored metrics / paired diffs / table3 | Interpretive; keep paired “did not change ROC-AUC”; prefer Table VII precision |
| §11 | Inventory limitations 1–29 (item 22 historical) | A / C | Inventory §10; current protocol | Honest limitations |
| §12 | Conclusion counts and M-5 ROC-AUC | A | Same artifacts as Abstract | None |
| §13 | `[1]`–`[34]` | A / C | Register | Unverified metadata preserved (STEP 3) |

---

## 3. Remaining evidence-gap inspection (STEP 2)

No values were calculated. Search was path/content lookup only.

### 3.1 Stage 5 reliability-diagram image files

| Check | Result |
| --- | --- |
| Named in Stage 5 report | `results/figures/calibration/figure1_validation_reliability`; `figure2_test_reliability` |
| PNG/PDF/SVG under `results/` | **NOT FOUND** (0 image files) |
| Directory `results/figures/calibration/` | **NOT FOUND** as stored images |
| Other figure manifests | `results/figures/explainability/figure_manifest.json` and `results/figures/shariah/figure_manifest.json` exist; they do **not** contain calibration reliability diagrams; explainability PNG/PDF also absent |
| Runner | `src/calibration/reliability.py` exists (code, not a figure artifact) |

**Recommendation:** Do **not** keep `[EVIDENCE REQUIRED]` as if a recoverable stored figure exists. In the final writing pass, convert to a transparent limitation: reliability diagrams are **named in the Stage 5 report but are not present as image artifacts**; they are omitted and must not be regenerated from scores under the closed-experiment rule.

### 3.2 Stage 4B logistic-regression ECE

| Check | Result |
| --- | --- |
| `results/metrics/stage4b_test_metrics.json` | **NOT FOUND** (`ece` key absent for LR **and** RF/XGB/EBM) |
| S10-A4 `s10_a4_sidebyside.csv` LC logistic_regression `existing_test_ece` | **empty** |
| Stage 4B report Table E | ROC-AUC/PR-AUC/Brier/log loss only; no ECE |

**Recommendation:** Convert `[EVIDENCE REQUIRED]` to “ECE was not stored for Stage 4B families.” Do not compute it. Optional: note the gap applies to all four Stage 4B families in that JSON, not only LR.

### 3.3 UCI family-raw ECE (LR / EBM / exploratory XGBoost)

| Family | `uci_test_family_raw.csv` | Other stored ECE? |
| --- | --- | --- |
| LR (M-9.4-AE) | **NOT FOUND** (no `ece` column) | S10-A4 sidebyside `existing_test_ece` empty. **Do not** use `uci_test_calibration.csv` (that file is the **selected** UCI family, which is XGBoost) |
| EBM (M-9.4-AE) | **NOT FOUND** | Same empty S10-A4 cell |
| XGBoost (M-9.4-X) | **NOT FOUND** in family-raw CSV; S10-A4 exploratory **raw** row ECE empty | **FOUND elsewhere:** `results/uci_generalization/v1/tables/uci_test_calibration.csv` method=`raw`, split=`test`: **ECE `0.20065704943022225`**. Same stored ROC-AUC `0.7733509623204742`, Brier, and log loss as family-raw XGBoost. This is the selected-family **raw** calibration row (exploratory XGBoost), **not** LR/EBM family-raw ECE |

**Recommendation:**

- LR and EBM family-raw ECE: convert marker to “not stored in family-raw artifacts.” **Do not fill.**
- XGBoost: Table VII’s `[EVIDENCE REQUIRED]` is correct **relative to `uci_test_family_raw.csv`**. A later writing pass **may** transcribe ECE `0.20065704943022225` from `uci_test_calibration.csv` **raw**, labeled exploratory / selected-family raw, **or** omit the ECE column for family-raw rows. Do not treat that ECE as LR/EBM. Selected-pipeline ECE `0.01744321566180452` (isotonic) is already reported from `uci_test_selected.json` and must remain exploratory.

---

## 4. Citation audit (STEP 3)

Map `[1]`–`[34]` matches `MANUSCRIPT_EVIDENCE_MAP.md` and `LITERATURE_SOURCE_REGISTER.csv`. All 34 numbers appear in the body. `SRC-AAOIFI-SS-INDEX` unused (redundant). No `[CITATION MAPPING REQUIRED]`. No web search; no invented metadata.

| # | SOURCE_ID | Supports in-text use | Unverified / partial metadata |
| ---: | --- | --- | --- |
| [1] | LIT-001 | CLM-01 credit scoring as classification | None |
| [2]–[3] | LIT-002/003 | CLM-02/03 benchmarks; not this TEST | None |
| [4]/[21] | LIT-004 / DS-002 | CLM-04–06 UCI PD / dataset 350 | None |
| [5]–[6] | LIT-005/006 | CLM-07/08 LC/P2P literature ≠ Zenodo extract | None |
| [7] | LIT-007 | CLM-12 SME P2P XAI; different population | None |
| [8] | LIT-008 | CLM-24 fairness discussion only | None |
| [9]–[11] | LIT-009–011 | CLM-13–15 GAM/EBM; [11] preprint | None |
| [12]–[13] | LIT-012/013 | CLM-16/17 SHAP / not TreeSHAP for this EBM | None |
| [14] | LIT-014 | CLM-18 Platt method | **No DOI; URL UNVERIFIED** |
| [15]–[16] | LIT-015/016 | CLM-19/20 Platt vs isotonic | None |
| [17] | LIT-017 | CLM-21 ECE methodology; not credit | DOI NONE in register (URL verified) |
| [18] | LIT-018 | CLM-22 algorithm only | None |
| [19] | LIT-019 | CLM-23 no fraud result | None |
| [20] | DS-001 | CLM-09 Zenodo primary | **Creator names UNVERIFIED** |
| [22]–[23] | DS-003/004 | CLM-10/11 literature-only | Explicitly not executed |
| [24]–[27] | SBP/SECP | CLM-28–31 identity/scope; not LC rulings | [25] PICG republication disclosed |
| [28]–[30] | AAOIFI | CLM-32–34 identity/listing | **[28]/[29] years UNVERIFIED; [29] URL UNVERIFIED** |
| [31] | REG-IFSB-10 | CLM-35 IIFS identity/FAQ | Full body not re-parsed (PARTIAL) |
| [32]–[34] | CFPB | CLM-25–27 adverse-action motivation | Not ECOA compliance of this repo |

Venue strings for `[10]`, `[15]`, `[16]`, `[18]` now match the register. `[17]` retains “34th ICML / PMLR 70” because that is in the register.

**Claims without a direct literature source (must not be filled by invention):** 2023–2026 systematic ML-credit review; real-time loan-engine latency paper; AAOIFI operative clauses; expert-validated Shariah mappings; literature validation of this project’s TEST metrics (CLM-36 — correctly **not** claimed).

**In-text grouping (writing pass, not a false citation):** Introduction still cites `[24]–[26], [31]` together. `[31]` is IFSB-10 (IIFS), not an SBP IBI circular. Recommended to separate IFSB from the Pakistan IBI sentence.

---

## 5. Model-provenance audit (STEP 4)

| Required boundary | Current manuscript | Verdict |
| --- | --- | --- |
| M-4B EBM = TRAIN+VALIDATION refit; TEST ROC-AUC **0.6799408767429772** | Table II/III; Abstract distinguishes M-4B vs M-5 | **Pass** |
| M-5 EBM = TRAIN-only; `results/calibration/artifacts/ebm_train_only_seed42.joblib`; hash `8d373df1…a0c4` | §7.7 | **Pass** (hash cited as recorded, not recomputed) |
| M-5 raw TEST ROC-AUC **0.6776693941139847**; Platt rank-identical | Abstract; Table II/IV; §7.7 | **Pass** |
| Stage 8 onward uses stored `p_selected` from M-5 | §7.1, §7.7, Table II | **Pass** |
| M-9.4-AE = UCI LR+EBM methodology | Abstract; §7; §9.5 | **Pass** |
| M-9.4-X exploratory; not primary; not superior; not merged with LC XGBoost | Abstract; §5.4; §6.5; §9.5; Conclusion | **Pass** |
| Gap EXPLAINED; not Platt changing rank | Table II; §9.1 | **Pass** |

**No wording found that violates these boundaries.**

---

## 6. SHAP / explainability audit (STEP 5)

| Requirement | Finding |
| --- | --- |
| Additive EBM `interactions=0` | Stated | **Pass** |
| Logit / `decision_function` exact additive identity | §7.8 formula matches Stage 6 | **Pass** |
| TreeSHAP not used | Repeated; `[13]` | **Pass** |
| Stage 6 opening vs TRAIN-only metadata | Disclosed; draft follows metadata | **Pass** |
| Calibration not inside explanation; Platt does not change EBM rank attribution | §7.8; Table II | **Pass** |
| Not proof of model correctness / not causal | §7.8; §9.3; Discussion | **Pass** |
| Sample n=5000 | Stated | **Pass** |

No stronger causal or second-model-confirmation claim remains.

---

## 7. Shariah governance audit (STEP 6)

| Prohibited claim | Found? |
| --- | --- |
| Shariah certification | No (explicitly denied) |
| Applicant-level compliance/non-compliance | No |
| Expert validation | No (`EXPERT_VALIDATED` = none) |
| Contract-level validation from LC | No (fields absent) |
| `INSUFFICIENT_INFORMATION` = religious non-compliance | No (explicitly denied) |
| A1 reject/review as a religious ruling | No (G0 × schema gap; HIGH n=27 REJECT is credit band + insufficiency, not a fatwa) |

Required framing (prototype; evidence-separated layer; schema insufficiency; human-review hold; no LC contract fields; no applicant verdict) is present in Abstract, §7.9, §9.4, §9.6, Conclusion.

**No stronger Shariah statement found.**

---

## 8. Dataset-scope audit (STEP 7)

| Dataset | Manuscript role | Verdict |
| --- | --- | --- |
| LendingClub Zenodo extract | PRIMARY executed | Correct |
| UCI Default of Credit Card Clients | Independent methodology only | Correct; not architecture/Shariah validation |
| German Credit [22] | Literature-only; excluded from Table I | Correct |
| Australian Credit Approval [23] | Literature-only; excluded from Table I | Correct |
| Stage 4B LC XGBoost vs 9.4 UCI XGBoost | Repeatedly separated | Correct |
| Stage 2 US P2P 2007–2018 | Attributed to Stage 2 §14 | Correct; “US consumer” not used for this extract |

Kaggle is not a third executed dataset. Datasets not merged.

---

## 9. TEST-set language audit (STEP 8)

Occurrences of watch-list words. **Do not rewrite here**; recommended boundary for the later writing pass.

| Word / phrase | Location | Supported? | Recommended boundary |
| --- | --- | --- | --- |
| independently **validated** … layers | §4 quoted Stage 9.1 RQ | Quote is accurate | Keep “design question, not proven superiority” (already there) |
| primary **validated** model | Abstract, §6, §8, §9.5, Conclusion | Always **negated** for M-9.4-X | Keep negation |
| **Confirmatory** family TEST / M-5 pipeline | §7 table; §8 | Matches protocol for M-4B TEST-after-freeze and M-5 reporting | Do not extend “confirmatory” to 9.1–9.3 or Stage 10 |
| not a new **confirmatory** experiment / TEST | §8, §9.4, §9.6 | Correct for 9.1 class B and S10 | Keep |
| **Best** mean validation PR-AUC / **Best** validation Brier | §7.6–7.7 | Frozen selection rules | Do not migrate “best” to TEST or UCI |
| not ranked as **best** / **winner** | §7.10, §9.4 | Correct | Keep |
| not overall **superior** / **superiority** | Abstract, §5.4, §9.5, §10 | Correct negations | Keep |
| **proves** / proof | Only in “not a proven…” / “not … proof” | Safe | Keep as negation |
| **demonstrates** schema insufficiency | §6.4 | Statuses stored | Prefer “record” / “the evidence indicates” |
| can be **demonstrated** | §10 last paragraph | Interpretive | Soften |
| **production**-ready / **real-time** | Denied; literature gap | Safe | Keep denials |
| architecture **generalizes** | Denied for UCI vs LC | Safe | Keep denial |
| **causal** | Denied for SHAP | Safe | Keep |
| Shariah **compliant** / **certified** | Denied or quoting SECP prohibition | Safe | Keep |
| Stage 9.2 / 9.3 | Class C exploratory; not reproduced as rankings | Correct | Keep labels if mentioned |
| Stage 9.4 XGBoost | Exploratory; degenerate five-seed noted | Correct | Keep `DEVIATION-001` |
| Stage 10 | Not confirmatory TEST | Correct | Keep class strings |

No sentence was found that upgrades 9.1–9.3, 9.4 XGBoost, or Stage 10 to a new confirmatory TEST.

---

## 10. Table / figure audit (STEP 9)

No figures were generated in this audit.

| ID | Source | Reproducible from stored evidence? | Manually derived? | Notes |
| --- | --- | --- | --- | --- |
| Table I | Inventory §2; Stage 2; split manifests | Yes (transcription) | No new metrics | Instantiated in §7.3 |
| Table II | Stage 4B/5 JSON; inventory §3 | Yes | No | Two EBM identities |
| Table III | `stage4b_test_metrics.json` | Yes | No | Full JSON precision |
| Table IV | Stage 5 VAL/TEST JSON | Yes | No | |
| Table V | `table1_global_attribution.csv` | Yes | No | Tiny shap/ebm float diffs are in the CSV |
| Table VI | v2 table3 | Yes | No | |
| Table VII | `uci_test_family_raw.csv`; `uci_test_selected.json` | Yes except ECE column | ECE markers not calculated | See STEP 2 |
| Table VIII | table3b | Yes | No | |
| Table IX / Fig. 2 | Stage 8 v2 G0 | Yes (copy) | No | Text table; no PNG |
| Table X | `results/stage10/v1/tables/s10_r1_year_decision_mix.csv` | Yes | No | Post-hoc |
| Table XI | `s10_a1_gap_crosstab.csv` | Yes | `208859=5232+203627` is algebra of stored cells | Not a new TEST metric |
| Fig. 1 | Stage 7/8 v2 layer list | Yes as **text schematic** | No new architecture | Remain text-only; no stored image |
| Reliability diagrams | Named in Stage 5; files absent | **No image** | Must not regenerate | Remain omitted / limitation |

---

## 11. Publication blockers (STEP 10)

### A. MUST FIX BEFORE FINAL MANUSCRIPT

These are **writing-pass documentation** items, not new science. No Stage 2–10 artifact change is required.

1. Replace remaining `[EVIDENCE REQUIRED]` draft markers with limitation prose suitable for a paper:
   - Stage 5 reliability diagrams: **not present as image artifacts** (do not regenerate).
   - Stage 4B ECE: **not stored** in `stage4b_test_metrics.json`.
   - UCI family-raw LR/EBM ECE: **not stored** in `uci_test_family_raw.csv`.
   - UCI XGBoost family-raw ECE: either omit, or transcribe `0.20065704943022225` from `uci_test_calibration.csv` method `raw` with exploratory / selected-family provenance — **do not compute**.
2. In the final prose pass, keep the Stage 9.1 research-question quote explicitly a **design question** (already true; do not drop the qualifier).
3. Optional but recommended in the same writing pass (not scientific failures): soften “demonstrate,” “conservative,” “modest,” “can be demonstrated”; cite Table VII instead of “approximately 0.76–0.77”; separate IFSB `[31]` from SBP IBI citations in the Introduction.

**No MUST-FIX item requires experiments, TEST reopen, threshold/calibration change, or model retraining.**

### B. DOCUMENTATION LIMITATIONS THAT MAY REMAIN

Transparent limitations; do not convert into fake scientific failures.

- Platt `[14]` DOI/URL unverified
- Zenodo `[20]` creator names unverified
- AAOIFI `[28]`/`[29]` years/clauses/URL unverified; GS listing identity only
- IFSB-10 full standard body not re-parsed
- No 2023–2026 systematic ML-credit review in the package
- No real-time latency paper
- Stage 4B final EBM SHA-256 not recorded
- `git_commit` null
- Stage 6 opening-sentence vs TRAIN-only metadata (disclosed)
- HIGH band n=27
- Stage 6 sample n=5,000
- 2018 Platt ECE deterioration (descriptive)
- 9.1 class B; 9.2/9.3 class C; 9.4 XGBoost `DEVIATION-001` exploratory; degenerate five-seed table
- Stage 10 post-hoc / integrity / analysis-only classes
- No `EXPERT_VALIDATED` rule; LC has no contract-level Shariah fields
- Fairness not evaluated; no fraud experiment
- Fig. 1–2 are text schematics/copies, not stored PNGs
- Controlling inventory/protocol files still say paper drafting `NOT STARTED` (lag in those files; out of this audit’s edit scope)

---

## 12. Final decision (STEP 11)

**B. READY WITH DOCUMENTATION LIMITATIONS**

The current draft is scientifically consistent with the frozen Stage 2–10 chain. A later **writing** pass may polish prose and convert remaining `[EVIDENCE REQUIRED]` markers into limitation language. That pass is **not** authorized by this audit. It is **not** Stage 11 and **not** a new experiment.

Not **A. READY FOR FINAL WRITING PASS** only because draft markers and a few interpretive Discussion verbs remain — not because of unsupported TEST claims.

Not **C. REQUIRES CORRECTION BEFORE FINAL WRITING PASS**: no substantive unsupported claim remains.

```text
MANUSCRIPT_FINAL_AUDIT_STATUS = READY_WITH_DOCUMENTATION_LIMITATIONS
MANUSCRIPT_REWRITE_REQUIRED = YES_FOR_PROSE_AND_MARKER_CONVERSION_ONLY
NEW_EXPERIMENTS_REQUIRED = NO
NEW_DATA_REQUIRED = NO
NEW_MODEL_TRAINING_REQUIRED = NO
TEST_REOPEN_REQUIRED = NO
STAGE_9_STATUS = CLOSED
STAGE_10_STATUS = CLOSED
STAGE_11_STATUS = NOT_STARTED
```

```text
FILES_CREATED = docs/paper/FINAL_MANUSCRIPT_EVIDENCE_AUDIT.md
FILES_MODIFIED = NONE
EXPERIMENTS_RUN = NONE
RESULTS_MODIFIED = NONE
MODELS_MODIFIED = NONE
DATA_MODIFIED = NONE
MANUSCRIPT_DRAFT_MODIFIED = NO
```
