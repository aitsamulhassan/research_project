# AMENDMENT-STAGE10-AUTHORIZATION

Prospective Stage 10 authorization. This file exists **before** any Stage 10 runner is written or executed.

| Item | Value |
| --- | --- |
| **Amendment ID** | `AMENDMENT-STAGE10-AUTHORIZATION` |
| **Constitution basis** | Rule #14: Document every methodology change. This amendment authorizes **execution scope** for the Stage 10 activities already defined in `docs/STAGE_10_EXPERIMENTAL_PROTOCOL.md`. It does not change Stage 7/8/9 science. |
| **Document date** | 2026-09-15 |
| **Approval date** | 2026-09-15 |
| **Status** | `APPROVED` |
| **Approver** | Research Owner (approval recorded via chat instruction) |
| **Expert sign-off** | None. This amendment is not expert Shariah validation. |
| **Does not authorize** | Stage 10 implementation or execution while this file remains `DRAFT`; Stage 11; paper drafting; any activity not listed in §3 |
| **Controlling protocol** | `docs/STAGE_10_EXPERIMENTAL_PROTOCOL.md` (`STAGE-10-PROTOCOL-2026-09-15`) |
| **Related records** | Stage 9 closure: `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md`. Process record: `docs/deviations/DEVIATION-001-stage9-authorization-gap.md` (not an authorization of 9.2/9.3/XGBoost) |

**STATUS: `APPROVED`**

This authorization is **prospective**. It does **not** take effect for implementation or execution until the research owner changes the status in this file (or a successor dated amendment) from `DRAFT — PENDING RESEARCH-OWNER APPROVAL` to an explicit approved status **and** records an approval date and research-owner approval in §9.

A Cursor command, a chat instruction to “run Stage 10,” or a runner writing files is **not** approval.

No Stage 10 source, runner, config, test, metric, figure, or result file is created by recording this draft.

---

## 1. Purpose

This amendment, **once approved**, authorizes the already-completed Stage 10 **design** to be **implemented and executed** exactly as specified in `docs/STAGE_10_EXPERIMENTAL_PROTOCOL.md`.

Stage 10 is a **controlled documentation / robustness-analysis** phase using **already-frozen** evidence. It does **not** repair Stage 9 documentation, does **not** reopen Stage 9, and introduces **no new confirmatory TEST-set experiment**.

This amendment does **not** convert exploratory Stage 9 work into confirmatory evidence.

---

## 2. Scope

| Bound | Statement |
| --- | --- |
| Stage 9 | **CLOSED** for experimentation. Stage 10 does **not** reopen Stage 9. No further Stage 9 experiments. |
| Stage 10 design | `STAGE_10_DESIGN_STATUS = COMPLETE` (already recorded in the protocol) |
| Stage 10 execution | `STAGE_10_EXECUTION = NOT AUTHORIZED` until this amendment is explicitly owner-approved |
| Science freeze | Stage 8 thresholds `t_low=0.06`, `t_high=0.69`, `t*=0.16`; frozen EBM + Platt; A0/A1/A3/A4 definitions **not redefined** |
| Provenance | Existing freeze-backed results from Stages 4B, 5, 8, 9.1, and the **approved-scope** portion of 9.4 (Logistic Regression + EBM) retain their **original provenance** |
| Stage 9.4 XGBoost | Remains **exploratory**. This amendment does **not** ratify it, retroactively or prospectively |
| Stage 11 / paper | **Not** authorized |

---

## 3. Authorized activities

When, and only when, this amendment is owner-approved, **only** the following Stage 10 activities from the protocol are authorized.

Cite-only inventory rows in the protocol (`S10-CITE-*`) remain **citation of existing artifacts**, not new experiments. They may appear in a later Stage 10 report **without regeneration**. They are not a license to rerun Stages 4B–9.4.

### 3.1 S10-I1-IDENTITY

| Field | Binding |
| --- | --- |
| Classification | `INTEGRITY / PROVENANCE CHECK — NOT A SCIENTIFIC CONFIRMATORY EXPERIMENT` |
| What is authorized | Verify that A0/A1/A3 use the same frozen `p_selected`; compare re-applied A0/A3 maps to stored Stage 8 v2 table3; check freeze-file SHA-256 against recorded hashes |
| What it is not | Not a scientific confirmatory experiment. Passing does **not** generate independent scientific evidence |

### 3.2 S10-R1-YEAR

| Field | Binding |
| --- | --- |
| Classification | `EXPLORATORY / DESCRIPTIVE POST-HOC REANALYSIS` |
| What is authorized | Year-wise (stored `year ∈ {2017, 2018}`) approve/review/reject mix under **frozen** A0/A1/A3 maps on already-unblinded LendingClub TEST `p_selected` |
| What it must remain | Explicitly **non-confirmatory**. No post-hoc LendingClub TEST analysis may be called confirmatory |
| Forbidden inside this activity | Model selection; threshold selection; calibration selection; year-tuned policy; inventing calendar fields |

### 3.3 S10-A1-GAP

| Field | Binding |
| --- | --- |
| Classification | `ANALYSIS-ONLY / DESCRIPTIVE` |
| What is authorized | Algebraic decomposition of the already-observed A1/G0 review allocation using existing Stage 8/9 artifacts (band counts, G0 matrix, L1/L2 statuses) |
| Forbidden inside this activity | New Shariah rule; fabricated contractual evidence; Shariah score/probability; G-unsafe; treating G1/G3 as empirical Shariah findings; independent validation of the Shariah governance layer |

### 3.4 S10-A4-SIDEBYSIDE

| Field | Binding |
| --- | --- |
| Classification | `ANALYSIS-ONLY / DESCRIPTIVE COMPARISON` |
| What is authorized | Side-by-side citation of **already-existing** LendingClub EBM/Platt TEST metrics and UCI **Logistic Regression + EBM** TEST metrics |
| Forbidden inside this activity | New AUC (or other) statistical equality test; reopening UCI TEST for selection; merging LC and UCI rows; transferring LC thresholds/calibrators/policy; labeling UCI as Shariah validation; elevating XGBoost |

---

## 4. Prohibited activities

This amendment does **not** authorize:

- Stage 10 implementation or execution while status remains `DRAFT — PENDING RESEARCH-OWNER APPROVAL`
- any **new confirmatory TEST-set experiment**
- reopening Stage 9, or any new Stage 9.1–9.4 experiment
- rewriting `audit/stage9_0_experimental_freeze.json` or Stage 7/8/9 result artifacts
- a **new model family** (no RF-on-UCI, no additional LC families, no XGBoost ratification)
- **threshold search** (including TEST remaps of alternative `r` grids; Experiment G rerun; R-SEED-POLICY threshold re-search)
- **calibration selection on TEST** (LC or UCI); refitting Platt/isotonic; applying LC Platt `(a,b)` to UCI
- retraining or rescoring models except reading already-stored `p_selected` for S10-I1 / S10-R1 as specified
- a **new Shariah rule**, AAOIFI clause invention, `SHR-001` reconstruction, or fabricated **expert validation**
- fabrication of **contract-level evidence**; a Shariah score or probability; modifying credit probability with a Shariah score
- G-unsafe; A3-F (still unspecified)
- LC → UCI transfer of thresholds, calibrators, Shariah rules, or decision policy
- Stage 11
- **paper drafting**
- any runner editing this amendment, the Stage 10 protocol execution gate, or `RESEARCH_CONSTITUTION.md`

---

## 5. TEST-data protection

| Rule | Binding |
| --- | --- |
| LC TEST | Already unblinded in Stages 4B–8. Stage 10 may **reanalyze** stored outputs only as specified (S10-I1, S10-R1). **Never** for model, threshold, or calibration **selection**. **Never** confirmatory by virtue of a new TEST cut |
| UCI TEST | **Not** reopened for family or calibrator selection. S10-A4 cites already-reported metrics only |
| Methodology choice | TEST results are not inspected to choose methodology |
| Confirmatory claims | May cite **freeze-backed prior-stage** evidence only (4B, 5, 8, 9.1 with class-B disclosure, 9.4 LR+EBM). Stage 10 native activities are **not** confirmatory TEST experiments |

```text
STAGE_10_EXECUTION = NOT AUTHORIZED
```

until the research owner explicitly approves this amendment (§9).

---

## 6. Artifact expectations (after approval only)

If, and only if, this amendment is approved, later execution **may** create artifacts named in the Stage 10 protocol (for example `configs/stage10/`, `experiments/stage10/`, `results/stage10/v1/`, `audit/stage10_*.json`, `docs/STAGE_10_ROBUSTNESS_REPORT.md`, `tests/test_stage10_*.py`).

This draft creates **none** of those files.

Runners **must not** edit authorization text, protocol execution-gate status, this amendment’s status, or the constitution.

---

## 7. Provenance rules

- Existing frozen evidence retains its **original** provenance. Stage 10 does not re-label Stage 4B/5/8/9.1/9.4 LR+EBM as “Stage 10 confirmatory experiments.”
- Stage 9.1 remains authorization class **B** (documentation gap; no retroactive rewrite).
- Stage 9.2 remains class **C** exploratory/sensitivity.
- Stage 9.3 G1/G3 remain class **C** hypothetical engineering, not empirical Shariah findings.
- Stage 9.4 XGBoost remains class **C** / execution-time expansion / **exploratory**. **Not ratified** here.
- S10-I1, S10-R1, S10-A1, S10-A4 keep the classifications in §3. Favorable numbers do **not** convert them to confirmatory TEST experiments.
- Do not silently remove inconvenient results (Constitution Rule #15).

---

## 8. Standing execution-gate rule

**No stage runner may edit its own execution-gate or authorization text.**

Execution-gate changes may occur only through a dedicated, dated amendment file created and reviewed **BEFORE** the corresponding runner is executed.

While this amendment remains `DRAFT — PENDING RESEARCH-OWNER APPROVAL`:

```text
STAGE_10_EXECUTION = NOT AUTHORIZED
```

**No Stage 10 runner may be created or executed.** S10-I1, S10-R1, S10-A1-GAP, and S10-A4-SIDEBYSIDE must **not** be run.

---

## 9. Approval

| Field | Value |
| --- | --- |
| **Status** | `APPROVED` |
| **Approval date** | 2026-09-15 |
| **Research owner approval** | Research Owner (approval recorded via chat instruction) |

Required order **after** explicit approval (not an execution, not performed by this file):

1. Research owner sets **Status** to an explicit approved value (not inferred) and fills **Approval date** and **Research owner approval**.
2. Only then may Stage 10 implementation of §3 begin.
3. `STAGE_10_EXECUTION` may change from `NOT AUTHORIZED` only by that recorded approval plus protocol/constitution document-control consistent with the approved amendment.
4. Stage 11 and paper drafting remain unauthorized.

---

## 10. Document control

| Field | Value |
| --- | --- |
| Amendment ID | `AMENDMENT-STAGE10-AUTHORIZATION` |
| Protocol | `docs/STAGE_10_EXPERIMENTAL_PROTOCOL.md` |
| Protocol ID | `STAGE-10-PROTOCOL-2026-09-15` |
| Stage 9 closure | `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md` (authoritative; not rewritten) |
| Constitution | **Not modified** by this draft |
| Stage 10 protocol execution status | **Not modified** by this draft; remains `STAGE_10_EXECUTION = NOT AUTHORIZED` |
| Paper | Not authorized |
| Stage 11 | Not authorized |
