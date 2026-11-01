### Q35 ⭐⭐ 🟡 Key dtype mismatch in pandas merge: customers.customer_id is int64 and orders.customer_id was read from CSV as object (strings, some with trailing spaces) or float64 (because of NaN). Explain the ValueError you get for int versus object, the silent wrong result for strings that look alike, float keys with NaN, and fix with astype('Int64'), str.strip and a post-merge unmatched check. Compare with SQL implicit casting (hedged: engine dependent).
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `merge` never casts a key for you: `int64` against `str` or `object` raises `ValueError`, but text against text, or a mixed `object` column, matches silently wrong, and a `float64` key (because of NaN) merges fine while the NaN rows can never match; so clean the key to one dtype (`str.strip`, `to_numeric`, `astype('Int64')`) and always check the unmatched rows after the merge.

**Schema and sample data:** customers has an `int64` key. The orders CSV has a trailing space on one key (`2 `), a blank key, and an unknown customer (7).
```text
order_id,customer_id
10,1
11,2 
12,3
13,
14,3
15,7
```
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders_raw(order_id INTEGER, customer_id TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders_raw VALUES (10,'1'),(11,'2 '),(12,'3'),(13,NULL),(14,'3'),(15,'7');
```

**SQL answer:** SQL has no dtype error to catch you here, so the point is the explicit cast. `SQL_IMPLICIT` is the lazy join and `SQL_FIX` is the safe one (both run in the Code block):
```sql
SELECT o.order_id, c.name FROM orders_raw o LEFT JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id
```
```sql
SELECT o.order_id, CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER) AS customer_id, c.name,
       CASE WHEN c.customer_id IS NULL THEN 'left_only' ELSE 'both' END AS _merge
FROM orders_raw o
LEFT JOIN customers c ON c.customer_id = CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER)
ORDER BY o.order_id
```
`NULLIF(..., '')` matters: in SQLite `CAST('' AS INTEGER)` and `CAST('x' AS INTEGER)` both give 0 (see the output), so without it a blank or junk key silently becomes key 0.

**pandas answer:** read, strip, convert, merge with `indicator=True`, then look at what did not match (same lines as in the Code block):
```py
orders["customer_id"] = pd.to_numeric(orders["customer_id"].str.strip(), errors="coerce").astype("Int64")
p = orders.merge(customers, on="customer_id", how="left", indicator=True)
unmatched = p[p["_merge"] != "both"]
```

**Example:** walk the six order rows through the fixed join. 10 has key 1, so Asha. 11 has `'2 '`, which strips to 2, so Ben. 12 has 3, so Chitra. 13 is blank, so NaN, so no match. 14 is 3 again, so Chitra. 15 has key 7, and there is no customer 7, so no match. Unmatched orders are therefore 13 and 15. Without the strip, text against text also loses order 11, giving 11, 13 and 15, and nothing warns you.

**Code:** run with `python3 -I`; the SQL and pandas fixed results are compared sorted by `order_id` with `assert_frame_equal`.
```python
# Q35: merge key dtype mismatch (int64 vs str/object/float64), silent drops, fix, SQLite implicit casting
import io
import sqlite3
import warnings
import pandas as pd

CSV = "order_id,customer_id\n10,1\n11,2 \n12,3\n13,\n14,3\n15,7\n"   # '2 ' has a trailing space, 13 has no key, 15 is unknown
customers = pd.DataFrame({"customer_id": [1, 2, 3, 4], "name": ["Asha", "Ben", "Chitra", "Dev"]})
print("customers key dtype:", customers["customer_id"].dtype)

# 1) every column read as text (what an object/str column looks like): int64 vs text raises
orders_txt = pd.read_csv(io.StringIO(CSV), dtype=str)
print("orders key dtype (dtype=str):", orders_txt["customer_id"].dtype)
try:
    customers.merge(orders_txt, on="customer_id")
except ValueError as e:
    print("int64 vs str ->", type(e).__name__ + ":", e)
orders_obj = pd.read_csv(io.StringIO(CSV), dtype=object)
try:
    customers.merge(orders_obj, on="customer_id")
except ValueError as e:
    print("int64 vs object ->", type(e).__name__ + ":", e)

# 1b) text on BOTH sides: no error at all, the '2 ' row just fails to match
cust_txt = customers.assign(customer_id=customers["customer_id"].astype(str))
t = orders_txt.merge(cust_txt, on="customer_id", how="left", indicator=True)
print("\ntext vs text, no strip: unmatched order_ids:", t.loc[t["_merge"] == "left_only", "order_id"].tolist())

# 2) silent wrong result: an object column holding a mix of ints and strings does NOT raise
mixed = pd.DataFrame({"order_id": [10, 11, 12], "customer_id": pd.Series([1, "2", 3], dtype=object)})
m = mixed.merge(customers, on="customer_id", how="left", indicator=True)
print("\nmixed object key (1, '2', 3), orders LEFT JOIN customers:")
print(m[["order_id", "customer_id", "name", "_merge"]].to_string(index=False))

# 3) float64 key because of the blank (NaN): matches ints, no error, but NaN row can never match
orders_default = pd.read_csv(io.StringIO(CSV.replace("2 ", "2")))
print("\ndefault read_csv key dtype:", orders_default["customer_id"].dtype)
print(orders_default.merge(customers, on="customer_id", how="left", indicator=True)
      [["order_id", "customer_id", "name", "_merge"]].to_string(index=False))

# 4) the fix: strip, convert to numbers (errors -> NaN), nullable Int64, then merge and check unmatched
orders = orders_txt.copy()
orders["order_id"] = orders["order_id"].astype("int64")
orders["customer_id"] = pd.to_numeric(orders["customer_id"].str.strip(), errors="coerce").astype("Int64")
print("\nafter fix, key dtype:", orders["customer_id"].dtype)
p = orders.merge(customers, on="customer_id", how="left", indicator=True)
p = p[["order_id", "customer_id", "name", "_merge"]].sort_values("order_id").reset_index(drop=True)
print(p.to_string())
unmatched = p[p["_merge"] != "both"]
print("unmatched orders:", unmatched["order_id"].tolist())
assert unmatched["order_id"].tolist() == [13, 15]       # blank key and unknown customer 7

# 5) the same in SQL (SQLite): orders loaded as TEXT, as a CSV import would give
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders_raw(order_id INTEGER, customer_id TEXT);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders_raw VALUES (10,'1'),(11,'2 '),(12,'3'),(13,NULL),(14,'3'),(15,'7');
""")
SQL_IMPLICIT = """
SELECT o.order_id, c.name FROM orders_raw o LEFT JOIN customers c ON c.customer_id = o.customer_id
ORDER BY o.order_id
"""
SQL_FIX = """
SELECT o.order_id, CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER) AS customer_id, c.name,
       CASE WHEN c.customer_id IS NULL THEN 'left_only' ELSE 'both' END AS _merge
FROM orders_raw o
LEFT JOIN customers c ON c.customer_id = CAST(NULLIF(TRIM(o.customer_id), '') AS INTEGER)
ORDER BY o.order_id
"""
print("\nSQLite implicit cast (TEXT vs INTEGER column, no TRIM):", con.execute(SQL_IMPLICIT).fetchall())
print("SQLite literal compare 1 = '1':", con.execute("SELECT 1 = '1'").fetchone()[0],
      "| '2 ' as number:", con.execute("SELECT CAST('2 ' AS INTEGER)").fetchone()[0],
      "| CAST('x' AS INTEGER):", con.execute("SELECT CAST('x' AS INTEGER)").fetchone()[0],
      "| CAST('' AS INTEGER):", con.execute("SELECT CAST('' AS INTEGER)").fetchone()[0])
s = pd.read_sql_query(SQL_FIX, con)
s["customer_id"] = s["customer_id"].astype("Int64")
s["_merge"] = pd.Categorical(s["_merge"], categories=["left_only", "right_only", "both"])  # same categories as indicator=True
print(s.to_string())
pd.testing.assert_frame_equal(s[["order_id", "customer_id", "name", "_merge"]], p, check_dtype=False)
print("SQL fix == pandas fix (sorted by order_id)")

# 6) a bad text value: pandas coerce gives NaN like NULLIF; SQLite CAST silently gives 0
print("\nto_numeric coerce on ['1',' 2','x']:",
      pd.to_numeric(pd.Series(["1", " 2", "x"]).str.strip(), errors="coerce").tolist())
try:
    pd.Series(["1", "x"]).astype("Int64")
except (ValueError, TypeError) as e:
    print("astype('Int64') on 'x' ->", type(e).__name__ + ":", e)
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    customers.merge(pd.DataFrame({"customer_id": [1.0, 2.5]}), on="customer_id")
print("int64 vs float64 with a non-integer float:", [str(x.message)[:60] for x in w])
try:
    pd.Series([1.5]).astype("Int64")
except (ValueError, TypeError) as e:
    print("astype('Int64') on 1.5 ->", type(e).__name__ + ":", e)
print("astype('Int64') on ['1', ' 2'] without strip:", pd.Series(["1", " 2"]).astype("Int64").tolist(),
      "| to_numeric without strip:", pd.to_numeric(pd.Series(["1", " 2"])).tolist())
# NaN keys on BOTH sides: pandas matches NaN with NaN (SQL never matches NULL = NULL)
left_nan = pd.DataFrame({"customer_id": [1.0, None], "name": ["Asha", "Unknown"]})
right_nan = pd.DataFrame({"customer_id": [None, 3.0], "order_id": [13, 12]})
both = left_nan.merge(right_nan, on="customer_id", how="inner")
print("NaN key on both sides, inner merge rows:", both[["name", "order_id"]].values.tolist())
sql_nan = sqlite3.connect(":memory:").execute(
    "SELECT COUNT(*) FROM (SELECT NULL AS k) a JOIN (SELECT NULL AS k) b ON a.k = b.k").fetchone()[0]
print("SQL NULL = NULL join rows:", sql_nan)
con.close()
```

**Output (my run):**
```text
customers key dtype: int64
orders key dtype (dtype=str): str
int64 vs str -> ValueError: You are trying to merge on int64 and str columns for key 'customer_id'. If you wish to proceed you should use pd.concat
int64 vs object -> ValueError: You are trying to merge on int64 and object columns for key 'customer_id'. If you wish to proceed you should use pd.concat

text vs text, no strip: unmatched order_ids: ['11', '13', '15']

mixed object key (1, '2', 3), orders LEFT JOIN customers:
 order_id customer_id   name    _merge
       10           1   Asha      both
       11           2    NaN left_only
       12           3 Chitra      both

default read_csv key dtype: float64
 order_id  customer_id   name    _merge
       10          1.0   Asha      both
       11          2.0    Ben      both
       12          3.0 Chitra      both
       13          NaN    NaN left_only
       14          3.0 Chitra      both
       15          7.0    NaN left_only

after fix, key dtype: Int64
   order_id  customer_id    name     _merge
0        10            1    Asha       both
1        11            2     Ben       both
2        12            3  Chitra       both
3        13         <NA>     NaN  left_only
4        14            3  Chitra       both
5        15            7     NaN  left_only
unmatched orders: [13, 15]

SQLite implicit cast (TEXT vs INTEGER column, no TRIM): [(10, 'Asha'), (11, 'Ben'), (12, 'Chitra'), (13, None), (14, 'Chitra'), (15, None)]
SQLite literal compare 1 = '1': 0 | '2 ' as number: 2 | CAST('x' AS INTEGER): 0 | CAST('' AS INTEGER): 0
   order_id  customer_id    name     _merge
0        10            1    Asha       both
1        11            2     Ben       both
2        12            3  Chitra       both
3        13         <NA>     NaN  left_only
4        14            3  Chitra       both
5        15            7     NaN  left_only
SQL fix == pandas fix (sorted by order_id)

to_numeric coerce on ['1',' 2','x']: [1.0, 2.0, nan]
astype('Int64') on 'x' -> ValueError: invalid literal for int() with base 10: 'x'
int64 vs float64 with a non-integer float: ['You are merging on int and float columns where the float val']
astype('Int64') on 1.5 -> TypeError: cannot safely cast non-equivalent object to int64
astype('Int64') on ['1', ' 2'] without strip: [1, 2] | to_numeric without strip: [1, 2]
NaN key on both sides, inner merge rows: [['Unknown', 13]]
SQL NULL = NULL join rows: 0
```

**Edge cases:**
- **int64 against str or object:** `ValueError: You are trying to merge on int64 and str columns ...` (the message says `object` when the column really is object dtype). On pandas 3.0.5 a text column read from CSV with `dtype=str` shows as `str`; both raised in my run.
- **Silent wrong results, no error:** text against text with a stray space (`'2 '` does not equal `'2'`), and an `object` column holding both ints and strings (the string `'2'` did not match the int 2 and the row fell out of the match, with no error).
- **float64 key because of NaN:** int64 against float64 merges without error and `1.0` matches `1`. The NaN row simply finds no partner. If a float key holds a non-integer value (2.5), pandas only emits a `UserWarning` (seen in my run). And `astype('Int64')` on a column containing 1.5 raised `TypeError`, which is the safe behaviour.
- **Leading and trailing spaces and the numeric cast:** in my run `to_numeric` and `astype('Int64')` both accepted `' 2'` without strip (Python's `int()` tolerates spaces). So the strip is essential for text keys that stay text (names, codes, ids with letters), and a good habit for numeric ones, but do not claim the cast fails without it.
- **Leading zeros:** `'01'` and `'1'` are different text keys but the same number. Decide which meaning you want before choosing text or integer.
- **NaN keys on both sides do match in pandas:** with NaN in both frames, an inner merge joined the NaN row to the NaN row (`Unknown` with order 13 in my run), while the SQL join `NULL = NULL` returned 0 rows. In this question's fixed merge only orders has a missing key, so that row is just `left_only`, but if the customer table also had a NaN key you would get false matches; drop or flag missing keys before merging.

**Then explain:**
- **Why pandas raises for int against str:** it refuses to guess a cast, because the guess could hide a data problem. `object` columns are the dangerous case: they can hold anything, so a mismatch may not be caught.
- **The fix order:** strip, then convert, with `errors="coerce"` so bad values become NaN rather than crash, then `Int64` (capital I) so the key keeps integers and still allows missing values. Plain `int64` cannot hold NaN.
- **The check that matters:** `indicator=True` and look at `left_only`, or compare the row count and the number of matched keys. A merge that silently matches fewer rows than expected is the real risk.
- **SQL implicit casting (ran on SQLite 3.45.1):** joining a TEXT column to an INTEGER column did match (`'2 '` matched 2 and Ben appeared), because SQLite applies numeric affinity to the text side. A bare literal comparison `1 = '1'` gave 0 in the same engine, so the rule depends on column affinity. This is engine dependent and I only ran SQLite.
- **Other engines, not executed here:** PostgreSQL normally errors on `integer = text` for columns (`operator does not exist`), MySQL converts strings to numbers silently (and that conversion can stop an index being used), SQL Server converts by data type precedence and fails with a conversion error on a bad value like `'x'`. Check the manual of your engine.

**Follow-ups:**
- *How do you stop this at load time?* Pass `dtype={"customer_id": "Int64"}` or convert explicitly right after `read_csv`, and assert `df["customer_id"].notna().all()` where blanks are not allowed.
- *Should the key be int or str?* If ids are codes (leading zeros, letters), keep them as stripped text on both sides; if they are numbers, use `Int64`.
- *How do you find which values break the cast?* `bad = s[pd.to_numeric(s.str.strip(), errors="coerce").isna() & s.notna()]`.

**Common mistakes:**
- Casting with `astype(int)` on a column with NaN and getting an error, then dropping rows to make it pass.
- Trusting a merge that did not raise: no error does not mean all rows matched.
- Using `COALESCE(key, 0)` or `CAST('' AS INTEGER)` and creating a fake customer 0.
- Fixing the dtype on one frame only, so the other side still holds text.

### Q36 ⭐ 🟡 Join on the nearest earlier timestamp: trades(trade_id, ticker, trade_time, qty) and quotes(ticker, quote_time, bid). Attach to each trade the latest quote at or before the trade for the same ticker. Show pandas merge_asof (both sorted by time, by='ticker', direction, tolerance, allow_exact_matches), note SQLite has no ASOF JOIN (some engines do, hedged) and write the portable SQL with a correlated MAX(quote_time) subquery.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `pd.merge_asof` is the "latest quote at or before the trade" join (backward direction by default, both frames sorted by time, `by="ticker"`), and the portable SQL is a LEFT JOIN with a correlated `MAX(quote_time)` subquery in the ON clause; SQLite 3.45 has no `ASOF JOIN`.

**Schema and sample data:**
```sql
CREATE TABLE trades(trade_id INTEGER PRIMARY KEY, ticker TEXT, trade_time TEXT, qty INTEGER);
CREATE TABLE quotes(ticker TEXT, quote_time TEXT, bid REAL);
INSERT INTO trades VALUES
 (1,'A','2026-01-05 09:00:05',100),
 (2,'A','2026-01-05 09:00:10', 50),
 (3,'B','2026-01-05 09:00:07', 20),
 (4,'A','2026-01-05 09:00:01', 10),
 (5,'B','2026-01-05 09:01:30', 30);
INSERT INTO quotes VALUES
 ('A','2026-01-05 09:00:02',10.0),
 ('A','2026-01-05 09:00:10',10.5),
 ('A','2026-01-05 09:00:12',11.0),
 ('B','2026-01-05 09:00:03',20.0),
 ('B','2026-01-05 09:00:08',21.0);
```

**SQL answer:** `SQL_MAIN` (the three variants `SQL_MAIN`, `SQL_TOL` for a 30 second tolerance and `SQL_STRICT` for strictly earlier are all in the Code block; `SQL_STRICT` is `SQL_MAIN` with `<=` changed to `<`):
```sql
SELECT t.trade_id, t.ticker, t.trade_time, t.qty, q.quote_time, q.bid
FROM trades t
LEFT JOIN quotes q
  ON q.ticker = t.ticker
 AND q.quote_time = (SELECT MAX(q2.quote_time) FROM quotes q2
                     WHERE q2.ticker = t.ticker AND q2.quote_time <= t.trade_time)
ORDER BY t.trade_id
```
The subquery finds, per trade, the latest quote time for the same ticker that is not after the trade. The outer join then fetches that quote row. LEFT JOIN keeps trades that have no earlier quote (they get NULL).

Not executed: DuckDB, Snowflake and ClickHouse, to my knowledge, have a native `ASOF JOIN` (syntax differs by engine), which does this in one clause. SQLite 3.45 rejected it in my run (`near "ASOF": syntax error`).

**pandas answer:** (same text as in the Code block)
```py
out = pd.merge_asof(trades.sort_values("trade_time"), quotes.sort_values("quote_time"),
                    left_on="trade_time", right_on="quote_time", by="ticker", **kw)
```
Here `**kw` is empty for the plain case, `tolerance=pd.Timedelta("30s")` for the tolerance case, `allow_exact_matches=False` for strictly earlier, and `direction="forward"` or `"nearest"` for the other directions. The `asof` helper in the Code block then restores the order by `trade_id`.

**Example:** quotes for A at 09:00:02 (10.0), 09:00:10 (10.5), 09:00:12 (11.0); for B at 09:00:03 (20.0) and 09:00:08 (21.0).
- Trade 1 (A, 09:00:05): latest A quote at or before is 09:00:02, so bid 10.0.
- Trade 2 (A, 09:00:10): there is a quote at exactly 09:00:10, so bid 10.5. With `allow_exact_matches=False` it would take the 09:00:02 quote, bid 10.0.
- Trade 3 (B, 09:00:07): B quote at 09:00:03, so 20.0 (the 09:00:08 quote is in the future).
- Trade 4 (A, 09:00:01): no quote before it, so NULL.
- Trade 5 (B, 09:01:30): latest quote is 09:00:08 (82 seconds old), so 21.0, or NULL with a 30 second tolerance.

**Code:** run with `python3 -I`; each of the three SQL variants is compared with its `merge_asof` call after sorting by `trade_id`.
```python
# Q36: attach the latest quote at or before each trade: SQL correlated MAX vs pandas merge_asof
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE trades(trade_id INTEGER PRIMARY KEY, ticker TEXT, trade_time TEXT, qty INTEGER);
CREATE TABLE quotes(ticker TEXT, quote_time TEXT, bid REAL);
INSERT INTO trades VALUES
 (1,'A','2026-01-05 09:00:05',100),
 (2,'A','2026-01-05 09:00:10', 50),
 (3,'B','2026-01-05 09:00:07', 20),
 (4,'A','2026-01-05 09:00:01', 10),
 (5,'B','2026-01-05 09:01:30', 30);
INSERT INTO quotes VALUES
 ('A','2026-01-05 09:00:02',10.0),
 ('A','2026-01-05 09:00:10',10.5),
 ('A','2026-01-05 09:00:12',11.0),
 ('B','2026-01-05 09:00:03',20.0),
 ('B','2026-01-05 09:00:08',21.0);
"""
SQL_MAIN = """
SELECT t.trade_id, t.ticker, t.trade_time, t.qty, q.quote_time, q.bid
FROM trades t
LEFT JOIN quotes q
  ON q.ticker = t.ticker
 AND q.quote_time = (SELECT MAX(q2.quote_time) FROM quotes q2
                     WHERE q2.ticker = t.ticker AND q2.quote_time <= t.trade_time)
ORDER BY t.trade_id
"""
# tolerance of 30 seconds: the quote must also be no older than 30 s
SQL_TOL = """
SELECT t.trade_id, t.ticker, t.trade_time, t.qty, q.quote_time, q.bid
FROM trades t
LEFT JOIN quotes q
  ON q.ticker = t.ticker
 AND q.quote_time >= datetime(t.trade_time, '-30 seconds')
 AND q.quote_time = (SELECT MAX(q2.quote_time) FROM quotes q2
                     WHERE q2.ticker = t.ticker AND q2.quote_time <= t.trade_time)
ORDER BY t.trade_id
"""
# strictly earlier (allow_exact_matches=False)
SQL_STRICT = SQL_MAIN.replace("<= t.trade_time", "< t.trade_time")

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
trades = pd.read_sql_query("SELECT * FROM trades", con, parse_dates=["trade_time"])
quotes = pd.read_sql_query("SELECT * FROM quotes", con, parse_dates=["quote_time"])

def sql_df(q):
    d = pd.read_sql_query(q, con, parse_dates=["trade_time", "quote_time"])
    return d.sort_values("trade_id").reset_index(drop=True)

def asof(**kw):
    out = pd.merge_asof(trades.sort_values("trade_time"), quotes.sort_values("quote_time"),
                        left_on="trade_time", right_on="quote_time", by="ticker", **kw)
    return out[["trade_id", "ticker", "trade_time", "qty", "quote_time", "bid"]].sort_values("trade_id").reset_index(drop=True)

p_main = asof()                                           # direction='backward', exact matches allowed
p_tol = asof(tolerance=pd.Timedelta("30s"))
p_strict = asof(allow_exact_matches=False)
for name, s, p in [("main", SQL_MAIN, p_main), ("tolerance 30s", SQL_TOL, p_tol), ("strictly earlier", SQL_STRICT, p_strict)]:
    d = sql_df(s)
    pd.testing.assert_frame_equal(d, p, check_dtype=False)
    print(f"--- {name}: SQL == merge_asof (sorted by trade_id)")
    print(d[["trade_id", "ticker", "trade_time", "quote_time", "bid"]].to_string(index=False))

# SQLite has no ASOF JOIN
try:
    con.execute("SELECT * FROM trades t ASOF JOIN quotes q ON q.ticker = t.ticker AND q.quote_time <= t.trade_time")
except sqlite3.Error as e:
    print("\nASOF JOIN in SQLite ->", type(e).__name__ + ":", e)

# direction='nearest' and 'forward' exist only in pandas; the SQL needs another subquery
print("\ndirection='forward', bids:", asof(direction="forward")["bid"].tolist())
print("direction='nearest', bids:", asof(direction="nearest")["bid"].tolist())

# merge_asof refuses unsorted input
try:
    pd.merge_asof(trades.sort_values("trade_id", ascending=False), quotes.sort_values("quote_time"),
                  left_on="trade_time", right_on="quote_time", by="ticker")
except ValueError as e:
    print("\nunsorted left ->", type(e).__name__ + ":", e)

# two quotes with the same timestamp: SQL returns two rows for the trade, merge_asof exactly one
con.execute("INSERT INTO quotes VALUES ('A','2026-01-05 09:00:12',11.2)")
con.execute("INSERT INTO trades VALUES (6,'A','2026-01-05 09:00:20',5)")
d = pd.read_sql_query(SQL_MAIN, con)
print("\nwith a duplicate quote timestamp, SQL rows for trade 6:", d[d["trade_id"] == 6]["bid"].tolist())
t2 = pd.read_sql_query("SELECT * FROM trades", con, parse_dates=["trade_time"])
q2 = pd.read_sql_query("SELECT * FROM quotes", con, parse_dates=["quote_time"])
a = pd.merge_asof(t2.sort_values("trade_time"), q2.sort_values("quote_time"),
                  left_on="trade_time", right_on="quote_time", by="ticker")
print("merge_asof rows for trade 6:", a[a["trade_id"] == 6]["bid"].tolist())
con.close()
```

**Output (my run):**
```text
--- main: SQL == merge_asof (sorted by trade_id)
 trade_id ticker          trade_time          quote_time  bid
        1      A 2026-01-05 09:00:05 2026-01-05 09:00:02 10.0
        2      A 2026-01-05 09:00:10 2026-01-05 09:00:10 10.5
        3      B 2026-01-05 09:00:07 2026-01-05 09:00:03 20.0
        4      A 2026-01-05 09:00:01                 NaT  NaN
        5      B 2026-01-05 09:01:30 2026-01-05 09:00:08 21.0
--- tolerance 30s: SQL == merge_asof (sorted by trade_id)
 trade_id ticker          trade_time          quote_time  bid
        1      A 2026-01-05 09:00:05 2026-01-05 09:00:02 10.0
        2      A 2026-01-05 09:00:10 2026-01-05 09:00:10 10.5
        3      B 2026-01-05 09:00:07 2026-01-05 09:00:03 20.0
        4      A 2026-01-05 09:00:01                 NaT  NaN
        5      B 2026-01-05 09:01:30                 NaT  NaN
--- strictly earlier: SQL == merge_asof (sorted by trade_id)
 trade_id ticker          trade_time          quote_time  bid
        1      A 2026-01-05 09:00:05 2026-01-05 09:00:02 10.0
        2      A 2026-01-05 09:00:10 2026-01-05 09:00:02 10.0
        3      B 2026-01-05 09:00:07 2026-01-05 09:00:03 20.0
        4      A 2026-01-05 09:00:01                 NaT  NaN
        5      B 2026-01-05 09:01:30 2026-01-05 09:00:08 21.0

ASOF JOIN in SQLite -> OperationalError: near "ASOF": syntax error

direction='forward', bids: [10.5, 10.5, 21.0, 10.0, nan]
direction='nearest', bids: [10.0, 10.5, 21.0, 10.0, 21.0]

unsorted left -> ValueError: left keys must be sorted

with a duplicate quote timestamp, SQL rows for trade 6: [11.0, 11.2]
merge_asof rows for trade 6: [11.2]
```

**Edge cases:**
- **Unsorted input:** `merge_asof` raised `ValueError: left keys must be sorted` in my run. Sort both frames on the time key (globally, not per ticker; `by` handles the ticker).
- **Duplicate quote timestamps:** with two quotes for A at 09:00:12 (11.0 and 11.2) the SQL returned two rows for the trade at 09:00:20 (`[11.0, 11.2]`), but `merge_asof` returned one (`[11.2]`, the later row). This is an honest difference: SQL needs a tie-break (a quote id or sequence number) to pick one row, `merge_asof` took the last of the tied rows (11.2).
- **No earlier quote:** NULL in SQL, NaN and NaT in pandas.
- **Tolerance:** in pandas it applies to the chosen quote, and a stale quote gives NaN; in SQL I put the age test in the ON clause, so the trade row is kept with NULLs (do not move it to WHERE, which would drop the trade).
- **Direction:** `forward` and `nearest` have no one-line SQL form; you would need a `MIN(quote_time) ... >=` subquery or a comparison of two subqueries.
- **Time zones and text timestamps:** my SQL compares ISO 8601 text (`YYYY-MM-DD HH:MM:SS`), which sorts correctly as text. Mixed formats or time zones would break that, and in pandas make both columns the same tz-aware or tz-naive dtype.

**Then explain:**
- **Why an equality join does not work:** quotes and trades almost never share a timestamp, so you need "the nearest one before".
- **The SQL idea:** a correlated subquery returns the right quote time, then an equality join on it. A window-function version also exists (Parts 4 and 5), not used here.
- **Cost:** the correlated subquery is fast only with an index on `(ticker, quote_time)`; `merge_asof` is a sorted merge scan and is typically much faster on large frames (concept; I did not benchmark).
- **`by`:** matches the ticker exactly, then finds the nearest time within it.
- **`allow_exact_matches=False`:** turns `<=` into `<`, which is what you want if a quote at the same instant may have been caused by the trade.

**Follow-ups:**
- *What if quotes arrive after the trade but you want the next one?* `direction="forward"`, which in SQL is `MIN(quote_time)` with `>=`.
- *What if the quotes table is huge?* Index `(ticker, quote_time)` for the SQL version, or pre-filter the day.
- *How would you handle ties in quote_time?* Add a sequence column and pick by `MAX(seq)`; in pandas sort by the time then the sequence before `merge_asof`.

**Common mistakes:**
- Forgetting to sort, or sorting by ticker then time (the key `on` must be sorted globally).
- Putting the tolerance condition in WHERE, which drops the unmatched trades.
- Using `BETWEEN` or `<=` on the join without a `MAX`, which returns every older quote for every trade (a fan-out).
- Merging on `ticker` first with a normal merge and then filtering (a huge intermediate result).

### Q37 ⭐ 🟡 Market-basket pairs with a self join: order_items(order_id, product_id). Find the ten most common pairs of products bought in the same order, each pair once. Join the table to itself on order_id with a.product_id < b.product_id, group by the pair, and count. Explain row growth with large baskets, duplicate lines of the same product, and the pandas version (merge on order_id and filter, then value_counts).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Join the table to itself on `order_id` with `a.product_id < b.product_id` so each pair appears once, `GROUP BY` the pair and `COUNT(*)` orders, but dedupe the lines first, or an order that has the same product on two lines counts a pair twice.

**Schema and sample data:**
```sql
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'C'),
 (4,'B'),(4,'C'),(4,'A'),
 (5,'A'),(5,'B'),(5,'B'),
 (6,'D');
```

**SQL answer:** `SQL_MAIN` in the Code block (derived tables, no CTE, because CTEs are Part 3):
```sql
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS n_orders
FROM (SELECT DISTINCT order_id, product_id FROM order_items) a
JOIN (SELECT DISTINCT order_id, product_id FROM order_items) b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY n_orders DESC, p1, p2
LIMIT 10
```
`SQL_NAIVE` in the Code block is the same query on `order_items` directly (no `DISTINCT`), kept to show the inflation.

**pandas answer:** (same text as in the Code block)
```py
basket = items.drop_duplicates()
pairs = basket.merge(basket, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs["product_id_1"] < pairs["product_id_2"]]
counts = pairs[["product_id_1", "product_id_2"]].value_counts()      # a Series indexed by the pair
```
After that the Code block renames the columns and sorts by count descending then the two ids, so ties come out in a fixed order, then takes `head(10)`.

**Example:** six orders. Order 1 has A, B, C, so pairs AB, AC, BC. Order 2 has A, B, so AB. Order 3 has A, C, so AC. Order 4 has B, C, A, so AB, AC, BC. Order 5 has A, B, B (B twice), so AB after deduplication. Order 6 has only D, so no pair. Totals: AB in orders 1, 2, 4 and 5 is 4; AC in 1, 3, 4 is 3; BC in 1 and 4 is 2. Without the dedupe, order 5 produces AB twice (A with each B line), giving 5, which is wrong.

**Code:** run with `python3 -I`; the SQL result and the pandas result are compared in the order `n_orders` descending, then `p1`, then `p2`.
```python
# Q37: market-basket pairs with a self join: dedupe lines, a < b, GROUP BY pair, top N
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE order_items(order_id INTEGER, product_id TEXT);
INSERT INTO order_items VALUES
 (1,'A'),(1,'B'),(1,'C'),
 (2,'A'),(2,'B'),
 (3,'A'),(3,'C'),
 (4,'B'),(4,'C'),(4,'A'),
 (5,'A'),(5,'B'),(5,'B'),
 (6,'D');
"""
SQL_MAIN = """
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS n_orders
FROM (SELECT DISTINCT order_id, product_id FROM order_items) a
JOIN (SELECT DISTINCT order_id, product_id FROM order_items) b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY n_orders DESC, p1, p2
LIMIT 10
"""
SQL_NAIVE = """
SELECT a.product_id AS p1, b.product_id AS p2, COUNT(*) AS n_orders
FROM order_items a
JOIN order_items b ON a.order_id = b.order_id AND a.product_id < b.product_id
GROUP BY a.product_id, b.product_id
ORDER BY n_orders DESC, p1, p2
LIMIT 10
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL (deduplicated baskets):")
print(sql_df.to_string(index=False))
print("\nSQL naive (duplicate line not removed):")
naive = pd.read_sql_query(SQL_NAIVE, con)
print(naive.to_string(index=False))

# pandas: dedupe lines, self-merge on order_id, keep p1 < p2, count pairs
items = pd.read_sql_query("SELECT * FROM order_items", con)
basket = items.drop_duplicates()
pairs = basket.merge(basket, on="order_id", suffixes=("_1", "_2"))
pairs = pairs[pairs["product_id_1"] < pairs["product_id_2"]]
counts = pairs[["product_id_1", "product_id_2"]].value_counts()      # a Series indexed by the pair
p_df = (counts.rename("n_orders").reset_index()
        .rename(columns={"product_id_1": "p1", "product_id_2": "p2"})
        .sort_values(["n_orders", "p1", "p2"], ascending=[False, True, True])
        .head(10).reset_index(drop=True))
print("\npandas (value_counts after the filtered self-merge):")
print(p_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, p_df, check_dtype=False)
print("SQL == pandas (compared in the order n_orders desc, p1, p2)")

# row growth: a basket of n distinct products produces n(n-1)/2 pair rows
for n in (3, 10, 100):
    con.execute("DELETE FROM order_items WHERE order_id = 99")
    con.executemany("INSERT INTO order_items VALUES (99, ?)", [(f"P{i:03d}",) for i in range(n)])
    rows = con.execute("""SELECT COUNT(*) FROM order_items a JOIN order_items b
                          ON a.order_id = b.order_id AND a.product_id < b.product_id
                          WHERE a.order_id = 99""").fetchone()[0]
    print(f"basket of {n:>3} products -> {rows} pair rows (n(n-1)/2 = {n*(n-1)//2})")
con.close()
```

**Output (my run):**
```text
SQL (deduplicated baskets):
p1 p2  n_orders
 A  B         4
 A  C         3
 B  C         2

SQL naive (duplicate line not removed):
p1 p2  n_orders
 A  B         5
 A  C         3
 B  C         2

pandas (value_counts after the filtered self-merge):
p1 p2  n_orders
 A  B         4
 A  C         3
 B  C         2
SQL == pandas (compared in the order n_orders desc, p1, p2)
basket of   3 products -> 3 pair rows (n(n-1)/2 = 3)
basket of  10 products -> 45 pair rows (n(n-1)/2 = 45)
basket of 100 products -> 4950 pair rows (n(n-1)/2 = 4950)
```

**Edge cases:**
- **Only three pairs exist in my toy data, so "top ten" returns three rows.** `LIMIT 10` is an upper bound, not a promise of ten.
- **Duplicate lines:** the naive version gave AB = 5 instead of 4. The fix is `SELECT DISTINCT order_id, product_id` on both sides (or a unique constraint on `(order_id, product_id)`).
- **Ties at the cut-off:** `LIMIT 10` cuts arbitrarily among equal counts unless the `ORDER BY` has a tie-break, which is why the query sorts by `p1, p2` after the count.
- **Single-item orders (D):** they produce no pair rows, which is correct.
- **`<` versus `<>`:** `<>` would give both (A,B) and (B,A), doubling every count; `<` also removes the (A,A) self pair.

**Then explain:**
- **Row growth:** an order with n distinct products creates n(n-1)/2 pair rows (3, 45 and 4950 rows for baskets of 3, 10 and 100 products in my run). One very large order (a bulk or test order) can dominate the join. Cap basket size, or filter out baskets above a limit, before the self join.
- **Why filter products first for scale:** keep only products with some minimum frequency before self-joining, since a pair cannot be common if one of its items is rare (this is the idea behind support thresholds; I describe it, I did not run it).
- **Count meaning:** `COUNT(*)` after the dedupe is the number of orders containing both products, which is what "bought together" means. It is not the units sold.
- **pandas:** the self-merge makes the same row blow-up in memory; `value_counts` on two columns counts each pair, and ties come out in no guaranteed order, so I sort explicitly before `head`.

**Follow-ups:**
- *How would you add lift or confidence?* Divide the pair count by the product counts (each from `COUNT(DISTINCT order_id)` on one product); that is a second aggregation joined back on.
- *Triples?* A three-way self join with `a < b < c`; growth is cubic, so filter first.
- *Can you avoid the self join?* Not easily in pure SQL; some engines allow array aggregation then unnesting, which is outside this part.

**Common mistakes:**
- Using `<>`, which doubles every pair.
- Not deduping duplicate lines, inflating counts.
- No tie-break in `ORDER BY ... LIMIT`.
- Running the self join on the full line table with huge baskets and wondering why it crawls.

### Q38 ⭐ 🟡 Students and courses (many-to-many): students(student_id, name), courses(course_id, title) and enrollments(student_id, course_id). Find students enrolled in no course, students enrolled in every course (relational division via GROUP BY HAVING COUNT(DISTINCT course_id) = total courses), and pairs of students sharing a course. Explain the bridge table and why duplicate enrollment rows need DISTINCT. Give pandas.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** The bridge table `enrollments` holds one row per student and course; "no course" is an anti-join, "every course" is `GROUP BY student HAVING COUNT(DISTINCT course_id) = (SELECT COUNT(*) FROM courses)`, and "pairs sharing a course" is a self join on `course_id` with `a.student_id < b.student_id`, always on de-duplicated enrolment rows.

**Schema and sample data:**
```sql
CREATE TABLE students(student_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE courses(course_id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE enrollments(student_id INTEGER, course_id INTEGER);   -- no primary key, so duplicates are possible
INSERT INTO students VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO courses VALUES (10,'SQL'),(20,'Stats'),(30,'ML');
INSERT INTO enrollments VALUES
 (1,10),(1,20),(1,30),
 (2,10),(2,10),(2,20),
 (3,10),(3,20),(3,30),
 (5,30);
```
Ben has a duplicated row (course 10 twice); Dev has no enrolment.

**SQL answer:** the queries are `SQL_NONE`, `SQL_ALL`, `SQL_ALL_WRONG` (the trap) and `SQL_PAIRS` in the Code block.
```sql
SELECT s.name FROM students s
WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.student_id)
ORDER BY s.student_id
```
```sql
SELECT s.name
FROM students s
JOIN enrollments e ON e.student_id = s.student_id
JOIN courses c ON c.course_id = e.course_id
GROUP BY s.student_id, s.name
HAVING COUNT(DISTINCT e.course_id) = (SELECT COUNT(*) FROM courses)
ORDER BY s.student_id
```
```sql
SELECT a.student_id AS s1, b.student_id AS s2, COUNT(*) AS shared_courses
FROM (SELECT DISTINCT student_id, course_id FROM enrollments) a
JOIN (SELECT DISTINCT student_id, course_id FROM enrollments) b ON a.course_id = b.course_id AND a.student_id < b.student_id
GROUP BY a.student_id, b.student_id
ORDER BY s1, s2
```

**pandas answer:** (same text as in the Code block)
```py
none_p = students.loc[~students["student_id"].isin(enr["student_id"]), "name"].tolist()
valid = enr.drop_duplicates().merge(courses[["course_id"]], on="course_id")           # drop dups, keep real courses
n_courses = valid.groupby("student_id")["course_id"].nunique()
all_ids = n_courses[n_courses == len(courses)].index
d = enr.drop_duplicates()
pp = d.merge(d, on="course_id", suffixes=("_1", "_2"))
pp = pp[pp["student_id_1"] < pp["student_id_2"]]
```

**Example:** Courses are 10, 20, 30. Asha: 10, 20, 30, so all three. Ben: 10, 10, 20, so two distinct (three rows). Chitra: 10, 20, 30, so all three. Dev: nothing. Esha: 30 only.
- No enrolment: Dev.
- Every course: Asha and Chitra. Ben's three rows would pass `COUNT(*) = 3`, which is wrong; `COUNT(DISTINCT course_id)` gives 2 and rejects him.
- Pairs: course 10 has Asha, Ben, Chitra, giving (1,2), (1,3), (2,3); course 20 gives the same three; course 30 has Asha, Chitra, Esha, giving (1,3), (1,5), (3,5). Shared courses per pair: (1,2) 2, (1,3) 3, (2,3) 2, (1,5) 1, (3,5) 1.

**Code:** run with `python3 -I`; pairs are compared sorted by `s1, s2`, and the two name lists are compared in `student_id` order.
```python
# Q38: many-to-many: no enrolment, enrolled in every course (division), pairs sharing a course
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE students(student_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE courses(course_id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE enrollments(student_id INTEGER, course_id INTEGER);   -- no primary key, so duplicates are possible
INSERT INTO students VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO courses VALUES (10,'SQL'),(20,'Stats'),(30,'ML');
INSERT INTO enrollments VALUES
 (1,10),(1,20),(1,30),
 (2,10),(2,10),(2,20),
 (3,10),(3,20),(3,30),
 (5,30);
"""
SQL_NONE = """
SELECT s.name FROM students s
WHERE NOT EXISTS (SELECT 1 FROM enrollments e WHERE e.student_id = s.student_id)
ORDER BY s.student_id
"""
SQL_ALL = """
SELECT s.name
FROM students s
JOIN enrollments e ON e.student_id = s.student_id
JOIN courses c ON c.course_id = e.course_id
GROUP BY s.student_id, s.name
HAVING COUNT(DISTINCT e.course_id) = (SELECT COUNT(*) FROM courses)
ORDER BY s.student_id
"""
SQL_ALL_WRONG = """
SELECT s.name FROM students s JOIN enrollments e ON e.student_id = s.student_id
GROUP BY s.student_id, s.name
HAVING COUNT(e.course_id) = (SELECT COUNT(*) FROM courses)
ORDER BY s.student_id
"""
SQL_PAIRS = """
SELECT a.student_id AS s1, b.student_id AS s2, COUNT(*) AS shared_courses
FROM (SELECT DISTINCT student_id, course_id FROM enrollments) a
JOIN (SELECT DISTINCT student_id, course_id FROM enrollments) b ON a.course_id = b.course_id AND a.student_id < b.student_id
GROUP BY a.student_id, b.student_id
ORDER BY s1, s2
"""
SQL_PAIRS_NAIVE = SQL_PAIRS.replace("(SELECT DISTINCT student_id, course_id FROM enrollments)",
                                    "enrollments")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
col = lambda q: [r[0] for r in con.execute(q).fetchall()]
print("no enrolment:", col(SQL_NONE))
print("every course:", col(SQL_ALL))
print("every course, COUNT(e.course_id) instead of DISTINCT (wrong):", col(SQL_ALL_WRONG))
pairs = pd.read_sql_query(SQL_PAIRS, con)
print("\npairs sharing a course (deduplicated):")
print(pairs.to_string(index=False))
print("\npairs with duplicate rows not removed (shared_courses inflated):")
print(pd.read_sql_query(SQL_PAIRS_NAIVE, con).to_string(index=False))

# pandas
students = pd.read_sql_query("SELECT * FROM students", con)
courses = pd.read_sql_query("SELECT * FROM courses", con)
enr = pd.read_sql_query("SELECT * FROM enrollments", con)
none_p = students.loc[~students["student_id"].isin(enr["student_id"]), "name"].tolist()
valid = enr.drop_duplicates().merge(courses[["course_id"]], on="course_id")           # drop dups, keep real courses
n_courses = valid.groupby("student_id")["course_id"].nunique()
all_ids = n_courses[n_courses == len(courses)].index
all_p = students.loc[students["student_id"].isin(all_ids)].sort_values("student_id")["name"].tolist()
d = enr.drop_duplicates()
pp = d.merge(d, on="course_id", suffixes=("_1", "_2"))
pp = pp[pp["student_id_1"] < pp["student_id_2"]]
pairs_p = (pp.groupby(["student_id_1", "student_id_2"], as_index=False).size()
           .rename(columns={"student_id_1": "s1", "student_id_2": "s2", "size": "shared_courses"})
           .sort_values(["s1", "s2"]).reset_index(drop=True))
assert none_p == col(SQL_NONE) == ["Dev"]
assert all_p == col(SQL_ALL) == ["Asha", "Chitra"]
pd.testing.assert_frame_equal(pairs, pairs_p, check_dtype=False)
print("\npandas: no enrolment", none_p, "| every course", all_p)
print("asserts passed (pairs compared sorted by s1, s2)")

# edge: no courses at all
con.execute("DELETE FROM courses")
print("with an empty courses table, 'every course' returns:", col(SQL_ALL))
con.close()
```

**Output (my run):**
```text
no enrolment: ['Dev']
every course: ['Asha', 'Chitra']
every course, COUNT(e.course_id) instead of DISTINCT (wrong): ['Asha', 'Ben', 'Chitra']

pairs sharing a course (deduplicated):
 s1  s2  shared_courses
  1   2               2
  1   3               3
  1   5               1
  2   3               2
  3   5               1

pairs with duplicate rows not removed (shared_courses inflated):
 s1  s2  shared_courses
  1   2               3
  1   3               3
  1   5               1
  2   3               3
  3   5               1

pandas: no enrolment ['Dev'] | every course ['Asha', 'Chitra']
asserts passed (pairs compared sorted by s1, s2)
with an empty courses table, 'every course' returns: []
```

**Edge cases:**
- **Duplicate enrolments:** `COUNT(e.course_id)` returned Ben as enrolled in every course (output line "COUNT(e.course_id) instead of DISTINCT (wrong)"). The pairs query without the `DISTINCT` inflated (1,2), (2,3) from 2 to 3 shared courses.
- **Enrolments for a course that does not exist:** the division query joins to `courses`, so an orphan `course_id` cannot make a student look complete. In pandas the same is the merge with `courses`.
- **No courses at all:** mathematically everyone "took every course" (an empty set), but the `GROUP BY` form returned nobody (empty output in my run), because it only sees students who have enrolments. Decide what you want if the courses table can be empty.
- **A student with no rows in `enrollments`:** not in the division result unless you start from `students`; they are in the "no course" result.
- **Pairs sharing no course:** do not appear; to list all pairs you would need a cross join and an anti-join.

**Then explain:**
- **Bridge table:** many-to-many is stored as a third table with one row per (student, course), and ideally a primary key on the pair, which would also stop duplicate rows at the source.
- **Relational division by counting:** "has every course" equals "has as many distinct courses as exist", valid only if each counted row is a real course, so join to `courses` first and count distinct.
- **Other forms (not run):** a double `NOT EXISTS` expresses division without counting and is robust to duplicates; I did not run it here.
- **Pair self join:** `a.student_id < b.student_id` removes mirror pairs and self pairs; the join on `course_id` gives one row per shared course, so `COUNT(*)` is the number of shared courses.

**Follow-ups:**
- *Students enrolled in exactly the same courses as another student?* Compare the sets; that is harder, and in SQL you would compare `COUNT(*)` of shared courses to each student's total.
- *Students with at least two courses?* `HAVING COUNT(DISTINCT course_id) >= 2`.
- *How do you stop duplicates?* `PRIMARY KEY (student_id, course_id)` on the bridge table.

**Common mistakes:**
- `COUNT(*)` or `COUNT(course_id)` without `DISTINCT` in the division.
- Comparing with a hard-coded course count instead of `(SELECT COUNT(*) FROM courses)`.
- Using an INNER JOIN from `students` for the "no course" case (it cannot show the missing rows).
- Using `<>` for the pair join and returning each pair twice.

### Q39 ⭐ 🟡 Outer join key columns: a(id, x) and b(key, y) joined FULL OUTER ON a.id = b.key. Explain why neither id nor key alone is the full key set, how COALESCE(a.id, b.key) fixes the output, what USING does in engines that support it, and how pandas outer merge with left_on/right_on returns both columns while on= returns one. Include the effect on a downstream GROUP BY.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** In a FULL OUTER JOIN on `a.id = b.key`, `a.id` is NULL for right-only rows and `b.key` is NULL for left-only rows, so neither column is the full key set; select `COALESCE(a.id, b.key)` (or use `USING` where it exists), and group by that, never by one side.

**Schema and sample data:**
```sql
CREATE TABLE a(id INTEGER, x TEXT);
CREATE TABLE b(key INTEGER, y INTEGER);
CREATE TABLE b2(id INTEGER, y INTEGER);          -- same data as b, key column renamed to id for USING
INSERT INTO a VALUES (1,'a1'),(2,'a2'),(3,'a3');
INSERT INTO b VALUES (2,20),(3,30),(4,40),(5,50);
INSERT INTO b2 SELECT key, y FROM b;
```

**SQL answer:** the queries are `SQL_RAW`, `SQL_MAIN`, `SQL_USING`, `SQL_GROUP_WRONG` and `SQL_GROUP_RIGHT` in the Code block.
```sql
SELECT COALESCE(a.id, b.key) AS id, a.x, b.y
FROM a FULL OUTER JOIN b ON a.id = b.key
ORDER BY id
```
```sql
SELECT COALESCE(a.id, b.key) AS grp, COUNT(*) AS n_rows, SUM(b.y) AS sum_y
FROM a FULL OUTER JOIN b ON a.id = b.key GROUP BY COALESCE(a.id, b.key) ORDER BY grp
```
SQLite 3.45 ran `FULL OUTER JOIN` and `USING`. `USING` needs a column with the same name on both sides, which is why `b2` repeats `b` with the key renamed to `id`. In engines that support USING (not executed: PostgreSQL, MySQL for the inner and left/right forms), the `USING` column is merged into one output column.

**pandas answer:** (same text as in the Code block)
```py
m_lr = a.merge(b, left_on="id", right_on="key", how="outer")
m_on = a.merge(b.rename(columns={"key": "id"}), on="id", how="outer")
m_lr["id"] = m_lr["id"].fillna(m_lr["key"])
```

**Example:** `a` has ids 1, 2, 3; `b` has keys 2, 3, 4, 5. The matched pairs are 2 and 3. Left-only is 1 (so `b.key` is NULL). Right-only are 4 and 5 (so `a.id` is NULL). Reading only `a.id` you would see 1, 2, 3, NULL, NULL and lose 4 and 5. `COALESCE(a.id, b.key)` gives 1, 2, 3, 4, 5. Grouping by `a.id` collapses 4 and 5 into one NULL group (2 rows, sum of y = 40 + 50 = 90); grouping by the coalesced key gives five groups.

**Code:** run with `python3 -I`; the coalesced SQL result is compared with both pandas forms (sorted by `id`), and the grouped totals are compared too.
```python
# Q39: FULL OUTER JOIN key columns: a.id and b.key are each NULL on one side; COALESCE, USING, pandas left_on/right_on vs on
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE a(id INTEGER, x TEXT);
CREATE TABLE b(key INTEGER, y INTEGER);
CREATE TABLE b2(id INTEGER, y INTEGER);          -- same data as b, key column renamed to id for USING
INSERT INTO a VALUES (1,'a1'),(2,'a2'),(3,'a3');
INSERT INTO b VALUES (2,20),(3,30),(4,40),(5,50);
INSERT INTO b2 SELECT key, y FROM b;
"""
SQL_RAW = "SELECT a.id, b.key, a.x, b.y FROM a FULL OUTER JOIN b ON a.id = b.key"
SQL_MAIN = """
SELECT COALESCE(a.id, b.key) AS id, a.x, b.y
FROM a FULL OUTER JOIN b ON a.id = b.key
ORDER BY id
"""
SQL_USING = "SELECT id, x, y FROM a FULL OUTER JOIN b2 USING (id) ORDER BY id"
SQL_GROUP_WRONG = """
SELECT a.id AS grp, COUNT(*) AS n_rows, SUM(b.y) AS sum_y
FROM a FULL OUTER JOIN b ON a.id = b.key GROUP BY a.id ORDER BY a.id
"""
SQL_GROUP_RIGHT = """
SELECT COALESCE(a.id, b.key) AS grp, COUNT(*) AS n_rows, SUM(b.y) AS sum_y
FROM a FULL OUTER JOIN b ON a.id = b.key GROUP BY COALESCE(a.id, b.key) ORDER BY grp
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
show = lambda q: print(pd.read_sql_query(q, con).to_string(index=False))
print("raw FULL JOIN, both key columns:"); show(SQL_RAW)
print("\nCOALESCE(a.id, b.key):"); show(SQL_MAIN)
print("\nUSING (id) on b2, SELECT id:"); show(SQL_USING)
print("\nGROUP BY a.id (wrong, right-only keys collapse into one NULL group):"); show(SQL_GROUP_WRONG)
print("\nGROUP BY COALESCE(a.id, b.key):"); show(SQL_GROUP_RIGHT)

# pandas
a = pd.read_sql_query("SELECT * FROM a", con)
b = pd.read_sql_query("SELECT * FROM b", con)
m_lr = a.merge(b, left_on="id", right_on="key", how="outer")
print("\npandas outer, left_on='id' right_on='key' (both columns kept):")
print(m_lr.to_string(index=False)); print("id and key dtypes:", m_lr[["id", "key"]].dtypes.astype(str).to_dict())
m_on = a.merge(b.rename(columns={"key": "id"}), on="id", how="outer")
print("\npandas outer, on='id' after renaming b.key to id (one coalesced column):")
print(m_on.to_string(index=False)); print("id dtype:", str(m_on["id"].dtype))

# the coalesced frame from left_on/right_on, and the group-by
m_lr["id"] = m_lr["id"].fillna(m_lr["key"])
p_main = m_lr[["id", "x", "y"]].sort_values("id").reset_index(drop=True)
sql_main = pd.read_sql_query(SQL_MAIN, con)
pd.testing.assert_frame_equal(sql_main, p_main.astype({"id": "int64", "y": "float64"}), check_dtype=False)
pd.testing.assert_frame_equal(sql_main, m_on[["id", "x", "y"]].sort_values("id").reset_index(drop=True), check_dtype=False)
lr = a.merge(b, left_on="id", right_on="key", how="outer")           # id still has NaN for right-only rows
agg = dict(n_rows=("y", "size"), sum_y=("y", lambda s: s.sum(min_count=1)))
print("\npandas groupby('id') on the uncoalesced column, default dropna=True (right-only rows vanish):")
print(lr.groupby("id").agg(**agg).reset_index().to_string(index=False))
print("pandas groupby('id', dropna=False) (the SQL-like NULL group):")
print(lr.groupby("id", dropna=False).agg(**agg).reset_index().to_string(index=False))
g_right = m_on.groupby("id").agg(**agg).reset_index()
print("\npandas groupby on the coalesced id:"); print(g_right.to_string(index=False))
sql_g = pd.read_sql_query(SQL_GROUP_RIGHT, con)
pd.testing.assert_frame_equal(sql_g.rename(columns={"grp": "id"}), g_right, check_dtype=False)
print("asserts passed: SQL == pandas (sorted by id)")
con.close()
```

**Output (my run):**
```text
raw FULL JOIN, both key columns:
 id  key   x    y
1.0  NaN  a1  NaN
2.0  2.0  a2 20.0
3.0  3.0  a3 30.0
NaN  4.0 NaN 40.0
NaN  5.0 NaN 50.0

COALESCE(a.id, b.key):
 id   x    y
  1  a1  NaN
  2  a2 20.0
  3  a3 30.0
  4 NaN 40.0
  5 NaN 50.0

USING (id) on b2, SELECT id:
 id   x    y
  1  a1  NaN
  2  a2 20.0
  3  a3 30.0
  4 NaN 40.0
  5 NaN 50.0

GROUP BY a.id (wrong, right-only keys collapse into one NULL group):
 grp  n_rows  sum_y
 NaN       2   90.0
 1.0       1    NaN
 2.0       1   20.0
 3.0       1   30.0

GROUP BY COALESCE(a.id, b.key):
 grp  n_rows  sum_y
   1       1    NaN
   2       1   20.0
   3       1   30.0
   4       1   40.0
   5       1   50.0

pandas outer, left_on='id' right_on='key' (both columns kept):
 id   x  key    y
1.0  a1  NaN  NaN
2.0  a2  2.0 20.0
3.0  a3  3.0 30.0
NaN NaN  4.0 40.0
NaN NaN  5.0 50.0
id and key dtypes: {'id': 'float64', 'key': 'float64'}

pandas outer, on='id' after renaming b.key to id (one coalesced column):
 id   x    y
  1  a1  NaN
  2  a2 20.0
  3  a3 30.0
  4 NaN 40.0
  5 NaN 50.0
id dtype: int64

pandas groupby('id') on the uncoalesced column, default dropna=True (right-only rows vanish):
 id  n_rows  sum_y
1.0       1    NaN
2.0       1   20.0
3.0       1   30.0
pandas groupby('id', dropna=False) (the SQL-like NULL group):
 id  n_rows  sum_y
1.0       1    NaN
2.0       1   20.0
3.0       1   30.0
NaN       2   90.0

pandas groupby on the coalesced id:
 id  n_rows  sum_y
  1       1    NaN
  2       1   20.0
  3       1   30.0
  4       1   40.0
  5       1   50.0
asserts passed: SQL == pandas (sorted by id)
```

**Edge cases:**
- **Both sides NULL:** if a row in `a` has `id = NULL`, `COALESCE` returns the other side's key (also NULL if it is unmatched), and NULL keys never match each other in a SQL join (see Q6).
- **Sums over missing:** SQL `SUM(b.y)` for key 1 is NULL (no `b` rows). pandas `sum()` of an all-NaN group gives 0.0, which my first run showed as a mismatch against SQL; the Code block uses `sum(min_count=1)` to get NaN like SQL.
- **pandas groupby drops NaN keys:** `groupby("id")` on the uncoalesced column dropped the NaN group (keys 4 and 5 vanished from the totals); `dropna=False` kept them as one NaN group, like SQL.
- **dtypes:** with `left_on`/`right_on` the key columns became `float64` (NaN needs float); with `on=` the key stayed `int64`.
- **Which column is "right"?** `a.id` is the left key and `b.key` the right key; with `on=` pandas fills both into one column.

**Then explain:**
- **Why:** a full join keeps unmatched rows from both sides; for each unmatched row the other side's columns are NULL, including its key column.
- **SQL fixes:** `COALESCE(a.id, b.key)` in SELECT, GROUP BY and any later join; or `USING (id)` where supported.
- **pandas:** `on="id"` (same name on both sides) returns one key column, filled from whichever side has it; `left_on`/`right_on` returns both, like SQL's raw output.
- **Downstream GROUP BY:** group by the coalesced expression. In my run, `GROUP BY a.id` gave 4 groups (one NULL group of 2 rows summing 90) where the coalesced version gave 5.
- **Dialect (not executed):** in SQLite `SELECT l.id, r.id` with USING in a FULL JOIN kept the sides separate (see Q43 for the run), while `SELECT id` was coalesced; other engines differ in details, so check the manual.

**Follow-ups:**
- *What does `SELECT *` return for USING versus ON?* One key column versus both (verified for SQLite in Q43).
- *Can you ORDER BY the key?* Order by the coalesced expression (or its alias), otherwise NULL keys sort together.
- *What if the key names differ in pandas but you want one column?* Rename before the merge, or merge with `left_on`/`right_on` and then `fillna` as in the Code block.

**Common mistakes:**
- Selecting `a.id` and reporting the right-only rows with a NULL id.
- `GROUP BY a.id` after a full join.
- `WHERE a.id IS NULL` to find "only in b", when that is correct but then using `a.id` as the display key.
- Expecting `merge(left_on=..., right_on=...)` to merge the key columns for you.

### Q40 ⭐ 🟡 Row count changed after adding a join (1,000 rows became 1,400). Describe a systematic diagnosis: define the grain you expect, compare COUNT(*) with COUNT(DISTINCT key) before and after, find the duplicated join keys with GROUP BY ... HAVING, test the join in isolation, and add guards (unique constraints, row-count assertions, validate= in pandas). Include a small worked example with a dimension table that has two current rows per key.
**Asked at:** data-modelling write-ups on fan and chasm traps (Coginiti, Sisense, Holistics; snippets), not candidate reports; analyst and data scientist rounds and BI debugging
**Say this first (1 line):** If 1,000 rows became 1,400, the join key is not unique on the side you added: define the expected grain, compare `COUNT(*)` with `COUNT(DISTINCT key)` before and after, find the duplicated keys with `GROUP BY ... HAVING COUNT(*) > 1`, test the join in isolation, then fix the data and add a guard.

**Schema and sample data:** 1,000 orders, 10 per customer for customers 1 to 100 (amount 10 each, so revenue is 10,000). `customer_dim` is a type 2 style table with an `is_current` flag. Customers 1 to 40 wrongly have two current rows, customers 41 to 60 have one old row and one current row (normal), and customers 61 to 100 have one current row. The Code block builds the data with a loop; the tables are:
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE customer_dim(customer_id INTEGER, segment TEXT, valid_from TEXT, is_current INTEGER);
```

**SQL answer:** the diagnosis queries run in the Code block, in order; the join that breaks and the fix are:
```sql
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o JOIN customer_dim d ON d.customer_id = o.customer_id AND d.is_current = 1
```
```sql
SELECT customer_id, COUNT(*) AS n FROM customer_dim WHERE is_current = 1
GROUP BY customer_id HAVING COUNT(*) > 1 ORDER BY customer_id
```
```sql
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o
JOIN customer_dim d
  ON d.customer_id = o.customer_id AND d.is_current = 1
 AND d.valid_from = (SELECT MAX(d2.valid_from) FROM customer_dim d2
                     WHERE d2.customer_id = d.customer_id AND d2.is_current = 1)
ORDER BY o.order_id
```
The fix picks the latest `valid_from` among the current rows, which is a business rule I chose for the example (the right rule depends on your data); it is better to repair the dimension at the source.

**pandas answer:** (same text as in the Code block)
```py
cur = cdim[cdim["is_current"] == 1]
orders.merge(cur, on="customer_id", validate="many_to_one")
latest = cur.sort_values("valid_from").drop_duplicates("customer_id", keep="last")
```

**Example:** the arithmetic is checkable by hand. 40 customers have two current rows, so each of their 10 orders matches twice: 40 customers x 10 orders x 1 extra row = 400 extra rows, 1,000 + 400 = 1,400. `SUM(amount)` goes from 10,000 to 14,000. Customers 41 to 60 do not add rows because their old row has `is_current = 0` and is filtered out in the join.

**Code:** run with `python3 -I`; the fixed SQL and fixed pandas results are compared sorted by `order_id`, and the row count is asserted to be 1,000.
```python
# Q40: 1,000 rows became 1,400 after a join: diagnose with COUNT(*) vs COUNT(DISTINCT), duplicated keys, isolation, guards
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE customer_dim(customer_id INTEGER, segment TEXT, valid_from TEXT, is_current INTEGER);
""")
# 1,000 orders, 10 per customer for customers 1..100
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, (i - 1) % 100 + 1, 10) for i in range(1, 1001)])
dim = []
for c in range(1, 101):
    if c <= 40:                                        # the bug: two 'current' rows for customers 1..40
        dim += [(c, "gold", "2025-01-01", 1), (c, "silver", "2025-06-01", 1)]
    elif c <= 60:                                      # normal history: one old row (not current) + one current
        dim += [(c, "bronze", "2024-01-01", 0), (c, "gold", "2025-01-01", 1)]
    else:
        dim.append((c, "gold", "2025-01-01", 1))
con.executemany("INSERT INTO customer_dim VALUES (?,?,?,?)", dim)

one = lambda q: con.execute(q).fetchone()
print("1. grain of orders: COUNT(*), COUNT(DISTINCT order_id) =", one("SELECT COUNT(*), COUNT(DISTINCT order_id) FROM orders"))

SQL_BAD = """
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o JOIN customer_dim d ON d.customer_id = o.customer_id AND d.is_current = 1
"""
print("2. after the join: COUNT(*), COUNT(DISTINCT order_id), SUM(amount) =",
      one(f"SELECT COUNT(*), COUNT(DISTINCT order_id), SUM(amount) FROM ({SQL_BAD})"), "(true SUM was 10000)")

SQL_DUPKEYS = """
SELECT customer_id, COUNT(*) AS n FROM customer_dim WHERE is_current = 1
GROUP BY customer_id HAVING COUNT(*) > 1 ORDER BY customer_id
"""
dups = con.execute(SQL_DUPKEYS).fetchall()
print("3. duplicated current keys:", len(dups), "keys, first three:", dups[:3])
print("   expected extra rows = SUM(n - 1) x orders per key =", sum(n - 1 for _, n in dups), "x 10 =",
      sum(n - 1 for _, n in dups) * 10)
print("4. isolate one key:", con.execute("SELECT * FROM customer_dim WHERE customer_id = 1").fetchall())

# fix in the query: pick the latest current row per key
SQL_FIX = """
SELECT o.order_id, o.customer_id, o.amount, d.segment
FROM orders o
JOIN customer_dim d
  ON d.customer_id = o.customer_id AND d.is_current = 1
 AND d.valid_from = (SELECT MAX(d2.valid_from) FROM customer_dim d2
                     WHERE d2.customer_id = d.customer_id AND d2.is_current = 1)
ORDER BY o.order_id
"""
fixed = pd.read_sql_query(SQL_FIX, con)
print("5. fixed join rows:", len(fixed), "| SUM(amount):", fixed["amount"].sum())

# pandas: same diagnosis and fix
orders = pd.read_sql_query("SELECT * FROM orders", con)
cdim = pd.read_sql_query("SELECT * FROM customer_dim", con)
cur = cdim[cdim["is_current"] == 1]
try:
    orders.merge(cur, on="customer_id", validate="many_to_one")
except pd.errors.MergeError as e:
    print("\npandas validate='many_to_one' ->", type(e).__name__ + ":", e)
print("pandas duplicated current keys:", int(cur["customer_id"].duplicated().sum()))
bad = orders.merge(cur, on="customer_id")
print("pandas unvalidated merge rows:", len(bad), "| sum amount:", bad["amount"].sum())
latest = cur.sort_values("valid_from").drop_duplicates("customer_id", keep="last")
p_fixed = (orders.merge(latest[["customer_id", "segment"]], on="customer_id", how="inner", validate="many_to_one")
           .sort_values("order_id").reset_index(drop=True))
pd.testing.assert_frame_equal(fixed[["order_id", "customer_id", "amount", "segment"]], p_fixed, check_dtype=False)
assert len(p_fixed) == len(orders) == 1000
print("asserts passed: SQL fix == pandas fix (sorted by order_id), row count 1000 == orders")

# guard at the source: a partial unique index makes the duplicate load fail
con.execute("DELETE FROM customer_dim WHERE customer_id <= 40 AND valid_from = '2025-01-01'")
con.execute("CREATE UNIQUE INDEX one_current ON customer_dim(customer_id) WHERE is_current = 1")
try:
    con.execute("INSERT INTO customer_dim VALUES (1, 'gold', '2026-01-01', 1)")
except sqlite3.IntegrityError as e:
    print("\nunique partial index ->", type(e).__name__ + ":", e)
con.close()
```

**Output (my run):**
```text
1. grain of orders: COUNT(*), COUNT(DISTINCT order_id) = (1000, 1000)
2. after the join: COUNT(*), COUNT(DISTINCT order_id), SUM(amount) = (1400, 1000, 14000) (true SUM was 10000)
3. duplicated current keys: 40 keys, first three: [(1, 2), (2, 2), (3, 2)]
   expected extra rows = SUM(n - 1) x orders per key = 40 x 10 = 400
4. isolate one key: [(1, 'gold', '2025-01-01', 1), (1, 'silver', '2025-06-01', 1)]
5. fixed join rows: 1000 | SUM(amount): 10000

pandas validate='many_to_one' -> MergeError: Merge keys are not unique in right dataset; not a many-to-one merge

Duplicates in right:
  customer_id
           1
           2
           3
           4
           5 ...
pandas duplicated current keys: 40
pandas unvalidated merge rows: 1400 | sum amount: 14000
asserts passed: SQL fix == pandas fix (sorted by order_id), row count 1000 == orders

unique partial index -> IntegrityError: UNIQUE constraint failed: customer_dim.customer_id
```

**Edge cases:**
- **Row count unchanged but totals wrong:** a join can also drop one row and duplicate another, so also compare `SUM` and `COUNT(DISTINCT order_id)`, not only `COUNT(*)`.
- **A LEFT JOIN with no match:** keeps the row once, so shrinking row counts point to an INNER JOIN or a filter in WHERE.
- **NULL keys:** orders with a NULL key match nothing and are not duplicated.
- **The unique index guard:** my partial unique index on `customer_id WHERE is_current = 1` made the duplicate insert fail with `IntegrityError`. Partial indexes exist in SQLite and PostgreSQL; MySQL and others differ (hedged, not executed).
- **pandas `MergeError` message:** it lists the duplicated key values (it printed customers 1 to 5 and `...`).

**Then explain:**
- **Step 1, grain:** say it out loud: one row per order. Check the base: 1,000 rows, 1,000 distinct `order_id`.
- **Step 2, after the join:** 1,400 rows but still 1,000 distinct `order_id` means fan-out (some orders repeated).
- **Step 3, find it:** group the joined table's key by `HAVING COUNT(*) > 1` (40 keys with 2 rows).
- **Step 4, isolate:** look at one key (customer 1 has two current rows), and run the join alone without other joins.
- **Step 5, guards:** a unique or partial unique index in the table, a row-count assertion after the join, `validate="many_to_one"` in pandas, and a dimension test in the pipeline.
- **Fix at the source versus in the query:** a query fix hides bad data and has to be repeated everywhere; fix the dimension load and keep the query guard as a second line.

**Follow-ups:**
- *What if the row count went down?* Look for an INNER JOIN or a WHERE on the right table; compare `left_only` rows.
- *Which is faster to detect, count or sum?* Both; sums catch duplicated rows that still keep distinct counts looking fine.
- *How would a dbt style test express this?* A unique test on the dimension key (a concept; not run here).

**Common mistakes:**
- Papering over it with `SELECT DISTINCT`, which hides the cause and can delete legitimate duplicates.
- Checking only the row count of the final query.
- Joining before checking uniqueness of the lookup table.
- Fixing the query but leaving the bad dimension for the next report.

### Q41 ⭐ 🔴 Join performance at concept level: explain nested-loop, hash and merge joins in plain words, why an index on the join key (and on the foreign key column, not just the primary key) helps, why filtering before joining and selecting fewer columns helps, why functions on join columns (ON LOWER(a.email) = LOWER(b.email) or casts) defeat indexes, and why a missing ON clause explodes. Hedge by engine and say deeper work and EXPLAIN belong to Part 11.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** A join is a nested loop, a hash join or a merge join; indexes on the join columns (especially the foreign key side) let the engine look up matches instead of scanning, filters before the join shrink the inputs, functions on join columns hide the column from the index, and a missing `ON` is a Cartesian product; deeper plan reading is Part 11.

**Schema and sample data:** 200 customers (4 cities, an email in mixed case), 2,000 orders (10 per customer), 100 leads with lower-case emails. The Code block creates them with loops; the tables are:
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, email TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE leads(lead_id INTEGER PRIMARY KEY, email TEXT);
```

**SQL answer:** the Code block runs `EXPLAIN QUERY PLAN` (SQLite's plan output, enough for concepts; Part 11 is the proper place) on the foreign key join before and after `CREATE INDEX ix_orders_customer ON orders(customer_id)`, on the `LOWER()` join before and after an expression index, and counts the rows of a join with no `ON`. The filter-first comparison uses these two queries, which return the same result:
```sql
SELECT c.city, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE o.amount >= 25 GROUP BY c.city ORDER BY c.city
```
```sql
SELECT c.city, SUM(o.amount) AS total FROM customers c
JOIN (SELECT customer_id, amount FROM orders WHERE amount >= 25) o ON o.customer_id = c.customer_id
GROUP BY c.city ORDER BY c.city
```

**pandas answer:** filter, then merge (same text as in the Code block):
```py
p = (customers.merge(orders[orders["amount"] >= 25][["customer_id", "amount"]], on="customer_id")
     .groupby("city", as_index=False).agg(total=("amount", "sum")).sort_values("city").reset_index(drop=True))
```

**Example:** the three join algorithms in plain words.
- **Nested loop:** for each row of the outer table, look up matching rows in the inner table. With an index on the inner join column each lookup is cheap; without one, it scans the inner table every time. Good for small outer inputs.
- **Hash join:** build an in-memory hash table on the smaller input, then stream the larger one and probe it. Good for large unsorted inputs and equality joins; needs memory.
- **Merge join:** sort both inputs on the key (or read them already sorted from an index) and walk through them together. Good when both sides are sorted or very large.
- In my run: 200 customers x 2,000 orders with no `ON` gave 400,000 rows.

**Code:** run with `python3 -I`; the SQL variants are compared with each other and with the pandas filter-then-merge result.
```python
# Q41: join performance at concept level: plans before/after an index, function on a join column, missing ON, filter-first
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, email TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE leads(lead_id INTEGER PRIMARY KEY, email TEXT);
""")
cities = ["Pune", "Delhi", "Chennai", "Kolkata"]
con.executemany("INSERT INTO customers VALUES (?,?,?)",
                [(i, f"User{i}@Example.com", cities[i % 4]) for i in range(1, 201)])
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, (i * 7) % 200 + 1, i % 50) for i in range(1, 2001)])
con.executemany("INSERT INTO leads VALUES (?,?)", [(i, f"user{i}@example.com") for i in range(1, 101)])

def plan(q):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + q).fetchall()]

Q_FK = "SELECT COUNT(*) FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE c.city = 'Pune'"
print("1. join on the foreign key, no index on orders.customer_id:"); [print("   ", p) for p in plan(Q_FK)]
con.execute("CREATE INDEX ix_orders_customer ON orders(customer_id)")
print("   after CREATE INDEX ix_orders_customer:"); [print("   ", p) for p in plan(Q_FK)]

Q_FUNC = "SELECT COUNT(*) FROM leads l JOIN customers c ON LOWER(c.email) = LOWER(l.email)"
Q_PLAIN = "SELECT COUNT(*) FROM leads l JOIN customers c ON c.email = l.email"
print("\n2. LOWER() on both join columns (no index on email yet):"); [print("   ", p) for p in plan(Q_FUNC)]
con.execute("CREATE INDEX ix_cust_email_lower ON customers(LOWER(email))")
print("   after an index on the expression LOWER(email):"); [print("   ", p) for p in plan(Q_FUNC)]
print("   matches:", con.execute(Q_FUNC).fetchone()[0], "| plain equality matches (case differs):", con.execute(Q_PLAIN).fetchone()[0])

n_c, n_o = 200, 2000
print("\n3. missing ON (comma join without a condition):",
      con.execute("SELECT COUNT(*) FROM customers c, orders o").fetchone()[0], "rows =", n_c, "x", n_o)

# 4. filter before join gives the same answer as filter after
Q_AFTER = """SELECT c.city, SUM(o.amount) AS total FROM customers c JOIN orders o ON o.customer_id = c.customer_id
WHERE o.amount >= 25 GROUP BY c.city ORDER BY c.city"""
Q_BEFORE = """SELECT c.city, SUM(o.amount) AS total FROM customers c
JOIN (SELECT customer_id, amount FROM orders WHERE amount >= 25) o ON o.customer_id = c.customer_id
GROUP BY c.city ORDER BY c.city"""
s_after = pd.read_sql_query(Q_AFTER, con)
s_before = pd.read_sql_query(Q_BEFORE, con)
pd.testing.assert_frame_equal(s_after, s_before)
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
p = (customers.merge(orders[orders["amount"] >= 25][["customer_id", "amount"]], on="customer_id")
     .groupby("city", as_index=False).agg(total=("amount", "sum")).sort_values("city").reset_index(drop=True))
pd.testing.assert_frame_equal(s_before, p, check_dtype=False)
print("\n4. filter-first SQL == filter-after SQL == pandas filter-then-merge (sorted by city):")
print(p.to_string(index=False))
big = customers.merge(orders, how="cross")
print("pandas cross merge rows:", len(big))
con.close()
```

**Output (my run):**
```text
1. join on the foreign key, no index on orders.customer_id:
    SCAN o
    SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   after CREATE INDEX ix_orders_customer:
    SCAN c
    SEARCH o USING COVERING INDEX ix_orders_customer (customer_id=?)

2. LOWER() on both join columns (no index on email yet):
    SCAN l
    SCAN c
   after an index on the expression LOWER(email):
    SCAN l
    SEARCH c USING INDEX ix_cust_email_lower (<expr>=?)
   matches: 100 | plain equality matches (case differs): 0

3. missing ON (comma join without a condition): 400000 rows = 200 x 2000

4. filter-first SQL == filter-after SQL == pandas filter-then-merge (sorted by city):
   city  total
Chennai   9620
  Delhi   8880
Kolkata   8880
   Pune   9620
pandas cross merge rows: 400000
```

**Edge cases:**
- **What I ran versus what I know:** the plans above are SQLite's. SQLite's plans only show scans and index searches (nested-loop style), which is why I describe hash and merge joins from general knowledge of other engines (PostgreSQL, SQL Server, Oracle, MySQL 8 and others differ in which algorithms exist and when they choose them); not executed here.
- **The planner can change the join order:** before the index SQLite scanned `orders` and looked up each customer by primary key; after the index it scanned the (city filtered) customers and used the index on `orders.customer_id`. The same query got a different plan, which is the point of indexing the foreign key.
- **Primary keys are indexed, foreign keys usually are not** (in most engines a foreign key column does not get an index automatically); the many side (`orders.customer_id`) is where joins and deletes need one.
- **Functions on join columns:** `LOWER(c.email) = LOWER(l.email)` scanned both tables (two `SCAN` lines). An index on the expression `LOWER(email)` let SQLite search customers; engines that support expression or function-based indexes behave similarly, others need a stored normalised column (hedged).
- **Casts and mismatched types** have the same effect as functions on the column (Q35).
- **Small tables:** a full scan can be the best plan; do not index everything.

**Then explain:**
- **Why an index on the foreign key helps:** the join asks "which orders belong to this customer", and without an index on `orders.customer_id` the engine must read all orders for each customer or build a temporary structure.
- **Why filter before the join (when it is safe):** fewer rows go into the join and the aggregation; in an INNER JOIN the optimiser usually pushes the filter down itself, so the written order often does not matter (my run gave the same result both ways; I did not time it). For a LEFT JOIN, moving a filter changes the result (Q3).
- **Fewer columns:** wide rows cost memory in sorts and hash tables; select only what you need.
- **Missing ON:** the result is the Cartesian product, 200 x 2,000 = 400,000 rows here, and pandas `how="cross"` made the same 400,000 rows.
- **Where it goes next:** reading `EXPLAIN`, statistics, join hints and partitioning are Part 11.

**Follow-ups:**
- *When is a hash join better than a nested loop?* When there is no useful index and both inputs are large.
- *What about a composite index?* Put the equality columns first; order matters (concept; Part 11).
- *Does `SELECT *` matter for joins?* Yes: it blocks covering-index plans and moves extra bytes.

**Common mistakes:**
- Indexing the primary key and forgetting the foreign key.
- Wrapping join columns in `LOWER`, `CAST` or `DATE`.
- Joining first, filtering later, on a LEFT JOIN where the filter changes meaning.
- Claiming one join algorithm is always best.

### Q42 ⭐ 🔴 Join, EXISTS and IN are not always interchangeable: orders(order_id, customer_id) has several rows per customer. Show a case where JOIN returns duplicates and EXISTS does not, a case where NOT IN returns nothing because of a NULL, and a case where the three agree. State a rule for choosing between them for existence checks versus fetching columns from the other table, and the matching pandas idioms.
**Asked at:** explainextended and SQL Server Central write-ups on NOT IN, NOT EXISTS and LEFT JOIN / IS NULL, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** `JOIN` returns one row per match, so it duplicates a customer who has several orders; `EXISTS` and `IN` only test for existence and return the customer once; `NOT IN` silently returns nothing if the subquery has a NULL; and `NOT EXISTS` or a `LEFT JOIN ... IS NULL` is the safe "does not exist" form.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);      -- several rows per customer, one NULL
CREATE TABLE orders_clean(order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL UNIQUE);  -- one row per customer, no NULL
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,1),(104,2),(105,NULL);
INSERT INTO orders_clean VALUES (201,1),(202,2);
```
`orders` has several rows for customer 1 and a NULL customer (guest). `orders_clean` has one row per customer and no NULL.

**SQL answer:** the Code block builds six queries per table with `queries(t)`: `JOIN`, `EXISTS`, `IN`, `NOT EXISTS`, `NOT IN` and `LEFT JOIN IS NULL`. With `t` standing for the table name (`orders` or `orders_clean`), the text in the code is:
```sql
SELECT c.name FROM customers c JOIN {t} o ON o.customer_id = c.customer_id ORDER BY c.customer_id
```
```sql
SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM {t} o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id
```
```sql
SELECT c.name FROM customers c WHERE c.customer_id NOT IN (SELECT customer_id FROM {t}) ORDER BY c.customer_id
```
The Code block fills `{t}` with an f-string; `NOT EXISTS`, `IN` and `LEFT JOIN IS NULL` follow the same pattern in `queries`.

**pandas answer:** (same text as in the Code block)
```py
p_join = customers.merge(orders, on="customer_id").sort_values(["customer_id", "order_id"])["name"].tolist()
p_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
p_not = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
```

**Example:** customers Asha (1), Ben (2), Chitra (3), Dev (4); orders 101, 102, 103 belong to Asha, 104 to Ben, 105 has a NULL customer.
- "Customers who ordered": `JOIN` gives Asha, Asha, Asha, Ben (4 rows, one per order). `EXISTS` and `IN` give Asha, Ben.
- "Customers who never ordered": `NOT EXISTS` and `LEFT JOIN ... IS NULL` give Chitra, Dev. `NOT IN` gives nothing, because the subquery contains the NULL from order 105, so `3 NOT IN (1, 2, NULL)` is UNKNOWN, not TRUE.
- Where they agree: in `orders_clean` (one order per customer, no NULL) `JOIN`, `EXISTS` and `IN` all give Asha, Ben, and the three "never ordered" forms all give Chitra, Dev.

**Code:** run with `python3 -I`; the asserts check each claim above and compare the pandas lists with the SQL form named in the label, in `customer_id` order.
```python
# Q42: JOIN vs EXISTS vs IN: duplicates, the NOT IN NULL trap, and a case where all forms agree
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);      -- several rows per customer, one NULL
CREATE TABLE orders_clean(order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL UNIQUE);  -- one row per customer, no NULL
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,1),(104,2),(105,NULL);
INSERT INTO orders_clean VALUES (201,1),(202,2);
"""
def queries(t):
    return {
        "JOIN":        f"SELECT c.name FROM customers c JOIN {t} o ON o.customer_id = c.customer_id ORDER BY c.customer_id",
        "EXISTS":      f"SELECT c.name FROM customers c WHERE EXISTS (SELECT 1 FROM {t} o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id",
        "IN":          f"SELECT c.name FROM customers c WHERE c.customer_id IN (SELECT customer_id FROM {t}) ORDER BY c.customer_id",
        "NOT EXISTS":  f"SELECT c.name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM {t} o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id",
        "NOT IN":      f"SELECT c.name FROM customers c WHERE c.customer_id NOT IN (SELECT customer_id FROM {t}) ORDER BY c.customer_id",
        "LEFT JOIN IS NULL": f"SELECT c.name FROM customers c LEFT JOIN {t} o ON o.customer_id = c.customer_id WHERE o.order_id IS NULL ORDER BY c.customer_id",
    }
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
res = {}
for t in ("orders", "orders_clean"):
    print(f"--- table {t}")
    res[t] = {k: [r[0] for r in con.execute(q).fetchall()] for k, q in queries(t).items()}
    for k, v in res[t].items():
        print(f"{k:>18}: {v}")

# the three existence forms agree on the clean table, JOIN differs on the duplicated table, NOT IN fails on NULLs
c = res["orders_clean"]
assert c["JOIN"] == c["EXISTS"] == c["IN"] == ["Asha", "Ben"]
assert c["NOT EXISTS"] == c["NOT IN"] == c["LEFT JOIN IS NULL"] == ["Chitra", "Dev"]
d = res["orders"]
assert d["JOIN"] == ["Asha", "Asha", "Asha", "Ben"] and d["EXISTS"] == d["IN"] == ["Asha", "Ben"]
assert d["NOT IN"] == [] and d["NOT EXISTS"] == d["LEFT JOIN IS NULL"] == ["Chitra", "Dev"]

# pandas idioms
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
p_join = customers.merge(orders, on="customer_id").sort_values(["customer_id", "order_id"])["name"].tolist()
p_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
p_semi = customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id").sort_values("customer_id")["name"].tolist()
p_not = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
p_anti = (customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
          .query("_merge == 'left_only'").sort_values("customer_id")["name"].tolist())
print("\npandas merge (like JOIN):", p_join)
print("pandas isin (like EXISTS/IN):", p_in)
print("pandas merge on dropped-duplicate keys (semi-join):", p_semi)
print("pandas ~isin (like NOT EXISTS, NOT like NOT IN):", p_not)
print("pandas anti-join via indicator:", p_anti)
assert p_join == d["JOIN"] and p_in == p_semi == d["EXISTS"] and p_not == p_anti == d["NOT EXISTS"]
print("asserts passed: pandas matches the SQL form named in each label (lists in customer_id order)")
con.close()
```

**Output (my run):**
```text
--- table orders
              JOIN: ['Asha', 'Asha', 'Asha', 'Ben']
            EXISTS: ['Asha', 'Ben']
                IN: ['Asha', 'Ben']
        NOT EXISTS: ['Chitra', 'Dev']
            NOT IN: []
 LEFT JOIN IS NULL: ['Chitra', 'Dev']
--- table orders_clean
              JOIN: ['Asha', 'Ben']
            EXISTS: ['Asha', 'Ben']
                IN: ['Asha', 'Ben']
        NOT EXISTS: ['Chitra', 'Dev']
            NOT IN: ['Chitra', 'Dev']
 LEFT JOIN IS NULL: ['Chitra', 'Dev']

pandas merge (like JOIN): ['Asha', 'Asha', 'Asha', 'Ben']
pandas isin (like EXISTS/IN): ['Asha', 'Ben']
pandas merge on dropped-duplicate keys (semi-join): ['Asha', 'Ben']
pandas ~isin (like NOT EXISTS, NOT like NOT IN): ['Chitra', 'Dev']
pandas anti-join via indicator: ['Chitra', 'Dev']
asserts passed: pandas matches the SQL form named in each label (lists in customer_id order)
```

**Edge cases:**
- **JOIN duplicates are a feature when you need columns from orders** (for example the order amount), and a bug when you only need the customer.
- **`IN` with NULL on the positive side is fine** (it can still be TRUE); only `NOT IN` breaks.
- **`SELECT DISTINCT` after a JOIN** fixes the duplicates for existence checks but costs a sort or hash, and it hides fan-out when you also select other columns.
- **Empty subquery:** `NOT IN` returns every customer, `NOT EXISTS` also.
- **pandas:** `~isin` ignores the NULL problem and returns Chitra and Dev (it matches `NOT EXISTS`, not the SQL `NOT IN`), which is why SQL and pandas answers differ in the trap case. NaN in `isin` is covered in Part 1 Q13.

**Then explain:**
- **Rule 1:** if you only need to test whether a related row exists, use `EXISTS` (or `NOT EXISTS`); it is NULL-safe and cannot duplicate rows.
- **Rule 2:** if you need columns from the other table, use a `JOIN`, and make sure you know the grain (one row per match) or aggregate first.
- **Rule 3:** use `IN` when the subquery column is `NOT NULL`, or filter NULLs in it; avoid `NOT IN` unless you can guarantee that.
- **Performance:** the optimiser often turns these into the same semi-join or anti-join plan, but that is engine specific (hedged, not executed); correctness differences matter first.
- **pandas idioms:** `merge` is the JOIN (duplicates included), `isin` or a merge on `drop_duplicates()` keys is the semi-join, `~isin` or `merge(..., indicator=True)` with `left_only` is the anti-join.

**Follow-ups:**
- *Is `EXISTS` slower than `IN`?* Not necessarily; a modern optimiser usually plans both as a semi-join (hedged, engine dependent).
- *What about `<> ALL`?* It is the same as `NOT IN` and has the same NULL problem.
- *How do you return one row per customer with the latest order amount?* That needs a join plus a selection rule (Part 4); `EXISTS` alone cannot return columns.

**Common mistakes:**
- Using `JOIN` for an existence check and then counting customers with `COUNT(*)`.
- Using `NOT IN` against a nullable column.
- Believing the three are always interchangeable.
- Fixing duplicates with `DISTINCT` and not noticing the fan-out in other columns.

### Q43 ⭐ 🔴 Dialect map for joins (answers must hedge and run only what SQLite can): FULL and RIGHT JOIN support (SQLite 3.39+, MySQL has neither FULL), EXCEPT versus MINUS, INTERSECT in MySQL, USING and NATURAL semantics, joined-column output order, cross join syntax (CROSS JOIN versus comma), and the lateral idea (not covered here). Present as a table with a 'verified by running on SQLite' column and a 'hedged, not executed' column.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** On SQLite 3.45.1 I ran INNER, LEFT, RIGHT, FULL, CROSS (both spellings), INTERSECT, EXCEPT, USING and NATURAL; MINUS, `<=>` and LATERAL failed there; everything about PostgreSQL, MySQL, Oracle, SQL Server, BigQuery and Snowflake in the table is from memory and not executed.

**Schema and sample data:** `l` has ids 1, 2, 3 and `r` has ids 2, 3, 4, so there are two matches, one left-only row and one right-only row.
```sql
CREATE TABLE l(id INTEGER, v TEXT);
CREATE TABLE r(id INTEGER, w TEXT);
INSERT INTO l VALUES (1,'l1'),(2,'l2'),(3,'l3');
INSERT INTO r VALUES (2,'r2'),(3,'r3'),(4,'r4');
```

**SQL answer:** the queries run in the Code block, with `attempt()` catching errors so a failing feature prints its error instead of stopping the script. The two columns the question asks for:

| Feature | Verified by running on SQLite 3.45.1 | Hedged, not executed |
|---|---|---|
| RIGHT JOIN | works; 3 rows; same rows as the LEFT JOIN with the tables swapped | PostgreSQL, SQL Server, Oracle, MySQL, BigQuery and Snowflake support it, to my knowledge; I believe SQLite added it in 3.39 (from memory; I only ran 3.45.1) |
| FULL OUTER JOIN | works; 4 rows | PostgreSQL, SQL Server, Oracle, BigQuery and Snowflake support it; MySQL has no FULL OUTER JOIN (the MySQL 8.4 join page shows only LEFT and RIGHT) |
| EXCEPT versus MINUS | `EXCEPT` works (returned 1); `MINUS` gave a syntax error | Oracle uses `MINUS` (older versions have no `EXCEPT`, as I recall); PostgreSQL, SQL Server, BigQuery and Snowflake use `EXCEPT` (Snowflake also accepts `MINUS`) |
| INTERSECT | works (returned 2 and 3) | MySQL support depends on version (added in 8.0.31 from memory; check your version) |
| USING | `SELECT *` returned `id, v, w` (one `id`); also worked with RIGHT and FULL JOIN | PostgreSQL and MySQL support it, with differences in how a qualified `l.id` behaves after an outer join; SQL Server does not support USING; check each manual |
| NATURAL JOIN | worked, same columns as USING (`id, v, w`) | supported in PostgreSQL, MySQL, Oracle and others (not SQL Server); it joins on all same-named columns (Q21) |
| Joined-column output order | ON: `id, v, id, w` (both keys, left columns then right); USING and NATURAL: the shared key first, then the rest | the standard puts the USING/NATURAL columns first; MySQL's join page documents the same coalesced order; I did not run MySQL |
| Cross join syntax | `CROSS JOIN` and the comma form both gave 9 rows | both are standard SQL and accepted widely; some engines or modes treat a comma join differently with precedence against explicit JOINs (hedged) |
| LATERAL | `LATERAL` gave a syntax error in SQLite | PostgreSQL, MySQL 8.0.14 and later and Snowflake support `LATERAL` (SQL Server uses `CROSS APPLY`); the lateral idea is not covered here |
| Null-safe equality | `IS NOT DISTINCT FROM` worked (returned 1) and `NULL IS NULL` returned 1; `<=>` gave a syntax error | PostgreSQL has `IS NOT DISTINCT FROM`; MySQL has `<=>`; others vary |

**pandas answer:** the parallels, run in the same Code block and compared by row count against the SQL result:
```py
l.merge(r, on="id", how="inner")
l.merge(r, on="id", how="outer")
l.merge(r, how="cross")
```
`how="right"` and `how="left"` map to the RIGHT and LEFT joins, `how="cross"` is CROSS JOIN, `on="id"` returns one key column like USING, and `left_on`/`right_on` returns both columns like ON. pandas has no NATURAL join (and `merge` with no `on` joins on all common column names by default, which is the same trap as NATURAL JOIN).

**Example:** by hand, INNER gives ids 2 and 3 (2 rows); LEFT adds id 1 (3 rows); RIGHT adds id 4 instead (3 rows); FULL has both unmatched rows (4 rows); CROSS is 3 x 3 = 9 rows. `l INTERSECT r` gives 2 and 3, and `l EXCEPT r` gives 1.

**Code:** run with `python3 -I`; it asserts the SQLite row counts equal the pandas counts, that RIGHT JOIN equals the swapped LEFT JOIN, and that INTERSECT and EXCEPT equal Python set operations on the ids.
```python
# Q43: join dialect map: run each feature on SQLite 3.45 and record what happens (other engines are NOT executed)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE l(id INTEGER, v TEXT);
CREATE TABLE r(id INTEGER, w TEXT);
INSERT INTO l VALUES (1,'l1'),(2,'l2'),(3,'l3');
INSERT INTO r VALUES (2,'r2'),(3,'r3'),(4,'r4');
""")
print("SQLite version:", sqlite3.sqlite_version)

def attempt(q):
    try:
        cur = con.execute(q)
        rows = cur.fetchall()
        return [d[0] for d in cur.description], rows
    except sqlite3.Error as e:
        return None, f"{type(e).__name__}: {e}"

l = pd.read_sql_query("SELECT * FROM l", con)
r = pd.read_sql_query("SELECT * FROM r", con)

# 1. join types: row counts, compared with pandas how=
checks = {
    "INNER JOIN":      ("SELECT * FROM l INNER JOIN r ON l.id = r.id", l.merge(r, on="id", how="inner")),
    "LEFT JOIN":       ("SELECT * FROM l LEFT JOIN r ON l.id = r.id", l.merge(r, on="id", how="left")),
    "RIGHT JOIN":      ("SELECT * FROM l RIGHT JOIN r ON l.id = r.id", l.merge(r, on="id", how="right")),
    "FULL OUTER JOIN": ("SELECT * FROM l FULL OUTER JOIN r ON l.id = r.id", l.merge(r, on="id", how="outer")),
    "CROSS JOIN":      ("SELECT * FROM l CROSS JOIN r", l.merge(r, how="cross")),
    "comma join":      ("SELECT * FROM l, r", l.merge(r, how="cross")),
}
print("\njoin type: SQLite rows | pandas rows")
for name, (q, pdf) in checks.items():
    cols, rows = attempt(q)
    assert isinstance(rows, list) and len(rows) == len(pdf), name
    print(f"{name:>16}: {len(rows)} | {len(pdf)}")
# RIGHT JOIN is the LEFT JOIN with the tables swapped (same rows, columns in a different order)
a = sorted(map(tuple, con.execute("SELECT r.id, r.w, l.v FROM l RIGHT JOIN r ON l.id = r.id").fetchall()), key=str)
b = sorted(map(tuple, con.execute("SELECT r.id, r.w, l.v FROM r LEFT JOIN l ON l.id = r.id").fetchall()), key=str)
assert a == b
print("RIGHT JOIN == swapped LEFT JOIN: True")

# 2. set operators
for name, q in [("INTERSECT", "SELECT id FROM l INTERSECT SELECT id FROM r"),
                ("EXCEPT", "SELECT id FROM l EXCEPT SELECT id FROM r"),
                ("MINUS", "SELECT id FROM l MINUS SELECT id FROM r")]:
    cols, rows = attempt(q)
    print(f"{name:>9}: {rows}")
assert [x[0] for x in con.execute("SELECT id FROM l INTERSECT SELECT id FROM r ORDER BY id")] == sorted(set(l.id) & set(r.id))
assert [x[0] for x in con.execute("SELECT id FROM l EXCEPT SELECT id FROM r ORDER BY id")] == sorted(set(l.id) - set(r.id))

# 3. USING / NATURAL / ON: which columns does SELECT * return, and in what order
print("\nSELECT * column lists:")
for name, q in [("ON", "SELECT * FROM l JOIN r ON l.id = r.id"),
                ("USING (id)", "SELECT * FROM l JOIN r USING (id)"),
                ("NATURAL JOIN", "SELECT * FROM l NATURAL JOIN r"),
                ("RIGHT JOIN USING", "SELECT * FROM l RIGHT JOIN r USING (id)"),
                ("FULL JOIN USING", "SELECT * FROM l FULL JOIN r USING (id)")]:
    cols, rows = attempt(q)
    print(f"{name:>17}: {cols}")
print("FULL JOIN USING rows:", attempt("SELECT * FROM l FULL JOIN r USING (id) ORDER BY id")[1])
print("qualified l.id with USING in a FULL JOIN:", attempt("SELECT l.id, r.id FROM l FULL JOIN r USING (id) ORDER BY 1, 2")[1])
print("pandas merge on='id' columns:", list(l.merge(r, on="id").columns),
      "| left_on/right_on columns:", list(l.merge(r.rename(columns={"id": "rid"}), left_on="id", right_on="rid").columns))

# 4. null-safe equality spellings and LATERAL
print("\nnull-safe equality in SQLite: NULL IS NULL ->", con.execute("SELECT NULL IS NULL").fetchone()[0],
      "| NULL IS NOT DISTINCT FROM NULL ->", con.execute("SELECT NULL IS NOT DISTINCT FROM NULL").fetchone()[0],
      "| NULL <=> NULL ->", attempt("SELECT NULL <=> NULL")[1])
print("LATERAL:", attempt("SELECT * FROM l, LATERAL (SELECT * FROM r WHERE r.id = l.id)")[1])
con.close()
```

**Output (my run):**
```text
SQLite version: 3.45.1

join type: SQLite rows | pandas rows
      INNER JOIN: 2 | 2
       LEFT JOIN: 3 | 3
      RIGHT JOIN: 3 | 3
 FULL OUTER JOIN: 4 | 4
      CROSS JOIN: 9 | 9
      comma join: 9 | 9
RIGHT JOIN == swapped LEFT JOIN: True
INTERSECT: [(2,), (3,)]
   EXCEPT: [(1,)]
    MINUS: OperationalError: near "SELECT": syntax error

SELECT * column lists:
               ON: ['id', 'v', 'id', 'w']
       USING (id): ['id', 'v', 'w']
     NATURAL JOIN: ['id', 'v', 'w']
 RIGHT JOIN USING: ['id', 'v', 'w']
  FULL JOIN USING: ['id', 'v', 'w']
FULL JOIN USING rows: [(1, 'l1', None), (2, 'l2', 'r2'), (3, 'l3', 'r3'), (4, None, 'r4')]
qualified l.id with USING in a FULL JOIN: [(None, 4), (1, None), (2, 2), (3, 3)]
pandas merge on='id' columns: ['id', 'v', 'w'] | left_on/right_on columns: ['id', 'v', 'rid', 'w']

null-safe equality in SQLite: NULL IS NULL -> 1 | NULL IS NOT DISTINCT FROM NULL -> 1 | NULL <=> NULL -> OperationalError: near ">": syntax error
LATERAL: OperationalError: near "SELECT": syntax error
```

**Edge cases:**
- **Qualified key after a FULL JOIN with USING:** in my run `SELECT l.id, r.id ... FULL JOIN ... USING (id)` returned the left and right keys separately, with NULLs on the unmatched side, while `SELECT id` (or `*`) returned the coalesced value. Use the unqualified name.
- **MINUS error message:** SQLite parsed `MINUS` as an alias, so the error is a confusing `near "SELECT": syntax error`.
- **Set operators and NULLs:** `INTERSECT` and `EXCEPT` treat NULLs as equal and remove duplicates (Q29).
- **pandas:** `merge` without `on` uses every common column name, so it behaves like NATURAL JOIN unless you pass `on`.

**Then explain:**
- **Portable subset:** `INNER JOIN`, `LEFT JOIN`, `CROSS JOIN` and `ON` work everywhere; for FULL JOIN emulate with `LEFT JOIN ... UNION ALL` plus an anti-join (Q32) when the engine lacks it.
- **Where I am sure and where not:** what is in the left result column was executed; the right column is from general knowledge and manuals as I remember them, and versions matter (MySQL INTERSECT and EXCEPT, SQLite RIGHT and FULL JOIN). Always check the engine's current documentation.
- **Lateral:** the idea (a subquery in FROM that can see columns of earlier FROM items) is outside this part; SQLite does not have it.

**Follow-ups:**
- *Why avoid RIGHT JOIN?* Swap the tables and use LEFT JOIN; readers think left to right.
- *How do you port a FULL JOIN to MySQL?* LEFT JOIN, then `UNION ALL` the right-only rows via an anti-join (Q32).
- *Does `UNION` behave like `INTERSECT` on NULL?* Both treat NULLs as equal for de-duplication (Q29).

**Common mistakes:**
- Assuming every engine supports FULL JOIN, USING or INTERSECT.
- Assuming `SELECT *` from a USING join gives two key columns.
- Using NATURAL JOIN in shared code.
- Writing `MINUS` in an engine that expects `EXCEPT`.

### Q44 ⭐ 🔴 Case: reconcile orders(order_id, amount) with payments(payment_id, order_id, paid_amount), where an order can have several partial payments and some payments reference unknown orders. Produce a status per order (unpaid, partial, paid, overpaid) and list orphan payments. Explain why you must aggregate payments to one row per order before joining (fan-out), the FULL or LEFT plus anti-join structure, and give the pandas groupby then merge with indicator=True and assert that total paid ties out.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Aggregate the payments to one row per order first, then LEFT JOIN that to orders and classify with a CASE, because joining orders straight to payments repeats each order once per payment and inflates every order total; list orphan payments with a separate anti-join on the payments side.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, paid_amount INTEGER);
INSERT INTO orders VALUES (1,100),(2,200),(3,50),(4,80),(5,120);
INSERT INTO payments VALUES
 (1,1,100),            -- order 1 paid in full
 (2,2,120),(3,2,50),   -- order 2 partial (170 of 200)
 (4,3,60),             -- order 3 overpaid
 (5,5,70),(6,5,50),    -- order 5 paid in full with two payments
 (7,99,40),            -- orphan: unknown order
 (8,NULL,25);          -- orphan: no order id at all
```

**SQL answer:** the Code block holds `SQL_MAIN` (status per order), `SQL_ORPHANS`, `SQL_WRONG` (the fan-out bug) and `SQL_FULL` (the one-pass FULL JOIN structure).
```sql
SELECT o.order_id, o.amount, COALESCE(p.paid, 0) AS paid,
       CASE WHEN p.paid IS NULL THEN 'unpaid'
            WHEN p.paid < o.amount THEN 'partial'
            WHEN p.paid = o.amount THEN 'paid'
            ELSE 'overpaid' END AS status
FROM orders o
LEFT JOIN (SELECT order_id, SUM(paid_amount) AS paid FROM payments GROUP BY order_id) p
       ON p.order_id = o.order_id
ORDER BY o.order_id
```
```sql
SELECT pm.payment_id, pm.order_id, pm.paid_amount
FROM payments pm LEFT JOIN orders o ON o.order_id = pm.order_id
WHERE o.order_id IS NULL
ORDER BY pm.payment_id
```
`SQL_FULL` does both in one statement: a FULL JOIN of orders to the aggregated payments, with `COALESCE(o.order_id, p.order_id)` as the key and a status of `orphan` when the order side is missing. Its limit: the payments aggregate has one row per `order_id`, so all payments with a NULL `order_id` collapse into one row (25 here) and you lose the payment-level detail, which is why I use the anti-join for the orphan list.

**pandas answer:** (same text as in the Code block)
```py
paid = payments.groupby("order_id", as_index=False).agg(paid=("paid_amount", "sum"))     # NaN order_id group is dropped by default
m = orders.merge(paid, on="order_id", how="left", validate="one_to_one")
chk = payments.merge(orders[["order_id"]], on="order_id", how="left", indicator=True)
```
The Code block then fills the missing paid values with 0, sets the status with four `loc` assignments (default overpaid, then paid, partial and unpaid overwrite it), and builds the orphan list from the `left_only` rows of `chk`.

**Example:** orders 1 to 5 have amounts 100, 200, 50, 80, 120.
- Order 1: one payment of 100, so paid 100 = amount, status paid.
- Order 2: payments 120 and 50, so 170 < 200, partial.
- Order 3: payment 60 > 50, overpaid.
- Order 4: no payment, paid 0, unpaid (the aggregate has no row, so `p.paid IS NULL`).
- Order 5: payments 70 and 50 sum to 120 = amount, paid (two payments, one order).
- Orphans: payment 7 (order 99 does not exist) and payment 8 (NULL order id).
- Tie-out: all payments 515 = matched 450 (100 + 170 + 60 + 0 + 120) + orphan 65 (40 + 25).
- The fan-out bug: summing `o.amount` after joining directly to payments gave 790 against a true order total of 550, because orders 2 and 5 are counted twice.

**Code:** run with `python3 -I`; the status table is compared sorted by `order_id`, the orphan list sorted by `payment_id`, and the tie-out is asserted in both SQL and pandas.
```python
# Q44: reconcile orders with partial payments: aggregate payments first, status per order, orphan payments, tie-out
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER);
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, order_id INTEGER, paid_amount INTEGER);
INSERT INTO orders VALUES (1,100),(2,200),(3,50),(4,80),(5,120);
INSERT INTO payments VALUES
 (1,1,100),            -- order 1 paid in full
 (2,2,120),(3,2,50),   -- order 2 partial (170 of 200)
 (4,3,60),             -- order 3 overpaid
 (5,5,70),(6,5,50),    -- order 5 paid in full with two payments
 (7,99,40),            -- orphan: unknown order
 (8,NULL,25);          -- orphan: no order id at all
"""
SQL_MAIN = """
SELECT o.order_id, o.amount, COALESCE(p.paid, 0) AS paid,
       CASE WHEN p.paid IS NULL THEN 'unpaid'
            WHEN p.paid < o.amount THEN 'partial'
            WHEN p.paid = o.amount THEN 'paid'
            ELSE 'overpaid' END AS status
FROM orders o
LEFT JOIN (SELECT order_id, SUM(paid_amount) AS paid FROM payments GROUP BY order_id) p
       ON p.order_id = o.order_id
ORDER BY o.order_id
"""
SQL_ORPHANS = """
SELECT pm.payment_id, pm.order_id, pm.paid_amount
FROM payments pm LEFT JOIN orders o ON o.order_id = pm.order_id
WHERE o.order_id IS NULL
ORDER BY pm.payment_id
"""
SQL_WRONG = """
SELECT SUM(o.amount) AS inflated_order_total
FROM orders o JOIN payments pm ON pm.order_id = o.order_id
"""
# the single-pass FULL JOIN structure: one row per order, plus one row per orphan order_id group
SQL_FULL = """
SELECT COALESCE(o.order_id, p.order_id) AS order_id, o.amount, p.paid,
       CASE WHEN o.order_id IS NULL THEN 'orphan' WHEN p.paid IS NULL THEN 'unpaid'
            WHEN p.paid < o.amount THEN 'partial' WHEN p.paid = o.amount THEN 'paid' ELSE 'overpaid' END AS status
FROM orders o
FULL JOIN (SELECT order_id, SUM(paid_amount) AS paid FROM payments GROUP BY order_id) p ON p.order_id = o.order_id
ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
sql_orph = pd.read_sql_query(SQL_ORPHANS, con)
print("status per order:"); print(sql_df.to_string(index=False))
print("\norphan payments:"); print(sql_orph.to_string(index=False))
print("\nFULL JOIN version (NULL order_id group sorts first):"); print(pd.read_sql_query(SQL_FULL, con).to_string(index=False))
print("\ntrue order total:", con.execute("SELECT SUM(amount) FROM orders").fetchone()[0],
      "| joined straight to payments:", con.execute(SQL_WRONG).fetchone()[0])

# pandas
orders = pd.read_sql_query("SELECT * FROM orders", con)
payments = pd.read_sql_query("SELECT * FROM payments", con)
print("\npayments.order_id dtype:", payments["order_id"].dtype, "(NULL became NaN)")
paid = payments.groupby("order_id", as_index=False).agg(paid=("paid_amount", "sum"))     # NaN order_id group is dropped by default
m = orders.merge(paid, on="order_id", how="left", validate="one_to_one")
m["paid"] = m["paid"].fillna(0).astype("int64")
m["status"] = "overpaid"
m.loc[m["paid"] == m["amount"], "status"] = "paid"
m.loc[m["paid"] < m["amount"], "status"] = "partial"
m.loc[m["paid"] == 0, "status"] = "unpaid"
p_df = m[["order_id", "amount", "paid", "status"]].sort_values("order_id").reset_index(drop=True)
chk = payments.merge(orders[["order_id"]], on="order_id", how="left", indicator=True)
p_orph = (chk[chk["_merge"] == "left_only"][["payment_id", "order_id", "paid_amount"]]
          .sort_values("payment_id").reset_index(drop=True))
pd.testing.assert_frame_equal(sql_df, p_df, check_dtype=False)
pd.testing.assert_frame_equal(sql_orph, p_orph, check_dtype=False)
print("asserts passed: status table and orphan list equal SQL (sorted by order_id / payment_id)")

# tie-out: every payment is either on a known order or an orphan
total_paid = int(payments["paid_amount"].sum())
matched = int(p_df["paid"].sum())
orph = int(p_orph["paid_amount"].sum())
print(f"tie-out: total payments {total_paid} = matched {matched} + orphan {orph}")
assert total_paid == matched + orph
g_total = int(paid["paid"].sum())
print("sum of the groupby result (default dropna=True):", g_total, "vs total payments", total_paid,
      "-> the NaN-order_id payment of", total_paid - g_total, "is silently missing from it")
assert total_paid - g_total == 25
sql_tie = con.execute("SELECT (SELECT SUM(paid_amount) FROM payments), "
                      "(SELECT SUM(pm.paid_amount) FROM payments pm JOIN orders o ON o.order_id = pm.order_id), "
                      "(SELECT SUM(paid_amount) FROM payments pm WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.order_id = pm.order_id))").fetchone()
print("SQL tie-out (all, matched, orphan):", sql_tie)
assert sql_tie == (total_paid, matched, orph)
con.close()
```

**Output (my run):**
```text
status per order:
 order_id  amount  paid   status
        1     100   100     paid
        2     200   170  partial
        3      50    60 overpaid
        4      80     0   unpaid
        5     120   120     paid

orphan payments:
 payment_id  order_id  paid_amount
          7      99.0           40
          8       NaN           25

FULL JOIN version (NULL order_id group sorts first):
 order_id  amount  paid   status
      NaN     NaN  25.0   orphan
      1.0   100.0 100.0     paid
      2.0   200.0 170.0  partial
      3.0    50.0  60.0 overpaid
      4.0    80.0   NaN   unpaid
      5.0   120.0 120.0     paid
     99.0     NaN  40.0   orphan

true order total: 550 | joined straight to payments: 790

payments.order_id dtype: float64 (NULL became NaN)
asserts passed: status table and orphan list equal SQL (sorted by order_id / payment_id)
tie-out: total payments 515 = matched 450 + orphan 65
sum of the groupby result (default dropna=True): 490 vs total payments 515 -> the NaN-order_id payment of 25 is silently missing from it
SQL tie-out (all, matched, orphan): (515, 450, 65)
```

**Edge cases:**
- **Status boundaries:** equality on integers is safe; on money stored as floats compare with a rounded difference (`ABS(paid - amount) < 0.005`) or store cents as integers. My toy data uses integers.
- **NULL `order_id` payments:** an INNER or LEFT join to orders never matches a NULL key, so they are orphans in the anti-join. The pandas `groupby` dropped the NaN group by default, so the grouped total (490) was 25 short of the 515 total; the orphan list built from the raw payments is what restores the tie-out.
- **Zero-amount or negative payments (refunds):** `SUM` nets them, so an order can be partial after a refund; decide if refunds belong here.
- **Order with amount 0 and no payment:** status unpaid by my CASE (since `paid IS NULL`), though arguably paid; define the rule.
- **Duplicate payment rows (same payment loaded twice):** the sum doubles; check `payment_id` uniqueness first.
- **pandas dtype:** `payments.order_id` came back `float64` because of the NULL, which is harmless for the merge (see Q35).

**Then explain:**
- **Why aggregate first:** the merge between orders and payments is one-to-many; aggregating payments to one row per `order_id` makes it one-to-one, which `validate="one_to_one"` proves in pandas.
- **Structure:** LEFT JOIN from orders answers "what is the status of every order"; the anti-join from payments answers "which payments have no order". A FULL JOIN can do both, at the cost of losing payment-level detail for NULL-key orphans.
- **Tie-out as a test:** total payments must equal matched plus orphan payments; assert it, because a mismatch means a dropped NULL group or a double count.
- **Status rules written down:** unpaid (no payments), partial (0 < paid < amount), paid (equal), overpaid (greater). State what you do for an amount of 0.

**Follow-ups:**
- *What if a payment can reference several orders?* Then you need an allocation table; the join becomes many-to-many (Q45).
- *How do you find which payment caused the overpayment?* That needs a running total ordered by date (Part 5, windows).
- *How would you monitor this daily?* Run the tie-out as a scheduled check and alert if orphan totals grow (a concept, not run).

**Common mistakes:**
- Joining payments directly and summing order amounts.
- Using an INNER JOIN and losing unpaid orders.
- Writing the status CASE in the wrong order, so overpaid is tested after paid with `>=`.
- Ignoring NULL `order_id` payments and finding the totals do not tie.

### Q45 ⭐ 🔴 Many-to-many comparison, a harder one: promo_codes(code, customer_id) has duplicate rows and customers can hold several codes, while orders(order_id, customer_id, amount) has several orders per customer. Report revenue by promo code without double counting an order that several codes of one customer touch, or deciding it must be allocated. Explain the many-to-many fan-out, the policy choices (count once per code, split, or pick one), the check that totals tie to orders, and the pandas merge with validate and groupby.
**Asked at:** data-modelling write-ups on fan and chasm traps (Coginiti, Sisense, Holistics; snippets), not candidate reports; analyst and data scientist rounds and BI debugging
**Say this first (1 line):** First de-duplicate the promo rows to one row per (code, customer), then choose and state a policy because a customer's orders belong to several codes: count the full order in each code (overlapping, does not add up to total revenue), split each order equally across the customer's codes, or pick one code per customer (both tie to the order total); check that the totals tie in every policy.

**Schema and sample data:**
```sql
CREATE TABLE promo_codes(code TEXT, customer_id INTEGER);          -- duplicates possible
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO promo_codes VALUES ('SAVE10',1),('SAVE10',1),('VIP',1),('SAVE10',2),('VIP',3),('FEST',3);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,80),(4,3,60),(5,3,40),(6,4,30);
```
Customer 1 has `SAVE10` (loaded twice) and `VIP`; customer 2 has `SAVE10`; customer 3 has `VIP` and `FEST`; customer 4 has no code.

**SQL answer:** the Code block holds `SQL_NAIVE` and the three policies `SQL_ONCE`, `SQL_SPLIT` and `SQL_PICK`; `DEDUP` is the derived table `(SELECT DISTINCT code, customer_id FROM promo_codes)` used by the first two (an f-string in the code, so I describe it instead of pasting the rendered text).
```sql
SELECT p.code, SUM(o.amount) AS revenue
FROM promo_codes p JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
```
```sql
SELECT p.code, SUM(o.amount) AS revenue
FROM (SELECT customer_id, MIN(code) AS code FROM promo_codes GROUP BY customer_id) p
JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
```
`SQL_ONCE` is the naive query with `promo_codes` replaced by `DEDUP`. `SQL_SPLIT` joins `DEDUP` to a per-customer count of codes (`COUNT(*) ... GROUP BY customer_id` over `DEDUP`) and sums `o.amount * 1.0 / n.n_codes`. `SQL_PICK` takes `MIN(code)` per customer as the chosen code; "alphabetically first" is only a placeholder rule, so use a business rule (first used, highest priority) in real work.

**pandas answer:** (same text as in the Code block)
```py
pd_dedup = promo.drop_duplicates()
once = orders.merge(pd_dedup, on="customer_id", validate="many_to_many")          # many-to-many on purpose, after de-duplication
p_once = once.groupby("code")["amount"].sum()
pick = promo.groupby("customer_id", as_index=False).agg(code=("code", "min"))
pk = orders.merge(pick, on="customer_id", validate="many_to_one")
```
The split policy merges `once` with the per-customer code counts and sums `amount / n_codes` per code.

**Example:** orders: customer 1 has 100 and 50 (150), customer 2 has 80, customer 3 has 60 and 40 (100), customer 4 has 30. Total 360; orders of customers who hold a code: 330.
- Naive join (duplicates not removed): SAVE10 380, VIP 250, FEST 100, sum 730 against 330 for customers with a code: customer 1's duplicate SAVE10 row doubles 150, and the overlaps add more.
- Once per code: SAVE10 = 150 + 80 = 230, VIP = 150 + 100 = 250, FEST = 100; sum 580. It is 250 more than 330 because customer 1 (150) and customer 3 (100) sit in two codes each. This is right for "revenue touched by each code" but the codes must not be added up.
- Split equally: SAVE10 = 75 + 80 = 155, VIP = 75 + 50 = 125, FEST = 50; sum 330, which ties.
- Pick one (the alphabetically first code): customer 1 gets SAVE10, customer 2 SAVE10, customer 3 FEST; SAVE10 230, FEST 100, VIP has nothing; sum 330, which ties.
- Customer 4 (30) has no code and sits outside all policies; 330 + 30 = 360.

**Code:** run with `python3 -I`; each policy is compared between SQL and pandas as a code-to-revenue mapping, and the tie-out is asserted.
```python
# Q45: revenue by promo code when customers hold several codes: dedupe, then three allocation policies, with tie-out
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE promo_codes(code TEXT, customer_id INTEGER);          -- duplicates possible
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO promo_codes VALUES ('SAVE10',1),('SAVE10',1),('VIP',1),('SAVE10',2),('VIP',3),('FEST',3);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,80),(4,3,60),(5,3,40),(6,4,30);
"""
DEDUP = "(SELECT DISTINCT code, customer_id FROM promo_codes)"
SQL_NAIVE = """
SELECT p.code, SUM(o.amount) AS revenue
FROM promo_codes p JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
SQL_ONCE = f"""
SELECT p.code, SUM(o.amount) AS revenue
FROM {DEDUP} p JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
SQL_SPLIT = f"""
SELECT p.code, SUM(o.amount * 1.0 / n.n_codes) AS revenue
FROM {DEDUP} p
JOIN (SELECT customer_id, COUNT(*) AS n_codes FROM {DEDUP} GROUP BY customer_id) n ON n.customer_id = p.customer_id
JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
SQL_PICK = """
SELECT p.code, SUM(o.amount) AS revenue
FROM (SELECT customer_id, MIN(code) AS code FROM promo_codes GROUP BY customer_id) p
JOIN orders o ON o.customer_id = p.customer_id
GROUP BY p.code ORDER BY p.code
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
total_orders = con.execute("SELECT SUM(amount) FROM orders").fetchone()[0]
with_code = con.execute("SELECT SUM(amount) FROM orders WHERE customer_id IN (SELECT customer_id FROM promo_codes)").fetchone()[0]
print("order total:", total_orders, "| orders of customers holding at least one code:", with_code)
sql = {k: dict(con.execute(q).fetchall()) for k, q in
       [("naive", SQL_NAIVE), ("once per code", SQL_ONCE), ("split equally", SQL_SPLIT), ("pick one (MIN code)", SQL_PICK)]}
for k, v in sql.items():
    print(f"{k:>20}: {v}  sum = {sum(v.values())}")

# pandas
promo = pd.read_sql_query("SELECT * FROM promo_codes", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("\nduplicate promo rows:", int(promo.duplicated().sum()))
try:
    orders.merge(promo, on="customer_id", validate="many_to_one")
except pd.errors.MergeError as e:
    print("validate='many_to_one' on the promo table ->", type(e).__name__ + ":", e)
pd_dedup = promo.drop_duplicates()
once = orders.merge(pd_dedup, on="customer_id", validate="many_to_many")          # many-to-many on purpose, after de-duplication
p_once = once.groupby("code")["amount"].sum()
n_codes = pd_dedup.groupby("customer_id").size().rename("n_codes").reset_index()
sp = once.merge(n_codes, on="customer_id", validate="many_to_one")
p_split = (sp["amount"] / sp["n_codes"]).groupby(sp["code"]).sum()
pick = promo.groupby("customer_id", as_index=False).agg(code=("code", "min"))
pk = orders.merge(pick, on="customer_id", validate="many_to_one")
p_pick = pk.groupby("code")["amount"].sum()
for k, s in [("once per code", p_once), ("split equally", p_split), ("pick one (MIN code)", p_pick)]:
    assert {c: float(v) for c, v in s.items()} == {c: float(v) for c, v in sql[k].items()}, k
print("pandas == SQL for all three policies (compared as code -> revenue)")

# tie-out checks
assert sum(sql["once per code"].values()) > with_code               # overlap by design
assert sum(sql["split equally"].values()) == with_code
assert sum(sql["pick one (MIN code)"].values()) == with_code
assert sum(sql["split equally"].values()) + (total_orders - with_code) == total_orders
print("tie-out: split and pick sum to", with_code, "(+", total_orders - with_code, "with no code =", total_orders,
      "); once-per-code sums to", sum(sql["once per code"].values()), "by design, so it must not be added up")
con.close()
```

**Output (my run):**
```text
order total: 360 | orders of customers holding at least one code: 330
               naive: {'FEST': 100, 'SAVE10': 380, 'VIP': 250}  sum = 730
       once per code: {'FEST': 100, 'SAVE10': 230, 'VIP': 250}  sum = 580
       split equally: {'FEST': 50.0, 'SAVE10': 155.0, 'VIP': 125.0}  sum = 330.0
 pick one (MIN code): {'FEST': 100, 'SAVE10': 230}  sum = 330

duplicate promo rows: 1
validate='many_to_one' on the promo table -> MergeError: Merge keys are not unique in right dataset; not a many-to-one merge

Duplicates in right:
  customer_id
           1
           1
           3 ...
pandas == SQL for all three policies (compared as code -> revenue)
tie-out: split and pick sum to 330 (+ 30 with no code = 360 ); once-per-code sums to 580 by design, so it must not be added up
```

**Edge cases:**
- **Duplicate promo rows:** one duplicate (`SAVE10`, customer 1) doubled that customer's orders in the naive query; fix it with `DISTINCT` or a unique constraint on `(code, customer_id)`.
- **Customers without a code:** an INNER JOIN drops them, so the totals do not reach 360; add a "no code" bucket with a LEFT JOIN if you need the grand total to tie.
- **Customer with codes but no orders:** contributes nothing; use a LEFT JOIN from codes if you want codes with 0 revenue to appear.
- **Float rounding in the split:** 1.0 multiplication keeps decimals, so sums can differ in the last digit; round at the end or store cents (my data splits cleanly).
- **Time:** a code may apply only to orders after it was issued; this table has no dates, so the example ignores that, but in real data the join needs a date condition.
- **pandas `validate`:** `many_to_one` on the promo side raised `MergeError`, which is exactly what you want to see before deduplicating; `many_to_many` is accepted but checks nothing, so I use it only after the dedupe, on purpose.

**Then explain:**
- **Why it fans out:** orders and promo codes are both many per customer, so joining them on `customer_id` is many-to-many: every order is repeated once per code row (and once more per duplicate row).
- **Policy choice:** the join cannot decide for you. Count in each code (marketing wants "revenue influenced"), split (finance wants totals that add up), or pick one (a rule such as last touch or priority). Say which one you used next to the number.
- **Tie-out:** split and pick must sum to the revenue of customers with a code (330), and plus the no-code bucket to the order total (360); once-per-code must exceed it by the overlap (580 against 330 here).
- **Order of operations:** de-duplicate, decide allocation, then join and group; never aggregate after a many-to-many join without knowing the policy.
- **True attribution:** a promo is normally attached to the order (an `order_promos` table), not the customer; if you have that, join on `order_id` and the fan-out shrinks (a design point, not run).

**Follow-ups:**
- *What if one order really uses two codes?* Then the grain is (order, code) and you split by a rule or weight; the check is still that the allocated amounts sum to the order amount.
- *How do you show the overlap?* Count orders in more than one code (a `COUNT(DISTINCT code)` per customer greater than 1).
- *Can `COUNT(DISTINCT order_id)` fix this?* It would fix a count of orders per code, but not a `SUM` (Q13).

**Common mistakes:**
- Summing revenue across codes and presenting it as the total.
- Leaving duplicate promo rows in the join.
- Not saying which allocation policy was used.
- Using `SUM(DISTINCT amount)`, which drops legitimate equal amounts.
