# Q16: a feature computed wrongly for three weeks; contain, re-score, do not poison the retrain (illustrative, seeded)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(16)
sig = lambda z: 1 / (1 + np.exp(-z))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, it=25):
    X1 = np.c_[np.ones(len(X)), X]; b = np.zeros(X1.shape[1])
    for _ in range(it):
        p = sig(X1 @ b); W = p * (1 - p)
        b += np.linalg.solve(X1.T @ (X1 * W[:, None]) + 1e-6 * np.eye(len(b)), X1.T @ (y - p))
    return b
pred = lambda b, X: sig(np.c_[np.ones(len(X)), X] @ b)

# Volume arithmetic
days, total = 21, 600_000
per_day = total / days
print(f"{total:,} predictions over {days} days = {per_day:,.0f} per day")
assert round(per_day) == 28571

# Truth: f1 = recency (correct), f2 = spend. Bug: spend is scaled x3 (a unit-mix error) for 3 of the last 4 weeks.
def gen(n):
    f1, f2 = rng.normal(size=n), rng.normal(size=n)
    y = (rng.random(n) < sig(-1.0 + 1.0 * f1 + 1.2 * f2)).astype(int)
    return f1, f2, y
# Old model trained on clean history
f1h, f2h, yh = gen(100_000)
b_old = fit(np.c_[f1h, f2h], yh)

# Three weeks of live traffic (600,000 predictions) with the bug in f2
f1, f2, y = gen(total)
f2_bug = f2 * 3.0
s_live = pred(b_old, np.c_[f1, f2_bug]); s_true = pred(b_old, np.c_[f1, f2])
thr = 0.5
dec_live, dec_true = s_live >= thr, s_true >= thr
flip = dec_live != dec_true
print(f"approved/flagged live {dec_live.mean():.3f} vs with correct feature {dec_true.mean():.3f}")
print(f"decisions that change on re-score: {flip.sum():,} of {total:,} ({100*flip.mean():.1f}%)")
print(f"  flagged wrongly (live yes, true no): {(dec_live & ~dec_true).sum():,};  missed (live no, true yes): {(~dec_live & dec_true).sum():,}")
assert flip.sum() > 0 and flip.mean() < 0.5
print(f"AUC live {auc(y, s_live):.3f} vs corrected {auc(y, s_true):.3f}")
# Triage: only re-visit flipped decisions, ranked by how far the score moved
gap = np.abs(s_live - s_true)
rank = np.argsort(-(gap * flip))
top = rank[:10_000]
print(f"revisit queue: all flips {flip.sum():,}; first 10,000 by score gap cover {100*flip[top].sum()/flip.sum():.1f}% of flips, mean gap {gap[top].mean():.3f}")

# Training data: this month's table logged the buggy f2 for 21 of 28 days
frac_bad = 21 / 28
print(f"share of this month's training rows with the bad feature = {100*frac_bad:.0f}%")
assert abs(frac_bad - 0.75) < 1e-12
n_tr = 200_000
a1, a2, ay = gen(n_tr)
bad = rng.random(n_tr) < frac_bad
a2_logged = np.where(bad, a2 * 3.0, a2)
t1, t2, ty = gen(100_000)                         # clean holdout, correct feature
variants = {
  "retrain on logged (bug included)": fit(np.c_[a1, a2_logged], ay),
  "retrain on recomputed-from-raw":   fit(np.c_[a1, a2], ay),
  "retrain on clean rows only":       fit(np.c_[a1[~bad], a2_logged[~bad]], ay[~bad]),
}
res = {}
for k, b in variants.items():
    res[k] = auc(ty, pred(b, np.c_[t1, t2])); print(f"{k:36} AUC on clean holdout {res[k]:.4f}   coef spend {b[2]:.2f}")
print(f"old model on clean holdout                 AUC {auc(ty, pred(b_old, np.c_[t1, t2])):.4f}")
r = list(res.values())
assert r[1] >= r[0] and r[1] >= r[2] - 0.003
# a retrain on logged rows would also see a mixed-scale feature
assert abs(variants["retrain on logged (bug included)"][2] - variants["retrain on recomputed-from-raw"][2]) > 0.2
