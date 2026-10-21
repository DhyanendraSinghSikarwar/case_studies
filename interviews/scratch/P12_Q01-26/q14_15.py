import numpy as np, pandas as pd, io
rng = np.random.default_rng(0)

print("=== Q14 ===")
from sklearn.model_selection import train_test_split, GroupKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
n = 1500
cust = rng.integers(0, 500, n)
base = pd.DataFrame({"customer_id": cust, "tenure": rng.normal(24, 8, n), "spend": rng.gamma(2, 50, n)})
base["churn"] = (rng.random(n) < 0.1).astype(int)       # label is pure noise vs features
base["refund_flag"] = base.churn * (rng.random(n) < 0.95)  # target-derived (post-outcome) column
base["row_id"] = np.arange(n)                              # ID-like
# duplicates: re-append 20% of rows
dup = base.sample(frac=0.2, random_state=0)
df = pd.concat([base, dup]).reset_index(drop=True)
X = df.drop(columns="churn"); y = df.churn
def run(Xc, y, split="random", groups=None):
    if split == "random":
        Xtr, Xte, ytr, yte = train_test_split(Xc, y, test_size=0.25, random_state=0)
    m = RandomForestClassifier(100, random_state=0, n_jobs=1).fit(Xtr, ytr)
    p = m.predict_proba(Xte)[:, 1]
    return round(accuracy_score(yte, m.predict(Xte)), 3), round(roc_auc_score(yte, p), 3)
print("base rate neg:", round(1 - y.mean(), 3))
print("0 as-is        (acc, auc):", run(X, y))
X1 = X.drop(columns="refund_flag")
print("1 drop target-derived:   ", run(X1, y))
X2 = X1.drop(columns="row_id")
print("2 drop ID-like:          ", run(X2, y))
# 3. dedupe + group split
d3 = df.drop_duplicates(subset=[c for c in df.columns])
Xd = d3.drop(columns=["churn", "refund_flag", "row_id"]); yd = d3.churn
gtr, gte = next(iter(GroupKFold(4).split(Xd, yd, groups=d3.customer_id)))
m = RandomForestClassifier(100, random_state=0, n_jobs=1).fit(Xd.iloc[gtr].drop(columns="customer_id"), yd.iloc[gtr])
p = m.predict_proba(Xd.iloc[gte].drop(columns="customer_id"))[:, 1]
print("3 dedupe + group split:  ", (round(accuracy_score(yd.iloc[gte], (p > .5).astype(int)), 3), round(roc_auc_score(yd.iloc[gte], p), 3)))

print("=== Q15 ===")
raw = io.StringIO("""order_id,order_date,price,qty,category,age
1,2025-01-05,"Rs 1,200.50",2,Electronics,34
2,05/02/2025,"₹ 99",1,electronics ,29
3,"March 3, 2025","2,450",1,ELECTRONICS,-5
4,2025-03-09,"₹1,00,000",1,Home & Kitchen,41
4,2025-03-09,"₹1,00,000",1,Home & Kitchen,41
5,2025-04-01,N/A,3,home and kitchen,230
6,not a date,"$ 15.5",1,Home-Kitchen,38
""")
d = pd.read_csv(raw, dtype=str)
n0 = len(d)
d = d.drop_duplicates()
d["price"] = (d.price.str.replace(r"[^\d.]", "", regex=True)).replace("", np.nan).astype(float)
d["qty"] = pd.to_numeric(d.qty, errors="coerce")
d["age"] = pd.to_numeric(d.age, errors="coerce")
d["order_date"] = pd.to_datetime(d.order_date, format="mixed", errors="coerce", dayfirst=False)
cat_map = {"electronics": "electronics", "home & kitchen": "home_kitchen", "home and kitchen": "home_kitchen", "home-kitchen": "home_kitchen"}
d["category"] = d.category.str.strip().str.lower().map(cat_map)
bad_age = ~d.age.between(0, 100)
d.loc[bad_age, "age"] = np.nan
print(d)
print("rows", n0, "->", len(d), "| unmapped category:", d.category.isna().sum(), "| bad dates:", d.order_date.isna().sum(), "| impossible ages:", int(bad_age.sum()))
assert d.order_id.is_unique
