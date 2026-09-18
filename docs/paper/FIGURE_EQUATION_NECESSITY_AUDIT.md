# Figure and Equation Necessity Audit

| Item | Value |
| --- | --- |
| **Document ID** | `FIGURE-EQUATION-NECESSITY-AUDIT` |
| **Audit date** | 2026-09-17 |
| **Type** | Diagnosis only — no figures, equations, wording, tables, LaTeX, or PDF added or edited |
| **Review PDF** | `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf` (13 pages) |
| **LaTeX source** | `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` |
| **Web search** | **None** |

Requested path `docs/paper/PAPER_EVIDENCE_INVENTORY.md` was **not found**. Inventory used: `docs/PAPER_EVIDENCE_INVENTORY.md`.

This audit asks whether additional figures or numbered equations are **scientifically required** for the research that was actually performed. It does not treat IEEE visual convention as a requirement.

---

## 1. Current Inventory

Inspected: IEEE Access source, review PDF text layer, `IEEE_MANUSCRIPT.md`, `MANUSCRIPT_DRAFT.md` figure plan, `MANUSCRIPT_EVIDENCE_MAP.md`, prior scientific-reviewer and cross-stage audits, Stage 5–8 reports, and `results/figures/` as they exist on disk.

| Object | Count in current IEEE PDF / source |
| --- | --- |
| Numbered figures | **1** (`FIGURE 1` / `\label{fig1}`) |
| Raster `\includegraphics` figures | **0** |
| Numbered equations | **1** (Eq. (1) in §IV-H) |
| Numbered tables | **11** (`TABLE 1`–`TABLE 11`) |
| Dangling `\ref` to a missing figure or equation | **0** |

**Inline (unnumbered) mathematics already in the manuscript** — not additional numbered equations:

- Platt map: \(\sigma(a \cdot \operatorname{logit}(p_{\mathrm{raw}})+b)\), \(C=\infty\), \(a=1.1988263209549705\), \(b=0.6697765046966161\) (PDF p. 6)
- Credit bands: LOW if \(p < t_{\mathrm{low}}\); HIGH if \(p \ge t_{\mathrm{high}}\); else MEDIUM, with \(t_{\mathrm{low}}=0.06\), \(t_{\mathrm{high}}=0.69\), \(t^{*}=0.16\) (PDF p. 7)

**Manuscript-family references to figures that are not in the IEEE PDF:**

| Reference | Status |
| --- | --- |
| Evidence-map “Fig. 2” = G0 matrix | **Omitted by design.** IEEE `TABLE 9` caption: “The same matrix is not repeated as a separate figure.” No `\ref` to Fig. 2 in the `.tex`. |
| Evidence-map “Fig. 3–4” reliability diagrams | Named in `docs/STAGE_5_CALIBRATION_REPORT.md` §E; **image files not retained**; manuscript states they are omitted and not regenerated. |
| Stage 6 `results/figures/explainability/figure_manifest.json` | Manifest lists 12 stems (`png`/`pdf`); **no matching image files** under `results/figures/explainability/`. |
| Stage 7 `results/figures/shariah/figure_manifest.json` | Manifest lists 2 stems; **no image files**. |
| Stage 8 v1/v2, 9.1, 9.2, 9.3 PNG paths in reports | **Paths named in reports; directories/files not present** in the current `results/figures/` tree (glob of `results/` found **no** `.png`/`.pdf`/`.svg` figure files). |

**NO_EXISTING_VALID_FIGURE_FOUND** for any additional manuscript figure that could be copied in without regeneration or scientific alteration (other than the text schematic already published as FIGURE 1).

---

## 2. Existing Figure Review

### FIGURE 1

| Field | Record |
| --- | --- |
| Number | FIGURE 1 (`\label{fig1}`) |
| Caption | “Evidence-separated research-prototype layers (text schematic; no stored PNG/PDF; no new numbers).” |
| What it represents | A four-row **text table**: Layer / Documented object / Not, for scoring, explainability, governance evidence, and decision fusion. |
| PDF location | Page 5 of `IEEE_ACCESS_REVIEW_READY.pdf` (float). |
| Stage / process | Architecture claim of Stages 7–8 (evidence separation + G0 fusion), with M-5 as the score object. **Not** a dataflow from raw file through TRAIN/VAL/TEST. |
| Scientifically necessary? | **Not required for correctness.** The same four layers are enumerated in §IV-A immediately above the float. |
| Duplicates a table or prose? | **Yes, partially.** It restates the §IV-A numbered list in tabular form. It does **not** duplicate TABLE 9 (G0 cells) or Table VI (counts). |
| Change recommended? | **No.** Already present; not false; caption correctly denies a stored PNG and new numbers. Replacing it with a raster pipeline would be cosmetic or optional comprehension, not a correctness fix. |

No other numbered figure exists in the source or PDF.

---

## 3. Existing Equation Review

### Equation (1)

| Field | Record |
| --- | --- |
| Number | (1) |
| Formal definition | \(\phi_i(x) = g_i(x_i) - \operatorname{mean}_{\mathrm{TRAIN}} g_i\) |
| What it defines | Closed-form additive interventional attribution of feature \(i\) as the TRAIN-centered EBM term on the logit / `decision_function` scale. |
| Where used | §IV-H method bullets; next sentence “In (1), \(g_i\) is…”; results Table V and identity-agreement prose depend on this identity. |
| Surrounding text depends on it? | **Yes.** Without (1), “SHAP-style” could be misread as TreeSHAP or KernelSHAP. The paper’s claim that Spearman \(=1\) is **expected** (not a second-model confirmation) is the direct implication of (1). |
| Scientifically necessary? | **Yes, as already printed.** It is the only formal statement of the executed explanation method. It is **not** missing. |

No other numbered `equation` environment exists in `IEEE_ACCESS_READY_MANUSCRIPT.tex`.

Platt scaling is defined **inline**, not as Eq. (2). That is sufficient (see §5).

---

## 4. Missing Figure Test

Context verified in the manuscript (not assumed to each need a figure): LendingClub; UCI; M-4B EBM; M-5 calibrated EBM; M-9.4-AE; M-9.4-X exploratory UCI XGBoost / `DEVIATION-001`; Platt; validation-derived \(t_{\mathrm{low}}=0.06\), \(t_{\mathrm{high}}=0.69\), \(t^{*}=0.16\); additive EBM explanations; decision-policy simulation / `HUMAN_REVIEW`; Shariah/governance framing; fused A1.

### A. Research workflow / pipeline figure

**Question:** Can dataset → model → calibration → explanation → decision policy → governance interpretation be understood without another figure?

**Yes.** Current carriers:

- Unnumbered context table (M-4B / M-5 / M-9.4-AE / M-9.4-X)
- TABLE 1 (datasets, splits, n)
- §IV-E temporal split; §IV-F M-4B; §IV-G M-5 Platt; §IV-H Eq. (1); §IV-I governance; §IV-J bands + TABLE 9
- §V protocol table (freeze vs exploratory)
- Table VI (A0/A1/A3 counts); Table XI (why A1 has 0 APPROVE)

A box-and-arrow pipeline would **not** add a frozen metric or a missing logical relation. FIGURE 1 already names the four **objects**; the protocol table already names **stage order**.

**Classification: NO_FIGURE_NEEDED**

(A true process diagram would be **category 2 — useful for some readers**, not category 1. It is not classified SCIENTIFICALLY_NECESSARY.)

### B. Model comparison figure (ROC / performance charts)

The paper’s comparison claims are **scalar** TEST metrics after freeze (Table III M-4B families; Table II two EBMs; Table VII UCI with context labels). It does **not** claim a curve-shape, threshold-sweep, or visual dominance result.

ROC/PR plots would **re-encode Table III/VII ranks**. They would not resolve M-4B vs M-5 (that is Table II). They must **not** be used to promote M-9.4-X.

Stored ROC-curve image files: **none found.**

**Classification: NO_FIGURE_NEEDED**  
**NO_EXISTING_VALID_FIGURE_FOUND**

Do not regenerate plots from raw scores.

### C. Calibration figure

Platt is specified inline (form, \(C=\infty\), \(a\), \(b\), `fit_split=validation`). Table IV(a)/(b) reports Brier, log loss, ECE, MCE, ROC-AUC, PR-AUC for raw / Platt / isotonic. Prose states Platt does not change TEST ROC-AUC; 2018 ECE deterioration is numeric.

A reliability diagram would help a reader **see** bin-wise 2018 miscalibration. It is **not** required to understand that Platt was fit on validation only, or to read the stored ECE values. Stage 5 named paths are **not retained** (`results/figures/calibration/` absent). Regenerating from scores is forbidden here and would be a new artifact.

**Classification: NO_FIGURE_NEEDED** (scientific communication of the executed calibration **procedure and stored metrics**)  
**NO_EXISTING_VALID_FIGURE_FOUND**

Optional comprehension (category 2) is recorded in §8. Not MUST_FIX.

### D. Explainability figure

Executed method: Eq. (1) + Table V (mean |attribution| on 5,000 TEST rows) + identity-agreement numbers. TreeSHAP is explicitly unused.

Beeswarm / local / effect-plot **stems** exist in `figure_manifest.json`; **image files do not**. Creating them would be new rendering from the EBM, not a frozen PNG include.

**Classification: NO_FIGURE_NEEDED**  
**NO_EXISTING_VALID_FIGURE_FOUND**

### E. Decision-policy figure

Bands: three inequalities in §IV-J. G0: TABLE 9. Maps A0/A1/A3: bullets + Table VI. `HUMAN_REVIEW` under observed L2: Table XI (all TEST rows `INSUFFICIENT_INFORMATION`). Cost-scenario FN:FP and \(C_{\mathrm{REVIEW}}\) are stated as researcher assumptions.

A number line of \(0.06/0.69/0.16\) would duplicate the inequalities. Stage 8 report PNG paths (cost curves, heatmaps, architecture) are **not on disk**. Several of those were v1/exploratory displays the paper already declined to promote.

**Classification: NO_FIGURE_NEEDED**  
**NO_EXISTING_VALID_FIGURE_FOUND**

---

## 5. Missing Equation Test

Classifications use only what the paper **actually claims**. No formula is invented.

| Concept | What the paper actually does | Classification | Reason |
| --- | --- | --- | --- |
| 1. EBM / additive model | Named InterpretML EBM, `interactions=0`, nine native columns; not a new estimator | **NO_EQUATION_NEEDED** | Training objective is not a contribution. Terms \(g_i\) are introduced under (1). |
| 2. Platt calibration | Inline \(\sigma(a\cdot\operatorname{logit}(p_{\mathrm{raw}})+b)\); unregularized logistic \(C=\infty\); frozen \(a,b\) | **EQUATION_USEFUL_BUT_NOT_REQUIRED** | Already stated completely **without** a numbered environment. Numbering it would not change meaning. |
| 3. ECE | “10 equal-width bins on \([0,1]\); empty bins excluded from ECE and MCE”; values transcribed; [17] cited | **NO_EQUATION_NEEDED** | Paper does not propose a new ECE. Binning rule + stored scalars + citation suffice. A summation formula would restate a standard definition. |
| 4. Threshold policy | \(t_{\mathrm{low}}=0.06\), \(t_{\mathrm{high}}=0.69\), \(t^{*}=0.16\); LOW/MED/HIGH inequalities | **NO_EQUATION_NEEDED** | Piecewise rules are already explicit. |
| 5. HUMAN_REVIEW region | MEDIUM band for A0; G0 cells for A1; simulated research map | **NO_EQUATION_NEEDED** | Discrete policy, not a density or cost-integral contribution in the main claims. |
| 6. Fused A1 logic | TABLE 9: L2 status \(\times\) credit band \(\to\) action | **NO_EQUATION_NEEDED** | The matrix **is** the definition. An indicator-function write-up would duplicate TABLE 9. |
| 7. Attribution / explanation | Numbered Eq. (1) already present | **EQUATION_REQUIRED** as **already included** — not missing | Distinguishes the method from TreeSHAP. |
| 8. Shariah / governance mapping | L1/L2 predicates; TABLE 9; Table XI; no score fusion | **NO_EQUATION_NEEDED** | Mapping is categorical. A formula would fake a Shariah **score**, which the paper refuses. |

No additional numbered equation is **required for scientific correctness**.

---

## 6. Table vs Figure/Equation Redundancy

The manuscript is table-heavy **because the executed claims are tabular**: family metrics, calibration scalars, attribution ranks, policy counts, G0 cells, year mix, L2×band.

| Hypothetical add-on | Relation to existing tables/prose |
| --- | --- |
| ROC overlay | Duplicates Table III / Table VII |
| Grouped bar of A0/A1/A3 | Duplicates Table VI |
| G0 heatmap | Duplicates TABLE 9 (caption already forbids a second figure) |
| Numbered Platt equation | Restates inline prose |
| Numbered ECE sum | Restates a cited standard + binning sentence |
| Numbered A1 case-wise formula | Restates TABLE 9 |
| Extra pipeline figure | Overlaps FIGURE 1 + §IV-A list + §V protocol table |
| Reliability diagram | Does **not** fully duplicate Table IV (bin-wise shape vs scalars) — still **not required** to interpret stored ECE; files absent |
| EBM shape plots | Do **not** fully duplicate Table V (functional form vs mean \|φ\|) — still **not required** given Eq. (1) and the identity disclosure; files absent |

**Tables are already sufficient** for every freeze-backed numeric and policy claim in the paper.

**One figure that could improve comprehension without duplicating evidence:** a **retained** Stage 5 reliability diagram, **if** the original files still existed. They do not. Restoring them would require regeneration (forbidden) or recovery of missing files (not present). Therefore it cannot be recommended as an include-now action.

---

## 7. Reviewer Perspective

**Question:** If a technical reviewer received this paper with 11 tables, 1 figure (text schematic), and 1 equation, would the **absence of additional figures/equations** create a **genuine methodological comprehension problem**?

**No.**

Concrete reasons:

1. **Objects and order** are stated in prose, the context table, FIGURE 1, and the protocol table. A reviewer can list dataset → M-4B family freeze → M-5 TRAIN-only EBM → VAL Platt → Eq. (1) attributions → VAL thresholds → TABLE 9 fusion → Table VI counts.
2. **M-4B vs M-5** is a table problem (Table II), not a missing plot. A ROC figure would not explain two joblibs.
3. **Calibration procedure** is fully specified inline; TEST non-use is explicit; Table IV separates VAL selection from TEST reporting.
4. **Policy reconstruction** uses three inequalities plus a 4×3 matrix (TABLE 9) plus observed occupancy (Table XI). That is how the executed G0 object is defined.
5. **Explanation method** is Eq. (1). Missing beeswarm plots do not prevent understanding that attributions **are** centered EBM terms.
6. **UCI / exploratory XGBoost** are labeled in Table VII; a chart would increase misread risk of ranking M-9.4-X.
7. What a reviewer **may** still dislike is **visual convention** (few plots) or **contribution scale** (A1 evidence-gap), neither of which is caused by a missing formal definition.

This is not an acceptance prediction, score, or ranking.

---

## 8. Scientifically Required vs Useful vs Cosmetic

| Item | Category | Notes |
| --- | --- | --- |
| Eq. (1) as already printed | **1 — REQUIRED FOR SCIENTIFIC CORRECTNESS** of the explanation-method claim | Already in the paper |
| TABLE 9 G0 matrix | **1** (table, not figure) | Already in the paper |
| Table II / IV / VI | **1** (tables) | Already in the paper |
| Additional pipeline flowchart | **2 — USEFUL FOR READER COMPREHENSION** | Not required; overlaps FIGURE 1 |
| Numbered Platt display equation | **2** | Inline form already complete |
| Reliability diagram | **2** | Interpretive aid for ECE; **no valid file**; do not regenerate |
| EBM term-shape / beeswarm | **2** | Interpretive aid; **no valid file**; do not compute new explanations |
| ROC/PR comparison charts | **3 — PURELY COSMETIC** relative to Table III/VII | Not recommended |
| Duplicate G0 figure (old Fig. 2 plan) | **3** | Caption already forbids it |
| Decorative “architecture PNG” | **3** | Stage 8 path not on disk; would not add science |
| ECE summation equation | **2** at most | Standard definition; not a paper contribution |
| Formula for Shariah mapping | **3 / harmful** | Would look like a compliance score; paper correctly uses a discrete matrix |

**MUST_FIX / category 1 missing items: none.**

Category 2 may be discussed as optional later. Category 3 is **not** recommended.

---

## 9. Required Additions, If Any

**NO_SCIENTIFICALLY_REQUIRED_FIGURE_MISSING**

**NO_SCIENTIFICALLY_REQUIRED_EQUATION_MISSING**

No section of the current paper has a scientific relationship that **cannot** be communicated with existing prose, tables, FIGURE 1, Eq. (1), and inline Platt/threshold math.

Therefore there is no “exact section / missing relationship / frozen artifact to include” row for a **required** add. Optional category-2 items (reliability diagram, shape plots, flowchart) either **duplicate** existing carriers or **lack a retained file** and would need new rendering.

Do **not** create them in this task.

---

## 10. Final Classification

FIGURE_STATUS = NO_SCIENTIFICALLY_REQUIRED_FIGURE_MISSING

EQUATION_STATUS = NO_SCIENTIFICALLY_REQUIRED_EQUATION_MISSING

HUMAN_REVIEW_REQUIRED is **not** used: the necessity question is decidable from the actual manuscript, tables, PDF, and the absence of includable image files.

---

```text
SCIENTIFIC_CONTENT_MODIFIED = NO
EXPERIMENTS_RUN = NONE
METRICS_RECALCULATED = NONE
MODELS_CHANGED = NONE
RESULTS_CHANGED = NONE
DATASETS_CHANGED = NONE
CALIBRATION_CHANGED = NONE
THRESHOLDS_CHANGED = NONE
TEST_REOPENED = NO
STAGE_9_REOPENED = NO
STAGE_10_REOPENED = NO
MANUSCRIPT_MODIFIED = NO
PDF_MODIFIED = NO
```

STOP. No other file was modified. No figure or equation was added.
