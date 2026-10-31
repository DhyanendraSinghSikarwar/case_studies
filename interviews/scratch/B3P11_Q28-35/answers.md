### Q28 ⭐⭐ 🟡 pandas memory and loading: a seeded 500,000-row DataFrame with ids, a string column with 20 distinct values (city), a status column with 4 values, an int column with values 0 to 100, a float column and a timestamp column. Show df.memory_usage(deep=True) per column (object or default str versus category), downcast with pd.to_numeric(downcast=...) and astype('category'), the size before and after, the risk of downcasting (overflow wrap in numpy casts, loss of precision in float32), and read_csv with usecols, dtype, parse_dates and chunksize on a CSV written in the run, aggregating per chunk. Explain why categoricals shrink low-cardinality text, when they do not (high cardinality), and how groupby behaves on categoricals (observed and sort arguments; check by running the pandas 3.0.5 default). Quote the pandas 'Scaling to large datasets' guide only for the ideas, not its numbers.
**Asked at:** pandas user guide pages 'Enhancing performance' and 'Scaling to large datasets' (opened); official documentation, not candidate reports; data scientist and analytics engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Load fewer columns, give low-cardinality text a `category` dtype and numbers the smallest safe integer or float type, and read big files in chunks of decomposable aggregates; the price is overflow and precision risks you must check, and categoricals only pay off when there are far fewer distinct values than rows.

**Schema and sample data:** the pandas frame has `id`, `city` (20 distinct strings), `status` (4 values), `score` (int 0 to 100), `amount` (float) and `ts` (timestamp), 500,000 rows from `np.random.default_rng(28)`. The same data goes into SQLite as `t` for the cross-check, and a 6-row mini file for the hand walk-through:
```sql
CREATE TABLE t(id INTEGER, city TEXT, status TEXT, score INTEGER, amount REAL, ts TEXT);
-- mini example (written to a CSV in the run): city, amount
-- Pune 10, Delhi 20, Pune 30 | Pune 40, Delhi 50, Agra 60
```

**SQL answer:** the aggregation that the chunked pandas loop must reproduce (same text as `sql` in the Code block):
```sql
SELECT status, city, ROUND(SUM(amount), 2) AS sum, COUNT(*) AS count
FROM t GROUP BY status, city ORDER BY status, city
```
SQL has no memory-layout knobs of this kind in SQLite; the closest ideas are declared column types and reading only the columns you SELECT. Other engines' column types and columnar compression are not executed here.

**pandas answer:** the loading recipe is the `lean = pd.read_csv(path, usecols=[...], dtype={...}, parse_dates=["ts"])` call and the chunk loop in the Code block:
```py
for chunk in pd.read_csv(path, usecols=["city", "status", "amount"], dtype={"city": "category", "status": "category"},
                         chunksize=100_000):
    parts.append(chunk.groupby(["status", "city"], observed=True)["amount"].agg(["sum", "count"]))
```
Downcasting is `pd.to_numeric(s, downcast="unsigned")` or `"float"`, and `astype("category")` for the two text columns. Only sums and counts are combined across chunks; a mean is rebuilt as sum divided by count, and a distinct count cannot be combined this way.

**Example:** the mini file has six rows read with `chunksize=3`. Chunk 0 is Pune 10, Delhi 20, Pune 30, so its partial result is Delhi (sum 20, count 1) and Pune (sum 40, count 2). Chunk 1 is Pune 40, Delhi 50, Agra 60, giving Agra (60, 1), Delhi (50, 1), Pune (40, 1). Adding the partials by city gives Agra (60, 1), Delhi (70, 2), Pune (80, 3), the same as grouping all six rows at once. As a category the city column holds the sorted categories Agra, Delhi, Pune and the codes 2, 1, 2, 2, 1, 0, so each row costs one small integer instead of its own string.

**Code:** run with `python3 -I`.
```python
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
```

**Output (my run):**
```text
dtypes: {'id': 'int64', 'city': 'str', 'status': 'str', 'score': 'int64', 'amount': 'float64', 'ts': 'datetime64[us]'}

memory_usage(deep=True) bytes, default dtypes:
id         4000000
city      28000000
status    27249606
score      4000000
amount     4000000
ts         4000000
total: 71249606

after downcast + category:
          before    after     after_dtype
id       4000000  2000000          uint32
city    28000000   501120        category
status  27249606   500218        category
score    4000000   500000           uint8
amount   4000000  2000000         float32
ts       4000000  4000000  datetime64[us]
total: 9501338 ratio 0.13

unique-per-row strings: str 29888890 bytes vs category 31888890 bytes
city codes dtype: int8 | categories: 20

risk 1: raw numpy cast wraps silently: [100, -56, 44, 112] (from [100, 200, 300, 70000])
   pandas Series.astype('int8') on out-of-range: [100, 44]
   to_numeric downcast picks the smallest type that fits: int16 and uint8
risk 2: float32 loses precision: float64 16777217 -> float32 -> 16777216 | 0.1 + 0.2 in float32 = 0.30000001192092896 | amount sum f64 50001499.66 vs f32 50001504.00
   amounts changed by float32 round-trip: 480164 of 500000

CSV size bytes: 25293568
plain read_csv total bytes: 101249606 {'id': 'int64', 'city': 'str', 'status': 'str', 'score': 'int64', 'amount': 'float64', 'ts': 'str'}
lean read_csv total bytes: 7502066 {'city': 'category', 'status': 'category', 'score': 'uint8', 'amount': 'float32', 'ts': 'datetime64[us]'}
chunks: 5

SQL vs chunked pandas: 80 groups, equal (compared after sorting by status, city)
status    city       sum  count
   new City_00 636138.38   6343
   new City_01 627193.63   6291
   new City_02 634780.98   6338

mini: categories ['Agra', 'Delhi', 'Pune'] codes [2, 1, 2, 2, 1, 0]
mini chunk 0: rows 3  partial {'Delhi': {'sum': 20, 'count': 1}, 'Pune': {'sum': 40, 'count': 2}}
mini chunk 1: rows 3  partial {'Agra': {'sum': 60, 'count': 1}, 'Delhi': {'sum': 50, 'count': 1}, 'Pune': {'sum': 40, 'count': 1}}
mini combined: {'Agra': {'sum': 60, 'count': 1}, 'Delhi': {'sum': 70, 'count': 2}, 'Pune': {'sum': 80, 'count': 3}}

categories order c,b,a; data has b,a,b. Default groupby (3.0.5):
g
b    4
a    2
observed=False:
g
c    0
b    4
a    2
observed=True, sort=False:
g
b    4
a    2
plain str groupby, sort=True/False: ['a', 'b'] ['b', 'a']
```

Reading the output: the two text columns were 28,000,000 and 27,249,606 bytes (the default `str` dtype in pandas 3.0.5, measured with `deep=True`) and became 501,120 and 500,218 bytes as categories (500,000 one-byte codes plus the 20 or 4 labels). Whole-frame memory went from 71,249,606 to 9,501,338 bytes, a ratio of 0.13. The `ts` column did not change. For 500,000 unique strings the category was larger (31,888,890 bytes against 29,888,890 for `str`), because it stores the codes and every label. The lean read used five columns and no `id`, so its 7,502,066 bytes against 101,249,606 for the plain read is not a like-for-like dtype comparison, it is dtypes plus fewer columns (the plain read also left `ts` as strings). The CSV itself was 25,293,568 bytes. The chunked groupby over 5 chunks gave 80 groups that equal the SQL result.

**Edge cases:**
- Overflow wraps silently: `np.array([100, 200, 300, 70000]).astype(np.int8)` gave `[100, -56, 44, 112]`. In this run (pandas 3.0.5) `pd.Series([100, 300]).astype("int8")` also returned `[100, 44]` with no error, so do not rely on `astype` to protect you. `pd.to_numeric(..., downcast=...)` chooses a type that fits the data it sees (int16 for `[100, 300]`, uint8 for `[100, 200]`), but a later batch with bigger values can still overflow a column you fixed at uint8.
- float32 loses precision: 16,777,217 became 16,777,216, `0.1 + 0.2` in float32 printed 0.30000001192092896, 480,164 of the 500,000 two-decimal amounts changed when round-tripped through float32, and the column sum moved from 50001499.66 (float64) to 50001504.00 (float32). Money columns should stay float64 or integer cents.
- Categories and missing values: NaN is not a category, it is code -1. A new value not in the categories cannot be assigned until you add the category.
- High cardinality: a category of 500,000 unique strings was bigger than the plain strings (see Output).
- Chunk boundaries: a group can span chunks, which is why partials are re-aggregated; the categories seen per chunk can differ, which is why the code casts to `str` before comparing with SQL.

**Then explain:**
- Why categoricals shrink low-cardinality text: the strings are stored once in the category index and each row holds a small integer code (int8 here for 20 categories), so memory is roughly rows times code size plus the labels.
- When they do not: when distinct values approach the row count, the codes plus the full label table cost more than the strings (shown above). They also help `groupby` and comparisons only while you stay in category land; converting back with `astype(str)` pays the cost again.
- `groupby` on a categorical, checked in pandas 3.0.5: with categories ordered c, b, a and data b, a, b, the default result was b = 4, a = 2: unobserved category c is dropped (the default is `observed=True` in this version) and `sort=True` follows the category order (b, then a), not alphabetical order. `observed=False` adds c with 0. `sort=False` on observed categories gave b then a. A plain string column sorted alphabetically (a, b), and with `sort=False` gave first-appearance order (b, a). Older pandas defaulted to `observed=False`, so pass it explicitly in code that must run on both.
- The pandas 'Scaling to large datasets' guide, for the ideas only: load less data (columns), use more efficient dtypes, and process in chunks. I use none of its numbers.
- Time zones and dates: `parse_dates` gives `datetime64` and is far smaller than leaving timestamps as text.

**Follow-ups:**
- What if the aggregate is a median or a distinct count across chunks? (Not decomposable: use a two-pass approach, a database, or an approximate sketch; not run here.)
- Parquet or another columnar format would store the same columns compressed and read only the columns asked for (not executed here, not benchmarked).
- When is `pyarrow`-backed `string[pyarrow]` an alternative? (Not tested here: pyarrow was not used in this run.)

**Common mistakes:**
- Quoting memory with `memory_usage()` without `deep=True`: for text it counts only pointers, not the strings.
- Downcasting before the data range is known, or downcasting money to float32.
- Using `category` on an id-like column.
- Forgetting `observed` and `sort` on categorical groupbys and being surprised by dropped or reordered groups.
- Summing means across chunks instead of sums and counts.

### Q29 ⭐⭐ 🔴 Diagnose a slow report end to end: a dashboard query on orders(order_id, customer_id, order_date, status, amount) 300,000 rows, customers(customer_id, name, city, segment) 20,000 rows and order_items(item_id, order_id, product_id, qty, price) 900,000 rows: revenue and distinct customers per city and month for the last 6 months, delivered orders only, top 10 cities by revenue. 'It took 2 seconds last year and 40 seconds now.' With no indexes except primary keys, print the plan, count VM steps, find each problem in order (function on the date column, missing foreign-key indexes, fan-out through order_items inflating counts, SELECT of unused columns, no pre-aggregation, a sort for the top-N), fix one thing at a time re-measuring VM steps after each, and assert the final result equals a pandas computation. Describe the loop (baseline, read the plan, change one thing, re-measure, re-check the results) and what you would ask about in a real system (table sizes, data growth, existing indexes, the engine, concurrency).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Measure first (plan and VM steps), then change one thing at a time and re-check the result, because the fan-out through `order_items` both wastes work and makes the revenue wrong, while the index and date fixes only change cost.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT, segment TEXT);       -- 20,000 rows
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount REAL);  -- 300,000 rows
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER, price REAL); -- 900,000 rows
-- mini example used for the hand walk (run in the Code block):
-- orders: (1,c1,2026-06-10,delivered,100) (2,c1,2026-06-20,delivered,50) (3,c2,2026-03-01,delivered,70) (4,c2,2026-06-25,placed,999)
-- items: order 1 has 3 items, order 2 has 1, order 3 has 2, order 4 has none; both customers are in Pune
```
The big data is seeded (`default_rng(29)`): 40 cities, dates 2024-11-01 to 2026-10-31, about 60% of orders delivered, "last 6 months" anchored at 2026-05-01 so the run is repeatable.

**SQL answer:** the final query is `S5` in the Code block (the earlier steps are the variants `S0` to `S4a`, `S6`); it needs the index `ix_ord_cov ON orders(status, order_date, customer_id, amount)`:
```sql
/* S5 covering index on orders */
WITH cm AS (
 SELECT c.city AS city, strftime('%Y-%m', o.order_date) AS month,
        SUM(o.amount) AS revenue, COUNT(DISTINCT o.customer_id) AS customers
 FROM orders o JOIN customers c ON c.customer_id = o.customer_id
 WHERE o.status = 'delivered' AND o.order_date >= '2026-05-01'
 GROUP BY c.city, strftime('%Y-%m', o.order_date))
SELECT cm.city, cm.month, cm.revenue, cm.customers FROM cm
WHERE cm.city IN (SELECT city FROM cm GROUP BY city ORDER BY SUM(revenue) DESC LIMIT 10)
ORDER BY cm.city, cm.month
```
Revenue is `SUM(orders.amount)` over delivered orders; distinct customers per city and month is `COUNT(DISTINCT customer_id)`; the 10 cities are the top by six-month revenue.

**pandas answer:** the expected result in the Code block:
```py
o = orders[(orders.status == "delivered") & (orders.order_date >= CUT)].merge(cust[["customer_id", "city"]], on="customer_id")
o["month"] = o["order_date"].str[:7]
cm = o.groupby(["city", "month"]).agg(revenue=("amount", "sum"), customers=("customer_id", "nunique")).reset_index()
top = cm.groupby("city")["revenue"].sum().nlargest(10).index
exp = cm[cm.city.isin(top)].sort_values(["city", "month"]).reset_index(drop=True)
```

**Example:** in the mini data, the order-items join repeats each order once per item: order 1 (amount 100, three items) counts three times and order 2 (amount 50, one item) once, so the join gives June revenue 300 + 50 = 350 where the truth is 100 + 50 = 150. The distinct customer count is 1 in both. Order 3 is outside the six-month window and order 4 is not delivered. (The run prints 350.0 with the join and 150.0 without it.) On the big data the same effect inflated each city-month revenue by about 2.8 to 3.0 times (3 items per order on average) and, because orders with no items disappear in an inner join (14,971 of 300,000), it also changed the top-10 set.

**Code:** run with `python3 -I`. VM steps are counted with `set_progress_handler(cb, 1)`; seconds are one run each, machine-specific.
```python
# Q29: diagnose a slow dashboard query step by step (SQLite 3.x via sqlite3; VM steps via progress handler).
import sqlite3, time
import numpy as np
import pandas as pd

rng = np.random.default_rng(29)
N_ORD, N_CUS, N_ITM = 300_000, 20_000, 900_000
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT, segment TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount REAL);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER, price REAL);
""")
cities = [f"City_{i:02d}" for i in range(40)]
cust = pd.DataFrame({"customer_id": np.arange(1, N_CUS + 1),
                     "name": [f"cust_{i}" for i in range(1, N_CUS + 1)],
                     "city": np.array(cities)[rng.integers(0, 40, N_CUS)],
                     "segment": np.array(["retail", "smb", "corp"])[rng.integers(0, 3, N_CUS)]})
days = pd.Timestamp("2024-11-01") + pd.to_timedelta(rng.integers(0, 730, N_ORD), unit="D")   # to 2026-10-31
orders = pd.DataFrame({"order_id": np.arange(1, N_ORD + 1),
                       "customer_id": rng.integers(1, N_CUS + 1, N_ORD),
                       "order_date": days.strftime("%Y-%m-%d"),
                       "status": np.array(["delivered", "placed", "cancelled", "returned"])[
                           rng.choice(4, N_ORD, p=[0.6, 0.2, 0.1, 0.1])],
                       "amount": rng.integers(500, 20000, N_ORD) / 100})
items = pd.DataFrame({"item_id": np.arange(1, N_ITM + 1), "order_id": rng.integers(1, N_ORD + 1, N_ITM),
                      "product_id": rng.integers(1, 500, N_ITM), "qty": rng.integers(1, 5, N_ITM),
                      "price": rng.integers(100, 5000, N_ITM) / 100})
for name, d in (("customers", cust), ("orders", orders), ("order_items", items)):
    con.executemany(f"INSERT INTO {name} VALUES ({','.join('?' * d.shape[1])})", d.itertuples(index=False, name=None))
con.commit()
print("rows:", [con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in ("orders", "customers", "order_items")])

CUT = "2026-05-01"   # 'last 6 months' anchored at a fixed date so the run is repeatable (data ends 2026-10-31)

def steps_and_rows(sql):
    cnt = [0]
    def cb():
        cnt[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return cnt[0], rows

def seconds(sql):
    t = time.perf_counter(); con.execute(sql).fetchall(); return time.perf_counter() - t

def plan(sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

TAIL = """
SELECT cm.city, cm.month, cm.revenue, cm.customers FROM cm
WHERE cm.city IN (SELECT city FROM cm GROUP BY city ORDER BY SUM(revenue) DESC LIMIT 10)
ORDER BY cm.city, cm.month"""

S0 = f"""/* S0 baseline */
WITH cm AS (
 SELECT c.city AS city, strftime('%Y-%m', o.order_date) AS month,
        SUM(o.amount) AS revenue, COUNT(DISTINCT o.customer_id) AS customers
 FROM orders o JOIN customers c ON c.customer_id = o.customer_id
               JOIN order_items i ON i.order_id = o.order_id
 WHERE o.status = 'delivered' AND strftime('%Y-%m', o.order_date) >= '2026-05'
 GROUP BY c.city, strftime('%Y-%m', o.order_date)){TAIL}"""
S1 = S0.replace("S0 baseline", "S1 sargable date").replace("strftime('%Y-%m', o.order_date) >= '2026-05'", f"o.order_date >= '{CUT}'")
S2 = S1.replace("S1 sargable date", "S2 after index on order_items(order_id)")
S3 = S2.replace("S2 after index on order_items(order_id)", "S3 drop the unused order_items join").replace(
    "\n               JOIN order_items i ON i.order_id = o.order_id", "")
S4_wide = f"""/* S4a wide SELECT inside a CTE */
WITH j AS (SELECT o.*, c.name, c.city, c.segment FROM orders o JOIN customers c ON c.customer_id = o.customer_id),
cm AS (
 SELECT city, strftime('%Y-%m', order_date) AS month, SUM(amount) AS revenue, COUNT(DISTINCT customer_id) AS customers
 FROM j WHERE status = 'delivered' AND order_date >= '{CUT}'
 GROUP BY city, strftime('%Y-%m', order_date)){TAIL}"""
S5 = S3.replace("S3 drop the unused order_items join", "S5 covering index on orders")
S6 = f"""/* S6 pre-aggregate per customer and month, then join customers */
WITH pc AS (
 SELECT customer_id, substr(order_date, 1, 7) AS month, SUM(amount) AS revenue
 FROM orders WHERE status = 'delivered' AND order_date >= '{CUT}'
 GROUP BY customer_id, substr(order_date, 1, 7)),
cm AS (
 SELECT c.city AS city, pc.month AS month, SUM(pc.revenue) AS revenue, COUNT(*) AS customers
 FROM pc JOIN customers c ON c.customer_id = pc.customer_id
 GROUP BY c.city, pc.month){TAIL}"""

def run(tag, sql, note=""):
    st, rows = steps_and_rows(sql)
    sec = seconds(sql)
    print(f"\n== {tag} {note}\nVM steps: {st:,}   seconds (machine-specific, one run): {sec:.2f}   rows returned: {len(rows)}")
    for p in plan(sql): print("   plan:", p)
    return st, rows

res = {}
res["S0"] = run("S0 baseline: strftime on date, no FK index, fan-out join, COUNT(DISTINCT)", S0)
res["S1"] = run("S1 sargable date predicate (order_date >= literal)", S1)
con.execute("CREATE INDEX ix_items_order ON order_items(order_id)")
res["S2"] = run("S2 + index on order_items(order_id)", S2)
res["S3"] = run("S3 drop the unused order_items join (removes the fan-out)", S3)
res["S4a"] = run("S4a wide SELECT o.*, c.* inside a CTE, otherwise S3", S4_wide)
con.execute("CREATE INDEX ix_ord_cov ON orders(status, order_date, customer_id, amount)")
res["S5"] = run("S5 + covering index orders(status, order_date, customer_id, amount)", S5)
res["S6"] = run("S6 pre-aggregate by customer and month, then join customers", S6)

# correctness: pandas on the same data
o = orders[(orders.status == "delivered") & (orders.order_date >= CUT)].merge(cust[["customer_id", "city"]], on="customer_id")
o["month"] = o["order_date"].str[:7]
cm = o.groupby(["city", "month"]).agg(revenue=("amount", "sum"), customers=("customer_id", "nunique")).reset_index()
top = cm.groupby("city")["revenue"].sum().nlargest(10).index
exp = cm[cm.city.isin(top)].sort_values(["city", "month"]).reset_index(drop=True)
exp["revenue"] = exp["revenue"].round(2)
print("\npandas expected rows:", len(exp), "| top-10 cities:", sorted(top))
print(exp.head(4).to_string(index=False))

def frame(rows):
    f = pd.DataFrame(rows, columns=["city", "month", "revenue", "customers"])
    f["revenue"] = f["revenue"].round(2)
    return f.sort_values(["city", "month"]).reset_index(drop=True)

for k in ("S3", "S4a", "S5", "S6"):
    pd.testing.assert_frame_equal(frame(res[k][1]), exp, check_dtype=False)
print("S3, S4a, S5, S6 equal pandas (compared after sorting by city, month)")
w, g = frame(res["S0"][1]), exp
print("S0 (fan-out) top-10 city set equals pandas?", set(w.city) == set(g.city),
      "| revenue equal?", bool(np.allclose(w.revenue.values, g.revenue.values)) if len(w) == len(g) else "row counts differ")
m = w.merge(g, on=["city", "month"], suffixes=("_s0", "_ok"))
print("   inflation of revenue in S0 (first rows):", (m.revenue_s0 / m.revenue_ok).round(2).head(4).tolist())
print("   S0 customers column equal on the shared city-months?", bool((m.customers_s0 == m.customers_ok).all()),
      "| orders with no items (dropped by the inner join):", int(len(set(orders.order_id) - set(items.order_id))))
print("orders delivered in the window:", len(o), "| items per order mean: %.2f" % (N_ITM / N_ORD))
print("\nsteps summary:", {k: v[0] for k, v in res.items()})

# the hand-checkable mini example (3 orders), same two shapes of query
m = sqlite3.connect(":memory:")
m.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount REAL);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER);
INSERT INTO customers VALUES (1,'Pune'),(2,'Pune');
INSERT INTO orders VALUES (1,1,'2026-06-10','delivered',100),(2,1,'2026-06-20','delivered',50),(3,2,'2026-03-01','delivered',70),(4,2,'2026-06-25','placed',999);
INSERT INTO order_items VALUES (1,1,1),(2,1,1),(3,1,2),(4,2,1),(5,3,1),(6,3,1);
""")
fan = m.execute("SELECT c.city, SUM(o.amount), COUNT(DISTINCT o.customer_id) FROM orders o JOIN customers c ON c.customer_id=o.customer_id "
                "JOIN order_items i ON i.order_id=o.order_id WHERE o.status='delivered' AND o.order_date >= '2026-05-01' GROUP BY c.city").fetchall()
ok = m.execute("SELECT c.city, SUM(o.amount), COUNT(DISTINCT o.customer_id) FROM orders o JOIN customers c ON c.customer_id=o.customer_id "
               "WHERE o.status='delivered' AND o.order_date >= '2026-05-01' GROUP BY c.city").fetchall()
print("\nmini example: with the order_items join", fan, "| without it", ok)
assert fan == [("Pune", 350.0, 1)] and ok == [("Pune", 150.0, 1)]
print("\nrecommended query (S5), exactly as run:\n" + S5)
```

**Output (my run):**
```text
rows: [300000, 20000, 900000]

== S0 baseline: strftime on date, no FK index, fan-out join, COUNT(DISTINCT) 
VM steps: 9,512,523   seconds (machine-specific, one run): 1.22   rows returned: 60
   plan: MATERIALIZE cm
   plan: SCAN i
   plan: SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
   plan: SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR count(DISTINCT)
   plan: SCAN cm
   plan: LIST SUBQUERY 2
   plan: SCAN cm
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR ORDER BY
   plan: USE TEMP B-TREE FOR ORDER BY

== S1 sargable date predicate (order_date >= literal) 
VM steps: 8,972,842   seconds (machine-specific, one run): 1.06   rows returned: 60
   plan: MATERIALIZE cm
   plan: SCAN i
   plan: SEARCH o USING INTEGER PRIMARY KEY (rowid=?)
   plan: SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR count(DISTINCT)
   plan: SCAN cm
   plan: LIST SUBQUERY 2
   plan: SCAN cm
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR ORDER BY
   plan: USE TEMP B-TREE FOR ORDER BY

== S2 + index on order_items(order_id) 
VM steps: 4,835,519   seconds (machine-specific, one run): 0.25   rows returned: 60
   plan: MATERIALIZE cm
   plan: SCAN o
   plan: SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   plan: SEARCH i USING COVERING INDEX ix_items_order (order_id=?)
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR count(DISTINCT)
   plan: SCAN cm
   plan: LIST SUBQUERY 2
   plan: SCAN cm
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR ORDER BY
   plan: USE TEMP B-TREE FOR ORDER BY

== S3 drop the unused order_items join (removes the fan-out) 
VM steps: 2,479,765   seconds (machine-specific, one run): 0.10   rows returned: 60
   plan: MATERIALIZE cm
   plan: SCAN o
   plan: SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR count(DISTINCT)
   plan: SCAN cm
   plan: LIST SUBQUERY 2
   plan: SCAN cm
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR ORDER BY
   plan: USE TEMP B-TREE FOR ORDER BY

== S4a wide SELECT o.*, c.* inside a CTE, otherwise S3 
VM steps: 2,479,765   seconds (machine-specific, one run): 0.09   rows returned: 60
   plan: MATERIALIZE cm
   plan: SCAN o
   plan: SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR count(DISTINCT)
   plan: SCAN cm
   plan: LIST SUBQUERY 3
   plan: SCAN cm
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR ORDER BY
   plan: USE TEMP B-TREE FOR ORDER BY

== S5 + covering index orders(status, order_date, customer_id, amount) 
VM steps: 1,311,137   seconds (machine-specific, one run): 0.07   rows returned: 60
   plan: MATERIALIZE cm
   plan: SEARCH o USING COVERING INDEX ix_ord_cov (status=? AND order_date>?)
   plan: SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR count(DISTINCT)
   plan: SCAN cm
   plan: LIST SUBQUERY 2
   plan: SCAN cm
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR ORDER BY
   plan: USE TEMP B-TREE FOR ORDER BY

== S6 pre-aggregate by customer and month, then join customers 
VM steps: 2,415,360   seconds (machine-specific, one run): 0.08   rows returned: 60
   plan: MATERIALIZE cm
   plan: MATERIALIZE pc
   plan: SEARCH orders USING COVERING INDEX ix_ord_cov (status=? AND order_date>?)
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: SCAN pc
   plan: SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: SCAN cm
   plan: LIST SUBQUERY 3
   plan: SCAN cm
   plan: USE TEMP B-TREE FOR GROUP BY
   plan: USE TEMP B-TREE FOR ORDER BY
   plan: USE TEMP B-TREE FOR ORDER BY

pandas expected rows: 60 | top-10 cities: ['City_02', 'City_07', 'City_10', 'City_11', 'City_13', 'City_19', 'City_26', 'City_27', 'City_35', 'City_39']
   city   month  revenue  customers
City_02 2026-05 22661.37        184
City_02 2026-06 23800.42        191
City_02 2026-07 21669.54        162
City_02 2026-08 20836.51        169
S3, S4a, S5, S6 equal pandas (compared after sorting by city, month)
S0 (fan-out) top-10 city set equals pandas? False | revenue equal? False
   inflation of revenue in S0 (first rows): [2.95, 2.89, 2.8, 3.01]
   S0 customers column equal on the shared city-months? False | orders with no items (dropped by the inner join): 14971
orders delivered in the window: 45568 | items per order mean: 3.00

steps summary: {'S0': 9512523, 'S1': 8972842, 'S2': 4835519, 'S3': 2479765, 'S4a': 2479765, 'S5': 1311137, 'S6': 2415360}

mini example: with the order_items join [('Pune', 350.0, 1)] | without it [('Pune', 150.0, 1)]

recommended query (S5), exactly as run:
/* S5 covering index on orders */
WITH cm AS (
 SELECT c.city AS city, strftime('%Y-%m', o.order_date) AS month,
        SUM(o.amount) AS revenue, COUNT(DISTINCT o.customer_id) AS customers
 FROM orders o JOIN customers c ON c.customer_id = o.customer_id
 WHERE o.status = 'delivered' AND o.order_date >= '2026-05-01'
 GROUP BY c.city, strftime('%Y-%m', o.order_date))
SELECT cm.city, cm.month, cm.revenue, cm.customers FROM cm
WHERE cm.city IN (SELECT city FROM cm GROUP BY city ORDER BY SUM(revenue) DESC LIMIT 10)
ORDER BY cm.city, cm.month
```

VM steps by step: S0 baseline 9,512,523; S1 sargable date 8,972,842; S2 plus index on `order_items(order_id)` 4,835,519; S3 drop the unused join 2,479,765; S4a wide `SELECT` inside a CTE 2,479,765 (no change); S5 covering index 1,311,137; S6 pre-aggregation 2,415,360 (worse than S5). Final results S3, S4a, S5 and S6 equal the pandas frame (60 rows: 10 cities times 6 months, compared after sorting by city and month); S0 does not.

**Edge cases:**
- The baseline's wrong answer is silent: it returns 60 plausible rows with inflated revenue and a different top-10 set, so fix correctness (the fan-out) before arguing about speed.
- Tied revenue at the 10th city would make the top 10 ambiguous; with random amounts there are no ties here, and a real report needs a tie-breaker column in the sort.
- `COUNT(DISTINCT customer_id)` per month is not additive across months: a customer in two months counts twice if you sum the months.
- A city with no delivered orders in the window simply has no rows; a calendar of all six months per city would need a join to a months table.
- The comparison `order_date >= '2026-05-01'` works on ISO text dates only because that format sorts as text; a different string format would break it.

**Then explain:**
- The loop: (1) baseline, record the plan, VM steps or time, and the result; (2) read the plan for scans, sorts, temp b-trees, join order; (3) change one thing; (4) re-measure; (5) re-check that the result is unchanged (or, for a bug like the fan-out, that it now matches an independent computation). Stop when the remaining cost is not where the time goes.
- What each step showed here, in order. `strftime` on the date column (S1): replacing it with a range on the raw column saved little (9.5M to 9.0M steps) because there was no index on `order_date` to unlock; the rewrite matters once an index exists. Missing foreign-key index (S2): the plan changed from `SCAN i` driving the join to `SCAN o` with an index probe `SEARCH i USING COVERING INDEX ix_items_order`, roughly halving the steps. Fan-out (S3): removing the unneeded `order_items` join halved the steps again and fixed the revenue. Unused columns (S4a): SQLite flattened the CTE and the step count did not change; in a row store that ships wide rows to a client or in a columnar engine the effect can differ, not run here. Covering index (S5): the plan became `SEARCH o USING COVERING INDEX ix_ord_cov (status=? AND order_date>?)`, the lowest count. Pre-aggregation (S6): per customer and month first, then join `customers`, was slightly worse than S5 in this engine at this size (2,415,360 against 1,311,137 steps), because the extra materialisation outweighed the cheaper join; it can win when the join side is much larger. Sort for the top-N: every plan still shows `USE TEMP B-TREE FOR ORDER BY`, but it sorts about 240 city-month rows, so it is not the cost; I did not try to remove it.
- This SQLite run does not reproduce 2 seconds versus 40 seconds: the baseline took about a second here. The loop transfers; the numbers do not.
- What to ask in a real system: table sizes and growth rate (what changed since last year), existing indexes and statistics freshness, the engine and version and its plan tool, how often the report runs and what runs concurrently, whether the date column is a real date type, and whether an exact answer is needed (a pre-computed summary table or materialised view may be the right fix; not executed here).
- Other engines (not executed here): the plan tools differ (PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`, MySQL `EXPLAIN`, SQL Server plans); the sargability and fan-out points carry over, the exact plan shapes do not.

**Follow-ups:**
- What if the table also needs `ANALYZE`? (Statistics can change the join order; I did not test it on this dataset.)
- How would you keep the report fast as data grows? (Summary table or incremental aggregation, partitioning by date; see Q32.)
- How do you prove the fix did not change results? (Assert against an independent computation, as done here.)

**Common mistakes:**
- Adding indexes first and never reading the plan.
- Fixing the speed of a query that returns the wrong revenue.
- Changing three things at once, so nothing is attributable.
- Trusting one wall-clock timing instead of repeating it or using a deterministic counter.
- Joining a child table "just in case" and aggregating a parent column.

### Q30 ⭐ 🟡 pandas groupby, merge, query and sorting performance choices: a seeded DataFrame of 500,000 rows (key with 1,000 values, category column with 4 values, value float) and a 1,000-row lookup table. Compare, with timings labelled machine-specific and equal results asserted: merge versus Series.map for adding one lookup column, groupby(sort=True) versus sort=False, groupby on a category column with observed=True or False, boolean mask versus df.query versus df.eval (and the 100,000-row guidance from the pandas docs), sort_values().head(k) versus nlargest(k), and an index-aligned operation versus a column operation. Show a chained assignment (df[df.a > 0]['b'] = 1) under pandas 3.0.5 copy-on-write: what happens to the original frame, and the .loc fix. Say which of these differences matter at which size.
**Asked at:** pandas user guide pages 'Enhancing performance' and 'Scaling to large datasets' (opened); official documentation, not candidate reports; data scientist and analytics engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** At 500,000 rows most of these choices differ by milliseconds, so choose by correctness and clarity (map for one lookup column, observed and sort stated explicitly, `.loc` for writes, `nlargest` for top-k) and keep the speed arguments for when sizes are much larger.

**Schema and sample data:**
```sql
-- the SQL cross-check in the run: t(key INTEGER, cat TEXT, value REAL) with 500,000 rows and lk(key INTEGER, label TEXT) with 1,000 rows
-- mini example for the hand walk: df = key 1,2,1 ; lookup = (1,'x'), (2,'y')
```
pandas: `df` has `key` (0 to 999), `cat` (category: a, b, c, d) and `value` (float), seeded with `default_rng(30)`; `lookup` has 1,000 rows.

**SQL answer:** the SQL equivalents of the merge and the groupby are checked in the Code block:
```sql
SELECT t.key, lk.label FROM t LEFT JOIN lk ON lk.key = t.key
SELECT key, SUM(value) AS v FROM t GROUP BY key ORDER BY key
```
(SQL has no `query`/`eval`/`map` distinction; the engine plans the join and group itself.)

**pandas answer:** the comparisons are in the Code block. Core forms:
```py
df.merge(lookup, on="key", how="left")
df["key"].map(lookup.set_index("key")["label"])
df.groupby("key", sort=False)["value"].sum()
df.query("value > 0.5 and key < 500")
df.nlargest(10, "value")
d.loc[d.a > 0, "b"] = 1
```

**Example:** with `df.key = [1, 2, 1]` and a lookup of 1 to x and 2 to y, both `merge(how='left')` and `map` give x, y, x in the original row order. If the lookup had two rows for key 1, `merge` would return four rows (the extra row is silently added) and `map` would raise an error (`InvalidIndexError` in my run, because the mapping index is not unique), which is the practical difference. For the chained assignment, `d = {a: [-1, 2, 3], b: [0, 0, 0]}`: `d[d.a > 0]['b'] = 1` writes to a temporary copy, so `b` stays `[0, 0, 0]`; `d.loc[d.a > 0, 'b'] = 1` gives `[0, 1, 1]`.

**Code:** run with `python3 -I`. Timings are the median of 5 timed repeats after one warm-up call, machine-specific, and noisy at the millisecond level.
```python
# Q30: pandas groupby/merge/query/sort choices. Timings: median of 5 repeats, machine-specific.
import sqlite3, time, warnings
import numpy as np
import pandas as pd

rng = np.random.default_rng(30)
n = 500_000
df = pd.DataFrame({"key": rng.integers(0, 1000, n),
                   "cat": pd.Categorical(np.array(list("abcd"))[rng.integers(0, 4, n)]),
                   "value": rng.normal(0, 1, n)})
lookup = pd.DataFrame({"key": np.arange(1000), "label": [f"L{i:04d}" for i in range(1000)]})

def t(fn, rep=5):
    xs = []
    fn()   # warm-up call, not timed
    for _ in range(rep):
        s = time.perf_counter(); r = fn(); xs.append(time.perf_counter() - s)
    return r, 1000 * float(np.median(xs))

def row(name, ms): print(f"  {name:<44}{ms:9.2f} ms")

print("1. add one lookup column")
m, ms1 = t(lambda: df.merge(lookup, on="key", how="left")); row("merge(how='left')", ms1)
mp, ms2 = t(lambda: df.assign(label=df["key"].map(lookup.set_index("key")["label"]))); row("Series.map on a keyed Series", ms2)
assert (m["label"].to_numpy() == mp["label"].to_numpy()).all() and len(m) == len(df)
print("   merge keeps row order for how='left' here:", bool((m["key"].to_numpy() == df["key"].to_numpy()).all()))
dup = pd.concat([lookup, lookup.iloc[:1]])
print("   duplicate key in lookup: merge rows", len(df.merge(dup, on="key", how="left")) - len(df), "extra;",
      "map raises:", end=" ")
try:
    df["key"].map(dup.set_index("key")["label"])
except Exception as e:
    print(type(e).__name__)

print("2. groupby sort")
g1, a = t(lambda: df.groupby("key")["value"].sum()); row("groupby('key', sort=True).sum", a)
g2, b = t(lambda: df.groupby("key", sort=False)["value"].sum()); row("groupby('key', sort=False).sum", b)
pd.testing.assert_series_equal(g1, g2.sort_index())
print("   same values after sort_index(); sort=False order is first appearance:", g2.index[:3].tolist())

print("3. groupby on the category column")
c1, a = t(lambda: df.groupby("cat", observed=True)["value"].sum()); row("category, observed=True", a)
c2, b = t(lambda: df.groupby("cat", observed=False)["value"].sum()); row("category, observed=False", b)
c3, c = t(lambda: df.assign(cs=df["cat"].astype(str)).groupby("cs")["value"].sum()); row("same column as str (incl. astype)", c)
pd.testing.assert_series_equal(c1, c2)
print("   default equals observed=True in 3.0.5:", c1.equals(df.groupby("cat")["value"].sum()),
      "| with an unused category observed=False adds a zero row:",
      df.assign(cat=df["cat"].cat.add_categories("z")).groupby("cat", observed=False)["value"].sum().loc["z"])

print("4. filter: mask vs query vs eval")
q1, a = t(lambda: df[(df["value"] > 0.5) & (df["key"] < 500)]); row("boolean mask", a)
q2, b = t(lambda: df.query("value > 0.5 and key < 500")); row("df.query", b)
q3, c = t(lambda: df[df.eval("value > 0.5 and key < 500")]); row("df[df.eval(...)]", c)
pd.testing.assert_frame_equal(q1, q2); pd.testing.assert_frame_equal(q1, q3)
small = df.iloc[:20_000]
_, a2 = t(lambda: small[(small["value"] > 0.5) & (small["key"] < 500)], 15)
_, b2 = t(lambda: small.query("value > 0.5 and key < 500"), 15)
print(f"   20,000 rows: mask {a2:.2f} ms vs query {b2:.2f} ms")
e1, a = t(lambda: df["value"] * 2 + df["key"]); row("arithmetic with plain operators", a)
e2, b = t(lambda: df.eval("value * 2 + key")); row("df.eval('value * 2 + key')", b)
assert np.allclose(e1, e2)

print("5. top k")
s1, a = t(lambda: df.sort_values("value", ascending=False).head(10)); row("sort_values(...).head(10)", a)
s2, b = t(lambda: df.nlargest(10, "value")); row("nlargest(10, 'value')", b)
assert s1["value"].tolist() == s2["value"].tolist()
print("   top value:", round(s2["value"].iloc[0], 4))

print("6. index-aligned vs column operation")
x = df["value"]; y = df["value"].sample(frac=1, random_state=1)    # same index labels, shuffled order
r1, a = t(lambda: x + y); row("x + y with the shuffled labels (aligns)", a)
r2, b = t(lambda: x + y.sort_index()); row("x + y.sort_index() (aligned, same order)", b)
r3, c = t(lambda: x.to_numpy() + y.to_numpy()); row("numpy: positional add (WRONG pairing)", c)
assert r1.equals(r2) and not np.allclose(r1.to_numpy(), r3)
print("   alignment pairs by label, positional add pairs by position: results differ (asserted)")

# SQL cross-check of the merge and groupby
con = sqlite3.connect(":memory:")
df.assign(cat=df["cat"].astype(str)).to_sql("t", con, index=False); lookup.to_sql("lk", con, index=False)
sj = pd.read_sql("SELECT t.key, lk.label FROM t LEFT JOIN lk ON lk.key = t.key", con)
assert sorted(sj["label"]) == sorted(m["label"])
sg = pd.read_sql("SELECT key, SUM(value) AS v FROM t GROUP BY key ORDER BY key", con).set_index("key")["v"]
assert np.allclose(sg.to_numpy(), g1.to_numpy())
con.close()
print("\nSQL LEFT JOIN labels and GROUP BY key sums equal pandas (sorted by key / label)")

print("\n7. chained assignment under pandas", pd.__version__)
d = pd.DataFrame({"a": [-1, 2, 3], "b": [0, 0, 0]})
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    d[d.a > 0]["b"] = 1
print("   after d[d.a > 0]['b'] = 1:", d["b"].tolist(), "| warnings:", [f"{x.category.__name__}" for x in w])
if w: print("   warning text:", str(w[0].message)[:230].replace("\n", " "))
d.loc[d.a > 0, "b"] = 1
print("   after d.loc[d.a > 0, 'b'] = 1:", d["b"].tolist())
sub = d[d.a > 0]; sub.loc[:, "b"] = 99
print("   writing to a filtered copy leaves the parent alone:", d["b"].tolist(), "| copy:", sub["b"].tolist())
```

**Output (my run):**
```text
1. add one lookup column
  merge(how='left')                               29.74 ms
  Series.map on a keyed Series                     8.50 ms
   merge keeps row order for how='left' here: True
   duplicate key in lookup: merge rows 513 extra; map raises: InvalidIndexError
2. groupby sort
  groupby('key', sort=True).sum                   10.32 ms
  groupby('key', sort=False).sum                  10.25 ms
   same values after sort_index(); sort=False order is first appearance: [105, 235, 754]
3. groupby on the category column
  category, observed=True                          5.90 ms
  category, observed=False                         2.66 ms
  same column as str (incl. astype)               31.93 ms
   default equals observed=True in 3.0.5: True | with an unused category observed=False adds a zero row: 0.0
4. filter: mask vs query vs eval
  boolean mask                                     3.17 ms
  df.query                                         5.77 ms
  df[df.eval(...)]                                 5.50 ms
   20,000 rows: mask 0.31 ms vs query 1.61 ms
  arithmetic with plain operators                  1.82 ms
  df.eval('value * 2 + key')                       3.42 ms
5. top k
  sort_values(...).head(10)                       28.97 ms
  nlargest(10, 'value')                            6.21 ms
   top value: 4.5214
6. index-aligned vs column operation
  x + y with the shuffled labels (aligns)         27.96 ms
  x + y.sort_index() (aligned, same order)        37.35 ms
  numpy: positional add (WRONG pairing)            0.78 ms
   alignment pairs by label, positional add pairs by position: results differ (asserted)

SQL LEFT JOIN labels and GROUP BY key sums equal pandas (sorted by key / label)

7. chained assignment under pandas 3.0.5
   after d[d.a > 0]['b'] = 1: [0, 0, 0] | warnings: ['ChainedAssignmentError']
   warning text: A value is being set on a copy of a DataFrame or Series through chained assignment. Such chained assignment never works to update the original DataFrame or Series, because the intermediate object on which we are setting values alw
   after d.loc[d.a > 0, 'b'] = 1: [0, 1, 1]
   writing to a filtered copy leaves the parent alone: [0, 1, 1] | copy: [99, 99]
```

**Edge cases:**
- Merge duplicates: a duplicate key in the lookup adds 513 rows to the result (500,000 rows over 1,000 keys, one duplicated key) while `map` raises. Missing keys give NaN in both.
- `groupby(sort=False)` returns groups in first-appearance order; the values equal the sorted result after `sort_index()` (asserted). In my run the two timings were about equal at 1,000 groups, so sorting 1,000 labels is not the cost.
- Categorical groupby in pandas 3.0.5: the default equals `observed=True`; `observed=False` only adds rows for unused categories (a zero row for an added category). In my run `observed=False` was faster than `observed=True` on a four-value category (2.66 against 5.90 ms), which I did not investigate; I would not choose between them on speed, choose on whether you need the empty groups.
- `query` and `eval` need the columns to be valid names and are strings, so refactoring tools cannot see them; both gave the same rows as the mask (asserted). Their documented purpose (the pandas 'Enhancing performance' guide, opened) is large frames: it gives roughly 100,000 rows as the size where `eval` starts to help. I did not reproduce that gain: at 500,000 rows my run had the mask at 3.17 ms against `query` 5.77 ms, and `eval('value * 2 + key')` at 3.42 ms against 1.82 ms for plain operators. numexpr is not installed here, so `eval` and `query` ran without that accelerator; the 100,000-row guidance assumes it is available, which may explain why I saw no gain.
- Alignment: `x + y` with a shuffled copy of the same labels aligned by label (correct, slower), the positional numpy add paired the wrong rows (results differ, asserted). With duplicate or missing labels alignment adds NaN or errors.
- `nlargest(10, "value")` with ties keeps the first by default (`keep="first"`), while `sort_values().head()` ties follow the sort's stability; the top values matched here (asserted).

**Then explain:**
- Merge versus map: `map` suits one lookup column with a unique key and returned the same labels in my run, faster here (8.50 against 29.74 ms); `merge` is for several columns or non-unique keys, and the row count change is the risk.
- `sort=True` versus `False`: use `sort=False` when order does not matter and the group count is large; keep `sort=True` when downstream code expects sorted keys.
- `nlargest(k)` avoids a full sort (6.21 against 28.97 ms here); for small k on big data it is the clearer choice.
- Which differences matter at which size: below about 100,000 rows none of the timings matter; at 500,000 rows the visible ones were map versus merge, nlargest versus full sort, and avoiding a string conversion before grouping (the groupby after a string conversion was several times slower than the category groupby in my run); the `query`, `eval` and sort choices were within a few milliseconds. At tens of millions of rows the algorithmic ones (sort versus partial sort, merge versus map memory) are the ones to revisit; I did not run that size.
- Chained assignment under pandas 3.0.5 copy-on-write: `d[d.a > 0]['b'] = 1` leaves `d` unchanged (`b` is still `[0, 0, 0]`) and emits a `ChainedAssignmentError` warning whose text says such chained assignment never works to update the original object. The `.loc` form updates the original (`[0, 1, 1]`). Writing to a filtered frame that you keep a name for changes only that copy. Earlier pandas versions sometimes updated the original and sometimes warned; that history is not run here.

**Follow-ups:**
- When would you use `merge_asof` or an index join instead? (Not run here.)
- How would `pd.Categorical` on `key` change the merge? (Not tested.)
- What changes at 50 million rows? (Memory first; consider a database or chunks, see Q28.)

**Common mistakes:**
- Treating a millisecond timing on one run as a real difference.
- A `merge` that silently multiplies rows because of a duplicate lookup key.
- Relying on `groupby` order when `sort=False`.
- Chained indexing for writes, which does nothing under copy-on-write.
- Assuming `query` is always faster than a boolean mask (it was slower at 500,000 rows here).

### Q31 ⭐ 🟡 Storage layout in SQLite: rowid tables versus WITHOUT ROWID, page counts and VACUUM. Create kv(a TEXT, b INTEGER, c TEXT, PRIMARY KEY (a, b)) as a rowid table and as WITHOUT ROWID with 100,000 seeded rows, print plans (USING INDEX sqlite_autoindex versus USING PRIMARY KEY), page_count and dbstat sizes of each, and show that a lookup on b alone scans. Then DELETE half the rows and show page_count does not shrink until VACUUM (freelist_count, PRAGMA auto_vacuum noted), and report the sizes before and after. Explain the docs' guidance (non-integer or composite keys with small rows benefit; single INTEGER PRIMARY KEY does not; no AUTOINCREMENT; the 1/20 of a page rule of thumb), and that this is the SQLite version of a clustered index (SQL Server clustered index and MySQL InnoDB clustered primary key, PostgreSQL heap plus CLUSTER, described, not executed).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** A WITHOUT ROWID table stores the rows inside the primary-key b-tree (SQLite's clustered-index form), which here halved the file for a composite text key with small rows, but it does not help a lookup on a non-leading key column, and deleting rows does not shrink the file until `VACUUM`.

**Schema and sample data:**
```sql
CREATE TABLE kv(a TEXT, b INTEGER, c TEXT, PRIMARY KEY (a, b));                 -- rowid table
CREATE TABLE kv(a TEXT, b INTEGER, c TEXT, PRIMARY KEY (a, b)) WITHOUT ROWID;   -- clustered by (a, b)
-- 100,000 seeded rows: a is one of 2,000 text keys, b = 0 to 99,999 (unique), c is a 3-character text
```

**SQL answer:** the statements run in the Code block (the same text is used for both layouts):
```sql
SELECT c FROM kv WHERE a = 'key_0007' AND b = 12345
SELECT c FROM kv WHERE b = 12345
SELECT name, COUNT(*), SUM(pgsize) FROM dbstat WHERE name IN ('kv') OR name LIKE 'sqlite_autoindex%' GROUP BY name
DELETE FROM kv WHERE b % 2 = 1
VACUUM
```

**pandas answer:** pandas holds the same rows and answers the lookups by boolean mask; the Code block asserts both layouts return what pandas finds:
```py
exp = sorted(data.loc[mask, "c"])
```

**Example:** the rowid table keeps two b-trees: the table itself (580 pages) and the automatic index `sqlite_autoindex_kv_1` on (a, b) (548 pages), plus one header page, which is the 1,129 pages printed. The WITHOUT ROWID table has one b-tree of 564 pages plus the header, 565 pages: the key columns are stored once. A lookup on `a` and `b` therefore searches the index and then fetches the row by rowid in the first layout (`USING INDEX sqlite_autoindex_kv_1`) and goes straight to the row in the second (`USING PRIMARY KEY`).

**Code:** run with `python3 -I`.
```python
# Q31: rowid table vs WITHOUT ROWID, page counts, DELETE and VACUUM (file databases in a temp dir).
import os, sqlite3, tempfile
import numpy as np
import pandas as pd

rng = np.random.default_rng(31)
N = 100_000
a = np.array([f"key_{i:04d}" for i in range(2000)])[rng.integers(0, 2000, N)]
b = np.arange(N)                     # unique b makes (a, b) unique
c = np.array([f"v{i % 97:02d}" for i in range(N)])
data = pd.DataFrame({"a": a, "b": b, "c": c})
rows = list(data.itertuples(index=False, name=None))
tmp = tempfile.mkdtemp()

def build(kind, big=False):
    path = os.path.join(tmp, f"{kind}{'_big' if big else ''}.db")
    con = sqlite3.connect(path)
    wr = " WITHOUT ROWID" if kind == "norowid" else ""
    con.execute(f"CREATE TABLE kv(a TEXT, b INTEGER, c TEXT, PRIMARY KEY (a, b)){wr}")
    payload = rows if not big else [(x, y, z * 100) for x, y, z in rows[:20_000]]
    con.executemany("INSERT INTO kv VALUES (?,?,?)", payload)
    con.commit()
    return con

def stats(con):
    pc = con.execute("PRAGMA page_count").fetchone()[0]
    ps = con.execute("PRAGMA page_size").fetchone()[0]
    fl = con.execute("PRAGMA freelist_count").fetchone()[0]
    return pc, ps, fl

def dbstat(con):
    return {r[0]: (r[1], r[2]) for r in con.execute(
        "SELECT name, COUNT(*), SUM(pgsize) FROM dbstat WHERE name IN ('kv') OR name LIKE 'sqlite_autoindex%' GROUP BY name")}

def plan(con, sql): return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

cons = {k: build(k) for k in ("rowid", "norowid")}
print("auto_vacuum:", cons["rowid"].execute("PRAGMA auto_vacuum").fetchone()[0], "(0 = NONE, the default)")
Q_AB = "SELECT c FROM kv WHERE a = 'key_0007' AND b = 12345"
Q_B = "SELECT c FROM kv WHERE b = 12345"
for k, con in cons.items():
    print(f"\n[{k}]")
    print("  plan a+b:", plan(con, Q_AB)); print("  plan b only:", plan(con, Q_B))
    pc, ps, fl = stats(con)
    print(f"  page_count {pc}, page_size {ps}, bytes {pc * ps:,}, freelist {fl}")
    print("  dbstat (pages, bytes) per b-tree:", dbstat(con))

# same answers from both layouts and from pandas
for q, mask in ((Q_AB, (data.a == "key_0007") & (data.b == 12345)), (Q_B, data.b == 12345)):
    exp = sorted(data.loc[mask, "c"])
    for k, con in cons.items():
        assert sorted(r[0] for r in con.execute(q)) == exp
print("\nlookups equal pandas on both layouts")

# rows with a big payload: the 1/20 page rule of thumb (4096 / 20 = about 204 bytes)
big = {k: build(k, big=True) for k in ("rowid", "norowid")}
print("\n20,000 rows with a 300-byte c column:", {k: stats(v)[0] for k, v in big.items()}, "pages")

# DELETE half, then VACUUM
print("\nDELETE half the rows (b odd), then VACUUM")
for k, con in cons.items():
    before = stats(con)
    con.execute("DELETE FROM kv WHERE b % 2 = 1"); con.commit()
    mid = stats(con)
    n_left = con.execute("SELECT COUNT(*) FROM kv").fetchone()[0]
    con.execute("VACUUM")
    after = stats(con)
    print(f"  {k}: rows left {n_left}; pages before {before[0]}, after DELETE {mid[0]} (freelist {mid[2]}), after VACUUM {after[0]} (freelist {after[2]});"
          f" file bytes after VACUUM {after[0] * after[1]:,}")
    assert n_left == N // 2
for con in list(cons.values()) + list(big.values()): con.close()
```

**Output (my run):**
```text
auto_vacuum: 0 (0 = NONE, the default)

[rowid]
  plan a+b: ['SEARCH kv USING INDEX sqlite_autoindex_kv_1 (a=? AND b=?)']
  plan b only: ['SCAN kv']
  page_count 1129, page_size 4096, bytes 4,624,384, freelist 0
  dbstat (pages, bytes) per b-tree: {'kv': (580, 2375680), 'sqlite_autoindex_kv_1': (548, 2244608)}

[norowid]
  plan a+b: ['SEARCH kv USING PRIMARY KEY (a=? AND b=?)']
  plan b only: ['SCAN kv']
  page_count 565, page_size 4096, bytes 2,314,240, freelist 0
  dbstat (pages, bytes) per b-tree: {'kv': (564, 2310144)}

lookups equal pandas on both layouts

20,000 rows with a 300-byte c column: {'rowid': 1773, 'norowid': 1916} pages

DELETE half the rows (b odd), then VACUUM
  rowid: rows left 50000; pages before 1129, after DELETE 1129 (freelist 21), after VACUUM 543 (freelist 0); file bytes after VACUUM 2,224,128
  norowid: rows left 50000; pages before 565, after DELETE 565 (freelist 29), after VACUUM 257 (freelist 0); file bytes after VACUUM 1,052,672
```

**Edge cases:**
- A lookup on `b` alone is `SCAN kv` in both layouts: `b` is not the leftmost column of the key, so neither b-tree can seek on it (queries on a trailing key column need their own index).
- Large rows: with a 300-byte `c` (20,000 rows) the WITHOUT ROWID table used more pages than the rowid table (1,916 against 1,773). That is the documented guidance showing up: WITHOUT ROWID suits small rows, because wide rows inside the key b-tree reduce how many keys fit per page, and the docs' rule of thumb is that rows over about one-twentieth of a page (about 200 bytes at 4,096) tend to do worse. I read this from the docs and checked the direction with one run, not the exact threshold.
- `DELETE` of half the rows left `page_count` unchanged (1,129 and 565) with only 21 and 29 free pages, because the pages are half empty, not free. `PRAGMA auto_vacuum` was 0 (NONE): with that default the file never shrinks by itself; with other `auto_vacuum` settings free pages can be released at commit (documented, not run here, and it does not defragment half-empty pages).
- After `VACUUM` the files shrank to 543 and 257 pages (2,224,128 and 1,052,672 bytes), freelist 0. `VACUUM` rewrites the whole file, needs temporary disk space and an exclusive lock, so it is a maintenance operation.
- A single `INTEGER PRIMARY KEY` is already the rowid, so WITHOUT ROWID adds nothing there (docs); do not add `AUTOINCREMENT` unless you need never-reused ids, and it is not available on WITHOUT ROWID tables.

**Then explain:**
- The docs' guidance (SQLite WITHOUT ROWID page, opened): a non-integer or composite primary key with small rows benefits; a single INTEGER primary key does not; no AUTOINCREMENT; the one-twentieth-of-a-page rule of thumb for row size.
- This is SQLite's clustered index: the table data is the primary-key b-tree, so range scans on the key read neighbouring rows from neighbouring pages. Other engines, described and not executed here: SQL Server has one clustered index per table (data ordered by that key) and nonclustered indexes pointing to it; MySQL InnoDB always clusters on the primary key and its secondary indexes carry the primary key value; PostgreSQL tables are heaps, and `CLUSTER` reorders a table once by an index without keeping it ordered afterwards.
- Why the rowid layout costs space: the key is stored in the table (as columns) and again in the autoindex, and every autoindex entry also carries the rowid.
- Space is not returned by `DELETE`: SQLite reuses free pages for new rows, so the file stays as large as the high-water mark until `VACUUM`.

**Follow-ups:**
- What does `dbstat` report for `freelist` pages? (Free pages are not part of any b-tree; `PRAGMA freelist_count` gave 21 and 29.)
- Would an extra index on `b` help the `b` lookup, and what does it cost in space? (Not run in this answer; an extra index would add pages and write cost.)
- How would you choose the page size? (Not run.)

**Common mistakes:**
- Using WITHOUT ROWID for wide rows or for a single integer key.
- Expecting `DELETE` to shrink the database file.
- Expecting a lookup on the second key column to use the composite primary key.
- Running `VACUUM` on a live database without budgeting the extra disk and the lock.

### Q32 ⭐ 🔴 Partitioning, pruning and clustering at concept level, with an emulation. events(event_id, user_id, event_time, event_type, payload) has 2 billion rows in a warehouse or OLTP database; most queries filter on a date range, some on user_id. Explain range, list and hash partitioning, what partition pruning needs (a predicate on the partition key in a form the optimiser can evaluate: a function or implicit cast on the key can defeat it), partition-wise indexes (local versus global), the small-partitions problem, how partitioning helps deletes and retention (drop a partition), and how it differs from an index. Cover clustering or sort keys (BigQuery clustering, Snowflake micro-partition pruning and clustering keys, Redshift sort and distribution keys), columnar storage (read only needed columns, compression) and materialised views, all hedged as not executed with no vendor numbers. Emulate pruning in SQLite with monthly tables ev_2024_01 ... and a UNION ALL view: print the plans for a one-month filter and a cross-month filter (SQLite probes every branch of the view with its own index; say what you observe) and show that a query that names the right table directly touches only that table.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; Partitioning and clustering and parameter-sniffing explainers (Dataford, a Substack post, Medium, SQLServerCentral, SQLShack, Red Gate; search snippets only, not opened); guides, not candidate reports; data engineer rounds at product companies and GCCs
**Say this first (1 line):** Partitioning splits one logical table so the engine can skip whole pieces (pruning) and drop old data cheaply, but pruning only works when the query's predicate is on the partition key in a form the optimiser can evaluate; SQLite has no partitioning, and my monthly-table emulation shows it probes every branch of the view while a query that names the right table touches one.

**Schema and sample data:**
```sql
CREATE TABLE ev_2024_01(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT, event_type TEXT);
CREATE INDEX ix_2024_01_time ON ev_2024_01(event_time);
CREATE INDEX ix_2024_01_user ON ev_2024_01(user_id);
-- the same for ev_2024_02 ... ev_2024_06; 60,000 seeded rows over six months
CREATE VIEW ev AS SELECT * FROM ev_2024_01 UNION ALL SELECT * FROM ev_2024_02 UNION ALL ... SELECT * FROM ev_2024_06;
```
The run builds this twice, once with `CHECK (event_time >= 'first of month' AND event_time < 'first of next month')` on each table.

**SQL answer:** the queries run in the Code block (same text as `one_view`, `cross_view`, `direct`, `by_user`):
```sql
SELECT COUNT(event_type) FROM ev WHERE event_time >= '2024-03-01' AND event_time < '2024-04-01'
SELECT COUNT(event_type) FROM ev WHERE event_time >= '2024-03-15' AND event_time < '2024-04-15'
SELECT COUNT(event_type) FROM ev_2024_03 WHERE event_time >= '2024-03-01' AND event_time < '2024-04-01'
SELECT COUNT(*) FROM ev WHERE user_id = 42
```

**pandas answer:** the expected counts come from the unpartitioned frame:
```py
exp_one = int(((ev.event_time >= "2024-03-01") & (ev.event_time < "2024-04-01")).sum())
```

**Example:** the six monthly tables hold 10,211, 9,606, 10,123, 9,811, 10,267 and 9,982 rows (60,000 in all). March has 10,123 rows, so the one-month query returns 10,123 whichever way it is written. Through the view the plan lists a `SEARCH` on all six tables (five of the ranges are empty); written against `ev_2024_03` directly there is one `SEARCH` and the cross-month query (15 March to 15 April) must touch two tables, which only the view or a `UNION ALL` of the two tables can do. The user query (`user_id = 42`) has no month in it, so every month has to be searched, with any layout; there are 10 such rows.

**Code:** run with `python3 -I`.
```python
# Q32: emulate partition pruning with monthly tables and a UNION ALL view in SQLite.
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(32)
months = [f"2024_{m:02d}" for m in range(1, 7)]
N = 60_000
t0 = pd.Timestamp("2024-01-01")
secs = rng.integers(0, 182 * 86400, N)           # Jan 1 to Jun 30
ev = pd.DataFrame({"event_id": np.arange(1, N + 1), "user_id": rng.integers(1, 5001, N),
                   "event_time": (t0 + pd.to_timedelta(secs, unit="s")).strftime("%Y-%m-%d %H:%M:%S"),
                   "event_type": np.array(["view", "click", "buy"])[rng.integers(0, 3, N)]})
ev["mon"] = ev["event_time"].str[:7].str.replace("-", "_")

def build(with_check):
    con = sqlite3.connect(":memory:")
    for m in months:
        lo, hi = m.replace("_", "-") + "-01", None
        nxt = (pd.Timestamp(lo) + pd.offsets.MonthBegin(1)).strftime("%Y-%m-%d")
        chk = f", CHECK (event_time >= '{lo}' AND event_time < '{nxt}')" if with_check else ""
        con.execute(f"CREATE TABLE ev_{m}(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT, event_type TEXT{chk})")
        con.execute(f"CREATE INDEX ix_{m}_time ON ev_{m}(event_time)")
        con.execute(f"CREATE INDEX ix_{m}_user ON ev_{m}(user_id)")
        part = ev[ev.mon == m]
        con.executemany(f"INSERT INTO ev_{m} VALUES (?,?,?,?)", part.iloc[:, :4].itertuples(index=False, name=None))
    con.execute("CREATE VIEW ev AS " + " UNION ALL ".join(f"SELECT * FROM ev_{m}" for m in months))
    con.commit()
    return con

def plan(con, sql): return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

def steps(con, sql):
    c = [0]
    def cb(): c[0] += 1; return 0
    con.set_progress_handler(cb, 1); r = con.execute(sql).fetchall(); con.set_progress_handler(None, 0)
    return c[0], r

one_view = "SELECT COUNT(event_type) FROM ev WHERE event_time >= '2024-03-01' AND event_time < '2024-04-01'"
cross_view = "SELECT COUNT(event_type) FROM ev WHERE event_time >= '2024-03-15' AND event_time < '2024-04-15'"
direct = "SELECT COUNT(event_type) FROM ev_2024_03 WHERE event_time >= '2024-03-01' AND event_time < '2024-04-01'"
by_user = "SELECT COUNT(*) FROM ev WHERE user_id = 42"

exp_one = int(((ev.event_time >= "2024-03-01") & (ev.event_time < "2024-04-01")).sum())
exp_cross = int(((ev.event_time >= "2024-03-15") & (ev.event_time < "2024-04-15")).sum())
exp_user = int((ev.user_id == 42).sum())
for label, with_check in (("no CHECK constraints", False), ("with CHECK constraints on event_time", True)):
    con = build(with_check)
    print(f"\n=== {label}")
    for name, q, exp in (("one month via view", one_view, exp_one), ("cross-month via view", cross_view, exp_cross),
                         ("one month, table named directly", direct, exp_one), ("user_id=42 via view", by_user, exp_user)):
        n_steps, r = steps(con, q)
        assert r[0][0] == exp
        print(f"-- {name}: count {r[0][0]} (pandas {exp}), VM steps {n_steps:,}")
        print("      plan:", " / ".join(p.replace("USING ", "").replace("INDEX ", "") for p in plan(con, q)))
    if not with_check:
        con.execute("CREATE VIEW ev_one AS SELECT * FROM ev_2024_03")
        q = one_view.replace("FROM ev WHERE", "FROM ev_one WHERE")
        n_steps, r = steps(con, q)
        assert r[0][0] == exp_one
        print(f"-- one month via a ONE-branch view (isolates the view overhead): VM steps {n_steps:,}")
    con.close()
print("rows per monthly table:", {m: int((ev.mon == m).sum()) for m in months}, "total", len(ev))
print("\nall counts equal pandas")
```

**Output (my run):**
```text

=== no CHECK constraints
-- one month via view: count 10123 (pandas 10123), VM steps 162,039
      plan: CO-ROUTINE ev / COMPOUND QUERY / LEFT-MOST SUBQUERY / SEARCH ev_2024_01 ix_2024_01_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_02 ix_2024_02_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_03 ix_2024_03_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_04 ix_2024_04_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_05 ix_2024_05_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_06 ix_2024_06_time (event_time>? AND event_time<?) / SCAN ev
-- cross-month via view: count 10069 (pandas 10069), VM steps 161,175
      plan: CO-ROUTINE ev / COMPOUND QUERY / LEFT-MOST SUBQUERY / SEARCH ev_2024_01 ix_2024_01_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_02 ix_2024_02_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_03 ix_2024_03_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_04 ix_2024_04_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_05 ix_2024_05_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_06 ix_2024_06_time (event_time>? AND event_time<?) / SCAN ev
-- one month, table named directly: count 10123 (pandas 10123), VM steps 50,632
      plan: SEARCH ev_2024_03 ix_2024_03_time (event_time>? AND event_time<?)
-- user_id=42 via view: count 10 (pandas 10), VM steps 174
      plan: CO-ROUTINE ev / COMPOUND QUERY / LEFT-MOST SUBQUERY / SEARCH ev_2024_01 ix_2024_01_user (user_id=?) / UNION ALL / SEARCH ev_2024_02 ix_2024_02_user (user_id=?) / UNION ALL / SEARCH ev_2024_03 ix_2024_03_user (user_id=?) / UNION ALL / SEARCH ev_2024_04 ix_2024_04_user (user_id=?) / UNION ALL / SEARCH ev_2024_05 ix_2024_05_user (user_id=?) / UNION ALL / SEARCH ev_2024_06 ix_2024_06_user (user_id=?) / SCAN ev
-- one month via a ONE-branch view (isolates the view overhead): VM steps 50,632

=== with CHECK constraints on event_time
-- one month via view: count 10123 (pandas 10123), VM steps 162,039
      plan: CO-ROUTINE ev / COMPOUND QUERY / LEFT-MOST SUBQUERY / SEARCH ev_2024_01 ix_2024_01_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_02 ix_2024_02_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_03 ix_2024_03_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_04 ix_2024_04_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_05 ix_2024_05_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_06 ix_2024_06_time (event_time>? AND event_time<?) / SCAN ev
-- cross-month via view: count 10069 (pandas 10069), VM steps 161,175
      plan: CO-ROUTINE ev / COMPOUND QUERY / LEFT-MOST SUBQUERY / SEARCH ev_2024_01 ix_2024_01_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_02 ix_2024_02_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_03 ix_2024_03_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_04 ix_2024_04_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_05 ix_2024_05_time (event_time>? AND event_time<?) / UNION ALL / SEARCH ev_2024_06 ix_2024_06_time (event_time>? AND event_time<?) / SCAN ev
-- one month, table named directly: count 10123 (pandas 10123), VM steps 50,632
      plan: SEARCH ev_2024_03 ix_2024_03_time (event_time>? AND event_time<?)
-- user_id=42 via view: count 10 (pandas 10), VM steps 174
      plan: CO-ROUTINE ev / COMPOUND QUERY / LEFT-MOST SUBQUERY / SEARCH ev_2024_01 ix_2024_01_user (user_id=?) / UNION ALL / SEARCH ev_2024_02 ix_2024_02_user (user_id=?) / UNION ALL / SEARCH ev_2024_03 ix_2024_03_user (user_id=?) / UNION ALL / SEARCH ev_2024_04 ix_2024_04_user (user_id=?) / UNION ALL / SEARCH ev_2024_05 ix_2024_05_user (user_id=?) / UNION ALL / SEARCH ev_2024_06 ix_2024_06_user (user_id=?) / SCAN ev
rows per monthly table: {'2024_01': 10211, '2024_02': 9606, '2024_03': 10123, '2024_04': 9811, '2024_05': 10267, '2024_06': 9982} total 60000

all counts equal pandas
```

**Edge cases:**
- What I observed: SQLite probes every branch of the view with that branch's own index, for both the one-month and the cross-month filter. The `CHECK` constraints made no difference to the plan or the step counts (identical in both runs), so SQLite did not use them to skip tables in this test; it is the view, not the planner, that lacks partition knowledge.
- The view costs more than naming the table: 162,039 VM steps through the view against 50,632 for the table named directly, for the same 10,123 rows. A view with only the March branch also took 50,632 steps, so the extra is not the five empty probes; it is the compound-query machinery moving every row through the view (my inference from that comparison, not a documented explanation).
- A filter that wraps the key in a function (`strftime(...)`, or `substr(event_time, 1, 7) = '2024-03'`) would defeat the index range in each branch; I did not run it in this answer (function-on-column plans are covered elsewhere in this part).
- Rows landing in the wrong monthly table are impossible for a real partitioned table, but a hand-made set of tables relies on the loader and the CHECK to be correct.

**Then explain:** (everything below that is not SQLite is not executed here, with no vendor numbers)
- Range, list and hash partitioning: range puts rows with key ranges (days, months) in separate partitions, list puts named values (a region) in each, and hash spreads rows evenly over a fixed number of partitions by hashing a key (good for even sizes and point lookups, useless for range pruning).
- What pruning needs: a predicate on the partition key that the optimiser can evaluate at planning or run time, such as a range on the date column. A function on the key (`WHERE DATE(event_time) = ...`), an implicit cast of the key to another type, or a condition on a different column can defeat it, so the engine reads every partition.
- Local versus global indexes: a local index is split along the same partitions (maintenance is per partition, a partition can be dropped or loaded with its index); a global index spans all partitions (efficient for lookups on a non-key column but heavier to maintain when a partition is dropped), and which engines offer which varies.
- The small-partitions problem: thousands of tiny partitions (per hour, per user) add planning overhead, metadata and many small files; choose a grain where partitions hold a meaningful amount of data.
- Deletes and retention: dropping or detaching an old partition is a metadata operation, whereas `DELETE ... WHERE event_time < ...` on a huge table writes and logs every row (and can bloat or lock; see Q35).
- Partitioning versus an index: an index is an extra ordered structure that lets the engine find rows fast within a table; partitioning is a physical layout that lets it skip whole chunks and manage them separately. They combine (a local index inside each partition), and a partition key with a query that does not use it gives no benefit.
- Clustering and sort keys: BigQuery clustering sorts data within a table or partition by chosen columns so filters on them read fewer blocks; Snowflake stores data in micro-partitions with min and max metadata, prunes by that metadata, and offers clustering keys for large tables; Redshift has sort keys and distribution keys (the latter chooses which node holds a row, which matters for joins). I describe these from general knowledge and did not run or benchmark any of them.
- Columnar storage and materialised views: columnar formats read only the needed columns and compress similar values well; a materialised view stores a precomputed query result that is refreshed on a schedule or incrementally, trading freshness and storage for speed. All not executed here.
- For 2 billion rows: partition by event date (retention and date filters), consider clustering or a secondary index on `user_id` for the user queries, and test with the real engine's plan tool, since this SQLite emulation shows the idea, not the engine behaviour.

**Follow-ups:**
- What if most queries filter on `user_id`? (Partition or cluster by it, or by a hash of it; date partitioning no longer helps those queries, as the `user_id` plan above shows.)
- How do you add next month's partition and drop old ones safely? (Create it ahead of time; detach or drop the oldest; automate and test.)
- What about skew? (A hot partition or a hash with few distinct values; not run here.)

**Common mistakes:**
- Partitioning by a column the queries do not filter on.
- Wrapping the partition key in a function or cast in the WHERE clause.
- Thousands of tiny partitions.
- Thinking SQLite prunes a UNION ALL view (it did not here), or that partitioning replaces indexes.
- Quoting vendor speed-ups without a measurement.

### Q33 ⭐ 🔴 Plans in other engines and join algorithms: given only text descriptions (not executed), explain how to read PostgreSQL EXPLAIN (ANALYZE, BUFFERS) (cost, rows, width, actual time, loops, shared hit versus read, estimate-versus-actual row gaps), MySQL EXPLAIN with the type, key, key_len, rows, filtered and Extra columns and EXPLAIN FORMAT=JSON, and a SQL Server graphical plan (index seek versus scan, key lookup, estimated versus actual rows, spills). Compare nested-loop, hash and merge joins (when each wins, memory use, sorted inputs), bitmap index scans, and index-only scans, and contrast with what SQLite actually prints (nested loops, automatic index, bloom filter, co-routine, materialize; run three example plans). Explain why EXPLAIN ANALYZE executes the statement (wrap writes in a transaction you roll back) and that plan text is not a stable interface. No vendor numbers.
**Asked at:** PostgreSQL docs using-explain and indexes-multicolumn and MySQL EXPLAIN output page (opened, used for contrast only); official documentation, not candidate reports; product company and GCC data engineer rounds; Partitioning and clustering and parameter-sniffing explainers (Dataford, a Substack post, Medium, SQLServerCentral, SQLShack, Red Gate; search snippets only, not opened); guides, not candidate reports; data engineer rounds at product companies and GCCs
**Say this first (1 line):** Read a plan from the inside out and compare estimated with actual rows; the join algorithm (nested loop, hash, merge) follows from the sizes, the indexes and the sort order, and SQLite prints only a simple nested-loop family, so the other engines' plan reading below is described, not executed.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);   -- 2,000 rows, 4 cities
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);   -- 20,000 rows
CREATE INDEX ix_o_cust ON orders(customer_id);
CREATE TABLE a(x INTEGER, k INTEGER);   -- 3,000 rows, no index
CREATE TABLE b(y INTEGER, k INTEGER);   -- 3,000 rows, no index
```

**SQL answer:** four statements whose plans are printed in the Code block (same text as `q1` to `q4`):
```sql
SELECT c.name, o.amount FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE c.city = 'Pune'
SELECT COUNT(*) FROM a JOIN b ON b.k = a.k
WITH t AS (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT t1.customer_id, t1.s FROM t t1 WHERE t1.s > (SELECT AVG(s) FROM t) ORDER BY t1.customer_id
SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE s > 6000
```

**pandas answer:** pandas `merge` is the equivalent of the first two joins and a `groupby` the others; the Code block asserts they match:
```py
e1 = cust[cust.city == "Pune"].merge(orders, on="customer_id")[["name", "amount"]]
assert n2 == len(A.merge(B, on="k"))
```

**Example:** plan 1 is a plain nested loop: scan the (filtered) customers, and for each one probe the index `ix_o_cust` on `customer_id=?`; 5,010 order rows come back for the Pune customers. Plan 2 has no usable index on either side, so SQLite builds a temporary `AUTOMATIC COVERING INDEX` on `b(k)` for the duration of the query and probes it for each row of `a`, with a `BLOOM FILTER` in front to skip keys that cannot match (17,841 matching pairs). Plan 3 computes the grouped CTE once (`MATERIALIZE t`) because it is used twice, and plan 4 (grouped subquery used once) is a `CO-ROUTINE`: rows are produced on demand and not stored.

**Code:** run with `python3 -I`.
```python
# Q33: three real SQLite plans (nested loop + index, automatic index / bloom filter, co-routine / materialize)
# and the rollback pattern for statements that execute.
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(33)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE a(x INTEGER, k INTEGER);
CREATE TABLE b(y INTEGER, k INTEGER);
""")
cust = pd.DataFrame({"customer_id": range(1, 2001), "name": [f"c{i}" for i in range(1, 2001)],
                     "city": np.array(["Pune", "Delhi", "Chennai", "Kolkata"])[rng.integers(0, 4, 2000)]})
orders = pd.DataFrame({"order_id": range(1, 20001), "customer_id": rng.integers(1, 2001, 20000),
                       "amount": rng.integers(10, 500, 20000)})
A = pd.DataFrame({"x": range(3000), "k": rng.integers(0, 500, 3000)})
B = pd.DataFrame({"y": range(3000), "k": rng.integers(0, 500, 3000)})
for nm, d in (("customers", cust), ("orders", orders), ("a", A), ("b", B)):
    con.executemany(f"INSERT INTO {nm} VALUES ({','.join('?' * d.shape[1])})", d.itertuples(index=False, name=None))
con.execute("CREATE INDEX ix_o_cust ON orders(customer_id)")

def plan(sql): return [(r[3]) for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

q1 = "SELECT c.name, o.amount FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE c.city = 'Pune'"
q2 = "SELECT COUNT(*) FROM a JOIN b ON b.k = a.k"
q3 = ("WITH t AS (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) "
      "SELECT t1.customer_id, t1.s FROM t t1 WHERE t1.s > (SELECT AVG(s) FROM t) ORDER BY t1.customer_id")

print("Plan 1: nested loop with an index probe on the inner table")
for p in plan(q1): print("   ", p)
print("Plan 2: no index on either side -> automatic index (before ANALYZE)")
for p in plan(q2): print("   ", p)
con.execute("ANALYZE")
print("Plan 2 after ANALYZE (a new statement text is used so no cached plan is reused):")
for p in plan(q2 + " /* after analyze */"): print("   ", p)
print("Plan 3: a CTE used twice -> MATERIALIZE plus a scalar subquery")
for p in plan(q3): print("   ", p)

q4 = "SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE s > 6000"
print("Plan 4: a grouped subquery used once -> co-routine instead of materialising")
for p in plan(q4): print("   ", p)
assert len(con.execute(q4).fetchall()) == int((orders.groupby("customer_id")["amount"].sum() > 6000).sum())

# results equal pandas
r1 = pd.read_sql(q1, con).sort_values(["name", "amount"]).reset_index(drop=True)
e1 = cust[cust.city == "Pune"].merge(orders, on="customer_id")[["name", "amount"]].sort_values(["name", "amount"]).reset_index(drop=True)
pd.testing.assert_frame_equal(r1, e1, check_dtype=False)
n2 = con.execute(q2).fetchone()[0]
assert n2 == len(A.merge(B, on="k"))
r3 = pd.read_sql(q3, con)
t = orders.groupby("customer_id")["amount"].sum()
e3 = t[t > t.mean()].reset_index().rename(columns={"amount": "s"}).sort_values("customer_id").reset_index(drop=True)
pd.testing.assert_frame_equal(r3, e3, check_dtype=False)
print(f"\nrows: plan1 {len(r1)}, plan2 count {n2}, plan3 {len(r3)}; all equal to pandas merge/groupby (sorted by name, amount / customer_id)")

con.commit()
# EXPLAIN in SQLite does not execute; the rollback pattern for statements that do
before = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
con.execute("EXPLAIN QUERY PLAN DELETE FROM orders WHERE amount < 100").fetchall()
mid = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
con.execute("BEGIN"); con.execute("DELETE FROM orders WHERE amount < 100")
inside = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
con.execute("ROLLBACK")
after = con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
print("orders rows: before", before, "| after EXPLAIN QUERY PLAN DELETE", mid, "| inside BEGIN..DELETE", inside, "| after ROLLBACK", after)
print("SQLite version:", sqlite3.sqlite_version)
```

**Output (my run):**
```text
Plan 1: nested loop with an index probe on the inner table
    SCAN c
    SEARCH o USING INDEX ix_o_cust (customer_id=?)
Plan 2: no index on either side -> automatic index (before ANALYZE)
    SCAN a
    BLOOM FILTER ON b (k=?)
    SEARCH b USING AUTOMATIC COVERING INDEX (k=?)
Plan 2 after ANALYZE (a new statement text is used so no cached plan is reused):
    SCAN a
    BLOOM FILTER ON b (k=?)
    SEARCH b USING AUTOMATIC COVERING INDEX (k=?)
Plan 3: a CTE used twice -> MATERIALIZE plus a scalar subquery
    MATERIALIZE t
    SCAN orders USING INDEX ix_o_cust
    SCAN t1
    SCALAR SUBQUERY 2
    SCAN t
    USE TEMP B-TREE FOR ORDER BY
Plan 4: a grouped subquery used once -> co-routine instead of materialising
    CO-ROUTINE (subquery-1)
    SCAN orders USING INDEX ix_o_cust
    SCAN (subquery-1)

rows: plan1 5010, plan2 count 17841, plan3 975; all equal to pandas merge/groupby (sorted by name, amount / customer_id)
orders rows: before 20000 | after EXPLAIN QUERY PLAN DELETE 20000 | inside BEGIN..DELETE 16413 | after ROLLBACK 20000
SQLite version: 3.45.1
```

**Edge cases:**
- In this run the plan for join 2 was the same before and after `ANALYZE`; the earlier research run (a different schema) saw a bloom filter appear only after `ANALYZE` in a different schema, so do not generalise from either.
- Plan text is not a stable interface: the SQLite documentation says the format may change between versions (this run is SQLite 3.45.1), and other engines' output differs by version and settings. Parse plans only for diagnosis, not in programs.
- `EXPLAIN QUERY PLAN` in SQLite does not execute the statement (the row count stayed 20,000 after explaining a `DELETE`), while `EXPLAIN ANALYZE` in PostgreSQL does execute it (next section).

**Then explain:** (everything about other engines is not executed here, with no vendor numbers)
- PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)`: each plan node shows `cost=start..total`, estimated `rows` and `width` (average row bytes), and with ANALYZE also `actual time=first..last`, actual `rows` and `loops` (the node ran that many times, so multiply per-loop figures). `BUFFERS` adds `shared hit` (pages found in the cache) and `read` (pages fetched from outside it). The first thing to look at is the gap between estimated and actual rows: a large gap means stale or insufficient statistics and usually explains a bad join choice.
- MySQL `EXPLAIN`: per table, `type` (the access method: `const`, `eq_ref`, `ref`, `range`, `index`, `ALL`, from best to worst in general), `key` (index chosen) and `key_len` (how much of a composite index is used), `rows` (estimate), `filtered` (estimated percentage kept after other conditions) and `Extra` (for example `Using index` for covering, `Using filesort`, `Using temporary`, `Using where`). `EXPLAIN FORMAT=JSON` gives the same with cost details and nesting. I read these from the MySQL manual page, not by running MySQL.
- SQL Server graphical plan: operators read right to left; index seek (jumps to matching keys) versus scan (reads the structure), a key lookup (extra trip to the clustered index for columns the nonclustered index lacks), estimated versus actual rows on each operator, and spill warnings when sort or hash work exceeded its memory grant and went to disk.
- Nested loop, hash and merge joins: a nested loop does one probe of the inner side per outer row, so it wins when the outer side is small and the inner side has a good index (plan 1 above). A hash join builds a hash table on the smaller input and probes it with the other, so it wins on large unsorted inputs, uses memory proportional to the build side and can spill. A merge join walks two inputs sorted on the join key, so it wins when both are already sorted (from an index or a prior sort) and the output is large; it uses little memory but needs the order. SQLite implements nested loops only (with automatic indexes and bloom filters as substitutes for the hash idea).
- Bitmap index scans (PostgreSQL) combine several index conditions into a bitmap of pages and then read the table pages in physical order, a middle path between an index scan and a full scan; index-only scans return the answer from the index without table access when the visibility information allows it (the PostgreSQL docs concept; SQLite's equivalent is the `COVERING INDEX` line).
- Why `EXPLAIN ANALYZE` executes the statement: it needs real timings and row counts, so an `INSERT`, `UPDATE` or `DELETE` really happens. Wrap it in a transaction and roll back (`BEGIN; EXPLAIN ANALYZE ...; ROLLBACK;`). The Code block shows the SQLite version of the rollback idea: 20,000 rows, then 16,413 inside the transaction after a `DELETE`, then 20,000 after `ROLLBACK`.
- What SQLite prints that others differ on: `SCAN`/`SEARCH`, `USING INDEX` and `COVERING INDEX`, `AUTOMATIC` indexes, `BLOOM FILTER`, `MATERIALIZE`, `CO-ROUTINE` and `USE TEMP B-TREE`, with no cost or row estimates in the output.

**Follow-ups:**
- When would you force a hash join? (Usually you do not; fix the statistics or indexes first.)
- What does a large estimate gap look like in practice? (An estimate of 10 rows against thousands actual, with a nested loop chosen; not run.)
- How would you read plan 3's `SCALAR SUBQUERY`? (The `AVG` runs once, not once per row; checked only by reading the plan.)

**Common mistakes:**
- Running `EXPLAIN ANALYZE` on a write against production without a rollback.
- Reading only the cost number, not estimated versus actual rows.
- Treating one engine's plan vocabulary as another's.
- Parsing plan text in application code.

### Q34 ⭐ 🔴 Plan caching, parameter sniffing, hints and prepared statements. In SQLite: show that sqlite3 caches prepared statements by SQL text, that a parameterised LIKE ? is re-planned when the bound value changes (the optoverview note), that EXPLAIN QUERY PLAN of an identical statement text after a CREATE INDEX or DROP INDEX in the same connection can show a stale plan (check by running; a changed SQL text or a fresh connection shows the real plan), and use INDEXED BY, NOT INDEXED and the unary plus as the SQLite hints. Then describe, not executed, SQL Server parameter sniffing (a plan compiled for the first parameter value is reused for atypical values; symptoms, OPTION (RECOMPILE), plan guides and the idea of parameter-sensitive plans), PostgreSQL generic versus custom plans for prepared statements, MySQL optimizer hints and index hints, why hints are a last resort, and why string-built SQL both risks injection and defeats plan reuse.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; Partitioning and clustering and parameter-sniffing explainers (Dataford, a Substack post, Medium, SQLServerCentral, SQLShack, Red Gate; search snippets only, not opened); guides, not candidate reports; data engineer rounds at product companies and GCCs
**Say this first (1 line):** In SQLite the plan follows the bound value and the index set, but Python's `sqlite3` statement cache can make an identical `EXPLAIN QUERY PLAN` text show a stale plan after a `DROP INDEX`, and hints (`INDEXED BY`, `NOT INDEXED`, unary plus) override the planner, so they should be a last resort backed by a measurement.

**Schema and sample data:**
```sql
CREATE TABLE t(id INTEGER PRIMARY KEY, cust INTEGER, name TEXT, status TEXT);
-- 50,000 seeded rows; status is 'a' for 98%, 'b' for 1.5% and 'c' for 0.5%; cust is 1 to 500
-- indexes are created and dropped during the run: ix_cust(cust), ix_name(name COLLATE NOCASE), ix_status(status)
```

**SQL answer:** the statements run in the Code block (the hint forms are the `H` template):
```sql
SELECT COUNT(*) FROM t WHERE cust = 7
SELECT COUNT(*) FROM t WHERE name LIKE ?
SELECT COUNT(*) FROM t {hint} WHERE status = 'c' AND cust > 100      -- hint is empty, INDEXED BY ix_cust, or NOT INDEXED
SELECT COUNT(*) FROM t WHERE +status = 'c' AND cust > 100
```

**pandas answer:** the counts are checked against pandas:
```py
exp_c = int(((df.status == "c") & (df.cust > 100)).sum())
exp = int(df["name"].str.lower().str.startswith("alp").sum())
```

**Example:** `cust = 7` matches 88 rows. With no index the plan is `SCAN t` (150,100 VM steps); after `CREATE INDEX` the same text runs as `SEARCH t USING COVERING INDEX ix_cust` (277 steps) with the same count 88. For `LIKE ?` on a NOCASE index, `'alp%'` is a range search (37,466 steps, 12,483 rows, which includes `Alpine...` because LIKE ignores case), `'%pha1'` has no usable prefix and scans the whole index (200,017 steps, 4 rows), and `'alp%'` again goes back to the range search: one statement text, three plans. For the status query the planner chose `ix_status` (1,469 steps), because `status = 'c'` is selective; forcing `ix_cust` (a range on `cust > 100`, most of the table) took 159,624 steps and `NOT INDEXED` 150,720, all with count 208.

**Code:** run with `python3 -I`.
```python
# Q34: plan caching and hints in SQLite (executed); other engines are described in prose only.
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(34)
N = 50_000
words = np.array(["alpha", "beta", "gamma", "delta", "Alpine", "betel", "zeta", "omega"])
df = pd.DataFrame({"id": np.arange(1, N + 1), "cust": rng.integers(1, 501, N),
                   "name": [w + str(i % 997) for w, i in zip(words[rng.integers(0, 8, N)], range(N))],
                   "status": rng.choice(["a", "b", "c"], N, p=[0.98, 0.015, 0.005])})

def connect(**kw):
    con = sqlite3.connect(":memory:", **kw)
    con.execute("CREATE TABLE t(id INTEGER PRIMARY KEY, cust INTEGER, name TEXT, status TEXT)")
    con.executemany("INSERT INTO t VALUES (?,?,?,?)", df.itertuples(index=False, name=None))
    con.commit()
    return con

def steps(con, sql, params=()):
    c = [0]
    def cb(): c[0] += 1; return 0
    con.set_progress_handler(cb, 1); r = con.execute(sql, params).fetchall(); con.set_progress_handler(None, 0)
    return c[0], r

def eqp(con, sql, params=()): return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql, params)]


# 1. same SQL text, index created or dropped in the same connection (separate fresh connections per case)
Q = "SELECT COUNT(*) FROM t WHERE cust = 7"
print("\n1a. CREATE INDEX after the statement text was used")
con = connect()
s_before, r0 = steps(con, Q); p_before = eqp(con, Q)
con.execute("CREATE INDEX ix_cust ON t(cust)")
s_after, r1 = steps(con, Q)
print("   real SELECT, same text: steps before", s_before, "after", s_after, "(count", r1[0][0], "= before", r0[0][0], ")")
print("   EXPLAIN QUERY PLAN before:", p_before)
print("   EXPLAIN QUERY PLAN after CREATE INDEX, identical text:", eqp(con, Q))
print("1b. DROP INDEX after the statement text was used")
con = connect(); con.execute("CREATE INDEX ix_cust ON t(cust)")
print("   EXPLAIN QUERY PLAN with the index:", eqp(con, Q))
con.execute("DROP INDEX ix_cust")
print("   after DROP INDEX, identical text:", eqp(con, Q))
print("   after DROP INDEX, text plus two trailing spaces:", eqp(con, Q + "  "))
n, r = steps(con, Q); print("   the real SELECT with the identical text still runs correctly: steps", n, "count", r[0][0])
fresh = connect(); fresh.execute("CREATE INDEX ix_cust ON t(cust)"); fresh.execute("DROP INDEX ix_cust")
print("   fresh connection after create+drop:", eqp(fresh, Q))
con2 = connect(cached_statements=0); con2.execute("CREATE INDEX ix_cust ON t(cust)"); eqp(con2, Q); con2.execute("DROP INDEX ix_cust")
print("   cached_statements=0, same text after DROP INDEX:", eqp(con2, Q))

# 2. LIKE ? re-planned when the bound value changes
c3 = connect(); c3.execute("CREATE INDEX ix_name ON t(name COLLATE NOCASE)")
QL = "SELECT COUNT(*) FROM t WHERE name LIKE ?"
for v in ("alp%", "%pha1", "alp%"):
    n, r = steps(c3, QL, (v,))
    print(f"\n2. LIKE ? bound to {v!r}: steps {n:,}, count {r[0][0]}, plan {eqp(c3, QL, (v,))}")
exp = int(df["name"].str.lower().str.startswith("alp").sum())
assert steps(c3, QL, ("alp%",))[1][0][0] == exp
print("   same statement text, three bindings: the plan follows the value (checked above; pandas count for 'alp%' =", exp, ")")

# 3. hints
c4 = connect()
c4.execute("CREATE INDEX ix_status ON t(status)"); c4.execute("CREATE INDEX ix_cust ON t(cust)")
H = "SELECT COUNT(*) FROM t {hint} WHERE status = 'c' AND cust > 100"
for tag, hint, cond in (("planner's choice", "", None), ("INDEXED BY ix_cust", "INDEXED BY ix_cust", None),
                        ("NOT INDEXED", "NOT INDEXED", None)):
    q = H.format(hint=hint)
    n, r = steps(c4, q)
    print(f"\n3. {tag}: steps {n:,}, count {r[0][0]}, plan {eqp(c4, q)}")
q = "SELECT COUNT(*) FROM t WHERE +status = 'c' AND cust > 100"
n, r = steps(c4, q); print(f"   unary plus on status: steps {n:,}, count {r[0][0]}, plan {eqp(c4, q)}")
exp_c = int(((df.status == "c") & (df.cust > 100)).sum()); assert r[0][0] == exp_c
for bad in ("SELECT COUNT(*) FROM t INDEXED BY no_such_index WHERE cust = 7",
            "SELECT COUNT(*) FROM t INDEXED BY ix_status WHERE cust = 7"):
    try:
        print("   ", bad, "->", c4.execute(bad).fetchall())
    except sqlite3.Error as e:
        print("   ", bad, "->", type(e).__name__ + ":", e)
print("   all hint variants return the same count as pandas:", exp_c)
```

**Output (my run):**
```text

1a. CREATE INDEX after the statement text was used
   real SELECT, same text: steps before 150100 after 277 (count 88 = before 88 )
   EXPLAIN QUERY PLAN before: ['SCAN t']
   EXPLAIN QUERY PLAN after CREATE INDEX, identical text: ['SEARCH t USING COVERING INDEX ix_cust (cust=?)']
1b. DROP INDEX after the statement text was used
   EXPLAIN QUERY PLAN with the index: ['SEARCH t USING COVERING INDEX ix_cust (cust=?)']
   after DROP INDEX, identical text: ['SEARCH t USING COVERING INDEX ix_cust (cust=?)']
   after DROP INDEX, text plus two trailing spaces: ['SCAN t']
   the real SELECT with the identical text still runs correctly: steps 150100 count 88
   fresh connection after create+drop: ['SCAN t']
   cached_statements=0, same text after DROP INDEX: ['SCAN t']

2. LIKE ? bound to 'alp%': steps 37,466, count 12483, plan ['SEARCH t USING COVERING INDEX ix_name (name>? AND name<?)']

2. LIKE ? bound to '%pha1': steps 200,017, count 4, plan ['SCAN t USING COVERING INDEX ix_name']

2. LIKE ? bound to 'alp%': steps 37,464, count 12483, plan ['SEARCH t USING COVERING INDEX ix_name (name>? AND name<?)']
   same statement text, three bindings: the plan follows the value (checked above; pandas count for 'alp%' = 12483 )

3. planner's choice: steps 1,469, count 208, plan ['SEARCH t USING INDEX ix_status (status=?)']

3. INDEXED BY ix_cust: steps 159,624, count 208, plan ['SEARCH t USING INDEX ix_cust (cust>?)']

3. NOT INDEXED: steps 150,720, count 208, plan ['SCAN t']
   unary plus on status: steps 159,624, count 208, plan ['SEARCH t USING INDEX ix_cust (cust>?)']
    SELECT COUNT(*) FROM t INDEXED BY no_such_index WHERE cust = 7 -> OperationalError: no such index: no_such_index
    SELECT COUNT(*) FROM t INDEXED BY ix_status WHERE cust = 7 -> [(88,)]
   all hint variants return the same count as pandas: 208
```

**Edge cases:**
- Stale plan: after `DROP INDEX`, `EXPLAIN QUERY PLAN` with the identical text still printed `SEARCH ... USING COVERING INDEX ix_cust`, while the same text with two trailing spaces, a fresh connection and a connection with `cached_statements=0` printed `SCAN t`. The real `SELECT` with the identical text still ran correctly (count 88, 150,100 steps, a full scan), so only the displayed plan was stale. In the opposite case (`CREATE INDEX` after the text was used) the identical text showed the new plan. I did not find the cause in the documentation; my guess is that the cached `EXPLAIN` statement is not re-prepared after the index disappears. Treat any plan you print as suspect after DDL on the same connection, and verify with a fresh connection or a changed text.
- `INDEXED BY ix_status ... WHERE cust = 7` did not error: it returned 88 rows (I did not print its plan in this run). `INDEXED BY no_such_index` raised `OperationalError: no such index: no_such_index`. I did not trigger the documented error for an existing index that cannot be used; do not rely on that error to detect a bad hint.
- The unary plus on `+status` disabled `ix_status` for that term, and the planner then picked `ix_cust` (159,624 steps), the same slow plan as `INDEXED BY ix_cust`.
- SQLite prepares a statement once and re-prepares it when the schema changes or when a bound parameter value would change the plan (the optimiser overview documents the `LIKE ?` case, which my run confirms).
- I did not measure whether string-built SQL defeats the statement cache: the trace callback shows expanded text, so it could not tell the two cases apart, and the claim below is the general reasoning, not a measurement.

**Then explain:** (everything below about other engines is not executed here, with no versions or numbers)
- The Python `sqlite3` module keeps a cache of prepared statements keyed by the SQL text (the `cached_statements` argument to `connect`; I set it to 0 above to switch it off), which is why a changed text or a fresh connection recompiles and an identical text can reuse an old compiled statement.
- SQL Server parameter sniffing: when a parameterised query or procedure is first compiled, the optimiser looks at the first parameter value and caches a plan built for it; later calls with very different values (a rare value, then a very common one) reuse a plan that may be wrong for them. Symptoms: the same procedure is fast for some inputs and slow for others, the slow plan appears after a restart or recompile, and the estimated row counts in the cached plan do not match the actuals for the slow call. Mitigations: `OPTION (RECOMPILE)` (compile each time, trading CPU for plan quality), plan guides, query hints, restructuring (for example separate procedures for the skewed cases), and newer parameter-sensitive plan features that keep several plans for one statement.
- PostgreSQL prepared statements: the server can plan a prepared statement for each execution with the actual values (a custom plan) or reuse one generic plan; it compares the cost and, after a few executions, may switch to the generic plan. A skewed parameter can make the generic plan poor.
- MySQL: optimizer hints in comments and index hints (`USE INDEX`, `FORCE INDEX`, `IGNORE INDEX`) to steer a plan.
- Why hints are a last resort: they freeze a decision while data and statistics change, hide the underlying problem (stale statistics, a missing index), and break when an index is renamed or dropped. Prefer fixing statistics, indexes and the query shape; keep a hint only with a comment, a measurement and a plan to revisit it. My SQLite run shows the risk: both hints made the status query about 100 times more VM steps than the planner's choice.
- String-built SQL: concatenating values into the text is open to injection and, because each value yields a different statement text, it prevents reuse of a cached plan or prepared statement (each text is compiled separately); bound parameters fix both, at the cost of the parameter-sniffing question above.

**Follow-ups:**
- How would you see whether SQLite chose a plan using statistics? (`ANALYZE` and `sqlite_stat1`; not run in this answer.)
- What is the safer alternative to `INDEXED BY`? (Fix the index or the predicate so the planner picks it itself.)
- How would you reproduce parameter sniffing without SQL Server? (You cannot exactly; the SQLite `LIKE ?` case is the nearest executable analogue.)

**Common mistakes:**
- Trusting a plan printed on a connection that has just changed the schema.
- Adding hints without measuring (they were far worse here).
- Building SQL by string concatenation.
- Assuming a plan for one parameter value is right for all values.

### Q35 ⭐ 🔴 Locking and isolation at concept level, with what SQLite can demonstrate: in a file-backed SQLite database in the default rollback-journal mode, show that a reader holding an open read transaction blocks a writer's commit ('database is locked', use a short timeout) and that in WAL mode the writer commits while the reader keeps its snapshot; read PRAGMA journal_mode, the wal and shm files and busy_timeout. Explain why long transactions hurt (locks, table bloat or undo growth, replication lag), the cost of CREATE INDEX on a live table (ONLINE and CONCURRENTLY options in other engines, hedged and not executed), MVCC versus lock-based isolation, the read-committed and repeatable-read anomalies (dirty, non-repeatable and phantom reads) in a table, and a deadlock example in words. Note what SQLite does not provide (row-level locking, a server) and keep every non-SQLite claim hedged without versions or numbers.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds
**Say this first (1 line):** In SQLite's default rollback-journal mode a reader holding an open read transaction stops a writer from committing, while in WAL mode the writer commits and the reader keeps its snapshot; other engines use row-level locks and MVCC, which SQLite does not have, and those parts below are described, not executed.

**Schema and sample data:**
```sql
CREATE TABLE acct(id INTEGER PRIMARY KEY, bal INTEGER);
INSERT INTO acct VALUES (1, 100);
-- a file-backed database in a temporary directory, three or more connections with timeout=0.1 (busy_timeout 100 ms)
```

**SQL answer:** the statements in the Code block (the transactions are sent by hand, `isolation_level=None`):
```sql
PRAGMA journal_mode=WAL;      -- or the default 'delete'
PRAGMA busy_timeout;
BEGIN; SELECT bal FROM acct WHERE id = 1;            -- reader, stays open
BEGIN; UPDATE acct SET bal = 150 WHERE id = 1; COMMIT;   -- writer
BEGIN IMMEDIATE;                                    -- second writer
```

**pandas answer:** the final table is read with pandas and compared with the expected frame:
```py
pd.testing.assert_frame_equal(o, pd.DataFrame({"id": [1], "bal": [expected[m]]}), check_dtype=False)
```

**Example:** the account starts at 100. In rollback-journal mode: the reader opens `BEGIN` and reads 100, which holds a shared lock for the whole transaction; the writer's `UPDATE` is accepted into its own transaction, but its `COMMIT` fails after the 100 ms timeout with `database is locked`, the reader still sees 100, and a `t.db-journal` file exists. After the reader commits, the writer retries and commits 150. In WAL mode: the same steps, but the writer's `COMMIT` succeeds, the reader inside its transaction still sees 100, files `t.db-wal` and `t.db-shm` exist, and after the reader commits it sees 150.

**Code:** run with `python3 -I`.
```python
# Q35: locking in a file-backed SQLite database: rollback journal vs WAL (executed); other engines in prose only.
import os, sqlite3, tempfile
import pandas as pd

def open_db(path, timeout=0.1):
    return sqlite3.connect(path, timeout=timeout, isolation_level=None)   # isolation_level=None: we send BEGIN/COMMIT ourselves

def run(mode):
    d = tempfile.mkdtemp(); path = os.path.join(d, "t.db")
    setup = open_db(path)
    setup.execute(f"PRAGMA journal_mode={mode}")
    setup.execute("CREATE TABLE acct(id INTEGER PRIMARY KEY, bal INTEGER)")
    setup.execute("INSERT INTO acct VALUES (1, 100)")
    print(f"\n===== journal_mode = {setup.execute('PRAGMA journal_mode').fetchone()[0]}  (busy_timeout = "
          f"{setup.execute('PRAGMA busy_timeout').fetchone()[0]} ms, from timeout=0.1)")
    reader, writer = open_db(path), open_db(path)
    reader.execute("BEGIN"); n0 = reader.execute("SELECT bal FROM acct WHERE id = 1").fetchone()[0]
    print("reader: BEGIN + SELECT sees bal =", n0, "and keeps the transaction open")
    writer.execute("BEGIN"); writer.execute("UPDATE acct SET bal = 150 WHERE id = 1")
    print("writer: BEGIN + UPDATE succeeded (change is uncommitted)")
    try:
        writer.execute("COMMIT"); print("writer: COMMIT succeeded")
        committed = True
    except sqlite3.OperationalError as e:
        print("writer: COMMIT failed ->", e); committed = False
    print("reader (same transaction) sees bal =", reader.execute("SELECT bal FROM acct WHERE id = 1").fetchone()[0])
    print("files in the directory:", sorted(os.listdir(d)))
    if not committed:
        writer.execute("ROLLBACK")
    reader.execute("COMMIT")
    print("reader after COMMIT sees bal =", reader.execute("SELECT bal FROM acct WHERE id = 1").fetchone()[0])
    if not committed:
        writer.execute("BEGIN"); writer.execute("UPDATE acct SET bal = 150 WHERE id = 1"); writer.execute("COMMIT")
        print("writer retried after the reader finished: committed; bal =", reader.execute("SELECT bal FROM acct WHERE id = 1").fetchone()[0])
    # second writer while the first holds the write lock
    w1, w2 = open_db(path), open_db(path)
    w1.execute("BEGIN IMMEDIATE")
    try:
        w2.execute("BEGIN IMMEDIATE"); print("second writer got the lock")
    except sqlite3.OperationalError as e:
        print("second BEGIN IMMEDIATE while a writer is open ->", e)
    w1.execute("ROLLBACK")
    if mode == "wal":
        # read-then-write on a snapshot that went stale
        r, w = open_db(path), open_db(path)
        r.execute("BEGIN"); r.execute("SELECT bal FROM acct").fetchall()
        w.execute("UPDATE acct SET bal = bal + 1 WHERE id = 1")           # autocommit write
        try:
            r.execute("UPDATE acct SET bal = bal + 10 WHERE id = 1"); print("reader upgraded to a writer fine")
        except sqlite3.OperationalError as e:
            print("reader with an old snapshot tries to write ->", e)
        r.execute("ROLLBACK"); r.close(); w.close()
    out = pd.read_sql("SELECT * FROM acct", setup)
    for c in (setup, reader, writer, w1, w2): c.close()
    return out

res = {m: run(m) for m in ("delete", "wal")}
expected = {"delete": 150, "wal": 151}   # wal run has one extra +1 update from the stale-snapshot demo
for m, o in res.items():
    pd.testing.assert_frame_equal(o, pd.DataFrame({"id": [1], "bal": [expected[m]]}), check_dtype=False)
print("\nfinal tables equal the expected pandas frames:", {m: o["bal"].tolist() for m, o in res.items()})

# autocommit reads see each other's commits (a non-repeatable read at the SQL level); a WAL snapshot does not
d = tempfile.mkdtemp(); p = os.path.join(d, "n.db")
a, b = open_db(p), open_db(p)
a.execute("PRAGMA journal_mode=WAL"); a.execute("CREATE TABLE x(v INTEGER)"); a.execute("INSERT INTO x VALUES (1)")
first = b.execute("SELECT v FROM x").fetchone()[0]; a.execute("UPDATE x SET v = 2")
second = b.execute("SELECT v FROM x").fetchone()[0]
print("\nautocommit reader, two SELECTs with a commit between:", first, "then", second)
b.execute("BEGIN"); f = b.execute("SELECT v FROM x").fetchone()[0]; a.execute("UPDATE x SET v = 3")
s = b.execute("SELECT v FROM x").fetchone()[0]; b.execute("COMMIT")
print("reader inside BEGIN (WAL snapshot), same two SELECTs:", f, "then", s)
a.close(); b.close()
```

**Output (my run):**
```text

===== journal_mode = delete  (busy_timeout = 100 ms, from timeout=0.1)
reader: BEGIN + SELECT sees bal = 100 and keeps the transaction open
writer: BEGIN + UPDATE succeeded (change is uncommitted)
writer: COMMIT failed -> database is locked
reader (same transaction) sees bal = 100
files in the directory: ['t.db', 't.db-journal']
reader after COMMIT sees bal = 100
writer retried after the reader finished: committed; bal = 150
second BEGIN IMMEDIATE while a writer is open -> database is locked

===== journal_mode = wal  (busy_timeout = 100 ms, from timeout=0.1)
reader: BEGIN + SELECT sees bal = 100 and keeps the transaction open
writer: BEGIN + UPDATE succeeded (change is uncommitted)
writer: COMMIT succeeded
reader (same transaction) sees bal = 100
files in the directory: ['t.db', 't.db-shm', 't.db-wal']
reader after COMMIT sees bal = 150
second BEGIN IMMEDIATE while a writer is open -> database is locked
reader with an old snapshot tries to write -> database is locked

final tables equal the expected pandas frames: {'delete': [150], 'wal': [151]}

autocommit reader, two SELECTs with a commit between: 1 then 2
reader inside BEGIN (WAL snapshot), same two SELECTs: 2 then 2
```

In the output, the `final table` line holds 150 for the rollback-journal run and 151 for the WAL run: the WAL run does one more `+1` update in the stale-snapshot demo, so the expected frames differ by design.

**Edge cases:**
- Only one writer at a time in both modes: a second `BEGIN IMMEDIATE` while another writer was open gave `database is locked`. Readers do not block writers in WAL mode, but writers still queue behind each other.
- In WAL mode a reader whose snapshot went stale cannot upgrade to a writer: after another connection committed a change, the reader's `UPDATE` failed with `database is locked` (a snapshot conflict); the reader must roll back and retry on a fresh transaction.
- An uncommitted writer does not block readers: the research run saw a reader succeed during an uncommitted writer transaction in both modes; this run does not repeat that.
- `PRAGMA journal_mode` returns the mode in effect; WAL is persistent in the database file, while `busy_timeout` is per connection (the `timeout` argument sets it). The `-wal` and `-shm` files are the write-ahead log and its shared-memory index; the WAL is merged into the main file at a checkpoint.
- Reading inside versus outside a transaction: an autocommit reader saw 1 and then 2 for two SELECTs with a commit between them, while a reader inside `BEGIN` on a WAL database saw 2 and 2 even though another connection then committed 3. That is the SQLite version of non-repeatable reads (autocommit) versus a stable snapshot (inside a transaction).

**Then explain:** (everything below that is not SQLite is not executed here; no versions or numbers)
- Why long transactions hurt: they hold locks (blocking writers or other lockers), they stop cleanup (in MVCC engines old row versions cannot be removed, causing table bloat or undo-log growth), and they hold back replication or checkpointing (replication lag). Keep transactions short, do not wait for user input inside one, and batch large changes.
- The cost of `CREATE INDEX` on a live table: a plain build blocks writes (and sometimes reads) while it runs. Options exist to reduce that: PostgreSQL has `CREATE INDEX CONCURRENTLY` (slower, extra scans, cannot run inside a transaction block), SQL Server and MySQL have online index options (edition and storage-engine dependent). All described, not executed. SQLite builds the index under the write lock, so no concurrent write can commit.
- MVCC versus lock-based isolation: with MVCC, readers see a snapshot of committed versions and do not block writers (PostgreSQL, InnoDB, and SQLite's WAL snapshots in a limited form); with lock-based isolation, readers take shared locks that conflict with writers' exclusive locks, which is what the rollback-journal run showed at database level.
- Anomalies by isolation level, in general terms (exact behaviour differs by engine, so check the manual):

| Anomaly | Read uncommitted | Read committed | Repeatable read | Serializable |
|---|---|---|---|---|
| Dirty read (see another transaction's uncommitted write) | possible | not possible | not possible | not possible |
| Non-repeatable read (same row read twice gives different values) | possible | possible | not possible | not possible |
| Phantom read (same predicate returns different rows) | possible | possible | possible in the textbook definition; some engines prevent it | not possible |

- A deadlock in words: transaction A updates row 1 and then wants row 2; transaction B updated row 2 and now wants row 1; each waits for the other, so the engine detects the cycle and aborts one with an error that the application must retry. Prevent it by touching rows in a consistent order and keeping transactions short. SQLite avoids the classic form by returning `database is locked` (busy) instead of waiting forever, as the stale-snapshot upgrade showed.
- What SQLite does not provide: row-level locking (locks are at database level; WAL allows one writer plus many readers), a server process, or the isolation-level menu of server databases (I believe SQLite transactions behave as serializable; I did not test isolation levels here).

**Follow-ups:**
- How do you tune the wait? (`busy_timeout`, short transactions, `BEGIN IMMEDIATE` for writers; I used 100 ms only to keep the demo fast.)
- What happens to the WAL file when it grows? (Checkpointing; not run here.)
- How would you detect a long-running transaction on a server database? (The engine's activity view; not executed here.)

**Common mistakes:**
- Leaving a read transaction open in the application "just in case".
- Assuming WAL allows two concurrent writers.
- Reading `database is locked` as corruption instead of contention.
- Starting an online index build without checking its transaction restrictions.
- Treating the isolation-level table as identical across engines.
