# IEEE Access Layout Repair Audit

## 1. Repair Scope

Changes were formatting-only. Scientific wording, citations, references, table values, figure content, thresholds, calibration parameters, and model/dataset claims were not rewritten. Author emails, ORCID, biographies, corresponding-author designation, funding, and acknowledgments were not added.

LaTeX edits are in `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex`. The previous 12-page PDF `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.pdf` was left in place. The repaired build artifact is `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf`.

## 2. Problems Repaired

### SHA-256 collisions

* Technique: layout-only `\sha{...}` helper (`\DeclareRobustCommand` + `\detokenize` + per-character `\allowbreak` inside `\ttfamily`). Long filesystem paths use the same helper. Hashes are not truncated, not ellipsized, and not altered. Complete 64-character strings reconstruct from the PDF text layer after removing wrap whitespace.

### TABLE 1 UCI clipping

* Technique: `table*` + `tabularx{\linewidth}` with `p{}` / `X` columns so the UCI column wraps instead of `|l|l|l|` overflow. SHA-256 cells use `\sha{...}`.

### TABLE 2 M-5 clipping

* Technique: `tabularx{\linewidth}` with wrapping `X` columns for the M-4B and M-5 sides. Joblib paths and the M-5 SHA-256 wrap inside the cell. Frozen ROC-AUC values remain in bold in both columns.

### TABLE 7 ECE note clipping

* Technique: `\resizebox{\linewidth}{!}` plus a `p{3.35cm}` ECE column so `0.20065704943022225 (selected-family raw; see note)` wraps in-cell. M-9.4-AE / M-9.4-X / `DEVIATION-001` wording is unchanged.

### TABLE 9 float placement

* Technique: converted the G0 matrix from `table*` to a single-column `table[!t]` with `tabularx{\columnwidth}` (first-column wrap of `NOT_STRUCTURABLE_WITHOUT_REDESIGN`). Table number remains TABLE 9 (`\setcounter{table}{8}` unchanged). It now appears in the methods/governance region (page 7), not as a two-column banner immediately above TABLE 2 on the results pages. TABLE 2 remains TABLE 2. Cross-references were not renamed.

Unnumbered single-column tabulars that previously crossed the gutter (model-context table; experimental-protocol table; governance-treatment table; Fig. 1 schematic) were constrained with `tabularx`/`p{}` and, where needed, `\resizebox{\columnwidth}{!}`.

## 3. Scientific Preservation

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

## 4. Build

* compiler: pdfTeX 3.141592653-2.6-1.40.28 (MiKTeX 25.12), `pdflatex`, official Access class directory `docs/paper/ieee_access_official_templates/latex/ACCESS_latex_template_20260513/`
* number of passes: 2 consecutive nonstopmode passes for the final artifact (citations/floats resolved; log does not request a rerun)
* page count: 13 (was 12; wrapping of previously overflowing strings/tables added one page)
* compilation result: SUCCESS. Fatal `!` errors = 0.
* citation status: no undefined citations
* reference status: no undefined references; no multiply-defined labels. Figure 1 present. Tables 1–11 present (9, then 2–8, 10, 11 as numbered; Fig. 2 still omitted).

## 5. Visual QA

Inspected all 13 pages of `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf`.

### Page 1

CLEAN for Access title/abstract/index-term/two-column opening. Template date/DOI placeholders remain. Citation ranges still show a thin space after `–` (`[14]– [16]`).

### Page 2

CLEAN. Two-column related work; no collisions.

### Page 3

CLEAN. Subsection heading wrap (`IDENTITY AND SCOPE`) unchanged and readable.

### Page 4

No column-to-column collision (the previous SHA/table gutter overwrite is gone). Remaining: the unnumbered five-column context tabular is cramped after `\resizebox{\columnwidth}{!}` / `p{}` wrapping (`TRAIN+ VALIDATION` line-breaks inside cells). Readable; no overlap with the right column.

### Page 5

CLEAN relative to the prior collision. FIGURE 1 text schematic fits the full-width float. UCI/LendingClub hashes wrap inside the column. Hyperparameter bullets wrap.

### Page 6

TABLE 1 UCI column is complete and inside the page. SHA-256 cells wrap rather than clip. Body hashes wrap. \(C=\infty\) and equation (1) render. Remaining: a band of whitespace under the TABLE 1 float before the M-4B/M-5 text resumes (standard `table*` deferral, not a collision).

### Page 7

TABLE 9 (G0) sits in the methods column, not on the results pages. Matrix cells are readable. Long governance identifiers wrap inside the treatment table. Remaining: unused space in the right column below TABLE 9 (single-column float). Freeze SHA-256 strings wrap in-column and are complete.

### Page 8

No gutter collision. Protocol table stays in the left column; Results §VI continues in both columns. Remaining: protocol table is dense/scriptsize; some first-column wraps are tight (`Explainability` / `Attributions`).

### Page 9

TABLE 2 M-5 column is complete (paths, SHA-256, ROC-AUC `0.6776693941139847`). TABLES 3–6 fit the page. Remaining: TABLE 4 is dense after `\resizebox` (digits remain; font is small).

### Page 10

CLEAN. Two-column UCI/discussion text; no collisions.

### Page 11

TABLE 7 ECE note is complete in-cell: `0.20065704943022225 (selected-family raw; see note)`. TABLES 8, 10, 11 readable. Limitation list continues cleanly.

### Page 12

CLEAN. Conclusion and references `[1]`–`[24]` in two-column Access bibliography format. `[22]` is present.

### Page 13

References `[25]`–`[34]` visible. Remaining: empty biography nameplates and lower-page whitespace (metadata still not supplied; not invented). One long CFPB URL in `[34]` wraps.

## 6. Scientific Value Preservation

Confirmed present in the repaired PDF (contiguous or wrap-reconstructed):

* `0.6799408767429772`
* `0.6776693941139847`
* `0.20065704943022225`
* `208886`
* `0.06` / `0.69` / `0.16`
* \(C=\infty\)
* Platt \(a=1.1988263209549705\), \(b=0.6697765046966161\)
* All previously recorded SHA-256 strings (including `8d373df1…`, `207d65b2…`, `e15ddd2f…`, freeze hashes)
* `DEVIATION-001`; M-9.4-AE / M-9.4-X labels; selected-family raw ECE note

## 7. Final Status

IEEE_ACCESS_LAYOUT_STATUS = MINOR_FORMATTING_ISSUES

The prior MAJOR defects (gutter collisions, clipped TABLE 1 UCI / TABLE 2 M-5 / TABLE 7 ECE, TABLE 9 bannered on top of TABLE 2) are repaired. Remaining notes are cramped single-column tabulars, `table*` whitespace, multi-line wrapped hashes, one extra page, and empty biography slots.

This label is visual/document formatting only. It is not a scientific-quality, acceptance, or submission-readiness claim.

STOP. No submission. No author metadata added.
