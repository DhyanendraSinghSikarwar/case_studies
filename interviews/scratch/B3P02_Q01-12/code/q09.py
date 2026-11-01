# Q9: duplicate keys in a lookup table inflate a join; detect, fix, guard.
import sqlite3
import pandas as pd
from pandas.errors import MergeError

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE products(product_id INTEGER, name TEXT, price INTEGER);      -- no PK: loaded twice
CREATE TABLE order_items(item_id INTEGER PRIMARY KEY, order_id INTEGER, product_id INTEGER, qty INTEGER);
INSERT INTO products VALUES (1,'Pen',10),(1,'Pen',10),(2,'Book',20),(3,'Cap',5);
INSERT INTO order_items VALUES (1,1,1,2),(2,1,2,1),(3,2,3,4);
""")
run = lambda q: con.execute(q).fetchall()

truth = run("SELECT SUM(qty * (SELECT MAX(price) FROM products p WHERE p.product_id = i.product_id)) FROM order_items i")[0][0]
bad = run("""SELECT COUNT(*), SUM(i.qty * p.price) FROM order_items i JOIN products p ON p.product_id = i.product_id""")[0]
print("true revenue:", truth, "| joined rows, revenue:", bad, "(3 items became", bad[0], "rows)")

sql_detect = "SELECT product_id, COUNT(*) AS n FROM products GROUP BY product_id HAVING COUNT(*) > 1"
print("duplicate keys:", run(sql_detect))
sql_fix = """SELECT COUNT(*), SUM(i.qty * p.price) FROM order_items i
JOIN (SELECT DISTINCT product_id, name, price FROM products) p ON p.product_id = i.product_id"""
fixed = run(sql_fix)[0]
print("after DISTINCT in a derived table:", fixed)
assert fixed == (3, truth) and bad == (4, 80) and truth == 60

# conflicting duplicates would survive DISTINCT: it keeps both rows
con.execute("INSERT INTO products VALUES (2,'Book',25)")
print("DISTINCT with a conflicting price keeps", run("SELECT COUNT(*) FROM (SELECT DISTINCT product_id, name, price FROM products) WHERE product_id=2")[0][0], "rows for product 2")
con.execute("DELETE FROM products WHERE price = 25")

# fix at the source: a key constraint rejects the second load
con.executescript("""CREATE TABLE products_clean(product_id INTEGER PRIMARY KEY, name TEXT, price INTEGER);
INSERT INTO products_clean SELECT DISTINCT product_id, name, price FROM products;""")
try:
    con.execute("INSERT INTO products_clean VALUES (1,'Pen',10)")
except sqlite3.IntegrityError as e:
    print("IntegrityError:", e)

# pandas
products = pd.read_sql("SELECT * FROM products", con)
items = pd.read_sql("SELECT * FROM order_items", con)
print("duplicated product_id rows:\n", products[products.duplicated("product_id", keep=False)].to_string(index=False))
m = items.merge(products, on="product_id")
print("naive merge:", len(m), "rows, revenue", int((m["qty"] * m["price"]).sum()))
try:
    items.merge(products, on="product_id", validate="many_to_one")
except MergeError as e:
    print("MergeError:", e)
clean = products.drop_duplicates(subset=["product_id", "name", "price"])
m2 = items.merge(clean, on="product_id", validate="many_to_one")
rev = int((m2["qty"] * m2["price"]).sum())
print("after drop_duplicates + validate:", len(m2), "rows, revenue", rev)
assert (len(m), int((m["qty"] * m["price"]).sum())) == bad and (len(m2), rev) == fixed
print("asserts passed")
