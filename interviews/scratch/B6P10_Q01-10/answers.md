### Q1 ⭐⭐⭐ 🟢 Fraud detection: A UPI-style payments app handles 5,000,000 payments a day, with a projected peak of 300 scoring requests per second, and 0.05% of payments are fraud (a measured last-quarter average, 2,500 a day). Scoring must finish within 100 ms at the 99th percentile inside a 250 ms approval path, one scoring instance sustains 120 requests per second within that budget, and you want to provision capacity of 1.4 times the peak. Design the end-to-end fraud system and size the number of instances.
**Asked at:** Fraud-detection design material (an Educative fraud-detection mock interview, a PracHub real-time payment fraud prompt with a 50 ms budget and prep guides that call fraud the prompt where probabilities, thresholds and feature freshness must be discussed); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** I would score every payment synchronously in the approval path with a simple rules baseline first and a gradient-boosted model after it; at a 300 per second peak, 40% headroom and 120 per second per instance, that is 420 / 120 = 3.5, so 4 instances, and 5 if I want to survive losing one.

**Clarifying questions:**
- Is the score used before approval (blocking) or after the fact? It decides whether the 100 ms p99 budget is a hard constraint.
- What happens if the scorer is slow or down: fail open, fail closed, or fall back to rules? It sets the availability target and the cost of an outage.
- What do a missed fraud and a wrongly blocked customer cost, and is a step-up (extra confirmation) possible? Without the cost ratio I cannot choose a threshold.
- How late do fraud labels arrive (chargebacks, customer disputes)? It sets how I evaluate and how often I retrain.
- Is the 300 per second peak a measured busiest second or a projection? Capacity is paid for at the peak, so I want the real busiest minute.
- Who owns false positives and what review capacity exists? It limits how many flags we can act on.
- For anything about data use, retention or explainability: I would ask compliance and legal, not assume.

**Approach:**
1. Clarify and frame: decision at approval time, three actions (approve, step up, decline), owner for false positives, fail-open policy. Goal: reduce fraud loss at an acceptable false-decline rate.
2. Metrics and guardrails: recall at a fixed review or friction budget, precision of declines, rupee loss prevented minus friction cost. Guardrails: p99 latency, error rate, approval rate, customer complaints.
3. Data and labels: payment, device, account and merchant features; real-time counters (payments in the last 10 minutes) from a low-latency store; labels from disputes and chargebacks that mature over weeks, so training uses only matured windows. Label noise and unreported fraud are named risks.
4. Baseline first: a hand-written rules engine plus a logistic regression on a handful of velocity features. This is the bar the model must beat and the fallback when the model is down.
5. Model and trade-offs: gradient-boosted trees over a deep model, because tabular features, 15 ms inference and easy explanation. Tiered thresholds, not one cut-off. Cost ratio sets the threshold: block pays when precision exceeds friction / (friction + loss).
6. Evaluation: offline on a time-based split with matured labels (precision-recall, not accuracy); then shadow mode on live traffic; then a staged rollout, for example 1%, 10%, 50%, with a holdback group to measure true fraud.
7. Sizing and launch: 300 x 1.4 = 420 rps, 420 / 120 = 3.5, so 4 instances, 5 for N+1. Split the 100 ms p99: gateway 15, features 30, model 15, rules 10, logging 10, slack 20.
8. Monitoring, retraining, risks and cost: feature freshness, score distribution, fraud rate on matured labels, monthly retrain; fraudsters adapt, so keep a challenger. Cost is small next to fraud loss, so spend it on freshness and a second region.

Pacing for a 45-minute round (indicative): clarify 5, metrics 5, data and labels 7, baseline 4, model 7, evaluation 6, sizing and launch 6, monitoring and risks 5.

**Metrics:**
- Recall = frauds blocked or stepped up / all frauds (matured labels). Precision = frauds among flagged / flagged payments.
- Net value per day = fraud loss prevented - (false blocks x friction cost). Break-even precision = friction / (friction + loss); illustrative 40 and 2,000 rupees gives 1.96%.
- Guardrails: p99 scoring latency under 100 ms, error rate, approval rate, step-up completion rate, support contacts.
- The 0.05% fraud rate is a measured last-quarter average (a sample); the 300 per second peak is a projection.

**Risks:**
- Labels lag, so recent recall looks too good or too bad; evaluate on matured windows only.
- A feature fetched stale at serving time but fresh in training (training-serving skew) gives great offline and weak live results.
- Capacity sized on a projected peak: if the real peak is 2x higher, 4 instances fail. Add autoscaling and a rules fallback.
- Adaptive fraudsters after you start blocking.
- Headroom wording: 40% above peak is 420 rps; if the team means 60% target utilisation, it is 500 rps and 5 instances. Say which one you used.

**What the interviewer scores:**
- Strong: frames the decision and cost ratio before models, and gets 4 (or 5 with N+1) from 420 / 120. Weak: names Kafka and a neural net and never sizes anything.
- Strong: baseline first and a fail-open or rules fallback. Weak: no plan for the model being down.
- Strong: evaluates on matured labels with a time split, then shadow and staged rollout. Weak: random split and accuracy.
- Strong: says "ask compliance" for data and explainability rules. Weak: asserts a regulation from memory.

**Example:** (illustrative numbers) Peak 300 rps x 1.4 = 420 rps. One instance does 120, so 3.5 instances, round up to 4; at the real peak each runs at 300 / 480 = 62.5% utilisation. With 5 instances, losing one still leaves 480 rps.
- Weak: "I would use a deep model on Kafka and Redis, and it should scale."
- Strong: "First I would ask what happens when the scorer is down. Then size it: 300 times 1.4 is 420, divided by 120 is 3.5, so 4 instances and a fifth for failure. The model is a boosted tree behind a rules baseline, shadowed for two weeks before any real decline."

**Code:**
```python
import math
# Q1 fraud: illustrative numbers from the prompt
daily, fraud_rate = 5_000_000, 0.0005
peak, per_inst, headroom = 300, 120, 0.40
avg = daily / 86_400
fraud_day = daily * fraud_rate
target = peak * (1 + headroom)            # capacity to provision
raw = target / per_inst
n = math.ceil(raw)
n_plus1 = n + 1
util_at_peak = peak / (n * per_inst)
cap_after_loss = (n - 1) * per_inst
alt_util_rule = math.ceil(peak / 0.60 / per_inst)   # if "40% headroom" meant 60% target utilisation
print(f"avg {avg:.1f} rps, peak/avg {peak/avg:.2f}x, fraud/day {fraud_day:,.0f}")
print(f"target capacity {target:.0f} rps -> {raw:.2f} instances -> {n}; with N+1 {n_plus1}")
print(f"utilisation at peak with {n}: {util_at_peak:.1%}; capacity after losing one of {n_plus1}: {n*per_inst} rps")
print(f"if headroom meant 60% utilisation: {peak/0.60:.0f} rps -> {alt_util_rule} instances")
# illustrative threshold economics: missed fraud 2,000 rupees, friction per false block 40
miss_cost, fp_cost = 2000, 40
be_prec = fp_cost / (fp_cost + miss_cost)
print(f"break-even precision to block: {be_prec:.2%}")
# latency budget split of the 100 ms p99 scoring slice
split = {"gateway+network": 15, "feature fetch": 30, "model": 15, "rules+policy": 10, "serialise/log": 10, "slack": 20}
print(split, sum(split.values()))
assert round(avg, 1) == 57.9 and round(peak / avg, 2) == 5.18 and fraud_day == 2500
assert target == 420 and round(raw, 2) == 3.5 and n == 4 and n_plus1 == 5
assert round(util_at_peak, 3) == 0.625 and cap_after_loss == 360 and n * per_inst == 480
assert alt_util_rule == 5 and round(be_prec * 100, 2) == 1.96 and sum(split.values()) == 100
# the N+1 fleet of 5 still serves 4 x 120 = 480 >= 420 after losing one instance
assert (n_plus1 - 1) * per_inst >= target
```

**Output (my run):**
```text
avg 57.9 rps, peak/avg 5.18x, fraud/day 2,500
target capacity 420 rps -> 3.50 instances -> 4; with N+1 5
utilisation at peak with 4: 62.5%; capacity after losing one of 5: 480 rps
if headroom meant 60% utilisation: 500 rps -> 5 instances
break-even precision to block: 1.96%
{'gateway+network': 15, 'feature fetch': 30, 'model': 15, 'rules+policy': 10, 'serialise/log': 10, 'slack': 20} 100
```

**Follow-ups:**
- What if the peak doubles? 600 x 1.4 / 120 = 7 instances; autoscale on queue depth and keep the rules fallback.
- How do you evaluate with delayed labels? See Book 6 Part 2 Q4 (card-fraud model, delayed chargeback labels); use matured windows and an early proxy such as confirmed disputes, labelled as a proxy.
- Latency theory for the tail: Book 4 Part 6 Q6 (latency, throughput and percentiles for a model API).

**Common mistakes:** Sizing on the average 58 rps instead of the peak. Dividing by 0.6 and by 1.4 interchangeably without saying which. Optimising accuracy on a 0.05% base rate. No fallback when the model is down. Training on unmatured labels.

### Q2 ⭐⭐⭐ 🟢 Feed ranking: A short-video app has 2,000,000 daily active users who open the feed 5 times a day on average (10,000,000 feed requests a day), and the end-to-end budget for each request is 150 ms. Assume the peak is 5 times the daily average request rate and each request ranks 500 retrieved candidates. Design the feed recommender from retrieval to ranking and launch, and compute the peak requests per second and item scores per second the ranker must handle.
**Asked at:** General ML system-design prep material (Educative's 6-step ML design framework and fraud-detection mock interview, DesignGurus, techinterview.org, PracHub's 2026 ML system design bank and a DEV Community guide describe open prompts such as feed or recommendation, search ranking and ad prediction, and one guide quotes a search prompt with 1,000 queries per second and 200 ms); commercial prep sites, so example numbers are treated as examples only; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** I would build a two-stage feed, retrieval to 500 candidates then a learned ranker, and the sizing is 10,000,000 / 86,400 = 115.7 requests per second on average, 578.7 at the 5x peak, and 578.7 x 500 = about 289,000 item scores per second.

**Clarifying questions:**
- What is the objective: watch time, satisfied sessions, or something that includes creator fairness? Optimising raw watch time can hurt long-term retention.
- How much of the catalogue and of the users are new (cold start)? It decides how much I lean on content features and exploration.
- How fresh must new videos be in the feed? It sets index refresh and feature-update speed.
- Is the 5x peak factor measured or assumed? Capacity is paid for at the peak.
- Is the 150 ms end-to-end including network to the phone or only server time? It changes the server budget.
- What does a bad recommendation cost (safety, brand, a creator complaint)? It sets the filter layer and guardrails.

**Approach:**
1. Clarify and frame: objective, users, freshness, hard filters (safety, already-seen). Say the product goal in one line.
2. Metrics and guardrails: primary is satisfied watch time per daily active user (watch time with a quality filter such as completions or likes). Guardrails: next-day and 7-day retention, skip rate, creator diversity, p95 latency, crash rate.
3. Data and labels: impressions with watch time, completion, like, share, skip. Implicit labels are biased to what was shown, so log the position and keep a small random exploration slice.
4. Baseline first: popularity by region plus recency, then a simple two-tower or item-to-item retrieval. The ranker must beat this on the same offline split.
5. Model and trade-offs: retrieval 500 from several sources (embedding nearest neighbour, trending, followed creators); a multi-task ranker (P(watch), P(like), P(skip)) combined into one score; a re-rank layer for diversity and filters. Sizing: peak 578.7 rps x 500 = 289,352 items/s; an assumed 25,000 items/s per instance at 50% utilisation gives 24 instances. A pre-rank cut to 100 candidates drops that to 57,870 items/s and 5 instances, at some recall cost.
6. Evaluation: offline recall at 500 for retrieval and AUC or NDCG for the ranker with a time-based split; counterfactual caution because logs are biased; then an A/B test with retention as the decision metric.
7. Launch and experiment plan: shadow scoring, 1% then 10% then 50%, run at least one full weekly cycle, keep a holdback group of old-ranker users for a long-run check.
8. Monitoring and risks: feature freshness, score drift, share of cold-start items shown, feedback-loop effects (the model amplifies what it already shows). Retrain daily or weekly; rank on cached embeddings.

Pacing for a 45-minute round (indicative): clarify 5, metrics 5, data 5, baseline 3, model and sizing 12, evaluation 6, launch 4, monitoring and risks 5.

**Metrics:**
- Requests per day = daily active users x opens per user = 2,000,000 x 5 = 10,000,000 (a measured average).
- Peak rps = (requests per day / 86,400) x 5; item scores per second = peak rps x candidates per request.
- Satisfied watch time per DAU = watch minutes on videos meeting a quality filter / daily active users.
- Guardrails: 7-day retention, p95 under 150 ms, skip rate, creator concentration (share of impressions to the top 1% of creators).

**Risks:**
- The 5x peak is an assumption: if real peaks are 8x, the item rate is 463,000 per second and capacity must scale.
- Feedback loop: the ranker only sees feedback on items it showed, so exploration is needed.
- Optimising a short-term metric (watch time) at the cost of retention.
- Feature store or ANN index slow at peak eats the 150 ms budget.
- Cold start: new users and creators get little exposure without an explicit rule.

**What the interviewer scores:**
- Strong: staged funnel (retrieve, rank, re-rank), with the 289,352 items per second computed and a cut-down option. Weak: "one big model ranks everything".
- Strong: ties the metric to long-term retention and names guardrails. Weak: maximise click-through rate.
- Strong: addresses logging bias and exploration. Weak: random split and AUC only.
- Strong: gives a latency split that adds to 150. Weak: no budget.

**Example:** (illustrative numbers) 10,000,000 requests / 86,400 = 115.74 rps; x 5 = 578.7 rps; x 500 = 289,352 items per second.
- Weak: "I would train a deep recommender and deploy it on GPUs."
- Strong: "Retrieval gives 500 candidates, the ranker scores them, and at peak that is 579 requests a second, about 289,000 item scores a second. If the ranker only scores the best 100 after a cheap pre-rank, it is about 58,000, so I would test that cut against recall before buying capacity."

**Code:**
```python
import math
# Q2 feed ranking: illustrative numbers from the prompt plus clearly labelled assumptions
dau, opens, budget_ms = 2_000_000, 5, 150
req_day = dau * opens
avg = req_day / 86_400
peak = avg * 5
cands = 500
items_s = peak * cands
print(f"requests/day {req_day:,}, avg {avg:.1f} rps, peak {peak:.1f} rps")
print(f"item scores/s at peak {items_s:,.0f}")
# assumption (illustrative): one ranker instance scores 25,000 items/s; run at 50% at peak
inst_rate, util = 25_000, 0.5
inst = math.ceil(items_s / (inst_rate * util))
print(f"instances at 50% utilisation: {items_s/(inst_rate*util):.2f} -> {inst}")
# trade-off: pre-rank cut from 500 to 100 before the heavy ranker
cut = 100
items_cut = peak * cut
inst_cut = math.ceil(items_cut / (inst_rate * util))
print(f"with a pre-rank cut to {cut}: {items_cut:,.0f} items/s -> {inst_cut} instances")
split = {"gateway+network": 10, "retrieval": 40, "feature fetch": 30, "ranker": 40, "re-rank rules+serialise": 15, "slack": 15}
print(split, sum(split.values()))
assert req_day == 10_000_000 and round(avg, 2) == 115.74 and round(peak, 1) == 578.7
assert round(items_s) == 289_352
assert inst == 24 and round(items_s / (inst_rate * util), 2) == 23.15
assert round(items_cut) == 57_870 and inst_cut == 5
assert sum(split.values()) == budget_ms
```

**Output (my run):**
```text
requests/day 10,000,000, avg 115.7 rps, peak 578.7 rps
item scores/s at peak 289,352
instances at 50% utilisation: 23.15 -> 24
with a pre-rank cut to 100: 57,870 items/s -> 5 instances
{'gateway+network': 10, 'retrieval': 40, 'feature fetch': 30, 'ranker': 40, 're-rank rules+serialise': 15, 'slack': 15} 150
```

**Follow-ups:**
- How do you handle a new user? Start from popular content in their region and language, explore widely, and switch to personal signals after a few views.
- How do you check latency under load? Load-test at 1.4x the planned peak and watch p99; see Book 4 Part 6 Q6 (latency, throughput and percentiles for a model API).

**Common mistakes:** Using the average rps for capacity. Forgetting to multiply by candidates per request. Optimising click-through rate only. No exploration, so the model trains on its own shadow. A latency plan that does not add up to the budget.

### Q3 ⭐⭐⭐ 🟢 Churn and retention: A subscription app has 400,000 paying subscribers and about 4% of them leave each month (a measured 12-month average, 16,000 a month). A retention offer costs 150 rupees per contacted subscriber, a subscriber kept is worth 1,200 rupees of margin, and the monthly budget is 3,000,000 rupees. Design the churn-prevention programme, and compute how many subscribers the budget lets you contact and the share of contacted subscribers who must be saved by the offer, because of it, to break even.
**Asked at:** Churn and credit design material (a DataTalks.Club guide saying the question is what action follows a churn prediction, Dataford end-to-end churn pipeline prompts, Interview Query credit-risk company guides from Credit Karma, ZestFinance and TransUnion); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** A churn model is only worth what the action after it earns: the 3,000,000 rupee budget buys 20,000 contacts at 150 each, and the offer must save 150 / 1,200 = 12.5% of those contacted, 2,500 subscribers, because of the offer, just to break even.

**Clarifying questions:**
- What is the offer (discount, feature, call), and can it be A/B tested? Without randomised contact I cannot separate who would leave from who the offer changes.
- Is the 1,200 rupee value one-time margin or lifetime value, and for how long does a kept subscriber stay? It sets the break-even.
- Does the 150 rupees apply to everyone contacted, saved or not? In the prompt it does, so the cost is paid on all 20,000.
- Is the 4% a stable monthly rate or does it vary by plan and tenure? It is a 12-month average (a measured figure), not a guarantee for next month.
- What is the downside of contacting someone who would have stayed (annoyance, discount given for free)? It argues for uplift targeting rather than risk targeting.
- Which customers are off-limits (recent complaint, contract terms)? Ask the business and compliance for contact rules.

**Approach:**
1. Clarify and frame: the goal is incremental retained margin, not "predict churn". Define churn (no renewal within 30 days of due date) and the action.
2. Metrics and guardrails: net value = subscribers saved by the offer x 1,200 - contacts x 150. Guardrails: unsubscribe and complaint rate from contacted users, discount cost leaking to those who would stay.
3. Data and labels: tenure, usage trend, payment failures, support tickets, plan; label is churn within 30 days; cut features before the observation date to avoid leakage.
4. Baseline first: a rule such as "no login in 14 days or payment failed", plus a simple logistic regression. Measure what share of churners sits in the top 20,000.
5. Model and trade-offs: first a churn-risk model, then an uplift model once a randomised holdout exists. Risk targeting contacts those who will leave anyway and sure-things; uplift targets those whose behaviour the offer changes.
6. Evaluation: offline lift or precision at the top 20,000 on a time split; online, a randomised test with a no-contact control group to measure saves, not just churn.
7. Launch and experiment plan: pilot on 10% of the budget with a 10% control, then scale; a no-contact control stays permanently so the value keeps being measured.
8. Monitoring, risks and cost: save rate per segment, offer fatigue, drift in who churns. Retrain monthly. Cost is the contact spend; the model itself is cheap.

Pacing for a 45-minute round (indicative): clarify 6, metrics and break-even 8, data 5, baseline 4, model 8, evaluation and experiment 8, monitoring and risks 6.

**Metrics:**
- Contacts = budget / cost per contact = 3,000,000 / 150 = 20,000.
- Break-even save share of contacted = cost / value = 150 / 1,200 = 12.5%, or 2,500 subscribers, 15.6% of the 16,000 monthly churners (2,500 / 16,000).
- Save rate among reached churners needed = 2,500 / (churners in the contacted list). With 8,000 churners in the list (illustrative) it is 31.25%.
- Incremental save = outcome in contacted - outcome in randomised control, per subscriber. Guardrail: complaint rate.

**Risks:**
- Counting "contacted and did not churn" as saved. Many would have stayed, so only the difference against a control counts.
- Targeting by risk alone: high-risk people may not respond (lost causes), and some low-risk people leave when nudged.
- Selecting the top 20,000 on the same data you evaluate on inflates the lift (winner's curse); use a fresh holdout.
- The 4% is an average; a seasonal spike changes the base.

**What the interviewer scores:**
- Strong: states 20,000 contacts and 12.5% break-even correctly and notes the cost is paid on everyone contacted. Weak: "the model has 85% AUC so it works".
- Strong: separates churn prediction from uplift and asks for a randomised control. Weak: treats the whole 16,000 as savable.
- Strong: shows how break-even depends on precision (31.25% of reached churners at 40% precision). Weak: ignores that precision matters.
- Strong: names guardrails and a launch plan. Weak: no experiment.

**Example:** (illustrative numbers) The top 20,000 contains 8,000 real churners (precision 40%, recall 50%). If the offer saves 30% of those churners, 2,400 stay, which is 12.0% of the contacted: net = 2,400 x 1,200 - 3,000,000 = -120,000. At 35%, 2,800 stay and net is +360,000.
- Weak: "We predict churn with 80% accuracy and send everyone an offer."
- Strong: "The budget buys 20,000 contacts. Break-even is 2,500 saves, 12.5% of contacted. If my top 20,000 holds 8,000 churners, the offer has to save a third of them. I would test that with a control group before spending the full budget."

**Code:**
```python
# Q3 churn: illustrative numbers from the prompt
subs, churn_rate = 400_000, 0.04
cost, value, budget = 150, 1_200, 3_000_000
churners = subs * churn_rate
contacts = budget // cost
be_share = cost / value                     # share of CONTACTED who must be saved by the offer
be_saved = contacts * be_share
print(f"churners/month {churners:,.0f}; contacts the budget allows {contacts:,}")
print(f"break-even save share of contacted {be_share:.1%} = {be_saved:,.0f} subscribers saved")
print(f"as share of all monthly churners: {be_saved/churners:.1%}")
# illustrative targeting: model puts 8,000 churners in the 20,000 contacted (precision 40%, recall 50%)
churn_in = 8_000
prec, rec = churn_in / contacts, churn_in / churners
need_rate = be_saved / churn_in   # offer must save this share of the churners it reaches
print(f"precision {prec:.0%}, recall {rec:.0%}; offer must save {need_rate:.2%} of reached churners")
def net(save_rate): return churn_in * save_rate * value - contacts * cost
for sr in (0.30, 0.3125, 0.35):
    print(f"save rate {sr:.2%}: saved {churn_in*sr:,.0f}, net {net(sr):,.0f}")
# contacting everyone who will churn at random (no model) versus the model
rand_churn_in = contacts * churn_rate
print(f"random 20,000 would hold {rand_churn_in:,.0f} churners; break-even save rate {be_saved/rand_churn_in:.0%} (impossible)")
assert churners == 16_000 and contacts == 20_000
assert be_share == 0.125 and be_saved == 2_500 and round(be_saved / churners, 4) == 0.1562
assert prec == 0.40 and rec == 0.50 and need_rate == 0.3125
assert net(0.30) == -120_000 and net(0.3125) == 0 and net(0.35) == 360_000
assert rand_churn_in == 800 and be_saved / rand_churn_in > 1
```

**Output (my run):**
```text
churners/month 16,000; contacts the budget allows 20,000
break-even save share of contacted 12.5% = 2,500 subscribers saved
as share of all monthly churners: 15.6%
precision 40%, recall 50%; offer must save 31.25% of reached churners
save rate 30.00%: saved 2,400, net -120,000
save rate 31.25%: saved 2,500, net 0
save rate 35.00%: saved 2,800, net 360,000
random 20,000 would hold 800 churners; break-even save rate 312% (impossible)
```

**Follow-ups:**
- Risk model or uplift model? Start with risk because you have labels today; move to uplift when a randomised test supplies treatment-effect labels (see Book 6 Part 4 Q55, uplift model with a biased comparison, and Book 6 Part 5 Q14, randomised retention test).
- What if the budget could buy more contacts than there are churners? Then do not spend it; contact only where expected net value is positive.

**Common mistakes:** Calling every non-churner among the contacted "saved". Ignoring that the 150 rupees is paid on all contacts. Using a one-month value when the offer shifts lifetime value without saying so. Evaluating lift on the training period. No control group.

### Q4 ⭐⭐⭐ 🟢 Customer-support RAG: A bank wants an LLM assistant that answers from a knowledge base of 8,000 articles for 60,000 chats a day, with a 4-second 95th-percentile budget to the first token. Each chat uses an average of 4,000 input tokens and 300 output tokens per chat, summed over all its turns, at an illustrative 0.30 rupees per 1,000 input tokens and 1.20 per 1,000 output tokens, and the ceiling is 2.00 rupees per chat. Design the system end to end, and compute the cost per chat, the daily cost and the headroom under the ceiling.
**Asked at:** LLM support-bot design material (an Educative 'LLM-powered customer support bot' lesson with gateway, retrieval, moderation and tiered model routing, a 1point3acres post reporting a Databricks prompt to design a RAG chatbot over enterprise data, and Interview Kickstart and Robylon guides; vendor accuracy figures in those pages were not relied on); prep-site and candidate-reported material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** I would build a retrieval-grounded assistant with a guardrail and a human handoff, and the cost is 4 x 0.30 + 0.3 x 1.20 = 1.56 rupees per chat, 93,600 a day, leaving 0.44 rupees (22% of the 2.00 ceiling) for retries, reranking and safety calls.

**Clarifying questions:**
- Is "4,000 input tokens and 300 output tokens" per whole chat or per turn? A multi-turn chat resends history, so a per-turn figure multiplies the cost.
- Does "4 seconds to the first answer" mean the first streamed token or the complete reply? A 300-token reply at an assumed 60 tokens per second takes 5 seconds on its own, so only the first reading is feasible.
- What may the assistant do: answer from articles only, or also take actions such as blocking a card? It sets the autonomy level and the guardrails.
- What is the cost of a wrong answer, and how is it handed to a human? A bank needs a conservative abstain-and-escalate path.
- How often does the knowledge base change? It sets re-indexing frequency and the staleness risk.
- Which data may go to an external model, and what must be masked? Ask compliance and security; do not assume.

**Approach:**
1. Clarify and frame: scope (answer from 8,000 articles), unsupported questions escalate, define "first answer" as first token.
2. Metrics and guardrails: resolution without human handoff, grounded-answer rate (each claim traceable to a retrieved article), cost per chat, p95 time to first token. Guardrails: wrong-answer rate on a graded sample, escalation rate, customer satisfaction.
3. Data and labels: chunk the 8,000 articles with titles and dates; build 300-500 real past questions with the correct article as a labelled evaluation set; support agents grade samples of answers.
4. Baseline first: keyword or BM25 search plus returning the top article snippet, no generation. Compare every later step to this on the same labelled questions.
5. Model and trade-offs: dense plus keyword retrieval, rerank the top 20 to 5, a mid-size model writing the answer with citations, a small router sending simple questions to a cheaper model. Cost per chat = 1.20 + 0.36 = 1.56; headroom 0.44 is roughly 1,467 extra input tokens, so a second model call or a long history can break the ceiling.
6. Evaluation: retrieval recall at 5 against the labelled set, answer groundedness by human or model graders (calibrated against humans), then shadow mode where agents see the draft and correct it.
7. Launch and experiment plan: internal agents first, then 5% of chats with a human fallback, then 25%, with a random control for resolution and satisfaction; kill switch on a groundedness drop.
8. Monitoring, risks and cost: log retrieved articles, abstain rate, cost per chat daily, drift when articles change; re-index on publish. Cut cost with caching of frequent questions, shorter context and tiered routing.

Pacing for a 45-minute round (indicative): clarify 5, metrics 5, data 5, baseline 4, model and cost 10, evaluation 6, launch 4, monitoring and risks 6.

**Metrics:**
- Cost per chat = input tokens / 1,000 x input price + output tokens / 1,000 x output price (illustrative prices).
- Headroom = ceiling - cost per chat = 2.00 - 1.56 = 0.44 rupees; as a share of ceiling 0.44 / 2.00 = 22%.
- Containment = chats resolved without a human / all chats; groundedness = answers whose claims are supported by retrieved text / sampled answers.
- p95 time to first token under 4 seconds (the stated budget); guardrail: unsafe or wrong-answer rate on a graded weekly sample.

**Risks:**
- Hallucinated policy answers; mitigate with citations and abstain-below-threshold.
- Prompt injection from retrieved or user text; treat retrieved text as untrusted.
- Stale articles producing outdated answers.
- Hidden token growth: conversation history and long retrieved chunks push the 4,000 tokens up and the cost past 2.00.
- Privacy: personal data in prompts; ask security and compliance what may leave the bank.

**What the interviewer scores:**
- Strong: gets 1.56, 93,600 and 0.44 and explains what eats the headroom. Weak: gives only a diagram.
- Strong: defines first answer as first token and shows a latency split. Weak: ignores the 4 seconds.
- Strong: evaluation set, retrieval and answer metrics separated, human fallback. Weak: "check if answers look good".
- Strong: staged rollout with a kill switch. Weak: launch to everyone.

**Example:** (illustrative numbers) Per chat: 4,000 / 1,000 x 0.30 = 1.20 plus 300 / 1,000 x 1.20 = 0.36, so 1.56. Over 60,000 chats: 93,600 a day, 2,808,000 over 30 days.
- Weak: "We use the best large model with all articles in the prompt."
- Strong: "Retrieval first, five chunks, a mid-size model with citations, and a human handoff when confidence is low. It costs 1.56 a chat, 93,600 a day, with 0.44 left under the ceiling, which is about 1,500 more input tokens. If a reranker or a retry would use that, I would route easy questions to a cheaper model, which in my illustration cuts the cost to about 0.81."

**Code:**
```python
# Q4 support RAG cost: illustrative prices from the prompt
chats, in_tok, out_tok = 60_000, 4_000, 300
p_in, p_out, ceiling = 0.30, 1.20, 2.00     # rupees per 1,000 tokens (illustrative)
c_in = in_tok / 1000 * p_in
c_out = out_tok / 1000 * p_out
per_chat = c_in + c_out
daily = chats * per_chat
headroom = ceiling - per_chat
print(f"input {c_in:.2f} + output {c_out:.2f} = {per_chat:.2f} per chat; daily {daily:,.0f}; 30 days {daily*30:,.0f}")
print(f"headroom {headroom:.2f} per chat = {headroom/ceiling:.0%} of ceiling; ceiling-level daily {ceiling*chats:,.0f}")
extra_in_tokens = headroom / p_in * 1000
print(f"headroom equals about {extra_in_tokens:,.0f} extra input tokens per chat")
# illustrative tiering: 60% of chats go to a model priced at one fifth
tier = 0.4 * per_chat + 0.6 * per_chat / 5
print(f"illustrative tiered cost per chat {tier:.3f}, daily {tier*chats:,.0f}")
# latency: why 'first answer' must mean first token / first chunk
gen_rate = 60  # tokens per second, assumption
full_gen_s = out_tok / gen_rate
print(f"full 300-token answer at {gen_rate} tok/s takes {full_gen_s:.1f} s, over the 4 s budget")
split = {"input guard": 100, "retrieve": 150, "rerank": 150, "prompt build": 50, "first token": 800, "streaming to user": 100}
print(split, sum(split.values()))
avg_cps = chats / 86_400
print(f"average {avg_cps:.2f} chats/s")
assert round(c_in, 2) == 1.20 and round(c_out, 2) == 0.36 and round(per_chat, 2) == 1.56
assert round(daily) == 93_600 and round(headroom, 2) == 0.44
assert round(headroom / ceiling, 2) == 0.22 and round(extra_in_tokens) == 1467
assert round(tier, 3) == 0.811 and round(full_gen_s, 1) == 5.0
assert sum(split.values()) == 1350 and sum(split.values()) < 4000
assert round(avg_cps, 2) == 0.69
```

**Output (my run):**
```text
input 1.20 + output 0.36 = 1.56 per chat; daily 93,600; 30 days 2,808,000
headroom 0.44 per chat = 22% of ceiling; ceiling-level daily 120,000
headroom equals about 1,467 extra input tokens per chat
illustrative tiered cost per chat 0.811, daily 48,672
full 300-token answer at 60 tok/s takes 5.0 s, over the 4 s budget
{'input guard': 100, 'retrieve': 150, 'rerank': 150, 'prompt build': 50, 'first token': 800, 'streaming to user': 100} 1350
average 0.69 chats/s
```

**Follow-ups:**
- How do you cut latency? Stream the answer, run guard and retrieval in parallel where possible, cache frequent questions; see Book 6 Part 7 Q29 (a RAG request with sequential stages) and Part 7 Q4 (time to first token).
- How do you know it is grounded? Citations plus a sampled human grade, and an automatic check that cited text supports the claim, calibrated against the human grades.

**Common mistakes:** Ignoring that conversation history multiplies input tokens. Treating "first answer" as the full reply. No labelled retrieval set. Sending everything to the largest model. Launching without a human fallback.

### Q5 ⭐⭐⭐ 🟡 Search ranking: A marketplace search serves a peak of 1,000 queries per second with a 200 ms end-to-end budget, retrieves 2,000 candidates per query and reranks the top 100 with a learned model. One CPU core scores 25,000 items per second, and you plan to run cores at 50% utilisation at peak. Design the search ranking solution including labels, and compute the cores needed for reranking and how you would split the 200 ms.
**Asked at:** General ML system-design prep material (Educative's 6-step ML design framework and fraud-detection mock interview, DesignGurus, techinterview.org, PracHub's 2026 ML system design bank and a DEV Community guide describe open prompts such as feed or recommendation, search ranking and ad prediction, and one guide quotes a search prompt with 1,000 queries per second and 200 ms); commercial prep sites, so example numbers are treated as examples only; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** I would use a funnel, cheap retrieval of 2,000 then a learned reranker on the top 100, because reranking 100 items at 1,000 queries per second is 100,000 items per second, which at 25,000 x 50% = 12,500 per core needs exactly 8 cores, while scoring all 2,000 would need 160.

**Clarifying questions:**
- What does a good result mean here: purchase, click then no bounce, or seller fairness? It sets labels and the primary metric.
- Is the 1,000 queries per second a measured peak or a projection, and what is the daily shape? Capacity is paid for at the peak.
- Is the 200 ms client-visible or server-side only? It sets the real server budget.
- How much of the query traffic is new or long-tail? It decides how much depends on semantic retrieval and how many labels exist.
- Are there business rules (sponsored slots, in-stock only, seller caps)? They sit after the ranker and eat time.
- What judged data exist today (clicks, purchases, human relevance judgements)? It decides the label plan.

**Approach:**
1. Clarify and frame: query types, what success means, hard filters (in stock, region), the 200 ms budget.
2. Metrics and guardrails: offline NDCG@10 against graded judgements; online conversion per search session and null-result rate; guardrails p99 latency, zero-result rate, seller concentration.
3. Data and labels: clicks and purchases are plentiful but position-biased (top results get clicked more), so use position as a feature or correct it with inverse-propensity weights, and add a human-judged set of query-item pairs for evaluation. Labelling 50,000 pairs at 5 per rater-minute is about 167 rater-hours (illustrative).
4. Baseline first: keyword retrieval (BM25-style) with a hand-tuned score on text match, popularity and recency. The learned model must beat this on the judged set.
5. Model and trade-offs: first-stage retrieval (keyword plus embedding nearest neighbour) returns 2,000 cheaply; a gradient-boosted ranker or small neural model reranks the top 100. Sizing: 1,000 x 100 = 100,000 items/s; 25,000 x 0.5 = 12,500 per core; 100,000 / 12,500 = 8 cores. That has no headroom at exactly 8, so I would run 10 or autoscale. Scoring all 2,000 would be 2,000,000 items/s and 160 cores, a 20x cost for a small recall gain.
6. Evaluation: offline NDCG and recall at 2,000 for retrieval (did the right item reach the reranker), then interleaving or an A/B test on conversion; slice by head and tail queries.
7. Launch and experiment plan: shadow rerank, then 1% to 10% to 50% traffic, p99 watched at each step; a cheap fallback ranker if the model times out.
8. Monitoring, risks and cost: query mix drift, feature freshness, rank-position click curves, index lag. Retrain weekly on recent logs; budget cores at 50% utilisation to absorb spikes.

Latency split of the 200 ms (illustrative): gateway and network 20, query understanding 20, retrieval 50, feature fetch 30, rerank 30, blend and render 20, slack 30.

Pacing for a 45-minute round (indicative): clarify 5, metrics 4, data and labels 8, baseline 3, model and sizing 10, evaluation 6, launch 4, monitoring and risks 5.

**Metrics:**
- NDCG@10 = discounted gain of the top 10 returned divided by the best possible for that query, averaged over judged queries.
- Rerank load (items per second) = queries per second x items reranked; cores = load / (per-core rate x utilisation).
- Retrieval recall@2,000 = relevant items present in the 2,000 / all relevant items; online conversion per search session.
- Guardrails: p99 latency under 200 ms, zero-result rate, share of impressions to the top sellers.

**Risks:**
- Position bias in click labels trains the model to repeat the old ranking.
- A good reranker cannot fix items that retrieval missed; watch recall@2,000.
- Exactly 8 cores means 100% of the usable budget; any spike breaks p99.
- Long-tail queries have few clicks and noisy labels.
- Feature fetch from a remote store dominating the budget.

**What the interviewer scores:**
- Strong: two-stage funnel with the 100,000 items per second and 8 cores computed, and the 160-core alternative used as the argument. Weak: one model over everything.
- Strong: discusses position bias and a judged evaluation set. Weak: trains on raw clicks and reports AUC.
- Strong: latency split that adds to 200 and a fallback. Weak: no budget.
- Strong: separates retrieval recall from ranking quality. Weak: one aggregate metric.

**Example:** (illustrative numbers) Peak 1,000 queries per second x 100 reranked items = 100,000 items/s. Each core is used at 50%, so it gives 12,500 items/s. 100,000 / 12,500 = 8 cores. Compute per query for 100 items on one core is 100 / 25,000 = 4 ms, so 30 ms for the rerank stage leaves room for batching and waiting.
- Weak: "I would use a transformer over all the results."
- Strong: "Retrieval gets 2,000 cheaply. The learned model only sees the top 100, which is 100,000 items a second, 8 cores at half load. Scoring all 2,000 would be 160 cores, so I would only widen the rerank depth if recall at 100 is the bottleneck."

**Code:**
```python
import math
# Q5 search ranking: illustrative numbers from the prompt
qps, cands, rerank_k = 1_000, 2_000, 100
core_rate, util = 25_000, 0.50
items_s = qps * rerank_k
eff = core_rate * util
cores = math.ceil(items_s / eff)
print(f"rerank load {items_s:,} items/s; effective per core {eff:,.0f}; cores {items_s/eff:.2f} -> {cores}")
full = qps * cands
print(f"if the learned model scored all {cands}: {full:,} items/s -> {math.ceil(full/eff)} cores ({full/items_s:.0f}x)")
print(f"single-core compute per query for {rerank_k} items: {rerank_k/core_rate*1000:.1f} ms")
split = {"gateway+network": 20, "query understanding": 20, "retrieval (2,000)": 50, "feature fetch": 30, "rerank (100)": 30, "blend+filters+render": 20, "slack": 30}
print(split, sum(split.values()))
# label budget illustration: 50,000 judged query-item pairs at 5 pairs/min per rater
pairs, rate = 50_000, 5
hours = pairs / rate / 60
print(f"labelling {pairs:,} pairs at {rate}/min = {hours:,.0f} rater-hours")
assert items_s == 100_000 and eff == 12_500 and cores == 8 and round(items_s / eff, 2) == 8.00
assert full == 2_000_000 and math.ceil(full / eff) == 160 and full / items_s == 20
assert rerank_k / core_rate * 1000 == 4.0 and sum(split.values()) == 200
assert round(hours) == 167
```

**Output (my run):**
```text
rerank load 100,000 items/s; effective per core 12,500; cores 8.00 -> 8
if the learned model scored all 2000: 2,000,000 items/s -> 160 cores (20x)
single-core compute per query for 100 items: 4.0 ms
{'gateway+network': 20, 'query understanding': 20, 'retrieval (2,000)': 50, 'feature fetch': 30, 'rerank (100)': 30, 'blend+filters+render': 20, 'slack': 30} 200
labelling 50,000 pairs at 5/min = 167 rater-hours
```

**Follow-ups:**
- How would you raise the rerank depth? Measure recall@100 versus recall@300; each extra 100 items costs 8 cores at this traffic.
- How do you correct position bias? Log the shown position, add it as a feature during training and fix it at a constant at serving, or weight clicks by inverse propensity; verify with a small randomised slot test.

**Common mistakes:** Forgetting that only the top 100 are reranked. Using 100% core utilisation. Training on clicks without handling position. Judging only on average NDCG and missing tail queries. No fallback when the ranker is slow.

### Q6 ⭐⭐⭐ 🟡 ETA prediction: A food-delivery app takes 400,000 orders a day, and an order stays in flight for 35 minutes on average. Assume 20% of daily orders arrive evenly across a 2-hour lunch peak and ignore orders arriving outside the lunch window, the ETA is computed once at checkout and then refreshed every 30 seconds while the order is in flight, and one prediction service answers both. Design the ETA system, and use Little's law to compute the orders in flight at the peak, the refresh requests per second and the total requests per second including checkout calls.
**Asked at:** ETA, forecasting and pricing design material (a CleverPrep Lyft ML engineer page listing real-time pricing, city-level demand forecasting with cold start and ETA-with-traffic prompts, an AlgoMaster ETA design page, Codemia demand-forecasting pipeline prompts and an AI Engineering Insider dynamic-pricing piece); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** By Little's law the orders in flight are arrival rate times time in system, 11.11 orders per second x 2,100 seconds = about 23,300, so refreshing every 30 seconds is 778 requests per second, 98.6% of the roughly 789 total with checkout calls.

**Clarifying questions:**
- Do the other 80% of daily orders also arrive during the lunch window? The prompt spreads only the 20% across the peak; background orders would add to the in-flight count.
- What is the ETA used for: a promise shown at checkout, rider dispatch, or both? A promise needs calibrated, slightly conservative estimates.
- How costly is under-promising (lost orders) versus over-promising (late, refunds)? It decides whether the target is the median or a high quantile.
- Must the refresh be polled every 30 seconds, or can the app be pushed an update only when the ETA changes? It decides the load.
- What data exist: restaurant prep-time history, rider GPS, traffic? It sets the features and the cold-start plan for new restaurants.
- Is the 35 minutes an average with a long tail (some orders much longer)? Little's law needs only the average, but capacity planning feels the tail.

**Approach:**
1. Clarify and frame: separate the legs (restaurant prep, rider pickup, travel, handover), the use of the number, and the quantity predicted (median versus 80th percentile).
2. Metrics and guardrails: mean absolute error in minutes, coverage of a stated interval (for example 80% of orders arrive before the promised time) and the late-delivery rate. Guardrails: orders lost from long promised times, p99 latency of the service, refresh error rate.
3. Data and labels: label = actual minutes from order to delivery, collected for every completed order (no delay problem); features: prep-time history per restaurant, time and day, distance, live traffic, order size, rider supply.
4. Baseline first: a lookup of restaurant median prep time plus distance divided by an average speed by hour; the model has to beat it in MAE and in late rate.
5. Model and trade-offs: a gradient-boosted model per leg or one model with leg features, with quantile outputs for uncertainty; refresh by re-running with the new rider position. Sizing with Little's law: arrivals 80,000 / 7,200 s = 11.11 per second; in flight = 11.11 x 2,100 = 23,333; refresh = 23,333 / 30 = 777.8 rps; plus 11.11 checkout calls = 788.9 rps. A 60-second refresh halves that to 400 rps; pushing updates only on change cuts it further.
6. Evaluation: offline MAE and interval coverage on a time-based split, sliced by restaurant, hour and zone; then shadow ETA next to the existing one; then an A/B test on conversion at checkout and the late rate.
7. Launch and experiment plan: shadow for a week, then one city, then all; a fallback to the baseline when features are missing.
8. Monitoring, risks and cost: error by hour and restaurant, coverage drift, feature freshness (traffic, GPS). Retrain weekly; cache static features; autoscale on the refresh rate.

Pacing for a 45-minute round (indicative): clarify 5, metrics 5, data 5, baseline 4, model and sizing 11, evaluation 6, launch 4, monitoring and risks 5.

**Metrics:**
- Orders in flight L = arrival rate x average time in system (steady state): 11.11/s x 2,100 s = 23,333.
- Refresh rps = in flight / refresh interval = 23,333 / 30 = 777.8; total rps = refresh rps + checkout rps = 777.8 + 11.11 = 788.9.
- Coverage = orders delivered no later than the promised time / orders with a promise (target set by the business, for example 80%).
- Late rate and MAE in minutes, per segment; guardrails: conversion at checkout, p99 service latency.

**Risks:**
- The prompt counts only the 20% peak arrivals. If background orders continue at 320,000 / 79,200 s = 4.04 per second, in flight is about 31,800 and total load about 1,076 rps (illustrative).
- Little's law assumes steady state; the peak lasts 120 minutes against a 35-minute dwell, which is long enough.
- A promise that is too optimistic raises conversion but also lateness and refunds.
- Polling dominates: 98.6% of requests are refreshes of orders whose ETA did not change.
- Sparse data for new restaurants and new zones.

**What the interviewer scores:**
- Strong: uses L = lambda x W correctly, with 23,333, 777.8 and 788.9. Weak: confuses daily orders with in-flight orders.
- Strong: sees that refresh traffic dwarfs checkout traffic and proposes push or a longer interval. Weak: sizes only for checkout.
- Strong: asks which quantity to predict and defines coverage, not only MAE. Weak: minimises MAE alone.
- Strong: states the steady-state assumption. Weak: silent on it.

**Example:** (illustrative numbers) 80,000 peak orders in 2 hours is 11.11 per second. Each stays 35 minutes, so at any moment about 11.11 x 2,100 = 23,333 are in flight. Each refreshes twice a minute, so 23,333 / 30 = 777.8 refresh calls per second.
- Weak: "400,000 orders a day, so about 5 requests per second."
- Strong: "At the peak 11 orders arrive a second and each lives 35 minutes, so Little's law gives about 23,000 in flight. At a 30-second refresh that is 778 requests a second, 99% of the total, so the first design question is whether the app needs to poll at all."

**Code:**
```python
import math
# Q6 ETA: illustrative numbers from the prompt (peak orders assumed to be only the 20% peak arrivals)
orders_day, peak_share, peak_hours = 400_000, 0.20, 2
dwell_s, refresh_s = 35 * 60, 30
peak_orders = orders_day * peak_share
lam = peak_orders / (peak_hours * 3600)          # orders per second during peak
L = lam * dwell_s                                 # Little's law: L = lambda * W
refresh_rps = L / refresh_s
total_rps = refresh_rps + lam
print(f"peak arrivals {peak_orders:,.0f} over {peak_hours} h = {lam:.2f} orders/s")
print(f"in flight at peak L = {lam:.2f} x {dwell_s} s = {L:,.0f}")
print(f"refresh {refresh_rps:,.1f} rps + checkout {lam:.2f} rps = {total_rps:,.1f} rps; refresh share {refresh_rps/total_rps:.1%}")
print(f"average in flight over the day {orders_day/86_400*dwell_s:,.0f} ({L/(orders_day/86_400*dwell_s):.1f}x)")
print(f"60 s refresh: {L/60:,.1f} + {lam:.2f} = {L/60+lam:,.1f} rps")
# caveat: the other 80% of orders (320,000) over the other 22 hours also overlap lunch
bg = orders_day * 0.80 / (22 * 3600)
print(f"if background orders continue at {bg:.2f}/s: in flight {(lam+bg)*dwell_s:,.0f}, total rps {(lam+bg)*dwell_s/refresh_s + lam + bg:,.1f}")
# instances at an assumed 150 rps each and 60% utilisation
inst = math.ceil(total_rps / (150 * 0.6))
print(f"instances at 150 rps x 60%: {total_rps/(150*0.6):.2f} -> {inst}")
# steady state is reached once the peak lasts longer than the dwell time
print(f"peak lasts {peak_hours*60} min vs dwell 35 min -> steady state reached")
assert peak_orders == 80_000 and round(lam, 2) == 11.11
assert round(L) == 23_333 and round(refresh_rps, 1) == 777.8 and round(total_rps, 1) == 788.9
assert round(refresh_rps / total_rps, 3) == 0.986
assert round(orders_day / 86_400 * dwell_s) == 9_722
assert round(L / 60 + lam, 1) == 400.0
assert round(bg, 2) == 4.04 and round((lam + bg) * dwell_s) == 31_818
assert inst == 9 and peak_hours * 60 > 35
```

**Output (my run):**
```text
peak arrivals 80,000 over 2 h = 11.11 orders/s
in flight at peak L = 11.11 x 2100 s = 23,333
refresh 777.8 rps + checkout 11.11 rps = 788.9 rps; refresh share 98.6%
average in flight over the day 9,722 (2.4x)
60 s refresh: 388.9 + 11.11 = 400.0 rps
if background orders continue at 4.04/s: in flight 31,818, total rps 1,075.8
instances at 150 rps x 60%: 8.77 -> 9
peak lasts 120 min vs dwell 35 min -> steady state reached
```

**Follow-ups:**
- What if the refresh interval doubles to 60 seconds? Refresh falls to 388.9 rps and the total to 400.0 rps; ETA staleness doubles, so check it against the accuracy guardrail.
- Which percentile do you serve? The percentile that matches the cost ratio, often above the median for a promise; capacity theory is in Book 4 Part 6 Q6 (latency, throughput and percentiles for a model API).

**Common mistakes:** Treating daily orders as the concurrency. Forgetting the refresh multiplies requests. Averaging the peak over 24 hours. Not stating that Little's law needs steady state. Minimising MAE when the business cares about being late.

### Q7 ⭐⭐⭐ 🟡 Demand forecasting: A grocery chain with 300 stores and 4,000 products per store (1,200,000 store-product series) needs a 14-day daily forecast produced each night inside a 3-hour batch window, and 40% of the series are intermittent, with many zero-sales days. A worker process can forecast 10 series per second. Design the forecasting solution, and compute the series per second the batch needs and the workers required.
**Asked at:** ETA, forecasting and pricing design material (a CleverPrep Lyft ML engineer page listing real-time pricing, city-level demand forecasting with cold start and ETA-with-traffic prompts, an AlgoMaster ETA design page, Codemia demand-forecasting pipeline prompts and an AI Engineering Insider dynamic-pricing piece); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The batch must produce 1,200,000 / 10,800 s = 111.1 series per second, which at 10 series per worker is 11.1, so 12 workers at 92.6% of the window, and I would run about 15 to leave room for retries; the harder design question is how to forecast the 40% intermittent series.

**Clarifying questions:**
- What decision does the forecast drive: order quantity, markdown, or staffing? It sets the metric and whether I need quantiles, not only a mean.
- What is the cost of a stock-out versus overstock, and is the product perishable? It sets the target quantile.
- Is "10 series per second per worker" measured on the real model, including intermittent series and feature building? A blended assumption hides slow cases.
- How are promotions, holidays and price changes known in advance? They are the biggest drivers of error.
- What is the history length, and how many series are new (cold start)? It decides the model type.
- What is the retry rule if the 3-hour window is missed: serve yesterday's forecast? It defines the fallback.

**Approach:**
1. Clarify and frame: decision, forecast level (store x product x day), horizon 14 days, hierarchy (store, category, chain) and the 3-hour nightly window.
2. Metrics and guardrails: weighted absolute percentage error (WAPE) = sum of absolute errors / sum of actuals, bias = sum of forecast minus actual / sum of actuals, and for stocking the quantile (pinball) loss at the service level; for intermittent series do not use MAPE (it divides by zero). Guardrails: stock-outs, waste, batch finish time.
3. Data and labels: daily sales per series with stock-out flags (zero sales while out of stock is not zero demand), promotions, calendar, price, weather if useful; label = units sold per day for the next 14 days.
4. Baseline first: seasonal naive (same weekday last week) or a moving average; every later model is judged against it on the same rolling-origin backtest.
5. Model and trade-offs: one global gradient-boosted model across series for the regular 60% (720,000 series), with a separate treatment for the 480,000 intermittent ones (interval-based methods such as Croston or a count or quantile model on the global features; see the cross-reference below). Sizing: 111.11 series per second needed; 11.11 workers; 12 workers uses 92.6% of the 10,800 seconds; with 30% headroom 15. If intermittent series cost twice as much (illustrative), the blended rate is 7.14 per second and the need is 16 workers.
6. Evaluation: rolling-origin backtests over several weeks, not one random split; WAPE and bias by segment (regular, intermittent, promo, new); quantile coverage; compare to the baseline per segment.
7. Launch and experiment plan: shadow forecasts for 4 weeks while the old process orders; pilot in a few stores with a control set; business value measured as stock-outs and waste difference.
8. Monitoring, risks and cost: bias drift, batch runtime, share of series falling back to the baseline; retrain weekly. Compute cost is small next to the stock decisions; cap the window with a fallback to yesterday's forecast.

Pacing for a 45-minute round (indicative): clarify 5, metrics 6, data 4, baseline 3, model and sizing 12, evaluation 7, launch 4, monitoring and risks 4.

**Metrics:**
- Series per second needed = series count / window seconds = 1,200,000 / 10,800 = 111.11; workers = need / per-worker rate = 11.11, rounded up to 12.
- WAPE = sum over series and days of |forecast - actual| / sum of actuals; bias = (sum forecast - sum actual) / sum actual.
- Pinball loss at quantile q = mean of max(q x (actual - forecast), (q - 1) x (actual - forecast)); coverage = actuals at or below the q-quantile forecast / all.
- Guardrails: batch finish time within 3 hours, stock-out rate, waste, share of series on fallback.

**Risks:**
- Zeros from stock-outs read as zero demand and bias forecasts down.
- MAPE and symmetric errors mislead on intermittent series; use WAPE and quantiles.
- 12 workers use 92.6% of the window with a single failure forcing a miss; add headroom or a retry queue.
- Promotion calendars unknown in advance make the 14-day horizon unreliable.
- Cold-start products have no history.

**What the interviewer scores:**
- Strong: 111.1 per second, 11.11 so 12 workers, plus headroom and a fallback. Weak: names a model and never sizes the batch.
- Strong: handles intermittent demand explicitly, with the right metric. Weak: MAPE on series with zeros.
- Strong: rolling-origin backtest and the cost ratio driving the quantile. Weak: random split and a mean forecast.
- Strong: notes stock-out censoring. Weak: treats zeros as demand.

**Example:** (illustrative numbers) 300 stores x 4,000 products = 1,200,000 series. In 3 hours (10,800 seconds) that is 111.1 series per second. Ten per worker per second gives 11.1 workers, so 12, using 92.6% of the window.
- Weak: "I would train an LSTM per product."
- Strong: "I need 111 series a second; a worker does 10, so 12 workers with no room to spare, and I would run 15. 480,000 series are intermittent, so I would not use MAPE or a plain average there; I would forecast a quantile and judge it with pinball loss against a seasonal-naive baseline."

**Code:**
```python
import math
# Q7 forecasting batch: illustrative numbers from the prompt
stores, per_store, window_h, worker_rate = 300, 4_000, 3, 10
series = stores * per_store
window_s = window_h * 3600
need = series / window_s
workers_exact = need / worker_rate
workers = math.ceil(workers_exact)
util = series / (workers * worker_rate * window_s)
print(f"series {series:,}; window {window_s:,} s; need {need:.2f} series/s; workers {workers_exact:.2f} -> {workers}")
print(f"with {workers} workers batch uses {util:.1%} of the window; spare {workers*worker_rate*window_s - series:,} series-slots")
w30 = math.ceil(workers_exact * 1.3)
print(f"with 30% headroom for retries and slow nodes: {w30} workers")
intermittent = int(series * 0.40)
print(f"intermittent series {intermittent:,}; regular {series-intermittent:,}; output rows {series*14:,}")
# if intermittent series take twice as long per series (illustrative), blended rate falls
blend_time = 0.6 * 1 + 0.4 * 2          # relative time per series
print(f"if intermittent cost 2x, blended rate {worker_rate/blend_time:.2f}/s -> workers {math.ceil(need/(worker_rate/blend_time))}")
assert series == 1_200_000 and window_s == 10_800 and round(need, 2) == 111.11
assert round(workers_exact, 2) == 11.11 and workers == 12 and round(util, 3) == 0.926
assert w30 == 15 and intermittent == 480_000 and series * 14 == 16_800_000
assert math.ceil(need / (worker_rate / blend_time)) == 16 and round(worker_rate / blend_time, 2) == 7.14
```

**Output (my run):**
```text
series 1,200,000; window 10,800 s; need 111.11 series/s; workers 11.11 -> 12
with 12 workers batch uses 92.6% of the window; spare 96,000 series-slots
with 30% headroom for retries and slow nodes: 15 workers
intermittent series 480,000; regular 720,000; output rows 16,800,000
if intermittent cost 2x, blended rate 7.14/s -> workers 16
```

**Follow-ups:**
- What if the window shrinks to 1 hour? 1,200,000 / 3,600 = 333.3 per second, so 33.3 workers, 34 rounded up; consider a global batched model instead of per-series fits.
- How to forecast intermittent demand? See Book 1 Part 6 Q30 (forecasting intermittent or lumpy demand: Croston, SBA, TSB and metrics) and Book 4 Part 12 Q14 (demand forecasting platform, clarify first).

**Common mistakes:** One metric for all series. MAPE with zero sales. Ignoring stock-out censoring. Zero headroom on the batch window. A random train and test split on time series.

### Q8 ⭐⭐⭐ 🟡 Notification targeting: An app with 3,000,000 users caps pushes at 3 per user per week, and a budget of 120,000 rupees at 0.02 rupees per push allows 6,000,000 pushes a week, so the budget binds before the cap (the cap would allow 9,000,000). A randomised 5% holdout test (a sample) suggests the 30% of users with the highest predicted uplift gain 1.5 percentage points of opens per push (incremental open probability per push versus no push) and the other 70% gain 0.3 points, and you assume the gain per push stays constant. Design the targeting system, and compute the extra opens a week from spreading 6,000,000 pushes evenly across users versus sending 3 pushes to every high-uplift user first and spending the rest on the others.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to push-notification ranking and uplift targeting in recommender and growth design material; search snippets only, not opened
**Say this first (1 line):** With a binding budget of 6,000,000 pushes, sending 3 pushes to every high-uplift user first and the rest to others gives 50,400 extra opens a week against 39,600 for an even spread, 10,800 more (27.3%), provided the measured gains hold and do not fade with each extra push.

**Clarifying questions:**
- Is "1.5 percentage points of opens per push" the extra chance a push is opened, compared with no push? I treat it as the incremental open probability per push, which is what uplift means.
- Is an open the goal, or is it a proxy for sessions, orders or retention? Opens can be gamed by urgent wording and do not guarantee value.
- Does the gain per push really stay constant for the second and third push in a week? The prompt says assume so; real fatigue usually lowers it.
- What is the cost of a push that annoys (uninstalls, muted notifications)? It needs a guardrail.
- Were the 5% holdout users randomised and is the uplift estimate on the same users used to pick the top 30%? If so it is optimistic.
- Which messages and hours are allowed per user? Ask the business and ask compliance and legal about consent and contact rules rather than assuming.

**Approach:**
1. Clarify and frame: goal is incremental valuable actions per rupee, with a weekly cap of 3 and a 6,000,000 push budget (120,000 / 0.02), which binds before the 9,000,000 cap (3,000,000 x 3).
2. Metrics and guardrails: incremental opens (or better, incremental sessions) per push versus a no-push control; guardrails: uninstall rate, push opt-out rate, 30-day retention.
3. Data and labels: randomised send versus no-send data (the 5% holdout is a sample), user features, past opens; the label for an uplift model is the outcome in treated versus control, not whether a user opened.
4. Baseline first: send evenly (2 per user a week) or by past open rate. Measure it against a random holdout.
5. Model and trade-offs: an uplift model (two outcome models or a meta-learner) ranking users by predicted gain per push. With constant gains, greedy allocation is optimal: fill the highest gain first up to the cap. 900,000 high users x 3 = 2,700,000 pushes x 0.015 = 40,500 opens; the remaining 3,300,000 pushes go to 2,100,000 others (1.571 each) x 0.003 = 9,900; total 50,400. Even: 6,000,000 pushes, 2 each: 27,000 + 12,600 = 39,600.
6. Evaluation: Qini or uplift-by-decile on a fresh randomised holdout (not the one used to choose the segments); check the 1.5-point estimate with an interval (illustratively about plus or minus 0.55 points at 22,500 users per arm and a 10% base rate).
7. Launch and experiment plan: run the targeted policy against the even policy on random halves of users for 2 to 4 weeks, with a permanent small no-push control to track true uplift.
8. Monitoring, risks and cost: gain per push by push number, opt-outs, drift in who responds, message-quality effects. Retrain monthly. Cost is the 0.02 per push, fixed by the budget; the question is only where to spend it.

Pacing for a 45-minute round (indicative): clarify 5, metrics 5, data and labels 6, baseline 3, model and allocation 11, evaluation 6, launch 4, monitoring and risks 5.

**Metrics:**
- Extra opens per week = sum over users of pushes x gain per push, with gain in opens per push (1.5 points = 0.015).
- Value per push by segment: high 0.015, other 0.003, so the high segment is 5 times as valuable per push.
- Guardrails: opt-out rate, uninstall rate, retention; primary check is incremental, not total, opens.

**Risks:**
- Constant gain per push is an assumption; if the third push has a lower gain, the allocation gain shrinks. If the high-segment gain were 1.0 point, the advantage is 6,300 opens, not 10,800.
- Winner's curse: users chosen for the highest predicted uplift on the same data look better than they are.
- A 5% holdout is a sample; the estimates have sampling error.
- Opens are a proxy; urgent wording can raise opens while hurting retention.
- Opt-outs mean the cap of 3 may be too high for some users.

**What the interviewer scores:**
- Strong: 6,000,000 vs 9,000,000 so the budget binds, then 39,600 vs 50,400. Weak: sends 3 to everyone and overspends.
- Strong: targets on uplift (treatment effect), not on who opens most. Weak: ranks by open rate.
- Strong: raises fatigue, a fresh holdout and guardrails. Weak: trusts constant gain.
- Strong: states the policy as greedy allocation by gain per push under cap and budget. Weak: no allocation logic.

**Example:** (illustrative numbers) 30% of 3,000,000 is 900,000 high-uplift users; 2,100,000 are others. Even: 2 each, 900,000 x 2 x 0.015 = 27,000 and 2,100,000 x 2 x 0.003 = 12,600, total 39,600. Targeted: 2,700,000 x 0.015 = 40,500 and 3,300,000 x 0.003 = 9,900, total 50,400.
- Weak: "Send everyone 3 pushes and measure opens."
- Strong: "The budget buys 6 million pushes, not 9. High-uplift users gain five times more per push, so they get their 3 first. That is about 10,800 more opens than spreading evenly, if the gain holds on the third push, which I would test with a fresh holdout and an opt-out guardrail."

**Code:**
```python
# Q8 notification targeting: illustrative numbers from the prompt
users, cap, budget, price = 3_000_000, 3, 120_000, 0.02
pushes = round(budget / price)
cap_total = users * cap
assert_binds = pushes < cap_total
hi_share, g_hi, g_lo = 0.30, 0.015, 0.003      # opens per push (percentage points / 100)
hi, lo = int(users * hi_share), int(users * (1 - hi_share))
# A: spread evenly
each = pushes / users
even = hi * each * g_hi + lo * each * g_lo
# B: 3 pushes to every high-uplift user first, remainder to the others (under the cap)
hi_push = hi * cap
rest = pushes - hi_push
lo_each = rest / lo
targeted = hi_push * g_hi + rest * g_lo
print(f"pushes {pushes:,} vs cap total {cap_total:,}; budget binds: {assert_binds}")
print(f"high {hi:,}, low {lo:,}; even each {each:.1f}")
print(f"even: high {hi*each*g_hi:,.0f} + low {lo*each*g_lo:,.0f} = {even:,.0f}")
print(f"targeted: high {hi_push*g_hi:,.0f} + low {rest*g_lo:,.0f} = {targeted:,.0f}; low users get {lo_each:.3f} each")
print(f"gain {targeted-even:,.0f} extra opens/week = {targeted/even-1:.1%} more")
# illustrative sampling error on the 1.5-point estimate (assumed 10% base open rate, 22,500 per arm)
import math
n_arm, p = 22_500, 0.10
se = math.sqrt(2 * p * (1 - p) / n_arm)
print(f"illustrative SE of a difference {se*100:.2f} points, 95% half-width {1.96*se*100:.2f}")
# if the true high-uplift gain were 1.0 point instead of 1.5
t2 = hi_push * 0.010 + rest * g_lo
e2 = hi * each * 0.010 + lo * each * g_lo
print(f"if high gain is 1.0 point: targeted {t2:,.0f} vs even {e2:,.0f}, gain {t2-e2:,.0f}")
assert pushes == 6_000_000 and cap_total == 9_000_000 and assert_binds
assert hi == 900_000 and lo == 2_100_000 and each == 2.0
assert round(even) == 39_600 and hi_push == 2_700_000 and rest == 3_300_000
assert round(lo_each, 3) == 1.571 and lo_each < cap
assert round(targeted) == 50_400 and round(targeted - even) == 10_800 and round(targeted / even - 1, 3) == 0.273
assert round(se * 100, 2) == 0.28 and round(1.96 * se * 100, 2) == 0.55 and round(t2 - e2) == 6_300
```

**Output (my run):**
```text
pushes 6,000,000 vs cap total 9,000,000; budget binds: True
high 900,000, low 2,100,000; even each 2.0
even: high 27,000 + low 12,600 = 39,600
targeted: high 40,500 + low 9,900 = 50,400; low users get 1.571 each
gain 10,800 extra opens/week = 27.3% more
illustrative SE of a difference 0.28 points, 95% half-width 0.55
if high gain is 1.0 point: targeted 36,900 vs even 30,600, gain 6,300
```

**Follow-ups:**
- What if gain falls on later pushes? Allocate by marginal gain per push and stop when the marginal gain of a high user falls below the others' first-push gain.
- How do you avoid the biased comparison in a targeted test? Compare against randomised controls within each segment; see Book 6 Part 4 Q55 (an uplift model compared to the untreated rest) and Book 6 Part 1 Q35 (push cap of three per day, metrics).

**Common mistakes:** Targeting by predicted open rate rather than uplift. Forgetting the budget binds before the cap. Reporting total opens, not extra opens versus control. Choosing segments and measuring them on the same holdout. Ignoring opt-outs.

### Q9 ⭐⭐⭐ 🟡 Content moderation: A short-video platform receives 2,000,000 uploads a day and 0.4% violate policy (a measured estimate from an audit of a random sample of 50,000 uploads). Human reviewers can handle at most 12,000 flagged items a day, and policy asks for at least 90% of violating uploads to be caught. Design the moderation pipeline, and compute the violating uploads a day, the true violations you must flag and the minimum precision of the flagged queue.
**Asked at:** Moderation and ads design material (a TryExponent Reddit ML engineer guide reporting an ad targeting or ad ranking design prompt, PracHub question banks with a short-video content-moderation prompt, an Interview Query Xandr guide); prep-site material; notification ranking had no clear page; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** About 2,000,000 x 0.4% = 8,000 uploads a day violate policy, catching 90% means flagging 7,200 of them, and with 12,000 review slots the queue needs at least 7,200 / 12,000 = 60% precision, but the 0.4% is a sample, and at its upper bound the requirement is about 68%.

**Clarifying questions:**
- Does "caught" mean removed before anyone sees it, or within some hours? It decides whether human review can sit in the path or only after publishing.
- Is the 90% a policy goal for all violations or by severity? Severe categories need near-total recall; mild ones can wait.
- How was the 0.4% measured: a random audit of 50,000 uploads, which is 200 violations? That is a sample with an interval, not a fixed rate.
- Do reviewers also make mistakes, and what is their agreement rate? Reviewer error limits the true labels.
- Can very confident cases be actioned automatically, and what appeal path exists? It frees reviewer capacity but raises the cost of errors.
- What are the policy and legal obligations? Ask policy, trust and safety and legal; I do not assume them.

**Approach:**
1. Clarify and frame: policy categories, severity tiers, "caught" definition, reviewer capacity of 12,000 a day, an appeal path.
2. Metrics and guardrails: recall of violations (the 90% goal), precision of the review queue, time to action. Guardrails: wrongful-removal rate (appeals upheld), reviewer agreement, latency of upload.
3. Data and labels: random audit labels (unbiased, used to estimate the base rate and recall), reviewer decisions from the queue (biased to what the model flagged), user reports. A fresh random sample each week is the only unbiased recall measure.
4. Baseline first: hash matching of known bad content plus keyword and rule lists, then user reports as a queue; record what share of violations this catches.
5. Model and trade-offs: a cheap multimodal classifier scores every upload; very high scores are actioned automatically, a middle band goes to the human queue, low scores pass. Sizing: violations 8,000; must flag 7,200; queue 12,000; minimum precision 60%. Interval check: 200 of 50,000 gives 0.345% to 0.455%, that is 6,893 to 9,107 violations a day, so the minimum precision ranges from 51.7% to 68.3%.
6. Evaluation: precision-recall curve on the audit sample, pick the threshold where recall is at or above 90% with queue at or below 12,000; per-category recall; compare reviewers with a gold set. Beware that recall computed only on reviewed items is biased (Book 6 reference below).
7. Launch and experiment plan: shadow classifier, then queue ordering by score, then automation for the top band after human audit; stagger by category; keep a random 0.5% slice always reviewed to track recall.
8. Monitoring, risks and cost: weekly random audit, queue backlog, appeal-overturn rate, adversarial drift (creators evade). Retrain on newly labelled items; the cost is reviewer time; precision gains cut it directly.

Pacing for a 45-minute round (indicative): clarify 5, metrics 6, data and labels 7, baseline 3, model and sizing 9, evaluation 6, launch 4, monitoring and risks 5.

**Metrics:**
- Violating uploads per day = uploads x violation rate = 2,000,000 x 0.004 = 8,000 (a measured estimate from a random sample of 50,000).
- True violations to flag = 8,000 x 90% = 7,200. Minimum queue precision = true violations flagged / queue size = 7,200 / 12,000 = 60%.
- Recall = true violations flagged / all violations; precision = true violations / flagged items.
- Guardrails: appeals upheld per 1,000 removals, queue age, reviewer agreement.

**Risks:**
- The base rate is a sample: 0.4% has an approximate 95% interval of 0.345% to 0.455%.
- Recall measured only on reviewed items looks fine while unseen violations pile up.
- Capacity is a ceiling: if violations rise 25% (10,000), the same 90% needs 9,000 true flags, so precision of at least 75% at 12,000.
- Automated actions at high scores create wrongful removals; they need an appeal route.
- Adversarial users change content once detection works.

**What the interviewer scores:**
- Strong: 8,000, 7,200, 60% computed, and notes the 0.4% is a sample with an interval. Weak: treats 0.4% as exact.
- Strong: tiers (auto, human, pass) and an unbiased audit slice to measure recall. Weak: reviews everything or trusts reviewed-only recall.
- Strong: separates the precision requirement from the model's actual precision and picks the threshold from the curve. Weak: "build a good classifier".
- Strong: guardrails for wrongful removals. Weak: only catches violations.

**Example:** (illustrative numbers) 2,000,000 uploads x 0.4% = 8,000 violating. 90% of 8,000 is 7,200 true flags. 7,200 / 12,000 = 60% minimum precision. If the true rate is 0.455%, there are 9,107 violations and the minimum is 68.3%.
- Weak: "I would train a classifier with high accuracy."
- Strong: "I need to flag 7,200 true violations in 12,000 slots, so precision of at least 60%, and 68% if the audit sample underestimated the base rate. I would measure recall with a random slice, auto-action only the very confident scores, and check where the model sits on the curve."

**Code:**
```python
import math
# Q9 moderation: illustrative numbers from the prompt
uploads, rate, audit_n = 2_000_000, 0.004, 50_000
review_cap, recall_goal = 12_000, 0.90
viol = uploads * rate
must_flag = viol * recall_goal
min_prec = must_flag / review_cap
print(f"violating/day {viol:,.0f}; must flag {must_flag:,.0f}; min precision of queue {min_prec:.0%}")
# the 0.4% is a sample estimate: 200 violations in 50,000 audited
k = round(audit_n * rate)
se = math.sqrt(rate * (1 - rate) / audit_n)
lo_r, hi_r = rate - 1.96 * se, rate + 1.96 * se
print(f"audit violations {k}; 95% interval {lo_r:.3%} to {hi_r:.3%}")
for lab, r in (("low", lo_r), ("base", rate), ("high", hi_r)):
    v = uploads * r
    print(f"{lab}: {v:,.0f} violations, flag {v*recall_goal:,.0f}, min precision {v*recall_goal/review_cap:.1%}")
# queue size when precision is lower: how many true violations reach reviewers
for p in (0.5, 0.6):
    tp = review_cap * p
    print(f"precision {p:.0%}: {tp:,.0f} true found, recall {tp/viol:.1%}")
max_p = viol / review_cap
print(f"a 12,000 queue that caught every violation would have precision {max_p:.1%}")
assert viol == 8_000 and must_flag == 7_200 and min_prec == 0.60
assert k == 200 and round(lo_r, 5) == 0.00345 and round(hi_r, 5) == 0.00455
assert round(uploads * lo_r * 0.9 / review_cap, 3) == 0.517 and round(uploads * hi_r * 0.9 / review_cap, 3) == 0.683
assert round(review_cap * 0.5 / viol, 3) == 0.75 and round(review_cap * 0.6 / viol, 2) == 0.90
assert round(max_p, 3) == 0.667
```

**Output (my run):**
```text
violating/day 8,000; must flag 7,200; min precision of queue 60%
audit violations 200; 95% interval 0.345% to 0.455%
low: 6,893 violations, flag 6,204, min precision 51.7%
base: 8,000 violations, flag 7,200, min precision 60.0%
high: 9,107 violations, flag 8,196, min precision 68.3%
precision 50%: 6,000 true found, recall 75.0%
precision 60%: 7,200 true found, recall 90.0%
a 12,000 queue that caught every violation would have precision 66.7%
```

**Follow-ups:**
- What if reviewers are fewer? Either lower the recall goal for low-severity categories or automate more of the top band; show the trade-off curve.
- How do you measure recall honestly? A random slice of all uploads, human-labelled; see Book 6 Part 2 Q38 (moderation labels only for items a reviewer sees) and Book 2 Part 12 Q24 (design a content moderation pipeline).

**Common mistakes:** Treating the audit-sample rate as exact. Reporting recall on reviewed items only. Using accuracy at a 0.4% base rate. No appeal path. Forgetting that the queue limit couples precision and recall.

### Q10 ⭐⭐⭐ 🟡 Credit scoring: A digital lender disburses 3,000 loans a month and wants a first scorecard for thin-file applicants within 10 weeks, and all 3,000 monthly loans are thin-file. Default means 90 days past due, which can only be observed 4 months after disbursal, and the last 12 months of approved loans (36,000) include the most recent 4 months that are still unlabelled. Design the scorecard end to end, and compute the labelled loans available and the expected number of defaulters if the default rate on matured loans is 7% (a measured average), and say what compliance must confirm.
**Asked at:** Churn and credit design material (a DataTalks.Club guide saying the question is what action follows a churn prediction, Dataford end-to-end churn pipeline prompts, Interview Query credit-risk company guides from Credit Karma, ZestFinance and TransUnion); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Of the 36,000 loans in the last 12 months only 24,000 are old enough to have a 90-day-past-due label, giving about 1,680 expected defaulters at 7%, enough for a simple scorecard, but the labels cover only approved loans and the first outcomes on new decisions take about 4 months, so I would plan a pilot rather than a full launch in 10 weeks.

**Clarifying questions:**
- What exactly is the label: 90 days past due within a fixed 4-month window, or ever? A fixed window means loans from 4 months ago are not fully comparable with older ones.
- What does "thin-file" mean here, and are all 3,000 monthly loans thin-file? It decides how many rows are relevant.
- How were past applicants approved and which were rejected? Labels exist only for approved loans (selection bias).
- Which features may be used (device, phone data, alternative data) and which are barred? Ask compliance and legal; do not assume.
- What is the decision: approve or decline, a limit, a price? It sets the cost matrix.
- What explanation must accompany a decline? Ask compliance what must be provided and what validation is needed before use.

**Approach:**
1. Clarify and frame: decision (approve, decline, refer), the 10-week deadline, label definition, who must approve the model.
2. Metrics and guardrails: ranking (AUC or KS) on matured loans, calibration (predicted versus actual default by band), and business value; guardrails: approval rate, stability of scores by segment, fairness checks specified by compliance.
3. Data and labels: loans disbursed 12 to 4 months ago are labelled: 3,000 x 8 = 24,000; the most recent 4 months, 12,000 loans, are excluded from training and used later. Expected defaulters 24,000 x 7% = 1,680 (about 1,603 to 1,757 at a 95% sampling interval). Reject inference is a risk: declined applicants have no outcome.
4. Baseline first: the current policy rules or a simple points table on 5 to 8 features; the scorecard must beat it on an out-of-time sample.
5. Model and trade-offs: a regularised logistic regression with binned features (a scorecard) over a boosted tree, because of explainability, monotonic behaviour and easy validation; a boosted tree can serve as a benchmark. About 1,680 defaulters supports a modest number of features; avoid hundreds.
6. Evaluation: out-of-time split, for example train on the oldest 5 matured months (15,000 loans, about 1,050 defaulters) and validate on the newest 3 matured months (9,000 loans, about 630 defaulters); report intervals; check calibration by band; bootstrap the AUC.
7. Launch and experiment plan: 10 weeks: 2 for label definition and data audit, 2 baseline and features, 3 model and validation, 3 governance and pilot setup. Then a champion-challenger pilot (score in shadow, decide a small share with the scorecard, with limits), because outcomes for new decisions arrive about 4 months later.
8. Monitoring, risks and cost: score distribution and population stability monthly, early-delinquency (30 days past due) as a leading proxy labelled as a proxy, default by band at maturity; recalibrate quarterly. Cost is analyst time plus data fees; the cost of a bad loan dominates.

Pacing for a 45-minute round (indicative): clarify 5, metrics 5, data and labels 9, baseline 3, model 7, evaluation 6, launch 5, monitoring and risks 5.

**Metrics:**
- Labelled loans = monthly loans x matured months = 3,000 x (12 - 4) = 24,000; unlabelled = 3,000 x 4 = 12,000.
- Expected defaulters = labelled loans x default rate on matured loans = 24,000 x 7% = 1,680 (the 7% is a measured average, so the count is an estimate).
- KS or AUC for rank ordering; calibration = mean predicted default / observed default per score band.
- Business: approve when expected loss is below margin; break-even probability of default = margin / (margin + loss given default), illustratively 800 / 10,800 = 7.41%. Guardrail: approval rate and stability index.

**Risks:**
- Selection bias: only approved loans have outcomes, so the scorecard learns on a filtered population.
- Label maturity: a 4-month lag means any score deployed now is validated on old behaviour.
- Population drift between the training months and the new applicants.
- A small defaulter count (1,680, only about 630 in the validation slice) makes the metrics noisy.
- Compliance: features, explanation and fairness requirements; ask compliance and legal, and make no claims from memory.

**What the interviewer scores:**
- Strong: 24,000 labelled and 1,680 defaulters, with the reason 12,000 are excluded. Weak: trains on all 36,000 with unlabelled loans counted as non-default.
- Strong: raises selection bias and a time-based validation. Weak: random split.
- Strong: a baseline, an explainable model and a pilot with a champion-challenger. Weak: "use XGBoost".
- Strong: defers regulatory points to compliance and legal. Weak: asserts specific rules.

**Example:** (illustrative numbers) 3,000 loans a month for 12 months is 36,000. The newest 4 months (12,000) are not yet 4 months old, so the label is unknown. Labelled: 24,000. At 7%, defaulters = 1,680; training on the oldest 15,000 leaves about 630 defaulters for the newest 9,000.
- Weak: "36,000 loans, 7% default, so I have 2,520 defaulters and will train a deep model."
- Strong: "Only 24,000 are matured, so about 1,680 defaulters. I would train a binned logistic scorecard on the oldest months, validate out of time, check calibration, and pilot a small share because new outcomes take four months. I would ask compliance what features and explanations are allowed."

**Code:**
```python
import math
# Q10 credit scoring: illustrative numbers from the prompt
per_month, months, unlabelled_months, dr = 3_000, 12, 4, 0.07
total = per_month * months
labelled = per_month * (months - unlabelled_months)
unl = per_month * unlabelled_months
defaulters = labelled * dr
se = math.sqrt(dr * (1 - dr) / labelled)
print(f"total {total:,}; labelled {labelled:,}; unlabelled {unl:,}; defaulters {defaulters:,.0f}")
print(f"default rate {dr:.0%} +/- {1.96*se*100:.2f} pts (95%) -> defaulters {labelled*(dr-1.96*se):,.0f} to {labelled*(dr+1.96*se):,.0f}")
# out-of-time split: oldest 5 matured months train, newest 3 matured months validate
train, valid = per_month * 5, per_month * 3
print(f"train {train:,} (~{train*dr:,.0f} defaulters), validate {valid:,} (~{valid*dr:,.0f})")
# an expected-value cut-off: loss given default vs margin on a good loan (illustrative)
lgd, margin = 10_000, 800
be_pd = margin / (margin + lgd)
print(f"approve if PD below {be_pd:.2%} (illustrative loss 10,000, margin 800)")
weeks = {"label definition+data audit": 2, "baseline+features": 2, "model+validation": 3, "governance+pilot setup": 3}
print(weeks, sum(weeks.values()))
print(f"first outcomes on new loans arrive {4} months (~17 weeks) after launch, beyond the 10-week plan")
assert total == 36_000 and labelled == 24_000 and unl == 12_000 and round(defaulters) == 1_680
assert round(1.96 * se * 100, 2) == 0.32
assert train == 15_000 and valid == 9_000 and round(valid * dr) == 630
assert round(be_pd, 4) == 0.0741 and sum(weeks.values()) == 10
```

**Output (my run):**
```text
total 36,000; labelled 24,000; unlabelled 12,000; defaulters 1,680
default rate 7% +/- 0.32 pts (95%) -> defaulters 1,603 to 1,757
train 15,000 (~1,050 defaulters), validate 9,000 (~630)
approve if PD below 7.41% (illustrative loss 10,000, margin 800)
{'label definition+data audit': 2, 'baseline+features': 2, 'model+validation': 3, 'governance+pilot setup': 3} 10
first outcomes on new loans arrive 4 months (~17 weeks) after launch, beyond the 10-week plan
```

**Follow-ups:**
- How would you handle unlabelled recent loans? Do not count them as good; use them for monitoring and add early-delinquency proxies only with a clear label.
- How do you handle approval selection? See Book 6 Part 2 Q13 (loan-approval model trained on past decisions), Book 4 Part 8 Q33 (retraining pitfalls and feedback loops) and Book 6 Part 9 Q6 (thin-file lender scenario).

**Common mistakes:** Treating unlabelled recent loans as non-defaults. Using all 36,000. A random split on time-ordered loans. Claiming regulatory requirements from memory. Reporting AUC without calibration.
