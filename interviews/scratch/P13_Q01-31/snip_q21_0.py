import numpy as np
rng = np.random.default_rng(2)
x = rng.exponential(1, 200000)
for n in (10, 100, 10000, 200000):
    print(n, round(x[:n].mean(), 4))     # drifts toward the true mean 1
