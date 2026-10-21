import numpy as np
rng = np.random.default_rng(3)
# 3 stores x 2 SKUs: bottom-level forecasts, and an independently made store-level forecast
bottom = np.array([[10., 5.], [20., 8.], [6., 4.]])
top_store = np.array([14., 31., 9.])          # store-level model says more than sum of bottoms
print("bottom sums:", bottom.sum(1), "vs store model:", top_store)
# simple top-down proportional reconciliation using store-level total
prop = bottom / bottom.sum(1, keepdims=True)
recon = prop * top_store[:, None]
print("reconciled:\n", recon.round(2), "\nsums:", recon.sum(1))
