# Stage 6 Explainability Report

## A. Explanation methodology

The frozen Stage 4B model is an Explainable Boosting Machine with `interactions=0`. It is used here as a **transparent-model reference**, not as ground truth, not as a causal explanation, and not as an authoritative explanation.

SHAP values are **model attributions** for this EBM, not causal effects and not proof that a feature causes default.

TreeSHAP was not used: it is not mathematically appropriate for this EBM. `shap.AdditiveExplainer` is the matching SHAP algorithm for a first-order GAM, but shap 0.52's Independent masker does not accept mixed string categoricals, and encoding categories as floats broke additivity in a probe. Stage 6 therefore computes the closed-form additive interventional SHAP on the EBM logit/link scale:

`phi_i(x) = g_i(x_i) - mean_{TRAIN} g_i`

where `g_i` are native EBM term contributions from `eval_terms`. For a first-order additive model this is the Shapley value of feature i. Output space: EBM `decision_function` (logit/link). Probability is `sigmoid(decision)`. Platt calibration is a later monotone map `sigmoid(a * logit(p_raw) + b)` and is not inside the EBM.

Explanation sample: 5000 TEST rows, `RandomState(42)` without replacement. Labels were not used to draw the sample or to choose local cases.

SHAP config: {"shap_library_version": "0.52.0", "explainer_type": "exact_additive_shap_from_ebm_terms", "shap_explainer_class_used": null, "tree_shap": false, "tree_shap_reason": "EBM is a first-order GAM of bin terms, not a TreeSHAP-compatible forest.", "additive_explainer_not_used_reason": "shap.AdditiveExplainer is the matching algorithm, but shap's Independent masker does not accept mixed string categoricals; float-encoding categories broke additivity.", "output_space": "ebm_decision_function_logit_link", "link_function": "EBM logit/link; probability is sigmoid(decision_function)", "background": "TRAIN rows after Stage 4A train-only imputation; mean term values", "additive_identity": "phi_i(x) = g_i(x_i) - mean_TRAIN g_i", "n_explained_observations": 5000}

## B. Global attribution

| Feature | SHAP mean(|value|) | SHAP rank | EBM mean(|contribution|) | EBM rank |
| --- | --- | --- | --- | --- |
| fico_n | 0.307210 | 1 | 0.307210 | 1 |
| loan_amnt | 0.288771 | 2 | 0.288771 | 2 |
| dti_n | 0.150847 | 3 | 0.150847 | 3 |
| revenue | 0.144974 | 4 | 0.144974 | 4 |
| home_ownership_n | 0.122529 | 5 | 0.122529 | 5 |
| zip_code | 0.119795 | 6 | 0.119795 | 6 |
| purpose | 0.102574 | 7 | 0.102574 | 7 |
| emp_length | 0.039840 | 8 | 0.039840 | 8 |
| addr_state | 0.007290 | 9 | 0.007290 | 9 |

SHAP values are TRAIN-centered EBM terms (`phi_i = g_i - mean_TRAIN g_i`). Uncentered EBM magnitudes are `mean(|g_i|)` on the same explanation sample. Max `|mean_TRAIN g_i|` was 6.184e-17, so the two global mean-absolute series are numerically identical at reported precision. This is a property of the fitted additive EBM, not evidence from a second model class. Ranks remain the primary comparison; raw magnitude is not treated as a second confirmatory scale.

The model attributes the largest mean |SHAP| to `fico_n`, then `loan_amnt`, `dti_n`, `revenue`, and `home_ownership_n`. `addr_state` has the smallest mean |SHAP|. These are attributions of this EBM, not causes of default.

## C. SHAP vs EBM comparison

| Top-k | Overlap | Spearman correlation |
| --- | --- | --- |
| 3 | 1.000 | 1.0000 |
| 5 | 1.000 | 1.0000 |
| 9 | 1.000 | 1.0000 |

Spearman rank correlation (full ranking): 1.0000. Kendall tau: 1.0000. Normalized Spearman footrule: 0.0000.

Sign agreement between SHAP values and **centered** EBM terms (identity for this explainer): 1.0000.
Sign agreement between SHAP values and **uncentered** EBM terms: 1.0000.

EBM is used as a transparent-model reference for attribution comparison, not as ground truth. Perfect rank agreement is expected because additive SHAP is the centered EBM term vector. It is not independent confirmation from a second attribution method or a second predictive model.

## D. Local explanations

Cases were selected from the explanation sample by a frozen rule: maximum raw probability, minimum raw probability, closest to the sample median raw probability, and lowest Spearman correlation between local |SHAP| and local |EBM term| rankings. Ties broken by `row_ref`. Labels were not used.

| Case | Raw probability | Calibrated probability | Top positive (SHAP) | Top negative (SHAP) |
| --- | --- | --- | --- | --- |
| High raw p | 0.518678 | 0.681220 | dti_n, fico_n, zip_code | loan_amnt |
| Low raw p | 0.023737 | 0.022185 | addr_state | fico_n, loan_amnt, revenue |
| Median raw p | 0.161614 | 0.213524 | fico_n, emp_length, purpose | loan_amnt, home_ownership_n, zip_code |
| Deterministic lowest |SHAP| vs |EBM| rank correlation | 0.329655 | 0.454852 | loan_amnt, dti_n, zip_code | revenue, purpose, home_ownership_n |

The fourth case is selected by a frozen rule (lowest Spearman of local |SHAP| vs |EBM term| ranks; ties broken by `row_ref`), not by inspecting plots. Observed local Spearman for that case: 1.0. Because TRAIN-mean EBM terms are numerically ~0, local SHAP rankings match local |EBM term| rankings; no substantial SHAP-vs-EBM rank disagreement exists in the sample.

True labels are stored only as descriptive context in the case JSON and were not used to choose or alter explanations.

## E. Seed stability

| Feature | Mean SHAP importance | SD | Mean rank | Rank SD | Top-3 frequency | Top-5 frequency |
| --- | --- | --- | --- | --- | --- | --- |
| fico_n | 0.307718 | 0.000522 | 1.00 | 0.00 | 1.00 | 1.00 |
| loan_amnt | 0.287129 | 0.001076 | 2.00 | 0.00 | 1.00 | 1.00 |
| dti_n | 0.150520 | 0.001035 | 3.00 | 0.00 | 1.00 | 1.00 |
| revenue | 0.144545 | 0.000789 | 4.00 | 0.00 | 0.00 | 1.00 |
| home_ownership_n | 0.122837 | 0.000998 | 5.00 | 0.00 | 0.00 | 1.00 |
| zip_code | 0.119613 | 0.000559 | 6.00 | 0.00 | 0.00 | 0.00 |
| purpose | 0.102317 | 0.000348 | 7.00 | 0.00 | 0.00 | 0.00 |
| emp_length | 0.040118 | 0.000696 | 8.00 | 0.00 | 0.00 | 0.00 |
| addr_state | 0.007028 | 0.000154 | 9.00 | 0.00 | 0.00 | 0.00 |

Pairwise Spearman between seeds (mean): 1.0000. Mean pairwise top-3 overlap: 1.0000. Mean pairwise top-5 overlap: 1.0000. Reported as mean ± SD across the five frozen seeds. No seed was selected as best.

## F. Calibration relationship

Platt is `sigmoid(a * logit(p_raw) + b)` with a=1.198826, b=0.669777. Because a>0 this is a strictly increasing map of the EBM probability and an affine map of the EBM logit (logit(p_cal) = a * decision + b). Additive SHAP on logit(p_cal) equals a times SHAP on the raw decision, so feature rankings are identical. Platt was applied to probabilities only; EBM intercept -1.557056 and term_importances were unchanged. Calibration changed probability values; it did not change the EBM's internal additive attribution structure.

## G. Feature effects

| Feature | Type | Observed pattern | Attribution scale |
| --- | --- | --- | --- |
| fico_n | continuous | Fitted term tends to decrease as fico_n increases (bin-level Pearson=-0.99); not a causal claim. | EBM additive term on logit/link scale |
| loan_amnt | continuous | Fitted term tends to increase as loan_amnt increases (bin-level Pearson=0.96); not a causal claim. | EBM additive term on logit/link scale |
| dti_n | continuous | Fitted term is not approximately monotone in dti_n (bin-level Pearson=0.40). | EBM additive term on logit/link scale |
| revenue | continuous | Fitted term is not approximately monotone in revenue (bin-level Pearson=-0.25). | EBM additive term on logit/link scale |
| home_ownership_n | categorical | Category-specific terms on the logit scale; home_ownership_n is not a numeric magnitude. Largest negative fitted term: MORTGAGE. Largest positive fitted term: RENT. | EBM additive term on logit/link scale |

ZIP codes and other categoricals are identities, not numeric distances. Associations are model attributions, not causes of default.

## H. Limitations

- Attributions describe this EBM, not the data-generating process.
- Additive SHAP equals centered EBM terms. Agreement is expected; it is not independent confirmation from a second model class.
- KernelSHAP on the probability scale was not used, so probability-space SHAP rankings were not estimated separately.
- The explanation sample is 5,000 TEST rows, not the full test set.
- Stage 6 uses the TRAIN-only EBM that Stage 5 calibrated. Stage 4B test metrics used a TRAIN+VALIDATION refit; those two EBMs are not mixed here.
- High-cardinality `zip_code` effect plots show the largest-magnitude categories only.
- No Shariah, threshold, or decision-policy analysis was performed.

## I. Reproducibility

- explainability_experiment_id: `stage6-lc-ebm-explain-v1`
- dataset_hash: `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc`
- split_manifest_hash: `d4db2099199258ae5ca4f5a85a7ce8e7dde2943a0bf7b9239212cce1e44d0e70`
- preprocessing_policy_hash: `3435a985086eccdfb548b6dff88c4fadaa6c060250237dcc759be3db64b44fd9`
- git_commit: `None`
- libraries: {"python": "3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]", "pandas": "3.0.5", "numpy": "2.5.2", "sklearn": "1.9.0", "interpret": "0.7.8", "shap": "0.52.0", "matplotlib": "3.11.1", "joblib": "1.6.0"}
- sample_seed: 42; sample_n: 5000; model seeds: [42, 123, 2024, 3407, 9999]

## J. Tests

........................................................................ [ 92%]
......                                                                   [100%]
============================== warnings summary ===============================
tests/test_stage4b_modeling.py::test_seeds_reproduce_logistic_within_tolerance
tests/test_stage4b_modeling.py::test_seeds_reproduce_logistic_within_tolerance
  C:\Users\User\AppData\Local\Programs\Python\Python312\Lib\site-packages\sklearn\linear_model\_logistic.py:1403: FutureWarning: 'penalty' was deprecated in version 1.8 and will be removed in 1.10. To avoid this warning, leave 'penalty' set to its default value and use 'l1_ratio' or 'C' instead. Use l1_ratio=0 instead of penalty='l2', l1_ratio=1 instead of penalty='l1', l1_ratio set to a float between 0 and 1 instead of penalty='elasticnet', and C=np.inf instead of penalty=None.
    warnings.warn(

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
78 passed, 2 warnings in 50.18s

## K. Stage gate

`STAGE_6_STATUS = PASS`

Explainability experiments completed with a valid additive SHAP method for EBM; tests passed.

Stage 7 was not started.

