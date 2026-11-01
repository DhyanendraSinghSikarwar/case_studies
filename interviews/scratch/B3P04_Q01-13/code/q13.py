# Q13: rank an aggregate in the same query
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_id INTEGER PRIMARY KEY, region TEXT, product TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'North','A',100),(2,'North','A',50),(3,'North','B',120),(4,'North','C',120),
  (5,'North','D',30),(6,'South','A',200),(7,'South','B',80),(8,'East','C',40),(9,'East','X',NULL);
"""
SQL_MAIN = """
SELECT region, product, SUM(amount) AS total,
       RANK() OVER (PARTITION BY region ORDER BY SUM(amount) DESC) AS rnk
FROM sales
GROUP BY region, product
ORDER BY region, rnk, product
"""
SQL_CTE = """
WITH t AS (SELECT region, product, SUM(amount) AS total FROM sales GROUP BY region, product)
SELECT region, product, total,
       RANK() OVER (PARTITION BY region ORDER BY total DESC) AS rnk
FROM t
ORDER BY region, rnk, product
"""
SQL_BAD = """
SELECT region, SUM(RANK() OVER (ORDER BY amount)) FROM sales GROUP BY region
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
cte_df = pd.read_sql_query(SQL_CTE, con)
print(sql_df.to_string(index=False))
assert sql_df.equals(cte_df)
try:
    con.execute(SQL_BAD).fetchall()
except sqlite3.OperationalError as e:
    print("\nwindow function inside an aggregate ->", type(e).__name__ + ":", e)

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
tot = sales.groupby(["region", "product"], as_index=False).agg(total=("amount", lambda s: s.sum(min_count=1)))
tot["rnk"] = (tot.groupby("region")["total"]
                 .rank(method="min", ascending=False, na_option="bottom").astype(int))
# pd:end
# compared after sorting by region, rnk, product
pd.testing.assert_frame_equal(sql_df, tot.sort_values(["region", "rnk", "product"]).reset_index(drop=True), check_dtype=False)
plain = sales.groupby(["region", "product"])["amount"].sum()
print("\nplain pandas .sum() for East/X (all NaN):", plain[("East", "X")], "  SQL SUM gives NULL")
print("asserts passed: aggregate+window == CTE == pandas groupby sum then rank")
