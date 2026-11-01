# Q13: selection bias in a loan model (illustrative simulation, seeded, numpy+scipy)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(13)
sig = lambda z: 1 / (1 + np.exp(-z))

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def fit_logit(X, y, it=30):
    X1 = np.c_[np.ones(len(X)), X]; b = np.zeros(X1.shape[1])
    for _ in range(it):
        p = sig(X1 @ b); W = p * (1 - p)
        b += np.linalg.solve(X1.T @ (X1 * W[:, None]) + 1e-9 * np.eye(len(b)), X1.T @ (y - p))
    return b
pred = lambda b, X: sig(np.c_[np.ones(len(X)), X] @ b)

# x = credit-quality score (higher = safer). True default risk rises sharply (non-linearly) at low x.
N = 400_000
x = rng.normal(0, 1, N)
true_logit = -3.0 - 1.5 * x + 0.5 * np.maximum(0, -x - 0.3) ** 2
pd_true = sig(true_logit)
default = (rng.random(N) < pd_true).astype(int)

# Old policy: approve only if x > -0.3 (about 62% approved). Outcomes exist only for approved.
approved = x > -0.3
print(f"approval rate {approved.mean():.3f}; default rate among approved {default[approved].mean():.3f}; "
      f"true default rate among ALL applicants {default.mean():.3f}")
assert default[approved].mean() < default.mean()

b = fit_logit(x[approved, None], default[approved])
p_hat = pred(b, x[:, None])
print(f"approved book: mean predicted PD {p_hat[approved].mean():.3f} vs observed {default[approved].mean():.3f} (looks calibrated)")
assert abs(p_hat[approved].mean() - default[approved].mean()) < 0.01
print(f"AUC on approved (what monitoring sees) = {auc(default[approved], p_hat[approved]):.3f}")
print(f"AUC on the rejected region (unobserved)  = {auc(default[~approved], p_hat[~approved]):.3f}")

# Calibration in the unseen region: x in bins below the cut
edges = [-3.5, -2.0, -1.2, -0.7, -0.3]
print("x-bin            n   mean predicted PD   true PD")
for lo, hi in zip(edges[:-1], edges[1:]):
    m = (x >= lo) & (x < hi)
    print(f"[{lo:5.1f},{hi:5.1f})  {m.sum():6d}   {p_hat[m].mean():.3f}               {default[m].mean():.3f}")
m_low = (x >= -2.0) & (x < -1.2)
assert p_hat[m_low].mean() < default[m_low].mean() - 0.10   # model badly under-predicts in the unseen region

# Option: random-approval exploration slice among would-be rejects
n_target = 1000
half_width = 1.96 * np.sqrt(0.30 * 0.70 / n_target)
print(f"exploration slice of {n_target} loans: 95% half-width on a ~30% default rate = +/-{100*half_width:.1f} points")
assert 0.027 < half_width < 0.030
rejected_idx = np.flatnonzero(~approved)
pick = rng.choice(rejected_idx, n_target, replace=False)
est = default[pick].mean()
print(f"measured default rate in explored slice = {est:.3f} (true default rate among rejects = {default[~approved].mean():.3f})")
loan, lgd = 100_000, 0.6                      # Rs 1 lakh loan, 60% loss given default (illustrative)
cost = default[pick].sum() * loan * lgd
print(f"expected exploration cost (losses only, ignoring interest earned) = Rs {cost/1e5:.1f} lakh")
small = default[pick].sum() * 10_000 * lgd
print(f"same slice with a Rs 10,000 loan cap: Rs {small/1e5:.1f} lakh")
assert abs(small * 10 - cost) < 1e-6
share = n_target / (~approved).sum()
print(f"slice is {100*share:.2f}% of rejected applicants ({(~approved).sum()} rejects)")

# Option: naive reject inference (label every reject with the model's own prediction) just echoes the model
y_aug = np.r_[default[approved], (p_hat[~approved] > 0.5).astype(int)]
X_aug = np.r_[x[approved], x[~approved]][:, None]
b2 = fit_logit(X_aug, y_aug)
low2 = pred(b2, x[:, None])[m_low].mean()
print(f"naive reject-inference refit: mean PD in the unseen bin = {low2:.3f} vs true {default[m_low].mean():.3f}")
assert low2 < default[m_low].mean() - 0.05    # still under-predicts: it learned nothing new
# Option: refit using explored slice (inverse-probability weight each explored reject)
w_each = (~approved).sum() / n_target
Xe = np.r_[x[approved], x[pick]][:, None]; ye = np.r_[default[approved], default[pick]]
we = np.r_[np.ones(approved.sum()), np.full(n_target, w_each)]
# weighted Newton
X1 = np.c_[np.ones(len(Xe)), Xe]; b3 = np.zeros(2)
for _ in range(40):
    p = sig(X1 @ b3); W = we * p * (1 - p)
    b3 += np.linalg.solve(X1.T @ (X1 * W[:, None]) + 1e-9 * np.eye(2), X1.T @ (we * (ye - p)))
low3 = pred(b3, x[:, None])[m_low].mean()
print(f"refit with weighted exploration slice: mean PD in the unseen bin = {low3:.3f} vs true {default[m_low].mean():.3f}")
assert abs(low3 - default[m_low].mean()) < abs(low2 - default[m_low].mean())
