# Q44: informative missingness across sites. SYNTHETIC simulation (invented), plus the prompt's two AUCs.
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(11)

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def make(n, order_rate):
    sev = rng.normal(size=n)                                  # true latent severity
    y = (rng.random(n) < 1 / (1 + np.exp(-(1.6 * sev - 3.0)))).astype(int)   # deterioration
    vit = sev + rng.normal(0, 1.5, n)                         # vitals-based signal, always present
    worry = sev + rng.normal(0, 0.7, n)                       # clinician worry
    thr = np.quantile(worry, 1 - order_rate)
    ordered = (worry > thr).astype(float)
    lact = (sev + rng.normal(0, 0.5, n)) * ordered            # value only if ordered
    return y, np.c_[vit, ordered, lact]

def fit(X, y, it=30):
    X1 = np.c_[np.ones(len(X)), X]; b = np.zeros(X1.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-X1 @ b)); W = p * (1 - p)
        b += np.linalg.solve(X1.T @ (X1 * W[:, None]) + 1e-6 * np.eye(len(b)), X1.T @ (y - p))
    return b
def score(b, X): return np.c_[np.ones(len(X)), X] @ b

N = 200_000
yA, XA = make(N, 0.60); yA2, XA2 = make(N, 0.60); yB, XB = make(N, 0.20)
print("ordering rate A / B:", XA[:, 1].mean().round(2), XB[:, 1].mean().round(2))
assert abs(XA[:, 1].mean() - 0.6) < 0.01 and abs(XB[:, 1].mean() - 0.2) < 0.01
b = fit(XA, yA)
a_a, a_b = auc(yA2, score(b, XA2)), auc(yB, score(b, XB))
print("model trained at A: AUC at A", round(a_a, 3), " AUC at B", round(a_b, 3), " (prompt: 0.85 vs 0.74, measured, different patients)")
assert a_a > a_b
# retrain at B, or drop the ordering-driven lactate features: what does each buy?
yB1, XB1 = make(N, 0.20); yB2, XB2 = make(N, 0.20)
bB = fit(XB1, yB1)
print("trained at B, AUC at B:", round(auc(yB2, score(bB, XB2)), 3))
bV = fit(XA[:, :1], yA)
print("vitals only (no lactate feature) at A / at B:", round(auc(yA2, score(bV, XA2[:, :1])), 3), round(auc(yB, score(bV, XB[:, :1])), 3))
assert abs(auc(yA2, score(bV, XA2[:, :1])) - auc(yB, score(bV, XB[:, :1]))) < 0.02   # stable but weaker
print("lactate only when ordered; AUC among ordered at B:", round(auc(yB[XB[:, 1] == 1], score(b, XB[XB[:, 1] == 1])), 3),
      " among not ordered:", round(auc(yB[XB[:, 1] == 0], score(b, XB[XB[:, 1] == 0])), 3))
