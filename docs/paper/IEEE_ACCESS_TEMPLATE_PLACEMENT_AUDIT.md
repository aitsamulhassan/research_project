# IEEE ACCESS TEMPLATE PLACEMENT AUDIT

TARGET_VENUE = IEEE ACCESS

OFFICIAL_TEMPLATE_SOURCE = https://ieeeaccess.ieee.org/authors/preparing-your-article/

TEMPLATE_PLACEMENT = COMPLETED

EXPERIMENTS_RUN = NONE

MODELS_CHANGED = NONE

RESULTS_CHANGED = NONE

DATA_CHANGED = NONE

CALIBRATION_CHANGED = NONE

THRESHOLDS_CHANGED = NONE

STAGE_9 = CLOSED

STAGE_10 = CLOSED

TEST_REOPENED = NO

M9_4_AE = INDEPENDENT_UCI_LOGISTIC_REGRESSION_AND_EBM

M9_4_X = EXPLORATORY_UCI_XGBOOST_DEVIATION_001

SHARIAH_CERTIFICATION_CLAIM = NO

NEW_CITATIONS = NO

NEW_FIGURES = NO

NEW_TABLE_DATA = NO

SCIENTIFIC_CONTENT_CHANGED = NO

---

| Item | Value |
| --- | --- |
| **Audit ID** | `IEEE-ACCESS-TEMPLATE-PLACEMENT-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Type** | Venue-specific formatting / official-template placement only |
| **Scientific research** | **CLOSED** (Stages 2–10 unchanged) |
| **Submission performed** | **NO** |

---

## Official template acquisition

The official IEEE Access author page was used (not a third-party template):

| Item | Value |
| --- | --- |
| Official page | https://ieeeaccess.ieee.org/authors/preparing-your-article/ |
| Related official page (requirements) | https://ieeeaccess.ieee.org/authors/submission-guidelines/ |
| Official Word template | https://ieeeaccess.ieee.org/wp-content/uploads/2025/08/Access-Template-2024.docx |
| Official LaTeX template | https://ieeeaccess.ieee.org/wp-content/uploads/2026/05/ACCESS_latex_template_20260513-1-1.zip |
| Word file obtained | `docs/paper/ieee_access_official_templates/Access-Template-2024.docx` (PK/ZIP Word document; 335244 bytes) |
| LaTeX zip obtained | `docs/paper/ieee_access_official_templates/ACCESS_latex_template_20260513-1-1.zip` (application/zip; 1942796 bytes; first curl attempt returned Cloudflare HTML 403 and was replaced by a successful official zip fetch) |
| Unpacked official class | `docs/paper/ieee_access_official_templates/latex/ACCESS_latex_template_20260513/ieeeaccess.cls` (with `IEEEtran.cls`, fonts, `logo.png`, `bullet.png`) |
| Template invented? | **NO** |

Placement uses the **official LaTeX class** `ieeeaccess.cls` from the 2026-05-13 IEEE Access bundle. The official Word `.docx` was obtained and retained as the official Word file; it was **not** filled, to avoid a second copy of the science and to keep numerals under LaTeX transcription control.

The official template states that the article must be submitted using an IEEE Access template as a Word or LaTeX file **and** as a PDF; that the manuscript is double-column, single-spaced; and that the abstract must be 150–250 words. Those rules were applied as formatting constraints. Submission was **not** performed.

---

## Files used as scientific sources (read only)

| Role | Path |
| --- | --- |
| Placement-ready wording | `docs/paper/IEEE_TEMPLATE_READY_MANUSCRIPT.md` |
| Evidence master | `docs/paper/MANUSCRIPT_DRAFT.md` |
| Evidence map | `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md` |
| Integrity freeze | `docs/paper/FINAL_MANUSCRIPT_INTEGRITY_AUDIT.md` |
| Prior IEEE placement audit | `docs/paper/IEEE_TEMPLATE_PLACEMENT_AUDIT.md` |
| M-9.4-AE correction | `docs/paper/M9_4_AE_CORRECTION_LOG.md` |

Scientific claims, numerals, table cells, equation (1), references [1]–[34], model-context labels, and Shariah governance wording were transcribed from those sources. They were not rewritten.

---

## Files created / modified

| Path | Action |
| --- | --- |
| `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` | **Created** — Access-ready manuscript in the official `ieeeaccess` class |
| `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.pdf` | **Created** — compiled PDF of that `.tex` (12 pages; not a new scientific result) |
| `docs/paper/ieee_access_official_templates/` | **Created** — official Word `.docx`, official LaTeX `.zip`, unpacked official class/fonts |
| `docs/paper/ieee_access_official_templates/latex/ACCESS_latex_template_20260513/IEEE_ACCESS_READY_MANUSCRIPT.tex` | **Created** — compile copy next to official `ieeeaccess.cls` / fonts / logos |
| `docs/paper/IEEE_ACCESS_TEMPLATE_PLACEMENT_AUDIT.md` | **Created** (this file) |
| `docs/paper/MANUSCRIPT_DRAFT.md` | **Not modified** |
| `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md` | **Not modified** |
| `docs/paper/IEEE_MANUSCRIPT.md` | **Not modified** |
| `docs/paper/IEEE_TEMPLATE_READY_MANUSCRIPT.md` | **Not modified** |
| Stage 2–10 artifacts / models / results / calibration / thresholds | **Not modified** |

Compile from the official unpacked template directory so `ieeeaccess.cls`, Access fonts, `logo.png`, and `bullet.png` resolve.

---

## Author information

Inserted exactly as supplied:

- Aitsam Ul Hassan
- Muhammad Haseeb Ramzan
- Pak-Austria Fachhochschule: Institute of Applied Sciences and Technology, Haripur, Pakistan

| Field | Status |
| --- | --- |
| Email addresses | **Not invented** |
| ORCID | **Not invented** (IEEE Author Portal requires submitting-author ORCID at submission; not placed in the manuscript) |
| Department beyond the confirmed institute line | **Not invented** |
| Corresponding-author status | **Not invented** (`\corresp` omitted) |
| Acknowledgments | **Not invented** (no Acknowledgments section) |
| Funding footnote | **Not invented** (`\tfootnote` omitted) |
| IEEE membership marks | **Not invented** |

Official Access `\history{Date of publication xxxx 00, 0000, ...}` and `\doi{10.1109/ACCESS.2024.0429000}` are **template placeholders** copied from the official `access.tex` sample. They are not a claimed Digital Object Identifier or publication date for this article.

---

## Abstract and keywords

| Check | Finding |
| --- | --- |
| Abstract text | Preserved from the frozen manuscript (no added fraud, real-time, production, certification, or XGBoost-superiority claims) |
| Official Access abstract length | 150–250 words required by the official template |
| Word count of the Access `abstract` environment | **250** (within the official range; not rewritten) |
| Keywords | The five frozen Index Terms, alphabetized as the official template instructs: credit risk, evidence traceability, explainable boosting machine, probability calibration, Shariah-oriented governance |
| Keyword identity | **Same five terms**; order-only formatting |

---

## Tables and figures

| Check | Finding |
| --- | --- |
| Table contents | Transcribed from the frozen manuscript; cells not recalculated |
| Table II before Table III | **Yes** |
| Table VII before Table VIII | **Yes** |
| Table IV (a) Validation | **Present** |
| Table IV (b) TEST (reporting only) | **Present** |
| Table I (datasets) and Table IX (G0) | Remain in Methods with frozen identities (IX still G0; not renumbered to appearance-order Table II) |
| Fig. 1 | Existing text schematic retained as a `figure*` tabular schematic (not a new image file) |
| Fig. 2 | **Omitted** (duplicate of Table IX G0) |
| Reliability diagrams | **Not regenerated** |
| Synthetic figures | **None** |
| NEW_FIGURES | **NO** |
| NEW_TABLE_DATA | **NO** |

---

## Model provenance (not merged)

| Context | Treatment in the Access manuscript |
| --- | --- |
| **M-4B** | Stage 4B EBM TRAIN+VALIDATION refit (LendingClub family TEST after freeze) |
| **M-5** | TRAIN-only EBM + validation-only Platt calibration (downstream `p_selected`) |
| **M-9.4-AE** | Independent UCI logistic-regression + EBM methodology |
| **M-9.4-X** | Exploratory UCI XGBoost / `DEVIATION-001` |

---

## Shariah language

No Shariah certification, applicant-level compliance determination, halal/haram determination, or formal Shariah ruling was introduced. Existing research-prototype / evidence-gap language is preserved (`INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`, `INSUFFICIENT_INFORMATION`, not `EXPERT_VALIDATED`).

SHARIAH_CERTIFICATION_CLAIM = NO

---

## Numerical integrity (not recalculated)

| Quantity | Required | Status in Access `.tex` |
| --- | --- | --- |
| M-4B EBM TEST ROC-AUC | `0.6799408767429772` | Present (unchanged) |
| M-5 raw/Platt TEST ROC-AUC | `0.6776693941139847` | Present (unchanged) |
| UCI XGBoost raw ECE (M-9.4-X) | `0.20065704943022225` | Present (unchanged) |
| LC TEST \(n\) | `208886` | Present as `208886` and `208,886` / `208{,}886` as in the frozen manuscript |
| \(t_{\mathrm{low}}\) | `0.06` | Present |
| \(t_{\mathrm{high}}\) | `0.69` | Present |
| \(t^{*}\) | `0.16` | Present |

Equation (1) is the frozen additive identity \(\phi_i(x) = g_i(x_i) - \operatorname{mean}_{\text{TRAIN}} g_i\). It was not replaced by a new formula.

No numerical discrepancy was found relative to the frozen manuscript. Nothing was recalculated from data.

---

## References

Mapping `[1]`–`[34]` is preserved as `\bibitem{b1}`–`\bibitem{b34}` with `\cite{b1}` etc. Source identity, DOIs/URLs, and UNVERIFIED/NONE fields are retained. No DOI, URL, missing metadata, or new reference was invented.

NEW_CITATIONS = NO

In-text citation syntax is IEEE Access `\cite{...}` formatting only.

---

## Official Access slots left empty (not invented)

IEEE Access additionally expects items that this owner block does not supply. They were **not invented**:

| Slot | Handling |
| --- | --- |
| Short biographies for all authors (below references) | Empty `IEEEbiographynophoto` environments with confirmed names only |
| Author photographs | **Not invented** |
| Graphical abstract | **Not created** (would be a new figure; typically a separate Author Portal upload) |
| Corresponding author / email | **Omitted** |
| Acknowledgments / AI-use disclosure paragraph | **Omitted** (no Acknowledgments section was invented) |

These are remaining owner/submission-system inputs. They do not change the frozen science.

---

## Compilation (format check only)

| Item | Value |
| --- | --- |
| Engine | MiKTeX `pdflatex` using official `ieeeaccess.cls` |
| Result | PDF written; 12 pages |
| Experiments | None |
| Layout warnings | Overfull/underfull boxes typical of two-column Access layout; not treated as a reason to rewrite science |

IEEE Access also requires a PDF at submission. The compiled PDF is a format product of the official class. Submission was not performed.

---

## Closed-stage confirmation

| Item | Value |
| --- | --- |
| EXPERIMENTS_RUN | NONE |
| MODELS_CHANGED | NONE |
| RESULTS_CHANGED | NONE |
| DATA_CHANGED | NONE |
| CALIBRATION_CHANGED | NONE |
| THRESHOLDS_CHANGED | NONE |
| STAGE_9 | CLOSED |
| STAGE_10 | CLOSED |
| TEST_REOPENED | NO |
| SCIENTIFIC_CONTENT_CHANGED | NO |

---

## Final status

TEMPLATE_PLACEMENT = COMPLETED

The frozen manuscript is in the official IEEE Access LaTeX template at `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex`. This audit does not authorize submission, Stage 11, experiments, or scientific edits.
