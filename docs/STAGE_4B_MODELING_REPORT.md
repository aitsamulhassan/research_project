# Stage 4B Modeling Report

## A. Dataset actually used

- Dataset: LendingClub granting-model extract, SHA-256 `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc`
- Predictors: `revenue`, `dti_n`, `loan_amnt`, `fico_n`, `emp_length`, `purpose`, `home_ownership_n`, `addr_state`, `zip_code` (9 frozen fields; Stage 4A matrix width 1023)
- Train rows: 941267
- Validation rows: 197528
- Test rows: 208886
- UCI was not used or merged.

## B. Models executed

{
  "logistic_regression": {
    "family": "logistic_regression",
    "solver": "liblinear",
    "penalty": "l2",
    "C": 1.0,
    "class_weight": "balanced",
    "max_iter": 300,
    "tol": 0.0001,
    "numeric_scaling": "StandardScaler on Stage 4A numeric block only, fit on current training matrix",
    "random_state": 42,
    "imbalance_strategy": "sklearn class_weight='balanced' (n_samples / (n_classes * n_class))"
  },
  "random_forest": {
    "family": "random_forest",
    "n_estimators": 80,
    "max_depth": 12,
    "min_samples_leaf": 100,
    "max_features": "sqrt",
    "class_weight": "balanced",
    "bootstrap": true,
    "n_jobs": 4,
    "random_state": 42,
    "imbalance_strategy": "sklearn class_weight='balanced'",
    "input_representation": "Stage 4A sparse matrix converted to CSC float32. Not densified; sklearn 1.9 RandomForestClassifier accepts sparse CSC.",
    "size_justification": "80 trees, depth 12, leaf 100: small enough for reproducible training on ~941k rows x 1023 features without an uncontrolled search."
  },
  "xgboost": {
    "family": "xgboost",
    "objective": "binary:logistic",
    "eval_metric": "logloss",
    "n_estimators": 300,
    "learning_rate": 0.05,
    "max_depth": 4,
    "min_child_weight": 20,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "reg_lambda": 1.0,
    "reg_alpha": 0.0,
    "scale_pos_weight": 4.352791647236787,
    "tree_method": "hist",
    "random_state": 42,
    "imbalance_strategy": "scale_pos_weight = n_neg/n_pos computed on the current fitting labels only",
    "early_stopping": "validation split only during the train/val phase; not used on test"
  },
  "explainable_boosting_machine": {
    "family": "explainable_boosting_machine",
    "feature_names": [
      "revenue",
      "dti_n",
      "loan_amnt",
      "fico_n",
      "emp_length",
      "purpose",
      "home_ownership_n",
      "addr_state",
      "zip_code"
    ],
    "feature_types": [
      "continuous",
      "continuous",
      "continuous",
      "continuous",
      "nominal",
      "nominal",
      "nominal",
      "nominal",
      "nominal"
    ],
    "interactions": 0,
    "interaction_justification": "Interactions are set to 0 before any test evaluation so EBM remains an additive per-original-feature reference. They are not added to improve test scores.",
    "max_bins": 256,
    "learning_rate": 0.02,
    "max_rounds": 200,
    "outer_bags": 4,
    "inner_bags": 0,
    "validation_size": 0.15,
    "early_stopping_rounds": 20,
    "random_state": 42,
    "imbalance_strategy": "none (EBM 0.7.8 has no class_weight argument; labels are used as observed)",
    "input_representation": "Stage 4A train-only (or train+val) imputers applied to the original 9 columns; one-hot expansion is not used because it would destroy EBM additive structure and exceed practical memory on 1023 dense dummy columns."
  }
}

## C. Validation results

### Per seed

| Model | Seed | ROC-AUC | PR-AUC | Brier | Log Loss |
| --- | --- | --- | --- | --- | --- |
| logistic_regression | 42 | 0.662147 | 0.378807 | 0.229471 | 0.650576 |
| logistic_regression | 123 | 0.662147 | 0.378807 | 0.229471 | 0.650576 |
| logistic_regression | 2024 | 0.662147 | 0.378807 | 0.229471 | 0.650576 |
| logistic_regression | 3407 | 0.662147 | 0.378807 | 0.229471 | 0.650576 |
| logistic_regression | 9999 | 0.662147 | 0.378807 | 0.229471 | 0.650576 |
| random_forest | 42 | 0.653065 | 0.370677 | 0.240311 | 0.673645 |
| random_forest | 123 | 0.652262 | 0.369865 | 0.239825 | 0.672647 |
| random_forest | 2024 | 0.650986 | 0.369041 | 0.240236 | 0.673498 |
| random_forest | 3407 | 0.649763 | 0.368382 | 0.240486 | 0.673981 |
| random_forest | 9999 | 0.650886 | 0.368516 | 0.240759 | 0.674560 |
| xgboost | 42 | 0.669672 | 0.388646 | 0.224535 | 0.638885 |
| xgboost | 123 | 0.669633 | 0.388473 | 0.224599 | 0.638987 |
| xgboost | 2024 | 0.669660 | 0.388436 | 0.224635 | 0.639069 |
| xgboost | 3407 | 0.669488 | 0.388415 | 0.224701 | 0.639195 |
| xgboost | 9999 | 0.669412 | 0.388393 | 0.224648 | 0.639106 |
| explainable_boosting_machine | 42 | 0.665690 | 0.385835 | 0.179908 | 0.541279 |
| explainable_boosting_machine | 123 | 0.665710 | 0.385749 | 0.179905 | 0.541256 |
| explainable_boosting_machine | 2024 | 0.665655 | 0.385851 | 0.179912 | 0.541288 |
| explainable_boosting_machine | 3407 | 0.665705 | 0.385790 | 0.179907 | 0.541266 |
| explainable_boosting_machine | 9999 | 0.665831 | 0.385979 | 0.179902 | 0.541248 |

### Aggregate across seeds

| Model | ROC-AUC Mean±SD | PR-AUC Mean±SD | Brier Mean±SD | Log Loss Mean±SD |
| --- | --- | --- | --- | --- |
| logistic_regression | 0.6621±0.0000 | 0.3788±0.0000 | 0.2295±0.0000 | 0.6506±0.0000 |
| random_forest | 0.6514±0.0013 | 0.3693±0.0010 | 0.2403±0.0003 | 0.6737±0.0007 |
| xgboost | 0.6696±0.0001 | 0.3885±0.0001 | 0.2246±0.0001 | 0.6390±0.0001 |
| explainable_boosting_machine | 0.6657±0.0001 | 0.3858±0.0001 | 0.1799±0.0000 | 0.5413±0.0000 |

### Range across seeds (min–max)

| Model | ROC-AUC min–max | PR-AUC min–max | Brier min–max | Log Loss min–max |
| --- | --- | --- | --- | --- |
| logistic_regression | 0.662147–0.662147 | 0.378807–0.378807 | 0.229471–0.229471 | 0.650576–0.650576 |
| random_forest | 0.649763–0.653065 | 0.368382–0.370677 | 0.239825–0.240759 | 0.672647–0.674560 |
| xgboost | 0.669412–0.669672 | 0.388393–0.388646 | 0.224535–0.224701 | 0.638885–0.639195 |
| explainable_boosting_machine | 0.665655–0.665831 | 0.385749–0.385979 | 0.179902–0.179912 | 0.541248–0.541288 |

Logistic regression is deterministic under L2/`liblinear` for this design, so seed statistics are identical. Random forest is the only family with material seed-to-seed movement, and it is still small.

Logistic regression used `class_weight='balanced'` and converged in 16 iterations (`n_iter=16 < max_iter=300`) on every validation seed. Random forest used `class_weight='balanced'`. XGBoost used `scale_pos_weight = n_neg/n_pos` on the fitting labels (train-only 4.3528; train+validation refit 4.0611). Early-stopping best-iteration counts were 300, 293, 300, 300, 300; the frozen final `n_estimators` is the median 300, with no early stopping on test. EBM 0.7.8 has no class-weight argument. EBM interactions were 0 before any test look, as an additive reference on the nine imputed native columns rather than the 1023-column one-hot matrix.

## D. Selected configurations

Primary validation criterion: mean PR-AUC across seeds [42, 123, 2024, 3407, 9999].
Selected family: `explainable_boosting_machine`.
Primary criterion is mean validation PR-AUC. Best PR-AUC is 0.388473. Candidates within 0.005: ['explainable_boosting_machine', 'xgboost']. Among those, lowest mean Brier then simplicity selected `explainable_boosting_machine` (PR-AUC=0.385841, Brier=0.179907).

All completed families were still retrained on TRAIN+VALIDATION and evaluated once on TEST after freeze, unless the run was blocked first. Test numbers were not used to choose the family.

## E. Final test results

| Model | ROC-AUC | 95% CI | PR-AUC | 95% CI | Brier | 95% CI | Log Loss | 95% CI |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| logistic_regression | 0.676356 | [0.673671, 0.679193] | 0.340648 | [0.336947, 0.344767] | 0.219984 | [0.219396, 0.220604] | 0.635413 | [0.633435, 0.637277] |
| random_forest | 0.660926 | [0.658341, 0.663658] | 0.332586 | [0.328355, 0.336528] | 0.235976 | [0.235802, 0.236150] | 0.664900 | [0.664549, 0.665250] |
| xgboost | 0.685440 | [0.682952, 0.688179] | 0.357670 | [0.353444, 0.362085] | 0.213638 | [0.213075, 0.214169] | 0.614946 | [0.613806, 0.616108] |
| explainable_boosting_machine | 0.679941 | [0.677252, 0.682832] | 0.353407 | [0.349280, 0.357713] | 0.156845 | [0.155867, 0.157954] | 0.484939 | [0.482565, 0.487668] |

Bootstrap: 1000 row resamples, percentile 95% CI, seed 42. Not used for tuning.

## F. Temporal robustness

| Model | Year | ROC-AUC | PR-AUC | Brier |
| --- | --- | --- | --- | --- |
| logistic_regression | 2017 | 0.674742 | 0.366168 | 0.222616 |
| logistic_regression | 2018 | 0.671688 | 0.263866 | 0.212828 |
| random_forest | 2017 | 0.658207 | 0.355739 | 0.237212 |
| random_forest | 2018 | 0.656729 | 0.254012 | 0.232616 |
| xgboost | 2017 | 0.682856 | 0.382325 | 0.216668 |
| xgboost | 2018 | 0.684533 | 0.279491 | 0.205399 |
| explainable_boosting_machine | 2017 | 0.677804 | 0.377247 | 0.168236 |
| explainable_boosting_machine | 2018 | 0.675593 | 0.276294 | 0.125866 |

These year slices are descriptive and were not used to modify models.

## G. Reproducibility

- experiment_id: `stage4b-lc-granting-v1`
- seeds: [42, 123, 2024, 3407, 9999]; final test seed: 42
- dataset_hash: `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc`
- split_manifest_hash: `d4db2099199258ae5ca4f5a85a7ce8e7dde2943a0bf7b9239212cce1e44d0e70`
- preprocessing_policy_hash: `3435a985086eccdfb548b6dff88c4fadaa6c060250237dcc759be3db64b44fd9`
- git_commit: `None`
- libraries: {"python": "3.12.10 (tags/v3.12.10:0cc8128, Apr  8 2025, 12:21:36) [MSC v.1943 64 bit (AMD64)]", "pandas": "3.0.5", "numpy": "2.5.2", "sklearn": "1.9.0", "xgboost": "3.4.1", "interpret": "0.7.8", "matplotlib": "3.11.1", "joblib": "1.6.0"}

## H. Tests

...............................................                          [100%]
47 passed in 40.92s

## I. Unexpected issues

- sklearn 1.9 emits a `FutureWarning` that `penalty=` is deprecated in 1.8 and scheduled for removal in 1.10. The executed estimator still used L2 with `solver='liblinear'` and `C=1.0`; this is recorded, not hidden.
- XGBoost early stopping rarely fired: four of five validation seeds used all 300 rounds (one seed stopped at 293). The frozen test model therefore uses 300 trees.
- Random forest was weaker than L2 logistic regression on every validation metric. That result is retained.
- EBM's Brier/log-loss advantage is expected in part because it is not class-weighted, while LR/RF/XGB are. Selection used the pre-declared PR-AUC window plus Brier rule, not a post-hoc preference for EBM.
- Test PR-AUC is lower than validation PR-AUC for every family, and 2018 PR-AUC is substantially lower than 2017. Prevalence also differs by split (train 18.7%, validation 24.9%, test 21.2%; 2018 is lower still). These are descriptive temporal findings, not a reason to retune.
- `git_commit` is null because this workspace is not a git repository.
- No calibration, SHAP, decision threshold, or Shariah layer was applied.

## J. Stage gate

`STAGE_4B_STATUS = PASS`

All four families completed validation (5 seeds) and one frozen test evaluation; integrity tests passed.

Stage 5 was not started.

