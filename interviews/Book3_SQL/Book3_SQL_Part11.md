# Book 3 — Part 11: Query optimisation, indexes, execution plans and partitioning, with pandas performance

**Topic:** reading EXPLAIN QUERY PLAN (SCAN, SEARCH, covering index, temp b-tree, co-routine, materialize, automatic index, bloom filter), CREATE INDEX variants (single, composite, covering, partial, expression, UNIQUE, COLLATE NOCASE), the leftmost-prefix rule and column order, selectivity, ANALYZE and sqlite_stat1, skew and stale statistics, sargability (functions on columns, LIKE, type conversion, OR, != and NOT IN), IN versus EXISTS versus JOIN and anti-join forms, ORDER BY with LIMIT, OFFSET versus keyset pagination, covering indexes, join keys and fan-out, correlated subqueries, CTE materialisation, window sort cost, write cost and batching, N+1 queries, rowid versus WITHOUT ROWID, VACUUM and page counts, hints, plan caching, WAL locking, VM-step counts with set_progress_handler as a deterministic cost proxy, pandas performance (vectorisation, dtypes and category, chunked reading, merge versus map, query versus masks, copy-on-write, SQL push-down), and concept-level, not-executed coverage of partitioning, clustering and sort keys, columnar storage, materialised views, execution plans in PostgreSQL, MySQL and SQL Server, bitmap and hash joins, parameter sniffing and isolation.
**Target:** 35  |  **Actual:** 35 (⭐⭐⭐ 14, ⭐⭐ 15, ⭐ 6)  |  **Date:** 2026-10-25  |  **Status:** Questions frozen (Wave A); answers pending (Wave B)

Scope note: this part owns query cost, plans and physical design. Part 1 to Part 3 own the query logic that these questions optimise: Part 2 Q2 (anti-join), Q8 (semi-join), Q12 (fan-out inflates SUM), Q13 (the chasm trap), Q17 (join order) and Q18 (join to an aggregated derived table); Part 3 Q3 (NOT IN NULL trap), Q4 (EXISTS versus IN), Q32 (reusing one CTE twice) and Q39 (correlated subquery performance); Part 4 Q39 (top N and pagination with ROW_NUMBER) and Q40 (window function performance concept) already gave short concept answers that these questions extend with plans and VM-step counts. Data engineering topics beyond SQL (Spark, Kafka, orchestration) belong to Book 4.

Evidence limits: no candidate-reported questions were found. Sources are the SQLite documentation (EXPLAIN QUERY PLAN, query planner, optimizer overview, CREATE INDEX, ANALYZE, WITHOUT ROWID), PostgreSQL docs (using-explain, indexes-multicolumn) and the MySQL EXPLAIN output page for contrast only, the pandas 'Enhancing performance' and 'Scaling to large datasets' guides (all opened), editorial SQL-optimisation interview guides (opened, none claims candidate reports) and search snippets on partitioning, clustering and parameter sniffing (not opened). 'Asked at' tags are source types, not company reports. Environment (checked by running): SQLite 3.45.1 and pandas 3.0.5; no PostgreSQL, MySQL, SQL Server or DuckDB. Every non-SQLite engine statement must be labelled 'not executed'. Timings are machine-specific; VM-step counts and plans are the deterministic evidence. See research_notes/Book3_Part11_sources.md for the plan texts and numbers checked in Wave A.

---

### Q1 ⭐⭐⭐ 🟢 Read EXPLAIN QUERY PLAN: orders(order_id INTEGER PRIMARY KEY, customer_id, order_date TEXT, status, amount) with 200,000 seeded rows and customers(customer_id INTEGER PRIMARY KEY, name, city) with 20,000 rows. Print the plan for SELECT * FROM orders WHERE customer_id = 5 before and after CREATE INDEX ix_cust ON orders(customer_id), then for SELECT customer_id, order_id (covering), SELECT ... ORDER BY amount, SELECT DISTINCT status and GROUP BY status. Explain every wording you see (SCAN, SEARCH, USING INDEX, USING COVERING INDEX, USE TEMP B-TREE FOR ORDER BY / DISTINCT / GROUP BY), what the parenthesised (customer_id=?) tells you, that the plan text is for humans and its format may change between releases, and how the same ideas read in PostgreSQL (Seq Scan, Index Scan, Index Only Scan, Sort) and MySQL (type ALL versus ref, key, Using index, Using filesort), both described and not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** `EXPLAIN QUERY PLAN` shows how SQLite will read each table: `SCAN` means every row, `SEARCH ... USING INDEX (col=?)` means a B-tree lookup on that column, `COVERING INDEX` means the index alone answered the query, and `USE TEMP B-TREE FOR ...` means an extra sort or de-duplication step.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT,
                    status TEXT, amount REAL);
```
The Code block generates 20,000 customers and 200,000 orders with `random.seed(1)` (customer ids 1 to 20000, four statuses, dates in 2024). The table is too big to hand-check, so the Example below uses the plan lines themselves, which are small enough to read.

**SQL answer:** the statements are in the Code block: `EXPLAIN QUERY PLAN` is put in front of each query and the fourth column of each returned row is the human-readable detail. I print the plan for six queries, once before and once after `CREATE INDEX ix_cust ON orders(customer_id)`.

**pandas answer:** pandas has no planner. The nearest equivalents are a boolean mask (`df[df.customer_id == 5]`, a full scan) and a lookup on a real index (`df.set_index("customer_id").loc[[5]]`). Both are in the Code block and asserted equal to the SQL rows.

**Example:** reading the plan lines in the output below.
- `SCAN orders` is a full table scan: 200,000 rows visited to find 9 matches (about 600,000 VM steps, 3 per row).
- After the index, `SEARCH orders USING INDEX ix_cust (customer_id=?)` is a B-tree lookup: 99 VM steps for the same 9 rows. The text in brackets lists the index columns that take part in the lookup; `customer_id=?` means an equality lookup on `customer_id` (the `?` is the value, shown as a placeholder).
- `SELECT customer_id, order_id` becomes `USING COVERING INDEX`: the index stores `customer_id` and the rowid, and `order_id` is the rowid (an `INTEGER PRIMARY KEY`), so the table is never touched.
- `ORDER BY amount` with a lookup on `customer_id` is `SEARCH ... | USE TEMP B-TREE FOR ORDER BY`: the 9 rows are found by the index but `amount` is not in it, so SQLite sorts them in a temporary B-tree.
- `DISTINCT status` and `GROUP BY status` stay `SCAN orders | USE TEMP B-TREE FOR DISTINCT / GROUP BY` even after the new index, because that index does not contain `status`.
- `ORDER BY customer_id LIMIT 10` changes from `SCAN orders | USE TEMP B-TREE FOR ORDER BY` to `SCAN orders USING INDEX ix_cust`: reading the index in order gives sorted output, so the sort step disappears.

**Code:** run with `python3 -I`; the plan helper adds trailing spaces to the SQL text because Python's sqlite3 statement cache can replay a stale plan after `CREATE INDEX` or `DROP INDEX` on identical text (seen in the Wave A environment checks).
```python
# Q1: read EXPLAIN QUERY PLAN output on a 200,000-row orders table.
import random
import sqlite3
import pandas as pd

random.seed(1)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT,
                    status TEXT, amount REAL);
""")
cities = ["Pune", "Delhi", "Chennai", "Mumbai"]
con.executemany("INSERT INTO customers VALUES (?,?,?)",
                [(i, f"cust{i}", cities[i % 4]) for i in range(1, 20001)])
statuses = ["placed", "shipped", "delivered", "cancelled"]
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)",
                [(i, random.randint(1, 20000),
                  f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                  random.choice(statuses), round(random.uniform(10, 500), 2))
                 for i in range(1, 200001)])
con.commit()

_n = [0]
def plan(sql):
    # python's statement cache can replay a stale plan after DROP/CREATE INDEX, so vary the text
    _n[0] += 1
    rows = con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]).fetchall()
    return [r[3] for r in rows]

queries = {
    "A  filter":        "SELECT * FROM orders WHERE customer_id = 5",
    "B  covering":      "SELECT customer_id, order_id FROM orders WHERE customer_id = 5",
    "C  order by amt":  "SELECT * FROM orders WHERE customer_id = 5 ORDER BY amount",
    "D  distinct":      "SELECT DISTINCT status FROM orders",
    "E  group by":      "SELECT status, COUNT(*) FROM orders GROUP BY status",
    "F  order by cust": "SELECT * FROM orders ORDER BY customer_id LIMIT 10",
}
print("-- BEFORE CREATE INDEX")
for k, q in queries.items():
    print(k, "->", plan(q))
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
print("\n-- AFTER CREATE INDEX ix_cust ON orders(customer_id)")
for k, q in queries.items():
    print(k, "->", plan(q))

# the plan is a 4-column row: id, parent, notused, detail
print("\nraw row:", con.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 5 ").fetchall())

# a join, to show nested plan lines (parent column)
for r in con.execute("EXPLAIN QUERY PLAN SELECT c.name, o.amount FROM customers c "
                     "JOIN orders o ON o.customer_id = c.customer_id WHERE c.city = 'Pune'  "):
    print("join:", r)

# VM steps as a cost proxy
def steps(sql):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], rows
con.execute("DROP INDEX ix_cust")
s0, r0 = steps("SELECT * FROM orders WHERE customer_id = 5")
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
s1, r1 = steps("SELECT * FROM orders WHERE customer_id = 5")
print("\nVM steps scan:", s0, " with index:", s1, " rows:", len(r0), len(r1))

# pandas: boolean mask (scan) vs set_index + loc (index), same rows
df = pd.read_sql("SELECT * FROM orders", con)
mask = df[df.customer_id == 5].sort_values("order_id").reset_index(drop=True)
idx = df.set_index("customer_id").loc[[5]].reset_index().sort_values("order_id").reset_index(drop=True)
idx = idx[mask.columns]
pd.testing.assert_frame_equal(mask, idx)
sql_rows = pd.DataFrame(sorted(r1), columns=mask.columns)
pd.testing.assert_frame_equal(mask, sql_rows, check_dtype=False)
print("asserts passed (SQL rows, boolean mask and indexed loc equal after sorting by order_id)")
print("distinct statuses:", sorted(df.status.unique()), "vs SQL:", sorted(r[0] for r in con.execute("SELECT DISTINCT status FROM orders")))
```

**Output (my run):**
```text
-- BEFORE CREATE INDEX
A  filter -> ['SCAN orders']
B  covering -> ['SCAN orders']
C  order by amt -> ['SCAN orders', 'USE TEMP B-TREE FOR ORDER BY']
D  distinct -> ['SCAN orders', 'USE TEMP B-TREE FOR DISTINCT']
E  group by -> ['SCAN orders', 'USE TEMP B-TREE FOR GROUP BY']
F  order by cust -> ['SCAN orders', 'USE TEMP B-TREE FOR ORDER BY']

-- AFTER CREATE INDEX ix_cust ON orders(customer_id)
A  filter -> ['SEARCH orders USING INDEX ix_cust (customer_id=?)']
B  covering -> ['SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)']
C  order by amt -> ['SEARCH orders USING INDEX ix_cust (customer_id=?)', 'USE TEMP B-TREE FOR ORDER BY']
D  distinct -> ['SCAN orders', 'USE TEMP B-TREE FOR DISTINCT']
E  group by -> ['SCAN orders', 'USE TEMP B-TREE FOR GROUP BY']
F  order by cust -> ['SCAN orders USING INDEX ix_cust']

raw row: [(3, 0, 0, 'SEARCH orders USING INDEX ix_cust (customer_id=?)')]
join: (4, 0, 0, 'SCAN c')
join: (8, 0, 0, 'SEARCH o USING INDEX ix_cust (customer_id=?)')

VM steps scan: 600071  with index: 99  rows: 9 9
asserts passed (SQL rows, boolean mask and indexed loc equal after sorting by order_id)
distinct statuses: ['cancelled', 'delivered', 'placed', 'shipped'] vs SQL: ['cancelled', 'delivered', 'placed', 'shipped']
```

Comparison for the assert: rows from SQL, the boolean mask and the indexed `.loc` are all sorted by `order_id` before `assert_frame_equal`.

**Edge cases:**
- **Plan text is not a stable interface.** The SQLite documentation says the format may change between releases, so never parse it in production code; read it as a human, or use the VM-step count or timing as the test.
- **Stale plans.** After `DROP INDEX`, re-running exactly the same `EXPLAIN` text on the same connection can show the old plan (statement cache). Vary the text or reconnect.
- **`SCAN ... USING COVERING INDEX` is still a scan.** It reads the whole (smaller) index, not one key; only `SEARCH` with a bracketed condition is a seek.
- **Selectivity.** An index lookup for a value that matches most rows is not cheaper than a scan; the plan line looks the same, the VM steps do not.
- **Unselective `GROUP BY` and `DISTINCT`:** with four statuses the temp B-tree stays tiny; with a high-cardinality column it can be large.
- **Nested plans.** The raw rows have four columns (id, parent, unused, detail); the `parent` column nests lines, which is how a join shows `SCAN c` and `SEARCH o` as children of the same query.

**Then explain:**
- **SCAN** reads every row of the table (or every entry of an index). **SEARCH** uses a B-tree to jump to the matching entries.
- **USING INDEX** means the index finds the rows and then SQLite goes to the table for the other columns (two binary searches per row: index, then table by rowid). **USING COVERING INDEX** skips the table visit.
- **USE TEMP B-TREE FOR ORDER BY / DISTINCT / GROUP BY** means SQLite builds a temporary sorted structure in memory or on disk because no index delivers rows in that order.
- **PostgreSQL (described, not executed here):** `Seq Scan` is the scan, `Index Scan` is index lookup plus table fetch, `Index Only Scan` is the covering case, and `Sort` is the explicit sort; `EXPLAIN ANALYZE` also runs the query and adds actual times and row counts.
- **MySQL (described, not executed here):** `type: ALL` is a full scan, `type: ref` (or `range`) an index lookup, `key` names the index chosen, `Using index` is a covering index and `Using filesort` is an explicit sort (it does not necessarily mean a file on disk).

**Follow-ups:**
- *How do you know an index helped?* The plan changes from `SCAN` to `SEARCH`, and the cost proxy drops (here from about 600,000 to 99 VM steps); on a real server compare actual runtime and rows examined, not the plan alone.
- *Does `SELECT *` ever use a covering index?* Only if the index contains every column the query needs; with `SELECT *` that means every column, so rarely.
- *What does `EXPLAIN` without `QUERY PLAN` show in SQLite?* The raw bytecode program; the VM-step counts above count the instructions of that program as they execute.

**Common mistakes:**
- Treating `SCAN ... USING COVERING INDEX` as an index seek.
- Assuming an index exists in use because it exists in the schema; only the plan shows use.
- Reading plan text from a stale cached statement after changing indexes.
- Quoting plan wording as if it were the same across SQLite, PostgreSQL and MySQL.

### Q2 ⭐⭐⭐ 🟢 What does an index buy you and what does it cost? Using orders(order_id, customer_id, order_date, status, amount) with 100,000 seeded rows, show by running that a lookup WHERE customer_id = 5 costs about 300,000 SQLite VM steps as a scan (count them with Connection.set_progress_handler) and a few dozen with an index, and that inserting 100,000 rows costs more VM steps and more time with 0, 1, 2 and 3 indexes (timings labelled machine-specific). Report page_count and the index size (dbstat, or page_count before and after CREATE INDEX). Explain the two binary searches per matched row, the lookup-versus-write trade-off, when NOT to add an index (tiny table, low-selectivity column, write-heavy table, an index that is a prefix of another) and why 'always index every column' is wrong.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** An index turns a read of every row into a few B-tree steps (here about 300,000 VM steps down to 89), and you pay for it on every write, in extra VM steps, time and disk pages, so index the columns your real queries filter, join and sort on, not every column.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL);
CREATE INDEX i1 ON orders(customer_id);
CREATE INDEX i2 ON orders(order_date);
CREATE INDEX i3 ON orders(status, amount);
```
100,000 rows generated with `random.seed(2)` in the Code block (customer ids 1 to 20000, so about 5 orders per customer; customer 5 happens to have 8).

**SQL answer:** the lookup is `SELECT * FROM orders WHERE customer_id = 5`, counted twice (without and with `i1`), plus the covering form `SELECT customer_id, order_id FROM orders WHERE customer_id = 5`. The write test inserts the same 100,000 rows into four fresh databases that have 0, 1, 2 and 3 of the indexes above. All statements are in the Code block.

**pandas answer:** a boolean mask `df[df.customer_id == 5]` reads every row (the scan); after sorting once by the key, `s.customer_id.searchsorted(5, "left")` and `searchsorted(5, "right")` find the matching slice by binary search (the index). The sort is the "index build cost" and is paid once; both are asserted equal to the SQL rows in the Code block.

**Example:** hand-check the lookup cost. A scan visits 100,000 rows at about 3 VM instructions per row, which is the 300,064 steps in the output (the 64 extra are the setup and the 8 returned rows). With `i1`, SQLite does one binary search in the index B-tree to find the first entry with `customer_id = 5`, reads the 8 consecutive entries, and for each does a second binary search in the table B-tree by rowid. That is the "two binary searches per matched row" cost: 89 steps in total, 49 when the index covers the query and the table search is skipped. For writes, each `INSERT` must also insert one entry into every index. The step counts rise from 1,600,006 (no index) to 2,200,006, 2,700,006 and 3,300,006, roughly 5 to 6 extra VM steps per row per index, and the file grows from 977 pages to 2,463 pages.

**Code:** run with `python3 -I`. The timings column is wall-clock time on my machine and is machine-specific; the VM-step and page numbers are deterministic for this seed.
```python
# Q2: what an index buys (lookup VM steps) and costs (insert VM steps, time, pages).
import random
import sqlite3
import time
import statistics
import pandas as pd

random.seed(2)
statuses = ["placed", "shipped", "delivered", "cancelled"]
rows = [(i, random.randint(1, 20000),
         f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
         random.choice(statuses), round(random.uniform(10, 500), 2))
        for i in range(1, 100001)]
DDL = "CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, order_date TEXT, status TEXT, amount REAL)"
INDEXES = ["CREATE INDEX i1 ON orders(customer_id)",
           "CREATE INDEX i2 ON orders(order_date)",
           "CREATE INDEX i3 ON orders(status, amount)"]

def count_steps(con, sql, args=()):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(sql, args).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], out

# 1. lookup: scan versus index
con = sqlite3.connect(":memory:")
con.execute(DDL)
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
q = "SELECT * FROM orders WHERE customer_id = 5"
s_scan, r_scan = count_steps(con, q)
con.execute(INDEXES[0])
s_idx, r_idx = count_steps(con, q)
s_cov, _ = count_steps(con, "SELECT customer_id, order_id FROM orders WHERE customer_id = 5")
print("rows matched:", len(r_scan), "| VM steps scan:", s_scan, "index:", s_idx, "covering:", s_cov)
assert sorted(r_scan) == sorted(r_idx)

# 2. write cost with 0..3 indexes
res = []
for k in range(4):
    c = sqlite3.connect(":memory:")
    c.execute(DDL)
    for ddl in INDEXES[:k]:
        c.execute(ddl)
    cnt = [0]
    def cb():
        cnt[0] += 1
        return 0
    times = []
    c.set_progress_handler(cb, 1)
    t = time.perf_counter()
    c.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
    c.commit()
    times.append(time.perf_counter() - t)
    c.set_progress_handler(None, 0)
    pages = c.execute("PRAGMA page_count").fetchone()[0]
    res.append((k, cnt[0], round(times[0] * 1000), pages))
out = pd.DataFrame(res, columns=["indexes", "vm_steps", "insert_ms_machine_specific", "page_count"])
print(out.to_string(index=False))

# 3. size of the table and each index (dbstat), page size 4096
con.execute("CREATE INDEX i2 ON orders(order_date)")
con.execute("CREATE INDEX i3 ON orders(status, amount)")
for name, nbytes, npages in con.execute(
        "SELECT name, SUM(pgsize), COUNT(*) FROM dbstat WHERE name IN ('orders','i1','i2','i3') GROUP BY name ORDER BY name"):
    print(f"{name:7s} {npages:5d} pages {nbytes:9d} bytes")
print("page_size", con.execute("PRAGMA page_size").fetchone()[0])

# pandas analogue: a boolean mask scans every row; a sorted index finds them by binary search
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "order_date", "status", "amount"])
m = df[df.customer_id == 5].sort_values("order_id").reset_index(drop=True)
s = df.sort_values("customer_id", kind="stable")
lo, hi = s.customer_id.searchsorted(5, "left"), s.customer_id.searchsorted(5, "right")
via_sorted = s.iloc[lo:hi].sort_values("order_id").reset_index(drop=True)
pd.testing.assert_frame_equal(m, via_sorted)
pd.testing.assert_frame_equal(m, pd.DataFrame(sorted(r_idx), columns=m.columns), check_dtype=False)
print("asserts passed: SQL scan, SQL index, pandas mask and sorted searchsorted give the same rows (sorted by order_id)")
```

**Output (my run):**
```text
rows matched: 8 | VM steps scan: 300064 index: 89 covering: 49
 indexes  vm_steps  insert_ms_machine_specific  page_count
       0   1600006                         293         977
       1   2200006                         432        1266
       2   2700006                         540        1779
       3   3300006                         753        2463
i1        262 pages   1073152 bytes
i2        460 pages   1884160 bytes
i3        625 pages   2560000 bytes
orders    976 pages   3997696 bytes
page_size 4096
asserts passed: SQL scan, SQL index, pandas mask and sorted searchsorted give the same rows (sorted by order_id)
```

Comparison for the assert: SQL scan rows, SQL indexed rows, the pandas mask and the `searchsorted` slice are sorted by `order_id` before being compared.

**Edge cases:**
- **Timings are noisy.** Insert time rose with each index in my run (see the `insert_ms_machine_specific` column), but a single run on a laptop is not a benchmark; the VM-step count is the stable evidence.
- **The step counter is a proxy.** It counts SQLite virtual-machine instructions, not disk reads; on a big table that does not fit in memory the I/O difference between scan and index is larger than the instruction counts suggest.
- **An index entry is not free to maintain on UPDATE.** Updating an indexed column deletes and re-inserts the index entry; updating an unindexed column does not touch it.
- **Page counts include free space.** `page_count` after bulk insert is the high-water mark; deleting rows does not shrink the file until `VACUUM`.
- **Low-selectivity columns.** An index on `status` (4 values) would find 25,000 rows per value; reading them by rowid one at a time can cost more than one scan.

**Then explain:**
- **What it buys:** an equality or range lookup in O(log n) steps plus the matching rows, ordered output without a sort, and a covering read that skips the table.
- **What it costs:** extra disk space (`i3` here is 625 pages, about 64 percent of the table's 976), slower `INSERT`, `UPDATE` and `DELETE`, and more work for the planner and for `VACUUM`/backup.
- **When NOT to add one:** a tiny table (a scan is one or two pages), a low-selectivity column (booleans, status flags) used alone, a write-heavy table where reads are rare, and an index that is a left prefix of an existing composite index (`(a)` when `(a, b)` exists; Q4 shows why the longer index already serves it).
- **Why "index everything" is wrong:** every index multiplies write cost and storage, most will never be chosen by the planner, and the planner can only use one or two per table per query, so unused indexes are pure cost.
- **Other engines (not executed here):** PostgreSQL and MySQL show the same trade-off, plus index bloat and vacuum or replication costs; I have not measured them.

**Follow-ups:**
- *How do you find unused indexes?* In SQLite you can only check the plans of your real queries; PostgreSQL has `pg_stat_user_indexes` and MySQL has the `sys` schema views (described, not executed here).
- *Is a unique index different?* It also enforces a rule; the lookup benefit is the same, and the write cost includes the uniqueness check.
- *Would a bulk load be faster if you build the index afterward?* Usually yes: one sorted build is cheaper than many random inserts. I did not measure it here.

**Common mistakes:**
- Quoting one timing as proof, with no repeat or no step count.
- Counting only the read benefit.
- Adding `(a)` and `(a, b)` both, leaving the shorter one redundant.
- Indexing a column with two or three distinct values and expecting a speed-up.

### Q3 ⭐⭐⭐ 🟡 Sargability: events(event_id, user_id, event_time TEXT 'YYYY-MM-DD HH:MM:SS', event_type, payload) with 300,000 rows and an index on event_time. For each of these predicates print the plan and say whether the index can be used: strftime('%Y-%m', event_time) = '2024-03', substr(event_time,1,7) = '2024-03', date(event_time) = '2024-03-05', event_time LIKE '2024-03%', COALESCE(event_time,'x') = ..., user_id + 0 = 5, and the rewrite event_time >= '2024-03-01' AND event_time < '2024-04-01'. Explain why a function on the column hides the index (the planner would need the function's value for every row), the half-open range rewrite that also works for timestamps, and the alternative of an expression index on the exact same expression. Hedge YEAR(), DATE_TRUNC and CAST(... AS DATE) behaviour in MySQL, PostgreSQL, SQL Server, BigQuery and Snowflake as not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** An index is sorted by the stored column value, so a predicate must compare the bare column to a constant for the planner to jump into it; wrap the column in a function and SQLite must compute the function for every row, so it scans (1.2 million VM steps here, against 2,464 for the half-open range on one day).

**Schema and sample data:**
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INT, event_time TEXT, event_type TEXT, payload TEXT);
CREATE INDEX ix_time ON events(event_time);
CREATE INDEX ix_user ON events(user_id);
```
300,000 rows with `random.seed(3)`: `event_time` is a random second in 2024 in the form `'2024-03-05 10:00:00'`, `user_id` is 1 to 5000. I added `ix_user` so the `user_id + 0` case has an index to hide.

**SQL answer:** eight `WHERE` forms, each run as `SELECT COUNT(*)` and as `SELECT *` (the plans differ in a useful way, see Edge cases). The three March predicates and the half-open range are in the Code block as `preds`; the winning rewrite is
`event_time >= '2024-03-01' AND event_time < '2024-04-01'`.

**pandas answer:** compare the string column directly (`df.event_time >= "2024-03-01"` and `< "2024-04-01"`), which is the pandas form of the same range; the function form is `pd.to_datetime(df.event_time).dt.strftime("%Y-%m") == "2024-03"`, and `searchsorted` on the sorted column plays the part of the index. All three are asserted to give the same count in the Code block.

**Example:** `strftime('%Y-%m', event_time) = '2024-03'` asks "what is the month of every row?", but the index is sorted by the raw text `'2024-01-01 00:00:03'`, not by month text, so SQLite cannot binary-search for `'2024-03'`; it must evaluate `strftime` on every entry. In the output, each function form took 1.2 million VM steps (4 per row), and only the bare-column forms searched. For one day, the function form `date(event_time) = '2024-03-05'` costs 1,200,826 steps and the range form `event_time >= '2024-03-05' AND event_time < '2024-03-06'` costs 2,464 steps; both return the same 815 rows.

**Code:** run with `python3 -I`.
```python
# Q3: sargability. Plans and VM steps for predicates on event_time (indexed) and user_id.
import random
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

random.seed(3)
base = datetime(2024, 1, 1)
rows = []
for i in range(1, 300001):
    t = base + timedelta(seconds=random.randint(0, 365 * 86400 - 1))
    rows.append((i, random.randint(1, 5000), t.strftime("%Y-%m-%d %H:%M:%S"),
                 random.choice(["view", "click", "buy"]), "x"))
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INT, event_time TEXT, event_type TEXT, payload TEXT)")
con.executemany("INSERT INTO events VALUES (?,?,?,?,?)", rows)
con.execute("CREATE INDEX ix_time ON events(event_time)")
con.execute("CREATE INDEX ix_user ON events(user_id)")
con.commit()

_n = [0]
def plan(where, sel="COUNT(*)"):
    _n[0] += 1
    sql = f"SELECT {sel} FROM events WHERE {where}"
    return con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]).fetchall()[0][3]

def steps(where):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    n = con.execute(f"SELECT COUNT(*) FROM events WHERE {where}").fetchone()[0]
    con.set_progress_handler(None, 0)
    return c[0], n

preds = [
    ("strftime",   "strftime('%Y-%m', event_time) = '2024-03'"),
    ("substr",     "substr(event_time,1,7) = '2024-03'"),
    ("date()",     "date(event_time) = '2024-03-05'"),
    ("LIKE",       "event_time LIKE '2024-03%'"),
    ("COALESCE",   "COALESCE(event_time,'x') = '2024-03-05 10:00:00'"),
    ("user_id+0",  "user_id + 0 = 5"),
    ("user_id=5",  "user_id = 5"),
    ("range",      "event_time >= '2024-03-01' AND event_time < '2024-04-01'"),
]
res = []
for name, w in preds:
    s, n = steps(w)
    res.append((name, plan(w), plan(w, "*"), s, n))
pd.set_option("display.width", 250)
print(pd.DataFrame(res, columns=["predicate", "plan COUNT(*)", "plan SELECT *", "vm_steps", "count"]).to_string(index=False))

# the three March predicates must agree on the count
c1 = steps("strftime('%Y-%m', event_time) = '2024-03'")[1]
c2 = steps("event_time >= '2024-03-01' AND event_time < '2024-04-01'")[1]
c3 = steps("event_time LIKE '2024-03%'")[1]
assert c1 == c2 == c3
print("March counts equal:", c1, c2, c3)

# timestamps: date = '2024-03-05' as a half-open range
a = steps("date(event_time) = '2024-03-05'")
b = steps("event_time >= '2024-03-05' AND event_time < '2024-03-06'")
assert a[1] == b[1]
print("one day: function form", a, "range form", b, "plan:", plan("event_time >= '2024-03-05' AND event_time < '2024-03-06'"))
# the closed-range trap: BETWEEN '2024-03-05' AND '2024-03-05' on timestamps returns 0 rows
print("BETWEEN '2024-03-05' AND '2024-03-05' count:", steps("event_time BETWEEN '2024-03-05' AND '2024-03-05'")[1])

# expression index on the exact expression
con.execute("CREATE INDEX ix_month ON events(strftime('%Y-%m', event_time))")
print("with expression index:", plan("strftime('%Y-%m', event_time) = '2024-03'"), steps("strftime('%Y-%m', event_time) = '2024-03'"))
print("same idea, different expression (substr):", plan("substr(event_time,1,7) = '2024-03'"))
print("strftime('%Y', ...) with the month index:", plan("strftime('%Y', event_time) = '2024'"))

# pandas: string compare on a sorted column is a range; the function form touches every row
df = pd.DataFrame(rows, columns=["event_id", "user_id", "event_time", "event_type", "payload"])
m_range = df[(df.event_time >= "2024-03-01") & (df.event_time < "2024-04-01")]
m_func = df[pd.to_datetime(df.event_time).dt.strftime("%Y-%m") == "2024-03"]
assert len(m_range) == len(m_func) == c2
s = df.sort_values("event_time")
lo, hi = s.event_time.searchsorted("2024-03-01", "left"), s.event_time.searchsorted("2024-04-01", "left")
assert hi - lo == c2
print("pandas: mask, to_datetime+strftime and searchsorted all give", c2)
```

**Output (my run):**
```text
predicate                                                              plan COUNT(*)                                                     plan SELECT *  vm_steps  count
 strftime                                   SCAN events USING COVERING INDEX ix_time                                                       SCAN events   1225359  25345
   substr                                   SCAN events USING COVERING INDEX ix_time                                                       SCAN events   1225360  25345
   date()                                   SCAN events USING COVERING INDEX ix_time                                                       SCAN events   1200828    815
     LIKE                                   SCAN events USING COVERING INDEX ix_time                                                       SCAN events   1225358  25345
 COALESCE                                   SCAN events USING COVERING INDEX ix_time                                                       SCAN events   1200013      0
user_id+0                                   SCAN events USING COVERING INDEX ix_user                                                       SCAN events   1200072     58
user_id=5                     SEARCH events USING COVERING INDEX ix_user (user_id=?)                     SEARCH events USING INDEX ix_user (user_id=?)       187     58
    range SEARCH events USING COVERING INDEX ix_time (event_time>? AND event_time<?) SEARCH events USING INDEX ix_time (event_time>? AND event_time<?)     76054  25345
March counts equal: 25345 25345 25345
one day: function form (1200826, 815) range form (2464, 815) plan: SEARCH events USING COVERING INDEX ix_time (event_time>? AND event_time<?)
BETWEEN '2024-03-05' AND '2024-03-05' count: 0
with expression index: SEARCH events USING INDEX ix_month (<expr>=?) (101395, 25345)
same idea, different expression (substr): SCAN events USING COVERING INDEX ix_time
strftime('%Y', ...) with the month index: SCAN events USING COVERING INDEX ix_time
pandas: mask, to_datetime+strftime and searchsorted all give 25345
```

Comparison for the assert: the three March predicates must return the same count (25,345), the one-day function and range forms the same count (815), and the pandas mask, the `to_datetime` form and `searchsorted` the same count as SQL.

**Edge cases:**
- **`SCAN ... USING COVERING INDEX` for `COUNT(*)`.** The plan column for `COUNT(*)` says `SCAN events USING COVERING INDEX ix_time` for the function forms: SQLite walked the whole (narrow) index instead of the wide table. That is still a scan, not a seek, which the `vm_steps` column confirms (about 1.2 million). The `SELECT *` column shows the plain `SCAN events`.
- **`LIKE '2024-03%'` did not use the index** (plain `SCAN`), the same trap as Q6: `LIKE` is case-insensitive and the index is BINARY, so the prefix cannot become a range.
- **Closed ranges on timestamps.** `BETWEEN '2024-03-05' AND '2024-03-05'` returned 0 rows because every real timestamp is greater than `'2024-03-05'`; `BETWEEN` includes the upper end, which is why the half-open form (`>= start AND < next_start`) is the safe habit.
- **The `COALESCE` row** uses a literal that matches nothing, so its count is 0; the point is its plan.
- **Result-equal does not mean cost-equal.** All three March predicates returned 25,345 rows; they differ only in cost.
- **Selectivity:** March is 8 percent of the table; the range plan took 76,054 steps because it still walks about 25,000 index entries and fetches those rows for `SELECT *`.
- **NULLs:** rows with NULL `event_time` match neither form; the sample has none.

**Then explain:**
- **Why a function hides the index:** the index stores the column, not `f(column)`. To use it, the planner would need `f(column)` for every row, which is the scan. Only a bare column compared with a constant (`=`, `<`, `>`, `BETWEEN`, `IN`, a LIKE prefix under the right conditions) can seek.
- **Half-open range rewrite:** `>= first_instant AND < next_period_start` works for dates, timestamps, and sub-second values, with no end-of-day trick like `23:59:59`.
- **Expression index:** `CREATE INDEX ix_month ON events(strftime('%Y-%m', event_time))` made the same predicate `SEARCH events USING INDEX ix_month (<expr>=?)`. It only helps when the query repeats the exact expression: `substr(event_time,1,7)` and `strftime('%Y', event_time)` still scanned. It costs an extra index to maintain (Q2).
- **`user_id + 0 = 5`** scanned although `user_id = 5` searched (187 steps against 1,200,072); `+ 0` is a known SQLite trick for switching an index off on purpose.
- **Other engines (not executed here):** MySQL `WHERE YEAR(col) = 2024` and PostgreSQL `date_trunc('month', col) = ...` or `col::date = ...` are generally non-sargable on a plain index in the same way; PostgreSQL supports expression indexes, MySQL 8 has functional indexes, for SQL Server and `CAST(col AS DATE)` I would check the plan rather than assume either way; BigQuery and Snowflake do not use B-tree indexes and prune partitions or micro-partitions, where the same advice (filter the raw column) still applies. I did not run any of these.

**Follow-ups:**
- *Does `col LIKE 'abc%'` use an index?* Depends on collation and engine; in SQLite only with a NOCASE index or `case_sensitive_like` (Q6).
- *How do you filter by month from a calendar table instead?* Join the month's start and end dates from a small table, then use the range.
- *Could you store the month in its own column?* Yes (a generated or maintained column plus an ordinary index), at the cost of storage and maintenance.

**Common mistakes:**
- `WHERE strftime(...) = ...`, `WHERE YEAR(col) = ...` or `WHERE DATE(col) = ...` on a large table.
- `BETWEEN '2024-03-01' AND '2024-03-31'` on timestamps, which drops all of 31 March after midnight.
- Creating an expression index but writing the query with a slightly different expression.
- Reading `SCAN ... COVERING INDEX` as a seek.

### Q4 ⭐⭐⭐ 🟡 Composite indexes and the leftmost-prefix rule: orders(order_id, customer_id, status, order_date, amount) with 200,000 rows and a single index ix(customer_id, status, order_date). For about ten predicates (customer_id=?; customer_id=? AND status=?; status=? alone; order_date range alone; customer_id=? AND order_date>?; customer_id>? AND status=?; customer_id=? AND status IN (...) AND order_date>?; ORDER BY only) print the plan and say which columns of the index each one uses and why (equality columns, then at most one range column, then nothing further; no gaps). Show that SQLite can skip-scan a missing leading column only after ANALYZE and when the leading column has few distinct values, and say PostgreSQL's multicolumn B-tree rule and MySQL's key_len reading are the same idea (described, not executed).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; PostgreSQL docs using-explain and indexes-multicolumn and MySQL EXPLAIN output page (opened, used for contrast only); official documentation, not candidate reports; product company and GCC data engineer rounds
**Say this first (1 line):** A composite index `(a, b, c)` is sorted by `a`, then `b` within `a`, then `c` within `b`, so a query can use equality on the leading columns, then at most one range column, and nothing after the first range or gap: here `customer_id = 5` alone or with `status` seeks, `status` alone or `order_date` alone scans.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL);
CREATE INDEX ix ON orders(customer_id, status, order_date);
```
200,000 rows from `random.seed(4)`, with 20,000 customers, four statuses and dates in 2024. I use a second table `o2` with an index `(status, order_date)` for the skip-scan demonstration, and `o3` with `(customer_id, order_date)` as the high-cardinality contrast.

**SQL answer:** nine `WHERE` forms plus four `ORDER BY` forms against `ix`, all listed in the Code block under `tests` and in the ORDER BY section.

**pandas answer:** the analogue is a sorted `MultiIndex`: `mi = df.set_index(["customer_id", "status", "order_date"]).sort_index()` then `mi.loc[(5, "placed")]` selects by leading levels; it cannot cheaply select by the second level alone. Asserted equal to the SQL ids and to the boolean mask in the Code block.

**Example:** think of `ix` as a phone book sorted by customer, then status, then date. The plan line `(customer_id=? AND status=?)` for `customer_id = 5 AND status = 'placed'` means: jump to customer 5, then within customer 5 jump to `placed`, 22 steps, 1 row. `status = 'placed'` alone gives `SCAN orders` (947,740 steps): the matching entries are scattered through all 20,000 customers, so there is no single place to jump to. `customer_id = 5 AND order_date > '2024-06-01'` uses only `customer_id=?` (85 steps): `status` is missing, so the search cannot go further than the gap, and `order_date` is only checked afterwards on each of the customer's entries. `customer_id = 5 AND status IN ('placed','shipped') AND order_date > '2024-06-01'` uses all three columns (`customer_id=? AND status=? AND order_date>?`, 54 steps): the `IN` is treated as a few equality probes, so the range on the third column still works.

**Code:** run with `python3 -I`.
```python
# Q4: composite index ix(customer_id, status, order_date): which columns does each predicate use?
import random
import sqlite3
import pandas as pd

random.seed(4)
statuses = ["placed", "shipped", "delivered", "cancelled"]
rows = [(i, random.randint(1, 20000), random.choice(statuses),
         f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", round(random.uniform(10, 500), 2))
        for i in range(1, 200001)]
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
con.execute("CREATE INDEX ix ON orders(customer_id, status, order_date)")
con.commit()

_n = [0]
def plan(where, order=""):
    _n[0] += 1
    w = f"WHERE {where} " if where else ""
    rows_ = con.execute(f"EXPLAIN QUERY PLAN SELECT * FROM orders {w}{order}" + " " * _n[0]).fetchall()
    return " | ".join(r[3] for r in rows_)

def steps(sql):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    n = len(con.execute(sql).fetchall())
    con.set_progress_handler(None, 0)
    return c[0], n

tests = [
    ("customer_id=5",                                   "customer_id = 5"),
    ("customer_id=5 AND status",                        "customer_id = 5 AND status = 'placed'"),
    ("all three equal",                                 "customer_id = 5 AND status = 'placed' AND order_date = '2024-03-05'"),
    ("status alone",                                    "status = 'placed'"),
    ("order_date range alone",                          "order_date >= '2024-03-01' AND order_date < '2024-04-01'"),
    ("customer_id=5 AND order_date>? (gap)",            "customer_id = 5 AND order_date > '2024-06-01'"),
    ("customer_id>? AND status=?",                      "customer_id > 19900 AND status = 'placed'"),
    ("cust=5 AND status IN AND date>",                  "customer_id = 5 AND status IN ('placed','shipped') AND order_date > '2024-06-01'"),
    ("cust=5 AND status>? AND date>?",                  "customer_id = 5 AND status > 'a' AND order_date > '2024-06-01'"),
]
rowsout = []
for name, w in tests:
    s, n = steps(f"SELECT * FROM orders WHERE {w}")
    rowsout.append((name, plan(w), s, n))
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 90)
print(pd.DataFrame(rowsout, columns=["predicate", "plan", "vm_steps", "rows"]).to_string(index=False))

print("\nORDER BY only:")
print("ORDER BY customer_id, status, order_date LIMIT 5 ->", plan("", "ORDER BY customer_id, status, order_date LIMIT 5"))
print("ORDER BY status LIMIT 5 ->", plan("", "ORDER BY status LIMIT 5"))
print("cust=5 ORDER BY status, order_date ->", plan("customer_id = 5", "ORDER BY status, order_date"))
print("cust=5 ORDER BY order_date ->", plan("customer_id = 5", "ORDER BY order_date"))

# skip-scan: leading column with few distinct values, only after ANALYZE
con.execute("CREATE TABLE o2 AS SELECT * FROM orders")
con.execute("CREATE INDEX ix2 ON o2(status, order_date)")
def plan2(sql):
    _n[0] += 1
    return con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]).fetchall()[0][3]
q = "SELECT * FROM o2 WHERE order_date = '2024-03-05'"
print("\nskip-scan before ANALYZE:", plan2(q), steps(q))
con.execute("ANALYZE")
print("stat1:", con.execute("SELECT idx, stat FROM sqlite_stat1 WHERE tbl='o2'").fetchall())
print("skip-scan after ANALYZE: ", plan2(q), steps(q))
# a high-cardinality leading column: no skip-scan
con.execute("CREATE TABLE o3 AS SELECT * FROM orders")
con.execute("CREATE INDEX ix3 ON o3(customer_id, order_date)")
con.execute("ANALYZE")
print("high-cardinality leading column:", plan2("SELECT * FROM o3 WHERE order_date = '2024-03-05'"))

# pandas: groupby/filter on a MultiIndex needs the leading levels in order
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "order_date", "amount"])
mi = df.set_index(["customer_id", "status", "order_date"]).sort_index()
a = mi.loc[(5, "placed")].reset_index()
b = df[(df.customer_id == 5) & (df.status == "placed")]
assert sorted(a.order_id) == sorted(b.order_id)
sqlids = sorted(r[0] for r in con.execute("SELECT order_id FROM orders WHERE customer_id=5 AND status='placed'"))
assert sqlids == sorted(b.order_id)
print("\npandas MultiIndex .loc[(5,'placed')] rows:", len(a), "| same as mask and SQL (sorted order_id): True")
```

**Output (my run):**
```text
                           predicate                                                                       plan  vm_steps  rows
                       customer_id=5                               SEARCH orders USING INDEX ix (customer_id=?)        99     9
            customer_id=5 AND status                  SEARCH orders USING INDEX ix (customer_id=? AND status=?)        22     1
                     all three equal SEARCH orders USING INDEX ix (customer_id=? AND status=? AND order_date=?)        16     0
                        status alone                                                                SCAN orders    947740 49676
              order_date range alone                                                                SCAN orders   1048224 16510
customer_id=5 AND order_date>? (gap)                               SEARCH orders USING INDEX ix (customer_id=?)        85     4
          customer_id>? AND status=?                               SEARCH orders USING INDEX ix (customer_id>?)      5636   248
      cust=5 AND status IN AND date> SEARCH orders USING INDEX ix (customer_id=? AND status=? AND order_date>?)        54     1
      cust=5 AND status>? AND date>?                  SEARCH orders USING INDEX ix (customer_id=? AND status>?)        90     4

ORDER BY only:
ORDER BY customer_id, status, order_date LIMIT 5 -> SCAN orders USING INDEX ix
ORDER BY status LIMIT 5 -> SCAN orders | USE TEMP B-TREE FOR ORDER BY
cust=5 ORDER BY status, order_date -> SEARCH orders USING INDEX ix (customer_id=?)
cust=5 ORDER BY order_date -> SEARCH orders USING INDEX ix (customer_id=?) | USE TEMP B-TREE FOR ORDER BY

skip-scan before ANALYZE: SCAN o2 (604089, 583)
stat1: [('ix2', '200000 50000 149')]
skip-scan after ANALYZE:  SEARCH o2 USING INDEX ix2 (ANY(status) AND order_date=?) (5868, 583)
high-cardinality leading column: SCAN o3

pandas MultiIndex .loc[(5,'placed')] rows: 1 | same as mask and SQL (sorted order_id): True
```

Comparison for the assert: the pandas `MultiIndex` selection, the pandas mask and the SQL order ids are all sorted by `order_id` first.

**Edge cases:**
- **A range on a column ends the prefix.** `customer_id > 19900 AND status = 'placed'` used only `(customer_id>?)`; the equality on `status` was applied row by row afterwards, so it examined all customers above 19,900 (5,636 steps for 248 rows). `customer_id = 5 AND status > 'a' AND order_date > '...'` used `(customer_id=? AND status>?)` and stopped there.
- **`ORDER BY` can use the index too.** `ORDER BY customer_id, status, order_date LIMIT 5` is `SCAN orders USING INDEX ix` with no sort; `ORDER BY status` needs `USE TEMP B-TREE FOR ORDER BY`. With `customer_id = 5` fixed, `ORDER BY status, order_date` needs no sort (the equality prefix pins the first column), while `ORDER BY order_date` does need one (there is a gap at `status`).
- **Skip-scan.** On `o2` with index `(status, order_date)` and `WHERE order_date = '2024-03-05'`: before `ANALYZE` the plan was `SCAN o2` (604,089 steps); after `ANALYZE` it was `SEARCH o2 USING INDEX ix2 (ANY(status) AND order_date=?)` (5,868 steps). `sqlite_stat1` held `200000 50000 149` (4 distinct values of the leading column). On `o3` with a high-cardinality leading column (`customer_id`), even after `ANALYZE` the plan stayed `SCAN o3`, because skip-scan only pays when the leading column has few distinct values.
- **Skip-scan is not a general solution.** It costs one probe per distinct leading value; it is an optimisation for a handful of values, not a way to avoid designing the index.
- **Column order for equality columns** does not matter within one query (the planner reorders `AND` terms), but it matters across queries: put the columns used by the most queries first.

**Then explain:**
- **The rule:** equality columns (including `IN` lists) from the left with no gaps, then one range column, then nothing. This is the same as a sorted phone book: you cannot find "all Raos" without knowing the first name's range.
- **What each tested predicate used:** `customer_id=?` (1 column); `customer_id=? AND status=?` (2); all three equal (3); `status` alone (0, scan); date range alone (0, scan); `customer_id=?` and `order_date>?` (1, gap); `customer_id>?` and `status=?` (1, range column ends the prefix); `customer_id=? AND status IN AND order_date>` (3); `customer_id=? AND status>? AND order_date>?` (2).
- **PostgreSQL (described, not executed here):** its multicolumn B-tree has the same prefix idea, with the leading column's condition limiting how much of the index is scanned efficiently. The docs I opened describe a newer skip-scan capability in one version; I do not state which versions have it.
- **MySQL (described, not executed here):** `EXPLAIN` shows `key_len`, the number of bytes of the index key used, so a short `key_len` against the full index length tells you only a prefix is in play; same idea as the bracket text in the SQLite plan.

**Follow-ups:**
- *Would you add a separate index on `status`?* Only if `status`-only queries matter and are selective; otherwise it costs writes (Q2).
- *Does the order of the `WHERE` terms matter?* No, the planner matches terms to index columns; the order of the columns in the index does.
- *Is `(a, b)` redundant if you already have `(a, b, c)`?* Yes for lookups; keep it only if its smaller size matters.

**Common mistakes:**
- Putting a range column before equality columns.
- Assuming `WHERE b = ?` can use `(a, b)`.
- Believing skip-scan is available without `ANALYZE`; in my run it was not.
- Putting the highest-cardinality column first by reflex without checking the queries.

### Q5 ⭐⭐⭐ 🟡 Design one composite index for one query: orders(order_id, customer_id, status, order_date, amount) with 200,000 rows and the query SELECT order_id, amount FROM orders WHERE status = 'shipped' AND order_date >= '2024-06-01' AND order_date < '2024-07-01' ORDER BY order_date LIMIT 50, and a second query WHERE customer_id = ? ORDER BY order_date DESC LIMIT 10. Compare (status), (order_date), (order_date, status), (status, order_date) and (status, order_date, amount, order_id) by printing plans and counting VM steps. State the rule (equality columns first, then the range or sort column, then covering columns), why putting the highest-cardinality column first is a heuristic and not the rule, why one equality column before a range column removes the sort, and what happens to the ORDER BY when the range column is not the sort column.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Build the index in the order equality columns, then the range or sort column, then covering columns: for the first query that is `(status, order_date, amount, order_id)`, which dropped the cost from 780,147 VM steps (no index) to 370 and needs no sort and no table lookup.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL);
```
200,000 rows from `random.seed(5)`: 20,000 customers, four statuses, dates in 2024. For the first query, 4,182 rows match (shipped, June 2024); the first 50 in date order are all dated `2024-06-01` (about 150 orders a day), which matters for the LIMIT (Edge cases).

**SQL answer:** the two queries are `Q1` and `Q2` in the Code block:
`SELECT order_id, amount FROM orders WHERE status = 'shipped' AND order_date >= '2024-06-01' AND order_date < '2024-07-01' ORDER BY order_date LIMIT 50` and `SELECT * FROM orders WHERE customer_id = 5 ORDER BY order_date DESC LIMIT 10`. Each candidate index is created, planned, run with the VM-step counter and dropped.

**pandas answer:** the same selection is a mask on `status` and the date range, `sort_values(["order_date", "order_id"])` and `head(50)`; the `order_id` tiebreaker makes the 50 rows deterministic. The Code block asserts the pandas dates equal the first 50 dates from SQL.

**Example:** walk Query 1 against `(status, order_date)`. The index is sorted by status, then date. The `status = 'shipped'` equality picks one contiguous block; inside it the dates are sorted, so the range `>= '2024-06-01' AND < '2024-07-01'` is one contiguous slice, and that slice is already in `ORDER BY order_date` order. So SQLite reads the first 50 entries of the slice and stops: 421 steps, no temp B-tree. With `(order_date, status)` the range is first, so status becomes a per-row filter inside the whole month (2,812 steps). With `(status)` it finds all shipped rows (about 50,000), then must sort the month's rows (329,996 steps, with `USE TEMP B-TREE FOR ORDER BY`). With the covering `(status, order_date, amount, order_id)` the 50 rows come from the index alone (370 steps, `USING COVERING INDEX`).

**Code:** run with `python3 -I`.
```python
# Q5: design one composite index for one query; compare candidates by plan and VM steps.
import random
import sqlite3
import pandas as pd

random.seed(5)
statuses = ["placed", "shipped", "delivered", "cancelled"]
rows = [(i, random.randint(1, 20000), random.choice(statuses),
         f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", round(random.uniform(10, 500), 2))
        for i in range(1, 200001)]
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
con.commit()

_n = [0]
def plan(sql):
    _n[0] += 1
    return " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]))

def run(sql, args=()):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(sql, args).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], out

Q1 = ("SELECT order_id, amount FROM orders WHERE status = 'shipped' AND order_date >= '2024-06-01' "
      "AND order_date < '2024-07-01' ORDER BY order_date LIMIT 50")
cands = [("none", None), ("(status)", "status"), ("(order_date)", "order_date"),
         ("(order_date, status)", "order_date, status"), ("(status, order_date)", "status, order_date"),
         ("(status, order_date, amount, order_id)", "status, order_date, amount, order_id")]
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 100)
out = []
ref = None
for name, cols in cands:
    con.execute("DROP INDEX IF EXISTS ixc")
    if cols:
        con.execute(f"CREATE INDEX ixc ON orders({cols})")
    s, r = run(Q1)
    # ties on order_date make LIMIT order ambiguous, so compare the set of (date) only through the count and the date column
    out.append((name, plan(Q1), s, len(r)))
print("Query 1:", Q1)
print(pd.DataFrame(out, columns=["index", "plan", "vm_steps", "rows"]).to_string(index=False))

# correctness: the result set is the same 50 dates whichever index is used; compare the sorted dates
con.execute("DROP INDEX IF EXISTS ixc")
full = con.execute("SELECT order_date, order_id, amount FROM orders WHERE status='shipped' AND order_date >= '2024-06-01' AND order_date < '2024-07-01' ORDER BY order_date, order_id").fetchall()
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "order_date", "amount"])
pm = df[(df.status == "shipped") & (df.order_date >= "2024-06-01") & (df.order_date < "2024-07-01")] \
       .sort_values(["order_date", "order_id"])
assert [r[1] for r in full] == list(pm.order_id)
print("matching rows without LIMIT:", len(full), "(SQL and pandas agree)")
print("first 50 dates only span:", full[0][0], "to", full[49][0], "-> ties on order_date mean LIMIT 50 is ambiguous without a tiebreaker")

# the second query
Q2 = "SELECT * FROM orders WHERE customer_id = 5 ORDER BY order_date DESC LIMIT 10"
out2 = []
for name, cols in [("none", None), ("(customer_id)", "customer_id"), ("(customer_id, order_date)", "customer_id, order_date"),
                   ("(order_date)", "order_date")]:
    con.execute("DROP INDEX IF EXISTS ixc")
    if cols:
        con.execute(f"CREATE INDEX ixc ON orders({cols})")
    s, r = run(Q2)
    out2.append((name, plan(Q2), s, len(r)))
print("\nQuery 2:", Q2)
print(pd.DataFrame(out2, columns=["index", "plan", "vm_steps", "rows"]).to_string(index=False))

# range column is not the sort column: status equal, date range, ORDER BY amount
Q3 = ("SELECT order_id FROM orders WHERE status = 'shipped' AND order_date >= '2024-06-01' "
      "AND order_date < '2024-07-01' ORDER BY amount LIMIT 50")
con.execute("DROP INDEX IF EXISTS ixc")
con.execute("CREATE INDEX ixc ON orders(status, order_date, amount)")
print("\nrange column is not the sort column, index (status, order_date, amount):", plan(Q3), run(Q3)[0])
con.execute("DROP INDEX ixc")
con.execute("CREATE INDEX ixc ON orders(status, amount, order_date)")
print("index (status, amount, order_date):", plan(Q3), run(Q3)[0])
con.execute("DROP INDEX ixc")
# pandas: the same query with nsmallest on dates
top = pm.head(50)
assert len(top) == 50 and list(top.order_date) == [r[0] for r in full[:50]]
print("pandas sort_values + head(50) gives the same 50 dates as SQL (ties broken by order_id)")
```

**Output (my run):**
```text
Query 1: SELECT order_id, amount FROM orders WHERE status = 'shipped' AND order_date >= '2024-06-01' AND order_date < '2024-07-01' ORDER BY order_date LIMIT 50
                                 index                                                                                plan  vm_steps  rows
                                  none                                          SCAN orders | USE TEMP B-TREE FOR ORDER BY    780147    50
                              (status)             SEARCH orders USING INDEX ixc (status=?) | USE TEMP B-TREE FOR ORDER BY    329996    50
                          (order_date)                       SEARCH orders USING INDEX ixc (order_date>? AND order_date<?)      1217    50
                  (order_date, status)                       SEARCH orders USING INDEX ixc (order_date>? AND order_date<?)      2812    50
                  (status, order_date)          SEARCH orders USING INDEX ixc (status=? AND order_date>? AND order_date<?)       421    50
(status, order_date, amount, order_id) SEARCH orders USING COVERING INDEX ixc (status=? AND order_date>? AND order_date<?)       370    50
matching rows without LIMIT: 4182 (SQL and pandas agree)
first 50 dates only span: 2024-06-01 to 2024-06-01 -> ties on order_date mean LIMIT 50 is ambiguous without a tiebreaker

Query 2: SELECT * FROM orders WHERE customer_id = 5 ORDER BY order_date DESC LIMIT 10
                    index                                                                         plan  vm_steps  rows
                     none                                   SCAN orders | USE TEMP B-TREE FOR ORDER BY    600181    10
            (customer_id) SEARCH orders USING INDEX ixc (customer_id=?) | USE TEMP B-TREE FOR ORDER BY       212    10
(customer_id, order_date)                                SEARCH orders USING INDEX ixc (customer_id=?)       120    10
             (order_date)                                                  SCAN orders USING INDEX ixc    770763    10

range column is not the sort column, index (status, order_date, amount): SEARCH orders USING COVERING INDEX ixc (status=? AND order_date>? AND order_date<?) | USE TEMP B-TREE FOR ORDER BY 34323
index (status, amount, order_date): SEARCH orders USING COVERING INDEX ixc (status=?) 3193
pandas sort_values + head(50) gives the same 50 dates as SQL (ties broken by order_id)
```

Comparison for the assert: the full unlimited SQL result, ordered by `order_date, order_id`, is compared with the pandas mask sorted by the same two columns (4,182 rows), and the pandas `head(50)` dates equal the first 50 SQL dates. The LIMIT result of each index plan is not compared id by id because rows tied on `order_date` can come back in a different order.

**Edge cases:**
- **LIMIT with ties.** All 50 rows have the same `order_date`, so which 50 rows you get is not defined by `ORDER BY order_date` alone. Add a tiebreaker (`ORDER BY order_date, order_id`) if the pages must be stable.
- **Range column is not the sort column.** For `WHERE status = 'shipped' AND order_date range ORDER BY amount LIMIT 50` with `(status, order_date, amount)` the plan was `SEARCH ... (status=? AND order_date>? AND order_date<?) | USE TEMP B-TREE FOR ORDER BY` (34,323 steps): once the range is applied the entries are in date order, not amount order, so a sort returns. The index `(status, amount, order_date)` gave `SEARCH ... (status=?)` with no sort and 3,193 steps, because rows within one status come out in amount order and SQLite filters the date as it goes and stops after 50. Which design is better depends on how many rows pass the date filter; here shipped June orders are about 8 percent of shipped orders, so the walk by amount stops early.
- **`(order_date)` alone is competitive here** (1,217 steps) because the first 50 days' rows fall quickly; with a rarer status it would walk far more rows to find 50 matches.
- **DESC.** `ORDER BY order_date DESC` on `(customer_id, order_date)` ran without a sort: SQLite can read an index backwards.
- **`(order_date)` as the only index for Query 2** is the worst candidate (770,763 steps): it walks the dates backwards looking for customer 5.
- **Write cost:** each of these indexes slows inserts (Q2); six candidates here do not mean create six.

**Then explain:**
- **The rule:** equality columns first, then the range or sort column, then extra columns to cover the select list. Equality fixes a contiguous block; the next column is ordered inside that block, so a range or `ORDER BY` on it is cheap; trailing columns avoid the table lookup.
- **Cardinality-first is a heuristic.** Putting the most distinct column first helps when it is used as an equality in every query, but it is wrong when the query's equality column is the lower-cardinality one and the high-cardinality column is only in a range or sort: here `status` (4 values) goes first because the query uses it with `=`, and `order_date` second for range and order.
- **Why one equality before the range removes the sort:** inside the equality block the next column is sorted, so `ORDER BY` on it is free; without the equality column first (`(order_date, status)`) the order is still by date but the status is filtered row by row.
- **Second query:** `(customer_id, order_date)` gave `SEARCH ... (customer_id=?)` with no temp B-tree (120 steps) against 212 steps with `(customer_id)` alone, which needs `USE TEMP B-TREE FOR ORDER BY`. The saving is small for 8 matching rows and large for a customer with thousands of orders.
- **Other engines (not executed here):** PostgreSQL and MySQL follow the same equality-then-range reasoning for B-trees; SQL Server calls the extra columns `INCLUDE` columns and PostgreSQL has `INCLUDE` too (described from memory, not executed).

**Follow-ups:**
- *Where would `LIMIT 50 OFFSET n` go wrong?* It still walks `n` entries (Part 4 Q39 compares OFFSET pagination with keyset pagination).
- *What if the query also filters `amount > 100`?* Put `amount` in the index after the date column only as a covering column; it cannot be a second range.
- *How do you decide between two designs?* Plan, then VM steps or measured runtime on a realistic copy, then write cost.

**Common mistakes:**
- Putting the range column before the equality column.
- Believing the high-cardinality column must always lead.
- Creating separate single-column indexes and expecting SQLite to combine them for an `AND` (the planner generally uses one index per table for `AND`; the docs I opened say it does not intersect indexes).
- Trusting a plan without checking the step count or runtime.

### Q6 ⭐⭐⭐ 🟡 LIKE and indexes: users(user_id, email, name, city) with 100,000 rows and indexes on email and name. Print plans for name LIKE 'Asha%', name LIKE '%Rao', name LIKE '%Rao%', lower(name) = 'asha rao', and show the SQLite-specific trap that LIKE 'Asha%' still scans on a plain index because LIKE is case-insensitive and the index uses BINARY collation, then fix it with an index on name COLLATE NOCASE (and, separately, with PRAGMA case_sensitive_like = ON, noting the pragma changes query results). Explain why a leading wildcard cannot use a B-tree, the prefix-range rewrite (name >= 'Asha' AND name < 'Ashb'), the expression-index route for lower(name), the reversed-string trick for suffix search, and where full-text search (FTS5 is compiled into this SQLite; check) or trigram indexes (PostgreSQL pg_trgm, not executed) take over.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** A B-tree index can only seek on a known prefix, so `LIKE 'Asha%'` can use an index but `LIKE '%Rao'` cannot; and in SQLite even the prefix form scans on a plain index, because `LIKE` ignores case while the index uses BINARY collation, so you need an index declared `COLLATE NOCASE`.

**Schema and sample data:**
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, email TEXT, name TEXT, city TEXT);
CREATE INDEX ix_email ON users(email);
CREATE INDEX ix_name ON users(name);
```
100,000 rows from `random.seed(6)`: names like `Asha Rao` built from 10 first names and 10 last names, with 5 percent in UPPER CASE and 5 percent in lower case, so case matters. `LIKE 'Asha%'` matches 10,042 rows (all cases); the case-exact `'Asha'` prefix matches 9,036.

**SQL answer:** the predicates are the `tests` list in the Code block. The key ones:
`name LIKE 'Asha%'`, `name >= 'Asha' AND name < 'Ashb'`, `lower(name) = 'asha rao'`, and the fixes `CREATE INDEX ix_name_nc ON users(name COLLATE NOCASE)`, `CREATE INDEX ix_lower ON users(lower(name))` and a reversed-name column with its own index.

**pandas answer:** `df.name.str.lower().str.startswith("asha")` is the case-insensitive `LIKE` (10,042 rows); `df.name.str.startswith("Asha")` is the BINARY prefix range (9,036). pandas always scans; there is no index to trap you, but the case decision is explicit. Both are asserted against SQL in the Code block.

**Example:** the stored names include `'Asha Rao'`, `'ASHA RAO'` and `'asha rao'`. `LIKE 'Asha%'` matches all three because SQLite's `LIKE` is case-insensitive for ASCII. A BINARY index sorts `'ASHA RAO'` (capitals sort first) far from `'Asha Rao'`, so the matches are not one contiguous range and the planner cannot seek: `SCAN users`, 420,093 steps. A `NOCASE` index sorts case-insensitively, so all three are adjacent and the plan becomes `SEARCH users USING INDEX ix_name_nc (name>? AND name<?)` at 40,180 steps. The hand-written range `name >= 'Asha' AND name < 'Ashb'` uses the plain index (36,159 steps) but is case-exact, so it returns 9,036 rows, not 10,042. The range's upper bound `'Ashb'` is the prefix with its last character incremented.

**Code:** run with `python3 -I`.
```python
# Q6: LIKE and indexes in SQLite (BINARY vs NOCASE index, prefix range, expression index, reversed string, FTS5).
import random
import sqlite3
import pandas as pd

random.seed(6)
first = ["Asha", "Rahul", "Priya", "Vikram", "Meera", "Arjun", "Kavya", "Ishaan", "Neha", "Sanjay"]
last = ["Rao", "Sharma", "Iyer", "Gupta", "Nair", "Patel", "Singh", "Menon", "Das", "Khan"]
def mk(i):
    f, l = random.choice(first), random.choice(last)
    n = f"{f} {l}"
    r = random.random()
    if r < 0.05: n = n.upper()        # upper case variant
    elif r < 0.10: n = n.lower()      # 'asha rao'
    return (i, f"user{i}@example.com", n, random.choice(["Pune", "Delhi"]))
rows = [mk(i) for i in range(1, 100001)]
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY, email TEXT, name TEXT, city TEXT)")
con.executemany("INSERT INTO users VALUES (?,?,?,?)", rows)
con.execute("CREATE INDEX ix_email ON users(email)")
con.execute("CREATE INDEX ix_name ON users(name)")
con.commit()

_n = [0]
def plan(where):
    _n[0] += 1
    return " | ".join(r[3] for r in con.execute(f"EXPLAIN QUERY PLAN SELECT * FROM users WHERE {where}" + " " * _n[0]))
def run(where):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(f"SELECT user_id FROM users WHERE {where}").fetchall()
    con.set_progress_handler(None, 0)
    return c[0], sorted(r[0] for r in out)

pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 80)
tests = ["name LIKE 'Asha%'", "name LIKE '%Rao%'", "name LIKE '%Rao'", "lower(name) = 'asha rao'",
         "name >= 'Asha' AND name < 'Ashb'", "name GLOB 'Asha*'"]
res = [(w, plan(w), run(w)[0], len(run(w)[1])) for w in tests]
print("-- plain index ix_name (BINARY collation)")
print(pd.DataFrame(res, columns=["predicate", "plan", "vm_steps", "rows"]).to_string(index=False))

# fix 1: NOCASE index
con.execute("CREATE INDEX ix_name_nc ON users(name COLLATE NOCASE)")
w = "name LIKE 'Asha%'"
print("\n-- with ix_name_nc ON users(name COLLATE NOCASE)")
print(plan(w), run(w)[0], len(run(w)[1]))
like_ids = run(w)[1]

# the prefix range gives a different (case-sensitive) answer than LIKE
rng = run("name >= 'Asha' AND name < 'Ashb'")[1]
glob = run("name GLOB 'Asha*'")[1]
print("LIKE rows:", len(like_ids), " BINARY prefix-range rows:", len(rng), " GLOB rows:", len(glob))
assert set(rng) <= set(like_ids) and rng == glob and len(like_ids) > len(rng)

# fix 2: PRAGMA case_sensitive_like = ON (changes results; use a fresh connection to see it clearly)
con2 = sqlite3.connect(":memory:")
con2.execute("CREATE TABLE users(user_id INTEGER PRIMARY KEY, email TEXT, name TEXT, city TEXT)")
con2.executemany("INSERT INTO users VALUES (?,?,?,?)", rows)
con2.execute("CREATE INDEX ix_name ON users(name)")
con2.execute("PRAGMA case_sensitive_like = ON")
p = " | ".join(r[3] for r in con2.execute("EXPLAIN QUERY PLAN SELECT * FROM users WHERE name LIKE 'Asha%'"))
n_on = con2.execute("SELECT COUNT(*) FROM users WHERE name LIKE 'Asha%'").fetchone()[0]
print("\ncase_sensitive_like=ON plan:", p, "| rows:", n_on, "(was", len(like_ids), "with the default)")
assert n_on == len(rng)

# expression index for lower(name)
con.execute("CREATE INDEX ix_lower ON users(lower(name))")
w = "lower(name) = 'asha rao'"
print("\nexpression index on lower(name):", plan(w), run(w)[0], len(run(w)[1]))

# suffix search: store the reversed string, index it, search with a prefix on the reversed text
con.execute("ALTER TABLE users ADD COLUMN name_rev TEXT")
con.executemany("UPDATE users SET name_rev = ? WHERE user_id = ?", [(r[2][::-1].lower(), r[0]) for r in rows])
con.execute("CREATE INDEX ix_rev ON users(name_rev)")
w = "name_rev >= 'oar' AND name_rev < 'oas'"
print("suffix 'rao' via reversed column:", plan(w), run(w)[0], len(run(w)[1]))
suffix_scan = run("lower(name) LIKE '%rao'")
assert suffix_scan[1] == run(w)[1]
print("full scan LIKE '%rao' steps:", suffix_scan[0], "rows:", len(suffix_scan[1]), "(same rows)")

# FTS5
print("\nFTS5 compiled in:", ("ENABLE_FTS5",) in con.execute("PRAGMA compile_options").fetchall())
con.execute("CREATE VIRTUAL TABLE fts USING fts5(name)")
con.executemany("INSERT INTO fts(rowid, name) VALUES (?,?)", [(r[0], r[2]) for r in rows])
print("FTS5 plan:", " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT rowid FROM fts WHERE fts MATCH 'asha'")))
fts_ids = sorted(r[0] for r in con.execute("SELECT rowid FROM fts WHERE fts MATCH 'asha'"))
print("MATCH 'asha' (whole word, case-insensitive):", len(fts_ids), "| prefix query 'ash*':",
      con.execute("SELECT COUNT(*) FROM fts WHERE fts MATCH 'ash*'").fetchone()[0])
assert fts_ids == like_ids

# pandas: str.startswith is a scan; case handling is explicit
df = pd.DataFrame(rows, columns=["user_id", "email", "name", "city"])
p_like = sorted(df[df.name.str.lower().str.startswith("asha")].user_id)
p_bin = sorted(df[df.name.str.startswith("Asha")].user_id)
assert p_like == like_ids and p_bin == rng
print("\npandas: str.lower().str.startswith('asha') =", len(p_like), "rows (= LIKE); str.startswith('Asha') =", len(p_bin), "(= BINARY range)")
```

**Output (my run):**
```text
-- plain index ix_name (BINARY collation)
                       predicate                                                 plan  vm_steps  rows
               name LIKE 'Asha%'                                           SCAN users    420093 10042
               name LIKE '%Rao%'                                           SCAN users    420245 10118
                name LIKE '%Rao'                                           SCAN users    420245 10118
        lower(name) = 'asha rao'                                           SCAN users    401955   973
name >= 'Asha' AND name < 'Ashb' SEARCH users USING INDEX ix_name (name>? AND name<?)     36159  9036
               name GLOB 'Asha*' SEARCH users USING INDEX ix_name (name>? AND name<?)     36155  9036

-- with ix_name_nc ON users(name COLLATE NOCASE)
SEARCH users USING INDEX ix_name_nc (name>? AND name<?) 40180 10042
LIKE rows: 10042  BINARY prefix-range rows: 9036  GLOB rows: 9036

case_sensitive_like=ON plan: SEARCH users USING INDEX ix_name (name>? AND name<?) | rows: 9036 (was 10042 with the default)

expression index on lower(name): SEARCH users USING INDEX ix_lower (<expr>=?) 4877 973
suffix 'rao' via reversed column: SEARCH users USING INDEX ix_rev (name_rev>? AND name_rev<?) 40487 10118
full scan LIKE '%rao' steps: 520248 rows: 10118 (same rows)

FTS5 compiled in: True
FTS5 plan: SCAN fts VIRTUAL TABLE INDEX 0:M1
MATCH 'asha' (whole word, case-insensitive): 10042 | prefix query 'ash*': 10042

pandas: str.lower().str.startswith('asha') = 10042 rows (= LIKE); str.startswith('Asha') = 9036 (= BINARY range)
```

Comparison for the assert: all result sets are lists of `user_id` sorted ascending; `LIKE` is compared with `str.lower().str.startswith`, the BINARY range with `GLOB 'Asha*'` and `str.startswith('Asha')`.

**Edge cases:**
- **`PRAGMA case_sensitive_like = ON` changes results.** With it on (new connection), the plain index was used (`name>? AND name<?`) but the query returned 9,036 rows instead of 10,042. It is a connection-level setting, so one connection can return different results from another for the same SQL; use it only when case-exact matching is genuinely what you want.
- **`%Rao%` and `%Rao` both scan** (420,245 steps each, same 10,118 rows here because every name ends in a last name). A leading wildcard means the match can start anywhere, so there is no sorted prefix to seek.
- **`lower(name) = 'asha rao'` scans** against a plain index (401,955 steps, 973 rows), and with `ix_lower ON users(lower(name))` it became `SEARCH ... (<expr>=?)` at 4,877 steps.
- **Wildcards inside the pattern.** `_` and `%` in user-supplied text must be escaped (`ESCAPE`), otherwise the prefix is not what you think.
- **Collation of the index must match the comparison.** An index declared NOCASE only helps comparisons that use NOCASE (and `LIKE`), not BINARY `=`.
- **Non-ASCII text.** SQLite's built-in `LIKE` and NOCASE fold ASCII only (from the SQLite function documentation, not re-verified here); other engines treat Unicode differently.

**Then explain:**
- **Why a leading wildcard cannot use a B-tree:** the tree is sorted from the first character. `'%Rao'` could match `'Asha Rao'`, `'Ben Rao'` and `'Zed Rao'`, which sit at opposite ends of the tree.
- **Suffix search with a reversed string:** store the reversed lower-case name (`'oar ahsa'`), index it, and the suffix `Rao` becomes the prefix range `name_rev >= 'oar' AND name_rev < 'oas'`: 40,487 steps and the same 10,118 rows as the 520,248-step scan of `lower(name) LIKE '%rao'`. In this table the saving is modest because the suffix matches 10 percent of rows; with a rarer suffix it is large. SQLite has no `reverse()` function, so I computed the string in Python and stored it in a column.
- **Where full-text takes over:** FTS5 is compiled into this SQLite (`ENABLE_FTS5` is in `compile_options`). `MATCH 'asha'` returned the same 10,042 rows as `LIKE 'Asha%'` (it matches whole words, case-insensitively, and handles the word anywhere in the text), and `'ash*'` is its prefix query. The plan line reads `SCAN fts VIRTUAL TABLE INDEX 0:M1`, which is the virtual table's own index and not a table scan in the usual sense.
- **Trigram indexes (not executed here):** PostgreSQL `pg_trgm` with a GIN or GiST index can serve `LIKE '%Rao%'`; I did not run it.

**Follow-ups:**
- *Would `ILIKE` or `UPPER()` help in PostgreSQL?* They need an expression index or `pg_trgm` there too (described, not executed here).
- *Which is better, NOCASE index or `lower()` expression index?* NOCASE serves `LIKE` and NOCASE comparisons; the `lower()` index only serves the exact expression.
- *What about a user searching "rao" in the middle?* FTS or trigram, not B-tree.

**Common mistakes:**
- Assuming `LIKE 'abc%'` always uses the index; in SQLite it does not on a BINARY index.
- Turning on `case_sensitive_like` globally to fix a plan and silently changing results.
- Wrapping the column in `lower()` and keeping a plain index.
- Writing the prefix range with a wrong upper bound (`'Asha~'` or the wrong increment).

### Q7 ⭐⭐⭐ 🟡 Implicit type conversion and an index that is not used: a(id INTEGER PRIMARY KEY, k TEXT, v INT) with 5,000 rows holding '1'..'5000' in k and b(id INTEGER PRIMARY KEY, k INTEGER, w INT) with 50,000 rows, with an index on a.k and one on b.k. Print plans for WHERE a.k = 42, WHERE a.k = '42', WHERE b.k = '42', a join a.k = b.k on mismatched declared types, and a join with b.k + 0 or b.k || '' on the join key. Show by running which of these keep the index in SQLite (column affinity is applied to the comparison, so a plain comparison against a literal still uses the index) and which break it (an expression on the join key flips the join order). Then explain why the same mismatch is a classic index killer in other engines (MySQL string column compared with a number, SQL Server implicit conversion by data type precedence, PostgreSQL cast of the column side), hedged and not executed, and how to check for it (the plan, warnings) and fix it (match the types, cast the literal not the column).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** In SQLite a plain comparison of an indexed column with a literal of the other type still used the index in every case I ran, because the column's affinity is applied to the literal; what broke the plan was an expression on the join key, which flipped the join order and cost about 2.6 times the steps; in MySQL, SQL Server and PostgreSQL the same mismatch can disable the index (hedged, not executed here), so match the types and cast the literal, never the column.

**Schema and sample data:**
```sql
CREATE TABLE a(id INTEGER PRIMARY KEY, k TEXT, v INT);
CREATE TABLE b(id INTEGER PRIMARY KEY, k INTEGER, w INT);
CREATE INDEX ia ON a(k);
CREATE INDEX ib ON b(k);
```
`a` has 5,000 rows with `k` holding the text `'1'` to `'5000'`; `b` has 50,000 rows with random integer `k` from 1 to 5000 (`random.seed(7)`). The Code block checks `typeof(k)`: text in `a`, integer in `b`.

**SQL answer:** the eight queries are in the Code block under `qs`: `a.k = 42`, `a.k = '42'`, `b.k = 42`, `b.k = '42'`, the join `a.k = b.k`, and the joins with `b.k + 0`, `b.k || ''` and `CAST(b.k AS TEXT)`.

**pandas answer:** pandas does not coerce for you: `da.merge(db, on="k")` with a `str` key on one side and `int64` on the other raised `ValueError` in my run (message in the output). The fix is explicit: `da.assign(k=da.k.astype("int64")).merge(db, on="k")`, asserted to give the same 50,000 rows as the SQL join.

**Example:** SQLite applies "affinity" to comparisons. For `a.k = 42`, `a.k` has TEXT affinity, so the number 42 is converted to the text `'42'` and the index on `a.k` is searched with that text. For `b.k = '42'`, `b.k` has INTEGER affinity, so the text becomes the number 42 and `ib` is used. All four literal comparisons printed `SEARCH ... USING INDEX` (17, 16, 93 and 94 steps; `b` returns 12 rows, `a` 1). For the join `a.k = b.k` (TEXT against INTEGER), SQLite applied numeric affinity to the TEXT side, scanned `a`'s covering index and probed `b` by index: `SCAN a USING COVERING INDEX ia | SEARCH b USING COVERING INDEX ib (k=?)`, 175,010 steps. Writing `b.k + 0` or `b.k || ''` on the join key hid `b.k` from the index, so the planner swapped the loops: `SCAN b ... | SEARCH a ... (k=?)`, scanning the 50,000-row table instead of the 5,000-row one, 449,999 steps (about 2.6 times as many).

**Code:** run with `python3 -I`.
```python
# Q7: implicit type conversion in SQLite (column affinity) and what it does to index use and join order.
import random
import sqlite3
import pandas as pd

random.seed(7)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE a(id INTEGER PRIMARY KEY, k TEXT, v INT);
CREATE TABLE b(id INTEGER PRIMARY KEY, k INTEGER, w INT);
""")
con.executemany("INSERT INTO a VALUES (?,?,?)", [(i, str(i), i % 7) for i in range(1, 5001)])
con.executemany("INSERT INTO b VALUES (?,?,?)", [(i, random.randint(1, 5000), i % 11) for i in range(1, 50001)])
con.execute("CREATE INDEX ia ON a(k)")
con.execute("CREATE INDEX ib ON b(k)")
con.commit()
print("declared affinities:", con.execute("SELECT name, type FROM pragma_table_info('a') UNION ALL SELECT name, type FROM pragma_table_info('b')").fetchall())
print("typeof stored:", con.execute("SELECT typeof(k) FROM a LIMIT 1").fetchone(), con.execute("SELECT typeof(k) FROM b LIMIT 1").fetchone())

_n = [0]
def plan(sql):
    _n[0] += 1
    return " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]))
def run(sql):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], out

pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 110)
qs = [
    ("a.k = 42 (TEXT col, int literal)",  "SELECT * FROM a WHERE a.k = 42"),
    ("a.k = '42'",                        "SELECT * FROM a WHERE a.k = '42'"),
    ("b.k = 42",                          "SELECT * FROM b WHERE b.k = 42"),
    ("b.k = '42' (INT col, text literal)", "SELECT * FROM b WHERE b.k = '42'"),
    ("join a.k = b.k (TEXT vs INTEGER)",  "SELECT COUNT(*) FROM a JOIN b ON a.k = b.k"),
    ("join a.k = b.k + 0",                "SELECT COUNT(*) FROM a JOIN b ON a.k = b.k + 0"),
    ("join a.k = b.k || ''",              "SELECT COUNT(*) FROM a JOIN b ON a.k = b.k || ''"),
    ("join CAST(b.k AS TEXT) = a.k",      "SELECT COUNT(*) FROM a JOIN b ON CAST(b.k AS TEXT) = a.k"),
]
res = []
for name, q in qs:
    s, r = run(q)
    res.append((name, plan(q), s, r[0][0] if len(r) == 1 and len(r[0]) == 1 else len(r)))
print(pd.DataFrame(res, columns=["query", "plan", "vm_steps", "count_or_rows"]).to_string(index=False))

# the sneaky part: affinity changes which rows match, not just the plan
con.execute("INSERT INTO a VALUES (9001, '042', 0)")
print("\nrow k='042' in TEXT column a:")
print("  a.k = 42   ->", con.execute("SELECT COUNT(*) FROM a WHERE a.k = 42").fetchone()[0], "(42 is converted to text '42', which is not '042')")
print("  a.k = '42' ->", con.execute("SELECT COUNT(*) FROM a WHERE a.k = '42'").fetchone()[0])
print("  join a.k = b.k, rows with a.id=9001:", con.execute("SELECT COUNT(*) FROM a JOIN b ON a.k = b.k WHERE a.id = 9001").fetchone()[0],
      "(column vs column: numeric affinity is applied to the TEXT side, so '042' = 42)")
print("  join on a.k = CAST(b.k AS TEXT), rows with a.id=9001:", con.execute("SELECT COUNT(*) FROM a JOIN b ON a.k = CAST(b.k AS TEXT) WHERE a.id = 9001").fetchone()[0])
con.execute("DELETE FROM a WHERE id = 9001")

# pandas: merging a str key with an int key does not silently convert
da = pd.read_sql("SELECT * FROM a", con)
db = pd.read_sql("SELECT * FROM b", con)
print("\npandas dtypes:", da.k.dtype, db.k.dtype)
try:
    da.merge(db, on="k")
except ValueError as e:
    print("pandas merge on mismatched dtypes ->", type(e).__name__ + ":", str(e)[:100])
m = da.assign(k=da.k.astype("int64")).merge(db, on="k")
sql_n = con.execute("SELECT COUNT(*) FROM a JOIN b ON a.k = b.k").fetchone()[0]
assert len(m) == sql_n
print("after astype(int64): merge rows", len(m), "= SQL join count", sql_n)
```

**Output (my run):**
```text
declared affinities: [('id', 'INTEGER'), ('k', 'TEXT'), ('v', 'INT'), ('id', 'INTEGER'), ('k', 'INTEGER'), ('w', 'INT')]
typeof stored: ('text',) ('integer',)
                             query                                                                    plan  vm_steps  count_or_rows
  a.k = 42 (TEXT col, int literal)                                           SEARCH a USING INDEX ia (k=?)        17              1
                        a.k = '42'                                           SEARCH a USING INDEX ia (k=?)        16              1
                          b.k = 42                                           SEARCH b USING INDEX ib (k=?)        93             12
b.k = '42' (INT col, text literal)                                           SEARCH b USING INDEX ib (k=?)        94             12
  join a.k = b.k (TEXT vs INTEGER) SCAN a USING COVERING INDEX ia | SEARCH b USING COVERING INDEX ib (k=?)    175010          50000
                join a.k = b.k + 0 SCAN b USING COVERING INDEX ib | SEARCH a USING COVERING INDEX ia (k=?)    449999          50000
              join a.k = b.k || '' SCAN b USING COVERING INDEX ib | SEARCH a USING COVERING INDEX ia (k=?)    449999          50000
      join CAST(b.k AS TEXT) = a.k SCAN b USING COVERING INDEX ib | SEARCH a USING COVERING INDEX ia (k=?)    399998          50000

row k='042' in TEXT column a:
  a.k = 42   -> 1 (42 is converted to text '42', which is not '042')
  a.k = '42' -> 1
  join a.k = b.k, rows with a.id=9001: 12 (column vs column: numeric affinity is applied to the TEXT side, so '042' = 42)
  join on a.k = CAST(b.k AS TEXT), rows with a.id=9001: 0

pandas dtypes: str int64
pandas merge on mismatched dtypes -> ValueError: You are trying to merge on str and int64 columns for key 'k'. If you wish to proceed you should use 
after astype(int64): merge rows 50000 = SQL join count 50000
```

Comparison for the assert: the pandas merge (after casting the key to `int64`) and the SQL join have the same row count (50,000); the count is compared, not the row order.

**Edge cases:**
- **Same plan, different answer.** I inserted a row with `k = '042'` into the TEXT column. `a.k = 42` and `a.k = '42'` both found only the real `'42'` row (the literal 42 becomes `'42'`, which is not `'042'`), but in the join `a.k = b.k` the `'042'` row matched the 12 `b` rows with `k = 42`, because column-to-column comparison applies numeric affinity to the TEXT side. `a.k = CAST(b.k AS TEXT)` matched 0 for that row. So the same data gives different results depending on how the comparison is written, a correctness trap before it is a performance one.
- **The premise to correct:** the question's framing says a mismatch is a classic index killer. In SQLite it was not, in any of the literal comparisons I ran; it is a risk in other engines (below).
- **`CAST(b.k AS TEXT)`** also flipped the order (399,998 steps), as expected for an expression on `b.k`.
- **Results were checked with `COUNT(*)` where the plan shows a covering index;** with `SELECT *` the plan lines read `USING INDEX` without `COVERING`.
- **The join count of 50,000** means every `b` row found a match in `a`, because every `b.k` is in 1 to 5000.

**Then explain:**
- **Why other engines break (described, not executed here):** MySQL compares a string column with a number by converting both sides to numbers, so the string column's index cannot be used and the whole column is converted row by row, as I understand the documentation; SQL Server applies data type precedence and implicitly converts the lower-precedence side, and if that is the column the index cannot be seeked and the plan shows a `CONVERT_IMPLICIT` warning; in PostgreSQL a cast on the column (`col::int`) is an expression on the column, so a plain index on `col` will not serve it, and how a mismatched parameter type is resolved depends on its operator rules, which I did not run. None of this was run here.
- **How to check:** read the plan for `SCAN` where you expected a seek, check engine warnings (SQL Server plan warnings, MySQL `SHOW WARNINGS`), and compare declared types of both sides of every join.
- **How to fix:** make the column types match (best), or cast the literal or parameter side to the column's type, not the column. Do not wrap an indexed column in `CAST`, `+ 0` or `|| ''`.
- **Join order flip:** an expression on one join key removes that side's index, so the planner chooses the other loop order; the smaller table should be the outer one, so the flip made the join about 2.6 times as expensive here.

**Follow-ups:**
- *Why did SQLite not need a cast?* Affinity rules decide the comparison type from the column declarations.
- *What would fix the `'042'` surprise?* Store keys in one type, with a CHECK or application validation.
- *Where does this bite in pandas?* A `merge` on mismatched dtypes raises; `object`/`str` keys with leading zeros (`'042'`) converted with `astype(int)` lose them.

**Common mistakes:**
- Assuming the behaviour seen in one engine holds in another.
- Fixing a slow join by casting the indexed column.
- Storing numeric ids in a TEXT column and joining them to an INTEGER column.
- Trusting `COUNT(*)` equality without checking edge keys such as leading zeros.

### Q8 ⭐⭐⭐ 🟡 IN versus EXISTS versus JOIN versus DISTINCT for a semi-join: customers(customer_id, name, city) with 20,000 rows and orders(order_id, customer_id, status, amount) with 200,000 rows, with and without an index on orders(customer_id). Return customers who have at least one 'placed' order using IN (subquery), EXISTS (correlated), a JOIN with DISTINCT, and a JOIN with GROUP BY. Print each plan (LIST SUBQUERY, CORRELATED SCALAR SUBQUERY, USE TEMP B-TREE FOR DISTINCT), count VM steps, assert identical results, and show that a plain JOIN without DISTINCT returns duplicate customers. Say that modern optimisers often turn IN and EXISTS into the same semi-join (state what SQLite actually printed, and hedge the PostgreSQL and MySQL behaviour as not executed), so the interview answer is 'check the plan', and when DISTINCT over a join is the costly way. Cross-reference Part 3 Q4 (EXISTS versus IN) and Part 2 Q8 (semi-join).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** IN, EXISTS, JOIN + DISTINCT and JOIN + GROUP BY all return the same customers, and which is cheapest depends on the engine and the indexes, so the interview answer is "write the clearest form (EXISTS or IN), then check the plan"; in SQLite with an index on `(customer_id, status)` EXISTS was cheapest (255,412 steps against about 733,000 to 1.0 million), but without a useful index it is the one that explodes.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, amount REAL);
CREATE INDEX ix_cust ON orders(customer_id);          -- second run
CREATE INDEX ix_cs ON orders(customer_id, status);    -- third run
```
20,000 customers, 200,000 orders from `random.seed(8)`; only customers 1 to 15,000 order, and about 10 percent of orders are `placed`. 11,080 customers have a placed order, and those customers have 20,038 placed orders in total, so a plain join returns 20,038 rows for 11,080 distinct customers. The no-index case for the correlated form uses a smaller copy (2,000 customers, 20,000 orders) because at full size it is far too slow to wait for.

**SQL answer:** the four forms are the `forms` dictionary in the Code block (`IN`, `EXISTS`, `JOIN+DISTINCT`, `JOIN+GROUP BY`) and the duplicate-producing `plain` join.

**pandas answer:** `cu[cu.customer_id.isin(placed.customer_id)]` is the semi-join (no duplicates possible). `cu.merge(placed[["customer_id"]], on="customer_id")` is the plain join (20,038 rows) and `.drop_duplicates()` brings it back to 11,080. Both are asserted equal to SQL in the Code block.

**Example:** take a customer with 3 placed orders (the sample has many). `EXISTS` asks "is there at least one?" and stops after the first. A plain `JOIN` returns that customer three times, one per placed order, which is how 11,080 customers become 20,038 rows. `DISTINCT` or `GROUP BY` collapses them with an extra temp B-tree (visible as `USE TEMP B-TREE FOR DISTINCT / GROUP BY` in the plan). `IN (SELECT ...)` builds the list of customer ids with a placed order once (`LIST SUBQUERY 1`) and probes `customers` by primary key.

**Code:** run with `python3 -I`. The first block (no index) uses the small copy; the last block repeats the three fast forms at full size with no index. Counts use `set_progress_handler`, so they are deterministic.
```python
# Q8: semi-join as IN, EXISTS, JOIN + DISTINCT, JOIN + GROUP BY, with and without an index on orders(customer_id).
import random
import sqlite3
import pandas as pd

def build(ncust, nord, active, seed=8):
    random.seed(seed)
    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
    CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, amount REAL);
    """)
    con.executemany("INSERT INTO customers VALUES (?,?,?)",
                    [(i, f"c{i}", ["Pune", "Delhi"][i % 2]) for i in range(1, ncust + 1)])
    # only the first `active` customers order at all; 'placed' is about 10 percent of orders
    con.executemany("INSERT INTO orders VALUES (?,?,?,?)",
                    [(i, random.randint(1, active), random.choices(["placed", "shipped", "delivered", "cancelled"], [1, 4, 4, 1])[0],
                      round(random.uniform(10, 500), 2)) for i in range(1, nord + 1)])
    con.commit()
    return con

forms = {
 "IN":            "SELECT customer_id, name FROM customers WHERE customer_id IN (SELECT customer_id FROM orders WHERE status = 'placed')",
 "EXISTS":        "SELECT c.customer_id, c.name FROM customers c WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id AND o.status = 'placed')",
 "JOIN+DISTINCT": "SELECT DISTINCT c.customer_id, c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'placed'",
 "JOIN+GROUP BY": "SELECT c.customer_id, c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'placed' GROUP BY c.customer_id, c.name",
}
plain = "SELECT c.customer_id, c.name FROM customers c JOIN orders o ON o.customer_id = c.customer_id WHERE o.status = 'placed'"

_n = [0]
def plan(con, sql):
    _n[0] += 1
    return " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]))
def run(con, sql):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], out

def report(con, label):
    print(f"=== {label}")
    res = {}
    for name, q in forms.items():
        s, r = run(con, q)
        res[name] = sorted(r)
        print(f"{name:14s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, q)}")
    s, r = run(con, plain)
    print(f"{'plain JOIN':14s} steps {s:9d} rows {len(r):6d}  (distinct customers in those rows: {len(set(r))})")
    ref = res["IN"]
    assert all(v == ref for v in res.values())
    return ref

# 1. no index: the correlated EXISTS rescans orders per customer, so use a small copy (2,000 / 20,000)
small = build(2000, 20000, 1500)
report(small, "NO index on orders(customer_id), SMALL data 2,000 customers / 20,000 orders")

# 2. full size 20,000 / 200,000, with the index
con = build(20000, 200000, 15000)
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
ref = report(con, "index ix_cust(customer_id), FULL data 20,000 customers / 200,000 orders")
con.execute("DROP INDEX ix_cust")
con.execute("CREATE INDEX ix_cs ON orders(customer_id, status)")
ref2 = report(con, "index ix_cs(customer_id, status), FULL data")
assert ref == ref2

# 3. full size without an index, only the forms that finish quickly (EXISTS skipped on purpose)
con.execute("DROP INDEX ix_cs")
print("=== NO index, FULL data (EXISTS not run: it rescans 200,000 rows per customer)")
for name in ["IN", "JOIN+DISTINCT", "JOIN+GROUP BY"]:
    s, r = run(con, forms[name])
    print(f"{name:14s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, forms[name])}")
    assert sorted(r) == ref

# pandas
cu = pd.read_sql("SELECT * FROM customers", con)
od = pd.read_sql("SELECT * FROM orders", con)
placed = od[od.status == "placed"]
via_isin = cu[cu.customer_id.isin(placed.customer_id)]
via_merge = cu.merge(placed[["customer_id"]], on="customer_id")
via_dedup = via_merge.drop_duplicates()
print("\npandas merge rows (duplicates):", len(via_merge), "| isin rows:", len(via_isin), "| merge + drop_duplicates:", len(via_dedup))
b = pd.DataFrame(ref, columns=["customer_id", "name"])
pd.testing.assert_frame_equal(via_isin.sort_values("customer_id")[["customer_id", "name"]].reset_index(drop=True), b, check_dtype=False)
pd.testing.assert_frame_equal(via_dedup.sort_values("customer_id")[["customer_id", "name"]].reset_index(drop=True), b, check_dtype=False)
print("asserts passed: all SQL forms, pandas isin and merge+drop_duplicates equal after sorting by customer_id; rows =", len(b))
```

**Output (my run):**
```text
=== NO index on orders(customer_id), SMALL data 2,000 customers / 20,000 orders
IN             steps     73950 rows   1124  plan: SEARCH customers USING INTEGER PRIMARY KEY (rowid=?) | LIST SUBQUERY 1 | SCAN orders
EXISTS         steps 105265768 rows   1124  plan: SCAN c | CORRELATED SCALAR SUBQUERY 1 | SCAN o
JOIN+DISTINCT  steps     73492 rows   1124  plan: SCAN o | SEARCH c USING INTEGER PRIMARY KEY (rowid=?) | USE TEMP B-TREE FOR DISTINCT
JOIN+GROUP BY  steps    102942 rows   1124  plan: SCAN o | SEARCH c USING INTEGER PRIMARY KEY (rowid=?) | USE TEMP B-TREE FOR GROUP BY
plain JOIN     steps     70119 rows   2022  (distinct customers in those rows: 1124)
=== index ix_cust(customer_id), FULL data 20,000 customers / 200,000 orders
IN             steps    737690 rows  11080  plan: SEARCH customers USING INTEGER PRIMARY KEY (rowid=?) | LIST SUBQUERY 1 | SCAN orders
EXISTS         steps    782251 rows  11080  plan: SCAN c | CORRELATED SCALAR SUBQUERY 1 | SEARCH o USING INDEX ix_cust (customer_id=?)
JOIN+DISTINCT  steps    733441 rows  11080  plan: SCAN o | SEARCH c USING INTEGER PRIMARY KEY (rowid=?) | USE TEMP B-TREE FOR DISTINCT
JOIN+GROUP BY  steps   1024595 rows  11080  plan: SCAN o | SEARCH c USING INTEGER PRIMARY KEY (rowid=?) | USE TEMP B-TREE FOR GROUP BY
plain JOIN     steps    700200 rows  20038  (distinct customers in those rows: 11080)
=== index ix_cs(customer_id, status), FULL data
IN             steps    737691 rows  11080  plan: SEARCH customers USING INTEGER PRIMARY KEY (rowid=?) | LIST SUBQUERY 1 | SCAN orders USING COVERING INDEX ix_cs
EXISTS         steps    255412 rows  11080  plan: SCAN c | CORRELATED SCALAR SUBQUERY 1 | SEARCH o USING COVERING INDEX ix_cs (customer_id=? AND status=?)
JOIN+DISTINCT  steps    733442 rows  11080  plan: SCAN o USING COVERING INDEX ix_cs | SEARCH c USING INTEGER PRIMARY KEY (rowid=?) | USE TEMP B-TREE FOR DISTINCT
JOIN+GROUP BY  steps   1024596 rows  11080  plan: SCAN o USING COVERING INDEX ix_cs | SEARCH c USING INTEGER PRIMARY KEY (rowid=?) | USE TEMP B-TREE FOR GROUP BY
plain JOIN     steps    700201 rows  20038  (distinct customers in those rows: 11080)
=== NO index, FULL data (EXISTS not run: it rescans 200,000 rows per customer)
IN             steps    737692 rows  11080  plan: SEARCH customers USING INTEGER PRIMARY KEY (rowid=?) | LIST SUBQUERY 1 | SCAN orders
JOIN+DISTINCT  steps    733442 rows  11080  plan: SCAN o | SEARCH c USING INTEGER PRIMARY KEY (rowid=?) | USE TEMP B-TREE FOR DISTINCT
JOIN+GROUP BY  steps   1024596 rows  11080  plan: SCAN o | SEARCH c USING INTEGER PRIMARY KEY (rowid=?) | USE TEMP B-TREE FOR GROUP BY

pandas merge rows (duplicates): 20038 | isin rows: 11080 | merge + drop_duplicates: 11080
asserts passed: all SQL forms, pandas isin and merge+drop_duplicates equal after sorting by customer_id; rows = 11080
```

Comparison for the assert: every SQL form must equal the `IN` result, sorted; the pandas `isin` and `merge + drop_duplicates` frames are sorted by `customer_id` before `assert_frame_equal`.

**Edge cases:**
- **What SQLite actually printed.** SQLite did not turn `EXISTS` into the same plan as `IN`: `IN` was `SEARCH customers USING INTEGER PRIMARY KEY | LIST SUBQUERY 1 | SCAN orders`, `EXISTS` stayed `CORRELATED SCALAR SUBQUERY 1`, the joins were `SCAN o | SEARCH c USING INTEGER PRIMARY KEY` (the planner started from `orders`, not `customers`). So in SQLite the forms are not interchangeable cost-wise.
- **No useful index, EXISTS.** With no index the correlated `EXISTS` was `SCAN c | CORRELATED SCALAR SUBQUERY 1 | SCAN o`: 105,265,768 steps on the small copy, against 73,950 for `IN`. I did not run it at full size.
- **An index on `customer_id` alone barely helped the placed-only question** (EXISTS 782,251 steps, a little worse than `IN` at 737,690) because every probe must still read each customer's rows to check `status`. The composite `(customer_id, status)` is what made EXISTS cheap (255,412 steps, `USING COVERING INDEX ix_cs (customer_id=? AND status=?)`).
- **`GROUP BY` costs more than `DISTINCT`** here (1,024,595 against 733,441 steps) probably because it groups on two columns (I did not test that explanation); the results are identical.
- **A plain `JOIN` is not a semi-join.** 20,038 rows for 11,080 customers, and `COUNT(*)` or `SUM` over it would be inflated (Part 2 Q12).
- **`DISTINCT` over a join is the costly form when the join is wide**: it first produces every matching pair and then removes duplicates; use it only when you also need columns from the child table.
- **NULLs:** `IN` and `EXISTS` ignore customers whose `customer_id` is NULL in orders; for `NOT` forms the story changes (Q9).

**Then explain:**
- **Semantics:** all four return customers who have at least one placed order; only `IN`, `EXISTS` and the pandas `isin` are semi-joins (they never duplicate the left row).
- **Optimisers (described, not executed here):** PostgreSQL and MySQL 8 commonly rewrite `IN` and `EXISTS` subqueries into the same semi-join plan, SQL Server too, though the exact rewrite depends on version and statistics; I did not run them. That is why "`EXISTS` is faster than `IN`" is folklore, and the answer is "check the plan".
- **When DISTINCT over a join is the costly way:** when the join multiplies rows (many orders per customer) and you then pay for a sort or hash to remove them, or when you forget it and the totals double-count.
- **Cross-references:** Part 3 Q4 (EXISTS versus IN) and Part 2 Q8 (semi-join).

**Follow-ups:**
- *Which would you write by default?* `EXISTS` for "has at least one", because it states the intent, cannot duplicate rows and handles NULLs safely.
- *When does `IN` with a subquery go wrong?* With `NOT IN` and NULLs (Q9).
- *Can you return the latest placed order too?* Then you need a join or a window function, not a semi-join (Part 4).

**Common mistakes:**
- Joining and forgetting `DISTINCT`, then double-counting.
- Using `SELECT DISTINCT` to hide a join mistake.
- Believing `EXISTS` is always faster than `IN` (or the reverse) without a plan.
- Testing only with an index that does not cover the filter column.

### Q9 ⭐⭐⭐ 🔴 NOT IN versus NOT EXISTS versus LEFT JOIN ... IS NULL, as plans and as results: customers(customer_id, name) with 20,000 rows and orders(order_id, customer_id, amount) with 200,000 rows where 3,000 customers have no orders and orders.customer_id contains a few NULLs in a second run. Print the plan of each anti-join with and without an index on orders(customer_id) (USING INDEX ... FOR IN-OPERATOR, CORRELATED SCALAR SUBQUERY, LEFT-JOIN), count VM steps and show that NOT IN returns zero rows once the subquery contains a NULL while the other two do not. Explain why the three are not interchangeable in the presence of NULLs, which one to default to and why, and that the efficiency comparison depends on the engine (hedge anti-join operators in PostgreSQL, MySQL, SQL Server and Spark, not executed). Cross-reference Part 3 Q3 (NOT IN NULL trap) and Part 2 Q2 (anti-join).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** `NOT EXISTS` and `LEFT JOIN ... IS NULL` find customers with no orders, and `NOT IN` finds them too until the subquery contains one NULL, after which `NOT IN` returns zero rows (I ran it: 3,000 rows become 0 after adding three orders with a NULL customer), so default to `NOT EXISTS`.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, amount REAL);
CREATE INDEX ix_cust ON orders(customer_id);
```
20,000 customers and 200,000 orders from `random.seed(9)`, where orders only reference customers 1 to 17,000, so 3,000 customers (17,001 to 20,000) have no orders. The NULL run inserts three more orders with `customer_id = NULL`. The no-index case for the correlated form uses a small copy (2,000 customers, 20,000 orders, 300 without orders) because it is far too slow at full size.

**SQL answer:** the three forms are the `forms` dictionary in the Code block, plus the NULL-safe `NOT IN (... WHERE customer_id IS NOT NULL)`.

**pandas answer:** `cu[~cu.customer_id.isin(od.customer_id)]` is the anti-join; `cu.merge(od[["customer_id", "order_id"]], on="customer_id", how="left", indicator=True)` and then the `left_only` rows is the `LEFT JOIN ... IS NULL` form. The orders column became `float64` once NULLs were present. Both returned 3,000 rows with the NULLs present, because `isin` and `merge` do not match a NaN to any customer id, so they behave like `NOT EXISTS`, not like `NOT IN`.

**Example:** `customer_id NOT IN (1, 2, NULL)` expands to `customer_id <> 1 AND customer_id <> 2 AND customer_id <> NULL`. The last term is UNKNOWN for every customer, so the whole `AND` is never TRUE and no row passes, which is exactly why the second run returned 0. For customer 18,000 with the clean list: it is not in orders, every comparison is TRUE, so it is returned. `NOT EXISTS` instead asks "is there a matching order row?" and a NULL order row never matches any customer, so 18,000 still comes back. `LEFT JOIN` finds no match, so the `o` columns are NULL and `o.order_id IS NULL` is TRUE.

**Code:** run with `python3 -I`. Steps are `set_progress_handler` counts.
```python
# Q9: NOT IN vs NOT EXISTS vs LEFT JOIN ... IS NULL: plans, VM steps, and the NULL trap.
import random
import sqlite3
import pandas as pd

def build(ncust, nord, active, nulls=0, seed=9):
    random.seed(seed)
    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
    CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, amount REAL);
    """)
    con.executemany("INSERT INTO customers VALUES (?,?)", [(i, f"c{i}") for i in range(1, ncust + 1)])
    con.executemany("INSERT INTO orders VALUES (?,?,?)",
                    [(i, random.randint(1, active), round(random.uniform(10, 500), 2)) for i in range(1, nord + 1)])
    # a few orders with no customer at all
    for j in range(nulls):
        con.execute("INSERT INTO orders VALUES (?,NULL,1.0)", (nord + 1 + j,))
    con.commit()
    return con

forms = {
 "NOT IN":     "SELECT customer_id, name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)",
 "NOT EXISTS": "SELECT c.customer_id, c.name FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)",
 "LEFT JOIN":  "SELECT c.customer_id, c.name FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id WHERE o.order_id IS NULL",
}
_n = [0]
def plan(con, sql):
    _n[0] += 1
    return " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]))
def run(con, sql):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], out

def report(con, label, skip=()):
    print(f"=== {label}")
    res = {}
    for name, q in forms.items():
        if name in skip:
            print(f"{name:11s} (not run: too slow at this size)")
            continue
        s, r = run(con, q)
        res[name] = sorted(r)
        print(f"{name:11s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, q)}")
    return res

# 1. no index, small copy 2,000 customers / 20,000 orders (the correlated form is too slow at full size)
small = build(2000, 20000, 1700)
r = report(small, "NO index, SMALL 2,000 customers / 20,000 orders (300 customers without orders)")
assert len({tuple(v) for v in r.values()}) == 1

# 2. full size, with the index
con = build(20000, 200000, 17000)
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
res = report(con, "index ix_cust, FULL 20,000 / 200,000 (3,000 customers without orders)")
ref = res["NOT IN"]
assert all(v == ref for v in res.values())
print("rows (customers with no orders):", len(ref))

# 3. full size, no index: NOT IN and LEFT JOIN only
con.execute("DROP INDEX ix_cust")
res3 = report(con, "NO index, FULL size (NOT EXISTS skipped)", skip=("NOT EXISTS",))
assert all(v == ref for v in res3.values())

# 4. the NULL trap: add 3 orders with customer_id NULL
con.execute("INSERT INTO orders VALUES (900001, NULL, 1.0), (900002, NULL, 1.0), (900003, NULL, 1.0)")
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
print("\n=== after inserting 3 orders with customer_id NULL (index ix_cust present)")
res4 = {}
for name, q in forms.items():
    s, r = run(con, q)
    res4[name] = sorted(r)
    print(f"{name:11s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, q)}")
assert res4["NOT IN"] == [] and res4["NOT EXISTS"] == ref and res4["LEFT JOIN"] == ref
# the NULL-safe version of NOT IN
safe = "SELECT customer_id, name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)"
s, r = run(con, safe)
print(f"{'NOT IN + IS NOT NULL':11s} steps {s:9d} rows {len(r):6d}  plan: {plan(con, safe)}")
assert sorted(r) == ref

# pandas: isin / ~isin behaves like NOT EXISTS, because NaN never matches a customer_id
cu = pd.read_sql("SELECT * FROM customers", con)
od = pd.read_sql("SELECT * FROM orders", con)
print("\npandas orders.customer_id dtype with NULLs:", od.customer_id.dtype)
p_anti = cu[~cu.customer_id.isin(od.customer_id)].sort_values("customer_id")[["customer_id", "name"]].reset_index(drop=True)
m = cu.merge(od[["customer_id", "order_id"]], on="customer_id", how="left", indicator=True)
p_merge = m[m["_merge"] == "left_only"][["customer_id", "name"]].sort_values("customer_id").reset_index(drop=True)
expected = pd.DataFrame(ref, columns=["customer_id", "name"])
pd.testing.assert_frame_equal(p_anti, expected, check_dtype=False)
pd.testing.assert_frame_equal(p_merge, expected, check_dtype=False)
print("pandas ~isin and merge(indicator) return", len(p_anti), "rows with NULLs present (same as NOT EXISTS / LEFT JOIN, not NOT IN)")
print("asserts passed (compared after sorting by customer_id)")
```

**Output (my run):**
```text
=== NO index, SMALL 2,000 customers / 20,000 orders (300 customers without orders)
NOT IN      steps    102911 rows    300  plan: SCAN customers | LIST SUBQUERY 1 | SCAN orders
NOT EXISTS  steps  35474856 rows    300  plan: SCAN c | CORRELATED SCALAR SUBQUERY 1 | SCAN o
LEFT JOIN   steps    238412 rows    300  plan: SCAN c | BLOOM FILTER ON o (customer_id=?) | SEARCH o USING AUTOMATIC COVERING INDEX (customer_id=?) LEFT-JOIN
=== index ix_cust, FULL 20,000 / 200,000 (3,000 customers without orders)
NOT IN      steps    129011 rows   3000  plan: SCAN customers | USING INDEX ix_cust FOR IN-OPERATOR
NOT EXISTS  steps    223009 rows   3000  plan: SCAN c | CORRELATED SCALAR SUBQUERY 1 | SEARCH o USING COVERING INDEX ix_cust (customer_id=?)
LEFT JOIN   steps   1130011 rows   3000  plan: SCAN c | SEARCH o USING COVERING INDEX ix_cust (customer_id=?) LEFT-JOIN
rows (customers with no orders): 3000
=== NO index, FULL size (NOT EXISTS skipped)
NOT IN      steps   1029013 rows   3000  plan: SCAN customers | LIST SUBQUERY 1 | SCAN orders
NOT EXISTS  (not run: too slow at this size)
LEFT JOIN   steps   2384014 rows   3000  plan: SCAN c | BLOOM FILTER ON o (customer_id=?) | SEARCH o USING AUTOMATIC COVERING INDEX (customer_id=?) LEFT-JOIN

=== after inserting 3 orders with customer_id NULL (index ix_cust present)
NOT IN      steps    132011 rows      0  plan: SCAN customers | USING INDEX ix_cust FOR IN-OPERATOR
NOT EXISTS  steps    223009 rows   3000  plan: SCAN c | CORRELATED SCALAR SUBQUERY 1 | SEARCH o USING COVERING INDEX ix_cust (customer_id=?)
LEFT JOIN   steps   1130011 rows   3000  plan: SCAN c | SEARCH o USING COVERING INDEX ix_cust (customer_id=?) LEFT-JOIN
NOT IN + IS NOT NULL steps   1029015 rows   3000  plan: SCAN customers | LIST SUBQUERY 1 | SEARCH orders USING COVERING INDEX ix_cust (customer_id>?)

pandas orders.customer_id dtype with NULLs: float64
pandas ~isin and merge(indicator) return 3000 rows with NULLs present (same as NOT EXISTS / LEFT JOIN, not NOT IN)
asserts passed (compared after sorting by customer_id)
```

Comparison for the assert: results are sorted lists of `(customer_id, name)`; the three forms must match each other (clean data) and the pandas frames sorted by `customer_id`; in the NULL run `NOT IN` must equal the empty list while the other two still equal the clean result.

**Edge cases:**
- **NULL in the subquery:** `NOT IN` returned 0 rows (132,011 steps, the plan unchanged), `NOT EXISTS` and `LEFT JOIN` 3,000. This is a silent wrong answer, not an error.
- **The fix for `NOT IN`:** add `WHERE customer_id IS NOT NULL` inside the subquery. It returned the correct 3,000 rows, but the plan changed from `USING INDEX ix_cust FOR IN-OPERATOR` to `LIST SUBQUERY 1 | SEARCH orders USING COVERING INDEX ix_cust (customer_id>?)`, and the cost went from 132,011 to 1,029,015 steps, so the safe form lost the fast path in SQLite.
- **Efficiency was not what folklore says in SQLite.** With the index, `NOT IN` was cheapest (129,011 steps) and the `LEFT JOIN` the most expensive (1,130,011): probably because it walks every order entry of each customer that has orders before the `IS NULL` test (I did not isolate that); `NOT EXISTS` stopped at the first match (223,009). Without an index the correlated `NOT EXISTS` used 35,474,856 steps on the small copy against 102,911 for `NOT IN` and 238,412 for `LEFT JOIN`, which SQLite helped with `BLOOM FILTER ... USING AUTOMATIC COVERING INDEX`.
- **Plan wording.** With the index I saw `USING INDEX ix_cust FOR IN-OPERATOR` (NOT IN), `CORRELATED SCALAR SUBQUERY 1` with a covering `SEARCH` (NOT EXISTS) and `SEARCH o USING COVERING INDEX ix_cust (customer_id=?) LEFT-JOIN` (LEFT JOIN). Without it, `LIST SUBQUERY 1 | SCAN orders`, `SCAN o`, and an automatic index with a bloom filter.
- **Duplicates on the right side** do not matter for any of the three (they would for a plain `JOIN`).
- **Empty subquery:** `NOT IN` of an empty set is TRUE for every row; the NULL problem only appears when a NULL is present.

**Then explain:**
- **Why not interchangeable with NULLs:** `NOT IN` uses three-valued logic, so one NULL turns every comparison into UNKNOWN; `NOT EXISTS` and `LEFT JOIN` only test whether a matching row exists, and NULL never matches.
- **Default:** `NOT EXISTS`, because it states the intent, is NULL-safe, and its performance is acceptable once the foreign-key column is indexed. Use `LEFT JOIN ... IS NULL` if you also want other columns or prefer it readable.
- **Efficiency depends on the engine.** PostgreSQL, MySQL, SQL Server and Spark have different anti-join operators (hash anti join, `NOT EXISTS` rewrites, `LEFT ANTI JOIN`), and some can rewrite `NOT IN` only when the column is declared NOT NULL; I did not run any of them, so describe, not promise.
- **Cross-references:** Part 3 Q3 (the NOT IN NULL trap) and Part 2 Q2 (anti-join).

**Follow-ups:**
- *Can you keep `NOT IN` safely?* Only if the subquery column is `NOT NULL` by constraint or filtered with `IS NOT NULL`.
- *What if the outer key can be NULL?* `NULL NOT IN (...)` is UNKNOWN, so that row is dropped by `NOT IN`; `NOT EXISTS` keeps it (reasoned from the three-valued rule, not run here).
- *How would you do it in pandas for a composite key?* A left `merge` with `indicator=True` on both columns.

**Common mistakes:**
- Using `NOT IN` on a nullable column.
- `LEFT JOIN ... WHERE o.some_column IS NULL` using a column that can be NULL in matched rows (use the primary key).
- Putting the right-table filter in `WHERE` instead of `ON` (turns a left join into an inner join).
- Declaring one form "fastest" without a plan and a step count.

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

**Output (my run):** one run on this machine.
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

### Q19 ⭐⭐ 🟡 Fan-out joins and pre-aggregation: customers(customer_id, name) 20,000 rows, orders(order_id, customer_id, order_total) 100,000 rows and order_items(item_id, order_id, qty, price) 400,000 rows. A report wants per-customer order count, revenue from orders and item quantity. Show the naive three-table join with SUM(order_total) over-counting (assert the wrong total), the plan and VM steps, the fix by pre-aggregating each child table in a derived table or CTE before joining, assert both fixed forms agree with a pandas groupby, and compare VM steps. Explain that fan-out is both a correctness and a cost problem (row count multiplication), why aggregating before joining shrinks the join input, and how to check the grain of each side. Cross-reference Part 2 Q12 (fan-out inflates SUM), Q13 (the chasm trap) and Q18 (join to an aggregated derived table).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** A three-table join multiplies each order row by its item rows, so any order-level column (SUM(order_total)) is counted once per item; aggregate each child to the grain of the key you join on (one row per customer) before joining, and the totals are right and the join input is smaller.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, price INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chen');
INSERT INTO orders VALUES (10,1,100),(11,1,50),(12,2,70);
INSERT INTO order_items VALUES (1,10,1,60),(2,10,2,20),(3,10,1,0),(4,11,3,10),(5,11,1,20),(6,12,2,35);
```

**SQL answer:** `NAIVE` (the wrong one), `FIX_DERIVED` (one derived table per child) and `FIX_CTE` (items rolled up to order grain in a CTE, then orders to customer grain) are in the Code block, copied here.
```sql
SELECT c.customer_id, COUNT(DISTINCT o.order_id) AS n_orders,
       SUM(o.order_total) AS revenue, SUM(i.qty) AS qty
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN order_items i ON i.order_id = o.order_id
GROUP BY c.customer_id ORDER BY c.customer_id

SELECT c.customer_id, COALESCE(oa.n_orders, 0) AS n_orders,
       COALESCE(oa.revenue, 0) AS revenue, COALESCE(ia.qty, 0) AS qty
FROM customers c
LEFT JOIN (SELECT customer_id, COUNT(*) AS n_orders, SUM(order_total) AS revenue
           FROM orders GROUP BY customer_id) oa ON oa.customer_id = c.customer_id
LEFT JOIN (SELECT o.customer_id, SUM(i.qty) AS qty
           FROM order_items i JOIN orders o ON o.order_id = i.order_id
           GROUP BY o.customer_id) ia ON ia.customer_id = c.customer_id
ORDER BY c.customer_id

WITH item_per_order AS (SELECT order_id, SUM(qty) AS qty FROM order_items GROUP BY order_id),
     per_customer AS (
       SELECT o.customer_id, COUNT(*) AS n_orders, SUM(o.order_total) AS revenue,
              SUM(COALESCE(ipo.qty, 0)) AS qty
       FROM orders o LEFT JOIN item_per_order ipo ON ipo.order_id = o.order_id
       GROUP BY o.customer_id)
SELECT c.customer_id, COALESCE(p.n_orders, 0) AS n_orders,
       COALESCE(p.revenue, 0) AS revenue, COALESCE(p.qty, 0) AS qty
FROM customers c LEFT JOIN per_customer p ON p.customer_id = c.customer_id
ORDER BY c.customer_id
```

**pandas answer:** Aggregate each side with `groupby`, then merge at customer grain (the same idea as the SQL fix).
```py
def pandas_answer(cu, od, it):
    oa = od.groupby("customer_id").agg(n_orders=("order_id", "size"), revenue=("order_total", "sum"))
    qty = it.merge(od[["order_id", "customer_id"]], on="order_id").groupby("customer_id")["qty"].sum().rename("qty")
    out = cu[["customer_id"]].merge(oa, on="customer_id", how="left").merge(qty, on="customer_id", how="left")
    out[["n_orders", "revenue", "qty"]] = out[["n_orders", "revenue", "qty"]].fillna(0).astype("int64")
    return out.sort_values("customer_id").reset_index(drop=True)
```

**Example:** Asha has orders 10 (total 100, three items) and 11 (total 50, two items); Ben has order 12 (total 70, one item); Chen has no orders. The naive join returns one row per item: order 10 appears 3 times and order 11 twice, so SUM(order_total) for Asha is 100*3 + 50*2 = 400, but the true revenue is 100 + 50 = 150. Her item quantity is right in both forms (1+2+1 + 3+1 = 8) because `qty` lives at the item grain, and COUNT(DISTINCT order_id) = 2 is right only because of DISTINCT. Ben: 70 and 2 are right (one item, no fan-out). Chen: the naive form gives NULL revenue and quantity (the LEFT JOIN found nothing), the fixed forms give 0 through COALESCE. At scale (seed 19) the true SUM(order_total) is 25,505,616 and the naive query returns 103,626,730, a factor of 4.06 (about the 4 items per order).

**Code:** run with `python3 -I`.
```python
# Q19: fan-out joins and pre-aggregation (SQLite in-memory + pandas)
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1                       # vary the text so the statement cache cannot return a stale plan
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

NAIVE = """
SELECT c.customer_id, COUNT(DISTINCT o.order_id) AS n_orders,
       SUM(o.order_total) AS revenue, SUM(i.qty) AS qty
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
LEFT JOIN order_items i ON i.order_id = o.order_id
GROUP BY c.customer_id ORDER BY c.customer_id
"""
FIX_DERIVED = """
SELECT c.customer_id, COALESCE(oa.n_orders, 0) AS n_orders,
       COALESCE(oa.revenue, 0) AS revenue, COALESCE(ia.qty, 0) AS qty
FROM customers c
LEFT JOIN (SELECT customer_id, COUNT(*) AS n_orders, SUM(order_total) AS revenue
           FROM orders GROUP BY customer_id) oa ON oa.customer_id = c.customer_id
LEFT JOIN (SELECT o.customer_id, SUM(i.qty) AS qty
           FROM order_items i JOIN orders o ON o.order_id = i.order_id
           GROUP BY o.customer_id) ia ON ia.customer_id = c.customer_id
ORDER BY c.customer_id
"""
FIX_CTE = """
WITH item_per_order AS (SELECT order_id, SUM(qty) AS qty FROM order_items GROUP BY order_id),
     per_customer AS (
       SELECT o.customer_id, COUNT(*) AS n_orders, SUM(o.order_total) AS revenue,
              SUM(COALESCE(ipo.qty, 0)) AS qty
       FROM orders o LEFT JOIN item_per_order ipo ON ipo.order_id = o.order_id
       GROUP BY o.customer_id)
SELECT c.customer_id, COALESCE(p.n_orders, 0) AS n_orders,
       COALESCE(p.revenue, 0) AS revenue, COALESCE(p.qty, 0) AS qty
FROM customers c LEFT JOIN per_customer p ON p.customer_id = c.customer_id
ORDER BY c.customer_id
"""
def pandas_answer(cu, od, it):
    oa = od.groupby("customer_id").agg(n_orders=("order_id", "size"), revenue=("order_total", "sum"))
    qty = it.merge(od[["order_id", "customer_id"]], on="order_id").groupby("customer_id")["qty"].sum().rename("qty")
    out = cu[["customer_id"]].merge(oa, on="customer_id", how="left").merge(qty, on="customer_id", how="left")
    out[["n_orders", "revenue", "qty"]] = out[["n_orders", "revenue", "qty"]].fillna(0).astype("int64")
    return out.sort_values("customer_id").reset_index(drop=True)

# ---- tiny hand-checkable sample ----
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, price INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chen');
INSERT INTO orders VALUES (10,1,100),(11,1,50),(12,2,70);
INSERT INTO order_items VALUES (1,10,1,60),(2,10,2,20),(3,10,1,0),(4,11,3,10),(5,11,1,20),(6,12,2,35);
""")
print("tiny naive      :", con.execute(NAIVE).fetchall())
print("tiny derived    :", con.execute(FIX_DERIVED).fetchall())
print("tiny cte        :", con.execute(FIX_CTE).fetchall())
# grain check: count rows per key on each side
print("grain: orders per (order_id) max =", con.execute("SELECT MAX(c) FROM (SELECT COUNT(*) c FROM orders GROUP BY order_id)").fetchone()[0],
      "; items per order_id max =", con.execute("SELECT MAX(c) FROM (SELECT COUNT(*) c FROM order_items GROUP BY order_id)").fetchone()[0])

# ---- scaled data ----
random.seed(19)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_total INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, price INTEGER);
""")
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, "c%d" % i) for i in range(1, 20001)])
# customers 19,001..20,000 have no orders on purpose
con.executemany("INSERT INTO orders VALUES (?,?,?)",
                [(i, random.randint(1, 19000), random.randint(10, 500)) for i in range(1, 100001)])
con.executemany("INSERT INTO order_items VALUES (?,?,?,?)",
                [(i, random.randint(1, 95000), random.randint(1, 5), random.randint(1, 100)) for i in range(1, 400001)])
con.commit()
con.execute("CREATE INDEX ix_o_cust ON orders(customer_id)")
con.execute("CREATE INDEX ix_i_order ON order_items(order_id)")
con.commit()
cu = pd.read_sql("SELECT * FROM customers", con)
od = pd.read_sql("SELECT * FROM orders", con)
it = pd.read_sql("SELECT * FROM order_items", con)

truth = int(od["order_total"].sum())
naive_rows, naive_steps = steps(con, NAIVE)
naive = pd.DataFrame(naive_rows, columns=["customer_id", "n_orders", "revenue", "qty"])
naive_total = int(naive["revenue"].sum())
print("true SUM(order_total) over orders :", truth)
print("naive three-table SUM(order_total):", naive_total, "(over-count x%.2f)" % (naive_total / truth))
assert naive_total != truth and naive_total > truth
print("naive COUNT(DISTINCT order_id) total:", int(naive["n_orders"].sum()), "(correct only because of DISTINCT); orders rows:", len(od))
print("rows after the join (fan-out): ", con.execute("SELECT COUNT(*) FROM customers c LEFT JOIN orders o ON o.customer_id=c.customer_id LEFT JOIN order_items i ON i.order_id=o.order_id").fetchone()[0],
      "vs 100,000 orders and 400,000 items")

print("customers with no orders:", con.execute("SELECT COUNT(*) FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id=c.customer_id)").fetchone()[0],
      "; orders with no items:", con.execute("SELECT COUNT(*) FROM orders o WHERE NOT EXISTS (SELECT 1 FROM order_items i WHERE i.order_id=o.order_id)").fetchone()[0])
res = {}
for name, sql in (("naive", NAIVE), ("derived tables", FIX_DERIVED), ("CTE", FIX_CTE)):
    rows, n = steps(con, sql)
    res[name] = (pd.DataFrame(rows, columns=["customer_id", "n_orders", "revenue", "qty"]), n)
    print("%-15s VM steps %9d" % (name, n))
exp = pandas_answer(cu, od, it)
for name in ("derived tables", "CTE"):
    pd.testing.assert_frame_equal(res[name][0], exp)   # both sorted by customer_id
print("asserts passed: both fixed forms equal the pandas groupby (sorted by customer_id); total revenue", int(exp["revenue"].sum()))
assert int(exp["revenue"].sum()) == truth
# naive qty and n_orders (DISTINCT) happen to be right, revenue is not:
assert (naive["qty"].fillna(0).astype(int).values == exp["qty"].values).all()
assert (naive["revenue"].fillna(0).values != exp["revenue"].values).any()
for name, sql in (("naive", NAIVE), ("derived tables", FIX_DERIVED), ("CTE", FIX_CTE)):
    print("\nPLAN", name)
    for l in plan(con, sql): print("  ", l)

# same fixed query without the two foreign-key indexes
con.execute("DROP INDEX ix_o_cust"); con.execute("DROP INDEX ix_i_order")
for name, sql in (("naive", NAIVE), ("derived tables", FIX_DERIVED), ("CTE", FIX_CTE)):
    rows, n = steps(con, sql)
    print("no FK indexes, %-15s VM steps %9d" % (name, n))
```

**Output (my run):**
```text
tiny naive      : [(1, 2, 400, 8), (2, 1, 70, 2), (3, 0, None, None)]
tiny derived    : [(1, 2, 150, 8), (2, 1, 70, 2), (3, 0, 0, 0)]
tiny cte        : [(1, 2, 150, 8), (2, 1, 70, 2), (3, 0, 0, 0)]
grain: orders per (order_id) max = 1 ; items per order_id max = 3
true SUM(order_total) over orders : 25505616
naive three-table SUM(order_total): 103626730 (over-count x4.06)
naive COUNT(DISTINCT order_id) total: 100000 (correct only because of DISTINCT); orders rows: 100000
rows after the join (fan-out):  407514 vs 100,000 orders and 400,000 items
customers with no orders: 1106 ; orders with no items: 6408
naive           VM steps   7782137
derived tables  VM steps   6848055
CTE             VM steps   9116103
asserts passed: both fixed forms equal the pandas groupby (sorted by customer_id); total revenue 25505616

PLAN naive
   SCAN c
   SEARCH o USING INDEX ix_o_cust (customer_id=?) LEFT-JOIN
   SEARCH i USING INDEX ix_i_order (order_id=?) LEFT-JOIN
   USE TEMP B-TREE FOR count(DISTINCT)

PLAN derived tables
   MATERIALIZE oa
   SCAN orders USING INDEX ix_o_cust
   MATERIALIZE ia
   SCAN o USING COVERING INDEX ix_o_cust
   SEARCH i USING INDEX ix_i_order (order_id=?)
   SCAN c
   BLOOM FILTER ON oa (customer_id=?)
   SEARCH oa USING AUTOMATIC COVERING INDEX (customer_id=?) LEFT-JOIN
   BLOOM FILTER ON ia (customer_id=?)
   SEARCH ia USING AUTOMATIC COVERING INDEX (customer_id=?) LEFT-JOIN

PLAN CTE
   MATERIALIZE per_customer
   MATERIALIZE item_per_order
   SCAN order_items USING INDEX ix_i_order
   SCAN o USING INDEX ix_o_cust
   BLOOM FILTER ON ipo (order_id=?)
   SEARCH ipo USING AUTOMATIC COVERING INDEX (order_id=?) LEFT-JOIN
   SCAN c
   BLOOM FILTER ON p (customer_id=?)
   SEARCH p USING AUTOMATIC COVERING INDEX (customer_id=?) LEFT-JOIN
no FK indexes, naive           VM steps  11125387
no FK indexes, derived tables  VM steps   9448060
no FK indexes, CTE             VM steps  11716107
```

**Edge cases:**
- Customers with no orders (1,106 of the 20,000 here, including ids 19,001 to 20,000 which get none by construction) come out as NULL in the naive query and 0 in the fixed ones; the pandas answer fills them with 0 too. The assertion compares all 20,000 rows.
- Orders with no items still survive the LEFT JOINs (once, with NULL qty). The naive join returned 407,514 rows: 400,000 item rows plus 1,106 customers without orders plus 6,408 orders without items (400,000 + 1,106 + 6,408).
- Which columns are wrong depends on their grain: order-level measures (order_total) inflate, item-level measures (qty) do not, and COUNT(*) on the joined rows counts items, not orders. Only the first is silent; always check the grain of each column.

**Then explain:**
- Fan-out is a correctness problem and a cost problem at once: the join output has one row per item (here 407,514 rows against 100,000 orders), so everything after the join (GROUP BY, DISTINCT, sort) works on the multiplied row count.
- Aggregating before joining makes each join input one row per key: `oa` is one row per customer from orders, `ia` one row per customer from items. The grain check is a query: `SELECT MAX(c) FROM (SELECT COUNT(*) c FROM t GROUP BY key)` must be 1 on the side you treat as 'one row per key' (printed in the run: orders per order_id 1, items per order_id up to 3).
- Cost, honestly measured: VM steps were 7,782,137 for the naive join, 6,848,055 for the derived-table fix (about 12% fewer) and 9,116,103 for the CTE form, which is MORE than the naive query. The two fixed forms still have to read all 400,000 item rows, and each materialised child gets an automatic covering index (see the plans: `MATERIALIZE`, `BLOOM FILTER`, `AUTOMATIC COVERING INDEX`). In SQLite with indexed foreign keys the saving on this shape is modest; the decisive win is correctness. Without the two foreign-key indexes all three were slower (11,125,387, 9,448,060 and 11,716,107 steps).
- The chasm trap (Part 2 Q13) is the same fault with two sibling children (orders and, say, payments) joined to one customer: each child multiplies the other. Pre-aggregating each child to the customer grain is the standard fix. See Part 2 Q12 for fan-out inflating SUM and Part 2 Q18 for joining to an aggregated derived table.
- COUNT(DISTINCT) or SUM(DISTINCT) are not repairs: SUM(DISTINCT order_total) drops legitimately equal totals.

**Follow-ups:**
- Why did the CTE version take more steps than the naive join? (Two materialisations plus two automatic indexes; steps count work, not elapsed time, and the effect depends on the data.)
- How would you do this in a warehouse? (Same pre-aggregation; planner behaviour and costs on PostgreSQL, MySQL, BigQuery or Snowflake were not executed here.)
- What if items must stay at item grain (revenue = SUM(qty*price))? Then sum at item grain first, then roll up: the grain stays explicit.

**Common mistakes:**
- Adding DISTINCT to a SUM to 'fix' double counting.
- Trusting COUNT(*) after a one-to-many join to mean orders.
- Using an INNER JOIN to the aggregated child and silently dropping customers without orders (use LEFT JOIN and COALESCE).
- Joining two sibling child tables to one parent and aggregating after the join.

### Q20 ⭐⭐ 🔴 Rewrite a slow correlated subquery: employees(emp_id, dept_id, salary, hire_date) with 50,000 rows. Return employees earning more than their department average using (a) a correlated scalar subquery in WHERE, (b) a join to a pre-aggregated department-average derived table, and (c) AVG() OVER (PARTITION BY dept_id). Print each plan with and without an index on (dept_id, salary), count VM steps (the correlated form re-runs once per outer row), assert identical results, and show that SQLite does not build an automatic index for the correlated inner scan in this shape (print what it prints). Say when the engine decorrelates automatically (hedged for PostgreSQL, SQL Server, MySQL, not executed) and why you should not rely on it. Cross-reference Part 3 Q39 (correlated subquery performance).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** The correlated scalar subquery re-runs the department average once per outer row (about n*n work with no index, n times an index range with one), while a derived table or a window computes each department once; SQLite does not decorrelate for you and builds no automatic index for that inner scan, so rewrite it.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER, hire_date TEXT);
INSERT INTO employees VALUES (1,10,100,'2020-01-01'),(2,10,200,'2021-01-01'),(3,10,300,'2022-01-01'),
 (4,20,50,'2020-05-01'),(5,20,50,'2021-05-01'),(6,30,70,'2023-01-01');
```

**SQL answer:** `A` is the correlated scalar subquery, `B` the join to a pre-aggregated derived table, `C` the window; all three are in the Code block, copied here.
```sql
SELECT e.emp_id FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY e.emp_id

SELECT e.emp_id FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) d ON d.dept_id = e.dept_id
WHERE e.salary > d.avg_sal ORDER BY e.emp_id

SELECT emp_id FROM (SELECT emp_id, salary, AVG(salary) OVER (PARTITION BY dept_id) AS avg_sal FROM employees)
WHERE salary > avg_sal ORDER BY emp_id
```

**pandas answer:** `groupby().transform('mean')` is the window version; the comparison is a boolean mask.
```py
def pandas_answer(df):
    m = df.groupby("dept_id")["salary"].transform("mean")
    return df.loc[df["salary"] > m, ["emp_id"]].sort_values("emp_id").reset_index(drop=True)
```

**Example:** Dept 10 has salaries 100, 200, 300 (average 200): only employee 3 (300) earns more. Dept 20 has 50 and 50 (average 50): nobody earns MORE than the average, so both are excluded (the strict > matters). Dept 30 has one employee, equal to its own average: excluded. Result: emp_id 3 for all three forms (printed as `tiny A/B/C [3]`).

**Code:** run with `python3 -I`.
```python
# Q20: correlated subquery vs derived table vs window (SQLite in-memory + pandas)
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

A = """SELECT e.emp_id FROM employees e
WHERE e.salary > (SELECT AVG(x.salary) FROM employees x WHERE x.dept_id = e.dept_id)
ORDER BY e.emp_id"""
B = """SELECT e.emp_id FROM employees e
JOIN (SELECT dept_id, AVG(salary) AS avg_sal FROM employees GROUP BY dept_id) d ON d.dept_id = e.dept_id
WHERE e.salary > d.avg_sal ORDER BY e.emp_id"""
C = """SELECT emp_id FROM (SELECT emp_id, salary, AVG(salary) OVER (PARTITION BY dept_id) AS avg_sal FROM employees)
WHERE salary > avg_sal ORDER BY emp_id"""
FORMS = (("A correlated", A), ("B derived join", B), ("C window", C))

def build(n, n_dept, seed):
    rnd = random.Random(seed)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER, hire_date TEXT)")
    con.executemany("INSERT INTO employees VALUES (?,?,?,?)",
        [(i, rnd.randint(1, n_dept), rnd.randint(20, 200) * 1000, "20%02d-%02d-01" % (rnd.randint(10, 24), rnd.randint(1, 12))) for i in range(1, n + 1)])
    con.commit()
    return con

def pandas_answer(df):
    m = df.groupby("dept_id")["salary"].transform("mean")
    return df.loc[df["salary"] > m, ["emp_id"]].sort_values("emp_id").reset_index(drop=True)

# tiny sample
con = sqlite3.connect(":memory:")
con.executescript("""CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER, hire_date TEXT);
INSERT INTO employees VALUES (1,10,100,'2020-01-01'),(2,10,200,'2021-01-01'),(3,10,300,'2022-01-01'),(4,20,50,'2020-05-01'),(5,20,50,'2021-05-01'),(6,30,70,'2023-01-01');""")
for name, sql in FORMS:
    print("tiny", name, [r[0] for r in con.execute(sql)])
print("tiny dept avgs:", con.execute("SELECT dept_id, AVG(salary) FROM employees GROUP BY dept_id").fetchall())

# the unindexed correlated form is quadratic: measure it on small tables only
print("\nCorrelated form WITHOUT an index, VM steps by table size (200 departments):")
small = {}
for n in (500, 1000, 2000):
    c = build(n, 200, 20)
    rows, st = steps(c, A)
    small[n] = st
    print("  n=%5d  steps %10d  steps/n^2 = %.2f" % (n, st, st / n / n))
print("  plan:", plan(build(500, 200, 20), A))
est = small[2000] / 2000 / 2000 * 50000 * 50000
print("  extrapolated to 50,000 rows by steps/n^2 (an estimate, NOT run): about %.1e steps" % est)

con = build(50000, 200, 20)
df = pd.read_sql("SELECT * FROM employees", con)
exp = pandas_answer(df)
print("\n50,000 employees, 200 departments, pandas answer rows:", len(exp))
for idx in (False, True):
    if idx:
        con.execute("CREATE INDEX ix_dept_sal ON employees(dept_id, salary)"); con.commit()
    print("--- index on (dept_id, salary):", idx)
    for name, sql in FORMS:
        if name.startswith("A") and not idx:
            print("  %-15s not run at 50,000 rows without an index (quadratic, see above)" % name)
            continue
        rows, n = steps(con, sql)
        pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["emp_id"]), exp)
        print("  %-15s rows %5d  VM steps %10d" % (name, len(rows), n))
    for name, sql in FORMS:
        print("  PLAN", name)
        for l in plan(con, sql): print("     ", l)
print("asserts passed: every form run returned the pandas rows (compared sorted by emp_id)")
```

**Output (my run):**
```text
tiny A correlated [3]
tiny B derived join [3]
tiny C window [3]
tiny dept avgs: [(10, 200.0), (20, 50.0), (30, 70.0)]

Correlated form WITHOUT an index, VM steps by table size (200 departments):
  n=  500  steps    1010385  steps/n^2 = 4.04
  n= 1000  steps    4025775  steps/n^2 = 4.03
  n= 2000  steps   16071237  steps/n^2 = 4.02
  plan: ['SCAN e', 'CORRELATED SCALAR SUBQUERY 1', 'SCAN x']
  extrapolated to 50,000 rows by steps/n^2 (an estimate, NOT run): about 1.0e+10 steps

50,000 employees, 200 departments, pandas answer rows: 24915
--- index on (dept_id, salary): False
  A correlated    not run at 50,000 rows without an index (quadratic, see above)
  B derived join  rows 24915  VM steps    1404036
  C window        rows 24915  VM steps    2426239
  PLAN A correlated
      SCAN e
      CORRELATED SCALAR SUBQUERY 1
      SCAN x
  PLAN B derived join
      CO-ROUTINE d
      SCAN employees
      USE TEMP B-TREE FOR GROUP BY
      SCAN e
      BLOOM FILTER ON d (dept_id=?)
      SEARCH d USING AUTOMATIC COVERING INDEX (dept_id=?)
  PLAN C window
      CO-ROUTINE (subquery-1)
      CO-ROUTINE (subquery-3)
      SCAN employees
      USE TEMP B-TREE FOR ORDER BY
      SCAN (subquery-3)
      SCAN (subquery-1)
      USE TEMP B-TREE FOR ORDER BY
--- index on (dept_id, salary): True
  A correlated    rows 24915  VM steps   51076033
  B derived join  rows 24915  VM steps     628860
  C window        rows 24915  VM steps    2026237
  PLAN A correlated
      SCAN e
      CORRELATED SCALAR SUBQUERY 1
      SEARCH x USING COVERING INDEX ix_dept_sal (dept_id=?)
  PLAN B derived join
      CO-ROUTINE d
      SCAN employees USING COVERING INDEX ix_dept_sal
      SCAN d
      SEARCH e USING COVERING INDEX ix_dept_sal (dept_id=? AND salary>?)
      USE TEMP B-TREE FOR ORDER BY
  PLAN C window
      CO-ROUTINE (subquery-1)
      CO-ROUTINE (subquery-3)
      SCAN employees USING COVERING INDEX ix_dept_sal
      SCAN (subquery-3)
      SCAN (subquery-1)
      USE TEMP B-TREE FOR ORDER BY
asserts passed: every form run returned the pandas rows (compared sorted by emp_id)
```

**Edge cases:**
- Ties and a single-person department return nothing, because salary > average is false when equal. Use >= only if the question says so.
- NULL salaries are ignored by AVG and never satisfy salary > avg; an employee with NULL dept_id gets a NULL average in the correlated form and in B (the equality never matches), so those rows are dropped, but the window form puts all NULL-dept rows in one partition and compares them with that partition's average, so the forms can differ. Reasoned from the rules, not run; there are no NULL departments in this data.
- AVG returns a float: the comparison is exact here because integer salaries make sums exact, but with REAL columns compare with a tolerance in tests.

**Then explain:**
- Cost (VM steps, deterministic proxy). Correlated form, NO index: 1,010,385 steps at 500 rows, 4,025,775 at 1,000 and 16,071,237 at 2,000, i.e. 4.0 steps times n squared every time (doubling the table quadruples the work). Extrapolating by that ratio to 50,000 rows gives about 1.0e10 steps; that number is an estimate and was NOT run.
- At 50,000 rows without an index only B (1,404,036 steps) and C (2,426,239) were run. With an index on (dept_id, salary): A 51,076,033, B 628,860, C 2,026,237 steps. The index turns each inner scan into a covering range search (`SEARCH x USING COVERING INDEX ix_dept_sal (dept_id=?)`) but the subquery still runs once per outer row, so A is still about 81 times B.
- What SQLite prints for the unindexed correlated form: `SCAN e`, `CORRELATED SCALAR SUBQUERY 1`, `SCAN x`. No automatic index appears for the inner scan (automatic indexes were on by default), whereas the derived-table form B shows `BLOOM FILTER ON d` and `SEARCH d USING AUTOMATIC COVERING INDEX (dept_id=?)`, so SQLite builds an automatic index on the materialised derived table but not on the inner scan of a correlated subquery.
- The window form needs the rows ordered by the partition key: without the index the plan shows `USE TEMP B-TREE FOR ORDER BY` twice (the window sort, then the final ORDER BY); with the index the window sort is replaced by an index scan but the final ORDER BY emp_id still sorts.
- Decorrelation by the optimiser: PostgreSQL, SQL Server and MySQL optimisers can sometimes turn some correlated subqueries into joins (SQL Server and recent MySQL for some patterns; PostgreSQL generally not for a correlated scalar aggregate). I did not run any of them, so treat this as a hedge. Do not rely on it: it differs by engine and version and by query shape, and when it does not happen the cost is quadratic. A rewrite that states the grouping explicitly (B or C) is portable and predictable.
- Cross-reference Part 3 Q39 (correlated subquery performance).

**Follow-ups:**
- When is the correlated form fine? (Small outer set, or a selective outer filter plus an index on the inner key, e.g. one department.)
- Why does C use more steps than B with the index? (Window evaluation buffers partitions and adds coroutines; steps are not time.)
- How would you test the three forms at the same size honestly? (Same data, same asserted result, fresh connection per plan print; steps first, timing only as a machine-specific second opinion.)

**Common mistakes:**
- Assuming the optimiser will decorrelate the subquery.
- Reading a plan from a stale statement cache: this run varies the EXPLAIN text so SQLite cannot return an old plan (see the sources note).
- Comparing with >= and then wondering why ties appear.
- Running the quadratic form at full size 'just to see'; measure it on small sizes and extrapolate, labelled as an estimate.

### Q21 ⭐⭐ 🟡 OR, UNION ALL, IN, != and NOT IN as access paths: orders(order_id, customer_id, status, order_date, amount) with 200,000 rows and indexes on customer_id, order_date and status. Print the plan and VM steps for customer_id = 5 OR customer_id = 7 (rewritten to IN), customer_id = 5 OR order_date = '2024-05-05' (MULTI-INDEX OR), customer_id = 5 OR amount > 400 (one unindexed term forces a scan), the UNION ALL rewrite with a guard against double counting versus plain UNION (dedupe cost, USE TEMP B-TREE), status != 'delivered' where 98% match, status NOT IN ('a','b') and status IN (list of the other values). Explain why OR across columns is only fast when every branch is indexable, why UNION removes duplicates at a cost, why inequality predicates rarely use indexes well and that UNION ALL needs mutually exclusive branches (or a NOT condition) for correctness. Hedge index-merge in MySQL and bitmap-OR in PostgreSQL as not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** OR is fast only when every branch has an index (SQLite turns same-column ORs into IN and different indexed columns into a MULTI-INDEX OR), one unindexed term forces a scan, UNION ALL needs mutually exclusive branches to stay correct, UNION pays a temp B-tree to deduplicate, and != / NOT IN on a column that matches 98% of rows is a scan whichever way you write it.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'delivered','2024-05-05',100),(2,5,'cancelled','2024-01-01',20),
 (3,7,'delivered','2024-05-05',30),(4,8,'delivered','2024-05-05',900),(5,9,'returned','2024-02-02',10);
```

**SQL answer:** The tiny forms are `OR2`, `U_ALL_BAD`, `U_ALL_OK` and `U_PLAIN`; the scaled forms are in the `CASES` list of the Code block (same text):
```sql
SELECT order_id FROM orders WHERE customer_id = 5 OR order_date = '2024-05-05' ORDER BY order_id

SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05' AND customer_id IS NOT 5 ORDER BY order_id

SELECT order_id FROM orders WHERE customer_id = 5 UNION
SELECT order_id FROM orders WHERE order_date = '2024-05-05' ORDER BY order_id

SELECT order_id FROM orders WHERE customer_id = 5 OR customer_id = 7
SELECT order_id FROM orders WHERE customer_id = 5 OR amount > 400
SELECT order_id FROM orders WHERE status != 'delivered'
SELECT order_id FROM orders WHERE status NOT IN ('cancelled','returned')
SELECT order_id FROM orders WHERE status IN ('cancelled','returned')
```

**pandas answer:** Boolean masks, one per query (these are the `lambda d: ...` bodies in the `CASES` list, which the code asserts against each SQL result after sorting by order_id).
```py
lambda d: d[(d.customer_id == 5) | (d.order_date == "2024-05-05")]
```

**Example:** Tiny table: customer 5 owns orders 1 and 2; date 2024-05-05 covers orders 1, 3 and 4. The OR returns {1,2,3,4} once each. UNION ALL without a guard returns order 1 twice ([1, 1, 2, 3, 4]) because it matches both branches. The guard `customer_id IS NOT 5` on the second branch removes it: [1, 2, 3, 4]. Plain UNION also returns [1, 2, 3, 4] by deduplicating, at the price of a sort or hash. If a row with customer_id NULL and that date exists (order 6), the guard `IS NOT 5` keeps it ([1,2,3,4,6], correct) but `!= 5` drops it (NULL != 5 is unknown). At 200,000 rows I forced row 1 to customer 5 on 2024-05-05 so the double count shows: the unguarded UNION ALL returned 614 rows against 613 correct.

**Code:** run with `python3 -I`.
```python
# Q21: OR, UNION ALL, IN, != and NOT IN as access paths
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

# tiny sample for the correctness walk-through
t = sqlite3.connect(":memory:")
t.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'delivered','2024-05-05',100),(2,5,'cancelled','2024-01-01',20),
 (3,7,'delivered','2024-05-05',30),(4,8,'delivered','2024-05-05',900),(5,9,'returned','2024-02-02',10);
""")
OR2 = "SELECT order_id FROM orders WHERE customer_id = 5 OR order_date = '2024-05-05' ORDER BY order_id"
U_ALL_BAD = """SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05' ORDER BY order_id"""
U_ALL_OK = """SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05' AND customer_id IS NOT 5 ORDER BY order_id"""
U_PLAIN = """SELECT order_id FROM orders WHERE customer_id = 5 UNION
SELECT order_id FROM orders WHERE order_date = '2024-05-05' ORDER BY order_id"""
for nm, q in (("OR", OR2), ("UNION ALL, no guard", U_ALL_BAD), ("UNION ALL, guarded", U_ALL_OK), ("UNION", U_PLAIN)):
    print("tiny %-20s" % nm, [r[0] for r in t.execute(q)])
# NULL trap for the guard: customer_id IS NOT 5 vs != 5
t.execute("INSERT INTO orders VALUES (6,NULL,'delivered','2024-05-05',1)")
g1 = [r[0] for r in t.execute(U_ALL_OK)]
g2 = [r[0] for r in t.execute(U_ALL_OK.replace("customer_id IS NOT 5", "customer_id != 5"))]
print("tiny with a NULL customer: guard 'IS NOT 5' ->", g1, "; guard '!= 5' ->", g2, "(the != guard drops order 6)")

# scaled data: 200,000 rows
rnd = random.Random(21)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER)")
sts = ["delivered"] * 98 + ["cancelled"] * 1 + ["returned"] * 1   # about 98 / 1 / 1 percent
rows = []
for i in range(1, 200001):
    rows.append((i, rnd.randint(1, 20000), rnd.choice(sts),
                 "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 500)))
rows[0] = (1, 5, "delivered", "2024-05-05", 250)   # force one row that matches both branches
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
con.execute("CREATE INDEX ix_date ON orders(order_date)")
con.execute("CREATE INDEX ix_status ON orders(status)")
con.commit()
df = pd.read_sql("SELECT * FROM orders", con)
print("\nstatus counts:", {k: int(v) for k, v in df["status"].value_counts().items()})

CASES = [
 ("OR on one column", "SELECT order_id FROM orders WHERE customer_id = 5 OR customer_id = 7",
   lambda d: d[(d.customer_id == 5) | (d.customer_id == 7)]),
 ("OR, two indexed columns", "SELECT order_id FROM orders WHERE customer_id = 5 OR order_date = '2024-05-05'",
   lambda d: d[(d.customer_id == 5) | (d.order_date == "2024-05-05")]),
 ("OR with unindexed amount", "SELECT order_id FROM orders WHERE customer_id = 5 OR amount > 400",
   lambda d: d[(d.customer_id == 5) | (d.amount > 400)]),
 ("UNION ALL, guarded", """SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05' AND customer_id IS NOT 5""",
   lambda d: d[(d.customer_id == 5) | (d.order_date == "2024-05-05")]),
 ("UNION (dedupe)", """SELECT order_id FROM orders WHERE customer_id = 5 UNION
SELECT order_id FROM orders WHERE order_date = '2024-05-05'""",
   lambda d: d[(d.customer_id == 5) | (d.order_date == "2024-05-05")]),
 ("status != 'delivered'", "SELECT order_id FROM orders WHERE status != 'delivered'", lambda d: d[d.status != "delivered"]),
 ("status NOT IN (a,b)", "SELECT order_id FROM orders WHERE status NOT IN ('cancelled','returned')",
   lambda d: d[~d.status.isin(["cancelled", "returned"])]),
 ("status IN (other values)", "SELECT order_id FROM orders WHERE status IN ('cancelled','returned')",
   lambda d: d[d.status.isin(["cancelled", "returned"])]),
]
for nm, sql, fn in CASES:
    r, n = steps(con, sql)
    exp = sorted(fn(df)["order_id"].tolist())
    assert sorted(x[0] for x in r) == exp, nm
    print("\n%s: %d rows, VM steps %d" % (nm, len(r), n))
    for l in plan(con, sql): print("   ", l)
bad_r, bad_n = steps(con, """SELECT order_id FROM orders WHERE customer_id = 5 UNION ALL
SELECT order_id FROM orders WHERE order_date = '2024-05-05'""")
ok = steps(con, CASES[3][1])[0]
print("\nUNION ALL WITHOUT the guard returns %d rows versus %d correct (rows matching both branches counted twice)" % (len(bad_r), len(ok)))
r2, n2 = steps(con, "SELECT order_id FROM orders NOT INDEXED WHERE status != 'delivered'")
print("status != delivered with NOT INDEXED (table scan): %d rows, VM steps %d" % (len(r2), n2))
print("asserts passed: every query returned the pandas filter's order_ids (compared sorted)")
```

**Output (my run):**
```text
tiny OR                   [1, 2, 3, 4]
tiny UNION ALL, no guard  [1, 1, 2, 3, 4]
tiny UNION ALL, guarded   [1, 2, 3, 4]
tiny UNION                [1, 2, 3, 4]
tiny with a NULL customer: guard 'IS NOT 5' -> [1, 2, 3, 4, 6] ; guard '!= 5' -> [1, 2, 3, 4] (the != guard drops order 6)

status counts: {'delivered': 195960, 'returned': 2064, 'cancelled': 1976}

OR on one column: 25 rows, VM steps 133
    SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)

OR, two indexed columns: 613 rows, VM steps 5541
    MULTI-INDEX OR
    INDEX 1
    SEARCH orders USING INDEX ix_cust (customer_id=?)
    INDEX 2
    SEARCH orders USING INDEX ix_date (order_date=?)

OR with unindexed amount: 40185 rows, VM steps 1080349
    SCAN orders

UNION ALL, guarded: 613 rows, VM steps 4265
    COMPOUND QUERY
    LEFT-MOST SUBQUERY
    SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)
    UNION ALL
    SEARCH orders USING INDEX ix_date (order_date=?)

UNION (dedupe): 613 rows, VM steps 4926
    COMPOUND QUERY
    LEFT-MOST SUBQUERY
    SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)
    UNION USING TEMP B-TREE
    SEARCH orders USING COVERING INDEX ix_date (order_date=?)

status != 'delivered': 4040 rows, VM steps 608089
    SCAN orders USING COVERING INDEX ix_status

status NOT IN (a,b): 195960 rows, VM steps 1785914
    SCAN orders USING COVERING INDEX ix_status

status IN (other values): 4040 rows, VM steps 16188
    SEARCH orders USING COVERING INDEX ix_status (status=?)

UNION ALL WITHOUT the guard returns 614 rows versus 613 correct (rows matching both branches counted twice)
status != delivered with NOT INDEXED (table scan): 4040 rows, VM steps 608088
asserts passed: every query returned the pandas filter's order_ids (compared sorted)
```

**Edge cases:**
- The double-count demonstration needed one forced row: with random data the two branches rarely overlap, so an unguarded UNION ALL can look right in a test and be wrong in production.
- NOT IN with a NULL in the list returns no rows (three-valued logic, see Part 3 Q3); the list here has none. `!=` and NOT IN exclude rows where status is NULL; there are none in this data.
- The status mix is seeded 98/1/1 percent (195,960 delivered, 1,976 cancelled, 2,064 returned in the run), so 'rare values' are 2% in total, not 0.5%.

**Then explain:**
- Plans and VM steps (200,000 rows, indexes on customer_id, order_date, status): `customer_id = 5 OR customer_id = 7` became one `SEARCH ... USING COVERING INDEX ix_cust (customer_id=?)`, 25 rows, 133 steps (SQLite rewrote the OR into IN). Two different indexed columns gave `MULTI-INDEX OR / INDEX 1 / INDEX 2`, 613 rows, 5,541 steps. With the unindexed `amount > 400` as one OR term the plan was `SCAN orders`, 40,185 rows, 1,080,349 steps: one unindexed branch ruins the whole OR.
- UNION ALL (guarded) took 4,265 steps and UNION 4,926; the UNION plan says `UNION USING TEMP B-TREE`, the cost of removing duplicates. Both branches used an index. UNION ALL is only correct when the branches cannot return the same row, or when you add the NOT condition shown.
- Inequality: `status != 'delivered'` matched 4,040 rows (2%) but the plan was `SCAN orders USING COVERING INDEX ix_status`, 608,089 steps, essentially identical to `NOT INDEXED` (608,088). SQLite did not seek an index for !=. `status IN ('cancelled','returned')` used `SEARCH ... (status=?)` and took 16,188 steps, about 38 times fewer, but it needs the complete list of other values and silently misses new statuses. `NOT IN ('cancelled','returned')` returns 98% of the table (195,960 rows, 1,785,914 steps), where no index can help: reading most of the table is what it costs.
- Why OR across columns is only fast when every branch is indexable: each branch needs its own index lookup, merged by rowid; one unindexed term needs a scan to evaluate, which makes the index lookups pointless. SQLite documents the MULTI-INDEX OR strategy; it does not intersect indexes for AND (see the sources note).
- Other engines, not executed: MySQL has an index_merge optimisation (union, intersection) and PostgreSQL combines indexes with bitmap OR / bitmap AND scans; both are hedged here because I only ran SQLite. Whether either is chosen depends on statistics.
- Rewriting with UNION ALL is a manual way to get what MULTI-INDEX OR does automatically: use it only when you have shown that the original OR is slow and the branches are exclusive.

**Follow-ups:**
- How would you make `status != 'delivered'` fast? (Often you cannot; a partial index on the rare statuses, or IN with the known list, or ask whether the report needs those rows at all; see Q22.)
- Why do the UNION plans say COVERING INDEX while the MULTI-INDEX OR plan printed a plain INDEX? (The index holds order_id as the rowid, so no table lookup is needed; I did not investigate why the OR plan does not say covering.)
- What does UNION do with NULLs? (Treats them as equal for deduplication.)

**Common mistakes:**
- UNION ALL over overlapping branches without a guard.
- Writing the guard as `!= 5` and losing NULL rows.
- Expecting an index to help `!=` or `NOT IN` on a column where most rows match.
- Wrapping an indexed column in a function inside the OR and then blaming OR.

### Q22 ⭐⭐ 🟡 Partial, expression and unique indexes: orders(order_id, customer_id, status, order_date, amount, email TEXT) with 200,000 rows where status = 'placed' is about 3% of rows and email is mixed case. Create (1) a partial index ON orders(order_date) WHERE status = 'placed', (2) an expression index on lower(email) and (3) a UNIQUE index on email with some NULLs. Print which queries use each (the query's WHERE must imply the index's WHERE; show that status IN ('placed'), status != 'delivered' and a bound parameter status = ? behave as they actually do on 3.45.1, by running), compare index size from page counts against a full index, show lower(email) = ? using the expression index only when the expression matches exactly, and show that UNIQUE allows several NULLs. Explain the benefits (smaller index, cheaper writes for the rest of the table) and hedge PostgreSQL partial and expression index details and SQL Server filtered indexes as not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** A partial index is used only when the query's WHERE clearly implies the index's WHERE (in SQLite 3.45.1 `status = 'placed'` and a bound `status = ?` qualify, `IN ('placed')` and `!=` did not), an expression index is used only when the query contains the exact same expression, and a UNIQUE index treats NULLs as distinct so it allows several.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT, email TEXT);
INSERT INTO orders VALUES (1,'placed','2024-06-01','Asha@Mail.com'),(2,'delivered','2024-06-02','ben@mail.com'),
 (3,'placed','2024-06-03',NULL),(4,'delivered','2024-06-04',NULL);
CREATE UNIQUE INDEX ux_email ON orders(email);
```

**SQL answer:** The three indexes and the probe queries are in the Code block, copied here (the full probe list is the `Q` and `E` lists):
```sql
CREATE INDEX ix_placed ON orders(order_date) WHERE status = 'placed'
CREATE INDEX ix_lower_email ON orders(lower(email))
CREATE UNIQUE INDEX ux_email ON orders(email)
CREATE INDEX ix_full ON orders(order_date)
SELECT order_id FROM orders WHERE status = 'placed' AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE status IN ('placed') AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE status != 'delivered' AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE status = ? AND order_date > '2024-11-01'
SELECT order_id FROM orders WHERE lower(email) = ?
```

**pandas answer:** Row-for-row filters that the code asserts against the SQL results.
```py
exp = df[(df.status == "placed") & (df.order_date > "2024-11-01")]
```

**Example:** Tiny table: orders 1 and 3 are 'placed'. The partial index ix_placed would hold only those two rows (entries for dates 2024-06-01 and 2024-06-03); orders 2 and 4 are not in it at all. `status = 'placed' AND order_date > '2024-06-02'` is answered from it (order 3). The UNIQUE index on email holds 'Asha@Mail.com', 'ben@mail.com' and two NULL entries: the two NULLs do not conflict (count printed: 2), a second 'ben@mail.com' fails with `UNIQUE constraint failed: orders.email`, and 'BEN@mail.com' is accepted because the default comparison is case-sensitive. At 200,000 rows (6,064 placed, 3.03%) the query `status = 'placed' AND order_date > '2024-11-01'` returned 982 rows, which equals the pandas filter.

**Code:** run with `python3 -I`.
```python
# Q22: partial, expression and unique indexes
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql, params=()):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0], params)]

# tiny sample
t = sqlite3.connect(":memory:")
t.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT, email TEXT);
INSERT INTO orders VALUES (1,'placed','2024-06-01','Asha@Mail.com'),(2,'delivered','2024-06-02','ben@mail.com'),(3,'placed','2024-06-03',NULL),(4,'delivered','2024-06-04',NULL);
CREATE UNIQUE INDEX ux_email ON orders(email);
""")
print("tiny: two NULL emails coexist under UNIQUE:", t.execute("SELECT COUNT(*) FROM orders WHERE email IS NULL").fetchone()[0])
try:
    t.execute("INSERT INTO orders VALUES (5,'placed','2024-06-05','ben@mail.com')")
except sqlite3.IntegrityError as e:
    print("tiny: duplicate non-NULL email ->", type(e).__name__, e)
t.execute("INSERT INTO orders VALUES (6,'placed','2024-06-06','BEN@mail.com')")
print("tiny: 'BEN@mail.com' is accepted next to 'ben@mail.com' (UNIQUE is case-sensitive, BINARY)")

# scaled data: 200,000 rows
rnd = random.Random(22)
rows = []
for i in range(1, 200001):
    st = "placed" if rnd.random() < 0.03 else rnd.choice(["delivered", "delivered", "shipped", "cancelled"])
    local = "user%d" % i
    email = None if rnd.random() < 0.05 else (local.upper() if rnd.random() < 0.3 else local.capitalize()) + "@Example.COM"
    rows.append((i, rnd.randint(1, 20000), st, "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 500), email))
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, order_date TEXT, amount INTEGER, email TEXT)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?)", rows)
con.commit()
df = pd.read_sql("SELECT * FROM orders", con)
print("\nplaced rows: %d of %d (%.2f%%)" % ((df.status == "placed").sum(), len(df), 100 * (df.status == "placed").mean()))

con.execute("CREATE INDEX ix_placed ON orders(order_date) WHERE status = 'placed'")
con.execute("CREATE INDEX ix_lower_email ON orders(lower(email))")
con.execute("CREATE UNIQUE INDEX ux_email ON orders(email)")
con.commit()

Q = [
 ("status = 'placed' AND order_date > ...", "SELECT order_id FROM orders WHERE status = 'placed' AND order_date > '2024-11-01'", ()),
 ("status IN ('placed') AND ...", "SELECT order_id FROM orders WHERE status IN ('placed') AND order_date > '2024-11-01'", ()),
 ("status != 'delivered' AND ...", "SELECT order_id FROM orders WHERE status != 'delivered' AND order_date > '2024-11-01'", ()),
 ("status = ? (bound) AND ...", "SELECT order_id FROM orders WHERE status = ? AND order_date > '2024-11-01'", ("placed",)),
 ("order_date > ... only", "SELECT order_id FROM orders WHERE order_date > '2024-11-01'", ()),
]
print("\nPARTIAL INDEX ix_placed(order_date) WHERE status = 'placed'")
for nm, sql, p in Q:
    r, n = steps(con, sql, p)
    print(" %-40s rows %5d steps %8d  %s" % (nm, len(r), n, plan(con, sql, p)))
exp = df[(df.status == "placed") & (df.order_date > "2024-11-01")]
assert sorted(x[0] for x in steps(con, Q[0][1])[0]) == sorted(exp.order_id)
assert sorted(x[0] for x in steps(con, Q[3][1], ("placed",))[0]) == sorted(exp.order_id)

target = df.email.dropna().iloc[1234]
E = [
 ("lower(email) = ?", "SELECT order_id FROM orders WHERE lower(email) = ?", (target.lower(),)),
 ("lower(email) = lower(?)", "SELECT order_id FROM orders WHERE lower(email) = lower(?)", (target,)),
 ("upper(email) = ?", "SELECT order_id FROM orders WHERE upper(email) = ?", (target.upper(),)),
 ("lower(trim(email)) = ?", "SELECT order_id FROM orders WHERE lower(trim(email)) = ?", (target.lower(),)),
 ("email = ? (exact)", "SELECT order_id FROM orders WHERE email = ?", (target,)),
 ("email = ? COLLATE NOCASE", "SELECT order_id FROM orders WHERE email = ? COLLATE NOCASE", (target.lower(),)),
 ("email LIKE ? (case-insensitive)", "SELECT order_id FROM orders WHERE email LIKE ?", (target.lower(),)),
]
print("\nEXPRESSION AND UNIQUE INDEXES, target email", target)
for nm, sql, p in E:
    r, n = steps(con, sql, p)
    print(" %-32s rows %d steps %8d  %s" % (nm, len(r), n, plan(con, sql, p)))
want = df[df.email.str.lower() == target.lower()]["order_id"].tolist()
assert [x[0] for x in con.execute(E[0][1], E[0][2])] == want
print("lower(email) lookup rows match pandas str.lower() filter:", want)

nulls = int(df.email.isna().sum())
print("\nNULL emails in the UNIQUE-indexed column: %d (all allowed)" % nulls)
assert con.execute("SELECT COUNT(*) FROM orders WHERE email IS NULL").fetchone()[0] == nulls
try:
    con.execute("INSERT INTO orders(customer_id,status,order_date,amount,email) VALUES (1,'placed','2024-01-01',1,?)", (target,))
except sqlite3.IntegrityError as e:
    print("duplicate insert ->", e)

# sizes
con.execute("CREATE INDEX ix_full ON orders(order_date)")
con.commit()
print("\nINDEX SIZES (dbstat bytes and pages, page_size %d)" % con.execute("PRAGMA page_size").fetchone()[0])
for nm in ("ix_placed", "ix_full", "ix_lower_email", "ux_email"):
    b, p = con.execute("SELECT SUM(pgsize), COUNT(*) FROM dbstat WHERE name = ?", (nm,)).fetchone()
    print("  %-15s %9d bytes %5d pages" % (nm, b, p))
b, p = con.execute("SELECT SUM(pgsize), COUNT(*) FROM dbstat WHERE name = 'orders'").fetchone()
print("  %-15s %9d bytes %5d pages (the table itself)" % ("orders", b, p))

# write cost: insert 'delivered' rows with only the partial index vs only the full index
import time
def insert_cost(index_sql):
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT)")
    c.execute(index_sql)
    batch = [(i, "delivered", "2024-%02d-%02d" % (1 + i % 12, 1 + i % 28)) for i in range(1, 100001)]
    n = [0]
    def cb():
        n[0] += 1
        return 0
    t0 = time.perf_counter()
    c.set_progress_handler(cb, 1)
    c.executemany("INSERT INTO orders VALUES (?,?,?)", batch)
    c.set_progress_handler(None, 0)
    c.commit()
    ms = (time.perf_counter() - t0) * 1000
    pages = c.execute("SELECT COUNT(*) FROM dbstat WHERE name = 'i'").fetchone()[0]
    return n[0], ms, pages
for label, ddl in (("partial index", "CREATE INDEX i ON orders(order_date) WHERE status = 'placed'"),
                   ("full index", "CREATE INDEX i ON orders(order_date)"),
                   ("no index", "CREATE TABLE IF NOT EXISTS unused(x)")):
    n, ms, pages = insert_cost(ddl)
    print("insert 100,000 'delivered' rows, %-13s: progress callbacks %d, index pages %d, wall %.0f ms (machine-specific, single run)" % (label, n, pages, ms))
```

**Output (my run):**
```text
tiny: two NULL emails coexist under UNIQUE: 2
tiny: duplicate non-NULL email -> IntegrityError UNIQUE constraint failed: orders.email
tiny: 'BEN@mail.com' is accepted next to 'ben@mail.com' (UNIQUE is case-sensitive, BINARY)

placed rows: 6064 of 200000 (3.03%)

PARTIAL INDEX ix_placed(order_date) WHERE status = 'placed'
 status = 'placed' AND order_date > ...   rows   982 steps     2958  ['SEARCH orders USING COVERING INDEX ix_placed (order_date>?)']
 status IN ('placed') AND ...             rows   982 steps   614102  ['SCAN orders']
 status != 'delivered' AND ...            rows 16839 steps   839434  ['SCAN orders']
 status = ? (bound) AND ...               rows   982 steps     5907  ['SEARCH orders USING COVERING INDEX ix_placed (order_date>?)']
 order_date > ... only                    rows 32837 steps   665682  ['SCAN orders']

EXPRESSION AND UNIQUE INDEXES, target email User1298@Example.COM
 lower(email) = ?                 rows 1 steps       17  ['SEARCH orders USING INDEX ix_lower_email (<expr>=?)']
 lower(email) = lower(?)          rows 1 steps       19  ['SEARCH orders USING INDEX ix_lower_email (<expr>=?)']
 upper(email) = ?                 rows 1 steps   800011  ['SCAN orders USING COVERING INDEX ux_email']
 lower(trim(email)) = ?           rows 1 steps  1000011  ['SCAN orders USING COVERING INDEX ux_email']
 email = ? (exact)                rows 1 steps       11  ['SEARCH orders USING COVERING INDEX ux_email (email=?)']
 email = ? COLLATE NOCASE         rows 1 steps   600011  ['SCAN orders USING COVERING INDEX ux_email']
 email LIKE ? (case-insensitive)  rows 1 steps   800013  ['SCAN orders USING COVERING INDEX ux_email']
lower(email) lookup rows match pandas str.lower() filter: [1298]

NULL emails in the UNIQUE-indexed column: 9938 (all allowed)
duplicate insert -> UNIQUE constraint failed: orders.email

INDEX SIZES (dbstat bytes and pages, page_size 4096)
  ix_placed          118784 bytes    29 pages
  ix_full           3792896 bytes   926 pages
  ix_lower_email    5890048 bytes  1438 pages
  ux_email          5890048 bytes  1438 pages
  orders           11223040 bytes  2740 pages (the table itself)
insert 100,000 'delivered' rows, partial index: progress callbacks 2000003, index pages 1, wall 363 ms (machine-specific, single run)
insert 100,000 'delivered' rows, full index   : progress callbacks 2000003, index pages 516, wall 432 ms (machine-specific, single run)
insert 100,000 'delivered' rows, no index     : progress callbacks 1400003, index pages 0, wall 245 ms (machine-specific, single run)
```

**Edge cases:**
- Implication is syntactic and conservative: `status IN ('placed')` means the same as `= 'placed'` but SQLite 3.45.1 scanned the table (614,102 steps against 2,958). `status != 'delivered'` is not implied by `status = 'placed'` anyway (it also matches other statuses) and scanned. A bound parameter `status = ?` did use the index (5,907 steps): the planner accepts a parameter for the equality here; I did not test what happens in other engines.
- A query with no status condition cannot use the partial index (it would miss rows): SCAN.
- UNIQUE on a mixed-case email does not make emails unique ignoring case: add a unique expression index on lower(email) for that (not run here; the lower(email) expression index in the code is non-unique).
- NULL emails: 9,938 of 200,000 rows are NULL and all coexist under the UNIQUE index.

**Then explain:**
- Which query used which index (plans printed in the output): `status = 'placed' AND order_date > ...` used `COVERING INDEX ix_placed (order_date>?)`; `IN ('placed')`, `!=` and the no-status query scanned. `lower(email) = ?` used `ix_lower_email (<expr>=?)` (17 steps), as did `lower(email) = lower(?)`. `upper(email) = ?`, `lower(trim(email)) = ?`, `email = ? COLLATE NOCASE` and `email LIKE ?` all scanned (the plan shows a scan of the narrowest covering index ux_email, 600,011 to 1,000,011 steps). `email = ?` used the UNIQUE index (11 steps). The expression must match exactly.
- Size (dbstat, 4,096-byte pages): partial ix_placed 29 pages (118,784 bytes) against full ix_full 926 pages (3,792,896 bytes), about 3% of the size; ix_lower_email and ux_email 1,438 pages each; the table 2,740 pages.
- Write cost: a partial index is only maintained for rows that satisfy its WHERE, so inserts and updates of the other 97% do not touch it. In a 100,000-row insert of non-'placed' rows the partial index ended with 1 page against 516 for the full index, and wall time was 363 ms against 432 ms (no index: 245 ms; machine-specific single runs). The VM-step proxy did NOT show a difference (2,000,003 callbacks for both), because the progress handler counts jump-style opcodes and the cheap skip is not visible there; do not use steps for this comparison.
- Benefits: smaller index, cheaper writes for rows outside the predicate, and a UNIQUE rule that can be limited to a subset (e.g. one active row per customer, not run here).
- Other engines, not executed: PostgreSQL partial and expression indexes have the same idea (the planner must be able to prove the query predicate implies the index predicate, and parameterised queries and generic plans can change that; check with EXPLAIN there). SQL Server filtered indexes are similar but are reported to be restricted for parameterised queries unless the plan is recompiled, and SQL Server and PostgreSQL treat NULLs in unique indexes differently (SQL Server allows one NULL in a unique index; PostgreSQL allows many, and newer versions have NULLS NOT DISTINCT). All of this is from memory and was not run.

**Follow-ups:**
- What is the risk of an expression index? (Every query and every ORM must write the same expression; a different function or collation silently scans.)
- Would ANALYZE change any of these plans? (Not tested in this answer.)
- How would you enforce case-insensitive uniqueness? (UNIQUE index on lower(email), or a NOCASE collation on the column; the lower(email) unique variant is not run here.)

**Common mistakes:**
- Assuming `IN ('placed')` or `!=` will use a partial index.
- Testing the expression index with `lower(trim(email))` or `upper(email)` and concluding indexes are broken.
- Believing UNIQUE rejects multiple NULLs (SQLite and PostgreSQL allow them; engines differ).
- Counting a partial index as free: the table still pays for all other indexes.

### Q23 ⭐⭐ 🟡 Write cost: batching inserts and transactions. Insert 100,000 seeded rows into events(event_id, user_id, event_type, event_time) in a file-backed SQLite database in four ways: one INSERT and commit per row (use 2,000 rows only), a single transaction with execute in a loop, executemany inside one transaction, and executemany after creating indexes versus creating the indexes afterwards. Report VM steps (deterministic) and wall-clock timings labelled machine-specific, show PRAGMA journal_mode and synchronous, explain why per-row commits are slow (each commit syncs to disk), why bulk loads add indexes after loading, parameter binding (prepared statements) versus string formatting, and mention multi-row INSERT, COPY (PostgreSQL), LOAD DATA (MySQL) and bulk-load paths in warehouses as not executed.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Each commit forces a sync to disk, so one commit per row costs milliseconds per row, while one transaction (with executemany and bound parameters) costs microseconds per row; load first, create indexes afterwards, and never build SQL with string formatting.

**Schema and sample data:**
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, event_time TEXT);
INSERT INTO events VALUES (1,17,'view','2024-01-01'),(2,17,'click','2024-01-01'),(3,42,'buy','2024-01-02');
```

**SQL answer:** The statements are the constants `DDL`, `INS` and the three `CREATE INDEX` strings in `IDX`; the load shapes are the Python functions in the Code block:
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, event_time TEXT)
INSERT INTO events VALUES (?,?,?,?)
CREATE INDEX ix_user ON events(user_id)
CREATE INDEX ix_type ON events(event_type)
CREATE INDEX ix_time ON events(event_time)
```

**pandas answer:** pandas holds the same seeded rows and is the checksum for every load.
```py
pdf = pd.DataFrame(data, columns=["event_id", "user_id", "event_type", "event_time"])
```

**Example:** Three rows go in. With a commit per row there are three transactions: three journal writes and three syncs. In one transaction there is one commit and one sync for all three rows. For 100,000 rows the same logic applies at scale: 100,000 syncs against one. The checksum in the code (row count and SUM(user_id) against the pandas frame) proves every method stored the same rows.

**Code:** run with `python3 -I`.
```python
# Q23: write cost: batching inserts and transactions (file-backed SQLite)
import sqlite3, random, os, tempfile, time
import pandas as pd

random.seed(23)
N = 100_000
types = ["view", "click", "cart", "buy"]
data = [(i, random.randint(1, 5000), random.choice(types), "2024-%02d-%02d" % (random.randint(1, 12), random.randint(1, 28)))
        for i in range(1, N + 1)]
pdf = pd.DataFrame(data, columns=["event_id", "user_id", "event_type", "event_time"])
DDL = "CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_type TEXT, event_time TEXT)"
INS = "INSERT INTO events VALUES (?,?,?,?)"
IDX = ["CREATE INDEX ix_user ON events(user_id)", "CREATE INDEX ix_type ON events(event_type)", "CREATE INDEX ix_time ON events(event_time)"]
tmp = tempfile.TemporaryDirectory()

def fresh(name):
    path = os.path.join(tmp.name, name + ".db")
    con = sqlite3.connect(path)
    con.execute(DDL)
    con.commit()
    return con

def run(label, fn, con, expect_rows):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    t0 = time.perf_counter()
    fn(con)
    ms = (time.perf_counter() - t0) * 1000
    con.set_progress_handler(None, 0)
    cnt, s = con.execute("SELECT COUNT(*), SUM(user_id) FROM events").fetchone()
    assert cnt == expect_rows
    assert s == int(pdf["user_id"].iloc[:expect_rows].sum())       # same rows as the pandas frame
    print("%-52s rows %6d  progress steps %9d  wall %8.1f ms" % (label, cnt, n[0], ms))
    return n[0], ms

con = fresh("probe")
print("journal_mode =", con.execute("PRAGMA journal_mode").fetchone()[0], "| synchronous =", con.execute("PRAGMA synchronous").fetchone()[0], "(2 = FULL)")
con.close()

def per_row(con):
    for r in data[:2000]:
        con.execute(INS, r)
        con.commit()
def loop_one_txn(con):
    for r in data:
        con.execute(INS, r)
    con.commit()
def many(con):
    con.executemany(INS, data)
    con.commit()
def multirow(con, k=500):
    for i in range(0, N, k):
        chunk = data[i:i + k]
        con.execute("INSERT INTO events VALUES " + ",".join(["(?,?,?,?)"] * len(chunk)), [v for r in chunk for v in r])
    con.commit()
def indexes_first(con):
    for s in IDX: con.execute(s)
    con.executemany(INS, data); con.commit()
def indexes_after(con):
    con.executemany(INS, data)
    for s in IDX: con.execute(s)
    con.commit()
def fmt_strings(con):                          # unsafe string formatting, shown only for cost
    for r in data:
        con.execute("INSERT INTO events VALUES (%d,%d,'%s','%s')" % r)
    con.commit()

print("\n-- commit granularity (default journal_mode, synchronous=FULL)")
a = run("1. execute + commit per row, 2,000 rows only", per_row, fresh("a"), 2000)
b = run("2. execute in a loop, one transaction, 100,000 rows", loop_one_txn, fresh("b"), N)
c = run("3. executemany, one transaction, 100,000 rows", many, fresh("c"), N)
d = run("3b. multi-row INSERT VALUES (500 rows per statement)", multirow, fresh("d"), N)
e = run("3c. execute with string formatting (not safe), one txn", fmt_strings, fresh("e"), N)
print("per-row commit costs %.2f ms per row; executemany costs %.4f ms per row (machine-specific)" % (a[1] / 2000, c[1] / N))

print("\n-- three secondary indexes before versus after the load (executemany, one transaction)")
f = run("4a. indexes created BEFORE loading", indexes_first, fresh("f"), N)
g = run("4b. indexes created AFTER loading", indexes_after, fresh("g"), N)

print("\n-- per-row commits under other settings (2,000 rows, machine-specific)")
settings = [("journal_mode=WAL, synchronous=FULL", ["PRAGMA journal_mode=WAL"]),
            ("journal_mode=WAL, synchronous=NORMAL", ["PRAGMA journal_mode=WAL", "PRAGMA synchronous=NORMAL"]),
            ("journal_mode=DELETE, synchronous=OFF", ["PRAGMA synchronous=OFF"])]
for j, (label, pragmas) in enumerate(settings):
    con = fresh("h%d" % j)
    for p in pragmas:
        con.execute(p).fetchall()
    run("5. per-row commit, " + label, per_row, con, 2000)

# the safe path: parameters. A quote in the data breaks the formatted statement
c2 = fresh("q")
try:
    c2.execute("INSERT INTO events VALUES (1,1,'it's','x')")
except sqlite3.OperationalError as ex:
    print("\nformatted SQL with a quote in the value ->", ex)
c2.execute(INS, (1, 1, "it's", "x"))
print("bound parameters store it safely:", c2.execute("SELECT event_type FROM events").fetchone()[0])
print("compile option for the bound-variable limit:", [o for o in sqlite3.connect(":memory:").execute("PRAGMA compile_options") if "MAX_VARIABLE" in o[0]])
print("asserts passed: every load produced the same row count and SUM(user_id) as the pandas frame")
tmp.cleanup()
```

**Output (my run):**
```text
journal_mode = delete | synchronous = 2 (2 = FULL)

-- commit granularity (default journal_mode, synchronous=FULL)
1. execute + commit per row, 2,000 rows only         rows   2000  progress steps     42000  wall   2179.2 ms
2. execute in a loop, one transaction, 100,000 rows  rows 100000  progress steps   1500006  wall    341.6 ms
3. executemany, one transaction, 100,000 rows        rows 100000  progress steps   1500006  wall    306.0 ms
3b. multi-row INSERT VALUES (500 rows per statement) rows 100000  progress steps   1401606  wall    257.4 ms
3c. execute with string formatting (not safe), one txn rows 100000  progress steps   1500006  wall    593.3 ms
per-row commit costs 1.09 ms per row; executemany costs 0.0031 ms per row (machine-specific)

-- three secondary indexes before versus after the load (executemany, one transaction)
4a. indexes created BEFORE loading                   rows 100000  progress steps   3100168  wall    985.8 ms
4b. indexes created AFTER loading                    rows 100000  progress steps   4200168  wall    719.9 ms

-- per-row commits under other settings (2,000 rows, machine-specific)
5. per-row commit, journal_mode=WAL, synchronous=FULL rows   2000  progress steps     42000  wall    575.1 ms
5. per-row commit, journal_mode=WAL, synchronous=NORMAL rows   2000  progress steps     42000  wall     46.9 ms
5. per-row commit, journal_mode=DELETE, synchronous=OFF rows   2000  progress steps     42000  wall     99.5 ms

formatted SQL with a quote in the value -> near "s": syntax error
bound parameters store it safely: it's
compile option for the bound-variable limit: [('MAX_VARIABLE_NUMBER=250000',)]
asserts passed: every load produced the same row count and SUM(user_id) as the pandas frame
```

**Edge cases:**
- Per-row commit was run on 2,000 rows only (as asked); 100,000 syncs would take minutes on this storage. The per-row figures are not extrapolated into a total in the text.
- VM steps are the same per row for commit-per-row (21 steps per row) and for one transaction (15 per row): commit-and-sync cost is I/O wait, not VM work, so the deterministic step count cannot show it. Only wall-clock shows it, so the timings below are the evidence and they are machine- and disk-specific single runs.
- File-backed database in a temporary directory; storage type, filesystem and fsync behaviour change the numbers a lot (WAL with synchronous=NORMAL is far faster for per-row commits but gives up some durability on power loss).

**Then explain:**
- Results in my run (machine-specific): commit per row 2,000 rows took about 2.2 seconds, around 1.1 ms per row; the same loop in one transaction inserted 100,000 rows in about 0.34 s (a few microseconds per row); executemany took about the same (0.31 s), because the loop overhead of Python is small next to the commit. A multi-row INSERT with 500 rows per statement was a little faster (0.26 s) and used the fewest VM steps (1,401,606 against 1,500,006). String formatting took longer (0.59 s) and cannot bind a value that contains a quote (the run shows `near "s": syntax error`) and is an injection hole: bound parameters are also faster because the statement is prepared once and reused.
- Settings printed: `PRAGMA journal_mode` = delete and `PRAGMA synchronous` = 2 (FULL) by default. For 2,000 per-row commits: WAL with synchronous=FULL about 0.58 s, WAL with synchronous=NORMAL about 0.05 s, journal_mode delete with synchronous=OFF about 0.1 s. Fewer syncs, faster commits; the price is durability, which is a business decision.
- Indexes: with three secondary indexes created BEFORE the load the insert took 3,100,168 steps and about 1.0 s; creating them AFTER the load took 4,200,168 steps but about 0.7 s. The step count went UP while the time went DOWN: a bulk index build sorts the keys and appends them in order instead of doing a random B-tree insert per row, and that is I/O and cache behaviour that VM steps do not capture. Use steps only for what they measure.
- Not executed here: PostgreSQL COPY, MySQL LOAD DATA, and bulk-load paths in warehouses (stage files then COPY or LOAD) are the same idea at a larger scale: few large operations rather than many small ones. Multi-row INSERT VALUES is standard SQL and was run on SQLite; its row limits differ by engine (SQLite's compile option here is MAX_VARIABLE_NUMBER=250000 bound variables, printed in the run).

**Follow-ups:**
- What does executemany do beyond the loop? (Reuses one prepared statement; the speed-up over a per-row execute in one transaction was small here.)
- What is the durability trade-off of synchronous=NORMAL or OFF? (A crash or power loss can lose recent commits or corrupt data in OFF mode.)
- Would you load into an indexed table if it is live? (Yes if readers need it; for a one-off bulk load, drop or defer indexes.)

**Common mistakes:**
- Calling commit inside the loop 'to be safe'.
- Leaving autocommit on with the Python default and wondering why it is slow (each INSERT outside a transaction commits).
- Building SQL with f-strings.
- Quoting wall-clock timings as if they were deterministic.

### Q24 ⭐⭐ 🟡 The N+1 query pattern from application code: customers(customer_id, name) 100 seeded rows and orders(order_id, customer_id, amount) 1,000 rows. Write the loop that fetches the customer list and then runs one query per customer, count the statements with Connection.set_trace_callback (101), then replace it with one JOIN/GROUP BY query (1 statement) and with one IN (?, ?, ...) batched query, assert the same data, and print the plan of the per-customer lookup. Explain why N+1 is a round-trip problem that grows with network latency (the SQLite example is in-process so its time is misleading: say so), the ORM lazy-loading origin and eager-loading fixes (described, no ORM executed), batching limits on IN lists (SQLite's variable limit, check compile options), and the pandas equivalent of looping over rows with read_sql per row versus one read_sql plus merge.
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** N+1 is one query for the list plus one query per row, 101 statements here against 1 (JOIN + GROUP BY) or 2 (a batched IN); in-process SQLite hides the cost, but against a networked database every extra statement is a round trip, so latency multiplies by N.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'cust001'),(2,'cust002'),(3,'cust003');
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,3,70);
```

**SQL answer:** The three shapes are in the Code block (the loop statement, the JOIN/GROUP BY and the batched IN), copied here:
```sql
SELECT customer_id, name FROM customers ORDER BY customer_id
SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = ?
SELECT c.customer_id, c.name, COUNT(o.order_id), COALESCE(SUM(o.amount),0)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name ORDER BY c.customer_id
SELECT customer_id, amount FROM orders WHERE customer_id IN (%s)
```

**pandas answer:** Per-row `read_sql` in a loop versus one `read_sql`, groupby and merge (both are in the Code block, copied here):
```py
agg = ord_df.groupby("customer_id")["amount"].agg(cnt="size", total="sum").reset_index()
```

**Example:** Tiny table: customer 1 has orders of 100 and 50 (count 2, total 150), customer 2 has none (count 0, total 0), customer 3 has 70. The N+1 loop issues the list query and then three lookups: 4 statements, in general 1 + N. The JOIN with GROUP BY returns the same three rows in one statement; the LEFT JOIN keeps customer 2 with count 0. At scale (100 customers, 1,000 orders) the trace callback counted exactly 101, 1 and 2 statements, and the three results are asserted equal.

**Code:** run with `python3 -I`.
```python
# Q24: the N+1 query pattern
import sqlite3, random, time
import pandas as pd

random.seed(24)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
""")
con.executemany("INSERT INTO customers VALUES (?,?)", [(i, "cust%03d" % i) for i in range(1, 101)])
con.executemany("INSERT INTO orders VALUES (?,?,?)", [(i, random.randint(1, 100), random.randint(10, 500)) for i in range(1, 1001)])
con.commit()

class Counter:
    def __init__(self, c):
        self.stmts = []
        c.set_trace_callback(self.stmts.append)
    def reset(self):
        self.stmts.clear()
ctr = Counter(con)

# 1. N+1: one query for the list, then one per customer
ctr.reset()
t0 = time.perf_counter()
customers = con.execute("SELECT customer_id, name FROM customers ORDER BY customer_id").fetchall()
n_plus_1 = []
for cid, name in customers:
    tot, cnt = con.execute("SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = ?", (cid,)).fetchone()
    n_plus_1.append((cid, name, cnt, tot))
t1 = (time.perf_counter() - t0) * 1000
print("N+1 loop: %d statements; first three traced:" % len(ctr.stmts))
for s in ctr.stmts[:3]: print("   ", s)
assert len(ctr.stmts) == 101

# 2. one JOIN + GROUP BY
ctr.reset()
t0 = time.perf_counter()
joined = con.execute("""SELECT c.customer_id, c.name, COUNT(o.order_id), COALESCE(SUM(o.amount),0)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.name ORDER BY c.customer_id""").fetchall()
t2 = (time.perf_counter() - t0) * 1000
print("JOIN + GROUP BY: %d statement" % len(ctr.stmts))
assert len(ctr.stmts) == 1

# 3. one batched IN (?, ?, ...) query, then group in Python
ctr.reset()
t0 = time.perf_counter()
ids = [c[0] for c in con.execute("SELECT customer_id FROM customers ORDER BY customer_id")]
ph = ",".join("?" * len(ids))
fetched = con.execute("SELECT customer_id, amount FROM orders WHERE customer_id IN (%s)" % ph, ids).fetchall()
agg = {}
for cid, amt in fetched:
    c, s = agg.get(cid, (0, 0)); agg[cid] = (c + 1, s + amt)
names = dict(customers)
batched = [(cid, names[cid], *agg.get(cid, (0, 0))) for cid in ids]
t3 = (time.perf_counter() - t0) * 1000
print("batched IN: %d statements (1 for ids + 1 for orders)" % len(ctr.stmts))
assert len(ctr.stmts) == 2
assert n_plus_1 == joined == batched
print("asserts passed: N+1, JOIN and batched IN give the same 100 rows (customer_id, name, order_count, total)")
print("in-process times (machine-specific, MISLEADING for a network database): N+1 %.2f ms, JOIN %.2f ms, IN %.2f ms" % (t1, t2, t3))
print("simulated latency of 0.5 ms per round trip (arithmetic, not a measurement): N+1 adds %.1f ms, JOIN adds %.1f ms, IN adds %.1f ms" % (101 * 0.5, 1 * 0.5, 2 * 0.5))

print("\nplan of the per-customer lookup, no index:", [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT SUM(amount) FROM orders WHERE customer_id = ?", (5,))])
con.execute("CREATE INDEX ix_orders_cust ON orders(customer_id)")
print("plan with index on orders(customer_id):  ", [r[3] for r in con.execute("EXPLAIN QUERY PLAN SELECT SUM(amount) FROM orders WHERE customer_id = ? ", (5,))])

n = [0]
def cb():
    n[0] += 1
    return 0
def vm(sql, p=()):
    n[0] = 0; con.set_progress_handler(cb, 1); con.execute(sql, p).fetchall(); con.set_progress_handler(None, 0); return n[0]
loop_steps = sum(vm("SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = ?", (cid,)) for cid in ids)
print("VM steps with the index: 100 lookups total %d; the single JOIN/GROUP BY query %d" % (loop_steps, vm("""SELECT c.customer_id, COUNT(o.order_id), COALESCE(SUM(o.amount),0)
FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id GROUP BY c.customer_id""")))

opts = [o[0] for o in con.execute("PRAGMA compile_options") if "MAX_VARIABLE" in o[0]]
print("\nbound-variable limit compile option:", opts)
big = list(range(1, 300001))
try:
    con.execute("SELECT COUNT(*) FROM orders WHERE customer_id IN (%s)" % ",".join("?" * len(big)), big)
except sqlite3.Error as ex:
    print("IN list with 300,000 placeholders ->", type(ex).__name__, ex)
chunks = [ids[i:i + 30] for i in range(0, len(ids), 30)]
tot = sum(con.execute("SELECT COUNT(*) FROM orders WHERE customer_id IN (%s)" % ",".join("?" * len(ch)), ch).fetchone()[0] for ch in chunks)
print("chunked IN (4 chunks of up to 30 ids): %d orders counted, table has %d" % (tot, con.execute("SELECT COUNT(*) FROM orders").fetchone()[0]))

# pandas: read_sql per row versus one read_sql + merge
ctr.reset()
rows = []
cust_df = pd.read_sql("SELECT * FROM customers ORDER BY customer_id", con)
for cid in cust_df["customer_id"]:
    one = pd.read_sql("SELECT COALESCE(SUM(amount),0) AS total, COUNT(*) AS cnt FROM orders WHERE customer_id = ?", con, params=(int(cid),))
    rows.append((int(cid), int(one.at[0, "cnt"]), int(one.at[0, "total"])))
loop_df = pd.DataFrame(rows, columns=["customer_id", "cnt", "total"])
print("\npandas per-row read_sql loop: %d statements" % len(ctr.stmts))
ctr.reset()
ord_df = pd.read_sql("SELECT customer_id, amount FROM orders", con)
agg = ord_df.groupby("customer_id")["amount"].agg(cnt="size", total="sum").reset_index()
merged = cust_df.merge(agg, on="customer_id", how="left").fillna({"cnt": 0, "total": 0}).astype({"cnt": "int64", "total": "int64"})
print("pandas one read_sql + groupby + merge: %d statements" % len(ctr.stmts))
pd.testing.assert_frame_equal(loop_df, merged[["customer_id", "cnt", "total"]])
print("asserts passed: both pandas versions equal (sorted by customer_id)")
```

**Output (my run):**
```text
N+1 loop: 101 statements; first three traced:
    SELECT customer_id, name FROM customers ORDER BY customer_id
    SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = 1
    SELECT COALESCE(SUM(amount),0), COUNT(*) FROM orders WHERE customer_id = 2
JOIN + GROUP BY: 1 statement
batched IN: 2 statements (1 for ids + 1 for orders)
asserts passed: N+1, JOIN and batched IN give the same 100 rows (customer_id, name, order_count, total)
in-process times (machine-specific, MISLEADING for a network database): N+1 4.65 ms, JOIN 0.95 ms, IN 1.24 ms
simulated latency of 0.5 ms per round trip (arithmetic, not a measurement): N+1 adds 50.5 ms, JOIN adds 0.5 ms, IN adds 1.0 ms

plan of the per-customer lookup, no index: ['SCAN orders']
plan with index on orders(customer_id):   ['SEARCH orders USING INDEX ix_orders_cust (customer_id=?)']
VM steps with the index: 100 lookups total 7700; the single JOIN/GROUP BY query 15219

bound-variable limit compile option: ['MAX_VARIABLE_NUMBER=250000']
IN list with 300,000 placeholders -> OperationalError too many SQL variables
chunked IN (4 chunks of up to 30 ids): 1000 orders counted, table has 1000

pandas per-row read_sql loop: 101 statements
pandas one read_sql + groupby + merge: 1 statements
asserts passed: both pandas versions equal (sorted by customer_id)
```

**Edge cases:**
- Customers without orders: the loop form gives (0, 0) through COALESCE and the JOIN needs a LEFT JOIN (with an INNER JOIN they would vanish, and the assert would fail).
- The batched IN query returns raw order rows, so the grouping happens in Python; customers with no orders are filled with (0, 0) in the code.
- An empty id list makes `IN ()`: build the placeholders from a non-empty list or skip the query.

**Then explain:**
- Why N+1 hurts: each statement costs a round trip (network latency plus parse and plan). In-process SQLite has no network, so the timing is misleading: the loop took about 4.5 ms and the JOIN about 1 ms in my run (machine-specific), a small absolute difference. Illustrative arithmetic only, not a measurement: at an assumed 0.5 ms per round trip, 101 statements add about 50 ms while 1 statement adds 0.5 ms, and for 10,000 rows N+1 would add 5 seconds.
- Even in process the plan of the per-customer lookup matters: `SCAN orders` without an index (so the loop reads the whole orders table 100 times) and `SEARCH orders USING INDEX ix_orders_cust (customer_id=?)` with one. With the index, 100 lookups took 7,700 VM steps and the single JOIN/GROUP BY 15,219 steps (it reads all 1,000 orders): in VM steps N+1 was not worse. The cost of N+1 is latency, not engine work, which is why in-process counts hide it.
- ORM origin (described, no ORM executed): lazy loading fetches related rows when an attribute is first touched, so iterating over 100 parents and reading `parent.children` triggers 100 child queries. Eager-loading options (a JOIN fetch, or a second query with IN over the parent ids, usually called select-in or batch loading) turn it into 1 or 2 statements. Check the ORM's SQL log, as this answer does with `set_trace_callback`.
- Batching limits: an IN list is limited by the engine's bound-variable limit. SQLite here reports `MAX_VARIABLE_NUMBER=250000`; an IN list of 300,000 placeholders failed with `OperationalError too many SQL variables`. Other engines have their own limits (hedged, not executed); chunk the ids (the code runs 4 chunks of up to 30 ids).
- pandas: loading customers and then calling `read_sql` once per customer produced 101 statements (1 + 100); one `read_sql` for orders followed by `groupby` and `merge` produced 1 statement (the customers frame was reused from the first part; reading it again would make 2).

**Follow-ups:**
- When is IN batching better than a JOIN? (When the child query needs different columns, filters or a different database or service from the parent.)
- How do you detect N+1 in production? (Statement counts per request in the application log or APM, repeated identical query shapes with different parameters.)
- What is the fix when the parent list is huge? (Chunk the ids, or push the work into one set-based query.)

**Common mistakes:**
- Judging N+1 by in-process timing.
- Using an INNER JOIN and dropping parents without children.
- Putting 100,000 ids into one IN list without checking the engine's limit.
- Looping over DataFrame rows and calling the database inside the loop.

### Q25 ⭐⭐ 🟡 CTE materialisation and subquery flattening: orders(order_id, customer_id, order_date, amount) with 200,000 rows and an index on customer_id. Print the plan for a CTE referenced twice (MATERIALIZE or CO-ROUTINE), for the same CTE written AS MATERIALIZED and AS NOT MATERIALIZED, for a filter applied outside a GROUP BY subquery (WHERE customer_id = 5 on top of the aggregate) and for the equivalent subquery inlined, and count VM steps. State what SQLite does with a CTE used once (flattened like a subquery) versus several times, the predicate push-down limits (a LIMIT or DISTINCT inside blocks it), and that PostgreSQL 12+ inlines single-use CTEs and MATERIALIZED/NOT MATERIALIZED exist there too (hedged, not executed), while older PostgreSQL treated a CTE as an optimisation fence. Cross-reference Part 3 Q32 (reusing one CTE twice).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** In SQLite 3.45.1 a CTE (or subquery) used once is run as a co-routine and a filter on its grouping column is pushed down into it, a CTE used twice is materialised once by default (AS NOT MATERIALIZED re-runs it for each reference, which here doubled the steps), and a LIMIT or an aggregate condition inside blocks the push-down.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'2024-01-01',10),(2,5,'2024-01-02',30),(3,6,'2024-01-03',5),(4,7,'2024-01-04',100);
```

**SQL answer:** The CTE-twice query is `TWICE` with `%s` replaced by nothing, `MATERIALIZED` or `NOT MATERIALIZED`; the others are below (same text as the Code block):
```sql
WITH t AS %s (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT customer_id, s FROM t WHERE s > (SELECT AVG(s) FROM t) ORDER BY customer_id
SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE customer_id = 5
SELECT customer_id, SUM(amount) AS s FROM orders WHERE customer_id = 5 GROUP BY customer_id
```

**pandas answer:** Group, then compare with the mean of the group totals (the CTE-twice question), and a plain filter for customer 5.
```py
exp5 = int(df.loc[df.customer_id == 5, "amount"].sum())
```

**Example:** Tiny table: customer totals are 5 -> 40, 6 -> 5, 7 -> 100; the average of the totals is 48.33, so only customer 7 (100) is above it: the CTE `t` is read twice, once for the rows and once inside the scalar subquery for the average. With `WHERE customer_id = 5` on top of the aggregate the answer is the single row (5, 40). The question is whether SQLite computes all customers' totals first and then throws four away, or computes only customer 5's.

**Code:** run with `python3 -I`.
```python
# Q25: CTE materialisation and subquery flattening
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

# tiny sample
t = sqlite3.connect(":memory:")
t.executescript("""CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,5,'2024-01-01',10),(2,5,'2024-01-02',30),(3,6,'2024-01-03',5),(4,7,'2024-01-04',100);""")
TWICE = "WITH t AS %s (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT customer_id, s FROM t WHERE s > (SELECT AVG(s) FROM t) ORDER BY customer_id"
print("tiny: per-customer totals", t.execute("SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id").fetchall(),
      "average of totals", t.execute("SELECT AVG(s) FROM (SELECT SUM(amount) s FROM orders GROUP BY customer_id)").fetchone()[0])
print("tiny: customers above the average total:", t.execute(TWICE % "").fetchall())

rnd = random.Random(25)
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?)",
    [(i, rnd.randint(1, 20000), "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 500)) for i in range(1, 200001)])
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
con.commit()
df = pd.read_sql("SELECT * FROM orders", con)
tot = df.groupby("customer_id")["amount"].sum()
exp_twice = tot[tot > tot.mean()].reset_index().rename(columns={"amount": "s"}).sort_values("customer_id").reset_index(drop=True)
exp5 = int(df.loc[df.customer_id == 5, "amount"].sum())

print("\n== CTE referenced twice (customers whose total exceeds the average total)")
for nm, hint in (("default", ""), ("AS MATERIALIZED", "MATERIALIZED"), ("AS NOT MATERIALIZED", "NOT MATERIALIZED")):
    sql = TWICE % hint
    rows, n = steps(con, sql)
    pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["customer_id", "s"]), exp_twice)
    print("%-20s rows %5d  VM steps %8d" % (nm, len(rows), n))
    for l in plan(con, sql): print("     ", l)

print("\n== filter applied OUTSIDE a GROUP BY subquery versus the inlined query (customer_id = 5)")
OUT = "SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) WHERE customer_id = 5"
INL = "SELECT customer_id, SUM(amount) AS s FROM orders WHERE customer_id = 5 GROUP BY customer_id"
CTE1 = "WITH t AS (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) SELECT customer_id, s FROM t WHERE customer_id = 5"
CTE1M = CTE1.replace("AS (SELECT", "AS MATERIALIZED (SELECT")
NOFILT = "SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id"
for nm, sql in (("subquery, filter outside", OUT), ("inlined filter", INL), ("CTE used once, filter outside", CTE1),
                ("CTE used once, AS MATERIALIZED", CTE1M), ("whole aggregate, no filter (for scale)", NOFILT)):
    rows, n = steps(con, sql)
    if "no filter" not in nm:
        assert rows == [(5, exp5)], (nm, rows)
    print("%-38s rows %5d  VM steps %8d" % (nm, len(rows), n))
    for l in plan(con, sql): print("     ", l)

print("\n== what blocks push-down (outer filter customer_id = 5)")
BLOCK = [
 ("LIMIT inside", "SELECT customer_id, amount FROM (SELECT customer_id, amount FROM orders LIMIT 1000000) WHERE customer_id = 5"),
 ("no LIMIT (flattened)", "SELECT customer_id, amount FROM (SELECT customer_id, amount FROM orders) WHERE customer_id = 5"),
 ("DISTINCT inside, filter on a distinct column", "SELECT customer_id, amount FROM (SELECT DISTINCT customer_id, amount FROM orders) WHERE customer_id = 5"),
 ("window inside, filter on PARTITION BY column", "SELECT customer_id, rn FROM (SELECT customer_id, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_id) rn FROM orders) WHERE customer_id = 5"),
 ("window inside, filter on the rank", "SELECT customer_id, rn FROM (SELECT customer_id, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_id) rn FROM orders) WHERE rn = 1 AND customer_id = 5"),
 ("aggregate inside, filter on the aggregate", "SELECT customer_id, s FROM (SELECT customer_id, SUM(amount) s FROM orders GROUP BY customer_id) WHERE s > 2000"),
]
for nm, sql in BLOCK:
    rows, n = steps(con, sql)
    want = int((tot > 2000).sum()) if "s > 2000" in sql else (1 if "rn = 1" in sql else int((df.customer_id == 5).sum()))
    assert len(rows) == want, (nm, len(rows), want)
    print("%-46s rows %6d  VM steps %8d" % (nm, len(rows), n))
    for l in plan(con, sql): print("     ", l)
print("asserts passed: every CTE or subquery form matched the pandas result (compared sorted by customer_id)")
```

**Output (my run):**
```text
tiny: per-customer totals [(5, 40), (6, 5), (7, 100)] average of totals 48.333333333333336
tiny: customers above the average total: [(7, 100)]

== CTE referenced twice (customers whose total exceeds the average total)
default              rows  9516  VM steps  2385659
      MATERIALIZE t
      SCAN orders USING INDEX ix_cust
      SCAN t
      SCALAR SUBQUERY 2
      SCAN t
      USE TEMP B-TREE FOR ORDER BY
AS MATERIALIZED      rows  9516  VM steps  2385659
      MATERIALIZE t
      SCAN orders USING INDEX ix_cust
      SCAN t
      SCALAR SUBQUERY 2
      SCAN t
      USE TEMP B-TREE FOR ORDER BY
AS NOT MATERIALIZED  rows  9516  VM steps  4465655
      CO-ROUTINE t
      SCAN orders USING INDEX ix_cust
      SCAN t
      SCALAR SUBQUERY 2
      CO-ROUTINE t
      SCAN orders USING INDEX ix_cust
      SCAN t
      USE TEMP B-TREE FOR ORDER BY

== filter applied OUTSIDE a GROUP BY subquery versus the inlined query (customer_id = 5)
subquery, filter outside               rows     1  VM steps      138
      CO-ROUTINE (subquery-1)
      SEARCH orders USING INDEX ix_cust (customer_id=?)
      SCAN (subquery-1)
inlined filter                         rows     1  VM steps      125
      SEARCH orders USING INDEX ix_cust (customer_id=?)
CTE used once, filter outside          rows     1  VM steps      138
      CO-ROUTINE t
      SEARCH orders USING INDEX ix_cust (customer_id=?)
      SCAN t
CTE used once, AS MATERIALIZED         rows     1  VM steps  2180011
      MATERIALIZE t
      SCAN orders USING INDEX ix_cust
      SCAN t
whole aggregate, no filter (for scale) rows 19999  VM steps  2080004
      SCAN orders USING INDEX ix_cust

== what blocks push-down (outer filter customer_id = 5)
LIMIT inside                                   rows      9  VM steps  1800040
      CO-ROUTINE (subquery-1)
      SCAN orders
      SCAN (subquery-1)
no LIMIT (flattened)                           rows      9  VM steps       63
      SEARCH orders USING INDEX ix_cust (customer_id=?)
DISTINCT inside, filter on a distinct column   rows      9  VM steps      161
      CO-ROUTINE (subquery-1)
      SEARCH orders USING INDEX ix_cust (customer_id=?)
      USE TEMP B-TREE FOR DISTINCT
      SCAN (subquery-1)
window inside, filter on PARTITION BY column   rows      9  VM steps      349
      CO-ROUTINE (subquery-1)
      CO-ROUTINE (subquery-3)
      SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)
      SCAN (subquery-3)
      SCAN (subquery-1)
window inside, filter on the rank              rows      1  VM steps      329
      CO-ROUTINE (subquery-1)
      CO-ROUTINE (subquery-3)
      SEARCH orders USING COVERING INDEX ix_cust (customer_id=?)
      SCAN (subquery-3)
      SCAN (subquery-1)
aggregate inside, filter on the aggregate      rows  13890  VM steps  2178912
      CO-ROUTINE (subquery-1)
      SCAN orders USING INDEX ix_cust
      SCAN (subquery-1)
asserts passed: every CTE or subquery form matched the pandas result (compared sorted by customer_id)
```

**Edge cases:**
- Both materialisation hints return identical rows; they change work, not results (asserted equal to the pandas totals).
- For a CTE referenced twice, NOT MATERIALIZED duplicates the work: it is only a good idea when the CTE is cheap or each use is selective.
- The plan wording CO-ROUTINE versus MATERIALIZE may change between SQLite versions (the EXPLAIN QUERY PLAN format is not a stable interface); these lines are 3.45.1.

**Then explain:**
- CTE referenced twice (200,000 rows, index on customer_id): the default plan was `MATERIALIZE t / SCAN orders USING INDEX ix_cust / SCAN t / SCALAR SUBQUERY 2 / SCAN t`, 2,385,659 steps, identical to AS MATERIALIZED. AS NOT MATERIALIZED showed `CO-ROUTINE t` twice and took 4,465,655 steps, because the whole GROUP BY ran twice. So for several uses SQLite materialises by default.
- A filter outside a GROUP BY subquery on the grouping column (`WHERE customer_id = 5`) was pushed into the subquery: plan `CO-ROUTINE (subquery-1) / SEARCH orders USING INDEX ix_cust (customer_id=?)`, 138 steps, against 125 for the hand-inlined form. The CTE used once with the same filter gave the identical plan and 138 steps: used once, a CTE behaves like a subquery. Adding AS MATERIALIZED to that single-use CTE disabled the push-down: `MATERIALIZE t / SCAN orders`, 2,180,011 steps (computing all 19,999 groups to keep one), close to the unfiltered aggregate (2,080,004 steps).
- Push-down limits observed (outer filter `customer_id = 5`): a LIMIT inside the subquery blocked it (`SCAN orders`, 1,800,040 steps, against 63 without the LIMIT, because the filter after a LIMIT is a different question). A filter on an aggregate result (`s > 2000`) cannot be pushed below the GROUP BY (2,178,912 steps, 13,890 rows). In this version a DISTINCT inside did NOT block a filter on one of the distinct columns (161 steps), and a window with the filter on its PARTITION BY column was pushed down too (349 steps); I did not test a filter on the rank value alone. The premise 'DISTINCT blocks push-down' is therefore only partly true: I tested the case where the filtered column is part of the DISTINCT list, and it did push.
- PostgreSQL, not executed here: from version 12 a single-use CTE that has no side effects is inlined and treated like a subquery, and MATERIALIZED and NOT MATERIALIZED exist there too; before 12, a CTE was an optimisation fence (always materialised). MySQL and SQL Server behaviour is not discussed here because it was not checked.
- Cross-reference Part 3 Q32 (reusing one CTE twice).

**Follow-ups:**
- Why can't `s > 2000` be pushed in? (It depends on the aggregate result, so it is a HAVING.)
- How do you force a one-time computation? (AS MATERIALIZED, or a temporary table.)
- How do you force re-evaluation? (AS NOT MATERIALIZED, useful when the filter makes the CTE tiny.)

**Common mistakes:**
- Treating a CTE as a stored temporary result in every engine.
- Adding AS MATERIALIZED 'for speed' and losing the push-down.
- Reading a plan once and generalising: the plan changes with the SQLite version and the data.

### Q26 ⭐⭐ 🔴 Window-function sort cost and top-N per group plans: sales(sale_id, region, product_id, sale_date, amount) with 300,000 rows, 50 regions. Print plans and VM steps for the top 3 sales per region using (a) ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC) filtered in an outer query, with no index, with an index on (region, amount DESC), (b) a correlated COUNT subquery, and (c) a correlated IN subquery with ORDER BY ... LIMIT 3 (check by running what each accepts and prints). Explain that a window needs rows ordered by the partition and order keys so the cost is a sort unless an index supplies the order, why one extra ORDER BY on a different key means a second sort, and why filtering the rank after the window cannot be pushed before it. Cross-reference Part 4 Q40 (window function performance concept) and Part 4 Q39 (top N and pagination).
**Asked at:** SQLite documentation pages (opened: eqp.html EXPLAIN QUERY PLAN, queryplanner.html, optoverview.html, lang_createindex.html, lang_analyze.html, withoutrowid.html); official documentation, not candidate reports; analyst, data scientist and data engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** A window function needs rows ordered by partition then order key, so unless an index supplies that order the plan sorts the whole table; an outer filter on the rank cannot run before the window, so the window still reads all 300,000 rows, and the correlated COUNT form grows quadratically.

**Schema and sample data:**
```sql
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'N',1,'2024-01-01',50),(2,'N',2,'2024-01-02',90),(3,'N',3,'2024-01-03',90),(4,'N',4,'2024-01-04',70),(5,'N',5,'2024-01-05',10),
 (6,'S',1,'2024-01-06',20),(7,'S',2,'2024-01-07',30);
```

**SQL answer:** `WIN` (window), `CNT` (correlated COUNT) and `INL` (correlated IN with ORDER BY ... LIMIT 3) are in the Code block, copied here; the tie-break (amount DESC, sale_id) makes the result deterministic:
```sql
SELECT region, sale_id, amount FROM (
  SELECT region, sale_id, amount, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, sale_id) AS rn FROM sales)
WHERE rn <= 3 ORDER BY region, amount DESC, sale_id

SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE (SELECT COUNT(*) FROM sales b WHERE b.region = a.region
       AND (b.amount > a.amount OR (b.amount = a.amount AND b.sale_id < a.sale_id))) < 3
ORDER BY a.region, a.amount DESC, a.sale_id

SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE a.sale_id IN (SELECT b.sale_id FROM sales b WHERE b.region = a.region ORDER BY b.amount DESC, b.sale_id LIMIT 3)
ORDER BY a.region, a.amount DESC, a.sale_id
```

**pandas answer:** Sort, then `groupby().head(3)`.
```py
def pandas_top3(df):
    d = df.sort_values(["region", "amount", "sale_id"], ascending=[True, False, True])
    return d.groupby("region").head(3)[["region", "sale_id", "amount"]].reset_index(drop=True)
```

**Example:** Tiny table, region N: amounts 50 (id 1), 90 (id 2), 90 (id 3), 70 (id 4), 10 (id 5). Sorted by amount DESC then sale_id: 2 (90), 3 (90), 4 (70), 1 (50), 5 (10); the top 3 are ids 2, 3, 4. Region S: 30 (id 7) and 20 (id 6). All three SQL forms return [('N',2,90),('N',3,90),('N',4,70),('S',7,30),('S',6,20)]. The two 90s are a tie: ROW_NUMBER with the sale_id tie-break picks both; the COUNT form needs the same tie-break in its comparison or it would count ties as equal and could return more than 3 rows.

**Code:** run with `python3 -I`.
```python
# Q26: window sort cost and top-N per group plans
import sqlite3, random
import pandas as pd

def steps(con, sql, params=()):
    n = [0]
    def cb():
        n[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql, params).fetchall()
    con.set_progress_handler(None, 0)
    return rows, n[0]

_k = [0]
def plan(con, sql):
    _k[0] += 1
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _k[0])]

WIN = """SELECT region, sale_id, amount FROM (
  SELECT region, sale_id, amount, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, sale_id) AS rn FROM sales)
WHERE rn <= 3 ORDER BY region, amount DESC, sale_id"""
CNT = """SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE (SELECT COUNT(*) FROM sales b WHERE b.region = a.region
       AND (b.amount > a.amount OR (b.amount = a.amount AND b.sale_id < a.sale_id))) < 3
ORDER BY a.region, a.amount DESC, a.sale_id"""
INL = """SELECT a.region, a.sale_id, a.amount FROM sales a
WHERE a.sale_id IN (SELECT b.sale_id FROM sales b WHERE b.region = a.region ORDER BY b.amount DESC, b.sale_id LIMIT 3)
ORDER BY a.region, a.amount DESC, a.sale_id"""
WIN_EXTRA = """SELECT region, sale_id, amount, sale_date FROM (
  SELECT region, sale_id, amount, sale_date, ROW_NUMBER() OVER (PARTITION BY region ORDER BY amount DESC, sale_id) AS rn FROM sales)
WHERE rn <= 3 ORDER BY sale_date"""

def build(n, seed=26, regions=50):
    rnd = random.Random(seed)
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product_id INTEGER, sale_date TEXT, amount INTEGER)")
    con.executemany("INSERT INTO sales VALUES (?,?,?,?,?)",
        [(i, "R%02d" % rnd.randint(1, regions), rnd.randint(1, 500), "2024-%02d-%02d" % (rnd.randint(1, 12), rnd.randint(1, 28)), rnd.randint(1, 3000)) for i in range(1, n + 1)])
    con.commit()
    return con

def pandas_top3(df):
    d = df.sort_values(["region", "amount", "sale_id"], ascending=[True, False, True])
    return d.groupby("region").head(3)[["region", "sale_id", "amount"]].reset_index(drop=True)

# tiny sample with a tie
t = sqlite3.connect(":memory:")
t.executescript("""CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'N',1,'2024-01-01',50),(2,'N',2,'2024-01-02',90),(3,'N',3,'2024-01-03',90),(4,'N',4,'2024-01-04',70),(5,'N',5,'2024-01-05',10),
 (6,'S',1,'2024-01-06',20),(7,'S',2,'2024-01-07',30);""")
for nm, q in (("window", WIN), ("correlated COUNT", CNT), ("correlated IN + LIMIT", INL)):
    print("tiny", nm, t.execute(q).fetchall())
print("tiny: plain count form with only '>' would return", t.execute("""SELECT a.sale_id FROM sales a WHERE (SELECT COUNT(*) FROM sales b WHERE b.region=a.region AND b.amount > a.amount) < 3 AND a.region='N' ORDER BY 1""").fetchall(), "(ties at 90 both rank 0, 70 rank 2, 50 rank 3 excluded; tie-break matters when ranks collide)")

# same-size comparison of all forms at 6,000 rows (the correlated forms are too slow at 300,000 without early exit)
print("\n== 6,000 rows (50 regions x about 120 rows), all forms, with and without the index")
small = build(6000)
sdf = pd.read_sql("SELECT * FROM sales", small)
exp_s = pandas_top3(sdf)
for idx in (False, True):
    if idx:
        small.execute("CREATE INDEX ix_reg_amt ON sales(region, amount DESC, sale_id)"); small.commit()
    for nm, q in (("window", WIN), ("correlated COUNT", CNT), ("correlated IN + LIMIT", INL)):
        rows, n = steps(small, q)
        pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_s)
        print("index=%-5s %-22s rows %3d VM steps %9d" % (idx, nm, len(rows), n))
        for l in plan(small, q): print("       ", l)

print("\n== quadratic growth of the correlated COUNT with the index (rows per region grows with n)")
for n in (3000, 6000, 12000):
    c = build(n); c.execute("CREATE INDEX ix_reg_amt ON sales(region, amount DESC, sale_id)")
    print("  n=%6d steps %9d  steps/n = %.1f" % (n, steps(c, CNT)[1], steps(c, CNT)[1] / n))

print("\n== 300,000 rows")
big = build(300000)
bdf = pd.read_sql("SELECT * FROM sales", big)
exp_b = pandas_top3(bdf)
rows, n = steps(big, WIN)
pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_b)
print("window, no index:                      rows %d VM steps %9d" % (len(rows), n))
for l in plan(big, WIN): print("       ", l)
big.execute("CREATE INDEX ix_reg_amt ON sales(region, amount DESC, sale_id)"); big.commit()
rows, n = steps(big, WIN)
pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_b)
print("window, index (region, amount DESC, sale_id): rows %d VM steps %9d" % (len(rows), n))
for l in plan(big, WIN): print("       ", l)
rows, n = steps(big, INL)
pd.testing.assert_frame_equal(pd.DataFrame(rows, columns=["region", "sale_id", "amount"]), exp_b)
print("correlated IN + LIMIT, index:           rows %d VM steps %9d" % (len(rows), n))
for l in plan(big, INL): print("       ", l)
print("(correlated COUNT not run at 300,000 rows: it needs about n*rows-per-region/2 index entries, see the growth table)")

print("\n== where the sorts come from, 300,000 rows (index present)")
WIN_NOORD = WIN.replace(" ORDER BY region, amount DESC, sale_id", "")
for nm, q in (("window, NO outer ORDER BY", WIN_NOORD), ("window, outer ORDER BY region, amount DESC, sale_id", WIN),
              ("window, outer ORDER BY sale_date (another key)", WIN_EXTRA)):
    rows, n = steps(big, q)
    pl = plan(big, q)
    print("%-52s rows %d VM steps %9d temp b-trees %d" % (nm, len(rows), n, sum("TEMP B-TREE" in l for l in pl)))
    for l in pl: print("       ", l)
big.execute("DROP INDEX ix_reg_amt"); big.commit()
for nm, q in (("NO index, no outer ORDER BY", WIN_NOORD), ("NO index, outer ORDER BY", WIN)):
    pl = plan(big, q)
    print("%-52s temp b-trees %d" % (nm, sum("TEMP B-TREE" in l for l in pl)))
print("asserts passed: all forms equal the pandas sort + groupby.head(3) (compared in order region, amount desc, sale_id)")
```

**Output (my run):**
```text
tiny window [('N', 2, 90), ('N', 3, 90), ('N', 4, 70), ('S', 7, 30), ('S', 6, 20)]
tiny correlated COUNT [('N', 2, 90), ('N', 3, 90), ('N', 4, 70), ('S', 7, 30), ('S', 6, 20)]
tiny correlated IN + LIMIT [('N', 2, 90), ('N', 3, 90), ('N', 4, 70), ('S', 7, 30), ('S', 6, 20)]
tiny: plain count form with only '>' would return [(2,), (3,), (4,)] (ties at 90 both rank 0, 70 rank 2, 50 rank 3 excluded; tie-break matters when ranks collide)

== 6,000 rows (50 regions x about 120 rows), all forms, with and without the index
index=False window                 rows 150 VM steps    290187
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales
        USE TEMP B-TREE FOR ORDER BY
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
index=False correlated COUNT       rows 150 VM steps 147731516
        SCAN a
        CORRELATED SCALAR SUBQUERY 1
        SCAN b
        USE TEMP B-TREE FOR ORDER BY
index=False correlated IN + LIMIT  rows 150 VM steps 148685000
        SCAN a
        CORRELATED LIST SUBQUERY 1
        SCAN b
        USE TEMP B-TREE FOR ORDER BY
        USE TEMP B-TREE FOR ORDER BY
index=True  window                 rows 150 VM steps    230185
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING COVERING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
index=True  correlated COUNT       rows 150 VM steps   5195467
        SCAN a USING COVERING INDEX ix_reg_amt
        CORRELATED SCALAR SUBQUERY 1
        SEARCH b USING COVERING INDEX ix_reg_amt (region=?)
index=True  correlated IN + LIMIT  rows 150 VM steps    162611
        SCAN a USING COVERING INDEX ix_reg_amt
        CORRELATED LIST SUBQUERY 1
        SEARCH b USING COVERING INDEX ix_reg_amt (region=?)

== quadratic growth of the correlated COUNT with the index (rows per region grows with n)
  n=  3000 steps   1332755  steps/n = 444.2
  n=  6000 steps   5195467  steps/n = 865.9
  n= 12000 steps  20470934  steps/n = 1705.9

== 300,000 rows
window, no index:                      rows 150 VM steps  14402187
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales
        USE TEMP B-TREE FOR ORDER BY
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
window, index (region, amount DESC, sale_id): rows 150 VM steps  11402185
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING COVERING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
correlated IN + LIMIT, index:           rows 150 VM steps   8100611
        SCAN a USING COVERING INDEX ix_reg_amt
        CORRELATED LIST SUBQUERY 1
        SEARCH b USING COVERING INDEX ix_reg_amt (region=?)
(correlated COUNT not run at 300,000 rows: it needs about n*rows-per-region/2 index entries, see the growth table)

== where the sorts come from, 300,000 rows (index present)
window, NO outer ORDER BY                            rows 150 VM steps  11401132 temp b-trees 0
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING COVERING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
window, outer ORDER BY region, amount DESC, sale_id  rows 150 VM steps  11402181 temp b-trees 1
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING COVERING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
window, outer ORDER BY sale_date (another key)       rows 150 VM steps  12602486 temp b-trees 1
        CO-ROUTINE (subquery-1)
        CO-ROUTINE (subquery-3)
        SCAN sales USING INDEX ix_reg_amt
        SCAN (subquery-3)
        SCAN (subquery-1)
        USE TEMP B-TREE FOR ORDER BY
NO index, no outer ORDER BY                          temp b-trees 1
NO index, outer ORDER BY                             temp b-trees 2
asserts passed: all forms equal the pandas sort + groupby.head(3) (compared in order region, amount desc, sale_id)
```

**Edge cases:**
- Ties at the cut-off: ROW_NUMBER gives exactly 3 rows per region; RANK or the plain `b.amount > a.amount` COUNT can return more. The tie-break columns in every form make the comparison with pandas exact.
- A region with fewer than 3 rows returns what it has (region S).
- The correlated forms were compared at 6,000 rows (all three forms, with and without the index) and at 300,000 rows only where they finish in reasonable time (window, correlated IN with index); the correlated COUNT was not run at 300,000 rows.

**Then explain:**
- 6,000 rows (50 regions x about 120 rows) VM steps, no index: window 290,187; correlated COUNT 147,731,516; correlated IN + LIMIT 148,685,000. With an index on (region, amount DESC, sale_id): window 230,185; COUNT 5,195,467; IN + LIMIT 162,611. Without an index each correlated outer row rescans or re-sorts its region (two temp B-trees for the IN form).
- Growth of the correlated COUNT with the index: 3,000 rows 1,332,755 steps (444 per row), 6,000 rows 5,195,467 (866 per row), 12,000 rows 20,470,934 (1,706 per row): steps per row double when n doubles, so cost is quadratic, because each row counts the rows above it in its region. That is why it was not run at 300,000.
- 300,000 rows: window with no index 14,402,187 steps; with the index 11,402,185 steps; correlated IN with ORDER BY ... LIMIT 3 and the index 8,100,611 steps (each outer row reads about three index entries), lower than the window here. All three were asserted equal to pandas. SQLite accepted LIMIT inside an IN subquery; MySQL is known to reject LIMIT in such a subquery (hedged, not run).
- Sorts, counted from the plans: with no index the window plan has `USE TEMP B-TREE FOR ORDER BY` twice (the window's partition/order sort plus the final ORDER BY: 2); with the index the window sort disappears (`SCAN sales USING COVERING INDEX ix_reg_amt`) and only the final ORDER BY sort remains (1); dropping that final ORDER BY leaves 0. A different outer ORDER BY key (sale_date) needs its own sort on top of whatever order the window had (1 sort, plus a non-covering index scan, 12,602,486 steps). So an extra ORDER BY on another key is an extra sort.
- Why the rank filter is not pushed before the window: `rn <= 3` depends on the window's output, and the window needs all rows of each partition to number them, so the plan reads all 300,000 rows (about 11.4 million steps even with the index) to return 150. The index saves the sort, not the scan.
- Cross-references: Part 4 Q40 (window function performance concept) and Part 4 Q39 (top N and pagination).

**Follow-ups:**
- How would you make top 3 per region cheap at 300,000 rows? (The correlated IN with an index above, or a LATERAL join in engines that have it, not executed; or keep a pre-aggregated table.)
- RANK versus ROW_NUMBER at a tie? (RANK keeps both tied rows, so more than 3 can come back.)
- Does the same plan appear in PostgreSQL? (Not executed; there, a WindowAgg node over a Sort or an Index Scan is the usual shape.)

**Common mistakes:**
- Running the correlated COUNT on the full table without checking its growth.
- Forgetting a tie-break and getting nondeterministic or inflated results.
- Believing `WHERE rn <= 3` makes the window stop early.
- Comparing plans for a statement text the connection has already planned (this run varies the text).

### Q27 ⭐⭐ 🟡 Push SQL work down before loading into pandas: a SQLite orders table with 500,000 seeded rows (order_id, customer_id, order_date, status, amount) and the task 'monthly revenue for delivered orders in 2024'. Compare (a) pd.read_sql of the whole table then pandas filter and groupby, (b) read_sql with WHERE and GROUP BY in SQL, (c) read_sql with chunksize (stream and aggregate per chunk), and (d) read_sql with only the columns needed. Assert the three results equal, report rows transferred, df.memory_usage(deep=True) and timings labelled machine-specific, and explain when to push down (filters, aggregations, joins on indexed keys, sampling) and when pandas is better (iterative exploration, logic hard to express in SQL), and why chunked aggregation only works for decomposable aggregates (sum and count, not median).
**Asked at:** pandas user guide pages 'Enhancing performance' and 'Scaling to large datasets' (opened); official documentation, not candidate reports; data scientist and analytics engineer rounds; SQL optimisation interview guides (DbVisualizer, PracHub, DataDriven, techinterview.org, DesignGurus, Interview Kickstart, opened; they are editorial guides, none says it reports real candidate questions); guides, not candidate reports; analyst, data scientist and data engineer rounds at Indian IT-services firms, GCCs and product companies
**Say this first (1 line):** Filter, aggregate and join in the database before the rows reach pandas: pulling 500,000 rows to compute 12 monthly totals moved 500,000 rows and 70 MB while the GROUP BY query moved 12 rows, and chunked reading saves memory, not time; chunked aggregation only works for decomposable aggregates such as sum and count.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, status TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,1,'2024-01-05','delivered',100),(2,2,'2024-01-20','delivered',50),(3,3,'2024-01-21','cancelled',999),
 (4,1,'2024-02-02','delivered',70),(5,2,'2023-12-31','delivered',500),(6,3,'2025-01-01','delivered',5);
```

**SQL answer:** The pushed-down query `SQL` is in the Code block, copied here:
```sql
SELECT substr(order_date, 1, 7) AS month, SUM(amount) AS revenue, COUNT(*) AS n_orders
FROM orders WHERE status = 'delivered' AND order_date >= '2024-01-01' AND order_date < '2025-01-01'
GROUP BY month ORDER BY month
```

**pandas answer:** The same aggregation in pandas, used for (a), (c) and (d) (a function in the Code block):
```py
def pandas_agg(df):
    d = df[(df["status"] == "delivered") & (df["order_date"] >= "2024-01-01") & (df["order_date"] < "2025-01-01")]
    g = d.assign(month=d["order_date"].str[:7]).groupby("month").agg(revenue=("amount", "sum"), n_orders=("amount", "size"))
    return g.reset_index().sort_values("month").reset_index(drop=True)
```

**Example:** Tiny table: delivered orders in 2024 are 1 (Jan, 100), 2 (Jan, 50) and 4 (Feb, 70). Order 3 is cancelled (excluded), order 5 is 2023-12-31 and order 6 is 2025-01-01 (outside 2024). Result: 2024-01 revenue 150 (2 orders) and 2024-02 revenue 70 (1 order); the run prints `[('2024-01', 150, 2), ('2024-02', 70, 1)]`. At 500,000 rows (seed 27) the same 12 monthly totals come out of all methods.

**Code:** run with `python3 -I`.
```python
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
```

**Output (my run):**
```text
database file: 17.6 MB, 500,000 rows
tiny: [('2024-01', 150, 2), ('2024-02', 70, 1)]
(a) read whole table: rows transferred 500000, memory_usage(deep) 70.3 MB, load 1249 ms + filter/groupby 251 ms
    dtypes: {'order_id': 'int64', 'customer_id': 'int64', 'order_date': 'str', 'status': 'str', 'amount': 'int64'}
(b) WHERE + GROUP BY in SQL: rows transferred 12, memory_usage(deep) 996 bytes, 155 ms
(c) chunksize=50,000, aggregate per chunk: rows transferred 500000, peak chunk memory 7.0 MB, 1492 ms
(d) only 3 needed columns, filter in pandas: rows transferred 500000, memory_usage(deep) 62.3 MB, 787 ms + 284 ms
(e) WHERE pushed down, 2 columns, aggregate in pandas: rows transferred 174908, memory_usage(deep) 11.7 MB, 316 ms
asserts passed: (a), (c), (d), (e) equal (b); compared sorted by month; revenue and n_orders as int64
  month  revenue  n_orders
2024-01 37025467     14746
2024-02 36307646     14513
2024-03 37027482     14744
2024-04 36358880     14419
2024-05 37196747     14761
2024-06 36614750     14526
2024-07 36298940     14510
2024-08 36623888     14588
2024-09 36100832     14392
2024-10 36491865     14610
2024-11 36228945     14444
2024-12 36541770     14655
timings are machine-specific single runs: a=1500 ms, b=155 ms, c=1492 ms, d=1071 ms, e=316 ms

median of delivered amounts: true 2511.0; mean of the 50,000-row chunk medians 2511.0 (equal here only because every chunk is a random sample of the same distribution)
counterexample: true median of all 8 values 4.5, mean of the two chunk medians 3.5
mean from decomposed (sum, count): 2507.8495; direct mean: 2507.8495
```

**Edge cases:**
- The date range is a half-open interval (`>= '2024-01-01' AND < '2025-01-01'`), which is safe for dates stored as ISO text; the month is `substr(order_date,1,7)` in SQL and `str[:7]` in pandas.
- Chunked results are partial sums per month; the per-chunk frames are concatenated and summed again. A month absent from a chunk simply contributes nothing.
- All five paths are asserted equal after casting revenue and n_orders to int64 and comparing sorted by month.

**Then explain:**
- Measured (500,000-row file database of 17.6 MB; timings are machine-specific single runs): (a) read the whole table: 500,000 rows transferred, `memory_usage(deep=True)` 70.3 MB, load about 1.2 s plus about 0.25 s to filter and group. (b) WHERE + GROUP BY in SQL: 12 rows, 996 bytes, about 0.16 s. (c) `chunksize=50,000`: still 500,000 rows transferred, peak chunk memory 7.0 MB, about 1.5 s: memory bounded, time not better. (d) only the three needed columns, filter in pandas: 500,000 rows, 62.3 MB, about 0.8 s load plus 0.28 s. (e) WHERE pushed down but aggregation in pandas, two columns: 174,908 rows, 11.7 MB, about 0.3 s.
- Honest observations: selecting columns alone (d) saved only 8 MB because the two dropped columns are integers, while the string columns order_date and status dominate the memory (pandas 3 uses the `str` dtype). The biggest saving is moving the filter (e) and the aggregation (b) to the database. No index was created here, so (b) still scanned the table in SQLite; an index on (status, order_date) would help but was not measured.
- Push down: filters, aggregations, joins on indexed keys, sampling and `LIMIT`; it reduces transferred rows and memory and uses the engine's indexes. Pandas is better for iterative exploration (re-slicing the same data many times after one load), logic that is awkward in SQL (complex reshaping, custom Python functions) and when the data is already small.
- Chunked aggregation works for decomposable aggregates (sum, count, min, max, and mean via sum and count): partial results combine exactly. The run shows mean from decomposed (sum, count) equal to the direct mean (2507.8495). A median does not decompose: the mean of 50,000-row chunk medians equalled the true median here only by chance (every chunk is a random sample of the same distribution); the counterexample with chunks [1,2,9] and [3,4,5,6,7] gives a true median of 4.5 and a mean of chunk medians of 3.5.
- Source note: the pandas guides named in the Asked-at line were opened for ideas only; no numbers from them are used.

**Follow-ups:**
- Would you use chunksize with a GROUP BY already in SQL? (Not needed: the result is small.)
- How would you do an exact median in chunks? (Two passes with a histogram or a sorted external merge, or use the database's percentile function where it exists; not run.)
- What if the table has no index? (Pushdown still reduces transfer, but the database scans; add an index for repeated queries.)

**Common mistakes:**
- Reading the whole table 'because pandas is easier' and then filtering.
- Using chunksize to speed things up (it reduces peak memory).
- Averaging chunk means or medians of unequal chunks.
- Forgetting that SELECT * of text columns costs far more memory than the integer columns.

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

