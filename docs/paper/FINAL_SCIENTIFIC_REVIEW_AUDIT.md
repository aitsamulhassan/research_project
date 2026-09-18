# Final Scientific Reviewer Audit

| Item | Value |
| --- | --- |
| **Document ID** | `FINAL-SCIENTIFIC-REVIEW-AUDIT` |
| **Audit date** | 2026-09-17 |
| **Type** | Scientific reviewer diagnosis only (no edits) |
| **Review PDF** | `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf` |
| **LaTeX source** | `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` |
| **Web search** | **None** |
| **Experiments / recomputes** | **None** |

This audit examines the current manuscript as a skeptical IEEE Access scientific review. It does not predict acceptance, assign a score, or rank the paper. Requested path `docs/paper/PAPER_EVIDENCE_INVENTORY.md` was **not found**; inventory used: `docs/PAPER_EVIDENCE_INVENTORY.md`.

No manuscript, table, reference, LaTeX, PDF, metric, model, dataset, calibration, or threshold was modified.

---

## 1. Executive Summary

The paper is a **research-prototype / integration / evidence-traceability** study, not a new classifier, not a certified Islamic-finance engine, and not a production decision system. The executed evidence supports: (i) a chronological LendingClub credit-scoring pipeline with two distinct EBM fits (M-4B vs M-5); (ii) validation-only Platt calibration of the TRAIN-only EBM; (iii) an additive logit-scale attribution identity on that M-5 EBM; (iv) a governance layer that records schema insufficiency on LendingClub; (v) frozen research maps on stored `p_selected` whose counts differ while scores do not; (vi) independent UCI logistic-regression / EBM methodology context, with UCI XGBoost kept exploratory (`DEVIATION-001`).

The main scientific tension a reviewer will press is **claim scale versus empirical reach**. The introductory design question asks whether evidence-separated layers yield a more transparent and defensible digital-financing pipeline than a monolithic classifier without materially sacrificing predictive performance. The stored results show object-separation and map-dependent counts on a conventional US P2P extract that contains **no** contract-level Shariah fields, so fused A1 assigns **0 APPROVE** and almost all TEST rows to simulated `HUMAN_REVIEW`. The manuscript itself labels the sentence a design question, denies operational superiority, and states that the question is only partially addressable. Those hedges are scientifically honest; they do not remove the mismatch a reviewer may still perceive between title/design question and the evidence-gap outcome.

Novelty, as written, is a **new combination / framework application** of existing methods (EBM, Platt, additive SHAP-style terms, a researcher fusion matrix) on a hashed extract, plus a documented evidence-gap for Shariah-oriented predicates. The paper correctly avoids calling the architecture “novel.” Related work is scoped to a recorded 1997–2022 scholarly set plus named regulatory instruments; the gap is explicitly relative to that package, not an absolute historical first.

No scientific contradiction was found among abstract, methods, results, tables, and the frozen keys listed in Section 6. No TreeSHAP use is claimed. Model contexts M-4B / M-5 / M-9.4-AE / M-9.4-X are not silently merged. German/Australian remain literature-only.

**MUST_FIX_BEFORE_SUBMISSION (scientific):** none identified. Remaining issues are interpretive positioning, contribution-weight, presentation (table-number reading order; table-heavy / figure-light layout), and already-recorded author-metadata incompleteness (venue process, not a scientific rewrite).

---

## 2. Actual Manuscript Inventory

Inspected: `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf` (text layer, all 13 pages) and `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex`. Not inferred from generic audit language.

| Item | Count / record |
| --- | --- |
| Pages | **13** (PDF markers `-- 1 of 13 --` … `-- 13 of 13 --`; layout-repair audit agrees) |
| Numbered tables | **11** (`TABLE 1`–`TABLE 11`) |
| Unnumbered tabulars | **3** (model-context IDs; governance treatment A–D; experimental-protocol stage grid) |
| Figures | **1** (`FIGURE 1`) |
| Raster / `\includegraphics` figures | **0** |
| Numbered equations | **1** (Eq. (1) on PDF page 6) |
| Additional display math | Platt form is **inline** \(\sigma(a\cdot\operatorname{logit}(p_{\mathrm{raw}})+b)\); thresholds \(t_{\mathrm{low}}, t_{\mathrm{high}}, t^{*}\) are inline; \(C=\infty\) renders on page 6 |
| Major sections (IEEE I–IX) | I Introduction; II Related Work; III Research Gap and Contributions; IV Methodology; V Experimental Protocol; VI Results; VII Discussion; VIII Limitations; IX Conclusion; then References `[1]`–`[34]`; empty biography nameplates |

**FIGURE 1 (actual content):** a four-row **text schematic table** (Layer / Documented object / Not). Caption: “Evidence-separated research-prototype layers (text schematic; no stored PNG/PDF; no new numbers).” Present on PDF page 5. Not a process diagram image.

**FIGURE 2:** **absent by design.** Source does not `\ref` a missing Fig. 2. `TABLE 9` caption states the G0 matrix is not repeated as a separate figure. Evidence map records Fig. 2 omitted.

**Equation (1) (actual content):** \(\phi_i(x)=g_i(x_i)-\operatorname{mean}_{\mathrm{TRAIN}} g_i\). Present. In-text “In (1)” resolves.

**Referenced figure/equation missing?** **No.** Fig. 1 exists; Eq. (1) exists.

**Tables in PDF reading order (not numerical order):** TABLE 1 (p. 6 methods) → FIGURE 1 (p. 5, float) → TABLE 9 (p. 7 methods, G0) → TABLE 2–6 (p. 9 results) → TABLE 7, 8, 10, 11 (p. 11). TABLE 9 is numbered 9 because the source sets `\setcounter{table}{8}` in methods.

**Do tables communicate the reported evidence?** Yes for the stored numerical claims (datasets, two EBMs, M-4B families, M-5 calibration, attributions, decision counts, UCI families, band rates, year mix, L2×band). They are dense (full stored precision) and table-heavy relative to figures.

Empty `IEEEbiographynophoto` nameplates appear on PDF page 13. Template placeholders remain (`xxxx 00, 0000`; DOI `10.1109/ACCESS.2024.0429000`; footer `VOLUME 11, 2023`).

---

## 3. Central Contribution

**Central contribution (as the manuscript actually argues, not as invented novelty):**

A **research prototype** that keeps credit-risk scoring, additive explainability, and Shariah-oriented governance evidence as **separate objects**, fuses them **only** at a frozen decision map on stored calibrated probabilities, and reports that architecture on a hashed chronological LendingClub extract, with a separate UCI credit/calibration methodology context.

### Concrete claimed contributions (Section III; five enumerated items)

| # | Claimed contribution | Type | Supported by executed evidence? |
| --- | --- | --- | --- |
| 1 | Evidence-separated pipeline on LendingClub; fusion is a map on `p_selected`, not an end-to-end Shariah score | Methodological + decision-policy / framework | **Yes (direct + policy simulation).** Layers and G0/A0/A1/A3 artifacts exist. |
| 2 | Chronological split, train-only preprocessor for the downstream EBM, validation-only calibration, one TEST report after freeze; hashes recorded | Methodological + empirical protocol | **Yes (direct).** Split n and hashes match inventory/manifests. “No newly discovered leakage” is a **recorded audit statement**, not a proof that every leakage path is absent (the paper says this). |
| 3 | Additive EBM (`interactions=0`) with exact additive logit SHAP-style decomposition of **that** model; TreeSHAP not used | Explainability | **Yes, as model attribution of M-5.** Perfect SHAP–EBM agreement is the **identity of centered terms** (paper discloses). Not a second-model confirmation. |
| 4 | Governance / evidence-gap prototype: schema insufficiency; not applicant-level compliance; no `EXPERT_VALIDATED`; AAOIFI clauses unimplemented | Shariah-governance (prototype) | **Yes as an evidence-gap / predicate implementation.** **Not** as working Islamic-contract decisioning. |
| 5 | Independent UCI LR+EBM methodology; UCI XGBoost exploratory (`DEVIATION-001`) | Empirical methodology context | **Yes, with the exploratory label on M-9.4-X.** Does not validate LC architecture or Shariah. |

**Explicitly not claimed (Section III):** certified Islamic-finance engine; fraud detector; new confirmatory test after frozen maps; proof that governance improves discrimination; proof that XGBoost is superior overall; expert-validated Shariah; fairness guarantees.

### What is / is not a “new method”

| Category | Finding |
| --- | --- |
| New algorithm / new estimator | **Not claimed.** EBM, Platt, isotonic, ROC-AUC/Brier/ECE, SHAP additive identity, XGBoost are existing methods. |
| New combination / integration | **Yes, this is the paper’s actual contribution class:** firewall + frozen fusion map + separate explanation object. |
| New empirical comparison | **Partial:** LC family TEST (M-4B) and UCI family-raw TEST (M-9.4-AE) are executed comparisons; they are not a unified architecture generalization test. |
| Framework / application | **Yes:** research prototype on a public conventional P2P extract. |
| Governance / policy formulation | **Yes:** G0 matrix and validation-derived \(t_{\mathrm{low}}=0.06\), \(t_{\mathrm{high}}=0.69\), \(t^{*}=0.16\) under a researcher cost scenario. |
| Exploratory finding | **Yes, labeled:** M-9.4-X; 9.2/9.3 class C (not ranked in main text); S10-R1 year mix; S10-A1 algebra. |

**Interpretation-dependent (not a new TEST number):** “more transparent and defensible than a monolithic classifier”; “independently validated and auditable evidence layers” inside the design-question quote; operational usefulness of `HUMAN_REVIEW` when it covers 208,859 / 208,886 TEST rows.

---

## 4. Novelty / Research Gap

### Positioning in the manuscript

- **Prior work already does (as cited):** statistical credit scoring [1]; algorithm benchmarks [2], [3]; P2P / Lending Club risk and SHAP granting models [5], [6]; SME Shapley-style credit explanations [7]; GAM / EBM / additive SHAP / TreeSHAP literature [9]–[13]; Platt / isotonic / ECE [14]–[17]; XGBoost [18]; fairness (cited, not executed) [8]; US adverse-action texts [32]–[34]; named SBP/SECP/AAOIFI/IFSB instruments [24]–[31].
- **Stated gap:** recorded sources do not contain a verified end-to-end study that, **on this hashed Zenodo extract**, (i) keeps scores, additive explanations, and Shariah-oriented evidence objects separate, (ii) fuses them only at a frozen map, and (iii) reports UCI methodology without treating UCI as architecture or Shariah validation.
- **Specificity:** the gap sentence is **specific** (extract + three numbered conditions), then immediately narrowed: “gap relative to the recorded literature sources, not a claim of absolute historical novelty.” “This paper does not call the architecture ‘novel.’”

### Unsupported “first” / “novel” / “unique”

**None found** as author claims. “State-of-the-art” appears only inside **other papers’ titles** ([2], [3]). “Superior” appears only in **denials**.

### Where contribution is clear

Section III’s five bullets plus the “not contributions” paragraph. Abstract and conclusion repeat prototype / non-certification / exploratory XGBoost.

### Where the gap is weakly demonstrated (reviewer-likely questions)

1. Related scholarly set is **1997–2022** by package lock; the paper **discloses** that no 2023–2026 systematic ML-credit review was locked. A reviewer can still treat the gap as **under-compared** to later explainable-credit or Islamic-fintech work **without this audit searching that literature**.
2. Distinguishing “this hashed extract” from other Lending Club papers [5], [6] is a **dataset-identity** gap, not a methods gap. A reviewer may ask what is scientifically new besides extract hashing and the G0 matrix.
3. Shariah-oriented contribution, empirically, is **non-application** of contract rules because fields are absent. That is a valid negative result if framed as such; it is a weak demonstration of a **functioning** Shariah-oriented pipeline.
4. Design-question language (“independently validated and auditable,” “more transparent and defensible digital-financing pipeline”) is **stronger** than Section III’s bounded bullets. Discussion later walks it back (only partially addressable). Reviewers often quote the question, not the walk-back.

**Incremental character (exact reason):** the predictive and explanation pieces are standard glass-box + post-hoc calibration practice; the distinctive integration is a governance firewall and fusion table applied to data that **cannot populate** the governance evidence the paper’s own sources say Islamic-banking contracts require. Incremental is therefore **expected**, not a hidden defect—provided the paper is read as a prototype/evidence-gap study.

---

## 5. Methodology Audit

A technically competent reviewer **can** reconstruct the executed design from Section IV–V plus tables, with repository artifacts needed for bit-level hashes and full local SHAP cases.

| Topic | Manuscript clarity | Reviewer residual |
| --- | --- | --- |
| Executed datasets | LC primary; UCI independent methodology; German/Australian **not** executed (Table I + prose) | Clear |
| Dataset roles | Table I roles; UCI “does not implement the Shariah governance layer” | Clear |
| TRAIN/VAL/TEST | LC temporal `issue_month`; UCI stratified 70/15/15 seed 42; n given | Clear |
| Model identities | Unnumbered context table: M-4B / M-5 / M-9.4-AE / M-9.4-X | Dual LC EBM is honest and cognitively heavy |
| Provenance | Joblib paths; M-5 SHA-256 recorded; M-4B final EBM SHA-256 **not recorded** (stated) | Reproducibility limit, disclosed |
| Calibration | VAL-only Platt/isotonic; TEST reporting; \(a,b\); \(C=\infty\); 10-bin ECE | Reconstructable without reliability plots |
| Thresholds | VAL researcher cost FN:FP=5:1, \(C_{\mathrm{REVIEW}}=0.25 C_{\mathrm{FP}}\); no new grid at fusion | Reconstructable |
| Evaluation | TEST reporting-only after freeze; bootstrap CIs not used for tuning | Clear |
| Explainability | Eq. (1); TreeSHAP not used; n=5000 TEST sample | Identity vs “SHAP study” must be read carefully |
| Decision policy | G0 = TABLE 9; A0/A1/A3 definitions | Clear |
| Exploratory vs primary | Protocol table + UCI subsection labels | Dense; class B/C jargon is repository-specific |

### Context non-merge (verified in IEEE source and PDF)

| ID | Role in paper | Silently merged? |
| --- | --- | --- |
| **M-4B** | LC families after TRAIN+VALIDATION refit; TEST family metrics; **not** used for LC decisions | **No.** Table II / Table III. LC XGBoost labeled “(LC only).” |
| **M-5** | TRAIN-only EBM + VAL Platt; `p_selected`; decisions/explanations | **No.** Table II / Table IV. |
| **M-9.4-AE** | UCI LR and EBM; independent methodology | **No.** Table VII context column. |
| **M-9.4-X** | UCI XGBoost; `DEVIATION-001` exploratory | **No.** ECE `0.20065704943022225` tied to this row only. |

### Other methodology checks

- LendingClub and UCI are the executed datasets; German/Australian literature-only: **holds**.
- Stage 5 Platt TEST metrics are not labeled as Stage 4B EBM metrics: **holds** (Table II gap = EXPLAINED, different fits).
- Validation-only fitting language: **holds** for calibrators and thresholds.
- TEST not used as calibration/tuning set: **stated and consistent** with stored protocol.
- Exploratory UCI XGBoost remains exploratory and tied to `DEVIATION-001`: **holds** in abstract, methods, Table VII, discussion, conclusion.

**Reviewer methodology questions that are fair, not errors:**

1. Why fuse the TRAIN-only M-5 EBM rather than the M-4B TRAIN+VAL EBM that has slightly higher TEST ROC-AUC (`0.6799408767429772` vs `0.6776693941139847`)? The paper answers: protocol freeze / different fit / do not swap joblibs. A reviewer may still want a one-sentence **design justification** (leakage-safe downstream preprocessor) made even louder.
2. Why select EBM on validation when LC XGBoost TEST ROC-AUC is `0.6854404067747387`? The paper answers: validation PR-AUC + Brier/simplicity; TEST not used to choose. Methodologically correct; still a likely question.
3. “Independently validated” layers: credit TEST reporting is freeze-backed; explainability is descriptive of one model; governance is a prototype without expert validation. The adjective in the design question is **stronger** than the protocol table.

---

## 6. Results and Evidence Audit

Values below are **transcribed as published**; they were **not** recalculated. Support types use the required vocabulary.

### Frozen keys

| Key | Manuscript / PDF | Support type |
| --- | --- | --- |
| M-4B EBM TEST ROC-AUC | `0.6799408767429772` | **derived from stored artifact** (`results/metrics/stage4b_test_metrics.json`; Table III) |
| M-5 raw/Platt TEST ROC-AUC | `0.6776693941139847` | **derived from stored artifact** (`stage5_test_metrics.json`; Table II, Table IV(b)) |
| UCI XGBoost raw ECE | `0.20065704943022225` | **derived from stored artifact** (selected-family raw row; Table VII note; M-9.4-X only) |
| TEST n | `208886` / `208,886` | **direct result** of Stage 3 split; repeated in abstract, Table I, Table II, results |
| \(t_{\mathrm{low}} / t_{\mathrm{high}} / t^{*}\) | `0.06` / `0.69` / `0.16` | **policy simulation** identified on validation (Stage 8 v1); reused frozen |

### Major claims

**CLAIM.** Research prototype separates scoring, additive explanation, and Shariah-oriented governance evidence; fusion only at a frozen map.  
**EVIDENCE SUPPORT.** Architecture prose, Fig. 1 text schematic, TABLE 9, Table VI.  
**SUPPORT TYPE:** **direct result** (implemented objects) + **policy simulation** (map).  
Not stronger than evidence if read as a prototype.

**CLAIM.** Not Shariah certification / fatwa / automated compliance / `EXPERT_VALIDATED` / production engine; no fraud performance.  
**EVIDENCE SUPPORT.** Repeated abstract/methods/conclusion; no fraud experiment.  
**SUPPORT TYPE:** **direct result** (negative / scope).  
Aligned.

**CLAIM.** M-5 TEST ROC-AUC `0.6776693941139847`; Platt Brier `0.15616920271522994`; Platt ECE `0.020267295489117824`; TEST not used to fit calibration.  
**EVIDENCE SUPPORT.** Table IV(b); Stage 5 report.  
**SUPPORT TYPE:** **derived from stored artifact**.  
Aligned. “Calibration improves discrimination” is **not** claimed (ROC-AUC equal raw/Platt).

**CLAIM.** Platt TEST Brier/ECE lower than raw (paired differences given).  
**EVIDENCE SUPPORT.** Stored paired differences and CIs; paper says **not** hypothesis-test \(p\)-values.  
**SUPPORT TYPE:** **derived from stored artifact** + **interpretation** (probability-mapping outcome).  
Not overstated if the “not a hypothesis test” clause is kept.

**CLAIM.** 2018 Platt ECE `0.06152417312325683` vs 2017 `0.005096425775164428`; temporal transfer failure; calibrator not recoded.  
**EVIDENCE SUPPORT.** Descriptive slices.  
**SUPPORT TYPE:** **interpretation** of stored slices (paper labels non-confirmatory).  
Aligned with limitations.

**CLAIM.** Explanations are exact additive SHAP-style logit decomposition of the M-5 EBM; TreeSHAP not used; top attributions `fico_n`, `loan_amnt`.  
**EVIDENCE SUPPORT.** Eq. (1); Table V; agreement = 1.0.  
**SUPPORT TYPE:** **direct result** of the identity method.  
**Risk of appearing stronger:** a reader skimming “SHAP” may think a second explainer confirmed the ranking. Surrounding text blocks that reading.

**CLAIM.** LC L1 `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`; all 208,886 TEST rows `INSUFFICIENT_INFORMATION`; not a compliance verdict.  
**EVIDENCE SUPPORT.** Methods + Table XI (only that L2 status populated).  
**SUPPORT TYPE:** **direct result** of predicates on this extract.  
Aligned.

**CLAIM.** A0 5232 / 203627 / 27; A1 0 / 208859 / 27; A3/A4 61855 / 0 / 147031; scores identical across maps; not production origination.  
**EVIDENCE SUPPORT.** Table VI.  
**SUPPORT TYPE:** **policy simulation** on stored `p_selected`.  
Aligned. A1’s 0 APPROVE is **algebraically implied** by Table XI + TABLE 9 (all rows `INSUFFICIENT_INFORMATION` × G0). That is evidence of the **matrix plus schema gap**, not of Shariah screening quality.

**CLAIM.** UCI LR/EBM are methodology context; UCI XGBoost exploratory; not LC architecture/Shariah validation.  
**EVIDENCE SUPPORT.** Table VII; discussion.  
**SUPPORT TYPE:** **direct result** (UCI metrics) + **interpretation** (non-comparability).  
Aligned. Exploratory selected UCI pipeline (XGBoost+isotonic) metrics are reported in prose with the exploratory class; they are easy to **misread as a second main result** if a reader skips labels.

**CLAIM (design question).** Layers independently validated; more transparent/defensible than monolithic; without materially sacrificing predictive performance.  
**EVIDENCE SUPPORT.** Discussion: only **partially** addressable; no governance-induced AUC change (scores identical); operational Islamic-finance defensibility **not shown**.  
**SUPPORT TYPE:** **insufficiently supported** as an answered empirical question; **supported** as a stated design question with an explicit non-proof.  
This is the principal **claim > result** tension.

**CLAIM.** Family selection used validation, not TEST; EBM selected.  
**EVIDENCE SUPPORT.** Mean val PR-AUC 0.388473 best; EBM 0.385841 within 0.005; Brier/simplicity.  
**SUPPORT TYPE:** **derived from stored artifact** (Stage 4B report).  
Aligned. TEST XGBoost AUC higher is reported and **not** used to overturn selection.

---

## 7. Table-by-Table Review

### Unnumbered tabulars

| Location | Question it supports | Interpretable? | Caption | Placement | Text match | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| §IV opening (PDF p. 4) | Keep four model contexts unmerged | Yes if read slowly; cramped after `\resizebox` | None (unnumbered) | Methods | Yes | Reviewer may treat it as “Table 0.” Not redundant. |
| §IV-I (PDF p. 7) | What was implemented vs identity-only standards | Yes | None | Methods | Yes | Complements TABLE 9; not a metric table. |
| §V (PDF p. 8) | Freeze vs exploratory classes | Dense | None | Before results | Yes | Repository jargon (class B/C) may be opaque to an Access reviewer. |

### Numbered tables

**TABLE 1 — Executed datasets.**  
Supports dataset identity, n, hashes, roles, Shariah-field absence. Interpretable. Caption adequate. Placement: methods (PDF p. 6), after UCI subsection (float delay). Surrounding text matches. Not redundant. Misread risk: treating UCI as a second full-architecture test—caption and “Independent” cell resist that.

**TABLE 2 — Two LendingClub EBMs.**  
Supports M-4B vs M-5 non-collapse; ROC-AUC `0.6799408767429772` vs `0.6776693941139847`. Interpretable. Caption strong (“must not be collapsed”). Results §VI-A (PDF p. 9). Essential. Misread risk: averaging the two AUCs—table forbids it.

**TABLE 3 — M-4B TEST families.**  
Supports family comparison after TRAIN+VAL refit. Interpretable. Caption adequate. Adjacent to Table II. Surrounding text correctly says these are **not** downstream decision scores and flags LC XGBoost ≠ M-9.4-X. Misread risk: calling XGBoost “the model.”

**TABLE 4 — M-5 calibration (a) VAL (b) TEST.**  
Supports calibrator selection and TEST reporting. Interpretable though **scriptsize**. Caption states VAL-only fit. Text correctly notes Platt ROC-AUC = raw. **No reliability plot**; numbers still reconstructable. Misread risk: reading isotonic VAL ECE \(\approx 0\) as TEST ECE (panels are separate).

**TABLE 5 — Global mean |attribution|.**  
Supports ranking on 5,000-row sample. Interpretable. Caption states sample size and logit scale. Text states identity. Misread risk: causal ranking of default drivers—text forbids it. `revenue` shap vs ebm last-digit difference (`…624` vs `…6237`) is stored-precision, not a second method.

**TABLE 6 — TEST decision counts.**  
Supports A0/A1/A3 policy simulation. Interpretable. Caption: frozen `p_selected`. Text: not winner ranking; not origination. Central empirical table for the fusion claim.

**TABLE 7 — UCI family-raw + exploratory ECE cell.**  
Supports M-9.4-AE vs M-9.4-X. Caption warns family-raw has no ECE column. Interpretable if the ECE note is read. Misread risk: **highest** among the three AUCs as “best model”; paper blocks superiority language. LR/EBM ECE “not stored” is disciplined.

**TABLE 8 — Credit-band default rates.**  
Supports LOW/MED/HIGH outcome rates on frozen scores. Interpretable; HIGH n=27 called out. Complements Table VI. Not redundant.

**TABLE 9 — G0 fusion matrix.**  
Supports reconstructability of A1. Interpretable. Caption adequate (not a Shariah ruling). **Placement:** methods p. 7, **before** Tables 2–8 in reading order. Narrative support is good; **numbering vs reading order** is a reviewer friction. Not scientifically redundant with Table XI (matrix vs observed counts).

**TABLE 10 — Year mix.**  
Supports post-hoc 2017/2018 assignment mix. Caption: not confirmatory. Interpretable. Could look like a robustness experiment if caption is skipped. Not required to prove the main fusion claim.

**TABLE 11 — L2 × credit band.**  
Supports why A1 has 0 APPROVE. Interpretable. Caption: not a Shariah ruling. Makes Table VI’s A1 row **non-mysterious**. Slight overlap with Table VI+TABLE 9 algebra; still useful.

**Important conclusion lacking a table?** No stored headline metric lacks a table. Missing **visual** calibration/shape displays are not missing tables.

**Redundant?** Table X is the weakest for the core argument (post-hoc). Not scientifically false. Table XI and TABLE 9 overlap logically; they answer different questions (definition vs observation).

---

## 8. Figures and Equations Audit

### Inventory (actual)

| Kind | Count | What it is |
| --- | --- | --- |
| Substantive raster figures | **0** | No `\includegraphics`; no ROC/PR/reliability/shape PNG |
| Named IEEE figures | **1** | FIGURE 1 = four-row text schematic (a table labeled as a figure) |
| Numbered equations | **1** | Additive SHAP-style identity (1) |
| Inline essential math | Several | Platt map; \(a,b\); \(C=\infty\); \(t_{\mathrm{low}},t_{\mathrm{high}},t^{*}\); credit-band inequalities |

**There are NO substantive (image) figures.**  
**There is NO multi-equation formal model of the fusion pipeline** beyond Eq. (1) plus TABLE 9.

### Missing figure/equation that blocks understanding?

| Candidate omission | Blocks methodology / reconstruction? | Classification |
| --- | --- | --- |
| Process flowchart (instead of Fig. 1 text) | **No.** Layers and G0 are in text + TABLE 9. | **ACCEPTABLE_AS_IS** |
| Fig. 2 G0 image | **No.** Intentionally TABLE 9. | **ACCEPTABLE_AS_IS** |
| Reliability diagrams (named in Stage 5 report; files not retained) | **No** for reconstructing Brier/ECE **numbers**. **Yes** as an interpretive aid for 2018 ECE deterioration and bin-wise miscalibration. Paper discloses omission and does not regenerate. | Not a formal-definition hole. See §17 |
| EBM shape-function plots | **No** for reconstructing Eq. (1) or Table V. Weakens **explainability contribution** visually. | **ACCEPTABLE_AS_IS** as omission-for-appearance; not recommended here as a required add |
| Numbered Platt equation | **No.** Inline form is complete. | **ACCEPTABLE_AS_IS** |
| Numbered G0 equations | **No.** Matrix is the actual object. | **ACCEPTABLE_AS_IS** |

**Does figure/equation scarcity create an actual scientific weakness?**  
It creates a **presentation / reviewer-expectation** weakness for an Access paper that is otherwise table-dense, **not** an inability to follow the experimental workflow or reconstruct the decision policy. Classification of the absence overall: **ACCEPTABLE_AS_IS** for scientific reconstruction.

This audit does **not** recommend adding decorative figures or equations.

---

## 9. Shariah / Governance Claim Audit

Checks against IEEE source and PDF:

| Required discipline | Status |
| --- | --- |
| Avoids certification claims | **Yes.** Abstract, §IV-I, conclusion. |
| Avoids religious authority / fatwa / replacing a Shariah Board | **Yes.** |
| Avoids claiming LC contains contract-level Shariah data | **Yes.** Table I; “none sufficient”; invoices/possession absent. |
| Avoids claiming UCI validates Shariah compliance | **Yes.** Governance layer not applied on UCI. |
| Distinguishes researcher assumptions from rulings | **Yes** for costs and G0 as research map. `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW` in the treatment tabular. |
| Distinguishes governance alignment from formal compliance | **Yes.** Evidence-gap / not applicant non-compliance. |
| Avoids overstating standards | **Mostly yes.** AAOIFI identity only; years UNVERIFIED; IFSB-10 FAQ not full-body parse; SECP used as **prohibition** of certification language; SBP 2012 circular “not a rule for the executed LendingClub extract.” |

### Sentences a skeptical reviewer **could** still misread as compliance/certification-adjacent

These are **not** rewritten here. None is a clean certification claim; each is a **misread risk**.

1. **Title / keywords:** “Shariah-Oriented Governance” on a US P2P extract. A skimming reviewer may expect Islamic-contract data. The abstract immediately denies certification and states the extract is not an Islamic-finance sample.
2. **Design question (PDF p. 2):** “independently validated and auditable evidence layers” including “Shariah-oriented governance.” “Validated” can be heard as religious/legal validation. Immediate following sentence: design question, not operational superiority.
3. **§IV-A:** “research prototype for Shariah-oriented governance and evidence traceability. It is decision-support / evidence-gap handling.” “Decision-support” plus Shariah-oriented may be over-read as usable IBI tooling. Follow-on: does not replace a Shariah Board.
4. **Discussion:** “The governance layer refused to convert missing contract evidence into PASS or into a religious non-compliance label.” Accurate; a hostile reading is anthropomorphic “governance layer” as an authority. Context blocks certification.

No sentence was found that states loans, applicants, or the software are Shariah-compliant or certified.

---

## 10. Decision-Policy Audit

| Check | Finding |
| --- | --- |
| \(t_{\mathrm{low}}=0.06\), \(t_{\mathrm{high}}=0.69\), \(t^{*}=0.16\) | Consistent in methods, discussion, limitations item 25, PDF p. 7. |
| Cost assumptions labeled assumptions | **Yes.** “researcher cost scenario, not operational cost”; FN:FP = 5:1 stated. |
| HUMAN_REVIEW simulated / research policy | **Yes.** “policy analyses on frozen `p_selected`, not real-world approval performance”; Stage 8 v1 (repository) called the review band simulated; paper: “Human review is not certification.” |
| APPROVE/REJECT not real origination | **Yes** in conclusion and Table VI context. |
| Not deployed / production-tested | **Yes.** Prototype; production/real-time/ECOA not evidenced. |
| Threshold derivation consistent | VAL identification, no new grid at fusion; TEST used for counts only. |

### Wording that could look like real-world validation

1. **Abstract:** “Frozen-score research maps **assign** … approve / human-review / reject **decisions**.” “Decisions” without “research-map” in that clause can sound operational. Same sentence says “research maps” and later “predictive scores are identical.”
2. **Conclusion:** “Research policy maps … change APPROVE / **REVIEW** / REJECT counts.” Uses **REVIEW** rather than `HUMAN_REVIEW`. Not a scientific change; slight label slip versus Table VI.
3. **A0 still “APPROVE assignments”** (discussion): correctly “assignments,” but large integer counts look like a portfolio outcome. Table VI’s approval-rate column and “not ranked as winner” mitigate.

HIGH band n=27 is disclosed (Table VIII). A reviewer may still say the two-threshold HIGH reject rule is empirically fragile.

---

## 11. Explainability Audit

| Check | Finding |
| --- | --- |
| Additive EBM language | **Correct:** `interactions=0`; logit / `decision_function`; Eq. (1); Platt not inside the explanation. |
| TreeSHAP | **Not claimed as used.** Cited as inappropriate for a first-order GAM. |
| Corresponds to actual model | Paper follows **M-5** TRAIN-only EBM metadata (`ebm_train_only_seed42.joblib`). |
| Silent wrong-model attribution | **No** in the manuscript. |
| Stage 6 opening-sentence provenance | **Documented** in §IV-H (PDF p. 7): historical report says “frozen Stage 4B model”; paper follows TRAIN-only metadata; historical files not rewritten. Same limitation #20. |

**Contribution weight:** Table V + identity error \(8.88\times10^{-16}\) is internally consistent and **scientifically modest**. A reviewer can call this “centered EBM terms, not a SHAP experiment.” The manuscript already says that.

---

## 12. Limitations Audit

Section VIII lists 27 executed-evidence limitations (git null; M-4B joblib hash; positional fusion identity; pytest lock; degenerate UCI XGBoost seeds; `DEVIATION-001`; class B/C; AAOIFI; no expert validation; selection bias; target mismatch; 2018 ECE; n=5000 explanations; HIGH n=27; missing ECE stores; zip one-hot; Stage 6 wording; schema gap; literature-package holes; fairness; fraud; researcher thresholds; omitted reliability images; German/Australian; non-confirmatory year-mix).

**Strength relative to evidence:** unusually explicit. Matches the inventory’s prohibited-claim list.

| Theme | Covered? |
| --- | --- |
| External validity | Yes (US P2P originated-and-resolved; not Islamic-finance sample) |
| Representativeness / selection bias | Yes (rejects absent) |
| Temporal generalization | Yes (2018 ECE; year-mix non-confirmatory) |
| Class imbalance **by name** | **Not named.** Prevalence (~21% TEST) and PR-AUC are reported. Absence is minor given those metrics; not a silently dropped scientific fact |
| Calibration | Yes (2018; no nested TRAIN calibrator; diagrams omitted) |
| Policy assumptions | Yes (item 25) |
| Exploratory analysis | Yes (items 5–8, 27) |
| Shariah data | Yes (item 21) |
| No real-world deployment | Yes (discussion + production/ECOA sentence) |
| No real origination outcomes | Yes (conclusion; Table VI framing) |
| Institutional/legal/regulatory scope | Yes (SECP/SBP/IFSB identity limits; not ECOA originator) |

**Clearly missing only if absence materially weakens interpretation:**

- **Human-review cost/capacity:** `HUMAN_REVIEW` ≈ 99.99% of TEST under A1. Limitations state thresholds are researcher-scenario costs and that review is not certification, but they do **not** spell out that a review band this large is **operationally vacuous** as an automated pipeline. Discussion already implies this via 0 APPROVE. Not a fabricated limitation; a **clarity** gap. See §17.
- **Class imbalance named:** not material given PR-AUC reporting.
- Do **not** invent unexecuted fairness, deployment, or AAOIFI-clause results as extra limitations.

The sentence “None of the scientifically necessary limitations is silently dropped” is **authorial**. This review agrees that the **executed** negative results are listed; it does not treat that sentence as proof against reviewer requests for tighter design-question framing.

---

## 13. Reproducibility Audit

**Reproducible from the paper alone (competent reader):**

- Dataset identity (Zenodo DOI, UCI 350), split rules, n, predictor list, exclusions
- Family hyperparameters (seed-42 blocks)
- Platt formula, \(a,b\), selection rule, ECE binning rule
- Eq. (1) explanation method and sample protocol
- G0 matrix and A0/A1/A3 definitions
- All headline TEST metrics as **transcribed values**

**Depends on repository artifacts (not fully in the PDF):**

- Row-level `p_selected` / audit CSV; local SHAP cases
- Joblib binaries; preprocessor
- Exact metric-wrapper notes (`docs/METRIC_DEFINITIONS.md` cited only as “project metric-definition notes”)
- Full Stage 9.2/9.3 exploratory tables (omitted from main text by class)

**Insufficiently specified in the paper (disclosed or residual):**

- M-4B final EBM **SHA-256 not recorded**
- `git_commit` null / no `.git`
- Reliability-diagram files not retained
- Fusion audit `row_ref` missing (positional identity)
- No code URL / artifact DOI for the prototype itself (paper does not claim a public code release)

Absence of a code dump is **not** treated here as a MUST_FIX unless the paper claimed one; it did not. Bit-for-bit reproduction of M-4B EBM is **limited** by the missing joblib hash (already in limitations).

---

## 14. Internal Consistency Audit

Compared: abstract, I–IX, numbered tables, `IEEE_MANUSCRIPT.md` / `MANUSCRIPT_DRAFT.md` scientific keys, evidence map, `FINAL_CROSS_STAGE_CONSISTENCY_AUDIT.md`.

| Item | Consistent? |
| --- | --- |
| Dataset names / executed vs literature-only | **Yes** |
| Model context IDs | **Yes** |
| M-4B / M-5 / UCI XGB ECE / TEST n / thresholds | **Yes** across abstract, tables, discussion, conclusion |
| Calibration VAL-only | **Yes** |
| Exploratory XGBoost / `DEVIATION-001` | **Yes** |
| Shariah non-certification | **Yes** |
| Policy not origination | **Yes** (conclusion “REVIEW” vs `HUMAN_REVIEW`: **label only**) |
| Fig. 1 referenced and present | **Yes** |
| Eq. (1) referenced and present | **Yes** |

**Non-scientific inconsistencies (do not change metrics):**

- TABLE **number** 9 appears in the PDF **before** TABLE 2.
- `MANUSCRIPT_DRAFT.md` still mentions a Fig. 2 plan; IEEE source/PDF omit Fig. 2 and say so in TABLE 9’s caption.
- `docs/PAPER_EVIDENCE_INVENTORY.md` header still says paper drafting NOT STARTED (file lag; not a manuscript contradiction).
- Author-metadata checklist `C_INFINITY_RENDERING = REVIEW_REQUIRED` is stale vs the review PDF, which shows `C=∞` (format history, not a metric).

No abstract-vs-table metric contradiction found.

---

## 15. Potential Reviewer Red Flags

| # | Location | What a reviewer may question | Evidence for the concern | Severity | Kind | Wording/documentation only? |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | §I design question (PDF p. 2) | Whether the study **answers** “more transparent and defensible … without materially sacrificing predictive performance” | Discussion (PDF p. 10–11) says only partially addressable; A1 has 0 APPROVE; scores identical across maps so “no sacrifice” is **by construction**, not a test of governance vs accuracy | **HIGH** | Interpretive / claim–evidence | **Yes** (framing). Not a stored-metric error. |
| 2 | Same quote: “independently validated … Shariah-oriented governance” | Whether governance was validated in a religious/legal sense | No `EXPERT_VALIDATED`; schema insufficiency on all TEST rows; paper denies certification | **HIGH** | Interpretive | **Yes** |
| 3 | Title + Table VI A1 | Whether a “Shariah-oriented” pipeline is demonstrated or only an evidence-gap | Table XI: only `INSUFFICIENT_INFORMATION`; TABLE 9 maps that to HUMAN_REVIEW/REJECT | **HIGH** | Evidentiary | Partly (framing). Cannot be “fixed” by new Shariah data without new experiments (out of scope here). |
| 4 | Dual EBM (Table II) | Why decisions use the slightly weaker TRAIN-only fit | Protocol freeze; different preprocessor; gap EXPLAINED | **MEDIUM** | Methodological | **Yes** (justification emphasis) |
| 5 | Table III vs selection | Why EBM if LC XGBoost TEST AUC is higher | Selection on validation PR-AUC/Brier/simplicity; TEST not used | **MEDIUM** | Methodological | **Yes** |
| 6 | Related work / §III gap | Gap only vs a 1997–2022 locked package | Paper discloses no 2023–2026 systematic review in the package | **MEDIUM** | Evidentiary / positioning | Documentation only **cannot** add unrecorded citations (this task forbids citation stuffing) |
| 7 | §VI-C / Table V | Explainability = algebraic identity | Paper states Spearman=1 expected | **MEDIUM** | Contribution weight | **Yes** |
| 8 | Omitted reliability diagrams | How to **see** 2018 ECE failure | Limitation 26; Table IV still has ECE | **MEDIUM** | Presentation / interpretive | Regenerating plots would be a **new artifact** (forbidden in this task). Wording already discloses. |
| 9 | TABLE 9 before TABLE 2 | Broken table numbering in reading order | PDF p. 7 vs p. 9; `\setcounter{table}{8}` | **MEDIUM** | Presentation | Format-only (not this task) |
| 10 | FIGURE 1 as a table | “Where are the figures?” | Caption admits text schematic | **LOW** | Presentation | Format-only |
| 11 | Abstract “assign … decisions” | Operational decisions vs research maps | Same abstract: research maps; conclusion: not origination | **LOW** | Interpretive | **Yes** |
| 12 | Conclusion “APPROVE / REVIEW / REJECT” | Inconsistent action name | Table VI uses `HUMAN_REVIEW` | **LOW** | Presentation | **Yes** |
| 13 | Table VII + prose selected UCI pipeline | Exploratory XGBoost+isotonic numbers in main text | Labels `DEVIATION-001` | **MEDIUM** | Interpretive | **Yes** (could be appendix in a future wording pass; not done here) |
| 14 | HIGH n=27 | Unstable REJECT default rate | Table VIII Wilson interval wide; disclosed | **LOW** | Evidentiary | Already disclosed |
| 15 | Placeholder DOI / empty bios (p. 1, p. 13) | Incomplete Access package | Template DOI; empty `IEEEbiographynophoto` | **LOW** for **science**; venue process is separate | Presentation / metadata | Author input required; **do not invent** |

Do not treat red flags 1–3 as metric errors. They are how a skeptical reviewer tests **contribution scale**.

---

## 16. MUST_FIX_BEFORE_SUBMISSION

**None** for scientific interpretation of stored results, model-context identity, dataset role, TEST n, thresholds, calibration identity, TreeSHAP non-use, or Shariah non-certification.

No MUST_FIX item is recorded for stylistic density, full-precision tables, figure scarcity, or IEEE Access biography/email/ORCID completeness. Those last items are **submission-process** blockers already logged in `docs/paper/IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md`; they are not scientific defects in the results.

---

## 17. NEEDS_AUTHOR_JUDGMENT

1. **How loudly to frame the design question** as unanswered / evidence-gap versus architecture demonstration (red flags 1–3). Wording-only; no new experiment required to **clarify**, but clarifying cannot create Islamic-contract fields that the extract lacks.
2. **Whether dual M-4B/M-5 EBM needs still more pedagogical emphasis** for Access readers (red flag 4).
3. **Whether exploratory UCI XGBoost+isotonic selected-pipeline numbers should remain in the main-text paragraph** under Table VII (red flag 13). Moving them would be a presentation/wording decision, not a metric change.
4. **TABLE 9 reading-order vs number** (red flag 9): format-only if ever retouched.
5. **Reliability-diagram omission:** leave disclosed-as-omitted (**current**) vs later restore **stored** images if they still exist outside the repo. This audit must **not** regenerate them from scores.
6. **Author metadata / biographies / corresponding author / emails / ORCID:** required for Access **process**, not for scientific validity. Owner must supply; nothing should be invented.
7. **Optional minor-formatting polish** of cramped tabulars (already diagnosed as NICE_TO_FIX in the layout track). Not scientific.

---

## 18. ACCEPTABLE_AS_IS

- Non-merge of M-4B / M-5 / M-9.4-AE / M-9.4-X
- LendingClub vs UCI roles; German/Australian literature-only
- Validation-only Platt and thresholds; TEST reporting-only
- Transcription of frozen keys listed in §6
- TreeSHAP non-use; Eq. (1); documented Stage 6 provenance note
- Explicit non-certification / non-fatwa / non-origination language
- Table coverage of headline numeric claims
- Absence of raster figures and of extra numbered equations **for reconstructability**
- Omission of Fig. 2 as a duplicate of TABLE 9
- Long limitations list covering executed negative results
- UNVERIFIED literature-package fields left unverified
- Historical Stage 8 “Stage 9 has NOT been started” wording (prior forensic audit: Stage-8-time boundary, not a manuscript contradiction)

---

## 19. Overall Scientific Readiness Notes

Scientifically, the manuscript is **internally disciplined**: it transcribes frozen artifacts, keeps model contexts apart, and repeatedly refuses certification, fraud, production, and XGBoost-superiority claims. A skeptical Access reviewer is less likely to reject it for **hidden metric fraud** than to challenge **whether the integration on a non-Islamic, contract-field-absent extract constitutes a sufficient empirical contribution** relative to the title and design question, and whether additive-identity explanations plus a schema-gap matrix are enough beyond existing EBM/Platt/P2P papers.

Those are **contribution and positioning** questions. They are not resolved by recalculating `0.6776693941139847`. They are not resolved by this audit. No acceptance prediction is offered.

---

```text
EXPERIMENTS_RUN = NONE
METRICS_RECALCULATED = NONE
MODELS_CHANGED = NONE
DATASETS_CHANGED = NONE
RESULTS_CHANGED = NONE
CALIBRATION_CHANGED = NONE
THRESHOLDS_CHANGED = NONE
TEST_REOPENED = NO
STAGE_9_REOPENED = NO
STAGE_10_REOPENED = NO
MANUSCRIPT_MODIFIED = NO
PDF_MODIFIED = NO
SCIENTIFIC_CONTENT_MODIFIED = NO
```

STOP. No other file was modified.
