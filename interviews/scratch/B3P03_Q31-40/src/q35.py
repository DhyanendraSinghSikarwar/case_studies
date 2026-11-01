# Q35: relational division: double NOT EXISTS vs GROUP BY HAVING COUNT(DISTINCT); vacuous truth
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE products(product_id INTEGER PRIMARY KEY, name TEXT, category TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, product_id INTEGER);
INSERT INTO customers VALUES (1,'Asha'),(2,'Ben'),(3,'Chitra'),(4,'Dev'),(5,'Esha');
INSERT INTO products VALUES (10,'Novel','Books'),(11,'Atlas','Books'),(12,'Diary','Books'),(20,'Pen','Stationery');
INSERT INTO orders VALUES
 (1,1,10),(2,1,11),(3,1,12),(4,1,10),
 (5,2,10),(6,2,11),
 (7,3,10),(8,3,11),(9,3,12),(10,3,20),
 (11,5,10),(12,5,10),(13,5,10);
"""
SQL_MAIN = """
SELECT c.customer_id, c.name
FROM customers c
WHERE NOT EXISTS (
  SELECT 1 FROM products p
  WHERE p.category = :cat
    AND NOT EXISTS (SELECT 1 FROM orders o
                    WHERE o.customer_id = c.customer_id AND o.product_id = p.product_id))
ORDER BY c.customer_id
"""
SQL_HAVING = """
SELECT o.customer_id
FROM orders o JOIN products p ON p.product_id = o.product_id
WHERE p.category = :cat
GROUP BY o.customer_id
HAVING COUNT(DISTINCT o.product_id) = (SELECT COUNT(*) FROM products WHERE category = :cat)
ORDER BY o.customer_id
"""
SQL_WRONG = SQL_HAVING.replace("COUNT(DISTINCT o.product_id)", "COUNT(*)")
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
for cat in ["Books", "Toys"]:
    a = [r[0] for r in con.execute(SQL_MAIN, {"cat": cat})]
    b = [r[0] for r in con.execute(SQL_HAVING, {"cat": cat})]
    w = [r[0] for r in con.execute(SQL_WRONG, {"cat": cat})]
    print("category %-6s double NOT EXISTS: %s | HAVING COUNT(DISTINCT): %s | HAVING COUNT(*): %s" % (cat, a, b, w))
a_books = pd.read_sql_query(SQL_MAIN, con, params={"cat": "Books"})
print("\nSQL double NOT EXISTS, Books:")
print(a_books.to_string(index=False))

customers = pd.read_sql_query("SELECT * FROM customers", con)
products = pd.read_sql_query("SELECT * FROM products", con)
orders = pd.read_sql_query("SELECT * FROM orders", con)
def divide(cat):
# pd:main
    needed = set(products.loc[products["category"] == cat, "product_id"])
    bought = orders.groupby("customer_id")["product_id"].agg(set)
    per_customer = customers["customer_id"].map(bought).apply(lambda s: s if isinstance(s, set) else set())
    return customers.loc[[needed.issubset(s) for s in per_customer], ["customer_id", "name"]].reset_index(drop=True)
# pd:end
pd_books = divide("Books")
print("\npandas issubset, Books:")
print(pd_books.to_string(index=False))
# compared in customer_id order
pd.testing.assert_frame_equal(a_books, pd_books)
for cat in ["Books", "Toys"]:
    a = [r[0] for r in con.execute(SQL_MAIN, {"cat": cat})]
    assert a == divide(cat)["customer_id"].tolist()
print("assert: SQL double NOT EXISTS == pandas issubset for Books and for Toys")
print("Toys (no such products): pandas rows ->", divide("Toys")["customer_id"].tolist(), "(every customer, vacuous truth, Dev included)")
b_toys = [r[0] for r in con.execute(SQL_HAVING, {"cat": "Toys"})]
print("HAVING form for Toys ->", b_toys)
print("\norder rows per customer for Books:",
      con.execute("SELECT o.customer_id, COUNT(*), COUNT(DISTINCT o.product_id) FROM orders o JOIN products p USING(product_id) WHERE p.category='Books' GROUP BY o.customer_id").fetchall(),
      "(customer, rows, distinct books)")
