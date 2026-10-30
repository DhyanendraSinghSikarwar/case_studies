# Q45: two overlapping experiments with an interaction (illustrative simulation)
import numpy as np
from scipy import stats
rng = np.random.default_rng(45)
N = 400_000
a = rng.random(N) < 0.5            # experiment A: carousel algorithm
b = rng.random(N) < 0.5            # experiment B: carousel layout (independent hash)
print("share in each cell (A,B):", {k: round(float(np.mean((a == k[0]) & (b == k[1]))), 3) for k in [(0,0),(1,0),(0,1),(1,1)]})
assert abs(np.mean(a & b) - 0.25) < 0.005
# illustrative mean minutes per user: each change alone helps, together they clash
base, ea, eb, inter = 100.0, 3.0, 3.0, -8.0
mu = base + ea * a + eb * b + inter * (a & b)
y = mu + rng.normal(0, 40, N)
cell = {k: y[(a == k[0]) & (b == k[1])] for k in [(0,0),(1,0),(0,1),(1,1)]}
for k, v in cell.items(): print("cell", k, "mean", round(float(v.mean()), 2), "n", len(v))
assert cell[(1,1)].mean() < cell[(1,0)].mean() and cell[(1,1)].mean() < cell[(0,1)].mean()
# each experiment analysed alone (ignores the other, averages over it)
for name, g in [("A alone", a), ("B alone", b)]:
    d = y[g].mean() - y[~g].mean(); se = np.sqrt(y[g].var()/g.sum() + y[~g].var()/(~g).sum())
    print(name, "estimate", round(float(d), 2), "+/-", round(1.96*se, 2))
    assert abs(d - (ea + inter/2)) < 1.0          # a + half the interaction = 3 - 4 = -1
# 2x2 regression with interaction term
X = np.column_stack([np.ones(N), a, b, a & b]).astype(float)
beta, *_ = np.linalg.lstsq(X, y, rcond=None)
res = y - X @ beta; s2 = res @ res / (N - 4)
se = np.sqrt(np.diag(s2 * np.linalg.inv(X.T @ X)))
print("main A", round(beta[1], 2), "main B", round(beta[2], 2), "interaction", round(beta[3], 2), "SE int", round(se[3], 2), "SE A", round(se[1], 2))
assert abs(beta[3] - inter) < 4 * se[3] and abs(beta[3]/se[3]) > 5
se_marg = np.sqrt(y[a].var()/a.sum() + y[~a].var()/(~a).sum())
print("interaction SE / marginal main-effect SE:", round(se[3]/se_marg, 2))   # 2 with equal cells
assert 1.8 < se[3]/se_marg < 2.2
# how often is a smaller interaction (-2) detected at this size? power by simulation
def power(inter_true, n, reps=300):
    hit = 0
    for _ in range(reps):
        a_ = rng.random(n) < .5; b_ = rng.random(n) < .5
        y_ = 100 + 3*a_ + 3*b_ + inter_true*(a_ & b_) + rng.normal(0, 40, n)
        X_ = np.column_stack([np.ones(n), a_, b_, a_ & b_]).astype(float)
        be, *_ = np.linalg.lstsq(X_, y_, rcond=None); r = y_ - X_@be
        s = np.sqrt((r@r/(n-4)) * np.linalg.inv(X_.T@X_)[3,3]); hit += abs(be[3]/s) > 1.96
    return hit/reps
p_small = power(-2.0, 20_000)
print("power to detect interaction -2 with 20,000 users:", p_small)
assert 0.25 < p_small < 0.6
