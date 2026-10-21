=== Q27
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

=== Q28
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

=== Q29
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

=== Q30
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

=== Q31
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

=== Q32
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

=== Q33
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

=== Q34
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

=== Q35
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

=== Q36
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

=== Q37
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

=== Q38
**Say this first (1 line):** Use inherently interpretable or well-explained models, document everything (data, features, validation, decisions), test for bias, keep humans accountable for decisions, and map each regulation to concrete controls.

**Then explain:**
- **Explainability:** a scorecard-style logistic regression or a GBDT with monotonic constraints plus SHAP for per-decision reason codes; global explanations for model governance.
- **Regulations (summary, check current text):**
  - *India (RBI):* expects model risk management, board-approved policies, fair-practice and transparency in digital lending, and fairness to borrowers; data localisation and consent apply (DPDP Act).
  - *GDPR (Europe):* rules on automated decisions, with the right to meaningful information about the logic and to human review of solely automated decisions.
  - *EU AI Act:* credit scoring is a high-risk use case; expects risk management, data governance, documentation, logging, human oversight, accuracy and robustness.
- **Controls:** model cards and documentation, independent validation, reason codes for adverse decisions, audit logs of inputs and versions, human override, periodic fairness and performance review, and a change-management process.
- **Data controls:** purpose limitation, data minimisation, no prohibited attributes, and a check for proxies.
- **Trade-offs:** an interpretable model may lose a little accuracy; a complex model needs more governance. In regulated credit, a simpler model that you can defend often wins.

**Example (illustrative):** A loan is declined. The notice shows the top three reasons from SHAP: "high utilisation on existing credit", "short credit history", "recent missed payment". The customer can request human review.

**Follow-ups:**
- *Is SHAP enough?* It explains the model, not causality, and can be unstable with correlated features, so pair with monotonic constraints and stability tests.
- *Who is accountable?* The business owner and model risk function, not the algorithm.

**Common mistakes:** claiming SHAP equals causal explanation, using proxy features for protected attributes, no audit trail, treating compliance as a final-stage task.

=== Q39
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

=== Q40
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

=== Q41
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

=== Q42
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

=== Q43
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

=== Q44
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

=== Q45
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

=== Q46
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

=== Q47
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

=== Q48
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

=== Q49
**Say this first (1 line):** Clicks depend on the position shown, not just relevance, so correct with propensity weights (inverse propensity scoring) or a click model, and evaluate new rankers offline with IPS/doubly-robust estimators on logs that include the logging probability, ideally with a small randomised slice.

**Then explain:**
- **Position bias:** users examine top results more; a mediocre item at rank 1 gets clicks that a great item at rank 8 does not. Training on raw clicks teaches "rank 1 is good".
- **Estimating bias:** randomisation experiments (swap positions in a small traffic slice), intervention harvesting from logs with different rankers, or an examination-propensity model learned jointly.
- **Learning to rank with bias correction:** weight each clicked example by 1 / P(examined at that position) (unbiased LTR), or use click models (position-based, cascade) and add position as a feature in training, then fix it at inference.
- **Counterfactual evaluation:** with logged actions, their propensities and rewards, estimate the new policy value: IPS = mean( w x reward ), w = P_new(a|x) / P_log(a|x). Self-normalised IPS (SNIPS) divides by sum of weights to reduce variance; doubly robust adds a reward model for lower variance.
- **Requirements and limits:** needs logged propensities and overlap (the new policy only takes actions the log could have taken); variance explodes with small propensities, so clip weights.
- **Alternatives:** interleaving for fast online comparison; A/B tests remain the final authority.

**Example (illustrative):** Simulated logs where the logging policy shows action 2 with probability 0.6. The true value of the new policy is 0.0312; IPS estimates 0.0307 and SNIPS 0.0306, while the logged-policy click rate (0.0363) would wrongly make the new policy look worse.

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
# true 0.0312 | IPS 0.0307 | SNIPS 0.0306 | logged CTR 0.0363
```

**Follow-ups:**
- *What if propensities were not logged?* Estimate them with a model (risky), or run a small randomised experiment first.
- *Why not trust offline estimates fully?* Variance, model misspecification and overlap issues; confirm with an A/B.

**Common mistakes:** training on raw clicks, ignoring overlap, no weight clipping, comparing rankers on logged clicks of the old ranker.

=== Q50
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

=== Q51
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

=== Q52
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
