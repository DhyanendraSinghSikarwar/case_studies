### Q11 ⭐⭐⭐ 🟡 Ad ranking: An ad server must rank ads on 50,000 requests per second at peak inside an 80 ms budget, and targeting leaves 300 candidate ads per request. A prefilter keeps 40 of them for the click model, and one scoring server runs 50,000 click predictions per second at full load. Design the ad ranking and auction system including calibration, and compute the predictions per second and servers needed with and without the prefilter.
**Asked at:** Moderation and ads design material (a TryExponent Reddit ML engineer guide reporting an ad targeting or ad ranking design prompt, PracHub question banks with a short-video content-moderation prompt, an Interview Query Xandr guide); prep-site material; notification ranking had no clear page; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
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
```python
import math
import numpy as np

# Sizing (from the question; peak figures are the question's, 'full load' means no headroom)
rps, cands, kept, per_server = 50_000, 300, 40, 50_000
no_pre = rps * cands
with_pre = rps * kept
assert no_pre == 15_000_000 and with_pre == 2_000_000
s_no, s_pre = math.ceil(no_pre / per_server), math.ceil(with_pre / per_server)
assert (s_no, s_pre) == (300, 40)
# With 30% headroom (my assumption) the fleet is larger; the prefilter itself costs extra
s_pre_hr = math.ceil(with_pre / (per_server * 0.70))
assert s_pre_hr == 58
print("predictions/s without prefilter:", no_pre, "servers:", s_no)
print("predictions/s with prefilter   :", with_pre, "servers:", s_pre, "| with 30% headroom:", s_pre_hr)
print("reduction factor:", no_pre / with_pre)

# Calibration: negatives down-sampled at keep rate w shifts predictions up; undo with p = p'w/(1-p'+p'w)
rng = np.random.default_rng(11)
n = 2_000_000
true_p = rng.beta(1, 49, n)                      # mean CTR about 2%
click = rng.random(n) < true_p
w = 0.1
keep = click | (rng.random(n) < w)               # keep all clicks, 10% of non-clicks
p_shift = true_p / (true_p + (1 - true_p) * w)   # what a perfect model fits on the sampled data
p_fix = p_shift * w / (1 - p_shift + p_shift * w)
assert np.allclose(p_fix, true_p)
print("mean true CTR:", round(float(true_p.mean()), 4),
      "| mean pred on sampled data:", round(float(p_shift[keep].mean()), 4),
      "| after correction:", round(float(p_fix.mean()), 4))
assert p_shift.mean() > 2 * true_p.mean()

# Prefilter recall: cheap score correlated with true value; keep top 40 of 300; how many of the true top 5 survive?
trials, hit = 2000, 0
for _ in range(trials):
    v = rng.normal(size=300)
    cheap = 0.7 * v + math.sqrt(1 - 0.49) * rng.normal(size=300)
    top5 = set(np.argsort(-v)[:5]); kept40 = set(np.argsort(-cheap)[:40])
    hit += len(top5 & kept40)
recall = hit / (trials * 5)
print("share of true top-5 ads kept by a 0.7-correlation prefilter (illustrative):", round(recall, 3))
assert 0.6 < recall < 0.95
```

**Output (my run):**
```
predictions/s without prefilter: 15000000 servers: 300
predictions/s with prefilter   : 2000000 servers: 40 | with 30% headroom: 58
reduction factor: 7.5
mean true CTR: 0.02 | mean pred on sampled data: 0.1695 | after correction: 0.02
share of true top-5 ads kept by a 0.7-correlation prefilter (illustrative): 0.782
```

**Follow-ups:**
- How would you lower cost further? Cache scores for repeated (user segment, ad) pairs for a short time, quantise the model, or tier the model (a small model for all 40, a larger one for the top 5); each trades some accuracy or freshness.
- What if the prefilter recall is only 70%? Raise the kept count (the cost scales linearly: 60 ads is 3,000,000 a second, 60 servers at full load), or train the prefilter to imitate the full model's ranking.
- How do you handle delayed conversions? Train on clicks as a fast proxy, add conversions with a maturity correction, and watch the calibration ratio on mature cohorts.

**Common mistakes:**
- Quoting servers without saying "at full load" or adding headroom.
- Forgetting that the prefilter has its own compute and latency cost.
- Skipping calibration, then multiplying uncalibrated scores by bids.
- Forgetting to correct probabilities after down-sampling non-clicks.

### Q12 ⭐⭐⭐ 🔴 Fraud with delayed labels: A card-not-present fraud model must be retrained monthly and launched in 12 weeks, but chargebacks arrive late: 60% of eventual chargebacks are in by day 30 and 90% by day 90 (a measured profile). True fraud is a steady 0.2% of transactions (a projection). Design the training, evaluation and monitoring plan, and compute the fraud rate that a 30-day-old window and a 90-day-old window appear to have.
**Asked at:** Fraud-detection design material (an Educative fraud-detection mock interview, a PracHub real-time payment fraud prompt with a 50 ms budget and prep guides that call fraud the prompt where probabilities, thresholds and feature freshness must be discussed); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** A 30-day-old window shows 0.12% fraud (60% of the true 0.2%) and a 90-day-old window shows 0.18% (90%), so I would never read recent label rates as truth: I would correct for maturity, train on the freshest window that is mostly matured, and use early proxy signals plus rules to cover the gap.

**Clarifying questions:**
- Is the 60% and 90% profile stable across merchants, countries and attack types? A single maturity curve is the whole basis of any correction.
- Besides chargebacks, are there faster labels (customer disputes, issuer confirmations, manual reviews)? They let me react before day 30.
- What do we do on a flagged transaction (block, step-up check, review)? Blocked fraud never produces a chargeback, so labels are censored by our own decisions.
- Is the 0.2% a measured rate or a planning figure? The question calls it a projection; I would treat it as an assumption to be checked on mature cohorts.
- What are the loss per missed fraud and the cost per false decline? They fix the threshold and the value of waiting for labels.

**Approach:**
1. Clarify and frame. State the problem: labels lag by months, the world changes weekly. Goal is a monthly retrained model, launched in 12 weeks (84 days, which is less than the 90 days needed for mostly matured labels).
2. Metrics and guardrails. Model: precision-recall at the review capacity, recall at a fixed false-decline rate, calibration. Business: fraud loss per 10,000 transactions, false-decline rate. Guardrails: review queue size, approval rate, latency.
3. Data and labels. Build a maturity table by label age. Use matured rows (about 90 days old) for the main training and evaluation; use younger rows only with a maturity correction or with fast proxy labels (disputes, confirmed review outcomes). Keep a small random "no-block" or low-friction audit slice to learn about blocked traffic, if the risk owner agrees.
4. Baseline first. Rules plus a simple model on matured data; this is what ships in week 12. Compare any complex model against it.
5. Model and trade-offs. Gradient-boosted trees on transaction, device and history features. The trade-off is freshness versus label quality: a 90-day lag keeps labels clean but the model is about 105 days behind on average between retrains (see the code); mitigate with fast-moving features, rules for new attacks and a recency-weighted loss.
6. Evaluation. Offline: out-of-time split on matured data (train on older months, test on a later matured month), never random split. Online: shadow mode first, then a small traffic slice with a champion-challenger comparison on maturity-corrected loss.
7. Launch and experiment plan. Shadow weeks 8 to 10, 5% to 25% traffic weeks 11 to 12. Decision at each stage on corrected fraud caught and false declines, not on raw label rates.
8. Monitoring, retraining and risks. Monitor score drift, feature drift, approval rate and early-label rates by age cohort; report fraud rate only per maturity cohort. Retrain monthly, and trigger an earlier retrain on an attack spike.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 8, 4, 8, 7, 5, 5.

**Metrics:**
- Apparent fraud rate at age a = chargebacks observed by age a / transactions = true rate x maturity(a): 0.2% x 0.60 = 0.12%; 0.2% x 0.90 = 0.18%.
- Maturity-corrected rate = apparent rate / maturity(a), which returns 0.2% from either window if the profile holds.
- Recall at fixed false-decline rate, precision at review capacity, expected loss per 10,000 transactions.
- Guardrails: approval rate, review queue length, p99 scoring latency, share of fraud caught by rules only.

**Risks:**
- Reading the last 30 days' 0.12% as a drop in fraud and relaxing controls.
- Training on young rows with a "not yet fraud" label for transactions that will become chargebacks (label noise that teaches the model to approve).
- Censoring: our own blocks hide fraud, so labels come mostly from approved traffic.
- The maturity profile can shift (new issuers, new attack types), so a fixed correction factor can mislead.
- Any claim about rules for chargebacks, dispute windows or customer data: ask compliance and legal.

**What the interviewer scores:**
- Strong: 0.12% and 0.18% against a true 0.2%, and the correction by dividing by maturity.
- Strong: out-of-time evaluation, fast proxy labels, and a plan for the first 12 weeks.
- Strong: names censoring from blocking and a stable-profile assumption.
- Weak: random train-test split on immature labels, or treating the recent low rate as good news.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "Fraud was only 0.12% last month, so the new model works and we can reduce reviews."
- Strong: "A 30-day-old window can only show 60% of the true 0.2%, which is 0.12%, and a 90-day-old window shows 0.18%. So I would divide by the maturity share before comparing, train on rows at least 90 days old, use disputes as an early signal, and judge the launch in shadow mode on maturity-corrected loss, with rules covering the newest attack patterns."

**Code:**
```python
import math

# Prompt arithmetic: true fraud rate 0.2% (assumption), chargeback maturity 60% at day 30, 90% at day 90
true_rate = 0.002
mat = {30: 0.60, 90: 0.90}
apparent = {d: true_rate * m for d, m in mat.items()}
assert abs(apparent[30] - 0.0012) < 1e-12 and abs(apparent[90] - 0.0018) < 1e-12
for d in (30, 90):
    print(f"window aged {d} days: apparent fraud rate {apparent[d]:.4%} (true {true_rate:.2%}), understated by {1 - mat[d]:.0%}")

# Maturity correction: divide the observed rate by the maturity share (valid only if the delay profile is stable)
for d in (30, 90):
    assert abs(apparent[d] / mat[d] - true_rate) < 1e-12
print("corrected estimate from either window:", apparent[30] / mat[30])

# Label-lag trade-off for monthly retraining: freshest data with at least 90% matured labels is 90 days old
lag_days, retrain_days = 90, 30
print("training rows end", lag_days, "days before today; model is", lag_days + retrain_days // 2,
      "days behind on average between retrains")
assert lag_days + retrain_days // 2 == 105

# How many transactions to see enough frauds? Poisson relative error of a count c is about 1/sqrt(c)
target_frauds = 400                                # relative standard error 5%, about +-10% at 95%
assert abs(1 / math.sqrt(target_frauds) - 0.05) < 1e-12
tx_90 = target_frauds / apparent[90]               # transactions in a 90-day-old window
tx_30 = target_frauds / apparent[30]
print("transactions needed for 400 observed frauds: 90-day-old window", round(tx_90), "| 30-day-old window", round(tx_30))
assert round(tx_90) == 222_222 and round(tx_30) == 333_333
# The 12-week launch fits: 12 weeks = 84 days < 90 days, so the first model cannot use fully matured labels from its own traffic
assert 12 * 7 == 84 < 90
```

**Output (my run):**
```
window aged 30 days: apparent fraud rate 0.1200% (true 0.20%), understated by 40%
window aged 90 days: apparent fraud rate 0.1800% (true 0.20%), understated by 10%
corrected estimate from either window: 0.002
training rows end 90 days before today; model is 105 days behind on average between retrains
transactions needed for 400 observed frauds: 90-day-old window 222222 | 30-day-old window 333333
```

**Follow-ups:**
- What if the maturity curve changes? Re-estimate it every month on cohorts old enough to be nearly complete, and report the correction with a range rather than one number.
- Can you learn from blocked transactions? Only with a deliberately small unblocked audit slice, approved by the risk owner, or with methods that adjust for selection; otherwise label bias remains.
- How would you cut the 90-day wait? Use faster signals (disputes, confirmed review outcomes) as an early label with its own calibration to final chargebacks.

**Common mistakes:**
- Calling the apparent rate "the fraud rate" without the age of the window.
- Random splits that leak future patterns into training.
- Using one correction factor for all merchants and countries.
- Forgetting that blocked fraud never becomes a chargeback.

### Q13 ⭐⭐⭐ 🔴 Agentic workflow: A retailer wants an agent to resolve refund requests end to end for 20,000 requests a day. A typical run makes 4 sequential LLM steps of 1.5 seconds each and 3 sequential tool calls of 0.4 seconds each (assume no retries), and the chat budget is 12 seconds at the 95th percentile. Design the agent, its approval rules for refunds above 2,000 rupees and its evaluation, and compute the typical latency and the slack left under the budget.
**Asked at:** Agentic and GenAI design material (Dataford agentic AI engineer guides listing multi-step customer-service workflows, techinterview.org and aiforanything.io pages on AI agent infrastructure and system design, and a post-LLM-era ML engineer interview guide saying 'design an LLM-based system for X' is now the most common prompt); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The typical run is 4 x 1.5 + 3 x 0.4 = 7.2 seconds, leaving 4.8 seconds under 12, but 7.2 is a typical figure and the budget is a 95th-percentile one, so I would measure the tail (retries and slow tools push it up) and design the agent as a bounded workflow with a human approval path outside the chat clock.

**Clarifying questions:**
- Which refunds can the agent finish alone, and what does a wrong refund cost? That fixes the autonomy level and the approval rule above 2,000 rupees.
- Are the 1.5 and 0.4 second figures means, medians or 95th percentiles? The slack of 4.8 seconds is only valid for typical runs.
- Can any of the 3 tool calls run in parallel (order lookup, payment status, policy check)? Parallel calls cut the 1.2 seconds of tool time.
- What happens after the agent's answer: does a human approval make the customer wait, or is the customer told "we will confirm"? Approval waits do not fit a 12-second chat budget.
- What fraud and abuse patterns exist for refunds (repeat claimants, new accounts)? The agent must not be the only control.

**Approach:**
1. Clarify and frame. Goal: resolve refund requests safely and quickly. Define the outcome classes: refund approved, refused with reason, handed to a human.
2. Metrics and guardrails. Correct-resolution rate against a human-reviewed standard, wrong-refund rate (the guardrail), handoff rate, time to answer (p95), cost per resolved request, customer satisfaction.
3. Data and labels. Collect past refund tickets with the final human decision and the policy version. Build a golden set of cases, including tricky ones (partial refunds, expired windows, abuse patterns), reviewed by a policy owner.
4. Baseline first. A rules-and-forms flow: look up the order, check policy, return a decision or hand off. Add the language model only for understanding the request and writing the reply.
5. Model and trade-offs. Keep the LLM out of the decision where a rule can decide: the model extracts the request, tools fetch facts, a policy engine decides, the model drafts. Typical latency 7.2 seconds as given; to cut it, run independent tool calls in parallel, use a smaller model for the easy steps, and stream the first message. Refunds above 2,000 rupees go to a human approval queue; the customer is told it is pending.
6. Evaluation. Offline replay on the golden set (decision accuracy, wrong-refund rate, tool-call correctness). Then shadow mode (agent proposes, human decides) before any live action. A clean test run of 299 independent cases with no wrong refund bounds the error rate under 1% at 95% confidence (see the code).
7. Launch and experiment plan. Shadow, then agent-assisted (human clicks approve), then autonomous only under 2,000 rupees on a small traffic share, with a kill switch. Ramp only if the wrong-refund guardrail holds.
8. Monitoring, retraining and risks. Log every step and tool call; sample audits weekly; alert on handoff rate, wrong-refund rate and p95 latency; re-run the golden set whenever the prompt, model or policy changes.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 5, 5, 11, 6, 5, 5.

**Metrics:**
- Typical latency = sum of sequential step times = 4 x 1.5 + 3 x 0.4 = 7.2 s; slack = 12 - 7.2 = 4.8 s (a typical figure, not a p95 figure).
- p95 end-to-end latency = 95th percentile of total time across requests, measured from logs, including retries.
- Wrong-refund rate = refunds that policy owners judge wrong / refunds issued by the agent. Guardrail with a hard ceiling set by the business.
- Handoff rate = requests passed to a human / all requests; correct-resolution rate = correct final outcomes / all requests.
- Cost per resolved request = model plus tool cost / resolved requests.

**Risks:**
- Treating mean latency as the 95th percentile: in my illustrative simulation the p95 was higher than 7.2 seconds (see output), and retries make it worse.
- Prompt injection or customer text that tries to talk the agent into a refund; the policy engine, not the model, must authorise money.
- Wrong refunds are expensive and hard to undo; autonomy limits and audits are the control.
- Tool failures and partial actions (refund issued, reply failed) need idempotent calls and clear state.
- Customer data in prompts and logs, and any legal rules on refunds: ask compliance and legal.

**What the interviewer scores:**
- Strong: 7.2 seconds and 4.8 seconds slack, then says that is typical, not p95, and tests the tail.
- Strong: a bounded workflow with a policy engine, approval above 2,000 rupees, shadow mode and a kill switch.
- Strong: evaluation by golden set, wrong-refund rate and a sample-size argument.
- Weak: "give the LLM the tools and let it decide", with no limits, approvals or tail latency.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "It takes 7.2 seconds against a 12 second budget, so latency is fine."
- Strong: "7.2 seconds is the typical sequential path, so 4.8 seconds of slack, but the budget is a 95th percentile. I would measure the tail from logs, and in a simple simulation with variable step times and some retries the p95 moves up toward the budget. So I would parallelise the tool calls, keep the money decision in a policy engine, send refunds over 2,000 rupees to a human with a 'pending' message, and run shadow mode first."

**Code:**
```python
import math
import numpy as np

# Prompt arithmetic: typical (mean) path latency, sequential
llm_steps, llm_s, tool_calls, tool_s, budget = 4, 1.5, 3, 0.4, 12.0
typical = llm_steps * llm_s + tool_calls * tool_s
slack = budget - typical
assert abs(typical - 7.2) < 1e-9 and abs(slack - 4.8) < 1e-9
print("typical latency (s):", typical, "| slack to 12 s budget (s):", round(slack, 1))

# The budget is for the 95th percentile, not the typical run. Illustrative simulation:
# each step is lognormal with the stated mean and a coefficient of variation of 0.4 (my assumption).
rng = np.random.default_rng(13)
def lognormal_with_mean(mean, cv, size):
    s2 = math.log(1 + cv ** 2)
    return rng.lognormal(math.log(mean) - s2 / 2, math.sqrt(s2), size)
N = 200_000
total = sum(lognormal_with_mean(llm_s, 0.4, N) for _ in range(llm_steps)) \
      + sum(lognormal_with_mean(tool_s, 0.4, N) for _ in range(tool_calls))
p95 = float(np.percentile(total, 95))
print("simulated mean:", round(float(total.mean()), 2), "| simulated p95:", round(p95, 2))
assert abs(total.mean() - 7.2) < 0.05 and p95 > typical
print("p95 within 12 s budget in this simulation:", p95 < budget)
# With one retry on each LLM step with 10% probability, the tail grows (assumed retry rate)
retry = rng.random((llm_steps, N)) < 0.10
extra = sum(retry[i] * lognormal_with_mean(llm_s, 0.4, N) for i in range(llm_steps))
p95_retry = float(np.percentile(total + extra, 95))
print("p95 with 10% retry per LLM step:", round(p95_retry, 2))
assert p95_retry > p95

# Load: 20,000 requests a day is small; Little's law for average concurrency (even spread, a simplification)
rate = 20_000 / 86_400
conc = rate * typical
print("average requests/s:", round(rate, 3), "| average concurrent runs:", round(conc, 2))
assert round(rate, 3) == 0.231 and round(conc, 2) == 1.67

# Evaluation budget: if a staged test shows 0 wrong refunds in n independent runs, the 95% upper bound on the error rate is about 3/n
n_zero = math.ceil(math.log(0.05) / math.log(1 - 0.01))
print("clean runs needed to bound wrong-refund rate below 1% at 95%:", n_zero)
assert n_zero == 299 and (1 - 0.01) ** n_zero <= 0.05 < (1 - 0.01) ** (n_zero - 1)
```

**Output (my run):**
```
typical latency (s): 7.2 | slack to 12 s budget (s): 4.8
simulated mean: 7.2 | simulated p95: 9.41
p95 within 12 s budget in this simulation: True
p95 with 10% retry per LLM step: 10.67
average requests/s: 0.231 | average concurrent runs: 1.67
clean runs needed to bound wrong-refund rate below 1% at 95%: 299
```

**Follow-ups:**
- What if the p95 is over 12 seconds? Cut sequential steps (parallel tools, smaller model for routing, cached policy), stream a first reply, or move slow cases to an asynchronous "we will email you" path.
- How do you choose the approval threshold? Start from the cost of a wrong refund and the audit results; 2,000 rupees is the question's rule, and I would lower or raise it with the business based on the wrong-refund rate in shadow mode.
- How do you evaluate multi-step runs? Score the final outcome and each tool call (right tool, right arguments), since a right answer can come from a wrong action.

**Common mistakes:**
- Comparing a mean latency with a percentile budget.
- Letting the model decide money movement with no deterministic policy check.
- Skipping shadow mode and launching autonomous.
- Forgetting idempotency when a refund call is retried.

### Q14 ⭐⭐⭐ 🔴 Multilingual voice assistant: A bank's voice bot takes 100,000 calls a day, 60% of them inside an 8-hour window (assume evenly spread), and a call lasts 3 minutes on average. One streaming speech-and-language server holds 25 concurrent calls, and the budget per spoken reply is 1.5 seconds. Design the assistant for Hindi, Tamil and mixed-language callers, and use Little's law to compute concurrent calls in the window and the servers needed.
**Asked at:** Indian-market material (a Let's Data Science / NPCI item on AI for UPI fraud and multilingual voice, an Elastic and Sarvam multilingual voice-agent blog, a SquadStack voice-bot page on noise and accents, Razorpay, Delhivery and Shiprocket pages on cash-on-delivery return-to-origin risk scoring, a Blinkit candidate report of a delivery-time debugging case); vendor and blog material, no confirmed interview round for these exact designs; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Little's law gives 60,000 calls over 8 hours = 2.08 calls a second x 180 seconds = 375 concurrent calls, which is 15 servers at full load, but I would plan about 18 to 22 because arrivals are random and the evenly-spread assumption hides a real peak.

**Clarifying questions:**
- Which tasks must the bot do (balance, card block, loan enquiry) and which must go to a human? Scope decides how risky an error is.
- How is the language mix: Hindi, Tamil, and mixed-language (code-switched) speech such as Hinglish? I need recorded test calls from each group, not just text.
- Is the 3-minute mean call length stable, and what share of calls end in a handoff? A longer or heavier tail raises concurrency (L = arrival rate x duration).
- What audio quality arrives (mobile, noisy, speaker phone)? Speech recognition errors dominate bad calls.
- Which identity or payment actions are allowed by voice? Ask compliance and legal what must be verified and recorded; I will not assume rules.

**Approach:**
1. Clarify and frame. Goal: resolve the top intents by voice with low friction and a safe handoff. Define "contained" (resolved without a human) and "safe" (no wrong action).
2. Metrics and guardrails. Containment, task success, word error rate by language, reply latency (the 1.5-second budget), handoff rate, repeat-call rate within 24 hours, customer satisfaction. Guardrails: wrong-action rate, authentication failures, abandon rate.
3. Data and labels. Collect consented, de-identified call audio with human transcripts per language, including code-mixed speech and noisy lines. Label intents and outcomes. Budget transcription by language, not in total, so minority languages are not starved.
4. Baseline first. A menu-style flow with a general speech-recognition model and an intent classifier for the top 5 intents; measure word error rate per language on a held-out set.
5. Model and trade-offs. Streaming speech recognition, an intent or dialogue model (a small model first, a larger language model only where needed), then streaming speech synthesis. Capacity by Little's law: 375 concurrent calls, 15 servers at 25 calls each at full load, 18 at the 99.9th percentile of random fluctuation, 22 with 30% headroom (see the code). Split the 1.5 seconds across recognition, understanding and synthesis.
6. Evaluation. Offline: word error rate and intent accuracy per language and per noise level; scripted test calls for sensitive intents. Online: a small share of live calls with easy handoff to a human, comparing containment and satisfaction against the human-only path.
7. Launch and experiment plan. Pilot one language and 2 intents on 5% of the window, then add languages when the per-language metrics clear a bar agreed with operations. Load-test to the planned concurrency before each ramp.
8. Monitoring, retraining and risks. Daily word error rate and latency by language; sampled call review; retrain recognition on corrected transcripts; alert on handoff and abandon spikes; fall back to a human line when servers saturate.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 6, 4, 11, 6, 5, 5.

**Metrics:**
- Concurrent calls L = arrival rate x mean duration = (60,000 / 28,800 s) x 180 s = 375.
- Servers = ceil(concurrent calls / calls per server): 15 at full load for the mean; more for the tail and for headroom.
- Word error rate per language = (substitutions + deletions + insertions) / words in the reference transcript.
- Containment = calls resolved without a human / all calls; wrong-action rate = wrong actions / actions taken.
- p95 reply latency = 95th percentile time from the caller finishing speaking to the first audio of the reply.

**Risks:**
- Little's law gives an average. Random fluctuation and uneven arrivals (a busy hour, salary day, an outage that triggers calls) push real concurrency above 375.
- Minority-language and mixed-language callers get worse recognition, so an overall average hides unfair service; always report per language.
- Voice cloning and fraud: a voice is a weak identity proof; ask compliance and security what verification is required.
- Recording and storing calls: consent, retention and privacy rules are for compliance and legal to confirm.
- A bot that traps callers in loops; always offer a human.

**What the interviewer scores:**
- Strong: 375 concurrent calls and 15 servers, then says that is the mean and adds headroom for variance and peaks.
- Strong: per-language evaluation, a latency split across the speech pipeline, and an easy human handoff.
- Strong: a staged rollout by language and intent, with load tests.
- Weak: one overall accuracy number, no per-language data, no capacity margin.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "I would use a large speech model that supports Indian languages, and 15 servers will do."
- Strong: "60,000 calls in 8 hours is about 2.1 calls a second, and a 3-minute call makes that 375 concurrent calls, so 15 servers only at full load. With random arrivals I would plan 18, and 22 with 30% headroom. I would measure word error rate separately for Hindi, Tamil and code-mixed callers on noisy lines, pilot one language on 5% of calls, and always keep a path to a human."

**Code:**
```python
import math

# Prompt arithmetic: Little's law L = lambda * W
calls_day, share_window, window_h, call_s, per_server = 100_000, 0.60, 8, 180, 25
calls_window = calls_day * share_window
lam = calls_window / (window_h * 3600)
L = lam * call_s
assert calls_window == 60_000 and abs(lam - 2.0833333) < 1e-6 and round(L) == 375
servers_flat = math.ceil(L / per_server)
assert servers_flat == 15
print("calls in window:", int(calls_window), "| arrival rate/s:", round(lam, 3), "| mean concurrent calls:", round(L, 1))
print("servers at 100% load (mean concurrency):", servers_flat)

# Off-window traffic for comparison
lam_off = calls_day * (1 - share_window) / (16 * 3600)
print("off-window mean concurrent calls:", round(lam_off * call_s, 1))
assert round(lam_off * call_s) == 125

# Random fluctuation: concurrency of Poisson arrivals is Poisson(L) (M/G/infinity); find the 99.9th percentile exactly
def poisson_ppf(q, mu):
    p = math.exp(-mu); c = p; k = 0
    while c < q:
        k += 1; p *= mu / k; c += p
    return k
k999 = poisson_ppf(0.999, L)
s999 = math.ceil(k999 / per_server)
s_hr = math.ceil(L / (per_server * 0.70))
print("99.9th percentile concurrent calls:", k999, "-> servers:", s999, "| servers at 70% target utilisation:", s_hr)
assert 420 < k999 < 450 and s999 == 18 and s_hr == 22

# Sensitivity to the 'evenly spread' assumption: if the busiest hour carries 1.5x the window average (assumed)
peak_L = L * 1.5
print("if busiest hour is 1.5x average: concurrent", round(peak_L), "-> servers", math.ceil(peak_L / per_server))
assert math.ceil(peak_L / per_server) == 23

# Latency: one conversational turn budget of 1.5 s, split (illustrative)
split = {"speech recognition": 0.5, "language understanding + answer": 0.6, "speech synthesis first audio": 0.3, "network + overhead": 0.1}
assert abs(sum(split.values()) - 1.5) < 1e-9
print("illustrative split of 1.5 s:", split)

# Follow-up check: 4-minute calls
L4 = round(lam * 240, 6)
assert round(L4) == 500 and math.ceil(L4 / per_server) == 20
print("4-minute calls: concurrent", round(L4), "servers", math.ceil(L4 / per_server))
```

**Output (my run):**
```
calls in window: 60000 | arrival rate/s: 2.083 | mean concurrent calls: 375.0
servers at 100% load (mean concurrency): 15
off-window mean concurrent calls: 125.0
99.9th percentile concurrent calls: 436 -> servers: 18 | servers at 70% target utilisation: 22
if busiest hour is 1.5x average: concurrent 562 -> servers 23
illustrative split of 1.5 s: {'speech recognition': 0.5, 'language understanding + answer': 0.6, 'speech synthesis first audio': 0.3, 'network + overhead': 0.1}
4-minute calls: concurrent 500 servers 20
```

**Follow-ups:**
- What if calls get longer after launch? Concurrency scales with duration: 4-minute calls give 500 concurrent calls and 20 servers at full load, so watch mean call length as a capacity metric.
- How would you handle code-mixed speech? Collect and transcribe code-mixed audio, evaluate on it explicitly, and consider language-identification per utterance before routing.
- How do you control cost? Route simple intents to a small model, cap call length, and measure cost per contained call against the human-handled cost.

**Common mistakes:**
- Using calls per day divided by 24 hours when 60% fall in an 8-hour window.
- Forgetting that Little's law needs the arrival rate in the same time unit as the duration.
- Sizing at 100% utilisation with no headroom.
- Reporting a single overall word error rate.

### Q15 ⭐⭐ 🟢 Resume and job matching: A job portal has 2,000,000 resumes and 150,000 live jobs, and recruiters want 200 shortlisted resumes per job within 300 ms. Resumes are stored as 768-dimension vectors of 4-byte floats. Design the matching system, and compute the raw vector storage in decimal gigabytes and the size if each value is quantised to 1 byte, then say what you would ask compliance about fairness.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to resume and job matching (public material is mostly patents and generic recommender guides); search snippets only, not opened
**Say this first (1 line):** Resume vectors are 2,000,000 x 768 x 4 bytes = 6.144 GB (decimal), or 1.536 GB at 1 byte per value, which fits one machine's memory, so the hard parts are label quality, ranking beyond similarity and fairness, not storage.

**Clarifying questions:**
- What is a good match: a recruiter shortlisting, an interview, or a hire? Different signals, different delays, and the target decides the label.
- Who sees the shortlist and does a human always decide? Automated rejection raises the stakes; I would design for decision support.
- How fresh must it be (new resume or new job appears in minutes)? It decides between a nightly batch and an online index.
- Which attributes may be used or must be excluded? Ask compliance and legal about fairness and protected-attribute rules; I will not state what is required.
- Are resumes multilingual or in mixed formats? Parsing and language coverage affect recall for some candidates.

**Approach:**
1. Clarify and frame. Goal: for each job, 200 good candidates in under 300 ms, with no hidden unfairness. Two stages: retrieve candidates by embedding similarity plus hard filters (location, skills, experience range), then re-rank.
2. Metrics and guardrails. Recall at 200 against recruiter-confirmed good candidates, ranking quality (NDCG at 10), recruiter time to shortlist, interview rate. Guardrails: selection rates by group (reviewed with compliance), latency p95, share of resumes ever shown.
3. Data and labels. Labels are noisy: recruiter clicks, shortlists, interviews. They reflect which candidates recruiters were shown (exposure bias) and past preferences (bias). Use graded labels (viewed, shortlisted, interviewed) and keep a random exploration slice if the product owner agrees.
4. Baseline first. Keyword and filter search (BM25-style) plus rules. Measure recall at 200 against labelled jobs; any embedding model must beat it.
5. Model and trade-offs. Embeddings (768 dimensions) for retrieval, a re-ranker with structured features. Storage: 6.144 GB in float32, 1.536 GB in int8 (see the code); the int8 shortlist overlapped the float32 shortlist well in a small synthetic test, but re-check on real data. Compute: 1,536,000,000 multiply-adds per brute-force query, which is why an approximate nearest-neighbour index or precomputing per job matters. Trade-off: recall versus latency versus memory.
6. Evaluation. Offline on held-out jobs with recruiter-confirmed matches; slice by seniority, language, city and group (as agreed with compliance); check for proxy features. Online: interleaving or an A/B test on recruiter time to shortlist and interview rate.
7. Launch and experiment plan. Shadow results shown beside the existing search, then 10% of recruiters, then wider. Gate on latency and the fairness review.
8. Monitoring, retraining and risks. Monitor index freshness, recall on a fixed set, selection rates, complaints. Retrain embeddings when the label distribution changes; document how candidates can correct their data.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 5, 6, 4, 10, 6, 5, 5.

**Metrics:**
- Raw storage = vectors x dimensions x bytes per value: 2,000,000 x 768 x 4 = 6,144,000,000 bytes = 6.144 GB (decimal); at 1 byte, 1.536 GB.
- Recall at 200 = recruiter-confirmed matches inside the shortlist / all confirmed matches for that job.
- NDCG at 10 = discounted gain of the top 10 divided by the best possible; recruiter time to shortlist.
- Selection-rate ratio between groups = selection rate of group A / selection rate of group B, reviewed with compliance (a monitoring signal, not a legal test).
- Guardrails: p95 latency under 300 ms, index age, complaint rate.

**Risks:**
- Learning past bias: if past hires favoured one group, labels teach the model to repeat it. Ask compliance and legal what testing and documentation are required.
- Proxy features (name, college, postcode, gaps) leaking sensitive attributes.
- Exposure bias: candidates never shown never get labels.
- Over-compressed vectors dropping rare skills; test recall per segment.
- Candidates gaming keywords; fake or duplicate resumes.

**What the interviewer scores:**
- Strong: 6.144 GB and 1.536 GB, then says storage is not the bottleneck and moves to labels and ranking.
- Strong: two-stage retrieve-and-rerank with a keyword baseline.
- Strong: fairness as design and monitoring, with compliance asked about the rules, not asserted.
- Weak: "embed everything and take the nearest 200", with no labels, bias or evaluation.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "I would use a big language model to score every resume against every job."
- Strong: "The vectors are 6.144 GB in float32 and 1.536 GB in 1-byte form, so they fit in memory. Brute force is about 1.5 billion multiply-adds a query, so I would use an approximate index with hard filters to get a few thousand candidates, then re-rank 200. I would measure recall against recruiter-confirmed matches, compare with a keyword baseline, check selection rates by group with compliance, and keep a human making every decision."

**Code:**
```python
import numpy as np

# Prompt arithmetic: raw vector storage, decimal GB (1 GB = 1e9 bytes)
resumes, jobs, dim = 2_000_000, 150_000, 768
f32 = resumes * dim * 4
i8 = resumes * dim * 1
assert f32 == 6_144_000_000 and i8 == 1_536_000_000
print("float32 resumes GB:", f32 / 1e9, "| int8 GB:", i8 / 1e9, "| ratio:", f32 / i8)
job_f32 = jobs * dim * 4
assert job_f32 == 460_800_000
print("job vectors float32 GB:", job_f32 / 1e9)

# Brute-force cost per job query: dot products against every resume
macs_per_query = resumes * dim
assert macs_per_query == 1_536_000_000
all_jobs_macs = macs_per_query * jobs
print("multiply-adds per query:", macs_per_query, "| for all jobs (nightly batch):", f"{all_jobs_macs:.3e}")
assert all_jobs_macs == 1_536_000_000 * 150_000

# Does int8 quantisation keep the shortlist? Small test: 20,000 synthetic unit vectors, 768 dims, top-200 overlap
rng = np.random.default_rng(15)
n, d, k = 20_000, 768, 200
base = rng.normal(size=(n, d)).astype(np.float32)
base += 0.6 * rng.normal(size=(1, d)).astype(np.float32)          # shared direction, so scores are not all near zero
base /= np.linalg.norm(base, axis=1, keepdims=True)
scale = np.abs(base).max()
q8 = np.round(base / scale * 127).astype(np.int8)
deq = q8.astype(np.float32) * (scale / 127)
overlaps = []
for _ in range(50):
    q = base[rng.integers(n)] + 0.3 * rng.normal(size=d).astype(np.float32)
    q /= np.linalg.norm(q)
    exact = set(np.argpartition(-(base @ q), k)[:k])
    approx = set(np.argpartition(-(deq @ q), k)[:k])
    overlaps.append(len(exact & approx) / k)
ov = float(np.mean(overlaps))
print("top-200 overlap, int8 vs float32 (synthetic, illustrative):", round(ov, 3))
assert ov > 0.9
assert q8.nbytes * 4 == base.nbytes
print("bytes ratio in the test:", base.nbytes / q8.nbytes)
```

**Output (my run):**
```
float32 resumes GB: 6.144 | int8 GB: 1.536 | ratio: 4.0
job vectors float32 GB: 0.4608
multiply-adds per query: 1536000000 | for all jobs (nightly batch): 2.304e+14
top-200 overlap, int8 vs float32 (synthetic, illustrative): 0.984
bytes ratio in the test: 4.0
```

**Follow-ups:**
- Would you store job vectors too? Yes, 150,000 x 768 x 4 = 0.4608 GB, and precomputing the shortlist per job nightly can cover most traffic; new jobs use an online query.
- How do you cope with sparse labels? Use weaker signals (views, saves) with lower weight, and use recruiter feedback on shown results to refresh the re-ranker.
- How do you test fairness with no sensitive attributes in the data? Ask compliance and legal what may be collected for testing and how; do not infer protected attributes without their guidance.

**Common mistakes:**
- Quoting megabytes or gigabytes without saying decimal versus binary.
- Treating click or shortlist labels as ground truth.
- Putting fairness only at the end, or stating legal rules as facts.
- Ignoring hard filters and going straight to nearest neighbours.

### Q16 ⭐⭐ 🟢 Document processing: A firm gets 50,000 scanned invoices a day, averaging 2.2 pages, in mixed Hindi and English, and wants straight-through processing for 85% of them. OCR takes 0.8 seconds per page on one core, the batch must finish inside a 6-hour window, and you plan 50% core utilisation. Design the extraction pipeline, and compute the cores needed and, if the other 15% need 90 seconds of human review each at 7 productive hours per person per day, the reviewers needed.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to invoice and document extraction with OCR (no page found in these searches); search snippets only, not opened
**Say this first (1 line):** OCR load is 110,000 pages x 0.8 s = 88,000 core-seconds, which at 50% utilisation over 6 hours needs 9 cores, and if only 85% go straight through, the other 7,500 invoices need 187.5 review hours, so 27 reviewers; the real design question is which fields are trusted without a person.

**Clarifying questions:**
- Which fields matter (invoice number, date, amount, tax identifier, line items) and what does a wrong amount cost? Error cost sets the confidence thresholds.
- Is the 85% straight-through target a goal or a measured rate? It is a goal; the reviewer count depends directly on it.
- What are the layouts and image quality (phone photos, scans, handwriting, Hindi and English mixed)? Quality drives recognition errors.
- Is there a purchase order or vendor master to validate against? Cross-checks catch errors OCR cannot.
- What is the arrival pattern: all at once, or spread through the day? A 6-hour batch window needs all files to have arrived.

**Approach:**
1. Clarify and frame. Goal: turn scans into validated records with 85% going straight through and the rest reviewed quickly. Define "straight through": all required fields above confidence and passing validation, with no human touch.
2. Metrics and guardrails. Field-level accuracy, invoice-level exact match, straight-through rate, review time per invoice, cost per invoice. Guardrail: wrong amount posted automatically (the costly error), and turnaround time.
3. Data and labels. Sample invoices across vendors, languages and quality; have people key the fields once (a gold set), and keep reviewer corrections as ongoing labels. Plan the labelling budget per layout family so rare vendors are covered.
4. Baseline first. Existing OCR plus regular expressions and vendor templates for the top vendors; measure field accuracy on the gold set.
5. Model and trade-offs. OCR (0.8 s a page on one core), then a layout-aware extractor for fields, then validation (totals add up, tax maths, date format, vendor match, duplicate check). Capacity: 88,000 core-seconds, 9 cores at 50% utilisation (see the code), plus the reviewer load. Trade-off: a higher confidence threshold cuts errors but lowers the straight-through rate and raises reviewer count.
6. Evaluation. Offline field accuracy and invoice-level exact match by vendor and language; calibration of confidence scores. Online: shadow mode where people key as usual and the system is compared, then partial automation on low-value invoices.
7. Launch and experiment plan. Start with the top vendors and lower-value invoices, expand by layout family; ramp straight-through share as audits stay clean.
8. Monitoring, retraining and risks. Weekly audit of a random sample of auto-posted invoices (598 clean audits bound the error rate below 0.5% at 95%, see the code), drift alerts on confidence scores and new layouts, retrain on reviewer corrections.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 6, 4, 11, 6, 5, 5.

**Metrics:**
- Pages = invoices x pages per invoice = 50,000 x 2.2 = 110,000; core-seconds = pages x 0.8 = 88,000.
- Cores = ceil(core-seconds / (window seconds x utilisation)) = ceil(88,000 / 10,800) = ceil(8.15) = 9.
- Straight-through rate = invoices posted with no human touch / all invoices.
- Reviewers = ceil(invoices to review x seconds per review / 3,600 / productive hours per person) = ceil(7,500 x 90 / 3,600 / 7) = ceil(26.8) = 27.
- Field accuracy = fields correct / fields; guardrail: auto-posted wrong-amount rate.

**Risks:**
- Silent errors (a misread digit in an amount) in auto-posted invoices; validation rules and audits are the control.
- The 85% target may not hold on poor scans or new vendors; the reviewer count moves by about 1.8 people per point.
- Mixed Hindi and English text and stamps reduce recognition; test per language.
- Peaks: a 6-hour window with uneven arrivals needs more than the average capacity.
- Personal and financial data in documents; ask compliance and legal about retention and access.

**What the interviewer scores:**
- Strong: 110,000 pages, 88,000 core-seconds, 9 cores, 187.5 review hours, 27 people, with the OCR applied to every page.
- Strong: confidence thresholds, validation rules and audit sampling for auto-posted records.
- Strong: sees the trade-off between straight-through rate and reviewer cost.
- Weak: "use a good OCR model", with no validation, no human loop and no capacity maths.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "OCR plus a language model reads the invoices and we are done."
- Strong: "50,000 invoices at 2.2 pages is 110,000 pages, so 88,000 core-seconds. At 50% utilisation over 6 hours, a core gives 10,800 seconds, so 9 cores. If 15% need review, that is 7,500 invoices, 187.5 hours, 27 reviewers. Each point of straight-through rate moves the team by about two people, so I would set the confidence threshold by the cost of a wrong amount, validate totals and vendors, and audit a random sample of auto-posted invoices every week."

**Code:**
```python
import math

# OCR sizing. OCR runs on every page, whether or not the invoice later goes straight through.
invoices, pages_per, ocr_s, window_h, util = 50_000, 2.2, 0.8, 6, 0.50
pages = invoices * pages_per
core_s = pages * ocr_s
usable_per_core = window_h * 3600 * util
assert round(pages) == 110_000 and round(core_s) == 88_000 and usable_per_core == 10_800
cores = math.ceil(core_s / usable_per_core)
assert cores == 9
print("pages:", round(pages), "| core-seconds:", round(core_s), "| usable seconds per core:", usable_per_core,
      "| cores (exact):", round(core_s / usable_per_core, 2), "-> cores:", cores)

# Human review of the non-straight-through share
stp, review_s, hours_per_person = 0.85, 90, 7
manual = round(invoices * (1 - stp))
review_hours = manual * review_s / 3600
people = math.ceil(review_hours / hours_per_person)
assert round(manual) == 7_500 and review_hours == 187.5 and people == 27
print("invoices to review:", round(manual), "| review hours:", review_hours, "| reviewers (exact):",
      round(review_hours / hours_per_person, 2), "-> reviewers:", people)

# Sensitivity: each 1 point of straight-through rate changes review load by 500 invoices = 12.5 hours = 1.8 people
per_point = round(invoices * 0.01)
assert per_point == 500 and per_point * review_s / 3600 == 12.5
print("1 point of straight-through rate = invoices:", per_point, "= hours:", per_point * review_s / 3600,
      "= people:", round(per_point * review_s / 3600 / hours_per_person, 2))
for r in (0.75, 0.80, 0.85, 0.90):
    n = math.ceil(invoices * (1 - r) * review_s / 3600 / hours_per_person)
    print(f"straight-through {r:.0%} -> reviewers {n}")
assert math.ceil(invoices * 0.25 * 90 / 3600 / 7) == 45 and math.ceil(invoices * 0.10 * 90 / 3600 / 7) == 18

# Sample size to check the straight-through error rate: 0 errors in n audited gives 95% upper bound about 3/n
n_audit = math.ceil(math.log(0.05) / math.log(1 - 0.005))
print("clean audited invoices to bound field-level error under 0.5% at 95%:", n_audit)
assert n_audit == 598
```

**Output (my run):**
```
pages: 110000 | core-seconds: 88000 | usable seconds per core: 10800.0 | cores (exact): 8.15 -> cores: 9
invoices to review: 7500 | review hours: 187.5 | reviewers (exact): 26.79 -> reviewers: 27
1 point of straight-through rate = invoices: 500 = hours: 12.5 = people: 1.79
straight-through 75% -> reviewers 45
straight-through 80% -> reviewers 36
straight-through 85% -> reviewers 27
straight-through 90% -> reviewers 18
clean audited invoices to bound field-level error under 0.5% at 95%: 598
```

**Follow-ups:**
- What if straight-through is only 75%? Reviewers rise to 45; consider better templates for top vendors, a second-pass model for low-confidence fields only, or a longer SLA.
- Could you skip OCR for digital invoices? Yes, if some arrive as text PDFs or structured files; that is a cheap win and cuts the core count.
- How do you set the confidence threshold? From the cost of a wrong auto-posted amount versus the cost of a review, using calibrated scores on the gold set.

**Common mistakes:**
- Computing OCR cores only for the straight-through 85%.
- Ignoring utilisation (running cores at 100%).
- Counting reviewers in people without productive hours.
- Treating the 85% target as a measured rate.

### Q17 ⭐⭐ 🟢 Dynamic pricing: A cab app reprices each of its 100 zones every 60 seconds and wants a rule that never changes a price by more than 20% of the previous price in one update. The base fare is 100 rupees. Design the pricing system and its guardrails, and compute the number of price decisions a day and the highest fare reachable after 5 consecutive 20% increases, and say how that informs an absolute cap.
**Asked at:** ETA, forecasting and pricing design material (a CleverPrep Lyft ML engineer page listing real-time pricing, city-level demand forecasting with cold start and ETA-with-traffic prompts, an AlgoMaster ETA design page, Codemia demand-forecasting pipeline prompts and an AI Engineering Insider dynamic-pricing piece); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 100 zones x 1,440 minutes = 144,000 price decisions a day, and five +20% steps take 100 rupees to 248.83, so a per-update cap limits speed but not level; I would add an absolute cap, a rate limit over longer windows and a human override, and confirm with the business and legal what price limits apply.

**Clarifying questions:**
- What is the objective: revenue, trips completed, driver supply balance? A price that clears the market is not always the profit-maximising one.
- Who may see and complain about prices, and are there fare limits we must respect? Ask compliance and legal; I do not assume the rules.
- Is demand data per zone available in near real time, and how noisy is it? Noisy inputs make prices jump.
- Do drivers see the same multiplier? Supply response matters for balance.
- Can we run randomised tests by zone or by time? It decides how we measure effect.

**Approach:**
1. Clarify and frame. Goal: balance supply and demand per zone every minute without price shocks. Pricing is a control problem: forecast, price, observe, adjust.
2. Metrics and guardrails. Completed trips per request, ride-request fill rate, driver utilisation, revenue per hour, wait time. Guardrails: price complaint rate, share of time at the cap, price volatility (steps over 10% in a row), cancellation rate.
3. Data and labels. Logged requests, available drivers, prices shown, accept and cancel outcomes, per zone and minute. Prices were set by past rules, so demand response is only learned in the range of prices tried (limited price variation); add randomised small price nudges if allowed.
4. Baseline first. A rule on the ratio of requests to available drivers in each zone, smoothed over a few minutes, with the 20% step cap. Measure fill rate and revenue against it.
5. Model and trade-offs. Demand forecast per zone and a price-response (elasticity) estimate. Optimise a price in a range, then apply guardrails: the +-20% step cap (limits speed), an absolute cap (limits level; 5 steps give 248.83, 4 steps already pass 2x base at 207.36, see the code), smoothing across neighbouring zones to avoid cliffs, and a manual kill switch.
6. Evaluation. Offline: forecast error by zone and hour, replay of logged data with the guardrails. Online: zone-level or time-slice randomisation (switchback) because riders and drivers interact across zones, which breaks simple user-level tests.
7. Launch and experiment plan. Start in a few zones, keep a share of zones on the old rule, ramp when fill rate and revenue improve without more complaints.
8. Monitoring, retraining and risks. Alerts on price volatility, time at the cap, forecast bias per zone; retrain the forecast frequently; review festival and weather events manually.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 5, 5, 4, 10, 7, 5, 5.

**Metrics:**
- Price decisions a day = zones x decisions per zone per day = 100 x 1,440 = 144,000.
- Maximum price after n capped increases = base x 1.2^n: 100 x 1.2^5 = 248.832 rupees.
- Fill rate = requests matched to a driver / requests; revenue per hour per zone.
- Steps to a multiple m of base = ceil(ln m / ln 1.2): 4 steps for 2x, 7 steps for 3x.
- Guardrails: share of time at the absolute cap, complaint rate, cancellation rate.

**Risks:**
- A per-update cap does not stop a gradual climb: 2x base is reached in 4 minutes at a 60-second interval.
- Feedback loops: higher prices reduce demand, which lowers the signal that justified the price.
- Interference across zones makes simple A/B tests biased; use switchback or zone-level designs.
- Fairness and public trust (surge during emergencies); agree policy with the business, and ask compliance and legal about limits.
- Elasticity learned from narrow past price ranges may not hold outside it.

**What the interviewer scores:**
- Strong: 144,000 decisions and 248.83, and notes that a step cap is not a level cap.
- Strong: rule-based baseline, forecast plus elasticity, guardrails, switchback testing.
- Strong: raises fairness and legal limits as questions for the right team.
- Weak: "reinforcement learning to maximise revenue" with no guardrails, baseline or test design.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "The model sets the price each minute and the 20% rule keeps it safe."
- Strong: "That is 144,000 decisions a day. A 20% step cap sounds safe, but five steps take 100 to 248.83 and four already pass 2x, so I would add an absolute cap chosen with the business and check with legal what limits apply. I would start with a smoothed demand-to-supply rule, test against it with a switchback design by zone and time, and watch complaint rate and time at the cap."

**Code:**
```python
import math

# Prompt arithmetic
zones, interval_s, base, cap_step = 100, 60, 100.0, 0.20
decisions = zones * (24 * 3600 // interval_s)
assert decisions == 144_000
print("price decisions a day:", decisions)
price5 = base * (1 + cap_step) ** 5
assert abs(price5 - 248.832) < 1e-9
print("fare after 5 consecutive +20% steps:", round(price5, 3), "| multiple of base:", round(price5 / base, 3))
# The per-update cap limits speed, not level: how long to reach 2x or 3x base?
for mult in (2, 3):
    steps = math.ceil(math.log(mult) / math.log(1 + cap_step))
    print(f"steps to reach at least {mult}x base: {steps} (= {steps} minutes at a 60 s interval); price after: {base * 1.2 ** steps:.2f}")
assert math.ceil(math.log(2) / math.log(1.2)) == 4 and abs(100 * 1.2 ** 4 - 207.36) < 1e-9
assert math.ceil(math.log(3) / math.log(1.2)) == 7
# Step down is not the mirror: -20% three times from 207.36
down = 207.36 * 0.8 ** 3
print("207.36 after three -20% steps:", round(down, 2))
assert abs(down - 106.16832) < 1e-6

# Guardrail check on a noisy raw price proposal: smoothing plus clip to +-20% and absolute cap
import numpy as np
rng = np.random.default_rng(17)
raw = base * np.exp(np.cumsum(rng.normal(0.08, 0.15, 30)))        # volatile model proposals (illustrative)
cap_abs = 2.0 * base                                                # illustrative absolute cap (business decision)
p, path = base, []
for r in raw:
    step = min(max(r, p * (1 - cap_step)), p * (1 + cap_step))
    p = min(step, cap_abs)
    path.append(p)
path = np.array(path)
ratios = path[1:] / path[:-1]
assert ratios.max() <= 1.2 + 1e-9 and ratios.min() >= 0.8 - 1e-9 and path.max() <= cap_abs + 1e-9
print("max one-step change:", round(float(ratios.max()), 3), "| max price:", round(float(path.max()), 2), "| minutes at cap:", int((path >= cap_abs - 1e-9).sum()))
```

**Output (my run):**
```
price decisions a day: 144000
fare after 5 consecutive +20% steps: 248.832 | multiple of base: 2.488
steps to reach at least 2x base: 4 (= 4 minutes at a 60 s interval); price after: 207.36
steps to reach at least 3x base: 7 (= 7 minutes at a 60 s interval); price after: 358.32
207.36 after three -20% steps: 106.17
max one-step change: 1.2 | max price: 200.0 | minutes at cap: 13
```

**Follow-ups:**
- How do you choose the absolute cap? From the business's tolerance, observed price response and complaint data, and legal or policy limits (ask compliance); I would start low and raise it only with evidence.
- Why not a user-level A/B test? Riders in a zone share the same supply, so treatment spills over; time-slice or zone randomisation handles it better.
- What about a downward step? Dropping 20% three times from 207.36 only gets to 106.17, so recovery is slow too; consider asymmetric limits.

**Common mistakes:**
- Treating 20% per step as a 20% limit overall.
- Forgetting the price may be applied every minute for 24 hours (144,000 decisions).
- Running user-level A/B tests where supply is shared.
- Learning elasticity only from the price range already used.

