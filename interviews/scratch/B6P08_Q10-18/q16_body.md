**Say this first (1 line):** A shadow run shows how the candidate behaves on real inputs (errors, latency, score differences, decision flips) but not what happens to outcomes or users, so 3.2% differing is a list to investigate, not a yes or no on the switch.

**Clarifying questions:**
- What is the decision threshold, and what does a score of 0.05 mean in decisions? Scores that differ without crossing the threshold may change nothing (0.5 here).
- Do we have delayed labels for the shadow period? If so we can compare accuracy, not just agreement.
- Is the shadow traffic the full mix (peak hours, all segments, edge cases)? A quiet weekday hides the bad cases.
- What is the cost of a wrong decision in each direction? It tells which flips matter.
- Did the shadow call the same features as production, or did it use a different feature path? Skew would make the comparison unfair.

**Approach:**
1. Say what shadow can tell: input handling on live data, error and timeout rate, latency under load, feature availability, score distribution, and how often the decision changes. It is risk-free for users because the candidate's output is not used.
2. Say what it cannot tell: whether the candidate is more accurate (no labels yet), how users react, effects on downstream systems or feedback loops, or behaviour once its own decisions change the data. It also may not reproduce production load if the candidate runs at lower priority.
3. Look at the 16,000: split by direction (candidate higher or lower), by decision flip at the threshold, and by segment, hour and feature missingness. In my simulation, 10,374 had the candidate higher and 5,626 lower; 3,087 (19% of the 16,000, 0.62% of all requests) flipped the decision at threshold 0.5.
4. Review a stratified sample: 200 from the flips and 200 from the non-flips; a 400-request review has a margin of error of about 4.9 points on a share. Where labels exist later, compare accuracy on the flips only: that is where the two models disagree about the action.
5. Decide with a rule: switch to a canary (not to 100%) if the flip count is explained, the flips are not concentrated in one risky segment, latency and errors are within budget, and the labelled comparison on flips is no worse. Do not switch if flips concentrate in a segment (for example new customers) without a reason, or if feature-missing rows dominate the differences.
6. First week: go to a canary with rollback criteria; next quarter: a standard promotion checklist including shadow metrics.
7. Blameless angle: no incident here, but if a past switch went wrong because shadow was treated as proof, write that down as a process gap.

**Metrics:**
- Difference rate = requests with |candidate - production| > 0.05 / all requests = 16,000 / 500,000 = 3.2%.
- Flip rate = requests whose decision changes at the threshold / all requests (0.62% in the run).
- Agreement on decisions = 1 - flip rate; accuracy on the flips once labels arrive.
- Guardrails: candidate error rate, p95 latency, feature-missing rate.

**Risks:**
- Treating 96.8% close scores as safety: the 3.2% might be the high-risk cases.
- Small score gaps can flip decisions near the threshold; a gap above 0.05 is not the same as a flip, and a gap under 0.05 can flip too. Check both.
- Shadow feeds the candidate from the same logs, so any feedback effect is invisible.
- Without labels, "different" does not mean "worse".

**What the interviewer scores:**
- Strong: separates what shadow shows (behaviour) from what it cannot (outcomes).
- Strong: moves from a count to decision flips and a stratified review.
- Strong: proposes the next step (canary) with criteria.
- Weak: "3.2% is low so it is safe" or "differences mean the new model is bad".

**Example:** Illustrative numbers. Weak versus strong:
- Weak: "Only 3.2% differ, so it is safe to switch."
- Strong: "Shadow tells me the candidate runs on live data. It does not tell me it is better. Of the 16,000, I would count how many cross the decision threshold, split by segment, and review 200 flips. If the flips are not concentrated and the candidate is no worse on labelled outcomes, I go to a 5% canary with rollback rules, not to 100%."

**Code:**
{{CODE}}

**Output (my run):**
{{OUTPUT}}

**Follow-ups:**
- Can shadow replace a canary? No. Canary shows user and business effects; shadow shows technical behaviour.
- What if the product owner wants a yes today? Give a conditional yes for a 5% canary with a written stop rule.
- How do you evaluate with delayed labels? Join labels when they arrive, compare both models on the same requests, and use a paired comparison on the flips.

**Common mistakes:**
- Using agreement as accuracy.
- Looking only at average score difference.
- Ignoring segments and the decision threshold.
- Going from shadow straight to 100%.
