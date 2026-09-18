# Literature-review evidence package

| Item | Value |
| --- | --- |
| **Document ID** | `LITERATURE-REVIEW-EVIDENCE` |
| **Date** | 2026-09-16 |
| **Type** | Research / literature-review package only — **no manuscript** |
| **Manuscript drafted** | **No** |
| **Experiments run** | **No** |
| **Stage 11** | **NOT STARTED** |
| **Paper drafting protocol modified** | **No** |

This package collects **candidate citations** for a later Related Work section. It does **not** write the paper. It does **not** validate this project’s TEST metrics. Literature cannot confirm Stage 4B/5/8/9/10 numbers.

**Authoritative empirical source remains** `docs/PAPER_EVIDENCE_INVENTORY.md`.  
**Drafting rules remain** `docs/PAPER_DRAFTING_PROTOCOL.md` (unchanged).

Companion files:

- `docs/literature/LITERATURE_SOURCE_REGISTER.csv`
- `docs/literature/LITERATURE_CLAIM_MATRIX.csv`
- `audit/literature_review_evidence_audit.json`

---

## 0. Scope warnings (binding)

### Datasets actually executed

| Dataset | Role in this project |
| --- | --- |
| Zenodo LendingClub granting-model extract (`10.5281/zenodo.11295916`) | **PRIMARY** |
| UCI Default of Credit Card Clients (`10.24432/C55S3H`) | **Independent methodology only** |

**Not executed:** German Credit (UCI 144), Australian Credit Approval (UCI 143), PaySim, IEEE-CIS, Kaggle as a third raw file, any fraud dataset. Those may appear only as **literature-context** datasets.

### Model contexts (do not merge)

| Context | Paper treatment of literature |
| --- | --- |
| Stage 4B LC families (LR, EBM, RF, **LC XGBoost**) | Cite ML/credit-scoring method papers as background |
| Stage 5 TRAIN-only EBM + Platt `p_selected` | Cite GAM/EBM/Platt/isotonic as **method** papers |
| Stage 9.4 UCI LR + EBM | Cite Yeh/UCI as dataset provenance; not LC architecture validation |
| Stage 9.4 UCI XGBoost | Cite Chen & Guestrin only as algorithm; class remains `EXECUTION-TIME EXPANSION, EXPLORATORY` |
| Stage 4B LC XGBoost | Distinct from 9.4 UCI XGBoost |

### Shariah

Prototype for **Shariah-oriented governance / evidence traceability**. Not certification. LendingClub has **no** contract-level Shariah fields. Do not invent invoices, possession, or applicant-level compliance.

---

## 1. How sources were verified

Verification session: 2026-09-16. Methods: publisher/official pages via web search and selected page retrieval (ScienceDirect, ACM, Springer, Wiley, NeurIPS PDF, PMLR, UCI, CFPB, SBP HTML, AAOIFI listing, IFSB FAQ PDF, project `docs/shariah/source_register.json`).

| Label | Meaning |
| --- | --- |
| `VERIFIED` | Title/authors/year/venue and DOI or official URL confirmed on a publisher or official landing page (or already `SOURCE_VERIFIED` in the Stage 7 register) |
| `PARTIAL` | Bibliographic identity confirmed from multiple scholarly records, but at least one field (DOI, official URL, or creator name) is missing or not re-fetched |
| `IDENTITY_ONLY` | Instrument exists; operative clauses not retrieved |
| `UNVERIFIED` | Field not confirmed this session — must not be invented later |

Search snippets were **not** treated as proof of this project’s empirical claims. They were used only to locate records, then checked against publisher/official pages where possible.

No citations were invented. Sources that could not be identified with title + authors + year + venue were omitted.

---

## 2. Topic coverage

### 2.1 AI / ML credit-risk assessment

| ID | Source | Year | Type | What it can support | What it cannot |
| --- | --- | --- | --- | --- | --- |
| LIT-002 | Baesens et al., *JORS* | 2003 | PEER_REVIEWED | ML classifiers have been benchmarked on real credit data | This project’s ROC-AUC |
| LIT-003 | Lessmann et al., *EJOR* | 2015 | PEER_REVIEWED | Updated public benchmark of scoring algorithms | This project’s family ranking |

Population/time differ (institutional European data, pre-2015 methods). **Methodology only.**

### 2.2 Credit scoring and default prediction

| ID | Source | Year | Type | Support |
| --- | --- | --- | --- | --- |
| LIT-001 | Hand & Henley, *JRSS A* | 1997 | PEER_REVIEWED | Scorecards as statistical classification into good/bad risk |
| LIT-004 | Yeh & Lien, *ESWA* | 2009 | PEER_REVIEWED | PD estimation vs binary labels; Taiwan credit-card clients |

Hand & Henley note commercial confidentiality of industry scorecards. Yeh & Lien’s ANN ranking is **their** result, not Stage 9.4.

### 2.3 Explainable AI for credit-risk decisions

| ID | Source | Year | Type | Support |
| --- | --- | --- | --- | --- |
| LIT-006 | Ariza-Garzón et al., *IEEE Access* | 2020 | PEER_REVIEWED | SHAP on P2P granting models |
| LIT-007 | Bussmann et al., *Computational Economics* | 2021 | PEER_REVIEWED | Shapley-based explanations in P2P/SME credit |

Neither paper uses this project’s TRAIN-only EBM or additive closed-form SHAP identity. Do not say they confirm Stage 6 tables.

### 2.4 EBM / GAM in tabular risk

| ID | Source | Year | Type | Support |
| --- | --- | --- | --- | --- |
| LIT-009 | Hastie & Tibshirani, *Statistical Science* | 1986 | PEER_REVIEWED | GAM additive structure |
| LIT-010 | Lou et al., *KDD* | 2013 | PEER_REVIEWED | GA2M pairwise interactions optional |
| LIT-011 | Nori et al., arXiv:1909.09223 | 2019 | PREPRINT | InterpretML EBM as glassbox GAM |

This project froze **`interactions=0`**. Cite Lou for the family, not as evidence that pairwise terms were fitted.

### 2.5 Probability calibration in credit-risk prediction

Yeh & Lien (LIT-004) motivate reporting probabilities. Guo et al. (LIT-017) discuss ECE and post-hoc calibration on **neural image/NLP** models — methodology for ECE language only, **not** a credit result.

Stage 5 numbers remain inventory-only.

### 2.6 Platt scaling / logistic calibration

| ID | Source | Year | Type | Support |
| --- | --- | --- | --- | --- |
| LIT-014 | Platt, *Advances in Large Margin Classifiers* | 1999 | OTHER (book chapter) | Sigmoid map of scores to probabilities |
| LIT-015 | Niculescu-Mizil & Caruana, *ICML* | 2005 | PEER_REVIEWED | Platt vs isotonic |
| LIT-016 | Zadrozny & Elkan, *KDD* | 2002 | PEER_REVIEWED | Isotonic-style calibration of ranking scores |

LIT-014 has **no DOI** and **no official MIT Press URL verified this session**. Identity is supported by the 2005 ICML paper’s reference list (PDF retrieved). Do not invent a DOI.

Platt `a`/`b` in this project come from `platt_record.json`, not from Platt 1999.

### 2.7 Fraud detection in lending / financial services

| ID | Source | Year | Type | Support |
| --- | --- | --- | --- | --- |
| LIT-019 | Bolton & Hand, *Statistical Science* | 2002 | PEER_REVIEWED | Fraud detection is a distinct statistical task (cards, telecom, etc.) |

**Executed fraud study: none.** Literature supports a **negative** paper claim: do not report fraud-detection performance.

### 2.8 Real-time or automated loan decision systems

No production latency/throughput paper was verified this session (gap). What **was** verified:

| ID | Source | Year | Type | Support |
| --- | --- | --- | --- | --- |
| REG-CFPB-1002-9 | 12 CFR 1002.9 | current | AUTHORITATIVE_REGULATORY | Adverse-action notices need specific reasons |
| REG-CFPB-2022-03 | CFPB Circular 2022-03 | 2022 | AUTHORITATIVE_REGULATORY | Black-box models do not waive that duty |
| REG-CFPB-2023-03 | CFPB Circular 2023-03 | 2023 | AUTHORITATIVE_REGULATORY | Sample checklists must match factors actually used |

These are **US creditor** rules. This repository is a research prototype, not an ECOA-regulated originator. Cite as motivation for auditability, not as a compliance result.

### 2.9 Fairness / governance / auditability

| ID | Source | Year | Type | Support |
| --- | --- | --- | --- | --- |
| LIT-008 | Kozodoi, Jacob & Lessmann, *EJOR* | 2022 | PEER_REVIEWED | Fairness criteria in scorecards; profit trade-offs |

This project **did not** run fairness processors. Use only as related-work context.

### 2.10 Islamic finance / Shariah governance

Prefer standards already in `docs/shariah/source_register.json`.

| ID | Instrument | Support | Limit |
| --- | --- | --- | --- |
| SRC-SBP-IFPD-C8-2024 | SBP IFPD Circular 08/2024 | SGF issued for IBIs; effective 2025 | Pakistan IBIs only |
| SRC-SBP-SGF-2025-TEXT | SGF 2025 text | Prior SB approval of products/process flows | PICG-hosted PDF (SBP annex 403) |
| SRC-SECP-SGR-2023-SRO-TEXT | SECP SGR 2023 | Cannot call a security Shariah-compliant without a Commission certificate | Not SBP banks; not US P2P |
| SRC-AAOIFI-SS8/SS9 | AAOIFI SS 8 / 9 | **Identity** of Murabahah and Ijarah standards | Clauses not retrieved |
| SRC-AAOIFI-GS-INDEX | AAOIFI GS listing 2024 | Governance-standard titles exist | Viewer password-protected |
| REG-IFSB-10 | IFSB-10 (2009) | Guiding principles for IIFS Shariah governance systems | FAQ PDF verified; full HTML thin |

### 2.11 Evidence / contractual information for Shariah-oriented products

| ID | Source | Support |
| --- | --- | --- |
| SRC-SBP-IBD-C1-2012 | SBP IBD Circular 01 of 2012 (official HTML retrieved) | Murabaha requires invoices or specified substitute documents (truck receipt, GRN, inspection, etc.) and documented Shariah Advisor approval |

This is the strongest **authoritative** illustration that contract-level evidence is expected in Islamic banking operations and is **absent** from the LendingClub extract. Map to L2 `INSUFFICIENT_INFORMATION` as an **evidence/schema gap**, not a ruling that a loan is non-compliant.

### 2.12 Common credit-risk datasets

| Dataset | Source IDs | In this project? |
| --- | --- | --- |
| LendingClub (Zenodo granting extract) | DS-001; context LIT-005, LIT-006 | **Yes — primary** |
| Taiwan / UCI Default of Credit Card Clients | DS-002; LIT-004 | **Yes — secondary methodology** |
| German Credit (Statlog) | DS-003 | **No — literature only** |
| Australian Credit Approval (Statlog) | DS-004 | **No — literature only** |

XGBoost algorithm: LIT-018 (Chen & Guestrin 2016). Cite as software/method. **Do not** collapse the two XGBoost executions.

---

## 3. Concise source notes (paraphrase only)

**LIT-001.** Public credit-scoring literature treats scorecards as classifiers of good vs bad risk; industry detail is often unpublished.

**LIT-002 / LIT-003.** Comparative studies find both sophisticated and simple classifiers can perform well on credit data; later work updates algorithms and metrics. Not a ranking of this repository’s models.

**LIT-004 / DS-002.** Taiwan credit-card clients (30,000 rows) are a standard PD table; UCI 350 is the repository record. Independent of LC.

**LIT-005 / LIT-006.** P2P Lending Club data appear in RF risk models and SHAP granting-score papers. Those files/pipelines are not this Zenodo extract.

**LIT-007.** Shapley explanations clustered via correlation networks on SME P2P borrowers — different units of analysis.

**LIT-008.** Fair scorecards are an active OR topic. Unused here empirically.

**LIT-009–011.** EBM sits in the GAM/GA2M family. Preprint LIT-011 is software documentation, not a credit TEST.

**LIT-012–013.** SHAP is additive attribution theory. TreeSHAP is for trees; using it as if it explained this EBM would be a method error.

**LIT-014–017.** Post-hoc sigmoid and isotonic maps are standard; ECE is a reliability summary. None of these papers selected Platt on this LC validation Brier.

**LIT-018.** Tree boosting system paper. Not evidence that UCI XGBoost is confirmatory.

**LIT-019.** Fraud vs default are different detection problems.

**Regulatory/standard rows.** Use for governance language and for **prohibiting** certification claims. Never as applicant-level Shariah findings.

---

## 4. Claims literature must not be used to make

- This project’s stored metrics (any ROC-AUC, Brier, counts, hashes).
- UCI validates the LC evidence-separated architecture or Shariah layer.
- XGBoost is the primary validated / best / overall superior model.
- Stage 4B LC XGBoost = Stage 9.4 UCI XGBoost.
- The system is Shariah-compliant, certified, or expert-validated.
- `INSUFFICIENT_INFORMATION` is a religious non-compliance finding.
- Fraud-detection performance.
- Production, real-time, or ECOA-compliant deployment.
- Fairness guarantees (no fairness experiment).
- Causal SHAP.

---

## 5. Residual gaps (do not fill by invention)

1. No 2023–2026 systematic review of ML credit scoring was locked to a verified bibliographic record this session (search error). Related Work may still use 2015–2022 peer-reviewed sources above.
2. No verified paper on **real-time latency** of loan engines; automated-lending coverage is regulatory (CFPB), not systems-performance.
3. AAOIFI operative clauses remain unavailable.
4. IFSB-10 full standard body was not re-parsed from a complete official HTML/PDF this session (FAQ PDF only).
5. Platt 1999 lacks a verified DOI and publisher URL.
6. Zenodo creator names were not retrieved (record fetch timeout).
7. No literature can supply missing Stage 4B joblib SHA-256 or `git_commit`.
8. Expert-validated Shariah mappings do not exist in this repository; literature cannot create them.

These are **documentation/literature gaps**, not licences to invent citations or rerun experiments.

---

## 6. Later insertion rule

When the manuscript Related Work is drafted (separate task):

1. Cite only `SOURCE_ID`s in the register.
2. Copy bibliographic fields from the register; if `DOI_STATUS=UNVERIFIED` or `NONE`, do not fabricate a DOI.
3. Attach the claim-matrix caveat to every sentence.
4. Keep executed-dataset sentences aligned with inventory §2.
5. Run a claim audit against inventory §11 before submission.

---

```text
LITERATURE_REVIEW_STATUS = COMPLETE
SOURCES_VERIFIED = 31
SOURCES_WITH_UNVERIFIED_METADATA = 4
CLAIMS_WITH_DIRECT_SUPPORT = 23
CLAIMS_REQUIRING_MORE_EVIDENCE = 8
INVENTORY_FILES_CREATED = 4
MANUSCRIPT_DRAFTED = NO
EXPERIMENTS_RUN = NO
RESULTS_MODIFIED = NO
```

`SOURCES_WITH_UNVERIFIED_METADATA` = LIT-014 (no DOI/URL), DS-001 (creator names), SRC-AAOIFI-SS9 and SRC-AAOIFI-SS-INDEX (URL not re-fetched this session). Other sources have verified DOI and/or official URL, or are identity-only standards with verified listing/identity URLs.

`COMPLETE` means: all twelve assigned topics have at least one non-invented source and the four package files exist. Residual gaps in §5 remain for a later literature pass if desired. It does **not** mean Related Work is written.
