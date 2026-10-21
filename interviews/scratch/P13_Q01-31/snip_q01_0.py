import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
a = rng.normal(10.0, 2, 200); b = rng.normal(10.5, 2, 200)
print(stats.ttest_ind(a, b).pvalue)                 # 0.1429

# p-value by brute force: how often does pure chance give a gap this big?
obs = abs(a.mean() - b.mean())
sims = [rng.normal(10,2,200).mean() - rng.normal(10,2,200).mean() for _ in range(5000)]
print(np.mean(np.abs(sims) >= obs))                 # ~0.144, matches

# when H0 is true, p < 0.05 happens ~5% of the time
ps = [stats.ttest_ind(rng.normal(0,1,50), rng.normal(0,1,50)).pvalue for _ in range(5000)]
print(np.mean(np.array(ps) < 0.05))                 # 0.045
