# Q33: rolling 30-day active users per day with a recursive-CTE date spine and a range join
import sqlite3
import pandas as pd

# Conventions: timestamps are UTC text, the day is the UTC date, no test-user table exists here so none is filtered.
SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 4,'2024-01-31 10:00:00','open'),
 (2, 3,'2024-02-01 23:30:00','open'),
 (3, 1,'2024-02-05 09:00:00','open'),
 (4, 2,'2024-02-20 09:00:00','open'),
 (5, 1,'2024-03-01 08:00:00','open'),
 (6, 1,'2024-03-02 08:00:00','open'),
 (7, 1,'2024-03-02 21:00:00','click'),
 (8, 2,'2024-03-02 12:00:00','open'),
 (9, 1,'2024-03-03 08:00:00','open'),
 (10,5,'2024-03-05 08:00:00','open'),
 (11,3,'2024-03-15 08:00:00','open'),
 (12,4,'2024-03-20 08:00:00','open'),
 (13,1,'2024-03-31 08:00:00','open'),
 (14,2,'2024-03-31 09:00:00','open');
"""

SQL_MAIN = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01'
  UNION ALL
  SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), ud AS (
  SELECT DISTINCT user_id, date(event_ts) AS event_date FROM events
)
SELECT s.d AS day,
       COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) AS dau,
       COUNT(DISTINCT ud.user_id) AS rolling_mau,
       ROUND(COUNT(DISTINCT CASE WHEN ud.event_date = s.d THEN ud.user_id END) * 1.0 /
             NULLIF(COUNT(DISTINCT ud.user_id), 0), 4) AS stickiness
FROM spine s
LEFT JOIN ud ON ud.event_date BETWEEN date(s.d, '-29 days') AND s.d
GROUP BY s.d
ORDER BY s.d
"""
# wrong: sum the daily distinct counts over 30 rows
SQL_WRONG = """
WITH RECURSIVE spine(d) AS (
  SELECT '2024-03-01' UNION ALL SELECT date(d, '+1 day') FROM spine WHERE d < '2024-03-31'
), daily AS (
  SELECT date(event_ts) AS d, COUNT(DISTINCT user_id) AS dau FROM events GROUP BY date(event_ts)
)
SELECT s.d AS day, COALESCE(daily.dau, 0) AS dau,
       SUM(COALESCE(daily.dau, 0)) OVER (ORDER BY s.d ROWS BETWEEN 29 PRECEDING AND CURRENT ROW) AS wrong_sum_of_daus
FROM spine s LEFT JOIN daily ON daily.d = s.d
ORDER BY s.d
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL, 31 spine days (first 5 and every day with activity shown below):")
print(sql_main.head(5).to_string(index=False))
print(sql_main[sql_main["dau"] > 0].to_string(index=False))
print("rows returned:", len(sql_main), "; days with rolling_mau = 0:", int((sql_main["rolling_mau"] == 0).sum()))
wrong = pd.read_sql_query(SQL_WRONG, con)
cmp = wrong.merge(sql_main[["day", "rolling_mau"]], on="day")
print("wrong sum of DAUs versus distinct rolling MAU on selected days:")
print(cmp[cmp["day"].isin(["2024-03-02", "2024-03-03", "2024-03-31"])].to_string(index=False))

# date arithmetic: datetime/date modifiers versus unixepoch, across the leap day
chk = con.execute("SELECT date('2024-03-01','-29 days'), date(unixepoch('2024-03-01') - 29*86400,'unixepoch'), "
                  "datetime('2024-03-08 10:00:00','+7 days'), datetime(unixepoch('2024-03-08 10:00:00') + 7*86400,'unixepoch')").fetchone()
print("date arithmetic check:", chk)
assert chk[0] == chk[1] and chk[2] == chk[3]

events = pd.read_sql_query("SELECT * FROM events", con)

# pd:main
def rolling_active(events, start="2024-03-01", end="2024-03-31", window=30):
    ud = (events.assign(event_date=pd.to_datetime(events["event_ts"]).dt.normalize())
                [["user_id", "event_date"]].drop_duplicates())
    spine = pd.DataFrame({"day": pd.date_range(start, end)})
    m = spine.merge(ud, how="cross")
    lo = m["day"] - pd.Timedelta(days=window - 1)
    m = m[(m["event_date"] >= lo) & (m["event_date"] <= m["day"])]
    out = pd.DataFrame({
        "dau": m[m["event_date"] == m["day"]].groupby("day")["user_id"].nunique(),
        "rolling_mau": m.groupby("day")["user_id"].nunique()}).reindex(spine["day"]).fillna(0).astype(int)
    out["stickiness"] = (out["dau"] / out["rolling_mau"].where(out["rolling_mau"] != 0)).round(4)
    out = out.reset_index()
    out["day"] = out["day"].dt.strftime("%Y-%m-%d")
    return out
# pd:end

pd_res = rolling_active(events)
# compare in day order (SQL ORDER BY day); NaN stickiness equals NULL
pd.testing.assert_frame_equal(pd_res, sql_main, check_dtype=False)

# pandas 3.0 has Rolling.nunique: cross-check on days that have a row, using a time-based 30D window
ud = (events.assign(event_date=pd.to_datetime(events["event_ts"]).dt.normalize())
            [["user_id", "event_date"]].drop_duplicates().sort_values("event_date").set_index("event_date"))
rn = ud["user_id"].astype(float).rolling("30D").nunique()
last = rn.groupby(level=0).last()
chk_days = last.loc["2024-03-01":"2024-03-31"]
cmp2 = sql_main.set_index(pd.to_datetime(sql_main["day"])).loc[chk_days.index, "rolling_mau"]
assert (chk_days.astype(int).to_numpy() == cmp2.to_numpy()).all()
print("Rolling('30D').nunique matches rolling_mau on the", len(chk_days), "days that have event rows; spine days without events:",
      31 - len(chk_days))

# SQLite plan for the range join (no index): shows a scan, hedged for other engines
plan = con.execute("EXPLAIN QUERY PLAN " + SQL_MAIN).fetchall()
print("EXPLAIN QUERY PLAN rows:", [p[3] for p in plan])
print("asserts passed")
