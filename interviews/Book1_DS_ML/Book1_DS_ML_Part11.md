# Book 1 — Part 11: ML System Design (Question List)

**Topic:** ML system design (framework, fraud, feed, ETA, pricing, churn, recsys, search, CTR, credit, forecasting, notifications, trade-offs)
**Target:** 40 questions  |  **Actual:** 52  |  **Date:** 2026-10-20

_Cross-references: MLOps tooling depth -> Book 4; GenAI system design -> Book 2; recsys/ranking algorithms -> Part 7._

> Dedupe pass: removed 1 cross-part duplicate(s); renumbered Q1–Q52.

---

### Q1 ⭐⭐⭐ 🟢 Walk me through your end-to-end framework for any ML system design question (requirements to monitoring).
**Asked at:** All companies; product, fintech, GCC, Europe
**Say this first (1 line):** I clarify the business goal, then walk a fixed ladder: requirements, data, features, model, evaluation, serving, monitoring, trade-offs, and I start with a simple baseline.

**Then explain:**
1. **Requirements:** goal, users, success metric, constraints (latency, cost, scale, compliance). Ask what a wrong prediction costs.
2. **Data and labels:** what logs exist, how labels arrive (and how late), label noise, bias in who gets labelled.
3. **Features:** user, item, context, real-time aggregates; plan point-in-time correctness so there is no leakage.
4. **Model:** baseline first (rules or logistic regression), then GBDT or deep model only if it earns its complexity.
5. **Evaluation:** offline metric tied to the business metric, time-based split, then online A/B with guardrails.
6. **Serving:** batch vs real-time, latency budget, feature store, fallbacks.
7. **Monitoring:** data drift, prediction drift, delayed-label performance, retraining trigger.
8. **Trade-offs:** accuracy vs latency vs cost vs explainability; say what I would build in v1 vs v2.

**Example:** "Design fraud detection": goal is to cut fraud loss without blocking good users. Labels are chargebacks that arrive 30-60 days late. Features are velocity counts. Model is GBDT. Metric is recall at a fixed false-positive rate. Serving is under 100 ms. Monitor drift because fraudsters adapt.

**Follow-ups:**
- *What if you only have 5 minutes?* Requirements, metric, baseline, and one serving or monitoring risk.
- *Where do most systems fail?* Labels and data, not the model.

**Common mistakes:** jumping to "use a transformer", never asking about the metric, skipping label delay, forgetting monitoring, giving a monologue instead of checking in with the interviewer.

### Q2 ⭐⭐⭐ 🟢 A product manager says 'reduce fraud' (or 'reduce churn'). How do you turn that vague ask into a well-defined ML problem with a success metric?
**Asked at:** Product cos, fintech, consulting-style DS rounds
**Say this first (1 line):** I turn the vague ask into a prediction target, a decision it drives, an action with a cost, and a metric measured against a baseline.

**Then explain:**
- **Define the decision first.** "Reduce churn" means: whom do we contact, with what offer, when? ML only predicts; the action creates the value.
- **Define the label precisely.** Churn = no purchase in the 60 days after being active. Fraud = confirmed chargeback or analyst-confirmed. Choose a prediction horizon and a label window.
- **Pick metrics at three levels:** business (fraud loss in rupees, retained revenue), model (PR-AUC, recall at fixed precision), guardrail (false-decline rate, complaint rate).
- **Check feasibility:** is there data, is the signal actionable, is the volume enough, is a rule simpler?
- **Define a baseline:** current rules or "do nothing", and the lift needed to justify the project.

**Example:** "Reduce churn": label = no order in the next 30 days among users active in the last 90. Action = coupon for the top 10% risk. Metric = incremental retained users versus a holdout, not "AUC 0.85". A coupon costs Rs 50 and margin per saved user is Rs 400, so we need to save more than 12.5% of treated users to break even (50/400).

**Follow-ups:**
- *Why not just predict churn probability?* Risk is not persuadability; uplift modelling targets users the offer actually changes.
- *Who do you talk to?* PM, ops, risk and finance, to confirm costs and constraints.

**Common mistakes:** optimising AUC with no action attached, ignoring the cost of intervention, defining the label after the fact (leakage), no baseline.

### Q3 ⭐⭐⭐ 🟢 Batch vs real-time (online) inference: how do you decide for a given use case?
**Asked at:** Product cos, Amazon, Flipkart, GCCs
**Say this first (1 line):** I choose by how fresh the prediction must be: batch if inputs change slowly and the entities are known in advance, online if the decision depends on the current request.

**Then explain:**

| | Batch | Online (real-time) |
|---|---|---|
| Trigger | Schedule (nightly) | Per request |
| Latency | Minutes to hours is fine | Tens of ms |
| Cost | Cheap, but may score users who never show up | Always-on infra, pay per request |
| Freshness | Stale | Fresh features and context |
| Examples | Churn scores, LTV, email recs | Fraud at payment, search ranking, ETA |

- **Decide on:** does the prediction depend on request-time context; how fast do features go stale; what does a stale prediction cost; what fraction of batch predictions are ever used.
- **Hybrid is common:** precompute candidates or embeddings in batch, re-rank online with fresh context. Cache results for hot keys.
- Online adds complexity: feature store, training-serving skew, autoscaling, fallbacks.

**Example:** Home-page recs for 50M users where 5M log in daily: compute top-200 candidates nightly, then a light online re-ranker uses session clicks. Pure online would waste compute; pure batch would miss current intent.

**Follow-ups:**
- *Streaming vs online?* Streaming (Flink/Spark) computes features continuously; online inference is a model call per request that reads those features.
- *How to cut online latency?* Smaller model, caching, cascade.

**Common mistakes:** defaulting to real-time because it sounds modern; ignoring that most batch predictions go unused; no fallback when the online service is down.

### Q4 ⭐⭐⭐ 🟡 Design a fraud detection system for UPI / card payments.
**Asked at:** PhonePe, Paytm, Amazon Pay, JPMC/GCCs, Klarna, DoorDash-type marketplaces
**Say this first (1 line):** A two-layer system: fast rules plus a real-time GBDT score within about 100 ms, a manual-review queue, and a feedback loop, because fraud labels are rare, delayed and adversarial.

**Then explain (framework):**
- **Requirements:** block fraud without declining good users; latency under 100 ms on the payment path; thousands of TPS at peak. A missed fraud costs the amount; a false decline costs revenue and trust.
- **Data and labels:** transactions, device, IP, merchant, user history. Labels: chargebacks and customer complaints (30-60 days late) plus analyst decisions. Fraud is about 0.1% or less, so it is highly imbalanced.
- **Features:** velocity (count and amount per user, device, merchant over 1 min / 1 h / 24 h), new-device flag, geo distance and impossible travel, payee age, graph features (shared devices, mule accounts), deviation from the user's own baseline.
- **Model:** hard rules for known patterns; GBDT (XGBoost/LightGBM) for the score; optional graph or sequence model for rings. Score maps to actions: allow, step-up auth (OTP), block, review.
- **Evaluation:** time-based split, PR-AUC, recall at a fixed review rate, rupee-weighted loss, cost-based threshold. Not accuracy.
- **Serving:** online feature store (Redis plus streaming aggregates), model service, rules fallback on timeout, log every decision with its features for replay.
- **Monitoring:** drift, alert rate, approval rate, delayed-label recall, champion/challenger.
- **Trade-offs:** recall vs friction; explainability for disputes (reason codes); frequent retraining since fraudsters adapt.

**Example (illustrative numbers):** Threshold set so 0.5% of transactions get step-up and it catches 70% of fraud rupees. Moving to 1% catches 78% but adds friction to twice as many good users, so the business picks a point from the cost curve.

**Follow-ups:**
- *Label delay?* Use fast proxies, train on matured cohorts, keep a labelled random holdout.
- *Selection bias?* Blocked transactions never reveal their label; keep a small random-allow sample.

**Common mistakes:** accuracy as the metric, random split instead of time split, no latency budget, ignoring feedback bias and adversaries.

### Q5 ⭐⭐⭐ 🟡 Design a news-feed / social-media feed ranking system.
**Asked at:** Meta-type, ShareChat, Instagram, product cos
**Say this first (1 line):** Candidate generation fetches thousands of posts, a ranker predicts engagement, and a re-ranker handles diversity, integrity and freshness; the objective is long-term value, not just clicks.

**Then explain (framework):**
- **Requirements:** feed served in under 200 ms; hundreds of millions of users; goal is meaningful engagement and retention, with guardrails (misinformation, creator fairness, complaints).
- **Data and labels:** impressions with positions, clicks, dwell time, likes, shares, hides, reports. Log what was shown so position bias can be corrected.
- **Candidates:** recent posts from follows, trending, interest-based via embeddings (about 1,000-5,000).
- **Features:** user history, author affinity, post content embedding, age (freshness), social signals, context (time, device).
- **Ranker:** multi-task model predicting P(click), P(like), P(share), P(hide); combine as score = sum of w_i x p_i with weights tuned by product and A/B tests.
- **Re-rank:** diversity (not five posts from one author), integrity filters, ad insertion, creator exposure.
- **Evaluation:** offline AUC/NDCG per task, then A/B on session time, retention and guardrails; keep long-term holdouts because clickbait lifts short-term clicks and hurts retention.
- **Serving:** precomputed embeddings plus ANN retrieval, feature store, batched ranker inference, caching.
- **Monitoring:** CTR drift, content mix, feedback loops.

**Example:** A clickbait post has high P(click) but high P(hide), so the weighted score ranks it below a friend's photo with moderate click probability and high share probability.

**Follow-ups:**
- *New posts?* Freshness boost plus exploration slots.
- *Feedback loop?* Popular posts get more impressions; use position-bias correction and exploration.

**Common mistakes:** a single click objective, ignoring position bias, no long-term metric, no integrity layer.

### Q6 ⭐⭐⭐ 🟡 Design a recommendation system for an e-commerce home page at scale.
**Asked at:** Flipkart, Amazon, Zalando, Spotify, Walmart
**Say this first (1 line):** A retrieval-then-ranking funnel: several retrievers produce a few hundred candidates, a ranker scores them for purchase or click, and business rules tidy the final slate.

**Then explain (framework):**
- **Requirements:** personalised home page, under 150 ms, millions of items; metrics: CTR, add-to-cart, conversion, revenue per session, plus diversity and catalogue coverage.
- **Data:** impressions, clicks, carts, purchases, item metadata, images, text. Labels are implicit and biased by what was shown.
- **Retrieval (recall):** two-tower embeddings with ANN search, co-purchase and recently viewed, popular in category, new items.
- **Ranking (precision):** GBDT or deep model with user, item, context and cross features; target purchase or a weighted mix of click, cart, buy.
- **Re-ranking:** diversity, stock availability, margin, de-duplication, seen-items filter.
- **Evaluation:** offline Recall@K and NDCG with a time split; A/B on conversion and revenue; check segments (new vs returning users).
- **Serving:** user embeddings precomputed daily; ANN index (FAISS/ScaNN); online ranker uses fresh session features; fallback to popular items.
- **Cold start:** content-based and popularity, exploration slots.
- **Monitoring:** CTR per slot, embedding freshness, feedback loop.

**Example:** 10M-item catalogue, 3 retrievers at 200 each gives about 600 candidates; the ranker scores them in about 20 ms; the final slate is 40 items after filters.

**Follow-ups:**
- *Why two stages?* A heavy model over 10M items is too slow; retrieval is cheap and high-recall, ranking is expensive and precise.
- *Clicks or revenue?* Blend purchase probability with margin, and watch returns.

**Common mistakes:** one heavy model over the whole catalogue, random-split evaluation, ignoring cold start and inventory.

### Q7 ⭐⭐⭐ 🟡 Design an ETA prediction system for food or grocery delivery.
**Asked at:** Swiggy, Zomato, Uber, DoorDash
**Say this first (1 line):** Predict delivery time as prep time plus rider assignment plus travel plus handover, output quantiles so we can show a safe promise, and retrain often because traffic and kitchens change.

**Then explain (framework):**
- **Requirements:** accurate ETA at checkout and updated in-app; latency under 100 ms; business metrics: on-time rate, trust, conversion (a long ETA loses orders, a short one causes cancellations).
- **Data and labels:** historical orders with timestamps for placed, accepted, ready, picked up, delivered; target = delivered minus placed. Handle cancelled orders (censoring).
- **Features:** restaurant prep-time history (by hour and order size), item count, kitchen load (open orders), route distance and travel time, rider availability nearby, weather, traffic, day/hour, festivals.
- **Model:** GBDT regression on components or end to end; quantile loss (P50 for display, P80-P90 for the promise); a sequence model for dynamic updates is optional.
- **Evaluation:** MAE, P90 error, quantile coverage, on-time rate; time-based split; slice by city, restaurant type, rain.
- **Serving:** online; features from a feature store plus real-time kitchen load; recompute as order status changes.
- **Monitoring:** error by city, prep-time drift, systematic bias.
- **Trade-offs:** asymmetric cost, so under-promise slightly; too much padding hurts conversion.

**Example:** Predicted P50 = 28 min and P90 = 38 min; show "30-40 min" so about 90% of orders arrive inside the window.

**Follow-ups:**
- *Why not MAE only?* Late is worse than early; use quantile loss and on-time rate.
- *New restaurant?* Fall back to cuisine/area averages.

**Common mistakes:** a single point estimate, ignoring kitchen prep (the biggest variance), random split, no per-city monitoring.

### Q8 ⭐⭐⭐ 🟡 Design a customer churn prediction and retention system.
**Asked at:** Telecom, SaaS, fintech, Booking, Spotify, GCCs
**Say this first (1 line):** Define churn carefully, predict risk with a time-safe model, then target users where an intervention changes behaviour, and measure success with a holdout, not AUC.

**Then explain (framework):**
- **Requirements:** who owns retention, what actions exist (offers, nudges, support), and the cost per action.
- **Label:** pick a snapshot time T; features come from before T; churned = no activity in the next N days (N fits the usage cycle).
- **Features:** recency, frequency, monetary value, trend (falling orders), support tickets, delivery delays, app version, tenure, price sensitivity.
- **Model:** logistic regression or GBDT baseline; survival model for time-to-churn; uplift model for who responds.
- **Evaluation:** PR-AUC, top-decile lift, calibration, time-based split. Online: randomised holdout measuring incremental retention and ROI.
- **Serving:** batch scoring daily or weekly, scores pushed to the CRM, an action engine with contact caps.
- **Monitoring:** score drift, label rate, campaign ROI, treated vs control retention.
- **Trade-offs:** risk vs persuadability; discounts can train users to wait for coupons.

**Example (illustrative numbers):** 1M users, 10% churn; the top decile churns at 35% (3.5x lift). A Rs 50 coupon to 100k users costs Rs 50 lakh. If it saves 5% of them at Rs 600 margin each, that is Rs 30 lakh, so blanket targeting loses money; uplift targeting of "persuadables" is needed.

**Follow-ups:**
- *Churn probability vs uplift?* Sure-things and lost-causes waste the coupon; uplift picks users the offer changes.
- *Class imbalance?* Class weights; do not resample the evaluation set.

**Common mistakes:** leakage (features computed after T), judging by AUC only, no control group, treating every high-risk user.

### Q9 ⭐⭐⭐ 🟡 Design a demand forecasting system for a retailer or quick-commerce platform.
**Asked at:** Walmart, Amazon, Zalando, Swiggy Instamart, Bain-type consulting DS
**Say this first (1 line):** Forecast demand per SKU-store-day as a distribution, at the grain that drives replenishment, and feed it to an inventory optimiser; the goal is fewer stock-outs and less wastage, not just low error.

**Then explain (framework):**
- **Requirements:** horizon (1-14 days for quick commerce), level (SKU x dark store x day), objective: minimise stock-outs and spoilage.
- **Data:** sales history, stock-out flags (sales are censored demand), prices, promos, calendar, festivals, weather, launches.
- **Features:** lags and rolling means, day of week, promo flags, price features, hierarchy (category, store).
- **Model:** one global GBDT or deep model across all series (scales better than per-series ARIMA); baseline = seasonal naive; Croston-style methods for intermittent slow movers. Output quantiles (P50, P90) for safety stock.
- **Evaluation:** rolling-origin backtests; WAPE or MASE (MAPE breaks on zeros), bias, pinball loss for quantiles, service level.
- **Serving:** nightly batch; forecasts feed replenishment; planners can override for promos.
- **Monitoring:** bias by category, value added over baseline, stock-out rate.
- **Trade-offs:** over-stock vs lost sales; perishables favour lower quantiles.

**Example (illustrative numbers):** Milk at a dark store: P50 = 120 units, P90 = 150. With a short shelf life, order near P65; for non-perishables, order near P90.

**Follow-ups:**
- *New product?* Use similar products' attributes or launch-curve priors.
- *Stock-outs?* Zero sales is not zero demand; flag and impute it.

**Common mistakes:** random cross-validation, MAPE with zeros, ignoring censored demand, forecasting a point instead of a quantile.

### Q10 ⭐⭐⭐ 🟡 Design a credit risk / loan default scoring system.
**Asked at:** JPMC and bank GCCs, Klarna, Indian NBFCs/fintech
**Say this first (1 line):** A calibrated, explainable probability-of-default model on bureau and behavioural data, trained on matured cohorts, with reject inference, cut-offs set by expected loss, and governance for fairness and regulation.

**Then explain (framework):**
- **Requirements:** approve/decline and pricing; metric = default rate at a given approval rate, and profit; regulatory explainability; decision in seconds.
- **Data and labels:** application, bureau (e.g. CIBIL), bank statements, device, repayment history. Label = 90+ days past due within 12 months of disbursal, so you need a long maturation window.
- **Selection bias:** you only see outcomes for approved applicants. Use reject inference or small randomised approvals, and be honest about the limits.
- **Features:** income, debt-to-income, utilisation, delinquency history, enquiries, cash-flow stability; avoid proxies for protected attributes.
- **Model:** WoE logistic-regression scorecard as the interpretable baseline; GBDT with monotonic constraints and SHAP for lift; calibrate probabilities.
- **Evaluation:** AUC/KS/Gini, calibration, PSI for stability, out-of-time test; business: expected loss = PD x LGD x EAD; threshold from the profit curve.
- **Serving:** online decision engine with policy rules plus score; log reason codes.
- **Monitoring:** PSI, vintage curves, approval rate, early delinquency, champion/challenger.
- **Trade-offs:** predictive power vs explainability and fairness.

**Example:** At 40% approval a GBDT lowers defaults from 4.1% to 3.4% versus the scorecard (illustrative numbers); the lender still checks reason codes and that the gain holds out of time.

**Follow-ups:**
- *Explaining a decline?* Adverse-action reason codes from SHAP or scorecard points.
- *Thin-file users?* Alternate data, with fairness checks.

**Common mistakes:** random split, leakage from post-disbursal data, ignoring selection bias and calibration, threshold not tied to cost.

### Q11 ⭐⭐⭐ 🟡 Design an ad click-through rate (CTR) prediction system.
**Asked at:** Amazon Ads, Flipkart Ads, Meta, Google, Microsoft
**Say this first (1 line):** Predict P(click) (often also P(conversion)) per ad impression with a calibrated model in tens of milliseconds, because the auction multiplies the probability by the bid.

**Then explain (framework):**
- **Requirements:** about 10-30 ms per request over hundreds of ads; billions of impressions; metrics: log-loss, calibration, revenue (eCPM), advertiser ROI.
- **Data and labels:** impression logs with a click label (clicks are about 1-2%, so imbalanced); conversions arrive later (delayed feedback).
- **Features:** mostly sparse categoricals (user, ad, advertiser, placement, query/context) as embeddings or hashed features, crosses, smoothed historical CTR, position.
- **Model:** logistic regression with hashed crosses as baseline; GBDT; deep models (Wide and Deep, DeepFM, DCN) for interactions.
- **Evaluation:** offline AUC and log-loss, plus calibration (predicted vs actual CTR by bucket) since miscalibration mis-prices auctions; online A/B on revenue and guardrails.
- **Serving:** low-latency feature store, model on CPU/GPU, caching, incremental/online learning for freshness.
- **Monitoring:** CTR drift by segment, calibration, budget pacing.
- **Trade-offs:** model complexity vs latency; exploring new ads.

**Example:** An ad with bid Rs 10 and P(click) 2% has eCPM = 1000 x 0.02 x 10 = Rs 200, beating a Rs 20 bid at 0.5% (eCPM Rs 100). If predictions are 2x too high, advertisers overpay.

**Follow-ups:**
- *Position bias?* Include position as a training feature and fix it at serving, or use inverse propensity weights.
- *Negative downsampling?* Re-calibrate afterwards: p = q / (q + (1 - q)/w), where w is the fraction of negatives kept.

**Common mistakes:** AUC only with no calibration check, leakage through future-aggregated CTR, ignoring delayed conversions.

### Q12 ⭐⭐⭐ 🟡 Design a search ranking system for an e-commerce site.
**Asked at:** Flipkart, Amazon, Walmart, Booking, Zalando
**Say this first (1 line):** Query understanding, then retrieval (lexical plus semantic), then a learning-to-rank model trained on clicks and purchases, then business re-ranking, all inside about 200 ms.

**Then explain (framework):**
- **Requirements:** relevance plus conversion; metrics: NDCG@10, CTR, add-to-cart, null-result rate, revenue per search.
- **Query understanding:** spell correction, synonyms (including Hinglish), brand/category/attribute extraction, intent classification.
- **Retrieval:** inverted index (BM25) in Elasticsearch/Solr plus embedding-based ANN for semantic matches; merge to about 500-1,000 candidates.
- **Ranking:** LambdaMART (GBDT) or a neural ranker with text match, popularity, CTR/CVR, price, rating, stock, delivery speed, personalisation. Graded labels: purchase > cart > click > impression with no click.
- **Re-rank:** diversity, sponsored mix, availability, business rules.
- **Bias:** position bias in click data, so use inverse propensity weights or randomisation; keep a human-judged gold set.
- **Evaluation:** offline NDCG on judged labels with a time split; A/B online; split head vs tail queries.
- **Serving:** near-real-time index updates for price and stock; cache head queries.
- **Monitoring:** zero-results rate, latency, CTR by query type.

**Example:** Query "red nike shoes": brand = Nike, colour = red, category = shoes; BM25 returns 800 items; the ranker puts in-stock, well-rated, fast-delivery items first.

**Follow-ups:**
- *Tail queries with few clicks?* Semantic retrieval and LLM-generated relevance labels.
- *Why LambdaMART?* Its gradients are weighted by the change in NDCG, so it optimises a ranking metric rather than a pointwise loss.

**Common mistakes:** training on raw clicks without bias correction, only lexical retrieval, ignoring head vs tail, no judged set.

### Q13 ⭐⭐⭐ 🟡 How do you choose offline metrics and online metrics for an ML system, and what do you do when they disagree?
**Asked at:** Product cos, Amazon, Spotify, Booking
**Say this first (1 line):** Offline metrics are cheap proxies for picking candidates; the online metric tied to the business is the truth, and when they disagree I trust online and investigate why the proxy failed.

**Then explain:**
- **Offline:** AUC, PR-AUC, NDCG, RMSE, calibration, on time-split data. Fast and repeatable, but measured on logs produced by the old model.
- **Online:** A/B-tested primary metric (conversion, retention, fraud loss) plus guardrails (latency, complaints, revenue).
- **Why they disagree:** selection bias in logs, feedback loops, a proxy not aligned with the business goal, novelty effects, distribution shift, things offline cannot see (latency, UI, item interactions), or an underpowered or invalid A/B (check sample-ratio mismatch).
- **What I do:** validate the experiment, slice by segment, check calibration, inspect examples, then fix the offline metric (counterfactual evaluation, IPS, interleaving) and iterate. Never ship on offline alone.
- **Choose offline metrics** that have historically predicted online wins; track that correlation.

**Example:** A new recommender lifts offline NDCG by 3% but online revenue is flat. Slicing shows it recommends cheap popular items users would have bought anyway; offline NDCG rewarded predicting existing behaviour. Switch the label to purchase value or incremental effect.

**Follow-ups:**
- *Offline up, online down?* Check leakage in offline evaluation first, then bias in logs.
- *Faster online signal?* Interleaving for ranking, CUPED for variance reduction.

**Common mistakes:** shipping on AUC, an unvalidated proxy, ignoring guardrails, reading an underpowered A/B.

### Q14 ⭐⭐⭐ 🟡 How do you handle the cold-start problem (new users, new items) in a production system?
**Asked at:** Flipkart, Spotify, Zalando, Swiggy
**Say this first (1 line):** For new users and items I fall back on content, popularity and context, use exploration to collect data fast, and shift to the learned model as interactions accumulate.

**Then explain:**
- **New users:** onboarding questions, location/device/source, popular-in-region, context (time of day), session-based recs after a few clicks.
- **New items:** content embeddings from title/image/category/brand, priors from similar items, plus a capped exploration (bandit) so the item gets impressions.
- **Model design:** use side features and embeddings (two-tower with content towers), not only IDs; blend weights move toward collaborative signals as data arrives.
- **Exploration:** epsilon-greedy or Thompson sampling with a cap on exposure to protect user experience.
- **Evaluation:** report cold and warm cohorts separately; A/B on new-user conversion and retention.
- **Monitoring:** share of impressions going to new items, time to first interaction.

**Example:** A new seller lists a product with no clicks. Use its category and image embedding to borrow the CTR of similar items as a prior, guarantee 1,000 impressions across diverse users, then update with Bayesian smoothing.

**Follow-ups:**
- *Why not just boost new items?* Too much boost hurts the experience; cap it and measure.
- *Cold start in fraud?* Use device/network and population-level features with conservative limits.

**Common mistakes:** pure ID-based collaborative filtering, no exploration, evaluating only warm users, ignoring the loop that keeps new items invisible.

### Q15 ⭐⭐⭐ 🟡 What is training-serving skew and how do you prevent it?
**Asked at:** Amazon, Microsoft IDC, Flipkart, GCCs
**Say this first (1 line):** Training-serving skew means the features or data the model sees in production differ from what it saw in training; I prevent it by sharing feature code and training on logged serving features.

**Then explain:**
- **Common causes:** different code paths (SQL for training, Java for serving), different freshness, different null/default handling, time leakage in training, different library or preprocessing versions, schema or label changes.
- **Prevention:**
  - A feature store with one definition used offline and online.
  - Log the exact features at serving time and train on them.
  - Point-in-time joins for training data.
  - Version preprocessing and ship it with the model (e.g. an sklearn Pipeline).
  - Test: compare offline vs online feature values on a sample of live requests.
- **Detection:** compare online vs training feature distributions (PSI, KS), null rates, and prediction distributions.

**Example:** Training computed "orders in last 30 days" including today; serving read a table refreshed nightly, which excluded recent orders. Offline metrics looked fine; online performance degraded. Fix: compute from the same event stream with the same window.

**Code:**
```python
import pandas as pd
# one shared feature function used by BOTH training and serving
def txn_features(events: pd.DataFrame, now: pd.Timestamp) -> dict:
    w = events[(events.ts > now - pd.Timedelta("1h")) & (events.ts <= now)]
    return {"cnt_1h": len(w), "amt_1h": float(w.amount.sum())}
ev = pd.DataFrame({"ts": pd.to_datetime(["2026-01-01 10:00","2026-01-01 10:20","2026-01-01 10:50","2026-01-01 11:30"]),
                   "amount": [100, 250, 40, 900]})
now = pd.Timestamp("2026-01-01 11:00")
print(txn_features(ev, now))   # {'cnt_1h': 2, 'amt_1h': 290.0}; the 11:30 event is the future and is excluded
```

**Follow-ups:**
- *Skew vs drift?* Skew is a train/serve mismatch at one point in time; drift is the world changing over time.
- *Hard case?* Real-time aggregates; replay the event stream to build training data.

**Common mistakes:** reimplementing features twice, ignoring default/null handling, no online-vs-offline comparison.

### Q16 ⭐⭐⭐ 🟡 How would you monitor an ML model in production and decide when to retrain?
**Asked at:** Almost all MLE/DS loops (deep tooling in Book 4)
**Say this first (1 line):** I monitor four layers (system, data quality, drift, performance with delayed labels) and retrain on a schedule plus triggers when drift or performance crosses a threshold.

**Then explain:**

| Layer | What | How |
|---|---|---|
| System | latency, errors, throughput | standard APM alerts |
| Data | nulls, schema, ranges | validation checks |
| Drift | feature and prediction distributions | PSI, KS test vs training window |
| Performance | accuracy, calibration, business KPI | labels once they arrive; proxies before |

- **Retrain decision:** a regular schedule (weekly/monthly) as baseline, plus triggers: PSI above about 0.25 on important features, a performance drop past a threshold, or a known event (new product, policy change). Promote only if the new model beats the champion on a recent holdout.
- **Delayed labels:** monitor proxies (approval rate, score distribution) and a small labelled sample until labels mature.
- **Safe rollout:** shadow, canary, rollback plan.
- Drift is not always harmful, so tie alerts to feature importance and performance impact.

**Example:** PSI on a scorecard variable hits 0.3 after a policy change, but early-vintage default rates stay flat. Investigate first; retraining on unmatured labels could hurt.

**Code:**
```python
import numpy as np
def psi(a, b, bins=10):
    edges = np.quantile(a, np.linspace(0, 1, bins+1)); edges[0], edges[-1] = -np.inf, np.inf
    pa = np.histogram(a, edges)[0]/len(a); pb = np.histogram(b, edges)[0]/len(b)
    pa, pb = np.clip(pa,1e-6,None), np.clip(pb,1e-6,None)
    return float(np.sum((pb-pa)*np.log(pb/pa)))
rng = np.random.default_rng(0)
ref = rng.normal(0,1,50000)
print(round(psi(ref, rng.normal(0,1,50000)),4), round(psi(ref, rng.normal(0.5,1,50000)),3))  # 0.0004 0.235
```
Rule of thumb: below 0.1 stable, 0.1-0.25 moderate shift, above 0.25 major shift.

**Follow-ups:**
- *No labels for weeks?* Monitor input and output drift and use proxy labels.
- *Retrain on all history?* Use a window; old data may be stale.

**Common mistakes:** only monitoring uptime, alerting on every drift with no link to impact, auto-retraining without validation, ignoring label delay.

### Q17 ⭐⭐⭐ 🟡 What are feedback loops and selection bias in deployed ML systems, and how do you mitigate them?
**Asked at:** Product cos, Spotify, Meta-type, Flipkart
**Say this first (1 line):** A deployed model changes the data it later learns from: it only sees outcomes for what it chose to act on, so it can reinforce its own bias; I mitigate with exploration, logged propensities and unbiased holdouts.

**Then explain:**
- **Selection bias:** labels exist only for chosen cases. Loans never approved have no default label; blocked transactions have no fraud label.
- **Feedback loop:** a recommender shows popular items, they get more clicks, and the model learns they are even more popular. Predictive policing is the textbook example.
- **Position bias** is a close cousin: top slots get clicks regardless of quality.
- **Mitigation:**
  - Randomised exploration (epsilon or bandit) and a small random holdout.
  - Log the propensity (probability the item was shown) and use inverse propensity weighting.
  - Counterfactual evaluation, interleaving, position as a feature.
  - Reject inference for credit; a random allow sample for fraud.
  - Monitor diversity/coverage and long-term metrics.

**Example:** A fraud model blocks everything scoring above 0.8, so later training data has no fraud labels for that region; measured recall looks great but the model is blind. Letting 1% of high-score transactions through (within limits) gives unbiased labels at a known, small cost.

**Follow-ups:**
- *Cost of exploration?* Capped, and cheaper than a blind model.
- *Problem with IPS?* High variance for small propensities; clip the weights.

**Common mistakes:** training on logs as if they were random samples, no holdout, optimising short-term clicks only.

### Q18 ⭐⭐⭐ 🟡 Walk through how you would prevent data leakage when building training data for a time-dependent system.
**Asked at:** Fintech, GCCs, product cos
**Say this first (1 line):** Everything about a training row must be knowable at its prediction time: features computed as-of that time, labels from after it, and a time-based split with a gap.

**Then explain:**
- **Point-in-time features:** for each row use only data timestamped before the prediction time (as-of joins; never join the latest snapshot table).
- **Label window:** define prediction time T and label over T to T+N; no features from inside the label window.
- **Time-based split:** train on the past, validate on the future, with a gap at least as long as the label window; never random-split temporal data.
- **Group leakage:** the same user or order in both train and test; split by time or user.
- **Preprocessing leakage:** scaling, imputation and target encoding must be fit on the training fold only. Be suspicious of a very strong single feature; drop it and retrain to check.
- **Late-arriving data:** make sure the data was actually available at the time (not back-filled corrections).

**Example:** A churn model uses "support tickets in the last 30 days" from today's table. For a user who churned last month, it includes tickets raised after cancelling. AUC is, say, 0.95 offline and 0.7 online (illustrative).

**Code:**
```python
import numpy as np, pandas as pd
rng = np.random.default_rng(0)
n = 1000
df = pd.DataFrame({"user": rng.integers(0, 50, n),
                   "ts": pd.Timestamp("2026-01-01") + pd.to_timedelta(np.sort(rng.integers(0, 90*24*3600, n)), unit="s"),
                   "y": rng.integers(0, 2, n)})
df = df.sort_values("ts").reset_index(drop=True)
df["past_pos"] = df.groupby("user")["y"].cumsum() - df["y"]   # strictly before this row
cut = pd.Timestamp("2026-03-01"); gap = pd.Timedelta("7D")      # gap = label window
train = df[df.ts < cut - gap]; test = df[df.ts >= cut]
print(len(train), len(test), train.ts.max() < test.ts.min())    # 572 354 True
```

**Follow-ups:**
- *Detecting leakage?* A too-good metric, one dominant feature, or a collapse in production.
- *Cross-validation?* Rolling-origin splits (e.g. TimeSeriesSplit).

**Common mistakes:** random split, joining latest snapshots, scaling or encoding before splitting, ignoring the label-window gap.

### Q19 ⭐⭐ 🟢 When should you not use ML at all? How do you decide between rules, heuristics and a model?
**Asked at:** Fintech, consulting-style DS, startups
**Say this first (1 line):** Use ML only when the rule is too complex to write, there is enough data with a learnable signal, and errors are tolerable; otherwise start with rules or a heuristic.

**Then explain:**
- **Skip ML when:** a simple rule solves it (a regulatory threshold), there is little or no data, wrong predictions are very costly and must be explained exactly, or the problem is deterministic (tax calculation).
- **Rules/heuristics first:** fast, transparent, no training data; a good baseline and a fallback.
- **Use ML when:** many interacting signals, patterns change and need re-learning, scale is large, and the payoff of a few extra percent is real.
- **Hybrid wins often:** rules for hard constraints (block sanctioned countries), ML for the grey area.
- **Decision test:** build the heuristic baseline; if ML lifts the metric by less than its cost (infra, maintenance, monitoring), do not ship it.

**Example:** "Flag orders over Rs 1 lakh for manual KYC" is a rule. "Score thousands of subtle signals to catch mule accounts" is ML. A new product with 200 users should start with popularity-based recommendations.

**Follow-ups:**
- *How do you justify ML?* Show baseline vs model lift in rupees, minus maintenance cost.
- *When does a rule engine break down?* Hundreds of interacting rules become unmaintainable and cannot learn.

**Common mistakes:** reaching for ML by default, no baseline, forgetting maintenance cost, replacing rules that legal requires.

### Q20 ⭐⭐ 🟢 Do a back-of-envelope estimate of QPS, storage and latency budget for a ranking or fraud system.
**Asked at:** Amazon, Flipkart, Microsoft IDC, senior roles
**Say this first (1 line):** I work backwards from users and actions: requests per second, then data and compute per request, then storage, then split the latency budget across stages.

**Then explain:**
- **QPS:** DAU x requests per user per day / 86,400, then multiply by a peak factor (2-5x).
- **Compute:** candidates per request x model cost per candidate; this tells you if you need a cascade.
- **Storage:** events per day x bytes per event x retention; embeddings = items x dimension x 4 bytes.
- **Latency budget (e.g. 200 ms):** network 20-30, feature fetch 20-30, retrieval 20-30, ranking 50-80, re-rank and logging the rest. Leave a margin and a timeout fallback.
- State assumptions aloud and sanity-check the answer.

**Example:** 20M DAU x 30 requests = 600M per day, about 6,900 QPS average and about 21,000 at 3x peak. Ranking 500 candidates at 200 B of features each is about 2 GB/s of feature reads at peak, which says: precompute, cache, and keep per-candidate features small. Logging 1B impressions a day at 100 B each is about 100 GB/day, or 36.5 TB/year.

**Code:**
```python
dau = 20e6; req_per_user = 30; peak = 3
avg_qps = dau * req_per_user / 86400; peak_qps = avg_qps * peak
print(round(avg_qps), round(peak_qps))                                  # 6944 20833
print("MB/s features at peak:", round(peak_qps * 500 * 200 / 1e6))      # 2083
print("GB/day logs:", round(1e9 * 100 / 1e9), "TB/yr:", round(1e9 * 100 * 365 / 1e12, 1))  # 100 36.5
```

**Follow-ups:**
- *Fraud at 5,000 TPS and 100 ms?* Per-request model must take a few ms; use GBDT on CPU, with features precomputed in Redis.
- *What if ranking is too slow?* Cascade: cheap model first, heavy model on the top 50.

**Common mistakes:** forgetting the peak factor, mixing bits and bytes, ignoring feature-fetch latency, no fallback.

### Q21 ⭐⭐ 🟡 Design a dynamic / surge pricing system.
**Asked at:** Uber, Swiggy, Booking, airlines, Flipkart
**Say this first (1 line):** Forecast demand and supply per zone and time bucket, then set the price multiplier by an optimiser that balances conversion, supply response and fairness caps; it needs experiments to learn elasticity.

**Then explain (framework):**
- **Requirements:** match supply and demand, maximise completed trips/revenue, limit user backlash; guardrails: max multiplier, regulatory caps, stability (no wild flicker).
- **Data:** requests, available drivers, completed trips, prices shown and accepted, weather, events, time.
- **Models:** short-term demand forecast per zone (GBDT or time-series); price elasticity (conversion vs price) from randomised price experiments; supply response (do drivers come in).
- **Optimiser:** for each zone-bucket, choose the multiplier that maximises expected completed trips or revenue subject to the supply and caps, using the elasticity curve.
- **Evaluation:** forecast error offline; online A/B/switchback tests (the market is shared, so user-level A/B has interference) on completion rate, ETA, revenue, driver earnings, complaints.
- **Serving:** near-real-time (updates every 1-5 minutes), smoothing across zones and time.
- **Monitoring:** extreme multipliers, fairness across areas, forecast bias.
- **Trade-offs:** short-term revenue vs trust; price discrimination and legal risk.

**Example (illustrative numbers):** Rain hits a zone: demand forecast 3x normal, supply 1.2x. Assume constant elasticity of -1.5, so demand scales as price^-1.5. Solve 3 x m^-1.5 = 1.2: m = 2.5^(2/3), about 1.84x. That is under the 2x cap, so the optimiser picks about 1.8x. The elasticity itself must come from price experiments.

**Follow-ups:**
- *Why switchback experiments?* Randomising by zone-time blocks avoids users in the same market interfering with each other.
- *Is per-user pricing OK?* Risky for fairness and regulation; prefer market-level pricing.

**Common mistakes:** estimating elasticity from observational data (price and demand rise together), user-level A/B with interference, no caps or smoothing.

### Q22 ⭐⭐ 🟡 Design a notification / push system that decides what to send, to whom and when.
**Asked at:** Swiggy, Zomato, Flipkart, Spotify, PhonePe
**Say this first (1 line):** Treat it as a decision system: choose the best notification and send time per user by estimating response and harm (opt-outs), under frequency caps, and learn with bandits and holdouts.

**Then explain (framework):**
- **Requirements:** maximise long-term engagement and value, not opens; guardrails: opt-out/uninstall rate, spam complaints, daily caps.
- **Data and labels:** sends, opens, clicks, conversions, unsubscribes; control group with no notification to measure incremental effect.
- **Candidates:** eligible messages from triggers (cart abandonment, price drop) and campaigns.
- **Models:** per-message P(click) and P(conversion); an uplift model for incremental effect; a model for P(opt-out | send); send-time model (when does the user usually engage).
- **Decision:** for each user, pick the message with the highest expected value = benefit minus cost of annoyance, subject to caps and cool-downs; a bandit explores new content and timing.
- **Evaluation:** A/B with a persistent no-notification holdout, measuring retention, revenue, and opt-outs, not opens.
- **Serving:** batch for planned campaigns, real-time for triggers; throttling queue.
- **Monitoring:** opt-out spikes, per-channel fatigue.

**Example (illustrative numbers):** A user gets 3 pushes a day with a 5% CTR but starts to opt out; reducing to 1 well-chosen push keeps 80% of the clicks and cuts opt-outs in half. The holdout shows true uplift.

**Follow-ups:**
- *Why not predict clicks only?* Clicks on a push the user would have acted on anyway add nothing; incremental value matters.
- *Fatigue?* Include recent-send counts as features and enforce caps.

**Common mistakes:** optimising open rate, no holdout, ignoring opt-out cost, sending to everyone.

### Q23 ⭐⭐ 🟡 Design a content moderation or spam / abuse detection system.
**Asked at:** Social/product cos, ShareChat, Microsoft
**Say this first (1 line):** A layered pipeline: cheap rules and hash matching, then ML classifiers (text, image, behaviour), then human review for the uncertain middle, with appeals and a feedback loop.

**Then explain (framework):**
- **Requirements:** remove harmful content fast while limiting wrongful takedowns; categories (spam, hate, scams, nudity) have different costs; latency from real-time (pre-publish) to minutes.
- **Data and labels:** user reports, moderator decisions, appeals outcomes. Labels are noisy and policy-dependent, so write clear guidelines and measure inter-annotator agreement.
- **Layers:** (1) blocklists, regex, hash matching of known bad media, rate limits; (2) classifiers: text (fine-tuned transformer), image/video models, plus behaviour signals (new account, burst posting, link patterns, network graph); (3) human review.
- **Decisions:** high-confidence = auto-action; mid-confidence = review queue ordered by severity and reach; low = allow and sample.
- **Evaluation:** precision and recall per category (precision for auto-remove; recall for severe harms), time-to-removal, prevalence (estimated from random sampling), appeal overturn rate.
- **Serving:** real-time for new posts, async for deep models; cascade for cost.
- **Monitoring:** adversarial adaptation (misspellings, emoji), language/regional coverage, drift.
- **Trade-offs:** free speech vs safety; false positives hurt creators.

**Example:** Spam bot posts 200 links in a minute; a rate limit and a behaviour model catch it before any text model runs. A borderline hate-speech post scores 0.6 and goes to a human, whose decision becomes training data.

**Follow-ups:**
- *Measuring prevalence when harm is rare?* Random sample reviewed by humans, stratified.
- *LLMs?* Useful for policy-aware labelling and edge cases; use a distilled classifier for volume.

**Common mistakes:** one global threshold, using accuracy, no appeals, relying on user reports only (biased).

### Q24 ⭐⭐ 🟡 Design an anomaly detection system for business or payment metrics.
**Asked at:** Fintech, GCCs, Walmart
**Say this first (1 line):** Model the expected value of a metric given its seasonality, detect deviations with a statistical or ML residual test, and route alerts by severity so on-call is not flooded.

**Then explain (framework):**
- **Requirements:** which metrics (payment success rate, orders per minute), detection delay, tolerance for false alarms; the cost of a missed outage vs alert fatigue.
- **Data:** metric time series at minute/hour grain, with dimensions (bank, region, device, merchant).
- **Methods, simple to complex:** static thresholds; rolling mean and z-score or robust (median/MAD); seasonal decomposition (STL) with residual thresholds; Prophet/forecast-based bands; isolation forest or autoencoders for multivariate cases.
- **Key design:** compare to the same hour last week to handle seasonality; for rates use binomial tests that account for small volume; drill down by dimension to localise root cause (e.g. one bank's success rate dropped).
- **Alerting:** severity from deviation size and business impact; deduplicate, group, suppress during known events (sales).
- **Evaluation:** replay historic incidents, measure precision, recall, detection delay.
- **Monitoring:** alert volume, ack rate, feedback labels "real/false" retrain thresholds.
- **Trade-offs:** sensitivity vs noise.

**Example:** UPI success rate is normally 97% at 2 pm with a small spread; today it is 91% for HDFC-issued transactions only. A global alert would miss it (overall 96%), but the dimensional drill-down catches it in 5 minutes.

**Follow-ups:**
- *Unlabelled data?* Use unsupervised methods and collect analyst feedback.
- *Sale-day spikes?* Include calendar features or suppress via event flags.

**Common mistakes:** fixed thresholds on seasonal data, only aggregate metrics, no drill-down, ignoring small-sample noise.

### Q25 ⭐⭐ 🟡 Design a model to predict cash-on-delivery order cancellations or return-to-origin (RTO) in Indian e-commerce.
**Asked at:** Flipkart, Meesho, Amazon India
**Say this first (1 line):** Predict at order placement the probability a COD order will be cancelled or returned undelivered (RTO), then act with cheap interventions (confirm by call/WhatsApp, prepay nudge, restrict COD) where the expected loss exceeds the cost.

**Then explain (framework):**
- **Requirements:** RTO costs shipping both ways plus handling, and RTO rates on COD can be high in some categories; goal is lower RTO without losing genuine orders; decision at checkout in under 100 ms.
- **Data and labels:** orders with outcome (delivered / RTO / customer cancel); label matures after delivery attempts (about 7-15 days).
- **Features:** pin code RTO history, order value, category, COD vs prepaid, customer history (past RTOs), new vs repeat, time of order, address quality (completeness, geocode match), phone validity, courier performance in that pin code, discount depth.
- **Model:** GBDT with calibrated probabilities; segment by new vs repeat customers.
- **Actions by score:** low = ship; medium = automated confirmation call or WhatsApp; high = require prepayment or cancel COD option.
- **Evaluation:** PR-AUC and calibration, time split; business: net savings = avoided RTO cost - lost sales - intervention cost; A/B with a holdout, since restricting COD may lose genuine customers.
- **Monitoring:** RTO rate by pin code, drift around festival sales, courier changes.
- **Trade-offs:** blocking COD in some regions may hurt access and growth; fairness concerns on pin-code proxies.

**Example (illustrative numbers):** Order of Rs 899 COD from a new customer in a pin code with 35% RTO and a vague address scores 0.6; expected loss = 0.6 x Rs 150 = Rs 90, call cost is Rs 5, so confirm first; if unreachable, offer a prepaid discount.

**Follow-ups:**
- *Why not just block high-risk pin codes?* Blunt and loses good customers; model plus interventions is more precise.
- *Cold-start customers?* Use pin code, address and device features.

**Common mistakes:** ignoring label maturation, leakage via delivery-attempt data, not measuring lost genuine orders, no intervention design.

### Q26 ⭐⭐ 🟡 Design a product-return prediction system for a fashion marketplace.
**Asked at:** Zalando, Myntra, Amazon
**Say this first (1 line):** Predict return probability per order line (often by reason: size/fit vs quality) before purchase, so the product can fix the cause (size guidance, listing quality) and pricing and logistics can account for expected returns.

**Then explain (framework):**
- **Requirements:** returns are a major cost in fashion (return rates can be very high); decide the intervention: size recommendations, a warning, fee, or just forecasting for inventory; guardrail: do not cut conversion.
- **Data and labels:** order lines with return flag and reason, within the return window (about 7-30 days; label matures after).
- **Features:** category, brand, price, size and fit signals (size chosen vs usual size), user return history, past bundle orders ("bracketing": buying two sizes), seller quality score, image/text quality, reviews mentioning fit, discount.
- **Model:** GBDT per category group or a single model with embeddings; multi-class on reason; calibrate.
- **Actions:** size recommendation based on past purchases, "runs small" nudges, seller quality interventions, adjust ranking by expected net revenue (revenue x (1 - P(return)) minus return cost).
- **Evaluation:** PR-AUC and calibration, time split, by category; A/B on return rate, net revenue, and conversion.
- **Monitoring:** seasonal drift, seller changes, new brand cold start.
- **Trade-offs:** penalising high-return items hurts honest sellers; serial returners vs genuine fit problems.

**Example:** A customer who usually buys M selects S in a slim-fit brand with reviews saying "runs small": P(return) = 0.55. The page shows "Customers say size up", which reduces the return probability and improves the experience.

**Follow-ups:**
- *Ranking impact?* Rank by expected net contribution, not clicks.
- *Fraudulent returns?* Separate model for abuse (wardrobing) versus fit.

**Common mistakes:** one label for all return reasons, leakage from post-delivery signals, ignoring the maturation window, treating returns as purely a customer problem.

### Q27 ⭐⭐ 🟡 Design a customer lifetime value (LTV) prediction system.
**Asked at:** Booking, Spotify, fintech, e-commerce
**Say this first (1 line):** Predict the future value a customer will generate (for example 12-month margin) from early behaviour, so marketing, retention and acquisition budgets go to high-value customers and not just high-volume ones.

**Then explain (framework):**
- **Requirements:** define value first: margin, not revenue, over a fixed horizon (6-12 months), net of returns and servicing cost. Decide the decision it drives: acquisition bid caps, retention spend, VIP treatment. Latency is batch (daily or weekly).
- **Data and labels:** snapshot customers at an "observation date" (say day 30 after signup), label = margin in the next N months. Long horizons mean labels arrive late, so train on older cohorts and accept staleness.
- **Features:** recency, frequency, monetary value, category mix, channel of acquisition, first-order basket, discount dependence, support contacts, device, geography.
- **Model:** two options. (1) Probabilistic (BG/NBD + Gamma-Gamma): explainable, good with sparse repeat-purchase data. (2) GBDT regression on RFM-style features, often with a log target or a two-part model (P(buy) x expected spend) because value is zero-inflated and heavy-tailed.
- **Evaluation:** time-based split by cohort; rank metrics (Spearman, decile lift, Gini of cumulative value) matter more than RMSE because decisions are about ranking; check calibration at the aggregate level (predicted total vs actual total per decile).
- **Serving and monitoring:** batch scores in the warehouse; monitor cohort drift, calibration by acquisition channel, and realised versus predicted LTV as labels mature.
- **Trade-offs:** whales dominate error, so cap or winsorise; LTV is correlated with past discounts and treatment, so it is not the same as uplift.

**Example (illustrative):** Customer A: 1 order of Rs 400, bought on a 50% promo. Customer B: 3 orders of Rs 900 each at full price. Predicted 12-month margin is Rs 60 versus Rs 1,100, so B gets the premium retention budget and a higher acquisition bid for similar profiles.

**Follow-ups:**
- *How do you validate when the horizon is 12 months?* Backtest on cohorts old enough to have matured, and use early proxies (90-day value) for fast iteration.
- *LTV for targeting a coupon?* LTV says who is valuable, not who will respond; use uplift modelling for the coupon decision.

**Common mistakes:** revenue instead of margin, leakage from data after the observation date, optimising RMSE on a heavy-tailed target, treating LTV as a causal effect.

### Q28 ⭐⭐ 🟡 Design a lead scoring / propensity-to-buy model for sales or lending.
**Asked at:** Fintech, banks, SaaS, GCCs
**Say this first (1 line):** Score each lead on the probability it converts within a defined window, so the sales or collections team works the best leads first, and validate that the ranking actually raises conversion per call and not just AUC.

**Then explain (framework):**
- **Requirements:** define conversion (loan disbursed, demo booked, paid account) and the window (30 days). Constraint: limited agent capacity, so the metric is conversions per agent-hour or per Rs of marketing spend.
- **Data and labels:** lead snapshot at creation time; label = converted within window. Many leads are still "open", so wait for the window to close or use survival-style handling.
- **Features:** source and campaign, firmographics or demographics, app activity, form completeness, time to first response, past interactions, bureau score for lending (with consent). Avoid features that only exist after sales contact.
- **Model:** logistic regression or GBDT with calibration; segment by product. For lending, add an eligibility or risk gate so you do not chase leads who would be declined.
- **Evaluation:** PR-AUC, lift in top deciles, calibration; online: A/B where the treatment team uses the score for priority and the control uses current rules.
- **Serving:** batch re-score plus real-time at lead creation so first contact is fast (speed to lead matters a lot).
- **Monitoring:** conversion by score decile, source mix drift, agent behaviour changes (agents ignore the score).
- **Trade-offs:** bias against hard-to-convert but valuable segments; low-score leads never get worked, so keep a small random exploration slice.

**Example (illustrative):** 10,000 leads a day, agents can call 2,000. Baseline calls a random 2,000 at 4% conversion = 80. Top-20% of scores converts at 12% = 240 conversions, a 3x lift.

**Follow-ups:**
- *Why a random slice?* Without it the model only sees outcomes for leads it chose, which freezes its own bias.
- *Propensity vs uplift?* Propensity targets people who would buy anyway; uplift targets people the call changes.

**Common mistakes:** leakage from sales-stage fields, ignoring capacity, no holdout, scoring that never changes agent behaviour.

### Q29 ⭐⭐ 🟡 Design a Spotify-style personalised playlist / 'because you watched' recommender.
**Asked at:** Spotify, Netflix-type, Hotstar
**Say this first (1 line):** Build a two-stage recommender: generate a few hundred candidates per user with embeddings and collaborative signals, then rank them with a model that optimises long-term satisfaction, with a layer for diversity, freshness and business rules.

**Then explain (framework):**
- **Requirements:** goal is satisfaction and retention (listening time that is not skipped, saves, return rate), not raw clicks. Home page latency under about 200 ms; playlists can be pre-computed offline.
- **Data:** implicit feedback (plays, skips, completes, saves, repeats), item metadata and audio embeddings, context (time of day, device).
- **Candidate generation:** two-tower or matrix factorisation embeddings with approximate nearest-neighbour search, plus "recently played", "similar to X" and editorial/popular sources.
- **Ranking:** GBDT or deep ranker with features such as user-item affinity, recency, skip rate, item popularity trend; label = engaged (played over 30 s or saved), with skips as negatives.
- **Re-ranking:** diversity (no 10 songs by one artist), freshness, explicit "because you listened to X" explanation, and removing recently shown items.
- **Evaluation:** offline recall at K and NDCG with time split; online A/B on satisfaction metrics and long-term retention, not only CTR; guardrails on diversity and artist exposure.
- **Cold start:** content embeddings and popularity for new items; onboarding picks for new users.
- **Monitoring:** feedback loops (popular items get more plays), embedding drift, filter-bubble metrics.

**Example (illustrative):** A user plays jazz at night and workout music in the morning. Context-aware candidates fill a "Late night jazz" shelf, ranked by predicted completion, and one exploratory slot tries a new artist similar to their saves.

**Follow-ups:**
- *Skips as negative labels?* Short skips are a strong negative; but a skip can also mean "already know this song".
- *How do you test "because you watched" explanations?* A/B: same ranking, with and without explanation, measure engagement.

**Common mistakes:** optimising clicks, ignoring the popularity feedback loop, one big model with no candidate stage, forgetting diversity and cold start.

### Q30 ⭐⭐ 🟡 Design a restaurant / dish ranking system for a food-delivery app.
**Asked at:** Swiggy, Zomato, DoorDash
**Say this first (1 line):** Rank restaurants and dishes per user by the expected probability they order and are happy with the order, using ETA, price, availability and personal taste, with explicit exploration for new restaurants.

**Then explain (framework):**
- **Requirements:** target is conversion and repeat orders, subject to delivery-time and quality guardrails. Hard constraints first: restaurant is open, serviceable address, items in stock.
- **Retrieval:** filter by geography and open status, then retrieve by cuisine, past orders, popular nearby, and embedding similarity.
- **Features:** user-restaurant history, cuisine affinity, price band fit, restaurant rating and rating count, predicted delivery time, delivery fee, current discount, time of day, weather, restaurant prep-time reliability, image quality.
- **Model:** GBDT ranker (LambdaMART) or neural ranker; label = order, with a secondary model for post-order outcome (rating, cancellation, delay). Final score = P(order) x quality adjustments.
- **Evaluation:** NDCG and order-per-impression offline; A/B on orders per session, repeat rate, delivery-time complaints.
- **Cold start:** new restaurants get a bounded exploration boost (bandit style), not a permanent one.
- **Monitoring:** position bias, supply-side fairness (small restaurants), peak-hour drift, ETA error since a bad ETA hurts the rank.
- **Trade-offs:** sponsored listings versus relevance; ranking a fast restaurant higher can starve far but loved ones.

**Example (illustrative):** At 8 pm a user with 5 past biryani orders sees a biryani place with 4.4 stars, 30-minute ETA and Rs 40 fee ranked above a 4.6 star place with a 55-minute ETA, because ETA strongly lowers order probability.

**Follow-ups:**
- *Dish-level vs restaurant-level?* Rank restaurants on the home page, then dishes inside the page using the same user taste vector.
- *Position bias?* Log the position and correct with propensity or randomise a slice (see Q49).

**Common mistakes:** ignoring availability and ETA, rating-only ranking, no cold-start plan for restaurants, optimising clicks over completed orders.

### Q31 ⭐⭐ 🟡 Design a customer-support ticket routing and prioritisation system.
**Asked at:** Amazon, Microsoft, SaaS, GCCs
**Say this first (1 line):** Treat it as text classification plus priority scoring: classify the ticket into a queue (and urgency), route to the right team, and rank by expected business impact and SLA risk, with a human fallback when confidence is low.

**Then explain (framework):**
- **Requirements:** goals are lower time-to-first-response and fewer reassignments. Metrics: routing accuracy, reassignment rate, SLA breaches, customer satisfaction.
- **Data and labels:** historical tickets labelled by the team that finally resolved them (not the first assignee, which is often wrong); urgency from escalations and SLA.
- **Features:** ticket text (embeddings or a fine-tuned transformer), product and plan, customer tier, past tickets, channel, language, attachment presence, time.
- **Model:** start with TF-IDF plus logistic regression as a baseline; move to embedding-based classifier. An LLM can help for multilingual or rare categories, but cost and latency matter at volume. Separate priority model: predicted escalation, churn risk, SLA clock.
- **Serving:** real-time at ticket creation (under a second); confidence thresholds: high = auto-route, medium = suggest to agent, low = triage queue.
- **Evaluation:** macro F1 (rare queues matter), confusion matrix between neighbouring teams, per-language results; online: reassignment rate and resolution time.
- **Monitoring:** new product launches create new topics (drift), label noise from agent mistakes, queue load balancing.
- **Trade-offs:** auto-route accuracy versus risk of misrouting a VIP; fairness across languages.

**Example (illustrative):** "Payment deducted but order failed" from a premium customer is classified as Payments, urgency high, and jumps the queue; an "update my address" ticket goes to the low-priority self-service macro.

**Follow-ups:**
- *New category appears?* Fallback to "other", cluster unrouted tickets weekly, add a class.
- *Where does an LLM fit?* Summaries and suggested replies; use the classifier for routing since it is cheaper and measurable.

**Common mistakes:** using first-assignee labels, accuracy on imbalanced classes, no confidence fallback, ignoring SLA when prioritising.

### Q32 ⭐⭐ 🟡 How do you design real-time velocity and aggregate features for fraud, and where do they live (feature store)?
**Asked at:** PhonePe, Paytm, Klarna, JPMC
**Say this first (1 line):** Compute counts and sums over sliding windows (for example transactions per card in the last 10 minutes) in a streaming job, store them in a low-latency key-value store keyed by entity, and use the same definitions offline so training and serving match.

**Then explain (framework):**
- **What features:** velocity (count, amount sum, distinct merchants/devices/IPs per card or user in 1 min, 1 hr, 24 hr), ratios versus the user's own history, time since last transaction.
- **Online path:** event stream (Kafka) -> stream processor (Flink or Spark Structured Streaming) -> online store (Redis or similar) keyed by entity. At scoring time the model service does a key lookup, adding a few milliseconds.
- **Offline path:** the same feature definitions, computed point-in-time correct from event logs for training; a feature store (Feast, Tecton, or in-house) enforces one definition for both.
- **Trick for freshness:** the transaction being scored is not yet in the stream aggregate, so combine stored aggregate with the current event in the scoring code.
- **Skew risks:** processing-time vs event-time, late events, different window boundaries, timezone bugs. Log the exact feature values served and train on the logged values when possible.
- **Cost trade-off:** many windows x many entities = a lot of state; use approximate sketches (HyperLogLog for distinct counts) and TTLs.
- **Monitoring:** feature freshness lag, null rates, online vs offline value comparison on a sample.

**Example (illustrative):** A card makes 6 transactions in 3 minutes across 4 merchants. Features: txn_count_5m = 6, distinct_merchants_5m = 4, amount_sum_1h = Rs 48,000 versus a usual Rs 2,000, and the model flags it.

**Follow-ups:**
- *Why not compute from the database at request time?* Too slow and loads the transactional DB.
- *How do you avoid leakage offline?* Point-in-time joins using event time, only data before the transaction.

**Common mistakes:** different window logic offline vs online, including the current transaction in training aggregates, ignoring late events, no freshness monitoring.

### Q33 ⭐⭐ 🟡 How do you handle concept drift and adversaries adapting in a fraud system?
**Asked at:** Fintech, Klarna, PhonePe, GCCs
**Say this first (1 line):** Assume fraudsters adapt to whatever you deploy, so combine frequent retraining with fresh labels, features that are hard to evade, rules for fast reaction, and anomaly/graph signals that do not depend on past labels.

**Then explain (framework):**
- **Concept drift vs adversarial drift:** normal drift (seasonality, new merchants) is gradual; adversarial drift is targeted, abrupt, and reacts to your decisions.
- **Detect it:** monitor fraud rate, score distribution, alert rate, feature PSI, and performance on matured labels by segment; investigate sudden changes in the approval rate of one merchant or BIN.
- **Label delay:** chargebacks arrive 30-90 days late, so use fast proxies (analyst decisions, customer disputes) and delay-aware training (Q48).
- **Respond:** frequent retraining with recent data weighted more, champion-challenger, and a rule layer that can be changed in hours for emerging attacks.
- **Make evasion costly:** use features that are costly to fake (device and network graph links, behavioural biometrics), avoid exposing decision reasons to attackers, and rate-limit probing.
- **Complement supervised models:** unsupervised anomaly detection, graph features (shared devices, accounts), and human review for novel patterns.
- **Trade-offs:** reacting fast risks overfitting to one attack and raising false positives on good users.

**Example (illustrative):** After you block transactions above Rs 10,000 from new devices, fraud shifts to many Rs 9,500 attempts. Velocity and device-graph features catch the pattern, and a rule goes live the same day while the model retrains next cycle.

**Follow-ups:**
- *Why not retrain every hour?* Label scarcity and noise; instead use daily refresh for features and weekly full retrain plus an emergency path.
- *Selection bias?* Blocked transactions have no label; keep a small random-approve holdout where the loss is tolerable.

**Common mistakes:** assuming a static distribution, evaluating on old data only, no fast rule path, ignoring that labels are biased by past decisions.

### Q34 ⭐⭐ 🟡 How do you roll out a new model safely (shadow, canary, A/B) and decide to ramp up?
**Asked at:** Amazon, Flipkart, Spotify, Microsoft
**Say this first (1 line):** Roll out in stages: offline checks, shadow mode (no user impact), a small canary with guardrails, then an A/B test; ramp only when pre-agreed metrics hold and keep an instant rollback.

**Then explain:**
- **Offline gate:** backtest on recent data, slice metrics, latency and cost check, and fairness check where relevant.
- **Shadow mode:** the new model scores live traffic but its output is only logged. Compare against the current model for score drift, latency, errors and disagreement; no user risk.
- **Canary:** route 1-5% of traffic (by user hash, so the same user always sees the same model) while watching guardrail metrics: errors, latency, key business metrics.
- **A/B test:** pre-register the primary metric, guardrails, sample size and duration; run at least a full weekly cycle to cover weekday effects.
- **Ramp-up:** 5% -> 25% -> 50% -> 100%, with automatic rollback on a guardrail breach. Keep a holdout of old model or no-model for a while to measure long-term effects.
- **Special cases:** fraud and credit models have delayed labels, so use proxy metrics (alert rate, review precision) early and decide on matured labels later. Marketplaces have interference between users, so use cluster or switchback randomisation.

**Example (illustrative):** A new ranker is shadowed for 3 days with 98% score correlation to the old one on top-10 items, canaried at 5% for 2 days with latency p99 under 150 ms, then A/B at 50% for 14 days: +1.2% orders, no guardrail drop, ramp to 100%.

**Follow-ups:**
- *Shadow vs canary?* Shadow checks technical behaviour with zero user effect; canary measures real user impact on a small group.
- *When is A/B impossible?* When effects spill over or traffic is tiny; use switchback, diff-in-diff, or interleaving for rankers.

**Common mistakes:** peeking and stopping early, no guardrails, not randomising by user, ramping without a rollback plan.

### Q35 ⭐⭐ 🟡 How do you reduce inference cost and latency (cascade models, distillation, caching, quantisation) without losing quality?
**Asked at:** Amazon, Flipkart, Microsoft IDC, product cos
**Say this first (1 line):** First measure where the time and money go, then apply the cheapest wins in order: cache, smaller or simpler models via a cascade, batching, quantisation, and distillation, validating each against the quality metric.

**Then explain:**
| Technique | What it does | Watch out for |
|---|---|---|
| Caching | Reuse outputs for repeated inputs or precompute scores offline | Staleness, cache hit rate |
| Cascade | Cheap model handles easy cases, expensive model only the hard ones | Threshold tuning, recall loss at the first stage |
| Distillation | Train a small "student" to mimic a large "teacher" outputs | Student gap on tail cases |
| Quantisation | Use int8/fp16 weights for faster, smaller inference | Small accuracy drop, hardware support |
| Pruning / smaller features | Drop expensive features and layers | Feature value vs lookup cost |
| Batching and hardware | Dynamic batching, ONNX/TensorRT, GPU vs CPU | Latency versus throughput |

- **Method:** profile first (feature fetch is often the bottleneck, not the model); set a quality budget (for example at most 0.5% relative NDCG loss) and latency budget (p99).
- **Evaluate:** compare against the full model on the same data, check slices and tail, and A/B for real impact.
- **For LLM-based components:** shorter prompts, smaller model for easy cases, response caching, batching.

**Example (illustrative):** A fraud model costs 40 ms. A small GBDT scores everything in 3 ms; only the 15% of transactions in the uncertain band go to the heavy graph model. Average latency drops to about 8 ms and the heavy model's compute cost falls by 85%, with recall unchanged on the validation set.

**Follow-ups:**
- *Distillation vs quantisation?* Distillation changes the model (needs training); quantisation changes number precision (usually post-training).
- *Cascade risk?* Stage one must have very high recall for what it filters, or you lose positives permanently.

**Common mistakes:** optimising the model when feature fetching is the bottleneck, no quality budget, testing only average latency instead of p99, skipping slice checks.

### Q36 ⭐⭐ 🟡 How do you incorporate exploration vs exploitation (bandits) into a recommender or notification system?
**Asked at:** Spotify, Flipkart, Booking, Meta-type
**Say this first (1 line):** Use a bandit when you need to learn what works while serving: mostly show the best-known option, but give uncertain options a controlled share of traffic so the system keeps learning and does not lock into its own past choices.

**Then explain:**
- **Why:** a purely greedy recommender only learns about what it already shows, so new items never get data (feedback loop, Q17).
- **Methods:** epsilon-greedy (random slice, simple), Thompson sampling (sample a belief per option, pick the best sample; explores more when uncertain), UCB (optimism under uncertainty), contextual bandits (LinUCB, or a model plus exploration) when the best choice depends on user context.
- **In recsys:** reserve explore slots for new or low-data items; add uncertainty to the ranker score; log the propensity (probability of showing) so you can do unbiased offline evaluation later (Q49).
- **In notifications:** treat each message template/time as an arm; reward = click or purchase minus an unsubscribe penalty.
- **Practicalities:** delayed rewards, non-stationary arms (discount decay), cap exploration cost with guardrails, and measure regret or exploration cost.
- **Trade-off:** exploration costs short-term metrics for long-term learning.

**Example (illustrative):** Three banners with true CTRs 4%, 5%, 8%. Thompson sampling quickly sends most traffic to the 8% banner while still testing the others.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(0)
true_ctr = np.array([0.04, 0.05, 0.08])       # illustrative
a = np.ones(3); b = np.ones(3)                 # Beta(1,1) priors
clicks = 0
for t in range(5000):
    arm = np.argmax(rng.beta(a, b))            # sample belief per arm, pick best sample
    r = rng.random() < true_ctr[arm]
    a[arm] += r; b[arm] += 1 - r; clicks += r
print("pulls per arm:", (a + b - 2).astype(int), "total CTR:", round(clicks / 5000, 4))
# pulls per arm: [ 104  163 4733] total CTR: 0.072
```

**Follow-ups:**
- *Bandit vs A/B test?* A/B gives clean inference on a fixed set; a bandit maximises reward while learning but makes inference messier.
- *Why log propensities?* They let you evaluate new policies offline with IPS.

**Common mistakes:** exploring with no logging of probabilities, exploring on high-stakes surfaces without guardrails, ignoring non-stationarity, using bandits when delayed rewards make feedback too slow.

### Q37 ⭐⭐ 🟡 How do you design a human-in-the-loop review queue for fraud or moderation and use analyst feedback as labels?
**Asked at:** Fintech, JPMC, Klarna, PhonePe
**Say this first (1 line):** Send the uncertain or high-impact cases to analysts through a prioritised queue, record their decisions with reasons in a structured way, and feed those decisions back as labels, while keeping an unbiased sample so the model is not trained only on what it already flagged.

**Then explain:**
- **Routing by score:** auto-allow below a low threshold, auto-block above a high one, human review in between; the review band is sized to analyst capacity.
- **Prioritisation:** order the queue by expected loss (score x amount) and SLA, not by arrival time; active learning style: add some uncertain cases to the queue because their labels are the most informative.
- **Label quality:** structured outcomes (fraud, not fraud, unsure), reasons, and review time; double-review a sample to measure agreement, track analyst bias and fatigue, and use gold-standard cases for calibration.
- **Selection bias:** only reviewed cases get labels. Keep a random sample of auto-allowed and low-score cases for review (small cost) to estimate true miss rate and train unbiased.
- **Feedback into the model:** analyst labels are fast (hours) versus chargebacks (weeks), so use them for quick retraining, but weight them less than confirmed outcomes if noisy.
- **Tooling:** show explanations (top features), related entities and history so analysts decide faster.
- **Metrics:** precision of the review queue, analyst throughput, time to decision, false positive rate on good users, label agreement.

**Example (illustrative):** 100,000 transactions a day, 300 reviewed at capacity. The model sends scores 0.6-0.9 for review and 20 random low-score cases for audit; the audit shows 0.5% fraud in the "safe" group, a gap the model would never have found otherwise.

**Follow-ups:**
- *Analysts disagree?* Use consensus or adjudication, and model label noise (soft labels).
- *Does review capacity change the threshold?* Yes, the threshold is set by capacity and cost, not fixed at 0.5.

**Common mistakes:** training only on reviewed cases, ordering the queue by time, no audit sample, ignoring analyst disagreement.

### Q38 ⭐⭐ 🟡 How do you ensure explainability and regulatory compliance (RBI, GDPR, EU AI Act) in a credit or fraud model?
**Asked at:** Banks/GCCs, Klarna, Europe fintech
**Say this first (1 line):** Use inherently interpretable or well-explained models, document everything (data, features, validation, decisions), test for bias, keep humans accountable for decisions, and map each regulation to concrete controls.

**Then explain:**
- **Explainability:** a scorecard-style logistic regression or a GBDT with monotonic constraints plus SHAP for per-decision reason codes; global explanations for model governance.
- **Regulations (summary, check current text):**
  - *India (RBI):* expects model risk management, board-approved policies, and fair-practice and transparency in digital lending (RBI digital-lending directions cover disclosures, consent and data handling); the DPDP Act adds consent and purpose rules for personal data.
  - *GDPR (Europe):* rules on automated decisions, with the right to meaningful information about the logic and to human review of solely automated decisions.
  - *EU AI Act:* creditworthiness scoring of individuals is listed as a high-risk use case; high-risk systems need risk management, data governance, documentation, logging, human oversight, accuracy and robustness. Application dates are phased and have been under revision, so check current timelines.
- **Controls:** model cards and documentation, independent validation, reason codes for adverse decisions, audit logs of inputs and versions, human override, periodic fairness and performance review, and a change-management process.
- **Data controls:** purpose limitation, data minimisation, no prohibited attributes, and a check for proxies.
- **Trade-offs:** an interpretable model may lose a little accuracy; a complex model needs more governance. In regulated credit, a simpler model that you can defend often wins.

**Example (illustrative):** A loan is declined. The notice shows the top three reasons from SHAP: "high utilisation on existing credit", "short credit history", "recent missed payment". The customer can request human review.

**Follow-ups:**
- *Is SHAP enough?* It explains the model, not causality, and can be unstable with correlated features, so pair with monotonic constraints and stability tests.
- *Who is accountable?* The business owner and model risk function, not the algorithm.

**Common mistakes:** claiming SHAP equals causal explanation, using proxy features for protected attributes, no audit trail, treating compliance as a final-stage task.

### Q39 ⭐⭐ 🟡 AI-era: when would you use an LLM inside a classic ML system (classification, feature extraction, explanations) versus a trained classifier or embedding model?
**Asked at:** Product cos 2025-26, Amazon, Microsoft; GenAI depth in Book 2
**Say this first (1 line):** Use a trained classifier or embedding model when you have labels, high volume and tight latency or cost limits; use an LLM when the task needs language understanding with little labelled data, flexible output, or generated text, and often use the LLM to bootstrap the cheaper model.

**Then explain:**
| Need | Better choice | Why |
|---|---|---|
| High-volume, low-latency scoring (fraud, ranking) | Trained model | Milliseconds, cheap, measurable |
| Stable classes, plenty of labels | Trained classifier | Better accuracy per rupee |
| Few labels, new or changing categories | LLM zero/few-shot | No training data needed |
| Feature extraction from messy text (reasons, addresses, reviews) | LLM offline, feed outputs as features | Run once, store the result |
| Explanations, summaries, agent drafts | LLM | Generation is its strength |
| Similarity, retrieval, clustering | Embedding model | Cheap, fast, good for search |

- **Pattern:** use the LLM to label data (then validate on a human-labelled sample), train a small classifier on those labels, and serve the small model.
- **Risks:** hallucination, nondeterminism, prompt injection, cost and latency, and data privacy when sending text to external APIs.
- **Evaluation:** a fixed human-labelled test set, agreement rate, cost per 1,000 calls, and monitoring for model version changes.
- **Rule:** never let an LLM make a regulated or irreversible decision alone.

**Example (illustrative):** Classifying 200 refund-reason types in tickets: LLM labels 20,000 tickets, humans verify 500, a small classifier trained on the labels reaches comparable accuracy at a tiny fraction of the cost and under 10 ms.

**Follow-ups:**
- *When is an LLM ranker justified?* Low volume, high-value decisions, or re-ranking a short list.
- *How do you control cost?* Cascade (classifier first, LLM for low confidence), caching, smaller models.

**Common mistakes:** using an LLM for everything, skipping a human-labelled test set, ignoring latency and cost at scale, trusting LLM labels without validation.

### Q40 ⭐⭐ 🟡 AI-era: how do embeddings, two-tower models and vector search change retrieval in search and recommendation systems?
**Asked at:** Flipkart, Amazon, Spotify, Booking; algorithm depth in Part 7
**Say this first (1 line):** Embeddings turn users and items into vectors so retrieval becomes nearest-neighbour search: a two-tower model learns the vectors, an ANN index finds candidates in milliseconds, and a heavier ranker refines the shortlist.

**Then explain:**
- **Two-tower model:** one network encodes the user (history, context), another encodes the item (text, image, metadata); trained so matching pairs have a high dot product. Item vectors are precomputed and indexed; the user vector is computed at request time.
- **Vector search:** exact search is too slow at millions of items, so use ANN (HNSW graph, IVF-PQ, ScaNN, or libraries like FAISS) trading a small recall loss for huge speed.
- **What changes vs keyword search:** semantic matching ("running shoes" finds "jogging sneakers"), works across languages and with images, and helps cold start through content embeddings.
- **Hybrid retrieval:** combine BM25 (exact terms, SKUs, brand names) with vector retrieval, then re-rank. Pure vector search misses exact matches.
- **Training details:** in-batch negatives are cheap but popularity-biased (correct with logQ correction or add hard negatives); fresh item embeddings need regular index updates.
- **Evaluation:** recall at K for retrieval, NDCG for the final ranking, then online A/B. Check ANN recall versus exact search.
- **Trade-offs:** two-tower is fast but cannot model user-item interactions deeply (that is the ranker's job); index memory and freshness.

**Example (illustrative):** 5 million products, ANN retrieves 500 candidates in about 10 ms; a GBDT ranker scores them in about 30 ms with richer features, and the page renders in under 150 ms.

**Follow-ups:**
- *Why not use the two-tower as the ranker?* It sees user and item separately; cross features (price vs user budget) need a ranker.
- *How do you handle new items?* Content-based embedding from text and images, plus exploration.

**Common mistakes:** pure vector search without lexical fallback, ignoring popularity bias in negatives, not measuring ANN recall, stale item index.

### Q41 ⭐⭐ 🔴 Design a delivery-partner / driver assignment (matching) system.
**Asked at:** Swiggy, Zomato, Uber, DoorDash
**Say this first (1 line):** Batch orders and available riders in short windows (for example every few seconds), predict the cost of each order-rider pair (pickup time, delivery time, food waiting, rider fairness), then solve an assignment problem to minimise total cost, instead of greedily giving each order its nearest rider.

**Then explain (framework):**
- **Requirements:** minimise delivery time and food-waiting time, keep riders productive and paid fairly, and respect capacity and shift limits. Decision latency of a few seconds.
- **Predictive part:** ETA models for rider-to-restaurant travel, restaurant prep time (often the main uncertainty), and drop-off travel; acceptance probability of each rider.
- **Optimisation part:** build a cost matrix; solve min-cost matching (Hungarian algorithm, or MIP/min-cost flow when batching multiple orders per rider). Add constraints such as max orders per bag, time windows and rider zones.
- **Why batching beats greedy:** nearest-rider-first can leave a later order with a far rider; matching looks at the whole set (see code).
- **Evaluation:** offline simulator replaying historical orders; online switchback tests (alternate policies by time-region blocks) because riders and orders interact.
- **Monitoring:** assignment time, rejection rates, idle time, late deliveries, and ETA calibration.
- **Trade-offs:** a longer batching window gives better matches but adds waiting; fairness across riders.

**Example (illustrative):** Four orders and four riders in a 5 km area. Optimal matching gave 6.13 km total pickup distance versus 8.46 km for greedy in the run below.

**Code:**
```python
import numpy as np
from scipy.optimize import linear_sum_assignment
rng = np.random.default_rng(1)
orders = rng.uniform(0, 5, (4, 2)); riders = rng.uniform(0, 5, (4, 2))   # km coordinates
cost = np.linalg.norm(orders[:, None] - riders[None], axis=2)            # pickup distance
r, c = linear_sum_assignment(cost)
greedy = 0; free = set(range(4))
for i in range(4):                                                        # greedy: nearest free rider
    j = min(free, key=lambda k: cost[i, k]); greedy += cost[i, j]; free.remove(j)
print("optimal total km:", round(cost[r, c].sum(), 2), "| greedy total km:", round(greedy, 2))
# optimal total km: 6.13 | greedy total km: 8.46
```

**Follow-ups:**
- *Prediction vs optimisation?* ML predicts costs; the optimiser decides. Errors in prep-time prediction flow straight into bad matches.
- *Cannot A/B per order, why?* Orders compete for the same riders, so treatments interfere; use switchback or geo-time randomisation.

**Common mistakes:** greedy nearest-rider, ignoring prep time, evaluating with a plain A/B on interfering units, no fairness or acceptance modelling.

### Q42 ⭐⭐ 🔴 Design a hierarchical demand-forecasting system for 100k+ SKU-store combinations with promotions and stock-outs.
**Asked at:** Walmart, Amazon, Zalando, Instamart
**Say this first (1 line):** Forecast at the levels where the signal is strong, correct for stock-outs and promotions in the data, use one global model across series with hierarchy-aware features, and reconcile forecasts so SKU, store and region totals agree.

**Then explain (framework):**
- **Requirements:** decisions are replenishment and allocation; horizon matters (daily for fresh, weekly for ambient); need quantiles (not only a mean) for safety stock.
- **Data issues:** stock-outs make sales understate demand ("censored demand"), so mark those days, impute demand or exclude them; promotions and price are known future features; many SKUs are intermittent (many zero days).
- **Model:** one global GBDT or neural model across all 100k+ series with features: lags, rolling means, calendar and festival flags, price, promo type, store attributes, category embeddings, plus hierarchy IDs. Predict quantiles (quantile loss) or use a distribution for intermittent items (Poisson / negative binomial or Croston-style baselines).
- **Hierarchy and reconciliation:** forecasts at SKU-store, store, region should add up; use bottom-up, top-down or MinT reconciliation. Sparse SKU-store series borrow strength from category and store-level patterns.
- **Evaluation:** rolling-origin backtest; WAPE or MASE, pinball loss for quantiles, bias, and service-level and waste metrics; baseline against seasonal naive.
- **Serving and monitoring:** daily batch; monitor bias by category, promo-lift error, new-SKU cold start.
- **Trade-offs:** one global model scales but may miss local quirks; fine-tune or add store-level features for big stores.

**Example (illustrative):** A store's sales for one SKU look flat because it was out of stock for 3 days. The model treats those days as censored and learns demand from the in-stock days, avoiding a self-reinforcing under-forecast.

**Code:** (simple top-down reconciliation to a store total)
```python
import numpy as np
bottom = np.array([[10., 5.], [20., 8.], [6., 4.]])   # 3 stores x 2 SKUs (illustrative)
top_store = np.array([14., 31., 9.])                  # store-level forecast
prop = bottom / bottom.sum(1, keepdims=True)
recon = prop * top_store[:, None]
print(recon.round(2), recon.sum(1))                   # sums now equal top_store
```

**Follow-ups:**
- *New SKUs?* Use attributes (category, price, brand) and similar-item history.
- *Promo effects?* Include promo features and lift estimates; check for cannibalisation of related items.

**Common mistakes:** training on censored sales as true demand, only point forecasts, one-size-fits-all metric (MAPE on zeros), ignoring reconciliation.

### Q43 ⭐ 🟡 Design a 'people you may know' / friend recommendation system.
**Asked at:** Meta-type, LinkedIn, ShareChat
**Say this first (1 line):** Generate candidates from the social graph (friends of friends, shared groups, contacts), rank them with a model predicting mutual acceptance, and apply safety and privacy filters, since this is a link-prediction problem with strong social structure.

**Then explain:**
- **Requirements:** goal is accepted connections that lead to lasting engagement, not just request sends; guardrails on spam, harassment and privacy.
- **Candidates:** friends-of-friends (ranked by number of mutual connections), shared school/workplace/groups, phone contacts (with consent), people who viewed your profile.
- **Features:** mutual friend count, graph proximity (Adamic-Adar), profile overlap, interaction history, geography, activity, and the candidate's own likelihood to accept.
- **Model:** GBDT ranker, or graph embeddings / GNN for candidate generation and features; label = request sent AND accepted (not only sent, since sending can be spammy).
- **Evaluation:** offline precision at K on accepted requests with time split; online: accepted connections, downstream engagement, plus reports and blocks as guardrails.
- **Scale:** two-hop expansion explodes for celebrities, so sample or cap neighbours; precompute daily.
- **Trade-offs:** privacy (do not reveal hidden relationships), popularity feedback loop favouring already-popular users, sensitive attribute leakage.

**Example (illustrative):** User A and B share 12 mutual connections and an employer. B has a high acceptance rate, so B ranks in A's top 5, labelled "12 mutual connections".

**Follow-ups:**
- *Celebrity problem?* Cap fan-out and penalise very high-degree candidates.
- *Privacy risk?* Suggestions can reveal sensitive connections; apply opt-outs and thresholds.

**Common mistakes:** label = request sent only, ignoring the receiving side's interest, no privacy review, fully ignoring graph scale.

### Q44 ⭐ 🟡 Design a search autocomplete / query suggestion system.
**Asked at:** Flipkart, Amazon, Google, Microsoft
**Say this first (1 line):** Precompute a ranked set of completions per prefix from query logs (popularity, recency, personalisation), serve them from a fast trie or index with strict latency, and measure success by keystrokes saved and downstream conversion.

**Then explain:**
- **Requirements:** latency under about 50-100 ms per keystroke, high availability, safe content (no offensive suggestions), multilingual and typo handling.
- **Candidate generation:** prefix match from a trie or n-gram index over historical queries; add fuzzy matching and spelling correction; for new queries use catalogue terms (product names, brands).
- **Ranking:** score = popularity (frequency with time decay), conversion rate of the query (queries that end in purchases), recency/trending, user history and context (category, location), then an optional ML re-ranker (LightGBM) with those features.
- **Data and labels:** logs of typed prefix, shown suggestions, clicked suggestion; label = click (position-bias corrected, Q49).
- **Filtering:** remove zero-result queries, offensive or sensitive terms, and near-duplicates.
- **Evaluation:** offline MRR / success@K on held-out prefixes; online: suggestion CTR, keystrokes saved, search conversion, null-result rate.
- **Serving:** cache hot prefixes at the edge; update index daily and refresh trending terms hourly.
- **Trade-offs:** personalisation versus cache hit rate; popularity bias drowns new products.

**Example (illustrative):** For prefix "iph", suggestions are "iphone 15", "iphone 15 case", "iphone charger", ranked by recent popularity and purchase rate; user history for Apple items moves "iphone 15 case" up.

**Follow-ups:**
- *Why not a generative model?* Possible, but latency, safety and cost are harder; most systems use retrieval and ranking, sometimes with a learned query model.
- *Typos?* Edit-distance candidates or phonetic and keyboard-aware correction.

**Common mistakes:** ranking by raw frequency only, no safety filter, ignoring latency, not accounting for position bias in click labels.

### Q45 ⭐ 🟡 How would you decide between one global model and per-country / per-segment models across markets?
**Asked at:** Booking, Zalando, Spotify, Amazon (Europe/global)
**Say this first (1 line):** Start with one global model with market as a feature, then split only where data shows real differences that the model cannot capture, weighing data volume, maintenance cost and regulatory needs.

**Then explain:**
- **Case for global:** more data per model, shared learning for small markets, one pipeline to maintain, easier cold start for new countries.
- **Case for local:** different behaviour (payment mix, seasonality, language), different regulation or data residency rules, different label definitions, very different data volumes.
- **Middle path:** global model with market embeddings or interaction features; global pretrain then fine-tune per market; or hierarchical / multi-task models; mixture of experts.
- **Decision test:** compare global vs local on each market's holdout; if the global model with market features is within a small margin on big markets and better on small markets, keep it global.
- **Evaluation:** per-market slices (not only the global average, which hides the minority), plus fairness across markets.
- **Operations:** per-market thresholds and calibration are cheap and often enough; separate models multiply monitoring, retraining and on-call cost.
- **Trade-offs:** global models can be dominated by large markets; local models overfit on small ones.

**Example (illustrative):** A ranking model across 12 countries: a single model with country features matches local models in the 4 big countries (within 0.2% NDCG) and beats them by 3% in the 8 small ones, so you keep one model with per-country calibration.

**Follow-ups:**
- *New market launch?* Start with the global model plus a handful of local features, collect data, then fine-tune.
- *Regulatory split?* If data cannot leave a region, train locally or use federated approaches.

**Common mistakes:** deciding before measuring, looking only at the global average metric, ignoring operational cost of many models.

### Q46 ⭐ 🟡 How do you design for privacy and data minimisation (DPDP Act, GDPR) in a personalisation system?
**Asked at:** Europe companies, banks, GCCs
**Say this first (1 line):** Collect only what you need, get clear consent, minimise and anonymise or pseudonymise data, limit retention, give users control, and design the system so personalisation still works with less data.

**Then explain:**
- **Principles:** purpose limitation (use data only for the stated purpose), data minimisation, storage limitation, consent and withdrawal, security, accountability (GDPR Art. 5; DPDP Act has similar notions of consent, purpose and erasure).
- **Design choices:** use coarse features (age band, city) over raw identifiers; pseudonymous IDs; separate PII from behavioural data with access control; retention windows and TTLs on logs and features.
- **Rights:** access, deletion and opt-out must be supported: a "forget this user" pipeline that deletes from raw data, feature stores and training sets (and a plan for retraining if their data affected the model).
- **Privacy-preserving ML:** on-device models, federated learning, differential privacy (noise in training or aggregates), aggregated or cohort-level signals, and contextual (non-personal) recommendations as a fallback.
- **Governance:** DPIA (data protection impact assessment) for high-risk processing, audit logs, vendor controls, and cross-border transfer rules.
- **Trade-offs:** less data may reduce accuracy; measure the personalisation lift against what each feature costs in privacy risk and drop features with low value.
- **Sensitive data:** do not infer sensitive attributes (health, religion) from behaviour.

**Example (illustrative):** A recommender uses 40 features. An ablation shows 12 raw-location and contact-derived features add under 0.3% lift; drop them and use city-level location, cutting risk at little cost.

**Follow-ups:**
- *Deleting a user from a trained model?* Delete from the data and retrain on schedule; machine unlearning is still hard in practice.
- *Is hashing an ID anonymisation?* No, it is pseudonymisation; it is still personal data.

**Common mistakes:** treating hashing as anonymisation, keeping logs forever, no deletion path through the feature store, collecting data "in case it is useful".

### Q47 ⭐ 🟡 AI-era: you are handed an AI-generated ML system design or architecture doc. What red flags do you look for in review?
**Asked at:** 2025-26 AI-assisted rounds, GCCs
**Say this first (1 line):** I would check that the design starts from the business decision and metric, that every claim is justified with numbers and trade-offs, and look for generic boilerplate, leakage, missing monitoring and impossible latency or cost assumptions.

**Then explain (red flags):**
- **Problem framing:** no clear decision, metric or baseline; jumps straight to a fancy model; no mention of when not to use ML.
- **Data and labels:** label definition vague; no label delay or selection bias; random split on time-dependent data; features that would not exist at prediction time (leakage).
- **Features and serving:** no mention of training-serving skew, point-in-time joins, or how online features are produced; unrealistic latency (a 500M-parameter model in a 20 ms budget on CPU).
- **Evaluation:** only accuracy or AUC on imbalanced data; no calibration, slices, or online test plan; no guardrails.
- **Operations:** no monitoring, retraining trigger, rollback, or cost estimate; no failure mode (fallback when the model or feature store is down).
- **Risk and compliance:** ignores privacy, fairness or explainability where it applies.
- **AI-generated tells:** buzzword stacks (Kafka, Flink, feature store, vector DB all in one for a small problem), no numbers, back-of-envelope estimates that do not add up, confident but invented library features, and no trade-offs discussed.
- **Action:** ask the author to justify each component with a requirement, check the arithmetic (QPS, storage), and run a small prototype to test the riskiest assumption.

**Example (illustrative):** A churn design states "use a deep model with real-time streaming" but the decision is a weekly retention email. Flag: batch is enough, simpler GBDT, and the label window is undefined.

**Follow-ups:**
- *How do you validate numbers an LLM wrote?* Recompute them yourself and trace each to an assumption.
- *Do you reject AI-written designs?* No; use them as a draft, then review with the same bar as any design.

**Common mistakes:** accepting plausible-sounding text without checking numbers, reviewing style instead of assumptions, not asking for failure modes.

### Q48 ⭐ 🔴 Design a system that handles delayed conversion feedback (ads / lending) when labels arrive days or weeks late.
**Asked at:** Amazon Ads, Flipkart Ads, fintech
**Say this first (1 line):** Do not treat unconverted recent clicks as negatives; model the delay explicitly, correct with a delay-aware loss or importance weights, and use early signals (like add-to-cart) as proxy labels, while retraining as the labels mature.

**Then explain:**
- **The problem:** a click from yesterday may convert next week, so training today labels it 0 and biases the model towards a lower conversion rate and towards old items.
- **Approaches:**
  1. *Wait window:* train only on events older than the maximum useful delay (simple but stale).
  2. *Delayed feedback model:* jointly model P(conversion) and the delay distribution (for example exponential or Weibull), so a not-yet-converted click gets a probability of "will still convert" (Chapelle's approach).
  3. *Fake negative calibration / importance weights:* treat all as negative at first, then correct with a weighted loss when positives arrive later (a "duplicate and correct" stream).
  4. *Proxy labels:* early actions (add-to-cart, application started) predict the final outcome and arrive quickly.
- **Evaluation:** backtest by "as-of" snapshots, evaluating on matured labels; compare predicted vs eventual conversion by click-age bucket.
- **Serving:** retrain frequently with updates, and keep calibration checks since the delay distribution drifts (sale days).
- **Trade-offs:** freshness versus label completeness; more complex training and risk of bad delay assumptions.

**Example (illustrative):** True conversion rate is 5%, but a naive training set on clicks aged 0-14 days sees only 3.84% as converted. Correcting with the delay distribution recovers 4.85%.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(4)
n = 100_000
conv = rng.random(n) < 0.05                    # true eventual converters
delay = rng.exponential(3, n)                  # days from click to conversion
age = rng.uniform(0, 14, n)                    # click age at training time
seen = conv & (delay <= age)
print("true:", round(conv.mean(), 4), "| naive:", round(seen.mean(), 4))
F = 1 - np.exp(-age / 3)                       # P(conversion already observed | converter)
print("delay-corrected:", round((seen / np.clip(F, 0.05, 1)).mean(), 4))
# true: 0.0498 | naive: 0.0384 | delay-corrected: 0.0485
```
(The exponential delay with a known mean is an assumption; in practice estimate it from data.)

**Follow-ups:**
- *Why not just wait 30 days?* Your model becomes a month stale; use waiting only for evaluation.
- *Credit risk equivalent?* Defaults take months, so use vintage analysis and early delinquency proxies.

**Common mistakes:** treating recent non-conversions as negatives, evaluating on immature labels, assuming a fixed delay distribution forever.

### Q49 ⭐ 🔴 How do you correct position bias and evaluate a ranker offline using logged data (counterfactual evaluation)?
**Asked at:** Flipkart, Amazon, Spotify, Booking
**Say this first (1 line):** Clicks depend on the position shown, not just relevance, so correct with propensity weights (inverse propensity scoring) or a click model, and evaluate new rankers offline with IPS/doubly-robust estimators on logs that include the logging probability, ideally with a small randomised slice.

**Then explain:**
- **Position bias:** users examine top results more; a mediocre item at rank 1 gets clicks that a great item at rank 8 does not. Training on raw clicks teaches "rank 1 is good".
- **Estimating bias:** randomisation experiments (swap positions in a small traffic slice), intervention harvesting from logs with different rankers, or an examination-propensity model learned jointly.
- **Learning to rank with bias correction:** weight each clicked example by 1 / P(examined at that position) (unbiased LTR), or use click models (position-based, cascade) and add position as a feature in training, then fix it at inference.
- **Counterfactual evaluation:** with logged actions, their propensities and rewards, estimate the new policy value: IPS = mean( w x reward ), w = P_new(a|x) / P_log(a|x). Self-normalised IPS (SNIPS) divides by sum of weights to reduce variance; doubly robust adds a reward model for lower variance.
- **Requirements and limits:** needs logged propensities and overlap (the new policy only takes actions the log could have taken); variance explodes with small propensities, so clip weights.
- **Alternatives:** interleaving for fast online comparison; A/B tests remain the final authority.

**Example (illustrative):** Simulated logs where the logging policy shows action 2 with probability 0.6. The true value of the new policy is 0.0312; IPS estimates 0.0306 and SNIPS 0.0306, while the logged-policy click rate (0.0363) would wrongly make the new policy look worse.

**Code:**
```python
import numpy as np
rng = np.random.default_rng(2)
n, K = 200_000, 5
x = rng.random(n)
true_p = np.stack([0.02 + 0.05 * x, 0.06 - 0.04 * x, np.full(n, 0.04),
                   np.full(n, 0.03), np.full(n, 0.01)], 1)
log_prob = np.array([0.1, 0.1, 0.6, 0.1, 0.1])         # logging policy favours action 2
a_log = rng.choice(K, size=n, p=log_prob)
click = rng.random(n) < true_p[np.arange(n), a_log]
a_new = np.where(x > 0.5, 1, 0)                         # candidate policy
w = (a_new == a_log) / log_prob[a_log]                  # importance weights
print("true", round(true_p[np.arange(n), a_new].mean(), 4),
      "| IPS", round((w * click).mean(), 4),
      "| SNIPS", round((w * click).sum() / w.sum(), 4),
      "| logged CTR", round(click.mean(), 4))
# true 0.0312 | IPS 0.0306 | SNIPS 0.0306 | logged CTR 0.0363
```

**Follow-ups:**
- *What if propensities were not logged?* Estimate them with a model (risky), or run a small randomised experiment first.
- *Why not trust offline estimates fully?* Variance, model misspecification and overlap issues; confirm with an A/B.

**Common mistakes:** training on raw clicks, ignoring overlap, no weight clipping, comparing rankers on logged clicks of the old ranker.

### Q50 ⭐ 🔴 Design a multi-objective ranking system balancing engagement, revenue, creator fairness and integrity.
**Asked at:** Meta-type, Spotify, ShareChat, senior roles
**Say this first (1 line):** Predict several outcomes per item (engagement, revenue, integrity risk, creator exposure), combine them in a transparent weighted utility with hard constraints for integrity and fairness, and tune the weights through experiments tied to long-term metrics.

**Then explain (framework):**
- **Requirements:** define objectives and who owns each: engagement (user value), revenue (business), creator fairness (supply health), integrity (policy and safety). Integrity is a constraint more than a weight.
- **Models:** multi-task model predicting P(like), P(share), P(long watch), P(report), P(ad conversion), integrity classifier scores, creator-level features. Predict short-term signals but also use long-term proxies (return next week).
- **Combination:** final score = sum of w_i x p_i (value model), minus penalties for integrity risk; items above a policy-risk threshold are removed or demoted regardless of engagement.
- **Fairness and exposure:** reserve exposure for new and small creators (explore slots), cap over-exposure of a single creator, and monitor Gini of exposure across creators.
- **Weight tuning:** run experiments across weights, find the Pareto frontier, and choose with leadership trade-offs; use surveys for "meaningful" value because engagement alone rewards clickbait.
- **Evaluation:** online A/B with a metric tree: primary (long-term retention or satisfaction), secondary (revenue, creator retention), guardrails (reports, harmful-content views).
- **Monitoring:** objective drift, adversarial gaming, creator behaviour changes, feedback loops.
- **Trade-offs:** any weighting is a policy choice; it should be documented and reviewed, not hidden in code.

**Example (illustrative):** Score = 1.0 x P(watch) + 0.5 x P(share) + 0.2 x revenue - 5 x risk. A viral borderline post with high engagement and risk 0.4 is demoted below a safe, moderately engaging video.

**Follow-ups:**
- *How do you pick weights?* Experiments plus explicit policy; for example maximise engagement subject to integrity and exposure constraints (constrained optimisation).
- *What if the metrics conflict?* Surface the trade-off with data; a decision-maker chooses, and you keep guardrails.

**Common mistakes:** engagement only, weights buried in code with no review, treating integrity as a soft weight, measuring only short-term A/B effects.

### Q51 ⭐ 🔴 Design a fairness and bias audit process for a credit-scoring model.
**Asked at:** Banks/GCCs, Klarna, Europe fintech
**Say this first (1 line):** Audit across the model lifecycle: check the data and labels, measure outcomes by group with agreed fairness metrics, look for proxies, test mitigations, document the trade-offs, and repeat the audit on a schedule.

**Then explain (process):**
- **Scope and law:** list legally protected or sensitive groups in each jurisdiction and what you can lawfully collect; if attributes are not collected, use careful proxy-based estimation or testing with consent, and document limits.
- **Data audit:** representation of groups, label bias (rejected applicants have no repayment label, a selection bias; past human decisions may carry bias), and proxies (pin code, device, name-derived features).
- **Metrics by group:** approval rate (demographic parity gap, or the "four-fifths" ratio as a screening heuristic), true positive rate (equal opportunity), false positive rate, calibration by group, and score distribution. These can conflict mathematically; pick with legal and business input.
- **Root cause:** feature ablations, SHAP by group, and counterfactual tests (change a sensitive attribute or proxy and see whether the decision shifts).
- **Mitigation:** remove or constrain proxies, reweigh data, group-aware thresholds only if legally allowed, constrained optimisation, or alternative data; re-measure the accuracy cost.
- **Governance:** model card, sign-off by risk and compliance, adverse action explanations, monitoring dashboards, and periodic re-audit (quarterly).
- **Trade-offs:** fairness constraints may reduce AUC a little; leave the human appeal path open.

**Example (illustrative):** Approval is 62% for group A and 48% for group B at the same default rate. Ablation shows a pin-code feature drives most of the gap; replacing it with income stability features narrows the gap to 5 points with AUC dropping by 0.004.

**Follow-ups:**
- *Why not drop the protected attribute and be done?* Proxies still encode it; you need the attribute (or an estimate) to measure disparity.
- *Which metric to choose?* Depends on harm: for credit, equal opportunity and calibration are common starting points, decided with compliance.

**Common mistakes:** "fairness through unawareness", one metric only, auditing once and never again, ignoring selection bias in rejected applicants.

### Q52 ⭐ 🔴 Design an inventory replenishment system for dark stores combining forecasting and optimisation.
**Asked at:** Swiggy Instamart, Zepto, Walmart, Amazon
**Say this first (1 line):** Forecast demand as a distribution for each item and dark store over the replenishment lead time, then choose order quantities with an optimisation that trades off lost sales against waste and holding cost under capacity and shelf-life limits.

**Then explain (framework):**
- **Requirements:** goals are availability (fill rate) and low waste, with constraints: shelf life, storage capacity, supplier minimum order quantities, delivery cycles. Decisions run daily or per delivery slot.
- **Forecasting:** probabilistic demand (quantiles) at SKU x store, from a global model with promo, weather, festival and local features; correct for stock-out censoring; forecast over the lead time plus review period.
- **Optimisation:** for each item, the newsvendor idea: order up to the quantile at critical ratio = underage cost / (underage + overage cost). Then solve the multi-item problem under shared constraints (space, budget, truck capacity) with LP / MIP or a greedy marginal-value heuristic.
- **Perishables:** include age profile of stock; waste cost rises with expiry; markdowns can be an action.
- **Evaluation:** simulation over historical demand comparing policies on fill rate, waste, lost sales, and holding cost; then pilot on selected stores.
- **Serving and monitoring:** daily batch with fallbacks (min-max rules) if the forecast fails; track forecast bias, service level, waste, supplier delays.
- **Trade-offs:** higher service level costs more waste; forecasting error feeds directly into stock decisions, so quantile calibration is critical.

**Example (illustrative):** A milk SKU has mean demand 40 and std 12 units until next delivery. Margin per sold unit is Rs 30, wasted unit loses Rs 70, so critical ratio = 30 / (30 + 70) = 0.3, and the order-up-to level is the 30th percentile of demand, about 33.7 units, less than the mean because waste is expensive.

**Code:**
```python
from scipy.stats import norm
mu, sigma = 40, 12                     # illustrative demand forecast
cu, co = 30, 70                        # underage (lost margin), overage (waste) cost per unit
crit = cu / (cu + co)
print(round(crit, 3), round(norm.ppf(crit, mu, sigma), 1))   # 0.3 33.7
```

**Follow-ups:**
- *Why not just use the mean forecast?* The cost of too much and too little differs; the best order is a quantile, not the mean.
- *Multiple items sharing space?* Allocate by marginal profit per unit of space until capacity is used (or solve an LP).

**Common mistakes:** point forecasts only, ignoring stock-out censoring, symmetric cost assumption, no capacity constraints, no simulation before rollout.
