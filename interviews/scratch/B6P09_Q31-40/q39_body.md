**Say this first (1 line):** If the 4% drop is uniform, video drives about 4,000,000 of the 100,000,000 sales (4%), four times the 1,000,000 that last-click credits; this is a projection from 10 regions, so I would report a range and the assumptions, not a point.

**Clarifying questions:**
- Is the 100,000,000 the with-video level in all 50 regions? The prompt fixes the 4% against the kept regions' 2,000,000 each; as a share of the no-video level the same gap is 4.17%.
- How were the 10 regions chosen, and were pre-period sales compared? Random choice helps, but 10 of 50 can still be unbalanced.
- How long was the pause, and how long do video effects last? A short test misses lagged effects.
- Do regions leak (people travel, national media, shared online audiences)? Leakage shrinks the measured gap.
- What did video cost in the period? Incremental sales alone do not say whether it paid.

**Approach:**
1. The arithmetic. Each region sells 100,000,000 / 50 = 2,000,000. A 4% drop is 80,000 per paused region, 800,000 for the 10 regions, and scaled to 50 regions 4,000,000. The observed total in the test was 99,200,000.
2. Compare with last click: 4,000,000 / 1,000,000 = 4.0 times; video is 4% of sales on this projection versus 1% credited.
3. Put a range on it with an invented noise level (relative sales noise per region after matching): with 2% noise the 95% interval for the effect is 2.6% to 5.4% (2.6M to 5.4M), at 3% it is 1.9% to 6.1%, and at 6% it is -0.2% to 8.2%, which includes zero. So the point estimate is far less informative than it looks when regions are noisy.
4. Improve the estimate: compare each region with its own pre-period (difference-in-differences) or use matched regions or synthetic controls. In my simulation of 4,000 random assignments with a true 4%, comparing levels gave a standard deviation of 16.8 points (regions differ in size), while comparing with each region's pre-period gave 1.1 points and only 0.45% of assignments came out below 1%.
5. Assumptions to state: uniform effect across regions; no spillover; stable effect over time; the 40 control regions kept normal spend; no other channel changed; the effect measured at the current spend level.
6. What a 10-region test can tell you: the average incremental effect of switching video off at the current spend, with a range. What it cannot: the shape of diminishing returns (it is an on/off test), effects by region type, long-run brand effects, interaction with other channels, or the return per unit of spend.
7. Use it: calibrate the attribution model or the marketing-mix model with the test result (a lift test as a prior); rerun with more regions, more spend levels (a dose test) or a longer window.
8. Report: incremental sales, range, cost, and incremental return, and say that last click and lift measure different things (see Book 6 Part 5, Q11 on reported versus incremental return on ad spend).

**Metrics:**
- Lift = 1 - (sales in paused regions / counterfactual sales) = 4% (paused regions sell 96% of the kept level).
- Incremental sales = lift x total sales with video = 0.04 x 100,000,000 = 4,000,000.
- Ratio to last click = incremental / credited = 4.0.
- Incremental return = incremental sales (or margin) / video spend (spend not given in the prompt).
- Guardrails: pre-period balance between arms, spillover check using neighbouring regions, test duration.

**Risks:**
- Noise: 10 regions is a small test; a 3% regional noise gives a 4% effect with a 1.9% to 6.1% range, and 6% noise makes it inconclusive.
- Random assignment can still leave unbalanced regions; use pre-period matching.
- Spillover and national media bias the gap towards zero.
- The effect at one spend level does not extend to doubling or halving spend.
- Last click and lift may both be right about different things (assist versus incremental).

**What the interviewer scores:**
- Strong: 4,000,000 versus 1,000,000, with the base stated and a range.
- Strong: pre-period adjustment and the fact that 10 regions cannot give a response curve.
- Strong: lists assumptions (uniform, no spillover, short horizon).
- Weak: "video is worth 4x last click" as fact; no uncertainty; ignores cost.

**Example:** Illustrative numbers from the run. 800,000 lost in 10 regions scales to 4,000,000; at region-level noise of 3% the 95% range is 1.9M to 6.1M.
- Weak: "Last click says 1 million, the test says 4 million, so last click is wrong."
- Strong: "If the 4% is uniform, video is about 4 million of sales, four times last click. With 10 regions the range could be roughly 2 to 6 million, so I would compare against the regions' own history, check for spillover, and weigh it against video spend. It tells me about on versus off at this spend, not the return of one more unit."

<<CODE>>

<<OUTPUT>>

**Follow-ups:**
- *Why might last click undercount video?* It credits the final touch, and video often creates demand that later converts through search or direct.
- *Could the true effect be bigger than the test?* Yes if spillover leaks sales into the kept regions; no if the paused regions got other media.
- *What next?* A larger, longer test with matched pairs, or varying spend levels to get a response curve.

**Common mistakes:**
- Treating the 4% as exact.
- Comparing regional levels without the pre-period.
- Using one on/off test to set the budget.
- Ignoring cost.
