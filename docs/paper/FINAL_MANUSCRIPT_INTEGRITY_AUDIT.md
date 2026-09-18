# FINAL MANUSCRIPT INTEGRITY AUDIT

| Item | Value |
| --- | --- |
| **Audit ID** | `FINAL-MANUSCRIPT-INTEGRITY-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Type** | Pre-template integrity audit **only** |
| **Ready manuscript** | `docs/paper/IEEE_TEMPLATE_READY_MANUSCRIPT.md` |
| **Experiments / recomputes** | **None** |
| **Manuscripts rewritten** | **No** |
| **IEEE template placement started** | **No** |

FINAL_MANUSCRIPT_INTEGRITY_STATUS = PASS_WITH_DOCUMENTATION_NOTES

AUTHOR_BLOCK_STATUS = PASS

SCIENTIFIC_CONTENT_STATUS = UNCHANGED

EXPERIMENT_STATUS = NONE_RUN

STAGE_2_10_STATUS = UNCHANGED

TEST_STATUS = NOT_REOPENED

M9_4_AE_STATUS = INDEPENDENT_UCI_LOGISTIC_REGRESSION_AND_EBM

M9_4_X_STATUS = EXPLORATORY_UCI_XGBOOST_DEVIATION_001

SHARIAH_CLAIM_STATUS = NO_CERTIFICATION_OR_COMPLIANCE_CLAIM

REFERENCE_STATUS = PRESERVED

KEY_VALUE_STATUS = MATCH

This audit does **not** start IEEE template placement.

---

## Files read

| File | Role |
| --- | --- |
| `docs/paper/IEEE_TEMPLATE_READY_MANUSCRIPT.md` | Placement-ready manuscript |
| `docs/paper/IEEE_MANUSCRIPT.md` | IEEE wording derivative |
| `docs/paper/MANUSCRIPT_DRAFT.md` | Evidence master |
| `docs/paper/MANUSCRIPT_EVIDENCE_MAP.md` | Claim-to-artifact map |
| `docs/PAPER_EVIDENCE_INVENTORY.md` | Evidence inventory |
| `docs/paper/IEEE_TEMPLATE_PLACEMENT_AUDIT.md` | Placement audit |
| `docs/paper/M9_4_AE_HUMAN_REVIEW.md` | M-9.4-AE review |
| `docs/paper/M9_4_AE_CORRECTION_LOG.md` | Classification correction log |
| `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md` | Stage 9 closed for experimentation |
| `docs/audits/STAGE_10_FINAL_CLOSURE_AUDIT.md` | Stage 10 `STAGE_10_EXECUTION = CLOSED` |
| `RESEARCH_CONSTITUTION.md` | Governing rules / amendment table |

No Stage 2–10 result, model, dataset, calibration, or threshold file was modified in this audit.

---

## A. Author block

Ready manuscript (paper body, after the non-paper envelope) and `IEEE_MANUSCRIPT.md`:

```
Aitsam Ul Hassan and Muhammad Haseeb Ramzan
Pak-Austria Fachhochschule:
Institute of Applied Sciences and Technology
Haripur, Pakistan
```

| Check | Finding |
| --- | --- |
| Names | Match owner-confirmed list |
| Affiliation / city / country | Match confirmed text |
| Email | **Absent** (not invented) |
| ORCID | **Absent** (not invented) |
| Extra department name | **Absent** (institute line is the confirmed affiliation, not an invented department) |
| Author roles / corresponding author | **Absent** |
| Acknowledgments / funding | **Absent** (no Acknowledgments section) |

AUTHOR_BLOCK_STATUS = PASS

---

## B. Manuscript structure

**Actual paper-body order** in `IEEE_TEMPLATE_READY_MANUSCRIPT.md`:

Title → authors/affiliation → Abstract → Index Terms → **I. Introduction** → **II. Related Work** → **III. Research Gap and Contributions** → **IV. Methodology** (A architecture, B LendingClub dataset, C UCI dataset, D feature/leakage policy, E temporal split, F M-4B models, G M-5 calibration, H explainability, I Shariah-oriented governance, J decision policies) → **V. Experimental Protocol** → **VI. Results** (A LC baseline, B calibration, C explainability, D decision policy, E UCI independent analysis, F descriptive/post-hoc) → **VII. Discussion** → **VIII. Limitations** → **IX. Conclusion** → References.

This is the IEEE conversion I–IX map. It is complete. No section was rewritten in this audit.

**Documentation note (not a scientific defect):** this audit prompt listed a different top-level taxonomy (III Research Questions; IV Methods; V Dataset; VI Temporal Split; VII Models/Calibration; VIII Results; IX Discussion/Limitations/Conclusion). Dataset, leakage, temporal split, models, calibration, explainability, and governance are **present as Section IV subsections**, not as separate Roman sections V–VII. Results/generalization/robustness content is in **VI** (plus UCI in VI.E). Discussion, limitations, and conclusion are **VII–IX**, not a single IX. **Do not rewrite** to force the prompt’s heading names.

---

## C. Scientific integrity / closed stages

| Check | Finding |
| --- | --- |
| Stage 9 | Closure audit: closed for experimentation; 9.5–9.7 unauthorized. Inventory: **CLOSED**. Not reopened by paper-phase files. |
| Stage 10 | Closure audit: `STAGE_10_EXECUTION = CLOSED`. Inventory: **CLOSED**. Not reopened. |
| TEST | Manuscript states TEST reporting-only; thresholds/calibrators identified on validation. No recompute in this audit. |
| New experiment | **None** in this audit |
| Metrics recalculated | **None** |
| Models retrained | **None** |
| Datasets changed | **None** |
| Calibration changed | **None** |
| Thresholds changed | **None** |

STAGE_2_10_STATUS = UNCHANGED  
TEST_STATUS = NOT_REOPENED  
EXPERIMENT_STATUS = NONE_RUN  
SCIENTIFIC_CONTENT_STATUS = UNCHANGED

**Documentation note:** `RESEARCH_CONSTITUTION.md` still contains the leftover sentence “Stage 10 is not started,” and the Stage 9 closure audit (written before Stage 10 execution) still says “Stage 10 has not been started.” The Stage 10 closure audit and paper inventory record Stage 10 **CLOSED**. This lag is a governing-doc / historical-audit issue, **not** a manuscript scientific rewrite. The IEEE ready manuscript does not claim Stage 10 is open.

---

## D. Key frozen values

Compared ready manuscript ↔ evidence master `docs/paper/MANUSCRIPT_DRAFT.md` (transcription check only; **not** recomputed).

| Quantity | Required | Ready manuscript | Master | Status |
| --- | --- | --- | --- | --- |
| M-4B EBM TEST ROC-AUC | `0.6799408767429772` | Present (Table II/III, Discussion) | Present | MATCH |
| M-5 raw/Platt EBM TEST ROC-AUC | `0.6776693941139847` | Present (Abstract, Table II/IV, Discussion, Conclusion) | Present | MATCH |
| UCI XGBoost raw ECE (M-9.4-X) | `0.20065704943022225` | Present (Table VII + note) | Present | MATCH |
| LC TEST \(n\) | `208886` | Present (`208886` and `208{,}886`) | Present | MATCH |
| \(t_{\text{low}}\) | `0.06` | Present | Present | MATCH |
| \(t_{\text{high}}\) | `0.69` | Present | Present | MATCH |
| \(t^{*}\) | `0.16` | Present | Present | MATCH |

KEY_VALUE_STATUS = MATCH

No mismatch found. Nothing was “fixed.”

---

## E. Model provenance

| Context | Ready-manuscript treatment | Audit |
| --- | --- | --- |
| **M-4B** | LendingClub families; TEST after TRAIN+VALIDATION refit; selected EBM not used from fusion onward | PASS |
| **M-5** | TRAIN-only EBM + validation-only Platt; `p_selected` downstream lineage | PASS |
| Downstream EBM | Decisions use M-5, not M-4B TEST dump; Stage 6 opening-language vs TRAIN-only metadata disclosed | PASS |
| TreeSHAP | Explicitly **not** used; not appropriate for first-order EBM GAM | PASS |
| **M-9.4-AE** | Independent methodology; approved written scope; LR+EBM | PASS (`INDEPENDENT_UCI_LOGISTIC_REGRESSION_AND_EBM`) |
| **M-9.4-X** | Exploratory; `DEVIATION-001`; not merged with M-4B LC XGBoost | PASS (`EXPLORATORY_UCI_XGBOOST_DEVIATION_001`) |

Aligned with `M9_4_AE_HUMAN_REVIEW.md` / `M9_4_AE_CORRECTION_LOG.md`. The withdrawn placement-task phrase “UCI exploratory analysis context” for M-9.4-AE is **not** used as the current paper classification.

---

## F. Shariah-oriented governance

The ready manuscript **does not** claim Shariah certification, religious/legal compliance certification, a formal Shariah ruling, or contract-level verification where fields are absent.

It states: research prototype for Shariah-oriented governance and evidence traceability; not certification/fatwa/automated verdict/`EXPERT_VALIDATED`; LendingClub lacks contract-level Shariah fields; `INSUFFICIENT_INFORMATION` is an evidence/schema limitation, not applicant/contract non-compliance; human review is not certification; SECP “shall not be called Shariah compliant unless a Commission certificate is granted” is used as a **prohibition**. Limitations keep the schema gap explicit.

SHARIAH_CLAIM_STATUS = NO_CERTIFICATION_OR_COMPLIANCE_CLAIM

---

## G. UCI generalization

Section VI.E: UCI “does **not** validate the LendingClub architecture or Shariah governance.” Discussion: UCI LR/EBM ROC-AUC values “are not comparable as a claim that the LendingClub architecture generalizes.” Abstract: independent UCI LR/EBM methodology context; UCI XGBoost exploratory.

M-9.4-X remains `DEVIATION-001` / `EXECUTION-TIME EXPANSION, EXPLORATORY`.

---

## H. Explainability / calibration

- Additive SHAP identity preserved as display equation (1): \(\phi_i(x)=g_i(x_i)-\operatorname{mean}_{\text{TRAIN}} g_i\).
- Platt: validation-only fit; TEST not used to fit; frozen \(a,b\); Platt TEST ROC-AUC equals raw.
- Reliability-diagram image files: **not retained**, omitted, **not regenerated** in this audit.
- Stage 4B ECE and UCI LR/EBM family-raw ECE: stated **not stored**; not invented.
- UCI XGBoost raw ECE transcribed only under M-9.4-X.

Fig. 1 remains a text schematic. Fig. 2 is not in the paper body (envelope notes omission as duplicate of Table IX).

---

## I. Claim integrity (report only; not rewritten)

Searched the ready manuscript for production deployment, real-time lending, fraud-detection performance, causal effects, certification/compliance, guaranteed fairness, unsupported novelty, exaggerated performance, and unsupported generalization.

**No blocking unsupported-affirmative claims found.** Occurrences are denials, literature-context, or qualified design questions:

| Location | Text class | Why not a blocker |
| --- | --- | --- |
| Abstract; I; II.E; IX | Fraud | **No** fraud experiment; performance **not** reported |
| I; II.F; VII; IX | Production / real-time / ECOA | Explicitly **not** production-ready; no latency paper; counts not origination outcomes |
| I design question | “independently validated and auditable” / “without materially sacrificing predictive performance” | Immediately labeled a **design question**, not a proven superiority result; governance not claimed to change ROC-AUC |
| III | Novelty | Gap “relative to the recorded literature sources”; architecture **not** called “novel” |
| II.F; III; VII | Fairness | Processors **not** run; fairness **not** a contribution |
| IV.H; VI.C | Causal | Attributions **not** causal |
| VI.E; VII | UCI / XGBoost superiority | Exploratory; not overall superior; not LC validation |
| I; IV.I; VII; VIII; IX | Shariah certification | Denied (see §F) |

---

## J. References

Ready manuscript References **[1]–[34]** match the evidence-master / evidence-map source identities. Unverified metadata remain marked (Platt [14] DOI/URL; Zenodo creators [20]; AAOIFI years [28],[29]; IFSB-10 FAQ [31]; Guo [17] DOI NONE). No bibliographic field was invented or updated in this audit.

REFERENCE_STATUS = PRESERVED

**Documentation note:** numeric order follows the master identity map, not IEEE first-appearance sequence. Previously recorded; not a key-value mismatch.

---

## 1. PASS items

- Author block: confirmed names and affiliation only; no invented email/ORCID/role/acknowledgment.
- Key frozen values MATCH the evidence master.
- M-4B / M-5 / M-9.4-AE / M-9.4-X provenance and TreeSHAP non-use preserved.
- Shariah: research prototype / evidence-gap; no certification or ruling claim.
- UCI not used as LendingClub validation; XGBoost remains exploratory `DEVIATION-001`.
- SHAP identity (1) and Platt wording preserved; missing ECE/reliability diagrams not fabricated.
- References [1]–[34] preserved.
- Stage 9/10 remain closed in controlling closure/inventory records; TEST not reopened; no experiment in this audit.
- Affirmative production / fraud-performance / causal / fairness-guarantee / certification claims not found.

## 2. Documentation-only notes

1. Top-level I–IX headings follow the IEEE conversion map, not this audit prompt’s Dataset / Temporal-Split / Models as separate Roman sections (those topics are IV.B–J and VI).
2. Table body order remains I → IX → II… (G0 in Methods); Results still present II before III and VII before VIII.
3. Fig. 1 is a text schematic; Fig. 2 omitted; reliability diagrams omitted.
4. No IEEE Word/LaTeX template in the repository (`TEMPLATE_NOT_FOUND`).
5. Citation numbers are master identities, not first-cite order.
6. Conclusion still uses master “APPROVE / REVIEW / REJECT” for counts labeled `HUMAN_REVIEW` in tables.
7. `RESEARCH_CONSTITUTION.md` leftover “Stage 10 is not started” vs Stage 10 closure **CLOSED**.
8. Stage 9 closure audit historically says Stage 10 not started (pre-Stage-10 document).
9. `docs/PAPER_EVIDENCE_INVENTORY.md` header still says paper drafting **NOT STARTED** (inventory file lag).
10. `docs/paper/IEEE_TEMPLATE_CONVERSION_AUDIT.md` still records historical `AUTHOR_BLOCK_STATUS = PLACEHOLDER_REQUIRED` (conversion-time snapshot). Current ready/IEEE manuscripts and placement audit have confirmed authors.
11. Evidence master has no author block (metadata wrapper draft); author text lives in IEEE derivatives only.

## 3. Blocking issues requiring human review

**None for scientific integrity of the ready manuscript.**

KEY_VALUE_STATUS = MATCH. No mismatch was found; nothing was altered.

---

IEEE template placement was **not** started.
