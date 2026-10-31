**Say this first (1 line):** Head queries are most of the volume, so a small head gain can cancel a large tail loss in the overall number; I would report NDCG by query frequency bucket with confidence intervals, alert on the tail slice itself, and fix the tail with better candidate generation, query understanding and tail-focused training data.

**Clarifying questions:**
- Is "20%" the share of queries or of traffic? Long-tail queries are rare, so the two shares differ and the weights in the overall number depend on it.
- How is "long tail" defined (frequency in the last 30 days, a head/torso/tail cut, or a rare-term flag)? The cut decides which queries land in the slice.
- Is NDCG computed from human judgements or from clicks? Clicks on rare queries are sparse and noisy.
- What changed in the ranker: new training data, a popularity feature, a new embedding model? Tail queries often depend on semantic matching.
- What does a failed tail query cost: zero-result pages, abandonment, support contacts?

**Approach:**
1. Slice the evaluation: bucket queries by frequency (head, torso, tail), by intent, by length, by language or script, and by whether the query has results at all. Report NDCG and volume per bucket.
2. Do the weighting arithmetic: overall change = sum of (share x change). A tail drop of 8% with 20% share is a 1.6% drag on the overall, and can be hidden by a head gain.
3. Add uncertainty: with fewer tail queries per week, bootstrap confidence intervals per slice; alert on a slice only when the interval excludes zero change.
4. Diagnose: compare candidate recall (is the right item even retrieved?) versus ranking order (is it retrieved but ranked low?). Tail failures are often retrieval or vocabulary mismatch.
5. Remedies: hybrid lexical plus semantic retrieval, query rewriting and spell correction, data augmentation or synthetic queries for tail, a tail-weighted loss, a separate tail model or fallback, and click-data smoothing so popularity features do not bury rare items.
6. Operationalise: a sliced-metrics dashboard with a minimum-sample rule, a release gate that blocks a launch if a protected slice regresses beyond a set margin, and a golden set of tail queries kept fresh.

**Metrics:**
- NDCG@10 by bucket = mean over queries in the bucket of DCG@10 / ideal DCG@10.
- Volume share by bucket = queries in bucket / all queries (state if by queries or traffic).
- Zero-result rate = queries returning no result / queries; abandonment rate on tail queries.
- Guardrails: head NDCG must not fall, latency, index recall at k.

**Risks:**
- Per-query NDCG is noisy and tail slices are small; a small slice can look worse by chance.
- Changing the bucket definition after seeing the result is slice shopping.
- Click-based labels favour head queries, so the tail looks worse than it is, or better.
- A tail-specific fix can slow queries or hurt the head.

**What the interviewer scores:**
- Strong: shows the weighted-average arithmetic and why the overall metric stays flat. Weak: "the model got worse for some queries".
- Strong: uses intervals and a minimum sample per slice. Weak: reads point estimates.
- Strong: separates retrieval from ranking failure. Weak: "add more data".
- Strong: proposes a release gate on slices. Weak: only a dashboard.

**Example:** (illustrative) Head NDCG is 0.70 on 80% of queries and tail NDCG is 0.50 on 20%. A tail fall of 8% takes it to 0.46, which moves the overall by 0.2 x (-0.04) = -0.008. The head needs to rise from 0.70 to 0.71 to hide it, a gain of only 1.4%. In a seeded simulation with 10,000 queries a week and per-query NDCG sd of 0.3: overall changes -0.0050 with a 95% bootstrap interval of [-0.0121, +0.0024] (flat); head +0.0041 [-0.0038, +0.0121]; tail -0.0412 [-0.0583, -0.0248] (clearly down). Only the tail slice shows the problem. Weak: "Overall NDCG is stable, so no action." Strong: "Show me NDCG by frequency bucket with intervals; the tail can fall while the head hides it."

**Code:**
