# Q10 loan default: 12-month labels, live 6 months. Early-warning from repayment behaviour (illustrative numbers)
import numpy as np
rng = np.random.default_rng(10)

# Historical vintages (labels complete): default flag and month of default (1..12)
n_hist = 40_000
p12_hist = 0.060
default = rng.random(n_hist) < p12_hist
month_pmf = np.array([1, 3, 7, 11, 12, 12, 11, 10, 9, 8, 8, 8], float); month_pmf /= month_pmf.sum()
dmonth = np.where(default, rng.choice(np.arange(1, 13), n_hist, p=month_pmf), 99)

by6 = ((dmonth <= 6)).sum(); by12 = (dmonth <= 12).sum()
r = by6 / by12                                  # share of eventual 12-month defaults already visible by month 6
print(f"history: default by month 6 = {by6/n_hist:.2%}, by month 12 = {by12/n_hist:.2%}, visible share r = {r:.2f}")
assert 0.4 < r < 0.5

# Current vintage: only 6 months observed
n_now = 25_000
true_p12_now = 0.075                            # truth we cannot see (worse than the 6.0% history)
d6_now = rng.binomial(n_now, true_p12_now * r) / n_now
print(f"current vintage: default by month 6 = {d6_now:.2%} on {n_now:,} loans")

# Project to 12 months and carry BOTH uncertainties by bootstrap
B = 4000
proj = np.empty(B)
for b in range(B):
    d6 = rng.binomial(n_now, d6_now) / n_now                              # sampling noise now
    h = rng.integers(0, n_hist, n_hist)                                    # resample history
    rb = (dmonth[h] <= 6).sum() / max((dmonth[h] <= 12).sum(), 1)
    proj[b] = d6 / rb
lo, mid, hi = np.percentile(proj, [2.5, 50, 97.5])
print(f"projected 12-month default: {mid:.2%} (95% interval {lo:.2%} to {hi:.2%}); model's predicted: 6.00%")
assert lo < 0.075 < hi and lo > 0.06                 # the interval excludes the model's 6.0%

# What the interval does NOT cover: the assumption that the timing pattern r is unchanged
for r_alt in (0.35, 0.55):
    print(f"if the visible share were {r_alt:.2f} instead of {r:.2f}: projection {d6_now/r_alt:.2%}")
assert d6_now / 0.35 > d6_now / 0.55
