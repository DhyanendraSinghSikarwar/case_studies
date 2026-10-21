import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
pop = rng.exponential(1.0, 1_000_000)
print("pop skew", round(stats.skew(pop), 2))                     # 2.0
for n in (2, 30, 500):
    means = rng.choice(pop, (10000, n)).mean(axis=1)
    print(n, round(stats.skew(means), 2), round(means.std(), 3), round(1/np.sqrt(n), 3))
# 2 1.48 0.704 0.707 | 30 0.37 0.18 0.183 | 500 0.06 0.045 0.045

c = rng.standard_cauchy((10000, 500)).mean(axis=1)               # Cauchy: no CLT
print(np.subtract(*np.percentile(c, [75, 25])).round(2))         # IQR ~2 (a single obs has IQR 2): no shrinkage
