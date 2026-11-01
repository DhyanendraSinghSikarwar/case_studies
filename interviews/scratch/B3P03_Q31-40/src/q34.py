# Q34: empty results inside subqueries
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price INTEGER);
INSERT INTO products VALUES (1,'Pen','Stationery',10),(2,'Book','Books',20),(3,'Bag','Bags',50),(4,'Ball','Sports',30);
"""
# one row of aggregates over an empty set (there are no Toys)
SQL_MAIN = """
SELECT COUNT(*)      AS n,
       COUNT(price)  AS n_price,
       MAX(price)    AS max_price,
       SUM(price)    AS sum_price,
       TOTAL(price)  AS total_price,
       AVG(price)    AS avg_price
FROM products WHERE category = 'Toys'
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
def q(sql):
    return con.execute(sql).fetchall()
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL aggregates over an empty set (WHERE category = 'Toys'):")
print(sql_df.to_string(index=False))

products = pd.read_sql_query("SELECT * FROM products", con)
# pd:main
toys = products.loc[products["category"] == "Toys", "price"]
pd_df = pd.DataFrame({
    "n": [len(toys)], "n_price": [toys.count()], "max_price": [toys.max()],
    "sum_price": [toys.sum(min_count=1)], "total_price": [float(toys.sum())], "avg_price": [toys.mean()],
})
# pd:end
print("\npandas on the empty Series:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.astype({"max_price": "float64", "sum_price": "float64", "avg_price": "float64"}), pd_df, check_dtype=False)
print("assert: SQL aggregates == pandas (one row; SUM needs min_count=1, TOTAL is 0.0 like sum())")

print("\n--- comparisons against the empty-set aggregate ---")
cmp_ = "SELECT COUNT(*) FROM products WHERE price > (SELECT MAX(price) FROM products WHERE category = 'Toys')"
print("price > (max of Toys)               ->", q(cmp_)[0][0], "rows")
print("price > COALESCE(max of Toys, 0)    ->", q("SELECT COUNT(*) FROM products WHERE price > COALESCE((SELECT MAX(price) FROM products WHERE category = 'Toys'), 0)")[0][0], "rows")
print("a scalar subquery that returns zero rows is NULL too:",
      q("SELECT (SELECT price FROM products WHERE category = 'Toys')"))
print("pandas products.price > NaN         ->", int((products.price > toys.max()).sum()), "rows")
mx = toys.max()
thr = 0 if pd.isna(mx) else mx
print("pandas with the COALESCE idea       ->", int((products.price > thr).sum()), "rows")

print("\n--- IN, NOT IN, EXISTS over the empty set ---")
for label, sql in [
    ("IN (empty)", "SELECT COUNT(*) FROM products WHERE product_id IN (SELECT product_id FROM products WHERE category = 'Toys')"),
    ("NOT IN (empty)", "SELECT COUNT(*) FROM products WHERE product_id NOT IN (SELECT product_id FROM products WHERE category = 'Toys')"),
    ("EXISTS (empty)", "SELECT COUNT(*) FROM products WHERE EXISTS (SELECT 1 FROM products WHERE category = 'Toys')"),
    ("NOT EXISTS (empty)", "SELECT COUNT(*) FROM products WHERE NOT EXISTS (SELECT 1 FROM products WHERE category = 'Toys')"),
]:
    print("%-20s -> %d rows" % (label, q(sql)[0][0]))
print("scalar form: 5 IN (empty) =", q("SELECT 5 IN (SELECT price FROM products WHERE category='Toys')")[0][0],
      "| 5 NOT IN (empty) =", q("SELECT 5 NOT IN (SELECT price FROM products WHERE category='Toys')")[0][0],
      "| NULL IN (empty) =", q("SELECT NULL IN (SELECT price FROM products WHERE category='Toys')")[0][0],
      "| NULL NOT IN (empty) =", q("SELECT NULL NOT IN (SELECT price FROM products WHERE category='Toys')")[0][0])
print("EXISTS (empty) as a value:", q("SELECT EXISTS (SELECT 1 FROM products WHERE category='Toys')")[0][0])
n_in = int(products.product_id.isin(products.loc[products.category == "Toys", "product_id"]).sum())
print("pandas isin(empty) rows:", n_in, "| ~isin(empty) rows:", int((~products.product_id.isin(products.loc[products.category == "Toys", "product_id"])).sum()))
assert q(cmp_)[0][0] == int((products.price > toys.max()).sum()) == 0
assert q("SELECT COUNT(*) FROM products WHERE price > COALESCE((SELECT MAX(price) FROM products WHERE category = 'Toys'), 0)")[0][0] == int((products.price > thr).sum()) == 4

print("\n--- when you want the row anyway: keep a row even if the subquery is empty ---")
keep = """
SELECT p.name, p.price FROM products p
WHERE p.price > (SELECT MAX(price) FROM products WHERE category = 'Books')
   OR NOT EXISTS (SELECT 1 FROM products WHERE category = 'Books')
ORDER BY p.product_id"""
print("pricier than every Book (Books exist):", q(keep))
print("same query, category 'Toys' instead  :", q(keep.replace("'Books'", "'Toys'")))
