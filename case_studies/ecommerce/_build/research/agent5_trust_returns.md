# Agent 5 — Trust, Returns and Operations Case Studies (Indian ecommerce / food delivery)

Compiled 2026-10-17. Facts marked as documented were read on pages/PDFs fetched during this research. Anything not on those pages is "Not publicly disclosed (ND)". Interpretation is confined to section 10 of each case and to the final notes.

Evidence key: A = company/named employee described it; B = credible external source on the actual implementation; C = paper or conference talk by company team; D = generic/vendor marketing.

---

## Case R1 — Predicting Return-to-Origin (RTO) on cash-on-delivery orders at checkout using order history plus public social-profile signals
**Company:** Flipkart (research with IIIT Delhi / IIIT Hyderabad academics)
**Industry:** Ecommerce marketplace (India)
**Business Area:** Checkout risk / logistics cost / fraud and abuse
**Problem Type:** Binary classification (order-level risk scoring), imbalanced, with feature enrichment from an external data source
**Evidence Level:** Strong (C) — peer-reviewed workshop paper (WWW '23 Companion) with four Flipkart-affiliated authors, real order data, full result table; no deployment or revenue figure is given.
**Primary Sources:** Hitkul, Abinaya K, Soham Saha, Satyajit Banerjee, Muthusamy Chelliah, Ponnurangam Kumaraguru, "Social Re-Identification Assisted RTO Detection for E-Commerce", WWW '23 Companion (April 30-May 4, 2023), DOI 10.1145/3543873.3587620. Supporting framing only: Meesho RHP coverage (MediaNama), practitioner article (HackerNoon).

### 1. Business Problem
The paper defines RTO as the case where "the user cancels an order while it is in transit for delivery" (authors' definition; its Figure 1 shows an order becoming RTO when cancelled after it has shipped from the source location). It names two losses:
- Logistical cost: shipping to the point of cancellation, returning, and restocking.
- Opportunity cost: the unit is unavailable to another customer who would have accepted delivery.

The authors say an increased RTO rate "by uninformed customers or bad actors can cause unanticipated revenue losses totaling double-digit million dollars annually" (company-team claim, no breakdown). They observed that "orders with cash on delivery are more prone to RTO", and so restricted the study to COD orders.

Context from a different primary document: Meesho's RHP states "72% of orders on Meesho were paid for using cash on delivery (CoD)" for the six months to September 2025, down from 77% in FY25 and 85% in FY24 (as reported by MediaNama; the article gives no RTO rate). The RHP also says CoD "requires physical cash handling by our last mile delivery partners" and raises the risk of unsuccessful deliveries when customers refuse products. This shows why COD risk matters in India but is not a Meesho RTO model.

### 2. Business Question
Can the platform predict, at the time of checkout, the likelihood that an order will become RTO, so that precautionary measures can be triggered? The paper's specific hypothesis: does adding socio-economic signals from a re-identified public professional-network profile improve RTO prediction over historical-trend features alone?

### 3. Data Available
| Data | Description |
|---|---|
| Historical orders and outcomes | "All past orders and their subsequent outcomes"; label = RTO vs delivered |
| Randomised control set | 5% of all orders randomly set aside with no intervention, to avoid bias from other checkout models; only COD orders from this set were used |
| Past-trend features (internal) | RTO ratio vs total orders over last 3 months and 1 year, for user, product, seller, product category; same trends for pin code, street and city in the delivery address; hour of day and weekday of order |
| Social profile, quantitative | Whether user is a student, number of jobs, number of degrees, friends and followers, total years working and in education |
| Social profile, abstractive | Embeddings (S-BERT, 387-dim vector) of job and education text |
| Re-identification inputs | User name and city, plus the set of cities the user has ordered from |
| Study window | November 2021 to April 2022; first 5 months train, last 1 month test |
| Final dataset | 6,881 orders by 2,121 unique users; 2,201 (32%) orders were RTO |

Only users who explicitly made name and city public were used; the paper states compliance with platform privacy policies.

### 4. Data Science Approach
Documented pipeline:
1. Ground truth from past orders; the 5% randomised, un-intervened control set is used so labels are not contaminated by earlier models' interventions. COD orders only.
2. Candidate extraction: query "<user name> <city name>" on a professional-network search and a web search engine; top 10 results are candidate profiles. Candidates were found for 1,091 of 2,121 users.
3. Re-identification: reject candidates whose name does not match; then compute a match score = share of locations in the candidate's profile that are also in the user's order-city set, with fuzzy matching (e.g., Delhi vs New Delhi, Bangalore vs Bengaluru). A profile is a match if the score exceeds a threshold (results reported at 0.6). Users fall into No match / Exact match / Multiple matches; no-match users are dropped from modelling; for multiple matches the feature values are averaged.
4. Feature construction (three groups above) and model training.
5. Classification threshold chosen to maximise "Goodness" subject to a cap on false-positive rate (cap set by product requirement; value ND), because a high FPR means false interventions that hurt customer experience.

Re-identification outcomes (Table 1): at threshold 0.6, Exact match 68.92%, Multiple 17.68%, No match 13.40%; at threshold 1.0 No match rises to 40.02%.

### 5. Statistical Analysis
- Randomised holdout (5% of orders with no intervention) to obtain unbiased outcome labels. This is the main statistical-design point documented.
- Time-based split (5 months train / 1 month test) rather than random split.
- Fuzzy string matching and a threshold-based match score for entity resolution; sensitivity to the threshold was checked ("results for varying values ... were consistent", not shown).
- No hypothesis tests, confidence intervals or significance values are reported (ND).

### 6. Machine Learning
- **Model(s):** Random Forest, XGBoost, TabNet (tabular deep net; tabular features encoded by TabNet, concatenated with S-BERT embeddings, then feed-forward layers). Random Forest performed best; the paper notes deep models did worse, consistent with the literature on tabular data.
- **Target variable:** Order becomes RTO (binary), COD orders in the control set.
- **Features:** See section 3. For tree models, the 387-dim S-BERT vectors for job and education were reduced with UMAP (output dimension treated as a hyperparameter) to limit overfitting.
- **Validation approach:** 5-month train / 1-month test; hyperparameters tuned by random search with 4-fold cross-validation on the training data.
- **Metrics:** Precision, recall, and a custom "Goodness" in basis points, described as reflecting "the reduction in the ratio of RTO orders after being evaluated by the model" (formula in the paper's equation 2). Test results, Random Forest (Table 2):

| Features | Precision % | Recall % | Goodness (bps) |
|---|---|---|---|
| Past trends | 85.7 | 40.3 | 1,005.7 |
| + Social quantitative | 85.7 | 50.4 | 1,305.6 |
| + Social quantitative + abstractive | 88.8 | 60.2 | 1,633.7 |

XGBoost with all features: precision 86.8, recall 44.5, Goodness 1,129.4. TabNet with all features: precision 64.2, recall 15.1, Goodness 320.0 (TabNet with past trends only: 82.4 / 39.4 / 977.0).

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Models | Random Forest, XGBoost, TabNet |
| Text embeddings | S-BERT (387-dim), UMAP for dimensionality reduction |
| Data sources | Internal order data; public professional-network profiles; search engines |
| Serving / infra | ND (paper only says a real-time checkout system is needed) |

### 8. Business Decision
The paper says the prediction, "combined with other attributes like customer history, and available stock of the product", can be used to "initiate precautionary measures that can mitigate RTO risk". The specific measure (block COD, require prepayment, extra verification, etc.) is ND. The decision threshold is set to maximise Goodness under a fixed false-positive-rate cap.

### 9. Business Impact
- "3.1% increase in precision and 19.9% increase in recall" (authors' wording; the table shows these are percentage-point gains: 85.7 to 88.8 precision and 40.3 to 60.2 recall for Random Forest).
- Goodness rises by 628 bps (1,005.7 to 1,633.7): +300 bps from quantitative social features, +328 bps from abstractive embeddings.
- Authors' claim: "every 1% increase in the recall can add six figures to the bottom-line revenue for a large-scale organization" (no currency or basis given, not independently verified).
- Production deployment, A/B test result and rupee savings: ND.
- Caveats stated by the authors: India-only data; social re-identification covered only a subset of users (1,091 of 2,121 had candidate profiles); privacy considerations.

### 10. What a Data Scientist Can Learn *(interpretation)*
- The 5% no-intervention holdout is the key design idea: when earlier models already block or alter orders, outcomes are censored, and a random holdout is the clean way to get labels. Interviewers like this.
- Report business-aligned metrics (the paper's Goodness at a fixed FPR cap) next to precision and recall.
- The final sample is small (6,881 orders, 32% positive) because of the privacy filter and the control-set restriction, so the lift is a proof of concept, not a production estimate. A candid answer would say so.
- Tree ensembles beat TabNet on this tabular problem; do not default to deep learning.
- Using social-profile data raises fairness and privacy questions (proxy for socio-economic status); be ready to discuss.

### 11. Source Links
- https://precog.iiit.ac.in/pubs/Flipkart_RTO_WWW_workshop_Cameraready.pdf — "Social Re-Identification Assisted RTO Detection for E-Commerce" (WWW '23 Companion, 2023; fetched PDF)
- https://medianama.com/2025/12/223-meesho-ipo-rhp-filing-5421-crore/ — MediaNama on Meesho RHP, COD share (December 2025; fetched)
- https://hackernoon.com/using-data-science-to-deal-with-rtos — Shaurya Uppal, "Using data science to deal with RTOs" (August 22, 2022; fetched; generic practitioner article, employer not named, no measured results; background only, not used for any figure in sections 1-9)

---

## Case R2 — Reducing size-related returns with a size and fit predictor that reads customer reviews
**Company:** Flipkart (substituted for Myntra; see below)
**Industry:** Fashion ecommerce (India)
**Business Area:** Returns reduction, product-page size and fit recommendation
**Problem Type:** Three-class classification (small / fit / large) with cold-start handling and text embeddings
**Evidence Level:** Strong (C) for the method (SIGIR eCom '22 workshop paper, three Flipkart authors, four category datasets); no business-impact figure is published, so impact is ND.
**Primary Sources:** Oishik Chatterjee, Jaidam Ram Tej, Narendra Varma Dasaraju (Flipkart Internet Pvt Ltd), "Incorporating Customer Reviews in Size and Fit Recommendation systems for Fashion E-Commerce", SIGIR eCom'22, July 2022, arXiv:2208.06261.

**Substitution note:** I could not find a Myntra, Ajio or Nykaa Fashion paper or engineering post with method detail on size recommendation. Search results only surfaced 2016 press about Myntra's uniform size chart and a job listing; I did not read those pages in full, so nothing from them is used as fact here. Flipkart's paper is a better-documented case of the same problem type.

### 1. Business Problem
The paper states "there are a lot of size related returns and refunds in e-fashion domain which causes inconvenience to the customers as well as costs the company", and cites "Up to 40% of online fashion products are returned" (from a third-party reference in the paper, not Flipkart's own number). It notes that symbolic sizes (S/M/L) vary between brands and sometimes within a brand, and that size guides are brand-level and cumbersome.

### 2. Business Question
Given a customer, a product and the reviews on that product's page, will the product be small, true-to-size, or large for this customer, so the platform can show "buy one size larger / smaller" tips? Can review text improve on a model that uses only customer and product features, especially for new customers (cold start)?

### 3. Data Available
| Data | Description |
|---|---|
| Product details | Numeric (e.g., size) and categorical (brand, fabric etc.) product features |
| Purchase and returns data | Each purchase labelled "small" or "large" if returned with that reason code ("Size smaller" / "Size larger"), otherwise "fit" |
| Customer features | Continuous and categorical (specific fields ND) |
| Customer reviews | Text reviews on the product page; zero, one or many per product |
| Public dataset | ModCloth fit reviews, used to train BERT where labelled reviews are not available |

Dataset scale (Table 1; "one of the largest e-commerce platforms"; Flipkart named in author affiliations):

| Category | Customers | Products | % Small | % Large |
|---|---|---|---|---|
| Women Jacket | 14,94,713 (1.49M) | 47,040 | 4.52% | 1.68% |
| Women Kurta and Kurti | 61,53,598 (6.15M) | 1,20,425 | 2.40% | 1.30% |
| Men's Jean | 31,72,637 (3.17M) | 47,140 | 2.92% | 2.35% |
| Men's Polo T-shirt | 21,18,089 (2.12M) | 47,040 | 3.14% | 2.76% |

(Indian digit grouping as printed in the paper.) Time window of the data: ND.

### 4. Data Science Approach
Documented:
1. Framed as classification P(F | C, P, R) over {small, fit, large}.
2. Three input pathways (product, customer, reviews), each a stack of residual blocks, then a combined pathway ending in softmax. Categorical features go through embedding layers; numeric features are normalised.
3. Each review is embedded with a pre-trained language model; embeddings for a product are averaged; a zero vector is used when no reviews exist.
4. Four language-model variants compared: BERT trained on ModCloth fit classification (BM), BERT fine-tuned on the platform's own review fit classification (BFC), FKBERT (a RoBERTa model pre-trained with masked-language-modelling on platform text: descriptions, reviews, Q&A) (FB), and FKBERT fine-tuned on fit classification (FFC). "Only Reviews" (majority vote of review-level predictions) is also reported.
5. Baseline: SFNet, a deep model using only customer and product features.
6. Because "the dataset is highly skewed towards the fit class", fit instances in training were re-sampled to equal the number of small plus large instances.

### 5. Statistical Analysis
- 80:10:10 train / validation / test split per category.
- Class-imbalance handling by re-sampling the majority class in training.
- Model selection by best validation F1 over up to 100 epochs.
- No significance tests, confidence intervals or variance across seeds are reported (ND). Improvements are single-run relative differences.

### 6. Machine Learning
- **Model(s):** Residual-block neural network with three pathways plus BERT/RoBERTa-style review encoder (768-dim review embedding); baseline SFNet.
- **Target variable:** Three classes: small / fit / large, derived from return reason codes (not returned = fit).
- **Features:** Product features, customer features, averaged review embeddings (details in section 3).
- **Validation approach:** 80:10:10 split; best-validation-F1 epoch; Adam, learning rate 0.01, batch size 2,048; BERT trained with AdamW at 2e-5.
- **Metrics:** Macro F1. Baseline SFNet macro F1: Women Jacket 38.26, Women Kurta/Kurti 35.6, Men's Jean 37.19, Men's Polo 37.2. Best model (FKBERT-FC) improvement over baseline: +4.31%, +3.09%, +1.37%, +2.42% respectively (relative improvements as presented in the table). "Only Reviews" was worse than baseline by 8.13% to 15.68%.

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Language models | BERT, RoBERTa-based "FKBERT" |
| Baseline | SFNet |
| Optimisers | Adam, AdamW |
| Public data | ModCloth |
| Serving, A/B testing, infra | ND |

### 8. Business Decision
Output is intended as a product-page tip: "buy one size large", "buy one size small", or no recommendation when the product is true to size. Whether and how this was launched, and the thresholds used, are ND.

### 9. Business Impact
- Paper's claim: "an improvement of 1.37% - 4.31% in F1 (macro) score over the baseline across the 4 different datasets"; transfer from the public ModCloth data alone gives "0.43% - 1.94% improvement".
- Reduction in return rate, return cost or conversion uplift: ND (not measured in the paper).

### 10. What a Data Scientist Can Learn *(interpretation)*
- Return reason codes act as free labels; the labelling rule (not returned = fit) is noisy because non-returners may still have been unhappy. Interviewers often probe this label noise.
- Macro F1 around 35 to 38 shows the task is hard and highly imbalanced (small and large are 1.3% to 4.5% of instances each). Accuracy would be meaningless here.
- Gains are modest (1% to 4% relative); a good answer discusses whether that is worth the engineering and how it would be tested (A/B test on return rate per category).
- Cold start is the real motivation for text features; discuss alternatives (brand-level embeddings, measurement questionnaires).

### 11. Source Links
- https://arxiv.org/abs/2208.06261 and https://arxiv.org/pdf/2208.06261 — Chatterjee, Tej, Dasaraju, "Incorporating Customer Reviews in Size and Fit Recommendation systems for Fashion E-Commerce" (arXiv August 11, 2022; SIGIR eCom'22, July 15, 2022; fetched PDF)

---

## Case R3 — Detecting rating fraud (fake and defaming reviews) on a marketplace with a Bayesian anomaly model (BIRDNEST)
**Company:** Flipkart (with Carnegie Mellon and other academic collaborators)
**Industry:** Ecommerce marketplace (India)
**Business Area:** Trust and safety, review integrity, seller fraud
**Problem Type:** Unsupervised anomaly detection / fraud ranking, validated by manual labelling
**Evidence Level:** Strong (C) — arXiv paper with two Flipkart-linked co-authors (Mohit Kumar, Disha Makhija; the paper's affiliation markers were not cleanly readable, but the paper reports Flipkart's own labelling), real Flipkart data, expert-labelled precision; dated (2015-16) and no production-impact figure.
**Primary Sources:** Bryan Hooi, Neil Shah, Alex Beutel, Stephan Gunnemann, Leman Akoglu, Mohit Kumar, Disha Makhija, Christos Faloutsos, "BIRDNEST: Bayesian Inference for Ratings-Fraud Detection", arXiv:1511.06030 (v1 November 19, 2015; v2 March 7, 2016).

Note: this paper does not cover refund/return abuse or promo abuse. For those, only an unofficial write-up of Swiggy's support flow (see R5) mentions refund-abuse scoring; no Flipkart/Amazon India return-abuse method with detail was found.

### 1. Business Problem
"Review fraud is a pervasive problem in online commerce, in which fraudulent sellers write or purchase fake reviews to manipulate perception of their products and services." Prior detectors rely either on bursts in time or on skewed rating distributions; either signal may be absent in a given dataset.

### 2. Business Question
Can a single principled model combine temporal-burst and rating-distribution signals to rank users by how suspicious they are, at scale, with no labelled training data, so that investigators review the most suspicious accounts first?

### 3. Data Available
| Data | Description |
|---|---|
| Flipkart ratings | 1.1M users, 550K products, 3.3M ratings (1 to 5 stars) with timestamps (Table 2 of paper) |
| Software-app reviews (SWM) | 0.97M users, 15K products, 1.1M ratings; crawled app reviews used as a second dataset |
| Expert labels (Flipkart) | Top 250 flagged users were investigated and hand-labelled by Flipkart |

Features per user: the count of each star rating, and the count of inter-rating time gaps in log-scale buckets (time since the user's previous rating, bucketed by integer part of the log, with base chosen to give close to 20 buckets).

### 4. Data Science Approach
1. Represent each user by two count vectors: ratings by star level and time-gap bucket counts.
2. BIRD model: users belong to one of K clusters (a mixture); each cluster has Dirichlet parameters; each user's rating distribution and temporal distribution are drawn from the cluster's Dirichlet prior; observed counts are multinomial. Parameters are fit by maximum likelihood (fixed-point iterations for the Dirichlet-multinomial).
3. Posterior for each user's true rating and temporal distributions is Dirichlet (conjugate update).
4. NEST suspiciousness metric: the expected "surprise" of a user's posterior under the global fitted distribution, computed separately for ratings and for time gaps, each normalised by its standard deviation across users, then combined so neither dominates.
5. Rank users by NEST; submit the top 250 Flipkart users to Flipkart for manual investigation.
6. Interpretability check on three anonymised real Flipkart users (alice, bob, carol), simulating 10,000 draws from each posterior to show the posterior of the long-run average rating.

Fraud patterns found by Flipkart's domain experts (as reported in the paper): users "spamming 4/5 star ratings to multiple products from a single seller (boosting seller's ratings), or spamming 1/2 star ratings to multiple products from another seller (defaming the competition)."

### 5. Statistical Analysis
- Dirichlet-multinomial mixture model, conjugate Bayesian updating, posterior simulation for interpretability.
- Likelihood-based "expected surprise" score (a Bayesian anomaly score) with standard-deviation normalisation.
- Precision-at-k reported against expert labels (precision 1.0 for the first 50 users).
- Scalability: linear-time algorithm; "running on our 1.1M user, 3.3M ratings dataset in around 2 minutes" on a 2.4 GHz Intel Core i5 MacBook Pro, 16 GB RAM (authors' statement).
- Baseline comparisons beyond the Flipkart evaluation: ND (not extracted).

### 6. Machine Learning
- **Model(s):** BIRD (Bayesian mixture of Dirichlet-multinomials) with NEST score; unsupervised.
- **Target variable:** None at training time (unsupervised). Evaluation target: whether a flagged user was "involved in fraud" per Flipkart labelling.
- **Features:** Star-rating histogram and log-bucketed inter-rating time histogram per user.
- **Validation approach:** Expert manual labelling of the top-250 output; precision@k. No train/test split (unsupervised). Recall and false-negative rate: ND (cannot be computed from top-k labelling alone).
- **Metrics:** Precision at k.

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Implementation | Python; code released by the authors (CMU-hosted archive) |
| Hardware | Single laptop for experiments (see section 5) |
| Production deployment at Flipkart | ND |

### 8. Business Decision
Flipkart investigated and hand-labelled the flagged accounts; what action followed (removal of reviews, account bans, seller penalties) is ND in the paper. The paper only says these are "substantial findings for Flipkart".

### 9. Business Impact
- "the 50 most suspicious users of the Flipkart platform flagged by our algorithm were investigated and all identified as fraudulent by domain experts at Flipkart" (abstract).
- "211 users of the top 250 flagged by BIRDNEST involved in fraud", and the paper's text states "precision of over 84% on the top 250" (211/250 = 84.4%). Authors' claim, validated by Flipkart reviewers; no independent audit.
- Revenue, trust-score or review-removal volume: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Fraud problems rarely have clean labels; an unsupervised score plus a human-in-the-loop review of the top-k, with precision@k as the headline metric, is a realistic design.
- Small-sample users (few ratings) are where Bayesian shrinkage matters: a Dirichlet prior stops one-or-two-rating users from looking extreme. This is a good interview talking point on smoothing versus raw proportions.
- Combining two weak signals (burstiness and skew) by normalising their scales is a general pattern; mention the risk of one signal dominating.
- The result is from 2015-16 data; it says nothing about modern LLM-generated or incentivised reviews.

### 11. Source Links
- https://arxiv.org/abs/1511.06030 — BIRDNEST abstract page (v1 November 19, 2015; v2 March 7, 2016; fetched)
- https://arxiv.org/pdf/1511.06030 — full paper (fetched and text-extracted)

---

## Case R4 — Filling missing product attributes automatically to improve catalogue quality (multimodal generative extraction), with a Flipkart image-similarity service as a supplementary data point
**Company:** Amazon (the paper does not state the India marketplace; see substitution note). Supplementary: Flipkart Trust & Safety (vendor case study).
**Industry:** Ecommerce marketplace (global; India-operating company)
**Business Area:** Catalogue quality, attribute enrichment (search and filters)
**Problem Type:** Information extraction / generative question answering over text and image
**Evidence Level:** Medium (C) — ACL 2023 Industry Track paper by Amazon authors with datasets, metrics and deployment scale; but India-specific deployment is not stated in the paper. The Flipkart supplementary item is D (vendor-authored).
**Primary Sources:** Anant Khandelwal, Happy Mittal, Shreyas Sunil Kulkarni, Deepak Gupta (Amazon), "Large Scale Generative Multimodal Attribute Extraction for E-commerce Attributes", arXiv:2306.00379 (June 1, 2023; ACL 2023 Industry Track). Supplementary: Daniel Azoulai, Qdrant blog, "Building real-time multimodal similarity search in Flipkart Trust & Safety with Qdrant" (January 9, 2026).

**Substitution note:** I found no Flipkart, Myntra or Amazon India engineering post or paper with attribute-extraction or counterfeit-detection method detail that I could fetch and confirm. Meesho's counterfeit-removal claim (about 42 lakh listings) appeared only in a search-result snippet; the Business Standard page returned HTTP 403, so it is not used as fact. The Amazon paper is the best-documented catalogue-quality case found; the paper does not name its marketplace ("a popular e-commerce store") nor say it serves India. Treat India relevance as the problem type, not the site.

### 1. Business Problem
"Sellers rarely specify all attribute values or mistakenly fill incorrect values." Missing or wrong attributes (colour, size, material, sleeve type) hurt catalogue quality and customer experience. Attributes may or may not appear in the text, and may only be inferable from images.

### 2. Business Question
Can one model extract (or infer) attribute values for thousands of product-type and attribute combinations from product text plus image, including values never seen in training and values not written in the text?

### 3. Data Available
| Data | Description |
|---|---|
| Product text | Product-type plus textual description |
| Product images | One image per product, embedded with ResNet-152 |
| Labels | Distant supervision: the abstract says it needs no human labelling (label source detail not extracted) |
| 30PT dataset | 30 product types, 38 unique attributes; 569k train and 84k validation products; test data from two product types, 73k products |
| E-commerce5PT dataset | A second dataset used for F1 comparison (size ND) |

### 4. Data Science Approach
The problem is posed as question answering: question = attribute name; context = product type + text + image; answer = attribute value. Architecture (MXT): T5 encoder-decoder; image embeddings from ResNet-152 fused into T5 text embeddings through a Multimodal Adaptation Gate (MAG); an Xception network gives attribute-aware regional visual embeddings fused via dot-product attention; T5 decoder generates the value. A single model is trained across many product-type/attribute pairs by putting the product type in the input. Compared against NER-MQMRC (extractive) and CMA-CLIP (multimodal classifier). Ablations: single-PT vs multi-PT training, without Xception, without MAG. Zero-shot (unseen value) and value-absent (not in text) inference are demonstrated.

### 5. Statistical Analysis
No hypothesis tests or confidence intervals are documented (ND). Evaluation uses recall at a fixed 90% precision (Recall@90P), on the top-5, top-10 and top-15 attributes by product count, plus ablation comparisons.

### 6. Machine Learning
- **Model(s):** MXT = T5 (t5-base) + MAG + ResNet-152 + Xception.
- **Target variable:** Attribute value (generated text) for a given attribute name.
- **Features:** Product type, text description, image embeddings.
- **Validation approach:** Train/validation/test by product type (test on two held-out product types for the 30PT dataset); trained 20 epochs, batch size 4, 8 V100 GPUs (16 GB).
- **Metrics:** Recall@90P (relative improvement over NER-MQMRC), F1.

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Models | T5-base, ResNet-152, Xception, MAG |
| Training hardware | 8 x NVIDIA V100 (16 GB) |
| Optimiser | Adam |
| Supplementary (Flipkart T&S) | Qdrant vector DB (HNSW), Java gRPC SDK, Prometheus, HBase+LSH (previous system), 2048-dim embeddings from Flipkart models (not named) |

### 8. Business Decision
Extracted values are used to fill catalogue attributes. The paper says models "are being used to extract attributes for over 12000 PT-attributes in a popular e-commerce store, and have extracted more than 150MM attribute values" (introduction); the deployment section says "6 English speaking markets covering >10K PT-attributes" and ">150MM attribute values" (the paper itself gives 12000 and >10K in different places). Confidence thresholds and human review: ND.

Supplementary Flipkart item (vendor-authored, D): Flipkart's Trust & Safety team moved from an HBase plus locality-sensitive-hashing batch system to a Qdrant-based real-time image-similarity service to catch fraud and abuse such as repeat returns and duplicate seller claims. It also supports address clustering for last-mile routing and retrieval for RAG. This is fraud and duplicate-claim matching, not catalogue attribute work.

### 9. Business Impact
- Paper: Recall@90P improvements of "10.16% and 6.9%" over existing state-of-the-art models (abstract). The in-paper table 1 gives gains over NER-MQMRC by attribute group, e.g., CMA-CLIP +1.81% to +6.70% and MXT variants up to +22.33% on the 30PT table. Treat the abstract figures as the headline claim and the table as detail; I did not reconcile the two.
- Scale: >150MM attribute values extracted.
- Effect on conversion, search quality or catalogue completeness rate: ND.
- Flipkart supplementary (Qdrant's narrative, quoting Flipkart engineer Sourabh Sarkar, SDE-III): lookups that "took up to nine hours" now take "under one minute"; no dataset size or methodology; vendor claim.

### 10. What a Data Scientist Can Learn *(interpretation)*
- "Recall at fixed precision" is the natural metric when auto-filling a catalogue: wrong values are costlier than missing ones.
- Distant supervision means label noise from sellers' own entries; interviewers may ask how you would audit it.
- Single multi-task model versus one model per category is a maintenance and monitoring trade-off, explicitly argued in the paper.
- Duplicate and counterfeit detection is usually embedding plus approximate nearest-neighbour search; the speed-up claim in the Flipkart case is about infrastructure, not model accuracy.

### 11. Source Links
- https://arxiv.org/abs/2306.00379 and https://arxiv.org/pdf/2306.00379 — Khandelwal et al., MXT (June 1, 2023; fetched)
- https://qdrant.tech/blog/case-study-flipkart/ — Qdrant, Flipkart Trust & Safety case study (January 9, 2026; fetched; vendor-authored)

---

## Case R5 — Automating food-delivery customer support with LLM agents and measuring containment, latency and CSAT (Zomato Zia and Nugget)
**Company:** Zomato (Eternal group), with Together AI and MongoDB as vendor narrators
**Industry:** Food delivery / quick commerce (India)
**Business Area:** Customer support automation
**Problem Type:** Conversational AI (intent detection, function calling, escalation policy) with operational KPIs
**Evidence Level:** Medium (A/D) — one source is adapted from a named Zomato AI engineer's Fifth Elephant 2024 talk (published by Together AI), the other is a MongoDB vendor case study quoting Zomato; all headline numbers are company-sourced via vendors and unaudited.
**Primary Sources:** Together AI customer story on Zomato's bot "Zia" (adapted from a talk by Yuvraj Gagneja, AI Engineer, Zomato AI, Fifth Elephant 2024; publication date ND); MongoDB blog by Vinay Agarwal, "Zomato Cuts $11M in Support Costs With MongoDB-Powered AI Platform" (March 24, 2026). Context: Swiggy chatbot architecture write-up by Arpit Bhayani (external, not a Swiggy source).

### 1. Business Problem
From the MongoDB case study (vendor-authored): support costs had grown to "US$20M annually"; operations were spread across "10 disparate platforms"; about 60% of tickets were already auto-resolved but Zomato wanted higher customer satisfaction. From the Together AI story: Zomato handles over one million orders a day across India, with meal-time spikes of 10 to 50 times baseline traffic and messages above 1,000 per minute at peak.

### 2. Business Question
Can LLM-based agents resolve a high share of order-related support queries within seconds, with safe escalation to humans, while improving CSAT and cutting cost per ticket?

### 3. Data Available
| Data | Description |
|---|---|
| Real-time order data | Fetched through targeted API calls via function classification and function calling; JSON converted to natural language for the LLM |
| Chat history | Conversation context in the prompt |
| Business guidelines | Policy text included in the final prompt |
| Escalation tags | Escalations carry predefined reasons, checked against order data |
| Ticket metadata and user history | Stored in MongoDB Atlas for Nugget (flexible schema, compound indexes) |

Training/fine-tuning data: ND (the story does not say Zomato fine-tuned any model).

### 4. Data Science Approach
Documented (Together AI story, talk-derived):
- First version used closed-source models including GPT-4; Llama 3 made open-source models competitive enough to switch.
- Larger 70B models for intent detection; smaller 8B models for chat completion.
- Function classification then function calling to pull order data; response composed from data + history + guidelines.
- "With LLM-only escalation decisions, containment swung between 80% and 50% day to day. A policy layer was added to stabilize it." (This is the fetched tool's paraphrase of the page, not a verbatim quote.)
- Evaluation: every system change gets human review, a sample of responses is graded by humans, LLM-as-judge is also used; four metrics tracked: factual consistency, information relevance, guideline compliance, customer pain-point resolution.
- Infrastructure: serverless endpoints for baseline traffic and dedicated endpoints for peaks.

Documented (MongoDB story): Nugget is an in-house "AI-native CX platform" with autonomous multi-channel agents (voice, chat, social, in-app), an agent co-pilot for humans, triage automation and outcome tracking; launched as a multi-tenant enterprise offering in 2025.

Context (not Zomato): an external write-up says Swiggy's bot is a deterministic decision tree built from top contact drivers, with fraud/refund-abuse scoring (refund-to-order ratio, past abuse scores) deciding auto-refund vs proof vs human. That article is by a Razorpay engineer, not Swiggy, and gives no efficacy percentage.

### 5. Statistical Analysis
No statistical tests, A/B design or confidence intervals are documented (ND). The only quality-measurement design point is human sampling plus LLM-as-judge on four rubric metrics.

### 6. Machine Learning
- **Model(s):** Llama family on Together AI (70B for intent detection, 8B for chat completion; earlier GPT-4). Model versions beyond "Llama 3" and fine-tuning: ND.
- **Target variable:** Intent / next action (resolve, call function, escalate) per turn; no explicit supervised label reported.
- **Features:** Prompt context (order data, chat history, guidelines).
- **Validation approach:** Human review of changes; sampled human grading; LLM-as-judge. Offline accuracy numbers: ND.
- **Metrics:** Containment/resolution rate, response latency, CSAT, factual consistency, relevance, guideline compliance, pain-point resolution.

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| LLM serving | Together AI (serverless and dedicated endpoints), Llama models; GPT-4 in v1 |
| Data store | MongoDB Atlas (chosen after testing DynamoDB and DocumentDB, per Zomato via MongoDB) |
| Platform | Nugget (in-house); function calling to order APIs |
| Evaluation | Human review, LLM-as-judge |

### 8. Business Decision
Replace most first-line support with LLM agents; keep humans via escalation and an agent co-pilot; add a policy layer to stabilise escalation decisions; offer the platform to other enterprises as Nugget.

### 9. Business Impact (all company-sourced via vendors, unaudited)
- Together AI story: CSAT "roughly doubled (2x)", no before/after scores; average response time fell 75% to under 10 seconds; target sub-10-second; on Mother's Day Zia "served over 80,000 customers" with peaks above 1,000 messages per minute; no final containment percentage; no cost figure.
- MongoDB story (as of January 2026): "more than 15 million" conversations per month; "85%" average query resolution rate; human-agent productivity up 40%; support cost down from US$20M to "$9 million annually" ("reduce support costs by 55%", headline $11M).
- Conflict note: a search result indicated Nugget's own case study reports a 25% CSAT improvement; I did not fetch it, so no figure is taken from it. Treat 2x CSAT as unreconciled.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Define resolution/containment precisely (resolved vs deflected vs abandoned); a bot can show high "resolution" while users give up, as press complaints about Swiggy and Zomato bots suggest (search-result summary only, not read in full).
- LLM-only escalation decisions were unstable (80% vs 50% daily containment); a deterministic policy layer on top of the model is a transferable design lesson.
- Report latency and cost alongside quality; model-size routing (70B for intent, 8B for generation) is a standard cost lever.
- Without a randomised holdout, a before/after CSAT comparison is confounded; ask what the control was.

### 11. Source Links
- https://www.together.ai/customers/zomato — Together AI, Zomato support bot Zia (adapted from Fifth Elephant 2024 talk; date ND; fetched; vendor-published)
- https://www.mongodb.com/company/blog/innovation/zomato-ai-solution-nugget-reduces-support-costs — MongoDB, Zomato Nugget (March 24, 2026; fetched; vendor-authored)
- https://arpitbhayani.me/videos/swiggy-chatbot-system-design/ — Arpit Bhayani, Swiggy chatbot design (date ND; fetched; external analysis, not Swiggy)
- https://arxiv.org/html/2507.05788v1 — Rajasekar et al. (Flipkart US R&D Center), "Flippi: End To End GenAI Assistant for E-Commerce" (July 8, 2025; fetched). Pre-purchase shopping assistant: 8-intent DistilBERT router with test accuracy 94.89% (final coarse intent accuracy "approximately 97%"); post-purchase issues are only routed to existing support channels. Not a support-automation case; listed as a Flipkart alternative considered.

---

## Case R6 — Marketplace winner selection (Buy Box) and seller-quality signals: an external audit of Amazon.in and other Amazon sites
**Company:** Amazon (India marketplace, plus US, Germany, France), studied by Indian and German academics
**Industry:** Ecommerce marketplace
**Business Area:** Seller ranking, default-offer (Buy Box) selection, seller performance metrics
**Problem Type:** Algorithm audit (choice architecture), with survey experiments and a surrogate feature-importance model
**Evidence Level:** Medium (B) — peer-reviewed academic audit (CSCW 2024) of the actual Amazon.in Buy Box outcomes; it does not disclose Amazon's algorithm (the authors say they have only partial knowledge of its features). No Flipkart or Meesho seller-scoring method with detail was found.
**Primary Sources:** Abhisek Dash, Abhijnan Chakraborty, Saptarshi Ghosh, Animesh Mukherjee, Krishna P. Gummadi, "Investigating Nudges toward Related Sellers on E-commerce Marketplaces: A Case Study on Amazon", arXiv:2407.01732 (July 1, 2024), ACM CSCW 2024.

**Substitution note:** Flipkart seller tiers (Bronze/Silver/Gold) and Meesho supplier ranking appeared only in seller-service blogs and unofficial guides in search results; none was fetched, and no Flipkart/Meesho paper or engineering post was found. The Meesho RHP coverage (MediaNama) only says Meesho delisted over 2 lakh products in September-November 2023 for poor quality and lists seller quality as a risk. CCI Director General findings on preferred sellers (reported by Reuters via secondary outlets) were seen only in search summaries, not fetched, and are not used as fact. Everything below is about Amazon's observable behaviour, not Amazon's internal model.

### 1. Business Problem
"When multiple sellers offer to sell the same product, the marketplace helps a customer in selecting an offer ... through a default offer selection algorithm" (the Buy Box) and by showing seller performance metrics. The paper asks whether this choice architecture nudges customers toward "Related Sellers": Amazon itself (US/DE/FR), special merchants (Cloudtail India and Appario Retail in India), and sellers using Amazon's fulfilment (FBA). Note: Cloudtail stopped selling on Amazon in 2022; data were collected while it was active.

### 2. Business Question
RQ1: how often do Amazon/related sellers win the Buy Box, and do the algorithm's choices match what customers would pick when shown all offers? RQ2: which seller features drive customer choice? RQ3: how do Amazon's review strike-through policies affect reported seller metrics, and how do customers react to corrected metrics?

### 3. Data Available
| Data | Description |
|---|---|
| Buy Box competitions | Scraped from Amazon.in, .com, .de, .fr: 100 most-searched keywords, product pages followed from search results, data collected over two weeks; each competition is a (product, timestamp) pair |
| India dataset size | 20,553 competitions, 2,766 distinct sellers (Table 3) |
| Seller feedback | Feedback for 1,000 active sellers across the four marketplaces, to recompute metrics including struck-through reviews |
| Survey 1 | 200 Prolific participants (50 per country, approval rate 98% or higher); 60 products (15 per marketplace) where special merchants won the Buy Box without the lowest price; top-4 offers shown; India: 750 evaluations |
| Survey 2 | 100 Prolific participants on understanding and fairness of strike-through |
| Survey 3 | 50 Indian participants per treatment setting (control and three treatments) |

### 4. Data Science Approach
1. Scrape Buy Box outcomes over time and compute how often Amazon or its special merchants win ("% Buy Box won"), and how often they win "out of position" (when not the lowest-price offer).
2. Survey 1: show people the top-4 offers with all features and record first-preference votes; compare with the algorithm's winner.
3. Fit a random forest regression on first-preference votes to rank feature importance (price, delivery option, average rating, percentage positive feedback, number of ratings).
4. Recompute seller metrics from raw feedback including reviews that Amazon struck through; compare with Amazon's reported metrics.
5. Survey 3 treatments (India): (T1) hide number of ratings, (T2) show rectified metrics without number of ratings, (T3) show rectified metrics with number of ratings; compare first-preference shares with control.

### 5. Statistical Analysis
Documented: comparison of proportions across control and treatment survey arms (first-preference vote shares); descriptive distributions of seller metrics (box plots) with and without struck-through reviews; counterfactual survey design (treatment arms). Formal hypothesis tests and p-values: not extracted (ND).

### 6. Machine Learning
- **Model(s):** Random forest regression as a descriptive surrogate of respondent choices (not Amazon's algorithm).
- **Target variable:** Respondent first-preference vote.
- **Features:** Relative price, delivery option, average rating, percentage positive feedback, number of ratings.
- **Validation approach:** ND (used for feature-importance ranking, not prediction).
- **Metrics:** Feature-importance ranking. Amazon's actual Buy Box model, features and metrics: ND (proprietary; the authors state partial knowledge only).

### 7. Tools & Technology
| Layer | Documented |
|---|---|
| Data collection | Custom web scraper |
| Surveys | Prolific crowdsourcing platform |
| Modelling | Random forest regression (library ND) |

### 8. Business Decision
Not a company decision; this is an external audit. The documented platform design is: default offer chosen by a proprietary algorithm; offer listing page sorted by price plus delivery charge; seller metrics shown (average rating, percentage positive feedback over 12 months, lifetime number of ratings); a policy allowing Amazon to strike through some negative feedback for related (Amazon-fulfilled) sellers. The authors raise fairness concerns; Amazon "has consistently denied the presence of any systemic preferential treatments" (as the paper reports).

### 9. Business Impact
These are audit findings, not company impact:
- Buy Box win rate of Amazon and special merchants (Table 4): India 87.74% (29.15% out of position), USA 86.12% (26.39%), Germany 85.35% (13.91%), France 79.98% (12.45%).
- India survey: of 750 evaluations, 407 (about 54%) gave first preference to the special merchants, whereas they won the Buy Box in nearly 90% of competitions.
- India, strike-through: 74.13% of low-rated reviews for Amazon-fulfilled sellers were struck through (97,603 of 131,664). Example: Appario Retail's reported positive feedback of 87% falls to 61% when struck-through reviews are included.
- India treatments: special-merchant first-preference share fell from about 54% (control) to 14.5% when number of ratings was hidden (T1), 6.93% with rectified metrics and no number of ratings (T2), and 28.53% with rectified metrics plus number of ratings (T3). Abstract: preference for related sellers is "almost halved" with rectified metrics.
- Number of ratings was the most influential feature in India (random-forest ranking), possibly reflecting scale rather than service quality (authors' interpretation).
- Seller conversion, GMV or return-rate effects of the Buy Box: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
- Black-box audits can still be rigorous: scrape outcomes, build counterfactual surveys, and fit a surrogate model to learn which features matter.
- Un-normalised features (lifetime number of ratings) favour incumbents; a well-designed seller score should normalise for scale and use recent, outcome-based metrics (late shipment, cancellation, return and defect rates). This is a design inference, not something this paper tests.
- Metric integrity matters: if bad outcomes are filtered from the metric, the score stops measuring quality.
- Winner-selection is a ranking problem with fairness constraints and exploration (rotation among eligible sellers); the paper raises skewed winner distribution as a concern.

### 11. Source Links
- https://arxiv.org/abs/2407.01732 and https://arxiv.org/pdf/2407.01732 — Dash et al., "Investigating Nudges toward Related Sellers on E-commerce Marketplaces: A Case Study on Amazon" (July 1, 2024; CSCW 2024; fetched PDF)
- https://medianama.com/2025/12/223-meesho-ipo-rhp-filing-5421-crore/ — Meesho RHP coverage, 2 lakh products delisted for quality (December 2025; fetched)

---

## Notes for the notebook author

### R1 — COD / RTO prediction
**(a) Calibration facts**
- RTO rate in the Flipkart COD control sample: 32% (2,201 of 6,881 orders), from a deliberately filtered sample, so do not treat it as the platform-wide RTO rate (Hitkul et al., 2023).
- Random Forest, past-trend features only: precision 85.7%, recall 40.3%; with social features: precision 88.8%, recall 60.2%; Goodness 1,005.7 to 1,633.7 bps.
- TabNet underperforms trees (precision 64.2%, recall 15.1% with all features).
- Meesho COD share of orders: 72% (six months to September 2025), 77% FY25, 85% FY24 (RHP via MediaNama).
- Design: 5% random no-intervention holdout; 5 months train / 1 month test; features are RTO ratios over 3 months and 1 year by user, product, seller, category, pin code, city; hour and weekday.
- Practitioner figures (HackerNoon, unverified, no employer named): RTO "more than 30% of orders"; INR 100 to 200 cost per RTO. Use only as loose assumptions and label them so.

**(b) Techniques an interviewer expects**
Logistic regression and gradient boosting (XGBoost/LightGBM) on imbalanced data; class weights or resampling; smoothed target-encoding of high-cardinality geography (pin code); time-based validation; precision-recall curves, PR-AUC, recall at a fixed false-positive rate; cost-sensitive threshold using cost of RTO versus lost sale; calibration; randomised holdout to measure the causal impact of blocking COD; fairness and proxy-variable discussion (pin code).

**(c) Prevalence:** very common (COD is 72% of Meesho orders; every COD-heavy Indian platform and logistics aggregator faces it).

### R2 — Size and fit / returns
**(a) Calibration facts**
- Class imbalance: "small" 2.40% to 4.52% and "large" 1.30% to 2.76% of purchase instances across four categories (Flipkart paper); "fit" is the rest.
- Baseline macro F1 about 35.6 to 38.3; best review-augmented model +1.37% to +4.31% relative.
- Category scale: 47K to 120K products and 1.5M to 6.2M customers per category.
- Labelling rule: return reason code "size smaller/larger" gives small/large; not returned gives fit.
- "Up to 40% of online fashion products are returned" (cited by the paper from a third-party source, not Flipkart data).
- Myntra-specific numbers (return rates, size-chart effect) were not verified from a fetched page; do not hardcode them.

**(b) Techniques an interviewer expects**
Multiclass classification with imbalance handling (class weights, resampling, macro F1, per-class recall); collaborative filtering and latent-factor / hierarchical Bayesian size models; cold-start strategies (content features, brand-level priors); text embeddings from reviews; calibration; A/B test on return rate and conversion; return-propensity models; measuring cannibalisation (a recommended size change may shift returns from "too small" to "too large").

**(c) Prevalence:** very common in fashion (Myntra, Ajio, Flipkart Fashion, Nykaa Fashion, Meesho); less so outside apparel and footwear.

### R3 — Review and seller fraud
**(a) Calibration facts**
- Flipkart ratings dataset: 1.1M users, 550K products, 3.3M ratings (BIRDNEST paper, Table 2).
- Top 50 flagged users: 100% judged fraudulent; top 250: 211 fraudulent (84.4% precision); precision@k is highest at small k.
- Observed fraud patterns: 4/5-star spam to many products of one seller (boosting) and 1/2-star spam to a competitor's products (defaming).
- Time-gap features bucketed on a log scale into about 20 buckets; star levels s = 5.
- Runtime claim: about 2 minutes on a laptop for 1.1M users / 3.3M ratings.

**(b) Techniques an interviewer expects**
Anomaly detection (isolation forest, one-class models, density-based), Bayesian smoothing of rating distributions (Dirichlet-multinomial, Beta-binomial), burst detection on timestamps, graph methods (dense-subgraph / lockstep behaviour), supervised classifiers when labels exist (severe imbalance, PU-learning caveats), text-based fake-review classifiers, precision@k and review-capacity-based evaluation, active learning with investigator feedback. Return and promo-abuse variants: user-level refund-to-order ratios, device/address linkage graphs, rules plus model scores.

**(c) Prevalence:** very common (every marketplace and food-delivery platform runs review, seller and refund/promo abuse detection), but public method detail is scarce.

### R4 — Catalogue quality
**(a) Calibration facts**
- MXT (Amazon): single model for more than 10,000 to 12,000 product-type/attribute pairs; more than 150MM attribute values extracted; Recall@90P improvements quoted as 10.16% and 6.9% over prior models.
- 30PT dataset: 30 product types, 38 attributes, 569k train and 84k validation products, 73k test products.
- Flipkart Trust & Safety (vendor-authored): similarity lookups from "up to nine hours" to "under one minute"; 2048-dim embeddings.
- India relevance of the Amazon paper is not stated; do not label the simulation as "Amazon India".

**(b) Techniques an interviewer expects**
NER / sequence tagging and QA-style extraction; seq2seq (T5) generative extraction; multimodal fusion (CLIP-style image-text embeddings); embeddings plus approximate nearest-neighbour search (HNSW, LSH) for duplicate and counterfeit detection; product matching and entity resolution (blocking plus pairwise classifier); recall at fixed precision; weak/distant supervision; active learning and human review loops; image-quality and attribute-completeness scoring.

**(c) Prevalence:** very common (catalogue quality is a core problem for every marketplace, especially with low-quality seller-supplied listings), though public India-specific method detail is limited.

### R5 — Customer-support automation
**(a) Calibration facts**
- Zomato (company data via MongoDB, January 2026): more than 15 million conversations a month; average resolution rate 85%; agent productivity +40%; support cost US$20M to $9M; about 60% of tickets auto-resolved before Nugget.
- Zia (Together AI story from a 2024 talk): over one million orders a day; peaks above 1,000 messages per minute; 10x to 50x meal-time spikes; response time down 75% to under 10 seconds; CSAT "roughly doubled".
- LLM-only escalation made daily containment swing between 80% and 50%.
- Flipkart Flippi: coarse intent model on 8 classes, DistilBERT accuracy 94.89%, macro F1 0.8204 for detailed intents, lowest-F1 intent 0.5882 (arXiv 2507.05788; shopping assistant, not support).
- Swiggy: public detail is only an external write-up (decision tree, "Bot Efficacy" north-star metric; no percentage).

**(b) Techniques an interviewer expects**
Intent classification and contact-reason taxonomy (TF-IDF/logistic regression baseline, BERT fine-tuning), confusion matrix and per-class F1 for rare intents, retrieval-augmented generation, function calling to order systems, containment / deflection / resolution definitions, escalation policy and threshold tuning, CSAT analysis (small, biased response samples), A/B testing against a human-only flow, LLM-as-judge with human calibration, cost per ticket analysis, queueing and peak-load planning.

**(c) Prevalence:** very common (every food-delivery, quick-commerce and marketplace player runs support automation), though public evidence is mostly vendor- or company-sourced.

### R6 — Seller quality and Buy Box
**(a) Calibration facts**
- Amazon.in: special merchants won the Buy Box in 87.74% of competitions they entered, and won out of position (not lowest price) 29.15% of the time; dataset 20,553 competitions, 2,766 sellers.
- Survey (India, 750 evaluations): 407 (about 54%) first-preference votes for special merchants versus about 90% Buy Box wins.
- Strike-through: 74.13% of low-rated reviews for Amazon-fulfilled sellers (97,603 of 131,664); Appario positive feedback 87% reported versus 61% recomputed.
- Treatment shares: 14.5% (no number of ratings), 6.93% (rectified, no number of ratings), 28.53% (rectified with number of ratings).
- Flipkart/Meesho seller-score formulas are not public in anything fetched; unofficial seller-guide claims (tiers, cancellation thresholds) are unverified and should not be hardcoded.

**(b) Techniques an interviewer expects**
Learning to rank (pointwise/pairwise/listwise), multi-objective ranking (conversion, margin, customer experience), seller scoring from late-shipment, cancellation, return, defect and rating metrics with Bayesian shrinkage for new sellers, bandits / exploration for new-seller cold start, fairness and rotation across eligible sellers, causal evaluation (interleaving, A/B), surrogate-model and feature-importance auditing, price-competitiveness features (relative to a reference price).

**(c) Prevalence:** common (all multi-seller marketplaces have some seller scoring and offer selection; Buy Box-style single-winner selection is most visible on Amazon, while Flipkart and Meesho details are largely undisclosed).
