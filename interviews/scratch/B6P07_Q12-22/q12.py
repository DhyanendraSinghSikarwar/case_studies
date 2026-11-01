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
