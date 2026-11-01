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
