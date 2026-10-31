# Book 6 — Part 10: Design a Solution End-to-End (Open Scenarios)

**Topic:** Open-ended "design an ML or GenAI solution for X" prompts for Data Scientist, ML Engineer and GenAI Engineer loops, where the candidate frames the problem and walks from goal and users through metrics and guardrails, data and labels, baseline, model, offline and online evaluation, launch, monitoring and retraining, risks, cost, latency, team and timeline. Themes: feed ranking, search ranking and retrieval, fraud detection (real-time, delayed labels, graph features), churn and retention, demand forecasting and stocking, dynamic pricing, content moderation, customer-support RAG, ETA prediction, personalisation and cold start, anomaly detection and predictive maintenance, credit scoring, notification targeting, ad ranking, resume and job matching, document processing, voice and vision use cases, Indian-market constraints (multilingual and Hinglish text, UPI-style payments, low bandwidth, cash-on-delivery, tier-2 and tier-3 cities), healthcare triage assist, agentic workflows, LLM cost design, a data-quality platform, an MLOps platform, an experimentation platform and team planning.

**Target:** 40  |  **Actual:** 40 (⭐⭐⭐ 14, ⭐⭐ 17, ⭐ 9)  |  **Date:** 2026-10-31  |  **Status:** Complete (answers merged, checked, reviewed)

**Scope note:** this part is the end-to-end design angle: each prompt gives a business context and at least one quantitative constraint (requests per second and a latency budget, a labelling or cost budget, a launch deadline, a review capacity), so a strong answer includes a sizing or trade-off calculation that can be reproduced in code. Detailed metric, degradation, imbalance, experiment, business-case, stakeholder, GenAI, MLOps-incident and domain scenarios belong to Book 6 Parts 1 to 9; Wave B answers should cross-reference those only by checked headings. All numbers in the prompts are invented illustrative numbers, not data from any company; money is in rupees or one unnamed currency unit, and prices are illustrative, not vendor prices. Every percentage names its base, rates are labelled as measured samples or projections, assumptions the answer needs (peak factors, utilisation, headroom, unit conventions) are stated in the prompt, and every arithmetic claim is checked in scratch/B6P10_wavea/qs.py. Anything touching law, regulation or clinical rules is framed as a question for compliance, and no legal or regulatory claim is made as fact. Stars: 3 means reported in most loops, 2 regular, 1 senior or niche; they are editorial judgements.

**Evidence limits:** WebFetch was unavailable, so no page was opened; every source is a WebSearch snippet or result summary only (see research_notes/Book6_Part10_sources.md). Searches returned ML system-design prep guides and question banks (Educative, DesignGurus, PracHub, Codemia, Dataford, techinterview.org), a few company-tagged prompts, and Indian-market vendor and blog pages. None tied a prompt to a verified employer round, so 'Asked at' lines name guide families only ('commonly reported in public guides'); prompts marked editor-designed have no located public page for the exact framing. Search coverage was thin for notification targeting, resume matching, document extraction, healthcare triage, vernacular search and low-bandwidth design. Star counts and difficulty tags are editorial. No salary figures appear anywhere in this part.

---

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
- The 1.4x rule means 420 rps; a 60% utilisation target would instead give 500 rps and 5 instances, so I state which rule I use.

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

**Common mistakes:** Sizing on the average 58 rps instead of the peak. Dividing by 0.6 when the rule is 1.4 times the peak, without saying so. Optimising accuracy on a 0.05% base rate. No fallback when the model is down. Training on unmatured labels.

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
- Are the 4,000 input and 300 output tokens summed over all turns of a chat? The prompt says per chat; I would still check how many turns that is, because history is resent each turn.
- The budget is to the first token. A 300-token reply at an assumed 60 tokens per second takes 5 seconds on its own, so the full reply cannot fit in 4 seconds; I would confirm streaming is allowed.
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
- Do orders outside the lunch window overlap the peak? The prompt says to ignore them, so I do, and I name the effect as a caveat.
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
- Only the 20% peak arrivals are counted, as instructed. If background orders continued at 320,000 / 79,200 s = 4.04 per second, in flight would be about 31,800 and total load about 1,076 rps (illustrative).
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
- The gain is the incremental open probability per push versus no push. Was it estimated on the same holdout used to pick the top 30%? If so it is optimistic.
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
- All 3,000 monthly loans are thin-file and approved loans, so labels exist only for approved applicants; how were declined applicants handled? It drives selection bias.
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

### Q11 ⭐⭐⭐ 🟡 Ad ranking: An ad server must rank ads on 50,000 requests per second at peak inside an 80 ms budget, and targeting leaves 300 candidate ads per request. A prefilter keeps 40 of them for the click model, and one scoring server runs 50,000 click predictions per second at full load within the latency budget (size servers at full load, with no headroom, and say separately how much headroom you would add). Design the ad ranking and auction system including calibration, and compute the predictions per second and servers needed with and without the prefilter.
**Asked at:** Moderation and ads design material (a TryExponent Reddit ML engineer guide reporting an ad targeting or ad ranking design prompt, PracHub question banks with a short-video content-moderation prompt, an Interview Query Xandr guide); prep-site material; notification ranking had no clear page; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Scoring all 300 ads is 15,000,000 predictions a second (300 servers at full load), a 40-ad prefilter makes it 2,000,000 a second (40 servers, about 58 with 30% headroom), so I would design retrieval, prefilter, calibrated click model and auction as four stages and judge the prefilter by recall of the ads the full model would have picked.

**Clarifying questions:**
- Is the 50,000 requests per second the fleet peak, and is the 80 ms the whole ad path (retrieval, scoring, auction, response)? It sets how many milliseconds the click model really gets.
- Which auction (first or second price) and which objective (clicks, conversions, revenue)? Calibration matters most when bids are multiplied by predicted rates.
- Is the 50,000 predictions per second per server measured with the production model and batch size? The question ties it to the latency budget; I would still verify it by load test.
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

### Q12 ⭐⭐⭐ 🔴 Fraud with delayed labels: A card-not-present fraud model must be retrained monthly and launched in 12 weeks, but chargebacks arrive late: 60% of eventual chargebacks are in by day 30 and 90% by day 90 (a measured profile). True fraud is a steady 0.2% of transactions (an assumption). Design the training, evaluation and monitoring plan, and compute the fraud rate that a window whose transactions are all 30 days old and one whose transactions are all 90 days old appear to have.
**Asked at:** Fraud-detection design material (an Educative fraud-detection mock interview, a PracHub real-time payment fraud prompt with a 50 ms budget and prep guides that call fraud the prompt where probabilities, thresholds and feature freshness must be discussed); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** A 30-day-old window shows 0.12% fraud (60% of the true 0.2%) and a 90-day-old window shows 0.18% (90%), so I would never read recent label rates as truth: I would correct for maturity, train on the freshest window that is mostly matured, and use early proxy signals plus rules to cover the gap.

**Clarifying questions:**
- Is the 60% and 90% profile stable across merchants, countries and attack types? A single maturity curve is the whole basis of any correction.
- Besides chargebacks, are there faster labels (customer disputes, issuer confirmations, manual reviews)? They let me react before day 30.
- What do we do on a flagged transaction (block, step-up check, review)? Blocked fraud never produces a chargeback, so labels are censored by our own decisions.
- Is the 0.2% a measured rate or a planning figure? The question gives it as an assumption; I would check it on mature cohorts.
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

### Q13 ⭐⭐⭐ 🔴 Agentic workflow: A retailer wants an agent to resolve refund requests end to end for 20,000 requests a day. A typical run makes 4 sequential LLM steps of 1.5 seconds each and 3 sequential tool calls of 0.4 seconds each (assume no retries), and the chat budget is 12 seconds at the 95th percentile. Design the agent, its approval rules for refunds above 2,000 rupees and its evaluation, and compute the typical (mean) latency and the slack left against the budget, and say what the 95th percentile needs.
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

### Q14 ⭐⭐⭐ 🔴 Multilingual voice assistant: A bank's voice bot takes 100,000 calls a day, 60% of them inside an 8-hour window (assume evenly spread), and a call lasts 3 minutes on average. One streaming speech-and-language server holds 25 concurrent calls, and the budget per spoken reply is 1.5 seconds. Design the assistant for Hindi, Tamil and mixed-language callers, and use Little's law to compute mean concurrent calls in the window and the servers needed at full load.
**Asked at:** Indian-market material (a Let's Data Science / NPCI item on AI for UPI fraud and multilingual voice, an Elastic and Sarvam multilingual voice-agent blog, a SquadStack voice-bot page on noise and accents, Razorpay, Delhivery and Shiprocket pages on cash-on-delivery return-to-origin risk scoring, a Blinkit candidate report of a delivery-time debugging case); vendor and blog material, no confirmed interview round for these exact designs; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Little's law gives 60,000 calls over 8 hours = 2.08 calls a second x 180 seconds = 375 mean concurrent calls, which is 15 servers at full load, but I would plan about 18 to 22 because arrivals are random and the evenly-spread assumption hides a real peak.

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

### Q18 ⭐⭐ 🟢 Anomaly detection for operations: An operations team monitors 20,000 metrics at 1-minute resolution, and the on-call engineer can triage at most 15 false alerts a day. Design the anomaly detection and alerting system, and compute the data points a day and the largest false-alert probability per data point that keeps expected false alerts within 15 a day, and say how grouping alerts would change the answer.
**Asked at:** Operations and platform design material (a Codemia anomaly-detection pipeline prompt attributed to ServiceNow, Codemia A/B-testing platform prompts attributed to a DoorDash onsite, a PracHub feature-store data-quality and backfill prompt attributed to a Faire onsite, datadriven.io and techinterview.org MLOps guides); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 20,000 metrics x 1,440 minutes = 28,800,000 points a day, so 15 false alerts a day means a false-alert probability of at most 15 / 28,800,000 = 5.2 in ten million per point; that is a very strict threshold, so I would alert on persistent, grouped, business-relevant deviations, not on single points.

**Clarifying questions:**
- What does a "false alert" mean to on-call: a spike that self-heals, a real anomaly nobody needs to act on, or noise? Only actionable alerts count against the 15.
- Which metrics matter most (customer-facing, revenue, errors) and which are noise? Tiering lets the strict budget go to the right ones.
- Are metrics seasonal (daily and weekly cycles, deploys, campaigns)? Seasonality is the main source of false alerts.
- Are metrics correlated (one outage moves hundreds)? It decides how alerts should be grouped.
- Is there labelled incident history? Without it I can only estimate false alerts by replay and on-call feedback.

**Approach:**
1. Clarify and frame. Goal: catch incidents that need a human, within 15 false alerts a day, across 20,000 metrics. Separate detection (score each point) from alerting (decide who is paged).
2. Metrics and guardrails. Precision of pages (actionable pages / pages), recall of known incidents, time to detect, false pages per day. Guardrail: the 15 a day budget and missed severe incidents.
3. Data and labels. Collect past incidents, on-call acknowledgements and "not actionable" marks. Few metrics have labels, so evaluate on a sample of important metrics and by replay of history.
4. Baseline first. Static thresholds plus a same-hour-last-week comparison with robust scale (median and median absolute deviation). Measure false pages by replay.
5. Model and trade-offs. Per-metric forecast with seasonality, residual scoring, a persistence rule, then grouping by service or time. Budget maths: 28,800,000 points, so a per-point false probability of 5.2e-7, roughly a 4.9 sigma Gaussian threshold (see the code); real residuals have heavier tails and autocorrelation, so I would calibrate thresholds on history rather than trust the Gaussian. Trade-off: stricter thresholds cut false pages but delay or miss small real anomalies.
6. Evaluation. Offline replay on 3 to 6 months: false pages per day, recall of past incidents, detection delay. Online: shadow alerts to a channel before paging, then page only the tiered top metrics.
7. Launch and experiment plan. Shadow for 2 to 4 weeks, tune thresholds per tier, page on tier 1 first. Review every false page weekly.
8. Monitoring, retraining and risks. Track false pages per day against 15, refit forecasts on schedule, add holiday and deploy calendars, suppress alerts during known maintenance.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 5, 5, 11, 6, 5, 5.

**Metrics:**
- Points a day = metrics x points per metric = 20,000 x 1,440 = 28,800,000.
- Maximum per-point false-alert probability = allowed false alerts / points = 15 / 28,800,000 = 5.2083e-7 (this is expected value, which needs no independence).
- Precision of pages = actionable pages / all pages; recall = incidents caught / incidents that occurred.
- Detection delay = time from incident start to page; false pages per day.
- Guardrail: false pages per day under 15.

**Risks:**
- Alert fatigue: if on-call stops trusting pages, real incidents get missed.
- Autocorrelation and bursts: false alerts arrive in clusters (one noisy hour), so the day-to-day count varies more than the average suggests.
- Seasonality and deploys cause predictable false positives.
- A very strict threshold may miss small but real degradations.
- Correlated failures produce alert storms; grouping is essential.

**What the interviewer scores:**
- Strong: 28.8 million points and 5.2e-7 per point, noticing how strict it is.
- Strong: persistence rules, tiering, grouping, seasonal baselines, and replay evaluation.
- Strong: says grouping raises the allowed per-point probability but the budget is really per page.
- Weak: "train an autoencoder on all metrics" with no alert budget or evaluation.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "Flag anything beyond 3 standard deviations."
- Strong: "20,000 metrics a minute is 28.8 million points a day, so to stay at 15 false alerts the per-point false rate must be near 5 in ten million. Three sigma would page thousands of times, so I would use seasonal forecasts, require persistence over several minutes, group by service so one outage is one page, tier the metrics, and tune on replayed history with on-call feedback."

**Code:**
```python
import math
from statistics import NormalDist
import numpy as np

# Prompt arithmetic
metrics, per_day, budget = 20_000, 24 * 60, 15
points = metrics * per_day
p_max = budget / points
assert points == 28_800_000 and abs(p_max - 5.2083e-7) < 1e-10
print("data points a day:", points, "| max false-alert probability per point:", f"{p_max:.4e}")

# What threshold does that imply for a Gaussian residual? one-sided z
z = NormalDist().inv_cdf(1 - p_max)
print("one-sided z threshold for a Gaussian residual:", round(z, 2))
assert 4.8 < z < 5.0

# Check by simulation (chunked): count exceedances of z over one simulated day of independent Gaussian points
rng = np.random.default_rng(18)
hits = 0
for _ in range(29):
    hits += int((rng.standard_normal(1_000_000)[:] > z).sum())
print("simulated false alerts over 29,000,000 independent points (expected about 15):", hits)
assert 3 <= hits <= 35

# Persistence rule: alert only if k consecutive points exceed a looser per-point threshold (independence assumed, so optimistic)
q = 1e-3
for k in (1, 2, 3):
    print(f"per-point tail {q} needed k={k} in a row -> false chance per point {q ** k:.1e}; alerts/day {points * q ** k:.3g}")
assert points * q ** 3 < budget < points * q ** 2
# Grouping: if correlated metrics fire together and count as one alert
groups_of = 20
print("if 20 metrics fail together as one alert, budget per group-event:", budget, "alerts -> point-level budget can be up to", budget * groups_of / points)
assert abs(budget * groups_of / points - 1.0417e-5) < 1e-8
p3 = 1 - NormalDist().cdf(3)
print("3-sigma one-sided tail:", round(p3, 5), "-> false alerts a day:", round(points * p3))
assert round(p3, 5) == 0.00135 and 38_800 < points * p3 < 38_900
```

**Output (my run):**
```
data points a day: 28800000 | max false-alert probability per point: 5.2083e-07
one-sided z threshold for a Gaussian residual: 4.88
simulated false alerts over 29,000,000 independent points (expected about 15): 16
per-point tail 0.001 needed k=1 in a row -> false chance per point 1.0e-03; alerts/day 2.88e+04
per-point tail 0.001 needed k=2 in a row -> false chance per point 1.0e-06; alerts/day 28.8
per-point tail 0.001 needed k=3 in a row -> false chance per point 1.0e-09; alerts/day 0.0288
if 20 metrics fail together as one alert, budget per group-event: 15 alerts -> point-level budget can be up to 1.0416666666666666e-05
3-sigma one-sided tail: 0.00135 -> false alerts a day: 38877
```

**Follow-ups:**
- How does grouping change the answer? The budget applies to pages, not points; if 20 correlated metrics become one page, the per-point probability can be about 20 times higher for the same page count (1.04e-5), but only if they really fail together and are grouped reliably.
- What does a 3-sigma rule cost? A one-sided 3-sigma tail is about 0.00135 per point, which is about 38,900 false alerts a day on 28.8 million independent Gaussian points, far above 15.
- How do you handle new metrics? Start in shadow with a longer warm-up and a looser tier until history exists.

**Common mistakes:**
- Forgetting to multiply by 1,440 points per metric per day.
- Assuming independent Gaussian noise and trusting the resulting z threshold.
- Counting alerts per metric instead of per page.
- Tuning thresholds on only the incidents, with no replay for false alerts.

### Q19 ⭐⭐ 🟡 Low-bandwidth personalisation: A marketplace app in tier-2 and tier-3 cities sees many sessions on connections that deliver about 400 kilobits per second, and the home screen must load in 3 seconds. Take 1 kilobyte as 1,000 bytes and ignore latency overheads. Design a personalised home feed under this constraint, and compute the upper bound on the payload in kilobytes and how you would shrink it.
**Asked at:** Indian-market material (a Let's Data Science / NPCI item on AI for UPI fraud and multilingual voice, an Elastic and Sarvam multilingual voice-agent blog, a SquadStack voice-bot page on noise and accents, Razorpay, Delhivery and Shiprocket pages on cash-on-delivery return-to-origin risk scoring, a Blinkit candidate report of a delivery-time debugging case); vendor and blog material, no confirmed interview round for these exact designs; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 400 kilobits a second for 3 seconds is 1,200 kilobits = 150 kilobytes, but that is a ceiling with zero overhead, so I would budget about 50 to 75 kB for the first screen, send ranked ids and small text first, and fetch images lazily.

**Clarifying questions:**
- Is "about 400 kilobits per second" the median or a low percentile? If it is the median, half of sessions are slower, so I design for a lower percentile.
- Does "load in 3 seconds" mean first usable content or everything? I would define it as the first screen of ranked items.
- What is cached on the device (app shell, previous feed)? Cached content does not count against the payload.
- Which features need fresh data (price, stock) versus can be a few hours old? It decides what to precompute.
- What share of sessions are new users with no history? They need a non-personalised fallback.

**Approach:**
1. Clarify and frame. Goal: a personalised first screen that is usable in 3 seconds on a slow link. Constraint first: payload ceiling 150 kB, realistic budget 50 to 75 kB.
2. Metrics and guardrails. Time to first usable screen (p75 and p90 on slow links), click and add-to-cart rate, bounce rate, bytes per session. Guardrail: no loss in conversion on fast links.
3. Data and labels. Click, add-to-cart and purchase logs, with network type and bandwidth recorded, so slow-link users can be evaluated separately. Labels from slow users are biased (they see fewer items), so I would check exposure.
4. Baseline first. A popularity-by-city feed cached on the device, then a lightly personalised re-order of the cached list. Measure load time and conversion.
5. Model and trade-offs. Rank on the server with a small model; send only ids, short text and tiny thumbnails; compress with gzip or similar; use a smaller image format and low-resolution placeholders; page the feed 6 items at a time. The trade-off is richness versus speed: each extra 10 kB costs 0.2 s at 400 kbps (see the code). Optionally rank on-device from cached candidates to avoid a round trip.
6. Evaluation. Offline ranking metrics as usual, plus byte and latency accounting per response. Online: A/B test with analysis split by connection speed.
7. Launch and experiment plan. Ship the byte-budgeted feed to slow-link sessions first, since they gain most; then everyone if fast-link conversion holds.
8. Monitoring, retraining and risks. Monitor payload size per response (alert on regressions in CI and in production), time to first screen by network class, conversion by network class.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 5, 5, 10, 7, 5, 5.

**Metrics:**
- Payload ceiling (kB) = bit rate (kbit/s) x seconds / 8 = 400 x 3 / 8 = 150 kB, with 1 kB = 1,000 bytes and no overhead.
- Time to first usable screen = time from tap to first ranked items visible; report p75 and p90 by network class.
- Bytes per session; conversion rate = orders / sessions, by network class.
- Guardrails: fast-link conversion, error rate, stale price or stock complaints.

**Risks:**
- The 150 kB is an upper bound; handshakes, retries and slower phases shrink it (1 second of overhead leaves 100 kB; half the rate leaves 75 kB).
- Averages hide slow tails; many users are slower than the 400 kbps figure.
- Heavy personalisation features can bloat payloads silently.
- Stale cached data (prices, stock) shown as current.
- Collecting device and network data: ask compliance and legal about consent and privacy.

**What the interviewer scores:**
- Strong: 150 kB as a ceiling, then a smaller realistic budget and a plan to hit it.
- Strong: ids first, lazy images, caching, paging, on-device re-ranking.
- Strong: evaluates by network class, not only overall.
- Weak: computes 150 kB and then designs a rich, image-heavy feed anyway.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "Use a deep model to personalise and send 40 big product images."
- Strong: "400 kilobits for 3 seconds is 150 kilobytes at most. After connection overhead and slower moments I would budget 60 to 75 kB: ranked ids, short compressed text and small thumbnails for the first 6 items, the rest loaded as the user scrolls. I would test it against the current feed and read conversion separately for slow connections."

**Code:**
```python
# Prompt arithmetic: bits to bytes
kbps, seconds = 400, 3
kbit = kbps * seconds
kB = kbit / 8
assert kbit == 1200 and kB == 150
print("kilobits in 3 s:", kbit, "| ceiling payload (kB):", kB)

# That ceiling ignores latency, handshakes and slow phases; show how fast it shrinks
for overhead_s in (0.0, 0.5, 1.0):
    avail = seconds - overhead_s
    print(f"with {overhead_s} s of fixed overhead -> payload ceiling {kbps * avail / 8:.0f} kB")
assert kbps * (3 - 1.0) / 8 == 100
# If the typical session gets only half the nominal rate (assumed), the ceiling halves
assert kB / 2 == 75

# Illustrative payload budget for a home screen (kB), compared with the ceiling at 1 s overhead and half rate
budget = {"layout + app shell (cached after first load)": 0, "feed ids and scores for 20 items": 1.0,
          "20 item cards, text only, compressed": 14.0, "20 thumbnails at 3 kB each": 60.0}
uncached = sum(budget.values())
print("illustrative uncached payload kB:", uncached, "| fits 75 kB ceiling:", uncached <= 75)
assert uncached == 75.0

# Image shrink options (assumed starting sizes): 20 images of 30 kB each
imgs, start = 20, 30
raw = imgs * start
print("uncompressed-size images kB:", raw, "| at 10 kB each:", imgs * 10, "| only 6 above-the-fold images at 10 kB:", 6 * 10)
assert raw == 600 and raw / 150 == 4.0
assert imgs * 10 == 200 > 150 and 6 * 10 == 60 < 75
# Time to download 75 kB at 400 and at 200 kbps
for r in (400, 200):
    print(f"75 kB at {r} kbps takes {75 * 8 / r:.2f} s")
assert 75 * 8 / 400 == 1.5 and 75 * 8 / 200 == 3.0
assert 10 * 8 / 400 == 0.2
print("each extra 10 kB costs seconds at 400 kbps:", 10 * 8 / 400)
```

**Output (my run):**
```
kilobits in 3 s: 1200 | ceiling payload (kB): 150.0
with 0.0 s of fixed overhead -> payload ceiling 150 kB
with 0.5 s of fixed overhead -> payload ceiling 125 kB
with 1.0 s of fixed overhead -> payload ceiling 100 kB
illustrative uncached payload kB: 75.0 | fits 75 kB ceiling: True
uncompressed-size images kB: 600 | at 10 kB each: 200 | only 6 above-the-fold images at 10 kB: 60
75 kB at 400 kbps takes 1.50 s
75 kB at 200 kbps takes 3.00 s
each extra 10 kB costs seconds at 400 kbps: 0.2
```

**Follow-ups:**
- Would you rank on the device? For re-ranking a cached candidate list, yes: no round trip and small model; keep the heavy model on the server for the candidate list.
- How do you test improvements for slow users? Randomise by user, record network class at session start, and report the effect within the slow class, with enough users in that class.
- What would you cut first? Images above the fold are largest; shrink or delay them before cutting text signals.

**Common mistakes:**
- Mixing bits and bytes (dividing by 8 is the whole step).
- Treating 150 kB as the budget rather than the ceiling.
- Measuring only on office wifi.
- Reporting averages instead of slow-link percentiles.

### Q20 ⭐⭐ 🟡 Cash-on-delivery risk: A shop platform ships 100,000 cash-on-delivery orders a day, and 25% come back as return-to-origin (a measured 90-day average), costing 90 rupees each in shipping. A model flags the 20% of orders with the highest risk, and the flagged group contains 50% of all return-to-origin orders (a back-test projection). A verification call costs 6 rupees and, in a pilot of 2,000 orders, rescued 40% of the would-be returns among 500 flagged orders in the pilot (a sample), and assume each rescued order saves the full 90 rupees. Design the programme, and compute the daily net saving of calling every flagged order and the precision of the flag.
**Asked at:** Indian-market material (a Let's Data Science / NPCI item on AI for UPI fraud and multilingual voice, an Elastic and Sarvam multilingual voice-agent blog, a SquadStack voice-bot page on noise and accents, Razorpay, Delhivery and Shiprocket pages on cash-on-delivery return-to-origin risk scoring, a Blinkit candidate report of a delivery-time debugging case); vendor and blog material, no confirmed interview round for these exact designs; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Flagging 20,000 orders that hold 12,500 of the 25,000 returns gives a precision of 62.5%, and calling them nets 450,000 - 120,000 = 330,000 rupees a day, but the 40% rescue rate comes from a small pilot and the benefit is the shipping saving only, so I would size the gain with an interval and expand calls only where the risk exceeds 16.7%.

**Clarifying questions:**
- Does the pilot's 40% (200 of 500 flagged would-be returns) hold for the whole flagged 20%, including its lower-risk end? A small sample from the top of the list may not generalise.
- What does "rescued" mean: the customer confirmed and the parcel was delivered and paid? Define it so a confirmation that later fails is not counted.
- Is 90 rupees the whole cost of a return, or only forward and return shipping? Packaging, handling and lost inventory time could raise it.
- Are there other actions besides a call (messages, prepaid discount, address check)? Cheaper actions change the break-even.
- Do customers dislike calls, and does the call delay dispatch? Both are guardrails.

**Approach:**
1. Clarify and frame. Goal: lower return-to-origin cost by intervening on risky cash-on-delivery orders before dispatch. The decision is whom to call, not only who is risky.
2. Metrics and guardrails. Net saving per day, precision of the flag (returns / flagged), recall (share of returns flagged), rescue rate, delivery delay. Guardrails: conversion of good orders, customer complaints, dispatch delay, share of customers called repeatedly.
3. Data and labels. Label = order returned to origin, observed after delivery attempts (a delay of days, so use matured cohorts). Features: pincode history, order value, customer history, time, address quality. Careful: the pilot's outcomes are changed by the call itself, so train on pre-intervention or randomised holdout orders.
4. Baseline first. Rules by pincode and order value; a simple logistic model. Compare precision at 20% flagged.
5. Model and trade-offs. Gradient-boosted trees or logistic regression with calibrated probabilities. Call when probability x rescue rate x 90 > 6, i.e. risk above 6 / (0.40 x 90) = 16.7% (see the code). The unflagged group runs at 15.6%, below that, so calling it loses money (marginal value -30,000 per day). The trade-off is call volume versus returns prevented.
6. Evaluation. Offline: precision and recall at the cut, lift by decile, calibration; check the projected 50% capture on a recent matured period. Online: randomise a holdout (some flagged orders not called) to measure the true rescue effect, which is the number the business case needs.
7. Launch and experiment plan. Start with the top decile, widen to the top 20% if the randomised rescue rate holds; keep a 5% holdout permanently.
8. Monitoring, retraining and risks. Monitor precision by pincode, rescue rate, call cost; retrain monthly on matured labels; watch for customers gaming the process.

Indicative pacing for a 45-minute round (minutes per step 1 to 8): 4, 4, 6, 4, 10, 7, 5, 5.

**Metrics:**
- Return-to-origin orders = 100,000 x 25% = 25,000; flagged = 20,000; returns in flagged = 12,500.
- Precision of the flag = returns among flagged / flagged = 12,500 / 20,000 = 62.5%. Recall = 12,500 / 25,000 = 50%.
- Net saving per day = rescued orders x 90 - calls x 6 = (12,500 x 0.40 x 90) - (20,000 x 6) = 450,000 - 120,000 = 330,000 rupees.
- Break-even return probability for a call = call cost / (rescue rate x saving per rescue) = 6 / (0.40 x 90) = 16.7%.
- Guardrails: good-order conversion, complaint rate, dispatch delay.

**Risks:**
- Sample versus projection: the 40% rescue rate is a pilot sample and the 50% capture is a back-test projection. With 500 flagged would-be returns in the pilot (200 rescued) the rescue interval is about 36% to 44%, so net ranges about 282,000 to 378,000.
- Selection: calling changes behaviour and hides what would have happened; only a randomised holdout measures it.
- Saving only shipping: ignoring lost sales from friction or complaints from customers who did not want a call.
- Drift: pincode risk changes with festivals, couriers and weather.
- Calling customers and using personal data: ask compliance and legal about consent and rules for calls and profiling.

**What the interviewer scores:**
- Strong: 62.5% precision, 330,000 net, and checks the marginal call against a 16.7% break-even.
- Strong: separates sample (pilot rescue) from projection (50% capture), and asks for a randomised holdout.
- Strong: guardrails for good-order conversion and customer experience.
- Weak: "flag the risky orders and call them all" with no break-even, no uncertainty, no holdout.

**Example:** Illustrative numbers from the question. Weak versus strong:
- Weak: "A model flags 20% of orders; we call them and save money."
- Strong: "25,000 of 100,000 orders return, the flag holds 12,500 of them, so precision is 62.5%. Calling 20,000 costs 120,000 and rescues 5,000 orders worth 450,000, net 330,000 a day. The 40% rescue is from a pilot sample, so I would show a range, and a call only pays when return risk is above 16.7%, so I would not call the other 80,000 whose risk is 15.6%. I would keep a randomised holdout to measure the real effect."

**Code:**
```python
import math

orders, rto_rate, ship, flag_share, flag_rto_share = 100_000, 0.25, 90, 0.20, 0.50
call, rescue = 6, 0.40
rto = round(orders * rto_rate)
flagged = round(orders * flag_share)
rto_flagged = round(rto * flag_rto_share)
assert (rto, flagged, rto_flagged) == (25_000, 20_000, 12_500)
precision = rto_flagged / flagged
assert precision == 0.625
cost = flagged * call
saved = rto_flagged * rescue * ship
net = saved - cost
assert cost == 120_000 and round(saved) == 450_000 and round(net) == 330_000
print("RTO orders:", rto, "| flagged:", flagged, "| RTO in flagged:", rto_flagged, "| precision:", precision)
print("call cost:", cost, "| saved:", round(saved), "| net per day:", round(net))

# Unflagged group and the marginal call
unf, unf_rto = orders - flagged, rto - rto_flagged
unf_rate = unf_rto / unf
breakeven = call / (rescue * ship)
print("unflagged orders:", unf, "RTO rate:", round(unf_rate, 4), "| break-even RTO probability for a call:", round(breakeven, 4))
assert round(unf_rate, 4) == 0.1562 and round(breakeven, 4) == 0.1667 and unf_rate < breakeven
net_all = rto * rescue * ship - orders * call
print("net if every order is called:", round(net_all), "| marginal value of calling the unflagged 80,000:", round(net_all - net))
assert round(net_all) == 300_000 and round(net_all - net) == -30_000

# The 40% rescue rate comes from a pilot sample: 500 flagged would-be returns (from the question)
n_rto_pilot = 500
se = math.sqrt(rescue * (1 - rescue) / n_rto_pilot)
lo, hi = rescue - 1.96 * se, rescue + 1.96 * se
print("pilot flagged would-be returns:", n_rto_pilot, "| rescue 95% interval:", round(lo, 3), "to", round(hi, 3))
for r in (lo, rescue, hi):
    print(f"  rescue {r:.3f} -> net per day {round(rto_flagged * r * ship - cost)}")
assert 0.35 < lo < 0.36 and 0.44 < hi < 0.45
assert round(rto_flagged * lo * ship - cost) < 285_000 < round(rto_flagged * hi * ship - cost)
# Rescue rate at which the flagged programme breaks even
be_rescue = cost / (rto_flagged * ship)
print("break-even rescue rate for the flagged group:", round(be_rescue, 4))
assert round(be_rescue, 4) == 0.1067
```

**Output (my run):**
```
RTO orders: 25000 | flagged: 20000 | RTO in flagged: 12500 | precision: 0.625
call cost: 120000 | saved: 450000 | net per day: 330000
unflagged orders: 80000 RTO rate: 0.1562 | break-even RTO probability for a call: 0.1667
net if every order is called: 300000 | marginal value of calling the unflagged 80,000: -30000
pilot flagged would-be returns: 500 | rescue 95% interval: 0.357 to 0.443
  rescue 0.357 -> net per day 281691
  rescue 0.400 -> net per day 330000
  rescue 0.443 -> net per day 378309
break-even rescue rate for the flagged group: 0.1067
```

**Follow-ups:**
- Should you call everyone at 16.7% or above, not just the top 20%? Yes, call by calibrated probability, not by a fixed 20%; the top 20% is a convenient cut, and the exact cut should come from the marginal rule with a safety margin for uncertainty.
- What if the rescue rate is only 10%? Below the 10.7% break-even for the flagged group, calling loses money; switch to cheaper actions such as a message or prepaid nudge.
- How would you check the 50% capture claim? Recompute capture on a recent matured period out of time and compare; it was a back-test, so it can be optimistic.

**Common mistakes:**
- Treating the pilot's 40% as a fixed fact.
- Forgetting that the 90-rupee saving ignores other costs and benefits.
- Calling a group below the break-even risk.
- Training on outcomes that were changed by the intervention.

### Q21 ⭐⭐ 🟡 Healthcare triage assist: A tele-clinic network handles 30,000 consultations a day, and 2% are urgent (an estimate from an audit sample). A triage tool must flag at least 95% of urgent cases for clinician review, and clinicians can review at most 3,000 flagged cases a day. Design the assistive tool, and compute the urgent cases a day, the true urgent cases the flags must contain and the minimum precision of the flagged queue, and say what you would ask compliance.
**Asked at:** Healthcare and vision design material (a Dataford prompt on end-to-end ML for medical signal or image data, behind a sign-up wall, and an arXiv technology-readiness paper noting trust as a barrier in regulated fields; no triage-specific interview page was found); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 30,000 x 2% = 600 urgent cases a day, 95% of them is 570, and with 3,000 review slots the queue only needs 570 / 3,000 = 19% precision at its floor, so I would design an assistive ranker that never closes a case, only moves risky ones to a clinician first.

**Clarifying questions:**
- What does "urgent" mean and who labelled it in the audit sample (clinician consensus, one reviewer, outcome after 48 hours)? The label sets the ceiling for everything, including the 2%.
- How big was the audit sample behind the 2%? A 2% from 1,000 consults could be anywhere from about 1.1% to 2.9%, which moves the workload and the precision floor.
- Is the tool ranking, flagging or deciding? I assume it only reorders and flags, and a clinician makes every decision. If it can auto-close cases the whole risk profile changes.
- What does a missed urgent case cost, and how fast must a flagged case be seen? That decides whether recall 95% is the right target and what the review delay budget is.
- What data arrives at triage (free text, vitals, history, audio)? That decides the model family and the privacy questions I take to compliance.
- Does the tool count as regulated software in our market? I do not assume an answer; I ask compliance and legal.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 8 / 6 / 8 / 8 / 5)
1. Clarify and frame (5 min). Assistive, human in the loop, never auto-dismiss. Say the numbers out loud: 600 urgent, 570 must be in the queue, 3,000 slots, so a 10% flag rate.
2. Metrics and guardrails (5 min). Primary: recall of urgent cases in the flagged queue (target 95%). Capacity: queue size at most 3,000. Guardrails: recall for each subgroup (age band, language, hospital, channel), time from flag to clinician review, and clinician override rate.
3. Data and labels (8 min). Labels from clinician outcomes, but the audit sample is a sample: get an interval on the 2%. Beware that past triage decisions shaped which cases got outcomes (label bias). Add a small random slice of "not flagged" cases for clinician audit so recall is measured and not assumed.
4. Baseline first (6 min). Keyword and vital-sign rules plus the current manual triage order. The model must beat that at the same 3,000 slots, in recall, not accuracy.
5. Model and trade-offs (8 min). Calibrated gradient boosting on structured fields plus a text encoder if free text matters. The queue is a rank cut: take the top 3,000, or fewer if the score falls below a threshold. Trade-off: a bigger queue raises recall but costs clinician time (the 19% floor rises as the queue shrinks). Binormal rough guide: a 95% recall at a 10% flag rate needs an AUC near 0.98, which is high, so say it may not be reachable and plan the fallback (higher cap, more reviewers, or a lower target).
6. Evaluate offline, then online (8 min). Offline: recall at the 3,000 cap on a time-split holdout, by subgroup, with intervals. Then shadow mode (the tool scores, nobody sees it), then clinician-visible on one hospital, then stage up. Online metric: urgent cases reviewed within the time target, measured on the random audit slice.
7. Monitoring, retraining, risks and cost (5 min). Daily: flag rate, queue age, score drift, subgroup recall on the audit slice, override rate. Retrain on a schedule with clinician-confirmed labels. Risks: automation bias, drift when a season or disease pattern changes, hidden subgroup misses. Cost: reviewer hours (3,000 reviews a day) against the harm of missed cases. Ask compliance and legal about approval, consent, retention and liability; I do not state rules as facts.

**Metrics:**
- Recall of the queue = urgent cases inside the flagged queue / all urgent cases that day (570 / 600 at target). Measure it on clinician-confirmed outcomes plus the random audit slice.
- Precision of the queue = urgent cases in the queue / queue size. At a full 3,000 queue the floor is 570 / 3,000 = 19%.
- Flag rate = flagged consults / all consults (10% at the cap).
- Time to first review = minutes from flag to a clinician opening the case, 95th percentile.
- Guardrails: recall for each subgroup (denominator: urgent cases in that subgroup), override rate, and the share of urgent cases found only after the patient came back.

**Risks:**
- The 19% is a floor only at a full queue. A smaller queue needs higher precision for the same 570 hits.
- The 2% is an estimate from a sample; if urgency is 3% the 95% target means 855 hits, not 570, and the precision floor becomes 28.5%.
- Recall measured only on flagged cases looks perfect. Measure it on an unflagged random slice.
- Clinicians trust the queue and stop looking at unflagged cases (automation bias).
- Subgroups with weak data (rare language, children) can have much lower recall than the average.

**What the interviewer scores:**
- Strong: derives 600, 570 and 19% in seconds and says what each means. Weak: starts with a model name.
- Strong: assistive framing, shadow mode, an audit slice of unflagged cases. Weak: "accuracy of 95%" and an autonomous decision.
- Strong: notices the 2% is a sample and the 19% is a floor. Weak: treats every number as exact.
- Strong: asks compliance and legal and states no rules as facts. Weak: invents regulations, or ignores them.
- Strong: gives a pacing plan and a fallback if the target is not reachable.

**Example:** Illustrative numbers. If the audit sample had 1,000 consults, the 2% has an interval of about plus or minus 0.9 points, so urgent cases are 340 to 860 a day and the precision floor is 10.8% to 27.2%.
- Weak: "I would train a classifier with 95% accuracy on urgent cases."
- Strong: "There are about 600 urgent cases a day. To catch 95% I need 570 of them in the queue. Clinicians can read 3,000, so the queue must be at least 19% urgent at the cap. I would ship it as an assistive ranker, run it in shadow first, and measure recall on a random audit slice, because the 2% is only an estimate. What counts as regulated here is a question for compliance and legal."

**Code:**
```python
# Q21 triage sizing (all numbers illustrative; the 2% is a sample estimate)
from statistics import NormalDist
N = NormalDist()
consults, urgent_rate, recall_target, cap = 30_000, 0.02, 0.95, 3_000
urgent = round(consults * urgent_rate)
must_catch = round(urgent * recall_target)
min_precision = must_catch / cap
assert urgent == 600 and must_catch == 570 and min_precision == 0.19
print(f"urgent/day={urgent}, true urgent in flags >= {must_catch}, min precision at a full queue = {min_precision:.0%}")

# Flag rate and the false-positive room inside the queue
flag_rate = cap / consults
fp_room = cap - must_catch
non_urgent = consults - urgent
max_fpr = fp_room / non_urgent
assert flag_rate == 0.10 and fp_room == 2_430 and abs(max_fpr - 0.08265) < 1e-4
print(f"flag rate={flag_rate:.0%}, false flags allowed={fp_room}, max false-positive rate={max_fpr:.2%}")

# Model assumption (equal-variance binormal scores): what separation does that need?
d = N.inv_cdf(recall_target) + N.inv_cdf(1 - max_fpr)
auc = N.cdf(d / 2 ** 0.5)
assert abs(d - 3.03) < 0.01 and abs(auc - 0.984) < 0.002
print(f"needed d'={d:.2f}, implied AUC={auc:.3f} (binormal assumption, a rough guide only)")

# The 2% is a sample. Suppose (invented) the audit had 1,000 consults.
n_audit = 1_000
se = (urgent_rate * (1 - urgent_rate) / n_audit) ** 0.5
lo, hi = urgent_rate - 1.96 * se, urgent_rate + 1.96 * se
u_lo, u_hi = consults * lo, consults * hi
p_lo, p_hi = recall_target * u_lo / cap, recall_target * u_hi / cap
assert abs(se - 0.004427) < 1e-5 and round(u_lo) == 340 and round(u_hi) == 860
assert abs(p_lo - 0.1077) < 1e-3 and abs(p_hi - 0.2724) < 1e-3
print(f"2% +/- {1.96*se:.2%} -> urgent {u_lo:.0f}..{u_hi:.0f}/day -> min precision {p_lo:.1%}..{p_hi:.1%}")
# If urgency were 3% instead of 2%
hits3 = consults * 0.03 * recall_target
assert round(hits3) == 855 and abs(hits3 / cap - 0.285) < 1e-9
print(f"if urgency is 3%: hits needed={hits3:.0f}, precision floor={hits3/cap:.1%}")
```

**Output (my run):**
```text
urgent/day=600, true urgent in flags >= 570, min precision at a full queue = 19%
flag rate=10%, false flags allowed=2430, max false-positive rate=8.27%
needed d'=3.03, implied AUC=0.984 (binormal assumption, a rough guide only)
2% +/- 0.87% -> urgent 340..860/day -> min precision 10.8%..27.2%
if urgency is 3%: hits needed=855, precision floor=28.5%
```

**Follow-ups:**
- What if the model only reaches 80% recall at the 3,000 cap? Say so, then offer options: a bigger cap with more reviewers, a two-stage queue (fast nurse check on the second tier), or a lower target agreed with clinical leads.
- How do you measure recall if unflagged cases are never reviewed? A small random audit slice of unflagged cases reviewed by a clinician each day, with an interval.
- Would you use an LLM here? Possibly to extract fields from free text, with the ranker doing the scoring, and with the same audit slice; free text from an LLM is not a decision.

**Common mistakes:** Quoting accuracy instead of recall at a fixed review capacity. Treating 19% as the required precision at any queue size. Forgetting the 2% is a sample. No unflagged audit slice. Letting the tool close cases. Stating legal rules as facts.

### Q22 ⭐⭐ 🟡 Experimentation platform: 40 product teams will run 120 concurrent experiments on an app with 12,000,000 daily users, organised in 10 layers where every user is in every layer and the 12 experiments inside a layer split its users evenly. Assignment lookups must answer in 5 ms at the 99th percentile at 20,000 requests per second. Design the platform, and compute the daily users each experiment sees if all users are eligible and compare it with a need of 800,000 distinct users across two arms over the run.
**Asked at:** Operations and platform design material (a Codemia anomaly-detection pipeline prompt attributed to ServiceNow, Codemia A/B-testing platform prompts attributed to a DoorDash onsite, a PracHub feature-store data-quality and backfill prompt attributed to a Faire onsite, datadriven.io and techinterview.org MLOps guides); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 12,000,000 users split 12 ways in each layer gives 1,000,000 users per experiment, which covers the 800,000 needed with 200,000 (25%) to spare, but only if every user is eligible, so I would design for eligibility rules and a layer-by-layer capacity check.

**Clarifying questions:**
- Confirm the 800,000 means distinct users over the run. One million "daily users" are mostly the same people tomorrow, so a multi-day run adds few new users.
- What share of users is eligible for a typical experiment (new users only, one country, one platform)? At 30% eligible, each experiment sees 300,000 and the plan breaks.
- What metrics, and what effect size must be detectable? The 800,000 is only a need if someone derived it; I would re-derive it (for a 5% baseline, 400,000 per arm detects about 0.14 points).
- Which experiments must be mutually exclusive (same screen, same ranking model) and which can overlap? That decides what goes into one layer.
- Do the 5 ms at 20,000 requests per second apply to the assignment call only, and is it from cache or from a service? It sets whether we assign by hash or look up a table.
- Who is allowed to launch, and who reviews a bad result? Governance decides the platform scope as much as the maths does.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 6 / 5 / 6 / 8 / 8 / 7)
1. Clarify and frame (5 min). Platform users are 40 teams; the product is trustworthy decisions at low cost. Do the arithmetic aloud: 120 / 10 = 12 per layer, 12,000,000 / 12 = 1,000,000 each.
2. Metrics and guardrails (6 min). Platform metrics: experiments launched per week, share of experiments reaching their needed sample, time to a decision, and a guardrail of sample ratio mismatch (assigned split against the planned split). Product metrics are owned by each team, with a shared guardrail set (crashes, latency, retention).
3. Data and labels (5 min). Exposure logs (user, experiment, arm, time), assignment configuration with versions, and metric tables. The key rule: log exposure at the moment the user actually sees the change, not at assignment.
4. Baseline first (6 min). Start with one layer, hash assignment, a basic z-test or t-test report and a sample-ratio check. Do not build sequential testing or variance reduction before that works.
5. Model and trade-offs (8 min). Assignment is a pure function: hash(salt per layer, user id) mod 12, no database lookup, so 5 ms at 20,000 per second is easy (about 100 in flight at most by Little's law). Trade-off: more layers give more concurrent tests but more interaction risk; fewer layers give clean results but a queue. Reserve a holdout. Capacity planner: refuse or queue an experiment whose eligible users cannot reach its needed sample.
6. Evaluate offline, then online (8 min). Offline: A/A tests on every layer should show about 5% false positives at 0.05 and a balanced split. Replay old experiments through the pipeline. Online: roll the platform out to two teams first.
7. Monitoring, retraining and cost (7 min). Alert on sample-ratio mismatch, logging gaps, and exposure drift. No model retraining here, but metric definitions are versioned. Cost: the logging and metric computation, not the assignment. Risks: peeking, interaction between layers, novelty effects, and teams reading many metrics without correction.

**Metrics:**
- Users per experiment per day = users in the layer / experiments in the layer = 12,000,000 / 12 = 1,000,000.
- Sample coverage = users the experiment sees over its run / users needed (target at least 1.0; here 1,000,000 / 800,000 = 1.25).
- Sample-ratio mismatch rate = experiments whose observed arm split differs from plan by a chi-square test at a strict threshold / all running experiments.
- Assignment latency p99 in ms (target 5) and error rate of the lookup.
- Guardrail: the false-positive rate of A/A tests, which should be near the chosen alpha.

**Risks:**
- Daily users and distinct users over the run are different bases; the 800,000 is distinct users over the run, and a longer run adds few new ones.
- Eligibility filters cut each experiment's sample sharply.
- Layers are independent only if each has its own salt; shared salts correlate assignments (the code checks this).
- Many experiments on one user can interact (two ranking changes in different layers).
- Peeking at results daily inflates false positives.

**What the interviewer scores:**
- Strong: 120 / 10 = 12 and 1,000,000 immediately, then immediately asks about eligibility and how many distinct users a run really accumulates. Weak: stops at "enough users".
- Strong: hash-based assignment, so lookups are computation, not a database. Weak: a table lookup per call with no capacity thought.
- Strong: sample-ratio mismatch and A/A tests as platform health checks. Weak: only the dashboard.
- Strong: a baseline first plan, one layer then more. Weak: builds everything at once.

**Example:** Illustrative numbers. One experiment limited to 30% eligible users sees 300,000 users, so it needs about 2.7 times the share of users (or a longer run, which helps only as new users arrive), while another that is open to everyone sees 1,000,000.
- Weak: "We have 12 million users and the test needs 800,000, so we are fine."
- Strong: "Each layer splits 12 million users 12 ways, so every experiment gets 1 million. That clears 800,000 by 25%, but only if all users are eligible. With 30% eligibility it falls to 300,000, so the platform should check eligible users against the needed sample before an experiment is allowed to launch."

**Code:**
```python
# Q22 experimentation platform sizing (illustrative)
import hashlib, math
users, layers, exps_total, per_layer = 12_000_000, 10, 120, 12
assert per_layer * layers == exps_total and exps_total // 40 == 3
users_per_exp = users // per_layer
need = 800_000
assert users_per_exp == 1_000_000 and users_per_exp >= need
headroom = users_per_exp - need
assert headroom == 200_000 and headroom / need == 0.25
print(f"users per experiment per day={users_per_exp:,}, need={need:,}, headroom={headroom:,} ({headroom/need:.0%} of need)")

# If only 30% of users are eligible (invented), each experiment sees fewer
elig = round(users_per_exp * 0.30)
assert elig == 300_000 and elig < need
print(f"with 30% eligibility: {elig:,} < {need:,}")

# What 800,000 (400,000 per arm) can detect: baseline 5%, alpha 0.05 two-sided, power 80%
z = 1.96 + 0.8416
p, n_arm = 0.05, 400_000
mde = z * math.sqrt(2 * p * (1 - p) / n_arm)
assert abs(mde - 0.001366) < 2e-5
print(f"minimum detectable absolute lift ~ {mde*100:.3f} points ({mde/p:.1%} relative)")

# Assignment load: Little's law on the lookup service (upper bound uses the 5 ms p99 for every call)
rps, lat = 20_000, 0.005
inflight = rps * lat
assert inflight == 100
print(f"requests in flight at most ~ {inflight:.0f}; each request resolves {layers} layers")

# Deterministic hash bucketing: each layer has its own salt, so layers are independent
def bucket(uid, layer, k):
    h = hashlib.sha256(f"layer{layer}:{uid}".encode()).digest()
    return int.from_bytes(h[:8], 'big') % k
N = 120_000
counts = [0] * per_layer
cross = [[0] * per_layer for _ in range(per_layer)]
for u in range(N):
    a, b = bucket(u, 0, per_layer), bucket(u, 1, per_layer)
    counts[a] += 1
    cross[a][b] += 1
expected = N / per_layer
assert all(abs(c - expected) / expected < 0.05 for c in counts)
# users in experiment 0 of layer 0 spread evenly over layer 1 buckets (independence)
row = cross[0]
assert all(abs(c - sum(row) / per_layer) / (sum(row) / per_layer) < 0.15 for c in row)
print("bucket counts layer0:", counts)
print("layer-0 experiment 0 across layer-1 buckets:", row)
```

**Output (my run):**
```text
users per experiment per day=1,000,000, need=800,000, headroom=200,000 (25% of need)
with 30% eligibility: 300,000 < 800,000
minimum detectable absolute lift ~ 0.137 points (2.7% relative)
requests in flight at most ~ 100; each request resolves 10 layers
bucket counts layer0: [9949, 9857, 9987, 9869, 9869, 10142, 9993, 10107, 10222, 9969, 10060, 9976]
layer-0 experiment 0 across layer-1 buckets: [827, 844, 822, 859, 840, 802, 806, 819, 845, 876, 790, 819]
```

**Follow-ups:**
- How do you run more than 12 experiments in a layer? Shrink each arm's share, run longer, or use more layers; every option trades speed for power or interaction risk.
- What if two experiments touch the same screen in different layers? Put them in the same layer so they are mutually exclusive, or analyse the interaction explicitly.
- How do you know the platform is trustworthy? A/A tests, sample-ratio checks, and replaying a past experiment. The detailed metric reading is covered in Book 6 Part 1 (see its question on a ranking change that lifts click-through while orders fall).

**Common mistakes:** Confusing daily users with distinct users over the run. Ignoring eligibility. Using one hash salt for all layers. Logging exposure at assignment time. Building sequential testing before the basics work. Giving no capacity check before launch.

### Q23 ⭐⭐ 🟡 Data-quality platform: A data team owns 1,500 tables with 6 automated checks each, run daily, and each check scans 40 GB on average at an illustrative 0.5 rupees per GB, with a budget of 100,000 rupees a day. Design the data-quality platform, and compute the daily scan cost with full scans and with a 50% row sample (assume scan cost is proportional to the rows read), and say which checks should not be sampled.
**Asked at:** Operations and platform design material (a Codemia anomaly-detection pipeline prompt attributed to ServiceNow, Codemia A/B-testing platform prompts attributed to a DoorDash onsite, a PracHub feature-store data-quality and backfill prompt attributed to a Faire onsite, datadriven.io and techinterview.org MLOps guides); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 1,500 tables x 6 checks is 9,000 scans, 360,000 GB, so 180,000 rupees a day with full scans (1.8 times the 100,000 budget) and 90,000 with a 50% sample, but a sample only helps if the engine really reads half the data and it must not touch checks that look for rare or exact defects.

**Clarifying questions:**
- The prompt assumes scan cost is proportional to rows read. In many columnar layouts a row sample still reads most of the data; only partition or file-level sampling saves cost. I would verify that before promising the 90,000.
- What are the six checks per table today (freshness, row count, schema, null rate, uniqueness, distribution)? Some can be answered from metadata at almost no cost.
- Which tables feed models or finance reports, and which are scratch? Criticality sets check depth and who gets paged.
- Are tables partitioned by date, so a daily check can scan only the new partition? That is usually a bigger saving than sampling.
- Who owns a failed check, and what is the expected response time? A check with no owner is a cost with no value.
- Is 100,000 rupees a hard cap or a target, and does it include storage and alert tooling?

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 6 / 5 / 6 / 8 / 8 / 7)
1. Clarify and frame (5 min). Goal: catch bad data before models and dashboards use it, within a cost cap. State the arithmetic: 9,000 checks, 360,000 GB, 180,000 rupees full, 90,000 sampled.
2. Metrics and guardrails (6 min). Detection: bad-data incidents caught by a check before a user noticed / all bad-data incidents. Cost: rupees per day against the 100,000 cap. Noise: alerts per week and the share that were real. Guardrail: time from a bad load to an alert.
3. Data and labels (5 min). Labels are past incidents (which table, which defect, how found). Start by listing the last 20 data incidents and asking which check would have caught each.
4. Baseline first (6 min). Metadata checks for every table (freshness, row count versus recent days, schema, partition present). These cost almost nothing and catch many failures.
5. Model and trade-offs (8 min). Tier the tables (critical, normal, scratch). Content checks run only on the new partition. Sample where an estimate is good enough (null rate, mean, distribution shift); scan fully where exactness matters (uniqueness of keys, orphan keys, value ranges that must never break, rare segments). Learned anomaly thresholds on top of row counts instead of fixed numbers, as a later step.
6. Evaluate offline, then online (8 min). Offline: replay the 20 past incidents and count which are caught, and at what cost. Online: shadow mode for two weeks (alerts to a channel nobody is paged by), then page for the critical tier only.
7. Monitoring, retraining and cost (7 min). Weekly report of cost per tier, alerts, false-alert share and incidents missed. Retune thresholds monthly. Risks: alert fatigue, a sample hiding a rare defect, checks drifting as schemas change, cost rising as tables grow. Build-versus-buy: an open or vendor tool can cover standard checks; the custom part is tiering and ownership.

**Metrics:**
- Daily scan cost = checks run x GB per check x rupees per GB (9,000 x 40 x 0.5 = 180,000).
- Detection rate = incidents caught by a check before a consumer reported them / all incidents in the period.
- False-alert share = alerts judged not real after triage / all alerts.
- Time to detect = hours from a bad load to its first alert.
- Guardrail: cost as a share of the cap (target below 100%), and incidents missed that a sampled check could have caught.

**Risks:**
- A row sample may not reduce bytes read; check the engine before promising savings.
- A sampled uniqueness check catches one duplicate pair only 25% of the time at a 50% sample.
- Rare bad segments disappear in samples (one bad row survives with probability 0.5).
- Checks run without an owner create alert noise.
- Table growth silently pushes the cost back over the cap.

**What the interviewer scores:**
- Strong: 9,000, 360,000 GB, 180,000 and 90,000 quickly, then notices full scans are over budget. Weak: designs checks with no cost figure.
- Strong: says which checks must not be sampled and why (uniqueness, referential integrity, hard ranges, rare segments). Weak: "sample everything".
- Strong: cheaper levers first (metadata, new partition only, tiering). Weak: only sampling.
- Strong: ownership, shadow mode and alert-noise tracking. Weak: dashboards no one reads.

**Example:** Illustrative numbers. If 3 of the 6 checks are metadata-only and the other 3 scan, full scans cost 90,000 a day, and scanning only the new partition (taken as 1/30 of the table) costs 3,000.
- Weak: "I would sample 50% of every table and that fits the budget."
- Strong: "Full scans cost 180,000 a day, 1.8 times the budget. A 50% sample gives 90,000 only if the engine really reads half the data. Before that I would answer freshness, volume and schema from metadata, scan only new partitions, and keep uniqueness and key-integrity checks unsampled because a sample catches one duplicate pair only a quarter of the time."

**Code:**
```python
# Q23 data-quality scan cost (illustrative)
import random
tables, checks, gb, price, budget = 1_500, 6, 40, 0.5, 100_000
runs = tables * checks
assert runs == 9_000
full = runs * gb * price
half = full * 0.5
assert full == 180_000 and half == 90_000
print(f"checks/day={runs}, full scan cost={full:,.0f} rupees ({full/budget:.2f}x budget), 50% sample={half:,.0f} ({half/budget:.0%} of budget)")

# Illustrative split of the 6 checks: 3 answered from metadata (almost free), 3 scan data
meta, scanning = 3, 3
mix_full = tables * scanning * gb * price
mix_half = mix_full * 0.5
assert mix_full == 90_000 and mix_half == 45_000
print(f"3 metadata + 3 scanning checks: full={mix_full:,.0f}, sampled={mix_half:,.0f}")

# Incremental scan: only the new daily partition (invented: 1/30 of the table) for the scanning checks
inc = mix_full / 30
assert inc == 3_000
print(f"incremental (new partition only, 1/30 of table): {inc:,.0f} rupees")

# Why uniqueness should not be sampled: one duplicated pair survives a 50% row sample with prob 0.25
random.seed(7)
trials, caught = 100_000, 0
for _ in range(trials):
    a, b = random.random() < 0.5, random.random() < 0.5
    caught += a and b
rate = caught / trials
assert abs(rate - 0.25) < 0.01
print(f"single duplicate pair caught by a 50% row sample: {rate:.3f} (theory 0.25)")

# A rare bad segment: 40 bad rows among 1,000,000; chance the sample contains none of them
p_none = 0.5 ** 40
assert p_none < 1e-12
# ... but chance of seeing zero of 1 bad row is 0.5, so tiny defects often vanish
print(f"sample sees none of 1 bad row: {0.5:.2f}; none of 40: {p_none:.1e}")
```

**Output (my run):**
```text
checks/day=9000, full scan cost=180,000 rupees (1.80x budget), 50% sample=90,000 (90% of budget)
3 metadata + 3 scanning checks: full=90,000, sampled=45,000
incremental (new partition only, 1/30 of table): 3,000 rupees
single duplicate pair caught by a 50% row sample: 0.250 (theory 0.25)
sample sees none of 1 bad row: 0.50; none of 40: 9.1e-13
```

**Follow-ups:**
- How do you set thresholds without hand tuning 9,000 checks? Start with rolling-window bounds from recent history per table, review the noisiest 5% by hand, and tier by criticality.
- What would you do if cost grows past the cap? Re-tier, widen sampling on non-critical tables only, reduce frequency for slow-changing tables, and show the trade-off to the data owners.
- How does this connect to model monitoring? Data checks protect inputs; model monitoring (Book 6 Part 2, see its question on a feature null rate jumping after an upstream deploy) sees the effect on predictions.

**Common mistakes:** Assuming a row sample halves the scan cost. Sampling uniqueness or key checks. Ignoring metadata checks. No owner per table. Pasting one threshold for every table. Forgetting the cost grows with table size.

### Q24 ⭐⭐ 🟡 MLOps platform: Four platform engineers have 6 months (take it as 26 weeks) to build a deployment and retraining platform for 25 models owned by 6 teams, of which 10 are real-time and 15 are batch. The real-time services target 99.9% availability over a 30-day month. Design the platform and its roadmap, and compute the monthly error budget in minutes and the engineer-weeks available.
**Asked at:** Operations and platform design material (a Codemia anomaly-detection pipeline prompt attributed to ServiceNow, Codemia A/B-testing platform prompts attributed to a DoorDash onsite, a PracHub feature-store data-quality and backfill prompt attributed to a Faire onsite, datadriven.io and techinterview.org MLOps guides); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 99.9% over a 30-day month is 0.001 x 43,200 = 43.2 minutes of allowed downtime per real-time service, and 4 engineers x 26 weeks is 104 engineer-weeks gross (about 73 at 70% focus), so I will build the thinnest platform that makes the 10 real-time models safe first and onboard the 15 batch models on the same pieces.

**Clarifying questions:**
- How do the 6 teams deploy and retrain today (scripts, notebooks, a scheduler)? The platform must replace pain, not add a new process.
- Is 99.9% per service measured at the user-facing endpoint, and what counts as a failure (errors, timeouts, stale model)? Without that, the 43.2 minutes is not measurable.
- Which of the 10 real-time models are revenue- or safety-critical? They go first.
- Which cloud, cluster and tools are already approved? Build-versus-buy depends on this.
- Who is on call, and is there a platform on-call or does each team page itself? That drives the effort needed for runbooks and alerts.
- What does "retraining" mean for each model (scheduled, triggered by drift, manual)? It sets the pipeline design.

**Approach:** (about 8 steps; pacing for a 45-minute round: 4 / 5 / 5 / 6 / 8 / 7 / 5 / 5)
1. Clarify and frame (4 min). Users are 6 teams and 25 models. Success is that a team can ship and retrain a model without the platform team in the loop.
2. Metrics and guardrails (5 min). Platform: deploy lead time, share of models on the platform, failed-deploy rate, rollback time. Reliability: error budget burn per service. Guardrail: team satisfaction and number of platform tickets per week.
3. Data and labels (5 min). The "data" here is an inventory: every model, its owner, its input data, how it serves (real-time or batch), how often it retrains and what it costs. Build that table in week 1.
4. Baseline first (6 min). A model registry plus a standard container and CI pipeline, a one-command deploy and a rollback. This alone removes the biggest risk and fits in the first 14 engineer-weeks.
5. Model and trade-offs (8 min). Real-time serving: canary or blue-green, health checks, autoscaling and an SLO dashboard. Batch: a templated scheduled pipeline with retraining, validation gates and promotion. Trade-off: buy or adopt existing tools for standard parts, build only the glue and the golden path. Resist a feature store or a UI in the first half.
6. Evaluate offline, then online (7 min). Pilot with two teams, one real-time and one batch. Measure deploy lead time before and after. Chaos-style test: kill a pod and a bad model version and time the rollback.
7. Launch, monitoring and retraining (5 min). Onboard the 10 real-time models in order of criticality, then the 15 batch ones. Monitor latency, errors, saturation and a model-quality proxy. A failed retrain must never replace the live model.
8. Risks and cost (5 min). Scope creep, adoption (teams keep their scripts), a single point of failure in the platform itself (three serial 99.9% parts give 99.7%, so the platform must not sit in the request path), key-person risk. Cost: effort first, cloud second.

**Metrics:**
- Monthly error budget (minutes) = (1 - 0.999) x 30 x 24 x 60 = 43.2 per service.
- Error-budget burn = bad minutes so far / 43.2 (alert at 50% and 100% of the monthly budget).
- Deploy lead time = hours from merge to serving traffic, median.
- Adoption = models deployed through the platform / 25.
- Guardrail: rollback time (target minutes) and failed retrains that reached production (target zero).

**Risks:**
- 104 engineer-weeks is gross; leave, support and on-call cut it to about 73 (at an invented 70%).
- A platform in the serving path adds its own downtime to every service.
- Teams do not migrate if the golden path is harder than their scripts.
- 43.2 minutes is per service per month; one bad 30-minute deploy uses 70% of it.
- Scope grows (feature store, UI, A/B tooling) before the basics work.

**What the interviewer scores:**
- Strong: 43.2 and 104 immediately, then the net capacity after overhead. Weak: stops at 104 or treats it as fully usable.
- Strong: a phased roadmap with engineer-weeks per phase that sums to capacity. Weak: a wish list.
- Strong: buy or adopt the standard parts, own the golden path and the SLO. Weak: build everything.
- Strong: reliability thinking (error budget, canary, rollback, platform not in the request path). Weak: "use Kubernetes".

**Example:** Illustrative split of about 73 net engineer-weeks: foundation 14, real-time serving 18, batch retraining 14, monitoring 10, onboarding 12 (about 0.5 each for 25 models), buffer 4.8.
- Weak: "We will build a full MLOps platform with a feature store and a model registry in six months."
- Strong: "Four people for 26 weeks is 104 engineer-weeks, about 73 after overhead. Real-time services get 43.2 minutes of downtime a month, so I would first ship registry, standard container, canary and one-command rollback for the 10 real-time models, then the templated batch pipeline, then monitoring. A feature store waits until the first teams are live."

**Code:**
```python
# Q24 MLOps platform sizing (illustrative)
minutes_month = 30 * 24 * 60
budget_min = (1 - 0.999) * minutes_month
assert minutes_month == 43_200 and abs(budget_min - 43.2) < 1e-9
print(f"monthly error budget at 99.9% = {budget_min:.1f} minutes per real-time service")
print(f"across 10 real-time services = {10*budget_min:.0f} service-minutes in total")

# Chained dependencies: serial availability multiplies
chain = 0.999 ** 3
assert abs(chain - 0.997003) < 1e-6
assert abs((1-chain)*minutes_month - 129.5) < 0.1
print(f"three serial 99.9% parts give {chain:.4%} -> {(1-chain)*minutes_month:.1f} min/month of downtime (3x the single budget)")

# Capacity
engineers, weeks = 4, 26
gross = engineers * weeks
focus = 0.70                     # invented: leave, meetings, on-call, support
net = gross * focus
assert gross == 104 and abs(net - 72.8) < 1e-9
print(f"gross engineer-weeks={gross}, at 70% focus={net:.1f}, per model (25) gross={gross/25:.2f}")

# Illustrative roadmap that sums to the net capacity
plan = {"foundation: registry, packaging, CI": 14,
        "real-time serving, canary, rollback": 18,
        "batch retraining pipelines": 14,
        "monitoring and SLO alerts": 10,
        "onboard 25 models (about 0.5 each)": 12,
        "buffer": 4.8}
tot = sum(plan.values())
assert abs(tot - net) < 1e-9
for k, v in plan.items():
    print(f"  {k}: {v} eng-weeks")
print(f"planned total={tot:.1f}")

# One bad deploy: how many full-outage minutes exhaust one service's budget
assert int(budget_min // 10) == 4
print(f"4 outages of 10 minutes use {40} of {budget_min:.1f} minutes")
assert round(30 / budget_min, 3) == 0.694
print(f"one 30-minute outage uses {30/budget_min:.1%} of the monthly budget")
```

**Output (my run):**
```text
monthly error budget at 99.9% = 43.2 minutes per real-time service
across 10 real-time services = 432 service-minutes in total
three serial 99.9% parts give 99.7003% -> 129.5 min/month of downtime (3x the single budget)
gross engineer-weeks=104, at 70% focus=72.8, per model (25) gross=4.16
  foundation: registry, packaging, CI: 14 eng-weeks
  real-time serving, canary, rollback: 18 eng-weeks
  batch retraining pipelines: 14 eng-weeks
  monitoring and SLO alerts: 10 eng-weeks
  onboard 25 models (about 0.5 each): 12 eng-weeks
  buffer: 4.8 eng-weeks
planned total=72.8
4 outages of 10 minutes use 40 of 43.2 minutes
one 30-minute outage uses 69.4% of the monthly budget
```

**Follow-ups:**
- What would you cut if the team loses one engineer? Drop the batch retraining templates to a later quarter and keep serving, rollback and monitoring; the 10 real-time models carry the availability risk.
- How do you set an SLO for a model, not only a service? Add a quality proxy (prediction distribution, a delayed-label metric) next to availability, and agree what a breach triggers.
- How do you measure that the platform helps? Compare deploy lead time and incident counts for onboarded versus not-yet-onboarded models. Detail on monitoring is in Book 6 Part 2 (e.g. the question on a feature null rate jumping after an upstream deploy).

**Common mistakes:** Using 104 as fully available. Forgetting the error budget is per service. Building a feature store first. Putting the platform in the request path. No pilot team. Skipping rollback.

### Q25 ⭐⭐ 🟡 Vision for insurance claims: An insurer receives 20,000 vehicle-damage photos a day through a mobile app, with 70% arriving in a 4-hour window (assume evenly spread). A raw photo is 1.2 MB and a compressed one is 250 KB (take 1 MB as 1,000,000 bytes), uplinks give about 500 kilobits per second, and one GPU scores 40 photos per second. Design the claims-photo triage system, and compute the upload time for each size, the peak photos per second and the GPUs needed, then say where the bottleneck is.
**Asked at:** Healthcare and vision design material (a Dataford prompt on end-to-end ML for medical signal or image data, behind a sign-up wall, and an arXiv technology-readiness paper noting trust as a barrier in regulated fields; no triage-specific interview page was found); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The peak is only 14,000 / 14,400 s = 0.97 photos a second, so one GPU at 40 a second is 2.4% busy; the real bottleneck is the customer's 500 kilobit uplink, where a raw photo takes 19.2 seconds and a compressed one 4.0 seconds, so I would compress on the phone and spend my design effort on upload and review.

**Clarifying questions:**
- What decision does the photo feed (fast-track payout, route to an adjuster, flag for fraud review)? The action decides which errors cost the most.
- How many photos per claim and is the customer waiting on screen for the result? That sets the latency target and whether upload time is the user's pain.
- Who owns the final claim decision? I assume a human adjuster for anything above a threshold; the tool triages and never denies a claim alone.
- Is the "evenly spread" 4-hour window realistic, or do claims spike after a weather event? Bursts matter more than the average.
- What labels exist (adjuster estimates, repair invoices, fraud outcomes), and how late do they arrive? Repair invoices can take weeks.
- What may be stored and for how long (photos contain locations, plates, people)? I ask compliance and legal; I do not assume.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 7 / 6 / 8 / 8 / 6)
1. Clarify and frame (5 min). Goal: faster, more consistent claim triage with fewer manual touches, without wrongly rejecting honest claims. Do the numbers aloud: 19.2 s versus 4 s upload, 0.97 per second, one GPU.
2. Metrics and guardrails (5 min). Primary: share of claims routed correctly (fast-track, adjuster, fraud review) compared with the final adjuster outcome. Operational: time from first photo to decision, upload failure rate. Guardrails: wrongly delayed honest claims, and error rate by phone type and region.
3. Data and labels (7 min). Past claims with photos and adjuster outcome (severity band, repair cost band, fraud flag). Labels are noisy and late, so use severity bands rather than exact cost, and check agreement between adjusters. Photo quality labels (blurred, wrong angle) are cheap to add and very useful.
4. Baseline first (6 min). Quality checks on the phone (blur, glare, vehicle present), a simple severity classifier, and the current adjuster queue order. Compare against it.
5. Model and trade-offs (8 min). On-device: resize and compress to about 250 KB, check quality, resumable uploads, upload in the background. Server: a pretrained vision backbone fine-tuned for damage severity and part location, plus a duplicate-photo and metadata check for fraud. Trade-off: compression too hard hurts damage detail; test accuracy at the compressed size, not at the original. Scoring is cheap, so the model can be larger.
6. Evaluate offline, then online (8 min). Offline: severity-band accuracy and the confusion cost matrix on a time-split holdout, by phone type and lighting. Online: shadow mode (score, route nothing), then recommend-only to adjusters, then fast-track low-risk bands for a small share.
7. Launch, monitoring and risks (6 min). Monitor upload failures, photo-quality rejects, score drift, override rate by adjusters and complaint rate. Retrain on adjuster outcomes. Risks: new phone cameras, staged fraud, fairness across regions and vehicle types, a weather-event burst. Cost: GPU is small; storage and adjuster time dominate.

**Metrics:**
- Upload time = bytes x 8 / uplink bits per second (1,200,000 x 8 / 500,000 = 19.2 s; 250,000 x 8 / 500,000 = 4.0 s).
- Peak rate = photos in the window / window seconds = 14,000 / 14,400 = 0.97 per second.
- GPU utilisation = peak rate / 40 = 2.4%.
- Routing accuracy = claims routed to the band the adjuster later confirmed / all routed claims.
- Guardrails: share of honest claims delayed beyond the target, and the fast-track error rate (fast-tracked claims later overturned / fast-tracked claims).

**Risks:**
- Evenly spread is an assumption; a storm can multiply the rate, though even 10 times is 9.7 per second.
- Compression that hides damage detail lowers accuracy; test it.
- Adjuster outcomes are late and noisy labels.
- Staged or reused photos need a separate fraud check.
- Customers on slow links abandon uploads; measure drop-off.

**What the interviewer scores:**
- Strong: finds that upload, not the GPU, is the bottleneck, with the numbers. Weak: sizes GPUs and stops.
- Strong: compress and resume on the phone, test accuracy at the compressed size. Weak: "send the raw photo".
- Strong: human adjuster decides, shadow mode first. Weak: automatic denial.
- Strong: labels and their lateness handled. Weak: assumes clean labels.

**Example:** Illustrative numbers. A claim of 6 photos sent one after another takes 115 seconds raw and 24 seconds compressed on that uplink, while the GPU needs 0.025 seconds a photo.
- Weak: "20,000 photos a day, so I need a GPU cluster."
- Strong: "The peak is under one photo a second, so one GPU, or two for redundancy, is plenty. The 500 kilobit uplink is the problem: 19.2 seconds raw versus 4 seconds compressed. So I compress on the phone, upload in the background and resume on failure, check accuracy at the compressed size, and keep an adjuster in the loop."

**Code:**
```python
# Q25 claims-photo triage sizing (illustrative)
import math
photos, share, window_h = 20_000, 0.70, 4
raw_B, comp_B, uplink_bps = 1_200_000, 250_000, 500_000
t_raw, t_comp = raw_B * 8 / uplink_bps, comp_B * 8 / uplink_bps
assert t_raw == 19.2 and t_comp == 4.0 and abs(t_raw / t_comp - 4.8) < 1e-9
print(f"upload time: raw {t_raw:.1f} s, compressed {t_comp:.1f} s ({t_raw/t_comp:.1f}x faster)")

peak_photos = photos * share
peak_rate = peak_photos / (window_h * 3600)
assert peak_photos == 14_000 and abs(peak_rate - 0.9722) < 1e-3
gpu_rate = 40
gpus = math.ceil(peak_rate / gpu_rate)
util = peak_rate / gpu_rate
assert gpus == 1 and abs(util - 0.0243) < 1e-3
print(f"peak rate={peak_rate:.3f} photos/s, GPUs needed={gpus}, utilisation={util:.1%}")

# Burst check: even a 10x burst over the even-spread rate
burst = 10 * peak_rate
assert math.ceil(burst / gpu_rate) == 1 and burst < gpu_rate
print(f"10x burst={burst:.2f} photos/s still fits one GPU (use 2 for redundancy)")

# Ingest bandwidth at the server for compressed photos
ingest_bps = peak_rate * comp_B * 8
assert abs(ingest_bps - 1_944_444) < 10
print(f"server ingest at peak ~ {ingest_bps/1e6:.2f} Mbit/s")

# Per claim with 6 photos (invented): customer waits
per_claim_raw, per_claim_comp = 6 * t_raw, 6 * t_comp
assert abs(per_claim_raw - 115.2) < 1e-9 and per_claim_comp == 24.0
print(f"6 photos one after another: raw {per_claim_raw:.1f} s, compressed {per_claim_comp:.1f} s")
# Scoring time per photo on a GPU is 1/40 s
assert 1 / 40 == 0.025
print("GPU scoring time per photo = 0.025 s versus 4.0 s upload: upload is 160x longer")
assert 4.0 / 0.025 == 160
```

**Output (my run):**
```text
upload time: raw 19.2 s, compressed 4.0 s (4.8x faster)
peak rate=0.972 photos/s, GPUs needed=1, utilisation=2.4%
10x burst=9.72 photos/s still fits one GPU (use 2 for redundancy)
server ingest at peak ~ 1.94 Mbit/s
6 photos one after another: raw 115.2 s, compressed 24.0 s
GPU scoring time per photo = 0.025 s versus 4.0 s upload: upload is 160x longer
```

**Follow-ups:**
- What if photos arrive in a storm at 50 times the rate? 50 x 0.97 is about 49 per second, so 2 GPUs; queue the rest and tell customers the expected wait.
- Do you score on the phone instead of the server? A small quality-check model on the phone, yes; the damage model stays on the server so it can be updated and audited.
- How would you catch fraud? Duplicate and near-duplicate photo search, metadata consistency, and routing to a specialist, never an automatic denial.

**Common mistakes:** Sizing the GPU and ignoring upload time. Sending raw photos over slow links. Testing accuracy only on uncompressed photos. Treating late adjuster labels as instant. Auto-denying on a model score.

### Q26 ⭐⭐ 🟡 Cold-start personalisation: A grocery app gets 60,000 new users a day with no history and plans to give 10% of recommendation slots to exploration, where the click rate is 1.5% per impression, against 3% for slots chosen by the best current policy (both rates measured in an earlier test, a sample). Design the new-user recommender, and compute the expected clicks per 100 impressions with that exploration and without it, and the relative loss against the no-exploration figure.
**Asked at:** General ML system-design prep material (Educative's 6-step ML design framework and fraud-detection mock interview, DesignGurus, techinterview.org, PracHub's 2026 ML system design bank and a DEV Community guide describe open prompts such as feed or recommendation, search ranking and ad prediction, and one guide quotes a search prompt with 1,000 queries per second and 200 ms); commercial prep sites, so example numbers are treated as examples only; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** With 10% exploration at 1.5% and 90% at 3%, I expect 0.10 x 1.5 + 0.90 x 3 = 2.85 clicks per 100 impressions against 3.00 without it, a 5% relative loss, and I would accept that price only because exploration is how a new user's profile gets learned.

**Clarifying questions:**
- Were the 1.5% and 3% measured on new users or on existing users? The sample may not transfer to people with no history, so I treat both as starting guesses.
- What is the goal for a new user (first order, second-week return, basket size)? Clicks are only a proxy, and exploration pays off in later sessions, not in the first click.
- What can be used before any history (city, device, time of day, install source, popular items)? That is the baseline policy for the cold start.
- How many items and categories exist, and how fast does the catalogue change? That decides how much exploration is needed.
- Are there items we must never show (out of stock, age-restricted, local rules)? Exploration must stay inside safe limits.
- How long does a user stay "new"? An exit rule from cold start sets how much of the traffic explores.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 6 / 6 / 9 / 8 / 6)
1. Clarify and frame (5 min). Goal: get a new user to a good first basket and a return visit, while learning fast. Say the arithmetic: 2.85 versus 3.00, 5% cost per slot.
2. Metrics and guardrails (5 min). Primary: clicks per 100 impressions in the first session, plus the real goal (orders in the first 7 days per new user). Guardrails: add-to-cart and order rate, return-visit rate on day 7, share of slots on out-of-stock or poor items, latency.
3. Data and labels (6 min). Impressions with clicks and orders, logged with the policy and the probability of showing each item (propensity). Without logged propensities, later learning from exploration data is biased.
4. Baseline first (6 min). Popularity by city and time of day, with a few hand-made category slots. That is the policy that gets 3%.
5. Model and trade-offs (9 min). A contextual bandit or a simple epsilon-greedy over popular items with a decaying exploration share; as a user's history builds, a personalised ranker takes over. Trade-off: exploration cost is 5% of clicks at 10%; the policy must improve by more than 5.56% relative (3.00% to 3.17%) for exploration to break even on clicks alone. Use smarter exploration (explore among decent items, not random ones) to cut the cost.
6. Evaluate offline, then online (8 min). Offline: replay logged data with propensities (inverse-propensity weighting) as a rough check only. Online: randomise users to exploration shares (0%, 5%, 10%) and measure 7-day orders per new user, not first-session clicks.
7. Monitoring, retraining and risks (6 min). Watch exploration share, popularity feedback loops (popular items get more clicks only because they are shown), catalogue coverage and per-city results. Retrain daily for new items. Cost is small compared with the learning value; the trade-off is a few percent of first-session clicks.

**Metrics:**
- Expected clicks per 100 impressions = 100 x (explore share x explore CTR + (1 - explore share) x policy CTR) = 2.85.
- Relative loss = (3.00 - 2.85) / 3.00 = 5%, base is the no-exploration figure.
- 7-day orders per new user = orders in 7 days from new users / new users in the arm.
- Catalogue coverage = distinct items shown to new users in a day / items in stock.
- Guardrails: out-of-stock impression share, day-7 return rate, latency.

**Risks:**
- The 1.5% and 3% are sample estimates (a 1.5% from 2,000 impressions could be 1.0% to 2.0%).
- The 5% is a first-session cost; the learning benefit is not in the figure.
- Rates are assumed constant; exploring on low-quality items may hurt the experience more than clicks show.
- Popularity bias: the algorithm shows popular items, they get clicks, they stay popular.
- Without logged propensities the exploration data cannot be used fairly.

**What the interviewer scores:**
- Strong: computes 2.85 and 5% quickly and frames it as the price of learning. Weak: "exploration is wasteful" or "explore a lot".
- Strong: a baseline first, then bandit, with a break-even condition. Weak: jumps to a deep model with no history.
- Strong: measures the long-run outcome, not first-click CTR. Weak: only clicks.
- Strong: says the rates are samples and may not transfer to new users. Weak: treats them as exact.

**Example:** Illustrative numbers. On 60,000 new users with 20 impressions each (1,200,000 impressions, an invented figure), the 5% relative loss is 0.15 clicks per 100, which is 1,800 clicks a day.
- Weak: "I would use 10% exploration because that is standard."
- Strong: "Ten percent exploration costs 0.15 clicks per 100 impressions, 2.85 against 3.00, a 5% loss. It is worth it only if it lifts the learned policy by about 5.6% relative or raises 7-day orders. I would test 0, 5 and 10 percent on new users and judge them by 7-day orders, with propensities logged."

**Code:**
```python
# Q26 cold-start exploration cost (illustrative rates, from a sample)
import random
explore, ctr_explore, ctr_policy = 0.10, 0.015, 0.03
with_exp = 100 * (explore * ctr_explore + (1 - explore) * ctr_policy)
without = 100 * ctr_policy
loss = (without - with_exp) / without
assert abs(with_exp - 2.85) < 1e-9 and abs(without - 3.0) < 1e-9 and abs(loss - 0.05) < 1e-9
print(f"clicks per 100 impressions: with exploration={with_exp:.2f}, without={without:.2f}, relative loss={loss:.1%}")

# What the learned policy must gain for exploration to pay back (rates held as assumptions)
needed = (ctr_policy - explore * ctr_explore) / (1 - explore)
assert abs(needed - 0.031667) < 1e-5
print(f"policy CTR must rise from 3.00% to {needed:.3%} ({needed/ctr_policy-1:.2%} relative) to break even")

# Simulation check with a fixed seed
random.seed(11)
n = 1_000_000
clicks = 0
for _ in range(n):
    p = ctr_explore if random.random() < explore else ctr_policy
    clicks += random.random() < p
sim = clicks / n * 100
assert abs(sim - with_exp) < 0.05
print(f"simulated clicks per 100 impressions={sim:.2f}")

# Noise in the measured rates: a 1.5% rate from 2,000 impressions (invented) has a wide interval
imp = 2_000
se = (ctr_explore * (1 - ctr_explore) / imp) ** 0.5
lo, hi = ctr_explore - 1.96 * se, ctr_explore + 1.96 * se
assert abs(lo - 0.00961) < 1e-4 and abs(hi - 0.02039) < 1e-4
print(f"1.5% from {imp} impressions: 95% interval {lo:.2%} to {hi:.2%}")
# Example: 60,000 new users x 20 impressions (invented)
imps = 60_000 * 20
assert imps == 1_200_000 and round(imps * (ctr_policy - (with_exp / 100))) == 1_800
print(f"daily clicks lost at {imps:,} impressions: {imps*(ctr_policy-with_exp/100):,.0f}")
```

**Output (my run):**
```text
clicks per 100 impressions: with exploration=2.85, without=3.00, relative loss=5.0%
policy CTR must rise from 3.00% to 3.167% (5.56% relative) to break even
simulated clicks per 100 impressions=2.81
1.5% from 2000 impressions: 95% interval 0.97% to 2.03%
daily clicks lost at 1,200,000 impressions: 1,800
```

**Follow-ups:**
- How would you cut the cost of exploration? Explore only among items already above a quality bar, shrink the share as history builds, and explore more where the model is uncertain.
- What if the catalogue is tiny? Then little exploration is needed, a few percent, because popular items already cover it.
- Why does popularity feedback matter? The items shown get clicks, so popularity looks self-confirming; logged propensities and some random slots keep the data honest.

**Common mistakes:** Judging exploration by first-session clicks only. Treating sample rates as exact. Not logging propensities. Using random items rather than decent ones. Using the same exploration share forever.

### Q27 ⭐⭐ 🟡 Vernacular search evaluation: A shopping app serves 3,000,000 queries a day in 8 languages and has a labelling budget of 120,000 rupees at 4 rupees per human relevance judgement. You want each language measured to within plus or minus 2.5 percentage points at 95% confidence for a proportion near 50%, using n = (1.96 times 0.5 over 0.025) squared, rounded up. Design the evaluation and labelling plan, and compute the judgements bought, the judgements per language for that precision, the total for 8 languages and what remains.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to multilingual search relevance evaluation (no page found in these searches); search snippets only, not opened
**Say this first (1 line):** The budget buys 120,000 / 4 = 30,000 judgements, precision of plus or minus 2.5 points needs 1,537 per language (1,536.64 rounded up), 8 languages cost 12,296, leaving 17,704, which I would spend on a harder question than one headline number per language.

**Clarifying questions:**
- What is being measured: the share of queries with a relevant result in the top results, NDCG, or a side-by-side preference? The 1,537 formula is for one proportion; other metrics need their own sizing.
- Is the goal to describe each language, or to compare two search systems in each language? A comparison needs more labels (about 3,074 per language per system at the same precision if samples are separate).
- How many judges per item, and how well do they agree? Two judges per item double the cost and give an agreement estimate; Hinglish and mixed script are the hard cases.
- Are queries drawn at random from traffic, or by popularity? Random draws describe users; head-heavy draws miss the long tail where search fails.
- Who are the judges (native speakers per language)? Quality and the cost of 4 rupees depend on it.
- Does the 8-language split reflect traffic? Small languages may need a different precision target.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 8 / 5 / 7 / 8 / 7)
1. Clarify and frame (5 min). The goal is a trustworthy relevance number per language, so that regressions are visible. Say the budget arithmetic: 30,000 judgements.
2. Metrics and guardrails (5 min). Primary: share of judged query-result pairs rated relevant (at top 5) per language. Guardrails: judge agreement per language and the share of queries with no result.
3. Data and labels (8 min). Sample queries at random per language (stratify by head, torso, tail), gold questions to check judges, written guidelines for mixed-script queries, two judges on a 10% slice to measure agreement.
4. Baseline first (5 min). One fixed judged set per language, scored once on the current system. That is the yardstick before any new model.
5. Model and trade-offs (7 min). The "model" here is the sampling plan: 1,537 per language gives about plus or minus 2.5 points for a proportion near 50%. Trade-off: eight separate 95% intervals all cover their truths only about 66% of the time; making them hold jointly needs 2,991 per language (23,928 total), still inside the 30,000.
6. Evaluate offline, then online (8 min). Offline: judged sets for regression checks on every ranker change. Online: compare click and reformulation metrics per language as a cross-check, since judgements and clicks can disagree.
7. Monitoring, retraining, risks and cost (7 min). Refresh a fraction of the set monthly as queries drift, keep a frozen core, track judge drift with gold items. Use leftover budget for tail queries or double judging. Risks: judge bias, stale sets, an LLM judge not validated against humans.

**Metrics:**
- Relevant share per language = pairs judged relevant / pairs judged, in that language.
- Margin = 1.96 x sqrt(p(1-p)/n), with p = 0.5 and n = 1,537 gives about 0.025.
- Agreement = pairs where both judges agree / pairs double-judged (or a chance-corrected kappa).
- Budget used = judgements x 4 rupees (12,296 x 4 = 49,184).
- Guardrail: the share of the budget on gold and double-judged items (target a stated small share).

**Risks:**
- The formula assumes a simple random sample of independent items; several judgements on one query are correlated, so the real margin is wider.
- p near 50% is the worst case; if p is 80% the same n gives a narrower margin.
- 8 intervals at 95% each are not 95% jointly.
- Tail queries drive complaints but rarely appear in a random sample.
- Judges may disagree on code-mixed queries; a noisy label limits what any sample size shows.

**What the interviewer scores:**
- Strong: 30,000, 1,537, 12,296 and 17,704 quickly and in the right units (judgements, then rupees). Weak: mixes rupees and judgements.
- Strong: knows what the margin applies to (one proportion) and the multiple-intervals point. Weak: quotes 2.5 points for everything.
- Strong: judge quality, guidelines, gold items. Weak: "buy labels" with no quality plan.
- Strong: spends the remainder on a stated purpose (tail, comparison, agreement). Weak: leaves it unspent.

**Example:** Illustrative numbers. After the 12,296 judgements, 17,704 remain (70,816 rupees); 1,600 tail queries x 8 languages = 12,800 more would leave 4,904.
- Weak: "I would label 30,000 queries and see how it goes."
- Strong: "1,537 judgements per language gives plus or minus 2.5 points, 12,296 in total, 17,704 left. I would keep the rest for tail queries and a second judge on a slice, and if we need all eight intervals to hold together I would go to 2,991 per language, 23,928 in all."

**Code:**
```python
# Q27 vernacular search evaluation labelling plan (illustrative)
import math
from statistics import NormalDist
budget, price, langs, moe = 120_000, 4, 8, 0.025
bought = budget // price
n_raw = (1.96 * 0.5 / moe) ** 2
n = math.ceil(n_raw)
total = langs * n
left = bought - total
assert bought == 30_000 and abs(n_raw - 1536.64) < 1e-9 and n == 1537
assert total == 12_296 and left == 17_704
print(f"bought={bought}, n per language={n} (raw {n_raw:.2f}), total={total}, remaining={left} judgements = {left*price} rupees")

# Joint coverage of 8 separate 95% intervals
joint = 0.95 ** langs
assert abs(joint - 0.6634) < 1e-3
print(f"chance all 8 intervals cover their truth ~ {joint:.1%} (independent)")

# Bonferroni: 8 intervals jointly at 95%
z = NormalDist().inv_cdf(1 - 0.05 / (2 * langs))
nb = math.ceil((z * 0.5 / moe) ** 2)
assert abs(z - 2.734) < 0.001 and nb == 2991 and langs * nb == 23_928 and bought - langs * nb == 6_072
print(f"Bonferroni z={z:.3f}, n per language={nb}, total={langs*nb}, remaining={bought-langs*nb}")

# Comparing two rankers on separate samples needs more (a paired design on shared queries can need less)
# Unpaired two-sample on proportions near 50%: n per arm = 2*(1.96*0.5/0.025)^2
nu = math.ceil(2 * (1.96 * 0.5 / 0.025) ** 2)
assert nu == 3074
print(f"unpaired comparison of two systems at same precision: {nu} per language per system")
assert langs * n * price == 49_184 and left - 1_600 * langs == 4_904 and left * price == 70_816
```

**Output (my run):**
```text
bought=30000, n per language=1537 (raw 1536.64), total=12296, remaining=17704 judgements = 70816 rupees
chance all 8 intervals cover their truth ~ 66.3% (independent)
Bonferroni z=2.734, n per language=2991, total=23928, remaining=6072
unpaired comparison of two systems at same precision: 3074 per language per system
```

**Follow-ups:**
- Can an LLM judge replace humans? It can cut cost, but validate it against a human-labelled slice per language and do not let it grade its own system alone. See Book 6 Part 3 (the question on using one LLM for labels and as the judge).
- How do you compare two rankers? Judge both on the same queries and analyse the paired difference; unpaired samples need about double the n at the same precision.
- What if a language has few queries? The sample is capped by what exists; report a wider interval honestly.

**Common mistakes:** Confusing rupees with judgements. Using p = 0.5 and ignoring that it is the worst case. Forgetting the margin applies to one proportion. Not rounding up. No judge-quality checks. Ignoring correlation within queries.

### Q28 ⭐⭐ 🔴 LLM analytics assistant: An internal assistant for 800 employees answers 5,000 questions a day, each using an average of 2.4 LLM calls of 6,000 tokens each, at an illustrative blended 0.25 rupees per 1,000 tokens against a monthly budget of 60,000 rupees (30 days). Design the assistant with its data-access limits and evaluation, and compute the monthly cost as designed, the factor by which cost must fall and two levers that could deliver it.
**Asked at:** Agentic and GenAI design material (Dataford agentic AI engineer guides listing multi-step customer-service workflows, techinterview.org and aiforanything.io pages on AI agent infrastructure and system design, and a post-LLM-era ML engineer interview guide saying 'design an LLM-based system for X' is now the most common prompt); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** As described the assistant uses 5,000 x 2.4 x 6,000 = 72 million tokens a day, 18,000 rupees a day, 540,000 a month, which is 9 times the 60,000 budget, so I design for a 9x cost cut first (route most calls to a small model and shrink the context) and treat quality and data access as the other two fixed constraints.

**Clarifying questions:**
- Tokens are 6,000 per call (14,400 per question), as the prompt says; I would confirm this against real logs, because if it were per question the bill would be 225,000 a month, 3.75 times over.
- What kinds of questions arrive (look up a number, build a chart, explain a trend)? Simple look-ups can use a cheap path.
- Which data may each employee see? Row-level and column-level access must follow the user, not the assistant. I ask the data-governance owner; I assume nothing.
- How wrong may an answer be? A wrong number in a board deck is worse than a refusal, so I set a wrong-answer ceiling before choosing models.
- Is the 0.25 blended price input plus output, and does it hold for a small model? I use it as given and treat a cheaper model price as an assumption to check.
- Is the budget a hard cap or a target? That sets whether we throttle or only alert.

**Approach:** (about 8 steps; pacing for a 45-minute round: 4 / 5 / 5 / 6 / 8 / 7 / 5 / 5)
1. Clarify and frame (4 min). Users are 800 employees asking about internal data. Success is a correct, traceable answer at a cost within 60,000 rupees a month. Say the gap aloud: 540,000 versus 60,000.
2. Metrics and guardrails (5 min). Primary: share of questions answered correctly (checked against a reference or a reviewer). Cost per question against 0.40 rupees allowed (60,000 / 30 / 5,000). Guardrails: wrong-answer rate, refusal rate, access violations (target zero), latency.
3. Data and labels (5 min). Collect 200 to 300 real questions with correct answers from analysts, split by type and difficulty. This is the test set and the source of routing labels.
4. Baseline first (6 min). Retrieval over a small governed set of tables and metric definitions, one strong model, one call per question. Measure accuracy and cost per question before adding agents.
5. Model and trade-offs (8 min). Generate queries against a semantic layer or approved views, run them under the asking user's permissions, and have the model explain the result. Cost levers: route about 80% of calls to a small model (a 3.57x cut if it is priced at a tenth, an assumption), cut tokens per call from 6,000 to 2,000 by sending only the relevant schema (3x), cache repeated questions. Together the first two give 10.7x, about 50,400 a month. Trade-off: cheaper paths lose accuracy on hard questions, so route by difficulty and escalate on low confidence.
6. Evaluate offline, then online (7 min). Offline: accuracy on the test set per route, and cost per question. Online: pilot with one team, thumbs and analyst spot checks, compare with a human analyst on a sample.
7. Launch, monitoring and retraining (5 min). Daily spend alert at 50% and 100% of the budget pace, per-user quota, logs of every query and the data touched, weekly review of failures, refresh the test set monthly.
8. Risks and cost (5 min). Wrong but confident numbers, data leakage across teams, prompt injection through table contents, costs creeping with usage. Build versus buy: buying a vendor tool shifts cost and data-access questions, which I would raise with security.

**Metrics:**
- Monthly cost = questions x calls x tokens per call / 1,000 x price x 30 = 540,000.
- Cost per question = 2.4 x 6,000 / 1,000 x 0.25 = 3.60 rupees; the allowed figure is 0.40.
- Answer accuracy = correct answers / questions in the test set (and in the audited live sample).
- Escalation rate = calls sent to the strong model / all calls.
- Guardrails: wrong-answer rate on audited live answers, access violations (zero), p95 latency.

**Risks:**
- Prices and the small-model share are assumptions; measure them.
- A 9x cut with no quality check just moves the cost into wrong answers.
- Caching can serve stale numbers; key it on data version and user permissions.
- Users who ask more because it is cheap raise the volume; a quota is needed.
- The assistant runs queries as a service account and exposes data a user may not see.

**What the interviewer scores:**
- Strong: 72 million, 540,000 and 9x in seconds, then levers with numbers. Weak: "use a cheaper model" with no figure.
- Strong: access follows the user, queries run under the user's rights. Weak: one shared database login.
- Strong: accuracy measured on a real question set before and after cost cuts. Weak: only cost.
- Strong: checks token counts against real logs. Weak: trusts the estimate.

**Example:** Illustrative numbers. Routing 80% of calls to a model at one tenth of the price gives 0.2 + 0.08 = 0.28 of the cost (3.57x cheaper); cutting 6,000 tokens to 2,000 gives 3x; together 10.7x, so 540,000 becomes about 50,400.
- Weak: "That is expensive, so I would switch to a smaller model."
- Strong: "As designed it costs 540,000 a month, 9 times the budget, or 3.60 rupees a question against 0.40 allowed. Routing most calls to a small model gives about 3.6x, pruning the context from 6,000 to 2,000 tokens gives 3x, together 10.7x, about 50,000. I would check accuracy on 250 real questions at every step, and run every query under the asker's own permissions."

**Code:**
```python
# Q28 LLM analytics assistant cost (illustrative prices)
qpd, calls, tok, price_k, budget, days = 5_000, 2.4, 6_000, 0.25, 60_000, 30
tokens_day = qpd * calls * tok
cost_day = tokens_day / 1000 * price_k
cost_month = cost_day * days
factor = cost_month / budget
assert tokens_day == 72_000_000 and cost_day == 18_000 and cost_month == 540_000 and factor == 9
print(f"tokens/day={tokens_day:,.0f}, cost/day={cost_day:,.0f}, cost/month={cost_month:,.0f}, factor over budget={factor:.0f}x")
per_q = calls * tok / 1000 * price_k
allowed = budget / days / qpd
assert abs(per_q - 3.6) < 1e-9 and abs(allowed - 0.4) < 1e-9
print(f"cost per question={per_q:.2f} rupees, allowed={allowed:.2f}")

# Lever A: route 80% of calls to a small model priced at 0.1x (assumed)
price_factor = 0.2 + 0.8 * 0.1
a = 1 / price_factor
# Lever B: cut tokens per call 6,000 -> 2,000 (schema pruning, short context)
b = 6_000 / 2_000
assert abs(a - 3.5714) < 1e-3 and b == 3
both = a * b
new_month = cost_month / both
assert abs(both - 10.714) < 1e-2 and new_month < budget and abs(new_month - 50_400) < 1
print(f"routing alone {a:.2f}x, token cut alone {b:.1f}x (neither reaches 9x), both {both:.2f}x -> {new_month:,.0f} per month")
# Lever C: answer cache with 30% hit rate adds headroom
c = 1 / 0.7
assert abs(both * c - 15.31) < 0.01
print(f"adding a 30% cache hit rate: {both*c:.2f}x -> {cost_month/(both*c):,.0f} per month")

# Alternative reading: 6,000 tokens per question in total
alt = qpd * 6_000 / 1000 * price_k * days
assert alt == 225_000 and abs(alt / budget - 3.75) < 1e-9
print(f"if 6,000 tokens were per question: {alt:,.0f} per month, {alt/budget:.2f}x over")
```

**Output (my run):**
```text
tokens/day=72,000,000, cost/day=18,000, cost/month=540,000, factor over budget=9x
cost per question=3.60 rupees, allowed=0.40
routing alone 3.57x, token cut alone 3.0x (neither reaches 9x), both 10.71x -> 50,400 per month
adding a 30% cache hit rate: 15.31x -> 35,280 per month
if 6,000 tokens were per question: 225,000 per month, 3.75x over
```

**Follow-ups:**
- What if the small model fails on hard questions? Escalate on low confidence or failed validation of the generated query; accept a small rise in cost on the hard tail.
- How do you stop a user from seeing data they should not? Run queries with the user's identity and the database's row and column permissions, log every query. I ask security and data governance how access is defined.
- How would you keep cost from creeping? Per-user and per-team quotas, a daily spend alert, and a monthly review of the top query types.

**Common mistakes:** Quoting cost per token and not per question. Cutting cost without an accuracy check. One shared service account. Forgetting caches need permission-aware keys. Not checking token counts against real logs.

### Q29 ⭐⭐ 🔴 Vision identity verification: A lender's app runs 40,000 selfie-and-ID checks a day, and 0.1% are spoof attempts (a projection from last quarter's investigations). A liveness model catches 95% of spoofs on a test set of known attack types (a sample), and new attack types are expected. Design the verification flow end to end with fallback and human review, compute the spoofs a day and how many pass liveness if the 95% also held for new attack types (a best case), and say what you would ask compliance.
**Asked at:** Healthcare and vision design material (a Dataford prompt on end-to-end ML for medical signal or image data, behind a sign-up wall, and an arXiv technology-readiness paper noting trust as a barrier in regulated fields; no triage-specific interview page was found); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 40,000 x 0.1% is 40 spoof attempts a day, a 95% catch rate stops 38 and lets 2 through, but that 2 is a best case because the 95% was measured on known attack types and new ones are expected, so I design layers, a human fallback and a fast retraining loop rather than trusting one liveness score.

**Clarifying questions:**
- What do spoofs cost (a fraudulent loan disbursed) compared with a genuine customer turned away? That sets the threshold and how much human review we can afford.
- Is the 0.1% the share of attempts or of customers, and how was it found (confirmed investigations only)? Undetected spoofs mean it is likely an underestimate.
- How big was the test set behind 95%, and which attack types did it contain (printed photo, screen replay, mask, deepfake)? A small set gives a wide interval and says nothing about new types.
- What is the false-reject rate on genuine users today, and for which phones, lighting and skin tones? Failure for honest users is the main cost of strictness.
- What other signals exist (device, location, behaviour, document checks, a second factor)? Layers reduce dependence on one model.
- Which checks and data retention does the lender need from compliance and legal? I ask; I do not assume rules.

**Approach:** (about 7 steps; pacing for a 45-minute round: 5 / 5 / 6 / 5 / 9 / 8 / 7)
1. Clarify and frame (5 min). Goal: stop impersonation without turning honest customers away. Say the numbers aloud: 40 spoofs, 38 caught, 2 passing as a best case.
2. Metrics and guardrails (5 min). Primary: spoofs reaching approval per day (confirmed later), and attack catch rate by attack type. Guardrails: genuine users falsely rejected, share sent to human review, completion time, subgroup false-reject rates.
3. Data and labels (6 min). Confirmed spoofs from investigations, red-team attacks built in-house for each new type, genuine sessions across phones and lighting. Keep the test set split by attack type so "new attack" is tested honestly.
4. Baseline first (5 min). The current liveness check plus document checks and device signals, a simple score threshold, and a human fallback. Measure its false-reject and catch rates by type.
5. Model and trade-offs (9 min). Layered flow: capture quality check, active liveness challenge, passive liveness model, face match to the ID, device and behaviour risk score. Three routes: pass, step-up (retry or another factor), human review. Trade-off: a stricter threshold catches more spoofs and rejects more genuine users; use two thresholds so the middle band goes to step-up, not to rejection.
6. Evaluate offline, then online (8 min). Offline: catch rate per attack type on a held-out attack type set (leave-one-attack-out), false-reject rate by subgroup, with intervals. Online: shadow mode first, then a small share of traffic, with confirmed spoofs tracked to the loan outcome.
7. Monitoring, retraining, risks and cost (7 min). Weekly red-team of new attack types, alert on score distribution drift, track review queue age, retrain when a new attack is confirmed. Risks: deepfakes, bias across skin tones and phones, adversaries probing the thresholds, privacy of biometric data (ask compliance and legal about consent, storage and retention).

**Metrics:**
- Spoofs per day = checks x spoof share = 40,000 x 0.001 = 40.
- Spoof pass rate = spoofs that pass liveness / spoofs (5% on known attacks; unknown on new ones).
- False reject rate = genuine users rejected or stepped up / genuine users (denominator 39,960).
- Review queue = users sent to a human per day, and its share that are real spoofs.
- Guardrails: false-reject rate per subgroup, review time, time to onboard.

**Risks:**
- 2 passing spoofs a day is a floor; at an assumed 50% catch on a new attack it is 20 a day.
- The 95% comes from a test of invented size 200 (190 caught); the interval is 91.0% to 97.3%.
- A 1% false-reject on 39,960 genuine users sends about 400 people a day to fallback, more than the spoofs.
- Adversaries adapt to a published threshold.
- Biometric data creates privacy and storage obligations; ask compliance and legal.

**What the interviewer scores:**
- Strong: 40, 38, 2 immediately, then says why 2 is optimistic. Weak: stops at "95% is good".
- Strong: layers, step-up, human review and a plan for new attacks. Weak: a single model.
- Strong: measures false rejects on honest users and by subgroup. Weak: only the catch rate.
- Strong: defers legal and biometric rules to compliance. Weak: invents them.

**Example:** Illustrative numbers. If the catch rate on a new attack type is 50%, 20 spoofs a day pass; with a 1% false-reject rate about 400 genuine users go to fallback, so about 8.7% of a 438-case review queue are real spoofs.
- Weak: "Liveness catches 95%, so only 2 spoofs get through."
- Strong: "40 attempts a day, 38 caught, 2 pass, but only against known attack types, so I treat 2 as a best case. I would add a step-up route, a human review band, a weekly red-team for new attacks and shadow mode before launch, and measure false rejects by phone and lighting. Biometric rules are a question for compliance and legal."

**Code:**
```python
# Q29 identity verification (illustrative; 0.1% is a projection, 95% is a sample on known attacks)
from math import sqrt
checks, spoof_rate, catch = 40_000, 0.001, 0.95
spoofs = round(checks * spoof_rate)
caught = spoofs * catch
passed = spoofs - caught
assert spoofs == 40 and caught == 38 and abs(passed - 2) < 1e-9
print(f"spoofs/day={spoofs}, caught={caught:.0f}, pass liveness={passed:.0f} (best case: known attacks only)")

# Sensitivity to the catch rate on new attack types
for r in (0.95, 0.80, 0.50, 0.20):
    print(f"  catch {r:.0%}: {spoofs*(1-r):.0f} spoofs pass a day")
assert abs(spoofs * (1 - 0.2) - 32) < 1e-9
assert spoofs * (1 - 0.5) == 20 and abs(spoofs * (1 - 0.8) - 8) < 1e-9

# The 95% is from a test set; invented size 200 attacks, 190 caught -> Wilson interval
n, k, z = 200, 190, 1.96
p = k / n
den = 1 + z * z / n
centre = (p + z * z / (2 * n)) / den
half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
lo, hi = centre - half, centre + half
assert abs(lo - 0.9104) < 0.002 and abs(hi - 0.9727) < 0.002
print(f"95% from 190/200: interval {lo:.1%} to {hi:.1%} -> {spoofs*(1-hi):.1f} to {spoofs*(1-lo):.1f} pass")

# Cost on genuine users: invented 1% fall back to human review
genuine = checks - spoofs
fallback = genuine * 0.01
assert genuine == 39_960 and abs(fallback - 399.6) < 1e-9
print(f"genuine users sent to fallback at 1%: {fallback:.1f} a day")
# Queue that a review team must handle: fallback plus caught spoofs
queue = fallback + caught
assert abs(queue - 437.6) < 1e-9
print(f"daily human-review queue ~ {queue:.1f} cases")
# Precision of the fallback queue
prec = caught / queue
assert abs(prec - 0.0868) < 1e-3
print(f"share of that queue that are real spoofs ~ {prec:.1%}")
```

**Output (my run):**
```text
spoofs/day=40, caught=38, pass liveness=2 (best case: known attacks only)
  catch 95%: 2 spoofs pass a day
  catch 80%: 8 spoofs pass a day
  catch 50%: 20 spoofs pass a day
  catch 20%: 32 spoofs pass a day
95% from 190/200: interval 91.0% to 97.3% -> 1.1 to 3.6 pass
genuine users sent to fallback at 1%: 399.6 a day
daily human-review queue ~ 437.6 cases
share of that queue that are real spoofs ~ 8.7%
```

**Follow-ups:**
- What if a deepfake attack appears? Block the pattern with a quick rule, add it to the red-team set, retrain, and use step-up for the risky band while it is fixed.
- How do you handle a rejected honest customer? A clear retry route and a human review path, because a hard rejection with no recourse is a harm in itself.
- How many human reviewers? Compute the queue (about 438 a day at the assumed 1% false-reject) times minutes per case; the review time is an input I would measure.

**Common mistakes:** Treating the known-attack catch rate as the real one. Ignoring false rejects of genuine users. One threshold with no middle band. No plan for new attack types. Storing biometrics without asking compliance. Using no subgroup checks.

### Q30 ⭐⭐ 🔴 Clinical note summarisation: An LLM tool will summarise 8,000 clinical notes a day across 12 hospitals, and you want an audit of a random daily sample of independent notes such that, if the true unsupported-note rate is exactly 2%, the sample contains at least one unsupported note with probability at least 95%. The audit should miss a true 2% rate with probability at most 5%. Design the rollout, safeguards and monitoring, compute the smallest daily audit size n with 1 minus 0.98 to the power n at least 0.95 and its share of the day's notes, and say what you would ask compliance.
**Asked at:** Healthcare and vision design material (a Dataford prompt on end-to-end ML for medical signal or image data, behind a sign-up wall, and an arXiv technology-readiness paper noting trust as a barrier in regulated fields; no triage-specific interview page was found); commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** ln 0.05 / ln 0.98 is 148.28, so the smallest daily audit is 149 notes, 1.86% of 8,000, which gives a 95% chance of seeing at least one unsupported note if the true rate is exactly 2%, and I would roll out in stages with every summary linked to its source note and a clinician in control.

**Clarifying questions:**
- What counts as an "unsupported claim" (a statement not in the note, a wrong drug or dose, an omission), and is the rate counted per note or per sentence? The 2% and the 149 are per note with at least one unsupported claim; I would define severity grades too.
- Who audits, and how good are they? An auditor who misses errors lowers the real detection chance; two auditors on a slice measure that.
- Are the 8,000 notes spread evenly across the 12 hospitals, and is the risk the same everywhere (specialty, language, note style)? A pooled sample can hide one bad hospital.
- Does the summary replace reading the note, or sit beside it? A clinician reading the summary instead of the note raises the stakes.
- Which errors are unacceptable regardless of rate (wrong allergy, wrong dose)? A rate target is not enough for those; they need hard checks.
- What does compliance and legal require for patient data, model use, audit records and sign-off? I ask; I do not state rules.

**Approach:** (about 8 steps; pacing for a 45-minute round: 4 / 5 / 5 / 5 / 8 / 8 / 5 / 5)
1. Clarify and frame (4 min). Goal: save clinician time without adding unsupported statements to the record. Define the error and say the sample-size maths aloud: 0.98 to the power 149 is 0.0493, below 5%.
2. Metrics and guardrails (5 min). Primary: unsupported-note rate (notes with at least one unsupported claim / notes audited), by severity. Guardrails: omission rate for key items (allergies, doses, diagnoses), clinician edit rate, time saved, complaints.
3. Data and labels (5 min). A gold set of notes with clinician-written summaries and error annotations. Audit labels need written guidelines and double review on a slice.
4. Baseline first (5 min). Extractive summary (selected sentences from the note) or a template of key fields, plus the clinician's current workflow. The LLM must beat it on errors, not on style.
5. Model and trade-offs (8 min). An LLM that must cite the source sentence for every claim, a check that each cited sentence supports the claim, and a block on high-risk fields unless they match the note exactly. Trade-off: stricter grounding reduces fabrication and also drops useful inference; accept shorter summaries. Human edits the summary before it enters the record at first.
6. Evaluate offline, then online (8 min). Offline: unsupported-note rate and omission rate on the gold set and on notes from each hospital, with intervals. Online: shadow mode, then one department, then hospitals in stages, with the daily random audit of 149 notes pooled and a stricter schedule at launch.
7. Monitoring, retraining and risks (5 min). The daily audit has limits: 149 notes detect a 2% rate with 95% probability, but a 1% true rate is caught only 77.6% of days, and 0.5% only 52.6%. Zero found in 149 means the rate is below about 1.99% with 95% confidence. Add automatic checks on every summary (citation present, high-risk fields match) and trend the weekly pooled audit.
8. Risks and cost (5 min). A pooled audit has about 12 notes per hospital, so a bad hospital hides; auditing 149 per hospital costs 1,788 notes a day (22.35%), so rotate hospitals or audit extra at launch. Cost is auditor time; ask compliance and legal about records, consent and who signs off.

**Metrics:**
- Unsupported-note rate = audited notes with at least one unsupported claim / audited notes.
- Detection probability = 1 - (1 - 0.02)^n, equal to 0.9507 at n = 149 (0.9497 at 148).
- Audit share = 149 / 8,000 = 1.86%.
- Omission rate = notes missing a required item (allergy, dose, diagnosis) / notes audited.
- Guardrails: clinician edit rate, per-hospital rate with intervals, time saved per note.

**Risks:**
- The audit is a detection rule for a 2% rate, not an estimate of the rate; one error in 149 gives a very wide interval.
- Independence matters: notes from one clinician or one hospital are correlated, so the real power is lower.
- Auditors miss errors; the true unsupported rate is higher than the audited one.
- A 2% rate may be too high for severe errors, which need their own zero-tolerance checks.
- Pooled sampling hides a bad hospital.

**What the interviewer scores:**
- Strong: derives 149 and 1.86%, and states what it guarantees and does not (95% chance of at least one at a 2% rate; weaker at lower rates). Weak: says "95% confident the rate is below 2%" with no condition.
- Strong: staged rollout with human review, citation grounding, hard checks on high-risk fields. Weak: "ship and monitor".
- Strong: notices the per-hospital hiding problem and its cost. Weak: ignores the 12 hospitals.
- Strong: asks compliance and legal and states no rules. Weak: invents them.

**Example:** Illustrative numbers. If the true rate is 1%, 149 notes catch at least one error on 77.6% of days; auditing each of 12 hospitals at 149 notes takes 1,788 notes a day, so I would rotate: one hospital a day at 149, each hospital every 12 days.
- Weak: "I would audit 5% of notes and see if the error rate is low."
- Strong: "149 notes a day, 1.86%, gives at least a 95% chance of catching at least one unsupported note if the rate is 2%. That is a tripwire, not a measurement, and at 1% it works 78% of the time. The sample is pooled over 12 hospitals, so I would add per-hospital rotation, automatic grounding checks on every summary, a clinician who edits before filing, and a staged launch. Legal and records questions go to compliance and legal."

**Code:**
```python
# Q30 audit sample size for unsupported-claim rate (illustrative)
import math
import numpy as np
p, notes, target = 0.02, 8_000, 0.95
n = math.ceil(math.log(1 - target) / math.log(1 - p))
assert n == 149 and 1 - (1 - p) ** n >= target > 1 - (1 - p) ** (n - 1)
share = n / notes
assert round(share * 100, 2) == 1.86
print(f"smallest n={n}, share of the day's notes={share:.2%}, detection prob at n: {1-(1-p)**n:.4f} (n-1: {1-(1-p)**(n-1):.4f})")

# Power at other true rates with n = 149
for r in (0.005, 0.01, 0.02, 0.03):
    print(f"  true rate {r:.1%}: P(at least one unsupported note in sample) = {1-(1-r)**n:.3f}")
assert abs((1 - 0.995 ** n) - 0.526) < 0.002 and abs((1 - 0.99 ** n) - 0.776) < 0.002

# If zero are found in 149: one-sided 95% upper bound for the rate
upper = 1 - 0.05 ** (1 / n)
assert abs(upper - 0.01987) < 1e-4
print(f"zero found in {n}: upper 95% bound on the rate = {upper:.2%}")

# Seeded simulation of the daily audit when the true rate is exactly 2%
rng = np.random.default_rng(5)
days = 200_000
hits = rng.binomial(n, p, size=days)
detect = (hits >= 1).mean()
assert abs(detect - 0.9506) < 0.005
print(f"simulated detection rate at 2% = {detect:.4f}")

# Per hospital: 12 hospitals, same guarantee for each
per_h_total = 12 * n
assert per_h_total == 1_788 and round(per_h_total / notes * 100, 2) == 22.35
print(f"same guarantee per hospital: {per_h_total} notes a day = {per_h_total/notes:.2%} of notes")
print(f"pooled sample gives {n/12:.1f} notes per hospital on average")
assert round(n / 12, 1) == 12.4
# Rotation alternative: each hospital gets the full 149 on one day of every 12-day cycle (invented schedule)
print(f"rotation: one hospital per day gets {n}; each hospital audited every 12 days")
```

**Output (my run):**
```text
smallest n=149, share of the day's notes=1.86%, detection prob at n: 0.9507 (n-1: 0.9497)
  true rate 0.5%: P(at least one unsupported note in sample) = 0.526
  true rate 1.0%: P(at least one unsupported note in sample) = 0.776
  true rate 2.0%: P(at least one unsupported note in sample) = 0.951
  true rate 3.0%: P(at least one unsupported note in sample) = 0.989
zero found in 149: upper 95% bound on the rate = 1.99%
simulated detection rate at 2% = 0.9504
same guarantee per hospital: 1788 notes a day = 22.35% of notes
pooled sample gives 12.4 notes per hospital on average
rotation: one hospital per day gets 149; each hospital audited every 12 days
```

**Follow-ups:**
- What do you do on the first unsupported note found? Review it, classify severity, check for a pattern (hospital, prompt, note type); one hit at a 2% rate is expected about twice per 100, so escalate on severity or a repeated pattern, not on a single mild case.
- How do you estimate the actual rate, not just trip on 2%? A larger weekly pooled sample with an interval: 1,000 notes at a 2% rate gives about plus or minus 0.9 points.
- Could an LLM do the audit? As a first-pass filter that picks notes for human review, yes, but humans must label the random sample, because an LLM judge shares blind spots with the summariser (see Book 6 Part 3, the question on one LLM labelling and judging).

**Common mistakes:** Calling the audit a 95% confidence that the rate is below 2% without the zero-found condition. Forgetting 149 is a minimum for a single pooled rate. Ignoring per-hospital differences. Assuming notes are independent. Treating audit rate as true rate when auditors miss errors. Stating legal rules as facts.

### Q31 ⭐⭐ 🔴 Two-tower retrieval: A catalogue has 20,000,000 items embedded in 128 dimensions of 4-byte floats, queries arrive at 3,000 per second at peak, and each node has 8 GB (decimal) of which 60% is usable for the index. One replica of the full index serves 1,200 queries per second. Design the candidate retrieval system, and compute the index size, nodes per replica, replicas for the peak and total nodes, ignoring index overhead.
**Asked at:** General ML system-design prep material (Educative's 6-step ML design framework and fraud-detection mock interview, DesignGurus, techinterview.org, PracHub's 2026 ML system design bank and a DEV Community guide describe open prompts such as feed or recommendation, search ranking and ad prediction, and one guide quotes a search prompt with 1,000 queries per second and 200 ms); commercial prep sites, so example numbers are treated as examples only; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** I would split it into a two-tower model, an offline item index and a replicated ANN service, and size it first: 20 million items x 128 x 4 bytes is 10.24 GB, 3 nodes per replica, 3 replicas for 3,000 queries per second, 9 nodes in total.

**Clarifying questions:**
- What is retrieval feeding (feed, search, ads) and what is the end-to-end latency budget? It sets how much of the budget retrieval may use, often a small slice.
- How many candidates must retrieval return (for example 500) and what recall of the final top results must it keep? That is the quality target for the ANN setting.
- How often does the catalogue change and how fresh must a new item be? It decides batch rebuild versus incremental inserts.
- What share of users and items are cold (no history)? Two-tower with content features handles items; new users need a fallback.
- Is 3,000 per second the true peak, and what failure headroom is wanted? The sizing below is exact for the peak and has no spare.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data 5, baseline 4, model 8, offline and online eval 8, launch and monitoring 6, risks and cost 5):**
1. Clarify and frame: retrieval is a recall job, ranking is a precision job. Agree the budget and the candidate count.
2. Metrics and guardrails: recall at K against the ranker's final picks, p99 retrieval latency, coverage of the catalogue, and a guardrail on diversity and on new-item exposure.
3. Data and labels: clicks and purchases as positives, in-batch or sampled negatives; watch popularity bias and position bias in the logs.
4. Baseline first: popularity plus category rules, then item-to-item co-occurrence. Anything fancier must beat these on recall at K.
5. Model and trade-offs: two towers (user and item encoders), item vectors computed offline, user vector at request time, ANN search over the item index. Size it: the index is 10.24 GB, one node holds 4.8 GB, so each replica needs 3 nodes (sharded); 3,000 / 1,200 gives 3 replicas (2.5 rounded up); total 9 nodes. Trade-off: lower precision (for example 8-bit vectors) can cut memory about four times, but recall must be measured (editor knowledge, not tested here).
6. Evaluation: offline recall at K and the ranker's lift on a holdout; then shadow traffic for latency and recall, then a 5% experiment on a business metric with guardrails.
7. Launch and monitoring: stage by region, keep the old retriever as fallback, rebuild the index on a schedule, watch embedding drift, p99 and the share of new items retrieved.
8. Risks and cost: 9 nodes has 83% utilisation at peak with no failure spare; N+1 means a fourth replica (12 nodes). Index overhead and updates will push the number up.

**Metrics:**
- Recall@K = final-ranked items that appear in the retrieved K / final-ranked items per request (K say 500).
- p99 retrieval latency (ms) at peak; replica utilisation = peak qps / (replicas x 1,200).
- Guardrails: catalogue coverage (distinct items retrieved / 20,000,000 per day), new-item exposure share, error and timeout rate.

**Risks:**
- Index overhead (graph links, metadata) is ignored in the prompt and is real; measure it.
- Popularity bias: the tower learns to retrieve what was already shown.
- Stale index: new items cannot be retrieved until the next build.
- Sharding adds a fan-out and a slowest-shard latency tail.
- Sizing at exactly the peak leaves nothing for a node loss or a campaign spike.

**What the interviewer scores:**
- Strong: gets 10.24 GB, 3, 3, 9 and states the rounding up and the assumption of no overhead.
- Strong: separates retrieval from ranking and judges retrieval on recall at K.
- Strong: names headroom and the quantisation trade-off with a measure.
- Weak: draws boxes with no numbers; sizes on the average; treats GB as GiB without saying.

**Example:** Illustrative numbers. Index 10.24 GB, usable per node 8 x 0.6 = 4.8 GB, 10.24 / 4.8 = 2.13, so 3 nodes. 3,000 / 1,200 = 2.5, so 3 replicas. 3 x 3 = 9 nodes.
- Weak: "I would use a vector database and scale it up if it is slow."
- Strong: "The index is 10.24 GB, a node gives me 4.8 GB, so each replica is three shards. Three replicas serve 3,600 queries a second against a 3,000 peak, so 9 nodes and 83% utilisation. I would ask for a fourth replica for failure headroom, and test 8-bit vectors, which could drop us to one node per replica if recall holds."

**Code:**
```python
import math
items, dim, bytes_per = 20_000_000, 128, 4
peak_qps, node_gb, usable, replica_qps = 3000, 8, 0.60, 1200
index_bytes = items * dim * bytes_per
usable_per_node = node_gb * 1e9 * usable
nodes_per_replica = math.ceil(index_bytes / usable_per_node)
replicas = math.ceil(peak_qps / replica_qps)
total = nodes_per_replica * replicas
print("index GB", index_bytes / 1e9, "usable per node GB", usable_per_node / 1e9)
print("nodes/replica", nodes_per_replica, "replicas", replicas, "total nodes", total)
assert index_bytes == 10_240_000_000 and usable_per_node == 4.8e9
assert nodes_per_replica == 3 and replicas == 3 and total == 9
# headroom view: 3 replicas serve 3,600 qps, so peak uses 3000/3600
util = peak_qps / (replicas * replica_qps)
print("replica utilisation at peak", round(util, 3))
assert round(util, 3) == 0.833
# losing one replica (N+1): 4 replicas = 12 nodes
assert math.ceil((peak_qps) / replica_qps) + 1 == 4 and 4 * nodes_per_replica == 12
# trade-off: int8 quantisation cuts the index 4x (editor knowledge, recall must be measured)
q_bytes = items * dim * 1
q_nodes = math.ceil(q_bytes / usable_per_node)
print("int8 index GB", q_bytes / 1e9, "nodes/replica", q_nodes, "total", q_nodes * replicas)
assert q_bytes == 2_560_000_000 and q_nodes == 1 and q_nodes * replicas == 3
```

**Output (my run):**
```text
index GB 10.24 usable per node GB 4.8
nodes/replica 3 replicas 3 total nodes 9
replica utilisation at peak 0.833
int8 index GB 2.56 nodes/replica 1 total 3
```

**Follow-ups:**
- *What if the catalogue doubles?* Index 20.48 GB, 5 nodes per replica (4.27 rounded up), 15 nodes. Check it with the same code.
- *Why not rank all 20 million items?* The ranker is too slow per item; retrieval narrows to hundreds first.
- *How do you handle new items?* Content-based item tower, a small fresh-items index, and an exploration slot.

**Common mistakes:** Forgetting to round up nodes and replicas. Mixing 1e9 and 2^30. Sizing for the average. Judging retrieval by click-through instead of recall at K.

### Q32 ⭐ 🟢 Predictive maintenance: A fleet of 500 delivery e-bikes sends a 200-byte sensor reading every 5 seconds over a mobile link, and each bike may upload at most 2,000,000 bytes a day. Design the anomaly detection for battery faults, which are rare, and compute the raw bytes per bike per day over 24 hours of continuous reporting and the reduction factor needed.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to predictive maintenance and sensor anomaly detection (adjacent to the Codemia anomaly-detection prompt); search snippets only, not opened
**Say this first (1 line):** Raw reporting is 3,456,000 bytes per bike per day against a 2,000,000 cap, so I need at least a 1.73x cut, and I would get it by summarising on the bike and uploading only the windows around suspicious events.

**Clarifying questions:**
- What does a battery fault cost (fire, a stranded rider, a replacement) and what lead time is useful? It sets how many false alerts are tolerable.
- Are there any labelled faults, or only maintenance records with dates? It decides supervised versus anomaly methods.
- Is the 2,000,000 bytes a hard cap or a cost target? A hard cap forces on-bike processing.
- What is the compute on the bike and can it run a small model? It decides where detection runs.
- How are faults defined (voltage sag, temperature rise, rapid capacity loss) and who acts on an alert? A rule nobody acts on has no value.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data and labels 6, baseline 6, model 8, evaluation 6, rollout and monitoring 6, risks and cost 4):**
1. Clarify and frame: predict a fault early enough to swap a battery, within a data cap.
2. Metrics and guardrails: recall of true faults with enough lead time, alerts per bike per month (workload), bytes per bike per day.
3. Data and labels: faults are rare, so label from maintenance and swap records; expect few positives and noisy dates.
4. Baseline first: threshold rules (voltage drop under load, temperature rise above a per-bike baseline). They are cheap, explainable and fit on the bike.
5. Model and trade-offs: robust per-bike baselines and a small anomaly score on summaries (rolling statistics); add a supervised model only when there are enough labelled faults. Bandwidth: raw is 17,280 readings x 200 = 3,456,000 bytes, factor needed 1.728. Options: one reading every 9 seconds (1.92 MB, loses detail), or a 400-byte summary a minute (576,000 bytes, a 6x cut) with about 118 sixty-reading event windows of spare cap.
6. Evaluation: replay history, measure recall at a fixed number of alerts, and check lead time; do not use accuracy.
7. Rollout: shadow alerts to the maintenance team, compare with their findings, then act on the top alerts; keep a fallback rule that works offline.
8. Monitoring and cost: alert precision from technician feedback, drift by battery age and season, cap usage per bike; retrain when the fault mix changes.

**Metrics:**
- Recall of faults = faults alerted at least N days before failure / all faults in the period.
- Precision of alerts = alerts that technicians confirm / alerts raised.
- Bytes per bike per day (guardrail <= 2,000,000) and alerts per bike per month.

**Risks:**
- Very few labelled faults; any recall number is a wide range.
- Summaries can hide the short spike that matters; keep an event-window upload.
- Seasonal heat and rider weight shift the baseline.
- Mobile dropouts create gaps that look like anomalies.

**What the interviewer scores:**
- Strong: computes 3,456,000 bytes and 1.728x, then chooses where processing happens.
- Strong: starts with rules, uses recall at an alert budget, and speaks about label scarcity.
- Weak: proposes a deep model with no labels; ignores the cap; quotes accuracy on rare faults.

**Example:** Illustrative numbers. 86,400 / 5 = 17,280 readings; x 200 B = 3,456,000 B; / 2,000,000 = 1.728.
- Weak: "Train an LSTM on all sensor data and flag anomalies."
- Strong: "Raw is 3.46 MB a day and the cap is 2 MB, so I need at least 1.73x. I would summarise each minute on the bike, which is about 0.58 MB, and keep the rest of the cap for raw windows around rule hits. I start with per-bike threshold rules, because I have few labelled faults."

**Code:**
```python
import math
bikes, rec_bytes, every_s, cap = 500, 200, 5, 2_000_000
readings = 24 * 3600 // every_s
raw = readings * rec_bytes
factor = raw / cap
print("readings/day", readings, "raw bytes/bike/day", raw, "reduction factor", round(factor, 3))
assert readings == 17_280 and raw == 3_456_000 and round(factor, 3) == 1.728
print("fleet raw GB/day", bikes * raw / 1e9)
assert bikes * raw == 1_728_000_000
# options to fit the cap (each must be >= 1.728x); sums are illustrative
send_every = math.ceil(every_s * factor)          # slower fixed rate
print("fixed-rate option: one reading every", send_every, "s ->", 86400 // send_every * rec_bytes, "bytes/day")
assert send_every == 9 and 86400 // 9 * 200 <= cap
# on-bike summary: 1 summary of 400 bytes per minute + event uploads
summary = 24 * 60 * 400
print("1-minute 400-byte summaries", summary, "bytes/day, factor", round(raw / summary, 2))
assert summary == 576_000 and round(raw / summary, 2) == 6.0
spare = cap - summary
print("spare for event windows (bytes/day)", spare, "= windows of 60 readings (12,000 B):", spare // 12_000)
assert spare // 12_000 == 118
```

**Output (my run):**
```text
readings/day 17280 raw bytes/bike/day 3456000 reduction factor 1.728
fleet raw GB/day 1.728
fixed-rate option: one reading every 9 s -> 1920000 bytes/day
1-minute 400-byte summaries 576000 bytes/day, factor 6.0
spare for event windows (bytes/day) 1424000 = windows of 60 readings (12,000 B): 118
```

**Follow-ups:**
- *Why not just send every 9 seconds?* It fits (1.92 MB) but loses the short event; summaries plus windows keep the shape of the spike.
- *Which metric with so few faults?* Recall at a fixed alert budget, with a range from the few positives.

**Common mistakes:** Forgetting per-day conversion. Treating the cap as per fleet. Quoting accuracy. Training before there is a rule baseline.

### Q33 ⭐ 🟢 Intent labelling: A support team has a labelling budget of 6,000 rupees at 3 rupees per label for a Hinglish ticket classifier with 10 intents, and the rarest intent is 3% of tickets (a measured sample share). Design the data and label plan, and compute the labels bought and the rare-intent examples expected from a purely random sample, then say how you would reach 200 of them.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to labelling plans for code-mixed text classification (no page found in these searches); search snippets only, not opened
**Say this first (1 line):** 6,000 rupees at 3 each buys 2,000 labels, a random sample gives about 60 examples of the 3% intent, so to reach 200 I would mix a small random slice with targeted sampling instead of buying 6,667 random labels.

**Clarifying questions:**
- Do all 10 intents matter equally, or is the rare one costly when missed? It decides whether 200 examples is worth the budget.
- How was the 3% measured, and from what period? It is a sample share, so the true share could be 2% or 4%.
- Can annotators handle Hinglish consistently, and what is their agreement? Noisy labels waste the budget.
- Do I have unlabelled tickets and an embedding or keyword search? That makes targeted sampling possible.
- Is there any existing label history, for example agent tags? Weak labels can seed the search.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data and labels 12, baseline 5, model 6, evaluation 6, rollout and monitoring 4, risks and cost 3):**
1. Clarify and frame: a classifier whose weakest intent is the rare one; the label budget is the main constraint.
2. Metrics and guardrails: per-intent recall and precision (macro average), with the rare intent reported alone, plus label agreement.
3. Data and labels: 6,000 / 3 = 2,000 labels. Random sample gives 2,000 x 0.03 = 60 rare examples (standard deviation about 7.6), and 40 to 80 if the true share is 2% to 4%. For 200 rare examples at random you need 200 / 0.03 = 6,667 labels, 20,001 rupees, 3.3 times the budget.
4. Baseline first: keyword rules and a TF-IDF plus logistic model on character n-grams (suits mixed Hinglish spelling), which also finds rare-intent candidates.
5. Model and trade-offs: plan 800 random labels (unbiased share and a clean test set) and 1,200 targeted ones from keyword or embedding search for the rare intent. At 30% precision of that pool that is about 360 rare examples; even at 15% it is 1,200 x 0.15 + 24 = 204. Then a small fine-tuned multilingual encoder or a prompted LLM with few-shot examples (editor knowledge: compare both on the same test set).
6. Evaluation: keep the random slice as the test set, label it twice on a subset to measure agreement, and report the rare intent with a range.
7. Rollout: shadow the classifier, send low-confidence tickets to humans, and use their corrections as new labels.
8. Monitoring and cost: weekly sample for the intent mix, retrain when a new intent appears, track label cost per rare example found.

**Metrics:**
- Rare-intent recall = rare tickets predicted rare / rare tickets in the random test slice (with its range).
- Label yield = rare examples found / labels bought.
- Guardrails: annotator agreement (for example Cohen's kappa), macro F1 across all 10 intents.

**Risks:**
- Targeted examples are not representative: use them for training only, never to estimate prevalence or test accuracy.
- The 800 random labels hold only about 24 rare tickets, so the rare-intent test is noisy.
- Keyword search finds only the easy phrasings.
- Hinglish spelling variants split the same intent.

**What the interviewer scores:**
- Strong: 2,000 labels, 60 expected, 6,667 and 20,001 needed, and a mixed plan with a test set kept random.
- Strong: says the 3% is a sample and shows 40 to 80.
- Weak: "label everything randomly" or "oversample" without noting the bias.

**Example:** Illustrative numbers. 6,000 / 3 = 2,000 labels; 2,000 x 0.03 = 60; 200 / 0.03 = 6,667 labels.
- Weak: "We will get 60 rare examples, that should be enough, we can use class weights."
- Strong: "A random sample gives about 60, with a range of 40 to 80 if the share is really 2 to 4 percent. To reach 200 I would spend 800 labels randomly for a clean test set and 1,200 on tickets found by keyword and embedding search. Even at 15 percent hit rate that gives about 204."

**Code:**
```python
import math
from statistics import NormalDist
budget, price, rare_share, target = 6000, 3, 0.03, 200
labels = budget // price
exp_rare = labels * rare_share
sd = math.sqrt(labels * rare_share * (1 - rare_share))
print("labels", labels, "expected rare", exp_rare, "sd", round(sd, 2))
assert labels == 2000 and round(exp_rare) == 60 and round(sd, 2) == 7.63
random_needed = math.ceil(target / rare_share)
print("random labels for 200 rare:", random_needed, "cost", random_needed * price, "x budget", round(random_needed * price / budget, 2))
assert random_needed == 6667 and random_needed * price == 20_001
# 5th-95th percentile band if the true share is only 2% or 4% (the 3% is a sample)
for s in (0.02, 0.03, 0.04):
    print("true share", s, "expected rare", labels * s)
assert labels * 0.02 == 40 and labels * 0.04 == 80
# targeted sampling: labels needed if a search/model-assisted pool has precision p for the rare intent
spend_rare = 1200  # labels from the enriched pool (illustrative split)
for p in (0.15, 0.30, 0.50):
    need = math.ceil(target / p)
    print("pool precision", p, "labels for 200 rare", need, "fits 2000:", need <= labels)
assert math.ceil(200 / 0.15) == 1334 and math.ceil(200 / 0.30) == 667 and math.ceil(200 / 0.50) == 400
# split plan: 800 random labels (unbiased share + base rates) + 1,200 enriched
rand_part, enr_part = 800, 1200
rare_random = rand_part * rare_share
rare_enriched = enr_part * 0.30
print("rare from random", rare_random, "from enriched at 30%", rare_enriched, "total", rare_random + rare_enriched)
assert rare_random == 24 and round(rare_enriched) == 360 and rand_part + enr_part == labels
# even at 15% precision: 1,200 * 0.15 + 24 = 204 >= 200
assert round(enr_part * 0.15 + rare_random) == 204
# weights: enriched examples must be down-weighted (or kept out) when estimating real prevalence
```

**Output (my run):**
```text
labels 2000 expected rare 60.0 sd 7.63
random labels for 200 rare: 6667 cost 20001 x budget 3.33
true share 0.02 expected rare 40.0
true share 0.03 expected rare 60.0
true share 0.04 expected rare 80.0
pool precision 0.15 labels for 200 rare 1334 fits 2000: True
pool precision 0.3 labels for 200 rare 667 fits 2000: True
pool precision 0.5 labels for 200 rare 400 fits 2000: True
rare from random 24.0 from enriched at 30% 360.0 total 384.0
```

**Follow-ups:**
- *How do you estimate prevalence after targeted labelling?* Only from the random slice, or by weighting by the inverse sampling probability.
- *Active learning?* Yes, after the first model: label the tickets near the decision boundary, then keep a random slice.

**Common mistakes:** Testing on the targeted sample. Quoting 3% as exact. Spending all labels before checking annotator agreement. Ignoring cost of a second annotator.

### Q34 ⭐ 🟡 Quick-commerce stocking: A dark store sells a perishable item whose daily demand is roughly normal with mean 100 and standard deviation 20 (a measured estimate). A missed sale loses 30 rupees of margin and each unsold unit loses 20 rupees. Design the forecasting and stocking solution, and compute the critical ratio and the stock level that follows from it (to the nearest whole unit).
**Asked at:** ETA, forecasting and pricing design material (a CleverPrep Lyft ML engineer page listing real-time pricing, city-level demand forecasting with cold start and ETA-with-traffic prompts, an AlgoMaster ETA design page, Codemia demand-forecasting pipeline prompts and an AI Engineering Insider dynamic-pricing piece); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** The critical ratio is 30 / (30 + 20) = 0.6, so I stock the 60th percentile of demand, 100 + 0.2533 x 20 = about 105 units, a little above the mean.

**Clarifying questions:**
- Is the 20 rupees per unsold unit the net loss (cost minus salvage)? It is the overage cost in the formula.
- Is the 30 rupees the margin lost, with no goodwill effect? A lost customer may cost more.
- Is the 100 and 20 measured on sales or on true demand? Sales are censored when you stock out, so demand is understated.
- How long is the shelf life and how often can I reorder? One-period stocking needs a single order each day.
- Is demand for this store-item-day normal enough, and does it vary by weekday and weather? The shape affects the answer.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data 5, baseline 5, model 8, evaluation 7, rollout and monitoring 7, risks and cost 4):**
1. Clarify and frame: a one-period stocking decision, so forecast a distribution, not a point.
2. Metrics and guardrails: expected cost = 20 x unsold + 30 x missed sales, fill rate, waste share, forecast calibration.
3. Data and labels: daily sales per store and item, with stock-out flags, promotions, weekday, weather; correct for censoring.
4. Baseline first: same weekday last week or a seven-day average, with an error-based standard deviation.
5. Model and trade-offs: a model for the mean (gradient boosting or a simple regression) and a calibrated spread; or a direct 0.6 quantile model. Critical ratio 30 / 50 = 0.6, z = 0.2533, stock 105.07. To the nearest whole unit the stock is 105 (the continuous rule that rounds up gives 106; the cost difference is under a rupee a day, and pack size may decide). Compare with stocking the mean: expected cost 398.94 against 386.34, about 12.6 rupees a day better (illustrative).
6. Evaluation: backtest the whole decision (cost with the rule against cost with the baseline), and check that demand stays below stock on about 60% of days.
7. Launch: A/B across stores, perhaps 10% of stores first, compare waste and fill rate; keep a manual override.
8. Monitoring and cost: weekly calibration of the 0.6 quantile, drift in demand spread, shrink the model back to the baseline if it loses.

**Metrics:**
- Service level = days with demand <= stock / days (target 0.6 from the ratio, a result, not a goal to set separately).
- Expected daily cost = (20 x units unsold + 30 x units short) per store-item-day.
- Guardrails: waste share = unsold units / units stocked, fill rate = units sold / units demanded.

**Risks:**
- Censored sales understate demand and the spread; if the real spread is 30, the stock would be 107.6.
- Normality fails for lumpy or intermittent items.
- Margin and waste costs differ by item; one ratio does not fit all.
- Substitution: when this item is out, demand moves to another.

**What the interviewer scores:**
- Strong: 0.6, z = 0.2533, 105 (nearest whole unit), and explains why the answer is above the mean.
- Strong: raises censoring and calibrates a quantile, then tests the decision, not just forecast error.
- Weak: stocks the mean or the mean plus a safety factor with no cost logic.

**Example:** Illustrative numbers. 30 / 50 = 0.6; z = 0.2533; 100 + 0.2533 x 20 = 105.07.
- Weak: "Forecast demand of 100 and stock 100, maybe a bit more to be safe."
- Strong: "A missed sale costs 30 and an unsold unit costs 20, so the critical ratio is 0.6 and I stock the 60th percentile, about 105. I would check that the spread of 20 comes from true demand, not stocked-out sales."

**Code:**
```python
from statistics import NormalDist
import math
mu, sd, cu, co = 100, 20, 30, 20
cr = cu / (cu + co)
z = NormalDist().inv_cdf(cr)
q = mu + sd * z
print("critical ratio", cr, "z", round(z, 4), "stock", round(q, 2))
assert cr == 0.6 and round(z, 4) == 0.2533 and round(q, 2) == 105.07
# integer stock: the smallest integer with P(D <= Q) >= 0.6 (continuous normal)
Q = math.ceil(q)
print("integer stock (continuous rule rounds up)", Q, "P(D<=Q)", round(NormalDist(mu, sd).cdf(Q), 4))
assert NormalDist(mu, sd).cdf(105) < 0.6 <= NormalDist(mu, sd).cdf(106)
# expected profit-loss (cost) at a few stocks by Monte Carlo-free numeric integration
nd = NormalDist(mu, sd)
def exp_cost(Q):
    lo, hi = mu - 6 * sd, mu + 6 * sd
    n = 20000; h = (hi - lo) / n; tot = 0.0
    for i in range(n):
        d = lo + (i + 0.5) * h
        tot += nd.pdf(d) * h * (co * max(Q - d, 0) + cu * max(d - Q, 0))
    return tot
for s in (100, 105, 106, 110):
    print("stock", s, "expected cost", round(exp_cost(s), 2))
assert exp_cost(105) < exp_cost(100) and exp_cost(105) < exp_cost(110)
c100, c105 = exp_cost(100), exp_cost(105)
print("saving per day vs stocking the mean", round(c100 - c105, 2), "rupees (illustrative)")
assert round(c100 - c105, 1) == 12.6
# demand sd matters: if the true sd is 30 (stockout-censored history), stock moves
q30 = mu + 30 * z
print("stock if sd were 30:", round(q30, 2))
assert round(q30, 2) == 107.6
```

**Output (my run):**
```text
critical ratio 0.6 z 0.2533 stock 105.07
integer stock (continuous rule rounds up) 106 P(D<=Q) 0.6179
stock 100 expected cost 398.94
stock 105 expected cost 386.34
stock 106 expected cost 386.76
stock 110 expected cost 397.8
saving per day vs stocking the mean 12.6 rupees (illustrative)
stock if sd were 30: 107.6
```

**Follow-ups:**
- *What if the missed sale cost doubles to 60?* The ratio becomes 60 / 80 = 0.75, z = 0.674, stock about 113.5.
- *What about a lead time of several days?* Use demand over the lead time plus review period and the same ratio logic.

**Common mistakes:** Using the ratio the wrong way (20 / 50). Stocking the mean. Ignoring censored data. Reporting accuracy of the forecast without testing the cost.

### Q35 ⭐ 🟡 LLM catalogue enrichment: A marketplace wants an LLM to enrich 3,000,000 listings in several Indian languages within 24 hours, using about 1,000 generated tokens per listing, and one serving cluster generates 20,000 tokens per second. Design the pipeline with quality checks, and compute the total tokens, the cluster-hours of work and the clusters needed for the deadline.
**Asked at:** Agentic and GenAI design material (Dataford agentic AI engineer guides listing multi-step customer-service workflows, techinterview.org and aiforanything.io pages on AI agent infrastructure and system design, and a post-LLM-era ML engineer interview guide saying 'design an LLM-based system for X' is now the most common prompt); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** 3 million listings x 1,000 tokens is 3 billion tokens, 150,000 seconds or 41.67 cluster-hours, so two clusters meet the 24-hour deadline at 87% utilisation with little room for reruns.

**Clarifying questions:**
- Is the 20,000 tokens per second a generation rate, and is the prompt extra? The prompt states 1,000 generated tokens per listing; prompt processing is faster but I would still measure it (editor knowledge).
- What does enrichment produce (attributes, translated titles, descriptions), and is a wrong attribute worse than a missing one? It sets the quality bar.
- Is 24 hours a one-off backfill or a recurring job? One-off can use spare capacity; recurring needs a steady-state design.
- Which languages and what review capacity do I have per language? Quality varies by language.
- Can enriched content appear without review, and who owns wrong claims? Ask compliance about any claim rules; I make none.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data 4, baseline 5, model and pipeline 10, evaluation 7, launch 5, monitoring and cost 5):**
1. Clarify and frame: a bulk backfill with a deadline, not a chat product.
2. Metrics and guardrails: attribute accuracy per language on an audited sample, schema-valid rate, unsupported-claim rate, cost per listing.
3. Data and labels: a gold set of listings checked by people for each language.
4. Baseline first: rules and a small extraction model for easy attributes; the LLM covers the rest.
5. Model and pipeline: prompt with a strict schema, batch inference, validators (schema, allowed values, language check), a second cheaper check, and a human queue for failures. Sizing: 3,000,000,000 tokens / 20,000 = 150,000 s = 41.67 hours; / 24 = 1.74, so 2 clusters. With 10% redone, 45.8 hours still fits two (95.5% utilisation); at 15% it is 99.8%; at 20% it needs three.
6. Evaluation: audit about 385 listings per language (worst-case margin about 5 points), compare with the gold set before the full run.
7. Launch: pilot on 1% (30,000 listings), then run in batches with a kill switch; publish through an A/B on a category before all.
8. Monitoring and cost: validator failure rate per batch, drift by language, tokens spent per listing, rerun share; keep a checkpoint so a failed batch restarts without redoing the rest.

**Metrics:**
- Attribute accuracy = correct attributes / audited attributes, per language.
- Schema-valid rate = outputs passing the validator / outputs.
- Throughput = tokens per second achieved / 20,000; redo share = listings re-run / listings.

**Risks:**
- Throughput quoted for the cluster may fall with long prompts or small languages with more tokens per word.
- Hallucinated attributes enter the catalogue; a wrong size or material has a real cost.
- No spare capacity at 87%; a failure loses the deadline.
- Token counts differ by language, so 1,000 average hides a heavy tail.

**What the interviewer scores:**
- Strong: gets 3 billion tokens, 41.67 hours, 2 clusters, and talks about headroom and redo rate.
- Strong: validators, human queue and per-language audits, not one overall accuracy.
- Weak: ignores deadline arithmetic; sends everything to the LLM with no checks.

**Example:** Illustrative numbers. 3,000,000 x 1,000 = 3 x 10^9; / 20,000 = 150,000 s = 41.67 h; / 24 h = 1.74 clusters, so 2.
- Weak: "We will run the LLM on all listings and fix errors later."
- Strong: "Three billion tokens at 20,000 a second is 41.7 cluster-hours, so two clusters for 24 hours, 87% busy. If 15% of listings are redone I am at 99.8%, so I want either a third cluster for a few hours or a validator that keeps redo below 10%."

**Code:**
```python
import math
listings, tok, rate, hours = 3_000_000, 1000, 20_000, 24
total = listings * tok
secs = total / rate
cluster_hours = secs / 3600
clusters = math.ceil(cluster_hours / hours)
print("tokens", total, "seconds", secs, "cluster-hours", round(cluster_hours, 2), "clusters", clusters)
assert total == 3_000_000_000 and secs == 150_000 and round(cluster_hours, 2) == 41.67 and clusters == 2
# utilisation of 2 clusters and headroom for reruns
cap_h = clusters * hours
print("capacity hours", cap_h, "utilisation", round(cluster_hours / cap_h, 3))
assert round(cluster_hours / cap_h, 3) == 0.868
# if 10% fail quality checks and are redone, and 5% are retried for format errors
for redo in (0.10, 0.15, 0.20):
    h = cluster_hours * (1 + redo)
    print("redo", redo, "hours", round(h, 2), "clusters", math.ceil(h / 24), "util at 2:", round(h / 48, 3))
assert math.ceil(cluster_hours * 1.10 / 24) == 2 and math.ceil(cluster_hours * 1.20 / 24) == 3
assert round(cluster_hours * 1.15 / 48, 3) == 0.998
# audit sample: 400 random listings per language batch gives margin ~ +-5 points at worst case
n = 385
moe = 1.96 * math.sqrt(0.25 / n)
print("n", n, "worst-case 95% margin", round(moe, 3))
assert round(moe, 3) == 0.05
# 1,000 tokens assumed to be all generated at the quoted rate (conservative: prefill is usually faster)
```

**Output (my run):**
```text
tokens 3000000000 seconds 150000.0 cluster-hours 41.67 clusters 2
capacity hours 48 utilisation 0.868
redo 0.1 hours 45.83 clusters 2 util at 2: 0.955
redo 0.15 hours 47.92 clusters 2 util at 2: 0.998
redo 0.2 hours 50.0 clusters 3 util at 2: 1.042
n 385 worst-case 95% margin 0.05
```

**Follow-ups:**
- *What about the prompt tokens?* They are extra work on top of the 1,000 generated; input is usually processed faster, so measure both rates (editor knowledge).
- *How do you cut cost?* Use a smaller model for easy attributes and cache repeated listing templates; compare quality first.

**Common mistakes:** Forgetting to round up clusters. No redo allowance. One accuracy figure for all languages. No staged rollout.

### Q36 ⭐ 🟡 Real-time fraud features: A card network keeps 10,000,000 active cards with 40 numeric features each at 8 bytes per value in an online store, with events arriving at 25,000 per second and a feature freshness target of 5 seconds. Design the real-time feature pipeline, and compute the memory (in decimal GB) for one copy of the online store and the events that arrive in one 5-second freshness window.
**Asked at:** Fraud-detection design material (an Educative fraud-detection mock interview, a PracHub real-time payment fraud prompt with a 50 ms budget and prep guides that call fraud the prompt where probabilities, thresholds and feature freshness must be discussed); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** One copy of the online store is 10 million x 40 x 8 bytes = 3.2 GB, and 25,000 events a second means 125,000 events in each 5-second freshness window, so the design is a stream processor updating a keyed store.

**Clarifying questions:**
- Is the 5 seconds from event to feature visible at scoring time, and is it a p99 target? It sets the pipeline budget.
- What is the scoring latency budget and what happens on a feature miss? A default and a fallback model are needed.
- Which features are windowed counts and which are slow profile values? Slow ones do not need streaming.
- Is training done from the same feature definitions? Training-serving skew is the classic fraud failure.
- How many copies and regions are needed? The 3.2 GB is one copy only.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data and labels 5, baseline 4, features and model 10, evaluation 6, launch 6, monitoring and cost 5):**
1. Clarify and frame: authorisation-time scoring with fresh velocity features.
2. Metrics and guardrails: feature age p99, missing-feature rate, scoring p99, fraud recall at a fixed false-decline rate.
3. Data and labels: chargebacks arrive late, so label with a delay and use confirmed reports for fast signals.
4. Baseline first: rules on a few velocity counts (card used in N places in 10 minutes), then a model.
5. Pipeline and trade-offs: events into a log, a stream job updating windowed counters, a keyed online store; the same definitions write to an offline store for training. Memory: 3,200,000,000 B = 3.2 decimal GB (2.98 GiB), 3 copies with an assumed 1.5x overhead is 14.4 GB. Window: 25,000 x 5 = 125,000 events, at most 1.25% of cards touched per window. A 1-hour counter in 5-second buckets is 720 buckets per card per counter, which is why you keep a few counters, not many.
6. Evaluation: offline with point-in-time features (no leakage), then shadow scoring on live traffic to measure feature age and score agreement.
7. Launch: shadow, then a small share of traffic with a human review band, with a fail-safe if freshness slips.
8. Monitoring and cost: feature age, null rate, distribution drift against training, store memory growth, reprocessing plan for late events.

**Metrics:**
- Feature freshness = scoring time minus the last event time included in the feature, p99 (target 5 s).
- Missing-feature rate = scored events with a default feature / scored events.
- Fraud recall at a fixed review rate; false-decline rate = good transactions blocked / good transactions.

**Risks:**
- Training-serving skew when offline and online code differ.
- Late and out-of-order events change window counts.
- A hot card (a merchant test attack) skews one key.
- Memory is per copy: replication, overhead and growth multiply the 3.2 GB.

**What the interviewer scores:**
- Strong: 3.2 GB, 125,000 per window, with units and "one copy" said aloud.
- Strong: one feature definition for training and serving; point-in-time training data.
- Weak: names tools only; sizes memory without replication; leakage in training.

**Example:** Illustrative numbers. 10,000,000 x 40 x 8 = 3,200,000,000 B; 25,000 x 5 = 125,000.
- Weak: "Use Kafka and Redis, it will be real time."
- Strong: "One copy is 3.2 GB, so three copies with overhead is under 15 GB, a small store. The harder part is correctness: 125,000 events land in every window, so I need late-event handling and one definition of each feature shared by training and serving."

**Code:**
```python
cards, feats, bpv, eps, fresh = 10_000_000, 40, 8, 25_000, 5
mem = cards * feats * bpv
print("bytes", mem, "GB (decimal)", mem / 1e9, "GiB", round(mem / 2**30, 3))
assert mem == 3_200_000_000 and round(mem / 2**30, 3) == 2.980
window = eps * fresh
print("events in one 5 s window", window)
assert window == 125_000
# share of cards touched in 5 s if events spread evenly (upper bound on distinct cards)
print("max share of cards updated in a window", window / cards)
assert window / cards == 0.0125
# with 3 copies (replication) and 1.5x key/overhead allowance (assumption, measure it)
copies, overhead = 3, 1.5
print("3 copies with 1.5x overhead GB", mem * copies * overhead / 1e9)
assert mem * copies * overhead == 14_400_000_000
# per-event write fan-out: a 40-feature update at 25k/s
writes = eps * 1  # one row write per event if features are stored as one row per card
print("row writes/s", writes, "bytes/s of values", eps * feats * bpv)
assert eps * feats * bpv == 8_000_000
# window features: a 1-hour sliding count with 5 s buckets needs 720 buckets per card per counter
buckets = 3600 // 5
print("buckets per counter", buckets)
assert buckets == 720
```

**Output (my run):**
```text
bytes 3200000000 GB (decimal) 3.2 GiB 2.98
events in one 5 s window 125000
max share of cards updated in a window 0.0125
3 copies with 1.5x overhead GB 14.4
row writes/s 25000 bytes/s of values 8000000
buckets per counter 720
```

**Follow-ups:**
- *Is 5 seconds a pipeline or a feature property?* Both: event-to-store lag plus the window update interval; measure it end to end.
- *What if the store is down?* Default features, a simpler fallback rule model, and an alert; decide fail-open or fail-closed with the business.

**Common mistakes:** Quoting memory for one copy as the total. Mixing GB and GiB. Training with features computed after the event. No default for a missing feature.

### Q37 ⭐ 🟡 Vernacular autocomplete: A shopping app expects 4,000 searches per second at peak in 8 languages, sends an average of 3 suggestion requests per search because of typing pauses, and each suggestion call has a 50 ms budget at the 99th percentile. Design the autocomplete system for Hinglish and native-script queries, and compute the suggestion requests per second and the instances needed if one instance serves 2,500 per second and you run it at 60% utilisation.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to vernacular and Hinglish autocomplete (no page found in these searches); search snippets only, not opened
**Say this first (1 line):** 4,000 searches a second at 3 requests each is 12,000 suggestion calls a second, and at 2,500 per instance run at 60% I need 12,000 / 1,500 = 8 instances.

**Clarifying questions:**
- Is the 4,000 searches per second the peak for the whole app or per region? It sets the number to size to.
- Is the 3 requests per search measured, and does it include debouncing? Typing behaviour changes it a lot.
- Is the 2,500 per second per instance measured at the 50 ms p99 budget? Throughput without a latency condition is meaningless.
- What query mix: Hinglish in Latin script, native scripts, and mixed? It drives normalisation and the index.
- How fresh must trending and new product terms be? It sets the rebuild cadence.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data 6, baseline 5, model 8, evaluation 7, launch 5, monitoring and cost 5):**
1. Clarify and frame: a very low latency suggestion service, with a ranking quality bar.
2. Metrics and guardrails: suggestion acceptance (clicks on a suggestion / sessions with suggestions shown), keystrokes saved, p99 latency, zero-result rate per language.
3. Data and labels: query logs, clicked suggestions, product titles; transliteration variants map Hinglish spellings to one form.
4. Baseline first: a prefix trie ranked by popularity per language, with a spelling-variant table. It is fast and is hard to beat on latency.
5. Model and trade-offs: add a light reranker on personal and recent signals only for the top candidates; keep the heavy model offline. Sizing: 12,000 per second; one instance at 60% gives 1,500; 8 instances; with one down, 7 instances run at 68.6%, so I would plan 9. A prefix cache with a 30% hit rate drops backend load to 8,400 per second, 6 instances; with 50% hits, 4 (cache hit rates are assumptions to measure). Budget for 50 ms p99, illustrative split: 10 network, 5 normalise, 15 retrieve, 15 rank, 5 slack.
6. Evaluation: offline mean reciprocal rank on logged completions per language; then an A/B on search success and time to first result.
7. Launch: one language group at a time, with the old autocomplete as fallback; client debouncing so requests per search falls.
8. Monitoring and cost: p99 and error rate per region, quality per language (small languages get their own dashboard), index refresh age.

**Metrics:**
- Acceptance rate = searches where a suggestion was selected / searches where suggestions were shown, per language.
- Suggestion requests per second = searches per second x requests per search (12,000 here).
- Guardrails: p99 latency at most 50 ms, zero-result rate, offensive-suggestion reports.

**Risks:**
- Average quality hides small languages; report per language.
- Offensive or sensitive suggestions from raw logs; filter and review (ask the policy team).
- Typing bursts exceed the 3 average; peak per second may be higher.
- Transliteration errors send Hinglish users to empty results.

**What the interviewer scores:**
- Strong: 12,000, 1,500, 8, plus N+1 and a latency condition on the throughput.
- Strong: trie baseline first, rerank only a few candidates, per-language measurement.
- Weak: a large neural model on the hot path; sizing at 100% utilisation.

**Example:** Illustrative numbers. 4,000 x 3 = 12,000; 2,500 x 0.6 = 1,500; 12,000 / 1,500 = 8.
- Weak: "Use a transformer to generate completions for every keystroke."
- Strong: "That is 12,000 calls a second and 8 instances at 60% load. I would serve a trie per language with transliteration variants, rerank the top 20 with a light model, and cut load with debouncing and a prefix cache, then check the cache hit rate before shrinking the fleet."

**Code:**
```python
import math
searches, per, cap, util = 4000, 3, 2500, 0.60
rps = searches * per
eff = cap * util
inst = math.ceil(rps / eff)
print("requests/s", rps, "effective per instance", eff, "instances", inst, "exact", rps / eff)
assert rps == 12_000 and eff == 1500 and inst == 8 and rps / eff == 8.0
# utilisation with one instance down
print("util with 7 instances", round(rps / (7 * cap), 3), "with 9 (N+1) minus one", round(rps / (8 * cap), 3))
assert round(rps / (7 * cap), 3) == 0.686 and round(rps / (8 * cap), 3) == 0.6
# debounce + prefix cache lever: if 30% of calls are cache hits, backend load falls
for hit in (0.0, 0.3, 0.5):
    load = rps * (1 - hit)
    print("cache hit", hit, "backend rps", load, "instances", math.ceil(load / eff))
assert math.ceil(rps * 0.7 / eff) == 6 and math.ceil(rps * 0.5 / eff) == 4
# if the real mean is 4 requests per search the answer moves
assert math.ceil(searches * 4 / eff) == 11
# p99 budget: 50 ms total; illustrative split
budget = {"network+gateway": 10, "normalise/transliterate": 5, "retrieve prefix/trie": 15, "rank top-k": 15, "slack": 5}
print(budget, sum(budget.values()))
assert sum(budget.values()) == 50
```

**Output (my run):**
```text
requests/s 12000 effective per instance 1500.0 instances 8 exact 8.0
util with 7 instances 0.686 with 9 (N+1) minus one 0.6
cache hit 0.0 backend rps 12000.0 instances 8
cache hit 0.3 backend rps 8400.0 instances 6
cache hit 0.5 backend rps 6000.0 instances 4
{'network+gateway': 10, 'normalise/transliterate': 5, 'retrieve prefix/trie': 15, 'rank top-k': 15, 'slack': 5} 50
```

**Follow-ups:**
- *What if requests per search is really 4?* 16,000 per second, 11 instances (10.67 rounded up).
- *Why 60% utilisation?* Headroom for bursts and for one node loss while holding the p99; the number should come from a load test.

**Common mistakes:** Forgetting the 3x multiplier. Using 100% utilisation. One quality number for all 8 languages. Putting the heavy model on the hot path.

### Q38 ⭐ 🔴 Autonomous remediation: An operations agent can restart services itself, saving 800 rupees of manual handling when right and costing 20,000 rupees when wrong, and it was right in 388 of 400 past incidents replayed offline (a sample, 97%). Design the autonomy levels, guardrails and rollout, and compute the break-even accuracy and compare the sample's accuracy with it.
**Asked at:** Agentic and GenAI design material (Dataford agentic AI engineer guides listing multi-step customer-service workflows, techinterview.org and aiforanything.io pages on AI agent infrastructure and system design, and a post-LLM-era ML engineer interview guide saying 'design an LLM-based system for X' is now the most common prompt); prep-site material; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** Break-even accuracy is 20,000 / 20,800 = 96.15%, the replay's 97% sits only a little above it with an interval that crosses it, so I would not give the agent full autonomy; I would start with suggestions and approvals and widen autonomy as live evidence builds.

**Clarifying questions:**
- Is 20,000 rupees the whole cost of a wrong restart, or the extra cost on top of the lost saving? It is the loss term in the break-even.
- Were the 400 replayed incidents random or the easy ones? A sample from a biased set overstates accuracy.
- Do errors cluster by service (a database restart is not like a stateless one)? Averages hide the dangerous cases.
- Can a restart be undone quickly, and what is the blast radius? It changes how much risk is tolerable.
- Who is on call and how fast can a human intervene? It decides which autonomy level fits.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 5, data 5, baseline 4, model and autonomy design 10, evaluation 6, rollout 6, monitoring and risks 4):**
1. Clarify and frame: a decision under unequal costs, so the threshold comes from the cost ratio.
2. Metrics and guardrails: accuracy of the action (right action / actions taken), cost per incident, rollback rate, incidents made worse.
3. Data and labels: replayed incidents with an expert label of the correct action; add live shadow decisions.
4. Baseline first: runbook rules and the current manual handling cost.
5. Model and autonomy levels: L0 recommend only, L1 act after one-click approval, L2 act alone on low-risk services with a confidence threshold, L3 broader scope. Break-even: 800 p = 20,000 (1 - p), so p = 0.9615. Expected value at 97% is 800 x 0.97 - 20,000 x 0.03 = 176 rupees per incident; at the break-even it is zero. The 95% Wilson interval for 388 of 400 is 94.8% to 98.3%, so the true accuracy may be below break-even, where the expected value is negative (-275 at the lower end).
6. Evaluation: replay on a larger, stratified set; if the true accuracy is 98%, about 1,000 incidents put the lower bound (96.9%) above break-even, while 400 do not (96.1%).
7. Rollout: L0 then L1 in shadow, measure agreement with humans; L2 for stateless services with a cap on actions per hour and an automatic stop after errors; widen by evidence.
8. Monitoring and risks: live accuracy with an interval against 96.15%, a kill switch, audit log of every action; limiting the cost of a wrong action (for example to 5,000) lowers the break-even to 86.2%.

**Metrics:**
- Accuracy = correct autonomous actions / autonomous actions taken (388 / 400 in the replay).
- Break-even accuracy = loss / (saving + loss) = 20,000 / 20,800.
- Net value per incident = 800 x accuracy - 20,000 x (1 - accuracy); guardrails: actions per hour, rollbacks, repeat incidents.

**Risks:**
- A replay is a sample and is not live behaviour; novel incidents are missing.
- Errors can be correlated (one bad action triggers many).
- Averaging hides a high-cost service class.
- Over-trust: humans stop checking.

**What the interviewer scores:**
- Strong: derives 96.15%, computes 176, and says the 97% sample does not clear it with confidence.
- Strong: levels, a kill switch and a cap on blast radius.
- Weak: "97% is above 96%, ship it"; no interval; no rollback.

**Example:** Illustrative numbers. 20,000 / 20,800 = 0.9615; 388 / 400 = 0.97; Wilson interval 0.948 to 0.983.
- Weak: "It is 97% accurate, which is better than the 96% we need, so let it run."
- Strong: "Break-even is 96.15 percent and we saw 97 percent on 400 replays, but the range is 94.8 to 98.3, so we cannot rule out losing money. I would run it with approvals first, restrict it to low-impact services, and move up only when the live lower bound clears break-even."

**Code:**
```python
import math
from statistics import NormalDist
save, loss, k, n = 800, 20_000, 388, 400
p_be = loss / (save + loss)
acc = k / n
print("break-even accuracy", round(p_be, 5), "sample accuracy", acc)
assert round(p_be, 5) == 0.96154 and acc == 0.97
ev = lambda p: save * p - loss * (1 - p)
print("EV per incident at 97%", ev(0.97), "at break-even", round(ev(p_be), 6))
assert round(ev(0.97), 2) == 176.0 and abs(ev(p_be)) < 1e-9
# Wilson 95% interval for 388/400
z = NormalDist().inv_cdf(0.975)
c = (acc + z * z / (2 * n)) / (1 + z * z / n)
h = z * math.sqrt(acc * (1 - acc) / n + z * z / (4 * n * n)) / (1 + z * z / n)
lo, hi = c - h, c + h
print("Wilson 95%", round(lo, 4), round(hi, 4), "EV at lower end", round(ev(lo), 1))
assert lo < p_be < hi and ev(lo) < 0
# exact binomial: chance of seeing >= 388 right if the true accuracy were exactly break-even
def sf(n, k, p):
    return sum(math.comb(n, i) * p**i * (1 - p)**(n - i) for i in range(k, n + 1))
pv = sf(n, k, p_be)
print("P(>=388 of 400 | p=break-even)", round(pv, 3))
assert 0.2 < pv < 0.4
# errors budget: at 97%, 12 wrong of 400; each costs 20,000
print("wrong in sample", n - k, "cost", (n - k) * loss, "savings", k * save, "net", k * save - (n - k) * loss)
assert (n - k) * loss == 240_000 and k * save == 310_400 and k * save - (n - k) * loss == 70_400
# accuracy needed if the loss were capped at 5,000 by a guardrail (e.g. blast-radius limit)
print("break-even if wrong costs 5,000:", round(5000 / (save + 5000), 4))
assert round(5000 / 5800, 4) == 0.8621
# sample size to put the lower bound above break-even if true accuracy is 0.98 (rough)
for m in (400, 1000, 2000):
    c = (0.98 + z * z / (2 * m)) / (1 + z * z / m)
    h = z * math.sqrt(0.98 * 0.02 / m + z * z / (4 * m * m)) / (1 + z * z / m)
    print("n", m, "lower bound at 98% observed", round(c - h, 4), "above break-even:", c - h > p_be)
```

**Output (my run):**
```text
break-even accuracy 0.96154 sample accuracy 0.97
EV per incident at 97% 175.99999999999943 at break-even 0.0
Wilson 95% 0.9483 0.9828 EV at lower end -275.3
P(>=388 of 400 | p=break-even) 0.232
wrong in sample 12 cost 240000 savings 310400 net 70400
break-even if wrong costs 5,000: 0.8621
n 400 lower bound at 98% observed 0.961 above break-even: False
n 1000 lower bound at 98% observed 0.9693 above break-even: True
n 2000 lower bound at 98% observed 0.9729 above break-even: True
```

**Follow-ups:**
- *What if wrong actions could be capped at 5,000?* Break-even falls to 86.2%.
- *Would more samples help?* Yes if accuracy is really 98%: about 1,000 incidents put the interval above break-even.

**Common mistakes:** Comparing 97% with 96% as if exact. Ignoring the interval. One accuracy for all services. No kill switch. Treating replay as live.

### Q39 ⭐ 🔴 Graph features for mule detection: A UPI-style network has 30,000,000 accounts with an average of 12 payment counterparties each, and scoring runs at 5,000 payments per second. Design the mule-account detection system, and compute the number of accounts within two hops of an account (one-hop plus two-hop neighbours, assume no overlap) and the lookups per second if every payment fetches the sender's two-hop neighbours, and say what you would precompute.
**Asked at:** Indian-market material (a Let's Data Science / NPCI item on AI for UPI fraud and multilingual voice, an Elastic and Sarvam multilingual voice-agent blog, a SquadStack voice-bot page on noise and accents, Razorpay, Delhivery and Shiprocket pages on cash-on-delivery return-to-origin risk scoring, a Blinkit candidate report of a delivery-time debugging case); vendor and blog material, no confirmed interview round for these exact designs; commonly reported in public guides for data scientist, ML engineer and GenAI engineer loops; search snippets only, not opened
**Say this first (1 line):** With 12 counterparties each, a sender has 12 one-hop and 144 two-hop neighbours (156 within two hops), so fetching them per payment is 780,000 lookups a second at 5,000 payments a second, which is why I would precompute neighbourhood features and fetch one vector per account.

**Clarifying questions:**
- Is the 12 an average, and do accounts overlap? The prompt says no overlap, so 156 within two hops (12 + 144); if you count only exactly-two-hop accounts it is 144 and 720,000 lookups a second.
- Are the 12 counterparties an average, and what are the maximum degrees (hubs)? Hubs make fan-out explode.
- What is the score latency budget and how fresh must graph features be? It decides batch versus streaming for graph features.
- How many confirmed mule accounts exist and how late are they labelled? It sets how supervised the model can be.
- What action follows a high score (hold, step-up check, review)? It sets the cost of a false positive. Ask compliance and legal about data use and reporting duties; I state no rule.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data and labels 7, baseline 4, graph features and model 10, evaluation 6, rollout 5, monitoring and risks 4):**
1. Clarify and frame: find accounts that receive and quickly forward money; the graph shape is the signal.
2. Metrics and guardrails: precision at a review budget, share of mule money caught before cash-out, false-hold rate on genuine users.
3. Data and labels: confirmed mule accounts are few and late; use investigation outcomes plus network seeds near known mules.
4. Baseline first: rules on account age, fan-in and fan-out in 24 hours, pass-through ratio.
5. Features and trade-offs: do not walk the graph at scoring time. Sizing: 12 + 12 x 12 = 156 per payment (no overlap, sender excluded), 5,000 x 156 = 780,000 profile lookups a second (720,000 for exactly two hops), plus 5,000 x 13 = 65,000 adjacency reads to find them. Precompute per account on a schedule: counts, pass-through, neighbour risk averages, or a graph embedding; then score with 1 vector per party, 10,000 reads a second, 78 times fewer. Cap fan-out for hubs (for example 50 per hop).
6. Evaluation: time-split offline, with graph features computed as of the payment date (no leakage from later links); measure lift over the rule baseline at a review budget.
7. Rollout: shadow scoring, then review-only, then step-up checks for a small share; review a sample of passes for missed cases.
8. Monitoring and risks: feature staleness, the share of accounts with a stale vector, drift when attackers change structure, a human review feedback loop.

**Metrics:**
- Precision at review budget = confirmed mules / accounts reviewed.
- Mule recall before cash-out = mule money stopped / mule money moved.
- Guardrails: false-hold rate = genuine users held / genuine users; lookups per second against the store limit.

**Risks:**
- Leakage: using links created after the payment.
- Guilt by association: a genuine user next to a mule is flagged; keep the action proportionate.
- Real neighbourhoods overlap, so 156 is an upper bound for average degrees, but hubs push the other way.
- Attackers adapt the structure.

**What the interviewer scores:**
- Strong: 144 and 156 named, 780,000 per second, and precompute plus bounded fan-out.
- Strong: time-correct features and a review-budget metric.
- Weak: a live graph walk per payment; no mention of hubs or leakage.

**Example:** Illustrative numbers. 12 x 12 = 144; 12 + 144 = 156; 5,000 x 156 = 780,000.
- Weak: "Run a graph neural network on the live graph for every payment."
- Strong: "Walking two hops live is 780,000 lookups a second. I would precompute neighbourhood aggregates or embeddings every few minutes and read one vector per party, which is 10,000 reads a second, and cap hub fan-out."

**Code:**
```python
accounts, deg, pps = 30_000_000, 12, 5000
one_hop = deg
two_hop_exact = deg * deg
within_two = one_hop + two_hop_exact
print("one-hop", one_hop, "exactly two-hop", two_hop_exact, "within two hops", within_two)
assert two_hop_exact == 144 and within_two == 156
lookups_within = pps * within_two
lookups_exact = pps * two_hop_exact
print("profile lookups/s (156 per payment)", lookups_within, "(144 per payment)", lookups_exact)
assert lookups_within == 780_000 and lookups_exact == 720_000
# adjacency-list reads to discover the two-hop set: 1 (sender) + 12 (each neighbour)
adj = pps * (1 + deg)
print("adjacency reads/s", adj)
assert adj == 65_000
# precomputed alternative: 1 vector read for the sender (and 1 for the receiver)
pre = pps * 2
print("precomputed reads/s", pre, "reduction vs 780,000:", lookups_within / pre)
assert pre == 10_000 and lookups_within / pre == 78.0
# edge storage: 30M * 12 outgoing edges, 8-byte ids (undirected counted both ways is the same count here)
edges = accounts * deg
print("edge entries", edges, "GB at 8 B each", edges * 8 / 1e9)
assert edges == 360_000_000 and edges * 8 == 2_880_000_000
# embedding table: 64 floats of 4 B per account
emb = accounts * 64 * 4
print("embedding table GB", emb / 1e9)
assert emb == 7_680_000_000
# overlap is real: with 12 neighbours of which some share neighbours, the true two-hop set is smaller
# but hub accounts (degree 100,000) explode the other way; cap fan-out
cap = 50
print("capped fan-out two hops", cap * cap, "per payment at 5,000/s:", pps * cap * cap)
assert pps * cap * cap == 12_500_000
```

**Output (my run):**
```text
one-hop 12 exactly two-hop 144 within two hops 156
profile lookups/s (156 per payment) 780000 (144 per payment) 720000
adjacency reads/s 65000
precomputed reads/s 10000 reduction vs 780,000: 78.0
edge entries 360000000 GB at 8 B each 2.88
embedding table GB 7.68
capped fan-out two hops 2500 per payment at 5,000/s: 12500000
```

**Follow-ups:**
- *How often to refresh the precomputed features?* As often as mule rings change money (minutes to hours); measure the benefit of fresher against cost.
- *What if a mule account is brand new?* No history: use account-age and onboarding signals, and a graph feature after its first links.

**Common mistakes:** Not saying which two-hop definition. Walking the graph live. Leakage from future edges. Ignoring hubs.

### Q40 ⭐ 🔴 Team planning: A team of 3 has 12 weeks, or 36 person-weeks, for 5 candidate ML projects costing 20, 14, 10, 8 and 6 person-weeks with projected annual benefits of 40, 30, 16, 14 and 12 lakh rupees (illustrative projections). Design the roadmap, deciding which projects to take and what to cut. Compute the best affordable subset by total benefit, and say which risks would change the choice.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to team capacity planning and project prioritisation (adjacent to general build-versus-buy guidance); search snippets only, not opened
**Say this first (1 line):** The best subset that fits 36 person-weeks is projects A and B (34 weeks, 70 lakh projected), but it leaves only 2 weeks of slack, so I would present it with a buffered alternative and say which risks would flip the choice.

**Clarifying questions:**
- Are the benefits projections or measured, and by whom? They are illustrative projections, so each carries a range.
- Are person-weeks interchangeable between people (skills, data access)? A project that needs one skill cannot absorb spare weeks from another.
- What else takes time (on-call, maintenance of live models, reviews)? Planning at 100% is a common failure.
- Are there dependencies between projects (shared data pipeline)? A cheap project may unlock a big one.
- When do benefits start and what is the cost of delay? Annual benefit in year one may be much lower.

**Approach (spoken framework, about 45 minutes: clarify 5, metrics 4, data 4, baseline 4, selection model 10, evaluation of risks 7, plan and launch 6, monitoring and cost 5):**
1. Clarify and frame: a portfolio choice under a capacity limit, a knapsack problem.
2. Metrics and guardrails: projected benefit, benefit per person-week, probability of delivery, and a buffer for existing models.
3. Data: ask owners for the evidence behind each benefit number and the data readiness.
4. Baseline first: rank by benefit per person-week (B 2.14, A 2.0, E 2.0, D 1.75, C 1.6).
5. Selection: capacity 3 x 12 = 36; all five cost 58. Test every subset: A + B = 34 weeks, 70 (best); A + C + E = 36 weeks, 68; A + D + E = 34, 66; B + C + D = 32, 60. At 80% planned capacity (28.8) the best is B + D + E, 28 weeks, 56 lakh. Also note that A (20 weeks) and B (14 weeks) each need at least two people in a 12-week calendar.
6. Evaluation of risk: if A delivers only half its benefit (20 instead of 40), the best subset becomes B + C + D (32 weeks, 60); if the data for A is not ready, the best set without A is B + C + D (32 weeks, 60).
7. Plan: stage gates at week 4 and week 8 (a data check and a baseline result) and a pre-agreed rule for dropping a project.
8. Monitoring and cost: weekly burn against the plan, measured benefit after launch to correct future estimates; the cut list is written down in advance.

**Metrics:**
- Total projected benefit of the chosen set = sum of benefits (70 lakh per year for A + B), a projection.
- Capacity used = person-weeks planned / 36 (94% for A + B).
- Benefit per person-week = benefit / cost; guardrail: planned buffer for maintenance (for example 20%).

**Risks:**
- Benefit projections are optimistic and uncorrelated with effort.
- Zero slack: any slip drops a project.
- Dependencies and skills: weeks are not interchangeable.
- Large projects carry more delivery risk than the point estimate shows.

**What the interviewer scores:**
- Strong: checks all subsets, gets A + B at 70, and then argues against planning at 100%.
- Strong: names which risk changes the choice (A halves, data not ready).
- Weak: picks by benefit alone or by gut, with no capacity arithmetic or buffer.

**Example:** Illustrative numbers. 3 x 12 = 36 weeks; A + B = 20 + 14 = 34 weeks, 40 + 30 = 70 lakh; A + C + E = 36 weeks, 68 lakh.
- Weak: "Take the two biggest ones, they have the most benefit."
- Strong: "A plus B uses 34 of 36 weeks for 70 lakh projected, the best fit. But that is 94% of capacity, so I would propose B, D, E at 28 weeks and 56 lakh as the safer plan, and start A only if the week-4 data check passes."

**Code:**
```python
from itertools import combinations
cost = {"A": 20, "B": 14, "C": 10, "D": 8, "E": 6}
ben = {"A": 40, "B": 30, "C": 16, "D": 14, "E": 12}
cap = 3 * 12
assert cap == 36 and sum(cost.values()) == 58 and sum(ben.values()) == 112
def best(capacity):
    res = []
    for r in range(1, 6):
        for s in combinations(cost, r):
            c = sum(cost[x] for x in s)
            if c <= capacity:
                res.append((sum(ben[x] for x in s), c, "".join(s)))
    return sorted(res, reverse=True)
top = best(cap)[:4]
print("capacity 36 top subsets (benefit, weeks, projects):", top)
assert top[0] == (70, 34, "AB") and top[1] == (68, 36, "ACE")
# buffer: plan to 80% of capacity (28.8 person-weeks)
buf = cap * 0.8
t2 = best(buf)[:3]
print("planned to", buf, "->", t2)
assert t2[0] == (56, 28, "BDE")
# benefit per person-week
for k in cost: print(k, round(ben[k] / cost[k], 2))
assert round(40 / 20, 2) == 2.0 and round(30 / 14, 2) == 2.14
# risk sensitivity: if A's benefit is really 40 * 0.5 (half the projection)
ben2 = dict(ben); ben2["A"] = 20
res = sorted(((sum(ben2[x] for x in s), sum(cost[x] for x in s), "".join(s))
              for r in range(1, 6) for s in combinations(cost, r) if sum(cost[x] for x in s) <= cap), reverse=True)[0]
print("if A delivers half:", res)
assert res == (60, 32, "BCD")
# feasibility: nobody can do more than 12 person-weeks on a calendar of 12 weeks
print("A needs at least", -(-20 // 12), "people; B needs at least", -(-14 // 12))
assert -(-20 // 12) == 2 and -(-14 // 12) == 2
```

**Output (my run):**
```text
capacity 36 top subsets (benefit, weeks, projects): [(70, 34, 'AB'), (68, 36, 'ACE'), (66, 34, 'ADE'), (60, 32, 'BCD')]
planned to 28.8 -> [(56, 28, 'BDE'), (54, 28, 'AD'), (52, 26, 'AE')]
A 2.0
B 2.14
C 1.6
D 1.75
E 2.0
if A delivers half: (60, 32, 'BCD')
A needs at least 2 people; B needs at least 2
```

**Follow-ups:**
- *What would make you drop A?* Data not ready by week 4, or evidence the benefit is under about half of its projection.
- *How do you handle a new urgent request?* Use the buffer; if it is larger, drop the lowest benefit-per-week project and tell stakeholders.

**Common mistakes:** Ranking only by benefit. Planning at 100% capacity. Treating projections as certain. Forgetting that a 20-week project cannot be done by one person in 12 weeks.

