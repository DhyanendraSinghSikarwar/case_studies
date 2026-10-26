# Q33: DAU excluding test accounts, zero-filled calendar, unknown user_id decision.
import sqlite3
import pandas as pd

con = sqlite3.connect(":memory:")
con.executescript("""
CREATE TABLE users(user_id INTEGER PRIMARY KEY, is_test INTEGER);
CREATE TABLE events(user_id INTEGER, event_ts TEXT);
INSERT INTO users VALUES (1,0),(2,0),(3,1),(4,0),(5,1),(6,0);
INSERT INTO events VALUES
 (1,'2025-06-01 09:00:00'),(1,'2025-06-01 15:00:00'),(1,'2025-06-01 18:00:00'),
 (2,'2025-06-01 10:00:00'),
 (3,'2025-06-02 11:00:00'),(3,'2025-06-03 12:00:00'),
 (4,'2025-06-02 08:00:00'),(4,'2025-06-04 09:00:00'),
 (1,'2025-06-04 10:00:00'),
 (5,'2025-06-03 13:00:00'),
 (99,'2025-06-05 10:00:00'),
 (6,'2025-06-05 12:00:00');
""")

sql_answer = """
WITH RECURSIVE days(d) AS (
  SELECT '2025-06-01' UNION ALL SELECT date(d, '+1 day') FROM days WHERE d < '2025-06-05'
), real_events AS (
  SELECT e.user_id, date(e.event_ts) AS d
  FROM events e JOIN users u ON u.user_id = e.user_id AND u.is_test = 0
)
SELECT days.d AS day, COUNT(DISTINCT r.user_id) AS dau
FROM days LEFT JOIN real_events r ON r.d = days.d
GROUP BY days.d
ORDER BY days.d
"""
got = pd.read_sql(sql_answer, con)
print(got.to_string(index=False))
print("\nwith unknown user 99 kept (LEFT JOIN users, is_test IS NOT 1):")
print(con.execute("""SELECT date(e.event_ts), COUNT(DISTINCT e.user_id) FROM events e
  LEFT JOIN users u ON u.user_id = e.user_id WHERE u.is_test IS NOT 1 GROUP BY 1 ORDER BY 1""").fetchall())

# --- pandas
users = pd.read_sql("SELECT * FROM users", con)
events = pd.read_sql("SELECT * FROM events", con)
real = events.merge(users[users.is_test == 0], on="user_id", how="inner")
real["day"] = real.event_ts.str[:10]
want = (real.groupby("day").user_id.nunique()
        .reindex(pd.date_range("2025-06-01", "2025-06-05").strftime("%Y-%m-%d"), fill_value=0)
        .rename_axis("day").rename("dau").reset_index())
# --- end pandas
print("\npandas"); print(want.to_string(index=False))
pd.testing.assert_frame_equal(got, want, check_dtype=False)
print("assert passed: 5 rows, ordered by day; day 2025-06-03 is 0 because only test user 3 and 5 were active")
