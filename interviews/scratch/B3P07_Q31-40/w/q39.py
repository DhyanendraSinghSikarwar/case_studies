# Q39: daily-login streaks by IST day versus UTC day, SQL + pandas (+ a pandas-only DST demo)
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE logins(user_id TEXT, login_ts_utc TEXT);
INSERT INTO logins VALUES
 ('U1','2024-03-07 10:00:00'),('U1','2024-03-03 10:00:00'),('U1','2024-03-05 20:00:00'),('U1','2024-03-04 10:00:00'),
 ('U2','2024-03-04 18:29:59'),('U2','2024-03-05 18:30:00'),
 ('U3','2024-03-04 10:00:00'),('U3','2024-03-04 19:00:00'),('U3','2024-03-06 10:00:00'),('U3','2024-03-06 10:00:00'),
 ('U4','2024-03-09 12:00:00'),
 ('U5','2024-03-04 10:00:00'),('U5',NULL),('U5','not a timestamp');
"""
SQL_MAIN = """
WITH d AS (
  SELECT DISTINCT user_id, date(login_ts_utc, :shift) AS day
  FROM logins
  WHERE date(login_ts_utc, :shift) IS NOT NULL
),
r AS (
  SELECT user_id, day,
         unixepoch(day) / 86400 - ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY day) AS k
  FROM d
)
SELECT user_id, MIN(day) AS streak_start, MAX(day) AS streak_end, COUNT(*) AS days
FROM r
GROUP BY user_id, k
ORDER BY user_id, streak_start
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
ist = pd.read_sql_query(SQL_MAIN, con, params={"shift": "+330 minutes"})
utc = pd.read_sql_query(SQL_MAIN, con, params={"shift": "+0 minutes"})
print("SQL, IST day:"); print(ist.to_string(index=False))
print("SQL, UTC day:"); print(utc.to_string(index=False))
print("check 20:00 UTC on 5 March:", con.execute("SELECT datetime('2024-03-05 20:00:00', '+330 minutes'), date('2024-03-05 20:00:00', '+330 minutes')").fetchone())
print("T and Z form accepted:", con.execute("SELECT datetime('2024-03-05T20:00:00Z', '+330 minutes')").fetchone())

logins = pd.read_sql_query("SELECT * FROM logins", con)
# pd:main
def streaks(df, shift_minutes):
    t = pd.to_datetime(df["login_ts_utc"], errors="coerce", format="%Y-%m-%d %H:%M:%S")
    x = pd.DataFrame({"user_id": df["user_id"], "day": (t + pd.Timedelta(minutes=shift_minutes)).dt.normalize()})
    x = x.dropna().drop_duplicates().sort_values(["user_id", "day"])
    x["k"] = (x["day"] - pd.Timestamp("1970-01-01")).dt.days - x.groupby("user_id").cumcount()
    out = (x.groupby(["user_id", "k"])
            .agg(streak_start=("day", "min"), streak_end=("day", "max"), days=("day", "size"))
            .reset_index().drop(columns="k").sort_values(["user_id", "streak_start"]).reset_index(drop=True))
    out["streak_start"] = out["streak_start"].dt.strftime("%Y-%m-%d")
    out["streak_end"] = out["streak_end"].dt.strftime("%Y-%m-%d")
    return out
# pd:end
p_ist, p_utc = streaks(logins, 330), streaks(logins, 0)
print("pandas IST:"); print(p_ist.to_string(index=False))
# compare after sorting by user_id, streak_start
assert p_ist.astype({"days": "int64"}).equals(ist.astype({"days": "int64"}))
assert p_utc.astype({"days": "int64"}).equals(utc.astype({"days": "int64"}))

# DST: pandas only (SQLite has no zones; not executed in SQLite). A fixed UTC-5 offset versus America/New_York.
try:
    t = pd.Timestamp("2024-03-11 04:30:00", tz="UTC")
    real = t.tz_convert("America/New_York")
    fixed = t - pd.Timedelta(hours=5)
    print("DST demo, real New York:", real.strftime("%Y-%m-%d %H:%M %Z"), "| fixed UTC-5:", fixed.strftime("%Y-%m-%d %H:%M"))
    day_start = pd.Timestamp("2024-03-10", tz="America/New_York")
    print("length of New York local day 2024-03-10:", (day_start + pd.offsets.Day(1) - day_start))
except Exception as e:
    print("DST demo skipped:", type(e).__name__, e)
print("asserts passed")
