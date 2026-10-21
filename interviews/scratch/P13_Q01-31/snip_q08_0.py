import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
print([round(stats.norm.cdf(k) - stats.norm.cdf(-k), 4) for k in (1, 2, 3)])  # [0.6827, 0.9545, 0.9973]
x = rng.normal(60, 8, 300)
z = (x - x.mean()) / x.std(ddof=1)
print(z.mean().round(6), z.std(ddof=1).round(3))                 # ~0 1.0
print(stats.shapiro(x).pvalue.round(3))                          # 0.697 -> consistent with normal
print(stats.shapiro(rng.lognormal(0, 1, 300)).pvalue)            # ~1e-20 -> not normal
print(stats.probplot(x, dist='norm')[1][2].round(4))             # Q-Q straightness r = 0.998
