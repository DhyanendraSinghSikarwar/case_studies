import numpy as np
from scipy.stats import ks_2samp
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(1)
N = 20000

def make(n, w=(2.0, 1.0, 0.0), mean1=0.0):
    X = rng.normal(0, 1, (n, 3)); X[:, 0] += mean1
    p = 1 / (1 + np.exp(-(X @ np.array(w) - 0.2)))
    return X, (rng.random(n) < p).astype(int)

Xtr, ytr = make(N)
model = LogisticRegression().fit(Xtr, ytr)

def report(name, X, y, note):
    d = max(ks_2samp(Xtr[:, j], X[:, j]).statistic for j in range(3))
    pred = model.predict(X)
    print(f"{name:<22} maxKS_D={d:5.3f}  pos_rate={pred.mean():5.3f}  acc={(pred == y).mean():5.3f}  {note}")

print(f"{'train (reference)':<22} pos_rate={model.predict(Xtr).mean():5.3f}  acc={model.score(Xtr, ytr):5.3f}")
X, y = make(N);                      report("no change", X, y, "control")
X, y = make(N, mean1=1.0);           report("covariate shift", X, y, "P(x) moved, P(y|x) same")
X, y = make(N, w=(2.0, -1.0, 0.0));  report("concept drift", X, y, "x same, P(y|x) changed")
# label/prior shift: keep P(x|y), resample so positives are rarer
Xp, yp = make(4 * N)
keep = (yp == 0) | (rng.random(len(yp)) < 0.2)
report("label (prior) shift", Xp[keep][:N], yp[keep][:N], "P(y) 0.5 -> about 0.17")
# upstream change: feature 2 now arrives as 0 (null filled with 0)
X, y = make(N); X[:, 1] = 0.0;       report("upstream change", X, y, "feature 2 filled with 0")
# skew: serving code scales feature 1 differently from training code
X, y = make(N); Xs = X.copy(); Xs[:, 0] *= 100
d = max(ks_2samp(Xtr[:, j], Xs[:, j]).statistic for j in range(3))
pred = model.predict(Xs)
print(f"{'train-serve skew':<22} maxKS_D={d:5.3f}  pos_rate={pred.mean():5.3f}  acc={(pred == y).mean():5.3f}  bug: unit scale")
# the skew check: replay the same raw rows through both code paths
print("parity max abs diff, same raw rows:", float(np.abs(Xs - X).max()).__round__(1), "(world data identical, pipeline differs)")
