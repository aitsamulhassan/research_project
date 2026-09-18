# Pre-Submission Integrity Audit

| Item | Value |
| --- | --- |
| **Audit ID** | `PRE-SUBMISSION-INTEGRITY-AUDIT` |
| **Audit date** | 2026-09-17 |
| **Type** | Repository-only pre-submission integrity gate |
| **Web search** | **None** |
| **Manuscript edited** | **No** |
| **Science / experiments** | **None** |

PRE_SUBMISSION_INTEGRITY_STATUS = USER_INPUT_REQUIRED

This audit read existing paper/audit files only. It did not invent author metadata, did not apply the `C=\infty` typesetting candidate, and did not modify any file except this report.

**Files read**

- `docs/paper/IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md`
- `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` (including line 333 and biography environments)
- `docs/paper/IEEE_TEMPLATE_PLACEMENT_AUDIT.md` (historical Markdown-placement record; `TEMPLATE_NOT_FOUND` at that time)
- `docs/paper/IEEE_ACCESS_TEMPLATE_PLACEMENT_AUDIT.md` (current Access placement: `TEMPLATE_PLACEMENT = COMPLETED`)
- `docs/paper/IEEE_ACCESS_FINAL_SUBMISSION_AUDIT.md`
- `docs/paper/FINAL_PAPER_INTEGRITY_GATE_AUDIT.md`
- `docs/paper/FINAL_MANUSCRIPT_DOCUMENTATION_CLEANUP_AUDIT.md`
- `docs/paper/IEEE_MANUSCRIPT.md`
- `docs/paper/IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md` paste blocks (empty)

Not modified: `IEEE_ACCESS_READY_MANUSCRIPT.tex` / `.pdf`, `MANUSCRIPT_DRAFT.md`, `MANUSCRIPT_EVIDENCE_MAP.md`, `IEEE_MANUSCRIPT.md`, `IEEE_TEMPLATE_READY_MANUSCRIPT.md`, Stage 2–10 artifacts, models, results, calibration, datasets, thresholds.

---

## 1. Current Submission State

| Item | Status in repository |
| --- | --- |
| Template | Official IEEE Access LaTeX class used (`ieeeaccess.cls`). `IEEE_ACCESS_TEMPLATE_PLACEMENT_AUDIT.md`: `TEMPLATE_PLACEMENT = COMPLETED`. Older `IEEE_TEMPLATE_PLACEMENT_AUDIT.md` recorded `TEMPLATE_NOT_FOUND` **before** Access placement; that historical file is not the current Access state. |
| Author metadata | `AUTHOR_METADATA_STATUS = USER_INPUT_REQUIRED` |
| Biography | `BIOS = USER_INPUT_REQUIRED` — empty `IEEEbiographynophoto` environments (names only) |
| ORCID | `ORCID = USER_INPUT_REQUIRED_OR_NOT_REQUIRED` — no ORCID string in the manuscript; checklist records portal vs co-author distinction; **not supplied** |
| Corresponding author | `CORRESPONDING_AUTHOR = USER_INPUT_REQUIRED` — `\corresp` omitted; comments only |
| Graphical abstract | `GRAPHICAL_ABSTRACT = VERIFY_PORTAL_REQUIREMENT` — no GA file/figure added |
| C=\infty rendering | `C_INFINITY_RENDERING = REVIEW_REQUIRED` — line 333 still the broken token; **not repaired** |

Submission has **not** been performed (`SUBMISSION_STATUS = NOT_SUBMITTED` in the final Access audit). Human metadata remains the submission blocker.

---

## 2. Author Metadata Integrity

Classification uses only what is in the repository. Empty checklist paste blocks contain **no values**.

| Field | Repository content | Classification |
| --- | --- | --- |
| Author names | `Aitsam Ul Hassan`; `Muhammad Haseeb Ramzan` in `IEEE_MANUSCRIPT.md` and `IEEE_ACCESS_READY_MANUSCRIPT.tex` (Access byline uses `\uppercase{...}`) | **User-provided** (owner-confirmed names already inserted). Not invented in this audit. Order matches those two files. |
| Affiliations | `Pak-Austria Fachhochschule: Institute of Applied Sciences and Technology, Haripur, Pakistan` as a single `\address[1]` shared by both authors | **User-provided** (owner-confirmed affiliation). No extra department name. |
| Emails | No `e-mail`, no `@domain` addresses, no `example@example.com` in the Access `.tex` | **Missing information** (not a filled placeholder; comments state omitted / not invented) |
| ORCID | No ORCID iD, no `0000-0000-0000-0000`, no `orcid.org` in the Access `.tex` | **Missing information** |
| Biographies | `\begin{IEEEbiographynophoto}{Aitsam Ul Hassan}` / `{Muhammad Haseeb Ramzan}` with **empty bodies**; comments: not supplied, not invented | **Placeholder / missing information** (slot present; **no invented bio text**) |
| Corresponding author | Comment: “Corresponding-author line omitted: not supplied; not invented.” No `\corresp{...}` | **Missing information** (not guessed) |
| Funding | Comment: “Funding/sponsor footnote omitted: not supplied; not invented.” No `\tfootnote{...}` | **Missing information** |
| Acknowledgments | No Acknowledgments section | **Missing information** (not fabricated) |

**Potentially invented information:** **None found** in the Access manuscript for emails, ORCID, biographies, corresponding-author designation, funding, or acknowledgments.

**Template production placeholders (not author identity):** `\history{Date of publication xxxx 00, 0000, ...}` and `\doi{10.1109/ACCESS.2024.0429000}` remain the official Access sample dummies. They are **not** claimed as this article’s DOI or as author metadata.

Checklist paste blocks in `IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md` are still blank (`Biography:`, `Email:`, `ORCID (if any):`, `Corresponding author? (yes/no):` with no filled values).

---

## 3. C=infinity Rendering Review

Inspected `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` **line 333** (not edited).

| Item | Finding |
| --- | --- |
| File | `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` |
| Line | **333** |
| Current source token | `\texttt{C=\textbackslash\{\}infty}` |
| Current rendering expression | Typewriter `C=` plus escaped backslash/braces, so `\infty` is **not** in math mode. Prior PDF extract recorded appearance `C=\{}infty`. |
| Expected mathematical meaning | Frozen manuscript: unregularized logistic regression **`C=\infty`** (sklearn unregularized Platt map). Adjacent frozen parameters on lines 336–337 remain \(a = 1.1988263209549705\), \(b = 0.6697765046966161\). Solver remains `lbfgs`. |
| Formatting-only? | **Yes.** This is a LaTeX escaping/transcription defect from converting inline code `` `C=\infty` `` into `\texttt{...}`. It does **not** change the recorded Platt \(a\), \(b\), selected method, or any frozen result numeral. |
| Changes scientific meaning of \(C=\infty\)? | **Intended meaning unchanged** (`C` unbounded / infinity). **Displayed token is wrong.** |

**Safe candidate replacement(s) — not applied**

Replace **only** `\texttt{C=\textbackslash\{\}infty}` on line 333 with one of:

1. `\texttt{C=}\(\infty\)`
2. `\(C=\infty\)`

Do not change \(a\), \(b\), `lbfgs`, or any metric. **This audit does not apply either replacement.**

---

## 4. Scientific Integrity Confirmation

This gate did not run code, retrain models, or rewrite science files. Frozen keys remain in `IEEE_ACCESS_READY_MANUSCRIPT.tex` as previously recorded (`0.6799408767429772`, `0.6776693941139847`, `0.20065704943022225`, \(t_{\text{low}}=0.06\), \(t_{\text{high}}=0.69\), \(t^{*}=0.16\); M-9.4-AE independent UCI LR+EBM; M-9.4-X exploratory `DEVIATION-001`). Prior audits (`FINAL_PAPER_INTEGRITY_GATE_AUDIT.md`, `FINAL_MANUSCRIPT_DOCUMENTATION_CLEANUP_AUDIT.md`, `IEEE_ACCESS_FINAL_SUBMISSION_AUDIT.md`) record Stage 9/10 closed, TEST not reopened, experiments none.

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

---

## 5. Remaining Human Inputs

Only items that the repository still lacks and that authors must supply (no example values):

1. Short biography text for Aitsam Ul Hassan (required by Access for all authors; empty slot only).
2. Short biography text for Muhammad Haseeb Ramzan (same).
3. Email address for each author if the owners will print or enter contact addresses.
4. Corresponding-author designation (which of the two authors; portal `\corresp` only after owner decision).
5. Submitting-author ORCID for the IEEE Author Portal account, if that author will submit (not present in the `.tex`; not invented).
6. Optional: co-author ORCID; optional author photographs; Author Portal graphical-abstract file **if** the portal asks for one (not verified in-repo as a required manuscript figure).
7. Optional later format-only authorization to apply the line-333 `C=\infty` typesetting candidate.
8. Funding and acknowledgments **only if** the authors have real text to add (currently omitted, not fabricated).

Do not invent any of the above.

---

## 6. Gate Status

PRE_SUBMISSION_INTEGRITY_STATUS = USER_INPUT_REQUIRED

Human input remains (biographies, emails, corresponding author; ORCID as portal/user input). The repository does **not** prove that no human input remains.

**Not done in this audit:** manuscript edit; `C=\infty` fix; author metadata insertion; experiments; TEST / Stage 9 / Stage 10 reopen; submission.
