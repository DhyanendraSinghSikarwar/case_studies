# Q16: longest daily streak per user with start and end, tie -> earlier run
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE searches(user_id INTEGER, search_ts TEXT);
INSERT INTO searches VALUES
 (1,'2025-03-01 09:00:00'),(1,'2025-03-02 09:00:00'),(1,'2025-03-02 12:30:00'),(1,'2025-03-02 23:59:59'),(1,'2025-03-03 08:00:00'),(1,'2025-03-05 10:00:00'),(1,'2025-03-06 10:00:00'),
 (2,'2025-03-01 09:00:00'),(2,'2025-03-02 09:00:00'),(2,'2025-03-04 09:00:00'),(2,'2025-03-05 09:00:00'),(2,'2025-03-06 09:00:00'),
 (3,'2025-03-07 10:00:00'),
 (4,'2025-03-01 09:00:00'),(4,'2025-03-02 09:00:00'),(4,'2025-03-10 09:00:00'),(4,'2025-03-11 09:00:00'),
 (5,'2025-01-30 20:00:00'),(5,'2025-01-31 20:00:00'),(5,'2025-02-01 20:00:00');
""")
sql = """
WITH days AS (SELECT DISTINCT user_id, date(search_ts) AS d FROM searches),
g AS (SELECT user_id, d, date(d, '-' || (ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY d) - 1) || ' days') AS grp FROM days),
runs AS (SELECT user_id, MIN(d) AS run_start, MAX(d) AS run_end, COUNT(*) AS days FROM g GROUP BY user_id, grp),
best AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY days DESC, run_start ASC) AS rn FROM runs)
SELECT user_id, run_start, run_end, days FROM best WHERE rn = 1 ORDER BY user_id
"""
a = pd.read_sql(sql, con)
print("SQL"); print(a.to_string(index=False))
raw = """
WITH g AS (SELECT date(search_ts) AS d,
  date(date(search_ts), '-' || (ROW_NUMBER() OVER (ORDER BY search_ts) - 1) || ' days') AS grp
  FROM searches WHERE user_id = 1)
SELECT MIN(d) AS run_start, MAX(d) AS run_end, COUNT(*) AS n FROM g GROUP BY grp ORDER BY run_start
"""
print("\nuser 1 without the DISTINCT-days step (row numbers over raw rows): the 3 searches on 03-02 split the run")
print(pd.read_sql(raw, con).to_string(index=False))

s = pd.read_sql("SELECT * FROM searches", con)
s["d"] = pd.to_datetime(s.search_ts.str[:10])
dd = s[["user_id", "d"]].drop_duplicates().sort_values(["user_id", "d"])
dd["new_run"] = dd.groupby("user_id")["d"].diff().ne(pd.Timedelta(days=1))
dd["grp"] = dd.groupby("user_id")["new_run"].cumsum()
runs = dd.groupby(["user_id", "grp"]).agg(run_start=("d", "min"), run_end=("d", "max"), days=("d", "size")).reset_index()
best = runs.sort_values(["user_id", "days", "run_start"], ascending=[True, False, True]).drop_duplicates("user_id")
p = best[["user_id", "run_start", "run_end", "days"]].sort_values("user_id").reset_index(drop=True)
p["run_start"] = p.run_start.dt.strftime("%Y-%m-%d"); p["run_end"] = p.run_end.dt.strftime("%Y-%m-%d")
print("\npandas"); print(p.to_string(index=False))
pd.testing.assert_frame_equal(a, p, check_dtype=False)
print("\nassert passed: equal, rows ordered by user_id")
