# Agent 3 Research: Search, Recommender Systems, Ads and Cold-Start in Indian Ecommerce

Compiled 2026-10-17. Facts marked as documented were read on pages fetched during this research. "ND" = Not publicly disclosed (in the sources read). Several sources were read through a text-extraction proxy (r.jina.ai) or arXiv's ar5iv HTML; figures inside images (charts, result tables) were not readable and are treated as ND.

## Case R1 — Hinglish Search Query Translation at Flipkart
**Company:** Flipkart
**Industry:** Ecommerce (marketplace)
**Business Area:** Search / query understanding
**Problem Type:** Code-mixed (Hinglish) query translation, language identification, relevance
**Evidence Level:** Medium. Category C (arXiv paper by Flipkart team: Kulkarni, Chennabasavaraj, Garera) with real method detail, but business impact is not quantified.
**Primary Sources:** arXiv 2208.03713 "Study of Encoder-Decoder Architectures for Code-Mix Search Query Translation" (7 Aug 2022).

### 1. Business Problem
The paper states that about 21% of Flipkart's queries are Hinglish (Hindi words typed in Latin script). Translating them to English lets the existing English search stack handle them. Stated difficulties: no parallel training data, spelling errors, brand misspellings, ambiguous language identification, non-standard query format, and "articulation gap" queries (example given: "juta bina dori wala" for "shoe without lace").

### 2. Business Question
How can a Hinglish query be reliably translated to English, at production latency, so that existing English-language retrieval and ranking serve it well?

### 3. Data Available
| Data | Description |
|---|---|
| Pseudo-labelled corpus | About 5M unlabeled Hindi/Hinglish queries, labelled using third-party translation and transliteration APIs (an earlier pilot used 200k queries) |
| In-house tagged Hinglish set | About 70k queries (under 1.5% of labelled set); stage-2 fine-tuning used 55k (10% validation), 15k test |
| Initial test set | 15k manually tagged Hinglish queries, balanced across Head, Torso, Tail |
| Language-detection set | 80k queries tagged per word, 20k held out for test |
| In-house alternative data (Sec 8.2) | Generic English-Hindi translation model on about 1.4M pairs translated about 18M English queries; transliteration model trained on 96.4k word pairs |

### 4. Data Science Approach
Documented: (a) a per-word language-identification step to detect Hinglish; (b) a sequence-to-sequence translation model trained in two stages (stage 1 on the 5M pseudo-labelled corpus for 5 epochs; stage 2 on in-house human labels until validation loss stopped improving); (c) data augmentation (Masking, AutoEncoder, DropChar dropping a character from 30-50% of words, WordOrderPermute); (d) knowledge distillation to a single-layer quantized student to meet latency. Loss was a weighted mix of supervised and augmentation cross-entropy (lambda = 0.5).

### 5. Statistical Analysis
No hypothesis testing documented. The paper compares models on BLEU and per-class precision/recall; A/B testing is mentioned without numbers. Test sets were stratified Head/Torso/Tail.

### 6. Machine Learning
- **Models:** T5-base (about 222M params), BART-base (about 139M, chosen), Bert2Bert, mT5-small and mBART-large-50 as multilingual comparisons; distilled 1-layer BART student. Language ID: CRF, FastText, CNN, LSTM.
- **Target variable:** English translation of the Hinglish query (seq2seq); language label per word for detection.
- **Features:** Raw query text (subword tokens). ND beyond that.
- **Validation approach:** Held-out tagged test sets (15k Head/Torso/Tail balanced); 10% validation split in stage 2; online A/B test (no figures).
- **Metrics:** SacreBLEU. Hinglish test set: Azure Translate 25.5, Google Translate 35.8, BART random init 49.9, BART no augmentation 50.3, BART with augmentation 51.3, mT5 48.3, mBART 46.6. Augmentation: AutoEncoder +1.37 (BART), WordOrderPermute -3.1 (BART). Language ID precision/recall/F1: CRF 0.84/0.72/0.76 (best), FastText 0.90/0.61/0.73, CNN 0.80/0.65/0.72, LSTM 0.82/0.63/0.71; the paper notes CRF recall rose from 28% (keyword baseline) to 72%. Distillation: teacher BLEU 51.3, p95 about 200 ms; quantized student with Jensen-Shannon KD loss BLEU 50.8, about 47 ms; with cross-entropy KD loss BLEU 49.7.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| T5 / BART / BERT checkpoints | Seq2seq models |
| AdamW, label smoothing 0.1, beam size 3 | Training and decoding |
| A100 GPU | Training |
| SacreBLEU | Evaluation |
| FastText, CRF | Language identification |
| Weight quantization on CPU, C libraries | Latency reduction in production |
| Azure / Google translation APIs | Pseudo-labelling only |

### 8. Business Decision
Documented: the model is live on the Flipkart app and website for millions of queries, and A/B testing was used to validate it. The choice of the distilled student over the teacher for latency is documented.

### 9. Business Impact
"Live on Flipkart" and "A/B testing was used" are the company authors' own claims. No quantified business metric (conversion, revenue, search success) is given: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
Without labels, bootstrap with noisy third-party labels at scale, then correct with a small high-quality human set (two-stage training). Evaluate by Head/Torso/Tail strata. Latency is a first-class constraint: a 0.5 BLEU drop for roughly 4x speed was accepted. Google/Azure scored far below the in-domain model, which illustrates how domain-specific the noise is.

### 11. Source Links
- arXiv 2208.03713, "Study of Encoder-Decoder Architectures for Code-Mix Search Query Translation", 2022-08-07: https://arxiv.org/abs/2208.03713 (content read via https://ar5iv.labs.arxiv.org/html/2208.03713; listing via arXiv API)

---

## Case R2 — ShopLook: Recommending Similar Products for Every Garment in a Model Image at Myntra
**Company:** Myntra (Flipkart group)
**Industry:** Fashion ecommerce
**Business Area:** Recommendations / visual similarity ("shop the look")
**Problem Type:** Computer-vision retrieval, cross-sell
**Evidence Level:** Strong. Category C (Myntra Designs authors; accepted at IEEE MIPR 2021), with a stated A/B result.
**Primary Sources:** Ravi, Repakula, Dutta, Parmar, "Buy Me That Look: An Approach for Recommending Similar Fashion Products", arXiv 2008.11638 (26 Aug 2020, revised 6 Apr 2021).

Note: Pinterest's "Complete the Look" (CVPR 2019) surfaced in search but was not fetched and is not used as a source. ShopLook is similar-item retrieval for each worn garment, not complementary-item recommendation.

### 1. Business Problem
Product pages show a model wearing a full outfit; shoppers who search for one item may want similar items for every garment worn. The authors state this supports cross-selling and customer engagement.

### 2. Business Question
Given a full-shot catalog image, can we automatically detect each garment worn and recommend visually similar catalog products for each?

### 3. Data Available
| Data | Description |
|---|---|
| Myntra catalog images | Roughly 7-9k training and about 800 test images per article type; about 150k training images total |
| Street2Shop (Kiapour et al.) | Street photos paired with catalog images, used for hard anchor-positive pairs |
| In-house tagger labels | Active-learning loop: taggers flag misclassifications for retraining |

### 4. Data Science Approach
Four-stage pipeline: (1) full-shot detection via human keypoints (head and ankle present) plus a pose classifier (front/back/left/right/detailed); (2) article localisation with Mask R-CNN for about 20 apparel types, with active learning; (3) a triplet-network embedding per detected article; (4) cosine-similarity retrieval against the catalog.

### 5. Statistical Analysis
Online A/B test reported; the paper gives no duration, sample size or significance for it. Expert review: 477 of 500 sampled recommendations judged visually relevant (about 95%).

### 6. Machine Learning
- **Models:** keypoint model (Xiao et al., ResNet-based); ResNet18 pose classifier; Mask R-CNN (ResNet-101-FPN); triplet network with shared-weight ResNet50 branches (best backbone), weighted triplet loss.
- **Target variable:** Pose class; article class and mask; embedding trained so same-article images are closer than different ones (triplet).
- **Features:** Raw images.
- **Validation approach:** Per-article held-out test images; retrieval baselines EUC, CE, SIFT; expert relevance review of 500 samples; online A/B.
- **Metrics:** Mask R-CNN average mAP 78% (up to 92% for some top-wear classes). Active learning AP (before to after): topwear 82.65 to 87.60, bottomwear 87.11 to 90.25, skirts 51.42 to 69.09, footwear 87.32 to 88.47, bags 69.71 to 78.37. Retrieval: P@3 28.4, R@3 15.5, P@5 24.6, R@5 26.1, P@10 15.8, R@10 37.6, beating the baselines at every K. Triplet: margin 0.2, embedding size 2048, ADAM lr 5e-5, batch 32, semi-hard mining. Inference per image (V100): pose about 200 ms, detection about 400 ms, embedding about 100 ms, retrieval about 5 ms.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Mask R-CNN, ResNet18/50/101 | Detection, classification, embeddings |
| ADAM optimizer | Triplet training |
| Tesla V100 GPUs | Training and timing |
| Serving stack | ND (not named in the paper) |

### 8. Business Decision
Documented: evaluated at Myntra and tested online; also noted to work on user-uploaded fashion images. Rollout scale: ND.

### 9. Business Impact
Authors' own claim from an online A/B test: click-through rate up 25%, add-to-cart ratio up 4%, and longer sessions (paraphrased by the fetch tool; exact paper wording not verified). No duration or significance given.

### 10. What a Data Scientist Can Learn *(interpretation)*
Decompose a complex visual task into stages, each with its own metric. Use active learning to improve weak classes (skirts, bags). Triplet loss with semi-hard mining is the standard metric-learning answer. Precision@K looks low (28.4 at K=3) yet expert-judged relevance was about 95%, a reminder that offline label-matching metrics understate perceived relevance.

### 11. Source Links
- arXiv 2008.11638 abstract page: https://arxiv.org/abs/2008.11638 (fetched)
- Full text via ar5iv: https://ar5iv.labs.arxiv.org/html/2008.11638 (fetched)
- Related, from arXiv listing only (not read in full): arXiv 1806.11371 "Personalizing Similar Product Recommendations in Fashion E-commerce" (Myntra, 2018-06-29).

---

## Case R3 — Item-to-Item Collaborative Filtering at Amazon.com
**Company:** Amazon.com (global; the template used across Indian ecommerce)
**Industry:** Ecommerce
**Business Area:** Recommendations
**Problem Type:** Collaborative filtering at scale
**Evidence Level:** Strong. Category A/C: published by Amazon employees (Linden, Smith, York), IEEE Internet Computing, Jan/Feb 2003.
**Primary Sources:** Linden, Smith, York, "Amazon.com Recommendations: Item-to-Item Collaborative Filtering" (hosted copy at cs.umd.edu).

### 1. Business Problem
Amazon needed real-time personalised recommendations over a very large catalog and customer base. The paper states Amazon had more than 29 million customers and several million catalog items, and notes prior algorithms were typically tested on much smaller datasets such as MovieLens (35,000 customers, 3,000 items).

### 2. Business Question
How can recommendations be generated in real time, with good quality even when a customer has little history, at a scale where classic user-based CF breaks?

### 3. Data Available
| Data | Description |
|---|---|
| Purchase/rating histories | Customer-item vectors, very sparse (most customers buy few items) |
| Catalog | Several million items |

### 4. Data Science Approach
Documented steps: (1) offline, build a similar-items table by finding items that customers tend to buy together (loop over items, then customers who bought each, then other items they bought); (2) similarity per item pair, typically cosine similarity over the customers who bought each; (3) online, for each item the user bought or rated, look up similar items, aggregate, and recommend the most popular or correlated. The paper contrasts three alternatives: traditional CF (compares a user to many customers; sampling or dimensionality reduction hurts quality), cluster models (cheap online but lower quality), and search/content-based methods (too general or too narrow).

### 5. Statistical Analysis
Cosine similarity between item vectors. Complexity analysis: offline table worst case O(N^2 M) but closer to O(NM) in practice; sampling buyers of best-sellers reduces cost further; online lookup depends only on the number of items the user has purchased or rated. Traditional CF: worst case O(MN), about O(M+N) with sparse data, with "severe performance and scaling issues" at 10M+ customers and 1M+ items (per the fetched summary).

### 6. Machine Learning
- **Models:** Item-to-item neighbourhood CF (memory-based, no trained parameters).
- **Target variable:** None (unsupervised similarity).
- **Features:** Co-purchase / co-rating vectors.
- **Validation approach:** ND (no offline metric tables appeared in the fetched summary; the paper is qualitative on quality).
- **Metrics:** ND.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Offline batch computation | Similar-items table build |
| Online lookup | Real-time recommendation |
| Specific software | ND |

### 8. Business Decision
Adopt item-to-item CF in production: expensive computation offline, cheap real-time lookup online, which the authors identify as the key to scalability. They state it works "based on as few as two or three items" (per the fetched summary).

### 9. Business Impact
No revenue or conversion figures in the fetched content: ND.

### 10. What a Data Scientist Can Learn *(interpretation)*
Move cost from the online path to the offline path. Item similarity is more stable than user similarity, so the table can be precomputed. Know the tradeoffs versus matrix factorisation and the known weaknesses (popularity bias, cold-start for new items, limited personalisation beyond history).

### 11. Source Links
- Linden, Smith, York, "Amazon.com Recommendations: Item-to-Item Collaborative Filtering", IEEE Internet Computing, 2003: https://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf (read through a text-extraction proxy)

---

## Case R4 — Dish Search and Query Understanding at Swiggy
**Company:** Swiggy (substituted from "Swiggy/Zomato": Swiggy is far better documented)
**Industry:** Food delivery
**Business Area:** Search, dish ranking, discovery
**Problem Type:** Query understanding (misspellings, transliteration), semantic retrieval, learning-to-rank
**Evidence Level:** Strong. Category A/C: Swiggy Bytes posts by named engineers; the 2024 post is a CODS-COMAD 2024 conference paper.
**Primary Sources:** Swiggy Bytes: "Find My Food" (2021-03-27), "Using Deep Learning for Ranking in Dish Search" (2021-07-20), "Improving search relevance in hyperlocal food delivery using (small) language models" (2024-03-13); Swiggy blog on neural search (2023-07-20).

### 1. Business Problem
Search is the main entry point for high-intent customers. The posts state that Indian dish names have no standard English spelling (biryani typed as 'biriyani', 'biriani', 'beriani', 'briyani' and others), text matching can return no results, and some searched dishes are unavailable locally so nothing similar is shown. Later posts add complex multi-intent queries (dish, diet, mood, time slot).

### 2. Business Question
How do we retrieve and rank dishes that match customer intent despite misspellings, regional names, vague queries and hyperlocal availability?

### 3. Data Available
| Data | Description |
|---|---|
| Search logs | About 2M <query, ordered_dish> tuples over 2 months for embedding training; 35,000 <query, clicked_dish> pairs for validation V1 (26,000 pairs for misspelled V2) |
| Click-through logs | Ranking: one month of training data, validation on a week from a much later period |
| Food Taxonomy | In-house; 300+ dish families and 6 dish categories |
| Historical orders | 996,000 documents (query + bought item + taxonomy metadata) for stage-1 fine-tuning in the 2024 post |
| Curated pairs | More than 300,000 query-item pairs, manually verified, LLM-augmented |
| Test set (2024) | 5000+ samples across 5 international cuisines, 15 Indian regional cuisines, 10+ dietary preferences |

### 4. Data Science Approach
Documented evolution: (1) 2021 embedding model: Siamese network with custom trigram tokenizer, embeddings of queries and dishes, used as a feature in an LTR model for re-ranking; a word-piece transformer variant was rejected because misspellings break tokenization and it was slow; (2) 2021 ranking: retrieval cuts "millions of dishes to hundreds", then a modular deep model scores semantic, restaurant, popularity and distance-time inputs, combined by a bias-free linear layer; (3) 2024: two-stage fine-tuned small language model for embedding-based retrieval of complex queries; (4) 2023 blog: LLM-based neural search planned (pilot "by September" 2023).

### 5. Statistical Analysis
Davies-Bouldin index to test whether embeddings cluster dishes by dish family (10 head families, 250 dishes each); proportion of top-10 results sharing the searched dish's category (2,000 historical queries that returned empty results). Synthetic misspelling set (V2) built from a curated spelling-variation dictionary.

### 6. Machine Learning
- **Models:** Siamese FCN with trigram tokenization (triplet loss, margin 0.4); Siamese Transformer (4 layers x 8 heads, rejected); baselines Word2Vec and FastText (64-d, skip-gram); ranking model inspired by Google's "Neural Ranking Model with Multiple Document Fields"; all-mpnet-base-v2 and all-MiniLM-L6-v2 fine-tuned and compared to BM25.
- **Target variable:** Ranking: clicked dish > shown-but-not-clicked dish > random dish (margin ranking loss, margins chosen experimentally). Embeddings: ordered dish is positive for the query; negatives sampled to be semantically related.
- **Features:** Query, dish name and dish family (trigram embeddings); restaurant embedding, cuisine embeddings, rating, preparation time, cost for two, SLA; normalized daily and monthly orders of dish and restaurant and query-restaurant interactions; last-mile distance, max delivery time (with squared and root transforms).
- **Validation approach:** Time split for ranking (1 month train, 1 later week validate); V1/V2 validation sets; manually relevance-tagged test set for the 2024 retrieval work.
- **Metrics:** MRR, Recall@100 (embeddings); MRR (ranking; result table was an image, values ND); MAP, Precision@1, Precision@5 (2024; values in images, ND). Documented figures: Siamese FCN-T (triplet) improves over the FastText baseline by 3% (MRR) and 4.49% (Recall@100) on V1, and by 93% and 25% on misspelled V2; 3X faster training and over 6X faster inference than the transformer; Word2Vec could not embed about 32% of available dishes in the test city.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| ElasticSearch | Existing fuzzy text retrieval backend |
| TensorFlow (Tensorflow estimator) | Embedding model training and serving |
| Learning-to-rank model | Consumes the cosine-similarity feature (described as one of its top features) |
| HuggingFace sentence-transformer models | 2024 retrieval; CPU instances with a 100 ms query-embedding latency budget |

### 8. Business Decision
Documented: Siamese FCN-T embeddings deployed online to re-rank dish search (query embedding latency about 2 ms at p99); small-LM retrieval "currently in the experimental phase and is being tested with a small cohort" (2024).

### 9. Business Impact
Offline metrics only, as listed above. No online conversion/revenue lift published in the posts read: ND. Catalog size claim: "more than 50 million items" (Swiggy's own 2023 blog).

### 10. What a Data Scientist Can Learn *(interpretation)*
Three-level negatives (clicked > shown > random) are a practical way to use implicit feedback. Character n-gram tokenization is the principled fix for transliteration noise. Build synthetic hard test sets (V2) for the failure you care about. Choosing the model with 3X/6X cheaper train/infer over the best-semantic model is a typical production tradeoff. No online impact is published, so do not claim one.

### 11. Source Links
- "Using Deep Learning for Ranking in Dish Search", Swiggy Bytes, 2021-07-20: https://medium.com/swiggy-bytes/using-deep-learning-for-ranking-in-dish-search-4df2772dddce (fetched via proxy)
- "Find My Food: Semantic Embeddings for Food Search Using Siamese Networks", 2021-03-27: https://medium.com/swiggy-bytes/find-my-food-semantic-embeddings-for-food-search-using-siamese-networks-abb55be0b639 (fetched via proxy)
- "Improving search relevance in hyperlocal food delivery using (small) language models", 2024-03-13 (CODS-COMAD 2024, doi 10.1145/3632410.3632428): https://medium.com/swiggy-bytes/improving-search-relevance-in-hyperlocal-food-delivery-using-small-language-models-ecda2acc24e6 (fetched via proxy)
- Swiggy generative AI / neural search blog, 2023-07-20: https://blog.swiggy.com/?p=14845 (fetched)
- "Personalizing Swiggy POP Recommendations", 2020-03-03: https://medium.com/swiggy-bytes/personalizing-swiggy-pop-recommendations-d434b6f555f9 (retrieved but not analysed here)
- Fifth Elephant 2018 talk abstract (Nitin Hardeniya): https://hasgeek.com/fifthelephant/2018/sub/our-experiments-with-food-recommendations-swiggy-Va5Tmf45onrjBbVMAor7vB (abstract only; no results)

---

## Case R5 — Unified Ranking of Sponsored and Organic Products on Flipkart "Similar Products"
**Company:** Flipkart
**Industry:** Ecommerce / retail media
**Business Area:** Ads ranking, recommendations
**Problem Type:** pCTR/pCVR modelling, ad/organic blending, calibration
**Evidence Level:** Strong. Category A: Flipkart Tech blog by a named data-science team (Amar Kumar et al.), 4 Nov 2025.
**Primary Sources:** "The Science of Unified Ranking: Integrating Ads and Organic Recommendations", Flipkart Tech.

### 1. Business Problem
Product-page widgets pinned sponsored items at fixed slots 2 and 5. The authors call this "safe, predictable, but ultimately sub-optimal" (for a new smartphone all five most relevant items might be sponsored; for pocket scissors, any ad hurts). Goal: let sponsored and organic items compete for slots under one objective.

### 2. Business Question
Can one model and one ranking function compare ads and organic products fairly and beat pinned slots on both organic orders and ad revenue?

### 3. Data Available
| Data | Description |
|---|---|
| Impression logs | Historical impressions from both organic and ads pipelines, combined; organic feedback is "multi-fold" larger than ads |
| Feature sets | Co-browse, co-impression "pair stats" (directional, e.g., impressions of P2 when P1 is viewed), popularity etc.; 27 key features identified for crossing |
| Candidate sources | Co-purchase, co-browse, attribute similarity |
| Ad bids/costs | Used in the sponsored score (exact formula ND) |

### 4. Data Science Approach
Funnel: candidate sourcing, a relevance-filtering stage (SGD classifier predicting probability of conversion given impression, pCVI, daily batch, cached), then a personalised online ranker (FTRL) with separate CTR and CVR models. Unification: single training set with an isAds flag plus 2-way and 3-way crosses of 27 features with isAds; separate organic and sponsored objective functions (organic is a weighted combination with tunable alpha and beta; sponsored adds bid cost components); weights chosen by offline simulation framed as multi-objective optimisation; circuit breaker reverting to pinned slots 2 and 5 if the organic ranker fails; parity pipelines for pair stats on ads plus TOTAL aggregate features.

### 5. Statistical Analysis
Online "high-mod AB test with cumulative exposures crossing 100M"; results reported as statistically significant (test type and confidence intervals: ND). Request AUC (within-request pairwise ordering) used offline.

### 6. Machine Learning
- **Models:** SGD classifier (log loss) for retrieval-stage pCVI; FTRL online logistic models for pCTR and pCVR.
- **Target variable:** Click given impression; conversion given click; conversion given impression.
- **Features:** isAds flag, isAds crosses, popularity, co-browse, co-impression pair stats, TOTAL aggregates; full list ND.
- **Validation approach:** Offline grid: baseline organic-only features vs isAds flag only vs full crosses, evaluated separately on organic-only and ads-only test sets; offline simulations over weights; online A/B.
- **Metrics:** AUC, Request AUC, NDCG, MAP, MRR; business: share of sponsored products, ad spend efficiency, organic orders, ad revenue. The offline lift chart is an image (values ND); the text says the lift was larger for ads with organic about unchanged.

### 7. Tools & Technology
| Tool | Use |
|---|---|
| scikit-learn SGDClassifier | Batch relevance stage |
| FTRL (online learning) | Personalised CTR/CVR rankers |
| Daily batch jobs + cache | Retrieval stage scoring |
| Circuit breaker | Fallback to pinned ads |

### 8. Business Decision
Scaled to 100% of Flipkart traffic after the A/B test; launched for the "Similar Products" recommender.

### 9. Business Impact
Company's own claim: "a statistically significant (1.36%) increase in orders for organic products and a 3.4% increase in bottomline Ads revenue."

### 10. What a Data Scientist Can Learn *(interpretation)*
Calibration across populations with different base rates is the core difficulty in blending ads and organic. A flag plus crosses gives one model with separate effective weights. Design failure modes up front (the 0.5 default-score fallback could flood the page with ads). Report counter metrics (organic orders as well as ad revenue). The exact auction/pricing mechanism is not described, so do not attribute one.

### 11. Source Links
- "The Science of Unified Ranking: Integrating Ads and Organic Recommendations", Flipkart Tech, 2025-11-04: https://blog.flipkart.tech/the-science-of-unified-ranking-integrating-ads-and-organic-recommendations-8cc24113ef21 (fetched via proxy)
- Secondary summary used to locate it: https://daily.dev/posts/the-science-of-unified-ranking-integrating-ads-and-organic-recommendations-fecxacm1v

Gap: no public Flipkart/Meesho/Myntra source on auction mechanics (GSP/VCG, reserve prices) was found. Auction design for this case remains ND.

---

## Case R6 — Cold-Start Feeds for New Users at Meesho (with exploration evidence from Myntra)
**Company:** Meesho (cold-start); Myntra (bandit exploration, substituted in because the Meesho post contains no exploration detail)
**Industry:** Value commerce / fashion ecommerce
**Business Area:** Feed ranking, new-user personalisation
**Problem Type:** Cold-start recommendation, contextual bandits
**Evidence Level:** Medium. Meesho: Category A (named senior data scientist, blog) but no numbers and no date; Myntra: Category C (arXiv paper by company team).
**Primary Sources:** Meesho blog "Personalization from Day One: Solving the Cold Start Problem at Meesho" (Vaishnav Chandak; publication date not stated); arXiv 2309.14046 "Diversify and Conquer: Bandits and Diversity for an Enhanced E-commerce Homepage Experience" (Jaiswal, Malayil, Jawaid, Vempati; 25 Sep 2023).

### 1. Business Problem
Meesho: "New users rarely give second chances." Irrelevant first-session feeds drove high bounce rates. Challenges: few early behavioural signals, and incorporating new in-app interactions in real time. Myntra: ranking heterogeneous homepage widgets per user, where widgets are added and removed over time (item cold-start), framed as a contextual bandit with delayed batch feedback.

### 2. Business Question
How can a useful feed be shown from the first session, and how can a ranker explore new items while exploiting what it knows?

### 3. Data Available
| Data | Description |
|---|---|
| Meesho demographics | Gender, location (X_demo) |
| Meesho early behaviour | Clicks, time on listings, scroll patterns; interaction sequences (X_seq) |
| Meesho user state | Login state, activity level, lifecycle stage (X_state) |
| Meesho item labels | sub_category, price_decile (auxiliary targets); dataset size: ND |
| Myntra | User-widget impressions and clicks; user vectors from browsing/cart/purchase (short and long ranges), SVD user and widget representations, widget metadata, time-of-day/week/year context, revenue features |

### 4. Data Science Approach
Meesho progression: (1) DemoRec: cohort popularity by demographics; (2) ESPM, Early Signal Personalization Model: demographics plus early behaviour predict purchase probability by category, feed built from top categories; (3) CWN, Cold-Warm Net: cold expert tower (demographics) and warm expert tower (sequences) blended by a gating network driven by user-state features, with dynamic knowledge distillation. Myntra: LinUCB and Linear Thompson Sampling produce relevance scores, then a Determinantal Point Process re-ranks for diversity.

### 5. Statistical Analysis
Meesho: backtests shown as charts only; no numbers or design details. Myntra: online A/B vs XGBoost, "high statistical significance" for the click lift (test details ND). Exploration: LinUCB exploration parameter alpha; LinTS posterior sampling; forgetting factor gamma in [0,1] for batch updates; DPP trade-off theta (range 0.6-0.8 reported as promising).

### 6. Machine Learning
- **Models:** Meesho: two-tower cold/warm experts with gating (CWN); prediction is sigmoid of cosine similarity of user and item embeddings; loss binary cross-entropy; a distillation loss is added only when the cold expert's loss exceeds the warm expert's; auxiliary sub_category and price_decile losses. Myntra: LinUCB, LinTS, XGBoost baseline, DPP re-ranker.
- **Target variable:** Meesho: user-item interaction (BCE; the exact label, e.g. click vs order, is not stated: ND). Myntra: widget click.
- **Features:** As in section 3. Item embeddings in Meesho come from a randomly initialised lookup table.
- **Validation approach:** Meesho: backtesting (details ND). Myntra: offline nDCG plus diversity metrics ILAD and ILMD; online A/B; the online model was warm-started on the last 7 days of data.
- **Metrics:** Meesho: CTR, CVR, "O/Vi" (undefined in the post), "FY" order contribution (abbreviation as written; not defined in the post), bounce rate, new-user activation. Myntra: nDCG; ILAD 0.480-0.502 and ILMD 0.039-0.042 across alpha settings (top-10 lists).

### 7. Tools & Technology
| Tool | Use |
|---|---|
| Meesho | No frameworks named (ND) |
| Myntra | No libraries named; architecture has an online inference service, batch retraining per interval, model versioning |

### 8. Business Decision
Meesho: deploy a cold/warm gated model so the feed adapts from the first interactions; the post says the "FY" improvements also helped Search and other surfaces. Myntra: replace the XGBoost widget ranker with bandit plus DPP.

### 9. Business Impact
Meesho (company's own claim, no figures): "notable uplift" in CTR, CVR and O/Vi, "significant" increase in FY order contribution, "sharp drop in bounce rate". Myntra (authors' claim): +0.24% homepage clicks per user over XGBoost, which they call "a decent gain given our scale"; revenue per user and conversion guardrails positive but unquantified.

### 10. What a Data Scientist Can Learn *(interpretation)*
Treat cold-start as a gating problem: blend a demographic expert and a behavioural expert by how much history exists. Distilling warm knowledge into the cold expert only when the cold expert is worse is a neat conditional regulariser. For exploration, bandits give principled explore/exploit and handle item cold-start; add diversity re-ranking so exploitation does not collapse the page. Weak point: Meesho publishes no numbers, so use the Myntra figure (0.24%) only as an order of magnitude in any simulation.

### 11. Source Links
- Meesho, "Personalization from Day One: Solving the Cold Start Problem at Meesho": https://www.meesho.io/blog/personalization-from-day-one-solving-the-cold-start-problem-at-meesho (fetched via proxy; direct fetch returned 403; date not shown)
- arXiv 2309.14046, "Diversify and Conquer: Bandits and Diversity for an Enhanced E-commerce Homepage Experience", 2023-09-25: https://arxiv.org/abs/2309.14046 (content read via https://ar5iv.labs.arxiv.org/html/2309.14046)

---

## Notes for the notebook author

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
