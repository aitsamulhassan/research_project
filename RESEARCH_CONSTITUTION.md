1. Never fabricate data.
2. Never fabricate results.
3. Never modify test labels.
4. Never fit preprocessing on test data.
5. Never select models using test performance.
6. Never claim synthetic data is real-world data.
7. Never call the Shariah layer certified without qualified expert validation.
8. Never report an experiment that was not executed.
9. Preserve all random seeds.
10. Save experiment configurations.
11. Save dataset/version hashes.
12. Every numerical claim in the paper must map to a generated experiment artifact.
13. Preserve negative results.
14. Document every methodology change.
15. Do not silently remove inconvenient results.

## Methodology amendments (Rule #14)

Rule #14 requires documenting methodology changes. The following table lists Rule #14 **amendments** and a separate **process-deviation** record. Listing `DEVIATION-001` here does **not** convert it into a scientific-method amendment and does **not** mean Stage 9.2 or Stage 9.3 were authorized before they were executed.

| ID | Status | Controls |
| --- | --- | --- |
| `AMENDMENT-SHARIAH-001` | `APPROVED` | Stage 7/8 Shariah-governance methodology remediation |
| `DEVIATION-001` | `RECORDED — PENDING RESEARCH-OWNER REVIEW` (process record, **not** retroactive authorization) | Stage 9 authorization-process gap: `docs/deviations/DEVIATION-001-stage9-authorization-gap.md` |
| `AMENDMENT-STAGE9-4-AUTHORIZATION` | `APPROVED` — 2026-09-15 | Stage 9.4 UCI independent generalization (written scope: Logistic Regression + EBM): `docs/amendments/AMENDMENT-STAGE9-4-AUTHORIZATION.md` |

Full text of the Stage 7/8 amendment: `docs/amendments/AMENDMENT-SHARIAH-001.md`

Stage 7 v2 L1/L2 is implemented (`docs/STAGE_7_SHARIAH_GOVERNANCE_REPORT_V2.md`). Stage 8 v2 per-row fusion is implemented (`docs/STAGE_8_DECISION_FUSION_REPORT_V2.md`).

This constitution is not a duplicate of the Shariah methodology. Operational boundary: `docs/shariah_methodology.md`.

**Stage 8 v2 still does not, by itself, authorize Stage 9.** Historical freeze meaning is unchanged: `audit/stage9_0_experimental_freeze.json` continues to record Stage 9 execution as not authorized at freeze time and is not rewritten.

Stage 9.1–9.3 process history is recorded in `DEVIATION-001`. That record does **not** authorize 9.2/9.3 retroactively. Stage 9.2 and Stage 9.3 remain exploratory/sensitivity analysis, not pre-registered confirmatory evidence.

`AMENDMENT-STAGE9-4-AUTHORIZATION` is `APPROVED` (approval date 2026-09-15). It authorizes the **written** Stage 9.4 UCI methodology scope: Logistic Regression + EBM. XGBoost was **not** part of that approved written scope. The XGBoost execution-time expansion remains exploratory under `DEVIATION-001`; no retroactive or prospective ratification is being sought for that expansion. Stages 9.5–9.7 remain unauthorized. Stage 9 is closed for experimentation. Stage 10 is not started.
