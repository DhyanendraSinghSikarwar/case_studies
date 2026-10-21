import numpy as np, pandas as pd
rng = np.random.default_rng(0)

print("=== Q1 ===")
n = 20
tx = pd.DataFrame({
    "user_id": rng.integers(1, 4, n),
    "ts": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 60, n), unit="D"),
    "amount": rng.integers(50, 500, n).astype(float),
    "category": rng.choice(["food", "travel", "books", "games"], n),
})
summary = tx.groupby("user_id").agg(
    total=("amount", "sum"), mean=("amount", "mean"),
    n_tx=("amount", "count"), last_tx=("ts", "max"))
top3 = (tx.groupby(["user_id", "category"], as_index=False)["amount"].sum()
          .sort_values(["user_id", "amount"], ascending=[True, False])
          .groupby("user_id").head(3))
print(summary.round(1))
print(top3)
# alternative: rank
g = tx.groupby(["user_id", "category"], as_index=False)["amount"].sum()
g["rk"] = g.groupby("user_id")["amount"].rank(method="first", ascending=False)
print(g[g.rk <= 3].sort_values(["user_id", "rk"]).shape)

print("=== Q2 ===")
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
df = pd.DataFrame({
    "age": rng.normal(40, 10, 200), "city": rng.choice(["A", "B", "C"], 200),
    "segment": rng.choice(["x", "y"], 200)})
df.loc[rng.random(200) < 0.15, "age"] = np.nan
df.loc[(df.segment == "y") & (rng.random(200) < 0.3), "city"] = None
audit = pd.DataFrame({"n_missing": df.isna().sum(), "pct": (df.isna().mean() * 100).round(1)})
print(audit)
print(df.drop(columns="segment").isna().groupby(df["segment"]).mean().round(2))
tr, te = train_test_split(df, test_size=0.25, random_state=0)
num, cat = ["age"], ["city"]
med = tr[num].median()
mode = tr[cat].mode().iloc[0]
tr2 = tr.copy(); te2 = te.copy()
for d in (tr2, te2):
    for c in num: d[c + "_was_na"] = d[c].isna().astype(int)
    d[num] = d[num].fillna(med); d[cat] = d[cat].fillna(mode)
print(med.to_dict(), mode.to_dict(), te2.isna().sum().sum())

print("=== Q3 ===")
df = pd.DataFrame({"a": [-1, 2, 3, 0], "b": [0, 0, 0, 0]}, index=[10, 11, 12, 13])
print(df.loc[11, "a"], df.iloc[1, 0], df.loc[10:12].shape, df.iloc[0:2].shape)  # label slice inclusive
print(df.loc[df.a > 0, "b"].tolist())
df.loc[df.a > 0, "b"] = 1
print(df)
import warnings
d2 = df.copy()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    d2[d2.a > 0]["b"] = 99
    print("chained assign changed original:", (d2.b == 99).any(), [str(x.category.__name__) for x in w])

print("=== Q4 ===")
orders = pd.DataFrame({"order_id": range(6), "cust_id": [1, 1, 2, 3, 4, 9]})
cust = pd.DataFrame({"cust_id": [1, 2, 2, 3, 5], "city": list("ABCDE")})
m = orders.merge(cust, on="cust_id", how="left")
print(len(orders), len(m))
print(cust[cust.cust_id.duplicated(keep=False)])
print(cust.cust_id.is_unique, orders.cust_id.is_unique)
try:
    orders.merge(cust, on="cust_id", validate="many_to_one")
except Exception as e:
    print(type(e).__name__, e)
cust_u = cust.sort_values("city").drop_duplicates("cust_id", keep="last")
m2 = orders.merge(cust_u, on="cust_id", how="left", validate="many_to_one", indicator=True)
print(len(m2)); print(m2["_merge"].value_counts())
