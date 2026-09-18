# IEEE TEMPLATE CONVERSION AUDIT

| Item | Value |
| --- | --- |
| **Audit ID** | `IEEE-TEMPLATE-CONVERSION-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Type** | Formatting / manuscript-structure derivative only |
| **Scientific research** | **CLOSED** (Stages 2–10 frozen; not reopened) |
| **Master preserved** | `docs/paper/MANUSCRIPT_DRAFT.md` **not overwritten** |
| **IEEE derivative created** | `docs/paper/IEEE_MANUSCRIPT.md` |
| **Experiments / recomputes** | **None** |
| **Stage 2–10 artifacts modified** | **No** |
| **Reliability diagrams** | Still omitted; **not regenerated** |
| **Venue / Word / LaTeX template** | **Not supplied**; this pass is Markdown IEEE-style source, not camera-ready submission |

---

SOURCE_MANUSCRIPT = `docs/paper/MANUSCRIPT_DRAFT.md`

IEEE_DERIVATIVE = `docs/paper/IEEE_MANUSCRIPT.md`

SECTIONS_REMAPPED = YES (heading numbers and wrappers only)

| Master draft | IEEE derivative |
| --- | --- |
| Front-matter metadata table + drafting note | **Removed** |
| ## 1. Title | Unnumbered title line |
| (no author block) | Placeholder author block |
| ## 2. Abstract | **Abstract**— (one paragraph) |
| ## 3. Keywords + Index Terms cross-ref | **Index Terms**— (5 terms from the master keyword list) |
| ### Table and figure plan | **Removed** |
| ## 4. Introduction | **I. Introduction** |
| ## 5. Related Work (5.1–5.7) | **II. Related Work** (A–G) |
| ## 6. Research Gap and Contributions | **III. Research Gap and Contributions** |
| ## 7. Methodology (7.1–7.10) | **IV. Methodology** (A–J) |
| ## 8. Experimental Protocol | **V. Experimental Protocol** |
| ## 9. Results (9.1–9.6) | **VI. Results** (A–F) |
| ## 10. Discussion | **VII. Discussion** |
| ## 11. Limitations | **VIII. Limitations** |
| ## 12. Conclusion | **IX. Conclusion** |
| ## 13. References [1]–[34] | **References** [1]–[34] (same source identities) |
| ## Drafting close | **Removed** |
| Acknowledgments | **Omitted** (none supplied; not invented) |

No Stage 11 section was created.

METADATA_REMOVED = YES

Removed from the IEEE derivative (retained in the master / audit repository):

- Document-ID metadata table (`MANUSCRIPT-DRAFT-V1`, date, type, evidence freeze, paired map)
- Drafting-priority prose about IEEE-style draft status
- Title-section duplicate heading and “does not describe…” drafting note
- Keywords drafting note (“deliberately omit…”)
- Table and figure plan
- Roadmap pointing to master Arabic section numbers 5–13
- “Stage 9 remains CLOSED / Stage 10 remains CLOSED / does not start Stage 11” protocol banner
- Protocol documentation-lag paragraph (leftover DRAFT header, 9.4 report-hash caveat, constitution leftover, `SHARIAH_GOVERNANCE_SCOPE.md` lag)
- Results source-path scaffolding where the scientific numeral and model context were already stated
- S10-I1 “PASS WITH DOCUMENTATION LIMITATION” status string
- Native activity codes as section titles (S10-I1/R1/A1/A4 kept as descriptive analyses, not as PASS/CLOSED banners)
- Reference-register unused-source note (`SRC-AAOIFI-SS-INDEX`)
- Drafting-close machine-readable block (`DRAFT_STATUS`, `SECTIONS_COMPLETED`, etc.)
- Repository-only limitations 20, 22, 23, 29 of the master (documentation-lag / constitution leftover). Scientific counterparts were preserved (git provenance, pytest lock limitation, ECE not stored, reliability diagrams omitted, UCI XGBoost exploratory, Stage 6 provenance wording, Shariah schema gap, bibliographic metadata gaps, German/Australian literature-only, descriptive Stage 10).

TABLE_ORDER_CORRECTED = YES

- Results now present **Table II then Table III** (master presented III then II).
- Results now present **Table VII then Table VIII**, with an explicit return sentence to the LendingClub test set (master presented VIII then VII).
- Table **identities and cells are unchanged**.
- First numbered table in the IEEE file is **Table I** (executed datasets).
- Table IX (G0) remains in Methodology after Table I, matching the master evidence-map identity. It is **not** first-cited in Section IV-A; the architecture subsection points to Section IV-J instead of forwarding Table IX before Table I.
- Global sequence of table **bodies**: I → IX → II → III → IV → V → VI → VII → VIII → X → XI. Numbers were **not** reassigned, so that Table II remains the two-EBM identity table and Table III remains the M-4B family TEST table.

FIGURE_ORDER_CORRECTED = YES

- **Fig. 1** retained as the existing text schematic (no PNG/PDF created).
- Reliability-diagram files remain omitted (not regenerated; not described as present).
- No Fig. 3+ invented.

FIGURE_2_TABLE_IX_HANDLING = RETAIN_TABLE_IX_DROP_DUPLICATE_FIG_2 (presentation-only)

- Master Fig. 2 was a captioned copy of the same G0 matrix as Table IX.
- IEEE derivative **retains Table IX** as the exact numerical / categorical G0 representation.
- IEEE derivative **does not number a Fig. 2**. Caption of Table IX states that the same matrix is not repeated as a separate figure.
- **No G0 cell was modified.** This is a presentation-efficiency decision, not a scientific result.

TABLE_IV_PANEL_HANDLING = LABELED_PANELS_A_VALIDATION_B_TEST

- One caption: M-5 calibration metrics (TRAIN-only EBM; calibrators fit on validation only).
- **(a)** Validation.
- **(b)** TEST (reporting only).
- Original values, method rows (raw / Platt selected / isotonic not selected), and M-5-only context preserved.
- Panels are not presented as a cross-model comparison.

EQUATION_HANDLING = EXISTING_SHAP_IDENTITY_NUMBERED_AS_1; PLATT_LEFT_INLINE

- The additive centered-term identity already in the master (`phi_i = g_i - mean_TRAIN g_i`) is formatted as display equation **(1)** with variables defined in the following sentence.
- Platt map remains inline, as in the master.
- No new equations. No formulas changed. No mathematical results calculated.

REFERENCE_HANDLING = MASTER_IDENTITIES_[1]–[34]_PRESERVED

- Source-to-number mapping is **identical** to the master / literature register.
- No DOI, author, publisher, URL, or year was invented.
- Unverified metadata remain marked (Platt [14]; Zenodo creators [20]; AAOIFI years [28], [29]; IFSB-10 FAQ-not-full-body [31]; Guo [17] DOI NONE).
- Unused register entry `SRC-AAOIFI-SS-INDEX` remains unused (not added).
- In-text `[1]`–`[34]` each exist in References; every reference `[1]`–`[34]` is cited; no duplicate numbers for the same source.
- First-appearance order in the IEEE file is **not** sequential (`[20]` appears before `[7]`, etc.), matching the master numbering. Strict IEEE first-cite renumbering was **not** applied, to avoid changing which source supports which claim. A mapping remains available at template placement if the venue requires it; it must be applied as a pure permutation of existing numbers, not as new literature.

AUTHOR_BLOCK_STATUS = PLACEHOLDER_REQUIRED

- No verified author, affiliation, city, country, email, or ORCID exists in the master.
- IEEE block uses explicit placeholders only: `[AUTHOR INFORMATION TO BE PROVIDED]`.
- Affiliation was **not** inferred from repository metadata.

ABSTRACT_WORD_COUNT = 250

- One paragraph; no citations; no equations.
- ROC-AUC and ECE expanded on first abstract use; EBM expanded.
- Shortening relative to the master removed repetition and drafting/Stage scaffolding only.
- Preserved: research question/design object; LendingClub granting-model extract and split sizes; M-4B vs M-5; stored TEST ROC-AUC / Brier / ECE; SHAP vs TreeSHAP; Shariah governance boundary (`INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`, `INSUFFICIENT_INFORMATION`); map counts; identical scores across maps; UCI LR/EBM methodology context and exploratory UCI XGBoost.
- Not marketing language. Not a fraud-detection or production-performance abstract.

SCIENTIFIC_CONTENT_CHANGED = NO

NEW_EXPERIMENTS = NO

NEW_METRICS = NO

NEW_MODELS = NO

NEW_DATA = NO

TEST_REOPENED = NO

STAGE_2_TO_10_RESULTS_CHANGED = NO

---

## Model-context labels (preserved)

| Context | IEEE treatment |
| --- | --- |
| **M-4B** | TRAIN+VALIDATION EBM (and LC family) TEST after freeze; not used from fusion onward |
| **M-5** | TRAIN-only EBM + validation-only Platt; `p_selected` lineage for later maps |
| **M-9.4-AE** | UCI logistic regression + EBM; independent methodology |
| **M-9.4-X** | UCI XGBoost; `DEVIATION-001`; exploratory only |

LendingClub XGBoost (M-4B) and UCI XGBoost (M-9.4-X) remain unmerged.

## Shariah / Islamic-finance language (preserved, not strengthened)

Retained: research prototype; Shariah-oriented governance; evidence traceability; `INSUFFICIENT_INFORMATION`; evidence/schema gap; not certification / fatwa / automated compliance verdict / `EXPERT_VALIDATED`.

Not introduced: Shariah certified; fatwa approved; Islamic-compliant applicant; legally compliant Islamic lending.

SECP “shall not be called Shariah compliant unless a Commission certificate is granted” remains a **prohibition** citation, not a claim about this prototype.

## Limitations retained (scientifically necessary)

Reliability-diagram image files not retained; M-4B ECE not stored; UCI LR/EBM family-raw ECE not stored; bibliographic metadata limitations; explainability-report vs TRAIN-only metadata (Stage 6 provenance wording); absence of contract-level Shariah fields in LendingClub; German/Australian literature/context only; exploratory UCI XGBoost; descriptive/non-confirmatory year-mix and evidence-gap analyses; git/`git_commit` null; pytest summaries do not lock every historical TEST point estimate.

## Index terms used (from master keywords; 5 terms)

credit risk; explainable boosting machine; probability calibration; Shariah-oriented governance; evidence traceability.

Not used: fraud detection; real-time loan approval.

## Verification notes

- Key stored numerals sampled present in the IEEE file (M-4B/M-5 ROC-AUC, Platt Brier/ECE, family TEST metrics, UCI family-raw and exploratory selected metrics, SHAP `fico_n`, reconstruction error, hashes, Platt \(a,b\), thresholds, A0/A1/A3 counts).
- Master `docs/paper/MANUSCRIPT_DRAFT.md` still contains its metadata table and drafting-close block.
- IEEE file contains no `DRAFT_STATUS`, no figure-plan block, no Fig. 2.

FINAL_CONVERSION_STATUS = READY_FOR_IEEE_TEMPLATE_PLACEMENT

This is **not** camera-ready submission. The target IEEE venue, final author information, and actual Word/LaTeX (IEEEtran) template have not been supplied.

REMAINING_USER_INPUTS =

1. Author names, department/institution, city/country, email, ORCID (if any).
2. Acknowledgments / funding text (if any; do not invent).
3. Target IEEE venue and official template (Word or LaTeX).
4. Optional venue-required first-appearance citation renumbering (permutation of existing [1]–[34] only).
5. Optional venue-required redraw of Fig. 1 as a vector graphic **without inventing architecture** (current text schematic is evidence-supported).
6. Reliability diagrams remain omitted unless original image files are recovered (do not regenerate from scores in this paper phase).
