# Regulatory source authentication and qualified expert-review protocol

**DRAFT PROTOCOL — NO AUTHENTICATED REGULATORY APPLICABILITY OR EXPERT VALIDATION ESTABLISHED**

This document is a research procedure. It is not a regulatory ruling, a Shariah certification, an application-scope approval, or a completed expert-review record. Every template below is empty or marked `NOT_YET_REVIEWED`. No reviewer is named. No source rule is moved to `EXPERT_VALIDATED` or `VERIFIED_IN_SCOPE`.

Prepared during STEP 3B-8A against local snapshot commit `583ad0b30e8007a5f3f0bb13ede7b010fdad5fec`. This file was not staged or committed by that step.

## A. Protocol Purpose and Research Limitations

The purpose is to define an auditable way to obtain regulatory texts, check their bytes and clauses, ask applicability questions, and arrange independent qualified review. The procedure separates five evidence requirements. Completing one requirement leaves the others open.

| ID | Requirement | What a completed record would show | What it leaves open |
| --- | --- | --- | --- |
| A | Authentic document identity | The issuing authority, official identifier, exact title, and publication location of a specific instrument | Whether the stored file is that instrument's bytes |
| B | Integrity of the exact document bytes | A raw-file digest, size, type, retrieval method, and preservation of those bytes | Whether the operative clause and version were read |
| C | Verification of operative clause text and document version | The examined clause, page or paragraph, version, and any amendment or supersession note, tied to the digested bytes | Whether that clause governs a particular institution, product, jurisdiction, and date |
| D | Regulatory applicability | A case-level scope determination for a verified institution, instrument, jurisdiction, and relevant date | Whether the software interpretation of that scope is endorsed |
| E | Independent qualified expert validation | A scoped endorsement of the interpretation and of the software implementation, by reviewers whose qualifications and independence are recorded | Any later change to text, code, evidence schema, or case facts |

A catalog label, a source URL, a stored hash, or a model prediction cannot establish any of these five requirements by itself. A hash can support byte identity against a recorded digest. It does not, by itself, prove official authenticity, clause meaning, applicability, or expert endorsement.

The current engine keeps all six source-specific rules at applicability status `SCOPE_UNKNOWN` under `stage7-applicability-scope-unknown-v1`. This protocol does not change that status. It does not create `VERIFIED_OUT_OF_SCOPE`. Missing evidence stays unresolved.

Public governance statuses in the existing engine remain `PASS`, `REVIEW`, `INSUFFICIENT_INFORMATION`, and `NOT_STRUCTURABLE_WITHOUT_REDESIGN`. Those statuses are research-screen outputs. Under the current scope gate, an applicable diagnostic `PASS` or `NOT_STRUCTURABLE_WITHOUT_REDESIGN` on a source-specific rule is withheld from the public rule result. This protocol does not treat a diagnostic predicate as requirement D or E.

## B. Current Snapshot and Version Baseline

Observed on 2026-10-18 before this document was written:

| Item | Observed value |
| --- | --- |
| Branch | `main` |
| Snapshot commit | `583ad0b30e8007a5f3f0bb13ede7b010fdad5fec` |
| Parent commit | `d49f39a68b740ae464f32f0d7a963b8e7e9938db` |
| Working tree before this file | clean |
| Commit file count | 12 |
| Governance engine in that commit | `stage7-shariah-engine-v2-scope-gated` |
| Applicability layer | `stage7-applicability-scope-unknown-v1` |
| Catalog version constant | `stage7-shariah-catalog-v1` |
| L1/L2 version constant | `stage7-l1l2-v2` |
| Amendment identifier | `AMENDMENT-SHARIAH-001` |
| Source register | `stage7-source-register-v1` |
| Conflict register | `stage7-conflicts-v1` |
| Reserved applicability name | `VERIFIED_IN_SCOPE` is named in code and is not emitted |
| Expert pathway | `trusted_expert_authorization_available()` returns false |
| Frozen decision thresholds | `t_low` 0.06 and `t_high` 0.69, unchanged by this step |

The twelve files in the snapshot are the five governance modules `src/shariah/engine.py`, `rules.py`, `evidence.py`, `schema.py`, and `applicability.py`; the six test modules named in the snapshot; and `docs/reproducibility/ENGINE_V2_FREEZE_CANDIDATE.md`. Historical Stage 7 and Stage 8 artifacts remain associated with governance engine `stage7-shariah-engine-v1`. This protocol does not relabel them.

The snapshot commit records software safety behavior. It is not a publication release and not an expert-validation record.

## C. Six-Rule Regulatory Source Inventory

Associations below were read from `docs/shariah/rule_catalog.json` at the snapshot baseline. Catalog `clause_verified: true` and `validation_status: SOURCE_VERIFIED_PENDING_EXPERT_REVIEW` are catalog fields. They do not complete requirements A through E. Each rule has `expert_validation_record: null`.

The diagnostic evaluator is the function in `src/shariah/rules.py`. The public source-rule result is then passed through `gate_source_rule` in `src/shariah/applicability.py`.

### C.1 `SH-SBP-SGF-002`

| Field | Catalog and code record |
| --- | --- |
| Source ID | `SRC-SBP-SGF-2025-TEXT` |
| Declared section | 3.B.ii |
| Declared document | Shariah Governance Framework for Islamic Banking Institutions (Effective from: January 01, 2025) |
| Catalog URL | PICG-hosted PDF `https://picg.org.pk/wp-content/uploads/2025/03/Shariah-Governance-Framework-for-Islamic-Banking-Institutions.pdf` |
| Catalog statement | All products or services to be offered and/or launched by the IBI shall have prior approval of the SB. |
| Interpretation note | Pakistani IBI product-governance prerequisite. The catalog says this is not a global fatwa and not a certification of Murabahah or Ijarah substance. |
| Diagnostic evaluator | `eval_sb_prior_approval` |
| Diagnostic behavior | Skip unless `institution_class` is `IBI` and the contract type is outside `{unknown, ambiguous, conventional_credit}`. Missing approval is `INSUFFICIENT_INFORMATION`. Exact Boolean false is `NOT_STRUCTURABLE_WITHOUT_REDESIGN`. A non-Boolean supplied value is `REVIEW`. Exact Boolean true is diagnostic `PASS`, with a reason that states it is not a certification. |
| Unresolved prerequisites | Authenticated primary SGF bytes; definition of IBI, SB, product, and service; effective date and any transitional rule; case execution date; qualified review of the Boolean mapping. |

### C.2 `SH-SBP-SGF-003`

| Field | Catalog and code record |
| --- | --- |
| Source ID | `SRC-SBP-SGF-2025-TEXT` |
| Declared section | 3.B.iii |
| Catalog statement | The SB shall review and approve procedure manuals, product programs/structures, process flows, related agreements, and broader sales and marketing parameters so that they conform with the rules and principles of Shariah. |
| Interpretation note | Operationalised as a binary evidence flag. The engine does not inspect legal drafting. |
| Diagnostic evaluator | `eval_sb_docs_approval` |
| Diagnostic behavior | Same institution and contract skip as `SH-SBP-SGF-002`, applied to `sb_approved_agreements_and_process_flows`. |
| Unresolved prerequisites | Same primary-text and definition gaps as C.1, plus review of whether one Boolean can represent manuals, programs, process flows, agreements, and sales parameters. |

### C.3 `SH-SBP-MUR-INV-001`

| Field | Catalog and code record |
| --- | --- |
| Source ID | `SRC-SBP-IBD-C1-2012` |
| Declared section | Circular body, paragraph 1 |
| Declared document | IBD Circular No. 01 of 2012: Invoice of Murabaha Transactions |
| Catalog URL | `https://www.sbp.org.pk/ibd/2012/C1.htm` |
| Catalog statement | The supplier invoice shall be in the name of Bank-Account Client. A client-name invoice may be acceptable, subject to specific Shariah Advisor approval, where an IBI-name invoice is not possible. |
| Interpretation note | Pakistani IBI Murabaha. The catalog says it is not applied to Ijarah or LendingClub purpose codes. |
| Diagnostic evaluator | `eval_murabaha_invoice` |
| Diagnostic behavior | Skip unless contract type is `Murabahah` and institution class is `IBI`. `bank_account_client` is diagnostic `PASS`. `client_only` depends on an exact Boolean Shariah Advisor flag. `no_formal_invoice` skips this rule. Other strings are `REVIEW`. Page in the catalog is `NOT_VERIFIED`. |
| Unresolved prerequisites | Digested official circular bytes; the cited 2008 Essentials annex; any later amendment; definitions of IBI, Murabaha, and Shariah Advisor; case documents that would support the invoice-status string. |

### C.4 `SH-SBP-MUR-INV-002`

| Field | Catalog and code record |
| --- | --- |
| Source ID | `SRC-SBP-IBD-C1-2012` |
| Declared section | Circular body, paragraph 2 |
| Catalog statement | Where no formal invoice in the bank's or client's name is possible, listed alternative documents may be accepted in lieu of an invoice with Shariah Advisor approval. |
| Interpretation note | The engine tests presence of alternative documents plus Advisor approval. It does not test the listed particulars. |
| Diagnostic evaluator | `eval_murabaha_alt_docs` |
| Diagnostic behavior | Engaged only for IBI Murabahah with `invoice_name_status` equal to `no_formal_invoice`. Both flags must be exact Boolean true for diagnostic `PASS`. Missing evidence is `INSUFFICIENT_INFORMATION`. Exact false is `NOT_STRUCTURABLE_WITHOUT_REDESIGN`. A non-Boolean value is `REVIEW`. |
| Unresolved prerequisites | Same circular-byte gap as C.3, plus review of whether a presence flag covers the circular's required particulars. |

### C.5 `SH-SBP-MUR-PAY-001`

| Field | Catalog and code record |
| --- | --- |
| Source ID | `SRC-SBP-IBD-C1-2012` |
| Declared section | Circular body, paragraph 4 |
| Catalog statement | Payment shall be made directly to the supplier or credited to an escrow account. Payment through an agent is described for genuine reasons, with recorded reasons and Shariah Advisor approval of the process flow. |
| Interpretation note | Payment to the customer is treated in the catalog as outside the permitted channels. The catalog says this is a Pakistani IBI Murabaha operational mapping and not an AAOIFI SS (8) clause. |
| Diagnostic evaluator | `eval_murabaha_payment` |
| Diagnostic behavior | `supplier` and `escrow` are diagnostic `PASS`. `agent` requires two exact Boolean flags. `customer` is diagnostic `NOT_STRUCTURABLE_WITHOUT_REDESIGN`. Unknown is `INSUFFICIENT_INFORMATION`. Other strings are `REVIEW`. |
| Unresolved prerequisites | Same circular-byte and supersession gaps as C.3, plus review of whether the customer-channel hard stop is the operative reading of paragraph 4. |

### C.6 `SH-SECP-SGR-SEC-001`

| Field | Catalog and code record |
| --- | --- |
| Source ID | `SRC-SECP-SGR-2023-SRO-TEXT` |
| Declared section | Regulation 7(2) |
| Declared document | Shariah Governance Regulations, 2023, S.R.O. 1314 (I)/2023 |
| Catalog URL | MUFAP-hosted PDF `https://www.mufap.com.pk/Upload/WebDoc/Regulations/Shariah-Governance-Regulations-20231177.pdf` |
| Catalog statement | No security shall be called a Shariah compliant security unless a Shariah compliance certificate has been granted by the Commission under these regulations. |
| Interpretation note | The catalog limits the mapping to a Shariah-compliant-security claim under the SECP company and security regime, and says it does not classify LendingClub loans. |
| Diagnostic evaluator | `eval_secp_security_claim` |
| Diagnostic behavior | A non-Boolean claim raises `ValueError` before the IBI skip. IBI inputs skip. `None` skips as claim information not provided. Exact false skips as no claim. Exact true runs the certificate state machine: missing certificate is `INSUFFICIENT_INFORMATION`; exact false is `NOT_STRUCTURABLE_WITHOUT_REDESIGN`; non-Boolean certificate is `REVIEW`; exact true is diagnostic `PASS`, with a reason that it is not a ruling by this engine. |
| Unresolved prerequisites | Official SRO bytes; definition of security; institutional category; certificate grant and verification procedure; exclusions, including the banking-company exclusion used by the skip; amendments after the cited SRO. |

### C.7 Additional instruments the register does not authenticate

The register already names related instruments. Their presence as identity rows does not close the six rules. A future acquisition step still needs to search for instruments the register may omit. The following are required before applicability can be considered, and this list is an evidence gap, not a finding that any instrument applies:

| Needed instrument | Why it is in scope for a future search | Current register state |
| --- | --- | --- |
| Official SBP IFPD Circular No. 08 of 2024, including any annex pointer | The SGF text is described as issued under this circular, effective 1 January 2025 | `SRC-SBP-IFPD-C8-2024` says official HTML was retrieved. `sha256` is null. The annex PDF is recorded as HTTP 403 from `sbp.org.pk`. |
| Official SBP SGF booklet bytes | Rules C.1 and C.2 cite sections 3.B.ii and 3.B.iii | `SRC-SBP-SGF-2025-TEXT` points at a PICG URL and a PICG digest. Official SBP bytes are absent. |
| SGF definitions, commencement, repeal, and transitional provisions | Institutional class and effective date cannot be inferred from sections 3.B.ii and 3.B.iii alone | Not separately digested. This step did not extract those clauses from the local PDF. |
| Official IBD Circular No. 01 of 2012 bytes | Rules C.3 through C.5 cite paragraphs 1, 2, and 4 | `SRC-SBP-IBD-C1-2012` URL is the SBP HTML page. `sha256` is null. Page is `NOT_VERIFIED`. |
| IBD Circular No. 02 of 2008 and its Murabaha Essentials annex | Circular 01 of 2012 cites Annexure-1, Appendix-A, Murabaha sub-clause vi | `SRC-SBP-IBD-C2-2008-IDENTITY` is `IDENTITY_VERIFIED_CLAUSES_NOT_VERIFIED`. The annex PDF is recorded as not retrieved. |
| IBD Circular No. 04 of 2008 | The 2012 register note says Circular 01 of 2012 repeals it | No separate source row and no digest. |
| Later SBP instruments that amend, exempt, or supersede the 2012 invoice and payment instructions or the 2025 SGF | Supersession cannot be assumed from the absence of a row | Not established. A future search is required. |
| Official SECP SGR 2023 PDF and the Gazette copy of S.R.O. 1314 (I)/2023 | Rule C.6 cites Regulation 7(2) | `SRC-SECP-SGR-2023-PAGE` records the official landing page and HTTP 403 for the official PDF. `sha256` is null. The mapped text is the MUFAP copy. |
| SGR definitions, application provision, certificate procedure, and exclusions | The security-claim rule depends on what a security is, who the Commission is, and which institutions are excluded | The register cites Regulation 1, Regulation 2(1)(d), and Regulation 7(2) from the hosted PDF. Those clauses were not re-read from bytes in this step. |
| Companies Act, 2017, section 451, and the statutory definition of security relied on by the SGR | The register scope text refers to declarations of Shariah-compliant companies and securities | No digested statutory source row. |
| Any SECP amendment, exemption, or repeal after 14 September 2023 | The cited publication date does not prove the text is still operative for a later case | Not established. |
| AAOIFI SS (8) and SS (9) licensed operative text, with revision history | Murabahah and Ijarah identity gates refuse to invent clauses. Structural rules such as possession remain unimplemented | Identity rows only. `sha256` is null. See section G of the AAOIFI boundary below. |

`docs/shariah/conflicts.json` records three research conflicts: AAOIFI SS (8) identity versus the 2012 SBP operational circular, unresolved; SECP versus SBP scope, marked resolved by scope inside the research register; and the unretrieved 2008 Essentials versus the 2012 circular, marked resolved only for retrieved 2012 paragraphs. Those conflict labels are research bookkeeping. They are not requirement D.

## D. Existing Source-Evidence Status

### D.1 Fresh hash check of local copies

On 2026-10-18 the following gitignored files were present and were hashed with SHA-256 in this step. No PDF was downloaded. No historical file was replaced.

| Local path | Size (bytes) | SHA-256 recomputed in this step | Comparison with `docs/shariah/source_register.json` |
| --- | --- | --- | --- |
| `audit/source_downloads/picg_sgf_2025.pdf` | 1194719 | `6c32d43d528104271bccd2dd228ba8ca33e94abe459494c6d4abdae41ef06ca1` | Equal to the digest stored on `SRC-SBP-SGF-2025-TEXT` |
| `audit/source_downloads/mufap_sgr2023.pdf` | 617755 | `7ffe4179154a793da18cfb1e783a32bf74408bea7513dffbf2b42b67f4929ba7` | Equal to the digest stored on `SRC-SECP-SGR-2023-SRO-TEXT` |
| `audit/source_downloads/baf_sgf.pdf` | 1328390 | `becd6b94ae3e0be1f30c482b1ad8b7158870c424963aa107a27a2763d46c09a8` | Not equal to the registered SGF digest. The register has no row for this file. |

Hash equality supports byte identity between the local PICG file and the digest recorded for `SRC-SBP-SGF-2025-TEXT`, and between the local MUFAP file and the digest recorded for `SRC-SECP-SGR-2023-SRO-TEXT`. It does not independently prove that either file is an official SBP or SECP instrument.

A different hash on `baf_sgf.pdf` requires investigation before anyone uses that file as a source. Difference of size and digest is not, by itself, a finding of fraud, alteration, or error. This step did not extract or compare clause text inside `baf_sgf.pdf`. The file is an extra local copy. It is outside the snapshot and outside the source register.

### D.2 PICG-hosted SBP SGF 2025 copy

The register describes this file as a public republication whose title page is said to identify the State Bank of Pakistan, Islamic Finance Policy Department, effective 1 January 2025. The registered URL is on `picg.org.pk`, not on `sbp.org.pk`. The register states that the official annex PDF returned HTTP 403 in the earlier environment. This step did not repeat that download and did not open the PDF to re-verify the title page.

Limits that remain:

- The file is a third-party-hosted copy.
- Domain appearance of the URL, and a successful earlier download, do not complete requirement A.
- The matching digest completes a byte-identity check against the register only.
- Official SBP bytes, retrieval logs, and a clause-level re-read are absent.
- Definitions, repeal, and transitional clauses were not authenticated here.

### D.3 MUFAP-hosted SECP SGR 2023 copy

The register describes this file as an industry-association hosting of S.R.O. 1314 (I)/2023. The registered URL is on `mufap.com.pk`. The official SECP document page is a separate identity row, and the register states that the official PDF returned HTTP 403. This step did not repeat that download and did not re-read Regulation 7(2) from the PDF.

Limits that remain:

- The file is a third-party-hosted copy.
- The matching digest completes a byte-identity check against the register only.
- Gazette publication, official SECP bytes, and the certificate-grant procedure were not authenticated here.
- The banking-company exclusion used by the software skip was not re-established from official bytes in this step.

### D.4 Register labels

Several rows use `verification_status: SOURCE_VERIFIED`. In this protocol that historical label means the earlier study recorded a retrieval note. It does not mean requirements A through E are complete. Rows with `sha256: null` have no registered raw-byte digest. That includes the official SBP circular HTML pages and all AAOIFI identity rows.

### D.5 AAOIFI evidence boundary

| Layer | SS (8) Murabahah | SS (9) Ijarah and Ijarah Muntahia Bittamleek |
| --- | --- | --- |
| Standard identity | `SRC-AAOIFI-SS8-IDENTITY` and `SRC-AAOIFI-SS-INDEX`. Status `IDENTITY_VERIFIED_CLAUSES_NOT_VERIFIED`. Title recorded from AAOIFI pages accessed 2026-09-15. | `SRC-AAOIFI-SS9-IDENTITY` and the same index. Same status. |
| Operative clause text | Not obtained. Register note: copyrighted body and password-protected viewer. `sha256` null. | Not obtained. `sha256` null. |
| Contract-specific rule extraction | `SH-AAOIFI-SS8-POSSESSION` is `executable: false`, version `0.0.0-not-implemented`, clause `NOT_VERIFIED`. | No executable SS (9) structural rule. |
| Software behavior | `SH-AAOIFI-SS8-GATE` returns `INSUFFICIENT_INFORMATION` for a Murabahah identification and skips otherwise. | `SH-AAOIFI-SS9-GATE` returns `INSUFFICIENT_INFORMATION` for `Ijarah` or `Ijarah_Muntahia_Bittamleek` and skips otherwise. |
| Qualified expert interpretation | No expert record. | No expert record. |

The identity gates do not implement operative AAOIFI rulings. A standard title is not clause text. Future acquisition must respect access control, copyright, and any licence or permission required to store and quote operative text. This protocol does not propose bypassing a password-protected viewer. If a licensed copy is later obtained, its bytes, licence scope, and quotation limits must be recorded outside the historical identity rows, without overwriting those rows.

## E. Primary-Source Retrieval and Authentication Procedure

This section is the future workflow. STEP 3B-8A does not perform it. Downloads of new or access-controlled documents require a separately supervised evidence-acquisition step.

For each primary source, the future evidence package records the fields below. Empty values stay empty until that step. A downloaded file on an official-looking domain is a candidate artifact. It becomes an authenticated official instrument only after requirement A and the authenticity evidence below are completed by the source-provenance verifier.

| Field | Record |
| --- | --- |
| Package ID | `NOT_YET_REVIEWED` |
| Issuing authority | |
| Official document identifier | |
| Exact title | |
| Official publication location | |
| Original URL | |
| Resolved retrieval URL | |
| Retrieval date and UTC time | |
| Retrieval method | |
| HTTP status and redirect chain | |
| Raw-file SHA-256 | |
| File size and type | |
| Document language | |
| Publication date | |
| Claimed effective date | |
| Claimed amendment or supersession history | |
| Document authenticity evidence | |
| Availability of operative clause text | |
| Differences from previously collected third-party copies | |
| Verification performer role | Source-provenance verifier |
| Approval state | `NOT_YET_REVIEWED` |

Preservation rules:

1. Store the raw response bytes before any conversion, OCR, text extraction, or PDF normalization.
2. Record each transformation as a separate derivative with its own digest and a link to the raw digest.
3. Never replace `picg_sgf_2025.pdf`, `mufap_sgr2023.pdf`, `baf_sgf.pdf`, or any historical digest.
4. A newly retrieved official file is stored under a new path. Comparison against a third-party copy is a difference record, not an overwrite.
5. If retrieval fails, record the UTC time, URL, status, and headers that are safe to retain. Failure leaves the related rules at `SCOPE_UNKNOWN`.
6. HTML pages and PDF annexes are separate byte objects. A hash of one is not a hash of the other.

Official-domain retrieval and independent authentication remain separate. The authenticity evidence may include, when available, gazette publication, an authority checksum or signature, a stable official record identifier, and agreement between the official landing page and the retrieved file. The protocol does not prescribe a single technical test as sufficient for every instrument.

## F. Clause and Version Verification Method

After raw bytes exist, a clause verification record is created per cited passage. The verifier works from the digested file, not from the catalog sentence alone.

| Field | Record |
| --- | --- |
| Clause record ID | `NOT_YET_REVIEWED` |
| Raw-file SHA-256 being read | |
| Document version and date examined | |
| Section, regulation, paragraph, and page | |
| Quotation or authenticated excerpt locator | |
| Text normalization, if any, and its derivative digest | |
| Comparison with the catalog `source_statement` | `NOT_YET_REVIEWED` |
| Definitions incorporated by reference | |
| Effective date and transitional text found in the same instrument | |
| Amendment, repeal, exemption, or supersession found | |
| Clause-verification state | `NOT_YET_REVIEWED` |

A catalog sentence may be confirmed, narrowed, or left unmatched. Until the state is an accepted clause verification, `clause_verified: true` in the catalog remains a historical catalog flag.

Version verification includes a search for later instruments. The search log is part of the record even when no later instrument is found. "No row in the current register" is not a completed supersession search.

## G. Independent Regulatory and Shariah Review Roles

Roles are competencies. One person may hold more than one competency only when each competency and its review scope are explicitly established. This draft names no person and stores no credential, signature, or contact detail.

| Role | Competence that must be established | Scope of this protocol | Outside this role's sole authority |
| --- | --- | --- | --- |
| Source-provenance verifier | Documentary retrieval, digest, and official-publication checks | Requirements A and B, and custody of raw bytes | Applicability and religious interpretation |
| Regulatory applicability reviewer | Relevant jurisdictional and institutional expertise for the cited regime | Requirement D for the assigned instrument family | Shariah certification and software release |
| Qualified Shariah reviewer | Qualification to interpret the cited governance or transactional question, established externally | Requirement E for interpretation of the examined clauses | Byte authentication and a claim that software output is a fatwa |
| Independent software implementation auditor | Ability to read the deterministic evaluator, tests, and evidence schema | Whether the code implements the reviewed interpretation and preserves diagnostic, applicability, public, and fusion boundaries | Source authenticity and legal scope |

Independence and conflict controls:

- Each role files a conflict-of-interest declaration in the external record. Employment by an issuing authority, a supervised institution, or this research project is disclosed. Disclosure does not by itself disqualify or qualify the reviewer.
- The software auditor is independent of the author of the evaluator under review. If that separation is unavailable, the record states the overlap and the review remains `NOT_YET_REVIEWED` for release purposes.
- Qualifications are described by role, jurisdiction, and date of establishment. Copies of identity documents and credentials stay in secure external retention. The repository stores an auditable reference such as an external record ID, a digest of the external packet, and the retention location class. It does not store the packet.
- No reviewer name is invented to fill a template.

Review method, for a future engaged review:

1. The reviewer receives the raw-file digest, the clause record, the rule identifier, the evaluator source, and the current tests.
2. The reviewer examines only the listed clauses and states interpretation limits.
3. The endorsement names its scope: document family, clauses, software version, and evidence-schema version.
4. Disagreement is recorded as a dissent or as `NOT_YET_REVIEWED`. It is not averaged into `EXPERT_VALIDATED`.
5. Sign-off is an external signature or equivalent provenance event. The repository stores the reference and digest.
6. Any change to cited text, evaluator logic, evidence schema, thresholds, or catalog validation status requires renewed review of the affected scope.

## H. Rule-Specific Applicability Questions

These questions are for future reviewers. This document does not answer them. A string such as `PK`, `IBI`, or `secp_ifi` is not an answer.

### H.1 SBP Shariah Governance Framework family

Applies to the future review of `SH-SBP-SGF-002` and `SH-SBP-SGF-003`.

1. Which legal classification does the cited text use for the institution it governs, and what evidence would verify that classification for a named institution?
2. What jurisdictional connection does the instrument require?
3. What definitions of product, service, offer, and launch does the text use?
4. Which contractual or operational events make section 3.B.ii or 3.B.iii relevant?
5. Do sections 3.B.ii and 3.B.iii operate alone, or do they incorporate definitions, responsibilities, or exceptions elsewhere in the same booklet or in IFPD Circular No. 08 of 2024?
6. What commencement, transitional, and repeal provisions govern a case dated before, on, or after 1 January 2025?
7. Which later circulars, exemptions, or superseding frameworks exist, and which cases do they reach?
8. What evidence would support a scope determination for one institution and one product?
9. Which institutions, products, or arrangements does the text expressly place outside this framework?
10. Which of the above remains uncertain after the authenticated text is read?

The Boolean flags `sb_prior_product_approval` and `sb_approved_agreements_and_process_flows` are software inputs. Whether those inputs are adequate evidence of Shariah Board approval is itself a review question.

### H.2 SBP Murabahah invoice and payment family

Applies to `SH-SBP-MUR-INV-001`, `SH-SBP-MUR-INV-002`, and `SH-SBP-MUR-PAY-001`.

1. Does IBD Circular No. 01 of 2012 govern the verified legal classification of the institution in the case?
2. What jurisdictional connection and Murabahah definition does the circular require?
3. Which events matter: invoice issuance, purchase, payment, agency, or a later financing drawdown?
4. Are paragraphs 1, 2, and 4 still operative, and do they incorporate the 2008 Essentials text they cite?
5. What is the operative relationship between Circular No. 02 of 2008, Circular No. 04 of 2008, and Circular No. 01 of 2012?
6. Which later amendments, exemptions, or product instructions supersede these paragraphs for the case date?
7. What documentary evidence would support `invoice_name_status`, alternative-document presence, payment channel, and Shariah Advisor approval?
8. Does the circular treat payment to the customer as a prohibited channel, or is that a software mapping that still needs interpretation?
9. Which transactions does the circular expressly decline to cover?
10. What remains uncertain, including any clause that cannot be read because the 2008 annex is absent?

### H.3 SECP security-claim family

Applies to `SH-SECP-SGR-SEC-001`.

1. What definition of security does the authenticated SRO and its parent statute use?
2. What institutional category does the regulation govern, and how is an SBP-regulated banking company identified and excluded?
3. What does the Commission-issued Shariah compliance certificate consist of, who may rely on it, and how is a specific certificate verified?
4. Does Regulation 7(2) apply only when a person calls a security Shariah compliant, and what conduct counts as that call?
5. Which jurisdictional connection brings an issuer, a security, or a statement within the regulation?
6. What effective date and transitional provisions apply to S.R.O. 1314 (I)/2023?
7. Which amendments, repeals, exemptions, or later regulations supersede Regulation 7(2)?
8. What evidence would show that a particular instrument is a security, that a particular entity is in the regulated category, and that a particular certificate was granted under these regulations?
9. Which claims, institutions, and products does the text expressly exclude?
10. What remains uncertain if the official PDF and the Gazette copy are unavailable or disagree with the MUFAP-hosted file?

The software skip for `institution_class == "IBI"` and the skip for a false or missing claim are implementation choices. They are questions for the applicability reviewer, not completed exclusions.

## I. Contract-Level Evidence Requirements

`FinancingEvidence` in `src/shariah/schema.py` currently stores:

- `case_id`, `synthetic`
- `contract_type`, `institution_class`, `jurisdiction`, `instrument_type` as strings
- Boolean or null operational flags for board approval, invoice exception, alternative documents, payment-channel companions, security claim, and certificate
- string invoice status and payment channel
- structural fields that the AAOIFI gates do not use as clause tests: underlying asset, possession, late-payment treatment, contractual sequence
- an `extra` dictionary

The schema has no contract execution date, no transaction or event date, no verified legal-entity record, no attached authentic document, and no source-version applicability field.

The timestamp accepted by `evaluate()` is an audit clock. `applicability.py` records `contract_date_status` as `CONTRACT_DATE_NOT_IN_SCHEMA` and states that the audit timestamp is not a contract execution date. A future reviewer must keep that distinction.

A future evidence-schema change, not implemented here, would need at least:

| Proposed future field | Purpose | Constraint |
| --- | --- | --- |
| `contract_execution_date` | Date the reviewed agreement was executed, with calendar and source | Distinct from the audit timestamp |
| `relevant_event_date` | Date of offer, launch, invoice, payment, or claim, as specified by the reviewer | One field may be insufficient if several events matter; the design must say which event controls |
| `institution_identity_ref` | External reference to a verified legal entity | A string `IBI` is not that verification |
| `legal_classification_record_ref` | External applicability memo for the institution | Digest and reviewer reference required |
| `instrument_classification_record_ref` | External memo for the product or security | Separate from `contract_type` |
| `jurisdictional_nexus_record_ref` | External memo for the connection the instrument requires | Separate from a jurisdiction string such as `PK` |
| `source_version_applicability_ref` | Authenticated instrument version found to govern the case date | Includes supersession search |
| `authentic_document_refs` | Digests of case documents actually reviewed | Presence flags remain diagnostic inputs until a reviewer accepts them |

The future applicability decision must be derived from those authenticated records and from the case evidence. It must not be derived from the bare strings `PK` or `IBI`.

## J. Reviewer Evidence Record Template

All fields below are blank or `NOT_YET_REVIEWED`. This template is not an example of a successful review.

```text
record_status: NOT_YET_REVIEWED
external_record_id:
external_retention_class:
external_packet_sha256:
repository_reference_only: true

reviewer_role:
qualification_established: NOT_YET_REVIEWED
independence_established: NOT_YET_REVIEWED
conflict_of_interest_declaration: NOT_YET_REVIEWED
identity_documents_in_repository: false

documents_and_versions_reviewed: []
raw_file_sha256: []
clauses_examined: []
software_commit:
evaluator_names: []
evidence_schema_version:

methodology: NOT_YET_REVIEWED
interpretation_limitations: NOT_YET_REVIEWED
scope_of_endorsement: NOT_YET_REVIEWED
review_date:
dissent_or_disagreement: NOT_YET_REVIEWED
sign_off_provenance: NOT_YET_REVIEWED
renewed_review_triggers_acknowledged: NOT_YET_REVIEWED
```

Personal names, credential images, signatures, and contact details belong in the external packet. They are not default repository content.

## K. Conflict, Amendment, and Supersession Handling

1. A research conflict row in `conflicts.json` can identify a question. It cannot close requirement C or D.
2. When two digested texts address the same transaction, the reviewer records both, the dates, and the unresolved difference. The software continues to withhold authoritative public results while applicability is `SCOPE_UNKNOWN`.
3. An amendment or repeal is effective for the protocol only when its own bytes and commencement text have passed requirements A through C.
4. A later instrument that is found, but not yet digested, blocks an applicability acceptance for cases that might fall under it.
5. Third-party copies are identified separately from official primary texts in every difference table.
6. `baf_sgf.pdf` stays an unidentified extra copy until a provenance package explains its origin and its byte difference from the PICG file and from any future official SBP file.
7. Supersession of historical experiment outputs is out of scope. Historical audits stay engine v1. A future governance change is a new software version with its own tests.

## L. Evidence Acceptance and Rejection Gates

Each gate can fail or remain unresolved without implying a legal exclusion. Failure and unresolved results keep the six source rules at `SCOPE_UNKNOWN`. They never produce `VERIFIED_OUT_OF_SCOPE`. A synthetic catalog record, including a forged `EXPERT_VALIDATED` label or a nonempty expert-record string, is not acceptance at any gate. The current engine already refuses those inputs as verification.

| Gate | Entry | Required documents | Responsible role | Acceptance criteria | Failure or unresolved outcome | Audit evidence | Renewed review when |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G0 Snapshot baseline | This protocol is approved for use as a procedure | Snapshot `583ad0b` and this draft's digest | Research supervisor | The draft matches the inventory in section C and changes no code | Stop. No acquisition | Supervisor note, external | The engine, catalog, or register changes before acquisition |
| G1 Document identity | G0 accepted | Official identifier, title, publication location | Source-provenance verifier | Identifier and title match the issuing authority's publication record | `NOT_YET_REVIEWED`. Rule stays `SCOPE_UNKNOWN` | Identity worksheet | The identifier, title, or publication location is corrected |
| G2 Byte integrity | G1 accepted | Raw file, retrieval log, SHA-256, size, type | Source-provenance verifier | Digest is computed on preserved raw bytes and the retrieval log is complete | Do not repair a hash by editing history. Store the new file separately | Raw file and retrieval log | The file is re-fetched or transformed |
| G3 Clause and version | G2 accepted | Digested file and clause record | Source-provenance verifier, then regulatory applicability reviewer for the legal effect of the clause | Cited passage is located in that digest, with version and supersession search logged | Catalog text remains unverified for release | Clause record | A later instrument or a text difference appears |
| G4 Applicability questionnaire | G3 accepted | Section H answers tied to one institution, product, jurisdiction, and date | Regulatory applicability reviewer | Each question is answered from the authenticated text and case evidence, or explicitly left uncertain | Uncertain questions block acceptance. They do not become an out-of-scope finding | Applicability memo, external | Institution, product, date, or text changes |
| G5 Interpretation | G4 accepted for the endorsed scope | Clause record and interpretation memo | Qualified Shariah reviewer | Endorsement states limits and the exact clauses | Dissent leaves the rule `NOT_YET_REVIEWED` | External sign-off reference and packet digest | Interpretation or clause set changes |
| G6 Implementation audit | G5 accepted | Evaluator, tests, schema, and the endorsed memo | Independent software implementation auditor | Code and tests match the endorsed interpretation and keep diagnostic results separate from public scope | No code change is released | Audit note against a commit | Any commit touching the endorsed evaluator, schema, catalog status, or thresholds |
| G7 Supervisor release | G6 accepted | Full packet digest and a proposed patch | Research supervisor | A separate authorization exists for schema design, source verification, and regression tests | The engine pathway stays closed | Authorization record | Any item in G1–G6 is renewed |

A synthetic fixture can test software behavior. It cannot satisfy G4 or G5.

## M. Current Blockers and Evidence Still Needed

The following blockers are sufficient to keep every source rule at `SCOPE_UNKNOWN`:

- No official SBP SGF annex bytes. The local PICG file matches the registered third-party digest only.
- No digested official copy of IFPD Circular No. 08 of 2024. The register hash is null.
- No digested official bytes for IBD Circular No. 01 of 2012. The register hash is null.
- The 2008 Essentials annex cited by that circular was not retrieved.
- No official SECP or Gazette bytes for S.R.O. 1314 (I)/2023. The local MUFAP file matches the registered third-party digest only.
- `baf_sgf.pdf` has a different size and digest and has no register row.
- AAOIFI SS (8) and SS (9) operative clauses are not in the repository.
- No contract execution date exists in `FinancingEvidence`.
- No external reviewer packet, qualification record, or sign-off exists.
- Catalog validation status remains `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW` with null expert records.
- The applicability layer still reports `source_text_authenticated: false`, `expert_metadata_authenticated: false`, and `source_digest_verified: false`.

## N. Manuscript Claim Boundary

These layers are different claims:

| Layer | Current basis | Boundary |
| --- | --- | --- |
| Reproducible software behavior | Snapshot `583ad0b` and the passing safety tests recorded in the freeze candidate | Describes the research screen at that commit |
| Stored historical ML performance | Frozen Stage 4B, Stage 5, and Stage 8 artifacts | Unchanged by governance source work |
| Document provenance | Register rows, local third-party PDFs, and the fresh digests in section D | Byte identity against a register digest where the hashes match |
| Verified source applicability | Not established | Questions in section H are unanswered |
| Expert-validated interpretation | Not established | Templates in section J are `NOT_YET_REVIEWED` |
| Real-world compliance | Not established | The engine is not a ruling authority |

The manuscript files `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex`, `docs/paper/IEEE_MANUSCRIPT.md`, and `docs/paper/MANUSCRIPT_DRAFT.md` contain a table row labeled "Verified source / provenance" for SBP SGF 2025, IBD Circular 01 of 2012, SECP SGR 2023, and AAOIFI identity citations. That phrase needs qualified wording unless a future evidence package actually completes the verification those words convey. The same manuscripts also state that source-mapped rules are `SOURCE_VERIFIED_PENDING_EXPERT_REVIEW` and that AAOIFI material is identity only. This step does not edit the manuscript.

This protocol does not claim IEEE Access acceptance, formal Shariah approval, or regulatory endorsement.

## O. Future Supervised Implementation Sequence

A reviewed record may be considered for implementation only after all of the following exist:

1. Supervisor approval of this protocol as the procedure to use.
2. A separate supervised acquisition step that stores new raw bytes without overwriting historical files.
3. Completed G1 through G6 records for the specific rule being considered.
4. A schema design review for the fields in section I.
5. Regression tests that still expect `SCOPE_UNKNOWN` for every source rule that lacks a completed packet.
6. A further supervisor authorization before any code path can emit a status other than `SCOPE_UNKNOWN`.

No positive applicability pathway is implemented by this document. `VERIFIED_IN_SCOPE` stays reserved and unemitted. `trusted_expert_authorization_available()` stays false until a later authorized change.

## P. Completion Checklist

This checklist records the draft state of STEP 3B-8A. It does not mark any evidence gate as passed.

- [x] Snapshot baseline matched `583ad0b30e8007a5f3f0bb13ede7b010fdad5fec` on `main` with parent `d49f39a68b740ae464f32f0d7a963b8e7e9938db` before this file was created.
- [x] Six catalog source associations were read from `rule_catalog.json`.
- [x] Local PICG, MUFAP, and `baf_sgf.pdf` bytes were hashed in this step.
- [ ] Official primary bytes acquired under a separate supervised step.
- [ ] Clause and version verification completed.
- [ ] Applicability questionnaires answered by a qualified reviewer.
- [ ] External reviewer packet created.
- [ ] Software implementation audit against an endorsed interpretation.
- [ ] Evidence schema change designed and separately authorized.
- [ ] Any future engine change authorized, implemented, and regression-tested.
- [ ] Manuscript wording reviewed in a separate writing step.

`record_status: NOT_YET_REVIEWED`

**DRAFT PROTOCOL — NO AUTHENTICATED REGULATORY APPLICABILITY OR EXPERT VALIDATION ESTABLISHED**
