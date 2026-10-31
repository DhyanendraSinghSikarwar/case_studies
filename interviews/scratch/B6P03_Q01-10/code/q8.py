# Q8 five rows per customer, random row split: same customers in train and test (illustrative simulation)
import numpy as np
from scipy.spatial import cKDTree
from scipy.stats import rankdata

rng = np.random.default_rng(8)
n_cust = 8_000
rows_per = 1 + rng.poisson(4, n_cust)                 # about five rows per customer
cust = np.repeat(np.arange(n_cust), rows_per)
n = len(cust)
print(f"rows={n}, customers={n_cust}, rows per customer={n/n_cust:.2f}")
assert abs(n / n_cust - 5) < 0.1

# Customer-level traits (stable across rows) and a customer-level outcome tendency; weak true row-level signal
d = 5
trait = rng.normal(size=(n_cust, d))
u = trait @ np.array([0.8, 0.6, 0.0, 0.0, 0.0]) + rng.normal(scale=2.0, size=n_cust)   # partly explained by traits
X = trait[cust] + rng.normal(scale=0.10, size=(n, d))                                  # rows of one customer look alike
rowfeat = rng.normal(size=n)
y = (rng.random(n) < 1 / (1 + np.exp(-(-0.5 + 1.0 * u[cust] + 0.3 * rowfeat)))).astype(int)
X = np.c_[X, rowfeat]

def auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
def knn_scores(Xtr, ytr, Xte, k=3):
    idx = cKDTree(Xtr).query(Xte, k)[1]
    return ytr[idx].mean(axis=1)

# Confirm the cause: how many test rows have the same customer in train under a random row split?
perm = rng.permutation(n); cut = int(0.8 * n); tr, te = perm[:cut], perm[cut:]
seen = np.isin(cust[te], np.unique(cust[tr])).mean()
print(f"random row split: {seen:.1%} of test rows belong to a customer that is also in train")
assert seen > 0.9
a_row = auc(y[te], knn_scores(X[tr], y[tr], X[te]))

# Customer-only 'model': previous label average of the same customer (uses no features at all)
sums = np.bincount(cust[tr], weights=y[tr], minlength=n_cust); cnt = np.bincount(cust[tr], minlength=n_cust)
mean_y = y[tr].mean()
cust_score = (sums[cust[te]] + mean_y) / (cnt[cust[te]] + 1)
print(f"AUC of 'same customer's other labels' alone, row split: {auc(y[te], cust_score):.3f}")

# Group split: whole customers go to train or test
cperm = rng.permutation(n_cust); is_test_c = np.zeros(n_cust, bool); is_test_c[cperm[:int(0.2 * n_cust)]] = True
te_g = np.flatnonzero(is_test_c[cust]); tr_g = np.flatnonzero(~is_test_c[cust])
assert not set(cust[te_g]) & set(cust[tr_g])
a_grp = auc(y[te_g], knn_scores(X[tr_g], y[tr_g], X[te_g]))
print(f"kNN AUC: random row split={a_row:.3f}  customer-group split={a_grp:.3f}  gap={a_row-a_grp:.3f}")
assert a_row - a_grp > 0.08

# Honest number with an interval: bootstrap over test customers
sc = knn_scores(X[tr_g], y[tr_g], X[te_g]); cg = cust[te_g]; yg = y[te_g]
ucs = np.unique(cg); order = {c: np.flatnonzero(cg == c) for c in ucs}
boots = []
for _ in range(200):
    pick = rng.choice(ucs, len(ucs))
    ii = np.concatenate([order[c] for c in pick])
    boots.append(auc(yg[ii], sc[ii]))
lo, hi = np.percentile(boots, [2.5, 97.5])
print(f"honest AUC (new customers) = {a_grp:.3f}, 95% customer-bootstrap interval [{lo:.3f}, {hi:.3f}]; test customers={len(ucs)}")
assert lo < a_grp < hi
