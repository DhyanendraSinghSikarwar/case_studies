import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
x = rng.lognormal(3, 1, 60); y = rng.lognormal(3.4, 1, 60)
print(stats.ttest_ind(x, y, equal_var=False).pvalue)                 # Welch t-test
print(stats.mannwhitneyu(x, y, alternative='two-sided').pvalue)      # rank test
