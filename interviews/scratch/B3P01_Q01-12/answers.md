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
