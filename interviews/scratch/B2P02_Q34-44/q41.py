import numpy as np
# SYNTHETIC: true law L = 1.7 + 400 * N^-0.34 (N in millions); noisy small runs; extrapolate 100x
f = lambda N, E, A, a: E + A * N ** (-a)
true = (1.7, 400.0, 0.34)
rng = np.random.default_rng(0)
N_fit = np.logspace(0, 2, 8)                        # 1M .. 100M params
N_big = 1e4                                         # 10B params = 100x beyond the fit range
grid = np.linspace(0.05, 1.0, 400)                  # candidate exponents

def fit(y):
    best = None
    for a in grid:                                  # for each a, E and A are linear least squares
        X = np.c_[np.ones_like(N_fit), N_fit ** (-a)]
        coef, res, *_ = np.linalg.lstsq(X, y, rcond=None)
        sse = ((X @ coef - y) ** 2).sum()
        if coef[1] > 0 and coef[0] >= 0 and (best is None or sse < best[0]):
            best = (sse, coef[0], coef[1], a)
    return best[1:]

preds = []
for s in range(200):
    y = f(N_fit, *true) + rng.normal(0, 0.01, N_fit.size)   # 0.01 loss noise
    E, A, a = fit(y)
    preds.append((f(N_big, E, A, a), E))
preds = np.array(preds)
print("true loss at 10B: %.3f" % f(N_big, *true))
print("extrapolated: median %.3f, 5th-95th pct %.3f to %.3f" % (np.median(preds[:, 0]), *np.percentile(preds[:, 0], [5, 95])))
print("fitted irreducible term E: 5th-95th pct %.2f to %.2f (true 1.70)" % tuple(np.percentile(preds[:, 1], [5, 95])))
