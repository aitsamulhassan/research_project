# Engine v2 Freeze Candidate

**DRAFT — NOT A COMMITTED RELEASE**

This document records the pre-commit freeze-candidate state observed against parent commit d49f39a68b740ae464f32f0d7a963b8e7e9938db. References to HEAD, the uncommitted working tree, and clean-checkout limitations describe that pre-commit baseline. Once committed, these statements remain historical audit observations, not descriptions of the repository's subsequent HEAD. This snapshot does not constitute a published release, authenticated regulatory ruling, or Shariah certification.

This file was prepared as a supervisor-review candidate before any snapshot commit. It is not a tag, a release signature, or a qualified expert attestation. Nothing in this document was created by `git add`, `git commit`, `git tag`, or `git push`.

The pre-edit manifest SHA-256, recorded in STEP 3B-7B-1 before this clarification, is `8f31ce2179c864dd2dc55a65f82f8e87f3d5dd279360346a4ea923c627f65cfa`. That value is a historical checksum of the earlier file bytes. It is not the checksum of this clarified text.

Prepared against parent commit `d49f39a68b740ae464f32f0d7a963b8e7e9938db` on branch `main`. At that pre-commit baseline, the scope-gated implementation existed only in the uncommitted working tree.

## A. Snapshot Candidate Identity

| Item | Value |
|---|---|
| Parent HEAD at pre-commit baseline | `d49f39a68b740ae464f32f0d7a963b8e7e9938db` |
| Branch at pre-commit baseline | `main` |
| Governance engine in that parent | `stage7-shariah-engine-v1` |
| Governance engine in the pre-commit working tree | `stage7-shariah-engine-v2-scope-gated` |
| Applicability layer | `stage7-applicability-scope-unknown-v1` |
| Catalog version | `stage7-shariah-catalog-v1` |
| L1/L2 version | `stage7-l1l2-v2` |
| Stage 8 decision policy v1 | `stage8-v1` in `results/decision/frozen_policy.json` |
| Stage 8 decision policy v2 | `stage8-v2` in `results/decision/v2/frozen_policy.json` |

Stage 8 decision-policy v2 is not the governance-engine v2. Policy v2 reuses the frozen thresholds and sets `thresholds_reselected` to false. At the pre-commit baseline, governance-engine v2 existed only as the uncommitted scope gate.

`git diff --stat` against HEAD, before this manifest existed:

```
 src/shariah/engine.py       | 214 ++++++++++++++++++++++++++++++++++++++++++--
 src/shariah/evidence.py     |   3 +-
 src/shariah/rules.py        | 193 +++++++++++++++++++++++++++++----------
 src/shariah/schema.py       |   2 +-
 tests/test_shariah_rules.py |  76 +++++++++++++++-
 tests/test_stage7_l1l2.py   |  75 +++++++++++++++-
 6 files changed, 503 insertions(+), 60 deletions(-)
```

`git diff --check` reported no whitespace errors. A scan of the candidate diff found no credentials, private keys, or API tokens. The only match for the word "password" is the existing AAOIFI abstention sentence that official clause text is access-controlled and password-protected.

## B. Exact Proposed File Allowlist

The proposed snapshot is these 11 safety source and test files, plus this manifest. No historical artifact is part of the proposed commit.

Tracked modifications:

1. `src/shariah/engine.py`
2. `src/shariah/rules.py`
3. `src/shariah/evidence.py`
4. `src/shariah/schema.py`
5. `tests/test_shariah_rules.py`
6. `tests/test_stage7_l1l2.py`

Untracked files that belong in the snapshot:

7. `src/shariah/applicability.py`
8. `tests/test_shariah_safety_red.py`
9. `tests/test_shariah_documentary_flags_red.py`
10. `tests/test_shariah_security_claim_red.py`
11. `tests/test_shariah_applicability_trust_red.py`

Manifest, present in the pre-commit working tree and not part of parent `d49f39a68b740ae464f32f0d7a963b8e7e9938db`:

12. `docs/reproducibility/ENGINE_V2_FREEZE_CANDIDATE.md`

`git ls-files --others --exclude-standard` listed only the five untracked source and test files above before this manifest was written. No other untracked path was present.

## C. Historical Experiment Artifact Registry

These files are already in Git unless noted. They were not modified by this step. Digests below were recomputed during this freeze preparation. A digest is called previously recorded only when the manuscript or source register already stored that exact value.

| Path | Exists | Git | SHA-256 recomputed this step | Designation | Version | Limit |
|---|---|---|---|---|---|---|
| `results/metrics/lendingclub_dimensions.json` | yes | tracked | `e3f9f364d043c430cc3c17a80abc005262855bc9db7bbaa4adc1c313c723c4e3` | historical | dataset inventory, `n_rows` 1347681 | Digest was not previously registered. This step did not recount the CSV. |
| `results/metrics/lendingclub_split_summary.json` | yes | tracked | `28e20f2ba12dbd188377bf45a82acd3916082868d486c39d0136b0cccbf055b2` | historical | chronological split 941267 / 197528 / 208886 | Digest was not previously registered. The three stored counts sum to 1347681. |
| `data/raw/LC_loans_granting_model_dataset.csv` | yes, local | gitignored (`data/raw/`) | `207d65b2712f775a91404496ab27c786ac0da6b0f977f849e6d5d8149e925acc` | historical input | Zenodo extract named in the manuscript | Recomputed digest equals the manuscript-recorded digest. A clean checkout does not contain the file. |
| `data/raw/default+of+credit+card+clients.zip` | yes, local | gitignored | `56c885f84457f6680f8438f02bfcdac9579323d8a94465ee5f26e32baa727602` | historical UCI input | UCI dataset 350 zip | Recomputed digest equals the manuscript-recorded digest. Not a Shariah dataset. |
| `results/metrics/stage4b_test_metrics.json` | yes | tracked | `960c01643a671805daa1c692e9034454a94d6088651c6336076433b3e8bdc612` | historical | `stage4b-lc-granting-v1` | Digest was not previously registered. TEST metrics were not recomputed. |
| `results/calibration/metrics/stage5_test_metrics.json` | yes | tracked | `a6c8ab44676d62109c1a346dbcf14a12a745b761f13b9fda6a9002853fc326e3` | historical | Stage 5 seed 42 | Digest was not previously registered. TEST metrics were not recomputed. |
| `results/calibration/test/ebm_seed42_calibrated.csv` | yes, local | gitignored (`results/calibration/test/`) | `e15ddd2f85a6c3fc9d0a79eecb578f7a94ded8a7efc63d9d114212728b2469eb` | historical probability file | Stage 5 `p_selected` | Recomputed digest equals the manuscript-recorded digest. Absent from a clean checkout. |
| `results/decision/frozen_policy.json` | yes | tracked | `4d3da6a9e5bac2b38b546c7a5a60e870bf83f30adcadf67f067f99951e32f0c4` | historical | `stage8-v1` | Recomputed digest equals the manuscript-recorded v1 freeze digest. |
| `results/decision/v2/frozen_policy.json` | yes | tracked | `b874782326a8f20ed9bb7df1aa5ed1c75f883d8b6cba76b68991181d50b1604b` | historical | `stage8-v2` policy, not governance-engine v2 | Recomputed digest equals the manuscript-recorded v2 freeze digest. `thresholds_reselected` is false. |
| `results/decision/metrics/fused_test.json` | yes | tracked | `53871e050a20f1536ad9ebf85e64f92d19747c7e9aad2748e4ede6b472dd8bc9` | historical | Stage 8 fused TEST counts | Digest was not previously registered. |
| `results/decision/v2/metrics/fused_test.json` | yes | tracked | `53871e050a20f1536ad9ebf85e64f92d19747c7e9aad2748e4ede6b472dd8bc9` | historical | Stage 8 v2 fused TEST counts | Same recomputed digest as the v1 metrics file. The files are byte-identical. This is not a v2 governance-engine rerun. |
| `results/decision/metrics/monolithic_test.json` | yes | tracked | `d4c18db2d6f62c367b5cc894a94236267ff4e28516a40df82bc4791be2a6efe9` | historical | single-threshold map | Digest was not previously registered. |
| `results/shariah/rule_evaluations.json` | yes | tracked | `c0613d05abb0ba7b5d9e696d2386fb455acf5547673fd0adc0ca6b30d28ca7dd` | historical | `stage7-shariah-gov-v1`; engine `stage7-shariah-engine-v1` on all 10 evaluations | Digest was not previously registered. Do not relabel as v2. |
| `results/shariah/v2/l2_fixture_evaluations.json` | yes | tracked | `e56dbffff698b4de9bb0ebacf2dc5c4ee6dba19ac36dcadc13e349630b7ea209` | historical | experiment id `stage7-shariah-gov-v2`; engine field `stage7-shariah-engine-v1` on all 3 evaluations | The experiment id says v2. The engine identifier inside each evaluation remains v1. |

Stored LendingClub TEST fusion counts in both fused-test files:

- APPROVE: 0
- HUMAN_REVIEW: 208859
- REJECT: 27
- `n`: 208886

These counts belong to the stored experiments. They are not a newly generated governance-engine v2 evaluation.

The monolithic stored map is APPROVE 61855, HUMAN_REVIEW 0, REJECT 147031. That is a credit-threshold map, not a Shariah result.

## D. Live Scope-Gated Engine Version Registry

Working-tree constants, inspected in source:

- `ENGINE_VERSION = "stage7-shariah-engine-v2-scope-gated"` in `src/shariah/engine.py`
- `APPLICABILITY_VERSION = "stage7-applicability-scope-unknown-v1"` in `src/shariah/applicability.py`
- `CATALOG_VERSION = "stage7-shariah-catalog-v1"`
- `L1L2_VERSION = "stage7-l1l2-v2"`

The parent commit, inspected with `git show d49f39a68b740ae464f32f0d7a963b8e7e9938db:src/shariah/engine.py`, has `ENGINE_VERSION = "stage7-shariah-engine-v1"` with the same catalog and L1/L2 versions. That parent's `schema.py` defaults `claims_shariah_compliant_security` to `False`. The pre-commit working tree uses `None`.

Behavior of the scope-gated engine in the pre-commit working tree:

- Diagnostic predicates remain available on `diagnostic_predicate_result` and `diagnostic_predicate_reason`.
- These six source rules default to `SCOPE_UNKNOWN` for every jurisdiction, including PK, GB, US, and unknown: `SH-SBP-SGF-002`, `SH-SBP-SGF-003`, `SH-SBP-MUR-INV-001`, `SH-SBP-MUR-INV-002`, `SH-SBP-MUR-PAY-001`, `SH-SECP-SGR-SEC-001`.
- `VERIFIED_IN_SCOPE` is a reserved name. `decide_applicability` does not emit it. `trusted_scope_established` is therefore false.
- `trusted_expert_authorization_available` returns false. Catalog `EXPERT_VALIDATED`, a nonempty expert record, `applicability_scope.verified`, a forged contract label, a jurisdiction string, and a forged clause do not open affirmative overall PASS.
- An applicable diagnostic `PASS` or `NOT_STRUCTURABLE_WITHOUT_REDESIGN` is emitted as guarded `REVIEW` while scope is unknown.
- Applicable source-specific outcomes stay noncertifying. `certification_claim` remains false.
- Synthetic hard-stop cases can move from frozen-matrix `REJECT` to `HUMAN_REVIEW` because the public governance status becomes `REVIEW`. That is a research-screen change. It is not a change to stored credit predictions and not a correction of historical JSON.
- No credit-model performance improvement is implied.

Historical v1 remains the label for stored Stage 7 evaluations and for the frozen LendingClub TEST decisions. Those files are not retrospectively relabeled.

## E. Frozen Model and Threshold Provenance

Two different EBMs must stay separate.

| Model | Training data | Role | Artifact | SHA-256 recomputed this step | Previously recorded? |
|---|---|---|---|---|---|
| Stage 4B final EBM | Train plus validation refit | Family comparison on TEST. Not the decision-fusion probability source. | `results/artifacts/final_explainable_boosting_machine_seed42.joblib` | `0da490baaa9d6f2c9ae85fcb2628cf05d40abc4fb2120cff0b88c2e6f3bbe789` | No. The manuscript states this hash was not recorded. This digest is a freeze-preparation calculation. |
| Stage 5 train-only EBM | `TRAIN_ONLY`, `n_train` 941267, seed 42, interactions 0 | Source of downstream probabilities after validation-only Platt scaling | `results/calibration/artifacts/ebm_train_only_seed42.joblib` | `8d373df1b576ca74f498d2bfcc54653cbf43d37b0af69400a26e20ab98a3a0c4` | Yes. Recomputed digest equals the manuscript-recorded digest. |
| Train-only preprocessor | Train-only imputer used by Stage 5 | Not the Stage 4B train-plus-validation preprocessor | `results/artifacts/lendingclub_preprocessor.joblib` | `d87ce3a8a2bcdcc3d646110767e5f292276ed2775ff04dccd491ccf0c0836445` | No manuscript registration was found for this digest. Freeze-preparation calculation only. |

Recorded Stage 4B EBM TEST metrics in `results/metrics/stage4b_test_metrics.json`, family `explainable_boosting_machine`, seed 42, `n` 208886. Not recomputed:

- ROC-AUC `0.6799408767429772`
- PR-AUC `0.3534066581608194`
- Brier `0.15684495750106664`
- That record has no ECE field.

Recorded Stage 5 Platt TEST metrics in `results/calibration/metrics/stage5_test_metrics.json`, method `platt`, seed 42, `n` 208886. Not recomputed:

- ROC-AUC `0.6776693941139847`
- PR-AUC `0.35096314719303284`
- Brier `0.15616920271522994`
- ECE `0.020267295489117824`

Stage 5 raw ROC-AUC is the same stored value as Platt ROC-AUC. The Stage 4B EBM ROC-AUC is a different fit.

Platt parameters, validation fit, in `results/calibration/artifacts/platt_record.json` and both frozen policies:

- `a` `1.1988263209549705`
- `b` `0.6697765046966161`
- Recomputed `platt_record.json` SHA-256: `9ca39188c961e5d1222346a7fba14902cb58dc24b78a0de2136b6437de01f44c`
- That JSON digest was not previously registered.

Thresholds in both policy files: `t_low` `0.06`, `t_high` `0.69`, `selection_split` `validation`. Stage 8 v2 `thresholds_source` points at `results/decision/frozen_policy.json`.

Selection records, digests computed this step and not previously registered:

- `experiments/stage4b_credit_risk/selected_configurations.json`: `a18ce2a571c2bde21d7f4f542456b7bce3d78f8893fd2b52eb043d4bccb09c73`. Selected family `explainable_boosting_machine` before test.
- `experiments/stage5_calibration/selected_calibration.json`: `126065e1b25b0d77b1875c6ed2a1d488ea59222653edd4b4fbd65792e2349c41`. Selected method `platt` before test.
- `experiments/stage5_calibration/checkpoints/train_only_ebm_meta.json`: `a5b9240ce3e3ee3e93f896455ff847cf462b89caed68c158a26b8d2a2667eb52`.

`results/decision/v2/metrics/predictive_test_stage5.json` SHA-256 `798d95a7cb665915a2b175c26bf301780a9bda1ae58b8d2be4a03cbc1f1bb992` repeats the stored Platt TEST metrics. Digest not previously registered. Not a new TEST calculation.

## F. Local SHA-256 Inventory and Verification Limits

Every digest in sections C and E was computed on this machine during freeze preparation with SHA-256 of the current file bytes. Equality with a manuscript or source-register string means the local file matches that previously recorded string. It does not create a new historical registration, and it does not authenticate a publisher.

Limits:

- Gitignored inputs can disappear from another checkout even when the digest matched here.
- The Stage 4B joblib digest and the preprocessor digest are new observations. They must not be described as hashes that were frozen with the original experiment.
- Identical SHA-256 values for the two fused-test JSON files mean those two files currently have the same bytes. They remain historical decision-count files.
- No TEST ROC-AUC, PR-AUC, Brier, or ECE was recalculated from predictions.

## G. Regulatory Source Authentication Limits

Register: `docs/shariah/source_register.json`, SHA-256 `5c6ede8c299a1a7b57970bc21fb80b98e83ca68632b80082e5b12cd636e3c7a2`, tracked. Catalog: `docs/shariah/rule_catalog.json`, SHA-256 `4eef75aad02540726c5784538dc961db0ef9f84d40e94526f3d5f8d33c94e6cd`, tracked. Both digests were computed this step and were not previously registered as file digests. Catalog labels were not changed.

These claims are different:

| Claim | Status in this repository |
|---|---|
| A local PDF matches a recorded digest | True for the two files below |
| The PDF is an authenticated official regulator byte stream | Not established |
| A reviewer has interpreted the clause for this study | Not established |
| A regulatory-applicability record is verified | Not established. Live status is `SCOPE_UNKNOWN` |
| A qualified Shariah expert has validated a rule | Not established. No catalog row is `EXPERT_VALIDATED` |

| Local file | SHA-256 recomputed this step | Compared with |
|---|---|---|
| `audit/source_downloads/picg_sgf_2025.pdf` | `6c32d43d528104271bccd2dd228ba8ca33e94abe459494c6d4abdae41ef06ca1` | Equals the register digest for `SRC-SBP-SGF-2025-TEXT`. The register identifies a PICG-hosted copy. The official SBP annex was recorded as HTTP 403. Matching checksums do not make this an authenticated official SBP byte stream. |
| `audit/source_downloads/mufap_sgr2023.pdf` | `7ffe4179154a793da18cfb1e783a32bf74408bea7513dffbf2b42b67f4929ba7` | Equals the register digest for `SRC-SECP-SGR-2023-SRO-TEXT`. The register identifies a MUFAP-hosted copy. The official SECP PDF was recorded as HTTP 403. Matching checksums do not make this an authenticated official SECP byte stream. |
| `audit/source_downloads/baf_sgf.pdf` | `becd6b94ae3e0be1f30c482b1ad8b7158870c424963aa107a27a2763d46c09a8` | Does not equal the registered SGF digest. Extra local file. Not part of the snapshot. |

All three PDFs are gitignored under `audit/source_downloads/*`. AAOIFI SS (8) and SS (9) entries have null hashes, `NOT_VERIFIED` clauses, and no local operative text. IBD Circular 01 of 2012 and IFPD Circular 08 of 2024 have null hashes. No qualified expert-validation record is stored.

## H. Environment and Reproduction Dependencies

`requirements.txt` lists minimum versions only. It is not a lockfile. No lockfile was created in this step.

Runtime observed on this machine:

- Python 3.12.10
- pytest 9.1.1
- scikit-learn 1.9.0
- NumPy 2.5.2
- pandas 3.0.5

Interpret, SHAP, and XGBoost versions were not queried in this step.

A clean checkout of parent `d49f39a68b740ae464f32f0d7a963b8e7e9938db`, as observed before this snapshot:

- Has governance engine v1, not the scope-gated v2.
- Does not contain this manifest or the then-untracked safety tests.
- Does not contain `data/raw/`, `results/calibration/test/`, or `audit/source_downloads/` PDFs.
- Does contain the tracked Stage 4B EBM joblib, the tracked Stage 5 train-only EBM joblib, and the tracked preprocessor joblib.

The safety suite was reproducible on the pre-commit working tree. A clean checkout of that parent is not a full reproduction of v2, and the gitignored inputs remain absent from Git. That parent-checkout test was not run. These sentences describe the pre-commit baseline. They do not describe a later HEAD.

## I. Test Execution Record

Commands used `PYTHONDONTWRITEBYTECODE=1` and `python -m pytest -p no:cacheprovider -q --tb=line`. Passing tests are software checks. They do not validate a regulatory applicability decision or a Shariah ruling.

| Suite | Result |
|---|---|
| `tests/test_shariah_applicability_trust_red.py` | 41 passed, 0 failed, 0 skipped, 1.58 s |
| Four safety files: applicability trust, security claim, documentary flags, safety | 149 passed, 0 failed, 0 skipped, 1.79 s |
| Five legacy modules: `test_shariah_rules.py`, `test_shariah_provenance.py`, `test_stage7_l1l2.py`, `test_stage8_decision.py`, `test_stage8_v2.py` | 86 passed, 0 failed, 0 skipped, 2.15 s |
| Full suite, `python -m pytest -p no:cacheprovider -q --tb=line` | 383 passed, 0 failed, 0 skipped, 0 errors, 2 warnings, 61.18 s |

Both warnings are the existing scikit-learn `FutureWarning` for the `penalty` argument in `tests/test_stage4b_modeling.py::test_seeds_reproduce_logistic_within_tolerance`.

## J. Scientific Claim Boundaries

Supported as stored historical evidence, subject to the gitignore limits above:

- LendingClub inventory 1347681 and the chronological split 941267 / 197528 / 208886.
- Stage 4B EBM TEST metrics and Stage 5 Platt TEST metrics as separate fits.
- Frozen thresholds 0.06 and 0.69.
- Stored fused TEST counts 0 / 208859 / 27.

Supported as pre-commit working-tree software behavior:

- Diagnostic predicate, applicability decision, guarded rule result, and overall governance status are separate fields.
- Six source rules are `SCOPE_UNKNOWN`.
- Unscoped source `PASS` and unscoped source hard stops are withheld from the public rule result.
- Forged catalog metadata does not produce overall PASS.
- `certification_claim` is false.

Not supported:

- Authenticated official SBP or SECP bytes.
- A verified in-scope regulatory determination.
- Qualified expert validation.
- A contract execution date. The applicability record uses `CONTRACT_DATE_NOT_IN_SCHEMA`.
- An Islamic-finance contract-level benchmark for the LendingClub extract.
- Any claim that v2 improved credit-model performance.
- Relabeling stored v1 audits or Stage 8 counts as v2 output.

## K. Missing Requirements for Qualified Expert Review

Before any `VERIFIED_IN_SCOPE` or expert-authorized PASS can exist, an external review would need:

- Official primary-source bytes for the SBP and SECP instruments, stored and hashed separately from the PICG and MUFAP copies.
- A reviewed applicability record tied to institution, product, jurisdiction, and dates.
- A contract execution date in the evidence contract.
- A qualified expert-validation record produced outside the catalog's self-declared fields.
- A decision, by that reviewer, about whether any source rule is in scope. This repository does not supply that decision.

This draft does not add a synthetic verified-scope example.

## L. Supervisor Approval Checklist

The checklist below records the approval conditions written before staging. It does not assert that a later commit exists, and it does not change the draft designation of this research snapshot.

- [ ] The allowlist is exactly the 11 safety source and test files plus this manifest.
- [ ] No historical Stage 4B–8 file, joblib, catalog, source register, fixture, manuscript, or dependency file is included.
- [ ] HEAD remains the parent, and stored audits stay `stage7-shariah-engine-v1`.
- [ ] The commit message names the snapshot as a scope-gated research screen, not as a regulatory or religious certification.
- [ ] The manuscript is not updated in the same commit unless a separate wording review is approved.
- [ ] Gitignored data, calibrated scores, and third-party PDFs stay outside the commit.
- [ ] No `VERIFIED_IN_SCOPE` fixture and no expert attestation is added.

**DRAFT — NOT A COMMITTED RELEASE**
