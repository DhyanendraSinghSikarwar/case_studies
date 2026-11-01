# Q38: are AUC 0.82 and 0.83 distinguishable on ONE shared test set? (simulated, illustrative)
import numpy as np
rng = np.random.default_rng(38)
n, prev = 5000, 0.10
y = (rng.random(n) < prev).astype(int)

def auc(y, s):
    r = s.argsort().argsort() + 1.0
    npos = y.sum(); nneg = len(y) - npos
    return (r[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg)

# two correlated models (share a latent signal), A a bit weaker than B
shared = rng.normal(size=n)                       # noise both models see
a = 1.38 * y + 0.9 * shared + np.sqrt(1 - 0.81) * rng.normal(size=n)
b = 1.43 * y + 0.9 * shared + np.sqrt(1 - 0.81) * rng.normal(size=n)
auc_a, auc_b = auc(y, a), auc(y, b)
diffs = []
idx_all = np.arange(n)
for _ in range(1000):
    i = rng.choice(idx_all, n)
    if y[i].sum() in (0, n): continue
    diffs.append(auc(y[i], b[i]) - auc(y[i], a[i]))
lo, hi = np.percentile(diffs, [2.5, 97.5])
print(f"positives in test set = {int(y.sum())}")
print(f"AUC A = {auc_a:.3f}, AUC B = {auc_b:.3f}, observed gap = {auc_b-auc_a:.3f}")
print(f"paired bootstrap 95% CI for gap = [{lo:.3f}, {hi:.3f}]")
assert y.sum() > 400
assert 0 < auc_b - auc_a < 0.03
assert (hi - lo) > 0.005       # interval has real width
print("CI includes 0:", lo <= 0 <= hi)
