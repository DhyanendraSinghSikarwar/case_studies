# Q31: model extraction demo. Victim = logistic regression on synthetic data. Seeded. Sandbox numbers only.
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
rng = np.random.default_rng(31)
D = 20
w = rng.normal(0, 1, D); b = 0.3
Xtr = rng.normal(0, 1, (5000, D)); ytr = (rng.random(5000) < 1 / (1 + np.exp(-(Xtr @ w + b)))).astype(int)
victim = LogisticRegression(max_iter=1000).fit(Xtr, ytr)
def api(X, mode):                                   # what a partner sees
    p = victim.predict_proba(X)[:, 1]
    if mode == "full": return p
    if mode == "round1": return np.round(p, 1)
    if mode == "bucket3": return np.digitize(p, [0.33, 0.66]) / 2.0          # low / mid / high
    if mode == "label": return (p >= 0.5).astype(float)
Xtest = rng.normal(0, 1, (5000, D)); vlab = victim.predict(Xtest)
def attack(mode, nq):
    X = rng.normal(0, 1, (nq, D)); y = api(X, mode)
    if mode == "full":                              # invert the sigmoid: exact linear system
        z = np.log(np.clip(y, 1e-9, 1 - 1e-9) / np.clip(1 - y, 1e-9, 1)); s = LinearRegression().fit(X, z)
        wh = s.coef_; pred = (Xtest @ wh + s.intercept_ > 0).astype(int)
    else:
        yl = (y >= 0.5).astype(int)
        if yl.min() == yl.max(): return float("nan"), float("nan")
        s = LogisticRegression(max_iter=2000, C=100).fit(X, yl); wh = s.coef_[0]; pred = s.predict(Xtest)
    cos = float(wh @ victim.coef_[0] / (np.linalg.norm(wh) * np.linalg.norm(victim.coef_[0])))
    return float((pred == vlab).mean()), cos
print(f"{'output given to partner':<26}{'queries':>8}{'agreement':>10}{'weight cosine':>14}")
for mode in ("full", "round1", "bucket3", "label"):
    for nq in (20000, 200, 25):
        a, c = attack(mode, nq); print(f"{mode:<26}{nq:>8}{a:>10.3f}{c:>14.3f}")
