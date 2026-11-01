**Say this first (1 line):** Item-level revenue rises 4,000,000 a day (+8%), but the substitutes lose 6,000,000, so the whole category falls 2,000,000 a day (-1.2%); the price cut mostly moves demand from neighbours to the discounted items, so I would test at the category level.

**Clarifying questions:**
- Are these numbers from a randomised pilot or a before/after comparison? Without randomisation the 20% and 5% could include trends and seasonality.
- Is the objective revenue, units or margin? The answer flips with unit cost (see the margin view below).
- Which items count as substitutes, and how was that list built? A wrong list hides or invents cannibalisation.
- Is there a time effect (promotion novelty, pull-forward of purchases)? A short pilot overstates a lasting lift.
- Is any inventory or fee affected by the price cut? Costs outside revenue change the decision.

**Approach:**
1. Item level. Revenue before = 100,000 x 500 = 50,000,000; after = 120,000 x 450 = 54,000,000; change +4,000,000 (+8.0%). Decomposition: -5,000,000 from the price cut on old units (100,000 x -50), +9,000,000 from the extra 20,000 units at 450.
2. Substitutes: 240,000 x 500 = 120,000,000 before, 228,000 x 500 = 114,000,000 after, change -6,000,000 (-5.0%).
3. Whole category: before 170,000,000, after 168,000,000: -2,000,000 per day (-1.18%). Units rose by 8,000 (20,000 extra on the test items minus 12,000 lost on substitutes), so units grew while revenue fell.
4. Cannibalisation share: 12,000 of the 20,000 extra units, 60%, came from substitutes. Elasticities: own -2.0, cross +0.5 (a 10% cut moved the substitutes 5% the other way).
5. Break-even: the category is revenue-neutral only if substitutes lose 8,000 units or fewer (3.3% of their units, instead of 5%).
6. Margin view (invented unit cost of 300): margin falls from 68,000,000 to 63,600,000, a loss of 4,400,000 per day, worse than the revenue figure.
7. Design to capture cannibalisation: randomise at the level where substitutes live (category, brand-by-region, or cluster of similar items), not the item. Measure outcome at the cluster level. In my toy model item-level randomisation (half the items cut) shows a +23.5% treated-versus-control lift, while cutting every item gives +3.2%, because the control items lose 9.1% of their own baseline.
8. Other designs: geo or time-based switchback tests; holdout clusters; track category total and a long window for pull-forward.

**Metrics:**
- Item-level revenue change = (units after x price after) - (units before x price before) for test items.
- Category revenue (and margin) change = test items + substitutes (+ any other affected items).
- Cannibalisation rate = units lost on substitutes / extra units on test items (60%).
- Guardrails: margin per day, conversion, returns, stock-outs, long-window repeat purchase.

**Risks:**
- Item-level randomisation shares customers between arms, so the estimate is biased (interference).
- A pilot's relative moves may not hold at scale; competitors may respond.
- Revenue can rise while margin falls.
- Substitute lists are subjective; some losses may be in non-listed items.

**What the interviewer scores:**
- Strong: computes +4M, -6M, -2M correctly and states units versus revenue.
- Strong: gives the cannibalisation share and asks about margin.
- Strong: randomises at cluster or category level and measures category totals.
- Weak: reports only the +8% item lift; ignores interference in the test design.

**Example:** Illustrative numbers from the run. Item level +4,000,000, substitutes -6,000,000, category -2,000,000 per day; 60% of the extra units are taken from neighbours.
- Weak: "The test lifted units 20% and revenue 8%, so we roll out."
- Strong: "Test items gain 4 million a day, but substitutes lose 6 million, so the category loses 2 million. Of the extra 20,000 units, 12,000 came from neighbours. I would re-run at the category level with a holdout and look at margin, not just revenue."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *What if the substitute drop is only 3%?* Substitutes lose 3,600,000 and the category is +400,000; the break-even is 3.3%, so the decision is close and needs a proper interval.
- *Is a switchback test enough?* It handles shared customers over time but needs washout between periods because of pull-forward.
- See also Book 6 Part 1, Q40 (a new tab grows while the parent tab loses orders) for the same cannibalisation logic in orders.

**Common mistakes:**
- Reading item lift as category lift.
- Randomising at item level when items substitute.
- Using revenue when the goal is margin.
- Treating the pilot as a forecast.
