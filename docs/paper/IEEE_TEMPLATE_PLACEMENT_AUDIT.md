# IEEE TEMPLATE PLACEMENT AUDIT

| Item | Value |
| --- | --- |
| **Audit ID** | `IEEE-TEMPLATE-PLACEMENT-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Type** | Documentation / formatting / template-placement only |
| **Scientific research** | **CLOSED** |
| **Experiments run** | **NONE** |
| **Models changed** | **NONE** |
| **Results changed** | **NONE** |
| **Data changed** | **NONE** |
| **Stage 9** | **CLOSED** |
| **Stage 10** | **CLOSED** |
| **TEST reopened** | **NO** |
| **Citations invented** | **NO** |
| **Shariah certification claim** | **NO** |
| **Model-context mixing** | **NO** |
| **Human review performed** | **YES** (`docs/paper/M9_4_AE_HUMAN_REVIEW.md`) |
| **Classification source** | `docs/paper/M9_4_AE_HUMAN_REVIEW.md` |
| **Scientific experiment** | **NONE** |
| **Metrics recalculated** | **NONE** |
| **Calibration changed** | **NONE** |
| **Thresholds changed** | **NONE** |
| **New citations** | **NO** |
| **New figures** | **NO** |
| **New tables** | **NO** |
| **Shariah claims added** | **NO** |
| **Scientific content changed** | **NO** (documentation correction of an unsupported **workflow** label only; see below) |
| **AUTHOR_BLOCK_STATUS** | **CONFIRMED_NAMES_AND_AFFILIATION_INSERTED** |

---

## Template availability

TEMPLATE_NOT_FOUND = YES

Searched the repository for:

- `*.tex`, `*.cls`, `*.sty`, `*.bst`, `*.bib`
- `*.docx`, `*.dotx`, `*.doc`
- filenames containing `IEEE`, `IEEEtran`, `template`, `conference`
- `\documentclass`, `IEEEtran`, `ieeeconf`

**Result:** no IEEE Word template, no IEEEtran/LaTeX class, and no conference/journal template files. The only IEEE-named files are manuscript/audit Markdown under `docs/paper/`.

An IEEE template was **not invented**. This pass prepares Markdown that is structurally ordered for later paste into an owner-supplied template.

---

## Files used as source

| Role | Path |
| --- | --- |
| Evidence master (scientific content) | `docs/paper/MANUSCRIPT_DRAFT.md` |
| IEEE wording derivative | `docs/paper/IEEE_MANUSCRIPT.md` |
| Evidence map | `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md` |
| Prior conversion audit | `docs/paper/IEEE_TEMPLATE_CONVERSION_AUDIT.md` |
| Integrity / camera-ready audits | `docs/paper/FINAL_PAPER_INTEGRITY_GATE_AUDIT.md`; `docs/paper/CAMERA_READY_PREPARATION_AUDIT.md` |

---

## Files created / modified

| Path | Action |
| --- | --- |
| `docs/paper/IEEE_TEMPLATE_READY_MANUSCRIPT.md` | **Created** |
| `docs/paper/IEEE_TEMPLATE_PLACEMENT_AUDIT.md` | **Created** (this file) |
| `docs/paper/MANUSCRIPT_DRAFT.md` | **Not modified** |
| `docs/paper/IEEE_MANUSCRIPT.md` | **Not modified** |
| `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md` | **Not modified** |
| Stage 2–10 artifacts / datasets / models / predictions | **Not modified** |

The ready manuscript is the IEEE derivative plus:

1. A **non-paper HTML comment envelope** (`TEMPLATE_NOT_FOUND`, paste order, figure/table/author constraints).
2. IEEE caption punctuation only: `**TABLE I**` → `**TABLE I.**` (and the same period for Tables II–XI). No cells, numerals, or captions-as-science were changed.

---

## Structure check

Paper-body order in the ready file:

Title → author block → Abstract → Index Terms → I. Introduction → II. Related Work → III. Research Gap and Contributions → IV. Methodology → V. Experimental Protocol → VI. Results → VII. Discussion → VIII. Limitations → IX. Conclusion → References.

AUTHOR_BLOCK_STATUS = CONFIRMED_NAMES_AND_AFFILIATION_INSERTED

Author block uses owner-confirmed names and affiliation only: Aitsam Ul Hassan and Muhammad Haseeb Ramzan; Pak-Austria Fachhochschule: Institute of Applied Sciences and Technology, Haripur, Pakistan. Emails, ORCID IDs, department names, author roles, acknowledgments, funding, and corresponding-author lines were **not** invented.

Abstract left at **250 words**. Not re-expanded. No fraud-detection performance, real-time approval, production deployment, Shariah certification, or XGBoost-superiority claims added.

---

## Tables

| Check | Finding |
| --- | --- |
| Content | Preserved from IEEE derivative / master |
| Numbering | I–XI retained (G0 remains Table IX) |
| Captions | Above tables; Roman numerals; period added for IEEE caption style |
| Body references | Unchanged identities |
| Duplicates | Fig. 2 still omitted; Table IX is the G0 matrix |
| Missing | None of I–XI dropped |
| Table II before Table III | **Yes** (Results) |
| Table VII before Table VIII | **Yes** (Results; return sentence to LendingClub TEST) |
| Table IV panels | **(a)** Validation; **(b)** TEST (reporting only) |

---

## Figures

| ID | Status |
| --- | --- |
| Fig. 1 | Text schematic retained (no PNG/PDF created) |
| Fig. 2 | Intentionally omitted (duplicate of Table IX) |
| Reliability diagrams | Absent; **not regenerated** |

No synthetic figures. Tables were not converted into fake figures.

---

## Equations

The existing additive SHAP identity remains display equation (1):

\[\phi_i(x) = g_i(x_i) - \operatorname{mean}_{\text{TRAIN}} g_i.\]

Platt remains inline. No new equations. No formula changes.

---

## References

`[1]`–`[34]` mapping preserved. No DOI, publisher URL, or bibliographic metadata invented. Known unverified fields remain marked in the reference list and Limitations. First-appearance renumbering was **not** applied (would require an actual venue rule plus an auditable permutation).

---

## Numerical integrity (transcription check only)

Compared IEEE wording file against the evidence master. Long floating-point tokens in the IEEE derivative match the master (none extra, none missing). Spot-checked values required by this task:

| Quantity | Value | Present unchanged |
| --- | --- | --- |
| M-4B EBM TEST ROC-AUC | `0.6799408767429772` | Yes |
| M-5 raw/Platt EBM TEST ROC-AUC | `0.6776693941139847` | Yes |
| UCI exploratory XGBoost raw ECE (M-9.4-X) | `0.20065704943022225` | Yes |
| LendingClub TEST \(n\) | `208886` | Yes |
| \(t_{\text{low}}\) | `0.06` | Yes |
| \(t_{\text{high}}\) | `0.69` | Yes |
| \(t^{*}\) | `0.16` | Yes |

No replacements were calculated. Values were not rounded to collapse M-4B vs M-5.

---

## Model provenance (not mixed)

| Context | Treatment preserved |
| --- | --- |
| **M-4B** | LendingClub family TEST after TRAIN+VALIDATION refit; EBM TEST ROC-AUC `0.6799408767429772`; not used from fusion onward |
| **M-5** | TRAIN-only EBM + validation-only Platt; downstream `p_selected` lineage; TEST ROC-AUC `0.6776693941139847` |
| **M-9.4-AE** | independent UCI logistic-regression + EBM methodology |
| **M-9.4-X** | UCI XGBoost exploratory / `DEVIATION-001` |

LendingClub XGBoost (M-4B) and UCI XGBoost (M-9.4-X) remain unmerged.

### M-9.4-AE human-review gate (closed; documentation correction only)

Classification source: `docs/paper/M9_4_AE_HUMAN_REVIEW.md`.

**Authoritative classification (frozen artifacts; not the later placement-task instruction):**

- **M-9.4-AE:** independent UCI logistic-regression + EBM methodology
- **M-9.4-X:** UCI XGBoost exploratory / `DEVIATION-001`

A prior placement-task STEP 9 phrase, “M-9.4-AE = UCI exploratory analysis context,” is **unsupported** and is **not** the current classification. It is retained here only as the withdrawn workflow label. It was **not** present as a scientific claim in the evidence master, evidence map, IEEE manuscript, or ready-manuscript paper body. Those files already used independent methodology (AE) vs exploratory XGBoost (X).

Human review performed = YES. No manuscript or Stage 9 artifact was rewritten to apply the withdrawn label. `DEVIATION-001` remains attached to **M-9.4-X** (UCI XGBoost), not to M-9.4-AE.

---

## Shariah / legal wording check

The paper does **not** state that the system is Shariah-certified, that applicants are Shariah-compliant or non-compliant, that AAOIFI/SBP/SECP certify the prototype, that `INSUFFICIENT_INFORMATION` is a Shariah ruling, or that the model determines halal/haram status (`halal` / `haram` do not appear).

It states the documented research-prototype / evidence-gap position, including that `INSUFFICIENT_INFORMATION` is **not** a finding of applicant or contract non-compliance. SECP language that a security shall not be called Shariah compliant without a Commission certificate is cited as a **prohibition**, not as a certification of this prototype.

---

## Limitations still visible

- Reliability-diagram image files are not retained
- M-4B / Stage 4B family ECE (including LR) is not stored
- UCI family-raw LR/EBM ECE is not stored
- Bibliographic metadata limitations (Platt DOI/URL, Zenodo creators, AAOIFI years, IFSB-10 FAQ-not-full-body, Guo DOI NONE)
- LendingClub lacks contract-level Shariah fields
- Governance layer is a research prototype / evidence-gap mechanism
- UCI is not validation of LendingClub
- UCI XGBoost is exploratory
- No production / real-time deployment claim

---

## Remaining presentation / documentation limitations

1. **No actual IEEE template** — cannot produce IEEEtran/Word camera-ready pagination, two-column layout, or IEEE PDF.
2. Email / ORCID / acknowledgments / funding / corresponding-author lines remain omitted (not supplied). Author names and affiliation have been inserted from owner-confirmed text.
3. Target venue unknown.
4. Citation numbers follow the master identity map, not first-appearance order.
5. Table bodies still appear as I → IX → II… because Table IX (G0) lives in Methodology; Results order II-before-III and VII-before-VIII is already corrected.
6. Fig. 1 remains a text schematic, not a venue graphic.
7. Reliability diagrams remain omitted.
8. Conclusion still uses the master phrase “APPROVE / REVIEW / REJECT” for the same stored counts labeled `HUMAN_REVIEW` in tables. Not rewritten (would be a wording judgment, not a required template rule).
9. M-9.4-AE vs M-9.4-X classification: human-review gate **closed**. M-9.4-AE = independent UCI logistic-regression + EBM methodology. M-9.4-X = UCI XGBoost exploratory / `DEVIATION-001`. The placement-task phrase “UCI exploratory analysis context” for M-9.4-AE is withdrawn (documentation correction only). See `docs/paper/M9_4_AE_CORRECTION_LOG.md`.

---

experiments run = NONE  
models changed = NONE  
results changed = NONE  
data changed = NONE  
calibration changed = NONE  
thresholds changed = NONE  
Stage 9 = CLOSED  
Stage 10 = CLOSED  
TEST reopened = NO  
citations invented = NO / new citations = NO  
new figures = NO  
new tables = NO  
Shariah certification claim = NO / Shariah claims added = NO  
model-context mixing = NO  
scientific content changed = NO  
Scientific experiment = NONE  
Metrics recalculated = NONE  
Human review performed = YES  
Classification source = `docs/paper/M9_4_AE_HUMAN_REVIEW.md`  

M-9.4-AE = independent UCI logistic-regression + EBM methodology  
M-9.4-X = UCI XGBoost exploratory / DEVIATION-001  

FINAL_PLACEMENT_STATUS = READY_FOR_OWNER_SUPPLIED_IEEE_TEMPLATE

Not camera-ready submission. Actual IEEE template placement was **not** started in this correction.
