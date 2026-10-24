# Book 3 — Part 1: SELECT, filtering, aggregation, GROUP BY and HAVING (SQL with pandas equivalents)

**Topic:** SELECT and column expressions, aliases, DISTINCT, WHERE with AND/OR/IN/BETWEEN/LIKE, NULL logic (IS NULL, three-valued logic, the NOT IN trap, COALESCE, NULLIF), ORDER BY with NULLs and ties, LIMIT/OFFSET and top-N basics, CASE WHEN and conditional aggregation, aggregates with NULLs, GROUP BY (multiple columns, expressions, ordinals), HAVING vs WHERE, order of execution, duplicates and data-quality checks, percentage of total with a scalar subquery, and the pandas counterparts (boolean masks, groupby and named aggregation, isna, value_counts, query, nunique, as_index, observed, dropna)
**Target:** 45  |  **Actual:** 45 (⭐⭐⭐ 18, ⭐⭐ 17, ⭐ 10)  |  **Date:** 2026-10-24  |  **Status:** Answers written (Wave B), Wave C review done

Scope note: this part stops before joins (Part 2), subqueries and CTEs (Part 3: only a scalar subquery and NOT IN/NOT EXISTS appear here), and window functions (Parts 4 and 5: 'second highest salary', top-N per group and running totals are deliberately absent). Pivot and string depth belong to Part 10 and indexes to Part 11. Every query question states its tables and columns so Wave B can build small sample data; answers must run on SQLite 3.45 and compare with pandas 3.0.x, and anything engine-specific (ILIKE, DATE_TRUNC, ROLLUP, PERCENTILE_CONT, FILTER outside SQLite and PostgreSQL, NULL sort order elsewhere) is shown as hedged text labelled 'not executed'.

Verification notes for Wave B: the pandas groupby defaults (as_index=True, dropna=True, sort=True, observed=True since 3.0.0) and the notna/isna, size() vs count() and head/nlargest equivalents were read on the pandas documentation pages; the PostgreSQL NULL ordering rule (NULLs sort as if larger than any value: last for ASC, first for DESC) was read on the PostgreSQL docs. Everything else about other engines (MySQL, SQL Server, Oracle, BigQuery, Snowflake) comes from general knowledge or search snippets and must be hedged or re-checked.

Evidence limits: no candidate-reported SQL questions were found; the search returned prep guides, question banks and documentation. The 'Asked at' tags are source types, and 'expert gap-check' marks questions chosen from practice. Star ratings blend how often a topic appears across guides with judgement. See research_notes/Book3_Part01_sources.md for which pages were opened.

---

### Q1 ⭐⭐⭐ 🟢 Why is SELECT * risky in production queries and interviews? Cover column order and schema changes, extra I/O and network, breaking views and joins with duplicate column names, covering indexes, and when SELECT * is fine (ad hoc exploration with LIMIT). What is the pandas habit that has the same risk (reading every column with read_sql or read_csv instead of usecols)?
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** SELECT * ties your code to whatever the table looks like today, so it breaks or slows down when the table changes, drags unneeded columns over the network, blocks covering indexes and gives duplicate names in joins; it is fine for a quick look with LIMIT, and the pandas twin is reading every column with read_sql or read_csv when you need two.

**Schema and sample data:** (customers and orders; `notes` is a wide text column we do not need)
```sql
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, notes TEXT);
CREATE INDEX idx_cust_amount ON orders(customer_id, amount);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben');
INSERT INTO orders VALUES (10,1,500,'completed','gift wrap, call before delivery'),
                          (11,1,300,'cancelled',NULL),
                          (12,2,700,'completed','fragile');
```

**SQL answer:** name the columns you need, in the order you need them (the statement is `SQL` in the code block):
```sql
SELECT customer_id, amount FROM orders WHERE status = 'completed' ORDER BY customer_id, amount
```

**pandas answer:** the pandas habit with the same risk is pulling every column and filtering afterwards. The risky read is `q("SELECT * FROM orders")` (or `pd.read_csv(path)` with no `usecols`); the better version names the columns at the source (`SELECT customer_id, amount ...`, or `pd.read_csv(path, usecols=[...])`). The code block shows the pandas filter on the wide frame and proves it equals the explicit-column SQL:
```py
all_cols = q("SELECT * FROM orders")                      # the risky habit: every column comes over the wire
pd_df = (all_cols.loc[all_cols["status"] == "completed", ["customer_id", "amount"]]
         .sort_values(["customer_id", "amount"]).reset_index(drop=True))
```

**Example:** the orders table has three completed/cancelled/completed rows. The explicit query returns only the two completed rows and only two columns: (customer 1, 500) and (customer 2, 700). `SELECT *` over the join `orders JOIN customers` returns seven columns with `id` twice (orders.id and customers.id), so in pandas `df["id"]` is a two-column DataFrame, not a Series. After `ALTER TABLE orders ADD COLUMN coupon TEXT`, `SELECT *` grows a sixth column; a consumer that reads column 5 by position or expects exactly five columns now fails or misreads. The explicit view over three named columns does not change.

**Code:** (one block; run with `python3 -I`)
```python
# Q1: why SELECT * is risky. SQLite 3.45 in memory + pandas.
import io, sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers (id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders (id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, notes TEXT);
CREATE INDEX idx_cust_amount ON orders(customer_id, amount);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben');
INSERT INTO orders VALUES (10,1,500,'completed','gift wrap, call before delivery'),
                          (11,1,300,'cancelled',NULL),
                          (12,2,700,'completed','fragile');
""")

def q(sql):
    return pd.read_sql_query(sql, con)

# 1. Explicit columns: what you need, in the order you name them
SQL = "SELECT customer_id, amount FROM orders WHERE status = 'completed' ORDER BY customer_id, amount"
sql_df = q(SQL)

# --- pandas version of the same thing (read only the columns you need, then filter)
all_cols = q("SELECT * FROM orders")                      # the risky habit: every column comes over the wire
pd_df = (all_cols.loc[all_cols["status"] == "completed", ["customer_id", "amount"]]
         .sort_values(["customer_id", "amount"]).reset_index(drop=True))
# --- end pandas
pd.testing.assert_frame_equal(sql_df, pd_df)
print("explicit-column SQL == pandas on the same rows (compared after sort by customer_id, amount)")
print(sql_df.to_string(index=False))

# 2. Duplicate column names from SELECT * over a join
dup = q("SELECT * FROM orders o JOIN customers c ON c.id = o.customer_id")
print("\nSELECT * over a join, column names:", list(dup.columns))
print("type of dup['id']:", type(dup["id"]).__name__, "(two columns called id, so you get a DataFrame, not a Series)")

# 3. Covering index: explicit columns can be answered from the index alone
plan_cols = con.execute("EXPLAIN QUERY PLAN SELECT customer_id, amount FROM orders WHERE customer_id = 1").fetchall()[0][3]
plan_star = con.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 1").fetchall()[0][3]
print("\nplan, explicit columns:", plan_cols)
print("plan, SELECT *        :", plan_star)
assert "COVERING INDEX" in plan_cols and "COVERING INDEX" not in plan_star

# 4. Schema change: SELECT * silently changes shape, an explicit list does not
con.execute("CREATE VIEW v_orders_star AS SELECT * FROM orders")
con.execute("CREATE VIEW v_orders_cols AS SELECT id, customer_id, amount FROM orders")
before_star = list(q("SELECT * FROM orders").columns)
before_view = list(q("SELECT * FROM v_orders_star").columns)
con.execute("ALTER TABLE orders ADD COLUMN coupon TEXT")
after_star = list(q("SELECT * FROM orders").columns)
after_view = list(q("SELECT * FROM v_orders_star").columns)
print("\nSELECT * before ALTER:", before_star)
print("SELECT * after  ALTER:", after_star)
print("view over SELECT * after ALTER (SQLite):", after_view)
print("explicit view columns unchanged:", list(q("SELECT * FROM v_orders_cols").columns))
assert after_star == before_star + ["coupon"]

# 5. pandas habit: read_csv without usecols
csv = "order_id,customer_id,amount,notes\n" + "\n".join(f"{i},{i%5},{i*10},{'long free text ' * 20}" for i in range(1, 201))
wide = pd.read_csv(io.StringIO(csv))
narrow = pd.read_csv(io.StringIO(csv), usecols=["customer_id", "amount"])
print("\nread_csv all columns  :", wide.shape, int(wide.memory_usage(deep=True).sum()), "bytes")
print("read_csv usecols      :", narrow.shape, int(narrow.memory_usage(deep=True).sum()), "bytes")
assert narrow.memory_usage(deep=True).sum() < wide.memory_usage(deep=True).sum()
```
**Output (my run):**
```text
explicit-column SQL == pandas on the same rows (compared after sort by customer_id, amount)
 customer_id  amount
           1     500
           2     700

SELECT * over a join, column names: ['id', 'customer_id', 'amount', 'status', 'notes', 'id', 'name']
type of dup['id']: DataFrame (two columns called id, so you get a DataFrame, not a Series)

plan, explicit columns: SEARCH orders USING COVERING INDEX idx_cust_amount (customer_id=?)
plan, SELECT *        : SEARCH orders USING INDEX idx_cust_amount (customer_id=?)

SELECT * before ALTER: ['id', 'customer_id', 'amount', 'status', 'notes']
SELECT * after  ALTER: ['id', 'customer_id', 'amount', 'status', 'notes', 'coupon']
view over SELECT * after ALTER (SQLite): ['id', 'customer_id', 'amount', 'status', 'notes', 'coupon']
explicit view columns unchanged: ['id', 'customer_id', 'amount']

read_csv all columns  : (200, 4) 74732 bytes
read_csv usecols      : (200, 2) 3332 bytes
```

**Edge cases:**
- **Views:** in SQLite the view `SELECT * FROM orders` picked up the new column (shown in the output). I recall that PostgreSQL expands `*` once when the view is created, so the view would not show the new column and also blocks some later table changes (from memory, not executed here). Either way the behaviour differs by engine, which is itself a reason not to rely on it.
- **Dropped or renamed columns:** an explicit column list fails loudly at once with "no such column"; `SELECT *` fails later, somewhere downstream, or worse keeps working with a shifted meaning when the consumer reads by position.
- **Covering index:** the plan line for the explicit query says COVERING INDEX (the answer comes from the index alone); for `SELECT *` it says plain INDEX, so SQLite must also visit the table rows. That is SQLite's EXPLAIN QUERY PLAN; other engines have their own wording (not executed here).
- **Wide text and blob columns:** the `usecols` run shows 74,732 bytes of memory for four columns against 3,332 bytes for two, because the long text column is the cost.
- **`SELECT *` is fine** in ad hoc exploration with a LIMIT, in `EXISTS (SELECT * ...)` (the column list is ignored there), and inside a CTE or subquery where the outer query then lists columns, provided no duplicate names reach the client.

**Then explain:**
- **Column order and schema changes:** `*` returns columns in table definition order. Add, drop or reorder a column and any code that depends on positions or counts breaks, or silently misaligns.
- **Extra I/O and network:** you read pages and ship bytes for columns you throw away; wide text, JSON and blob columns make it worse. In pandas the same bytes become memory.
- **Duplicate column names in joins:** `SELECT *` from two tables that share `id` returns two columns called `id`. Many clients keep only one (last wins) or raise; in pandas you get a DataFrame for `df["id"]`. Views and CREATE TABLE AS SELECT can fail outright on duplicate names in some engines (not executed here).
- **Covering indexes:** if every column the query needs is in the index, the engine never touches the table. `*` almost always defeats that.
- **Contract:** an explicit column list documents what the query is for and lets a reviewer see what it exposes (for example, not selecting a sensitive column).
- **pandas habit:** `read_sql("SELECT * ...")` and `read_csv(...)` without `usecols` (and `dtype`) load everything first, then you filter. Select columns and rows at the source.

**Follow-ups:**
- *Is `SELECT COUNT(*)` also bad?* No. `COUNT(*)` is a different construct: it counts rows and does not read all columns.
- *What about `SELECT t.*` in a CTE?* Acceptable if the outer query names columns and the duplicates are resolved; still prefer explicit lists at the boundary where the schema is a contract.
- *How would you protect an ETL job against schema drift?* Explicit column lists plus a test that compares the expected column list to the actual one.

**Common mistakes:**
- Saying SELECT * is "slower" without saying why (extra I/O, no covering index, wider network transfer).
- Forgetting the duplicate-column problem in joins.
- Treating `usecols` as a micro-optimisation when it can decide whether the file fits in memory.
- Using `SELECT *` in a view or `INSERT ... SELECT *` and then adding a column.

### Q2 ⭐⭐⭐ 🟢 Explain the logical order of execution of a SELECT statement (FROM, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, LIMIT/OFFSET). Using orders(order_id, customer_id, amount, status, created_at), explain why 'SELECT amount*1.18 AS gross FROM orders WHERE gross > 500' fails in most engines but 'ORDER BY gross' works, and which engines let you reuse an alias in GROUP BY or HAVING (state this as hedged dialect behaviour).
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** The engine does not run a query in the order you write it: it logically runs FROM, WHERE, GROUP BY, HAVING, SELECT, DISTINCT, ORDER BY, then LIMIT/OFFSET, so a SELECT alias does not exist yet in WHERE in standard SQL (Postgres, SQL Server and Oracle reject it) but is visible in ORDER BY; SQLite, which I ran, is more forgiving than the standard.

**Schema and sample data:**
```sql
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1, 1, 100,  'completed', '2025-01-05'),
 (2, 1, 300,  'completed', '2025-01-09'),
 (3, 2, 450,  'cancelled', '2025-02-01'),
 (4, 2, 500,  'completed', '2025-02-11'),
 (5, 3, 600,  'completed', '2025-03-02'),
 (6, 3, 1000, 'completed', '2025-03-15');
```

**SQL answer:** the portable way is to compute the alias in a subquery (or CTE) and filter outside (the statement is `SQL` in the code block):
```sql
SELECT order_id, gross
FROM (SELECT order_id, amount * 1.18 AS gross FROM orders) AS t
WHERE gross > 500
ORDER BY gross DESC
```
The query as written in the question, `SELECT amount*1.18 AS gross FROM orders WHERE gross > 500`, is rejected in standard SQL engines (I recall PostgreSQL, SQL Server and Oracle reject it; not executed here), but SQLite 3.45 ran it and returned the same orders (see the output). Repeating the expression, `WHERE amount * 1.18 > 500`, works everywhere.

**pandas answer:** pandas has no logical-order surprise because each step is explicit, in the order you code it: compute the column, mask the rows, pick the columns, sort.
```py
o = pd.read_sql_query("SELECT order_id, amount FROM orders", con)
o = o.assign(gross=o["amount"] * 1.18)                    # SELECT expression
pd_df = (o.loc[o["gross"] > 500, ["order_id", "gross"]]   # WHERE on the computed column
         .sort_values("gross", ascending=False).reset_index(drop=True))
```

**Example:** six orders with amounts 100, 300, 450, 500, 600, 1000; gross is amount times 1.18, so 118, 354, 531, 590, 708, 1180. WHERE gross > 500 keeps orders 3, 4, 5 and 6 (531, 590, 708, 1180). Sorted by gross DESC the result is 6, 5, 4, 3. For the order-of-execution demo: customer 2 has 950 in total across a cancelled 450 and a completed 500 order; because WHERE runs before GROUP BY, filtering `status = 'completed'` makes that customer's total 500, not 950, and HAVING SUM(amount) > 400 then runs on the already-filtered groups (customer 2 with 500 and customer 3 with 1600 survive).

**Code:** (one block; run with `python3 -I`)
```python
# Q2: logical order of execution and alias scope. SQLite 3.45 in memory + pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1, 1, 100,  'completed', '2025-01-05'),
 (2, 1, 300,  'completed', '2025-01-09'),
 (3, 2, 450,  'cancelled', '2025-02-01'),
 (4, 2, 500,  'completed', '2025-02-11'),
 (5, 3, 600,  'completed', '2025-03-02'),
 (6, 3, 1000, 'completed', '2025-03-15');
""")

def q(sql):
    return pd.read_sql_query(sql, con)

# Portable form: compute the alias in a subquery (or CTE), filter in the outer query
SQL = """
SELECT order_id, gross
FROM (SELECT order_id, amount * 1.18 AS gross FROM orders) AS t
WHERE gross > 500
ORDER BY gross DESC
"""
sql_df = q(SQL)

# --- pandas version
o = pd.read_sql_query("SELECT order_id, amount FROM orders", con)
o = o.assign(gross=o["amount"] * 1.18)                    # SELECT expression
pd_df = (o.loc[o["gross"] > 500, ["order_id", "gross"]]   # WHERE on the computed column
         .sort_values("gross", ascending=False).reset_index(drop=True))
# --- end pandas
pd.testing.assert_frame_equal(sql_df, pd_df)
print("portable subquery form == pandas (compared in order gross DESC; no ties in this data)")
print(sql_df.to_string(index=False))

# The question's query. Standard SQL (Postgres, SQL Server, Oracle ...) rejects it; SQLite accepts it.
non_portable = "SELECT order_id, amount * 1.18 AS gross FROM orders WHERE gross > 500 ORDER BY gross DESC"
try:
    r = q(non_portable)
    print("\nSQLite ran 'WHERE gross > 500' on an alias:", r["order_id"].tolist())
    assert r["order_id"].tolist() == sql_df["order_id"].tolist()
except Exception as e:
    print("\nSQLite rejected it:", e)

# Alias in GROUP BY and HAVING (SQLite accepts both)
r = q("""SELECT status AS s, COUNT(*) AS n FROM orders GROUP BY s HAVING n > 1 ORDER BY s""")
print("\nSQLite alias in GROUP BY and HAVING:", r.values.tolist())

# Alias that shadows a real column: the column wins inside WHERE in SQLite
r = q("SELECT order_id, amount * 2 AS amount FROM orders WHERE amount > 500 ORDER BY order_id")
print("alias named like a column, WHERE amount > 500 uses the column:", r["order_id"].tolist())
assert r["order_id"].tolist() == [5, 6]

# Observable order of execution, step by step on the same table
steps = {
 "FROM+WHERE (status='completed')": "SELECT COUNT(*) FROM orders WHERE status = 'completed'",
 "GROUP BY customer_id, then HAVING": "SELECT customer_id, SUM(amount) AS s FROM orders WHERE status = 'completed' GROUP BY customer_id HAVING SUM(amount) > 400 ORDER BY customer_id",
 "SELECT DISTINCT before LIMIT": "SELECT DISTINCT customer_id FROM orders ORDER BY customer_id LIMIT 2",
}
print()
for k, s in steps.items():
    print(f"{k:34s}", con.execute(s).fetchall())
# WHERE runs before GROUP BY: customer 2 has 950 in total but only 500 completed
total_all = con.execute("SELECT SUM(amount) FROM orders WHERE customer_id = 2").fetchone()[0]
total_completed = con.execute("SELECT SUM(amount) FROM orders WHERE customer_id = 2 AND status = 'completed'").fetchone()[0]
print("customer 2: all orders", total_all, "| completed only", total_completed)
```
**Output (my run):**
```text
portable subquery form == pandas (compared in order gross DESC; no ties in this data)
 order_id  gross
        6 1180.0
        5  708.0
        4  590.0
        3  531.0

SQLite ran 'WHERE gross > 500' on an alias: [6, 5, 4, 3]

SQLite alias in GROUP BY and HAVING: [['completed', 5]]
alias named like a column, WHERE amount > 500 uses the column: [5, 6]

FROM+WHERE (status='completed')    [(5,)]
GROUP BY customer_id, then HAVING  [(2, 500), (3, 1600)]
SELECT DISTINCT before LIMIT       [(1,), (2,)]
customer 2: all orders 950 | completed only 500
```

**Edge cases:**
- **Honest surprise (premise partly wrong for SQLite):** the question says the alias-in-WHERE query "fails in most engines". That is true of the standard and the engines I named from memory, but it ran fine in SQLite 3.45, which resolves aliases in WHERE, GROUP BY and HAVING. Code that works in SQLite can therefore fail when moved to Postgres.
- **Alias shadowing a column:** `SELECT amount*2 AS amount ... WHERE amount > 500` used the real column in SQLite (rows 5 and 6, whose real amount is above 500), not the doubled alias. Do not name an alias after a column.
- **Window functions** run after HAVING and before the final DISTINCT/ORDER BY, which is why you cannot filter on them in WHERE (Part 4).
- **DISTINCT before LIMIT:** LIMIT takes the first N distinct rows of the already-sorted result.
- **Alias reuse by engine (hedged, from memory, not executed here):** ORDER BY accepts the alias nearly everywhere. GROUP BY accepts it in MySQL, PostgreSQL and BigQuery (as I recall); HAVING accepts it in MySQL but not in PostgreSQL; WHERE rejects it in all of those. Snowflake is reported to allow more alias reuse than most. Check your engine's documentation before relying on any of this.

**Then explain:**
- **The logical order:** FROM and JOINs, then WHERE (row filter), GROUP BY, HAVING (group filter), SELECT (expressions and aliases), DISTINCT, ORDER BY, LIMIT/OFFSET. It is the logical order; the optimiser may physically do things differently as long as the result is the same.
- **Why alias fails in WHERE:** WHERE runs before SELECT, so `gross` has not been computed. ORDER BY runs after SELECT, so it can use it.
- **Why WHERE cannot hold aggregates:** groups do not exist yet at WHERE time. HAVING runs after GROUP BY.
- **Practical rule:** filter rows early in WHERE (cheaper, can use indexes), filter groups in HAVING, and use a CTE or subquery when you need to filter on a computed alias.

**Follow-ups:**
- *Why can ORDER BY use an alias but HAVING often cannot?* ORDER BY is after SELECT in the logical order; HAVING is before it. MySQL bends the rule for convenience.
- *Does this order mean the database scans everything first?* No, it is a logical model; indexes and predicate pushdown change the physical plan, not the result.
- *Where do window functions fit?* After HAVING, before DISTINCT and ORDER BY (Part 4).

**Common mistakes:**
- Using an alias in WHERE and assuming it works because it worked in SQLite or MySQL for GROUP BY.
- Putting a non-aggregate row filter in HAVING.
- Naming an alias the same as an existing column.
- Thinking the physical execution plan follows the written or logical order.

### Q3 ⭐⭐⭐ 🟢 What is the difference between WHERE and HAVING? Using orders(order_id, customer_id, amount, status, created_at), write a query for customers whose completed orders total more than 1,000, and show where the status filter and the total filter each belong. Can a non-aggregate condition go in HAVING, and should it? Give the pandas equivalent (boolean mask before groupby, filter on the aggregated frame after).
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** WHERE filters rows before grouping and cannot use aggregates; HAVING filters groups after aggregation and is where SUM or COUNT conditions go, so "completed orders only" belongs in WHERE and "total above 1,000" belongs in HAVING.

**Schema and sample data:**
```sql
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1, 1, 600, 'completed', '2025-01-05'),
 (2, 1, 700, 'completed', '2025-01-09'),
 (3, 1, 500, 'cancelled', '2025-01-20'),
 (4, 2, 400, 'completed', '2025-02-01'),
 (5, 2, 300, 'completed', '2025-02-11'),
 (6, 2, 900, 'cancelled', '2025-02-12'),
 (7, 3, 1000,'completed', '2025-03-02'),
 (8, 4, 1200,'cancelled', '2025-03-15');
```

**SQL answer:** (the statement is `SQL` in the code block)
```sql
SELECT customer_id, SUM(amount) AS completed_total
FROM orders
WHERE status = 'completed'
GROUP BY customer_id
HAVING SUM(amount) > 1000
ORDER BY customer_id
```

**pandas answer:** boolean mask before `groupby` is WHERE; a filter on the aggregated frame is HAVING.
```py
o = pd.read_sql_query("SELECT customer_id, amount, status FROM orders", con)
totals = (o[o["status"] == "completed"]                    # boolean mask = WHERE
          .groupby("customer_id", as_index=False)
          .agg(completed_total=("amount", "sum")))
pd_df = totals[totals["completed_total"] > 1000].sort_values("customer_id").reset_index(drop=True)   # filter on aggregated frame = HAVING
```

**Example:** completed totals are customer 1: 600 + 700 = 1,300; customer 2: 400 + 300 = 700; customer 3: 1,000; customer 4: none (only a cancelled order). "More than 1,000" keeps only customer 1, because customer 3 is exactly 1,000 and `>` excludes it. If the status filter is forgotten, totals include cancelled money: customer 1 becomes 1,800, customer 2 becomes 1,600 (700 completed plus 900 cancelled) and customer 4 becomes 1,200, so customers 2 and 4 wrongly appear.

**Code:** (one block; run with `python3 -I`)
```python
# Q3: WHERE vs HAVING. SQLite 3.45 in memory + pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1, 1, 600, 'completed', '2025-01-05'),
 (2, 1, 700, 'completed', '2025-01-09'),
 (3, 1, 500, 'cancelled', '2025-01-20'),
 (4, 2, 400, 'completed', '2025-02-01'),
 (5, 2, 300, 'completed', '2025-02-11'),
 (6, 2, 900, 'cancelled', '2025-02-12'),
 (7, 3, 1000,'completed', '2025-03-02'),
 (8, 4, 1200,'cancelled', '2025-03-15');
""")

def q(sql):
    return pd.read_sql_query(sql, con)

# Right: row filter in WHERE (before grouping), group filter in HAVING (after aggregation)
SQL = """
SELECT customer_id, SUM(amount) AS completed_total
FROM orders
WHERE status = 'completed'
GROUP BY customer_id
HAVING SUM(amount) > 1000
ORDER BY customer_id
"""
sql_df = q(SQL)

# --- pandas version
o = pd.read_sql_query("SELECT customer_id, amount, status FROM orders", con)
totals = (o[o["status"] == "completed"]                    # boolean mask = WHERE
          .groupby("customer_id", as_index=False)
          .agg(completed_total=("amount", "sum")))
pd_df = totals[totals["completed_total"] > 1000].sort_values("customer_id").reset_index(drop=True)   # filter on aggregated frame = HAVING
# --- end pandas
pd.testing.assert_frame_equal(sql_df, pd_df)
print("WHERE + HAVING SQL == pandas mask then filter (compared after sort by customer_id)")
print(sql_df.to_string(index=False))

# Wrong 1: status filter forgotten (cancelled money counted)
wrong1 = q("SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id HAVING SUM(amount) > 1000 ORDER BY customer_id")
print("\nwrong 1, no status filter:", wrong1.values.tolist())
assert wrong1["customer_id"].tolist() == [1, 2, 4]          # customer 2 (cancelled 900) and 4 (only cancelled) sneak in

# Wrong 2: non-aggregate status condition in HAVING. SQLite accepts a bare column there and checks an arbitrary row.
try:
    wrong2 = q("SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id HAVING status = 'completed' AND SUM(amount) > 1000 ORDER BY customer_id")
    print("wrong 2, status in HAVING (SQLite, bare column):", wrong2.values.tolist())
except Exception as e:
    print("wrong 2 raised:", e)

# Legal but pointless: a grouping column in HAVING. Same answer as WHERE, but filters after grouping.
alt = q("SELECT customer_id, SUM(amount) AS t FROM orders GROUP BY customer_id HAVING customer_id <> 4 AND SUM(amount) > 1000 ORDER BY customer_id")
alt2 = q("SELECT customer_id, SUM(amount) AS t FROM orders WHERE customer_id <> 4 GROUP BY customer_id HAVING SUM(amount) > 1000 ORDER BY customer_id")
pd.testing.assert_frame_equal(alt, alt2)
print("grouping-column filter in HAVING vs WHERE gives the same rows:", alt.values.tolist())

# Condition on the status filter without WHERE: conditional aggregation inside HAVING
alt3 = q("SELECT customer_id, SUM(CASE WHEN status = 'completed' THEN amount END) AS completed_total FROM orders GROUP BY customer_id HAVING SUM(CASE WHEN status = 'completed' THEN amount END) > 1000 ORDER BY customer_id")
pd.testing.assert_frame_equal(alt3, sql_df)
print("conditional aggregation in HAVING matches too")
```
**Output (my run):**
```text
WHERE + HAVING SQL == pandas mask then filter (compared after sort by customer_id)
 customer_id  completed_total
           1             1300

wrong 1, no status filter: [[1, 1800], [2, 1600], [4, 1200]]
wrong 2, status in HAVING (SQLite, bare column): [[1, 1800], [2, 1600]]
grouping-column filter in HAVING vs WHERE gives the same rows: [[1, 1800], [2, 1600]]
conditional aggregation in HAVING matches too
```

**Edge cases:**
- **Boundary:** `> 1000` excludes exactly 1,000 (customer 3); use `>=` if the business rule says "at least".
- **No completed orders at all:** a customer with only cancelled orders (customer 4) has no group after the WHERE, so they do not appear, rather than appearing with a total of 0. To list them with 0 you need a left join to a customers table (Part 2) or conditional aggregation without the WHERE.
- **Silent wrong answer in SQLite:** `HAVING status = 'completed' AND SUM(amount) > 1000` did not raise an error here. SQLite accepts a bare, non-grouped column in HAVING and tests an arbitrary row of the group, and the sum still included cancelled orders: it returned customers 1 and 2 with totals 1,800 and 1,600, which is wrong. I recall PostgreSQL rejects this with an error, and MySQL does so under `ONLY_FULL_GROUP_BY` (not executed here).
- **Non-aggregate condition in HAVING:** a condition on a grouping column (`customer_id <> 4`) is legal and returned the same rows as the WHERE version in my run, but it filters after grouping, so the engine groups rows you were going to throw away. Put it in WHERE.
- **Conditional aggregation** (`SUM(CASE WHEN status = 'completed' THEN amount END)` in HAVING) also gives the right answer without a WHERE, which is useful when you need several different filtered measures in one query (Q10).

**Then explain:**
- **Order of execution:** WHERE then GROUP BY then HAVING (Q2). An aggregate cannot be in WHERE because the groups do not exist yet.
- **Performance:** WHERE can use indexes and shrink the data before grouping; HAVING works on the aggregated result. Push every row-level condition into WHERE.
- **Can a non-aggregate go in HAVING?** Only if it uses a grouping column (or an aggregate); standards-compliant engines reject other columns. Even when legal, it should not be there.
- **pandas:** `df[mask].groupby(...).agg(...)` then `agg_df[agg_df.total > 1000]`; there is no HAVING keyword, so the second filter is just another mask. `groupby(...).filter(lambda g: ...)` also exists and keeps original rows, not aggregated rows.

**Follow-ups:**
- *Where would "orders in 2025 only" go?* WHERE, with a half-open date range (Q30).
- *How do you show customers with total above 1,000 along with their cancelled total?* Conditional aggregation: `SUM(CASE WHEN status = 'completed' ...)` and `SUM(CASE WHEN status = 'cancelled' ...)` with HAVING on the first (Q10).
- *HAVING without GROUP BY?* Treats the whole table as one group (Q25).

**Common mistakes:**
- Forgetting the status filter, so cancelled money counts.
- Writing the status test in HAVING.
- Using `>` when the rule is "at least".
- In pandas, filtering the aggregated frame before the groupby, or forgetting `as_index=False` and then filtering on an index.

### Q4 ⭐⭐⭐ 🟢 Explain COUNT(*), COUNT(column), COUNT(DISTINCT column) and SUM/AVG/MIN/MAX with NULLs. Given employees(emp_id, dept, salary, bonus) where bonus is NULL for some people, show what each returns and what AVG(bonus) means versus AVG(COALESCE(bonus,0)). Map to pandas: size() vs count() vs nunique(), and mean() skipping NaN.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** COUNT(*) counts rows, COUNT(col) counts non-NULL values, COUNT(DISTINCT col) counts distinct non-NULL values, and SUM, AVG, MIN and MAX all skip NULLs, so AVG(bonus) is the average over people who have a bonus while AVG(COALESCE(bonus, 0)) treats missing as zero and is a different number.

**Schema and sample data:**
```sql
CREATE TABLE employees (emp_id INTEGER PRIMARY KEY, dept TEXT, salary INTEGER, bonus INTEGER);
INSERT INTO employees VALUES
 (1, 'eng',   100, 10),
 (2, 'eng',   120, 10),
 (3, 'eng',   140, NULL),
 (4, 'sales',  80, 20),
 (5, 'sales',  90, NULL),
 (6, 'hr',     70, NULL);
```

**SQL answer:** (the statement is `SQL` in the code block)
```sql
SELECT COUNT(*)                     AS n_rows,
       COUNT(bonus)                 AS n_bonus,
       COUNT(DISTINCT bonus)        AS n_distinct_bonus,
       SUM(bonus)                   AS sum_bonus,
       AVG(bonus)                   AS avg_bonus,
       AVG(COALESCE(bonus, 0))      AS avg_bonus_zero_filled,
       MIN(bonus)                   AS min_bonus,
       MAX(bonus)                   AS max_bonus
FROM employees
```

**pandas answer:** `size` is COUNT(*), `count` is COUNT(col), `nunique` is COUNT(DISTINCT col), and `mean`, `sum`, `min`, `max` skip NaN by default.
```py
e = pd.read_sql_query("SELECT emp_id, dept, salary, bonus FROM employees", con)
pd_df = pd.DataFrame({
    "n_rows": [e["bonus"].size],                          # size = COUNT(*): counts rows, NaN included
    "n_bonus": [e["bonus"].count()],                      # count = COUNT(col): non-null only
    "n_distinct_bonus": [e["bonus"].nunique()],           # nunique skips NaN by default
    "sum_bonus": [e["bonus"].sum()],
    "avg_bonus": [e["bonus"].mean()],                     # mean skips NaN (skipna=True)
    "avg_bonus_zero_filled": [e["bonus"].fillna(0).mean()],
    "min_bonus": [e["bonus"].min()],
    "max_bonus": [e["bonus"].max()],
})
```

**Example:** bonuses are 10, 10, NULL, 20, NULL, NULL. There are 6 rows, so COUNT(*) = 6. Three bonuses are present, so COUNT(bonus) = 3. The distinct present values are 10 and 20, so COUNT(DISTINCT bonus) = 2. SUM = 10 + 10 + 20 = 40. AVG(bonus) = 40 / 3 = 13.33 (divide by the 3 non-NULL values). AVG(COALESCE(bonus, 0)) = 40 / 6 = 6.67 (the three missing bonuses count as zero). MIN = 10 and MAX = 20. Which average is right depends on the question: "average bonus among people who got one" versus "average bonus per employee".

**Code:** (one block; run with `python3 -I`)
```python
# Q4: COUNT(*), COUNT(col), COUNT(DISTINCT col), SUM/AVG/MIN/MAX with NULLs. SQLite 3.45 + pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees (emp_id INTEGER PRIMARY KEY, dept TEXT, salary INTEGER, bonus INTEGER);
INSERT INTO employees VALUES
 (1, 'eng',   100, 10),
 (2, 'eng',   120, 10),
 (3, 'eng',   140, NULL),
 (4, 'sales',  80, 20),
 (5, 'sales',  90, NULL),
 (6, 'hr',     70, NULL);
""")

def q(sql):
    return pd.read_sql_query(sql, con)

SQL = """
SELECT COUNT(*)                     AS n_rows,
       COUNT(bonus)                 AS n_bonus,
       COUNT(DISTINCT bonus)        AS n_distinct_bonus,
       SUM(bonus)                   AS sum_bonus,
       AVG(bonus)                   AS avg_bonus,
       AVG(COALESCE(bonus, 0))      AS avg_bonus_zero_filled,
       MIN(bonus)                   AS min_bonus,
       MAX(bonus)                   AS max_bonus
FROM employees
"""
sql_df = q(SQL)

# --- pandas version
e = pd.read_sql_query("SELECT emp_id, dept, salary, bonus FROM employees", con)
pd_df = pd.DataFrame({
    "n_rows": [e["bonus"].size],                          # size = COUNT(*): counts rows, NaN included
    "n_bonus": [e["bonus"].count()],                      # count = COUNT(col): non-null only
    "n_distinct_bonus": [e["bonus"].nunique()],           # nunique skips NaN by default
    "sum_bonus": [e["bonus"].sum()],
    "avg_bonus": [e["bonus"].mean()],                     # mean skips NaN (skipna=True)
    "avg_bonus_zero_filled": [e["bonus"].fillna(0).mean()],
    "min_bonus": [e["bonus"].min()],
    "max_bonus": [e["bonus"].max()],
})
# --- end pandas
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)   # one row each; dtypes differ (int vs float after NaN)
print("SQL aggregates == pandas aggregates (one row; dtypes not compared, values are)")
for c in sql_df.columns:
    print(f"{c:22s}", sql_df[c].iloc[0])

# Per department: an all-NULL group (hr). SQL SUM is NULL, pandas sum is 0 by default
g_sql = q("SELECT dept, COUNT(*) AS n, COUNT(bonus) AS n_bonus, SUM(bonus) AS sum_bonus, AVG(bonus) AS avg_bonus FROM employees GROUP BY dept ORDER BY dept")
g_pd = (e.groupby("dept").agg(n=("emp_id", "size"), n_bonus=("bonus", "count"), sum_bonus=("bonus", "sum"), avg_bonus=("bonus", "mean"))
        .reset_index())
print("\nSQL per dept:\n" + g_sql.to_string(index=False))
print("\npandas per dept (default sum of all-NaN = 0):\n" + g_pd.to_string(index=False))
g_pd2 = e.groupby("dept").agg(n=("emp_id", "size"), n_bonus=("bonus", "count"),
                              sum_bonus=("bonus", lambda s: s.sum(min_count=1)), avg_bonus=("bonus", "mean")).reset_index()
pd.testing.assert_frame_equal(g_sql, g_pd2, check_dtype=False)
print("\nwith sum(min_count=1) pandas matches SQL, including NaN for hr")

# An empty-looking mean: AVG(bonus) vs AVG with zero fill differ
assert abs(sql_df.loc[0, "avg_bonus"] - 40/3) < 1e-9 and abs(sql_df.loc[0, "avg_bonus_zero_filled"] - 40/6) < 1e-9
```
**Output (my run):**
```text
SQL aggregates == pandas aggregates (one row; dtypes not compared, values are)
n_rows                 6
n_bonus                3
n_distinct_bonus       2
sum_bonus              40
avg_bonus              13.333333333333334
avg_bonus_zero_filled  6.666666666666667
min_bonus              10
max_bonus              20

SQL per dept:
 dept  n  n_bonus  sum_bonus  avg_bonus
  eng  3        2       20.0       10.0
   hr  1        0        NaN        NaN
sales  2        1       20.0       20.0

pandas per dept (default sum of all-NaN = 0):
 dept  n  n_bonus  sum_bonus  avg_bonus
  eng  3        2       20.0       10.0
   hr  1        0        0.0        NaN
sales  2        1       20.0       20.0

with sum(min_count=1) pandas matches SQL, including NaN for hr
```

**Edge cases:**
- **All-NULL group:** in the `hr` department the only bonus is NULL. SQL gives COUNT(bonus) = 0, SUM = NULL, AVG = NULL. pandas `groupby().sum()` gave 0.0 for the same group in my run (an honest difference); `sum(min_count=1)` makes pandas return NaN like SQL (Q16 goes deeper). The mean is NaN in both.
- **Empty table:** COUNT(*) = 0 but SUM, AVG, MIN, MAX are NULL (Q33).
- **Integer columns:** `AVG` on an integer column returned 13.33 in SQLite (it returns a float); some engines return an integer-typed average for integer input (I recall SQL Server does, and PostgreSQL returns numeric; not executed here). Cast to decimal when in doubt (Q29).
- **COUNT(1) vs COUNT(*):** equivalent in practice, both count rows.
- **COUNT(DISTINCT a, b):** not standard everywhere (Q19).

**Then explain:**
- **Why aggregates skip NULL:** NULL means unknown; an unknown value cannot add to a sum or count. Only COUNT(*) is about rows, not values.
- **AVG(col) = SUM(col) / COUNT(col),** not divided by COUNT(*). That is why zero-filling changes the average.
- **pandas mapping:** `Series.size` counts all (including NaN), `Series.count()` counts non-NaN, `nunique()` excludes NaN unless `dropna=False`, `mean()` skips NaN unless `skipna=False`.
- **Say the business meaning:** whether a missing bonus means "no bonus" (zero) or "unknown" decides which average you report.

**Follow-ups:**
- *Does COUNT(*) ever differ from COUNT(1)?* Not in results; some people claim a speed difference, which modern optimisers do not show.
- *What does `df.groupby("dept").count()` return?* Non-null counts per column; `size()` returns rows per group (one number).
- *How do I count NULLs?* `COUNT(*) - COUNT(col)` or `SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END)`; in pandas `s.isna().sum()`.

**Common mistakes:**
- Using COUNT(col) when they want row count.
- Assuming AVG divides by the number of rows.
- Not saying whether NULL bonus should be 0 or ignored.
- Assuming pandas and SQL agree on the sum of an all-missing group (they do not by default).

### Q5 ⭐⭐⭐ 🟢 How does NULL behave in comparisons? Explain three-valued logic (TRUE, FALSE, UNKNOWN) with the AND, OR and NOT truth tables, why 'WHERE col = NULL' returns nothing, why 'WHERE status <> ''cancelled''' silently drops rows where status is NULL, and how IS NULL, IS NOT NULL and COALESCE fix it. Contrast with pandas, where NaN != NaN is True and df[df.col != 'x'] keeps NaN rows.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** A comparison with NULL is neither true nor false but UNKNOWN, WHERE keeps only rows where the condition is TRUE, so `= NULL` returns nothing and `<> 'cancelled'` silently drops NULL-status rows; use IS NULL, IS NOT NULL or COALESCE, and remember pandas is the opposite: NaN != 'x' is True, so the NaN rows stay.

**Schema and sample data:** (`v` holds the three truth values 1 = TRUE, 0 = FALSE, NULL = UNKNOWN)
```sql
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, status TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'completed',100),(2,'cancelled',200),(3,NULL,300),(4,'shipped',400);
CREATE TABLE v (x INTEGER);
INSERT INTO v VALUES (1),(0),(NULL);          -- 1 = TRUE, 0 = FALSE, NULL = UNKNOWN
```

**SQL answer:** the truth tables, produced by the engine (the statement is `SQL` in the code block):
```sql
SELECT a.x AS a, b.x AS b, (a.x AND b.x) AS a_and_b, (a.x OR b.x) AS a_or_b, (NOT a.x) AS not_a
FROM v AS a CROSS JOIN v AS b
ORDER BY a.x IS NULL, a.x DESC, b.x IS NULL, b.x DESC
```
The null-safe filters from the Edge cases section are the three `fix` queries in the code block (`status <> 'cancelled' OR status IS NULL`, the COALESCE form, and SQLite's `status IS NOT 'cancelled'`).

**pandas answer:** the nullable `boolean` dtype follows the same three-valued logic, so it reproduces the truth tables; the ordinary mask on a text column does not.
```py
vals = pd.array([True, False, None], dtype="boolean")
rows = [(a, b, a & b, a | b, ~a) for a in vals for b in vals]
pd_df = pd.DataFrame(rows, columns=["a", "b", "a_and_b", "a_or_b", "not_a"], dtype="Int64")
pd_df = pd_df.astype({c: "Int64" for c in pd_df.columns})
```

**Example:** truth tables (T true, F false, U unknown). AND: T and U = U, F and U = F (false wins), U and U = U. OR: T or U = T (true wins), F or U = U. NOT U = U. On the orders table (ids 1 to 4, status completed, cancelled, NULL, shipped) `WHERE status <> 'cancelled'` returns ids 1 and 4: row 3 has `NULL <> 'cancelled'` = UNKNOWN, so it is dropped even though a NULL status is "not cancelled" in plain English. `WHERE status = NULL` returns nothing for the same reason. Adding `OR status IS NULL` brings back 3, so the result is 1, 3, 4.

**Code:** (one block; run with `python3 -I`)
```python
# Q5: NULL logic, three-valued logic, and pandas contrast. SQLite 3.45 + pandas 3.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, status TEXT, amount INTEGER);
INSERT INTO orders VALUES (1,'completed',100),(2,'cancelled',200),(3,NULL,300),(4,'shipped',400);
CREATE TABLE v (x INTEGER);
INSERT INTO v VALUES (1),(0),(NULL);          -- 1 = TRUE, 0 = FALSE, NULL = UNKNOWN
""")

def q(sql):
    return pd.read_sql_query(sql, con)

# Truth tables from the engine itself: every pair (a, b) of TRUE / FALSE / UNKNOWN
SQL = """
SELECT a.x AS a, b.x AS b, (a.x AND b.x) AS a_and_b, (a.x OR b.x) AS a_or_b, (NOT a.x) AS not_a
FROM v AS a CROSS JOIN v AS b
ORDER BY a.x IS NULL, a.x DESC, b.x IS NULL, b.x DESC
"""
sql_df = q(SQL)

# --- pandas version: the nullable "boolean" dtype implements the same three-valued (Kleene) logic
vals = pd.array([True, False, None], dtype="boolean")
rows = [(a, b, a & b, a | b, ~a) for a in vals for b in vals]
pd_df = pd.DataFrame(rows, columns=["a", "b", "a_and_b", "a_or_b", "not_a"], dtype="Int64")
pd_df = pd_df.astype({c: "Int64" for c in pd_df.columns})
# --- end pandas
# SQL gives 1/0/NULL; Int64 gives 1/0/<NA>. Compare as Int64.
pd.testing.assert_frame_equal(sql_df.astype("Int64"), pd_df)
print("AND / OR / NOT truth tables: SQLite == pandas nullable boolean (rows ordered TRUE, FALSE, UNKNOWN for a then b)")
print(sql_df.astype("Int64").to_string(index=False, na_rep="NULL"))

# WHERE col = NULL, and <> dropping NULL rows
print("\nWHERE status = NULL           ->", q("SELECT order_id FROM orders WHERE status = NULL")["order_id"].tolist())
print("WHERE status <> 'cancelled'    ->", q("SELECT order_id FROM orders WHERE status <> 'cancelled' ORDER BY order_id")["order_id"].tolist())
print("WHERE NOT (status = 'cancelled') ->", q("SELECT order_id FROM orders WHERE NOT (status = 'cancelled') ORDER BY order_id")["order_id"].tolist())

fix1 = "SELECT order_id FROM orders WHERE status <> 'cancelled' OR status IS NULL ORDER BY order_id"
fix2 = "SELECT order_id FROM orders WHERE COALESCE(status, 'unknown') <> 'cancelled' ORDER BY order_id"
fix3 = "SELECT order_id FROM orders WHERE status IS NOT 'cancelled' ORDER BY order_id"   # SQLite-only spelling of null-safe <>
naive = q("SELECT order_id FROM orders WHERE status <> 'cancelled' ORDER BY order_id")["order_id"].tolist()
ids1, ids2, ids3 = (q(s)["order_id"].tolist() for s in (fix1, fix2, fix3))
print("fix IS NULL / COALESCE / IS NOT   ->", ids1, ids2, ids3)
assert naive == [1, 4] and ids1 == ids2 == ids3 == [1, 3, 4]

# pandas: NaN != 'cancelled' is True, so NaN rows are KEPT by the naive mask
o = pd.read_sql_query("SELECT order_id, status, amount FROM orders", con)
print("\npandas status dtype:", o["status"].dtype, "| missing value:", o["status"].iloc[2])
pd_naive = o.loc[o["status"] != "cancelled", "order_id"].tolist()
pd_eq_null = o.loc[o["status"] == None, "order_id"].tolist()    # noqa: E711  (never match NaN with ==)
pd_sql_like = o.loc[o["status"].notna() & (o["status"] != "cancelled"), "order_id"].tolist()
print("pandas df[df.status != 'cancelled']        ->", pd_naive, "(keeps the NaN row)")
print("pandas df[df.status == None]               ->", pd_eq_null)
print("pandas notna() & != 'cancelled' (SQL-like)  ->", pd_sql_like)
assert pd_naive == ids1 and pd_sql_like == naive and pd_eq_null == []
print("NaN != NaN in numpy/pandas:", float('nan') != float('nan'), "| SQL NULL <> NULL:", con.execute("SELECT NULL <> NULL").fetchone()[0])
```
**Output (my run):**
```text
AND / OR / NOT truth tables: SQLite == pandas nullable boolean (rows ordered TRUE, FALSE, UNKNOWN for a then b)
   a    b  a_and_b  a_or_b  not_a
   1    1        1       1      0
   1    0        0       1      0
   1 <NA>     <NA>       1      0
   0    1        0       1      1
   0    0        0       0      1
   0 <NA>        0    <NA>      1
<NA>    1     <NA>       1   <NA>
<NA>    0        0    <NA>   <NA>
<NA> <NA>     <NA>    <NA>   <NA>

WHERE status = NULL           -> []
WHERE status <> 'cancelled'    -> [1, 4]
WHERE NOT (status = 'cancelled') -> [1, 4]
fix IS NULL / COALESCE / IS NOT   -> [1, 3, 4] [1, 3, 4] [1, 3, 4]

pandas status dtype: str | missing value: nan
pandas df[df.status != 'cancelled']        -> [1, 3, 4] (keeps the NaN row)
pandas df[df.status == None]               -> []
pandas notna() & != 'cancelled' (SQL-like)  -> [1, 4]
NaN != NaN in numpy/pandas: True | SQL NULL <> NULL: None
```

**Edge cases:**
- **NOT of UNKNOWN is UNKNOWN:** `NOT (status = 'cancelled')` still drops the NULL row (it returned ids 1 and 4), so "negating" the condition does not rescue NULLs.
- **NULL <> NULL** is NULL (SQLite printed None), and so is `NULL = NULL`. Use IS NULL, or a null-safe equality (Q41).
- **pandas string columns:** in pandas 3 a text column uses the `str` dtype with NaN as the missing value; `df[df.status != 'cancelled']` returned ids 1, 3, 4 (NaN kept), `df.status == None` matched nothing, and the SQL-like version needs `df.status.notna() & (df.status != 'cancelled')` (ids 1, 4). So the two worlds disagree on the default, and a literal SQL-to-pandas translation changes the answer.
- **NaN in numeric comparisons:** `NaN > 5`, `NaN == NaN` are False and `NaN != NaN` is True in pandas and numpy, with no UNKNOWN state; only the nullable `boolean` dtype (with `<NA>`) models UNKNOWN.
- **CHECK constraints and CASE:** CHECK passes when the condition is UNKNOWN (standard behaviour), while WHERE rejects UNKNOWN; CASE WHEN UNKNOWN falls through to the next branch or ELSE (Q44).

**Then explain:**
- **Three values:** a comparison involving NULL gives UNKNOWN. AND, OR and NOT extend naturally: UNKNOWN AND FALSE is FALSE, UNKNOWN OR TRUE is TRUE, otherwise UNKNOWN.
- **WHERE keeps only TRUE.** UNKNOWN and FALSE are both dropped, which is why NULL rows vanish from both a predicate and its negation.
- **Fixes:** `IS NULL` and `IS NOT NULL` test for missing values; `COALESCE(status, 'unknown')` replaces NULL before comparing; `IS DISTINCT FROM` in engines that have it (Q41).
- **Contrast with pandas:** boolean masks are two-valued, missing values compare as not-equal, so you must be explicit about NaN either way.

**Follow-ups:**
- *Why does `NOT IN` with a NULL return nothing?* It expands to a chain of `<>` joined by AND, and one UNKNOWN makes the whole chain not TRUE (Q13).
- *What does `COUNT(col)` do with NULL?* Skips it (Q4).
- *How would you find rows where status is NULL?* `WHERE status IS NULL`; pandas `df[df.status.isna()]`.

**Common mistakes:**
- Writing `= NULL` or `<> NULL`.
- Assuming a filter and its negation together return all rows.
- Forgetting that the NaN row stays in pandas but not in SQL.
- Treating NULL as an empty string or zero without deciding explicitly.

### Q6 ⭐⭐⭐ 🟢 What do COALESCE and NULLIF do, and when would you use each? Using payments(payment_id, amount, discount, units) show: replacing NULL discount with 0 in a sum, avoiding divide-by-zero in amount/units with NULLIF, and why COALESCE(a,b,c) differs from a CASE expression only in how it is written. Mention IFNULL, NVL and ISNULL as dialect names (hedged) and the pandas counterparts fillna and where.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** COALESCE returns the first non-NULL argument (use it to replace NULL with a default), and NULLIF(a, b) returns NULL when a equals b, otherwise a (use it to turn a bad value like 0 into NULL so division gives NULL instead of an error).

**Schema and sample data:**
```sql
CREATE TABLE payments (payment_id INTEGER PRIMARY KEY, amount REAL, discount REAL, units INTEGER);
INSERT INTO payments VALUES
 (1, 100.0, 10.0, 4),
 (2, 200.0, NULL, 0),
 (3,  60.0,  5.0, NULL),
 (4,  90.0, NULL, 3);
```

**SQL answer:** row level, plus totals (both are in the code block as `SQL` and `SQL_TOTALS`):
```sql
SELECT payment_id,
       amount - COALESCE(discount, 0)  AS net_amount,
       amount - discount               AS net_naive,
       amount / NULLIF(units, 0)       AS unit_price
FROM payments
ORDER BY payment_id
```
```sql
SELECT SUM(amount - COALESCE(discount, 0)) AS net_total,
       SUM(amount - discount)              AS net_total_naive
FROM payments
```

**pandas answer:** `fillna` is COALESCE with a constant; `where` is NULLIF (keep the value where the condition holds, else NaN).
```py
p = pd.read_sql_query("SELECT payment_id, amount, discount, units FROM payments", con)
pd_df = pd.DataFrame({
    "payment_id": p["payment_id"],
    "net_amount": p["amount"] - p["discount"].fillna(0),          # COALESCE(discount, 0)
    "net_naive": p["amount"] - p["discount"],                      # NaN propagates like NULL
    "unit_price": p["amount"] / p["units"].where(p["units"] != 0),  # NULLIF(units, 0): where keeps units, else NaN
})
tot_pd = pd.DataFrame({"net_total": [(p["amount"] - p["discount"].fillna(0)).sum()],
                       "net_total_naive": [(p["amount"] - p["discount"]).sum()]})   # sum skips NaN like SUM skips NULL
```

**Example:** four payments: amounts 100, 200, 60, 90; discounts 10, NULL, 5, NULL; units 4, 0, NULL, 3. Net amount with COALESCE: 90, 200, 55, 90, total 435. Naive `amount - discount` is NULL whenever the discount is NULL, so only payments 1 and 3 count: 90 + 55 = 145 (the sum silently drops two payments). Unit price: 100 / 4 = 25; 200 / NULLIF(0, 0) = 200 / NULL = NULL; 60 / NULL = NULL; 90 / 3 = 30. COALESCE(discount, units, -1) gives 10, 0 (discount is NULL, units is 0, which is not NULL so it wins), 5, 3.

**Code:** (one block; run with `python3 -I`)
```python
# Q6: COALESCE and NULLIF. SQLite 3.45 + pandas 3.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE payments (payment_id INTEGER PRIMARY KEY, amount REAL, discount REAL, units INTEGER);
INSERT INTO payments VALUES
 (1, 100.0, 10.0, 4),
 (2, 200.0, NULL, 0),
 (3,  60.0,  5.0, NULL),
 (4,  90.0, NULL, 3);
""")

def q(sql):
    return pd.read_sql_query(sql, con)

# Row level: NULL discount -> 0, units 0 -> NULL so the division gives NULL instead of an error
SQL = """
SELECT payment_id,
       amount - COALESCE(discount, 0)  AS net_amount,
       amount - discount               AS net_naive,
       amount / NULLIF(units, 0)       AS unit_price
FROM payments
ORDER BY payment_id
"""
sql_df = q(SQL)

# Totals: the NULL-discount rows vanish from the naive sum
SQL_TOTALS = """
SELECT SUM(amount - COALESCE(discount, 0)) AS net_total,
       SUM(amount - discount)              AS net_total_naive
FROM payments
"""
tot_sql = q(SQL_TOTALS)

# --- pandas version
p = pd.read_sql_query("SELECT payment_id, amount, discount, units FROM payments", con)
pd_df = pd.DataFrame({
    "payment_id": p["payment_id"],
    "net_amount": p["amount"] - p["discount"].fillna(0),          # COALESCE(discount, 0)
    "net_naive": p["amount"] - p["discount"],                      # NaN propagates like NULL
    "unit_price": p["amount"] / p["units"].where(p["units"] != 0),  # NULLIF(units, 0): where keeps units, else NaN
})
tot_pd = pd.DataFrame({"net_total": [(p["amount"] - p["discount"].fillna(0)).sum()],
                       "net_total_naive": [(p["amount"] - p["discount"]).sum()]})   # sum skips NaN like SUM skips NULL
# --- end pandas
pd.testing.assert_frame_equal(sql_df, pd_df)
pd.testing.assert_frame_equal(tot_sql, tot_pd)
print("row-level and totals: SQL == pandas (compared in payment_id order)")
print(sql_df.to_string(index=False))
print(tot_sql.to_string(index=False))

# pandas surprise: dividing by 0 gives inf, SQLite gives NULL, strict engines raise an error
print("\npandas 200.0/0 without the guard:", (p["amount"] / p["units"]).tolist())
print("SQLite 200.0/0 without NULLIF  :", con.execute("SELECT 200.0/0").fetchone()[0])

# COALESCE(a, b, c) behaves like the searched CASE below
case_sql = """SELECT CASE WHEN discount IS NOT NULL THEN discount WHEN units IS NOT NULL THEN units ELSE -1 END AS pick FROM payments ORDER BY payment_id"""
coal_sql = "SELECT COALESCE(discount, units, -1) AS pick FROM payments ORDER BY payment_id"
ifnull_sql = "SELECT IFNULL(discount, 0) AS d FROM payments ORDER BY payment_id"
coalesce2 = "SELECT COALESCE(discount, 0) AS d FROM payments ORDER BY payment_id"
pd.testing.assert_frame_equal(q(case_sql), q(coal_sql))
pd.testing.assert_frame_equal(q(ifnull_sql), q(coalesce2))
print("\nCOALESCE(discount, units, -1) :", q(coal_sql)["pick"].tolist(), "(same as the CASE form)")
print("IFNULL(discount, 0) == COALESCE(discount, 0) in SQLite:", q(ifnull_sql)["d"].tolist())
# pandas: first non-null across columns is bfill along axis 1 or combine_first
first = p[["discount", "units"]].bfill(axis=1).iloc[:, 0].fillna(-1)
assert first.tolist() == q(coal_sql)["pick"].tolist()

# NULLIF with strings: turn empty strings into NULL
print("NULLIF('', '') ->", con.execute("SELECT NULLIF('', '')").fetchone()[0], "| NULLIF('x', '') ->", con.execute("SELECT NULLIF('x', '')").fetchone()[0])
```
**Output (my run):**
```text
row-level and totals: SQL == pandas (compared in payment_id order)
 payment_id  net_amount  net_naive  unit_price
          1        90.0       90.0        25.0
          2       200.0        NaN         NaN
          3        55.0       55.0         NaN
          4        90.0        NaN        30.0
 net_total  net_total_naive
     435.0            145.0

pandas 200.0/0 without the guard: [25.0, inf, nan, 30.0]
SQLite 200.0/0 without NULLIF  : None

COALESCE(discount, units, -1) : [10.0, 0.0, 5.0, 3.0] (same as the CASE form)
IFNULL(discount, 0) == COALESCE(discount, 0) in SQLite: [10.0, 0.0, 5.0, 0.0]
NULLIF('', '') -> None | NULLIF('x', '') -> x
```

**Edge cases:**
- **Division by zero differs by engine:** SQLite returned NULL for `200.0/0` even without NULLIF (shown in the output). I recall PostgreSQL and SQL Server raise an error and MySQL returns NULL unless strict mode is set (not executed here), so NULLIF is the portable guard. pandas goes a third way: it returns `inf` (shown in the output), which then poisons an average.
- **NULLIF on units that is NULL:** NULLIF(NULL, 0) is NULL, so NULL stays NULL.
- **COALESCE vs CASE:** `COALESCE(a, b, c)` is defined as the CASE expression `CASE WHEN a IS NOT NULL THEN a WHEN b IS NOT NULL THEN b ELSE c END`; the code block asserts they return the same values. Differences are only in how it reads and, in some engines, in how the result type is chosen (not executed here).
- **Type mixing:** all COALESCE arguments should have compatible types; engines differ on whether an integer and a date raise an error.
- **Do not replace NULL with 0 blindly:** zero-filling changes averages (Q4); decide if "missing" means "none" or "unknown".

**Then explain:**
- **COALESCE:** picks the first non-NULL argument, evaluated left to right; many engines stop evaluating after the first hit.
- **NULLIF:** returns NULL if the two arguments are equal. Typical uses: `x / NULLIF(y, 0)` and `NULLIF(TRIM(col), '')` to turn empty strings into NULL.
- **Dialect names (hedged, from memory):** IFNULL (MySQL, SQLite, which I ran with two arguments), NVL (Oracle), ISNULL (SQL Server, two arguments only, with different type rules). COALESCE is standard and works in all of them.
- **pandas:** `fillna(value)`, `combine_first` or `bfill(axis=1)` for a first non-null across columns, `where` / `mask` for NULLIF-style replacement.

**Follow-ups:**
- *Can you COALESCE to an empty string?* Yes for text columns, but it hides the missing state; do it at the reporting layer.
- *Why not write `CASE WHEN units = 0 THEN NULL ELSE amount / units END`?* Same result, longer; NULLIF is the idiom.
- *What if discount is 0 vs NULL?* They are different facts: 0 is "no discount", NULL is "unknown or not recorded".

**Common mistakes:**
- Forgetting that `amount - discount` is NULL when discount is NULL, so rows vanish from SUM.
- Using COALESCE(x, 0) before AVG and changing the meaning.
- Dividing by a column that can be 0 and getting `inf` in pandas or an error in strict engines.
- Using the SQL Server ISNULL with three arguments (it takes two).

### Q7 ⭐⭐⭐ 🟢 Classic interview question: find duplicate emails. Given users(user_id, email, created_at), list each email that appears more than once with its count, then write a DELETE that keeps the lowest user_id per email, and explain why email casing and trailing spaces can hide duplicates. Show pandas duplicated(keep=False), drop_duplicates and groupby().size(). (Window-function dedup is Part 4.)
**Asked at:** public LeetCode-style problem bank (SQL 50 style problems), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Group by email and keep groups with COUNT(*) > 1 to list duplicates; delete every row that has a smaller user_id with the same email to keep the lowest id; and normalise with LOWER(TRIM(email)) first, because 'B@x.com' and 'b@x.com ' are different strings to the database.

**Schema and sample data:** (eight users: three exact copies of a@x.com, a case-and-space duplicate of b@x.com, one unique email, and two NULL emails)
```sql
CREATE TABLE users (user_id INTEGER PRIMARY KEY, email TEXT, created_at TEXT);
INSERT INTO users VALUES
 (1, 'a@x.com',  '2025-01-01'),
 (2, 'B@x.com',  '2025-01-02'),
 (3, 'c@x.com',  '2025-01-03'),
 (4, 'a@x.com',  '2025-01-04'),
 (5, 'b@x.com ', '2025-01-05'),
 (6, NULL,       '2025-01-06'),
 (7, NULL,       '2025-01-07'),
 (8, 'a@x.com',  '2025-01-08');
```

**SQL answer:** list the duplicates (the statement is `SQL` in the code block):
```sql
SELECT email, COUNT(*) AS n
FROM users
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1
```
The normalised version (`SQL_NORM`):
```sql
SELECT LOWER(TRIM(email)) AS email_clean, COUNT(*) AS n
FROM users
WHERE email IS NOT NULL
GROUP BY LOWER(TRIM(email))
HAVING COUNT(*) > 1
ORDER BY email_clean
```
Delete, keeping the lowest user_id per email (`DELETE_SQL`):
```sql
DELETE FROM users
WHERE EXISTS (SELECT 1 FROM users AS u2
              WHERE u2.email = users.email AND u2.user_id < users.user_id)
```
An equivalent form with MIN (`DELETE_SQL_2`):
```sql
DELETE FROM users
WHERE email IS NOT NULL
  AND user_id NOT IN (SELECT MIN(user_id) FROM users GROUP BY email)
```

**pandas answer:** `groupby().size()` for the counts, `duplicated(keep=False)` to see every member of a duplicate set, `duplicated(keep="first")` or `drop_duplicates` to keep the first row per email.
```py
u = pd.read_sql_query("SELECT user_id, email, created_at FROM users", con)
pd_df = (u[u["email"].notna()].groupby("email").size().rename("n").reset_index()
         .query("n > 1"))
```

**Example:** the exact duplicate list is a@x.com with count 3 (user_ids 1, 4, 8). After LOWER(TRIM(...)) it is a@x.com 3 and b@x.com 2 (user_ids 2 and 5), so the casing and trailing space were hiding a duplicate. The DELETE removes any row that has a smaller user_id with the same email: ids 4 and 8 go (a@x.com), leaving 1, 2, 3, 5, 6, 7. With the normalised key id 5 also goes, leaving 1, 2, 3, 6, 7. The two NULL-email rows (6 and 7) stay in both versions because NULL = NULL is not TRUE, so the EXISTS never matches them.

**Code:** (one block; run with `python3 -I`)
```python
# Q7: find and delete duplicate emails. SQLite 3.45 + pandas 3.
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE users (user_id INTEGER PRIMARY KEY, email TEXT, created_at TEXT);
INSERT INTO users VALUES
 (1, 'a@x.com',  '2025-01-01'),
 (2, 'B@x.com',  '2025-01-02'),
 (3, 'c@x.com',  '2025-01-03'),
 (4, 'a@x.com',  '2025-01-04'),
 (5, 'b@x.com ', '2025-01-05'),
 (6, NULL,       '2025-01-06'),
 (7, NULL,       '2025-01-07'),
 (8, 'a@x.com',  '2025-01-08');
"""

def fresh():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c

con = fresh()
def q(sql, c=None):
    return pd.read_sql_query(sql, c or con)

# 1. Exact duplicates. NULL emails form one group in GROUP BY, so exclude them explicitly.
SQL = """
SELECT email, COUNT(*) AS n
FROM users
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1
"""
sql_df = q(SQL)

# --- pandas version
u = pd.read_sql_query("SELECT user_id, email, created_at FROM users", con)
pd_df = (u[u["email"].notna()].groupby("email").size().rename("n").reset_index()
         .query("n > 1"))
# --- end pandas
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_df.reset_index(drop=True), check_dtype=False)
print("duplicate emails (exact match), SQL == pandas groupby().size():")
print(sql_df.to_string(index=False))

# 2. After normalising with LOWER(TRIM(...)): the hidden duplicate appears
SQL_NORM = """
SELECT LOWER(TRIM(email)) AS email_clean, COUNT(*) AS n
FROM users
WHERE email IS NOT NULL
GROUP BY LOWER(TRIM(email))
HAVING COUNT(*) > 1
ORDER BY email_clean
"""
norm_sql = q(SQL_NORM)
clean = u[u["email"].notna()].assign(email_clean=lambda d: d["email"].str.strip().str.lower())
norm_pd = (clean.groupby("email_clean").size().rename("n").reset_index().query("n > 1").reset_index(drop=True))
pd.testing.assert_frame_equal(norm_sql, norm_pd, check_dtype=False)
print("\nafter LOWER(TRIM(email)):")
print(norm_sql.to_string(index=False))

# 3. DELETE keeping the lowest user_id per email (EXISTS form; NULL emails are never matched, so they stay)
DELETE_SQL = """
DELETE FROM users
WHERE EXISTS (SELECT 1 FROM users AS u2
              WHERE u2.email = users.email AND u2.user_id < users.user_id)
"""
c1 = fresh(); c1.execute(DELETE_SQL)
kept_exists = [r[0] for r in c1.execute("SELECT user_id FROM users ORDER BY user_id")]

# Same idea with NOT IN (SELECT MIN ...). The guard keeps NULL-email rows, which GROUP BY would otherwise collapse into one group.
DELETE_SQL_2 = """
DELETE FROM users
WHERE email IS NOT NULL
  AND user_id NOT IN (SELECT MIN(user_id) FROM users GROUP BY email)
"""
c2 = fresh(); c2.execute(DELETE_SQL_2)
kept_in = [r[0] for r in c2.execute("SELECT user_id FROM users ORDER BY user_id")]

# --- pandas version of the delete: keep the first row per email, but never treat NaN emails as duplicates of each other
us = u.sort_values("user_id")
kept_pd = us[us["email"].isna() | ~us.duplicated(subset="email", keep="first")]["user_id"].tolist()
# --- end pandas
print("\nkept after DELETE (EXISTS):", kept_exists, "| (NOT IN + MIN):", kept_in, "| pandas:", kept_pd)
assert kept_exists == kept_in == kept_pd == [1, 2, 3, 5, 6, 7]

# 4. Normalised delete: keep lowest user_id per LOWER(TRIM(email))
DELETE_NORM = """
DELETE FROM users
WHERE EXISTS (SELECT 1 FROM users AS u2
              WHERE LOWER(TRIM(u2.email)) = LOWER(TRIM(users.email)) AND u2.user_id < users.user_id)
"""
c3 = fresh(); c3.execute(DELETE_NORM)
kept_norm = [r[0] for r in c3.execute("SELECT user_id FROM users ORDER BY user_id")]
clean_sorted = clean.sort_values("user_id")
kept_norm_pd = sorted(u.loc[u["email"].isna(), "user_id"].tolist() + clean_sorted.loc[~clean_sorted.duplicated("email_clean", keep="first"), "user_id"].tolist())
print("kept after normalised DELETE:", kept_norm, "| pandas:", kept_norm_pd)
assert kept_norm == kept_norm_pd == [1, 2, 3, 6, 7]

# 5. pandas duplicated(keep=False) shows ALL members of each duplicate set; NaN pairs count as duplicates here
print("\nduplicated(keep=False) rows (user_id):", u[u.duplicated("email", keep=False)]["user_id"].tolist(),
      "<- includes the two NULL-email rows 6 and 7")
print("with notna() guard                    :", u[u["email"].notna() & u.duplicated("email", keep=False)]["user_id"].tolist())
print("unguarded SQL, GROUP BY email HAVING COUNT(*) > 1 returns a NULL row:",
      q("SELECT email, COUNT(*) AS n FROM users GROUP BY email HAVING COUNT(*) > 1 ORDER BY email").values.tolist())

# drop_duplicates is the same as ~duplicated(keep='first'), so it also collapses the NaN rows
dd = us.drop_duplicates(subset="email", keep="first")["user_id"].tolist()
print("drop_duplicates(subset='email') keeps user_id:", dd, "(row 7 lost: NaN counted as a duplicate of NaN)")
assert dd == [1, 2, 3, 5, 6]
```
**Output (my run):**
```text
duplicate emails (exact match), SQL == pandas groupby().size():
  email  n
a@x.com  3

after LOWER(TRIM(email)):
email_clean  n
    a@x.com  3
    b@x.com  2

kept after DELETE (EXISTS): [1, 2, 3, 5, 6, 7] | (NOT IN + MIN): [1, 2, 3, 5, 6, 7] | pandas: [1, 2, 3, 5, 6, 7]
kept after normalised DELETE: [1, 2, 3, 6, 7] | pandas: [1, 2, 3, 6, 7]

duplicated(keep=False) rows (user_id): [1, 4, 6, 7, 8] <- includes the two NULL-email rows 6 and 7
with notna() guard                    : [1, 4, 8]
unguarded SQL, GROUP BY email HAVING COUNT(*) > 1 returns a NULL row: [[nan, 2], ['a@x.com', 3]]
drop_duplicates(subset='email') keeps user_id: [1, 2, 3, 5, 6] (row 7 lost: NaN counted as a duplicate of NaN)
```

**Edge cases:**
- **NULL emails:** `GROUP BY email HAVING COUNT(*) > 1` without the guard returned a NULL group with count 2, because GROUP BY puts all NULLs in one group. Two missing emails are not duplicates of each other, so the guard `WHERE email IS NOT NULL` matters. pandas `groupby` drops NaN keys by default, so it matches the guarded SQL.
- **pandas duplicated and NaN:** `duplicated("email", keep=False)` flagged rows 6 and 7 (NaN equals NaN there), and `drop_duplicates(subset="email")` dropped row 7 (shown in the output). Add `notna()` to the mask or keep NaN rows separately.
- **Ties on created_at do not matter here** because we keep the lowest user_id, a unique key. If "keep the earliest" is meant, say whether created_at or user_id decides.
- **Hidden duplicates:** case, leading or trailing spaces, non-breaking spaces and lookalike characters. LOWER(TRIM()) fixes the first two; others need cleaning rules (Part 10). Whether `=` is case-sensitive depends on the collation (Q39).
- **Engine differences (hedged, from memory, not executed here):** MySQL refuses a DELETE whose subquery reads the same table (error "You can't specify target table ... for update in FROM clause") unless you wrap it in a derived table; PostgreSQL allows it. Window-function dedup (`ROW_NUMBER() ... > 1`) is Part 4.
- **Safety:** run the SELECT version first, count the rows it would remove, and delete inside a transaction. Then add a UNIQUE constraint (on the normalised value if your engine supports it) so the problem does not come back.

**Then explain:**
- **Find duplicates:** GROUP BY the key, HAVING COUNT(*) > 1. HAVING because the condition is on the aggregate (Q3).
- **Which row to keep:** pick a rule (lowest id, earliest created_at); `MIN(user_id)` per key or the "no smaller id exists" test implement "keep lowest".
- **Why the casing trap:** the key is compared as bytes or by collation; clean it before comparing.
- **pandas:** `groupby("email").size()` for counts; `duplicated(keep=False)` shows all members; `drop_duplicates(subset="email", keep="first")` after sorting by user_id keeps the lowest.

**Follow-ups:**
- *How would you see the duplicate rows, not only counts?* Join the duplicate list back to users, or in pandas `df[df.duplicated("email", keep=False)]`.
- *How do you prevent them?* A UNIQUE constraint or unique index on the normalised email, plus validation at insert.
- *Why EXISTS rather than NOT IN with a subquery?* NOT IN breaks if the subquery returns a NULL (Q13); here MIN(user_id) is never NULL, but EXISTS is safer by habit.

**Common mistakes:**
- Deleting without checking what the SELECT returns first.
- Forgetting that NULL emails form a group.
- Treating 'B@x.com' and 'b@x.com ' as different customers.
- `DELETE ... WHERE user_id NOT IN (SELECT MIN(user_id) ... GROUP BY email)` without a NULL guard: it would delete all but one NULL-email row.

### Q8 ⭐⭐⭐ 🟡 AND/OR precedence and the filters IN, BETWEEN and LIKE. Given products(product_id, category, price, name), explain why 'WHERE category = ''toys'' OR category = ''games'' AND price > 500' does not mean what people expect, how BETWEEN treats its endpoints (inclusive), how IN differs from chained ORs with NULL, and how LIKE wildcards (% and _) work including a literal percent with ESCAPE. Give the pandas versions (parentheses with &, |, isin, between, str.contains with regex=False).
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** AND binds tighter than OR, so `category = 'toys' OR category = 'games' AND price > 500` means "toys at any price, or games above 500"; BETWEEN includes both endpoints, IN is shorthand for ORs but a NULL in the list never matches, and LIKE uses % for any run of characters and _ for exactly one.

**Schema and sample data:** (eight products; one has a NULL category, one has a literal % and one a literal _ in the name)
```sql
CREATE TABLE products (product_id INTEGER PRIMARY KEY, category TEXT, price INTEGER, name TEXT);
INSERT INTO products VALUES
 (1, 'toys',  100, 'Toy car'),
 (2, 'toys',  600, '50% off puzzle'),
 (3, 'games', 400, 'Board game'),
 (4, 'games', 700, 'Card game'),
 (5, 'books', 800, 'Novel'),
 (6, NULL,    900, 'Mystery box'),
 (7, 'toys',  500, 'toy_robot'),
 (8, 'games', 501, 'ToyBox');
```

**SQL answer:** the eight statements are in the `cases` list in the code block, each paired with its pandas mask. The key ones:
```sql
SELECT product_id FROM products WHERE category = 'toys' OR category = 'games' AND price > 500 ORDER BY product_id
```
```sql
SELECT product_id FROM products WHERE (category = 'toys' OR category = 'games') AND price > 500 ORDER BY product_id
```
```sql
SELECT product_id FROM products WHERE price BETWEEN 500 AND 700 ORDER BY product_id
```
```sql
SELECT product_id FROM products WHERE category NOT IN ('toys', NULL) ORDER BY product_id
```

**pandas answer:** parentheses are mandatory because `&` and `|` bind tighter than comparisons; `isin`, `between` and `str.contains(..., regex=False)` replace IN, BETWEEN and a literal LIKE.
```py
(p["category"] == "toys") | ((p["category"] == "games") & (p["price"] > 500))
((p["category"] == "toys") | (p["category"] == "games")) & (p["price"] > 500)
p["category"].isin(["toys", "games"]) & (p["price"] > 500)
p["price"].between(500, 700)
p["name"].str.contains("_", regex=False)
```

**Example:** products: 1 toys 100; 2 toys 600; 3 games 400; 4 games 700; 5 books 800; 6 NULL 900; 7 toys 500; 8 games 501. Without parentheses the filter is `toys OR (games AND price > 500)`, which returns 1, 2, 4, 7, 8 (every toy, plus games above 500). With parentheses it is `(toys OR games) AND price > 500`: 2, 4, 8. BETWEEN 500 AND 700 includes both 500 and 700 so it returns 2, 4, 7, 8. `category IN ('toys', NULL)` returns the toys (1, 2, 7) and nothing for the NULL. `category NOT IN ('toys', NULL)` returns nothing at all.

**Code:** (one block; run with `python3 -I`)
```python
# Q8: AND/OR precedence, BETWEEN, IN with NULL, LIKE and ESCAPE. SQLite 3.45 + pandas 3.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript(r"""
CREATE TABLE products (product_id INTEGER PRIMARY KEY, category TEXT, price INTEGER, name TEXT);
INSERT INTO products VALUES
 (1, 'toys',  100, 'Toy car'),
 (2, 'toys',  600, '50% off puzzle'),
 (3, 'games', 400, 'Board game'),
 (4, 'games', 700, 'Card game'),
 (5, 'books', 800, 'Novel'),
 (6, NULL,    900, 'Mystery box'),
 (7, 'toys',  500, 'toy_robot'),
 (8, 'games', 501, 'ToyBox');
""")

def ids(sql):
    return [r[0] for r in con.execute(sql)]

p = pd.read_sql_query("SELECT product_id, category, price, name FROM products", con)
def pids(mask):
    return sorted(p.loc[mask, "product_id"].tolist())

cases = [
 ("AND binds tighter than OR",
  "SELECT product_id FROM products WHERE category = 'toys' OR category = 'games' AND price > 500 ORDER BY product_id",
  (p["category"] == "toys") | ((p["category"] == "games") & (p["price"] > 500))),
 ("with parentheses",
  "SELECT product_id FROM products WHERE (category = 'toys' OR category = 'games') AND price > 500 ORDER BY product_id",
  ((p["category"] == "toys") | (p["category"] == "games")) & (p["price"] > 500)),
 ("IN list, same as the parenthesised ORs",
  "SELECT product_id FROM products WHERE category IN ('toys', 'games') AND price > 500 ORDER BY product_id",
  p["category"].isin(["toys", "games"]) & (p["price"] > 500)),
 ("BETWEEN is inclusive at both ends",
  "SELECT product_id FROM products WHERE price BETWEEN 500 AND 700 ORDER BY product_id",
  p["price"].between(500, 700)),
 ("LIKE: starts with 'To' then anything (SQLite LIKE ignores ASCII case)",
  "SELECT product_id FROM products WHERE name LIKE 'to%' ORDER BY product_id",
  p["name"].str.lower().str.startswith("to")),
 ("LIKE _ is exactly one character",
  "SELECT product_id FROM products WHERE name LIKE 'Toy ___' ORDER BY product_id",
  p["name"].str.fullmatch(r"(?i)toy ...")),
 ("literal underscore needs ESCAPE",
  r"SELECT product_id FROM products WHERE name LIKE '%\_%' ESCAPE '\' ORDER BY product_id",
  p["name"].str.contains("_", regex=False)),
 ("literal percent with ESCAPE",
  r"SELECT product_id FROM products WHERE name LIKE '%\%%' ESCAPE '\' ORDER BY product_id",
  p["name"].str.contains("%", regex=False)),
]
print("SQL id list == pandas mask id list for each case (both sorted by product_id)")
for label, sql, mask in cases:
    got, want = ids(sql), pids(mask)
    assert got == want, (label, got, want)
    print(f"{label:68s} {got}")

# NULL and IN: IN (..., NULL) never matches the NULL row; NOT IN with a NULL in the list matches nothing at all
in_null = ids("SELECT product_id FROM products WHERE category IN ('toys', NULL) ORDER BY product_id")
not_in_null = ids("SELECT product_id FROM products WHERE category NOT IN ('toys', NULL) ORDER BY product_id")
not_in_ok = ids("SELECT product_id FROM products WHERE category NOT IN ('toys', 'books') ORDER BY product_id")
chained = ids("SELECT product_id FROM products WHERE NOT (category = 'toys' OR category = NULL) ORDER BY product_id")
print("\ncategory IN ('toys', NULL)           ->", in_null)
print("category NOT IN ('toys', NULL)       ->", not_in_null, "(empty: NOT (x=toys OR x=NULL) is never TRUE)")
print("category NOT IN ('toys', 'books')    ->", not_in_ok, "(NULL category row 6 is NOT returned either)")
assert in_null == [1, 2, 7] and not_in_null == [] and chained == [] and not_in_ok == [3, 4, 8]
# pandas isin: NaN in the list matches NaN in the column (different from SQL)
print("pandas isin(['toys', None]) hits row 6?  ", 6 in pids(p["category"].isin(["toys", None])))
print("pandas ~isin(['toys','books']) hits row 6?", 6 in pids(~p["category"].isin(["toys", "books"])))
# pandas precedence trap: without parentheses & binds tighter than ==
try:
    p["category"] == "toys" & p["price"] > 500
except Exception as e:
    print("\nunparenthesised pandas mask raises:", type(e).__name__)
```
**Output (my run):**
```text
SQL id list == pandas mask id list for each case (both sorted by product_id)
AND binds tighter than OR                                            [1, 2, 4, 7, 8]
with parentheses                                                     [2, 4, 8]
IN list, same as the parenthesised ORs                               [2, 4, 8]
BETWEEN is inclusive at both ends                                    [2, 4, 7, 8]
LIKE: starts with 'To' then anything (SQLite LIKE ignores ASCII case) [1, 7, 8]
LIKE _ is exactly one character                                      [1]
literal underscore needs ESCAPE                                      [7]
literal percent with ESCAPE                                          [2]

category IN ('toys', NULL)           -> [1, 2, 7]
category NOT IN ('toys', NULL)       -> [] (empty: NOT (x=toys OR x=NULL) is never TRUE)
category NOT IN ('toys', 'books')    -> [3, 4, 8] (NULL category row 6 is NOT returned either)
pandas isin(['toys', None]) hits row 6?   True
pandas ~isin(['toys','books']) hits row 6? True

unparenthesised pandas mask raises: TypeError
```

**Edge cases:**
- **NOT IN with a NULL in the list:** `NOT IN ('toys', NULL)` expands to `category <> 'toys' AND category <> NULL`; the second part is never TRUE, so no row qualifies (empty result). Even `NOT IN ('toys', 'books')` leaves out the NULL-category row 6 (it returned 3, 4, 8), because NULL is not in the list and not outside it either (Q5, Q13).
- **pandas isin treats NaN as a value:** `isin(['toys', None])` matched the NaN row, and `~isin(['toys', 'books'])` included row 6, so the NULL row is kept in pandas but dropped in SQL.
- **LIKE case sensitivity (hedged):** SQLite's LIKE is case-insensitive for ASCII (row 8 'ToyBox' matched `'to%'` in my run). I recall PostgreSQL's LIKE is case-sensitive (ILIKE is the insensitive form) and MySQL follows the column collation, usually insensitive (not executed here).
- **ESCAPE:** SQLite has no default escape character, so you name one: `LIKE '%\%%' ESCAPE '\'` matches a literal percent and `'%\_%' ESCAPE '\'` a literal underscore. Some engines use backslash by default (not executed here).
- **pandas precedence error:** `p["category"] == "toys" & p["price"] > 500` raises a TypeError (shown in the output), because `&` is evaluated before `==`.
- **BETWEEN with dates and timestamps:** inclusive endpoints bite with timestamps (Q30). BETWEEN needs low then high; `BETWEEN 700 AND 500` returns nothing.
- **str.contains default is regex:** without `regex=False`, a name like `a.b` or `50%` behaves unexpectedly.

**Then explain:**
- **Precedence:** NOT first, then AND, then OR. When mixing AND and OR, always use parentheses; it protects readers as much as the engine.
- **BETWEEN a AND b** is `>= a AND <= b`; **IN (...)** is a list of ORs; both are TRUE/FALSE/UNKNOWN as usual and ignore rows where the tested value is NULL.
- **LIKE:** `%` any number of characters (including none), `_` exactly one; to match them literally use ESCAPE. Without wildcards it behaves like `=` (with pattern semantics).
- **pandas:** `&`, `|`, `~` with parentheses; `isin`, `between(inclusive="both")` by default, `str.contains(pat, regex=False)`, `str.startswith`.

**Follow-ups:**
- *How do you make the unparenthesised version read correctly?* Add the parentheses; do not rely on precedence knowledge.
- *Is `x IN (SELECT ...)` the same as ORs?* Logically yes, with the same NULL behaviour.
- *Does a leading wildcard use an index?* Usually not (Q21).

**Common mistakes:**
- Forgetting parentheses around OR conditions inside a larger AND.
- Assuming BETWEEN excludes the upper endpoint.
- Using `NOT IN` against a list or subquery that can contain NULL.
- Using `str.contains("50%")` or `"a_b"` in pandas without `regex=False` when the text is meant literally.

### Q9 ⭐⭐⭐ 🟡 Scenario: orders(order_id, customer_id, amount, status, created_at). Write a query for revenue and order count per month and per status for completed and shipped orders in one calendar year, sorted by month then revenue descending. Show grouping by two columns and by an expression, GROUP BY with an alias or ordinal (and why that is not portable), and the pandas groupby with named aggregation and as_index=False. Hedge the date-truncation dialects (strftime, DATE_TRUNC, DATE_FORMAT, FORMAT_DATE).
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** Filter the status and the year in WHERE (using a half-open date range), group by the month expression and the status, aggregate with SUM and COUNT, and sort by month then revenue descending; in pandas derive a month column, `groupby(["month", "status"], as_index=False).agg(...)` and `sort_values`.

**Schema and sample data:** (timestamps stored as ISO-8601 text; includes edge rows around the year boundary and a NULL timestamp)
```sql
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1,  1, 100, 'completed', '2025-01-05 10:00:00'),
 (2,  2, 250, 'completed', '2025-01-20 09:30:00'),
 (3,  1, 400, 'shipped',   '2025-01-31 23:59:59'),
 (4,  3, 900, 'cancelled', '2025-01-15 12:00:00'),
 (5,  2, 300, 'completed', '2025-02-02 08:00:00'),
 (6,  3, 300, 'shipped',   '2025-02-14 18:00:00'),
 (7,  1, 150, 'shipped',   '2025-02-20 11:00:00'),
 (8,  4,  80, 'completed', '2024-12-31 23:59:59'),
 (9,  4, 500, 'completed', '2025-12-31 23:59:59'),
 (10, 5, 700, 'completed', '2026-01-01 00:00:00'),
 (11, 5, 120, 'completed', NULL);
```

**SQL answer:** (the statement is `SQL` in the code block; `strftime` is SQLite's date formatter)
```sql
SELECT strftime('%Y-%m', created_at) AS month,
       status,
       SUM(amount) AS revenue,
       COUNT(*)    AS n_orders
FROM orders
WHERE status IN ('completed', 'shipped')
  AND created_at >= '2025-01-01' AND created_at < '2026-01-01'
GROUP BY strftime('%Y-%m', created_at), status
ORDER BY month, revenue DESC, status
```

**pandas answer:** convert to datetime, mask, derive the month column (the expression you group by), then `groupby(["month", "status"], as_index=False)` with named aggregation and a sort.
```py
o = pd.read_sql_query("SELECT order_id, amount, status, created_at FROM orders", con)
o["created_at"] = pd.to_datetime(o["created_at"])                      # NULL becomes NaT
m = o[o["status"].isin(["completed", "shipped"])
      & (o["created_at"] >= "2025-01-01") & (o["created_at"] < "2026-01-01")].copy()
m["month"] = m["created_at"].dt.strftime("%Y-%m")                       # group by an expression: derive a column first
pd_df = (m.groupby(["month", "status"], as_index=False)
           .agg(revenue=("amount", "sum"), n_orders=("order_id", "size"))
           .sort_values(["month", "revenue", "status"], ascending=[True, False, True])
           .reset_index(drop=True))
```

**Example:** the year filter and status filter keep orders 1, 2, 3, 5, 6, 7 and 9. Order 4 is cancelled, order 8 is on 2024-12-31 23:59:59 (before the range), order 10 is exactly 2026-01-01 00:00:00 (the exclusive upper bound) and order 11 has a NULL timestamp (the range comparison is UNKNOWN). January 2025: completed 100 + 250 = 350 over 2 orders; shipped 400 over 1 order. February: completed 300 over 1; shipped 300 + 150 = 450 over 2. December: completed 500 over 1 (order 9 at 23:59:59 on 31 December is included). Within January, shipped (400) sorts before completed (350) because revenue is descending after month.

**Code:** (one block; run with `python3 -I`)
```python
# Q9: revenue and order count per month and status. SQLite 3.45 + pandas 3.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1,  1, 100, 'completed', '2025-01-05 10:00:00'),
 (2,  2, 250, 'completed', '2025-01-20 09:30:00'),
 (3,  1, 400, 'shipped',   '2025-01-31 23:59:59'),
 (4,  3, 900, 'cancelled', '2025-01-15 12:00:00'),
 (5,  2, 300, 'completed', '2025-02-02 08:00:00'),
 (6,  3, 300, 'shipped',   '2025-02-14 18:00:00'),
 (7,  1, 150, 'shipped',   '2025-02-20 11:00:00'),
 (8,  4,  80, 'completed', '2024-12-31 23:59:59'),
 (9,  4, 500, 'completed', '2025-12-31 23:59:59'),
 (10, 5, 700, 'completed', '2026-01-01 00:00:00'),
 (11, 5, 120, 'completed', NULL);
""")

def q(sql):
    return pd.read_sql_query(sql, con)

SQL = """
SELECT strftime('%Y-%m', created_at) AS month,
       status,
       SUM(amount) AS revenue,
       COUNT(*)    AS n_orders
FROM orders
WHERE status IN ('completed', 'shipped')
  AND created_at >= '2025-01-01' AND created_at < '2026-01-01'
GROUP BY strftime('%Y-%m', created_at), status
ORDER BY month, revenue DESC, status
"""
sql_df = q(SQL)

# --- pandas version
o = pd.read_sql_query("SELECT order_id, amount, status, created_at FROM orders", con)
o["created_at"] = pd.to_datetime(o["created_at"])                      # NULL becomes NaT
m = o[o["status"].isin(["completed", "shipped"])
      & (o["created_at"] >= "2025-01-01") & (o["created_at"] < "2026-01-01")].copy()
m["month"] = m["created_at"].dt.strftime("%Y-%m")                       # group by an expression: derive a column first
pd_df = (m.groupby(["month", "status"], as_index=False)
           .agg(revenue=("amount", "sum"), n_orders=("order_id", "size"))
           .sort_values(["month", "revenue", "status"], ascending=[True, False, True])
           .reset_index(drop=True))
# --- end pandas
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("SQL == pandas (compared in the output order: month asc, revenue desc, status asc)")
print(sql_df.to_string(index=False))

# GROUP BY alias and ordinal give the same rows in SQLite (not portable)
alias = q("""SELECT strftime('%Y-%m', created_at) AS month, status, SUM(amount) AS revenue, COUNT(*) AS n_orders
FROM orders WHERE status IN ('completed', 'shipped') AND created_at >= '2025-01-01' AND created_at < '2026-01-01'
GROUP BY month, status ORDER BY month, revenue DESC, status""")
ordinal = q("""SELECT strftime('%Y-%m', created_at) AS month, status, SUM(amount) AS revenue, COUNT(*) AS n_orders
FROM orders WHERE status IN ('completed', 'shipped') AND created_at >= '2025-01-01' AND created_at < '2026-01-01'
GROUP BY 1, 2 ORDER BY 1, 3 DESC, 2""")
pd.testing.assert_frame_equal(alias, sql_df)
pd.testing.assert_frame_equal(ordinal, sql_df)
print("\nGROUP BY month, status and GROUP BY 1, 2 return the same rows in SQLite")

# Boundary rows: what the half-open year filter did with the edge timestamps
edge = q("SELECT order_id, created_at FROM orders WHERE order_id IN (8, 9, 10, 11) ORDER BY order_id")
in_year = set(m["order_id"])
print("\nedge rows and whether they are in the 2025 result:")
for oid, ts in edge.values.tolist():
    print(f"  order {oid:2d}  {ts}  in result: {oid in in_year}")
assert in_year.isdisjoint({8, 10, 11}) and 9 in in_year
# pandas default sort: groupby sorts group keys; SQL without ORDER BY promises nothing
print("\npandas groupby sort=True orders by (month, status) before our sort_values:",
      m.groupby(["month", "status"], as_index=False).size()[["month", "status"]].values.tolist())
```
**Output (my run):**
```text
SQL == pandas (compared in the output order: month asc, revenue desc, status asc)
  month    status  revenue  n_orders
2025-01   shipped      400         1
2025-01 completed      350         2
2025-02   shipped      450         2
2025-02 completed      300         1
2025-12 completed      500         1

GROUP BY month, status and GROUP BY 1, 2 return the same rows in SQLite

edge rows and whether they are in the 2025 result:
  order  8  2024-12-31 23:59:59  in result: False
  order  9  2025-12-31 23:59:59  in result: True
  order 10  2026-01-01 00:00:00  in result: False
  order 11  nan  in result: False

pandas groupby sort=True orders by (month, status) before our sort_values: [['2025-01', 'completed'], ['2025-01', 'shipped'], ['2025-02', 'completed'], ['2025-02', 'shipped'], ['2025-12', 'completed']]
```

**Edge cases:**
- **Alias and ordinal in GROUP BY:** `GROUP BY month, status` and `GROUP BY 1, 2` both returned the same rows in SQLite (asserted in the code). Alias support in GROUP BY varies by engine (I recall PostgreSQL, MySQL and BigQuery accept it and SQL Server and Oracle do not; not executed here), and ordinals break when the SELECT list is reordered, so repeating the expression is the portable form (Q23).
- **Missing months:** a month with no completed or shipped orders produces no row. To show zeros you need a calendar table and a left join (Part 6).
- **NULL timestamps and NULL statuses:** both fall out of the WHERE (UNKNOWN is not TRUE); say so if the business wants them counted.
- **Year boundary:** `created_at < '2026-01-01'` is safer than `BETWEEN '2025-01-01' AND '2025-12-31'`, which would drop 2025-12-31 23:59:59 unless the time is included (Q30).
- **Time zones:** if created_at is UTC and the business reports in IST, the month boundary shifts by 5 hours 30 minutes; convert before truncating (engine-specific, not executed here).
- **Date truncation by dialect (hedged, from memory, not executed here):** PostgreSQL `DATE_TRUNC('month', created_at)` or `TO_CHAR(created_at, 'YYYY-MM')`; MySQL `DATE_FORMAT(created_at, '%Y-%m')`; BigQuery `FORMAT_DATE('%Y-%m', DATE(created_at))` or `DATE_TRUNC(DATE(created_at), MONTH)`; Snowflake `DATE_TRUNC('month', created_at)`; SQL Server `FORMAT(created_at, 'yyyy-MM')` or `DATEFROMPARTS(YEAR(created_at), MONTH(created_at), 1)`.
- **Sort order:** `revenue DESC` ties within a month are broken by status, so the output is deterministic (Q14). In pandas, `groupby` sorts group keys by default (`sort=True`), but SQL gives no order without ORDER BY (Q31).

**Then explain:**
- **Two grouping columns:** one row per (month, status) combination that exists in the filtered data.
- **Grouping by an expression:** the SELECT expression must match the GROUP BY expression; in pandas derive the column first.
- **WHERE vs ORDER BY:** filters go in WHERE (before grouping); ORDER BY may use the aliases because it runs after SELECT (Q2).
- **Strings as dates:** ISO-8601 text sorts and compares correctly in SQLite; elsewhere use real DATE or TIMESTAMP columns.

**Follow-ups:**
- *How do you get a year-over-year comparison?* Later parts (Part 6) use windows and self-joins.
- *Why `COUNT(*)` and not `COUNT(amount)`?* The question asks for orders; COUNT(amount) would skip NULL amounts.
- *What does `as_index=False` change?* It keeps `month` and `status` as ordinary columns instead of a MultiIndex.

**Common mistakes:**
- `BETWEEN '2025-01-01' AND '2025-12-31'` on timestamps.
- Grouping by `month` alone and then selecting status (non-grouped column).
- Using `GROUP BY 1, 2` in shared code and then reordering the SELECT.
- Sorting by revenue only, so months interleave.

### Q10 ⭐⭐⭐ 🟡 Conditional aggregation: orders(order_id, customer_id, amount, status, created_at) with status in completed, cancelled, refunded. In one pass per customer, return total orders, completed orders, cancelled orders, cancel rate as a percentage and revenue from completed orders only, using SUM(CASE WHEN ...) and COUNT(CASE WHEN ...). Explain why COUNT(CASE WHEN ... THEN 1 ELSE 0 END) is a bug, and the integer-division trap in the rate. Show the pandas version with agg and boolean sums.
**Asked at:** interview-prep guide and platform question bank (StrataScratch, DataLemur style), not a candidate report; product-company data scientist screens
**Say this first (1 line):** Put the condition inside the aggregate: `SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)` or `COUNT(CASE WHEN ... THEN 1 END)` (no ELSE), because COUNT counts every non-NULL value and a 0 is not NULL; and multiply by 100.0 before dividing to avoid integer division.

**Schema and sample data:** (four customers: mixed history, no completed orders, mostly completed, and mostly cancelled)
```sql
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1, 1, 100, 'completed', '2025-01-05'),
 (2, 1, 200, 'completed', '2025-01-09'),
 (3, 1, 300, 'cancelled', '2025-01-20'),
 (4, 2, 400, 'cancelled', '2025-02-01'),
 (5, 2, 500, 'refunded',  '2025-02-11'),
 (6, 3, 600, 'completed', '2025-03-02'),
 (7, 3, 700, 'cancelled', '2025-03-15'),
 (8, 3, 800, 'completed', '2025-03-16'),
 (9, 3, 900, 'completed', '2025-03-17'),
 (10,3, 50,  'refunded',  '2025-03-18'),
 (11,4, 60,  'completed', '2025-04-01'),
 (12,4, 70,  'cancelled', '2025-04-02'),
 (13,4, 80,  'cancelled', '2025-04-03');
```

**SQL answer:** (the statement is `SQL` in the code block)
```sql
SELECT customer_id,
       COUNT(*)                                                    AS total_orders,
       COUNT(CASE WHEN status = 'completed' THEN 1 END)            AS completed_orders,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)       AS cancelled_orders,
       ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_rate_pct,
       COALESCE(SUM(CASE WHEN status = 'completed' THEN amount END), 0) AS completed_revenue
FROM orders
GROUP BY customer_id
ORDER BY customer_id
```

**pandas answer:** build boolean helper columns, then sum them in `agg` (True counts as 1); `where` keeps only completed amounts.
```py
o = pd.read_sql_query("SELECT order_id, customer_id, amount, status FROM orders", con)
o = o.assign(is_completed=o["status"] == "completed",
             is_cancelled=o["status"] == "cancelled",
             completed_amount=o["amount"].where(o["status"] == "completed", 0))
pd_df = (o.groupby("customer_id", as_index=False)
           .agg(total_orders=("order_id", "size"),
                completed_orders=("is_completed", "sum"),       # sum of booleans counts the True rows
                cancelled_orders=("is_cancelled", "sum"),
                completed_revenue=("completed_amount", "sum")))
pd_df["cancel_rate_pct"] = (100 * pd_df["cancelled_orders"] / pd_df["total_orders"]).round(2)
pd_df = pd_df[["customer_id", "total_orders", "completed_orders", "cancelled_orders", "cancel_rate_pct", "completed_revenue"]]
```

**Example:** customer 1 has orders: completed 100, completed 200, cancelled 300. Total 3, completed 2, cancelled 1, cancel rate 100 x 1 / 3 = 33.33, completed revenue 300. Customer 2 has cancelled 400 and refunded 500: total 2, completed 0, cancelled 1, rate 50.00, completed revenue NULL from the SUM, turned into 0 by COALESCE. Customer 3 has five orders (three completed 600, 800, 900 = 2,300; one cancelled; one refunded): rate 20.00. Customer 4: completed 60, cancelled 70 and 80: total 3, rate 66.67, completed revenue 60.

**Code:** (one block; run with `python3 -I`)
```python
# Q10: conditional aggregation per customer. SQLite 3.45 + pandas 3.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1, 1, 100, 'completed', '2025-01-05'),
 (2, 1, 200, 'completed', '2025-01-09'),
 (3, 1, 300, 'cancelled', '2025-01-20'),
 (4, 2, 400, 'cancelled', '2025-02-01'),
 (5, 2, 500, 'refunded',  '2025-02-11'),
 (6, 3, 600, 'completed', '2025-03-02'),
 (7, 3, 700, 'cancelled', '2025-03-15'),
 (8, 3, 800, 'completed', '2025-03-16'),
 (9, 3, 900, 'completed', '2025-03-17'),
 (10,3, 50,  'refunded',  '2025-03-18'),
 (11,4, 60,  'completed', '2025-04-01'),
 (12,4, 70,  'cancelled', '2025-04-02'),
 (13,4, 80,  'cancelled', '2025-04-03');
""")

def q(sql):
    return pd.read_sql_query(sql, con)

SQL = """
SELECT customer_id,
       COUNT(*)                                                    AS total_orders,
       COUNT(CASE WHEN status = 'completed' THEN 1 END)            AS completed_orders,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)       AS cancelled_orders,
       ROUND(100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_rate_pct,
       COALESCE(SUM(CASE WHEN status = 'completed' THEN amount END), 0) AS completed_revenue
FROM orders
GROUP BY customer_id
ORDER BY customer_id
"""
sql_df = q(SQL)

# --- pandas version
o = pd.read_sql_query("SELECT order_id, customer_id, amount, status FROM orders", con)
o = o.assign(is_completed=o["status"] == "completed",
             is_cancelled=o["status"] == "cancelled",
             completed_amount=o["amount"].where(o["status"] == "completed", 0))
pd_df = (o.groupby("customer_id", as_index=False)
           .agg(total_orders=("order_id", "size"),
                completed_orders=("is_completed", "sum"),       # sum of booleans counts the True rows
                cancelled_orders=("is_cancelled", "sum"),
                completed_revenue=("completed_amount", "sum")))
pd_df["cancel_rate_pct"] = (100 * pd_df["cancelled_orders"] / pd_df["total_orders"]).round(2)
pd_df = pd_df[["customer_id", "total_orders", "completed_orders", "cancelled_orders", "cancel_rate_pct", "completed_revenue"]]
# --- end pandas
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("SQL == pandas (compared after ORDER BY customer_id; dtypes not compared)")
print(sql_df.to_string(index=False))

# The COUNT(CASE ... ELSE 0) bug: COUNT counts every non-NULL value, and 0 is not NULL
bug = q("""SELECT customer_id, COUNT(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) AS completed_wrong, COUNT(*) AS total
           FROM orders GROUP BY customer_id ORDER BY customer_id""")
print("\nCOUNT(CASE ... THEN 1 ELSE 0 END) equals COUNT(*):")
print(bug.to_string(index=False))
assert (bug["completed_wrong"] == bug["total"]).all()

# Integer division trap: 100 * cancelled / total with integers truncates in SQLite (and in PostgreSQL, SQL Server)
trap = q("""SELECT customer_id,
       100 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*)   AS int_division,
       100.0 * SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) / COUNT(*) AS float_division
FROM orders GROUP BY customer_id ORDER BY customer_id""")
print("\ninteger vs decimal rate:")
print(trap.to_string(index=False))
assert trap["int_division"].tolist() == [33, 50, 20, 66]
# The classic version: cancelled / COUNT(*) before multiplying
frac = con.execute("SELECT SUM(CASE WHEN status='cancelled' THEN 1 ELSE 0 END) / COUNT(*) FROM orders WHERE customer_id = 1").fetchone()[0]
print("cancelled / COUNT(*) for customer 1 as integers:", frac, "(0, so the rate shows 0)")
assert frac == 0
```
**Output (my run):**
```text
SQL == pandas (compared after ORDER BY customer_id; dtypes not compared)
 customer_id  total_orders  completed_orders  cancelled_orders  cancel_rate_pct  completed_revenue
           1             3                 2                 1            33.33                300
           2             2                 0                 1            50.00                  0
           3             5                 3                 1            20.00               2300
           4             3                 1                 2            66.67                 60

COUNT(CASE ... THEN 1 ELSE 0 END) equals COUNT(*):
 customer_id  completed_wrong  total
           1                3      3
           2                2      2
           3                5      5
           4                3      3

integer vs decimal rate:
 customer_id  int_division  float_division
           1            33       33.333333
           2            50       50.000000
           3            20       20.000000
           4            66       66.666667
cancelled / COUNT(*) for customer 1 as integers: 0 (0, so the rate shows 0)
```

**Edge cases:**
- **Why `COUNT(CASE WHEN ... THEN 1 ELSE 0 END)` is a bug:** the ELSE 0 gives a non-NULL value on every row, and COUNT counts non-NULL values, so it equals COUNT(*). In my run the "completed" column came out as 3, 2, 5, 3, the same as the total. Either drop the ELSE (COUNT ignores the NULL) or use SUM(... THEN 1 ELSE 0).
- **Integer-division trap:** `100 * cancelled / COUNT(*)` with integer operands gave 33, 50, 20, 66 in SQLite (truncated, and 66 not 67), and `cancelled / COUNT(*)` for customer 1 is 0. Using `100.0 *` first fixes it. I recall PostgreSQL and SQL Server also truncate integer division, while MySQL's `/` returns a decimal and Oracle's does too (not executed here); do not depend on it.
- **No completed orders:** `SUM(CASE ... THEN amount END)` is NULL for customer 2, so without COALESCE the report shows NULL, not 0. With COUNT(CASE ...) you get 0 correctly.
- **Refunded orders** are neither completed nor cancelled; they count in total_orders but in neither bucket. State this to the interviewer.
- **NULL status:** a NULL status matches no WHEN, so it counts only in the total. Define the bucket for it explicitly.
- **Rounding:** SQLite ROUND and pandas `round(2)` agreed on these values (33.33, 66.67); engines and pandas may differ on exact ties (half away from zero versus banker's rounding, Q40).
- **FILTER clause:** `COUNT(*) FILTER (WHERE status = 'completed')` is shorter in SQLite and PostgreSQL; MySQL lacks it (Q34).

**Then explain:**
- **One pass:** conditional aggregation computes many filtered measures in a single scan and a single GROUP BY, instead of several subqueries or joins.
- **CASE returns NULL by default,** so `SUM(CASE WHEN c THEN amount END)` sums only the matching rows and COUNT(CASE WHEN c THEN 1 END) counts them.
- **Rate:** divide by COUNT(*) (all orders) and make at least one operand decimal.
- **pandas:** boolean columns summed in `agg`, or `groupby(...).apply`; the named-aggregation form is vectorised and faster.

**Follow-ups:**
- *Why not use WHERE status = 'completed' for the revenue?* It would also remove the cancelled rows from the total and cancelled counts; conditional aggregation keeps them.
- *How do you compute a rate with a different denominator?* Use the right COUNT, for example the non-refunded orders.
- *How do you do the same per month?* Add the month expression to GROUP BY.

**Common mistakes:**
- COUNT(CASE ... ELSE 0).
- Integer division in the rate.
- Forgetting COALESCE and returning NULL revenue.
- Dividing by zero when a group has no rows (a group always has at least one row in GROUP BY, but a filtered denominator can be 0: use NULLIF).

### Q11 ⭐⭐⭐ 🟡 Find all customers who placed more than 2 orders in 2025 and show their order count and average order value. Using orders(order_id, customer_id, amount, status, created_at), put each condition in the right clause (year filter, count threshold), explain what changes if cancelled orders must be excluded, and show the pandas version with groupby().agg() then a boolean filter or query(). Mention COUNT(*) vs COUNT(DISTINCT order_id) when the table can hold duplicate rows.
**Asked at:** public LeetCode-style problem bank (SQL 50 style problems), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Put the 2025 date filter in WHERE (row filter, half-open range), group by customer, and put the count threshold in HAVING; if cancelled orders must go, add the status condition to WHERE (not HAVING) and handle NULL status.

**Schema and sample data:** (`orders` is clean; `orders_dup` has no primary key and holds repeated rows from a bad load)
```sql
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1,  1, 100, 'completed', '2025-01-05'),
 (2,  1, 200, 'completed', '2025-03-09'),
 (3,  1, 300, 'cancelled', '2025-06-20'),
 (4,  1, 900, 'completed', '2024-12-31'),
 (5,  2, 400, 'completed', '2025-02-01'),
 (6,  2, 500, 'completed', '2025-02-11'),
 (7,  3, 600, 'completed', '2025-03-02'),
 (8,  3, 700, 'completed', '2025-04-15'),
 (9,  3, 800, 'completed', '2025-05-16'),
 (10, 3, 900, 'cancelled', '2025-06-17'),
 (11, 4, 50,  NULL,        '2025-07-01'),
 (12, 4, 60,  'completed', '2025-07-02'),
 (13, 4, 70,  'completed', '2025-07-03');
-- the same orders loaded twice by a bad pipeline step, plus order 7 duplicated: no primary key
CREATE TABLE orders_dup AS SELECT * FROM orders WHERE customer_id = 2 OR order_id IN (7, 8);
INSERT INTO orders_dup SELECT * FROM orders WHERE order_id = 5;
```

**SQL answer:** (the statement is `SQL` in the code block)
```sql
SELECT customer_id, COUNT(*) AS order_count, AVG(amount) AS avg_order_value
FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'
GROUP BY customer_id
HAVING COUNT(*) > 2
ORDER BY customer_id
```
Excluding cancelled orders (`SQL_EXCL`):
```sql
SELECT customer_id, COUNT(*) AS order_count, AVG(amount) AS avg_order_value
FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'
  AND (status <> 'cancelled' OR status IS NULL)
GROUP BY customer_id
HAVING COUNT(*) > 2
ORDER BY customer_id
```
With duplicate rows:
```sql
SELECT customer_id, COUNT(*) AS n_rows, COUNT(DISTINCT order_id) AS n_orders
FROM orders_dup GROUP BY customer_id HAVING COUNT(*) > 2 ORDER BY customer_id
```

**pandas answer:** filter by date with a mask, `groupby().agg(...)` with named aggregation, then `query()` (or a boolean filter) for the count threshold.
```py
o = pd.read_sql_query("SELECT order_id, customer_id, amount, status, created_at FROM orders", con)
o["created_at"] = pd.to_datetime(o["created_at"])
y = o[(o["created_at"] >= "2025-01-01") & (o["created_at"] < "2026-01-01")]
agg = y.groupby("customer_id", as_index=False).agg(order_count=("order_id", "size"), avg_order_value=("amount", "mean"))
pd_df = agg.query("order_count > 2").sort_values("customer_id").reset_index(drop=True)
```

**Example:** 2025 orders per customer: customer 1 has orders 1, 2, 3 in 2025 (order 4 is 2024-12-31 and is excluded by the date filter): count 3, average (100 + 200 + 300) / 3 = 200. Customer 2 has 2 orders (not more than 2). Customer 3 has 4 (600, 700, 800, 900): average 750. Customer 4 has 3 (50, 60, 70): average 60. So the result is customers 1, 3 and 4. Excluding cancelled: customer 1 drops to 2 orders (order 3 is cancelled) and falls out; customer 3 drops to 3 orders (600, 700, 800), average 700; customer 4 keeps 3 because order 11 has a NULL status and the `OR status IS NULL` keeps it.

**Code:** (one block; run with `python3 -I`)
```python
# Q11: customers with more than 2 orders in 2025, with count and average order value. SQLite 3.45 + pandas 3.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1,  1, 100, 'completed', '2025-01-05'),
 (2,  1, 200, 'completed', '2025-03-09'),
 (3,  1, 300, 'cancelled', '2025-06-20'),
 (4,  1, 900, 'completed', '2024-12-31'),
 (5,  2, 400, 'completed', '2025-02-01'),
 (6,  2, 500, 'completed', '2025-02-11'),
 (7,  3, 600, 'completed', '2025-03-02'),
 (8,  3, 700, 'completed', '2025-04-15'),
 (9,  3, 800, 'completed', '2025-05-16'),
 (10, 3, 900, 'cancelled', '2025-06-17'),
 (11, 4, 50,  NULL,        '2025-07-01'),
 (12, 4, 60,  'completed', '2025-07-02'),
 (13, 4, 70,  'completed', '2025-07-03');
-- the same orders loaded twice by a bad pipeline step, plus order 7 duplicated: no primary key
CREATE TABLE orders_dup AS SELECT * FROM orders WHERE customer_id = 2 OR order_id IN (7, 8);
INSERT INTO orders_dup SELECT * FROM orders WHERE order_id = 5;
""")

def q(sql):
    return pd.read_sql_query(sql, con)

SQL = """
SELECT customer_id, COUNT(*) AS order_count, AVG(amount) AS avg_order_value
FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'
GROUP BY customer_id
HAVING COUNT(*) > 2
ORDER BY customer_id
"""
sql_df = q(SQL)

# --- pandas version
o = pd.read_sql_query("SELECT order_id, customer_id, amount, status, created_at FROM orders", con)
o["created_at"] = pd.to_datetime(o["created_at"])
y = o[(o["created_at"] >= "2025-01-01") & (o["created_at"] < "2026-01-01")]
agg = y.groupby("customer_id", as_index=False).agg(order_count=("order_id", "size"), avg_order_value=("amount", "mean"))
pd_df = agg.query("order_count > 2").sort_values("customer_id").reset_index(drop=True)
# --- end pandas
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("2025, more than 2 orders: SQL == pandas groupby().agg() then query() (sorted by customer_id)")
print(sql_df.to_string(index=False))

# Excluding cancelled orders. status = NULL for order 11 is the trap: <> 'cancelled' would drop it.
SQL_EXCL = """
SELECT customer_id, COUNT(*) AS order_count, AVG(amount) AS avg_order_value
FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01'
  AND (status <> 'cancelled' OR status IS NULL)
GROUP BY customer_id
HAVING COUNT(*) > 2
ORDER BY customer_id
"""
excl = q(SQL_EXCL)
y2 = y[(y["status"] != "cancelled") | y["status"].isna()]       # pandas != keeps NaN, which matches the IS NULL branch
pd_excl = (y2.groupby("customer_id", as_index=False).agg(order_count=("order_id", "size"), avg_order_value=("amount", "mean"))
           .query("order_count > 2").reset_index(drop=True))
pd.testing.assert_frame_equal(excl, pd_excl, check_dtype=False)
print("\nexcluding cancelled (NULL status kept):")
print(excl.to_string(index=False))
naive_excl = q("""SELECT customer_id, COUNT(*) AS order_count FROM orders
WHERE created_at >= '2025-01-01' AND created_at < '2026-01-01' AND status <> 'cancelled'
GROUP BY customer_id HAVING COUNT(*) > 2 ORDER BY customer_id""")
print("with the naive status <> 'cancelled' (drops NULL status):", naive_excl.values.tolist())
assert naive_excl["customer_id"].tolist() == [3] and excl["customer_id"].tolist() == [3, 4]

# Duplicated rows: COUNT(*) vs COUNT(DISTINCT order_id)
dup = q("""SELECT customer_id, COUNT(*) AS n_rows, COUNT(DISTINCT order_id) AS n_orders
FROM orders_dup GROUP BY customer_id HAVING COUNT(*) > 2 ORDER BY customer_id""")
print("\norders_dup, rows vs distinct orders for customers with more than 2 rows:")
print(dup.to_string(index=False))
d = pd.read_sql_query("SELECT order_id, customer_id, amount FROM orders_dup", con)
pd_dup = d.groupby("customer_id").agg(n_rows=("order_id", "size"), n_orders=("order_id", "nunique")).query("n_rows > 2").reset_index()
pd.testing.assert_frame_equal(dup, pd_dup, check_dtype=False)
```
**Output (my run):**
```text
2025, more than 2 orders: SQL == pandas groupby().agg() then query() (sorted by customer_id)
 customer_id  order_count  avg_order_value
           1            3            200.0
           3            4            750.0
           4            3             60.0

excluding cancelled (NULL status kept):
 customer_id  order_count  avg_order_value
           3            3            700.0
           4            3             60.0
with the naive status <> 'cancelled' (drops NULL status): [[3, 3]]

orders_dup, rows vs distinct orders for customers with more than 2 rows:
 customer_id  n_rows  n_orders
           2       3         2
```

**Edge cases:**
- **Status exclusion and NULLs:** the naive `status <> 'cancelled'` dropped the NULL-status order (11) and customer 4 fell to 2 orders, so only customer 3 remained (shown in the output). Decide whether NULL means "not cancelled" and write it explicitly (Q5). pandas `!= 'cancelled'` keeps NaN, so the pandas version needed no extra clause but behaves the opposite way by default.
- **Duplicate rows:** `orders_dup` repeats order 5 (customer 2), so COUNT(*) says 3 rows but COUNT(DISTINCT order_id) says 2 orders; customer 2 would wrongly pass the "more than 2" threshold. The average is also distorted by duplicates. Deduplicate first (Q7) or count distinct ids, and fix the source if you can.
- **Threshold:** "more than 2" is `> 2`; "at least 2" is `>= 2`.
- **Customers with zero orders** are not in the table at all, so they cannot appear (and should not for a `> 2` rule).
- **Date boundaries:** timestamps on 31 December need `< '2026-01-01'`, not `<= '2025-12-31'` (Q30).
- **AVG:** order value average skips NULL amounts; COUNT(*) counts the rows including them, so use COUNT(amount) if the denominator must match.

**Then explain:**
- **WHERE vs HAVING:** year and status are row conditions (WHERE); the count threshold depends on the group (HAVING). The year condition in WHERE also lets an index on created_at be used.
- **COUNT(*) vs COUNT(DISTINCT order_id):** identical when order_id is a key; different when the table can hold repeated rows.
- **Changing the exclusion:** a status filter changes both the counts and the averages, because it is applied before grouping.
- **pandas:** `agg` gives a frame with the counts and means; `query("order_count > 2")` is the HAVING step.

**Follow-ups:**
- *How would you also show each customer's cancelled count?* Use conditional aggregation (Q10) instead of excluding in WHERE.
- *What if created_at is a timestamp with time zone?* Convert to the reporting time zone before applying the year range.
- *What index helps?* One on `(created_at, customer_id)` or `(customer_id, created_at)` depending on selectivity (Part 11).

**Common mistakes:**
- Putting `COUNT(*) > 2` in WHERE (an error).
- Putting the year filter in HAVING.
- Filtering `status <> 'cancelled'` and silently losing NULL status rows.
- Using COUNT(*) on a table that can have duplicate order rows.

### Q12 ⭐⭐⭐ 🟡 Top-N basics: from orders(order_id, customer_id, amount, status, created_at), return the top 3 customers by total completed revenue. Explain ORDER BY ... DESC LIMIT 3, why a tie at rank 3 makes the answer ambiguous, how to make the result deterministic with a tie-breaker column, what 'LIMIT without ORDER BY' guarantees (nothing), and how TOP (SQL Server) and FETCH FIRST differ (hedged). Pandas: sort_values, head, nlargest and its keep parameter. (Ranking with ties via window functions is Part 4.)
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** Sum completed revenue per customer, ORDER BY revenue DESC and add a tie-breaker column so the order is fully specified, then LIMIT 3; without a tie-breaker a tie at rank 3 means the database may return either customer, and LIMIT without ORDER BY promises no particular rows at all.

**Schema and sample data:** (customer totals of completed orders: 1 is 900, 2 is 800, 3 and 4 are 500 each, 5 and 6 are 100 each; order 7 is a cancelled 999 that must not count)
```sql
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1,  5, 100, 'completed', '2025-01-01'),
 (2,  3, 300, 'completed', '2025-01-02'),
 (3,  4, 500, 'completed', '2025-01-03'),
 (4,  1, 900, 'completed', '2025-01-04'),
 (5,  3, 200, 'completed', '2025-01-05'),
 (6,  2, 800, 'completed', '2025-01-06'),
 (7,  2, 999, 'cancelled', '2025-01-07'),
 (8,  6, 100, 'completed', '2025-01-08');
```

**SQL answer:** (the statement is `SQL` in the code block)
```sql
SELECT customer_id, SUM(amount) AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY customer_id
ORDER BY revenue DESC, customer_id ASC
LIMIT 3
```
Keeping everybody who ties with the third value (`SQL_TIES`; SQLite has no WITH TIES, so the third value is used as a threshold):
```sql
WITH t AS (SELECT customer_id, SUM(amount) AS revenue FROM orders WHERE status = 'completed' GROUP BY customer_id)
SELECT customer_id, revenue FROM t
WHERE revenue >= (SELECT revenue FROM t ORDER BY revenue DESC LIMIT 1 OFFSET 2)
ORDER BY revenue DESC, customer_id
```

**pandas answer:** `sort_values` with the same two keys then `head(3)`; or `nlargest(3, "revenue", keep=...)`.
```py
o = pd.read_sql_query("SELECT order_id, customer_id, amount, status FROM orders", con)
rev = o[o["status"] == "completed"].groupby("customer_id", as_index=False).agg(revenue=("amount", "sum"))
pd_df = rev.sort_values(["revenue", "customer_id"], ascending=[False, True]).head(3).reset_index(drop=True)
```
and the `nlargest` variants:
```py
by_first = rev.nlargest(3, "revenue", keep="first")["customer_id"].tolist()
by_last = rev.nlargest(3, "revenue", keep="last")["customer_id"].tolist()
by_all = rev.nlargest(3, "revenue", keep="all").sort_values(["revenue", "customer_id"], ascending=[False, True]).reset_index(drop=True)
```

**Example:** completed totals: customer 1 = 900, customer 2 = 800, customers 3 and 4 = 500 each, customers 5 and 6 = 100 each. The top two are clear (1 and 2). For third place, 3 and 4 are tied at 500, so "top 3 customers" has two correct answers unless a rule decides. With `ORDER BY revenue DESC, customer_id ASC LIMIT 3` the rule is "lower id wins", giving 1, 2, 3 every time. Customer 2's cancelled 999 order is excluded by the WHERE, otherwise customer 2 would have 1,799 and rank first.

**Code:** (one block; run with `python3 -I`)
```python
# Q12: top 3 customers by completed revenue, ties, determinism. SQLite 3.45 + pandas 3.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1,  5, 100, 'completed', '2025-01-01'),
 (2,  3, 300, 'completed', '2025-01-02'),
 (3,  4, 500, 'completed', '2025-01-03'),
 (4,  1, 900, 'completed', '2025-01-04'),
 (5,  3, 200, 'completed', '2025-01-05'),
 (6,  2, 800, 'completed', '2025-01-06'),
 (7,  2, 999, 'cancelled', '2025-01-07'),
 (8,  6, 100, 'completed', '2025-01-08');
""")

def q(sql):
    return pd.read_sql_query(sql, con)

# Totals: 1 -> 900, 2 -> 800, 3 -> 500, 4 -> 500, 5 -> 100, 6 -> 100. A tie sits at rank 3.
SQL = """
SELECT customer_id, SUM(amount) AS revenue
FROM orders
WHERE status = 'completed'
GROUP BY customer_id
ORDER BY revenue DESC, customer_id ASC
LIMIT 3
"""
sql_df = q(SQL)

# --- pandas version
o = pd.read_sql_query("SELECT order_id, customer_id, amount, status FROM orders", con)
rev = o[o["status"] == "completed"].groupby("customer_id", as_index=False).agg(revenue=("amount", "sum"))
pd_df = rev.sort_values(["revenue", "customer_id"], ascending=[False, True]).head(3).reset_index(drop=True)
# --- end pandas
pd.testing.assert_frame_equal(sql_df, pd_df)
print("top 3 with tie-breaker: SQL == pandas sort_values().head(3) (compared in output order: revenue desc, customer_id asc)")
print(sql_df.to_string(index=False))

# Without a tie-breaker: customers 3 and 4 both have 500 and only one fits
loose = q("""SELECT customer_id, SUM(amount) AS revenue FROM orders WHERE status = 'completed'
GROUP BY customer_id ORDER BY revenue DESC LIMIT 3""")
print("\nORDER BY revenue DESC LIMIT 3 (no tie-breaker):", loose.values.tolist(), "<- which of 3 and 4 appears is not promised")
print("ORDER BY revenue DESC, customer_id DESC LIMIT 3:",
      q("""SELECT customer_id, SUM(amount) AS revenue FROM orders WHERE status = 'completed'
GROUP BY customer_id ORDER BY revenue DESC, customer_id DESC LIMIT 3""").values.tolist(), "<- explicit rule: higher customer_id wins the tie")

# LIMIT without ORDER BY: SQLite happens to return group-key order here; that is an accident of the plan, not a promise
print("LIMIT 3 with no ORDER BY at all:", q("SELECT customer_id, SUM(amount) AS revenue FROM orders WHERE status = 'completed' GROUP BY customer_id LIMIT 3").values.tolist())

# Keep ties: include everybody who equals the 3rd value (SQLite has no WITH TIES, so use the 3rd value as a threshold)
SQL_TIES = """
WITH t AS (SELECT customer_id, SUM(amount) AS revenue FROM orders WHERE status = 'completed' GROUP BY customer_id)
SELECT customer_id, revenue FROM t
WHERE revenue >= (SELECT revenue FROM t ORDER BY revenue DESC LIMIT 1 OFFSET 2)
ORDER BY revenue DESC, customer_id
"""
ties = q(SQL_TIES)

# --- pandas nlargest and keep
by_first = rev.nlargest(3, "revenue", keep="first")["customer_id"].tolist()
by_last = rev.nlargest(3, "revenue", keep="last")["customer_id"].tolist()
by_all = rev.nlargest(3, "revenue", keep="all").sort_values(["revenue", "customer_id"], ascending=[False, True]).reset_index(drop=True)
# --- end pandas
print("\nnlargest keep='first':", by_first, "| keep='last':", by_last)
print("nlargest keep='all':", by_all.values.tolist())
pd.testing.assert_frame_equal(ties, by_all)
print("tie-inclusive SQL (threshold form) == nlargest(keep='all'):", ties.values.tolist())
assert len(ties) == 4 and by_first == [1, 2, 3] and by_last == [1, 2, 4]
```
**Output (my run):**
```text
top 3 with tie-breaker: SQL == pandas sort_values().head(3) (compared in output order: revenue desc, customer_id asc)
 customer_id  revenue
           1      900
           2      800
           3      500

ORDER BY revenue DESC LIMIT 3 (no tie-breaker): [[1, 900], [2, 800], [4, 500]] <- which of 3 and 4 appears is not promised
ORDER BY revenue DESC, customer_id DESC LIMIT 3: [[1, 900], [2, 800], [4, 500]] <- explicit rule: higher customer_id wins the tie
LIMIT 3 with no ORDER BY at all: [[1, 900], [2, 800], [3, 500]]

nlargest keep='first': [1, 2, 3] | keep='last': [1, 2, 4]
nlargest keep='all': [[1, 900], [2, 800], [3, 500], [4, 500]]
tie-inclusive SQL (threshold form) == nlargest(keep='all'): [[1, 900], [2, 800], [3, 500], [4, 500]]
```

**Edge cases:**
- **Ties at the cut-off (honest result):** with only `ORDER BY revenue DESC LIMIT 3` SQLite returned customer 4, not 3, in my run (the output shows it); with `customer_id ASC` as the tie-breaker you always get 3. The plain version is not wrong in SQLite, it is unspecified, and other engines or versions can pick the other one.
- **LIMIT without ORDER BY:** returns some rows, with no guarantee about which or in what order; in my run it happened to give 1, 2, 3 (group-key order), which is a plan accident. Never rely on it for "first" or "top".
- **Keep all ties:** if the business wants everyone tied for third, the answer has four rows. Standard `FETCH FIRST 3 ROWS WITH TIES` does it where supported (PostgreSQL 13 and later, Oracle 12c and later, as I recall; SQL Server `TOP 3 WITH TIES`; not executed here). The threshold query above is the SQLite way and matched pandas `nlargest(keep="all")`.
- **pandas nlargest keep:** `keep="first"` returned customers 1, 2, 3, `keep="last"` returned 1, 2, 4, and `keep="all"` returned four rows. The default is `"first"`, which depends on row order in the frame, so it is also unspecified unless you sort first.
- **Fewer than 3 customers:** LIMIT 3 simply returns what exists.
- **NULL revenue:** SUM ignores NULL amounts; a customer whose completed amounts are all NULL has a NULL total, and NULLs sort first in SQLite ascending and last descending, so check where they land (Q14).
- **Dialect syntax (hedged, from memory, not executed here):** SQL Server and Access use `SELECT TOP 3 ...`; Oracle 12c+, PostgreSQL 13+ and recent DB2 accept the standard `FETCH FIRST 3 ROWS ONLY` (with optional `OFFSET`); MySQL, PostgreSQL, SQLite and BigQuery accept `LIMIT 3`.

**Then explain:**
- **Top-N pattern:** aggregate, sort descending, limit.
- **Determinism:** a sort key that is not unique leaves rows with equal keys in any order, so add a unique tie-breaker (customer_id).
- **LIMIT without ORDER BY:** a set has no order; the engine returns whichever rows its plan produces first.
- **pandas:** `sort_values(..., ascending=[False, True]).head(3)` gives a deterministic answer (and `sort_values` has `kind="stable"` for ties); `nlargest` is a shortcut with its own `keep` rule for ties.
- **Why a tie matters in an interview:** ask "what should happen on a tie?" before coding; it shows you noticed.

**Follow-ups:**
- *What if "top 3" should include ties?* Use WITH TIES where available, or a threshold subquery, or RANK in Part 4.
- *Top 3 per region?* That is a top-N per group, which needs window functions (Part 4).
- *Is `ORDER BY 2 DESC` OK?* Works, but is fragile (Q23).

**Common mistakes:**
- Forgetting the status filter before aggregating.
- No tie-breaker, so the answer changes between runs or engines.
- Using LIMIT without ORDER BY.
- Using `nlargest` and not checking `keep`.
- Putting LIMIT inside a subquery where it silently changes what is aggregated.

### Q13 ⭐⭐⭐ 🟡 NOT IN with NULL: customers(customer_id, name) and orders(order_id, customer_id) where orders.customer_id can be NULL for guest checkouts. Write 'customers who have never ordered' with NOT IN and show it returns zero rows when the subquery contains a NULL; explain it with three-valued logic and fix it with NOT EXISTS or a NOT NULL filter in the subquery. (Subqueries are Part 3 and anti-joins Part 2; the point here is the NULL trap.) Show the pandas ~isin result, and what pandas does with NaN in isin.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** `NOT IN` returns zero rows as soon as the subquery contains one NULL, because `x NOT IN (1, 2, NULL)` can never be TRUE; use `NOT EXISTS`, or filter the NULLs out of the subquery.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);  -- NULL = guest checkout
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,2),(104,NULL);
```

**SQL answer:** three queries are in the Code block: `sql_not_in` (the trap), `sql_not_in_filtered` (NOT NULL filter inside the subquery) and `sql_not_exists` (the safe default).

**pandas answer:** `customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"]`, shown in the Code block as `p_not_in`.

**Example:** Customers 1 to 4, orders belong to customers 1, 1, 2 and one guest (NULL). The real answer is Chitra (3) and Dev (4). For customer 3 the predicate is `NOT (3 = 1 OR 3 = 2 OR 3 = NULL)`. That is `NOT (FALSE OR FALSE OR UNKNOWN)`, which is `NOT UNKNOWN`, which is UNKNOWN. `WHERE` keeps only TRUE, so Chitra is dropped. Customer 4 is the same. Customers 1 and 2 give FALSE. No row can ever be TRUE, so the result is empty.

**Code:** run with `python3 -I`.
```python
# NOT IN with a NULL in the subquery: SQL result, the fixes, and what pandas isin does with NaN.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);  -- NULL = guest checkout
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,2),(104,NULL);
""")

sql_not_in = "SELECT name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders) ORDER BY customer_id"
sql_not_in_filtered = ("SELECT name FROM customers WHERE customer_id NOT IN "
                       "(SELECT customer_id FROM orders WHERE customer_id IS NOT NULL) ORDER BY customer_id")
sql_not_exists = ("SELECT c.name FROM customers c WHERE NOT EXISTS "
                  "(SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id) ORDER BY c.customer_id")

def run(q): return [r[0] for r in con.execute(q).fetchall()]
print("NOT IN (subquery has a NULL):", run(sql_not_in))
print("NOT IN with IS NOT NULL filter:", run(sql_not_in_filtered))
print("NOT EXISTS:", run(sql_not_exists))
print("3 NOT IN (1, 2, NULL) ->", con.execute("SELECT 3 NOT IN (1,2,NULL)").fetchone()[0])
print("1 NOT IN (1, 2, NULL) ->", con.execute("SELECT 1 NOT IN (1,2,NULL)").fetchone()[0])
print("3 NOT IN (1, 2)       ->", con.execute("SELECT 3 NOT IN (1,2)").fetchone()[0])

# pandas
customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con)
print("orders.customer_id dtype:", orders["customer_id"].dtype, "(NULL became NaN, ints became float)")
p_not_in = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].tolist()
print("pandas ~isin:", p_not_in)

# isin and NaN: NaN matches NaN, so a NaN key on the left WOULD be treated as 'found'
left = pd.Series([1.0, 3.0, np.nan])
print("isin with NaN in values:", left.isin([1.0, np.nan]).tolist())

# the pandas result matches the NOT EXISTS result (compare as lists, ordered by customer_id)
assert p_not_in == run(sql_not_exists) == run(sql_not_in_filtered) == ["Chitra", "Dev"]
assert run(sql_not_in) == []

# NOT IN with NULL filtered out explicitly in pandas gives the same thing
ids = orders["customer_id"].dropna()
assert customers.loc[~customers["customer_id"].isin(ids), "name"].tolist() == p_not_in
print("asserts passed")
```

**Output (my run):**
```text
NOT IN (subquery has a NULL): []
NOT IN with IS NOT NULL filter: ['Chitra', 'Dev']
NOT EXISTS: ['Chitra', 'Dev']
3 NOT IN (1, 2, NULL) -> None
1 NOT IN (1, 2, NULL) -> 0
3 NOT IN (1, 2)       -> 1
orders.customer_id dtype: float64 (NULL became NaN, ints became float)
pandas ~isin: ['Chitra', 'Dev']
isin with NaN in values: [True, False, True]
asserts passed
```

**Edge cases:**
- The NULL only has to appear once, and it only matters in a `NOT IN` (or `<> ALL`). A positive `IN` still works: `1 IN (1, 2, NULL)` is TRUE, while `3 IN (1, 2, NULL)` is UNKNOWN (not TRUE, so the row is not returned, which happens to be the answer you wanted).
- If the subquery returns no rows at all, `NOT IN` returns every customer.
- If the left-hand value is itself NULL, `NULL NOT IN (...)` is UNKNOWN for any non-empty list, so that row is also dropped.
- Duplicates in the subquery do not matter.

**Then explain:**
- **Three-valued logic:** comparisons with NULL give UNKNOWN, not FALSE. `NOT UNKNOWN` is UNKNOWN. `WHERE` keeps only TRUE.
- **Why NOT EXISTS is safe:** the correlated test `o.customer_id = c.customer_id` is UNKNOWN for the guest row, `EXISTS` just sees "no matching row", and `NOT EXISTS` returns TRUE.
- **Alternatives:** filter the subquery with `WHERE customer_id IS NOT NULL`, or use a LEFT JOIN ... IS NULL anti-join (Part 2). I recommend `NOT EXISTS` because it does not break when someone later adds NULLs.
- **pandas differs from SQL here:** the SQL query returns nothing, but `~isin` returns Chitra and Dev. `isin` is a plain membership test with no UNKNOWN. In my run the NULL became NaN and the key column became `float64`; that matters only for display, the comparison still works.
- **NaN in isin:** `isin` treats NaN as equal to NaN (`[1.0, 3.0, NaN].isin([1.0, NaN])` gave `[True, False, True]`). So if the left side contains NaN and the list also has NaN, the row counts as "found", the opposite of SQL, where NULL never matches.
- All SQL engines I know follow this standard rule, but I only ran SQLite here (not executed on Postgres, MySQL, BigQuery or Snowflake).

**Follow-ups:**
- *Does `x IN (..., NULL)` have the same problem?* No: it can be TRUE; you only lose the UNKNOWN cases, which were not matches anyway.
- *Why not just use a LEFT JOIN?* That works too (Part 2), and it is NULL-safe if you test a non-null column of the right table.
- *How do you make pandas behave like SQL?* Drop NaN from the keys explicitly and decide what NaN on the left should do; do not rely on `isin` to guess.

**Common mistakes:**
- Blaming the data ("there are no customers without orders") instead of the NULL.
- Fixing it with `COALESCE(customer_id, 0)`, which invents a customer 0.
- Believing `NOT IN` and `NOT EXISTS` are always interchangeable.
- Reading a `float64` key column in pandas as a data problem and casting it away without handling the NaN first.

### Q14 ⭐⭐⭐ 🟡 ORDER BY with NULLs and ties: employees(emp_id, name, dept, salary) where salary can be NULL. Where do NULLs sort in ascending and descending order in PostgreSQL, MySQL, SQLite, SQL Server and Oracle (state as hedged dialect behaviour; check the engine docs) and how do you force NULLS LAST portably with a CASE or an IS NULL sort key? Explain multi-column ORDER BY, sorting by an expression or ordinal, and why ties make output order non-deterministic. Show pandas sort_values with na_position and a stable sort.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** There is no portable default for where NULLs sort (SQLite and, from memory, MySQL and SQL Server treat NULL as smallest, PostgreSQL and, from memory, Oracle as largest), so when it matters I write the NULL position explicitly with `NULLS LAST` where supported or a `CASE WHEN x IS NULL` sort key where not, and I always add a unique tie-breaker column.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha','Eng',90),(2,'Ben','Eng',NULL),(3,'Chitra','Ops',70),
 (4,'Dev','Ops',90),(5,'Esha','Eng',70),(6,'Farid','Ops',NULL),(7,'Gita','Eng',90);
```

**SQL answer:** all queries are in the Code block: plain `ORDER BY salary` (ASC and DESC), `NULLS LAST` / `NULLS FIRST`, the portable `sql_portable` with a CASE key, `sql_multi` for a multi-column sort, an ordinal sort and an expression sort.

**pandas answer:** `df.sort_values(["salary", "emp_id"], ascending=[False, True], na_position="last")`, plus `kind="stable"` for a stable sort; all variants are in the Code block.

**Dialect behaviour of NULL ordering:**

| Engine | NULLs in ASC | NULLs in DESC | NULLS FIRST/LAST keyword | Status |
|---|---|---|---|---|
| SQLite 3.45 | first | last | yes (since 3.30, ran it) | executed here |
| PostgreSQL | last | first | yes | PostgreSQL docs page opened: NULLs sort as if larger |
| MySQL | first | last | no (use a sort key) | from memory, not opened or executed |
| SQL Server | first | last | no (use a sort key) | from memory, not opened or executed |
| Oracle | last | first | yes | from memory, not opened or executed |

Check the engine docs before relying on the last three rows.

**Example:** salaries are Asha 90, Ben NULL, Chitra 70, Dev 90, Esha 70, Farid NULL, Gita 90. `ORDER BY salary, emp_id` in SQLite gives the NULLs first: Ben (2), Farid (6), then the 70s (3, 5), then the 90s (1, 4, 7). `ORDER BY salary DESC, emp_id` gives 1, 4, 7, 3, 5, 2, 6, so NULLs fall to the bottom. The portable `CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary DESC, emp_id` gives the same list `[1, 4, 7, 3, 5, 2, 6]` on every engine, because the CASE key is a plain 0/1 number that sorts the same everywhere.

**Code:** run with `python3 -I`.
```python
# ORDER BY with NULLs and ties: SQLite behaviour, portable NULLS LAST, multi-column, ordinal, ties, pandas.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha','Eng',90),(2,'Ben','Eng',NULL),(3,'Chitra','Ops',70),
 (4,'Dev','Ops',90),(5,'Esha','Eng',70),(6,'Farid','Ops',NULL),(7,'Gita','Eng',90);
""")

def ids(q): return [r[0] for r in con.execute(q).fetchall()]

asc = ids("SELECT emp_id FROM employees ORDER BY salary, emp_id")
desc = ids("SELECT emp_id FROM employees ORDER BY salary DESC, emp_id")
print("SQLite ASC  (salary, emp_id):", asc)
print("SQLite DESC (salary DESC, emp_id):", desc)

nl_asc = ids("SELECT emp_id FROM employees ORDER BY salary NULLS LAST, emp_id")
nl_desc = ids("SELECT emp_id FROM employees ORDER BY salary DESC NULLS FIRST, emp_id")
print("NULLS LAST asc:", nl_asc, "| DESC NULLS FIRST:", nl_desc)

# Portable NULLS LAST: a CASE sort key (works where NULLS LAST is not supported)
sql_portable = """SELECT emp_id FROM employees
ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary DESC, emp_id"""
portable = ids(sql_portable)
print("portable, salary DESC NULLS LAST, tie-break emp_id:", portable)

# multi-column + expression + ordinal
sql_multi = "SELECT emp_id, dept, salary FROM employees ORDER BY dept ASC, salary DESC, emp_id ASC"
print("dept ASC, salary DESC, emp_id ASC (NULL salary is last within each dept):")
print(con.execute(sql_multi).fetchall())
print("ordinal ORDER BY 2, 1:", con.execute("SELECT emp_id, dept FROM employees ORDER BY 2, 1").fetchall())
print("expression ORDER BY -salary (NULL stays NULL):", ids("SELECT emp_id FROM employees ORDER BY -salary, emp_id"))

# ties without tie-breaker: only salary key. Order among equals is up to the engine
print("ties, no tie-breaker (engine's choice, not a guarantee):", ids("SELECT emp_id FROM employees ORDER BY salary DESC"))

# pandas
df = pd.read_sql("SELECT * FROM employees", con)
p_asc = df.sort_values(["salary", "emp_id"])["emp_id"].tolist()                      # na_position='last' is the default
p_asc_first = df.sort_values(["salary", "emp_id"], na_position="first")["emp_id"].tolist()
p_desc = df.sort_values(["salary", "emp_id"], ascending=[False, True])["emp_id"].tolist()
p_desc_first = df.sort_values(["salary", "emp_id"], ascending=[False, True], na_position="first")["emp_id"].tolist()
print("pandas default asc (NaN last):", p_asc)
print("pandas asc na_position='first' (matches SQLite ASC):", p_asc_first)
print("pandas desc default (NaN last, matches SQLite DESC):", p_desc)
print("pandas desc na_position='first':", p_desc_first)

# stable sort: sort by salary only with kind='stable' keeps original row order among ties
st = df.sort_values("salary", ascending=False, kind="stable")["emp_id"].tolist()
print("pandas stable desc, salary only:", st)
st2 = df.sort_values("salary", kind="stable").sort_values("dept", kind="stable")["emp_id"].tolist()
print("two stable passes (salary then dept):", st2)

assert asc == p_asc_first                    # SQLite puts NULL first in ASC
assert desc == p_desc                        # SQLite puts NULL last in DESC
assert nl_asc == p_asc and nl_desc == p_desc_first
assert portable == df.sort_values(["salary", "emp_id"], ascending=[False, True])["emp_id"].tolist()
p_multi = df.sort_values(["dept", "salary", "emp_id"], ascending=[True, False, True])[["emp_id", "dept", "salary"]]
sql_multi_rows = con.execute(sql_multi).fetchall()
assert [(a, b, None if pd.isna(c) else int(c)) for a, b, c in p_multi.itertuples(index=False)] == sql_multi_rows
print("asserts passed")
```

**Output (my run):**
```text
SQLite ASC  (salary, emp_id): [2, 6, 3, 5, 1, 4, 7]
SQLite DESC (salary DESC, emp_id): [1, 4, 7, 3, 5, 2, 6]
NULLS LAST asc: [3, 5, 1, 4, 7, 2, 6] | DESC NULLS FIRST: [2, 6, 1, 4, 7, 3, 5]
portable, salary DESC NULLS LAST, tie-break emp_id: [1, 4, 7, 3, 5, 2, 6]
dept ASC, salary DESC, emp_id ASC (NULL salary is last within each dept):
[(1, 'Eng', 90), (7, 'Eng', 90), (5, 'Eng', 70), (2, 'Eng', None), (4, 'Ops', 90), (3, 'Ops', 70), (6, 'Ops', None)]
ordinal ORDER BY 2, 1: [(1, 'Eng'), (2, 'Eng'), (5, 'Eng'), (7, 'Eng'), (3, 'Ops'), (4, 'Ops'), (6, 'Ops')]
expression ORDER BY -salary (NULL stays NULL): [2, 6, 1, 4, 7, 3, 5]
ties, no tie-breaker (engine's choice, not a guarantee): [1, 4, 7, 3, 5, 2, 6]
pandas default asc (NaN last): [3, 5, 1, 4, 7, 2, 6]
pandas asc na_position='first' (matches SQLite ASC): [2, 6, 3, 5, 1, 4, 7]
pandas desc default (NaN last, matches SQLite DESC): [1, 4, 7, 3, 5, 2, 6]
pandas desc na_position='first': [2, 6, 1, 4, 7, 3, 5]
pandas stable desc, salary only: [1, 4, 7, 3, 5, 2, 6]
two stable passes (salary then dept): [5, 1, 7, 2, 3, 4, 6]
asserts passed
```

**Edge cases:**
- Ties: the 90s are tied three ways. Without the `emp_id` tie-breaker the SQL standard allows any order among them; my SQLite run happened to give 1, 4, 7, which is no guarantee on another engine or after the table grows.
- Multi-column: later keys only break ties of earlier keys, each with its own direction.
- An expression such as `-salary` keeps NULL as NULL, so NULL placement still follows the engine's rule.
- Ordinals (`ORDER BY 2, 1`) work in the engines I know but break when the SELECT list changes (Q23).
- pandas default: `na_position="last"` in both directions. So the pandas default matches SQLite for DESC but not for ASC. I had to pass `na_position="first"` to match SQLite's ASC.

**Then explain:**
- **Force NULLS LAST portably:** `ORDER BY CASE WHEN salary IS NULL THEN 1 ELSE 0 END, salary DESC`. In several engines you can sort on the boolean `salary IS NULL` directly, but a CASE is the most portable (Oracle has no boolean type, from memory).
- **Multi-column:** `ORDER BY dept ASC, salary DESC, emp_id ASC`; the first key is the major sort.
- **Expression or ordinal:** you can sort on any expression; ordinal positions are legal but fragile.
- **Ties are not stable:** a stable sort is a pandas feature you opt into (`kind="stable"`); SQL gives no such promise, so make the order total with a unique key.
- **pandas:** `kind="stable"` keeps the original row order among equal keys; in my run `sort_values("salary", ascending=False, kind="stable")` gave 1, 4, 7, 3, 5, 2, 6, ties in original row order. Two stable passes (minor key first) also give a multi-key sort.

**Follow-ups:**
- *How does `DISTINCT` or `GROUP BY` order output?* Not at all; add `ORDER BY` if you need an order.
- *What does `ORDER BY salary DESC LIMIT 1` return with a NULL top?* Depends on the engine's default; with NULLs-first-in-DESC (PostgreSQL) the NULL row wins, which is a classic "highest salary" bug.
- *How do you sort a mixed column of text numbers?* Cast to a number in the sort key (Part 10 has string traps).

**Common mistakes:**
- Assuming NULLs sort the same way in every database.
- No tie-breaker, then a flaky test or flaky pagination.
- Using `salary IS NULL` as a sort key and forgetting that FALSE (0) sorts before TRUE (1) in ASC.
- Using `na_position` and expecting it to apply to the SQL engine.

### Q15 ⭐⭐⭐ 🟡 Translate SQL to pandas. SQL: SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_sal FROM employees WHERE salary IS NOT NULL AND hired >= '2020-01-01' GROUP BY dept HAVING COUNT(*) >= 3 ORDER BY avg_sal DESC LIMIT 5, on employees(emp_id, name, dept, salary, hired). Write the pandas with boolean masks, groupby with named aggregation, query() and sort_values().head(5); explain as_index, reset_index, and how to assert the two results match (same rows, order, dtypes).
**Asked at:** pandas documentation (Comparison with SQL) and prep guides, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `WHERE` becomes a boolean mask, `GROUP BY ... COUNT/AVG` becomes `groupby().agg(n=..., avg_sal=...)` with named aggregation, `HAVING` becomes a second filter (`query` or a mask) on the aggregated frame, and `ORDER BY ... LIMIT` becomes `sort_values().head()`.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER, hired TEXT);
INSERT INTO employees VALUES
 (1,'a1','Eng',100,'2021-03-01'),(2,'a2','Eng',140,'2022-05-10'),(3,'a3','Eng',120,'2020-01-01'),(4,'a4','Eng',NULL,'2023-01-01'),(5,'a5','Eng',500,'2019-12-31'),
 (6,'b1','Ops',60,'2020-06-01'),(7,'b2','Ops',80,'2021-01-01'),(8,'b3','Ops',70,'2024-02-02'),
 (9,'c1','HR',50,'2020-02-02'),(10,'c2','HR',55,'2022-02-02'),(11,'c3','HR',45,'2023-03-03'),(12,'c4','HR',90,'2018-01-01'),
 (13,'d1','Fin',200,'2021-01-01'),(14,'d2','Fin',210,'2021-02-01'),(15,'d3','Fin',190,'2021-03-01'),
 (16,'e1','Mkt',75,'2022-01-01'),(17,'e2','Mkt',85,'2022-02-01'),(18,'e3','Mkt',95,'2022-03-01'),
 (19,'f1','Sales',65,'2020-01-01'),(20,'f2','Sales',66,'2020-02-01'),(21,'f3','Sales',67,'2020-03-01'),
 (22,'g1','Legal',300,'2021-01-01'),(23,'g2','Legal',310,'2021-02-01');
```

**SQL answer:** the query is the string `sql` in the Code block, verbatim from the question.

**pandas answer:** `v1` (masks, named aggregation, `query`, `sort_values`, `head(5)`) and `v2` (`query()` for the row filter, then `reset_index()`) in the Code block.

**Example:** after `WHERE salary IS NOT NULL AND hired >= '2020-01-01'`, Eng keeps ids 1, 2, 3 (id 4 has a NULL salary, id 5 was hired in 2019): n = 3, average of 100, 140, 120 = 120. Ops keeps 60, 80, 70: n = 3, avg 70. HR keeps 50, 55, 45 (id 12 hired 2018): n = 3, avg 50. Fin avg 200, Mkt 85, Sales 66, all with n = 3. Legal has only 2 rows, so `HAVING COUNT(*) >= 3` removes it. Six departments pass; sorted by average descending they are Fin 200, Eng 120, Mkt 85, Ops 70, Sales 66, HR 50, and `LIMIT 5` drops HR.

**Code:** run with `python3 -I`.
```python
# Translate SQL to pandas (Q15) and assert the two results are identical (rows, order, dtypes).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER, hired TEXT);
INSERT INTO employees VALUES
 (1,'a1','Eng',100,'2021-03-01'),(2,'a2','Eng',140,'2022-05-10'),(3,'a3','Eng',120,'2020-01-01'),(4,'a4','Eng',NULL,'2023-01-01'),(5,'a5','Eng',500,'2019-12-31'),
 (6,'b1','Ops',60,'2020-06-01'),(7,'b2','Ops',80,'2021-01-01'),(8,'b3','Ops',70,'2024-02-02'),
 (9,'c1','HR',50,'2020-02-02'),(10,'c2','HR',55,'2022-02-02'),(11,'c3','HR',45,'2023-03-03'),(12,'c4','HR',90,'2018-01-01'),
 (13,'d1','Fin',200,'2021-01-01'),(14,'d2','Fin',210,'2021-02-01'),(15,'d3','Fin',190,'2021-03-01'),
 (16,'e1','Mkt',75,'2022-01-01'),(17,'e2','Mkt',85,'2022-02-01'),(18,'e3','Mkt',95,'2022-03-01'),
 (19,'f1','Sales',65,'2020-01-01'),(20,'f2','Sales',66,'2020-02-01'),(21,'f3','Sales',67,'2020-03-01'),
 (22,'g1','Legal',300,'2021-01-01'),(23,'g2','Legal',310,'2021-02-01');
""")

sql = """
SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_sal
FROM employees
WHERE salary IS NOT NULL AND hired >= '2020-01-01'
GROUP BY dept
HAVING COUNT(*) >= 3
ORDER BY avg_sal DESC
LIMIT 5
"""
sql_df = pd.read_sql(sql, con)
print(sql_df.to_string(index=False))

emp = pd.read_sql("SELECT * FROM employees", con)

# version 1: boolean masks + named aggregation
mask = emp["salary"].notna() & (emp["hired"] >= "2020-01-01")
v1 = (emp[mask]
      .groupby("dept", as_index=False)
      .agg(n=("emp_id", "size"), avg_sal=("salary", "mean"))
      .query("n >= 3")
      .sort_values("avg_sal", ascending=False)
      .head(5)
      .reset_index(drop=True))

# version 2: query() for the row filter, as_index=True then reset_index
v2 = (emp.query("salary.notna() and hired >= '2020-01-01'")
         .groupby("dept")
         .agg(n=("emp_id", "size"), avg_sal=("salary", "mean"))
         .query("n >= 3")
         .sort_values("avg_sal", ascending=False)
         .head(5)
         .reset_index())
print(v1.dtypes.to_dict())
print(sql_df.dtypes.to_dict())

pd.testing.assert_frame_equal(sql_df, v1)
pd.testing.assert_frame_equal(sql_df, v2)
print("asserts passed: SQL == v1 == v2 (same rows, same order, same dtypes; no ties in avg_sal here)")

# what as_index=True does if you forget reset_index
g = emp[mask].groupby("dept").agg(n=("emp_id", "size"))
print("as_index=True: dept is the index ->", g.index.name, "| columns:", list(g.columns))

# how many rows got there before the limit
print("depts passing HAVING before LIMIT 5:", len(emp[mask].groupby("dept").filter(lambda x: len(x) >= 3)["dept"].unique()))
```

**Output (my run):**
```text
 dept  n  avg_sal
  Fin  3    200.0
  Eng  3    120.0
  Mkt  3     85.0
  Ops  3     70.0
Sales  3     66.0
{'dept': <StringDtype(storage='python', na_value=nan)>, 'n': dtype('int64'), 'avg_sal': dtype('float64')}
{'dept': <StringDtype(storage='python', na_value=nan)>, 'n': dtype('int64'), 'avg_sal': dtype('float64')}
asserts passed: SQL == v1 == v2 (same rows, same order, same dtypes; no ties in avg_sal here)
as_index=True: dept is the index -> dept | columns: ['n']
depts passing HAVING before LIMIT 5: 6
```

**Edge cases:**
- Ties in `avg_sal` at the 5th/6th place make `LIMIT 5` ambiguous in both SQL and pandas; add a tie-breaker (`ORDER BY avg_sal DESC, dept`; in pandas `sort_values(["avg_sal", "dept"], ascending=[False, True])`). Not needed in this data.
- `COUNT(*)` after the WHERE counts rows (`size`); `COUNT(salary)` would be `count` (here identical, because the mask removes the NULLs).
- A department with zero surviving rows simply does not appear in either version.
- `hired` is text in ISO format, so string comparison works. With real dates in pandas I would `pd.to_datetime` first.

**Then explain:**
- **Order of work is identical:** filter rows, group, aggregate, filter groups, sort, cut.
- **`as_index`:** `groupby("dept")` makes `dept` the index of the result (my run printed `dept` as the index name); `as_index=False` or `reset_index()` puts it back as a column so it matches the SQL frame.
- **Named aggregation:** `agg(n=("emp_id", "size"), avg_sal=("salary", "mean"))` names output columns like SQL aliases.
- **Why HAVING is `query("n >= 3")`:** it runs after aggregation, on the grouped frame, just like HAVING.
- **How to assert a match:** `pd.testing.assert_frame_equal(sql_df, v1)` checks rows, order, column names and dtypes (here `n` is `int64`, `avg_sal` is `float64`, `dept` is pandas' string dtype on both sides). It passed for both versions. For queries without a total order, sort both sides on all columns first.

**Follow-ups:**
- *`size` vs `count`?* `size` counts rows (SQL `COUNT(*)`), `count` counts non-null values of a column (SQL `COUNT(col)`).
- *How would you do it in one chain?* The chain in `v1` is one expression; use `.pipe` if you need to reuse a step.
- *Why is HAVING not just WHERE?* WHERE runs before grouping and cannot see aggregates; HAVING runs after.

**Common mistakes:**
- Forgetting `reset_index` and then trying to use `dept` as a column.
- Putting the `n >= 3` filter before the groupby (that filters rows, not groups).
- Comparing frames by eye instead of asserting dtypes and order.
- Using `count` where SQL used `COUNT(*)`.

### Q16 ⭐⭐⭐ 🟡 SQL vs pandas NULL differences in grouping and aggregation. Given orders(order_id, region, amount) where region and amount have NULLs, show what SQL GROUP BY region returns (NULLs form one group) versus pandas groupby('region') (NaN keys dropped unless dropna=False), SUM of an all-NULL group (NULL in SQL, 0 in pandas unless min_count=1), AVG vs mean skipping missing values, COUNT(col) vs count(), and how to make pandas match SQL.
**Asked at:** pandas documentation (Comparison with SQL) and prep guides, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** SQL and pandas disagree by default on four things: SQL keeps a NULL group, pandas drops NaN keys; SQL `SUM` of only NULLs is NULL, pandas gives 0; `COUNT(col)` and `count()` agree (both skip missing values) but `COUNT(*)` is `size()`; and both `AVG` and `mean` skip missing values. Pass `dropna=False` and `min_count=1` to make pandas match.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'North',100),(2,'North',NULL),(3,'North',50),
 (4,'South',NULL),(5,'South',NULL),
 (6,NULL,30),(7,NULL,NULL),(8,'East',20);
```

**SQL answer:** the query is `sql` in the Code block (`COUNT(*)`, `COUNT(amount)`, `SUM`, `AVG` per region, NULL region ordered last by `ORDER BY region IS NULL, region`).

**pandas answer:** `matched` in the Code block: `groupby("region", dropna=False)` with `size`, `count`, a `sum(min_count=1)` lambda and `mean`.

**Example:** North has amounts 100, NULL, 50: 3 rows, 2 non-null amounts, sum 150, average 75 (the NULL is skipped, so it is 150/2, not 150/3). South has 2 rows and no amount at all: `SUM` is NULL, `AVG` is NULL, `COUNT(amount)` is 0. The NULL-region rows (orders 6 and 7) form one group: 2 rows, 1 amount, sum 30. East is 20.

**Code:** run with `python3 -I`.
```python
# SQL vs pandas NULL differences in GROUP BY and aggregates (Q16).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'North',100),(2,'North',NULL),(3,'North',50),
 (4,'South',NULL),(5,'South',NULL),
 (6,NULL,30),(7,NULL,NULL),(8,'East',20);
""")

sql = """
SELECT region,
       COUNT(*)      AS n_rows,
       COUNT(amount) AS n_amount,
       SUM(amount)   AS total,
       AVG(amount)   AS avg_amt
FROM orders
GROUP BY region
ORDER BY region IS NULL, region
"""
sql_df = pd.read_sql(sql, con)
print("SQL:"); print(sql_df.to_string(index=False))

orders = pd.read_sql("SELECT * FROM orders", con)

# default pandas: NaN keys dropped, SUM of nothing = 0
naive = orders.groupby("region").agg(n_rows=("order_id", "size"), n_amount=("amount", "count"),
                                     total=("amount", "sum"), avg_amt=("amount", "mean"))
print("\npandas defaults (dropna=True, sum without min_count):"); print(naive)

# matched to SQL: keep the NaN group, min_count=1 so an all-NaN group sums to NaN
matched = (orders.groupby("region", dropna=False)
           .agg(n_rows=("order_id", "size"), n_amount=("amount", "count"),
                total=("amount", lambda s: s.sum(min_count=1)), avg_amt=("amount", "mean"))
           .reset_index()
           .sort_values("region", na_position="last")
           .reset_index(drop=True))
print("\npandas matched to SQL:"); print(matched.to_string(index=False))

# compare: NULL/NaN treated as equal, int columns as int64
pd.testing.assert_frame_equal(sql_df, matched, check_dtype=True)
print("\nasserts passed: SQL == matched pandas (rows ordered by region, NULL region last)")

# whole-table behaviour: all-NULL column
empty_like = orders[orders["region"] == "South"]["amount"]
print("pandas sum of all-NaN:", empty_like.sum(), "| with min_count=1:", empty_like.sum(min_count=1))
print("SQL SUM of all-NULL group:", con.execute("SELECT SUM(amount) FROM orders WHERE region='South'").fetchone()[0],
      "| TOTAL():", con.execute("SELECT TOTAL(amount) FROM orders WHERE region='South'").fetchone()[0],
      "| AVG:", con.execute("SELECT AVG(amount) FROM orders WHERE region='South'").fetchone()[0])
print("pandas mean of all-NaN:", empty_like.mean())
```

**Output (my run):**
```text
SQL:
region  n_rows  n_amount  total  avg_amt
  East       1         1   20.0     20.0
 North       3         2  150.0     75.0
 South       2         0    NaN      NaN
   NaN       2         1   30.0     30.0

pandas defaults (dropna=True, sum without min_count):
        n_rows  n_amount  total  avg_amt
region                                  
East         1         1   20.0     20.0
North        3         2  150.0     75.0
South        2         0    0.0      NaN

pandas matched to SQL:
region  n_rows  n_amount  total  avg_amt
  East       1         1   20.0     20.0
 North       3         2  150.0     75.0
 South       2         0    NaN      NaN
   NaN       2         1   30.0     30.0

asserts passed: SQL == matched pandas (rows ordered by region, NULL region last)
pandas sum of all-NaN: 0.0 | with min_count=1: nan
SQL SUM of all-NULL group: None | TOTAL(): 0.0 | AVG: None
pandas mean of all-NaN: nan
```

**Edge cases:**
- All-NULL group: SQL `SUM` gives NULL; SQLite's `TOTAL()` returns 0.0 (SQLite-specific, shown in the run). pandas `sum()` gave 0.0 and `sum(min_count=1)` gave NaN.
- `mean` of an all-NaN group is NaN in both.
- Default pandas dropped the NULL-region group entirely and the default result had 3 groups instead of 4.
- NULL and NaN are shown differently (`None` vs `NaN`), and `assert_frame_equal` treats them as equal missing values.
- The row-level `n_rows` (`size`) must come from a column that has no gaps (here `order_id`), or use `size()` directly.

**Then explain:**
- **Grouping:** SQL `GROUP BY` puts all NULLs into one group; pandas `groupby` drops them unless `dropna=False`.
- **Sum:** pandas treats the sum of nothing as 0; `min_count=1` says "need at least one non-missing value", giving NaN like SQL.
- **Avg/mean:** both skip missing values, so the denominator is the count of non-null values.
- **Counting:** `COUNT(*)` is `size()`; `COUNT(col)` is `count()`.
- **Sorting:** SQLite sorts NULL first in ASC; pandas `sort_values` puts NaN last by default, so I sorted with an explicit `na_position` before comparing.
- Dialect note: other engines follow the same standard rules for NULL groups and `SUM` (not executed here).

**Follow-ups:**
- *Why does pandas give 0 for an all-NaN sum?* It defines the empty sum as 0, the additive identity; SQL has no such rule. The behaviour shown is from my pandas 3.0.5 run.
- *How do you make SQL match pandas?* `COALESCE(SUM(amount), 0)`.
- *What does `groupby` do to NaN in the value column?* Skips it in `sum`, `mean`, `count`.

**Common mistakes:**
- Forgetting that pandas silently drops NaN-key rows, so totals no longer reconcile with SQL.
- Reporting 0 revenue for a group that has no data (should be NULL/"no data").
- Dividing by `size` instead of `count` for an average.

### Q17 ⭐⭐⭐ 🟡 Debugging: 'This query returns the wrong totals.' A teammate computes revenue per customer from orders(order_id, customer_id, amount, status) with SELECT customer_id, SUM(DISTINCT amount) ... and gets lower totals for some customers; another version filters status in HAVING and fails. Explain what SUM(DISTINCT) does, why two equal-amount orders vanish, when DISTINCT in an aggregate is legitimate, and give the corrected query plus a pandas check that exposes the bug.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** `SUM(DISTINCT amount)` adds each distinct amount once, so two orders of the same value count once and revenue is understated; the fix is plain `SUM(amount)` with the status filter in `WHERE`, and the status test belongs in `WHERE` (or inside a `CASE`), not `HAVING`.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT);
INSERT INTO orders VALUES
 (1,1,100,'completed'),(2,1,100,'completed'),(3,1,50,'cancelled'),
 (4,2,200,'completed'),(5,2,300,'completed'),
 (6,3,40,'completed'),(7,3,40,'refunded'),(8,3,40,'completed');
```

**SQL answer:** `fixed` (and the equivalent `fixed_case`) in the Code block. The buggy queries are `buggy` and `buggy_having`.

**pandas answer:** `distinct_all` (drop duplicates then sum) reproduces the bug, `true_all` (plain sum) is the right figure, and `completed` is the corrected pandas result, in the Code block.

**Premise correction:** the question says the HAVING version "fails". In SQLite it does not fail: it runs and silently returns the wrong thing (my run: totals of all statuses, 250, 500, 120, not the completed-only totals). A strict engine (PostgreSQL, and MySQL with `ONLY_FULL_GROUP_BY`, from memory, not executed) rejects it because `status` is neither grouped nor aggregated. In every engine, `HAVING` filters groups after aggregation, not rows before it.

**Example:** customer 1 has orders 100, 100 (completed) and 50 (cancelled). `SUM(DISTINCT amount)` = 100 + 50 = 150, but the real total is 250 (200 completed). Customer 3 has 40, 40, 40: DISTINCT gives 40 instead of 120 (80 completed). Customer 2 has two different amounts, so DISTINCT happens to be right (500), which is why the bug shows up only for "some customers".

**Code:** run with `python3 -I`.
```python
# Debugging SUM(DISTINCT amount) and HAVING on a non-aggregated column (Q17).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT);
INSERT INTO orders VALUES
 (1,1,100,'completed'),(2,1,100,'completed'),(3,1,50,'cancelled'),
 (4,2,200,'completed'),(5,2,300,'completed'),
 (6,3,40,'completed'),(7,3,40,'refunded'),(8,3,40,'completed');
""")

buggy = "SELECT customer_id, SUM(DISTINCT amount) AS revenue FROM orders GROUP BY customer_id ORDER BY customer_id"
buggy_having = ("SELECT customer_id, SUM(amount) AS revenue FROM orders GROUP BY customer_id "
                "HAVING status = 'completed' ORDER BY customer_id")
fixed = ("SELECT customer_id, SUM(amount) AS revenue FROM orders WHERE status = 'completed' "
         "GROUP BY customer_id ORDER BY customer_id")
fixed_case = ("SELECT customer_id, SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS revenue "
              "FROM orders GROUP BY customer_id ORDER BY customer_id")
fixed_all = "SELECT customer_id, SUM(amount) AS revenue FROM orders GROUP BY customer_id ORDER BY customer_id"

for name, q in [("buggy SUM(DISTINCT)", buggy), ("HAVING status (bare column)", buggy_having),
                ("fixed (WHERE before GROUP BY)", fixed), ("fixed (SUM(CASE ...))", fixed_case), ("SUM(amount), all statuses", fixed_all)]:
    print(name, con.execute(q).fetchall())

# pandas check that exposes the bug
orders = pd.read_sql("SELECT * FROM orders", con)
true_all = orders.groupby("customer_id")["amount"].sum()
distinct_all = orders.groupby("customer_id")["amount"].apply(lambda s: s.drop_duplicates().sum())
check = pd.DataFrame({"sum": true_all, "sum_distinct": distinct_all})
check["lost"] = check["sum"] - check["sum_distinct"]
print(check)
print("customers where DISTINCT lost money:", check.index[check["lost"] > 0].tolist())

completed = orders[orders["status"] == "completed"].groupby("customer_id", as_index=False)["amount"].sum()
completed = completed.rename(columns={"amount": "revenue"})
sql_fixed = pd.read_sql(fixed, con)
pd.testing.assert_frame_equal(sql_fixed, completed)
pd.testing.assert_frame_equal(pd.read_sql(fixed_case, con), completed)
# the buggy SQL equals the pandas drop_duplicates version (proves what DISTINCT does)
sql_buggy = pd.read_sql(buggy, con)
assert sql_buggy["revenue"].tolist() == distinct_all.tolist()
# the real totals differ from the buggy ones for customers 1 and 3
assert true_all.tolist() != distinct_all.tolist()

# legitimate DISTINCT: count distinct customers, not rows
print("legit: COUNT(DISTINCT customer_id) =", con.execute("SELECT COUNT(DISTINCT customer_id) FROM orders").fetchone()[0],
      "| pandas nunique =", orders["customer_id"].nunique())
print("asserts passed (rows ordered by customer_id)")
```

**Output (my run):**
```text
buggy SUM(DISTINCT) [(1, 150), (2, 500), (3, 40)]
HAVING status (bare column) [(1, 250), (2, 500), (3, 120)]
fixed (WHERE before GROUP BY) [(1, 200), (2, 500), (3, 80)]
fixed (SUM(CASE ...)) [(1, 200), (2, 500), (3, 80)]
SUM(amount), all statuses [(1, 250), (2, 500), (3, 120)]
             sum  sum_distinct  lost
customer_id                         
1            250           150   100
2            500           500     0
3            120            40    80
customers where DISTINCT lost money: [1, 3]
legit: COUNT(DISTINCT customer_id) = 3 | pandas nunique = 3
asserts passed (rows ordered by customer_id)
```

**Edge cases:**
- Customers whose amounts are all different look fine, so spot checks on a few rows can pass.
- A customer with no completed orders disappears from the `WHERE` version, but shows revenue 0 in the `SUM(CASE ...)` version. Choose which one you want.
- NULL amounts are ignored by both `SUM` and `SUM(DISTINCT)`.
- Float amounts: two prices that look equal can differ in the last digit, and DISTINCT then does not remove them.

**Then explain:**
- **What DISTINCT does:** de-duplicates the values, not the rows or the orders. `SUM(DISTINCT amount)` treats amounts as a set.
- **When DISTINCT in an aggregate is right:** `COUNT(DISTINCT customer_id)` (unique customers). For sums, de-duplicate by key (for example `SELECT DISTINCT order_id, amount` in a subquery, or fix the join that fanned rows out), never by value.
- **Corrected query:** filter rows with `WHERE status = 'completed'`, then `SUM(amount) ... GROUP BY customer_id`; or `SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END)`. Both gave 200, 500, 80.
- **pandas check:** `sum` versus `drop_duplicates().sum()` per customer; the `lost` column (100 and 80) shows exactly which customers were hit, and the buggy SQL equals the drop-duplicates version.
- **HAVING:** use it only for conditions on aggregates (`HAVING SUM(amount) > 100`).

**Follow-ups:**
- *How would a join cause a similar problem?* A one-to-many join repeats the amount on each child row, so `SUM` overstates; `DISTINCT` on the amount is the wrong repair (Part 2).
- *`AVG(DISTINCT x)`?* Same idea: averages the distinct values.
- *How do you catch this in review?* Reconcile against an independent total (pandas or `SUM` without DISTINCT).

**Common mistakes:**
- Adding DISTINCT to make a number "look right".
- Putting a row filter in `HAVING`.
- Not checking per-group totals against a second method.

### Q18 ⭐⭐⭐ 🟡 Debugging: this query errors in PostgreSQL but runs in some MySQL setups: SELECT customer_id, status, SUM(amount) FROM orders GROUP BY customer_id. Explain the rule that every non-aggregated SELECT column must be in GROUP BY (or functionally dependent on it), what MySQL ONLY_FULL_GROUP_BY and SQLite bare columns do instead (hedged), why silent arbitrary values are dangerous, and how to fix it correctly for each intended meaning (group by status too, or aggregate it).
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** Every non-aggregated SELECT column must be in `GROUP BY` or functionally dependent on it; PostgreSQL rejects the query, MySQL with `ONLY_FULL_GROUP_BY` (the default in recent versions, from memory) rejects it, while SQLite accepts it and returns the `status` of one arbitrary row, which is dangerous because it looks like a real answer.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'completed',100),(2,1,'cancelled',50),(3,1,'completed',70),
 (4,2,'refunded',200),(5,2,'completed',30);
```

**SQL answer:** `bad` is the query from the question; `f1` (group by customer and status) and `f2` (aggregate the status) are the fixes, all in the Code block.

**pandas answer:** `p1` (`groupby(["customer_id", "status"])`) and `p2` (named aggregation with `max`/`nunique`) in the Code block. pandas has no bare columns: a non-key column must go through an explicit function such as `first`.

**Example:** customer 1 has completed 100, cancelled 50, completed 70. The bad query returns one row per customer with total 220, and a status of `completed`, but the query never says which status. For customer 2 (refunded 200, completed 30) it returned `refunded`. If the intent was "total per customer and status", `f1` returns four rows (1/cancelled 50, 1/completed 170, 2/completed 30, 2/refunded 200). If the intent was "total per customer, plus one summary of the status", `f2` makes the choice explicit (`MAX(status)`, number of distinct statuses).

**Code:** run with `python3 -I`.
```python
# Debugging a bare column in GROUP BY (Q18): SQLite runs it, silently.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'completed',100),(2,1,'cancelled',50),(3,1,'completed',70),
 (4,2,'refunded',200),(5,2,'completed',30);
""")

bad = "SELECT customer_id, status, SUM(amount) AS total FROM orders GROUP BY customer_id ORDER BY customer_id"
print("bare column (SQLite runs it; value of status is not defined by the query):")
print(con.execute(bad).fetchall())

# SQLite special case: with a single MIN() or MAX(), bare columns come from the row holding the min/max
mx = "SELECT customer_id, status, MAX(amount) AS top_amt FROM orders GROUP BY customer_id ORDER BY customer_id"
print("SQLite MAX special case (status of the max row):", con.execute(mx).fetchall())
two = "SELECT customer_id, status, MAX(amount), MIN(amount) FROM orders GROUP BY customer_id ORDER BY customer_id"
print("with MAX and MIN both (no special case, arbitrary row):", con.execute(two).fetchall())

# fix 1: the intended meaning is 'per customer and status'
f1 = "SELECT customer_id, status, SUM(amount) AS total FROM orders GROUP BY customer_id, status ORDER BY customer_id, status"
# fix 2: the intended meaning is 'per customer, status is an aggregate' (say which one)
f2 = ("SELECT customer_id, MAX(status) AS max_status, COUNT(DISTINCT status) AS n_statuses, SUM(amount) AS total "
      "FROM orders GROUP BY customer_id ORDER BY customer_id")
print("fix 1:", con.execute(f1).fetchall())
print("fix 2:", con.execute(f2).fetchall())

orders = pd.read_sql("SELECT * FROM orders", con)
p1 = (orders.groupby(["customer_id", "status"], as_index=False)["amount"].sum()
      .rename(columns={"amount": "total"}).sort_values(["customer_id", "status"]).reset_index(drop=True))
p2 = (orders.groupby("customer_id")
      .agg(max_status=("status", "max"), n_statuses=("status", "nunique"), total=("amount", "sum"))
      .reset_index())
pd.testing.assert_frame_equal(pd.read_sql(f1, con), p1)
pd.testing.assert_frame_equal(pd.read_sql(f2, con), p2)
print(p1.to_string(index=False)); print(p2.to_string(index=False))
print("asserts passed (fix 1 ordered by customer_id, status; fix 2 by customer_id)")

# pandas has no bare columns: asking for a non-key column needs an explicit function
print("pandas explicit first():", orders.groupby("customer_id").agg(status=("status", "first"), total=("amount", "sum")).reset_index().to_dict("records"))
```

**Output (my run):**
```text
bare column (SQLite runs it; value of status is not defined by the query):
[(1, 'completed', 220), (2, 'refunded', 230)]
SQLite MAX special case (status of the max row): [(1, 'completed', 100), (2, 'refunded', 200)]
with MAX and MIN both (no special case, arbitrary row): [(1, 'cancelled', 100, 50), (2, 'completed', 200, 30)]
fix 1: [(1, 'cancelled', 50), (1, 'completed', 170), (2, 'completed', 30), (2, 'refunded', 200)]
fix 2: [(1, 'completed', 2, 220), (2, 'refunded', 2, 230)]
 customer_id    status  total
           1 cancelled     50
           1 completed    170
           2 completed     30
           2  refunded    200
 customer_id max_status  n_statuses  total
           1  completed           2    220
           2   refunded           2    230
asserts passed (fix 1 ordered by customer_id, status; fix 2 by customer_id)
pandas explicit first(): [{'customer_id': 1, 'status': 'completed', 'total': 220}, {'customer_id': 2, 'status': 'refunded', 'total': 230}]
```

**Edge cases:**
- SQLite's documented special case (confirmed by my run): with a single `MAX()` or `MIN()` in the query, bare columns come from the row that holds the max or min (customer 1 gave `completed` with 100, customer 2 `refunded` with 200). With both `MAX` and `MIN` it falls back to an arbitrary row (customer 1 gave `cancelled`). Do not rely on it.
- Functional dependence: grouping by a primary key lets PostgreSQL (and MySQL 5.7+, from memory) accept other columns of that table.
- `GROUP BY customer_id` with a `name` column from the same customers table is fine only under that rule.

**Then explain:**
- **The rule:** after grouping, each output row represents a group; a column with several values per group has no single value to show.
- **MySQL:** `ONLY_FULL_GROUP_BY` SQL mode rejects the query; when the mode is switched off, MySQL silently picks a value (from memory, not executed here).
- **Danger:** the result looks valid, passes review and changes when the plan changes.
- **Fix by intent:** add the column to `GROUP BY`, or aggregate it (`MAX`, `COUNT(DISTINCT)`, `MIN`), or use a window function for "status of the latest order" (Part 4).
- **pandas:** the equivalent of a bare column is `first()`/`last()`, which is explicit about the choice and depends on row order.

**Follow-ups:**
- *How do you get the status of the largest order per customer?* Use a ranking window (Part 4); the SQLite `MAX` trick is not portable.
- *Is `ANY_VALUE` an option?* MySQL and some others have it (from memory, not executed); it states "I do not care which".
- *Does SELECT DISTINCT have this issue?* No, it applies to the whole row.

**Common mistakes:**
- "Fixing" the error by adding every column to `GROUP BY` and changing the grain.
- Disabling `ONLY_FULL_GROUP_BY` to make the query run.
- Trusting SQLite's output as a model of other engines.

### Q19 ⭐⭐ 🟢 What is the difference between SELECT DISTINCT and GROUP BY? Using orders(order_id, customer_id, status, city), show DISTINCT on one and on several columns, how NULLs are treated (collapsed to one value), COUNT(DISTINCT customer_id) versus COUNT(DISTINCT customer_id, city) (multi-column count is not portable; hedge), and when GROUP BY is needed because you also aggregate. Pandas: drop_duplicates, unique, nunique and groupby.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** `SELECT DISTINCT` and `GROUP BY` with no aggregate return the same rows; use `GROUP BY` when you also need an aggregate, and note that both treat NULLs as one value, while `COUNT(DISTINCT col)` skips NULLs.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, city TEXT);
INSERT INTO orders VALUES
 (1,10,'paid','Pune'),(2,10,'paid','Pune'),(3,10,'paid','Delhi'),
 (4,20,'refunded','Pune'),(5,20,NULL,'Pune'),(6,30,NULL,NULL),
 (7,NULL,'paid','Delhi'),(8,NULL,'paid','Delhi');
```

**SQL answer:** `d1`, `d2`, `g1`, `agg`, `portable` and `only_complete` in the Code block.

**pandas answer:** `drop_duplicates`, `unique`, `nunique` and `groupby(...).agg(...)` in the Code block.

**Example:** `status` values are paid, paid, paid, refunded, NULL, NULL, paid, paid, so `DISTINCT status` returns NULL, paid, refunded (3 values: the two NULLs collapse into one). `DISTINCT customer_id, city` returns 5 pairs: (NULL, Delhi), (10, Delhi), (10, Pune), (20, Pune), (30, NULL). `COUNT(DISTINCT customer_id)` is 3 (10, 20, 30; the NULL customer is not counted), but counting the `DISTINCT customer_id` subquery rows gives 4 because the NULL is a row there.

**Code:** run with `python3 -I`.
```python
# SELECT DISTINCT vs GROUP BY, NULLs, COUNT(DISTINCT) variants (Q19).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, city TEXT);
INSERT INTO orders VALUES
 (1,10,'paid','Pune'),(2,10,'paid','Pune'),(3,10,'paid','Delhi'),
 (4,20,'refunded','Pune'),(5,20,NULL,'Pune'),(6,30,NULL,NULL),
 (7,NULL,'paid','Delhi'),(8,NULL,'paid','Delhi');
""")
def rows(q): return con.execute(q).fetchall()

d1 = "SELECT DISTINCT status FROM orders ORDER BY status"
d2 = "SELECT DISTINCT customer_id, city FROM orders ORDER BY customer_id, city"
g1 = "SELECT status FROM orders GROUP BY status ORDER BY status"
print("DISTINCT status:", rows(d1))
print("GROUP BY status:", rows(g1), "(same rows)")
print("DISTINCT customer_id, city:", rows(d2))
assert rows(d1) == rows(g1)

print("COUNT(DISTINCT customer_id):", rows("SELECT COUNT(DISTINCT customer_id) FROM orders")[0][0], "(NULL not counted)")
print("COUNT(*) over DISTINCT customer_id subquery:", rows("SELECT COUNT(*) FROM (SELECT DISTINCT customer_id FROM orders)")[0][0], "(NULL counted as a value)")
try:
    con.execute("SELECT COUNT(DISTINCT customer_id, city) FROM orders")
except sqlite3.Error as e:
    print("COUNT(DISTINCT a, b) in SQLite ->", type(e).__name__, e)
portable = "SELECT COUNT(*) FROM (SELECT DISTINCT customer_id, city FROM orders)"
print("pairs via subquery (NULL pairs kept):", rows(portable)[0][0])
only_complete = "SELECT COUNT(*) FROM (SELECT DISTINCT customer_id, city FROM orders WHERE customer_id IS NOT NULL AND city IS NOT NULL)"
print("pairs with no NULLs (what a multi-column COUNT(DISTINCT) would give where supported):", rows(only_complete)[0][0])

# GROUP BY is needed when you also aggregate
agg = "SELECT customer_id, COUNT(*) AS n_orders, COUNT(DISTINCT city) AS n_cities FROM orders GROUP BY customer_id ORDER BY customer_id"
print("GROUP BY with aggregates:", rows(agg))

# pandas
df = pd.read_sql("SELECT * FROM orders", con)
p1 = df[["status"]].drop_duplicates().sort_values("status", na_position="first").reset_index(drop=True)
print("pandas drop_duplicates on status:", p1["status"].tolist())
print("unique():", df["status"].unique().tolist())
print("nunique() default dropna=True:", df["customer_id"].nunique(), "| dropna=False:", df["customer_id"].nunique(dropna=False))
p2 = df[["customer_id", "city"]].drop_duplicates()
print("pairs via drop_duplicates:", len(p2), "| NULL-free pairs:", len(p2.dropna()))
sql_d2 = pd.read_sql(d2, con)
p2s = p2.sort_values(["customer_id", "city"], na_position="first").reset_index(drop=True)
assert list(map(tuple, sql_d2.astype(object).where(sql_d2.notna(), None).values.tolist())) == \
       list(map(tuple, p2s.astype(object).where(p2s.notna(), None).values.tolist()))
sql_agg = pd.read_sql(agg, con)
p_agg = (df.groupby("customer_id", dropna=False).agg(n_orders=("order_id", "size"), n_cities=("city", "nunique"))
         .reset_index().sort_values("customer_id", na_position="first").reset_index(drop=True))
pd.testing.assert_frame_equal(sql_agg, p_agg, check_dtype=False)
assert rows("SELECT COUNT(DISTINCT customer_id) FROM orders")[0][0] == df["customer_id"].nunique()
assert rows(portable)[0][0] == len(p2) and rows(only_complete)[0][0] == len(p2.dropna())
print("asserts passed (sorted with NULL first, as SQLite does)")
```

**Output (my run):**
```text
DISTINCT status: [(None,), ('paid',), ('refunded',)]
GROUP BY status: [(None,), ('paid',), ('refunded',)] (same rows)
DISTINCT customer_id, city: [(None, 'Delhi'), (10, 'Delhi'), (10, 'Pune'), (20, 'Pune'), (30, None)]
COUNT(DISTINCT customer_id): 3 (NULL not counted)
COUNT(*) over DISTINCT customer_id subquery: 4 (NULL counted as a value)
COUNT(DISTINCT a, b) in SQLite -> OperationalError wrong number of arguments to function COUNT()
pairs via subquery (NULL pairs kept): 5
pairs with no NULLs (what a multi-column COUNT(DISTINCT) would give where supported): 3
GROUP BY with aggregates: [(None, 2, 1), (10, 3, 2), (20, 2, 1), (30, 1, 0)]
pandas drop_duplicates on status: [nan, 'paid', 'refunded']
unique(): ['paid', 'refunded', nan]
nunique() default dropna=True: 3 | dropna=False: 4
pairs via drop_duplicates: 5 | NULL-free pairs: 3
asserts passed (sorted with NULL first, as SQLite does)
```

**Edge cases:**
- Multi-column `COUNT(DISTINCT a, b)` is not valid in SQLite (my run raised `wrong number of arguments to function COUNT()`). MySQL accepts it (and skips rows where any argument is NULL, from memory); PostgreSQL does not accept the comma form (a row-constructor form exists, with its own NULL behaviour); not executed here. The portable form is `SELECT COUNT(*) FROM (SELECT DISTINCT a, b ...)`, which counts a pair with a NULL as a value (5 here), unlike a NULL-skipping multi-column count (3).
- `DISTINCT` applies to the whole row, not to the first column: `SELECT DISTINCT a, b` is not "distinct a".
- pandas `nunique()` skips NaN by default (3), `nunique(dropna=False)` counts it (4); `unique()` keeps NaN in the output.
- `groupby` drops NaN keys unless `dropna=False`; the run used `dropna=False` to match SQL.

**Then explain:**
- **Equivalence:** `DISTINCT x` is the same result as `GROUP BY x`; engines often plan them the same way (hedged, not checked here).
- **Choose GROUP BY** when you aggregate (`COUNT(*)`, `COUNT(DISTINCT city)`); choose DISTINCT for a plain unique list.
- **NULLs:** collapsed into one value by both.
- **Counting uniques:** `COUNT(DISTINCT col)` ignores NULL; `COUNT(*)` over a DISTINCT subquery does not.
- **pandas:** `df[["status"]].drop_duplicates()` (keeps first NaN), `Series.unique()` (array, order of appearance), `nunique()` (count), `groupby(...).agg(n=("order_id", "size"))`.

**Follow-ups:**
- *Is DISTINCT slow?* It needs a sort or hash over the selected columns; use it only when duplicates are real (Part 11).
- *Why not put DISTINCT in every query?* It hides a join fan-out bug (Part 2) and costs time.
- *DISTINCT ON?* PostgreSQL-only (from memory, not executed).

**Common mistakes:**
- Thinking `COUNT(DISTINCT x)` counts NULL as a value.
- Using DISTINCT to hide a duplicate-producing join.
- Using a multi-column `COUNT(DISTINCT a, b)` and expecting it to run everywhere.

### Q20 ⭐⭐ 🟢 Column expressions and aliases: given order_items(item_id, order_id, qty, unit_price, discount_pct), write a SELECT with a computed line_total, a rounded value, and a text label built by concatenation (|| versus CONCAT, hedged). Explain alias scope, quoting aliases with spaces, integer division (qty/2 when both are integers) and implicit casting, and how the same is written in pandas with assign and round.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** A SELECT list can hold any expression; an alias names it, but an alias cannot be used in the WHERE clause of standard SQL (SQLite allows it) and dividing two integers truncates, so write `/ 100.0` or cast.

**Schema and sample data:**
```sql
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, unit_price REAL, discount_pct INTEGER);
INSERT INTO order_items VALUES
 (1,100,3,199.99,10),(2,100,5,49.50,0),(3,101,1,2.50,0),(4,101,2,15.25,25),(5,102,7,12.00,5);
```

**SQL answer:** the query is `sql` in the Code block: `line_total`, a rounded value with a quoted alias containing spaces, and a text label with `||`.

**pandas answer:** `assign(...)` with `round(2)` and string concatenation, in the Code block (`p`).

**Example:** item 1: 3 x 199.99 with 10 per cent off = 3 x 199.99 x 0.9 = 539.973, rounded 539.97. Item 3: 1 x 2.50, no discount = 2.5. Item 4: 2 x 15.25 x 0.75 = 22.875, rounded to 22.88. The label for item 1 is `Item 1 x3`. Now the integer trap: `discount_pct / 100` with `discount_pct = 10` is `0` (integer division), so the discount would vanish (my run: `(10, 0, 0.1)`). `qty / 2` for qty 5 gives 2, not 2.5.

**Code:** run with `python3 -I`.
```python
# Column expressions, aliases, integer division, rounding, concatenation (Q20).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, qty INTEGER, unit_price REAL, discount_pct INTEGER);
INSERT INTO order_items VALUES
 (1,100,3,199.99,10),(2,100,5,49.50,0),(3,101,1,2.50,0),(4,101,2,15.25,25),(5,102,7,12.00,5);
""")

sql = """
SELECT item_id,
       qty * unit_price * (1 - discount_pct / 100.0)            AS line_total,
       ROUND(qty * unit_price * (1 - discount_pct / 100.0), 2)  AS "Line Total (rounded)",
       'Item ' || item_id || ' x' || qty                        AS label
FROM order_items
ORDER BY item_id
"""
sql_df = pd.read_sql(sql, con)
print(sql_df.to_string(index=False))

# the traps
print("qty / 2 (both integers):", con.execute("SELECT qty, qty / 2, qty / 2.0 FROM order_items ORDER BY item_id").fetchall())
print("discount_pct / 100 (integer):", con.execute("SELECT discount_pct, discount_pct / 100, discount_pct / 100.0 FROM order_items WHERE item_id IN (1,4)").fetchall())
print("alias in ORDER BY works:", con.execute("SELECT qty*unit_price AS gross FROM order_items ORDER BY gross DESC LIMIT 1").fetchall())
try:
    print("alias in WHERE (SQLite accepts it as an extension):", con.execute("SELECT qty*unit_price AS gross FROM order_items WHERE gross > 100 ORDER BY item_id").fetchall())
except sqlite3.Error as e:
    print("alias in WHERE ->", e)
print("'Item ' || NULL ->", con.execute("SELECT 'Item ' || NULL").fetchone()[0])
print("'5' + 3 =", con.execute("SELECT '5' + 3").fetchone()[0], "| typeof('5' + 3) =", con.execute("SELECT typeof('5' + 3)").fetchone()[0])

# pandas
oi = pd.read_sql("SELECT * FROM order_items", con)
p = (oi.assign(line_total=lambda d: d["qty"] * d["unit_price"] * (1 - d["discount_pct"] / 100),
               rounded=lambda d: d["line_total"].round(2),
               label=lambda d: "Item " + d["item_id"].astype(str) + " x" + d["qty"].astype(str))
       [["item_id", "line_total", "rounded", "label"]]
       .rename(columns={"rounded": "Line Total (rounded)"}))
pd.testing.assert_frame_equal(sql_df, p)
print("asserts passed: SQL == pandas (ordered by item_id, round to 2 places; float values agree exactly here)")

# pandas / in Python is TRUE division; SQL integer / is truncating. Match with //.
print("pandas qty / 2:", (oi["qty"] / 2).tolist(), "| qty // 2:", (oi["qty"] // 2).tolist())
assert (oi["qty"] // 2).tolist() == [r[0] for r in con.execute("SELECT qty / 2 FROM order_items ORDER BY item_id")]

# honest surprise: halves round differently. SQLite rounds half away from zero, numpy rounds half to even.
print("ROUND(2.5), ROUND(3.5) in SQLite:", con.execute("SELECT ROUND(2.5), ROUND(3.5)").fetchone())
print("pandas Series([2.5, 3.5]).round():", pd.Series([2.5, 3.5]).round().tolist())
```

**Output (my run):**
```text
 item_id  line_total  Line Total (rounded)     label
       1     539.973                539.97 Item 1 x3
       2     247.500                247.50 Item 2 x5
       3       2.500                  2.50 Item 3 x1
       4      22.875                 22.88 Item 4 x2
       5      79.800                 79.80 Item 5 x7
qty / 2 (both integers): [(3, 1, 1.5), (5, 2, 2.5), (1, 0, 0.5), (2, 1, 1.0), (7, 3, 3.5)]
discount_pct / 100 (integer): [(10, 0, 0.1), (25, 0, 0.25)]
alias in ORDER BY works: [(599.97,)]
alias in WHERE (SQLite accepts it as an extension): [(599.97,), (247.5,)]
'Item ' || NULL -> None
'5' + 3 = 8 | typeof('5' + 3) = integer
asserts passed: SQL == pandas (ordered by item_id, round to 2 places; float values agree exactly here)
pandas qty / 2: [1.5, 2.5, 0.5, 1.0, 3.5] | qty // 2: [1, 2, 0, 1, 3]
ROUND(2.5), ROUND(3.5) in SQLite: (3.0, 4.0)
pandas Series([2.5, 3.5]).round(): [2.0, 4.0]
```

**Edge cases:**
- Alias scope: you can use an alias in `ORDER BY`; standard SQL evaluates `WHERE` before the SELECT list, so aliases are not visible there. SQLite accepted `WHERE gross > 100` anyway (shown in the run); PostgreSQL and SQL Server reject it (from memory, not executed). Repeat the expression or use a subquery or CTE.
- NULL: `'Item ' || NULL` is NULL in SQLite (shown in the run). `CONCAT` ignores NULLs in MySQL and PostgreSQL (from memory, not executed).
- Rounding of exact halves differs: SQLite `ROUND(2.5)` is 3.0, pandas `Series([2.5, 3.5]).round()` gave `[2.0, 4.0]` (round half to even). In this data the 22.875 case agreed (22.88 in both) and I did not hit a conflict in the two-decimal results, but a half at the rounding digit can differ between engines; a decimal type or integer cents is safer for money.
- Implicit casting: in SQLite `'5' + 3` gave the integer 8; other engines are stricter or differ (from memory, not executed).

**Then explain:**
- **Computed column:** `qty * unit_price * (1 - discount_pct / 100.0) AS line_total`.
- **Quoting an alias with spaces:** double quotes in standard SQL (`"Line Total (rounded)"`); MySQL uses backticks, SQL Server brackets (from memory, not executed). Avoid spaces in real code.
- **Concatenation:** `||` is standard (SQLite, PostgreSQL, Oracle); `CONCAT()` in MySQL, SQL Server and others; in MySQL `||` is logical OR by default (from memory, not executed).
- **Integer division:** `qty / 2` with two integers truncates in SQLite (and in PostgreSQL, SQL Server; MySQL's `/` returns a decimal, with `DIV` for integer division; from memory, not executed). Write `qty / 2.0` or `CAST(qty AS REAL) / 2`.
- **pandas:** `assign(line_total=..., rounded=lambda d: d["line_total"].round(2))`; `/` is true division, `//` matches SQL's truncation for non-negative numbers (for negatives floor and truncation differ).

**Follow-ups:**
- *Why not alias in WHERE?* The WHERE clause runs before SELECT is computed (execution order: FROM, WHERE, GROUP BY, HAVING, SELECT, ORDER BY).
- *How do you round money?* Store integer minor units or a decimal type; round at the end.
- *What about floating-point display?* `0.1 + 0.2` style noise; round for display, not for storage.

**Common mistakes:**
- `discount_pct / 100` with integers, silently giving no discount.
- Using an alias in WHERE and having it fail on the next database.
- Rounding in the middle of a calculation and then summing.
- Assuming `ROUND` and `numpy.round` agree on halves.

### Q21 ⭐⭐ 🟢 String filtering basics: customers(customer_id, name, email, city). Write filters for names starting with 'A', emails ending in '@gmail.com', cities in a list, case-insensitive match (ILIKE, LOWER, COLLATE, hedged), and a name containing a literal underscore. Explain why a leading wildcard usually prevents index use (light note; Part 11 has indexes) and the pandas str.startswith, str.contains(case=False, regex=False) and na handling.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** use `LIKE 'A%'` for starts-with, `LIKE '%@gmail.com'` for ends-with, `IN (...)` for lists, `ESCAPE` for a literal `_` or `%`, and `LOWER(col) LIKE LOWER(...)` for a case-insensitive match that works everywhere; remember that `_` is a wildcard and NULL never matches.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
INSERT INTO customers VALUES
 (1,'Asha','asha@gmail.com','Pune'),
 (2,'arjun','arjun@Gmail.com','Delhi'),
 (3,'Ben','ben@work.in','Mumbai'),
 (4,'A_B Traders','ab@gmail.com','Pune'),
 (5,'Chitra',NULL,'Delhi'),
 (6,'Aman','aman@gmail.com.fake','Chennai'),
 (7,'Dev','dev@gmail.com',NULL),
 (8,'AxB Co','x@y.com','Pune');
```

**SQL answer:** the queries `q_start`, `q_start_cs`, `q_end`, `q_in`, `q_ci`, `q_nocase`, `q_under` and `q_under_wrong` in the Code block.

**pandas answer:** `str.startswith`, `str.endswith`, `isin`, `str.contains(..., case=False, regex=False)` and the lower-cased variants, all with `na=False`, in the Code block.

**Example:** names starting with A (SQLite, case-insensitive `LIKE`): Asha, arjun, A_B Traders, Aman, AxB Co, so ids 1, 2, 4, 6, 8. Emails ending in `@gmail.com`: ids 1, 2 (`@Gmail.com` matches because SQLite's `LIKE` ignores ASCII case), 4 and 7; the NULL email (5) and `aman@gmail.com.fake` (6) are not returned. Cities in (Pune, Delhi): 1, 2, 4, 5, 8; customer 7 has a NULL city, so it never matches. A literal underscore: `name LIKE '%\_%' ESCAPE '\'` returns only id 4. Without the escape, `'A_B%'` returns ids 4 and 8, because `_` matches any single character, so 'AxB Co' matches too.

**Code:** run with `python3 -I`.
```python
# String filtering: LIKE, IN, case-insensitive, literal underscore, NULLs, and the pandas equivalents (Q21).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, email TEXT, city TEXT);
INSERT INTO customers VALUES
 (1,'Asha','asha@gmail.com','Pune'),
 (2,'arjun','arjun@Gmail.com','Delhi'),
 (3,'Ben','ben@work.in','Mumbai'),
 (4,'A_B Traders','ab@gmail.com','Pune'),
 (5,'Chitra',NULL,'Delhi'),
 (6,'Aman','aman@gmail.com.fake','Chennai'),
 (7,'Dev','dev@gmail.com',NULL),
 (8,'AxB Co','x@y.com','Pune');
""")
def ids(q, *a): return [r[0] for r in con.execute(q, a).fetchall()]

q_start = "SELECT customer_id FROM customers WHERE name LIKE 'A%' ORDER BY customer_id"
q_start_cs = "SELECT customer_id FROM customers WHERE name GLOB 'A*' ORDER BY customer_id"
q_end = "SELECT customer_id FROM customers WHERE email LIKE '%@gmail.com' ORDER BY customer_id"
q_in = "SELECT customer_id FROM customers WHERE city IN ('Pune','Delhi') ORDER BY customer_id"
q_ci = "SELECT customer_id FROM customers WHERE LOWER(email) LIKE '%@gmail.com' ORDER BY customer_id"
q_nocase = "SELECT customer_id FROM customers WHERE email COLLATE NOCASE LIKE '%@gmail.com' ORDER BY customer_id"
q_under = "SELECT customer_id FROM customers WHERE name LIKE '%\\_%' ESCAPE '\\' ORDER BY customer_id"
q_under_wrong = "SELECT customer_id FROM customers WHERE name LIKE 'A_B%' ORDER BY customer_id"

print("name LIKE 'A%' (SQLite LIKE ignores ASCII case):", ids(q_start))
print("name GLOB 'A*' (case-sensitive, SQLite only):", ids(q_start_cs))
print("email LIKE '%@gmail.com' (NULL email excluded, 'Gmail' matches):", ids(q_end))
print("city IN list:", ids(q_in), "(NULL city never matches IN)")
print("LOWER(email) LIKE ...:", ids(q_ci))
print("COLLATE NOCASE LIKE:", ids(q_nocase))
print("literal underscore with ESCAPE:", ids(q_under))
print("unescaped 'A_B%' (underscore is a wildcard for one character, so 'AxB Co' matches too):", ids(q_under_wrong))
print("PRAGMA case_sensitive_like makes LIKE case-sensitive:")
con.execute("PRAGMA case_sensitive_like = ON")
print("  name LIKE 'A%' now:", ids(q_start))
con.execute("PRAGMA case_sensitive_like = OFF")

# pandas
df = pd.read_sql("SELECT * FROM customers", con)
def pid(mask): return df.loc[mask, "customer_id"].tolist()
p_start_ci = pid(df["name"].str.lower().str.startswith("a", na=False))
p_start_cs = pid(df["name"].str.startswith("A", na=False))
p_end_ci = pid(df["email"].str.lower().str.endswith("@gmail.com", na=False))
p_in = pid(df["city"].isin(["Pune", "Delhi"]))
p_contains = pid(df["email"].str.contains("@GMAIL.COM", case=False, regex=False, na=False))
p_under = pid(df["name"].str.contains("_", regex=False, na=False))
print("pandas startswith 'A' case-sensitive:", p_start_cs, "| lower().startswith('a'):", p_start_ci)
print("pandas email endswith (lowercased):", p_end_ci, "| contains('@GMAIL.COM', case=False, regex=False):", p_contains)
print("raw str.startswith without na= on a NaN row ->", df["email"].str.startswith("a").tolist())
print("raw str.contains('gmail') with na default ->", df["email"].str.contains("gmail", regex=False).tolist())

assert ids(q_start) == p_start_ci and ids(q_start_cs) == p_start_cs
assert ids(q_ci) == ids(q_nocase) == p_end_ci
assert ids(q_end) == p_end_ci
assert ids(q_in) == p_in and ids(q_under) == p_under == [4]
assert ids(q_under_wrong) == [4, 8]
print("asserts passed (results compared as customer_id lists, ascending)")
```

**Output (my run):**
```text
name LIKE 'A%' (SQLite LIKE ignores ASCII case): [1, 2, 4, 6, 8]
name GLOB 'A*' (case-sensitive, SQLite only): [1, 4, 6, 8]
email LIKE '%@gmail.com' (NULL email excluded, 'Gmail' matches): [1, 2, 4, 7]
city IN list: [1, 2, 4, 5, 8] (NULL city never matches IN)
LOWER(email) LIKE ...: [1, 2, 4, 7]
COLLATE NOCASE LIKE: [1, 2, 4, 7]
literal underscore with ESCAPE: [4]
unescaped 'A_B%' (underscore is a wildcard for one character, so 'AxB Co' matches too): [4, 8]
PRAGMA case_sensitive_like makes LIKE case-sensitive:
  name LIKE 'A%' now: [1, 4, 6, 8]
pandas startswith 'A' case-sensitive: [1, 4, 6, 8] | lower().startswith('a'): [1, 2, 4, 6, 8]
pandas email endswith (lowercased): [1, 2, 4, 7] | contains('@GMAIL.COM', case=False, regex=False): [1, 2, 4, 6, 7]
raw str.startswith without na= on a NaN row -> [True, True, False, True, False, True, False, False]
raw str.contains('gmail') with na default -> [True, False, False, True, False, True, True, False]
asserts passed (results compared as customer_id lists, ascending)
```

**Edge cases:**
- Case sensitivity is a per-engine surprise: SQLite `LIKE` is case-insensitive for ASCII (shown: 1, 2, 4, 6, 8), `GLOB` and `PRAGMA case_sensitive_like = ON` make it case-sensitive (1, 4, 6, 8). PostgreSQL `LIKE` is case-sensitive and has `ILIKE`; in MySQL and SQL Server it depends on the column collation (all from memory, not executed). `LOWER(col) LIKE ...` is portable. `COLLATE NOCASE` is SQLite-specific syntax (other engines name collations differently).
- NULL: `NULL LIKE '%x'` is UNKNOWN, so the row is dropped; `NOT LIKE` drops it as well.
- `IN` with a NULL city: never matches (see Q13 for the NOT IN trap).
- pandas on NaN: in my pandas 3.0.5 run `str.startswith("a")` returned `False` for the NaN row, but older object-dtype columns returned NaN (from memory), which breaks a boolean mask. Always pass `na=False`.
- `str.contains` is a substring test, not an ends-with test: `contains("@GMAIL.COM", case=False, regex=False)` also matched id 6 (`aman@gmail.com.fake`), so it returned 1, 2, 4, 6, 7 versus the SQL answer 1, 2, 4, 7.

**Then explain:**
- **Wildcards:** `%` means any run of characters, `_` means exactly one.
- **Literal underscore or percent:** `LIKE '%\_%' ESCAPE '\'`; the escape character is chosen by the `ESCAPE` clause in standard SQL.
- **Leading wildcard and indexes (light note):** `LIKE '%gmail.com'` cannot use an ordinary B-tree index to seek, because the start of the string is unknown; `LIKE 'A%'` often can (hedged: it depends on the engine and collation; Part 11 covers indexes).
- **pandas:** `str.contains(case=False, regex=False)` treats the pattern literally, which avoids regex metacharacters such as `.` and `_`.
- **Case-insensitive options:** `LOWER`, `ILIKE` (PostgreSQL), `COLLATE` (engine-specific).

**Follow-ups:**
- *Regex?* `REGEXP`, `~` or `RLIKE` depending on the engine (not executed here); SQLite needs a user function for REGEXP.
- *How would you match the domain exactly?* Extract it (for example with `SUBSTR` and `INSTR` after the `@`) and compare for equality, instead of pattern-matching the whole address.
- *Trim spaces?* Clean with `TRIM` first (Part 10).

**Common mistakes:**
- Forgetting that `_` is a wildcard.
- Assuming `LIKE` is case-sensitive (or case-insensitive) in every database.
- Using `str.contains` with the default `regex=True` and a pattern with `.`, `+` or `(`.
- No `na=False`, then a mask with NaN fails on indexing.

### Q22 ⭐⭐ 🟡 LIMIT and OFFSET for pagination: orders(order_id, created_at, amount). Show page 3 with 10 rows per page, why OFFSET gets slower on deep pages, why pages can overlap or skip rows if the sort key has ties or rows are inserted between requests, and the keyset (seek) alternative with WHERE (created_at, order_id) < (...) (row-value syntax is not available everywhere; hedge). Pandas: iloc slicing and head/tail, nlargest with offset from the pandas docs.
**Asked at:** interview-prep guide and platform question bank (StrataScratch, DataLemur style), not a candidate report; product-company data scientist screens
**Say this first (1 line):** page N is `ORDER BY ... LIMIT 10 OFFSET (N-1)*10`, which needs a total order (add the unique key) and gets slower on deep pages and unstable when rows arrive; for infinite scroll use keyset pagination, `WHERE (created_at, order_id) < (last_created_at, last_order_id)`.

**Schema and sample data:** 30 orders, two per day so `created_at` has ties: order `i` (1 to 30) has `created_at = '2025-03-' || day` with `day = (i - 1) / 2 + 1` (orders 1 and 2 on 2025-03-01, 3 and 4 on 03-02, ..., 29 and 30 on 03-15) and `amount = 100 + 10 * i`. The Code block creates it with `executemany`.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, created_at TEXT, amount INTEGER);
-- 30 rows built by the Python loop in the Code block
```

**SQL answer:** `page3` (offset form), `keyset_rv` (row-value keyset) and `keyset_or` (expanded keyset) in the Code block.

**pandas answer:** `ordered.iloc[20:30]`, and the pandas-docs idiom `nlargest(30, ...).tail(10)`, in the Code block.

**Example:** sorted newest first with `order_id` as the tie-breaker the list is 30, 29, 28, ..., 1. Page 1 is 30..21, page 2 is 20..11, page 3 (`OFFSET 20 LIMIT 10`) is 10..1. If a new order 31 arrives after the client fetched page 1, page 2 now starts one row lower: my run returned 21..12, so order 21 appears on both pages. Keyset page 2 after order 30..21 uses the last row (2025-03-11, id 21): `(created_at, order_id) < ('2025-03-11', 21)` gives 20..11 again, even after order 31 is inserted.

**Code:** run with `python3 -I`.
```python
# LIMIT/OFFSET pagination, its failure modes, and keyset (seek) pagination (Q22).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, created_at TEXT, amount INTEGER)")
# 30 orders, two per day (so created_at has ties): ids 1,2 on 2025-03-01; 3,4 on 2025-03-02; ... 29,30 on 2025-03-15
rows = [(i, f"2025-03-{(i - 1) // 2 + 1:02d}", 100 + 10 * i) for i in range(1, 31)]
con.executemany("INSERT INTO orders VALUES (?,?,?)", rows)

PAGE, N = 10, 3
page3 = f"SELECT order_id, created_at FROM orders ORDER BY created_at DESC, order_id DESC LIMIT {PAGE} OFFSET {(N - 1) * PAGE}"
r3 = con.execute(page3).fetchall()
print("page 3 (OFFSET 20):", [r[0] for r in r3])

page1 = "SELECT order_id FROM orders ORDER BY created_at DESC, order_id DESC LIMIT 10 OFFSET 0"
page2 = "SELECT order_id FROM orders ORDER BY created_at DESC, order_id DESC LIMIT 10 OFFSET 10"
p1 = [r[0] for r in con.execute(page1)]
print("page 1:", p1)

# a new order arrives between requests -> offset pages shift
con.execute("INSERT INTO orders VALUES (31,'2025-03-16',999)")
p2_after_insert = [r[0] for r in con.execute(page2)]
print("page 2 after a new order arrived:", p2_after_insert, "-> repeats", sorted(set(p1) & set(p2_after_insert)), "from page 1")
con.execute("DELETE FROM orders WHERE order_id = 31")

# ties: sort key without the tie-breaker (created_at only) can split a tie group unpredictably between pages
tie_q = "SELECT order_id FROM orders ORDER BY created_at DESC LIMIT 3 OFFSET {}"
print("created_at-only order, pages of 3 (engine's tie order, not guaranteed):",
      [[r[0] for r in con.execute(tie_q.format(o))] for o in (0, 3)])

# keyset (seek): continue after the last row of page 1 with a row-value comparison
last = con.execute("SELECT created_at, order_id FROM orders WHERE order_id = ?", (p1[-1],)).fetchone()
keyset_rv = ("SELECT order_id FROM orders WHERE (created_at, order_id) < (?, ?) "
             "ORDER BY created_at DESC, order_id DESC LIMIT 10")
keyset_or = ("SELECT order_id FROM orders WHERE created_at < ? OR (created_at = ? AND order_id < ?) "
             "ORDER BY created_at DESC, order_id DESC LIMIT 10")
k_rv = [r[0] for r in con.execute(keyset_rv, last)]
k_or = [r[0] for r in con.execute(keyset_or, (last[0], last[0], last[1]))]
print("keyset page 2 (row values):", k_rv)
print("keyset page 2 (expanded OR):", k_or)

# after a new row arrives, keyset page 2 is unchanged
con.execute("INSERT INTO orders VALUES (31,'2025-03-16',999)")
print("keyset page 2 after insert:", [r[0] for r in con.execute(keyset_rv, last)])
con.execute("DELETE FROM orders WHERE order_id = 31")

# pandas
df = pd.read_sql("SELECT * FROM orders", con)
ordered = df.sort_values(["created_at", "order_id"], ascending=False).reset_index(drop=True)
pp3 = ordered.iloc[(N - 1) * PAGE : N * PAGE]
print("pandas iloc[20:30]:", pp3["order_id"].tolist())
# nlargest then tail is the pandas docs' idiom for LIMIT/OFFSET (tail of the top 30 = rows 21-30)
# nlargest needs numeric or datetime columns, so convert the text date first
df2 = df.assign(day=pd.to_datetime(df["created_at"]))
nl = df2.nlargest(30, ["day", "order_id"]).tail(10)
print("nlargest(30, ['day','order_id']).tail(10):", nl["order_id"].tolist())
try:
    df.nlargest(3, "created_at")
except TypeError as e:
    print("nlargest on a text column ->", type(e).__name__, e)

assert [r[0] for r in r3] == pp3["order_id"].tolist() == nl["order_id"].tolist()
assert k_rv == k_or == [r[0] for r in con.execute(page2)] == ordered.iloc[10:20]["order_id"].tolist()
print("asserts passed (all compared in order, newest first with order_id tie-break)")
```

**Output (my run):**
```text
page 3 (OFFSET 20): [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
page 1: [30, 29, 28, 27, 26, 25, 24, 23, 22, 21]
page 2 after a new order arrived: [21, 20, 19, 18, 17, 16, 15, 14, 13, 12] -> repeats [21] from page 1
created_at-only order, pages of 3 (engine's tie order, not guaranteed): [[29, 30, 27], [28, 25, 26]]
keyset page 2 (row values): [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
keyset page 2 (expanded OR): [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
keyset page 2 after insert: [20, 19, 18, 17, 16, 15, 14, 13, 12, 11]
pandas iloc[20:30]: [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
nlargest(30, ['day','order_id']).tail(10): [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
nlargest on a text column -> TypeError Column 'created_at' has dtype str, cannot use method 'nlargest' with this dtype
asserts passed (all compared in order, newest first with order_id tie-break)
```

**Edge cases:**
- Ties: with `ORDER BY created_at DESC` alone (no `order_id`), the order inside a day is the engine's choice; my run printed pages `[29, 30, 27]` and `[28, 25, 26]`, which is not even consistent within a day, and rows can skip or repeat across pages.
- Inserts or deletes between requests shift OFFSET pages (shown: a repeated row).
- Offset beyond the end returns an empty page.
- Row-value comparison `(a, b) < (x, y)` ran in SQLite 3.45; PostgreSQL and MySQL support it (from memory); SQL Server does not (from memory, not executed). Where it is missing use the expanded form `created_at < ? OR (created_at = ? AND order_id < ?)`, which I also ran.
- Row-value comparison against a NULL key is UNKNOWN; keyset needs non-null sort columns.
- `nlargest` does not work on a text column (my run raised `TypeError`); convert the date first.

**Then explain:**
- **Page 3 of 10:** `LIMIT 10 OFFSET 20`.
- **Why deep pages get slow:** the database still has to produce and discard the first 20 (or 20,000) rows before returning the next 10 (a general statement, not timed here).
- **Why pages shift:** OFFSET counts positions, not rows; a new row at the top moves every later row down by one.
- **Keyset:** remember the last key and ask for rows after it; cost does not grow with page depth when an index matches the sort order (hedged; Part 11), and it is stable under inserts. Its limits: no jumping to page N, and it needs a unique sort key.
- **Standard syntax:** `OFFSET 20 ROWS FETCH NEXT 10 ROWS ONLY` (SQL Server, Oracle 12c+, PostgreSQL), `LIMIT/OFFSET` in SQLite, PostgreSQL, MySQL (from memory, not executed except SQLite).
- **pandas:** `iloc[20:30]` after sorting; `head(30).tail(10)`; `nlargest(30, cols).tail(10)` is the pandas docs' LIMIT/OFFSET idiom.

**Follow-ups:**
- *Does a client see duplicates with keyset pagination?* Not from inserts above the cursor; deletes of the cursor row are fine because you compare on values.
- *How do you show "page 3 of N"?* `COUNT(*)` separately; or avoid the total.
- *Total order needs what?* A unique tie-breaker such as the primary key.

**Common mistakes:**
- `OFFSET` without a unique `ORDER BY`.
- Using `OFFSET` for million-row exports.
- Writing the keyset condition only on `created_at`, which skips tied rows.
- Mixing ascending and descending columns in a row-value comparison (it needs one direction).

### Q23 ⭐⭐ 🟡 GROUP BY ordinals and aliases, and ORDER BY ordinals: write 'SELECT status, COUNT(*) FROM orders GROUP BY 1 ORDER BY 2 DESC' and explain what the numbers mean, which dialects accept aliases in GROUP BY (hedged), why ordinals are fragile when the SELECT list changes, and the style used in team code. Include the pandas equivalent value_counts() and groupby().size().sort_values().
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** `GROUP BY 1 ORDER BY 2 DESC` means group by the first SELECT column and sort by the second; it is a quick shortcut in ad-hoc work, but it silently changes meaning when the SELECT list changes, so team code usually names the columns.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT);
INSERT INTO orders VALUES
 (1,'completed'),(2,'completed'),(3,'completed'),(4,'cancelled'),(5,'cancelled'),
 (6,'refunded'),(7,'pending'),(8,NULL),(9,NULL);
```

**SQL answer:** `q` (ordinals, with a tie-breaker `, 1`) and `q_alias` (names) in the Code block; the assert shows they return the same rows.

**pandas answer:** `value_counts(dropna=False)` and `groupby("status", dropna=False).size()`, each sorted by `n` descending then `status`, as `v` and `g` in the Code block.

**Example:** statuses: completed 3, cancelled 2, NULL 2, refunded 1, pending 1. `GROUP BY 1` groups by `status` (the first SELECT item) and `ORDER BY 2 DESC` sorts by `COUNT(*)`. The result in my run is completed 3, NULL 2, cancelled 2, pending 1, refunded 1. The tie between NULL and cancelled (2 each) and between pending and refunded (1 each) is why I added `, 1` as a tie-breaker; SQLite puts NULL before text in ascending order.

**Code:** run with `python3 -I`.
```python
# GROUP BY / ORDER BY ordinals and aliases (Q23), plus pandas value_counts and groupby().size().
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT);
INSERT INTO orders VALUES
 (1,'completed'),(2,'completed'),(3,'completed'),(4,'cancelled'),(5,'cancelled'),
 (6,'refunded'),(7,'pending'),(8,NULL),(9,NULL);
""")

q = "SELECT status, COUNT(*) AS n FROM orders GROUP BY 1 ORDER BY 2 DESC, 1"
q_alias = "SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY n DESC, status"
print("GROUP BY 1 ORDER BY 2 DESC, 1:", con.execute(q).fetchall())
assert con.execute(q).fetchall() == con.execute(q_alias).fetchall()

# fragility: reorder the SELECT list and the ordinal silently points at another column
frag = "SELECT COUNT(*) AS n, status FROM orders GROUP BY 1 ORDER BY 2"
print("reordered SELECT, ordinals updated by hand (correct):", con.execute("SELECT COUNT(*) AS n, status FROM orders GROUP BY 2 ORDER BY 1 DESC, 2").fetchall())
# someone inserts a column before COUNT(*): ORDER BY 2 now silently sorts by first_id, no error
print("column inserted, ORDER BY 2 left alone (silently wrong):",
      con.execute("SELECT status, MIN(order_id) AS first_id, COUNT(*) AS n FROM orders GROUP BY 1 ORDER BY 2 DESC").fetchall())
try:
    print(con.execute(frag).fetchall())
except sqlite3.Error as e:
    print("reordered SELECT but GROUP BY 1 not updated (column 1 is now COUNT(*)) ->", type(e).__name__, e)
try:
    con.execute("SELECT status, COUNT(*) FROM orders GROUP BY 1 ORDER BY 3")
except sqlite3.Error as e:
    print("ORDER BY 3 with two columns ->", type(e).__name__, e)

# alias in GROUP BY, alias of an expression
q_expr = "SELECT LENGTH(COALESCE(status,'')) AS len, COUNT(*) AS n FROM orders GROUP BY len ORDER BY len"
print("alias of an expression in GROUP BY (SQLite accepts):", con.execute(q_expr).fetchall())

# pandas: three equivalents. value_counts and groupby both drop NaN by default; SQL keeps the NULL group.
orders = pd.read_sql("SELECT * FROM orders", con)
sql_df = pd.read_sql(q, con)
v = (orders["status"].value_counts(dropna=False).rename("n").rename_axis("status").reset_index()
     .sort_values(["n", "status"], ascending=[False, True], na_position="first").reset_index(drop=True))
g = (orders.groupby("status", dropna=False).size().rename("n").reset_index()
     .sort_values(["n", "status"], ascending=[False, True], na_position="first").reset_index(drop=True))
print("value_counts() default (NaN dropped):", orders["status"].value_counts().to_dict())
print("groupby().size() default (NaN dropped):", orders.groupby("status").size().to_dict())
print(g.to_string(index=False))
pd.testing.assert_frame_equal(sql_df, v)
pd.testing.assert_frame_equal(sql_df, g)
print("asserts passed (n DESC, status ASC tie-break; NULL status sorts first inside the tie, as in SQLite)")
```

**Output (my run):**
```text
GROUP BY 1 ORDER BY 2 DESC, 1: [('completed', 3), (None, 2), ('cancelled', 2), ('pending', 1), ('refunded', 1)]
reordered SELECT, ordinals updated by hand (correct): [(3, 'completed'), (2, None), (2, 'cancelled'), (1, 'pending'), (1, 'refunded')]
column inserted, ORDER BY 2 left alone (silently wrong): [(None, 8, 2), ('pending', 7, 1), ('refunded', 6, 1), ('cancelled', 4, 2), ('completed', 1, 3)]
reordered SELECT but GROUP BY 1 not updated (column 1 is now COUNT(*)) -> OperationalError aggregate functions are not allowed in the GROUP BY clause
ORDER BY 3 with two columns -> OperationalError 1st ORDER BY term out of range - should be between 1 and 2
alias of an expression in GROUP BY (SQLite accepts): [(0, 2), (7, 1), (8, 1), (9, 5)]
value_counts() default (NaN dropped): {'completed': 3, 'cancelled': 2, 'refunded': 1, 'pending': 1}
groupby().size() default (NaN dropped): {'cancelled': 2, 'completed': 3, 'pending': 1, 'refunded': 1}
   status  n
completed  3
      NaN  2
cancelled  2
  pending  1
 refunded  1
asserts passed (n DESC, status ASC tie-break; NULL status sorts first inside the tie, as in SQLite)
```

**Edge cases:**
- Fragility, run: if you reorder the SELECT list to `COUNT(*), status` and leave `GROUP BY 1`, SQLite raises `aggregate functions are not allowed in the GROUP BY clause`. If a column is inserted before `COUNT(*)` and `ORDER BY 2` stays, there is no error: my run silently sorted by `MIN(order_id)` instead of the count.
- An ordinal beyond the SELECT list is an error (`1st ORDER BY term out of range`).
- Alias of an expression in GROUP BY: SQLite accepted `GROUP BY len`. Support elsewhere, from memory and not executed: PostgreSQL, MySQL, BigQuery and Snowflake accept aliases (and ordinals) in GROUP BY; SQL Server does not accept an alias or ordinal in GROUP BY (it does in ORDER BY); Oracle's support varies by version. Treat this as a list to verify.
- Ties in `n`: `value_counts` and `sort_values` order of ties is not something to depend on; add the key as a second sort column in both.
- NULLs: SQL keeps the NULL group; `value_counts()` and `groupby().size()` drop NaN by default (the default `value_counts()` printed no NaN entry). I used `dropna=False` to match.

**Then explain:**
- **Ordinals** are 1-based positions in the SELECT list.
- **Fragile:** adding, removing or reordering SELECT columns changes the meaning, sometimes without any error.
- **Team style:** name the columns in `GROUP BY` and `ORDER BY` for production code; ordinals are accepted in exploration. The alias in `ORDER BY` is allowed everywhere, since ORDER BY runs after SELECT.
- **pandas:** `orders["status"].value_counts()` is the one-liner; `groupby("status").size().sort_values(ascending=False)` is the long form and lets you add more keys.

**Follow-ups:**
- *Why can ORDER BY use an alias but WHERE cannot?* ORDER BY is evaluated after SELECT.
- *Does `GROUP BY 1` hurt performance?* No, it is syntax only.
- *How do you break ties in pandas?* `sort_values(["n", "status"], ascending=[False, True])`.

**Common mistakes:**
- Editing the SELECT list and forgetting the ordinals.
- Leaving ties unbroken, then a flaky output order.
- Forgetting that pandas drops the NULL group by default.

### Q24 ⭐⭐ 🟡 Group by a CASE bucket: orders(order_id, customer_id, amount). Bucket orders into 'small' (< 500), 'medium' (500 to 1,999) and 'large' (2,000 or more), count orders and total revenue per bucket, and handle NULL amounts explicitly. Explain why you repeat or wrap the CASE (alias in GROUP BY is not portable), how an empty bucket disappears from the output and how you would show it, and the pandas pd.cut with right=False and observed.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** Wrap the CASE once in a subquery (or repeat it) and GROUP BY the result, with an explicit NULL branch first so a NULL amount gets its own 'unknown' bucket instead of silently landing in 'large'.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL);
INSERT INTO orders VALUES
 (1,1,100),(2,1,499.99),(3,2,500),(4,2,1999.99),(5,3,2000),(6,3,NULL),(7,4,3500);
```

**SQL answer:** Main query is the `sql` variable in the Code block (CASE computed once in a subquery, then `GROUP BY bucket`):

```sql
SELECT bucket, COUNT(*) AS n_orders, SUM(amount) AS revenue
FROM (SELECT amount,
             CASE WHEN amount IS NULL THEN 'unknown'
                  WHEN amount < 500   THEN 'small'
                  WHEN amount < 2000  THEN 'medium'
                  ELSE 'large' END AS bucket
      FROM orders) t
GROUP BY bucket
ORDER BY bucket
```

The code also runs the repeated-CASE form and the alias-in-GROUP-BY form and asserts all three give the same rows. To show an empty bucket, the code drives the query from a list of bucket names with a LEFT JOIN (the `fix_sql` variable).

**pandas answer:** `pd.cut(orders["amount"], bins=[-np.inf, 500, 2000, np.inf], right=False, labels=labels)` builds left-closed buckets [-inf,500), [500,2000), [2000,inf). NaN stays NaN, so I add an 'unknown' category and `fillna` it. Then `groupby("bucket", observed=True)` with `size` and `sum(min_count=1)`. For the empty-bucket report I use `observed=False`.

**Example:** Orders 1 to 7 have amounts 100, 499.99, 500, 1999.99, 2000, NULL, 3500. Small (< 500): orders 1 and 2, 2 orders, 599.99. Medium (500 to 1,999.99): orders 3 and 4, 2 orders, 2499.99. Large (>= 2000): orders 5 and 7, 2 orders, 5500.00. Order 6 is NULL, so 'unknown', 1 order, revenue NULL. The boundary values 500 and 2000 go to the higher bucket because the tests use `<`. Now filter to customer 1 only: orders 1 and 2 are small, so a plain GROUP BY returns one row, and medium, large and unknown vanish. The LEFT JOIN from a bucket list gives four rows with counts 0 and revenue NULL.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL);
INSERT INTO orders VALUES
 (1,1,100),(2,1,499.99),(3,2,500),(4,2,1999.99),(5,3,2000),(6,3,NULL),(7,4,3500);
""")
orders = pd.read_sql_query("SELECT * FROM orders", con)

# SQL answer: wrap the CASE once in a subquery, then GROUP BY the column (portable).
sql = """
SELECT bucket, COUNT(*) AS n_orders, SUM(amount) AS revenue
FROM (SELECT amount,
             CASE WHEN amount IS NULL THEN 'unknown'
                  WHEN amount < 500   THEN 'small'
                  WHEN amount < 2000  THEN 'medium'
                  ELSE 'large' END AS bucket
      FROM orders) t
GROUP BY bucket
ORDER BY bucket
"""
sql_df = pd.read_sql_query(sql, con)

# Same thing with the CASE repeated and with the alias in GROUP BY (SQLite accepts both).
case = """CASE WHEN amount IS NULL THEN 'unknown' WHEN amount < 500 THEN 'small'
              WHEN amount < 2000 THEN 'medium' ELSE 'large' END"""
rep = pd.read_sql_query(f"SELECT {case} AS bucket, COUNT(*) AS n_orders, SUM(amount) AS revenue "
                        f"FROM orders GROUP BY {case} ORDER BY bucket", con)
alias = pd.read_sql_query(f"SELECT {case} AS bucket, COUNT(*) AS n_orders, SUM(amount) AS revenue "
                          f"FROM orders GROUP BY bucket ORDER BY bucket", con)

# pandas answer: pd.cut with right=False gives [0,500) [500,2000) [2000,inf); NaN amount -> 'unknown'.
labels = ["small", "medium", "large"]
b = pd.cut(orders["amount"], bins=[-np.inf, 500, 2000, np.inf], right=False, labels=labels)
orders["bucket"] = b.cat.add_categories("unknown").fillna("unknown")
pd_df = (orders.groupby("bucket", observed=True)
               .agg(n_orders=("order_id", "size"), revenue=("amount", lambda s: s.sum(min_count=1)))
               .reset_index())
pd_df["bucket"] = pd_df["bucket"].astype(str)
pd_df = pd_df.sort_values("bucket").reset_index(drop=True)

# Compare after sorting both by bucket name.
for other in (rep, alias, pd_df):
    pd.testing.assert_frame_equal(sql_df, other, check_dtype=False)
print("SQL (wrapped CASE):"); print(sql_df.to_string(index=False))

# Empty bucket: only customer 1's orders -> no 'medium', 'large', 'unknown' rows.
only1 = pd.read_sql_query(f"SELECT {case} AS bucket, COUNT(*) AS n_orders, SUM(amount) AS revenue "
                          f"FROM orders WHERE customer_id = 1 GROUP BY {case}", con)
print("\nCustomer 1 only, plain GROUP BY (empty buckets vanish):"); print(only1.to_string(index=False))

# Fix: drive from a list of buckets and LEFT JOIN.
fix_sql = f"""
SELECT b.bucket, COUNT(o.order_id) AS n_orders, SUM(o.amount) AS revenue
FROM (SELECT 'small' AS bucket UNION ALL SELECT 'medium' UNION ALL SELECT 'large' UNION ALL SELECT 'unknown') b
LEFT JOIN (SELECT order_id, amount, {case} AS bucket FROM orders WHERE customer_id = 1) o
       ON o.bucket = b.bucket
GROUP BY b.bucket
ORDER BY b.bucket
"""
fix_sql_df = pd.read_sql_query(fix_sql, con)
print("\nCustomer 1 only, LEFT JOIN from bucket list:"); print(fix_sql_df.to_string(index=False))

# pandas: observed=False keeps every category, including empty ones.
sub = orders[orders["customer_id"] == 1]
fix_pd = (sub.groupby("bucket", observed=False)
             .agg(n_orders=("order_id", "size"), revenue=("amount", lambda s: s.sum(min_count=1)))
             .reset_index())
fix_pd["bucket"] = fix_pd["bucket"].astype(str)
fix_pd = fix_pd.sort_values("bucket").reset_index(drop=True)
pd.testing.assert_frame_equal(fix_sql_df, fix_pd, check_dtype=False)
print("\npandas observed=False:"); print(fix_pd.to_string(index=False))
print("\nobserved=True on the same data:")
print(sub.groupby("bucket", observed=True).size().to_string())
print("\nplain sum() of the all-NaN 'unknown' bucket in pandas:",
      orders[orders.bucket == "unknown"]["amount"].sum(), "(SQL SUM gives NULL)")
# Trap: no explicit NULL branch -> NULL < 500 is UNKNOWN, so the NULL row falls through to ELSE.
trap = con.execute("""SELECT CASE WHEN amount < 500 THEN 'small' WHEN amount < 2000 THEN 'medium' ELSE 'large' END AS bucket, COUNT(*)
                      FROM orders GROUP BY 1 ORDER BY 1""").fetchall()
print("\nwithout a NULL branch:", trap, "(NULL order silently counted as large)")
print("asserts passed")
```

**Output (my run):**
```text
SQL (wrapped CASE):
 bucket  n_orders  revenue
  large         2  5500.00
 medium         2  2499.99
  small         2   599.99
unknown         1      NaN

Customer 1 only, plain GROUP BY (empty buckets vanish):
bucket  n_orders  revenue
 small         2   599.99

Customer 1 only, LEFT JOIN from bucket list:
 bucket  n_orders  revenue
  large         0      NaN
 medium         0      NaN
  small         2   599.99
unknown         0      NaN

pandas observed=False:
 bucket  n_orders  revenue
  large         0      NaN
 medium         0      NaN
  small         2   599.99
unknown         0      NaN

observed=True on the same data:
bucket
small    2

plain sum() of the all-NaN 'unknown' bucket in pandas: 0.0 (SQL SUM gives NULL)

without a NULL branch: [('large', 3), ('medium', 2), ('small', 2)] (NULL order silently counted as large)
asserts passed
```

**Edge cases:**
- **NULL amount:** `NULL < 500` is UNKNOWN, so without the NULL branch the order falls through to `ELSE 'large'`. The run shows large = 3 instead of 2. This is the silent bug.
- **Boundaries:** use `<` against the next lower bound in a CASE; `BETWEEN 500 AND 2000` would count 2000 in medium and large.
- **All-NULL bucket:** SQL `SUM` is NULL; pandas plain `sum()` gives 0.0. I use `sum(min_count=1)` to match. Wrap in `COALESCE(...,0)` in SQL if the report wants zeros.
- **Empty bucket:** GROUP BY only creates groups from rows that exist. pandas `observed=False` keeps empty categories (count 0, sum NaN with `min_count=1`).
- **pd.cut lower edge:** if the first bin edge is 0, a negative amount becomes NaN and lands in 'unknown'. I use `-np.inf`.

**Then explain:**
- **Alias in GROUP BY:** it ran on SQLite 3.45 here. From memory (not executed here), PostgreSQL and MySQL also accept a select alias in GROUP BY, while SQL Server and Oracle do not. Standard SQL evaluates GROUP BY before SELECT, so the portable forms are the subquery or the repeated CASE. Do not use `GROUP BY 1` in production for the same fragility reason: it breaks when columns are reordered.
- **Why wrapping is nicer:** one copy of the business rule, so the bucket edges cannot drift between SELECT and GROUP BY.
- **Showing empty buckets:** keep the bucket names in a small lookup table (or a `VALUES` or `UNION ALL` list), LEFT JOIN the data to it, and `COUNT(o.order_id)` (not `COUNT(*)`, which would give 1 for the unmatched row).
- **pandas:** `right=False` makes intervals left-closed, matching `< 500`. The default `right=True` would put 500 in small. `observed` only matters for categorical keys; pandas 3 changed its default to True (from the pandas docs, not re-checked by a run of the default), so pass it explicitly.

**Follow-ups:**
- *Why not just `GROUP BY amount`?* That groups by each distinct amount, not by range.
- *How do you order the buckets small, medium, large?* Add a numeric sort key in the subquery (`1,2,3`) and `ORDER BY` it. I sorted alphabetically here only so the pandas and SQL results can be compared.
- *How would this become percent of revenue per bucket?* Divide by `(SELECT SUM(amount) FROM orders)` as in Q26.

**Common mistakes:**
- No NULL branch, so NULL amounts count as 'large'.
- `BETWEEN` on a continuous amount, double counting the edges.
- `GROUP BY alias` in an engine that rejects it.
- `COUNT(*)` after a LEFT JOIN, so empty buckets show 1.
- `pd.cut` with default `right=True`, which moves exact edge values into the lower bucket.

### Q25 ⭐⭐ 🟡 HAVING with several conditions and without GROUP BY: products(product_id, category, price, stock). Return categories with at least 5 products and average price above 1,000, plus the maximum price; then write a query that returns one row only if the whole table has more than 100 products (HAVING without GROUP BY, hedged by dialect). Explain which conditions can go in WHERE for speed, and show the pandas filter after groupby.agg.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** Group by category and put the aggregate conditions in HAVING (`COUNT(*) >= 5 AND AVG(price) > 1000`); without GROUP BY, HAVING treats the whole table as one group and returns one row or none.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, price REAL, stock INTEGER);
INSERT INTO products VALUES
 (1,'Electronics',500,10),(2,'Electronics',1500,0),(3,'Electronics',2500,4),(4,'Electronics',1000,7),(5,'Electronics',1200,2),
 (6,'Books',200,50),(7,'Books',300,40),(8,'Books',250,10),(9,'Books',150,5),(10,'Books',400,0),
 (11,'Toys',5000,3),(12,'Toys',4000,2),(13,'Toys',3000,1),
 (14,'Home',900,5),(15,'Home',1100,5),(16,'Home',1000,5),(17,'Home',1200,5),(18,'Home',800,5),(19,'Home',1000,5);
```

**SQL answer:** Main query is the `sql` variable in the Code block:

```sql
SELECT category, COUNT(*) AS n_products, AVG(price) AS avg_price, MAX(price) AS max_price
FROM products
GROUP BY category
HAVING COUNT(*) >= 5 AND AVG(price) > 1000
ORDER BY category
```

The whole-table check is `SELECT COUNT(*) AS n_products FROM products HAVING COUNT(*) > 100`, run in the code with the limit set to 100 and then 10.

**pandas answer:** `g = products.groupby("category").agg(n_products=..., avg_price=..., max_price=...)` then the filter `g[(g["n_products"] >= 5) & (g["avg_price"] > 1000)]`. The whole-table version is just `len(products) > limit`.

**Example:** Categories: Electronics 5 products, prices 500, 1500, 2500, 1000, 1200, average 1340, max 2500. Books 5 products, average 260. Toys 3 products, average 4000 (fails the count). Home 6 products, average exactly 1000 (fails `> 1000`, which is the boundary case). Only Electronics survives: 5, 1340.0, 2500.0. For the whole table there are 19 products: `HAVING COUNT(*) > 100` returns no rows; `> 10` returns one row with 19.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, price REAL, stock INTEGER);
INSERT INTO products VALUES
 (1,'Electronics',500,10),(2,'Electronics',1500,0),(3,'Electronics',2500,4),(4,'Electronics',1000,7),(5,'Electronics',1200,2),
 (6,'Books',200,50),(7,'Books',300,40),(8,'Books',250,10),(9,'Books',150,5),(10,'Books',400,0),
 (11,'Toys',5000,3),(12,'Toys',4000,2),(13,'Toys',3000,1),
 (14,'Home',900,5),(15,'Home',1100,5),(16,'Home',1000,5),(17,'Home',1200,5),(18,'Home',800,5),(19,'Home',1000,5);
""")
products = pd.read_sql_query("SELECT * FROM products", con)

sql = """
SELECT category, COUNT(*) AS n_products, AVG(price) AS avg_price, MAX(price) AS max_price
FROM products
GROUP BY category
HAVING COUNT(*) >= 5 AND AVG(price) > 1000
ORDER BY category
"""
sql_df = pd.read_sql_query(sql, con)

g = (products.groupby("category")
             .agg(n_products=("product_id", "size"), avg_price=("price", "mean"), max_price=("price", "max")))
pd_df = g[(g["n_products"] >= 5) & (g["avg_price"] > 1000)].reset_index().sort_values("category").reset_index(drop=True)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("categories with >= 5 products and avg price > 1000:"); print(sql_df.to_string(index=False))

print("\nall categories before HAVING:")
print(pd.read_sql_query("SELECT category, COUNT(*) AS n, AVG(price) AS avg_price FROM products GROUP BY category ORDER BY category", con).to_string(index=False))

# HAVING without GROUP BY: the whole table is one group.
for limit in (100, 10):
    q = f"SELECT COUNT(*) AS n_products FROM products HAVING COUNT(*) > {limit}"
    rows = con.execute(q).fetchall()
    pd_rows = [len(products)] if len(products) > limit else []
    assert [r[0] for r in rows] == pd_rows
    print(f"\nHAVING COUNT(*) > {limit} (no GROUP BY) -> {rows}")

# A WHERE that is allowed: row-level filter before grouping (changes the question: only in-stock items).
w = pd.read_sql_query("""SELECT category, COUNT(*) AS n_products, AVG(price) AS avg_price, MAX(price) AS max_price
FROM products WHERE stock > 0 GROUP BY category HAVING COUNT(*) >= 5 AND AVG(price) > 1000 ORDER BY category""", con)
pw = products[products["stock"] > 0].groupby("category").agg(n_products=("product_id", "size"),
        avg_price=("price", "mean"), max_price=("price", "max"))
pw = pw[(pw.n_products >= 5) & (pw.avg_price > 1000)].reset_index()
pd.testing.assert_frame_equal(w, pw, check_dtype=False)
print("\nwith WHERE stock > 0 added:", w.to_dict("records"))
print("asserts passed")
```

**Output (my run):**
```text
categories with >= 5 products and avg price > 1000:
   category  n_products  avg_price  max_price
Electronics           5     1340.0     2500.0

all categories before HAVING:
   category  n  avg_price
      Books  5      260.0
Electronics  5     1340.0
       Home  6     1000.0
       Toys  3     4000.0

HAVING COUNT(*) > 100 (no GROUP BY) -> []

HAVING COUNT(*) > 10 (no GROUP BY) -> [(19,)]

with WHERE stock > 0 added: []
asserts passed
```

**Edge cases:**
- **Boundary:** Home averages exactly 1000, so `> 1000` drops it. A `>=` would keep it.
- **WHERE changes the question:** adding `WHERE stock > 0` removes out-of-stock rows first; Electronics then has 4 products and fails the count, so the result is empty (the run shows this). That is why only row-level conditions that you really mean go in WHERE.
- **NULL price:** `AVG` ignores NULL prices but `COUNT(*)` counts the row; use `COUNT(price)` if the count should mean priced products (not in the sample data).
- **HAVING without GROUP BY:** one group; empty table gives `COUNT(*) = 0`, so a `> 100` test returns no row.

**Then explain:**
- **Aggregate conditions cannot go in WHERE** because WHERE runs before grouping. Count and average conditions must stay in HAVING.
- **Speed:** conditions on plain columns (for example `category <> 'Toys'` or `price > 0`) are better in WHERE: they shrink the rows before they are grouped. A condition on the grouping key written in HAVING is often pushed down by the optimiser, but write it in WHERE so it does not depend on that.
- **HAVING without GROUP BY:** it ran on SQLite 3.45 here. From memory (not executed here): PostgreSQL and MySQL accept it, and older SQLite versions (before 3.39, per my recollection of its release notes) rejected it. Treat it as a niche feature; a plain `SELECT ... WHERE (SELECT COUNT(*) FROM products) > 100` style guard is more portable.
- **pandas:** there is no HAVING; you aggregate first and then filter the result with a boolean mask (parentheses and `&`).

**Follow-ups:**
- *Which rows does HAVING see?* The groups, after aggregation. *WHERE?* Individual rows, before.
- *Can HAVING use a select alias?* SQLite and MySQL allow it, standard SQL and PostgreSQL do not (from memory, not executed here for the non-SQLite engines); repeat the aggregate to be safe.
- *How would you also list the product ids in each category?* That needs a join or window function (Parts 2 and 4).

**Common mistakes:**
- `WHERE COUNT(*) >= 5`, which is an error because aggregates are not allowed in WHERE.
- Putting a row filter such as stock in WHERE and not noticing it changes the counts.
- Using `>` when the brief says at least (`>=`).
- In pandas, `and` instead of `&`, or forgetting the parentheses.

### Q26 ⭐⭐ 🟡 Percentage of total with a scalar subquery: orders(order_id, region, amount). Return each region's revenue and its share of total revenue, rounded to 2 decimals, using (SELECT SUM(amount) FROM orders) as a scalar subquery (subqueries are Part 3; keep it light), explain the integer-division and NULL traps, what happens when a region has NULL amounts, and the pandas version with transform or division by the sum. Note that window functions solve this in Part 5.
**Asked at:** interview-prep guide and platform question bank (StrataScratch, DataLemur style), not a candidate report; product-company data scientist screens
**Say this first (1 line):** Divide each region's SUM by a scalar subquery of the grand total, multiply by 100.0 (not 100) so the division is not integer, and expect a region whose amounts are all NULL to show NULL.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'North',100),(2,'North',200),(3,'North',NULL),
 (4,'South',300),(5,'South',400),
 (6,'East',NULL),
 (7,'West',500);
```

**SQL answer:** Main query is the `sql` variable in the Code block:

```sql
SELECT region,
       SUM(amount) AS revenue,
       ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM orders), 2) AS pct_of_total
FROM orders
GROUP BY region
ORDER BY region
```

**pandas answer:** `rev = orders.groupby("region")["amount"].sum(min_count=1)` then `(100.0 * rev / orders["amount"].sum()).round(2)`. The grand total comes from the column, not from `rev`, so it does not depend on the group sums. `transform("sum")` is shown in the code too; it repeats the region total on every row.

**Example:** Amounts: North 100, 200, NULL; South 300, 400; East NULL; West 500. Total = 100+200+300+400+500 = 1500 (NULLs ignored). North revenue 300, share 300/1500 = 20.00. South 700, 46.67. West 500, 33.33. East has only a NULL, so its SUM is NULL and the share is NULL. The three non-NULL shares add to 100.0 (20 + 46.67 + 33.33).

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'North',100),(2,'North',200),(3,'North',NULL),
 (4,'South',300),(5,'South',400),
 (6,'East',NULL),
 (7,'West',500);
""")
orders = pd.read_sql_query("SELECT * FROM orders", con)

sql = """
SELECT region,
       SUM(amount) AS revenue,
       ROUND(100.0 * SUM(amount) / (SELECT SUM(amount) FROM orders), 2) AS pct_of_total
FROM orders
GROUP BY region
ORDER BY region
"""
sql_df = pd.read_sql_query(sql, con)

# pandas: SUM per region (NaN-only region stays NaN), divided by the grand total.
rev = orders.groupby("region")["amount"].sum(min_count=1)
pd_df = pd.DataFrame({"revenue": rev, "pct_of_total": (100.0 * rev / orders["amount"].sum()).round(2)}).reset_index()
pd_df = pd_df.sort_values("region").reset_index(drop=True)
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
print("SQL result (sorted by region):"); print(sql_df.to_string(index=False))

# Trap 1: integer division. Both sides are INTEGER, so SQLite truncates.
bad = con.execute("SELECT region, SUM(amount) / (SELECT SUM(amount) FROM orders) * 100 FROM orders GROUP BY region ORDER BY region").fetchall()
print("\nInteger division, wrong:", bad)
# Trap 2: dividing by COUNT or SUM of a column with NULLs: the denominator ignores NULL rows.
print("SUM ignores NULL, COUNT(*) does not:", con.execute("SELECT SUM(amount), COUNT(amount), COUNT(*) FROM orders").fetchone())
print("shares of non-NULL regions add to:", round(sql_df["pct_of_total"].sum(), 2))

# pandas transform: repeats the group total on every row.
t = orders.groupby("region")["amount"].transform("sum")
print("\ntransform('sum') for the all-NaN East row:", t[orders.region == "East"].tolist(), "(SQL gives NULL; pandas gives 0.0)")
orders["region_rev"] = t
orders["row_share_of_total"] = (100 * orders["amount"] / orders["amount"].sum()).round(2)
print(orders.to_string(index=False))
print("\nSQLite 1.0/0 ->", con.execute("SELECT 1.0 / 0").fetchone()[0], "(NULL, no error)")
print("asserts passed")
```

**Output (my run):**
```text
SQL result (sorted by region):
region  revenue  pct_of_total
  East      NaN           NaN
 North    300.0         20.00
 South    700.0         46.67
  West    500.0         33.33

Integer division, wrong: [('East', None), ('North', 0), ('South', 0), ('West', 0)]
SUM ignores NULL, COUNT(*) does not: (1500, 5, 7)
shares of non-NULL regions add to: 100.0

transform('sum') for the all-NaN East row: [0.0] (SQL gives NULL; pandas gives 0.0)
 order_id region  amount  region_rev  row_share_of_total
        1  North   100.0       300.0                6.67
        2  North   200.0       300.0               13.33
        3  North     NaN       300.0                 NaN
        4  South   300.0       700.0               20.00
        5  South   400.0       700.0               26.67
        6   East     NaN         0.0                 NaN
        7   West   500.0       500.0               33.33

SQLite 1.0/0 -> None (NULL, no error)
asserts passed
```

**Edge cases:**
- **Integer division:** with an INTEGER column, `SUM(amount) / (SELECT SUM(amount) FROM orders) * 100` gives 0 for North, South and West in SQLite (the run shows it), because 300/1500 is 0 in integer arithmetic. Multiply by `100.0` first, or `CAST(... AS REAL)`.
- **NULL amounts inside a region:** ignored by SUM, so North's revenue is 300 and the shares still add up. The grand total also skips NULLs (SUM 1500, COUNT(amount) 5, COUNT(*) 7), so numerator and denominator stay consistent.
- **All-NULL region:** SUM is NULL, so the share is NULL. Use `COALESCE(SUM(amount), 0)` if the report needs 0.00.
- **Zero or NULL total:** dividing by NULL gives NULL. SQLite returns NULL for `1.0 / 0` (the run shows it); from memory, PostgreSQL raises a division-by-zero error (not executed here), so guard with `NULLIF(total, 0)`.
- **pandas difference:** `transform('sum')` gives 0.0 for the all-NaN East rows, whereas SQL gives NULL; plain `groupby().sum()` has the same default. Use `min_count=1` when NULL matters.

**Then explain:**
- **Scalar subquery:** `(SELECT SUM(amount) FROM orders)` returns one value, so it can sit inside the select list. It is computed once for the query in most engines (not verified here); Part 3 covers subqueries.
- **Rounding:** `ROUND(x, 2)` rounds the display only. The rounded shares may add to 99.99 or 100.01, so say that rounding is cosmetic. In PostgreSQL `ROUND(value, 2)` needs numeric, not double precision (from memory, not executed here), so cast to numeric there.
- **Window alternative:** `SUM(SUM(amount)) OVER ()` gives the total without a subquery; that is Part 5, not run here.
- **pandas:** either divide a group-sum Series by the column total (as in the code) or use `transform` when you want the share on each row of the original frame.

**Follow-ups:**
- *How do you get share per row instead of per region?* Divide `amount` by the total; in pandas `df.amount / df.amount.sum()`.
- *Should the denominator include NULL regions?* Decide explicitly: a NULL region key forms its own group in GROUP BY, so its revenue is already inside the total.
- *What about a filtered total (only paid orders)?* Put the same WHERE inside the subquery as in the outer query, or the percentages will not add to 100.

**Common mistakes:**
- `SUM(amount) / SUM(amount)` with integers, giving 0 or 1.
- Dividing by `COUNT(*)` instead of the sum.
- Different WHERE filters in the outer query and the subquery.
- Expecting rounded shares to add to exactly 100.
- In pandas, believing a NaN-only group sums to NaN; it sums to 0.0 by default.

### Q27 ⭐⭐ 🟡 Simple data-quality checks. For a table customers(customer_id, email, phone, signup_date, city) write queries for: total rows, distinct customer_id (is it really a key?), NULL count and NULL percentage per column, empty strings that should be NULL, min and max signup_date to spot impossible dates, and rows with duplicate emails. Show the pandas equivalents (isna().mean(), nunique, duplicated, describe) and say which checks you would automate.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** Profile the table with a handful of one-line queries: row count versus distinct key, NULL count and percentage per column, empty strings, min and max dates, and duplicate emails; then decide which become automated tests.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER, email TEXT, phone TEXT, signup_date TEXT, city TEXT);
INSERT INTO customers VALUES
 (1,'a@x.com','111','2024-01-05','Pune'),
 (2,'b@x.com',NULL,'2024-02-10','Delhi'),
 (3,'c@x.com','333','2024-03-01','Pune'),
 (3,'c2@x.com','','2024-03-02',NULL),
 (4,NULL,'444','2099-01-01','Delhi'),
 (5,'','555','2024-05-05',''),
 (6,'a@x.com','666','1900-01-01','Mumbai'),
 (7,'A@X.com','777','2024-07-07','Pune');
```

**SQL answer:** The SQL is inside the Code block (each check is one query):

- rows and key: `SELECT COUNT(*), COUNT(DISTINCT customer_id) FROM customers`
- NULL count per column: `SUM(col IS NULL)` for each column (the code builds the select list from the column list); NULL percentage: `ROUND(100.0 * SUM(col IS NULL) / COUNT(*), 1)`
- empty strings: `SUM(col = '')` on the text columns
- date range: `SELECT MIN(signup_date), MAX(signup_date) FROM customers`, plus a WHERE listing dates before 2010-01-01 or after 2026-10-24
- duplicate emails: `GROUP BY email HAVING COUNT(*) > 1`, once exact and once on `LOWER(TRIM(email))`, ignoring NULL and empty emails

`SUM(col IS NULL)` works in SQLite and MySQL because a comparison returns 0 or 1; PostgreSQL needs `SUM(CASE WHEN col IS NULL THEN 1 ELSE 0 END)` or `COUNT(*) - COUNT(col)` (from memory, not executed here). `COUNT(*) - COUNT(col)` is the portable form.

**pandas answer:** `len(df)` and `df["customer_id"].nunique()`; `df.isna().sum()` and `(df.isna().mean() * 100).round(1)`; `(df[txt] == "").sum()`; `df["signup_date"].min()` and `.max()` (or after `pd.to_datetime`); `e.duplicated(keep=False)` for the duplicate emails; `df.describe(include="all")` for a quick profile.

**Example:** The 8 rows have customer ids 1, 2, 3, 3, 4, 5, 6, 7, so there are 8 rows but 7 distinct ids: customer_id is not a key, and id 3 appears twice. One email is NULL (id 4), one phone is NULL (id 2), one city is NULL (the second id 3 row): 1 of 8 is 12.5 percent each; signup_date has no NULLs. Empty strings: email '' (id 5), phone '' (second id 3), city '' (id 5), one each. Dates run from 1900-01-01 (id 6) to 2099-01-01 (id 4): two impossible dates. Emails: 'a@x.com' appears for ids 1 and 6 (exact duplicate, count 2). After lowercasing, 'A@X.com' (id 7) joins them, giving count 3.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER, email TEXT, phone TEXT, signup_date TEXT, city TEXT);
INSERT INTO customers VALUES
 (1,'a@x.com','111','2024-01-05','Pune'),
 (2,'b@x.com',NULL,'2024-02-10','Delhi'),
 (3,'c@x.com','333','2024-03-01','Pune'),
 (3,'c2@x.com','','2024-03-02',NULL),
 (4,NULL,'444','2099-01-01','Delhi'),
 (5,'','555','2024-05-05',''),
 (6,'a@x.com','666','1900-01-01','Mumbai'),
 (7,'A@X.com','777','2024-07-07','Pune');
""")
df = pd.read_sql_query("SELECT * FROM customers", con)
cols = ["customer_id", "email", "phone", "signup_date", "city"]

# 1) rows and key check
n_rows, n_distinct = con.execute("SELECT COUNT(*), COUNT(DISTINCT customer_id) FROM customers").fetchone()
assert (n_rows, n_distinct) == (len(df), df["customer_id"].nunique())
print("rows:", n_rows, "distinct customer_id:", n_distinct, "-> key?", n_rows == n_distinct)
dup_ids = con.execute("SELECT customer_id, COUNT(*) FROM customers GROUP BY customer_id HAVING COUNT(*) > 1").fetchall()
print("duplicate ids:", dup_ids)

# 2) NULL count and NULL percentage per column (one SELECT, built from the column list)
sel = ", ".join(f"SUM({c} IS NULL) AS {c}" for c in cols)
nulls_sql = pd.read_sql_query(f"SELECT {sel} FROM customers", con).iloc[0]
sel_pct = ", ".join(f"ROUND(100.0 * SUM({c} IS NULL) / COUNT(*), 1) AS {c}" for c in cols)
pct_sql = pd.read_sql_query(f"SELECT {sel_pct} FROM customers", con).iloc[0]
pd.testing.assert_series_equal(nulls_sql, df.isna().sum(), check_dtype=False, check_names=False)
pd.testing.assert_series_equal(pct_sql, (df.isna().mean() * 100).round(1), check_dtype=False, check_names=False)
print("\nNULL counts:", nulls_sql.to_dict())
print("NULL pct   :", pct_sql.to_dict())

# 3) empty strings that should be NULL (text columns only)
txt = ["email", "phone", "city"]
sel_e = ", ".join(f"SUM({c} = '') AS {c}" for c in txt)
empty_sql = pd.read_sql_query(f"SELECT {sel_e} FROM customers", con).iloc[0]
empty_pd = (df[txt] == "").sum()
pd.testing.assert_series_equal(empty_sql, empty_pd, check_dtype=False, check_names=False)
print("empty strings:", empty_sql.to_dict())

# 4) min / max signup_date (ISO text sorts correctly) and impossible dates
mn, mx = con.execute("SELECT MIN(signup_date), MAX(signup_date) FROM customers").fetchone()
assert (mn, mx) == (df["signup_date"].min(), df["signup_date"].max())
print("\nmin/max signup_date:", mn, mx)
bad_sql = con.execute("SELECT customer_id, signup_date FROM customers WHERE signup_date < '2010-01-01' OR signup_date > '2026-10-24' ORDER BY customer_id").fetchall()
d = pd.to_datetime(df["signup_date"])
bad_pd = df.loc[(d < "2010-01-01") | (d > "2026-10-24"), ["customer_id", "signup_date"]].sort_values("customer_id")
assert bad_sql == list(bad_pd.itertuples(index=False, name=None))
print("impossible dates:", bad_sql)

# 5) duplicate emails: exact, then normalised (lower + trim); NULL and '' are not real emails
exact = con.execute("SELECT email, COUNT(*) FROM customers WHERE email IS NOT NULL AND email <> '' GROUP BY email HAVING COUNT(*) > 1 ORDER BY email").fetchall()
norm = con.execute("SELECT LOWER(TRIM(email)) AS e, COUNT(*) FROM customers WHERE email IS NOT NULL AND TRIM(email) <> '' GROUP BY e HAVING COUNT(*) > 1 ORDER BY e").fetchall()
e = df["email"].dropna()
e = e[e.str.strip() != ""]
exact_pd = e[e.duplicated(keep=False)].value_counts().sort_index()
norm_pd = e.str.strip().str.lower()
norm_pd = norm_pd[norm_pd.duplicated(keep=False)].value_counts().sort_index()
assert exact == list(exact_pd.items()) and norm == list(norm_pd.items())
print("\nduplicate emails, exact:", exact)
print("duplicate emails, lower/trim:", norm)
print("\ndf.describe(include='all') (first 4 rows):")
print(df.describe(include="all").head(4).to_string())
print("asserts passed")
```

**Output (my run):**
```text
rows: 8 distinct customer_id: 7 -> key? False
duplicate ids: [(3, 2)]

NULL counts: {'customer_id': 0, 'email': 1, 'phone': 1, 'signup_date': 0, 'city': 1}
NULL pct   : {'customer_id': 0.0, 'email': 12.5, 'phone': 12.5, 'signup_date': 0.0, 'city': 12.5}
empty strings: {'email': 1, 'phone': 1, 'city': 1}

min/max signup_date: 1900-01-01 2099-01-01
impossible dates: [(4, '2099-01-01'), (6, '1900-01-01')]

duplicate emails, exact: [('a@x.com', 2)]
duplicate emails, lower/trim: [('a@x.com', 3)]

df.describe(include='all') (first 4 rows):
        customer_id    email phone signup_date  city
count           8.0        7     7           8     7
unique          NaN        6     7           8     4
top             NaN  a@x.com   111  2024-01-05  Pune
freq            NaN        2     1           1     3
asserts passed
```

**Edge cases:**
- **NULL versus empty string:** `email IS NULL` does not catch `''`. Count both, and decide whether `''` should become NULL (`NULLIF(email, '')`).
- **Duplicates differ by case or spaces:** the exact check found 2 but the normalised check found 3.
- **NULLs in duplicate checks:** `GROUP BY email` puts all NULLs in one group, which would be reported as a duplicate; filter NULL and empty out first.
- **Dates as text:** the SQL min and max compare ISO strings, which sort correctly (see Q30). If the column holds mixed formats this check is meaningless; the pandas `pd.to_datetime` step would raise or give NaT.
- **pandas describe:** `describe(include='all')` reports `count` as the non-null count, so email shows 7 of 8 rows. It does not count the empty string as missing.

**Then explain:**
- **Key test:** `COUNT(*) = COUNT(DISTINCT customer_id)`. A NULL id would be skipped by `COUNT(DISTINCT)`, so also check NULLs in the key column.
- **Percentage per column:** NULL percentage = NULLs divided by all rows, not by non-NULL rows.
- **Impossible dates:** min and max reveal sentinel values such as 1900-01-01 or 2099-01-01; compare against a plausible window (business launch date to today).
- **Automate:** key uniqueness, NULL percentage thresholds on required columns, date range, and duplicate count on business keys. Run them on every load and fail or alert on breach. Ad hoc: describe-style profiling and the normalised duplicate search when you first meet a table.
- **Weak spot:** these checks find symptoms, not causes. A 12.5 percent NULL rate may be fine for phone and a bug for email; that needs the data owner.

**Follow-ups:**
- *How would you show the duplicate rows themselves?* Join back on the duplicated key, or in pandas `df[df.duplicated("customer_id", keep=False)]`.
- *How do you keep one row per duplicate?* Window `ROW_NUMBER()` (Part 4) or pandas `drop_duplicates`.
- *Why `keep=False`?* So every member of a duplicate group is flagged, not only the later ones.

**Common mistakes:**
- Testing NULL with `= NULL`.
- Counting NULLs with `COUNT(col)`, which counts non-NULLs.
- Forgetting empty strings and whitespace.
- Treating the NULL group of a `GROUP BY email` as a duplicate email.
- Trusting a column named `_id` to be unique without testing.

### Q28 ⭐⭐ 🟡 Users with several kinds of rows: submissions(user_id, type, created_at) with types such as 'refinance', 'in_school', 'mortgage'. Return users who have both 'refinance' and 'in_school' submissions using GROUP BY and HAVING COUNT(DISTINCT type) = 2 (and a SUM(CASE ...) alternative); explain why WHERE type = 'a' AND type = 'b' returns nothing, and how this changes if one type appears twice for a user. Pandas: groupby with nunique or isin then filter.
**Asked at:** interview-prep guide and platform question bank (StrataScratch, DataLemur style), not a candidate report; product-company data scientist screens
**Say this first (1 line):** Filter to the two types, GROUP BY user and keep `HAVING COUNT(DISTINCT type) = 2`; the WHERE with AND on the same column returns nothing because one row has one type.

**Schema and sample data:**
```sql
CREATE TABLE submissions(user_id INTEGER, type TEXT, created_at TEXT);
INSERT INTO submissions VALUES
 (1,'refinance','2024-01-01'),(1,'in_school','2024-01-02'),
 (2,'refinance','2024-01-03'),(2,'refinance','2024-01-04'),
 (3,'refinance','2024-01-05'),(3,'in_school','2024-01-06'),(3,'mortgage','2024-01-07'),
 (4,'in_school','2024-01-08'),(4,'in_school','2024-01-09'),(4,'refinance','2024-01-10'),
 (5,NULL,'2024-01-11'),(5,'refinance','2024-01-12'),
 (6,'mortgage','2024-01-13');
```

**SQL answer:** Main queries are `q_distinct` and `q_sum` in the Code block:

```sql
SELECT user_id FROM submissions
WHERE type IN ('refinance', 'in_school')
GROUP BY user_id
HAVING COUNT(DISTINCT type) = 2
ORDER BY user_id
```

```sql
SELECT user_id FROM submissions
GROUP BY user_id
HAVING SUM(CASE WHEN type = 'refinance' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN type = 'in_school' THEN 1 ELSE 0 END) > 0
ORDER BY user_id
```

**pandas answer:** `two = sub[sub["type"].isin(["refinance", "in_school"])]`, then `n = two.groupby("user_id")["type"].nunique()` and `n[n == 2]`. A second version builds a set of types per user and tests that both wanted types are in it.

**Example:** Users: 1 has refinance and in_school (qualifies). User 2 has refinance twice (one distinct type). User 3 has refinance, in_school and mortgage (qualifies, because the WHERE removes mortgage before counting). User 4 has in_school twice and refinance (qualifies, 2 distinct types over 3 rows). User 5 has a NULL type and refinance (1 distinct type, NULL not counted). User 6 has mortgage only. Result: users 1, 3, 4.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE submissions(user_id INTEGER, type TEXT, created_at TEXT);
INSERT INTO submissions VALUES
 (1,'refinance','2024-01-01'),(1,'in_school','2024-01-02'),
 (2,'refinance','2024-01-03'),(2,'refinance','2024-01-04'),
 (3,'refinance','2024-01-05'),(3,'in_school','2024-01-06'),(3,'mortgage','2024-01-07'),
 (4,'in_school','2024-01-08'),(4,'in_school','2024-01-09'),(4,'refinance','2024-01-10'),
 (5,NULL,'2024-01-11'),(5,'refinance','2024-01-12'),
 (6,'mortgage','2024-01-13');
""")
sub = pd.read_sql_query("SELECT * FROM submissions", con)

q_distinct = """
SELECT user_id FROM submissions
WHERE type IN ('refinance', 'in_school')
GROUP BY user_id
HAVING COUNT(DISTINCT type) = 2
ORDER BY user_id
"""
q_sum = """
SELECT user_id FROM submissions
GROUP BY user_id
HAVING SUM(CASE WHEN type = 'refinance' THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN type = 'in_school' THEN 1 ELSE 0 END) > 0
ORDER BY user_id
"""
q_wrong_and = "SELECT user_id FROM submissions WHERE type = 'refinance' AND type = 'in_school'"
q_wrong_count = """
SELECT user_id FROM submissions WHERE type IN ('refinance', 'in_school')
GROUP BY user_id HAVING COUNT(*) = 2 ORDER BY user_id
"""
q_no_where = "SELECT user_id FROM submissions GROUP BY user_id HAVING COUNT(DISTINCT type) = 2 ORDER BY user_id"

ids = lambda q: [r[0] for r in con.execute(q).fetchall()]

# pandas: filter to the two types, count distinct types per user
two = sub[sub["type"].isin(["refinance", "in_school"])]
n = two.groupby("user_id")["type"].nunique()
pd_ids = sorted(n[n == 2].index.tolist())
# pandas alternative: set per user and issubset
sets = sub.groupby("user_id")["type"].agg(lambda s: set(s.dropna()))
pd_ids2 = sorted(sets[sets.apply(lambda s: {"refinance", "in_school"} <= s)].index.tolist())

assert ids(q_distinct) == ids(q_sum) == pd_ids == pd_ids2
print("COUNT(DISTINCT) with WHERE IN :", ids(q_distinct))
print("SUM(CASE) alternative         :", ids(q_sum))
print("pandas nunique / set versions :", pd_ids, pd_ids2)
print("\nWHERE type='refinance' AND type='in_school':", ids(q_wrong_and), "(one row has one type)")
print("HAVING COUNT(*) = 2 (wrong)   :", ids(q_wrong_count), "-> user 2 (refinance twice) slips in, user 4 (in_school twice + refinance) is lost")
print("no WHERE, HAVING COUNT(DISTINCT type) = 2:", ids(q_no_where), "-> user 3 (three types) is lost; NULL type is not counted, so user 5 is correctly absent")
print("per-user distinct types (NULL ignored):", sub.groupby("user_id")["type"].nunique().to_dict())
print("asserts passed")
```

**Output (my run):**
```text
COUNT(DISTINCT) with WHERE IN : [1, 3, 4]
SUM(CASE) alternative         : [1, 3, 4]
pandas nunique / set versions : [1, 3, 4] [1, 3, 4]

WHERE type='refinance' AND type='in_school': [] (one row has one type)
HAVING COUNT(*) = 2 (wrong)   : [1, 2, 3] -> user 2 (refinance twice) slips in, user 4 (in_school twice + refinance) is lost
no WHERE, HAVING COUNT(DISTINCT type) = 2: [1, 4] -> user 3 (three types) is lost; NULL type is not counted, so user 5 is correctly absent
per-user distinct types (NULL ignored): {1: 2, 2: 1, 3: 3, 4: 2, 5: 1, 6: 1}
asserts passed
```

**Edge cases:**
- **Repeats:** user 2 has two rows but one type. `HAVING COUNT(*) = 2` wrongly returns user 2 and drops user 4 (the run shows [1, 2, 3]); `COUNT(DISTINCT type)` is the right counter.
- **Extra types:** without the `WHERE type IN (...)` filter, `COUNT(DISTINCT type) = 2` drops user 3, who has three types (the run shows [1, 4]). Either filter first or use `>= 2` plus a specific type check; the SUM(CASE) form needs no filter.
- **NULL type:** `COUNT(DISTINCT type)` ignores NULL, and the SUM(CASE) form counts it as neither type.
- **Why WHERE ... AND fails:** WHERE is evaluated row by row. No single row has `type = 'refinance'` and `type = 'in_school'` at once, so zero rows come back (the run confirms an empty result).

**Then explain:**
- **Two-step logic:** WHERE keeps only rows of interest, GROUP BY makes one group per user, HAVING asks whether the group has both types.
- **SUM(CASE) alternative:** each SUM counts rows of one type, and `> 0` on both means both are present. It needs no WHERE and extends to any mix of conditions, such as one type present and another absent.
- **Self-join or INTERSECT alternative:** possible (Part 2), but the GROUP BY pattern scales better.
- **pandas:** `nunique` ignores NaN by default; the set version is clear to read but slower on large data.

**Follow-ups:**
- *How do you get users with refinance but not in_school?* `SUM(CASE ... = 'refinance') > 0 AND SUM(CASE ... = 'in_school') = 0`.
- *What if it is 'at least two of five types'?* Drop the equality and use `COUNT(DISTINCT type) >= 2` over the filtered rows.
- *How do you return the submission rows of these users?* Join back to the user list (Part 2) or use `user_id IN (subquery)` (Part 3).

**Common mistakes:**
- `WHERE type = 'a' AND type = 'b'`, which can never be true.
- `HAVING COUNT(*) = 2`, which counts repeats.
- `COUNT(DISTINCT type) = 2` without the filter, which drops users with a third type.
- Writing `OR` in WHERE and forgetting the HAVING, which returns users with only one type.

### Q29 ⭐⭐ 🟡 AVG pitfalls: employees(emp_id, dept, salary, bonus). Explain integer AVG truncation in some engines (cast to decimal), NULLs skewing or excluding averages, average of group averages versus overall average (weighted by group size), and AVG(DISTINCT). Give a small numeric example where an average of department averages differs from the company average, and the pandas groupby().mean() versus weighted np.average.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** An average of department averages is not the company average unless the departments are the same size; weight by headcount, remember AVG skips NULL, and cast before dividing if your engine does integer division.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept TEXT, salary INTEGER, bonus INTEGER);
INSERT INTO employees VALUES
 (1,'A',100,10),(2,'A',200,NULL),
 (3,'B',300,NULL),(4,'B',300,20),(5,'B',300,20),(6,'B',600,NULL),
 (7,'C',101,5),(8,'C',102,NULL);
```

**SQL answer:** The queries are inside the Code block: per department, `COUNT(*)`, `AVG(salary)`, `SUM(salary) / COUNT(*)` and `AVG(DISTINCT salary)`; then `SELECT AVG(a) FROM (SELECT AVG(salary) AS a FROM employees GROUP BY dept)` for the average of averages, `SELECT AVG(salary) FROM employees` for the overall one, and `SELECT AVG(bonus), AVG(COALESCE(bonus, 0)) FROM employees` for the NULL case.

**pandas answer:** `emp.groupby("dept")["salary"].mean()` for the department averages; `np.average(pd_dept["avg_salary"], weights=pd_dept["n"])` for the weighted version; `emp["salary"].mean()` for the overall; `emp["bonus"].mean()` versus `emp["bonus"].fillna(0).mean()` for NULLs.

**Example:** Dept A: 2 people, salaries 100 and 200, average 150. Dept B: 4 people, 300, 300, 300, 600, average 375. Dept C: 2 people, 101 and 102, average 101.5. Average of the three averages = (150 + 375 + 101.5) / 3 = 208.833. Company average = (300 + 1500 + 203) / 8 = 250.375. They differ because B has four people and gets the same weight as the two-person departments. Weighted by headcount: (2*150 + 4*375 + 2*101.5) / 8 = 250.375, which matches. Bonus: 4 non-NULL bonuses (10, 20, 20, 5) average 13.75; treating the 4 NULLs as zeros gives 55 / 8 = 6.875. `AVG(DISTINCT salary)` for B is (300 + 600) / 2 = 450, not 375.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept TEXT, salary INTEGER, bonus INTEGER);
INSERT INTO employees VALUES
 (1,'A',100,10),(2,'A',200,NULL),
 (3,'B',300,NULL),(4,'B',300,20),(5,'B',300,20),(6,'B',600,NULL),
 (7,'C',101,5),(8,'C',102,NULL);
""")
emp = pd.read_sql_query("SELECT * FROM employees", con)

per_dept = pd.read_sql_query("""
SELECT dept, COUNT(*) AS n, AVG(salary) AS avg_salary,
       SUM(salary) / COUNT(*) AS int_division,
       AVG(DISTINCT salary) AS avg_distinct
FROM employees GROUP BY dept ORDER BY dept""", con)
print(per_dept.to_string(index=False))

# pandas versions
g = emp.groupby("dept")
pd_dept = pd.DataFrame({"n": g.size(), "avg_salary": g["salary"].mean(),
                        "int_division": g["salary"].sum() // g.size(),
                        "avg_distinct": g["salary"].agg(lambda s: s.drop_duplicates().mean())}).reset_index()
pd.testing.assert_frame_equal(per_dept, pd_dept, check_dtype=False)

# average of group averages vs the overall average
avg_of_avgs = con.execute("SELECT AVG(a) FROM (SELECT AVG(salary) AS a FROM employees GROUP BY dept)").fetchone()[0]
overall = con.execute("SELECT AVG(salary) FROM employees").fetchone()[0]
weighted = np.average(pd_dept["avg_salary"], weights=pd_dept["n"])
assert np.isclose(avg_of_avgs, pd_dept["avg_salary"].mean()) and np.isclose(overall, emp["salary"].mean()) and np.isclose(weighted, overall)
print(f"\naverage of dept averages = {avg_of_avgs:.3f}")
print(f"overall average          = {overall:.3f}")
print(f"np.average(avg, weights=n) = {weighted:.3f}")

# NULL bonus: AVG skips NULL; COALESCE(bonus,0) counts them as zeros
b_skip, b_zero = con.execute("SELECT AVG(bonus), AVG(COALESCE(bonus, 0)) FROM employees").fetchone()
assert np.isclose(b_skip, emp["bonus"].mean()) and np.isclose(b_zero, emp["bonus"].fillna(0).mean())
print(f"\nAVG(bonus) ignores NULL = {b_skip}, AVG(COALESCE(bonus,0)) = {b_zero}")
print("typeof(AVG(int)) in SQLite:", con.execute("SELECT typeof(AVG(salary)) FROM employees").fetchone()[0])
print("CAST to REAL fixes SUM/COUNT:", con.execute("SELECT CAST(SUM(salary) AS REAL) / COUNT(*) FROM employees WHERE dept='C'").fetchone()[0])
print("asserts passed")
```

**Output (my run):**
```text
dept  n  avg_salary  int_division  avg_distinct
   A  2       150.0           150         150.0
   B  4       375.0           375         450.0
   C  2       101.5           101         101.5

average of dept averages = 208.833
overall average          = 250.375
np.average(avg, weights=n) = 250.375

AVG(bonus) ignores NULL = 13.75, AVG(COALESCE(bonus,0)) = 6.875
typeof(AVG(int)) in SQLite: real
CAST to REAL fixes SUM/COUNT: 101.5
asserts passed
```

**Edge cases:**
- **Integer truncation:** in SQLite `AVG` returns a real (the run prints `real`), so `AVG` itself does not truncate here. The truncation shows with manual division: `SUM(salary) / COUNT(*)` for dept C gives 101, not 101.5. From memory (not executed here), SQL Server returns an integer from `AVG` over an integer column, while PostgreSQL and MySQL return numeric or decimal results. The fix is `AVG(CAST(salary AS DECIMAL(12,2)))` or multiply by `1.0`; in SQLite use `CAST(... AS REAL)`.
- **NULLs:** `AVG(bonus)` ignores NULL rows both in the sum and in the count, so it answers 'average among people who have a bonus'. If NULL means no bonus, COALESCE to 0 first. Choose deliberately.
- **Empty or all-NULL group:** AVG is NULL, and pandas gives NaN.
- **AVG(DISTINCT):** de-duplicates values before averaging; B drops from 375 to 450. Rarely what you want.

**Then explain:**
- **Weighted mean:** company average = sum of (department average times headcount) divided by total headcount. The easy mistake is averaging the averages.
- **NULL-aware headcount:** if some salaries were NULL, the weight is the count of non-NULL salaries, not the headcount. That is `COUNT(salary)`, not `COUNT(*)`.
- **pandas:** `groupby().mean()` skips NaN like SQL. `np.average` needs explicit weights; it does not skip NaN, so drop them first.
- **Salary here is toy column data** used only to show the arithmetic.

**Follow-ups:**
- *When do the two averages agree?* When all groups have equal size, or equal averages.
- *How do you get the median?* Not a plain aggregate in SQLite; see the median emulation question in this part.
- *How would you compute the weighted average in one query?* `SUM(avg * n) / SUM(n)`, or simply the overall `AVG`.

**Common mistakes:**
- Averaging the group averages.
- Dividing two integers and getting a truncated result.
- Ignoring NULLs in AVG without saying so.
- Using `COUNT(*)` as a weight when some values are NULL.
- Using `AVG(DISTINCT ...)` by habit.

### Q30 ⭐⭐ 🟡 Date filtering without date functions heavy lifting: orders(order_id, amount, created_at) where created_at is a timestamp. Explain why 'created_at BETWEEN ''2025-01-01'' AND ''2025-01-31''' misses most of 31 January, why the half-open range >= start AND < next_start is safer, how timestamps stored as text sort in SQLite (ISO 8601 strings sort correctly), and the time-zone hazard for 'today' (hedged by engine). Pandas: boolean mask on datetime64 and between(inclusive=...).
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** BETWEEN is inclusive on both ends, and '2025-01-31' means the start of that day, so rows later on 31 January are missed; use `created_at >= '2025-01-01' AND created_at < '2025-02-01'` instead.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER, created_at TEXT);
INSERT INTO orders VALUES
 (1,10,'2024-12-31 23:59:59'),
 (2,20,'2025-01-01 00:00:00'),
 (3,30,'2025-01-15 12:00:00'),
 (4,40,'2025-01-31 00:00:00'),
 (5,50,'2025-01-31 10:30:00'),
 (6,60,'2025-01-31 23:59:59'),
 (7,70,'2025-02-01 00:00:00'),
 (8,80,'2025-01-31 23:59:59.500');
```

**SQL answer:** Three queries are in the Code block:

```sql
SELECT order_id FROM orders WHERE created_at BETWEEN '2025-01-01' AND '2025-01-31' ORDER BY order_id
SELECT order_id FROM orders WHERE created_at >= '2025-01-01' AND created_at < '2025-02-01' ORDER BY order_id
```

The first is the trap, the second is the safe half-open range. The code also runs the 'end of day' variant with `'2025-01-31 23:59:59'`.

**pandas answer:** Convert the text with `pd.to_datetime(..., format="ISO8601")`, then `mask = (o["created_at"] >= start) & (o["created_at"] < nxt)` for the half-open range. `o["created_at"].between("2025-01-01", "2025-01-31")` is inclusive on both ends by default (`inclusive="both"`) and has the same trap; `between(start, nxt, inclusive="left")` is the half-open form.

**Example:** Eight orders: 1 is 2024-12-31 23:59:59; 2 is 2025-01-01 00:00:00; 3 is 15 January noon; 4 is 31 January 00:00:00; 5 is 31 January 10:30; 6 is 31 January 23:59:59; 7 is 1 February 00:00:00; 8 is 31 January 23:59:59.500. January orders should be 2, 3, 4, 5, 6, 8. The text `BETWEEN '2025-01-01' AND '2025-01-31'` returns only 2 and 3: in SQLite the timestamp is a string, and '2025-01-31 00:00:00' sorts after '2025-01-31', so even order 4 is lost. The half-open range returns all six. The 'end of day' trick `BETWEEN ... AND '2025-01-31 23:59:59'` returns 2, 3, 4, 5, 6 and still loses order 8 with its fractional second.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, amount INTEGER, created_at TEXT);
INSERT INTO orders VALUES
 (1,10,'2024-12-31 23:59:59'),
 (2,20,'2025-01-01 00:00:00'),
 (3,30,'2025-01-15 12:00:00'),
 (4,40,'2025-01-31 00:00:00'),
 (5,50,'2025-01-31 10:30:00'),
 (6,60,'2025-01-31 23:59:59'),
 (7,70,'2025-02-01 00:00:00'),
 (8,80,'2025-01-31 23:59:59.500');
""")
o = pd.read_sql_query("SELECT * FROM orders", con)
ids = lambda q: [r[0] for r in con.execute(q).fetchall()]

between = ids("SELECT order_id FROM orders WHERE created_at BETWEEN '2025-01-01' AND '2025-01-31' ORDER BY order_id")
half_open = ids("SELECT order_id FROM orders WHERE created_at >= '2025-01-01' AND created_at < '2025-02-01' ORDER BY order_id")
end_of_day = ids("SELECT order_id FROM orders WHERE created_at BETWEEN '2025-01-01 00:00:00' AND '2025-01-31 23:59:59' ORDER BY order_id")
print("BETWEEN '2025-01-01' AND '2025-01-31'          :", between)
print("half-open  >= '2025-01-01' AND < '2025-02-01'    :", half_open)
print("BETWEEN ... '2025-01-31 23:59:59' (fragile)      :", end_of_day)

# pandas
o["created_at"] = pd.to_datetime(o["created_at"], format="ISO8601")
start, nxt = pd.Timestamp("2025-01-01"), pd.Timestamp("2025-02-01")
mask = (o["created_at"] >= start) & (o["created_at"] < nxt)
pd_half = o.loc[mask, "order_id"].tolist()
pd_between = o.loc[o["created_at"].between("2025-01-01", "2025-01-31"), "order_id"].tolist()
pd_between_left = o.loc[o["created_at"].between(start, nxt, inclusive="left"), "order_id"].tolist()
assert pd_half == half_open == pd_between_left == [2, 3, 4, 5, 6, 8]
assert end_of_day == [2, 3, 4, 5, 6] and half_open == [2, 3, 4, 5, 6, 8]   # the .500 row is lost by the 23:59:59 trick
print("\npandas half-open mask      :", pd_half)
print("pandas between(.., '2025-01-31') both-inclusive:", pd_between, "(string means midnight, so 31 Jan after 00:00 is lost)")
print("pandas between(start, next, inclusive='left')  :", pd_between_left)

# SQLite text sorting: ISO 8601 sorts correctly; other layouts do not
print("\nISO text sorts as dates:", con.execute("SELECT '2025-02-01' > '2025-01-31'").fetchone()[0])
print("DD/MM/YYYY text: is '01/02/2025' (1 Feb) > '31/01/2025' (31 Jan)?", con.execute("SELECT '01/02/2025' > '31/01/2025'").fetchone()[0], "(0 = no, wrong order)")

# Time-zone hazard: stored as UTC, business day is IST (UTC+5:30)
utc = con.execute("""SELECT order_id, created_at, datetime(created_at, '+330 minutes') AS ist,
                            date(created_at) AS utc_day, date(created_at, '+330 minutes') AS ist_day
                     FROM orders WHERE order_id IN (1, 6) ORDER BY order_id""").fetchall()
for r in utc: print(r)
ist = o.set_index("created_at").tz_localize("UTC").tz_convert("Asia/Kolkata")
print("pandas IST day of order 6:", ist.loc[ist.order_id == 6].index[0].date(), "| UTC day:", o.loc[o.order_id == 6, "created_at"].iloc[0].date())
jan_ist_sql = ids("SELECT order_id FROM orders WHERE datetime(created_at,'+330 minutes') >= '2025-01-01 00:00:00' AND datetime(created_at,'+330 minutes') < '2025-02-01 00:00:00' ORDER BY order_id")
jan_ist_pd = ist.loc[(ist.index >= pd.Timestamp("2025-01-01", tz="Asia/Kolkata")) & (ist.index < pd.Timestamp("2025-02-01", tz="Asia/Kolkata")), "order_id"].tolist()
assert jan_ist_sql == sorted(jan_ist_pd)
print("January in IST, SQL and pandas:", jan_ist_sql)
print("asserts passed")
```

**Output (my run):**
```text
BETWEEN '2025-01-01' AND '2025-01-31'          : [2, 3]
half-open  >= '2025-01-01' AND < '2025-02-01'    : [2, 3, 4, 5, 6, 8]
BETWEEN ... '2025-01-31 23:59:59' (fragile)      : [2, 3, 4, 5, 6]

pandas half-open mask      : [2, 3, 4, 5, 6, 8]
pandas between(.., '2025-01-31') both-inclusive: [2, 3, 4] (string means midnight, so 31 Jan after 00:00 is lost)
pandas between(start, next, inclusive='left')  : [2, 3, 4, 5, 6, 8]

ISO text sorts as dates: 1
DD/MM/YYYY text: is '01/02/2025' (1 Feb) > '31/01/2025' (31 Jan)? 0 (0 = no, wrong order)
(1, '2024-12-31 23:59:59', '2025-01-01 05:29:59', '2024-12-31', '2025-01-01')
(6, '2025-01-31 23:59:59', '2025-02-01 05:29:59', '2025-01-31', '2025-02-01')
pandas IST day of order 6: 2025-02-01 | UTC day: 2025-01-31
January in IST, SQL and pandas: [1, 2, 3, 4, 5]
asserts passed
```

**Edge cases:**
- **Engines with real timestamps:** `BETWEEN '2025-01-01' AND '2025-01-31'` converts the date to midnight, so only an exact midnight on 31 January survives; this is the 'misses most of 31 January' case. In SQLite text the whole of 31 January is lost, because a longer string with the same prefix sorts later. pandas shows the midnight version: `between` returned 2, 3, 4, so order 4 is kept but orders 5, 6, 8 are lost.
- **Fractional seconds:** `23:59:59` as an end bound misses `23:59:59.500`.
- **Time zones:** `date(created_at)` is the UTC day. Order 6 at 2025-01-31 23:59:59 UTC is 2025-02-01 05:29:59 in IST (UTC+5:30), so a business day in India is not the UTC day; the run shows both. January in IST then contains orders 1 to 5, not 6 or 8.
- **'Today':** SQLite `'now'` is UTC, and `'localtime'` uses the machine time zone; PostgreSQL `CURRENT_DATE` uses the session time zone and MySQL `CURDATE()` the server time zone (from memory, not executed here). Say which time zone the report uses.
- **Text formats:** ISO 8601 (`YYYY-MM-DD HH:MM:SS`) sorts correctly as text. `DD/MM/YYYY` does not: the run shows `'01/02/2025' > '31/01/2025'` is false.

**Then explain:**
- **Half-open range:** `>= start AND < next_start` works for dates, timestamps, fractional seconds and any precision, and next_start is easy to compute (the first day of the next month).
- **Index use:** comparing the bare column to constants lets an index on `created_at` be used (Part 11); wrapping the column in `date(created_at)` or `DATE(created_at)` generally prevents it.
- **SQLite has no timestamp type:** values are text, real or integer, and the string comparison is what you see here.
- **pandas:** parse to datetime first; compare to `pd.Timestamp`. A date string in `between` means midnight, so the same trap applies.

**Follow-ups:**
- *How do you filter 'last 7 days'?* `created_at >= start_of_today - 7 days AND created_at < start_of_tomorrow`, with the time zone stated.
- *How do you group by month?* Truncate the timestamp (`strftime('%Y-%m', created_at)` in SQLite, `DATE_TRUNC` in PostgreSQL, not executed here), see Part 6.
- *Why not `DATE(created_at) = '2025-01-31'`?* It works but can block index use.

**Common mistakes:**
- `BETWEEN` with a date on a timestamp column.
- `23:59:59` end bounds that lose fractional seconds.
- Mixing UTC storage with local reporting days.
- Storing dates as `DD/MM/YYYY` text and then sorting or filtering them.
- Applying a function to the column in WHERE on a large table.

### Q31 ⭐⭐ 🟡 pandas groupby output shape versus SQL: for orders(region, status, amount) explain as_index=True versus as_index=False, reset_index, sort=True (groups are sorted by default, SQL gives no order without ORDER BY), named aggregation syntax agg(total=('amount','sum'), n=('amount','size')), multiple aggregations per column producing MultiIndex columns, and how to flatten them to a SQL-like table.
**Asked at:** pandas documentation (Comparison with SQL) and prep guides, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Default `groupby` puts the keys in the index and sorts them; `as_index=False` or `reset_index()` gives the flat SQL-like table, and named aggregation (`total=('amount','sum')`) gives clean column names with no MultiIndex.

**Schema and sample data:**
```sql
CREATE TABLE orders(region TEXT, status TEXT, amount REAL);
INSERT INTO orders VALUES
 ('West','paid',100),('East','paid',200),('West','cancelled',50),
 ('East','paid',NULL),('North','paid',300),('West','paid',150);
```

**SQL answer:** The SQL baseline in the Code block (`sql` variable):

```sql
SELECT region, SUM(amount) AS total, COUNT(*) AS n FROM orders GROUP BY region ORDER BY region
```

The `ORDER BY` is what fixes the row order; without it SQL promises none.

**pandas answer:** `df.groupby("region", as_index=False).agg(total=("amount", "sum"), n=("amount", "size"))` is the flat form; the code compares it with `groupby("region").agg(...).reset_index()` and with the SQL result sorted by region.

**Example:** Six orders: West 100, East 200, West 50 (cancelled), East NULL, North 300, West 150. SQL result: East total 200 (the NULL is skipped) with n = 2; North 300, n = 1; West 300, n = 3. In pandas, the default result has `region` as the index name; `as_index=False` makes it a normal column. With `sort=False`, groups appear in first-seen order: West, East, North. With the default, East, North, West.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(region TEXT, status TEXT, amount REAL);
INSERT INTO orders VALUES
 ('West','paid',100),('East','paid',200),('West','cancelled',50),
 ('East','paid',NULL),('North','paid',300),('West','paid',150);
""")
df = pd.read_sql_query("SELECT * FROM orders", con)

sql = "SELECT region, SUM(amount) AS total, COUNT(*) AS n FROM orders GROUP BY region ORDER BY region"
sql_df = pd.read_sql_query(sql, con)

# 1) default: keys become the index, groups sorted
a = df.groupby("region").agg(total=("amount", "sum"), n=("amount", "size"))
print("as_index=True (default): index name =", a.index.name); print(a.to_string())
# 2) as_index=False or reset_index gives a flat SQL-like table
b = df.groupby("region", as_index=False).agg(total=("amount", "sum"), n=("amount", "size"))
c = a.reset_index()
pd.testing.assert_frame_equal(b, c)
pd.testing.assert_frame_equal(sql_df, b, check_dtype=False)   # both sorted by region
print("\nas_index=False columns:", list(b.columns))

# 3) sort=True vs sort=False (first-appearance order); SQL without ORDER BY promises no order at all
unsorted = df.groupby("region", sort=False, as_index=False).agg(total=("amount", "sum"))
print("\nsort=False order:", unsorted["region"].tolist(), "| sort=True order:", b["region"].tolist())

# 4) size vs count with a NULL amount; sum of East skips the NULL
nn = df.groupby("region").agg(size=("amount", "size"), count=("amount", "count"))
print("\nsize counts rows, count skips NaN:"); print(nn.to_string())

# 5) several aggregations on one column -> MultiIndex columns; flatten
m = df.groupby("region").agg({"amount": ["sum", "mean", "max"]})
print("\nMultiIndex columns:", m.columns.tolist())
flat = m.copy(); flat.columns = ["_".join(col) for col in flat.columns]; flat = flat.reset_index()
print("flattened:", list(flat.columns))
named = df.groupby("region", as_index=False).agg(amount_sum=("amount", "sum"), amount_mean=("amount", "mean"), amount_max=("amount", "max"))
pd.testing.assert_frame_equal(flat, named)

# 6) two keys: MultiIndex rows; SQL GROUP BY region, status
two = df.groupby(["region", "status"]).agg(total=("amount", "sum"), n=("amount", "size"))
print("\ntwo keys, index names:", two.index.names); print(two.reset_index().to_string(index=False))
sql2 = pd.read_sql_query("SELECT region, status, SUM(amount) AS total, COUNT(*) AS n FROM orders GROUP BY region, status ORDER BY region, status", con)
pd.testing.assert_frame_equal(sql2, two.reset_index(), check_dtype=False)
print("asserts passed")
```

**Output (my run):**
```text
as_index=True (default): index name = region
        total  n
region          
East    200.0  2
North   300.0  1
West    300.0  3

as_index=False columns: ['region', 'total', 'n']

sort=False order: ['West', 'East', 'North'] | sort=True order: ['East', 'North', 'West']

size counts rows, count skips NaN:
        size  count
region             
East       2      1
North      1      1
West       3      3

MultiIndex columns: [('amount', 'sum'), ('amount', 'mean'), ('amount', 'max')]
flattened: ['region', 'amount_sum', 'amount_mean', 'amount_max']

two keys, index names: ['region', 'status']
region    status  total  n
  East      paid  200.0  2
 North      paid  300.0  1
  West cancelled   50.0  1
  West      paid  250.0  2
asserts passed
```

**Edge cases:**
- **size versus count:** `size` counts rows including NaN (East = 2), `count` counts non-NaN (East = 1). In SQL that is `COUNT(*)` versus `COUNT(amount)`.
- **NaN keys:** `groupby` drops NaN keys by default (`dropna=True`), whereas SQL GROUP BY keeps NULL as one group. Pass `dropna=False` to match SQL.
- **Order:** pandas sorts group keys by default (`sort=True`); SQL gives no order without ORDER BY, and `sort=False` returns first-appearance order, which is not a promise SQL makes either. I compared after sorting by region.
- **Two keys:** `groupby(["region", "status"])` gives a MultiIndex of two levels (index names: region, status); `reset_index()` flattens it.

**Then explain:**
- **as_index=True versus False:** True (default) moves the group keys into the index; False keeps them as columns, like a SQL SELECT. `reset_index()` after the fact is equivalent.
- **Named aggregation:** `agg(total=('amount','sum'), n=('amount','size'))` names the output columns directly. Use it as the default style.
- **Several aggregations per column:** `agg({'amount': ['sum', 'mean', 'max']})` gives MultiIndex columns like `('amount', 'sum')`. Flatten with `['_'.join(c) for c in df.columns]` then `reset_index()`; named aggregation avoids this step (the code asserts both give the same frame).
- **Sort:** pandas sorts keys by default; the SQL has `ORDER BY` only because you wrote it.

**Follow-ups:**
- *How do you sort the result by total descending?* `.sort_values("total", ascending=False)` (SQL `ORDER BY total DESC`).
- *How do you keep a NULL region group?* `groupby(..., dropna=False)`.
- *Can the group key be an expression?* Yes: pass a Series (for example `df.amount // 100`) or use `pd.cut`.

**Common mistakes:**
- Writing a result to CSV with the group key still in the index, so the key column is missing or named oddly.
- Using `count` when `size` is meant (or the reverse).
- Assuming SQL also returns groups sorted.
- Leaving MultiIndex columns and then failing to select `df['amount_sum']`.
- Forgetting that NaN keys vanish in pandas but stay in SQL.

### Q32 ⭐⭐ 🟡 pandas boolean-mask traps against SQL WHERE: explain why df[df.a > 1 and df.b < 5] raises an error, the need for parentheses and & | ~, how NaN behaves in comparisons (False) versus NULL in SQL (UNKNOWN), isin with NaN, between() being inclusive by default, query() with @variable, and chained-assignment and copy-on-write behaviour when you filter then assign (pandas 3). Give a SQL query and the matching mask.
**Asked at:** pandas documentation (Comparison with SQL) and prep guides, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** Python's `and` cannot combine two Series (their truth value is ambiguous), so use `&`, `|`, `~` with each comparison in parentheses; and note that NaN comparisons are False, so `~` flips them to True, unlike SQL where NOT of UNKNOWN is still UNKNOWN and the row is dropped.

**Schema and sample data:**
```sql
CREATE TABLE t(id INTEGER PRIMARY KEY, a REAL, b REAL);
INSERT INTO t VALUES (1,5,1),(2,0,2),(3,NULL,3),(4,7,9),(5,2,NULL);
```

**SQL answer:** SQL used in the Code block:

```sql
SELECT id FROM t WHERE a > 1 AND b < 5
SELECT id FROM t WHERE NOT (a > 1)
SELECT id FROM t WHERE a IN (0, NULL)
SELECT id FROM t WHERE a BETWEEN 2 AND 5
```

**pandas answer:** `mask = (df.a > 1) & (df.b < 5)` then `df[mask]`; for NOT use `~(df.a > 1) & df.a.notna()`; `df.a.between(2, 5)`; `df.query("a > @lo and b < 5")`; `df.loc[df.a > 1, "b"] = 0` for assignment.

**Example:** Table t: ids 1 to 5 with (a, b) = (5, 1), (0, 2), (NULL, 3), (7, 9), (2, NULL). `a > 1 AND b < 5`: row 1 passes; row 4 fails on b; row 5 has b NULL (UNKNOWN); rows 2 and 3 fail or are UNKNOWN on a. Result id 1, and the mask returns the same. `NOT (a > 1)`: SQL returns only id 2 (a = 0). A naive `~(df.a > 1)` returns ids 2 and 3, because NaN > 1 is False and `~False` is True, so the NULL row sneaks in; adding `& df.a.notna()` restores the SQL answer.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3, warnings
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE t(id INTEGER PRIMARY KEY, a REAL, b REAL);
INSERT INTO t VALUES (1,5,1),(2,0,2),(3,NULL,3),(4,7,9),(5,2,NULL);
""")
df = pd.read_sql_query("SELECT * FROM t", con)
ids = lambda q: [r[0] for r in con.execute(q).fetchall()]

# 1) and / or raise
try:
    df[df.a > 1 and df.b < 5]
except Exception as e:
    print("and ->", type(e).__name__, ":", str(e)[:70])
try:
    df[df.a > 1 & df.b < 5]
except Exception as e:
    print("missing parentheses ->", type(e).__name__, ":", str(e)[:70])

# 2) the right mask matches the SQL
sql_ids = ids("SELECT id FROM t WHERE a > 1 AND b < 5 ORDER BY id")
mask = (df.a > 1) & (df.b < 5)
assert sql_ids == df.loc[mask, "id"].tolist()
print("\nWHERE a > 1 AND b < 5 ->", sql_ids, "| mask rows:", df.loc[mask, "id"].tolist())

# 3) NaN is False in a comparison, so ~ flips it to True; SQL NOT(UNKNOWN) is UNKNOWN (row dropped)
sql_not = ids("SELECT id FROM t WHERE NOT (a > 1) ORDER BY id")
pd_not = df.loc[~(df.a > 1), "id"].tolist()
pd_not_ok = df.loc[~(df.a > 1) & df.a.notna(), "id"].tolist()
assert sql_not == pd_not_ok and pd_not != sql_not
print("WHERE NOT (a > 1): SQL", sql_not, "| naive ~mask", pd_not, "| ~mask & a.notna()", pd_not_ok)
print("df.a == np.nan:", (df.a == np.nan).sum(), "rows match; SQL a = NULL also matches 0:", len(ids("SELECT id FROM t WHERE a = NULL")))

# 4) isin with NaN matches NaN, SQL IN (..., NULL) does not
print("\nisin([0, nan]) ids:", df.loc[df.a.isin([0, np.nan]), "id"].tolist(), "| SQL a IN (0, NULL):", ids("SELECT id FROM t WHERE a IN (0, NULL) ORDER BY id"))

# 5) between is inclusive both ends by default, like SQL BETWEEN
sql_b = ids("SELECT id FROM t WHERE a BETWEEN 2 AND 5 ORDER BY id")
assert sql_b == df.loc[df.a.between(2, 5), "id"].tolist()
print("BETWEEN 2 AND 5:", sql_b, "| inclusive='neither':", df.loc[df.a.between(2, 5, inclusive="neither"), "id"].tolist())

# 6) query() with @variable
lo = 1
q = df.query("a > @lo and b < 5")["id"].tolist()
assert q == sql_ids
print("query('a > @lo and b < 5'):", q)

# 7) filter then assign in pandas 3 (copy-on-write): the original never changes
orig = df.copy()
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    df[df.a > 1]["b"] = 0                     # chained assignment: modifies a temporary copy
chained_changed = not df.equals(orig)
print("\nchained df[mask]['b'] = 0 -> original changed?", chained_changed, "| warnings:", [type(x.message).__name__ for x in w])
assert not chained_changed
sub = df[df.a > 1]
sub["flag"] = 1                               # assigning on the filtered frame touches only sub
print("filtered frame has 'flag':", "flag" in sub.columns, "| original has 'flag':", "flag" in df.columns)
df.loc[df.a > 1, "b"] = 0                     # the correct, explicit way
print("df.loc[mask, 'b'] = 0 changed ids:", df.loc[df.b == 0, "id"].tolist(), "(ids 1 and 4 had a > 1; row 5 has a=2 and b NULL -> now 0)")
con.close()
print("asserts passed")
```

**Output (my run):**
```text
and -> ValueError : The truth value of a Series is ambiguous. Use a.empty, a.bool(), a.ite
missing parentheses -> TypeError : Cannot perform 'rand_' with a dtyped [float64] array and scalar of typ

WHERE a > 1 AND b < 5 -> [1] | mask rows: [1]
WHERE NOT (a > 1): SQL [2] | naive ~mask [2, 3] | ~mask & a.notna() [2]
df.a == np.nan: 0 rows match; SQL a = NULL also matches 0: 0

isin([0, nan]) ids: [2, 3] | SQL a IN (0, NULL): [2]
BETWEEN 2 AND 5: [1, 5] | inclusive='neither': []
query('a > @lo and b < 5'): [1]

chained df[mask]['b'] = 0 -> original changed? False | warnings: ['ChainedAssignmentError']
filtered frame has 'flag': True | original has 'flag': False
df.loc[mask, 'b'] = 0 changed ids: [1, 4, 5] (ids 1 and 4 had a > 1; row 5 has a=2 and b NULL -> now 0)
asserts passed
```

**Edge cases:**
- **Errors (from the run):** `df[df.a > 1 and df.b < 5]` raises `ValueError: The truth value of a Series is ambiguous`. Without parentheses `df.a > 1 & df.b < 5` raises a `TypeError`, because `&` binds tighter than `>`.
- **NaN in comparisons:** `NaN == NaN` is False, and `df.a == np.nan` matches 0 rows, just as SQL `a = NULL` matches 0 rows. Use `isna()` and `notna()`.
- **isin with NaN:** `df.a.isin([0, np.nan])` returned ids 2 and 3 (it matches NaN), but SQL `a IN (0, NULL)` returned only id 2, because comparing with NULL is UNKNOWN.
- **between:** inclusive on both ends by default, like SQL BETWEEN (`inclusive='neither'` returned nothing for 2 to 5, since 2 and 5 are the boundary values).
- **Copy-on-write (pandas 3):** the chained `df[df.a > 1]["b"] = 0` emitted `ChainedAssignmentError` and left the original unchanged. Assigning a new column on a filtered frame changes only that frame. Use `.loc[mask, col] = value` to modify the original.
- **query with a variable:** `@lo` refers to a local Python variable.

**Then explain:**
- **Three-valued logic:** SQL keeps rows only when WHERE is TRUE; UNKNOWN is dropped, including under NOT. pandas masks are two-valued, so you must add `notna()` yourself.
- **Precedence:** `&` and `|` bind tighter than comparisons, hence the parentheses.
- **query():** reads like SQL and avoids repeated `df.` prefixes; its `and` keyword is fine there because it is parsed by pandas, not Python.
- **Assignment:** in pandas 3 copy-on-write, a filtered result behaves as a new object; changes to it never propagate. The pre-3 `SettingWithCopyWarning` behaviour is gone (I describe this from the run on 3.0.5; I did not run older versions).

**Follow-ups:**
- *How do you write `a IS NULL OR a > 1`?* `df.a.isna() | (df.a > 1)`.
- *What does `df[df.a > 1].copy()` add under copy-on-write?* Little; it is now mostly explicit intent.
- *`isin` versus `==`?* `isin` for a list of values; chained `|` of `==` is equivalent but longer.

**Common mistakes:**
- `and`, `or`, `not` on Series.
- Missing parentheses around comparisons.
- Using `== np.nan` or `== None` to find missing values.
- `~mask` on a column with NaN without excluding NaN, which differs from SQL NOT.
- Chained assignment `df[mask][col] = x` and expecting the original to change.

### Q33 ⭐⭐ 🟡 Aggregates over an empty set: what do COUNT(*), COUNT(col), SUM, AVG and MAX return when no rows match; why a query with aggregates and no GROUP BY always returns one row while the same query with GROUP BY returns zero rows; how COALESCE(SUM(x),0) fixes a report. Using orders(order_id, customer_id, amount), show the result for a customer with no orders, and compare with pandas sum of an empty Series (0), mean (NaN) and max (NaN).
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** With no matching rows and no GROUP BY, COUNT returns 0 and SUM, AVG, MAX return NULL, in a single row; with GROUP BY there are no groups, so zero rows; COALESCE(SUM(x), 0) turns the NULL into 0.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL);
INSERT INTO orders VALUES (1,1,100),(2,1,250),(3,2,NULL),(4,3,40);
```

**SQL answer:** Queries in the Code block (customer 99 has no orders):

```sql
SELECT COUNT(*), COUNT(amount), SUM(amount), AVG(amount), MAX(amount) FROM orders WHERE customer_id = 99
SELECT customer_id, SUM(amount) FROM orders WHERE customer_id = 99 GROUP BY customer_id
SELECT COALESCE(SUM(amount), 0) AS revenue FROM orders WHERE customer_id = 99
```

**pandas answer:** `s = df.loc[df.customer_id == 99, "amount"]` gives an empty Series; `s.size`, `s.count()`, `s.sum()`, `s.mean()`, `s.max()`. For the grouped case: `df[df.customer_id == 99].groupby("customer_id")["amount"].sum()`.

**Example:** orders has 4 rows: (1, customer 1, 100), (2, customer 1, 250), (3, customer 2, NULL), (4, customer 3, 40). For customer 99 no row matches. The aggregate query returns one row: `(0, 0, None, None, None)`. The GROUP BY version returns `[]`. `COALESCE(SUM(amount), 0)` returns `0`. In pandas the empty Series gives size 0, count 0, sum 0.0, mean NaN, max NaN. A customer who has orders but only a NULL amount (customer 2) gives `(1, 0, None, None, None)` in SQL.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount REAL);
INSERT INTO orders VALUES (1,1,100),(2,1,250),(3,2,NULL),(4,3,40);
""")
df = pd.read_sql_query("SELECT * FROM orders", con)

agg = "COUNT(*), COUNT(amount), SUM(amount), AVG(amount), MAX(amount)"
no_match = con.execute(f"SELECT {agg} FROM orders WHERE customer_id = 99").fetchall()
grouped = con.execute("SELECT customer_id, SUM(amount) FROM orders WHERE customer_id = 99 GROUP BY customer_id").fetchall()
coalesced = con.execute("SELECT COALESCE(SUM(amount), 0) AS revenue FROM orders WHERE customer_id = 99").fetchall()
only_null = con.execute(f"SELECT {agg} FROM orders WHERE customer_id = 2").fetchall()
print("no matching rows, no GROUP BY :", no_match)
print("no matching rows, GROUP BY    :", grouped)
print("COALESCE(SUM(amount), 0)      :", coalesced)
print("customer 2 (one NULL amount)  :", only_null)

# pandas
s = df.loc[df.customer_id == 99, "amount"]
res = (s.size, s.count(), s.sum(), s.mean(), s.max())
print("\npandas empty Series: size, count, sum, mean, max =", res)
assert no_match[0][0] == res[0] and no_match[0][1] == res[1]
assert no_match[0][2] is None and np.isnan(res[3]) and np.isnan(res[4])       # SQL NULL vs pandas NaN
assert res[2] == 0 and coalesced[0][0] == 0                                   # pandas sum is already 0
n = df.loc[df.customer_id == 2, "amount"]
print("pandas all-NaN Series (customer 2): count, sum, sum(min_count=1), mean =", n.count(), n.sum(), n.sum(min_count=1), n.mean())
assert only_null[0][2] is None and n.sum() == 0.0 and np.isnan(n.sum(min_count=1))

# groupby on the empty selection returns no rows, like SQL GROUP BY
e = df[df.customer_id == 99].groupby("customer_id")["amount"].sum()
print("pandas groupby on empty selection:", len(e), "rows,", "SQL:", len(grouped), "rows")
assert len(e) == len(grouped) == 0

# Report that must show every customer, including those with no matching orders
rep = con.execute("""SELECT c, COALESCE(SUM(o.amount), 0) FROM (SELECT 1 AS c UNION ALL SELECT 99) k
                     LEFT JOIN orders o ON o.customer_id = k.c GROUP BY c ORDER BY c""").fetchall()
pd_rep = df.groupby("customer_id")["amount"].sum().reindex([1, 99], fill_value=0).tolist()
assert [r[1] for r in rep] == pd_rep
print("report with a zero row for customer 99:", rep)
print("asserts passed")
```

**Output (my run):**
```text
no matching rows, no GROUP BY : [(0, 0, None, None, None)]
no matching rows, GROUP BY    : []
COALESCE(SUM(amount), 0)      : [(0,)]
customer 2 (one NULL amount)  : [(1, 0, None, None, None)]

pandas empty Series: size, count, sum, mean, max = (0, np.int64(0), np.float64(0.0), nan, nan)
pandas all-NaN Series (customer 2): count, sum, sum(min_count=1), mean = 0 0.0 nan nan
pandas groupby on empty selection: 0 rows, SQL: 0 rows
report with a zero row for customer 99: [(1, 350.0), (99, 0)]
asserts passed
```

**Edge cases:**
- **Empty versus all-NULL:** SQL treats them alike for SUM, AVG and MAX (NULL), but COUNT(*) differs (0 versus 1). In pandas the sum of an all-NaN Series is 0.0, not NaN, unless `min_count=1`; the code shows customer 2 sum 0.0 versus `sum(min_count=1)` NaN.
- **pandas sum of an empty Series is 0.0, not NULL:** a real SQL versus pandas difference. SQL needs COALESCE to reach 0; pandas gives 0.0 by default.
- **Report showing every customer:** a customer with no orders produces no row in a plain grouped query. Build the customer list first and LEFT JOIN orders (Part 2); the code does this with a list of customer ids and shows `(99, 0)`.
- **GROUP BY returning zero rows:** an empty result is not the same as a row of zeros.

**Then explain:**
- **Why one row:** an aggregate without GROUP BY treats the whole (filtered) input as a single group, even if that group is empty. So the result always has exactly one row.
- **Why zero rows with GROUP BY:** groups are formed from existing rows; no rows, no groups.
- **COUNT versus the rest:** COUNT counts rows or non-NULL values, and zero is a valid count. SUM, AVG and MAX have no value to report, so they return NULL.
- **COALESCE:** fixes the display (`0` for revenue). For AVG or MAX, 0 may mislead, so prefer to leave NULL or show 'n/a'.
- **pandas:** `count` 0, `sum` 0.0, `mean` NaN, `max` NaN, matching SQL except for sum.

**Follow-ups:**
- *What does `MAX` of an empty set return in pandas?* NaN in this run (the Series is float). Some dtypes can raise instead; I only ran the float case.
- *How do you get 0 rows when nothing matches, instead of one row of NULLs?* Add GROUP BY or a HAVING on the count (see Q25).
- *Does `SUM` of integers returning NULL break application code?* It can, which is why COALESCE is common.

**Common mistakes:**
- Assuming SUM of nothing is 0 in SQL.
- Expecting a row for a customer with no orders after GROUP BY.
- Using `COALESCE` on AVG and mistaking the 0 for a real average.
- Treating `COUNT(col)` and `COUNT(*)` as the same.
- Believing pandas `sum` gives NaN for empty data; it gives 0.0.

### Q34 ⭐⭐ 🟡 Three ways to count a condition: for orders(order_id, status) count cancelled orders per day with COUNT(CASE WHEN ...), SUM(CASE WHEN ... THEN 1 ELSE 0 END) and the FILTER (WHERE ...) clause (supported in SQLite and PostgreSQL; hedge other engines such as MySQL, which lacks FILTER). Explain which one ignores NULL status and why, and the pandas (status == 'cancelled').sum() and groupby().apply alternatives.
**Asked at:** interview-prep guide and platform question bank (StrataScratch, DataLemur style), not a candidate report; product-company data scientist screens
**Say this first (1 line):** `COUNT(CASE WHEN status = 'cancelled' THEN 1 END)`, `SUM(CASE WHEN ... THEN 1 ELSE 0 END)` and `COUNT(*) FILTER (WHERE status = 'cancelled')` all give the same count, and all treat a NULL status as not cancelled; the one to avoid is `COUNT(CASE ... THEN 1 ELSE 0 END)`, which counts every row.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT);
INSERT INTO orders VALUES
 (1,'cancelled','2025-03-01'),(2,'paid','2025-03-01'),(3,NULL,'2025-03-01'),
 (4,'cancelled','2025-03-02'),(5,'cancelled','2025-03-02'),
 (6,'paid','2025-03-03'),(7,NULL,'2025-03-03');
```

**SQL answer:** Main query is the `sql` variable in the Code block:

```sql
SELECT order_date,
       COUNT(CASE WHEN status = 'cancelled' THEN 1 END)             AS cnt_case,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)        AS sum_case,
       COUNT(*) FILTER (WHERE status = 'cancelled')                 AS cnt_filter,
       COUNT(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)      AS wrong_count_else0,
       SUM(CASE WHEN status <> 'cancelled' THEN 1 ELSE 0 END)       AS not_cancelled,
       SUM(CASE WHEN status = 'cancelled' THEN 1 END)               AS sum_no_else
FROM orders
GROUP BY order_date
ORDER BY order_date
```

The first three count columns are the three methods; the last three are traps shown for contrast.

**pandas answer:** `is_c = df["status"] == "cancelled"` then `is_c.groupby(df["order_date"]).sum()`. Also `df.groupby("order_date").apply(lambda g: (g["status"] == "cancelled").sum(), include_groups=False)` and named aggregation on a helper boolean column.

**Example:** Seven orders over three days. 2025-03-01: cancelled, paid, NULL status, so 1 cancelled out of 3 rows. 2025-03-02: two cancelled. 2025-03-03: paid and NULL, so 0 cancelled. All three methods return 1, 2, 0. The trap `COUNT(CASE ... THEN 1 ELSE 0 END)` returns 3, 2, 2 (every row, because 0 is not NULL). `SUM(CASE ... THEN 1 END)` without ELSE returns 1.0, 2.0 and NULL for the last day.

**Code:** (sqlite3 in-memory plus pandas; the asserts compare the SQL and pandas results after sorting by the group key; run with `python3 -I`)
```python
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, order_date TEXT);
INSERT INTO orders VALUES
 (1,'cancelled','2025-03-01'),(2,'paid','2025-03-01'),(3,NULL,'2025-03-01'),
 (4,'cancelled','2025-03-02'),(5,'cancelled','2025-03-02'),
 (6,'paid','2025-03-03'),(7,NULL,'2025-03-03');
""")
df = pd.read_sql_query("SELECT * FROM orders", con)

sql = """
SELECT order_date,
       COUNT(CASE WHEN status = 'cancelled' THEN 1 END)             AS cnt_case,
       SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)        AS sum_case,
       COUNT(*) FILTER (WHERE status = 'cancelled')                 AS cnt_filter,
       COUNT(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END)      AS wrong_count_else0,
       SUM(CASE WHEN status <> 'cancelled' THEN 1 ELSE 0 END)       AS not_cancelled,
       SUM(CASE WHEN status = 'cancelled' THEN 1 END)               AS sum_no_else
FROM orders
GROUP BY order_date
ORDER BY order_date
"""
sql_df = pd.read_sql_query(sql, con)
print(sql_df.to_string(index=False))
assert (sql_df.cnt_case == sql_df.sum_case).all() and (sql_df.sum_case == sql_df.cnt_filter).all()

# pandas: boolean sum, groupby.apply, and named aggregation on a helper column
is_c = df["status"] == "cancelled"                      # NaN/None == 'cancelled' is False
p1 = is_c.groupby(df["order_date"]).sum()
p2 = df.groupby("order_date").apply(lambda g: (g["status"] == "cancelled").sum(), include_groups=False)
p3 = df.assign(c=is_c).groupby("order_date").agg(cancelled=("c", "sum"))["cancelled"]
for p in (p1, p2, p3):
    assert p.tolist() == sql_df["cnt_case"].tolist()
print("\npandas (status == 'cancelled').groupby(order_date).sum():", p1.to_dict())
print("whole table:", int(is_c.sum()), "cancelled of", len(df))
nc = (df["status"] != "cancelled").groupby(df["order_date"]).sum()
print("pandas != 'cancelled' counts NULL status as True:", nc.to_dict(), "| SQL <> skips NULL:", dict(zip(sql_df.order_date, sql_df.not_cancelled)))
assert nc.tolist() != sql_df["not_cancelled"].tolist()
print("asserts passed")
```

**Output (my run):**
```text
order_date  cnt_case  sum_case  cnt_filter  wrong_count_else0  not_cancelled  sum_no_else
2025-03-01         1         1           1                  3              1          1.0
2025-03-02         2         2           2                  2              0          2.0
2025-03-03         0         0           0                  2              1          NaN

pandas (status == 'cancelled').groupby(order_date).sum(): {'2025-03-01': 1, '2025-03-02': 2, '2025-03-03': 0}
whole table: 3 cancelled of 7
pandas != 'cancelled' counts NULL status as True: {'2025-03-01': 2, '2025-03-02': 0, '2025-03-03': 2} | SQL <> skips NULL: {'2025-03-01': 1, '2025-03-02': 0, '2025-03-03': 1}
asserts passed
```

**Edge cases:**
- **NULL status:** `NULL = 'cancelled'` is UNKNOWN, so CASE falls to the missing or ELSE branch. The row is not counted as cancelled by any of the three methods. The FILTER clause drops UNKNOWN rows as well.
- **Not-cancelled count:** `SUM(CASE WHEN status <> 'cancelled' THEN 1 ELSE 0 END)` ignores NULL status in SQL (the run shows 1, 0, 1), but pandas `status != 'cancelled'` is True for NaN, giving 2, 0, 2. The two disagree unless you add `.notna()`.
- **Day with no cancellations:** `COUNT` and `SUM(... ELSE 0)` return 0; `SUM` without ELSE returns NULL. A day with no rows at all produces no group.
- **Dialects:** FILTER ran on SQLite 3.45. From memory (not executed here), PostgreSQL supports it, MySQL does not, so use the CASE forms there; check other engines' documentation.

**Then explain:**
- **Why COUNT(CASE ... THEN 1 END) works:** CASE returns NULL when there is no ELSE, and COUNT of an expression skips NULL.
- **Why SUM(CASE ... ELSE 0) works:** it adds 1 for matches and 0 otherwise; with no ELSE the sum of nothing is NULL.
- **Which ignores NULL status:** all three ignore it for the equality test. The difference is in the result of an all-miss group (0 for COUNT and SUM with ELSE 0, NULL for SUM without ELSE).
- **Style:** FILTER is the most readable; CASE is the most portable.
- **pandas:** comparing gives a boolean Series, and `sum` counts the True values. `groupby().apply` works but is slower and, is slower than the boolean-sum form. I pass `include_groups=False` in pandas 3 and did not test what happens without it.

**Follow-ups:**
- *How do you compute the cancellation rate per day?* `AVG(CASE WHEN status = 'cancelled' THEN 1.0 ELSE 0 END)`; note that NULL status counts in the denominator.
- *How do you count several statuses in one query?* One conditional aggregate per status in the same SELECT (conditional aggregation, the pivot pattern).
- *Why not `WHERE status = 'cancelled'`?* It drops the other statuses, so you cannot show totals or days with zero cancellations in the same query.

**Common mistakes:**
- `COUNT(CASE WHEN ... THEN 1 ELSE 0 END)`, which counts all rows.
- `SUM(CASE ... THEN 1 END)` with no ELSE and getting NULL for a quiet day.
- Using FILTER on MySQL.
- Expecting `status != 'cancelled'` to behave the same in SQL and pandas.
- `WHERE status = 'cancelled' GROUP BY day`, which hides zero days.

### Q35 ⭐⭐ 🟡 Frequency table of a column: for orders(order_id, status, amount) return each status with its order count and percentage of all orders, most frequent first, keeping NULL status as its own row. Explain GROUP BY plus COUNT(*), the ordering tie-break, and the pandas value_counts(dropna=False, normalize=True) versus groupby().size(), including why value_counts drops NaN by default and how a percentage that must sum to 100 is checked.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** Group by status, count the rows with COUNT(*), divide by the total row count for the percentage, and ORDER BY count descending with the status as a tie-break; GROUP BY keeps NULL as its own row, whereas pandas value_counts silently drops NaN unless you pass dropna=False.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'completed',100),(2,'completed',250),(3,'cancelled',80),
 (4,'shipped',300),(5,'completed',120),(6,'shipped',90),
 (7,NULL,60),(8,'cancelled',45),(9,'completed',200);
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_MAIN
SELECT status,
       COUNT(*) AS n,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 2) AS pct
FROM orders
GROUP BY status
ORDER BY n DESC, status
```
`COUNT(*)` counts rows, so the NULL-status group is counted. The `100.0` forces decimal division (`100 * 4 / 9` with integers would truncate). The denominator is a scalar subquery; a window version (`SUM(COUNT(*)) OVER ()`) exists but belongs to Parts 4 and 5, so I did not run it here.

**pandas answer:** (same text as in the Code block)
```python
freq = (orders["status"].value_counts(dropna=False)
        .rename_axis("status").reset_index(name="n"))
freq["pct"] = (100.0 * freq["n"] / freq["n"].sum()).round(2)
freq = freq.sort_values(["n", "status"], ascending=[False, True],
                        na_position="first").reset_index(drop=True)
```
`value_counts(dropna=False)` gives the counts with NaN kept; I add the percentage from the counts and sort explicitly so ties are deterministic and the NULL position matches SQLite.

**Example:** Nine orders: completed 4, cancelled 2, shipped 2, NULL 1.
- completed: 4 / 9 = 44.44 percent; cancelled and shipped: 2 / 9 = 22.22 each; NULL: 1 / 9 = 11.11.
- Order: completed first (4). cancelled and shipped tie at 2, so the second sort key puts cancelled before shipped (alphabetical). The NULL row has the smallest count so it is last.
- The rounded percentages add to 44.44 + 22.22 + 22.22 + 11.11 = 99.99, not 100. That is rounding, not a bug; the unrounded sum is 100.0 in the run.

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q35: frequency table of orders.status with NULL kept, SQLite vs pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'completed',100),(2,'completed',250),(3,'cancelled',80),
 (4,'shipped',300),(5,'completed',120),(6,'shipped',90),
 (7,NULL,60),(8,'cancelled',45),(9,'completed',200);
"""
SQL_MAIN = """
SELECT status,
       COUNT(*) AS n,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 2) AS pct
FROM orders
GROUP BY status
ORDER BY n DESC, status
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL result:")
print(sql_df)

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
freq = (orders["status"].value_counts(dropna=False)
        .rename_axis("status").reset_index(name="n"))
freq["pct"] = (100.0 * freq["n"] / freq["n"].sum()).round(2)
freq = freq.sort_values(["n", "status"], ascending=[False, True],
                        na_position="first").reset_index(drop=True)
# pd:end
print("\npandas value_counts(dropna=False) + explicit tie-break:")
print(freq)

# Compare: same rows, same order (both already ordered), NULL/NaN status mapped to a marker
def norm(d):
    d = d.copy()
    d["status"] = d["status"].astype(object).where(d["status"].notna(), "<NULL>")
    return d.reset_index(drop=True)
pd.testing.assert_frame_equal(norm(sql_df), norm(freq), check_dtype=False)
print("\nassert: SQL == pandas (compared in the printed order, NULL as '<NULL>')")

# The pandas shortcut: normalize=True gives fractions
vc_norm = orders["status"].value_counts(dropna=False, normalize=True)
print("\nvalue_counts(dropna=False, normalize=True):")
print(vc_norm)

# Default drops NaN: percentages are over the 8 non-null rows only
vc_default = orders["status"].value_counts(normalize=True)
print("\nvalue_counts(normalize=True) default (NaN dropped):")
print(vc_default)
print("sum of default fractions:", vc_default.sum(), "| rows used:", orders["status"].notna().sum(), "of", len(orders))

# groupby route: size() counts every row, dropna=False keeps the NaN key
gb = orders.groupby("status", dropna=False).size()
print("\ngroupby('status', dropna=False).size():")
print(gb)
print("groupby('status').size() default:")
print(orders.groupby("status").size())

# Check that percentages sum to 100: rounded pct can drift, use a tolerance
print("\nsum of rounded pct:", round(freq["pct"].sum(), 2), "| exact sum:", (100.0 * freq["n"] / freq["n"].sum()).sum())
assert abs(freq["pct"].sum() - 100) < 0.02 * len(freq)
assert freq["n"].sum() == len(orders) == 9
print("checks passed: counts add to 9, pct within rounding tolerance of 100")

# Mistake demo: COUNT(status) instead of COUNT(*) reports 0 for the NULL group
print("\nCOUNT(status) per group (mistake):", con.execute(
    "SELECT status, COUNT(status) FROM orders GROUP BY status ORDER BY COUNT(*) DESC, status").fetchall())
print("integer division in SQLite: 100 * 4 / 9 =", con.execute("SELECT 100 * 4 / 9").fetchone()[0], "| 100.0 * 4 / 9 =", con.execute("SELECT 100.0 * 4 / 9").fetchone()[0])
```

**Output (my run):**
```
SQL result:
      status  n    pct
0  completed  4  44.44
1  cancelled  2  22.22
2    shipped  2  22.22
3        NaN  1  11.11

pandas value_counts(dropna=False) + explicit tie-break:
      status  n    pct
0  completed  4  44.44
1  cancelled  2  22.22
2    shipped  2  22.22
3        NaN  1  11.11

assert: SQL == pandas (compared in the printed order, NULL as '<NULL>')

value_counts(dropna=False, normalize=True):
status
completed    0.444444
cancelled    0.222222
shipped      0.222222
NaN          0.111111
Name: proportion, dtype: float64

value_counts(normalize=True) default (NaN dropped):
status
completed    0.50
cancelled    0.25
shipped      0.25
Name: proportion, dtype: float64
sum of default fractions: 1.0 | rows used: 8 of 9

groupby('status', dropna=False).size():
status
cancelled    2
completed    4
shipped      2
NaN          1
dtype: int64
groupby('status').size() default:
status
cancelled    2
completed    4
shipped      2
dtype: int64

sum of rounded pct: 99.99 | exact sum: 100.0
checks passed: counts add to 9, pct within rounding tolerance of 100

COUNT(status) per group (mistake): [('completed', 4), ('cancelled', 2), ('shipped', 2), (None, 0)]
integer division in SQLite: 100 * 4 / 9 = 44 | 100.0 * 4 / 9 = 44.44444444444444
```

**Edge cases:**
- NULL status: its own row in SQL (`GROUP BY` puts all NULLs in one group) and with `dropna=False` in pandas. If a NULL ties with a real value on count, SQLite sorts NULL first in an ascending sort key (seen in this part's Q38 demo); PostgreSQL's documented default is NULLs last for ASC (read on its docs page). Say what you want with an explicit key rather than relying on the engine.
- Ties: cancelled and shipped both have 2. Without a second ORDER BY key the SQL order between them is not guaranteed. In pandas `value_counts` the tie order in my run followed first appearance, but I would not rely on that either; sort explicitly.
- Rounding: displayed percentages may add to 99.99 or 100.01. To show 100 exactly, round all but the largest row and give that row the remainder, or just state the unrounded total in a test.
- Empty table: no groups, so no rows and no division by zero.

**Then explain:**
- **GROUP BY plus COUNT(*)** is the frequency table; `COUNT(*)` counts rows, `COUNT(status)` would skip NULLs and show 0 for the NULL row (see the last line of the output).
- **Percentage** is `100.0 * n / total`; the total comes from a scalar subquery or a window function.
- **Tie-break:** `ORDER BY n DESC, status` makes the order reproducible.
- **pandas:** `value_counts()` is shorthand for `groupby(col).size()` sorted by count; both drop NaN keys by default (`dropna=True`), which is why the default percentages in the output are over 8 rows (50, 25, 25) and quietly hide the missing 9th. Use `dropna=False` to keep NaN.
- **Check that percentages sum to 100:** assert on the unrounded values or with a tolerance, and assert that the counts add to the row count (`n.sum() == len(df)`).

**Follow-ups:**
- *Add a cumulative percentage?* Running total over the sorted rows: window function (Part 5).
- *Percentage within each group instead of overall?* Join to a per-group total or use `SUM(COUNT(*)) OVER (PARTITION BY ...)` (not run here).
- *Show only the top 5 and lump the rest as Other?* A CASE bucket over a ranked list (Parts 3 and 4).

**Common mistakes:**
- Using `COUNT(status)` so the NULL row shows 0, or a denominator of `COUNT(status)` so the percentages are over non-null rows only while the NULL row is also shown.
- Integer division: `100 * COUNT(*) / total` with integer columns truncates (SQLite returned 44 for `100 * 4 / 9` in the run; PostgreSQL behaves the same way, not executed here; see Q10).
- Trusting `value_counts()` defaults and reporting percentages that exclude missing values without saying so.
- Not asserting that the counts add up to the table's row count.

---

### Q36 ⭐ 🟡 ROLLUP, CUBE and GROUPING SETS: for sales(region, product, amount) explain what each produces (subtotals and grand total), how GROUPING() tells a real NULL from a subtotal NULL, and emulate ROLLUP with UNION ALL because SQLite lacks it (label the native syntax 'not executed'; support differs in MySQL WITH ROLLUP, PostgreSQL, SQL Server, BigQuery, Snowflake, hedged). Show a pandas version with groupby plus concat, or pivot_table(margins=True).
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** ROLLUP(a, b) returns the detail rows plus a subtotal per a plus a grand total, CUBE gives every combination, GROUPING SETS lists exactly the groupings you want, and GROUPING(col) tells a subtotal NULL (1) from a real NULL (0); SQLite 3.45 has none of them, so I emulate ROLLUP with UNION ALL and flag columns.

**Schema and sample data:**
```sql
CREATE TABLE sales(region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','A',10),('East','B',20),('East','A',5),
 ('West','A',7),('West','B',15),('West',NULL,3);
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_MAIN
SELECT region, product, SUM(amount) AS total, 0 AS g_region, 0 AS g_product
FROM sales GROUP BY region, product
UNION ALL
SELECT region, NULL, SUM(amount), 0, 1
FROM sales GROUP BY region
UNION ALL
SELECT NULL, NULL, SUM(amount), 1, 1
FROM sales
ORDER BY g_region, region, g_product, product
```
The three SELECTs are the three grouping sets of `ROLLUP(region, product)`: (region, product), (region) and (). `g_region` and `g_product` are literal flags playing the role of `GROUPING()`.

Native syntax, **not executed** (SQLite rejected `ROLLUP`: the first line of the output shows `no such function: ROLLUP`):

```sql
-- not executed here
SELECT region, product, SUM(amount) AS total,
       GROUPING(region) AS g_region, GROUPING(product) AS g_product
FROM sales
GROUP BY ROLLUP (region, product);
-- CUBE (region, product): (region, product), (region), (product), ()
-- GROUPING SETS ((region, product), (region), ()): the same three sets as ROLLUP
```

Dialect support from memory, **not executed here**: PostgreSQL, SQL Server, Oracle, Snowflake and BigQuery accept `GROUP BY ROLLUP(...)`, `CUBE(...)` and `GROUPING SETS(...)` with `GROUPING()`; MySQL uses `GROUP BY a, b WITH ROLLUP` and, to my knowledge, has no CUBE or GROUPING SETS. Check the engine's manual before relying on any of this.

**pandas answer:** (same text as in the Code block)
```python
detail = (sales.groupby(["region", "product"], dropna=False, as_index=False)
          .agg(total=("amount", "sum")).assign(g_region=0, g_product=0))
by_region = (sales.groupby("region", as_index=False).agg(total=("amount", "sum"))
             .assign(product=None, g_region=0, g_product=1))
grand = pd.DataFrame({"region": [None], "product": [None],
                      "total": [sales["amount"].sum()], "g_region": [1], "g_product": [1]})
cols = ["region", "product", "total", "g_region", "g_product"]
rolled = pd.concat([detail[cols], by_region[cols], grand[cols]], ignore_index=True)
rolled = rolled.sort_values(["g_region", "region", "g_product", "product"],
                            na_position="first", kind="stable").reset_index(drop=True)
```
Groupby per grouping set, tag each frame with the flags, `concat`, then sort. `pivot_table(margins=True)` also builds a subtotal layout, but see the surprise in the output: it drops the NaN product group.

**Example:** Six sales rows: East A 10 and 5 (15), East B 20, West A 7, West B 15, West with NULL product 3.
- Detail rows (flags 0,0): East A 15, East B 20, West NULL 3, West A 7, West B 15.
- Region subtotals (flags 0,1): East 35, West 3 + 7 + 15 = 25.
- Grand total (flags 1,1): 35 + 25 = 60.
- The rows (West, NULL, 3) and (West, NULL, 25) both show NULL in product; only `g_product` (0 versus 1) says which is a real NULL and which is a subtotal.

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q36: ROLLUP emulation with UNION ALL in SQLite; pandas groupby+concat and pivot_table(margins=True)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','A',10),('East','B',20),('East','A',5),
 ('West','A',7),('West','B',15),('West',NULL,3);
"""
# Native syntax (NOT executed here, SQLite 3.45 has no ROLLUP): GROUP BY ROLLUP(region, product)
SQL_MAIN = """
SELECT region, product, SUM(amount) AS total, 0 AS g_region, 0 AS g_product
FROM sales GROUP BY region, product
UNION ALL
SELECT region, NULL, SUM(amount), 0, 1
FROM sales GROUP BY region
UNION ALL
SELECT NULL, NULL, SUM(amount), 1, 1
FROM sales
ORDER BY g_region, region, g_product, product
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)

try:
    con.execute("SELECT region, product, SUM(amount) FROM sales GROUP BY ROLLUP(region, product)")
except sqlite3.Error as e:
    print("native ROLLUP in SQLite 3.45 ->", type(e).__name__, ":", e)

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("\nSQL (UNION ALL emulation, g_* = GROUPING() flags):")
print(sql_df)

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
detail = (sales.groupby(["region", "product"], dropna=False, as_index=False)
          .agg(total=("amount", "sum")).assign(g_region=0, g_product=0))
by_region = (sales.groupby("region", as_index=False).agg(total=("amount", "sum"))
             .assign(product=None, g_region=0, g_product=1))
grand = pd.DataFrame({"region": [None], "product": [None],
                      "total": [sales["amount"].sum()], "g_region": [1], "g_product": [1]})
cols = ["region", "product", "total", "g_region", "g_product"]
rolled = pd.concat([detail[cols], by_region[cols], grand[cols]], ignore_index=True)
rolled = rolled.sort_values(["g_region", "region", "g_product", "product"],
                            na_position="first", kind="stable").reset_index(drop=True)
# pd:end
print("\npandas groupby + concat:")
print(rolled)

def norm(d):
    d = d.copy()
    for c in ["region", "product"]:
        d[c] = d[c].astype(object).where(d[c].notna(), "<NULL>")
    d["total"] = d["total"].astype("int64")
    return d.astype({"g_region": "int64", "g_product": "int64"}).reset_index(drop=True)
# Both are compared in their printed order (g_region, region, g_product, product; NULL first as SQLite sorts it)
pd.testing.assert_frame_equal(norm(sql_df), norm(rolled), check_dtype=False)
print("\nassert: SQL emulation == pandas concat (printed order, NULL as '<NULL>')")
print("grand total check:", sales["amount"].sum(), "== sum of region subtotals:", by_region["total"].sum())

# GROUPING() flag is what separates the real NULL product (West, NULL, 3) from the subtotal row (West, NULL, 25)
print("\nreal NULL rows (g_product=0):")
print(sql_df[sql_df["product"].isna() & (sql_df["g_product"] == 0)])

# pivot_table(margins=True): all_ = subtotal labels, but a NaN product is silently dropped from the columns
pt = sales.pivot_table(index="region", columns="product", values="amount", aggfunc="sum", margins=True)
print("\npivot_table(margins=True):")
print(pt)
print("margin 'All' for West:", pt.loc["West", "All"], "| true West total:", int(sales[sales.region == "West"].amount.sum()))

# Why UNION ALL and not UNION: a region whose only product is NULL gives identical detail and subtotal rows if flags are dropped
con.executescript("CREATE TABLE s2(region TEXT, product TEXT, amount INTEGER); INSERT INTO s2 VALUES ('West', NULL, 3);")
no_flags = "SELECT region, product, SUM(amount) FROM s2 GROUP BY region, product {u} SELECT region, NULL, SUM(amount) FROM s2 GROUP BY region"
print("\nUNION ALL without flags:", con.execute(no_flags.format(u="UNION ALL")).fetchall())
print("UNION     without flags:", con.execute(no_flags.format(u="UNION")).fetchall(), "(one row silently lost)")
# Empty table: the grand-total branch has no GROUP BY, so it still returns one row
con.executescript("CREATE TABLE s3(region TEXT, product TEXT, amount INTEGER);")
print("emulated ROLLUP on an empty table:", con.execute(SQL_MAIN.replace("FROM sales", "FROM s3")).fetchall())
```

**Output (my run):**
```
native ROLLUP in SQLite 3.45 -> OperationalError : no such function: ROLLUP

SQL (UNION ALL emulation, g_* = GROUPING() flags):
  region product  total  g_region  g_product
0   East       A     15         0          0
1   East       B     20         0          0
2   East     NaN     35         0          1
3   West     NaN      3         0          0
4   West       A      7         0          0
5   West       B     15         0          0
6   West     NaN     25         0          1
7    NaN     NaN     60         1          1

pandas groupby + concat:
  region product  total  g_region  g_product
0   East       A     15         0          0
1   East       B     20         0          0
2   East    None     35         0          1
3   West     NaN      3         0          0
4   West       A      7         0          0
5   West       B     15         0          0
6   West    None     25         0          1
7   None    None     60         1          1

assert: SQL emulation == pandas concat (printed order, NULL as '<NULL>')
grand total check: 60 == sum of region subtotals: 60

real NULL rows (g_product=0):
  region product  total  g_region  g_product
3   West     NaN      3         0          0

pivot_table(margins=True):
product   A   B  All
region
East     15  20   35
West      7  15   22
All      22  35   57
margin 'All' for West: 22 | true West total: 25

UNION ALL without flags: [('West', None, 3), ('West', None, 3)]
UNION     without flags: [('West', None, 3)] (one row silently lost)
emulated ROLLUP on an empty table: [(None, None, None, 1, 1)]
```

**Edge cases:**
- Real NULL in the data: shown above. `COALESCE(product, 'All')` would merge the two kinds of NULL; use the flag in a CASE instead.
- `UNION ALL`, not `UNION`: with a region whose only product is NULL, detail and subtotal rows can be identical if the flags are dropped, and `UNION` removes one silently (the output shows a row lost).
- Empty table: the grand-total branch has no GROUP BY, so the emulation still returns one row, with NULL total (the output shows it). Native engines may behave differently on empty input; not executed here.
- Ordering: subtotal placement is not defined by ROLLUP itself; sort by the flags as I did.
- `pivot_table(margins=True)` dropped the NaN-product row: West's margin is 22 instead of 25 and the grand total 57 instead of 60.

**Then explain:**
- **ROLLUP** is hierarchical (region, then product within region); the order of the columns matters. **CUBE** is every combination (2^n sets). **GROUPING SETS** is the general form; ROLLUP and CUBE are shorthand for it.
- **GROUPING(col)** is 1 on rows where `col` was aggregated away, 0 otherwise, which is how you label subtotal rows without confusing them with data NULLs.
- **Emulation cost:** one scan per grouping set; native ROLLUP lets the engine do it in one pass (general expectation, not measured here).
- **pandas:** groupby once per level and `concat`, or `pivot_table(..., margins=True)` for a quick cross-tab with 'All' margins. Prefer the explicit concat when NaN keys matter.

**Follow-ups:**
- *How do you get only the subtotals?* Filter on the flags (`WHERE g_product = 1 AND g_region = 0`), or `HAVING GROUPING(product) = 1` natively (not executed).
- *Three levels?* Four UNION ALL branches for ROLLUP(a, b, c); this is why native syntax is worth using where it exists.
- *Pivot layout?* Part 10.

**Common mistakes:**
- Replacing subtotal NULLs with COALESCE and merging them with real NULLs.
- Using `UNION` instead of `UNION ALL`.
- Forgetting that `pivot_table` drops NaN index and column keys, so the margins are wrong when keys are missing.
- Forgetting an ORDER BY: subtotals appear wherever the engine puts them.

---

### Q37 ⭐ 🔴 Dialect trap: bare columns in aggregate queries. In SQLite, SELECT name, MAX(salary) FROM employees returns the name from the max row (a documented special case), MySQL without ONLY_FULL_GROUP_BY returns an arbitrary row, and PostgreSQL errors. Explain this on employees(emp_id, name, dept, salary), what happens on ties, why you should not rely on it, and a portable rewrite. Say what you verified by running SQLite versus what is hedged text.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** In SQLite a bare column next to a lone MAX or MIN takes its value from the row holding the max or min, MySQL without ONLY_FULL_GROUP_BY returns a value from an arbitrary row, and PostgreSQL raises an error; do not rely on it, and use ORDER BY with LIMIT 1 and a tie-break, or filter with a subquery, or join to the grouped maximum.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha','Eng',90),(2,'Ben','Eng',120),(3,'Chitra','Eng',120),
 (4,'Dev','Ops',70),(5,'Esha','Ops',80);
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_BARE
SELECT name, MAX(salary) AS top_salary FROM employees

-- SQL_ONE_ROW
SELECT emp_id, name, salary FROM employees
ORDER BY salary DESC, emp_id
LIMIT 1

-- SQL_ALL_TIES
SELECT emp_id, name, salary FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees)
ORDER BY emp_id

-- SQL_PER_DEPT
SELECT e.dept, e.emp_id, e.name, e.salary
FROM employees e
JOIN (SELECT dept, MAX(salary) AS m FROM employees GROUP BY dept) t
  ON t.dept = e.dept AND t.m = e.salary
ORDER BY e.dept, e.emp_id
```
The first query is the trap (SQLite only). The three after it are portable rewrites: one deterministic row (tie-break on `emp_id`), all tied rows, and the top earner(s) per department via a join to the grouped maximum. The Code block also runs the variants `SQL_BARE_TIE`, `SQL_BARE_TWO`, `SQL_BARE_SUM` and `SQL_BARE_DEPT`.

**pandas answer:** (same text as in the Code block)
```python
one = emp.sort_values(["salary", "emp_id"], ascending=[False, True]).head(1)[["emp_id", "name", "salary"]]
all_ties = emp[emp["salary"] == emp["salary"].max()].sort_values("emp_id")[["emp_id", "name", "salary"]]
per_dept = (emp[emp["salary"] == emp.groupby("dept")["salary"].transform("max")]
            .sort_values(["dept", "emp_id"])[["dept", "emp_id", "name", "salary"]])
```
pandas has no bare-column behaviour: you must choose the row yourself, by `sort_values` plus `head`, by a mask against the max, or per group with `transform('max')`. (`idxmax` is another way to pick one row; not run here.)

**Example:** Employees: Asha 90, Ben 120, Chitra 120 (Eng); Dev 70, Esha 80 (Ops).
- `SELECT name, MAX(salary) FROM employees` returns Ben 120 (the first max row met in the scan).
- Eng only, where Ben and Chitra tie at 120: returns Ben. The same rows inserted in the order Chitra, Ben, Asha (table without an INTEGER PRIMARY KEY, so row order is insert order) returned Chitra. So on ties the winner follows physical scan order, which is not a contract.
- `SELECT name, MAX(salary), MIN(salary)` returned Dev (the MIN row, salary 70): with two competing aggregates the name cannot belong to both rows.
- `SELECT name, SUM(salary)` returned Asha, the first row; SUM has no 'special row' at all.
- Portable: ORDER BY salary DESC, emp_id LIMIT 1 returns Ben deterministically; the subquery form returns Ben and Chitra; the join form returns Ben, Chitra (Eng) and Esha (Ops).

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q37: SQLite bare columns with MAX/MIN; ties; portable rewrites
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha','Eng',90),(2,'Ben','Eng',120),(3,'Chitra','Eng',120),
 (4,'Dev','Ops',70),(5,'Esha','Ops',80);
"""
SQL_BARE = "SELECT name, MAX(salary) AS top_salary FROM employees"
SQL_BARE_TIE = "SELECT name, MAX(salary) FROM employees WHERE dept = 'Eng'"
SQL_BARE_TWO = "SELECT name, MAX(salary), MIN(salary) FROM employees"
SQL_BARE_SUM = "SELECT name, SUM(salary) FROM employees"
SQL_BARE_DEPT = "SELECT dept, name, MAX(salary) AS top_salary FROM employees GROUP BY dept ORDER BY dept"
# Portable rewrites
SQL_ONE_ROW = """
SELECT emp_id, name, salary FROM employees
ORDER BY salary DESC, emp_id
LIMIT 1
"""
SQL_ALL_TIES = """
SELECT emp_id, name, salary FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees)
ORDER BY emp_id
"""
SQL_PER_DEPT = """
SELECT e.dept, e.emp_id, e.name, e.salary
FROM employees e
JOIN (SELECT dept, MAX(salary) AS m FROM employees GROUP BY dept) t
  ON t.dept = e.dept AND t.m = e.salary
ORDER BY e.dept, e.emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)

print("bare name + MAX(salary), whole table:\n", q(SQL_BARE))
print("\nties (Ben and Chitra both 120), Eng only:\n", q(SQL_BARE_TIE))
print("\nbare name + MAX + MIN together (which row does name come from?):\n", q(SQL_BARE_TWO))
print("\nbare name + SUM (no min/max rule applies):\n", q(SQL_BARE_SUM))
print("\nbare name per dept:\n", q(SQL_BARE_DEPT))

print("\nportable: one row, deterministic tie-break:\n", q(SQL_ONE_ROW))
print("\nportable: all tied rows:\n", q(SQL_ALL_TIES))
print("\nportable: top per dept, all ties kept:\n", q(SQL_PER_DEPT))

emp = q("SELECT * FROM employees")
# pd:main
one = emp.sort_values(["salary", "emp_id"], ascending=[False, True]).head(1)[["emp_id", "name", "salary"]]
all_ties = emp[emp["salary"] == emp["salary"].max()].sort_values("emp_id")[["emp_id", "name", "salary"]]
per_dept = (emp[emp["salary"] == emp.groupby("dept")["salary"].transform("max")]
            .sort_values(["dept", "emp_id"])[["dept", "emp_id", "name", "salary"]])
# pd:end
print("\npandas one:\n", one, "\npandas all ties:\n", all_ties, "\npandas per dept:\n", per_dept)
pd.testing.assert_frame_equal(q(SQL_ONE_ROW).reset_index(drop=True), one.reset_index(drop=True))
pd.testing.assert_frame_equal(q(SQL_ALL_TIES).reset_index(drop=True), all_ties.reset_index(drop=True))
pd.testing.assert_frame_equal(q(SQL_PER_DEPT).reset_index(drop=True), per_dept.reset_index(drop=True))
print("\nasserts passed: portable SQL == pandas (compared in printed order)")

# Does the tie winner depend on physical row order? Use a table with no INTEGER PRIMARY KEY (rowid order = insert order).
con2 = sqlite3.connect(":memory:")
con2.executescript("CREATE TABLE employees(emp_id INTEGER, name TEXT, dept TEXT, salary INTEGER);"
                   "INSERT INTO employees VALUES (3,'Chitra','Eng',120),(2,'Ben','Eng',120),(1,'Asha','Eng',90);")
print("\nsame data inserted in a different order, tie query:", con2.execute(SQL_BARE_TIE).fetchall())

# Empty table: a query with aggregates and no GROUP BY still returns one row
con.executescript("CREATE TABLE empty_emp(emp_id INTEGER, name TEXT, salary INTEGER);")
print("bare name + MAX(salary) on an empty table:", con.execute("SELECT name, MAX(salary) FROM empty_emp").fetchall())
```

**Output (my run):**
```
bare name + MAX(salary), whole table:
   name  top_salary
0  Ben         120

ties (Ben and Chitra both 120), Eng only:
   name  MAX(salary)
0  Ben          120

bare name + MAX + MIN together (which row does name come from?):
   name  MAX(salary)  MIN(salary)
0  Dev          120           70

bare name + SUM (no min/max rule applies):
    name  SUM(salary)
0  Asha          480

bare name per dept:
   dept  name  top_salary
0  Eng   Ben         120
1  Ops  Esha          80

portable: one row, deterministic tie-break:
    emp_id name  salary
0       2  Ben     120

portable: all tied rows:
    emp_id    name  salary
0       2     Ben     120
1       3  Chitra     120

portable: top per dept, all ties kept:
   dept  emp_id    name  salary
0  Eng       2     Ben     120
1  Eng       3  Chitra     120
2  Ops       5    Esha      80

pandas one:
    emp_id name  salary
1       2  Ben     120
pandas all ties:
    emp_id    name  salary
1       2     Ben     120
2       3  Chitra     120
pandas per dept:
   dept  emp_id    name  salary
1  Eng       2     Ben     120
2  Eng       3  Chitra     120
4  Ops       5    Esha      80

asserts passed: portable SQL == pandas (compared in printed order)

same data inserted in a different order, tie query: [('Chitra', 120)]
bare name + MAX(salary) on an empty table: [(None, None)]
```

**Edge cases:**
- Ties: one row or all tied rows is a business choice; decide and state it.
- NULL salaries: MAX ignores them; in `ORDER BY salary DESC` SQLite puts NULLs last, so a NULL never wins the LIMIT 1 here. (Other engines differ, see Q14.)
- Empty table: an aggregate query without GROUP BY still returns one row; the output shows `(None, None)`.
- Group-wise: the bare-column trick also works per group in SQLite (Eng Ben, Ops Esha in the output), with the same tie caveat.

**Then explain:**
- **SQLite special case (verified by running, behaviour only):** with exactly one MIN or MAX in the query, bare columns come from the row that supplied the min or max. I observed that; I did not re-open the SQLite documentation page in this session, so the 'documented' part is from the question's premise and my memory.
- **Other engines (hedged, not executed here):** PostgreSQL rejects a non-grouped, non-aggregated column unless it is functionally dependent on the grouping key (see Q18); MySQL with ONLY_FULL_GROUP_BY off (the setting depends on version and configuration) may return a value from an arbitrary row, and newer versions have it on by default.
- **Why not rely on it:** it is SQLite-only, it silently breaks when someone adds a second aggregate, and ties are resolved by scan order.
- **Portable rewrite:** `ORDER BY ... LIMIT 1` for one row, `WHERE salary = (SELECT MAX(salary) ...)` for all ties, a join to the grouped max for per group. Window functions (`ROW_NUMBER`) do the per-group case more cleanly: Part 4, not run here.
- **What I ran versus hedged:** everything about SQLite above (including the tie flip and the MAX+MIN result) was run; PostgreSQL and MySQL behaviour is text from memory.

**Follow-ups:**
- *Why is MAX(salary) alone fine but name not?* Many rows could share the max; a plain aggregate returns one value, a bare column needs a choice of row.
- *Top 3 per department?* Window functions, Part 4.
- *How to catch this in code review?* Turn on strict group-by (ONLY_FULL_GROUP_BY in MySQL; PostgreSQL does it by default) and lint for bare columns.

**Common mistakes:**
- Believing the bare-column result is the same everywhere.
- Adding a MIN next to the MAX and silently changing which row supplies the name.
- Using the join-to-max form and forgetting it returns all ties, so row counts differ from LIMIT 1.
- Assuming a tie winner is stable between runs, loads or index changes.

---

### Q38 ⭐ 🔴 Median and percentile without window functions: employees(emp_id, dept, salary). Explain why AVG and median differ for skewed pay, how PERCENTILE_CONT / PERCENTILE_DISC / MEDIAN exist in some engines but not SQLite (hedged), and emulate the median in SQLite with ORDER BY, LIMIT and OFFSET (odd and even counts, NULLs removed first). Show pandas median(), quantile(interpolation=...) and check the two agree.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** The mean is dragged by outliers while the median is the middle value, so for skewed pay they differ; SQLite has no median function, so sort the non-NULL salaries and take the middle one or two rows with LIMIT and OFFSET, averaging them (LIMIT 2 - n % 2 OFFSET (n - 1) / 2), and compare with pandas median().

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Eng',30),(2,'Eng',32),(3,'Eng',35),(4,'Eng',40),(5,'Eng',300),
 (6,'Ops',20),(7,'Ops',24),(8,'Ops',28),(9,'Ops',100),
 (10,'Ops',NULL);
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_MEDIAN
SELECT AVG(salary) AS median_salary FROM (
  SELECT salary FROM employees
  WHERE salary IS NOT NULL AND dept = :dept
  ORDER BY salary
  LIMIT  2 - (SELECT COUNT(salary) FROM employees WHERE dept = :dept) % 2
  OFFSET (SELECT (COUNT(salary) - 1) / 2 FROM employees WHERE dept = :dept)
)
```
`n` is `COUNT(salary)` (non-NULL only, which is why the NULLs are 'removed first'). Odd n: `LIMIT 1 OFFSET (n-1)/2` is the middle row. Even n: `LIMIT 2 OFFSET (n-1)/2` is the two middle rows and `AVG` of them is the median. `:dept` is a bound parameter.

Native functions, **not executed here** (from memory; check the manuals): PostgreSQL `PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary)` and `PERCENTILE_DISC`; Oracle `MEDIAN(salary)` and `PERCENTILE_CONT`; Snowflake `MEDIAN` and `PERCENTILE_CONT`; SQL Server `PERCENTILE_CONT ... OVER (...)` only as a window function; BigQuery `PERCENTILE_CONT` as an analytic function; MySQL has no median function. `PERCENTILE_CONT` interpolates between the two middle values; `PERCENTILE_DISC` returns an actual value from the data.

**pandas answer:** (same text as in the Code block)
```python
s = emp.loc[emp["dept"] == dept, "salary"]          # median() skips NaN by default
pd_med = s.median()
```
`Series.median()` skips NaN by default. `quantile(0.5, interpolation=...)` shows how the choice of interpolation maps to `PERCENTILE_CONT` (linear) and the discrete flavours (lower, higher, midpoint, nearest).

**Example:** - Eng salaries: 30, 32, 35, 40, 300. Mean = 437 / 5 = 87.4; median is the 3rd value, 35. One outlier (300) pulls the mean to 2.5 times the median.
- Ops salaries: 20, 24, 28, 100 and one NULL. After removing the NULL n = 4 (even): `LIMIT 2 - 0 = 2 OFFSET (4-1)/2 = 1` takes 24 and 28, median 26. The mean is 43.0.
- Unknown dept: n = 0, `OFFSET (0-1)/2 = 0` with no rows, so AVG of nothing is NULL; pandas gives NaN.

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q38: median in SQLite with ORDER BY / LIMIT / OFFSET; pandas median and quantile
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept TEXT, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Eng',30),(2,'Eng',32),(3,'Eng',35),(4,'Eng',40),(5,'Eng',300),
 (6,'Ops',20),(7,'Ops',24),(8,'Ops',28),(9,'Ops',100),
 (10,'Ops',NULL);
"""
# Native (NOT executed, SQLite has none): PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) in PostgreSQL / Oracle / SQL Server (window form);
# MEDIAN(salary) in Oracle, Snowflake, DuckDB; PERCENTILE_DISC likewise.  MySQL has neither.
SQL_MEDIAN = """
SELECT AVG(salary) AS median_salary FROM (
  SELECT salary FROM employees
  WHERE salary IS NOT NULL AND dept = :dept
  ORDER BY salary
  LIMIT  2 - (SELECT COUNT(salary) FROM employees WHERE dept = :dept) % 2
  OFFSET (SELECT (COUNT(salary) - 1) / 2 FROM employees WHERE dept = :dept)
)
"""
SQL_AVG = "SELECT AVG(salary) FROM employees WHERE dept = :dept"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
emp = pd.read_sql_query("SELECT * FROM employees", con)

for dept in ["Eng", "Ops", "None_here"]:
    n = con.execute("SELECT COUNT(salary) FROM employees WHERE dept=?", (dept,)).fetchone()[0]
    sql_med = con.execute(SQL_MEDIAN, {"dept": dept}).fetchone()[0]
    sql_avg = con.execute(SQL_AVG, {"dept": dept}).fetchone()[0]
    # pd:main
    s = emp.loc[emp["dept"] == dept, "salary"]          # median() skips NaN by default
    pd_med = s.median()
    # pd:end
    print(f"{dept:9s} n(non-null)={n}  AVG={sql_avg}  SQL median={sql_med}  pandas median={pd_med}")
    if n == 0:
        assert sql_med is None and pd.isna(pd_med)
    else:
        assert abs(sql_med - pd_med) < 1e-9
print("asserts passed: SQL emulated median == pandas median for each dept, incl. empty set (NULL vs NaN)")

# Even-count behaviour: 'linear' (PERCENTILE_CONT) vs 'lower'/'higher' (PERCENTILE_DISC-style) vs midpoint/nearest
ops = emp.loc[emp["dept"] == "Ops", "salary"]      # 20, 24, 28, 100 (NULL skipped)
print("\nOps salaries (NaN skipped):", sorted(ops.dropna().tolist()))
for how in ["linear", "lower", "higher", "midpoint", "nearest"]:
    print(f"quantile(0.5, interpolation={how!r}) =", ops.quantile(0.5, interpolation=how))
# PERCENTILE_DISC(0.5) returns the first value whose cumulative share >= 50%: the lower middle value for even n
lower_sql = con.execute("""SELECT salary FROM employees WHERE dept='Ops' AND salary IS NOT NULL
                           ORDER BY salary LIMIT 1 OFFSET (SELECT (COUNT(salary)-1)/2 FROM employees WHERE dept='Ops')""").fetchone()[0]
assert lower_sql == ops.quantile(0.5, interpolation="lower") == 24
print("SQLite LIMIT 1 OFFSET (n-1)/2 =", lower_sql, "== quantile(0.5, 'lower') (the PERCENTILE_DISC(0.5) value)")

# Skew: mean vs median for Eng
eng = emp.loc[emp["dept"] == "Eng", "salary"]
print("\nEng mean:", eng.mean(), "| median:", eng.median())

# Mistake demo: forgetting to drop NULLs changes the count used for OFFSET
bad = con.execute("""SELECT AVG(salary) FROM (SELECT salary FROM employees WHERE dept='Ops' ORDER BY salary
                     LIMIT 2 - (SELECT COUNT(*) FROM employees WHERE dept='Ops') % 2
                     OFFSET (SELECT (COUNT(*)-1)/2 FROM employees WHERE dept='Ops'))""").fetchone()[0]
print("Ops median if COUNT(*) and no NULL filter is used (NULL sorts first in SQLite):", bad)
```

**Output (my run):**
```
Eng       n(non-null)=5  AVG=87.4  SQL median=35.0  pandas median=35.0
Ops       n(non-null)=4  AVG=43.0  SQL median=26.0  pandas median=26.0
None_here n(non-null)=0  AVG=None  SQL median=None  pandas median=nan
asserts passed: SQL emulated median == pandas median for each dept, incl. empty set (NULL vs NaN)

Ops salaries (NaN skipped): [20.0, 24.0, 28.0, 100.0]
quantile(0.5, interpolation='linear') = 26.0
quantile(0.5, interpolation='lower') = 24.0
quantile(0.5, interpolation='higher') = 28.0
quantile(0.5, interpolation='midpoint') = 26.0
quantile(0.5, interpolation='nearest') = 28.0
SQLite LIMIT 1 OFFSET (n-1)/2 = 24 == quantile(0.5, 'lower') (the PERCENTILE_DISC(0.5) value)

Eng mean: 87.4 | median: 35.0
Ops median if COUNT(*) and no NULL filter is used (NULL sorts first in SQLite): 24.0
```

**Edge cases:**
- NULLs must be excluded both from the sorted rows and from the count; in the output, using `COUNT(*)` and not filtering NULLs for Ops returns 24.0 instead of 26.0 (NULL sorts first in SQLite and shifts the window).
- Even counts: `PERCENTILE_CONT(0.5)` gives 26 (the average of 24 and 28); a discrete percentile gives 24 (lower) or 28 (higher). pandas `lower` returned 24 and `higher` 28; `nearest` also returned 28 (it resolved the 24-versus-28 tie upward), so do not use it for medians.
- Ties and duplicates do not matter for the median value.
- Empty set: NULL in SQL, NaN in pandas; the assert in the Code block handles that.
- Per-group medians in SQLite without window functions need a correlated subquery or one query per group; windows (Parts 4 and 5) are cleaner (not run here).

**Then explain:**
- **Skew:** the mean uses every value's magnitude; the median uses only rank, so it resists outliers. Report the median (and a few percentiles) for pay.
- **Emulation:** order, skip `(n-1)/2` rows, take 1 or 2 rows, average. All arithmetic is integer, so `(n-1)/2` is a floor.
- **PERCENTILE_DISC(0.5)** is the first value whose cumulative share reaches 50 percent; for even n that is the lower middle value, which matched `quantile(0.5, interpolation='lower')` = 24 in my run.
- **pandas:** `median()` equals `quantile(0.5)` with the default `linear` interpolation.

**Follow-ups:**
- *Median per department?* Windows, or a loop of this query per group; Parts 4 and 5.
- *90th percentile?* Nearest-rank: skip `ceil(0.9 n) - 1` rows and take one; pandas equivalent depends on the interpolation, so say which definition you use (not run here).
- *Approximate quantiles on big data?* APPROX_QUANTILES or t-digest style functions in warehouses (hedged, not executed).

**Common mistakes:**
- Averaging the two middle rows by hand but forgetting to drop NULLs first.
- Using `COUNT(*)` instead of `COUNT(salary)` for n.
- Taking `AVG` of department medians as a company median.
- Calling PERCENTILE_DISC and PERCENTILE_CONT the same thing for an even number of rows.

---

### Q39 ⭐ 🔴 Case, whitespace and collation in filters and grouping: status values 'Completed', 'completed ', 'COMPLETED' in orders(order_id, status). Explain what GROUP BY and DISTINCT do (separate groups), how collation changes equality (case-sensitive in PostgreSQL by default, case-insensitive in MySQL's default collation, BINARY and NOCASE in SQLite; hedged), cleaning with LOWER and TRIM, and the pandas str.strip().str.lower() with value_counts.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** GROUP BY and DISTINCT use the column's collation, and in SQLite's default BINARY collation 'Completed', 'completed ' and 'COMPLETED' are three different values, so they form separate groups; clean with LOWER(TRIM(status)) (and decide which whitespace you strip), or change the collation, then GROUP BY the cleaned expression; in pandas use str.strip().str.lower().value_counts().

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT);
INSERT INTO orders VALUES
 (1,'Completed'),(2,'completed '),(3,'COMPLETED'),(4,'completed'),
 (5,'Completed'),(6,'completed' || char(9)),(7,'cancelled');
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_RAW
SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY status

-- SQL_CLEAN
SELECT LOWER(TRIM(status, ' ' || char(9) || char(10) || char(13))) AS status_clean, COUNT(*) AS n
FROM orders
GROUP BY status_clean
ORDER BY n DESC, status_clean
```
`SQL_RAW` shows the problem; `SQL_CLEAN` fixes it by grouping on the cleaned expression (SQLite allows the alias in GROUP BY; other engines, see Q23, may not, so repeat the expression there). The Code block also runs the collation comparisons.

Dialect notes, **not executed here** (from memory): PostgreSQL string comparison is case-sensitive by default (depends on the collation chosen for the database; case-insensitive options are `citext`, `ILIKE` or `LOWER`); MySQL's default collations are usually case-insensitive and, for most `PAD SPACE` collations, ignore trailing spaces in comparisons; SQL Server's default collation depends on the install and is often case-insensitive. Verify the collation of the actual column.

**pandas answer:** (same text as in the Code block)
```python
clean_counts = (orders["status"].str.strip().str.lower()
                .value_counts().rename_axis("status_clean").reset_index(name="n")
                .sort_values(["n", "status_clean"], ascending=[False, True]).reset_index(drop=True))
```
`str.strip()` and `str.lower()` before `value_counts()`. pandas compares strings exactly (case-sensitive, whitespace-sensitive), like SQLite BINARY.

**Example:** Seven rows: 'Completed' (2), 'completed ' (trailing space), 'COMPLETED', 'completed', 'completed' plus a tab, 'cancelled'.
- Raw `GROUP BY status`: six groups, counts 1 (COMPLETED), 2 (Completed), 1 (cancelled), 1 (completed), 1 (completed with tab), 1 (completed with space); `COUNT(DISTINCT status)` = 6.
- `status = 'completed'` under BINARY matches only order 4. With `COLLATE NOCASE` it matches orders 1, 3, 4, 5 (case ignored, trailing space still counts). With `COLLATE RTRIM` it matches 2 and 4 (trailing spaces ignored, case still counts). `LOWER(TRIM(status))` matches 1 to 5, but not order 6 (the tab).
- Cleaning with space, tab, LF and CR trimmed and lower-cased: completed 6, cancelled 1, identical in pandas.

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q39: case, whitespace and collation in GROUP BY / filters (SQLite BINARY, NOCASE, RTRIM)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT);
INSERT INTO orders VALUES
 (1,'Completed'),(2,'completed '),(3,'COMPLETED'),(4,'completed'),
 (5,'Completed'),(6,'completed' || char(9)),(7,'cancelled');
"""
SQL_RAW = "SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY status"
SQL_DISTINCT = "SELECT COUNT(DISTINCT status) FROM orders"
SQL_CLEAN = """
SELECT LOWER(TRIM(status, ' ' || char(9) || char(10) || char(13))) AS status_clean, COUNT(*) AS n
FROM orders
GROUP BY status_clean
ORDER BY n DESC, status_clean
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)

print("raw GROUP BY (each spelling is its own group; the tab row prints as 'completed' + tab):")
print(q(SQL_RAW).assign(status=lambda d: d["status"].map(repr)))
print("COUNT(DISTINCT status):", con.execute(SQL_DISTINCT).fetchone()[0])

print("\nequality under SQLite collations (rows matching 'completed'):")
for label, cond in [
    ("status = 'completed'                 (BINARY, default)", "status = 'completed'"),
    ("status = 'completed' COLLATE NOCASE", "status = 'completed' COLLATE NOCASE"),
    ("status = 'completed' COLLATE RTRIM", "status = 'completed' COLLATE RTRIM"),
    ("LOWER(TRIM(status)) = 'completed'", "LOWER(TRIM(status)) = 'completed'"),
]:
    ids = [r[0] for r in con.execute(f"SELECT order_id FROM orders WHERE {cond} ORDER BY order_id")]
    print(f"  {label:55s} -> order_ids {ids}")

print("\ncleaned with LOWER + TRIM of space, tab, LF, CR:")
sql_clean = q(SQL_CLEAN)
print(sql_clean)

orders = q("SELECT * FROM orders")
# pd:main
clean_counts = (orders["status"].str.strip().str.lower()
                .value_counts().rename_axis("status_clean").reset_index(name="n")
                .sort_values(["n", "status_clean"], ascending=[False, True]).reset_index(drop=True))
# pd:end
print("\npandas str.strip().str.lower().value_counts():")
print(clean_counts)
pd.testing.assert_frame_equal(sql_clean, clean_counts, check_dtype=False)
print("assert: SQL == pandas (compared in printed order n DESC, status_clean ASC)")

# Honest differences
naive = q("SELECT LOWER(TRIM(status)) AS s, COUNT(*) AS n FROM orders GROUP BY s ORDER BY s")
print("\nSQLite TRIM(status) with no second argument strips spaces only; the tab row stays separate:")
print(naive.assign(s=lambda d: d["s"].map(repr)))
print("pandas .str.strip() with no argument strips all whitespace, including the tab.")

# Non-ASCII: SQLite LOWER/NOCASE fold ASCII only unless built with ICU
print("\nSQLite LOWER of 'E-acute + COLE':", con.execute("SELECT LOWER('ÉCOLE')").fetchone()[0],
      "| Python 'str.lower':", "ÉCOLE".lower())
print("NOCASE equal for 'É' vs 'é'?", con.execute("SELECT 'É' = 'é' COLLATE NOCASE").fetchone()[0])

# Non-breaking space (U+00A0): is it stripped?
nb = "completed "
print("\nSQLite TRIM removes U+00A0 by default?", con.execute("SELECT TRIM(?) = 'completed'", (nb,)).fetchone()[0])
print("pandas str.strip() removes U+00A0?   ", pd.Series([nb]).str.strip().iloc[0] == "completed")
# LIKE case sensitivity in SQLite
print("SQLite 'COMPLETED' LIKE 'completed':", con.execute("SELECT 'COMPLETED' LIKE 'completed'").fetchone()[0])
```

**Output (my run):**
```
raw GROUP BY (each spelling is its own group; the tab row prints as 'completed' + tab):
          status  n
0    'COMPLETED'  1
1    'Completed'  2
2    'cancelled'  1
3    'completed'  1
4  'completed\t'  1
5   'completed '  1
COUNT(DISTINCT status): 6

equality under SQLite collations (rows matching 'completed'):
  status = 'completed'                 (BINARY, default)  -> order_ids [4]
  status = 'completed' COLLATE NOCASE                     -> order_ids [1, 3, 4, 5]
  status = 'completed' COLLATE RTRIM                      -> order_ids [2, 4]
  LOWER(TRIM(status)) = 'completed'                       -> order_ids [1, 2, 3, 4, 5]

cleaned with LOWER + TRIM of space, tab, LF, CR:
  status_clean  n
0    completed  6
1    cancelled  1

pandas str.strip().str.lower().value_counts():
  status_clean  n
0    completed  6
1    cancelled  1
assert: SQL == pandas (compared in printed order n DESC, status_clean ASC)

SQLite TRIM(status) with no second argument strips spaces only; the tab row stays separate:
               s  n
0    'cancelled'  1
1    'completed'  5
2  'completed\t'  1
pandas .str.strip() with no argument strips all whitespace, including the tab.

SQLite LOWER of 'E-acute + COLE': École | Python 'str.lower': école
NOCASE equal for 'É' vs 'é'? 0

SQLite TRIM removes U+00A0 by default? 0
pandas str.strip() removes U+00A0?    True
SQLite 'COMPLETED' LIKE 'completed': 1
```

**Edge cases:**
- Honest surprise: SQLite's one-argument `TRIM(status)` strips spaces only, so the tab row stayed separate (the naive query in the output shows 5 and 1 for 'completed' and 'completed' plus tab); pandas `str.strip()` strips all whitespace by default. I gave `TRIM` the characters to strip explicitly to match.
- Non-ASCII: SQLite's `LOWER` and `NOCASE` only fold ASCII letters in the build I ran (the output shows `LOWER` leaving the accented capital E alone, and `NOCASE` saying the capital and small accented E are different), while Python's `lower()` folds it. Not-ASCII text needs ICU or application-side normalisation (hedged for other engines).
- NULL status: a separate group; `LOWER(NULL)` is NULL.
- Non-breaking space (U+00A0), common in web or Excel data: SQLite's default `TRIM` did not remove it (the output shows 0), but pandas `str.strip()` did (True). Another SQL-versus-pandas difference; pass `char(160)` to `TRIM` if needed.

**Then explain:**
- **GROUP BY and DISTINCT** compare values using the column's collation; BINARY compares bytes, so case and spaces matter.
- **Collation changes equality:** NOCASE (ASCII case-insensitive) and RTRIM (ignore trailing spaces) are SQLite's built-ins; you can set them on a column or per comparison with `COLLATE`.
- **Clean once, then group:** `LOWER(TRIM(...))` in the query, or better, clean on load and store a normalised column. Keep the raw value too.
- **Do not hide the mess:** report how many raw spellings collapsed (6 raw values became 2 here); data-quality counts belong in the profile (Q27 and Q45).

**Follow-ups:**
- *Would a unique index treat 'a' and 'A' as duplicates?* Only if the column's collation says so (index collation); hedged by engine, Part 11 for indexes.
- *Mapping variants like 'complete', 'done', 'Completed'?* A mapping table or CASE, then reconcile counts before and after.
- *Does LIKE respect case?* In SQLite `'COMPLETED' LIKE 'completed'` returned 1 in my run (ASCII case-insensitive by default); PostgreSQL's LIKE is case-sensitive (hedged, not executed; Q21).

**Common mistakes:**
- Cleaning in the WHERE clause but forgetting the same cleaning in GROUP BY, so reports disagree.
- Trimming only spaces and missing tabs and newlines from copy-pasted data.
- Assuming the database's default collation is case-insensitive (or case-sensitive) without checking.
- Lower-casing with a tool that only handles ASCII on non-English names.

---

### Q40 ⭐ 🔴 Money and floating point in aggregates: payments(payment_id, amount) with amounts like 0.1 and 0.2. Show why SUM over floating-point columns can print 0.30000000000000004 or give tiny differences between SQL and pandas, why money should use DECIMAL or integer paise, how ROUND behaves (half-away-from-zero versus banker's rounding in Python and pandas), and how to compare results with a tolerance in tests.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Binary floating point cannot store 0.1 or 0.2 exactly, so sums can print 0.30000000000000004 or differ in the last digit between SQLite, Python and pandas; store money as DECIMAL or integer paise, and in tests compare with a tolerance (or compare the integer paise exactly).

**Schema and sample data:**
```sql
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, amount REAL, paise INTEGER);
INSERT INTO payments VALUES
 (1,0.1,10),(2,0.1,10),(3,0.1,10),(4,0.1,10),(5,0.1,10),
 (6,0.1,10),(7,0.1,10),(8,0.1,10),(9,0.1,10),(10,0.1,10),(11,0.2,20);
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_SUM
SELECT SUM(amount) AS total_real, SUM(paise) AS total_paise, SUM(paise) / 100.0 AS rupees FROM payments
```
`total_real` sums the REAL column, `total_paise` sums integers (exact), and `rupees` divides by 100.0 for display.

Dialect notes, **not executed here** (from memory): PostgreSQL has exact `NUMERIC`/`DECIMAL`; MySQL has `DECIMAL`; SQLite has no real DECIMAL type (a declared DECIMAL gets NUMERIC affinity and stores binary floats for fractional values), which is why integer paise is the safe SQLite pattern.

**pandas answer:** (same text as in the Code block)
```python
pd_sum = pay["amount"].sum()                 # numpy pairwise summation
pd_paise = pay["paise"].sum()                # exact in integers
```
`Series.sum()` on a float column is floating point too; sum an integer paise column for an exact result, or use `decimal.Decimal` in Python.

**Example:** Ten payments of 0.1 and one of 0.2; the true total is 1.2 (120 paise).
- `0.1 + 0.2` prints 0.30000000000000004 in both Python and SQLite, and SQLite's `SUM` over a 0.1 row and the 0.2 row also gave 0.30000000000000004.
- Left-to-right adding of ten 0.1 values (a plain loop) gives 0.9999999999999999.
- Over the 11 rows the tools disagree in the last digit: SQLite `SUM` 1.2000000000000002, Python `sum` 1.2000000000000002, `math.fsum` 1.2000000000000002, pandas `sum()` 1.2. A surprise: `fsum` (the most exact of these, it adds the stored binary values exactly and rounds once) says 1.2000000000000002, so the pandas 1.2 is the 'prettier' answer, not the more exact one. Also `sum([0.1] * 10)` printed 1.0 in this Python and `np.sum` also 1.0, even though the naive loop gave 0.9999999999999999 (the builtin `sum` and numpy use smarter summation than a plain loop; mechanism from memory).
- In integer paise SQLite and pandas both gave 120 exactly, `Decimal` gave 1.2, and `== 1.2` on the float sum is False.

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q40: floating point and money; SUM in SQLite vs Python vs pandas; ROUND behaviour; tolerance tests
import math
import sqlite3
from decimal import Decimal, ROUND_HALF_UP
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE payments(payment_id INTEGER PRIMARY KEY, amount REAL, paise INTEGER);
INSERT INTO payments VALUES
 (1,0.1,10),(2,0.1,10),(3,0.1,10),(4,0.1,10),(5,0.1,10),
 (6,0.1,10),(7,0.1,10),(8,0.1,10),(9,0.1,10),(10,0.1,10),(11,0.2,20);
"""
SQL_SUM = "SELECT SUM(amount) AS total_real, SUM(paise) AS total_paise, SUM(paise) / 100.0 AS rupees FROM payments"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
pay = pd.read_sql_query("SELECT * FROM payments", con)
print("python 0.1 + 0.2             :", repr(0.1 + 0.2))
print("sqlite SELECT 0.1 + 0.2      :", repr(con.execute("SELECT 0.1 + 0.2").fetchone()[0]))
print("sqlite SUM over 0.1 and 0.2  :", repr(con.execute("SELECT SUM(amount) FROM payments WHERE payment_id IN (1, 11)").fetchone()[0]))
naive = 0.0
for x in pd.read_sql_query("SELECT amount FROM payments", con)["amount"].tolist():
    naive += x                               # plain left-to-right float addition
print("naive loop acc += x over all 11:", repr(naive))
ten = 0.0
for _ in range(10):
    ten += 0.1
print("naive loop, ten times 0.1     :", repr(ten))

row = con.execute(SQL_SUM).fetchone()
# pd:main
pd_sum = pay["amount"].sum()                 # numpy pairwise summation
pd_paise = pay["paise"].sum()                # exact in integers
# pd:end
tenth = [0.1] * 10
print("\nten values of 0.1 (ten 0.1 and one 0.2; true total 1.2):")
print("  sqlite SUM(real)       :", repr(row[0]))
print("  pandas Series.sum()    :", repr(float(pd_sum)))
print("  python sum(list)       :", repr(sum(pay['amount'].tolist())))
print("  math.fsum (exact-ish)  :", repr(math.fsum(pay['amount'].tolist())))
print("  python sum([0.1]*10)   :", repr(sum(tenth)), "| np.sum([0.1]*10):", repr(float(np.sum(tenth))))
print("  integer paise: sqlite  :", row[1], "| pandas:", pd_paise, "-> rupees", row[2])
print("  Decimal sum            :", sum((Decimal("0.1") for _ in range(10)), Decimal("0.2")))

# Tolerance in tests: equal as paise, or isclose in floats
assert abs(row[0] - pd_sum) < 1e-9 and math.isclose(row[0], pd_sum, rel_tol=1e-12)
assert row[1] == pd_paise == 120
assert round(row[0] * 100) == pd_paise
print("\nasserts passed: SQL and pandas agree within 1e-9; both agree exactly in integer paise (120)")
print("  == would say:", row[0] == 1.2, "(exact float equality is the wrong test)")

# ROUND: SQLite half away from zero; Python round() and pandas/numpy half to even
print("\nROUND behaviour on exact binary halves (2.5, 3.5, 0.5, -2.5) and on 2.675:")
vals = [2.5, 3.5, 0.5, -2.5, 2.675]
sql_round = [con.execute("SELECT ROUND(?, 0)", (v,)).fetchone()[0] for v in vals[:4]] + [con.execute("SELECT ROUND(2.675, 2)").fetchone()[0]]
print("  sqlite ROUND(x,0)/ROUND(2.675,2):", sql_round)
print("  python round(x)/round(2.675,2)  :", [round(v) for v in vals[:4]] + [round(2.675, 2)])
print("  pandas Series.round()/round(2)  :", pd.Series(vals[:4]).round().tolist(), pd.Series([2.675]).round(2).tolist())
print("  numpy np.round(2.675, 2)        :", float(np.round(2.675, 2)))
print("  Decimal quantize HALF_UP 2.675  :", Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
print("  Decimal(2.675) from float is    :", Decimal(2.675))
```

**Output (my run):**
```
python 0.1 + 0.2             : 0.30000000000000004
sqlite SELECT 0.1 + 0.2      : 0.30000000000000004
sqlite SUM over 0.1 and 0.2  : 0.30000000000000004
naive loop acc += x over all 11: 1.2
naive loop, ten times 0.1     : 0.9999999999999999

ten values of 0.1 (ten 0.1 and one 0.2; true total 1.2):
  sqlite SUM(real)       : 1.2000000000000002
  pandas Series.sum()    : 1.2
  python sum(list)       : 1.2000000000000002
  math.fsum (exact-ish)  : 1.2000000000000002
  python sum([0.1]*10)   : 1.0 | np.sum([0.1]*10): 1.0
  integer paise: sqlite  : 120 | pandas: 120 -> rupees 1.2
  Decimal sum            : 1.2

asserts passed: SQL and pandas agree within 1e-9; both agree exactly in integer paise (120)
  == would say: False (exact float equality is the wrong test)

ROUND behaviour on exact binary halves (2.5, 3.5, 0.5, -2.5) and on 2.675:
  sqlite ROUND(x,0)/ROUND(2.675,2): [3.0, 4.0, 1.0, -3.0, 2.67]
  python round(x)/round(2.675,2)  : [2, 4, 0, -2, 2.67]
  pandas Series.round()/round(2)  : [2.0, 4.0, 0.0, -2.0] [2.68]
  numpy np.round(2.675, 2)        : 2.68
  Decimal quantize HALF_UP 2.675  : 2.68
  Decimal(2.675) from float is    : 2.67499999999999982236431605997495353221893310546875
```

**Edge cases:**
- Rounding on exact halves: SQLite `ROUND(2.5, 0)` = 3.0, `ROUND(-2.5, 0)` = -3.0 (half away from zero). Python `round(2.5)` = 2 and `round(0.5)` = 0 (half to even), and pandas `Series.round()` gave [2.0, 4.0, 0.0, -2.0] for 2.5, 3.5, 0.5, -2.5 (half to even as well).
- Values that are not exact halves in binary: `ROUND(2.675, 2)` in SQLite and `round(2.675, 2)` in Python gave 2.67, but numpy and pandas gave 2.68, and `Decimal('2.675')` quantized HALF_UP gave 2.68. The float 2.675 is really 2.67499999999999982..., so which answer you get depends on the algorithm; for money, round the decimal value, with a stated rule.
- Aggregating a rounded value versus rounding an aggregate gives different totals; decide which one the report uses.
- NULL amounts are ignored by SUM in both SQL and pandas (not in the toy data; see Q16 for the all-NULL difference).

**Then explain:**
- **Why:** 0.1 is a repeating fraction in binary, so each stored value has a tiny error and sums accumulate or cancel it depending on the order and algorithm.
- **SQL versus pandas:** both are correct to about 1e-15 relative; they can differ in the last bit because they add in a different order or with different compensation. Never assert exact equality on floats.
- **Fix for money:** integer minor units (paise) or DECIMAL/NUMERIC; do the division only for display.
- **Tolerance in tests:** `math.isclose(a, b, rel_tol=1e-12)` or `abs(a - b) < 1e-9`, or convert to paise with `round(x * 100)` and compare integers (the Code block does both).
- **ROUND rules:** state the rounding mode (half away from zero, half even, half up) and check what the engine and the language do; they differ.

**Follow-ups:**
- *Which rounding do banks use?* Often half-even (banker's rounding) to avoid bias, but your finance team decides; I do not claim a standard here.
- *How big are the errors?* About 1e-16 relative per operation; they matter for equality, for sums of millions of rows, and for reconciliation to the paisa.
- *Does pandas have an exact decimal type?* Object columns of `Decimal` work but are slow; paise integers are simpler.

**Common mistakes:**
- `assert sql_total == pandas_total` on floats.
- Storing money as FLOAT and rounding at the end, then being a paisa off in reconciliation.
- Assuming SQL `ROUND` and Python `round` agree on halves.
- Dividing integer paise by 100 early and then summing the floats.

---

### Q41 ⭐ 🔴 Null-safe equality: how do you compare two nullable columns so that NULL equals NULL? Show IS DISTINCT FROM / IS NOT DISTINCT FROM (PostgreSQL and others), the SQLite 'IS' operator, MySQL's <=>, and the portable (a = b OR (a IS NULL AND b IS NULL)) form on a table changes(id, old_value, new_value) used to find rows that changed. Contrast with pandas, where NaN != NaN, and show equals() and a mask that treats NaN pairs as equal.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Plain `=` gives UNKNOWN when either side is NULL, so use a null-safe comparison: `IS NOT DISTINCT FROM` (standard, PostgreSQL and others), SQLite's `IS`, MySQL's `<=>`, or the portable `(a = b OR (a IS NULL AND b IS NULL))`; to find changed rows negate it carefully, and in pandas remember `NaN != NaN` is True so you must mask the both-missing case.

**Schema and sample data:**
```sql
CREATE TABLE changes(id INTEGER PRIMARY KEY, old_value TEXT, new_value TEXT);
INSERT INTO changes VALUES
 (1,'a','a'),(2,'a','b'),(3,NULL,NULL),(4,NULL,'x'),(5,'y',NULL);
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_IS
SELECT id FROM changes WHERE old_value IS NOT new_value ORDER BY id

-- SQL_IDF
SELECT id FROM changes WHERE old_value IS DISTINCT FROM new_value ORDER BY id

-- SQL_PORTABLE
SELECT id FROM changes
WHERE old_value <> new_value
   OR (old_value IS NULL AND new_value IS NOT NULL)
   OR (old_value IS NOT NULL AND new_value IS NULL)
ORDER BY id

-- SQL_SAME
SELECT id FROM changes
WHERE old_value = new_value OR (old_value IS NULL AND new_value IS NULL)
ORDER BY id
```
`SQL_IS` is SQLite's operator (`old_value IS NOT new_value` is true when the values differ, treating NULL as a value). `SQL_IDF` is the standard `IS DISTINCT FROM`, which SQLite accepted in 3.45.1 (I believe from 3.39; the run proves 3.45). `SQL_PORTABLE` spells out the changed condition without any special operator. `SQL_SAME` is the equality version from the question.

Dialect notes, **not executed here** (from memory): PostgreSQL supports `IS [NOT] DISTINCT FROM`; MySQL spells null-safe equality `<=>` (and also supports `IS NOT DISTINCT FROM` in recent versions, I believe, check your version); SQL Server added `IS [NOT] DISTINCT FROM` only in recent releases (verify); Oracle has no direct operator and people use `DECODE` or the explicit form.

**pandas answer:** (same text as in the Code block)
```python
both_missing = a.isna() & b.isna()
changed_mask = (a != b) & ~both_missing          # NaN pairs are not changes; one-sided NaN still is
same_mask = (a == b) | both_missing
changed_ids = df.loc[changed_mask, "id"].tolist()
```
Build the mask from `!=` and exclude the both-missing rows; `equals()` answers a whole-object question, not a row-wise one.

**Example:** `changes` has five rows: (1, 'a', 'a'), (2, 'a', 'b'), (3, NULL, NULL), (4, NULL, 'x'), (5, 'y', NULL). The truly changed rows are 2, 4 and 5.
- `old_value <> new_value`: row 2 only, because rows 3, 4 and 5 evaluate to UNKNOWN.
- `IS NOT`, `IS DISTINCT FROM` and the explicit form all return 2, 4, 5.
- The trap `NOT (old_value = new_value OR (old_value IS NULL AND new_value IS NULL))` returns only row 2: for row 4 the inner expression is UNKNOWN OR FALSE = UNKNOWN, and NOT UNKNOWN is still UNKNOWN, so the row is dropped.
- The 'same' rows with `a = b OR both NULL` are 1 and 3.
- pandas `a != b` is [False, True, True, True, True] (row 3, NaN versus NaN, is wrongly flagged) and `a == b` is [True, False, False, False, False]; the mask `(a != b) & ~both_missing` gives 2, 4, 5.

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q41: null-safe equality, SQLite vs pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE changes(id INTEGER PRIMARY KEY, old_value TEXT, new_value TEXT);
INSERT INTO changes VALUES
 (1,'a','a'),(2,'a','b'),(3,NULL,NULL),(4,NULL,'x'),(5,'y',NULL);
"""
# changed rows are ids 2, 4, 5 (id 1 same value, id 3 NULL to NULL = no change)
SQL_NAIVE = "SELECT id FROM changes WHERE old_value <> new_value ORDER BY id"
SQL_IS = "SELECT id FROM changes WHERE old_value IS NOT new_value ORDER BY id"
SQL_IDF = "SELECT id FROM changes WHERE old_value IS DISTINCT FROM new_value ORDER BY id"
SQL_PORTABLE = """
SELECT id FROM changes
WHERE old_value <> new_value
   OR (old_value IS NULL AND new_value IS NOT NULL)
   OR (old_value IS NOT NULL AND new_value IS NULL)
ORDER BY id
"""
SQL_WRONG_NOT = """
SELECT id FROM changes
WHERE NOT (old_value = new_value OR (old_value IS NULL AND new_value IS NULL))
ORDER BY id
"""
SQL_SAME = """
SELECT id FROM changes
WHERE old_value = new_value OR (old_value IS NULL AND new_value IS NULL)
ORDER BY id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
ids = lambda s: [r[0] for r in con.execute(s)]
print("naive  old <> new                       :", ids(SQL_NAIVE), "(misses 4 and 5)")
print("SQLite old IS NOT new                   :", ids(SQL_IS))
print("IS DISTINCT FROM (SQLite >= 3.39)       :", ids(SQL_IDF))
print("portable explicit form                  :", ids(SQL_PORTABLE))
print("NOT (a = b OR both NULL)  [trap]        :", ids(SQL_WRONG_NOT), "(row 4 is UNKNOWN, NOT UNKNOWN is UNKNOWN)")
print("'same' rows, a = b OR both NULL         :", ids(SQL_SAME))
print("SELECT NULL = NULL ->", con.execute("SELECT NULL = NULL").fetchone()[0],
      "| NULL IS NULL ->", con.execute("SELECT NULL IS NULL").fetchone()[0],
      "| NULL IS NOT 'x' ->", con.execute("SELECT NULL IS NOT 'x'").fetchone()[0])

df = pd.read_sql_query("SELECT * FROM changes", con)
a, b = df["old_value"], df["new_value"]
print("\npandas a != b (NaN != NaN is True):", (a != b).tolist())
print("pandas a == b                     :", (a == b).tolist())
# pd:main
both_missing = a.isna() & b.isna()
changed_mask = (a != b) & ~both_missing          # NaN pairs are not changes; one-sided NaN still is
same_mask = (a == b) | both_missing
changed_ids = df.loc[changed_mask, "id"].tolist()
# pd:end
print("changed ids (pandas mask)         :", changed_ids)
assert changed_ids == ids(SQL_IS) == ids(SQL_IDF) == ids(SQL_PORTABLE) == [2, 4, 5]
assert df.loc[same_mask, "id"].tolist() == ids(SQL_SAME) == [1, 3]
print("asserts passed: SQL (IS NOT / IS DISTINCT FROM / portable) == pandas mask, ids sorted ascending")

# Whole-column equals(): NaN in the same position counts as equal, but it is all-or-nothing
print("\na.equals(b):", a.equals(b))
print("df[['old_value']].equals(df[['old_value']].copy()):", df[["old_value"]].equals(df[["old_value"]].copy()))
print("a[same_mask].equals(b[same_mask]) (rows 1 and 3, NaN pair included):", a[same_mask].equals(b[same_mask]))
# pandas 3 string dtype
print("dtype of old_value:", a.dtype)
```

**Output (my run):**
```
naive  old <> new                       : [2] (misses 4 and 5)
SQLite old IS NOT new                   : [2, 4, 5]
IS DISTINCT FROM (SQLite >= 3.39)       : [2, 4, 5]
portable explicit form                  : [2, 4, 5]
NOT (a = b OR both NULL)  [trap]        : [2] (row 4 is UNKNOWN, NOT UNKNOWN is UNKNOWN)
'same' rows, a = b OR both NULL         : [1, 3]
SELECT NULL = NULL -> None | NULL IS NULL -> 1 | NULL IS NOT 'x' -> 1

pandas a != b (NaN != NaN is True): [False, True, True, True, True]
pandas a == b                     : [True, False, False, False, False]
changed ids (pandas mask)         : [2, 4, 5]
asserts passed: SQL (IS NOT / IS DISTINCT FROM / portable) == pandas mask, ids sorted ascending

a.equals(b): False
df[['old_value']].equals(df[['old_value']].copy()): True
a[same_mask].equals(b[same_mask]) (rows 1 and 3, NaN pair included): True
dtype of old_value: str
```

**Edge cases:**
- Both NULL means not changed; one NULL and one value means changed (rows 4 and 5).
- Empty strings are not NULL: `'' IS NOT NULL` is true; do not mix them up in change detection.
- Types: in pandas 3 the string columns use the `str` dtype with NaN as the missing value, so `a != b` behaves as shown.
- `Series.equals` treats NaNs in the same positions as equal but is all-or-nothing (False for the whole column here, True for the rows 1 and 3 subset).
- Do not use a sentinel such as `COALESCE(old_value, '') = COALESCE(new_value, '')`: it conflates NULL with ''. (Reasoning only; not run.)

**Then explain:**
- **Why `=` fails:** a comparison with NULL is UNKNOWN, and `WHERE` keeps only TRUE (Q5).
- **Null-safe forms:** `IS NOT DISTINCT FROM` (standard), `IS` in SQLite, `<=>` in MySQL, or the explicit three-part boolean.
- **Changed rows** are the negation, but write the changed condition directly (`<>` or one-sided NULL), or use `IS DISTINCT FROM`; do not `NOT` the explicit equality form because UNKNOWN survives NOT.
- **pandas:** NaN is not equal to anything including itself, so `!=` flags NaN pairs as changes; mask with `isna() & isna()`. `a.eq(b) | both_missing` is the null-safe equality.

**Follow-ups:**
- *Join on nullable keys so NULL matches NULL?* The same null-safe operator in the ON clause (Part 2); pandas merge matches NaN keys to each other, as the pandas docs warn.
- *Index use?* An OR with IS NULL can defeat an index in some engines (Part 11; not run).
- *Compare two whole tables?* EXCEPT or a FULL JOIN with this predicate (Part 2).

**Common mistakes:**
- Using `=` or `<>` and missing NULL transitions.
- Negating the null-safe equality form with NOT and losing UNKNOWN rows.
- Trusting `df.a != df.b` for change detection when NaNs exist.
- Using a sentinel value in COALESCE that can also occur in real data.

---

### Q42 ⭐ 🔴 Distinct users per day versus overall: events(event_id, user_id, event_date). Explain why the sum of daily COUNT(DISTINCT user_id) is not the number of distinct users over the period, show both queries, the pandas nunique per day versus overall, and why a monthly active count cannot be built by adding daily counts. (Part 8 covers DAU/MAU metrics; this is the aggregation fact behind them.)
**Asked at:** interview-prep guide and platform question bank (StrataScratch, DataLemur style), not a candidate report; product-company data scientist screens
**Say this first (1 line):** Adding up daily distinct users counts a user once per day they were active, so the sum is at least as large as the distinct users over the whole period; to get the period's distinct users you must run COUNT(DISTINCT user_id) over the whole period, not add up the daily counts, and the same is true for monthly actives.

**Schema and sample data:**
```sql
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_date TEXT);
INSERT INTO events VALUES
 (1,1,'2026-01-30'),(2,1,'2026-01-30'),(3,2,'2026-01-30'),
 (4,1,'2026-01-31'),(5,2,'2026-01-31'),
 (6,3,'2026-01-31'),(7,1,'2026-02-01'),(8,3,'2026-02-01'),
 (9,NULL,'2026-02-01'),(10,4,'2026-02-02');
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_DAILY
SELECT event_date, COUNT(DISTINCT user_id) AS dau, COUNT(*) AS events
FROM events GROUP BY event_date ORDER BY event_date

-- SQL_OVERALL
SELECT COUNT(DISTINCT user_id) AS distinct_users FROM events

-- SQL_SUM_DAILY
SELECT SUM(dau) FROM (SELECT COUNT(DISTINCT user_id) AS dau FROM events GROUP BY event_date)

-- SQL_MONTH
SELECT substr(event_date, 1, 7) AS month,
       COUNT(DISTINCT user_id) AS mau,
       (SELECT SUM(d) FROM (SELECT COUNT(DISTINCT user_id) AS d FROM events e2
                            WHERE substr(e2.event_date,1,7) = substr(events.event_date,1,7)
                            GROUP BY e2.event_date)) AS sum_of_daily
FROM events GROUP BY month ORDER BY month
```
`SQL_DAILY` is one row per day, `SQL_OVERALL` the distinct users over all events, `SQL_SUM_DAILY` the (wrong) sum of daily counts, and `SQL_MONTH` compares each month's true distinct count with the sum of its daily counts. The month is `substr(event_date, 1, 7)` because ISO date strings sort and slice cleanly in SQLite (date functions by engine are hedged in Part 6).

**pandas answer:** (same text as in the Code block)
```python
pd_daily = (ev.groupby("event_date", as_index=False)
            .agg(dau=("user_id", "nunique"), events=("event_id", "size")))
pd_overall = ev["user_id"].nunique()
ev["month"] = ev["event_date"].str[:7]
pd_month = ev.groupby("month", as_index=False).agg(mau=("user_id", "nunique"))
pd_month["sum_of_daily"] = (ev.groupby(["month", "event_date"])["user_id"].nunique()
                            .groupby("month").sum().to_numpy())
```
`groupby('event_date')['user_id'].nunique()` for the daily counts, `df['user_id'].nunique()` for overall, and for the months a groupby on the month then the sum of the per-day nunique. `nunique()` skips NaN by default (`dropna=True`).

**Example:** Ten events. Daily distinct users: 30 Jan {1, 2} = 2, 31 Jan {1, 2, 3} = 3, 1 Feb {1, 3} = 2 (a NULL user_id row is ignored), 2 Feb {4} = 1.
- Sum of daily distinct = 2 + 3 + 2 + 1 = 8; distinct users overall = 4 (users 1, 2, 3, 4).
- January: users {1, 2, 3}, so 3 distinct, but the daily counts add to 2 + 3 = 5 (users 1 and 2 are counted twice).
- February: users {1, 3, 4} = 3 distinct, and the daily counts also add to 3, only because no user is active on both February days. The sum equals the distinct count only when no user repeats across the days.
- 30 January has 3 events but 2 distinct users (user 1 appeared twice): `COUNT(*)` also differs from `COUNT(DISTINCT user_id)`.

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q42: sum of daily distinct users is not the overall distinct count
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_date TEXT);
INSERT INTO events VALUES
 (1,1,'2026-01-30'),(2,1,'2026-01-30'),(3,2,'2026-01-30'),
 (4,1,'2026-01-31'),(5,2,'2026-01-31'),
 (6,3,'2026-01-31'),(7,1,'2026-02-01'),(8,3,'2026-02-01'),
 (9,NULL,'2026-02-01'),(10,4,'2026-02-02');
"""
SQL_DAILY = """
SELECT event_date, COUNT(DISTINCT user_id) AS dau, COUNT(*) AS events
FROM events GROUP BY event_date ORDER BY event_date
"""
SQL_OVERALL = "SELECT COUNT(DISTINCT user_id) AS distinct_users FROM events"
SQL_SUM_DAILY = "SELECT SUM(dau) FROM (SELECT COUNT(DISTINCT user_id) AS dau FROM events GROUP BY event_date)"
SQL_MONTH = """
SELECT substr(event_date, 1, 7) AS month,
       COUNT(DISTINCT user_id) AS mau,
       (SELECT SUM(d) FROM (SELECT COUNT(DISTINCT user_id) AS d FROM events e2
                            WHERE substr(e2.event_date,1,7) = substr(events.event_date,1,7)
                            GROUP BY e2.event_date)) AS sum_of_daily
FROM events GROUP BY month ORDER BY month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
daily = q(SQL_DAILY)
print(daily)
overall = con.execute(SQL_OVERALL).fetchone()[0]
sum_daily = con.execute(SQL_SUM_DAILY).fetchone()[0]
print("\noverall COUNT(DISTINCT user_id):", overall, "| SUM of daily distinct:", sum_daily)
month = q(SQL_MONTH)
print("\nper month, distinct vs sum of daily distinct:")
print(month)

ev = q("SELECT * FROM events")
# pd:main
pd_daily = (ev.groupby("event_date", as_index=False)
            .agg(dau=("user_id", "nunique"), events=("event_id", "size")))
pd_overall = ev["user_id"].nunique()
ev["month"] = ev["event_date"].str[:7]
pd_month = ev.groupby("month", as_index=False).agg(mau=("user_id", "nunique"))
pd_month["sum_of_daily"] = (ev.groupby(["month", "event_date"])["user_id"].nunique()
                            .groupby("month").sum().to_numpy())
# pd:end
print("\npandas daily:\n", pd_daily)
print("pandas overall nunique:", pd_overall, "| sum of daily:", pd_daily["dau"].sum())
print("pandas month:\n", pd_month)

pd.testing.assert_frame_equal(daily, pd_daily, check_dtype=False)      # both ordered by event_date
pd.testing.assert_frame_equal(month, pd_month, check_dtype=False)      # both ordered by month
assert overall == pd_overall == 4 and sum_daily == pd_daily["dau"].sum() == 8
assert (pd_month["mau"] <= pd_month["sum_of_daily"]).all() and overall <= sum_daily
print("\nasserts passed: SQL == pandas (ordered by date / month); overall 4 <= sum of daily 8")

# NULL user_id: COUNT(DISTINCT) ignores it, nunique() default dropna=True ignores it; COUNT(*) counts the row
print("NULL user_id row on 2026-02-01: COUNT(*) =", int(daily.loc[daily.event_date == '2026-02-01', 'events'].iloc[0]),
      "| dau =", int(daily.loc[daily.event_date == '2026-02-01', 'dau'].iloc[0]))
print("nunique(dropna=False) overall:", ev["user_id"].nunique(dropna=False), "(counts the missing value as a user)")
```

**Output (my run):**
```
   event_date  dau  events
0  2026-01-30    2       3
1  2026-01-31    3       3
2  2026-02-01    2       3
3  2026-02-02    1       1

overall COUNT(DISTINCT user_id): 4 | SUM of daily distinct: 8

per month, distinct vs sum of daily distinct:
     month  mau  sum_of_daily
0  2026-01    3             5
1  2026-02    3             3

pandas daily:
    event_date  dau  events
0  2026-01-30    2       3
1  2026-01-31    3       3
2  2026-02-01    2       3
3  2026-02-02    1       1
pandas overall nunique: 4 | sum of daily: 8
pandas month:
      month  mau  sum_of_daily
0  2026-01    3             5
1  2026-02    3             3

asserts passed: SQL == pandas (ordered by date / month); overall 4 <= sum of daily 8
NULL user_id row on 2026-02-01: COUNT(*) = 3 | dau = 2
nunique(dropna=False) overall: 5 (counts the missing value as a user)
```

**Edge cases:**
- NULL user_id: `COUNT(DISTINCT user_id)` and `nunique()` ignore it, `COUNT(*)` does not; `nunique(dropna=False)` would count the missing value as a user (5 overall in the output).
- Duplicates: repeated events by the same user on a day count once in DAU.
- Time zones: 'day' depends on the time zone of the timestamp; the toy data uses plain dates (Part 6).
- Month boundaries and partial months: compare like with like.
- Pre-aggregated tables: if you only keep daily counts you cannot recover weekly or monthly distincts; keep user-level rows or use sketches (HyperLogLog-style, engine-specific, not run here).

**Then explain:**
- **Distinct counts are not additive:** `COUNT(DISTINCT x)` over a union of groups is at most the sum of the groups' counts, equal only if the groups share no values.
- **DAU, WAU, MAU** are each their own distinct count over their own window; you cannot derive MAU from DAU rows (Part 8).
- **pandas:** `nunique` per group versus overall; same arithmetic.
- **The stickiness ratio** DAU/MAU needs a real MAU, which is why this matters.

**Follow-ups:**
- *Average DAU in a month?* The average of the daily distinct counts is fine and is a different quantity from MAU.
- *Weekly actives from a daily summary table?* Not possible without the user-level rows; store a user-day table instead.
- *Large data?* Approximate distinct counts, hedged by engine.

**Common mistakes:**
- `SUM(daily_users)` presented as monthly actives.
- Counting events (`COUNT(*)`) instead of users.
- Counting NULL user_id as a user, or forgetting `nunique` ignores NaN.
- Mixing windows (users active in the last 30 days versus calendar month).

---

### Q43 ⭐ 🔴 pandas groupby with categoricals and empty groups: orders(region as a categorical dtype, amount). Explain observed=True versus False (default True in pandas 3 per the docs), how unobserved categories appear as zero or NaN rows, how that compares with SQL, where empty groups need a LEFT JOIN to a reference table, and how sum versus count versus mean behave on an empty category. Include dropna and sort as well.
**Asked at:** pandas documentation (Comparison with SQL) and prep guides, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** With a categorical key, `observed=True` returns only categories that appear in the data (the default in pandas 3.0, which I confirmed in my run), `observed=False` also returns the unobserved categories as zero-count rows (sum 0.0, count 0, mean NaN), whereas SQL GROUP BY never invents a group; to show empty groups in SQL you LEFT JOIN from a reference table.

**Schema and sample data:**
```sql
CREATE TABLE regions(region TEXT PRIMARY KEY);
INSERT INTO regions VALUES ('East'),('North'),('South'),('West');
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'North',100),(2,'North',50),(3,'East',70),(4,'South',NULL),(5,NULL,30);
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_PLAIN
SELECT region, COUNT(*) AS n, COUNT(amount) AS n_amount, SUM(amount) AS total, AVG(amount) AS mean_amt
FROM orders GROUP BY region ORDER BY region

-- SQL_REF
SELECT r.region, COUNT(o.order_id) AS n, COUNT(o.amount) AS n_amount, SUM(o.amount) AS total, AVG(o.amount) AS mean_amt
FROM regions r LEFT JOIN orders o ON o.region = r.region
GROUP BY r.region ORDER BY r.region
```
`SQL_PLAIN` is the plain GROUP BY (no West, and the NULL region is its own group). `SQL_REF` starts from a `regions` reference table and LEFT JOINs `orders`, counting `o.order_id` and `o.amount` (not `*`, which would count the NULL-extended row as 1).

**pandas answer:** (same text as in the Code block)
```python
# 'South' first on purpose: a categorical sorts by category order, not alphabetically
cats = ["South", "North", "East", "West"]
df = raw.assign(region=pd.Categorical(raw["region"], categories=cats))
agg = dict(n=("order_id", "size"), n_amount=("amount", "count"),
           total=("amount", "sum"), mean_amt=("amount", "mean"))
default = df.groupby("region").agg(**agg)                                  # observed default is True in pandas 3
unobserved = df.groupby("region", observed=False).agg(**agg)               # every category, even West
with_nan = df.groupby("region", observed=False, dropna=False).agg(**agg)   # plus a NaN group
```
`region` is a `Categorical` with the category order South, North, East, West (deliberately not alphabetical). The three groupbys differ only in `observed` and `dropna`.

**Example:** Five orders: North 100 and 50, East 70, South with NULL amount, and a NULL region with 30. West is a known category with no orders.
- pandas default (observed=True, dropna=True): South, North, East; no West, and the NULL-region order (30) is dropped.
- `observed=False`: adds West: n = 0, count 0, sum 0.0, mean NaN, min and max NaN.
- `observed=False, dropna=False`: adds a NaN group with total 30.0.
- SQL LEFT JOIN from regions: West with `COUNT = 0`, `SUM = NULL`, `AVG = NULL`; South has n = 1 and `COUNT(amount)` = 0, SUM NULL.
- Different from pandas: SQL SUM of nothing is NULL, pandas sum of nothing is 0.0 unless `min_count=1`. I used `min_count=1` to match SQL and compared in alphabetical order, since pandas sorts a categorical by its category order (South, North, East, West) while my SQL used ORDER BY region.

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q43: pandas groupby on a categorical key: observed, dropna, sort; SQL LEFT JOIN to a reference table
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE regions(region TEXT PRIMARY KEY);
INSERT INTO regions VALUES ('East'),('North'),('South'),('West');
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'North',100),(2,'North',50),(3,'East',70),(4,'South',NULL),(5,NULL,30);
"""
SQL_PLAIN = """
SELECT region, COUNT(*) AS n, COUNT(amount) AS n_amount, SUM(amount) AS total, AVG(amount) AS mean_amt
FROM orders GROUP BY region ORDER BY region
"""
SQL_REF = """
SELECT r.region, COUNT(o.order_id) AS n, COUNT(o.amount) AS n_amount, SUM(o.amount) AS total, AVG(o.amount) AS mean_amt
FROM regions r LEFT JOIN orders o ON o.region = r.region
GROUP BY r.region ORDER BY r.region
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
print("pandas version:", pd.__version__)
print("SQL GROUP BY on orders only (the NULL region is its own group; West absent):")
print(q(SQL_PLAIN))
print("\nSQL LEFT JOIN from the reference table (West appears; SUM and AVG are NULL, COUNT(col) is 0):")
sql_ref = q(SQL_REF)
print(sql_ref)

raw = q("SELECT * FROM orders")
# pd:main
# 'South' first on purpose: a categorical sorts by category order, not alphabetically
cats = ["South", "North", "East", "West"]
df = raw.assign(region=pd.Categorical(raw["region"], categories=cats))
agg = dict(n=("order_id", "size"), n_amount=("amount", "count"),
           total=("amount", "sum"), mean_amt=("amount", "mean"))
default = df.groupby("region").agg(**agg)                                  # observed default is True in pandas 3
unobserved = df.groupby("region", observed=False).agg(**agg)               # every category, even West
with_nan = df.groupby("region", observed=False, dropna=False).agg(**agg)   # plus a NaN group
# pd:end
print("\ngroupby default (observed=True in pandas 3, dropna=True):\n", default)
print("\nobserved=False:\n", unobserved)
print("\nobserved=False, dropna=False:\n", with_nan)
print("\nobserved=True explicit equals the default:", default.equals(df.groupby('region', observed=True).agg(**agg)))

# Match SQL: reorder alphabetically and make SUM NULL for empty groups with min_count=1
pd_ref = (df.groupby("region", observed=False)
          .agg(n=("order_id", "size"), n_amount=("amount", "count"),
               total=("amount", lambda s: s.sum(min_count=1)), mean_amt=("amount", "mean"))
          .reset_index())
pd_ref["region"] = pd_ref["region"].astype(object)       # sort_values on a categorical uses category order
pd_ref = pd_ref.sort_values("region").reset_index(drop=True)
print("\npandas shaped like the LEFT JOIN result (alphabetical, min_count=1):\n", pd_ref)
pd.testing.assert_frame_equal(sql_ref.fillna(-1), pd_ref.fillna(-1), check_dtype=False)
print("assert: LEFT JOIN result == pandas observed=False with min_count=1 (alphabetical order, NaN/NULL compared via fillna(-1))")

# What the default sum() does on the empty and the all-missing category
print("\nWest (empty) sum:", unobserved.loc['West', 'total'], "| South (all NaN amount) sum:", unobserved.loc['South', 'total'],
      "| West mean:", unobserved.loc['West', 'mean_amt'])
# Plain object (non-categorical) column never produces empty groups
obj = raw.groupby("region").agg(**agg)
print("\nsame data, plain string column: groups =", list(obj.index), "| sorted alphabetically")
print("sort=False on categorical, observed=False:", list(df.groupby('region', observed=False, sort=False).size().index))

# min and max on an empty or all-NaN category
mm = df.groupby("region", observed=False).agg(lo=("amount", "min"), hi=("amount", "max"))
print("\nmin/max per category (observed=False):\n", mm)
```

**Output (my run):**
```
pandas version: 3.0.5
SQL GROUP BY on orders only (the NULL region is its own group; West absent):
  region  n  n_amount  total  mean_amt
0    NaN  1         1   30.0      30.0
1   East  1         1   70.0      70.0
2  North  2         2  150.0      75.0
3  South  1         0    NaN       NaN

SQL LEFT JOIN from the reference table (West appears; SUM and AVG are NULL, COUNT(col) is 0):
  region  n  n_amount  total  mean_amt
0   East  1         1   70.0      70.0
1  North  2         2  150.0      75.0
2  South  1         0    NaN       NaN
3   West  0         0    NaN       NaN

groupby default (observed=True in pandas 3, dropna=True):
         n  n_amount  total  mean_amt
region
South   1         0    0.0       NaN
North   2         2  150.0      75.0
East    1         1   70.0      70.0

observed=False:
         n  n_amount  total  mean_amt
region
South   1         0    0.0       NaN
North   2         2  150.0      75.0
East    1         1   70.0      70.0
West    0         0    0.0       NaN

observed=False, dropna=False:
         n  n_amount  total  mean_amt
region
South   1         0    0.0       NaN
North   2         2  150.0      75.0
East    1         1   70.0      70.0
West    0         0    0.0       NaN
NaN     1         1   30.0      30.0

observed=True explicit equals the default: True

pandas shaped like the LEFT JOIN result (alphabetical, min_count=1):
   region  n  n_amount  total  mean_amt
0   East  1         1   70.0      70.0
1  North  2         2  150.0      75.0
2  South  1         0    NaN       NaN
3   West  0         0    NaN       NaN
assert: LEFT JOIN result == pandas observed=False with min_count=1 (alphabetical order, NaN/NULL compared via fillna(-1))

West (empty) sum: 0.0 | South (all NaN amount) sum: 0.0 | West mean: nan

same data, plain string column: groups = ['East', 'North', 'South'] | sorted alphabetically
sort=False on categorical, observed=False: ['North', 'East', 'South', 'West']

min/max per category (observed=False):
           lo     hi
region
South    NaN    NaN
North   50.0  100.0
East    70.0   70.0
West     NaN    NaN
```

**Edge cases:**
- Empty category: sum 0.0, count 0, size 0, mean NaN, min and max NaN. South (all-missing amounts) behaves like an empty group for sum, count, mean, min and max but has size 1.
- `dropna`: default True drops NaN keys; the NULL-region order's 30 disappears from the totals unless `dropna=False`. SQL keeps NULL as a group.
- `sort`: default True sorts groups by category order for a categorical (not alphabetical); `sort=False` gave North, East, South, West (observed groups in order of appearance, then unobserved). With a plain string column the groups come out alphabetically.
- `observed` only matters for categorical (or multiple categorical) keys; for plain string keys there are no unobserved groups.
- Combining several grouping keys with `observed=False` can create the Cartesian product of categories, which may be large (not demonstrated here).

**Then explain:**
- **Categorical dtype** stores the full list of allowed values, so pandas knows about categories with no rows.
- **observed=True** matches what SQL GROUP BY does; **observed=False** gives a 'complete' table like a LEFT JOIN from a dimension table.
- **Version warning:** the documented default changed to True in pandas 3.0.0 (I read this on the groupby reference page; earlier versions defaulted to False with a deprecation warning; the old behaviour is from memory). Pass `observed` explicitly in shared code.
- **sum, count, mean** on an empty category: 0, 0, NaN in pandas; SQL via LEFT JOIN: NULL, 0, NULL. Use `COALESCE(SUM(...), 0)` in SQL or `min_count=1` in pandas to align.

**Follow-ups:**
- *Why a LEFT JOIN and not a WHERE?* A WHERE on the right table's column turns it back into an inner join (Part 2).
- *Fill zeros for a chart?* `reindex(categories, fill_value=0)` on a plain groupby result is another route (not run here).
- *Do I need categoricals?* For memory with few distinct strings and ordered categories; otherwise plain strings avoid this trap.

**Common mistakes:**
- Assuming a missing region shows up as a zero row in the default pandas groupby.
- Mixing up `COUNT(*)` and `COUNT(col)` on the LEFT JOIN (the empty group gets 1 instead of 0).
- Forgetting that categorical sort order is the category order, not alphabetical.
- Relying on the old default of `observed` across pandas versions.

---

### Q44 ⭐ 🔴 CASE WHEN subtleties: explain the searched versus simple CASE forms, evaluation order (first match wins), the missing-ELSE NULL, why CASE x WHEN NULL THEN ... never matches, and how mixed result types behave (hedged by engine). Give a bug example from a status mapping on orders(order_id, status) that miscategorises NULL, and show the pandas np.select / Series.map / where equivalents with default and NaN handling.
**Asked at:** interview-prep guide, not a candidate report; SQL screens and rounds for data analyst and data scientist roles at product companies, GCCs, IT services and startups
**Say this first (1 line):** A searched CASE (`CASE WHEN cond ...`) tests arbitrary conditions in order and the first true one wins, a simple CASE (`CASE x WHEN v ...`) is shorthand for `x = v`, a missing ELSE returns NULL, and because `x = NULL` is never true, `CASE x WHEN NULL` never matches; in pandas use np.select (first True wins) or map plus fillna and handle NaN explicitly.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT);
INSERT INTO orders VALUES
 (1,'completed'),(2,'cancelled'),(3,'shipped'),(4,NULL),(5,'refunded'),(6,'completed');
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_BUG
SELECT order_id, status,
       CASE WHEN status <> 'cancelled' THEN 'active' ELSE 'inactive' END AS bucket
FROM orders ORDER BY order_id

-- SQL_FIX
SELECT order_id, status,
       CASE WHEN status IS NULL THEN 'unknown'
            WHEN status IN ('completed', 'shipped') THEN 'active'
            WHEN status IN ('cancelled', 'refunded') THEN 'inactive'
            ELSE 'other' END AS bucket
FROM orders ORDER BY order_id

-- SQL_SIMPLE_NULL
SELECT order_id, CASE status WHEN NULL THEN 'unknown' WHEN 'completed' THEN 'done' END AS simple_case
FROM orders ORDER BY order_id

-- SQL_ORDER
SELECT order_id, status,
       CASE WHEN status LIKE 'c%' THEN 'starts_with_c'
            WHEN status = 'completed' THEN 'completed' END AS first_match_wins
FROM orders ORDER BY order_id
```
`SQL_BUG` is the miscategorising status mapping. `SQL_FIX` handles NULL first and lists the statuses explicitly. `SQL_SIMPLE_NULL` shows `CASE status WHEN NULL`. `SQL_ORDER` shows first match wins.

**pandas answer:** (same text as in the Code block)
```python
conds = [s.isna(), s.isin(["completed", "shipped"]), s.isin(["cancelled", "refunded"])]
bucket_select = np.select(conds, ["unknown", "active", "inactive"], default="other")   # first True wins, like CASE
bucket_map = s.map({"completed": "active", "shipped": "active",
                    "cancelled": "inactive", "refunded": "inactive"}).fillna("unknown")  # map: missing key -> NaN
bucket_where = pd.Series("active", index=s.index).where(s.ne("cancelled"), "inactive")      # mirrors the buggy CASE
```
`np.select(conditions, choices, default)` mirrors CASE; `Series.map` with a dict is a simple CASE where unmapped keys (including NaN) become NaN; `where` keeps values where the condition is true and replaces the rest.

**Example:** Statuses: completed, cancelled, shipped, NULL, refunded, completed.
- `SQL_BUG` (`WHEN status <> 'cancelled' THEN 'active' ELSE 'inactive'`): the NULL row gets 'inactive' (the comparison is UNKNOWN, so the ELSE branch runs) and 'refunded' gets 'active'. Two miscategorised rows, no error.
- `SQL_FIX`: NULL becomes 'unknown', refunded 'inactive'. Result: active, inactive, active, unknown, inactive, active.
- `CASE status WHEN NULL THEN 'unknown' WHEN 'completed' THEN 'done' END`: the NULL row returns NULL, not 'unknown', and statuses without a WHEN (cancelled, shipped, refunded) return NULL because there is no ELSE.
- First match wins: with `WHEN status LIKE 'c%' THEN 'starts_with_c' WHEN status = 'completed' THEN 'completed'`, both completed rows return 'starts_with_c' and the second branch is never reached; cancelled also returns 'starts_with_c'.

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q44: CASE WHEN subtleties on SQLite, and np.select / map / where in pandas
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, status TEXT);
INSERT INTO orders VALUES
 (1,'completed'),(2,'cancelled'),(3,'shipped'),(4,NULL),(5,'refunded'),(6,'completed');
"""
# Buggy mapping: NULL status falls into ELSE
SQL_BUG = """
SELECT order_id, status,
       CASE WHEN status <> 'cancelled' THEN 'active' ELSE 'inactive' END AS bucket
FROM orders ORDER BY order_id
"""
# Fixed: handle NULL explicitly, first matching WHEN wins
SQL_FIX = """
SELECT order_id, status,
       CASE WHEN status IS NULL THEN 'unknown'
            WHEN status IN ('completed', 'shipped') THEN 'active'
            WHEN status IN ('cancelled', 'refunded') THEN 'inactive'
            ELSE 'other' END AS bucket
FROM orders ORDER BY order_id
"""
SQL_SIMPLE_NULL = """
SELECT order_id, CASE status WHEN NULL THEN 'unknown' WHEN 'completed' THEN 'done' END AS simple_case
FROM orders ORDER BY order_id
"""
SQL_ORDER = """
SELECT order_id, status,
       CASE WHEN status LIKE 'c%' THEN 'starts_with_c'
            WHEN status = 'completed' THEN 'completed' END AS first_match_wins
FROM orders ORDER BY order_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
print("BUG (<> with NULL goes to ELSE):\n", q(SQL_BUG))
sql_fix = q(SQL_FIX)
print("\nFIX:\n", sql_fix)
print("\nsimple CASE with WHEN NULL never matches; no ELSE gives NULL:\n", q(SQL_SIMPLE_NULL))
print("\nfirst match wins (row 1 and 6 would also match the second WHEN):\n", q(SQL_ORDER))
print("\nCASE WHEN NULL IS NULL THEN ... works:", con.execute("SELECT CASE WHEN NULL IS NULL THEN 'yes' ELSE 'no' END").fetchone()[0])

# Mixed result types: SQLite does not complain, typeof differs per row; PostgreSQL would reject (not executed)
mixed = con.execute("SELECT order_id, CASE WHEN order_id < 3 THEN 1 ELSE 'many' END AS v, typeof(CASE WHEN order_id < 3 THEN 1 ELSE 'many' END) FROM orders ORDER BY order_id").fetchall()
print("\nmixed integer/text branches in SQLite:", mixed)

orders = q("SELECT * FROM orders")
s = orders["status"]
# pd:main
conds = [s.isna(), s.isin(["completed", "shipped"]), s.isin(["cancelled", "refunded"])]
bucket_select = np.select(conds, ["unknown", "active", "inactive"], default="other")   # first True wins, like CASE
bucket_map = s.map({"completed": "active", "shipped": "active",
                    "cancelled": "inactive", "refunded": "inactive"}).fillna("unknown")  # map: missing key -> NaN
bucket_where = pd.Series("active", index=s.index).where(s.ne("cancelled"), "inactive")      # mirrors the buggy CASE
# pd:end
print("\nnp.select  :", bucket_select.tolist())
print("map+fillna :", bucket_map.tolist())
print("where (bug):", bucket_where.tolist(), "<- NaN != 'cancelled' is True, so NULL becomes 'active' here, not 'inactive' as in SQL")
assert bucket_select.tolist() == sql_fix["bucket"].tolist() == bucket_map.tolist()
print("assert: np.select == map+fillna == SQL fixed CASE (ordered by order_id)")

# np.select needs a default compatible with the choices
try:
    np.select([s == "completed"], ["done"])
except TypeError as e:
    print("np.select with string choices and the implicit default 0 ->", type(e).__name__)
print("np.select numeric choices, implicit default 0:", np.select([orders.order_id < 3], [10]).tolist())
print("np.select string choices, default=None:", np.select([s == "completed"], ["done"], default=None).tolist())
print("map with dict, unmapped and NaN keys -> NaN:", s.map({"completed": "done"}).tolist())
```

**Output (my run):**
```
BUG (<> with NULL goes to ELSE):
    order_id     status    bucket
0         1  completed    active
1         2  cancelled  inactive
2         3    shipped    active
3         4        NaN  inactive
4         5   refunded    active
5         6  completed    active

FIX:
    order_id     status    bucket
0         1  completed    active
1         2  cancelled  inactive
2         3    shipped    active
3         4        NaN   unknown
4         5   refunded  inactive
5         6  completed    active

simple CASE with WHEN NULL never matches; no ELSE gives NULL:
    order_id simple_case
0         1        done
1         2         NaN
2         3         NaN
3         4         NaN
4         5         NaN
5         6        done

first match wins (row 1 and 6 would also match the second WHEN):
    order_id     status first_match_wins
0         1  completed    starts_with_c
1         2  cancelled    starts_with_c
2         3    shipped              NaN
3         4        NaN              NaN
4         5   refunded              NaN
5         6  completed    starts_with_c

CASE WHEN NULL IS NULL THEN ... works: yes

mixed integer/text branches in SQLite: [(1, 1, 'integer'), (2, 1, 'integer'), (3, 'many', 'text'), (4, 'many', 'text'), (5, 'many', 'text'), (6, 'many', 'text')]

np.select  : ['active', 'inactive', 'active', 'unknown', 'inactive', 'active']
map+fillna : ['active', 'inactive', 'active', 'unknown', 'inactive', 'active']
where (bug): ['active', 'inactive', 'active', 'active', 'active', 'active'] <- NaN != 'cancelled' is True, so NULL becomes 'active' here, not 'inactive' as in SQL
assert: np.select == map+fillna == SQL fixed CASE (ordered by order_id)
np.select with string choices and the implicit default 0 -> TypeError
np.select numeric choices, implicit default 0: [10, 10, 0, 0, 0, 0]
np.select string choices, default=None: ['done', None, None, None, None, 'done']
map with dict, unmapped and NaN keys -> NaN: ['done', nan, nan, nan, nan, 'done']
```

**Edge cases:**
- NULL input: only `IS NULL` (or `COALESCE`) catches it; `CASE WHEN NULL IS NULL ...` works (the output prints yes).
- Mixed result types: SQLite returned an integer for some rows and text for others in the same column (`typeof` differs per row); PostgreSQL requires compatible branch types and would raise an error for integer and text branches (not executed here), and other engines may coerce silently or fail; keep branches the same type, with an explicit CAST.
- Evaluation order: branches are tested in order; engines may short-circuit, but do not rely on side-effect order (hedged).
- pandas: `Series.where(s.ne('cancelled'), 'inactive')` mirrors the buggy CASE but with a different NULL outcome (the NaN row becomes 'active' because `NaN != 'cancelled'` is True); `map` leaves NaN for unmapped keys; `np.select` with string choices and no default raises a `TypeError` in this numpy (the implicit default is the integer 0), numeric choices default to 0 silently, so always pass `default=`.

**Then explain:**
- **Searched versus simple:** simple CASE can only test equality of one expression; searched CASE can test anything.
- **First match wins:** order your WHENs from specific to general.
- **Missing ELSE is NULL:** often hides unmapped values; add an explicit `ELSE 'other'` or let NULL stand for 'unmapped' on purpose and test for it.
- **NULL:** put `WHEN col IS NULL` first, and prefer `IN (...)` lists over negations (`<>`, `NOT IN`), which let NULLs fall through to ELSE.
- **pandas:** same logic with `np.select`; for dict maps use `.map(...).fillna('unknown')`, and decide whether unmapped values should be 'other' or 'unknown'.

**Follow-ups:**
- *Can CASE appear in ORDER BY, GROUP BY, aggregates?* Yes (Q9, Q10, Q24).
- *COALESCE versus CASE?* COALESCE is shorthand for a CASE on IS NOT NULL (Q6).
- *How do you test a mapping?* Count rows per output bucket and check the buckets add up to the table's rows, as in Q45.

**Common mistakes:**
- `CASE x WHEN NULL`.
- `WHEN status <> 'cancelled'` assuming it covers NULL.
- Leaving out ELSE and then summing a NULL-heavy column.
- Overlapping WHENs in the wrong order.
- In pandas, `np.select` without `default`, or `map` without handling the NaN it produces.

---

### Q45 ⭐ 🔴 Mini case, messy orders table: orders(order_id, customer_id, amount, status, created_at) arrives with duplicate order_ids, NULL amounts, status spelling variants, negative amounts and future dates. Plan the profiling queries in SQL (counts, distinct, null rates, min/max, group by status) and the pandas cleaning steps, state what you would quarantine versus fix versus escalate, and how you would prove that a corrected revenue total reconciles to the source.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Profile first (row count versus distinct keys, null rates, min and max, status spellings, negatives, future dates), then cleanly separate what you fix (spelling, whitespace, exact duplicate rows), quarantine (conflicting duplicates, NULL amounts, future dates, negative non-refunds) and escalate (what the negatives and the conflicts mean), and prove the result with a bridge: source rows and amount equal clean plus removed plus quarantined.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, amount REAL, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1,101,500,'completed','2026-01-05'),
 (2,102,300,'Completed','2026-01-06'),
 (3,103,NULL,'completed','2026-01-07'),
 (4,104,-50,'refunded','2026-01-08'),
 (5,105,200,'shipped ','2026-02-01'),
 (5,105,200,'shipped ','2026-02-01'),
 (6,106,700,'COMPLETED','2026-02-03'),
 (6,106,750,'completed','2026-02-03'),
 (7,107,400,'cancelled','2027-03-01'),
 (8,108,150,'Cancelled','2026-03-02'),
 (9,109,-20,'completed','2026-03-03'),
 (10,110,100,NULL,'2026-03-04');
```

**SQL answer:** (same text as in the Code block, where it is executed on SQLite 3.45.1)
```sql
-- SQL_PROFILE
SELECT COUNT(*)                                   AS n_rows,
       COUNT(DISTINCT order_id)                   AS distinct_order_ids,
       SUM(amount IS NULL)                        AS null_amount,
       SUM(status IS NULL)                        AS null_status,
       MIN(amount)                                AS min_amount,
       MAX(amount)                                AS max_amount,
       SUM(amount < 0)                            AS negative_amounts,
       MIN(created_at)                            AS min_date,
       MAX(created_at)                            AS max_date,
       SUM(created_at > :as_of)                   AS future_dates,
       ROUND(100.0 * SUM(amount IS NULL) / COUNT(*), 2) AS null_amount_pct
FROM orders

-- SQL_STATUS_CLEAN
SELECT LOWER(TRIM(status)) AS status_clean, COUNT(*) AS n FROM orders GROUP BY status_clean ORDER BY status_clean

-- SQL_DUP_IDS
SELECT order_id, COUNT(*) AS n_rows, COUNT(DISTINCT amount || '|' || IFNULL(status,'') || '|' || created_at) AS n_versions
FROM orders GROUP BY order_id HAVING COUNT(*) > 1 ORDER BY order_id

-- SQL_VIEW
CREATE VIEW flagged AS
SELECT rowid AS rid, order_id, customer_id, amount,
       LOWER(TRIM(status)) AS status_clean, created_at,
       CASE
         WHEN rowid NOT IN (SELECT MIN(rowid) FROM orders
                            GROUP BY order_id, customer_id, amount, status, created_at) THEN 'exact_duplicate'
         WHEN order_id IN (SELECT order_id FROM (SELECT DISTINCT * FROM orders)
                           GROUP BY order_id HAVING COUNT(*) > 1) THEN 'conflicting_duplicate'
         WHEN amount IS NULL THEN 'null_amount'
         WHEN created_at > '2026-10-24' THEN 'future_date'
         WHEN amount < 0 AND LOWER(TRIM(status)) IS NOT 'refunded' THEN 'negative_not_refund'
         ELSE 'ok'
       END AS reason
FROM orders

-- SQL_BRIDGE
SELECT reason, COUNT(*) AS n_rows, COALESCE(SUM(amount), 0) AS amount_sum
FROM flagged GROUP BY reason ORDER BY reason
```
Profile query, normalised status counts, duplicate-id check, a view that tags each row with a reason, and a bridge query by reason. The as-of date is a fixed string (`2026-10-24`) so the run is repeatable; in production use the load date or `date('now')` (SQLite). `SUM(amount IS NULL)` counts true values because SQLite booleans are 0 and 1; PostgreSQL would need `COUNT(*) FILTER (WHERE ...)` or a CASE (hedged, not executed). The view uses plain subqueries (Part 3) to keep the first of exact duplicates and to find order_ids with more than one distinct version.

**pandas answer:** (same text as in the Code block)
```python
df = raw.copy()
df["status_clean"] = df["status"].str.strip().str.lower()
exact_dup = df.duplicated(subset=["order_id", "customer_id", "amount", "status", "created_at"], keep="first")
survivors = df[~exact_dup]
conflict_ids = survivors.loc[survivors["order_id"].duplicated(keep=False), "order_id"].unique()
df["reason"] = "ok"
df.loc[df["amount"].lt(0) & df["status_clean"].ne("refunded"), "reason"] = "negative_not_refund"
df.loc[df["created_at"] > AS_OF, "reason"] = "future_date"
df.loc[df["amount"].isna(), "reason"] = "null_amount"
df.loc[df["order_id"].isin(conflict_ids), "reason"] = "conflicting_duplicate"
df.loc[exact_dup, "reason"] = "exact_duplicate"          # later assignments override earlier ones = CASE order reversed
bridge_pd = (df.groupby("reason", as_index=False)
             .agg(n_rows=("rid", "size"), amount_sum=("amount", lambda s: s.sum())))
clean = df[df["reason"] == "ok"].assign(status_clean=lambda d: d["status_clean"].fillna("unknown"))
```
Normalise the status, flag exact duplicates, conflicting duplicates, NULL amounts, future dates and negative non-refunds, each into a `reason` column (later assignments override earlier ones, so I assign in the reverse of the CASE order), then `groupby('reason')` for the bridge.

**Example:** Twelve source rows (10 distinct order_ids), total amount 3230.0 (NULL ignored).
- Profile: 12 rows, 10 distinct order_ids, 1 NULL amount (8.33 percent), 1 NULL status, amounts from -50 to 750, 2 negatives, dates from 2026-01-05 to 2027-03-01, 1 date after the as-of date.
- Status spellings: 8 raw values (including 'shipped ' with a trailing space and NULL) collapse to 4 plus NULL: cancelled 2, completed 6, refunded 1, shipped 2, NULL 1.
- Duplicate ids: order 5 appears twice with identical content (exact copy: fix by keeping one); order 6 appears twice with amounts 700 and 750 (conflict: cannot know which is right).
- Row decisions: order 3 (NULL amount) quarantined; order 4 (-50, refunded) kept (a refund can be negative) and flagged for finance to confirm; order 7 (date in 2027) quarantined; order 9 (-20, completed) quarantined; order 10 (NULL status) kept as 'unknown'.
- Bridge: clean 6 rows / 1200.0; exact duplicate 1 row / 200.0; conflicting duplicate 2 rows / 1450.0; future date 1 / 400.0; negative non-refund 1 / -20.0; NULL amount 1 / 0.0. Rows: 6 + 1 + 2 + 1 + 1 + 1 = 12. Amount: 1200 + 200 + 1450 + 400 - 20 + 0 = 3230. It reconciles.
- Completed revenue: 1230.0 by exact match on 'completed', 2230.0 with only lower and trim (which also includes the quarantined 700, 750 and -20 rows), 800.0 after the flags (orders 1 and 2).

**Code:** (SQLite in memory plus pandas; asserts that the two results are equal; run with `python3 -I`)
```python
# Q45: profile, clean and reconcile a messy orders table (SQLite SQL + pandas), as-of date fixed for repeatability
import sqlite3
import pandas as pd

AS_OF = "2026-10-24"
SCHEMA = """
CREATE TABLE orders(order_id INTEGER, customer_id INTEGER, amount REAL, status TEXT, created_at TEXT);
INSERT INTO orders VALUES
 (1,101,500,'completed','2026-01-05'),
 (2,102,300,'Completed','2026-01-06'),
 (3,103,NULL,'completed','2026-01-07'),
 (4,104,-50,'refunded','2026-01-08'),
 (5,105,200,'shipped ','2026-02-01'),
 (5,105,200,'shipped ','2026-02-01'),
 (6,106,700,'COMPLETED','2026-02-03'),
 (6,106,750,'completed','2026-02-03'),
 (7,107,400,'cancelled','2027-03-01'),
 (8,108,150,'Cancelled','2026-03-02'),
 (9,109,-20,'completed','2026-03-03'),
 (10,110,100,NULL,'2026-03-04');
"""
SQL_PROFILE = """
SELECT COUNT(*)                                   AS n_rows,
       COUNT(DISTINCT order_id)                   AS distinct_order_ids,
       SUM(amount IS NULL)                        AS null_amount,
       SUM(status IS NULL)                        AS null_status,
       MIN(amount)                                AS min_amount,
       MAX(amount)                                AS max_amount,
       SUM(amount < 0)                            AS negative_amounts,
       MIN(created_at)                            AS min_date,
       MAX(created_at)                            AS max_date,
       SUM(created_at > :as_of)                   AS future_dates,
       ROUND(100.0 * SUM(amount IS NULL) / COUNT(*), 2) AS null_amount_pct
FROM orders
"""
SQL_STATUS = """
SELECT status, COUNT(*) AS n FROM orders GROUP BY status ORDER BY status
"""
SQL_STATUS_CLEAN = """
SELECT LOWER(TRIM(status)) AS status_clean, COUNT(*) AS n FROM orders GROUP BY status_clean ORDER BY status_clean
"""
SQL_DUP_IDS = """
SELECT order_id, COUNT(*) AS n_rows, COUNT(DISTINCT amount || '|' || IFNULL(status,'') || '|' || created_at) AS n_versions
FROM orders GROUP BY order_id HAVING COUNT(*) > 1 ORDER BY order_id
"""
SQL_VIEW = """
CREATE VIEW flagged AS
SELECT rowid AS rid, order_id, customer_id, amount,
       LOWER(TRIM(status)) AS status_clean, created_at,
       CASE
         WHEN rowid NOT IN (SELECT MIN(rowid) FROM orders
                            GROUP BY order_id, customer_id, amount, status, created_at) THEN 'exact_duplicate'
         WHEN order_id IN (SELECT order_id FROM (SELECT DISTINCT * FROM orders)
                           GROUP BY order_id HAVING COUNT(*) > 1) THEN 'conflicting_duplicate'
         WHEN amount IS NULL THEN 'null_amount'
         WHEN created_at > '2026-10-24' THEN 'future_date'
         WHEN amount < 0 AND LOWER(TRIM(status)) IS NOT 'refunded' THEN 'negative_not_refund'
         ELSE 'ok'
       END AS reason
FROM orders
"""
SQL_BRIDGE = """
SELECT reason, COUNT(*) AS n_rows, COALESCE(SUM(amount), 0) AS amount_sum
FROM flagged GROUP BY reason ORDER BY reason
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.executescript(SQL_VIEW)
q = lambda s, p=None: pd.read_sql_query(s, con, params=p or {})

print("PROFILE:\n", q(SQL_PROFILE, {"as_of": AS_OF}).T.rename(columns={0: "value"}))
print("\nraw statuses:\n", q(SQL_STATUS).assign(status=lambda d: d["status"].map(repr)))
print("\nnormalised statuses:\n", q(SQL_STATUS_CLEAN))
print("\nduplicated order_ids (n_versions = 1 exact copies, 2 conflicting):\n", q(SQL_DUP_IDS))
flag_sql = q("SELECT rid, order_id, reason FROM flagged ORDER BY rid")
print("\nrow flags (SQL view):\n", flag_sql)
bridge_sql = q(SQL_BRIDGE)
print("\nbridge by reason (SQL):\n", bridge_sql)

raw = q("SELECT rowid AS rid, * FROM orders ORDER BY rid")
# pd:main
df = raw.copy()
df["status_clean"] = df["status"].str.strip().str.lower()
exact_dup = df.duplicated(subset=["order_id", "customer_id", "amount", "status", "created_at"], keep="first")
survivors = df[~exact_dup]
conflict_ids = survivors.loc[survivors["order_id"].duplicated(keep=False), "order_id"].unique()
df["reason"] = "ok"
df.loc[df["amount"].lt(0) & df["status_clean"].ne("refunded"), "reason"] = "negative_not_refund"
df.loc[df["created_at"] > AS_OF, "reason"] = "future_date"
df.loc[df["amount"].isna(), "reason"] = "null_amount"
df.loc[df["order_id"].isin(conflict_ids), "reason"] = "conflicting_duplicate"
df.loc[exact_dup, "reason"] = "exact_duplicate"          # later assignments override earlier ones = CASE order reversed
bridge_pd = (df.groupby("reason", as_index=False)
             .agg(n_rows=("rid", "size"), amount_sum=("amount", lambda s: s.sum())))
clean = df[df["reason"] == "ok"].assign(status_clean=lambda d: d["status_clean"].fillna("unknown"))
# pd:end
print("\nbridge by reason (pandas):\n", bridge_pd)
pd.testing.assert_frame_equal(flag_sql, df[["rid", "order_id", "reason"]], check_dtype=False)
pd.testing.assert_frame_equal(bridge_sql, bridge_pd, check_dtype=False)
print("asserts passed: row flags and bridge table equal between SQL view and pandas (ordered by rid / reason)")

# Reconciliation: rows and amount must bridge back to the source exactly
src_rows, src_sum = con.execute("SELECT COUNT(*), SUM(amount) FROM orders").fetchone()
clean_rows, clean_sum = con.execute("SELECT COUNT(*), SUM(amount) FROM flagged WHERE reason = 'ok'").fetchone()
other = con.execute("SELECT COUNT(*), COALESCE(SUM(amount),0) FROM flagged WHERE reason <> 'ok'").fetchone()
print(f"\nsource: {src_rows} rows, amount {src_sum} | clean: {clean_rows} rows, amount {clean_sum} | removed or quarantined: {other[0]} rows, amount {other[1]}")
assert src_rows == clean_rows + other[0] and abs(src_sum - (clean_sum + other[1])) < 1e-9
assert clean["amount"].sum() == clean_sum and len(clean) == clean_rows
print("assert: source rows = clean + removed; source amount = clean + removed (to the paisa)")

# The number the business cares about, before and after
raw_completed = con.execute("SELECT SUM(amount) FROM orders WHERE status = 'completed'").fetchone()[0]
naive_completed = con.execute("SELECT SUM(amount) FROM orders WHERE LOWER(TRIM(status)) = 'completed'").fetchone()[0]
clean_completed = con.execute("SELECT SUM(amount) FROM flagged WHERE reason = 'ok' AND status_clean = 'completed'").fetchone()[0]
print("\ncompleted revenue: exact-match status", raw_completed, "| lower+trim only", naive_completed, "| clean (flags applied)", clean_completed)
assert clean.loc[clean["status_clean"] == "completed", "amount"].sum() == clean_completed == 800
print("assert: pandas clean completed revenue == SQL clean == 800")
```

**Output (my run):**
```
PROFILE:
                          value
n_rows                      12
distinct_order_ids          10
null_amount                  1
null_status                  1
min_amount               -50.0
max_amount               750.0
negative_amounts             2
min_date            2026-01-05
max_date            2027-03-01
future_dates                 1
null_amount_pct           8.33

raw statuses:
         status  n
0          nan  1
1  'COMPLETED'  1
2  'Cancelled'  1
3  'Completed'  1
4  'cancelled'  1
5  'completed'  4
6   'refunded'  1
7   'shipped '  2

normalised statuses:
   status_clean  n
0          NaN  1
1    cancelled  2
2    completed  6
3     refunded  1
4      shipped  2

duplicated order_ids (n_versions = 1 exact copies, 2 conflicting):
    order_id  n_rows  n_versions
0         5       2           1
1         6       2           2

row flags (SQL view):
     rid  order_id                 reason
0     1         1                     ok
1     2         2                     ok
2     3         3            null_amount
3     4         4                     ok
4     5         5                     ok
5     6         5        exact_duplicate
6     7         6  conflicting_duplicate
7     8         6  conflicting_duplicate
8     9         7            future_date
9    10         8                     ok
10   11         9    negative_not_refund
11   12        10                     ok

bridge by reason (SQL):
                   reason  n_rows  amount_sum
0  conflicting_duplicate       2      1450.0
1        exact_duplicate       1       200.0
2            future_date       1       400.0
3    negative_not_refund       1       -20.0
4            null_amount       1         0.0
5                     ok       6      1200.0

bridge by reason (pandas):
                   reason  n_rows  amount_sum
0  conflicting_duplicate       2      1450.0
1        exact_duplicate       1       200.0
2            future_date       1       400.0
3    negative_not_refund       1       -20.0
4            null_amount       1         0.0
5                     ok       6      1200.0
asserts passed: row flags and bridge table equal between SQL view and pandas (ordered by rid / reason)

source: 12 rows, amount 3230.0 | clean: 6 rows, amount 1200.0 | removed or quarantined: 6 rows, amount 2030.0
assert: source rows = clean + removed; source amount = clean + removed (to the paisa)

completed revenue: exact-match status 1230.0 | lower+trim only 2230.0 | clean (flags applied) 800.0
assert: pandas clean completed revenue == SQL clean == 800
```

**Edge cases:**
- Which rule order matters: exact duplicates first, then conflicting duplicates, then NULLs, dates, negatives. A different order changes the bridge numbers (and a CASE returns the first match only).
- NULL amounts: `SUM` ignores them, so they are invisible in the amount bridge; count them in the row bridge.
- Negative amounts: refunds can be legitimate; the rule here is a business assumption to confirm, not a fact.
- Future dates: could be time-zone issues or typos; quarantine, do not silently clip.
- Conflicting duplicates: keep both in quarantine; never pick by max or latest without a rule (no updated_at column here).
- Rounding: amounts are REAL; money in practice should be integer paise (Q40).
- Customer_id null rate, id formats and referential integrity checks (against a customers table) would be added in a real profile (not in this toy).

**Then explain:**
- **Profile before cleaning:** counts, `COUNT(DISTINCT key)` versus `COUNT(*)`, null rates per column, min and max of amounts and dates, `GROUP BY` on raw status, and a duplicate-key query. Record the numbers: they are the 'before' of the reconciliation.
- **Fix** (safe, reversible, rule-based): status case and whitespace, exact duplicate rows, NULL status to 'unknown' while keeping the row.
- **Quarantine** (hold in a separate table with a reason, do not delete): conflicting duplicates, NULL amounts, future dates, negatives that are not refunds.
- **Escalate** (needs a decision from the owner): are negatives refunds, which duplicate version is right, are future dates a feed bug, what happens to NULL status.
- **Prove it:** a bridge table with source = clean + removed + quarantined for rows and for amount, asserted in code; also recompute the headline metric from the raw table and explain each difference, as in the completed revenue line.
- **pandas versus SQL:** same flags and the same bridge (asserted in the Code block).

**Follow-ups:**
- *How would you automate this?* A scheduled checks job with thresholds (null rate, duplicate rate, row-count drift) that fails the load, writes quarantined rows and alerts (tooling is Book 4).
- *What if the business wants the dedup to keep the latest version?* Needs a version column; window functions (Part 4).
- *Keep or delete the quarantined rows?* Keep them, with the reason, so the bridge can be re-run.

**Common mistakes:**
- Cleaning silently and reporting a new number nobody can reconcile.
- Deleting suspicious rows instead of quarantining them.
- Trusting `DISTINCT` or `drop_duplicates()` on order_id alone and losing conflicting versions.
- Normalising status in one query but not in the revenue metric.
- Treating all negatives as errors (refunds) or all as valid.

