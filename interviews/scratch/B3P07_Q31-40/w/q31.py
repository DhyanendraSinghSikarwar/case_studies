# Q31: attendance streaks over working days (weekend and holiday skipping), SQL + pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE attendance(emp_id TEXT, work_date TEXT);
CREATE TABLE holidays(holiday_date TEXT);
INSERT INTO holidays VALUES ('2024-03-14');
INSERT INTO attendance VALUES
 ('E1','2024-03-11'),('E1','2024-03-08'),('E1','2024-03-07'),('E1','2024-03-08'),
 ('E1','2024-03-12'),('E1','2024-03-13'),('E1','2024-03-15'),
 ('E2','2024-03-04'),('E2','2024-03-05'),('E2','2024-03-07'),('E2','2024-03-08'),
 ('E3','2024-03-18'),
 ('E4','2024-03-08'),('E4','2024-03-12'),
 ('E5','2024-03-13'),('E5','2024-03-14'),('E5','2024-03-15'),('E5','2024-03-16'),
 ('E6','2024-03-19'),(NULL,'2024-03-19'),('E6',NULL);
"""
CAL_CTE = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
),
cal AS (
  SELECT d AS cal_date, ROW_NUMBER() OVER (ORDER BY d) AS wd_no
  FROM spine s
  WHERE strftime('%w', d) NOT IN ('0', '6')
    AND NOT EXISTS (SELECT 1 FROM holidays h WHERE h.holiday_date = s.d)
),
a AS (
  SELECT DISTINCT emp_id, work_date FROM attendance
  WHERE emp_id IS NOT NULL AND work_date IS NOT NULL
),
j AS (
  SELECT a.emp_id, c.cal_date, c.wd_no,
         ROW_NUMBER() OVER (PARTITION BY a.emp_id ORDER BY c.cal_date) AS rn
  FROM a JOIN cal c ON c.cal_date = a.work_date
)
"""
SQL_MAIN = CAL_CTE + """
SELECT emp_id, MIN(cal_date) AS streak_start, MAX(cal_date) AS streak_end, COUNT(*) AS days
FROM j
GROUP BY emp_id, wd_no - rn
ORDER BY emp_id, streak_start
"""
SQL_CALDAY = """
WITH a AS (
  SELECT DISTINCT emp_id, work_date FROM attendance
  WHERE emp_id IS NOT NULL AND work_date IS NOT NULL
),
r AS (
  SELECT emp_id, work_date,
         ROW_NUMBER() OVER (PARTITION BY emp_id ORDER BY work_date) AS rn
  FROM a
)
SELECT emp_id, MIN(work_date) AS streak_start, MAX(work_date) AS streak_end, COUNT(*) AS days
FROM r
GROUP BY emp_id, julianday(work_date) - rn
ORDER BY emp_id, streak_start
"""
SQL_CAL = CAL_CTE + "SELECT cal_date, wd_no, strftime('%w', cal_date) AS dow FROM cal WHERE cal_date BETWEEN '2024-03-06' AND '2024-03-18'"

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL, working-day streaks:")
print(sql_df.to_string(index=False))
print("SQL, calendar-day streaks (splits at weekends):")
print(pd.read_sql_query(SQL_CALDAY, con).to_string(index=False))
print("working-day calendar, 6 to 18 March:")
print(pd.read_sql_query(SQL_CAL, con).to_string(index=False))

attendance = pd.read_sql_query("SELECT * FROM attendance", con)
holidays = pd.read_sql_query("SELECT * FROM holidays", con)
# pd:main
days = pd.date_range("2024-03-01", "2024-03-31")
cal = pd.DataFrame({"cal_date": days})
cal = cal[(cal["cal_date"].dt.dayofweek < 5)
          & ~cal["cal_date"].isin(pd.to_datetime(holidays["holiday_date"]))].copy()
cal["wd_no"] = range(1, len(cal) + 1)
a = attendance.dropna().drop_duplicates()
a = a.assign(cal_date=pd.to_datetime(a["work_date"])).merge(cal, on="cal_date")
a = a.sort_values(["emp_id", "cal_date"])
a["key"] = a["wd_no"] - (a.groupby("emp_id").cumcount() + 1)
pd_df = (a.groupby(["emp_id", "key"])
          .agg(streak_start=("cal_date", "min"), streak_end=("cal_date", "max"), days=("cal_date", "size"))
          .reset_index().drop(columns="key")
          .sort_values(["emp_id", "streak_start"]).reset_index(drop=True))
pd_df["streak_start"] = pd_df["streak_start"].dt.strftime("%Y-%m-%d")
pd_df["streak_end"] = pd_df["streak_end"].dt.strftime("%Y-%m-%d")
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
# compare after sorting both by emp_id, streak_start
assert pd_df.astype({"days": "int64"}).equals(sql_df.astype({"days": "int64"}))

# edge: E5 attended on the holiday and on a Saturday; both rows are dropped by the inner join
print("E5 rows kept:", int((a["emp_id"] == "E5").sum()), "of", int((attendance["emp_id"] == "E5").sum()))
# edge: a NULL holiday_date would break NOT IN but not NOT EXISTS
con.execute("INSERT INTO holidays VALUES (NULL)")
print("rows with NULL holiday present:", len(pd.read_sql_query(SQL_MAIN, con)))
print("asserts passed")
