import numpy as np
from scipy import stats
rng = np.random.default_rng(2)
x = rng.uniform(1, 10, 200); y = np.exp(x/2) + rng.normal(0, .5, 200)
print(stats.pearsonr(x, y)[0].round(3), stats.spearmanr(x, y)[0].round(3), stats.kendalltau(x, y)[0].round(3))
x2, y2 = x.copy(), y.copy(); x2[0], y2[0] = 1, 500                  # one outlier
print(stats.pearsonr(x2, y2)[0].round(3), stats.spearmanr(x2, y2)[0].round(3))
