import numpy as np
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
rng = np.random.default_rng(2)
g1, g2, g3 = rng.normal(10, 2, 30), rng.normal(10.5, 2, 30), rng.normal(12, 2, 30)
print(stats.f_oneway(g1, g2, g3))
vals = np.concatenate([g1, g2, g3]); lab = np.repeat(['A', 'B', 'C'], 30)
print(pairwise_tukeyhsd(vals, lab))
