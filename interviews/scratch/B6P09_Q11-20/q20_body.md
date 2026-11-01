**Say this first (1 line):** The net value per impression is +0.05, +0.01, -0.02 and -0.04, so the best weekly cap is 2 (cumulative net 0.06 per user), but the second impression clears break-even by only 0.05 points, so I would confirm the numbers with a randomised frequency test before setting the cap.

**Clarifying questions:**
- How were the incremental probabilities measured: randomised holdout, ghost ads, or observational attribution? Only the first two are causal.
- Is a conversion worth a flat 20, or does value vary by customer? Variable value changes the break-even per user.
- Is the 0.05 cost an average? Costs may differ by placement or auction, and later impressions may be cheaper.
- Are the probabilities conditional on a user reaching that impression? Users who reach the 4th are a selected group.
- Within what window is the conversion counted (the same week, 7 or 30 days)? A longer window changes later impressions' value.

**Approach:**
1. Compute net value per impression = incremental probability x 20 - 0.05. First: 0.005 x 20 = 0.10, minus 0.05 = +0.05. Second: 0.003 x 20 = 0.06, so +0.01. Third: 0.0015 x 20 = 0.03, so -0.02. Fourth: 0.0005 x 20 = 0.01, so -0.04.
2. Choose the cap by the cumulative sum, which is 0.05, 0.06, 0.04, 0.00 per user for caps 1 to 4. The maximum is at cap 2. Equivalent rule: keep adding impressions while incremental probability exceeds cost / value = 0.05 / 20 = 0.25%. The first two impressions (0.50% and 0.30%) pass; the third (0.15%) does not.
3. Note how thin the margin is. The second impression is at 0.30% against a 0.25% threshold, so if its true effect is 17% lower it is worth nothing. Treat cap 2 as the best estimate, not a certainty. Cap 1 loses only 0.01 per user compared with cap 2, so there is a cheap fallback.
4. Check causality. The numbers should come from randomisation: assign users at random to cap 1, 2, 3 and 4 (or to a holdout), then incremental probability of the k-th impression = conversion rate under cap k minus under cap k-1. Observational comparisons are confounded: heavy-exposure users are more active and more likely to buy anyway. In a simulation with zero ad effect, users who saw 4 impressions converted at 0.83% against 0.38% for 1 and 0.28% for 0 (see the run).
5. Size the test. To separate 0.30% from 0.25% at a 1% baseline conversion takes about 620,000 users per arm (80% power, 5% two-sided, illustrative); to see the full 0.30-point effect takes about 17,000 per arm. If that is too large, test cap 1 versus cap 2 first and use the confidence interval to decide.
6. Implement and monitor. Enforce the cap with a per-user counter (including across devices where identity allows), watch spend, reach and conversions, and revisit when creative, season or audience changes; repeat the test periodically.

**Metrics:**
- Incremental probability of impression k = P(convert | cap k) - P(convert | cap k-1), from randomised arms.
- Net value per impression = incremental probability x value - cost per impression; cumulative net per user by cap.
- Break-even incremental probability = cost / value = 0.25%.
- Guardrails: reach (share of target users with at least one impression), total conversions, and spend per incremental conversion.

**Risks:**
- Confounding by user intent if the numbers are observational.
- Selection: the effect of a fourth impression is measured on those the auction reached.
- A flat value of 20 hides the mix of customers; a higher-value customer may justify a higher cap.
- Cross-device counting misses impressions, so the cap is enforced loosely.
- Cap interacts with creative fatigue and the auction; a result for one campaign may not carry over.

**What the interviewer scores:**
- Strong: gets +0.05, +0.01, -0.02, -0.04, cap 2, and the 0.25% break-even rule.
- Strong: points out the margin is thin and sets up a randomised test, with a sample-size estimate.
- Strong: explains why exposure-level comparisons are confounded.
- Weak: choosing the cap by conversion rate alone, or taking the observational lift as causal.

**Example:** Using the question's numbers. Weak versus strong:
- Weak: "Conversion keeps rising with each impression, so I would cap at 4."
- Strong: "Break-even is 0.25%, so only the first two impressions pay: +0.05 and +0.01 net, then -0.02 and -0.04. Cap 2 gives 0.06 per user. The second impression is only just above break-even, so I would run a randomised test across cap levels with several hundred thousand users per arm, because comparing heavy and light viewers measures their intent, not the ads."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if impression costs fall for later impressions? Recompute net value with the actual cost per impression; the rule is the same (incremental probability times value above cost).
- What if conversion value varies by user? Set caps per segment, using the expected value for that segment.
- Is a cap per week the right unit? Test a per-day cap and a spacing rule too; the effect of the second impression may depend on gap.

**Common mistakes:**
- Using total conversion rate by exposure count as incremental.
- Forgetting the cost term, so every impression looks positive.
- Ignoring the 0.05-point margin of the second impression.
- Treating a cap as a purely statistical choice, not a spend and reach decision.
