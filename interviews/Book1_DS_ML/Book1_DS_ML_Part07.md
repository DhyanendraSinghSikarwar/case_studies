# Book 1 — Part 07: Recommender Systems, Ranking, Search & Learning-to-Rank

**Topic:** collaborative filtering, matrix factorization, two-tower, cold start, candidate generation + ranking, ranking metrics, LambdaMART/LTR, position bias, bandits/exploration, embeddings/ANN, LLM reranking
**Target:** >=40 questions | **Actual:** 49 (⭐⭐⭐ 15, ⭐⭐ 21, ⭐ 13)
**Date:** 2026-10-20 | **Status:** Phase 1 (questions only)

### Q1 ⭐⭐⭐ 🟢 Explain collaborative filtering. User-based vs item-based: how do they differ, and which scales better and why?
**Asked at:** Product / e-commerce / streaming recsys teams; GCC DS screens
<!-- ANSWER_PENDING -->

### Q2 ⭐⭐⭐ 🟢 Explicit vs implicit feedback: what is the difference, and how does your modelling and loss function change for implicit data (clicks, views, purchases)?
**Asked at:** E-commerce, food-delivery, media; ML breadth rounds
<!-- ANSWER_PENDING -->

### Q3 ⭐⭐⭐ 🟢 What is the cold-start problem? How do you handle a new user, a new item, and a brand-new platform?
**Asked at:** Almost all recsys loops (e-commerce, marketplaces, streaming)
<!-- ANSWER_PENDING -->

### Q4 ⭐⭐⭐ 🟡 Why do large recommenders use a two-stage pipeline (candidate generation then ranking)? What does each stage optimise, and what metric does each care about?
**Asked at:** Product companies; ML system-design-flavoured rounds
<!-- ANSWER_PENDING -->

### Q5 ⭐⭐⭐ 🟡 Define precision@k, recall@k, MRR, MAP and NDCG. When would you pick each one?
**Asked at:** Search/recsys teams; DS and MLE loops
<!-- ANSWER_PENDING -->

### Q6 ⭐⭐⭐ 🟡 Compute NDCG@k by hand for a small ranked list, then write it in NumPy. Why the log discount, and how do you handle ideal-DCG = 0 and ties?
**Asked at:** Coding / ML-breadth rounds (product cos, GCCs)
<!-- ANSWER_PENDING -->

### Q7 ⭐⭐⭐ 🟡 Explain matrix factorization for recommendations. How is it trained (SGD vs ALS), why not treat missing entries as zeros, and what does the embedding size control?
**Asked at:** Product / fintech / e-commerce; fresher to senior
<!-- ANSWER_PENDING -->

### Q8 ⭐⭐⭐ 🟡 Content-based vs collaborative vs hybrid recommenders: strengths, weaknesses, and when would you choose each?
**Asked at:** Generalist DS rounds; e-commerce, media
<!-- ANSWER_PENDING -->

### Q9 ⭐⭐⭐ 🟡 Explain the two-tower model: architecture, training objective and negatives, and how it is served (precomputed item embeddings + ANN).
**Asked at:** Product cos, MLE loops; Spotify/Zalando-style retrieval teams
<!-- ANSWER_PENDING -->

### Q10 ⭐⭐⭐ 🟡 Offline NDCG/AUC improved but the A/B test got worse (or flat). What could explain it and how do you debug?
**Asked at:** Senior DS/MLE; recsys and ads teams
<!-- ANSWER_PENDING -->

### Q11 ⭐⭐⭐ 🟡 What is popularity bias and how do feedback loops form in recommenders? How would you detect and reduce them?
**Asked at:** Product cos, marketplaces, media
<!-- ANSWER_PENDING -->

### Q12 ⭐⭐⭐ 🟡 What is position bias in click data? How does it corrupt a ranker trained on clicks, and how do you correct it (propensity weighting, position feature dropped at serving, randomisation)?
**Asked at:** Search / ads / e-commerce ranking teams
<!-- ANSWER_PENDING -->

### Q13 ⭐⭐⭐ 🟡 How do you split data and evaluate a recommender offline? Why is a random split wrong, and where can data leakage creep in (e.g. features using future purchases)?
**Asked at:** Senior DS/MLE; fintech and e-commerce
<!-- ANSWER_PENDING -->

### Q14 ⭐⭐⭐ 🟡 How do you sample negatives for implicit-feedback training (random, popularity-based, hard negatives, in-batch)? What are the trade-offs?
**Asked at:** MLE roles; retrieval/ranking teams
<!-- ANSWER_PENDING -->

### Q15 ⭐⭐⭐ 🟡 Walk through how you would build a recommender for an e-commerce / food-delivery / music app: data, labels, candidate sources, ranker features, metrics. (Full end-to-end design belongs to Part 11; answer at model level here.)
**Asked at:** Flipkart/Swiggy/Amazon-type and Spotify-type teams; DS and MLE
<!-- ANSWER_PENDING -->

### Q16 ⭐⭐ 🟢 Cosine similarity vs dot product vs Euclidean distance for embeddings: when do they give different rankings, and why normalise?
**Asked at:** ML breadth rounds; retrieval roles
<!-- ANSWER_PENDING -->

### Q17 ⭐⭐ 🟢 Why is RMSE a poor metric for top-N recommendation on implicit data? What should you use instead?
**Asked at:** DS rounds at product cos and GCCs
<!-- ANSWER_PENDING -->

### Q18 ⭐⭐ 🟡 Pointwise vs pairwise vs listwise learning-to-rank: how do the losses differ and when would you use each?
**Asked at:** Search/ranking teams
<!-- ANSWER_PENDING -->

### Q19 ⭐⭐ 🟡 Explain LambdaRank and LambdaMART. How do you train a ranker in XGBoost/LightGBM (query groups, objective, eval metric)?
**Asked at:** Search, ads, e-commerce ranking roles
<!-- ANSWER_PENDING -->

### Q20 ⭐⭐ 🟡 How does approximate nearest neighbour search work? Compare HNSW, IVF-PQ and ScaNN/FAISS indexes on recall, latency, memory and updates.
**Asked at:** MLE / retrieval teams; RAG-adjacent loops
<!-- ANSWER_PENDING -->

### Q21 ⭐⭐ 🟡 Exploration vs exploitation in recommenders: epsilon-greedy, UCB, Thompson sampling. How would you inject exploration for new items?
**Asked at:** Senior DS/MLE; media, marketplaces
<!-- ANSWER_PENDING -->

### Q22 ⭐⭐ 🟡 How do you add diversity, novelty, serendipity and freshness to a ranked list? Explain MMR/DPP re-ranking and how you would measure it.
**Asked at:** Product cos; media (Spotify-type)
<!-- ANSWER_PENDING -->

### Q23 ⭐⭐ 🟡 Your system predicts click, add-to-cart, purchase and dwell time. How do you combine multiple objectives into one ranking (scalarisation, multi-task learning, constraints)?
**Asked at:** Senior DS/MLE; e-commerce, feeds
<!-- ANSWER_PENDING -->

### Q24 ⭐⭐ 🟡 CTR is up but retention or long-term satisfaction is falling (clickbait ranks high). What is going on and what do you change?
**Asked at:** Product cos, feeds, media
<!-- ANSWER_PENDING -->

### Q25 ⭐⭐ 🟡 Compare SVD, truncated SVD, ALS, NMF and SVD++ for recommendations. What do user/item bias terms and regularisation do?
**Asked at:** Classical ML breadth rounds; GCCs
<!-- ANSWER_PENDING -->

### Q26 ⭐⭐ 🟡 Search relevance: TF-IDF vs BM25 vs dense retrieval vs hybrid search. When does each fail?
**Asked at:** Search teams; e-commerce, Booking-style travel
<!-- ANSWER_PENDING -->

### Q27 ⭐⭐ 🟡 How do you evaluate a search/ranking system online and offline: relevance labels, click models, interleaving, A/B tests?
**Asked at:** Search/ranking roles; Booking.com-type hotel ranking
<!-- ANSWER_PENDING -->

### Q28 ⭐⭐ 🟡 How are item embeddings learned (item2vec/prod2vec, session co-occurrence)? What are the pitfalls (popularity, window size, sparse items)?
**Asked at:** E-commerce, travel, music
<!-- ANSWER_PENDING -->

### Q29 ⭐⭐ 🟡 In-batch negatives in two-tower training bias the model towards popular items. How do logQ correction or mixed negative sampling fix it?
**Asked at:** MLE roles at product cos
<!-- ANSWER_PENDING -->

### Q30 ⭐⭐ 🟡 Wide & Deep, DeepFM, DLRM: why do ranking models need explicit feature crosses and how do these architectures provide them?
**Asked at:** Ads / e-commerce ranking MLE
<!-- ANSWER_PENDING -->

### Q31 ⭐⭐ 🟡 Sequential and session-based recommendation: Markov chains, GRU4Rec, SASRec/BERT4Rec. When do they beat matrix factorization?
**Asked at:** Senior DS/MLE; e-commerce, music
<!-- ANSWER_PENDING -->

### Q32 ⭐⭐ 🟡 Selection bias and counterfactual evaluation: explain inverse propensity scoring for offline evaluation of a new ranker and its variance problem (clipping, doubly robust).
**Asked at:** Senior DS; ads/recsys
<!-- ANSWER_PENDING -->

### Q33 ⭐⭐ 🟡 Does a ranker's predicted probability need to be calibrated? When does it matter (ads, blending scores, thresholds) and how do you fix it?
**Asked at:** Ads, fintech, ranking roles
<!-- ANSWER_PENDING -->

### Q34 ⭐⭐ 🟡 How do you meet a latency budget (e.g. 100 ms) in a recsys: cascaded ranking, caching, precomputation, feature-freshness tiers? What do you inspect when latency spikes?
**Asked at:** MLE roles
<!-- ANSWER_PENDING -->

### Q35 ⭐⭐ 🟡 Implement item-based collaborative filtering (cosine similarity on a sparse user-item matrix) with NumPy/pandas and produce top-N recommendations.
**Asked at:** Live-coding at product cos / GCCs
<!-- ANSWER_PENDING -->

### Q36 ⭐⭐ 🔴 Implement matrix factorization with SGD from scratch in NumPy (bias terms, L2, train/val RMSE). How would you adapt it to implicit feedback?
**Asked at:** Coding rounds, MLE; Microsoft IDC / Amazon-type
<!-- ANSWER_PENDING -->

### Q37 ⭐ 🟡 Bi-encoder vs cross-encoder: how do they differ for retrieval vs reranking, and why is a cross-encoder only used on a shortlist?
**Asked at:** Search/RAG-adjacent MLE roles
<!-- ANSWER_PENDING -->

### Q38 ⭐ 🟡 How can LLMs or pretrained text/image embeddings help cold start and item representation? What is generative retrieval with semantic IDs?
**Asked at:** AI-era recsys/search roles
<!-- ANSWER_PENDING -->

### Q39 ⭐ 🟡 Can you use an LLM as a judge to label search/recommendation relevance? What biases and validation steps do you need?
**Asked at:** AI-era search/ranking roles
<!-- ANSWER_PENDING -->

### Q40 ⭐ 🟡 How do you measure and improve fairness and exposure for small creators or sellers? How do you stop sellers spamming metadata to game the ranker?
**Asked at:** Marketplaces, creator platforms
<!-- ANSWER_PENDING -->

### Q41 ⭐ 🟡 A recommendation reveals a sensitive inference about a user. What privacy, explainability and guardrail changes would you make?
**Asked at:** Senior roles; fintech/health/EU-regulated cos
<!-- ANSWER_PENDING -->

### Q42 ⭐ 🟡 How do you measure the causal impact of recommendations on engagement (not just correlation)? Discuss holdouts, uplift and incrementality.
**Asked at:** Senior DS; marketplaces, Booking-type
<!-- ANSWER_PENDING -->

### Q43 ⭐ 🔴 Design LLM-based reranking for top-k candidates: pointwise vs listwise prompting, cost and latency, distillation into a small ranker, and failure modes (position bias, reward hacking by preserving order).
**Asked at:** AI-era senior MLE/DS
<!-- ANSWER_PENDING -->

### Q44 ⭐ 🔴 Unbiased learning-to-rank from click logs: how do you estimate position propensities, and how does Unbiased LambdaMART use them?
**Asked at:** Search/ads ranking specialists
<!-- ANSWER_PENDING -->

### Q45 ⭐ 🔴 Contextual bandits for recommendation (LinUCB, Thompson sampling) and off-policy evaluation. When would you use a bandit instead of a supervised ranker?
**Asked at:** Senior DS/MLE; media, ads
<!-- ANSWER_PENDING -->

### Q46 ⭐ 🔴 Why is NDCG not directly optimisable by gradient descent, and how do lambda gradients get around that?
**Asked at:** Ranking specialists; research-leaning MLE
<!-- ANSWER_PENDING -->

### Q47 ⭐ 🔴 Graph-based recommenders: random walks, PinSage, LightGCN. When are they worth the complexity?
**Asked at:** Large-catalog platforms; senior
<!-- ANSWER_PENDING -->

### Q48 ⭐ 🔴 Recommending in a two-sided marketplace (customer / restaurant / delivery partner, or job seeker / recruiter): how do you balance stakeholders and capacity constraints?
**Asked at:** Swiggy/Zomato/Uber/LinkedIn-type
<!-- ANSWER_PENDING -->

### Q49 ⭐ 🔴 Embedding and index operations: how do you refresh embeddings, version two-tower models, avoid mismatches between towers and the ANN index, and roll back?
**Asked at:** Senior MLE
<!-- ANSWER_PENDING -->
