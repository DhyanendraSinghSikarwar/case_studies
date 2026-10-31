**Say this first (1 line):** Scoring all 300 ads is 15,000,000 predictions a second (300 servers at full load), a 40-ad prefilter makes it 2,000,000 a second (40 servers, about 58 with 30% headroom), so I would design retrieval, prefilter, calibrated click model and auction as four stages and judge the prefilter by recall of the ads the full model would have picked.

**Clarifying questions:**
- Is the 50,000 requests per second the fleet peak, and is the 80 ms the whole ad path (retrieval, scoring, auction, response)? It sets how many milliseconds the click model really gets.
- Which auction (first or second price) and which objective (clicks, conversions, revenue)? Calibration matters most when bids are multiplied by predicted rates.
- Is "50,000 predictions per second per server at full load" measured with the production model and batch size, at the 99th percentile latency? A throughput figure without a latency figure is not a capacity number.
- Are there advertiser budgets, pacing and brand-safety rules that run before or after scoring? They shrink the candidate list and add latency.
- Is click or conversion delay long? It decides how fresh labels can be and how often to retrain.

**Approach:**
1. Clarify and frame. Goal: maximise value (advertiser outcomes and platform revenue) inside 80 ms. Say the stages: targeting leaves 300, prefilter keeps 40, click model scores 40, auction picks winners.
2. Metrics and guardrails. Online: revenue per thousand requests, advertiser return, click rate. Model: log loss and calibration ratio (predicted clicks / observed clicks), because the auction multiplies the prediction by a bid. Guardrails: p99 latency, timeout rate, advertiser spend pacing, user complaints and ad load.
3. Data and labels. Log every impression with features and the auction context. Clicks are plentiful; conversions arrive late. Down-sample non-clicks to cut cost and correct the probabilities afterwards (see the code).
4. Baseline first. Start with a logistic regression on hashed features and a simple prefilter (a cheap score from historic click rate of the ad and the context). It ships in weeks and gives the benchmark.
5. Model and trade-offs. Gradient-boosted trees or a small neural net for the click model; keep the prefilter far cheaper than the model. Cost per request: 300 scored = 300 servers, 40 scored = 40 servers (plus the prefilter, which I must size too). The price of the prefilter is lost recall, so measure it. Calibrate with Platt or isotonic scaling on recent traffic.
6. Evaluation. Offline: log loss, calibration by bucket, prefilter recall of the full model's top few ads. Then shadow scoring, then a small randomised traffic test against the baseline with advertiser-side checks.
7. Launch and experiment plan. 1% to 5% to 25% of traffic, gated on latency and spend pacing; keep a random exploration slice so future models see ads they would not pick.
8. Monitoring, retraining and risks. Daily calibration ratio by bucket, feature freshness, timeout rate; retrain on a schedule agreed with how fast the ad market moves; fall back to the baseline if the model times out.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 5, 4, 12, 6, 5, 5.

**Metrics:**
- Predictions per second = requests per second x ads scored per request: 50,000 x 300 = 15,000,000, versus 50,000 x 40 = 2,000,000.
- Servers = predictions per second / predictions per server per second: 300 versus 40 at full load; add headroom as a separate decision.
- Calibration ratio = sum of predicted click probabilities / observed clicks, per bucket; aim for about 1.00.
- Prefilter recall = share of the ads that the full model would have put in the top few that survive the prefilter.
- Guardrails: p99 latency, timeout share, spend pacing, ad load per user.

**Risks:**
- Capacity: "full load" leaves no room for spikes, retries or a model rollback; plan headroom.
- Prefilter bias: ads the prefilter never lets through never get data (feedback loop); keep an exploration slice.
- Miscalibration after down-sampling or a model change silently overbids or underbids in the auction.
- Latency tail: 40 predictions per request inside 80 ms is tight if features come from many stores.
- Privacy and policy rules for targeting: ask compliance and legal what signals may be used; I make no claim about what is allowed.

**What the interviewer scores:**
- Strong: gets 15,000,000 and 2,000,000 a second and 300 versus 40 servers, and then adds headroom and the prefilter's own cost.
- Strong: treats calibration as essential for an auction, and knows the down-sampling correction.
- Strong: judges the prefilter by recall against the full model and keeps an exploration slice.
- Weak: "just scale the servers" or "use deep learning" with no stage budget, calibration or fallback.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "I would train a deep model on all ads and autoscale the servers until it is fast enough."
- Strong: "At 50,000 requests a second, scoring 300 ads is 15 million predictions a second, which is 300 servers at full load. A 40-ad prefilter cuts that to 2 million, so 40 servers, and about 58 with 30% headroom. The trade is recall, so I would measure how many of the full model's top ads the prefilter keeps, calibrate the click model because the auction multiplies by it, and ramp from 1% traffic with latency and spend-pacing guardrails."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- How would you lower cost further? Cache scores for repeated (user segment, ad) pairs for a short time, quantise the model, or tier the model (a small model for all 40, a larger one for the top 5); each trades some accuracy or freshness.
- What if the prefilter recall is only 70%? Raise the kept count (the cost scales linearly: 60 ads is 3,000,000 a second, 60 servers at full load), or train the prefilter to imitate the full model's ranking.
- How do you handle delayed conversions? Train on clicks as a fast proxy, add conversions with a maturity correction, and watch the calibration ratio on mature cohorts.

**Common mistakes:**
- Quoting servers without saying "at full load" or adding headroom.
- Forgetting that the prefilter has its own compute and latency cost.
- Skipping calibration, then multiplying uncalibrated scores by bids.
- Forgetting to correct probabilities after down-sampling non-clicks.
