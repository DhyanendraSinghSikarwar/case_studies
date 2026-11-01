# Q1: read EXPLAIN QUERY PLAN output on a 200,000-row orders table.
import random
import sqlite3
import pandas as pd

random.seed(1)
con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE customers(customer_id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, order_date TEXT,
                    status TEXT, amount REAL);
""")
cities = ["Pune", "Delhi", "Chennai", "Mumbai"]
con.executemany("INSERT INTO customers VALUES (?,?,?)",
                [(i, f"cust{i}", cities[i % 4]) for i in range(1, 20001)])
statuses = ["placed", "shipped", "delivered", "cancelled"]
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)",
                [(i, random.randint(1, 20000),
                  f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
                  random.choice(statuses), round(random.uniform(10, 500), 2))
                 for i in range(1, 200001)])
con.commit()

_n = [0]
def plan(sql):
    # python's statement cache can replay a stale plan after DROP/CREATE INDEX, so vary the text
    _n[0] += 1
    rows = con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]).fetchall()
    return [r[3] for r in rows]

queries = {
    "A  filter":        "SELECT * FROM orders WHERE customer_id = 5",
    "B  covering":      "SELECT customer_id, order_id FROM orders WHERE customer_id = 5",
    "C  order by amt":  "SELECT * FROM orders WHERE customer_id = 5 ORDER BY amount",
    "D  distinct":      "SELECT DISTINCT status FROM orders",
    "E  group by":      "SELECT status, COUNT(*) FROM orders GROUP BY status",
    "F  order by cust": "SELECT * FROM orders ORDER BY customer_id LIMIT 10",
}
print("-- BEFORE CREATE INDEX")
for k, q in queries.items():
    print(k, "->", plan(q))
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
print("\n-- AFTER CREATE INDEX ix_cust ON orders(customer_id)")
for k, q in queries.items():
    print(k, "->", plan(q))

# the plan is a 4-column row: id, parent, notused, detail
print("\nraw row:", con.execute("EXPLAIN QUERY PLAN SELECT * FROM orders WHERE customer_id = 5 ").fetchall())

# a join, to show nested plan lines (parent column)
for r in con.execute("EXPLAIN QUERY PLAN SELECT c.name, o.amount FROM customers c "
                     "JOIN orders o ON o.customer_id = c.customer_id WHERE c.city = 'Pune'  "):
    print("join:", r)

# VM steps as a cost proxy
def steps(sql):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    rows = con.execute(sql).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], rows
con.execute("DROP INDEX ix_cust")
s0, r0 = steps("SELECT * FROM orders WHERE customer_id = 5")
con.execute("CREATE INDEX ix_cust ON orders(customer_id)")
s1, r1 = steps("SELECT * FROM orders WHERE customer_id = 5")
print("\nVM steps scan:", s0, " with index:", s1, " rows:", len(r0), len(r1))

# pandas: boolean mask (scan) vs set_index + loc (index), same rows
df = pd.read_sql("SELECT * FROM orders", con)
mask = df[df.customer_id == 5].sort_values("order_id").reset_index(drop=True)
idx = df.set_index("customer_id").loc[[5]].reset_index().sort_values("order_id").reset_index(drop=True)
idx = idx[mask.columns]
pd.testing.assert_frame_equal(mask, idx)
sql_rows = pd.DataFrame(sorted(r1), columns=mask.columns)
pd.testing.assert_frame_equal(mask, sql_rows, check_dtype=False)
print("asserts passed (SQL rows, boolean mask and indexed loc equal after sorting by order_id)")
print("distinct statuses:", sorted(df.status.unique()), "vs SQL:", sorted(r[0] for r in con.execute("SELECT DISTINCT status FROM orders")))
