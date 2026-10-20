---

# Case Study 16 — Dish Search and Query Understanding (Swiggy) · `cs16_dish_search_ranking.ipynb`

## D-16-01: Data source — synthetic sessions with hidden graded relevance and click model

- Date: 2026-10-20
- Case: 16
- Context / question: We need search logs with misspellings, availability gaps, relevance labels and a click model to compare retrieval and ranking methods.
- Options considered: public query logs (AOL, MS MARCO, Amazon ESCI; none Indian, no transliteration noise, no known click model); synthetic data.
- Decision: 48,000 sessions, 120 dish families, 1,200 menu names, 19,600 listings in 5 areas, 33% misspelled dish-like queries, hidden relevance 0 to 3.
- Why: Editorial NDCG, click replay and an online twin can only be compared when the truth is known.
- Assumption checks / evidence: Production returns nothing for 9.9% of sessions; 4.2% of clean vs 20.8% of misspelled dish queries.
- Impact if wrong / mitigation: Noise model, availability and click model are assumed; rebuild the test set from real logs with human labels.

## D-16-02: Evaluation — time split, graded NDCG@10 plus MRR and P@1

- Date: 2026-10-20
- Case: 16
- Context / question: Which metrics and split give a trustworthy comparison?
- Options considered: random split; time split; binary vs graded relevance.
- Decision: Train days 0 to 34, test days 53 to 59 (5,548 sessions); NDCG@10 with gain 2^rel − 1 as primary; MRR and P@1 on answerable sessions.
- Why: A later week mirrors Swiggy's validation; graded NDCG values close alternatives for unavailable dishes.
- Assumption checks / evidence: MRR and P@1 rank the classifier below fuzzy matching (0.788 vs 0.840 MRR) while NDCG ranks it above (0.878 vs 0.776).
- Impact if wrong / mitigation: Choose the metric to match the product question; report several.

## D-16-03: Replace word matching with character n-grams plus a learned query classifier

- Date: 2026-10-20
- Case: 16
- Context / question: How do we handle non-standard spellings?
- Options considered: exact match; ES-style fuzzy match; trigram cosine; query classifier; blend; LTR.
- Decision: Blend of fuzzy, trigram and classifier scores as the retrieval layer.
- Why: NDCG@10 0.893 vs 0.776 (fuzzy) and 0.673 (exact); zero-result 0% vs 10.8%; misspelled queries 0.914 vs 0.698.
- Assumption checks / evidence: Difference-in-differences +0.195 for the classifier (CI 0.168 to 0.222); Davies-Bouldin 0.36 vs 0.89 for trigram vs word embeddings.
- Impact if wrong / mitigation: The spelling dictionary used a subset of the true rules; refresh it from real logs.

## D-16-04: Add a click-trained ranker behind an A/B test

- Date: 2026-10-20
- Case: 16
- Context / question: Is learning to rank worth the complexity?
- Options considered: blend only; LTR on clicks; LTR with IPW; LTR on production logs only.
- Decision: Test LTR on clicks (13 features, gradient boosting) against the blend.
- Why: NDCG@10 0.900 vs 0.893 (+0.007, CI 0.003 to 0.011); NDCG@1 0.914 vs 0.898; effect size small (d_z 0.04).
- Assumption checks / evidence: IPW 0.896 and production-logs-only 0.896: close, since the trial arm covers the blind spots here.
- Impact if wrong / mitigation: A small gain needs a large test (about 35,000 sessions for 0.005 NDCG).

## D-16-05: Keep an exploration arm and de-bias clicks

- Date: 2026-10-20
- Case: 16
- Context / question: Can clicks from the old system train the next one?
- Options considered: production logs only; IPW; a trial arm of 10% traffic.
- Decision: Keep 10% of traffic on an alternative retriever and weight clicks by position propensity when the arms are small.
- Why: Odds of a click at position 10 are 0.14 of position 1 for the same relevance; 88.2% of shown exact-dish listings are not clicked.
- Assumption checks / evidence: Production-only training lost 0.004 NDCG here; the loss would be larger with weaker retrieval.
- Impact if wrong / mitigation: Propensities are known only in simulation; estimate by randomised swaps in real data.

## D-16-06: Do not use click replay as a decision metric

- Date: 2026-10-20
- Case: 16
- Context / question: Can logged orders judge new rankers offline?
- Options considered: editorial NDCG; click replay; online twin.
- Decision: Use editorial NDCG as the offline gate and a live A/B as the final test.
- Why: Replay Spearman with editorial NDCG -0.31 and with the twin -0.52; editorial vs twin +0.95 (p = 0.0003).
- Assumption checks / evidence: Replay ranks fuzzy lexical (the logging system) first and the classifier last.
- Impact if wrong / mitigation: With 8 methods the replay correlations are not significant; the direction is the warning.

## D-16-07: Show alternatives for unavailable dishes

- Date: 2026-10-20
- Case: 16
- Context / question: What should the customer see when the dish is not nearby?
- Options considered: empty page; fuzzy results; family and cluster alternatives.
- Decision: Show same-family and same-cluster alternatives, labelled.
- Why: For 1,026 test sessions with no exact dish, NDCG@10 is 0.505 (fuzzy) vs 0.975 (classifier); 98.4% of its top 10 in the intended category.
- Assumption checks / evidence: 21% of dish-like sessions have no exact dish locally in our simulation.
- Impact if wrong / mitigation: Availability rates are assumed; monitor orders per search on these sessions.

## D-16-08: Business case and test size

- Date: 2026-10-20
- Case: 16
- Context / question: What is it worth and how big must the test be?
- Options considered: report the twin lift only; scenario table with pass-through.
- Decision: Base case about ₹55 crore a year for the ranker (₹25 to ₹88 crore) and about ₹20 crore for the blend, after ₹4 crore costs; live test needs 17,851 sessions per arm for a +2% click lift.
- Why: Twin lift 27.1% (CI 26.1% to 28.1%) with 25 lakh sessions a day, 20% conversion, ₹30 per order, 40% pass-through.
- Assumption checks / evidence: No online lift is published by Swiggy; the twin rewards rating and distance as well as relevance.
- Impact if wrong / mitigation: Use the ordering of methods, not the rupee figure; measure orders per search live.
