**Follow-ups:**
- How big should the random slice be? Size it for the smallest tail-versus-head CTR gap you care about, using the two-proportion sample-size formula on impressions; typically 1 to 2% of traffic is enough because impressions are plentiful.
- Can you fix it without exploration? Partly: IPS-weighted training and diversity constraints help, but they cannot learn about items with zero exposure, so some exploration is still needed.
- How does this relate to Book 6 Part 1, Q39 ("A recommendation model refresh raised click-through rate by 5%, but catalogue diversity fell ...")? That question is about weighing a short-term CTR lift against long-term harm and setting up a holdout for the decision; this one is about why a deployed ranker slides over weeks and how to prove the loop. The long-term holdout idea carries over.

**Common mistakes:**
- Taking logged-click NDCG as proof of a better ranker.
- Blaming seasonality without checking exposure concentration.
- Adding a diversity re-ranker without measuring whether it helps CTR or revenue.
- Running exploration without a budget, or forgetting to log exposure propensities so they cannot be used later.
- Treating the 6% as points when it is relative, or the reverse.
