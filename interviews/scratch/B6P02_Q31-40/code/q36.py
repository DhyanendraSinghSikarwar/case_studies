# Q36: precision 62% -> 48% in smaller cities: covariate shift or a different relationship? (illustrative simulation)
import numpy as np

rng = np.random.default_rng(36)

# 0. Arithmetic first: how much of 62% -> 48% could a lower base rate explain alone?
odds = lambda p: p / (1 - p)
ratio = odds(0.48) / odds(0.62)
print(f"precision odds ratio 0.48 vs 0.62: {ratio:.3f}")
# precision odds = (TPR / FPR) x (prevalence odds); if TPR and FPR are fixed, prevalence odds must fall by that ratio
prev_new = lambda prev_old: (odds(prev_old) * ratio) / (1 + odds(prev_old) * ratio)
print(f"a base rate of 20% falling to {prev_new(0.20):.1%} gives the same precision drop")
assert abs(prev_new(0.20) - 0.1239) < 0.001

def sig(z): return 1 / (1 + np.exp(-z))
def fit(X, y, steps=30, l2=1e-3):
    Xb = np.c_[np.ones(len(X)), X]; w = np.zeros(Xb.shape[1])
    for _ in range(steps):
        p = sig(Xb @ w); g = Xb.T @ (p - y) + l2 * w
        H = (Xb * (p * (1 - p))[:, None]).T @ Xb + l2 * np.eye(len(w)); w -= np.linalg.solve(H, g)
    return w
pred = lambda w, X: sig(np.c_[np.ones(len(X)), X] @ w)

def world(shift_x, shift_rel, n=60_000):
    """metro: x ~ N(0,1) two features, y depends on x. new: x shifted (covariate) and/or coefficients changed (concept)."""
    beta = np.array([1.2, 0.8]); b0 = -2.2
    Xm = rng.normal(0, 1, (n, 2)); ym = rng.random(n) < sig(b0 + Xm @ beta)
    Xn = rng.normal(shift_x, 1, (n, 2))
    beta_n = beta * shift_rel[0]; b0n = b0 + shift_rel[1]
    yn = rng.random(n) < sig(b0n + Xn @ beta_n)
    return Xm, ym.astype(float), Xn, yn.astype(float)

def diagnose(name, shift_x, shift_rel, keep=False):
    Xm, ym, Xn, yn = world(shift_x, shift_rel)
    global LAST; LAST = (Xm, ym, Xn, yn)
    w = fit(Xm[:40_000], ym[:40_000]); th = 0.5
    flag_m = pred(w, Xm[40_000:]) > th; flag_n = pred(w, Xn) > th
    prec_m = ym[40_000:][flag_m].mean(); prec_n = yn[flag_n].mean()
    # domain classifier: can x tell the two regions apart?
    Xd = np.r_[Xm[:20_000], Xn[:20_000]]; yd = np.r_[np.zeros(20_000), np.ones(20_000)]
    wd = fit(Xd, yd); dp = pred(wd, Xd)
    # importance weights for metro rows, then reweighted metro precision on the flagged rows
    pm = pred(wd, Xm[40_000:]); wgt = pm / (1 - pm); wgt = np.clip(wgt, 0, 20)
    prec_rw = (wgt[flag_m] * ym[40_000:][flag_m]).sum() / wgt[flag_m].sum()
    print(f"{name:34} metro {prec_m:.1%}  new {prec_n:.1%}  metro reweighted to new covariates {prec_rw:.1%}")
    return prec_m, prec_n, prec_rw

a = diagnose("A covariate shift only", -1.0, (1.0, 0.0))
b = diagnose("B different relationship", 0.0, (0.85, -0.25))
# A: reweighting explains most of the new precision; B: reweighting does not
gap_a = abs(a[2] - a[1]); gap_b = abs(b[2] - b[1])
print(f"unexplained gap after reweighting: A {gap_a:.3f}, B {gap_b:.3f}")
assert gap_a < 0.03 and gap_b > 0.10

# Fix options for world B, using a small labelled sample from the new region (2,000 rows)
Xm, ym, Xn, yn = LAST
def logloss(y, p): p = np.clip(p, 1e-6, 1 - 1e-6); return -(y * np.log(p) + (1 - y) * np.log(1 - p)).mean()
Xn_tr, yn_tr, Xn_te, yn_te = Xn[:2000], yn[:2000], Xn[2000:], yn[2000:]
w_metro = fit(Xm, ym)
w_region = fit(np.c_[np.r_[Xm, Xn_tr], np.r_[np.zeros(len(Xm)), np.ones(2000)]], np.r_[ym, yn_tr])   # region flag
w_newonly = fit(Xn_tr, yn_tr)
w_new200 = fit(Xn_tr[:200], yn_tr[:200])
res = {
    "metro model as is": logloss(yn_te, pred(w_metro, Xn_te)),
    "metro + region flag (2,000 new rows)": logloss(yn_te, pred(w_region, np.c_[Xn_te, np.ones(len(Xn_te))])),
    "new-region only, 2,000 rows": logloss(yn_te, pred(w_newonly, Xn_te)),
    "new-region only, 200 rows": logloss(yn_te, pred(w_new200, Xn_te)),
}
for k, v in res.items(): print(f"  log loss on new region, {k:38} {v:.4f}")
assert res["metro + region flag (2,000 new rows)"] < res["metro model as is"]
assert res["new-region only, 2,000 rows"] < res["metro model as is"]
assert res["new-region only, 200 rows"] > res["metro model as is"]   # too few rows: worse than the metro model
