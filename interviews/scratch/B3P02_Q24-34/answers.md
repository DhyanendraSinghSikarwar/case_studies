### Q24 ⭐⭐ 🟢 Anti-join and semi-join in pandas: customers(customer_id, name) and orders(order_id, customer_id). Write customers with no orders and customers with at least one order using (a) merge(how='left', indicator=True) with a _merge filter, (b) ~isin and isin, and (c) merge on drop_duplicates keys. Explain which is fastest conceptually, what happens with NaN in isin, and the SQL NOT IN NULL trap that does not exist in isin.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** In pandas, "no orders" is `~customers.customer_id.isin(orders.customer_id)` and "has orders" is `isin`; the merge forms (`indicator=True` then filter `_merge`, or an inner merge on deduplicated keys) give the same rows, and unlike SQL `NOT IN`, a NaN in the orders keys does not wipe out the result.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);  -- NULL = guest checkout
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (101,1),(102,1),(103,2),(104,NULL);
```

**SQL answer:** (the reference result; same text as in the Code block)
```sql
SELECT c.customer_id, c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
```
```sql
SELECT c.customer_id, c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
```
Anti-join is `NOT EXISTS`, semi-join is `EXISTS`. The `NOT IN` version is also in the Code block, only to show that it returns zero rows here (Part 1 Q13 and Part 2 Q2 cover that trap).

**pandas answer:** (same text as in the Code block)
```python
# (a) merge + indicator, then filter _merge
m = customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id",
                    how="left", indicator=True, validate="one_to_one")
anti_a = m.loc[m["_merge"] == "left_only", ["customer_id", "name"]]
semi_a = m.loc[m["_merge"] == "both", ["customer_id", "name"]]
```
```python
# (b) isin
anti_b = customers[~customers["customer_id"].isin(orders["customer_id"])]
semi_b = customers[customers["customer_id"].isin(orders["customer_id"])]
```
```python
# (c) inner merge on deduplicated keys (semi-join only)
keys = orders[["customer_id"]].drop_duplicates()
semi_c = customers.merge(keys, on="customer_id", how="inner")
```
In (a) and (c) the orders side is reduced to its distinct key first, so the merge cannot repeat a customer. `validate="one_to_one"` makes pandas check that for me.

**Example:** Customers are 1 Asha, 2 Ben, 3 Chitra, 4 Dev. Orders belong to 1, 1, 2 and a guest (NULL). Distinct order keys: {1, 2, NaN}. Left-merge with indicator: Asha and Ben are `both`, Chitra and Dev are `left_only`. So anti-join = Chitra, Dev and semi-join = Asha, Ben. Without the `drop_duplicates`, Asha would appear twice (two orders), exactly like a plain SQL JOIN.

**Code:** (run with `python3 -I`; the SQL and pandas results are compared as lists of (customer_id, name) sorted by customer_id)
```python
# Q24: anti-join and semi-join in pandas (merge+indicator, isin, merge on deduplicated keys) vs SQL
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

# sql:anti
SQL_ANTI = """
SELECT c.customer_id, c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
"""
# end
# sql:semi
SQL_SEMI = """
SELECT c.customer_id, c.name FROM customers c
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.customer_id
"""
# end
SQL_NOT_IN = "SELECT customer_id, name FROM customers WHERE customer_id NOT IN (SELECT customer_id FROM orders)"

def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
sql_anti, sql_semi = sql(SQL_ANTI), sql(SQL_SEMI)
print("SQL anti (NOT EXISTS):", sql_anti)
print("SQL semi (EXISTS):    ", sql_semi)
print("SQL NOT IN with a NULL in orders:", sql(SQL_NOT_IN))

customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("\norders.customer_id dtype:", orders["customer_id"].dtype, "| customers.customer_id dtype:", customers["customer_id"].dtype)

def rows(df): return [tuple(r) for r in df[["customer_id", "name"]].sort_values("customer_id").itertuples(index=False, name=None)]

# pd:a
m = customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id",
                    how="left", indicator=True, validate="one_to_one")
anti_a = m.loc[m["_merge"] == "left_only", ["customer_id", "name"]]
semi_a = m.loc[m["_merge"] == "both", ["customer_id", "name"]]
# end
# pd:b
anti_b = customers[~customers["customer_id"].isin(orders["customer_id"])]
semi_b = customers[customers["customer_id"].isin(orders["customer_id"])]
# end
# pd:c
keys = orders[["customer_id"]].drop_duplicates()
semi_c = customers.merge(keys, on="customer_id", how="inner")
# end
print("\n(a) merge indicator counts:", m["_merge"].value_counts().to_dict())
print("(a) anti:", rows(anti_a), "| semi:", rows(semi_a))
print("(b) anti:", rows(anti_b), "| semi:", rows(semi_b))
print("(c) semi:", rows(semi_c))
assert rows(anti_a) == rows(anti_b) == sql_anti
assert rows(semi_a) == rows(semi_b) == rows(semi_c) == sql_semi
assert len(m) == len(customers)   # validate='one_to_one' + dedup kept the grain at one row per customer

# what goes wrong without drop_duplicates: Asha has two orders
dup = customers.merge(orders[["customer_id"]], on="customer_id", how="inner")
print("\ninner merge WITHOUT drop_duplicates:", dup["name"].tolist(), "(Asha twice, a plain JOIN fan-out)")
try:
    customers.merge(orders[["customer_id"]], on="customer_id", validate="one_to_one")
except pd.errors.MergeError as e:
    print("validate='one_to_one' on the raw orders ->", type(e).__name__, "|", str(e).splitlines()[0])

# NaN in isin: NaN matches NaN. In the SQL NOT IN, a NULL in the subquery kills every row.
print("\nisin with NaN:", pd.Series([1.0, 3.0, np.nan]).isin([1.0, np.nan]).tolist())
cust_nan = pd.DataFrame({"customer_id": [1.0, 3.0, np.nan], "name": ["Asha", "Chitra", "NoKey"]})
print("~isin where BOTH sides have NaN keeps:", cust_nan[~cust_nan["customer_id"].isin(orders["customer_id"])]["name"].tolist(),
      "(NoKey is treated as having an order)")
print("~isin after orders keys .dropna() keeps:",
      cust_nan[~cust_nan["customer_id"].isin(orders["customer_id"].dropna())]["name"].tolist())
print("merge also matches NaN to NaN:",
      cust_nan.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)[["name", "_merge"]].values.tolist())

# dtype note: int64 keys against float64 keys (NaN made orders float) merge fine; int against str raises
try:
    customers.merge(pd.DataFrame({"customer_id": ["1", "2"]}), on="customer_id")
except ValueError as e:
    print("\nint64 vs str key ->", type(e).__name__, "|", str(e)[:75])
print("asserts passed")
```

**Output (my run):**
```text
SQL anti (NOT EXISTS): [(3, 'Chitra'), (4, 'Dev')]
SQL semi (EXISTS):     [(1, 'Asha'), (2, 'Ben')]
SQL NOT IN with a NULL in orders: []

orders.customer_id dtype: float64 | customers.customer_id dtype: int64

(a) merge indicator counts: {'left_only': 2, 'both': 2, 'right_only': 0}
(a) anti: [(3, 'Chitra'), (4, 'Dev')] | semi: [(1, 'Asha'), (2, 'Ben')]
(b) anti: [(3, 'Chitra'), (4, 'Dev')] | semi: [(1, 'Asha'), (2, 'Ben')]
(c) semi: [(1, 'Asha'), (2, 'Ben')]

inner merge WITHOUT drop_duplicates: ['Asha', 'Asha', 'Ben'] (Asha twice, a plain JOIN fan-out)
validate='one_to_one' on the raw orders -> MergeError | Merge keys are not unique in right dataset; not a one-to-one merge

isin with NaN: [True, False, True]
~isin where BOTH sides have NaN keeps: ['Chitra'] (NoKey is treated as having an order)
~isin after orders keys .dropna() keeps: ['Chitra', 'NoKey']
merge also matches NaN to NaN: [['Asha', 'both'], ['Chitra', 'left_only'], ['NoKey', 'both']]

int64 vs str key -> ValueError | You are trying to merge on int64 and str columns for key 'customer_id'. If 
asserts passed
```

**Edge cases:**
- **Duplicate order rows:** semi-join by plain merge repeats the customer once per order. Deduplicate the keys first, or use `isin`, which returns each customer once.
- **NaN in `isin`:** `isin` treats NaN as equal to NaN (output: `[True, False, True]`). With NaN keys on both sides, a customer whose key is NaN counts as "has an order" (`NoKey` vanished from the anti-join). Drop NaN from the keys if that is not what you want. This is the opposite of SQL, where NULL never equals NULL.
- **The SQL `NOT IN` trap does not exist in `isin`:** the SQL `NOT IN` returned `[]` because of the guest NULL; `~isin` returned Chitra and Dev, because `isin` is a plain yes/no membership test with no UNKNOWN state.
- **Merge also matches NaN to NaN** (`NoKey` came back as `both`). I confirmed this by running it on pandas 3.0.5; it is a pandas behaviour, not SQL behaviour.
- **dtype:** the NULL turned `orders.customer_id` into float64 while `customers.customer_id` is int64. Merge and `isin` still match 1 with 1.0. An int key against a string key raises `ValueError` (printed above); that belongs to Q35.
- **Empty orders table:** the anti-join returns all customers and the semi-join none.

**Then explain:**
- **(a) merge with indicator** is the literal LEFT JOIN ... IS NULL: `left_only` is the unmatched rows, `both` the matched ones. It is the most explicit and lets you see both groups in one pass.
- **(b) isin** is a membership test: pandas hashes the orders keys once and probes each customer. For an existence check I would use this first; it is short and cannot change the number of rows.
- **(c) merge on deduplicated keys** is the "JOIN plus DISTINCT" semi-join. It is useful when you want to bring columns across, but then deduplicate to the grain you need first.
- **Which is fastest, conceptually:** all three are hash-based and linear in the sizes. `isin` should do the least work because it builds no result frame with the orders columns and no `_merge` column; the merges allocate a joined frame. I did not benchmark it here, so treat it as expected, not measured. On big data, measure.
- **Choosing:** `isin` for a pure filter, merge when you need columns from the right table or want the `_merge` audit.
- **SQL side:** the dialect-independent safe forms are `NOT EXISTS` and `EXISTS`. I only ran SQLite here, so Postgres, MySQL, BigQuery and Snowflake behaviour of `NOT IN` is from memory (not executed), though the NULL rule is standard.

**Follow-ups:**
- *How do I get SQL-like NOT IN behaviour in pandas?* Say what you want: `if orders["customer_id"].isna().any(): result = empty` replicates SQL; usually you do not want that, so drop the NaN keys and filter.
- *Why not `merge` without `drop_duplicates` for the semi-join?* It repeats customers once per order.
- *How would you catch a changed grain?* `validate="one_to_one"` or `"many_to_one"` and an `assert len(result) == len(customers)`.

**Common mistakes:**
- Using `merge(how="inner")` on raw orders and reporting inflated customers.
- Filtering `_merge == "left_only"` without `indicator=True`, or checking `isna()` on a right column that can itself be NULL, instead of the `_merge` flag.
- Writing `customers[~customers.customer_id.isin(orders.customer_id)]` and assuming NaN keys are excluded; they match each other.
- Assuming `isin` has the SQL `NOT IN` NULL trap, or that SQL `NOT IN` is as forgiving as `~isin`.

### Q25 ⭐⭐ 🟡 Non-equi join with bands: employees(emp_id, name, salary) and grades(grade, min_salary, max_salary). Assign each employee a grade with a range join. Explain what happens at boundary values when ranges overlap or use BETWEEN on both ends (an employee gets two grades), how to define half-open ranges, and show pandas options (cross merge then filter, pd.cut or IntervalIndex, merge_asof on min_salary).
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** A band lookup is a non-equi join (`ON salary >= min AND salary < max`); store the bands half-open so every salary falls in exactly one band, because `BETWEEN` on both ends gives an employee on a shared edge two grades.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
CREATE TABLE grades(grade TEXT PRIMARY KEY, min_salary INTEGER, max_salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',30),(2,'Ben',50),(3,'Chitra',75),(4,'Dev',100),(5,'Esha',150),(6,'Farid',250);
INSERT INTO grades VALUES ('C',0,50),('B',50,100),('A',100,200);
```
(The salaries are toy column values. The bands share their edges: C ends at 50 where B starts, B ends at 100 where A starts.)

**SQL answer:** (same text as in the Code block)
```sql
SELECT e.emp_id, e.name, e.salary, g.grade
FROM employees e
LEFT JOIN grades g ON e.salary >= g.min_salary AND e.salary < g.max_salary
ORDER BY e.emp_id
```
The `BETWEEN` version, which is the trap:
```sql
SELECT e.emp_id, e.name, e.salary, g.grade
FROM employees e
LEFT JOIN grades g ON e.salary BETWEEN g.min_salary AND g.max_salary
ORDER BY e.emp_id, g.grade
```
I use `LEFT JOIN` so an employee above every band (Farid, 250) is kept with a NULL grade instead of silently disappearing.

**pandas answer:** (same text as in the Code block; all four give the same result)
```python
# 1. cross merge then filter (the literal non-equi join)
x = employees.merge(grades, how="cross")
x = x[(x["salary"] >= x["min_salary"]) & (x["salary"] < x["max_salary"])]
p_cross = employees.merge(x[["emp_id", "grade"]], on="emp_id", how="left", validate="one_to_one")
```
```python
# 2. pd.cut with right=False (half-open)
bins = [0, 50, 100, 200]                      # edges taken from the grade table, sorted
p_cut = employees.assign(grade=pd.cut(employees["salary"], bins=bins, right=False,
                                      labels=["C", "B", "A"]).astype(object))
```
```python
# 3. IntervalIndex lookup
iv = pd.IntervalIndex.from_arrays(grades["min_salary"], grades["max_salary"], closed="left")
idx = iv.get_indexer(employees["salary"])    # -1 when no interval contains the value
p_interval = employees.assign(grade=np.where(idx >= 0, grades["grade"].to_numpy()[idx], None))
```
```python
# 4. merge_asof on the lower bound, then check the upper bound
asof = pd.merge_asof(employees.sort_values("salary"), grades.sort_values("min_salary"),
                     left_on="salary", right_on="min_salary", direction="backward")
asof["grade"] = asof["grade"].where(asof["salary"] < asof["max_salary"])   # asof ignores the upper edge
p_asof = asof.sort_values("emp_id")[["emp_id", "name", "salary", "grade"]]
```

**Example:** Ben earns 50. Under `BETWEEN`, 50 is inside C (0 to 50) and inside B (50 to 100), so Ben gets two rows. Dev earns 100, the edge of B and A, so Dev gets two rows. 6 employees become 8 rows. With half-open bands `[min, max)`, 50 belongs only to B (50 >= 50 and 50 < 100) and 100 only to A. Farid at 250 is outside every band, so he keeps a NULL grade through the LEFT JOIN.

**Code:** (run with `python3 -I`; each pandas result is compared with the half-open SQL result as a list of (emp_id, name, salary, grade) sorted by emp_id)
```python
# Q25: non-equi (range) join with salary bands: BETWEEN overlap vs half-open, plus pandas options
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, salary INTEGER);
CREATE TABLE grades(grade TEXT PRIMARY KEY, min_salary INTEGER, max_salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',30),(2,'Ben',50),(3,'Chitra',75),(4,'Dev',100),(5,'Esha',150),(6,'Farid',250);
INSERT INTO grades VALUES ('C',0,50),('B',50,100),('A',100,200);
""")

# sql:between
SQL_BETWEEN = """
SELECT e.emp_id, e.name, e.salary, g.grade
FROM employees e
LEFT JOIN grades g ON e.salary BETWEEN g.min_salary AND g.max_salary
ORDER BY e.emp_id, g.grade
"""
# end
# sql:main
SQL_MAIN = """
SELECT e.emp_id, e.name, e.salary, g.grade
FROM employees e
LEFT JOIN grades g ON e.salary >= g.min_salary AND e.salary < g.max_salary
ORDER BY e.emp_id
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
sql_between, sql_main = sql(SQL_BETWEEN), sql(SQL_MAIN)
print("BETWEEN on both ends (bands share their edges):")
for r in sql_between: print("  ", r)
print("rows:", len(sql_between), "for", 6, "employees")
print("\nhalf-open [min, max):")
for r in sql_main: print("  ", r)

employees = pd.read_sql_query("SELECT * FROM employees", con)
grades = pd.read_sql_query("SELECT * FROM grades", con)

# pd:cross
x = employees.merge(grades, how="cross")
x = x[(x["salary"] >= x["min_salary"]) & (x["salary"] < x["max_salary"])]
p_cross = employees.merge(x[["emp_id", "grade"]], on="emp_id", how="left", validate="one_to_one")
# end
# pd:cut
bins = [0, 50, 100, 200]                      # edges taken from the grade table, sorted
p_cut = employees.assign(grade=pd.cut(employees["salary"], bins=bins, right=False,
                                      labels=["C", "B", "A"]).astype(object))
# end
# pd:interval
iv = pd.IntervalIndex.from_arrays(grades["min_salary"], grades["max_salary"], closed="left")
idx = iv.get_indexer(employees["salary"])    # -1 when no interval contains the value
p_interval = employees.assign(grade=np.where(idx >= 0, grades["grade"].to_numpy()[idx], None))
# end
# pd:asof
asof = pd.merge_asof(employees.sort_values("salary"), grades.sort_values("min_salary"),
                     left_on="salary", right_on="min_salary", direction="backward")
asof["grade"] = asof["grade"].where(asof["salary"] < asof["max_salary"])   # asof ignores the upper edge
p_asof = asof.sort_values("emp_id")[["emp_id", "name", "salary", "grade"]]
# end
def norm(df):
    d = df[["emp_id", "name", "salary", "grade"]].sort_values("emp_id")
    return [(int(a), b, int(c), None if pd.isna(g) else g) for a, b, c, g in d.itertuples(index=False, name=None)]
ref = norm(pd.DataFrame(sql_main, columns=["emp_id", "name", "salary", "grade"]))
for name, df in [("cross+filter", p_cross), ("pd.cut", p_cut), ("IntervalIndex", p_interval), ("merge_asof", p_asof)]:
    assert norm(df) == ref, name
    print(f"pandas {name:14s} == SQL half-open:", norm(df) == ref)

# merge_asof WITHOUT the upper-edge check wrongly grades Farid (250)
raw = pd.merge_asof(employees.sort_values("salary"), grades.sort_values("min_salary"),
                    left_on="salary", right_on="min_salary")
print("\nmerge_asof without the max_salary check, Farid ->", raw.loc[raw["name"] == "Farid", "grade"].iloc[0])
dupes = pd.DataFrame(sql_between, columns=["emp_id", "name", "salary", "grade"]).groupby("emp_id").size()
print("employees with 2 grades under BETWEEN:", dupes[dupes > 1].index.tolist())
print("asserts passed")
```

**Output (my run):**
```text
BETWEEN on both ends (bands share their edges):
   (1, 'Asha', 30, 'C')
   (2, 'Ben', 50, 'B')
   (2, 'Ben', 50, 'C')
   (3, 'Chitra', 75, 'B')
   (4, 'Dev', 100, 'A')
   (4, 'Dev', 100, 'B')
   (5, 'Esha', 150, 'A')
   (6, 'Farid', 250, None)
rows: 8 for 6 employees

half-open [min, max):
   (1, 'Asha', 30, 'C')
   (2, 'Ben', 50, 'B')
   (3, 'Chitra', 75, 'B')
   (4, 'Dev', 100, 'A')
   (5, 'Esha', 150, 'A')
   (6, 'Farid', 250, None)
pandas cross+filter   == SQL half-open: True
pandas pd.cut         == SQL half-open: True
pandas IntervalIndex  == SQL half-open: True
pandas merge_asof     == SQL half-open: True

merge_asof without the max_salary check, Farid -> A
employees with 2 grades under BETWEEN: [2, 4]
asserts passed
```

**Edge cases:**
- **Shared edges with `BETWEEN`:** Ben and Dev were duplicated (row count 8 instead of 6). Any later `SUM` or `COUNT` per employee would double count them (the fan-out of Q12).
- **Gaps:** if the bands were 0-49 and 51-100, a salary of 50 (or 50.5) would match nothing; with a LEFT JOIN you see a NULL grade, with an INNER JOIN the employee vanishes.
- **Above the top band:** Farid has NULL. Decide whether that is a data error or a catch-all grade.
- **NULL salary:** every comparison is UNKNOWN, so the LEFT JOIN keeps the employee with a NULL grade (not run in the sample data; standard SQL rule). In pandas, `merge_asof` raises `ValueError: Merge keys contain null values on left side` (I confirmed this message by running a one-off check on pandas 3.0.5), while `pd.cut` gives NaN.
- **Float salaries** are why half-open bands matter: with integer bands `0-49, 50-99` a salary of 49.5 falls through; `[0, 50)` does not.
- **merge_asof surprise:** it only looks backward at the lower bound, so Farid got grade A (row printed above) until I added the upper-bound check.

**Then explain:**
- **Non-equi join:** the join condition uses `<`, `>=` or `BETWEEN` instead of `=`. Engines cannot hash it, so the work is roughly employees x grades (a nested loop, concept-level and engine dependent). Fine for a handful of bands, expensive for two big tables.
- **Half-open ranges:** write `min <= x AND x < max`, and have each band's `max` equal the next band's `min`. No overlaps and no gaps by construction. Enforce it with a check query on the band table (Q26 shows the overlap check).
- **pandas options:** cross merge then filter is the literal translation but builds employees x grades rows before filtering (see Q31 for the memory risk). `pd.cut` and `IntervalIndex` are lookups; they need bands that do not overlap and have no gaps. `merge_asof` is fast and also needs sorted, non-overlapping bands, and needs the manual upper-bound check.
- `pd.cut` with `right=False` is the half-open version; its default `right=True` gives `(a, b]`, the opposite edge, so check which edge you want.
- I only ran SQLite here. Other engines accept the same `ON` conditions (standard SQL), not executed.

**Follow-ups:**
- *How do you prevent overlapping bands in the data?* A check query or constraint on the band table, then half-open boundaries.
- *What if the bands come with an inclusive max, like 0-49?* Use `salary BETWEEN min AND max` for integers only, and say that a decimal salary can fall into the gap.
- *Can the join be an equi-join?* Only if you first compute a band key (for example `salary / 50`), which works for equal-width bands.

**Common mistakes:**
- `BETWEEN` with bands that share an edge, then not noticing duplicates.
- An INNER JOIN that silently drops employees outside every band.
- Using `merge_asof` and forgetting the upper bound, or forgetting that both sides must be sorted.
- Cross merge on large frames without checking `len(a) * len(b)` first.

### Q26 ⭐⭐ 🟡 Join on date ranges: price_history(product_id, price, valid_from, valid_to) with valid_to NULL for the current price, and orders(order_id, product_id, order_date, qty). Price each order at the price valid on order_date. Explain the BETWEEN with open-ended NULL trap, what a gap or an overlap in the history does (zero rows or duplicate rows), and how you would check the history for overlaps. Give pandas (merge on product_id then filter, or merge_asof).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Join orders to the price row whose window contains the order date, `valid_from <= order_date AND (valid_to IS NULL OR order_date <= valid_to)`; `BETWEEN valid_from AND valid_to` silently loses every order on the current price because `valid_to` is NULL, and gaps or overlaps in the history give zero rows or duplicate rows.

**Schema and sample data:**
```sql
CREATE TABLE price_history(product_id INTEGER, price REAL, valid_from TEXT, valid_to TEXT);  -- valid_to NULL = current
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, product_id INTEGER, order_date TEXT, qty INTEGER);
INSERT INTO price_history VALUES
 (1,10.0,'2024-01-01','2024-01-31'),(1,12.0,'2024-02-01',NULL),        -- clean history
 (2, 5.0,'2024-01-01','2024-01-10'),(2, 6.0,'2024-01-15',NULL),        -- gap 11-14 Jan
 (3,20.0,'2024-01-01','2024-01-31'),(3,22.0,'2024-01-20',NULL);        -- overlap 20-31 Jan
INSERT INTO orders VALUES
 (1,1,'2024-01-15',2),(2,1,'2024-02-01',1),(3,1,'2024-03-10',4),(4,1,'2023-12-31',1),
 (5,2,'2024-01-12',3),(6,3,'2024-01-25',1);
```
`valid_to` is inclusive here (the last day the price applies); dates are ISO text, which compares correctly as text in SQLite.

**SQL answer:** (same text as in the Code block)
```sql
SELECT o.order_id, o.product_id, o.order_date, p.price, o.qty * p.price AS revenue
FROM orders o
LEFT JOIN price_history p
  ON p.product_id = o.product_id
 AND p.valid_from <= o.order_date
 AND (p.valid_to IS NULL OR o.order_date <= p.valid_to)
ORDER BY o.order_id, p.valid_from
```
The trap version:
```sql
SELECT o.order_id, p.price
FROM orders o
LEFT JOIN price_history p
  ON p.product_id = o.product_id AND o.order_date BETWEEN p.valid_from AND p.valid_to
ORDER BY o.order_id
```
History checks. Overlap: a later version starts on or before the end of an earlier one (an open end counts as far future):
```sql
SELECT a.product_id, a.valid_from AS a_from, a.valid_to AS a_to, b.valid_from AS b_from, b.valid_to AS b_to
FROM price_history a
JOIN price_history b
  ON a.product_id = b.product_id
 AND a.valid_from < b.valid_from
 AND b.valid_from <= COALESCE(a.valid_to, '9999-12-31')
ORDER BY a.product_id, a.valid_from
```
Gap: the day after a version ends must fall inside some version:
```sql
SELECT a.product_id, a.valid_to AS ends_on, date(a.valid_to, '+1 day') AS uncovered_day
FROM price_history a
WHERE a.valid_to IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM price_history b
                  WHERE b.product_id = a.product_id
                    AND b.valid_from <= date(a.valid_to, '+1 day')
                    AND COALESCE(b.valid_to, '9999-12-31') >= date(a.valid_to, '+1 day'))
ORDER BY a.product_id
```

**pandas answer:** (same text as in the Code block)
```python
# merge on product_id, filter the window, then merge back so unpriced orders stay
m = orders.merge(ph, on="product_id", how="left")
ok = (m["valid_from"] <= m["order_date"]) & (m["valid_to"].isna() | (m["order_date"] <= m["valid_to"]))
hit = m.loc[ok, ["order_id", "price", "valid_from"]]
p_main = orders.merge(hit, on="order_id", how="left")
p_main["revenue"] = p_main["qty"] * p_main["price"]
```
```python
# merge_asof: latest valid_from <= order_date per product, then check valid_to
a = pd.merge_asof(orders.sort_values("order_date"), ph.sort_values("valid_from"),
                  left_on="order_date", right_on="valid_from", by="product_id", direction="backward")
a["price"] = a["price"].where(a["valid_to"].isna() | (a["order_date"] <= a["valid_to"]))
```

**Example:** Product 1 has 10.0 up to 31 Jan and 12.0 from 1 Feb with no end. Order 1 (15 Jan) gets 10.0. Order 2 (1 Feb) and order 3 (10 Mar) fall in the open-ended row and get 12.0. With `BETWEEN`, `o.order_date BETWEEN '2024-02-01' AND NULL` is UNKNOWN, so orders 2 and 3 get a NULL price (the `Output` shows `None` for them). Order 4 (31 Dec 2023) is before the history, no row matches, NULL. Order 5 (product 2, 12 Jan) is in the gap, NULL. Order 6 (product 3, 25 Jan) is in the overlap, so it matches both 20.0 and 22.0 and appears twice; its revenue is counted twice if you sum.

**Code:** (run with `python3 -I`; pandas is compared with SQL on (order_id, price) sorted by order_id, price)
```python
# Q26: price each order at the price valid on order_date; BETWEEN/NULL trap, gaps, overlaps, checks
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE price_history(product_id INTEGER, price REAL, valid_from TEXT, valid_to TEXT);  -- valid_to NULL = current
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, product_id INTEGER, order_date TEXT, qty INTEGER);
INSERT INTO price_history VALUES
 (1,10.0,'2024-01-01','2024-01-31'),(1,12.0,'2024-02-01',NULL),        -- clean history
 (2, 5.0,'2024-01-01','2024-01-10'),(2, 6.0,'2024-01-15',NULL),        -- gap 11-14 Jan
 (3,20.0,'2024-01-01','2024-01-31'),(3,22.0,'2024-01-20',NULL);        -- overlap 20-31 Jan
INSERT INTO orders VALUES
 (1,1,'2024-01-15',2),(2,1,'2024-02-01',1),(3,1,'2024-03-10',4),(4,1,'2023-12-31',1),
 (5,2,'2024-01-12',3),(6,3,'2024-01-25',1);
""")

# sql:trap
SQL_TRAP = """
SELECT o.order_id, p.price
FROM orders o
LEFT JOIN price_history p
  ON p.product_id = o.product_id AND o.order_date BETWEEN p.valid_from AND p.valid_to
ORDER BY o.order_id
"""
# end
# sql:main
SQL_MAIN = """
SELECT o.order_id, o.product_id, o.order_date, p.price, o.qty * p.price AS revenue
FROM orders o
LEFT JOIN price_history p
  ON p.product_id = o.product_id
 AND p.valid_from <= o.order_date
 AND (p.valid_to IS NULL OR o.order_date <= p.valid_to)
ORDER BY o.order_id, p.valid_from
"""
# end
# sql:overlap
SQL_OVERLAP = """
SELECT a.product_id, a.valid_from AS a_from, a.valid_to AS a_to, b.valid_from AS b_from, b.valid_to AS b_to
FROM price_history a
JOIN price_history b
  ON a.product_id = b.product_id
 AND a.valid_from < b.valid_from
 AND b.valid_from <= COALESCE(a.valid_to, '9999-12-31')
ORDER BY a.product_id, a.valid_from
"""
# end
# sql:gap
SQL_GAP = """
SELECT a.product_id, a.valid_to AS ends_on, date(a.valid_to, '+1 day') AS uncovered_day
FROM price_history a
WHERE a.valid_to IS NOT NULL
  AND NOT EXISTS (SELECT 1 FROM price_history b
                  WHERE b.product_id = a.product_id
                    AND b.valid_from <= date(a.valid_to, '+1 day')
                    AND COALESCE(b.valid_to, '9999-12-31') >= date(a.valid_to, '+1 day'))
ORDER BY a.product_id
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
trap, main = sql(SQL_TRAP), sql(SQL_MAIN)
print("BETWEEN with NULL valid_to (order_id, price):", trap)
print("\ncorrect join (order_id, product_id, order_date, price, revenue):")
for r in main: print("  ", r)
print("\noverlap check:", sql(SQL_OVERLAP))
print("gap check:    ", sql(SQL_GAP))

orders = pd.read_sql_query("SELECT * FROM orders", con, parse_dates=["order_date"])
ph = pd.read_sql_query("SELECT * FROM price_history", con, parse_dates=["valid_from", "valid_to"])

# pd:main
m = orders.merge(ph, on="product_id", how="left")
ok = (m["valid_from"] <= m["order_date"]) & (m["valid_to"].isna() | (m["order_date"] <= m["valid_to"]))
hit = m.loc[ok, ["order_id", "price", "valid_from"]]
p_main = orders.merge(hit, on="order_id", how="left")
p_main["revenue"] = p_main["qty"] * p_main["price"]
# end
# pd:asof
a = pd.merge_asof(orders.sort_values("order_date"), ph.sort_values("valid_from"),
                  left_on="order_date", right_on="valid_from", by="product_id", direction="backward")
a["price"] = a["price"].where(a["valid_to"].isna() | (a["order_date"] <= a["valid_to"]))
# end
def norm(rows):
    return sorted((int(r[0]), None if pd.isna(r[1]) else float(r[1])) for r in rows)
sql_prices = norm([(r[0], r[3]) for r in main])
assert norm(p_main[["order_id", "price"]].itertuples(index=False, name=None)) == sql_prices
print("\npandas merge+filter == SQL (order_id, price), incl. the duplicated order 6 and the unpriced orders")
print("pandas rows:", len(p_main), "| SQL rows:", len(main), "| orders:", len(orders))
# merge_asof picks ONE row (the latest valid_from <= date): no duplicates, so the overlap for order 6 is hidden
print("merge_asof (order_id, price):", sorted(zip(a["order_id"], a["price"])))
dups = p_main.groupby("order_id").size()
print("orders priced more than once:", dups[dups > 1].index.tolist())
print("orders with no price:", p_main.loc[p_main["price"].isna(), "order_id"].tolist())
# overlap check in pandas
pm = ph.merge(ph, on="product_id", suffixes=("_a", "_b"))
ov = pm[(pm["valid_from_a"] < pm["valid_from_b"]) &
        (pm["valid_from_b"] <= pm["valid_to_a"].fillna(pd.Timestamp("2262-04-11")))]
assert len(ov) == len(sql(SQL_OVERLAP)) == 1
print("asserts passed")
```

**Output (my run):**
```text
BETWEEN with NULL valid_to (order_id, price): [(1, 10.0), (2, None), (3, None), (4, None), (5, None), (6, 20.0)]

correct join (order_id, product_id, order_date, price, revenue):
   (1, 1, '2024-01-15', 10.0, 20.0)
   (2, 1, '2024-02-01', 12.0, 12.0)
   (3, 1, '2024-03-10', 12.0, 48.0)
   (4, 1, '2023-12-31', None, None)
   (5, 2, '2024-01-12', None, None)
   (6, 3, '2024-01-25', 20.0, 20.0)
   (6, 3, '2024-01-25', 22.0, 22.0)

overlap check: [(3, '2024-01-01', '2024-01-31', '2024-01-20', None)]
gap check:     [(2, '2024-01-10', '2024-01-11')]

pandas merge+filter == SQL (order_id, price), incl. the duplicated order 6 and the unpriced orders
pandas rows: 7 | SQL rows: 7 | orders: 6
merge_asof (order_id, price): [(1, 10.0), (2, 12.0), (3, 12.0), (4, nan), (5, nan), (6, 22.0)]
orders priced more than once: [6]
orders with no price: [4, 5]
asserts passed
```

**Edge cases:**
- **Open end:** `BETWEEN a AND NULL` is never TRUE. Use `valid_to IS NULL OR ...` or `COALESCE(valid_to, '9999-12-31')`. A sentinel date is simple but must be the same in every query.
- **Gap:** the order matches nothing. A LEFT JOIN from orders shows it with a NULL price (orders 4 and 5); an INNER JOIN drops it and revenue falls silently.
- **Overlap:** the order matches two rows and is repeated (order 6). Row count 7 for 6 orders is the signal.
- **Inclusive versus exclusive end:** if `valid_to` is the day the next price starts (exclusive), use `order_date < valid_to`, and the gap check must compare with `valid_to` itself instead of `valid_to + 1 day`. Pick one convention and check the data against it.
- **Timestamps:** with a datetime `order_date`, an inclusive `valid_to` of `2024-01-31` excludes the afternoon of 31 Jan; half-open `[valid_from, valid_to)` with the next start as the end avoids that (not run here; the sample uses dates).
- **merge_asof** returns one row per order, the latest `valid_from <= order_date`. It hid the overlap (order 6 got only 22.0) and needs the `valid_to` check to expose gaps (order 5 became NaN). It also needs both sides sorted by the date key and raises on NaN keys (Q25).

**Then explain:**
- **Why the grain matters:** the lookup must return exactly one row per order. Each of the two failure modes (gap: 0 rows, overlap: 2 rows) breaks that, so test the history rather than trust it.
- **Overlap check:** the self join compares version a with a later version b of the same product. In my run it found one pair, product 3. `a.valid_from < b.valid_from` stops pairs being reported twice and stops a row overlapping itself.
- **Gap check:** it found product 2 (ends 10 Jan, 11 Jan uncovered). My first version asked "does a version start the day after?" and wrongly flagged product 3, whose successor starts early because of the overlap, so I changed it to ask whether the day is covered at all.
- **pandas:** merge on `product_id`, build the boolean window mask, take the hits, then merge back on `order_id` so unpriced orders survive. Filtering after a `how="left"` merge would drop them.
- `merge_asof` is the efficient form for large inputs (sorted merge, no full product per key), but it does not know about the end date or duplicates.
- Fix the source if you can: enforce non-overlapping versions with a constraint (PostgreSQL range types with an exclusion constraint do this; stated from memory, not executed here).

**Follow-ups:**
- *What if there are many orders and few price changes?* The join is cheap if indexed on `(product_id, valid_from)`; merge_asof is the pandas analogue.
- *How would you get the current price only?* `WHERE valid_to IS NULL` (one row per product if the history is clean; add a uniqueness check).
- *What would you do about gaps?* Report them, and decide with the business whether to backfill or let the price be missing; do not default silently.

**Common mistakes:**
- `BETWEEN` with an open-ended NULL.
- INNER JOIN, which hides gaps and unpriced orders.
- Not checking for duplicate order rows after the join (compare row count with the orders count).
- `<=` on both ends when the next version starts on the day the old one ends (double match on that day).

### Q27 ⭐⭐ 🟡 Overlapping intervals with a self join: bookings(booking_id, room_id, start_date, end_date). Find pairs of bookings for the same room that overlap. State the overlap condition (a.start < b.end AND b.start < a.end), explain why a.booking_id < b.booking_id, what changes if end_date is inclusive, and give the pandas version (merge on room_id then filter).
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Two bookings of the same room overlap when each starts before the other ends, `a.start < b.end AND b.start < a.end`; add `a.booking_id < b.booking_id` so each pair appears once and no booking is paired with itself, and use `<=` instead of `<` only if the end date is inclusive.

**Schema and sample data:**
```sql
CREATE TABLE bookings(booking_id INTEGER PRIMARY KEY, room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO bookings VALUES
 (1,1,'2024-01-01','2024-01-05'),
 (2,1,'2024-01-03','2024-01-08'),
 (3,1,'2024-01-08','2024-01-10'),
 (4,2,'2024-01-01','2024-01-02'),
 (5,2,'2024-01-05','2024-01-06'),
 (6,3,'2024-01-02','2024-01-04'),
 (7,1,'2024-01-10','2024-01-12');
```
Here `end_date` is the check-out day, so the room is free for the next guest on that day (end exclusive).

**SQL answer:** (same text as in the Code block)
```sql
SELECT a.booking_id AS a_id, b.booking_id AS b_id, a.room_id
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.start_date < b.end_date
 AND b.start_date < a.end_date
 AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
```

**pandas answer:** (same text as in the Code block)
```python
m = bk.merge(bk, on="room_id", suffixes=("_a", "_b"))
hit = m[(m["booking_id_a"] < m["booking_id_b"]) &
        (m["start_date_a"] < m["end_date_b"]) &
        (m["start_date_b"] < m["end_date_a"])]
p_main = hit[["booking_id_a", "booking_id_b", "room_id"]].sort_values(["booking_id_a", "booking_id_b"])
```

**Example:** Room 1 has bookings 1 (1 to 5 Jan), 2 (3 to 8 Jan), 3 (8 to 10 Jan) and 7 (10 to 12 Jan). Bookings 1 and 2: 1 Jan < 8 Jan and 3 Jan < 5 Jan, so they overlap (3 to 5 Jan). Bookings 2 and 3: 3 Jan < 10 Jan but 8 Jan < 8 Jan is false, so they only touch at the check-out day and do not overlap. Same for 3 and 7. Room 2 (1 to 2 Jan and 5 to 6 Jan) and room 3 (one booking) have none. Result: the single pair (1, 2).

**Code:** (run with `python3 -I`; compared as sorted lists of (a_id, b_id, room_id) for both the exclusive and the inclusive versions)
```python
# Q27: overlapping bookings with a self join (end exclusive vs inclusive)
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE bookings(booking_id INTEGER PRIMARY KEY, room_id INTEGER, start_date TEXT, end_date TEXT);
INSERT INTO bookings VALUES
 (1,1,'2024-01-01','2024-01-05'),
 (2,1,'2024-01-03','2024-01-08'),
 (3,1,'2024-01-08','2024-01-10'),
 (4,2,'2024-01-01','2024-01-02'),
 (5,2,'2024-01-05','2024-01-06'),
 (6,3,'2024-01-02','2024-01-04'),
 (7,1,'2024-01-10','2024-01-12');
""")
# sql:main
SQL_MAIN = """
SELECT a.booking_id AS a_id, b.booking_id AS b_id, a.room_id
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.start_date < b.end_date
 AND b.start_date < a.end_date
 AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
"""
# end
# sql:incl
SQL_INCL = """
SELECT a.booking_id AS a_id, b.booking_id AS b_id, a.room_id
FROM bookings a
JOIN bookings b
  ON a.room_id = b.room_id
 AND a.start_date <= b.end_date
 AND b.start_date <= a.end_date
 AND a.booking_id < b.booking_id
ORDER BY a.booking_id, b.booking_id
"""
# end
# sql:no_id
SQL_NO_ID = """
SELECT COUNT(*) FROM bookings a JOIN bookings b
  ON a.room_id = b.room_id AND a.start_date < b.end_date AND b.start_date < a.end_date
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
sql_main, sql_incl = sql(SQL_MAIN), sql(SQL_INCL)
print("end exclusive (a.start < b.end AND b.start < a.end):", sql_main)
print("end inclusive (<=):", sql_incl)
print("same condition WITHOUT a.booking_id < b.booking_id -> rows:", sql(SQL_NO_ID)[0][0])

bk = pd.read_sql_query("SELECT * FROM bookings", con, parse_dates=["start_date", "end_date"])
# pd:main
m = bk.merge(bk, on="room_id", suffixes=("_a", "_b"))
hit = m[(m["booking_id_a"] < m["booking_id_b"]) &
        (m["start_date_a"] < m["end_date_b"]) &
        (m["start_date_b"] < m["end_date_a"])]
p_main = hit[["booking_id_a", "booking_id_b", "room_id"]].sort_values(["booking_id_a", "booking_id_b"])
# end
# pd:incl
hit_i = m[(m["booking_id_a"] < m["booking_id_b"]) &
          (m["start_date_a"] <= m["end_date_b"]) &
          (m["start_date_b"] <= m["end_date_a"])]
p_incl = hit_i[["booking_id_a", "booking_id_b", "room_id"]].sort_values(["booking_id_a", "booking_id_b"])
# end
assert [tuple(map(int, r)) for r in p_main.itertuples(index=False, name=None)] == sql_main
assert [tuple(map(int, r)) for r in p_incl.itertuples(index=False, name=None)] == sql_incl
print("pandas exclusive and inclusive == SQL")
print("rows after the merge on room_id alone:", len(m), "| bookings per room:", bk.groupby("room_id").size().to_dict())
touch = sorted(set(sql_incl) - set(sql_main))
print("pairs that only touch at an endpoint (inclusive adds them):", touch)
print("asserts passed")
```

**Output (my run):**
```text
end exclusive (a.start < b.end AND b.start < a.end): [(1, 2, 1)]
end inclusive (<=): [(1, 2, 1), (2, 3, 1), (3, 7, 1)]
same condition WITHOUT a.booking_id < b.booking_id -> rows: 9
pandas exclusive and inclusive == SQL
rows after the merge on room_id alone: 21 | bookings per room: {1: 4, 2: 2, 3: 1}
pairs that only touch at an endpoint (inclusive adds them): [(2, 3, 1), (3, 7, 1)]
asserts passed
```

**Edge cases:**
- **Why the condition works:** two intervals do not overlap only if one ends before the other starts: `a.end <= b.start` or `b.end <= a.start`. Negating gives `a.start < b.end AND b.start < a.end` (for end-exclusive intervals). It also covers one interval inside another, which a check like "a.start is within b" would miss.
- **Inclusive end dates:** if `end_date` is the last night, use `<=` on both comparisons. In my run this added (2, 3) and (3, 7), the touching pairs. Choose the convention from the business meaning (a hotel check-out day is exclusive; a leave request "1 to 5 Jan" is usually inclusive), and say it out loud.
- **Pair direction:** without `a.booking_id < b.booking_id` the same condition returned 9 rows: each of the 7 bookings overlapping itself plus the pair (1, 2) in both orders. `<>` would drop the self pairs but still return both orders.
- **Three-way overlaps** produce three pairs, one per two bookings; if you need clusters of overlap that is a gaps-and-islands problem (Part 7).
- **NULL end date** (open booking): the comparisons become UNKNOWN and the pair disappears; use `COALESCE(end_date, '9999-12-31')` (see Q26). Not run on this sample.
- **Same room is part of the join key.** Dropping `a.room_id = b.room_id` gives false overlaps across rooms.

**Then explain:**
- **Self join with two aliases:** `a` and `b` are the same table treated as two copies; the `ON` condition decides which pairs to keep.
- **Cost:** per room, every booking is compared with every other (about n squared / 2 pairs). In the sample, merging on `room_id` alone produced 21 rows (4x4 + 2x2 + 1x1) before the date filter. Large rooms with thousands of bookings are costly; an index on `(room_id, start_date)` helps in an engine, and in pandas you would filter early or sort and sweep. Engine behaviour is not executed here.
- **pandas:** merge on `room_id` with suffixes, then filter with the same three conditions. The `booking_id_a < booking_id_b` mask is the pandas version of the ordering rule.
- **Dates:** I parsed them as datetimes in pandas; in SQLite ISO text compares in the right order.

**Follow-ups:**
- *How would you find bookings that overlap a given date range?* One table, the same logic against constants: `start < :range_end AND end > :range_start`.
- *How do you prevent overlaps in the first place?* A constraint or exclusion rule (PostgreSQL range types, from memory, not executed) or a check in the booking transaction.
- *How do you list each booking with the number of conflicts?* Use the pair query as a subquery, or union both sides of each pair and count.

**Common mistakes:**
- Using `<=` on an end-exclusive calendar and flagging back-to-back bookings as conflicts, or `<` on an inclusive one and missing them.
- Testing only "a.start between b.start and b.end", which misses the case where `a` contains `b`.
- `<>` instead of `<` on the id, leaving mirror pairs.
- Forgetting the room condition.

### Q28 ⭐⭐ 🟡 Compare two snapshots, what changed: products_old(product_id, price, status) and products_new(product_id, price, status). Produce added, removed and changed products in one result. Use a FULL OUTER JOIN (or two LEFT JOINs with UNION ALL), a NULL-safe comparison for changed rows, and in pandas merge with indicator=True and DataFrame.compare. Explain why price <> price silently misses rows where one side is NULL.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** FULL OUTER JOIN the two snapshots on the key, then label a row `added` if the old side is missing, `removed` if the new side is missing, and `changed` if a column differs using a NULL-safe test (`IS NOT` in SQLite), because `price <> price` is UNKNOWN when either side is NULL and silently skips those rows.

**Schema and sample data:**
```sql
CREATE TABLE products_old(product_id INTEGER PRIMARY KEY, price INTEGER, status TEXT);
CREATE TABLE products_new(product_id INTEGER PRIMARY KEY, price INTEGER, status TEXT);
INSERT INTO products_old VALUES (1,10,'active'),(2,20,'active'),(3,30,'active'),(4,NULL,'active'),(5,7,'active'),(6,NULL,'active'),(7,15,'active');
INSERT INTO products_new VALUES (1,10,'active'),(2,20,'discontinued'),(3,35,'active'),(4,5,'active'),(5,NULL,'active'),(6,NULL,'active'),(8,40,'active');
```
(Prices are toy values.) Expected by eye: 1 same, 2 status changed, 3 price changed, 4 price NULL to 5, 5 price 7 to NULL, 6 NULL on both sides (not a change), 7 removed, 8 added.

**SQL answer:** (same text as in the Code block, runs on SQLite 3.45.1)
```sql
SELECT COALESCE(o.product_id, n.product_id) AS product_id,
       CASE WHEN o.product_id IS NULL THEN 'added'
            WHEN n.product_id IS NULL THEN 'removed'
            ELSE 'changed' END AS change,
       o.price AS old_price, n.price AS new_price, o.status AS old_status, n.status AS new_status
FROM products_old o
FULL OUTER JOIN products_new n ON n.product_id = o.product_id
WHERE o.product_id IS NULL OR n.product_id IS NULL
   OR o.price IS NOT n.price OR o.status IS NOT n.status
ORDER BY product_id
```
Alternative for an engine without FULL JOIN (the same rows; shown and run in the Code block):
```sql
SELECT o.product_id, 'removed' AS change, o.price AS old_price, NULL AS new_price, o.status AS old_status, NULL AS new_status
FROM products_old o LEFT JOIN products_new n ON n.product_id = o.product_id WHERE n.product_id IS NULL
UNION ALL
SELECT n.product_id, 'added', NULL, n.price, NULL, n.status
FROM products_new n LEFT JOIN products_old o ON o.product_id = n.product_id WHERE o.product_id IS NULL
UNION ALL
SELECT o.product_id, 'changed', o.price, n.price, o.status, n.status
FROM products_old o JOIN products_new n ON n.product_id = o.product_id
WHERE o.price IS NOT n.price OR o.status IS NOT n.status
ORDER BY 1
```
The trap, which gives the wrong answer:
```sql
SELECT o.product_id FROM products_old o JOIN products_new n ON n.product_id = o.product_id
WHERE o.price <> n.price OR o.status <> n.status ORDER BY 1
```

**pandas answer:** (same text as in the Code block)
```python
m = old.merge(new, on="product_id", how="outer", suffixes=("_old", "_new"), indicator=True, validate="one_to_one")
def differs(a, b):                       # NaN-safe "not equal": two NaN count as equal
    return ~(a.eq(b) | (a.isna() & b.isna()))
changed_mask = (m["_merge"] == "both") & (differs(m["price_old"], m["price_new"]) |
                                         differs(m["status_old"], m["status_new"]))
m["change"] = np.select([m["_merge"] == "right_only", m["_merge"] == "left_only", changed_mask],
                        ["added", "removed", "changed"], default="same")
p_main = m.loc[m["change"] != "same", ["product_id", "change", "price_old", "price_new", "status_old", "status_new"]]
```
```python
# DataFrame.compare on the keys present in both snapshots
both_ids = sorted(set(old["product_id"]) & set(new["product_id"]))
o2 = old.set_index("product_id").loc[both_ids]
n2 = new.set_index("product_id").loc[both_ids]
diff = o2.compare(n2, result_names=("old", "new"))
```

**Example:** Product 7 exists only in the old snapshot (removed) and product 8 only in the new one (added). For product 4 the old price is NULL and the new price is 5: `NULL <> 5` is UNKNOWN, so the naive query does not see the change; `NULL IS NOT 5` is TRUE, so the NULL-safe query does. Product 5 (7 to NULL) is the mirror case. Product 6 has NULL on both sides: `NULL IS NOT NULL` is FALSE, so correctly not changed. Result: changed 2, 3, 4, 5; removed 7; added 8.

**Code:** (run with `python3 -I`; SQL and pandas compared as lists sorted by product_id, NULL and NaN both as None)
```python
# Q28: compare two snapshots: added, removed, changed (NULL-safe), SQL FULL JOIN + pandas indicator / compare
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products_old(product_id INTEGER PRIMARY KEY, price INTEGER, status TEXT);
CREATE TABLE products_new(product_id INTEGER PRIMARY KEY, price INTEGER, status TEXT);
INSERT INTO products_old VALUES (1,10,'active'),(2,20,'active'),(3,30,'active'),(4,NULL,'active'),(5,7,'active'),(6,NULL,'active'),(7,15,'active');
INSERT INTO products_new VALUES (1,10,'active'),(2,20,'discontinued'),(3,35,'active'),(4,5,'active'),(5,NULL,'active'),(6,NULL,'active'),(8,40,'active');
-- 1 same; 2 status; 3 price; 4 NULL->5; 5 7->NULL; 6 NULL on both sides (same); 7 removed; 8 added
""")
# sql:main
SQL_MAIN = """
SELECT COALESCE(o.product_id, n.product_id) AS product_id,
       CASE WHEN o.product_id IS NULL THEN 'added'
            WHEN n.product_id IS NULL THEN 'removed'
            ELSE 'changed' END AS change,
       o.price AS old_price, n.price AS new_price, o.status AS old_status, n.status AS new_status
FROM products_old o
FULL OUTER JOIN products_new n ON n.product_id = o.product_id
WHERE o.product_id IS NULL OR n.product_id IS NULL
   OR o.price IS NOT n.price OR o.status IS NOT n.status
ORDER BY product_id
"""
# end
# sql:two
SQL_TWO = """
SELECT o.product_id, 'removed' AS change, o.price AS old_price, NULL AS new_price, o.status AS old_status, NULL AS new_status
FROM products_old o LEFT JOIN products_new n ON n.product_id = o.product_id WHERE n.product_id IS NULL
UNION ALL
SELECT n.product_id, 'added', NULL, n.price, NULL, n.status
FROM products_new n LEFT JOIN products_old o ON o.product_id = n.product_id WHERE o.product_id IS NULL
UNION ALL
SELECT o.product_id, 'changed', o.price, n.price, o.status, n.status
FROM products_old o JOIN products_new n ON n.product_id = o.product_id
WHERE o.price IS NOT n.price OR o.status IS NOT n.status
ORDER BY 1
"""
# end
# sql:naive
SQL_NAIVE = """
SELECT o.product_id FROM products_old o JOIN products_new n ON n.product_id = o.product_id
WHERE o.price <> n.price OR o.status <> n.status ORDER BY 1
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
sql_main, sql_two = sql(SQL_MAIN), sql(SQL_TWO)
for r in sql_main: print(r)
print("two LEFT JOINs + UNION ALL gives the same rows:", sql_main == sql_two)
print("naive <> finds only:", [r[0] for r in sql(SQL_NAIVE)], "(misses 4 and 5, where one side is NULL)")

old = pd.read_sql_query("SELECT * FROM products_old", con)
new = pd.read_sql_query("SELECT * FROM products_new", con)
print("\nprice dtype in pandas:", old["price"].dtype, "(NULL made it float)")

# pd:main
m = old.merge(new, on="product_id", how="outer", suffixes=("_old", "_new"), indicator=True, validate="one_to_one")
def differs(a, b):                       # NaN-safe "not equal": two NaN count as equal
    return ~(a.eq(b) | (a.isna() & b.isna()))
changed_mask = (m["_merge"] == "both") & (differs(m["price_old"], m["price_new"]) |
                                         differs(m["status_old"], m["status_new"]))
m["change"] = np.select([m["_merge"] == "right_only", m["_merge"] == "left_only", changed_mask],
                        ["added", "removed", "changed"], default="same")
p_main = m.loc[m["change"] != "same", ["product_id", "change", "price_old", "price_new", "status_old", "status_new"]]
# end
# pd:compare
both_ids = sorted(set(old["product_id"]) & set(new["product_id"]))
o2 = old.set_index("product_id").loc[both_ids]
n2 = new.set_index("product_id").loc[both_ids]
diff = o2.compare(n2, result_names=("old", "new"))
# end
def norm(rows):
    out = []
    for r in rows:
        out.append(tuple(None if (isinstance(v, float) and np.isnan(v)) or v is None else (int(v) if isinstance(v, (float, np.integer)) else v) for v in r))
    return sorted(out)
a = norm(sql_main)
b = norm(p_main.sort_values("product_id").itertuples(index=False, name=None))
assert a == b, (a, b)
print("pandas merge(indicator) == SQL (sorted by product_id, NULL as None)")
print("\nDataFrame.compare on the common ids (only differing cells are shown, NaN == NaN):")
print(diff)
assert sorted(diff.index.tolist()) == [2, 3, 4, 5]
print("compare finds ids", diff.index.tolist(), "= the 'changed' ids", sorted(r[0] for r in sql_main if r[1] == "changed"))
print("asserts passed")
```

**Output (my run):**
```text
(2, 'changed', 20, 20, 'active', 'discontinued')
(3, 'changed', 30, 35, 'active', 'active')
(4, 'changed', None, 5, 'active', 'active')
(5, 'changed', 7, None, 'active', 'active')
(7, 'removed', 15, None, 'active', None)
(8, 'added', None, 40, None, 'active')
two LEFT JOINs + UNION ALL gives the same rows: True
naive <> finds only: [2, 3] (misses 4 and 5, where one side is NULL)

price dtype in pandas: float64 (NULL made it float)
pandas merge(indicator) == SQL (sorted by product_id, NULL as None)

DataFrame.compare on the common ids (only differing cells are shown, NaN == NaN):
           price        status              
             old   new     old           new
product_id                                  
2            NaN   NaN  active  discontinued
3           30.0  35.0     NaN           NaN
4            NaN   5.0     NaN           NaN
5            7.0   NaN     NaN           NaN
compare finds ids [2, 3, 4, 5] = the 'changed' ids [2, 3, 4, 5]
asserts passed
```

**Edge cases:**
- **NULL-safe comparison by dialect:** SQLite has `IS NOT` (ran above) and `IS`. PostgreSQL has `IS DISTINCT FROM` and MySQL `NOT (a <=> b)`; I did not run either. A portable form is `(a <> b OR (a IS NULL AND b IS NOT NULL) OR (a IS NOT NULL AND b IS NULL))`, which I did not run here but follows from the standard rules.
- **Naive `<>`:** it found only products 2 and 3. Products 4 and 5 were missed. It would also miss a status that changes to or from NULL.
- **Duplicate keys in a snapshot** multiply rows; in pandas `validate="one_to_one"` raises `MergeError` (I only used it on clean data). Check uniqueness first.
- **Float price in pandas:** the NULL made the column `float64`; ids with NaN on both sides are equal for `differs`, because I treat two NaN as the same.
- **`DataFrame.compare` surprise:** it shows `NaN` for any cell that did not change, so a real NULL (id 4 old price, id 5 new price) looks the same as "unchanged". Read it together with the source frames. It needs identical row and column labels, so I restricted both frames to the common ids first; it does not handle added or removed rows.
- **Column list:** if you compare many columns, generate the comparison per column; `IS NOT` per column is long but safe.

**Then explain:**
- **Three groups from one join:** added (left key NULL), removed (right key NULL), changed (matched with a difference). `COALESCE(o.product_id, n.product_id)` gives a key in every row (Q16, Q39).
- **FULL JOIN versus two LEFT JOINs + UNION ALL:** same rows when each part is disjoint (removed, added, changed). SQLite 3.45 ran both; I did not run MySQL, which lacks FULL JOIN (hedged).
- **pandas:** `merge(how="outer", indicator=True)` gives `_merge` (`left_only` means removed, `right_only` added); the changed mask needs an explicit NaN-safe comparison, since `NaN != NaN` is True in pandas, which would flag product 6 as changed. This differs from SQL, where the plain `<>` is the one that misses rows.
- **What `compare` is for:** a quick human-readable diff of two same-shaped frames; the merge version is the one you can load into a table.

**Follow-ups:**
- *How would you do this at scale?* Compare row hashes per key first, then drill into the differing keys (concept, not run here).
- *What if there is a composite key?* Join on all key columns and coalesce each.
- *Can EXCEPT do it?* `SELECT * FROM old EXCEPT SELECT * FROM new` returns rows that differ in any column and treats NULLs as equal (Q29), but it does not tell you which column changed or added versus changed.

**Common mistakes:**
- `price <> price` with NULLs.
- Calling a row "changed" when both sides are NULL (the other direction, using `=` or pandas `!=`).
- Filtering the FULL JOIN with `WHERE o.price <> n.price`, which also drops the added and removed rows.
- Reading `compare` output's NaN as "this cell is NULL".

### Q29 ⭐⭐ 🟡 EXCEPT and INTERSECT versus joins: customers_2024(customer_id) and customers_2025(customer_id). Find customers in both years, in 2024 only, and in 2025 only with INTERSECT, EXCEPT and with joins or EXISTS. Say how set operators treat NULLs and duplicates (they de-duplicate and treat NULLs as equal), that Oracle calls EXCEPT MINUS, and MySQL support is version dependent (hedge). Give pandas isin and merge.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** `INTERSECT` gives customers in both years, `EXCEPT` gives one year minus the other; both de-duplicate and treat NULL as equal to NULL, which the join and `EXISTS` versions do not, so they agree with the set operators only after `DISTINCT` and a NULL-safe match.

**Schema and sample data:**
```sql
CREATE TABLE customers_2024(customer_id INTEGER);
CREATE TABLE customers_2025(customer_id INTEGER);
INSERT INTO customers_2024 VALUES (1),(2),(3),(3),(NULL);
INSERT INTO customers_2025 VALUES (2),(3),(4),(NULL);
```
(Deliberately dirty: customer 3 is listed twice in 2024, and both years have a NULL id.)

**SQL answer:** (same text as in the Code block)
```sql
SELECT customer_id FROM customers_2024 INTERSECT SELECT customer_id FROM customers_2025 ORDER BY 1
```
```sql
SELECT customer_id FROM customers_2024 EXCEPT SELECT customer_id FROM customers_2025 ORDER BY 1
```
```sql
SELECT customer_id FROM customers_2025 EXCEPT SELECT customer_id FROM customers_2024 ORDER BY 1
```
Join and `EXISTS` versions:
```sql
SELECT DISTINCT a.customer_id FROM customers_2024 a
JOIN customers_2025 b ON b.customer_id = a.customer_id ORDER BY 1
```
```sql
SELECT DISTINCT a.customer_id FROM customers_2024 a
WHERE NOT EXISTS (SELECT 1 FROM customers_2025 b WHERE b.customer_id = a.customer_id) ORDER BY 1
```
```sql
SELECT DISTINCT a.customer_id FROM customers_2024 a
WHERE NOT EXISTS (SELECT 1 FROM customers_2025 b WHERE b.customer_id IS a.customer_id) ORDER BY 1
```

**pandas answer:** (same text as in the Code block)
```python
in_both = c24[c24.isin(c25)].drop_duplicates()
only_24 = c24[~c24.isin(c25)].drop_duplicates()
only_25 = c25[~c25.isin(c24)].drop_duplicates()
```
```python
k24, k25 = c24.drop_duplicates().to_frame(), c25.drop_duplicates().to_frame()
mm = k24.merge(k25, on="customer_id", how="outer", indicator=True, validate="one_to_one")
m_both = mm.loc[mm["_merge"] == "both", "customer_id"]
m_only24 = mm.loc[mm["_merge"] == "left_only", "customer_id"]
m_only25 = mm.loc[mm["_merge"] == "right_only", "customer_id"]
```

**Example:** 2024 = {1, 2, 3, 3, NULL}, 2025 = {2, 3, 4, NULL}. `INTERSECT` de-duplicates and matches NULL with NULL, giving {NULL, 2, 3}. `2024 EXCEPT 2025` removes 2, 3 and NULL, leaving {1}. `2025 EXCEPT 2024` leaves {4}. The inner JOIN with `DISTINCT` gives only {2, 3}, because `NULL = NULL` is not TRUE, so the NULL customer is missing. Without `DISTINCT` the plain join returned 3 rows for 2 customers, since 3 appears twice in 2024.

**Code:** (run with `python3 -I`; pandas compared with the SQL set operators as sorted lists, NULL and NaN shown as None and first)
```python
# Q29: INTERSECT / EXCEPT versus joins and EXISTS; NULL and duplicate behaviour; pandas isin and merge
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers_2024(customer_id INTEGER);
CREATE TABLE customers_2025(customer_id INTEGER);
INSERT INTO customers_2024 VALUES (1),(2),(3),(3),(NULL);
INSERT INTO customers_2025 VALUES (2),(3),(4),(NULL);
""")
def sql(q): return [r[0] for r in con.execute(q).fetchall()]
# sql:both
SQL_BOTH = "SELECT customer_id FROM customers_2024 INTERSECT SELECT customer_id FROM customers_2025 ORDER BY 1"
# end
# sql:only24
SQL_ONLY24 = "SELECT customer_id FROM customers_2024 EXCEPT SELECT customer_id FROM customers_2025 ORDER BY 1"
# end
# sql:only25
SQL_ONLY25 = "SELECT customer_id FROM customers_2025 EXCEPT SELECT customer_id FROM customers_2024 ORDER BY 1"
# end
# sql:join_both
SQL_JOIN_BOTH = """
SELECT DISTINCT a.customer_id FROM customers_2024 a
JOIN customers_2025 b ON b.customer_id = a.customer_id ORDER BY 1
"""
# end
# sql:exists_only24
SQL_EX_ONLY24 = """
SELECT DISTINCT a.customer_id FROM customers_2024 a
WHERE NOT EXISTS (SELECT 1 FROM customers_2025 b WHERE b.customer_id = a.customer_id) ORDER BY 1
"""
# end
# sql:null_safe
SQL_NULL_SAFE = """
SELECT DISTINCT a.customer_id FROM customers_2024 a
WHERE NOT EXISTS (SELECT 1 FROM customers_2025 b WHERE b.customer_id IS a.customer_id) ORDER BY 1
"""
# end
both, only24, only25 = sql(SQL_BOTH), sql(SQL_ONLY24), sql(SQL_ONLY25)
print("INTERSECT:", both, "| 2024 only (EXCEPT):", only24, "| 2025 only (EXCEPT):", only25)
print("plain JOIN without DISTINCT, row count:", sql("SELECT COUNT(*) FROM customers_2024 a JOIN customers_2025 b ON b.customer_id = a.customer_id")[0])
print("JOIN + DISTINCT:", sql(SQL_JOIN_BOTH), "(NULL dropped by =)")
print("NOT EXISTS, 2024 only:", sql(SQL_EX_ONLY24), "(NULL kept: no equal row exists)")
print("NOT EXISTS with IS (null-safe):", sql(SQL_NULL_SAFE))
print("UNION ALL row count:", sql("SELECT COUNT(*) FROM (SELECT customer_id FROM customers_2024 UNION ALL SELECT customer_id FROM customers_2025)")[0],
      "| UNION:", sql("SELECT customer_id FROM customers_2024 UNION SELECT customer_id FROM customers_2025 ORDER BY 1"))
print("INTERSECT ALL in SQLite 3.45:", end=" ")
try: con.execute("SELECT customer_id FROM customers_2024 INTERSECT ALL SELECT customer_id FROM customers_2025").fetchall(); print("ok")
except sqlite3.Error as e: print("error:", e)

c24 = pd.read_sql_query("SELECT * FROM customers_2024", con)["customer_id"]
c25 = pd.read_sql_query("SELECT * FROM customers_2025", con)["customer_id"]
def lst(s): return [None if pd.isna(v) else int(v) for v in s.sort_values(na_position="first")]
# pd:isin
in_both = c24[c24.isin(c25)].drop_duplicates()
only_24 = c24[~c24.isin(c25)].drop_duplicates()
only_25 = c25[~c25.isin(c24)].drop_duplicates()
# end
# pd:merge
k24, k25 = c24.drop_duplicates().to_frame(), c25.drop_duplicates().to_frame()
mm = k24.merge(k25, on="customer_id", how="outer", indicator=True, validate="one_to_one")
m_both = mm.loc[mm["_merge"] == "both", "customer_id"]
m_only24 = mm.loc[mm["_merge"] == "left_only", "customer_id"]
m_only25 = mm.loc[mm["_merge"] == "right_only", "customer_id"]
# end
assert lst(in_both) == lst(m_both) == both == [None, 2, 3]
assert lst(only_24) == lst(m_only24) == only24 == [1]
assert lst(only_25) == lst(m_only25) == only25 == [4]
print("\npandas isin and merge(outer, indicator) == INTERSECT / EXCEPT (NULL/NaN first, duplicates removed)")
print("pandas in both:", lst(in_both), "| 2024 only:", lst(only_24), "| 2025 only:", lst(only_25))
print("asserts passed")
```

**Output (my run):**
```text
INTERSECT: [None, 2, 3] | 2024 only (EXCEPT): [1] | 2025 only (EXCEPT): [4]
plain JOIN without DISTINCT, row count: 3
JOIN + DISTINCT: [2, 3] (NULL dropped by =)
NOT EXISTS, 2024 only: [None, 1] (NULL kept: no equal row exists)
NOT EXISTS with IS (null-safe): [1]
UNION ALL row count: 9 | UNION: [None, 1, 2, 3, 4]
INTERSECT ALL in SQLite 3.45: error: near "ALL": syntax error

pandas isin and merge(outer, indicator) == INTERSECT / EXCEPT (NULL/NaN first, duplicates removed)
pandas in both: [None, 2, 3] | 2024 only: [1] | 2025 only: [4]
asserts passed
```

**Edge cases:**
- **Set operators and NULL:** `INTERSECT` and `EXCEPT` treat NULLs as equal ("not distinct"), so NULL appeared in the intersection and disappeared from the 2024-only result. Joins and `EXISTS` use `=`, where NULL never matches.
- **A surprise worth remembering:** `NOT EXISTS` for "2024 only" returned `[None, 1]`, `EXCEPT` returned `[1]`. The difference is only the NULL row. Using `IS` (SQLite null-safe equality) in the subquery gave `[1]` again.
- **Duplicates:** set operators return distinct rows; a join repeats a row once per match (3 rows for 2 customers). `DISTINCT` fixes that but hides real duplicate rows; if you need multiplicity, you want `INTERSECT ALL` or `EXCEPT ALL`, which SQLite 3.45 rejected (`near "ALL": syntax error`). They exist in PostgreSQL (from memory, not executed).
- **Column count and types** must match across the two SELECTs.
- **pandas:** `isin` and `merge` match NaN with NaN, so pandas agreed with `INTERSECT` here, not with the join. Duplicates must be removed explicitly (`drop_duplicates`).

**Then explain:**
- **Set operators compare whole rows.** With one column it is the key; with several columns all of them must match, so for "same customer" on wider tables use a join or `EXISTS` on the key instead.
- **Join/EXISTS forms:** `EXISTS` is the semi-join (in both years) and `NOT EXISTS` the anti-join (only one year). They keep the left table's columns and its duplicates, and they let you select other columns, which set operators cannot.
- **Dialects (hedged, not executed here):** Oracle calls `EXCEPT` `MINUS` (newer Oracle versions also accept `EXCEPT`, I believe, check the manual). PostgreSQL, SQL Server, BigQuery and Snowflake have `INTERSECT` and `EXCEPT` (BigQuery requires `DISTINCT` explicitly, from memory). MySQL added `INTERSECT` and `EXCEPT` only in 8.0.31, so older versions need joins or `EXISTS`. Check the version you run.
- **pandas:** the three results above come from `isin` (a filter on one column) or an outer merge of the de-duplicated keys with `indicator=True` (`both`, `left_only`, `right_only`), which gives all three groups in one pass. `validate="one_to_one"` confirms the keys are unique after `drop_duplicates`.

**Follow-ups:**
- *Why use EXISTS if INTERSECT is shorter?* You can return other columns, and you control the NULL treatment.
- *What about a union of both years?* `UNION` de-duplicates (all five distinct values above, including NULL); `UNION ALL` keeps 9 rows.
- *How would you do customers in both years for a composite key?* Compare the full tuple (`INTERSECT` on both columns) or join on both columns.

**Common mistakes:**
- Assuming `INTERSECT` and an inner join return the same thing when NULLs or duplicates are present.
- Expecting `EXCEPT` to preserve duplicates.
- Mismatched column counts or order between the two SELECTs.
- Using `EXCEPT` on MySQL older than 8.0.31 (hedged) or `MINUS` on an engine that does not have it.

### Q30 ⭐⭐ 🟡 Generate a complete grid with a CROSS JOIN: stores(store_id, store_name), calendar(day) and sales(store_id, sale_date, amount), where days with no sales have no rows. Produce one row per store per day with 0 for no sales. Explain the CROSS JOIN then LEFT JOIN pattern, why aggregating after the left join is correct, and how to fill dates without a calendar table (hedge: recursive CTE or GENERATE_SERIES is another part). Give pandas how='cross' or MultiIndex.from_product with reindex.
**Asked at:** public LeetCode-style problem bank (SQL 50 join problems, known only from repo snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Build the grid first with `stores CROSS JOIN calendar` (every store with every day), LEFT JOIN `sales` onto it on both store and date, then `GROUP BY store, day` with `COALESCE(SUM(amount), 0)`; the grid fixes the grain at one row per store per day, so empty days survive.

**Schema and sample data:**
```sql
CREATE TABLE stores(store_id INTEGER PRIMARY KEY, store_name TEXT);
CREATE TABLE calendar(day TEXT PRIMARY KEY);
CREATE TABLE sales(store_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO stores VALUES (1,'North'),(2,'South');
INSERT INTO calendar VALUES ('2024-01-01'),('2024-01-02'),('2024-01-03');
INSERT INTO sales VALUES (1,'2024-01-01',10),(1,'2024-01-01',5),(2,'2024-01-03',7);
```

**SQL answer:** (same text as in the Code block)
```sql
SELECT st.store_id, st.store_name, c.day, COALESCE(SUM(s.amount), 0) AS total
FROM stores st
CROSS JOIN calendar c
LEFT JOIN sales s ON s.store_id = st.store_id AND s.sale_date = c.day
GROUP BY st.store_id, st.store_name, c.day
ORDER BY st.store_id, c.day
```
Without a calendar table, one option is a recursive CTE for the days (it ran on SQLite 3.45 in the Code block, but recursive CTEs are Part 9, and `GENERATE_SERIES` in PostgreSQL is not executed here):
```sql
WITH RECURSIVE days(day) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(day, '+1 day') FROM days WHERE day < '2024-01-03')
SELECT day FROM days
```

**pandas answer:** (same text as in the Code block)
```python
# cross merge, aggregate sales to one row per store and day, merge, fill
grid = stores.merge(calendar, how="cross")
daily = sales.groupby(["store_id", "sale_date"], as_index=False).agg(total=("amount", "sum"))
p_cross = (grid.merge(daily, left_on=["store_id", "day"], right_on=["store_id", "sale_date"],
                      how="left", validate="one_to_one")
           .assign(total=lambda d: d["total"].fillna(0).astype("int64"))
           .loc[:, ["store_id", "store_name", "day", "total"]])
```
```python
# MultiIndex.from_product + reindex
idx = pd.MultiIndex.from_product([stores["store_id"], calendar["day"]], names=["store_id", "day"])
p_re = (sales.groupby(["store_id", "sale_date"])["amount"].sum().rename_axis(["store_id", "day"])
        .reindex(idx, fill_value=0).reset_index(name="total")
        .merge(stores, on="store_id")[["store_id", "store_name", "day", "total"]])
```

**Example:** Two stores x three days = 6 grid rows. North sold 10 and 5 on 1 Jan, so the LEFT JOIN brings two sales rows onto the (North, 1 Jan) grid row and `SUM` gives 15; North has no sales on 2 and 3 Jan, so the LEFT JOIN gives one row with NULL amount and `COALESCE(SUM(NULL), 0)` gives 0. South sold 7 on 3 Jan and nothing on the other two days. Six rows come out: 15, 0, 0, 0, 0, 7.

**Code:** (run with `python3 -I`; compared as lists of (store_id, store_name, day, total) sorted by store_id, day)
```python
# Q30: one row per store per day: CROSS JOIN then LEFT JOIN then aggregate; pandas cross merge / from_product
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE stores(store_id INTEGER PRIMARY KEY, store_name TEXT);
CREATE TABLE calendar(day TEXT PRIMARY KEY);
CREATE TABLE sales(store_id INTEGER, sale_date TEXT, amount INTEGER);
INSERT INTO stores VALUES (1,'North'),(2,'South');
INSERT INTO calendar VALUES ('2024-01-01'),('2024-01-02'),('2024-01-03');
INSERT INTO sales VALUES (1,'2024-01-01',10),(1,'2024-01-01',5),(2,'2024-01-03',7);
""")
# sql:main
SQL_MAIN = """
SELECT st.store_id, st.store_name, c.day, COALESCE(SUM(s.amount), 0) AS total
FROM stores st
CROSS JOIN calendar c
LEFT JOIN sales s ON s.store_id = st.store_id AND s.sale_date = c.day
GROUP BY st.store_id, st.store_name, c.day
ORDER BY st.store_id, c.day
"""
# end
# sql:cte
SQL_CTE = """
WITH RECURSIVE days(day) AS (
  SELECT '2024-01-01' UNION ALL SELECT date(day, '+1 day') FROM days WHERE day < '2024-01-03')
SELECT day FROM days
"""
# end
# sql:wrong
SQL_WRONG = """
SELECT st.store_id, c.day, SUM(s.amount) AS total
FROM stores st CROSS JOIN calendar c
LEFT JOIN sales s ON s.store_id = st.store_id AND s.sale_date = c.day
WHERE s.amount > 0
GROUP BY st.store_id, c.day
"""
# end
sql_main = [tuple(r) for r in con.execute(SQL_MAIN).fetchall()]
for r in sql_main: print(r)
print("recursive CTE days:", [r[0] for r in con.execute(SQL_CTE)], "== calendar:", [r[0] for r in con.execute("SELECT day FROM calendar ORDER BY day")])
print("WHERE s.amount > 0 version returns", len(con.execute(SQL_WRONG).fetchall()), "rows instead of 6")

stores = pd.read_sql_query("SELECT * FROM stores", con)
calendar = pd.read_sql_query("SELECT * FROM calendar", con)
sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:cross
grid = stores.merge(calendar, how="cross")
daily = sales.groupby(["store_id", "sale_date"], as_index=False).agg(total=("amount", "sum"))
p_cross = (grid.merge(daily, left_on=["store_id", "day"], right_on=["store_id", "sale_date"],
                      how="left", validate="one_to_one")
           .assign(total=lambda d: d["total"].fillna(0).astype("int64"))
           .loc[:, ["store_id", "store_name", "day", "total"]])
# end
# pd:reindex
idx = pd.MultiIndex.from_product([stores["store_id"], calendar["day"]], names=["store_id", "day"])
p_re = (sales.groupby(["store_id", "sale_date"])["amount"].sum().rename_axis(["store_id", "day"])
        .reindex(idx, fill_value=0).reset_index(name="total")
        .merge(stores, on="store_id")[["store_id", "store_name", "day", "total"]])
# end
def norm(df): return [tuple(r) for r in df.sort_values(["store_id", "day"]).itertuples(index=False, name=None)]
assert norm(p_cross) == sql_main
assert norm(p_re) == sql_main
print("\npandas cross merge == SQL; from_product + reindex == SQL (sorted by store_id, day)")
print("total dtype after fillna(0) before the cast:",
      grid.merge(daily, left_on=["store_id", "day"], right_on=["store_id", "sale_date"], how="left")["total"].fillna(0).dtype)
print("grid rows:", len(grid), "= stores x days =", len(stores), "*", len(calendar))
print("asserts passed")
```

**Output (my run):**
```text
(1, 'North', '2024-01-01', 15)
(1, 'North', '2024-01-02', 0)
(1, 'North', '2024-01-03', 0)
(2, 'South', '2024-01-01', 0)
(2, 'South', '2024-01-02', 0)
(2, 'South', '2024-01-03', 7)
recursive CTE days: ['2024-01-01', '2024-01-02', '2024-01-03'] == calendar: ['2024-01-01', '2024-01-02', '2024-01-03']
WHERE s.amount > 0 version returns 2 rows instead of 6

pandas cross merge == SQL; from_product + reindex == SQL (sorted by store_id, day)
total dtype after fillna(0) before the cast: float64
grid rows: 6 = stores x days = 2 * 3
asserts passed
```

**Edge cases:**
- **Aggregating after the join is correct:** the grid row is the grain. Several sales rows on the same day collapse into one total through the `GROUP BY`. If you aggregated sales first and then joined, that also works as long as the sales are one row per store per day (the `validate="one_to_one"` in the pandas version checks this).
- **A filter on `sales` in WHERE breaks it:** `WHERE s.amount > 0` turned the LEFT JOIN into an inner join and returned 2 rows instead of 6. Put sale conditions in the `ON` clause (Q3).
- **Sum of nothing:** `SUM` of all-NULL is NULL in SQL, hence the `COALESCE`. pandas `sum` of an empty group is 0, but after a left merge the missing values are NaN, so `fillna(0)` is needed.
- **dtype after `fillna`:** the column was `float64` (printed before the cast); I cast back to `int64`. `reindex(fill_value=0)` kept it integer.
- **Days in `sales` that are not in the calendar** disappear from the grid; that is usually a data quality check worth running.
- **Time zones or timestamps:** truncate to a date before joining; a datetime never equals a date key (not run here).

**Then explain:**
- **Why CROSS JOIN first:** a LEFT JOIN can only keep rows that exist on its left side. You need a row for every (store, day) before sales are attached, and a cross join produces exactly that.
- **Cost:** the grid has stores x days rows, so a thousand stores and a year of days is 365,000 rows; fine, but compute it before you run it (Q31).
- **No calendar table:** generate days (recursive CTE, or `GENERATE_SERIES` in PostgreSQL, hedged and not executed here), or keep a permanent calendar table; a calendar table also carries week, month and holiday columns.
- **pandas:** `how="cross"` is the same product. `MultiIndex.from_product` plus `reindex` builds the same grid without a merge and fills missing combinations in one step.

**Follow-ups:**
- *What if I only want days that stores were open?* Join to an `open_days` table instead of the full calendar.
- *How would you also show the previous day's total?* That needs window functions (Part 5).
- *How would you fill missing days in pandas time series?* `asfreq` or `resample` on a datetime index (not run here).

**Common mistakes:**
- Starting from `sales` and expecting zero rows.
- Filtering on the sales table in WHERE.
- `COUNT(*)` instead of `COUNT(s.sale_date)` when counting sales per day (counts the grid row as one sale).
- Forgetting that `SUM` over no rows is NULL.

### Q31 ⭐⭐ 🟡 Cartesian product pitfalls: a three-table query FROM orders o, customers c, products p WHERE o.customer_id = c.customer_id forgets the products condition. Explain the row explosion (rows multiply), how to detect it (row count vs expected, COUNT(*) vs COUNT(DISTINCT order_id)), why comma joins invite this, why explicit JOIN ... ON is safer, and when a cross join is intentional. Show the pandas how='cross' memory risk.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Forget one join condition in a comma join and the missing table is cross-joined, so rows multiply by its row count (5 orders became 20 rows with 4 products) and every `SUM` is inflated by the same factor; catch it by comparing `COUNT(*)` with `COUNT(DISTINCT order_id)` and use explicit `JOIN ... ON` so a missing condition is visible.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra');
INSERT INTO products VALUES (10,'Pen'),(20,'Ink'),(30,'Pad'),(40,'Cap');
INSERT INTO orders VALUES (1,1,10,100),(2,1,20,200),(3,2,10,50),(4,3,30,70),(5,2,40,30);
```

**SQL answer:** (same text as in the Code block). The buggy query, which forgets `o.product_id = p.product_id`:
```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT o.order_id) AS n_orders, SUM(o.amount) AS revenue
FROM orders o, customers c, products p
WHERE o.customer_id = c.customer_id
```
The fixed query:
```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT o.order_id) AS n_orders, SUM(o.amount) AS revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN products p ON p.product_id = o.product_id
```

**pandas answer:** (same text as in the Code block)
```python
# the bug: a cross merge with no key
p_bad = orders.merge(customers, on="customer_id").merge(products, how="cross")
```
```python
# the fix, with validate so a duplicated product key would raise
p_main = orders.merge(customers, on="customer_id").merge(products, on="product_id", validate="many_to_one")
```

**Example:** Five orders, three customers, four products. The comma join pairs each order with its customer (condition present), but with all four products (no condition): 5 x 4 = 20 rows. `COUNT(DISTINCT order_id)` is still 5. Revenue is 1800 instead of the true 450, because each amount is repeated four times: 450 x 4 = 1800. The ratio `COUNT(*) / COUNT(DISTINCT order_id)` = 4 equals the number of products, which points straight at the missing table.

**Code:** (run with `python3 -I`; compares the (rows, distinct orders, revenue) triple from SQL with pandas for both the buggy and the fixed version)
```python
# Q31: cartesian product pitfall: forgotten join condition, detection, and the pandas cross-merge risk
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, title TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra');
INSERT INTO products VALUES (10,'Pen'),(20,'Ink'),(30,'Pad'),(40,'Cap');
INSERT INTO orders VALUES (1,1,10,100),(2,1,20,200),(3,2,10,50),(4,3,30,70),(5,2,40,30);
""")
# sql:bad
SQL_BAD = """
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT o.order_id) AS n_orders, SUM(o.amount) AS revenue
FROM orders o, customers c, products p
WHERE o.customer_id = c.customer_id
"""
# end
# sql:main
SQL_MAIN = """
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT o.order_id) AS n_orders, SUM(o.amount) AS revenue
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN products p ON p.product_id = o.product_id
"""
# end
bad = con.execute(SQL_BAD).fetchone()
good = con.execute(SQL_MAIN).fetchone()
print("comma join, missing condition: rows, distinct orders, revenue =", bad)
print("explicit JOIN ... ON:          rows, distinct orders, revenue =", good)
print("n_rows / n_orders =", bad[0] // bad[1], "= number of products (", con.execute("SELECT COUNT(*) FROM products").fetchone()[0], ")")
try:
    con.execute("SELECT * FROM orders o JOIN customers c")  # no ON
    print("JOIN without ON in SQLite: accepted (it behaves as a cross join)")
except sqlite3.Error as e:
    print("JOIN without ON in SQLite: error:", e)

orders = pd.read_sql_query("SELECT * FROM orders", con)
customers = pd.read_sql_query("SELECT * FROM customers", con)
products = pd.read_sql_query("SELECT * FROM products", con)
# pd:bad
p_bad = orders.merge(customers, on="customer_id").merge(products, how="cross")
# end
# pd:main
p_main = orders.merge(customers, on="customer_id").merge(products, on="product_id", validate="many_to_one")
# end
assert (len(p_bad), p_bad["order_id"].nunique(), int(p_bad["amount"].sum())) == bad
assert (len(p_main), p_main["order_id"].nunique(), int(p_main["amount"].sum())) == good
print("pandas cross merge rows:", len(p_bad), "| correct merge rows:", len(p_main), "(both equal SQL)")
try:
    orders.merge(customers, how="cross", on="customer_id")
except pd.errors.MergeError as e:
    print("pandas: how='cross' with on= ->", type(e).__name__, "|", e)
# the memory risk: pure arithmetic, nothing is allocated
for n_left, n_right in [(5, 4), (100_000, 100_000), (1_000_000, 50_000)]:
    rows = n_left * n_right
    print(f"cross merge {n_left:>9,} x {n_right:>7,} = {rows:>16,} rows (not run); at 16 bytes/row if two 8-byte columns: {rows*16/1e9:,.1f} GB")
print("asserts passed")
```

**Output (my run):**
```text
comma join, missing condition: rows, distinct orders, revenue = (20, 5, 1800)
explicit JOIN ... ON:          rows, distinct orders, revenue = (5, 5, 450)
n_rows / n_orders = 4 = number of products ( 4 )
JOIN without ON in SQLite: accepted (it behaves as a cross join)
pandas cross merge rows: 20 | correct merge rows: 5 (both equal SQL)
pandas: how='cross' with on= -> MergeError | Can not pass on, right_on, left_on or set right_index=True or left_index=True
cross merge         5 x       4 =               20 rows (not run); at 16 bytes/row if two 8-byte columns: 0.0 GB
cross merge   100,000 x 100,000 =   10,000,000,000 rows (not run); at 16 bytes/row if two 8-byte columns: 160.0 GB
cross merge 1,000,000 x  50,000 =   50,000,000,000 rows (not run); at 16 bytes/row if two 8-byte columns: 800.0 GB
asserts passed
```

**Edge cases:**
- **How to detect it:** compare the row count with what you expect for the grain (5 orders, 20 rows), compare `COUNT(*)` with `COUNT(DISTINCT order_id)`, and sanity check a total against the single table (`SELECT SUM(amount) FROM orders` = 450).
- **Comma joins invite it:** with `FROM a, b, c WHERE ...`, a missing predicate is not a syntax error, and the conditions are far from the tables. In `JOIN ... ON` every join has its own condition next to it. (Modern engines treat both the same; this is a readability and safety argument, not a speed one.)
- **A forgotten `ON` in SQLite** was accepted and produced a cross join (printed in the output). Some other engines raise a syntax error for `JOIN` without `ON`; not executed here, so check yours.
- **A condition that does not reduce rows** is also a quiet cartesian: `ON 1 = 1`, or a condition that is true for every pair.
- **Intentional cross joins** exist: a grid of every store and every day (Q30), every pair of values in a test matrix, or attaching a one-row parameter table to every row. Write them with `CROSS JOIN` so the intent is visible.
- **Empty table:** a cross join with an empty table returns zero rows, so a forgotten condition can also make the result vanish.

**Then explain:**
- **Rows multiply:** n rows x m rows gives n x m rows. Three unconstrained tables of 1,000 rows each give a billion rows.
- **Inflated measures:** every `SUM` and `COUNT(*)` is multiplied by the factor; `AVG` can look plausible, so it is easy to miss. `COUNT(DISTINCT key)` is the one that stays right, which is why the comparison works as a detector (it is no fix, see Q13).
- **pandas memory risk:** `merge(how="cross")` materializes every pair at once. The lines in the output are plain arithmetic (not run): 100,000 x 100,000 is 10 billion rows. The size estimate assumes just two 8-byte columns, a lower bound; real frames have more columns, so the true memory is larger. `validate=` is no guard here: in a one-off check I ran, `validate="one_to_one"` on a cross merge raised `MergeError` because the hidden constant key is repeated, and passing `on=` with `how="cross"` raises as printed (see Q9 for `validate` on keyed merges).
- **Guard before you run:** compute `len(a) * len(b)` first and refuse above a limit, or filter both sides before crossing.

**Follow-ups:**
- *How would you spot this in a query plan?* A join with no predicate, shown as a nested loop over a full scan; EXPLAIN belongs to Part 11 and is not executed here.
- *Does `JOIN` without ON behave like CROSS JOIN everywhere?* No, not guaranteed: SQLite accepted it; check each engine's behaviour (not executed).
- *How do you bring a single parameter row into every row?* `CROSS JOIN params` (one row), which is a safe cross join.

**Common mistakes:**
- Fixing inflated totals with `SUM(DISTINCT amount)`, which also drops legitimate equal amounts.
- Joining on the wrong column pair (customer_id to product_id), which gives a plausible but wrong result.
- Reading a correct-looking small test as proof; row-count checks are the real test.
- Running `how="cross"` on large frames "to see what happens".

### Q32 ⭐⭐ 🟡 Simulate FULL OUTER JOIN with UNION: a_users(user_id, name) and b_users(user_id, email), for an engine without FULL JOIN (MySQL; hedged). Write LEFT JOIN UNION RIGHT JOIN, then the better version (LEFT JOIN UNION ALL anti-join of the right table), and explain why UNION ALL is correct there, what UNION de-duplication could wrongly collapse, and the cost of the extra scan.
**Asked at:** DataCamp and InterviewBit SQL joins interview guides, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Without FULL JOIN, write `LEFT JOIN` for everything on the left, then `UNION ALL` the right-table rows that have no match on the left (an anti-join); `LEFT JOIN UNION RIGHT JOIN` also works but `UNION` de-duplicates, so it can collapse legitimate duplicate rows, and it scans both sides twice.

**Schema and sample data:**
```sql
CREATE TABLE a_users(user_id INTEGER, name TEXT);
CREATE TABLE b_users(user_id INTEGER, email TEXT);
INSERT INTO a_users VALUES (1,'Ann'),(2,'Bob'),(3,'Cy'),(5,'Eve'),(5,'Eve');
INSERT INTO b_users VALUES (2,'bob@x.com'),(3,'cy@x.com'),(4,'di@x.com');
```
(User 5 is deliberately loaded twice in `a_users` with no match in `b_users`, to show what `UNION` does to duplicates.)

**SQL answer:** (same text as in the Code block)
The better version, LEFT JOIN plus `UNION ALL` of the right-only rows:
```sql
SELECT a.user_id, a.name, b.email FROM a_users a LEFT JOIN b_users b ON b.user_id = a.user_id
UNION ALL
SELECT b.user_id, NULL, b.email FROM b_users b
WHERE NOT EXISTS (SELECT 1 FROM a_users a WHERE a.user_id = b.user_id)
ORDER BY 1, 2, 3
```
The classic version (`LEFT JOIN UNION RIGHT JOIN`), which SQLite 3.45.1 accepts because it supports RIGHT JOIN (confirmed by running):
```sql
SELECT a.user_id, a.name, b.email FROM a_users a LEFT JOIN b_users b ON b.user_id = a.user_id
UNION
SELECT b.user_id, a.name, b.email FROM a_users a RIGHT JOIN b_users b ON b.user_id = a.user_id
ORDER BY 1, 2, 3
```
The native form to compare with (SQLite 3.45.1 ran it):
```sql
SELECT COALESCE(a.user_id, b.user_id) AS user_id, a.name, b.email
FROM a_users a FULL OUTER JOIN b_users b ON b.user_id = a.user_id
ORDER BY 1, 2, 3
```
MySQL has no FULL OUTER JOIN (hedged: its 8.4 JOIN documentation shows only LEFT and RIGHT; I did not run MySQL), which is why these emulations exist.

**pandas answer:** (same text as in the Code block)
```python
left = a.merge(b, on="user_id", how="left")
b_only = b[~b["user_id"].isin(a["user_id"])].assign(name=None)
p_main = pd.concat([left, b_only[["user_id", "name", "email"]]], ignore_index=True)
```
```python
# the direct equivalent
p_full = a.merge(b, on="user_id", how="outer", indicator=True)
```

**Example:** `a_users` has users 1, 2, 3, 5, 5; `b_users` has 2, 3, 4. A FULL JOIN returns 6 rows: 1 (name only), 2 and 3 (matched), 4 (email only), and 5 twice (name only). The LEFT JOIN part returns users 1, 2, 3, 5, 5 (five rows). The anti-join part returns user 4 (not in `a_users`). `UNION ALL` of the two gives 6 rows and matches the FULL JOIN. With `UNION`, the two identical rows `(5, Eve, NULL)` collapse into one, giving 5 rows, a silently wrong result.

**Code:** (run with `python3 -I`; the three SQL versions are compared and pandas is compared with the native FULL JOIN as sorted rows (user_id, name, email), NULL as None)
```python
# Q32: simulate FULL OUTER JOIN: LEFT JOIN UNION RIGHT JOIN, and LEFT JOIN UNION ALL anti-join; vs native FULL JOIN
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
print("sqlite", sqlite3.sqlite_version)
con.executescript("""
CREATE TABLE a_users(user_id INTEGER, name TEXT);
CREATE TABLE b_users(user_id INTEGER, email TEXT);
INSERT INTO a_users VALUES (1,'Ann'),(2,'Bob'),(3,'Cy'),(5,'Eve'),(5,'Eve');
INSERT INTO b_users VALUES (2,'bob@x.com'),(3,'cy@x.com'),(4,'di@x.com');
""")
# user 5 is in a_users twice (a loaded-twice row), and has no b row
# sql:native
SQL_FULL = """
SELECT COALESCE(a.user_id, b.user_id) AS user_id, a.name, b.email
FROM a_users a FULL OUTER JOIN b_users b ON b.user_id = a.user_id
ORDER BY 1, 2, 3
"""
# end
# sql:union
SQL_UNION = """
SELECT a.user_id, a.name, b.email FROM a_users a LEFT JOIN b_users b ON b.user_id = a.user_id
UNION
SELECT b.user_id, a.name, b.email FROM a_users a RIGHT JOIN b_users b ON b.user_id = a.user_id
ORDER BY 1, 2, 3
"""
# end
# sql:main
SQL_MAIN = """
SELECT a.user_id, a.name, b.email FROM a_users a LEFT JOIN b_users b ON b.user_id = a.user_id
UNION ALL
SELECT b.user_id, NULL, b.email FROM b_users b
WHERE NOT EXISTS (SELECT 1 FROM a_users a WHERE a.user_id = b.user_id)
ORDER BY 1, 2, 3
"""
# end
def sql(q): return [tuple(r) for r in con.execute(q).fetchall()]
full, uni, main = sql(SQL_FULL), sql(SQL_UNION), sql(SQL_MAIN)
print("native FULL OUTER JOIN:", len(full), "rows"); [print("  ", r) for r in full]
print("LEFT JOIN UNION RIGHT JOIN:", len(uni), "rows ->", "same as FULL" if uni == full else "DIFFERENT")
print("   FULL has", full.count((5, "Eve", None)), "copies of (5, Eve, None); UNION kept", uni.count((5, "Eve", None)))
print("LEFT JOIN UNION ALL anti-join:", len(main), "rows ->", "same as FULL" if main == full else "DIFFERENT")
assert main == full and uni != full and len(full) - len(uni) == 1

a = pd.read_sql_query("SELECT * FROM a_users", con)
b = pd.read_sql_query("SELECT * FROM b_users", con)
# pd:main
left = a.merge(b, on="user_id", how="left")
b_only = b[~b["user_id"].isin(a["user_id"])].assign(name=None)
p_main = pd.concat([left, b_only[["user_id", "name", "email"]]], ignore_index=True)
# end
# pd:full
p_full = a.merge(b, on="user_id", how="outer", indicator=True)
# end
def norm(df):
    rows = [tuple(None if pd.isna(v) else (int(v) if k == 0 else v) for k, v in enumerate(r))
            for r in df[["user_id", "name", "email"]].itertuples(index=False, name=None)]
    return sorted(rows, key=lambda r: (r[0], r[1] or "", r[2] or ""))
assert norm(p_main) == norm(p_full) == full
print("\npandas concat(left merge, right-only rows) == outer merge == SQL FULL (sorted)")
print("outer merge _merge counts:", p_full["_merge"].value_counts().to_dict())
print("asserts passed")
```

**Output (my run):**
```text
sqlite 3.45.1
native FULL OUTER JOIN: 6 rows
   (1, 'Ann', None)
   (2, 'Bob', 'bob@x.com')
   (3, 'Cy', 'cy@x.com')
   (4, None, 'di@x.com')
   (5, 'Eve', None)
   (5, 'Eve', None)
LEFT JOIN UNION RIGHT JOIN: 5 rows -> DIFFERENT
   FULL has 2 copies of (5, Eve, None); UNION kept 1
LEFT JOIN UNION ALL anti-join: 6 rows -> same as FULL

pandas concat(left merge, right-only rows) == outer merge == SQL FULL (sorted)
outer merge _merge counts: {'left_only': 3, 'both': 2, 'right_only': 1}
asserts passed
```

**Edge cases:**
- **Duplicates:** the example above; `UNION` (and `UNION DISTINCT`) removes duplicate rows, including legitimate ones. A FULL JOIN keeps both Eve rows, so the emulation must too.
- **Why `UNION ALL` is correct:** the two parts cannot overlap. Part 1 holds rows whose key exists in `a_users`; part 2 holds only rows whose key does not. So no row can be produced twice and no de-duplication is needed.
- **Key column in the right part:** take `b.user_id` there. In the `UNION` version, `a.user_id` would be NULL for right-only rows, so I selected `b.user_id` in the second SELECT (the alternative is `COALESCE(a.user_id, b.user_id)` in both).
- **NULL keys:** a NULL `user_id` never matches in the join. In the anti-join, `NOT EXISTS` keeps right rows with a NULL key, as FULL JOIN does. Do not use `NOT IN (SELECT user_id ...)`: one NULL in `a_users` would return no right-only rows (Part 1 Q13).
- **Column order and types** must match in every SELECT of the union (the NULL literal for `name` is typed by the other branch).
- **Cost:** `b_users` is read twice (in the LEFT JOIN and again in the anti-join) and `a_users` is probed twice. With an index on the join key it is cheap; without one it is two full passes. Engine specific and not measured here.

**Then explain:**
- **Why not `UNION`:** it costs a sort or hash to de-duplicate the whole result, and it changes the answer when duplicates are real. `UNION ALL` does neither.
- **Why the anti-join form beats `LEFT UNION RIGHT`:** it joins `b_users` once and filters instead of re-joining everything; it is also exact on duplicates.
- **Native FULL JOIN:** SQLite 3.45.1 ran it; PostgreSQL, SQL Server, Oracle, Snowflake and BigQuery support it (from memory, not executed). Use it when available; it is shorter and cannot make this mistake.
- **pandas:** `how="outer"` is the FULL JOIN. The concat version mirrors the SQL emulation (left merge plus right-only rows via `~isin`) and matched the outer merge; the outer merge's `_merge` counts show 3 left only, 2 both, 1 right only.

**Follow-ups:**
- *Could you add a `source` column?* Yes: `'a_only'`, `'both'`, `'b_only'` by testing which side's key IS NULL (Q16 does this with FULL JOIN).
- *What about MySQL's RIGHT JOIN?* It exists in MySQL, so `LEFT JOIN UNION RIGHT JOIN` runs there; the anti-join form is still preferred (hedged, not executed).
- *Do you ever need UNION instead of UNION ALL here?* Only if the sources can produce duplicate result rows that you also want collapsed, which is a different requirement from a FULL JOIN.

**Common mistakes:**
- Using `UNION` and losing duplicate rows (or paying the de-duplication cost for nothing).
- Using the wrong key column in the right-only branch, so the user id is NULL.
- A `NOT IN` anti-join with NULLs in the left key.
- Forgetting that a FULL JOIN is not supported in the engine and getting a syntax error in production.

### Q33 ⭐⭐ 🟡 Consecutive rows with a self join (join approach only, no window functions): logs(id, num) with consecutive ids. Find numbers that appear at least three times in a row (the LeetCode Consecutive Numbers idea) by joining the table to itself on id + 1 and id + 2. Say what breaks when ids have gaps, why DISTINCT is needed, and the pandas shift-free equivalent using merge with an offset key.
**Asked at:** public LeetCode-style problem bank (SQL 50 join problems, known only from repo snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Join `logs` to itself three times, `l2.id = l1.id + 1` and `l3.id = l1.id + 2` with the same `num` on all three, and select `DISTINCT num`; it works only when ids are gap-free, and DISTINCT is needed because a run longer than three produces several overlapping triples.

**Schema and sample data:**
```sql
CREATE TABLE logs(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs VALUES (1,1),(2,1),(3,1),(4,1),(5,2),(6,3),(7,3),(8,2),(9,2),(10,2);
CREATE TABLE logs_gap(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs_gap VALUES (1,7),(2,7),(4,7),(5,9);   -- id 3 was deleted
```

**SQL answer:** (same text as in the Code block)
```sql
SELECT DISTINCT l1.num AS consecutive_num
FROM logs l1
JOIN logs l2 ON l2.id = l1.id + 1 AND l2.num = l1.num
JOIN logs l3 ON l3.id = l1.id + 2 AND l3.num = l1.num
ORDER BY 1
```

**pandas answer:** (same text as in the Code block). No `shift`: shift the key instead and merge.
```python
def consecutive(df):
    n1 = df.assign(id=df["id"] - 1).rename(columns={"num": "num1"})     # row at id+1, keyed by this row's id
    n2 = df.assign(id=df["id"] - 2).rename(columns={"num": "num2"})     # row at id+2
    m = (df.merge(n1, on="id", validate="one_to_one")
           .merge(n2, on="id", validate="one_to_one"))
    return sorted(m.loc[(m["num"] == m["num1"]) & (m["num"] == m["num2"]), "num"].unique().tolist())
```

**Example:** `logs` has 1, 1, 1, 1 at ids 1 to 4, then 2, 3, 3, 2, 2, 2. Starting from id 1: id 2 and id 3 also hold 1, so a triple exists. Starting from id 2: ids 3 and 4 hold 1, a second triple. So the number 1 is returned twice without `DISTINCT` (the output shows `[1, 1, 2]`). Starting from id 8: ids 9 and 10 hold 2, so 2 qualifies. The 3 appears only twice in a row (ids 6 and 7), so it fails. Answer with `DISTINCT`: 1 and 2.

**Code:** (run with `python3 -I`; SQL and pandas compared as sorted lists of numbers, both for `logs` and for the gap table)
```python
# Q33: Consecutive Numbers with a self join on id+1 and id+2; gaps; DISTINCT; pandas offset-key merge
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE logs(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs VALUES (1,1),(2,1),(3,1),(4,1),(5,2),(6,3),(7,3),(8,2),(9,2),(10,2);
CREATE TABLE logs_gap(id INTEGER PRIMARY KEY, num INTEGER);
INSERT INTO logs_gap VALUES (1,7),(2,7),(4,7),(5,9);   -- id 3 was deleted
""")
# sql:main
SQL_MAIN = """
SELECT DISTINCT l1.num AS consecutive_num
FROM logs l1
JOIN logs l2 ON l2.id = l1.id + 1 AND l2.num = l1.num
JOIN logs l3 ON l3.id = l1.id + 2 AND l3.num = l1.num
ORDER BY 1
"""
# end
SQL_NO_DISTINCT = SQL_MAIN.replace("SELECT DISTINCT", "SELECT")
def sql(q, t="logs"): return [r[0] for r in con.execute(q.replace("logs", t)).fetchall()]
main = sql(SQL_MAIN)
print("with DISTINCT:   ", main)
print("without DISTINCT:", sql(SQL_NO_DISTINCT), "(num 1 appears in two overlapping triples: ids 1-3 and 2-4)")
print("gap table logs_gap (ids 1,2,4 all num 7):", sql(SQL_MAIN, "logs_gap"), "<- misses it, id 3 is missing")

logs = pd.read_sql_query("SELECT * FROM logs", con)
logs_gap = pd.read_sql_query("SELECT * FROM logs_gap", con)
# pd:main
def consecutive(df):
    n1 = df.assign(id=df["id"] - 1).rename(columns={"num": "num1"})     # row at id+1, keyed by this row's id
    n2 = df.assign(id=df["id"] - 2).rename(columns={"num": "num2"})     # row at id+2
    m = (df.merge(n1, on="id", validate="one_to_one")
           .merge(n2, on="id", validate="one_to_one"))
    return sorted(m.loc[(m["num"] == m["num1"]) & (m["num"] == m["num2"]), "num"].unique().tolist())
# end
p_main = consecutive(logs)
assert p_main == main == [1, 2]
assert consecutive(logs_gap) == sql(SQL_MAIN, "logs_gap") == []
print("\npandas offset-key merge:", p_main, "== SQL; gap table:", consecutive(logs_gap))
print("rows after the two inner merges on logs (ids that have id+1 and id+2):", len(
    logs.merge(logs.assign(id=logs["id"] - 1), on="id").merge(logs.assign(id=logs["id"] - 2), on="id")))
print("asserts passed")
```

**Output (my run):**
```text
with DISTINCT:    [1, 2]
without DISTINCT: [1, 1, 2] (num 1 appears in two overlapping triples: ids 1-3 and 2-4)
gap table logs_gap (ids 1,2,4 all num 7): [] <- misses it, id 3 is missing

pandas offset-key merge: [1, 2] == SQL; gap table: []
rows after the two inner merges on logs (ids that have id+1 and id+2): 8
asserts passed
```

**Edge cases:**
- **Gaps in ids:** in `logs_gap`, the rows with ids 1, 2 and 4 all hold 7 and are consecutive in the table, but `id + 2` does not exist for id 2. The query returned nothing. The join approach assumes ids are exactly `1, 2, 3, ...` (the LeetCode problem states this). If ids can have gaps, number the rows first with `ROW_NUMBER()` (Part 4) or use a window function with `LAG` (Part 5) and compare neighbours by position; not covered in this part.
- **Why DISTINCT:** one run of four equal numbers contains two triples; a run of n has n - 2 triples. `DISTINCT` collapses them.
- **At least three:** runs longer than three qualify, as 1 (four times) did. For exactly three, you would also need to check the neighbours on each side.
- **Ids that are not unique** would multiply the join; the primary key rules this out. In pandas, `validate="one_to_one"` on the shifted frames asserts it.
- **NULL num:** `NULL = NULL` is not TRUE, so NULLs never form a run (not run on the sample).
- **Unsorted ids** do not matter for the join, unlike for window functions.

**Then explain:**
- **Three aliases, one table:** `l1` is the starting row, `l2` the row one id later, `l3` the row two ids later. The two conditions `l2.num = l1.num` and `l3.num = l1.num` say all three values are equal.
- **pandas without `shift`:** subtract the offset from the id of a copy (`id - 1`), so that the row that is really at `id + 1` now carries this row's id and a plain `on="id"` merge lines them up. Two such merges give the three values in one row; the filter does the comparison. `unique()` plays the role of `DISTINCT`. At the edges, ids without `id + 1` or `id + 2` drop out of the inner merges, like in SQL (8 rows survived in my run).
- **Why shift is simpler in practice:** `df["num"].eq(df["num"].shift(1))` is shorter, but depends on the row order being right; the offset-key merge depends on ids instead, which is the same assumption as the SQL join.
- **Generalising to n in a row** needs n - 1 joins; a window-function solution is better (Part 5).

**Follow-ups:**
- *How would you return the start id of each run?* `SELECT l1.id` instead of the number, then group, or use gaps and islands (Part 7).
- *What about "at least 5 times"?* Five aliases, or windows; the self-join gets long.
- *What if the table has no id?* Then there is no order to compare; you must add or define one.

**Common mistakes:**
- Forgetting `DISTINCT`, which returns the same number repeatedly.
- Comparing `l1.num = l2.num` and `l2.num = l3.num` but only `l2.id = l1.id + 1` (missing the third id condition).
- Assuming ids are gap-free after deletes.
- Using `l1.id < l2.id` instead of `id + 1`, which matches rows that are not adjacent.

### Q34 ⭐⭐ 🟡 Many-to-many and duplicate keys in pandas: orders_a(order_id, item) and orders_b(order_id, tag) each repeat some order_id values. Explain why merge returns the Cartesian product of the matching rows per key (2 x 3 = 6), how validate='one_to_one', 'one_to_many' and 'many_to_one' raise MergeError, how to check len(result) against expectations, and the SQL parallel.
**Asked at:** pandas user guide (merge, join, concatenate) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** When a key repeats on both sides, merge pairs every left row with every right row for that key, so a key with 2 left rows and 3 right rows gives 2 x 3 = 6 rows; `validate=` makes pandas raise `MergeError` when the key is not unique where you said it should be, and `len(result)` should be checked against the sum of `na * nb` per key.

**Schema and sample data:**
```sql
CREATE TABLE orders_a(order_id INTEGER, item TEXT);
CREATE TABLE orders_b(order_id INTEGER, tag TEXT);
INSERT INTO orders_a VALUES (1,'pen'),(1,'ink'),(2,'book'),(3,'cap');
INSERT INTO orders_b VALUES (1,'gift'),(1,'rush'),(1,'fragile'),(2,'gift'),(4,'promo');
```

**SQL answer:** (same text as in the Code block)
```sql
SELECT a.order_id, a.item, b.tag
FROM orders_a a JOIN orders_b b ON b.order_id = a.order_id
ORDER BY a.order_id, a.item, b.tag
```
SQL has no `validate=`; the equivalent checks are:
```sql
SELECT order_id, COUNT(*) AS n FROM orders_a GROUP BY order_id HAVING COUNT(*) > 1
```
```sql
SELECT SUM(na * nb) FROM
  (SELECT order_id, COUNT(*) AS na FROM orders_a GROUP BY order_id) x
  JOIN (SELECT order_id, COUNT(*) AS nb FROM orders_b GROUP BY order_id) y ON y.order_id = x.order_id
```

**pandas answer:** (same text as in the Code block)
```python
m = a.merge(b, on="order_id", how="inner")
expected = int((a["order_id"].value_counts() * b["order_id"].value_counts()).sum())   # per key: na * nb (inner)
assert len(m) == expected
```
```python
for v in ["one_to_one", "one_to_many", "many_to_one", "many_to_many"]:
    try:
        r = a.merge(b, on="order_id", validate=v)
        print(f"validate={v!r:15} -> ok, {len(r)} rows")
    except pd.errors.MergeError as e:
        print(f"validate={v!r:15} -> MergeError:", str(e).splitlines()[0])
```

**Example:** Order 1 has 2 items (pen, ink) and 3 tags (gift, rush, fragile): the join pairs every item with every tag, 2 x 3 = 6 rows (`pen/gift`, `pen/rush`, `pen/fragile`, `ink/gift`, ...). Order 2 has 1 item and 1 tag: 1 row. Order 3 (only in `a`) and order 4 (only in `b`) have no partner and vanish in an inner merge. Total: 6 + 1 = 7 rows. The check `value_counts() * value_counts()` gives 2 x 3 = 6 and 1 x 1 = 1 for the keys present on both sides, so 7 expected.

**Code:** (run with `python3 -I`; the pandas inner merge is compared with the SQL JOIN as sorted lists of (order_id, item, tag))
```python
# Q34: many-to-many merge in pandas: Cartesian product per key, validate= errors, row-count check, SQL parallel
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders_a(order_id INTEGER, item TEXT);
CREATE TABLE orders_b(order_id INTEGER, tag TEXT);
INSERT INTO orders_a VALUES (1,'pen'),(1,'ink'),(2,'book'),(3,'cap');
INSERT INTO orders_b VALUES (1,'gift'),(1,'rush'),(1,'fragile'),(2,'gift'),(4,'promo');
""")
# sql:main
SQL_MAIN = """
SELECT a.order_id, a.item, b.tag
FROM orders_a a JOIN orders_b b ON b.order_id = a.order_id
ORDER BY a.order_id, a.item, b.tag
"""
# end
# sql:dup
SQL_DUP = """
SELECT order_id, COUNT(*) AS n FROM orders_a GROUP BY order_id HAVING COUNT(*) > 1
"""
# end
# sql:expected
SQL_EXPECTED = """
SELECT SUM(na * nb) FROM
  (SELECT order_id, COUNT(*) AS na FROM orders_a GROUP BY order_id) x
  JOIN (SELECT order_id, COUNT(*) AS nb FROM orders_b GROUP BY order_id) y ON y.order_id = x.order_id
"""
# end
sql_main = [tuple(r) for r in con.execute(SQL_MAIN).fetchall()]
print("SQL join rows:", len(sql_main), "->", sql_main)
print("duplicate keys in orders_a:", con.execute(SQL_DUP).fetchall())
print("expected rows = SUM(na * nb) per key:", con.execute(SQL_EXPECTED).fetchone()[0])

a = pd.read_sql_query("SELECT * FROM orders_a", con)
b = pd.read_sql_query("SELECT * FROM orders_b", con)
# pd:main
m = a.merge(b, on="order_id", how="inner")
expected = int((a["order_id"].value_counts() * b["order_id"].value_counts()).sum())   # per key: na * nb (inner)
assert len(m) == expected
# end
p_main = [tuple(r) for r in m.sort_values(["order_id", "item", "tag"]).itertuples(index=False, name=None)]
assert p_main == sql_main
print("\npandas inner merge rows:", len(m), "== expected", expected, "== SQL", len(sql_main))
print("rows per order_id after the merge:", m["order_id"].value_counts().sort_index().to_dict())

# pd:validate
for v in ["one_to_one", "one_to_many", "many_to_one", "many_to_many"]:
    try:
        r = a.merge(b, on="order_id", validate=v)
        print(f"validate={v!r:15} -> ok, {len(r)} rows")
    except pd.errors.MergeError as e:
        print(f"validate={v!r:15} -> MergeError:", str(e).splitlines()[0])
# end
# validate when one side IS unique
b_unique = b.drop_duplicates("order_id")
r = a.merge(b_unique, on="order_id", validate="many_to_one")
print("\nafter b.drop_duplicates('order_id'): many_to_one ok,", len(r), "rows (orders_a rows 1, 1, 2 matched)")
try:
    a.merge(b_unique, on="order_id", validate="one_to_many")
except pd.errors.MergeError as e:
    print("one_to_many on the same data -> MergeError:", str(e).splitlines()[0])

# how= and indicator for the unmatched keys
o = a.merge(b, on="order_id", how="outer", indicator=True)
print("\nouter merge rows:", len(o), "| _merge:", o["_merge"].value_counts().to_dict())
print("asserts passed")
```

**Output (my run):**
```text
SQL join rows: 7 -> [(1, 'ink', 'fragile'), (1, 'ink', 'gift'), (1, 'ink', 'rush'), (1, 'pen', 'fragile'), (1, 'pen', 'gift'), (1, 'pen', 'rush'), (2, 'book', 'gift')]
duplicate keys in orders_a: [(1, 2)]
expected rows = SUM(na * nb) per key: 7

pandas inner merge rows: 7 == expected 7 == SQL 7
rows per order_id after the merge: {1: 6, 2: 1}
validate='one_to_one'    -> MergeError: Merge keys are not unique in either left or right dataset; not a one-to-one merge.
validate='one_to_many'   -> MergeError: Merge keys are not unique in left dataset; not a one-to-many merge
validate='many_to_one'   -> MergeError: Merge keys are not unique in right dataset; not a many-to-one merge
validate='many_to_many'  -> ok, 7 rows

after b.drop_duplicates('order_id'): many_to_one ok, 3 rows (orders_a rows 1, 1, 2 matched)
one_to_many on the same data -> MergeError: Merge keys are not unique in left dataset; not a one-to-many merge

outer merge rows: 9 | _merge: {'both': 7, 'left_only': 1, 'right_only': 1}
asserts passed
```

**Edge cases:**
- **Which validate fails:** with duplicates on both sides, `one_to_one` fails (message says not unique in either dataset), `one_to_many` fails (left not unique) and `many_to_one` fails (right not unique); `many_to_many` passes and is the default, so no check happens unless you ask. The messages come from my run on pandas 3.0.5.
- **When one side is unique:** after `b.drop_duplicates("order_id")`, `many_to_one` passed (3 rows), and `one_to_many` on the same data still raised, because the left side has duplicates. Remember the naming: the first word is the left frame, the second is the right frame.
- **validate only looks at the merge keys**, not at whether the result is what you meant. It also does not look at rows without a partner.
- **Unmatched keys:** orders 3 and 4 vanish in the inner merge. `how="outer", indicator=True` kept them: 9 rows, with 7 `both`, 1 `left_only` and 1 `right_only`.
- **NaN keys:** NaN matches NaN in a pandas merge, so many rows with a missing key all pair with each other, a hidden many-to-many (see Q24 and Q6; here the keys have no NaN).
- **Growth is multiplicative:** two frames with 1,000 repeated rows per key give a million per key. Check `len(a)`, `len(b)` and `len(result)` before you continue.

**Then explain:**
- **Why it is a Cartesian product per key:** the join pairs rows, not keys. For each key it returns all combinations of left rows and right rows with that key.
- **How to avoid it:** decide the grain you want. Usually one side should be reduced to one row per key first (`drop_duplicates`, or `groupby` and aggregate), and `validate="one_to_many"` or `"many_to_one"` documents and enforces that.
- **Check the size:** compute the expected count from the key counts (as in the code) and `assert len(result) == expected`; if the number is not what you expect, a key is duplicated somewhere.
- **SQL parallel:** a SQL JOIN does exactly the same (7 rows above). SQL has no `validate` flag; you check uniqueness with `GROUP BY key HAVING COUNT(*) > 1` and compare row counts, or enforce it with a primary key or unique constraint on the table (Q9, Q40).
- **When many-to-many is legitimate:** for example items and tags where you really want every combination. Usually it is a mistake, and the fan-out inflates sums (Q12, Q13).

**Follow-ups:**
- *What does `validate="one_to_one"` check?* That the key is unique in both frames; it raises before the merge result is returned.
- *Does validate cost much?* It checks key uniqueness, which is cheap compared with building a large product (concept; not measured).
- *How do you aggregate before merging?* `b.groupby("order_id")["tag"].agg(list)` or a count per key, then a one-to-one merge.

**Common mistakes:**
- Merging without `validate` and noticing the inflated row count only downstream.
- Mixing up `one_to_many` and `many_to_one` (the first word is the left side).
- Using `drop_duplicates()` on the whole frame instead of on the key, which keeps duplicate keys with different values.
- Expecting `validate` to check anything about unmatched rows.
