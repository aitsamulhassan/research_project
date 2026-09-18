# Final Submission-Blocker Audit

| Item | Value |
| --- | --- |
| **Document ID** | `FINAL-SUBMISSION-BLOCKER-AUDIT` |
| **Audit date** | 2026-09-17 |
| **Type** | Submission-blocker diagnosis only |
| **Manuscript source** | `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` |
| **Current review PDF** | `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf` (13 pages) |
| **Web search** | **None** |
| **Manuscript / PDF / Stage 2–10 modified** | **No** |

This audit inspects the **current** source and review PDF. Older checklist lines that still say `C_INFINITY_RENDERING = REVIEW_REQUIRED` are treated as **stale** relative to `FINAL_LATEX_BUILD_QA.md` and the live PDF text layer.

---

## FINAL_SUBMISSION_BLOCKER_STATUS

```text
FINAL_SUBMISSION_BLOCKER_STATUS = READY_FOR_USER_METADATA
```

Remaining blockers are **owner-supplied author metadata** (and portal-time checks). No scientific file fix and no scientifically required figure/equation add are outstanding.

---

## 1. Frozen integrity cross-check (current PDF / source)

| Check | Evidence | Status |
| --- | --- | --- |
| Authors exactly `Aitsam Ul Hassan`; `Muhammad Haseeb Ramzan` | `.tex` `\author{...}`; PDF byline `AITSAM UL HASSAN` / `MUHAMMAD HASEEB RAMZAN` | **SATISFIED** |
| Affiliation exactly Pak-Austria Fachhochschule: Institute of Applied Sciences and Technology, Haripur, Pakistan | `.tex` `\address[1]{...}`; PDF line 8 | **SATISFIED** |
| Abstract ≈ 250 words (Access abstract length as locked in prior placement/final-submission audits) | Abstract environment unchanged in `.tex`; PDF ABSTRACT block present | **SATISFIED** |
| References `[1]`–`[34]` | `\bibitem{b1}` … `\bibitem{b34}` in `.tex`; PDF ends with `[34]` | **SATISFIED** |
| TEST n = 208886 / 208,886 | Abstract, Table I/II, results prose; PDF abstract and TABLE 2 | **SATISFIED** |
| \(t_{\mathrm{low}}/t_{\mathrm{high}}/t^{*}=0.06/0.69/0.16\) | `.tex` §IV-J; PDF p. 7 `tlow = 0.06, thigh = 0.69`, `t∗ = 0.16` | **SATISFIED** |
| M-4B TEST ROC-AUC `0.6799408767429772` | TABLE 2 / TABLE 3; PDF p. 9 | **SATISFIED** |
| M-5 raw/Platt TEST ROC-AUC `0.6776693941139847` | Abstract + TABLE 2 / TABLE 4(b); PDF | **SATISFIED** |
| UCI XGBoost raw ECE `0.20065704943022225` | TABLE 7; PDF p. 11 | **SATISFIED** |
| \(C=\infty\) renders correctly | Source: `\texttt{C=}\(\infty\)` (not the old broken token). PDF: `unregularized logistic regression (C=∞, solver lbfgs)`. Confirmed in `FINAL_LATEX_BUILD_QA.md` and layout-repair scientific preservation | **SATISFIED** (see §3B; checklist label is stale) |
| No TreeSHAP-used claim | “TreeSHAP was not used” / designed for trees not this EBM | **SATISFIED** |
| No Shariah certification/compliance claim | Explicit denials; `INSUFFICIENT_INFORMATION` = evidence gap | **SATISFIED** |
| No fraud-detection performance claim | Explicit negative claim; Bolton & Hand literature-only | **SATISFIED** |
| No real-time/production claim | Prototype; production/real-time not evidenced | **SATISFIED** |
| Stage 9 / 10 closed; no reopen | Cross-stage + scientific-reviewer audits | **SATISFIED** |
| Scientific MUST_FIX | `FINAL_SCIENTIFIC_REVIEW_AUDIT.md`: none | **SATISFIED** |
| Required figures/equations | `FIGURE_EQUATION_NECESSITY_AUDIT.md`: none missing | **SATISFIED** |

---

## 2. A. USER INPUT REQUIRED

| # | Exact requirement | Evidence | Current status | Exact action needed | Without scientific content change? |
| --- | --- | --- | --- | --- | --- |
| A1 | Short biographies for **all** authors below References (Access checklist item 6) | Empty `IEEEbiographynophoto` bodies in `.tex` lines 961–965; PDF p. 13 shows names only (`AITSAM UL HASSAN` / `MUHAMMAD HASEEB RAMZAN`) | **USER_INPUT_REQUIRED** / **BLOCKED** | Owner supplies biography text for both authors; later format-only insert into existing nophoto environments | **Yes** |
| A2 | Author email addresses (portal / corresponding-author contact; template `\corresp` uses email when used) | No `@` author emails in `.tex`; comments: not supplied / not invented. Checklist paste blocks empty | **USER_INPUT_REQUIRED** / **BLOCKED** | Owner supplies emails; do not invent placeholders | **Yes** |
| A3 | Corresponding-author designation (who is the contact) | No `\corresp`; comment at `.tex` line 46 | **USER_INPUT_REQUIRED** / **BLOCKED** | Owner names which author is corresponding; designation also occurs in portal (see C2) | **Yes** |
| A4 | ORCID for **submitting** author (Access: ORCID associated with Author Portal account; publicly visible) | No ORCID string in manuscript; checklist: portal-mandatory for submitting author | **USER_INPUT_REQUIRED** (portal account) | Submitting author ensures ORCID on portal account; optional print in `.tex` is **not** verified as mandatory | **Yes** |
| A5 | Co-author ORCID (if any) | Not in manuscript; Access checklist does **not** state co-author ORCID as mandatory in the article body | **USER_INPUT_REQUIRED** only if owner wants it printed; otherwise optional | Supply if desired; do not invent | **Yes** |
| A6 | Author photographs | Optional when using `IEEEbiographynophoto` (already used) | **SATISFIED** as optional path (no photo required) | None unless owner chooses photos | **Yes** |
| A7 | Funding / acknowledgments | Omitted by comment; none invented | Not a blocker if none exist | Supply only if real funding/acks exist; do not invent | **Yes** |

**Minimal blocker list (user input):** A1 biographies; A2 emails; A3 corresponding-author choice; A4 submitting-author ORCID on portal.

---

## 3. B. MANUSCRIPT / FILE FIX REQUIRED

| # | Exact requirement | Evidence | Current status | Exact action needed | Without scientific content change? |
| --- | --- | --- | --- | --- | --- |
| B1 | \(C=\infty\) must render as infinity, not `C=\{}infty` | **Current** `.tex`: `\texttt{C=}\(\infty\)`. **Current** PDF: `C=∞`. Broken token **absent**. `FINAL_LATEX_BUILD_QA.md` records the format-only fix. Older checklist / `PRE_SUBMISSION_INTEGRITY_AUDIT.md` still say `REVIEW_REQUIRED` — **stale** | **SATISFIED** | None | N/A |
| B2 | No malformed LaTeX that prevents Access compile | Layout repair + build QA: compile SUCCESS; `\EOD` present; refs/cites resolved | **SATISFIED** | None | N/A |
| B3 | No major clipping/overlap that blocks reading of scientific tables | `IEEE_ACCESS_LAYOUT_REPAIR_AUDIT.md`: prior MAJOR defects repaired; remaining = **MINOR_FORMATTING_ISSUES** (cramped cells, float whitespace, wrapped hashes). Not treated as a submission-blocking file defect | **SATISFIED** for blocker purposes (optional polish is **not** recommended here) | None required | N/A |
| B4 | Official Access structural/template placement | `ieeeaccess.cls`; `IEEE_ACCESS_TEMPLATE_PLACEMENT_AUDIT.md`: COMPLETED; FIGURE 1, Eq. (1), Tables 1–11, biographies slots, `\EOD` | **SATISFIED** | None | N/A |
| B5 | Scientifically required figure/equation missing | `FIGURE_EQUATION_NECESSITY_AUDIT.md`: none missing | **SATISFIED** | Do **not** add figures/equations for appearance | N/A |
| B6 | Historical Stage 8 “Stage 9 has NOT been started” wording | Cross-stage audit: Stage-8-time historical boundary; not a current manuscript claim conflict | **Not a submission file blocker** | Do not rewrite historical Stage reports for submission | N/A |

```text
FILE_FIX_REQUIRED = NONE
```

---

## 4. C. PORTAL / SUBMISSION-TIME VERIFICATION

| # | Exact requirement | Evidence | Current status | Exact action needed | Without scientific content change? |
| --- | --- | --- | --- | --- | --- |
| C1 | Graphical abstract / video-as-GA | Checklist: `GRAPHICAL_ABSTRACT = VERIFY_PORTAL_REQUIREMENT`; Submission Checklist does not clearly mandate a GA image; video becomes GA if present | **PORTAL_VERIFY** | Check Author Portal at upload time; do not invent a GA figure in the repo | **Yes** |
| C2 | Corresponding author selected **in the submission system** | Access checklist item 4 (recorded in author-metadata checklist) | **PORTAL_VERIFY** (+ depends on A3) | Designate corresponding author in portal | **Yes** |
| C3 | Submitting-author ORCID on portal account | Same checklist finding | **PORTAL_VERIFY** (+ A4) | Link/public ORCID on account before/at submit | **Yes** |
| C4 | AI-generated-content / AI-use disclosure (IEEE policies evolve) | Not asserted from a fresh web fetch in this audit | **PORTAL_VERIFY** / **VERIFY** | Follow current IEEE Access / Author Portal prompts at submission; do not invent disclosure text here | **Yes** |
| C5 | Portal keywords / subject categories / manuscript type | Manuscript has five Index Terms; portal fields are separate | **PORTAL_VERIFY** | Enter keywords/categories in portal to match manuscript | **Yes** |
| C6 | Template placeholders (`xxxx` dates; sample DOI `10.1109/ACCESS.2024.0429000`; footer `VOLUME 11, 2023`) | PDF p. 1 / class chrome | **PORTAL_VERIFY** / production | IEEE production typically replaces; do not invent a real article DOI now | **Yes** |
| C7 | Upload source `.tex` **and** matching PDF; size limits | Official Access process (prior final-submission audit) | **PORTAL_VERIFY** | Upload consistent pair after metadata insertion + rebuild | **Yes** |

```text
PORTAL_VERIFY = GRAPHICAL_ABSTRACT; CORRESPONDING_AUTHOR_IN_PORTAL; SUBMITTING_AUTHOR_ORCID_ACCOUNT; AI_DISCLOSURE_IF_PROMPTED; PORTAL_KEYWORDS; TEMPLATE_DOI_HISTORY_PLACEHOLDERS; SOURCE_PDF_PAIR_UPLOAD
```

---

## 5. D. ALREADY SATISFIED (do not re-touch)

| Item | Status |
| --- | --- |
| Author names (exact) | **SATISFIED** |
| Affiliation (exact) | **SATISFIED** |
| Official IEEE Access LaTeX class / placement | **SATISFIED** |
| Title, abstract scientific content, Index Terms | **SATISFIED** |
| Sections I–IX structure | **SATISFIED** |
| FIGURE 1 text schematic; Eq. (1); 11 numbered tables | **SATISFIED** |
| References `[1]`–`[34]` / `b1`–`b34` | **SATISFIED** |
| Frozen metrics / TEST n / thresholds / Platt \(a,b\) | **SATISFIED** |
| \(C=\infty\) rendering in **current** review PDF | **SATISFIED** |
| TreeSHAP non-use; Shariah non-certification; no fraud performance; no production/real-time claims | **SATISFIED** |
| Stage 2–10 CLOSED; TEST not reopened | **SATISFIED** |
| Scientific MUST_FIX = none | **SATISFIED** |
| Scientifically required figure/equation = none missing | **SATISFIED** |
| Layout major collisions/clipping repaired | **SATISFIED** (minor remaining = not a blocker) |
| `\EOD` present | **SATISFIED** |
| `IEEEbiographynophoto` **slots** present (bodies empty → A1) | Slot structure **SATISFIED** |

---

## 6. Stale audit labels (not current blockers)

| Stale statement | Where | Current truth |
| --- | --- | --- |
| `C_INFINITY_RENDERING = REVIEW_REQUIRED` | `IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md`; older final-submission / pre-submission integrity notes | Fixed in source + `IEEE_ACCESS_REVIEW_READY.pdf` shows `C=∞` |
| Pre-submission integrity: line 333 still broken token | `PRE_SUBMISSION_INTEGRITY_AUDIT.md` (written before the fix) | Superseded by `FINAL_LATEX_BUILD_QA.md` |
| Final-submission audit PDF = 12-page `IEEE_ACCESS_READY_MANUSCRIPT.pdf` | Older audit | Current review artifact is **13-page** `IEEE_ACCESS_REVIEW_READY.pdf` after layout repair |

Do not re-open scientific content to “fix” these stale labels.

---

## 7. Explicit remaining blockers (minimal)

1. **Biographies** for both authors (manuscript body) — USER_INPUT  
2. **Emails** for portal / corresponding contact — USER_INPUT  
3. **Corresponding-author** choice — USER_INPUT + PORTAL_VERIFY  
4. **Submitting-author ORCID** on Author Portal account — USER_INPUT + PORTAL_VERIFY  

No file-level scientific or typesetting blocker remains for \(C=\infty\), required figures/equations, or major layout collisions.

---

## 8. Recommended next owner step (not performed here)

1. Fill `docs/paper/IEEE_ACCESS_AUTHOR_METADATA_CHECKLIST.md` paste blocks with real bios, emails, corresponding-author choice, ORCID status.  
2. Authorize a **format-only** pass to insert bios / `\corresp` (if desired) **without** changing science.  
3. Rebuild PDF; then complete portal verification items in §4.  

This audit does **not** perform those steps.

---

```text
FINAL_SUBMISSION_BLOCKER_STATUS = READY_FOR_USER_METADATA
USER_INPUT_REQUIRED = AUTHOR_BIOGRAPHIES; AUTHOR_EMAILS; CORRESPONDING_AUTHOR_DESIGNATION; SUBMITTING_AUTHOR_ORCID_PORTAL
FILE_FIX_REQUIRED = NONE
PORTAL_VERIFY = GRAPHICAL_ABSTRACT; CORRESPONDING_AUTHOR_IN_PORTAL; SUBMITTING_AUTHOR_ORCID_ACCOUNT; AI_DISCLOSURE_IF_PROMPTED; PORTAL_KEYWORDS; TEMPLATE_DOI_HISTORY_PLACEHOLDERS; SOURCE_PDF_PAIR_UPLOAD
SCIENTIFIC_FIXES_REQUIRED = NONE
FILES_MODIFIED = docs/paper/FINAL_SUBMISSION_BLOCKER_AUDIT.md ONLY
```

STOP. No other file was modified.
