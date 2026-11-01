import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(37)
n = 100_000
x1 = rng.normal(size=n); x2 = rng.normal(size=n)
z = 2.0 * x1 - 1.0 * x2 + rng.normal(scale=0.7, size=n) + 3.0          # feature with missing values; strongly related to x1, x2
logit = 0.9 * (z - 3.0) + 0.5 * x1 - 0.3 * x2 - 1.0
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
# MAR: missingness depends on x1, x2 (observed), tuned to 15%
t = -2.3 + 1.2 * x1 + 0.8 * x2
m = rng.random(n) < 1 / (1 + np.exp(-t))
print("missing share:", round(float(m.mean()), 3), " mean z when missing / observed:", round(float(z[m].mean()), 2), round(float(z[~m].mean()), 2))
assert 0.14 < m.mean() < 0.16

def auc(y, s):
    r = rankdata(s); n1 = int(y.sum()); return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1))
def fit(F, t, iters=20, l2=1e-3):
    b = np.zeros(F.shape[1])
    for _ in range(iters):
        q = 1 / (1 + np.exp(-F @ b)); g = F.T @ (q - t) + l2 * b
        H = (F * (q * (1 - q))[:, None]).T @ F + l2 * np.eye(len(b)); b -= np.linalg.solve(H, g)
    return b
def lin_fit(A, t): return np.linalg.lstsq(A, t, rcond=None)[0]

# imputers: each is fitted on a training part only, then applied to any part
def make_median(Xa, za, ma, ya=None):
    med = np.median(za[~ma])
    return lambda Xb, zb, mb: (np.where(mb, med, zb), mb.astype(float))
def make_regress(Xa, za, ma, ya=None):
    A = np.c_[Xa, np.ones(len(Xa))]; beta_ = lin_fit(A[~ma], za[~ma])
    return lambda Xb, zb, mb: (np.where(mb, np.c_[Xb, np.ones(len(Xb))] @ beta_, zb), mb.astype(float))
def make_leaky_target(Xa, za, ma, ya):                       # includes the TARGET in the imputation model
    A = np.c_[Xa, ya, np.ones(len(Xa))]; beta_ = lin_fit(A[~ma], za[~ma])
    return lambda Xb, zb, mb, yb: (np.where(mb, np.c_[Xb, yb, np.ones(len(Xb))] @ beta_, zb), mb.astype(float))

X = np.c_[x1, x2]
tr = np.arange(n) < 70_000; te = ~tr
res = {}
# a) imputation quality on rows where z is known: mask them under the same mechanism, impute, score RMSE
known = ~m
# hide a further share of the known values with the same MAR mechanism
msk = known & (rng.random(n) < 1 / (1 + np.exp(-(t + 0.0))))
for name, mk in [("median", make_median), ("regression", make_regress)]:
    imp = mk(X[tr], z[tr], m[tr] | msk[tr])
    zi, _ = imp(X[te], z[te], msk[te] | m[te])
    err = zi[msk[te]] - z[te][msk[te]]
    print(f"imputation RMSE on masked known values, {name:10s}: {np.sqrt((err ** 2).mean()):.3f}   (std of z {z.std():.2f})")

# b) downstream AUC, imputer fitted on the training part only
def downstream(mk, add_flag=True):
    imp = mk(X[tr], z[tr], m[tr])
    ztr, ftr = imp(X[tr], z[tr], m[tr]); zte, fte = imp(X[te], z[te], m[te])
    cols = lambda Xb, zb, fb: np.c_[Xb, zb, fb] if add_flag else np.c_[Xb, zb]
    Ftr = np.c_[cols(X[tr], ztr, ftr), np.ones(tr.sum())]; Fte = np.c_[cols(X[te], zte, fte), np.ones(te.sum())]
    b = fit(Ftr, y[tr]); sc = Fte @ b; return auc(y[te], sc), auc(y[te][m[te]], sc[m[te]])
bf = fit(np.c_[X[tr], z[tr], np.ones(tr.sum())], y[tr]); sf = np.c_[X[te], z[te], np.ones(te.sum())] @ bf
full, full_m = auc(y[te], sf), auc(y[te][m[te]], sf[m[te]])
print("AUC with z fully observed (ceiling): all test rows", round(float(full), 4), "  rows that are missing in practice", round(float(full_m), 4))
for name, mk in [("median", make_median), ("regression", make_regress)]:
    for flag in (False, True):
        a_all, a_m = downstream(mk, flag); print(f"AUC, {name:10s} flag={flag!s:5s}: all rows {a_all:.4f}   missing-rows only {a_m:.4f}")
# c) the leak: impute using the target, on both parts (fine offline, impossible at serving time)
imp = make_leaky_target(X[tr], z[tr], m[tr], y[tr])
ztr, ftr = imp(X[tr], z[tr], m[tr], y[tr]); zte, fte = imp(X[te], z[te], m[te], y[te])
b = fit(np.c_[X[tr], ztr, ftr, np.ones(tr.sum())], y[tr])
sl = np.c_[X[te], zte, fte, np.ones(te.sum())] @ b
leak_auc, leak_m = auc(y[te], sl), auc(y[te][m[te]], sl[m[te]])
print("AUC with target-aware imputation (leak): all rows", round(float(leak_auc), 4), "  missing-rows only", round(float(leak_m), 4))
assert leak_m > full_m + 0.01
# d) imputer fitted on all rows vs inside the training fold: for a label-free imputer the gap is tiny, still do it inside
imp_all = make_median(X, z, m)
zall, _ = imp_all(X, z, m)
print("median fitted on all rows:", round(float(np.median(z[~m])), 4), " fitted on train part:", round(float(np.median(z[tr & ~m])), 4))
print("MAR check: missing rate in x1 quartiles:", [round(float(m[(x1 >= lo) & (x1 < hi)].mean()), 3) for lo, hi in zip(np.quantile(x1, [0, .25, .5, .75]), np.r_[np.quantile(x1, [.25, .5, .75]), 1e9])])
