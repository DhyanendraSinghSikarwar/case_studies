# Q16: feature missingness jumps from 5% to 40% (illustrative simulation)
import numpy as np
from scipy.stats import rankdata, norm
rng = np.random.default_rng(16)
def sig(z): return 1 / (1 + np.exp(-z))
def auc(s, y):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, it=30):
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (y - p))
    return w
def make(n, miss_rate, informative=False):
    x1, x2 = rng.normal(size=n), rng.normal(size=n)
    y = (rng.random(n) < sig(-1.0 + 1.0 * x1 + 1.4 * x2)).astype(float)
    if informative:      # training world: the feature is missing more often for positives (about 5% overall)
        miss = rng.random(n) < np.where(y == 1, 0.09, 0.03)
    else:                # outage world: missing at random, whatever the label
        miss = rng.random(n) < miss_rate
    return x1, x2, miss, y
def design(x1, x2, miss, mu2, flag):
    x2f = np.where(miss, mu2, x2)                       # mean imputation
    cols = [np.ones(len(x1)), x1, x2f] + ([miss.astype(float)] if flag else [])
    return np.c_[tuple(cols)]
x1, x2, m, y = make(300_000, 0, informative=True)
print(f"training: missing rate {m.mean():.1%}; positive rate when missing {y[m].mean():.1%} vs present {y[~m].mean():.1%}")
mu2 = x2[~m].mean()
# A: today's setup (mean imputation, no flag)
wA = fit(design(x1, x2, m, mu2, False), y)
# B: add a missing flag, trained on the real 5% (the flag soaks up the label link)
wB = fit(design(x1, x2, m, mu2, True), y)
# C: flag, but training copies also get extra RANDOM missingness (to about 40%), so the flag cannot stand for risk
x1c, x2c, mc, yc = np.r_[x1, x1], np.r_[x2, x2], np.r_[m, m | (rng.random(len(m)) < 0.37)], np.r_[y, y]
wC = fit(design(x1c, x2c, mc, mu2, True), yc)
print("flag coefficient: B", round(float(wB[3]), 2), " C", round(float(wC[3]), 2))
out = {}
for rate in (0.05, 0.40):
    a1, a2, am, ay = make(150_000, rate)
    row = []
    for w, f in ((wA, False), (wB, True), (wC, True)):
        sc = design(a1, a2, am, mu2, f) @ w
        row.append((auc(sc, ay), float(sig(sc).mean())))
    out[rate] = row
    print(f"live missing {rate:.0%} (random): actual rate {ay.mean():.3f} | AUC / mean score  A {row[0][0]:.3f} / {row[0][1]:.3f}   B {row[1][0]:.3f} / {row[1][1]:.3f}   C {row[2][0]:.3f} / {row[2][1]:.3f}")
assert out[0.05][0][0] - out[0.40][0][0] > 0.04          # every model loses AUC: the information really is gone
assert out[0.40][1][0] < out[0.40][2][0] - 0.01           # flag-trained-on-5% (B) is worse than the augmented model (C)
# alert: hourly missing rate against the training rate, exact binomial limit, 2,000 requests an hour
from scipy.stats import binom
n_h, p0 = 2_000, 0.05
limit = binom.ppf(0.9999, n_h, p0)                       # about 1 false alarm in 10,000 normal hours
print(f"alert when more than {int(limit)} of {n_h} hourly requests are missing ({limit / n_h:.2%})")
quiet = rng.binomial(n_h, p0, 24 * 30)
print("false alarms in 30 days (720 normal hours):", int((quiet > limit).sum()))
outage = rng.binomial(n_h, 0.40)
print(f"outage hour: {outage} missing of {n_h} -> alarm {outage > limit}")
assert limit / n_h < 0.07 and outage > limit
