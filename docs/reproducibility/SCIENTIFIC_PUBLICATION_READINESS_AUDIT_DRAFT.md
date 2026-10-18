# Scientific publication readiness audit

**DRAFT — INDEPENDENT CRITICAL REVIEW. NOT A SUBMISSION RECOMMENDATION AND NOT AN ACCEPTANCE FORECAST.**

Prepared as STEP 3B-10A. This file is the only file created by that step. No manuscript, protocol, ledger, catalog, test, model, or historical result was edited. No metric was recomputed from protected TEST rows.

## A. Audit Scope and Baseline

Role: skeptical IEEE Access review of whether the current manuscripts can support the claims a reader will take from the title, abstract, and lead design question.

Canonical scientific text reviewed: `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex`. Parallel wording was checked in `docs/paper/IEEE_MANUSCRIPT.md` and `docs/paper/MANUSCRIPT_DRAFT.md`. The gitignored template duplicate was confirmed byte-identical to the canonical LaTeX file by SHA-256.

Baseline observed before this audit file was created:

| Check | Observed |
| --- | --- |
| Branch | `main` |
| HEAD | `583ad0b30e8007a5f3f0bb13ede7b010fdad5fec` |
| Canonical and duplicate LaTeX SHA-256 | `98b8bc34b5b6d80ce9410c3475d33efad8590bb7cd85982962538cf063efe418` |
| `IEEE_MANUSCRIPT.md` | `4d54fcf95e40c6add38a29e7a8580863b545b3e87f013c59cc13a25870392a29` |
| `MANUSCRIPT_DRAFT.md` | `100e229ac37fd5cff19f2f3a236efa7571fd1ae5f40dbf75ac04452796de2a4f` |
| Protocol draft SHA-256 | `b4bd071a96a6d0180f1850bcacd5fe1af8ccfbb7de9faa137e4164e2563df76b` |
| Acquisition ledger SHA-256 | `100fa59b74d2c187e268e76432e8cda3089ac6b2942a630b15cc491c91f180fb` |
| Template duplicate | gitignored by `.gitignore` line 89 |

The three tracked manuscripts were already modified. The protocol and ledger were untracked. That baseline matched the STEP 3B-9B record, so the audit proceeded.

Evidence consulted included stored metric JSON and CSV files, Stage 4B–10 reports, split manifests, the rule catalog, applicability code, the expert-review protocol, the acquisition ledger, and the 16-page PDF already compiled in STEP 3B-9B at `%TEMP%\karimpay-3b9b-canon3\IEEE_ACCESS_READY_MANUSCRIPT.pdf` (581,289 bytes). Pages were rendered for inspection. This audit did not recompile the manuscript and did not rerun experiments.

## B. Executive Scientific Verdict

The stored evidence demonstrates a **research software prototype and a frozen descriptive evaluation**. It does not demonstrate that evidence separation is more transparent, more defensible, or predictively competitive in the sense posed by the lead design question.

What the artifacts actually show:

| Layer | What is demonstrated | What is not demonstrated |
| --- | --- | --- |
| A. Predictive modeling | Four established families were fit under a chronological split. Validation mean PR-AUC, a 0.005 window, then Brier and simplicity, selected the additive EBM. On TEST, that M-4B EBM has ROC-AUC 0.6799408767429772. LendingClub XGBoost has higher stored TEST ROC-AUC (0.6854404067747387) and PR-AUC. | A new scoring method. A fair probability ranking of families. Superiority over prior LendingClub models. |
| B. Calibration | A TRAIN-only EBM (M-5), distinct from the M-4B refit, received validation-only Platt scaling. Pooled TEST Brier and ECE are lower for Platt than for raw. ROC-AUC is unchanged, as expected for a strictly increasing map. | A new calibrator. Uniform calibration across years. The 2018 slice reverses the pooled improvement. |
| C. Additive explainability | On a 5,000-row TEST sample, centered additive terms reconstruct the M-5 logit with max absolute error \(8.881784197001252\times 10^{-16}\). Rank agreement with those same terms is 1.0. | Usefulness, fairness, causality, or adverse-action sufficiency. |
| D. Software architecture | Credit scores, explanation objects, and governance evidence are separate, and a frozen map consumes `p_selected`. | Methodological novelty beyond composition of known parts. |
| E. Governance screening | Historical engine v1 returns `INSUFFICIENT_INFORMATION` for every stored LendingClub TEST row because contract fields are absent. | Accuracy of a Shariah classification. Applicability of SBP, SECP, or AAOIFI rules. |
| F. Decision-policy simulation | Three maps on identical scores yield different APPROVE / HUMAN_REVIEW / REJECT counts. | A better policy. A measured human-review workload. A change in predictive performance. |

The honest contribution is an engineering demonstration: a fail-closed evidence-gap map can be attached to a frozen credit probability without changing that probability. Combining Platt scaling, an additive EBM, and a rule screen does not by itself create a new empirical method.

The lead question in Section I is only illustrated. Section IX already says it is only partially addressable. That admission is scientifically correct and is not yet carried into the question the paper asks.

**Verdict:** not submission-ready. A narrowed prototype paper can be defended from existing evidence. A paper that answers the quoted comparative question cannot.

## C. Dataset Suitability

### LendingClub granting-model extract

Source: Zenodo record 11295916, DOI `10.5281/zenodo.11295916`, version 0.1, CC-BY-4.0. Local file hash `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc`. Row count 1,347,681 × 15 is in `results/metrics/final_target_definition.json` and `results/metrics/lendingclub_dimensions.json`.

The label is a resolved-loan outcome. Freeze coding is Default = 1 for Charged Off and 0 for Fully Paid (`docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex`, dataset subsection). `results/metrics/lendingclub_target_audit.json` records `TARGET_DEFINITION_DOCUMENTATION_CONFLICT` and `original_loan_status_mapping_verified: false`. The depositor text both equates the positive class with charged-off loans and, in another sentence, says the release keeps Fully Paid or Default. Those are not the same Lending Club status. The manuscript says a conflict was frozen. It does not quote the conflict. A reader cannot judge how much label noise remains.

The extract keeps originated loans that reached a resolved status. Rejected applicants are absent. The manuscript states that selection bias. Two further limits are only partly stated:

- `issue_d` is the split clock and is excluded as a feature. `docs/lendingclub_leakage_audit.md` classifies it as an approval/origination month, not a demonstrated pre-decision application date. The chronological split is therefore a split of originated loans, not a prospective application-time trial.
- Resolved-only inclusion drops loans that have not yet reached Fully Paid or Charged Off. Later issue months are a different selection, not only a later calendar slice. Stored TEST year mix in `results/stage10/v1/metrics/s10_r1_year.json` and the manuscript year table show 2017 default rate 0.2317483598077603 (\(n=152726\)) and 2018 default rate 0.15751424501424502 (\(n=56160\)). The manuscript reports the rates. It does not state the maturity/selection interpretation those rates support.

Feature timing is not fully closed. `docs/lendingclub_leakage_audit.md` marks `dti_n` as `SAFE_APPLICATION_TIME` at medium confidence because of a “Monthly information” wording ambiguity, and `experience_c` as `UNKNOWN` (correctly excluded). The manuscript says newly discovered leakage beyond the frozen exclusions is recorded as none, and it flags `dti_n==999` as unlabeled. The medium-confidence timing note is not in the manuscript.

Geography and institution are US peer-to-peer consumer credit, 2007–2018. Nothing in the schema is a verified Islamic-finance contract. `results/shariah/v2/l1_lendingclub.json` lists the contractual fields as missing and sets readiness to `INSUFFICIENT_SCHEMA_FOR_APPLICANT_DETERMINATION`. There are no human-reviewed Shariah compliance labels.

### UCI Default of Credit Card Clients

`results/metrics/uci_dataset_audit.json` and `results/metrics/uci_split_summary.json`: 30,000 × 25; stratified random split, seed 42, 20,999 / 4,499 / 4,502; no calendar index. Target is `default payment next month`. Undocumented EDUCATION and MARRIAGE codes are recorded and were not recoded. TEST prevalence is 0.22123500666370502 with 996 positives (`results/uci_generalization/v1/metrics/uci_test_selected.json`).

UCI checks whether logistic regression and an additive EBM can be fit and calibrated on a second public credit table. `results/uci_generalization/v1/metrics/family_selection.json` shows the exploratory arm selected XGBoost by UCI validation PR-AUC. That arm is `DEVIATION-001`. It does not validate the LendingClub architecture, the fusion map, or any Shariah rule.

### Credit-risk validation versus governance validation

The manuscript keeps these apart in the abstract, contribution list, UCI subsection, and conclusion. That separation is warranted. Neither public dataset contains a Shariah label, a contract type, or an expert ruling. They cannot validate Shariah decision accuracy.

A new Islamic-finance benchmark is **not essential** to defend the claims the stored evidence can support: chronological credit scoring, a described Platt map, additive reconstruction of one EBM, and a fail-closed evidence-gap count. It **is essential** before any claim that the governance layer classifies Shariah compliance, that a rule applies to a real product, or that the pipeline is defensible inside an Islamic financial institution. That benchmark should be a scoped future requirement, not a silent repair of the present experiment.

## D. ML and Calibration Methodology

### Split and leakage

`audit/lendingclub_split_manifest.json` and `results/metrics/lendingclub_split_summary.json`: train through 2016-03 (\(n=941267\)), validation 2016-04 through 2017-01 (\(n=197528\)), test from 2017-02 (\(n=208886\)). Cutoffs follow cumulative issue-month share and are not described as performance-tuned. Preprocessing for the downstream EBM is train-only (`docs/STAGE_4A_PREPROCESSING_REPORT.md`). Target, `issue_d`, `id`, `experience_c`, `title`, and `desc` are excluded from the credit model.

Residual leakage risk is the unresolved `dti_n` timing note and the fact that the clock is origination month. The manuscript’s “no newly discovered leakage” sentence is accurate only as “no additional column was later condemned.” It does not clear those two residual issues.

### Model identity

M-4B and M-5 are different fits. Table II of the manuscript records the paths, the missing M-4B joblib digest, the M-5 digest `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4`, and the two ROC-AUC values. That separation is a strength. The downstream probability is M-5 `p_platt`, not the M-4B refit.

### Family selection

`experiments/stage4b_credit_risk/selected_configurations.json` stores the rule: mean validation PR-AUC, 0.005 window, then lowest mean Brier, then simplicity. The stored ranking lists XGBoost first and the EBM second. The manuscript methods paragraph transcribes the window and the EBM selection figures.

`docs/STAGE_4B_MODELING_REPORT.md` states that the EBM Brier advantage is expected in part because logistic regression and random forest use `class_weight='balanced'` and XGBoost uses `scale_pos_weight`, while EBM 0.7.8 has no class-weight argument. The manuscript records those configurations and does not state that the Brier tie-break compares differently weighted probability scales. TEST metrics in `results/metrics/stage4b_test_metrics.json` then show XGBoost ahead on ROC-AUC and PR-AUC and the EBM ahead on Brier. A reader of the abstract sentence “validation selected the EBM” can take that as a predictive win. The methods paragraph prevents that reading only if the reader reaches it and supplies the weighting caveat the paper omits.

The numeral 0.388473 is stored as “Best PR-AUC” in the selection record and as XGBoost seed 123 in `results/metrics/stage4b_validation_metrics.json` (`pr_auc` 0.38847335600164584). The manuscript calls it the best **mean**. The report’s aggregate mean is printed as 0.3885. This audit did not recompute the five-seed mean. The digits are supported. The word “mean” on that specific numeral is not independently verified.

### Calibration

`results/decision/frozen_policy.json` and the manuscript: Platt form \(\sigma(a\cdot\mathrm{logit}(p_{\mathrm{raw}})+b)\), \(a=1.1988263209549705\), \(b=0.6697765046966161\), fit on validation. Selection: validation Brier, 0.001 tie, order raw > Platt > isotonic. Isotonic validation Brier 0.17469431274375435; Platt 0.1748453678205707. Platt is selected by the tie rule.

Pooled TEST (`results/calibration/metrics/stage5_test_metrics.json`):

| Method | ROC-AUC | PR-AUC | Brier | ECE |
| --- | --- | --- | --- | --- |
| raw | 0.6776693941139847 | 0.35096314719303284 | 0.1579357158246714 | 0.03753450535939786 |
| Platt | 0.6776693941139847 | 0.35096314719303284 | 0.15616920271522994 | 0.020267295489117824 |
| isotonic | 0.6775144297473418 | 0.3462755761696744 | 0.1561969364282068 | 0.020046149884935992 |

Paired Platt-minus-raw differences are stored in `results/calibration/metrics/stage5_paired_differences.json`. The manuscript rounds Brier to \(-0.001767\) and ECE to \(-0.017267\), and it says those intervals are not \(p\)-values. That reading is faithful. The absolute Brier change is about 0.0018 on a score whose level is about 0.156.

`results/calibration/metrics/stage5_temporal.json` is the 2018 deterioration:

| Year | \(n\) | Raw ECE | Platt ECE | Raw Brier | Platt Brier |
| --- | --- | --- | --- | --- | --- |
| 2017 | 152726 | 0.0540168458414863 | 0.005096425775164428 | 0.1697378917044011 | 0.16568677660675435 |
| 2018 | 56160 | 0.010258720583955352 | 0.06152417312325683 | 0.1258399338907754 | 0.13028635032639518 |

On 2018, frozen Platt is worse than raw on Brier, log loss, and ECE. The manuscript results and limitations state this and call it temporal transfer failure. The abstract reports only the pooled Platt ECE. A reader who stops at the abstract will think calibration succeeded on the test period.

### Uncertainty, imbalance, and reuse

Bootstrap percentile intervals, 1,000 resamples, seed 42, are stored for M-4B and M-5. The manuscript quotes the M-4B EBM ROC, PR, and Brier intervals and the paired calibration intervals. The main family table and the calibration table print point estimates only. No hypothesis test is stored, and this audit invents none.

Prevalence is about 0.20. ROC-AUC, PR-AUC, Brier, and log loss are all stored. PR-AUC is the more informative discrimination summary at this prevalence, and the paper does report it. That is appropriate.

The same TEST rows then support family metrics, calibration reporting, fusion counts, year slices, ablation, cost scenarios, and Stage 10 description. The protocol labels the later passes non-confirmatory. The results section still displays them. There is no multiplicity adjustment. That is acceptable only while every post-hoc display stays descriptive.

UCI logistic regression and EBM are methodology context. UCI XGBoost is exploratory. The manuscript says so. The five-seed UCI XGBoost validation table is recorded as degenerate in the limitations. That limitation should stay.

## E. Explainability Validity

The manuscript equation is \(\phi_i(x)=g_i(x_i)-\mathrm{mean}_{\mathrm{TRAIN}} g_i\) on the M-5 EBM logit, with `interactions=0`. For a first-order GAM, that is the centered additive term. It is the right mathematical object. It is not an independent Shapley explanation from a second algorithm.

`results/explainability/metrics/shap_vs_ebm_agreement.json`: Spearman 1.0, top-k overlap 1.0, reconstruction max absolute error \(8.881784197001252\times 10^{-16}\). `results/explainability/artifacts/seed42_attributions.meta.json`: `n_explained=5000`, output space `ebm_decision_function_logit_link`, model id `ebm_train_only_seed42`. The manuscript states the sample size, the identity interpretation, and that TreeSHAP was not used. Those statements match the artifacts.

The manuscript also says attributions are not causal and are not an approval criterion. Section IX says perfect agreement should not be advertised as a second-model confirmation. Those fences are right.

What remains unshown:

- Human interpretability was not studied.
- Financial usefulness was not studied.
- US adverse-action reason suitability was not studied. The ECOA and CFPB citations are motivation. The paper says the prototype is not an ECOA finding.
- `zip_code` is both a quasi-identifier and an explained feature. No fairness audit was run (`docs/paper` limitations; Kozodoi et al. is context only).

Additive identity supports reconstruction accuracy and faithfulness to this model’s own terms. It does not support a claim of useful, actionable, fair, or regulatorily sufficient explanations.

## F. Governance and Fusion Interpretation

Stored historical runs record `stage7-shariah-engine-v1`:

- `audit/stage7_shariah_run.json`
- `audit/stage7_v2_governance_run.json` (experiment id v2, engine still v1)
- `audit/stage8_policy_config.json`

The live code constant is `stage7-shariah-engine-v2-scope-gated` (`src/shariah/engine.py`). Applicability is `stage7-applicability-scope-unknown-v1` (`src/shariah/applicability.py`). The six source rules `SH-SBP-SGF-002`, `SH-SBP-SGF-003`, `SH-SBP-MUR-INV-001`, `SH-SBP-MUR-INV-002`, `SH-SBP-MUR-PAY-001`, and `SH-SECP-SGR-SEC-001` remain `SCOPE_UNKNOWN`. Diagnostic predicates are not public applicability decisions. `certification_claim` is false. The manuscript says the live screen did not generate the stored TEST counts. That statement matches the artifacts.

G0, as printed in the manuscript, maps `INSUFFICIENT_INFORMATION` × LOW or MEDIUM to `HUMAN_REVIEW` and × HIGH to `REJECT`. `results/decision/metrics/fused_test.json` and `results/stage10/v1/metrics/s10_a1_gap.json`:

| Map | APPROVE | HUMAN_REVIEW | REJECT | Source of the count |
| --- | --- | --- | --- | --- |
| A0 credit-only | 5232 | 203627 | 27 | LOW / MEDIUM / HIGH bands |
| A1 fused | 0 | 208859 | 27 | all rows `INSUFFICIENT_INFORMATION`; 5232+203627=208859 |
| A3/A4 monolithic | 61855 | 0 | 147031 | `results/decision/metrics/monolithic_test.json` |

The 27 REJECT rows are the 27 HIGH-band rows (\(p_{\mathrm{selected}}\ge 0.69\)). Their default rate is 0.5185185185185185 with a wide Wilson interval stored in the fused-test file. They are not a finding that 27 applicants failed a Shariah test. The results section and the conclusion say this. The abstract says every row is `INSUFFICIENT_INFORMATION` and then lists the three count triples. It does not say, in the same sentence, that 27 is the credit HIGH band.

`HUMAN_REVIEW` \(n=208859\) is a simulated policy count. Figure 3’s caption says it is not a collected human-review outcome. No analyst time, queue, or decision quality was measured. Review “workload” here means a row count under an assumed map.

Predictive scores are identical across A0, A1, and A3/A4 because each map reads the same `p_selected`. Count differences are allocation differences. They are not a predictive improvement and not evidence that one policy is better. Stored expected costs use an assumed 5:1 false-negative/false-positive scenario and, for the fused file, a review cost of 0.25, while the monolithic file stores review cost 0. The manuscript does not treat those costs as a winner. They must stay out of any later superiority sentence.

Synthetic rule tests and safety regression tests exercise software paths. They do not validate religious or regulatory conclusions on LendingClub.

## G. Regulatory and Expert-Review Boundaries

`docs/reproducibility/REGULATORY_SOURCE_AND_EXPERT_REVIEW_PROTOCOL_DRAFT.md` separates document identity, byte integrity, clause verification, applicability, and independent expert endorsement. All five are open. No reviewer is named.

`docs/reproducibility/OFFICIAL_PRIMARY_SOURCE_ACQUISITION_LEDGER_DRAFT.md` records HTTP 403 for the official SBP and SECP URLs attempted on 2026-10-18. A 403 response is a failed retrieval. It is not evidence that an instrument applies, and it is not evidence that an instrument does not apply. The manuscript treats the responses as failed retrievals.

PICG and MUFAP copies match recorded register digests. Hash equality identifies those stored third-party bytes. It does not authenticate an official original. The manuscript says this. Operative sentences about board approval, Murabaha documents, and the SECP certificate rule are still paraphrases of those unauthenticated copies or of identity pages. They can remain only as descriptions of what those copies say.

AAOIFI SS 8 and SS 9 are identity-only. Operative clauses were not retrieved. Catalog `clause_verified: true` on source-mapped rules is a catalog flag. The manuscript says `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW` is not authentication or expert validation. That fence matches `src/shariah/applicability.py`, which refuses to treat catalog text, hashes, or jurisdiction labels as a review.

No qualified Shariah or regulatory expert has validated a rule. No real contract was reviewed. The failed downloads must not be upgraded into a scope determination in a later draft.

## H. Literature and Novelty

The bibliography used for scholarly method is concentrated in 1986–2022 (Hand and Henley 1997 through Bussmann et al. and the CFPB circulars). The manuscript states that no 2023–2026 systematic machine-learning credit review was in the recorded sources, that Platt 1999 has no verified DOI or publisher URL, that Guo et al. 2017 has a DOI field recorded as none, and that AAOIFI years and the IFSB-10 full text are unresolved. Those are honest bibliographic gaps.

The research-gap paragraph says the recorded sources do not contain this exact end-to-end study on this hashed extract. The next sentence says that is a gap relative to the recorded sources and not absolute novelty. The second sentence is the only one a reviewer should accept. A closed local register cannot establish that the field lacks the comparison. This audit does not invent the missing papers and does not declare the architecture novel.

Prior LendingClub and SHAP papers are cited as different extracts and different pipelines. That comparison is fair. What is missing, and must be supplied by an external literature check rather than by assertion, is a current comparison with post-2022 credit calibration, additive explanations, and Islamic digital-finance governance studies. Until that check exists, the contribution has to stand as a prototype on two public credit datasets, not as a field-level gap.

## I. Numeric Evidence Traceability

Headline quantities checked against a file present on disk. This audit did not recompute them.

| Quantity | Value in the manuscript | Supporting file and field | Status |
| --- | --- | --- | --- |
| LendingClub rows | 1,347,681 | `results/metrics/final_target_definition.json` `n_rows` | Supported |
| Split counts | 941,267 / 197,528 / 208,886 | `audit/lendingclub_split_manifest.json` | Supported |
| Positive class | Charged Off / Fully Paid | `final_target_definition.json`; conflict in `lendingclub_target_audit.json` | Coding supported; original `loan_status` map unverified |
| M-4B EBM TEST ROC-AUC | 0.6799408767429772 | `results/metrics/stage4b_test_metrics.json` | Supported |
| M-4B EBM CI | [0.6772520975812178, 0.6828319764466856] | same file | Supported |
| M-4B XGBoost TEST ROC-AUC | 0.6854404067747387 | same file | Supported |
| M-5 Platt ROC-AUC, PR-AUC, Brier, ECE | 0.6776693941139847; 0.35096314719303284; 0.15616920271522994; 0.020267295489117824 | `results/calibration/metrics/stage5_test_metrics.json` method `platt` | Supported |
| Thresholds | 0.06, 0.69, monolithic 0.16 | `results/decision/v2/frozen_policy.json` | Supported |
| A1 counts | 0 / 208859 / 27 | `results/decision/metrics/fused_test.json` | Supported |
| A3/A4 counts | 61855 / 0 / 147031 | `results/decision/metrics/monolithic_test.json` | Supported |
| A0 counts | 5232 / 203627 / 27 | `results/stage10/v1/metrics/s10_a1_gap.json` credit bands; `results/ablation/v1/metrics/ablation_summary.json` | Supported |
| 2018 Platt ECE | 0.06152417312325683 | `results/calibration/metrics/stage5_temporal.json` | Supported |
| UCI family-raw LR / EBM / XGBoost | full rows in Table VII | `results/uci_generalization/v1/tables/uci_test_family_raw.csv` | Supported |
| UCI XGBoost raw ECE | 0.20065704943022225 | `results/uci_generalization/v1/tables/uci_test_calibration.csv` row `raw` | Supported |
| UCI selected isotonic | ROC-AUC 0.7708780071798891 and the other four metrics | `results/uci_generalization/v1/metrics/uci_test_selected.json` | Supported |
| Attribution sample and reconstruction error | 5,000; \(8.88\times 10^{-16}\) | `seed42_attributions.meta.json`; `shap_vs_ebm_agreement.json` | Supported |
| Selection numeral 0.388473 as a **mean** | manuscript methods | selection JSON says “Best PR-AUC”; seed 123 equals that numeral | Digits supported; “mean” label not independently verified |
| M-4B final EBM SHA-256 | stated as not recorded | manuscript limitation | Absent, and the paper says so |
| M-4B family ECE | stated as not stored | `stage4b_test_metrics.json` has no ECE field | Absent, and the paper says so |
| 10-bin reliability diagrams | omitted | manuscript; image files not retained | Absent, and the paper says so |

Stage 10 findings used above are descriptive fields in `results/stage10/v1/metrics/`. They were not treated as new confirmatory estimates.

`results/stage10/v1/metrics/s10_a4_sidebyside.json` repeats UCI Brier values at slightly shorter printed precision than `uci_test_family_raw.csv`. The manuscript matches the CSV. The CSV is the right source.

## J. Reproducibility and Software Integrity

Two different claims must stay apart.

**Reading the published numbers** is possible on this machine. Metric JSON, the UCI family CSV, split manifests, and the manuscript are present. Figure PDFs `fig1`–`fig5` under `docs/paper/figures/` are tracked. Sixteen local `.tfm` font files in the IEEE template directory are tracked. STEP 3B-9B compiled the canonical file to a 16-page PDF with local font paths and no package installation.

**Reproducing the experiments from a clean checkout** is not established.

- `requirements.txt` pins lower bounds (`pandas>=2.0.0`, `scikit-learn>=1.5`, `xgboost>=2.0`, `interpret>=0.6`), not the executed builds.
- Historical manifests record `git_commit: null` (`audit/lendingclub_split_manifest.json`). The Stage 4B report still says the workspace was not a Git repository. Commit `583ad0b` is a later safety snapshot. It did not generate Stage 4B–8.
- `data/raw/` is gitignored. `results/calibration/test/` is gitignored, including `ebm_seed42_calibrated.csv`, whose hash the manuscript quotes. A clean checkout does not contain the score file the fusion counts were read from.
- The M-4B final EBM joblib hash is not recorded.
- Some other joblibs and row-level prediction dumps are gitignored.
- Safety tests check the current research screen. They do not regenerate TEST ROC-AUC, calibration, or decision counts.
- The official-template LaTeX duplicate is gitignored. The canonical source is the tracked, currently uncommitted `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex`.
- The manuscript edits are not in HEAD. A checkout of HEAD does not contain this audit’s scientific text.

Source-code inspection of the live engine is possible from the snapshot commit. Reproduction of the published numerical results requires the ignored raw data, the ignored calibrated scores, unpinned dependencies, and historical manifests that point at no commit.

## K. IEEE Formatting and Submission Quality

The title matches a prototype paper. The abstract is numerically dense and, on the rendered first page, the words are visible. The STEP 3B-9B log still records an overfull horizontal box of 9.2679 pt on the abstract. This audit’s page render did not show a cut-off word. Slight margin protrusion can exist without a missing word. That is not camera-ready proof.

Other layout observations from the rendered PDF and the prior log:

- The experimental-protocol table is a full-width unnumbered float and is readable on page 9. The earlier 111 pt vertical overflow is gone.
- Figure 2 (threshold diagram) and Figure 3 (ROC bars) are legible. Bar labels are rounded to four decimals (for example 0.6799 and 0.6777) while the tables keep full stored precision. The caption does not say the labels are rounded.
- Calibration and attribution tables are dense and small. They remained inside the page in the render inspected here.
- Remaining log overflows under 20 pt were 2.46 pt, 5.13 pt, 12.58 pt, 4.92 pt, 5.21 pt, and 0.58 pt, plus the abstract. Font warning: `T1/pcr/n/n` undefined, with system URW Courier embedded.
- Hashes are broken across lines by the manuscript’s break macro. A production proofread should confirm that line breaks do not insert spaces into SHA-256 strings.

Submission completeness:

- There is no labeled data-availability or code-availability statement. The Zenodo DOI and file hash appear in the methods. IEEE Access expects a statement.
- The acknowledgment discloses AI-assisted formatting and says experimental numbers were not generated by the tools. That disclosure should stay.
- Ethics and privacy are partial: `id`, `zip_code`, `addr_state`, and `revenue` are identified as sensitive in `docs/dataset_card.md`, and the manuscript calls state and ZIP quasi-identifiers. There is no formal ethics or consent statement. The data are a public historical extract; the statement still needs to say what was not published (raw free text, row-level scores).
- Citation order in the bibliography is not numerical. That is a production defect, not a scientific one.
- Three manuscript variants plus a gitignored duplicate increase the chance that a later edit lands in only one file.

Compilation success and passing safety tests do not make the paper camera-ready or scientifically complete.

## L. Prioritized Findings Register

### B-01 — Lead design question is not answered

- Severity: `BLOCKER`
- Location: Section I design-question quote; abstract opening; Section III contribution list; Section IX paragraph that begins “The design question in Section I”.
- Evidence: identical `p_selected` across maps (`results/decision/v2/frozen_policy.json`, fused and monolithic TEST JSON); no expert, user, or adverse-action study; Section IX’s own partial-address sentence.
- Why it matters: the quoted question asks for greater transparency, greater defensibility, and no material predictive sacrifice versus a monolithic classifier. Transparency and defensibility were not measured. Predictive equality is true because the maps share one score vector. A reviewer can desk-reject or demand a new study because the paper’s question and its evidence do not match.
- Correctable from existing evidence: rewrite the question to the three results the files support: layers can be stored separately; Platt does not change ROC-AUC; the G0 map changes counts under universal `INSUFFICIENT_INFORMATION`.
- Requires new work: any empirical test of transparency, defensibility, or policy quality.
- Action: replace the quote before submission. Keep the Section IX admission until the quote is gone.

### M-01 — EBM selection can be read as a predictive win

- Severity: `MAJOR`
- Location: abstract sentence “validation selected the EBM”; Section IV baseline-model paragraph.
- Evidence: `experiments/stage4b_credit_risk/selected_configurations.json` ranks XGBoost ahead of the EBM; `docs/STAGE_4B_MODELING_REPORT.md` Section I states the Brier gap is expected because only the EBM is unweighted; `results/metrics/stage4b_test_metrics.json` gives XGBoost the higher TEST ROC-AUC and PR-AUC.
- Why it matters: the tie-break that selects the EBM uses Brier on probability scales that the training objectives did not share. The abstract omits the rule.
- Correctable from existing evidence: state the weighting incomparability, the XGBoost rank on PR-AUC and ROC-AUC, and that the EBM is the additive reference retained inside the predeclared window.
- Requires new work: a validation-only comparison with a common probability objective. That comparison must not use TEST for selection.
- Action: narrow the sentence. Do not refit on TEST.

### M-02 — Resolved-loan and origination-time limits

- Severity: `MAJOR`
- Location: dataset subsection; limitations item on selection bias.
- Evidence: `docs/lendingclub_leakage_audit.md` on `issue_d`; target audit on excluded transitory statuses; year default rates in the manuscript year table and `results/stage10/v1/metrics/s10_r1_year.json`.
- Why it matters: discrimination, calibration drift, and the 2018 PR-AUC drop can be properties of who reached a resolved status, not of a full applicant population at decision time.
- Correctable from existing evidence: state origination-time indexing, rejected-applicant exclusion, and resolved-only selection, and connect them to the stored 2017 versus 2018 prevalence gap.
- Requires new work: reject inference or an application-time book with a fixed outcome horizon.
- Action: add the interpretation. Do not invent a censoring model.

### M-03 — Target documentation conflict is named and not shown

- Severity: `MAJOR`
- Location: dataset subsection; limitations list.
- Evidence: `results/metrics/lendingclub_target_audit.json` field `documentation_conflict`.
- Why it matters: Default = 1 may not be a single original `loan_status`. All ROC, PR, Brier, and decision metrics inherit that label.
- Correctable from existing evidence: quote the frozen conflict in the methods. Keep `original_loan_status_mapping_verified: false`.
- Requires new work: a row-level map to original Lending Club status, which this extract does not contain.
- Action: disclose the two depositor sentences. Do not relabel TEST.

### M-04 — Residual feature-timing ambiguity

- Severity: `MAJOR`
- Location: feature-policy subsection, sentence that newly discovered leakage is recorded as none.
- Evidence: `docs/lendingclub_leakage_audit.md` rows for `dti_n` and `issue_d`.
- Why it matters: `dti_n` is a model feature with medium-confidence application-time status. The current sentence reads as a closed leakage audit.
- Correctable from existing evidence: cite the medium-confidence flag and the origination-month clock.
- Requires new work: a data dictionary that settles `dti_n` timing.
- Action: qualify the leakage sentence.

### M-05 — Abstract omits the 2018 calibration reversal

- Severity: `MAJOR`
- Location: abstract Platt ECE sentence; results temporal paragraph; limitations item on 2018 Platt ECE.
- Evidence: `results/calibration/metrics/stage5_temporal.json`.
- Why it matters: the pooled ECE improvement is the calibration result a reviewer will remember. On the later test year, Platt increases ECE from about 0.010 to about 0.062 and also increases Brier.
- Correctable from existing evidence: put the 2018 reversal next to the pooled numbers in the abstract or in the first calibration claim.
- Requires new work: a nested or year-aware calibrator, fit without TEST, if the authors want a stronger calibration claim. The present claim does not require that fit.
- Action: qualify the abstract. Keep the frozen Platt map.

### M-06 — Repeated use of the same TEST rows

- Severity: `MAJOR`
- Location: Section V protocol table; Section VI year, ablation, and Stage 10 displays.
- Evidence: protocol authorization classes in the manuscript; `results/stage10/v1/metrics/s10_a1_gap.json` field `confirmatory_experiment: false`.
- Why it matters: many descriptive cuts of one TEST set can look like a family of confirmed findings.
- Correctable from existing evidence: keep the non-confirmatory labels and move post-hoc cuts out of the main result claim.
- Requires new work: a later cohort that was not used to design the maps, if a confirmatory policy claim is desired.
- Action: do not add another TEST-based selection or threshold search.

### M-07 — Regulatory paraphrases rest on unauthenticated copies

- Severity: `MAJOR`
- Location: related-work Shariah subsection; governance layer table; references [24]–[31].
- Evidence: acquisition ledger; protocol draft Sections A–E; `src/shariah/applicability.py`; catalog `validation_status` values `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW`.
- Why it matters: a paraphrase of a PICG or MUFAP PDF can be quoted later as what SBP or SECP requires. HTTP 403 does not decide applicability. No expert has endorsed the encoding.
- Correctable from existing evidence: keep every operative sentence tied to the named unauthenticated copy, and keep the six rules at `SCOPE_UNKNOWN`.
- Requires new work: official bytes and qualified review under the existing protocol.
- Action: do not strengthen legal or religious wording.

### M-08 — Literature gap is a statement about a local register

- Severity: `MAJOR`
- Location: Section II opening; Section III first two paragraphs; limitations literature item.
- Evidence: bibliography years in the manuscript; the manuscript’s own “recorded literature sources” qualifier.
- Why it matters: IEEE Access reviewers treat an unevidenced novelty claim as a contribution failure. The paper already refuses absolute novelty, then still uses the register gap as the contribution setup.
- Correctable from existing evidence: make the prototype the contribution and demote the register observation to a limitation.
- Requires new work: an external literature verification. This audit names no new papers.
- Action: stop short of field-level novelty.

### M-09 — Experimental results are not reproducible from a clean checkout

- Severity: `MAJOR`
- Location: limitations items on `git_commit`, the missing M-4B digest, and pytest scope; methods data paragraph.
- Evidence: `.gitignore` entries for `data/raw/` and `results/calibration/test/`; `requirements.txt`; `audit/lendingclub_split_manifest.json` `git_commit: null`.
- Why it matters: a reader of HEAD cannot rebuild the score file or rerun Stage 4B–8 from the committed tree alone.
- Correctable from existing evidence: state the ignored paths, the public Zenodo DOI, the quoted score hash, and the snapshot-commit boundary.
- Requires new work: pinned environment, a data-availability package that does not leak forbidden row dumps, and a recorded M-4B digest if the joblib still exists. Do not regenerate TEST to fill the digest.
- Action: write the availability statement from facts already known.

### m-01 — Abstract count line can still be skimmed as Shariah rejects

- Severity: `MINOR`
- Location: abstract decision-count sentence.
- Evidence: G0 table; `fused_test.json` HIGH band \(n=27\).
- Why it matters: the body identifies the 27 rejects. A skim of the abstract may not.
- Correctable from existing evidence: add “HIGH credit band” to that sentence.
- Requires new work: none.
- Action: one clause.

### m-02 — Main tables omit stored intervals

- Severity: `MINOR`
- Location: M-4B family table; M-5 calibration table.
- Evidence: bootstrap objects in `stage4b_test_metrics.json` and `stage5_test_metrics.json`.
- Why it matters: point estimates look more precise than the stored uncertainty.
- Correctable from existing evidence: add the stored intervals or point to them.
- Requires new work: none. Do not run a new bootstrap.
- Action: transcribe.

### m-03 — Figure bars are rounded relative to the tables

- Severity: `MINOR`
- Location: Figure 3 labels versus Table III.
- Evidence: rendered page 11 shows 0.6854, 0.6799, and 0.6777; JSON values are longer.
- Why it matters: a reader can think the figure and the table disagree.
- Correctable from existing evidence: say the labels are rounded to four decimals.
- Requires new work: none.
- Action: caption clause. Do not redraw from TEST scores unless the figure is rebuilt only from the stored point estimates.

### m-04 — No data and code availability statement

- Severity: `MINOR` for a draft; it becomes a submission blocker at the IEEE checklist, so it is listed here as presentation completeness rather than as a false scientific claim.
- Location: end matter.
- Evidence: Zenodo DOI in the methods; repository gitignore behavior in Section J.
- Why it matters: Access requires the statement.
- Correctable from existing evidence: add a statement that names the DOI, the unavailable row-level score dump, and the code snapshot boundary.
- Requires new work: none to write the truthful statement.
- Action: add the statement when manuscript edits are next authorized.

### m-05 — Typesetting residue

- Severity: `MINOR`
- Location: abstract; small overfull boxes recorded in the STEP 3B-9B log; gitignored duplicate.
- Evidence: log warnings listed in Section K; duplicate SHA equal to the canonical file and ignored by `.gitignore` line 89.
- Why it matters: production, not inference.
- Correctable from existing evidence: a later typesetting pass.
- Requires new work: none scientific.
- Action: do not treat the 16-page PDF as camera-ready.

### m-06 — ZIP attributions and fairness are unassessed

- Severity: `MINOR`
- Location: attribution table; limitations fairness item.
- Evidence: `zip_code` in the explained feature list; no fairness processor was run.
- Why it matters: an explanation that highlights ZIP can be read as an adverse-action reason.
- Correctable from existing evidence: say the attribution table is not a reason-code study.
- Requires new work: a fairness or reason-code review.
- Action: one limiting sentence.

### A-01 — Public credit data are not an Islamic-finance benchmark

- Severity: `ACCEPTABLE LIMITATION`
- Location: abstract, dataset table, UCI subsection, conclusion.
- Evidence: L1 JSON missing contract fields; UCI target definition.
- Why it matters: it bounds every governance sentence.
- Correctable from existing evidence: already disclosed, and must stay disclosed.
- Requires new work: only if the claim is widened.
- Action: retain.

### A-02 — Additive agreement is an identity

- Severity: `ACCEPTABLE LIMITATION`
- Location: explainability results.
- Evidence: `shap_vs_ebm_agreement.json`.
- Why it matters: the paper already refuses a second-model confirmation.
- Correctable from existing evidence: already stated.
- Requires new work: a human or regulatory explanation study, if that claim is added.
- Action: retain.

### A-03 — A1 is an evidence-gap simulation

- Severity: `ACCEPTABLE LIMITATION`
- Location: results fusion subsection; conclusion.
- Evidence: fused TEST JSON; G0 matrix.
- Why it matters: 208,859 reviews and 27 rejects are map outputs under missing fields.
- Correctable from existing evidence: already stated in the body.
- Requires new work: real contracts, if the claim is widened.
- Action: retain, and apply m-01 in the abstract.

### A-04 — Engine v1 counts and live v2 screen stay separate

- Severity: `ACCEPTABLE LIMITATION`
- Location: governance subsection; limitations.
- Evidence: audit JSON engine strings; `ENGINE_VERSION` in `src/shariah/engine.py`.
- Why it matters: mixing them would rewrite history.
- Correctable from existing evidence: already stated.
- Requires new work: none to preserve the distinction. Regenerating TEST with v2 would be a new experiment and is not authorized.
- Action: retain.

### A-05 — UCI XGBoost remains exploratory

- Severity: `ACCEPTABLE LIMITATION`
- Location: abstract; UCI subsection; `family_selection.json`.
- Evidence: `DEVIATION-001` labeling; `xgboost_ratified` false in the side-by-side record.
- Why it matters: UCI XGBoost ROC-AUC 0.773 is the largest discrimination number in the paper and is easy to promote.
- Correctable from existing evidence: the label already exists.
- Requires new work: a pre-registered confirmatory UCI protocol, if someone wants that promotion. It must not be decided on the current TEST selection.
- Action: retain the exploratory label.

### A-06 — HTTP 403 is a failed download

- Severity: `ACCEPTABLE LIMITATION`
- Location: regulatory subsection; ledger.
- Evidence: acquisition ledger statuses.
- Why it matters: a block page must not become a legal conclusion.
- Correctable from existing evidence: the manuscript already treats 403 as non-retrieval.
- Requires new work: a successful official acquisition.
- Action: retain.

## M. Minimal Remediation Plan

### A. Mandatory before a defensible submission

1. Replace the Section I question with the narrower questions the files answer. Align the title, abstract, contributions, and conclusion with that wording.
2. State that EBM selection was a predeclared PR-AUC window plus a Brier tie-break across differently weighted families, and that stored TEST ROC-AUC and PR-AUC are higher for LendingClub XGBoost.
3. Place the 2018 Platt reversal beside the pooled calibration claim.
4. Identify the 27 A1 rejects as the credit HIGH band under universal `INSUFFICIENT_INFORMATION`.
5. Quote the target-documentation conflict and the origination-time / resolved-only limits.
6. Qualify the leakage sentence with the `dti_n` timing flag.
7. Demote the literature-register gap so it is not the contribution.
8. Add a data and code availability statement that matches the gitignore and the Zenodo DOI.
9. Keep every SBP/SECP/AAOIFI sentence inside the current authentication and expert-review fences.

These nine items use existing evidence. They do not require a new model.

### B. Improvements from frozen evidence

- Transcribe stored bootstrap intervals into the main tables.
- Label Figure 3 as four-decimal rounding of stored point estimates.
- State that M-4B ECE and the M-4B joblib digest are absent.
- Note that expected-cost fields use an assumed scenario and different review-cost settings, so they are not a policy ranking.
- Proofread hash line breaks and the abstract overflow in a later typesetting pass.

### C. Work that needs new experimental authorization

- A validation-only, probability-comparable family comparison. TEST must not choose the family.
- A validation-only recalibration designed for the 2018 shift. TEST must not choose the calibrator.
- Any new threshold search. The frozen 0.06 / 0.69 / 0.16 values stay frozen unless a new validation-only protocol is authorized.
- A confirmatory cohort that was not used to design the maps.

No proposed experiment may reuse protected TEST for model selection or threshold optimization.

### D. Work that needs an external institution, regulator, or qualified expert

- Official SBP and SECP bytes, followed by clause and applicability review under the existing protocol.
- Independent qualified review before any rule leaves `SCOPE_UNKNOWN`.
- A human study of explanation usefulness or adverse-action reason quality.
- An external literature check beyond the frozen register. This audit does not supply the missing citations.

### E. Optional future research

- An Islamic-finance benchmark with contract fields and expert labels.
- Reject inference or a fixed-horizon outcome definition.
- Fairness constraints.
- German Credit or Australian Credit as additional executed datasets. They are not required for the narrowed prototype claim.

A defensible engineering paper is possible without new Islamic-finance data if, and only if, the claims stay inside these limits:

- The paper reports a prototype on a public US consumer-credit extract and a separate UCI credit table.
- Predictive results are descriptive performance of frozen models, with M-4B and M-5 kept distinct, and with no claim that the EBM won on ROC-AUC.
- Calibration results include the pooled change and the 2018 reversal.
- Explanations are additive reconstructions of one model on 5,000 rows.
- Governance results are an evidence-gap simulation: no applicant is approved, 208,859 rows are simulated reviews, and 27 high-score rows are rejected by the credit band while every governance status is `INSUFFICIENT_INFORMATION`.
- The paper does not claim Shariah compliance, regulatory applicability, expert validation, ECOA compliance, fraud performance, or fairness.

Acceptance is not guaranteed under those limits.

## N. Questions Requiring External Evidence

1. What is the official text and version of the SBP and SECP instruments, and which institution, product, and date do they govern?
2. Do qualified reviewers endorse the software encoding of any source rule?
3. Can the Zenodo positive class be tied to original Lending Club `loan_status` values?
4. Was `dti_n` known at the application decision, or does “Monthly information” mean a later measurement?
5. Would a credit practitioner or a Shariah reviewer find the additive terms usable as reasons?
6. Does the current credit-scoring and Islamic-finance literature, outside this register, already contain the architecture this paper assembles?

None of these questions is answered by the safety tests or by the compiled PDF.

## O. Recommendation on Submission Readiness

Do not submit the manuscripts in their current scientific framing.

The numerical spine of the credit, calibration, fusion, and UCI tables is traceable to files on disk, and the paper already contains many of the right caveats in the body. The lead question, the abstract’s model-selection and calibration sentences, the unresolved label and timing limits, the unauthenticated regulatory paraphrases, the register-relative novelty setup, and the inability to reproduce the experiments from a clean checkout are enough to draw a major revision or a desk rejection.

The smallest scientifically defensible next paper is a prototype and evidence-traceability paper with the claim limits in Section M. New Islamic-finance data are not required for that paper. They are required before any stronger governance claim.

This audit is not a certificate of correctness, not a Shariah determination, and not a prediction of peer-review outcome.
