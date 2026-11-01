**Say this first (1 line):** At the stated 50-to-5 costs, threshold Y costs 27,500 and threshold X 41,500, so Y wins unless a miss costs less than two thirds of a false flag, and I would get the three groups to agree on the cost matrix first.

**Clarifying questions:**
- Where do the 50 and 5 come from, and does Legal see harm in wrongful flags that 5 understates? Why: if a false flag costs more than a miss, the choice flips.
- What is the human review capacity? Why: Y flags 2,000 items versus 1,500 for X.
- Can action be tiered (auto remove, review, leave)? Why: tiers beat one threshold.
- Are precision and recall measured on a fresh labelled sample, and how big? Why: errors in them move the cost.
- Who decides if the groups still disagree? Why: needs an owner.

**Approach:**
1. Compute: X catches 1,200 of 2,000, misses 800, flags 1,500 (1,200 / 0.8), so 300 are false. Y catches 1,500, misses 500, flags 2,000, so 500 are false.
2. Cost = misses x 50 + false flags x 5. X is 800 x 50 + 300 x 5 = 41,500. Y is 500 x 50 + 500 x 5 = 27,500. Y is cheaper by 14,000.
3. Compute the break-even miss-to-false-flag cost ratio: 200 extra false flags buy 300 fewer misses, so ratio 200 / 300 = 0.667.
4. Get Legal, growth and trust-and-safety to agree one cost matrix, with a range for each team's view.
5. Run sensitivity: if a false flag cost 100 and a miss 50 (ratio 0.5), X costs 70,000 and Y 75,000, so X wins.
6. Offer a tiered policy: high score auto-actioned, middle band to review, within capacity.

**Metrics:** Cost = FN x 50 + FP x 5. FN = positives x (1 - recall). FP = TP / precision - TP. Review load = flagged items. Guardrails: review capacity, appeal rate on wrongful flags.

**Risks:**
- Unmodelled costs: user harm, appeals, legal exposure.
- Precision and recall measured on small samples.
- Each team optimising its own number.

**What the interviewer scores:**
- Strong: correct arithmetic, break-even ratio, capacity check, a decision process.
- Weak: arithmetic errors, or picking by who shouts loudest.

**Example:** X: TP 1,200, FN 800, flagged 1,500, FP 300, cost 40,000 + 1,500 = 41,500. Y: TP 1,500, FN 500, flagged 2,000, FP 500, cost 25,000 + 2,500 = 27,500. The 100,000 total items does not enter the cost.
- Weak: "X has higher precision so X is better."
- Strong: "Y costs 14,000 less. It only loses if a miss costs under two thirds of a false flag. Let us agree the cost matrix and our review capacity."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if Legal says a false flag costs 100 against a miss of 50? Then X costs 70,000 and Y 75,000, so X wins.
- Could a third threshold be better? Possibly. Sweep the curve, and see Book 1 Part 03, Q41: "Derive the Bayes-optimal threshold for a given cost matrix and explain why it needs calibrated probabilities."

**Common mistakes:** Using the 100,000 in the cost. Ignoring review capacity. Using one cost for all groups. Presenting a winner without sensitivity.
