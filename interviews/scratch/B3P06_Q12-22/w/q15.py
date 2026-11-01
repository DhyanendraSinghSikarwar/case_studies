# Q15: distinct active users per month and per Monday-start week; Grouper defaults; ISO-year emulation
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO events VALUES
 (1,'2024-01-02 09:00:00'),(1,'2024-01-09 18:30:00'),
 (2,'2024-01-03 10:00:00'),(2,'2024-01-04 11:00:00'),
 (3,'2024-01-10 08:00:00'),(3,'2024-01-31 23:59:59'),
 (4,'2024-01-29 07:00:00'),(4,'2024-02-01 12:00:00'),
 (5,'2024-02-06 13:00:00');
"""
SQL_MONTH = """
SELECT strftime('%Y-%m', event_ts) AS month, COUNT(DISTINCT user_id) AS active_users
FROM events GROUP BY month ORDER BY month
"""
SQL_WEEK = """
SELECT date(event_ts, 'weekday 0', '-6 days') AS week_start, COUNT(DISTINCT user_id) AS active_users
FROM events GROUP BY week_start ORDER BY week_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
m_sql = pd.read_sql_query(SQL_MONTH, con)
w_sql = pd.read_sql_query(SQL_WEEK, con)
print("SQL monthly:"); print(m_sql.to_string(index=False))
print("SQL weekly (Monday start):"); print(w_sql.to_string(index=False))
print("sum of January-week rows (weeks starting 01-01..01-29):", int(w_sql[w_sql.week_start < "2024-02-01"].active_users.sum()),
      "vs January MAU:", int(m_sql.loc[m_sql.month == "2024-01", "active_users"].iloc[0]))

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
e = events.assign(event_ts=pd.to_datetime(events["event_ts"]))
m_pd = (e.groupby(pd.Grouper(key="event_ts", freq="MS"))["user_id"].nunique()
          .rename("active_users").reset_index())
m_pd["month"] = m_pd["event_ts"].dt.strftime("%Y-%m")
m_pd = m_pd[["month", "active_users"]]
w_pd = (e.groupby(pd.Grouper(key="event_ts", freq="W-MON", closed="left", label="left"))["user_id"].nunique()
          .rename("active_users").reset_index())
w_pd["week_start"] = w_pd["event_ts"].dt.strftime("%Y-%m-%d")
w_pd = w_pd.loc[w_pd["active_users"] > 0, ["week_start", "active_users"]].reset_index(drop=True)
# pd:end
# compared in ascending month / week_start order; Grouper also emits empty weeks, filtered out above
pd.testing.assert_frame_equal(m_pd, m_sql, check_dtype=False)
pd.testing.assert_frame_equal(w_pd, w_sql, check_dtype=False)
print("pandas equals SQL (monthly and weekly)")

raw = e.groupby(pd.Grouper(key="event_ts", freq="W-MON"))["user_id"].nunique()
print("W-MON with default closed/label (right/right), labels are the Monday that ENDS each bin:")
print(raw.to_string())
all_weeks = e.groupby(pd.Grouper(key="event_ts", freq="W-MON", closed="left", label="left"))["user_id"].nunique()
print("empty weeks pandas keeps (SQL omits):", [d.strftime("%Y-%m-%d") for d in all_weeks[all_weeks == 0].index])

# ISO-year emulation for the week label's year (date(d,'-3 days','weekday 4') = Thursday of the ISO week)
dates = ["2023-01-01", "2024-12-30", "2021-01-01", "2024-01-01", "2026-12-31", "2020-12-31"]
for d in dates:
    iso_sql = con.execute("SELECT strftime('%Y', date(?, '-3 days', 'weekday 4'))", (d,)).fetchone()[0]
    iso_pd = pd.Timestamp(d).isocalendar().year
    assert int(iso_sql) == int(iso_pd), (d, iso_sql, iso_pd)
print("ISO-year emulation matches isocalendar().year for", dates)
print("strftime('%V') on 3.45.1:", con.execute("SELECT strftime('%V','2024-12-30')").fetchone()[0])
print("asserts passed")
