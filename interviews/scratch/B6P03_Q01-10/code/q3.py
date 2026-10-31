# Q3 ROC-AUC 0.97 vs PR-AUC 0.18 at 0.2% positives (illustrative simulation)
import numpy as np
from scipy.stats import rankdata, norm

rng = np.random.default_rng(3)
n, prev = 1_000_000, 0.002
y = (rng.random(n) < prev).astype(int)
pos = int(y.sum())
sg = 1.3                                         # negatives are more spread out than positives
d = norm.ppf(0.97) * (1 + sg**2) ** 0.5          # shift that gives ROC-AUC = 0.97
s = rng.normal(size=n) * np.where(y == 1, 1.0, sg) + d * y

def roc_auc(y, s):
    r = rankdata(s); n1 = y.sum(); n0 = len(y) - n1
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)

def avg_precision(y, s):
    o = np.argsort(-s); yy = y[o]
    tp = np.cumsum(yy); k = np.arange(1, len(yy) + 1)
    return (tp / k)[yy == 1].mean()                # mean precision at each true positive

auc = roc_auc(y, s); ap = avg_precision(y, s)
print(f"positives={pos} ({pos/n:.2%}); ROC-AUC={auc:.3f}; PR-AUC (average precision)={ap:.3f}; no-skill PR-AUC={prev}")
assert 0.965 < auc < 0.975 and 0.10 < ap < 0.30
assert ap / prev > 50                              # far better than random, but far from 0.97

# Why: at recall 0.80 the false-positive rate looks tiny, yet false alarms swamp the hits
thr = np.quantile(s[y == 1], 0.20)                 # keeps 80% of positives
flag = s >= thr
tp = (flag & (y == 1)).sum(); fp = (flag & (y == 0)).sum()
fpr = fp / (y == 0).sum(); prec = tp / (tp + fp)
print(f"at recall 0.80: FPR={fpr:.3f}, flagged={flag.sum()}, TP={tp}, FP={fp}, precision={prec:.3f}")
assert fpr < 0.06 and prec < 0.05

# Same scores shape, but 20% prevalence: ROC-AUC unchanged, PR-AUC much higher
y2 = (rng.random(200_000) < 0.2).astype(int); s2 = rng.normal(size=200_000) * np.where(y2 == 1, 1.0, sg) + d * y2
print(f"prevalence 20%: ROC-AUC={roc_auc(y2,s2):.3f}, PR-AUC={avg_precision(y2,s2):.3f}")
assert abs(roc_auc(y2, s2) - auc) < 0.01 and avg_precision(y2, s2) > 0.8

# Business view: a review queue of 1,000 transactions out of 1,000,000
top = np.argsort(-s)[:1000]
print(f"top 1,000 flagged: {y[top].sum()} true positives (precision {y[top].mean():.3f}), recall {y[top].sum()/pos:.3f}; random queue would find {1000*prev:.0f}")
assert y[top].sum() > 100
