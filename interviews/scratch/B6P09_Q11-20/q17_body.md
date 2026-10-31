**Say this first (1 line):** I would pick cutoff B: total profit is 41.5 million against 34.4 million for A and 40.6 million for C, because the extra applicants from A to B have a 7.5% bad rate (below the 14.3% break-even) and the extra from B to C have 15.2% (above it), and first I would check that those bad rates are calibrated on a recent, out-of-time sample.

**Clarifying questions:**
- Are the bad rates projections from a model, and how were they validated (out-of-time, reject-inference-free)? Everything below depends on them.
- Is the profit of 1,000 per good customer and the loss of 6,000 per bad customer net of funding cost, servicing and recoveries, and over what horizon? The break-even rate depends on this ratio.
- Is there a capital or exposure limit that caps the approvals? It might rule out C regardless of profit.
- Will the bad rate of the marginal band hold when the economy changes? The marginal customers are the most sensitive.
- Does the choice need fair-lending or model-risk review before changing the cutoff? That is a question for compliance and the model-risk team.

**Approach:**
1. Set up the economics. Break-even bad rate = 1,000 / (1,000 + 6,000) = 14.3%: a customer is worth taking if the chance of bad is below that.
2. Compute profit at each cutoff. Profit = (approved - bad) x 1,000 - bad x 6,000. A: 800 bad, profit 34,400,000. B: 1,925 bad, profit 41,525,000. C: 4,200 bad, profit 40,600,000 (illustrative currency units, undiscounted).
3. Use marginal bands, not averages. A to B adds 15,000 applicants and 1,125 bad, a marginal bad rate of 7.5%, profit +7,125,000. B to C adds 15,000 and 2,275 bad, 15.2%, profit -925,000. The overall bad rates of 3.5% and 6% hide that the C band is worse than break-even.
4. Test the sensitivity. If every bad rate is 20% higher, B is still best (38.8 million). At 50% higher B is still best. At double, A wins (28.8 million against 28.05 million). So B is robust to moderate error but not to a doubling.
5. Check first: that the projected rates hold on recent data. Backtest the score on the latest matured cohort, look at calibration in the 40,000 to 55,000 band in particular, and check drift since training. The B to C margin (15.2% versus 14.3%) is thin, so small error flips it.
6. Decide and monitor. Choose B, with a staged ramp (approve in tranches, watch early-arrears), and a trigger to tighten if the band's bad rate passes a pre-agreed level, say 10% (agree it with risk).

**Metrics:**
- Bad rate = accounts bad within the horizon / accounts approved, matured only.
- Marginal bad rate of a band = extra bad / extra approved.
- Profit = good x 1,000 - bad x 6,000, with a stated horizon and discounting.
- Guardrails: early-arrears rate of the new band, concentration of exposure, calibration error by band.

**Risks:**
- Projected bad rates carry model error; the marginal band is the least reliable.
- One profit figure per applicant ignores heterogeneity (limits, price, product).
- Selection: customers near the cutoff may behave differently than the model assumes (see reject inference).
- Profit-maximising cutoffs may conflict with fairness and capital constraints; neither is in the numbers.

**What the interviewer scores:**
- Strong: computes 34.4, 41.5 and 40.6 million and the 14.3% break-even.
- Strong: uses marginal bands (7.5% and 15.2%), explaining why averages mislead.
- Strong: runs a sensitivity and names validation of the projected bad rates as the first check.
- Weak: picks the lowest bad rate (A) or the largest volume (C), or compares average rates to break-even.

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "A has the lowest bad rate, so choose A. Or C because it approves the most."
- Strong: "I compute profit at each: 34.4, 41.5 and 40.6 million. Break-even is 14.3% bad. The 15,000 extra people from A to B have a 7.5% bad rate and add 7.1 million; the next 15,000 have 15.2% and lose 0.9 million. So B. Before committing I would backtest the score's calibration in that band on a recent cohort, because B beats A even at a 50% worse bad rate but loses to A at double."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if the extra band's bad rate is uncertain by +/- 3 points? B to C at 15.2% could be 12% to 18%, so C is a coin flip; stay at B and gather data.
- How would you add capital cost? Subtract a per-account cost from the good-customer profit, which lowers the break-even bad rate.
- Could you price instead of rejecting? Yes, higher rates on the riskier band can lift profit, subject to the pricing and fair-lending rules, which are for the compliance team to specify.

**Common mistakes:**
- Comparing average bad rates to the break-even instead of the marginal rate.
- Ignoring that the rates are projections.
- Forgetting the cost of 6,000 versus the profit of 1,000 asymmetry (a bad customer costs 6 good ones).
- Not checking constraints beyond profit.
