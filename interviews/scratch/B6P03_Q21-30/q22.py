# Q22 focal loss vs class weights vs plain cross-entropy (illustrative; a linear model stands in for the image model)
import numpy as np
from scipy.optimize import minimize
rng = np.random.default_rng(22)

# 1) What focal loss does to one example (gamma = 2)
gamma = 2.0
def ce(pt): return -np.log(pt)
def fl(pt, g=gamma): return -(1 - pt) ** g * np.log(pt)
easy_neg, hard_pos = 0.99, 0.10             # p_t = probability given to the true class
print(f"CE  easy negative {ce(easy_neg):.4f}, hard positive {ce(hard_pos):.4f}")
print(f"FL  easy negative {fl(easy_neg):.7f}, hard positive {fl(hard_pos):.4f}")
print(f"focal multiplier: easy negative {(1-easy_neg)**gamma:.4f}, hard positive {(1-hard_pos)**gamma:.2f}")
assert abs((1 - easy_neg) ** gamma - 1e-4) < 1e-12
assert abs((1 - hard_pos) ** gamma - 0.81) < 1e-12
# total loss contributed by 99,700 easy negatives versus 300 hard positives
neg_share_ce = 99_700 * ce(easy_neg) / (99_700 * ce(easy_neg) + 300 * ce(hard_pos))
neg_share_fl = 99_700 * fl(easy_neg) / (99_700 * fl(easy_neg) + 300 * fl(hard_pos))
print(f"share of total loss from the 99,700 easy negatives: CE {neg_share_ce:.1%}, FL {neg_share_fl:.2%}")
assert neg_share_ce > 0.55 and neg_share_fl < 0.01

# 2) Small experiment: 100,000 rows, 300 positives (0.3%), 5 features
n, npos = 100_000, 300
y = np.zeros(n, int); y[:npos] = 1
X = rng.normal(size=(n, 5)); X[y == 1] += 1.2
perm = rng.permutation(n); X, y = X[perm], y[perm]
tr = np.arange(n) < 70_000
Xtr, ytr, Xte, yte = X[tr], y[tr], X[~tr], y[~tr]
Xb = lambda A: np.hstack([A, np.ones((len(A), 1))])
sig = lambda z: 1 / (1 + np.exp(-np.clip(z, -30, 30)))

def make_obj(kind):
    def obj(w):
        z = Xb(Xtr) @ w; p = sig(z)
        if kind == "ce":
            wt = np.ones(len(ytr))
            L = -(ytr * np.log(p + 1e-12) + (1 - ytr) * np.log(1 - p + 1e-12))
            g = (p - ytr)
        elif kind == "weighted":
            wt = np.where(ytr == 1, 50.0, 1.0)
            L = -(ytr * np.log(p + 1e-12) + (1 - ytr) * np.log(1 - p + 1e-12)) * wt
            g = (p - ytr) * wt
        else:  # focal
            pt = np.where(ytr == 1, p, 1 - p); pt = np.clip(pt, 1e-12, 1 - 1e-12)
            L = -(1 - pt) ** gamma * np.log(pt)
            dL_dpt = gamma * (1 - pt) ** (gamma - 1) * np.log(pt) - (1 - pt) ** gamma / pt
            g = dL_dpt * pt * (1 - pt) * np.where(ytr == 1, 1, -1)
        return L.mean(), (Xb(Xtr).T @ g) / len(ytr)
    return obj

def ap(y, s):
    o = np.argsort(-s); yy = y[o]
    tp = np.cumsum(yy); prec = tp / np.arange(1, len(yy) + 1)
    return (prec * yy).sum() / yy.sum()

print(f"test rows {len(yte)}, positives {yte.sum()}, no-skill AP = base rate = {yte.mean():.4f}")
res = {}
for kind in ["ce", "weighted", "focal"]:
    w = minimize(make_obj(kind), np.zeros(6), jac=True, method="L-BFGS-B").x
    p = sig(Xb(Xte) @ w)
    res[kind] = (ap(yte, p), p.mean())
    print(f"{kind:9s} AP {res[kind][0]:.3f}   mean predicted prob {p.mean():.4f}   (true rate {yte.mean():.4f})")
# calibration claims
assert abs(res["ce"][1] - yte.mean()) < 0.001            # plain CE keeps probabilities near the base rate
assert res["weighted"][1] > 5 * yte.mean()               # weights inflate probabilities
assert res["focal"][1] > 2 * yte.mean() or res["focal"][1] < yte.mean() / 2   # focal distorts them too (direction printed above)
assert all(v[0] > 5 * yte.mean() for v in res.values())  # all rank far better than no-skill
