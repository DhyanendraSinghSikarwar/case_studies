# Q14: calibration decay with stable AUC (illustrative, seeded, numpy+scipy)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(14)
sig = lambda z: 1 / (1 + np.exp(-z))
logit = lambda p: np.log(p / (1 - p))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

# Hand-check: ratio and gap
pred_mean, obs = 0.10, 0.14
print(f"observed/predicted = {obs/pred_mean:.2f}, gap = {100*(obs-pred_mean):.0f} points")
assert abs(obs / pred_mean - 1.4) < 1e-12

# Build matured data: the model's logit is offset by -0.46 relative to the truth, ranking untouched
N = 200_000
z = rng.normal(0, 1.0, N)                         # latent signal
y = (rng.random(N) < sig(-2.40 + 1.4 * z)).astype(int)
p_model = sig(-2.86 + 1.4 * z)                    # model under-predicts after drift in base rate
print(f"mean predicted {p_model.mean():.3f}, observed positive rate {y.mean():.3f}, AUC {auc(y, p_model):.3f}")
assert abs(p_model.mean() - 0.10) < 0.01 and abs(y.mean() - 0.14) < 0.01

def ece(y, p, bins=10):
    edges = np.quantile(p, np.linspace(0, 1, bins + 1)); edges[-1] += 1e-9
    idx = np.digitize(p, edges[1:-1]); tot = 0
    for b in range(bins):
        m = idx == b
        tot += m.mean() * abs(y[m].mean() - p[m].mean())
    return tot

# Split matured data: fit fixes on first half, judge on second half
h = N // 2
ytr, ptr, yte, pte = y[:h], p_model[:h], y[h:], p_model[h:]

def fit_platt(y, p, it=30):
    x = logit(p); X = np.c_[np.ones(len(x)), x]; b = np.array([0., 1.])
    for _ in range(it):
        q = sig(X @ b); W = q * (1 - q)
        b += np.linalg.solve(X.T @ (X * W[:, None]), X.T @ (y - q))
    return b
b = fit_platt(ytr, ptr)
p_recal = sig(b[0] + b[1] * logit(pte))
print(f"Platt fit: intercept {b[0]:+.3f}, slope {b[1]:.3f}")
print(f"ECE before {ece(yte, pte):.4f} -> after recalibration {ece(yte, p_recal):.4f}; AUC {auc(yte, pte):.4f} -> {auc(yte, p_recal):.4f}")
assert ece(yte, p_recal) < ece(yte, pte) / 3
assert abs(auc(yte, pte) - auc(yte, p_recal)) < 1e-9      # monotone map leaves AUC unchanged

def prf(y, flag):
    tp = (flag & (y == 1)).sum()
    return tp / max(flag.sum(), 1), tp / y.sum(), flag.mean()
pr, rc, fr = prf(yte, pte >= 0.5)
print(f"fixed 0.5 on old scores: precision {pr:.3f}, recall {rc:.3f}, flagged {fr:.3f}")
pr2, rc2, fr2 = prf(yte, p_recal >= 0.5)
print(f"fixed 0.5 on recalibrated scores: precision {pr2:.3f}, recall {rc2:.3f}, flagged {fr2:.3f}")
# Threshold from a business rule: review capacity = flag the top 10% by score (rank-based, immune to calibration shift)
k = np.quantile(pte, 0.90)
pr3, rc3, fr3 = prf(yte, pte >= k)
print(f"top-10% capacity rule: precision {pr3:.3f}, recall {rc3:.3f}, flagged {fr3:.3f}")
# Cost-based threshold: a missed positive costs 5, a false alarm costs 1 -> flag if p >= 1/6 on CALIBRATED scores
t = 1 / (1 + 5)
pr4, rc4, fr4 = prf(yte, p_recal >= t)
pr5, rc5, fr5 = prf(yte, pte >= t)
print(f"cost threshold p>={t:.3f}: recalibrated flagged {fr4:.3f} recall {rc4:.3f}; uncalibrated flagged {fr5:.3f} recall {rc5:.3f}")
assert rc4 > rc5 and rc2 > rc

# How much matured data per weekly check to see a 1.4x ratio? Standard error of observed rate
for n in (200, 500, 2000):
    se = np.sqrt(0.14 * 0.86 / n)
    print(f"n={n:6d}: observed 0.14 +/- {1.96*se:.4f} (95%), excludes 0.10: {bool(0.14 - 1.96*se > 0.10)}")
assert not (0.14 - 1.96 * np.sqrt(0.14 * 0.86 / 200) > 0.10)
assert 0.14 - 1.96 * np.sqrt(0.14 * 0.86 / 500) > 0.10
