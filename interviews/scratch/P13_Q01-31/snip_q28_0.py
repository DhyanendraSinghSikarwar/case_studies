import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
x = rng.exponential(1, 200)
print(stats.shapiro(x).pvalue)                       # tiny -> not normal
rej = 0
for _ in range(4000):
    a = rng.exponential(1, 40); b = rng.exponential(1, 40)
    rej += stats.ttest_ind(a, b).pvalue < 0.05
print(rej / 4000)                                    # ~0.05: t-test still holds its Type I rate
big = rng.standard_t(8, 5000)                        # mildly heavy tails, n large
print(stats.shapiro(big).pvalue)                     # very small p although practically harmless
