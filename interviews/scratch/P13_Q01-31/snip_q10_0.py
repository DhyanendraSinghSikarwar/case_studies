import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
n = 200000
a = rng.normal(100, 20, n); b = rng.normal(100.4, 20, n)
r = stats.ttest_ind(b, a)
d = (b.mean() - a.mean()) / np.sqrt((a.var(ddof=1) + b.var(ddof=1)) / 2)
diff = b.mean() - a.mean(); se = np.sqrt(a.var(ddof=1)/n + b.var(ddof=1)/n)
print(r.pvalue, round(d, 3), round(diff, 3), np.round([diff - 1.96*se, diff + 1.96*se], 3))
# 4.4e-08  0.017  0.346  [0.222 0.47]
