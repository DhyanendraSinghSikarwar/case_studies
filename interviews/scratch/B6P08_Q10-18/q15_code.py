import numpy as np

assert round(0.842 - 0.829, 3) == 0.013
rng = np.random.default_rng(15)
n, pos_rate = 10_000, 0.10                     # ASSUMED 10% positives (the prompt does not say)
npos = int(n * pos_rate); nneg = n - npos
assert (npos, nneg) == (1000, 9000)

# Hanley-McNeil standard error of one AUC
def hm_se(auc, npos, nneg):
    q1 = auc / (2 - auc); q2 = 2 * auc * auc / (1 + auc)
    v = (auc * (1 - auc) + (npos - 1) * (q1 - auc**2) + (nneg - 1) * (q2 - auc**2)) / (npos * nneg)
    return v ** 0.5
se1 = hm_se(0.842, npos, nneg)
print("Hanley-McNeil SE of one AUC:", round(se1, 4))
assert round(se1, 3) == 0.008
se_diff_indep = (2 * se1 ** 2) ** 0.5
print("SE of the gap if two different holdouts:", round(se_diff_indep, 4), "| gap/SE:", round(0.013 / se_diff_indep, 2))
assert 0.010 < se_diff_indep < 0.013 and 1.0 < 0.013 / se_diff_indep < 1.4

# Simulate: scores with AUC about 0.84, bootstrap SE of AUC and a seed-noise check on a tiny model
def auc(y, s):
    r = s.argsort().argsort() + 1
    return (r[y == 1].sum() - npos * (npos + 1) / 2) / (npos * nneg)
y = np.r_[np.ones(npos), np.zeros(nneg)].astype(int)
s = np.r_[rng.normal(1.4, 1, npos), rng.normal(0, 1, nneg)]
a0 = auc(y, s)
boots = []
for _ in range(300):
    i = rng.integers(0, n, n); yy, ss = y[i], s[i]
    k1 = yy.sum(); k0 = n - k1
    r = ss.argsort().argsort() + 1
    boots.append((r[yy == 1].sum() - k1 * (k1 + 1) / 2) / (k1 * k0))
print("simulated AUC", round(a0, 3), "| bootstrap SE", round(float(np.std(boots)), 4))
assert 0.005 < np.std(boots) < 0.011

# Seed noise: logistic regression by gradient descent from random starts + row-order shuffles
X = np.c_[s, rng.normal(size=(n, 3))]
def fit(seed, steps=30):
    r = np.random.default_rng(seed); w = r.normal(0, 1, X.shape[1]); idx = r.permutation(n)
    for _ in range(steps):                       # a few SGD-style mini-batch steps, undertrained on purpose
        for b in np.array_split(idx, 20):
            p = 1 / (1 + np.exp(-(X[b] @ w))); w -= 0.05 * X[b].T @ (p - y[b]) / len(b)
    return auc(y, X @ w)
aucs = [fit(sd) for sd in range(10)]
print("seed-only spread over 10 fits: min", round(min(aucs), 4), "max", round(max(aucs), 4), "sd", round(float(np.std(aucs)), 4))
assert np.std(aucs) < 0.02
print("so a 0.013 gap is about", round(0.013 / se_diff_indep, 1), "SE: not strong evidence of real change from the data alone")
