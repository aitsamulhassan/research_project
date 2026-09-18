# Stage 10 final closure audit

| Item | Value |
| --- | --- |
| **Audit ID** | `STAGE-10-FINAL-CLOSURE-AUDIT` |
| **Audit date** | 2026-09-16 |
| **Audit type** | Documentation / artifact inspection only |
| **Experiments rerun** | **No** |
| **Stage 10 activities rerun** | **No** |
| **Models retrained or loaded for scoring** | **No** |
| **Metrics recomputed** | **No** |
| **Calibration refit** | **No** |
| **Thresholds searched or changed** | **No** |
| **Stage 9 reopened** | **No** |
| **UCI TEST reopened for selection** | **No** |
| **Stage 11 started** | **No** |
| **Paper drafted** | **No** |
| **New amendment created** | **No** |
| **Git / `.git` available** | **No.** Repository-level diff verification is unavailable and is **not** fabricated. |

This audit inspects existing Stage 10 authorization, protocol, activity audits, reports, metrics manifests, and stored test records. It does **not** rerun S10-I1, S10-R1, S10-A1, or S10-A4. It does **not** rewrite historical authorization records.

**Final classification: B. PASS WITH DOCUMENTATION/REPRODUCIBILITY LIMITATION**

**Closure:** Stage 10 is closed for experimentation. The four authorized activities are complete. No further Stage 10 experiment should be started without a new prospective amendment. That amendment is **not** created by this audit. Stage 11 and paper drafting remain unauthorized.

---

## 1. Executive closure classification

**B. PASS WITH DOCUMENTATION/REPRODUCIBILITY LIMITATION**

All four activities authorized by `AMENDMENT-STAGE10-AUTHORIZATION` (`APPROVED` 2026-09-15) have stored completion records. Each remains in its declared non-confirmatory class. Recorded flags show no model training, no calibration refit, no threshold search, no Stage 9 reopen, and no UCI TEST selection. Remaining issues are already-documented provenance/reproducibility limitations. They are **not** treated as new scientific failures.

Not A: `git_commit` is null on every Stage 10 manifest; Stage 8 v2 audit identity is positional; Stage 4B final EBM joblib SHA-256 is unrecorded; stored pytest summaries do not independently lock every historical TEST point estimate; Stage 9 authorization classes B/C remain as previously closed.

Not C: no prohibited experiment is recorded; no frozen Stage 8/9 result rewrite is recorded; the Stage 4B vs Stage 5 EBM TEST ROC-AUC difference is already classified **EXPLAINED**.

---

## 2. Authorization provenance

| Item | Recorded finding |
| --- | --- |
| Amendment | `docs/amendments/AMENDMENT-STAGE10-AUTHORIZATION.md` |
| Status | `APPROVED` |
| Approval date | 2026-09-15 |
| Protocol | `docs/STAGE_10_EXPERIMENTAL_PROTOCOL.md` (`STAGE-10-PROTOCOL-2026-09-15`) |
| Design status in protocol | `STAGE_10_DESIGN_STATUS = COMPLETE` |
| Execution gate in protocol | `STAGE_10_EXECUTION = AUTHORIZED FOR S10-I1-IDENTITY, S10-R1-YEAR, S10-A1-GAP, AND S10-A4-SIDEBYSIDE ONLY` |
| Authorized activities | Exactly those four |
| Cite-only inventory (`S10-CITE-*`) | Citation of existing artifacts; **not** additional experiments; no `S10-CITE-*` runner exists |
| Stage 11 | **Not authorized** (amendment §4 / §9; protocol) |
| Paper drafting | **Not authorized** |
| Stage 9 | **CLOSED**; Stage 10 must not reopen it |
| Stage 9.4 XGBoost | Remains exploratory; amendment does **not** ratify it retroactively or prospectively |

No fifth Stage 10 experiment ID is present under `experiments/` or `audit/stage10_*.json`. Existing Stage 10 runners are only:

- `experiments/stage10_i1_identity/run_s10_i1.py`
- `experiments/stage10_r1_year/run_s10_r1.py`
- `experiments/stage10_a1_gap/run_s10_a1.py`
- `experiments/stage10_a4_sidebyside/run_s10_a4.py`

No `stage11` path and no paper draft file were found.

---

## 3. Four Stage 10 activity status table

Sources: the four `audit/stage10_*.json` manifests and their reports. Values below are **recorded**, not regenerated.

| Field | S10-I1-IDENTITY | S10-R1-YEAR | S10-A1-GAP | S10-A4-SIDEBYSIDE |
| --- | --- | --- | --- | --- |
| Experiment ID / version | `s10_i1_identity_v1` | `s10_r1_year_v1` | `s10_a1_gap_v1` | `s10_a4_sidebyside_v1` |
| Execution status | `PASS WITH DOCUMENTATION LIMITATION` | `COMPLETED — exploratory/descriptive post-hoc reanalysis` | `COMPLETED — analysis-only descriptive decomposition` | `PASS WITH DOCUMENTATION LIMITATION` |
| Classification | `INTEGRITY / PROVENANCE CHECK — NOT A SCIENTIFIC CONFIRMATORY EXPERIMENT` | `EXPLORATORY / DESCRIPTIVE POST-HOC REANALYSIS — NON-CONFIRMATORY` | `ANALYSIS-ONLY / DESCRIPTIVE` | `ANALYSIS-ONLY / DESCRIPTIVE COMPARISON` |
| Confirmatory experiment | false | false | false | false |
| Started (recorded UTC) | 2026-09-15T20:32:14+00:00 | 2026-09-15T20:40:42+00:00 | 2026-09-16T13:18:55+00:00 | 2026-09-16T15:03:18+00:00 |
| Model trained | false | false | false | false |
| Model loaded for scoring | false | false | not a dedicated audit field; `models_trained=false` | false |
| Calibration refit | false | false | false | false |
| Thresholds searched/changed | false (`thresholds_reselected=false`) | false (`year_specific_threshold=false`) | false | false |
| TEST used for selection | No. Identity check on stored `p_selected`; not model/calibrator/threshold selection | No. Post-hoc grouping of already-unblinded stored `year` / frozen maps; not selection | No. Algebraic citation of stored Stage 8/9 counts | No. `uci_test_used_for_selection=false`; metrics cited, not recomputed |
| Historical Stage 8/9 artifacts modified | `stage8_9_results_modified=false`; `protected_files_unchanged=true` | `stage8_9_results_modified=false`; `protected_files_unchanged=true` | `protected_files_unchanged=true`; S10-I1/R1 not modified | `protected_files_unchanged=true`; `stage9_reopened=false` |
| Recorded pytest | exit 0; `6 passed in 1.66s` (`tests/test_stage10_i1_identity.py`) | exit 0; `5 passed in 0.92s` (`tests/test_stage10_r1_year.py`) | exit 0; `5 passed in 2.55s` (`tests/test_stage10_a1_gap.py`) | exit 0; `8 passed in 0.54s` (`tests/test_stage10_a4_sidebyside.py`) |
| Issues | None | None | None | None |
| Documented limitations (recorded) | Stage 8 v2 audit has no `row_ref` (positional `p_selected` check); `git_commit` null | HIGH band n=27; post-hoc non-confirmatory; `git_commit` null | No `row_ref` on Stage 8 v2 audit; LC has no contract-level Shariah fields; does not independently validate governance; identical evidence object across TEST; `git_commit` null | Unrecorded Stage 4B final-EBM hash; TRAIN+VAL total not stored as one field; missing ECE in some cited tables; LC≠UCI targets; `git_commit` null |

Each activity’s own report states it executed **only** that activity at the time it was written. Later authorized activities exist as separate records. That sequencing is expected and is **not** a contradiction.

Recorded freeze / TEST hashes on S10-I1, S10-R1, S10-A1, and S10-A4 (where present) match the Stage 9.1 / Stage 9.4 protected values:

| Artifact | Recorded SHA-256 |
| --- | --- |
| Stage 8 v1 freeze | `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4` |
| Stage 8 v2 freeze | `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b` |
| table3 | `90759eb72f1173b40b5b9363c21b0ef3d6f1cde5042748eb57871d49fb73d5ee` |
| LC TEST calibrated CSV | `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb` |

This audit did **not** re-hash those files.

---

## 4. Stage 9 closure verification

Authoritative prior record: `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md` (not rewritten here). Stage 10 amendment §2: Stage 9 is **CLOSED**.

| Statement | Finding from existing records |
| --- | --- |
| Stage 9 remains CLOSED | **Yes.** Freeze JSON `stage9_execution` remains `"NOT AUTHORIZED"`. No new `audit/stage9_*` run after Stage 9 closure is part of Stage 10. Stage 10 A4 records `stage9_reopened=false`. |
| No Stage 9 experiment reopened during Stage 10 | **Yes.** Stage 10 runners are S10-I1/R1/A1/A4 only. Stage 9.1–9.4 result files are on each Stage 10 forbidden-write list; each Stage 10 audit records `protected_files_unchanged=true`. |
| UCI TEST not reopened for model selection | **Yes.** S10-I1/R1/A1: `uci_opened=false`. S10-A4: `uci_reopened=false`, `uci_test_used_for_selection=false`. Protocol: S10-A4 is citation-only. |
| Stage 9.4 XGBoost | **EXECUTION-TIME EXPANSION, EXPLORATORY** (`DEVIATION-001`; Stage 9 closure §2 and §9; Stage 10 amendment §2). |
| XGBoost ratified as pre-registered/confirmatory | **No.** S10-A4: `xgboost_ratified=false`; XGBoost not in the primary table. |
| Retroactive/prospective ratification sought | **No.** Amendment: “This amendment does **not** ratify it, retroactively or prospectively.” |
| Stage 9.1 | Remains **class B** (authorized with documentation gap). No retroactive rewrite. |
| Stage 9.2 | Remains **class C** exploratory / sensitivity. |
| Stage 9.3 | Remains **class C** exploratory / sensitivity. G1/G3 remain hypothetical; S10-A1 `g1_g3_treated_as_observed=false`. |
| Stage 9.4 XGBoost | Remains **class C / exploratory**. |

Stage 10 does **not** convert Stage 9 class B/C items into confirmatory evidence.

---

## 5. TEST-protection verification

LendingClub TEST (n = 208,886; already unblinded in Stages 4B–8):

| Check | Finding |
| --- | --- |
| New LC TEST model selection in Stage 10 | **Not found.** All four audits: `models_trained=false` |
| New LC TEST threshold selection | **Not found.** Recorded `t_low=0.06`, `t_high=0.69`, `t*=0.16`; all `thresholds_searched=false` |
| Calibration refit on LC TEST | **Not found.** All four: `calibration_refit=false`. Live freeze JSON still stores Platt `a=1.1988263209549705`, `b=0.6697765046966161`, `fit_split=validation` |
| TEST membership modified | **Not found.** S10-A4 records Stage 3 `test_hash` `4dfedb1ad7785fa3833047135b1883676f3e1b49aca9c87fcdb346e64fd489c6`, n=208886, `membership_recomputed=false` |
| S10-I1 TEST use | Integrity remap of **stored** `p_selected` vs table3; not selection |
| S10-R1 TEST use | Descriptive year mix of **stored** outputs; protocol class: exploratory / post-hoc / non-confirmatory |

UCI TEST (n = 4,502):

| Check | Finding |
| --- | --- |
| Reopened for family or calibrator selection | **No** (S10-A4 recorded flags; protocol forbids it) |
| LC thresholds/calibrators transferred | S10-A4: `lc_thresholds_transferred_to_uci=false`, `lc_calibration_transferred_to_uci=false` |

---

## 6. Model / calibration / threshold immutability verification

Live freeze files (inspected, not rewritten):

| File | Recorded science still present |
| --- | --- |
| `results/decision/frozen_policy.json` | `t_low=0.06`, `t_high=0.69`, Platt a/b as frozen, `selection_split=validation` |
| `results/decision/v2/frozen_policy.json` | same thresholds; `monolithic_t=0.16`; `thresholds_reselected=false` |

Stage 10 A4 records Stage 8 onward probability/model identity as:

- `results/calibration/test/ebm_seed42_calibrated.csv` (`p_selected`)
- `results/calibration/artifacts/ebm_train_only_seed42.joblib` (recorded SHA-256 `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4`)

That is the Stage 5 TRAIN-only EBM, not the Stage 4B TRAIN+VALIDATION TEST EBM.

No Stage 10 audit records a write to Stage 4B/5/8/9 metric, model, calibration, or policy artifacts.

---

## 7. Stage 4B vs Stage 5 ROC-AUC discrepancy resolution

Already completed diagnostic, cited by S10-A4 (`ebm_test_roc_discrepancy`). **Not recomputed here.**

| Item | Recorded value |
| --- | --- |
| Stage 4B EBM TEST ROC-AUC | 0.6799408767429772 |
| Stage 5 raw EBM TEST ROC-AUC | 0.6776693941139847 |
| Classification | **EXPLAINED** |
| Cause | Stage 4B uses a TRAIN+VALIDATION refit; Stage 5 uses a separately fitted TRAIN-only EBM |
| TEST split | Same frozen Stage 3 TEST (n=208886); S10-A4 `same_frozen_test_split=true` |
| ROC-AUC implementation | Same recorded wrapper (`evaluation.metrics.roc_auc` used by Stage 4B and Stage 5; sklearn `roc_auc_score`) |
| Stage 8 onward | Stage 5 TRAIN-only EBM / stored calibrated `p_selected`, **not** the Stage 4B TEST EBM |
| Investigation reopened in S10-A4 | false |
| Correction required | false |

This is **not** an unresolved discrepancy. It is **not** a protocol/scientific violation on the existing record.

---

## 8. Consolidated documentation / reproducibility limitations

These are **already-known**. They are not converted into new failures.

1. **No `.git` / `git_commit` null** on Stage 9 freeze and all four Stage 10 manifests. Protocol: record null; do not fabricate; not by itself a scientific abort.
2. **Stage 4B final EBM joblib SHA-256 not recorded.** Dump path is documented; hash was not computed in S10-A4.
3. **Stage 4B TRAIN+VALIDATION total not stored as one field.** TRAIN=941267 and VALIDATION=197528 are stored separately.
4. **Stage 8 v2 audit rows have no `row_ref`.** S10-I1 `p_selected` vs audit `calibrated_probability` identity is positional. S10-A1 band × L2 identity uses stored Stage 8 columns, not a keyed join.
5. **Stored pytest summaries do not independently lock every historical TEST point estimate.** Stage 10 tests check identity, citation, and prohibition flags. Stage 9 closure already recorded the same limit for 9.1–9.4.
6. **Stage 9.4 XGBoost** was an execution-time expansion outside the written approved model scope and is **permanently exploratory**.
7. **XGBoost five-seed validation table is degenerate** (Stage 9 closure §9: identical metrics across five recorded seeds; must not be cited as five independent fits).
8. **Stage 9.1 documentation gap** remains class B. No retroactive authorization claim.
9. **Stage 9.2 / 9.3** remain class C exploratory / sensitivity.
10. **S10-R1 is post-hoc and non-confirmatory.** Year mix of already-unblinded LC TEST under frozen maps.
11. **S10-A1 uses existing governance evidence** and does **not** independently validate Shariah compliance.
12. **LendingClub lacks contract-level Shariah fields.** No contract evidence was fabricated. L2 `INSUFFICIENT_INFORMATION` on all TEST rows is an evidence-gap status, not an applicant-level Shariah ruling.

Additional already-recorded Stage 10 notes that do not change classification: HIGH credit-band n=27; UCI and LC targets are not equivalent; UCI does not validate Shariah governance; some ECE values are absent from cited Stage 4B / UCI family-raw tables.

---

## 9. Files inspected

Authorization / protocol / prior closure:

- `docs/amendments/AMENDMENT-STAGE10-AUTHORIZATION.md`
- `docs/STAGE_10_EXPERIMENTAL_PROTOCOL.md`
- `docs/audits/STAGE_9_FINAL_CLOSURE_AUDIT.md`
- `audit/stage9_0_experimental_freeze.json`

Stage 10 audits, reports, metrics:

- `audit/stage10_i1_identity.json`
- `audit/stage10_s10_r1_year.json`
- `audit/stage10_s10_a1_gap.json`
- `audit/stage10_s10_a4_sidebyside.json`
- `docs/STAGE_10_S10_I1_IDENTITY_REPORT.md`
- `docs/STAGE_10_S10_R1_YEAR_REPORT.md`
- `docs/STAGE_10_S10_A1_GAP_REPORT.md`
- `docs/STAGE_10_S10_A4_SIDEBYSIDE_REPORT.md`
- `results/stage10/v1/metrics/s10_a4_sidebyside.json`

Freeze / policy (read-only confirmation of stored thresholds and Platt parameters):

- `results/decision/frozen_policy.json`
- `results/decision/v2/frozen_policy.json`

Path inventory (existence only): `experiments/` Stage 10/9 runners; glob for `*stage11*` and `*paper*` (none found).

---

## 10. Files modified

**None**, except the creation of this audit file.

This audit did not modify results, models, calibration, thresholds, policies, configs, freeze artifacts, historical experiment artifacts, Stage 9 records, Stage 10 activity reports, the Stage 10 protocol, or the Stage 10 authorization amendment.

---

## 11. Final execution status

Stage 10 authorized execution is complete. Stage 10 is closed for experimentation.

```text
STAGE_10_DESIGN_STATUS = COMPLETE
STAGE_10_EXECUTION = CLOSED
STAGE_10_FINAL_CLOSURE = B. PASS WITH DOCUMENTATION/REPRODUCIBILITY LIMITATION
```

| Confirmation | Status |
| --- | --- |
| File created | `docs/audits/STAGE_10_FINAL_CLOSURE_AUDIT.md` |
| Other files modified | **None** |
| Experiment run during this audit | **No** |
| Result / model / calibration / threshold changed | **No** |
| Stage 9 remains CLOSED | **Yes** |
| Stage 11 started | **No** |
| Paper drafting started | **No** |
