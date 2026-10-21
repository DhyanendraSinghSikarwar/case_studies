import numpy as np
from scipy.stats import ttest_ind
rng=np.random.default_rng(0)
ps=[ttest_ind(rng.normal(0,1,500),rng.normal(0,1,500)).pvalue for _ in range(2000)]
print("A/A rejection rate:", np.mean(np.array(ps)<0.05), " p-value mean (uniform~0.5):", round(np.mean(ps),2))
