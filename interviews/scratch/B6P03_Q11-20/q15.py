# Q15: target-mean imputation computed before the split leaks the label (illustrative simulation)
import numpy as np
from scipy.stats import rankdata
rng = np.random.default_rng(15)
def auc(s, y):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)
N, CITIES = 20_000, 2_000                   # about 10 rows per city
city = rng.integers(0, CITIES, N)
y = (rng.random(N) < 0.10).astype(int)      # label is pure noise: NO real signal in any column
missing = rng.random(N) < 0.60               # feature missing in 60% of rows
test = rng.random(N) < 0.30

def city_target_mean(idx_fit, idx_apply):
    s = np.bincount(city[idx_fit], weights=y[idx_fit], minlength=CITIES)
    c = np.bincount(city[idx_fit], minlength=CITIES)
    g = y[idx_fit].mean()
    m = np.where(c > 0, s / np.maximum(c, 1), g)
    return m[city[idx_apply]]

allrows = np.arange(N)
leaky = city_target_mean(allrows, allrows)                  # whole data, before the split
tr, te = np.flatnonzero(~test), np.flatnonzero(test)
clean = city_target_mean(tr, te)                            # train rows only
m_te = missing[te]
a_leaky = auc(leaky[te][m_te], y[te][m_te])
a_clean = auc(clean[m_te], y[te][m_te])
print(f"test rows with a filled value: {m_te.sum()}")
print(f"AUC of the filled value on a label with NO signal: leaky {a_leaky:.3f}   train-only fill {a_clean:.3f}")
assert a_leaky > 0.58 and abs(a_clean - 0.5) < 0.05
# permutation proof: shuffle the labels, redo the leaky fill; AUC stays high -> the fill is reading y
y_real = y.copy()
aucs = []
for _ in range(5):
    y[:] = rng.permutation(y_real)
    lk = city_target_mean(allrows, allrows)
    aucs.append(auc(lk[te][m_te], y[te][m_te]))
print("leaky AUC after shuffling labels (5 shuffles):", [round(float(a), 3) for a in aucs])
assert min(aucs) > 0.58
# why: a row's own label sits inside its city mean.  Own-label share = 1 / rows in city
n_city = np.bincount(city, minlength=CITIES)
print(f"median rows per city {np.median(n_city):.0f}; own label is {1 / np.median(n_city):.0%} of that city's mean")
# the right setup: fit the fill inside each training fold, with out-of-fold means for training rows
folds = rng.integers(0, 5, len(tr)); oof = np.zeros(len(tr))
for k in range(5):
    fit_idx, app_idx = tr[folds != k], tr[folds == k]
    oof[folds == k] = city_target_mean(fit_idx, app_idx)
a_oof = auc(oof[missing[tr]], y[tr][missing[tr]])
print(f"out-of-fold fill on training rows: AUC {a_oof:.3f}  (honest, close to 0.5)")
assert abs(a_oof - 0.5) < 0.05
