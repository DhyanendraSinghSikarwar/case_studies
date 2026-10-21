import numpy as np
from scipy import stats
rng = np.random.default_rng(1)
data = rng.exponential(30, 80)
boots = np.array([rng.choice(data, data.size, replace=True).mean() for _ in range(10000)])
print(np.percentile(boots, [2.5, 97.5]).round(2), data.mean().round(2))   # CI and mean
print(boots.std().round(2), stats.sem(data).round(2))                      # bootstrap SE vs formula SE
res = stats.bootstrap((data,), np.mean, n_resamples=9999, random_state=0, method='percentile')
print(res.confidence_interval)                                             # scipy cross-check
