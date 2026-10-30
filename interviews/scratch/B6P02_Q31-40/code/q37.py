# Q37: retrain on the last 4 weeks, which had a payment outage and a heavy promotion (illustrative simulation)
import numpy as np
from scipy.stats import rankdata

rng = np.random.default_rng(37)
sig = lambda z: 1 / (1 + np.exp(-z))
def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def fit(X, y, steps=30, l2=1e-3):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = sig(Xb @ w); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w)); w -= np.linalg.solve(H, g)
    return w
pred = lambda w, X: sig(np.c_[np.ones(len(X)), X] @ w)
def logloss(y, p): p = np.clip(p, 1e-6, 1 - 1e-6); return -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()

# 30 weeks of daily data, 700 rows a day. Weeks 25-28 = the last four weeks used for the retrain.
days, per = 210, 400
beta = np.array([1.0, -0.8, 0.5]); b0 = -1.0
rows = []
for d in range(days):
    wk = d // 7
    promo = 24 <= wk <= 27 and (d % 7) in (2, 3, 4)           # promo days in the 4-week window
    outage = wk == 26 and (d % 7) in (0, 1, 2, 3, 4)                  # payment outage days
    X = rng.normal(0, 1, (per, 3))
    if promo: X[:, 0] += 1.5                                  # promo-driven shift in feature 0
    y = (rng.random(per) < sig(b0 + X @ beta)).astype(float)
    if outage:                                                # failed payments mislabelled as the positive class
        flip = rng.random(per) < 0.6
        y = np.where(flip, 1.0, y)
    rows.append((np.full(per, d), X, y, np.full(per, promo), np.full(per, outage)))
D = np.concatenate([r[0] for r in rows]); X = np.concatenate([r[1] for r in rows])
Y = np.concatenate([r[2] for r in rows]); P = np.concatenate([r[3] for r in rows]); O = np.concatenate([r[4] for r in rows])
print(f"outage days: {len(np.unique(D[O]))}, promo days: {len(np.unique(D[P]))}, share of the 4-week window with a flipped-label risk: {O[D >= 168].mean():.1%}")

# Clean test: the next 2 weeks (days 196-209 are normal; train data end before day 196)
test = D >= 196; Xt, Yt = X[test], Y[test]
window = (D >= 168) & (D < 196)
old_w = fit(X[D < 168], Y[D < 168])                       # old model: weeks 1-24
models = {
    "old model (weeks 1-24)": old_w,
    "retrain: last 4 weeks, as is": fit(X[window], Y[window]),
    "retrain: last 4 weeks, outage days dropped": fit(X[window & ~O], Y[window & ~O]),
    "retrain: 28 weeks, outage dropped, promo flag": None,
}
# 28 weeks with outage days dropped, promo flag as a feature (set to 0 at serving on normal days)
tr = (D < 196) & ~O
Xf = np.c_[X, P.astype(float)]
w_flag = fit(Xf[tr], Y[tr])
res = {}; ratio_ = {}
for k, w in models.items():
    if w is None: p = pred(w_flag, np.c_[Xt, np.zeros(len(Xt))])
    else: p = pred(w, Xt)
    res[k] = (auc(Yt, p), logloss(Yt, p))
    print(f"{k:48} AUC {res[k][0]:.4f}  log loss {res[k][1]:.4f}  mean pred/observed {p.mean() / Yt.mean():.3f}")
    ratio_[k] = p.mean() / Yt.mean()
a_old = res["old model (weeks 1-24)"]; a_bad = res["retrain: last 4 weeks, as is"]
a_fix = res["retrain: 28 weeks, outage dropped, promo flag"]
assert a_bad[1] > a_old[1]                      # the naive retrain is worse than the old model on log loss
assert a_fix[1] <= a_old[1] + 0.003             # a careful retrain is at least as good
assert res["retrain: last 4 weeks, outage days dropped"][1] < a_bad[1]
print(f"naive retrain minus old model: log loss {a_bad[1] - a_old[1]:+.4f}")
assert ratio_["retrain: last 4 weeks, as is"] > ratio_["old model (weeks 1-24)"] + 0.02   # inflated base rate
# in the 4-week window the outage and promo days differ from normal days:
print(f"positive rate: normal window days {Y[window & ~O & ~P].mean():.3f}, outage days {Y[window & O].mean():.3f}, test {Yt.mean():.3f}")
assert Y[window & O].mean() > Y[window & ~O & ~P].mean() + 0.1
