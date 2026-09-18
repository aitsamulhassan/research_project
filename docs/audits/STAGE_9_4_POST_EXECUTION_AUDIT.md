# Stage 9.4 post-execution audit

| Item | Value |
| --- | --- |
| **Audit ID** | `STAGE-9.4-POST-EXECUTION-AUDIT` |
| **Audit date** | 2026-09-15 |
| **Audit type** | Documentation / artifact inspection only |
| **Experiments rerun** | **No** |
| **Models retrained** | **No** |
| **Calibration refit** | **No** |
| **Stage 9.4 results modified** | **No** |
| **Original Stage 9.4 report modified** | **No** |

This audit independently inspects already-executed Stage 9.4 artifacts. It does **not** assume `docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md` is correct because it says `PASS`.

**Final classification: B. PASS WITH DOCUMENTATION/REPRODUCIBILITY LIMITATION**

---

## 1. Authorization verification

**Sources:** `docs/amendments/AMENDMENT-STAGE9-4-AUTHORIZATION.md`; `audit/stage9_4_uci_run.json`; chat-recorded owner approval (2026-09-15); Stage 9 protocol freeze table U1.

| Check | Result |
| --- | --- |
| Amendment file exists | **Yes** |
| Status | **`APPROVED`** (header line and status field) |
| Approval date | **2026-09-15** |
| Approver | Research owner (recorded via chat instruction) |
| Approved before Stage 9.4 execution artifacts | **Yes.** Amendment file mtime precedes `results/uci_generalization/v1/` TEST tables and `docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md`. Run `started` `2026-09-15T19:07:00+00:00`. |
| Runner does not write the amendment / protocol / constitution | **Yes** (source inspection of `experiments/stage9_4_uci_generalization/run_stage9_4.py`) |
| `audit/stage9_0_experimental_freeze.json` still records freeze-time `stage9_execution: NOT AUTHORIZED` | **Yes** (historical freeze not rewritten) |

**Scope match (mostly yes, with one documented expansion):**

The amendment authorizes UCI independent generalization: frozen stratified split, no LC merge, no LC threshold transfer, UCI-only train/val fitting, Stage 5 calibration rule, UCI TEST protected until after freeze, U3 metadata-only L1, no L2, no invented calendar time.

**Inconsistency (not silently ignored):** frozen U1 and the approved amendment text say **EBM + L2 logistic regression only** (“not a four-family competition”). The executed candidate set is **logistic regression, EBM, and XGBoost**, as stated in the owner’s Stage 9.4 execution instruction and in the Stage 9.4 report. There is **no dated successor amendment** that records that candidate-set expansion. Random forest was not run (so it is not a four-family bake-off).

This is a **process/documentation gap**, not evidence that Stage 9.4 ran while the amendment was still `DRAFT`. The same research owner who set `APPROVED` then instructed the three-family set. Paper language must **not** describe XGBoost as part of the frozen U1 confirmatory protocol.

Authorization records were **not** modified by this audit.

---

## 2. Frozen split verification

**Sources (read-only; split not recreated):** `audit/uci_split_manifest.json`; `results/tables/uci_split_assignments.csv`; `results/metrics/uci_split_summary.json`; `data/raw/default+of+credit+card+clients.zip`.

Membership hashes were **recomputed from the existing assignment CSV** using the Stage 3 method (`sha256` of sorted `ID\tID` lines). A new split was **not** created.

| Split | Rows (CSV) | Manifest | Prevalence (summary) | Membership hash match |
| --- | ---: | ---: | ---: | --- |
| train | 20999 | 20999 | 0.22120100957188438 | **Yes** `70b1819de66fdae6793691e83224b5dc4e1956c021b582ffcf0a89791c9ac2f1` |
| validation | 4499 | 4499 | 0.22116025783507445 | **Yes** `76a91b4b6fefbfd111d6a7c536ad222330c3bcf0f4358c259e40d4814382bcd4` |
| test | 4502 | 4502 | 0.22123500666370502 | **Yes** `0783db42ac57a277f79379e0a62ef00f2a2b189f868ed993cebdf16def404126` |

Raw zip SHA-256 matches recorded `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602`. `merged_with_lendingclub: false`. `time_index: null`. Stage 9.4 report row counts and prevalences match these artifacts (report rounds prevalence to 6 decimals).

---

## 3. Target semantics verification

| Dataset | Target | Positive | Negative |
| --- | --- | --- | --- |
| UCI | `default payment next month` | 1 = default payment next month | 0 = no default payment next month |
| LendingClub | `Default` | 1 = Charged Off | 0 = Fully Paid |

Stage 3 policy (`docs/uci_feature_policy.csv`) states the UCI target is **not equivalent** to LendingClub `Default`. The Stage 9.4 report §B states they are two separate datasets with two separate targets, reported alongside, not merged, with no test of AUC equality. Config `configs/stage9_4_uci_generalization.yaml` records `target_not_equivalent_to`. **Targets are not treated as identical.**

---

## 4. Preprocessing / leakage audit

**Sources:** `src/preprocessing/uci_preprocessor.py`; runner `main()`; Stage 2 `docs/uci_schema_report.md`; Stage 3 `docs/uci_feature_policy.csv`.

| Control | Evidence |
| --- | --- |
| Preprocessor fit on UCI TRAIN only | `UCIPreprocessor().fit(train_df)` before any TEST slice |
| Validation transformed with train-fit object | `preprocessor.transform(val_df)` after fit on train |
| TEST transformed with the same train-fit object | `preprocessor.transform(test_df)` **after** family and calibrator freeze |
| TEST labels not used in preprocessing | `fit` / `transform` take feature frames; target is not in `UCI_PREDICTORS` |
| Target excluded from predictors | `default payment next month` is `TARGET_ONLY` in the frozen policy and absent from `UCI_PREDICTORS` |
| No LendingClub preprocessor reused | UCI modules do not import `preprocessing.lendingclub_preprocessor`; tests parse AST for that import |
| No LC feature schema transferred | Forbidden LC columns rejected if present; UCI 23-column policy used |

**PAY_0, PAY_2–PAY_6, BILL_AMT\*, PAY_AMT\*:** Stage 2/3 treat these as UCI candidate predictors with timing `UCI_STUDY_WINDOW_NOT_LC_APPLICATION_TIME` (fixed April–September 2005 billing window; `NO_CALENDAR_TIMESTAMPS`). Stage 9.4 uses them as predictors, codes undocumented PAY/EDUCATION/MARRIAGE levels as extra one-hot/nominal levels, and does not recode. That **matches** the frozen UCI policy. It is **not** LendingClub application-time leakage. This audit does **not** reinterpret those fields.

**Not leakage, but a design fact:** `load_uci_with_splits()` loads the full 30,000-row table into memory before slicing. TEST rows exist in that frame; they are not passed to `fit` or to selection metrics until after freeze.

**EBM internal holdout:** EBM `validation_size=0.15` is a holdout **from UCI TRAIN**, not the Stage 3 validation split and not TEST.

---

## 5. Model-selection audit

Only three families appear in `FAMILIES`, the config, validation tables, and TEST family table: logistic regression, EBM, XGBoost. No random forest.

**Declared rule (Stage 4B methodology, applied to UCI validation aggregates):** primary = mean validation PR-AUC; families within 0.005 of best; then lower mean Brier; then simplicity `logistic > ebm > xgboost`.

Stored validation aggregates (`results/uci_generalization/v1/tables/uci_validation_family_aggregates.csv`):

| Family | Val ROC-AUC mean | Val PR-AUC mean | Val Brier mean | Val log loss mean |
| --- | ---: | ---: | ---: | ---: |
| logistic_regression | 0.763567 | 0.520869 | 0.183702 | 0.562443 |
| explainable_boosting_machine | 0.774351 | 0.527686 | 0.138074 | 0.437841 |
| xgboost | 0.776028 | 0.534172 | 0.178710 | 0.543870 |

Best PR-AUC = 0.534172 (XGBoost). EBM PR-AUC is 0.006486 below best, **outside** the 0.005 band. Candidates: `['xgboost']` only. XGBoost selection is **arithmetically consistent** with the declared rule. Selection JSON records `declared_before_test: true` and `test_metrics_not_consulted: true`.

**Internal note, confirmed from stored validation aggregates:** UCI EBM had **better raw validation Brier** (0.138074 vs 0.178710) and better validation log loss, but XGBoost won the **pre-declared PR-AUC** rule. The same pattern appears on stored raw TEST family metrics (EBM Brier 0.137432 vs XGBoost 0.181736). This audit does **not** change the selection rule.

**Limitation:** XGBoost validation metrics are **identical across all five seeds**. With `subsample=1.0` and `colsample_bytree=1.0`, seed robustness for XGBoost is **degenerate**. That table must not be cited as five independent XGBoost fits.

XGBoost `n_estimators` for the train-only freeze is taken from validation early stopping (`best_iteration`). That is **validation** hyperparameter use, not TEST.

---

## 6. Calibration audit

Stage 5 rule (from `docs/STAGE_5_CALIBRATION_REPORT.md` and `experiments/stage5_calibration/run_stage5.py`): validation Brier; 0.001 practical tie; simplicity `raw > platt > isotonic`. UCI reuse: `BRIER_TIE = 0.001` in `src/uci_generalization/stage9_4.py`. LendingClub Platt `a,b` (1.1988… / 0.6698…) were **not** reused. UCI Platt record: `a=0.9373939123374948`, `b=-1.1820132758454134`, `fit_split=validation`.

Stored **validation** calibration (`results/uci_generalization/v1/tables/uci_validation_calibration.csv`):

| Method | Val Brier | Val log loss | Val ECE | Val ROC-AUC | Val PR-AUC |
| --- | ---: | ---: | ---: | ---: | ---: |
| raw | 0.178710 | 0.543870 | 0.195387 | 0.776028 | 0.534172 |
| platt | 0.136998 | 0.434463 | 0.018891 | 0.776028 | 0.534172 |
| isotonic | 0.134862 | 0.428378 | 0.000000 | 0.780610 | 0.524953 |

Best Brier = 0.134862 (isotonic). Gap vs Platt = 0.002136 **> 0.001**, so **not** a tie. Isotonic is the correct frozen choice under the Stage 5 rule. `PlattCalibrator.fit` / `IsotonicCalibrator.fit` reject `split != "validation"`.

Stored **UCI TEST** calibration (reporting only; not used to choose):

| Method | TEST Brier | TEST log loss | TEST ECE | TEST ROC-AUC |
| --- | ---: | ---: | ---: | ---: |
| raw | 0.181736 | 0.551860 | 0.200657 | 0.773351 |
| platt | 0.136406 | 0.435551 | 0.019547 | 0.773351 |
| isotonic | 0.136853 | 0.449533 | 0.017443 | 0.770878 |

**Verified fact:** On UCI TEST, Platt Brier was slightly better than isotonic (0.136406 vs 0.136853), but isotonic remained the correct frozen choice because calibrator selection was performed on validation only.

The original Stage 9.4 report **shows** those TEST numbers in §E. It does **not** spell out the sentence above. That is a documentation gap in the original report. This audit does **not** rewrite the original report.

Validation isotonic ECE = 0 is the known Stage 5 optimism (isotonic fit and scored on the same validation predictions). TEST ECE is the honest calibration comparison.

---

## 7. TEST-protection audit

Runner control flow (source):

1. Fit preprocessor on TRAIN; score families on VALIDATION.
2. `select_family(aggregates)` using validation PR-AUC only.
3. Train-only seed-42 freeze; `fit_calibrators(..., y_va)`; `select_calibrator` on validation Brier.
4. **Then** `split_xy(table, "test")`, transform TEST with the frozen preprocessor, score.

No UCI TEST metric enters `select_family` or `select_calibrator`. Config states TEST is not used for family/calibrator/hyperparameter selection. Audit flag `test_used_for_selection: false`.

Searched Stage 9.4 code/config for TEST use in selection, LC thresholds, and SHAP training: **no** `t_low`/`t_high`/`t*` search; LC `0.06/0.69/0.16` appear only as **not transferred**. SHAP-vs-EBM is hardcoded `skipped`. No feature selection on TEST. No threshold transfer.

**Post-freeze TEST reporting of all three families** is labeled in the report as not used to choose the family. That is consistent with Stage 4B’s once-after-freeze TEST evaluation. Paper text must not treat that TEST family ranking as the selection rule.

**No TEST leakage found.** Classification **D** is not supported.

---

## 8. Final TEST metric verification

Selected pipeline in artifacts: **XGBoost + isotonic**, `n=4502`.

Compared Stage 9.4 report §E, `results/uci_generalization/v1/metrics/uci_test_selected.json`, `results/uci_generalization/v1/tables/uci_test_calibration.csv` (isotonic row), and `audit/stage9_4_uci_run.json` `uci_test_selected`. **No discrepancy** at stored precision. Metrics were **not** recomputed from models.

| Metric | Stored point | Stored 95% CI | Report (6 d.p.) |
| --- | ---: | --- | ---: |
| ROC-AUC | 0.7708780071798891 | [0.753054, 0.787670] | 0.770878 |
| PR-AUC | 0.5224208622925242 | [0.489710, 0.553604] | 0.522421 |
| Brier | 0.1368528550434721 | [0.131053, 0.143440] | 0.136853 |
| Log loss | 0.449533259034068 | [0.426559, 0.475760] | 0.449533 |
| ECE | 0.01744321566180452 | [0.011304, 0.029490] | 0.017443 |

Bootstrap: 1000 percentile, seed 42, recorded in the TEST calibration table. Report matches.

---

## 9. LendingClub comparison audit

Citation source: `results/calibration/metrics/stage5_test_metrics.json`, method `platt`. SHA-256 `a6c8ab44676d62109c1a346dbcf14a12a745b761f13b9fda6a9002853fc326e3` matches the live file and the Stage 9.4 citation record. Values were **not** recomputed.

| Metric | Cited LC TEST (Platt / EBM) |
| --- | ---: |
| ROC-AUC | 0.6776693941139847 |
| PR-AUC | 0.35096314719303284 |
| Brier | 0.15616920271522994 |
| Log loss | 0.48357015583149326 |
| ECE | 0.020267295489117824 |
| n | 208886 |

Report §F uses these numbers (rounded) and states a better UCI number does **not** mean the LendingClub pipeline is inferior. It does **not** claim “UCI proves the LendingClub model is inferior.” Alongside table labels `plain_comparison=better` on all five metrics; that is a **numeric** comparison of two different tasks, which the surrounding prose correctly qualifies.

**Defensible interpretation (preserved):** the credit-risk/calibration *methodology* produced usable ranking and probability quality on a second independent dataset. Populations, features, target definitions, and prevalence differ.

---

## 10. Explainability audit

Stored `results/uci_generalization/v1/tables/uci_ebm_global_attributions.csv`: rank 1 = **PAY_0**, mean |term| 0.477839. Matches the report. Computed on **UCI train** (runner: `ebm_global_stats(..., train_df)`). Scale: logit/link. Report states associations, not causes.

SHAP-vs-EBM: config `out_of_scope`; runner sets `status: "skipped"`; report says **skipped**. No SHAP experiment was added in this audit.

Explainability is for the **EBM** (Tier 2), not the selected XGBoost. That is consistent with the owner instruction (EBM native attributions) and must not be described as explaining the selected XGBoost scores.

---

## 11. Non-claim audit

The Stage 9.4 report explicitly states:

- no Shariah governance evaluation on UCI;
- L1 metadata-only; no L2 fusion; no per-row Shariah rulings;
- no LC threshold transfer; no UCI decision thresholds selected;
- UCI does not validate or invalidate the LendingClub architecture as a whole;
- the experiment tests credit-risk/calibration methodology generalization only;
- UCI is not temporally validated.

Runner/config contain no `from shariah` import. Audit flags: `shariah_evaluation_on_uci: false`, `l2_fusion_on_uci: false`.

---

## 12. Artifact integrity audit

| Artifact | Present | Consistent with report |
| --- | --- | --- |
| `docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md` | Yes | SHA-256 matches audit `report_sha256` |
| `results/uci_generalization/v1/` tables, metrics, predictions, figures | Yes | Numbers in §5–§8 match |
| `audit/stage9_4_uci_run.json` | Yes | Same selected family/calibrator/TEST metrics |
| `configs/stage9_4_uci_generalization.yaml` | Yes | Copied under results v1 |
| Checkpoints under `experiments/stage9_4_uci_generalization/checkpoints/` | Yes | preprocessor, XGBoost, EBM, calibrators |

Audit manifest fields present: split hashes and prevalences; seeds (TEST seed 42; validation seed list in config); `models_trained: true`; `test_used_for_selection: false`; calibrator record (Platt a,b; isotonic thresholds); dataset hash; software versions; protected-file hashes; `git_commit: null`.

**Manifest limitations (do not change scientific numbers):** `git_commit` is null (no repository `.git` at run time). `pytest_summary` currently reads `14 passed in 2.45s`; the first runner pass recorded pytest **before** the audit file existed (13 passed, 1 skipped), and the summary field was later updated. Boolean flags in JSON were initially serialized as `1`/`0` because `bool` is a subclass of `int`; they were rewritten to JSON booleans without rerunning models. Those are **audit-file hygiene** issues, not TEST-metric changes.

---

## 13. Prior-stage protection audit

`protected_hashes_before` equals `protected_hashes_after` in `audit/stage9_4_uci_run.json`. This audit **rehashed the live files**; all 17 protected paths still match, including:

- LendingClub Stage 5 TEST metrics and calibrated TEST CSV
- Stage 4B TEST metrics
- Stage 7 v2 report
- Stage 8 v2 freeze, table3, fusion report
- Stage 8 decision-policy YAML
- Stage 9.0 freeze JSON (still `NOT AUTHORIZED` at freeze time)
- Stage 9.1 / 9.2 / 9.3 reports and run JSON

Those files were **not** modified by this audit.

---

## 14. Test-suite coverage assessment

`tests/test_stage9_4_uci.py` contains **14 tests**. This audit inspected their source. It did **not** rerun pytest as an experiment.

| Concern | What the tests actually do | Coverage |
| --- | --- | --- |
| Split integrity | Re-verify membership hashes, counts, zip hash, no merge/recode | **Strong** |
| Preprocessing | Tiny synthetic frame: undocumented PAY/EDU codes retained; LC columns rejected | **Partial** (not the real 21k-row fit) |
| Model selection | Toy PR-AUC numbers exercise the rule function | **Partial** (does not lock the stored UCI aggregates) |
| Calibration | Calibrators reject `split="test"`; toy Brier tie prefers Platt | **Partial** (does not lock UCI val Brier table) |
| TEST protection | Flags in audit JSON when present; no dynamic trace that TEST metrics cannot enter `select_family` | **Weak–moderate** |
| Artifact integrity | Audit flags; protected hashes vs live files; `n==4502` | **Moderate** |
| Reproducibility | Amendment APPROVED; no LC preprocessor import; runner does not name protocol/constitution files | **Partial** |
| Reported TEST metrics | **Not locked** (no assert on 0.770878 etc.) | **Gap** |
| XGBoost-vs-U1 expansion | **Not tested** | **Gap** |
| Isotonic-vs-Platt TEST Brier | **Not tested** | **Gap** |

“14 passed” is not by itself evidence that TEST was unused or that the reported TEST metrics are correct. The **code-order inspection** and **stored-table cross-check** in this audit are the stronger evidence.

**Recommendations only (not implemented):**

1. Dated amendment recording XGBoost as an owner-specified addition to frozen U1.
2. Tests that lock selected TEST metrics and validation aggregates to stored CSV hashes.
3. A test that `select_family` / `select_calibrator` functions have no TEST-split argument and that TEST scoring in the runner is after those calls (AST/line-order).
4. Paper footnote: XGBoost five-seed table is degenerate; EBM had better Brier; Platt had slightly better TEST Brier than frozen isotonic.
5. Record a git commit in future run audits.

---

## 15. Final classification

**B. PASS WITH DOCUMENTATION/REPRODUCIBILITY LIMITATION**

Not A: U1 vs XGBoost is not in a dated amendment; git commit null; pytest/audit JSON hygiene; tests do not lock TEST numbers; XGBoost seed table is degenerate; original report does not explicitly state the Platt-vs-isotonic TEST Brier fact.

Not C: stored selection and calibration follow the declared validation rules; numbers match artifacts; no correction of Stage 9.4 results is required for validity of the executed protocol.

Not D: no TEST leakage or LC threshold transfer found.

---

## 16. Limitations

- No git commit; no raw Stage 9.4 terminal log in-repo.
- Frozen protocol numbering still lists UCI as Stage 9.5 in §12; this run is Stage 9.4 per the approved amendment’s numbering note.
- Amendment body still contains leftover “draft / before execution” sentences after the status was set to `APPROVED` (authorization-file leftover, not a result rewrite).
- This audit did not reload UCI models or recompute TEST metrics from predictions.
- Selected credit family is XGBoost; EBM attributions do not explain XGBoost scores.

---

## 17. Recommended future actions

Do **not** rerun Stage 9.4 to “fix” Platt vs isotonic on TEST.

Do **not** convert UCI into a Shariah or fusion evaluation.

Before paper drafting: disclose U1 expansion, dataset/target mismatch, methodology-only claim, frozen isotonic despite slightly better TEST Platt Brier, and EBM-vs-XGBoost Brier vs PR-AUC tension.

Stage 9.5–9.7, Stage 10, and paper writing remain out of scope for this audit.
