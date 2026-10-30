import numpy as np
from scipy import stats
rng = np.random.default_rng(9)

rho = 0.7
print("variance after CUPED = (1 - rho^2) =", round(1 - rho ** 2, 2), "-> sample size needed:", int(100_000 * (1 - rho ** 2)), "per arm")
assert round(1 - rho ** 2, 2) == 0.51
assert int(100_000 * (1 - rho ** 2)) == 51_000
print("claim '70% fewer users' would mean 30,000 per arm; the formula says 51,000")

# Simulate: pre-period spend X, in-period spend Y with correlation 0.7, treatment effect +0.5
n = 200_000
cov = [[1.0, rho], [rho, 1.0]]
xy = rng.multivariate_normal([0, 0], cov, n)
x = xy[:, 0] * 20 + 100            # pre-experiment spend
y = xy[:, 1] * 20 + 100            # in-experiment spend (control behaviour)
treat = rng.random(n) < 0.5
y = y + 0.5 * treat                # true effect +0.5

# CUPED: theta from pooled data, adjust Y
theta = np.cov(x, y)[0, 1] / x.var(ddof=1)
y_adj = y - theta * (x - x.mean())
print(f"theta = {theta:.3f} (expected {rho:.3f})")
var_ratio = y_adj.var(ddof=1) / y.var(ddof=1)
print(f"variance ratio after / before = {var_ratio:.3f}")
assert abs(var_ratio - 0.51) < 0.02

def effect(v):
    d = v[treat].mean() - v[~treat].mean()
    se = np.sqrt(v[treat].var(ddof=1) / treat.sum() + v[~treat].var(ddof=1) / (~treat).sum())
    return d, se
d0, se0 = effect(y); d1, se1 = effect(y_adj)
print(f"raw: effect {d0:.3f} se {se0:.3f} | CUPED: effect {d1:.3f} se {se1:.3f}")
print(f"se ratio = {se1/se0:.3f} (sqrt of 0.51 = {np.sqrt(0.51):.3f})")
assert abs(se1 / se0 - np.sqrt(0.51)) < 0.02
print(f"sample size ratio (se ratio squared) = {(se1/se0)**2:.3f}")

# Bad covariate: a post-treatment variable (e.g. in-experiment sessions affected by treatment) biases the effect
m = 0.8 * (y - 100) / 20 + 0.6 * treat + rng.standard_normal(n) * 0.5     # moves with treatment
th = np.cov(m, y)[0, 1] / m.var(ddof=1)
y_bad = y - th * (m - m.mean())
db, _ = effect(y_bad)
print(f"post-treatment covariate: estimated effect = {db:.3f} (true 0.5)")
assert abs(db - 0.5) > 0.3
