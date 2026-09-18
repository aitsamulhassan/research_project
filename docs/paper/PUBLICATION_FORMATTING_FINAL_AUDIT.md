# Publication Formatting Final Audit

## 1. Overall Status

PUBLICATION_FORMATTING_STATUS = MINOR_ISSUES

Primary deliverables:
- `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` (formatting/presentation edits only)
- `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf` (14 pages; official `ieeeaccess` class)
- Presentation figure assets under `docs/paper/figures/` (`fig1_architecture` added; `fig2`--`fig5` typography polish)

Science, metrics, datasets, calibration, thresholds, Stage 9/10, and TEST remain frozen.

## 2. Equation Audit

| Eq. | Label | Location | Purpose | Status | Cross-reference |
| --- | --- | --- | --- | --- | --- |
| (1) | `eq:platt` | §IV-G (M-5 calibration) | Platt map \(p_{\mathrm{platt}}=\sigma(a\cdot\operatorname{logit}(p_{\mathrm{raw}})+b)\) with frozen \(a,b\) | Numbered display; identical math to prior inline form | Referenced via `\eqref{eq:platt}` |
| (2) | `eq:shap` | §IV-H (Explainability) | Additive SHAP-style logit attribution \(\phi_i(x)=g_i(x_i)-\operatorname{mean}_{\mathrm{TRAIN}}g_i\) | Unchanged formula; notation `\mathrm{TRAIN}` for consistency | Referenced via `\eqref{eq:shap}` in prose and Fig. 5 caption |
| (3) | `eq:bands` | §IV-J (Decision policies) | Credit-band piecewise definition on frozen \(t_{\mathrm{low}},t_{\mathrm{high}}\) | Presentation transform of prior inline LOW/MEDIUM/HIGH prose; values unchanged | Defined in place; thresholds also stated in prose/Fig. 2 |

No new mathematical models, Youden/Brier-skill/fraud/TreeSHAP equations, or invented formulas were added. TreeSHAP remains unused.

## 3. Figure Audit

| Fig. | File | Purpose | Evidence source | Caption | Cross-ref | Placement | Visual |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `figures/fig1_architecture.pdf` | Evidence-separated research-prototype architecture | Manuscript §IV-A layers / executed fusion design (presentation diagram; no new numbers) | Self-contained; research prototype; no fraud layer; not production/certification | `Fig.~\ref{fig:arch}` before float | `figure*` near architecture subsection (appears p. 5) | CLEAN; readable boxes/arrows |
| 2 | `figures/fig3_decision_policy_thresholds.pdf` | Frozen A0 bands vs A3/A4 \(t^*\) | `results/decision/v2/frozen_policy.json` (\(t_{\mathrm{low}}=0.06\), \(t_{\mathrm{high}}=0.69\), \(t^*=0.16\)) | Distinguishes research policy / not origination outcomes | `Fig.~\ref{fig:policy}` | `figure*` (p. 8) | CLEAN |
| 3 | `figures/fig2_model_test_roc_auc.pdf` | Stored TEST ROC-AUC bars (M-4B families + M-5) | `stage4b_test_metrics.json`; `stage5_test_metrics.json` | Separates M-4B vs M-5; frozen ROC-AUC values | `Fig.~\ref{fig:roc}` | `figure*` (p. 10) | CLEAN |
| 4 | `figures/fig5_calibration_risk_ranges.pdf` | Stored risk-range calibration scatter | `results/calibration/tables/stage5_risk_ranges.csv` | Explicitly not the omitted 10-bin ECE diagram | `Fig.~\ref{fig:cal}` | single-column (p. 11) | CLEAN |
| 5 | `figures/fig4_global_attribution.pdf` | Global mean \(\lvert\phi_i\rvert\) | `results/explainability/tables/table1_global_attribution.csv` | Ties to Eq.~\eqref{eq:shap}; TreeSHAP not used | `Fig.~\ref{fig:attr}` | single-column (p. 11) | CLEAN |

No fraud-detector, confusion-matrix, prior-shift, or TreeSHAP figures were invented. No scientific plots were regenerated from raw scores beyond the existing frozen-table presentation assets.

## 4. Table Audit

| Table | Label | Visual status |
| --- | --- | --- |
| I | `tab:t1` | CLEAN (`table*` + wrapping SHA cells) |
| II | `tab:t2` | CLEAN (wrapping paths/SHA; frozen ROC-AUC preserved) |
| III | `tab:t3` | CLEAN |
| IV | `tab:t4` | CLEAN (dense but within margins; small font) |
| V | `tab:t5` | CLEAN |
| VI | `tab:t6` | CLEAN |
| VII | `tab:t7` | CLEAN (ECE note wraps; value `0.20065704943022225` preserved) |
| VIII | `tab:t8` | CLEAN |
| IX | `tab:t9` | CLEAN (single-column G0 matrix near methods; intentional early number via `\setcounter`) |
| X | `tab:t10` | CLEAN |
| XI | `tab:t11` | CLEAN |
| Unnumbered context tabular (M-4B/M-5/M-9.4-*) | — | MINOR: cramped after `\resizebox{\columnwidth}{!}` on p. 4; readable; no column collision |
| Unnumbered protocol / governance treatment tabulars | — | CLEAN within column |

Captions use standard IEEE roman style (bold caption wrappers removed). No scientific rows/columns removed.

## 5. Workflow / Architecture Audit

Fig. 1 matches the **executed / evaluated** evidence-separated prototype:

1. LendingClub inputs → M-5 TRAIN-only EBM + validation-only Platt → \(p_{\mathrm{selected}}\) → credit bands  
2. Additive explanations branch (not an approval criterion; TreeSHAP not used)  
3. Shariah-oriented L1/L2 evidence → L2 status  
4. G0 fusion → APPROVE / HUMAN_REVIEW / REJECT  

Fraud screening was **not** added (no fraud experiment). Caption states research prototype / not production or certification. No deployment claim.

## 6. Cross-Reference Audit

undefined references = 0  
undefined citations = 0  
duplicate labels = 0  
missing figures = 0  
missing tables = 0  

Final log: no undefined references/citations; no multiply-defined labels. PDF text layer contains no `??`. Labels used: `fig:arch`, `fig:policy`, `fig:roc`, `fig:cal`, `fig:attr`, `eq:platt`, `eq:shap`, `eq:bands`, `tab:t1`--`tab:t11` (with intentional TABLE 9 early placement).

## 7. Page-by-Page Visual QA

Inspected all 14 pages of `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf`.

| Page | Status |
| --- | --- |
| Page 1 | CLEAN (title/authors/affiliation/abstract/index terms/two-column opening; template date/DOI placeholders remain by design) |
| Page 2 | CLEAN |
| Page 3 | CLEAN |
| Page 4 | ISSUE: unnumbered five-column context tabular is cramped after column-width fit; no gutter collision |
| Page 5 | CLEAN (Fig. 1 architecture; hashes wrap) |
| Page 6 | CLEAN (TABLE I; Eq. 1) |
| Page 7 | CLEAN (Eq. 2--3; TABLE 9; governance tabular) |
| Page 8 | CLEAN (Fig. 2; protocol tabular) |
| Page 9 | CLEAN (results prose; floats deferred by normal IEEE placement) |
| Page 10 | CLEAN (TABLE II--IV + Fig. 3; dense but no clipping/overlap) |
| Page 11 | CLEAN (TABLE V--VII + Fig. 4--5 side-by-side columns) |
| Page 12 | CLEAN (discussion/limitations) |
| Page 13 | CLEAN (TABLE VIII, X, XI; conclusion; intentional skip VIII→X because TABLE IX earlier) |
| Page 14 | CLEAN (references [1]--[34]; empty `IEEEbiographynophoto` placeholders; ORCID not invented) |

## 8. Scientific Preservation

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

Frozen values verified present unchanged in manuscript/PDF where applicable:  
`0.6799408767429772`, `0.6776693941139847`, `0.20065704943022225`, `208886` / `208,886`, `0.06`, `0.69`, `0.16`.

## 9. Final Recommendation

Additional FORMATTING work is **not objectively necessary** for a coherent IEEE Access two-column presentation. Residual items are optional polish only (cramped unnumbered context tabular on p. 4; naturally dense float pages). No further formatting pass is required to preserve scientific integrity or cross-references.
