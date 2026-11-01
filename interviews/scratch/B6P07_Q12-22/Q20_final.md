### Q20 ⭐⭐ 🟢 Before switching models you plan to shadow 10% of 700,000 weekly calls on the candidate at an illustrative 0.0153 per call, while the old model still answers users. Compute the weekly shadow cost, and say what you can and cannot learn from shadow traffic compared with an A/B test.
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to rollout and shadow-traffic topics in LLMOps material; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** Shadowing 10% costs about 1,071 a week (70,000 calls x 0.0153) and tells me how the candidate behaves on real inputs, but not how users react, so it is a filter before an A/B test, not a replacement.

**Clarifying questions:**
- Is the 0.0153 per call the candidate's real average cost? Why it matters: cost scales with output length, which can differ between models.
- Does the candidate call tools or write anywhere? Why it matters: shadow calls must never take real actions.
- Is the 10% random or stratified by intent? Why it matters: rare intents may be missed.
- What decision follows (go to a 5% canary, or full switch)? Why it matters: sets what evidence is needed.
- Can we log user data for the shadow outputs? Why it matters: privacy and retention apply to shadow logs too.

**Approach:**
1. Cost: 700,000 x 10% = 70,000 calls x 0.0153 = 1,071 a week; the full-traffic equivalent is 10,710.
2. Sample randomly, plus enough of each rare intent. Never let shadow outputs reach users or trigger actions.
3. Compare per call with the old model: format validity, length, latency, token cost, refusal rate, and disagreement.
4. Review the disagreements. If 12% disagree (invented), that is 8,400 pairs; read a random 400 and note the margin is about plus or minus 4.9 points.
5. Use shadow for rare failures too. Zero failures in 70,000 calls bounds the failure rate near 0.0043% at 95%.
6. What shadow cannot show: whether users are happier, resolve more, or come back. Users never saw the candidate's answer, and in multi-turn chats the conversation continues from the old model's replies, so later turns are not what the candidate would have faced.
7. Next step: a small live canary or A/B. To see +1 point on a 60% resolution rate you need about 37,600 conversations per arm.

**Metrics:**
- Shadow cost = shadowed calls x cost per call.
- Disagreement rate = calls where the models' answers differ materially / shadowed calls.
- Candidate win rate on disagreements = candidate better / reviewed disagreements, with an interval.
- Parse-failure rate and latency p95 for the candidate.
- Guardrails: shadow adds no user-visible latency, rate limits not hit.

**Risks:**
- Shadow calls slow the main path or hit rate limits.
- Shadow tool calls cause real side effects.
- Judging with a judge that favours its own family.
- Treating "looks fine on shadow" as proof of better user outcomes.

**What the interviewer scores:**
- Strong: correct cost, clear can and cannot list, next step to A/B with a sample size.
- Strong: side-effect and multi-turn caveats.
- Weak: "shadow is as good as an A/B test".
- Weak: no cost or sample numbers.

**Example:** Illustrative. Weak: "Shadow looked good so switch." Strong: "Shadow showed the candidate parses 99.5%, is 12% different, and wins 58% of 400 reviewed disagreements, which is not decisive at plus or minus 4.9 points. It cost 1,071 for the week. I would go to a 5% canary and watch resolution and escalation."

**Code:**
```python
import math
weekly, share, price = 700_000, 0.10, 0.0153
shadow = weekly * share
cost = shadow * price
print(f"shadow calls {shadow:,.0f}; weekly cost {cost:,.0f}; full-traffic equivalent {weekly*price:,.0f}")
assert shadow == 70_000 and round(cost) == 1071 and round(weekly * price) == 10_710
rule3 = 3 / shadow
print(f"0 failures in {shadow:,.0f} shadow calls -> 95% upper bound ~{rule3:.4%} per call (rule of three)")
assert round(rule3 * 100, 4) == 0.0043
# What an A/B test needs to see a 1-point change in a 60% resolution rate (80% power, 5% two-sided).
za, zb = 1.96, 0.84
p = 0.60
n_arm = 2 * p * (1 - p) * (za + zb) ** 2 / 0.01 ** 2
print(f"A/B needs ~{n_arm:,.0f} conversations per arm for +1 point at 60%")
assert round(n_arm) == 37_632
# Disagreement review: if models differ on 12% of shadow calls, how many are there to read?
dis = shadow * 0.12
print(f"if 12% disagree: {dis:,.0f} pairs; reviewing a random 400 gives a margin of about +-{1.96*math.sqrt(0.25/400)*100:.1f} pts on 'candidate better'")
assert dis == 8400 and round(1.96 * math.sqrt(0.25 / 400) * 100, 1) == 4.9
```

**Output (my run):**
```
shadow calls 70,000; weekly cost 1,071; full-traffic equivalent 10,710
0 failures in 70,000 shadow calls -> 95% upper bound ~0.0043% per call (rule of three)
A/B needs ~37,632 conversations per arm for +1 point at 60%
if 12% disagree: 8,400 pairs; reviewing a random 400 gives a margin of about +-4.9 pts on 'candidate better'
```

**Follow-ups:**
- Why not skip shadow? It is cheap protection against format and latency surprises before users see anything.
- Shadow or canary first? Shadow first for safety, then canary for outcomes.
- How long to shadow? Long enough to cover weekly cycles and rare intents; a week is a starting point.

**Common mistakes:**
- Letting shadow outputs have side effects.
- Using shadow to claim user satisfaction.
- Skipping rare-intent coverage.
- Forgetting shadow logs are data too.

