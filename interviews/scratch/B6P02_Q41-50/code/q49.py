# Q49: regime change; 2 years of old data, 6 weeks of new data. Illustrative simulation.
import numpy as np
from scipy.optimize import minimize
from scipy.stats import rankdata
rng = np.random.default_rng(49)
d = 30
beta_old = rng.normal(0, 0.4, d)
beta_new = beta_old.copy()
beta_new[:4] = [1.0, -1.0, 0.8, -0.8]          # four features change meaning, 26 keep it
b0 = -3.5
def gen(n, beta):
    X = rng.normal(size=(n, d))
    y = rng.random(n) < 1/(1+np.exp(-(b0 + X@beta)))
    return X, y.astype(float)
n_old, n_new = 200_000, 500
Xo, yo = gen(n_old, beta_old)
Xn, yn = gen(n_new, beta_new)
Xt, yt = gen(100_000, beta_new)               # future new-regime data

def fit(X, y, w=None, l2=0.0, center=None):
    X1 = np.column_stack([np.ones(len(X)), X]); w = np.ones(len(y)) if w is None else w
    c = np.zeros(d+1) if center is None else center
    f = lambda b: np.sum(w*(np.logaddexp(0, X1@b) - y*(X1@b)))/w.sum() + l2*np.sum((b[1:]-c[1:])**2)
    return minimize(f, c, method="L-BFGS-B").x
def auc(b, X, y):
    s = np.column_stack([np.ones(len(X)), X])@b
    r = rankdata(s); n1 = y.sum(); n0 = len(y)-n1
    return (r[y == 1].sum() - n1*(n1+1)/2)/(n1*n0)
print(f"new-regime events in 6 weeks: {int(yn.sum())} of {n_new}")
b_old = fit(Xo, yo)
res = {"old model unchanged": auc(b_old, Xt, yt), "new data only": auc(fit(Xn, yn, l2=0.0), Xt, yt)}
res["new data only, ridge 0.01"] = auc(fit(Xn, yn, l2=0.01), Xt, yt)
for lam in (0.01, 0.03, 0.1):
    res[f"new data, shrink to old, lam {lam}"] = auc(fit(Xn, yn, l2=lam, center=b_old), Xt, yt)
X = np.vstack([Xo, Xn]); y = np.concatenate([yo, yn])
res["pooled, old weight 0.02"] = auc(fit(X, y, np.concatenate([np.full(n_old, 0.02), np.ones(n_new)])), Xt, yt)
res["oracle (true new coefficients)"] = auc(np.concatenate([[b0], beta_new]), Xt, yt)
for k, v in res.items(): print(f"{k:38s} AUC on future new-regime data = {v:.3f}")
shrink = {k: v for k, v in res.items() if "shrink" in k}
best_shrink = max(shrink.values())
assert best_shrink > res["old model unchanged"] + 0.05 and res["new data only"] > res["old model unchanged"] + 0.05
assert res["oracle (true new coefficients)"] >= best_shrink
print(f"best shrink-to-old = {best_shrink:.3f} vs new-only {res['new data only']:.3f} vs old {res['old model unchanged']:.3f}")
# six weeks is a small sample, so one fit is noisy: repeat the new-only vs shrink comparison on 15 different six-week samples
a_new, a_shr = [], []
for s in range(30):
    r = np.random.default_rng(1000+s)
    Xs = r.normal(size=(n_new, d)); ys = (r.random(n_new) < 1/(1+np.exp(-(b0 + Xs@beta_new)))).astype(float)
    a_new.append(auc(fit(Xs, ys), Xt, yt)); a_shr.append(auc(fit(Xs, ys, l2=0.03, center=b_old), Xt, yt))
print(f"30 six-week samples: new-only mean {np.mean(a_new):.3f} (sd {np.std(a_new):.3f}); shrink-to-old mean {np.mean(a_shr):.3f} (sd {np.std(a_shr):.3f})")
assert abs(np.mean(a_shr) - np.mean(a_new)) < 0.01     # no clear gain from shrinking in this run
assert res['pooled, old weight 0.02'] < res['new data only'] - 0.03   # naive pooling is clearly worse
print("promotion rule used: new model must beat the interim model by more than twice the sample-to-sample sd:", round(2*np.std(a_shr), 3))
