# SQL vs pandas NULL differences in GROUP BY and aggregates (Q16).
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, region TEXT, amount REAL);
INSERT INTO orders VALUES
 (1,'North',100),(2,'North',NULL),(3,'North',50),
 (4,'South',NULL),(5,'South',NULL),
 (6,NULL,30),(7,NULL,NULL),(8,'East',20);
""")

sql = """
SELECT region,
       COUNT(*)      AS n_rows,
       COUNT(amount) AS n_amount,
       SUM(amount)   AS total,
       AVG(amount)   AS avg_amt
FROM orders
GROUP BY region
ORDER BY region IS NULL, region
"""
sql_df = pd.read_sql(sql, con)
print("SQL:"); print(sql_df.to_string(index=False))

orders = pd.read_sql("SELECT * FROM orders", con)

# default pandas: NaN keys dropped, SUM of nothing = 0
naive = orders.groupby("region").agg(n_rows=("order_id", "size"), n_amount=("amount", "count"),
                                     total=("amount", "sum"), avg_amt=("amount", "mean"))
print("\npandas defaults (dropna=True, sum without min_count):"); print(naive)

# matched to SQL: keep the NaN group, min_count=1 so an all-NaN group sums to NaN
matched = (orders.groupby("region", dropna=False)
           .agg(n_rows=("order_id", "size"), n_amount=("amount", "count"),
                total=("amount", lambda s: s.sum(min_count=1)), avg_amt=("amount", "mean"))
           .reset_index()
           .sort_values("region", na_position="last")
           .reset_index(drop=True))
print("\npandas matched to SQL:"); print(matched.to_string(index=False))

# compare: NULL/NaN treated as equal, int columns as int64
pd.testing.assert_frame_equal(sql_df, matched, check_dtype=True)
print("\nasserts passed: SQL == matched pandas (rows ordered by region, NULL region last)")

# whole-table behaviour: all-NULL column
empty_like = orders[orders["region"] == "South"]["amount"]
print("pandas sum of all-NaN:", empty_like.sum(), "| with min_count=1:", empty_like.sum(min_count=1))
print("SQL SUM of all-NULL group:", con.execute("SELECT SUM(amount) FROM orders WHERE region='South'").fetchone()[0],
      "| TOTAL():", con.execute("SELECT TOTAL(amount) FROM orders WHERE region='South'").fetchone()[0],
      "| AVG:", con.execute("SELECT AVG(amount) FROM orders WHERE region='South'").fetchone()[0])
print("pandas mean of all-NaN:", empty_like.mean())
