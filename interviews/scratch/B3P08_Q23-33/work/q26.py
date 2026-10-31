# Q26: notification and email funnel: unique opens, unique clicks, open rate, CTOR, CTR over sent
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE sends(send_id INTEGER PRIMARY KEY, user_id INTEGER, channel TEXT, sent_ts TEXT);
CREATE TABLE opens(send_id INTEGER, open_ts TEXT);
CREATE TABLE clicks(send_id INTEGER, click_ts TEXT);
INSERT INTO sends VALUES
 (1,1,'push', '2024-03-01 09:00:00'),(2,1,'push', '2024-03-02 09:00:00'),
 (3,2,'push', '2024-03-01 09:00:00'),(4,3,'push', '2024-03-01 09:00:00'),
 (5,1,'email','2024-03-01 08:00:00'),(6,2,'email','2024-03-01 08:00:00'),
 (7,2,'email','2024-03-02 08:00:00'),(8,3,'email','2024-03-01 08:00:00');
INSERT INTO opens VALUES
 (1,'2024-03-01 09:01:00'),(1,'2024-03-01 20:00:00'),(2,'2024-03-02 09:02:00'),
 (5,'2024-03-01 08:05:00'),(5,'2024-03-01 08:06:00'),(5,'2024-03-02 07:00:00'),
 (7,'2024-03-02 08:10:00');
INSERT INTO clicks VALUES
 (1,'2024-03-01 09:01:30'),
 (3,'2024-03-01 09:30:00'),
 (5,'2024-03-01 08:05:30'),(5,'2024-03-01 08:07:00'),
 (6,'2024-03-01 12:00:00'),
 (8,'2024-03-01 13:00:00');
"""

SQL_MAIN = """
WITH f AS (
  SELECT s.send_id, s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens  o WHERE o.send_id = s.send_id) AS opened,
         EXISTS (SELECT 1 FROM clicks c WHERE c.send_id = s.send_id) AS clicked
  FROM sends s
)
SELECT channel,
       COUNT(*) AS sent,
       SUM(opened) AS unique_opens,
       SUM(clicked) AS unique_clicks,
       ROUND(SUM(opened) * 1.0 / COUNT(*), 2) AS open_rate,
       ROUND(SUM(clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor,
       ROUND(SUM(clicked) * 1.0 / COUNT(*), 2) AS ctr,
       SUM(clicked AND NOT opened) AS click_without_open,
       ROUND(SUM(opened AND clicked) * 1.0 / NULLIF(SUM(opened), 0), 2) AS ctor_clicked_and_opened
FROM f
GROUP BY channel
ORDER BY channel
"""
SQL_RAW = """
SELECT s.channel,
       (SELECT COUNT(*) FROM opens  o JOIN sends x ON x.send_id = o.send_id WHERE x.channel = s.channel) AS open_events,
       (SELECT COUNT(*) FROM clicks c JOIN sends x ON x.send_id = c.send_id WHERE x.channel = s.channel) AS click_events,
       COUNT(*) AS sent
FROM sends s GROUP BY s.channel ORDER BY s.channel
"""
SQL_USER = """
WITH f AS (
  SELECT s.user_id, s.channel,
         EXISTS (SELECT 1 FROM opens o WHERE o.send_id = s.send_id) AS opened
  FROM sends s
)
SELECT channel, COUNT(DISTINCT user_id) AS users_sent,
       COUNT(DISTINCT CASE WHEN opened THEN user_id END) AS users_opened,
       ROUND(COUNT(DISTINCT CASE WHEN opened THEN user_id END) * 1.0 / COUNT(DISTINCT user_id), 2) AS user_open_rate
FROM f GROUP BY channel ORDER BY channel
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
print("SQL, each send counted once:")
print(sql_main.to_string(index=False))
raw = pd.read_sql_query(SQL_RAW, con)
raw["raw_open_rate"] = (raw["open_events"] / raw["sent"]).round(2)
raw["raw_click_over_open_events"] = (raw["click_events"] / raw["open_events"]).round(2)
print("SQL, raw event counts (wrong rates):")
print(raw.to_string(index=False))
sql_user = pd.read_sql_query(SQL_USER, con)
print("SQL, user-level open rate:")
print(sql_user.to_string(index=False))

sends = pd.read_sql_query("SELECT * FROM sends", con)
opens = pd.read_sql_query("SELECT * FROM opens", con)
clicks = pd.read_sql_query("SELECT * FROM clicks", con)

# pd:main
def notification_funnel(sends, opens, clicks):
    f = sends.assign(opened=sends["send_id"].isin(opens["send_id"]),
                     clicked=sends["send_id"].isin(clicks["send_id"]))
    f["both"] = f["opened"] & f["clicked"]
    f["click_no_open"] = f["clicked"] & ~f["opened"]
    out = f.groupby("channel").agg(sent=("send_id", "size"), unique_opens=("opened", "sum"),
                                   unique_clicks=("clicked", "sum"),
                                   click_without_open=("click_no_open", "sum"),
                                   both=("both", "sum")).reset_index()
    opened = out["unique_opens"].where(out["unique_opens"] != 0)
    out["open_rate"] = (out["unique_opens"] / out["sent"]).round(2)
    out["ctor"] = (out["unique_clicks"] / opened).round(2)
    out["ctr"] = (out["unique_clicks"] / out["sent"]).round(2)
    out["ctor_clicked_and_opened"] = (out["both"] / opened).round(2)
    return out[["channel", "sent", "unique_opens", "unique_clicks", "open_rate", "ctor", "ctr",
                "click_without_open", "ctor_clicked_and_opened"]]
# pd:end

pd_main = notification_funnel(sends, opens, clicks)
# compare after sorting by channel (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_main.sort_values("channel").reset_index(drop=True), sql_main, check_dtype=False)
u = sends.assign(opened=sends["send_id"].isin(opens["send_id"]))
pd_user = (u.groupby("channel").apply(lambda g: pd.Series({
    "users_sent": g["user_id"].nunique(), "users_opened": g.loc[g["opened"], "user_id"].nunique()}),
    include_groups=False).reset_index())
pd_user["user_open_rate"] = (pd_user["users_opened"] / pd_user["users_sent"]).round(2)
pd.testing.assert_frame_equal(pd_user, sql_user, check_dtype=False)
print("pandas:")
print(pd_main.to_string(index=False))
print("asserts passed")
