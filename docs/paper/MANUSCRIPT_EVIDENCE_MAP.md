# Manuscript evidence map (drafting aid)

| Item | Value |
| --- | --- |
| **Document ID** | `MANUSCRIPT-EVIDENCE-MAP` |
| **Date** | 2026-09-16 |
| **Paired draft** | `docs/paper/MANUSCRIPT_DRAFT.md` |
| **Experiments** | None |
| **Sync** | Updated after documentation-cleanup of remaining evidence markers, then after FINAL PAPER INTEGRITY GATE prose narrowing (no new metrics) |

This file maps draft claims to frozen artifacts. It is not the paper.

## Citation number map

Numbers in `MANUSCRIPT_DRAFT.md` match this table. Bibliographic fields are copied from `docs/literature/LITERATURE_SOURCE_REGISTER.csv`. Unverified fields are not filled.

| Draft # | SOURCE_ID | Notes |
| ---: | --- | --- |
| [1] | LIT-001 | Hand & Henley 1997 |
| [2] | LIT-002 | Baesens et al. 2003 |
| [3] | LIT-003 | Lessmann et al. 2015 |
| [4] | LIT-004 | Yeh & Lien 2009 |
| [5] | LIT-005 | Malekipirbazari & Aksakalli 2015 |
| [6] | LIT-006 | Ariza-Garzón et al. 2020 |
| [7] | LIT-007 | Bussmann et al. 2021 |
| [8] | LIT-008 | Kozodoi et al. 2022 |
| [9] | LIT-009 | Hastie & Tibshirani 1986 |
| [10] | LIT-010 | Lou et al. 2013 |
| [11] | LIT-011 | Nori et al. 2019 preprint |
| [12] | LIT-012 | Lundberg & Lee 2017 |
| [13] | LIT-013 | Lundberg et al. 2020 TreeSHAP |
| [14] | LIT-014 | Platt 1999; **no DOI**; URL UNVERIFIED |
| [15] | LIT-015 | Niculescu-Mizil & Caruana 2005 |
| [16] | LIT-016 | Zadrozny & Elkan 2002 |
| [17] | LIT-017 | Guo et al. 2017; DOI field NONE in register |
| [18] | LIT-018 | Chen & Guestrin 2016 |
| [19] | LIT-019 | Bolton & Hand 2002 |
| [20] | DS-001 | Zenodo LC extract; **creator names UNVERIFIED** |
| [21] | DS-002 | UCI dataset 350 |
| [22] | DS-003 | German Credit; **not executed** |
| [23] | DS-004 | Australian Credit Approval; **not executed** |
| [24] | SRC-SBP-IFPD-C8-2024 | SBP circular |
| [25] | SRC-SBP-SGF-2025-TEXT | SGF 2025 text |
| [26] | SRC-SBP-IBD-C1-2012 | Murabaha invoices |
| [27] | SRC-SECP-SGR-2023-SRO-TEXT | SECP SGR 2023 |
| [28] | SRC-AAOIFI-SS8-IDENTITY | Identity only |
| [29] | SRC-AAOIFI-SS9-IDENTITY | Identity only; URL not re-fetched in literature package |
| [30] | SRC-AAOIFI-GS-INDEX | Listing only |
| [31] | REG-IFSB-10 | FAQ PDF verified |
| [32] | REG-CFPB-1002-9 | Regulation B |
| [33] | REG-CFPB-2022-03 | Algorithms / adverse action |
| [34] | REG-CFPB-2023-03 | Sample forms |

`SRC-AAOIFI-SS-INDEX` is in the register but unused in the draft (redundant with [28]–[29]).

## Numerical transcription sources

| Draft quantity | Artifact |
| --- | --- |
| LC n, splits, hashes | inventory §2; `audit/lendingclub_split_manifest.json` |
| UCI n, splits, hashes | inventory §2; `audit/uci_split_manifest.json` |
| M-4B TEST metrics | `results/metrics/stage4b_test_metrics.json`; Stage 4B report table E |
| M-4B family selection | `docs/STAGE_4B_MODELING_REPORT.md` §D |
| M-5 VAL/TEST cal | `stage5_validation_metrics.json`; `stage5_test_metrics.json`; `selected_calibration.json` |
| Platt a, b | `platt_record.json` / inventory |
| Stage 6 ranks / identity error | `table1_global_attribution.csv`; `shap_vs_ebm_agreement.json` |
| A0/A1/A3 counts | `results/decision/v2/tables/table3_test_decision_outcomes.csv` |
| Band default rates | `table3b_test_default_rates_by_band.csv` |
| G0 | Stage 8 v2 report |
| UCI family-raw TEST | `results/uci_generalization/v1/tables/uci_test_family_raw.csv` (no ECE column) |
| UCI LR/EBM family-raw ECE | **not stored** (family-raw CSV; S10-A4 `existing_test_ece` empty) |
| UCI XGBoost selected-family raw ECE (M-9.4-X exploratory only) | `results/uci_generalization/v1/tables/uci_test_calibration.csv` `method=raw` ECE `0.20065704943022225` |
| UCI selected (exploratory) | `uci_test_selected.json` |
| S10-R1 n and mix | `s10_r1_year_decision_mix.csv` |
| S10-A1 gap | `s10_a1_gap_crosstab.csv` |

## Table/figure plan (no new experiments)

| ID | Draft location | Source | New computation? |
| --- | --- | --- | --- |
| Table I | Instantiated in §7.3 | inventory §2; Stage 2 report; LC/UCI split manifests | No |
| Table II | M-4B vs M-5 EBM | inventory §3 | No |
| Table III | M-4B TEST | stage4b_test_metrics.json | No |
| Table IV | Stage 5 VAL/TEST calibration | stage5_*_metrics.json | No |
| Table V | Stage 6 global ranks | table1 | No |
| Table VI | A0/A1/A3 counts | table3 | No |
| Table VII | UCI family-raw + exploratory selected | `uci_test_family_raw.csv`; `uci_test_selected.json`; XGBoost raw ECE from `uci_test_calibration.csv` `method=raw` (exploratory / `DEVIATION-001` only) | No |
| Table VIII | Band default rates | table3b | No |
| Table IX / Fig. 2 | G0 matrix | Stage 8 v2 report; instantiated as captioned copy in §7.10; no image file | Copy |
| Table X | S10-R1 year mix | `results/stage10/v1/tables/s10_r1_year_decision_mix.csv` | No |
| Table XI | S10-A1 gap crosstab | `results/stage10/v1/tables/s10_a1_gap_crosstab.csv` | No |
| Fig. 1 | Text schematic in §7.1 | Stage 7 v2 / Stage 8 v2 layer descriptions; **no stored image file** | None |
| Fig. 3–4 | Reliability diagrams | Named in `docs/STAGE_5_CALIBRATION_REPORT.md` §E; **image files not retained** | Omitted from manuscript package; do not regenerate |

ECE 10-bin rule is sourced from `docs/STAGE_5_CALIBRATION_REPORT.md`, not `docs/METRIC_DEFINITIONS.md`.

## Gaps carried into the draft

- Platt [14] DOI/URL unverified
- Zenodo [20] creator names unverified
- AAOIFI SS 8/9 years UNVERIFIED; SS9 URL not re-fetched
- No 2023–2026 systematic ML-credit review in the package
- No real-time latency paper
- AAOIFI clauses unavailable
- Stage 4B final EBM SHA-256 not recorded
- `git_commit` null
- Calibration and explainability **image** files named in reports/manifests are not present as png/pdf in the repository; omitted rather than regenerated. Stage 5 reliability diagrams remain omitted from the manuscript package.
- ECE not stored for any Stage 4B family in `stage4b_test_metrics.json`
- UCI family-raw ECE not stored for logistic regression or EBM
- UCI XGBoost family-raw CSV has no ECE column; selected-family raw ECE transcribed from `uci_test_calibration.csv` `method=raw` as exploratory M-9.4-X / `DEVIATION-001` only (`0.20065704943022225`). Path `results/calibration/uci_test_calibration.csv` does not exist.
- Register `SRC-AAOIFI-SS-INDEX` unused (redundant with [28]–[29])
- Historical Stage 9 leftover `DRAFT` wording is a **closure-audit** record; the current Stage 9 protocol file does not contain that leftover status. Stage 9 is CLOSED. UCI XGBoost remains exploratory (`DEVIATION-001`).
