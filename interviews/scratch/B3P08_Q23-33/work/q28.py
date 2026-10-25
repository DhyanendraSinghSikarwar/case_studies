# Q28: engagement distribution: mean and median events per user, NTILE(10) power users, top decile share
import sqlite3
import pandas as pd

def build_events():
    # events per March user: u1 1, u2 1, u3 2, u4 2, u5 3, u6 4, u7 5, u8 8, u9 20, u10 60
    counts = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 4, 7: 5, 8: 8, 9: 20, 10: 60}
    rows, i = [], 0
    for u, n in counts.items():
        for k in range(n):
            i += 1
            rows.append((i, u, "2024-03-%02d 10:%02d:00" % (1 + (k % 28), k % 60), "click"))
    rows += [(1001, 1, "2024-02-28 10:00:00", "click"), (1002, 11, "2024-02-29 10:00:00", "click"),
             (1003, 2, "2024-04-01 10:00:00", "click"), (1004, 13, "2024-03-05 10:00:00", "click")]
    return rows

SCHEMA = """
CREATE TABLE users(user_id INTEGER PRIMARY KEY, signup_date TEXT, country TEXT, is_test INTEGER);
CREATE TABLE events(event_id INTEGER PRIMARY KEY, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO users VALUES
 (1,'2024-01-05','IN',0),(2,'2024-01-06','IN',0),(3,'2024-01-07','IN',0),(4,'2024-01-08','IN',0),
 (5,'2024-01-09','IN',0),(6,'2024-01-10','IN',0),(7,'2024-01-11','IN',0),(8,'2024-01-12','IN',0),
 (9,'2024-01-13','IN',0),(10,'2024-01-14','IN',0),(11,'2024-01-15','IN',0),(12,'2024-01-16','IN',0),
 (13,'2024-01-17','IN',1);
"""

# {BASE} is replaced: active users only (INNER JOIN) or all non-test registered users (LEFT JOIN, zeros kept)
SQL_TEMPLATE = """
WITH u AS (
  SELECT us.user_id, COUNT(e.event_id) AS n
  FROM users us
  {JOIN} events e ON e.user_id = us.user_id
       AND e.event_ts >= '2024-03-01' AND e.event_ts < '2024-04-01'
  WHERE us.is_test = 0
  GROUP BY us.user_id
), r AS (
  SELECT user_id, n,
         NTILE(10) OVER (ORDER BY n DESC, user_id) AS decile,
         ROW_NUMBER() OVER (ORDER BY n, user_id) AS rn,
         COUNT(*) OVER () AS cnt
  FROM u
), med AS (
  SELECT AVG(n) AS median FROM r WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
)
SELECT COUNT(*) AS users,
       SUM(n) AS events,
       ROUND(AVG(n), 2) AS mean_events,
       (SELECT median FROM med) AS median_events,
       SUM(decile = 1) AS top_decile_users,
       SUM(CASE WHEN decile = 1 THEN n END) AS top_decile_events,
       ROUND(SUM(CASE WHEN decile = 1 THEN n END) * 100.0 / SUM(n), 2) AS top_decile_share_pct
FROM r
"""
SQL_ACTIVE = SQL_TEMPLATE.replace("{JOIN}", "JOIN")
SQL_ALL = SQL_TEMPLATE.replace("{JOIN}", "LEFT JOIN")
SQL_DECILES = """
SELECT user_id, COUNT(e.event_id) AS n,
       NTILE(10) OVER (ORDER BY COUNT(e.event_id) DESC, us.user_id) AS decile
FROM users us LEFT JOIN events e ON e.user_id = us.user_id
     AND e.event_ts >= '2024-03-01' AND e.event_ts < '2024-04-01'
WHERE us.is_test = 0
GROUP BY us.user_id
ORDER BY decile, us.user_id
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
con.executemany("INSERT INTO events VALUES (?,?,?,?)", build_events())
print("integer division check, (12 + 1) / 2 and (12 + 2) / 2:", con.execute("SELECT (12+1)/2, (12+2)/2").fetchone())
a = pd.read_sql_query(SQL_ACTIVE, con)
b = pd.read_sql_query(SQL_ALL, con)
print("SQL, active users only (zero-event users excluded):")
print(a.to_string(index=False))
print("SQL, all non-test registered users (zero-event users kept):")
print(b.to_string(index=False))
dec = pd.read_sql_query(SQL_DECILES, con)
print("SQL, deciles over all non-test users (NTILE(10) over 12 rows):")
print(dec.to_string(index=False))

users = pd.read_sql_query("SELECT * FROM users", con)
events = pd.read_sql_query("SELECT * FROM events", con)

# pd:main
def ntile(n_rows, k):
    # NTILE: the first (n_rows % k) buckets get one extra row; assigned by position
    base, extra = divmod(n_rows, k)
    out = []
    for i in range(n_rows):
        if i < extra * (base + 1):
            out.append(i // (base + 1) + 1)
        else:
            out.append(extra + (i - extra * (base + 1)) // base + 1)
    return out

def engagement(users, events, keep_zero):
    m = events[(events["event_ts"] >= "2024-03-01") & (events["event_ts"] < "2024-04-01")]
    cnt = m.groupby("user_id").size().rename("n")
    u = users.loc[users["is_test"] == 0, ["user_id"]].merge(cnt, on="user_id", how="left")
    u["n"] = u["n"].fillna(0).astype(int)
    if not keep_zero:
        u = u[u["n"] > 0]
    u = u.sort_values(["n", "user_id"], ascending=[False, True]).reset_index(drop=True)
    u["decile"] = ntile(len(u), 10) if len(u) >= 10 else range(1, len(u) + 1)
    top = u[u["decile"] == 1]
    return pd.DataFrame({"users": [len(u)], "events": [u["n"].sum()], "mean_events": [round(u["n"].mean(), 2)],
                         "median_events": [float(u["n"].median())], "top_decile_users": [len(top)],
                         "top_decile_events": [top["n"].sum()],
                         "top_decile_share_pct": [round(top["n"].sum() * 100.0 / u["n"].sum(), 2)]}), u
# pd:end

pd_a, _ = engagement(users, events, keep_zero=False)
pd_b, pu = engagement(users, events, keep_zero=True)
# one-row results, so no sort is needed
pd.testing.assert_frame_equal(pd_a, a, check_dtype=False)
pd.testing.assert_frame_equal(pd_b, b, check_dtype=False)
pd.testing.assert_frame_equal(pu[["user_id", "n", "decile"]].sort_values(["decile", "user_id"]).reset_index(drop=True),
                              dec, check_dtype=False)
print("pandas, keep_zero=True:")
print(pd_b.to_string(index=False))
print("asserts passed")
