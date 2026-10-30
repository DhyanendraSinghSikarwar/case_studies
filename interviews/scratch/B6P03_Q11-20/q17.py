# Q17: SMOTE vs class weights vs undersampling on 0.5% positives (illustrative simulation)
import numpy as np
rng = np.random.default_rng(17)
def sig(z): return 1 / (1 + np.exp(-z))
def fit(X, y, wt=None, it=25, l2=1.0):
    wt = np.ones(len(y)) if wt is None else wt
    w = np.zeros(X.shape[1])
    for _ in range(it):
        p = sig(X @ w); H = (X * (wt * p * (1 - p))[:, None]).T @ X + l2 * np.eye(len(w))
        w += np.linalg.solve(H, X.T @ (wt * (y - p)) - l2 * w)
    return w
def avg_precision(s, y):
    o = np.argsort(-s); yy = y[o]; tp = np.cumsum(yy)
    return float((tp / np.arange(1, len(yy) + 1))[yy == 1].mean())
D = 10
beta = np.r_[1.2, 0.8, 0.5, np.zeros(D - 3)]
def make(n, pos):
    X = rng.normal(size=(n, D)); X[:pos] += 1.0 * beta  # first rows are positives, shifted
    y = np.zeros(n); y[:pos] = 1
    return X, y
def smote(Xp, n_new, k=5):
    d = ((Xp[:, None, :] - Xp[None, :, :]) ** 2).sum(-1); np.fill_diagonal(d, np.inf)
    nn = np.argsort(d, 1)[:, :k]
    i = rng.integers(0, len(Xp), n_new); j = nn[i, rng.integers(0, k, n_new)]
    t = rng.random((n_new, 1)); return Xp[i] + t * (Xp[j] - Xp[i])
res = {k: [] for k in ("plain", "class weight", "undersample 1:10", "SMOTE to 1:1")}
for seed in range(8):
    Xtr, ytr = make(60_000, 300); Xte, yte = make(60_000, 300)
    A = lambda X: np.c_[np.ones(len(X)), X]
    res["plain"].append(avg_precision(A(Xte) @ fit(A(Xtr), ytr), yte))
    wt = np.where(ytr == 1, 199.0, 1.0)
    res["class weight"].append(avg_precision(A(Xte) @ fit(A(Xtr), ytr, wt), yte))
    neg = np.flatnonzero(ytr == 0); keep = np.r_[np.arange(300), rng.choice(neg, 3_000, replace=False)]
    res["undersample 1:10"].append(avg_precision(A(Xte) @ fit(A(Xtr[keep]), ytr[keep]), yte))
    Xs = np.r_[Xtr, smote(Xtr[:300], 59_400)]; ys = np.r_[ytr, np.ones(59_400)]
    res["SMOTE to 1:1"].append(avg_precision(A(Xte) @ fit(A(Xs), ys), yte))
print("test positive rate 0.50%, so a no-skill average precision is about 0.005")
print(f"{'method':18} {'mean AP':>8} {'sd over 8 seeds':>16} {'train rows':>11}")
rows = {"plain": 60_000, "class weight": 60_000, "undersample 1:10": 3_300, "SMOTE to 1:1": 119_400}
for k, v in res.items(): print(f"{k:18} {np.mean(v):8.4f} {np.std(v, ddof=1):16.4f} {rows[k]:11,d}")
# time arithmetic from the prompt (assume time grows linearly with rows; an assumption, not a measurement)
base_h = 2.0
for k in ("undersample 1:10", "SMOTE to 1:1"):
    print(f"{k}: about {base_h * rows[k] / 60_000 * 60:.0f} minutes if time is linear in rows")
assert round(base_h * 3_300 / 60_000 * 60) == 7 and round(base_h * 119_400 / 60_000) == 4
assert 60_000 * 0.005 == 300
m = {k: np.mean(v) for k, v in res.items()}
assert min(m.values()) > 10 * 0.005
spread = max(m.values()) - min(m.values()); sd = np.mean([np.std(v, ddof=1) for v in res.values()])
print(f'spread of method means {spread:.4f} versus seed-to-seed sd {sd:.4f}')
