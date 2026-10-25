# Q10: pivot totals that do not match: dirty labels, NULL month, NULL amounts; reconciliation and self-check.
import sqlite3
import numpy as np
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE sales(id INTEGER PRIMARY KEY, region TEXT, product TEXT, month TEXT, amount INTEGER);
INSERT INTO sales VALUES
 (1,'East','A','Jan',100),(2,'East','A','Feb',50),(3,'East','B','Mar',NULL),(4,'East','B','jan',30),
 (5,'West','A',' Feb',70),(6,'West','A','Mar',40),(7,'West','B','Apr',20),(8,'West','B',NULL,10),
 (9,'North','A','Jan',60),(10,'North','A','Feb',NULL),
 (11,'West','A','Jan',15),(12,'West','A','Feb',25);
""")

sql_teammate = """
SELECT region,
       SUM(CASE WHEN month = 'Jan' THEN amount END) AS jan,
       SUM(CASE WHEN month = 'Feb' THEN amount END) AS feb,
       SUM(CASE WHEN month = 'Mar' THEN amount END) AS mar,
       SUM(CASE WHEN month = 'Jan' THEN amount END)
     + SUM(CASE WHEN month = 'Feb' THEN amount END)
     + SUM(CASE WHEN month = 'Mar' THEN amount END) AS total
FROM sales GROUP BY region ORDER BY region
"""
sql_fixed = """
WITH s AS (SELECT region, LOWER(TRIM(month)) AS m, amount FROM sales)
SELECT region,
       SUM(CASE WHEN m = 'jan' THEN amount END) AS jan,
       SUM(CASE WHEN m = 'feb' THEN amount END) AS feb,
       SUM(CASE WHEN m = 'mar' THEN amount END) AS mar,
       SUM(CASE WHEN m IS NULL OR m NOT IN ('jan', 'feb', 'mar') THEN amount END) AS other,
       SUM(amount) AS total
FROM s GROUP BY region ORDER BY region
"""
def make_check(pivot_sql, parts):
    """Rows that disagree with the plain SUM(amount), per region and for the grand total. Zero rows = reconciled."""
    pivot_sql = pivot_sql.replace(" ORDER BY region", "")
    return f"""
WITH pivot AS ({pivot_sql}), plain AS (SELECT region, SUM(amount) AS total FROM sales GROUP BY region)
SELECT p.region, {parts} AS parts, pl.total AS plain_total
FROM pivot p JOIN plain pl ON pl.region = p.region
WHERE {parts} <> COALESCE(pl.total, 0)
UNION ALL
SELECT 'GRAND', SUM({parts}), (SELECT SUM(amount) FROM sales)
FROM pivot p
HAVING SUM({parts}) <> (SELECT SUM(amount) FROM sales)
"""

parts_fixed = "COALESCE(p.jan, 0) + COALESCE(p.feb, 0) + COALESCE(p.mar, 0) + COALESCE(p.other, 0)"
parts_teammate = "COALESCE(p.jan, 0) + COALESCE(p.feb, 0) + COALESCE(p.mar, 0)"
sql_check = make_check(sql_fixed, parts_fixed)
sql_check_teammate = make_check(sql_teammate, parts_teammate)
sql_in_other = """
SELECT month, COUNT(*) AS n_rows, SUM(amount) AS amount
FROM sales
WHERE LOWER(TRIM(month)) IS NULL OR LOWER(TRIM(month)) NOT IN ('jan', 'feb', 'mar')
GROUP BY month ORDER BY month
"""

print("plain SUM(amount):", con.execute("SELECT SUM(amount) FROM sales").fetchone()[0])
t = pd.read_sql(sql_teammate, con)
print("\nteammate pivot (jan + feb + mar):"); print(t.to_string(index=False))
print("sum of the teammate total column:", t.total.sum(), "vs SUM(amount) above")
print("distinct month labels:", [r[0] for r in con.execute("SELECT DISTINCT month FROM sales ORDER BY 1")])

f = pd.read_sql(sql_fixed, con)
print("\nfixed pivot with other and a direct SUM(amount) total:"); print(f.to_string(index=False))
print("pivot grand total:", f.total.sum(), "| sum of the five parts:", f[["jan", "feb", "mar", "other"]].fillna(0).sum().sum())
bad = con.execute(sql_check_teammate).fetchall()
print("\nself-check on the teammate's pivot (parts vs total, no 'other'):", bad)
good = con.execute(sql_check).fetchall()
print("self-check on the fixed pivot returns:", good)
assert good == []

print("what lands in other (month label, rows, amount):", con.execute(sql_in_other).fetchall())

# pandas
sales = pd.read_sql("SELECT * FROM sales", con)
raw = sales.pivot_table(index="region", columns="month", values="amount", aggfunc="sum", margins=True, margins_name="total")
print("\npandas pivot_table on the raw labels, margins=True:"); print(raw)
print("pandas grand total cell:", raw.loc["total", "total"], "vs df.amount.sum():", sales.amount.sum(),
      "(rows with a NaN month key are dropped from the pivot)")

m = sales.month.str.strip().str.lower()
m = m.where(m.isin(["jan", "feb", "mar"]), "other")     # NaN is not in the list, so it becomes 'other'
sales["m"] = m
pt = sales.pivot_table(index="region", columns="m", values="amount", aggfunc="sum", margins=True, margins_name="total")
pt = pt.reindex(columns=["jan", "feb", "mar", "other", "total"]).reset_index().rename_axis(columns=None)
grand = pt.loc[pt.region == "total", "total"].item()
pt = pt[pt.region != "total"].sort_values("region").reset_index(drop=True)
print("\npandas fixed pivot (margins=True):"); print(pt.to_string(index=False))
assert grand == sales.amount.sum() == con.execute("SELECT SUM(amount) FROM sales").fetchone()[0]

# SQL gives NULL for a cell whose rows all have NULL amounts, pandas sum gives 0: compare after filling both with 0
pd.testing.assert_frame_equal(f.fillna(0), pt.fillna(0), check_dtype=False)
print("East/Mar: SQL", f.set_index('region').loc['East', 'mar'], "| pandas", pt.set_index('region').loc['East', 'mar'])
print("asserts passed (compared after sorting by region, NULL/NaN filled with 0 on both sides)")
