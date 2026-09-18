# CAMERA-READY PREPARATION AUDIT

| Item | Value |
| --- | --- |
| **Audit ID** | `CAMERA-READY-PREPARATION-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Type** | Formatting / presentation / consistency only |
| **Scientific research** | **CLOSED** (Stages 2–10 frozen) |
| **Manuscript** | `docs/paper/MANUSCRIPT_DRAFT.md` |
| **Experiments / recomputes** | **None** |
| **Stage 2–10 artifacts modified** | **No** |
| **Requested but not found** | `docs/paper/FINAL_ACADEMIC_WRITING_POLISH_AUDIT.md` (**NOT FOUND**) |
| **Final status** | **READY_WITH_DOCUMENTATION_LIMITATIONS** |

This audit asks whether the current manuscript is structurally and visually ready to be placed in a formal publication template. It does **not** reopen science. It does **not** choose an IEEE venue. No reliability-diagram images were generated.

Narrow presentation-only edits applied in this pass (no metric changes):

1. Table X column header `REVIEW` → `HUMAN_REVIEW` (same stored `n_review` counts; avoids confusion with L2 status `REVIEW`).
2. Table II M-5 SHA-256 expanded from the truncated form to the full hash already transcribed in §7.7.
3. Draft header `Type` line updated to the current manuscript state.

---

## A. Structural status

The draft is a complete IEEE-**style** Markdown manuscript, not an IEEEtran source file.

### Current section map

| Draft heading | Role | IEEE-body analogue |
| --- | --- | --- |
| Front-matter metadata table + drafting note | Repository wrapper | Strip before template |
| ## 1. Title | Title (duplicated: also the `#` heading) | Front matter, not a numbered body section |
| ## 2. Abstract | Abstract | Front matter |
| ## 3. Keywords | Keywords / index terms | Front matter |
| ### Table and figure plan | Drafting apparatus | Strip before template |
| ## 4. Introduction | Introduction | I. Introduction |
| ## 5. Related Work | Related work | II |
| ## 6. Research Gap and Contributions | Gap / contributions | III or end of Introduction |
| ## 7. Methodology | Methods | IV |
| ## 8. Experimental Protocol | Protocol / authorization classes | Methods or appendix |
| ## 9. Results | Results | V |
| ## 10. Discussion | Discussion | VI |
| ## 11. Limitations | Limitations | Discussion or separate |
| ## 12. Conclusion | Conclusion | VII |
| ## 13. References | References | Bibliography |
| ## Drafting close | Repository wrapper | Strip before template |

The roadmap in §4 correctly points to Sections 5–13 of **this** numbering. That numbering is internally consistent. It is **not** IEEE body numbering (where Abstract is unnumbered and Introduction is Section I).

**Do not rewrite the scientific structure** merely to force a template. Remap heading levels only during template conversion.

| Check | Finding |
| --- | --- |
| Missing scientific sections | None of Title, Abstract, Keywords, Introduction, Related Work, Gap/Contributions, Methodology, Protocol, Results, Discussion, Limitations, Conclusion, References is empty or missing |
| Duplicate scientific sections | None |
| Empty sections | None |
| Misplaced sections | Results table **appearance order** is not numeric (see §C) |
| Inconsistent numbering | Body uses Arabic 4–13; Title/Abstract/Keywords occupy 1–3; IEEE conversion must demote 1–3 to front matter |
| Author / affiliation / email | **Absent** (correct: do not invent) |
| Acknowledgments | **Absent** (add only if a venue requires it and the owner supplies text) |

**STRUCTURE_STATUS = COHERENT_MARKDOWN_DRAFT_NOT_IEEE_SOURCE**

---

## B. Figure status

| ID | What it is | Image file | Caption | Referenced in text | Unique? | Claimed as included PNG? |
| --- | --- | --- | --- | --- | --- | --- |
| Fig. 1 | Text schematic of four layers + a layer table | **No** (`results/` has no PNG/PDF/SVG) | Yes: “text schematic; Not a stored PNG/PDF” | Yes (§7.1) | Yes | **No** (correctly denied) |
| Fig. 2 | Captioned copy of the G0 matrix (same cells as Table IX) | **No** | Yes: “No separate image file” | Yes (§7.1, §7.10) | Yes as a figure number | **No** (correctly denied) |
| Stage 5 reliability diagrams | Named in Stage 5 report as `figure1_validation_reliability` / `figure2_test_reliability` | **NOT RETAINED** | Omission stated in the figure plan, §9.2, and Limitation 30 | Named as omitted | N/A | **No** — not described as included |

No Fig. 3+ is claimed. Optional 9.2/9.3 displays are explicitly omitted.

**Do not regenerate reliability diagrams.** They remain a documentation limitation.

Other figure issues (presentation, not missing science):

- Fig. 2 and Table IX are the **same G0 matrix**. Camera-ready conversion should keep one numbered float (table or figure), not both, unless the venue wants a graphic.
- Fig. 1 is a Markdown table, not a vector graphic. Template conversion needs a drawn schematic **only if** the venue requires graphics; a table of layers is evidence-supported and must not invent architecture.

**FIGURE_STATUS = TEXT_SCHEMATICS_ONLY_RELIABILITY_OMITTED**

---

## C. Table status

Eleven uniquely numbered tables: I–XI. All have captions. All have a stored source in the figure/table plan. Model contexts in metric tables are labeled.

| ID | Caption location | First numeric appearance order in §9 | Context separation | Source |
| --- | --- | --- | --- | --- |
| I | §7.3 | (methods) | LC vs UCI; German/Australian excluded | Inventory / Stage 2 / split manifests |
| II | §9.1 **after** Table III | 2nd in Results | M-4B vs M-5 columns | Stage 4B/5 JSON |
| III | §9.1 | 1st in Results | M-4B only; LC XGBoost labeled “LC only” | `stage4b_test_metrics.json` |
| IV | §9.2 | 3rd | M-5 only; VAL vs TEST stacked | Stage 5 JSON |
| V | §9.3 | 4th | M-5 explainability sample | `table1_global_attribution.csv` |
| VI | §9.4 | 5th | Frozen `p_selected` maps | v2 table3 |
| VII | §9.5 **after** Table VIII | 7th in Results | M-9.4-AE vs M-9.4-X labeled; ECE provenance noted | family-raw CSV + calibration CSV raw |
| VIII | §9.4 | 6th in Results | Credit bands on same TEST | table3b |
| IX | §7.10 (with Fig. 2) | (methods) | G0 fusion; not a score table | Stage 8 v2 §B |
| X | §9.6 | 8th | Post-hoc year mix | `s10_r1_year_decision_mix.csv` |
| XI | §9.6 | 9th | S10-A1 gap; not a Shariah ruling | `s10_a1_gap_crosstab.csv` |

**No table merges M-4B, M-5, M-9.4-AE, and M-9.4-X into one experiment.** Table II is explicitly a two-identity comparison. Table VII labels UCI rows by context.

Unnumbered Markdown tables (not I–XI): front-matter metadata; figure/table plan; §7 context-ID table; Fig. 1 layer table; §7.9 four-way Shariah table; §8 stage-authorization table. These are fine in the draft; IEEE conversion should either number them or keep them as in-text lists.

Table IV is **one caption, two grids** (validation and TEST). Template conversion should use subtables or a single float with a panel note. TEST is labeled “reporting only.”

**IMPORTANT:** Results appearance order is III → II → IV → V → VI → VIII → VII → X → XI. Numbers are unique but not sequential on the page. Do **not** invent new tables to fill the sequence; reorder existing floats in the formatting pass.

**TABLE_STATUS = COMPLETE_WITH_NONSEQUENTIAL_RESULTS_ORDER**

---

## D. Equation status

| Equation | Form | Numbered? | Symbols |
| --- | --- | --- | --- |
| Platt map | Inline: \(\sigma(a \cdot \operatorname{logit}(p_{\text{raw}}) + b)\) | No | \(a,b\) given from `selected_calibration.json`; \(p_{\text{raw}}\) named |
| Additive SHAP | Display: \(\phi_i(x) = g_i(x_i) - \operatorname{mean}_{\text{TRAIN}} g_i\) | No | Matches Stage 6; \(g_i\) = EBM term |
| Thresholds | \(t_{\text{low}}\), \(t_{\text{high}}\), \(t^{*}\), \(C_{\text{REVIEW}}\) | N/A | Defined in §7.10 before use in Results |

No duplicated equation numbers (none are numbered). No malformed `\[ \]` block found. Meaning was not changed in this audit.

IEEE conversion may add `(1)` / `(2)` without altering formulas. **Do not introduce new equations.**

**EQUATION_STATUS = UNNUMBERED_BUT_DEFINED**

---

## E. Citation / reference status

- In-text `[1]`–`[34]` each have a bibliography entry.
- Bibliography `[1]`–`[34]` is consecutive; no skip; no duplicate numbers.
- `[30]` is cited in §5.7 and §7.9.
- Register source `SRC-AAOIFI-SS-INDEX` remains unused (disclosed after the list).
- Roadmap “Section 5 … Section 13” matches current headings.
- “Section 4” in Discussion refers to the Introduction (where the design question sits) — consistent with **this** numbering, not IEEE “Section I.”
- Stage 11 is mentioned only as **not started** (§8). No reference to a Stage 11 result.
- No citation of a nonexistent figure.

Unverified fields are still marked, not filled: Platt `[14]`; Zenodo creators `[20]`; AAOIFI `[28]`/`[29]` years/clauses; `[29]` URL; IFSB-10 `[31]` FAQ vs full body; `[17]` DOI field NONE.

**REFERENCE_STATUS = INTERNALLY_CONSISTENT_UNVERIFIED_FIELDS_PRESERVED**

---

## F. Numerical consistency (transcription only; not recomputed)

| Quantity | Occurrences | Match to stored artifact? |
| --- | --- | --- |
| M-4B EBM TEST ROC-AUC `0.6799408767429772` | Table III, Table II, Discussion | Yes — `stage4b_test_metrics.json` |
| M-5 raw/Platt TEST ROC-AUC `0.6776693941139847` | Abstract, Table II, Table IV, Discussion, Conclusion | Yes — `stage5_test_metrics.json` |
| UCI XGBoost selected-family raw ECE `0.20065704943022225` | Table VII + note | Yes — `uci_test_calibration.csv` `method=raw` |
| LC full file 1,347,681; splits 941,267 / 197,528 / 208,886 | Abstract, §7.2, Table I | Yes — Stage 2 / split manifest |
| A0/A1/A3 counts 5232 / 203627 / 27; 0 / 208859 / 27; 61855 / 0 / 147031 | Abstract, Table VI, Conclusion | Yes — v2 table3 |
| Table XI 5232+203627=208859 | §9.6 algebra of stored cells | Same stored cells; not a new TEST metric |
| S10-R1 2017 n=152726 / 2018 n=56160 and mix counts | Table X | Yes — `s10_r1_year_decision_mix.csv` |
| Platt \(a,b\) | §7.7 | Yes — `selected_calibration.json` |
| M-5 joblib SHA-256 | §7.7 and Table II (now identical full string) | Yes — inventory / Stage 5 |
| Seed 42 | M-4B TEST, M-5, UCI, SHAP sample | Consistent with artifacts |

**Format variants of the same integers (not different values):** `208886` vs `208,886` vs `208{,}886`; `5232` vs `5,232`; `n=5000` vs \(n=5{,}000\). Template conversion should pick one grouping style.

Stage 4B rounded prevalences 18.7% / 24.9% / 21.2% vs M-5 exact TEST prevalence `0.2117901630554465` are **already labeled** as Stage 4B descriptive rounding vs stored M-5 prevalence. Not a silent discrepancy.

**NUMERICAL_CONSISTENCY = CONSISTENT_TRANSCRIPTION_FORMAT_VARIANTS_ONLY**

---

## G. Model-provenance presentation

| Context | How tables present it | Verdict |
| --- | --- | --- |
| M-4B | Table III; Table II left column; LC XGBoost “LC only” | Separate |
| M-5 | Table II right column; Table IV; downstream `p_selected` | Separate; Stage 8 uses M-5, not M-4B dump |
| M-9.4-AE | Table VII LR/EBM; ECE “not stored” | Separate |
| M-9.4-X | Table VII XGBoost row + exploratory selected pipeline | Exploratory; not merged with LC XGBoost |

**MODEL_PROVENANCE_PRESENTATION = SEPARATED**

---

## H. Shariah wording status

Headings use “Shariah-Oriented Governance.” Fig. 2 / Table IX caption states `INSUFFICIENT_INFORMATION` is not converted to `PASS` or to religious non-compliance. Table XI is captioned “not a Shariah ruling.”

No caption or table introduces certification, fatwa-as-result, Shariah-certified loan, compliant/non-compliant applicant, or legally compliant Islamic lending. Fatwa/certification appear only as **denials**.

**SHARIAH_PRESENTATION = WITHIN_PROTOTYPE_BOUNDS**

---

## I. Limitation visibility

| Required limitation | Where visible |
| --- | --- |
| 1. Stage 5 reliability diagrams not retained | Figure plan; §9.2; Limitation 30 |
| 2. Stage 4B ECE not stored | §9.1; Limitation 18 |
| 3. UCI LR/EBM family-raw ECE not stored | Table VII; Limitation 18 |
| 4. Unverified bibliographic fields | §5.3; §7.2; Limitation 25; reference notes on [14][17][20][28][29][31] |
| 5. Stage 6 provenance discrepancy | §7.8; Limitation 21 |
| 6. LC lacks contract-level Shariah fields | Abstract; §7.2; §7.9; Limitation 24; Conclusion |
| 7. German / Australian literature-only | §4; §5.1; Table I caption; [22][23] notes |
| 8. UCI XGBoost exploratory | Abstract; §6; Table VII; Limitation 6; Conclusion |
| 9. Stage 10 descriptive/non-confirmatory | §8 table; §9.6; Limitations 7–8, 29 |

Limitations are not hidden for presentation.

**LIMITATIONS_VISIBLE = YES**

---

## J. Title status

**Current manuscript title:**

> Evidence-Separated Credit Scoring, Additive Explainability, and Shariah-Oriented Governance: A Research Prototype on a LendingClub Extract, with Independent UCI Methodology Context

This matches executed work: LC primary extract, UCI methodology context, prototype governance, no fraud result, no real-time engine.

**FYP / project working title** (“AI-Driven Risk Assessment, Fraud Detection, and Real-Time Loan Approval System”) **overclaims** the executed evidence (no fraud experiment; no latency/throughput study; not production approval). **Do not use it as the camera-ready paper title.**

This audit does **not** silently replace the manuscript title. Recommended action: keep the current research title (or a shortened venue variant of it), not the FYP title.

**TITLE_STATUS = CONSISTENT_WITH_EXECUTED_EVIDENCE_DO_NOT_USE_FYP_TITLE**

---

## K. Template readiness

Ready to **place content** into a standard IEEE-style template **after** a formatting conversion pass. Not already in IEEEtran.

| Template element | Present in Markdown? | Action at conversion |
| --- | --- | --- |
| Title | Yes (twice: `#` and §1) | Use once |
| Author / affiliation / email | No | Owner-supplied placeholders only; **do not invent** |
| Abstract | Yes (long) | Compress if venue has a word cap; do not add claims |
| Keywords | Yes; “Index Terms—See Keywords” is a pointer | Merge into IEEE `\IEEEkeywords` |
| Numbered body sections | Arabic 4–13 | Remap to I, II, … if the template requires it |
| Figures | Two text schematics; no PNG | Keep as table/schematic or redraw **without new numbers** |
| Tables | I–XI | Reorder floats; split Table IV panels if needed |
| Equations | Unnumbered | Optional `(1)` `(2)` |
| References | `[1]`–`[34]` | BibTeX mapping from register; keep UNVERIFIED notes |
| Acknowledgments | No | Only if required and supplied |

**TEMPLATE_READINESS = CONTENT_PLACEABLE_AFTER_FORMATTING_PASS**

---

## L. Page-limit awareness

No target venue or page limit is known. **Do not claim the draft meets a page limit.**

| Approximate size (Markdown, not IEEE two-column pages) | Estimate |
| --- | --- |
| File length | ~740 lines |
| Abstract | Four paragraphs; on the order of **500+ words** (typical IEEE abstract is much shorter) |
| Numbered figures | 2 (text-only) + 0 image files |
| Numbered tables | 11 |
| References | 34 |
| Display equations | 1 (+ inline Platt form) |

Sections most likely to need compression **if** a short conference limit is later chosen (do not shorten now):

- Abstract
- §8 Experimental Protocol (authorization classes could move to a supplement)
- §11 Limitations (30-item list)
- Full-precision metric tables (rounding is a later presentation choice; do not round here)
- Duplicate G0 as both Fig. 2 and Table IX

---

## M. Remaining blockers

### CRITICAL

None for **scientific** camera-ready conversion. Reliability diagrams are omitted on purpose. No claimed missing figure. No broken `[n]` citation. No model-context merge in tables.

### IMPORTANT (formatting pass)

1. Strip repository wrappers: metadata table, table/figure plan, drafting-close block.
2. Remap §1–3 (Title/Abstract/Keywords) to IEEE front matter; remap body 4–12 to I–… if the template requires it.
3. Reorder Results floats so Table II appears before Table III and Table VII before Table VIII **without changing values**.
4. Resolve Fig. 2 / Table IX duplication (one float).
5. Table IV: two grids, one caption — convert to subtables or one labeled float.
6. Abstract length vs typical IEEE abstract caps.
7. No author/affiliation block — must be supplied by the owner, not invented.
8. Integer grouping style (`5232` vs `5,232`) should be unified in the template.
9. `docs/paper/FINAL_ACADEMIC_WRITING_POLISH_AUDIT.md` was listed as an authoritative file and is **not in the repository**.

### MINOR

1. Unnumbered in-text tables.
2. Equations unnumbered.
3. “Index Terms—See Keywords.”
4. Hash previously truncated in Table II (corrected in this pass).
5. Table X `REVIEW` header (corrected in this pass to `HUMAN_REVIEW`).
6. Optional acknowledgments.

### DOCUMENTATION_ONLY

- Stage 5 reliability images remain unavailable.
- Stage 4B / UCI LR–EBM ECE remain not stored.
- Unverified bibliographic metadata remain unmarked-complete.
- Stage 6 opening-sentence discrepancy remains disclosed.
- FYP working title remains unsuitable as the paper title.
- Protocol/inventory files still say paper drafting `NOT STARTED` (lag; out of experimental scope).

---

## 16. No scientific changes

```text
NEW_EXPERIMENTS = NO
NEW_METRICS = NO
NEW_MODELS = NO
NEW_DATA = NO
TEST_REOPENED = NO
THRESHOLDS_CHANGED = NO
CALIBRATION_CHANGED = NO
STAGE_2_TO_10_RESULTS_CHANGED = NO
```

---

## 17. Final status

**READY_WITH_DOCUMENTATION_LIMITATIONS**

Not `READY_FOR_FORMATTING`: the file is still a repository Markdown draft with meta scaffolding, nonsequential table order, text-only figures, no author block, and known omitted images.

Not `NOT_READY`: structure is complete, citations resolve, tables are sourced, model contexts stay separate, Shariah bounds hold, and limitations remain visible.

```text
CAMERA_READY_PREPARATION = COMPLETE

STRUCTURE_STATUS = COHERENT_MARKDOWN_DRAFT_NOT_IEEE_SOURCE
FIGURE_STATUS = TEXT_SCHEMATICS_ONLY_RELIABILITY_OMITTED
TABLE_STATUS = COMPLETE_WITH_NONSEQUENTIAL_RESULTS_ORDER
EQUATION_STATUS = UNNUMBERED_BUT_DEFINED
REFERENCE_STATUS = INTERNALLY_CONSISTENT_UNVERIFIED_FIELDS_PRESERVED
NUMERICAL_CONSISTENCY = CONSISTENT_TRANSCRIPTION_FORMAT_VARIANTS_ONLY
MODEL_PROVENANCE_PRESENTATION = SEPARATED
SHARIAH_PRESENTATION = WITHIN_PROTOTYPE_BOUNDS
LIMITATIONS_VISIBLE = YES
TITLE_STATUS = CONSISTENT_WITH_EXECUTED_EVIDENCE_DO_NOT_USE_FYP_TITLE
TEMPLATE_READINESS = CONTENT_PLACEABLE_AFTER_FORMATTING_PASS
CRITICAL_BLOCKERS = NONE
IMPORTANT_BLOCKERS = META_SCAFFOLDING; SECTION_REMAP; TABLE_ORDER; FIG2_TABLE_IX_DUPLICATE; TABLE_IV_PANELS; LONG_ABSTRACT; NO_AUTHOR_BLOCK; INTEGER_GROUPING; MISSING_POLISH_AUDIT_FILE
MINOR_BLOCKERS = UNNUMBERED_EQUATIONS; INDEX_TERMS_POINTER; OPTIONAL_ACKNOWLEDGMENTS

NEW_EXPERIMENTS = NO
NEW_METRICS = NO
NEW_MODELS = NO
NEW_DATA = NO
TEST_REOPENED = NO
STAGE_2_TO_10_RESULTS_CHANGED = NO

FINAL_STATUS = READY_WITH_DOCUMENTATION_LIMITATIONS
NEXT_ACTION = Template conversion pass only: strip wrappers, remap headings if the venue requires it, reorder existing floats, keep omitted reliability diagrams omitted, do not invent authors/DOIs/figures; do not start Stage 11
```

```text
FILES_CREATED = docs/paper/CAMERA_READY_PREPARATION_AUDIT.md
FILES_MODIFIED = docs/paper/MANUSCRIPT_DRAFT.md
PRESENTATION_EDITS = Table_X_HUMAN_REVIEW_header; Table_II_full_M-5_hash; draft_Type_line
EXPERIMENTAL_ARTIFACTS_MODIFIED = NO
```
