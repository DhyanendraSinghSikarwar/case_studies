# Q9 random split vs time split on a drifting churn problem (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(13)
def sig(x): return 1 / (1 + np.exp(-x))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(A, y, iters=25):
    b = np.zeros(A.shape[1])
    for _ in range(iters):
        p = sig(A @ b); g = A.T @ (p - y); H = (A * (p * (1 - p))[:, None]).T @ A + 1e-6 * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    return b

per_month = 6_000
def month_data(m):
    """Month m = 1..15. The effect of each feature drifts slowly."""
    X = rng.normal(size=(per_month, 4))
    t = (m - 1) / 14
    coef = np.array([1.6 - 1.4 * t, 0.2 + 1.4 * t, 0.8, 0.0])        # driver 1 fades, driver 2 grows
    y = (rng.random(per_month) < sig(-1.6 + X @ coef)).astype(float)
    return np.full(per_month, m), X, y

parts = [month_data(m) for m in range(1, 16)]
M = np.concatenate([p[0] for p in parts]); X = np.vstack([p[1] for p in parts]); y = np.concatenate([p[2] for p in parts])
A = np.c_[np.ones(len(y)), X]

hist = M <= 12; future = M >= 13                                      # months 13-15 play the role of 'after launch'
Ah, yh, Mh = A[hist], y[hist], M[hist]

# (a) random split of the 12 months, 25% test
idx = rng.permutation(len(yh)); cut = int(0.75 * len(yh))
b_rand = fit(Ah[idx[:cut]], yh[idx[:cut]])
a_rand = auc(yh[idx[cut:]], Ah[idx[cut:]] @ b_rand)
# (b) time split: train months 1-9, test months 10-12
tr = Mh <= 9; te = Mh >= 10
b_time = fit(Ah[tr], yh[tr]); a_time = auc(yh[te], Ah[te] @ b_time)
print(f"random split AUC={a_rand:.3f}   time split (train 1-9, test 10-12) AUC={a_time:.3f}")
# (c) what really happens after launch: train on all 12 months, score months 13-15
b_all = fit(Ah, yh); a_fut = auc(y[future], A[future] @ b_all)
print(f"after launch (train 1-12, score months 13-15) AUC={a_fut:.3f}")
assert a_rand > a_time + 0.015
assert abs(a_fut - a_time) < abs(a_fut - a_rand)       # the time split predicts the future better than the random split

# (d) rolling-origin validation: train on months 1..k, test on k+1..k+3
rows = []
for k in (6, 7, 8, 9):
    t1 = Mh <= k; t2 = (Mh > k) & (Mh <= k + 3)
    rows.append(auc(yh[t2], Ah[t2] @ fit(Ah[t1], yh[t1])))
print("rolling-origin AUCs (train 1..k, test k+1..k+3, k=6..9):", " ".join(f"{a:.3f}" for a in rows), f" mean={np.mean(rows):.3f}")
assert max(rows) < a_rand
# test-set size is not the point: a bigger random test set stays optimistic
idx2 = rng.permutation(len(yh)); cut2 = int(0.5 * len(yh))
a_rand50 = auc(yh[idx2[cut2:]], Ah[idx2[cut2:]] @ fit(Ah[idx2[:cut2]], yh[idx2[:cut2]]))
print(f"random split with a 50% test set: AUC={a_rand50:.3f}")
assert a_rand50 > a_time + 0.015
