# Q14: reject inference / selection bias (illustrative simulation)
import numpy as np
rng = np.random.default_rng(14)
def sig(z): return 1 / (1 + np.exp(-z))
def fit_logit(X, y, it=30):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (y - p))
    return w
def auc(s, y):
    from scipy.stats import rankdata
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

N = 100_000
risk = rng.normal(size=N)                  # higher = riskier applicant (bureau-style score, standardised)
true_logit = -3.6 + 0.8 * risk + 0.9 * np.maximum(risk, 0) ** 2   # risk climbs faster in the tail
default = rng.random(N) < sig(true_logit)
# old policy: approve the 60,000 lowest-risk applicants (rank cut)
order = np.argsort(risk); approved = np.zeros(N, bool); approved[order[:60_000]] = True
print("approved", approved.sum(), "rejected", (~approved).sum())
assert approved.sum() == 60_000 and (~approved).sum() == 40_000
print(f"default rate: approved {default[approved].mean():.2%}   rejected (unseen by the lender) {default[~approved].mean():.2%}")
X = np.c_[np.ones(N), risk, risk ** 2]   # a flexible-enough logit: intercept, risk, risk squared
w = fit_logit(X[approved], default[approved].astype(float))
pred = sig(X @ w)
print(f"approved-only model: AUC on approved {auc(pred[approved], default[approved].astype(int)):.3f}")
# new policy approves the next 25,000 lowest-risk applicants (ranks 60,000 to 85,000)
band = np.zeros(N, bool); band[order[60_000:85_000]] = True
print(f"new band: predicted default {pred[band].mean():.2%}  actual {default[band].mean():.2%}")
assert default[band].mean() > 1.3 * pred[band].mean()
# worst slice: the riskiest 5,000 of the rejected
tail = np.zeros(N, bool); tail[order[-5_000:]] = True
print(f"riskiest 5,000: predicted {pred[tail].mean():.2%}  actual {default[tail].mean():.2%}")
# fix 1: exploration: approve a random 3% of rejected applicants and observe them (1,200 loans)
rej_idx = np.flatnonzero(~approved)
explore = rng.choice(rej_idx, 1_200, replace=False)
print("exploration sample:", len(explore), "loans =", f"{len(explore) / 40_000:.0%} of rejected")
assert len(explore) == 1_200
# reweight the exploration rows by inverse sampling probability (1 / 0.03) and refit on approved + explored
use = np.r_[np.flatnonzero(approved), explore]
wt = np.r_[np.ones(60_000), np.full(len(explore), 40_000 / 1_200)]
w2 = np.zeros(3)
for _ in range(30):
    p = sig(X[use] @ w2); H = (X[use] * (wt * p * (1 - p))[:, None]).T @ X[use] + 1e-6 * np.eye(3)
    w2 += np.linalg.solve(H, X[use].T @ (wt * (default[use] - p)))
pred2 = sig(X @ w2)
print(f"with weighted exploration: new band predicted {pred2[band].mean():.2%}  actual {default[band].mean():.2%}; riskiest 5,000 predicted {pred2[tail].mean():.2%}")
err_old = abs(pred[tail].mean() - default[tail].mean()); err_new = abs(pred2[tail].mean() - default[tail].mean())
print(f"tail error (percentage points): approved-only {err_old * 100:.1f}  with exploration {err_new * 100:.1f}")
assert err_new < err_old
