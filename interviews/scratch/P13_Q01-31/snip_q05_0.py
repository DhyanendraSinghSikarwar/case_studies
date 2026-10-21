import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
true_mu, n, hits = 50, 25, 0
for _ in range(10000):
    s = rng.normal(true_mu, 10, n)
    lo, hi = stats.t.interval(0.95, n-1, loc=s.mean(), scale=stats.sem(s))
    hits += lo <= true_mu <= hi
print(hits / 10000)    # 0.9464 -> about 95% of intervals cover the truth
