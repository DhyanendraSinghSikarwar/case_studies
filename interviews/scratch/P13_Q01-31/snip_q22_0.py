import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
u = rng.uniform(0, 1, 200000)
print(u.mean().round(3), u.var().round(4), round(1/12, 4))    # 0.5 0.0831 0.0833
lam = 2.0
e = -np.log(1 - u) / lam                                       # inverse transform
print(e.mean().round(3), stats.kstest(e, 'expon', args=(0, 1/lam)).pvalue.round(3))  # mean ~0.5; fits exponential
