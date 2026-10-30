import numpy as np
from scipy import stats

# Illustrative numbers from the prompt
n_c, n_t = 52_000, 48_000
x_c, x_t = round(0.048 * n_c), round(0.050 * n_t)   # conversions: 2496 and 2400

# 1) SRM check: expected 50/50
exp = 50_000
chi2 = ((n_c - exp) ** 2 + (n_t - exp) ** 2) / exp
p_srm = stats.chi2.sf(chi2, 1)
print("SRM chi2 =", chi2, " p =", p_srm)
assert chi2 == 160.0 and p_srm < 1e-30

# 2) The prompt's conversion test, recomputed from the stated counts
p_c, p_t = x_c / n_c, x_t / n_t
pool = (x_c + x_t) / (n_c + n_t)
se = np.sqrt(pool * (1 - pool) * (1 / n_c + 1 / n_t))
z = (p_t - p_c) / se
p_two = 2 * stats.norm.sf(abs(z))
print(f"conversion control {p_c:.4f}, treatment {p_t:.4f}, diff {p_t-p_c:.4f}")
print(f"z = {z:.2f}, two-sided p = {p_two:.3f}, one-sided p = {stats.norm.sf(z):.3f}")
assert p_two > 0.10          # the prompt's p = 0.03 does NOT follow from these counts

# 3) Chance that a fair 50/50 split ever looks like 52,000 / 48,000
print("P(|diff| >= 2000 under fair split) =", 2 * stats.binom.cdf(48_000, 100_000, 0.5))

# 4) Why the SRM matters. The treatment arm is 2,000 short of 50,000. Suppose those 2,000
#    were low converters (illustrative: 1.0%) dropped by a bug. Treatment with them restored:
lost = 2_000
rate_full = (x_t + lost * 0.01) / (n_t + lost)
gap = rate_full - p_c
print(f"treatment rate with the 2,000 restored: {rate_full:.4f}; gap to control: {gap*100:.2f} points")
assert abs(gap) < 0.0005     # the 0.2-point gap shrinks to about 0.04 points
