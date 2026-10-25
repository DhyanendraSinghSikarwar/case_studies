# Q1: pivot with conditional aggregation (SUM and COUNT of CASE) vs pandas pivot_table.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('East','A','Jan',100),('East','A','Jan',50),('East','B','Feb',200),('East','A','Mar',30),
 ('West','A','Feb',80),('West','B','Feb',20),('West','B','Mar',60),
 ('North','A','Mar',40);
""")

sql_sum = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS mar,
       SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY region
"""
sql_else0 = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount ELSE 0 END) AS jan,
       SUM(CASE WHEN month = 'Feb' THEN amount ELSE 0 END) AS feb,
       SUM(CASE WHEN month = 'Mar' THEN amount ELSE 0 END) AS mar,
       SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY region
"""
sql_count = """
SELECT region,
       COUNT(CASE WHEN month = 'Jan' THEN 1 END) AS jan_n,
       COUNT(CASE WHEN month = 'Feb' THEN 1 END) AS feb_n,
       COUNT(CASE WHEN month = 'Mar' THEN 1 END) AS mar_n
FROM sales
GROUP BY region
ORDER BY region
"""
sql_filter = """
SELECT region,
       SUM(amount) FILTER (WHERE month = 'Jan') AS jan,
       SUM(amount) FILTER (WHERE month = 'Feb') AS feb,
       SUM(amount) FILTER (WHERE month = 'Mar') AS mar,
       SUM(amount) AS total
FROM sales
GROUP BY region
ORDER BY region
"""

def show(title, q):
    df = pd.read_sql(q, con)
    print(title); print(df.to_string(index=False)); print()
    return df

s_sum = show("SUM(CASE) no ELSE (missing month = NULL):", sql_sum)
s_else0 = show("SUM(CASE ... ELSE 0) (missing month = 0):", sql_else0)
s_cnt = show("COUNT(CASE ... THEN 1 END):", sql_count)
s_fil = show("SUM(amount) FILTER (WHERE ...):", sql_filter)
assert s_sum.equals(s_fil)

# wrong version: CASE outside the aggregate needs GROUP BY region, month and gives one row per month
wrong = pd.read_sql("SELECT region, CASE WHEN month='Jan' THEN SUM(amount) END AS jan "
                    "FROM sales GROUP BY region, month ORDER BY region, month", con)
print("CASE outside SUM, grouped by region and month: %d rows instead of 3" % len(wrong)); print()

# pandas
sales = pd.read_sql("SELECT * FROM sales", con)
months = ["Jan", "Feb", "Mar"]
pt = sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum")
print("pivot_table default column order:", list(pt.columns))
pt = pt[months]
pt.columns = [m.lower() for m in months]
pt["total"] = sales.groupby("region")["amount"].sum()
p_sum = pt.reset_index().rename_axis(columns=None).sort_values("region").reset_index(drop=True)
print(p_sum.to_string(index=False)); print()

cnt = sales.pivot_table(index="region", columns="month", values="amount", aggfunc="count", fill_value=0)
cnt = cnt[months]
cnt.columns = [m.lower() + "_n" for m in months]
p_cnt = cnt.reset_index().rename_axis(columns=None).sort_values("region").reset_index(drop=True)

# compare after sorting by region; NaN in pandas == NULL in SQL (read_sql gives NaN for NULL)
pd.testing.assert_frame_equal(s_sum.sort_values("region").reset_index(drop=True), p_sum, check_dtype=False)
pd.testing.assert_frame_equal(s_cnt.sort_values("region").reset_index(drop=True), p_cnt, check_dtype=False)
print("pivot_table with fill_value=0 turns the missing West/Jan into 0:",
      sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", fill_value=0).loc["West", "Jan"])
print("asserts passed (compared after sorting by region)")
