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

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *What if the catalogue doubles?* Index 20.48 GB, 5 nodes per replica (4.27 rounded up), 15 nodes. Check it with the same code.
- *Why not rank all 20 million items?* The ranker is too slow per item; retrieval narrows to hundreds first.
- *How do you handle new items?* Content-based item tower, a small fresh-items index, and an exploration slot.

**Common mistakes:** Forgetting to round up nodes and replicas. Mixing 1e9 and 2^30. Sizing for the average. Judging retrieval by click-through instead of recall at K.
