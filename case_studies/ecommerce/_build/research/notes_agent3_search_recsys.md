

### R1 Hinglish search (Flipkart)
(a) Calibrate to: about 21% of queries Hinglish; Head/Torso/Tail balanced 15k test set; BLEU 51.3 (teacher) vs Google Translate 35.8 and Azure 25.5; language-ID CRF precision 0.84, recall 0.72 (keyword baseline recall 28%); latency p95 about 200 ms teacher vs about 47 ms student (BLEU 50.8).
(b) Interviewers expect: query classification, spell correction (edit distance, noisy channel), transliteration, seq2seq or retrieval-based rewriting, query-product relevance with NDCG/MRR, Head/Torso/Tail analysis, zero-result rate, A/B testing with query-level metrics, latency tradeoffs.
(c) Very common (spelling-noisy and vernacular queries are a core problem for any Indian marketplace).

### R2 Visual similarity / shop the look (Myntra)
(a) Calibrate to: P@3 28.4, R@3 15.5, P@10 15.8, R@10 37.6; 477/500 expert-relevant (about 95%); A/B: CTR +25%, add-to-cart ratio +4% (authors' claim); Mask R-CNN mAP 78%; about 150k training images.
(b) Interviewers expect: embeddings and nearest-neighbour search, triplet/contrastive loss and hard-negative mining, CNN transfer learning, object detection, precision/recall@K, offline-versus-online metric gaps, A/B testing, cold-start items via content features.
(c) Common (strong in fashion and beauty; present in most large catalogues).

### R3 Item-to-item CF (Amazon)
(a) Calibrate to: more than 29 million customers; several million items; offline O(N^2 M), practically about O(NM); online cost independent of catalog size; works from "as few as two or three items"; MovieLens comparison (35,000 customers, 3,000 items).
(b) Interviewers expect: cosine/Pearson/Jaccard similarity, user-based vs item-based CF, sparsity, cold-start, popularity bias, implicit vs explicit feedback, matrix factorisation (ALS/SVD), evaluation with precision/recall@K, MAP, NDCG, coverage, and online A/B.
(c) Very common (the default "customers also bought" building block everywhere).

### R4 Dish search and discovery (Swiggy)
(a) Calibrate to: 8+ listed spellings of biryani; about 2M training tuples over 2 months; V1 35,000 pairs and V2 26,000 misspelled pairs; improvement over FastText of 3% MRR / 4.49% Recall@100 on V1 and 93% / 25% on misspelled V2; Word2Vec out-of-vocabulary for about 32% of dishes in the test city; ranking: 1 month training, 1 later week validation; 300+ dish families; embedding latency about 2 ms p99.
(b) Interviewers expect: retrieval-then-ranking funnel, BM25 vs embeddings, learning-to-rank (pairwise/listwise), implicit-feedback labels and position bias, MRR/NDCG/MAP, spell-correction, hyperlocal availability filters, cold-start restaurants, exploration.
(c) Common (every food, grocery and quick-commerce app has item search with local availability constraints).

### R5 Ads ranking (Flipkart)
(a) Calibrate to: fixed slots 2 and 5 in the old design; 27 features crossed with isAds; A/B exposures above 100M; organic orders +1.36%, ad revenue +3.4% (company claim); default fallback score 0.5; organic feedback volume "multi-fold" larger than ads.
(b) Interviewers expect: CTR/CVR models (logistic regression, GBDT, FTRL, DeepFM), calibration (Platt/isotonic, reliability curves), expected-value ranking (bid x pCTR x pCVR), second-price/GSP auctions, position bias, AUC/log loss/NDCG, delayed conversions, A/B testing with seller and platform guardrails.
(c) Very common (retail media is a major revenue line across Indian ecommerce).

### R6 Cold start and exploration (Meesho / Myntra)
(a) Calibrate to: Myntra widget bandit +0.24% homepage clicks per user vs XGBoost, 7-day warm start, ILAD about 0.48-0.50, DPP theta 0.6-0.8; Meesho: ND for all numerical effects (directional claims only), so treat any cold-start uplift in a simulation as an assumption.
(b) Interviewers expect: popularity and demographic baselines, content-based cold start, multi-armed bandits (epsilon-greedy, UCB, Thompson sampling), contextual bandits, two-tower models, knowledge distillation, diversity re-ranking, new-user activation and retention metrics, A/B tests on new-user cohorts.
(c) Very common (Indian apps acquire many first-time internet shoppers, so new-user cold start is a standard problem).
