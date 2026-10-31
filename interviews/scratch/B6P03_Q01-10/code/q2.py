# Q2 SMOTE before the split: synthetic points leak into the test set (illustrative data)
import numpy as np
from scipy.spatial import cKDTree

rng = np.random.default_rng(11)
n, d = 10_000, 6
y = np.zeros(n, int); y[:500] = 1                      # 500 positives = 5%
rng.shuffle(y)
assert y.sum() == 500 and y.mean() == 0.05
X = rng.normal(size=(n, d)); X[y == 1] += 0.5          # weak signal, classes overlap

def smote(X, y, rng, k=5):
    """Oversample class 1 to a 50/50 mix: new point = a + u*(neighbour - a), neighbour among k nearest positives."""
    P = X[y == 1]; need = (y == 0).sum() - len(P)
    nn = cKDTree(P).query(P, k + 1)[1][:, 1:]
    i = rng.integers(0, len(P), need); j = nn[i, rng.integers(0, k, need)]
    u = rng.random((need, 1))
    Xs = P[i] + u * (P[j] - P[i])
    return np.vstack([X, Xs]), np.r_[y, np.ones(need, int)]

def one_nn_recall(Xtr, ytr, Xte, yte):
    pred = ytr[cKDTree(Xtr).query(Xte, 1)[1]]            # 1-nearest-neighbour: memorises its neighbourhood
    return pred[yte == 1].mean(), pred[yte == 0].mean()

# WRONG: SMOTE the whole table, then split
Xb, yb = smote(X, y, rng)
assert abs(yb.mean() - 0.5) < 1e-9 and len(yb) == 19_000
idx = rng.permutation(len(yb)); cut = int(0.8 * len(yb))
tr, te = idx[:cut], idx[cut:]
r_wrong, fpr_wrong = one_nn_recall(Xb[tr], yb[tr], Xb[te], yb[te])
n_syn_in_test = (te >= n).sum()
print(f"WRONG: test rows={len(te)}, synthetic positives in test={n_syn_in_test} ({n_syn_in_test/(yb[te]==1).sum():.0%} of test positives)")
print(f"WRONG: test recall = {r_wrong:.3f}")

# RIGHT: split the real rows first (stratified), SMOTE the training part only, test on real untouched rows
idx1 = np.flatnonzero(y == 1); idx0 = np.flatnonzero(y == 0)
rng.shuffle(idx1); rng.shuffle(idx0)
te_real = np.r_[idx1[:100], idx0[:1900]]; tr_real = np.r_[idx1[100:], idx0[1900:]]
assert len(te_real) == 2000 and y[te_real].mean() == 0.05
Xtr, ytr = smote(X[tr_real], y[tr_real], rng)
r_right, fpr_right = one_nn_recall(Xtr, ytr, X[te_real], y[te_real])
print(f"RIGHT: real test rows={len(te_real)}, positives={y[te_real].sum()}, test recall = {r_right:.3f}, false-positive rate = {fpr_right:.3f}")
assert r_wrong > 0.85 and r_right < r_wrong - 0.3
