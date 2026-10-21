import numpy as np
from sklearn.metrics import roc_auc_score, average_precision_score

def _curve(y, s):
    """Cumulative TP/FP at each DISTINCT score threshold (ties collapse to one point)."""
    y = np.asarray(y); s = np.asarray(s, dtype=float)
    order = np.argsort(-s, kind="mergesort")
    s, y = s[order], y[order]
    last = np.r_[np.where(np.diff(s))[0], len(s) - 1]     # last index of each tie group
    tp = np.cumsum(y)[last]
    fp = (last + 1) - tp
    return tp, fp

def auc_roc(y, s):
    tp, fp = _curve(y, s)
    tpr = np.r_[0, tp / tp[-1]]; fpr = np.r_[0, fp / fp[-1]]
    return np.trapezoid(tpr, fpr)          # ties -> diagonal segment = 0.5 credit

def avg_precision(y, s):
    tp, fp = _curve(y, s)
    prec = tp / (tp + fp); rec = tp / tp[-1]
    return np.sum(np.diff(np.r_[0, rec]) * prec)   # step-wise sum, same as sklearn

rng = np.random.default_rng(0)
y = rng.integers(0, 2, 1000)
s = np.round(rng.normal(y * 0.8, 1), 1)            # rounding creates many ties
print(len(np.unique(s)), "distinct scores for 1000 rows")
print(auc_roc(y, s), roc_auc_score(y, s))
print(avg_precision(y, s), average_precision_score(y, s))
assert np.isclose(auc_roc(y, s), roc_auc_score(y, s))
assert np.isclose(avg_precision(y, s), average_precision_score(y, s))
# rank-based AUC (Mann-Whitney) as a cross-check
from scipy.stats import rankdata
r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
print((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
