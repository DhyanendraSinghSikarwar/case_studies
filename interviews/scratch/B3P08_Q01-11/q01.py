# Q1: DAU, WAU, MAU at a fixed as-of date with COUNT(DISTINCT user_id), SQL and pandas
import sqlite3
import pandas as pd

AS_OF = "2024-03-31"
SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-01-20','IN',0),(3,'2024-02-01','US',0),
 (4,'2024-02-10','IN',0),(5,'2024-02-15','IN',0),(6,'2024-02-20','IN',0),
 (7,'2024-03-01','US',0),(99,'2024-01-01','IN',1);
INSERT INTO events VALUES
 (1,'2024-03-31 00:05:00','open'),(1,'2024-03-31 09:00:00','click'),(1,'2024-03-31 23:59:59','click'),
 (2,'2024-03-31 10:00:00','open'),
 (3,'2024-03-25 08:00:00','open'),
 (4,'2024-03-24 23:59:59','open'),
 (5,'2024-03-02 00:00:00','open'),
 (6,'2024-03-01 23:59:59','open'),
 (7,'2024-04-01 00:00:00','open'),
 (99,'2024-03-31 12:00:00','open'),
 (NULL,'2024-03-31 12:30:00','open'),
 (1,'2024-03-29 10:00:00','open');
"""
# window = [start, as_of + 1 day), half-open on timestamps; start = as_of - (N-1) days
SQL_MAIN = """
SELECT
  COUNT(DISTINCT CASE WHEN e.event_ts >= :as_of
                       AND e.event_ts <  date(:as_of, '+1 day') THEN e.user_id END) AS dau,
  COUNT(DISTINCT CASE WHEN e.event_ts >= date(:as_of, '-6 days')
                       AND e.event_ts <  date(:as_of, '+1 day') THEN e.user_id END) AS wau,
  COUNT(DISTINCT CASE WHEN e.event_ts >= date(:as_of, '-29 days')
                       AND e.event_ts <  date(:as_of, '+1 day') THEN e.user_id END) AS mau
FROM events e
JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0
"""
SQL_COUNT_STAR = """
SELECT
  COUNT(CASE WHEN e.event_ts >= :as_of AND e.event_ts < date(:as_of, '+1 day') THEN 1 END) AS dau_rows,
  COUNT(CASE WHEN e.event_ts >= date(:as_of, '-6 days') AND e.event_ts < date(:as_of, '+1 day') THEN 1 END) AS wau_rows
FROM events e JOIN users u ON u.user_id = e.user_id WHERE u.is_test = 0
"""
# wrong boundary: BETWEEN on a date string against timestamp text drops the as-of day itself
SQL_BETWEEN = """
SELECT COUNT(DISTINCT e.user_id) AS dau_between
FROM events e JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0 AND e.event_ts BETWEEN :as_of AND :as_of
"""
SQL_WHO = """
SELECT e.user_id, MIN(e.event_ts) AS first_in_window, COUNT(*) AS rows_in_window
FROM events e JOIN users u ON u.user_id = e.user_id
WHERE u.is_test = 0 AND e.event_ts >= date(:as_of, '-29 days') AND e.event_ts < date(:as_of, '+1 day')
GROUP BY e.user_id ORDER BY e.user_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
p = {"as_of": AS_OF}
sql_df = pd.read_sql_query(SQL_MAIN, con, params=p)
print("SQL DAU/WAU/MAU as of", AS_OF)
print(sql_df.to_string(index=False))
print("COUNT(*) instead of DISTINCT:", con.execute(SQL_COUNT_STAR, p).fetchone())
print("BETWEEN as_of AND as_of (wrong, text timestamps):", con.execute(SQL_BETWEEN, p).fetchone())
print(pd.read_sql_query(SQL_WHO, con, params=p).to_string(index=False))
pa = {"a": AS_OF}
print("window starts: date() says", con.execute("SELECT date(:a,'-6 days'), date(:a,'-29 days')", pa).fetchone(),
      "| unixepoch says", con.execute(
          "SELECT date(unixepoch(:a) - 6*86400, 'unixepoch'), date(unixepoch(:a) - 29*86400, 'unixepoch')", pa).fetchone())

events = pd.read_sql_query("SELECT * FROM events", con)
users = pd.read_sql_query("SELECT * FROM users", con)
# pd:main
e = events.merge(users.loc[users["is_test"] == 0, ["user_id"]], on="user_id")
ts = pd.to_datetime(e["event_ts"])
end = pd.Timestamp(AS_OF) + pd.Timedelta(days=1)

def active(days):
    in_win = (ts >= end - pd.Timedelta(days=days)) & (ts < end)
    return e.loc[in_win, "user_id"].nunique()

pd_df = pd.DataFrame({"dau": [active(1)], "wau": [active(7)], "mau": [active(30)]})
# pd:end
print("pandas:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(pd_df, sql_df, check_dtype=False)  # one row, same columns
print("asserts passed")

# NULL user_id: SQL COUNT(DISTINCT) and pandas nunique both skip it; len(set()) does not
print("events with NULL user_id:", int(events["user_id"].isna().sum()),
      "| nunique:", events["user_id"].nunique(),
      "| len(set(...)):", len(set(events["user_id"])),
      "| SQL COUNT(DISTINCT):", con.execute("SELECT COUNT(DISTINCT user_id) FROM events").fetchone()[0])
# a window with nobody in it: counts are 0, not NULL
print("empty day:", con.execute(SQL_MAIN, {"as_of": "2023-01-01"}).fetchone())
