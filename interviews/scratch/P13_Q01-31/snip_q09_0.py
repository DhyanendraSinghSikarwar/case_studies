import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
x = rng.normal(52, 10, 20)
t = (x.mean() - 50) / (x.std(ddof=1) / np.sqrt(20))
print(round(t, 3), round(2 * stats.t.sf(abs(t), 19), 4))   # 0.499 0.6238
print(stats.ttest_1samp(x, 50))                             # same
print(stats.t.ppf(0.975, [5, 20, 100, 10000]).round(3), stats.norm.ppf(0.975).round(3))
