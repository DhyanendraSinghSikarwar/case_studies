# Q21: month-over-month revenue with a missing month (April), spine in SQL and reindex in pandas.
import sqlite3
import pandas as pd

DDL = """
CREATE TABLE orders(order_id INTEGER PRIMARY KEY, order_date TEXT, amount INTEGER);
INSERT INTO orders VALUES
 (1,'2025-01-10',100),(2,'2025-01-31',50),
 (3,'2025-02-14',200),
 (4,'2025-03-01',150),(5,'2025-03-20',50),
 (6,'2025-05-05',120);
"""
SQL = """
WITH RECURSIVE spine(m) AS (
  SELECT '2025-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM spine WHERE m < '2025-05-01'
),
monthly AS (
  SELECT substr(s.m, 1, 7) AS month, COALESCE(SUM(o.amount), 0) AS revenue
  FROM spine s
  LEFT JOIN orders o ON substr(o.order_date, 1, 7) = substr(s.m, 1, 7)
  GROUP BY s.m
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_revenue,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 1) AS growth_pct
FROM monthly
ORDER BY month
"""

con = sqlite3.connect(":memory:")
con.executescript(DDL)
s = pd.read_sql(SQL, con)
print(s.to_string(index=False))

orders = pd.read_sql("SELECT * FROM orders", con, parse_dates=["order_date"])
# PANDAS START
m = orders.set_index("order_date")["amount"].resample("MS").sum()
m = m.reindex(pd.date_range("2025-01-01", "2025-05-01", freq="MS"), fill_value=0)
p = m.rename("revenue").to_frame()
p["month"] = p.index.strftime("%Y-%m")
p["prev_revenue"] = p["revenue"].shift(1)
p["growth_pct"] = (100.0 * (p["revenue"] - p["prev_revenue"])
                   / p["prev_revenue"].where(p["prev_revenue"] != 0)).round(1)
p = p[["month", "revenue", "prev_revenue", "growth_pct"]].reset_index(drop=True)
# PANDAS END
print()
print(p.to_string(index=False))
pd.testing.assert_frame_equal(s, p, check_dtype=False)
print("\nasserts passed (same 5 rows, ordered by month; NULL in SQL equals NaN in pandas)")

# resample alone only spans the months that have orders: it stops at the last order
short = orders[orders["order_date"] < "2025-05-01"].set_index("order_date")["amount"].resample("MS").sum()
print("resample without reindex, orders before May only: rows", len(short), "ending at", short.index.max().strftime("%Y-%m"))
# naive growth without NULLIF would divide by zero
print("SQLite 100.0*(120-0)/0 gives (NULL, no error in SQLite):", con.execute("SELECT 100.0*(120-0)/0").fetchone()[0])
