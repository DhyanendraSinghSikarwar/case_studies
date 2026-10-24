# Q1: the five join types on one small dataset, SQL (SQLite 3.45) versus pandas how=.
import sqlite3
import pandas as pd

print("SQLite", sqlite3.sqlite_version, "| pandas", pd.__version__)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER);
INSERT INTO customers VALUES (1,'Asha','Pune'),(2,'Ben','Delhi'),(3,'Chitra','Pune'),(4,'Dev','Delhi');
INSERT INTO orders VALUES (101,1,100),(102,1,50),(103,2,75),(104,NULL,30),(105,3,20);
""")

COLS = "c.customer_id AS c_id, c.name, o.order_id, o.customer_id AS o_cust, o.amount"
sql = {
 "inner": f"SELECT {COLS} FROM customers c INNER JOIN orders o ON o.customer_id = c.customer_id",
 "left":  f"SELECT {COLS} FROM customers c LEFT JOIN orders o ON o.customer_id = c.customer_id",
 "right": f"SELECT {COLS} FROM customers c RIGHT JOIN orders o ON o.customer_id = c.customer_id",
 "outer": f"SELECT {COLS} FROM customers c FULL OUTER JOIN orders o ON o.customer_id = c.customer_id",
 "cross": f"SELECT {COLS} FROM customers c CROSS JOIN orders o",
}
# RIGHT JOIN is a LEFT JOIN with the tables swapped (same rows, columns listed the same way)
sql_swapped = f"SELECT {COLS} FROM orders o LEFT JOIN customers c ON o.customer_id = c.customer_id"

def rows(items):
    """Normalise to a sorted list of tuples: NaN -> None, whole floats -> int."""
    out = []
    for r in items:
        t = []
        for x in r:
            if x is None or (isinstance(x, float) and x != x): x = None
            elif isinstance(x, float) and x.is_integer(): x = int(x)
            t.append(x)
        out.append(tuple(t))
    return sorted(out, key=lambda t: tuple((v is None, str(v)) for v in t))

customers = pd.read_sql("SELECT * FROM customers", con)
orders = pd.read_sql("SELECT * FROM orders", con).rename(columns={"customer_id": "o_cust"})
orders["c_key"] = orders["o_cust"]          # keep both key columns visible, like the SQL output
customers["c_id"] = customers["customer_id"]

for how in ["inner", "left", "right", "outer", "cross"]:
    s = rows(con.execute(sql[how]).fetchall())
    if how == "cross":
        p = customers.merge(orders, how="cross")
    else:
        p = customers.merge(orders, how=how, left_on="c_id", right_on="c_key")
    p = rows(p[["c_id", "name", "order_id", "o_cust", "amount"]].itertuples(index=False, name=None))
    assert s == p, how                      # compared after sorting all rows
    print(f"{how:5s} -> {len(s):2d} rows (SQL == pandas)")

assert rows(con.execute(sql["right"]).fetchall()) == rows(con.execute(sql_swapped).fetchall())
print("RIGHT JOIN == swapped LEFT JOIN: True")
print("\nFULL OUTER rows (order_id sort, None = NULL):")
for r in sorted(rows(con.execute(sql["outer"]).fetchall()), key=lambda t: (t[2] is None, t[2] or 0, t[0] or 0)):
    print(r)
print("asserts passed")
