import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
before = rng.normal(100, 15, 30)
after = before + rng.normal(3, 4, 30)               # same people, small within-person change
print(stats.ttest_rel(after, before).pvalue)         # paired: tiny
print(stats.ttest_ind(after, before).pvalue)         # independent: large -> misses the effect
