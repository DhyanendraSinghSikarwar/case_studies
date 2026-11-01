### Q10 ⭐⭐⭐ 🔴 Debug 'my index is not used': orders(order_id, customer_id, status, order_date, amount, code TEXT) with 200,000 rows and indexes on customer_id, (status, order_date), code and a partial index on (customer_id) WHERE status = 'cancelled'. For seven complaints (a function on the column, a leading-wildcard LIKE, a predicate on the second column of a composite index only, OR across two different columns, a NOT/!= predicate on a column where 90% of rows match, a query that does not repeat the partial index's WHERE, and an index that exists but stale statistics make the planner prefer another path) print the plan, name the cause and give the fix. Include the case where a scan is the right choice (low selectivity: the index would touch most of the table) and show it with VM steps. Finish with a checklist an interviewer would accept (plan first, predicate shape, types, column order, statistics, selectivity, then hints), noting INDEXED BY exists but is a last resort.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Read the plan first, then check seven things in order: is the predicate sargable (no function on the column), does the LIKE have a fixed prefix, is the filter on the leading column of the index, is it an OR across unindexed columns, would the index touch most of the table anyway, does the query repeat the partial index's WHERE, and are the statistics current; a scan is the right answer when the index would visit most of the table.

**Schema and sample data:** 200,000 seeded rows (the full generator is in the Code block; `random.Random(11)`), status 90% delivered, 6% placed, 3% cancelled, 1% returned. A tiny hand-checkable slice of the same shape:
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL, code TEXT);
INSERT INTO orders VALUES (1,5,'delivered','2024-03-05',10.0,'12'),(2,5,'cancelled','2024-03-06',20.0,'127'),
                          (3,7,'delivered','2024-03-05',30.0,'7'),(4,9,'placed','2024-04-01',40.0,'1207');
CREATE INDEX ix_cust ON orders(customer_id);
CREATE INDEX ix_st_dt ON orders(status, order_date);
CREATE INDEX ix_code ON orders(code);
CREATE INDEX ix_part ON orders(customer_id) WHERE status = 'cancelled';
```

**SQL answer:** each complaint is a pair (bad query, fix); every pair is printed with its plan, VM steps and row count in the Code block. The fixes:
- Function on the column: `customer_id + 0 = 5` becomes `customer_id = 5`; `substr(code, 1, 2) = '12'` becomes `code >= '12' AND code < '13'` (same rows, asserted).
- Leading wildcard: `code LIKE '%7'` cannot use a B-tree on `code` at all (there is no fix inside the index; the usual answers are a reversed-suffix column, a full-text or trigram index, or accepting the scan, not executed here). A prefix `LIKE '12%'` is a different story: on a default (BINARY) index it still scans, because LIKE is case-insensitive in SQLite, and `CREATE INDEX ... (code COLLATE NOCASE)` fixes it.
- Second column only: `WHERE order_date = '2024-03-05'` on `(status, order_date)`: add `CREATE INDEX ix_dt ON orders(order_date)`.
- OR across columns: add an index on the other column (SQLite then plans a MULTI-INDEX OR) or rewrite as `UNION`.
- `!=` on 97%: no fix needed, the scan is right.
- Partial index: repeat the literal `status = 'cancelled'` in the query.
- Statistics: `ANALYZE`.

**pandas answer:** pandas has no planner: a boolean mask such as `df[df.customer_id == 5]` is always a full pass over the column. The pandas side of this question is therefore the oracle: every query above is re-computed with masks (`df.code.str.startswith("12")`, `(df.customer_id == 5) | (df.amount > 490)` and so on) and the sorted `order_id` lists are asserted equal to the SQL results. If you need repeated lookups in pandas, `set_index("customer_id").sort_index()` plus `.loc[5]` is the index analogue.

**Example:** take `customer_id + 0 = 5`. The index `ix_cust` is sorted by the stored `customer_id` values, so a lookup of `5` is a binary search. `customer_id + 0` is a different value computed row by row, so the sorted order says nothing about where `= 5` lives and the engine must evaluate it on every row: the plan prints `SCAN orders` and the run cost 800,147 VM steps for 12 rows, against 183 steps for `customer_id = 5` (`SEARCH ... USING INDEX ix_cust (customer_id=?)`). On the 4-row slice above, customer 5 is orders 1 and 2 in both forms; only the cost differs. The same walk for `status != 'cancelled'`: the index sorts by status, the rows you want are everything except one block, which is not a contiguous range, and 97% of the table qualifies, so a scan is also the cheapest honest plan.

**Code:** one Python file, run with `python3 -I`; it uses temporary file databases (not `:memory:`) because every plan and step count is read on a fresh connection (see Edge cases for why). Results are compared after sorting by `order_id`.
```python
# Q10
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

# ---------- data: 200,000 orders, status skewed (90% delivered) ----------
rng = random.Random(11)
statuses = ["delivered"] * 90 + ["placed"] * 6 + ["cancelled"] * 3 + ["returned"] * 1
rows = [(i, rng.randint(1, 20000), rng.choice(statuses),
         "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
         round(rng.uniform(5, 500), 2), str(rng.randint(1, 5000))) for i in range(1, 200001)]
DDL = "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL, code TEXT)"

def build(name, index_sql):
    path = WORK + "/" + name
    c = sqlite3.connect(path)
    c.execute(DDL)
    c.executemany("INSERT INTO orders VALUES(?,?,?,?,?,?)", rows)
    for s in index_sql:
        c.execute(s)
    c.commit(); c.close()
    return path

IDX = ["CREATE INDEX ix_cust ON orders(customer_id)",
       "CREATE INDEX ix_st_dt ON orders(status, order_date)",
       "CREATE INDEX ix_code ON orders(code)",
       "CREATE INDEX ix_part ON orders(customer_id) WHERE status = 'cancelled'"]
db = build("main.db", IDX)
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "order_date", "amount", "code"])

def show(label, path, sql, params=()):
    st, res = steps(path, sql, params)
    print(f"{label}\n   plan : {' | '.join(plan(path, sql, params))}\n   steps: {st:,}   rows: {len(res):,}")
    return sorted(r[0] for r in res)          # order_ids, compared after sorting

print("=== 1. function on the column ===")
a = show("bad : customer_id + 0 = 5", db, "SELECT * FROM orders WHERE customer_id + 0 = 5")
b = show("good: customer_id = 5", db, "SELECT * FROM orders WHERE customer_id = 5")
assert a == b == sorted(df.order_id[df.customer_id == 5])
a = show("bad : substr(code, 1, 2) = '12'", db, "SELECT * FROM orders WHERE substr(code, 1, 2) = '12'")
b = show("good: code >= '12' AND code < '13'", db, "SELECT * FROM orders WHERE code >= '12' AND code < '13'")
assert a == b == sorted(df.order_id[df.code.str.startswith("12")])

print("=== 2. leading wildcard ===")
a = show("bad : code LIKE '%7'", db, "SELECT * FROM orders WHERE code LIKE '%7'")
assert a == sorted(df.order_id[df.code.str.endswith("7")])
a = show("prefix LIKE '12%' on a BINARY index", db, "SELECT * FROM orders WHERE code LIKE '12%'")
c = sqlite3.connect(db); c.execute("CREATE INDEX ix_code_nc ON orders(code COLLATE NOCASE)"); c.commit(); c.close()
b = show("prefix LIKE '12%' after a NOCASE index", db, "SELECT * FROM orders WHERE code LIKE '12%'")
assert a == b
c = sqlite3.connect(db); c.execute("DROP INDEX ix_code_nc"); c.commit(); c.close()
c = sqlite3.connect(db); c.execute("PRAGMA case_sensitive_like = ON")
print("   with PRAGMA case_sensitive_like=ON, BINARY index only:",
      " | ".join(r[3] for r in c.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE code LIKE '12%'")))
c.close()

print("=== 3. second column of the composite index only ===")
a = show("bad : order_date = '2024-03-05'  (before ANALYZE)", db, "SELECT * FROM orders WHERE order_date = '2024-03-05'")
c = sqlite3.connect(db); c.execute("ANALYZE"); c.commit(); c.close()
b = show("same query after ANALYZE (skip-scan possible)", db, "SELECT * FROM orders WHERE order_date = '2024-03-05'")
c = sqlite3.connect(db); c.execute("CREATE INDEX ix_dt ON orders(order_date)"); c.commit(); c.close()
e = show("good: index on order_date", db, "SELECT * FROM orders WHERE order_date = '2024-03-05'")
assert a == b == e == sorted(df.order_id[df.order_date == "2024-03-05"])

print("=== 4. OR across two columns ===")
a = show("bad : customer_id = 5 OR amount > 490 (amount unindexed)", db, "SELECT * FROM orders WHERE customer_id = 5 OR amount > 490")
c = sqlite3.connect(db); c.execute("CREATE INDEX ix_amt ON orders(amount)"); c.commit(); c.close()
b = show("good: index on amount too", db, "SELECT * FROM orders WHERE customer_id = 5 OR amount > 490")
u = show("UNION rewrite", db, "SELECT * FROM orders WHERE customer_id = 5 UNION SELECT * FROM orders WHERE amount > 490")
assert a == b == u == sorted(df.order_id[(df.customer_id == 5) | (df.amount > 490)])

print("=== 5. != on a column where 97% of rows match ===")
a = show("status != 'cancelled'", db, "SELECT * FROM orders WHERE status != 'cancelled'")
b = show("INDEXED BY ix_st_dt (forced)", db, "SELECT * FROM orders INDEXED BY ix_st_dt WHERE status != 'cancelled'")
assert a == b == sorted(df.order_id[df.status != "cancelled"])
a = show("status != 'delivered' (10% match, still a scan)", db, "SELECT * FROM orders WHERE status != 'delivered'")
b = show("status IN ('placed','cancelled','returned')", db, "SELECT * FROM orders WHERE status IN ('placed', 'cancelled', 'returned')")
assert a == b

print("=== 6. partial index, WHERE not repeated (only the partial index on customer_id exists) ===")
dbp = build("partial.db", ["CREATE INDEX ix_part ON orders(customer_id) WHERE status = 'cancelled'"])
a = show("customer_id = 5", dbp, "SELECT * FROM orders WHERE customer_id = 5")
b = show("customer_id = 5 AND status = 'cancelled'", dbp, "SELECT * FROM orders WHERE customer_id = 5 AND status = 'cancelled'")
c_ = show("customer_id = 5 AND status IN ('cancelled')", dbp, "SELECT * FROM orders WHERE customer_id = 5 AND status IN ('cancelled')")
assert b == sorted(df.order_id[(df.customer_id == 5) & (df.status == "cancelled")])

print("=== 7. stale statistics (small table analysed while b was constant, then grown) ===")
dbs = WORK + "/stale.db"
c = sqlite3.connect(dbs)
c.execute("CREATE TABLE w(id INTEGER PRIMARY KEY, a INT, b INT)")
c.execute("CREATE INDEX ix_a ON w(a)"); c.execute("CREATE INDEX ix_b ON w(b)")
c.executemany("INSERT INTO w(a, b) VALUES(?, ?)", [(i % 2, 7) for i in range(1000)])
c.execute("ANALYZE"); c.commit()
print("   stat1 when analysed:", c.execute("SELECT idx, stat FROM sqlite_stat1 ORDER BY idx").fetchall())
r2 = random.Random(5)
w_rows = [(r2.randint(0, 1), r2.randint(1, 100000)) for _ in range(200000)]
c.executemany("INSERT INTO w(a, b) VALUES(?, ?)", w_rows); c.commit()
print("   stat1 after 200,000 more rows (not refreshed):", c.execute("SELECT idx, stat FROM sqlite_stat1 ORDER BY idx").fetchall())
q = "SELECT * FROM w WHERE a = 1 AND b = 500"
q2 = "SELECT * FROM w WHERE b = 500"
sa = show("stale stats: a = 1 AND b = 500", dbs, q)
sb = show("stale stats: b = 500", dbs, q2)
c.execute("ANALYZE"); c.commit()
print("   stat1 after re-ANALYZE:", c.execute("SELECT idx, stat FROM sqlite_stat1 ORDER BY idx").fetchall())
print("   same connection that ran ANALYZE, EXPLAIN b = 500:", " | ".join(r[3] for r in c.execute("EXPLAIN QUERY PLAN " + q2 + " ")))
c.close()
fa = show("fresh stats: a = 1 AND b = 500", dbs, q)
fb = show("fresh stats: b = 500", dbs, q2)
assert sa == fa and sb == fb

print("=== 8. a scan is the right choice (status = 'delivered', 90% of rows) ===")
dbm = db
a = show("planner choice", dbm, "SELECT * FROM orders WHERE status = 'delivered'")
b = show("NOT INDEXED (forced scan)", dbm, "SELECT * FROM orders NOT INDEXED WHERE status = 'delivered'")
d_ = show("INDEXED BY ix_st_dt (forced)", dbm, "SELECT * FROM orders INDEXED BY ix_st_dt WHERE status = 'delivered'")
assert a == b == d_ == sorted(df.order_id[df.status == "delivered"])
print("   pandas: a boolean mask is always a full scan; rows =", int((df.status == "delivered").sum()))
```

**Output (my run):**
```text
=== 1. function on the column ===
bad : customer_id + 0 = 5
   plan : SCAN orders
   steps: 800,147   rows: 12
good: customer_id = 5
   plan : SEARCH orders USING INDEX ix_cust (customer_id=?)
   steps: 183   rows: 12
bad : substr(code, 1, 2) = '12'
   plan : SCAN orders
   steps: 834,636   rows: 4,323
good: code >= '12' AND code < '13'
   plan : SEARCH orders USING INDEX ix_code (code>? AND code<?)
   steps: 47,609   rows: 4,323
=== 2. leading wildcard ===
bad : code LIKE '%7'
   plan : SCAN orders
   steps: 961,994   rows: 20,243
prefix LIKE '12%' on a BINARY index
   plan : SCAN orders
   steps: 834,634   rows: 4,323
prefix LIKE '12%' after a NOCASE index
   plan : SEARCH orders USING INDEX ix_code_nc (code>? AND code<?)
   steps: 47,613   rows: 4,323
   with PRAGMA case_sensitive_like=ON, BINARY index only: SEARCH orders USING INDEX ix_code (code>? AND code<?)
=== 3. second column of the composite index only ===
bad : order_date = '2024-03-05'  (before ANALYZE)
   plan : SCAN orders
   steps: 604,818   rows: 596
same query after ANALYZE (skip-scan possible)
   plan : SEARCH orders USING INDEX ix_st_dt (ANY(status) AND order_date=?)
   steps: 6,669   rows: 596
good: index on order_date
   plan : SEARCH orders USING INDEX ix_dt (order_date=?)
   steps: 6,647   rows: 596
=== 4. OR across two columns ===
bad : customer_id = 5 OR amount > 490 (amount unindexed)
   plan : SCAN orders
   steps: 1,232,481   rows: 4,053
good: index on amount too
   plan : MULTI-INDEX OR | INDEX 1 | SEARCH orders USING INDEX ix_cust (customer_id=?) | INDEX 2 | SEARCH orders USING INDEX ix_amt (amount>?)
   steps: 56,866   rows: 4,053
UNION rewrite
   plan : COMPOUND QUERY | LEFT-MOST SUBQUERY | SEARCH orders USING INDEX ix_cust (customer_id=?) | UNION USING TEMP B-TREE | SEARCH orders USING INDEX ix_amt (amount>?)
   steps: 77,136   rows: 4,053
=== 5. != on a column where 97% of rows match ===
status != 'cancelled'
   plan : SCAN orders
   steps: 2,151,937   rows: 193,980
INDEXED BY ix_st_dt (forced)
   plan : SCAN orders USING INDEX ix_st_dt
   steps: 2,351,938   rows: 193,980
status != 'delivered' (10% match, still a scan)
   plan : SCAN orders
   steps: 761,201   rows: 20,138
status IN ('placed','cancelled','returned')
   plan : SCAN orders
   steps: 1,761,211   rows: 20,138
=== 6. partial index, WHERE not repeated (only the partial index on customer_id exists) ===
customer_id = 5
   plan : SCAN orders
   steps: 600,125   rows: 12
customer_id = 5 AND status = 'cancelled'
   plan : SEARCH orders USING INDEX ix_part (customer_id=?)
   steps: 34   rows: 0
customer_id = 5 AND status IN ('cancelled')
   plan : SCAN orders
   steps: 600,055   rows: 0
=== 7. stale statistics (small table analysed while b was constant, then grown) ===
   stat1 when analysed: [('ix_a', '1000 500'), ('ix_b', '1000 1000')]
   stat1 after 200,000 more rows (not refreshed): [('ix_a', '1000 500'), ('ix_b', '1000 1000')]
stale stats: a = 1 AND b = 500
   plan : SEARCH w USING INDEX ix_a (a=?)
   steps: 503,672   rows: 0
stale stats: b = 500
   plan : SCAN w
   steps: 603,067   rows: 2
   stat1 after re-ANALYZE: [('ix_a', '201000 100500'), ('ix_b', '201000 3')]
   same connection that ran ANALYZE, EXPLAIN b = 500: SCAN w
fresh stats: a = 1 AND b = 500
   plan : SEARCH w USING INDEX ix_b (b=?)
   steps: 74   rows: 0
fresh stats: b = 500
   plan : SEARCH w USING INDEX ix_b (b=?)
   steps: 74   rows: 2
=== 8. a scan is the right choice (status = 'delivered', 90% of rows) ===
planner choice
   plan : SEARCH orders USING INDEX ix_st_dt (status=?)
   steps: 1,978,580   rows: 179,862
NOT INDEXED (forced scan)
   plan : SCAN orders
   steps: 2,038,993   rows: 179,862
INDEXED BY ix_st_dt (forced)
   plan : SEARCH orders USING INDEX ix_st_dt (status=?)
   steps: 1,978,580   rows: 179,862
   pandas: a boolean mask is always a full scan; rows = 179862
```

**Edge cases:**
- **Stale EXPLAIN is real.** In my Wave A checks, re-running the identical `EXPLAIN QUERY PLAN` text after `DROP INDEX` still printed the old plan on the same connection. In section 7 above, the same connection that ran `ANALYZE` printed `SCAN w` for `b = 500`, while a fresh connection printed `SEARCH w USING INDEX ix_b (b=?)`. So after any index or statistics change, read the plan on a new connection. I did not find the cause in the documentation; this is observed behaviour of the Python 3.13 / SQLite 3.45.1 combination.
- **Skip-scan surprise.** Before `ANALYZE`, `order_date = '2024-03-05'` against `(status, order_date)` is a `SCAN orders` (604,818 steps). After `ANALYZE` SQLite chose `SEARCH ... (ANY(status) AND order_date=?)` (6,669 steps), a skip-scan that probes each of the four status values. A dedicated `ix_dt` index cost 6,647 steps, the same order of magnitude here only because status has four values; with thousands of status values the skip-scan would be bad (SQLite uses it only when the leading column has few distinct values per its statistics).
- **`!=` never uses the index in these runs**, even for `status != 'delivered'` (10% of rows, 761,201 steps). Rewriting it as `status IN ('placed','cancelled','returned')` gave `SCAN orders` after `ANALYZE` (1,761,211 steps, slower than the `!=` scan) because the planner's single average estimate (50,000 rows per status) made three probes look as expensive as a scan.
- **Partial index with `IN`.** `status IN ('cancelled')` did not use `ix_part`, `status = 'cancelled'` did; `customer_id = 5` alone scanned when only the partial index existed (600,125 steps vs 34).
- **LIKE and `PRAGMA case_sensitive_like`.** With `case_sensitive_like = ON`, the BINARY index was used for `LIKE '12%'`. The pragma changes results for text with letters, so it is a semantic switch, not a tuning flag (the pragma is documented as deprecated; it still ran on 3.45.1).
- **Scan is right, steps do not show random I/O.** For `status = 'delivered'` (90% of rows) the index path cost 1,978,580 steps and a forced `NOT INDEXED` scan 2,038,993: the step counts are almost equal, but the index path does one table seek per entry, which on a disk-resident table is random page access that VM steps do not count. Do not claim the index "wins" from steps here; the honest statement is: no win, extra work in a real system.
- `INDEXED BY` did not error for an index that could only be scanned; the error case is shown in Q18.

**Then explain:**
- **Checklist (what I would say):** (1) get the plan, `EXPLAIN QUERY PLAN` in SQLite (`EXPLAIN ANALYZE` in PostgreSQL, not executed here); (2) predicate shape: no function or arithmetic on the indexed column, no leading wildcard; (3) types and collation: a text index with a different collation is not used by LIKE (types did not break the index in my SQLite checks; other engines can differ, not executed); (4) column order: equality columns first, leftmost prefix; (5) statistics: `ANALYZE`; (6) selectivity: would the index touch most rows; (7) only then hints (`INDEXED BY`, `NOT INDEXED`, unary `+`), a last resort because they pin a plan that may be wrong after the data changes.
- **Why each case fails:** an index is a sorted copy of the key, so it helps only when the question can be answered by a range or a lookup on that sorted key.
- **OR:** SQLite can answer `a OR b` with two index probes only when both sides are indexed; one unindexed side forces a scan.
- **Selectivity:** the planner's statistics in this table said "50,000 rows per status" for every status; the real count of `cancelled` was 3% and `delivered` 90% (Q18 digs into this).
- **Other engines (not executed):** PostgreSQL can use expression indexes and `pg_trgm` for leading-wildcard LIKE, MySQL 8 can use functional indexes, SQL Server can use computed columns with an index; I have not run any of these here.

**Follow-ups:**
- *The query is slow but the index is used: what now?* Compare estimated and actual rows, count the table lookups, and ask whether the index is covering (Q13).
- *Would you add an index for every slow query?* No: each index slows writes and takes space (Q16).
- *Is a full scan always bad?* No: for a query that returns most of the table it is the cheapest plan.

**Common mistakes:**
- Wrapping the column in `LOWER()`, `DATE()`, `strftime()` or arithmetic instead of moving the function to the constant side.
- Believing that "an index exists" means "the index will be used".
- Forcing the index with a hint on a low-selectivity predicate and leaving it in the code.
- Reading a plan from an old connection after changing indexes or statistics.
- Quoting step counts as wall-clock time.

### Q11 ⭐⭐⭐ 🟡 ORDER BY with LIMIT, with and without an index: orders(order_id, customer_id, order_date, amount) with 200,000 rows. Print plans and count VM steps for ORDER BY amount LIMIT 10 (USE TEMP B-TREE FOR ORDER BY), the same after CREATE INDEX on amount, ORDER BY order_date DESC LIMIT 10 with an index on order_date (the index is read backwards), WHERE customer_id = ? ORDER BY order_date with only an index on customer_id (temp b-tree for the matches) versus an index on (customer_id, order_date) (no sort), and a missing LIMIT. Explain why LIMIT without ORDER BY gives arbitrary rows, why a sort of K rows costs K log K, the 'top-N heap' idea (described for PostgreSQL top-N heapsort, not executed), and why ORDER BY + LIMIT is only cheap when an index delivers the order.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** `ORDER BY ... LIMIT k` is cheap only when an index already delivers the rows in the requested order, so the engine can stop after k rows; otherwise it must read and sort everything (a temp b-tree in SQLite), and `LIMIT` without `ORDER BY` returns arbitrary rows.

**Schema and sample data:** 200,000 seeded rows (generator in the Code block). Hand-checkable slice:
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, amount REAL);
INSERT INTO orders VALUES (1,5,'2024-03-01',30.0),(2,5,'2024-03-09',10.0),(3,6,'2024-03-05',10.0),(4,5,'2024-03-02',99.0);
```

**SQL answer:** in the Code block, in four groups: (A) `ORDER BY amount, order_id LIMIT 10` with and without `CREATE INDEX ix_amt ON orders(amount)`; (B) `ORDER BY order_date DESC, order_id DESC LIMIT 10` with and without an index on `order_date`; (C) `WHERE customer_id = 5 ORDER BY order_date, order_id` with an index on `customer_id` only, then with `(customer_id, order_date)`; (D) `LIMIT 3` without `ORDER BY`, before and after an index. I add `order_id` as a tie-break everywhere, because `amount` and `order_date` repeat and `ORDER BY amount LIMIT 10` alone is ambiguous when the 10th and 11th rows tie.

**pandas answer:** `df.sort_values(["amount", "order_id"]).head(10)` and `df.nsmallest(10, "amount")`; both are asserted equal to the SQL rows (same order, the sort key list is the ORDER BY). `nsmallest` keeps the first of tied values by row position, which equals `order_id` order here because the frame is in `order_id` order.

**Example:** in the slice, `ORDER BY amount, order_id LIMIT 2` gives (2, 10.0) and (3, 10.0): amounts tie at 10.0 and `order_id` decides. Without an index SQLite reads all 4 rows, sorts them, and returns the first two. With `ix_amt` the index entries are ordered by (amount, rowid), so reading the first two entries is the answer and the other two rows are never read. On the real 200,000 rows that is 1,600,363 VM steps against 88.

**Code:** run with `python3 -I`; compare the lists exactly (they are ordered).
```python
# Q11
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

rng = random.Random(21)
rows = [(i, rng.randint(1, 20000), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
         round(rng.uniform(5, 500), 2)) for i in range(1, 200001)]
DDL = "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, amount REAL)"
def build(name, idx):
    path = WORK + "/" + name
    c = sqlite3.connect(path); c.execute(DDL)
    c.executemany("INSERT INTO orders VALUES(?,?,?,?)", rows)
    for s in idx: c.execute(s)
    c.commit(); c.close(); return path
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date", "amount"])

def run(label, path, sql, params=()):
    st, res = steps(path, sql, params)
    print(f"{label}\n   plan : {' | '.join(plan(path, sql, params))}\n   steps: {st:,}   rows: {len(res)}")
    return res

def add(path, sql):
    c = sqlite3.connect(path); c.execute(sql); c.commit(); c.close()

db = build("o.db", [])
print("--- A. ORDER BY amount LIMIT 10 ---")
q = "SELECT order_id, amount FROM orders ORDER BY amount, order_id LIMIT 10"
a = run("no index", db, q)
add(db, "CREATE INDEX ix_amt ON orders(amount)")
b = run("index on amount (rowid is the hidden last column, so the order_id tie-break is free)", db, q)
run("no LIMIT, index on amount", db, "SELECT order_id, amount FROM orders ORDER BY amount, order_id")
run("LIMIT 10 but ORDER BY amount DESC, order_id", db, "SELECT order_id, amount FROM orders ORDER BY amount DESC, order_id LIMIT 10")
p = df.sort_values(["amount", "order_id"]).head(10)
assert a == b == list(zip(p.order_id, p.amount))
nl = df.nsmallest(10, "amount")           # keep='first' on ties: ties are broken by row position (= order_id here)
assert list(nl.order_id) == list(p.order_id)

print("--- B. ORDER BY order_date DESC LIMIT 10 (index read backwards) ---")
q = "SELECT order_id, order_date FROM orders ORDER BY order_date DESC, order_id DESC LIMIT 10"
a = run("no index on order_date", db, q)
add(db, "CREATE INDEX ix_dt ON orders(order_date)")
b = run("index on order_date", db, q)
p = df.sort_values(["order_date", "order_id"], ascending=False).head(10)
assert a == b == list(zip(p.order_id, p.order_date))
run("ORDER BY order_date DESC, order_id ASC (mixed direction)", db, "SELECT order_id, order_date FROM orders ORDER BY order_date DESC, order_id ASC LIMIT 10")

print("--- C. WHERE customer_id = ? ORDER BY order_date ---")
q = "SELECT order_id, order_date FROM orders WHERE customer_id = 5 ORDER BY order_date, order_id"
add(db, "CREATE INDEX ix_cust ON orders(customer_id)")
a = run("index on customer_id only", db, q)
add(db, "CREATE INDEX ix_cust_dt ON orders(customer_id, order_date)")
b = run("plus index on (customer_id, order_date)", db, q)
p = df[df.customer_id == 5].sort_values(["order_date", "order_id"])
assert a == b == list(zip(p.order_id, p.order_date))

print("--- D. LIMIT without ORDER BY is arbitrary ---")
q = "SELECT order_id, amount FROM orders WHERE amount > 495 LIMIT 3"
db2 = build("o2.db", [])
x = run("no index on amount", db2, q)
add(db2, "CREATE INDEX ix_amt ON orders(amount)")
y = run("after CREATE INDEX on amount (same SQL text)", db2, q)
print("   first run :", x); print("   second run:", y)
assert x != y
```

**Output (my run):**
```text
--- A. ORDER BY amount LIMIT 10 ---
no index
   plan : SCAN orders | USE TEMP B-TREE FOR ORDER BY
   steps: 1,600,363   rows: 10
index on amount (rowid is the hidden last column, so the order_id tie-break is free)
   plan : SCAN orders USING COVERING INDEX ix_amt
   steps: 88   rows: 10
no LIMIT, index on amount
   plan : SCAN orders USING COVERING INDEX ix_amt
   steps: 1,000,028   rows: 200000
LIMIT 10 but ORDER BY amount DESC, order_id
   plan : SCAN orders USING COVERING INDEX ix_amt | USE TEMP B-TREE FOR RIGHT PART OF ORDER BY
   steps: 225   rows: 10
--- B. ORDER BY order_date DESC LIMIT 10 (index read backwards) ---
no index on order_date
   plan : SCAN orders | USE TEMP B-TREE FOR ORDER BY
   steps: 1,401,933   rows: 10
index on order_date
   plan : SCAN orders USING COVERING INDEX ix_dt
   steps: 85   rows: 10
ORDER BY order_date DESC, order_id ASC (mixed direction)
   plan : SCAN orders USING COVERING INDEX ix_dt | USE TEMP B-TREE FOR RIGHT PART OF ORDER BY
   steps: 7,968   rows: 10
--- C. WHERE customer_id = ? ORDER BY order_date ---
index on customer_id only
   plan : SEARCH orders USING INDEX ix_cust (customer_id=?) | USE TEMP B-TREE FOR ORDER BY
   steps: 194   rows: 12
plus index on (customer_id, order_date)
   plan : SEARCH orders USING COVERING INDEX ix_cust_dt (customer_id=?)
   steps: 115   rows: 12
--- D. LIMIT without ORDER BY is arbitrary ---
no index on amount
   plan : SCAN orders
   steps: 597   rows: 3
after CREATE INDEX on amount (same SQL text)
   plan : SEARCH orders USING COVERING INDEX ix_amt (amount>?)
   steps: 48   rows: 3
   first run : [(125, 499.04), (129, 497.11), (140, 496.76)]
   second run: [(39725, 495.01), (78384, 495.01), (138241, 495.01)]
```

**Edge cases:**
- **Ties.** The index on `amount` also orders by the hidden rowid, so `ORDER BY amount, order_id` is free (`order_id` is the rowid here). `ORDER BY amount DESC, order_id` (mixed directions) needed `USE TEMP B-TREE FOR RIGHT PART OF ORDER BY`: SQLite reads the index backwards and only sorts within each group of equal amounts (225 steps, because the first 10 rows were reached quickly). Likewise `order_date DESC, order_id ASC` cost 7,968 steps versus 85 for the matching direction, because the groups of equal dates are large.
- **Few rows after a filter.** In (C) both plans cost 194 and 115 steps for 12 rows: the temp b-tree only sorts the 12 matching rows, so the missing composite index is a small cost there. The difference grows with the number of matches per customer, not with table size.
- **No LIMIT.** `ORDER BY amount` with no LIMIT still walked the whole index (1,000,028 steps for 200,000 rows): the index saves the sort but not the read.
- **LIMIT without ORDER BY.** The same SQL text `... WHERE amount > 495 LIMIT 3` returned order_ids 125, 129, 140 (amounts 499.04, 497.11, 496.76) before the index and 39725, 78384, 138241 (all 495.01) after it: the engine returns whatever it reaches first, and a new index changed which rows those were. Nothing in SQL promises either answer.
- **Covering.** These queries select only columns present in the index (amount and the rowid), so the plan says `COVERING INDEX`; selecting a column that is not in the index would add a table lookup per row.

**Then explain:**
- **Cost of a sort:** sorting n rows is about n log n comparisons; keeping only the best k with a heap is about n log k, and reading from an index in order is about k. PostgreSQL has a "top-N heapsort" node for `ORDER BY ... LIMIT` (described, not executed here); SQLite prints only `USE TEMP B-TREE FOR ORDER BY` and I did not measure whether it limits the size of the sorter, so I do not claim it.
- **Index order:** a B-tree index is sorted, so it can be read forwards or backwards; `DESC` on the query does not need a `DESC` index (my run: `order_date DESC` used the plain `ix_dt` with no sort step).
- **Rule of thumb:** put the equality columns first and the ORDER BY column next, `(customer_id, order_date)`, so the matching rows come out already sorted.
- **pandas:** `sort_values` sorts everything; `nsmallest/nlargest` avoids a full sort for small k (Wave A timed 3 ms against 11 ms on 200,000 rows, machine-specific, not re-run here).

**Follow-ups:**
- *What if I need page 5,000?* OFFSET still pays for the skipped rows; see Q12 and Part 4 Q39.
- *Does `ORDER BY` in a subquery or view guarantee the outer order?* No; only the outer `ORDER BY` does.
- *How do you get the top 10 per group?* A window function; see Part 4.

**Common mistakes:**
- Using `LIMIT` as if it meant "latest" or "first" without an `ORDER BY`.
- Ordering by a non-unique column only, so the result changes between runs and between pages.
- Indexing `(order_date, customer_id)` when the query filters on `customer_id` and sorts by `order_date`: the sort column must come after the equality column.
- Assuming the index helps when there is no `LIMIT` and every row must be returned.

### Q12 ⭐⭐⭐ 🟡 Pagination: OFFSET versus keyset. feed(post_id INTEGER PRIMARY KEY, created_at TEXT, user_id, title) with 200,000 rows and an index on (created_at, post_id). Show page 1, page 5,000 and page 9,000 with LIMIT 20 OFFSET n and with a keyset WHERE (created_at, post_id) < (?, ?) ORDER BY created_at DESC, post_id DESC LIMIT 20; print plans and VM steps for each (OFFSET steps grow with the page number, keyset steps stay flat), assert both return the same page, and show what goes wrong with keyset when the sort key is not unique (rows skipped or repeated) and the tie-break column fix. State the trade-offs (no jump to page N, no total count, stable under inserts) and when OFFSET is acceptable. Cross-reference Part 4 Q39 (top N and pagination with ROW_NUMBER).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** OFFSET makes the engine read and throw away every skipped row, so page N costs about N times page 1; keyset (seek) pagination remembers the last row's sort key and starts from there, so every page costs about the same, but you must sort by a unique key and you cannot jump to page N.

**Schema and sample data:** 200,000 posts, `created_at` taking about 20,000 distinct values (so it repeats about 10 times each). Hand-checkable slice:
```sql
CREATE TABLE feed(post_id INTEGER PRIMARY KEY, created_at TEXT, user_id INT, title TEXT);
INSERT INTO feed VALUES (1,'10:00',1,'a'),(2,'10:00',2,'b'),(3,'10:00',3,'c'),(4,'09:00',1,'d'),(5,'09:00',2,'e');
CREATE INDEX ix_feed ON feed(created_at, post_id);
```

**SQL answer:** the two queries are printed once in the Code block as `OFF` and `KEY`:
```sql
-- OFF
SELECT post_id, created_at FROM feed ORDER BY created_at DESC, post_id DESC LIMIT 20 OFFSET ?
-- KEY
SELECT post_id, created_at FROM feed WHERE (created_at, post_id) < (?, ?) ORDER BY created_at DESC, post_id DESC LIMIT 20
```
The row-value comparison `(a, b) < (?, ?)` is standard SQL and SQLite supports it (from memory: added in 3.15, not checked here).

**pandas answer:** `ordered = df.sort_values(["created_at", "post_id"], ascending=False)`, then page n is `ordered.iloc[off:off+20]`. pandas always has the whole frame in memory, so slicing is cheap; the pandas frame is the oracle for the page contents and for the "which rows were missed" counts.

**Example:** slice sorted `created_at DESC, post_id DESC`: 3, 2, 1 (all 10:00), then 5, 4. Page size 2: page 1 is posts 3, 2; the cursor is (10:00, 2). Keyset with both columns `(created_at, post_id) < ('10:00', 2)` returns post 1 then 5, correct. Keyset on `created_at` alone, `created_at < '10:00'`, skips post 1 (same timestamp as the cursor) and returns 5, 4: post 1 never appears. Using `<=` instead returns posts 3, 2 again. In the real data: page 1 last row was (20641, '2024-03-10 10:30'), twelve posts share that timestamp, and the true page 2 lost 2 rows with `<` and 10 rows with `<=`.

**Code:** run with `python3 -I`; each page is compared to the pandas page exactly (ordered).
```python
# Q12
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

rng = random.Random(31)
N = 200000
base = pd.Timestamp("2024-01-01")
# 20,000 distinct timestamps, about 10 posts each, so created_at is NOT unique
stamps = [(base + pd.Timedelta(minutes=5 * rng.randint(0, 19999))).strftime("%Y-%m-%d %H:%M") for _ in range(N)]
feed_rows = [(i, stamps[i - 1], rng.randint(1, 5000), "post %d" % i) for i in range(1, N + 1)]
path = WORK + "/feed.db"
c = sqlite3.connect(path)
c.execute("CREATE TABLE feed(post_id INTEGER PRIMARY KEY, created_at TEXT, user_id INT, title TEXT)")
c.executemany("INSERT INTO feed VALUES(?,?,?,?)", feed_rows)
c.execute("CREATE INDEX ix_feed ON feed(created_at, post_id)")
c.commit(); c.close()
df = pd.DataFrame(feed_rows, columns=["post_id", "created_at", "user_id", "title"])
ordered = df.sort_values(["created_at", "post_id"], ascending=False).reset_index(drop=True)
print("distinct created_at:", df.created_at.nunique(), "of", N, "rows")

OFF = "SELECT post_id, created_at FROM feed ORDER BY created_at DESC, post_id DESC LIMIT 20 OFFSET ?"
KEY = ("SELECT post_id, created_at FROM feed WHERE (created_at, post_id) < (?, ?) "
       "ORDER BY created_at DESC, post_id DESC LIMIT 20")
print(f"{'page':>5} {'OFFSET steps':>13} {'keyset steps':>13}")
for page in (1, 5000, 9000):
    off = (page - 1) * 20
    so, ro = steps(path, OFF, (off,))
    if page == 1:
        sk, rk = steps(path, "SELECT post_id, created_at FROM feed ORDER BY created_at DESC, post_id DESC LIMIT 20")
    else:                                   # cursor = last row of the previous page
        last = ordered.iloc[off - 1]
        sk, rk = steps(path, KEY, (last.created_at, int(last.post_id)))
    assert ro == rk == list(zip(ordered.post_id[off:off + 20], ordered.created_at[off:off + 20]))
    print(f"{page:>5} {so:>13,} {sk:>13,}")
last = ordered.iloc[5000 * 20 - 21]
print("OFFSET plan:", plan(path, OFF, (99980,)))
print("keyset plan:", plan(path, KEY, (last.created_at, int(last.post_id))))

print("--- keyset with a NON-unique key only (created_at) ---")
def walk(sql_first, sql_next, key_of):
    seen, cur, pages = [], None, 0
    while True:
        rows = sqlite3.connect(path).execute(sql_first if cur is None else sql_next, () if cur is None else (cur,)).fetchall()
        if not rows: break
        seen += [r[0] for r in rows]; cur = key_of(rows[-1]); pages += 1
        if pages > 20000: break
    return seen, pages
seen, pages = walk("SELECT post_id, created_at FROM feed ORDER BY created_at DESC LIMIT 20",
                   "SELECT post_id, created_at FROM feed WHERE created_at < ? ORDER BY created_at DESC LIMIT 20", lambda r: r[1])
print(f"created_at < ?  : fetched {len(seen):,} rows in {pages:,} pages, {N - len(set(seen)):,} rows never returned")
# one page boundary with ties
page1 = sqlite3.connect(path).execute("SELECT post_id, created_at FROM feed ORDER BY created_at DESC, post_id DESC LIMIT 20").fetchall()
seen2 = [r[0] for r in page1]
nxt_lt = sqlite3.connect(path).execute("SELECT post_id FROM feed WHERE created_at < ? ORDER BY created_at DESC, post_id DESC LIMIT 20", (page1[-1][1],)).fetchall()
nxt_le = sqlite3.connect(path).execute("SELECT post_id FROM feed WHERE created_at <= ? ORDER BY created_at DESC, post_id DESC LIMIT 20", (page1[-1][1],)).fetchall()
nxt_ok = sqlite3.connect(path).execute(KEY, (page1[-1][1], page1[-1][0])).fetchall()
print("page 1 last row:", page1[-1], "| ties with that timestamp in the table:", int((df.created_at == page1[-1][1]).sum()))
true2 = set(ordered.post_id[20:40])
print("page 2 via '<'  : repeats", len(set(seen2) & {r[0] for r in nxt_lt}), "| true page-2 rows missing:", len(true2 - {r[0] for r in nxt_lt}))
print("page 2 via '<=' : repeats", len(set(seen2) & {r[0] for r in nxt_le}), "| true page-2 rows missing:", len(true2 - {r[0] for r in nxt_le}))
assert [r[0] for r in nxt_ok] == list(ordered.post_id[20:40])

print("--- stable under inserts ---")
c = sqlite3.connect(path)
before = c.execute(OFF, (20,)).fetchall()
c.executemany("INSERT INTO feed VALUES(?,?,?,?)", [(N + k, "2025-01-01 00:%02d" % k, 1, "new %d" % k) for k in range(1, 6)])
c.commit()
after = c.execute(OFF, (20,)).fetchall()
print("OFFSET 20 page 2: rows shifted by 5 new posts; overlap with the old page 2:", len({r[0] for r in before} & {r[0] for r in after}), "of 20")
cursor = (page1[-1][1], page1[-1][0])
print("keyset page 2 after the inserts equals the old page 2:", [r[0] for r in c.execute(KEY, cursor).fetchall()] == [r[0] for r in before])
c.close()
```

**Output (my run):**
```text
distinct created_at: 19999 of 200000 rows
 page  OFFSET steps  keyset steps
    1           151           128
 5000       200,111           255
 9000       360,111           405
OFFSET plan: ['SCAN feed USING COVERING INDEX ix_feed']
keyset plan: ['SEARCH feed USING COVERING INDEX ix_feed (created_at<?)']
--- keyset with a NON-unique key only (created_at) ---
created_at < ?  : fetched 160,876 rows in 8,044 pages, 39,124 rows never returned
page 1 last row: (20641, '2024-03-10 10:30') | ties with that timestamp in the table: 12
page 2 via '<'  : repeats 0 | true page-2 rows missing: 2
page 2 via '<=' : repeats 10 | true page-2 rows missing: 10
--- stable under inserts ---
OFFSET 20 page 2: rows shifted by 5 new posts; overlap with the old page 2: 15 of 20
keyset page 2 after the inserts equals the old page 2: True
```

**Edge cases:**
- **The step counts.** Page 1: 151 steps (OFFSET) against 128 (keyset); page 5,000: 200,111 against 255; page 9,000: 360,111 against 405. OFFSET grows roughly linearly with the page number (about 20 steps per skipped row here, a covering index scan); keyset stays flat. These are VM steps; they do not include disk reads.
- **The plans differ in one word.** OFFSET: `SCAN feed USING COVERING INDEX ix_feed` (walks from the end of the index and counts). Keyset: `SEARCH feed USING COVERING INDEX ix_feed (created_at<?)`: only the first column is used as the search key and the row-value comparison is re-checked on the rows read, which is fine because it starts at the cursor.
- **Non-unique key.** Paging with `created_at < ?` alone, walking all pages, fetched 160,876 rows in 8,044 pages and never returned 39,124 posts (every post sharing a timestamp with the last row of a page was skipped when it fell on the page boundary).
- **Inserts between pages.** After 5 new posts arrived at the top, `OFFSET 20` page 2 overlapped the old page 2 in only 15 of 20 rows (the other 5 were rows the user had already seen on page 1); the keyset page 2 equalled the old page 2.
- **Direction.** Row values compare lexicographically with a single direction: `ORDER BY created_at DESC, post_id ASC` cannot use `(a, b) < (?, ?)`; spell the condition out as `created_at < ? OR (created_at = ? AND post_id > ?)`. I did not run that mixed-direction form here.
- **Last page and empty results.** An empty result means you are past the end. OFFSET past the end also returns zero rows (not run here).

**Then explain:**
- **Why OFFSET is slow:** the engine must produce the skipped rows in order before discarding them; an index only makes producing them cheaper, not free.
- **Why keyset is flat:** the seek lands directly at the cursor in the index; cost depends on the page size.
- **Trade-offs:** no "jump to page 4,712" (you only have next/previous), no cheap total count, and the sort key must be unique (add the primary key as a tie-break) and indexed in the same order. The benefit is stable pages under inserts and deletes.
- **When OFFSET is fine:** small tables, admin screens with few pages, or when users genuinely need page numbers and the number of pages is capped.
- **Dialects (not executed here):** PostgreSQL and MySQL 8 also support row-value comparisons; SQL Server uses `OFFSET ... FETCH NEXT` and has no row-value comparison, so write the OR form.
- Cross-reference: Part 4 Q39 shows pagination with ROW_NUMBER; this question is about the cost of that approach.

**Follow-ups:**
- *How do you build "previous page"?* Reverse the comparison and the order, fetch, then reverse the page in the application.
- *What about a user-chosen sort column?* One index per supported sort, each with the primary key as a tie-break.
- *Can you show a total count?* Only with a separate `COUNT(*)`, which is itself a scan; many products show "10,000+" instead.

**Common mistakes:**
- Keyset on a non-unique column without a tie-break (rows skipped or repeated).
- Comparing the cursor with `<=` and returning the last row twice.
- Mixing ASC and DESC in the ORDER BY but using a single row-value comparison.
- Forgetting that the query must match the index order, or the planner sorts all candidate rows.

### Q13 ⭐⭐⭐ 🟡 SELECT * versus needed columns, and covering indexes: orders(order_id, customer_id, order_date, status, amount, notes TEXT of about 300 characters) with 100,000 rows. Compare SELECT * and SELECT customer_id, order_date, amount WHERE customer_id = ? with an index on (customer_id), then on (customer_id, order_date, amount): print plans (USING INDEX versus USING COVERING INDEX), VM steps and the index size from page counts. Explain what covering means, why it can avoid the table lookup entirely, the cost (a wider index, slower writes, more pages to cache), why SELECT * defeats it (and breaks when columns are added), and the INCLUDE / included-columns syntax in PostgreSQL and SQL Server and the clustered-index behaviour in MySQL InnoDB (secondary indexes carry the primary key), all hedged and not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** A covering index contains every column the query reads, so the engine answers from the index alone and never touches the wide table row; `SELECT *` cannot be covered unless the index holds every column, and it also changes meaning when someone adds a column.

**Schema and sample data:** 100,000 rows, `notes` about 300 characters (average 299.9 in my run). Slice:
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL, notes TEXT);
INSERT INTO orders VALUES (1,5,'2024-03-01','placed',30.0,'long text...'),(2,5,'2024-03-09','shipped',10.0,'long text...'),(3,6,'2024-03-05','placed',10.0,'long text...');
CREATE INDEX ix_cust ON orders(customer_id);
CREATE INDEX ix_cov ON orders(customer_id, order_date, amount);
```

**SQL answer:** two queries on `customer_id BETWEEN 1 AND 500` (about 5,000 rows) and `customer_id = 7`: `SELECT *` and `SELECT customer_id, order_date, amount, order_id`. The SQL is printed once in the Code block (`SEL_STAR`, `SEL_COLS`); index sizes come from the `dbstat` virtual table (compiled into this SQLite build) and `PRAGMA page_count`.

**pandas answer:** the analogue is reading only the columns you need: `pd.read_csv(csv, usecols=[...])` against the full read, compared with `memory_usage(deep=True)`; the column subset is asserted equal to `full[[...]]`.

**Example:** customer 5 in the slice has orders 1 and 2. With `ix_cust` alone the engine finds the two index entries (customer 5, rowid 1 and 2), then goes to the table b-tree twice to fetch `order_date` and `amount` (and the 300-character notes if you asked for `*`). With `ix_cov` the index entries themselves hold `(5, '2024-03-01', 30.0)` and `(5, '2024-03-09', 10.0)` plus the rowid, so the answer is read straight from the index. The plan wording changes from `USING INDEX` to `USING COVERING INDEX`.

**Code:** run with `python3 -I`; row sets are compared after sorting.
```python
# Q13
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

rng = random.Random(41)
words = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet"]
def note():
    s = " ".join(rng.choice(words) for _ in range(50))
    return s[:300]
N = 100000
rows = [(i, rng.randint(1, 10000), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
         rng.choice(["placed", "shipped", "delivered"]), round(rng.uniform(5, 500), 2), note()) for i in range(1, N + 1)]
path = WORK + "/o.db"
c = sqlite3.connect(path)
c.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL, notes TEXT)")
c.executemany("INSERT INTO orders VALUES(?,?,?,?,?,?)", rows)
c.execute("CREATE INDEX ix_cust ON orders(customer_id)")
c.commit(); c.close()
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date", "status", "amount", "notes"])
print("average notes length:", round(df.notes.str.len().mean(), 1))

def sizes(label):
    c = sqlite3.connect(path)
    pc = c.execute("PRAGMA page_count").fetchone()[0]
    ds = c.execute("SELECT name, COUNT(*) pages, SUM(pgsize) FROM dbstat GROUP BY name ORDER BY name").fetchall()
    c.close()
    print(f"{label}: page_count={pc} ->", ", ".join(f"{n}: {p} pages ({b:,} bytes)" for n, p, b in ds))

def run(label, sql, params=()):
    st, res = steps(path, sql, params)
    print(f"{label}\n   plan : {' | '.join(plan(path, sql, params))}\n   steps: {st:,}   rows: {len(res):,}")
    return res

SEL_STAR = "SELECT * FROM orders WHERE customer_id BETWEEN 1 AND 500"
SEL_COLS = "SELECT customer_id, order_date, amount, order_id FROM orders WHERE customer_id BETWEEN 1 AND 500"
sizes("with ix_cust only")
a1 = run("SELECT * with ix_cust(customer_id)", SEL_STAR)
b1 = run("3 columns with ix_cust(customer_id): still needs the table row for order_date and amount", SEL_COLS)
c = sqlite3.connect(path); c.execute("CREATE INDEX ix_cov ON orders(customer_id, order_date, amount)"); c.commit(); c.close()
sizes("after ix_cov")
a2 = run("SELECT * with both indexes", SEL_STAR)
b2 = run("3 columns with ix_cov(customer_id, order_date, amount)", SEL_COLS)
sub = df[df.customer_id.between(1, 500)]
assert sorted(b1) == sorted(b2) == sorted(zip(sub.customer_id, sub.order_date, sub.amount, sub.order_id))
assert len(a1) == len(a2) == len(sub)
one = run("one customer, 3 columns, covering", "SELECT order_date, amount FROM orders WHERE customer_id = 7")
run("one customer, SELECT *", "SELECT * FROM orders WHERE customer_id = 7")
c = sqlite3.connect(path); c.execute("DROP INDEX ix_cov"); c.commit(); c.close()
run("one customer, 3 columns, no covering index", "SELECT order_date, amount FROM orders WHERE customer_id = 7")

print("--- SELECT * is not stable when the schema changes ---")
c = sqlite3.connect(path)
cols_before = [d[0] for d in c.execute("SELECT * FROM orders LIMIT 1").description]
c.execute("ALTER TABLE orders ADD COLUMN coupon TEXT"); c.commit()
cols_after = [d[0] for d in c.execute("SELECT * FROM orders LIMIT 1").description]
print("columns before:", cols_before); print("columns after :", cols_after)
c.close()

print("--- pandas: only read the columns you need ---")
csv = WORK + "/orders.csv"
df.to_csv(csv, index=False)
full = pd.read_csv(csv)
slim = pd.read_csv(csv, usecols=["customer_id", "order_date", "amount"])
print("memory_usage(deep=True) bytes: all columns", int(full.memory_usage(deep=True).sum()), "| usecols", int(slim.memory_usage(deep=True).sum()))
print("notes column alone:", int(full.notes.memory_usage(deep=True)))
assert slim.equals(full[["customer_id", "order_date", "amount"]])
```

**Output (my run):**
```text
average notes length: 299.9
with ix_cust only: page_count=9359 -> ix_cust: 262 pages (1,073,152 bytes), orders: 9096 pages (37,257,216 bytes), sqlite_schema: 1 pages (4,096 bytes)
SELECT * with ix_cust(customer_id)
   plan : SEARCH orders USING INDEX ix_cust (customer_id>? AND customer_id<?)
   steps: 55,549   rows: 5,047
3 columns with ix_cust(customer_id): still needs the table row for order_date and amount
   plan : SEARCH orders USING INDEX ix_cust (customer_id>? AND customer_id<?)
   steps: 45,455   rows: 5,047
after ix_cov: page_count=10113 -> ix_cov: 754 pages (3,088,384 bytes), ix_cust: 262 pages (1,073,152 bytes), orders: 9096 pages (37,257,216 bytes), sqlite_schema: 1 pages (4,096 bytes)
SELECT * with both indexes
   plan : SEARCH orders USING INDEX ix_cust (customer_id>? AND customer_id<?)
   steps: 55,556   rows: 5,047
3 columns with ix_cov(customer_id, order_date, amount)
   plan : SEARCH orders USING COVERING INDEX ix_cov (customer_id>? AND customer_id<?)
   steps: 40,415   rows: 5,047
one customer, 3 columns, covering
   plan : SEARCH orders USING COVERING INDEX ix_cov (customer_id=?)
   steps: 85   rows: 8
one customer, SELECT *
   plan : SEARCH orders USING INDEX ix_cust (customer_id=?)
   steps: 125   rows: 8
one customer, 3 columns, no covering index
   plan : SEARCH orders USING INDEX ix_cust (customer_id=?)
   steps: 86   rows: 8
--- SELECT * is not stable when the schema changes ---
columns before: ['order_id', 'customer_id', 'order_date', 'status', 'amount', 'notes']
columns after : ['order_id', 'customer_id', 'order_date', 'status', 'amount', 'notes', 'coupon']
--- pandas: only read the columns you need ---
memory_usage(deep=True) bytes: all columns 48827385 | usecols 7500132
notes column alone: 34894798
```

**Edge cases:**
- **VM steps barely move.** For the 5,047-row range, `SELECT *` took 55,556 steps, three columns with only `ix_cust` 45,455 and with the covering index 40,415. For one customer (8 rows) it was 125 against 85. The step counter counts virtual-machine instructions, not page reads, so it understates the saving: the table is 9,096 pages (37 MB) and the covering index 754 pages (3 MB, dbstat), and a covering plan can avoid the 9,096-page table entirely. I did not measure page reads or cold-cache time, so I do not put a number on the I/O saving.
- **Cost of covering.** `ix_cov` added 754 pages (3,088,384 bytes) next to `ix_cust` (262 pages) and every insert, delete or update of `amount`/`order_date` must now maintain it too (see Q16 for the insert cost).
- **`SELECT *` is not covered even with `ix_cov`:** the plan stayed `USING INDEX ix_cust` and the covering index was ignored for it.
- **`SELECT *` is unstable:** after `ALTER TABLE ... ADD COLUMN coupon`, `SELECT *` returned 7 columns instead of 6 (printed). Code that maps columns by position breaks.
- **The primary key is free:** in a rowid table every index entry carries the rowid, so `order_id` can be selected from any index without adding it (my 3-column query selected `order_id` and was still covering).
- **Without the covering index** the same three-column query for one customer used `USING INDEX ix_cust` (86 steps), i.e. SQLite looked up each row in the table.

**Then explain:**
- **Covering:** all columns the query touches (select list, WHERE, ORDER BY) are in the index.
- **Column order still matters:** `(customer_id, order_date, amount)` is covering for this query and also gives the leftmost-prefix lookups on `customer_id`; the trailing columns are payload, not search keys here.
- **Wide rows:** a 300-character column in `SELECT *` multiplies the bytes returned and cached even when you do not use them.
- **Other engines (hedged, not executed here):** PostgreSQL and SQL Server let you add non-key columns with `INCLUDE (...)` so the index stays small to search but covers the query; PostgreSQL reports `Index Only Scan` (and may still visit the heap if the visibility map is not up to date); MySQL InnoDB stores the table clustered on the primary key and every secondary index entry carries the primary key, so a secondary index already covers queries that only need the key; its `EXPLAIN` shows `Using index` in Extra.
- **pandas:** with `usecols`, my run held 7,500,132 bytes against 48,827,385 for all columns (deep memory), 34,894,798 of them for `notes` alone.

**Follow-ups:**
- *Why not cover everything?* Wider indexes cost writes and cache; cover the hottest queries only.
- *Does `COUNT(*)` use the narrowest index?* In SQLite the plan scans the smallest covering index (Wave A observed this; not re-run in this block).
- *How do you detect missing coverage?* In the plan: `USING INDEX` (with lookup) versus `USING COVERING INDEX`.

**Common mistakes:**
- `SELECT *` in application queries and views.
- Adding a covering index and then selecting one more column, which silently removes the coverage.
- Expecting the same plan wording across engines.
- Judging by row counts instead of pages and bytes read.

### Q14 ⭐⭐⭐ 🟡 pandas performance basics: a seeded DataFrame of 200,000 rows (int column a, float column b, string column s with four values). Compute a*b with a vectorised expression, df.apply(axis=1), a list comprehension over iterrows and over itertuples, and Series.map; time each with time.perf_counter (label timings machine-specific and report only the order of magnitude and ranking), assert all give the same values, and explain why iterrows builds a Series per row and loses dtypes, why apply(axis=1) is a Python loop in disguise, when vectorising is impossible (use itertuples, numpy.where/select, np.vectorize caveats, or push to SQL). Also compare s.str.upper() with s.map(str.upper) and say when .str methods are not faster than a plain loop. Mention the pandas guide's advice to vectorise first and its 100,000-row rule of thumb for eval(); do not quote its benchmark numbers as yours.
**Asked at:** pandas user guide pages 'Enhancing performance' and 'Scaling to large datasets' (opened); official documentation, not candidate reports; data scientist and analytics engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Vectorise first (one operation on whole columns in compiled code); `apply(axis=1)` and `iterrows` run a Python function once per row, so they are orders of magnitude slower on 200,000 rows, and when a formula really cannot be vectorised, use `np.where`/`np.select`, `itertuples` or `zip`, or push the work to SQL.

**Schema and sample data:** a seeded frame `rng = np.random.default_rng(14)` with 200,000 rows: `a` int64 (1 to 99), `b` float64 (0 to 10, 3 decimals), `s` one of four colours. A hand-checkable slice:
```sql
CREATE TABLE t(a INT, b REAL, s TEXT);
INSERT INTO t VALUES (2, 1.5, 'red'), (3, 2.0, 'blue'), (4, 0.5, 'red');
```

**SQL answer:** `SELECT a * b AS ab FROM t` computes the same column inside the engine (the Code block loads the 200,000 rows with `to_sql` and asserts equality with the pandas result, row for row, in table order). That is the answer to "push it to SQL" when the data already lives in a database.

**pandas answer:** the seven forms in the Code block: `df.a * df.b` (vectorised), the same on `.to_numpy()` arrays, `[x * y for x, y in zip(df.a, df.b)]`, a list over `itertuples`, `Series.map(lambda)`, `df.apply(lambda r: r["a"] * r["b"], axis=1)` and a list over `iterrows`. All are asserted equal to the vectorised result with `np.allclose`.

**Example:** slice rows (2, 1.5), (3, 2.0), (4, 0.5): `a*b` = 3.0, 6.0, 2.0. The vectorised form multiplies two arrays in one call. `apply(axis=1)` builds a small Series for each of the three rows, calls your lambda, and collects three results; on 200,000 rows that is 200,000 Series constructions plus 200,000 Python calls.

**Code:** run with `python3 -I`. The timings are machine-specific and noisy; I report them for ranking only.
```python
# Q14
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

import time
rng = np.random.default_rng(14)
N = 200000
df = pd.DataFrame({"a": rng.integers(1, 100, N), "b": rng.uniform(0, 10, N).round(3),
                   "s": rng.choice(["red", "green", "blue", "amber"], N)})
print(df.dtypes.to_dict())

def timed(fn, repeat=3):
    best = None
    for _ in range(repeat):
        t0 = time.perf_counter(); out = fn(); dt = time.perf_counter() - t0
        best = dt if best is None or dt < best else best
    return out, best * 1000

vec, t_vec = timed(lambda: df.a * df.b)
app, t_app = timed(lambda: df.apply(lambda r: r["a"] * r["b"], axis=1), repeat=1)
itr, t_itr = timed(lambda: [r["a"] * r["b"] for _, r in df.iterrows()], repeat=1)
tup, t_tup = timed(lambda: [t.a * t.b for t in df.itertuples(index=False)])
zp, t_zip = timed(lambda: [x * y for x, y in zip(df.a, df.b)])
mp, t_map = timed(lambda: df.a.map(lambda x: x * 2.5))
arr, t_np = timed(lambda: df.a.to_numpy() * df.b.to_numpy())
for name, out in [("apply", app), ("iterrows", itr), ("itertuples", tup), ("zip", zp)]:
    assert np.allclose(np.asarray(out, dtype=float), vec.to_numpy()), name
assert np.allclose(arr, vec.to_numpy())
assert np.allclose(mp.to_numpy(), df.a.to_numpy() * 2.5)
print("machine-specific timings in ms (best of 3 where cheap, one run for apply and iterrows):")
for k, v in sorted({"vectorised a*b": t_vec, "numpy arrays": t_np, "zip loop": t_zip, "itertuples": t_tup,
                    "Series.map(lambda)": t_map, "apply(axis=1)": t_app, "iterrows": t_itr}.items(), key=lambda kv: kv[1]):
    print(f"   {k:<20}{v:>10.1f}")
print("ratios vs vectorised: apply x%.0f, iterrows x%.0f, itertuples x%.0f" % (t_app / t_vec, t_itr / t_vec, t_tup / t_vec))

print("--- iterrows builds a Series per row and upcasts ---")
small = pd.DataFrame({"i": [1, 2], "x": [0.5, 1.5], "t": ["u", "v"]})
for idx, row in small.iterrows():
    print("   row dtype:", row.dtype, "| row['i'] =", repr(row["i"]), type(row["i"]).__name__)
    break
print("   itertuples keeps types:", [type(v).__name__ for v in next(small.itertuples(index=False))])
numeric = pd.DataFrame({"i": [1, 2], "x": [0.5, 1.5]})
print("   numeric-only iterrows: row dtype", next(numeric.iterrows())[1].dtype, "(int 1 became float)")

print("--- when you cannot vectorise a formula, push the branching into numpy ---")
cond = [df.a < 20, df.a < 60]
sel, t_sel = timed(lambda: np.select(cond, [df.b * 1.0, df.b * 1.5], default=df.b * 2.0))
def tiered(a, b):
    return b if a < 20 else (b * 1.5 if a < 60 else b * 2.0)
lp, t_lp = timed(lambda: [tiered(a, b) for a, b in zip(df.a, df.b)])
vz, t_vz = timed(lambda: np.vectorize(tiered)(df.a, df.b), repeat=1)
assert np.allclose(sel, lp) and np.allclose(sel, vz)
print(f"   np.select {t_sel:.1f} ms | python loop {t_lp:.1f} ms | np.vectorize {t_vz:.1f} ms (np.vectorize is a loop, not speed)")

print("--- strings: .str.upper vs map(str.upper) vs apply ---")
u1, t1 = timed(lambda: df.s.str.upper())
u2, t2 = timed(lambda: df.s.map(str.upper))
u3, t3 = timed(lambda: df.s.apply(lambda v: v.upper()))
cat = df.s.astype("category")
u4, t4 = timed(lambda: cat.cat.rename_categories(str.upper))
assert u1.tolist() == u2.tolist() == u3.tolist() == u4.astype(str).tolist()
print(f"   .str.upper {t1:.1f} | map(str.upper) {t2:.1f} | apply(lambda) {t3:.1f} | category rename {t4:.1f}  (ms)")

print("--- SQL pushes the same arithmetic into the engine ---")
c = sqlite3.connect(":memory:")
df.to_sql("t", c, index=False)
sq = pd.read_sql("SELECT a * b AS ab FROM t", c).ab
assert np.allclose(sq.to_numpy(), vec.to_numpy())
print("SQL a*b equals pandas a*b for all", N, "rows")

print("--- eval/query ---")
m, tm = timed(lambda: df[(df.a > 50) & (df.b < 5)])
q, tq = timed(lambda: df.query("a > 50 and b < 5"))
assert m.equals(q)
print(f"   mask {tm:.1f} ms | query {tq:.1f} ms (200,000 rows, machine-specific)")
```

**Output (my run, one run on this machine):**
```text
{'a': dtype('int64'), 'b': dtype('float64'), 's': <StringDtype(storage='python', na_value=nan)>}
machine-specific timings in ms (best of 3 where cheap, one run for apply and iterrows):
   vectorised a*b             0.6
   numpy arrays               0.8
   zip loop                  43.6
   Series.map(lambda)        44.2
   itertuples               168.8
   apply(axis=1)            790.2
   iterrows                4757.6
ratios vs vectorised: apply x1283, iterrows x7725, itertuples x274
--- iterrows builds a Series per row and upcasts ---
   row dtype: object | row['i'] = 1 int
   itertuples keeps types: ['int', 'float', 'str']
   numeric-only iterrows: row dtype float64 (int 1 became float)
--- when you cannot vectorise a formula, push the branching into numpy ---
   np.select 3.2 ms | python loop 31.4 ms | np.vectorize 90.1 ms (np.vectorize is a loop, not speed)
--- strings: .str.upper vs map(str.upper) vs apply ---
   .str.upper 36.7 | map(str.upper) 22.3 | apply(lambda) 27.5 | category rename 0.2  (ms)
--- SQL pushes the same arithmetic into the engine ---
SQL a*b equals pandas a*b for all 200000 rows
--- eval/query ---
   mask 3.1 ms | query 6.0 ms (200,000 rows, machine-specific)
```

**Edge cases:**
- **Ranking, not numbers.** On this machine the order was: numpy arrays and the vectorised expression (under 1 ms), then `zip` loop and `Series.map` (tens of ms), `itertuples` (about 100 ms or more), `apply(axis=1)` (hundreds of ms to about 1 s) and `iterrows` (several seconds). Across three runs while I built this answer the milliseconds moved by up to a factor of 2 (for example `apply` 790 to 1,075 ms, `np.vectorize` 45 to 90 ms), but the groups kept their order (vectorised, then loops over arrays, then `itertuples`, then `apply`, then `iterrows`). The gap between vectorised and `apply` was three orders of magnitude.
- **`zip` beat `itertuples`.** Iterating plain columns with `zip` was faster than `itertuples` in every run; both beat `apply(axis=1)` and `iterrows` by a wide margin. If a loop is unavoidable, loop over arrays or tuples, never over row Series.
- **`iterrows` loses dtypes.** Each row is a Series, so a mixed row becomes `object` (int stays a Python int but the Series dtype is object) and a numeric row upcasts: in my run an int column was returned as `float64` in the numeric-only frame. `itertuples` kept `int`, `float`, `str`.
- **`np.vectorize` is not speed.** For a three-way tiered formula `np.select` took 3.2 ms, a Python loop 31.4 ms and `np.vectorize` 90.1 ms in the printed run (an earlier run had the loop and `vectorize` about equal); I recall the NumPy docs calling `vectorize` a convenience wrapper that is essentially a for loop (from memory); the measurement agrees.
- **`.str` is not automatically faster.** `.str.upper()` 36.7 ms, `map(str.upper)` 22.3 ms, `apply(lambda)` 27.5 ms on 200,000 short strings (the three were within a factor of 1.7 of each other in every run, and `.str` was never clearly ahead): all of them run Python string code per element in these pandas 3 default string columns. Converting to `category` and renaming the four categories took 0.2 ms, because the work is done on four labels, not 200,000 rows.
- **`query()` versus a mask.** At 200,000 rows the printed run had a mask at 3.1 ms and `query()` at 6.0 ms (earlier runs: 2.4 and 4.1 ms). The pandas guide says `eval()`/`query()` pays off for large frames (it quotes a rule of thumb around 100,000 rows); at this size I measured no win, so I do not claim one.

**Then explain:**
- **Why vectorised is fast:** one Python-level call, then C loops over contiguous memory with no per-element Python objects.
- **Why `apply(axis=1)` is a loop in disguise:** it iterates rows and calls your function each time; only `apply` on a column with a NumPy ufunc-style function or on groups with a built-in is cheap.
- **When vectorising is impossible:** row-dependent control flow (use `np.where`/`np.select`, or `map` on a small lookup), stateful or recursive formulas (use `itertuples`/`zip`, or a numeric library), external calls (batch them), or push the logic into SQL/the database.
- **The pandas guide's advice:** vectorise first, use `eval`/`query` for big frames and consider Cython or Numba only for hot loops (I did not use Numba here; I do not quote the guide's benchmark numbers).
- **Memory vs time:** `category` and downcasting help memory too (see Wave A's `memory_usage` checks in the sources note; Q13 shows `usecols`).

**Follow-ups:**
- *What would you do for a custom rule per row?* Express it as `np.select` conditions; if impossible, `zip` over columns.
- *Is `apply` ever fine?* On small frames, on groupby results, or when readability matters more than speed.
- *How do you time reliably?* Repeat and take the minimum or median, on the same machine, with warm caches; seed the data.

**Common mistakes:**
- `df.apply(f, axis=1)` for arithmetic that is a single expression.
- Modifying the frame inside an `iterrows` loop and expecting the frame to change.
- Reporting one timing as a fact; the ranking is the portable claim.
- Assuming `.str` methods or `np.vectorize` are vectorised.

### Q15 ⭐⭐ 🟡 Join keys, join order and automatic indexes: customers(customer_id INTEGER PRIMARY KEY, name, city) 20,000 rows, orders(order_id, customer_id, order_date, status, amount) 200,000 rows, order_items(item_id, order_id, product_id, qty) 600,000 rows. For the three-table join filtered on customers.city = 'Pune', print the plan with no foreign-key indexes, then with PRAGMA automatic_index = OFF, then with indexes on orders(customer_id) and order_items(order_id), and after ANALYZE. Note which table becomes the outer loop each time, when SQLite builds an automatic index or a BLOOM FILTER, count VM steps, and show how a CROSS JOIN fixes the join order. Explain nested-loop joins with an inner index lookup (SQLite's only join method) versus hash and merge joins in PostgreSQL, MySQL 8 and SQL Server (described, not executed), and why a missing foreign-key index is the usual cause of a join that slows as tables grow. Cross-reference Part 2 Q17 (multiple joins and join order).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; PostgreSQL docs using-explain and indexes-multicolumn and MySQL EXPLAIN output page (opened, used for contrast only); official documentation, not candidate reports; product company and GCC data engineer rounds
**Say this first (1 line):** SQLite joins with nested loops: for each row of the outer table it looks up the inner table, so the join is fast only when the inner side has an index on the join column; a missing foreign-key index is the usual reason a join gets slower as tables grow.

**Schema and sample data:** customers 20,000, orders 200,000, order_items 600,000, all seeded (generator in the Code block). Slice:
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INT, product_id INT, qty INT);
INSERT INTO customers VALUES (1,'a','Pune'),(2,'b','Delhi');
INSERT INTO orders VALUES (10,1,'2024-03-01','placed',5.0),(11,2,'2024-03-02','placed',6.0);
INSERT INTO order_items VALUES (100,10,7,2),(101,10,8,1),(102,11,7,4);
```

**SQL answer:** one query, printed once in the Code block as `Q` (and the CROSS JOIN variant `QX`):
```sql
SELECT COUNT(*), SUM(i.qty) FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items i ON i.order_id = o.order_id
WHERE c.city = 'Pune'
```

**pandas answer:** `C[C.city == "Pune"].merge(O, on="customer_id").merge(I, on="order_id")`, then `(len(m), m.qty.sum())`; every SQL variant is asserted to return the same pair.

**Example:** in the slice, Pune customer 1 has order 10, which has items 100 and 101: the count is 2 and the quantity sum is 3. A nested loop does this as: for each Pune customer, find its orders (needs an index on `orders(customer_id)`, else scan all orders), and for each order find its items (needs `order_items(order_id)`). In the real data, 59,861 item rows belong to Pune customers (sum of qty 179,764).

**Code:** run with `python3 -I`; it needs about half a minute on this machine because the "no index" self-join at the end is deliberately slow.
```python
# Q15
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

rng = random.Random(51)
cities = ["Pune", "Delhi", "Mumbai", "Chennai", "Kolkata", "Jaipur", "Indore", "Surat", "Patna", "Noida"]
cust = [(i, "c%d" % i, rng.choice(cities)) for i in range(1, 20001)]
orders = [(i, rng.randint(1, 20000), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
           rng.choice(["placed", "shipped", "delivered"]), round(rng.uniform(5, 500), 2)) for i in range(1, 200001)]
items = [(i, rng.randint(1, 200000), rng.randint(1, 500), rng.randint(1, 5)) for i in range(1, 600001)]
path = WORK + "/j.db"
c = sqlite3.connect(path)
c.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INT, product_id INT, qty INT);""")
c.executemany("INSERT INTO customers VALUES(?,?,?)", cust)
c.executemany("INSERT INTO orders VALUES(?,?,?,?,?)", orders)
c.executemany("INSERT INTO order_items VALUES(?,?,?,?)", items)
c.commit(); c.close()
C = pd.DataFrame(cust, columns=["customer_id", "name", "city"])
O = pd.DataFrame(orders, columns=["order_id", "customer_id", "order_date", "status", "amount"])
I = pd.DataFrame(items, columns=["item_id", "order_id", "product_id", "qty"])

Q = """SELECT COUNT(*), SUM(i.qty) FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items i ON i.order_id = o.order_id
WHERE c.city = 'Pune'"""
QX = Q.replace("FROM customers c\nJOIN orders o", "FROM customers c CROSS JOIN orders o")
QX_BAD = """SELECT COUNT(*), SUM(i.qty) FROM order_items i CROSS JOIN orders o CROSS JOIN customers c
WHERE o.order_id = i.order_id AND c.customer_id = o.customer_id AND c.city = 'Pune'"""
m = C[C.city == "Pune"].merge(O, on="customer_id").merge(I, on="order_id")
expected = (len(m), int(m.qty.sum()))

def run(label, sql, auto=True):
    cc = sqlite3.connect(path)
    if not auto: cc.execute("PRAGMA automatic_index = OFF")
    pl = [r[3] for r in cc.execute("EXPLAIN QUERY PLAN " + sql)]
    n = [0]
    def tick():
        n[0] += 1; return 0
    cc.set_progress_handler(tick, 1); res = cc.execute(sql).fetchone(); cc.set_progress_handler(None, 0); cc.close()
    print(f"{label}\n   plan : {' | '.join(pl)}\n   steps: {n[0]:,}   result: {res}")
    assert tuple(res) == expected
print("pandas result (rows, sum qty):", expected)
run("1. primary keys only", Q)
run("2. same, PRAGMA automatic_index = OFF", Q, auto=False)
c = sqlite3.connect(path)
c.execute("CREATE INDEX ix_o_cust ON orders(customer_id)"); c.execute("CREATE INDEX ix_i_ord ON order_items(order_id)"); c.commit(); c.close()
run("3. indexes on orders(customer_id), order_items(order_id), NO statistics yet", Q)
run("3b. same indexes, CROSS JOIN customers -> orders pins customers as the outer loop", QX)
c = sqlite3.connect(path); c.execute("ANALYZE"); c.commit(); c.close()
run("4. after ANALYZE", Q)
run("5. after ANALYZE, CROSS JOIN customers -> orders (same plan as 4)", QX)
c = sqlite3.connect(path); c.execute("DROP INDEX ix_o_cust"); c.execute("DROP INDEX ix_i_ord"); c.execute("DELETE FROM sqlite_stat1"); c.commit(); c.close()
run("6. indexes dropped again, stats cleared", Q)
run("7. CROSS JOIN order forced to items -> orders -> customers, no FK indexes", QX_BAD)

print("--- automatic index and BLOOM FILTER: other orders of the same customer (self join, no index on customer_id) ---")
S = """SELECT COUNT(*) FROM orders a JOIN orders b ON b.customer_id = a.customer_id AND b.order_id <> a.order_id WHERE a.order_id <= 100"""
def runs(label, auto):
    cc = sqlite3.connect(path)
    if not auto: cc.execute("PRAGMA automatic_index = OFF")
    pl = [r[3] for r in cc.execute("EXPLAIN QUERY PLAN " + S)]
    n = [0]
    def tick():
        n[0] += 1; return 0
    cc.set_progress_handler(tick, 1); res = cc.execute(S).fetchone()[0]; cc.set_progress_handler(None, 0); cc.close()
    print(f"{label}\n   plan : {' | '.join(pl)}\n   steps: {n[0]:,}   result: {res}")
    return res
a = O[O.order_id <= 100][["order_id", "customer_id"]].merge(O[["order_id", "customer_id"]], on="customer_id", suffixes=("_a", "_b"))
want = int((a.order_id_a != a.order_id_b).sum())
r1 = runs("automatic_index ON", True)
r2 = runs("automatic_index OFF", False)
assert r1 == r2 == want
print("pandas self-merge count:", want)
```

**Output (my run):**
```text
pandas result (rows, sum qty): (59861, 179764)
1. primary keys only
   plan : SCAN i | SEARCH o USING INTEGER PRIMARY KEY (rowid=?) | SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   steps: 4,379,599   result: (59861, 179764)
2. same, PRAGMA automatic_index = OFF
   plan : SCAN i | SEARCH o USING INTEGER PRIMARY KEY (rowid=?) | SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   steps: 4,379,599   result: (59861, 179764)
3. indexes on orders(customer_id), order_items(order_id), NO statistics yet
   plan : SCAN i | SEARCH o USING INTEGER PRIMARY KEY (rowid=?) | SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   steps: 4,379,599   result: (59861, 179764)
3b. same indexes, CROSS JOIN customers -> orders pins customers as the outer loop
   plan : SCAN c | SEARCH o USING COVERING INDEX ix_o_cust (customer_id=?) | SEARCH i USING INDEX ix_i_ord (order_id=?)
   steps: 502,826   result: (59861, 179764)
4. after ANALYZE
   plan : SCAN c | SEARCH o USING COVERING INDEX ix_o_cust (customer_id=?) | SEARCH i USING INDEX ix_i_ord (order_id=?)
   steps: 502,823   result: (59861, 179764)
5. after ANALYZE, CROSS JOIN customers -> orders (same plan as 4)
   plan : SCAN c | SEARCH o USING COVERING INDEX ix_o_cust (customer_id=?) | SEARCH i USING INDEX ix_i_ord (order_id=?)
   steps: 502,826   result: (59861, 179764)
6. indexes dropped again, stats cleared
   plan : SCAN i | SEARCH o USING INTEGER PRIMARY KEY (rowid=?) | SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   steps: 4,379,599   result: (59861, 179764)
7. CROSS JOIN order forced to items -> orders -> customers, no FK indexes
   plan : SCAN i | SEARCH o USING INTEGER PRIMARY KEY (rowid=?) | SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
   steps: 4,379,601   result: (59861, 179764)
--- automatic index and BLOOM FILTER: other orders of the same customer (self join, no index on customer_id) ---
automatic_index ON
   plan : SEARCH a USING INTEGER PRIMARY KEY (rowid<?) | BLOOM FILTER ON b (customer_id=?) | SEARCH b USING AUTOMATIC COVERING INDEX (customer_id=?)
   steps: 1,207,357   result: 973
automatic_index OFF
   plan : SEARCH a USING INTEGER PRIMARY KEY (rowid<?) | SCAN b
   steps: 80,004,607   result: 973
pandas self-merge count: 973
```

**Edge cases:**
- **No foreign-key indexes (cases 1, 2, 6, 7).** The planner did `SCAN i` (all 600,000 items) then `SEARCH o USING INTEGER PRIMARY KEY (rowid=?)` then `SEARCH c USING INTEGER PRIMARY KEY (rowid=?)`: it starts from the biggest table and walks to the parents by primary key, because that is the only index available. 4,379,599 steps. `PRAGMA automatic_index = OFF` made no difference here, because no automatic index was needed (primary-key probes already existed).
- **Indexes created but no statistics (case 3).** The plan was unchanged: still `SCAN i`, 4,379,599 steps. This surprised me: creating `ix_o_cust` and `ix_i_ord` did not change the plan until I either ran `ANALYZE` (case 4) or pinned the order with `CROSS JOIN` (case 3b).
- **After `ANALYZE` (case 4) and with the CROSS JOIN (cases 3b, 5):** `SCAN c` (filter city) then `SEARCH o USING COVERING INDEX ix_o_cust (customer_id=?)` then `SEARCH i USING INDEX ix_i_ord (order_id=?)`: 502,823 steps, about 8.7 times fewer than 4,379,599. The scan of 20,000 customers dominates what is left; an index on `customers(city)` would shrink it further (not run here).
- **CROSS JOIN pins the order.** SQLite does not reorder tables on the two sides of a `CROSS JOIN`, so it is a (non-portable) join-order hint. Case 7 pinned the bad order (items, orders, customers) and got the same plan and steps as the planner's own choice.
- **Automatic index and BLOOM FILTER.** For the self-join "other orders of the same customer" with no index on `orders(customer_id)` (after dropping the indexes), the plan was `SEARCH b USING AUTOMATIC COVERING INDEX (customer_id=?)` with `BLOOM FILTER ON b (customer_id=?)`: SQLite built a temporary index for the query, 1,207,357 steps. With `automatic_index = OFF` it scanned `b` for each outer row: 80,004,607 steps for the same 973 rows, about 66 times more. An automatic index is built for the statement while it runs and thrown away (documented behaviour, not separately checked here), so it is a warning sign, not a solution: create the real index.
- **Fan-out and inner join NULLs:** a customer with no orders or an order with no items drops out of the INNER JOIN; use LEFT JOIN if counts of zero matter (Part 2).

**Then explain:**
- **Nested-loop join with index lookup:** cost is about (outer rows) x (cost of one index probe); the planner picks the outer table to minimise that, using statistics.
- **Why a missing FK index hurts:** without it the inner side is scanned per outer row (cost grows like outer x inner), so doubling both tables quadruples the work; with it, doubling the tables roughly doubles the work.
- **Other engines (described, not executed here):** PostgreSQL has nested-loop, hash and merge joins and chooses by cost; MySQL 8 added hash joins (used when there is no usable index); SQL Server has nested loops, hash and merge joins. SQLite has only the nested loop, plus automatic indexes and bloom filters to make it tolerable.
- **Statistics matter:** the same indexes only changed the plan after `ANALYZE` (Q17), which is why "I added an index and nothing changed" is often a statistics or join-order question.
- Cross-reference: Part 2 Q17 covers join order for correctness and style.

**Follow-ups:**
- *Do primary keys create indexes?* In SQLite an `INTEGER PRIMARY KEY` is the rowid; other primary keys create an automatic unique index. Foreign keys never create an index on the child side in SQLite (from memory, not executed: PostgreSQL behaves the same, and MySQL InnoDB does create one).
- *Does join order in the FROM clause matter?* Not for ordinary JOINs in SQLite; it does for CROSS JOIN.
- *How would you find missing indexes?* Look for `SCAN` on the inner side of a join in the plan.

**Common mistakes:**
- Believing the FROM order is the join order.
- Leaving the foreign key column unindexed because the primary key is indexed.
- Relying on automatic indexes in production queries.
- Reading a plan without running `ANALYZE` and trusting the planner's guess.

### Q16 ⭐⭐ 🔴 Design indexes for a query mix: orders(order_id, customer_id, status, order_date, amount) with 300,000 rows and three workload queries: Q_a: WHERE customer_id = ? ORDER BY order_date DESC LIMIT 20 (a frequent customer page); Q_b: WHERE status = 'placed' AND order_date < ? (an ops backlog report, status 'placed' is about 3% of rows); Q_c: SELECT status, COUNT(*), SUM(amount) FROM orders WHERE order_date >= ? AND order_date < ? GROUP BY status (a daily dashboard). Propose a minimal index set, justify every column and its order, show plans and VM steps before and after, show the cost of the extra indexes on a bulk insert, and say which proposed index you would drop (redundant prefix, partial index alternative for the rare status) and what you would check in production (the plan, the slow-query log, index usage statistics: described for other engines, not executed).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Design indexes from the workload: for each query put the equality column first, then the range or sort column, add trailing columns only if they make the query covering, drop any index that is a prefix of another, use a partial index for a rare status, and weigh every index against its write cost.

**Schema and sample data:** 300,000 seeded rows; status is 80% delivered, 15% shipped, 3% placed (2.98% measured), 2% cancelled. Slice:
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL);
INSERT INTO orders VALUES (1,77,'placed','2024-01-10',10.0),(2,77,'delivered','2024-03-05',20.0),(3,8,'placed','2024-03-05',30.0);
```

**SQL answer:** the three workload queries, printed once in the Code block as `QA`, `QB`, `QC`:
```sql
-- Qa
SELECT order_id, order_date FROM orders WHERE customer_id = ? ORDER BY order_date DESC, order_id DESC LIMIT 20
-- Qb
SELECT order_id FROM orders WHERE status = 'placed' AND order_date < ?
-- Qc
SELECT status, COUNT(*), ROUND(SUM(amount), 2) FROM orders WHERE order_date >= ? AND order_date < ? GROUP BY status ORDER BY status
```
Proposed set: `ix_a(customer_id, order_date)` for Qa (equality, then the sort column, so no sort and the first 20 entries are the answer); `ix_b(status, order_date)` for Qb (equality, then range); `ix_c(order_date, status, amount)` for Qc (range first, then the grouping and aggregated columns, so the query is covered). Then I test dropping `ix_b` and replacing it with the partial index `ix_p(order_date) WHERE status = 'placed'`.

**pandas answer:** the three queries as masks, `sort_values` + `head(20)`, and a `groupby("status")` with `size` and `sum`; asserted against the SQL results for every index configuration (Qa exact order, Qb sorted `order_id`s, Qc counts exact and sums within a cent).

**Example:** Qb on the slice: `status = 'placed' AND order_date < '2024-02-01'` returns order 1. With `ix_b` the engine goes straight to the `placed` block of the index and reads entries up to the date bound (3,051 steps on the real data, 749 rows). Without it, it scans all 300,000 rows (919,408 steps). With only `ix_a` and `ix_c` the engine uses `ix_c` by `order_date < ?` and filters status on each entry (101,991 steps): 33 times the work of `ix_b`, about 11% of the full scan. With the partial `ix_p` only `placed` rows are indexed (43 pages against 2,107 pages for `ix_b`) and Qb is 3,050 steps.

**Code:** run with `python3 -I`. Write timings are machine-specific; the step counts are the portable numbers.
```python
# Q16
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

import time
rng = random.Random(61)
N = 300000
stat = ["delivered"] * 80 + ["shipped"] * 15 + ["placed"] * 3 + ["cancelled"] * 2
rows = [(i, rng.randint(1, 30000), rng.choice(stat), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
         round(rng.uniform(5, 500), 2)) for i in range(1, N + 1)]
DDL = "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL)"
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "order_date", "amount"])
print("share of 'placed':", round((df.status == "placed").mean() * 100, 2), "%")

def build(name, idx=()):
    path = WORK + "/" + name
    c = sqlite3.connect(path); c.execute(DDL)
    c.executemany("INSERT INTO orders VALUES(?,?,?,?,?)", rows)
    for s in idx: c.execute(s)
    c.commit(); c.close(); return path

QA = ("SELECT order_id, order_date FROM orders WHERE customer_id = ? ORDER BY order_date DESC, order_id DESC LIMIT 20", (77,))
QB = ("SELECT order_id FROM orders WHERE status = 'placed' AND order_date < ?", ("2024-02-01",))
QC = ("SELECT status, COUNT(*), ROUND(SUM(amount), 2) FROM orders WHERE order_date >= ? AND order_date < ? GROUP BY status ORDER BY status", ("2024-03-05", "2024-03-06"))
def report(label, path):
    out = {}
    for nm, (sql, p) in (("Qa", QA), ("Qb", QB), ("Qc", QC)):
        st, res = steps(path, sql, p)
        out[nm] = res
        print(f"  {nm}: steps {st:>9,} rows {len(res):>5} | {' | '.join(plan(path, sql, p))}")
    return out

print("--- 0. no secondary indexes ---")
r0 = report("none", build("none.db"))
IA = "CREATE INDEX ix_a ON orders(customer_id, order_date)"
IB = "CREATE INDEX ix_b ON orders(status, order_date)"
IC = "CREATE INDEX ix_c ON orders(order_date, status, amount)"
IP = "CREATE INDEX ix_p ON orders(order_date) WHERE status = 'placed'"
IA0 = "CREATE INDEX ix_cust ON orders(customer_id)"
print("--- 1. proposed set: ix_a(customer_id, order_date), ix_b(status, order_date), ix_c(order_date, status, amount) ---")
p3 = build("three.db", [IA, IB, IC])
r3 = report("three", p3)
print("--- 2. drop ix_b, keep ix_a and ix_c: how bad is Qb? ---")
p2 = build("ac.db", [IA, IC]); r2 = report("ac", p2)
print("--- 3. replace ix_b by the partial index ix_p(order_date) WHERE status = 'placed' ---")
pp = build("apc.db", [IA, IC, IP]); r3p = report("apc", pp)
print("--- 4. a redundant prefix: ix_cust(customer_id) next to ix_a ---")
pr = build("red.db", [IA0, IA])
print("  Qa with both:", " | ".join(plan(pr, *QA)))

# oracle: pandas answers
a = df[df.customer_id == 77].sort_values(["order_date", "order_id"], ascending=False).head(20)
b = df[(df.status == "placed") & (df.order_date < "2024-02-01")]
c = df[(df.order_date >= "2024-03-05") & (df.order_date < "2024-03-06")].groupby("status").agg(n=("amount", "size"), s=("amount", "sum")).reset_index().sort_values("status")
for r in (r0, r3, r2, r3p):
    assert r["Qa"] == list(zip(a.order_id, a.order_date))
    assert sorted(x[0] for x in r["Qb"]) == sorted(b.order_id)
    assert [(s, n) for s, n, _ in r["Qc"]] == list(zip(c.status, c.n))
    assert all(abs(t - round(s, 2)) < 0.011 for (_, _, t), s in zip(r["Qc"], c.s))

print("--- index sizes (dbstat) ---")
for nm, path in (("three.db", p3), ("apc.db", pp)):
    cc = sqlite3.connect(path)
    print(nm, [(n, pg) for n, pg in cc.execute("SELECT name, COUNT(*) FROM dbstat WHERE name LIKE 'ix_%' GROUP BY name ORDER BY name")])
    cc.close()

print("--- write cost: insert 100,000 more rows with k secondary indexes ---")
extra = [(N + i, rng.randint(1, 30000), rng.choice(stat), "2024-%02d-%02d" % (rng.randint(1, 12), rng.randint(1, 28)),
          round(rng.uniform(5, 500), 2)) for i in range(1, 100001)]
for label, idx in (("0 indexes", []), ("ix_a", [IA]), ("ix_a, ix_b", [IA, IB]), ("ix_a, ix_b, ix_c", [IA, IB, IC]), ("ix_a, ix_c, partial ix_p", [IA, IC, IP])):
    path = WORK + "/w_%d.db" % len(label)
    cc = sqlite3.connect(path); cc.execute(DDL)
    for s in idx: cc.execute(s)
    cc.commit()
    n = [0]
    def tick():
        n[0] += 1; return 0
    cc.set_progress_handler(tick, 1)
    t0 = time.perf_counter()
    cc.executemany("INSERT INTO orders VALUES(?,?,?,?,?)", extra)
    cc.commit()
    ms = (time.perf_counter() - t0) * 1000
    cc.set_progress_handler(None, 0); cc.close()
    print(f"  {label:<26} VM steps {n[0]:>10,}   time {ms:7.0f} ms (machine-specific)")
```

**Output (my run):**
```text
share of 'placed': 2.98 %
--- 0. no secondary indexes ---
  Qa: steps   900,095 rows     7 | SCAN orders | USE TEMP B-TREE FOR ORDER BY
  Qb: steps   919,408 rows   749 | SCAN orders
  Qc: steps 1,406,495 rows     4 | SCAN orders | USE TEMP B-TREE FOR GROUP BY
--- 1. proposed set: ix_a(customer_id, order_date), ix_b(status, order_date), ix_c(order_date, status, amount) ---
  Qa: steps        92 rows     7 | SEARCH orders USING COVERING INDEX ix_a (customer_id=?)
  Qb: steps     3,051 rows   749 | SEARCH orders USING COVERING INDEX ix_b (status=? AND order_date<?)
  Qc: steps    16,501 rows     4 | SEARCH orders USING COVERING INDEX ix_c (order_date>? AND order_date<?) | USE TEMP B-TREE FOR GROUP BY
--- 2. drop ix_b, keep ix_a and ix_c: how bad is Qb? ---
  Qa: steps        84 rows     7 | SEARCH orders USING COVERING INDEX ix_a (customer_id=?)
  Qb: steps   101,991 rows   749 | SEARCH orders USING COVERING INDEX ix_c (order_date<?)
  Qc: steps    16,492 rows     4 | SEARCH orders USING COVERING INDEX ix_c (order_date>? AND order_date<?) | USE TEMP B-TREE FOR GROUP BY
--- 3. replace ix_b by the partial index ix_p(order_date) WHERE status = 'placed' ---
  Qa: steps        91 rows     7 | SEARCH orders USING COVERING INDEX ix_a (customer_id=?)
  Qb: steps     3,050 rows   749 | SEARCH orders USING COVERING INDEX ix_p (order_date<?)
  Qc: steps    16,499 rows     4 | SEARCH orders USING COVERING INDEX ix_c (order_date>? AND order_date<?) | USE TEMP B-TREE FOR GROUP BY
--- 4. a redundant prefix: ix_cust(customer_id) next to ix_a ---
  Qa with both: SEARCH orders USING COVERING INDEX ix_a (customer_id=?)
--- index sizes (dbstat) ---
three.db [('ix_a', 1615), ('ix_b', 2107), ('ix_c', 2763)]
apc.db [('ix_a', 1615), ('ix_c', 2763), ('ix_p', 43)]
--- write cost: insert 100,000 more rows with k secondary indexes ---
  0 indexes                  VM steps  1,600,006   time     397 ms (machine-specific)
  ix_a                       VM steps  2,300,006   time     481 ms (machine-specific)
  ix_a, ix_b                 VM steps  2,900,006   time     915 ms (machine-specific)
  ix_a, ix_b, ix_c           VM steps  3,600,006   time    1636 ms (machine-specific)
  ix_a, ix_c, partial ix_p   VM steps  3,512,022   time    1219 ms (machine-specific)
```

**Edge cases:**
- **Qa returned only 7 rows** (customer 77 has 7 orders in this seed), so the `LIMIT 20` never bites; the plan is still the point: `SEARCH ... COVERING INDEX ix_a (customer_id=?)` with no temp b-tree, 92 steps against 900,095 for the scan plus sort.
- **Qc has a GROUP BY temp b-tree** even with `ix_c`, because the index is ordered by `order_date` first; 16,501 steps against 1,406,495. An index ordered `(status, order_date, amount)` would deliver the groups in order, but then the date range is no longer a single range probe: I did not test that one.
- **The redundant prefix** `ix_cust(customer_id)` next to `ix_a(customer_id, order_date)`: Qa used `ix_a`, so `ix_cust` serves only queries that `ix_a` already serves, and costs writes. Drop it.
- **Which one to drop:** `ix_b` (2,107 pages) becomes redundant if the partial `ix_p` (43 pages) is enough, because `ix_p` gave the same 3,050 steps for Qb; the price is that `ix_p` only helps queries that repeat `status = 'placed'` (Q10), and a new report on `shipped` would need another index.
- **Write cost.** Inserting 100,000 rows: 1,600,006 VM steps with no index, 2,300,006 with `ix_a`, 2,900,006 with `ix_a, ix_b`, 3,600,006 with all three, and 3,512,022 with `ix_a, ix_c, ix_p`. Times on this machine in the printed run were 397, 481, 915, 1,636 and 1,219 ms (machine-specific and noisy: an earlier run gave 353, 565, 940, 1,454 and 1,322 ms): each index added work and time, and the last configuration (partial index instead of `ix_b`) was cheaper than the three-index set in steps in both runs.
- **Data skew:** the status split here is seeded; on real data re-check the 3% claim before choosing a partial index.

**Then explain:**
- **Rule per query:** equality columns first, then the range/sort column, then payload columns for coverage.
- **Minimal set:** three indexes cover three queries; dropping `ix_b` costs 33 times more steps for the backlog report but saves an index, so the choice depends on how often Qb runs and how fresh it must be.
- **In production, check (described from memory, not executed here):** the actual plan with `EXPLAIN ANALYZE` (PostgreSQL), the slow-query log and `performance_schema` (MySQL), `pg_stat_user_indexes` for unused indexes in PostgreSQL, the missing-index and index-usage DMVs in SQL Server; SQLite has no usage counters, so I rely on plans.
- **Write-heavy tables:** each secondary index multiplies insert cost; batch loads can drop and rebuild indexes (not run here).
- **Index set review:** list all indexes, find prefixes, find indexes no plan uses, and check the writes per second the table sees.

**Follow-ups:**
- *Would the index order change if Qa had no `LIMIT`?* No; the sort is still avoided, but the whole customer history is returned.
- *What if `status` has a few values and `customer_id` many?* Equality columns still go first in order of how the queries filter; selectivity is secondary to the query shapes (Q17).
- *Can one composite index serve Qa and a customer-only lookup?* Yes, via the leftmost prefix.

**Common mistakes:**
- One index per column instead of composites that match query shapes.
- Putting the range column before the equality column.
- Keeping prefix-redundant indexes.
- Measuring only reads and ignoring insert/update cost.

### Q17 ⭐⭐ 🟡 Selectivity, cardinality and ANALYZE: events(event_id, user_id, event_type, country, event_time) with 300,000 seeded rows where user_id has about 20,000 distinct values, country has 5, and event_type has 3 values with one rare. Run ANALYZE and read sqlite_stat1 (the 'N k1 k2' stat string means rows and average rows per distinct key prefix), compute the selectivity of each index by hand and compare to the stat, show a plan that changes after ANALYZE (for example a join order or a skip-scan), and explain PRAGMA optimize, PRAGMA analysis_limit and that statistics are not updated automatically as data changes. Explain the equivalent ideas in PostgreSQL (pg_stats, ANALYZE, histograms), MySQL (ANALYZE TABLE, histograms) and SQL Server (statistics objects), hedged and not executed, and why the ranking 'index on the more selective column' is a heuristic.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; PostgreSQL docs using-explain and indexes-multicolumn and MySQL EXPLAIN output page (opened, used for contrast only); official documentation, not candidate reports; product company and GCC data engineer rounds
**Say this first (1 line):** The planner picks plans from statistics, and in SQLite those live in `sqlite_stat1` as strings like `'300000 15'` (total rows, then the average number of rows per distinct key prefix); they are a snapshot made by `ANALYZE`, not updated as data changes, and "index the more selective column" is only a heuristic built on those averages.

**Schema and sample data:** 300,000 events, `user_id` about 20,000 distinct, `country` 5 values, `event_type` 3 values (70% view, 29% click, 1% purchase), `event_time` hourly strings. Indexes `ix_user(user_id)`, `ix_type(event_type)`, `ix_country_time(country, event_time)`. Slice:
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INT, event_type TEXT, country TEXT, event_time TEXT);
INSERT INTO events VALUES (1,5,'view','IN','2024-03-05 10:00'),(2,5,'click','IN','2024-03-05 11:00'),(3,6,'view','US','2024-03-05 10:00'),(4,7,'purchase','IN','2024-03-06 09:00');
```
By hand on the slice: 4 rows, 3 distinct `user_id` values, so about 1.33 rows per user; `ANALYZE` stores whole numbers, so the exact rounding is easier to check on the big table (below) than on this slice. The rare `purchase` is 1 row of 4, which an average per value cannot show.

**SQL answer:** `ANALYZE;` then `SELECT idx, stat FROM sqlite_stat1`, and the queries listed in the Code block (`QS`), each with plan and VM steps before and after. Hand check on the big table: rows divided by distinct values, `300000 / 20000 = 15` for `user_id`, `300000 / 3 = 100000` for `event_type`, `300000 / 5 = 60000` for `country` alone; the code computes the second number of each stat from the data (`groupby(...).ngroups`) and asserts it within one row.

**pandas answer:** `df.groupby(cols).ngroups` gives the number of distinct key prefixes; `ceil(N / ngroups)` reproduces each number in `sqlite_stat1` (asserted within 1 row); `value_counts()` gives the real per-value counts the average hides.

**Example:** `ix_type` has stat `'300000 100000'`: three distinct values, so the planner thinks any `event_type = ?` returns 100,000 rows. Actually `view` returned 209,785 rows, `click` 87,163 and `purchase` 3,052. The estimate is exactly right on average and wrong for every single value: the `purchase` lookup cost 27,540 steps, `view` cost 1,888,136. For `country = 'IN' AND event_type = 'purchase'` the planner compared its two averages (60,000 for `country`, 100,000 for `event_type`) and chose `ix_country_time`: 304,155 steps. `INDEXED BY ix_type` cost 18,989 steps for the same 609 rows, 16 times fewer, because `purchase` is rare. The heuristic "the more selective column" was applied to averages and chose wrongly.

**Code:** run with `python3 -I`.
```python
# Q17
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

rng = random.Random(71)
N = 300000
countries = ["IN", "US", "UK", "DE", "SG"]
types = ["view"] * 70 + ["click"] * 29 + ["purchase"] * 1       # 'purchase' is rare (1%)
rows = [(i, rng.randint(1, 20000), rng.choice(types), rng.choice(countries),
         "2024-%02d-%02d %02d:00" % (rng.randint(1, 12), rng.randint(1, 28), rng.randint(0, 23))) for i in range(1, N + 1)]
path = WORK + "/ev.db"
c = sqlite3.connect(path)
c.execute("CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INT, event_type TEXT, country TEXT, event_time TEXT)")
c.executemany("INSERT INTO events VALUES(?,?,?,?,?)", rows)
for s in ["CREATE INDEX ix_user ON events(user_id)", "CREATE INDEX ix_type ON events(event_type)",
          "CREATE INDEX ix_country_time ON events(country, event_time)"]:
    c.execute(s)
c.commit(); c.close()
df = pd.DataFrame(rows, columns=["event_id", "user_id", "event_type", "country", "event_time"])
print("distinct user_id:", df.user_id.nunique(), "| event_type counts:", df.event_type.value_counts().to_dict())

QS = {"user_id = 5": "SELECT * FROM events WHERE user_id = 5",
      "event_type = 'purchase' (rare)": "SELECT * FROM events WHERE event_type = 'purchase'",
      "event_type = 'view' (common)": "SELECT * FROM events WHERE event_type = 'view'",
      "event_time = '2024-03-05 10:00' (2nd column only)": "SELECT * FROM events WHERE event_time = '2024-03-05 10:00'",
      "country = 'IN' AND event_type = 'purchase'": "SELECT * FROM events WHERE country = 'IN' AND event_type = 'purchase'"}
def plans(title):
    print(title)
    for k, q in QS.items():
        st, res = steps(path, q)
        print(f"  {k:<52} steps {st:>9,} rows {len(res):>6,} | {' | '.join(plan(path, q))}")
def stat1():
    cc = sqlite3.connect(path)
    r = cc.execute("SELECT idx, stat FROM sqlite_stat1 ORDER BY idx").fetchall() if cc.execute("SELECT 1 FROM sqlite_master WHERE name='sqlite_stat1'").fetchone() else None
    cc.close(); return r
print("sqlite_stat1 before ANALYZE:", stat1())
plans("--- plans before ANALYZE ---")
c = sqlite3.connect(path); c.execute("ANALYZE"); c.commit(); c.close()
s = dict(stat1())
print("sqlite_stat1 after ANALYZE:", s)
plans("--- plans after ANALYZE ---")

print("--- the planner's pick for country AND event_type is a heuristic, not a guarantee ---")
q = "SELECT * FROM events %s WHERE country = 'IN' AND event_type = 'purchase'"
for lab, hint in (("planner's choice", ""), ("INDEXED BY ix_type", "INDEXED BY ix_type")):
    st, res = steps(path, q % hint)
    print(f"  {lab:<20} steps {st:>9,} rows {len(res)} | {' | '.join(plan(path, q % hint))}")

print("--- selectivity by hand (rows / distinct values) ---")
for idx, cols in (("ix_user", ["user_id"]), ("ix_type", ["event_type"]), ("ix_country_time", ["country", "event_time"])):
    expect = [N]
    for k in range(1, len(cols) + 1):
        expect.append(int(np.ceil(N / df.groupby(cols[:k]).ngroups)))
    got = [int(x) for x in s[idx].split()]
    print(f"  {idx:<16} stat {s[idx]!r:<22} by hand {expect}")
    assert got == expect or all(abs(a - b) <= 1 for a, b in zip(got, expect)), (got, expect)
print("  actual rows for event_type values:", df.event_type.value_counts().to_dict(), "(stat says", s["ix_type"].split()[1], "for every value)")

print("--- statistics are a snapshot: add 100,000 rows of one new user ---")
c = sqlite3.connect(path)
c.executemany("INSERT INTO events VALUES(?,?,?,?,?)", [(N + i, 999999, "view", "IN", "2024-12-31 23:00") for i in range(1, 100001)])
c.commit(); c.close()
print("stat1 unchanged:", dict(stat1())["ix_user"], "| true rows for user 999999:", 100000)
c = sqlite3.connect(path)
c.execute("SELECT COUNT(*) FROM events WHERE user_id = 999999").fetchall()     # optimize only looks at tables this connection queried
print("PRAGMA optimize(0x03) dry run (lists the ANALYZE it would run):", c.execute("PRAGMA optimize(0x03)").fetchall())
print("PRAGMA optimize(0x02) runs it:", c.execute("PRAGMA optimize(0x02)").fetchall()); c.commit(); c.close()
print("stat1 after optimize:", dict(stat1())["ix_user"], "| sqlite_stat1 rows:", len(stat1()))
c = sqlite3.connect(path)
c.execute("PRAGMA analysis_limit = 400"); c.execute("ANALYZE"); c.commit()
print("PRAGMA analysis_limit=400 then ANALYZE ->", c.execute("PRAGMA analysis_limit").fetchone(), dict(stat1()))
c.close()

print("--- PRAGMA optimize on a table whose size changed a lot (1,000 -> 51,000 rows) ---")
p2 = WORK + "/opt.db"
c = sqlite3.connect(p2)
c.execute("CREATE TABLE a(id INTEGER PRIMARY KEY, u INT)"); c.execute("CREATE INDEX ia ON a(u)")
c.executemany("INSERT INTO a(u) VALUES(?)", [(i % 100,) for i in range(1000)]); c.execute("ANALYZE"); c.commit()
c.executemany("INSERT INTO a(u) VALUES(?)", [(i % 100,) for i in range(50000)]); c.commit(); c.close()
c = sqlite3.connect(p2)
c.execute("SELECT * FROM a WHERE u = 5").fetchall()
print("stat1 now:", c.execute("SELECT * FROM sqlite_stat1").fetchall())
print("PRAGMA optimize(0x03) says:", c.execute("PRAGMA optimize(0x03)").fetchall())
c.execute("PRAGMA optimize"); c.commit()
print("stat1 after PRAGMA optimize:", c.execute("SELECT * FROM sqlite_stat1").fetchall())
c.close()
```

**Output (my run):**
```text
distinct user_id: 20000 | event_type counts: {'view': 209785, 'click': 87163, 'purchase': 3052}
sqlite_stat1 before ANALYZE: None
--- plans before ANALYZE ---
  user_id = 5                                          steps       152 rows     12 | SEARCH events USING INDEX ix_user (user_id=?)
  event_type = 'purchase' (rare)                       steps    27,512 rows  3,052 | SEARCH events USING INDEX ix_type (event_type=?)
  event_type = 'view' (common)                         steps 1,888,108 rows 209,785 | SEARCH events USING INDEX ix_type (event_type=?)
  event_time = '2024-03-05 10:00' (2nd column only)    steps   900,253 rows     35 | SCAN events
  country = 'IN' AND event_type = 'purchase'           steps   304,127 rows    609 | SEARCH events USING INDEX ix_country_time (country=?)
sqlite_stat1 after ANALYZE: {'ix_country_time': '300000 60000 8', 'ix_type': '300000 100000', 'ix_user': '300000 15'}
--- plans after ANALYZE ---
  user_id = 5                                          steps       180 rows     12 | SEARCH events USING INDEX ix_user (user_id=?)
  event_type = 'purchase' (rare)                       steps    27,540 rows  3,052 | SEARCH events USING INDEX ix_type (event_type=?)
  event_type = 'view' (common)                         steps 1,888,136 rows 209,785 | SEARCH events USING INDEX ix_type (event_type=?)
  event_time = '2024-03-05 10:00' (2nd column only)    steps       423 rows     35 | SEARCH events USING INDEX ix_country_time (ANY(country) AND event_time=?)
  country = 'IN' AND event_type = 'purchase'           steps   304,155 rows    609 | SEARCH events USING INDEX ix_country_time (country=?)
--- the planner's pick for country AND event_type is a heuristic, not a guarantee ---
  planner's choice     steps   304,155 rows 609 | SEARCH events USING INDEX ix_country_time (country=?)
  INDEXED BY ix_type   steps    18,989 rows 609 | SEARCH events USING INDEX ix_type (event_type=?)
--- selectivity by hand (rows / distinct values) ---
  ix_user          stat '300000 15'            by hand [300000, 15]
  ix_type          stat '300000 100000'        by hand [300000, 100000]
  ix_country_time  stat '300000 60000 8'       by hand [300000, 60000, 8]
  actual rows for event_type values: {'view': 209785, 'click': 87163, 'purchase': 3052} (stat says 100000 for every value)
--- statistics are a snapshot: add 100,000 rows of one new user ---
stat1 unchanged: 300000 15 | true rows for user 999999: 100000
PRAGMA optimize(0x03) dry run (lists the ANALYZE it would run): []
PRAGMA optimize(0x02) runs it: []
stat1 after optimize: 300000 15 | sqlite_stat1 rows: 3
PRAGMA analysis_limit=400 then ANALYZE -> (400,) {'ix_country_time': '426466 401 8', 'ix_type': '361380 401', 'ix_user': '398400 15'}
--- PRAGMA optimize on a table whose size changed a lot (1,000 -> 51,000 rows) ---
stat1 now: [('a', 'ia', '1000 10')]
PRAGMA optimize(0x03) says: [('ANALYZE "main"."a"',)]
stat1 after PRAGMA optimize: [('a', 'ia', '51000 510')]
```

**Edge cases:**
- **Before ANALYZE there is no `sqlite_stat1`** (the table does not exist yet; my code prints `None`) and the planner uses built-in defaults.
- **Skip-scan appears only with statistics.** `event_time = '2024-03-05 10:00'` (second column of `ix_country_time`) was `SCAN events` (900,253 steps) before and `SEARCH ... (ANY(country) AND event_time=?)` (423 steps) after `ANALYZE`: with only 5 countries and 60,000 rows each, probing each country is cheap. A skip-scan on a high-cardinality first column would be hopeless; the planner decides from the stat.
- **Statistics are not updated.** After inserting 100,000 rows for one new user, `ix_user` still said `300000 15`, though the true count for that user was 100,000.
- **`PRAGMA optimize`.** In the events database (300,000 to 400,000 rows) it did nothing (empty result, stat unchanged). In a second small database where a table grew from 1,000 to 51,000 rows after `ANALYZE`, `PRAGMA optimize(0x03)` listed `ANALYZE "main"."a"` and `PRAGMA optimize` ran it (`'1000 10'` became `'51000 510'`). So it re-analyses only when it judges the size change large; I did not determine the exact threshold, and the documentation says its behaviour changed in later releases (I did not verify 3.46).
- **`PRAGMA analysis_limit = 400`** makes `ANALYZE` examine only about 400 index entries per index and gives approximate values: the stat strings became `'426466 401 8'`, `'361380 401'` and `'398400 15'`, with row counts that are estimates (the true table then had 400,000 rows). The averages for `ix_user` (15) and the composite's last column (8) stayed close, but the second numbers (401 for `country` and for `event_type`, against 60,000 and 100,000 without the limit) are far off; I did not investigate why, so treat limited stats as coarse. Use it on big tables to bound the cost of `ANALYZE`, and treat the numbers as approximate.
- **Fixed plans.** Stat strings can be written by hand in `sqlite_stat1` (documented); I did not run that.
- **Rare value, equal estimate:** the plan for `purchase` and `view` was the same `SEARCH ... ix_type (event_type=?)`, which is right for the rare value and a poor choice for the common one (1.89M steps vs a scan).

**Then explain:**
- **Reading `'N k1 k2'`:** N rows in the index; k1 rows per distinct value of the first column; k2 rows per distinct pair, and so on. A low last number means the index is close to unique.
- **Selectivity:** the fraction of rows a predicate keeps; low-cardinality columns (country) are poor index keys by themselves, high-cardinality ones (user_id) good. But the average per key is not the count for a particular key: skew breaks it (Q18).
- **Why the ranking is a heuristic:** it ignores correlation between columns (a rare event type may be concentrated in one country), skew, the data layout, caching, and whether the index is covering.
- **Other engines (hedged, not executed):** PostgreSQL keeps per-column statistics in `pg_stats` (most common values, histograms, distinct estimates) refreshed by `ANALYZE` and autovacuum; MySQL has `ANALYZE TABLE` and, from 8.0, histograms that you create explicitly; SQL Server keeps statistics objects (histograms) per index and column, and updates them automatically after enough changes. So those engines can see skew that the SQLite average hides; SQLite can too with the optional stat4 build option, which this build may not include (not checked).
- **Operational advice:** run `ANALYZE` after bulk loads and large deletes; use `PRAGMA optimize` before closing short-lived connections (SQLite docs advice, from memory).

**Follow-ups:**
- *Who updates statistics in production?* In SQLite, you do; in PostgreSQL and SQL Server, background jobs, with manual refresh when needed.
- *Is cardinality the same as selectivity?* Cardinality is the number of distinct values; selectivity is the fraction of rows matched by a predicate.
- *Why did the plan change only after `ANALYZE`?* Without stats the planner uses defaults, so it did not consider the skip-scan worthwhile.

**Common mistakes:**
- Assuming statistics update themselves in SQLite.
- Treating the average rows per key as the cost of every key.
- Indexing a 5-value column on its own and expecting a win.
- Comparing plans without running `ANALYZE` first, or reading them on an old connection.

### Q18 ⭐⭐ 🔴 Skew, stale statistics and cardinality-estimation errors: orders(order_id, customer_id, status, amount) with 200,000 rows where status is 'delivered' for 98% and 'cancelled' for 0.5% (seeded), with an index on status. Show that SQLite estimates the same number of rows for every status value from sqlite_stat1 averages (read the stat), print the plan for status = 'cancelled' and status = 'delivered' and compare real row counts and VM steps for the index path versus NOT INDEXED, then show what happens after a bulk update changes the distribution and before ANALYZE is re-run. Explain INDEXED BY and NOT INDEXED as hints (and that INDEXED BY errors if the index cannot be used, check by running), the unary + trick, and the concept of cardinality-estimation errors producing a bad join order. Describe PostgreSQL EXPLAIN ANALYZE estimated versus actual rows and plan hints in other engines as not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; PostgreSQL docs using-explain and indexes-multicolumn and MySQL EXPLAIN output page (opened, used for contrast only); official documentation, not candidate reports; product company and GCC data engineer rounds
**Say this first (1 line):** SQLite's `sqlite_stat1` stores one average per index ("200000 50000": rows, then rows per distinct status), so every status value gets the same estimate whether it matches 0.5% or 98% of the table; the index is great for the rare value and pointless for the common one, and `INDEXED BY`, `NOT INDEXED` and unary `+` are blunt overrides.

**Schema and sample data:** 200,000 orders; status is 98% delivered, 1% placed, 0.5% returned, 0.5% cancelled (measured: 97.98, 1.0, 0.53, 0.5 %), plus `customers` (20,000) for the join-order part. Slice:
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, amount REAL);
INSERT INTO orders VALUES (1,1,'delivered',10.0),(2,2,'delivered',20.0),(3,3,'delivered',30.0),(4,1,'cancelled',5.0);
CREATE INDEX ix_status ON orders(status);
```
On the slice `ANALYZE` would store 4 rows and 2 distinct statuses, an average of 2 rows per status: right on average, wrong for both values (3 and 1).

**SQL answer:** `ANALYZE`, `SELECT stat FROM sqlite_stat1 WHERE idx = 'ix_status'`, then each `status = ?` query with the index, with `NOT INDEXED`, and with `+status = ?` (unary plus disables index use for that term). The statements are in the Code block.

**pandas answer:** `df.status.value_counts()` is the true distribution (the thing the optimiser does not store); every SQL row count is asserted against it, and the join result against `merge`.

**Example:** `ix_status` stat is `200000 50000`: 200,000 rows, 4 distinct values, so 50,000 per value. Real counts: `cancelled` 991 rows, `delivered` 195,952. For `cancelled` the index path cost 9,000 VM steps against 606,024 for a scan (67 times better); for `delivered` it cost 1,763,649 against 1,775,790 for `NOT INDEXED`: no real gain, and each of the 195,952 index entries needs a table lookup that costs more in I/O than the steps show. The planner printed the same plan for both values: `SEARCH ... USING INDEX ix_status (status=?)`.

**Code:** run with `python3 -I`; it uses temporary file databases and fresh connections for every plan and step count (see Q10 for why).
```python
# Q18
import sqlite3, random, tempfile
import numpy as np
import pandas as pd

WORK = tempfile.mkdtemp()          # file databases: every plan and step count uses a FRESH connection

def plan(path, sql, params=()):
    """EXPLAIN QUERY PLAN detail lines, read on a fresh connection (a reused connection can show a stale plan)."""
    c = sqlite3.connect(path)
    try:
        return [r[3] for r in c.execute("EXPLAIN QUERY PLAN " + sql, params)]
    finally:
        c.close()

def steps(path, sql, params=()):
    """(VM steps, rows) for one statement: set_progress_handler(cb, 1) fires once per VM opcode."""
    c = sqlite3.connect(path)
    n = [0]
    def tick():
        n[0] += 1
        return 0
    c.set_progress_handler(tick, 1)
    rows = c.execute(sql, params).fetchall()
    c.set_progress_handler(None, 0)
    c.close()
    return n[0], rows

rng = random.Random(81)
N = 200000
pool = ["delivered"] * 980 + ["cancelled"] * 5 + ["placed"] * 10 + ["returned"] * 5
cities = ["Pune", "Delhi", "Mumbai", "Chennai", "Kolkata", "Jaipur", "Indore", "Surat", "Patna", "Noida"]
cust = [(i, "c%d" % i, rng.choice(cities)) for i in range(1, 20001)]
rows = [(i, rng.randint(1, 20000), rng.choice(pool), round(rng.uniform(5, 500), 2)) for i in range(1, N + 1)]
path = WORK + "/s.db"
c = sqlite3.connect(path)
c.executescript("""CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, amount REAL);""")
c.executemany("INSERT INTO customers VALUES(?,?,?)", cust); c.executemany("INSERT INTO orders VALUES(?,?,?,?)", rows)
c.execute("CREATE INDEX ix_status ON orders(status)"); c.execute("CREATE INDEX ix_cust ON orders(customer_id)")
c.execute("CREATE INDEX ix_city ON customers(city)")
c.commit(); c.close()
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "amount"])
CU = pd.DataFrame(cust, columns=["customer_id", "name", "city"])
true = df.status.value_counts()
print("true counts:", true.to_dict(), "| shares %:", (true / N * 100).round(2).to_dict())

def stat():
    cc = sqlite3.connect(path)
    r = dict(cc.execute("SELECT idx, stat FROM sqlite_stat1").fetchall()) if cc.execute("SELECT 1 FROM sqlite_master WHERE name='sqlite_stat1'").fetchone() else None
    cc.close(); return r
def line(label, sql, params=()):
    st, res = steps(path, sql, params)
    print(f"  {label:<44} steps {st:>9,} rows {len(res):>8,} | {' | '.join(plan(path, sql, params))}")
    return res

c = sqlite3.connect(path); c.execute("ANALYZE"); c.commit(); c.close()
print("sqlite_stat1 (status):", stat()["ix_status"], "-> 'rows, average rows per distinct status', not per value")
print("--- one estimate for every value; real counts differ ---")
for v in ("cancelled", "delivered"):
    a = line(f"status = '{v}' (planner)", "SELECT * FROM orders WHERE status = ?", (v,))
    b = line(f"status = '{v}' NOT INDEXED", "SELECT * FROM orders NOT INDEXED WHERE status = ?", (v,))
    d = line(f"status = '{v}' unary +", "SELECT * FROM orders WHERE +status = ?", (v,))
    assert sorted(a) == sorted(b) == sorted(d) and len(a) == true[v]

print("--- INDEXED BY and NOT INDEXED as hints; when INDEXED BY errors ---")
for lab, sql in (("INDEXED BY ix_nosuch", "SELECT * FROM orders INDEXED BY ix_nosuch WHERE status = 'x'"),
                 ("INDEXED BY ix_cust, filter on status", "SELECT * FROM orders INDEXED BY ix_cust WHERE status = 'cancelled'"),
                 ("INDEXED BY ix_status, filter on customer", "SELECT * FROM orders INDEXED BY ix_status WHERE customer_id = 5")):
    cc = sqlite3.connect(path)
    try:
        n = len(cc.execute(sql).fetchall()); print(f"  {lab}: ok, {n} rows | plan {' | '.join(r[3] for r in cc.execute('EXPLAIN QUERY PLAN ' + sql))}")
    except sqlite3.Error as e:
        print(f"  {lab}: error: {e}")
    cc.close()
cc = sqlite3.connect(path); cc.execute("CREATE INDEX ix_part ON orders(amount) WHERE status = 'cancelled'"); cc.commit()
try:
    cc.execute("SELECT * FROM orders INDEXED BY ix_part WHERE amount > 100").fetchall()
except sqlite3.Error as e:
    print("  INDEXED BY a partial index the WHERE does not imply: error:", e)
cc.execute("DROP INDEX ix_part"); cc.commit(); cc.close()

print("--- a cardinality error shows up as a join order ---")
QJ = "SELECT COUNT(*) FROM orders o %s customers c ON c.customer_id = o.customer_id WHERE o.status = 'cancelled' AND c.city = 'Pune'"
QJ2 = "SELECT COUNT(*) FROM customers c CROSS JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'cancelled' AND c.city = 'Pune'"
want = len(df[df.status == "cancelled"].merge(CU[CU.city == "Pune"], on="customer_id"))
for lab, sql in (("planner's order", QJ % "JOIN"), ("forced: orders first", QJ % "CROSS JOIN"), ("forced: customers first", QJ2)):
    r = line(lab, sql); assert r[0][0] == want
print("pandas merge count:", want)

print("--- a bulk update changes the distribution; statistics are not refreshed ---")
c = sqlite3.connect(path)
c.execute("UPDATE orders SET status = 'cancelled' WHERE order_id % 2 = 0 AND status = 'delivered'"); c.commit(); c.close()
df.loc[(df.order_id % 2 == 0) & (df.status == "delivered"), "status"] = "cancelled"
true2 = df.status.value_counts()
print("true counts now:", true2.to_dict(), "| stat still:", stat()["ix_status"])
a = line("status = 'cancelled' (stale stats)", "SELECT * FROM orders WHERE status = 'cancelled'")
b = line("status = 'cancelled' NOT INDEXED", "SELECT * FROM orders NOT INDEXED WHERE status = 'cancelled'")
assert len(a) == len(b) == true2["cancelled"]
c = sqlite3.connect(path); c.execute("ANALYZE"); c.commit(); c.close()
print("after ANALYZE (still 4 distinct values, so the average is unchanged):", stat()["ix_status"])
c = sqlite3.connect(path)
c.execute("UPDATE orders SET status = 'S' || (order_id % 40) WHERE status = 'delivered'"); c.commit()
print("after splitting 'delivered' into 40 labels, stat1 not refreshed:", stat()["ix_status"])
c.execute("ANALYZE"); c.commit(); c.close()
print("after ANALYZE:", stat()["ix_status"], "| distinct statuses:", sqlite3.connect(path).execute("SELECT COUNT(DISTINCT status) FROM orders").fetchone()[0])
```

**Output (my run):**
```text
true counts: {'delivered': 195952, 'placed': 1990, 'returned': 1067, 'cancelled': 991} | shares %: {'delivered': 97.98, 'placed': 1.0, 'returned': 0.53, 'cancelled': 0.5}
sqlite_stat1 (status): 200000 50000 -> 'rows, average rows per distinct status', not per value
--- one estimate for every value; real counts differ ---
  status = 'cancelled' (planner)               steps     9,000 rows      991 | SEARCH orders USING INDEX ix_status (status=?)
  status = 'cancelled' NOT INDEXED             steps   606,024 rows      991 | SCAN orders
  status = 'cancelled' unary +                 steps   606,024 rows      991 | SCAN orders
  status = 'delivered' (planner)               steps 1,763,649 rows  195,952 | SEARCH orders USING INDEX ix_status (status=?)
  status = 'delivered' NOT INDEXED             steps 1,775,790 rows  195,952 | SCAN orders
  status = 'delivered' unary +                 steps 1,775,790 rows  195,952 | SCAN orders
--- INDEXED BY and NOT INDEXED as hints; when INDEXED BY errors ---
  INDEXED BY ix_nosuch: error: no such index: ix_nosuch
  INDEXED BY ix_cust, filter on status: ok, 991 rows | plan SCAN orders USING INDEX ix_cust
  INDEXED BY ix_status, filter on customer: ok, 9 rows | plan SCAN orders USING INDEX ix_status
  INDEXED BY a partial index the WHERE does not imply: error: no query solution
--- a cardinality error shows up as a join order ---
  planner's order                              steps   105,434 rows        1 | SEARCH c USING COVERING INDEX ix_city (city=?) | SEARCH o USING INDEX ix_cust (customer_id=?)
  forced: orders first                         steps    71,254 rows        1 | SEARCH o USING INDEX ix_status (status=?) | BLOOM FILTER ON c (customer_id=?) | SEARCH c USING INTEGER PRIMARY KEY (rowid=?)
  forced: customers first                      steps   105,436 rows        1 | SEARCH c USING COVERING INDEX ix_city (city=?) | SEARCH o USING INDEX ix_cust (customer_id=?)
pandas merge count: 82
--- a bulk update changes the distribution; statistics are not refreshed ---
true counts now: {'cancelled': 99002, 'delivered': 97941, 'placed': 1990, 'returned': 1067} | stat still: 200000 50000
  status = 'cancelled' (stale stats)           steps   891,097 rows   99,002 | SEARCH orders USING INDEX ix_status (status=?)
  status = 'cancelled' NOT INDEXED             steps 1,194,090 rows   99,002 | SCAN orders
after ANALYZE (still 4 distinct values, so the average is unchanged): 200000 50000
after splitting 'delivered' into 40 labels, stat1 not refreshed: 200000 50000
after ANALYZE: 200000 8696 | distinct statuses: 23
```

**Edge cases:**
- **Hints.** `NOT INDEXED` and unary `+status = ?` both produced `SCAN orders` (606,024 steps for `cancelled`). `INDEXED BY ix_nosuch` raised `no such index: ix_nosuch`. `INDEXED BY ix_cust WHERE status = 'cancelled'` did not error: it printed `SCAN orders USING INDEX ix_cust`, i.e. a full scan of the wrong index, which is worse than a plain scan. The error appears when the index cannot be used at all: a partial index whose WHERE the query does not imply gave `no query solution` (my run). So `INDEXED BY` does not guarantee a good plan; it only guarantees that this index or an error is used.
- **Bulk update, same statistics.** After setting `delivered` to `cancelled` for every even `order_id`, `cancelled` held 99,002 rows (about half the table) and the stat still said `200000 50000`, as it should: four distinct values is still four, so even a fresh `ANALYZE` printed the same string. The plan for `cancelled` stayed `SEARCH ... USING INDEX ix_status`, which cost 891,097 steps against 1,194,090 for a scan; at half the table the index was still slightly cheaper in steps but likely more expensive in real life for the reasons above (not measured). Freshness did not matter here; skew did.
- **When statistics do go stale.** After splitting `delivered` into many labels (23 distinct statuses afterwards), the old stat still said `200000 50000` and re-running `ANALYZE` produced `200000 8696`. That is the stale-statistics case: distinct count changes are visible, distribution changes are not.
- **Join order.** For `o.status = 'cancelled' AND c.city = 'Pune'` the planner chose customers first (`SEARCH c USING COVERING INDEX ix_city`, then `SEARCH o USING INDEX ix_cust`): 105,434 steps. Forcing orders first with `CROSS JOIN` gave `SEARCH o USING INDEX ix_status (status=?)` then a bloom filter and a primary-key probe of customers: 71,254 steps, about a third fewer. The planner's choice was not catastrophic here; it would be if the estimate was off by a larger factor. Same 82 result rows as the pandas merge.
- **Row estimates across engines (not executed here).** PostgreSQL stores most-common values and histograms, so `EXPLAIN ANALYZE` shows estimated versus actual rows per plan node and a big gap flags the problem; it has no plan hints in core (extensions exist); MySQL has optimizer hints and index hints; SQL Server has `OPTION` hints and plan guides; Oracle has hints. I have not run any of these.

**Then explain:**
- **Why one number per index:** `ANALYZE` stores the average; a histogram (the optional `stat4` build option) would let SQLite see the skew; I did not check whether this build has it.
- **What a bad estimate does:** a wrong row estimate propagates into join order, join method and index choice; the costs multiply down the plan, which is how a small estimate error becomes a 100-times-slower query.
- **Overrides in order of preference:** fix the query shape, refresh statistics, add a better index or a partial index (`WHERE status = 'cancelled'`, Q10); `INDEXED BY` / `NOT INDEXED` / unary `+` last, because they freeze today's data distribution into the SQL text.
- **In an interview:** say "estimate versus actual rows is the first thing I compare" (PostgreSQL `EXPLAIN ANALYZE`, described), and that row-count estimates of the first mistaken node are the root cause, not the slowest node.

**Follow-ups:**
- *How would a partial index help here?* `CREATE INDEX ... ON orders(order_id) WHERE status = 'cancelled'` indexes only the rare rows (Q16 shows the 43-page partial index).
- *What if the application passes the status as a bind parameter?* The plan may be chosen without knowing the value (parameter sniffing in SQL Server is a related issue, described not executed).
- *What does unary `+` do?* It turns `status` into an expression so the term cannot use an index; it is a standard SQLite trick and does not change results.

**Common mistakes:**
- Believing an index is always better than a scan.
- Forcing an index with `INDEXED BY` in application code and forgetting it after the data changes.
- Re-running `ANALYZE` and expecting it to fix skew when the stat stores only averages.
- Blaming the slowest operator instead of the first wrong estimate.
