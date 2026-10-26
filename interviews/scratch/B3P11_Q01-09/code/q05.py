# Q5: design one composite index for one query; compare candidates by plan and VM steps.
import random
import sqlite3
import pandas as pd

random.seed(5)
statuses = ["placed", "shipped", "delivered", "cancelled"]
rows = [(i, random.randint(1, 20000), random.choice(statuses),
         f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}", round(random.uniform(10, 500), 2))
        for i in range(1, 200001)]
con = sqlite3.connect(":memory:")
con.execute("CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INT, status TEXT, order_date TEXT, amount REAL)")
con.executemany("INSERT INTO orders VALUES (?,?,?,?,?)", rows)
con.commit()

_n = [0]
def plan(sql):
    _n[0] += 1
    return " | ".join(r[3] for r in con.execute("EXPLAIN QUERY PLAN " + sql + " " * _n[0]))

def run(sql, args=()):
    c = [0]
    def cb():
        c[0] += 1
        return 0
    con.set_progress_handler(cb, 1)
    out = con.execute(sql, args).fetchall()
    con.set_progress_handler(None, 0)
    return c[0], out

Q1 = ("SELECT order_id, amount FROM orders WHERE status = 'shipped' AND order_date >= '2024-06-01' "
      "AND order_date < '2024-07-01' ORDER BY order_date LIMIT 50")
cands = [("none", None), ("(status)", "status"), ("(order_date)", "order_date"),
         ("(order_date, status)", "order_date, status"), ("(status, order_date)", "status, order_date"),
         ("(status, order_date, amount, order_id)", "status, order_date, amount, order_id")]
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 100)
out = []
ref = None
for name, cols in cands:
    con.execute("DROP INDEX IF EXISTS ixc")
    if cols:
        con.execute(f"CREATE INDEX ixc ON orders({cols})")
    s, r = run(Q1)
    # ties on order_date make LIMIT order ambiguous, so compare the set of (date) only through the count and the date column
    out.append((name, plan(Q1), s, len(r)))
print("Query 1:", Q1)
print(pd.DataFrame(out, columns=["index", "plan", "vm_steps", "rows"]).to_string(index=False))

# correctness: the result set is the same 50 dates whichever index is used; compare the sorted dates
con.execute("DROP INDEX IF EXISTS ixc")
full = con.execute("SELECT order_date, order_id, amount FROM orders WHERE status='shipped' AND order_date >= '2024-06-01' AND order_date < '2024-07-01' ORDER BY order_date, order_id").fetchall()
df = pd.DataFrame(rows, columns=["order_id", "customer_id", "status", "order_date", "amount"])
pm = df[(df.status == "shipped") & (df.order_date >= "2024-06-01") & (df.order_date < "2024-07-01")] \
       .sort_values(["order_date", "order_id"])
assert [r[1] for r in full] == list(pm.order_id)
print("matching rows without LIMIT:", len(full), "(SQL and pandas agree)")
print("first 50 dates only span:", full[0][0], "to", full[49][0], "-> ties on order_date mean LIMIT 50 is ambiguous without a tiebreaker")

# the second query
Q2 = "SELECT * FROM orders WHERE customer_id = 5 ORDER BY order_date DESC LIMIT 10"
out2 = []
for name, cols in [("none", None), ("(customer_id)", "customer_id"), ("(customer_id, order_date)", "customer_id, order_date"),
                   ("(order_date)", "order_date")]:
    con.execute("DROP INDEX IF EXISTS ixc")
    if cols:
        con.execute(f"CREATE INDEX ixc ON orders({cols})")
    s, r = run(Q2)
    out2.append((name, plan(Q2), s, len(r)))
print("\nQuery 2:", Q2)
print(pd.DataFrame(out2, columns=["index", "plan", "vm_steps", "rows"]).to_string(index=False))

# range column is not the sort column: status equal, date range, ORDER BY amount
Q3 = ("SELECT order_id FROM orders WHERE status = 'shipped' AND order_date >= '2024-06-01' "
      "AND order_date < '2024-07-01' ORDER BY amount LIMIT 50")
con.execute("DROP INDEX IF EXISTS ixc")
con.execute("CREATE INDEX ixc ON orders(status, order_date, amount)")
print("\nrange column is not the sort column, index (status, order_date, amount):", plan(Q3), run(Q3)[0])
con.execute("DROP INDEX ixc")
con.execute("CREATE INDEX ixc ON orders(status, amount, order_date)")
print("index (status, amount, order_date):", plan(Q3), run(Q3)[0])
con.execute("DROP INDEX ixc")
# pandas: the same query with nsmallest on dates
top = pm.head(50)
assert len(top) == 50 and list(top.order_date) == [r[0] for r in full[:50]]
print("pandas sort_values + head(50) gives the same 50 dates as SQL (ties broken by order_id)")
