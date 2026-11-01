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
