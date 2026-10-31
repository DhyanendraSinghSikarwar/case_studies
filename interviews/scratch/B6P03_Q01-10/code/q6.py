# Q6 class weight 99 at a 1% positive rate: scores become "weighted probabilities" (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(9)
def sig(x): return 1 / (1 + np.exp(-x))
def make(n, rng, coef=(0.4, 0.3, 0.2), icpt=-4.6):
    X = rng.normal(size=(n, 3))
    logit = icpt + X @ np.array(coef)
    return X, (rng.random(n) < sig(logit)).astype(float)
Xtr, ytr = make(300_000, rng); Xva, yva = make(200_000, rng)
print(f"train positive rate={ytr.mean():.4f}, validation positive rate={yva.mean():.4f}")
assert 0.008 < ytr.mean() < 0.013

def fit(X, y, w, iters=30):                        # weighted logistic regression by Newton steps
    A = np.c_[np.ones(len(X)), X]; b = np.zeros(A.shape[1])
    for _ in range(iters):
        p = sig(A @ b); g = A.T @ (w * (p - y)); H = (A * (w * p * (1 - p))[:, None]).T @ A
        b -= np.linalg.solve(H, g)
    return b
def predict(b, X): return sig(np.c_[np.ones(len(X)), X] @ b)
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def logloss(y, p): return -np.mean(y * np.log(p) + (1 - y) * np.log(1 - p))

W = 99.0
b_plain = fit(Xtr, ytr, np.ones(len(ytr)))
b_w = fit(Xtr, ytr, np.where(ytr == 1, W, 1.0))
p_plain, p_w = predict(b_plain, Xva), predict(b_w, Xva)
print(f"mean predicted: unweighted={p_plain.mean():.4f}  weight-99={p_w.mean():.4f}  true rate={yva.mean():.4f}")
assert abs(p_plain.mean() - yva.mean()) < 0.002 and 0.4 < p_w.mean() < 0.6

# Why 0.50: the weight 99 makes positives count as many as negatives (effective prevalence)
eff = 99 * 0.01 / (99 * 0.01 + 0.99)
print(f"effective prevalence under weight 99 = {eff:.2f}")
assert abs(eff - 0.5) < 1e-9

# Fix 1: undo the weight in odds space: odds_true = odds_weighted / W
p_fix = p_w / (p_w + W * (1 - p_w))
print(f"after prior correction: mean predicted={p_fix.mean():.4f}")
assert abs(p_fix.mean() - yva.mean()) < 0.003

# Ranking is untouched (monotone transform), probabilities are repaired
print(f"AUC: weighted={auc(yva, p_w):.4f}  corrected={auc(yva, p_fix):.4f}  unweighted={auc(yva, p_plain):.4f}")
assert abs(auc(yva, p_w) - auc(yva, p_fix)) < 1e-12
print(f"log-loss: weighted raw={logloss(yva, p_w):.4f}  corrected={logloss(yva, p_fix):.4f}  unweighted={logloss(yva, p_plain):.4f}")
assert logloss(yva, p_fix) < logloss(yva, p_w) and abs(logloss(yva, p_fix) - logloss(yva, p_plain)) < 0.005

# Check by decile: expected loss uses probabilities, so compare mean prediction with observed rate per decile
q = np.quantile(p_fix, np.linspace(0, 1, 11)); d = np.clip(np.searchsorted(q, p_fix, side="right") - 1, 0, 9)
print("decile: observed rate vs mean corrected prediction")
for k in (0, 5, 9):
    m = d == k; print(f"  decile {k}: observed={yva[m].mean():.4f} predicted={p_fix[m].mean():.4f}")
tot_exp = p_fix.sum(); tot_obs = yva.sum()
print(f"expected positives={tot_exp:.0f} vs observed={tot_obs:.0f}; raw weighted scores would imply {p_w.sum():.0f}")
assert abs(tot_exp - tot_obs) / tot_obs < 0.1 and p_w.sum() > 20 * tot_obs

# Side note: with a much stronger signal the weighted mean is lower than 0.50 but still far above 1%
Xs, ys = make(300_000, rng, (1.2, 0.8, 0.5), -5.6); Xsv, ysv = make(200_000, rng, (1.2, 0.8, 0.5), -5.6)
bs = fit(Xs, ys, np.where(ys == 1, W, 1.0)); ps = predict(bs, Xsv)
print(f"strong-signal model: true rate={ysv.mean():.4f}, mean weight-99 score={ps.mean():.4f}")
assert ps.mean() > 10 * ysv.mean()
