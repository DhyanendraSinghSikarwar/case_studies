# Q12: Day-1 retention (LeetCode 550 pattern): SQL first-login CTE + join, wrong answers, pandas
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE activity(player_id INTEGER, device_id INTEGER, event_date TEXT, games_played INTEGER);
INSERT INTO activity VALUES
 (1,2,'2024-03-01',5),(1,2,'2024-03-02',6),(1,3,'2024-03-02',1),(1,2,'2024-05-02',4),
 (2,3,'2024-03-05',1),(2,3,'2024-03-09',2),
 (3,1,'2024-03-02',0),(3,1,'2024-03-03',4),(3,4,'2024-03-03',2),
 (4,4,'2024-03-10',3),
 (5,1,'2024-02-29',2),(5,1,'2024-03-01',7);
"""
SQL_MAIN = """
WITH fl AS (
  SELECT player_id, MIN(event_date) AS first_login
  FROM activity
  GROUP BY player_id
)
SELECT ROUND(1.0 * COUNT(DISTINCT a.player_id) / (SELECT COUNT(*) FROM fl), 2) AS fraction
FROM fl
LEFT JOIN activity a
  ON a.player_id = fl.player_id
 AND a.event_date = date(fl.first_login, '+1 day')
"""
SQL_ROWS = """
WITH fl AS (SELECT player_id, MIN(event_date) AS first_login FROM activity GROUP BY player_id)
SELECT ROUND(1.0 * COUNT(a.player_id) / (SELECT COUNT(*) FROM fl), 2)
FROM fl LEFT JOIN activity a
  ON a.player_id = fl.player_id AND a.event_date = date(fl.first_login, '+1 day')
"""
SQL_ANY_LATER = """
WITH fl AS (SELECT player_id, MIN(event_date) AS first_login FROM activity GROUP BY player_id)
SELECT ROUND(1.0 * COUNT(DISTINCT a.player_id) / (SELECT COUNT(*) FROM fl), 2)
FROM fl LEFT JOIN activity a
  ON a.player_id = fl.player_id AND a.event_date > fl.first_login
"""
SQL_PER_LOGIN = """
WITH fl AS (SELECT player_id, MIN(event_date) AS first_login FROM activity GROUP BY player_id)
SELECT ROUND(1.0 * COUNT(DISTINCT a.player_id) / (SELECT COUNT(*) FROM activity), 2)
FROM fl LEFT JOIN activity a
  ON a.player_id = fl.player_id AND a.event_date = date(fl.first_login, '+1 day')
"""
SQL_WHO = """
WITH fl AS (SELECT player_id, MIN(event_date) AS first_login FROM activity GROUP BY player_id)
SELECT fl.player_id, fl.first_login, date(fl.first_login, '+1 day') AS next_day,
       COUNT(a.player_id) AS rows_on_next_day
FROM fl LEFT JOIN activity a
  ON a.player_id = fl.player_id AND a.event_date = date(fl.first_login, '+1 day')
GROUP BY fl.player_id ORDER BY fl.player_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_val = con.execute(SQL_MAIN).fetchone()[0]
print("SQL day-1 retention:", sql_val)
print("wrong 1, count rows not players:", con.execute(SQL_ROWS).fetchone()[0])
print("wrong 2, any later login:", con.execute(SQL_ANY_LATER).fetchone()[0])
print("wrong 3, divide by login rows:", con.execute(SQL_PER_LOGIN).fetchone()[0])
print(pd.read_sql_query(SQL_WHO, con).to_string(index=False))

activity = pd.read_sql_query("SELECT * FROM activity", con)
# pd:main
a = activity.assign(event_date=pd.to_datetime(activity["event_date"]))
a["first_login"] = a.groupby("player_id")["event_date"].transform("min")
day1 = a[a["event_date"] == a["first_login"] + pd.Timedelta(days=1)]
pd_val = round(day1["player_id"].nunique() / a["player_id"].nunique(), 2)
# pd:end
print("pandas day-1 retention:", pd_val)
assert pd_val == sql_val  # scalar, no row order involved
# the same pandas result through an explicit merge of first logins back to activity
fl = a.groupby("player_id", as_index=False)["event_date"].min().rename(columns={"event_date": "first_login"})
m = fl.merge(a[["player_id", "event_date"]], on="player_id", how="left")
m_hit = m[m["event_date"] == m["first_login"] + pd.Timedelta(days=1)]
assert round(m_hit["player_id"].nunique() / len(fl), 2) == sql_val

# edge: empty table
con.execute("DELETE FROM activity")
print("empty table, SQL:", con.execute(SQL_MAIN).fetchone()[0])
try:
    print(round(a.iloc[0:0]["player_id"].nunique() / a.iloc[0:0]["player_id"].nunique(), 2))
except ZeroDivisionError as e:
    print("empty table, pandas: ZeroDivisionError:", e)
print("asserts passed")
