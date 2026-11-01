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
