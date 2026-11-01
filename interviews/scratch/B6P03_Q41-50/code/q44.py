# Q44: imputation for training vs for serving one row. Illustrative simulation (numpy only).
import numpy as np
rng = np.random.default_rng(44)

mean = np.array([0.0, 0.0, 0.0]); 
cov = np.array([[1.0, 0.3, 0.5], [0.3, 1.0, 0.2], [0.5, 0.2, 1.0]])
def draw(n):
    X = rng.multivariate_normal(mean, cov, n)
    y = X[:, 0] + X[:, 1] + 0.5 * X[:, 2] + rng.normal(0, 0.7, n)
    return X, y

Xtr, ytr = draw(50_000); Xte, yte = draw(50_000)
miss_rate = 0.50                                   # column 1 missing in 50% of rows (MCAR here)
mtr = rng.random(len(ytr)) < miss_rate; mte = rng.random(len(yte)) < miss_rate

def ols(X, t):
    A = np.column_stack([np.ones(len(X)), X]); return np.linalg.lstsq(A, t, rcond=None)[0]
def pred(w, X): return np.column_stack([np.ones(len(X)), X]) @ w
def r2(t, p): return 1 - ((t - p) ** 2).sum() / ((t - t.mean()) ** 2).sum()

# imputers fitted on TRAINING rows only (stored as small coefficient vectors)
obs = ~mtr
w_noy = ols(Xtr[obs][:, [0, 2]], Xtr[obs, 1])                         # x1 ~ x0, x2          (no target)
w_y   = ols(np.column_stack([Xtr[obs][:, [0, 2]], ytr[obs]]), Xtr[obs, 1])   # x1 ~ x0, x2, y (uses target)

def impute(X, m, w, y=None):
    Z = X.copy()
    F = X[:, [0, 2]] if y is None else np.column_stack([X[:, [0, 2]], y])
    Z[m, 1] = pred(w, F)[m]
    return Z

# Train A: imputation used the target (like a "full data" imputation model). Train B: no target.
A = impute(Xtr, mtr, w_y, ytr); B = impute(Xtr, mtr, w_noy)
mA = ols(A, ytr); mB = ols(B, ytr)

# Serving: target unknown, only this row's other fields available
Se = impute(Xte, mte, w_noy)
print(f"coefficient on x1  A (target-informed fill): {mA[2]:.3f}   B (no target): {mB[2]:.3f}   truth 1.000")
rA = r2(yte, pred(mA, Se)); rB = r2(yte, pred(mB, Se)); rfull = r2(yte, pred(ols(Xtr, ytr), Xte))
print(f"serving R2  A: {rA:.3f}   B: {rB:.3f}   no missing at all: {rfull:.3f}")
assert rB > rA and mA[2] - mB[2] > 0.15 and abs(mB[2] - 1) < 0.05

# Pattern problem: at serving, x2 may ALSO be missing. Gaussian conditional mean for any observed subset.
def cond_mean(obs_idx, x_obs, miss_idx, mu, S):
    So = S[np.ix_(obs_idx, obs_idx)]; Smo = S[np.ix_(miss_idx, obs_idx)]
    return mu[miss_idx] + Smo @ np.linalg.solve(So, x_obs - mu[obs_idx])

mu_hat = Xtr.mean(0); S_hat = np.cov(Xtr.T)
row = np.array([1.0, np.nan, np.nan])
print("x1, x2 missing, x0=1.0 ->", np.round(cond_mean([0], row[[0]], [1, 2], mu_hat, S_hat), 3))
assert abs(cond_mean([0], row[[0]], [1, 2], mu_hat, S_hat)[0] - 0.3) < 0.03

# Multiple imputation draws spread; for ONE prediction use the mean (or train with missingness)
res_sd = np.std(Xtr[obs, 1] - pred(w_noy, Xtr[obs][:, [0, 2]]))
print(f"residual sd of the fill (what 'multiple' imputation adds as noise): {res_sd:.3f}")
