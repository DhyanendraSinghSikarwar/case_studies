import numpy as np
from scipy import stats
rng = np.random.default_rng(42)

# What sample size makes 6.3% vs 6.0% give p = 0.03? (illustrative: infer n per arm)
p_c, p_t = 0.060, 0.063
z_target = stats.norm.isf(0.03 / 2)
pool = (p_c + p_t) / 2
n_needed = 2 * pool * (1 - pool) * (z_target / (p_t - p_c)) ** 2
print(f"p = 0.03 needs about {n_needed:,.0f} users per arm at day 4")
n4 = 59_000
se = np.sqrt(2 * pool * (1 - pool) / n4)
z4 = (p_t - p_c) / se
print(f"with n = {n4:,} per arm: z = {z4:.2f}, p = {2*stats.norm.sf(z4):.3f}")
assert abs(2 * stats.norm.sf(z4) - 0.03) < 0.005
lo, hi = (p_t - p_c) - 1.96 * se, (p_t - p_c) + 1.96 * se
print(f"95% CI for the difference: {lo*100:.2f} to {hi*100:.2f} points")
assert abs(lo*100 - 0.03) < 0.01 and abs(hi*100 - 0.57) < 0.01
assert abs(p_t / p_c - 1 - 0.05) < 1e-9      # 5% relative

# Peeking: A/A test (no true effect), 14 daily looks, 5,000 users per arm per day
days, per_day, sims, p0 = 14, 5_000, 4_000, 0.06
xa = rng.binomial(per_day, p0, size=(sims, days)).cumsum(axis=1)
xb = rng.binomial(per_day, p0, size=(sims, days)).cumsum(axis=1)
n = per_day * np.arange(1, days + 1)
pp = (xa + xb) / (2 * n)
z = (xb / n - xa / n) / np.sqrt(2 * pp * (1 - pp) / n)
fp_any = (np.abs(z) > 1.96).any(axis=1).mean()
fp_final = (np.abs(z[:, -1]) > 1.96).mean()
print(f"false win rate: stop at first p<0.05 in 14 daily looks = {fp_any:.3f}; one look at day 14 = {fp_final:.3f}")
assert 0.15 < fp_any < 0.27 and 0.03 < fp_final < 0.07

# Pocock-style constant boundary for 14 equally spaced looks (via simulation of the null)
zz = rng.standard_normal((200_000, days)).cumsum(axis=1) / np.sqrt(np.arange(1, days + 1))
bound = np.quantile(np.abs(zz).max(axis=1), 0.95)
print(f"constant z boundary for 14 looks at overall 5%: {bound:.2f}  (day-4 z = {z4:.2f} is below it)")
assert z4 < bound
