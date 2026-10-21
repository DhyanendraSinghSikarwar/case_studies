import numpy as np, pandas as pd
rng = np.random.default_rng(0)
print("=== Q12 ===")
from sklearn.model_selection import KFold
from sklearn.metrics import roc_auc_score
n = 3000
cat = rng.integers(0, 1500, n)     # high-cardinality, ~2 rows per level, pure noise
yy = rng.integers(0, 2, n)
df = pd.DataFrame({"cat": cat, "y": yy})
def te_fit(train, m=10):
    prior = train.y.mean()
    s = train.groupby("cat").y.agg(["sum", "count"])
    enc = (s["sum"] + m * prior) / (s["count"] + m)
    return enc, prior
def te_apply(s, enc, prior): return s.map(enc).fillna(prior)
def te_oof(train, k=5, m=10, seed=0):
    oof = pd.Series(np.nan, index=train.index)
    for tr_i, va_i in KFold(k, shuffle=True, random_state=seed).split(train):
        enc, prior = te_fit(train.iloc[tr_i], m)
        oof.iloc[va_i] = te_apply(train.iloc[va_i]["cat"], enc, prior).values
    return oof
tr, te = df.iloc[:2000].copy(), df.iloc[2000:].copy()
# naive (m tiny = almost raw mean)
enc, prior = te_fit(tr, m=0.001)
naive_tr = te_apply(tr.cat, enc, prior); naive_te = te_apply(te.cat, enc, prior)
print("NAIVE  train AUC:", round(roc_auc_score(tr.y, naive_tr), 3), " test AUC:", round(roc_auc_score(te.y, naive_te), 3))
oof = te_oof(tr, m=10)
enc, prior = te_fit(tr, m=10)
print("OOF    train AUC:", round(roc_auc_score(tr.y, oof), 3), " test AUC:", round(roc_auc_score(te.y, te_apply(te.cat, enc, prior)), 3))
