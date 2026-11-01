### Q21 ⭐⭐ 🟡 Translating IN and NOT IN subqueries to pandas: customers(customer_id, name, city) and orders(order_id, customer_id, amount) with some NaN customer_id in orders. Write 'customers with total spend over 500' using an aggregated frame, then isin on its index, then map of the aggregated Series onto customers, then a merge. Show what isin does with NaN (NaN matches NaN) versus SQL IN, and why ~isin has no NOT IN trap. State which form keeps customers without orders.
**Asked at:** pandas user guide (groupby transform, dropna) and Comparison with SQL, not a candidate report; analyst and data scientist rounds that mix SQL and pandas
**Say this first (1 line):** `IN (subquery)` becomes `customers[customers.customer_id.isin(...)]` on an aggregated Series' index, `map` gives you the total as a column, and a left merge does the same with a join; pandas `isin` treats NaN as equal to NaN while SQL `IN` never matches NULL, and `~isin` is a plain boolean flip, so it has no NOT IN trap.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Goa');
INSERT INTO orders VALUES (1,1,300),(2,1,250),(3,2,200),(4,2,100),(5,NULL,900),(6,3,50);
```
The NULL customer_id order (900) is the trap: it makes a NULL group that is bigger than 500.

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT customer_id, name, city
FROM customers
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      HAVING SUM(amount) > 500)
ORDER BY customer_id
```
The anti-join twins, `SQL_NOT_IN` and `SQL_NOT_EXISTS`, are in the Code block too.
```sql
SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id
                          FROM orders
                          GROUP BY customer_id
                          HAVING SUM(amount) > 500)
ORDER BY customer_id
```
```sql
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1
                  FROM orders o
                  WHERE o.customer_id = c.customer_id
                  GROUP BY o.customer_id
                  HAVING SUM(o.amount) > 500)
ORDER BY c.customer_id
```

**pandas answer:** three forms of the same subquery, all inside `# pd:main` in the Code block.
```python
agg = orders.groupby("customer_id")["amount"].sum()          # NaN group dropped (dropna=True default)
big = agg[agg > 500]
form_isin = customers[customers["customer_id"].isin(big.index)]
form_map = (customers.assign(total=customers["customer_id"].map(agg))
            .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
form_merge = (customers.merge(agg.rename("total").reset_index(), on="customer_id", how="left")
              .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
```
`agg` plays the role of the subquery: one row per customer, indexed by `customer_id`. The `isin` form is the direct translation of `IN`. The `map` form looks up each customer's total (NaN if none). The merge form joins the same Series back as a column.

**Example:**
- Group totals from the orders table: Asha 300 + 250 = 550, Ben 200 + 100 = 300, Chitra 50, and the NULL-id order 900 forms its own group.
- `HAVING SUM(amount) > 500` keeps Asha (550) and the NULL group (900). The subquery returns the list (1, NULL).
- `customer_id IN (1, NULL)`: Asha matches 1, so true. Ben gives `2 = 1` false and `2 = NULL` unknown, so the result is unknown, which WHERE treats as not true. Result: Asha only.
- pandas: `groupby("customer_id")` silently drops the NaN key, so `agg` has Asha 550, Ben 300, Chitra 50. `big` is Asha only. All three forms return Asha.
- Flip it to NOT IN: the list is (1, NULL), and `2 NOT IN (1, NULL)` is `2 <> 1 AND 2 <> NULL`, true AND unknown = unknown. Every customer is unknown or false, so SQL returns zero rows. pandas `~isin([1])` returns Ben, Chitra and Dev.

**Code:** run with `python3 -I`.
```python
# Q21: IN / NOT IN subqueries translated to pandas (isin, map, merge), with NaN customer_id in orders
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Goa');
INSERT INTO orders VALUES (1,1,300),(2,1,250),(3,2,200),(4,2,100),(5,NULL,900),(6,3,50);
"""
SQL_MAIN = """
SELECT customer_id, name, city
FROM customers
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      HAVING SUM(amount) > 500)
ORDER BY customer_id
"""
SQL_NOT_IN = """
SELECT customer_id, name
FROM customers
WHERE customer_id NOT IN (SELECT customer_id
                          FROM orders
                          GROUP BY customer_id
                          HAVING SUM(amount) > 500)
ORDER BY customer_id
"""
SQL_NOT_EXISTS = """
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (SELECT 1
                  FROM orders o
                  WHERE o.customer_id = c.customer_id
                  GROUP BY o.customer_id
                  HAVING SUM(o.amount) > 500)
ORDER BY c.customer_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("orders customer_id dtype in pandas:", orders["customer_id"].dtype, "| NaN count:", int(orders["customer_id"].isna().sum()))

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("\nSQL IN subquery (customers with total spend > 500):")
print(sql_df.to_string(index=False))
print("SQL group totals incl. the NULL group:", con.execute(
    "SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id ORDER BY customer_id").fetchall())

# pd:main
agg = orders.groupby("customer_id")["amount"].sum()          # NaN group dropped (dropna=True default)
big = agg[agg > 500]
form_isin = customers[customers["customer_id"].isin(big.index)]
form_map = (customers.assign(total=customers["customer_id"].map(agg))
            .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
form_merge = (customers.merge(agg.rename("total").reset_index(), on="customer_id", how="left")
              .loc[lambda d: d["total"] > 500, ["customer_id", "name", "city"]])
# pd:end
for label, f in [("isin", form_isin), ("map", form_map), ("merge(left)", form_merge)]:
    f = f.sort_values("customer_id").reset_index(drop=True)
    pd.testing.assert_frame_equal(sql_df, f, check_dtype=False)
    print(f"pandas form {label}: rows {f['customer_id'].tolist()} == SQL")

print("\nWhich form keeps customers without orders (before filtering)?")
print("  isin: only filters customers, it produces no total column")
print("  map keeps every customer, total is NaN for Dev:", customers.assign(total=customers["customer_id"].map(agg))["total"].tolist())
print("  merge how='left' rows:", len(customers.merge(agg.rename('total').reset_index(), on='customer_id', how='left')),
      "| how='inner' rows:", len(customers.merge(agg.rename('total').reset_index(), on='customer_id', how='inner')))

print("\nNaN handling:")
s = pd.Series([1.0, np.nan, 3.0])
print("  pandas  s.isin([nan]) ->", s.isin([np.nan]).tolist(), "  (NaN matches NaN)")
print("  SQLite  NULL IN (NULL)         ->", con.execute("SELECT NULL IN (NULL)").fetchone()[0])
print("  SQLite  1 NOT IN (2, NULL)     ->", con.execute("SELECT 1 NOT IN (2, NULL)").fetchone()[0])
print("  pandas  ~isin([2, nan]) on [1,nan,3] ->", (~s.isin([2.0, np.nan])).tolist())

print("  empty list: pandas ~isin([]) ->", (~s.isin([])).tolist(), "| SQLite 1 NOT IN (SELECT 1 WHERE 0) ->", con.execute("SELECT 1 NOT IN (SELECT 1 WHERE 0)").fetchone()[0])

not_in = pd.read_sql_query(SQL_NOT_IN, con)
not_ex = pd.read_sql_query(SQL_NOT_EXISTS, con)
print("\nSQL NOT IN over a list that contains the NULL group, rows:", len(not_in))
print("SQL NOT EXISTS, ids:", not_ex["customer_id"].tolist())
pd_not = customers[~customers["customer_id"].isin(big.index)]
print("pandas ~isin, ids:", pd_not["customer_id"].tolist())
# the SQL list was (1, NULL); the pandas list is [1] because groupby dropped NaN, so give pandas the NULL too:
big_with_nan = orders.groupby("customer_id", dropna=False)["amount"].sum()
big_with_nan = big_with_nan[big_with_nan > 500]
print("pandas groupby(dropna=False) list:", big_with_nan.index.tolist(),
      "-> ~isin ids:", customers[~customers["customer_id"].isin(big_with_nan.index)]["customer_id"].tolist())
assert len(not_in) == 0
assert not_ex["customer_id"].tolist() == pd_not["customer_id"].tolist() == [2, 3, 4]
print("\nasserts passed: SQL IN == pandas isin == map == merge (compared after sorting by customer_id)")
```

**Output (my run):**
```text
orders customer_id dtype in pandas: float64 | NaN count: 1

SQL IN subquery (customers with total spend > 500):
 customer_id name city
           1 Asha Pune
SQL group totals incl. the NULL group: [(None, 900), (1, 550), (2, 300), (3, 50)]
pandas form isin: rows [1] == SQL
pandas form map: rows [1] == SQL
pandas form merge(left): rows [1] == SQL

Which form keeps customers without orders (before filtering)?
  isin: only filters customers, it produces no total column
  map keeps every customer, total is NaN for Dev: [550.0, 300.0, 50.0, nan]
  merge how='left' rows: 4 | how='inner' rows: 3

NaN handling:
  pandas  s.isin([nan]) -> [False, True, False]   (NaN matches NaN)
  SQLite  NULL IN (NULL)         -> None
  SQLite  1 NOT IN (2, NULL)     -> None
  pandas  ~isin([2, nan]) on [1,nan,3] -> [True, False, True]
  empty list: pandas ~isin([]) -> [True, True, True] | SQLite 1 NOT IN (SELECT 1 WHERE 0) -> 1

SQL NOT IN over a list that contains the NULL group, rows: 0
SQL NOT EXISTS, ids: [2, 3, 4]
pandas ~isin, ids: [2, 3, 4]
pandas groupby(dropna=False) list: [1.0, nan] -> ~isin ids: [2, 3, 4]

asserts passed: SQL IN == pandas isin == map == merge (compared after sorting by customer_id)
```

**Edge cases:**
- **Which form keeps customers without orders:** `isin` returns a filtered copy of `customers`, so a customer with no orders is simply "not in the list" and dropped by a positive filter. `map` and a `how="left"` merge keep Dev with a NaN total (the printed list shows `nan` for Dev); filtering `total > 500` then drops him because NaN > 500 is False. A `how="inner"` merge drops Dev (3 rows in my run), which is the same hidden loss as an INNER JOIN in SQL.
- **NaN customer_id in orders:** the column becomes `float64` in pandas (1 NaN in my run), so customer ids come back as 1.0, 2.0. `groupby` drops NaN keys by default; `groupby(..., dropna=False)` keeps them (my run shows the index `[1.0, nan]`).
- **isin and NaN:** `Series([1.0, nan, 3.0]).isin([nan])` is `[False, True, False]` in my run. NaN matches NaN. SQL `NULL IN (NULL)` is NULL (it printed `None`).
- **`~isin` has no NOT IN trap:** `~Series([1, nan, 3]).isin([2, nan])` gave `[True, False, True]`. A NaN in the list only removes NaN values; it does not wipe out the whole result. The SQL equivalent, `1 NOT IN (2, NULL)`, printed `None` (unknown).
- **A NaN in the pandas list is not what changes the answer here:** I also ran `groupby(dropna=False)` so the list was `[1.0, nan]`, and `~isin` still returned ids 2, 3, 4 while SQL `NOT IN` returned zero rows.
- **Empty list:** `~isin([])` is all True in pandas, and SQLite `1 NOT IN (empty subquery)` is 1 (true), both printed in my run. An empty list is the one case where SQL NOT IN is safe.

**Then explain:**
- **Subquery as a Series:** the aggregated Series is the "subquery result". Its index is the list of ids, its values are the totals. Filtering the Series (`agg > 500`) is the `HAVING`.
- **Three forms:** `isin` for a yes/no filter (semi-join), `map` when you also need the value as a column, `merge` when you need several columns from the other side or a left/inner choice. `merge(..., validate="many_to_one")` raises if the right side has duplicate keys.
- **NOT IN in pandas:** use `~isin`, or a left merge with `indicator=True` and keep `left_only` (the anti-join). Neither can return nothing because of one missing value.
- **Where pandas differs from SQL:** NaN matches NaN in `isin` and in `merge` keys, while SQL NULL matches nothing. The pandas documentation's SQL comparison page notes that null merge keys match each other.
- In SQL, use `NOT EXISTS` (or filter NULLs inside the subquery) for the anti-join. In my run `NOT EXISTS` returned ids 2, 3, 4.
- Joins and how they differ from subqueries are in Part 2; window-function versions are in Parts 4 and 5.

**Follow-ups:**
- *Why did `groupby` hide the NULL group?* `dropna=True` is the default for group keys, so NaN keys vanish. That helped here, but if the NaN rows matter you must say `dropna=False`.
- *How do I make pandas behave like SQL on NaN?* Drop or mask NaN before `isin` or `merge`, for example `orders.dropna(subset=["customer_id"])`.
- *What about `isin` on a nullable `Int64` column?* I did not run it, so I will not claim how it treats `pd.NA`; test before relying on it.
- *Which engines have the same NOT IN trap?* The NULL rule is standard three-valued logic and the PostgreSQL documentation describes the same NOT IN behaviour, but I only ran SQLite here; other engines are not executed.

**Common mistakes:**
- Using `NOT IN (subquery)` on a nullable column and getting an empty result.
- Assuming `isin` follows SQL rules for NaN.
- Using an inner merge and losing the customers with no orders.
- Forgetting that the NaN-key rows were dropped by `groupby` and then reconciling totals against the orders table (900 is missing from the pandas side).

### Q22 ⭐⭐ 🟡 ANY, SOME and ALL when the engine lacks them (SQLite has none; PostgreSQL and MySQL do): products(product_id, name, category, price). Write 'price greater than ALL prices in Books' and 'price greater than ANY price in Books' as the native syntax (hedged text, not executed) and as the runnable equivalents (> MAX(...), > MIN(...), or NOT EXISTS / EXISTS). Explain what each does when the Books subquery is empty and when it contains NULL prices, and that = ANY is IN and <> ALL is NOT IN.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** `> ALL (subquery)` means greater than every value, so it is `> MAX(...)` only when the subquery has no NULLs and is not empty, and `> ANY` means greater than at least one value, which is `> MIN(...)`; SQLite has neither keyword, so I use the MAX/MIN form with care or the `NOT EXISTS` / `EXISTS` form, which is exact.

**Schema and sample data:**
```sql
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES
 (1,'Atlas','Books',10),(2,'Novel','Books',20),(3,'Cookbook','Books',30),
 (4,'Digest','Mags',15),(5,'Zine','Mags',NULL),
 (6,'Pen','Stationery',5),(7,'Lamp','Home',25),(8,'Chair','Home',40),(9,'Desk','Home',35),
 (10,'Bag','Travel',NULL);
```
Three subqueries to test: Books (clean prices 10, 20, 30), Mags (prices 15 and NULL) and Toys (no such category, so an empty subquery).

**SQL answer:** the native syntax is below; it is hedged text, not executed on SQLite (the Code block shows what SQLite does with it). The runnable forms are in the Code block.
```sql
-- native, PostgreSQL and MySQL (not executed here)
SELECT name FROM products WHERE price > ALL (SELECT price FROM products WHERE category = 'Books');
SELECT name FROM products WHERE price > ANY (SELECT price FROM products WHERE category = 'Books');
```
Runnable equivalents, `?` is the category:
```sql
SELECT product_id FROM products
WHERE price > (SELECT MAX(price) FROM products WHERE category = ?)
ORDER BY product_id
```
```sql
SELECT p.product_id FROM products p
WHERE NOT EXISTS (SELECT 1 FROM products b
                  WHERE b.category = ?
                    AND NOT COALESCE(p.price > b.price, 0))
ORDER BY p.product_id
```
```sql
SELECT product_id FROM products
WHERE price > (SELECT MIN(price) FROM products WHERE category = ?)
ORDER BY product_id
```
```sql
SELECT p.product_id FROM products p
WHERE EXISTS (SELECT 1 FROM products b
              WHERE b.category = ?
                AND p.price > b.price)
ORDER BY p.product_id
```

**pandas answer:** compare each price with every value of the subquery as a 2-D boolean array, then `.all` or `.any` across the subquery axis. NaN comparisons are False, which is exactly SQL's "not true".
```python
def pd_all(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]   # NaN compares False
    return df.loc[cmp.all(axis=1), "product_id"].tolist()            # all() of an empty row is True

def pd_any(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]
    return df.loc[cmp.any(axis=1), "product_id"].tolist()            # any() of an empty row is False
```

**Example:** Books prices are 10, 20, 30.
- `price > ALL`: the price must beat 30. Chair (40) and Desk (35) do. Lamp (25) does not. Result ids 8 and 9. `price > MAX(...)` gives the same.
- `price > ANY`: the price must beat at least one value, so beating 10 is enough. Novel 20, Cookbook 30, Digest 15, Lamp, Chair and Desk qualify (ids 2, 3, 4, 7, 8, 9). Atlas (10) does not beat itself, Pen (5) does not.
- Mags prices are 15 and NULL. `price > ALL (15, NULL)`: the NULL comparison is unknown for every row, so no row can be true. The `NOT EXISTS` form returns nothing. `> MAX(...)` ignores the NULL, uses 15, and returns five rows (ids 2, 3, 7, 8, 9). That is a different answer from the native syntax.
- Toys is empty. `> ALL (empty)` is true for every row, even rows with a NULL price (all ten products). `> MAX(empty)` is `> NULL`, unknown for all, so zero rows. `> ANY (empty)` is false for every row, and `> MIN(empty)` returns zero rows too, so ANY survives an empty set.

**Code:** run with `python3 -I`.
```python
# Q22: ANY / SOME / ALL when SQLite has none: MAX / MIN and EXISTS / NOT EXISTS equivalents
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES
 (1,'Atlas','Books',10),(2,'Novel','Books',20),(3,'Cookbook','Books',30),
 (4,'Digest','Mags',15),(5,'Zine','Mags',NULL),
 (6,'Pen','Stationery',5),(7,'Lamp','Home',25),(8,'Chair','Home',40),(9,'Desk','Home',35),
 (10,'Bag','Travel',NULL);
"""
# native syntax (PostgreSQL / MySQL), NOT executed on SQLite
NATIVE_ALL = "SELECT name FROM products WHERE price > ALL (SELECT price FROM products WHERE category = ?)"
NATIVE_ANY = "SELECT name FROM products WHERE price > ANY (SELECT price FROM products WHERE category = ?)"

SQL_ALL_MAX = """
SELECT product_id FROM products
WHERE price > (SELECT MAX(price) FROM products WHERE category = ?)
ORDER BY product_id
"""
SQL_ALL_NOT_EXISTS = """
SELECT p.product_id FROM products p
WHERE NOT EXISTS (SELECT 1 FROM products b
                  WHERE b.category = ?
                    AND NOT COALESCE(p.price > b.price, 0))
ORDER BY p.product_id
"""
SQL_ANY_MIN = """
SELECT product_id FROM products
WHERE price > (SELECT MIN(price) FROM products WHERE category = ?)
ORDER BY product_id
"""
SQL_ANY_EXISTS = """
SELECT p.product_id FROM products p
WHERE EXISTS (SELECT 1 FROM products b
              WHERE b.category = ?
                AND p.price > b.price)
ORDER BY p.product_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)

for label, sql in [("price > ALL", NATIVE_ALL), ("price > ANY", NATIVE_ANY), ("price > SOME", NATIVE_ANY.replace("ANY", "SOME"))]:
    try:
        con.execute(sql, ("Books",)).fetchall()
        print(label, "-> ran")
    except sqlite3.Error as e:
        print(f"{label} on SQLite -> {type(e).__name__}: {e}")

prices = pd.read_sql_query("SELECT * FROM products", con)
def ids(sql, cat):
    return [r[0] for r in con.execute(sql, (cat,))]

# pd:main
def pd_all(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]   # NaN compares False
    return df.loc[cmp.all(axis=1), "product_id"].tolist()            # all() of an empty row is True

def pd_any(df, cat):
    sub = df.loc[df["category"] == cat, "price"].to_numpy(dtype=float)
    cmp = df["price"].to_numpy(dtype=float)[:, None] > sub[None, :]
    return df.loc[cmp.any(axis=1), "product_id"].tolist()            # any() of an empty row is False
# pd:end

print()
res = {}
for cat, what in [("Books", "clean prices"), ("Mags", "one NULL price"), ("Toys", "empty subquery")]:
    r = (ids(SQL_ALL_MAX, cat), ids(SQL_ALL_NOT_EXISTS, cat), pd_all(prices, cat),
         ids(SQL_ANY_MIN, cat), ids(SQL_ANY_EXISTS, cat), pd_any(prices, cat))
    res[cat] = r
    print(f"{cat:5s} ({what})")
    for name, v in zip(["ALL MAX", "ALL NOT EXISTS", "pandas all", "ANY MIN", "ANY EXISTS", "pandas any"], r):
        print(f"   {name:15s}{v}")

for cat in res:
    mx, ne, pa, mn, ex, pn = res[cat]
    assert ne == pa and ex == pn and mn == ex       # NOT EXISTS / EXISTS forms equal pandas; ANY via MIN always equal
assert res["Books"][0] == res["Books"][1] == [8, 9]
assert res["Mags"][0] != res["Mags"][1] and res["Toys"][0] != res["Toys"][1]
print("\nasserts passed: NOT EXISTS == pandas all, EXISTS == MIN == pandas any; MAX differs from ALL on NULL and empty sets")
```

**Output (my run):**
```text
price > ALL on SQLite -> OperationalError: near "ALL": syntax error
price > ANY on SQLite -> OperationalError: near "SELECT": syntax error
price > SOME on SQLite -> OperationalError: near "SELECT": syntax error

Books (clean prices)
   ALL MAX        [8, 9]
   ALL NOT EXISTS [8, 9]
   pandas all     [8, 9]
   ANY MIN        [2, 3, 4, 7, 8, 9]
   ANY EXISTS     [2, 3, 4, 7, 8, 9]
   pandas any     [2, 3, 4, 7, 8, 9]
Mags  (one NULL price)
   ALL MAX        [2, 3, 7, 8, 9]
   ALL NOT EXISTS []
   pandas all     []
   ANY MIN        [2, 3, 7, 8, 9]
   ANY EXISTS     [2, 3, 7, 8, 9]
   pandas any     [2, 3, 7, 8, 9]
Toys  (empty subquery)
   ALL MAX        []
   ALL NOT EXISTS [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   pandas all     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
   ANY MIN        []
   ANY EXISTS     []
   pandas any     []

asserts passed: NOT EXISTS == pandas all, EXISTS == MIN == pandas any; MAX differs from ALL on NULL and empty sets
```

**Edge cases:**
- **NULLs in the subquery:** `> ALL` is the fragile one. One NULL in the set turns "no row fails" into "some comparison is unknown", and a WHERE clause drops unknown. `> ANY` is not hurt, because one true comparison is enough. My run shows this: Mags gives `[]` for ALL (NOT EXISTS form) but the same five rows as MIN for ANY.
- **Empty subquery:** `> ALL (empty)` is TRUE for every row, `> ANY (empty)` is FALSE. The MAX/MIN rewrites cannot express this, because aggregates over zero rows are NULL (Toys: MAX form returned `[]`, the NOT EXISTS form returned all 10).
- **NULL on the left:** a product with a NULL price (Zine, Bag) fails `> ANY` and `> ALL` against a non-empty set, but passes `> ALL (empty)`. Bag appears in the Toys ALL result.
- **Fixing the MAX form:** add `AND NOT EXISTS (SELECT 1 FROM ... WHERE price IS NULL)` and a guard for the empty case. At that point `NOT EXISTS` is simpler and exact.
- **Ties:** `>` is strict, so a product priced exactly 30 does not beat Books' 30. Use `>= ALL` for "at least as expensive as all".

**Then explain:**
- **Meaning:** `x op ANY (S)` is true if the comparison is true for at least one value in S. `x op ALL (S)` is true if it is true for every value. `SOME` is a synonym for `ANY`.
- **Identities:** `= ANY (S)` is `IN (S)`, and `<> ALL (S)` is `NOT IN (S)`. So `NOT IN` inherits the same NULL trap as `<> ALL`: one NULL in S and no row can pass. I have not run the native forms.
- **Support:** SQLite rejected `ALL`, `ANY` and `SOME` with a syntax error in my run (messages above). PostgreSQL's subquery-expressions page documents `ANY`, `SOME` and `ALL`, with the empty-subquery and NULL rules above; the MySQL subquery-restrictions page lists them as well. Both are hedged, not executed.
- **MySQL restriction:** per its documentation, `ALL`, `ANY` and `SOME` need a scalar left side, and `LIMIT` inside them is not allowed. That is the same restriction as Q28; not executed here.
- **Which rewrite:** use MAX/MIN when you know the set is non-empty and has no NULLs (say so out loud), otherwise `NOT EXISTS` / `EXISTS`.

**Follow-ups:**
- *Is `> ANY` the same as `> MIN`?* Yes, in a WHERE clause: my runs matched on all three scenarios. MIN ignores NULLs, and an empty set gives no rows either way.
- *Why is `x <> ALL (S)` dangerous?* It is `NOT IN`, so a NULL in S gives no rows.
- *How would you write "price equals ANY"?* Just use `IN`.

**Common mistakes:**
- Treating `> ALL` as `> MAX` and getting wrong rows when the subquery is empty or contains NULL.
- Expecting `> ALL (empty)` to return no rows. It returns every row.
- Writing `NOT EXISTS (... WHERE p.price <= b.price)` and forgetting the unknown case when prices are NULL (use `NOT COALESCE(p.price > b.price, 0)` as in the Code block).
- Assuming SQLite supports `ANY`/`ALL` because other engines do.

### Q23 ⭐⭐ 🟡 Subquery versus JOIN: do they always return the same rows? customers(customer_id, name) and orders(order_id, customer_id, amount) with several orders per customer and a NULL customer_id order. Compare SELECT name FROM customers WHERE customer_id IN (SELECT customer_id FROM orders) with the same via JOIN, and NOT IN versus LEFT JOIN ... IS NULL. Show where counts differ (duplicates from the JOIN, the NULL in NOT IN), say when you need DISTINCT, and when a subquery is clearer than a join because you only need a yes or no.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** No, not always: `IN (subquery)` returns each customer once, a JOIN returns one row per matching order (so Asha with 3 orders appears 3 times), and `NOT IN` returns nothing at all when the subquery contains one NULL while `LEFT JOIN ... IS NULL` and `NOT EXISTS` return the right customers.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,1,30),(4,2,40),(5,NULL,50);
```

**SQL answer:** all seven queries are in the Code block. The two pairs:
```sql
SELECT name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders)
ORDER BY name
```
```sql
SELECT c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.name
```
```sql
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY name
```
```sql
SELECT c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.name
```
Also in the Code block: `SQL_JOIN_DISTINCT` (JOIN with DISTINCT), `SQL_NOT_IN_FIXED` (NOT IN with `WHERE customer_id IS NOT NULL` in the subquery) and `SQL_NOT_EXISTS`.

**pandas answer:** `isin` is the subquery form, `merge` the join form, and a left merge with `indicator=True` the anti-join.
```python
pd_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
pd_join = customers.merge(orders, on="customer_id")["name"].sort_values().tolist()
pd_anti = (customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
           .query("_merge == 'left_only'")["name"].sort_values().tolist())
pd_not_isin = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
```

**Example:**
- Orders by customer: Asha 3 rows (10, 20, 30), Ben 1 row (40), one order with a NULL customer_id (50), Chitra and Dev none.
- `IN (SELECT customer_id FROM orders)`: the list is (1, 1, 1, 2, NULL). Asha matches, Ben matches, Chitra gives `3 = 1`, `3 = 2` false and `3 = NULL` unknown, so not true. Result Asha, Ben (2 rows). The NULL in the list is harmless for `IN`.
- `JOIN`: each order matches its customer once. Asha 3 rows, Ben 1 row, the NULL order matches nothing and drops. 4 rows, with Asha repeated. `SELECT DISTINCT` brings it back to 2.
- `NOT IN (1, 1, 1, 2, NULL)`: for Chitra, `3 <> 1 AND 3 <> 2 AND 3 <> NULL` is true AND true AND unknown, which is unknown, so she is dropped. Same for Dev. Zero rows.
- `LEFT JOIN ... WHERE o.order_id IS NULL`: Chitra and Dev have no order row, so the right side is NULL. Result Chitra, Dev. `NOT EXISTS` does the same, and so does `NOT IN` with the NULLs filtered out inside the subquery.

**Code:** run with `python3 -I`.
```python
# Q23: subquery vs JOIN: IN vs JOIN (duplicates) and NOT IN vs LEFT JOIN ... IS NULL (the NULL trap)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev');
INSERT INTO orders VALUES (1,1,10),(2,1,20),(3,1,30),(4,2,40),(5,NULL,50);
"""
SQL_IN = """
SELECT name FROM customers
WHERE customer_id IN (SELECT customer_id FROM orders)
ORDER BY name
"""
SQL_JOIN = """
SELECT c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.name
"""
SQL_JOIN_DISTINCT = """
SELECT DISTINCT c.name FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
ORDER BY c.name
"""
SQL_NOT_IN = """
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders)
ORDER BY name
"""
SQL_NOT_IN_FIXED = """
SELECT name FROM customers
WHERE customer_id NOT IN (SELECT customer_id FROM orders WHERE customer_id IS NOT NULL)
ORDER BY name
"""
SQL_ANTI_JOIN = """
SELECT c.name FROM customers c
LEFT JOIN orders o ON o.customer_id = c.customer_id
WHERE o.order_id IS NULL
ORDER BY c.name
"""
SQL_NOT_EXISTS = """
SELECT c.name FROM customers c
WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)
ORDER BY c.name
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def names(sql):
    return [r[0] for r in con.execute(sql)]
customers = pd.read_sql_query("SELECT * FROM customers", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)

r = {k: names(v) for k, v in [("IN", SQL_IN), ("JOIN", SQL_JOIN), ("JOIN DISTINCT", SQL_JOIN_DISTINCT),
                              ("NOT IN", SQL_NOT_IN), ("NOT IN (NULLs filtered)", SQL_NOT_IN_FIXED),
                              ("LEFT JOIN IS NULL", SQL_ANTI_JOIN), ("NOT EXISTS", SQL_NOT_EXISTS)]}
for k, v in r.items():
    print(f"{k:24s} {len(v)} rows  {v}")

# pd:main
pd_in = customers.loc[customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
pd_join = customers.merge(orders, on="customer_id")["name"].sort_values().tolist()
pd_anti = (customers.merge(orders[["customer_id"]].drop_duplicates(), on="customer_id", how="left", indicator=True)
           .query("_merge == 'left_only'")["name"].sort_values().tolist())
pd_not_isin = customers.loc[~customers["customer_id"].isin(orders["customer_id"]), "name"].sort_values().tolist()
# pd:end
print("\npandas isin          ", pd_in)
print("pandas merge (join)  ", pd_join)
print("pandas anti-join     ", pd_anti)
print("pandas ~isin         ", pd_not_isin)

assert r["IN"] == pd_in == ["Asha", "Ben"]
assert r["JOIN"] == pd_join == ["Asha", "Asha", "Asha", "Ben"]
assert r["JOIN DISTINCT"] == ["Asha", "Ben"]
assert r["NOT IN"] == []
assert r["NOT IN (NULLs filtered)"] == r["LEFT JOIN IS NULL"] == r["NOT EXISTS"] == pd_anti == pd_not_isin == ["Chitra", "Dev"]
print("\nasserts passed: IN == isin (2 rows), JOIN == merge (4 rows with duplicates), NOT IN returns 0 rows, anti-joins return Chitra and Dev")
```

**Output (my run):**
```text
IN                       2 rows  ['Asha', 'Ben']
JOIN                     4 rows  ['Asha', 'Asha', 'Asha', 'Ben']
JOIN DISTINCT            2 rows  ['Asha', 'Ben']
NOT IN                   0 rows  []
NOT IN (NULLs filtered)  2 rows  ['Chitra', 'Dev']
LEFT JOIN IS NULL        2 rows  ['Chitra', 'Dev']
NOT EXISTS               2 rows  ['Chitra', 'Dev']

pandas isin           ['Asha', 'Ben']
pandas merge (join)   ['Asha', 'Asha', 'Asha', 'Ben']
pandas anti-join      ['Chitra', 'Dev']
pandas ~isin          ['Chitra', 'Dev']

asserts passed: IN == isin (2 rows), JOIN == merge (4 rows with duplicates), NOT IN returns 0 rows, anti-joins return Chitra and Dev
```

**Edge cases:**
- **Duplicates from the JOIN:** only the "one-to-many" side multiplies. Joining customers to orders gives 4 rows; a SUM over the joined rows is fine for a per-order measure but wrong for a per-customer measure (Part 2 Q13 has the fan-out case). If you only need the customer once, use `IN`, `EXISTS`, or `DISTINCT`.
- **The NULL order:** an INNER JOIN drops it silently. `IN` ignores it. `NOT IN` is wrecked by it. In pandas, `isin` and `merge` do not treat NaN like SQL (see Q21) but here the customer ids have no NaN, so the results match.
- **Empty subquery:** `NOT IN (empty)` returns every customer, `IN (empty)` none. Only a NULL in the list triggers the trap.
- **Orders pointing to a missing customer:** the JOIN and `IN` ignore them; an anti-join from the orders side would show them.

**Then explain:**
- **When they are the same:** `IN` and `JOIN` match when the subquery side has at most one row per key (a unique key such as a customer id). Here the orders side repeats keys, so they differ.
- **Subquery is clearer** when you only need a yes or no ("has this customer ever ordered?") and no columns from the other table. It also cannot multiply rows, so no DISTINCT is needed.
- **JOIN is needed** when you want columns from the other side (order amount, date), or to aggregate over them.
- **Anti-join:** prefer `NOT EXISTS` or `LEFT JOIN ... IS NULL`. If you keep `NOT IN`, filter NULLs in the subquery or the column must be declared NOT NULL.
- **Performance:** I did not measure it here. Optimisers often turn an `IN` or `EXISTS` subquery into a semi-join, so do not assume a subquery is slower; I have not run EXPLAIN on other engines (not executed). See Part 11 for plans.
- **Test the `IS NULL` check on a non-null column of the right side** (`o.order_id`), not on a column that can be NULL in a matching row.

**Follow-ups:**
- *Which is faster?* Depends on engine and data; look at the plan. Not measured here.
- *How do I get the same 2 rows from the JOIN?* `DISTINCT`, or join to `(SELECT DISTINCT customer_id FROM orders)`.
- *Why not just filter `NOT IN` with `IS NOT NULL`?* You can, I did (`SQL_NOT_IN_FIXED`), but you must remember to do it every time; `NOT EXISTS` is safe by construction.

**Common mistakes:**
- Using `NOT IN` against a nullable column.
- Counting customers with `COUNT(*)` after a one-to-many JOIN.
- Putting the filter on the right table in the `WHERE` of a LEFT JOIN (e.g. `o.amount > 0`), which turns it into an inner join.
- Adding `DISTINCT` to hide a join that should have been a semi-join.

### Q24 ⭐⭐ 🟡 UPDATE with a subquery: customers(customer_id, name, total_spent) and orders(order_id, customer_id, amount). Set total_spent to each customer's order total, with 0 for customers with no orders, using a correlated scalar subquery with COALESCE. Explain what happens without COALESCE (NULL), that SQLite supports this, and the dialect points as hedged text: UPDATE ... FROM in PostgreSQL and SQLite 3.33+, join-update syntax in MySQL, and MySQL error 1093 when the subquery reads the table being updated. Show a before and after check and the pandas map or merge equivalent.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Set the column to a correlated scalar subquery `(SELECT SUM(amount) FROM orders WHERE orders.customer_id = customers.customer_id)` wrapped in `COALESCE(..., 0)`, because a customer with no orders gets a NULL sum, and without the COALESCE you overwrite their total with NULL.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, total_spent INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha',999),(2,'Ben',NULL),(3,'Chitra',NULL),(4,'Dev',77),(5,'Esha',NULL);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,200),(4,5,NULL);
```
Asha and Dev start with stale totals (999 and 77), so you can see which updates overwrite them. Esha has one order whose amount is NULL.

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
UPDATE customers
SET total_spent = COALESCE((SELECT SUM(o.amount)
                            FROM orders o
                            WHERE o.customer_id = customers.customer_id), 0)
```
Variants, all executed in the Code block, each on a fresh copy of the data: the same without COALESCE,
```sql
UPDATE customers
SET total_spent = (SELECT SUM(o.amount)
                   FROM orders o
                   WHERE o.customer_id = customers.customer_id)
```
`UPDATE ... FROM` (SQLite 3.33 and later; it ran on the 3.45.1 used here),
```sql
UPDATE customers
SET total_spent = t.s
FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) AS t
WHERE customers.customer_id = t.customer_id
```
and a CTE before the UPDATE.
```sql
WITH t AS (SELECT customer_id, COALESCE(SUM(amount), 0) AS s FROM orders GROUP BY customer_id)
UPDATE customers
SET total_spent = COALESCE((SELECT s FROM t WHERE t.customer_id = customers.customer_id), 0)
```

**pandas answer:** aggregate once, `map` the Series onto the customer ids, fill the gaps with 0.
```python
totals = orders.groupby("customer_id")["amount"].sum()                 # all-NaN group sums to 0.0 by default
pd_df = cust.assign(total_spent=cust["customer_id"].map(totals).fillna(0).astype("int64"))
```

**Example:**
- Order totals: Asha 100 + 50 = 150, Ben 200, Esha only has a NULL amount (SUM of only NULLs is NULL), Chitra and Dev have no orders (subquery returns no row, so the scalar subquery is NULL).
- Before: Asha 999, Ben NULL, Chitra NULL, Dev 77, Esha NULL.
- With COALESCE: Asha 150, Ben 200, Chitra 0, Dev 0, Esha 0. Five rows updated. Dev's stale 77 is correctly reset to 0.
- Without COALESCE: Asha 150, Ben 200, and Chitra, Dev, Esha all NULL (printed `NaN` by pandas).
- `UPDATE ... FROM` joins to the per-customer aggregate, so it touches only customers that have order rows (3 rows: Asha, Ben, Esha). Chitra stays NULL and Dev keeps the stale 77. Esha is updated to NULL because her SUM is NULL.
- Check: the updated column adds to 350 and so does `SUM(amount)` on the orders table (assert in the Code block).

**Code:** run with `python3 -I`.
```python
# Q24: UPDATE with a correlated scalar subquery (COALESCE), UPDATE ... FROM, WITH before UPDATE, pandas map
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, total_spent INTEGER);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha',999),(2,'Ben',NULL),(3,'Chitra',NULL),(4,'Dev',77),(5,'Esha',NULL);
INSERT INTO orders VALUES (1,1,100),(2,1,50),(3,2,200),(4,5,NULL);
"""
SQL_MAIN = """
UPDATE customers
SET total_spent = COALESCE((SELECT SUM(o.amount)
                            FROM orders o
                            WHERE o.customer_id = customers.customer_id), 0)
"""
SQL_NO_COALESCE = """
UPDATE customers
SET total_spent = (SELECT SUM(o.amount)
                   FROM orders o
                   WHERE o.customer_id = customers.customer_id)
"""
SQL_UPDATE_FROM = """
UPDATE customers
SET total_spent = t.s
FROM (SELECT customer_id, SUM(amount) AS s FROM orders GROUP BY customer_id) AS t
WHERE customers.customer_id = t.customer_id
"""
SQL_WITH_UPDATE = """
WITH t AS (SELECT customer_id, COALESCE(SUM(amount), 0) AS s FROM orders GROUP BY customer_id)
UPDATE customers
SET total_spent = COALESCE((SELECT s FROM t WHERE t.customer_id = customers.customer_id), 0)
"""
CHECK = "SELECT customer_id, name, total_spent FROM customers ORDER BY customer_id"

def fresh():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c
BASE = fresh().total_changes                   # rows inserted by the setup script
def run(sql):
    c = fresh()
    c.execute(sql)
    return c, c.total_changes - BASE     # rowcount is -1 for a statement that starts with WITH
def table(c):
    return pd.read_sql_query(CHECK, c)

con = fresh()
before = table(con)
print("BEFORE (stale values 999 and 77, NULLs elsewhere):")
print(before.to_string(index=False))
print("check query, orders per customer:", con.execute(
    "SELECT customer_id, SUM(amount), COUNT(*) FROM orders GROUP BY customer_id").fetchall())

c_main, n_main = run(SQL_MAIN)
c_nc, n_nc = run(SQL_NO_COALESCE)
c_from, n_from = run(SQL_UPDATE_FROM)
c_with, n_with = run(SQL_WITH_UPDATE)
sql_df = table(c_main)
print(f"\nAFTER SQL_MAIN (correlated subquery + COALESCE), rows updated: {n_main}")
print(sql_df.to_string(index=False))
print(f"\nAFTER SQL_NO_COALESCE, rows updated: {n_nc}")
print(table(c_nc).to_string(index=False))
print(f"\nAFTER SQL_UPDATE_FROM (SQLite 3.45), rows updated: {n_from}")
print(table(c_from).to_string(index=False))
print(f"\nAFTER SQL_WITH_UPDATE, rows updated: {n_with}")
print(table(c_with).to_string(index=False))

orders = pd.read_sql_query("SELECT * FROM orders", con)
cust = before.copy()
# pd:main
totals = orders.groupby("customer_id")["amount"].sum()                 # all-NaN group sums to 0.0 by default
pd_df = cust.assign(total_spent=cust["customer_id"].map(totals).fillna(0).astype("int64"))
# pd:end
print("\npandas map + fillna(0):")
print(pd_df.to_string(index=False))
strict = orders.groupby("customer_id")["amount"].sum(min_count=1)
print("pandas sum() of Esha's only (NaN) order:", totals.loc[5], "| with min_count=1:", strict.loc[5])

# compared by customer_id, same order
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
pd.testing.assert_frame_equal(sql_df, table(c_with), check_dtype=False)
assert table(c_nc)["total_spent"].isna().tolist() == [False, False, True, True, True]
assert table(c_from)["total_spent"].fillna(-1).tolist() == [150, 200, -1, 77, -1]
assert orders["amount"].sum() == sql_df["total_spent"].sum() == 350
print("\nasserts passed: SQL == pandas == WITH variant; UPDATE ... FROM leaves unmatched customers untouched; totals tie to orders (350)")
```

**Output (my run):**
```text
BEFORE (stale values 999 and 77, NULLs elsewhere):
 customer_id   name  total_spent
           1   Asha        999.0
           2    Ben          NaN
           3 Chitra          NaN
           4    Dev         77.0
           5   Esha          NaN
check query, orders per customer: [(1, 150, 2), (2, 200, 1), (5, None, 1)]

AFTER SQL_MAIN (correlated subquery + COALESCE), rows updated: 5
 customer_id   name  total_spent
           1   Asha          150
           2    Ben          200
           3 Chitra            0
           4    Dev            0
           5   Esha            0

AFTER SQL_NO_COALESCE, rows updated: 5
 customer_id   name  total_spent
           1   Asha        150.0
           2    Ben        200.0
           3 Chitra          NaN
           4    Dev          NaN
           5   Esha          NaN

AFTER SQL_UPDATE_FROM (SQLite 3.45), rows updated: 3
 customer_id   name  total_spent
           1   Asha        150.0
           2    Ben        200.0
           3 Chitra          NaN
           4    Dev         77.0
           5   Esha          NaN

AFTER SQL_WITH_UPDATE, rows updated: 5
 customer_id   name  total_spent
           1   Asha          150
           2    Ben          200
           3 Chitra            0
           4    Dev            0
           5   Esha            0

pandas map + fillna(0):
 customer_id   name  total_spent
           1   Asha          150
           2    Ben          200
           3 Chitra            0
           4    Dev            0
           5   Esha            0
pandas sum() of Esha's only (NaN) order: 0.0 | with min_count=1: nan

asserts passed: SQL == pandas == WITH variant; UPDATE ... FROM leaves unmatched customers untouched; totals tie to orders (350)
```

**Edge cases:**
- **No orders:** the correlated subquery returns no rows, and a scalar subquery with no rows is NULL. `COALESCE(..., 0)` turns that into 0. The stale 77 on Dev shows the difference between "update everyone" and "update only matched customers".
- **NULL amounts:** Esha's `SUM(NULL)` is NULL, so even a customer who has an order can get NULL; the COALESCE covers both. pandas differs: `sum()` of an all-NaN group is 0.0 by default and NaN only with `min_count=1` (both printed in my run). So the pandas `map` result needs no `fillna` for Esha, only for customers missing from the Series.
- **Row count:** the Python `sqlite3` module reports `rowcount = -1` for a statement that starts with `WITH`, so I counted changes with `total_changes` instead.
- **Many orders per customer:** the subquery aggregates inside, so there is still one value per customer. An unaggregated subquery returning several rows would silently take the first row in SQLite (see Q26).
- **Run it as a transaction:** wrap the UPDATE in a transaction and check the before/after counts first when doing it on real data (`BEGIN; UPDATE ...; check; COMMIT`).

**Then explain:**
- **Correlated:** the inner query refers to the outer row (`customers.customer_id`), so it runs per customer. For an UPDATE the outer row is the row being updated.
- **Why COALESCE:** an UPDATE assigns whatever the subquery returns, NULL included. Decide whether "no orders" should be 0 or NULL and write it down.
- **Dialect points (not executed here):** PostgreSQL supports `UPDATE ... SET ... FROM ... WHERE`, the same shape as my SQLite 3.45 run. MySQL uses a join in the UPDATE (`UPDATE customers c LEFT JOIN (SELECT ...) t ON ... SET c.total_spent = COALESCE(t.s, 0)`). The MySQL documentation says you cannot modify a table and select from the same table in a subquery; that is error 1093 (the number is from memory, not on the page I read), and the workaround is to wrap the subquery in a derived table. Not executed here. SQLite allowed the subquery here because the subquery reads `orders`, not `customers` (Q25 shows the same-table case).
- **LEFT JOIN update:** `UPDATE ... FROM` with an inner join skips unmatched rows. To reset the unmatched ones you need the COALESCE form, a second UPDATE, or a LEFT JOIN where the dialect allows it.
- **CTE before UPDATE:** SQLite accepted `WITH ... UPDATE` in my run.

**Follow-ups:**
- *How would you make it safe to rerun?* The statement is idempotent: running it twice gives the same totals, because it recomputes from orders.
- *Is it slow?* It runs one aggregate per customer; with an index on `orders(customer_id)` that is a lookup. I did not time it here.
- *Why not store the total at all?* A stored total goes stale as orders change; a view or query computes it fresh. If you must store it, rebuild it on a schedule or maintain it with a trigger.

**Common mistakes:**
- Forgetting COALESCE and wiping totals to NULL.
- Using `UPDATE ... FROM` with an inner join and leaving stale values on unmatched rows.
- Assuming pandas and SQL agree on a sum of only NULLs (0.0 versus NULL).
- Running the UPDATE without a before/after count check.

### Q25 ⭐⭐ 🟡 DELETE with a subquery: employees(emp_id, name, email) has duplicate rows for the same email. Delete the duplicates keeping the row with the smallest emp_id using DELETE FROM employees WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email), and a NOT EXISTS / correlated version. Explain the NULL-email risk, the NOT IN with NULL id risk, that SQLite allows a subquery on the same table while MySQL raises error 1093 (hedged; workaround is a derived table), and the pandas drop_duplicates(keep='first').
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Keep the smallest `emp_id` per email and delete the rest with `DELETE FROM employees WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email)`, but know that `GROUP BY` puts all NULL emails in one group (so NULL-email rows get "deduplicated" too) and that a NULL in the id list would make NOT IN delete nothing; `NOT EXISTS` with an earlier row of the same email avoids both.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO employees VALUES
 (1,'Asha','a@x.com'),(2,'Asha R','a@x.com'),
 (3,'Ben','b@x.com'),(4,'Ben K','b@x.com'),(5,'Ben K2','b@x.com'),
 (6,'Chitra','c@x.com'),
 (7,'Dev',NULL),(8,'Eve',NULL);
```
The Code block also builds a second table, `emp_loose(emp_id INTEGER, email TEXT)`, with no primary key and two NULL ids, for the NULL-id risk.

**SQL answer:** all in the Code block. The question's version:
```sql
DELETE FROM employees
WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email)
```
The correlated NOT EXISTS-style version (delete a row if an earlier row has the same email):
```sql
DELETE FROM employees
WHERE EXISTS (SELECT 1 FROM employees e2
              WHERE e2.email = employees.email
                AND e2.emp_id < employees.emp_id)
```
The same NOT IN with a CTE in front of DELETE (it ran on SQLite 3.45):
```sql
WITH keep AS (SELECT MIN(emp_id) AS id FROM employees GROUP BY email)
DELETE FROM employees WHERE emp_id NOT IN (SELECT id FROM keep)
```

**pandas answer:** sort by `emp_id` and keep the first row per email.
```python
dedup_all = emp.sort_values("emp_id").drop_duplicates(subset="email", keep="first")        # NaN emails count as equal
dedup_sql_exists = emp[emp["email"].isna() | ~emp.duplicated(subset="email", keep="first")]  # NULL emails never match
```
`dedup_all` is the NOT IN result. `dedup_sql_exists` keeps every NULL-email row, which is what the correlated version does.

**Example:**
- Groups by email: a@x.com has ids 1, 2 (min 1); b@x.com has 3, 4, 5 (min 3); c@x.com has id 6 (min 6); the NULL group has ids 7, 8 (min 7).
- `NOT IN (1, 3, 6, 7)` deletes ids 2, 4, 5, 8: four rows. Kept 1, 3, 6, 7.
- The NOT EXISTS version looks for an earlier row with the same email: id 2 has id 1 (delete), ids 4 and 5 have id 3 (delete), id 8 has no match because `NULL = NULL` is not true, so it stays. Three rows deleted, kept 1, 3, 6, 7, 8.
- So the two are not the same whenever emails can be NULL: GROUP BY treats NULLs as one group, equality does not. Whether Dev and Eve are duplicates is a business decision; neither query asks it.
- pandas `drop_duplicates(subset="email")` treats NaN as equal to NaN, so it matches the NOT IN result, ids 1, 3, 6, 7.

**Code:** run with `python3 -I`.
```python
# Q25: DELETE duplicates with a subquery on the same table: NOT IN vs NOT EXISTS, NULL email, NULL id
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, email TEXT);
INSERT INTO employees VALUES
 (1,'Asha','a@x.com'),(2,'Asha R','a@x.com'),
 (3,'Ben','b@x.com'),(4,'Ben K','b@x.com'),(5,'Ben K2','b@x.com'),
 (6,'Chitra','c@x.com'),
 (7,'Dev',NULL),(8,'Eve',NULL);
CREATE TABLE emp_loose(emp_id INTEGER, email TEXT);
INSERT INTO emp_loose VALUES (1,'a@x.com'),(2,'a@x.com'),(NULL,'b@x.com'),(NULL,'b@x.com'),(5,'c@x.com');
"""
SQL_NOT_IN = """
DELETE FROM employees
WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM employees GROUP BY email)
"""
SQL_NOT_EXISTS = """
DELETE FROM employees
WHERE EXISTS (SELECT 1 FROM employees e2
              WHERE e2.email = employees.email
                AND e2.emp_id < employees.emp_id)
"""
SQL_WITH_DELETE = """
WITH keep AS (SELECT MIN(emp_id) AS id FROM employees GROUP BY email)
DELETE FROM employees WHERE emp_id NOT IN (SELECT id FROM keep)
"""
SQL_LOOSE_NOT_IN = """
DELETE FROM emp_loose
WHERE emp_id NOT IN (SELECT MIN(emp_id) FROM emp_loose GROUP BY email)
"""
SQL_LOOSE_NOT_EXISTS = """
DELETE FROM emp_loose
WHERE NOT EXISTS (SELECT 1 FROM (SELECT MIN(emp_id) AS m FROM emp_loose GROUP BY email) k
                  WHERE k.m = emp_loose.emp_id)
"""
def fresh():
    c = sqlite3.connect(":memory:")
    c.executescript(SCHEMA)
    return c
BASE = fresh().total_changes          # rows inserted by the setup script
def run(sql, tbl="employees"):
    c = fresh()
    c.execute(sql)
    rows = c.execute(f"SELECT * FROM {tbl} ORDER BY emp_id").fetchall()
    return rows, c.total_changes - BASE

con = fresh()
emp = pd.read_sql_query("SELECT * FROM employees ORDER BY emp_id", con)
print("before:", len(emp), "rows")
rows_in, n_in = run(SQL_NOT_IN)
rows_ex, n_ex = run(SQL_NOT_EXISTS)
rows_with, n_with = run(SQL_WITH_DELETE)
print("\nNOT IN (MIN(emp_id) ... GROUP BY email):  deleted", n_in, "kept ids", [r[0] for r in rows_in])
print("NOT EXISTS (earlier row, same email):     deleted", n_ex, "kept ids", [r[0] for r in rows_ex])
print("WITH keep AS (...) DELETE ... NOT IN:      deleted", n_with, "kept ids", [r[0] for r in rows_with])

# pd:main
dedup_all = emp.sort_values("emp_id").drop_duplicates(subset="email", keep="first")        # NaN emails count as equal
dedup_sql_exists = emp[emp["email"].isna() | ~emp.duplicated(subset="email", keep="first")]  # NULL emails never match
# pd:end
print("\npandas drop_duplicates(subset='email', keep='first') ids:", dedup_all["emp_id"].tolist())
print("pandas NULL emails kept (like NOT EXISTS) ids:           ", dedup_sql_exists["emp_id"].tolist())

loose_in, _ = run(SQL_LOOSE_NOT_IN, "emp_loose")
loose_ex, _ = run(SQL_LOOSE_NOT_EXISTS, "emp_loose")
print("\nemp_loose has NULL emp_id rows (no primary key). Before: 5 rows")
print("  NOT IN with a NULL in the list, rows left:", len(loose_in), loose_in)
print("  NOT EXISTS form, rows left:               ", len(loose_ex), loose_ex)

assert [r[0] for r in rows_in] == [r[0] for r in rows_with] == dedup_all["emp_id"].tolist() == [1, 3, 6, 7]
assert [r[0] for r in rows_ex] == dedup_sql_exists["emp_id"].tolist() == [1, 3, 6, 7, 8]
assert len(loose_in) == 5
print("\nasserts passed: NOT IN == WITH variant == drop_duplicates (ids 1,3,6,7); NOT EXISTS == pandas with NULL emails kept (ids 1,3,6,7,8); compared as lists of emp_id sorted ascending")
```

**Output (my run):**
```text
before: 8 rows

NOT IN (MIN(emp_id) ... GROUP BY email):  deleted 4 kept ids [1, 3, 6, 7]
NOT EXISTS (earlier row, same email):     deleted 3 kept ids [1, 3, 6, 7, 8]
WITH keep AS (...) DELETE ... NOT IN:      deleted 4 kept ids [1, 3, 6, 7]

pandas drop_duplicates(subset='email', keep='first') ids: [1, 3, 6, 7]
pandas NULL emails kept (like NOT EXISTS) ids:            [1, 3, 6, 7, 8]

emp_loose has NULL emp_id rows (no primary key). Before: 5 rows
  NOT IN with a NULL in the list, rows left: 5 [(None, 'b@x.com'), (None, 'b@x.com'), (1, 'a@x.com'), (2, 'a@x.com'), (5, 'c@x.com')]
  NOT EXISTS form, rows left:                2 [(1, 'a@x.com'), (5, 'c@x.com')]

asserts passed: NOT IN == WITH variant == drop_duplicates (ids 1,3,6,7); NOT EXISTS == pandas with NULL emails kept (ids 1,3,6,7,8); compared as lists of emp_id sorted ascending
```

**Edge cases:**
- **NULL email:** covered above. Decide whether rows with no email are duplicates. If not, exclude them: `WHERE email IS NOT NULL` in the subquery and keep NULL-email rows with `OR email IS NULL`, or use the NOT EXISTS form.
- **NULL emp_id risk:** if the id column can be NULL (my `emp_loose` table has no primary key), a group whose ids are all NULL has `MIN` equal to NULL, so the NOT IN list contains a NULL and no row can pass `NOT IN`. In my run nothing was deleted (5 rows left, the duplicate id 2 included). The `NOT EXISTS`-against-the-keep-list form deleted both NULL-id rows and left 2 rows. Neither is right, so dedupe on a real, non-null key, and keep the primary key.
- **Ties:** `MIN(emp_id)` is unique per group only because `emp_id` is unique. If the key repeats, you keep several rows per group.
- **Rows deleted count:** `SELECT COUNT(*) FROM employees` before and after (8 to 4 for NOT IN, 8 to 5 for NOT EXISTS here).
- **Case and spaces:** `A@x.com` and `a@x.com ` are different strings, so normalise with `LOWER(TRIM(email))` first if that matters. I did not run that here.

**Then explain:**
- **Why it works:** the subquery returns the one id to keep for each email; every other id is deleted. The subquery runs once (it is not correlated), and the result list is checked per row.
- **Same-table subquery:** SQLite let me delete from `employees` while selecting from it. MySQL does not (error 1093, number from memory; the MySQL documentation says you cannot modify and select from the same table in a subquery). The workaround is a derived table around the inner query, for example `NOT IN (SELECT id FROM (SELECT MIN(emp_id) AS id FROM employees GROUP BY email) k)`. Not executed here. PostgreSQL's behaviour for this statement I did not run.
- **Check before deleting:** run the same subquery as a SELECT (`SELECT * FROM employees WHERE emp_id NOT IN (...)`) first, then wrap the DELETE in a transaction.
- **pandas:** `keep='first'` after sorting keeps the smallest id. `keep='last'` keeps the largest, `keep=False` drops every duplicated row.
- A window-function version (ROW_NUMBER, then delete rows numbered above 1) is in Part 4.

**Follow-ups:**
- *Why not `DELETE ... JOIN`?* Join-delete syntax is not standard SQL and differs by engine (MySQL has `DELETE e1 FROM ... JOIN`); not executed here.
- *How do I keep the newest instead?* Use `MAX(emp_id)` (or the latest date).
- *How do I stop it happening again?* A `UNIQUE` constraint on the email column; NULLs are allowed multiple times under UNIQUE in most engines (I did not run that here).

**Common mistakes:**
- Using `NOT IN` where the subquery can return NULL.
- Not thinking about NULL emails and silently deleting rows that were never real duplicates.
- Running the DELETE without previewing it as a SELECT and without a transaction.
- Using `MIN(name)` or another non-key column to choose the keeper.

### Q26 ⭐⭐ 🟡 The max-per-group tie problem: employees(emp_id, name, dept_id, salary). Return the highest-paid employee in each department, and all of them when there is a tie. Solve it by joining to a derived table of MAX(salary) per department, and with a correlated subquery, and show that a LIMIT 1 per group or a GROUP BY with a bare column gives one arbitrary row. Explain the tie behaviour, the pandas transform('max') mask versus idxmax, and the pointer to the window version in Part 4.
**Asked at:** public LeetCode-style problem bank (Customers Who Bought All Products, Nth Highest Salary, Department Highest Salary; known only from list snippets), not a candidate report; analyst and data scientist screens
**Say this first (1 line):** To keep ties, find each department's MAX(salary) first and match every employee against it, either by joining to a derived table of those maxima or with a correlated `salary = (SELECT MAX(...) ... same dept)`; `LIMIT 1` per group or a bare column under `GROUP BY` returns exactly one row, so a tie is cut down to one arbitrary person.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
 (4,'Dev',20,80),
 (5,'Eve',30,60),(6,'Farid',30,50),
 (7,'Hari',40,NULL),
 (8,'Ivy',NULL,95);
```
Department 10 has a tie at 90. Hari's salary is NULL. Ivy has no department.

**SQL answer:** `SQL_MAIN` (derived-table join) in the Code block.
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, MAX(salary) AS max_salary
      FROM employees
      GROUP BY dept_id) m
  ON m.dept_id = e.dept_id AND m.max_salary = e.salary
ORDER BY e.dept_id, e.emp_id
```
The correlated version:
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary = (SELECT MAX(e2.salary)
                  FROM employees e2
                  WHERE e2.dept_id = e.dept_id)
ORDER BY e.dept_id, e.emp_id
```
The two wrong-by-design forms, for contrast. A `LIMIT 1` per group:
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.emp_id = (SELECT e2.emp_id FROM employees e2
                  WHERE e2.dept_id = e.dept_id
                  ORDER BY e2.salary DESC LIMIT 1)
ORDER BY e.dept_id
```
And a bare column under `GROUP BY`:
```sql
SELECT dept_id, name, MAX(salary) AS max_salary
FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id
ORDER BY dept_id
```
The Code block also has `SQL_NOT_EXISTS` ("nobody in my department earns more").

**pandas answer:** a mask against the per-group max keeps all ties; `idxmax` keeps one row per group.
```python
mask = emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")
pd_df = emp[mask].sort_values(["dept_id", "emp_id"]).reset_index(drop=True)
idx_df = emp.dropna(subset=["salary", "dept_id"]).loc[lambda d: d.groupby("dept_id")["salary"].idxmax()]
```

**Example:**
- Department maxima: 10 gives 90, 20 gives 80, 30 gives 60, 40 gives NULL (its only salary is NULL), and the NULL department forms one group with max 95.
- Join: Asha (10, 90) matches 90, Ben (10, 90) matches 90, Chitra (70) does not. Dev matches 80. Eve matches 60, Farid does not. So the result is Asha, Ben, Dev, Eve (ids 1, 2, 4, 5). The tie in department 10 produces two rows.
- Hari: `m.max_salary = e.salary` is `NULL = NULL`, not true, so he is dropped. Ivy: `m.dept_id = e.dept_id` is `NULL = NULL`, also dropped.
- Correlated: for Asha the inner query returns 90, equal, kept. For Ivy the inner `e2.dept_id = NULL` matches no row, the scalar subquery is NULL, `95 = NULL` is not true, dropped. Same result, ids 1, 2, 4, 5.
- `LIMIT 1` per group: each department yields one `emp_id`; in my run department 10 returned Asha and not Ben. Ben is simply cut, and nothing in the SQL says why Asha won.
- pandas: `transform("max")` writes the department maximum on every row (90, 90, 90, 80, 60, 60, NaN, NaN; the NaN key and the all-NaN department both give NaN), and `salary == max` is False for NaN rows. Mask gives ids 1, 2, 4, 5, same as SQL.

**Code:** run with `python3 -I`.
```python
# Q26: highest-paid employee per department, ties included: derived-table join vs correlated subquery
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),
 (4,'Dev',20,80),
 (5,'Eve',30,60),(6,'Farid',30,50),
 (7,'Hari',40,NULL),
 (8,'Ivy',NULL,95);
"""
SQL_MAIN = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
JOIN (SELECT dept_id, MAX(salary) AS max_salary
      FROM employees
      GROUP BY dept_id) m
  ON m.dept_id = e.dept_id AND m.max_salary = e.salary
ORDER BY e.dept_id, e.emp_id
"""
SQL_CORRELATED = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.salary = (SELECT MAX(e2.salary)
                  FROM employees e2
                  WHERE e2.dept_id = e.dept_id)
ORDER BY e.dept_id, e.emp_id
"""
SQL_NOT_EXISTS = """
SELECT e.emp_id FROM employees e
WHERE NOT EXISTS (SELECT 1 FROM employees e2
                  WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary)
ORDER BY e.emp_id
"""
SQL_LIMIT1 = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE e.emp_id = (SELECT e2.emp_id FROM employees e2
                  WHERE e2.dept_id = e.dept_id
                  ORDER BY e2.salary DESC LIMIT 1)
ORDER BY e.dept_id
"""
SQL_BARE = """
SELECT dept_id, name, MAX(salary) AS max_salary
FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id
ORDER BY dept_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
emp = pd.read_sql_query("SELECT * FROM employees", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
corr_df = pd.read_sql_query(SQL_CORRELATED, con)
print("derived-table join (ties kept):")
print(sql_df.to_string(index=False))
print("correlated subquery ids:", corr_df["emp_id"].tolist())
print("NOT EXISTS (nobody earns more) ids:", [r[0] for r in con.execute(SQL_NOT_EXISTS)])
print("\nLIMIT 1 per group (no tie-break) -> one row per department:")
print(pd.read_sql_query(SQL_LIMIT1, con).to_string(index=False))
print("\nGROUP BY dept_id with bare column `name` next to MAX(salary) (SQLite only):")
print(pd.read_sql_query(SQL_BARE, con).to_string(index=False))

print("\nFROM-subquery without an alias:", con.execute(
    "SELECT MAX(m) FROM (SELECT MAX(salary) AS m FROM employees GROUP BY dept_id)").fetchall())
print("scalar subquery returning many rows (dept 10, ORDER BY salary ASC / DESC):",
      con.execute("SELECT (SELECT salary FROM employees WHERE dept_id = 10 ORDER BY salary), "
                  "(SELECT salary FROM employees WHERE dept_id = 10 ORDER BY salary DESC)").fetchone())

# pd:main
mask = emp["salary"] == emp.groupby("dept_id")["salary"].transform("max")
pd_df = emp[mask].sort_values(["dept_id", "emp_id"]).reset_index(drop=True)
idx_df = emp.dropna(subset=["salary", "dept_id"]).loc[lambda d: d.groupby("dept_id")["salary"].idxmax()]
# pd:end
print("\npandas transform('max') mask ids:", pd_df["emp_id"].tolist())
print("pandas idxmax ids (one per dept):", idx_df["emp_id"].tolist())
print("transform('max') on the NaN dept key:", emp.groupby("dept_id")["salary"].transform("max").tolist())

# compared after sorting by dept_id, emp_id; NaN dept/salary rows never match in either engine
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert corr_df["emp_id"].tolist() == sql_df["emp_id"].tolist() == [1, 2, 4, 5]
assert len(idx_df) == 3 and set(idx_df["dept_id"]) == {10, 20, 30}
print("\nasserts passed: join == correlated == pandas transform mask (ids 1,2,4,5); idxmax returns one row per department")
```

**Output (my run):**
```text
derived-table join (ties kept):
 emp_id name  dept_id  salary
      1 Asha       10      90
      2  Ben       10      90
      4  Dev       20      80
      5  Eve       30      60
correlated subquery ids: [1, 2, 4, 5]
NOT EXISTS (nobody earns more) ids: [1, 2, 4, 5, 7, 8]

LIMIT 1 per group (no tie-break) -> one row per department:
 emp_id name  dept_id  salary
      1 Asha       10    90.0
      4  Dev       20    80.0
      5  Eve       30    60.0
      7 Hari       40     NaN

GROUP BY dept_id with bare column `name` next to MAX(salary) (SQLite only):
 dept_id name  max_salary
      10 Asha        90.0
      20  Dev        80.0
      30  Eve        60.0
      40 Hari         NaN

FROM-subquery without an alias: [(95,)]
scalar subquery returning many rows (dept 10, ORDER BY salary ASC / DESC): (70, 90)

pandas transform('max') mask ids: [1, 2, 4, 5]
pandas idxmax ids (one per dept): [1, 4, 5]
transform('max') on the NaN dept key: [90.0, 90.0, 90.0, 80.0, 60.0, 60.0, nan, nan]

asserts passed: join == correlated == pandas transform mask (ids 1,2,4,5); idxmax returns one row per department
```

**Edge cases:**
- **Ties:** the join, the correlated subquery and the pandas mask all return both Asha and Ben. If you want exactly one per department, say how to break the tie (lowest `emp_id`, earliest hire date) and put it in the query; Part 4 does this with `ROW_NUMBER`.
- **NULL salary:** `NOT EXISTS (higher salary)` returned Hari and Ivy as well (ids 7 and 8) because a NULL comparison finds no higher row, so "nobody earns more" is true. The join and `=` versions drop them. Pick on purpose.
- **NULL department:** the NULL group exists in `GROUP BY` (max 95), but `NULL = NULL` never joins it back to Ivy. pandas `groupby` drops NaN keys, so `transform("max")` gives NaN for Ivy and the mask excludes her. SQL and pandas agree for different reasons.
- **Department with all NULL salaries:** department 40 appears in the SQL maxima with a NULL max, and returns nothing. pandas `idxmax` on an all-NaN group would be a problem, so I dropped NaN salary and department rows before `idxmax` (I did not run the version without the drop).
- **Empty department:** a department with no employees has no row, so it cannot appear in either result.

**Then explain:**
- **Tie behaviour:** the join compares with `=` to the max, so every employee at the max qualifies. That is usually what "the highest-paid, and all of them when tied" asks for.
- **`LIMIT 1` per group:** a correlated `ORDER BY salary DESC LIMIT 1` returns one row per department. With a tie the choice depends on the engine and plan unless you add a tie-breaker such as `, e2.emp_id`.
- **Bare column with GROUP BY:** SQLite accepted `SELECT dept_id, name, MAX(salary) ... GROUP BY dept_id`, and returned Asha for department 10; the other engines I know of reject a non-aggregated column like that or pick arbitrarily (not executed here; PostgreSQL rejects it from what I know, MySQL depends on `ONLY_FULL_GROUP_BY`). Do not rely on it. It also hides the tie.
- **Two other SQLite facts from the run:** a FROM-subquery without an alias is accepted (the Code block ran `FROM (SELECT ...)` with no name; other engines may require one, not executed), and a scalar subquery that returns several rows does not error, it returns the first row in its `ORDER BY` (70 ascending, 90 descending for department 10). PostgreSQL documents an error for that case, which I did not run.
- **pandas:** `transform("max")` keeps the original index and length, so a boolean mask works directly (the same idea as the derived-table join). `idxmax` returns the index label of the first max in each group, so it returns one row and drops the tie.
- Window version, `RANK() OVER (PARTITION BY dept_id ORDER BY salary DESC) = 1`, is in Part 4.

**Follow-ups:**
- *How do I get exactly one per department?* Add a deterministic tie-break, `ORDER BY salary DESC, emp_id LIMIT 1`, or `ROW_NUMBER` in Part 4.
- *Which is faster, join or correlated?* Not measured here; the join aggregates once, the correlated form runs the inner query per outer row unless the optimiser rewrites it (not executed).
- *How would I find the second highest?* Part 4 and Q27.

**Common mistakes:**
- `WHERE salary = (SELECT MAX(salary) FROM employees)`: that is the single highest in the whole company, not per department.
- `GROUP BY dept_id` with `name` selected and trusting the name that comes back.
- Using `idxmax` and being surprised that ties vanish.
- Forgetting that NULL salaries and NULL departments fall out of equality joins.

### Q27 ⭐⭐ 🟡 Top-N per group via a correlated subquery, no window functions: employees(emp_id, name, dept_id, salary). Return the top 2 earners in each department using WHERE (SELECT COUNT(*) FROM employees e2 WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) < 2. Explain why strict > makes ties share a rank (so more than 2 rows can return), how to break ties with emp_id, the cost (one count per outer row, quadratic per group), why LIMIT inside a per-group subquery is not portable (hedged: MySQL error 1235 for LIMIT in IN), and the pandas groupby head or nlargest. Point to Part 4 for ROW_NUMBER.
**Asked at:** datadriven.io subquery interview patterns and a LetsDataScience CTE-vs-subquery guide, not candidate reports; analyst and data scientist screens
**Say this first (1 line):** For each employee, count how many people in the same department earn strictly more, and keep the employee if that count is below 2; because the test is strict `>`, tied salaries share a rank, so a tie at second place returns more than 2 rows, and you add `emp_id` to the comparison to get exactly 2.

**Schema and sample data:**
```sql
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),(4,'Dev',10,60),
 (5,'Eve',20,80),(6,'Farid',20,75),(7,'Gita',20,75),(8,'Hari',20,60),
 (9,'Ivy',30,50);
```
Department 20 has a tie for second place (Farid and Gita at 75).

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
```
With the tie broken by `emp_id` (`SQL_TIEBREAK`):
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary > e.salary OR (e2.salary = e.salary AND e2.emp_id < e.emp_id))) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
```
The same with a row-value comparison (`SQL_ROWVALUE`), which ran on SQLite 3.45:
```sql
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id)) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
```

**pandas answer:** `rank(method="min")` reproduces the strict-greater count, `head(2)` after a sort reproduces the tie-break, and `nlargest` is the per-group shortcut.
```python
rank_min = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False)     # = (count strictly higher) + 1
pd_ties = emp[rank_min <= 2].sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
pd_head = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
           .groupby("dept_id").head(2))
pd_nlargest = emp.groupby("dept_id", group_keys=False).apply(lambda g: g.nlargest(2, "salary", keep="first"))
```

**Example:** the inner count for each employee (printed as `higher` in the Code block).
- Department 10: Asha 90 has 0 higher, Ben 90 has 0 (equal is not higher), Chitra 70 has 2, Dev 60 has 3. `< 2` keeps Asha and Ben.
- Department 20: Eve 80 has 0, Farid 75 has 1, Gita 75 has 1, Hari 60 has 3. `< 2` keeps Eve, Farid and Gita, three rows for a "top 2".
- Department 30: Ivy 50 has 0, kept.
- Total 6 rows for `SQL_MAIN`.
- With the tie-break: Gita's count becomes 2 (Eve higher, and Farid has the same salary with a smaller id), so she drops. Department 20 returns Eve and Farid. Total 5 rows, exactly 2 per department (department 30 has only one person).
- The row-value version compares `(salary, -emp_id)` as a pair, higher salary first and lower id winning ties. It returned the same ids, 1, 2, 5, 6, 9.

**Code:** run with `python3 -I`.
```python
# Q27: top-N per group with a correlated COUNT subquery (no window functions); ties; tie-break; row values
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE employees(emp_id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER, salary INTEGER);
INSERT INTO employees VALUES
 (1,'Asha',10,90),(2,'Ben',10,90),(3,'Chitra',10,70),(4,'Dev',10,60),
 (5,'Eve',20,80),(6,'Farid',20,75),(7,'Gita',20,75),(8,'Hari',20,60),
 (9,'Ivy',30,50);
"""
SQL_MAIN = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_TIEBREAK = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary > e.salary OR (e2.salary = e.salary AND e2.emp_id < e.emp_id))) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_ROWVALUE = """
SELECT e.emp_id, e.name, e.dept_id, e.salary
FROM employees e
WHERE (SELECT COUNT(*) FROM employees e2
       WHERE e2.dept_id = e.dept_id
         AND (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id)) < 2
ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_COUNTS = """
SELECT e.emp_id, e.dept_id, e.salary,
       (SELECT COUNT(*) FROM employees e2
        WHERE e2.dept_id = e.dept_id AND e2.salary > e.salary) AS higher
FROM employees e ORDER BY e.dept_id, e.salary DESC, e.emp_id
"""
SQL_LIMIT_IN = """
SELECT emp_id FROM employees
WHERE emp_id IN (SELECT e2.emp_id FROM employees e2 ORDER BY e2.salary DESC, e2.emp_id LIMIT 2)
ORDER BY emp_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
emp = pd.read_sql_query("SELECT * FROM employees", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
tb_df = pd.read_sql_query(SQL_TIEBREAK, con)
rv_df = pd.read_sql_query(SQL_ROWVALUE, con)
print("strict > (ties share a rank):")
print(sql_df.to_string(index=False))
print("\nhow many strictly higher earners in the department, per employee:")
print(pd.read_sql_query(SQL_COUNTS, con).to_string(index=False))
print("\ntie-break by emp_id, rows:", len(tb_df), "ids", tb_df["emp_id"].tolist())
print("row-value tie-break (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id), ids", rv_df["emp_id"].tolist())
print("LIMIT inside an IN subquery runs on SQLite (global top 2, not per group):", [r[0] for r in con.execute(SQL_LIMIT_IN)])

# pd:main
rank_min = emp.groupby("dept_id")["salary"].rank(method="min", ascending=False)     # = (count strictly higher) + 1
pd_ties = emp[rank_min <= 2].sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
pd_head = (emp.sort_values(["dept_id", "salary", "emp_id"], ascending=[True, False, True])
           .groupby("dept_id").head(2))
pd_nlargest = emp.groupby("dept_id", group_keys=False).apply(lambda g: g.nlargest(2, "salary", keep="first"))
# pd:end
pairs = int((emp.groupby("dept_id").size() ** 2).sum())
print("\npandas rank(method='min') <= 2 ids:", pd_ties["emp_id"].tolist())
print("pandas sort + groupby.head(2) ids:", pd_head["emp_id"].tolist())
print("pandas groupby nlargest(2, keep='first') ids:", sorted(pd_nlargest["emp_id"].tolist()))
print(f"comparisons the correlated count makes: {pairs} (sum of group size squared) for {len(emp)} rows")

pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_ties.reset_index(drop=True), check_dtype=False)
pd.testing.assert_frame_equal(tb_df.reset_index(drop=True), pd_head.reset_index(drop=True), check_dtype=False)
assert rv_df["emp_id"].tolist() == tb_df["emp_id"].tolist()
assert sorted(pd_nlargest["emp_id"]) == sorted(tb_df["emp_id"])
print("\nasserts passed: strict-> SQL == rank(method='min'); tie-break SQL == row-value SQL == head(2) == nlargest; compared in dept_id, salary desc, emp_id order")
```

**Output (my run):**
```text
strict > (ties share a rank):
 emp_id  name  dept_id  salary
      1  Asha       10      90
      2   Ben       10      90
      5   Eve       20      80
      6 Farid       20      75
      7  Gita       20      75
      9   Ivy       30      50

how many strictly higher earners in the department, per employee:
 emp_id  dept_id  salary  higher
      1       10      90       0
      2       10      90       0
      3       10      70       2
      4       10      60       3
      5       20      80       0
      6       20      75       1
      7       20      75       1
      8       20      60       3
      9       30      50       0

tie-break by emp_id, rows: 5 ids [1, 2, 5, 6, 9]
row-value tie-break (e2.salary, -e2.emp_id) > (e.salary, -e.emp_id), ids [1, 2, 5, 6, 9]
LIMIT inside an IN subquery runs on SQLite (global top 2, not per group): [1, 2]

pandas rank(method='min') <= 2 ids: [1, 2, 5, 6, 7, 9]
pandas sort + groupby.head(2) ids: [1, 2, 5, 6, 9]
pandas groupby nlargest(2, keep='first') ids: [1, 2, 5, 6, 9]
comparisons the correlated count makes: 33 (sum of group size squared) for 9 rows

asserts passed: strict-> SQL == rank(method='min'); tie-break SQL == row-value SQL == head(2) == nlargest; compared in dept_id, salary desc, emp_id order
```

**Edge cases:**
- **Ties:** strict `>` gives tied people the same count, so they share a rank (SQL's RANK behaviour). A tie across the cutoff returns more than N rows (3 rows in department 20 above). A tie across the whole top is fine (Asha and Ben both 90).
- **Fewer than N rows in a group:** the group returns everything it has (Ivy).
- **NULL salary:** `e2.salary > NULL` is unknown, so a NULL-salary employee has a count of 0 and passes `< 2`, and is treated as top earner. Filter `salary IS NOT NULL` first. I did not run NULL salaries in this table.
- **NULL department:** `e2.dept_id = e.dept_id` never matches NULL, so those rows have count 0 and are all returned. I did not run that here either; filter them.
- **Duplicate `emp_id`:** the tie-break assumes ids are unique.

**Then explain:**
- **Why it works:** a person's rank is 1 plus the number of people ahead of them. "Count below 2" means at most 2 are ahead, so the person is in the top 2 (or tied into it).
- **Cost:** the count runs for every outer row and scans the department, so work grows with the square of the group size. In my run that is 33 comparisons (16 + 16 + 1) for 9 rows. With an index on `(dept_id, salary)` an engine can do better; I did not test this and optimisers differ (not executed).
- **LIMIT inside a per-group subquery is not portable:** you cannot write "LIMIT 2 per department" as a plain inner query, because the inner query would be limited globally. In my run `... IN (SELECT ... ORDER BY salary DESC LIMIT 2)` returned the global top 2 (ids 1 and 2), not top 2 per department. MySQL rejects `LIMIT` inside `IN`/`ALL`/`ANY`/`SOME` subqueries with error 1235 (from its documentation; not executed here); see Q28.
- **pandas:** `groupby("dept_id").head(2)` after sorting is the simplest tie-broken top N. `nlargest(2, "salary", keep="first")` per group is equivalent; `keep="all"` would keep the tied rows. The rank form keeps ties like the SQL count.
- **Window version:** `ROW_NUMBER() OVER (PARTITION BY dept_id ORDER BY salary DESC, emp_id)` is the standard answer, and it is covered in Part 4 (and `RANK` / `DENSE_RANK` there too). The correlated count is the "no windows" answer an interviewer may ask for.

**Follow-ups:**
- *What changes for DENSE_RANK semantics?* Count distinct higher salaries, `COUNT(DISTINCT e2.salary)`, instead of rows. Not run here.
- *How do I get the top 1?* `< 1`, which is Q26.
- *Why not `LIMIT 2` in the correlated subquery?* A scalar subquery can return one value, not two rows. You can use `IN` with a per-row subquery on some engines, but MySQL rejects it (hedged).

**Common mistakes:**
- Using `>=` without noticing that every employee then counts themself, so the cutoff would have to become `<= 2`.
- Not breaking ties and returning 3 rows for a "top 2".
- Forgetting NULL salaries rank as top.
- Believing `LIMIT` inside the subquery limits per department.

### Q28 ⭐⭐ 🟡 Subqueries with LIMIT: customers(customer_id, name) and orders(order_id, customer_id, amount). Show the orders of the top 3 customers by total spend. Write WHERE customer_id IN (SELECT customer_id FROM orders GROUP BY customer_id ORDER BY SUM(amount) DESC LIMIT 3), explain that SQLite accepts it, that MySQL rejects LIMIT inside IN, ALL, ANY or SOME subqueries with error 1235 (hedged, not executed) and that a derived-table join is the portable workaround. Cover the tie at rank 3 and ORDER BY determinism, and give pandas nlargest then isin.
**Asked at:** vendor documentation (SQLite, PostgreSQL, MySQL) on subquery expressions, WITH and subquery restrictions, not a candidate report; engine-behaviour follow-ups in analyst and data scientist rounds
**Say this first (1 line):** Rank customers by `SUM(amount)` in a subquery with `ORDER BY ... DESC LIMIT 3` and keep the orders whose customer is in that list; SQLite accepts the `LIMIT` inside `IN`, MySQL (per its documentation) does not, so the portable form joins to the same query as a derived table, and you must add a tie-breaker because customer 3 and customer 4 tie for third place.

**Schema and sample data:**
```sql
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Eve'),(6,'Farid');
INSERT INTO orders VALUES
 (1,1,300),(2,1,200),(3,2,400),(4,3,300),(5,4,100),(6,4,200),(7,5,100);
```

**SQL answer:** `SQL_MAIN` in the Code block.
```sql
SELECT order_id, customer_id, amount
FROM orders
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      ORDER BY SUM(amount) DESC, customer_id
                      LIMIT 3)
ORDER BY order_id
```
The portable derived-table join (`SQL_DERIVED`):
```sql
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN (SELECT customer_id
      FROM orders
      GROUP BY customer_id
      ORDER BY SUM(amount) DESC, customer_id
      LIMIT 3) top3 ON top3.customer_id = o.customer_id
ORDER BY o.order_id
```
Tie-inclusive: every customer whose total is at least the third-highest total (`SQL_TIES`):
```sql
WITH spend AS (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id)
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN spend s ON s.customer_id = o.customer_id
WHERE s.total >= (SELECT total FROM spend ORDER BY total DESC LIMIT 1 OFFSET 2)
ORDER BY o.order_id
```

**pandas answer:** aggregate, take the top three with an explicit tie-break, then `isin`; `nlargest(..., keep="all")` is the tie-inclusive form.
```python
totals = orders.groupby("customer_id")["amount"].sum().reset_index()
top3 = totals.sort_values(["amount", "customer_id"], ascending=[False, True]).head(3)     # tie-break by id
pd_df = orders[orders["customer_id"].isin(top3["customer_id"])].sort_values("order_id").reset_index(drop=True)
tie_ids = totals.set_index("customer_id")["amount"].nlargest(3, keep="all").index     # keep every tie at rank 3
pd_ties = orders[orders["customer_id"].isin(tie_ids)].sort_values("order_id").reset_index(drop=True)
```

**Example:**
- Totals: Asha 300 + 200 = 500, Ben 400, Chitra 300, Dev 100 + 200 = 300, Eve 100, Farid no orders.
- Ranked by total: Asha 500, Ben 400, then Chitra and Dev tied at 300, then Eve 100.
- `ORDER BY SUM(amount) DESC, customer_id LIMIT 3` picks Asha, Ben, and Chitra (the tie goes to the smaller id). The outer query returns their orders: 1, 2 (Asha), 3 (Ben), 4 (Chitra).
- The tie-inclusive query uses the third-highest total, 300 (`OFFSET 2`), and keeps everyone with a total of at least 300: Asha, Ben, Chitra and Dev. That adds Dev's orders 5 and 6.
- Without the `customer_id` tie-break, my run picked Dev (customers 1, 2, 4), not Chitra. Both are valid answers to the SQL as written, which is the point.

**Code:** run with `python3 -I`.
```python
# Q28: orders of the top 3 customers by total spend: LIMIT inside IN, derived-table join, tie at rank 3
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Eve'),(6,'Farid');
INSERT INTO orders VALUES
 (1,1,300),(2,1,200),(3,2,400),(4,3,300),(5,4,100),(6,4,200),(7,5,100);
"""
SQL_MAIN = """
SELECT order_id, customer_id, amount
FROM orders
WHERE customer_id IN (SELECT customer_id
                      FROM orders
                      GROUP BY customer_id
                      ORDER BY SUM(amount) DESC, customer_id
                      LIMIT 3)
ORDER BY order_id
"""
SQL_DERIVED = """
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN (SELECT customer_id
      FROM orders
      GROUP BY customer_id
      ORDER BY SUM(amount) DESC, customer_id
      LIMIT 3) top3 ON top3.customer_id = o.customer_id
ORDER BY o.order_id
"""
SQL_TIES = """
WITH spend AS (SELECT customer_id, SUM(amount) AS total FROM orders GROUP BY customer_id)
SELECT o.order_id, o.customer_id, o.amount
FROM orders o
JOIN spend s ON s.customer_id = o.customer_id
WHERE s.total >= (SELECT total FROM spend ORDER BY total DESC LIMIT 1 OFFSET 2)
ORDER BY o.order_id
"""
SQL_NO_TIEBREAK = """
SELECT customer_id FROM orders GROUP BY customer_id ORDER BY SUM(amount) DESC LIMIT 3
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
orders = pd.read_sql_query("SELECT * FROM orders", con)
print("totals per customer:", con.execute(
    "SELECT customer_id, SUM(amount) FROM orders GROUP BY customer_id ORDER BY SUM(amount) DESC, customer_id").fetchall())

sql_df = pd.read_sql_query(SQL_MAIN, con)
der_df = pd.read_sql_query(SQL_DERIVED, con)
ties_df = pd.read_sql_query(SQL_TIES, con)
print("\nIN (... LIMIT 3), tie broken by customer_id:")
print(sql_df.to_string(index=False))
print("derived-table join gives the same rows:", sql_df.equals(der_df))
print("tie-inclusive (total >= third-highest total) customers:", sorted(ties_df["customer_id"].unique().tolist()))
print("without the customer_id tie-break the rank-3 pick is left to the engine; this run chose:",
      [r[0] for r in con.execute(SQL_NO_TIEBREAK)])

print("\nLIMIT / OFFSET forms on SQLite 3.45:")
print("  LIMIT 1+1 OFFSET 4/2        ->", [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id LIMIT 1+1 OFFSET 4/2")])
print("  LIMIT -1 OFFSET 5           ->", [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id LIMIT -1 OFFSET 5")])
print("  LIMIT (SELECT 2)            ->", [r[0] for r in con.execute("SELECT order_id FROM orders ORDER BY order_id LIMIT (SELECT 2)")])
try:
    con.execute("SELECT order_id FROM orders ORDER BY order_id OFFSET 1").fetchall()
except sqlite3.Error as e:
    print("  OFFSET without LIMIT        -> error:", e)

# pd:main
totals = orders.groupby("customer_id")["amount"].sum().reset_index()
top3 = totals.sort_values(["amount", "customer_id"], ascending=[False, True]).head(3)     # tie-break by id
pd_df = orders[orders["customer_id"].isin(top3["customer_id"])].sort_values("order_id").reset_index(drop=True)
tie_ids = totals.set_index("customer_id")["amount"].nlargest(3, keep="all").index     # keep every tie at rank 3
pd_ties = orders[orders["customer_id"].isin(tie_ids)].sort_values("order_id").reset_index(drop=True)
# pd:end
print("\npandas nlargest(3, keep='all') customers:", sorted(tie_ids.tolist()))
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
pd.testing.assert_frame_equal(ties_df, pd_ties, check_dtype=False)
assert sorted(sql_df["customer_id"].unique()) == [1, 2, 3] and sorted(ties_df["customer_id"].unique()) == [1, 2, 3, 4]
print("\nasserts passed: SQL IN(LIMIT) == derived join == pandas (customers 1, 2, 3); tie-inclusive == nlargest(keep='all') (1, 2, 3, 4); compared by order_id")
```

**Output (my run):**
```text
totals per customer: [(1, 500), (2, 400), (3, 300), (4, 300), (5, 100)]

IN (... LIMIT 3), tie broken by customer_id:
 order_id  customer_id  amount
        1            1     300
        2            1     200
        3            2     400
        4            3     300
derived-table join gives the same rows: True
tie-inclusive (total >= third-highest total) customers: [1, 2, 3, 4]
without the customer_id tie-break the rank-3 pick is left to the engine; this run chose: [1, 2, 4]

LIMIT / OFFSET forms on SQLite 3.45:
  LIMIT 1+1 OFFSET 4/2        -> [3, 4]
  LIMIT -1 OFFSET 5           -> [6, 7]
  LIMIT (SELECT 2)            -> [1, 2]
  OFFSET without LIMIT        -> error: near "OFFSET": syntax error

pandas nlargest(3, keep='all') customers: [1, 2, 3, 4]

asserts passed: SQL IN(LIMIT) == derived join == pandas (customers 1, 2, 3); tie-inclusive == nlargest(keep='all') (1, 2, 3, 4); compared by order_id
```

**Edge cases:**
- **Tie at rank 3:** `LIMIT 3` must cut somewhere. Decide: arbitrary (bad), deterministic with a tie-break (my `SQL_MAIN`), or include all tied customers (`SQL_TIES`, 4 customers, 6 orders in my run). pandas: `nlargest(3, keep="first")` or `keep="all"`.
- **Non-deterministic ORDER BY:** with only `ORDER BY SUM(amount) DESC`, which tied customer wins depends on the plan. Always end the `ORDER BY` with a unique column.
- **Fewer than 3 customers:** `LIMIT 3` returns what exists.
- **Customers without orders (Farid):** they have no rows in `orders`, so they cannot rank. If you want them in a ranking, start from `customers` with a LEFT JOIN.
- **NULL customer_id orders:** the NULL group is a group in `GROUP BY` and could rank in the top 3; the outer `IN` then never matches it. I did not include such a row here, so filter `customer_id IS NOT NULL` in the subquery if you may have them.
- **LIMIT with expressions:** on SQLite 3.45, `LIMIT 1+1 OFFSET 4/2` ran (rows 3 and 4), `LIMIT -1 OFFSET 5` ran (a negative limit means no limit; rows 6 and 7), `LIMIT (SELECT 2)` ran, and `OFFSET` without `LIMIT` is a syntax error. Other engines differ (for example, PostgreSQL allows `OFFSET` alone); not executed here.

**Then explain:**
- **What the subquery returns:** a list of three ids. `IN` then keeps the orders of those customers. A subquery with `GROUP BY ... ORDER BY aggregate ... LIMIT n` is the standard "top N entities" pattern.
- **MySQL (hedged, not executed here):** its documentation says `LIMIT` is not supported inside `IN`, `ALL`, `ANY` or `SOME` subqueries (error 1235). The workaround is the derived-table join, which my run shows returns exactly the same rows as the `IN` form on SQLite.
- **Other engines:** PostgreSQL's subquery documentation does not forbid it as far as I read it, but I did not run PostgreSQL, BigQuery or Snowflake here, so I would test it on the target engine.
- **Tie rule:** "top 3" is ambiguous when there is a tie. Ask the interviewer, then say which you chose.
- **pandas:** `groupby().sum()` then `nlargest`, then `isin`. The `isin` is the `IN`, the `nlargest` is the `ORDER BY ... LIMIT`. `nlargest` defaults to `keep="first"`, which resolves ties by position, but I did not run that form, so I used an explicit sort on `(amount, customer_id)` for the tie-break.
- **Window version:** `DENSE_RANK() OVER (ORDER BY total DESC) <= 3` is in Part 4.

**Follow-ups:**
- *Why the derived table in MySQL?* It turns the limited subquery into a table that is joined, not a list tested with `IN`.
- *How do I get the top 3 per region?* That is top-N per group, Q27 and Part 4.
- *What if two customers tie for first?* They take ranks 1 and 1, and with `LIMIT 3` you may only get one of the tied rank-3 customers.

**Common mistakes:**
- Leaving out the tie-breaker, then wondering why the answer changes between runs or engines.
- Putting `LIMIT 3` on the outer query, which returns three orders, not the orders of three customers.
- Using `SUM` per order row without `GROUP BY` in the subquery.
- Assuming `LIMIT` inside `IN` works everywhere.

### Q29 ⭐⭐ 🟡 CTE scaffolding for a cohort-style question (scaffolding only; retention logic is Part 6): orders(order_id, customer_id, order_date, amount) with ISO date strings. Using chained CTEs, compute each customer's first order date, label every order as 'first' or 'repeat', and count new versus repeat customers per month (strftime). Explain why each CTE has one purpose and one grain, how to check grain with COUNT(*) versus COUNT(DISTINCT customer_id), and give the pandas groupby/transform('min') version.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Build it in layers: one CTE gives each customer's first order date (one row per customer), the next labels every order `first` or `repeat` by comparing its date with that first date (one row per order), and the last counts distinct customers per month and label; each layer has one job and one grain, which I check with `COUNT(*)` against `COUNT(DISTINCT customer_id)`.

**Schema and sample data:**
```sql
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05',20),(2,1,'2024-01-20',30),(3,2,'2024-01-25',40),
 (4,1,'2024-02-03',10),(5,2,'2024-02-10',25),
 (6,3,'2024-02-15',60),(7,3,'2024-02-15',15),
 (8,4,'2024-03-01',35),(9,1,'2024-03-09',50);
```
Customer 3 has two orders on the same first day, which is the one grain trap in the data.

**SQL answer:** `SQL_MAIN` in the Code block (scaffolding only; retention curves are Part 6).
```sql
WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM orders
  GROUP BY customer_id
),
labelled AS (
  SELECT o.order_id, o.customer_id, strftime('%Y-%m', o.order_date) AS order_month,
         CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o
  JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT order_month,
       COUNT(DISTINCT CASE WHEN label = 'first'  THEN customer_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN label = 'repeat' THEN customer_id END) AS repeat_customers
FROM labelled
GROUP BY order_month
ORDER BY order_month
```
The grain check, `SQL_GRAIN`, is also in the Code block.
```sql
WITH first_order AS (SELECT customer_id, MIN(order_date) AS first_date FROM orders GROUP BY customer_id),
labelled AS (
  SELECT o.order_id, o.customer_id, CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT 'first_order' AS cte, COUNT(*) AS n_rows, COUNT(DISTINCT customer_id) AS n_customers FROM first_order
UNION ALL SELECT 'labelled', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled
UNION ALL SELECT 'labelled first rows', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled WHERE label = 'first'
UNION ALL SELECT 'orders', COUNT(*), COUNT(DISTINCT customer_id) FROM orders
```

**pandas answer:** `transform("min")` is the `first_order` CTE joined back onto every order in one step.
```python
o = orders.assign(first_date=orders.groupby("customer_id")["order_date"].transform("min"),
                  order_month=orders["order_date"].str[:7])
o["label"] = (o["order_date"] == o["first_date"]).map({True: "first", False: "repeat"})
new_c = o[o["label"] == "first"].groupby("order_month")["customer_id"].nunique()
rep_c = o[o["label"] == "repeat"].groupby("order_month")["customer_id"].nunique()
pd_df = (pd.DataFrame({"new_customers": new_c, "repeat_customers": rep_c})
         .fillna(0).astype("int64").rename_axis("order_month").reset_index())
```

**Example:**
- `first_order`: customer 1 first on 2024-01-05, customer 2 on 2024-01-25, customer 3 on 2024-02-15, customer 4 on 2024-03-01. 4 rows, 4 customers.
- `labelled`: orders 1, 3, 6, 7, 8 are `first` (their date equals the customer's first date; order 7 ties with order 6 on 2024-02-15). Orders 2, 4, 5, 9 are `repeat`. 9 rows, 4 customers.
- January: new customers are 1 and 2 (2). Customer 1 also ordered again on 2024-01-20, which is a repeat order in the same month, so repeat customers = 1.
- February: new is customer 3 (1; two rows, one customer). Repeat customers: 1 (order 4) and 2 (order 5) = 2.
- March: new is customer 4 (1), repeat is customer 1 (order 9) = 1.
- So the table is (Jan 2, 1), (Feb 1, 2), (Mar 1, 1). A customer can be both new and repeat in their first month.
- Counting rows instead would give February `new = 2`, because both of customer 3's same-day orders are labelled `first`. The distinct count prevents that.

**Code:** run with `python3 -I`.
```python
# Q29: chained CTEs: first order date, first/repeat label, new vs repeat customers per month
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'2024-01-05',20),(2,1,'2024-01-20',30),(3,2,'2024-01-25',40),
 (4,1,'2024-02-03',10),(5,2,'2024-02-10',25),
 (6,3,'2024-02-15',60),(7,3,'2024-02-15',15),
 (8,4,'2024-03-01',35),(9,1,'2024-03-09',50);
"""
SQL_MAIN = """
WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_date
  FROM orders
  GROUP BY customer_id
),
labelled AS (
  SELECT o.order_id, o.customer_id, strftime('%Y-%m', o.order_date) AS order_month,
         CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o
  JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT order_month,
       COUNT(DISTINCT CASE WHEN label = 'first'  THEN customer_id END) AS new_customers,
       COUNT(DISTINCT CASE WHEN label = 'repeat' THEN customer_id END) AS repeat_customers
FROM labelled
GROUP BY order_month
ORDER BY order_month
"""
SQL_GRAIN = """
WITH first_order AS (SELECT customer_id, MIN(order_date) AS first_date FROM orders GROUP BY customer_id),
labelled AS (
  SELECT o.order_id, o.customer_id, CASE WHEN o.order_date = f.first_date THEN 'first' ELSE 'repeat' END AS label
  FROM orders o JOIN first_order f ON f.customer_id = o.customer_id
)
SELECT 'first_order' AS cte, COUNT(*) AS n_rows, COUNT(DISTINCT customer_id) AS n_customers FROM first_order
UNION ALL SELECT 'labelled', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled
UNION ALL SELECT 'labelled first rows', COUNT(*), COUNT(DISTINCT customer_id) FROM labelled WHERE label = 'first'
UNION ALL SELECT 'orders', COUNT(*), COUNT(DISTINCT customer_id) FROM orders
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
orders = pd.read_sql_query("SELECT * FROM orders", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("new vs repeat customers per month (SQL):")
print(sql_df.to_string(index=False))
print("\ngrain check (rows vs distinct customers):")
print(pd.read_sql_query(SQL_GRAIN, con).to_string(index=False))

# pd:main
o = orders.assign(first_date=orders.groupby("customer_id")["order_date"].transform("min"),
                  order_month=orders["order_date"].str[:7])
o["label"] = (o["order_date"] == o["first_date"]).map({True: "first", False: "repeat"})
new_c = o[o["label"] == "first"].groupby("order_month")["customer_id"].nunique()
rep_c = o[o["label"] == "repeat"].groupby("order_month")["customer_id"].nunique()
pd_df = (pd.DataFrame({"new_customers": new_c, "repeat_customers": rep_c})
         .fillna(0).astype("int64").rename_axis("order_month").reset_index())
# pd:end
print("\npandas version:")
print(pd_df.to_string(index=False))
print("\nlabelled orders per label:", o["label"].value_counts().to_dict())

# compared after ordering both by order_month
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert o["first_date"].notna().all() and len(o) == len(orders) == 9
assert o.loc[o["label"] == "first", "customer_id"].nunique() == 4 and (o["label"] == "first").sum() == 5
print("\nasserts passed: SQL == pandas (4 customers, 5 rows labelled 'first' because customer 3 has two orders on the first day)")
```

**Output (my run):**
```text
new vs repeat customers per month (SQL):
order_month  new_customers  repeat_customers
    2024-01              2                 1
    2024-02              1                 2
    2024-03              1                 1

grain check (rows vs distinct customers):
                cte  n_rows  n_customers
        first_order       4            4
           labelled       9            4
labelled first rows       5            4
             orders       9            4

pandas version:
order_month  new_customers  repeat_customers
    2024-01              2                 1
    2024-02              1                 2
    2024-03              1                 1

labelled orders per label: {'first': 5, 'repeat': 4}

asserts passed: SQL == pandas (4 customers, 5 rows labelled 'first' because customer 3 has two orders on the first day)
```

**Edge cases:**
- **Same-day first orders:** the `first` label is on the order, not the customer, so customer 3 has 2 `first` rows (5 `first` rows for 4 customers in my run). Count customers with `COUNT(DISTINCT customer_id)`. If you need exactly one first order per customer, add a tie-break on `order_id` (a window function in Part 4).
- **Month with no repeat customers:** the `COUNT(DISTINCT CASE ...)` form returns 0, not a missing row. In pandas the two series do not line up, so the frame is built from both and `fillna(0)` fills the gap; I used `astype("int64")` afterwards.
- **A month with no orders at all:** it does not appear in either result. A calendar table or a generated series would be needed; not done here.
- **NULL dates or customers:** `MIN(order_date)` ignores NULLs. A NULL `order_date` gives `strftime` NULL, a NULL month group. A NULL `customer_id` forms its own group in `first_order`, and the join `f.customer_id = o.customer_id` drops it (and in pandas `groupby` drops NaN keys, so `transform` gives NaN). I did not put NULLs in this table.
- **Date format:** ISO strings (`YYYY-MM-DD`) sort correctly as text, so `MIN` works. Other formats (`DD/MM/YYYY`) do not.

**Then explain:**
- **One purpose, one grain:** `first_order` is one row per customer. `labelled` is one row per order. The last select is one row per month. When a result has the wrong number of rows, you can find which layer broke the grain.
- **Grain check:** `COUNT(*)` versus `COUNT(DISTINCT customer_id)` on each CTE (printed above). For `first_order` they must be equal (4 and 4), for `labelled` the row count must equal the orders table (9). If a join step makes `labelled` bigger than `orders`, a key was not unique.
- **Why CTEs here:** each can be selected alone while debugging, and the names document the logic. The same query as nested subqueries would work and return the same rows; I did not time either (see the follow-up below).
- **pandas:** `groupby("customer_id")["order_date"].transform("min")` repeats the customer's min date on every order row, so no merge is needed. Then `nunique` per month and label.
- **strftime:** `strftime('%Y-%m', date)` is SQLite. PostgreSQL uses `TO_CHAR` or `DATE_TRUNC`, MySQL `DATE_FORMAT`, BigQuery `FORMAT_DATE` (from memory, not executed here).

**Follow-ups:**
- *Is a CTE faster than a subquery?* Not by itself. SQLite's documentation says the `MATERIALIZED` and `NOT MATERIALIZED` hints exist (3.35+) and are not binding. I did not measure it.
- *How would this become retention?* Join each order to the cohort month of its customer and count months since first order: Part 6.
- *What if the first order is on a later day than the first signup?* Then the cohort is defined by signup, not by order; use that table instead.

**Common mistakes:**
- Counting rows (`COUNT(*)`) instead of distinct customers and double counting same-day first orders.
- Joining `first_order` on something that is not unique.
- Comparing dates stored as text in a non-ISO format.
- Putting everything in one 40-line query so no layer can be checked alone.

### Q30 ⭐⭐ 🟡 CTE scaffolding for a funnel-style question (scaffolding only; funnel metrics are Part 8): events(user_id, event_name, event_time) with names 'view', 'cart', 'purchase'. With one CTE per step (users who viewed, users who carted, users who purchased) and joins, count users at each step and the step-to-step conversion. Explain why a CTE of DISTINCT users per step avoids double counting, that step order is ignored by this simple version, and give pandas sets or isin. Note that ordering within a session is a later part.
**Asked at:** expert gap-check from practice, no candidate report found; analyst and data scientist rounds
**Say this first (1 line):** Make one CTE per step holding the DISTINCT users who did it, chain them with LEFT JOINs from the first step so each later step only counts users who passed the earlier ones, count each column, and divide for conversion; DISTINCT users per step is what stops a user with two views and two carts from counting four times.

**Schema and sample data:**
```sql
CREATE TABLE events(user_id INTEGER, event_name TEXT, event_time TEXT);
INSERT INTO events VALUES
 (1,'view','2024-05-01 09:00'),(1,'cart','2024-05-01 09:05'),(1,'purchase','2024-05-01 09:10'),
 (2,'view','2024-05-01 10:00'),(2,'cart','2024-05-01 10:02'),
 (3,'view','2024-05-01 11:00'),
 (4,'view','2024-05-01 12:00'),(4,'view','2024-05-01 12:01'),(4,'cart','2024-05-01 12:03'),(4,'cart','2024-05-01 12:04'),
 (5,'cart','2024-05-01 13:00'),
 (6,'purchase','2024-05-01 08:00'),(6,'cart','2024-05-01 08:30'),(6,'view','2024-05-01 09:00');
```
User 4 repeats events, user 5 carted without viewing, and user 6 did all three steps but in the wrong order.

**SQL answer:** `SQL_MAIN` in the Code block (scaffolding only; real funnel metrics are Part 8).
```sql
WITH viewed AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'view'),
     carted AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'cart'),
     bought AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'purchase'),
     steps AS (
       SELECT v.user_id AS viewer, c.user_id AS carter, b.user_id AS buyer
       FROM viewed v
       LEFT JOIN carted c ON c.user_id = v.user_id
       LEFT JOIN bought b ON b.user_id = c.user_id
     ),
     counts AS (
       SELECT COUNT(viewer) AS viewed_users, COUNT(carter) AS carted_users, COUNT(buyer) AS bought_users
       FROM steps
     )
SELECT viewed_users, carted_users, bought_users,
       ROUND(1.0 * carted_users / viewed_users, 3) AS view_to_cart,
       ROUND(1.0 * bought_users / carted_users, 3) AS cart_to_buy,
       ROUND(1.0 * bought_users / viewed_users, 3) AS view_to_buy
FROM counts
```
The naive join that double counts (`SQL_NAIVE`) and a time-ordered check (`SQL_ORDERED`) are in the Code block too.
```sql
SELECT COUNT(*) AS joined_rows, COUNT(DISTINCT v.user_id) AS distinct_users
FROM events v
JOIN events c ON c.user_id = v.user_id AND c.event_name = 'cart'
WHERE v.event_name = 'view'
```

**pandas answer:** sets of user ids per step, intersected in funnel order; the `isin` form is the same count.
```python
viewed = set(events.loc[events["event_name"] == "view", "user_id"])
carted = set(events.loc[events["event_name"] == "cart", "user_id"])
bought = set(events.loc[events["event_name"] == "purchase", "user_id"])
n_view = len(viewed)
n_cart = len(viewed & carted)
n_buy = len(viewed & carted & bought)
pd_df = pd.DataFrame({"viewed_users": [n_view], "carted_users": [n_cart], "bought_users": [n_buy],
                      "view_to_cart": [round(n_cart / n_view, 3)], "cart_to_buy": [round(n_buy / n_cart, 3)],
                      "view_to_buy": [round(n_buy / n_view, 3)]})
# same counts with isin on distinct users
v = events.loc[events["event_name"] == "view", "user_id"].drop_duplicates()
c = events.loc[events["event_name"] == "cart", "user_id"].drop_duplicates()
b = events.loc[events["event_name"] == "purchase", "user_id"].drop_duplicates()
n_cart2 = int(c.isin(v).sum())
n_buy2 = int(b[b.isin(v) & b.isin(c)].shape[0])
```

**Example:**
- Distinct users per step: viewers 1, 2, 3, 4, 6 (5 users); carters 1, 2, 4, 5, 6 (5 users); purchasers 1, 6 (2 users).
- Step 1: 5 viewers.
- Step 2: viewers who also carted are 1, 2, 4, 6. User 3 never carted and user 5 never viewed, so 4. view-to-cart is 4 / 5 = 0.8.
- Step 3: carters among those who bought are 1 and 6, so 2. cart-to-buy is 2 / 4 = 0.5; view-to-buy is 2 / 5 = 0.4.
- Without the per-step DISTINCT: user 4 has 2 view rows and 2 cart rows, so a direct join of view rows to cart rows gives 4 rows for that one user. The naive join returned 7 rows for 4 users in my run (users 1, 2, 6 contribute 1 row each, user 4 contributes 4).
- Order is ignored: user 6 purchased at 08:00, carted at 08:30 and viewed at 09:00, yet counts as a full funnel user. With `view < cart < purchase` time conditions only 1 user (user 1) qualifies in my run, so the simple version reports 2.

**Code:** run with `python3 -I`.
```python
# Q30: funnel scaffolding: one CTE of DISTINCT users per step, joined, with step-to-step conversion
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_name TEXT, event_time TEXT);
INSERT INTO events VALUES
 (1,'view','2024-05-01 09:00'),(1,'cart','2024-05-01 09:05'),(1,'purchase','2024-05-01 09:10'),
 (2,'view','2024-05-01 10:00'),(2,'cart','2024-05-01 10:02'),
 (3,'view','2024-05-01 11:00'),
 (4,'view','2024-05-01 12:00'),(4,'view','2024-05-01 12:01'),(4,'cart','2024-05-01 12:03'),(4,'cart','2024-05-01 12:04'),
 (5,'cart','2024-05-01 13:00'),
 (6,'purchase','2024-05-01 08:00'),(6,'cart','2024-05-01 08:30'),(6,'view','2024-05-01 09:00');
"""
SQL_MAIN = """
WITH viewed AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'view'),
     carted AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'cart'),
     bought AS (SELECT DISTINCT user_id FROM events WHERE event_name = 'purchase'),
     steps AS (
       SELECT v.user_id AS viewer, c.user_id AS carter, b.user_id AS buyer
       FROM viewed v
       LEFT JOIN carted c ON c.user_id = v.user_id
       LEFT JOIN bought b ON b.user_id = c.user_id
     ),
     counts AS (
       SELECT COUNT(viewer) AS viewed_users, COUNT(carter) AS carted_users, COUNT(buyer) AS bought_users
       FROM steps
     )
SELECT viewed_users, carted_users, bought_users,
       ROUND(1.0 * carted_users / viewed_users, 3) AS view_to_cart,
       ROUND(1.0 * bought_users / carted_users, 3) AS cart_to_buy,
       ROUND(1.0 * bought_users / viewed_users, 3) AS view_to_buy
FROM counts
"""
SQL_NAIVE = """
SELECT COUNT(*) AS joined_rows, COUNT(DISTINCT v.user_id) AS distinct_users
FROM events v
JOIN events c ON c.user_id = v.user_id AND c.event_name = 'cart'
WHERE v.event_name = 'view'
"""
SQL_ORDERED = """
SELECT COUNT(DISTINCT v.user_id)
FROM events v
JOIN events c ON c.user_id = v.user_id AND c.event_name = 'cart'  AND c.event_time > v.event_time
JOIN events p ON p.user_id = v.user_id AND p.event_name = 'purchase' AND p.event_time > c.event_time
WHERE v.event_name = 'view'
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
events = pd.read_sql_query("SELECT * FROM events", con)

sql_df = pd.read_sql_query(SQL_MAIN, con)
print("funnel (SQL):")
print(sql_df.to_string(index=False))
print("\nnaive join of raw event rows (view x cart):", con.execute(SQL_NAIVE).fetchone(), "(joined_rows, distinct_users)")
print("distinct users who did cart at all:", con.execute("SELECT COUNT(DISTINCT user_id) FROM events WHERE event_name='cart'").fetchone()[0],
      "| carted AND viewed:", sql_df.loc[0, "carted_users"])
print("users whose view < cart < purchase times are in order:", con.execute(SQL_ORDERED).fetchone()[0], "(simple version counts", sql_df.loc[0, "bought_users"], ")")

# pd:main
viewed = set(events.loc[events["event_name"] == "view", "user_id"])
carted = set(events.loc[events["event_name"] == "cart", "user_id"])
bought = set(events.loc[events["event_name"] == "purchase", "user_id"])
n_view = len(viewed)
n_cart = len(viewed & carted)
n_buy = len(viewed & carted & bought)
pd_df = pd.DataFrame({"viewed_users": [n_view], "carted_users": [n_cart], "bought_users": [n_buy],
                      "view_to_cart": [round(n_cart / n_view, 3)], "cart_to_buy": [round(n_buy / n_cart, 3)],
                      "view_to_buy": [round(n_buy / n_view, 3)]})
# same counts with isin on distinct users
v = events.loc[events["event_name"] == "view", "user_id"].drop_duplicates()
c = events.loc[events["event_name"] == "cart", "user_id"].drop_duplicates()
b = events.loc[events["event_name"] == "purchase", "user_id"].drop_duplicates()
n_cart2 = int(c.isin(v).sum())
n_buy2 = int(b[b.isin(v) & b.isin(c)].shape[0])
# pd:end
print("\npandas sets:")
print(pd_df.to_string(index=False))
print("pandas isin counts:", len(v), n_cart2, n_buy2)

# single row, compared column by column
pd.testing.assert_frame_equal(sql_df, pd_df, check_dtype=False)
assert (len(v), n_cart2, n_buy2) == (5, 4, 2)
print("\nasserts passed: SQL == pandas sets == isin counts (5 viewers, 4 carted, 2 purchased)")
```

**Output (my run):**
```text
funnel (SQL):
 viewed_users  carted_users  bought_users  view_to_cart  cart_to_buy  view_to_buy
            5             4             2           0.8          0.5          0.4

naive join of raw event rows (view x cart): (7, 4) (joined_rows, distinct_users)
distinct users who did cart at all: 5 | carted AND viewed: 4
users whose view < cart < purchase times are in order: 1 (simple version counts 2 )

pandas sets:
 viewed_users  carted_users  bought_users  view_to_cart  cart_to_buy  view_to_buy
            5             4             2           0.8          0.5          0.4
pandas isin counts: 5 4 2

asserts passed: SQL == pandas sets == isin counts (5 viewers, 4 carted, 2 purchased)
```

**Edge cases:**
- **Repeated events:** `SELECT DISTINCT user_id` per step removes them; the grain of each step CTE is one row per user. In pandas, `drop_duplicates` or a set does the same.
- **Skipped steps:** user 5 carted without a view. Joining from `viewed` leaves them out of the cart step, so the funnel is "of the viewers". If you want raw reach per step, count each CTE alone (5 carters in my run, versus 4 in the funnel).
- **Order:** the simple version asks "did the user ever do each thing". It does not know about order or time windows (see `SQL_ORDERED`, which uses text comparison on ISO timestamps). Sessions and ordering belong to Part 8 and Part 7.
- **Empty step:** if no one purchased, `COUNT(buyer)` is 0 and `cart_to_buy` is 0 (fine). If no one carted, `bought_users / carted_users` would divide by zero (SQLite returns NULL for division by zero; I did not run that case) and pandas would raise or return inf for a float division; guard with `NULLIF` or an `if`.
- **Duplicate users in the join:** the join key `user_id` is unique in each CTE, so no step can multiply the rows.

**Then explain:**
- **Why DISTINCT users:** the question is "how many people", not "how many events". Events are many per user; the CTE brings each step to the grain of one row per user before any join (same principle as Q29 and Part 2 Q13).
- **Why LEFT JOIN from step 1:** it keeps everyone who viewed and shows NULL where a later step is missing, so `COUNT(column)` counts only the non-NULL ones. The purchase join is on `c.user_id` so only users who carted are looked up.
- **Conversion:** step-to-step is this step over the previous step; overall is the last over the first. Multiply by `1.0` so the division is not integer division in SQLite.
- **Limits of the simple version:** order ignored, no time window, no sessions, no unique-per-day definition. These are real funnel work and are Part 8.
- **pandas:** sets are the most readable form for three steps. For more steps, `isin` with chained boolean filters or a pivot of event flags per user scales better.
- **Name check:** the event names are exact strings. A misspelt `'purchase'` gives an empty step, not an error.

**Follow-ups:**
- *How would you enforce the order?* Join step tables on time, `c.event_time > v.event_time`, as in `SQL_ORDERED` (executed in the Code block); sessionisation needs window functions (later parts).
- *Why not just `COUNT(DISTINCT user_id)` with `CASE`?* You can: `COUNT(DISTINCT CASE WHEN event_name = 'view' THEN user_id END)` for each step. That counts raw reach per step, not the funnel of viewers, unless you intersect.
- *What about a time window of 24 hours?* Add the time difference to the join; date arithmetic differs by engine (not executed here).

**Common mistakes:**
- Joining raw event tables, which multiplies rows for users with repeated events.
- Counting events instead of users.
- Dividing integers in SQLite (`3 / 4` is 0) instead of using `1.0 *`.
- Reporting the simple version as if it respected order.
