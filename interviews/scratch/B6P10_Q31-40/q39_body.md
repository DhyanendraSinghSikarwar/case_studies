**Say this first (1 line):** With 12 counterparties each, a sender has 12 one-hop and 144 two-hop neighbours (156 within two hops), so fetching them per payment is 780,000 lookups a second at 5,000 payments a second, which is why I would precompute neighbourhood features and fetch one vector per account.

**Clarifying questions:**
- Does "two-hop neighbourhood" mean exactly two hops (144) or within two hops (156)? I state the 156 and show 144 as the other reading.
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

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *How often to refresh the precomputed features?* As often as mule rings change money (minutes to hours); measure the benefit of fresher against cost.
- *What if a mule account is brand new?* No history: use account-age and onboarding signals, and a graph feature after its first links.

**Common mistakes:** Not saying which two-hop definition. Walking the graph live. Leakage from future edges. Ignoring hubs.
