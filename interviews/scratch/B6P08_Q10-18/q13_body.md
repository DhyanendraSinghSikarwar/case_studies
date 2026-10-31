**Say this first (1 line):** The model learns from clicks it caused by showing those items, so popular items get more exposure, more clicks and a higher score next week; I prove it with a small random-exposure slice and fix it with exploration, propensity logging and exposure-aware training.

**Clarifying questions:**
- Is the 52% a share of impressions (as stated, 17 absolute points up from 35%) and of all slots or only the first screen? Position matters because top slots get most attention.
- Did the catalogue change (a new hit release, a seasonal event)? A real hit also raises the top share without any loop.
- Are impressions and positions logged for each click? Without them we cannot separate exposure from appeal.
- Is any traffic shown randomly or with a different ranker today? That slice is the cleanest evidence.
- What is the business goal (clicks now, long-term retention, creator fairness)? A flat page CTR with a narrower catalogue can still hurt long-term.

**Approach:**
1. Explain the loop in two sentences: items shown more get more clicks, and a model trained on clicks scores them higher, so they are shown more. Clicks measure exposure times appeal, but the model reads them as appeal.
2. Prove it with the data you have:
   - Plot top-1% impression share by week against the retrain dates; the rise should follow retrains, not the catalogue.
   - Compare click-through for the same items at the same position, early versus late weeks. If exposure rose and CTR at fixed position did not, the model is not finding better items.
   - Look at items whose exposure rose most: were they already ahead six weeks ago (rich get richer)? Use a rank correlation between last month's clicks and this week's exposure.
   - If any random or exploration traffic exists, compute CTR there. In my simulation the top items had 11,939 impressions each against 81 for the others, yet their CTR in a random slice was 6.0%, the same as the catalogue's 6.05%: exposure rose without appeal rising.
3. Logging fix: log position, the candidate set, the model score and the probability the item was shown (propensity). Keep a 1 to 2% randomised exploration slice as a permanent measuring stick.
4. Training fix: weight clicks by inverse propensity (clipped), or add a position feature trained away at serving; add exploration (epsilon or a bandit); hold out the exploration slice for evaluation. Monitor exposure and quality, not only clicks.
5. Rollback and escalation: if the top-1% share exceeds a ceiling agreed with product (for example 55%) or tail-item coverage drops below a floor, hold the retrain and serve the previous model plus exploration; escalate to the product owner because it trades short-term clicks for long-term health.
6. First 15 minutes does not apply (no outage); first week: logging and the exploration slice. Next quarter: counterfactual evaluation, exposure caps, a creator and catalogue-health dashboard.
7. Blameless angle: the system optimised the metric we gave it; the gap is in what we measured. Action item: add an exposure metric to the retrain gate.

**Metrics:**
- Top-1% exposure share = impressions on the top 1% of items by impressions / all impressions (35% to 52% is 17 absolute points, about 1.49x).
- Catalogue coverage = items with at least N impressions / catalogue size; Gini or entropy of exposure.
- Exploration-slice CTR by item group (unbiased because exposure is random).
- Page CTR (flat) as a guardrail, plus a long-term metric such as 30-day return rate.

**Risks:**
- Top share also rises from genuine quality or a real hit; the exploration slice is what separates them.
- Exploration costs short-term clicks; size it (1 to 2%) and tell the business.
- Inverse-propensity weights have high variance when propensities are tiny; clip them.
- Flat page CTR can hide harm to new creators and cold-start items.

**What the interviewer scores:**
- Strong: states the loop, then proves it with data (fixed position, exploration slice), not only a story.
- Strong: fixes logging first (propensity, position), then training, and picks an exposure metric.
- Strong: considers alternative explanations.
- Weak: "just add diversity" with no measurement; or "the model is fine because CTR is flat".

**Example:** Illustrative simulation: 1,000 items with nearly equal appeal, weekly retrains on last week's clicks. Top-1% share goes from 27% to 53% over six weeks while page CTR stays about 6.0% to 6.2%. Weak versus strong:
- Weak: "CTR is flat, so nothing is wrong."
- Strong: "CTR is flat because appeal did not change; only who gets shown did. In a random slice the top items click at 6.0%, the same as everything else. I would log propensities, keep a 2% random slice, weight training by inverse propensity, and track top-1% share and coverage next to CTR."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Why not just boost the tail? Boosting without measurement may show worse items; use exploration to learn their real appeal first.
- What if you cannot randomise at all? Use position-debiasing with logged propensities, or natural experiments such as ranker changes; weaker evidence.
- Is the simulation proof? It shows the mechanism is possible; your real proof is the data comparison in step 2.

**Common mistakes:**
- Reading clicks as pure appeal.
- No logging of what was shown, only what was clicked.
- Adding diversity with no metric.
- Treating a flat CTR as success.
