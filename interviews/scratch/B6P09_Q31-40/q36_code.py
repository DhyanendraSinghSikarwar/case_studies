import numpy as np

# prompt arithmetic
adm, t0, t1 = 20000, 1000, 800
print("transfer rate", t0 / adm, "->", t1 / adm, "| absolute", round((t0 - t1) / adm, 3), "| relative", (t0 - t1) / t0)
assert t0 / adm == 0.05 and t1 / adm == 0.04 and (t0 - t1) / t0 == 0.2

# Illustrative hand-check: assume 1,000 alerts per 20,000 admissions (the prompt gives PPV, not volume)
V = 1000
tp_replay, tp_live = 0.30 * V, 0.18 * V
print("true positives among alerts: replay", tp_replay, "live", tp_live, "| missing", tp_replay - tp_live)
assert tp_replay == 300 and tp_live == 180 and tp_replay - tp_live == 120
print("recall vs transfers: replay", tp_replay / t0, "live", tp_live / t1)
assert tp_replay / t0 == 0.3 and tp_live / t1 == 0.225
# if alerts prevented X transfers among alerted patients and nothing else changed: X = 120 of the 200 fewer transfers
print("transfers fewer in total", t0 - t1, "| of which alert-saved if PPV drop is all treatment", tp_replay - tp_live, "| the other", (t0 - t1) - (tp_replay - tp_live), "from other causes or non-alerted")
assert (t0 - t1) - (tp_replay - tp_live) == 80

# prevalence alone (same sensitivity 30% and same false-positive rate as replay)
sens = tp_replay / t0
fpr = (V - tp_replay) / (adm - t0)
tp_p = sens * t1; fp_p = fpr * (adm - t1)
print("prevalence-only PPV", round(tp_p / (tp_p + fp_p), 3), "| alert volume would be", round(tp_p + fp_p))
assert round(tp_p / (tp_p + fp_p), 3) == 0.253

# simulation: alerts change outcomes, so the label (ICU transfer) understates true deterioration
rng = np.random.default_rng(36)
def make(n):
    r = rng.beta(1.0, 19, n)                       # latent risk of deterioration w/o intervention
    X = np.c_[np.log(r / (1 - r)) + rng.normal(0, 1.0, n), rng.normal(size=n)]   # noisy vital-sign score + noise
    return r, X
def fit(X, y, it=30):
    A = np.c_[np.ones(len(X)), X]; w = np.zeros(3)
    for _ in range(it):
        mu = 1 / (1 + np.exp(-(A @ w))); W = mu * (1 - mu)
        w += np.linalg.solve(A.T @ (A * W[:, None]) + 1e-6 * np.eye(3), A.T @ (y - mu))
    return w
score = lambda w, X: np.c_[np.ones(len(X)), X] @ w
n = 200_000
r0, X0 = make(n); y0 = (rng.random(n) < r0).astype(float)          # pre-launch labels
w1 = fit(X0, y0)
rep = 0.05
thr = np.quantile(score(w1, X0), 1 - rep)
alert0 = score(w1, X0) >= thr
print("replay: alert share", round(alert0.mean(), 3), "| PPV", round(y0[alert0].mean(), 3), "| prevalence", round(y0.mean(), 4))
eff = 0.45                                         # invented: intervention cuts transfer risk 45% (relative) when alerted
r1, X1 = make(n); a1 = score(w1, X1) >= thr
p1 = r1 * np.where(a1, 1 - eff, 1.0)
y1 = (rng.random(n) < p1).astype(float)
print("live  : alert share", round(a1.mean(), 3), "| PPV", round(y1[a1].mean(), 3), "| prevalence", round(y1.mean(), 4))
tp_live_ = y1[a1].mean()
print("true deterioration rate among alerted (untreated risk)", round(r1[a1].mean(), 3))
assert y1[a1].mean() < y0[alert0].mean() and y1.mean() < y0.mean()
# naive retrain on live labels: the model learns "alerted-looking patients rarely transfer"
w2 = fit(X1, y1)
sig = lambda z: 1 / (1 + np.exp(-z))
p_cut = sig(thr)                                   # the probability cut the original model used
share_orig = (sig(score(w1, X1)) >= p_cut).mean()
share_naive = (sig(score(w2, X1)) >= p_cut).mean()
print("alert share at the same probability cut: original", round(share_orig, 4), "| naive retrain on live labels", round(share_naive, 4))
print("mean predicted risk: original", round(sig(score(w1, X1)).mean(), 4), "| naive retrain", round(sig(score(w2, X1)).mean(), 4), "| mean untreated risk", round(r1.mean(), 4), "| observed live rate", round(y1.mean(), 4))
print("coefficients original", np.round(w1, 3), "naive retrain", np.round(w2, 3))
assert share_naive < share_orig
assert round(y0[alert0].mean(), 3) == 0.12 and round(y1[a1].mean(), 3) == 0.072
assert round(share_orig, 4) == 0.0512 and round(share_naive, 4) == 0.0244
