# Debugging SUM(DISTINCT amount) and HAVING on a non-aggregated column (Q17).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, customer_id INTEGER, amount INTEGER, status TEXT);
INSERT INTO orders VALUES
 (1,1,100,'completed'),(2,1,100,'completed'),(3,1,50,'cancelled'),
 (4,2,200,'completed'),(5,2,300,'completed'),
 (6,3,40,'completed'),(7,3,40,'refunded'),(8,3,40,'completed');
""")

buggy = "SELECT customer_id, SUM(DISTINCT amount) AS revenue FROM orders GROUP BY customer_id ORDER BY customer_id"
buggy_having = ("SELECT customer_id, SUM(amount) AS revenue FROM orders GROUP BY customer_id "
                "HAVING status = 'completed' ORDER BY customer_id")
fixed = ("SELECT customer_id, SUM(amount) AS revenue FROM orders WHERE status = 'completed' "
         "GROUP BY customer_id ORDER BY customer_id")
fixed_case = ("SELECT customer_id, SUM(CASE WHEN status = 'completed' THEN amount ELSE 0 END) AS revenue "
              "FROM orders GROUP BY customer_id ORDER BY customer_id")
fixed_all = "SELECT customer_id, SUM(amount) AS revenue FROM orders GROUP BY customer_id ORDER BY customer_id"

for name, q in [("buggy SUM(DISTINCT)", buggy), ("HAVING status (bare column)", buggy_having),
                ("fixed (WHERE before GROUP BY)", fixed), ("fixed (SUM(CASE ...))", fixed_case), ("SUM(amount), all statuses", fixed_all)]:
    print(name, con.execute(q).fetchall())

# pandas check that exposes the bug
orders = pd.read_sql("SELECT * FROM orders", con)
true_all = orders.groupby("customer_id")["amount"].sum()
distinct_all = orders.groupby("customer_id")["amount"].apply(lambda s: s.drop_duplicates().sum())
check = pd.DataFrame({"sum": true_all, "sum_distinct": distinct_all})
check["lost"] = check["sum"] - check["sum_distinct"]
print(check)
print("customers where DISTINCT lost money:", check.index[check["lost"] > 0].tolist())

completed = orders[orders["status"] == "completed"].groupby("customer_id", as_index=False)["amount"].sum()
completed = completed.rename(columns={"amount": "revenue"})
sql_fixed = pd.read_sql(fixed, con)
pd.testing.assert_frame_equal(sql_fixed, completed)
pd.testing.assert_frame_equal(pd.read_sql(fixed_case, con), completed)
# the buggy SQL equals the pandas drop_duplicates version (proves what DISTINCT does)
sql_buggy = pd.read_sql(buggy, con)
assert sql_buggy["revenue"].tolist() == distinct_all.tolist()
# the real totals differ from the buggy ones for customers 1 and 3
assert true_all.tolist() != distinct_all.tolist()

# legitimate DISTINCT: count distinct customers, not rows
print("legit: COUNT(DISTINCT customer_id) =", con.execute("SELECT COUNT(DISTINCT customer_id) FROM orders").fetchone()[0],
      "| pandas nunique =", orders["customer_id"].nunique())
print("asserts passed (rows ordered by customer_id)")
