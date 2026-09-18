# IEEE ACCESS FINAL PRE-SUBMISSION AUDIT

FINAL_SUBMISSION_AUDIT_STATUS = PASS_WITH_SUBMISSION_BLOCKERS

PDF_COMPILE_STATUS = PASS_WITH_LAYOUT_WARNINGS

PDF_INTEGRITY_STATUS = PASS_WITH_FORMAT_NOTES

AUTHOR_BLOCK_STATUS = PASS

SCIENTIFIC_CONTENT_STATUS = UNCHANGED

NUMERICAL_INTEGRITY_STATUS = MATCH

MODEL_PROVENANCE_STATUS = PASS

SHARIAH_GOVERNANCE_STATUS = NO_CERTIFICATION_OR_COMPLIANCE_CLAIM

REFERENCE_STATUS = PRESERVED

TEMPLATE_REQUIREMENTS_STATUS = PARTIALLY_MET

EXPERIMENTS_RUN = NONE

MODELS_CHANGED = NONE

RESULTS_CHANGED = NONE

DATA_CHANGED = NONE

CALIBRATION_CHANGED = NONE

THRESHOLDS_CHANGED = NONE

STAGE_2_10_STATUS = CLOSED_UNCHANGED

TEST_REOPENED = NO

SUBMISSION_STATUS = NOT_SUBMITTED

BLOCKERS_BEFORE_SUBMISSION = AUTHOR_BIOGRAPHIES_EMPTY; SUBMITTING_AUTHOR_ORCID_NOT_IN_PORTAL; CORRESPONDING_AUTHOR_NOT_DESIGNATED; AUTHOR_EMAILS_NOT_SUPPLIED

AUTHOR_ACTIONS_REQUIRED = SEE docs/paper/IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md

AUTHOR_METADATA_STATUS = USER_INPUT_REQUIRED

BIOS = USER_INPUT_REQUIRED

EMAILS = USER_INPUT_REQUIRED

ORCID = USER_INPUT_REQUIRED_OR_NOT_REQUIRED

CORRESPONDING_AUTHOR = USER_INPUT_REQUIRED

GRAPHICAL_ABSTRACT = VERIFY_PORTAL_REQUIREMENT

C_INFINITY_RENDERING = REVIEW_REQUIRED

---

| Item | Value |
| --- | --- |
| **Audit ID** | `IEEE-ACCESS-FINAL-SUBMISSION-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Type** | Pre-submission audit **only** (no scientific edits; no IEEE upload) |
| **Target venue** | IEEE Access |
| **Official template page** | https://ieeeaccess.ieee.org/authors/preparing-your-article/ |
| **Official submission guidelines** | https://ieeeaccess.ieee.org/authors/submission-guidelines/ |
| **Manuscript (source)** | `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` |
| **Manuscript (PDF)** | `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.pdf` |
| **Placement audit** | `docs/paper/IEEE_ACCESS_TEMPLATE_PLACEMENT_AUDIT.md` |
| **Integrity freeze** | `docs/paper/FINAL_MANUSCRIPT_INTEGRITY_AUDIT.md` |

This audit does **not** modify the manuscript, does **not** recalculate results, and does **not** submit.

**Metadata follow-up (2026-09-16):** owner values for biographies, emails, ORCID, and corresponding author have **still not been supplied** and were **not invented**. Collection template: `docs/paper/IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md`. The Access `.tex` / `.pdf` were not edited in that follow-up. The `C=\infty` PDF token remains a **review-required** typesetting issue (checklist records the exact line and a format-only proposal; **not applied**).

---

## Files read (no scientific writes)

| Path | Role |
| --- | --- |
| `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` | Access-ready LaTeX |
| `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.pdf` | Access-ready PDF (12 pages) |
| `docs/paper/ieee_access_official_templates/latex/ACCESS_latex_template_20260513/` | Official unpacked `ieeeaccess.cls` compile directory |
| `docs/paper/IEEE_ACCESS_TEMPLATE_PLACEMENT_AUDIT.md` | Placement record |
| `docs/paper/FINAL_MANUSCRIPT_INTEGRITY_AUDIT.md` | Frozen scientific integrity |
| `docs/paper/IEEE_TEMPLATE_READY_MANUSCRIPT.md` | Frozen wording source (spot-check of `C=\infty`) |
| Official Access pages (fetched this audit) | Preparing Your Article; Submission Guidelines |

No Stage 2–10 model, result, calibration, threshold, or dataset file was modified.

The compile copy `.../ACCESS_latex_template_20260513/IEEE_ACCESS_READY_MANUSCRIPT.tex` has the **same SHA-256** as `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` (`DBEBD02AE4B0C5E7E7937730C9D3FEDE09FBCC0444F85154FB74CC8E647CA99B`).

---

## A. PDF compilation

Recompiled from the unpacked official IEEE Access LaTeX directory:

`docs/paper/ieee_access_official_templates/latex/ACCESS_latex_template_20260513/`

| Check | Finding |
| --- | --- |
| Engine | MiKTeX `pdflatex` (two passes) |
| Exit code | **0** |
| LaTeX `!` errors | **None** |
| Fatal / emergency stop / undefined control sequence | **None** |
| Undefined citations after second pass | **None** |
| `\EOD` missing | **No** (`\EOD` is present) |
| Output | `IEEE_ACCESS_READY_MANUSCRIPT.pdf` — **12 pages**, 442777 bytes |

PDF_COMPILE_STATUS = PASS_WITH_LAYOUT_WARNINGS

**Warnings that can affect submission appearance (not treated as compile failure):**

| Warning class | Observed |
| --- | --- |
| Overfull `\hbox` | 72 messages (includes large `505.12177pt` overfulls during page output; two-column Access header/layout) |
| Underfull `\hbox` / `\vbox` | 95 messages |
| Font substitution | Courier `T1/pcr/n/n` → `T1/pcr/m/n`; Times `bx` → `b` (class/font-map substitutions) |
| MiKTeX | “you have not checked for MiKTeX updates” (local TeX install, not manuscript content) |

These are layout/font warnings. They were **not** used as a reason to rewrite science.

The `docs/paper/` PDF was **not overwritten** by this audit. A recompile in the official template directory produced a PDF of the **same page count and byte size**; SHA-256 differs (typical `pdflatex` metadata). Canonical PDF text extraction was performed on `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.pdf`.

---

## B. PDF integrity

Extracted text from the 12-page PDF (pypdf). PDF extraction concatenates columns and can split words; identities below are checked against that extract plus the `.tex`.

| Item | Finding |
| --- | --- |
| Page count | **12** |
| Title | Present: Evidence-Separated Credit Scoring, Additive Explainability, and Shariah-Oriented Governance: A Research Prototype on a LendingClub Extract, with Independent UCI Methodology Context |
| Authors | Present in Access uppercase byline: **AITSAM UL HASSAN** and **MUHAMMAD HASEEB RAMZAN** (same names; template uppercasing) |
| Affiliation | **Pak-Austria Fachhochschule: Institute of Applied Sciences and Technology, Haripur, Pakistan** |
| Abstract | Present; same frozen claims; 250 words in the `.tex` `abstract` environment (official template range 150–250) |
| Keywords / INDEX TERMS | Five frozen terms, alphabetized: credit risk, evidence traceability, explainable boosting machine, probability calibration, Shariah-oriented governance |
| Section order | I Introduction → II Related Work → III Research Gap and Contributions → IV Methodology → V Experimental Protocol → VI Results → VII Discussion → VIII Limitations → IX Conclusion → References |
| Equation (1) | Present (additive SHAP-style identity of the M-5 EBM). PDF text extract shows the same identity with subscript glyphs flattened. |
| Tables | Table identities preserved: datasets (I/1), G0 (IX/9) **before** two-EBM (II/2) and M-4B metrics (III/3); IV(a) Validation and IV(b) TEST reporting only; VII UCI before VIII credit bands; X year mix; XI L2×band. PDF extractor prints Arabic “TABLE 1 … TABLE 9 … TABLE 2 …” rather than Roman numerals; **counters were not scientifically reassigned**. |
| Fig. 1 | Present as the frozen text schematic caption |
| Fig. 2 | **Absent** (omitted as designed) |
| References | `[1]` through `[34]` present; mapping unchanged |
| Email / ORCID in PDF | **Absent** |
| Acknowledgments / funding | **Absent** |
| Author biographies | Name headings only; **no biographical sentences** (see blockers) |

**Format notes (not repaired in this audit):**

1. Official Access `\history` / `\doi{10.1109/ACCESS.2024.0429000}` placeholders appear on page 1. They are **template dummies**, not a claimed article DOI or publication date.
2. Frozen source `C=\infty` (Platt sklearn regularizer) is typeset in the PDF as `C=\{}infty` because the `.tex` contains `\texttt{C=\textbackslash\{\}infty}`. Frozen Platt parameters \(a=1.1988263209549705\) and \(b=0.6697765046966161\) are intact. **This audit did not repair that token** (no scientific edit).
3. Running headers / overfull boxes are layout warnings only.

PDF_INTEGRITY_STATUS = PASS_WITH_FORMAT_NOTES

No discrepancy was found in the **seven frozen numerical keys** (Section D). No Shariah-certification sentence was found. No Fig. 2 was found.

---

## C. Author information

Confirmed in `.tex` and PDF byline/affiliation only:

```
Aitsam Ul Hassan
Muhammad Haseeb Ramzan
Pak-Austria Fachhochschule:
Institute of Applied Sciences and Technology
Haripur, Pakistan
```

| Field | Status |
| --- | --- |
| Email | **Not present** (not invented) |
| ORCID | **Not present** (not invented) |
| Extra department | **Not present** |
| Corresponding-author line | **Omitted** (`\corresp` not used) |
| Biography text | **Empty** `IEEEbiographynophoto` slots (names only) |
| Funding `\tfootnote` | **Omitted** |
| Acknowledgments | **No section** |

AUTHOR_BLOCK_STATUS = PASS

---

## D. Scientific / numerical integrity

Compared Access `.tex` and PDF extract to the frozen keys. **Not recomputed from data.**

| Quantity | Required | `.tex` | PDF extract | Status |
| --- | --- | --- | --- | --- |
| M-4B EBM TEST ROC-AUC | `0.6799408767429772` | Present | Present (3) | MATCH |
| M-5 raw/Platt TEST ROC-AUC | `0.6776693941139847` | Present | Present (6) | MATCH |
| UCI XGBoost raw ECE (M-9.4-X) | `0.20065704943022225` | Present | Present (2) | MATCH |
| LC TEST \(n\) | `208886` | `208886` and `208,886` / `208{,}886` | `208886` (1) and `208,886` (8) | MATCH |
| \(t_{\mathrm{low}}\) | `0.06` | Present | Present | MATCH |
| \(t_{\mathrm{high}}\) | `0.69` | Present | Present | MATCH |
| \(t^{*}\) | `0.16` | Present | Present | MATCH |

NUMERICAL_INTEGRITY_STATUS = MATCH

No mismatch among the required keys. Nothing was recalculated. The `C=\infty` typesetting note in Section B is **not** a change to these keys or to frozen \(a\), \(b\).

SCIENTIFIC_CONTENT_STATUS = UNCHANGED

---

## E. Model provenance

| Context | Manuscript treatment | Audit |
| --- | --- | --- |
| **M-4B** | Stage 4B EBM TRAIN+VALIDATION refit; LC family TEST after freeze; not used from fusion onward | PASS |
| **M-5** | TRAIN-only EBM + validation-only Platt; downstream `p_selected` | PASS |
| **M-9.4-AE** | Independent UCI logistic-regression + EBM methodology | PASS |
| **M-9.4-X** | Exploratory UCI XGBoost / `DEVIATION-001`; not merged with M-4B LC XGBoost | PASS |

MODEL_PROVENANCE_STATUS = PASS

---

## F. Shariah / governance language

The PDF/abstract/conclusion retain the frozen **research-prototype / evidence-gap** wording.

| Prohibited claim | Found? |
| --- | --- |
| Shariah certification | **No** (explicitly denied) |
| Applicant-level Shariah compliance determination | **No** (`INSUFFICIENT_INFORMATION` is an evidence/schema limitation) |
| Halal/haram determination | **No** (terms absent) |
| Formal Shariah ruling / fatwa | **No** (explicitly denied) |

SECP “shall not be called Shariah compliant unless a Commission certificate is granted” remains a **prohibition** on certification language for this prototype.

SHARIAH_GOVERNANCE_STATUS = NO_CERTIFICATION_OR_COMPLIANCE_CLAIM

---

## G. References

| Check | Finding |
| --- | --- |
| Mapping | `[1]`–`[34]` ↔ `\bibitem{b1}`–`\bibitem{b34}` |
| New references | **None** |
| Invented DOI/URL/metadata | **None** (UNVERIFIED / NONE fields retained, including Platt [14]) |
| PDF | `[1]` … `[34]` present in REFERENCES |

REFERENCE_STATUS = PRESERVED

---

## H. Official IEEE Access requirements vs this manuscript

Checked against the official pages fetched this audit (not guessed from third-party blogs).

### Met (manuscript / compile)

| Requirement (official) | Finding |
| --- | --- |
| Use an IEEE Access Word **or** LaTeX template | Official `ieeeaccess.cls` from ieeeaccess.ieee.org (2026-05-13 bundle) |
| Submit source **and** PDF; contents must match | LaTeX source + PDF compiled from that source; PDF 12 pages |
| Double-column, single-spaced Access template | `ieeeaccess` class defaults |
| Source/PDF file size ≤ 40 MB | PDF ≈ 0.42 MB |
| Abstract 150–250 words (official sample/template text) | 250 words in `.tex` abstract |
| Keywords 3–10 at submission | Five Index Terms in the manuscript (portal keywords still an author action) |
| Strongly recommend &lt; 20 pages | **12 pages** |
| All authors listed on source and PDF | Both authors listed |
| References present; no new invented bibliography | `[1]`–`[34]` preserved |

### Not met in the frozen manuscript (do not invent; author action)

These are **official checklist items**. They are **not** filled in the frozen files.

| Official requirement | Manuscript state |
| --- | --- |
| Short biographies for **ALL** authors below references | Empty `IEEEbiographynophoto` environments (names only) |
| Submitting author **ORCID** on the IEEE Author Portal account (public, populated) | Not in the manuscript (correctly not invented) |
| Corresponding author designated **in the submission system** | Not designated (correctly not invented) |
| Author emails | Not in the manuscript (correctly not invented) |

TEMPLATE_REQUIREMENTS_STATUS = PARTIALLY_MET

### Not verified as a mandatory manuscript-file item (do not guess)

| Item | What official pages actually say | Audit |
| --- | --- | --- |
| Graphical abstract image | Preparing-Your-Article discusses **video** (≤ 100 MB) published as a graphical abstract; the numbered Submission Checklist **does not** list a GA image as a required upload | **UNVERIFIED** whether the Author Portal later asks for a GA file. Do not create one here. |
| Author photographs | Template documents author photos as a graphic type; checklist requires **biographies**, not explicitly photos | Photos **not invented**; `IEEEbiographynophoto` used |
| AI-generated-content acknowledgment | Required **if** AI-generated content is used; grammar-only AI is outside the main intent, disclosure recommended | No Acknowledgments section was invented. Authors must disclose **if applicable**. |
| Manuscript type | Portal selection (Research Article / etc.) | Author Portal action; not in the `.tex` |
| Scope / originality / not under review elsewhere | Editorial/policy items | Author Portal / cover-letter actions |

---

## I. Required external submission items (not part of the frozen manuscript)

Do **not** invent any of the following. They remain owner/portal inputs.

| Item | Required by | In frozen manuscript? |
| --- | --- | --- |
| Short author biographies (all authors) | Submission Checklist item 6 | **No** (empty slots) |
| Author photographs | Template graphic type; not verified as checklist-mandatory | **No** |
| Corresponding-author designation | Submission Checklist item 4 (system) | **No** |
| Author email address(es) | Portal / correspondence | **No** |
| Submitting-author ORCID (public profile) | Submission Checklist item 4 | **No** |
| Graphical abstract | **Not verified** as a checklist-mandatory manuscript file; check Author Portal | **No** (none created) |
| Portal metadata | Keywords (3–10), manuscript type, opposed reviewers, supplemental material, cover/ethics questions | **Not in `.tex`** |
| AI-use acknowledgment | If AI-generated content is used | **Not invented** |
| IEEE Copyright Form / eCF | After acceptance / final files (guidelines) | **Not this audit** |

BLOCKERS_BEFORE_SUBMISSION =

1. **Author biographies** — official Access rule: short biographies required for all authors below references. Currently empty.
2. **Submitting-author ORCID** — required on the Author Portal account; not supplied and not invented.
3. **Corresponding author** — must be designated in the submission system; not designated here.
4. **Author email(s)** — needed for portal correspondence; not in the manuscript.

AUTHOR_ACTIONS_REQUIRED =

- Supply biographies (and photos if the authors choose to include them).
- Create/link a public populated ORCID for the submitting author in the IEEE Author Portal.
- Designate the corresponding author and provide email(s) **in the portal**, not by inventing lines in the frozen `.tex` during this audit.
- Select manuscript type and 3–10 portal keywords (the five Index Terms already exist).
- Confirm on the Author Portal whether a graphical abstract file is requested; do not generate a new figure in this repository unless the authors supply one.
- Disclose AI-generated content in Acknowledgments **only if** that policy applies.
- Do not submit until the blockers above are resolved by the authors.

---

## J. Closed research state

| Item | Value |
| --- | --- |
| EXPERIMENTS_RUN | NONE |
| MODELS_CHANGED | NONE |
| RESULTS_CHANGED | NONE |
| DATA_CHANGED | NONE |
| CALIBRATION_CHANGED | NONE |
| THRESHOLDS_CHANGED | NONE |
| STAGE_2_10_STATUS | CLOSED_UNCHANGED |
| TEST_REOPENED | NO |
| SUBMISSION_STATUS | NOT_SUBMITTED |

---

## Final statement

The Access PDF **compiles without LaTeX errors** from the official template directory. Frozen numerals, model-context labels, Shariah evidence-gap wording, and references `[1]`–`[34]` are intact. Submission is **blocked** until the authors supply biographies and portal identity fields (ORCID, corresponding author, emails). This audit did not submit the article and did not repair the `C=\infty` typesetting token.
