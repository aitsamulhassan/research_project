# AMENDMENT-STAGE9-4-AUTHORIZATION

Prospective Stage 9.4 authorization. This file exists **before** any Stage 9.4 runner is written or executed.

| Item | Value |
| --- | --- |
| **Amendment ID** | `AMENDMENT-STAGE9-4-AUTHORIZATION` |
| **Constitution basis** | Rule #14: Document every methodology change. This amendment authorizes **execution scope** for Stage 9.4 only. It does not change Stage 7/8 science. |
| **Document date** | 2026-09-15 |
| **Approval date** | 2026-09-15 |
| **Status** | `APPROVED` |
| **Approver** | Research owner (recorded via chat instruction; no other identity-recording mechanism exists in this repository) |
| **Expert sign-off** | None. This amendment is not expert Shariah validation. |
| **Does not authorize** | Stages 9.5–9.7; Stage 9.4 runner creation or execution while this file remains `DRAFT`; retroactive authorization of Stage 9.2 or Stage 9.3 |
| **Related process record** | `docs/deviations/DEVIATION-001-stage9-authorization-gap.md` (not an authorization of 9.2/9.3) |

**STATUS: APPROVED**

This authorization is **prospective**. It exists **before** Stage 9.4 code execution. It does **not** take effect for implementation or execution until the research owner changes the status in this file (or a successor dated amendment) from `DRAFT — PENDING RESEARCH-OWNER APPROVAL` to an explicit approved status. A Cursor command, a chat instruction to “run UCI,” or a runner writing files is **not** approval.

No Stage 9.4 source, runner, or UCI modeling output is created by recording this draft.

---

## 1. What this amendment does and does not do

This amendment, **once approved**, authorizes:

**STAGE 9.4 — UCI INDEPENDENT GENERALIZATION**

as specified in `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` §7 (UCI role) and freeze decisions U1, U2, U3.

It does **not**:

- rewrite `audit/stage9_0_experimental_freeze.json`;
- authorize Stage 9.2 or Stage 9.3 retroactively (see `DEVIATION-001`);
- expand UCI work beyond the frozen protocol scope;
- authorize LendingClub threshold transfer, UCI+LC merging, L2 fusion on UCI, or Shariah-rule training;
- authorize Stages 9.5–9.7;
- permit any Stage 9.4 runner to edit authorization text.

---

## 2. Numbering note (protocol §12 vs this amendment)

Protocol §12 preferred order listed “Stage 9.4 Credit robustness (cite Stage 4B/5/6 seeds)” and “Stage 9.5 UCI generalization.” This amendment does **not** rewrite §12 scientific content.

This amendment prospectively names **UCI independent generalization** as **Stage 9.4**, matching the owner documentation task that created this file. Frozen U1/U2/U3 **science** is unchanged. The LC seed/year citation item listed as “9.4 credit robustness” in §12 is **not** authorized here and remains unauthorized unless a separate dated amendment is approved.

---

## 3. Authorized Stage 9.4 scope (frozen protocol, not expanded)

When, and only when, this amendment is owner-approved:

| Constraint | Requirement |
| --- | --- |
| Dataset | UCI Default of Credit Card Clients (SHA-256 `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602` as recorded in the Stage 9 protocol) |
| Role | Independent credit-risk generalization / replication. Not Islamic-finance data. |
| Split | Frozen UCI stratified 0.70/0.15/0.15, seed 42 (train 20,999; validation 4,499; test 4,502). Do not change the split. |
| Merge | `merged_with_lendingclub: false`. No row linkage. |
| Thresholds | No transfer of LendingClub `t_low=0.06`, `t_high=0.69`, or `t*=0.16`. No UCI decision-threshold search is authorized by this amendment (protocol: any later UCI threshold needs its own pre-specified validation-only procedure; not authorized in 9.0; not authorized here). |
| Models | Frozen U1: EBM (`interactions=0`) and L2 logistic regression only. UCI-specific, train-only hyperparameters. No LC weight transfer. Not a four-family competition. |
| Calibration | Fit on **UCI validation only**. Do not reuse LendingClub Platt `a,b`. Selection uses the Stage 5 rule. UCI TEST is not used to select the calibrator. |
| Shariah | No Shariah-rule training. No L2 fusion. U3: dataset-metadata L1 only, not 4,502 applicant rulings. |
| Temporal structure | `NO_CALENDAR_TIMESTAMPS`. Do not invent a calendar validation. |
| UCI TEST | Remains **protected** until an approved Stage 9.4 execution protocol is followed. **No** UCI TEST for model, calibrator, or threshold selection. One TEST evaluation only after freeze of the UCI methodology objects for that run, seed 42. |
| Reproducibility | Versioned config, audit JSON, hashes, and reports. Do not overwrite Stages 4–8 or Stage 9.1–9.3 artifacts. |

UCI TEST must not be used to choose the UCI family, calibrator, or any LendingClub methodology.

---

## 4. Standing execution-gate rule

**No stage runner may edit its own execution-gate or authorization text going forward.**

Execution-gate changes may occur only through a dedicated, dated amendment file created and reviewed **BEFORE** the corresponding stage's runner is executed.

The Stage 9.4 runner, when eventually created, **MUST NOT** be permitted to modify:

- execution authorization,
- protocol authorization text,
- amendment status,
- Constitution authorization records.

Authorization must always be external to the runner.

While this amendment remains `DRAFT — PENDING RESEARCH-OWNER APPROVAL`, **no Stage 9.4 runner may be created or executed**.

---

## 5. Required order after approval (not an execution)

1. Research owner sets this file’s **Status** to an explicit approved value (not inferred).
2. Only then may Stage 9.4 implementation begin.
3. UCI methodology objects for the run must be frozen before UCI TEST is opened.
4. Stages 9.5–9.7 remain unauthorized.

---

## 6. Paper claim bound

Until UCI TEST is evaluated under an **approved** Stage 9.4 execution, no paper claim of UCI generalization may be written as if it were executed. Constitution Rule #8 remains: never report an experiment that was not executed.
