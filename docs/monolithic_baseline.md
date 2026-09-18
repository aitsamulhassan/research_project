# Monolithic baseline (Stage 8)

The research comparison is **architectural**, not a new neural network.

## Baseline definition

```text
frozen Platt-calibrated EBM probability
        → single threshold t* selected on VALIDATION
        → APPROVE if p < t*
        → REJECT  if p >= t*
```

Properties:

- No Shariah-oriented governance layer
- No review band
- No audit fusion of independent evidence
- Explainability is not consulted
- `C_REVIEW = 0` during baseline threshold selection
- The probability file is the **same** Stage 5 artifact used by the proposed system

`t*` minimizes expected normalized cost ` (C_FN * FN + C_FP * FP) / n ` on validation under the same assumed FN:FP ratio as the primary scenario.

## Proposed system

```text
same frozen probability
        → cost-sensitive credit bands (validation only)
        + Stage 7 governance status (not a score)
        + Stage 6 attribution attached as evidence
        → matrix policy → APPROVE / HUMAN_REVIEW / REJECT
        → audit record
```

## What may be compared

- Action mix (approval / review / rejection rates)
- Whether governance insufficiency blocks automatic approval
- Whether an audit record exists
- Expected cost **under the stated cost convention** (fused cost includes `C_REVIEW`; baseline does not)

## What must not be claimed unless shown

- Better ROC-AUC, PR-AUC, or Brier (the scores are the same file)
- That review improves outcomes (no reviewer labels exist)
- That the fused system is Shariah-certified
- That a lower approval rate is morally or religiously superior

If LendingClub contractual evidence is insufficient, the fused system is expected to approve few or no real applications. That is an empirical architecture result, not a reason to weaken Stage 7 rules.
