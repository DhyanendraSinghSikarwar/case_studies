# Q2: number series and calendar spine with a recursive CTE, LEFT JOIN, 7-day moving total; pandas date_range + reindex
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sales(sale_date TEXT, amount INTEGER);
INSERT INTO sales VALUES
 ('2024-02-28', 999),                       -- outside the range
 ('2024-03-01', 100),
 ('2024-03-02', 50), ('2024-03-02', 25),    -- two rows on one day
 ('2024-03-04', 200),
 ('2024-03-07', NULL),                      -- a day whose only amount is NULL
 ('2024-03-08', 70),
 ('2024-03-10', 30),
 ('2024-03-12', 500);                       -- outside the range
"""
SQL_NUMS = """
WITH RECURSIVE nums(n) AS (
  SELECT 1 UNION ALL SELECT n + 1 FROM nums WHERE n < 10
)
SELECT n FROM nums
"""
SQL_MAIN = """
WITH RECURSIVE spine(d) AS (
  SELECT :start WHERE :start <= :stop
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < :stop
), daily AS (
  SELECT sale_date AS d, SUM(amount) AS amt FROM sales GROUP BY sale_date
)
SELECT spine.d AS day,
       COALESCE(daily.amt, 0) AS amount,
       SUM(COALESCE(daily.amt, 0)) OVER (ORDER BY spine.d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS total_7d
FROM spine LEFT JOIN daily ON daily.d = spine.d
ORDER BY spine.d
"""
P = {"start": "2024-03-01", "stop": "2024-03-10"}
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("integers:", [r[0] for r in con.execute(SQL_NUMS)])
sql_df = pd.read_sql_query(SQL_MAIN, con, params=P)
print(sql_df.to_string(index=False))

sales = pd.read_sql_query("SELECT * FROM sales", con)
# pd:main
days = pd.date_range("2024-03-01", "2024-03-10")
daily = (sales.assign(sale_date=pd.to_datetime(sales["sale_date"]))
              .groupby("sale_date")["amount"].sum())
filled = daily.reindex(days, fill_value=0).fillna(0)
pd_df = pd.DataFrame({"day": days.strftime("%Y-%m-%d"), "amount": filled.to_numpy(),
                      "total_7d": filled.rolling(7, min_periods=1).sum().to_numpy()})
# pd:end
pd.testing.assert_frame_equal(pd_df.reset_index(drop=True), sql_df, check_dtype=False)   # both ordered by day
print("pandas equals SQL (ordered by day)")

# Edge cases
r = con.execute(SQL_MAIN, {"start": "2024-03-10", "stop": "2024-03-01"}).fetchall()
print("start after stop with the anchor guard:", r)
r = con.execute(SQL_MAIN.replace("SELECT :start WHERE :start <= :stop", "SELECT :start"), {"start": "2024-03-10", "stop": "2024-03-01"}).fetchall()
print("start after stop WITHOUT the guard: rows =", len(r), "first =", r[0])
print("single day range:", con.execute(SQL_MAIN, {"start": "2024-03-04", "stop": "2024-03-04"}).fetchall())
print("bad date text '2024-3-1' through date():", con.execute("SELECT date('2024-3-1')").fetchone())
con.execute("DELETE FROM sales")
empty = con.execute(SQL_MAIN, P).fetchall()
print("empty sales: rows =", len(empty), "all zero =", all(a == 0 and t == 0 for _, a, t in empty))
print("asserts passed")
