# Decision-cost assumptions (Stage 8)

All costs in Stage 8 are **ASSUMED RELATIVE COST SCENARIOS**. They are researcher sensitivity settings, not measured operational costs of LendingClub, a bank, an Islamic financial institution, or a regulator.

No dollar amounts are used.

## Unit

`C_FP = 1` is the unit cost of **automatically rejecting a non-default** (false positive in the underwriting convention).

`C_FN = r * C_FP` is the relative cost of **automatically approving a default**, with

```text
r in {1, 2, 5, 10}
```

labeled `FN:FP = r:1`.

## Review cost

A review band that is free would send every application to review. That is not a decision policy.

Stage 8 therefore assumes

```text
C_REVIEW = 0.25 * C_FP
```

unless Experiment G replaces `0.25` with `{0.10, 0.25, 0.50}`.

This is still an assumption. It is not a staffing model.

## Expected cost

On a labeled split used **only for evaluation or for validation-only selection**:

```text
Cost_total = C_FN * FN + C_FP * FP + C_REVIEW * n_review
Cost_normalized = Cost_total / n
```

where

- `FN` = auto-approved defaults
- `FP` = auto-rejected non-defaults
- `n_review` = applications in `HUMAN_REVIEW`

Reviewed cases are excluded from the automatic confusion counts `TP/TN/FP/FN`. Population FNR is `FN / n_defaults`. Auto FNR is `FN / (FN + rejected defaults)` and is undefined if no default is auto-decided.

## Primary freeze

The configuration declares `primary_fn_fp_ratio: 5` **before** test evaluation. Other ratios remain sensitivity analyses.

## What is not claimed

These ratios do not represent:

- expected loss given default
- recovery rates
- cost of capital
- Shariah-review honoraria
- regulatory penalties

They exist so that threshold selection is explicit rather than an unexplained `0.30 / 0.70` cut.
