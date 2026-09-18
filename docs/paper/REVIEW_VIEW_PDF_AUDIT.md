# Review-View PDF Audit

Inspection type: visual/presentation only. Scientific content was not edited. Author emails, ORCID, biographies, corresponding-author designation, funding, and acknowledgments were not added. This is not a submission package.

Inspection method: the compiled PDF was opened as 12 page-renders (150 dpi) plus cropped close-ups of collision/clip regions. Frozen numerals and labels were compared to `docs/paper/IEEE_MANUSCRIPT.md`. No source `.tex` was modified.

## 1. Build Information

* PDF path: `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.pdf`
* page count: 12
* compiler: MiKTeX pdfTeX 1.40.28 (`pdflatex`; PDF producer string `MiKTeX pdfTeX-1.40.28`; creation date 17 Sep 2026 07:22). Media box 576.00 × 782.93 pt (IEEE Access trim, not US Letter).
* two-column status: YES. Body pages use a left column (~x 36–286 pt) and a right column (~x 298–540 pt), IEEE Access header/logo, running head `Ul Hassan and Ramzan: Evidence-Separated Credit Scoring and Shariah-Oriented Governance`, `VOLUME 11, 2023` footer from the official class, single-spaced body, abstract and index terms in the Access title block, numbered section headings (`I.` … `IX.`), and a two-column References list.

Title/author block, ABSTRACT, and INDEX TERMS are correctly placed on page 1 in Access style. Template placeholders remain: `Date of publication xxxx 00, 0000`, DOI `10.1109/ACCESS.2024.0429000`, and class footer `VOLUME 11, 2023`. Those are template chrome, not new scientific claims.

## 2. Page-by-Page Visual Review

### Page 1

* layout status: Access title page is two-column below the abstract. Drop-cap introduction is intact. Margins and logo look consistent with the official class.
* tables: none
* figures: none
* equations: none
* obvious visual defects: template date/DOI placeholders (expected). Citation ranges show a small extra space after the en dash (example `[14]– [16]`, `[9]– [11]`). Not a collision.
* otherwise: CLEAN for a title page.

### Page 2

* layout status: balanced two-column related-work continuation. Section `II` and subsection `A`/`B` headings are formatted correctly. No overlapping objects.
* tables: none
* figures: none
* equations: inline \(n = 1000\) / \(n = 690\) readable.
* obvious visual defects: none that collide or clip.
* status: CLEAN

### Page 3

* layout status: two-column, readable. Subsection `G` heading wraps to a second line (`IDENTITY AND SCOPE`). Contribution list item 2 splits at the page break; the heading is not orphaned as a lone line with no following text on the next page, but the sentence is interrupted.
* tables: none
* figures: none
* equations: none
* obvious visual defects: minor heading wrap only.
* status: CLEAN (minor wrap only)

### Page 4

* layout status: NOT CLEAN. The unnumbered model-context tabular in the left column is wider than the column. Its last column (`Used for LC decisions?`) collides with the right-column dataset prose. SHA-256 and filename strings in the right column run through the right margin.
* tables: unnumbered context table is unreadable at the column join (cells overwrite body text: `applicants are absent`, `US P2P 2007–2018`, `not contain contract-level…`).
* figures: none (Fig. 1 has not yet appeared).
* equations: none on this page.
* obvious visual defects: text collision; truncated hashes (`207d65b2…ac0d`, split hashes cut at the margin).
* status: MAJOR visual defects

### Page 5

* layout status: NOT CLEAN. Figure 1 (text schematic table) is a full-width float. Hash lines under the figure overflow from the left column into the right column and collide with the temporal-split paragraph. Typewriter paths (`lendingclub_preprocessor.joblib`, `results/artifacts/fi…`) and hyperparameter tokens (`min_samples_le`, `colsample_bytr`, `max_bins=25`) run out of the right column.
* tables: Fig. 1 table content is mostly readable; the caption is slightly tight at the right edge (`no new nu…` in the overflow detector). Body table of datasets is on the next page.
* figures: FIGURE 1 present as the intended text schematic. No fabricated image. No Fig. 2.
* equations: none.
* obvious visual defects: column collision under Fig. 1; clipped typewriter strings in M-4B hyperparameter bullets.
* status: MAJOR visual defects

### Page 6

* layout status: NOT CLEAN. TABLE 1 is too wide: the UCI column is clipped at the page edge. Long SHA-256 / path strings in the left column overflow into the right column (artifact path collides with the explainability bullets; calibrated-CSV SHA collides with subsection `I`).
* tables: TABLE 1 — UCI cells truncated (`UCI Default of Credit C`, `Independent credit-ris`, `56c885f84457f668`, `0783db42ac57a277`, `Governance layer not ap`). Governance-treatment tabular in the right column is also clipped (`…evaluat`, `…APPLICA`, `…implem`).
* figures: none
* equations: Platt form and \(C=\infty\) render correctly in the left column (confirmed close-up: `C=∞`, solver `lbfgs`, \(a = 1.1988263209549705\), \(b = 0.6697765046966161\)). Equation (1) is present in the right column as \(\phi_i(x)=g_i(x_i)-\operatorname{mean}_{\mathrm{TRAIN}} g_i\); the identity is readable, but neighboring overflowing hashes compete with it.
* obvious visual defects: clipped Table 1; hash/path overflow collisions.
* status: MAJOR visual defects

### Page 7

* layout status: NOT CLEAN. Freeze SHA-256 strings in the left column cross into the right column. The experimental-protocol tabular is wider than one column and overwrites Results §VI-B calibration prose. The right column is not readable through that band.
* tables: protocol table last column (`Authorization class…`) is clipped (`authorizati`, `Shariah findin`, `methodology (M`). The table body is unusable for a reviewer.
* figures: none
* equations: \(t_{\mathrm{low}}=0.06\), \(t_{\mathrm{high}}=0.69\), \(t^{*}=0.16\), FN:FP and \(C_{\mathrm{REVIEW}}\) in §IV-J are readable in the left column above the collision.
* obvious visual defects: the most severe collision in the PDF.
* status: MAJOR visual defects

### Page 8

* layout status: stacked full-width tables occupy most of the page. Remaining two-column text at the bottom is readable. Table numbering on this page is 9, then 2, 3, 4, 5 (float order).
* tables:
  * TABLE 9 (G0 matrix): readable; caption complete; cells not clipped.
  * TABLE 2: M-5 column is clipped at the right edge (`M-5 r`, `TRAI`, `lend`, `resu`, `208,8`, `0.677`, `Yes (p`). A reviewer cannot read the M-5 ROC-AUC or dump path from this table.
  * TABLE 3: family metrics readable (ROC-AUC / PR-AUC / Brier / log loss match the frozen values).
  * TABLE 4 (a)/(b): dense but the numeric grid is present; PR-AUC of panel (a) sits on the right margin.
  * TABLE 5: nine-row attribution table readable.
* figures: none. Fig. 2 still omitted (no replacement graphic).
* equations: continuation of the reconstruction-error sentence \(\,= 8.881784197001252\times 10^{-16}\) is readable at the foot of Table 5.
* obvious visual defects: Table 2 clipped; Table 9 appears before Table 2.
* status: defects present (Table 2 clip + numbering order)

### Page 9

* layout status: two-column, generally readable. TABLE 6 is a full-width float at the top and fits.
* tables: TABLE 6 decision counts readable (`5232 / 203627 / 27`, `0 / 208859 / 27`, `61855 / 0 / 147031`).
* figures: none
* equations: none beyond inline scores.
* obvious visual defects: long path `results/calibration/uci_test_calibration.csv` is tight in the left column but does not collide with the right column in the page render.
* status: CLEAN (with a tight path string)

### Page 10

* layout status: four full-width tables, then two-column discussion/limitations. No body-text collision.
* tables:
  * TABLE 7: family ROC-AUC/PR-AUC/Brier/log loss readable; ECE note on the XGBoost row is clipped (`0.20065704943022225 (selected-fa`). LR/EBM `not stored` cells are visible.
  * TABLE 8: readable (LOW/MEDIUM/HIGH \(n\), default rates, Wilson intervals).
  * TABLE 10: year-mix counts readable.
  * TABLE 11: L2 × band table readable, including the unpopulated-status row.
* figures: none
* equations: none
* obvious visual defects: Table 7 last cell clipped; limitation item 18 splits across the page break (continuation is on page 11).
* status: defects present (Table 7 clip)

### Page 11

* layout status: limitations continue in the left column; conclusion; REFERENCES begin and fill the right column through [22]. Two-column reference formatting is standard Access style.
* tables: none
* figures: none
* equations: none
* obvious visual defects: none in this page render. [21] and [22] are both visible at the bottom of the right column.
* status: CLEAN

### Page 12

* layout status: references [23]–[34] in two columns, then empty biography nameplates. Large lower-page whitespace is the unused `IEEEbiographynophoto` bodies, not a broken column.
* tables: none
* figures: none
* equations: none
* obvious visual defects: empty biographies (metadata, not a typesetting collision). One long CFPB URL in [34] wraps across a line. No invented bio text, email, or ORCID.
* status: CLEAN as a references page; biography slots empty by design

## 3. Tables and Figures

Formatting problems only (no scientific rewrite):

1. **Column overflow / collision (pages 4–7).** Single-column tabulars and SHA-256 / filesystem strings are too wide. They overwrite the adjacent column. The experimental-protocol table on page 7 is the worst case: Results calibration text is not readable through it.
2. **Clipped table cells.** TABLE 1 UCI column, TABLE 2 M-5 column, TABLE 7 XGBoost ECE annotation, and the unnumbered governance-treatment tabular on page 6 are cut at the right margin.
3. **Float numbering order.** Visible captions are TABLE 1, then TABLE 9, TABLE 2–TABLE 8, TABLE 10, TABLE 11. TABLE 9 is the G0 methods matrix (IEEE_MANUSCRIPT TABLE IX) floated onto the results pages ahead of TABLE 2. There is no second copy of any table. Fig. 2 is not present.
4. **Figure 1** is the intended text schematic (a 4-row layer table plus caption). It is not a stored PNG/PDF plot and was not replaced by a fabricated graphic. The caption is present. Hash lines immediately below it collide with the right column.
5. **Arabic vs Roman table numerals.** The Access class prints `TABLE 1` … `TABLE 11` rather than `TABLE I` … `TABLE XI` in `IEEE_MANUSCRIPT.md`. Same objects; class numbering style.
6. **No missing table/figure references in the compiled sense** (previous build QA: no undefined refs). In-text “Table VIII” / “Table VI” / “Fig. 1” still resolve to those objects. A reviewer may still find TABLE 9 appearing before TABLE 2 confusing.

## 4. Equations and Mathematical Rendering

* \(C=\infty\) on page 6 renders as `C=∞` (not the former `C=\{}infty` token). Frozen \(a\) and \(b\) are intact.
* Equation (1) renders as a readable centered identity on the logit / `decision_function` scale. Symbols \(\phi_i\), \(g_i\), and the TRAIN mean are present.
* Thresholds \(t_{\mathrm{low}}=0.06\), \(t_{\mathrm{high}}=0.69\), \(t^{*}=0.16\) are readable on page 7 (left column).
* Table 4 isotonic ECE uses scientific notation \(\times 10^{-17}\) / \(\times 10^{-16}\) and is readable.
* No malformed leftover `\textbackslash` / `infty` token was found in the page renders.
* Equations do not themselves run out of the column; the collisions on pages 4–7 come from tables and SHA strings, not from display math.

## 5. References

* References are visible on pages 11–12.
* Numbering is consecutive `[1]`–`[34]`. No missing number and no duplicate bibliography entry.
* Two-column IEEE Access bibliography formatting is intact (author, title, venue, year, doi/URL notes as already frozen, including Platt 1999 DOI-none wording).
* No broken `[?]` markers.
* Minor presentation: some URLs wrap; citation ranges in the body have a thin extra space after `–`.

## 6. PDF ↔ IEEE Manuscript Consistency

Compared against `docs/paper/IEEE_MANUSCRIPT.md`.

Scientific / numeric identity (spot-checked; all present in the PDF text layer):

* Title, author names, affiliation line, abstract wording, and the five index-term phrases.
* M-5 TEST ROC-AUC `0.6776693941139847`, Platt Brier `0.15616920271522994`, Platt ECE `0.020267295489117824`.
* Platt \(a=1.1988263209549705\), \(b=0.6697765046966161\).
* M-4B TEST EBM ROC-AUC `0.6799408767429772`; LC XGBoost `0.6854404067747387`.
* Decision counts A0 `5232 / 203627 / 27`, A1 `0 / 208859 / 27`, A3/A4 `61855 / 0 / 147031`.
* Thresholds `0.06` / `0.69` / `0.16`.
* UCI exploratory XGBoost raw ECE `0.20065704943022225`; M-9.4-AE ROC-AUC values `0.7572778277972128` and `0.7688563724378406`.
* Artifact hashes `8d373df1…`, `e15ddd2f…`, file SHA `207d65b2…`, TEST hash `4dfedb1a…`.
* `DEVIATION-001`, `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`, `INSUFFICIENT_INFORMATION`.
* One figure (Fig. 1 text schematic); Fig. 2 omitted; references `[1]`–`[34]`.

Presentation-only differences (not new science):

* Index terms are the same five phrases; the PDF prints them in alphabetical Access order (`credit risk, evidence traceability, explainable boosting machine, probability calibration, Shariah-oriented governance`) versus the manuscript file order.
* Table labels are Arabic (`TABLE 1`) rather than Roman (`TABLE I`).
* Some `PAY_*` / `BILL_AMT*` asterisks are hard to see next to underscores in the feature-policy sentence (typewriter rendering), not a changed feature list.
* Clipped table *cells* hide characters from a reviewer; the PDF text layer and the manuscript file still contain the frozen values. This is a layout defect, not a silent metric edit.

No rewritten scientific claims, no changed model names, no changed thresholds, and no dropped or added bibliography items were found.

## 7. Reviewer-View Presentation Quality

The first page, related-work pages, later discussion/limitations, and the reference list visually resemble a serious IEEE Access research article (official class, two-column, Access title/abstract/index-term block, numbered headings). Sections I–III are easy to follow. Mathematics that is not adjacent to overflowing hashes is readable. Tables 3, 5, 6, 8, 9, 10, and 11 are usable.

Pages 4–8 would distract a reviewer: overlapping columns, unreadable protocol table, and clipped metric columns (especially TABLE 2’s M-5 side and TABLE 1’s UCI side). Those are obvious formatting defects, not scientific judgments.

DOCUMENT_PRESENTATION_QUALITY = MAJOR_FORMATTING_ISSUES

This label is visual/document formatting only. It is not a statement about scientific merit, acceptance, or publication.

## 8. Final Submission Blockers

AUTHOR_METADATA = INCOMPLETE_FOR_FINAL_SUBMISSION

Missing user inputs (not filled in this audit):

* biographies (both `IEEEbiographynophoto` bodies are empty; page 12 shows names only)
* emails
* ORCID
* corresponding-author designation
* funding (still omitted)
* acknowledgments (still omitted)

Template placeholders that remain visible: publication dates `xxxx 00, 0000` and the class example DOI `10.1109/ACCESS.2024.0429000`.

## 9. Scientific Integrity

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
scientific_content_changed = NO

STOP. No submission. No author metadata added. No scientific content modified. No acceptance prediction.
