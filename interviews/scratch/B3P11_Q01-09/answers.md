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
