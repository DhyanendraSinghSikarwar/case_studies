import numpy as np, pandas as pd, time
rng = np.random.default_rng(0)

print("=== Q5 ===")
n = 200_000
df = pd.DataFrame({"amount": rng.gamma(2, 500, n), "country": rng.choice(["IN", "DE", "US"], n),
                   "is_prime": rng.random(n) < 0.3})
def slow_row(r):
    if r["amount"] > 2000: tier = "high"
    elif r["amount"] > 500: tier = "mid"
    else: tier = "low"
    rate = {"IN": 0.18, "DE": 0.19, "US": 0.07}[r["country"]]
    disc = 0.1 if r["is_prime"] else 0.0
    return pd.Series({"tier": tier, "net": r["amount"] * (1 - disc) * (1 + rate)})
sub = df.head(20_000)
t = time.perf_counter(); slow = sub.apply(slow_row, axis=1); t_slow = time.perf_counter() - t
def fast(d):
    tier = np.select([d.amount > 2000, d.amount > 500], ["high", "mid"], default="low")
    rate = d.country.map({"IN": 0.18, "DE": 0.19, "US": 0.07})
    disc = np.where(d.is_prime, 0.1, 0.0)
    return pd.DataFrame({"tier": tier, "net": d.amount * (1 - disc) * (1 + rate)}, index=d.index)
t = time.perf_counter(); f = fast(sub); t_fast = time.perf_counter() - t
print(f"apply axis=1 20k rows: {t_slow:.2f}s  vectorized: {t_fast*1000:.1f}ms  speedup~{t_slow/t_fast:.0f}x")
print((slow.tier == f.tier).all(), np.allclose(slow.net.astype(float), f.net))

print("=== Q6 ===")
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
X, y = make_classification(n_samples=300, n_features=20, random_state=0)
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=0)
sc = StandardScaler().fit(X)  # BUG
print("leaky mean of test cols (full-fit scaler):", np.abs(sc.transform(Xte).mean(0)).mean().round(3))
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(Xtr, ytr)
print("test acc (pipeline):", round(pipe.score(Xte, yte), 3))
# leakage shows up more with e.g. test being scaled with own stats shift
Xs = X.copy(); Xs[:, 0] = Xs[:, 0] * 50
print(cross_val_score(make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)), X, y, cv=5).mean().round(3))
# demonstrate the magnitude: fitting stats on full data
from sklearn.neighbors import KNeighborsClassifier
rng2 = np.random.default_rng(1)
Xn = rng2.normal(size=(60, 500)); yn = rng2.integers(0, 2, 60)
print("n/a")

print("=== Q7 ===")
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
m = 500
d = pd.DataFrame({"age": rng.normal(40, 10, m), "income": rng.lognormal(10, 0.5, m),
                  "city": rng.choice(["A", "B", "C"], m), "plan": rng.choice(["free", "pro"], m)})
yy = ((d.age > 42) ^ (d.city == "A") | (rng.random(m) < 0.1)).astype(int)
d.loc[rng.random(m) < 0.1, "age"] = np.nan
d.loc[rng.random(m) < 0.1, "city"] = np.nan
pre = ColumnTransformer([
    ("num", make_pipeline(SimpleImputer(strategy="median"), StandardScaler()), ["age", "income"]),
    ("cat", make_pipeline(SimpleImputer(strategy="most_frequent"),
                          OneHotEncoder(handle_unknown="ignore")), ["city", "plan"])])
clf = make_pipeline(pre, RandomForestClassifier(200, random_state=0))
sc = cross_val_score(clf, d, yy, cv=5, scoring="roc_auc")
print(sc.round(3), sc.mean().round(3))

print("=== Q8 ===")
g = pd.DataFrame({"team": list("aabbbc"), "sales": [10., 20, 5, 15, 40, 7]})
g["grp_mean"] = g.groupby("team")["sales"].transform("mean")
g["z"] = g.groupby("team")["sales"].transform(lambda s: (s - s.mean()) / s.std(ddof=0))
g["share"] = g["sales"] / g.groupby("team")["sales"].transform("sum")
print(g.round(2))
print(g.groupby("team")["sales"].agg(["mean", "sum"]))

print("=== Q9 ===")
from sklearn.model_selection import KFold, TimeSeriesSplit, StratifiedKFold
from sklearn.metrics import accuracy_score, average_precision_score, roc_auc_score
try:
    from imblearn.over_sampling import SMOTE
    from imblearn.pipeline import Pipeline as IPipe
    have = True
except Exception as e:
    have = False; print("imblearn missing", e)
print("imblearn:", have)
