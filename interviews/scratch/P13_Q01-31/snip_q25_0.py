import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
f = g = 0
for _ in range(4000):
    a = rng.normal(0, 1, 15); b = rng.normal(0, 4, 60)         # H0 true, unequal variances
    f += stats.ttest_ind(a, b).pvalue < 0.05                    # pooled
    g += stats.ttest_ind(a, b, equal_var=False).pvalue < 0.05   # Welch
print(f/4000, g/4000)     # pooled 0.001 vs Welch 0.0505
