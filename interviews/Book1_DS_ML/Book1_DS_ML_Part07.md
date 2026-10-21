# Book 1 — Part 07: Recommender Systems, Ranking, Search & Learning-to-Rank

**Topic:** collaborative filtering, matrix factorization, two-tower, cold start, candidate generation + ranking, ranking metrics, LambdaMART/LTR, position bias, bandits/exploration, embeddings/ANN, LLM reranking
**Target:** >=40 questions | **Actual:** 49 (⭐⭐⭐ 15, ⭐⭐ 21, ⭐ 13)
**Date:** 2026-10-20 | **Status:** Phase 1 (questions only)

### Q1 ⭐⭐⭐ 🟢 Explain collaborative filtering. User-based vs item-based: how do they differ, and which scales better and why?
**Asked at:** Product / e-commerce / streaming recsys teams; GCC DS screens

**Say this first (1 line):** Collaborative filtering (CF) recommends using only behaviour: people who acted like you liked X, so you may like X. User-based finds similar users; item-based finds similar items, and item-based usually scales better.

**Then explain:**
- **User-based:** score(u, i) = similarity-weighted average of what u's nearest neighbour users did on item i.
- **Item-based:** score(u, i) = similarity-weighted average of u's own ratings on items similar to i.
- **Why item-based scales better:** in most products there are far more users than items, and user behaviour changes daily while item-item similarity is stable. So you precompute the item-item table offline (often only the top-N neighbours per item) and serve with a lookup. User-user similarity needs a huge, constantly stale user table.
- **Where user-based is OK:** small user base, or when the user's taste is highly personal and items are many and short-lived.
- **Limits of both:** sparsity (most pairs have no overlap), cold start, popularity bias. Matrix factorization (MF) and two-tower models fix sparsity by learning dense embeddings.

**Example:** Tiny 4x4 rating matrix (two taste groups), predicting user 0 on item 2. Both methods agree here and give about 2.09 (low, since the similar user rated it low).

**Code:**
```python
import numpy as np
R = np.array([[5,4,0,1],[4,5,1,0],[1,0,5,4],[0,1,4,5]], float)  # 0 = unrated (zero-filled cosine: toy simplification)
def cos(M):
    n = np.linalg.norm(M, axis=1, keepdims=True)
    Mn = M / np.where(n == 0, 1, n); return Mn @ Mn.T
user_sim, item_sim = cos(R), cos(R.T)
u, i = 0, 2
w = user_sim[u].copy(); w[u] = 0; m = R[:, i] > 0
print("user-based", round((w[m] @ R[m, i]) / w[m].sum(), 2))   # 2.09
w2 = item_sim[i].copy(); w2[i] = 0; m2 = R[u] > 0
print("item-based", round((w2[m2] @ R[u, m2]) / w2[m2].sum(), 2))  # 2.09
```

**Follow-ups:**
- *How do you handle rating-scale differences?* Mean-centre per user (or use adjusted cosine / Pearson) before computing similarity.
- *Why not just use CF at web scale?* Exact all-pairs similarity is O(items^2); use top-N neighbours, sparse matrices, or ANN over embeddings.

**Common mistakes:** Zero-filling unrated cells for similarity on real data without mean-centring (fine for a toy); saying user-based scales better; forgetting to remove already-seen items from the output; not mean-centring.

### Q2 ⭐⭐⭐ 🟢 Explicit vs implicit feedback: what is the difference, and how does your modelling and loss function change for implicit data (clicks, views, purchases)?
**Asked at:** E-commerce, food-delivery, media; ML breadth rounds

**Say this first (1 line):** Explicit feedback is a stated opinion (a 1-5 rating); implicit feedback is behaviour (click, view, purchase). Implicit is far more plentiful but it is noisy and has no true negatives, so you stop regressing a rating and instead learn to rank observed items above unobserved ones.

**Then explain:**
| | Explicit | Implicit |
|---|---|---|
| Signal | Rating, thumbs | Click, watch time, purchase, add-to-cart |
| Volume | Tiny, self-selected | Huge |
| Negatives | Real (low rating) | None. Missing = unknown, not dislike |
| Noise | Low | High (accidental click, bought as gift) |
- **Positive-only problem:** a non-click may mean "didn't see it", "not interested" or "not yet". So treat it as *unlabelled*.
- **Confidence, not rating:** classic implicit-ALS (Hu, Koren, Volinsky) sets preference p = 1 if interacted else 0, with confidence c = 1 + alpha * count. Unobserved cells get low confidence, strong interactions get high.
- **Loss changes:** pointwise log-loss with sampled negatives, pairwise BPR (score(positive) > score(negative)), or sampled softmax in two-tower models. Metrics change too: recall@k / NDCG, not RMSE.
- **Signal strength matters:** weight purchase > add-to-cart > click; use dwell time to filter accidental clicks.

**Example:** Food app: a user ordered biryani 6 times and viewed 40 other dishes once. Count-based confidence says biryani is strongly preferred; the views are weak positives; all remaining dishes are sampled as negatives with a lower weight.

**Follow-ups:**
- *Why not treat all unobserved as negatives?* Most are just unseen; you would train the model to repel items the user would have loved. Sampling plus down-weighting is the compromise.
- *Can you mix explicit and implicit?* Yes: SVD++ or multi-task heads, with explicit ratings used as high-quality labels.

**Common mistakes:** Using RMSE on clicks; counting "no click" as a hard negative; ignoring exposure (an item never shown cannot be clicked); not weighting signals by strength.

### Q3 ⭐⭐⭐ 🟢 What is the cold-start problem? How do you handle a new user, a new item, and a brand-new platform?
**Asked at:** Almost all recsys loops (e-commerce, marketplaces, streaming)

**Say this first (1 line):** Cold start means we have no behaviour data for a new user or item, so collaborative signals are empty. We fall back to content, context and popularity, and we actively explore to collect data quickly.

**Then explain:**
- **New user:** use what you do have: device, city, referral source, time of day; onboarding questions ("pick 3 cuisines"); popular or trending items for that segment; then switch to personalised after a few interactions. A common trick is blending by interaction count: weight on personalised score grows with history.
- **New item:** content-based embeddings (title, category, image, price, description) mapped into the same space as the behavioural embeddings; a reserved exploration slot or bandit to get early impressions; boost freshness for a limited time; seller or creator history as a prior.
- **Brand-new platform:** no data at all. Start with popularity, editorial rules or content similarity; buy or reuse data (public catalogue, partner data); run broad exploration; log exposure properly from day one so you can train unbiased later.
- **Model-side fix:** train with *dropout of ID embeddings* so the model learns to rely on content features when the ID is unseen. Use a hybrid (Q8).

**Example:** New restaurant on a delivery app: embed its menu text plus cuisine and price band, find similar mature restaurants, borrow their predicted CTR as a prior, and show it in 2 of 20 slots to nearby users until it has about 500 impressions.

**Follow-ups:**
- *How do you evaluate cold start?* Slice offline metrics by user/item age (e.g. items under 7 days old), and A/B test on new-user cohort.
- *Does exploration hurt?* A little short-term; cap it (say 5% of slots) and measure the cost.

**Common mistakes:** Saying "just use popularity" for everything; not separating user, item and system cold start; forgetting exploration; evaluating only on warm users so the problem is invisible.

### Q4 ⭐⭐⭐ 🟡 Why do large recommenders use a two-stage pipeline (candidate generation then ranking)? What does each stage optimise, and what metric does each care about?
**Asked at:** Product companies; ML system-design-flavoured rounds

**Say this first (1 line):** You cannot score millions of items with a heavy model inside ~100 ms, so a cheap retrieval stage cuts millions to hundreds, and an expensive ranker orders those hundreds.

**Then explain:**
| | Candidate generation (retrieval) | Ranking |
|---|---|---|
| Input size | Millions to billions of items | 100 to 1000 candidates |
| Model | Two-tower embeddings + ANN, co-visitation, popularity, rules | GBDT or deep net with rich cross features |
| Optimises | Recall (don't miss good items) | Precision at top, NDCG, business objective |
| Latency | Few ms, precomputed item vectors | 10-50 ms |
| Features | User and item separate (needed for precompute) | User x item x context crosses |
- Often there is a third stage: **re-ranking** for diversity, freshness, business rules, ads and fairness.
- Multiple retrieval sources (personalised, trending, recently viewed, similar-to-last-item) are merged and de-duplicated.
- **Trade-off:** errors compound. An item dropped by retrieval can never be rescued by ranking, so monitor retrieval recall against what ranker would have picked.

**Example:** Video app: 10M videos -> 500 from 5 retrievers -> ranker predicts watch-time and like probability for the 500 -> re-rank to enforce diversity -> top 20 shown.

**Follow-ups:**
- *How do you evaluate retrieval alone?* Recall@K against later engaged items, plus the share of final-ranked top-N that came from each source.
- *Why not one big model?* Cost grows linearly with candidates; the ranker's cross features cannot be precomputed.

**Common mistakes:** Optimising both stages for the same metric; judging retrieval by NDCG; training ranker only on items retrieval would show (sample selection bias); ignoring end-to-end latency budget.

### Q5 ⭐⭐⭐ 🟡 Define precision@k, recall@k, MRR, MAP and NDCG. When would you pick each one?
**Asked at:** Search/recsys teams; DS and MLE loops

**Say this first (1 line):** Precision@k and recall@k count relevant items in the top k; MRR looks at the first relevant hit; MAP rewards putting all relevant items early; NDCG handles graded relevance with a position discount.

**Then explain:**
| Metric | Definition | Use when |
|---|---|---|
| Precision@k | relevant in top k / k | Screen space fixed, every slot costs |
| Recall@k | relevant in top k / total relevant | Retrieval stage, "did we find them" |
| MRR | mean of 1 / rank of first relevant | One right answer (navigational search, QA) |
| MAP | mean over queries of Average Precision (average of precision@r at each relevant rank r) | Binary relevance, many relevant items |
| NDCG@k | DCG@k / ideal DCG@k, DCG = sum (2^rel - 1) / log2(pos + 1) | Graded labels (0-3), main ranking metric |
- Only NDCG uses graded gains; the others are binary.
- All are per-query averages. Compare on the same k and the same query set.
- P@k and R@k ignore order within top k.

**Example:** Ranked results relevant = [1,0,1,0,0,1], 4 relevant exist in total. P@5 = 2/5 = 0.4, R@5 = 2/4 = 0.5, reciprocal rank = 1, AP = (1 + 2/3 + 3/6) / 4 = 0.54 (divide by all 4 relevant; the one never retrieved counts as zero).

**Follow-ups:**
- *Which for a retrieval model?* Recall@K (K = what ranker will see). *For a final ranker?* NDCG@k.
- *Why not accuracy/AUC?* AUC weighs all pair positions equally; users only see the top.

**Common mistakes:** Dividing AP by retrieved relevant instead of total relevant; mixing log bases; reporting P@k when most queries have fewer than k relevant items (cap at min(k, total)); comparing NDCG across different k.

### Q6 ⭐⭐⭐ 🟡 Compute NDCG@k by hand for a small ranked list, then write it in NumPy. Why the log discount, and how do you handle ideal-DCG = 0 and ties?
**Asked at:** Coding / ML-breadth rounds (product cos, GCCs)

**Say this first (1 line):** NDCG = DCG of my ranking divided by DCG of the perfect ranking; DCG sums gain (2^rel - 1) times a 1/log2(position + 1) discount. Ideal-DCG of zero means no relevant items, so I return 0 and exclude or flag those queries.

**Then explain (hand calc):** relevance in ranked order = [3, 2, 3, 0, 1, 2], k = 6.
- Gains (2^rel - 1): 7, 3, 7, 0, 1, 3. Discounts 1/log2(pos+1): 1, 0.631, 0.5, 0.431, 0.387, 0.356.
- DCG = 7 + 1.893 + 3.5 + 0 + 0.387 + 1.069 = 13.848.
- Ideal order [3,3,2,2,1,0]: gains 7,7,3,3,1,0 -> IDCG = 7 + 4.417 + 1.5 + 1.292 + 0.387 = 14.595.
- NDCG@6 = 13.848 / 14.595 = 0.949.
- **Why the log discount:** a smooth, slowly decaying position weight: rank 1 matters much more than rank 2, but rank 20 vs 21 barely differs. It mimics decreasing attention; it is a modelling choice, not a law. The 2^rel - 1 gain makes very relevant items count disproportionately (linear gain is also used).
- **IDCG = 0:** define NDCG = 0 (or drop the query) and report how many such queries; do not divide by zero.
- **Ties:** scores that tie have undefined order, so average over random permutations or break ties by a stable rule; scikit-learn's `ndcg_score(ignore_ties=False)` averages over ties.

**Example:** The hand calculation above is the example: a search result list whose labels are [3, 2, 3, 0, 1, 2] scores 0.949. The two slips are the 2 and 3 in ranks 2-3 being the wrong way round and a 0 at rank 4 ahead of a 1 and a 2. Moving the first item (the 3) to the last place would drop the score sharply, because its large gain lands at a heavily discounted position.

**Code:**
```python
import numpy as np
def dcg(rel, k):
    rel = np.asarray(rel, float)[:k]
    return ((2**rel - 1) / np.log2(np.arange(2, rel.size + 2))).sum()
def ndcg(rel, k):
    idcg = dcg(np.sort(rel)[::-1], k)
    return 0.0 if idcg == 0 else dcg(rel, k) / idcg
rel = [3, 2, 3, 0, 1, 2]
print(round(ndcg(rel, 6), 4))   # 0.9488
print(round(ndcg(rel, 3), 4))   # 0.9595
print(ndcg([0, 0, 0], 3))       # 0.0
```
`rel` is labels in the order the model ranked them (sort by predicted score first). IDCG uses labels of *all* candidate items for the query, not just the top k.

**Follow-ups:**
- *NDCG@3 vs @10?* Pick k = what the user sees.
- *Can NDCG be compared across queries?* Yes, that is why we normalise.

**Common mistakes:** Computing IDCG from only the returned list when relevant items exist further down; log2(pos) instead of log2(pos + 1) (division by zero at rank 1); using unsorted labels.

### Q7 ⭐⭐⭐ 🟡 Explain matrix factorization for recommendations. How is it trained (SGD vs ALS), why not treat missing entries as zeros, and what does the embedding size control?
**Asked at:** Product / fintech / e-commerce; fresher to senior

**Say this first (1 line):** Matrix factorization (MF) approximates the user-item matrix as a product of two thin matrices: each user and item gets a k-dimensional vector, and the predicted score is their dot product (plus biases), trained only on observed entries.

**Then explain:**
- **Model:** r_ui ~ mu + b_u + b_i + p_u . q_i. Loss = sum over *observed* (u, i) of (r - prediction)^2 + lambda (|p|^2 + |q|^2).
- **SGD:** loop over observed ratings, update p_u and q_i along the gradient. Simple, cheap per step, easy to extend with biases and custom losses.
- **ALS (alternating least squares):** fix Q, solve each p_u in closed form (a small ridge regression); then fix P, solve each q_i. Each step is convex, parallelises across users/items, and handles implicit data with dense weighting well (Spark MLlib).
- **Why not missing = 0:** a zero would say "user hates this item", but the cell is just unobserved. SVD on the zero-filled matrix learns to predict zeros everywhere. Fit only on observed cells (or give unobserved cells small weight with sampled negatives for implicit data).
- **Embedding size k:** controls capacity. Small k underfits (smooth, popular-heavy); large k overfits sparse users unless regularised. Tune k and lambda on validation (typical 16-256).

**Example / Code:** Synthetic 300x150 low-rank matrix with 20% observed, 80/20 train/test split. Test RMSE of the observed-only ALS vs the zero-filled SVD:
```python
import numpy as np
rng = np.random.default_rng(0)
nu, ni, d = 300, 150, 5
truth = rng.normal(size=(nu,d)) @ rng.normal(size=(ni,d)).T / np.sqrt(d)
R = truth + rng.normal(0, .3, truth.shape)
obs = rng.random((nu, ni)) < 0.2
tr = obs & (rng.random((nu, ni)) < 0.8); te = obs & ~tr
def als(mask, k=5, lam=1.0, iters=15):
    P = rng.normal(0, .1, (nu, k)); Q = rng.normal(0, .1, (ni, k)); I = lam*np.eye(k)
    for _ in range(iters):
        for u in range(nu):
            j = mask[u]; P[u] = np.linalg.solve(Q[j].T@Q[j] + I, Q[j].T@R[u, j])
        for i in range(ni):
            j = mask[:, i]; Q[i] = np.linalg.solve(P[j].T@P[j] + I, P[j].T@R[j, i])
    return P @ Q.T
rmse = lambda pred: np.sqrt(((pred - R)[te]**2).mean())
print("ALS observed only:", round(rmse(als(tr)), 2))              # 0.37
print("mean baseline    :", round(rmse(np.full_like(R, R[tr].mean())), 2))  # 1.04
U, s, Vt = np.linalg.svd(np.where(tr, R, 0.0), full_matrices=False)
print("SVD missing = 0  :", round(rmse((U[:, :5]*s[:5]) @ Vt[:5]), 2))     # 0.92
```
Result: 0.37 vs 0.92. Zero-filling is barely better than the 1.04 baseline.

**Follow-ups:**
- *SGD vs ALS?* ALS: parallel and stable, good for implicit with confidence weights. SGD: flexible losses, streaming, easier with biases and side features.
- *Complexity of ALS?* About O(nnz k^2 + (n_users + n_items) k^3) per sweep.

**Common mistakes:** Training on zero-filled matrix; no regularisation; random split instead of time split; forgetting biases (they capture a lot of the variance).

### Q8 ⭐⭐⭐ 🟡 Content-based vs collaborative vs hybrid recommenders: strengths, weaknesses, and when would you choose each?
**Asked at:** Generalist DS rounds; e-commerce, media

**Say this first (1 line):** Content-based recommends items similar to what the user liked using item attributes; collaborative uses behaviour patterns across users; hybrid combines both. I would pick hybrid in production: CF for warm users and items, content for cold ones.

**Then explain:**
| | Content-based | Collaborative | Hybrid |
|---|---|---|---|
| Uses | Item features (text, image, category) + user profile | Interaction matrix | Both |
| Cold-start item | Works | Fails | Works |
| Cold-start user | Needs a first signal | Fails | Partly |
| Serendipity | Low (more of the same) | High (finds cross-genre taste) | Medium-high |
| Needs | Good metadata | Enough interactions | Both, more engineering |
| Failure | Filter bubble, weak metadata | Sparsity, popularity bias | Complexity, tuning |
- **Hybrid styles:** weighted score blend; switch by data availability; feed content features into the CF model (two-tower with side features); stack as features in a ranker (the usual industrial answer).
- **Choose:** tiny catalogue with rich metadata and few users -> content-based; large engaged user base -> CF; always new items (news, listings) -> content-heavy hybrid.

**Example:** News app: a new article has zero clicks, so content (topic, text embedding) retrieves it; for established articles, CF embeddings dominate. The ranker learns how much to trust each.

**Follow-ups:**
- *How would you decide the blend?* Learn it in a ranker with features such as interaction count; offline slices by item age, then A/B.
- *Is a two-tower with ID + content features hybrid?* Yes.

**Common mistakes:** Saying one is "better" without context; ignoring cold start; assuming content-based avoids bias (it can create filter bubbles); blending raw scores from different scales without normalising.

### Q9 ⭐⭐⭐ 🟡 Explain the two-tower model: architecture, training objective and negatives, and how it is served (precomputed item embeddings + ANN).
**Asked at:** Product cos, MLE loops; Spotify/Zalando-style retrieval teams

**Say this first (1 line):** A two-tower model has one neural network for the user (and context) and one for the item; both output vectors in the same space, the score is their dot product or cosine, and because towers do not interact until the last step, item vectors can be precomputed and searched with approximate nearest neighbour (ANN).

**Then explain:**
- **Architecture:** user tower: user ID embedding, history (pooled or sequence), demographics, context -> MLP -> vector u. Item tower: item ID, category, text/image embeddings, price -> MLP -> vector v. Score = u . v (often L2-normalised with a temperature).
- **Training:** positives = (user, item) pairs with engagement. Loss: sampled softmax / contrastive (InfoNCE) over one positive vs many negatives, so the model pulls positives together and pushes negatives away.
- **Negatives:** *in-batch* (other users' positives in the batch; cheap but popularity-biased, fixed with logQ correction, Q29), plus random or hard negatives. Never use only impressions without clicks as the sole negative (they are already similar to what the old system showed).
- **Serving:** offline, run the item tower over the catalogue and build an ANN index (HNSW/IVF-PQ). Online, run only the user tower, query the index for top few hundred, send to the ranker. Item vectors are refreshed on a schedule; new items get a vector from content features immediately.
- **Limitation:** no user-item feature crosses (the ranker handles those). Towers must be versioned together with the index.

**Example (illustrative figures, not benchmarks):** 5M products, 64-d vectors. User tower takes roughly a few ms; ANN returns 300 candidates in roughly 5-10 ms; ranker scores those 300. Real numbers depend on hardware, index and recall target, so measure them.

**Follow-ups:**
- *Why dot product and not an MLP over concatenated features?* An MLP cannot be precomputed or ANN-indexed.
- *Temperature?* Scales logits; lower = sharper focus on hard negatives.

**Common mistakes:** Training on random negatives only (easy, model learns little); not correcting in-batch popularity bias; serving the user tower with features unavailable online (train-serve skew); forgetting to rebuild the index when the model changes.

### Q10 ⭐⭐⭐ 🟡 Offline NDCG/AUC improved but the A/B test got worse (or flat). What could explain it and how do you debug?
**Asked at:** Senior DS/MLE; recsys and ads teams

**Say this first (1 line):** Offline metrics are measured on logged data from the old system, so they can improve while real user behaviour does not; I would first check the experiment itself, then the offline-online gap, then the metric choice.

**Then explain (debug in this order):**
1. **Experiment validity:** sample-ratio mismatch, logging bugs, novelty effect, too short a run, wrong unit of randomisation, underpowered test (flat may just mean low power).
2. **Train-serve skew:** features computed differently online (missing values, stale features, leakage of future info offline), different candidate set, model version or index mismatch.
3. **Offline data bias:** logs only show items the old system displayed (selection and position bias), so a new ranker is scored on items it would not pick. Offline NDCG rewards copying the old policy.
4. **Metric mismatch:** NDCG/AUC on clicks vs online goal (revenue, retention). Better click ranking can mean clickbait, cheaper items, lost diversity.
5. **Latency or coverage:** slower model times out and falls back to default; new model covers fewer users.
6. **Interference:** marketplace effects, shared inventory, feedback loops between arms.
- **Fix:** slice by segment (new vs old users, category), compare feature distributions online vs offline, replay with counterfactual estimators (IPS, Q32), shadow-deploy the model and log scores, add guardrail metrics.

**Example:** AUC +1.5% offline but online orders flat: found the "price rank" feature was computed after the user's click offline (leak). Online it was null, so the model degraded.

**Follow-ups:**
- *Is offline AUC useless then?* No, it is a cheap filter; it is necessary, not sufficient.
- *What if the test is flat?* Check power and MDE, then segment effects (Simpson-type cancellation).

**Common mistakes:** Blaming "noise" without checking power or SRM; trusting offline metrics blindly; not checking serving features; looking at one metric only.

### Q11 ⭐⭐⭐ 🟡 What is popularity bias and how do feedback loops form in recommenders? How would you detect and reduce them?
**Asked at:** Product cos, marketplaces, media

**Say this first (1 line):** Popularity bias means popular items get recommended far more than their true quality warrants; a feedback loop forms because those items get more exposure, so more clicks, so the next model trained on that data recommends them even more.

**Then explain:**
- **Loop:** model -> recommendations -> clicks only on shown items -> new training data -> model. Unseen items get no data and the tail starves ("rich get richer").
- **Detect:** exposure and click share vs catalogue share (Gini or Lorenz curve of impressions); coverage (% of catalogue ever recommended); average popularity of recommended items vs user's history; drift of the same cohort's diversity over time.
- **Reduce:**
  - Data side: propensity or popularity-based reweighting, logQ correction for sampled negatives, exposure-aware training.
  - Model side: remove or regularise popularity features, popularity-debiased scores (divide by item popularity^alpha).
  - Serving side: exploration (bandits, reserved slots), re-ranking for diversity/novelty (Q22), freshness boosts.
  - Process: log randomised slots to get unbiased data.
- **Not all popularity is bad:** popular items are often popular for a reason; the goal is calibration, not removing them.

**Example (illustrative numbers):** Music app: suppose the top 1% of songs get 60% of streams. Reserving 10% of slots for random-from-tail songs yields clean data; the tail's measured CTR can then be compared fairly.

**Follow-ups:**
- *Metric for it?* Coverage, Gini of exposure, average recommendation popularity, long-tail recall.
- *Cost?* Small short-term engagement drop; judge on retention and catalogue health.

**Common mistakes:** Treating popularity as pure bias; evaluating only on popular items (popular baseline looks strong offline); not logging exposure, which makes debiasing impossible.

### Q12 ⭐⭐⭐ 🟡 What is position bias in click data? How does it corrupt a ranker trained on clicks, and how do you correct it (propensity weighting, position feature dropped at serving, randomisation)?
**Asked at:** Search / ads / e-commerce ranking teams

**Say this first (1 line):** Users click top positions more simply because they see them first, so click data mixes real relevance with position; a ranker trained naively learns "top = good" and just reinforces the old ranking.

**Then explain:**
- **Model (position-based click model):** P(click) = P(examined at position p) x P(relevant). Observed CTR at position 1 is higher even for identical items.
- **Corrections:**
  - *Inverse propensity weighting (IPW):* weight each click by 1 / P(examined at p). Need propensities from randomisation (swap experiments, result randomisation on small traffic) or from EM/regression-based estimation.
  - *Position as a training feature:* include it in training, then set it to a fixed default (e.g. position 1 or a constant) at serving. Simple, common; works when the model separates position from relevance, which is imperfect.
  - *Randomisation:* shuffle a small slice of traffic to get unbiased labels and propensities. Costs engagement.
  - *Click models (cascade, DBN):* model examination explicitly.
- **Trade-off:** IPW is unbiased but high variance for deep positions (clip weights, Q32).

**Example / Code (simulation):** examination probability 1/pos, same item relevance at every position. Naive CTR at position 1 is 0.349 vs 0.068 at position 5 (5x apart for equal items); IPW recovers 0.349 vs 0.340 (the gap is sampling noise, larger at deep positions).
```python
import numpy as np
rng = np.random.default_rng(0); n = 200_000
true_rel = rng.uniform(.1, .6, n); pos = rng.integers(1, 6, n)
exam = 1 / pos
click = rng.random(n) < true_rel * exam
for p in (1, 5):
    m = pos == p
    print(p, round(click[m].mean(), 3), round((click[m] / exam[m]).mean(), 3))
# 1 0.349 0.349
# 5 0.068 0.34
```

**Follow-ups:**
- *Where do propensities come from?* Randomisation experiments or EM (Q44).
- *Can you just drop position?* If it is dropped in training without correction, the model still absorbs the bias.

**Common mistakes:** Treating CTR as relevance; fixing position at serving without including it in training; not clipping IPW weights; ignoring that propensity also depends on device and surrounding items.

### Q13 ⭐⭐⭐ 🟡 How do you split data and evaluate a recommender offline? Why is a random split wrong, and where can data leakage creep in (e.g. features using future purchases)?
**Asked at:** Senior DS/MLE; fintech and e-commerce

**Say this first (1 line):** Split by time, not at random: train on the past, validate on the following period, test on the one after that, and score on what the user did next. A random split lets the model see the future, so offline numbers are inflated.

**Then explain:**
- **Why random is wrong:** the same user's later behaviour, trends, and item popularity leak into training; production always predicts forward.
- **Leave-last-out / per-user temporal split:** for sequential models, hold out each user's last interaction(s). Global time cut is closer to production.
- **Eval protocol:** only users and items seen in train (or report cold start separately); remove items already consumed from the truth and from candidates; rank against all items or a large sampled set. Be careful: sampling 100 negatives and ranking only those can reorder models (sampled metrics are inconsistent), so prefer full ranking.
- **Leakage hotspots:**
  - Features with future info: "total purchases" aggregates, price/popularity computed on full data, item embeddings trained on test period.
  - Embeddings or similarity tables fitted on all data.
  - Label from the same session as the features.
  - Duplicates or re-orders of the same order in train and test.
- **Metrics:** recall@k, NDCG@k, MAP; plus coverage, diversity.

**Example:** Three shoppers, cut-off 15 Jan. Everything before the cut is training history; after it, we keep only items the user had not already bought. User 1 bought a, b before the cut and c after, so (1, c) is a test pair; user 2 bought a before and d, e after, so (2, d) and (2, e) are test pairs. Had anyone re-bought an item already in their history, that pair would be dropped.

**Code (time split, filter seen items):**
```python
import pandas as pd
ev = pd.DataFrame({"user":[1,1,1,2,2,2,3,3], "item":list("abcadebc"),
    "ts":pd.to_datetime(["2026-01-01","2026-01-05","2026-01-20","2026-01-02","2026-01-18","2026-01-25","2026-01-03","2026-01-22"])})
cut = pd.Timestamp("2026-01-15")
train, test = ev[ev.ts < cut], ev[ev.ts >= cut]
seen = train.groupby("user")["item"].apply(set)
test = test[test.user.isin(seen.index)]
test = test[[i not in seen[u] for u, i in zip(test.user, test.item)]]
print(test[["user","item"]])   # (1,c) (2,d) (2,e) (3,c)
```

**Follow-ups:**
- *How many folds?* Rolling-origin (expanding window) backtests to see stability.
- *Reconsumption (music, groceries)?* Keep repeats in the truth if repeat consumption is a goal.

**Common mistakes:** Random k-fold; features built from the full dataset; evaluating on users with no train history without saying so; sampled-negative metrics treated as absolute.

### Q14 ⭐⭐⭐ 🟡 How do you sample negatives for implicit-feedback training (random, popularity-based, hard negatives, in-batch)? What are the trade-offs?
**Asked at:** MLE roles; retrieval/ranking teams

**Say this first (1 line):** With implicit data we only see positives, so we must pick negatives from unobserved items; the choice sets what the model learns: random negatives are easy and give broad coverage, hard negatives sharpen the boundary but risk false negatives, and a mix is standard.

**Then explain:**
| Strategy | Pros | Cons |
|---|---|---|
| Uniform random | Simple, unbiased over catalogue, cheap | Too easy; model learns "popular vs obscure" and stops improving |
| Popularity-based (p ~ freq^0.75, word2vec-style) | Harder, matches what users could see | Pushes against popular items if overdone; needs tuning |
| Hard negatives (ANN neighbours of the positive, or items ranked high by current model) | Best gains at top of the list | Many "negatives" are real unclicked-but-liked items (false negatives); can destabilise training |
| Impressed-not-clicked | Real signal that user saw it | Biased by old ranker; position-dependent; use as extra, not only source |
| In-batch | Free (reuse other rows' positives), scales to big batches | Follows popularity distribution, so over-penalises popular items (fix: logQ correction, Q29) |
- **Practical recipe:** in-batch + a few random negatives + a small share of hard negatives mined from the previous model checkpoint; ramp hard negatives in later (curriculum).
- Sample more negatives per positive (5 to 100s) for pairwise/softmax losses; more helps with diminishing returns.
- Filter out items the user actually interacted with from their negatives.

**Example:** Two-tower retrieval for music: negatives = 1 in-batch set of 4096 + 256 random tracks + 64 ANN neighbours of the positive that the user never played.

**Follow-ups:**
- *False negatives?* Drop negatives too similar to a positive, or down-weight them.
- *Why does evaluation disagree with training negatives?* Train with sampled, evaluate against the full catalogue.

**Common mistakes:** Only random negatives; only hard negatives from step 0; using all unclicked impressions as true negatives; not excluding the user's own positives.

### Q15 ⭐⭐⭐ 🟡 Walk through how you would build a recommender for an e-commerce / food-delivery / music app: data, labels, candidate sources, ranker features, metrics. (Full end-to-end design belongs to Part 11; answer at model level here.)
**Asked at:** Flipkart/Swiggy/Amazon-type and Spotify-type teams; DS and MLE

**Say this first (1 line):** I would build a two-stage system: several candidate sources produce a few hundred items, a gradient-boosted or deep ranker predicts engagement, and a re-ranker adds diversity and business rules; I would pick labels and metrics that match the business goal, not just clicks.

**Then explain (model-level framework):**
- **Goal and labels:** e-commerce: purchase (strong), add-to-cart, click (weak); food delivery: order, with restaurant open and delivery time constraints; music: stream completion above 30 s, save, skip as negative. Weight by signal strength or train multi-task (Q23).
- **Data:** interaction logs with *exposure* (what was shown, position), item catalogue, user profile, context (time, location, device). Time-based splits (Q13).
- **Candidate sources:** personalised two-tower/ALS, item-to-item "similar to last viewed/ordered", recently viewed or reorder, trending by city/segment, new-item exploration slot. Merge and de-duplicate.
- **Ranker features:** user (history aggregates, recency, price affinity), item (category, price, rating, CTR, freshness, availability), context (hour, weather, location), cross (user-category affinity, distance, ETA), embedding similarity from retrieval. LightGBM lambdarank or a DLRM-style net.
- **Re-rank:** diversity (MMR), dedupe, remove out-of-stock, enforce ads/seller caps.
- **Metrics:** offline recall@K (retrieval), NDCG@k and AUC (ranker), calibration; online CTR, conversion, GMV/order frequency, retention, plus guardrails (latency, diversity, cancellations). Cold-start slices.

**Example:** Food delivery: candidates = reorder favourites + nearby similar restaurants + trending; features include ETA, price vs user's median; label = order within session; metric = orders per session with cancellation rate as guardrail.

**Follow-ups:**
- *How would you start with little data?* Popularity by segment plus content similarity, log exposure, move to ML once enough volume.
- *What's different for music?* Sequence and session context matter more; skip is a strong negative.

**Common mistakes:** Jumping to a deep model with no baseline (popularity, item-item); optimising CTR only; no exposure logging; ignoring availability and business constraints; random-split evaluation.

### Q16 ⭐⭐ 🟢 Cosine similarity vs dot product vs Euclidean distance for embeddings: when do they give different rankings, and why normalise?
**Asked at:** ML breadth rounds; retrieval roles

**Say this first (1 line):** Dot product depends on both direction and length, cosine only on direction, and Euclidean distance on both; they rank differently whenever vector norms vary, and I normalise when length is noise (e.g. popularity) rather than signal.

**Then explain:**
- **Dot product:** a.b = |a||b|cos. Long vectors win. In MF/two-tower, norm often encodes popularity or confidence, which can be good (and bad: popularity bias).
- **Cosine:** a.b / (|a||b|), range [-1, 1]. Ignores length; compares topics or direction.
- **Euclidean:** |a - b|. For unit-length vectors, |a - b|^2 = 2 - 2 cos, so cosine and Euclidean give the *same ranking*.
- **Normalise** (L2) so that a prolific user or popular item with a huge norm does not dominate, and so ANN indexes (cosine = inner product on unit vectors) are consistent. Use the unnormalised dot product if you want popularity or magnitude to count.
- **Training/serving must match:** if training used dot product, serve with dot product (ANN with MIPS or an augmenting trick).

**Example / Code:** query a = (1, 0). Dot product prefers the big off-angle vector; cosine prefers the aligned one; Euclidean also prefers the aligned one.
```python
import numpy as np
a = np.array([1.0, 0.0])
items = {"popular_big": np.array([4.0, 3.0]), "niche_aligned": np.array([0.9, 0.0]), "off_topic": np.array([0.0, 2.0])}
for n, v in items.items():
    print(f"{n:14s} dot={a@v:5.2f} cos={a@v/np.linalg.norm(a)/np.linalg.norm(v):5.2f} euclid={np.linalg.norm(a-v):5.2f}")
# popular_big    dot= 4.00 cos= 0.80 euclid= 4.24
# niche_aligned  dot= 0.90 cos= 1.00 euclid= 0.10
# off_topic      dot= 0.00 cos= 0.00 euclid= 2.24
```

**Follow-ups:**
- *Cosine with ANN?* Normalise both sides, then use inner-product index.
- *High dimensions?* Euclidean distances concentrate; cosine/dot is more informative.

**Common mistakes:** Saying cosine and Euclidean always differ (they agree on unit vectors); normalising at serving but not training; ignoring that norm may carry popularity signal.

### Q17 ⭐⭐ 🟢 Why is RMSE a poor metric for top-N recommendation on implicit data? What should you use instead?
**Asked at:** DS rounds at product cos and GCCs

**Say this first (1 line):** RMSE measures how close predicted ratings are to observed ones, but top-N recommendation is about getting the right items to the top of a list, and implicit data has no ratings to be close to.

**Then explain:**
- **Wrong target:** a model with great rating accuracy on average items can still rank the best items poorly; errors in the middle of the list cost the same as errors at the top.
- **Wrong population:** RMSE is computed on observed ratings only, which users chose to give (selection bias); it says nothing about the unobserved items we actually rank.
- **Implicit data:** values are 0/1 or counts; "0" means unknown, so squared error on it is meaningless.
- **Use instead:** recall@k, precision@k, MAP, NDCG@k, hit rate, MRR for ranking; coverage, diversity, novelty for list quality; calibration if probabilities are used; online CTR/conversion/retention. Evaluate against all candidates, with time-based split (Q13).
- RMSE still fine for true explicit-rating prediction or as a feature-model sanity check.

**Example:** Model A predicts every item as 3.8 (global mean) - RMSE looks good on a skewed rating set but ranks arbitrarily; model B has slightly worse RMSE but puts the user's actual future purchases in the top 10. B wins NDCG@10.

**Follow-ups:**
- *Netflix prize lesson?* The RMSE-winning ensemble was never deployed; the problem moved to ranking and implicit signals.
- *What about AUC?* OK for pointwise classification, but it ignores position.

**Common mistakes:** Reporting RMSE on clicks; sampling a handful of negatives and calling the metric absolute; ignoring selection bias in which ratings exist.

### Q18 ⭐⭐ 🟡 Pointwise vs pairwise vs listwise learning-to-rank: how do the losses differ and when would you use each?
**Asked at:** Search/ranking teams

**Say this first (1 line):** Pointwise predicts a score per item independently (regression or classification), pairwise learns which of two items should rank higher, and listwise optimises a loss defined over the whole list, closest to what NDCG measures.

**Then explain:**
| Approach | Loss | Example | Pros | Cons |
|---|---|---|---|---|
| Pointwise | Log-loss / MSE on label | Logistic regression, GBDT classifier | Simple, calibrated probabilities, scales | Ignores relative order; treats all errors equally |
| Pairwise | Penalise mis-ordered pairs: log(1 + exp(-(s_i - s_j))) for i preferred over j | RankNet, BPR, LambdaRank's base | Learns order directly | O(pairs) cost; all pairs equally weighted unless lambda-weighted |
| Listwise | Defined on the permutation / list: ListNet (softmax cross-entropy over list), ListMLE, LambdaRank/LambdaMART (pairwise gradients scaled by delta-NDCG) | LambdaMART, softmax loss | Closest to the metric, best top-of-list | Needs query groups; no calibrated probabilities |
- **When:** pointwise when you need probabilities (ads CTR, calibration) or have only click/no-click; pairwise or listwise when only ordering matters and you have graded labels or query groups. LambdaMART is the strong default for tabular ranking features.
- Neural rankers in recsys often train with sampled softmax (listwise-like) over one positive + negatives.

**Example:** Search for "running shoes": labels 0-3 by editors. Pointwise regression predicts 2.6 vs 2.7 for two items with equal error, but if their true order is reversed, nothing penalises that. LambdaMART directly penalises the swap, more heavily if it is at rank 1-2.

**Follow-ups:**
- *Why does LambdaMART often beat pointwise on NDCG?* Gradients are weighted by how much the metric changes.
- *Can you mix?* Yes: pointwise heads for probabilities plus a rank loss.

**Common mistakes:** Using pointwise classification and judging by AUC alone; shuffling rows so query groups break; expecting calibrated probabilities from a rank loss.

### Q19 ⭐⭐ 🟡 Explain LambdaRank and LambdaMART. How do you train a ranker in XGBoost/LightGBM (query groups, objective, eval metric)?
**Asked at:** Search, ads, e-commerce ranking roles

**Say this first (1 line):** LambdaRank trains by giving each item a "lambda" gradient, the RankNet pairwise gradient multiplied by how much NDCG would change if the two items were swapped; LambdaMART plugs those lambdas into gradient-boosted trees, so the model optimises the ranking metric without needing its gradient.

**Then explain:**
- **RankNet:** for pair (i more relevant than j), loss = log(1 + exp(-(s_i - s_j))). Gradient lambda_ij = -1 / (1 + exp(s_i - s_j)).
- **LambdaRank:** multiply by |delta NDCG_ij| (the change if i and j swap positions). Pairs near the top, with a big gain difference, get big gradients; swaps deep in the list get small ones. No explicit loss, just these gradients (Q46).
- **LambdaMART:** MART = gradient-boosted regression trees. Each tree fits the lambdas (per-item sum over its pairs), with Newton-style leaf values from second derivatives.
- **In LightGBM/XGBoost:** `objective="lambdarank"` (LightGBM) or `rank:ndcg` / `rank:pairwise` (XGBoost). Provide **query groups**: rows must be contiguous per query and `group` lists the size of each query. Labels are non-negative ints (graded relevance). Eval metric `ndcg@k`; use a validation set of *whole queries* (split by query, never within one).
- Useful knobs: `lambdarank_truncation_level`, `label_gain` (default 2^l - 1), `eval_at`.

**Example:** A product-search team has 300 queries, each with 20 candidate products graded 0-3. We train on the first 240 queries and validate on the other 60. The synthetic run below reaches NDCG@5 of about 0.90 against about 0.37 for a random ordering. Both numbers come from toy data, not a benchmark.

**Code (LightGBM, synthetic 300 queries x 20 docs; takes about 40 s on a laptop, hence `n_jobs=1`):**
```python
import numpy as np, lightgbm as lgb
from sklearn.metrics import ndcg_score
rng = np.random.default_rng(0); nq, per = 300, 20
X = rng.normal(size=(nq*per, 5))
s = X[:, 0] + .5*X[:, 1] + rng.normal(0, .5, nq*per)
y = np.digitize(s, np.quantile(s, [.5, .8, .95]))          # labels 0..3
tr, va = slice(0, 240*per), slice(240*per, None)           # split by whole queries
m = lgb.LGBMRanker(objective="lambdarank", n_estimators=100, learning_rate=.1,
                   min_child_samples=5, random_state=0, n_jobs=1, verbose=-1)
m.fit(X[tr], y[tr], group=[per]*240, eval_set=[(X[va], y[va])],
      eval_group=[[per]*60], eval_at=[5], eval_metric="ndcg")
p = m.predict(X[va])
print(round(ndcg_score(y[va].reshape(60, per), p.reshape(60, per), k=5), 3))               # 0.902
print(round(ndcg_score(y[va].reshape(60, per), rng.random((60, per)), k=5), 3))            # 0.372 (random)
```

**Follow-ups:**
- *Why GBDT, not a neural net?* Strong on tabular features, fast, robust; deep rankers win with sparse/ID features at scale.
- *Position bias in labels?* Use unbiased LambdaMART (Q44).

**Common mistakes:** Wrong or unsorted groups (silent garbage); random row split across queries; float labels; judging by AUC; queries with all-equal labels contribute nothing.

### Q20 ⭐⭐ 🟡 How does approximate nearest neighbour search work? Compare HNSW, IVF-PQ and ScaNN/FAISS indexes on recall, latency, memory and updates.
**Asked at:** MLE / retrieval teams; RAG-adjacent loops

**Say this first (1 line):** Exact nearest-neighbour search compares the query with every vector (O(N d)), too slow at millions; ANN builds an index so it looks at only a small part of the data and returns neighbours that are almost always the true ones, trading a little recall for large speedups.

**Then explain:**
| Index | Idea | Recall / latency | Memory | Updates |
|---|---|---|---|---|
| **HNSW** | Multi-layer proximity graph; greedy walk from sparse top layer down | Very high recall, low latency | High (vectors + graph links) | Insert is easy; deletes awkward (tombstones) |
| **IVF** (inverted file) | k-means cells; search the `nprobe` nearest cells only | Good; recall rises with nprobe | Low-moderate | Add easy, retrain centroids as data drifts |
| **IVF-PQ** | IVF + product quantisation: split vector into sub-vectors, store small codes | Lower recall (lossy), fast | Very low (10-100x smaller) | Good for billions; retrain for drift |
| **ScaNN** | Partitioning + anisotropic quantisation tuned for inner product, then re-score | High recall for MIPS | Moderate | Rebuild-oriented |
| **FAISS** | A library implementing IVF, PQ, HNSW, flat, GPU | Depends on index | - | - |
- **Knobs:** HNSW `M`, `efSearch`; IVF `nlist`, `nprobe`; PQ code size. Higher = better recall, slower.
- **Choose:** up to tens of millions and RAM available -> HNSW; hundreds of millions or billions / memory limited -> IVF-PQ (often with re-ranking by exact distance on the shortlist); frequently updated -> HNSW or periodic rebuild with a delta index.
- **Filtering** (in-stock, region) is hard: pre-filter, post-filter, or filtered-graph variants.

**Example (back-of-envelope arithmetic; latency and recall depend on hardware and tuning, so measure them):** 100M items, 128-d float32 is about 51 GB raw; PQ with 16 bytes per vector is about 1.6 GB plus overhead, so IVF-PQ fits comfortably in RAM on one machine, whereas HNSW needs the raw vectors plus graph links (well over 51 GB) and would be sharded or use a big-memory box.

**Follow-ups:**
- *How do you measure ANN quality?* Recall@k against brute-force ground truth on a sample, versus latency (QPS at fixed recall).
- *Why re-rank after PQ?* Compressed distances are approximate.

**Common mistakes:** Quoting a single "best" index; forgetting memory; tuning on recall alone ignoring p99 latency; metric mismatch (cosine vs inner-product index); not rebuilding after model changes.

### Q21 ⭐⭐ 🟡 Exploration vs exploitation in recommenders: epsilon-greedy, UCB, Thompson sampling. How would you inject exploration for new items?
**Asked at:** Senior DS/MLE; media, marketplaces

**Say this first (1 line):** If you only show what you currently think is best (exploit), you never learn about new or under-shown items; exploration spends a little traffic on uncertain items so future recommendations improve. Thompson sampling is my default.

**Then explain:**
- **Epsilon-greedy:** with prob. epsilon show a random item, otherwise the best. Simple, but explores blindly and forever.
- **UCB:** pick the item with the highest (mean + uncertainty bonus, e.g. sqrt(2 ln t / n)). Deterministic, explores items with few trials; sensitive to the bonus constant.
- **Thompson sampling:** keep a posterior per item (Beta(clicks+1, misses+1) for CTR), sample from each, show the highest sample. Explores in proportion to the chance an item is best, usually best in practice and easy to implement.
- **New-item exploration:** reserved slots (e.g. 5%), bandit over new items per context, bonus based on uncertainty (low impressions), start from a content-based prior CTR, cap impressions budget per item.
- **Costs:** short-term engagement loss; need unbiased logging (store the propensity of each shown item for later off-policy evaluation).

**Example / Code:** 4 items with CTR 4%, 5%, 6%, 10%, 5000 impressions, cumulative regret (lost clicks vs always showing the best), averaged over 10 runs:
```python
import numpy as np
rng = np.random.default_rng(0)
p = np.array([0.04, 0.05, 0.06, 0.10]); T = 5000
def run(policy):
    a = np.ones(4); b = np.ones(4); n = np.zeros(4); s = np.zeros(4); reg = 0
    for t in range(T):
        if policy == "eps": arm = rng.integers(4) if rng.random() < .1 else np.argmax(s/np.maximum(n, 1))
        elif policy == "ucb": arm = t if t < 4 else np.argmax(s/n + np.sqrt(2*np.log(t+1)/n))
        else: arm = np.argmax(rng.beta(a, b))
        r = rng.random() < p[arm]; n[arm] += 1; s[arm] += r; a[arm] += r; b[arm] += 1 - r
        reg += p.max() - p[arm]
    return reg
for pol in ("eps", "ucb", "ts"):
    print(pol, round(np.mean([run(pol) for _ in range(10)]), 1))
# eps 65.6   ucb 133.8   ts 33.2
```
Thompson has the lowest regret here; UCB with this bonus constant over-explores when CTRs are small (it can be tuned).

**Follow-ups:**
- *Contextual?* LinUCB / linear Thompson using user and item features (Q45).
- *How do you evaluate?* Log propensities; use IPS/doubly robust (Q32).

**Common mistakes:** Treating epsilon-greedy as enough; exploring without logging propensities; ignoring non-stationarity (CTR drifts; use decay); letting new items eat unlimited traffic.

### Q22 ⭐⭐ 🟡 How do you add diversity, novelty, serendipity and freshness to a ranked list? Explain MMR/DPP re-ranking and how you would measure it.
**Asked at:** Product cos; media (Spotify-type)

**Say this first (1 line):** A pure relevance sort fills the list with near-duplicates, so I add a re-ranking step that trades a little relevance for variety: MMR greedily picks items that are relevant but dissimilar to what is already chosen, and DPP does the same with a probabilistic set-level model.

**Then explain:**
- **Definitions:** *Diversity* = items differ from each other; *novelty* = items the user has not seen or are not popular; *serendipity* = relevant and surprising; *freshness* = recent items.
- **MMR (maximal marginal relevance):** pick next item = argmax lam * relevance(i) - (1 - lam) * max similarity(i, already chosen). lam = 1 is plain relevance. Greedy, O(k N) similarity checks, easy to ship.
- **DPP (determinantal point process):** score a set by det of a kernel matrix combining quality and similarity; larger when items are both good and different. Greedy MAP inference is cheap enough for production (e.g. YouTube, Hulu-style feeds); more principled than MMR, a bit harder to tune.
- **Other levers:** category caps/slot rules ("max 2 per artist"), freshness boosts or decay, exploration slots.
- **Measure:** intra-list distance (ILD, mean pairwise dissimilarity), coverage, category entropy, novelty (mean -log popularity), serendipity (relevant but unexpected vs a baseline), and online: session length, retention, skip rate. Always show the relevance-diversity trade-off curve.

**Example / Code:** 50 items in 5 "genres", genre 0 is most relevant, so top-10 by relevance is dominated by it. MMR with lam = 0.5 barely lowers mean relevance but raises ILD:
```python
import numpy as np
rng = np.random.default_rng(0)
centers = rng.normal(size=(5, 8)); cl = rng.integers(0, 5, 50)
E = centers[cl] + .3 * rng.normal(size=(50, 8)); E /= np.linalg.norm(E, axis=1, keepdims=True)
rel = rng.random(50) + 0.4 * (cl == 0)
def mmr(rel, E, k, lam=0.5):
    chosen, cand = [], list(range(len(rel))); S = E @ E.T
    while len(chosen) < k:
        best = max(cand, key=lambda i: lam*rel[i] - (1-lam)*(max(S[i, chosen]) if chosen else 0))
        chosen.append(best); cand.remove(best)
    return chosen
def ild(ids): S = E[ids] @ E[ids].T; k = len(ids); return 1 - (S.sum() - k) / (k*(k-1))
top = list(np.argsort(-rel)[:10]); m = mmr(rel, E, 10)
print("top-10: rel %.2f ILD %.2f" % (rel[top].mean(), ild(top)))   # rel 1.01 ILD 0.77
print("MMR   : rel %.2f ILD %.2f" % (rel[m].mean(), ild(m)))       # rel 0.97 ILD 0.84
```

**Follow-ups:**
- *How to choose lam?* Pick on the Pareto curve; confirm with A/B on retention, not CTR.
- *Where in the pipeline?* After ranking, on the top 50-100.

**Common mistakes:** Diversifying with the same embedding that ranked (similarity then reflects relevance); equating diversity with serendipity; measuring only offline relevance and concluding diversity "hurts".

### Q23 ⭐⭐ 🟡 Your system predicts click, add-to-cart, purchase and dwell time. How do you combine multiple objectives into one ranking (scalarisation, multi-task learning, constraints)?
**Asked at:** Senior DS/MLE; e-commerce, feeds

**Say this first (1 line):** I predict each outcome with its own calibrated probability (multi-task model), then combine them into one score with business weights, e.g. score = p(click) x (w1 + p(purchase | click) x value), tuned online, with hard constraints for things that must not break.

**Then explain:**
- **Multi-task learning (MTL):** shared bottom or MMoE/PLE experts with one head per objective (click, cart, purchase, dwell). Shares signal from dense labels (clicks) to sparse ones (purchases). Watch negative transfer.
- **Scalarisation:** final = sum w_k * f(p_k). Chain rule is more principled: expected value = P(click) x P(buy | click) x margin. Weights come from business value, then fine-tuned via A/B or Bayesian optimisation on online metrics.
- **Constraints instead of weights:** maximise purchases subject to dwell/return rate, delivery time, ad load, diversity cap (Lagrangian or filters). Easier to explain to stakeholders.
- **Calibration matters:** blending needs comparable probabilities (Q33); dwell time is regression, so transform it (log, clip).
- **Watch for:** objective conflict (clickbait vs satisfaction, Q24), Pareto trade-offs, delayed labels for purchase (use delay-aware training).

**Example:** E-commerce: score = p_click x (1 + 3 x p_cart + 10 x p_buy x margin_norm). A new weight set is released to 5% of traffic, judged on GMV, conversion and a guardrail (returns, latency).

**Follow-ups:**
- *Why not train a single model on purchase only?* Too sparse; click and cart supervise representations.
- *How to pick weights?* Business value mapping, then online search; present the Pareto frontier.

**Common mistakes:** Adding raw scores on different scales; treating clicks and purchases as equal; ignoring delayed conversion labels; tuning weights offline only.

### Q24 ⭐⭐ 🟡 CTR is up but retention or long-term satisfaction is falling (clickbait ranks high). What is going on and what do you change?
**Asked at:** Product cos, feeds, media

**Say this first (1 line):** CTR is a short-term proxy; if I optimise it alone the model learns to promote clickbait (eye-catching, low-value items), which gets clicks but disappoints users, so I change the objective to measure satisfaction, not just attention.

**Then explain:**
- **Why it happens:** Goodhart's law. Clicks are cheap, easy to measure and respond to titles/thumbnails; value (watch completion, return visits, purchases, satisfaction) is delayed and sparse. The feedback loop then reinforces more clickbait.
- **Diagnose:** look at post-click behaviour (bounce, dwell, completion, hides, "not interested", returns/refunds), cohort retention by exposure to the top-ranked content, content-quality audit of top items, CTR vs satisfaction by item.
- **Change:**
  - Labels: long-click/dwell > threshold, completion, saves, purchase kept, survey responses (satisfaction). Penalise quick bounces and negative feedback.
  - Multi-objective score (Q23) including predicted satisfaction and a quality prior; constraints on clickbait signals.
  - Features/ranking penalties for title-body mismatch, low-quality sources.
  - Evaluate with long-running holdouts: retention at 7/28 days, not just session CTR.
  - Add diversity and exploration so the system is not stuck in the high-click corner.
- **Trade-off:** short-term CTR will dip; sell the change on retention and lifetime value.

**Example (illustrative numbers):** Video feed: new ranker lifts CTR 4% but 7-day retention drops 1%. Reweighting to predicted watch-completion and adding a hide-rate penalty reduces CTR 2% but retention recovers and rises after 4 weeks.

**Follow-ups:**
- *How to run the experiment?* Long-term A/B or a persistent holdout; use surrogate metrics that predict retention.
- *How do you know satisfaction labels are valid?* Validate against survey or retention correlation.

**Common mistakes:** Treating CTR drop as failure; adding "quality" with no validation; watching only session-level metrics; not segmenting (new users vs heavy users).

### Q25 ⭐⭐ 🟡 Compare SVD, truncated SVD, ALS, NMF and SVD++ for recommendations. What do user/item bias terms and regularisation do?
**Asked at:** Classical ML breadth rounds; GCCs

**Say this first (1 line):** They are all low-rank factorizations, but they differ in how they treat missing entries and constraints: plain SVD needs a full matrix, truncated SVD keeps the top-k components, ALS and SGD-based MF train only on observed entries, NMF forces non-negative factors, and SVD++ adds implicit feedback to the user vector.

**Then explain:**
| Method | Key idea | Handles missing? | Notes |
|---|---|---|---|
| SVD (full) | A = U S V^T exactly | No (needs complete matrix) | Not used directly on sparse ratings |
| Truncated SVD | Keep top-k singular values | Only if you fill (zeros or mean-centred), which biases | Fast on sparse matrices (LSA, item embeddings) |
| ALS | Alternate closed-form ridge solves | Yes, via mask/weights | Parallel; good for implicit with confidence weights |
| "Funk SVD" / SGD MF | SGD on observed ratings with L2 | Yes | Flexible, add biases |
| NMF | A ~ W H with W, H >= 0 | Usually zero-filled unless masked variants | Parts-based, interpretable topics |
| SVD++ | r = mu + b_u + b_i + q_i . (p_u + sum of implicit item vectors / sqrt(|N(u)|)) | Yes | Uses which items user rated/viewed, strong on Netflix-prize style data; slower |
- **Bias terms:** b_u and b_i soak up "this user rates high" and "this item is great". Without them the latent factors waste capacity on averages.
- **Regularisation (L2 on factors and biases):** shrinks factors toward 0, so users/items with few interactions fall back to biases and the global mean, preventing overfitting on sparse data. Tune lambda with validation.
- Pitfall: calling SGD-trained MF "SVD"; it is not an SVD of the matrix.

**Example:** User with 2 ratings: unregularised factors fit those 2 points perfectly and produce wild predictions; with L2 their vector stays small so the prediction is about mu + b_u + b_i.

**Follow-ups:**
- *Which for implicit?* ALS with confidence weights or BPR/two-tower; not plain SVD on counts.
- *Why mean-centre before truncated SVD?* Otherwise first component just captures the mean.

**Common mistakes:** Zero-filling missing and treating it as a rating; no biases; no regularisation; confusing SVD with funk-SVD; using NMF on mean-centred (negative) data.

### Q26 ⭐⭐ 🟡 Search relevance: TF-IDF vs BM25 vs dense retrieval vs hybrid search. When does each fail?
**Asked at:** Search teams; e-commerce, Booking-style travel

**Say this first (1 line):** TF-IDF and BM25 match exact words (fast, precise, explainable), dense retrieval matches meaning through embeddings (handles synonyms, misses exact tokens), and hybrid search combines both, which is what I would ship.

**Then explain:**
| Method | How it scores | Fails when |
|---|---|---|
| TF-IDF | term frequency x rarity of the term | Long docs favoured; no saturation; no length control |
| BM25 | TF-IDF with term-frequency saturation (k1) and length normalisation (b) | Vocabulary mismatch: "sneakers" vs "trainers"; typos; no word order |
| Dense (bi-encoder) | cosine of query and doc embeddings | Rare tokens, SKUs, model numbers, names; out-of-domain text; hard to debug |
| Hybrid | BM25 and dense scores fused (RRF or learned weights), then a reranker | Costs two indexes; fusion weights need tuning |
- **BM25** score per query term = idf x tf(k1+1) / (tf + k1(1 - b + b x len/avglen)). Typical k1 about 1.2, b about 0.75. Saturation means the 10th occurrence of a word adds little.
- **Reciprocal rank fusion (RRF):** score = sum over lists of 1/(60 + rank). It needs no score calibration, which is why it is the default hybrid.
- Typical stack: BM25 + dense retrieve top few hundred, cross-encoder or LTR reranks the top 50 (Q37).

**Example:** Query "iphone 15 128gb black": BM25 nails the exact model tokens; dense alone may return iPhone 14 or Samsung phones. Query "something warm for hiking in the rain": BM25 finds nothing useful, dense finds waterproof jackets.

**Code:** (BM25 from scratch, run on a toy corpus)
```python
import numpy as np
from collections import Counter
docs = ["red running shoes for men", "blue running shoes", "leather office shoes for men",
        "wireless bluetooth headphones", "running shorts for women", "men running jacket red"]
tok = [d.split() for d in docs]
N = len(tok); avgdl = np.mean([len(t) for t in tok])
df = Counter(w for t in tok for w in set(t))
def bm25(q, t, k1=1.2, b=0.75):
    tf = Counter(t); s = 0.0
    for w in q.split():
        if w not in tf: continue
        idf = np.log(1 + (N - df[w] + 0.5) / (df[w] + 0.5))
        s += idf * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * len(t) / avgdl))
    return s
q = "red running shoes"
for s, d in sorted([(bm25(q, t), d) for t, d in zip(tok, docs)], reverse=True)[:3]:
    print(round(s, 2), d)
```
Output: `1.96 red running shoes for men`, `1.47 men running jacket red`, `1.26 blue running shoes`.

**Follow-ups:**
- *Why not just dense?* Exact-match queries (IDs, brands) and explainability; BM25 is a strong, cheap baseline that dense often loses to out of domain.
- *How do you fine-tune dense?* Click or purchase pairs as positives, hard negatives from BM25 top results.

**Common mistakes:** Saying "dense replaces BM25"; mixing raw BM25 and cosine scores without normalisation or RRF; no evaluation split by query type (head, tail, exact-ID).

### Q27 ⭐⭐ 🟡 How do you evaluate a search/ranking system online and offline: relevance labels, click models, interleaving, A/B tests?
**Asked at:** Search/ranking roles; Booking.com-type hotel ranking

**Say this first (1 line):** Offline I score the ranker on labelled or click-derived relevance with NDCG/MRR; online I use interleaving for fast, sensitive comparisons and a full A/B test on business metrics (conversion, revenue, retention) to make the ship decision.

**Then explain:**
- **Relevance labels:** human raters (graded 0-4 scale, with guidelines and agreement checks), implicit labels from clicks/purchases (cheap but biased), or LLM judges (Q39). Compute NDCG@k, MRR, precision@k on a fixed query set, sliced by head/torso/tail queries.
- **Click models:** clicks are biased by position and trust. Position-based or cascade models separate "was examined" from "was relevant" so click logs become usable labels (Q44).
- **Interleaving:** mix results of rankers A and B in one list (team-draft); the ranker whose items get more clicks wins. Often needs far fewer queries than A/B for the same sensitivity (published comparisons report roughly an order of magnitude or more), but only measures preference, not revenue.
- **A/B test:** randomise users (not queries, to avoid carry-over), pre-register the primary metric (conversion or revenue per search), guardrails (latency, zero-result rate, abandonment), check sample-ratio mismatch, and run at least a full week for weekday effects.
- **Pipeline:** offline gate (no regression on golden set) -> interleaving screen -> A/B on the winners.

**Example (illustrative numbers):** Hotel search: new ranker raises offline NDCG@10 from 0.62 to 0.65. Interleaving says it wins 54% of decisive queries. A/B shows +0.8% bookings, with no increase in cancellations. Ship.

**Follow-ups:**
- *Offline gain, online flat. Why?* Labels do not match user intent, position bias in labels, offline set not representative, or latency/UX effects.
- *Why not interleaving only?* It cannot capture whole-page effects or long-term metrics.

**Common mistakes:** Evaluating on click-trained labels the old ranker produced (self-confirming); NDCG only on head queries; randomising by query and leaking users across arms; no guardrails.

### Q28 ⭐⭐ 🟡 How are item embeddings learned (item2vec/prod2vec, session co-occurrence)? What are the pitfalls (popularity, window size, sparse items)?
**Asked at:** E-commerce, travel, music

**Say this first (1 line):** Item2vec treats each user session as a "sentence" of item IDs and trains word2vec (skip-gram with negative sampling), so items that appear in similar contexts get nearby vectors.

**Then explain:**
- **Prod2vec / item2vec:** sessions are sequences; the window defines "context"; the model learns a vector per item so that co-occurring items have high dot product. Used for similar-item retrieval, candidate generation and as features.
- **Pitfalls:**
  - **Popularity:** popular items dominate pairs. Word2vec's negative sampling uses unigram^0.75, and frequent-item subsampling helps; otherwise neighbours of everything are the top sellers.
  - **Window size:** small window gives "substitutes" (similar functionality), large window gives "complements/topical" relatedness. Pick for the use case (similar items vs "also bought").
  - **Sparse and cold items:** items with few sessions get noisy vectors. Set a min count, add content features (text/image) or train a side-info model (e.g. Airbnb's listing embeddings used booking-as-global-context and cluster-based cold start).
  - **Session noise:** bots, long sessions, unrelated browsing; cut sessions at inactivity gaps and cap length.
  - **Evaluation:** offline hit-rate on next item, plus manual neighbour checks; vectors are not comparable across retrainings (Q49).
- **Alternative:** matrix factorization of the item co-occurrence matrix (PMI) is close to what skip-gram implicitly does.

**Example:** Music: window 5 on listening sessions gives songs of the same genre; window 2 on playlists gives near-identical artists/remixes.

**Follow-ups:**
- *Why not just count co-occurrence?* Counts are sparse and dominated by popular items; embeddings generalise and compress.
- *Does order matter?* Skip-gram ignores order inside the window; use sequence models (Q31) if order matters.

**Common mistakes:** No popularity handling; one window size for all uses; training on all events including bot sessions; treating cosine neighbours as complements when they are substitutes.

### Q29 ⭐⭐ 🟡 In-batch negatives in two-tower training bias the model towards popular items. How do logQ correction or mixed negative sampling fix it?
**Asked at:** MLE roles at product cos

**Say this first (1 line):** With in-batch negatives, popular items appear as negatives in proportion to their popularity, which is not uniform sampling; logQ correction subtracts log of each item's sampling probability from its logit so the softmax is unbiased, and mixed negative sampling adds uniformly sampled negatives to cover rare items.

**Then explain:**
- **Why bias:** negatives in a batch are other users' positives, so item i is drawn with probability q_i proportional to its popularity. So popular items are over-penalised as negatives (their scores are pushed too low) and rare items are under-penalised (rarely seen as negatives, so scored too high). The sampled softmax estimates the wrong partition function.
- **logQ correction (Yi et al., Google 2019):** use logit' = s(u, i) - log q_i in the softmax loss (at training time only). At serving time use raw s(u, i). q_i is estimated by streaming frequency counts.
- **Mixed negative sampling (MNS):** in-batch negatives plus a second set drawn uniformly from the catalogue (extra item tower forward passes). Gives tail items a chance to be negatives; often combined with logQ.
- **Other levers:** hard negatives (ANN-mined near misses), but add them carefully because false negatives creep in; larger batches; cross-batch memory.
- Remember the other side: removing popularity bias entirely can hurt, since popularity is a genuine signal. Check with a popularity-sliced recall.

**Example (illustrative):** Item A is 100x more common than item B. Without correction, A is a negative in 100x as many batch comparisons, so its score is suppressed relative to its true relevance and B's is inflated; subtracting log q fixes the relative levels.

**Follow-ups:**
- *Why only subtract at training?* The correction fixes the sampling distribution of the loss; at serving we rank by true affinity.
- *Why not sample negatives uniformly only?* Easy negatives teach little; in-batch gives informative, free negatives.

**Common mistakes:** Applying logQ at inference; sign error (it is minus); not handling duplicate items in a batch (same item as positive and negative); stale frequency estimates.

### Q30 ⭐⭐ 🟡 Wide & Deep, DeepFM, DLRM: why do ranking models need explicit feature crosses and how do these architectures provide them?
**Asked at:** Ads / e-commerce ranking MLE

**Say this first (1 line):** CTR depends on feature interactions (user x item, device x time, category x price) and MLPs learn these slowly and inexactly, so these architectures add an explicit cross component: Wide & Deep uses hand-made crosses in a linear part, DeepFM learns all pairwise crosses with a factorization machine, and DLRM does dot-product interactions between embeddings.

**Then explain:**
- **Why explicit crosses:** most CTR features are high-cardinality categoricals turned into embeddings. A plain MLP on concatenated embeddings must discover multiplicative effects through ReLU layers; in practice it does this poorly (Beutel et al. 2018, "Latent Cross"), and explicit crosses are cheap, interpretable and give a strong gain.
- **Wide & Deep (Google, 2016):** wide = linear model over sparse crosses (memorisation, e.g. installed_app x impression_app); deep = MLP on embeddings (generalisation). Trained jointly. Needs manual feature engineering for the wide side.
- **DeepFM:** FM part computes all pairwise dot products of field embeddings (order-2 interactions) and shares embeddings with the deep part. No manual crosses.
- **DLRM (Meta):** sparse features to embeddings, dense features to a bottom MLP, pairwise dot products between all vectors, top MLP. Designed for huge embedding tables (model-parallel) and compute efficiency.
- **Others:** DCN/DCNv2 (explicit higher-order crosses via cross layers), xDeepFM, AutoInt.

**Example:** "Pizza ad x user at 8 pm" is only strongly positive for that combination. A linear model with a cross feature nails it with one weight; an MLP has to learn it from data in every region of embedding space.

**Follow-ups:**
- *When is a GBDT enough?* Smaller data, mostly dense features; GBDT models interactions through tree depth. Deep ranking models win at scale with high-cardinality sparse IDs.
- *Serving cost?* Embedding tables dominate memory; interactions are cheap.

**Common mistakes:** Saying MLPs "cannot" learn interactions (they can, inefficiently); forgetting that Wide & Deep's wide part needs manual crosses; ignoring embedding table size and hashing collisions.

### Q31 ⭐⭐ 🟡 Sequential and session-based recommendation: Markov chains, GRU4Rec, SASRec/BERT4Rec. When do they beat matrix factorization?
**Asked at:** Senior DS/MLE; e-commerce, music

**Say this first (1 line):** Sequence models beat matrix factorization when order and recency matter, when users are anonymous or have short sessions, and when intent drifts quickly; MF is a static taste profile and ignores what you did a minute ago.

**Then explain:**
- **Markov chain:** next item depends on the last 1-2 items (item-to-item transition counts). Simple, strong baseline for short sessions; fails with long-range intent and sparse transitions.
- **GRU4Rec:** an RNN reads the session click by click and scores the next item; trained with ranking losses (BPR/TOP1/sampled softmax). Works for anonymous sessions (no user ID needed).
- **SASRec:** causal self-attention over the user's history, predicts the next item at each position. Attends to the relevant past actions, parallel training, usually beats RNNs.
- **BERT4Rec:** bidirectional attention with masked-item (cloze) training. Its reported gains over SASRec are contested: a replicability study (Petrov and Macdonald, 2022) found it can win but only with much longer training than commonly used, and later work showed SASRec trained with a softmax/cross-entropy loss is often competitive. So do not claim it is simply better; compare under equal tuning.
- **When MF is enough:** stable tastes (books, movies), long histories, no strong sequence signal, tight latency. Always test a sequence-agnostic baseline.
- **Serving:** encode history to a user vector in real time, then ANN retrieval; or use the model as a ranker with the last-N items as features.

**Example:** E-commerce session: user views 3 phone cases. MF recommends their long-term favourite (running shoes); a sequence model recommends more phone cases and chargers.

**Follow-ups:**
- *How to evaluate?* Leave-last-out is common but flawed; prefer temporal split, sampled metrics with care (sampled negatives distort rankings; use full-catalogue ranking).
- *Cold-start users?* Session models need no profile, only a few clicks.

**Common mistakes:** Random train/test split (leaks future); evaluating on sampled negatives; assuming Transformers always win; ignoring serving latency for long histories.

### Q32 ⭐⭐ 🟡 Selection bias and counterfactual evaluation: explain inverse propensity scoring for offline evaluation of a new ranker and its variance problem (clipping, doubly robust).
**Asked at:** Senior DS; ads/recsys

**Say this first (1 line):** Logs only show feedback for what the old policy chose to show, so to estimate how a new ranker would do I reweight each logged event by new-policy probability / logging-policy probability (inverse propensity scoring); it is unbiased but can have huge variance, which clipping, self-normalisation and doubly robust estimators reduce.

**Then explain:**
- **IPS estimator:** V_hat = mean over logged events of w x r, where w = pi_new(a|x) / pi_log(a|x). Requires the logging policy to have **non-zero probability** for everything the new policy might pick (support/overlap) and logged propensities.
- **Variance problem:** a rare logged action that the new policy loves gets a huge weight, so a single event dominates the estimate. Variance grows with the weight spread; check the effective sample size.
- **Fixes:**
  - **Clipping** weights at M: cuts variance, adds bias (usually downward).
  - **Self-normalised IPS (SNIPS):** divide by sum of weights; small bias, much lower variance.
  - **Doubly robust (DR):** V = model-based estimate + IPS correction on the residual. Unbiased if either the propensities or the reward model is right, and low variance when the reward model is decent.
- **Practical:** log propensities at serving time, keep a small randomised exploration slice so overlap exists.

**Example:** (illustrative simulation, 200k logs, 5 items, logging policy 60% on item 0 and 3% on item 4, new policy the reverse; true value of new policy 0.0918)
```python
import numpy as np
rng = np.random.default_rng(0); n = 200_000
p_log = np.array([.60, .10, .10, .17, .03]); p_new = np.array([.03, .10, .10, .17, .60])
q = np.array([.05, .07, .08, .09, .10])          # true CTR per item (illustrative)
a = rng.choice(5, size=n, p=p_log); r = (rng.random(n) < q[a]).astype(float)
qhat = q * 0.8                                   # reward model that is 20% off
w = p_new[a] / p_log[a]                          # per-event importance weights
print("true ", round(p_new @ q, 4))              # 0.0918
print("ips  ", round(np.mean(w * r), 4))         # 0.0942
print("clip ", round(np.mean(np.minimum(w, 10) * r), 4))   # 0.0629 (biased low)
print("snips", round(np.sum(w * r) / np.sum(w), 4))        # 0.095
print("dr   ", round(np.mean(p_new @ qhat + w * (r - qhat[a])), 4))  # 0.0949
```
Run with seed 0: max weight 20, effective sample size about 16,100 of 200,000. Clipping at 10 visibly under-estimates here; that is the bias-variance trade-off made concrete.

**Follow-ups:**
- *What if the old policy was deterministic?* IPS is invalid (zero overlap); use the model-based direct method, or run a small randomised experiment first.
- *Position-based propensities?* For rankings use the position-bias propensity or a cascade assumption (Q44).

**Common mistakes:** Not logging propensities; ignoring overlap; clipping and calling it unbiased; judging a new ranker by its AUC on the old policy's logs.

### Q33 ⭐⭐ 🟡 Does a ranker's predicted probability need to be calibrated? When does it matter (ads, blending scores, thresholds) and how do you fix it?
**Asked at:** Ads, fintech, ranking roles

**Say this first (1 line):** If you only sort by score, calibration barely matters (only order does); it matters as soon as you multiply or add probabilities, compare against a threshold or a cost, or compute a bid, because then the number itself must mean what it says.

**Then explain:**
- **When it matters:**
  - **Ads:** expected revenue = bid x pCTR (x pCVR); a pCTR that is 30% too high overbids and hurts advertisers/auction efficiency.
  - **Blending scores** from different models or objectives (Q23): they must be on one probability scale.
  - **Thresholds:** "show only if p > 0.2", fraud/lending cut-offs, budget pacing.
  - **Downsampling negatives** during training shifts probabilities: correct with p = p_s / (p_s + (1 - p_s)/r) where p_s is the model output and r is the fraction of negatives kept (e.g. r = 0.1).
- **When it does not:** pure ranking by one score (NDCG only needs order).
- **Measure:** reliability diagram, expected calibration error, log loss, and calibration by slice (device, country, position, new vs old items). Global calibration can hide slice miscalibration.
- **Fix:** post-hoc Platt scaling (sigmoid) or isotonic regression on a held-out recent set; for neural nets, temperature scaling; ongoing monitoring (observed vs predicted CTR) because drift breaks it.
- Gradient boosting with log loss is roughly calibrated; deep nets and tree ensembles with heavy regularisation can be over/under-confident.

**Example:** Model A predicts mean pCTR 3.0%, actual 2.0% (overestimate). Ad revenue forecast is 50% too high. An isotonic map trained on the last week brings average prediction to about 2.0%.

**Follow-ups:**
- *Does isotonic hurt ranking?* It is monotone, so order is preserved except for ties in flat regions.
- *Calibrate per position?* Yes if training data are position-biased; correct for position first.

**Common mistakes:** Calibrating on the training set; forgetting negative-downsampling correction; fixing global calibration while slices are off; treating AUC as proof of calibration.

### Q34 ⭐⭐ 🟡 How do you meet a latency budget (e.g. 100 ms) in a recsys: cascaded ranking, caching, precomputation, feature-freshness tiers? What do you inspect when latency spikes?
**Asked at:** MLE roles

**Say this first (1 line):** I cannot score a million items with a heavy model in 100 ms, so I use a funnel: cheap retrieval narrows to hundreds, a medium model to dozens, a heavy model re-ranks the top few, and I precompute and cache everything that does not need to be real-time.

**Then explain:**
- **Cascade (illustrative budget):** retrieval (ANN, ~10-20 ms, 10^3 candidates) -> light ranker (GBDT/small MLP, ~15 ms, 10^2) -> heavy ranker (deep model, ~30 ms, 10-50) -> re-rank/business rules (~5 ms). Leave slack for network and tail latency.
- **Precompute:** item embeddings, item features, popular/trending lists, user embeddings for stable users.
- **Cache:** per-user results for a short TTL, hot-item features, embedding lookups; accept slight staleness.
- **Feature-freshness tiers:** batch (daily), near-real-time (minutes, streaming), real-time (request context, last click). Only pay for real-time where lift justifies it.
- **Engineering levers:** batch candidates into one model call, quantisation/distillation, ONNX/TensorRT, async parallel feature fetches, timeouts with fallbacks (if the heavy ranker times out, return light-ranker results).
- **Latency spike checklist:** p99 not mean; which stage (traces per stage); feature store or DB slow/hot key; cache hit-rate drop after deploy; larger candidate set or payload; cold-start of new pods; GC pauses; noisy neighbour; a downstream dependency.

**Example:** Home-feed p99 jumps from 90 to 250 ms after a release. Stage traces show feature fetch doubled: a new feature uses an uncached call. Fix: move it to the batch tier and add a timeout default.

**Follow-ups:**
- *Why p99?* Users and upstream timeouts feel tails; a mean of 60 ms can hide a 400 ms tail.
- *Trade-off of caching?* Staleness vs cost; for fast-moving inventory use short TTL or invalidate on stock change.

**Common mistakes:** Quoting average latency; adding model complexity with no stage budget; no fallback path; real-time features everywhere; testing latency with warm caches only.

### Q35 ⭐⭐ 🟡 Implement item-based collaborative filtering (cosine similarity on a sparse user-item matrix) with NumPy/pandas and produce top-N recommendations.
**Asked at:** Live-coding at product cos / GCCs

**Say this first (1 line):** Build a sparse user x item matrix, L2-normalise the item columns so that a matrix product gives cosine similarity between items, then score unseen items by summing their similarity to items the user has already interacted with.

**Then explain:**
- Cosine between items i and j = (r_i . r_j) / (|r_i| |r_j|) over the users who interacted with them. After normalising columns, S = R_n^T R_n.
- Zero out the diagonal (an item should not recommend itself), exclude already-seen items.
- Keep only the top-k neighbours per item: less noise, less memory (a dense item-item matrix does not fit at catalogue scale; at scale use ANN or sparse top-k).
- Cost: R^T R is sparse-sparse multiplication; fine for toy and mid-size data, precompute offline.
- For ratings, mean-centre per user first (adjusted cosine) and use a weighted average of neighbour ratings.

**Example:** 5 users, 5 items (binary views).

**Code:** (executed)
```python
import numpy as np, pandas as pd
from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize
df = pd.DataFrame({"user":[0,0,0,1,1,2,2,2,3,3,3,4,4],
                   "item":[0,1,2,0,1,1,2,3,2,3,4,0,4]})
R = csr_matrix((np.ones(len(df)), (df.user, df.item)))
Rn = normalize(R, axis=0)                  # L2-normalise item columns
S = (Rn.T @ Rn).toarray()                  # item-item cosine
np.fill_diagonal(S, 0)
def recommend(u, n=2, k=3):
    seen = R[u].indices
    Sk = np.zeros_like(S)                  # keep top-k neighbours per item
    idx = np.argsort(-S, axis=1)[:, :k]
    np.put_along_axis(Sk, idx, np.take_along_axis(S, idx, 1), 1)
    scores = Sk[:, seen].sum(1)
    scores[seen] = -np.inf                 # drop already-seen
    top = np.argsort(-scores)[:n]
    return [(int(i), round(float(scores[i]), 3)) for i in top]
print(recommend(0)); print(recommend(4))
```
Output: user 0 gets `[(3, 1.225), (4, 0.816)]`; user 4 gets `[(1, 0.667), (3, 0.5)]`.

**Follow-ups:**
- *Item-based vs user-based?* Item-based is more stable (items change less than users), precomputable and explainable ("because you viewed X").
- *Popularity bias?* Popular items have high similarity with many items; use shrinkage or normalise (e.g. cosine with damping).

**Common mistakes:** Building a dense user-item matrix; forgetting to remove seen items and the diagonal; using raw dot product (favours popular items); no top-k pruning; evaluating with a random split instead of a temporal one.

### Q36 ⭐⭐ 🔴 Implement matrix factorization with SGD from scratch in NumPy (bias terms, L2, train/val RMSE). How would you adapt it to implicit feedback?
**Asked at:** Coding rounds, MLE; Microsoft IDC / Amazon-type

**Say this first (1 line):** Predict r_ui = mu + b_u + b_i + p_u . q_i, loop over observed ratings, and for each one take a gradient step on the squared error plus L2 penalty; for implicit feedback I would switch to a ranking or confidence-weighted loss with sampled negatives.

**Then explain:**
- **Update rule** with error e = r - r_hat, learning rate lr, L2 strength lam:
  b_u += lr(e - lam b_u); b_i += lr(e - lam b_i); p_u += lr(e q_i - lam p_u); q_i += lr(e p_u - lam q_i).
- Init factors small and random (0.1 std); shuffle each epoch; track **train and validation RMSE** every few epochs and stop when validation stops improving.
- Tune k, lr, lam on validation; use a temporal split if data are timestamped.
- **Implicit adaptation:** there are no negative ratings, only unobserved. Options: (1) ALS with confidence weights c = 1 + alpha x count (Hu, Koren, Volinsky); (2) BPR: sample (u, positive i, negative j) and maximise log sigmoid(x_ui - x_uj); (3) sampled softmax / two-tower. Evaluate with recall@k/NDCG on held-out interactions, not RMSE.

**Example:** Synthetic: 200 users, 100 items, 40% observed, true rank 5 plus noise 0.3.

**Code:** (executed, seed 0)
```python
import numpy as np
rng = np.random.default_rng(0)
nu, ni, k = 200, 100, 5
P0, Q0 = rng.normal(size=(nu, k)), rng.normal(size=(ni, k))
mask = rng.random((nu, ni)) < 0.4
u, i = np.where(mask)
r = 3 + (P0[u] * Q0[i]).sum(1) * 0.5 + rng.normal(0, .3, len(u))
perm = rng.permutation(len(u)); cut = int(.8 * len(u))
tr, va = perm[:cut], perm[cut:]
def fit(lam=0.1, lr=0.02, epochs=60, k=5):
    P = rng.normal(0, .1, (nu, k)); Q = rng.normal(0, .1, (ni, k))
    bu, bi = np.zeros(nu), np.zeros(ni); mu = r[tr].mean()
    rmse = lambda idx: np.sqrt(np.mean((r[idx] - (mu + bu[u[idx]] + bi[i[idx]]
                                       + (P[u[idx]] * Q[i[idx]]).sum(1)))**2))
    for ep in range(epochs):
        for t in rng.permutation(tr):
            a, b = u[t], i[t]
            e = r[t] - (mu + bu[a] + bi[b] + P[a] @ Q[b])
            bu[a] += lr * (e - lam * bu[a]); bi[b] += lr * (e - lam * bi[b])
            P[a], Q[b] = P[a] + lr * (e * Q[b] - lam * P[a]), Q[b] + lr * (e * P[a] - lam * Q[b])
        if ep % 20 == 19: print(ep + 1, round(rmse(tr), 3), round(rmse(va), 3))
fit()
```
Output (epoch, train RMSE, val RMSE): `20 0.385 0.509`, `40 0.345 0.442`, `60 0.344 0.44`. Note: on a sparser 15% mask the same model overfit (after 60 epochs val about 1.08 vs train 0.44), which shows why regularisation and enough data per user matter.

**Follow-ups:**
- *SGD vs ALS?* ALS parallelises and has closed-form solves; SGD is flexible and simple for biases/extra terms.
- *Why does val RMSE go up while train falls?* Overfitting; raise lam, lower k, early stop.

**Common mistakes:** Updating P[a] and Q[b] sequentially with stale values (use the old P[a] for the Q update, as above); regularising by the wrong amount; no bias terms; using RMSE for implicit data; random split when time matters.

### Q37 ⭐ 🟡 Bi-encoder vs cross-encoder: how do they differ for retrieval vs reranking, and why is a cross-encoder only used on a shortlist?
**Asked at:** Search/RAG-adjacent MLE roles

**Say this first (1 line):** A bi-encoder embeds query and document separately, so document vectors can be precomputed and searched fast; a cross-encoder reads query and document together through full attention, which is more accurate but needs one forward pass per pair, so it only runs on a shortlist.

**Then explain:**
| | Bi-encoder | Cross-encoder |
|---|---|---|
| Input | query and doc encoded separately | [query; doc] concatenated |
| Score | dot/cosine of two vectors | classifier/regression head on joint representation |
| Precompute docs | Yes (index with ANN) | No |
| Cost for N docs | 1 query encode + ANN search | N forward passes |
| Accuracy | good, loses token-level interaction | higher (token-to-token attention) |
| Use | first-stage retrieval | reranking top 20-200 |
- **Why shortlist only:** 1M docs x 20 ms = hours per query. At top-100, a distilled cross-encoder costs 100 x a few ms, batched on GPU.
- **Middle ground:** late interaction (ColBERT) keeps per-token vectors and scores with MaxSim, between the two in cost and quality.
- Train bi-encoder with contrastive loss and hard negatives; train cross-encoder with pairwise/listwise loss on labelled (query, doc) data.

**Example:** RAG: dense retrieval fetches 100 passages; cross-encoder rescores them; top 5 go into the LLM prompt. Recall@100 of stage one sets the ceiling for the whole pipeline.

**Follow-ups:**
- *Bottleneck?* First-stage recall: a reranker cannot recover what retrieval missed.
- *Reduce reranker cost?* Distil into a smaller model, truncate docs, cache, dynamic shortlist size.

**Common mistakes:** Proposing a cross-encoder for full-corpus retrieval; evaluating reranker without measuring stage-one recall; mismatched train/test shortlist distributions.

### Q38 ⭐ 🟡 How can LLMs or pretrained text/image embeddings help cold start and item representation? What is generative retrieval with semantic IDs?
**Asked at:** AI-era recsys/search roles

**Say this first (1 line):** Pretrained text/image models turn an item's content into a vector, so a brand-new item with zero interactions still gets a sensible representation; generative retrieval goes further and has a model generate the item's discrete "semantic ID" token by token instead of searching an index.

**Then explain:**
- **Cold-start with content embeddings:** encode title/description/image with a text or CLIP-style model, feed as item-tower features or initialise the ID embedding from content. New items are retrievable on day one; as interactions arrive, the behavioural embedding takes over (blend by interaction count).
- **LLM uses:** enrich/normalise messy catalogue text, generate attributes and queries, cold-start user profiles from a short description, synthetic training data, explanation text. Costly, so run offline in batch, not per request.
- **Semantic IDs (TIGER-style, Rajput et al., 2023, a research result; production use is still limited and reported gains are on public benchmarks):** quantise the content embedding (e.g. RQ-VAE, residual quantisation) into a short code like (12, 87, 3). Similar items share code prefixes. A seq2seq Transformer takes the user history of semantic IDs and generates the next item's code. Benefits: shared structure helps cold items, no giant ID embedding table. Risks: invalid IDs, collisions, retraining costs, and it is still being matured in production, so describe it as emerging.
- **Cautions:** content embeddings capture "looks similar", not "gets clicked"; popularity and behaviour signals must still dominate for warm items. LLM hallucinations in generated metadata need validation.

**Example:** A new phone case with no clicks: text+image embedding places it near other cases, so it is retrieved for case browsers; after 1,000 impressions its behavioural vector is blended in.

**Follow-ups:**
- *How do you evaluate cold start?* Slice offline metrics by item age/interaction count, and run an A/B on new-item exposure and downstream engagement.
- *Why not LLM-only recommendation?* Latency, cost, grounding in catalogue/inventory, and weaker collaborative signal.

**Common mistakes:** Replacing behavioural signals with content embeddings; calling LLM per request; not checking multilingual/low-quality text; presenting semantic IDs as standard practice.

### Q39 ⭐ 🟡 Can you use an LLM as a judge to label search/recommendation relevance? What biases and validation steps do you need?
**Asked at:** AI-era search/ranking roles

**Say this first (1 line):** Yes, LLM judges can label relevance at a fraction of human cost and are widely used for offline evaluation, but only after I validate them against human labels, control their known biases, and keep humans for calibration and hard cases.

**Then explain:**
- **How:** prompt with the query, item (title, description, key attributes), a graded rubric (0-3 with examples), ask for a label plus a short reason; temperature 0; structured output.
- **Biases to control:**
  - **Position/order bias** (pairwise or listwise prompts): randomise order, test both orders.
  - **Verbosity/length bias:** prefers longer descriptions.
  - **Self-preference:** favours text written in its own style (or by an LLM).
  - **Prompt sensitivity and drift** when the vendor model updates: pin version.
  - **Missing context:** judge cannot know user intent, locale, availability, price sensitivity, so labels reflect "topical relevance", not utility.
- **Validation:** collect a human-labelled gold set (a few hundred to a thousand, stratified by query type), measure agreement (Cohen's/weighted kappa, Spearman) between LLM and human, compare to human-human agreement; check the LLM ranks systems in the same order as humans do (what matters for model selection). Re-validate on each prompt/model change.
- **Use:** regression testing, cheap NDCG on tail queries, finding bad results; do not replace online A/B for ship decisions. Never train and evaluate with the same LLM judge (circularity).

**Example (illustrative numbers):** 500 queries x top-10 items judged by LLM at about 5k calls; kappa 0.62 vs human-human 0.68; LLM-vs-human system ranking agrees on 5 of 5 candidates. Accepted for offline screening only.

**Follow-ups:**
- *Pointwise vs pairwise judging?* Pairwise is more discriminating but order-sensitive; pointwise is cheaper and easier to aggregate.
- *Privacy?* Do not send user PII to external LLMs; use redacted queries or a self-hosted model.

**Common mistakes:** Trusting the LLM with no human check; ignoring prompt/model version drift; using the judge to both optimise and evaluate; judging relevance without the information shown to users.

### Q40 ⭐ 🟡 How do you measure and improve fairness and exposure for small creators or sellers? How do you stop sellers spamming metadata to game the ranker?
**Asked at:** Marketplaces, creator platforms

**Say this first (1 line):** I measure exposure share and outcomes per creator group against what their quality would deserve, improve it with exploration and exposure constraints inside the ranker, and defend against gaming with quality-based features, anomaly detection and penalties, never with raw seller-provided text alone.

**Then explain:**
- **Measure:** exposure (impressions, rank-weighted, e.g. 1/log2(1+rank)) by seller/creator segment (new, small, large); Gini or share of top-1% sellers; exposure-to-relevance ratio ("amortised fairness": exposure proportional to merit); time for new creators to reach a first sale.
- **Improve:**
  - Explore: boost for new items for a bounded number of impressions (Q21).
  - Re-rank with exposure targets or minimum-exposure constraints (Lagrangian/greedy re-ranker).
  - Use per-item rather than per-seller normalisation so big sellers do not dominate through volume.
  - Sustained effect: check supply (do small creators stay?).
- **Trade-off:** short-term relevance or revenue dips; measure long-term supply health and buyer satisfaction.
- **Anti-gaming:** metadata stuffing (keywords, fake categories, copied titles) is a classic adversarial problem.
  - Weight behavioural signals (clicks, conversions, returns, reviews) over self-declared text.
  - Detect: duplicate/near-duplicate listings, keyword-stuffing scores, abnormal CTR/ratings, bursts of new accounts.
  - Penalise or demote, human review, clear policy, and expect an arms race (rotate features, do not publish exact formulas).
  - Keep features that sellers can edit cheaply away from the ranker's most heavily weighted inputs.

**Example (illustrative numbers):** Handmade marketplace: top 1% sellers get 70% of impressions. Reserving 10% of slots for exploration of new listings plus a quality floor lifts new-seller first-sale rate with a 0.3% drop in conversion; sustained seller retention improves after 8 weeks.

**Follow-ups:**
- *Fairness legal/ethical risk?* Define groups relevant to policy (small vs large seller); for protected attributes involve legal/ethics review.
- *Can fairness constraints hurt users?* Yes, if exposure is forced on low-quality items; tie it to a quality threshold.

**Common mistakes:** Equal exposure regardless of quality; measuring only seller outcomes; publishing ranking rules that invite spam; only one-time fix without monitoring.

### Q41 ⭐ 🟡 A recommendation reveals a sensitive inference about a user. What privacy, explainability and guardrail changes would you make?
**Asked at:** Senior roles; fintech/health/EU-regulated cos

**Say this first (1 line):** I would stop and fix it at three levels: remove or restrict the sensitive inference (data/feature level), give users control and an explanation (product level), and add a guardrail and audit layer (system level), involving privacy/legal early.

**Then explain:**
- **Immediately:** suppress the category (health, pregnancy, sexuality, religion, finances in distress) in recommendations and ads, review the incident, check what data fed it.
- **Data/feature level:** do not use sensitive attributes directly; also check **proxies** (items bought, search terms, location) that let the model infer them. Data minimisation, purpose limitation, retention limits; honour consent and opt-outs (GDPR: special-category data needs explicit consent or another legal basis).
- **Model/system guardrails:** a sensitive-topic classifier on candidates and a block-list/category filter at re-rank; no sensitive segments in targeting; audit by running probes ("does the model infer pregnancy from these purchases?"). Consider differential privacy or federated/on-device approaches for high-risk domains.
- **Explainability and control:** "Why am I seeing this?" (e.g. "because you viewed X"), ability to remove an item from history, reset or turn off personalisation; avoid explanations that reveal the inference itself ("because you may be pregnant").
- **Governance:** privacy impact assessment (DPIA), logging, regular audits, human escalation path, documentation (model cards).
- **Trade-off:** personalisation quality vs privacy; show it with an A/B that the filtered system loses little.

**Example:** Retail: baby products shown to a user before they told family. Fix: remove pregnancy-related inference from shared surfaces (emails, homepage banners), keep it only in-session with opt-in, add a "hide this category" control.

**Follow-ups:**
- *Is removing the attribute enough?* No; proxies leak it, so test for inference with probe models.
- *Unlearning on request?* Delete user data and retrain on schedule; design pipelines for deletion.

**Common mistakes:** Only dropping the sensitive column; no user control; explanations that expose the sensitive inference; skipping legal review.

### Q42 ⭐ 🟡 How do you measure the causal impact of recommendations on engagement (not just correlation)? Discuss holdouts, uplift and incrementality.
**Asked at:** Senior DS; marketplaces, Booking-type

**Say this first (1 line):** Engagement with recommendations is confounded, because people click what they would have found anyway, so I measure impact with randomised holdouts: some users (or slots) get no recommendations or a baseline, and incrementality is the difference in outcomes versus that control.

**Then explain:**
- **Correlation trap:** users who click recommendations are already heavy, motivated users. Comparing clickers vs non-clickers overstates impact.
- **Global holdout:** 1-5% of users see the non-personalised (popular/chronological) experience for weeks; compare engagement, retention, revenue. Gives true lift of the whole recsys.
- **Slot/item-level randomisation:** randomly remove or swap a module or a share of recommended items (ghost ads/intent-to-treat); estimate how many purchases are truly caused versus cannibalised from organic.
- **Incrementality = lift over control**, not conversion rate on recommendations. Report incremental conversions per 1000 impressions, plus cannibalisation of other channels.
- **Uplift modelling:** estimate per-user treatment effect (T/X-learners, causal forests) to target recommendations or promotions at users who change behaviour (persuadables), not sure-things.
- **Observational fallback** when randomisation is impossible: diff-in-diff, instrumental variables from natural randomness (rollout timing, exploration traffic), inverse propensity; weaker and assumption-heavy.
- **Beware:** interference/network effects (marketplaces: shifting demand between sellers), novelty effects, long-term effects needing long holdouts.

**Example:** (illustrative) Holdout of 2% of users: treated group makes 3.10 orders/month versus 2.95 in holdout, so incremental +0.15 orders, though 40% of orders came "from recommendations" by attribution. True lift is the 0.15, not the 40%.

**Follow-ups:**
- *Cost of a holdout?* Lost revenue on holdout users; keep small and time-bounded, or use ghost slots.
- *Why attribute poorly?* Last-click attribution credits the recommendation for purchases that would happen anyway.

**Common mistakes:** Reporting "revenue from recommendations"; clicker vs non-clicker comparison; ignoring cannibalisation; holdouts too short for retention effects; user-level interference.

### Q43 ⭐ 🔴 Design LLM-based reranking for top-k candidates: pointwise vs listwise prompting, cost and latency, distillation into a small ranker, and failure modes (position bias, reward hacking by preserving order).
**Asked at:** AI-era senior MLE/DS

**Say this first (1 line):** I would use an LLM only as a second-stage reranker on the top 20-50 candidates, pointwise or listwise, with a strict cost/latency budget, then distil its judgements into a small, fast ranker for the bulk of traffic, and guard against position bias and order-copying.

**Then explain:**
- **Requirements:** which gain justifies it (long-tail, ambiguous queries, text-rich items)? Latency (e.g. under 300 ms added), cost per 1000 queries, fallbacks.
- **Pointwise:** score each (query, doc) independently (yes/no logit or 0-3 grade). Parallel, cacheable, easy to calibrate, but scores are not comparable across docs without care; k LLM calls.
- **Listwise:** put all k docs in one prompt and ask for a ranking. Captures comparisons and costs one call, but long context, order sensitivity, and output-format errors; sliding windows for longer lists. Pairwise sits in between (O(k log k) with sorting).
- **Cost/latency:** tokens = k x doc length. Truncate docs, use a small/fine-tuned model, cache by (query, doc), batch, run only for queries where the first-stage ranker is uncertain, async fallbacks.
- **Distillation:** log LLM scores on a large query sample, train a cross-encoder or GBDT/LTR on them (plus click labels), serve the student; LLM stays for evaluation and hard queries. Check student vs LLM agreement and online metrics.
- **Failure modes:**
  - **Position bias:** the LLM favours items early in the prompt; shuffle and average across permutations.
  - **Reward hacking by preserving order:** if you train or evaluate with feedback that rewards agreement with the input order, the model learns to copy the input ranking (high NDCG, no value). Evaluate against a "keep first-stage order" baseline and against labels the first stage did not produce.
  - Hallucinated or dropped IDs in listwise output (validate, fall back), prompt injection from document text, unstable outputs, business-rule violations (out-of-stock, policy) so apply filters after.
- **Eval:** offline NDCG vs human labels, interleaving, then A/B with latency and cost guardrails.

**Example:** Top-30 for "gift for a 5 year old who likes dinosaurs": first stage returns generic toys; LLM pointwise judging promotes dinosaur kits; distilled student recovers about 80% of the gain at 1/50th of the cost (illustrative target, to be measured).

**Follow-ups:**
- *Pointwise or listwise first?* Pointwise to start: simpler, parallel, debuggable; listwise if comparisons matter and budget allows.
- *When not worth it?* Head queries with strong behavioural signals; tight latency.

**Common mistakes:** Applying the LLM to the full candidate set; no order-shuffle test; trusting output IDs unchecked; no distillation plan so costs scale linearly with traffic.

### Q44 ⭐ 🔴 Unbiased learning-to-rank from click logs: how do you estimate position propensities, and how does Unbiased LambdaMART use them?
**Asked at:** Search/ads ranking specialists

**Say this first (1 line):** Clicks are biased because users look at top positions more, so I estimate the probability that a position is examined (the propensity), for example from a small randomisation experiment or an EM click model, and then weight each click by 1/propensity so that learning-to-rank sees unbiased relevance; Unbiased LambdaMART does this inside the lambda gradients.

**Then explain:**
- **Model:** position-based model: P(click) = P(examined at position k) x P(relevant). We want relevance, but we only see clicks.
- **Estimating propensities p_k:**
  - **Randomisation:** swap items at positions (e.g. positions 1 and 2) for a small share of traffic; ratio of CTRs estimates relative examination. Costs some quality.
  - **Intervention harvesting:** use natural variation of the same item at different positions across logs.
  - **EM / regression-EM:** jointly fit examination and relevance from logs without swaps; needs enough overlap and assumes the model is right.
- **IPS-weighted loss:** weight each clicked document by 1/p_k, so clicks at low positions (rarely examined) count more. Clip weights for variance (Q32).
- **Unbiased LambdaMART (Hu et al. 2019):** keeps LambdaMART's pairwise lambdas but builds pairs from clicked vs unclicked documents and reweights each pair with two learned position-bias terms (one for clicked, one for unclicked documents). The ranker and the propensity terms are updated alternately until they stabilise. Open-source LTR toolkits (e.g. ULTRA) implement it.
- **Limitations:** needs correct propensities and overlap; trust bias (users click top items even if worse) requires extra terms; the propensity can depend on query and presentation.

**Example:** (illustrative) If position 1 is examined 90% of the time and position 5 only 30%, a click at position 5 gets weight 3.3, one at position 1 gets 1.1. A relevant item hidden at rank 5 is thereby up-weighted.

**Follow-ups:**
- *Why not just add position as a feature?* Then at serving you must set position to a constant; works as a baseline, but gives no guarantee and can confound.
- *Alternative?* Dual-learning algorithm: ranker and propensity model trained against each other.

**Common mistakes:** Treating CTR as relevance; no clipping; assuming propensity is only position when presentation (images, snippets) also matters; evaluating on biased clicks.

### Q45 ⭐ 🔴 Contextual bandits for recommendation (LinUCB, Thompson sampling) and off-policy evaluation. When would you use a bandit instead of a supervised ranker?
**Asked at:** Senior DS/MLE; media, ads

**Say this first (1 line):** A contextual bandit picks an item given user context, observes only the reward of the chosen item, and updates while balancing exploration and exploitation; I would use it when feedback is online and fast, there are few arms or a small slate, and exploration matters (new items, drift), and use a supervised ranker when I have a large logged dataset and a stable catalogue.

**Then explain:**
- **LinUCB:** assume reward ~ theta_a . x per arm; maintain A_a = I + sum x x^T and b_a; choose arm maximising x^T theta_a + alpha sqrt(x^T A_a^-1 x), where theta_a = A_a^-1 b_a. The second term is the uncertainty bonus.
- **Thompson sampling:** sample theta from the posterior, pick the best arm under the sample. Often performs as well or better and handles delayed feedback gracefully; simple with Beta-Bernoulli per arm or Bayesian linear regression.
- **Off-policy evaluation:** to test a new bandit policy from logs, use IPS/SNIPS/DR (Q32); requires logged propensities and overlap.
- **Bandit vs supervised ranker:**
  - Bandit: reward feedback only on shown items, catalogue or user behaviour changing quickly (news, promotions, notifications), cold start, few arms.
  - Supervised: massive stable logs, rich features, huge catalogue (use retrieval + ranking, with an exploration layer on top).
- Slate/combinatorial actions and big catalogues are hard for classic bandits; usually combine: ranker for candidates, bandit for a few exploratory slots.

**Example:** Homepage banner with 8 creatives and user context (device, segment): Thompson sampling shifts traffic to better creatives within hours; a supervised model would need labelled data from a prior uniform test.

**Follow-ups:**
- *Risk?* Early under-exploration, non-stationarity (use discounting), reward delay, debuggability.
- *Why log propensities?* Without them you cannot evaluate or retrain off-policy.

**Common mistakes:** Using bandits for huge catalogues without candidate generation; ignoring delayed rewards; no propensity logging; evaluating a bandit with a standard random split.

### Q46 ⭐ 🔴 Why is NDCG not directly optimisable by gradient descent, and how do lambda gradients get around that?
**Asked at:** Ranking specialists; research-leaning MLE

**Say this first (1 line):** NDCG depends on the sorted order of the scores, and sorting is piecewise constant: a small score change either changes nothing (gradient 0) or swaps two items (a jump), so there is no usable gradient; LambdaRank skips the loss and directly defines the gradient as a pairwise RankNet gradient scaled by how much NDCG would change.

**Then explain:**
- **Problem:** NDCG = DCG/IDCG with DCG = sum (2^rel - 1)/log2(rank+1). Rank is a step function of scores, so dNDCG/dscore is 0 almost everywhere and undefined at swaps.
- **RankNet:** smooth pairwise loss: P(i above j) = sigmoid(s_i - s_j), cross-entropy against the truth. Smooth, but treats all misordered pairs equally; a swap at ranks 99/100 matters as much as 1/2.
- **LambdaRank:** lambda_ij = RankNet gradient x |Delta NDCG_ij| (the NDCG change if i and j swapped). Each document's lambda = sum over its pairs. These "lambdas" act as gradients without any explicit loss function; LambdaMART fits trees to them (gradient boosting).
- **Effect:** errors near the top and between very different relevance grades are pushed harder.
- **Alternatives:** smooth surrogates (ApproxNDCG, softmax listwise losses, NeuralNDCG); LambdaLoss gives a theoretical bound view.

**Example:** (executed illustration) One query, relevance [3, 0, 2, 0, 1], scores [2.0, 1.5, 0.3, 0.2, -1.0]:
```python
import numpy as np
rel = np.array([3, 0, 2, 0, 1]); s = np.array([2.0, 1.5, 0.3, 0.2, -1.0]); n = len(rel)
order = np.argsort(-s); rank = np.empty(n, int); rank[order] = np.arange(n)   # 0-based rank
gain = 2.0**rel - 1; disc = 1 / np.log2(rank + 2)
idcg = (np.sort(gain)[::-1] / np.log2(np.arange(2, n + 2))).sum()
lam = np.zeros(n)
for i in range(n):
    for j in range(n):
        if rel[i] > rel[j]:                          # i should rank above j
            d = abs((gain[i] - gain[j]) * (disc[i] - disc[j])) / idcg   # |delta NDCG| if swapped
            rho = 1 / (1 + np.exp(s[i] - s[j]))      # RankNet pair gradient
            lam[i] += rho * d; lam[j] -= rho * d
print(np.round(lam, 3))   # [ 0.215 -0.16   0.015 -0.074  0.004]
```
Lambdas: `[0.215, -0.16, 0.015, -0.074, 0.004]`. The irrelevant item sitting at rank 2 (index 1) is pushed down hardest, the top relevant one is pushed up, and the tail items get tiny updates because swaps there barely move NDCG.

**Follow-ups:**
- *Is LambdaRank optimising NDCG exactly?* No; it is a heuristic that was later shown to optimise a bound/smoothed version of it, and empirically improves NDCG.
- *LightGBM objective?* `lambdarank` with `label_gain`, `lambdarank_truncation_level`, and the `eval_at` NDCG metrics.

**Common mistakes:** Saying NDCG is "non-convex" (the issue is non-differentiability); describing LambdaMART as "RankNet with trees" with no |Delta NDCG|; ignoring truncation at k.

### Q47 ⭐ 🔴 Graph-based recommenders: random walks, PinSage, LightGCN. When are they worth the complexity?
**Asked at:** Large-catalog platforms; senior

**Say this first (1 line):** Graph recommenders treat users and items as a bipartite graph and let signals travel along edges (random walks or graph neural networks); they are worth it when the graph structure carries information that plain embeddings miss, such as sparse users, multi-hop relations, or rich item content, and when you can afford the complexity.

**Then explain:**
- **Random walks (e.g. Pixie, Node2vec-style):** start at a user's items, walk item -> user -> item, count visits; fast, no training, real-time, great for related-pins style candidate generation. Counts popularity-biased; needs pruning/biased walks.
- **PinSage (Pinterest):** GraphSAGE-style convolution with random-walk-based neighbour sampling (importance pooling) on a graph of billions of nodes; item embeddings combine visual/text features with graph neighbourhood. Production scale via sampling, MapReduce inference.
- **LightGCN:** simplified GCN for collaborative filtering: drops feature transforms and nonlinearities, uses only linear neighbourhood aggregation of ID embeddings and averages layers; trained with BPR loss. A strong, cheap academic baseline.
- **Worth it when:** sparse interactions (neighbour smoothing helps), item-item relation graphs, cold start via features, need for multi-hop signals.
- **Often not worth it when:** a well-tuned two-tower, MF or sequence model reaches the same quality; the graph is mostly dense popularity; latency and engineering for sampling/serving and freshness are costly; GNN gains in papers shrink under fair baselines.
- **Practical rule:** build the strong simple baseline first; try graph features (e.g. neighbour aggregates, random-walk candidates) before full GNNs.

**Example:** Visual discovery app: new pin with image embedding but few engagements. PinSage-style aggregation of its board neighbours gives a useful embedding where an ID-based model has none.

**Follow-ups:**
- *Scaling GNNs?* Neighbour sampling, mini-batches, precomputed embeddings offline.
- *Staleness?* Graph changes constantly; inference is batch, with fresher signals added in ranking.

**Common mistakes:** Assuming GNNs always win; no strong baseline comparison; ignoring over-smoothing with deep stacks; forgetting the cost of keeping graph and embeddings fresh.

### Q48 ⭐ 🔴 Recommending in a two-sided marketplace (customer / restaurant / delivery partner, or job seeker / recruiter): how do you balance stakeholders and capacity constraints?
**Asked at:** Swiggy/Zomato/Uber/LinkedIn-type

**Say this first (1 line):** A marketplace ranker should maximise a combined marketplace value, not one side's clicks, so I predict each side's outcome (customer order probability, restaurant acceptance/prep capacity, delivery time and rider availability), combine them into a utility, and enforce capacity as hard constraints.

**Then explain:**
- **Requirements and metrics:** orders/GMV, customer satisfaction (delivery time, ratings), partner health (restaurant utilisation, rider earnings per hour), platform cost (subsidy, rider idle time). Guardrails per side.
- **Models:** pOrder(user, restaurant, context), predicted delivery time (ETA) and its uncertainty, cancellation/reject probability, restaurant load; for jobs: pApply, pRecruiterResponse, pHire.
- **Utility:** score = pOrder x (value) minus penalties for late delivery, restaurant overload, rider scarcity. Two-sided recommenders in jobs (reciprocal): score = pApply x pRecruiterResponds (a candidate is not helped by apply-spam to unresponsive recruiters).
- **Capacity constraints:** dynamic: if a restaurant is overloaded or riders are scarce in a zone, demote or hide; limit recommendations per recruiter per day to avoid flooding (a load-aware re-rank with exposure caps, or a small assignment/LP formulation).
- **Fairness:** exposure for new or small supply (Q40); avoid winner-take-all.
- **Experimentation:** marketplace interference (a treated customer takes capacity from control), so use cluster/switchback tests (by city or time slot) rather than user-level A/B.
- **Serving:** real-time supply signals (kitchen load, rider count) as a fast feature tier.

**Example:** Peak dinner rush: a popular restaurant's kitchen has 25 pending orders. Ranking still scores it high on appeal, but the capacity penalty drops it and favours nearby restaurants with an ETA 12 minutes shorter; order conversion dips slightly, late deliveries and cancellations fall.

**Follow-ups:**
- *How do you set weights?* Business value mapping and online tuning on marketplace-level metrics; show the Pareto frontier.
- *Why switchback?* Because supply is shared, so user-level randomisation leaks across arms.

**Common mistakes:** Optimising customer CTR only; ignoring supply capacity; user-level A/B in a shared-capacity market; no reciprocal term in two-sided matching (jobs, dating).

### Q49 ⭐ 🔴 Embedding and index operations: how do you refresh embeddings, version two-tower models, avoid mismatches between towers and the ANN index, and roll back?
**Asked at:** Senior MLE

**Say this first (1 line):** The query tower, item tower and ANN index must come from the same model version because their vector spaces are only compatible together; so I version them as one bundle, rebuild the index whenever the item tower changes, release them atomically, and keep the previous bundle ready for instant rollback.

**Then explain:**
- **The mismatch risk:** each training run learns its own embedding space. Item vectors from model v7 searched with a v8 query vector give garbage with no error message, just a silent recall collapse.
- **Versioning:** one `model_version` ties together user/query tower weights, item tower weights, the item embeddings, the ANN index build, feature schema, and a manifest with training data window and offline metrics. Store embeddings with the version key.
- **Refresh:**
  - New or updated items: embed with the current item tower and insert (HNSW supports incremental adds; IVF-PQ may need periodic re-training of centroids; see Q20).
  - Full retrain: re-embed the whole catalogue in batch, build a **new index** next to the live one.
  - Between retrains, the item tower is frozen, so fresh items only need an embed call; user vectors are computed online by the current query tower.
- **Safe release:** build -> offline checks (recall of ANN vs brute-force top-k on a sample, embedding norm/dist sanity, metrics vs previous) -> shadow traffic -> canary (1-5%) -> full. Serve query tower and index version selected from the same config key, never separately.
- **Rollback:** keep the previous index and towers hot (or quickly loadable); roll back by flipping the version pointer. Keep rollback tested.
- **Monitoring:** ANN recall vs exact on a sampled set, embedding drift (norm, centroid), candidate-overlap with previous version, retrieval-hit rate, latency, online metrics, and an alert if query and index versions differ.
- **Alternative for freshness:** compatible-embedding training (backward-compatible training) so a new model's embeddings still work with old index during migration, at the cost of complexity.

**Example (illustrative numbers):** New two-tower v8 is trained. Pipeline re-embeds 20M items (3 hours), builds the index, runs shadow for a day, switches 5% then 100% by changing `serving_version: v8`. A sharp drop in hit-rate triggers pointing back to v7 within minutes.

**Follow-ups:**
- *Query tower deployed alone?* Never for a new training run; for tiny feature fixes only if it provably leaves item space unchanged.
- *Cost of full re-embedding?* Schedule it, use incremental updates between releases.

**Common mistakes:** Deploying towers independently; replacing the model without rebuilding the index; deleting the old index right away; no ANN-vs-exact recall check; ignoring schema/feature version mismatches.
