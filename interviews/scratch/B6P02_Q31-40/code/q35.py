# Q35: a feature that exists only after the outcome leaks offline and is empty live (illustrative simulation)
import numpy as np
import pandas as pd
from scipy.stats import rankdata

rng = np.random.default_rng(35)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit_logit(X, y, l2=1e-3, steps=40):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = 1 / (1 + np.exp(-Xb @ w)); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w
def score(w, X): return np.c_[np.ones(len(X)), X] @ w

N = 60_000
legit = rng.normal(size=(N, 3))
y = (legit @ np.array([0.9, 0.6, 0.4]) + rng.normal(0, 2.4, N) > 1.5).astype(int)
# leaky feature: written by the process that happens AFTER the outcome (e.g. a 'case closed' amount)
leak = y * rng.normal(1.0, 0.42, N) + (1 - y) * rng.normal(0.0, 0.42, N)
train, test = slice(0, 40_000), slice(40_000, N)

# 1. Offline with the leaky feature
X_all = np.c_[legit, leak]
w_all = fit_logit(X_all[train], y[train])
offline = auc(y[test], score(w_all, X_all[test]))
# 2. Live: the feature is empty (filled with 0 by the pipeline)
X_live = np.c_[legit, np.zeros(N)]
live = auc(y[test], score(w_all, X_live[test]))
# 3. Clean model, no leaky feature
w_cl = fit_logit(legit[train], y[train])
clean = auc(y[test], score(w_cl, legit[test]))
print(f"offline AUC (with leak) {offline:.3f}   live-like AUC (feature empty) {live:.3f}   clean model {clean:.3f}")
assert offline > 0.93 and 0.68 < live < 0.80 and clean > live - 0.02

# Confirm leakage: single-feature AUC, and ablation
print(f"single-feature AUC: leak {auc(y, leak):.3f}   best legit {max(auc(y, legit[:, j]) for j in range(3)):.3f}")
print(f"ablation: dropping the leaky feature changes offline AUC by {clean - offline:+.3f}")
assert auc(y, leak) > 0.85 and clean < offline - 0.15

# Time check: share of rows whose feature timestamp is after the prediction time
t_pred = rng.uniform(0, 100, N)
t_feat = np.where(rng.random(N) < 0.98, t_pred + rng.uniform(0.1, 5, N), t_pred - 1)   # 98% written later
after = (t_feat > t_pred).mean()
print(f"rows where the feature is written after the prediction time: {after:.1%}")
assert after > 0.97

# Point-in-time (as-of) join versus the leaky 'latest value' join
events = pd.DataFrame({"user": [1, 1, 1, 2, 2], "ts": [10, 20, 30, 15, 25], "val": [100, 200, 300, 50, 60]})
labels = pd.DataFrame({"user": [1, 2], "ts": [22, 20]})                       # prediction times
latest = events.sort_values("ts").groupby("user")["val"].last()               # leaky
asof = pd.merge_asof(labels.sort_values("ts"), events.sort_values("ts"), on="ts", by="user")
print("latest-value join:", latest.to_dict(), "  as-of join:", dict(zip(asof.user, asof.val)))
assert latest.to_dict() == {1: 300, 2: 60} and dict(zip(asof.user, asof.val)) == {1: 200, 2: 50}

# Live handling: the old leaky model's scores shift when the feature is empty
s_off = 1 / (1 + np.exp(-score(w_all, X_all[test]))); s_live = 1 / (1 + np.exp(-score(w_all, X_live[test])))
print(f"mean predicted risk offline {s_off.mean():.3f} vs live-like {s_live.mean():.3f}; true rate {y[test].mean():.3f}")
assert s_live.mean() < 0.5 * s_off.mean()
# decisions at the old threshold of 0.5: how many cases get flagged, and how many true cases are found
for name, s_ in (("offline", s_off), ("live-like", s_live)):
    f = s_ > 0.5
    print(f"{name:10} flagged {f.mean():.1%}  recall {(f & (y[test] == 1)).sum() / y[test].sum():.1%}")
assert (s_live > 0.5).mean() < 0.3 * (s_off > 0.5).mean()
