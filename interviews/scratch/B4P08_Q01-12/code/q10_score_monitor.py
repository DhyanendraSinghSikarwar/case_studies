import numpy as np
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(4)

def psi(ref, cur, bins=10, eps=1e-4):
    e = np.quantile(ref, np.linspace(0, 1, bins + 1)); e[0], e[-1] = -np.inf, np.inf
    r = np.clip(np.histogram(ref, e)[0] / len(ref), eps, None)
    c = np.clip(np.histogram(cur, e)[0] / len(cur), eps, None)
    return float(np.sum((c - r) * np.log(c / r)))

def make(n):
    X = rng.normal(0, 1, (n, 3))
    p = 1 / (1 + np.exp(-(1.5 * X[:, 0] + 1.0 * X[:, 1] + 0.5 * X[:, 2] - 1.6)))
    return X, (rng.random(n) < p).astype(int)

Xtr, ytr = make(30000)
v1 = LogisticRegression().fit(Xtr, ytr)
v2 = LogisticRegression(class_weight="balanced").fit(Xtr, ytr)       # the "new model" in event C
Xref, yref = make(20000)
ref_score = v1.predict_proba(Xref)[:, 1]
print(f"reference: positive rate at 0.5 = {(ref_score >= 0.5).mean():.3f}, true prevalence = {yref.mean():.3f}")

Xn, yn = make(20000)
Xa = Xn.copy(); Xa[:, 0] = 0.0                                        # A: feature 0 outage, filled with 0
Xp, yp = make(80000)
keep = (yp == 1) | (rng.random(len(yp)) < 0.35)                       # B: positives become more common
Xb = Xp[keep][:20000]
events = {
    "no event":            dict(X=Xn, live=v1.predict_proba(Xn)[:, 1], tag="v1"),
    "A feature outage":    dict(X=Xa, live=v1.predict_proba(Xa)[:, 1], tag="v1"),
    "B prevalence rise":   dict(X=Xb, live=v1.predict_proba(Xb)[:, 1], tag="v1"),
    "C model swap to v2":  dict(X=Xn, live=v2.predict_proba(Xn)[:, 1], tag="v2"),
}
print(f"{'event':<20}{'score PSI':>10}{'pos rate':>10}{'max feat PSI':>14}{'replay-v1 PSI':>15}{'model tag':>11}")
for name, e in events.items():
    s_psi = psi(ref_score, e["live"])
    pos = (e["live"] >= 0.5).mean()
    f_psi = max(psi(Xref[:, j], e["X"][:, j]) for j in range(3))
    replay = psi(ref_score, v1.predict_proba(e["X"])[:, 1])     # old model on today's inputs
    print(f"{name:<20}{s_psi:10.3f}{pos:10.3f}{f_psi:14.3f}{replay:15.3f}{e['tag']:>11}")
