# FINAL PAPER INTEGRITY GATE AUDIT

| Item | Value |
| --- | --- |
| **Audit ID** | `FINAL-PAPER-INTEGRITY-GATE` |
| **Audit date** | 2026-09-16 |
| **Type** | Final scientific / publication-integrity gate (audit + narrow prose corrections only) |
| **Manuscript audited** | `docs/paper/MANUSCRIPT_DRAFT.md` |
| **Prior audits** | `FINAL_MANUSCRIPT_EVIDENCE_AUDIT.md`; `FINAL_MANUSCRIPT_DOCUMENTATION_CLEANUP_AUDIT.md` |
| **Experiments / recomputes** | **None** |
| **Stage 2–10 artifacts modified** | **No** |
| **Stage 11 started** | **No** |
| **Final status** | **PASS_WITH_DOCUMENTATION_LIMITATIONS** |

This gate asks whether the **current manuscript** can truthfully represent the **current repository evidence**. It does not claim the paper is perfect. It records every material wording issue found, the narrow correction applied where justified, and the documentation limitations that must remain.

---

## 1. Files inspected

Controlling paper files: `MANUSCRIPT_DRAFT.md`, `MANUSCRIPT_EVIDENCE_MAP.md`, `FINAL_MANUSCRIPT_EVIDENCE_AUDIT.md`, `FINAL_MANUSCRIPT_DOCUMENTATION_CLEANUP_AUDIT.md`, `PAPER_EVIDENCE_INVENTORY.md`, `PAPER_DRAFTING_PROTOCOL.md`.

Stage reports (not modified): Stage 2 data audit; Stage 3 split/feature; Stage 4B modeling; Stage 5 calibration; Stage 6 explainability; Stage 7 v2 Shariah; Stage 8 v1 policy and v2 fusion; Stage 9 protocol and 9.1–9.4 reports; Stage 9/10 closure audits; Stage 10 I1/R1/A1/A4 reports.

Literature: `LITERATURE_SOURCE_REGISTER.csv`, `LITERATURE_CLAIM_MATRIX.csv`, `LITERATURE_REVIEW_EVIDENCE.md`.

Cited artifacts sampled against the draft: `stage4b_test_metrics.json`; `stage5_test_metrics.json`; `selected_calibration.json`; `uci_test_family_raw.csv`; `uci_test_calibration.csv`; `uci_test_selected.json`; `table1_global_attribution.csv`; `shap_vs_ebm_agreement.json`; `table3_test_decision_outcomes.csv` (v2); `table3b_test_default_rates_by_band.csv`; `s10_r1_year_decision_mix.csv`; `s10_a1_gap_crosstab.csv`; `lendingclub_split_manifest.json`; `lendingclub_feature_policy.csv`.

`docs/STAGE_4B_BASELINE_REPORT.md` is **not present**; `docs/STAGE_4B_MODELING_REPORT.md` is the Stage 4B report.

### Files modified in this gate (prose only)

- `docs/paper/MANUSCRIPT_DRAFT.md` (narrow overstatement corrections listed in §16)
- `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md` (sync note only)

### File created

- `docs/paper/FINAL_PAPER_INTEGRITY_GATE_AUDIT.md` (this file)

### Not modified

Frozen Stage 2–10 results, models, data, historical audit reports, literature register.

---

## 2. Project working title vs manuscript title

The repository project name is “Next-Gen Loan Solutions: AI-Driven Risk Assessment, Fraud Detection, and Real-Time Loan Approval System.”

The manuscript title does **not** use that working title. The executed evidence does **not** support fraud-detection performance or a real-time loan-approval engine. The draft keywords omit those phrases, and Abstract/Conclusion now deny production deployment and fraud-performance reporting.

This is a **repository naming / FYP-title mismatch**, not a manuscript scientific claim. It must not be reintroduced into the paper.

---

## 3. Claim–evidence matrix

Status values: `SUPPORTED` | `SUPPORTED_WITH_LIMITATION` | `OVERSTATED` | `UNSUPPORTED` | `NOT_APPLICABLE`.

Where a row was `OVERSTATED` and a safe prose correction was applied in this gate, **Required Action** records `CORRECTED IN THIS GATE`. Historical wording is preserved in the “Claim (as found)” column.

| Claim ID | Section | Claim (as found before this gate, unless noted) | Evidence artifact | Evidence type | Status | Required action |
| --- | --- | --- | --- | --- | --- | --- |
| C-01 | Title | Research prototype; not Shariah-compliant, certified, or production-ready | Protocol §11; inventory §11 | Method / prohibition | SUPPORTED | None |
| C-02 | Abstract | Prototype for Shariah-oriented governance and evidence traceability; not certification/fatwa/applicant verdict | Stage 7 v2; AMENDMENT-SHARIAH-001; SECP [27] | Governance prototype | SUPPORTED | None |
| C-03 | Abstract | “digital credit decisioning” | No production-engine artifact | Application-flavored prose | OVERSTATED | CORRECTED IN THIS GATE → “credit-risk decision mapping”; added not-production / no-fraud clauses |
| C-04 | Abstract | LC n=1,347,681; splits 941,267 / 197,528 / 208,886; US P2P 2007–2018 | Stage 2 §14; split manifest | Dataset | SUPPORTED | None |
| C-05 | Abstract | Four LC families TRAIN+VAL TEST (M-4B); downstream is TRAIN-only + VAL Platt (M-5) | Stage 4B JSON; Stage 5 joblib / `p_selected` | Model provenance | SUPPORTED | “selected M-4B family” narrowed to **validation-selected** |
| C-06 | Abstract | M-5 TEST ROC-AUC 0.6776693941139847; Platt Brier 0.15616920271522994; ECE 0.020267295489117824 | `stage5_test_metrics.json` method=platt | Frozen TEST | SUPPORTED | None |
| C-07 | Abstract | A0/A1/A3 counts 5232/203627/27; 0/208859/27; 61855/0/147031 | v2 `table3_test_decision_outcomes.csv` | Frozen policy counts | SUPPORTED | Added: research maps on frozen TEST, not production origination |
| C-08 | Abstract | L1/L2 insufficiency; not applicant/contract non-compliance | Stage 7/8 v2; S10-A1 | Governance gap | SUPPORTED | None |
| C-09 | Abstract | Additive logit SHAP; TreeSHAP unused | Stage 6 report | Explainability | SUPPORTED | None |
| C-10 | Abstract | M-9.4-AE methodology only; M-9.4-X exploratory, not superior; LC vs UCI XGBoost not merged | Stage 9.4; `DEVIATION-001` | Independent / exploratory | SUPPORTED | None |
| C-11 | §4 RQ quote | “independently validated … layers” | Stage 9.1 exact quote | Design question | SUPPORTED_WITH_LIMITATION | Keep qualifier (already present). Do not promote quote to a result |
| C-12 | §4 | Two executed datasets; German/Australian not executed; no fraud experiment | Inventory §2; DS-003/004; LIT-019 | Dataset scope | SUPPORTED | None |
| C-13 | §4 | `[24]–[26], [31]` as IBI circulars together | Register: [31]=IFSB-10 IIFS, not SBP IBI | Citation grouping | OVERSTATED | CORRECTED IN THIS GATE: IFSB separated |
| C-14 | §5 | Literature does not validate this TEST | CLM-36 | Literature bound | SUPPORTED | None |
| C-15 | §5 | Related-work claims mapped to LIT-001–019 / DS / SRC / REG | Claim matrix CLM-01–35 | Citation use | SUPPORTED_WITH_LIMITATION | Unverified metadata for [14][20][28][29] preserved, not invented |
| C-16 | §6 | Gap vs recorded package, not absolute novelty; “novel” denied | Protocol writing rules | Contribution bound | SUPPORTED | None |
| C-17 | §6 | “Leakage-controlled chronological evaluation” | Stage 3: no newly discovered leakage beyond frozen exclusions | Design wording | OVERSTATED | CORRECTED IN THIS GATE: frozen exclusions + Stage 3 wording; not a proof of zero leakage |
| C-18 | §6 | Predicates “demonstrate” schema insufficiency | L1/L2 stored statuses | Verb strength | OVERSTATED | CORRECTED IN THIS GATE: “record” |
| C-19 | §6 | `[24]–[27], [31]` as product-approval/documentation texts | [27]=SECP certification prohibition; [31]=IFSB | Citation grouping | OVERSTATED | CORRECTED IN THIS GATE |
| C-20 | §7 table | M-4B / M-5 / M-9.4-AE / M-9.4-X | Protocol §4 | Model contexts | SUPPORTED | None |
| C-21 | Fig. 1 | Four-layer text schematic; no PNG | Stage 7/8 v2 layer list | Architecture transcription | SUPPORTED | Remain text-only |
| C-22 | Table I | Dataset n, hashes, splits, characterizations | Inventory; Stage 2; split manifests | Dataset | SUPPORTED | None |
| C-23 | §7.5 | TEST reporting-only; thresholds/calibrators on validation | Stage 5 `declared_before_test`; Stage 8 v1 table2 | Protocol | SUPPORTED | None |
| C-24 | §7.6 | Best mean VAL PR-AUC 0.388473; EBM 0.385841 / Brier 0.179907 | Stage 4B §D selection string | Validation **selection**, not TEST ranking | SUPPORTED | Do not migrate “best” to TEST |
| C-25 | §7.7 | `ebm_train_only_seed42.joblib`; hash `8d373df1…`; Platt a/b; `p_selected` SHA `e15ddd2f…` | Inventory; `selected_calibration.json`; Stage 5 | M-5 lineage | SUPPORTED | None |
| C-26 | §7.8 | Additive identity; TreeSHAP unused; C2 Stage 6 opening discrepancy disclosed | Stage 6 report + metadata | Explainability + provenance limitation | SUPPORTED | “not valid” narrowed to Stage 6 “not mathematically appropriate” |
| C-27 | §7.9 | Prototype; `EXPERT_VALIDATED`=none; AAOIFI identity only | Rule catalog; AAOIFI IDENTITY_ONLY | Shariah bound | SUPPORTED | None |
| C-28 | Table IX / Fig. 2 | G0 matrix copy | Stage 8 v2 §B | Policy | SUPPORTED | Text copy; no PNG |
| C-29 | §8 | Stage 9/10 CLOSED; 9.1 class B; 9.2/9.3 class C; 9.4 XGB `DEVIATION-001` | Closure audits; protocol | Authorization class | SUPPORTED_WITH_LIMITATION | Live Stage 9 protocol header still says `STAGE 9.0 DESIGN FREEZE` (no leftover `DRAFT`); CLOSED is the closure-audit status. Remain as limitation |
| C-30 | Table III | M-4B TEST metrics including EBM 0.6799408767429772 | `stage4b_test_metrics.json` | Frozen TEST | SUPPORTED | None |
| C-31 | Table II | Two EBM ROC-AUCs; Stage 8 uses M-5 not M-4B | JSON + S10-A4 EXPLAINED | Provenance | SUPPORTED | None |
| C-32 | §9.1 | Stage 4B ECE not stored | JSON has no `ece` key | Documentation gap | SUPPORTED | Limitation 18; not calculated |
| C-33 | Table IV | M-5 VAL vs TEST calibration | Stage 5 JSON | VAL selection / TEST reporting | SUPPORTED | Not swapped |
| C-34 | §9.2 | Reliability diagrams named, images not retained, omitted | Stage 5 §E; no PNG under `results/` | Missing image | SUPPORTED | Limitation 30; not regenerated |
| C-35 | Table V | SHAP ranks; not causal | `table1_global_attribution.csv` | Descriptive sample n=5000 | SUPPORTED | None |
| C-36 | Table VI / VIII | Decision counts; band default rates | v2 table3 / table3b | Frozen TEST maps | SUPPORTED | Not winner ranking |
| C-37 | Table VII LR/EBM ECE | not stored | family-raw CSV; S10-A4 empty ECE | Gap | SUPPORTED | Not calculated |
| C-38 | Table VII XGB ECE 0.20065704943022225 | `uci_test_calibration.csv` method=raw | Exploratory M-9.4-X | SUPPORTED | Exploratory label retained; not superiority |
| C-39 | §9.5 | Selected UCI XGB+isotonic metrics | `uci_test_selected.json` | Exploratory | SUPPORTED | Not primary validated |
| C-40 | Table X | S10-R1 year mix | `s10_r1_year_decision_mix.csv` | Post-hoc descriptive | SUPPORTED | Non-confirmatory label present |
| C-41 | Table XI | S10-A1 gap; 208859=5232+203627 | `s10_a1_gap_crosstab.csv` | Algebra of stored cells | SUPPORTED | Not a Shariah ruling |
| C-42 | §10 | “modest”; “Calibration improved”; “conservative”; “approximately 0.76–0.77”; “can be demonstrated” | Stored numbers exist; verbs interpretive | Discussion | OVERSTATED | CORRECTED IN THIS GATE (see §16) |
| C-43 | §10 | UCI does not show LC architecture generalizes | Table VII vs LC; different targets | Bound | SUPPORTED | None |
| C-44 | §11 | Limitations 1–30 including missing ECE, omitted diagrams, C2, no expert validation | Inventory + stage reports | Honest limitations | SUPPORTED | May remain |
| C-45 | §12 | M-5 ROC-AUC; map counts; not certification/production/fraud | Same artifacts as Abstract | Conclusion | SUPPORTED | Added “research policy maps” / not origination |
| C-46 | §13 | `[1]`–`[34]` from register; unused `SRC-AAOIFI-SS-INDEX` disclosed | Register 35 sources | Bibliography | SUPPORTED_WITH_LIMITATION | Unverified fields not filled |
| C-47 | Working title | Fraud detection / real-time loan approval | No fraud experiment; no latency paper | FYP name | NOT_APPLICABLE | Do not import into manuscript |

No `UNSUPPORTED` scientific result remains after the corrections in §16.

---

## 4. Model-provenance gate

| Required boundary | Verdict |
| --- | --- |
| M-4B EBM = TRAIN+VALIDATION; TEST ROC-AUC **0.6799408767429772** | Pass (Table II/III) |
| M-5 EBM = TRAIN-only `ebm_train_only_seed42.joblib`; hash recorded; raw TEST ROC-AUC **0.6776693941139847**; Platt rank-identical | Pass |
| Stage 8 onward uses stored `p_selected` from M-5, not the M-4B dump | Pass (explicit “No” / “Yes” in Table II) |
| M-9.4-AE vs M-9.4-X; LC XGBoost not merged with UCI XGBoost | Pass |
| Stage 6 opening vs TRAIN-only metadata | Disclosed; historical Stage 6 not rewritten | Pass |

**MODEL_CONTEXT_MIXING = NO**

---

## 5. TEST-set integrity

| Check | Verdict |
| --- | --- |
| No metric calculated after experimental closure in this gate | Pass |
| Stage 10 labeled post-hoc / analysis-only / non-confirmatory | Pass |
| VAL vs TEST not swapped in Table IV | Pass |
| Thresholds identified on validation (`t_low=0.06`, `t_high=0.69`, `t*=0.16`) | Pass |
| Platt `fit_split=validation`; TEST not used to fit | Pass |
| TEST not used to choose M-4B family | Pass |
| Post-hoc not described as prospective validation | Pass |
| “Confirmatory” used only for M-4B family TEST and M-5 pipeline reporting, per protocol | Pass with limitation: do not extend that word to 9.1–9.3 or Stage 10 (already denied) |

No TEST-reopen language found.

---

## 6. Dataset integrity

| Dataset | Role in manuscript | Match to inventory |
| --- | --- | --- |
| LendingClub Zenodo extract | PRIMARY executed | Yes |
| UCI Default of Credit Card Clients | Independent methodology | Yes; not architecture/Shariah validation |
| German Credit [22] | Literature-only; excluded from Table I | Yes |
| Australian Credit Approval [23] | Literature-only | Yes |

Split dates, hashes, targets (`Default` Charged Off/Fully Paid; UCI next-month default), nine LC predictors, and “no newly discovered leakage in Stage 3 beyond frozen exclusions” match Stage 2/3 artifacts after the contribution-2 correction.

---

## 7. Explainability integrity

Stage 6 formula \(\phi_i = g_i - \mathrm{mean}_{TRAIN} g_i\) is transcribed. TreeSHAP unused. EBM is a reference, not ground truth. Agreement 1.0 is identity, not a second model. Sample n=5000 disclosed. Fairness not claimed. Causal ranking denied.

Wording “is not valid” was stronger than Stage 6’s “not mathematically appropriate”; corrected.

---

## 8. Calibration integrity

TRAIN-only EBM + validation-only Platt: correct. Missing Stage 4B and UCI LR/EBM ECE remain “not stored.” Reliability images omitted, not claimed as included. UCI XGBoost raw ECE `0.20065704943022225` is transcribed from `results/uci_generalization/v1/tables/uci_test_calibration.csv` `method=raw`, labeled M-9.4-X / `DEVIATION-001`, not used for LC conclusions.

---

## 9–10. Stage 9 and Stage 10 integrity

Stage 9 CLOSED (closure audit). Leftover `DRAFT` is historical. Current protocol has no `DRAFT` string; header still says `STAGE 9.0 DESIGN FREEZE` (documentation lag, Limitation 22). 9.1 class B; 9.2/9.3 class C; 9.4 XGBoost exploratory. No superiority claim.

Stage 10 CLOSED. S10-I1 integrity; S10-R1 post-hoc; S10-A1 evidence-gap, not a ruling; S10-A4 analysis-only EXPLAINED gap. No model change from Stage 10.

---

## 11. Shariah / Islamic-finance integrity (high sensitivity)

No remaining affirmative claim of certification, fatwa, applicant compliance/non-compliance, contract compliance, expert validation, or implemented AAOIFI clauses.

`INSUFFICIENT_INFORMATION` is framed as evidence/schema insufficiency and a G0 hold (LOW/MEDIUM → HUMAN_REVIEW; HIGH → REJECT as credit band × insufficiency), not a religious ruling.

`SOURCE_VERIFIED_PENDING_EXPERT_REVIEW` is not upgraded to `EXPERT_VALIDATED`.

The pre-gate grouping of IFSB `[31]` with Pakistan IBI circulars **was** an over-grouping; it is corrected. SECP `[27]` is no longer described as a product-approval/documentation circular.

**UNSUPPORTED_SHARIAH_CLAIMS = NO** (after correction of citation grouping)

---

## 12. Legal / regulatory claim gate

Citations to CFPB/ECOA, SBP, SECP, AAOIFI, and IFSB are framed as regulatory **context** / **prohibition of certification language**. The prototype is explicitly not an ECOA originator, not production-ready, and not licensed to certify loans.

Internal “APPROVED” refers to `AMENDMENT-STAGE9-4-AUTHORIZATION`, not a legal licence.

**UNSUPPORTED_LEGAL_CLAIMS = NO**

---

## 13. Novelty / contribution integrity

No “first,” “novel,” “state-of-the-art,” “industry-leading,” or “first Islamic AI loan system” as a project claim. “state-of-the-art” appears only inside bibliographic titles of [2] and [3] (register strings). “Best” appears only as frozen **validation selection-criterion** language or in negations. “First” appears as “first-order GAM” or “First, post-hoc…” (not novelty).

---

## 14. References

`[1]`–`[34]` map to the register as in `MANUSCRIPT_EVIDENCE_MAP.md`. All 34 appear in the body. `SRC-AAOIFI-SS-INDEX` unused (disclosed). No invented DOI/URL/year.

Unverified / partial metadata (must remain):

| # | Issue |
| ---: | --- |
| [14] | No DOI; URL UNVERIFIED |
| [17] | DOI field NONE in register (URL verified) |
| [20] | Creator names UNVERIFIED |
| [28]/[29] | Years UNVERIFIED; [29] URL UNVERIFIED; clauses not retrieved |
| [31] | FAQ PDF verified; full IFSB-10 body not re-parsed |

Pre-gate IFSB/SBP grouping: **corrected** (REFERENCE_PROBLEMS after correction = remaining unverified metadata only).

---

## 15. Figures and tables

| ID | Exists as claimed? | Values from stored artifact? |
| --- | --- | --- |
| Tables I–XI | Unique numbers; all instantiated | Yes (ECE “not stored” cells are explicit gaps) |
| Fig. 1 | Text schematic; caption denies PNG | Yes |
| Fig. 2 | Captioned copy of Table IX | Yes |
| Reliability diagrams | Explicitly omitted | N/A |

**Presentation limitation (not a false figure):** in §9, Table III appears before Table II, and Table VIII before Table VII. Numbers remain unique. Optional later reorder only.

**FIGURE_TABLE_PROBLEMS = PRESENTATION_ORDER_ONLY**

---

## 16. Abstract / conclusion stress test

**Before this gate**, a reviewer reading only the Abstract could still hear “digital credit decisioning” plus APPROVE/REJECT counts as a live origination engine, and could read “the selected M-4B family is the EBM” as TEST-set selection.

**After this gate:**

- Abstract denies production engine and fraud performance.
- Counts are labeled research policy-map assignments on frozen TEST.
- M-4B selection is labeled **validation-selected**.
- Conclusion labels maps as research policy maps, not origination outcomes.
- Neither Abstract nor Conclusion claims superiority, generalization, certification, legal compliance, causality, or fraud detection.

Residual stress-test limitation: the **repository/FYP working title** still says fraud detection and real-time approval. The manuscript must keep refusing that title as a scientific claim.

---

## 17. Corrections applied in this gate

All are wording-only. No metric was computed.

1. Abstract: “digital credit decisioning” → credit-risk decision mapping; not a production engine; no fraud performance.
2. Abstract: validation-selected M-4B EBM; APPROVE/REVIEW/REJECT = research maps on frozen TEST.
3. Introduction: IFSB `[31]` separated from SBP IBI `[24]`–`[26]`.
4. §6: SECP `[27]` and IFSB `[31]` no longer lumped as product-approval documentation.
5. Contribution 2: leakage wording aligned to Stage 3 (“no newly discovered leakage beyond frozen exclusions”), not a guarantee.
6. Contribution 4: “demonstrate” → “record”.
7. §7.8: TreeSHAP “not valid” → Stage 6 “not mathematically appropriate”.
8. Discussion: removed modest / improved / conservative / approximately 0.76–0.77 / can be demonstrated; replaced with stored numerals and map-count comparisons.
9. Conclusion: research policy maps; not origination outcomes.

---

## 18. Phase 17 watch-list (post-correction)

| String | Remaining uses | Justified? |
| --- | --- | --- |
| `[EVIDENCE REQUIRED]` / TODO / FIXME / TBD | None in draft | Yes |
| DRAFT | Historical leftover `DRAFT` in Limitation 22 / §8; document IDs | Yes (historical) |
| best | Validation selection criterion; “not ranked as best”; “not confirmed best model” | Yes |
| superior | Only in negations | Yes |
| state-of-the-art | Bibliographic titles [2][3] only | Yes |
| first | first-order GAM; “First, post-hoc…” | Yes |
| certified / certification / fatwa / compliant / non-compliant | Denials, SECP quote, or “not Shariah non-compliant” | Yes |
| legally compliant | Absent | Yes |
| causal | Denied | Yes |
| proves / guarantees | “not a proven…” / “fairness guarantees” as **non**-contributions | Yes |
| novel | Explicitly not claimed | Yes |

---

## 19. Remaining documentation limitations (may stay)

These are not fake scientific failures.

- Reliability-diagram image files named in Stage 5 are not retained.
- Stage 4B family ECE not stored; UCI LR/EBM family-raw ECE not stored.
- Unverified literature metadata ([14][20][28][29]; IFSB-10 full body).
- Stage 6 report opening vs TRAIN-only metadata (disclosed; historical files unchanged).
- M-4B final EBM SHA-256 not recorded; `git_commit` null.
- Fig. 1–2 text-only; Results table order not sequential.
- HIGH band n=27; Stage 6 sample n=5000; 2018 Platt ECE deterioration (descriptive).
- M-9.4-X remains `DEVIATION-001` exploratory; 9.1 class B; 9.2/9.3 class C; Stage 10 non-confirmatory.
- No `EXPERT_VALIDATED` rule; LC contract-level Shariah fields absent.
- Live Stage 9 protocol header still `STAGE 9.0 DESIGN FREEZE` while closure audits say CLOSED.
- Constitution leftover that Stage 10 is not started; older `SHARIAH_GOVERNANCE_SCOPE.md` lag.
- FYP/project working title overclaims relative to executed evidence.
- Optional IEEE prose polish (table order, further sentence smoothing) is writing, not missing science.

---

## 20. Why this is not PASS, and not FAIL

Not **PASS**: known evidence/provenance/documentation limitations remain (missing images, unstored ECE, unverified bibliographic fields, Stage 6 wording discrepancy, protocol-header lag). The instruction prefers an honest `PASS_WITH_DOCUMENTATION_LIMITATIONS` over overstating certainty.

Not **FAIL**: after the listed prose corrections, no material unsupported scientific claim, fabricated evidence, model-context mixing, unauthorized result, or unsupported Shariah/legal claim remains.

The manuscript can now truthfully represent the frozen Stage 2–10 record **if those limitations stay visible**.

```text
FINAL_PAPER_INTEGRITY_GATE = PASS_WITH_DOCUMENTATION_LIMITATIONS

UNSUPPORTED_SCIENTIFIC_CLAIMS = NO
OVERSTATED_CLAIMS = YES_THEN_NARROWED
UNSUPPORTED_SHARIAH_CLAIMS = NO
UNSUPPORTED_LEGAL_CLAIMS = NO
MODEL_CONTEXT_MIXING = NO
REFERENCE_PROBLEMS = UNVERIFIED_METADATA_ONLY
FIGURE_TABLE_PROBLEMS = PRESENTATION_ORDER_ONLY
EVIDENCE_MARKERS_REMAINING = NONE
NEW_METRICS_CALCULATED = NO
NEW_MODELS_TRAINED = NO
NEW_DATA_INTRODUCED = NO
TEST_REOPENED = NO
STAGE_2_TO_10_RESULTS_CHANGED = NO

MANUSCRIPT_STATUS = INTEGRITY_GATE_PROSE_NARROWED
NEXT_ACTION = Optional writing polish only; do not start Stage 11; do not reopen experiments; keep documentation limitations visible
```

```text
FILES_CREATED = docs/paper/FINAL_PAPER_INTEGRITY_GATE_AUDIT.md
FILES_MODIFIED = docs/paper/MANUSCRIPT_DRAFT.md; docs/paper/MANUSCRIPT_EVIDENCE_MAP.md
EXPERIMENTAL_ARTIFACTS_MODIFIED = NO
```
