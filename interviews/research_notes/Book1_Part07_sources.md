# Book 1 Part 07 — Research Sources (recsys / ranking / search / LTR)

Date: 2026-10-20. WebSearch/WebFetch WORKED but returned mostly prep-site question banks and docs, not first-hand 2025-26 candidate reports. Glassdoor/AmbitionBox/Blind/LeetCode Discuss/GfG did not surface recsys-specific experiences. Dataford and Interview Query fetches returned HTTP 429 (only search snippets seen). No first-hand Zalando, Klarna recsys, Walmart, PhonePe, Meesho or Amazon recsys reports were found. 'Asked at' tags in the question file are therefore pattern-based (type of team), not verified quotes.

## Sources
| ID | URL | Status |
|---|---|---|
| S1 | https://hyring.com/jobseeker-toolkit/interview-questions/technical/recommender-systems | Opened; 45-question bank (2026) |
| S2 | https://www.techinterview.org/post/3233474409/ai-ml-interview-recommendation-systems-collaborative-filtering-content-based-embeddings-two-tower-model-cold-start/ | Opened; CF, MF, two-tower, ranking, cold start, bandits, bias |
| S3 | https://www.hellointerview.com/learn/ml-system-design/patterns/recommendation-systems | Opened; retrieval vs ranking, multi-objective, sequential, evaluation |
| S4 | https://dataford.io/questions/lists/recommendation-systems-questions | Search snippet only (429); cold-start ranker, offline NDCG vs A/B |
| S5 | https://xgboost.readthedocs.io/en/stable/tutorials/learning_to_rank.html ; https://arxiv.org/pdf/1809.05818 ; https://github.com/microsoft/LightGBM/pull/4531 | Search snippet; LambdaMART / unbiased LTR background, not interview reports |
| S6 | https://arxiv.org/abs/2602.07774v2 | Search snippet; LLM reranking (GR2), semantic IDs, reward hacking by preserving order |
| S7 | https://prepfully.com/interview-questions/spotify/data-scientist?page=3 (also page=6, page=9) | Search snippet; Spotify recommender-from-listening-behaviour case, podcast search design |
| S8 | https://www.interviewquery.com/interview-guides/flipkart-machine-learning-engineer ; https://dataford.io/interview-guides/swiggy/data-scientist | Search snippet (429 on fetch); Flipkart 4 rounds (ML breadth, ML design, coding, HM); Swiggy DS on food-discovery personalisation |
| S9 | https://jobrise.io/de/blog/booking-com-data-scientist-resume-interview-2026/ ; https://static.glassdoor.at/Interview/Booking-com-Interview-E256653-RVW9991413.htm | Search snippet; Booking ads list ranking/personalisation; 2016 Glassdoor mentions ordering hotels |
| S10 | https://www.educative.io/courses/grokking-the-machine-learning-system-design-interview/the-cold-start-problem-and-data-scarcity ; https://www.vskills.in/interview-questions/data-science-interview-questions/ai-recommender-systems-interview-questions | Search snippet; cold start, MF/NDCG for freshers |

## Question -> sources -> frequency -> recency
Frequency = number of listed sources covering the topic (topic-level match, not verbatim). Recency: all 2025-2026 except S9 Glassdoor (2016). Origin: found = in sources; gap-check = added by expert review.

| Q | Question (short) | Origin | Sources | Freq |
|---|---|---|---|---|
| 1 | Explain collaborative filtering. User-based vs item-based: how do they differ, a | found | S1,S2,S10 | 3 |
| 2 | Explicit vs implicit feedback: what is the difference, and how does your modelli | found | S1,S2,S3 | 3 |
| 3 | What is the cold-start problem? How do you handle a new user, a new item, and a  | found | S1,S2,S3,S4,S10 | 5 |
| 4 | Why do large recommenders use a two-stage pipeline (candidate generation then ra | found | S1,S2,S3 | 3 |
| 5 | Define precision@k, recall@k, MRR, MAP and NDCG. When would you pick each one? | found | S1,S3,S10 | 3 |
| 6 | Compute NDCG@k by hand for a small ranked list, then write it in NumPy. Why the  | found | S1,S3,S4,S10 | 4 |
| 7 | Explain matrix factorization for recommendations. How is it trained (SGD vs ALS) | found | S1,S2,S3,S10 | 4 |
| 8 | Content-based vs collaborative vs hybrid recommenders: strengths, weaknesses, an | found | S1,S2,S3 | 3 |
| 9 | Explain the two-tower model: architecture, training objective and negatives, and | found | S1,S2,S3,S4 | 4 |
| 10 | Offline NDCG/AUC improved but the A/B test got worse (or flat). What could expla | found | S1,S3,S4 | 3 |
| 11 | What is popularity bias and how do feedback loops form in recommenders? How woul | found | S1,S2,S3 | 3 |
| 12 | What is position bias in click data? How does it corrupt a ranker trained on cli | found | S2,S5 | 2 |
| 13 | How do you split data and evaluate a recommender offline? Why is a random split  | found | S1,S3 | 2 |
| 14 | How do you sample negatives for implicit-feedback training (random, popularity-b | found | S1,S3 | 2 |
| 15 | Walk through how you would build a recommender for an e-commerce / food-delivery | found | S1,S3,S7,S8 | 4 |
| 16 | Cosine similarity vs dot product vs Euclidean distance for embeddings: when do t | gap-check | - | 0 |
| 17 | Why is RMSE a poor metric for top-N recommendation on implicit data? What should | found | S1/S2/S3 topic-level | 1 |
| 18 | Pointwise vs pairwise vs listwise learning-to-rank: how do the losses differ and | gap-check | - | 0 |
| 19 | Explain LambdaRank and LambdaMART. How do you train a ranker in XGBoost/LightGBM | found | S1/S2/S3 topic-level | 1 |
| 20 | How does approximate nearest neighbour search work? Compare HNSW, IVF-PQ and Sca | found | S1/S2/S3 topic-level | 1 |
| 21 | Exploration vs exploitation in recommenders: epsilon-greedy, UCB, Thompson sampl | found | S1/S2/S3 topic-level | 1 |
| 22 | How do you add diversity, novelty, serendipity and freshness to a ranked list? E | found | S1/S2/S3 topic-level | 1 |
| 23 | Your system predicts click, add-to-cart, purchase and dwell time. How do you com | found | S1/S2/S3 topic-level | 1 |
| 24 | CTR is up but retention or long-term satisfaction is falling (clickbait ranks hi | found | S1/S2/S3 topic-level | 1 |
| 25 | Compare SVD, truncated SVD, ALS, NMF and SVD++ for recommendations. What do user | gap-check | - | 0 |
| 26 | Search relevance: TF-IDF vs BM25 vs dense retrieval vs hybrid search. When does  | found | S1/S2/S3 topic-level | 1 |
| 27 | How do you evaluate a search/ranking system online and offline: relevance labels | found | S1/S2/S3 topic-level | 1 |
| 28 | How are item embeddings learned (item2vec/prod2vec, session co-occurrence)? What | gap-check | - | 0 |
| 29 | In-batch negatives in two-tower training bias the model towards popular items. H | found | S1/S2/S3 topic-level | 1 |
| 30 | Wide & Deep, DeepFM, DLRM: why do ranking models need explicit feature crosses a | found | S1/S2/S3 topic-level | 1 |
| 31 | Sequential and session-based recommendation: Markov chains, GRU4Rec, SASRec/BERT | found | S1/S2/S3 topic-level | 1 |
| 32 | Selection bias and counterfactual evaluation: explain inverse propensity scoring | found | S1/S2/S3 topic-level | 1 |
| 33 | Does a ranker's predicted probability need to be calibrated? When does it matter | gap-check | - | 0 |
| 34 | How do you meet a latency budget (e.g. 100 ms) in a recsys: cascaded ranking, ca | found | S1/S2/S3 topic-level | 1 |
| 35 | Implement item-based collaborative filtering (cosine similarity on a sparse user | gap-check | - | 0 |
| 36 | Implement matrix factorization with SGD from scratch in NumPy (bias terms, L2, t | gap-check | - | 0 |
| 37 | Bi-encoder vs cross-encoder: how do they differ for retrieval vs reranking, and  | gap-check | - | 0 |
| 38 | How can LLMs or pretrained text/image embeddings help cold start and item repres | gap-check | - | 0 |
| 39 | Can you use an LLM as a judge to label search/recommendation relevance? What bia | gap-check | - | 0 |
| 40 | How do you measure and improve fairness and exposure for small creators or selle | found | S1/S2/S3 topic-level | 1 |
| 41 | A recommendation reveals a sensitive inference about a user. What privacy, expla | found | S1/S2/S3 topic-level | 1 |
| 42 | How do you measure the causal impact of recommendations on engagement (not just  | found | S1/S2/S3 topic-level | 1 |
| 43 | Design LLM-based reranking for top-k candidates: pointwise vs listwise prompting | gap-check | - | 0 |
| 44 | Unbiased learning-to-rank from click logs: how do you estimate position propensi | found | S1/S2/S3 topic-level | 1 |
| 45 | Contextual bandits for recommendation (LinUCB, Thompson sampling) and off-policy | found | S1/S2/S3 topic-level | 1 |
| 46 | Why is NDCG not directly optimisable by gradient descent, and how do lambda grad | gap-check | - | 0 |
| 47 | Graph-based recommenders: random walks, PinSage, LightGCN. When are they worth t | found | S1/S2/S3 topic-level | 1 |
| 48 | Recommending in a two-sided marketplace (customer / restaurant / delivery partne | gap-check | - | 0 |
| 49 | Embedding and index operations: how do you refresh embeddings, version two-tower | gap-check | - | 0 |

Added from expert gap-check: Q16, Q18, Q25, Q28, Q33, Q35, Q36, Q37, Q38, Q39, Q43, Q46, Q48, Q49.
Star logic: 3+ sources or core to every recsys loop = ⭐⭐⭐; regular = ⭐⭐; niche/senior/AI-era = ⭐.

## AI-era changes noted
- LLM reranking and generative retrieval (semantic IDs) now appear as senior follow-ups (S6); known pitfalls: position bias, reward hacking by keeping original order.
- LLM-as-judge for relevance labels is replacing some human labelling in search; interviewers probe validation.
- Retrieval vocabulary (bi/cross-encoder, ANN, hybrid search) overlaps with RAG; expect cross-over questions (Book 2 Parts 6-7).
- Classical themes unchanged: cold start, two-stage design, NDCG, offline vs online mismatch, position bias.
- End-to-end design cases (feed, YouTube-style recommender) are deferred to Book 1 Part 11.
