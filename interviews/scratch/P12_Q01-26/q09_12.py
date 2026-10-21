import numpy as np, pandas as pd
rng = np.random.default_rng(0)

print("=== Q9 ===")
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score, average_precision_score
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as IPipe
from sklearn.datasets import make_classification
X, y = make_classification(n_samples=4000, n_features=20, n_informative=3, weights=[0.98], flip_y=0.02, random_state=0)
print("positive rate", y.mean().round(3))
print("always-negative accuracy:", round(accuracy_score(y, np.zeros_like(y)), 3))
# BUGGY: SMOTE on everything, then CV
Xs, ys = SMOTE(random_state=0).fit_resample(X, y)
rf = RandomForestClassifier(100, random_state=0, n_jobs=1)
leaky = cross_val_score(rf, Xs, ys, cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="average_precision").mean()
# FIXED: SMOTE inside pipeline (only resamples train folds)
pipe = IPipe([("smote", SMOTE(random_state=0)), ("rf", RandomForestClassifier(100, random_state=0))])
fixed = cross_val_score(pipe, X, y, cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring="average_precision").mean()
print("AP SMOTE-before-CV:", leaky.round(3), " AP SMOTE-inside-CV:", fixed.round(3), " baseline (prevalence):", y.mean().round(3))

print("=== Q10 ===")
ev = pd.DataFrame({
    "cust": rng.integers(0, 3, 40),
    "ts": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 60 * 24, 40), unit="h"),
    "amt": rng.integers(10, 100, 40).astype(float)}).sort_values(["cust", "ts"]).reset_index(drop=True)
def add_roll(df, win):
    out = []
    for c, g in df.groupby("cust"):
        r = g.set_index("ts")["amt"].rolling(win, closed="left")   # excludes current row
        out.append(pd.DataFrame({"mean_" + win: r.mean().values, "cnt_" + win: r.count().values}, index=g.index))
    return pd.concat(out)
feat = ev.join(add_roll(ev, "7D")).join(add_roll(ev, "30D"))
print(feat.head(8).round(1).to_string())
# check: row i feature must equal manual mean of strictly earlier events in last 7 days
i = 6; row = feat.loc[i]
past = ev[(ev.cust == row.cust) & (ev.ts < row.ts) & (ev.ts >= row.ts - pd.Timedelta("7D"))]
print("manual:", past.amt.mean(), len(past), "feature:", row["mean_7D"], row["cnt_7D"])
# simpler variant: same with shift(1) for event-count windows
ev["prev3_mean"] = ev.groupby("cust")["amt"].transform(lambda s: s.shift(1).rolling(3).mean())

print("=== Q11 ===")
from sklearn.model_selection import KFold, GroupKFold, TimeSeriesSplit, StratifiedGroupKFold
n_users, per = 200, 20
uid = np.repeat(np.arange(n_users), per)
user_effect = rng.normal(size=(n_users, 5)).repeat(per, axis=0)
Xg = user_effect + 0.1 * rng.normal(size=(n_users * per, 5))
user_label = rng.integers(0, 2, n_users)  # label depends on user only (pure noise wrt features, but features identify user)
yg = user_label[uid]
rf = RandomForestClassifier(100, random_state=0, n_jobs=1)
naive = cross_val_score(rf, Xg, yg, cv=KFold(5, shuffle=True, random_state=0), scoring="roc_auc").mean()
grouped = cross_val_score(rf, Xg, yg, groups=uid, cv=GroupKFold(5), scoring="roc_auc").mean()
sgk = cross_val_score(rf, Xg, yg, groups=uid, cv=StratifiedGroupKFold(5, shuffle=True, random_state=0), scoring="roc_auc").mean()
print("naive KFold AUC:", naive.round(3), " GroupKFold AUC:", grouped.round(3), " StratifiedGroupKFold:", sgk.round(3))
# time order: trend + shuffled KFold
T = 600
t = np.arange(T)
Xt = np.c_[t + rng.normal(0, 3, T), rng.normal(size=T)]
yt = (t / T + 0.3 * rng.normal(size=T)) + 0  # drifting target
from sklearn.ensemble import RandomForestRegressor
rr = RandomForestRegressor(100, random_state=0, n_jobs=1)
s1 = cross_val_score(rr, Xt, yt, cv=KFold(5, shuffle=True, random_state=0), scoring="r2").mean()
s2 = cross_val_score(rr, Xt, yt, cv=TimeSeriesSplit(5), scoring="r2").mean()
print("shuffled KFold R2:", s1.round(3), " TimeSeriesSplit R2:", s2.round(3))

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
