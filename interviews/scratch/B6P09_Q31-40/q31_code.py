import numpy as np

rng = np.random.default_rng(31)
names = ["income", "tenure", "debt_ratio", "utilisation", "inquiries", "file_age"]
n, p = 1500, len(names)
cov = np.eye(p)
cov[0, 1] = cov[1, 0] = 0.85            # income and tenure correlated at 0.85
X = rng.multivariate_normal(np.zeros(p), cov, size=n)
beta_true = np.array([-0.45, -0.45, 0.50, 0.40, 0.25, -0.20])
pd_true = 1 / (1 + np.exp(-(-2.0 + X @ beta_true)))
y = (rng.random(n) < pd_true).astype(float)
print("sample corr(income, tenure) =", round(np.corrcoef(X[:, 0], X[:, 1])[0, 1], 3))
assert abs(np.corrcoef(X[:, 0], X[:, 1])[0, 1] - 0.85) < 0.03

def fit(Xb, yb, l2=1e-3, it=25):
    A = np.c_[np.ones(len(Xb)), Xb]
    w = np.zeros(A.shape[1])
    for _ in range(it):                     # IRLS (Newton) for logistic regression
        mu = 1 / (1 + np.exp(-(A @ w)))
        W = mu * (1 - mu)
        H = A.T @ (A * W[:, None]) + l2 * np.eye(A.shape[1])
        w = w + np.linalg.solve(H, A.T @ (yb - mu) - l2 * w)
    return w

def retrain(seed):
    r = np.random.default_rng(seed)
    idx = r.integers(0, n, n)               # a retrain = a fresh resample of the same population
    return fit(X[idx], y[idx])

# 100 reviewed declines: the 100 highest-risk applicants under the reference model
w_ref = fit(X, y)
risk = np.c_[np.ones(n), X] @ w_ref
dec = np.argsort(-risk)[:100]
mu_x = X.mean(0)

def contrib(w, rows):                       # linear-logit attribution: coef * (x - mean)
    return w[1:] * (X[rows] - mu_x)

def top(w, rows, groups=None):
    c = contrib(w, rows)
    if groups is not None:
        c = np.c_[[c[:, g].sum(1) for g in groups]].T
    return c.argmax(1), np.argsort(-c, 1)[:, :4]

wa, wb = retrain(1), retrain(2)
ta, sa = top(wa, dec); tb, sb = top(wb, dec)
flip = int((ta != tb).sum())
print("raw top reason differs between two retrains:", flip, "of 100")
jac = np.mean([len(set(a) & set(b)) / len(set(a) | set(b)) for a, b in zip(sa, sb)])
print("mean Jaccard overlap of the 4-reason sets (raw):", round(jac, 3))

groups = [[0, 1], [2], [3], [4], [5]]       # income+tenure merged into one reason group
ga, _ = top(wa, dec, groups); gb, _ = top(wb, dec, groups)
gflip = int((ga != gb).sum())
print("grouped (income+tenure = one reason) top reason differs:", gflip, "of 100")

def bagged(seed0, B=60):
    return np.mean([retrain(seed0 + b) for b in range(B)], axis=0)
ba, bb = bagged(1000), bagged(2000)
tba, _ = top(ba, dec); tbb, _ = top(bb, dec)
bflip = int((tba != tbb).sum())
print("bagged coefficients (60 resamples each), raw top reason differs:", bflip, "of 100")

# validation numbers: how big is 30 of 100? Wilson interval for the prompt's sample
def wilson(k, m, z=1.96):
    ph = k / m; d = 1 + z * z / m
    c = (ph + z * z / (2 * m)) / d
    h = z * np.sqrt(ph * (1 - ph) / m + z * z / (4 * m * m)) / d
    return c - h, c + h
lo, hi = wilson(30, 100)
print("prompt: 30 of 100 =", 30 / 100, "| 95% Wilson interval", round(lo, 3), "to", round(hi, 3))
assert 30 / 100 == 0.3 and 0.21 < lo < 0.22 and 0.39 < hi < 0.40
print("coefficient sd across 60 resamples (income, tenure):",
      np.round(np.std([retrain(5000 + b)[1:3] for b in range(60)], axis=0), 3))
corr_ab = np.corrcoef(np.array([retrain(5000 + b)[1:3] for b in range(60)]).T)[0, 1]
print("corr of income and tenure coefficient across resamples:", round(corr_ab, 3))
print("true coefficients", dict(zip(names, beta_true.tolist())))
assert flip == 47 and gflip == 12 and bflip == 17 and round(jac, 3) == 0.884
assert gflip < flip and bflip < flip
assert corr_ab < -0.7
