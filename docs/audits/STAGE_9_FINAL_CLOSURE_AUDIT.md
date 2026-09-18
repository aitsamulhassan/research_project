# Stage 9 final closure audit

| Item | Value |
| --- | --- |
| **Audit ID** | `STAGE-9-FINAL-CLOSURE-AUDIT` |
| **Audit date** | 2026-09-15 |
| **Audit type** | Documentation / artifact inspection only |
| **Experiments rerun** | **No** |
| **Models retrained** | **No** |
| **Calibration refit** | **No** |
| **Thresholds recomputed** | **No** |
| **Metrics/figures regenerated** | **No** |
| **Stage 7/8/9.1–9.4 result artifacts modified** | **No** |
| **New amendment created** | **No** |
| **Stage 10 started** | **No** |
| **Paper drafted** | **No** |
| **Git / `.git` available** | **No.** Repository-level diff verification is unavailable and is **not** fabricated. |

This audit inspects the complete Stage 9 sequence (9.0–9.4) against existing protocol, amendments, `DEVIATION-001`, reports, audit manifests, configs, result artifacts, and test files. It does **not** rewrite historical authorization records or retroactively authorize previously unauthorized work.

**Final classification: B. PASS WITH DOCUMENTATION/REPRODUCIBILITY LIMITATION**

**Closure:** Stage 9 is closed for experimentation. No further Stage 9 experiments should be started without a new prospective amendment. That amendment is **not** created by this audit.

---

## 1. Stage 9.0 freeze

**Sources:** `audit/stage9_0_experimental_freeze.json`; `results/decision/frozen_policy.json`; `results/decision/v2/frozen_policy.json`; `docs/STAGE_9_EXPERIMENTAL_PROTOCOL.md` freeze table.

| Check | Finding |
| --- | --- |
| Freeze JSON still a design-freeze record | **Yes.** `record_type`: `stage9_0_design_freeze`; `execution_timestamp`: `2026-09-15T16:34:17+00:00`; `experiments_executed`: false; `models_trained`: false; `calibrators_fitted`: false |
| Freeze JSON rewritten to look like later stages were authorized | **No.** `stage9_execution` remains `"NOT AUTHORIZED"` |
| Current SHA-256 of freeze JSON | `cc351f8f577ff4ee313fbb31f3e9f6b7e3cd1d360c63c1de88c880a5379c3fb6` — **matches** Stage 9.4 `protected_hashes_after` |
| Current Stage 8 v1 freeze SHA-256 | `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4` — **matches** freeze JSON and Stage 9.1 integrity |
| Current Stage 8 v2 freeze SHA-256 | `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b` — **matches** freeze JSON |
| `t_low` | **0.06** (v1, v2, freeze JSON, live `frozen_policy.json`) |
| `t_high` | **0.69** |
| A3/A4 `t*` / `monolithic_t` | **0.16** |
| A0 / A1 / A3 / A4 definitions | **Traceable** (see below). Freeze `a3_definition` is `DEFINED_FROM_EXISTING_STAGE_8_MONOLITHIC_BASELINE` at `t*=0.16` |
| Stage 9.0 authorized later execution | **No.** `stage9_execution` remains `"NOT AUTHORIZED"`. U1 frozen as **EBM + logistic regression only**. O-TEST Option A: no additional LC TEST policy remaps |

Traceable definitions (Stage 9.1 report §3; freeze `a3_definition`; freeze `freeze_decisions`):

| ID | Definition preserved |
| --- | --- |
| A0 | Credit-only three-way: `p_selected < 0.06` APPROVE; `0.06 <= p < 0.69` HUMAN_REVIEW; `p >= 0.69` REJECT |
| A1 | Same credit bands, fused with Stage 7 v2 L2 under G0 (proposed architecture) |
| A3 | Binary: `p_selected < 0.16` APPROVE; `p_selected >= 0.16` REJECT; HUMAN_REVIEW empty |
| A4 | Same object as A3 under the Stage 9.0 freeze |

The Stage 9 protocol **execution-gate text** was later updated (documented in `DEVIATION-001`). That is a protocol-document change **after** freeze. The freeze JSON itself was **not** rewritten to backdate authorization. The freeze JSON still stores the protocol SHA-256 from freeze time (`768100884ec46048666bbcc12bb14d182fee587f90f5490cfc5c2f3c263a5a1e`); the live protocol SHA-256 is now `7f767366ced0234175eb409996a919a7b6d9c6ef35a1a3a7d48de330944a5347` because of later gate/documentation edits. That mismatch is expected and is **not** evidence that freeze science (thresholds, A0–A4, U1) was altered.

Documentation lag (not a freeze rewrite): the live protocol header still labels `AMENDMENT-STAGE9-4-AUTHORIZATION` as `DRAFT — PENDING RESEARCH-OWNER APPROVAL`, while that amendment file **STATUS is `APPROVED`** (approval date 2026-09-15). `DEVIATION-001` also retains an earlier sentence still calling the amendment a draft; the later **Stage 9.4 — Model-scope expansion** subsection is present and is the controlling XGBoost record.

---

## 2. Authorization / deviation history

**Sources:** `docs/deviations/DEVIATION-001-stage9-authorization-gap.md`; `docs/amendments/AMENDMENT-STAGE9-4-AUTHORIZATION.md`; Stage 9.4 report provenance caveat.

`DEVIATION-001` **does** contain subsection **Stage 9.4 — Model-scope expansion**.

| Stage | Classification (authorization, not scientific PASS/FAIL) | Treatment |
| --- | --- | --- |
| **9.1** | **B. AUTHORIZED WITH DOCUMENTATION GAP** | Technically supported; chat instruction existed; freeze JSON / constitution had no matching prospective authorization record. **No retroactive authorization claim.** |
| **9.2** | **C. UNAUTHORIZED BUT SCIENTIFICALLY VALID POST-FREEZE ANALYSIS** | Permanently **exploratory / sensitivity** only. No retrospective ratification. |
| **9.3** | **C. UNAUTHORIZED BUT SCIENTIFICALLY VALID POST-FREEZE ANALYSIS** | Permanently **exploratory / sensitivity** only. No retrospective ratification. |
| **9.4 UCI methodology** | Stage 9.4 execution was prospectively authorized by `AMENDMENT-STAGE9-4-AUTHORIZATION` **APPROVED** 2026-09-15, **before** UCI run artifacts (`started` `2026-09-15T19:07:00+00:00`) | Purpose: credit-risk / calibration **methodology** generalization only. Approved written model scope: **Logistic Regression + EBM** (U1). |
| **9.4 XGBoost** | **C. UNAUTHORIZED BUT SCIENTIFICALLY VALID POST-FREEZE ANALYSIS** | **Execution-time model-scope expansion.** Permanently **exploratory**. **No retroactive or prospective ratification** is being sought. Must **not** be described as pre-registered/confirmatory. |

This audit does **not** convert class C items into class A.

---

## 3. TEST protection

**LendingClub TEST** (already unblinded in Stages 4B–8; n = 208,886):

| Check | Finding |
| --- | --- |
| New LC TEST threshold selection after Stage 9.0 freeze | **Not found.** Stage 9.1–9.3 audits: `thresholds` frozen `0.06 / 0.69 / 0.16`; Stage 9.1 `thresholds_searched: false`; Stage 9.2/9.3 do not search thresholds |
| New LC TEST model selection after freeze | **Not found.** Stage 9.1–9.3: `models_trained: false` |
| Calibration refit on LC TEST | **Not found.** Stage 9.2/9.3: `calibration_refit: false`; Stage 9.1 uses stored Platt `p_selected` |
| Stage 8 thresholds unchanged | **Yes.** Live `t_low=0.06`, `t_high=0.69`, `monolithic_t=0.16`; freeze hashes match Stage 9.1 recorded hashes |
| O-TEST Option A | Freeze: no additional LC TEST policy remaps. Stage 9.2 does not remap decisions. Stage 9.3 does not store G1/G3 as a new TEST policy |

**UCI TEST** (still-naive holdout until Stage 9.4; n = 4,502):

| Check | Finding |
| --- | --- |
| Used for UCI family selection | **No.** Selection used UCI **validation** PR-AUC. Audit: `test_used_for_selection: false` |
| Used for UCI calibrator selection | **No.** Isotonic selected on UCI **validation** Brier (Stage 5 0.001 tie rule) |
| When opened | After family and calibrator freeze in `run_stage9_4.py` (`split_xy(..., "test")` follows `select_calibrator`) |

The two TESTs are **not** interchangeable. LC TEST is a previously exposed LendingClub split. UCI TEST is a separate stratified holdout on a different dataset and target.

---

## 4. Model / calibration integrity

| Check | Finding |
| --- | --- |
| Stage 9.1–9.3 retrain/refit LC models | **No.** Manifests: `models_trained: false`; 9.1 did not load EBM for scoring |
| Stage 9.4 pipeline | **UCI-only** train/validation preprocessor, models, and calibrators (`src/preprocessing/uci_preprocessor.py`, `src/models/uci_models.py`) |
| LC model/threshold transfer to UCI | **No.** U2 freeze; no `0.06/0.69/0.16` applied to UCI; LC Platt `a,b` not reused (UCI Platt `a≈0.937`, `b≈-1.182`) |
| Stage 9.4 calibrator | **Isotonic**, selected on UCI validation Brier (0.134862 vs Platt 0.136998; gap > 0.001, not a tie) |
| Stage 9.4 XGBoost “selected model” | Exploratory: candidate was **outside approved written U1 scope**; PR-AUC-first rule still selected it among the executed families |

---

## 5. Shariah / governance boundary

| Check | Finding |
| --- | --- |
| New Shariah rules in Stage 9 | **No.** Freeze: `new_shariah_rules_added: false`; Stage 9.3: same flag |
| Shariah score / probability | **No.** Stage 9.1: governance not fed into the credit model |
| Credit probability modified by a Shariah score | **No.** A0/A1/A3 share stored `p_selected` |
| Unsupported AAOIFI clauses invented | **No.** Freeze: `aaoifi_clauses_invented: false`; `shr_001_reconstructed: false` |
| Expert validation fabricated | **No.** Amendment and Stage 7/8 records: methodological, not expert sign-off |
| UCI subjected to Shariah governance | **No.** U3 metadata-only; Stage 9.4 report and audit: no L2 fusion |
| Stage 9.4 validates Shariah architecture | **No.** Purpose is credit/calibration methodology only |

---

## 6. Stage 9.1 results — provenance only

Existing Stage 9.1 / Stage 8 v2 TEST decision counts (`audit/stage9_1_ablation_run.json`; report §8). **Not regenerated.**

| System | APPROVE | HUMAN_REVIEW | REJECT |
| --- | ---: | ---: | ---: |
| A0 | 5232 | 203627 | 27 |
| A1 / G0 | 0 | 208859 | 27 |
| A3/A4 | 61855 | 0 | 147031 |

n = 208,886. A3 identical to A4. These are existing Stage 9.1 results and **must not** be regenerated or changed.

---

## 7. Stage 9.2 results — provenance only

Existing normalized costs (`docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md` §7.2). Frozen decisions; costs only. **Not regenerated.**

| System | r=1 | r=2 | r=5 | r=10 |
| --- | ---: | ---: | ---: | ---: |
| A0 | 0.244706 | 0.245645 | 0.248460 | 0.253151 |
| A1 | 0.250030 | 0.250030 | 0.250030 | 0.250030 |
| A3/A4 | 0.549347 | 0.577976 | 0.663860 | 0.807000 |

A1 is invariant at 0.250030 under the stored FN/FP/review counts.

**Experiment G:** `NOT_EXECUTED — CITE_ONLY_PER_STAGE_9_0_FREEZE`. Cited from existing validation CSV; not rerun; LC TEST not used for G.

---

## 8. Stage 9.3 results — provenance only

Existing decision-layer allocations (`audit/stage9_3_governance_sensitivity_run.json`). **Not regenerated.**

| Scenario | Role | APPROVE | HUMAN_REVIEW | REJECT |
| --- | --- | ---: | ---: | ---: |
| G0 | **Observed / primary** | 0 | 208859 | 27 |
| G1 | **Hypothetical engineering** — all reject | 0 | 0 | 208886 |
| G3 | **Hypothetical engineering** — all review | 0 | 208886 | 0 |
| G-unsafe | **Not executed** (`NOT_EXECUTED — NOT_AUTHORIZED`) | — | — | — |

G1 and G3 are **hypothetical engineering cases**, **not** empirical Shariah findings.

---

## 9. Stage 9.4 UCI — provenance only

Existing UCI TEST metrics for the **executed** XGBoost + isotonic pipeline (`results/uci_generalization/v1/metrics/uci_test_selected.json`). **Not recomputed.**

| Metric | Stored value (report 6 d.p.) |
| --- | ---: |
| ROC-AUC | 0.770878 |
| PR-AUC | 0.522421 |
| Brier | 0.136853 |
| Log loss | 0.449533 |
| ECE | 0.017443 |

n = 4,502. Selected calibrator: isotonic. UCI target = `default payment next month`. LendingClub target = `Default` (Charged Off vs Fully Paid). Datasets are **not** directly equivalent. UCI results are **methodology-generalization evidence only** and do **not** validate the evidence-separated / Shariah architecture.

Existing UCI **validation family** means (report; not regenerated): logistic regression PR-AUC 0.520869; EBM PR-AUC 0.527686 / raw Brier 0.138074; XGBoost PR-AUC 0.534172 / raw Brier 0.178710. Isotonic validation Brier 0.134862 vs Platt 0.136998 (gap > 0.001).

XGBoost is **exploratory** (model-scope deviation). Observed selection fact: EBM had **better raw validation Brier**; XGBoost had **better validation PR-AUC**; the declared PR-AUC-first rule selected XGBoost. Because XGBoost was outside approved written scope, that “selected model” label is **exploratory**, not a pre-registered confirmatory outcome. XGBoost validation metrics are identical across all five recorded seeds (degenerate seed table; must not be cited as five independent fits).

Logistic regression and EBM remain **pre-registered scope** under `AMENDMENT-STAGE9-4-AUTHORIZATION`.

---

## 10. Artifact integrity

Live SHA-256 values (this audit; **not** a git diff). Stage 8 and Stage 9.1–9.3 result hashes **match** the Stage 9.4 `protected_hashes_after` snapshot:

| Artifact | Live SHA-256 | Status |
| --- | --- | --- |
| `results/decision/frozen_policy.json` | `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4` | Unchanged vs freeze / 9.1 / 9.4 protection |
| `results/decision/v2/frozen_policy.json` | `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b` | Unchanged |
| `results/calibration/test/ebm_seed42_calibrated.csv` | `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb` | Unchanged |
| `audit/stage9_0_experimental_freeze.json` | `cc351f8f577ff4ee313fbb31f3e9f6b7e3cd1d360c63c1de88c880a5379c3fb6` | Still `stage9_execution: NOT AUTHORIZED` |
| `audit/stage9_1_ablation_run.json` | `8f93bf371844fa5ba8f2014c8d1b1a4ccc5b919f90fd148005de82f9d6a7704b` | Unchanged vs 9.4 protection |
| `docs/STAGE_9_1_ABLATION_REPORT.md` | `4d6f227503e282b1b79048fe7012d85f6ad8d90f53e424d689c170d56c9c23fe` | Unchanged |
| `results/cost_sensitivity/v1/metrics/cost_sensitivity_summary.json` | `e8d3c4ca07576885a00603ec6344010fa02a34ce0cb8e19b1b54f798b2a88289` | Unchanged (9.2 results) |
| `audit/stage9_2_cost_sensitivity_run.json` | `ba69bd35ea899717d4435ff755a786c36e1251033162de7da96ebd073d51f889` | Unchanged |
| `docs/STAGE_9_2_COST_SENSITIVITY_REPORT.md` | `5ec4712abcfd5934dcb11d50b4780b798ae80fe3cdb4291b46c958ade31d58ba` | Unchanged |
| `audit/stage9_3_governance_sensitivity_run.json` | `91a84ca8fb2c986322f6db98745a8fc7c8ea464bde83172faa6a746936a6c75f` | Unchanged vs 9.4 protection |
| `docs/STAGE_9_3_GOVERNANCE_SENSITIVITY_REPORT.md` | `6172fcb9038b45af9b0224f431cfeaece6a50e961ac8efad84c6c3928a6ff5ed` | Unchanged |
| `results/uci_generalization/v1/metrics/uci_test_selected.json` | `9d2635919c7dfe0a8cc03040cffcb1cbc750db8235507e94ee2e215762000a02` | Unchanged numerical result file |
| `docs/STAGE_8_DECISION_FUSION_REPORT_V2.md` | `211337df3f4e1d2600198e645f4ed6ad50a2f3824b1073fcd397d9ac4c98a36d` | Unchanged |
| `docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md` | `6d8185de96f7b27f3a037129c36b489752b886babfb9bd620f76bb1359ef6db0` | Unchanged |

Documented markdown / audit-manifest provenance **after** the Stage 9.4 runner (numbers in result JSON/CSV were not rewritten):

| File | Note |
| --- | --- |
| `docs/STAGE_9_4_UCI_GENERALIZATION_REPORT.md` | Runner stored `report_sha256` `60bd9db04b9b1984…`. Live hash is `65aba5b02afd6c18dd222920874a34cbd58dd875833c3aad221211db2562056b` because a **provenance caveat** was added later. Metrics in the report were not changed. |
| `docs/deviations/DEVIATION-001-stage9-authorization-gap.md` | Later **Stage 9.4 — Model-scope expansion** subsection. |
| `audit/stage9_4_uci_run.json` | `test_summary` was updated after the first pytest (recorded in the Stage 9.4 post-execution audit). Result metric files were not rewritten to hide deviations. |
| This closure audit | New file only. |

No result file was rewritten in this task to hide deviations. Historical freeze JSON was not silently replaced. Historical audits (`STAGE_9_4_POST_EXECUTION_AUDIT.md`, Stage 9.1–9.3 run JSONs) were not replaced by this audit.

**Limitation:** no `.git` directory (`gitdir` = false). Repository-level `git diff` / `git status` **cannot** be produced and **must not** be fabricated. Integrity here is content + SHA-256 of named artifacts.

---

## 11. Test / pytest evidence (stored; not rerun)

This audit **did not** rerun pytest. Stored manifests:

| Stage | Stored command | Stored summary | What that supports |
| --- | --- | --- | --- |
| 9.1 | `python -m pytest tests/test_stage9_1_ablation.py -q --tb=short` | `9 passed in 0.54s` (exit 0) | Integrity of frozen maps / hashes in that test module, **not** independent recomputation of all paper numbers |
| 9.2 | `tests/test_stage9_2_cost_sensitivity.py` | `10 passed in 0.78s` | Cost-formula / freeze-threshold tests as written |
| 9.3 | `tests/test_stage9_3_governance_sensitivity.py` | `13 passed in 1.16s` | G0/G1/G3 algebra and G-unsafe block as written |
| 9.4 | `tests/test_stage9_4_uci.py` | `14 passed in 2.45s` | Split hashes, preprocessor guards, selection-rule toys, audit flags. **Does not lock** 0.770878 etc. First runner pass ran pytest before the audit file existed; summary was later updated |

Passing tests **do not**, by themselves, prove the reported numerical metrics unless a test asserts those numbers. Stage 9.4 tests do **not** assert the UCI TEST point estimates.

---

## 12. Final classification

**B. PASS WITH DOCUMENTATION/REPRODUCIBILITY LIMITATION**

Not A: authorization gaps (9.1 documentation class B; 9.2/9.3 class C; 9.4 XGBoost class C), `git_commit` null throughout, pytest evidence does not lock all reported metrics, XGBoost seed table is degenerate, protocol/deviation leftover “DRAFT” wording vs approved amendment, Stage 9.4 report hash changed after the provenance caveat.

Not C: no correction of scientific result files is required for the executed, documented protocol. Stored numbers match the cited reports. Thresholds and Stage 8 hashes hold. Leftover draft wording is a **documentation lag**, not a hidden result rewrite.

Not D: no LC TEST model/threshold/calibration selection after freeze; no UCI TEST selection of family or calibrator.

Git unavailability is recorded as a **verification limitation**, not as a reason to choose C or D.

---

## 13. Publication-safe interpretation

### Confirmatory / freeze-backed evidence

- Stage 9.0 design freeze: A0 / A1 / A3=A4 definitions; `t_low=0.06`, `t_high=0.69`, `t*=0.16`; O-TEST Option A; U1 = LR+EBM; U2/U3.
- Frozen Stage 8 v2 fusion artifacts and Stage 5 LC Platt TEST metrics **as already produced before Stage 9** (cited, not restaged).
- Stage 9.1 ablation **counts** as a re-application of those frozen maps (technically supported; authorization class **B** — disclose the documentation gap; do not pretend freeze JSON authorized 9.1 in advance).
- Stage 9.4 **UCI logistic regression and EBM** credit/calibration methodology on the frozen UCI split (approved written scope), including the semantic non-equivalence of targets.

### Exploratory / deviation-bound evidence

- Stage 9.2 cost sensitivity (class **C**; exploratory / sensitivity).
- Stage 9.3 G1/G3 (class **C**; hypothetical engineering, not Shariah findings). G0 observed counts are citations of frozen Stage 8 v2 / 9.1 A1.
- Stage 9.4 **XGBoost** and any “selected UCI model” claim that depends on XGBoost (class **C**; execution-time expansion; exploratory; no ratification).

**Do not claim that all Stage 9 results are confirmatory or pre-registered.**

---

## 14. Closure decision

Stage 9.0–9.4 have been executed or recorded as specified above. Stages **9.5–9.7 remain unauthorized**. Stage 10 has not been started.

**Stage 9 is closed for experimentation. No further Stage 9 experiments should be started without a new prospective amendment.**

This audit does **not** create that amendment.

---

## 15. Stop

No other files were modified. No experiments, reruns, metric changes, or Stage 10 work follow from this audit.
