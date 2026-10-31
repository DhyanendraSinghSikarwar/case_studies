# Q1: green job, worse model. All numbers invented / illustrative.
import math
import numpy as np

# 1) the prompt's numbers
auc_prod, auc_new = 0.812, 0.771
drop = round(auc_prod - auc_new, 3)
rows_usual, rows_read = 5_000_000, 4_200_000
missing = rows_usual - rows_read
assert drop == 0.041 and missing == 800_000 and missing / rows_usual == 0.16

# 2) is a 0.041 AUC drop on 20,000 holdout rows more than noise?
# Hanley-McNeil standard error of one AUC; ASSUMPTION: 10% positives (2,000 pos, 18,000 neg).
def hm_se(a, n_pos, n_neg):
    q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
    v = (a*(1-a) + (n_pos-1)*(q1-a*a) + (n_neg-1)*(q2-a*a)) / (n_pos*n_neg)
    return math.sqrt(v)
se = hm_se(0.812, 2000, 18000)
z_conservative = drop / (math.sqrt(2) * se)   # ignores that both models score the SAME rows (paired), so it is conservative
print(f"HM SE of one AUC = {se:.4f}; conservative z for the drop = {z_conservative:.1f}")
assert z_conservative > 4          # a real drop, not holdout noise (under the 10% positives assumption)

# 3) gates, written as code (thresholds are illustrative policy, not a standard)
def gates(rows, usual, auc_new, auc_prod, row_tol=0.05, auc_margin=0.005):
    fails = []
    if abs(rows - usual) / usual > row_tol: fails.append("row_count")
    if auc_new < auc_prod - auc_margin: fails.append("auc_noninferiority")
    return fails
f = gates(rows_read, rows_usual, auc_new, auc_prod)
print("gates failed:", f)
assert f == ["row_count", "auc_noninferiority"]
assert gates(4_900_000, rows_usual, 0.810, auc_prod) == []     # a normal night passes both

# 4) exposure: how many requests the worse model serves (invented traffic 50 req/s)
rps = 50
auto_deploy_noticed_after_h = 7                      # deploy 02:00, human notices 09:00
exposed = rps * auto_deploy_noticed_after_h * 3600
canary_exposed = int(rps * 0.05 * 10 * 60)           # 5% canary, auto rollback after 10 min
print("requests on bad model: no gate =", exposed, "| 5% canary + 10-min auto rollback =", canary_exposed)
assert exposed == 1_260_000 and canary_exposed == 1_500

# 5) does "16% fewer rows" alone explain it? Simulation, seeded. Logistic model by Newton steps.
rng = np.random.default_rng(6)
K, n = 25, 250_000                                    # 25 segments of ~4% each
seg = rng.integers(0, K, n)
base = rng.normal(0, 1.0, K)
X = rng.normal(size=(n, 4))
logit = base[seg] + X @ np.array([0.8, -0.5, 0.3, 0.2]) - 1.5
y = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(float)
def design(seg, X): return np.hstack([np.eye(K)[seg], X])
def fit(D, y, it=12):
    w = np.zeros(D.shape[1])
    for _ in range(it):
        p = 1 / (1 + np.exp(-D @ w)); g = D.T @ (p - y) + 1e-3 * w
        H = (D * (p * (1 - p))[:, None]).T @ D + 1e-3 * np.eye(D.shape[1])
        w -= np.linalg.solve(H, g)
    return w
def auc(s, y):
    r = s.argsort().argsort() + 1; n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
hold = np.arange(n) >= 230_000                         # last 20,000 rows are the holdout
tr = ~hold
Dh = design(seg[hold], X[hold])
auc_full = auc(Dh @ fit(design(seg[tr], X[tr]), y[tr]), y[hold])
keep_rand = tr & (rng.random(n) > 0.16)                # drop 16% at random
auc_rand = auc(Dh @ fit(design(seg[keep_rand], X[keep_rand]), y[keep_rand]), y[hold])
gone = np.argsort(-np.abs(base))[:4]                   # drop 4 segments (the 4 most extreme): ~16% of rows, not random
keep_seg = tr & ~np.isin(seg, gone)
auc_seg = auc(Dh @ fit(design(seg[keep_seg], X[keep_seg]), y[keep_seg]), y[hold])
lost = 1 - keep_seg.sum() / tr.sum()
print(f"AUC full={auc_full:.3f} | 16% random rows dropped={auc_rand:.3f} | 4 segments ({lost:.0%} of rows) dropped={auc_seg:.3f}")
assert auc_full - auc_rand < 0.005                     # random loss barely matters
assert auc_full - auc_seg > 5 * (auc_full - auc_rand)  # a missing slice hurts far more
print("lesson: the row-count gap points to a missing slice, so find WHICH slice is missing")
