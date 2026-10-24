### Q39 ⭐ 🟡 Top N overall versus top N per group, and pagination with ROW_NUMBER: products(product_id, category, name, price). Show ORDER BY price DESC LIMIT 5 (overall), the per-group top 5 with ROW_NUMBER, and page 2 of a list (rows 11 to 20) with ROW_NUMBER BETWEEN versus LIMIT 10 OFFSET 10. Explain why OFFSET pagination gets slower on deep pages and is unstable if ties or inserts exist (a unique tie-breaker is needed), and give the pandas nlargest, head and iloc versions.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** `ORDER BY price DESC LIMIT 5` gives the top 5 rows overall, `ROW_NUMBER() OVER (PARTITION BY category ...)` gives the top N inside each group, and a page is just a slice of a fully ordered list, so the order needs a unique tie-breaker or pages can overlap or skip rows.

**Schema and sample data:** 14 products in three categories. Two Books at price 40 (ids 1 and 3), two Toys at 30 (5 and 7), two Tech at 20 (9 and 12), two at 90 (6 and 11), so ties are on purpose. The question says top 5 per group and pages of 10; the table is tiny, so I use top 2 per category and pages of 5 (page 2 is rows 6 to 10). The logic is identical.
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES
 (1,'Books','Atlas',40),(2,'Books','Brief',25),(3,'Books','Cipher',40),(4,'Books','Digest',10),
 (5,'Toys','Kite',30),(6,'Toys','Lego',90),(7,'Toys','Mask',30),(8,'Toys','Net',15),
 (9,'Tech','Cable',20),(10,'Tech','Dock',60),(11,'Tech','Earbuds',90),(12,'Tech','Fan',20),
 (13,'Tech','Gimbal',150),(14,'Books','Epic',55);
```

**SQL answer:** all five queries are in the Code block. Overall top 5 (`SQL_TOP`), per-category top 2 (`SQL_PER_GROUP`), page 2 by row number (`SQL_PAGE_RN`), page 2 by offset (`SQL_PAGE_OFFSET`) and a keyset version (`SQL_KEYSET`).
```sql
SELECT product_id, category, name, price
FROM products
ORDER BY price DESC, product_id
LIMIT 5
```
```sql
WITH r AS (
  SELECT product_id, category, name, price,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC, product_id) AS rn
  FROM products
)
SELECT category, rn, product_id, name, price
FROM r
WHERE rn <= 2
ORDER BY category, rn
```
```sql
WITH r AS (
  SELECT product_id, name, price,
         ROW_NUMBER() OVER (ORDER BY price DESC, product_id) AS rn
  FROM products
)
SELECT rn, product_id, name, price
FROM r
WHERE rn BETWEEN 6 AND 10
ORDER BY rn
```
```sql
SELECT product_id, name, price
FROM products
ORDER BY price DESC, product_id
LIMIT 5 OFFSET 5
```
```sql
SELECT product_id, name, price
FROM products
WHERE price < ? OR (price = ? AND product_id > ?)
ORDER BY price DESC, product_id
LIMIT 5
```

**pandas answer:** sort once by price descending then product_id, then `head`, `groupby().head` and `iloc` are all slices of the same ordered frame. `nlargest` is the one-liner for the overall case.
```python
ordered = prod.sort_values(["price", "product_id"], ascending=[False, True])
pd_top = ordered.head(5)
pd_nlargest = prod.nlargest(5, "price")          # keep='first': ties resolved by row order
pd_group = ordered.groupby("category").head(2)
pd_page2 = ordered.iloc[5:10]
```

**Example:** sorted by price DESC, product_id ASC the whole list is: 13 (150), 6 (90), 11 (90), 10 (60), 14 (55), 1 (40), 3 (40), 5 (30), 7 (30), 2 (25), then 9 (20), 12 (20), 8 (15), 4 (10).
- Overall top 5 is the first five: 13, 6, 11, 10, 14 (6 beats 11 at the 90 tie because its id is lower).
- Per category top 2: Books 14 (55) and 1 (40, because id 1 beats id 3 on the 40 tie); Tech 13 and 11; Toys 6 and 5 (30 tie broken by id).
- Page 2 (rows 6 to 10): 1, 3, 5, 7, 2. `ROW_NUMBER BETWEEN 6 AND 10` and `LIMIT 5 OFFSET 5` return the same rows.

**Code:** run with `python3 -I`.
```python
# Q39: top N overall, top N per group, pagination
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, category TEXT, name TEXT, price INTEGER);
INSERT INTO products VALUES
 (1,'Books','Atlas',40),(2,'Books','Brief',25),(3,'Books','Cipher',40),(4,'Books','Digest',10),
 (5,'Toys','Kite',30),(6,'Toys','Lego',90),(7,'Toys','Mask',30),(8,'Toys','Net',15),
 (9,'Tech','Cable',20),(10,'Tech','Dock',60),(11,'Tech','Earbuds',90),(12,'Tech','Fan',20),
 (13,'Tech','Gimbal',150),(14,'Books','Epic',55);
"""
SQL_TOP = """
SELECT product_id, category, name, price
FROM products
ORDER BY price DESC, product_id
LIMIT 5
"""
SQL_PER_GROUP = """
WITH r AS (
  SELECT product_id, category, name, price,
         ROW_NUMBER() OVER (PARTITION BY category ORDER BY price DESC, product_id) AS rn
  FROM products
)
SELECT category, rn, product_id, name, price
FROM r
WHERE rn <= 2
ORDER BY category, rn
"""
SQL_PAGE_RN = """
WITH r AS (
  SELECT product_id, name, price,
         ROW_NUMBER() OVER (ORDER BY price DESC, product_id) AS rn
  FROM products
)
SELECT rn, product_id, name, price
FROM r
WHERE rn BETWEEN 6 AND 10
ORDER BY rn
"""
SQL_PAGE_OFFSET = """
SELECT product_id, name, price
FROM products
ORDER BY price DESC, product_id
LIMIT 5 OFFSET 5
"""
SQL_KEYSET = """
SELECT product_id, name, price
FROM products
WHERE price < ? OR (price = ? AND product_id > ?)
ORDER BY price DESC, product_id
LIMIT 5
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s, p=(): pd.read_sql_query(s, con, params=p)

top = q(SQL_TOP)
per_group = q(SQL_PER_GROUP)
page_rn = q(SQL_PAGE_RN)
page_off = q(SQL_PAGE_OFFSET)
print("overall top 5:"); print(top.to_string(index=False))
print("\nper-category top 2:"); print(per_group.to_string(index=False))
print("\npage 2 via ROW_NUMBER BETWEEN 6 AND 10:"); print(page_rn.to_string(index=False))
assert page_rn[["product_id", "name", "price"]].equals(page_off)
print("page 2 via LIMIT 5 OFFSET 5 is identical: True")

# pandas
prod = q("SELECT * FROM products")
# pd:main
ordered = prod.sort_values(["price", "product_id"], ascending=[False, True])
pd_top = ordered.head(5)
pd_nlargest = prod.nlargest(5, "price")          # keep='first': ties resolved by row order
pd_group = ordered.groupby("category").head(2)
pd_page2 = ordered.iloc[5:10]
# pd:end
pd.testing.assert_frame_equal(top, pd_top.reset_index(drop=True))
assert pd_nlargest["product_id"].tolist() == top["product_id"].tolist()   # equal here only because rows are stored in product_id order
g = pd_group.sort_values(["category", "price", "product_id"], ascending=[True, False, True]).reset_index(drop=True)
assert per_group[["category", "product_id", "price"]].equals(g[["category", "product_id", "price"]])
pd.testing.assert_frame_equal(page_off, pd_page2[["product_id", "name", "price"]].reset_index(drop=True))
print("\npandas: head(5), nlargest(5), groupby.head(2), iloc[5:10] all match the SQL rows")

# instability: ties and inserts. Unstable page = ORDER BY price DESC only, no tie-breaker.
print("\nrows 6 and 7 tie at price 40 (products 1 and 3). With page size 6 the page boundary splits them.")
print("ORDER BY price DESC only, rows 6-7:", con.execute("SELECT product_id, price FROM products ORDER BY price DESC LIMIT 2 OFFSET 5").fetchall(),
      "<- product 1 first on this run; without a tie-breaker nothing guarantees it stays that way")
print("ORDER BY price DESC, product_id, rows 6-7:", con.execute("SELECT product_id, price FROM products ORDER BY price DESC, product_id LIMIT 2 OFFSET 5").fetchall())

# insert between page fetches: OFFSET repeats a row, keyset does not
page1 = q(SQL_TOP)
con.execute("INSERT INTO products VALUES (15,'Tech','Hub',200)")        # a new top-priced row arrives after page 1 was shown
page2_offset = q(SQL_PAGE_OFFSET)
last = page1.iloc[-1]
# keyset on the same order (price DESC, product_id ASC): next rows are price < last.price OR (price = last.price AND product_id > last.product_id)
page2_keyset = q(SQL_KEYSET, (int(last["price"]), int(last["price"]), int(last["product_id"])))
print("\nafter inserting Hub (200) once page 1 was shown:")
print("page 1 shown earlier :", page1["product_id"].tolist())
print("page 2 by OFFSET     :", page2_offset["product_id"].tolist(), "<- repeats product", sorted(set(page1["product_id"]) & set(page2_offset["product_id"])))
print("page 2 by keyset     :", page2_keyset["product_id"].tolist())
assert set(page1["product_id"]) & set(page2_offset["product_id"])
assert not (set(page1["product_id"]) & set(page2_keyset["product_id"]))
print("asserts passed")
```

**Output (my run):**
```text
overall top 5:
 product_id category    name  price
         13     Tech  Gimbal    150
          6     Toys    Lego     90
         11     Tech Earbuds     90
         10     Tech    Dock     60
         14    Books    Epic     55

per-category top 2:
category  rn  product_id    name  price
   Books   1          14    Epic     55
   Books   2           1   Atlas     40
    Tech   1          13  Gimbal    150
    Tech   2          11 Earbuds     90
    Toys   1           6    Lego     90
    Toys   2           5    Kite     30

page 2 via ROW_NUMBER BETWEEN 6 AND 10:
 rn  product_id   name  price
  6           1  Atlas     40
  7           3 Cipher     40
  8           5   Kite     30
  9           7   Mask     30
 10           2  Brief     25
page 2 via LIMIT 5 OFFSET 5 is identical: True

pandas: head(5), nlargest(5), groupby.head(2), iloc[5:10] all match the SQL rows

rows 6 and 7 tie at price 40 (products 1 and 3). With page size 6 the page boundary splits them.
ORDER BY price DESC only, rows 6-7: [(1, 40), (3, 40)] <- product 1 first on this run; without a tie-breaker nothing guarantees it stays that way
ORDER BY price DESC, product_id, rows 6-7: [(1, 40), (3, 40)]

after inserting Hub (200) once page 1 was shown:
page 1 shown earlier : [13, 6, 11, 10, 14]
page 2 by OFFSET     : [14, 1, 3, 5, 7] <- repeats product [14]
page 2 by keyset     : [1, 3, 5, 7, 2]
asserts passed
```

**Edge cases:**
- Ties: Atlas and Cipher both cost 40. Without `product_id` in the ORDER BY the engine may put either first, so which one is on which page can change. I printed rows 6 and 7 without the tie-breaker; they came out in id order on this tiny table, but nothing guarantees that.
- A category with fewer than N products simply returns fewer rows (ROW_NUMBER never invents rows).
- Insert between pages: after page 1 was shown I inserted a new top-priced product (id 15). `OFFSET 5` then returned product 14 again, which was already on page 1 (see output). The keyset query did not repeat it.
- `nlargest(5, 'price')` resolves ties by row order (keep='first'). It matched here only because the frame is stored in product_id order, so I assert against the explicit sort.
- Deleting a row between pages has the opposite effect: a row is skipped.

**Then explain:**
- **Overall versus per group:** `LIMIT` cuts the whole result once; per-group needs a window with `PARTITION BY category` and a filter on the row number, in a CTE because a window cannot sit in WHERE.
- **ROW_NUMBER BETWEEN versus LIMIT/OFFSET:** same rows. LIMIT/OFFSET is shorter; the row-number form is useful when the page filter must live inside a bigger query or when you also want the number printed.
- **Why deep pages are slow:** to return rows 1,000,001 to 1,000,010 the engine still has to produce and throw away the first million in order. I did not time this on SQLite here; it is the standard explanation (an index on the sort key helps the sort, but the skip is still a walk). Not executed on other engines.
- **Why unstable:** OFFSET counts positions, not rows. Inserts or deletes shift positions between requests, and tied rows can move.
- **Keyset (seek) pagination:** remember the last (price, product_id) you showed and ask for rows after it. The cost does not grow with the page number and inserted rows do not shift pages. Trade-off: you cannot jump to page 40 directly. Row-value comparisons such as `(price, product_id) < (?, ?)` exist in some engines (not run here); I wrote the expanded `OR` form, which runs on SQLite and handles the mixed directions (price DESC, product_id ASC).

**Follow-ups:**
- *How would you do this for a million-row table in a web app?* Keyset pagination on an indexed unique sort key.
- *Why include product_id in ORDER BY if price is almost unique?* Almost is not unique; one tie is enough to cause duplicates or gaps between pages.
- *`LIMIT 5` per group in one statement?* Not in standard SQL without a window (or LATERAL in engines that have it; not executed here).

**Common mistakes:**
- `LIMIT 2` on a grouped query and expecting two per group.
- OFFSET pagination on a non-unique ORDER BY.
- Putting `ROW_NUMBER() BETWEEN ...` in WHERE instead of using a CTE.
- Off-by-one: page p of size s is rows `(p-1)*s + 1` to `p*s`, and `OFFSET (p-1)*s`.

### Q40 ⭐ 🟡 Window function performance concept: employees(emp_id, name, dept_id, salary) with a million rows in a real system. Explain that a ranking window needs the rows sorted by partition and order keys, so the cost is a sort (or an index scan that delivers that order), that several windows with the same PARTITION BY/ORDER BY can share one sort, that different windows force different sorts (use a named window to see the reuse), and how an index on (dept_id, salary) may help. Run EXPLAIN QUERY PLAN on a SQLite example and hedge other engines; deeper tuning is Part 11.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** A ranking window has to see each partition's rows in the ORDER BY order, so its cost is a sort (or an index scan that already delivers that order); windows with the same PARTITION BY/ORDER BY can share one sort, different windows each pay for their own, and an index on (dept_id, salary) can remove the sort.

**Schema and sample data:** the question says a million rows; I cannot run that sensibly here, so the Code block builds 3000 employees in 30 departments with many salary ties and looks at the query plan text, which does not depend on the row count. No timings are printed, because they would vary by machine and say little at this size.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
-- 3000 rows: dept_id = i % 30, salary = 3000 + (i * 37) % 500 (loop in the Code block)
```

**SQL answer:** three queries, run through `EXPLAIN QUERY PLAN` before and after an index. `SQL_ONE` is one window, `SQL_SAME` uses a named window for ROW_NUMBER and RANK plus a SUM with only PARTITION BY, `SQL_DIFF` has two different windows.
```sql
SELECT emp_id, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
FROM employees
```
```sql
SELECT emp_id,
       ROW_NUMBER() OVER w AS rn,
       RANK()       OVER w AS rk,
       SUM(salary)  OVER (PARTITION BY dept_id) AS dept_total
FROM employees
WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC, emp_id)
```
```sql
SELECT emp_id,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn,
       ROW_NUMBER() OVER (ORDER BY salary, emp_id) AS overall_rn
FROM employees
```

**pandas answer:** pandas has no planner; the same work is an explicit sort plus `cumcount`. It is here to check the ranking, not to compare cost.
```python
ordered = emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
ordered["rn"] = ordered.groupby("dept_id").cumcount() + 1
pd_res = ordered.sort_values("emp_id").reset_index(drop=True)[["emp_id", "dept_id", "salary", "rn"]]
```

**Example:** how to read the plan lines in the output below (SQLite 3.45.1 wording).
- Query 1, no index: `SCAN employees`, then `USE TEMP B-TREE FOR ORDER BY`. The temp b-tree is the sort by (dept_id, salary DESC, emp_id). One window, one sort.
- Query 2: ROW_NUMBER and RANK share the named window, and SUM uses `PARTITION BY dept_id` only. The plan has two temp b-trees, so SQLite did not reuse the first sort for the SUM window even though its partitioning is a prefix of the other. I would not assume other engines behave the same (not executed).
- Query 3: two different windows, two temp b-trees.
- Query 4: after `CREATE INDEX ix_dept_salary ON employees(dept_id, salary DESC, emp_id)` the plan is `SCAN employees USING COVERING INDEX ix_dept_salary` and the temp b-tree disappears: the index delivers rows already in window order.
- Query 5 (two different windows with the index): still two temp b-trees. The index matches one window's order at best, and the plan text does not say which window each sort belongs to, so I do not claim more than "the index did not remove both sorts".

**Code:** run with `python3 -I`.
```python
# Q40: window function cost = a sort; EXPLAIN QUERY PLAN on SQLite 3.45
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);")
# deterministic toy data: 3000 employees, 30 departments, salaries with many ties
rows = [(i, f"e{i}", i % 30, 3000 + (i * 37) % 500) for i in range(1, 3001)]
con.executemany("INSERT INTO employees VALUES (?,?,?,?)", rows)
print("sqlite", sqlite3.sqlite_version, "| rows:", con.execute("SELECT COUNT(*) FROM employees").fetchone()[0])

SQL_ONE = """
SELECT emp_id, dept_id, salary,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
FROM employees
"""
SQL_SAME = """
SELECT emp_id,
       ROW_NUMBER() OVER w AS rn,
       RANK()       OVER w AS rk,
       SUM(salary)  OVER (PARTITION BY dept_id) AS dept_total
FROM employees
WINDOW w AS (PARTITION BY dept_id ORDER BY salary DESC, emp_id)
"""
SQL_DIFF = """
SELECT emp_id,
       ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn,
       ROW_NUMBER() OVER (ORDER BY salary, emp_id) AS overall_rn
FROM employees
"""

def plan(sql):
    return [r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql)]

def show(title, sql):
    p = plan(sql)
    print(f"\n{title}")
    for line in p:
        print("   ", line)
    n = sum("TEMP B-TREE" in line for line in p)
    print("    -> temp b-tree lines:", n)
    return n

n1 = show("1) one window, no index", SQL_ONE)
n2 = show("2) ROW_NUMBER and RANK share one named window; SUM uses PARTITION BY only", SQL_SAME)
n3 = show("3) two windows with different ORDER BY / PARTITION BY", SQL_DIFF)
con.execute("CREATE INDEX ix_dept_salary ON employees(dept_id, salary DESC, emp_id)")
n4 = show("4) one window again, after CREATE INDEX (dept_id, salary DESC, emp_id)", SQL_ONE)
n5 = show("5) different windows, with the index", SQL_DIFF)

# correctness: SQL ranking equals pandas
sql_res = pd.read_sql_query(SQL_ONE + " ORDER BY emp_id", con)
emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
# pd:main
ordered = emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
ordered["rn"] = ordered.groupby("dept_id").cumcount() + 1
pd_res = ordered.sort_values("emp_id").reset_index(drop=True)[["emp_id", "dept_id", "salary", "rn"]]
# pd:end
pd.testing.assert_frame_equal(sql_res, pd_res, check_dtype=False)
print("\nSQL ROW_NUMBER equals pandas sort + cumcount + 1 on all", len(sql_res), "rows (compared after sorting by emp_id)")
print("note: result rows come back in index/partition order, not emp_id order, unless you add ORDER BY")
print("first 3 rows of SQL_ONE, index in place, no outer ORDER BY:", con.execute(SQL_ONE + " LIMIT 3").fetchall())
```

**Output (my run):**
```text
sqlite 3.45.1 | rows: 3000

1) one window, no index
    CO-ROUTINE (subquery-2)
    SCAN employees
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-2)
    -> temp b-tree lines: 1

2) ROW_NUMBER and RANK share one named window; SUM uses PARTITION BY only
    CO-ROUTINE (subquery-2)
    CO-ROUTINE (subquery-3)
    CO-ROUTINE (subquery-4)
    SCAN employees
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-4)
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-3)
    SCAN (subquery-2)
    -> temp b-tree lines: 2

3) two windows with different ORDER BY / PARTITION BY
    CO-ROUTINE (subquery-2)
    CO-ROUTINE (subquery-3)
    SCAN employees
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-3)
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-2)
    -> temp b-tree lines: 2

4) one window again, after CREATE INDEX (dept_id, salary DESC, emp_id)
    CO-ROUTINE (subquery-2)
    SCAN employees USING COVERING INDEX ix_dept_salary
    SCAN (subquery-2)
    -> temp b-tree lines: 0

5) different windows, with the index
    CO-ROUTINE (subquery-2)
    CO-ROUTINE (subquery-3)
    SCAN employees USING COVERING INDEX ix_dept_salary
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-3)
    USE TEMP B-TREE FOR ORDER BY
    SCAN (subquery-2)
    -> temp b-tree lines: 2

SQL ROW_NUMBER equals pandas sort + cumcount + 1 on all 3000 rows (compared after sorting by emp_id)
note: result rows come back in index/partition order, not emp_id order, unless you add ORDER BY
first 3 rows of SQL_ONE, index in place, no outer ORDER BY: [(270, 0, 3490, 1), (1770, 0, 3490, 2), (540, 0, 3480, 3)]
```

**Edge cases:**
- Without an outer `ORDER BY`, the output order is whatever the window evaluation leaves (in the last line, rows come back by department and salary, not by `emp_id`). Never rely on it.
- An index only helps if its column order and directions match the window: `(dept_id, salary)` helps `PARTITION BY dept_id ORDER BY salary`, not `ORDER BY salary` alone. I only tested one index (salary DESC); I did not test whether an ASC index would also avoid the sort.
- Plan wording differs between SQLite versions and engines. These lines are from 3.45.1 only.
- A window with no PARTITION BY puts the whole table in one partition, so one big sort of everything.

**Then explain:**
- **Why a sort:** RANK needs to know who comes before whom within the partition; the cheapest way is to sort by partition key then order key and walk the rows once.
- **Several windows:** identical window definitions (a named window makes this visible and removes drift) can be computed in one pass over one sorted stream. Different definitions need different orderings, hence another sort. In my run SQLite gave two sorts when the second window had the same partition but no ORDER BY.
- **Index:** a covering index on (dept_id, salary) lets the engine skip the sort. It costs write time and space; that trade-off and reading plans on other engines are Part 11.
- **Other engines:** PostgreSQL and MySQL also sort or use an index for window ordering and show it in `EXPLAIN`, with different wording; I am stating this from general knowledge, not executed here.
- **Cheaper still:** filter rows before the window (`WHERE` runs first), and rank only the columns you need.

**Follow-ups:**
- *Does top-N per group need to sort everything?* A full sort of each partition is the simple plan; some engines have top-N optimisations (not executed here).
- *Is a window faster than a self-join?* Often, because it makes one pass instead of re-reading, but measure on your engine; I did not benchmark.
- *What would you check first on a slow window query?* The plan for a sort that spills to disk, then whether an index matching PARTITION BY + ORDER BY exists.

**Common mistakes:**
- Saying "window functions are slow" without naming the sort.
- Adding an index with the columns in the wrong order and expecting the sort to vanish.
- Declaring several slightly different windows and paying for several sorts.
- Quoting plan text from one engine as if it were universal.

### Q41 ⭐ 🟡 PERCENTILE_CONT and percentiles via windows, hedged: salaries per department. Compute the 90th percentile salary per department in SQLite using the nearest-rank method with ROW_NUMBER / COUNT / CEIL-style arithmetic (or CUME_DIST >= 0.9 and MIN), show PERCENTILE_CONT and PERCENTILE_DISC as PostgreSQL, Snowflake and Oracle dialect text (hedged, not executed), and explain the difference between nearest-rank, interpolated, and pandas quantile(0.9) (linear interpolation by default). Run pandas and compare numbers, saying exactly where they differ.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** SQLite has no PERCENTILE_CONT, so the 90th percentile is built from ROW_NUMBER and COUNT (nearest-rank: the value at rank ceil(0.9 n)), or CUME_DIST >= 0.9 with MIN, or an interpolation between two neighbouring ranks; pandas `quantile(0.9)` is the interpolated one, so it gives different numbers from nearest-rank except when the position lands exactly on a row.

**Schema and sample data:** five departments chosen to expose the differences: dept 10 has ten salaries 10..100, dept 20 has four (100..400), dept 30 has one, dept 40 has seven with ties (10, 20 x5, 90), and dept 50 has one real salary (70) and two NULLs, which are filtered first.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,10,10),(2,10,20),(3,10,30),(4,10,40),(5,10,50),(6,10,60),(7,10,70),(8,10,80),(9,10,90),(10,10,100),
 (11,20,100),(12,20,200),(13,20,300),(14,20,400),
 (15,30,500),
 (16,40,10),(17,40,20),(18,40,20),(19,40,20),(20,40,20),(21,40,20),(22,40,90),
 (23,50,NULL),(24,50,70),(25,50,NULL);
```

**SQL answer:** nearest-rank with ROW_NUMBER (`SQL_NEAREST`; `ceil(9n/10)` written as `(9n + 9) / 10` in integer arithmetic so no CEIL function or float rounding is needed), the CUME_DIST form (`SQL_CUME`) and the interpolated form (`SQL_INTERP`).
```sql
WITH r AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id) AS n
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT dept_id, salary AS p90_nearest
FROM r
WHERE rn = (9 * n + 9) / 10
ORDER BY dept_id
```
```sql
WITH c AS (
  SELECT dept_id, salary,
         CUME_DIST() OVER (PARTITION BY dept_id ORDER BY salary) AS cd
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT dept_id, MIN(salary) AS p90_nearest
FROM c
WHERE cd >= 0.9
GROUP BY dept_id
ORDER BY dept_id
```
```sql
WITH r AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id) AS n
  FROM employees
  WHERE salary IS NOT NULL
), p AS (
  SELECT dept_id, n,
         1 + (9 * (n - 1)) / 10          AS lo,
         (9 * (n - 1)) % 10 / 10.0       AS frac
  FROM r GROUP BY dept_id
)
SELECT p.dept_id,
       MAX(CASE WHEN r.rn = p.lo     THEN r.salary END) +
       p.frac * (COALESCE(MAX(CASE WHEN r.rn = p.lo + 1 THEN r.salary END),
                          MAX(CASE WHEN r.rn = p.lo     THEN r.salary END))
                 - MAX(CASE WHEN r.rn = p.lo THEN r.salary END)) AS p90_interp
FROM p JOIN r ON r.dept_id = p.dept_id
GROUP BY p.dept_id
ORDER BY p.dept_id
```
Dialect text, not executed here: PostgreSQL, Snowflake and Oracle have `PERCENTILE_CONT(0.9) WITHIN GROUP (ORDER BY salary)` (interpolated) and `PERCENTILE_DISC(0.9) WITHIN GROUP (ORDER BY salary)` (the nearest-rank style value that actually exists in the data). Used per department with `GROUP BY dept_id`. SQL Server and BigQuery have analytic-function forms of PERCENTILE_CONT with an OVER clause; MySQL has no built-in. I am stating this from memory.

**pandas answer:** default `quantile` is linear interpolation. For nearest-rank I use numpy's `inverted_cdf` method (pandas `Series.quantile` does not take that method).
```python
clean = emp.dropna(subset=["salary"])
pd_linear = clean.groupby("dept_id")["salary"].quantile(0.9)                # default interpolation='linear'
pd_nearest = clean.groupby("dept_id")["salary"].apply(
    lambda s: np.quantile(s, 0.9, method="inverted_cdf"))                   # nearest-rank (numpy method name)
pd_higher = clean.groupby("dept_id")["salary"].quantile(0.9, interpolation="higher")
```

**Example:** dept 10 (n = 10, values 10..100).
- Nearest rank: ceil(0.9 x 10) = 9, the 9th smallest is 90. Check with CUME_DIST: the value 90 has 9 of 10 rows at or below it, 0.9, the first value reaching 0.9.
- Interpolated: position 1 + 0.9 x 9 = 9.1, so 90 + 0.1 x (100 - 90) = 91. pandas gives 91.0 too.
- Dept 20 (n = 4): nearest rank ceil(3.6) = 4, value 400; interpolated position 1 + 0.9 x 3 = 3.7, so 300 + 0.7 x 100 = 370.
- Dept 40 (n = 7, ties): nearest rank ceil(6.3) = 7, value 90; interpolated position 6.4, so 20 + 0.4 x 70 = 48 (a value that is not in the data).
- Dept 30 and 50 have one usable value, so every method returns it.

**Code:** run with `python3 -I`.
```python
# Q41: 90th percentile per department: nearest-rank, interpolated (PERCENTILE_CONT style), pandas
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,10,10),(2,10,20),(3,10,30),(4,10,40),(5,10,50),(6,10,60),(7,10,70),(8,10,80),(9,10,90),(10,10,100),
 (11,20,100),(12,20,200),(13,20,300),(14,20,400),
 (15,30,500),
 (16,40,10),(17,40,20),(18,40,20),(19,40,20),(20,40,20),(21,40,20),(22,40,90),
 (23,50,NULL),(24,50,70),(25,50,NULL);
"""
# nearest rank: value at rank k = ceil(0.9 * n) in ascending order; ceil(9n/10) = (9n + 9) / 10 in integer arithmetic
SQL_NEAREST = """
WITH r AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id) AS n
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT dept_id, salary AS p90_nearest
FROM r
WHERE rn = (9 * n + 9) / 10
ORDER BY dept_id
"""
SQL_CUME = """
WITH c AS (
  SELECT dept_id, salary,
         CUME_DIST() OVER (PARTITION BY dept_id ORDER BY salary) AS cd
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT dept_id, MIN(salary) AS p90_nearest
FROM c
WHERE cd >= 0.9
GROUP BY dept_id
ORDER BY dept_id
"""
# interpolated (what PERCENTILE_CONT(0.9) does): position 1 + 0.9 * (n - 1), blend the two neighbours
SQL_INTERP = """
WITH r AS (
  SELECT dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary, emp_id) AS rn,
         COUNT(*)     OVER (PARTITION BY dept_id) AS n
  FROM employees
  WHERE salary IS NOT NULL
), p AS (
  SELECT dept_id, n,
         1 + (9 * (n - 1)) / 10          AS lo,
         (9 * (n - 1)) % 10 / 10.0       AS frac
  FROM r GROUP BY dept_id
)
SELECT p.dept_id,
       MAX(CASE WHEN r.rn = p.lo     THEN r.salary END) +
       p.frac * (COALESCE(MAX(CASE WHEN r.rn = p.lo + 1 THEN r.salary END),
                          MAX(CASE WHEN r.rn = p.lo     THEN r.salary END))
                 - MAX(CASE WHEN r.rn = p.lo THEN r.salary END)) AS p90_interp
FROM p JOIN r ON r.dept_id = p.dept_id
GROUP BY p.dept_id
ORDER BY p.dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
nearest = pd.read_sql_query(SQL_NEAREST, con)
cume = pd.read_sql_query(SQL_CUME, con)
interp = pd.read_sql_query(SQL_INTERP, con)
assert nearest.equals(cume), "ROW_NUMBER nearest-rank and CUME_DIST >= 0.9 should agree"

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
clean = emp.dropna(subset=["salary"])
pd_linear = clean.groupby("dept_id")["salary"].quantile(0.9)                # default interpolation='linear'
pd_nearest = clean.groupby("dept_id")["salary"].apply(
    lambda s: np.quantile(s, 0.9, method="inverted_cdf"))                   # nearest-rank (numpy method name)
pd_higher = clean.groupby("dept_id")["salary"].quantile(0.9, interpolation="higher")
# pd:end
cmp = pd.DataFrame({"n": clean.groupby("dept_id").size(),
                    "sql_nearest": nearest.set_index("dept_id")["p90_nearest"],
                    "np_inverted_cdf": pd_nearest,
                    "pandas_higher": pd_higher,
                    "sql_interp": interp.set_index("dept_id")["p90_interp"],
                    "pandas_quantile": pd_linear})
print(cmp.to_string())
assert np.allclose(cmp["sql_nearest"], cmp["np_inverted_cdf"])
assert np.allclose(cmp["sql_interp"], cmp["pandas_quantile"])
diff = cmp.index[cmp["sql_nearest"] != cmp["pandas_quantile"]].tolist()
print("\ndepartments where nearest-rank != pandas default quantile:", diff)
print("departments where pandas 'higher' != nearest-rank:", cmp.index[cmp["sql_nearest"] != cmp["pandas_higher"]].tolist())
print("dept 50 has", int(emp[emp.dept_id == 50]["salary"].isna().sum()), "NULL salaries filtered first; n counts only the non-NULL one")
print("asserts passed: ROW_NUMBER == CUME_DIST (nearest-rank); SQL interpolation == pandas quantile; numpy inverted_cdf == nearest-rank")
```

**Output (my run):**
```text
          n  sql_nearest  np_inverted_cdf  pandas_higher  sql_interp  pandas_quantile
dept_id                                                                              
10       10           90             90.0          100.0        91.0             91.0
20        4          400            400.0          400.0       370.0            370.0
30        1          500            500.0          500.0       500.0            500.0
40        7           90             90.0           90.0        48.0             48.0
50        1           70             70.0           70.0        70.0             70.0

departments where nearest-rank != pandas default quantile: [10, 20, 40]
departments where pandas 'higher' != nearest-rank: [10]
dept 50 has 2 NULL salaries filtered first; n counts only the non-NULL one
asserts passed: ROW_NUMBER == CUME_DIST (nearest-rank); SQL interpolation == pandas quantile; numpy inverted_cdf == nearest-rank
```

**Edge cases:**
- Where they differ: nearest-rank and pandas default quantile differ in departments 10, 20 and 40 and agree in 30 and 50 (see output). They agree only when the interpolation position is a whole number or n = 1.
- pandas `interpolation='higher'` is not nearest-rank either: it differs in dept 10 (100.0 versus 90) because it rounds the interpolation position up, not the rank 0.9 n.
- NULLs: filtered first with `WHERE salary IS NOT NULL`, otherwise they would count in `n` and take ranks. Dept 50's n is 1.
- Ties: nearest-rank is well defined with ties (the value at that rank); the row chosen does not matter because the values are equal. I added emp_id to the ROW_NUMBER order only so the numbering is repeatable.
- Floating point: the nearest-rank row uses integers; `CUME_DIST >= 0.9` compares floats, which matched here (9/10 equals the literal 0.9), but I would prefer the integer form in production.

**Then explain:**
- **Nearest-rank:** sort, take the value at rank ceil(p n). Always returns a value that exists in the data. It is what PERCENTILE_DISC is meant to do (from documentation memory, not executed).
- **Interpolated (continuous):** treat the sorted values as points on a line and read the p position, which can fall between two values. SQL PERCENTILE_CONT and pandas default `quantile` agree on this definition; my SQL emulation matched pandas exactly in the assert.
- **Small groups:** the two definitions disagree most when n is small, which is exactly the per-group case.
- **Say which one you used.** A "p90" without a definition is ambiguous.

**Follow-ups:**
- *Median this way?* p = 0.5; see Q38.
- *Which should a dashboard use?* Whichever matches the other tools it is compared against; for small groups document it.
- *Can CUME_DIST replace the ROW_NUMBER form?* Yes for nearest-rank, as asserted, with the float caveat.

**Common mistakes:**
- Taking the top 10 percent of the whole table with one LIMIT instead of computing the percentile per department.
- Not filtering NULLs before computing `n`.
- Comparing SQL nearest-rank with pandas default quantile and calling the difference a bug.
- Using `ntile(10) = 10` as the 90th percentile (bucket sizes are positional).

### Q42 ⭐ 🟡 PERCENT_RANK, CUME_DIST and pandas rank(pct=True) are not the same thing: scores with ties on a small table. Compute SQL RANK, PERCENT_RANK ((rank-1)/(n-1)), CUME_DIST (rank of last peer / n) and pandas rank(pct=True) with method='average', 'min' and 'max', then show which pandas call equals CUME_DIST (method='max', pct=True) and how to get PERCENT_RANK ((rank(method='min') - 1) / (n - 1)). Run all in one script and assert the matches.
**Asked at:** pandas reference and user guide (DataFrame.rank, qcut; groupby, Comparison with SQL), not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** They are three different definitions: PERCENT_RANK is (rank - 1) / (n - 1) and starts at 0, CUME_DIST is (rows up to the last tied row) / n and ends at 1, and pandas `rank(pct=True)` is rank / n, which equals CUME_DIST only with `method='max'` and is not PERCENT_RANK at all.

**Schema and sample data:** seven scores with a tie of two (85) and a tie of three (70), plus a one-row table for the edge case.
```sql
CREATE TABLE scores(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,90),(2,85),(3,85),(4,70),(5,70),(6,70),(7,60);
CREATE TABLE solo(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO solo VALUES (1,75);
```

**SQL answer:** `SQL_MAIN` shows RANK, PERCENT_RANK and CUME_DIST with scores descending; `SQL_SOLO` is the one-row case.
```sql
SELECT student_id, score,
       RANK()         OVER (ORDER BY score DESC) AS rnk,
       PERCENT_RANK() OVER (ORDER BY score DESC) AS pct_rank,
       CUME_DIST()    OVER (ORDER BY score DESC) AS cume_dist
FROM scores
ORDER BY student_id
```
```sql
SELECT student_id, PERCENT_RANK() OVER (ORDER BY score) AS pr, CUME_DIST() OVER (ORDER BY score) AS cd FROM solo
```

**pandas answer:** pct with the three tie methods, and the PERCENT_RANK formula built from `method='min'`.
```python
r_avg = sc["score"].rank(pct=True, ascending=False)                    # method='average' (default)
r_min = sc["score"].rank(pct=True, ascending=False, method="min")
r_max = sc["score"].rank(pct=True, ascending=False, method="max")
rank_min = sc["score"].rank(ascending=False, method="min")
pd_percent_rank = (rank_min - 1) / (n - 1)
```

**Example:** n = 7, scores descending.
- 90: RANK 1; PERCENT_RANK (1 - 1) / 6 = 0; CUME_DIST 1 / 7 = 0.1429.
- Two 85s: RANK 2 for both; PERCENT_RANK (2 - 1) / 6 = 0.1667; CUME_DIST uses the last tied row, row 3, so 3 / 7 = 0.4286.
- Three 70s: RANK 4; PERCENT_RANK 3 / 6 = 0.5; CUME_DIST 6 / 7 = 0.8571.
- 60: RANK 7; PERCENT_RANK 6 / 6 = 1; CUME_DIST 7 / 7 = 1.
- pandas pct for the two 85s: `method='min'` gives 2 / 7 = 0.2857, `'max'` gives 3 / 7 = 0.4286 (equal to CUME_DIST), and the default `'average'` gives rank 2.5 / 7 = 0.3571, which matches neither SQL function.

**Code:** run with `python3 -I`.
```python
# Q42: RANK, PERCENT_RANK, CUME_DIST versus pandas rank(pct=True)
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE scores(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO scores VALUES (1,90),(2,85),(3,85),(4,70),(5,70),(6,70),(7,60);
CREATE TABLE solo(student_id INTEGER PRIMARY KEY, score INTEGER);
INSERT INTO solo VALUES (1,75);
"""
SQL_MAIN = """
SELECT student_id, score,
       RANK()         OVER (ORDER BY score DESC) AS rnk,
       PERCENT_RANK() OVER (ORDER BY score DESC) AS pct_rank,
       CUME_DIST()    OVER (ORDER BY score DESC) AS cume_dist
FROM scores
ORDER BY student_id
"""
SQL_SOLO = """
SELECT student_id, PERCENT_RANK() OVER (ORDER BY score) AS pr, CUME_DIST() OVER (ORDER BY score) AS cd FROM solo
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql = pd.read_sql_query(SQL_MAIN, con)
solo = pd.read_sql_query(SQL_SOLO, con)

sc = pd.read_sql_query("SELECT * FROM scores ORDER BY student_id", con)
n = len(sc)
# pd:main
r_avg = sc["score"].rank(pct=True, ascending=False)                    # method='average' (default)
r_min = sc["score"].rank(pct=True, ascending=False, method="min")
r_max = sc["score"].rank(pct=True, ascending=False, method="max")
rank_min = sc["score"].rank(ascending=False, method="min")
pd_percent_rank = (rank_min - 1) / (n - 1)
# pd:end
out = sql.copy()
out["pd_avg"], out["pd_min"], out["pd_max"], out["pd_pr"] = r_avg.round(4), r_min.round(4), r_max.round(4), pd_percent_rank.round(4)
out["pct_rank"], out["cume_dist"] = out["pct_rank"].round(4), out["cume_dist"].round(4)
print(out.to_string(index=False))
assert np.allclose(sql["cume_dist"], r_max)
assert np.allclose(sql["pct_rank"], pd_percent_rank)
assert np.allclose(sql["rnk"] / n, r_min)           # pandas pct with method='min' is rank / n
assert not np.allclose(sql["cume_dist"], r_avg)
print("\nmatches: CUME_DIST == rank(pct=True, method='max'); PERCENT_RANK == (rank(method='min') - 1) / (n - 1); rank(pct=True, method='min') == RANK / n")
print("rank(pct=True) with the default 'average' matches neither:", r_avg.round(4).tolist())

print("\none-row table, SQL:", solo.to_dict("records"))
one = pd.Series([75])
with np.errstate(all="ignore"):
    print("one-row pandas (rank-1)/(n-1):", ((one.rank(method='min') - 1) / (len(one) - 1)).tolist(), "<- 0/0 is NaN; SQLite returns 0.0")
print("asserts passed")
```

**Output (my run):**
```text
 student_id  score  rnk  pct_rank  cume_dist  pd_avg  pd_min  pd_max  pd_pr
          1     90    1    0.0000     0.1429  0.1429  0.1429  0.1429 0.0000
          2     85    2    0.1667     0.4286  0.3571  0.2857  0.4286 0.1667
          3     85    2    0.1667     0.4286  0.3571  0.2857  0.4286 0.1667
          4     70    4    0.5000     0.8571  0.7143  0.5714  0.8571 0.5000
          5     70    4    0.5000     0.8571  0.7143  0.5714  0.8571 0.5000
          6     70    4    0.5000     0.8571  0.7143  0.5714  0.8571 0.5000
          7     60    7    1.0000     1.0000  1.0000  1.0000  1.0000 1.0000

matches: CUME_DIST == rank(pct=True, method='max'); PERCENT_RANK == (rank(method='min') - 1) / (n - 1); rank(pct=True, method='min') == RANK / n
rank(pct=True) with the default 'average' matches neither: [0.1429, 0.3571, 0.3571, 0.7143, 0.7143, 0.7143, 1.0]

one-row table, SQL: [{'student_id': 1, 'pr': 0.0, 'cd': 1.0}]
one-row pandas (rank-1)/(n-1): [nan] <- 0/0 is NaN; SQLite returns 0.0
asserts passed
```

**Edge cases:**
- One-row partition: PERCENT_RANK is 0.0 and CUME_DIST is 1.0 in SQLite (output). The pandas formula (rank - 1) / (n - 1) is 0 / 0 = NaN, so you must handle it (for example `fillna(0)`) to match SQL.
- Ties: PERCENT_RANK ties share one value (all based on the min rank), CUME_DIST ties share one value (based on the max position).
- Direction: I ranked with `ascending=False` in pandas and `ORDER BY score DESC` in SQL, so rank 1 is the top score. Flip both together; the formulas then describe the share of rows below or above you in the other direction.
- NULL scores: not in this table; they would take a rank in SQL (see Q29) and stay NaN in pandas by default.

**Then explain:**
- **Words:** PERCENT_RANK is "the fraction of the other rows that come strictly before this row's tie group". CUME_DIST is "the fraction of all rows at or before this row's tie group".
- **Why CUME_DIST >= 0.9 selects at least 10 percent:** a row's value includes its ties and itself.
- **pandas:** `rank(pct=True, method='max')` is CUME_DIST; `rank(method='min')` minus 1 over n minus 1 is PERCENT_RANK. Asserted in the Code block.
- **Default average:** the default `method='average'` is neither; it is often what people use by accident.

**Follow-ups:**
- *Which gives 0 for the lowest row?* PERCENT_RANK; CUME_DIST's lowest row is 1/n at least.
- *Which one for "top 10 percent"?* CUME_DIST on the descending order or >= 0.9 on ascending, see Q36 and Q47.
- *Do they ever agree?* On the last row both are 1.0 in the output; elsewhere they differ on this data.

**Common mistakes:**
- Assuming `rank(pct=True)` is PERCENT_RANK.
- Forgetting the one-row division by zero in pandas.
- Mixing `method='average'` pct with a SQL threshold and getting a different set of rows.
- Dividing RANK by COUNT yourself and calling it CUME_DIST (it is the min-method pct, not the max).

### Q43 ⭐ 🟡 Windows, DISTINCT and ORDER BY interplay: employees(emp_id, name, dept_id, salary). Show that SELECT DISTINCT dept_id, ROW_NUMBER() OVER (...) does not deduplicate as expected because the window runs before DISTINCT, that window functions may appear only in the SELECT list and ORDER BY, and how to rank departments by average salary in one query (ORDER BY RANK() OVER (...) in the outer query or via a CTE). Run it on SQLite and explain the evaluation order again in one line.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Window functions are computed after FROM, WHERE, GROUP BY and HAVING and before DISTINCT, ORDER BY and LIMIT, so `SELECT DISTINCT dept_id, ROW_NUMBER() OVER (...)` numbers every row first and DISTINCT then finds nothing to remove; windows are allowed only in the SELECT list and ORDER BY.

**Schema and sample data:** six employees in three departments (10: Asha 50, Ben 70, Chitra 60; 20: Dev 90, Esha 40; 30: Farid 55).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Farid',30,55);
```

**SQL answer:** the DISTINCT trap (`SQL_DISTINCT_BAD`), the case where DISTINCT does work because the window value repeats (`SQL_DISTINCT_OK`), and three ways to rank departments by average salary: window over an aggregate (`SQL_ONE_QUERY`), window in ORDER BY (`SQL_ORDER_BY_WINDOW`), and a CTE (`SQL_CTE`).
```sql
SELECT DISTINCT dept_id, ROW_NUMBER() OVER (ORDER BY dept_id) AS rn
FROM employees
ORDER BY rn
```
```sql
SELECT DISTINCT dept_id, DENSE_RANK() OVER (ORDER BY dept_id) AS drk
FROM employees
ORDER BY dept_id
```
```sql
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary,
       RANK() OVER (ORDER BY AVG(salary) DESC) AS rnk
FROM employees
GROUP BY dept_id
ORDER BY rnk, dept_id
```
```sql
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY dept_id
ORDER BY RANK() OVER (ORDER BY AVG(salary) DESC), dept_id
```
```sql
WITH d AS (SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id)
SELECT dept_id, ROUND(avg_salary, 2) AS avg_salary, RANK() OVER (ORDER BY avg_salary DESC) AS rnk
FROM d
ORDER BY rnk, dept_id
```

**pandas answer:** `groupby().mean()` then `rank`, with no ordering of evaluation to worry about because each step is a separate statement.
```python
g = emp.groupby("dept_id", as_index=False)["salary"].mean().rename(columns={"salary": "avg_salary"})
g["rnk"] = g["avg_salary"].rank(method="min", ascending=False).astype(int)
pd_df = g.sort_values(["rnk", "dept_id"]).reset_index(drop=True)
pd_df["avg_salary"] = pd_df["avg_salary"].round(2)
```

**Example:**
- `ROW_NUMBER() OVER (ORDER BY dept_id)` gives 1 to 6 on the six employee rows. Each (dept_id, rn) pair is unique, so DISTINCT removes nothing and returns six rows, not three.
- `DENSE_RANK() OVER (ORDER BY dept_id)` gives 1, 1, 1, 2, 2, 3. Within a department the pair is identical, so DISTINCT collapses to three rows. DISTINCT is not broken; it ran after the window.
- Department averages: 10 is 60, 20 is 65, 30 is 55. Ranked by average descending: 20, 10, 30.

**Code:** run with `python3 -I`.
```python
# Q43: windows, DISTINCT and ORDER BY interplay
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,50),(2,'Ben',10,70),(3,'Chitra',10,60),
  (4,'Dev',20,90),(5,'Esha',20,40),(6,'Farid',30,55);
"""
SQL_DISTINCT_BAD = """
SELECT DISTINCT dept_id, ROW_NUMBER() OVER (ORDER BY dept_id) AS rn
FROM employees
ORDER BY rn
"""
SQL_DISTINCT_OK = """
SELECT DISTINCT dept_id, DENSE_RANK() OVER (ORDER BY dept_id) AS drk
FROM employees
ORDER BY dept_id
"""
SQL_ONE_QUERY = """
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary,
       RANK() OVER (ORDER BY AVG(salary) DESC) AS rnk
FROM employees
GROUP BY dept_id
ORDER BY rnk, dept_id
"""
SQL_ORDER_BY_WINDOW = """
SELECT dept_id, ROUND(AVG(salary), 2) AS avg_salary
FROM employees
GROUP BY dept_id
ORDER BY RANK() OVER (ORDER BY AVG(salary) DESC), dept_id
"""
SQL_CTE = """
WITH d AS (SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id)
SELECT dept_id, ROUND(avg_salary, 2) AS avg_salary, RANK() OVER (ORDER BY avg_salary DESC) AS rnk
FROM d
ORDER BY rnk, dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)

bad = q(SQL_DISTINCT_BAD)
print("SELECT DISTINCT dept_id, ROW_NUMBER() ... returns", len(bad), "rows (6 employees, 3 departments):")
print(bad.to_string(index=False))
assert len(bad) == 6
ok = q(SQL_DISTINCT_OK)
print("\nwith DENSE_RANK over dept_id the window value is the same inside a department, so DISTINCT collapses:")
print(ok.to_string(index=False))
assert len(ok) == 3

for label, sql in [("window in WHERE", "SELECT * FROM employees WHERE ROW_NUMBER() OVER (ORDER BY salary) = 1"),
                   ("window in GROUP BY", "SELECT 1 FROM employees GROUP BY ROW_NUMBER() OVER (ORDER BY salary)"),
                   ("window inside an aggregate", "SELECT SUM(ROW_NUMBER() OVER (ORDER BY salary)) FROM employees")]:
    try:
        con.execute(sql).fetchall(); print(label, "-> ran")
    except sqlite3.Error as e:
        print(f"\n{label} -> {type(e).__name__}: {e}")

one = q(SQL_ONE_QUERY); ob = q(SQL_ORDER_BY_WINDOW); cte = q(SQL_CTE)
print("\ndepartments ranked by average salary, one query:"); print(one.to_string(index=False))
assert one[["dept_id", "avg_salary"]].equals(ob) and one.equals(cte)

emp = q("SELECT * FROM employees")
# pd:main
g = emp.groupby("dept_id", as_index=False)["salary"].mean().rename(columns={"salary": "avg_salary"})
g["rnk"] = g["avg_salary"].rank(method="min", ascending=False).astype(int)
pd_df = g.sort_values(["rnk", "dept_id"]).reset_index(drop=True)
pd_df["avg_salary"] = pd_df["avg_salary"].round(2)
# pd:end
pd.testing.assert_frame_equal(one, pd_df, check_dtype=False)
print("\nasserts passed: three SQL forms equal each other and pandas groupby mean + rank(method='min')")
```

**Output (my run):**
```text
SELECT DISTINCT dept_id, ROW_NUMBER() ... returns 6 rows (6 employees, 3 departments):
 dept_id  rn
      10   1
      10   2
      10   3
      20   4
      20   5
      30   6

with DENSE_RANK over dept_id the window value is the same inside a department, so DISTINCT collapses:
 dept_id  drk
      10    1
      20    2
      30    3

window in WHERE -> OperationalError: misuse of window function ROW_NUMBER()

window in GROUP BY -> OperationalError: misuse of window function ROW_NUMBER()

window inside an aggregate -> OperationalError: misuse of window function ROW_NUMBER()

departments ranked by average salary, one query:
 dept_id  avg_salary  rnk
      20        65.0    1
      10        60.0    2
      30        55.0    3

asserts passed: three SQL forms equal each other and pandas groupby mean + rank(method='min')
```

**Edge cases:**
- SQLite rejected a window function in WHERE, in GROUP BY and inside an aggregate with the same message (`misuse of window function ROW_NUMBER()`); see the output. The wording is SQLite's, other engines word it differently (not executed).
- `RANK() OVER (ORDER BY AVG(salary) DESC)` works because the window runs after GROUP BY and sees one row per department with the aggregate already computed. The window cannot be placed inside an aggregate, but an aggregate can be inside a window's ORDER BY.
- Ties in the average would share a rank (RANK), and I added `dept_id` to the outer ORDER BY so the printed order is repeatable.
- Departments with all-NULL salaries have a NULL average; they would sort as NULL (smallest in SQLite).

**Then explain:**
- **Order of evaluation in one line:** FROM, WHERE, GROUP BY, HAVING, window functions, SELECT list, DISTINCT, ORDER BY, LIMIT.
- **Where windows may appear:** SELECT list and ORDER BY only (the SQLite documentation page and the PostgreSQL tutorial both say this).
- **To deduplicate on a window result:** put the window in a CTE or subquery and filter or DISTINCT outside.
- **Ranking departments by average:** all three forms gave the same rows in my run; the CTE reads best.
- **pandas parallel:** `drop_duplicates` after adding a row number would also keep every row, for the same reason.

**Follow-ups:**
- *Can I `ORDER BY` a window function?* Yes, as in `SQL_ORDER_BY_WINDOW`; the window is computed, then the result is sorted by it.
- *Why not `WHERE rn = 1` directly?* The window does not exist yet at WHERE time; use a CTE (Q3).
- *What is the cleanest way to get one row per department?* GROUP BY if you only need aggregates, ROW_NUMBER = 1 in a CTE if you need a whole row.

**Common mistakes:**
- Using DISTINCT to remove duplicates created by a row number.
- Writing `AVG(RANK() OVER ...)` and expecting it to work.
- Trusting the display order after a window query with no outer ORDER BY.
- Assuming DISTINCT runs before the window.

### Q44 ⭐ 🔴 Dedup with several tie-break criteria: product_prices(row_id, product_id, price, source, updated_at) where several rows per product share the latest updated_at, and a source priority applies ('manual' beats 'feed' beats 'scrape'). Keep one row per product: latest updated_at, then highest source priority (CASE expression in ORDER BY), then highest row_id. Show ROW_NUMBER with a CASE in the ORDER BY, and the pandas version using a priority map and sort_values with keep='first'. Explain how to prove the result is unique per product.
**Asked at:** datadriven.io window-function practice problems and cheat sheet (dedup latest per key, top-N with ties, LAST_VALUE frame trap, share of partition; labels from the platform), not candidate reports; analyst and data scientist screens
**Say this first (1 line):** Keep one row per product with `ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY updated_at DESC, <CASE priority> DESC, row_id DESC) = 1`; the CASE turns the text source into a rank (manual 3, feed 2, scrape 1, anything else 0) and the unique `row_id` last makes the choice repeatable, and in pandas the same keys go into `sort_values` before `drop_duplicates(keep='first')`.

**Schema and sample data:** nine price rows for four products. Product 100 has three rows on the latest date with different sources (scrape, manual, feed); product 200 has two 'feed' rows on the same date (only `row_id` separates them); product 300 has 'import' (an unknown source) and 'scrape' on the same date; product 400 has a NULL source.
```sql
CREATE TABLE product_prices(row_id INTEGER PRIMARY KEY, product_id INTEGER, price INTEGER, source TEXT, updated_at TEXT);
INSERT INTO product_prices VALUES
 (1,100,50,'feed',  '2026-03-01'),
 (2,100,52,'scrape','2026-03-02'),
 (3,100,51,'manual','2026-03-02'),
 (4,100,53,'feed',  '2026-03-02'),
 (5,200,70,'feed',  '2026-03-05'),
 (6,200,71,'feed',  '2026-03-05'),
 (7,300,10,'import','2026-03-01'),
 (8,300,11,'scrape','2026-03-01'),
 (9,400,99,NULL,    '2026-03-04');
```

**SQL answer:** `SQL_MAIN` is the answer; `SQL_WRONG_ALPHA` shows the mistake of sorting the source text itself.
```sql
WITH r AS (
  SELECT row_id, product_id, price, source, updated_at,
         ROW_NUMBER() OVER (
           PARTITION BY product_id
           ORDER BY updated_at DESC,
                    CASE source WHEN 'manual' THEN 3 WHEN 'feed' THEN 2 WHEN 'scrape' THEN 1 ELSE 0 END DESC,
                    row_id DESC
         ) AS rn
  FROM product_prices
)
SELECT row_id, product_id, price, source, updated_at
FROM r
WHERE rn = 1
ORDER BY product_id
```
```sql
WITH r AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY updated_at DESC, source DESC, row_id DESC) AS rn
  FROM product_prices
)
SELECT row_id, product_id, source FROM r WHERE rn = 1 ORDER BY product_id
```

**pandas answer:** map the source to a number (unknown or NULL gets 0), sort so the best row is first within each product, keep the first row.
```python
prio = {"manual": 3, "feed": 2, "scrape": 1}
pp["prio"] = pp["source"].map(prio).fillna(0)          # unknown or NULL source ranks lowest
pd_df = (pp.sort_values(["product_id", "updated_at", "prio", "row_id"], ascending=[True, False, False, False])
           .drop_duplicates("product_id", keep="first")
           .drop(columns="prio")
           .reset_index(drop=True))
```

**Example:**
- Product 100: latest date is 2026-03-02 (rows 2, 3, 4). Priorities: scrape 1, manual 3, feed 2, so row 3 (manual, price 51) wins.
- Product 200: both rows share date and priority; the highest `row_id` wins, row 6 (price 71).
- Product 300: same date; 'scrape' has priority 1 and 'import' is unknown (0), so row 8 wins.
- Product 400: one row, kept even though its source is NULL.
- Wrong alphabetical sort: `source DESC` puts 'scrape' above 'manual' and 'feed', so product 100 would keep row 2 (scrape). Alphabet is not the business priority.

**Code:** run with `python3 -I`.
```python
# Q44: dedup with several tie-break criteria (CASE priority)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE product_prices(row_id INTEGER PRIMARY KEY, product_id INTEGER, price INTEGER, source TEXT, updated_at TEXT);
INSERT INTO product_prices VALUES
 (1,100,50,'feed',  '2026-03-01'),
 (2,100,52,'scrape','2026-03-02'),
 (3,100,51,'manual','2026-03-02'),
 (4,100,53,'feed',  '2026-03-02'),
 (5,200,70,'feed',  '2026-03-05'),
 (6,200,71,'feed',  '2026-03-05'),
 (7,300,10,'import','2026-03-01'),
 (8,300,11,'scrape','2026-03-01'),
 (9,400,99,NULL,    '2026-03-04');
"""
SQL_MAIN = """
WITH r AS (
  SELECT row_id, product_id, price, source, updated_at,
         ROW_NUMBER() OVER (
           PARTITION BY product_id
           ORDER BY updated_at DESC,
                    CASE source WHEN 'manual' THEN 3 WHEN 'feed' THEN 2 WHEN 'scrape' THEN 1 ELSE 0 END DESC,
                    row_id DESC
         ) AS rn
  FROM product_prices
)
SELECT row_id, product_id, price, source, updated_at
FROM r
WHERE rn = 1
ORDER BY product_id
"""
SQL_WRONG_ALPHA = """
WITH r AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY updated_at DESC, source DESC, row_id DESC) AS rn
  FROM product_prices
)
SELECT row_id, product_id, source FROM r WHERE rn = 1 ORDER BY product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql = pd.read_sql_query(SQL_MAIN, con)
print("kept rows:"); print(sql.to_string(index=False, na_rep="NULL"))

# proof of uniqueness: one row per product, and the sort key (product, updated_at, priority, row_id) has no duplicates
assert sql["product_id"].is_unique
dups = con.execute("""
SELECT COUNT(*) FROM (
  SELECT product_id, updated_at,
         CASE source WHEN 'manual' THEN 3 WHEN 'feed' THEN 2 WHEN 'scrape' THEN 1 ELSE 0 END AS prio, row_id
  FROM product_prices GROUP BY 1, 2, 3, 4 HAVING COUNT(*) > 1)""").fetchone()[0]
print("\nduplicate full sort keys (must be 0 for a repeatable pick):", dups)
assert dups == 0
print("rows kept vs distinct products:", len(sql), "vs", con.execute("SELECT COUNT(DISTINCT product_id) FROM product_prices").fetchone()[0])
print("\nalphabetical source DESC instead of the CASE (wrong):")
print(pd.read_sql_query(SQL_WRONG_ALPHA, con).to_string(index=False, na_rep="NULL"))

pp = pd.read_sql_query("SELECT * FROM product_prices", con)
# pd:main
prio = {"manual": 3, "feed": 2, "scrape": 1}
pp["prio"] = pp["source"].map(prio).fillna(0)          # unknown or NULL source ranks lowest
pd_df = (pp.sort_values(["product_id", "updated_at", "prio", "row_id"], ascending=[True, False, False, False])
           .drop_duplicates("product_id", keep="first")
           .drop(columns="prio")
           .reset_index(drop=True))
# pd:end
pd.testing.assert_frame_equal(sql, pd_df, check_dtype=False)
assert not pp.duplicated(["product_id", "updated_at", "prio", "row_id"]).any()
print("\nasserts passed: SQL ROW_NUMBER with CASE == pandas map + sort_values + drop_duplicates (rows compared in product_id order)")
```

**Output (my run):**
```text
kept rows:
 row_id  product_id  price source updated_at
      3         100     51 manual 2026-03-02
      6         200     71   feed 2026-03-05
      8         300     11 scrape 2026-03-01
      9         400     99   NULL 2026-03-04

duplicate full sort keys (must be 0 for a repeatable pick): 0
rows kept vs distinct products: 4 vs 4

alphabetical source DESC instead of the CASE (wrong):
 row_id  product_id source
      2         100 scrape
      6         200   feed
      8         300 scrape
      9         400   NULL

asserts passed: SQL ROW_NUMBER with CASE == pandas map + sort_values + drop_duplicates (rows compared in product_id order)
```

**Edge cases:**
- Unknown or NULL source: the CASE `ELSE 0` handles both (NULL matches no WHEN). Without an ELSE the CASE returns NULL, and with DESC order NULL sorts last in SQLite anyway, but write the ELSE so the rule is explicit.
- A source spelled differently ('Manual', ' manual') hits the ELSE and loses silently; normalise first if the data is messy.
- Same `updated_at` as text: ISO dates sort correctly as text; other formats do not.
- How to prove uniqueness: (1) the result has exactly as many rows as distinct products (checked in the Code block, 4 and 4); (2) the full sort key (product_id, updated_at, priority, row_id) has no duplicates, which is guaranteed because `row_id` is a primary key and checked by a GROUP BY ... HAVING COUNT(*) > 1 query returning 0.

**Then explain:**
- **Order of keys is the business rule:** newest first, then source trust, then newest row id. A tie-break column that is not unique is not a tie-break.
- **Why a CASE:** the ORDER BY needs a sortable rank; the alphabet is wrong here, as the run shows.
- **pandas:** a dictionary plus `map` is the CASE; `fillna(0)` is the ELSE. With one `ascending` list the directions can differ per key.
- **Stability:** I do not rely on the sort being stable, because every key combination is unique.

**Follow-ups:**
- *Priority stored in a lookup table?* Join to it (LEFT JOIN with COALESCE to 0) and order by that column.
- *Should the priority beat the date?* Then swap the order of the first two keys. State the rule to the stakeholder.
- *What if `row_id` is not available?* Then there is no repeatable answer for full ties; add a column or accept an arbitrary pick and say so.

**Common mistakes:**
- Sorting the text of `source`.
- Forgetting ELSE, so unknown sources get NULL and sort unpredictably across engines (NULL ordering differs by engine, see Q29).
- Putting the priority before the date when the rule says the date comes first.
- Relying on `drop_duplicates` after an unsorted frame.

### Q45 ⭐ 🔴 Top-N per group with explicit tie rules: employees(emp_id, name, dept_id, salary, hire_date). Return the top 2 per department by salary, with ties on salary broken by earlier hire_date, then lower emp_id, and also the variant 'top 2 salary levels with all tied employees' (DENSE_RANK). Show both, state what happens in a department with only one employee, and give the pandas versions. Discuss how you would explain the rule you chose to a stakeholder.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** "Top 2 per department" has two defensible meanings: exactly two people (ROW_NUMBER with a full tie-break: salary DESC, hire_date, emp_id) or the top two salary levels with everyone tied (DENSE_RANK <= 2); a department with one employee returns one row in both.

**Schema and sample data:** nine employees. Dept 10: Asha 90, then Ben, Chitra and Dev all at 80 (Ben hired 2019-05-01, Chitra and Dev both 2018-02-01), Esha 70. Dept 20: Farid and Gita both 60 hired on the same day, Hari 50. Dept 30: Ila alone. `salary` is declared NOT NULL here; the NULL case is a side check in the Code block.
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER NOT NULL, hire_date TEXT);
INSERT INTO employees VALUES
 (1,'Asha',10,90,'2020-01-10'),(2,'Ben',10,80,'2019-05-01'),(3,'Chitra',10,80,'2018-02-01'),
 (4,'Dev',10,80,'2018-02-01'),(5,'Esha',10,70,'2021-07-01'),
 (6,'Farid',20,60,'2022-01-01'),(7,'Gita',20,60,'2022-01-01'),(8,'Hari',20,50,'2017-03-03'),
 (9,'Ila',30,75,'2023-04-04');
```

**SQL answer:** exactly two (`SQL_ROWNUM`) and the DENSE_RANK variant (`SQL_DENSE`).
```sql
WITH r AS (
  SELECT emp_id, name, dept_id, salary, hire_date,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, hire_date, emp_id) AS rn
  FROM employees
)
SELECT dept_id, rn, emp_id, name, salary, hire_date
FROM r
WHERE rn <= 2
ORDER BY dept_id, rn
```
```sql
WITH r AS (
  SELECT emp_id, name, dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS drk
  FROM employees
)
SELECT dept_id, drk, emp_id, name, salary
FROM r
WHERE drk <= 2
ORDER BY dept_id, drk, emp_id
```

**pandas answer:** sort by the same keys and take `groupby().head(2)`; the dense variant is a groupby rank with `method='dense'`.
```python
ordered = emp.sort_values(["dept_id", "salary", "hire_date", "emp_id"], ascending=[True, False, True, True])
pd_a = ordered.groupby("dept_id").head(2)
dense = emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False)
pd_b = emp[dense <= 2].assign(drk=dense)
```

**Example:**
- Dept 10, exactly two: Asha (90) is first. Among the three at 80 the earliest hire date wins, and Chitra and Dev tie on 2018-02-01, so emp_id decides: Chitra (3). Result Asha, Chitra. Ben (hired later) and Dev (higher id) are cut.
- Dept 10, DENSE_RANK <= 2: levels 90 and 80, so Asha plus all three at 80: four rows.
- Dept 20: Farid and Gita tie fully on salary and hire date, so emp_id puts Farid first and both are the top two, with Hari (50) cut. DENSE_RANK keeps Farid, Gita (level 1) and Hari (level 2): three rows.
- Dept 30: one employee, one row in both variants (no padding to two).

**Code:** run with `python3 -I`.
```python
# Q45: top 2 per department with explicit tie rules, and the DENSE_RANK variant
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER NOT NULL, hire_date TEXT);
INSERT INTO employees VALUES
 (1,'Asha',10,90,'2020-01-10'),(2,'Ben',10,80,'2019-05-01'),(3,'Chitra',10,80,'2018-02-01'),
 (4,'Dev',10,80,'2018-02-01'),(5,'Esha',10,70,'2021-07-01'),
 (6,'Farid',20,60,'2022-01-01'),(7,'Gita',20,60,'2022-01-01'),(8,'Hari',20,50,'2017-03-03'),
 (9,'Ila',30,75,'2023-04-04');
"""
SQL_ROWNUM = """
WITH r AS (
  SELECT emp_id, name, dept_id, salary, hire_date,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, hire_date, emp_id) AS rn
  FROM employees
)
SELECT dept_id, rn, emp_id, name, salary, hire_date
FROM r
WHERE rn <= 2
ORDER BY dept_id, rn
"""
SQL_DENSE = """
WITH r AS (
  SELECT emp_id, name, dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS drk
  FROM employees
)
SELECT dept_id, drk, emp_id, name, salary
FROM r
WHERE drk <= 2
ORDER BY dept_id, drk, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_ROWNUM, con)
b = pd.read_sql_query(SQL_DENSE, con)
print("exactly 2 per department (salary DESC, hire_date, emp_id):"); print(a.to_string(index=False))
print("\ntop 2 salary levels, all tied employees (DENSE_RANK <= 2):"); print(b.to_string(index=False))

emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
ordered = emp.sort_values(["dept_id", "salary", "hire_date", "emp_id"], ascending=[True, False, True, True])
pd_a = ordered.groupby("dept_id").head(2)
dense = emp.groupby("dept_id")["salary"].rank(method="dense", ascending=False)
pd_b = emp[dense <= 2].assign(drk=dense)
# pd:end
pd_a = pd_a.assign(rn=pd_a.groupby("dept_id").cumcount() + 1)
pd.testing.assert_frame_equal(a[["dept_id", "rn", "emp_id"]],
    pd_a[["dept_id", "rn", "emp_id"]].reset_index(drop=True), check_dtype=False)
pd_b = pd_b.sort_values(["dept_id", "drk", "emp_id"]).reset_index(drop=True)
assert b["emp_id"].tolist() == pd_b["emp_id"].tolist() and b["drk"].tolist() == pd_b["drk"].astype(int).tolist()
print("\nrows per department, ROW_NUMBER variant:", a.groupby("dept_id").size().to_dict())
print("rows per department, DENSE_RANK variant:", b.groupby("dept_id").size().to_dict())

# side check: a NULL salary (the table above forbids it; a nullable column behaves differently)
con.executescript("CREATE TABLE emp2(emp_id INTEGER, dept_id INTEGER, salary INTEGER); INSERT INTO emp2 VALUES (1,10,80),(2,10,NULL),(3,10,NULL);")
n_rows = con.execute("""SELECT COUNT(*) FROM (SELECT ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) rn FROM emp2) WHERE rn <= 2""").fetchone()[0]
n_dense = con.execute("""SELECT COUNT(*) FROM (SELECT DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) r FROM emp2) WHERE r <= 2""").fetchone()[0]
e2 = pd.read_sql_query("SELECT * FROM emp2", con)
p_dense = int((e2.groupby("dept_id")["salary"].rank(method="dense", ascending=False) <= 2).sum())
print("\nNULL salary side check (one real salary, two NULLs): SQL ROW_NUMBER <= 2 keeps", n_rows,
      "| SQL DENSE_RANK <= 2 keeps", n_dense, "| pandas dense rank <= 2 keeps", p_dense)
print("asserts passed")
```

**Output (my run):**
```text
exactly 2 per department (salary DESC, hire_date, emp_id):
 dept_id  rn  emp_id   name  salary  hire_date
      10   1       1   Asha      90 2020-01-10
      10   2       3 Chitra      80 2018-02-01
      20   1       6  Farid      60 2022-01-01
      20   2       7   Gita      60 2022-01-01
      30   1       9    Ila      75 2023-04-04

top 2 salary levels, all tied employees (DENSE_RANK <= 2):
 dept_id  drk  emp_id   name  salary
      10    1       1   Asha      90
      10    2       2    Ben      80
      10    2       3 Chitra      80
      10    2       4    Dev      80
      20    1       6  Farid      60
      20    1       7   Gita      60
      20    2       8   Hari      50
      30    1       9    Ila      75

rows per department, ROW_NUMBER variant: {10: 2, 20: 2, 30: 1}
rows per department, DENSE_RANK variant: {10: 4, 20: 3, 30: 1}

NULL salary side check (one real salary, two NULLs): SQL ROW_NUMBER <= 2 keeps 2 | SQL DENSE_RANK <= 2 keeps 3 | pandas dense rank <= 2 keeps 1
asserts passed
```

**Edge cases:**
- Single-employee department: one row; ROW_NUMBER never invents rows.
- Row counts differ: 2 / 2 / 1 for the ROW_NUMBER variant versus 4 / 3 / 1 for DENSE_RANK in my run, so the DENSE_RANK result is not "top 2 people".
- NULL salary (not in the table above because of NOT NULL): in my side check (one real salary, two NULLs in one department) SQLite ROW_NUMBER <= 2 kept 2 rows (the NULL rows rank after the real one in DESC order), DENSE_RANK <= 2 kept 3, and pandas dense rank <= 2 kept 1, because pandas leaves NaN unranked. If the column is nullable, decide whether NULL salaries should be excluded and filter them out in both versions.
- Hire date as ISO text sorts correctly; a different text format would not.

**Then explain:**
- **ROW_NUMBER variant:** a precise, repeatable rule; the cost is that two people with the same salary can be treated differently because of hire date. That is only fair if the business agrees the hire date matters.
- **DENSE_RANK variant:** treats equal salary as equal, but the number of people returned varies.
- **Stakeholder wording:** "Two people per department; if salaries are equal, the earlier hire wins, then the lower employee id. If you would rather include everyone who ties, I can return the top two salary levels, which may give more than two people." Show the Dept 10 example, where it is 2 versus 4 rows.
- **pandas:** `head(2)` after a full sort is the ROW_NUMBER variant; `rank(method='dense')` is DENSE_RANK; both asserted equal to SQL.

**Follow-ups:**
- *Why not RANK <= 2?* It includes ties at the cutoff like DENSE_RANK but also leaves gaps after ties; worked by hand, not run: for dept 10 it returns Asha plus the three at 80 (ranks 1 and 2), the same four rows, but for dept 20 Farid and Gita are both rank 1 and Hari is rank 3, so RANK <= 2 drops Hari while DENSE_RANK keeps him.
- *Different tie rule?* Change the ORDER BY list; keep a unique column last.
- *How do I show the rank?* Select `rn` or `drk` as in the output.

**Common mistakes:**
- Not including a unique last tie-break column.
- Assuming "top 2" means two rows when the requirement was "top 2 salaries".
- Forgetting `ascending=[...]` with mixed directions in pandas.
- Leaving NULL salaries unhandled when the column allows them.

### Q46 ⭐ 🔴 Second highest salary per department including departments with a single distinct salary (returned as NULL), with windows: employees(emp_id, name, dept_id, salary) and departments(dept_id, dept_name). Use DENSE_RANK in a CTE, a LEFT JOIN from departments so a department with one distinct salary or no employees still appears with NULL, and aggregate with MAX(CASE WHEN rnk = 2 THEN salary END). Run it, compare with the Part 3 correlated-subquery version, and give the pandas groupby with unique and nlargest approach.
**Asked at:** public LeetCode-style problem bank (176 Second Highest Salary, 177 Nth Highest Salary, 184 Department Highest Salary, 185 Department Top Three Salaries; known only from third-party list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** Rank distinct salaries with DENSE_RANK per department in a CTE, LEFT JOIN from `departments` so every department stays, and take `MAX(CASE WHEN rnk = 2 THEN salary END)`, which is NULL when there is no second distinct salary or no employee at all.

**Schema and sample data:** four departments. Eng (10) has salaries 100, 100, 80, 60 (top tied, so the second distinct is 80). Ops (20) has 70, 70 (one distinct salary). Legal (30) has no employees. Sales (40) has 90, 50 and one NULL salary.
```sql
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (10,'Eng'),(20,'Ops'),(30,'Legal'),(40,'Sales');
INSERT INTO employees VALUES
 (1,'Asha',10,100),(2,'Ben',10,100),(3,'Chitra',10,80),(4,'Dev',10,60),
 (5,'Esha',20,70),(6,'Farid',20,70),
 (7,'Gita',40,90),(8,'Hari',40,50),(9,'Ila',40,NULL);
```

**SQL answer:** window version `SQL_MAIN`, correlated-subquery version `SQL_CORRELATED`. A note on the premise: Part 3 does not contain a per-department version; its Q15 is the whole-company Nth highest and the answer there says the per-department form needs `AND e2.dept_id = e1.dept_id`. The version below is my own per-department correlated form (second highest = the maximum below the maximum).
```sql
WITH r AS (
  SELECT dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT d.dept_id, d.dept_name,
       MAX(CASE WHEN r.rnk = 2 THEN r.salary END) AS second_highest
FROM departments d
LEFT JOIN r ON r.dept_id = d.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY d.dept_id
```
```sql
SELECT d.dept_id, d.dept_name,
       (SELECT MAX(e.salary) FROM employees e
         WHERE e.dept_id = d.dept_id
           AND e.salary < (SELECT MAX(x.salary) FROM employees x WHERE x.dept_id = d.dept_id)) AS second_highest
FROM departments d
ORDER BY d.dept_id
```

**pandas answer:** per group, take the distinct non-NaN values sorted descending and pick the second if it exists; then map onto the departments table so empty departments appear as NaN.
```python
def second(s):
    u = np.sort(s.dropna().unique())[::-1]
    return u[1] if len(u) > 1 else np.nan
sec = emp.groupby("dept_id")["salary"].agg(second)
pd_df = dep.assign(second_highest=dep["dept_id"].map(sec)).sort_values("dept_id").reset_index(drop=True)
```

**Example:**
- Eng: distinct salaries 100, 80, 60, ranks 1, 2, 3, so the second is 80 (the tied 100s are one level).
- Ops: one distinct salary (70), no rank 2, so the CASE finds nothing and MAX of nothing is NULL.
- Legal: the LEFT JOIN keeps the department with no matching rows; MAX over a NULL-only group is NULL.
- Sales: the NULL salary is filtered in the CTE; distinct salaries 90 and 50, so the second is 50.

**Code:** run with `python3 -I`.
```python
# Q46: second highest distinct salary per department, NULL when it does not exist
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE departments(dept_id INTEGER PRIMARY KEY, dept_name TEXT);
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO departments VALUES (10,'Eng'),(20,'Ops'),(30,'Legal'),(40,'Sales');
INSERT INTO employees VALUES
 (1,'Asha',10,100),(2,'Ben',10,100),(3,'Chitra',10,80),(4,'Dev',10,60),
 (5,'Esha',20,70),(6,'Farid',20,70),
 (7,'Gita',40,90),(8,'Hari',40,50),(9,'Ila',40,NULL);
"""
SQL_MAIN = """
WITH r AS (
  SELECT dept_id, salary,
         DENSE_RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rnk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT d.dept_id, d.dept_name,
       MAX(CASE WHEN r.rnk = 2 THEN r.salary END) AS second_highest
FROM departments d
LEFT JOIN r ON r.dept_id = d.dept_id
GROUP BY d.dept_id, d.dept_name
ORDER BY d.dept_id
"""
SQL_CORRELATED = """
SELECT d.dept_id, d.dept_name,
       (SELECT MAX(e.salary) FROM employees e
         WHERE e.dept_id = d.dept_id
           AND e.salary < (SELECT MAX(x.salary) FROM employees x WHERE x.dept_id = d.dept_id)) AS second_highest
FROM departments d
ORDER BY d.dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
a = pd.read_sql_query(SQL_MAIN, con)
b = pd.read_sql_query(SQL_CORRELATED, con)
print("window version:"); print(a.to_string(index=False, na_rep="NULL"))
pd.testing.assert_frame_equal(a, b)
print("\ncorrelated-subquery version is identical: True")

dep = pd.read_sql_query("SELECT * FROM departments", con)
emp = pd.read_sql_query("SELECT * FROM employees", con)
# pd:main
def second(s):
    u = np.sort(s.dropna().unique())[::-1]
    return u[1] if len(u) > 1 else np.nan
sec = emp.groupby("dept_id")["salary"].agg(second)
pd_df = dep.assign(second_highest=dep["dept_id"].map(sec)).sort_values("dept_id").reset_index(drop=True)
# pd:end
pd.testing.assert_frame_equal(a, pd_df, check_dtype=False)
# the nlargest route: top 2 per group, then the smaller one only if two distinct values
nl = emp.dropna(subset=["salary"]).drop_duplicates(["dept_id", "salary"]).groupby("dept_id")["salary"].nlargest(2)
nl2 = nl.groupby(level=0).apply(lambda s: s.iloc[1] if len(s) == 2 else np.nan)
print("\nnlargest after drop_duplicates, second per dept:", nl2.to_dict())
print("without drop_duplicates, nlargest(2) would give dept 20 the value 70 (the top value twice):",
      emp.groupby("dept_id")["salary"].nlargest(2).loc[20].tolist())
print("asserts passed: window == correlated == pandas (dept 30 has no employees, dept 20 one distinct value: NaN/NULL)")
```

**Output (my run):**
```text
window version:
 dept_id dept_name  second_highest
      10       Eng            80.0
      20       Ops            NULL
      30     Legal            NULL
      40     Sales            50.0

correlated-subquery version is identical: True

nlargest after drop_duplicates, second per dept: {10: 80.0, 20: nan, 40: 50.0}
without drop_duplicates, nlargest(2) would give dept 20 the value 70 (the top value twice): [70.0, 70.0]
asserts passed: window == correlated == pandas (dept 30 has no employees, dept 20 one distinct value: NaN/NULL)
```

**Edge cases:**
- Why the filter `salary IS NOT NULL` in the CTE: in SQLite NULL sorts last in DESC order and would take a rank of its own; for a department with one real salary the NULL would become rank 2, and `MAX(CASE ... salary END)` would still return NULL, but for clarity and for other engines I remove NULL salaries first.
- `GROUP BY` after the LEFT JOIN with MAX is what turns "no rank 2" into a single NULL row instead of no row.
- Ties at the top (Eng) do not push the second level away, because DENSE_RANK counts values, not rows. RANK = 2 would find nothing for Eng.
- The two SQL versions and the pandas version agree on all four departments in the assert.
- pandas gives NaN (float) where SQL gives NULL.

**Then explain:**
- **DENSE_RANK:** ranks values, so rank 2 is the second distinct salary.
- **LEFT JOIN from departments:** an inner join, or aggregating only from `employees`, would silently drop Legal. Starting from the dimension table is how you keep empty groups.
- **Correlated version:** simpler to read for "second" only (max below the max), clumsy for third, fourth; it re-evaluates per department. I did not time it; on SQLite it matched the window result.
- **pandas:** `drop_duplicates(['dept_id','salary'])` before `nlargest(2)` is needed, otherwise the tied top value appears twice (run output: dept 20 gives 70 and 70).

**Follow-ups:**
- *Nth instead of second?* Replace 2 with N (in Python a parameter, as in Q6).
- *Return the employees who earn the second highest salary?* Filter `rnk = 2` in the CTE and join back, instead of aggregating.
- *What if a department should show 0 instead of NULL?* Wrap in COALESCE, but state that it changes the meaning.

**Common mistakes:**
- Using ROW_NUMBER or RANK and getting the tied top salary as "second".
- Starting from `employees` and losing departments with no (or one distinct) salary.
- Forgetting that `MAX` over zero matching CASE branches gives NULL, not 0.
- In pandas, `nlargest(2)` without removing duplicates.

### Q47 ⭐ 🔴 Users in the top 10 percent of activity within each country: events(event_id, user_id, event_time) and users(user_id, country). Count events per user, then within each country find users whose activity percentile is at or above the 90th using PERCENT_RANK or CUME_DIST over (PARTITION BY country ORDER BY n_events). Explain why NTILE(10) is a poor selector for small countries (one-user country is always bucket 1), how ties behave, and give the pandas groupby rank(pct=True) version, noting pandas pct differs from SQL PERCENT_RANK.
**Asked at:** LetsDataScience SQL window-function interview guide (14 sample questions: top earner per department, nth highest salary, quartiles, top 5 percent per state), not a candidate report; analyst and data scientist screens at product companies and GCCs
**Say this first (1 line):** Count events per user (LEFT JOIN so inactive users count as 0), then compute `CUME_DIST() OVER (PARTITION BY country ORDER BY n_events)` and keep rows with value >= 0.9 for "at or above the 90th percentile of the country"; PERCENT_RANK >= 0.9 is stricter and NTILE(10) is positional, so both behave badly on small or tied groups.

**Schema and sample data:** 16 users in three countries. Event counts per user (a loop in the Code block writes that many `events` rows): India (IN) users 1..10 have 50, 40, 40, 30, 20, 20, 10, 5, 3, 0 events (user 10 has none); US users 11..15 have 9, 4, 4, 1, 1; Singapore (SG) has one user (16) with 2.
```sql
CREATE TABLE users(user_id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT);
-- users 1..16 as above; events: one row per event (loop in the Code block)
```

**SQL answer:** one query shows PERCENT_RANK, CUME_DIST and NTILE(10) side by side with a 0/1 flag for each selection rule. The NTILE order has `user_id` as a tie-breaker so its output is repeatable.
```sql
WITH per_user AS (
  SELECT u.user_id, u.country, COUNT(e.event_id) AS n_events
  FROM users u
  LEFT JOIN events e ON e.user_id = u.user_id
  GROUP BY u.user_id, u.country
), scored AS (
  SELECT user_id, country, n_events,
         PERCENT_RANK() OVER (PARTITION BY country ORDER BY n_events) AS pr,
         CUME_DIST()    OVER (PARTITION BY country ORDER BY n_events) AS cd,
         NTILE(10)      OVER (PARTITION BY country ORDER BY n_events DESC, user_id) AS decile
  FROM per_user
)
SELECT country, user_id, n_events, ROUND(pr, 3) AS pr, ROUND(cd, 3) AS cd, decile,
       CASE WHEN pr >= 0.9 THEN 1 ELSE 0 END AS top_by_pr,
       CASE WHEN cd >= 0.9 THEN 1 ELSE 0 END AS top_by_cd
FROM scored
ORDER BY country, n_events DESC, user_id
```

**pandas answer:** merge, count, then rank within country. `method='max'` pct equals CUME_DIST; PERCENT_RANK is built from `method='min'`.
```python
n = (users.merge(events, on="user_id", how="left")
          .groupby(["user_id", "country"])["event_id"].count().rename("n_events").reset_index())
n["pct_max"] = n.groupby("country")["n_events"].rank(pct=True, method="max")      # equals CUME_DIST
n["pct_avg"] = n.groupby("country")["n_events"].rank(pct=True)                    # default 'average'
size = n.groupby("country")["n_events"].transform("size")
r_min = n.groupby("country")["n_events"].rank(method="min")
n["pr"] = ((r_min - 1) / (size - 1)).fillna(0.0)                                  # PERCENT_RANK; one-row group gives 0/0
top = n[n["pct_max"] >= 0.9]
```

**Example:**
- IN has 10 users. Ascending by events, user 1 (50) is last: CUME_DIST 10/10 = 1.0, PERCENT_RANK 9/9 = 1.0. Users 2 and 3 tie at 40 and occupy ranks 8 to 9: PERCENT_RANK (8 - 1) / 9 = 0.778 and CUME_DIST 9/10 = 0.9.
- So `CUME_DIST >= 0.9` selects users 1, 2, 3 (three users, 30 percent of a 10-user country) because the tie at 40 sits exactly on the cutoff. `PERCENT_RANK >= 0.9` selects only user 1.
- US has 5 users: user 11 (9 events) is 1.0 on both and is the only one selected. The two users with 4 events have CUME_DIST 0.8, not enough.
- SG has one user: CUME_DIST 1.0, PERCENT_RANK 0.0 (one-row partition), NTILE bucket 1. CUME_DIST and NTILE select that user; PERCENT_RANK does not.

**Code:** run with `python3 -I`.
```python
# Q47: users in the top 10 percent of activity within each country
import sqlite3
import numpy as np
import pandas as pd

# event counts per user are listed here so the data can be checked by hand; the loop writes one events row per event
COUNTS = {  # user_id: (country, events)
    1: ("IN", 50), 2: ("IN", 40), 3: ("IN", 40), 4: ("IN", 30), 5: ("IN", 20),
    6: ("IN", 20), 7: ("IN", 10), 8: ("IN", 5), 9: ("IN", 3), 10: ("IN", 0),
    11: ("US", 9), 12: ("US", 4), 13: ("US", 4), 14: ("US", 1), 15: ("US", 1),
    16: ("SG", 2),
}
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, country TEXT);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_time TEXT);
""")
con.executemany("INSERT INTO users VALUES (?,?)", [(u, c) for u, (c, _) in COUNTS.items()])
ev, eid = [], 1
for u, (_, n) in COUNTS.items():
    for k in range(n):
        ev.append((eid, u, f"2026-01-{1 + k % 28:02d}")); eid += 1
con.executemany("INSERT INTO events VALUES (?,?,?)", ev)

SQL_MAIN = """
WITH per_user AS (
  SELECT u.user_id, u.country, COUNT(e.event_id) AS n_events
  FROM users u
  LEFT JOIN events e ON e.user_id = u.user_id
  GROUP BY u.user_id, u.country
), scored AS (
  SELECT user_id, country, n_events,
         PERCENT_RANK() OVER (PARTITION BY country ORDER BY n_events) AS pr,
         CUME_DIST()    OVER (PARTITION BY country ORDER BY n_events) AS cd,
         NTILE(10)      OVER (PARTITION BY country ORDER BY n_events DESC, user_id) AS decile
  FROM per_user
)
SELECT country, user_id, n_events, ROUND(pr, 3) AS pr, ROUND(cd, 3) AS cd, decile,
       CASE WHEN pr >= 0.9 THEN 1 ELSE 0 END AS top_by_pr,
       CASE WHEN cd >= 0.9 THEN 1 ELSE 0 END AS top_by_cd
FROM scored
ORDER BY country, n_events DESC, user_id
"""
sql = pd.read_sql_query(SQL_MAIN, con)
print(sql.to_string(index=False))
print("\nselected by PERCENT_RANK >= 0.9:", sql.loc[sql.top_by_pr == 1, "user_id"].tolist())
print("selected by CUME_DIST    >= 0.9:", sql.loc[sql.top_by_cd == 1, "user_id"].tolist())
print("NTILE(10) bucket 1         :", sql.loc[sql.decile == 1, "user_id"].tolist())

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
n = (users.merge(events, on="user_id", how="left")
          .groupby(["user_id", "country"])["event_id"].count().rename("n_events").reset_index())
n["pct_max"] = n.groupby("country")["n_events"].rank(pct=True, method="max")      # equals CUME_DIST
n["pct_avg"] = n.groupby("country")["n_events"].rank(pct=True)                    # default 'average'
size = n.groupby("country")["n_events"].transform("size")
r_min = n.groupby("country")["n_events"].rank(method="min")
n["pr"] = ((r_min - 1) / (size - 1)).fillna(0.0)                                  # PERCENT_RANK; one-row group gives 0/0
top = n[n["pct_max"] >= 0.9]
# pd:end
m = sql.merge(n, on=["user_id", "country"])
assert np.allclose(m["cd"], m["pct_max"].round(3))
assert np.allclose(m["pr_x"], m["pr_y"].round(3))
assert sorted(top["user_id"]) == sorted(sql.loc[sql.top_by_cd == 1, "user_id"])
print("\npandas rank(pct=True, method='max') >= 0.9 selects:", sorted(top["user_id"]), "(same as CUME_DIST)")
print("pandas default 'average' pct for the tied users 2,3 in IN:", n.loc[n.user_id.isin([2, 3]), "pct_avg"].round(3).tolist(),
      "vs method='max':", n.loc[n.user_id.isin([2, 3]), "pct_max"].round(3).tolist())
print("asserts passed")
```

**Output (my run):**
```text
country  user_id  n_events    pr  cd  decile  top_by_pr  top_by_cd
     IN        1        50 1.000 1.0       1          1          1
     IN        2        40 0.778 0.9       2          0          1
     IN        3        40 0.778 0.9       3          0          1
     IN        4        30 0.667 0.7       4          0          0
     IN        5        20 0.444 0.6       5          0          0
     IN        6        20 0.444 0.6       6          0          0
     IN        7        10 0.333 0.4       7          0          0
     IN        8         5 0.222 0.3       8          0          0
     IN        9         3 0.111 0.2       9          0          0
     IN       10         0 0.000 0.1      10          0          0
     SG       16         2 0.000 1.0       1          0          1
     US       11         9 1.000 1.0       1          1          1
     US       12         4 0.500 0.8       2          0          0
     US       13         4 0.500 0.8       3          0          0
     US       14         1 0.000 0.4       4          0          0
     US       15         1 0.000 0.4       5          0          0

selected by PERCENT_RANK >= 0.9: [1, 11]
selected by CUME_DIST    >= 0.9: [1, 2, 3, 16, 11]
NTILE(10) bucket 1         : [1, 16, 11]

pandas rank(pct=True, method='max') >= 0.9 selects: [1, 2, 3, 11, 16] (same as CUME_DIST)
pandas default 'average' pct for the tied users 2,3 in IN: [0.85, 0.85] vs method='max': [0.9, 0.9]
asserts passed
```

**Edge cases:**
- Small groups: NTILE(10) over a one-user country always gives bucket 1, so "bucket 1" means "everyone" there. With 5 users, NTILE(10) also makes five buckets of one, and user 11 alone is bucket 1 (output).
- Ties on the cutoff: CUME_DIST includes both tied users (2 and 3); NTILE(10) put users 2 and 3 in different buckets (2 and 3) even though both have 40 events, because it is positional.
- A single-user group: PERCENT_RANK is 0.0, so a PERCENT_RANK threshold excludes the only user; CUME_DIST includes them. Decide which you want.
- Zero-event users: included via LEFT JOIN with `COUNT(e.event_id)`; user 10 has 0. With an inner join they would vanish and change every percentile.
- pandas `rank(pct=True)` with default `average` ranks gives the tied pair 0.85 instead of 0.9 (output), so the threshold would drop them; with `method='max'` it matches CUME_DIST.

**Then explain:**
- **Which one to use:** CUME_DIST >= 0.9 reads as "at least as active as 90 percent of the country (including ties and yourself)". PERCENT_RANK >= 0.9 reads as "at least 90 percent of the others are strictly below you".
- **Why not NTILE(10):** it forces equal-sized buckets by position, ignores ties and cannot say "top 10 percent" when a group has fewer than ten users.
- **Whether a user is "top 10 percent" with n small:** no method can pick exactly 10 percent of 5 users; say so.
- **pandas:** `groupby('country')['n_events'].rank(pct=True, method='max') >= 0.9`; the code asserts the same users as CUME_DIST.

**Follow-ups:**
- *What if you need at most 10 percent?* Use PERCENT_RANK or a ROW_NUMBER cutoff, and say ties are cut arbitrarily or by a stated rule.
- *Minimum group size?* Exclude countries with fewer than, say, 10 users, and state the threshold.
- *Activity window?* Filter the events by date inside the first CTE.

**Common mistakes:**
- Using `NTILE(10) = 1` for small groups.
- Forgetting the LEFT JOIN so inactive users disappear.
- Mixing up pandas pct with SQL PERCENT_RANK.
- Not saying how ties at the cutoff are treated.

### Q48 ⭐ 🔴 Ranking after a join: a join fan-out silently changes ranks. orders(order_id, customer_id, amount) and order_items(item_id, order_id, product_id). A report ranks customers by SUM(amount) after joining orders to order_items, which repeats each order amount per item and inflates totals (and can change the rank order). Reproduce it, diagnose with COUNT(*) versus COUNT(DISTINCT order_id), and fix by aggregating to the right grain before ranking. Explain that RANK is computed on the wrong inputs, not wrongly, and give the pandas bug and fix.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Joining `orders` to `order_items` repeats each order's amount once per item, so `SUM(amount)` is inflated for customers whose orders have many items and the RANK computed on those totals is correct for the wrong numbers; diagnose with `COUNT(*)` versus `COUNT(DISTINCT order_id)` and rank after aggregating at the right grain.

**Schema and sample data:** five orders for four customers. Order 1 (customer 1, 100) has four items. Orders 2 and 3 (customer 2, 150 and 120) have one item each. Order 4 (customer 3, 200) has one item. Order 5 (customer 4, 50) has no items.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,2,150),(3,2,120),(4,3,200),(5,4,50);
INSERT INTO order_items VALUES
 (1,1,7),(2,1,8),(3,1,9),(4,1,10),
 (5,2,7),(6,3,8),(7,4,9);
```

**SQL answer:** the buggy ranking (`SQL_BUG`), the diagnostic (`SQL_DIAG`) and the fix (`SQL_FIX`), which does not need the items table at all because the question asks about order amounts.
```sql
SELECT o.customer_id, SUM(o.amount) AS total,
       RANK() OVER (ORDER BY SUM(o.amount) DESC) AS rnk
FROM orders o JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY rnk, o.customer_id
```
```sql
SELECT o.customer_id, COUNT(*) AS joined_rows, COUNT(DISTINCT o.order_id) AS real_orders
FROM orders o JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id
```
```sql
SELECT customer_id, SUM(amount) AS total,
       RANK() OVER (ORDER BY SUM(amount) DESC) AS rnk
FROM orders
GROUP BY customer_id
ORDER BY rnk, customer_id
```

**pandas answer:** the merge reproduces the fan-out; the fix aggregates the orders frame on its own (or collapses items to one row per order before merging if item columns are needed).
```python
joined = orders.merge(items, on="order_id")                                   # one row per item: the fan-out
bug_pd = joined.groupby("customer_id")["amount"].sum().rename("total").reset_index()
bug_pd["rnk"] = bug_pd["total"].rank(method="min", ascending=False).astype(int)
fix_pd = orders.groupby("customer_id")["amount"].sum().rename("total").reset_index()
fix_pd["rnk"] = fix_pd["total"].rank(method="min", ascending=False).astype(int)
```

**Example:**
- True totals from `orders` alone: customer 2 is 150 + 120 = 270, customer 3 is 200, customer 1 is 100, customer 4 is 50. True order: 2, 3, 1, 4.
- After the join, order 1 appears four times (once per item), so customer 1's total becomes 4 x 100 = 400 and jumps from last-but-one to first. Customer 2 stays 270 (one item per order).
- The buggy ranks: 1 (400), 2 (270), 3 (200). Customer 4 has no items, so the inner join removes it completely.
- Diagnostic: customer 1 shows 4 joined rows but 1 real order; that mismatch is the signature of the fan-out.

**Code:** run with `python3 -I`.
```python
# Q48: ranking after a join fan-out
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER);
INSERT INTO orders VALUES (1,1,100),(2,2,150),(3,2,120),(4,3,200),(5,4,50);
INSERT INTO order_items VALUES
 (1,1,7),(2,1,8),(3,1,9),(4,1,10),      -- order 1 has 4 items
 (5,2,7),(6,3,8),(7,4,9);               -- orders 2, 3, 4 have 1 item; order 5 has none
"""
SQL_BUG = """
SELECT o.customer_id, SUM(o.amount) AS total,
       RANK() OVER (ORDER BY SUM(o.amount) DESC) AS rnk
FROM orders o JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY rnk, o.customer_id
"""
SQL_DIAG = """
SELECT o.customer_id, COUNT(*) AS joined_rows, COUNT(DISTINCT o.order_id) AS real_orders
FROM orders o JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.customer_id
ORDER BY o.customer_id
"""
SQL_FIX = """
SELECT customer_id, SUM(amount) AS total,
       RANK() OVER (ORDER BY SUM(amount) DESC) AS rnk
FROM orders
GROUP BY customer_id
ORDER BY rnk, customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
bug, diag, fix = q(SQL_BUG), q(SQL_DIAG), q(SQL_FIX)
print("buggy (join first, then rank):"); print(bug.to_string(index=False))
print("\ndiagnosis, COUNT(*) vs COUNT(DISTINCT order_id):"); print(diag.to_string(index=False))
print("\nfixed (aggregate at order grain, then rank):"); print(fix.to_string(index=False))
assert bug["customer_id"].tolist() != fix["customer_id"].tolist()

orders = q("SELECT * FROM orders"); items = q("SELECT * FROM order_items")
# pd:main
joined = orders.merge(items, on="order_id")                                   # one row per item: the fan-out
bug_pd = joined.groupby("customer_id")["amount"].sum().rename("total").reset_index()
bug_pd["rnk"] = bug_pd["total"].rank(method="min", ascending=False).astype(int)
fix_pd = orders.groupby("customer_id")["amount"].sum().rename("total").reset_index()
fix_pd["rnk"] = fix_pd["total"].rank(method="min", ascending=False).astype(int)
# pd:end
pd.testing.assert_frame_equal(bug, bug_pd.sort_values(["rnk", "customer_id"]).reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(fix, fix_pd.sort_values(["rnk", "customer_id"]).reset_index(drop=True), check_dtype=False)
print("\ncustomer 4 (order 5 has no items) is missing from the buggy result:", 4 not in bug["customer_id"].tolist())
print("pandas: merged rows", len(joined), "vs orders", len(orders), "| order_id duplicated after merge:", int(joined["order_id"].duplicated().sum()))
# a second safe fix: collapse items to one row per order first
items_per_order = items.groupby("order_id").size().rename("n_items").reset_index()
safe = orders.merge(items_per_order, on="order_id", how="left")
assert len(safe) == len(orders)
assert safe.groupby("customer_id")["amount"].sum().equals(fix_pd.set_index("customer_id")["total"])
print("asserts passed: SQL bug == pandas bug; SQL fix == pandas fix; the two rankings differ")
```

**Output (my run):**
```text
buggy (join first, then rank):
 customer_id  total  rnk
           1    400    1
           2    270    2
           3    200    3

diagnosis, COUNT(*) vs COUNT(DISTINCT order_id):
 customer_id  joined_rows  real_orders
           1            4            1
           2            2            2
           3            1            1

fixed (aggregate at order grain, then rank):
 customer_id  total  rnk
           2    270    1
           3    200    2
           1    100    3
           4     50    4

customer 4 (order 5 has no items) is missing from the buggy result: True
pandas: merged rows 7 vs orders 5 | order_id duplicated after merge: 3
asserts passed: SQL bug == pandas bug; SQL fix == pandas fix; the two rankings differ
```

**Edge cases:**
- Rank order changed, not only the totals: customer 1 went from third to first in my run.
- Inner join also drops customers whose orders have no items (customer 4 disappears from the buggy result). A LEFT JOIN would keep the row but would not cure the inflation.
- `COUNT(DISTINCT order_id)` fixes a count of orders but not a SUM, because the repeated amount is still added several times.
- If you need item-level information as well, aggregate items to one row per order first (a CTE with `GROUP BY order_id`), then join; the Code block checks that this keeps one row per order.

**Then explain:**
- **RANK is not wrong:** it ranks whatever rows it is given. The bug is the grain of the inputs, which is why checking `COUNT(*)` against `COUNT(DISTINCT key)` right after a join is a good habit.
- **Fix:** choose the grain first (one row per order), aggregate to the grain you rank on (one row per customer), then rank. The window sits last.
- **Same bug in pandas:** `merge` also multiplies rows (7 merged rows from 5 orders, 3 duplicated order ids in the output); `groupby.sum` then adds them.
- **Sanity check to propose:** compare the report total with the plain `SUM(amount)` on `orders`; they should match.

**Follow-ups:**
- *Related trap?* Joining two child tables to one parent (see Part 2 on the chasm trap).
- *How do I test a CTE in isolation?* Select from it and compare row count and distinct keys.
- *Why not `SUM(DISTINCT amount)`?* It would collapse two different orders with the same amount.

**Common mistakes:**
- Using `SUM(DISTINCT amount)` as the fix.
- Adding more joins to a report without re-checking the grain.
- Believing a plausible-looking ranking proves the totals are right.
- Joining `order_items` just to filter and forgetting it multiplies rows (use EXISTS for filtering).

### Q49 ⭐ 🔴 Revenue by decile (Pareto-style) with NTILE: orders(order_id, customer_id, amount). Compute customer totals, bucket customers into deciles with NTILE(10) over total descending, and report per decile the number of customers, total revenue, and share of overall revenue, showing that the top decile holds a large share on skewed data. Explain NTILE unevenness with few customers, ties across a bucket boundary, and give the pandas qcut or rank-based version, stating where it differs from NTILE.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Total spend per customer, `NTILE(10) OVER (ORDER BY total DESC, customer_id)` to cut the customers into ten positional buckets, then per bucket count customers, sum revenue and divide by the grand total; on skewed data decile 1 holds a large share (about half in my sample).

**Schema and sample data:** 23 customers with totals 1000, 700, 500, 400, 300, 250, 200, 150, 120, 120, 100, 90, 80, 70, 60, 55, 50, 45, 40, 35, 30, 25, 20 (customer ids 1 to 23 in that order). Each customer has two orders that add up to the total (a loop in the Code block writes them). Customers 9 and 10 tie at 120 and sit across a bucket boundary.
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
-- two orders per customer, amounts t // 2 and t - t // 2 for each total t (loop in the Code block)
```

**SQL answer:** the decile table (`SQL_MAIN`) and the per-customer assignment (`SQL_ASSIGN`), used to check the pandas version.
```sql
WITH t AS (
  SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
), b AS (
  SELECT customer_id, total,
         NTILE(10) OVER (ORDER BY total DESC, customer_id) AS decile
  FROM t
)
SELECT decile, COUNT(*) AS customers, SUM(total) AS revenue,
       ROUND(100.0 * SUM(total) / (SELECT SUM(total) FROM t), 1) AS share_pct
FROM b
GROUP BY decile
ORDER BY decile
```
```sql
SELECT customer_id, SUM(amount) AS total,
       NTILE(10) OVER (ORDER BY SUM(amount) DESC, customer_id) AS decile
FROM orders GROUP BY customer_id ORDER BY customer_id
```

**pandas answer:** reproduce NTILE exactly with arithmetic on the sorted position (first `n mod 10` buckets get one extra row), then group. `pd.qcut` is shown in the Code block and compared.
```python
tot = orders.groupby("customer_id", as_index=False)["amount"].sum().rename(columns={"amount": "total"})
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
n, k = len(tot), 10
q, r = divmod(n, k)                                   # first r buckets get q + 1 rows (NTILE rule)
pos = pd.Series(range(n))
tot["ntile"] = (pos // (q + 1) + 1).where(pos < r * (q + 1), r + (pos - r * (q + 1)) // q + 1).astype(int)
by = tot.groupby("ntile")["total"].agg(customers="size", revenue="sum").reset_index()
by["share_pct"] = (100.0 * by["revenue"] / tot["total"].sum()).round(1)
```

**Example:**
- 23 customers into 10 buckets: 23 = 10 x 2 + 3, so the first three buckets get 3 customers and the rest 2. Sizes: 3, 3, 3, 2, 2, 2, 2, 2, 2, 2.
- Decile 1 is customers 1 to 3: 1000 + 700 + 500 = 2200 of 4440 total, 49.5 percent.
- Decile 2 is customers 4 to 6: 400 + 300 + 250 = 950, 21.4 percent. Decile 10 holds 20 + 25 = 45, 1.0 percent.
- Customers 9 and 10 both have 120. Customer 9 is the last row of bucket 3 and customer 10 the first row of bucket 4: NTILE separated two equal customers, and only the `customer_id` tie-break decided which one landed in the higher bucket.

**Code:** run with `python3 -I`.
```python
# Q49: revenue by decile with NTILE(10)
import sqlite3
import pandas as pd

# 23 customers (ids 1..23); each has two orders that add up to the total listed
TOTALS = [1000, 700, 500, 400, 300, 250, 200, 150, 120, 120, 100, 90, 80, 70, 60, 55, 50, 45, 40, 35, 30, 25, 20]
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
""")
rows, oid = [], 1
for cid, t in enumerate(TOTALS, start=1):
    a = t // 2
    rows += [(oid, cid, a), (oid + 1, cid, t - a)]; oid += 2
con.executemany("INSERT INTO orders VALUES (?,?,?)", rows)

SQL_MAIN = """
WITH t AS (
  SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id
), b AS (
  SELECT customer_id, total,
         NTILE(10) OVER (ORDER BY total DESC, customer_id) AS decile
  FROM t
)
SELECT decile, COUNT(*) AS customers, SUM(total) AS revenue,
       ROUND(100.0 * SUM(total) / (SELECT SUM(total) FROM t), 1) AS share_pct
FROM b
GROUP BY decile
ORDER BY decile
"""
SQL_ASSIGN = """
SELECT customer_id, SUM(amount) AS total,
       NTILE(10) OVER (ORDER BY SUM(amount) DESC, customer_id) AS decile
FROM orders GROUP BY customer_id ORDER BY customer_id
"""
sql = pd.read_sql_query(SQL_MAIN, con)
assign = pd.read_sql_query(SQL_ASSIGN, con)
print(sql.to_string(index=False))
print("customers per decile:", sql["customers"].tolist(), "| total revenue:", int(sql["revenue"].sum()))

orders = pd.read_sql_query("SELECT * FROM orders", con)
# pd:main
tot = orders.groupby("customer_id", as_index=False)["amount"].sum().rename(columns={"amount": "total"})
tot = tot.sort_values(["total", "customer_id"], ascending=[False, True]).reset_index(drop=True)
n, k = len(tot), 10
q, r = divmod(n, k)                                   # first r buckets get q + 1 rows (NTILE rule)
pos = pd.Series(range(n))
tot["ntile"] = (pos // (q + 1) + 1).where(pos < r * (q + 1), r + (pos - r * (q + 1)) // q + 1).astype(int)
by = tot.groupby("ntile")["total"].agg(customers="size", revenue="sum").reset_index()
by["share_pct"] = (100.0 * by["revenue"] / tot["total"].sum()).round(1)
# pd:end
tot_sorted = tot.sort_values("customer_id").reset_index(drop=True)
assert assign["decile"].tolist() == tot_sorted["ntile"].tolist()
assert sql["customers"].tolist() == by["customers"].tolist() and sql["share_pct"].tolist() == by["share_pct"].tolist()
print("\npandas floor arithmetic reproduces NTILE exactly (same decile for all", n, "customers)")

# qcut comparisons
by_value = pd.qcut(tot["total"], 10, labels=False, duplicates="drop")        # 0 = lowest total
by_rank = pd.qcut(tot["total"].rank(method="first", ascending=False), 10, labels=False)  # 0 = top rank
tot["qcut_value"] = 10 - by_value
tot["qcut_rank"] = by_rank + 1
print("\nqcut on total (ties stay together):    sizes", tot["qcut_value"].value_counts().sort_index().tolist())
print("qcut on rank(method='first'):           sizes", tot["qcut_rank"].value_counts().sort_index().tolist())
print("NTILE sizes                           :", sql["customers"].tolist())
print("customers whose qcut-on-rank decile differs from NTILE:", int((tot["qcut_rank"] != tot["ntile"]).sum()))
print("customers whose qcut-on-total decile differs from NTILE:", int((tot["qcut_value"] != tot["ntile"]).sum()))
split = tot[tot["total"] == 120][["customer_id", "total", "ntile", "qcut_value"]]
print("\nthe tied pair (total 120):"); print(split.to_string(index=False))
print("asserts passed")
```

**Output (my run):**
```text
 decile  customers  revenue  share_pct
      1          3     2200       49.5
      2          3      950       21.4
      3          3      470       10.6
      4          2      220        5.0
      5          2      170        3.8
      6          2      130        2.9
      7          2      105        2.4
      8          2       85        1.9
      9          2       65        1.5
     10          2       45        1.0
customers per decile: [3, 3, 3, 2, 2, 2, 2, 2, 2, 2] | total revenue: 4440

pandas floor arithmetic reproduces NTILE exactly (same decile for all 23 customers)

qcut on total (ties stay together):    sizes [3, 2, 2, 1, 3, 3, 2, 2, 2, 3]
qcut on rank(method='first'):           sizes [3, 2, 2, 2, 3, 2, 2, 2, 2, 3]
NTILE sizes                           : [3, 3, 3, 2, 2, 2, 2, 2, 2, 2]
customers whose qcut-on-rank decile differs from NTILE: 10
customers whose qcut-on-total decile differs from NTILE: 11

the tied pair (total 120):
 customer_id  total  ntile  qcut_value
           9    120      3           5
          10    120      4           5
asserts passed
```

**Edge cases:**
- Uneven sizes: with 23 customers the buckets are 3,3,3,2,... NTILE gives the larger buckets to the first (highest-spending) deciles, so the top deciles have slightly more customers and revenue shares are not strictly comparable across deciles.
- Few customers: with fewer than 10 customers I expect NTILE(10) to give each customer a bucket of their own, numbered 1 to n, leaving the higher deciles empty. I did not run that case.
- Ties across a boundary: customers 9 and 10 are in deciles 3 and 4 in SQL and in the same decile under `qcut` on the totals (output: `qcut_value` 5 for both).
- `qcut` versus NTILE: in my run, `qcut` on the totals produced bucket sizes 3, 2, 2, 1, 3, 3, 2, 2, 2, 3 and `qcut` on `rank(method='first')` produced 3, 2, 2, 2, 3, 2, 2, 2, 2, 3. Neither matches NTILE's 3, 3, 3, 2, ..., and 11 of the 23 customers (qcut on totals) or 10 of 23 (qcut on rank) land in a different decile than under NTILE. `qcut` cuts at interpolated quantile values; NTILE counts positions.
- `duplicates='drop'` can reduce the number of buckets when many totals are equal; I used it on the totals as a guard, and no bin was dropped here.

**Then explain:**
- **Pareto reading:** the top decile (3 customers) holds 49.5 percent of revenue and the top three deciles about 81.5 percent (2200 + 950 + 470 = 3620 of 4440), a skewed distribution. This is made-up data; real data would tell its own story.
- **NTILE:** positional, equal-count (to within one) buckets; it ignores ties, so equal customers can land in different deciles. Add a tie-breaker so the split is repeatable.
- **Direction:** NTILE over `total DESC` makes decile 1 the top spenders; over ASC it is the bottom.
- **pandas:** the floor arithmetic reproduces NTILE exactly (asserted); `qcut` is the idiomatic route but gives a different split.

**Follow-ups:**
- *What if customers with no orders should count?* Start from `customers` with a LEFT JOIN and `COALESCE(total, 0)`; they land in the bottom deciles.
- *Cumulative share by decile?* That is a running total, Part 5.
- *Why not 10 equal revenue buckets?* That is a different question (cut by cumulative revenue, not by customer count).

**Common mistakes:**
- Reporting decile shares without saying the buckets are equal in customers, not revenue.
- Forgetting the tie-breaker and getting different bucket members on each run.
- Using `qcut` and assuming it matches NTILE.
- Computing the overall share with a different base (for example orders instead of customers).

### Q50 ⭐ 🔴 Dialect map for ranking and top-N (hedge everything not run on SQLite 3.45): QUALIFY (BigQuery, Snowflake, DuckDB), PostgreSQL DISTINCT ON for one row per group, FETCH FIRST ... WITH TIES, PERCENTILE_CONT / PERCENTILE_DISC, NULLS FIRST / NULLS LAST support, window function support in MySQL 8.0 versus 5.7 (none), IGNORE NULLS on FIRST_VALUE / LAST_VALUE, and the ROW_NUMBER emulation in older engines. Present a table with a 'verified by running on SQLite' column and a 'hedged, not executed' column, and show the CTE emulation of QUALIFY that does run.
**Asked at:** vendor documentation (SQLite window functions page, PostgreSQL window-function tutorial), not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** On SQLite 3.45 I ran what exists (windows, CTE emulations of QUALIFY and DISTINCT ON, NULLS FIRST, a window-free rank) and ran the unsupported syntaxes to capture the errors; everything about PostgreSQL, MySQL, BigQuery, Snowflake, Oracle, DuckDB and SQL Server below is from memory and is labelled "not executed".

**Schema and sample data:** nine employees in three departments. Dept 10: Asha 90, Ben 80, Chitra 80, Dev 70. Dept 20: Esha 60, Farid NULL, Gita 50. Dept 30: Hari NULL, Ila NULL (only NULLs).
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,80),(3,'Chitra',10,80),(4,'Dev',10,70),
  (5,'Esha',20,60),(6,'Farid',20,NULL),(7,'Gita',20,50),(8,'Hari',30,NULL),(9,'Ila',30,NULL);
```

**SQL answer:** the CTE emulation of QUALIFY (`SQL_QUALIFY_EMU`), DISTINCT ON emulation (`SQL_DISTINCT_ON_EMU`), a rank with no window function (`SQL_NO_WINDOW_RANK`) compared with `SQL_WINDOW_RANK`, and NULLS FIRST with its portable emulation (`SQL_NULLS`, `SQL_NULLS_PORTABLE`).
```sql
WITH r AS (
  SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT emp_id, dept_id, salary, rk FROM r WHERE rk <= 2 ORDER BY dept_id, rk, emp_id
```
```sql
WITH r AS (
  SELECT emp_id, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT emp_id, dept_id, salary FROM r WHERE rn = 1 ORDER BY dept_id
```
```sql
SELECT e.emp_id, e.dept_id, e.salary,
       1 + (SELECT COUNT(*) FROM employees x WHERE x.dept_id = e.dept_id AND x.salary > e.salary) AS rk
FROM employees e
WHERE e.salary IS NOT NULL
ORDER BY e.dept_id, rk, e.emp_id
```
```sql
SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
FROM employees WHERE salary IS NOT NULL ORDER BY dept_id, rk, emp_id
```
```sql
SELECT emp_id, salary FROM employees WHERE dept_id = 20 ORDER BY salary DESC NULLS FIRST, emp_id
```
```sql
SELECT emp_id, salary FROM employees WHERE dept_id = 20 ORDER BY (salary IS NULL) DESC, salary DESC, emp_id
```

The dialect map. "Ran on SQLite 3.45.1" means I executed it here (or the error text in the output is from this run). Everything in the right column is from memory and not executed; check the vendor documentation for your version.

| Feature | Ran on SQLite 3.45.1 | Hedged, not executed |
|---|---|---|
| QUALIFY | Syntax error in the run (`near "ROW_NUMBER"`). The CTE emulation ran: `SQL_QUALIFY_EMU` | Exists in BigQuery, Snowflake, DuckDB (and Teradata, Databricks as far as I remember); not in PostgreSQL or MySQL |
| DISTINCT ON | Syntax error in the run (`near "ON"`). ROW_NUMBER = 1 emulation ran: `SQL_DISTINCT_ON_EMU` | PostgreSQL has `SELECT DISTINCT ON (dept_id) ... ORDER BY dept_id, salary DESC`; DuckDB I believe too |
| FETCH FIRST n ROWS WITH TIES | Syntax error in the run (`near "FETCH"`). Emulation: `RANK() <= n` over the whole set (same idea as Q26) | PostgreSQL 13+ and Oracle 12c+ support it; SQL Server has `TOP n WITH TIES`; MySQL has no equivalent |
| PERCENTILE_CONT / PERCENTILE_DISC | Syntax error in the run (`near "("`). Built from ROW_NUMBER/CUME_DIST in Q41 | PostgreSQL, Snowflake, Oracle use `... WITHIN GROUP (ORDER BY x)`; SQL Server and BigQuery have window-style forms; MySQL has none |
| NULLS FIRST / NULLS LAST | Ran: `SQL_NULLS` returned the NULL row first on 3.45.1. The portable `ORDER BY (col IS NULL) DESC, col` form gave the same rows | PostgreSQL and Oracle support the syntax; PostgreSQL treats NULL as larger than any value by default, MySQL as smaller and has no NULLS FIRST/LAST syntax; I did not run them |
| NULL order default in SQLite | Ran: NULLs come first in ASC, last in DESC (NULL acts as the smallest value) | See the row above |
| Window functions in MySQL | Not applicable | MySQL 8.0 added them; 5.7 and earlier have none (hence the user-variable or correlated-count tricks) |
| IGNORE NULLS on FIRST_VALUE / LAST_VALUE | Syntax error in the run (`near "NULLS"`). Emulation: filter NULLs in a CTE then take the first row | Oracle, BigQuery, Snowflake support `IGNORE NULLS`; PostgreSQL did not as far as I know; SQL Server added it in a recent version (I am unsure which) |
| ROW_NUMBER emulation with no windows | Ran: `SQL_NO_WINDOW_RANK` (1 + count of higher values in the group) equals RANK() | MySQL 5.7 era code often used session variables; not recommended, not executed |
| Named windows (`WINDOW w AS`) | Ran in this Code block; extending a named window in OVER (`OVER (w ORDER BY ...)`) works when `w` has no ORDER BY of its own, and fails with `cannot override ORDER BY clause of window: w` when it does | PostgreSQL and MySQL 8 support WINDOW clauses; the extension rules I did not execute |

**pandas answer:** the pandas side of the same features: QUALIFY is a mask on a groupby rank, DISTINCT ON is sort plus `drop_duplicates`, NULLS FIRST is `na_position`, and `groupby().first()` skips NaN, which is `FIRST_VALUE ... IGNORE NULLS`.
```python
clean = emp.dropna(subset=["salary"])
pd_qualify = clean.assign(rk=clean.groupby("dept_id")["salary"].rank(method="min", ascending=False))
pd_qualify = pd_qualify[pd_qualify["rk"] <= 2]                                      # QUALIFY
pd_distinct_on = (clean.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
                       .drop_duplicates("dept_id"))                                 # DISTINCT ON
pd_nulls_first = emp[emp["dept_id"] == 20].sort_values(["salary", "emp_id"], ascending=[False, True], na_position="first")
first_nonnull = emp.groupby("dept_id")["salary"].first()                            # FIRST_VALUE ... IGNORE NULLS
```

**Example:** dept 10: RANK by salary DESC gives Asha 1, Ben 2, Chitra 2, Dev 4, so `rk <= 2` keeps three rows (the tie at 2). Dept 20: after dropping the NULL, Esha 1 and Gita 2. Dept 30: only NULL salaries, filtered out, so the department disappears from the result. DISTINCT ON emulation: Asha for 10 (ROW_NUMBER with emp_id tie-break) and Esha for 20.
- The NULLS FIRST query on dept 20 returns emp 6 (Farid, NULL) first, then Esha 60 and Gita 50.
- First non-NULL salary per department by emp_id: 90 for dept 10, 60 for dept 20 (Farid's NULL skipped), and nothing for dept 30.

**Code:** run with `python3 -I`.
```python
# Q50: dialect map for ranking and top-N: what runs on SQLite 3.45, what is hedged
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES (1,'Asha',10,90),(2,'Ben',10,80),(3,'Chitra',10,80),(4,'Dev',10,70),
  (5,'Esha',20,60),(6,'Farid',20,NULL),(7,'Gita',20,50),(8,'Hari',30,NULL),(9,'Ila',30,NULL);
"""
# the QUALIFY emulation that runs: CTE (or subquery) + WHERE on the window column
SQL_QUALIFY_EMU = """
WITH r AS (
  SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT emp_id, dept_id, salary, rk FROM r WHERE rk <= 2 ORDER BY dept_id, rk, emp_id
"""
# DISTINCT ON (dept_id) emulation: ROW_NUMBER = 1 with a tie-breaker
SQL_DISTINCT_ON_EMU = """
WITH r AS (
  SELECT emp_id, dept_id, salary,
         ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id) AS rn
  FROM employees
  WHERE salary IS NOT NULL
)
SELECT emp_id, dept_id, salary FROM r WHERE rn = 1 ORDER BY dept_id
"""
# no windows at all (MySQL 5.7 era): rank = 1 + number of rows in the same group with a higher value
SQL_NO_WINDOW_RANK = """
SELECT e.emp_id, e.dept_id, e.salary,
       1 + (SELECT COUNT(*) FROM employees x WHERE x.dept_id = e.dept_id AND x.salary > e.salary) AS rk
FROM employees e
WHERE e.salary IS NOT NULL
ORDER BY e.dept_id, rk, e.emp_id
"""
SQL_WINDOW_RANK = """
SELECT emp_id, dept_id, salary, RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) AS rk
FROM employees WHERE salary IS NOT NULL ORDER BY dept_id, rk, emp_id
"""
SQL_NULLS = """
SELECT emp_id, salary FROM employees WHERE dept_id = 20 ORDER BY salary DESC NULLS FIRST, emp_id
"""
SQL_NULLS_PORTABLE = """
SELECT emp_id, salary FROM employees WHERE dept_id = 20 ORDER BY (salary IS NULL) DESC, salary DESC, emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
q = lambda s: pd.read_sql_query(s, con)
print("SQLite", sqlite3.sqlite_version)

qe, de, nw, wr = q(SQL_QUALIFY_EMU), q(SQL_DISTINCT_ON_EMU), q(SQL_NO_WINDOW_RANK), q(SQL_WINDOW_RANK)
print("\nQUALIFY emulation (RANK <= 2 per department, NULL salaries removed):"); print(qe.to_string(index=False))
print("\nDISTINCT ON emulation (one row per department):"); print(de.to_string(index=False))
assert nw.equals(wr)
print("\nrank without any window function (correlated COUNT) equals RANK(): True")
nf = q(SQL_NULLS); npt = q(SQL_NULLS_PORTABLE)
print("\nNULLS FIRST on SQLite 3.45 (dept 20):", nf["emp_id"].tolist(), "| portable IS NULL emulation gives the same:", nf.equals(npt))
assert nf.equals(npt)
print("default SQLite order, ASC puts NULLs first:",
      [r[0] for r in con.execute("SELECT salary FROM employees WHERE dept_id=20 ORDER BY salary")])

print("\nsyntax tried on SQLite 3.45 that is NOT supported (error text from the run):")
tries = {
 "QUALIFY": "SELECT emp_id FROM employees QUALIFY ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary) = 1",
 "DISTINCT ON": "SELECT DISTINCT ON (dept_id) emp_id FROM employees ORDER BY dept_id, salary DESC",
 "FETCH FIRST WITH TIES": "SELECT emp_id FROM employees ORDER BY salary DESC FETCH FIRST 2 ROWS WITH TIES",
 "PERCENTILE_CONT": "SELECT PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY salary) FROM employees",
 "IGNORE NULLS": "SELECT FIRST_VALUE(salary) IGNORE NULLS OVER (PARTITION BY dept_id ORDER BY emp_id) FROM employees",
}
for name, sql in tries.items():
    try:
        con.execute(sql).fetchall(); print(f"  {name}: RAN (unexpected)")
    except sqlite3.Error as e:
        print(f"  {name}: {type(e).__name__}: {e}")

print("\nnamed window extension on SQLite 3.45.1:")
ok = con.execute("SELECT emp_id, ROW_NUMBER() OVER (w ORDER BY emp_id) FROM employees WINDOW w AS (PARTITION BY dept_id) ORDER BY emp_id").fetchall()
print("  OVER (w ORDER BY ...) where w has only PARTITION BY: ran, first rows", ok[:4])
try:
    con.execute("SELECT ROW_NUMBER() OVER (w ORDER BY emp_id) FROM employees WINDOW w AS (PARTITION BY dept_id ORDER BY salary)").fetchall()
except sqlite3.Error as e:
    print("  OVER (w ORDER BY ...) where w already has ORDER BY:", type(e).__name__ + ":", e)

emp = q("SELECT * FROM employees")
# pd:main
clean = emp.dropna(subset=["salary"])
pd_qualify = clean.assign(rk=clean.groupby("dept_id")["salary"].rank(method="min", ascending=False))
pd_qualify = pd_qualify[pd_qualify["rk"] <= 2]                                      # QUALIFY
pd_distinct_on = (clean.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
                       .drop_duplicates("dept_id"))                                 # DISTINCT ON
pd_nulls_first = emp[emp["dept_id"] == 20].sort_values(["salary", "emp_id"], ascending=[False, True], na_position="first")
first_nonnull = emp.groupby("dept_id")["salary"].first()                            # FIRST_VALUE ... IGNORE NULLS
# pd:end
pd.testing.assert_frame_equal(qe[["emp_id", "rk"]], pd_qualify.sort_values(["dept_id", "rk", "emp_id"])[["emp_id", "rk"]].astype(int).reset_index(drop=True), check_dtype=False)
assert de["emp_id"].tolist() == pd_distinct_on["emp_id"].tolist()
assert nf["emp_id"].tolist() == pd_nulls_first["emp_id"].tolist()
ign = con.execute("""SELECT dept_id, salary FROM (SELECT dept_id, salary, ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY emp_id) rn
        FROM employees WHERE salary IS NOT NULL) WHERE rn = 1 ORDER BY dept_id""").fetchall()
print("\nFIRST_VALUE IGNORE NULLS emulated by filtering NULLs first (first non-NULL per dept by emp_id):", ign)
print("pandas groupby first() skips NaN by default:", first_nonnull.to_dict(), "(dept 30 has only NULLs -> NaN)")
assert [r[1] for r in ign] == [first_nonnull[10], first_nonnull[20]]
print("asserts passed")
```

**Output (my run):**
```text
SQLite 3.45.1

QUALIFY emulation (RANK <= 2 per department, NULL salaries removed):
 emp_id  dept_id  salary  rk
      1       10      90   1
      2       10      80   2
      3       10      80   2
      5       20      60   1
      7       20      50   2

DISTINCT ON emulation (one row per department):
 emp_id  dept_id  salary
      1       10      90
      5       20      60

rank without any window function (correlated COUNT) equals RANK(): True

NULLS FIRST on SQLite 3.45 (dept 20): [6, 5, 7] | portable IS NULL emulation gives the same: True
default SQLite order, ASC puts NULLs first: [None, 50, 60]

syntax tried on SQLite 3.45 that is NOT supported (error text from the run):
  QUALIFY: OperationalError: near "ROW_NUMBER": syntax error
  DISTINCT ON: OperationalError: near "ON": syntax error
  FETCH FIRST WITH TIES: OperationalError: near "FETCH": syntax error
  PERCENTILE_CONT: OperationalError: near "(": syntax error
  IGNORE NULLS: OperationalError: near "NULLS": syntax error

named window extension on SQLite 3.45.1:
  OVER (w ORDER BY ...) where w has only PARTITION BY: ran, first rows [(1, 1), (2, 2), (3, 3), (4, 4)]
  OVER (w ORDER BY ...) where w already has ORDER BY: OperationalError: cannot override ORDER BY clause of window: w

FIRST_VALUE IGNORE NULLS emulated by filtering NULLs first (first non-NULL per dept by emp_id): [(10, 90), (20, 60)]
pandas groupby first() skips NaN by default: {10: 90.0, 20: 60.0, 30: nan} (dept 30 has only NULLs -> NaN)
asserts passed
```

**Edge cases:**
- Unsupported syntax gave only a generic syntax error in SQLite (it points at the first unknown word). The error text is not a statement about other engines.
- An all-NULL department vanishes after `WHERE salary IS NOT NULL`; keep it with a LEFT JOIN from a departments table if needed (Q46).
- The portable NULLS emulation sorts by `(col IS NULL)` first. Be careful with the direction (`DESC` on the boolean puts NULLs first).
- `groupby().first()` returns NaN for the all-NaN department, like a NULL.

**Then explain:**
- **Main message:** the CTE (or subquery) plus WHERE on the window column replaces QUALIFY in every engine that has windows; QUALIFY is just shorthand.
- **Per-group top-1:** ROW_NUMBER = 1 with a tie-breaker replaces DISTINCT ON.
- **Ties with a limit:** RANK <= n replaces WITH TIES.
- **Percentiles:** emulate with ROW_NUMBER and COUNT or CUME_DIST (Q41).
- **Always add the caveat:** the right column of the table is memory, not a run.

**Follow-ups:**
- *Which engines can't do windows at all?* MySQL 5.7 and earlier (hedged); use a correlated count as run above.
- *Is the emulation slower than QUALIFY?* On engines that have QUALIFY it is the same plan idea; I did not measure.
- *How do you check your engine's support?* Run a tiny query for each syntax, as the Code block does on SQLite.

**Common mistakes:**
- Writing QUALIFY and being surprised by a syntax error on PostgreSQL, MySQL or SQLite.
- Assuming NULL ordering is the same everywhere.
- Using DISTINCT ON without ORDER BY and expecting a repeatable row.
- Stating dialect facts as verified when they are remembered.
