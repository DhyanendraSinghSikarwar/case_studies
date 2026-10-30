import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(30)

def sigmoid(z): return 1 / (1 + np.exp(-z))
def fit(X, y, it=25):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(it):
        p = sigmoid(Xb @ w); W = p * (1 - p)
        w += np.linalg.solve(Xb.T @ (Xb * W[:, None]) + 1e-6 * np.eye(len(w)), Xb.T @ (y - p))
    cov = np.linalg.inv(Xb.T @ (Xb * (sigmoid(Xb @ w) * (1 - sigmoid(Xb @ w)))[:, None]))
    return w, np.sqrt(np.diag(cov))
def pred(w, X): return sigmoid(np.c_[np.ones(len(X)), X] @ w)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def decile_lift(y, s):
    top = s >= np.quantile(s, 0.9)
    return y[top].mean() / y.mean()

def make(n, usage_slope, intercept):
    usage = rng.normal(0, 1, n); tenure = rng.normal(0, 1, n)
    p = sigmoid(intercept + usage_slope * usage - 0.3 * tenure)
    return np.c_[usage, tenure], (rng.random(n) < p).astype(float)

# Before price change: churn falls with usage (slope -1.0). After: the same usage no longer protects (slope -0.2), base level higher.
Xa, ya = make(40000, -1.0, -1.5)
Xb, yb = make(40000, -0.2, -1.0)           # input distribution identical, relationship changed
Xt, yt = make(40000, -0.2, -1.0)           # fresh post-change test data

wA, seA = fit(Xa, ya); wB, seB = fit(Xb, yb)
print("coefficient on usage: before", round(wA[1], 2), "+/-", round(1.96 * seA[1], 2), "| after", round(wB[1], 2), "+/-", round(1.96 * seB[1], 2))
assert abs(wA[1] - wB[1]) > 4 * np.hypot(seA[1], seB[1])           # difference far outside noise

# Data-drift check: the input means and sds barely move
print("input mean/sd before:", Xa.mean(0).round(2), Xa.std(0).round(2), "after:", Xb.mean(0).round(2), Xb.std(0).round(2))
assert np.abs(Xa.mean(0) - Xb.mean(0)).max() < 0.03 and np.abs(Xa.std(0) - Xb.std(0)).max() < 0.03

print(f"old model on old-regime test data: AUC {auc(ya, pred(wA, Xa)):.3f}, top-decile lift {decile_lift(ya, pred(wA, Xa)):.2f}")
print(f"old model on new-regime test data: AUC {auc(yt, pred(wA, Xt)):.3f}, top-decile lift {decile_lift(yt, pred(wA, Xt)):.2f}")
print(f"refit on new regime, same test:    AUC {auc(yt, pred(wB, Xt)):.3f}, top-decile lift {decile_lift(yt, pred(wB, Xt)):.2f}")
assert auc(yt, pred(wA, Xt)) < auc(yt, pred(wB, Xt)) - 0.02
assert decile_lift(yt, pred(wA, Xt)) < decile_lift(yt, pred(wB, Xt))

# Training-window trade-off: only 3,000 post-change rows exist; combine with old data plus a regime flag
Xn, yn = Xb[:3000], yb[:3000]
w_small, _ = fit(Xn, yn)
Xmix = np.r_[Xa[:20000], Xn]; flag = np.r_[np.zeros(20000), np.ones(3000)]
Xi = np.c_[Xmix, flag, Xmix[:, 0] * flag]
w_int, _ = fit(Xi, np.r_[ya[:20000], yn])
Xti = np.c_[Xt, np.ones(len(Xt)), Xt[:, 0]]
print(f"3,000 new rows only:               AUC {auc(yt, pred(w_small, Xt)):.3f}")
print(f"old 20,000 + new 3,000 + regime x usage: AUC {auc(yt, pred(w_int, Xti)):.3f}")
assert auc(yt, pred(w_small, Xt)) > auc(yt, pred(wA, Xt))
print("asserts passed")
