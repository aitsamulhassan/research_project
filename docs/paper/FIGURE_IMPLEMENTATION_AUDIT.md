# Figure Implementation Audit

| Item | Value |
| --- | --- |
| **Document ID** | `FIGURE-IMPLEMENTATION-AUDIT` |
| **Audit date** | 2026-09-17 |
| **Type** | Comprehension figures from frozen stored evidence only |
| **Source** | `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` |
| **Review PDF** | `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf` |
| **Figure assets** | `docs/paper/figures/` |
| **Builder** | `docs/paper/figures/build_publication_figures.py` (reads CSVs/JSONs; plots only) |

```text
FIGURE_IMPLEMENTATION_STATUS = FIGURES_ADDED_VALIDATED
```

---

## 1. Candidate evidence table (pre-implementation)

| FIGURE CANDIDATE | SOURCE DATA/EVIDENCE | EXACT VALUES AVAILABLE? | NEW SCIENTIFIC COMPUTATION REQUIRED? | SCIENTIFICALLY SAFE? | COMPREHENSION VALUE | DECISION |
| --- | --- | --- | --- | ---: | --- | --- |
| Model TEST ROC-AUC comparison (M-4B families + distinct M-5 EBM) | `results/metrics/stage4b_test_metrics.json`; `results/calibration/metrics/stage5_test_metrics.json` | **Yes** (exact ROC-AUC floats) | **No** (plot stored scalars) | **Yes** if contexts labeled | High | **ADD** |
| 10-bin ECE reliability diagram | Stage 5 report paths; image files absent; no stored 10-bin table | **No** for ECE bins | Would require regenerating bins from scores | **No** as “reliability = ECE bins” | N/A | **SKIP** |
| TEST risk-range mean-predicted vs observed | `results/calibration/tables/stage5_risk_ranges.csv` (TEST) | **Yes** | **No** | **Yes** if caption states it is **not** the omitted 10-bin ECE image | High | **ADD** |
| Decision-policy thresholds | `results/decision/v2/frozen_policy.json` (`t_low=0.06`, `t_high=0.69`, `monolithic_t=0.16`) | **Yes** | **No** | **Yes** (no invented counts) | High | **ADD** |
| End-to-end pipeline (extra) | Existing FIGURE 1 text schematic | Already present | No | Duplicate | Low | **SKIP** |
| Global additive attribution bars | `results/explainability/tables/table1_global_attribution.csv` | **Yes** (matches Table V) | **No** | **Yes**; TreeSHAP not used | High | **ADD** |
| A0/A1/A3 decision-count bars | `results/decision/v2/tables/table3_test_decision_outcomes.csv` | Yes | No | Yes | Medium (duplicates Table VI) | **SKIP** |
| Historical Stage 8/9 PNG paths | Named in reports; files not on disk | No | Would regenerate | No | N/A | **SKIP** |

---

## 2. Final figure inventory

| PDF number | Label | Asset file | Placement |
| ---: | --- | --- | --- |
| FIGURE 1 | `fig1` | Text schematic (tabular; no PNG) | §IV-A Research Architecture |
| FIGURE 2 | `fig:policy` | `figures/fig3_decision_policy_thresholds.pdf` | §IV-J Decision Policies |
| FIGURE 3 | `fig:roc` | `figures/fig2_model_test_roc_auc.pdf` | §VI-A after M-4B family discussion |
| FIGURE 4 | `fig:cal` | `figures/fig5_calibration_risk_ranges.pdf` | §VI-B Calibration Results |
| FIGURE 5 | `fig:attr` | `figures/fig4_global_attribution.pdf` | §VI-C Explainability Results |

Equation (1) retains `\label{eq:shap}` for attribution caption cross-reference only (formula unchanged).

**Total figures:** 5 (1 prior + 4 added).  
**Numbered equations:** still 1.  
**Numbered tables:** still 11 (unchanged cells).

---

## 3. Figures added (exact source evidence)

### FIGURE 2 — Decision-policy thresholds
- **Source:** `results/decision/v2/frozen_policy.json`
- **Values used:** `t_low=0.06`, `t_high=0.69`, `monolithic_t=0.16`
- **Not used:** TEST decision counts (no invented portfolio outcomes)
- **Caption discipline:** research policy; `HUMAN_REVIEW` simulated; not origination; A1 uses G0 (Table 9)

### FIGURE 3 — Model TEST ROC-AUC
- **Sources:** Stage 4B TEST family `roc_auc` (seed 42); Stage 5 TEST `method=platt` `roc_auc`
- **Asserted equals manuscript:** M-4B EBM `0.6799408767429772`; M-5 `0.6776693941139847`
- **Context separation:** first four bars labeled M-4B; fifth bar labeled M-5; caption forbids averaging

### FIGURE 4 — Calibration risk ranges
- **Source:** `results/calibration/tables/stage5_risk_ranges.csv` (written from TEST in Stage 5 runner; stored table only)
- **Points:** raw and Platt `mean_predicted` vs `observed_rate` for five stored ranges
- **Explicitly not:** regenerated 10-bin ECE reliability image; ECE not recomputed

### FIGURE 5 — Global attributions
- **Source:** `results/explainability/tables/table1_global_attribution.csv`
- **Values:** `shap_mean_abs` by feature (identical to centered EBM magnitudes under Eq. 1)
- **Caption:** TreeSHAP not used; not causal; not approval criterion

---

## 4. Candidates skipped (and why)

| Candidate | Why skipped |
| --- | --- |
| 10-bin ECE reliability PNG/PDF | Image files not retained; no stored 10-bin table; regenerating from `p`/`y` would be new bin computation |
| Extra pipeline figure | FIGURE 1 already communicates four layers |
| A0/A1/A3 count bar chart | Exact counts already in Table VI; limited added interpretive value |
| Stage 6 beeswarm / local / effect PNGs | Manifest stems only; image files absent; regenerating would require model reload / new rendering beyond frozen CSV ranks |
| Exploratory cost/governance sensitivity PNGs | Class-C / omitted from main-text rankings by design |

---

## 5. Scientific integrity confirmations

| Check | Result |
| --- | --- |
| Experiments / retraining / TEST reopen / Stage 2–10 reopen | **NONE** |
| Metrics recalculated | **NONE** (plots read stored floats only) |
| Calibration refit / threshold change | **NONE** |
| Table cell values changed | **NO** |
| Equation (1) formula changed | **NO** (label `eq:shap` added only) |
| Authors / affiliation / ORCID | Unchanged; **no ORCID added** |
| References `[1]`–`[34]` | Unchanged |
| M-4B TEST ROC-AUC `0.6799408767429772` | Present in PDF |
| M-5 raw/Platt TEST ROC-AUC `0.6776693941139847` | Present in PDF |
| UCI XGBoost raw ECE `0.20065704943022225` | Present in PDF |
| TEST n `208,886` | Present in PDF |
| `t_low/t_high/t* = 0.06/0.69/0.16` | Present in PDF / Fig. 2 |
| `C=∞` renders correctly | Present in PDF (`C=∞`) |
| TreeSHAP claimed as used | **NO** |
| Shariah certification/compliance claimed | **NO** (denials retained) |
| Fraud-detection performance claimed | **NO** |
| Real-time/production approval claimed | **NO** |
| Every new figure referenced in text | **YES** (`Fig.~\ref{...}`) |
| Orphan figures | **NONE** |

---

## 6. Compilation

| Item | Value |
| --- | --- |
| Compiler | MiKTeX `pdflatex` (2 passes) from official Access template directory |
| Fatal `!` errors | **0** |
| Undefined citations / references | **0** |
| Multiply-defined labels | **0** |
| Output | `IEEE_ACCESS_REVIEW_READY.pdf` |
| **Page count** | **14** (was 13; +1 from four figure floats) |
| PDF size | ≈ 591 KB |

`\graphicspath` updated to resolve `figures/` from `docs/paper/` and `../../../figures/` from the template compile directory.

---

## 7. Files touched (this task)

| Path | Action |
| --- | --- |
| `docs/paper/figures/build_publication_figures.py` | Created (plot builder) |
| `docs/paper/figures/fig2_model_test_roc_auc.pdf` (+ `.png`) | Created |
| `docs/paper/figures/fig3_decision_policy_thresholds.pdf` (+ `.png`) | Created |
| `docs/paper/figures/fig4_global_attribution.pdf` (+ `.png`) | Created |
| `docs/paper/figures/fig5_calibration_risk_ranges.pdf` (+ `.png`) | Created |
| `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` | Figure inserts, `\graphicspath`, `\label{eq:shap}` |
| Template compile copy of the `.tex` | Synced for build |
| `docs/paper/IEEE_ACCESS_REVIEW_READY.pdf` | Rebuilt (14 pages) |
| `docs/paper/FIGURE_IMPLEMENTATION_AUDIT.md` | This file |

**Not modified:** Stage 2–10 result/model/dataset/calibration/threshold artifacts; literature register; author metadata; table numeric cells; bibliography entries.

---

```text
FIGURE_IMPLEMENTATION_STATUS = FIGURES_ADDED_VALIDATED
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
scientific_values_unchanged = YES
```
