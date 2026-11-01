# Q26: remove consecutive repeats per user (keep first of each run), NULL-safe with IS NOT
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (6,1,'2024-03-01 10:05:00','A'),
 (1,1,'2024-03-01 10:00:00','A'),
 (2,1,'2024-03-01 10:01:00','A'),
 (3,1,'2024-03-01 10:02:00','B'),
 (4,1,'2024-03-01 10:03:00','A'),
 (5,1,'2024-03-01 10:04:00','A'),
 (7,2,'2024-03-01 11:00:00','A'),
 (8,3,'2024-03-01 12:00:00','B'),
 (9,3,'2024-03-01 12:00:00','B'),
 (10,3,'2024-03-01 12:00:00','C'),
 (11,4,'2024-03-01 13:00:00',NULL),
 (12,4,'2024-03-01 13:01:00',NULL),
 (13,4,'2024-03-01 13:02:00','A'),
 (14,4,'2024-03-01 13:03:00',NULL);
"""
SQL_MAIN = """
WITH x AS (
  SELECT event_id, user_id, event_ts, event_name,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS rn,
         LAG(event_name) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_name
  FROM events
)
SELECT event_id, user_id, event_ts, event_name
FROM x
WHERE rn = 1 OR event_name IS NOT prev_name
ORDER BY user_id, event_ts, event_id
"""
SQL_DISTINCT = """
SELECT DISTINCT user_id, event_name FROM events WHERE user_id = 1 ORDER BY event_name
"""
SQL_NEQ = """
WITH x AS (
  SELECT event_id, user_id, event_name,
         LAG(event_name) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_name
  FROM events
)
SELECT event_id, user_id, event_name FROM x WHERE event_name != prev_name ORDER BY user_id, event_id
"""
SQL_NOGUARD = """
WITH x AS (
  SELECT event_id, user_id, event_name,
         LAG(event_name) OVER (PARTITION BY user_id ORDER BY event_ts, event_id) AS prev_name
  FROM events
)
SELECT event_id, user_id, event_name FROM x WHERE event_name IS NOT prev_name AND user_id = 4 ORDER BY event_id
"""
con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_df = pd.read_sql_query(SQL_MAIN, con)
print("SQL answer (kept rows):")
print(sql_df.to_string(index=False))
print("wrong: SELECT DISTINCT user_id, event_name for user 1 (the second A is lost):")
print(pd.read_sql_query(SQL_DISTINCT, con).to_string(index=False))
print("wrong: != instead of IS NOT (first rows and NULL names vanish):")
print(pd.read_sql_query(SQL_NEQ, con).to_string(index=False))
print("IS NOT without the rn = 1 guard, user 4 (leading NULL name is dropped):")
print(pd.read_sql_query(SQL_NOGUARD, con).to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)
# pd:main
e = events.sort_values(["user_id", "event_ts", "event_id"]).reset_index(drop=True)
prev = e.groupby("user_id")["event_name"].shift()
first_of_user = e.groupby("user_id").cumcount().eq(0)
same_as_prev = e["event_name"].eq(prev) | (e["event_name"].isna() & prev.isna())
pd_df = e[first_of_user | ~same_as_prev].reset_index(drop=True)
# pd:end
print("pandas answer:")
print(pd_df.to_string(index=False))
pd.testing.assert_frame_equal(sql_df.reset_index(drop=True), pd_df, check_dtype=False)  # both ordered by user_id, event_ts, event_id

# the naive pandas comparison: NaN != NaN is True, so a run of NULL names is NOT collapsed
naive = e[first_of_user | e["event_name"].ne(prev)]
print("naive pandas ne(shift) keeps rows of user 4:", naive[naive["user_id"] == 4]["event_id"].tolist(), "vs SQL", sql_df[sql_df["user_id"] == 4]["event_id"].tolist())
# single row group and tie on timestamp are covered by users 2 and 3
print("asserts passed")
