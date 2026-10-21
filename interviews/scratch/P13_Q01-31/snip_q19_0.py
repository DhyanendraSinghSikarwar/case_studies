import numpy as np
rng = np.random.default_rng(1)
v0, v1 = [], []
for _ in range(100000):
    s = rng.normal(0, 2, 5)              # true variance = 4
    v0.append(s.var(ddof=0)); v1.append(s.var(ddof=1))
v0, v1 = np.array(v0), np.array(v1)
print(v0.mean().round(3), v1.mean().round(3))                      # 3.189 3.987  -> bias of ddof=0
print(((v0 - 4)**2).mean().round(3), ((v1 - 4)**2).mean().round(3))   # MSE 5.795 vs 8.028
