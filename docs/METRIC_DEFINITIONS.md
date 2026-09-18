# Metric Definitions

Stage 4B uses the following definitions. All metrics are computed from binary labels `y ∈ {0,1}` and predicted probabilities `p ∈ [0,1]` for the positive class `Default = 1` (Charged Off). No decision threshold is applied in this stage. Accuracy is not a primary metric.

## ROC-AUC

Implementation: `sklearn.metrics.roc_auc_score(y, p)`.

This is the area under the receiver-operating-characteristic curve of true-positive rate versus false-positive rate as the threshold on `p` varies. It equals the probability that a randomly chosen positive receives a higher score than a randomly chosen negative.

## PR-AUC

Implementation: `sklearn.metrics.average_precision_score(y, p)`.

This is the area under the precision-recall curve, summarized as average precision. It is the pre-declared primary validation selection statistic because the positive class is materially imbalanced.

## Brier score

Implementation: `sklearn.metrics.brier_score_loss(y, p)`.

`Brier = mean((p − y)^2)`. Lower is better. It is a strictly proper scoring rule for probabilistic quality.

## Log loss

Implementation: `sklearn.metrics.log_loss(y, p, labels=[0,1])` with probabilities clipped to `[1e-15, 1−1e-15]`.

`LogLoss = −mean( y log p + (1−y) log(1−p) )`. Lower is better. It is a strictly proper scoring rule.

## Bootstrap confidence intervals (test only)

After each family is frozen and evaluated once on test, 95% percentile bootstrap intervals are computed by resampling test rows with replacement `n_bootstrap = 1000` times using `numpy.random.RandomState(42)`. The interval uses the 2.5th and 97.5th percentiles of the bootstrap metric distribution. Resamples that contain only one class are skipped. Bootstrap results are not used to select or modify models.

## What these metrics are not

They are not calibrated-probability claims (Stage 5), not explanation claims (Stage 6), and not Shariah or decision-policy claims.
