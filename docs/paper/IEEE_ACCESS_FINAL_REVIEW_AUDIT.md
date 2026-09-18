# IEEE Access Final Review Audit

**Rebuild pass:** journal-quality presentation repair (readability / typography / layout).  
**Scientific freeze:** absolute (no experiments, no metric recalculation, no Stage 9/10 or TEST reopen).

FINAL_IEEE_ACCESS_STATUS = CLEAN

Primary outputs:
- `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex`
- `docs/paper/IEEE_ACCESS_FINAL_REVIEW_READY.pdf` (15 pages; Access trim 576×783 pt)
- Compile directory: `docs/paper/ieee_access_official_templates/latex/ACCESS_latex_template_20260513/` (official fonts/maps)

Prior PDF preserved as `docs/paper/IEEE_ACCESS_FINAL_REVIEW_READY.prev.pdf` before overwrite.

---

## Status Flags

AUTHOR_1_BIO_STATUS = COMPLETE  
AUTHOR_2_BIO_STATUS = COMPLETE  
AUTHOR_EMAIL_STATUS = COMPLETE  
AUTHOR_1_ORCID = NOT_SUPPLIED  
AUTHOR_2_ORCID = NOT_SUPPLIED  
ORCID_INVENTED = NO  
CORRESPONDING_AUTHOR = Aitsam Ul Hassan (aitsamulhassan.awan@gmail.com) — COMPLETE in manuscript `\corresp`  
AI_DISCLOSURE_STATUS = NARROW_FACTUAL_ACKNOWLEDGMENT_INCLUDED  

---

## 1. Metadata / Header Status

| Item | Status |
| --- | --- |
| Fake DOI (article) | ABSENT |
| Fake publication / current-version date | ABSENT |
| Fake VOLUME / year header | ABSENT |
| Sample Access logo / running title | ABSENT |
| Page numbers | Present (footer only) |
| Bibliographic `doi:` fields in References | Present where verified (not article metadata) |

Sample IEEE Access chrome remains suppressed via custom `\@maketitle` / `\ps@headings` / `\ps@titlepage`.

---

## 2. Author / Corresponding-Author Status

| Field | Value | Status |
| --- | --- | --- |
| Author 1 | Aitsam Ul Hassan | EXACT |
| Author 2 | Muhammad Haseeb Ramzan | EXACT |
| Affiliation | Pak-Austria Fachhochschule: Institute of Applied Sciences and Technology, Haripur, Pakistan | EXACT |
| Email 1 | aitsamulhassan.awan@gmail.com | SUPPLIED |
| Email 2 | haseebramzan536@gmail.com | SUPPLIED |
| Corresponding author | Aitsam Ul Hassan (e-mail: aitsamulhassan.awan@gmail.com) | INSERTED via `\corresp` |
| ORCID | none | NOT_SUPPLIED / NOT_INVENTED |

Front page shows title, authors, affiliation, corresponding-author line, abstract, and index terms without collision.

---

## 3. Biography Status

Both biographies use `IEEEbiographynophoto` with **only** owner-supplied facts:

**Aitsam Ul Hassan:** B.S. Computer Science, PAF-IAST / Pak-Austria Fachhochschule, Haripur, 2025; QA Specialist and AI/Data Science Research Intern; data validation, ML evaluation, ETL; interests in ML for financial risk, data quality, AI-driven decision systems.

**Muhammad Haseeb Ramzan:** B.S. Artificial Intelligence, same institution, 2026; Full Stack Developer and AI Engineer; production web apps, REST APIs, ML-backed systems (Python, React, FastAPI, cloud); interests in applied ML for fintech, credit-risk modeling, decision-support systems.

No invented memberships, awards, employers, degrees, ORCID, or photos.

**Layout:** `\clearpage` before biographies so both complete biographies appear together on page 15 (no mid-biography orphan across pages 14–15). Trailing whitespace on page 15 is normal IEEE end-matter for short bios.

---

## 4. Grammar / Typo Corrections (presentation only)

Editorial / clarity fixes applied without changing scientific meaning, including:
- `licence` → `license` (dataset wording)
- Credit-band equation trailing clause cleaned (removed self-referential “as in eq.” phrasing)
- Limitation item updated to reflect **verified** Zenodo creators (no longer “unverified names”)
- Path / URL `\allowbreak` insertions for column-safe wrapping
- Table markup readability (tabularx / controlled `\resizebox` only where full-precision wide panels require it)
- Acknowledgment placed before References (IEEE order)
- Biography capitalization / chronological IEEE phrasing polish

No results, thresholds, claims strength, or limitation substance upgraded.

---

## 5. Citation-Order Audit

`\cite` first-appearance key order matches `\bibitem` order (34 keys).  
IEEE numerical labels therefore appear in first-citation order.  
Apparent gaps such as `[8]–[10]` in PDF text are **citation ranges**, not missing `[9]`.

undefined citations = 0

---

## 6. Claim-to-Citation Audit

Citations remain attached to literature / regulatory / dataset claims they support (credit scoring surveys, calibration, GAMs/SHAP/TreeSHAP distinction, US adverse-action instruments, SBP/SECP/IFSB/AAOIFI identity sources, Zenodo/UCI datasets).  
No citation is used to validate this study’s frozen TEST metrics.  
Sources with incomplete metadata retain honest notes (e.g., Platt DOI none recorded; AAOIFI years UNVERIFIED where applicable).

---

## 7. Reference Metadata Audit

Bibliography visually uniform (author, title, venue, year, volume/pages, DOI/URL where available).  
No fake DOIs or invented authors/dates.  
Where DOI/URL is unavailable, limitation language is retained.

---

## 8. Equation Audit

| Label | Content | Status |
| --- | --- | --- |
| `eq:platt` | Platt map | Intact; `\eqref` used |
| `eq:shap` | Additive centered terms | Intact; `\eqref` used |
| `eq:bands` | Credit-band cases | Intact; sequential numbering |
| Inline | `C=\infty` as `\texttt{C=}\(\infty\)` | Renders as `C=∞` |

No invented equations. No formula changes.

---

## 9. Figure Audit

| Fig. | Role | Asset | Status |
| --- | --- | --- | --- |
| 1 | Evidence-separated workflow | `fig1_architecture.pdf` (regenerated vertical flowchart) | Present |
| 2 | Frozen decision thresholds | `fig3_decision_policy_thresholds.pdf` | Present |
| 3 | M-4B vs distinct M-5 ROC-AUC | `fig2_model_test_roc_auc.pdf` | Present |
| 4 | Stored calibration risk ranges | `fig5_calibration_risk_ranges.pdf` | Present |
| 5 | Additive M-5 attributions | `fig4_global_attribution.pdf` | Present |

No decorative figures. No fabricated reliability diagrams. No fraud visualization. No TreeSHAP in EBM explanation path.  
Figure numbers follow appearance order (automatic).

---

## 10. Workflow Audit (Figure 1)

Figure 1 center path: LendingClub inputs → M-5 TRAIN-only EBM → validation-only Platt → frozen \(p_{\mathrm{selected}}\) → credit bands → G0 → APPROVE / HUMAN_REVIEW / REJECT.  
Right path: additive explanations (not an approval criterion; TreeSHAP not used).  
Left path: Shariah-oriented L1/L2 evidence (governance support, not certification).  
Caption states: research prototype; not production; no fraud layer evaluated.

---

## 11. Table Audit

All tables retained with **unchanged numerals**.  
Wide tables use `table*`. Hash cells use `\sha` wrapping.  
M-5 calibration panels use slight `\resizebox{\linewidth}{!}{...}` only to prevent column overflow while keeping full stored precision readable.  
UCI Table 7 retains ECE `0.20065704943022225` with exploratory note.  
TABLE 9 (G0) remains early via intentional `\setcounter` (documented presentation choice).

---

## 12. Two-Column Layout Audit

| Check | Result |
| --- | --- |
| Clean Access two-column body | YES |
| Text crossing columns | NO (full-width floats only where intended) |
| Figure / table clipping | NO |
| Equation clipping | NO |
| Caption collisions | NO |
| Fake header chrome | NO |
| Forced excessive `\clearpage` body breaks | NO (one `\clearpage` before bios only) |

Ink-density / edge QA on rendered pages: no edge clipping; high mid-gutter ink only on full-width float pages (expected).

---

## 13. Page-by-Page Visual QA

Inspection method: full PDF render (150 dpi) + region crops + text-layer checks + ink/edge heuristics.

| Page | Status | Notes |
| --- | --- | --- |
| Page 1 | CLEAN | Title, authors, emails, `\corresp`, abstract, keywords; no sample metadata |
| Page 2 | CLEAN | Introduction / two-column body |
| Page 3 | CLEAN | Method context |
| Page 4 | CLEAN | Architecture prose |
| Page 5 | CLEAN | Context table + FIGURE 1 workflow |
| Page 6 | CLEAN | TABLE 1 datasets |
| Page 7 | CLEAN | Features / calibration setup |
| Page 8 | CLEAN | FIGURE 2 thresholds + TABLE 9 G0 |
| Page 9 | CLEAN | Experimental protocol |
| Page 10 | CLEAN | TABLES 2–4 + FIGURE 3 ROC |
| Page 11 | CLEAN | TABLES 5–7 + FIGURES 4–5 |
| Page 12 | CLEAN | Discussion / limitations prose |
| Page 13 | CLEAN | TABLES 8, 10, 11 + limitations list |
| Page 14 | CLEAN | Conclusion, Acknowledgment, References |
| Page 15 | CLEAN | Both biographies complete; normal end whitespace |

---

## 14. Scientific Preservation

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

Frozen values verified in PDF text layer:
- `0.6799408767429772`
- `0.6776693941139847`
- `0.20065704943022225`
- `208886`
- `0.06`
- `0.69`
- `0.16`

---

## 15. AI Disclosure Status

Acknowledgment (before References):

> The authors used AI-assisted tools for manuscript formatting and editorial polishing. All scientific results, numerical values, and claims are based on the frozen Stage 2–10 evidence package and were reviewed by the authors. AI tools were not used to generate experimental results, metrics, thresholds, or calibration parameters.

Narrowly factual; does **not** claim AI ran experiments or generated scientific results.  
AI_DISCLOSURE_STATUS = NARROW_FACTUAL_ACKNOWLEDGMENT_INCLUDED  

---

## 16. Remaining User Decisions

| Decision | Status |
| --- | --- | --- |
| ORCID identifiers in manuscript | NOT_SUPPLIED — do not invent |
| IEEE Author Portal ORCID association | Required by IEEE for submitting author; outside this PDF |
| Funding / sponsor footnote | Not supplied; not invented |
| Final portal upload / submission | Not performed |

---

## Cross-Reference Summary

undefined citations = 0  
undefined references = 0  
duplicate labels = 0  
missing figures = 0  
missing tables = 0  
missing equations = 0  
dangling figure/table/equation refs = 0  

---

STOP. Repaired PDF and this audit generated. No submission performed.
