# Q23: stock up-streaks with NULL closes, flat days, weekends; LAG flag + running count of non-up rows
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE prices(day TEXT, close REAL);
INSERT INTO prices VALUES
 ('2024-03-08',104),('2024-03-04',100),('2024-03-05',101),('2024-03-06',102),('2024-03-07',103),
 ('2024-03-11',104),('2024-03-12',105),('2024-03-13',NULL),('2024-03-14',105),('2024-03-15',106),
 ('2024-03-18',107),('2024-03-19',108),('2024-03-20',107),('2024-03-21',108),('2024-03-22',109);
"""
FLAGS = """
WITH f AS (
  SELECT day, close,
         LAG(close) OVER (ORDER BY day) AS prev_close,
         CASE WHEN close > LAG(close) OVER (ORDER BY day) THEN 1 ELSE 0 END AS up
  FROM prices
), g AS (
  SELECT *, SUM(1 - up) OVER (ORDER BY day ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS grp
  FROM f
)
"""
SQL_MAIN = FLAGS + """
SELECT MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS up_days
FROM g
WHERE up = 1
GROUP BY grp
HAVING COUNT(*) >= 3
ORDER BY start_day
"""
SQL_LONGEST = FLAGS + """
, s AS (SELECT grp, MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS up_days FROM g WHERE up = 1 GROUP BY grp)
SELECT start_day, end_day, up_days FROM s WHERE up_days = (SELECT MAX(up_days) FROM s) ORDER BY start_day
"""
SQL_ALL = FLAGS + """
SELECT MIN(day) AS start_day, MAX(day) AS end_day, COUNT(*) AS up_days
FROM g WHERE up = 1 GROUP BY grp ORDER BY start_day
"""
SQL_DETAIL = FLAGS + "SELECT day, close, prev_close, up, grp FROM g ORDER BY day"
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
print("flags per row:")
print(pd.read_sql_query(SQL_DETAIL, con).to_string(index=False))
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL, streaks of at least 3 up days:")
print(sql_df.to_string(index=False))
print("SQL, every up-streak:")
print(pd.read_sql_query(SQL_ALL, con).to_string(index=False))
print("SQL, longest (ties all returned):")
print(pd.read_sql_query(SQL_LONGEST, con).to_string(index=False))

prices = pd.read_sql_query("SELECT * FROM prices", con)
# pd:main
p = prices.assign(day=pd.to_datetime(prices["day"])).sort_values("day").reset_index(drop=True)
p["up"] = p["close"].gt(p["close"].shift())
p["grp"] = (~p["up"]).cumsum()
pd_all = (p[p["up"]].groupby("grp")
            .agg(start_day=("day", "min"), end_day=("day", "max"), up_days=("day", "size"))
            .reset_index(drop=True))
pd_df = pd_all[pd_all["up_days"] >= 3].reset_index(drop=True)
# pd:end
out = pd_df.assign(start_day=pd_df["start_day"].dt.strftime("%Y-%m-%d"), end_day=pd_df["end_day"].dt.strftime("%Y-%m-%d"))
print("pandas, at least 3:")
print(out.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.sort_values("start_day").reset_index(drop=True),
                              out.sort_values("start_day").reset_index(drop=True), check_dtype=False)  # sorted by start_day
# the longest in pandas, ties kept
longest = pd_all[pd_all["up_days"] == pd_all["up_days"].max()]
print("pandas longest rows:", len(longest), "up_days", int(longest["up_days"].iloc[0]))

# edge: an exact duplicate row for the same day looks like a flat day and breaks a streak
con.execute("INSERT INTO prices VALUES ('2024-03-06',102)")
print("after inserting a duplicate 2024-03-06 row:")
print(pd.read_sql_query(SQL_MAIN, con).to_string(index=False))
con.execute("DELETE FROM prices WHERE rowid IN (SELECT MAX(rowid) FROM prices)")
# edge: shift on an integer column upcasts to float64
s = pd.Series([1, 2, 3])
print("int shift dtype:", s.dtype, "->", s.shift().dtype, "; with fill_value=0:", s.shift(fill_value=0).dtype)
print("NaN > anything is False:", float("nan") > 1, pd.Series([1.0, float("nan")]).gt(0.5).tolist())
# edge: empty and single row
con.execute("DELETE FROM prices WHERE day <> '2024-03-04'")
print("single row, SQL rows:", len(pd.read_sql_query(SQL_ALL, con)))
print("asserts passed")
