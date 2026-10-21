import numpy as np
rng = np.random.default_rng(0)
h = rng.normal(170, 10, 500); w = 0.5*h + rng.normal(0, 5, 500)
print(np.cov(h, w)[0,1].round(2), np.corrcoef(h, w)[0,1].round(3))          # 47.7  0.707
print(np.cov(h/100, w)[0,1].round(3), np.corrcoef(h/100, w)[0,1].round(3))  # 0.477 0.707
