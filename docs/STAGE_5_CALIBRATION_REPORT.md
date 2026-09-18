# Stage 5 Calibration Report

## A. Calibration protocol

Selected Stage 4B family: Explainable Boosting Machine. Stage 4B model-selection decisions were not changed.

Protocol: TRAIN-only EBM (seed 42, frozen Stage 4B hyperparameters) produces raw probabilities. Platt and isotonic calibrators are fit on VALIDATION raw probabilities and labels only. The calibration method is frozen using validation Brier (with a 0.001 practical-tie rule preferring simpler methods). Frozen calibrators are then applied to TEST raw probabilities. Calibrators were **not** refit on TRAIN+VALIDATION.

Platt form: `sigmoid(a * logit(p_raw) + b)`, unregularized logistic regression (`C=np.inf`, solver `lbfgs`) on `logit(p_raw)`. Stage 4B stored probabilities rather than decision scores, so logit of the probability is the raw score.

Isotonic: `sklearn.isotonic.IsotonicRegression(y_min=0, y_max=1, increasing=True, out_of_bounds='clip')`.

ECE: 10 equal-width bins on [0,1]; empty bins excluded from ECE and MCE.

TRAIN-only EBM vs Stage 4B stored validation probabilities: max abs diff = 9.71445146547012e-17.

## B. Validation results

| Method | Brier | Log Loss | ECE | MCE | ROC-AUC | PR-AUC |
| --- | --- | --- | --- | --- | --- | --- |
| RAW | 0.179908 | 0.541279 | 0.062862 | 0.602342 | 0.665690 | 0.385835 |
| PLATT | 0.174845 | 0.527846 | 0.002212 | 0.026432 | 0.665690 | 0.385835 |
| ISOTONIC | 0.174694 | 0.527392 | 0.000000 | 0.000000 | 0.666144 | 0.382362 |

## C. Selected calibration method

Selected method: `platt`.
Primary criterion is validation Brier. Best Brier=0.174694. Methods within 0.001 (practically indistinguishable): ['platt', 'isotonic']. Among those, simplicity order ['raw', 'platt', 'isotonic'] selected `platt` (Brier=0.174845, log_loss=0.527846, ECE=0.002212).

Selection used validation metrics only. Test metrics were not consulted.

## D. Final test results

| Method | Brier | 95% CI | Log Loss | 95% CI | ECE | 95% CI | MCE | 95% CI | ROC-AUC | PR-AUC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| RAW | 0.157936 | [0.156926, 0.159064] | 0.488086 | [0.485607, 0.490931] | 0.037535 | [0.035998, 0.039307] | 0.384272 | [0.100770, 0.384272] | 0.677669 | 0.350963 |
| PLATT | 0.156169 | [0.155352, 0.157127] | 0.483570 | [0.481567, 0.485824] | 0.020267 | [0.018602, 0.021866] | 0.186947 | [0.044427, 0.407723] | 0.677669 | 0.350963 |
| ISOTONIC | 0.156197 | [0.155384, 0.157154] | 0.483608 | [0.481629, 0.485879] | 0.020046 | [0.018409, 0.021651] | 0.307568 | [0.141740, 0.482337] | 0.677514 | 0.346276 |

Bootstrap: 1000 row resamples, percentile 95% CI, seed 42. Not used for tuning. Negative Brier/log-loss/ECE/MCE differences mean improvement.

ROC-AUC and PR-AUC are reported to check ranking. Platt is a strictly increasing map of `p_raw`, so ROC-AUC and PR-AUC are identical to RAW. Isotonic is piecewise constant and slightly changed ranking (test PR-AUC 0.351 → 0.346). Calibration is not claimed to improve discrimination.

## E. Calibration curves

Validation reliability diagrams: `results/figures/calibration/figure1_validation_reliability`.
Test reliability diagrams for RAW, Platt, and isotonic (reporting only): `results/figures/calibration/figure2_test_reliability`.

## F. Paired differences

| Comparison | Metric | Difference | 95% CI |
| --- | --- | --- | --- |
| RAW vs PLATT | brier | -0.001767 | [-0.002005, -0.001508] |
| RAW vs PLATT | log_loss | -0.004515 | [-0.005181, -0.003845] |
| RAW vs PLATT | ece | -0.017267 | [-0.020730, -0.014170] |
| RAW vs PLATT | mce | -0.197325 | [-0.336627, 0.270316] |
| RAW vs ISOTONIC | brier | -0.001739 | [-0.001976, -0.001480] |
| RAW vs ISOTONIC | log_loss | -0.004477 | [-0.005119, -0.003803] |
| RAW vs ISOTONIC | ece | -0.017488 | [-0.020971, -0.014390] |
| RAW vs ISOTONIC | mce | -0.076704 | [-0.238185, 0.351202] |

Difference = calibrated − raw. Intervals are percentile bootstrap intervals for that difference. This report does not interpret interval exclusion of zero as a hypothesis test p-value.

## G. Temporal robustness

| Method | Year | Brier | Log Loss | ECE |
| --- | --- | --- | --- | --- |
| RAW | 2017 | 0.169738 | 0.516693 | 0.054017 |
| RAW | 2018 | 0.125840 | 0.410288 | 0.010259 |
| PLATT | 2017 | 0.165687 | 0.506010 | 0.005096 |
| PLATT | 2018 | 0.130286 | 0.422546 | 0.061524 |
| ISOTONIC | 2017 | 0.165714 | 0.506079 | 0.004924 |
| ISOTONIC | 2018 | 0.130317 | 0.422499 | 0.061170 |

Year slices are descriptive. Models and calibrators were not refit by year. On 2017, Platt and isotonic reduce Brier and ECE relative to RAW. On 2018 they increase Brier, log loss, and ECE. The validation window is 2016-04 through 2017-01, so this is a temporal transfer failure, not a reason to recode the frozen calibrator.

## H. Seed stability

For each Stage 4B seed, Platt and isotonic were fit on that seed's stored TRAIN-only validation predictions (never test). The same selection rule was applied.

| Seed | RAW Brier | Platt Brier | Isotonic Brier | Selected |
| --- | --- | --- | --- | --- |
| 42 | 0.179908 | 0.174845 | 0.174694 | platt |
| 123 | 0.179905 | 0.174845 | 0.174706 | platt |
| 2024 | 0.179912 | 0.174846 | 0.174700 | platt |
| 3407 | 0.179907 | 0.174845 | 0.174712 | platt |
| 9999 | 0.179902 | 0.174825 | 0.174688 | platt |

## I. Leakage audit

- Calibrator `.fit` methods raise if `split != 'validation'`.
- Selection file is written before test metrics are computed.
- Test labels are used only after freeze, and only to compute reporting metrics.
- No test-set Brier/ECE was used to choose Platt vs isotonic vs raw.
- Feature policy is unchanged; calibration maps a scalar probability and cannot add predictors.
- Stage 4B TRAIN+VALIDATION refit test probabilities were not used, because a calibrator fit on TRAIN-only validation scores is not a valid map for a different (train+val) model.

## J. Tests

64 passed, 2 warnings in 55.69s (`pytest tests/`). The warnings are sklearn 1.9 `FutureWarning` on `LogisticRegression(penalty='l2')` in a Stage 4B unit test, not a Stage 5 failure.

## K. Limitations

- Validation isotonic ECE/MCE near zero is an in-sample artifact: the isotonic map is fit and scored on the same validation predictions. It is not evidence of perfect out-of-sample calibration.
- Validation selection for isotonic is therefore optimistic. The 0.001 Brier-tie rule preferred Platt over isotonic. TEST evaluation is the honest comparison.
- No nested cross-fitting of the calibrator inside TRAIN was used. A TRAIN+VALIDATION model with a nested calibrator was not implemented; the simpler valid protocol was preserved.
- Stage 5 RAW test metrics are from a TRAIN-only EBM and will not match Stage 4B's TRAIN+VALIDATION test numbers.
- ECE/MCE depend on the declared 10 equal-width bins; they are not a universal standard. MCE is dominated by sparse high-probability bins and has wide bootstrap intervals that include both improvement and deterioration.
- Platt uses logit(p_raw) rather than an EBM decision_function object because Stage 4B artifacts store probabilities.
- A calibrator fit on 2016–early-2017 validation scores does not improve 2018 ECE; year-specific recalibration was not performed.
- Decision thresholds and Shariah rules were not applied.

## L. Stage gate

`STAGE_5_STATUS = PASS`

Calibration experiments completed; method frozen on validation; test evaluated once; leakage tests passed.

Stage 6 was not started.

