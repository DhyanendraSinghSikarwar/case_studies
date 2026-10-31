**Say this first (1 line):** At the stated 50-to-5 costs, threshold Y costs about 23,429 and threshold X about 40,667, so Y wins unless a miss costs less than about 1.4 times a false flag, and I would get the three groups to agree on the cost matrix first.

**Clarifying questions:**
- Where do the 50 and 5 come from, and does Legal see harm in wrongful flags that 5 understates? Why: the answer flips if false flags are costlier.
- What is the human review capacity? Why: Y flags about 2,286 items versus 1,333 for X.
- Can action be tiered (auto remove, review, leave)? Why: tiers beat one threshold.
- Is the 2,000 violation count and the precision and recall measured on a fresh sample? Why: errors in them move the cost.
- Who decides if the groups still disagree? Why: needs an owner.

**Approach:**
1. Compute: X has 1,200 caught, 800 missed, about 133 wrongly flagged. Y has 1,600 caught, 400 missed, about 686 wrongly flagged.
2. Cost = misses x 50 + false flags x 5. X is 40,666.67; Y is 23,428.57; Y is cheaper by 17,238.
3. Compute the break-even miss-to-false-flag cost ratio (1.381) and show the groups how far their views are from it.
4. Get Legal, growth and trust-and-safety to agree one cost matrix, with ranges for each team's view.
5. Run sensitivity: at what cost does the choice change?
6. Offer a tiered policy: high score auto-actioned, middle band to review, within capacity.

**Metrics:** Cost = FN x 50 + FP x 5. FN = positives x (1 - recall). FP = TP / precision - TP. Review load = flagged items. Guardrails: review capacity, appeal rate on wrongful flags.

**Risks:**
- Unmodelled costs: user harm, appeals, legal exposure.
- Precision and recall measured on small samples.
- Each team optimising its own number.

**What the interviewer scores:**
- Strong: correct arithmetic, break-even ratio, capacity check, a decision process.
- Weak: arithmetic errors, or picking by who shouts loudest.

**Example:** X: recall 0.6 on 2,000 gives TP 1,200 and FN 800. Flagged = 1,200/0.9 = 1,333.33 so FP 133.33. Cost 800 x 50 + 133.33 x 5 = 40,666.67. Y: TP 1,600, FN 400, flagged 2,285.71, FP 685.71, cost 20,000 + 3,428.57 = 23,428.57. Fractions of items arise because 90% and 70% do not divide evenly; rounded, they are 40,665 and 23,430. The 100,000 total items is not needed.
- Weak: "Y has lower precision so X is better."
- Strong: "Y costs 17,238 less. It only loses if a miss costs under 1.4 times a false flag. Let us agree the cost matrix and what capacity we have."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- What if Legal says a false flag costs 50? Then FP weight rises: X would cost 800 x 50 + 133.33 x 50 = 46,667 and Y 400 x 50 + 685.71 x 50 = 54,286, so X wins.
- Could a third threshold be better? Possibly. Sweep the curve, and see Book 1 Part 03, Q41: "Derive the Bayes-optimal threshold for a given cost matrix and explain why it needs calibrated probabilities."

**Common mistakes:** Using the 100,000 in the cost. Ignoring review capacity. Using one cost for all groups. Presenting a winner without sensitivity.
