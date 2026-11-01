# Q28: pandas memory and loading, with a SQLite cross-check of the chunked aggregate
import os, sqlite3, tempfile
import numpy as np
import pandas as pd

print("pandas", pd.__version__, "| numpy", np.__version__)
rng = np.random.default_rng(28)
N = 500_000
cities = [f"City{i:02d}" for i in range(20)]
statuses = ["placed", "shipped", "delivered", "returned"]
df = pd.DataFrame({
    "id": np.arange(1, N + 1),
    "city": rng.choice(cities, N),
    "status": rng.choice(statuses, N),
    "score": rng.integers(0, 101, N),
    "amount": rng.normal(100, 30, N).round(2),
    "ts": pd.Timestamp("2024-01-01") + pd.to_timedelta(rng.integers(0, 365 * 86400, N), unit="s"),
})
print(df.dtypes.to_string())

def mem(frame):
    return frame.memory_usage(deep=True, index=False)

before = mem(df)
small = df.copy()
small["id"] = pd.to_numeric(small["id"], downcast="unsigned")
small["score"] = pd.to_numeric(small["score"], downcast="integer")
small["amount"] = pd.to_numeric(small["amount"], downcast="float")
small["city"] = small["city"].astype("category")
small["status"] = small["status"].astype("category")
after = mem(small)
cmp = pd.DataFrame({"before": before, "after": after, "dtype_after": small.dtypes.astype(str)})
cmp["ratio"] = (cmp["after"] / cmp["before"]).round(3)
print(cmp.to_string())
print("total before", before.sum(), "after", after.sum(), "ratio", round(after.sum() / before.sum(), 3))

# when categoricals do not help: all-unique strings
hi = pd.Series([f"user-{i:07d}" for i in range(N)])
print("high cardinality str bytes", hi.memory_usage(deep=True, index=False),
      "category bytes", hi.astype("category").memory_usage(deep=True, index=False))

# risks of downcasting
print("numpy int8 wrap:", np.array([100, 200, 300]).astype(np.int8).tolist())
print("to_numeric downcast of 0..300 picks:", pd.to_numeric(pd.Series([0, 300]), downcast="integer").dtype)
print("float32 16777217 ->", int(np.float32(16777217)), "| 0.1 as float32 ->", repr(float(np.float32(0.1))))
print("float32 sum of amount vs float64:", float(small["amount"].sum()), float(df["amount"].sum()))
print("float32 sum with float64 accumulator:", float(small["amount"].astype("float64").sum()))
print("amounts changed by float32 downcast:", int((small["amount"].astype("float64") != df["amount"]).sum()), "of", N)

# CSV round trip
d = tempfile.mkdtemp()
path = os.path.join(d, "events.csv")
df.to_csv(path, index=False)
print("csv bytes", os.path.getsize(path))
full = pd.read_csv(path)
print("read_csv defaults:", full.dtypes.astype(str).to_dict(), "bytes", int(mem(full).sum()))
lean = pd.read_csv(path, usecols=["city", "status", "amount", "ts"],
                   dtype={"city": "category", "status": "category", "amount": "float32"},
                   parse_dates=["ts"])
print("read_csv lean:", lean.dtypes.astype(str).to_dict(), "bytes", int(mem(lean).sum()))
tot = None; nchunks = 0; maxrows = 0
for chunk in pd.read_csv(path, usecols=["city", "amount"], dtype={"city": "category", "amount": "float64"}, chunksize=100_000):
    nchunks += 1; maxrows = max(maxrows, len(chunk))
    part = chunk.groupby("city", observed=True)["amount"].agg(["sum", "count"])
    tot = part if tot is None else tot.add(part, fill_value=0)
print("chunks", nchunks, "max rows per chunk", maxrows)
chunked = tot.reset_index().rename(columns={"sum": "total", "count": "n"})
chunked["city"] = chunked["city"].astype(str)
chunked = chunked.sort_values("city").reset_index(drop=True)
chunked["n"] = chunked["n"].astype("int64")

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE ev(id INTEGER, city TEXT, status TEXT, score INTEGER, amount REAL, ts TEXT)")
con.executemany("INSERT INTO ev VALUES (?,?,?,?,?,?)", full.itertuples(index=False, name=None))
SQL = "SELECT city, SUM(amount) AS total, COUNT(*) AS n FROM ev GROUP BY city ORDER BY city"
sql_df = pd.read_sql_query(SQL, con)
assert list(sql_df["city"]) == list(chunked["city"])
assert (sql_df["n"] == chunked["n"]).all()
assert np.allclose(sql_df["total"], chunked["total"], rtol=0, atol=1e-6)
print("SQL equals chunked pandas (sorted by city, float tolerance 1e-6): OK;", len(sql_df), "cities")
print(sql_df.head(3).to_string(index=False))

# groupby on categoricals: observed and sort defaults in this pandas
cat = pd.Series(pd.Categorical(["b", "a", "b"], categories=["c", "b", "a"]))
v = pd.Series([1, 2, 3])
print("default (observed, sort):\n", v.groupby(cat).sum().to_string())
print("observed=False:\n", v.groupby(cat, observed=False).sum().to_string())
print("observed=True, sort=False:\n", v.groupby(cat, observed=True, sort=False).sum().to_string())
print("plain strings, sort=True index:", v.groupby(pd.Series(["b", "a", "b"])).sum().index.tolist(),
      "| sort=False:", v.groupby(pd.Series(["b", "a", "b"]), sort=False).sum().index.tolist())
