# Final LaTeX Build QA

Scope: formatting-only correction of the malformed \(C=\infty\) token, then compile/QA of the IEEE Access manuscript. Scientific content remains frozen. Author emails, ORCID, biographies, corresponding-author designation, funding, and acknowledgments were not supplied and were not invented. This report does not authorize submission.

## 1. C=infinity Fix

* original expression: `\texttt{C=\textbackslash\{\}infty}` (prints the literal string `C=\{}infty`; frozen meaning is \(C=\infty\), sklearn unregularized Platt logistic)
* corrected expression: `\texttt{C=}\(\infty\)` (monospace `C=` followed by mathematical infinity)
* file: `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex`
* line: 333
* confirmation that the change is formatting-only: YES

The surrounding Platt-form sentence, citation `\cite{b14}`, solver `\texttt{lbfgs}`, frozen parameters \(a=1.1988263209549705\) and \(b=0.6697765046966161\), and all other wording on that line are unchanged. The same one-token replacement was applied to the official-template compile copy `docs/paper/ieee_access_official_templates/latex/ACCESS_latex_template_20260513/IEEE_ACCESS_READY_MANUSCRIPT.tex` so that PDF generation used the corrected source. SHA-256 of both `.tex` files after the fix: `5F06F309D853F0BD538EF3775B6010050F5B654DC30FE43C556807F7E61CC20D`.

PDF text extraction of the compiled article shows the intended rendering: `unregularized logistic regression (C=∞, solver lbfgs)`. The malformed `C=\{}infty` token is gone.

## 2. Compilation

* compiler used: pdfTeX 3.141592653-2.6-1.40.28 (MiKTeX 25.12), format `pdflatex` (preloaded 2026.9.2). Two nonstopmode passes from `docs/paper/ieee_access_official_templates/latex/ACCESS_latex_template_20260513/` so that `ieeeaccess.cls`, Access fonts, `logo.png`, `bullet.png`, and `notaglinelogo.png` resolve.
* compilation status: SUCCESS. No fatal errors. Output written on `IEEE_ACCESS_READY_MANUSCRIPT.pdf` (12 pages, 442980 bytes). Build artifact copied to `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.pdf` (SHA-256 `3891F8312DB4A119129F399A57219C7099861B35E2B4D8FED8D2209AC769B9F8`).
* errors: NONE (`!` fatal/error lines = 0).
* warnings (non-fatal; none block compilation):
  * LaTeX Font Warning: font shape `T1/pcr/n/n` undefined, substituted `T1/pcr/m/n` (2 font-warning records). This is a Courier/typewriter fallback, not a missing citation or reference.
  * Overfull `\hbox`: 72 (IEEE Access two-column layout plus wide tables/hashes; also template header/logo boxes of 505.12177pt while `\output` is active).
  * Underfull `\hbox`: 93; underfull `\vbox`: 2.
  * Package `bm` Info (not errors): no bold for some math symbol fonts, using `\pmb`.
  * MiKTeX note: updates not checked. Not a manuscript error.
  * `LaTeX Warning:` lines (undefined references / rerun required): 0.
* unresolved references: NONE. Unique `\label` count = 13; no multiply-defined labels. Log does not contain “There were undefined references.” Auxiliary file contains no undefined markers.
* unresolved citations: NONE. Bibliography keys `b1`--`b34` are all cited and all defined (`\bibitem` count = 34; missing cites = none; unused bibs = none). Auxiliary file: 34 `\bibcite` entries. Citation-undefined count in the log = 0.

Equation (1) compiled. Figure 1 compiled (text schematic). No Figure 2 (omitted by frozen manuscript design). Eleven `table*` environments (`tab:t1`, `tab:t9`, `tab:t2`--`tab:t8`, `tab:t10`, `tab:t11`); no duplicate table or figure environments.

## 3. Document Integrity

Confirm:

* title unchanged: YES. `\title{Evidence-Separated Credit Scoring, Additive Explainability, and Shariah-Oriented Governance: A Research Prototype on a LendingClub Extract, with Independent UCI Methodology Context}`
* abstract unchanged: YES (no abstract edits).
* index terms unchanged: YES. `credit risk, evidence traceability, explainable boosting machine, probability calibration, Shariah-oriented governance.`
* sections unchanged: YES. Introduction; Related Work; Research Gap and Contributions; Methodology; Experimental Protocol; Results; Discussion; Limitations; Conclusion.
* tables unchanged: YES (no table text, captions, labels, or numeric cells edited).
* figures unchanged: YES (one text schematic, Figure 1; no Figure 2 added).
* equations unchanged except the rendering correction: YES. Display equation (1) (centered additive SHAP identity) was not edited. The only math-token change is the inline \(C=\infty\) rendering on line 333.
* references unchanged: YES. `[1]`--`[34]` / `b1`--`b34` unmodified.
* scientific results unchanged: YES. Frozen stored values remain in the compiled PDF, including M-5 TEST ROC-AUC `0.6776693941139847`, Platt Brier `0.15616920271522994`, Platt ECE `0.020267295489117824`, Platt \(a=1.1988263209549705\), and M-4B TEST EBM ROC-AUC `0.6799408767429772`.

No edits were made to `docs/paper/MANUSCRIPT_DRAFT.md`, `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md`, Stage 2--10 artifacts, evidence master, datasets, models, calibration, or thresholds.

## 4. Author Metadata

Confirm:

* author metadata remains user-input dependent: YES. Names and the single affiliation line already present in the frozen template placement were not altered. No emails, departments, or additional affiliations were added. Comments at lines 38--39 still record that corresponding-author and funding footnotes are omitted because they were not supplied.
* bios remain user-input dependent: YES. Both `IEEEbiographynophoto` environments remain empty of biographical text:

```
\begin{IEEEbiographynophoto}{Aitsam Ul Hassan}
\end{IEEEbiographynophoto}

\begin{IEEEbiographynophoto}{Muhammad Haseeb Ramzan}
\end{IEEEbiographynophoto}
```

The compiled PDF ends with the two names only (`AITSAM UL HASSAN` / `MUHAMMAD HASEEB RAMZAN`) and no invented biography paragraphs.

* emails remain user-input dependent: YES. No `\thanks`, e-mail, or `@` author-contact addresses were inserted. PDF extraction contains no `example@` / invented mailbox.
* ORCID remains user-input dependent: YES. No ORCID identifiers were inserted. PDF extraction contains no `ORCID` string.
* corresponding author remains user-input dependent: YES. No `\corresp` line and no “corresponding author” designation were inserted.

Funding and acknowledgments were not invented. Empty biography slots were not filled.

## 5. Scientific Integrity

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

## 6. Gate

FINAL_LATEX_BUILD_QA_STATUS = PASS_WITH_AUTHOR_METADATA_BLOCKER

Compilation succeeded. The \(C=\infty\) rendering bug is corrected. Remaining blockers are user-input author items (emails, ORCID, biographies, corresponding-author designation) plus any venue items the owner must still supply in the IEEE Author Portal (not invented here). PRE_SUBMISSION_INTEGRITY_STATUS remains USER_INPUT_REQUIRED.

STOP. No submission package assembly. No author information added. No biographies invented. No graphical abstract created. No scientific content changed beyond the one formatting token on line 333.
