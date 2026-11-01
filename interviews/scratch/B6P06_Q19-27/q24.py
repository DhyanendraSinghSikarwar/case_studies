import numpy as np
rng = np.random.default_rng(24)
G, per, n = 10, 4, 3000                     # 10 groups of 4 correlated features = 40 features
def make(m):
    f = rng.normal(size=(m, G))
    X = np.repeat(f, per, axis=1) * np.sqrt(0.9) + rng.normal(size=(m, G*per)) * np.sqrt(0.1)  # within-group corr 0.9
    return X, f
beta_g = np.array([1.0, -0.8, 0.6, 0.5, -0.4, 0.3, 0.2, 0.1, 0.1, 0.05])
X, f = make(n)
y = (rng.random(n) < 1/(1+np.exp(-(f@beta_g - 0.5)))).astype(float)
def fit(X, y, lam=1e-3):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(25):
        p = 1/(1+np.exp(-Xb@w)); g = Xb.T@(p-y) + lam*np.r_[0, w[1:]]
        H = (Xb.T*(p*(1-p)))@Xb + lam*np.diag(np.r_[0, np.ones(len(w)-1)])
        w = w - np.linalg.solve(H, g)
    return w[1:]
x_app = np.zeros(G*per); x_app[:] = np.repeat(np.array([0.2, 1.5, 0.3, -0.3, 0.9, 0.4, -0.2, 0.3, 0.1, 0.0]), per) # one applicant
retrains, top1, topg = 40, [], []
for r in range(retrains):
    idx = rng.integers(0, n, n)
    w = fit(X[idx], y[idx])
    mu = X[idx].mean(0)
    shap = w * (x_app - mu)              # exact SHAP in log-odds for a linear model with independent-feature baseline
    top1.append(int(np.argmax(-shap)))   # biggest push toward decline (lowest score)
    topg.append(int(np.argmax(-shap.reshape(G, per).sum(1))))
def modal_share(v): return max(np.bincount(v)) / len(v)
print(f"distinct top reasons across {retrains} retrains: single features {len(set(top1))}, groups {len(set(topg))}")
print(f"most common top reason appears in: single feature {modal_share(top1):.0%} of retrains, group {modal_share(topg):.0%}")
assert len(set(top1)) > len(set(topg))
assert modal_share(topg) > modal_share(top1)
