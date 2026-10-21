import numpy as np
from scipy import stats
n, p = 1000, 0.003
k = np.arange(8)
print(np.round(stats.binom.pmf(k, n, p), 4))      # [0.0496 0.1491 0.2242 0.2244 0.1683 0.1009 0.0503 0.0215]
print(np.round(stats.poisson.pmf(k, n*p), 4))     # [0.0498 0.1494 0.224  0.224  0.168  0.1008 0.0504 0.0216]
print(stats.binom.stats(100, 0.3), stats.poisson.stats(3))   # var 21 vs mean 30; var = mean = 3
