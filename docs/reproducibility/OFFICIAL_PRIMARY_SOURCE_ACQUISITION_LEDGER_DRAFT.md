# Official primary-source acquisition ledger

**DRAFT EVIDENCE LEDGER — SOURCE ACQUISITION ONLY; NO REGULATORY APPLICABILITY OR EXPERT VALIDATION ESTABLISHED**

This ledger records one public retrieval attempt on 2026-10-18. It is not an authenticity determination, an applicability decision, or an expert attestation. No instrument is marked `AUTHENTICATED`. No rule is marked `VERIFIED_IN_SCOPE` or `EXPERT_VALIDATED`. Gates G1 through G7 in the approved protocol are not completed.

No official raw bytes of the requested instruments were obtained. The responses below are access-block pages. They were not saved under `audit/source_downloads/` and they were not given document filenames.

## A. Acquisition Scope and Approved Snapshot

| Item | Value observed before retrieval |
| --- | --- |
| Branch | `main` |
| HEAD | `583ad0b30e8007a5f3f0bb13ede7b010fdad5fec` |
| Pre-existing untracked file | `docs/reproducibility/REGULATORY_SOURCE_AND_EXPERT_REVIEW_PROTOCOL_DRAFT.md` |
| Protocol SHA-256 | `b4bd071a96a6d0180f1850bcacd5fe1af8ccfbb7de9faa137e4164e2563df76b` |
| Rule catalog SHA-256 | `4eef75aad02540726c5784538dc961db0ef9f84d40e94526f3d5f8d33c94e6cd` |
| Source register SHA-256 | `5c6ede8c299a1a7b57970bc21fb80b98e83ca68632b80082e5b12cd636e3c7a2` |
| Approved protocol | STEP 3B-8A draft. This step did not modify it. |
| Client | `curl` over HTTPS, HTTP/1.1, certificate verification left enabled, redirects not followed |
| Access policy | One ordinary public GET per recorded URL. No credential, no CAPTCHA solution, no user-agent substitution, no proxy, and no TLS verification bypass. |

Targets were limited to the SBP SGF 2025 family, SBP IBD Circular No. 01 of 2012, and the SECP SGR 2023 record already named in the source register.

## B. Source Register Baseline

Read from `docs/shariah/source_register.json` (`stage7-source-register-v1`) before any request. These rows are historical register entries. Their `verification_status` labels are not findings of this acquisition.

| Source ID | Register URL | Register `sha256` | Register note used as the starting point |
| --- | --- | --- | --- |
| `SRC-SBP-IFPD-C8-2024` | `https://www.sbp.org.pk/ifpd/2024/C8.htm` | null | Official HTML said to have been retrieved earlier. Annex PDF said to have returned HTTP 403. The annex URL is not stored in the register. |
| `SRC-SBP-SGF-2025-TEXT` | PICG-hosted PDF URL | `6c32d43d528104271bccd2dd228ba8ca33e94abe459494c6d4abdae41ef06ca1` | Third-party copy. Not used as an official download in this step. |
| `SRC-SBP-IBD-C1-2012` | `https://www.sbp.org.pk/ibd/2012/C1.htm` | null | Official HTML said to have been retrieved on 2026-09-15. |
| `SRC-SBP-IBD-C2-2008-IDENTITY` | `https://www.sbp.org.pk/ibd/2008/C2.htm` | null | Identity row. Annex clauses `NOT_VERIFIED`. |
| `SRC-SECP-SGR-2023-PAGE` | `https://www.secp.gov.pk/document/shariah-governance-regulations-2023-2/` | null | Official landing page. Official PDF said to have returned HTTP 403. The PDF URL is not stored in the register. |
| `SRC-SECP-SGR-2023-SRO-TEXT` | MUFAP-hosted PDF URL | `7ffe4179154a793da18cfb1e783a32bf74408bea7513dffbf2b42b67f4929ba7` | Third-party copy. Not used as an official download in this step. |

No annex URL, Gazette URL, or official SECP PDF URL was invented.

## C. Target A — SBP SGF 2025

### C.1 IFPD Circular No. 08 of 2024

| Field | Observation |
| --- | --- |
| Issuing authority sought | State Bank of Pakistan |
| Instrument sought | IFPD Circular No. 08 of 2024 |
| Request URL | `https://www.sbp.org.pk/ifpd/2024/C8.htm` |
| Retrieval UTC | `2026-10-18T19:02:47.142Z` |
| HTTP status | 403 Forbidden |
| Final URL | Same as the request URL |
| Redirect history | None. No `Location` header. |
| Response `Date` | Sun, 18 Oct 2026 19:02:47 GMT |
| `Content-Type` | `text/html; charset=UTF-8` |
| `Server` | cloudflare |
| `CF-RAY` | `a4c9cca5997344a9-SIN` |
| Body size | 5020 bytes |
| Body SHA-256 | `86245ddcea6cc7fd7e2c95c90eb772b747bac6da2868cb8ba2060bc13631aa25` |
| Actual file type | HTML. Leading bytes are `<!DOCTYPE html>`. Title: `Attention Required! \| Cloudflare`. Not a PDF. |
| Local repository path | Not saved. The body is a block page, not the circular. |
| Acquisition state | `RETRIEVAL_BLOCKED` and `ACCESS_RESTRICTED` |
| Byte state | `NO_OFFICIAL_BYTES_AVAILABLE` |
| Authenticity | `INDEPENDENT_AUTHENTICATION_PENDING` |

The circular HTML was not retrieved, so no official title, publication metadata, or annex link could be read from it in this step.

### C.2 SGF annex or booklet

No annex URL was present in the source register, and the circular page did not load. No annex request was issued. State: `DOCUMENT_IDENTITY_UNRESOLVED` for the official annex address, and `NO_OFFICIAL_BYTES_AVAILABLE`.

The historical PICG file remains a third-party copy. It was not re-downloaded and was not treated as the official SBP annex.

## D. Target B — SBP IBD Circular 01 of 2012

| Field | Observation |
| --- | --- |
| Issuing authority sought | State Bank of Pakistan |
| Instrument sought | IBD Circular No. 01 of 2012 |
| Request URL | `https://www.sbp.org.pk/ibd/2012/C1.htm` |
| Retrieval UTC | `2026-10-18T19:02:48.612Z` |
| HTTP status | 403 Forbidden |
| Final URL | Same as the request URL |
| Redirect history | None. No `Location` header. |
| Response `Date` | Sun, 18 Oct 2026 19:02:48 GMT |
| `Content-Type` | `text/html; charset=UTF-8` |
| `Server` | cloudflare |
| `CF-RAY` | `a4c9cca8ae869b2b-SIN` |
| Body size | 5020 bytes |
| Body SHA-256 | `9f4f6e78f9cbf14d7184d55802aa67485aeba994bd1b9ed839822e13894c2d04` |
| Actual file type | HTML block page. Title: `Attention Required! \| Cloudflare`. Not a PDF. |
| Local repository path | Not saved. |
| Acquisition state | `RETRIEVAL_BLOCKED` and `ACCESS_RESTRICTED` |
| Byte state | `NO_OFFICIAL_BYTES_AVAILABLE` |
| Authenticity | `INDEPENDENT_AUTHENTICATION_PENDING` |

Because the page was not retrieved, this step could not determine whether the official page contains the complete operative circular or links to attachments.

### D.1 Contextual 2008 reference already recorded in the register

The 2012 page supplied no new link. The register already records `https://www.sbp.org.pk/ibd/2008/C2.htm` as `SRC-SBP-IBD-C2-2008-IDENTITY`. One public GET was made to that recorded URL so its current access state could be logged. This was not an authentication of the 2008 Murabahah Essentials annex.

| Field | Observation |
| --- | --- |
| Request URL | `https://www.sbp.org.pk/ibd/2008/C2.htm` |
| Retrieval UTC | `2026-10-18T19:03:06.885Z` |
| HTTP status | 403 Forbidden |
| Final URL | Same as the request URL |
| Redirect history | None. No `Location` header. |
| Response `Date` | Sun, 18 Oct 2026 19:03:06 GMT |
| `Content-Type` | `text/html; charset=UTF-8` |
| `Server` | cloudflare |
| `CF-RAY` | `a4c9cd1b3f5781c6-SIN` |
| Body size | 5020 bytes |
| Body SHA-256 | `085b00ce08bc18e76ae0a2d86649829f42cb9f6e01927cf34290fb64c22283c5` |
| Actual file type | HTML block page. Title: `Attention Required! \| Cloudflare`. |
| Local repository path | Not saved. |
| Acquisition state | `RETRIEVAL_BLOCKED` and `ACCESS_RESTRICTED` |
| Annex bytes | `NO_OFFICIAL_BYTES_AVAILABLE`. The Essentials annex remains unauthenticated. |

## E. Target C — SECP SGR 2023

| Field | Observation |
| --- | --- |
| Issuing authority sought | Securities and Exchange Commission of Pakistan |
| Instrument sought | Official record for the Shariah Governance Regulations, 2023, S.R.O. 1314 (I)/2023 |
| Request URL | `https://www.secp.gov.pk/document/shariah-governance-regulations-2023-2/` |
| Retrieval UTC | `2026-10-18T19:02:49.046Z` |
| HTTP status | 403 Forbidden |
| Final URL | Same as the request URL |
| Redirect history | None. No `Location` header. |
| Response `Date` | Sun, 18 Oct 2026 19:02:49 GMT |
| `Content-Type` | `text/html; charset=UTF-8` |
| `Content-Length` | 5557 |
| `Server` | cloudflare |
| `CF-RAY` | `a4c9ccac6d37fdc5-SIN` |
| `Cf-Mitigated` | `challenge` |
| Body size | 5557 bytes |
| Body SHA-256 | `dcc0503b7d73e703c5035964f8cb33aab052fb319e33ae1e190e4b31de167fa5` |
| Actual file type | HTML. Title: `Just a moment...`. Challenge markup refers to `challenges.cloudflare.com`. Not a PDF. |
| Local repository path | Not saved. |
| Acquisition state | `ACCESS_RESTRICTED` and `RETRIEVAL_BLOCKED` |
| Byte state | `NO_OFFICIAL_BYTES_AVAILABLE` |
| Authenticity | `INDEPENDENT_AUTHENTICATION_PENDING` |

The challenge was not solved. No official SECP PDF URL was present in the register, and none was inferred. No Gazette location was identified from a retrieved SECP page. A Gazette copy and an SECP copy were therefore not compared, and they are not assumed to be byte-identical.

The historical MUFAP file was not used as a substitute official download.

## F. Raw-Artifact Inventory

No candidate official document was saved.

| Artifact | Repository path | SHA-256 | Size | Source URL | Retrieval UTC | Git-ignored |
| --- | --- | --- | --- | --- | --- | --- |
| None | — | — | — | — | — | — |

Block-page responses were hashed only to identify what the client received. They are unsuccessful attempts, not completed downloads. Their SHA-256 values are in sections C, D, and E. They were not copied into the repository.

`git check-ignore` was confirmed before this step for the existing pattern `audit/source_downloads/*` (`.gitignore` line 67). No new raw destination was written, because no retrieved body was the requested document.

## G. Retrieval Logs and Access Failures

| Attempt | UTC | URL | Status | Redirects | Classification |
| --- | --- | --- | --- | --- | --- |
| A circular | `2026-10-18T19:02:47.142Z` | `https://www.sbp.org.pk/ifpd/2024/C8.htm` | 403 | none | Cloudflare HTML block page. Not the circular. |
| B circular | `2026-10-18T19:02:48.612Z` | `https://www.sbp.org.pk/ibd/2012/C1.htm` | 403 | none | Cloudflare HTML block page. Not the circular. |
| C landing page | `2026-10-18T19:02:49.046Z` | `https://www.secp.gov.pk/document/shariah-governance-regulations-2023-2/` | 403 | none | Cloudflare challenge page. Not the SRO. |
| B context, register URL only | `2026-10-18T19:03:06.885Z` | `https://www.sbp.org.pk/ibd/2008/C2.htm` | 403 | none | Cloudflare HTML block page. Not the 2008 annex. |

TLS certificate verification remained enabled. No request was retried with a different user agent, cookie, or solver. No third-party mirror was fetched.

## H. Comparison With Historical Third-Party Copies

The three historical files were present. Their SHA-256 values were recomputed before the requests and matched the previously reported digests.

| Historical file | Recomputed SHA-256 | Size (bytes) | Comparison with a new official candidate |
| --- | --- | --- | --- |
| `audit/source_downloads/picg_sgf_2025.pdf` | `6c32d43d528104271bccd2dd228ba8ca33e94abe459494c6d4abdae41ef06ca1` | 1194719 | Cannot be compared. Official SBP circular and annex bytes were not obtained. |
| `audit/source_downloads/mufap_sgr2023.pdf` | `7ffe4179154a793da18cfb1e783a32bf74408bea7513dffbf2b42b67f4929ba7` | 617755 | Cannot be compared. Official SECP bytes were not obtained. |
| `audit/source_downloads/baf_sgf.pdf` | `becd6b94ae3e0be1f30c482b1ad8b7158870c424963aa107a27a2763d46c09a8` | 1328390 | Cannot be compared. Official SBP bytes were not obtained. |

These recomputed digests also match the digests recorded for the PICG and MUFAP rows in the source register. The BAF file still has no register row. No historical PDF was modified. A hash difference was not available to interpret, because the official side of each comparison is missing.

## I. Official-Source Authenticity Still Pending

| Requirement | State after this step |
| --- | --- |
| A. Document identity from an official publication record | Unresolved. The official pages did not load. |
| B. Integrity of official instrument bytes | `NO_OFFICIAL_BYTES_AVAILABLE`. Block-page hashes identify the failed responses only. |
| C. Operative clause and version | Not examined. No clause comparison was performed. |
| D. Case-level applicability | Not started. |
| E. Qualified expert validation | Not started. |
| G1–G7 | Not completed. A blocked download is not a completed gate. |
| Engine applicability | Remains `SCOPE_UNKNOWN` for the six source rules. This step did not change the engine. |

A URL on `sbp.org.pk` or `secp.gov.pk` was the address requested. The HTTP 403 response does not establish that the unseen document is authentic, in force, or applicable.

## J. Amendments and Supersession Discovery Leads

No amendment, replacement, Gazette, repeal, or transitional link was observed in this step, because the official pages returned block pages rather than instrument text.

The source register already contains earlier notes that IBD Circular No. 01 of 2012 repeals IBD Circular No. 04 of 2008, and that the 2012 circular cites the 2008 Essentials annex. Those notes are prior register text. This acquisition did not re-read them from official bytes and does not declare any instrument repealed, amended, or currently operative.

Unanswered later-version questions:

- Whether any SBP instrument after IFPD Circular No. 08 of 2024 amends or replaces the SGF.
- Whether any SBP instrument after 6 February 2012 amends the 2012 invoice and payment paragraphs.
- Whether the 2008 Essentials annex still has operative text for cases that cite it.
- Whether S.R.O. 1314 (I)/2023 has a Gazette copy, and whether that copy matches any later official SECP file.
- Whether any SECP instrument after 14 September 2023 amends the Shariah Governance Regulations, 2023.

## K. Remaining Missing Instruments

| Instrument | State |
| --- | --- |
| Official IFPD Circular No. 08 of 2024 HTML | `NO_OFFICIAL_BYTES_AVAILABLE` |
| Official SGF 2025 annex or booklet | Address unresolved. Bytes not obtained. |
| Official IBD Circular No. 01 of 2012 HTML | `NO_OFFICIAL_BYTES_AVAILABLE` |
| 2008 Murabahah Essentials annex | Not authenticated. The recorded circular URL returned 403. |
| Official SECP SGR 2023 landing content | `ACCESS_RESTRICTED` |
| Official SECP PDF for S.R.O. 1314 (I)/2023 | URL not in the register and not discovered. Bytes not obtained. |
| Gazette copy of S.R.O. 1314 (I)/2023 | Publication location not identified in this step. |

## L. Git and Historical Artifact Integrity

Pre-acquisition `git status --short` listed only the untracked protocol draft. HEAD was the expected snapshot. The protocol, catalog, source register, and three historical PDFs were hashed before retrieval.

This step created only this ledger. It did not modify the protocol, catalog, source register, engine, tests, manuscripts, models, datasets, thresholds, or historical PDFs. It did not create Stage 7 or Stage 8 outputs. The post-acquisition comparison is recorded after the ledger file itself is written; the retrieval operation completed before this sentence was drafted and did not write those tracked paths.

## M. Recommended Next Authentication-Review Step

Repeat the official-page retrieval from a supervised environment that receives the public pages through ordinary access, or obtain the instruments through a formal public-records request to SBP and SECP. Preserve any future raw bytes under new gitignored names. Do not overwrite `picg_sgf_2025.pdf`, `mufap_sgr2023.pdf`, or `baf_sgf.pdf`.

If a future response is the instrument rather than a block page, hash it, then compare it with the historical third-party digests. That comparison still leaves independent provenance review, clause verification, applicability, and qualified Shariah review uncompleted.

This environment should not solve the Cloudflare challenge or rotate client identity in order to convert the recorded 403 responses into downloads.

**DRAFT EVIDENCE LEDGER — SOURCE ACQUISITION ONLY; NO REGULATORY APPLICABILITY OR EXPERT VALIDATION ESTABLISHED**
