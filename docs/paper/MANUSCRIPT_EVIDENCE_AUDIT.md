# MANUSCRIPT EVIDENCE AUDIT

| Item | Value |
| --- | --- |
| **Audit ID** | `MANUSCRIPT-EVIDENCE-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Audited files** | `docs/paper/MANUSCRIPT_DRAFT.md`; `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md` |
| **Audit type** | Diagnostic only — no manuscript rewrite |
| **Experiments run** | **None** |
| **Metrics recomputed** | **No** |
| **Models / data / results modified** | **No** |
| **Web search** | **None** |
| **Manuscript rewrite authorized** | **No** |

Controlling paper documentation inspected: `docs/PAPER_DRAFTING_PROTOCOL.md`; `docs/PAPER_EVIDENCE_INVENTORY.md`; `docs/PAPER_EVIDENCE_INVENTORY_AUDIT.md`; `docs/literature/LITERATURE_REVIEW_EVIDENCE.md`; `docs/literature/LITERATURE_CLAIM_MATRIX.csv`; `docs/literature/LITERATURE_SOURCE_REGISTER.csv`. Stage 2–10 reports and stored JSON/CSV artifacts were inspected where a manuscript numeral or provenance sentence required a source check. Joblib binaries were not loaded or hashed.

---

## 1. Overall classification

**PASS WITH DOCUMENTATION LIMITATIONS**

The first complete draft is scientifically consistent with the frozen Stage 2–10 record on the material points: executed datasets, four model contexts, validation-only Platt calibration, transcribed TEST metrics, additive SHAP method, Shariah non-certification, Stage 9/10 class labels, and literature-package citations. It does not merge M-4B / M-5 / M-9.4-AE / M-9.4-X, does not treat German or Australian Credit as executed, does not claim TEST-set calibration fitting, and does not claim that calibration improved ROC-AUC.

The classification is not `PASS` because of documentation limitations and a small number of provenance slips (wrong source file for the ECE binning rule; a present-tense Stage 9 “leftover DRAFT” claim that is not currently visible in `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md`; planned Table I / Fig. 1–2 not instantiated; bibliographic venue expansions beyond the register; inferred “US” geography). It is not `NEEDS CORRECTION` or `SCIENTIFIC/PROVENANCE INCONSISTENCY` because no stored TEST metric was found to be mistranscribed, and no Shariah/certification or model-identity boundary is crossed.

This audit does **not** authorize a manuscript rewrite.

---

## 2. Executive summary

`MANUSCRIPT_DRAFT.md` is a first IEEE-style draft that, on inspection, transcribes frozen numerals from the artifacts named in `MANUSCRIPT_EVIDENCE_MAP.md` and in the evidence inventory. Abstract and Conclusion stay inside permitted claim language: research prototype; not certification; UCI as independent methodology; exploratory UCI XGBoost not primary/superior; two LendingClub EBM ROC-AUC values kept separate.

**What holds**

- Executed datasets are only the Zenodo LendingClub granting-model extract and UCI Default of Credit Card Clients. German Credit and Australian Credit Approval are labeled literature-only, with register sizes \(n=1000\) / \(n=690\).
- M-4B TEST EBM ROC-AUC `0.6799408767429772` (TRAIN+VALIDATION refit) and M-5 raw/Platt TEST ROC-AUC `0.6776693941139847` (TRAIN-only) match `stage4b_test_metrics.json` and `stage5_test_metrics.json`. The gap is labeled `EXPLAINED`.
- Platt \(a,b\), `fit_split=validation`, TEST Brier/ECE, A0/A1/A3 counts, thresholds `0.06` / `0.69` / `0.16`, Stage 6 SHAP ranks, UCI family-raw LR/EBM, exploratory UCI selected row, S10-R1 year mix, and S10-A1 crosstab match stored files.
- TreeSHAP is stated as unused. Stage 6 opening “frozen Stage 4B model” vs TRAIN-only metadata is disclosed, not silently rewritten.
- Shariah wording matches the required prototype / evidence-gap formulation. `INSUFFICIENT_INFORMATION` is not treated as a ruling.
- Stage 9.1 is class B; 9.2/9.3 class C; 9.4 XGBoost exploratory (`DEVIATION-001`). Stage 10 activities are labeled non-confirmatory.
- Citations `[1]`–`[34]` map to the literature register. Unverified metadata (Platt DOI/URL; Zenodo creators; AAOIFI years) are preserved.

**What does not fully hold (documentation, not new science)**

- §7.7 cites `docs/METRIC_DEFINITIONS.md` for “ECE uses 10 equal-width bins.” That file defines ROC-AUC/PR-AUC/Brier/log loss/bootstrap only. The 10-bin ECE rule is in `docs/STAGE_5_CALIBRATION_REPORT.md`.
- Limitation 22 / protocol paragraph claims leftover `DRAFT` wording in the Stage 9 protocol. The current `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` contains no `DRAFT` string (a later documentation cleanup is consistent with that absence). Closures/inventory still record the leftover historically.
- Table I is in the figure/table plan and in the evidence map but is **not** rendered as a labeled table in the body (dataset facts appear as prose in §7.2–7.3). Fig. 1–2 are “proposed” schematics, not repository image files. Stage 5 reliability-diagram paths are correctly omitted (`[EVIDENCE REQUIRED]`).
- Related-work venue lines expand KDD/ICML ordinals (“19th”, “8th”, “22nd”) beyond the register fields.
- “US consumer LendingClub extract” / “US P2P loans” is not a Stage 2 wording; Stage 2 does not record “United States.”
- Controlling inventory/protocol files still say paper drafting `NOT STARTED`. That is lag in those files, not a manuscript scientific error. This audit does not edit them.

**Language watch-list (mostly negation or selection-criterion use)**

Words such as “best,” “validated,” “compliant,” “certified,” “superior,” “real-time,” and “production-ready” appear almost entirely in **prohibitions**, in the quoted Stage 9.1 design question, or as “best mean validation PR-AUC” for the frozen family-selection rule. Discussion uses “demonstrate,” “conservative,” and “modest,” which should be softened before submission but do not create unsupported empirical claims.

---

## 3. Claim audit

Classification: **A** = directly supported by stored evidence; **B** = supported but requires qualification; **C** = unsupported / evidence missing; **D** = potentially inconsistent with repository provenance.

| Section | Claim | Classification A/B/C/D | Evidence source | Issue |
| --- | --- | --- | --- | --- |
| Title / §1 | Research prototype; no certification language | A | Protocol working title; inventory §11 | None |
| Abstract | Two executed datasets; LC split n; M-4B four families + TRAIN+VAL TEST; M-5 TRAIN-only + VAL Platt; TEST ROC-AUC/Brier/ECE; TreeSHAP unused; L1/L2 statuses; A0/A1/A3 counts; UCI independent; M-9.4-X not primary | A | Split manifests; `stage4b_test_metrics.json`; `stage5_test_metrics.json`; table3; Stage 7/8 v2 | Compression only; class-B label for 9.1 not needed because counts are v2 freeze-backed and score identity is S10-I1 / shared `p_selected` |
| Abstract | “digital credit decisioning” | B | Prototype scope | Does not claim production; still slightly application-flavored |
| Keywords | Omits certified / fraud | A | Protocol §11.1 | None |
| Table plan | Table I from inventory/split manifests | B | Plan vs body | Table I **not instantiated** in the body |
| Table plan | Fig. 1–2 schematic | B | Stage 7/8 v2 | “Proposed” only; no image files |
| Table plan | Stage 5 reliability figures omitted | A | Stage 5 report names paths; no png/pdf under `results/figures/calibration/` | `[EVIDENCE REQUIRED]` justified |
| §4 Intro | Credit scoring as classification [1]; ML benchmarks [2], [3]; PD vs binary [4] | A | LIT-001–004; claim matrix CLM-01–04 | Methodology only; not project TEST |
| §4 | LC P2P literature ≠ Zenodo extract [5], [6], [20] | A | LIT-005/006; DS-001 | None |
| §4 | Quoted Stage 9.1 design question including “independently validated … layers” | B | `docs/STAGE_9_1_ABLATION_REPORT.md` §2 | Quote is accurate. Draft correctly treats it as a **design question**, not a proven result. Keep that qualifier if the quote is retained |
| §4 | German/Australian not executed [22], [23] | A | DS-003/004 `EXECUTED_IN_THIS_PROJECT=NO` | None |
| §4 | No fraud experiment [19] | A | Inventory §11; LIT-019 | None |
| §4 / §5.7 | Instruments “do not license this software to certify US P2P loans” | B | SECP [27]; Stage 2 | “US” geography is not in Stage 2; prohibition itself is required |
| §5.1 | German \(n=1000\), Australian \(n=690\) | A | Register caveats DS-003/004 | Literature sizes, not executed n |
| §5.2 | `interactions=0`; TreeSHAP inappropriate [13] | A | Stage 6 report; LIT-013 | None |
| §5.2 | “US consumer LendingClub extract” | C / B | Stage 2 report (no US string); literature package paraphrase | Geography not a Stage 2 recorded field |
| §5.3 | Platt 1999; no DOI; URL UNVERIFIED [14] | A | LIT-014 | Metadata preserved |
| §6 | Gap relative to literature package, not absolute novelty | A | Protocol writing rules; literature residual gaps | None |
| §6 item 2 | “Leakage-controlled chronological evaluation” | B | Stage 3 report: no newly discovered leakage beyond frozen exclusions | Design wording; not a TEST result |
| §6 item 4 | Predicates “demonstrate” schema insufficiency | B | L1/L2 stored statuses | “Demonstrate” is interpretive; statuses are A |
| §7 table | Four contexts M-4B / M-5 / M-9.4-AE / M-9.4-X | A | Protocol §4 | None |
| §7.2 | LC n, hashes, DOI, CC-BY-4.0, 1,347,681×15 | A | Inventory §2; split manifest; DS-001 | Version 0.1 from literature package, not inventory table |
| §7.2 | Split prevalence 18.7% / 24.9% / 21.2% | B | Stage 4B report §I (rounded) | TEST prevalence also given exactly as `0.2117901630554465` from Stage 5 JSON — rounding dual display |
| §7.3 | UCI n, hashes, stratified split, not merged | A | `audit/uci_split_manifest.json` | None |
| §7.5 | Band/split rules; TEST not used for family/calibrator/threshold choice | A | Split manifest; Stage 4B/5/8 reports | None |
| §7.6 | Family configs; selection PR-AUC 0.388473 / EBM 0.385841, Brier 0.179907 | A | Stage 4B report §D; TEST JSON `config` | “Best mean validation PR-AUC” is selection-criterion language, not overall superiority |
| §7.7 | TRAIN-only `n_train=941267`; Platt a/b; VAL selection; TEST hash | A | `train_only_ebm_meta.json`; `platt_record.json`; `selected_calibration.json`; inventory/S10 recorded hashes | Preprocessor cited as basename `lendingclub_preprocessor.joblib`; meta records `results/artifacts/lendingclub_preprocessor.joblib` |
| §7.7 | “ECE uses 10 equal-width bins (`docs/METRIC_DEFINITIONS.md`)” | D | Stage 5 report §A; `METRIC_DEFINITIONS.md` has **no ECE section** | Correct rule, **wrong source file** |
| §7.7 | All five VAL seeds selected Platt | A | `stage5_seed_stability.json` (`selected_on_this_seed=platt` for seeds 42, 123, 2024, 3407, 9999) | None |
| §7.8 | Additive logit SHAP identity; n=5000; TreeSHAP unused; C2 disclosure | A | Stage 6 report; `seed42_attributions.meta.json` | Follows metadata, not the opening “Stage 4B model” sentence |
| §7.9–7.10 | Prototype; G0 matrix; thresholds; A3=A4; recorded freeze hashes | A | Stage 8 v2; `decision_policy_specification.md`; inventory §7 | Band inequalities match spec: `p < t_low` LOW; `p >= t_high` HIGH |
| §8 | Does not reopen Stage 9/10; class labels B/C; 9.0 `NOT AUTHORIZED` in freeze JSON | A / B | `audit/stage9_0_experimental_freeze.json`; inventory §8–9 | Does not use the exact words “Stage 9 CLOSED” / “Stage 10 CLOSED” except constitution leftover for Stage 10 |
| §8 | Leftover `DRAFT` in Stage 9 protocol | D | Current `STAGE_9_EXPERIMENTAL_PROTOCOL.md` has **no** `DRAFT`; inventory/closures still mention it | Present-tense leftover is stale relative to the current protocol file |
| §9.1 Table III | M-4B TEST metrics | A | `results/metrics/stage4b_test_metrics.json` | Digit-for-digit match |
| §9.1 | EBM bootstrap CIs | A | Same JSON | Match |
| §9.1 | ECE missing for Stage 4B LR | A / B | No `ece` field in that JSON | Marker justified; ECE is also absent for RF/XGB/EBM in the same JSON |
| §9.1 Table F year slices | 2017/2018 EBM descriptive | A | Stage 4B report Table F | Report rounding (6 decimals), not TEST JSON |
| §9.1 Table II | Two EBM identities; EXPLAINED | A | Inventory §3; S10-A4 | Truncated SHA `8d373df1…a0c4` matches full recorded suffix |
| §9.2 Table IV | VAL/TEST calibration | A | `stage5_validation_metrics.json`; `stage5_test_metrics.json` | Full JSON precision; Stage 5 report rounded isotonic ECE to 0 — protocol prefers JSON |
| §9.2 | Platt TEST ROC-AUC = raw; isotonic PR-AUC drop | A | Same TEST JSON | None |
| §9.2 | Paired Platt Brier/ECE differences | A | Stage 5 report Table F (transcribed, not recomputed) | Report rounding |
| §9.2 | 2017/2018 Platt ECE | A | `stage5_temporal.json` | Labeled descriptive |
| §9.3 Table V | SHAP ranks | A | `table1_global_attribution.csv` | Match; identity of centered terms disclosed |
| §9.3 | Agreement JSON | A | `shap_vs_ebm_agreement.json` | Match |
| §9.3 | Local tables exist | A | `table4_local_cases.csv`; `table5_top_feature_effects.csv` | Files exist; not reproduced in full |
| §9.4 Table VI | A0 5232/203627/27; A1 0/208859/27; A3 61855/0/147031 | A | v2 `table3_test_decision_outcomes.csv` | Match; not ranked as winner |
| §9.4 Table VIII | Band default rates | A | `table3b_test_default_rates_by_band.csv` | HIGH n=27 caveat present |
| §9.4 | Contingency all `INSUFFICIENT_INFORMATION` | A | `table4_credit_governance_contingency.csv`; S10-A1 | Not a Shariah score |
| §9.4 | 9.1 class B; 9.2/9.3 class C | A | Inventory §8 | None |
| §9.5 Table VII | UCI family-raw LR/EBM/XGB | A | `uci_test_family_raw.csv` | Match; XGB labeled exploratory |
| §9.5 | Family-raw ECE `[EVIDENCE REQUIRED]` | A / B | No ECE column in that CSV | Justified for that file. Exploratory XGB **raw** ECE `0.20065704943022225` exists in `uci_test_calibration.csv` (not used; correctly not invented into Table VII) |
| §9.5 | Selected XGB+isotonic metrics; not primary | A | `uci_test_selected.json`; `DEVIATION-001` | Exact JSON; class preserved |
| §9.5 | `xgboost_ratified=false` | A | `audit/stage10_s10_a4_sidebyside.json`; S10-A4 metrics | None |
| §9.6 | S10-I1 integrity, not confirmatory | A | `docs/STAGE_10_S10_I1_IDENTITY_REPORT.md` | Positional `row_ref` caveat correct |
| §9.6 Table X | Year mix | A | `results/stage10/v1/tables/s10_r1_year_decision_mix.csv` | Match; post-hoc label present |
| §9.6 Table XI | Gap crosstab; 208859=5232+203627 | A | `s10_a1_gap_crosstab.csv` | Algebra of stored cells, not a new TEST metric; not Shariah validation |
| §10 | Modest LC TEST discrimination; maps differ, scores do not | A / B | Stage 5 JSON; table3 | “Modest” is interpretive |
| §10 | “Calibration improved” TEST Brier/ECE; not ROC-AUC | A / B | Stage 5 paired diffs | Allowed for Brier/ECE; “improved” should stay tied to stored diffs, never to discrimination |
| §10 | “transparency … can be demonstrated” | B | Design + L1/L2/G0 artifacts | Watch-list verb; not a new metric |
| §10 | A0 “conservative” vs A3 | B | Table VI counts | Qualitative reading of stored approval rates |
| §10 | UCI ~0.76–0.77 does not mean LC generalizes | A / B | Table VII | Rounding vs full precision in the table |
| §11 items 1–21, 23–29 | Inventory limitations | A | Inventory §10; constitution leftover; scope file lag | Item 20 (`SHARIAH_GOVERNANCE_SCOPE.md` “Stage 8 … not implemented”) matches current file |
| §11 item 22 | Stage 9 protocol leftover DRAFT | D | Current protocol file has no `DRAFT` | Stale present-tense limitation |
| §12 Conclusion | Prototype; M-5 ROC-AUC; counts; insufficiency ≠ non-compliance; UCI context; no production/fraud | A | Same artifacts as Abstract | Does not over-claim vs Abstract |
| §13 | `[1]`–`[34]` from register | A / B | `LITERATURE_SOURCE_REGISTER.csv` | Venue ordinal expansions beyond register (see §12 of this audit) |
| Evidence map | Citation map `[1]`–`[34]` | A | Matches draft | Table I listed as if present; body has no Table I |
| Controlling docs | Inventory/protocol `PAPER_DRAFTING = NOT STARTED` | D (those files, not the draft) | Inventory header; protocol close | Documentation lag after the draft exists; **not modified** in this audit |

No claim was found that German/Australian were executed, that TEST fitted calibration, that Platt improved ROC-AUC, that UCI validates LC architecture or Shariah, that UCI XGBoost is confirmatory/best/superior, that Stage 4B LC XGBoost equals Stage 9.4 UCI XGBoost, or that the system is Shariah-certified.

---

## 4. Dataset audit

| Check | Finding |
| --- | --- |
| Executed datasets | **Only** LendingClub Zenodo granting extract and UCI Default of Credit Card Clients. Explicit in Abstract, §4, §7.2–7.3 |
| German Credit | Literature-only `[22]`; “must not be read as additional empirical settings” |
| Australian Credit Approval | Literature-only `[23]`; same |
| PaySim / IEEE-CIS / fraud files | Not described as used; fraud performance explicitly not reported |
| LC full-file n | 1,347,681 × 15 — matches inventory / Stage 2 |
| LC splits | 941,267 / 197,528 / 208,886 — matches `audit/lendingclub_split_manifest.json` |
| LC temporal rules | `<= 2016-03` / `2016-04`–`2017-01` / `>= 2017-02` — matches manifest |
| LC file SHA-256 | `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc` — match |
| LC split hashes | TRAIN/VAL/TEST hashes digit-match the manifest |
| LC TEST hash | `4dfedb1ad7785fa3833047135b1883676f3e1b49aca9c87fcdb346e64fd489c6` — match |
| Hash method | SHA-256 of sorted `issue_month\tid` — match |
| `git_commit` | `null` — disclosed |
| Target freeze | `Default` 1=Charged Off, 0=Fully Paid; Stage 2 conflict disclosed |
| Not Islamic data; no contract-level Shariah fields | Stated; matches inventory C6 |
| Selection bias (originated-and-resolved) | Stated |
| Kaggle not a third executed dataset | Stated |
| UCI 30,000 × 25; splits 20,999 / 4,499 / 4,502 | Match UCI manifest (sum 30,000) |
| UCI zip SHA-256 / TEST hash | Match |
| UCI stratified 70/15/15 seed 42; `NO_CALENDAR_TIMESTAMPS`; `merged_with_lendingclub: false` | Match |
| Feature lists | LC nine predictors and exclusions match the split manifest `retained_columns` / `excluded_columns` |

**Flags:** none that imply German/Australian execution. Dual prevalence display (Stage 4B rounded 21.2% vs Stage 5 exact `0.2117901630554465`) is a rounding inconsistency of presentation, not a data-definition error.

---

## 5. Model provenance audit

| Context | Manuscript treatment | Verdict |
| --- | --- | --- |
| **M-4B** | Four LC families; TEST after TRAIN+VALIDATION refit; not used from Stage 8 | **Consistent** |
| **M-5** | TRAIN-only EBM `n_train=941267`; `trained_on=TRAIN_ONLY` in `train_only_ebm_meta.json`; Platt on VAL; `p_selected` downstream | **Consistent** |
| **M-9.4-AE** | UCI LR + EBM; independent methodology; no Shariah layer | **Consistent** |
| **M-9.4-X** | Exploratory `DEVIATION-001`; not primary/best/superior; not merged with LC XGBoost | **Consistent** |
| Two LC EBMs | Table II; Abstract; Discussion; S10-A4 `EXPLAINED` | **Never collapsed** |
| Two XGBoosts | Repeated separation; `[18]` algorithm-only | **Never merged** |
| Stage 6 model | Metadata `model_id=ebm_train_only_seed42`; `stage5_model_path=results/calibration/artifacts/ebm_train_only_seed42.joblib`; opening-sentence trap disclosed | **Consistent** (C2 preserved) |
| M-4B dump SHA | Explicitly **not recorded** | **Consistent** |
| M-5 dump SHA | `8d373df1…a0c4` matches inventory / S10-A4 **recorded** hash (not recomputed here) | **Consistent** |
| Preprocessor names | Table II `preprocessor_train_plus_validation.joblib` vs `lendingclub_preprocessor.joblib` matches inventory/S10-A4 recorded paths | **Consistent** as recorded strings; binaries not inspected |

No sentence treats Stage 4B TEST EBM as the Stage 8 model, or Stage 9.4 UCI XGBoost as a LendingClub result.

---

## 6. Calibration audit

| Requirement | Manuscript | Artifact | Verdict |
| --- | --- | --- | --- |
| Base model TRAIN-only | Yes | `train_only_ebm_meta.json` | Pass |
| Fit split validation | `fit_split=validation`; TEST not used to fit | `platt_record.json`; `selected_calibration.json` | Pass |
| Form \(\sigma(a\operatorname{logit}(p_{\text{raw}})+b)\) | Yes | Same | Pass |
| \(a,b\) | `1.1988263209549705`, `0.6697765046966161` | Exact match | Pass |
| Selection: VAL Brier, 0.001 tie, simplicity, `declared_before_test=true` → Platt | Yes | `selected_calibration.json` | Pass |
| Isotonic stored, not selected | Yes | Same | Pass |
| Protocol string | `validation_only_calibration_no_train_val_calibrator_refit` | Inventory / Stage 5 | Pass |
| TEST vector SHA recorded | `e15ddd2f…469eb` | Inventory; S10-A4 recorded string | Pass (cited, not recomputed) |
| `p_selected` = `p_platt` | Yes | Stage 5 / S10-I1 | Pass |
| Platt TEST ROC-AUC = raw | Both `0.6776693941139847` | `stage5_test_metrics.json` | Pass |
| Claim that calibration improved **discrimination** | Explicitly denied | Protocol §5 | Pass |
| Brier/ECE “improved” in Discussion | Stored TEST Platt Brier/ECE lower than raw | Stage 5 paired-diff table | Pass with wording qualification (see §14) |
| ECE 10 equal-width bins | Rule matches Stage 5 report | **Cited file is `METRIC_DEFINITIONS.md`, which does not define ECE** | **Documentation provenance slip** |
| 2018 Platt ECE deterioration | Descriptive; not recoded | `stage5_temporal.json` | Pass |

---

## 7. TEST metric audit

No manuscript numeral below was found to differ from the named stored file. No new TEST computation is described. Rounding notes are presentation-only.

| Quantity | Manuscript | Source | Match? |
| --- | --- | --- | --- |
| M-4B LR ROC-AUC / PR-AUC / Brier / log loss | 0.6763559009686606 / 0.3406477564928828 / 0.21998431914321218 / 0.6354126164492524 | `stage4b_test_metrics.json` | Yes |
| M-4B RF | 0.6609260816246479 / 0.33258566142201473 / 0.23597628092130948 / 0.6648999360582141 | Same | Yes |
| M-4B LC XGBoost | 0.6854404067747387 / 0.3576696570242051 / 0.2136380371614269 / 0.6149464126269267 | Same | Yes |
| M-4B EBM | **0.6799408767429772** / 0.3534066581608194 / 0.15684495750106664 / 0.48493888407781477 | Same | Yes |
| M-4B EBM ROC-AUC CI | [0.6772520975812178, 0.6828319764466856] | Same | Yes |
| `scale_pos_weight` train+val refit | 4.061108666764441 | Same `config` | Yes |
| M-5 TEST n / n_pos / prevalence | 208886 / 44240 / 0.2117901630554465 | `stage5_test_metrics.json` | Yes |
| M-5 raw/Platt TEST ROC-AUC | **0.6776693941139847** | Same | Yes |
| M-5 Platt Brier / ECE | 0.15616920271522994 / 0.020267295489117824 | Same | Yes |
| M-5 VAL Platt/isotonic Brier | 0.1748453678205707 / 0.17469431274375435 | `stage5_validation_metrics.json` | Yes |
| M-5 isotonic TEST ROC-AUC / PR-AUC | 0.6775144297473418 / 0.3462755761696744 | TEST JSON | Yes |
| `t_low` / `t_high` / `t*` | 0.06 / 0.69 / 0.16 | table2 FN:FP=5:1; v2 `frozen_policy.json` | Yes |
| A0 / A1 / A3 counts | 5232/203627/27; 0/208859/27; 61855/0/147031 | v2 table3 | Yes |
| Approval rates A0/A3 | 0.025047154907461486 / 0.2961184569573835 | table3 | Yes |
| Band default rates LOW/MED/HIGH | 0.03746177370030581 / 0.21622869265863565 / 0.5185185185185185 | table3b | Yes |
| SHAP `fico_n` … `addr_state` | Full table1 values | `table1_global_attribution.csv` | Yes |
| Reconstruction error | 8.881784197001252e-16 | `shap_vs_ebm_agreement.json` | Yes |
| UCI family-raw LR/EBM/XGB ROC-AUC | 0.7572778277972128 / 0.7688563724378406 / 0.7733509623204742 | `uci_test_family_raw.csv` | Yes |
| UCI selected (exploratory) | 0.7708780071798891 / 0.5224208622925242 / 0.1368528550434721 / 0.449533259034068 / 0.01744321566180452 | `uci_test_selected.json` | Yes |
| S10-R1 n / defaults / decisions | 152726 / 56160 and all Table X counts | `s10_r1_year_decision_mix.csv` | Yes |
| S10-A1 cells | 5232 / 203627 / 27 | `s10_a1_gap_crosstab.csv` | Yes |
| M-4B EBM year slices | 0.677804 / 0.377247 / 0.168236 and 2018 triple | Stage 4B report Table F | Yes (report rounding) |
| Platt 2017/2018 ECE | 0.005096425775164428 / 0.06152417312325683 | `stage5_temporal.json` | Yes |
| Freeze / table3 hashes | v1 `4d3da6a9…`; v2 `b8747823…`; table3 `90759eb7…` | Inventory; Stage 10 closure / S10-A4 recorded strings | Yes (cited, not recomputed) |

`[EVIDENCE REQUIRED]` markers checked:

| Marker | Justified? |
| --- | --- |
| Stage 4B LR ECE not in `stage4b_test_metrics.json` | **Yes** (no `ece` key for any 4B family) |
| UCI family-raw ECE not in `uci_test_family_raw.csv` | **Yes** for that CSV. Do not silently copy XGB raw ECE from `uci_test_calibration.csv` without labeling the different file |
| Stage 5 reliability image files | **Yes** (named in Stage 5 report; no image files present under `results/figures/calibration/`) |

---

## 8. Explainability / SHAP audit

| Requirement | Finding |
| --- | --- |
| Additive EBM `interactions=0` | Stated; matches Stage 6 / EBM config |
| Exact additive SHAP-style \(\phi_i=g_i-\mathrm{mean}_{TRAIN} g_i\) on logit / `decision_function` | Stated; matches Stage 6 config JSON in the report |
| TreeSHAP not used | Stated repeatedly; `tree_shap: false` in Stage 6 |
| `shap.AdditiveExplainer` not used | Stated |
| Platt not inside explanation | Stated |
| Sample 5,000 TEST, `RandomState(42)`, without replacement; labels unused | Matches Stage 6 report |
| Not causal; not approval criterion; not second-model confirmation | Stated; Discussion does not convert ranks into causes |
| Stage 4B vs Stage 5 identity | C2 opening-sentence discrepancy **preserved as a limitation**, not rewritten |
| Table V transcription | Digit match to `table1`; tiny shap vs ebm float differences on `revenue` / `home_ownership_n` are in the **source CSV** and are copied, not invented |
| Explainability PNG/PDF | Manifest exists; png/pdf not present; draft does **not** cite those images |

No causal SHAP claim found.

---

## 9. Shariah governance audit

| Boundary | Manuscript | Verdict |
| --- | --- | --- |
| Research prototype for Shariah-oriented governance / evidence traceability | Title, Abstract, §7.1, §7.9, Conclusion | **Preserved** |
| Not certification / fatwa / automated verdict / expert-validated decisioning | Abstract, §7.9, Conclusion | **Preserved** |
| No applicant declared compliant/non-compliant | Abstract, §7.9, §9.4, §9.6, §10, §12 | **Preserved** |
| `INSUFFICIENT_INFORMATION` = evidence/schema gap | Abstract and all governance result paragraphs | **Preserved** |
| LC has no contract-level Shariah fields | Abstract, §7.2, §7.9, C6 limitation | **Preserved** |
| S10-A1 does not validate compliance | §9.6 | **Preserved** |
| No fabricated contract evidence | No invoices/possession invented; circular [26] used only to illustrate absence | **Preserved** |
| No `EXPERT_VALIDATED` | §7.9; limitations | **Preserved** |
| Regulatory sources not treated as project certification | §4, §5.7, §7.9 | **Preserved**; [27] used to **prohibit** certification language |
| A1 HUMAN_REVIEW from G0 × insufficiency, not a Shariah score | §7.9, §9.4 | **Preserved** |
| AAOIFI identity only; clauses unimplemented | §5.7, §7.9 | **Preserved**; years UNVERIFIED not filled |
| Scope-file lag vs Stage 8 v2 | Limitation 20; current scope file still says Stage 8 fusion is **not** implemented | **Accurate disclosure** |
| G1/G3 not empirical Shariah | §8, §9.4 | **Preserved** |

No sentence was found that calls the system Shariah-compliant, certified, or a substitute Shariah Board.

Minor grouping issue (not a certification claim): Introduction cites `[24]–[26], [31]` together as frameworks for “Islamic banking institutions.” `[31]` (IFSB-10) is IIFS guiding principles (FAQ PDF), not an SBP IBI circular. **Recommended** to keep IFSB in the IIFS/identity sentence rather than the Pakistan IBI sentence.

---

## 10. Stage 9 audit

| Requirement | Finding |
| --- | --- |
| Stage 9 remains CLOSED | Draft says it does not reopen Stage 9 and does not start Stage 11. Exact “CLOSED” token is sparse. Closures in the repo remain CLOSED. **Recommended** explicit CLOSED label |
| 9.0 freeze JSON not backdated | `stage9_execution` remains `NOT AUTHORIZED` in `audit/stage9_0_experimental_freeze.json`; draft states this | Pass |
| 9.1 class B | Protocol table and §9.4 | Pass |
| 9.2 / 9.3 exploratory; G1/G3 not Shariah | Protocol table and §9.4 | Pass |
| 9.4 LR+EBM vs XGBoost separated | M-9.4-AE vs M-9.4-X throughout | Pass |
| XGBoost not primary validated / not overall superior | Abstract, §6, §9.5, Conclusion | Pass |
| No winner language for A0/A1/A3 | Explicit “not ranked as winner” | Pass |
| UCI not validation of LC performance or architecture | Abstract, §7.3, §9.5, §10, Conclusion | Pass |
| Five-seed XGBoost table degenerate | Stated as Stage 9.4 / inventory limitation | **B**: the phrase is in inventory and Stage 9.4 **post-execution audit**, not in the Stage 9.4 report body (no “degenerate” hit there) |
| Leftover protocol `DRAFT` | See §3 D-row | Stale vs current protocol file |

---

## 11. Stage 10 audit

| Activity | Required class | Manuscript | Verdict |
| --- | --- | --- | --- |
| S10-I1 | Integrity/provenance; not confirmatory | Quoted class; positional `row_ref` | Pass |
| S10-R1 | Exploratory/descriptive post-hoc; non-confirmatory | Labeled; Table X; not year-tuned policy | Pass |
| S10-A1-GAP | Analysis-only/descriptive | Labeled; not Shariah validation | Pass |
| S10-A4 | Analysis-only/descriptive comparison; EXPLAINED; `xgboost_ratified=false` | Labeled | Pass |
| Stage 10 CLOSED | Closures | Draft does not reopen Stage 10; limitation 29 notes constitution leftover vs CLOSED | Pass with recommended explicit CLOSED token |
| No Stage 10 confirmatory TEST | Native S10 not described as new TEST experiments | Pass |  |

---

## 12. Reference/citation audit

Citation map in `MANUSCRIPT_EVIDENCE_MAP.md` matches the draft’s `[1]`–`[34]` to `LITERATURE_SOURCE_REGISTER.csv` SOURCE_IDs. Every number `[1]`–`[34]` appears in the body (not only in the reference list). `SRC-AAOIFI-SS-INDEX` is unused, as the map states.

| Draft # | SOURCE_ID | Supports associated claims? | Metadata issues |
| ---: | --- | --- | --- |
| [1] | LIT-001 | Credit scoring as classification | None |
| [2]–[3] | LIT-002/003 | ML credit benchmarks; not this TEST | None |
| [4] / [21] | LIT-004 / DS-002 | UCI PD literature + dataset record | None |
| [5]–[6] | LIT-005/006 | LC/P2P literature ≠ Zenodo extract | None |
| [7] | LIT-007 | XAI credit / SME P2P; different population | None |
| [8] | LIT-008 | Fairness discussion only; no project fairness result | None |
| [9]–[11] | LIT-009–011 | GAM/EBM family; [11] labeled preprint | None |
| [12]–[13] | LIT-012/013 | SHAP theory; TreeSHAP not for this EBM | None |
| [14] | LIT-014 | Platt sigmoid method | **No DOI; URL UNVERIFIED** — preserved |
| [15]–[16] | LIT-015/016 | Platt vs isotonic | None |
| [17] | LIT-017 | ECE as reliability summary; not credit population | DOI NONE in register — preserved; URL used |
| [18] | LIT-018 | XGBoost algorithm only | None |
| [19] | LIT-019 | Fraud ≠ default; no fraud result | None |
| [20] | DS-001 | Zenodo primary dataset | **Creator names UNVERIFIED** — preserved |
| [22]–[23] | DS-003/004 | Literature-only datasets | Explicitly not executed |
| [24]–[27] | SBP/SECP | Identity/scope; not LC rulings | [25] PICG republication disclosed |
| [28]–[30] | AAOIFI identity/listing | Identity only | [28]/[29] years UNVERIFIED; [29] URL UNVERIFIED — preserved |
| [31] | REG-IFSB-10 | IIFS governance identity/FAQ | Full standard body not re-parsed — disclosed |
| [32]–[34] | CFPB | Adverse-action motivation; not ECOA compliance of this repo | None |

**Bibliographic expansions not in the register (do not invent; recommended to revert to register venue strings):**

- [10] “Proc. 19th ACM SIGKDD …” — register: `KDD '13 Proceedings 623-631`
- [15] “22nd Int. Conf. Machine Learning” — register: `ICML '05 Proceedings 625-632`
- [16] “8th ACM SIGKDD” — register: `KDD '02 Proceedings 694-699`
- [18] “22nd ACM SIGKDD” — register: `KDD '16 Proceedings 785-794`

No DOI, author, or year was fabricated for UNVERIFIED fields. No `[CITATION MAPPING REQUIRED]` appears; mapping `[1]`–`[34]` is determinate. Residual literature gaps (no 2023–2026 systematic review; no real-time latency paper) are disclosed rather than filled.

In-text use is consistent with the claim matrix: literature is not used to validate this project’s TEST metrics (CLM-36).

---

## 13. Table/figure audit

| ID | In body? | Artifact exists? | Numbers match? | Context correct? | Issue |
| --- | --- | --- | --- | --- | --- |
| Table I (plan) | **No labeled table** | Sources exist | N/A | — | Plan/map list it; body uses §7.2–7.3 prose instead |
| Table II | Yes (§9.1) | Inventory / JSON | Yes | M-4B vs M-5 | Truncated hash in table; full hash in §7.7 |
| Table III | Yes | `stage4b_test_metrics.json` | Yes | M-4B TEST | None |
| Table IV | Yes | Stage 5 VAL/TEST JSON | Yes | M-5 | None |
| Table V | Yes | `table1_global_attribution.csv` | Yes | M-5 sample n=5000 | None |
| Table VI | Yes | v2 table3 | Yes | Frozen `p_selected` | None |
| Table VII | Yes | UCI family-raw CSV + selected JSON | Yes | AE vs X labeled | ECE column correctly `[EVIDENCE REQUIRED]` for the cited CSV |
| Table VIII | Yes | table3b | Yes | TEST bands | HIGH n=27 |
| Table IX | Yes (§7.10) | Stage 8 v2 G0 | Copy match | G0 | Also “proposed Fig. 2” |
| Table X | Yes | `s10_r1_year_decision_mix.csv` | Yes | Post-hoc | Path in plan omitted `v1/` prefix; file is under `results/stage10/v1/tables/` |
| Table XI | Yes | `s10_a1_gap_crosstab.csv` | Yes | Descriptive | Same `v1/` path note |
| Fig. 1 | Proposed only | No image | N/A | Schematic allowed by protocol | Not a stored figure |
| Fig. 2 | Proposed only | G0 already Table IX | N/A | Duplicate of Table IX | Not a stored figure |
| Fig. 3–4 (plan, omitted) | Omitted | Named in Stage 5; **images absent** | N/A | — | `[EVIDENCE REQUIRED]` correct; do not regenerate |

Evidence-map Table X/XI source names omit the `v1/` directory segment; the draft body also uses short names. The files exist at `results/stage10/v1/tables/`. **Recommended** to use the full path. Not a missing-artifact error.

---

## 14. Abstract and conclusion audit

**Abstract**

| Risk | Present? |
| --- | --- |
| Causal claims | No |
| Superiority / best-model claims | No (XGBoost explicitly not overall superior) |
| UCI validates LendingClub | Explicitly denied |
| Shariah certification / applicant rulings | Explicitly denied; insufficiency = schema gap |
| Real-time / production-ready | No |
| External validation of TEST metrics | No |
| Calibration improved ROC-AUC | No; Platt ROC-AUC stated equal to raw |
| Merged EBM or XGBoost contexts | No; M-4B vs M-5 vs M-9.4-X separated |
| Stronger than evidence | “digital credit decisioning” is the only slightly application-flavored phrase; still framed as a research prototype |

**Conclusion**

Same boundaries. Counts and M-5 ROC-AUC match stored artifacts. A1 pattern correctly attributed to `INSUFFICIENT_INFORMATION`, not non-compliance. Independent UCI LR/EBM; exploratory XGBoost not primary. Not a production engine; no fraud performance.

Neither section claims Stage 10 confirmatory TEST, governance-improved AUC, or expert-validated Shariah.

---

## 15. Required corrections

This section identifies what **should** be corrected in a later writing pass. It does **not** rewrite the manuscript and does **not** authorize revision.

### REQUIRED before submission

Documentation / provenance only. No new experiments.

1. **ECE binning source.** In §7.7, cite `docs/STAGE_5_CALIBRATION_REPORT.md` (10 equal-width bins on `[0,1]`; empty bins excluded) instead of `docs/METRIC_DEFINITIONS.md`, which does not define ECE.
2. **Stage 9 leftover `DRAFT`.** Do not state as a present-tense fact that `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` still contains leftover `DRAFT` wording. The current file has no `DRAFT` string. If retained, locate it in a file that still contains it, or describe it as a **historical** closure-audit item.
3. **Table I.** Instantiate a labeled Table I from inventory/split manifests, or remove Table I from the plan/map so plan and body agree.
4. **Fig. 1–2.** Add non-numeric schematics (protocol-permitted) or stop citing “proposed Fig. 1/2” as if they were manuscript figures.
5. **Register-faithful venues.** Revert KDD/ICML ordinal expansions in `[10]`, `[15]`, `[16]`, `[18]` to the literature-register venue strings.
6. **Geography.** Qualify or remove “US consumer” / “US P2P” unless a Stage 2/3 artifact is cited that records United States as the population (Stage 2 report has no such string).

### RECOMMENDED clarification

1. Say explicitly **Stage 9 CLOSED** and **Stage 10 CLOSED** (closures already record this).
2. Replace Discussion “can be demonstrated,” “conservative,” and “modest” with protocol-preferred “the evidence indicates” / “stored counts show fewer A0 approvals than A3.”
3. Keep “Calibration improved Brier/ECE” tied to stored paired differences; never allow it to be read as improved discrimination (already denied in the next sentence — keep that pairing).
4. Note that Stage 4B JSON lacks ECE for **all** families, not only logistic regression.
5. If UCI family-raw XGB ECE is ever filled, transcribe `uci_test_calibration.csv` method `raw` and label the file; do not compute it.
6. Use full paths `results/stage10/v1/tables/...` and `results/artifacts/lendingclub_preprocessor.joblib`.
7. Attribute the degenerate five-seed XGBoost table to the Stage 9.4 post-execution audit / inventory, not generically to the Stage 9.4 report body.
8. Keep IFSB-10 `[31]` out of the Pakistan IBI circular grouping in the Introduction.
9. In Discussion, prefer Table VII full UCI ROC-AUC values over “approximately 0.76–0.77.”
10. “Best mean validation PR-AUC” is acceptable as a frozen selection rule; do not let “best” migrate to TEST or to UCI.

### EVIDENCE GAPS that must remain explicitly marked

Do not fill by invention, web search, or new runs.

- `[EVIDENCE REQUIRED]` Stage 4B family ECE (absent from `stage4b_test_metrics.json`)
- `[EVIDENCE REQUIRED]` UCI family-raw LR/EBM ECE (absent from `uci_test_family_raw.csv`)
- `[EVIDENCE REQUIRED]` Stage 5 reliability-diagram **image files** (named, not present; do not regenerate from scores)
- Platt 1999 DOI / official URL **UNVERIFIED** `[14]`
- Zenodo creator names **UNVERIFIED** `[20]`
- AAOIFI SS 8/9 years **UNVERIFIED**; operative clauses unavailable `[28]`, `[29]`
- Stage 4B final EBM SHA-256 **not recorded**
- `git_commit` null
- No 2023–2026 systematic ML-credit review in the literature package
- No verified real-time latency paper
- IFSB-10 full standard body not re-parsed
- No `EXPERT_VALIDATED` Shariah rule
- Explainability PNG/PDF named in `figure_manifest.json` but not present as files (draft correctly does not cite them)

---

## 16. Final decision

The draft is **evidentially fit to remain the first complete manuscript** under the frozen Stage 2–10 record, with documentation limitations listed above. Frozen science, model identities, calibration protocol, TEST transcription, SHAP method, Shariah boundaries, and Stage 9/10 classes are consistent with the repository.

**Final classification: PASS WITH DOCUMENTATION LIMITATIONS**

A later writing pass should apply §15 required documentation corrections. This audit does not perform that pass and does not authorize it.

```text
MANUSCRIPT_EVIDENCE_AUDIT_STATUS = PASS_WITH_DOCUMENTATION_LIMITATIONS
MANUSCRIPT_REWRITE_AUTHORIZED = NO
EXPERIMENTS_RUN = NONE
RESULTS_MODIFIED = NONE
MODELS_MODIFIED = NONE
DATA_MODIFIED = NONE
```
