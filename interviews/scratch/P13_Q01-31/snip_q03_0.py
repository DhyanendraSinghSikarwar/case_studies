import numpy as np
from scipy import stats
rng = np.random.default_rng(0)
x = rng.normal(100, 15, 400)
sd = x.std(ddof=1); se = sd / np.sqrt(len(x))
print(round(sd, 2), round(se, 2), round(stats.sem(x), 2))  # 16.64 0.83 0.83
