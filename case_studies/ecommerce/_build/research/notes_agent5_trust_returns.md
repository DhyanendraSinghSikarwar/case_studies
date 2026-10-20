

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
