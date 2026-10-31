# Debugging a bare column in GROUP BY (Q18): SQLite runs it, silently.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, status TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,1,'completed',100),(2,1,'cancelled',50),(3,1,'completed',70),
 (4,2,'refunded',200),(5,2,'completed',30);
""")

bad = "SELECT customer_id, status, SUM(amount) AS total FROM orders GROUP BY customer_id ORDER BY customer_id"
print("bare column (SQLite runs it; value of status is not defined by the query):")
print(con.execute(bad).fetchall())

# SQLite special case: with a single MIN() or MAX(), bare columns come from the row holding the min/max
mx = "SELECT customer_id, status, MAX(amount) AS top_amt FROM orders GROUP BY customer_id ORDER BY customer_id"
print("SQLite MAX special case (status of the max row):", con.execute(mx).fetchall())
two = "SELECT customer_id, status, MAX(amount), MIN(amount) FROM orders GROUP BY customer_id ORDER BY customer_id"
print("with MAX and MIN both (no special case, arbitrary row):", con.execute(two).fetchall())

# fix 1: the intended meaning is 'per customer and status'
f1 = "SELECT customer_id, status, SUM(amount) AS total FROM orders GROUP BY customer_id, status ORDER BY customer_id, status"
# fix 2: the intended meaning is 'per customer, status is an aggregate' (say which one)
f2 = ("SELECT customer_id, MAX(status) AS max_status, COUNT(DISTINCT status) AS n_statuses, SUM(amount) AS total "
      "FROM orders GROUP BY customer_id ORDER BY customer_id")
print("fix 1:", con.execute(f1).fetchall())
print("fix 2:", con.execute(f2).fetchall())

orders = pd.read_sql("SELECT * FROM orders", con)
p1 = (orders.groupby(["customer_id", "status"], as_index=False)["amount"].sum()
      .rename(columns={"amount": "total"}).sort_values(["customer_id", "status"]).reset_index(drop=True))
p2 = (orders.groupby("customer_id")
      .agg(max_status=("status", "max"), n_statuses=("status", "nunique"), total=("amount", "sum"))
      .reset_index())
pd.testing.assert_frame_equal(pd.read_sql(f1, con), p1)
pd.testing.assert_frame_equal(pd.read_sql(f2, con), p2)
print(p1.to_string(index=False)); print(p2.to_string(index=False))
print("asserts passed (fix 1 ordered by customer_id, status; fix 2 by customer_id)")

# pandas has no bare columns: asking for a non-key column needs an explicit function
print("pandas explicit first():", orders.groupby("customer_id").agg(status=("status", "first"), total=("amount", "sum")).reset_index().to_dict("records"))
