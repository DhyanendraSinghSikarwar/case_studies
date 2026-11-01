**Say this first (1 line):** If the recommender learns only from clicks on items it already showed, popular items get more exposure and more clicks, the tail starves, diversity shrinks and CTR drifts down, while an offline NDCG measured on those same logs still looks better; I would prove it with exposure data and a small random slice, then add exploration.

**Clarifying questions:**
- Is "6%" relative (5.0% to 4.7%) or six points? It sets how big the problem is, and I will assume relative.
- Is CTR per impression or per user, and did the traffic mix (new versus returning users, platform) change over the eight weeks? A mix shift can fake a slide.
- How was the offline NDCG computed? If it used clicks logged under the old ranker, it can only credit items that ranker already showed, so it is exposure-biased.
- How is "diversity" measured: share of catalogue shown, entropy of impressions, top-10 item share? I need one number to track.
- Is any traffic randomised today? Random exposure is the only unbiased evidence of how tail items really perform.
- Do users see the same items repeatedly? That adds fatigue, a second cause of a slide.

**Approach:**
1. Confirm the slide is real: CTR per impression by week, split by position, platform and user cohort, with seasonality and UI changes ruled out.
2. Measure concentration over time: distinct items shown per day, share of impressions going to the top 1% of items, normalised entropy of impression shares. Compare week 0 with week 8.
3. Test the loop directly: for items with similar quality signals (price, rating, age), compare CTR per exposure for items that got high early exposure versus low. Use position-normalised CTR so slot effects do not distort it.
4. Run a small randomised slice (illustrative 1 to 2% of requests, one slot filled by random eligible items). Compare CTR of randomised-slot items by popularity bucket. If tail items do as well per exposure as head items, the ranker is under-exposing them.
5. Check fatigue: CTR by number of prior exposures of the same item to the same user.
6. Change the system: reserve exploration slots or use Thompson-style sampling for uncertain items; train with inverse-propensity weights from logged exposure probabilities; add a diversity or coverage constraint in re-ranking; give new items a freshness boost.
7. Evaluate offline with a counterfactual estimator on randomised data, not raw logged NDCG; then run a long A/B with a permanent small holdout.

**Metrics:**
- CTR = clicks / impressions, also reported per position so slot mix does not change it.
- Coverage = distinct items shown in a day / eligible items that day.
- Top-1% share = impressions on the 1% most-shown items / all impressions.
- Normalised entropy = -sum(s_i ln s_i) / ln(N), where s_i is item i's impression share and N the number of items.
- Randomised-slot CTR by popularity bucket (head, torso, tail).
- Guardrails: orders or revenue per session, session length, latency, and the CTR cost of the exploration slice.

**Risks:**
- Exposure-biased offline evaluation: NDCG up 3% on logged data does not show a better ranker for items it never showed.
- Seasonality or catalogue changes can explain CTR without any loop.
- Exploration lowers CTR in the short run, so it needs a budget and a time horizon.
- Diversity can be gamed with irrelevant items; pair it with a relevance floor.
- A multi-week slide has more than one cause (fatigue, novelty fade, competition); do not credit it all to the loop.

**What the interviewer scores:**
- Strong: explains the loop (exposure drives clicks, clicks drive ranking) and why offline logged NDCG cannot see it. Weak: says "retrain more often".
- Strong: asks for randomised exposure data or a holdout as unbiased evidence. Weak: argues from the dashboard only.
- Strong: gives concrete concentration metrics and the fix list (exploration, IPS, diversity). Weak: "add diversity" with no measurement.
- Strong: states the cost of exploration and how to cap it.

**Example:** (illustrative) CTR goes from 5.00% to 4.70%, which is -6.0% relative. Offline NDCG goes from 0.500 to 0.515, +3.0% relative. Both are in the code. Then a toy world of 300 items, 5 slots, with a legacy popularity head start unrelated to true appeal, and an assumption that an item's appeal saturates as it is shown to the same audience. Ranking by raw clicks shows only 5 distinct items and the slate CTR falls 14.1% over the run. A ranker that keeps one slot random shows all 300 items, top-5 impression share 0.60 instead of 1.00, and its slate CTR roughly doubles because it finds better items. These are toy numbers; the saturation assumption is mine and produces the slide. Weak: "NDCG improved, so the model is better; CTR will recover." Strong: "NDCG was measured on what the old model chose to show. Show me concentration over time and a randomised slice before I touch the model."

**Code:**
