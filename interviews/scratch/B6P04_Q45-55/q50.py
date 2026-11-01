# Q50: why interleaving needs far fewer users than a user-level A/B test (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(50)
LIFT = 0.005                                         # ranker B gets 0.5% more clicks than A
def users(n, shape):
    return rng.gamma(shape, 2.0 / shape, n)          # mean 2 clicks per user, heavy between-user spread
def ab_p(n, shape):
    lam = users(2*n, shape); arm = np.r_[np.zeros(n, bool), np.ones(n, bool)]
    y = rng.poisson(lam * np.where(arm, 1 + LIFT, 1.0))
    return stats.ttest_ind(y[arm], y[~arm], equal_var=False).pvalue
def il_p(n, shape):
    lam = users(n, shape); clicks = rng.poisson(lam)            # every user sees the interleaved list
    pB = (1 + LIFT) / (2 + LIFT)                                 # share of clicks that land on B's items
    d = 2 * rng.binomial(clicks, pB) - clicks                    # per-user (B clicks - A clicks)
    return stats.ttest_1samp(d, 0).pvalue
def power(f, n, shape, reps=400):
    return np.mean([f(n, shape) < 0.05 for _ in range(reps)])
for shape in (4.0, 0.3):
    # analytic users needed for 80% power, from variances
    mean, var_lam = 2.0, 4.0 / shape
    n_ab = 2 * (1.96 + 0.84)**2 * (var_lam + mean) / (LIFT * mean)**2          # per arm, Poisson mixture variance
    pB = (1 + LIFT) / (2 + LIFT); mu_d = mean * (2*pB - 1); var_d = mean * (1 - (2*pB-1)**2) + (2*pB-1)**2 * var_lam
    n_il = (1.96 + 0.84)**2 * var_d / mu_d**2                                    # total users, one group
    print(f"between-user spread shape={shape}: A/B needs {n_ab:,.0f} per arm ({2*n_ab:,.0f} total); interleaving {n_il:,.0f} users; ratio {2*n_ab/n_il:.1f}x")
    if shape == 0.3: ratio_heavy = 2*n_ab/n_il
    if shape == 4.0: ratio_light = 2*n_ab/n_il
assert ratio_heavy > ratio_light > 1.4
# check by simulation at the interleaving sample size
pa, pi = power(ab_p, 315_000, 0.3, 100), power(il_p, 630_000, 0.3, 100)
print("simulated power with the SAME 630,000 users (heavy-tailed): A/B 315,000 per arm =", pa, "| interleaving =", pi)
assert pi > 0.7 and pa < 0.3
