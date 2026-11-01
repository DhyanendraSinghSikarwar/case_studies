import numpy as np
from scipy.stats import ks_2samp
from sklearn.linear_model import LogisticRegression

rng = np.random.default_rng(5)
n = 10000
PLANS = ["basic", "plus", "pro"]
# raw rows
height_m = rng.normal(1.7, 0.1, n)
plan = rng.choice(PLANS, n, p=[.5, .3, .2])
y = (rng.random(n) < 1 / (1 + np.exp(-(8 * (height_m - 1.7) + (plan == "pro") * 1.5 - (plan == "basic") * 0.8)))).astype(int)

def train_transform(h, p):          # training code: metres, plan codes by position in PLANS
    return np.c_[h, [PLANS.index(x) for x in p]]
def serve_transform(h, p):          # serving code, written separately: centimetres, codes by sorted() order
    order = sorted(PLANS)           # a different convention: codes assigned from the reversed sorted list
    return np.c_[h * 100, [order[::-1].index(x) for x in p]]

Xtr = train_transform(height_m, plan)
m = LogisticRegression(max_iter=1000).fit(Xtr, y)
h2 = rng.normal(1.7, 0.1, n); p2 = rng.choice(PLANS, n, p=[.5, .3, .2])
y2 = (rng.random(n) < 1 / (1 + np.exp(-(8 * (h2 - 1.7) + (p2 == "pro") * 1.5 - (p2 == "basic") * 0.8)))).astype(int)
good, bad = train_transform(h2, p2), serve_transform(h2, p2)
print("accuracy, correct pipeline:", round(m.score(good, y2), 3))
print("accuracy, skewed pipeline :", round(m.score(bad, y2), 3))

print("\nCheck 1: compare logged serving features with training features")
for j, name in enumerate(["height", "plan_code"]):
    d = ks_2samp(Xtr[:, j], bad[:, j]).statistic
    print(f"  {name:<10} train mean={Xtr[:, j].mean():8.2f}  serve mean={bad[:, j].mean():8.2f}  KS D={d:.3f}  ratio={bad[:, j].mean() / Xtr[:, j].mean():.2f}")
print("\nCheck 2: parity test, same raw rows through both code paths")
a, b = train_transform(h2[:5], p2[:5]), serve_transform(h2[:5], p2[:5])
print("  max abs diff per column:", np.abs(a - b).max(axis=0).round(2).tolist(), "(expect 0, 0)")
print("\nCheck 3: categorical code mapping must be identical")
print("  train mapping:", {p: PLANS.index(p) for p in PLANS})
print("  serve mapping:", {p: sorted(PLANS)[::-1].index(p) for p in PLANS})
