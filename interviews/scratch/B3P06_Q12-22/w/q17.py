# Q17: YoY with missing months: LAG(12) is wrong, spine + self join is right; pandas pct_change(12) after reindex
import sqlite3
import numpy as np
import pandas as pd

SCHEMA = """
CREATE TABLE monthly_revenue(month TEXT PRIMARY KEY, revenue INTEGER);
INSERT INTO monthly_revenue VALUES
 ('2023-01-01',100),('2023-02-01',120),('2023-03-01',0),('2023-04-01',150),
 ('2023-06-01',130),('2023-07-01',140),('2023-08-01',160),('2023-09-01',170),
 ('2023-10-01',180),('2023-11-01',200),('2023-12-01',300),
 ('2024-01-01',150),('2024-03-01',90),('2024-04-01',30);
"""
AS_OF = "2024-04-15"
SQL_LAG12_FULL = """
WITH x AS (
  SELECT month, revenue,
         LAG(month, 12) OVER (ORDER BY month) AS lag12_month,
         LAG(revenue, 12) OVER (ORDER BY month) AS lag12_revenue
  FROM monthly_revenue
)
SELECT month, revenue, lag12_month, lag12_revenue FROM x WHERE month >= '2024-01-01' ORDER BY month
"""
SQL_MAIN = """
WITH RECURSIVE spine(m) AS (
  SELECT '2023-01-01'
  UNION ALL
  SELECT date(m, '+1 month') FROM spine WHERE m < date(:as_of, 'start of month')
),
cal AS (
  SELECT s.m AS month, COALESCE(r.revenue, 0) AS revenue
  FROM spine s LEFT JOIN monthly_revenue r ON r.month = s.m
)
SELECT c.month, c.revenue, p.revenue AS last_year,
       ROUND(100.0 * (c.revenue - p.revenue) / NULLIF(p.revenue, 0), 1) AS yoy_pct
FROM cal c
LEFT JOIN cal p ON p.month = date(c.month, '-1 year')
WHERE date(c.month, '+1 month') <= date(:as_of, '+1 day')
ORDER BY c.month
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("LAG(12) on the table with missing months (2023-05 and 2024-02 are missing):")
print(pd.read_sql_query(SQL_LAG12_FULL, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con, params={"as_of": AS_OF})
print("spine + self join (as of", AS_OF, "; 2024-04 is partial so it is excluded):")
print(sql_df.to_string(index=False))

mr = pd.read_sql_query("SELECT * FROM monthly_revenue", con)
# pd:main
s = mr.set_index(pd.to_datetime(mr["month"]))["revenue"].astype(float)
spine = pd.date_range("2023-01-01", "2024-03-01", freq="MS")   # completed months only (as of 2024-04-15)
s_full = s.reindex(spine, fill_value=0)
yoy = (s_full.pct_change(12, fill_method=None) * 100).replace([np.inf, -np.inf], np.nan).round(1)
yoy_shift = ((s_full / s_full.shift(12, freq="MS").reindex(s_full.index) - 1) * 100).replace([np.inf, -np.inf], np.nan).round(1)
pd_df = pd.DataFrame({"month": s_full.index.strftime("%Y-%m-%d"), "revenue": s_full.to_numpy(),
                      "last_year": s_full.shift(12).to_numpy(), "yoy_pct": yoy.to_numpy()})
# pd:end
# compared in ascending month order; SQL last_year is NULL for 2023 because the spine starts in 2023-01
cmp_sql = sql_df.assign(revenue=sql_df["revenue"].astype(float), last_year=sql_df["last_year"].astype(float))
pd.testing.assert_frame_equal(pd_df, cmp_sql, check_dtype=False)
assert yoy_shift.equals(yoy)
print("pandas pct_change(12) after reindex equals SQL; shift(12, freq='MS') gives the same YoY")
print("pandas without the reindex, pct_change(12) on the 14-row series:")
raw = s.pct_change(12, fill_method=None).mul(100).round(1)
print(pd.DataFrame({"month": raw.index.strftime("%Y-%m-%d"), "yoy_pct": raw.to_numpy()}).tail(4).to_string(index=False))
print("zero base in pandas before replace, 2024-03:", (s_full.pct_change(12, fill_method=None) * 100).loc["2024-03-01"])

# duplicate month rows (a late adjustment row for 2023-06): LAG(12) shifts by one the other way
con.executescript("""
CREATE TABLE mr_dup(month TEXT, revenue INTEGER);
INSERT INTO mr_dup SELECT * FROM monthly_revenue;
INSERT INTO mr_dup VALUES ('2023-06-01', 5);
""")
dup = pd.read_sql_query(SQL_LAG12_FULL.replace("monthly_revenue", "mr_dup"), con)
print("LAG(12) with a duplicate 2023-06 row and the missing 2023-05 row:")
print(dup.to_string(index=False))
print("asserts passed")
