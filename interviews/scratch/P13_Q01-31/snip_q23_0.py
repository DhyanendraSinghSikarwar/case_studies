import numpy as np
rng = np.random.default_rng(2)
t = rng.exponential(10, 500000)                  # mean wait 10 min
print((t[t > 10] - 10).mean().round(2), t.mean().round(2))      # ~10 ~10: memoryless

gaps = rng.exponential(1/5, 100000)              # 5 events per hour
arr = np.cumsum(gaps)
counts = np.bincount(np.floor(arr[arr < 20000]).astype(int))   # events per hour
print(counts.mean().round(3), counts.var().round(3))            # ~5 and ~5: Poisson
