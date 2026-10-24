# Q5: left join to get zeros for unsold products.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'Pen'),(2,'Book'),(3,'Bag'),(4,'Cap');
INSERT INTO sales VALUES (1,1,5),(2,1,3),(3,2,4);
""")

sql = """SELECT p.name, COALESCE(SUM(s.qty), 0) AS units, COUNT(s.sale_id) AS n_sales
FROM products p LEFT JOIN sales s ON s.product_id = p.product_id
GROUP BY p.product_id, p.name ORDER BY p.product_id"""
sql_bad = """SELECT p.name, COUNT(*) AS wrong_count, COUNT(s.sale_id) AS right_count, SUM(s.qty) AS raw_sum
FROM products p LEFT JOIN sales s ON s.product_id = p.product_id
GROUP BY p.product_id, p.name ORDER BY p.product_id"""
s = con.execute(sql).fetchall()
print("SQL:", s)
for r in con.execute(sql_bad): print("COUNT(*) vs COUNT(s.sale_id) vs raw SUM:", r)

products = pd.read_sql("SELECT * FROM products", con)
sales = pd.read_sql("SELECT * FROM sales", con)
m = products.merge(sales, on="product_id", how="left")
print("qty dtype after merge:", m["qty"].dtype)
g = m.groupby(["product_id", "name"], as_index=False).agg(units=("qty", "sum"), n_sales=("sale_id", "count"))
print("units dtype straight out of groupby sum:", g["units"].dtype, "(float64, because qty was float64)")
g_min = m.groupby("name")["qty"].sum(min_count=1)
print("sum(min_count=1) for Bag:", g_min["Bag"], "(NaN, the SQL-style raw SUM)")
g["units"] = g["units"].fillna(0).astype("int64")      # fillna alone keeps float64; astype restores int
print("dtype after fillna + astype:", g["units"].dtype)
print(g[["name", "units", "n_sales"]].to_string(index=False))

# the pandas trap equivalent to COUNT(*): size() counts the NaN row from the left join
print("size() per product (like COUNT(*)):", m.groupby("name").size().to_dict())

assert list(g[["name", "units", "n_sales"]].itertuples(index=False, name=None)) == s
assert s == [("Pen", 8, 2), ("Book", 4, 1), ("Bag", 0, 0), ("Cap", 0, 0)]
print("asserts passed (compared in product_id order)")
