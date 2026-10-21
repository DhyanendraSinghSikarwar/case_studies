import numpy as np
rng = np.random.default_rng(0)
for d in [2, 10, 100, 1000]:
    X = rng.uniform(size=(1000, d))
    q = rng.uniform(size=d)
    dist = np.linalg.norm(X - q, axis=1)
    print(f"d={d:<5} (max-min)/min = {(dist.max()-dist.min())/dist.min():.2f}")
