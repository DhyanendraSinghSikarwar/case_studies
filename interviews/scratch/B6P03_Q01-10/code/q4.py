# Q4 income missing 22%: pattern by age, what the data can and cannot say (illustrative data)
import numpy as np
from scipy.stats import chi2_contingency

# Counts from the prompt
old_n, young_n = 4_000, 6_000
old_miss, young_miss = 1_600, 600
assert old_miss / old_n == 0.40 and young_miss / young_n == 0.10
assert old_miss + young_miss == 2_200 and (old_miss + young_miss) / (old_n + young_n) == 0.22
tab = np.array([[old_miss, old_n - old_miss], [young_miss, young_n - young_miss]])
chi2, p, _, _ = chi2_contingency(tab, correction=False)
print(f"missing vs age group: chi2={chi2:.0f}, p={p:.2e}  -> not MCAR (missingness depends on age)")
assert p < 1e-100

# Two worlds with the SAME observed missing rates by age (40% / 10%) but different mechanisms
rng = np.random.default_rng(5)
def world(mnar):
    old = np.r_[np.ones(old_n, bool), np.zeros(young_n, bool)]
    mean = np.where(old, 70.0, 100.0)                    # income index: older group lower on average
    inc = mean * rng.lognormal(0, 0.4, len(old)) / np.exp(0.08)
    base = np.where(old, 0.40, 0.10)
    if mnar:                                             # within each age group, high earners hide income more
        miss = np.zeros(len(old), bool)
        for g, rate in ((True, 0.40), (False, 0.10)):
            idx = np.flatnonzero(old == g)
            rank = inc[idx].argsort().argsort() / len(idx)          # 0..1 within group
            w = 0.2 + 1.6 * rank; w = w / w.mean() * rate           # exact group mean = rate
            miss[idx] = rng.random(len(idx)) < np.minimum(w, 1)
    else:
        miss = rng.random(len(old)) < base                          # depends on age only
    return old, inc, miss

for label, mnar in (("MAR (age only)", False), ("MNAR (also income)", True)):
    old, inc, miss = world(mnar)
    obs = ~miss
    true_mean = inc.mean()
    cc = inc[obs].mean()                                             # complete-case mean
    # MAR repair: group means among observed, weighted by the true age mix
    adj = old.mean() * inc[obs & old].mean() + (1 - old.mean()) * inc[obs & ~old].mean()
    print(f"{label:20s} missing by age: {miss[old].mean():.3f} / {miss[~old].mean():.3f}  "
          f"true mean={true_mean:.1f}  complete-case={cc:.1f}  age-adjusted={adj:.1f}")
    if not mnar:
        assert abs(adj - true_mean) < 1.5 and abs(cc - true_mean) > 2     # adjustment works under MAR
    else:
        assert abs(adj - true_mean) > 3                                    # adjustment fails under MNAR
