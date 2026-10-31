# Q27: push SQL work down before loading into pandas
import sqlite3, random, os, tempfile, time
import numpy as np
import pandas as pd

rnd = random.Random(27)
statuses = ["delivered"] * 70 + ["cancelled"] * 10 + ["returned"] * 10 + ["placed"] * 10
rows = [(i, rnd.randint(1, 50000), "%d-%02d-%02d" % (rnd.choice([2023, 2024, 2024, 2025]), rnd.randint(1, 12), rnd.randint(1, 28)),
         rnd.choice(statuses), rnd.randint(10, 5000)) for i in range(1, 500001)]
tmp = tempfile.TemporaryDirectory()
path = os.path.join(tmp.name, "orders.db")
con = sqlite3.connect(path)
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
con.commit()
con.close()
print("database file: %.1f MB, 500,000 rows" % (os.path.getsize(path) / 1e6))

# tiny sample for the hand walk-through
t = sqlite3.connect(":memory:")
t.executescript("""CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,1,'2024-01-05','delivered',100),(2,2,'2024-01-20','delivered',50),(3,3,'2024-01-21','cancelled',999),
 (4,1,'2024-02-02','delivered',70),(5,2,'2023-12-31','delivered',500),(6,3,'2025-01-01','delivered',5);""")
SQL = """SELECT substr(order_date, 1, 7) AS month, SUM(amount) AS revenue, COUNT(*) AS n_orders
FROM orders WHERE status = 'delivered' AND order_date >= '2024-01-01' AND order_date < '2025-01-01'
GROUP BY month ORDER BY month"""
print("tiny:", t.execute(SQL).fetchall())

def timed(fn):
    t0 = time.perf_counter()
    out = fn()
    return out, (time.perf_counter() - t0) * 1000

conn = sqlite3.connect(path)
res = {}

def pandas_agg(df):
    d = df[(df["status"] == "delivered") & (df["order_date"] >= "2024-01-01") & (df["order_date"] < "2025-01-01")]
    g = d.assign(month=d["order_date"].str[:7]).groupby("month").agg(revenue=("amount", "sum"), n_orders=("amount", "size"))
    return g.reset_index().sort_values("month").reset_index(drop=True)

# (a) whole table
full, ms = timed(lambda: pd.read_sql("SELECT * FROM orders", conn))
mem_a = int(full.memory_usage(deep=True).sum())
res["a"], ms2 = timed(lambda: pandas_agg(full))
print("(a) read whole table: rows transferred %d, memory_usage(deep) %.1f MB, load %.0f ms + filter/groupby %.0f ms" % (len(full), mem_a / 1e6, ms, ms2))
print("    dtypes:", dict(full.dtypes.astype(str)))
t_a = ms + ms2
# (b) SQL does the filter and aggregation
dfb, t_b = timed(lambda: pd.read_sql(SQL, conn))
res["b"] = dfb
print("(b) WHERE + GROUP BY in SQL: rows transferred %d, memory_usage(deep) %d bytes, %.0f ms" % (len(dfb), dfb.memory_usage(deep=True).sum(), t_b))
# (c) chunked: stream, aggregate per chunk, combine
def chunked():
    parts, total_rows, peak = [], 0, 0
    for ch in pd.read_sql("SELECT * FROM orders", conn, chunksize=50000):
        total_rows += len(ch)
        peak = max(peak, int(ch.memory_usage(deep=True).sum()))
        parts.append(pandas_agg(ch))
    allp = pd.concat(parts)
    out = allp.groupby("month", as_index=False)[["revenue", "n_orders"]].sum().sort_values("month").reset_index(drop=True)
    return out, total_rows, peak
(res["c"], rows_c, peak_c), t_c = timed(chunked)
print("(c) chunksize=50,000, aggregate per chunk: rows transferred %d, peak chunk memory %.1f MB, %.0f ms" % (rows_c, peak_c / 1e6, t_c))
# (d) only the needed columns, filter in SQL but aggregate in pandas; and columns only (no WHERE)
def cols_only():
    return pd.read_sql("SELECT order_date, status, amount FROM orders", conn)
dcols, t_d1 = timed(cols_only)
res["d"], t_d2 = timed(lambda: pandas_agg(dcols))
print("(d) only 3 needed columns, filter in pandas: rows transferred %d, memory_usage(deep) %.1f MB, %.0f ms + %.0f ms" % (len(dcols), dcols.memory_usage(deep=True).sum() / 1e6, t_d1, t_d2))
dwhere, t_d3 = timed(lambda: pd.read_sql("SELECT order_date, amount FROM orders WHERE status = 'delivered' AND order_date >= '2024-01-01' AND order_date < '2025-01-01'", conn))
res["e"] = (dwhere.assign(month=dwhere["order_date"].str[:7]).groupby("month").agg(revenue=("amount", "sum"), n_orders=("amount", "size")).reset_index())
print("(e) WHERE pushed down, 2 columns, aggregate in pandas: rows transferred %d, memory_usage(deep) %.1f MB, %.0f ms" % (len(dwhere), dwhere.memory_usage(deep=True).sum() / 1e6, t_d3))

for k in ("a", "c", "d", "e"):
    pd.testing.assert_frame_equal(res[k][["month", "revenue", "n_orders"]].astype({"revenue": "int64", "n_orders": "int64"}),
                                   res["b"][["month", "revenue", "n_orders"]].astype({"revenue": "int64", "n_orders": "int64"}))
print("asserts passed: (a), (c), (d), (e) equal (b); compared sorted by month; revenue and n_orders as int64")
print(res["b"].to_string(index=False))
print("timings are machine-specific single runs: a=%.0f ms, b=%.0f ms, c=%.0f ms, d=%.0f ms, e=%.0f ms" % (t_a, t_b, t_c, t_d1 + t_d2, t_d3))

# decomposable versus not
chunk_med = []
for ch in pd.read_sql("SELECT order_date, status, amount FROM orders WHERE status = 'delivered'", conn, chunksize=50000):
    chunk_med.append(ch["amount"].median())
true_med = pd.read_sql("SELECT amount FROM orders WHERE status = 'delivered'", conn)["amount"].median()
print("\nmedian of delivered amounts: true %.1f; mean of the 50,000-row chunk medians %.1f (equal here only because every chunk is a random sample of the same distribution)" % (true_med, float(np.mean(chunk_med))))
c1, c2 = pd.Series([1, 2, 9]), pd.Series([3, 4, 5, 6, 7])
print("counterexample: true median of all 8 values %.1f, mean of the two chunk medians %.1f" % (pd.concat([c1, c2]).median(), (c1.median() + c2.median()) / 2))
# mean needs (sum, count) pairs
sums = pd.read_sql("SELECT SUM(amount) s, COUNT(*) c FROM orders WHERE status = 'delivered'", conn).iloc[0]
print("mean from decomposed (sum, count): %.4f; direct mean: %.4f" % (sums["s"] / sums["c"], full.loc[full.status == "delivered", "amount"].mean()))
tmp.cleanup()
