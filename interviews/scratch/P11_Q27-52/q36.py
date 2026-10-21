import numpy as np
rng = np.random.default_rng(0)
true_ctr = np.array([0.04, 0.05, 0.08])        # 3 candidate items (illustrative)
a = np.ones(3); b = np.ones(3)                  # Beta(1,1) priors
clicks = 0
for t in range(5000):
    arm = np.argmax(rng.beta(a, b))             # sample a belief per arm, pick the best sample
    r = rng.random() < true_ctr[arm]
    a[arm] += r; b[arm] += 1 - r; clicks += r
print("pulls per arm:", (a + b - 2).astype(int), "total CTR:", round(clicks / 5000, 4))
