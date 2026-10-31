# Q27: cart abandonment rate and bounce rate per day of the session's first event
import sqlite3
import pandas as pd

SCHEMA = """
CREATE TABLE events(event_id INTEGER PRIMARY KEY, session_id TEXT, user_id INTEGER, event_ts TEXT, event_name TEXT);
INSERT INTO events VALUES
 (1, 'A',1,'2024-03-01 09:00:00','page_view'),
 (2, 'A',1,'2024-03-01 09:01:00','add_to_cart'),
 (3, 'A',1,'2024-03-01 09:02:00','purchase'),
 (4, 'B',2,'2024-03-01 10:00:00','page_view'),
 (5, 'B',2,'2024-03-01 10:01:00','add_to_cart'),
 (6, 'C',3,'2024-03-01 11:00:00','page_view'),
 (7, 'D',4,'2024-03-01 12:00:00','purchase'),
 (8, 'D',4,'2024-03-01 12:01:00','add_to_cart'),
 (9, 'E',5,'2024-03-01 13:00:00','add_to_cart'),
 (10,'F',6,'2024-03-02 09:00:00','page_view'),
 (11,'F',6,'2024-03-02 09:01:00','add_to_cart'),
 (12,'G',6,'2024-03-02 18:00:00','purchase'),
 (13,'H',7,'2024-03-02 10:00:00','page_view'),
 (14,'H',7,'2024-03-02 10:01:00','page_view'),
 (15,'I',8,'2024-03-03 10:00:00','page_view');
"""

SQL_MAIN = """
WITH s AS (
  SELECT session_id,
         date(MIN(event_ts)) AS day,
         COUNT(*) AS n_events,
         MAX(event_name = 'add_to_cart') AS has_cart,
         MAX(event_name = 'purchase') AS has_purchase,
         MAX(event_name = 'page_view') AS has_view
  FROM events
  GROUP BY session_id
)
SELECT day,
       COUNT(*) AS sessions,
       SUM(has_cart) AS cart_sessions,
       SUM(has_cart = 1 AND has_purchase = 0) AS abandoned,
       ROUND(SUM(has_cart = 1 AND has_purchase = 0) * 1.0 / NULLIF(SUM(has_cart), 0), 2) AS abandonment_rate,
       SUM(n_events = 1) AS bounce_any_event,
       ROUND(SUM(n_events = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_any,
       SUM(n_events = 1 AND has_view = 1) AS bounce_one_page_view,
       ROUND(SUM(n_events = 1 AND has_view = 1) * 1.0 / COUNT(*), 2) AS bounce_rate_pv
FROM s
GROUP BY day
ORDER BY day
"""
# variant: a purchase only completes the cart if it happens at or after the first add_to_cart
SQL_ORDERED = """
WITH s AS (
  SELECT session_id, date(MIN(event_ts)) AS day,
         MIN(CASE WHEN event_name = 'add_to_cart' THEN event_ts END) AS first_cart,
         MAX(CASE WHEN event_name = 'purchase' THEN event_ts END) AS last_purchase
  FROM events GROUP BY session_id
)
SELECT day,
       SUM(first_cart IS NOT NULL) AS cart_sessions,
       SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) AS abandoned,
       ROUND(SUM(first_cart IS NOT NULL AND (last_purchase IS NULL OR last_purchase < first_cart)) * 1.0 /
             NULLIF(SUM(first_cart IS NOT NULL), 0), 2) AS abandonment_rate_ordered
FROM s GROUP BY day ORDER BY day
"""

con = sqlite3.connect(":memory:")
con.executescript(SCHEMA)
sql_main = pd.read_sql_query(SQL_MAIN, con)
sql_ord = pd.read_sql_query(SQL_ORDERED, con)
print("SQL (abandoned = cart and no purchase anywhere in the session):")
print(sql_main.to_string(index=False))
print("SQL variant (purchase must be at or after the first add_to_cart):")
print(sql_ord.to_string(index=False))

events = pd.read_sql_query("SELECT * FROM events", con)

# pd:main
def session_metrics(events):
    e = events.assign(cart=events["event_name"] == "add_to_cart",
                      buy=events["event_name"] == "purchase",
                      view=events["event_name"] == "page_view")
    s = e.groupby("session_id").agg(first_ts=("event_ts", "min"), n_events=("event_id", "size"),
                                    has_cart=("cart", "max"), has_purchase=("buy", "max"),
                                    has_view=("view", "max")).reset_index()
    s["day"] = s["first_ts"].str[:10]
    s["abandon"] = s["has_cart"] & ~s["has_purchase"]
    s["bounce_any"] = s["n_events"] == 1
    s["bounce_pv"] = s["bounce_any"] & s["has_view"]
    out = s.groupby("day").agg(sessions=("session_id", "size"), cart_sessions=("has_cart", "sum"),
                               abandoned=("abandon", "sum"), bounce_any_event=("bounce_any", "sum"),
                               bounce_one_page_view=("bounce_pv", "sum")).reset_index()
    out["abandonment_rate"] = (out["abandoned"] / out["cart_sessions"].where(out["cart_sessions"] != 0)).round(2)
    out["bounce_rate_any"] = (out["bounce_any_event"] / out["sessions"]).round(2)
    out["bounce_rate_pv"] = (out["bounce_one_page_view"] / out["sessions"]).round(2)
    return out[["day", "sessions", "cart_sessions", "abandoned", "abandonment_rate",
                "bounce_any_event", "bounce_rate_any", "bounce_one_page_view", "bounce_rate_pv"]]
# pd:end

pd_main = session_metrics(events)
# compare after sorting by day (SQL result is already in that order)
pd.testing.assert_frame_equal(pd_main.sort_values("day").reset_index(drop=True), sql_main, check_dtype=False)
print("pandas:")
print(pd_main.to_string(index=False))
print("asserts passed")
