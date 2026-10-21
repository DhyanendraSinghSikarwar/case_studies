import numpy as np
rng = np.random.default_rng(0)
sims, days, n = 2000, 14, 500
fp = 0
for _ in range(sims):
    ca = rng.binomial(n, 0.1, days).cumsum(); cb = rng.binomial(n, 0.1, days).cumsum()
    N = n * np.arange(1, days + 1)
    pa, pb, pp = ca / N, cb / N, (ca + cb) / (2 * N)
    z = (pb - pa) / np.sqrt(2 * pp * (1 - pp) / N)
    fp += (np.abs(z) > 1.96).any()
print("false positive rate with daily peeking:", fp / sims)
