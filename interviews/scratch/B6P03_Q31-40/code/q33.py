import numpy as np

# --- the arithmetic in the prompt
real_fraud, total = 800, 400_000
synth = 50_000
legit = total - real_fraud
print("fraud share before:", round(real_fraud / total, 4))
print("fraud share after adding 50,000:", round((real_fraud + synth) / (legit + real_fraud + synth), 4))
need = legit - real_fraud
print("synthetic rows needed for 50/50:", need)
assert round((real_fraud + synth) / (total + synth), 3) == round(50_800 / 450_000, 3)
assert need == 398_400

rng = np.random.default_rng(33)
d = 4
def make(n, nf):
    X = rng.normal(size=(n, d)); y = np.zeros(n, int); y[:nf] = 1       # exactly nf frauds
    sign = np.where(rng.random(nf) < 0.5, -1.0, 1.0)                     # two fraud modes: x0 near -2.2 or +2.2
    X[:nf, 0] = sign * 2.2 + rng.normal(scale=0.6, size=nf)
    X[:nf, 1] += 1.0; X[:nf, 2] += 0.8; X[:nf, 3] += 0.6
    p = rng.permutation(n)
    return X[p], y[p]
X, y = make(400_000, 800)
print("simulated fraud cases:", int(y.sum()), "rate", round(float(y.mean()), 4))
idx = rng.permutation(len(y)); tr, te = idx[:280_000], idx[280_000:]
Xtr, ytr, Xte, yte = X[tr], y[tr], X[te], y[te]

def feats(X): return np.hstack([X, X ** 2, np.ones((len(X), 1))])
def fit(F, t, w=None, iters=25, l2=1e-3):
    w = np.ones(len(t)) if w is None else w
    b = np.zeros(F.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-F @ b)); g = F.T @ (w * (p - t)) + l2 * b
        H = (F * (w * p * (1 - p))[:, None]).T @ F + l2 * np.eye(len(b))
        b -= np.linalg.solve(H, g)
    return b
def ap(t, s):
    o = np.argsort(-s); t = t[o]; tp = np.cumsum(t)
    return float(np.sum(tp / np.arange(1, len(t) + 1) * t) / t.sum())

# generators fitted ONLY on the 560 real training frauds (the honest way), or on all frauds (the leak)
F_tr = Xtr[ytr == 1]; F_all = X[y == 1]
def gaussian_gen(src, n):
    return rng.multivariate_normal(src.mean(0), np.cov(src.T), n)
def memoriser_gen(src, n, s=0.15):
    return src[rng.integers(0, len(src), n)] + rng.normal(scale=s, size=(n, d))

from scipy.spatial import cKDTree
def run(Xs=None):
    Xa = Xtr if Xs is None else np.vstack([Xtr, Xs]); ya = ytr if Xs is None else np.r_[ytr, np.ones(len(Xs), int)]
    b = fit(feats(Xa), ya)
    lr = ap(yte, feats(Xte) @ b)
    _, nn = cKDTree(Xa).query(Xte, k=15)
    knn = ap(yte, ya[nn].mean(1) + 1e-6 * (feats(Xte) @ b > 0))
    return lr, knn
print("test fraud cases:", int(yte.sum()), "train fraud cases:", int(ytr.sum()))
res = {}
res["real only"] = run()
res["+50k gaussian (one blob)"] = run(gaussian_gen(F_tr, synth))
res["+50k memoriser (train frauds)"] = run(memoriser_gen(F_tr, synth))
res["+50k memoriser fitted on ALL frauds (leak)"] = run(memoriser_gen(F_all, synth))
print(f"{'arm':45s} {'logistic PR-AUC':>16s} {'15-NN PR-AUC':>13s}   (real test, base rate {yte.mean():.4f})")
for k, v in res.items(): print(f"{k:45s} {v[0]:16.3f} {v[1]:13.3f}")
# the leak is visible: the leaky arm beats the honest memoriser only because test frauds were copied
assert res["+50k memoriser fitted on ALL frauds (leak)"][1] > res["+50k memoriser (train frauds)"][1]
# sanity: how many of the 50,000 synthetic rows are within 0.3 of a real test fraud in the leaky arm vs honest
def near_test(Xs):
    T = Xte[yte == 1]; c = 0
    for r in Xs[:2000]: c += (np.sqrt(((T - r) ** 2).sum(1)).min() < 0.3)
    return c / 2000
print("share of synthetic rows within 0.3 of a real TEST fraud: honest", near_test(memoriser_gen(F_tr, synth)), " leaky", near_test(memoriser_gen(F_all, synth)))
assert near_test(memoriser_gen(F_all, synth)) > near_test(memoriser_gen(F_tr, synth))
# one real train fraud is copied about 50,000 / 560 times
print("copies per real training fraud:", round(synth / int(ytr.sum()), 1))
assert 80 < synth / int(ytr.sum()) < 100
gs = gaussian_gen(F_tr, synth)
print("share of real train frauds with |x0|<1:", round(float((np.abs(F_tr[:, 0]) < 1).mean()), 3), "  of gaussian synthetic rows:", round(float((np.abs(gs[:, 0]) < 1).mean()), 3))
assert (np.abs(gs[:, 0]) < 1).mean() > 5 * (np.abs(F_tr[:, 0]) < 1).mean()
