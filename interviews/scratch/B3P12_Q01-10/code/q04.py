# Q4: relational division: customers who bought ALL featured products. Double NOT EXISTS, HAVING COUNT(DISTINCT), pandas.
import sqlite3
import pandas as pd

def build():
    con = sqlite3.connect(":memory:")
    con.executescript("""
    CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER);
    CREATE TABLE order_items(order_id INTEGER, product_id INTEGER);
    CREATE TABLE featured(product_id INTEGER PRIMARY KEY);
    INSERT INTO featured VALUES (101),(102),(103);
    INSERT INTO orders VALUES (1,1),(2,1),(3,2),(4,2),(5,3),(6,4),(7,5);
    INSERT INTO order_items VALUES
     (1,101),(1,102),(2,102),(2,103),   -- cust 1: all three, product 102 twice
     (3,101),(3,101),(3,102),           -- cust 2: duplicate rows, only 101 and 102
     (4,101),                           -- cust 2: 101 again
     (5,101),(5,102),(5,103),(5,999),   -- cust 3: all three plus a non-featured product
     (6,555),                           -- cust 4: no featured product
     (7,103);                           -- cust 5: one featured product
    """)
    return con

con = build()
not_exists = """
SELECT c.customer_id
FROM (SELECT DISTINCT customer_id FROM orders) c
WHERE NOT EXISTS (
  SELECT 1 FROM featured f
  WHERE NOT EXISTS (
    SELECT 1 FROM orders o JOIN order_items i ON i.order_id = o.order_id
    WHERE o.customer_id = c.customer_id AND i.product_id = f.product_id))
ORDER BY c.customer_id
"""
having = """
SELECT o.customer_id
FROM orders o
JOIN order_items i ON i.order_id = o.order_id
JOIN featured f ON f.product_id = i.product_id
GROUP BY o.customer_id
HAVING COUNT(DISTINCT f.product_id) = (SELECT COUNT(*) FROM featured)
ORDER BY o.customer_id
"""
wrong = """
SELECT o.customer_id, COUNT(*) AS rows_hit, COUNT(DISTINCT f.product_id) AS distinct_hit
FROM orders o JOIN order_items i ON i.order_id = o.order_id JOIN featured f ON f.product_id = i.product_id
GROUP BY o.customer_id ORDER BY o.customer_id
"""
a = pd.read_sql(not_exists, con); b = pd.read_sql(having, con)
print("double NOT EXISTS:", a.customer_id.tolist())
print("HAVING COUNT(DISTINCT):", b.customer_id.tolist())
print("rows vs distinct featured hits per customer (COUNT(*) >= 3 would wrongly pass customer 2):")
print(pd.read_sql(wrong, con).to_string(index=False)); print()

# pandas
orders = pd.read_sql("SELECT * FROM orders", con); items = pd.read_sql("SELECT * FROM order_items", con)
featured = pd.read_sql("SELECT * FROM featured", con)
def division(orders, items, featured):
    hit = orders.merge(items, on="order_id").merge(featured, on="product_id")[["customer_id", "product_id"]].drop_duplicates()
    cnt = hit.groupby("customer_id")["product_id"].nunique()
    return sorted(cnt[cnt == len(featured)].index.tolist())
p = division(orders, items, featured)
print("pandas nunique == len(featured):", p)
assert a.customer_id.tolist() == b.customer_id.tolist() == p
print("asserts passed (compared as sorted customer_id lists)"); print()

# empty featured list
con.execute("DELETE FROM featured")
a0 = pd.read_sql(not_exists, con).customer_id.tolist(); b0 = pd.read_sql(having, con).customer_id.tolist()
p0 = division(orders, items, featured.iloc[0:0])
sets = items.merge(orders, on="order_id").groupby("customer_id")["product_id"].agg(set)
p0_sets = sorted(sets[sets.apply(lambda s: set(featured.iloc[0:0]["product_id"]) <= s)].index.tolist())
print("empty featured -> NOT EXISTS:", a0, "| HAVING:", b0, "| pandas merge/nunique:", p0, "| pandas set subset:", p0_sets)
