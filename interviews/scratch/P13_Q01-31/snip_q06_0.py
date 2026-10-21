import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
a = rng.normal(0.3, 1, 40); b = rng.normal(0, 1, 40)
print(stats.ttest_ind(a, b).pvalue)                          # two-sided
print(stats.ttest_ind(a, b, alternative='greater').pvalue)   # half of it (effect is in that direction)
print(stats.ttest_ind(a, b, alternative='less').pvalue)      # ~1 - half: wrong direction
