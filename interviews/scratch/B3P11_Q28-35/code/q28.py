# Q28: pandas memory and loading. Seeded 500,000-row frame; SQLite holds the same data for the SQL cross-check.
import os, sqlite3, tempfile
import numpy as np
import pandas as pd

rng = np.random.default_rng(28)
n = 500_000
cities = np.array([f"City_{i:02d}" for i in range(20)])
statuses = np.array(["new", "paid", "shipped", "returned"])
df = pd.DataFrame({
    "id": np.arange(1, n + 1),
    "city": cities[rng.integers(0, 20, n)],
    "status": statuses[rng.integers(0, 4, n)],
    "score": rng.integers(0, 101, n),
    "amount": rng.normal(100, 30, n).round(2),
    "ts": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 365 * 86400, n), unit="s"),
})
print("dtypes:", dict(df.dtypes.astype(str)))
before = df.memory_usage(deep=True, index=False)
print("\nmemory_usage(deep=True) bytes, default dtypes:")
print(before.to_string()); print("total:", before.sum())

small = df.copy()
small["id"] = pd.to_numeric(small["id"], downcast="unsigned")
small["score"] = pd.to_numeric(small["score"], downcast="unsigned")
small["amount"] = pd.to_numeric(small["amount"], downcast="float")
small["city"] = small["city"].astype("category")
small["status"] = small["status"].astype("category")
after = small.memory_usage(deep=True, index=False)
cmp_ = pd.DataFrame({"before": before, "after": after, "after_dtype": small.dtypes.astype(str)})
print("\nafter downcast + category:"); print(cmp_.to_string()); print("total:", after.sum(),
      "ratio %.2f" % (after.sum() / before.sum()))

# high cardinality: category does not help
hc = pd.Series([f"user_{i}" for i in range(n)])
print("\nunique-per-row strings: str %d bytes vs category %d bytes" % (
    hc.memory_usage(deep=True, index=False), hc.astype("category").memory_usage(deep=True, index=False)))
print("city codes dtype:", small["city"].cat.codes.dtype, "| categories:", small["city"].cat.categories.size)

# risks of downcasting
print("\nrisk 1: raw numpy cast wraps silently:", np.array([100, 200, 300, 70000]).astype(np.int8).tolist(),
      "(from [100, 200, 300, 70000])")
print("   pandas Series.astype('int8') on out-of-range:", end=" ")
try:
    print(pd.Series([100, 300]).astype("int8").tolist())
except Exception as e:
    print(type(e).__name__, "-", str(e)[:80])
print("   to_numeric downcast picks the smallest type that fits:", pd.to_numeric(pd.Series([100, 300]), downcast="integer").dtype,
      "and", pd.to_numeric(pd.Series([100, 200]), downcast="unsigned").dtype)
x = np.float64(16777217.0)
print("risk 2: float32 loses precision: float64 16777217 -> float32 ->", int(np.float32(x)),
      "| 0.1 + 0.2 in float32 =", float(np.float32(0.1) + np.float32(0.2)), "| amount sum f64 %.2f vs f32 %.2f" % (
          df["amount"].sum(), small["amount"].astype("float32").sum()))
print("   amounts changed by float32 round-trip:", int((small["amount"].astype("float64") != df["amount"]).sum()), "of", n)

# CSV round trip
d = tempfile.mkdtemp()
path = os.path.join(d, "big.csv")
df.to_csv(path, index=False)
print("\nCSV size bytes:", os.path.getsize(path))
full = pd.read_csv(path)
print("plain read_csv total bytes:", full.memory_usage(deep=True, index=False).sum(), dict(full.dtypes.astype(str)))
lean = pd.read_csv(path, usecols=["city", "status", "score", "amount", "ts"],
                   dtype={"city": "category", "status": "category", "score": "uint8", "amount": "float32"},
                   parse_dates=["ts"])
print("lean read_csv total bytes:", lean.memory_usage(deep=True, index=False).sum(), dict(lean.dtypes.astype(str)))

# chunked aggregation: sum and count per (status, city) without holding the file in memory
parts = []
for chunk in pd.read_csv(path, usecols=["city", "status", "amount"], dtype={"city": "category", "status": "category"},
                         chunksize=100_000):
    parts.append(chunk.groupby(["status", "city"], observed=True)["amount"].agg(["sum", "count"]))
print("chunks:", len(parts))
chunked = pd.concat(parts).groupby(level=["status", "city"]).sum().reset_index()
chunked = chunked.sort_values(["status", "city"]).reset_index(drop=True)

# SQL version of the same aggregation
con = sqlite3.connect(":memory:")
df.assign(ts=df["ts"].astype(str)).to_sql("t", con, index=False)
sql = """SELECT status, city, ROUND(SUM(amount), 2) AS sum, COUNT(*) AS count
FROM t GROUP BY status, city ORDER BY status, city"""
s = pd.read_sql(sql, con)
chunked[["status", "city"]] = chunked[["status", "city"]].astype(str)
chunked["sum"] = chunked["sum"].round(2)
pd.testing.assert_frame_equal(s, chunked, check_dtype=False)
print("\nSQL vs chunked pandas: %d groups, equal (compared after sorting by status, city)" % len(s))
print(s.head(3).to_string(index=False))

# the hand-checkable mini example: 6 rows, chunksize=3
mini = pd.DataFrame({"city": ["Pune", "Delhi", "Pune", "Pune", "Delhi", "Agra"], "amount": [10, 20, 30, 40, 50, 60]})
mp = os.path.join(d, "mini.csv"); mini.to_csv(mp, index=False)
mc = mini["city"].astype("category")
print("\nmini: categories", mc.cat.categories.tolist(), "codes", mc.cat.codes.tolist())
mparts = []
for i, ch in enumerate(pd.read_csv(mp, chunksize=3)):
    p = ch.groupby("city")["amount"].agg(["sum", "count"]); mparts.append(p)
    print(f"mini chunk {i}: rows {len(ch)}  partial {p.to_dict('index')}")
mtot = pd.concat(mparts).groupby(level="city").sum()
print("mini combined:", mtot.to_dict("index"))
assert mtot["sum"].to_dict() == mini.groupby("city")["amount"].sum().to_dict()

# groupby on categoricals: observed and sort (pandas 3.0.5)
c = pd.DataFrame({"g": pd.Categorical(["b", "a", "b"], categories=["c", "b", "a"]), "v": [1, 2, 3]})
print("\ncategories order c,b,a; data has b,a,b. Default groupby (3.0.5):")
print(c.groupby("g")["v"].sum().to_string())
print("observed=False:"); print(c.groupby("g", observed=False)["v"].sum().to_string())
print("observed=True, sort=False:"); print(c.groupby("g", observed=True, sort=False)["v"].sum().to_string())
print("plain str groupby, sort=True/False:", c.assign(g=c["g"].astype(str)).groupby("g")["v"].sum().index.tolist(),
      c.assign(g=c["g"].astype(str)).groupby("g", sort=False)["v"].sum().index.tolist())
