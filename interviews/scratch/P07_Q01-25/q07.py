import numpy as np
rng = np.random.default_rng(0)
nu, ni, d = 300, 150, 5
truth = rng.normal(size=(nu,d)) @ rng.normal(size=(ni,d)).T / np.sqrt(d)
R = truth + rng.normal(0, .3, truth.shape)
obs = rng.random((nu, ni)) < 0.2
tr = obs & (rng.random((nu, ni)) < 0.8); te = obs & ~tr

def als(mask, k=5, lam=1.0, iters=15):
    P = rng.normal(0, .1, (nu, k)); Q = rng.normal(0, .1, (ni, k))
    I = lam * np.eye(k)
    for _ in range(iters):
        for u in range(nu):                       # fix Q, solve each user
            j = mask[u]
            P[u] = np.linalg.solve(Q[j].T @ Q[j] + I, Q[j].T @ R[u, j])
        for i in range(ni):                       # fix P, solve each item
            j = mask[:, i]
            Q[i] = np.linalg.solve(P[j].T @ P[j] + I, P[j].T @ R[j, i])
    return P @ Q.T

rmse = lambda pred: np.sqrt(((pred - R)[te] ** 2).mean())
print("ALS, observed entries only:", round(rmse(als(tr)), 2))
print("global-mean baseline      :", round(rmse(np.full_like(R, R[tr].mean())), 2))
# "missing = 0" version: treat every unobserved cell as a rating of 0
R0 = np.where(tr, R, 0.0)
U, s, Vt = np.linalg.svd(R0, full_matrices=False)
pred0 = (U[:, :5] * s[:5]) @ Vt[:5]
print("SVD with missing = 0      :", round(rmse(pred0), 2))
