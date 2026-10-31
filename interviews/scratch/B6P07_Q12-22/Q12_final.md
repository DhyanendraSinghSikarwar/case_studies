### Q12 ⭐⭐⭐ 🟡 On an extraction task a prompt scored 156 of 200 (78%) in one run and 166 of 200 (83%) in another run of the same model and prompt, because of sampling at temperature 0.7. A teammate wants to ship a new prompt that scored 83% in a single run. What is the run-to-run noise, and how do you design the comparison?
**Asked at:** No public page found for this exact scenario, editor-designed; the theme is adjacent to non-determinism and temperature topics in GenAI guides; related topics appear in public guides for data scientist, ML engineer and GenAI engineer loops; no page for the exact framing; search snippets only, not opened
**Say this first (1 line):** A 5-point gap between two runs of the same prompt is the noise level, so one 83% run proves nothing; I would compare the two prompts on the same items, several runs each, and ship only if the paired gain clears the noise.

**Clarifying questions:**
- Are the 200 items the same in both runs? Why it matters: same items means a paired comparison, which is much tighter than two separate samples.
- Is the new prompt's 83% on those same 200 items? Why it matters: if not, item difficulty is mixed into the gap.
- How is a run scored (exact match, field-level, judge)? Why it matters: a judge adds its own noise on top of sampling noise.
- Do we need sampling at temperature 0.7, or is that a leftover setting? Why it matters: production settings decide which noise we must live with.
- What gain is worth the switch (cost, latency, risk)? Why it matters: sets the minimum effect size and the sample size.

**Approach:**
1. Measure the noise first. Run the OLD prompt 5 to 10 times on the same 200 items and look at the spread. Here the two runs already differ by 5 points (156 versus 166 of 200).
2. Upper bound from the binomial: one run has an SD of about 2.8 points, and the gap between two runs has an SD of about 4.0 points, so 5 points is 1.26 SD (p about 0.21).
3. Item-level noise is usually smaller, because the same items are re-asked. A toy model with a few coin-flip items gives about 1.5 points per run. The honest range is therefore roughly 1.5 to 2.8 points per run.
4. Note the teammate's 83% equals the old prompt's second run. There is no evidence of improvement yet.
5. Run both prompts k times (say 5) on the same items. Score each item as the mean over runs. Compare per item (paired).
6. Test with a paired method: McNemar or sign test on majority-vote results, or a paired bootstrap over items. Report the difference with an interval.
7. Size the set for the gain you care about. For +3 points at 80% power, about 2,788 items per prompt unpaired, about 869 paired if 10% of items disagree.
8. Decide before looking: ship if the interval for the gain excludes zero and the lower end beats the cost of switching.

**Metrics:**
- Accuracy per run = items correct / 200 items. Mean accuracy per prompt = average over runs.
- Run-to-run SD = standard deviation of accuracy across repeat runs of the same prompt.
- Paired gain = (items only new gets right, minus items only old gets right) / N, with a 95% interval.
- Flip rate = items whose answer changes between runs of the same prompt / N.
- Guardrails: parse-failure rate, latency, cost per call, and no loss on a held-out slice that matters.

**Risks:**
- Shipping a prompt picked as the best of several single runs (winner's curse: the best of many noisy runs is biased upward).
- Tuning the prompt on the same 200 items, then testing on them.
- Judge noise mistaken for model noise.
- Treating "not significant" as "no difference". The set may just be too small.

**What the interviewer scores:**
- Strong: measures noise by repeating the baseline, uses a paired design, quotes an interval and a sample size.
- Strong: notices the new 83% matches the old prompt's own 83% run.
- Weak: "83 is higher than 78, ship it", or "just set temperature 0" without testing the production setting.
- Weak: no number for the noise, no mention of the same items.

**Example:** Illustrative numbers. Old prompt: 156 and 166 of 200 in two runs. New prompt: one run of 166 of 200. Weak answer: "It is 83, the old one is 78, so we have a 5-point gain, let us ship." Strong answer: "The old prompt itself moved 5 points between runs, so a single 83 is inside the noise. I will run each prompt 5 times on the same items, compare item by item, and look at the interval. If 38 items flip to the new prompt and 22 flip to the old one, the sign test gives p of about 0.052, which is borderline, so I would collect more items before shipping."

**Code:**
```python
import math
import numpy as np
from scipy import stats

n = 200
a, b = 156, 166
pa, pb = a / n, b / n
assert (pa, pb) == (0.78, 0.83)
pbar = (a + b) / (2 * n)
se_run = math.sqrt(pbar * (1 - pbar) / n)          # binomial SD of one run's accuracy (upper bound)
se_diff = math.sqrt(2) * se_run                    # two independent runs
z = (pb - pa) / se_diff
p2 = 2 * (1 - stats.norm.cdf(z))
print(f"one-run SD (binomial upper bound) = {se_run*100:.2f} pts; SD of difference of two runs = {se_diff*100:.2f} pts")
print(f"observed gap 5.0 pts = {z:.2f} SD, two-sided p = {p2:.2f}")
assert round(se_run * 100, 1) == 2.8 and round(se_diff * 100, 1) == 4.0 and round(z, 2) == 1.26 and round(p2, 2) == 0.21

# Toy flaky-item model (invented): 150 steady-right items, 20 coin-flip items, 30 mostly-wrong items.
rng = np.random.default_rng(7)
p_item = np.array([0.98] * 150 + [0.5] * 20 + [0.05] * 30)
var_items = float((p_item * (1 - p_item)).sum())
sd_run_toy = math.sqrt(var_items) / n * 100
sd_diff_toy = math.sqrt(2) * sd_run_toy
runs = rng.random((20000, 2, n)) < p_item
acc = runs.mean(axis=2)
gap = np.abs(acc[:, 0] - acc[:, 1])
print(f"toy same-items model: mean acc {p_item.mean()*100:.1f}%, one-run SD {sd_run_toy:.2f} pts, SD of gap {sd_diff_toy:.2f} pts")
print(f"toy: share of run pairs with |gap| >= 5 pts = {np.mean(gap >= 0.05 - 1e-9)*100:.1f}%")
assert round(sd_run_toy, 1) == 1.5 and round(sd_diff_toy, 1) == 2.2
assert abs(np.mean(gap >= 0.05 - 1e-9) - 0.03) < 0.02

# Sample size for a 3-point gain at 80% power, 5% two-sided.
za, zb = 1.96, 0.84
delta, p0 = 0.03, 0.80
n_unpaired = 2 * p0 * (1 - p0) * (za + zb) ** 2 / delta ** 2
d = 0.10                                           # assumed share of items where the two prompts disagree
n_paired = ((za * math.sqrt(d) + zb * math.sqrt(d - delta ** 2)) / delta) ** 2
print(f"items needed per prompt, unpaired: {n_unpaired:.0f}; paired (10% of items disagree): {n_paired:.0f}")
assert round(n_unpaired) == 2788 and round(n_paired) == 869

# Paired McNemar-style exact test on a made-up result: 400 items, 5 runs per prompt, majority vote.
b_only, a_only = 38, 22                            # items only new right, items only old right
p_mc = stats.binomtest(b_only, b_only + a_only, 0.5).pvalue
print(f"discordant 38 vs 22 -> exact sign test p = {p_mc:.3f}")
assert round(p_mc, 3) == 0.052
```

**Output (my run):**
```
one-run SD (binomial upper bound) = 2.80 pts; SD of difference of two runs = 3.96 pts
observed gap 5.0 pts = 1.26 SD, two-sided p = 0.21
toy same-items model: mean acc 79.3%, one-run SD 1.53 pts, SD of gap 2.16 pts
toy: share of run pairs with |gap| >= 5 pts = 2.8%
items needed per prompt, unpaired: 2788; paired (10% of items disagree): 869
discordant 38 vs 22 -> exact sign test p = 0.052
```

**Follow-ups:**
- Would temperature 0 fix this? It removes most sampling noise, but it may not match production, and Book 2 Part 02 Q21 ("Is temperature 0 deterministic? What causes run-to-run differences in LLM output, and how do you get reproducibility?") covers why outputs can still vary. Test the setting you will ship.
- What if the set is only 200 items and cannot grow? Use more runs to cut sampling noise, but item-selection noise stays, so report the interval and say it is a small set.
- Majority vote or mean? Use the mean for the estimate. Majority vote is fine for the sign test, but say so.

**Common mistakes:**
- Comparing two single runs.
- Using the independent-sample formula when the items are shared (too loose) or ignoring item correlation in the other direction.
- Forgetting that the first run of each prompt is not special; picking the best run.
- Quoting a p-value without a sample size or effect size.

