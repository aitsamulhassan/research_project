# Contemporary literature and dataset-feasibility audit (draft)

Status: draft for supervisor review. Search date: 2026-10-18. This file records a focused external check. It is not a PRISMA systematic review, not a manuscript revision, and not a new experiment.

No dataset file was downloaded. No historical result was recomputed. Absence from this search is not absence from the literature.

## A. Scope and baseline

Branch `main`. HEAD `583ad0b30e8007a5f3f0bb13ede7b010fdad5fec`.

Manuscript hashes verified before this file was created:

| File | SHA-256 |
|---|---|
| `docs/paper/IEEE_ACCESS_READY_MANUSCRIPT.tex` | `0d6197f62e8abee200c63fb0d75a21b03ac9305ff508ac7128e87cbbb18ea9d3` |
| Gitignored template duplicate | `0d6197f62e8abee200c63fb0d75a21b03ac9305ff508ac7128e87cbbb18ea9d3` |
| `docs/paper/IEEE_MANUSCRIPT.md` | `88fb860de5d43875041fd009c3798db95411c516ff78dea5771e4f3666ef92fb` |
| `docs/paper/MANUSCRIPT_DRAFT.md` | `50d64a4761847a5920b2abaa9b6bc97291f2ec6bba0231f3022a91451868e11d` |

Unchanged companion drafts:

| File | SHA-256 |
|---|---|
| `REGULATORY_SOURCE_AND_EXPERT_REVIEW_PROTOCOL_DRAFT.md` | `b4bd071a96a6d0180f1850bcacd5fe1af8ccfbb7de9faa137e4164e2563df76b` |
| `OFFICIAL_PRIMARY_SOURCE_ACQUISITION_LEDGER_DRAFT.md` | `100fa59b74d2c187e268e76432e8cda3089ac6b2942a630b15cc491c91f180fb` |
| `SCIENTIFIC_PUBLICATION_READINESS_AUDIT_DRAFT.md` | `052b4bf184c75e2368a89e445a6a07cd33e4cdaa555010b1cebe121165944e1e` |

Sources read inside the repository: the canonical LaTeX manuscript, especially Sections II–III and the dataset subsection, and `SCIENTIFIC_PUBLICATION_READINESS_AUDIT_DRAFT.md` findings M-08 and A-01.

The manuscript’s own contribution boundary, already written in Section III, is the object of this audit:

- An engineering integration and auditability case study.
- A software evidence-separation design.
- A documented fixed-score routing experiment.
- Explicitly not a new predictive algorithm, a regulatory certification, or a demonstrated human-interpretability gain.
- The local literature register is not treated as proof that comparable work is absent worldwide.

### What the frozen artifacts actually demonstrate

| Item | Demonstrated by stored artifacts | Not demonstrated |
|---|---|---|
| A. Chronological credit-risk evaluation | LendingClub issue-month split; four families; validation PR-AUC tie then Brier/simplicity; one TEST report. M-4B EBM ROC-AUC 0.6799408767429772. XGBoost TEST ROC-AUC 0.6854404067747387 is higher. | A new scoring algorithm. A fair probability ranking across differently weighted objectives. Superiority to prior Lending Club models. |
| B. Train-only EBM plus validation-fitted calibration | M-5 is a different fit from M-4B. Platt was selected on validation Brier with a 0.001 tie. Pooled TEST Brier and ECE improve. The 2018 slice worsens Brier, log loss, and ECE. Year-slice intervals are not stored. | That governance improves prediction. That Platt is stable across later years. A calibrator chosen from the 2018 slice. |
| C. Additive explanations | `interactions=0` EBM; additive reconstruction error \(8.881784197001252\times 10^{-16}\) on 5,000 TEST rows; Spearman 1.0 with the centered terms. | A human interpretability benefit. An adverse-action reason-code study. A fairness audit. |
| D. Evidence-separated architecture | Scores, explanation objects, and governance outputs are separate software objects. Fusion reads frozen `p_selected`. | That the separation is new in the literature. That unit tests prove operational effectiveness. |
| E. Documentary abstention | Historical engine v1 labels all 208,886 LendingClub TEST rows `INSUFFICIENT_INFORMATION` because contract fields are absent. Six live rules are `SCOPE_UNKNOWN`. No rule is `EXPERT_VALIDATED`. | Shariah accuracy. Applicability of SBP, SECP, or AAOIFI text. A measured review workload. |
| F. Frozen-score routing | A0, A1, and A3/A4 counts differ on identical scores. The 27 A1 rejects are the HIGH band, \(n=27\), Wilson interval [0.3398532458621043, 0.6925704935029092]. | That one map outperforms another. That `HUMAN_REVIEW` was staffed or completed. |

UCI Default of Credit Card Clients is a second public credit table. It does not carry the governance layer. The exploratory UCI XGBoost arm remains `DEVIATION-001`.

## B. Literature search strategy and search date

Date of search: 2026-10-18.

This was a focused discovery pass, not a database-wide systematic review. Scopus, Web of Science, and IEEE Xplore full-text search were not available in this session. Identity checks used Crossref (`https://api.crossref.org/works/{doi}`), arXiv abs pages, Zenodo’s record API, publisher HTML when returned by search, and regulator pages.

Queries used:

- explainable boosting machine credit scoring calibration 2023–2025
- probability calibration temporal validation credit scoring Platt isotonic
- Islamic banking machine learning credit risk murabahah dataset 2023–2025
- Shariah compliance artificial intelligence screening governance 2023–2025
- selective prediction, reject inference, and human review in credit scoring
- IEEE Access explainable credit scoring Lending Club 2024–2025
- public Islamic-bank financing default dataset, OJK statistics, IFSB PSIFIs, SBP Islamic Banking Bulletin

A paper is “independently identifiable” here only when a DOI or arXiv identifier resolved to a title, authors, year, and venue. Abstract-only comparisons are marked. Full-text findings are reported only where the HTML was actually retrieved.

## C. Verified contemporary literature

Fifteen works are retained. Preprints are not counted as peer-reviewed articles.

### C1. Schwartz, Wang, and Fang (2025) — strongest predictive overlap

- Title: Enhancing ML Models Interpretability for Credit Scoring.
- Authors: Sagi Schwartz; Qinling Wang; Fang Fang.
- Year: submitted 14 September 2025.
- Venue: arXiv:2509.11389. Preprint, not a journal article.
- DOI: `10.48550/arXiv.2509.11389`. Record URL: `https://arxiv.org/abs/2509.11389`.
- Research question: whether SHAP-guided feature selection plus a glass-box model can match a black-box credit model with fewer features.
- Dataset: Lending Club platform data. The fetched HTML says the target keeps Fully Paid and Charged Off, uses `issue_d`, trains through July 2015, and tests August 2015–December 2018, with about 87 features before reduction. It cites Ariza-Garzón et al., IEEE Access, 2020, as the preprocessing precedent. It does not cite Zenodo `10.5281/zenodo.11295916` in the sections inspected.
- Methods: XGBoost as the black-box benchmark; SHAP for feature selection; EBM and penalized logistic tree regression as glass-box models; class weights. A calibration section was not found in the fetched HTML.
- Outcomes: the HTML reports that more than 10 features did not substantially improve AUPRC, AUROC, and F1 on that Lending Club preprocessing, an 88.5% feature reduction in the abstract.
- Limitations visible in the fetched text: one platform dataset; future tests on other datasets are recommended. No Shariah objects.
- Overlap with KarimPay: same platform family, chronological `issue_d` split, EBM versus XGBoost, and additive/glass-box motivation. Not the same 15-column Zenodo extract, not Platt-on-validation, not documentary abstention.
- Verification: arXiv abs page and the HTML full text. Preprint.

### C2. Hoang, Karthikeya, and Rao (2025) — EBM plus calibration and risk tiers

- Title: Bridging Predictive Performance and Transparency: A Multi-Model Framework for Small-Business Loan Default Segmentation.
- Authors: Minh Nguyen Hoang; Thota Sai Karthikeya; Thota Sree Mallikharjuna Rao.
- Year: Crossref issued year 2025. Publisher HTML says published 2025-12-24.
- Venue: Journal of Technology Management for Growing Economies. Crossref type: journal-article.
- DOI: `10.15415/jtmge/2025.162001`. Publisher HTML: `https://tmg.chitkara.edu.in/paper-html.php?pId=3141`.
- Research question: whether a calibrated LightGBM champion and an EBM challenger can segment SME default risk while remaining transparent.
- Dataset: described as SME loans. The publisher abstract does not give a public repository URL. It suggests LendingClub as a future external test, which implies this study’s own file is not that extract.
- Methods, from the abstract only: cross-validated LightGBM and EBM optimized for ROC-AUC; isotonic calibration mentioned for the LightGBM pipeline; probability tiers Low / Medium / High.
- Outcomes stated in the abstract: LightGBM ROC-AUC 0.969; EBM ROC-AUC 0.963; tier default rates 2.5%, 48.8%, and 89.7%. These figures were not recomputed and the underlying file was not seen.
- Limitations: full methods, sample size, and data-release status were not verified beyond the publisher abstract.
- Overlap: glass-box EBM, probability calibration, and post-score risk tiers. Not Shariah evidence, not a frozen multi-map policy, not the KarimPay extract.
- Verification: Crossref plus publisher abstract HTML. Full-methods comparison was not possible.

### C3. Hartomo, Arthur, and Nataliani (2025) — IEEE Access explainable credit model

- Title: A Novel Weighted Loss TabTransformer Integrating Explainable AI for Imbalanced Credit Risk Datasets.
- Authors: Kristoko Dwi Hartomo; Christian Arthur; Yessica Nataliani.
- Year: 2025.
- Venue: IEEE Access. Crossref type: journal-article.
- DOI: `10.1109/ACCESS.2025.3541878`.
- Research question: class imbalance and opacity in credit risk models.
- Dataset named in the abstract: BISAID and German Credit. A public landing page for BISAID was not found in this search.
- Methods, from the abstract: TabTransformer with weighted loss; SHAP.
- Outcomes stated in the abstract: accuracy 86.35% to 89.27% on one set and 93% to 95% on the other. Not recomputed.
- Limitations: abstract only. No EBM, no temporal Platt study, no Islamic contract labels identified.
- Overlap: explainable credit scoring in the same target journal. The algorithm and datasets differ.
- Verification: Crossref metadata and the abstract returned with the DOI. Full text was not retrieved.

### C4. Xu, Liao, Li, Zhang, Song, Wang, and Yuan (2024)

- Title: SHAP-based Interpretable Models for Credit Default Assessment Using Machine Learning.
- Year: 2024. Venue: 2024 14th International Conference on Software Technology and Engineering (ICSTE). Crossref type: proceedings-article.
- DOI: `10.1109/ICSTE63875.2024.00044`.
- Research question: feature contributions in credit default assessment.
- Dataset named in the abstract: Lending Club. The extract, row count, and split were not in the retrieved abstract.
- Methods: SVM, MLP, XGBoost, LightGBM, with SHAP. Not an EBM identity proof.
- Outcomes: abstract says interest rate and credit policy dominate in that dataset. No numeric AUC was in the retrieved abstract.
- Overlap: Lending Club plus post-hoc SHAP. Not documentary governance.
- Verification: Crossref and abstract. Full text was not retrieved.

### C5. Kozodoi, Lessmann, Alamgir, Moreira-Matias, and Papakonstantinou (2025)

- Title: Fighting sampling bias: A framework for training and evaluating credit scoring models.
- Year: 2025. Venue: European Journal of Operational Research. Crossref type: journal-article.
- DOI: `10.1016/j.ejor.2025.01.040`.
- Research question: how to train and evaluate scorecards when rejected applicants have no observed repayment.
- Dataset: abstract says synthetic data plus observational micro-lending data that includes an unbiased accepted-without-scoring sample. No public URL was in the retrieved abstract.
- Methods, from the abstract: bias-aware self-labeling and a Bayesian evaluation that imputes random pseudo-labels for rejects.
- Outcomes stated in the abstract: expected return per dollar issued increases by up to 2.07 and 5.76 percentage points for the two proposals. Not recomputed.
- Overlap: directly relevant to KarimPay’s originated-and-resolved LendingClub cohort. It does not supply Islamic contract labels. KarimPay did not run reject inference.
- Verification: Crossref and abstract. Full-methods comparison was not possible.

### C6. Scarone and Baeza-Yates (2026)

- Title: The Illusion of Improvement: Reject Inference Strategies in Credit Scoring.
- Authors and affiliations as printed on the HTML: Bruno Scarone, Northeastern University; Ricardo Baeza-Yates, KTH.
- Year: arXiv submission dated 16 June 2026.
- Venue: arXiv:2606.18479. Preprint.
- DOI: `10.48550/arXiv.2606.18479`. URL: `https://arxiv.org/abs/2606.18479`.
- Research question: whether standard reject-inference metrics create an illusion of improvement under a retraining cycle.
- Datasets named in the fetched HTML: Default (30,000 persons, 23 features; the UCI-style credit-card table), PPDai (31,389), and a 2017 LendingClub slice filtered to 302,595 rows after down-sampling. These are not KarimPay’s 1,347,681-row Zenodo extract.
- Methods: GBDT and random forest; several reject-inference strategies; a controlled exploration of rejected applicants inside a simulation.
- Outcomes in the fetched HTML: on the Default/GBDT configuration, accuracy can rise while recall falls; the authors treat that as a failure of accuracy under selection bias. LendingClub effects in their simulation are smaller than on Default.
- Overlap: public credit data and the originated-only bias. Not Shariah screening. The exploration policy is a research simulation, as is KarimPay’s `HUMAN_REVIEW`, but the mechanisms differ.
- Verification: arXiv HTML. Preprint, not peer-reviewed.

### C7. Pugnana and Ruggieri (2023)

- Title: A Model-Agnostic Heuristics for Selective Classification.
- Year: 2023. Venue: Proceedings of the AAAI Conference on Artificial Intelligence. Crossref type: journal-article (AAAI proceedings).
- DOI: `10.1609/aaai.v37i8.26133`.
- Research question: model-agnostic selective classification, motivated in part by credit scoring as a high-risk use.
- Datasets: the fetched page names tabular sets including Lending, GiveMe, and UCICredit among the experiments, with LightGBM as one base learner. Islamic contract fields are not part of the study.
- Methods: SCROSS, a cross-fitting reject option. Abstention means refusing a low-confidence prediction.
- Outcomes: comparative coverage and selective accuracy against plugin, SelectiveNet, and self-adaptive training. Figures were not transcribed into this audit.
- Overlap: abstention as a statistical reject option. KarimPay’s abstention is documentary: missing contract fields, not low predictive confidence. These are different decisions.
- Verification: publisher HTML retrieved through the DOI. Experimental tables were not re-analyzed.

### C8. Züger, Mahlow, Pothmann, Mosene, Burmeister, Kettemann, and Schulz (2025)

- Title: Crediting Humans: A Systematic Assessment of Influencing Factors for Human-in-the-Loop Figurations in Consumer Credit Lending Decisions.
- Year: 2025. Venue: Proceedings of the 2025 ACM Conference on Fairness, Accountability, and Transparency.
- DOI: `10.1145/3715275.3732086`. URL: `https://dl.acm.org/doi/10.1145/3715275.3732086`.
- Research question: what lets a human meaningfully control semi-automated consumer-credit decisions.
- Dataset: not a loan table. The fetched HTML describes a German-context study: a roundtable of 13 experts and 13 interviews with 19 experts from lenders, counselors, Schufa, and BaFin.
- Methods: qualitative architecture modeling and interviews. Scope stated as consumer loans up to about one million euros in Germany.
- Outcomes: interview evidence that humans still override or manually complete cases, and that application forms drop information the model cannot see. No predictive metric.
- Overlap: human review in credit operations. KarimPay’s `HUMAN_REVIEW` is a simulated label, not an observed staffing process. This paper is evidence that a simulated route is not a measured review.
- Verification: ACM HTML. Peer-reviewed conference paper.

### C9. Kurth, Nendel, and Streicher (2024)

- Title: A Hypothesis Test for the Long-Term Calibration in Rating Systems with Overlapping Time Windows.
- Year: 2024. Venue: Risks (MDPI), volume 12, issue 8. An earlier working-paper version is cited by RePEc as Bielefeld CMS working paper 735 and as arXiv:2312.14765.
- DOI: `10.3390/risks12080131`.
- Research question: a supervisory test of long-run default rates when rating windows overlap.
- Dataset: statistical method; no applicant microdata were identified in the retrieved abstract.
- Methods: normal approximation and conservative tests for an unknown distribution of default probabilities.
- Overlap: temporal calibration can fail even when a rating system is fixed. KarimPay’s 2018 Platt reversal is an empirical slice, not this hypothesis test. The paper does not validate KarimPay’s Platt map.
- Verification: Crossref. Full text was not fetched, so the comparison stays at the abstract and bibliographic record.

### C10. Pomazanov and Berezhnoy (2024)

- Title: Parametric methods for precision calibration of scoring models.
- Year: 2024. Venue: Procedia Computer Science. Crossref type: journal-article.
- DOI: `10.1016/j.procs.2024.08.175`.
- Research question: IRB-style calibration of a score to a long-run default frequency, with conservative rounding on the rating scale.
- Dataset: the ScienceDirect abstract says the methods were tested in practice on loan-portfolio segments. No public micro file was named in that abstract.
- Methods: two parametric calibration adjustments. Not Platt versus isotonic on LendingClub.
- Overlap: credit-score calibration as a regulated activity. Not KarimPay’s validation-only Platt protocol.
- Verification: Crossref plus the ScienceDirect abstract. Full-methods comparison was not possible.

### C11. Sugozu, Verberi, and Yasar (2025)

- Title: Machine learning approaches to credit risk: Evaluating Turkish participation and conventional banks.
- Year: 2025. Venue: Borsa Istanbul Review.
- DOI: `10.1016/j.bir.2025.02.001`. URL: `https://doi.org/10.1016/j.bir.2025.02.001`.
- Research question: competition and credit risk in Turkish participation (Islamic) versus conventional banks.
- Dataset: 33 conventional and 6 Islamic banks, annual data 2009–2022. This is a bank-year panel, not borrower contracts.
- Methods: CatBoost, XGBoost, random forest, LightGBM, and TreeSHAP.
- Outcomes in the abstract: participation banks have higher credit risk in that panel; competition and loan size increase risk; growth reduces it.
- Overlap: Islamic banking appears as an institution type. There is no Murabahah invoice, no documentary abstention, and no applicant default label.
- Verification: Crossref and the article abstract. A reusable microdata URL was not provided.

### C12. Gafsi (2025)

- Title: Machine Learning Approaches to Credit Risk: Comparative Evidence from Participation and Conventional Banks in the UK.
- Year: 2025. Venue: Journal of Risk and Financial Management, 18(7), 345.
- DOI: `10.3390/jrfm18070345`.
- Research question: ML forecasts of credit risk for UK participation and conventional banks.
- Dataset: abstract describes a bank panel, about 2010–2023, with non-performing loans and a Lerner-index competition measure. No applicant file and no contract corpus were named.
- Methods: machine-learning forecasts at bank level. Full specification was not fetched.
- Overlap: “Islamic / participation bank” at institutional grain. Not a Shariah-screening benchmark.
- Verification: Crossref and the IDEAS abstract. Full text was not compared method by method.

### C13. Siregar, Ruslan, Faried, and Sembiring (2025)

- Title: Implementation of Machine Learning Algorithm for Credit Scoring Prediction in Islamic Microfinance.
- Year: published date on the publisher page 2025-07-16. Venue: Journal of Intelligent Systems and Information Technology.
- DOI: `10.61971/jisit.v2i2.156`.
- Research question: XGBoost, with and without pruning, for collectibility of Islamic microfinance customers.
- Dataset: primary questionnaires from 57 customers in Hamparan Perak, Deli Serdang, 2022–2024. Seven attributes include financial ratio, payment history, financing amount, business age, sector, transaction frequency, and collectibility. The fetched page does not give a repository URL.
- Methods: XGBoost. The page claims the model supports Shariah-compliant decisions, but the attributes listed are ordinary credit attributes. No invoice, possession, or scholar-label field is described.
- Outcomes stated on the page: small metric lifts after pruning (accuracy about 0.70 percentage points). Not recomputed. With \(n=57\), those lifts are not a population benchmark.
- Overlap: the phrase “Islamic microfinance credit scoring.” The design is a tiny private survey, not KarimPay’s architecture and not a public contract benchmark.
- Verification: Crossref and the publisher HTML, which includes a methods section. The microdata were not released in that HTML.

### C14. Gassouma (2025)

- Title: Investigation of Artificial Intelligence Models (AI) in Shariah Auditing of Islamic and Conventional Financing.
- Author: Mohamed Sadok Gassouma.
- Year: 2025. Venue: book chapter in Implications of ICT for Islamic Finance and Economics (IGI Global).
- DOI: `10.4018/979-8-3693-8079-6.ch002`.
- Research question: automated Shariah classification of financing granted to listed Tunisian firms.
- Dataset: not named as a public file. The abstract says the inputs are jurisprudential principles and bank financing to listed institutions.
- Methods: several AI models; the abstract says logistic regression had the lowest error. Full feature list was not retrieved.
- Overlap: an attempt to classify financing as Shariah-relevant. It is institution-level financing of listed firms, not KarimPay’s applicant schema, and it does not use the fail-closed `INSUFFICIENT_INFORMATION` rule on a public consumer extract.
- Verification: Crossref abstract only. Full-methods comparison was not possible.

### C15. Arsyad, Kharisma, and Wiwoho (2025)

- Title: Artificial intelligence and Islamic finance industry: problems and oversight.
- Year: 2025. Venue: International Journal of Law and Management.
- DOI: `10.1108/IJLMA-07-2024-0236`.
- Research question: legal and supervisory design for AI in Islamic finance in Indonesia, Hong Kong, Malaysia, and the UAE.
- Dataset: statutes and comparative legal sources, not a loan table.
- Methods: statute, conceptual, and comparative legal research.
- Outcomes: the abstract says current Islamic banking and insurance statutes do not adequately govern AI, and that Shariah boards need technological expertise. No predictive metric.
- Overlap: the governance problem KarimPay’s software does not solve. The paper is oversight doctrine, not an evidence-gap engine.
- Verification: Crossref abstract. Full text was not fetched.

## D. Literature identity and access limitations

Identified but not used as primary overlap anchors:

- Ajay Punia, “Risk Decisioning for Unsecured Lending Using Gradient Boosted Decision Trees: Calibration, Governance, and Operational Trade-Offs,” International Journal of Science and Research, 2024, DOI `10.21275/SR24727100805`. Crossref resolves the title. The fetched page discusses Platt, isotonic regression, and reason codes as practice guidance. It does not disclose an experimental dataset. It is not treated here as a peer-reviewed empirical benchmark.
- Hebah Shalhoob and Iman Babiker, Open Journal of Business and Management, 2025, DOI `10.4236/ojbm.2025.132075`. Crossref resolves a discussion of AI in Shariah-compliant accounting. Examples of bank deployments in that HTML were not independently checked. Not an applicant-level study.
- Nurfarahin Mohd Haridan and coauthors, “WHAT DO SHARIAH BOARDS THINK ABOUT AI?,” Jurnal Bisnis Terapan, 2023, DOI `10.24123/jbt.v7i2.6061`. Conceptual. Crossref-verified. Not a scoring experiment.
- A PDF titled “Explainable Machine Learning for Credit Risk Assessment” on `ijetjournal.org`, naming Viswatej Seela and reporting EBM AUC 0.782 on 48,000 Lending Club rows, was returned by search. No Crossref DOI was resolved. That item is not counted as verified.

Access limits of this audit:

- No Scopus or Web of Science export.
- IEEE Access and IGI full texts were not purchased.
- Several comparisons are abstract-only, as marked in Section C.
- Search-engine ranking can miss paywalled or non-English papers. A null result is not a worldwide novelty proof.

## E. KarimPay overlap and novelty matrix

| Dimension | What verified 2023–2026 work already does | KarimPay status |
|---|---|---|
| Credit-score performance | EBM versus boosted trees on Lending Club (C1, preprint) and on SME loans (C2, abstract). SHAP on Lending Club (C4). TabTransformer plus SHAP (C3). | Shared method family. KarimPay’s numbers belong to one frozen Zenodo extract and are not a new algorithm. XGBoost’s higher stored TEST discrimination is already disclosed. |
| Calibration | Isotonic or Platt-style calibration is standard in C2, C9, and C10. | The validation-only Platt fit and the 2018 deterioration are a documented case on this extract. They are not a new calibration theory. |
| Explainability | SHAP feature selection and glass-box EBM (C1). SHAP rankings (C3, C4, C11). | The additive reconstruction identity is a property of this `interactions=0` EBM. No human study shows that identity helps a reviewer. |
| Policy separated from prediction | C8 describes operational human control around a score. C7 abstains when the score is uncertain. | KarimPay’s maps are fixed functions of a frozen probability plus an evidence flag. That software separation was implemented. It was not shown to be unique, and it was not shown to improve decisions. |
| Regulatory-document provenance | C15 discusses the lack of AI-specific Islamic-finance statutes. | KarimPay’s SBP/SECP primary bytes remain unauthenticated. This is a limitation, not a contribution. |
| Evidence completeness and abstention | C7 abstains on low predictive confidence. C13 and C14 do not describe a fail-closed missing-document state. | Supported as a software behavior on a schema that lacks contract fields: every stored LendingClub TEST row is `INSUFFICIENT_INFORMATION`. Not a measured compliance rate. |
| Human-review routing | C8 studies real German lending staff. C6 simulates exploring rejected applicants. | `HUMAN_REVIEW` is a simulated route. It is not C8’s observed work. |
| Real Islamic-finance contracts | C11 and C12 are bank panels. C13 is 57 survey respondents. C14 is an abstract about listed-firm financing. | No verified Islamic contract in the executed KarimPay files. |
| Expert-verified Shariah labels | None of C1–C15 supplies a public, expert-labeled contract benchmark that was inspected here. | Not present. Software tests are not scholar review. |
| External validation | C1 explicitly leaves other datasets to future work. C5 and C6 use other public credit tables, still conventional credit. | UCI is a second credit table, not governance validation. |

No verified paper was shown to combine, on the hashed Zenodo LendingClub granting-model extract, a train-only EBM, validation-only Platt, additive term identity, and a documentary Shariah abstention flag fused only at a frozen map. That sentence is a statement about this search. It is not proof that the integration is absent worldwide, and it is not proof that the integration is scientifically superior.

Claim classes:

- Supported differentiation: the audited software record of evidence objects that refuse to score missing contract fields as compliance, plus the frozen counts and the 2018 calibration reversal on this extract.
- Shared with prior work: gradient boosting and EBM credit models, SHAP-style explanations, Platt/isotonic calibration, chronological Lending Club splits, and the warning that accepted-only samples are biased.
- Descriptive implementation choices: threshold values 0.06 / 0.69 / 0.16, the G0 matrix, engine version strings, and the choice of EBM under the tie rule.
- Untested potential contributions: institutional defensibility, human interpretability, review-cost reduction, and Shariah accuracy.
- Unsupported novelty assertions: any claim that the literature contains no comparable system, or that the prototype is a new predictive method.

## F. Dataset candidate inventory

| Candidate | Identity and URL | Class | What was verified on 2026-10-18 | Suitability for KarimPay |
|---|---|---|---|---|
| LendingClub granting-model extract | Zenodo `10.5281/zenodo.11295916`, already the executed file | `PUBLIC_DATA_VERIFIED` | Public record already documented in the manuscript. Not re-downloaded here. | Adequate for the narrow conventional credit task already run. Not an Islamic contract benchmark. |
| UCI Default of Credit Card Clients | DOI `10.24432/C55S3H`, already executed | `PUBLIC_DATA_VERIFIED` | Second public credit table in the project. Not re-downloaded here. | Credit-method context only. No governance fields. |
| Indonesian Islamic-bank financing risk | Zenodo API `https://zenodo.org/api/records/13879460` returned title “dataset of financing risk for islamic banking in Indonesia (semi-annual 2006-2022)”, DOI field `10.5281/zenodo.13879461`, CC-BY-4.0, open, one file `dataset financing risk.xlsx` (119,959 bytes) | `PUBLIC_DATA_VERIFIED` for the file’s existence | The xlsx was not opened, so columns, row count, and contract labels are not verified. The semi-annual span is consistent with an aggregate series. | Not established as an applicant-level Shariah benchmark. |
| OJK Islamic banking statistics | `https://ojk.go.id/id/kanal/syariah/data-dan-statistik/statistik-perbankan-syariah/Pages/Statistik-Perbankan-Syariah---Maret-2025.aspx` | `AGGREGATE_ONLY` | Search retrieval of the official page lists a March 2025 PDF and xlsx. The workbook was not downloaded. | Industry statistics. Not contracts, invoices, or expert labels. |
| IFSB country data | `https://www.ifsb.org/data-metadata/` | `AGGREGATE_ONLY` | Page fetched. Pakistan is listed under Islamic-banking country data and detailed financial statements. No borrower file is offered on that page. | Supervisory aggregates. Not a KarimPay label set. |
| SBP Islamic Banking Bulletin | Index `https://www.sbp.org.pk/ibd/bulletin/bulletin.asp`. December 2025 PDF `https://www.sbp.org.pk/ibd/Bulletin/2025/Islamic%20Banking%20Bulletin%20December%202025.pdf` | `AGGREGATE_ONLY` | PDF text shows industry assets, deposits, financing, and branch counts in PKR billions, sourced from bank RCOA submissions. Example: Dec-2025 financing (net) PKR 5,654 billion. | Pakistan Islamic-banking context. Not applicant, contract, or scholar-labeled data. |
| JISIT microfinance survey | DOI `10.61971/jisit.v2i2.156` | `STUDY_EXISTS_DATASET_UNAVAILABLE` | Paper describes 57 private questionnaires. No download URL. | Too small, private, and not a document corpus. |
| Turkish participation-bank panel | DOI `10.1016/j.bir.2025.02.001` | `STUDY_EXISTS_DATASET_UNAVAILABLE` | Bank-year study. No public microdata URL in the abstract. | Institution-level credit risk. Not contracts. |
| UK participation-bank panel | DOI `10.3390/jrfm18070345` | `STUDY_EXISTS_DATASET_UNAVAILABLE` | Same limitation as the Turkish panel. | Not an applicant benchmark. |
| BISAID, named by Hartomo et al. | Named only in DOI `10.1109/ACCESS.2025.3541878` | `AVAILABILITY_UNVERIFIED` | No dataset landing page was resolved. | Cannot be used until a file and license are identified. |
| German Credit and Australian Credit Approval | Literature-context UCI tables already cited in the manuscript | `PUBLIC_DATA_VERIFIED` as ordinary credit benchmarks | Not executed in KarimPay. Not Islamic. | Optional predictive benchmarks only. |

## G. Verified dataset availability

Public files that this search could confirm are conventional consumer-credit tables already known to the project, one small Zenodo spreadsheet whose columns were not opened, and regulator workbooks or PDFs of industry totals.

A published Islamic-banking paper is not a dataset. C11, C12, C13, and C14 do not, on the evidence retrieved, deposit an applicant-level contract file.

No inspected source simultaneously offered all of the following as a download: borrower or contract rows, a repayment label, an Islamic contract type, invoice or possession evidence, and an expert Shariah label.

## H. Islamic-finance data and label gaps

The gaps that block a compliance claim are:

- Observation level. SBP, OJK, and IFSB publish industry or institutional totals. A balance sheet is not an application.
- Contract type. Murabahah, Ijarah, and similar labels were not found as fields in a verified public micro file.
- Documentary evidence. Invoices, asset identification, possession, and price schedules are the inputs KarimPay’s rules require. They are absent from LendingClub and were not found in a public download.
- Expert labels. No inspected dataset carries a qualified reviewer’s decision that could be compared with the engine.
- Consent. A real financing book is personal data. This audit did not seek bank records and did not attempt to bypass access controls.
- Target conflict already inside LendingClub. The executed extract remains an originated-and-resolved cohort with the documented Default versus Charged Off wording conflict. That is a credit-label problem, separate from the missing Shariah fields.

## I. Minimum viable governance benchmark

A benchmark that could support a Shariah-accuracy claim would need, at minimum:

1. A permissioned sample of real financing contracts in a declared product scope, with the contract type recorded.
2. The documents or structured fields a reviewer would have had at the decision date: asset or invoice identity, price and schedule, possession or ownership evidence, and any cited approval.
3. Labels from qualified reviewers under a written protocol, using categories the software can actually emit, including insufficient information. A model score must not be the label.
4. A split that keeps the labeled contracts out of the rule-writing loop.
5. A separate repayment field only if the study also claims credit prediction. Compliance and default are different targets and should not be collapsed.

Sample size was not estimated here. The current HIGH band of 27 rows shows that a rare cell cannot support a precise rate. A governance benchmark smaller than that, such as the 57-person survey in C13, is not a substitute.

This benchmark is not required to keep the present prototype claim: a chronological credit case, an additive identity, a fail-closed count on a schema without contract fields, and a fixed-score routing table. It is required before any claim of Shariah accuracy, rule applicability, or institutional defensibility.

## J. Recommended research contribution

The strongest framing that matches both the artifacts and the 2023–2026 search is:

An auditability case study of an evidence-separated research prototype. Predictive scores and governance evidence stay distinct. Missing contract documents produce abstention rather than a compliance verdict. A frozen probability is then routed by a predeclared map. On this LendingClub extract, validation-only Platt calibration improves pooled Brier and ECE and worsens all three of Brier, log loss, and ECE in 2018.

That framing has a demonstrable empirical core in the calibration reversal, the family comparison under a predeclared rule, and the exact abstention counts. The architecture itself is a software design. Unit tests show that the code follows its rules. They do not show that the rules are correct Islamic law or that a bank would work faster or more safely.

The current evidence is enough for that bounded case study if the related-work section is updated with the verified overlaps, especially C1, C2, C5, C6, and C7. It is not enough for a paper whose contribution is novelty of method or validated Shariah screening. If those stronger claims are required, the minimum additional evaluation is the expert-labeled contract benchmark in Section I, not another pass over the same LendingClub TEST rows.

## K. IEEE Access publication feasibility

IEEE Access publishes applied machine-learning prototypes, so the venue is not out of scope for a carefully bounded system paper. Scope fit is not acceptance.

| Question | Assessment |
|---|---|
| Empirical strength | Moderate for a case study. The models are established. The useful empirical results are the disclosed tradeoffs: XGBoost discriminates better on the stored TEST metrics; Platt helps the pool and hurts 2018; the HIGH band is tiny. |
| Related work | Incomplete until C1–C7 are discussed. The manuscript already says the 2023–2026 check was not done. This audit supplies a starting set, not a systematic review. |
| Novelty evidence | The integration was not found in this search. That is not a literature proof. Reviewers can cite C1 and C2 as nearby glass-box credit systems. |
| Data and external validity | LendingClub is adequate for the credit task already defined and inadequate for Shariah validation. UCI does not repair that gap. |
| Prototype without expert Shariah review | Defensible only while the paper refuses compliance, applicability, and institutional-defensibility claims. |
| Likely reviewer objections | Prior Lending Club EBM/SHAP work; originated-only bias; 2018 calibration reversal; unauthenticated regulatory texts; simulated rather than observed human review; no Islamic contracts; class-weight limits on Brier. |

This audit does not predict acceptance.

Problems solvable by editing: cite the verified papers, keep the descriptive objective, and keep the negative results visible.

Problems that need new work or external data: expert-labeled contracts, a real review-time study, authenticated primary legal texts, and any paired test that is not already stored. Do not choose a new model on the existing TEST file.

## L. Mandatory versus optional improvements

Mandatory before a compliance or “novel system” claim:

- Update related work with the verified 2023–2026 overlaps, or explicitly retain the “search not completed” limit if the manuscript is not edited. This audit does not itself edit the manuscript.
- Keep Shariah accuracy out of the contribution.
- Do not describe UCI as governance validation.

Mandatory only if the claim is strengthened beyond the prototype:

- The Section I benchmark.
- Qualified reviewer sign-off.
- Authenticated SBP/SECP/AAOIFI texts for any rule that is said to apply.

Optional:

- A later public credit benchmark such as German Credit, as an ordinary predictive check, with a new predeclared split. It would not add Shariah labels.
- Opening the Zenodo Indonesia xlsx under a separate authorization to see whether it is only a semi-annual aggregate. That inspection is not a contract benchmark even if the file is larger than expected.

## M. Prioritized remediation recommendations

1. Treat C1 as the nearest Lending Club glass-box comparator and C5–C6 as the nearest selection-bias comparators when the manuscript’s related work is next authorized.
2. Keep the contribution sentence that this is an integration case study.
3. Leave model choice, thresholds, and the Platt map frozen.
4. If a supervisor wants a Shariah-accuracy paper, commission the Section I benchmark. Do not fill that gap with SBP industry totals or with the 57-person survey.
5. Record this search as incomplete relative to a library systematic review.

## N. Unresolved questions

- Whether Schwartz et al. used any rows from Zenodo `10.5281/zenodo.11295916`. The fetched HTML cites the 2020 IEEE Access preprocessing paper and describes 87 features, which does not match the 15-column granting-model extract, but a row-level identity check was not done.
- Whether the JTMGE SME file, BISAID, or the EJOR micro-lending file can be licensed. No landing page was verified.
- Column inventory of `dataset financing risk.xlsx`. The file is public and was not opened.
- Papers in Arabic, Urdu, Bahasa, and Turkish that this English-language search missed.
- Whether a qualified reviewer panel is available to build the Section I benchmark.

## O. Supervisor decision checklist

1. Accept the bounded case-study framing, or require the expert-labeled contract benchmark before any further manuscript claim.
2. Authorize a later manuscript edit to cite Section C, or leave the literature gap explicitly open.
3. Confirm that no model is reselected on the existing TEST file.
4. Confirm that aggregate SBP, OJK, and IFSB statistics will not be described as an applicant-level Shariah dataset.
5. Decide whether the unopened Zenodo Indonesia workbook deserves a separate, read-only schema inspection.

Search engines, Crossref, arXiv, Zenodo, and the cited regulator pages are the evidence for identities and access. Inferences are marked as inferences. No acceptance probability is offered.
