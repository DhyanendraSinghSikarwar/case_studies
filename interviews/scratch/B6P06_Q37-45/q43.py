# Q43: is "2 AUC points better" proven, and what does it buy? (simulated, illustrative)
import numpy as np
rng = np.random.default_rng(43)
n, prev = 20_000, 0.10
y = (rng.random(n) < prev).astype(int)
def auc(y, s):
    r = s.argsort().argsort() + 1.0
    npos = y.sum(); nneg = len(y) - npos
    return (r[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg)
shared = rng.normal(size=n)
old = 1.04 * y + 0.9 * shared + np.sqrt(0.19) * rng.normal(size=n)   # about 0.77
new = 1.17 * y + 0.9 * shared + np.sqrt(0.19) * rng.normal(size=n)   # about 0.80
a_old, a_new = auc(y, old), auc(y, new)
diffs = []
for _ in range(500):
    i = rng.integers(0, n, n)
    diffs.append(auc(y[i], new[i]) - auc(y[i], old[i]))
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"old AUC {a_old:.3f}, new AUC {a_new:.3f}, gap {a_new-a_old:.3f}, 95% CI [{lo:.3f}, {hi:.3f}]")
assert 0.015 < a_new - a_old < 0.05 and lo > 0
# business translation: positives caught when the team reviews the top 10% of scores
k = int(0.10 * n)
def caught(s): return int(y[np.argsort(-s)[:k]].sum())
c_old, c_new = caught(old), caught(new)
print(f"positives total {int(y.sum())}; caught in top 10%: old {c_old}, new {c_new}, extra {c_new-c_old}")
assert c_new > c_old
# a 0.02 AUC claim only holds up if the interval is clear of zero and the extra catches matter
