# Q30 lookalike campaign: reported vs incremental cost per conversion (illustrative numbers)
from math import sqrt
n_t = n_c = 500_000
conv_t, conv_c = 4_000, 3_500
assert conv_t / n_t == 0.008 and conv_c / n_c == 0.007
spend = 40_000
reported = spend / conv_t
assert reported == 10.0
incr = conv_t - conv_c
assert incr == 500
incr_cost = spend / incr
assert incr_cost == 80.0
print(f"reported cost per conversion {reported:.0f}; incremental {incr_cost:.0f}; ratio {incr_cost/reported:.0f}x")
print(f"share of reported conversions that would have happened anyway: {conv_c/conv_t:.1%}")
assert conv_c / conv_t == 0.875

# Interval on the lift (two-proportion, unpooled SE)
p_t, p_c = conv_t / n_t, conv_c / n_c
se = sqrt(p_t*(1-p_t)/n_t + p_c*(1-p_c)/n_c)
lo, hi = (p_t - p_c) - 1.96*se, (p_t - p_c) + 1.96*se
inc_lo, inc_hi = lo * n_t, hi * n_t
print(f"incremental conversions 95% interval {inc_lo:.0f} to {inc_hi:.0f}; cost per incremental {spend/inc_hi:.0f} to {spend/inc_lo:.0f}")
assert 325 < inc_lo < 335 and 665 < inc_hi < 675
z = (p_t - p_c) / sqrt((p_t+p_c)/2 * (1-(p_t+p_c)/2) * 2 / n_t)
assert 5.5 < z < 6.0
print(f"z = {z:.1f}")

# Relative lift and what a better audience could do (invented): same spend, same reach, lift doubles
rel = (p_t - p_c) / p_c
assert abs(rel - 1/7) < 1e-9
print(f"relative lift {rel:.1%}")
better = spend / 1000
print(f"if lift were 1,000 incremental conversions at the same spend: cost per incremental {better:.0f}")
assert better == 40.0

# Holdout sizing: control needed to detect a 0.1-point lift on a 0.7% base, per arm (alpha .05, power .8)
from statistics import NormalDist
zz = NormalDist().inv_cdf
n = (zz(.975)+zz(.8))**2 * (0.008*0.992 + 0.007*0.993) / 0.001**2
print(f"users per arm to detect 0.80% vs 0.70%: {n:,.0f}")
assert 100_000 < n < 120_000
